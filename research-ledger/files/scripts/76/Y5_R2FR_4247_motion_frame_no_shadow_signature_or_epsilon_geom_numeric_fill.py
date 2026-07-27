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

CHECKPOINT = "4247"
CLAIM_ID = "L-088"
BRANCH = "MTS_R2FR_Y5_MOTION_FRAME_NOSHADOW_OR_EPSILON_GEOM_NUMERIC_FILL_4247"
DECISION = "MOTION_FRAME_NOSHADOW_NOT_PARENT_SIGNED_EPSILON_GEOM_NUMERIC_FILL_CONTRACT_READY_NONCLAIM"
MARKER = "PPC4161_MOTION_FRAME_NOSHADOW_EPSILON_GEOM_FILL_4247"
PACKET_MARKER = "PPC4161_PACKET_MOTION_FRAME_NOSHADOW_EPSILON_GEOM_FILL_4247"
NEXT_TARGET = "4248-Y5-R2FR-epsilon-geom-profile-sampler-or-coframe-shadow-bound-first-row.md"

FORMAL_PATH = FORMAL / "263-PPC4161-motion-frame-no-shadow-signature-or-epsilon-geom-numeric-fill.md"
DOC_PATH = POST / "4247-Y5-R2FR-motion-frame-no-shadow-signature-or-epsilon-geom-numeric-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4247_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4247_00_4246_next": SourceSpec(
        "SRC4247_00_4246_next",
        SOURCE_DIR / "P8_Y5_R2FR_4246_NEXT_TARGET.csv",
        "4247-Y5-R2FR-motion-frame-no-shadow-signature-or-epsilon-geom-numeric-fill.md",
        "4246 selected the motion-frame/no-shadow or epsilon_geom numeric-fill target.",
    ),
    "SRC4247_01_4246_formal": SourceSpec(
        "SRC4247_01_4246_formal",
        FORMAL / "262-PPC4161-Hperp-geometry-zero-certificate-or-epsilon-geom-profile-fill.md",
        "A_MF/no-shadow for Hperp",
        "4246 named the exact geometry-zero parent-signature target.",
    ),
    "SRC4247_02_4246_profile": SourceSpec(
        "SRC4247_02_4246_profile",
        SOURCE_DIR / "P8_Y5_R2FR_4246_EPSILON_GEOM_PROFILE_ROW.csv",
        "epsilon_Oloc",
        "4246 decomposed epsilon_geom profile row.",
    ),
    "SRC4247_03_motion_frame_missing": SourceSpec(
        "SRC4247_03_motion_frame_missing",
        FORMAL / "198-PPC4161-motion-frame-symmetry-parent-signature-gate.md",
        "A_MF_PARENT_SIGNATURE_NOT_FOUND",
        "Current corpus does not parent-sign A_MF.",
    ),
    "SRC4247_04_AMF_contract": SourceSpec(
        "SRC4247_04_AMF_contract",
        FORMAL / "199-PPC4161-motion-frame-axiom-adoption-consequences-and-test-contract.md",
        "A_MF_adoption_contract_written = true",
        "A_MF adoption contract exists as a conditional contract.",
    ),
    "SRC4247_05_AMF_not_EH": SourceSpec(
        "SRC4247_05_AMF_not_EH",
        FORMAL / "199-PPC4161-motion-frame-axiom-adoption-consequences-and-test-contract.md",
        "Palatini_EH_forced_by_A_MF_alone = false",
        "A_MF alone does not force Palatini/EH.",
    ),
    "SRC4247_06_IR_selector": SourceSpec(
        "SRC4247_06_IR_selector",
        FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md",
        "selector_assumptions_parent_derived = false",
        "IR selector assumptions remain conditional.",
    ),
    "SRC4247_07_solder_fail": SourceSpec(
        "SRC4247_07_solder_fail",
        FORMAL / "142-owner-spacetime-solder-map-theorem.md",
        "bulk owner-connection route failed at the solder map.",
        "Owner-spacetime solder backup fails as a bulk derivation.",
    ),
    "SRC4247_08_same_coframe": SourceSpec(
        "SRC4247_08_same_coframe",
        FORMAL / "221-PPC4161-EH-coframe-parent-signature-or-Kperp-score.md",
        "same observed coframe for matter, EM, clocks and rods;",
        "Same observed coframe is a six-clause parent gate.",
    ),
    "SRC4247_09_projector_zero": SourceSpec(
        "SRC4247_09_projector_zero",
        FORMAL / "230-PPC4161-projector-stress-curl-zero-or-bound.md",
        "D_v e_obs = 0",
        "Projector/coframe zero only under q-basic observed-coframe selector.",
    ),
    "SRC4247_10_EH_false": SourceSpec(
        "SRC4247_10_EH_false",
        FORMAL / "197-PPC4161-EH-local-metric-principal-block-origin-gate.md",
        "current_MTS_EH_derivation = false",
        "EH/local metric origin is not currently parent-derived.",
    ),
    "SRC4247_11_signature_policy": SourceSpec(
        "SRC4247_11_signature_policy",
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "The selector clauses are action-level signatures.",
        "A missing selector clause cannot be set to zero silently.",
    ),
}


EPSILON_PIECES = [
    (
        "epsilon_Oloc",
        "observed local metric/readout variation from Hperp",
        "norm_D_Hperp_Oloc",
        "PPN;clock;R10;orbital",
        "needs local observable/readout derivative profile",
    ),
    (
        "epsilon_coframe",
        "same-frame/coframe variation from Hperp",
        "norm_D_Hperp_eobs",
        "PPN;WEP;clock;Maxwell_Hodge",
        "needs A_MF/no-shadow or coframe derivative profile",
    ),
    (
        "epsilon_projector",
        "projector/domain/denominator geometry leakage",
        "abs_R_domain_plus_R_denominator",
        "PPN;R10;source_readout",
        "needs projector/domain residual profile",
    ),
    (
        "epsilon_wall",
        "active selector-wall or boundary-projector geometry leakage",
        "abs_R_wall",
        "local_boundary;PPN;clock",
        "needs no-wall certificate or wall profile",
    ),
    (
        "epsilon_Hodge_geom",
        "Hodge/readout geometry deformation not counted as EM stress",
        "abs_R_Hodge_readout",
        "EM;clock;R10",
        "needs Hodge-geometry profile separated from Maxwell stress",
    ),
]


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


def no_shadow_audit_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "NSA4247_0_AMF_contract_exists",
            "A_MF adoption contract written",
            "conditional_contract_exists",
            "SRC4247_04_AMF_contract",
            "contract can be used as a future adopted axiom, not as current derivation",
        ),
        (
            "NSA4247_1_AMF_parent_signed",
            "A_MF is parent-signed by current MTS corpus",
            "fail_current_corpus",
            "SRC4247_03_motion_frame_missing",
            "no-shadow cannot be adopted from A_MF yet",
        ),
        (
            "NSA4247_2_AMF_forces_EH",
            "A_MF alone forces Palatini/EH local principal block",
            "fail",
            "SRC4247_05_AMF_not_EH",
            "even adopted A_MF still needs an IR selector",
        ),
        (
            "NSA4247_3_IR_selector_parent",
            "IR normal-form selector assumptions are parent-derived",
            "fail_current_corpus",
            "SRC4247_06_IR_selector",
            "Palatini/EH remains conditional rather than derived",
        ),
        (
            "NSA4247_4_solder_backup",
            "owner-spacetime solder route supplies no-shadow without metric reentry",
            "fail_bulk_route",
            "SRC4247_07_solder_fail",
            "older owner-solder route does not close the no-shadow gap",
        ),
        (
            "NSA4247_5_same_coframe_parent",
            "same observed coframe for matter, EM, clocks and rods is parent-owned",
            "open_six_clause_gate",
            "SRC4247_08_same_coframe",
            "needed before epsilon_coframe can be zeroed",
        ),
        (
            "NSA4247_6_projector_selector",
            "projector/coframe zero theorem is available for q-basic observed-coframe selector",
            "conditional_present",
            "SRC4247_09_projector_zero",
            "useful only after Hperp no-shadow is signed",
        ),
    ]
    return [
        {
            **common(),
            "audit_id": audit_id,
            "test": test,
            "status": status,
            "source_support": source_support,
            "effect": effect,
            "adopt_no_shadow_now": "False",
            "valid_for_claim": "False",
        }
        for audit_id, test, status, source_support, effect in rows
    ]


def numeric_fill_contract_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for quantity, meaning, measurement_proxy, arenas, acquisition_note in EPSILON_PIECES:
        rows.append(
            {
                **common(),
                "quantity": quantity,
                "meaning": meaning,
                "measurement_proxy": measurement_proxy,
                "required_columns": "system_id;collar_id;Hperp_profile_id;value;uncertainty;units;norm_definition;source_path;assumptions;valid_for_claim",
                "arenas_affected": arenas,
                "numeric_value": "MISSING",
                "source_status": "MISSING_NUMERIC_PROFILE_OR_ZERO_THEOREM",
                "acquisition_note": acquisition_note,
                "valid_for_claim": "False",
            }
        )
    rows.append(
        {
            **common(),
            "quantity": "epsilon_geom",
            "meaning": "safe L1 geometry envelope for ||Dq_geom[Hperp]||",
            "measurement_proxy": "epsilon_Oloc + epsilon_coframe + epsilon_projector + epsilon_wall + epsilon_Hodge_geom",
            "required_columns": "system_id;collar_id;Hperp_profile_id;epsilon_Oloc;epsilon_coframe;epsilon_projector;epsilon_wall;epsilon_Hodge_geom;epsilon_geom_L1;units;source_path;assumptions;valid_for_claim",
            "arenas_affected": "PPN;WEP;clock;R10;orbital;EM",
            "numeric_value": "MISSING",
            "source_status": "MISSING_ALL_COMPONENT_VALUES",
            "acquisition_note": "compute only after all five component pieces have sourced values or theorem zeros",
            "valid_for_claim": "False",
        }
    )
    return rows


def template_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "system_id": "LOCAL_COLLAR_TEMPLATE",
            "collar_id": "MISSING_COLLAR_ID",
            "Hperp_profile_id": "MISSING_HPERP_PROFILE",
            "epsilon_Oloc": "MISSING",
            "epsilon_coframe": "MISSING",
            "epsilon_projector": "MISSING",
            "epsilon_wall": "MISSING",
            "epsilon_Hodge_geom": "MISSING",
            "epsilon_geom_L1": "MISSING",
            "units": "geometry_component_Dq_norm",
            "source_path": "MISSING_SOURCE_PATH",
            "assumptions": "requires local observed geometry/coframe profile or no-shadow theorem",
            "valid_for_claim": "False",
        }
    ]


def arena_projection_rows() -> List[Dict[str, str]]:
    arenas = [
        (
            "PPN",
            "delta_gamma_geom, delta_beta_geom, alpha1/alpha2/xi geometry leakage",
            "C_PPN_geom * epsilon_geom_L1",
            "MISSING_PPN_GEOMETRY_PROJECTION_CONSTANTS",
        ),
        (
            "R10",
            "short-range fifth-force geometry/readout leakage",
            "C_R10_geom(lambda) * epsilon_geom_L1",
            "MISSING_R10_GEOMETRY_KERNEL",
        ),
        (
            "clocks",
            "redshift/clock coframe and Hodge-readout leakage",
            "C_clock_geom * epsilon_geom_L1",
            "MISSING_CLOCK_SENSITIVITY_MAP",
        ),
        (
            "EM",
            "Hodge/constitutive geometry readout not counted as Hilbert EM stress",
            "C_EM_Hodge * epsilon_Hodge_geom",
            "MISSING_EM_HODGE_GEOMETRY_MAP",
        ),
        (
            "orbital",
            "observed metric/source-readout geometry leakage into GM/orbit fits",
            "C_orb_geom * epsilon_geom_L1",
            "MISSING_ORBITAL_GEOMETRY_PROJECTION",
        ),
    ]
    return [
        {
            **common(),
            "arena": arena,
            "residual": residual,
            "projection_formula": projection_formula,
            "missing_input": missing_input,
            "scoreable_now": "False",
            "valid_for_claim": "False",
        }
        for arena, residual, projection_formula, missing_input in arenas
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4247",
            "decision": DECISION,
            "scoreable_now": "False",
            "no_shadow_adopted": "False",
            "reason": "A_MF is a written conditional adoption contract but is not parent-signed; it also does not alone force Palatini/EH, and the owner-spacetime solder backup failed as a bulk derivation.",
            "selected_route": "Build the epsilon_geom numeric-fill contract and then source/bound the first component, preferably epsilon_coframe or epsilon_Oloc.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rules = [
        ("FW4247_0_no_AMF_adoption", "Do not treat the A_MF adoption contract as a parent-signed theorem."),
        ("FW4247_1_no_EH_from_AMF", "Even adopted A_MF does not force Palatini/EH without an IR selector."),
        ("FW4247_2_no_solder_shortcut", "The owner-spacetime solder bulk route failed and cannot be used as no-shadow proof."),
        ("FW4247_3_no_numeric_claim", "The epsilon_geom numeric-fill row is a template until all MISSING values are replaced by sourced values or zeros."),
        ("FW4247_4_no_arena_projection", "PPN/R10/clock/EM/orbital projections remain blocked without arena constants."),
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
            "summary": "4247 rejects current no-shadow adoption, not by vibes but by source-backed gates: A_MF is conditional, not parent-signed; A_MF does not force EH; owner-solder fails. The epsilon_geom numeric-fill contract is now ready.",
            "scoreable_now": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "task": "Build a profile sampler for epsilon_geom, starting with coframe-shadow or observed-readout leakage; keep rows invalid for claim until numeric profiles and arena projections are sourced.",
            "reason": "The derivation route now has a precise missing parent axiom; the fallback must become quantitative rather than another symbolic gap.",
            "valid_for_claim": "False",
        }
    ]


def all_generated_groups() -> List[List[Dict[str, str]]]:
    return [
        source_rows(),
        no_shadow_audit_rows(),
        numeric_fill_contract_rows(),
        template_rows(),
        arena_projection_rows(),
        decision_rows(),
        firewall_rows(),
        status_rows(),
        next_target_rows(),
    ]


def formal_doc() -> str:
    return f"""
# 263 - PPC4161 motion-frame no-shadow signature or epsilon_geom numeric fill

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4247 does not adopt `A_MF`, does not prove `Dq_geom[Hperp]=0`, does not derive local GR, and does not score PPN/R10/clock/orbital safety.

## No-Shadow Attempt

4246 left the geometry zero route at:

```text
A_MF/no-shadow for Hperp
=> Dq_geom[Hperp]=0.
```

The sweep finds:

```text
A_MF_adoption_contract_written = true,
A_MF_PARENT_SIGNATURE_NOT_FOUND,
Palatini_EH_forced_by_A_MF_alone = false,
selector_assumptions_parent_derived = false,
bulk owner-connection route failed at the solder map.
```

So the exact no-shadow certificate cannot be adopted from the current corpus. This is not a dead end; it means the target is now clean:

```text
Either parent-sign A_MF + IR normal-form + no-shadow,
or treat epsilon_geom as a sourced local residual.
```

## Numeric Fill Contract

The retained safe envelope is:

```text
epsilon_geom_L1
= epsilon_Oloc
+ epsilon_coframe
+ epsilon_projector
+ epsilon_wall
+ epsilon_Hodge_geom.
```

Each piece must be either theorem-zero or numerically filled:

```text
epsilon_Oloc        : observed local metric/readout variation from Hperp,
epsilon_coframe     : same-frame/coframe variation from Hperp,
epsilon_projector   : projector/domain/denominator geometry leakage,
epsilon_wall        : active selector-wall or boundary-projector leakage,
epsilon_Hodge_geom  : Hodge/readout geometry deformation not counted as EM stress.
```

The template row is deliberately invalid for claim until all `MISSING` values are replaced by source-backed numbers or theorem zeros.

## Arena Projections

Even after `epsilon_geom` is filled, local evidence still requires projection constants:

```text
PPN    : C_PPN_geom,
R10    : C_R10_geom(lambda),
clocks : C_clock_geom,
EM     : C_EM_Hodge,
orbit  : C_orb_geom.
```

That prevents a common cheat: using a local geometry norm as if it were already a PPN or R10 residual.

## Next Target

`{NEXT_TARGET}` should build the first real sampler/fill row for `epsilon_geom`, starting with either `epsilon_coframe` or `epsilon_Oloc`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4247 - motion-frame no-shadow signature or epsilon_geom numeric fill

**Status:** `{DECISION}`.

## Result

No-shadow is not adopted. The source-backed reasons are:

```text
A_MF_PARENT_SIGNATURE_NOT_FOUND,
Palatini_EH_forced_by_A_MF_alone = false,
selector_assumptions_parent_derived = false,
bulk owner-connection route failed at the solder map.
```

## What improved

`epsilon_geom` is now a numeric-fill contract, not just a symbol:

```text
epsilon_geom_L1
= epsilon_Oloc
+ epsilon_coframe
+ epsilon_projector
+ epsilon_wall
+ epsilon_Hodge_geom.
```

The template rows are intentionally `valid_for_claim=false`.

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
        "claim": "4247 tests the motion-frame/no-shadow route for Dq_geom[Hperp]. A_MF is found to be a conditional adoption contract, not a parent-signed theorem; A_MF alone does not force EH; the owner-solder bulk route fails. Therefore epsilon_geom is promoted to a numeric-fill contract with five sourced pieces.",
        "current_evidence": "4247 source register, no-shadow audit, epsilon_geom numeric-fill contract, template row, arena projection requirements, decision and firewall.",
        "status": "private_no_shadow_rejected_numeric_fill_contract_nonclaim",
        "next_test": "Build the epsilon_geom profile sampler and fill the first coframe-shadow or observed-readout row with sourced values or theorem zeros.",
        "key_risk": "Adopting A_MF or a solder map by assumption would smuggle the local observed-geometry shadow zero.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 motion-frame no-shadow audit and epsilon_geom fill contract

Marker: `{MARKER}`

4247 rejects current no-shadow adoption:

```text
A_MF_PARENT_SIGNATURE_NOT_FOUND,
Palatini_EH_forced_by_A_MF_alone = false,
selector_assumptions_parent_derived = false.
```

The geometry residual is now a numeric-fill contract:

```text
epsilon_geom_L1 = epsilon_Oloc + epsilon_coframe + epsilon_projector + epsilon_wall + epsilon_Hodge_geom.
```
"""
    packet_block = f"""
## Packet Update - no-shadow audit / epsilon_geom fill

Marker: `{PACKET_MARKER}`

The motion-frame no-shadow route remains conditional, so the local geometry branch moves to a real `epsilon_geom` profile-fill contract with five explicit pieces and blocked arena projections.
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
    audit = no_shadow_audit_rows()
    fill = numeric_fill_contract_rows()
    template = template_rows()
    arenas = arena_projection_rows()
    all_rows = [row for group in all_generated_groups() for row in group]

    add("VAL4247_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources), "source register")
    add("VAL4247_1_needles_found", "all source needles found", all(row["required_text_found"] == "True" for row in sources), "source register")
    add("VAL4247_2_AMF_missing", "A_MF parent signature is failed/missing", any(row["audit_id"] == "NSA4247_1_AMF_parent_signed" and row["status"] == "fail_current_corpus" for row in audit), "no-shadow audit")
    add("VAL4247_3_AMF_not_EH", "A_MF alone does not force EH", any(row["audit_id"] == "NSA4247_2_AMF_forces_EH" and row["status"] == "fail" for row in audit), "no-shadow audit")
    add("VAL4247_4_solder_fails", "owner-solder bulk route fails", any(row["audit_id"] == "NSA4247_4_solder_backup" and row["status"] == "fail_bulk_route" for row in audit), "no-shadow audit")
    add("VAL4247_5_no_adoption", "no-shadow is not adopted", all(row["adopt_no_shadow_now"] == "False" for row in audit), "no-shadow audit")
    add("VAL4247_6_fill_pieces", "numeric fill has five pieces plus total", len(fill) == 6, "numeric fill contract")
    add("VAL4247_7_fill_piece_names", "fill includes all epsilon_geom pieces", {"epsilon_Oloc", "epsilon_coframe", "epsilon_projector", "epsilon_wall", "epsilon_Hodge_geom", "epsilon_geom"}.issubset({row["quantity"] for row in fill}), "numeric fill contract")
    add("VAL4247_8_template_invalid", "template row remains invalid for claim", template[0]["valid_for_claim"] == "False" and "MISSING" in template[0]["epsilon_geom_L1"], "template row")
    add("VAL4247_9_arena_blockers", "arena projections include PPN R10 clocks EM orbital", {"PPN", "R10", "clocks", "EM", "orbital"}.issubset({row["arena"] for row in arenas}), "arena requirements")
    add("VAL4247_10_decision_nonclaim", "decision keeps scoreable false", decision_rows()[0]["scoreable_now"] == "False", "decision")
    add("VAL4247_11_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4247_12_claim_register", "claims register contains L-088", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4247_13_spine_marker", "spine contains marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4247_14_packet_marker", "packet contains marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4247_15_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for row in all_rows), "all generated groups")
    add("VAL4247_16_next_target", "next target selected", next_target_rows()[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4247_SOURCE_REGISTER.csv",
        "audit": SOURCE_DIR / "P8_Y5_R2FR_4247_NO_SHADOW_SIGNATURE_AUDIT.csv",
        "fill": SOURCE_DIR / "P8_Y5_R2FR_4247_EPSILON_GEOM_NUMERIC_FILL_CONTRACT.csv",
        "template": SOURCE_DIR / "P8_Y5_R2FR_4247_EPSILON_GEOM_TEMPLATE_ROWS.csv",
        "arenas": SOURCE_DIR / "P8_Y5_R2FR_4247_ARENA_PROJECTION_REQUIREMENTS.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4247_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4247_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4247_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4247_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["audit"], no_shadow_audit_rows())
    write_csv(paths["fill"], numeric_fill_contract_rows())
    write_csv(paths["template"], template_rows())
    write_csv(paths["arenas"], arena_projection_rows())
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

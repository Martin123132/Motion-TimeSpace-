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

CHECKPOINT = "4251"
CLAIM_ID = "L-092"
BRANCH = "MTS_R2FR_Y5_HPERP_MEMORY_TRANSFER_CONSTANT_OR_REAL_PROFILE_SOURCE_4251"
DECISION = "SCALAR_MEMORY_DIRECT_TRANSFER_REJECTED_MIXED_QSHEAR_TRANSFER_OR_REAL_HPERP_PROFILE_REQUIRED_NONCLAIM"
MARKER = "PPC4161_HPERP_MEMORY_TRANSFER_OR_REAL_PROFILE_4251"
PACKET_MARKER = "PPC4161_PACKET_HPERP_MEMORY_TRANSFER_OR_REAL_PROFILE_4251"
NEXT_TARGET = "4252-Y5-R2FR-mixed-memory-Qshear-transfer-inputs-or-direct-Hperp-profile-acquisition.md"

FORMAL_PATH = FORMAL / "267-PPC4161-Hperp-memory-transfer-constant-or-real-profile-source.md"
DOC_PATH = POST / "4251-Y5-R2FR-Hperp-memory-transfer-constant-or-real-profile-source.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4251_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4251_00_4250_formal": SourceSpec(
        "SRC4251_00_4250_formal",
        FORMAL / "266-PPC4161-hU-C1-source-candidate-or-selector-leakage-inputs.md",
        "A_H <= C_HM0 M_tr + eta_H_background",
        "4250 named the missing memory-to-Hperp transfer.",
    ),
    "SRC4251_01_4250_crosswalk": SourceSpec(
        "SRC4251_01_4250_crosswalk",
        SOURCE_DIR / "P8_Y5_R2FR_4250_HPERP_MEMORY_CROSSWALK_THEOREMS.csv",
        "M_tr is not Hperp",
        "4250 no-smuggle crosswalk rows.",
    ),
    "SRC4251_02_4249_formal": SourceSpec(
        "SRC4251_02_4249_formal",
        FORMAL / "265-PPC4161-hU-response-bound-or-coframe-transfer-first-source-row.md",
        "h_U_C1 + 2 Omega_E h_U_profile + eta_Lie_frame",
        "4249 response-bound route awaiting real Hperp inputs.",
    ),
    "SRC4251_03_3794_constructor": SourceSpec(
        "SRC4251_03_3794_constructor",
        POST / "3794-Y5-R2FR-parent-BQ-owner-constructor-two-pair-CP2-or-finite-profile.md",
        "H_Q=dC1 wedge dD1+dC2 wedge dD2",
        "B_Q/H_Q two-pair constructor and profile fallback.",
    ),
    "SRC4251_04_3795_qflow": SourceSpec(
        "SRC4251_04_3795_qflow",
        POST / "3795-Y5-R2FR-Qflow-two-pair-lift-or-Bperp-profile-first-input.md",
        "Q_coh^i_j=(N_D/u3) delta^i_j",
        "Qflow one-scalar no-go and shear/eigenframe route.",
    ),
    "SRC4251_05_3799_hu": SourceSpec(
        "SRC4251_05_3799_hu",
        SOURCE_DIR / "P8_Y5_R2FR_3799_FIRST_HU_SOURCE_ROWS.csv",
        "HU3799_1_hU_response",
        "h_U response source rows.",
    ),
    "SRC4251_06_3800_rank": SourceSpec(
        "SRC4251_06_3800_rank",
        SOURCE_DIR / "P8_Y5_R2FR_3800_FULL_RANK_CLEBSCH_BASICNESS_THEOREM.csv",
        "CBT3800_1_full_rank_no_cancellation",
        "Full-rank Clebsch/symplectic gate.",
    ),
    "SRC4251_07_3801_refinement": SourceSpec(
        "SRC4251_07_3801_refinement",
        SOURCE_DIR / "P8_Y5_R2FR_3801_QOBS_QSHEAR_REFINEMENT_THEOREM.csv",
        "ker(Dq_X)=ker(Dq_obs) cap ker(DX_Q)",
        "q_X refinement theorem.",
    ),
    "SRC4251_08_4250_smoke": SourceSpec(
        "SRC4251_08_4250_smoke",
        SOURCE_DIR / "P8_Y5_R2FR_4250_UNIT_TRANSFER_SMOKE_RESULT.csv",
        "transition_h_U_response_proxy",
        "4250 smoke result to quarantine.",
    ),
    "SRC4251_09_spine_corrected": SourceSpec(
        "SRC4251_09_spine_corrected",
        FORMAL / "07-unification-spine.md",
        "h_U_response_proxy = 7.0710678118654745e-08",
        "Spine now records corrected 4250 smoke scale.",
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


def theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "HMT4251_0_target_transfer",
            "actual transfer target",
            "Need Hperp = (1-P_q) H_Q[Y_Q(m,Z)] on U_good, with H_Q=sum_i dC_i wedge dD_i and Y_Q=(C1,D1,C2,D2).",
            "TARGET_SHARPENED",
            "C_HM0/C_HM1 are derivatives of this parent map, not free constants.",
            "MISSING_PARENT_MAP_YQ_OF_MEMORY_AND_QSHEAR",
        ),
        (
            "HMT4251_1_scalar_memory_rank_no_go",
            "one-scalar memory cannot own generic Hperp",
            "If Y_Q=Y_Q(m) only, then dC_i=C_i'(m)dm and dD_i=D_i'(m)dm, so dC_i wedge dD_i=0 for every pair. Hence H_Q=0 and the scalar-memory-only transfer cannot produce generic Hperp curvature.",
            "EXACT_DIFFERENTIAL_FORM_NO_GO",
            "Rejects treating M_tr as Hperp with C_HM=1 as physics.",
            "NEED_AT_LEAST_TWO_PARENT_VARIABLE_DIRECTIONS_OR_DIRECT_PROFILE",
        ),
        (
            "HMT4251_2_mixed_memory_Qshear_route",
            "mixed memory and Q/shear transfer",
            "If Y_Q=Y_Q(m,Z^a), then dY=Y_m dm + Y_a dZ^a and H_Q contains dm wedge dZ and dZ wedge dZ pieces. A real transfer must bound these terms, not just |dm|.",
            "EXACT_CHAIN_RULE_ROUTE",
            "The viable bridge is C_mZ/C_ZZ plus Z-gradient data.",
            "MISSING_PARENT_Z_VARIABLES_AND_GRADIENT_BOUNDS",
        ),
        (
            "HMT4251_3_amplitude_bound",
            "mixed amplitude envelope",
            "A_H <= C_perp*(C_mZ M_tr Z_1 + C_ZZ Z_1^2 + eta_chart + eta_qproj + eta_background).",
            "DERIVED_BOUND_INTERFACE",
            "Replaces fake C_HM0 with sourceable mixed transfer pieces.",
            "MISSING_C_mZ_C_ZZ_Z1_ETA_VALUES",
        ),
        (
            "HMT4251_4_C1_bound",
            "mixed C1 envelope",
            "h_U_C1 <= C_perp1*(C_mZ M_tr (L_U/ell_tr) Z_1 + C_mZ1 M_tr Z_1 + C_ZZ1 Z_1^2 + eta_C1).",
            "DERIVED_C1_BOUND_INTERFACE",
            "Turns the 4249 C1 row into a Qshear/memory mixed-profile row.",
            "MISSING_C1_TRANSFER_AND_Z_PROFILE_VALUES",
        ),
        (
            "HMT4251_5_direct_profile_route",
            "direct Hperp profile alternative",
            "Instead of deriving the transfer map, source Hperp directly: A_H=||Hperp||_F/F_ref and h_U_C1=max||nabla Hperp||/(F_ref/L_U) on the selected U_good domain.",
            "DIRECT_SOURCE_ROUTE",
            "Bypasses the scalar-memory transfer ambiguity.",
            "MISSING_REAL_HPERP_PROFILE_SOURCE",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "mathematical_form": mathematical_form,
            "derivation_status": status,
            "result_if_signed": result,
            "missing_for_current_claim": missing,
            "valid_for_claim": "False",
        }
        for theorem_id, claim_piece, mathematical_form, status, result, missing in raw
    ]


def transfer_schema_rows() -> List[Dict[str, str]]:
    raw = [
        ("C_perp", "projection norm from H_Q to Hperp", "dimensionless", "parent/projector source or theorem"),
        ("C_mZ", "bilinear memory-Qshear curvature transfer coefficient", "dimensionless", "bound on omega_0(Y_m,Y_Z)"),
        ("C_ZZ", "pure Qshear curvature leakage coefficient", "dimensionless", "bound on omega_0(Y_Z,Y_Z)"),
        ("Z_1", "normalized Q/shear/eigenframe C1 profile", "dimensionless", "max ||dZ|| over U_good"),
        ("eta_chart", "chart transition residue", "dimensionless", "eigenframe/Pi4 chart certificate"),
        ("eta_qproj", "q projection/descent residue", "dimensionless", "projector/quotient certificate"),
        ("eta_background", "background Hperp offset at m_L", "dimensionless", "must vanish or be sourced"),
        ("C_perp1", "C1 projection/connection norm", "dimensionless", "C1 transfer norm"),
        ("C_mZ1", "first-derivative mixed-transfer coefficient", "dimensionless", "derivative of C_mZ or profiles"),
        ("C_ZZ1", "first-derivative Qshear leakage coefficient", "dimensionless", "derivative of pure Qshear term"),
        ("eta_C1", "C1 regularity residue", "dimensionless", "corners, frame, degeneracy, boundary"),
        ("Hperp_profile_path", "direct profile source path", "path", "alternative source-backed profile route"),
    ]
    return [
        {
            **common(),
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "source_requirement": requirement,
            "valid_for_claim": "False",
        }
        for symbol, definition, units, requirement in raw
    ]


def quarantine_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "candidate_id": "HU4250_LOCAL_TRANSITION_UNIT_TRANSFER_SMOKE",
            "quarantine_status": "SMOKE_ONLY_NOT_PHYSICS",
            "reason": "4251 proves scalar-memory-only Y_Q(m) gives H_Q=0, so M_tr cannot be identified with generic Hperp without mixed Q/shear variables or a direct profile.",
            "allowed_use": "pipeline scale check only",
            "forbidden_use": "local-GR/PPN/R10/clock/orbital evidence; source-backed h_U_response",
            "valid_for_claim": "False",
        }
    ]


def profile_source_rows() -> List[Dict[str, str]]:
    raw = [
        ("HPS4251_0_domain", "U_good domain", "regular quotient patch, metric/coframe, boundary support, and defect exclusions"),
        ("HPS4251_1_Hperp_amplitude", "A_H", "||Hperp||_F/F_ref sampled or theorem-bounded on U_good"),
        ("HPS4251_2_Hperp_C1", "h_U_C1", "max ||nabla Hperp||/(F_ref/L_U), with frame/anholonomy terms separated"),
        ("HPS4251_3_qstar_inverse", "C_qinv", "operator norm of q_*^-1 on the response bundle"),
        ("HPS4251_4_coframe_transfer", "C_coframe_hU", "transfer from h_U_response to epsilon_coframe in 4248"),
        ("HPS4251_5_no_cancellation", "absolute-sum guard", "all residual channels summed without cancellation unless parent identity proves it"),
    ]
    return [
        {
            **common(),
            "row_id": row_id,
            "required_object": obj,
            "source_requirement": requirement,
            "current_status": "REQUIRED_NOT_FILLED",
            "valid_for_claim": "False",
        }
        for row_id, obj, requirement in raw
    ]


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4251_0_progress",
            "direct scalar memory transfer rejected",
            "A single scalar memory transition cannot generate a generic Clebsch two-form; Y_Q(m) gives dC wedge dD=0.",
            "Do not upgrade the 4250 unit-transfer smoke row.",
        ),
        (
            "DEC4251_1_viable_route",
            "mixed memory-Qshear transfer selected",
            "A nonzero Hperp transfer needs at least one additional parent variable direction Z, or a direct Hperp profile.",
            "Move to mixed-transfer inputs C_mZ/Z_1/C_ZZ or direct profile acquisition.",
        ),
        (
            "DEC4251_2_next",
            "derive C_mZ/Z profile or source Hperp",
            "This is narrower and more physical than C_HM0 as a black-box coefficient.",
            NEXT_TARGET,
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "action": action,
            "valid_for_claim": "False",
        }
        for decision_id, decision, rationale, action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4251_0_no_Mtr_equals_Hperp", "M_tr = Hperp", "rejected by scalar-memory rank/no-go theorem"),
        ("FW4251_1_no_unit_transfer_claim", "C_HM0=C_HM1=1 as physics", "allowed only as 4250 smoke"),
        ("FW4251_2_no_one_scalar_generic_EM", "one scalar generates generic Maxwell rank", "false; pullback of a two-form to one-dimensional image vanishes"),
        ("FW4251_3_no_hidden_Z", "hide Q/shear variable Z without sourcing", "mixed route must source Z profile and transfer constants"),
        ("FW4251_4_no_arena_claim", "use 4250/4251 for PPN/R10/clock/orbital pass", "all arena claims remain blocked"),
    ]
    return [
        {
            **common(),
            "firewall_id": fid,
            "blocked_shortcut": shortcut,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for fid, shortcut, rule in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": DECISION,
            "summary": "4251 rejects scalar-memory-only transfer as a generic Hperp source and reduces the real bridge to mixed memory-Qshear transfer constants or direct Hperp profile acquisition.",
            "scoreable_now": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "objective": "Derive or source C_mZ, Z_1, C_ZZ, eta terms, and C1 mixed-transfer coefficients, or acquire a direct Hperp amplitude/C1 profile.",
            "avoid": "Do not use scalar M_tr alone as Hperp; do not claim local-GR/PPN/R10/clock/orbital closure.",
            "valid_for_claim": "False",
        }
    ]


def append_claim_row() -> None:
    path = FORMAL / "02-claims-register.csv"
    current = read_text(path)
    if f"{CLAIM_ID}," in current:
        return
    row = [
        CLAIM_ID,
        "local_gr",
        "4251 rejects the direct scalar-memory transfer shortcut: if the Clebsch owner variables depend only on one scalar memory m, H_Q=sum dC_i wedge dD_i vanishes. A real Hperp transfer therefore needs mixed memory-Qshear variables or a direct Hperp profile.",
        "4251 source register, scalar-memory rank no-go theorem, mixed memory-Qshear transfer interface, direct profile source requirements, candidate quarantine, decision and firewall.",
        "private_scalar_memory_Hperp_transfer_rejected_mixed_Qshear_or_profile_required_nonclaim",
        "Derive/source C_mZ, Z_1, C_ZZ and C1 mixed-transfer rows, or acquire a real Hperp profile.",
        "Treating the 4250 unit-transfer smoke row as physics would identify a scalar transition with a generic two-form curvature and smuggle local-GR safety.",
    ]
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow(row)


def write_formal_doc() -> None:
    text = f"""
# 267 - PPC4161 Hperp memory-transfer constant or real profile source

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4251 does not prove Hperp is small and does not prove local GR, PPN, R10, clock, or orbital safety.

## Main Result

The direct scalar-memory bridge is rejected:

```text
Y_Q = Y_Q(m) only
=> dC_i = C_i'(m) dm, dD_i = D_i'(m) dm
=> dC_i wedge dD_i = 0
=> H_Q = 0.
```

So `M_tr` alone cannot be identified with a generic `Hperp` curvature. The 4250 unit-transfer row remains a smoke test only.

## Viable Transfer Route

A nonzero parent Hperp transfer must use at least one additional parent direction:

```text
Y_Q = Y_Q(m, Z^a),
dY = Y_m dm + Y_a dZ^a.
```

Then `H_Q=Y_Q^*omega_0` contains mixed terms:

```text
dm wedge dZ,
dZ wedge dZ.
```

The sourceable bound is:

```text
A_H <= C_perp*(C_mZ M_tr Z_1 + C_ZZ Z_1^2
               + eta_chart + eta_qproj + eta_background).
```

and the C1 route is:

```text
h_U_C1 <= C_perp1*(C_mZ M_tr (L_U/ell_tr) Z_1
                  + C_mZ1 M_tr Z_1
                  + C_ZZ1 Z_1^2
                  + eta_C1).
```

## Direct Profile Alternative

If the mixed transfer cannot be derived cleanly, the honest route is a direct profile:

```text
A_H = ||Hperp||_F/F_ref,
h_U_C1 = max ||nabla Hperp||/(F_ref/L_U).
```

This can feed 4249 without pretending scalar memory alone owns a two-form.

## Next Target

`{NEXT_TARGET}` should derive/source the mixed `m,Z` transfer coefficients or acquire a real `Hperp` profile.
"""
    write_text(FORMAL_PATH, text)


def write_checkpoint_doc() -> None:
    text = f"""
# 4251 - Hperp memory-transfer constant or real profile source

**Status:** `{DECISION}`.

## Result

The scalar-only transfer route fails as a generic Hperp source:

```text
Y_Q(m) => H_Q=sum_i dC_i wedge dD_i = 0.
```

Therefore the 4250 smoke row is quarantined. A real bridge needs mixed memory-Qshear variables:

```text
A_H <= C_perp*(C_mZ M_tr Z_1 + C_ZZ Z_1^2 + eta...)
```

or a direct Hperp profile.

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, text)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 Hperp memory-transfer or real profile source

Marker: `{MARKER}`

4251 rejects the tempting shortcut:

```text
Y_Q=Y_Q(m) only => H_Q=sum_i dC_i wedge dD_i = 0.
```

Thus `M_tr` alone cannot be promoted to `Hperp`. A real transfer needs mixed parent variables:

```text
A_H <= C_perp*(C_mZ M_tr Z_1 + C_ZZ Z_1^2 + eta...),
```

or a direct `Hperp` profile. This keeps the local-GR route derivation-first instead of hiding the curvature in a scalar proxy.
"""
    packet_block = f"""
## Packet Update - Hperp memory transfer or real profile

Marker: `{PACKET_MARKER}`

The packet now quarantines the 4250 unit-transfer smoke row. Scalar memory alone cannot own generic two-form curvature; the next bridge must be mixed memory-Qshear transfer or direct Hperp profile acquisition.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validation_rows(outputs: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = source_rows()
    theorems = theorem_rows()
    validations = [
        ("VAL4251_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4251_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        ("VAL4251_2_scalar_no_go_present", any(row["theorem_id"] == "HMT4251_1_scalar_memory_rank_no_go" for row in theorems), "scalar memory no-go theorem emitted"),
        ("VAL4251_3_mixed_route_present", any(row["theorem_id"] == "HMT4251_2_mixed_memory_Qshear_route" for row in theorems), "mixed transfer route emitted"),
        ("VAL4251_4_direct_profile_present", any(row["theorem_id"] == "HMT4251_5_direct_profile_route" for row in theorems), "direct profile route emitted"),
        ("VAL4251_5_quarantine_nonclaim", all(row["valid_for_claim"] == "False" for row in quarantine_rows()), "4250 smoke row quarantined"),
        ("VAL4251_6_firewall_closed", all(row["claim_allowed"] == "False" for row in firewall_rows()), "firewall gates closed"),
        ("VAL4251_7_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4251_8_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4251_9_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4251_10_spine_marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine marker present"),
        ("VAL4251_11_packet_marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet marker present"),
    ]
    for name, path in outputs.items():
        validations.append((f"VAL4251_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "source_register": SOURCE_DIR / "P8_Y5_R2FR_4251_SOURCE_REGISTER.csv",
        "transfer_theorems": SOURCE_DIR / "P8_Y5_R2FR_4251_HPERP_MEMORY_TRANSFER_THEOREMS.csv",
        "transfer_schema": SOURCE_DIR / "P8_Y5_R2FR_4251_MIXED_TRANSFER_INPUT_SCHEMA.csv",
        "candidate_quarantine": SOURCE_DIR / "P8_Y5_R2FR_4251_4250_CANDIDATE_QUARANTINE.csv",
        "direct_profile": SOURCE_DIR / "P8_Y5_R2FR_4251_DIRECT_HPERP_PROFILE_REQUIREMENTS.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4251_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4251_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4251_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4251_NEXT_TARGET.csv",
    }

    write_formal_doc()
    write_checkpoint_doc()
    append_claim_row()
    update_spine_and_packet()

    write_csv(outputs["source_register"], source_rows())
    write_csv(outputs["transfer_theorems"], theorem_rows())
    write_csv(outputs["transfer_schema"], transfer_schema_rows())
    write_csv(outputs["candidate_quarantine"], quarantine_rows())
    write_csv(outputs["direct_profile"], profile_source_rows())
    write_csv(outputs["decision"], decision_rows())
    write_csv(outputs["firewall"], firewall_rows())
    write_csv(outputs["status"], status_rows())
    write_csv(outputs["next_target"], next_target_rows())
    write_csv(VALIDATION_PATH, validation_rows(outputs))

    validation = csv_rows(VALIDATION_PATH)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(outputs)} csv artifacts")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()

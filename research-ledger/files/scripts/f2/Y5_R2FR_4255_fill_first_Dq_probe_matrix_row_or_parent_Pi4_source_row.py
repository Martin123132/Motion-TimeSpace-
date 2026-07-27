from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4255"
CLAIM_ID = "L-096"
BRANCH = "MTS_R2FR_Y5_FILL_FIRST_DQ_PROBE_MATRIX_ROW_OR_PARENT_PI4_SOURCE_ROW_4255"
DECISION = "DQ_COORDINATE_PROBE_MATRIX_FILLED_AS_SEMINORM_SMOKE_PHYSICAL_NORM_BRIDGE_STILL_MISSING_NONCLAIM"
MARKER = "PPC4161_DQ_PROBE_MATRIX_OR_PARENT_PI4_SOURCE_4255"
PACKET_MARKER = "PPC4161_PACKET_DQ_PROBE_MATRIX_OR_PARENT_PI4_SOURCE_4255"
NEXT_TARGET = "4256-Y5-R2FR-fill-Dq-component-values-or-physical-Hperp-Dq-norm-equivalence.md"

FORMAL_PATH = FORMAL / "271-PPC4161-fill-first-Dq-probe-matrix-row-or-parent-Pi4-source-row.md"
DOC_PATH = POST / "4255-Y5-R2FR-fill-first-Dq-probe-matrix-row-or-parent-Pi4-source-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4255_VALIDATION.csv"

MATRIX_CANDIDATE_4254_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_SOURCE_PROBE_MATRIX_CANDIDATE.csv"
LOCAL_MATRIX_PATH = SOURCE_DIR / "P8_Y5_R2FR_4255_DQ_COORDINATE_PROBE_MATRIX.csv"

PROBES = (
    "Dq_geom",
    "Dq_tau",
    "Dq_matter",
    "Dq_source_readout",
    "Dq_theta_marker",
    "Dq_boundary_projector",
    "Dq_EM",
    "Dq_coeff",
)

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4255_00_4254_formal": SourceSpec(
        "SRC4255_00_4254_formal",
        FORMAL / "270-PPC4161-fill-source-probe-rank-or-parent-Pi4-Jacobian-row.md",
        "sigma_S^2 = lambda_min",
        "4254 weighted rank gate.",
    ),
    "SRC4255_01_4254_next": SourceSpec(
        "SRC4255_01_4254_next",
        SOURCE_DIR / "P8_Y5_R2FR_4254_NEXT_TARGET.csv",
        "Fill either a source-probe matrix",
        "4254 target for matrix/component/constants or Pi4 pack.",
    ),
    "SRC4255_02_4243_matrix": SourceSpec(
        "SRC4255_02_4243_matrix",
        SOURCE_DIR / "P8_Y5_R2FR_4243_DQ_COMPONENT_BOUND_MATRIX.csv",
        "Dq_geom[H_L]",
        "Dq component names and missing value audit.",
    ),
    "SRC4255_03_4245_split": SourceSpec(
        "SRC4255_03_4245_split",
        FORMAL / "261-PPC4161-HL-qbasic-strip-and-Dq-bound-first-input-row.md",
        "Dq_i[Hperp]",
        "H_q strip reducing live Dq rows to Hperp-only rows.",
    ),
    "SRC4255_04_4254_audit": SourceSpec(
        "SRC4255_04_4254_audit",
        SOURCE_DIR / "P8_Y5_R2FR_4254_CURRENT_DQ_NUMERIC_AUDIT.csv",
        "NOT_NUMERIC_SOURCE_BACKED",
        "Current audit says Dq values are still not numeric.",
    ),
    "SRC4255_05_4252_template": SourceSpec(
        "SRC4255_05_4252_template",
        SOURCE_DIR / "P8_Y5_R2FR_4252_JACOBIAN_COMPONENTS_TEMPLATE.csv",
        "derivative_direction",
        "Parallel parent Pi4/X_m/X_a route remains available.",
    ),
    "SRC4255_06_4253_guard": SourceSpec(
        "SRC4255_06_4253_guard",
        FORMAL / "269-PPC4161-source-Jacobian-or-first-direct-Hperp-profile-fill.md",
        "Poynting/Hodge Guard",
        "Non-double-counting and no-free-Pi4 guard carried forward.",
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


def dq_coordinate_matrix_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    candidate_id = "DQ_COORDINATE_SEMINORM_SMOKE_4255"
    source_path = str(FORMAL_PATH)
    for row_type in ("amplitude", "C1"):
        for probe_id in PROBES:
            for basis_id in PROBES:
                rows.append(
                    {
                        **common(),
                        "candidate_id": candidate_id,
                        "row_type": row_type,
                        "probe_id": probe_id,
                        "basis_id": basis_id,
                        "coefficient": "1.0" if probe_id == basis_id else "0.0",
                        "units": "Dq_coordinate_seminorm_only",
                        "source_path": source_path,
                        "claim_authority": "DQ_COORDINATE_SEMINORM_NOT_PHYSICAL_HPERP_NORM",
                        "valid_for_claim": "False",
                    }
                )
    return rows


def theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DQM4255_0_identity_matrix",
            "Dq-coordinate source-probe matrix",
            "Define a Dq-coordinate basis e_i by the eight named Dq_i[Hperp] components. In that seminorm only, S_Dq=I and sigma_Dq=1.",
            "EXACT_COORDINATE_DEFINITION_NONCLAIM",
            "Fills the matrix socket for runner testing without inventing physical Hperp data.",
            "MISSING_PHYSICAL_NORM_EQUIVALENCE",
        ),
        (
            "DQM4255_1_physical_norm_guard",
            "physical Hperp norm bridge",
            "To turn Dq-coordinate rank into A_H, one still needs ||Hperp||_F/F_ref <= C_HDq ||Dq[Hperp]||_W + eta_Dq_kernel on U_good.",
            "REQUIRED_GUARD_THEOREM",
            "This is the real injectivity/norm-equivalence condition behind sigma_S>0.",
            "MISSING_C_HDq_AND_ETA_DQ_KERNEL",
        ),
        (
            "DQM4255_2_kernel_no_go",
            "Dq-kernel obstruction",
            "If there exists nonzero Hperp in ker(Dq_*) on the selected sector, the Dq-coordinate matrix can be full rank in its own coordinates but still fail to bound the physical Hperp norm.",
            "NO_SMUGGLE_OBSTRUCTION",
            "Prevents declaring local-GR safety from Dq components alone.",
            "MISSING_DQ_KERNEL_ZERO_PROOF",
        ),
        (
            "DQM4255_3_C1_guard",
            "C1 norm bridge",
            "For the 4249 C1 route, the analogous bridge is ||nabla Hperp||/(F_ref/L_U) <= C_HDq1 ||nabla Dq[Hperp]||_W + C_comm ||Dq[Hperp]||_W + eta_Dq_C1_kernel.",
            "REQUIRED_C1_GUARD_THEOREM",
            "Separates derivative control from amplitude control.",
            "MISSING_C_HDq1_C_COMM_ETA_DQ_C1_KERNEL",
        ),
        (
            "DQM4255_4_parent_Pi4_parallel",
            "parent Pi4 alternative",
            "If parent Pi4/X_m/X_a rows arrive first, use 4252; if Dq component/norm-equivalence rows arrive first, use 4254/4255.",
            "ROUTE_SELECTION_THEOREM",
            "Both routes feed A_H/h_U_C1 into 4249 without scalar-memory smuggling.",
            "MISSING_FIRST_SOURCE_PACK",
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


def rank_smoke_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "candidate_id": "DQ_COORDINATE_SEMINORM_SMOKE_4255",
            "row_type": "rank_smoke",
            "matrix_shape": "8x8_identity_for_amplitude_and_C1",
            "sigma_Dq_amplitude": "1.000000000000e+00",
            "sigma_Dq_C1": "1.000000000000e+00",
            "interpretation": "rank is only in the Dq-coordinate seminorm; it is not a physical Hperp norm pass",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def missing_bridge_rows() -> List[Dict[str, str]]:
    raw = [
        ("C_HDq", "physical Hperp norm from weighted Dq norm", "||Hperp||_F/F_ref <= C_HDq ||Dq[Hperp]||_W + eta_Dq_kernel", "MISSING_PHYSICAL_NORM_EQUIVALENCE"),
        ("eta_Dq_kernel", "unseen Dq-kernel residue", "sup ||P_kerDq Hperp||_F/F_ref on U_good", "MISSING_DQ_KERNEL_ZERO_OR_BOUND"),
        ("C_HDq1", "physical C1 norm from differentiated Dq norm", "||nabla Hperp||/(F_ref/L_U) <= C_HDq1 ||nabla Dq[Hperp]||_W + ...", "MISSING_C1_NORM_EQUIVALENCE"),
        ("C_comm", "commutator/connection correction", "Dq[nabla Hperp] vs nabla Dq[Hperp]", "MISSING_DQ_NABLA_COMMUTATOR_BOUND"),
        ("epsilon_i", "componentwise Dq values", "epsilon_i >= ||Dq_i[Hperp]||", "MISSING_NUMERIC_OR_THEOREM_ZERO_COMPONENTS"),
        ("epsilon_i_C1", "componentwise differentiated Dq values", "epsilon_i_C1 >= ||nabla Dq_i[Hperp]||", "MISSING_NUMERIC_OR_THEOREM_ZERO_C1_COMPONENTS"),
    ]
    return [
        {
            **common(),
            "symbol": symbol,
            "role": role,
            "formula": formula,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for symbol, role, formula, status in raw
    ]


def parent_pi4_source_rows() -> List[Dict[str, str]]:
    raw = [
        ("Pi4_parent_rule", "parent/symmetry-fixed map Pi4:X_Q->Y_Q", "MISSING_PARENT_PI4_RULE"),
        ("X_m_components", "memory direction X_m in Q-shear/eigenframe coordinates", "MISSING_X_M_COMPONENTS"),
        ("X_a_components", "Q/shear directions X_a in the same coordinates", "MISSING_X_A_COMPONENTS"),
        ("DPi4_X", "Jacobian of parent selector on U_good", "MISSING_DPI4_JACOBIAN"),
        ("chart_degeneracy_guard", "eigenframe chart/degen support certificate", "MISSING_CHART_DEGEN_CERTIFICATE"),
        ("no_EM_readout_guard", "proof Pi4 chosen before EM/local-GR readout", "MISSING_NO_POSTHOC_READOUT_CERTIFICATE"),
    ]
    return [
        {
            **common(),
            "row_id": row_id,
            "required_object": required_object,
            "status": status,
            "feeds": "P8_Y5_R2FR_4252_JACOBIAN_COMPONENTS_CANDIDATE.csv",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, required_object, status in raw
    ]


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4255_0_matrix_socket",
            "The first Dq probe matrix socket is filled by an identity matrix in Dq-coordinate seminorm only.",
            "This tests and narrows the rank route without pretending to bound physical Hperp.",
            "Keep valid_for_claim=false.",
        ),
        (
            "DEC4255_1_real_missing_piece",
            "The real missing piece is not matrix rank now; it is physical norm-equivalence and component values.",
            "Need C_HDq, eta_Dq_kernel, epsilon_i, and C1 counterparts.",
            NEXT_TARGET,
        ),
        (
            "DEC4255_2_parallel_Pi4",
            "The parent Pi4/Jacobian route remains cleaner if those source rows can be found first.",
            "It bypasses the Dq physical norm-equivalence problem by computing C_mZ/C_ZZ directly.",
            "Do not hand-pick Pi4.",
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
        ("FW4255_0_identity", "treating Dq-coordinate identity matrix as physical Hperp rank", "FORBIDDEN_WITHOUT_C_HDq", "False"),
        ("FW4255_1_kernel", "ignoring a nonzero Dq-kernel Hperp mode", "DQ_KERNEL_ZERO_REQUIRED", "False"),
        ("FW4255_2_components", "using missing Dq epsilon_i component rows", "COMPONENT_VALUES_REQUIRED", "False"),
        ("FW4255_3_C1", "using amplitude norm bridge as derivative norm bridge", "C1_BRIDGE_SEPARATE", "False"),
        ("FW4255_4_Pi4", "hand-picked Pi4 selector", "POSTHOC_SELECTOR_FORBIDDEN", "False"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "blocked_shortcut": shortcut,
            "reason": reason,
            "claim_allowed": claim_allowed,
            "valid_for_claim": "False",
        }
        for firewall_id, shortcut, reason, claim_allowed in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": DECISION,
            "summary": "4255 fills the first Dq-coordinate source-probe matrix as a nonclaim seminorm smoke pack, while adding the physical norm-equivalence and Dq-kernel guard needed before it can bound Hperp.",
            "scoreable_now": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "objective": "Fill physical Hperp-from-Dq norm-equivalence constants and Dq component values, or source parent Pi4/X_m/X_a Jacobian rows.",
            "avoid": "Do not treat the Dq-coordinate identity matrix as physical Hperp injectivity.",
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
        "4255 fills the first Dq-coordinate source-probe matrix as a nonclaim seminorm smoke pack: S_Dq=I and sigma_Dq=1 only in Dq coordinates. It adds the required physical norm-equivalence guard C_HDq and Dq-kernel residue before this can bound Hperp.",
        "4255 source register, Dq-coordinate matrix candidate copied to 4254 input path, rank smoke result, norm-equivalence guard theorem, parent Pi4 source row ledger, decision and firewall.",
        "private_Dq_coordinate_probe_matrix_filled_physical_norm_bridge_missing_nonclaim",
        "Fill C_HDq/eta_Dq_kernel and Dq component values, or source parent Pi4/X_m/X_a Jacobian rows.",
        "Treating the Dq-coordinate identity matrix as physical Hperp injectivity would smuggle local-GR safety.",
    ]
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow(row)


def write_formal_doc() -> None:
    text = f"""
# 271 - PPC4161 fill first Dq probe matrix row or parent Pi4 source row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4255 does not prove `Hperp` is small and does not prove local GR, PPN, R10, clock, or orbital safety.

## What Was Filled

4255 fills the first source-probe matrix socket for 4254 with a Dq-coordinate identity matrix:

```text
Hbasis_i := Dq_i[Hperp] coordinate,
S_Dq = I,
sigma_Dq = 1.
```

This is only a Dq-seminorm smoke pack. It proves the runner wiring and rank convention, not physical Hperp suppression.

## Physical Guard

To convert this into a physical `A_H` bound, the theory still needs:

```text
||Hperp||_F/F_ref <= C_HDq ||Dq[Hperp]||_W + eta_Dq_kernel.
```

If `ker(Dq_*)` contains a nonzero `Hperp` mode, then the Dq-coordinate identity matrix does not bound physical `Hperp`.

For the C1 route:

```text
||nabla Hperp||/(F_ref/L_U)
  <= C_HDq1 ||nabla Dq[Hperp]||_W
     + C_comm ||Dq[Hperp]||_W
     + eta_Dq_C1_kernel.
```

## Parallel Route

The parent `Pi4/X_m/X_a` route remains open. If those source rows arrive first, 4252 computes `C_mZ` and `C_ZZ` directly.

## Next Target

`{NEXT_TARGET}` should fill `C_HDq`, `eta_Dq_kernel`, component values `epsilon_i`, or the parent `Pi4/X_m/X_a` Jacobian pack.
"""
    write_text(FORMAL_PATH, text)


def write_checkpoint_doc() -> None:
    text = f"""
# 4255 - Fill first Dq probe matrix row or parent Pi4 source row

**Status:** `{DECISION}`.

## Result

The first 4254 source-probe matrix socket is filled by a Dq-coordinate identity matrix:

```text
S_Dq = I, sigma_Dq = 1.
```

This is deliberately nonclaim. Physical `Hperp` still needs:

```text
||Hperp||_F/F_ref <= C_HDq ||Dq[Hperp]||_W + eta_Dq_kernel.
```

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, text)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 Dq probe matrix or parent Pi4 source

Marker: `{MARKER}`

4255 fills the first source-probe matrix socket with a Dq-coordinate identity matrix:

```text
S_Dq = I, sigma_Dq = 1
```

but only as a Dq-seminorm smoke pack. A physical `Hperp` bound still needs:

```text
||Hperp||_F/F_ref <= C_HDq ||Dq[Hperp]||_W + eta_Dq_kernel.
```

So the next live missing object is `C_HDq`/kernel silence plus Dq component values, unless the parent `Pi4/X_m/X_a` route lands first.
"""
    packet_block = f"""
## Packet Update - Dq probe matrix or parent Pi4 source

Marker: `{PACKET_MARKER}`

The packet now has a nonclaim Dq-coordinate source-probe matrix feeding the 4254 runner. This does not close local-GR; it exposes the exact remaining bridge: physical Hperp-from-Dq norm equivalence or parent Pi4/X_m/X_a Jacobian ownership.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validation_rows(outputs: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = source_rows()
    matrix = dq_coordinate_matrix_rows()
    validations: List[Tuple[str, bool, str]] = [
        ("VAL4255_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4255_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        ("VAL4255_2_matrix_size", len(matrix) == 2 * len(PROBES) * len(PROBES), "Dq identity matrix has amplitude and C1 blocks"),
        ("VAL4255_3_matrix_nonclaim", all(row["valid_for_claim"] == "False" for row in matrix), "all matrix rows nonclaim"),
        ("VAL4255_4_4254_candidate_written", MATRIX_CANDIDATE_4254_PATH.exists(), "4254 matrix candidate path exists"),
        ("VAL4255_5_norm_guard", any(row["theorem_id"] == "DQM4255_1_physical_norm_guard" for row in theorem_rows()), "physical norm guard emitted"),
        ("VAL4255_6_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4255_7_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4255_8_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4255_9_spine_marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine marker present"),
        ("VAL4255_10_packet_marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet marker present"),
    ]
    for name, path in outputs.items():
        validations.append((f"VAL4255_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
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
        "source_register": SOURCE_DIR / "P8_Y5_R2FR_4255_SOURCE_REGISTER.csv",
        "dq_coordinate_matrix": LOCAL_MATRIX_PATH,
        "rank_smoke": SOURCE_DIR / "P8_Y5_R2FR_4255_RANK_SMOKE_RESULT.csv",
        "theorems": SOURCE_DIR / "P8_Y5_R2FR_4255_DQ_NORM_GUARD_THEOREMS.csv",
        "missing_bridge": SOURCE_DIR / "P8_Y5_R2FR_4255_MISSING_PHYSICAL_BRIDGE_LEDGER.csv",
        "parent_pi4": SOURCE_DIR / "P8_Y5_R2FR_4255_PARENT_PI4_SOURCE_ROW_LEDGER.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4255_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4255_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4255_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4255_NEXT_TARGET.csv",
    }

    write_formal_doc()
    write_checkpoint_doc()
    append_claim_row()
    update_spine_and_packet()

    matrix_rows = dq_coordinate_matrix_rows()
    write_csv(outputs["source_register"], source_rows())
    write_csv(outputs["dq_coordinate_matrix"], matrix_rows)
    write_csv(MATRIX_CANDIDATE_4254_PATH, matrix_rows)
    write_csv(outputs["rank_smoke"], rank_smoke_rows())
    write_csv(outputs["theorems"], theorem_rows())
    write_csv(outputs["missing_bridge"], missing_bridge_rows())
    write_csv(outputs["parent_pi4"], parent_pi4_source_rows())
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

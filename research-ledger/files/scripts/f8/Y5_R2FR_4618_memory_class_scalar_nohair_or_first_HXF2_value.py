from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4618"
CLAIM_ID = "L-460"
BRANCH_ID = "MTS_R2FR_Y5_MEMORY_CLASS_SCALAR_HXF2_4618"
MARKER = "PPC4161_MEMORY_CLASS_SCALAR_NOHAIR_OR_FIRST_HXF2_VALUE_4618"
PACKET_MARKER = "PPC4161_PACKET_MEMORY_CLASS_SCALAR_HXF2_4618"
DECISION = "CMEMORY_F2_ZERO_REDUCED_TO_QGAUGE_CONSTANT_OR_POSITIVE_NOHAIR_OR_NO_TARGET_NONCLAIM_FIRST_VALUE_ROW_READY"
NEXT_TARGET = "4619-Y5-R2FR-F2-memory-coefficient-owner-or-Zmem-M2mem-source-row.md"

DOC_PATH = POST / "4618-Y5-R2FR-memory-class-scalar-nohair-or-first-HXF2-value.md"
FORMAL_PATH = FORMAL / "634-PPC4161-memory-class-scalar-nohair-or-first-HXF2-value.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4618_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4618_MEMORY_CLASS_SCALAR_NOHAIR_THEOREM.csv"
NO_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4618_MEMORY_F2_NO_TARGET_GATE_ROWS.csv"
VALUE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4618_CMEMORY_F2_VALUE_ROW_NONCLAIM.csv"
HXF2_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4618_HXF2_UPDATE_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4618_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4618_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4618_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4618_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4618_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4618_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4618_VALIDATION.csv"

CSV_4617_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4617_NEXT_TARGET.csv"
CSV_4617_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4617_PARENT_SCALAR_FUNCTIONAL_THEOREM.csv"
CSV_4617_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4617_HXF2_COMPONENT_VECTOR_NONCLAIM.csv"
CSV_1092_NOHAIR = SOURCE_DIR / "P8_Y5_R10_1092_SCALAR_NOHAIR_ROUTE_AUDIT.csv"
CSV_1092_GENERATORS = SOURCE_DIR / "P8_Y5_R10_1092_SURVIVING_GENERATOR_LEDGER.csv"
CSV_1093_THEOREM = SOURCE_DIR / "P8_Y5_R10_1093_CONDITIONAL_NOHAIR_THEOREM.csv"
CSV_1042_IDENTITY = SOURCE_DIR / "P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv"
CSV_4506_OPERATOR = SOURCE_DIR / "P8_Y5_R2FR_4506_MEMORY_OPERATOR_SIGNATURE.csv"
CSV_4506_EXTREMUM = SOURCE_DIR / "P8_Y5_R2FR_4506_MEMORY_EXTREMUM_TEST.csv"
CSV_4506_BODY = SOURCE_DIR / "P8_Y5_R2FR_4506_BODY_CHARGE_INPUT_ROW.csv"
CSV_4506_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4506_PARENT_SIGNATURE_AUDIT.csv"
CSV_980_COUNTER = SOURCE_DIR / "P8_Y5_R10_980_COUNTEREXAMPLE_LEDGER.csv"
CSV_4616_PROOF = SOURCE_DIR / "P8_Y5_R2FR_4616_VISIBLE_IMAGE_PROOF_ATTEMPT.csv"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines)


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return number
    return 0


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    suffix = "\n" if text.endswith("\n") or not text else "\n\n"
    write_text(path, text + suffix + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not path.exists() or not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--porcelain"], text=True, capture_output=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4618_00_4617_next", CSV_4617_NEXT, "4618-Y5-R2FR-memory-class-scalar-nohair-or-first-HXF2-value.md", "4617 selected memory/class scalar."),
        ("SRC4618_01_4617_theorem", CSV_4617_THEOREM, "PSF4617_4_finite_vector_fallback", "4617 staged H_XF2 vector fallback."),
        ("SRC4618_02_4617_vector", CSV_4617_VECTOR, "HXF24617_3_memory", "4617 memory component row."),
        ("SRC4618_03_1092_nohair", CSV_1092_NOHAIR, "SNH1092_4_verdict", "1092 scalar no-hair audit."),
        ("SRC4618_04_1092_generators", CSV_1092_GENERATORS, "GEN1092_3_memory_scalar", "1092 memory scalar obstruction."),
        ("SRC4618_05_1093_theorem", CSV_1093_THEOREM, "THM1093_2_zero_result", "1093 conditional no-hair theorem."),
        ("SRC4618_06_1042_identity", CSV_1042_IDENTITY, "NH1042_2_positive_zero_theorem", "1042 positive X no-hair identity."),
        ("SRC4618_07_4506_operator", CSV_4506_OPERATOR, "MOP4506_2_nohair_guard", "4506 memory operator signature."),
        ("SRC4618_08_4506_extremum", CSV_4506_EXTREMUM, "MEXT4506_1_branch_extremum", "4506 memory extremum test."),
        ("SRC4618_09_4506_body", CSV_4506_BODY, "BCIN4506_0_memory_density", "4506 memory body-charge input row."),
        ("SRC4618_10_4506_audit", CSV_4506_AUDIT, "PA4506_0_Bmem", "4506 parent signature audit."),
        ("SRC4618_11_980_memory", CSV_980_COUNTER, "CEX980_4_memory_class_scalar", "980 memory/class scalar counterexample."),
        ("SRC4618_12_4616_countermodel", CSV_4616_PROOF, "VIP4616_2_scalar_functional_countermodel", "4616 F2 scalar countermodel."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": needle in text,
            "line": line_of(path, needle),
            "role": role,
            "valid_for_claim": False,
            "timestamp_utc": now,
        })
    return rows


def theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MCS4618_0_qgauge_constant_zero",
            "claim_piece": "memory/class scalar q-gauge constant route",
            "formal_statement": "If m_mem is q-basic or constant on the connected transitive hidden fibre, then D_v m_mem=0 for v in ker(Dq).",
            "derivation": "This imports the 4617 invariant-triviality fork into the specific memory/class scalar generator: m_mem cannot vary along hidden directions if it is q-owned, gauge, or fixed branch data.",
            "zero_effect": "C_memory_F2=0 for any coefficient lambda_F2(m_mem) that is otherwise a fixed visible target.",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "source_refs": "PSF4617_0_transitive_fibre_triviality;GEN1092_3_memory_scalar",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MCS4618_1_positive_nohair_zero",
            "claim_piece": "memory/class scalar positive no-hair",
            "formal_statement": "For delta_m on a local exterior A, if L_mem delta_m=(-nabla_i Z_mem nabla^i+M2_mem)delta_m=rho_mem is self-adjoint positive, rho_mem=0, boundary flux/charge=0, and zero modes are removed, then delta_m=0 or fixed reference on A.",
            "derivation": "Multiply by delta_m and integrate: int_A(Z_mem|grad delta_m|^2+M2_mem delta_m^2)=int_A delta_m rho_mem+Phi_boundary. With positive left side and zero right side, the profile vanishes.",
            "zero_effect": "D_v m_mem=0 locally and the memory/class scalar cannot feed a local F2 drift.",
            "current_status": "Z_MEM_M2_MEM_SOURCE_BOUNDARY_INPUTS_UNSIGNED",
            "source_refs": "THM1093_2_zero_result;NH1042_2_positive_zero_theorem;MOP4506_2_nohair_guard",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MCS4618_2_no_target_zero",
            "claim_piece": "no F2 target for memory scalar",
            "formal_statement": "Even if m_mem survives, C_memory_F2=0 if Hom_parent(m_mem,Coeff(F_Q^2)) is absent and Coeff(F_Q^2) is exhausted by the parent Maxwell norm/fixed constants.",
            "derivation": "The memory scalar can only alter alpha/Maxwell stress by entering the EM kinetic coefficient. If the 4616 visible-image/no-target theorem is signed for memory arguments, the coefficient derivative is ill-typed.",
            "zero_effect": "lambda_F2 cannot depend on m_mem, so partial_m lambda_F2=0 and C_memory_F2=0.",
            "current_status": "NO_TARGET_NOT_PARENT_SIGNED",
            "source_refs": "VIP4616_0_exact_image_zero_theorem;VIP4616_2_scalar_functional_countermodel",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MCS4618_3_extremum_double_zero_route",
            "claim_piece": "memory coefficient extremum route",
            "formal_statement": "If lambda_F2(m)=lambda_0+1/2 lambda_2(delta_m)^2+... at the parent-selected branch and delta_m satisfies the no-hair zero branch, then C_memory_F2 is at least quadratic and locally zero on the exact branch.",
            "derivation": "4506 already sharpens B_mem=0 to F0_prime=0 or projection-removal. Applied to the F2 coefficient, the same extremum removes the linear memory-F2 coupling.",
            "zero_effect": "First-order hidden-Hom drift from memory vanishes; finite branch is quadratic/profile bounded.",
            "current_status": "BRANCH_EXTREMUM_NOT_PARENT_SIGNED",
            "source_refs": "MEXT4506_1_branch_extremum;MEXT4506_3_finite_residual",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MCS4618_4_countermodel_and_value_need",
            "claim_piece": "memory scalar F2 countermodel",
            "formal_statement": "If a memory/class scalar survives and Coeff(F_Q^2) is a legal target, lambda_F2=lambda_0+epsilon m_mem is a legal finite branch.",
            "derivation": "The 980 memory/class scalar counterexample and 4616 scalar-functional countermodel combine directly: a surviving scalar can feed a continuous EM coefficient unless no-target/no-hair/q-gauge constancy is proved.",
            "zero_effect": "No zero claim; fill C_memory_F2 with units, parent variation basis, coefficient owner, source profile and arena projections.",
            "current_status": "FINITE_VALUE_ROW_REQUIRED_IF_PROOF_FAILS",
            "source_refs": "CEX980_4_memory_class_scalar;VIP4616_2_scalar_functional_countermodel;BCIN4506_0_memory_density",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def no_target_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "NT4618_0_visible_F2_target_absent",
            "required_signature": "Coeff(F_Q^2) is not an independent target object outside Gen_EM=C_P N_Q <F_Q,F_Q>",
            "if_signed": "memory scalar has no F2 coefficient target",
            "if_unsigned": "lambda_F2(m_mem) remains legal",
            "current_status": "UNSIGNED_PARENT_IMAGE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "NT4618_1_memory_argument_absent",
            "required_signature": "m_mem is not an allowed argument of any visible EM coefficient functional",
            "if_signed": "partial_m lambda_F2=0",
            "if_unsigned": "C_memory_F2 row remains live",
            "current_status": "UNSIGNED_NO_HOM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "NT4618_2_readout_EFT_no_reentry",
            "required_signature": "readout/EFT/radiative projection cannot reintroduce m_mem into F2 after variation",
            "if_signed": "tree-level no-target is stable",
            "if_unsigned": "C_readout_F2 and C_rad_F2 remain in H_XF2",
            "current_status": "UNSIGNED_RADIOUT_CLOSURE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def value_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CMF4618_0_first_value_contract",
            "symbol": "C_memory_F2",
            "definition": "memory/class contribution to H_XF2 from a nonconstant memory scalar feeding the Maxwell kinetic coefficient",
            "normal_form": "C_memory_F2 := |partial_m ln(lambda_F2)| Delta_v m_mem",
            "field_equation": "(-Z_mem nabla^2 + M2_mem) delta_m = rho_mem",
            "source_density": "rho_mem = B_mem R_obs + C_mem T + J_mem",
            "amplitude_law": "Delta_v m_mem <= [exp(R_body/lambda_mem) int_body |rho_mem| dV + |Q_boundary_mem|]/(4*pi |Z_mem|)",
            "required_inputs": "partial_m lambda_F2;Z_mem;M2_mem;B_mem;C_mem;J_mem;Q_boundary_mem;body profile;vertical normalization;arena K/tau projections;source paths",
            "value": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "units": "dimensionless derivative contribution",
            "source_path": str(VALUE_CSV),
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CMF4618_1_zero_switch",
            "symbol": "C_memory_F2_zero",
            "definition": "exact zero switch for memory-F2 Hom row",
            "normal_form": "C_memory_F2=0 if D_v m_mem=0 or partial_m lambda_F2=0",
            "field_equation": "q-gauge constant OR positive no-hair OR no-target theorem",
            "source_density": "rho_mem=0 and Q_boundary_mem=0 on no-hair branch",
            "amplitude_law": "Delta_v m_mem=0",
            "required_inputs": "same-branch parent signatures, not separate closures",
            "value": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "units": "dimensionless",
            "source_path": str(VALUE_CSV),
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def hxf2_update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": "HUP4618_0_vector_update",
            "old_component": "HXF24617_3_memory",
            "new_component": "CMF4618_0_first_value_contract",
            "formula": "H_XF2 <= H_XF2_without_memory + |C_memory_F2|",
            "status": "MEMORY_COMPONENT_SHARPENED_NOT_VALUED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "update_id": "HUP4618_1_arena_projection",
            "old_component": "R10/PPN/clock/cosmology projections",
            "new_component": "K_A C_memory_F2 tau_A",
            "formula": "|residual_A^memF2| <= |K_A^memF2| |C_memory_F2| tau_A",
            "status": "PROJECTION_SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4618_0_no_wrong_variable_nohair",
            "rule": "Do not use a no-hair theorem for a generic X unless X is the same parent variable that feeds lambda_F2.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4618_1_no_source_free_assertion",
            "rule": "rho_mem=0 and Q_boundary_mem=0 must be parent-signed or source-backed; compact support prose is not enough.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4618_2_no_fit_inversion",
            "rule": "Do not infer partial_m lambda_F2 or C_memory_F2 from observational bounds; values need parent/source provenance.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4618_0_F2_memory_owner",
            "claim_blocked": "C_memory_F2=0 by no-target",
            "missing_signature": "parent says memory/class scalar is not an argument of Coeff(F_Q^2)",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4618_1_positive_operator_inputs",
            "claim_blocked": "C_memory_F2=0 by no-hair",
            "missing_signature": "Z_mem, M2_mem, self-adjoint domain, zero modes, rho_mem=0 and Q_boundary_mem=0",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4618_2_first_value_inputs",
            "claim_blocked": "finite H_XF2 scoring",
            "missing_signature": "partial_m lambda_F2, Delta_v m_mem, body profile, source paths and arena K/tau projections",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4618_0_zero_branch",
            "requirement": "q/gauge constant memory OR positive no-hair inputs OR no F2 target, plus readout/radiative no-reentry",
            "current_status": "BLOCKED_PARENT_SIGNATURE_UNSIGNED",
            "sources_valid": sources_ok,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4618_1_value_branch",
            "requirement": "source-backed C_memory_F2 value with units, parent variation basis, no-cancellation envelope and arena projections",
            "current_status": "BLOCKED_VALUE_MISSING",
            "sources_valid": sources_ok,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4618_0",
            "decision": DECISION,
            "what_changed": "The memory/class scalar is no longer a generic obstruction: C_memory_F2 has three exact zero routes and one explicit first-value contract.",
            "claim_status": "NONCLAIM_PRIVATE_DERIVATION_STAGE",
            "exact_paths": "q/gauge constant; positive no-hair; no F2 target; branch extremum/double-zero",
            "fallback_path": "fill C_memory_F2 := |partial_m ln(lambda_F2)| Delta_v m_mem with Z_mem/M2_mem/source/boundary inputs",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "PRIVATE_NONCLAIM_DERIVATION_ADVANCE",
            "summary": "C_memory_F2 zero routes and first finite value contract are written; next is coefficient owner or Z_mem/M2_mem source row.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "timestamp_utc": now,
            "next_target": NEXT_TARGET,
            "why": "4618 makes C_memory_F2 exact enough that the next proof must target the F2 coefficient owner or the first no-hair operator inputs.",
            "derive_path": "prove memory/class scalar has no parent Hom into Coeff(F_Q^2), or prove partial_m lambda_F2=0 at the selected branch",
            "fallback_path": "source Z_mem, M2_mem, rho_mem and Q_boundary_mem plus partial_m lambda_F2 for a first finite value row",
            "claim_allowed": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4618 - Memory/Class Scalar No-Hair Or First H_XF2 Value

Generated UTC: `{now}`

Marker: `{MARKER}`

## Result

4618 sharpens the first live `H_XF2` component:

```text
C_memory_F2 := |partial_m ln(lambda_F2)| Delta_v m_mem.
```

There are now three exact zero routes:

1. `m_mem` is q-basic/gauge constant, so `D_v m_mem=0`.
2. `m_mem` satisfies a signed positive no-hair identity, so `delta_m=0` or fixed reference locally.
3. `m_mem` has no parent target into `Coeff(F_Q^2)`, so `partial_m lambda_F2=0`.

If none closes, the first finite value row is no longer vague:

```text
(-Z_mem nabla^2 + M2_mem) delta_m = B_mem R_obs + C_mem T + J_mem,
Delta_v m_mem <= [exp(R_body/lambda_mem) int_body |rho_mem| dV + |Q_boundary_mem|]/(4*pi |Z_mem|).
```

No local-GR, Maxwell, clock, R10, PPN or Newton claim fires from this checkpoint.

## Source Register

{markdown_table(tables["sources"])}

## Memory/Class Scalar No-Hair Theorem

{markdown_table(tables["theorem"])}

## Memory F2 No-Target Gate Rows

{markdown_table(tables["no_target"])}

## C_memory_F2 Value Row Nonclaim

{markdown_table(tables["value"])}

## H_XF2 Update Rows

{markdown_table(tables["hxf2_update"])}

## Controls

{markdown_table(tables["controls"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Decision

{markdown_table(tables["decision"])}

## Status

{markdown_table(tables["status"])}

## Next Target

`{NEXT_TARGET}`
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 Formal Addendum 634 - Memory/Class Scalar No-Hair Or First H_XF2 Value

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

## Zero Routes

For the memory/class scalar contribution to the EM kinetic Hom row,

```text
C_memory_F2 := |partial_m ln(lambda_F2)| Delta_v m_mem.
```

The component is zero if any same-branch condition holds:

```text
D_v m_mem = 0,
or partial_m lambda_F2 = 0,
or (-Z_mem nabla^2 + M2_mem)delta_m=0 with positive operator and zero boundary flux.
```

## Finite Branch

If memory is not q/gauge constant, not no-hair, and not barred from `Coeff(F_Q^2)`,

```text
(-Z_mem nabla^2 + M2_mem) delta_m = B_mem R_obs + C_mem T + J_mem,
H_XF2 <= H_XF2_without_memory + |C_memory_F2|.
```

Next target: `{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "sector": "local_gr_empirical_interface",
        "claim": "4618 sharpens the first H_XF2 memory/class scalar component into exact zero routes and an explicit C_memory_F2 first-value contract.",
        "evidence": "Generated memory no-hair theorem rows, no-target gate rows, C_memory_F2 value rows, H_XF2 updates, controls, blockers, promotion gates, decision, status, next target and validation.",
        "status": "CmemoryF2_zero_routes_and_first_value_contract_nonclaim",
        "next_action": NEXT_TARGET,
        "risk": "Using no-hair for the wrong variable, asserting source silence, or inferring C_memory_F2 from observational bounds.",
        "owner": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "No b_alpha, Maxwell, WEP, clock, R10, Newton or local-GR pass until the memory F2 coefficient owner or Z_mem/M2_mem/source/boundary inputs are parent-signed or source-backed.",
    }
    existing = read_text(CLAIMS_PATH)
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not existing.endswith("\n"):
            handle.write("\n")
        writer.writerow(row)


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        })

    missing_sources = [row["source_id"] for row in tables["sources"] if not row["path_exists"] or not row["needle_found"]]
    add("VAL4618_00_sources_exist_and_needles_found", not missing_sources, "missing: " + ",".join(missing_sources) if missing_sources else "all cited paths/needles found")

    csv_paths = [
        SOURCE_REGISTER, THEOREM_CSV, NO_TARGET_CSV, VALUE_CSV, HXF2_UPDATE_CSV,
        CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV,
    ]
    csv_ok = True
    details: list[str] = []
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4618_01_csv_parse", csv_ok, ";".join(details))

    theorem_text = "\n".join(str(row) for row in tables["theorem"])
    no_target_text = "\n".join(str(row) for row in tables["no_target"])
    value_text = "\n".join(str(row) for row in tables["value"])
    update_text = "\n".join(str(row) for row in tables["hxf2_update"])
    add("VAL4618_02_zero_routes", "D_v m_mem=0" in theorem_text and "partial_m lambda_F2=0" in theorem_text and "positive no-hair" in theorem_text, "three zero routes present")
    add("VAL4618_03_countermodel_guard", "lambda_F2=lambda_0+epsilon m_mem" in theorem_text and "FINITE_VALUE_ROW_REQUIRED" in theorem_text, "countermodel retained")
    add("VAL4618_04_no_target_gates", "Coeff(F_Q^2)" in no_target_text and "m_mem" in no_target_text, "no-target gates present")
    add("VAL4618_05_value_contract", "C_memory_F2 := |partial_m ln(lambda_F2)| Delta_v m_mem" in value_text and "Z_mem;M2_mem" in value_text, "value contract present")
    add("VAL4618_06_HXF2_update", "H_XF2_without_memory" in update_text and "K_A C_memory_F2 tau_A" in update_text, "H_XF2 updates present")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "claim_pass", "empirical_pass_claimed", "score_ready"} and value is True:
                    all_false = False
    add("VAL4618_07_no_claim_true", all_false, "no generated row promotes a claim")
    add("VAL4618_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4618_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4618_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4618_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4618_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4618_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4618_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4618_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4618_OVERALL", all(row["status"] == "PASS" for row in rows), "4618 memory-class scalar H_XF2 checkpoint")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "theorem": theorem_rows(now),
        "no_target": no_target_rows(now),
        "value": value_rows(now),
        "hxf2_update": hxf2_update_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(THEOREM_CSV, tables["theorem"])
    write_csv(NO_TARGET_CSV, tables["no_target"])
    write_csv(VALUE_CSV, tables["value"])
    write_csv(HXF2_UPDATE_CSV, tables["hxf2_update"])
    write_csv(CONTROL_CSV, tables["controls"])
    write_csv(BLOCKERS_CSV, tables["blockers"])
    write_csv(PROMOTION_CSV, tables["promotion"])
    write_csv(DECISION_CSV, tables["decision"])
    write_csv(STATUS_CSV, tables["status"])
    write_csv(NEXT_CSV, tables["next"])
    write_text(DOC_PATH, build_doc(now, tables))
    write_text(FORMAL_PATH, build_formal(now))
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 Local Addendum - Memory/Class Scalar No-Hair Or First HXF2 Value

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

4618 sharpens the first finite `H_XF2` component. `C_memory_F2 := |partial_m ln(lambda_F2)| Delta_v m_mem` is zero only if memory is q/gauge constant, satisfies the positive no-hair branch, or has no parent Hom into `Coeff(F_Q^2)`. Otherwise it is the first explicit HXF2 value row requiring `partial_m lambda_F2`, `Z_mem`, `M2_mem`, `B_mem`, `C_mem`, `J_mem`, `Q_boundary_mem`, body profile, vertical normalization and arena projections.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Memory/Class Scalar No-Hair Or First HXF2 Value

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The packet now has the first concrete EM Hom coefficient target: `C_memory_F2`. Next work must either prove memory cannot own an F2 coefficient or source the operator/coefficient inputs for the first finite row.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4618 validation failed: {failed}")
    print(f"4618 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()

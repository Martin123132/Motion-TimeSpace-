from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4142-Y5-R2FR-scalar-hair-U2-orthogonality-or-beta-overlap-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_SCALAR_HAIR_U2_ORTHOGONALITY_OR_BOUND_4142"
CHECKPOINT_ID = "4142"
DECISION = "SCALAR_HAIR_U2_OVERLAP_REDUCED_TO_PHI_SOURCE_ORTHOGONALITY_NO_GENERIC_ZERO"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4142_00_4141_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4141_NEXT_TARGET.csv",
        "4142-Y5-R2FR-scalar-hair-U2-orthogonality-or-beta-overlap-bound.md",
        "4141 selected scalar-hair U2 orthogonality or beta-overlap bound.",
    ),
    "SRC4142_01_4141_overlap": (
        SOURCE_DIR / "P8_Y5_R2FR_4141_ADJOINT_OVERLAP_REDUCTION.csv",
        "int_Omega phi U^2",
        "4141 adjoint reduction exposing the scalar-hair overlap.",
    ),
    "SRC4142_02_4141_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4141_BETA_DENSITY_BOUND_ROWS.csv",
        "H_phiU2",
        "4141 nonclaim scalar-hair beta bound row.",
    ),
    "SRC4142_03_1527_aux": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1527_LOCAL_AUXILIARY_ACTION_CONTRACT.csv",
        "Box phi=S_Gamma",
        "1527 local auxiliary phi owner contract.",
    ),
    "SRC4142_04_1527_nonlocal": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1527_NONLOCALITY_GUARD.csv",
        "REJECT_FOR_LOCAL_FIELD_THEORY_CLAIM",
        "1527 guard rejecting inverse-Box shortcut for local field-theory claims.",
    ),
    "SRC4142_05_1527_hunt": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1527_PHI_OWNER_SOURCE_HUNT.csv",
        "Box phi=(2/3)",
        "1527 phi owner source hunt.",
    ),
    "SRC4142_06_2220_birth": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_2220_TRACEFREE_IMPROVEMENT_BIRTH_CERTIFICATE.csv",
        "AUXILIARY_CONTRACT_STAGED_NONCLAIM",
        "2220 trace-free birth certificate: phi owner staged, not adopted.",
    ),
    "SRC4142_07_4138_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT.csv",
        "local phi owner",
        "4138 local phi owner blocker.",
    ),
    "SRC4142_08_4138_zero": (
        SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_ZERO_THEOREM_OR_BOUND.csv",
        "D_TF=0",
        "4138 trace-free zero theorem remains conditional.",
    ),
    "SRC4142_09_1287_component": (
        SOURCE_DIR / "P8_Y5_R10_1287_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv",
        "Box phi=(2/3)",
        "1287 K_L component row with phi source relation.",
    ),
    "SRC4142_10_4139_acquisition": (
        SOURCE_DIR / "P8_Y5_R2FR_4139_SOURCE_ACQUISITION_PACK.csv",
        "U(x)",
        "4139 source-normalized U profile requirement.",
    ),
    "SRC4142_11_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4142_scalar_hair_U2_orthogonality_or_beta_overlap_bound.py",
        "Reproducible generator for this 4142 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def scalar_overlap_derivation_rows() -> List[dict]:
    data = [
        (
            "SO4142_0_overlap_definition",
            "scalar-hair overlap",
            "H_phiU2:=int_Omega phi U^2 d^3x",
            "This is the scalar term exposed by 4141 after adjoint integration by parts.",
            "OVERLAP_TARGET_DEFINED",
            "phi and U are not source-backed profiles",
        ),
        (
            "SO4142_1_adjoint_phi_identity",
            "phi equation adjoint identity",
            "If Delta phi=S_phi and Delta chi_U=U^2, then H_phiU2=int_Omega chi_U S_phi d^3x + int_partialOmega(phi partial_n chi_U-chi_U partial_n phi)dS",
            "The overlap is controlled by the phi source weighted by chi_U plus a boundary bilinear.",
            "ADJOINT_IDENTITY_DERIVED",
            "requires boundary convention and source-normalized chi_U",
        ),
        (
            "SO4142_2_phi_source",
            "MTS phi source",
            "S_phi=(2/3)(Gamma_eff+C)+R_phi_owner+R_lambda+R_boundary",
            "The local auxiliary route turns the overlap into weighted Gamma/source plus owner/boundary remnants.",
            "SOURCE_DECOMPOSITION_FILLED",
            "S_phi is staged nonclaim, not a live parent equation",
        ),
        (
            "SO4142_3_calibration_constant",
            "constant C route",
            "H_phiU2=0 would require int chi_U (Gamma_eff+C)d^3x plus boundary/remnants =0",
            "A constant can only be used if parent-owned and universal, not fitted per source/domain.",
            "CALIBRATION_GUARD_ADDED",
            "no parent-owned C selection theorem exists",
        ),
        (
            "SO4142_4_generic_nonzero_guard",
            "generic nonzero guard",
            "For sign-definite chi_U and sign-definite nonzero S_phi with silent boundary, H_phiU2 is generically nonzero.",
            "This rejects the shortcut that scalar hair is automatically U^2-orthogonal.",
            "NO_GENERIC_ZERO",
            "requires no-hair, coefficient zero, or real orthogonality theorem",
        ),
        (
            "SO4142_5_nohair_zero",
            "no-hair zero route",
            "H_phiU2=0 if phi=0 in Omega or S_phi=0 with homogeneous boundary data.",
            "This is clean but strong: it is a local scalar no-hair theorem, not an algebraic identity.",
            "ZERO_ROUTE_CONDITIONAL",
            "not signed by current phi owner rows",
        ),
        (
            "SO4142_6_bound_law",
            "overlap bound",
            "|H_phiU2| <= ||chi_U||_2 ||S_phi||_2 + |B_phi_chi|",
            "If no-hair/orthogonality fails, the bound needs source-backed chi_U, S_phi and boundary bilinear.",
            "BOUND_LAW_DERIVED",
            "all norms are symbolic only",
        ),
        (
            "SO4142_7_beta_insertion",
            "trace-free beta insertion",
            "|I_TF| <= |lambda_00^TF epsilon_TF|/2 * (|B_phi_gradchi|+|H_phiU2|)",
            "The scalar overlap feeds the trace-free beta residual only through the coefficient mismatch and projection coefficient.",
            "BETA_INSERTION_DERIVED",
            "lambda_00^TF, epsilon_TF, boundary and H_phiU2 are not numeric/source-backed",
        ),
    ]
    rows: List[dict] = []
    for derivation_id, step, formula, meaning, status, blocker in data:
        row = row_base()
        row.update(
            {
                "derivation_id": derivation_id,
                "step": step,
                "formula": formula,
                "meaning": meaning,
                "status": status,
                "blocker": blocker,
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def zero_route_audit_rows() -> List[dict]:
    data = [
        (
            "ZA4142_0_coefficient",
            "coefficient route",
            "epsilon_TF=0 makes the trace-free current/overlap irrelevant",
            "UNSIGNED_BUT_CLEAN",
            "sigma_resp*c_I=1 still not source-fixed",
        ),
        (
            "ZA4142_1_phi_nohair",
            "phi no-hair route",
            "phi=0 or S_phi=0 with homogeneous boundary data in the PPN collar",
            "UNSIGNED_STRONG_THEOREM",
            "current phi owner is staged nonclaim",
        ),
        (
            "ZA4142_2_weighted_source_orthogonality",
            "weighted source orthogonality",
            "int chi_U S_phi d^3x=0",
            "UNSIGNED_OR_FINE_TUNED",
            "no symmetry/parent theorem enforces this currently",
        ),
        (
            "ZA4142_3_boundary_compensation",
            "boundary compensation",
            "B_phi_chi=int_partialOmega(phi partial_n chi_U-chi_U partial_n phi)dS cancels bulk overlap",
            "UNSIGNED_BOUNDARY",
            "would be dangerous if tuned by boundary condition rather than parent-owned",
        ),
        (
            "ZA4142_4_constant_C",
            "constant C calibration",
            "C selected so int chi_U(Gamma_eff+C)=0",
            "NOT_ALLOWED_UNLESS_PARENT_UNIVERSAL",
            "per-body/per-domain choice would be post-hoc calibration",
        ),
        (
            "ZA4142_5_numeric_bound",
            "numeric overlap bound",
            "source-backed ||chi_U||, ||S_phi||, B_phi_chi and N_U2",
            "NOT_SCORE_READY",
            "profiles/kernels/boundary rows missing",
        ),
    ]
    rows: List[dict] = []
    for audit_id, route, pass_condition, status, blocker in data:
        row = row_base()
        row.update(
            {
                "audit_id": audit_id,
                "route": route,
                "pass_condition": pass_condition,
                "status": status,
                "blocker": blocker,
                "route_passed": "False",
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def overlap_bound_rows() -> List[dict]:
    data = [
        (
            "OB4142_0_phi_source",
            "S_phi",
            "(2/3)(Gamma_eff+C)+R_phi_owner+R_lambda+R_boundary",
            "L^-2 or declared source-normalized phi equation units",
            "live phi equation or nonclaim source profile",
            "MISSING_SOURCE_BACKED_PROFILE",
        ),
        (
            "OB4142_1_adjoint_potential",
            "chi_U",
            "Delta chi_U=U^2 with same PPN boundary/window",
            "U^2 times length^2 in Poisson units",
            "source-normalized U and domain/boundary convention",
            "MISSING_ADJOINT_PROFILE",
        ),
        (
            "OB4142_2_boundary_bilinear",
            "B_phi_chi",
            "int_partialOmega(phi partial_n chi_U-chi_U partial_n phi)dS",
            "scalar overlap units",
            "phi, chi_U and normal derivatives on collar",
            "MISSING_BOUNDARY_BILINEAR",
        ),
        (
            "OB4142_3_scalar_overlap",
            "H_phiU2",
            "int_Omega phi U^2 d^3x = int chi_U S_phi d^3x + B_phi_chi",
            "scalar overlap units",
            "S_phi, chi_U, boundary bilinear",
            "NONCLAIM_BOUND_ROW",
        ),
        (
            "OB4142_4_overlap_bound",
            "H_bound",
            "|H_phiU2| <= ||chi_U||_2 ||S_phi||_2 + |B_phi_chi|",
            "scalar overlap units",
            "norms and boundary value",
            "BOUND_FORM_ONLY",
        ),
        (
            "OB4142_5_beta_overlap",
            "I_TF",
            "|I_TF| <= |lambda_00^TF epsilon_TF|/2*(|B_phi_gradchi|+|H_phiU2|)",
            "projected beta numerator units",
            "lambda_00^TF, epsilon_TF, H_phiU2 and boundary term",
            "BOUND_FORM_ONLY",
        ),
        (
            "OB4142_6_beta_residual",
            "delta_beta_TF",
            "|delta_beta_TF| <= (|B_TF|+|I_TF|+|I_rem_TF|)/(2N_U2)",
            "dimensionless beta",
            "N_U2 and all numerator terms source-backed",
            "NOT_SCORE_READY",
        ),
    ]
    rows: List[dict] = []
    for bound_id, symbol, formula, units, required_inputs, status in data:
        row = row_base()
        row.update(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "formula": formula,
                "units": units,
                "required_inputs": required_inputs,
                "status": status,
                "numeric_value_present": "False",
                "source_backed": "False",
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_gate_rows() -> List[dict]:
    data = [
        (
            "DG4142_0_overlap_reduced",
            "H_PHI_U2_REDUCED_TO_SOURCE_AND_BOUNDARY",
            "The scalar-hair overlap is now expressed as a weighted phi-source integral plus boundary bilinear.",
            "use the phi equation rather than treating phi overlap as a black box",
        ),
        (
            "DG4142_1_no_generic_zero",
            "NO_GENERIC_SCALAR_ORTHOGONALITY",
            "Sign-definite nonzero scalar source generally gives nonzero H_phiU2; scalar hair is not automatically beta-safe.",
            "do not claim U2 orthogonality without a theorem",
        ),
        (
            "DG4142_2_clean_zero_routes",
            "ZERO_REQUIRES_COEFFICIENT_NOHAIR_OR_PARENT_ORTHOGONALITY",
            "The clean routes are epsilon_TF=0, phi no-hair/homogeneous boundary, or a parent-owned weighted-source orthogonality theorem.",
            "route selector needed",
        ),
        (
            "DG4142_3_bound_pack",
            "OVERLAP_BOUND_ROWS_FILLED",
            "Source-ready rows now exist for S_phi, chi_U, B_phi_chi, H_phiU2, I_TF and delta_beta_TF.",
            "can become numeric after profile/kernel rows exist",
        ),
        (
            "DG4142_4_next",
            "NEXT_ROUTE_SELECTOR_SELECTED",
            "Since scalar-hair zero is not generic, the next best step is to choose the less-scrutiny completion route: coefficient adoption versus parent no-hair.",
            "4143-Y5-R2FR-tracefree-coefficient-adoption-or-phi-nohair-route-selector.md",
        ),
    ]
    rows: List[dict] = []
    for gate_id, decision, rationale, next_action in data:
        row = row_base()
        row.update(
            {
                "gate_id": gate_id,
                "decision": decision,
                "rationale": rationale,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4142_0",
            "result": DECISION,
            "summary": (
                "4142 reduces H_phiU2=int phi U^2 to int chi_U S_phi plus a boundary bilinear using the local phi equation and adjoint Poisson identity. "
                "This shows scalar-hair U2 orthogonality is not generic: sign-definite nonzero scalar source gives a nonzero overlap unless coefficient matching, no-hair, parent-owned orthogonality or boundary compensation closes. "
                "Nonclaim bound rows for S_phi, chi_U, B_phi_chi, H_phiU2 and beta insertion are filled."
            ),
            "scalar_overlap_reduced": "True",
            "generic_zero_rejected": "True",
            "zero_theorem_signed": "False",
            "overlap_bound_rows_filled": "True",
            "score_ready": "False",
            "claim_state": "no scalar-hair orthogonality claim, trace-free beta zero, q_loc beta pass, total PPN pass, local-GR pass, Newton limit claim, or public evidence claim",
            "next_target": "4143 tracefree coefficient adoption or phi nohair route selector",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4142_0",
            "target_doc": "4143-Y5-R2FR-tracefree-coefficient-adoption-or-phi-nohair-route-selector.md",
            "target_script": "scripts/Y5_R2FR_4143_tracefree_coefficient_adoption_or_phi_nohair_route_selector.py",
            "objective": (
                "compare the two remaining clean trace-free beta zero routes: source-sign epsilon_TF=1-sigma_resp*c_I=0 through parent coefficient adoption, "
                "or prove a parent phi no-hair/weighted-source orthogonality theorem; choose the route with fewer unsourced assumptions and emit bound rows for the rejected branch"
            ),
            "success_gate": "one route is parent-signed as lower-scrutiny, or both remain nonclaim with explicit bound/acquisition rows",
            "reason": "4142 rejects generic scalar-hair U2 orthogonality; the next move must choose coefficient adoption or a strong no-hair theorem rather than circling the overlap.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4142_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4142_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4142_SCALAR_OVERLAP_DERIVATION": SOURCE_DIR / "P8_Y5_R2FR_4142_SCALAR_OVERLAP_DERIVATION.csv",
        "P8_Y5_R2FR_4142_ZERO_ROUTE_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4142_ZERO_ROUTE_AUDIT.csv",
        "P8_Y5_R2FR_4142_OVERLAP_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4142_OVERLAP_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4142_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4142_DECISION_GATES.csv",
        "P8_Y5_R2FR_4142_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4142_STATUS.csv",
        "P8_Y5_R2FR_4142_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4142_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    sections = [
        "# 4142 - Scalar Hair U2 Orthogonality Or Beta Overlap Bound",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- `H_phiU2=int phi U^2` is reduced to a weighted phi-source integral plus boundary bilinear.",
        "- Generic scalar-hair orthogonality is rejected: it needs coefficient matching, no-hair, parent-owned orthogonality, or boundary compensation.",
        "- No beta/local-GR/Newton claim is made.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(
        [
            "",
            "## Core Identity",
            "",
            "Let `Delta phi=S_phi` and `Delta chi_U=U^2`.",
            "",
            "`H_phiU2=int_Omega phi U^2 d^3x`",
            "",
            "`H_phiU2=int_Omega chi_U S_phi d^3x + int_partialOmega(phi partial_n chi_U-chi_U partial_n phi)dS`.",
            "",
            "With the MTS local auxiliary branch:",
            "",
            "`S_phi=(2/3)(Gamma_eff+C)+R_phi_owner+R_lambda+R_boundary`.",
            "",
            "So scalar-hair beta safety is now a source-orthogonality/no-hair problem.",
            "",
            "## Zero Route Audit",
            "",
            "| route | status | blocker |",
            "|---|---|---|",
        ]
    )
    for row in zero_route_audit_rows():
        sections.append(f"| {row['route']} | {row['status']} | {row['blocker']} |")
    sections.extend(
        [
            "",
            "## Bound Rows",
            "",
            "| symbol | status | required inputs |",
            "|---|---|---|",
        ]
    )
    for row in overlap_bound_rows():
        sections.append(f"| {row['symbol']} | {row['status']} | {row['required_inputs']} |")
    sections.extend(
        [
            "",
            "## Claim Ceiling",
            "",
            "- No scalar-hair orthogonality claim, trace-free beta zero, `q_loc` beta pass, total PPN pass, local-GR pass, Newton-limit claim, or public evidence claim follows from 4142.",
            "- The useful movement is that generic scalar hair is now known not to be automatically safe; the route must choose coefficient adoption or a real no-hair theorem.",
            "",
            "## Next Target",
            "",
            "- `4143-Y5-R2FR-tracefree-coefficient-adoption-or-phi-nohair-route-selector.md`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4142_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4142_SCALAR_OVERLAP_DERIVATION": scalar_overlap_derivation_rows,
        "P8_Y5_R2FR_4142_ZERO_ROUTE_AUDIT": zero_route_audit_rows,
        "P8_Y5_R2FR_4142_OVERLAP_BOUND_ROWS": overlap_bound_rows,
        "P8_Y5_R2FR_4142_DECISION_GATES": decision_gate_rows,
        "P8_Y5_R2FR_4142_STATUS": status_rows,
        "P8_Y5_R2FR_4142_NEXT_TARGET": next_target_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4142_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add(
        "VAL4142_1_doc",
        "checkpoint markdown exists and names decision",
        DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"),
        str(DOC_PATH),
    )

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4142_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    derivation_text = flatten_rows([outputs["P8_Y5_R2FR_4142_SCALAR_OVERLAP_DERIVATION"]])
    derivation_ok = all(
        token in derivation_text
        for token in [
            "H_phiU2",
            "Delta phi=S_phi",
            "S_phi=(2/3)(Gamma_eff+C)",
            "NO_GENERIC_ZERO",
            "H_phiU2=0",
            "||chi_U||_2",
            "BETA_INSERTION_DERIVED",
        ]
    )
    add("VAL4142_3_scalar_derivation", "derivation includes H definition, adjoint identity, phi source, generic nonzero guard, zero and bound laws, beta insertion", derivation_ok, "derivation tokens checked")

    audit_text = flatten_rows([outputs["P8_Y5_R2FR_4142_ZERO_ROUTE_AUDIT"]])
    audit_ok = all(
        token in audit_text
        for token in [
            "epsilon_TF=0",
            "phi=0",
            "int chi_U S_phi",
            "B_phi_chi",
            "C selected",
            "NOT_SCORE_READY",
        ]
    )
    add("VAL4142_4_zero_audit", "zero audit covers coefficient, nohair, weighted source, boundary, C calibration and numeric bound", audit_ok, "audit tokens checked")

    bound_text = flatten_rows([outputs["P8_Y5_R2FR_4142_OVERLAP_BOUND_ROWS"]])
    bound_ok = all(
        token in bound_text
        for token in [
            "S_phi",
            "chi_U",
            "B_phi_chi",
            "H_phiU2",
            "H_bound",
            "I_TF",
            "delta_beta_TF",
        ]
    )
    add("VAL4142_5_bound_rows", "bound rows include S_phi, chi_U, boundary bilinear, H overlap, H bound, I_TF and beta residual", bound_ok, "bound tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4142_DECISION_GATES"]])
    decision_ok = all(
        token in decision_text
        for token in [
            "H_PHI_U2_REDUCED_TO_SOURCE_AND_BOUNDARY",
            "NO_GENERIC_SCALAR_ORTHOGONALITY",
            "ZERO_REQUIRES_COEFFICIENT_NOHAIR_OR_PARENT_ORTHOGONALITY",
            "OVERLAP_BOUND_ROWS_FILLED",
            "NEXT_ROUTE_SELECTOR_SELECTED",
        ]
    )
    add("VAL4142_6_decisions", "decisions record source-boundary reduction, no generic zero, clean routes, bound pack and next selector", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4142_STATUS"])
    status_ok = (
        bool(status)
        and status[0].get("result") == DECISION
        and status[0].get("scalar_overlap_reduced") == "True"
        and status[0].get("generic_zero_rejected") == "True"
        and status[0].get("zero_theorem_signed") == "False"
        and status[0].get("overlap_bound_rows_filled") == "True"
    )
    add("VAL4142_7_status", "status records reduced overlap, rejected generic zero, unsigned theorem and filled bound rows", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4142_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4143-Y5-R2FR-tracefree-coefficient-adoption-or-phi-nohair-route-selector.md"
    add("VAL4142_8_next_target", "next target is trace-free coefficient adoption or phi nohair route selector", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4142_9_no_claim_flags", "all generated rows remain no-claim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4142*")) or any(FORMALIZATION.rglob("4142-Y5-R2FR*"))
    add(
        "VAL4142_10_scope",
        "outputs stay in post-checkpoint-work and not formalization-workbench",
        in_scope and not formalization_output and not formalization_touched,
        f"doc={DOC_PATH}; csv_count={len(outputs)}",
    )

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4142_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4142_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
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

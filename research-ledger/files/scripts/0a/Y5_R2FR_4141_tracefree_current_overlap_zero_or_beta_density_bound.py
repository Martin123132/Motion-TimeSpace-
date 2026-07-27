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
DOC_PATH = ROOT / "4141-Y5-R2FR-tracefree-current-overlap-zero-or-beta-density-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_TRACEFREE_CURRENT_OVERLAP_ZERO_OR_BOUND_4141"
CHECKPOINT_ID = "4141"
DECISION = "TRACEFREE_CURRENT_DERIVED_ZERO_REQUIRES_COEFFICIENT_AND_SCALAR_HAIR_ORTHOGONALITY"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4141_00_4140_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4140_NEXT_TARGET.csv",
        "4141-Y5-R2FR-tracefree-current-overlap-zero-or-beta-density-bound.md",
        "4140 selected trace-free current-overlap zero or beta-density bound.",
    ),
    "SRC4141_01_4140_density": (
        SOURCE_DIR / "P8_Y5_R2FR_4140_SOURCE_DENSITY_DERIVATION.csv",
        "partial_i J_q^i",
        "4140 source-density reduction to divergence-current form.",
    ),
    "SRC4141_02_4140_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4140_DIVERGENCE_PROJECTOR_THEOREM.csv",
        "I_J",
        "4140 adjoint divergence projector theorem.",
    ),
    "SRC4141_03_4140_rows": (
        SOURCE_DIR / "P8_Y5_R2FR_4140_FIRST_DENSITY_ROWS.csv",
        "B_J",
        "4140 first density rows for boundary and overlap terms.",
    ),
    "SRC4141_04_4138_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT.csv",
        "sigma_resp*c_I=1",
        "4138 coefficient/sign blocker for trace-free Khat adoption.",
    ),
    "SRC4141_05_4138_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_ZERO_THEOREM_OR_BOUND.csv",
        "A_TF/L_TF <=",
        "4138 trace-free residual amplitude law.",
    ),
    "SRC4141_06_4139_projector": (
        SOURCE_DIR / "P8_Y5_R2FR_4139_CBETA_QLOC_PROJECTOR_DERIVATION.csv",
        "C_beta_qloc[D]",
        "4139 same-normalized beta projector definition.",
    ),
    "SRC4141_07_1287_component": (
        SOURCE_DIR / "P8_Y5_R10_1287_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv",
        "partial_mu K_L",
        "1287 flat/local cancellation row for the K_L component.",
    ),
    "SRC4141_08_1525_origin": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1525_KHAT_ORIGIN_AUDIT.csv",
        "trace-free Hessian identity",
        "1525 K_L origin audit.",
    ),
    "SRC4141_09_1526_variation": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1526_VARIATION_DERIVATION.csv",
        "EXACT_TRACEFREE_MATCH_DERIVED",
        "1526 trace-free phi R response derivation.",
    ),
    "SRC4141_10_833_amplitude": (
        SOURCE_DIR / "P8_Y5_R10_833_HESSIAN_KHAT_AMPLITUDE_LAW.csv",
        "sqrt(n/(n-1))",
        "833 amplitude law warning: no parametric suppression from K_L shape alone.",
    ),
    "SRC4141_11_2220_birth": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_2220_TRACEFREE_IMPROVEMENT_BIRTH_CERTIFICATE.csv",
        "BIRTH_CERTIFICATE_FAILS_CURRENT_CORPUS",
        "2220 current-corpus nonpromotion of trace-free route.",
    ),
    "SRC4141_12_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4141_tracefree_current_overlap_zero_or_beta_density_bound.py",
        "Reproducible generator for this 4141 checkpoint.",
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


def current_derivation_rows() -> List[dict]:
    data = [
        (
            "CD4141_0_tracefree_tensor",
            "trace-free tensor",
            "K_L^{mu nu}=2[nabla^mu nabla^nu phi-(1/4)g^{mu nu}Box phi]",
            "In the static weak-field local patch, the time-derivative part is suppressed and K_L^{00}=+1/2 Delta phi up to the declared sign convention.",
            "STATIC_COMPONENT_DERIVED",
            "requires PPN sign convention and static/collar assumptions",
        ),
        (
            "CD4141_1_phi_source",
            "phi source relation",
            "Box phi=(2/3)(Gamma_eff+C)",
            "The same relation gives K_L^{00}=Gamma_eff/3 in the flat/local static branch, matching the older partial_mu K_L cancellation.",
            "CONDITIONAL_FLAT_BRANCH",
            "phi owner and local branch are not live-adopted",
        ),
        (
            "CD4141_2_residual_coefficient",
            "coefficient mismatch",
            "epsilon_TF:=1-sigma_resp*c_I",
            "If epsilon_TF=0, the trace-free derivative current vanishes before any beta projection.",
            "ZERO_IF_COEFFICIENT_SIGNED",
            "sigma_resp*c_I=1 is derived but not source-fixed",
        ),
        (
            "CD4141_3_source_density",
            "trace-free beta source density",
            "S_TF^{(4)}=lambda_00^TF*epsilon_TF*K_L^{00}+lambda_phiG*phi G_TF^{00}+S_owner+S_boundary+S_adoption",
            "The first term is the clean divergence-current piece; the remaining terms are bulk/remnant terms.",
            "SOURCE_SPLIT_DERIVED",
            "lambda_00^TF and remnant projections are not numeric/source-backed",
        ),
        (
            "CD4141_4_current",
            "trace-free current",
            "J_TF^i=(lambda_00^TF*epsilon_TF/2) partial^i phi",
            "This is the concrete current whose divergence supplies the leading trace-free improvement beta source in the static weak-field branch.",
            "CURRENT_DERIVED_CONDITIONAL",
            "profile phi and lambda_00^TF are not source-backed",
        ),
        (
            "CD4141_5_divergence",
            "current divergence",
            "partial_i J_TF^i=(lambda_00^TF*epsilon_TF/2) Delta phi=(lambda_00^TF*epsilon_TF/3)(Gamma_eff+C)",
            "The current is not automatically small; it is controlled by coefficient mismatch and scalar/source profile.",
            "DIVERGENCE_LAW_DERIVED",
            "Gamma_eff/C profile and support are not source-backed",
        ),
        (
            "CD4141_6_bulk_remainders",
            "bulk remainders",
            "S_TF,bulk=lambda_phiG*phi G_TF^{00}+S_owner+S_boundary+S_adoption+S_gauge",
            "Curvature, owner, boundary, adoption and gauge terms cannot be erased by calling the leading term a divergence.",
            "REMAINDER_LEDGER_KEPT",
            "all remainders must be zero-signed or bounded",
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


def overlap_reduction_rows() -> List[dict]:
    data = [
        (
            "OR4141_0_boundary_term",
            "B_TF",
            "B_TF=(lambda_00^TF*epsilon_TF/2) int_partialOmega chi_U n_i partial^i phi dS",
            "This is the trace-free current boundary term in the adjoint beta projection.",
            "BOUNDARY_TERM_DERIVED",
        ),
        (
            "OR4141_1_current_overlap",
            "I_TF",
            "I_TF=(lambda_00^TF*epsilon_TF/2) int_Omega partial^i phi partial_i chi_U d^3x",
            "This is the core current-overlap term; it is the new local beta test.",
            "OVERLAP_TERM_DERIVED",
        ),
        (
            "OR4141_2_scalar_overlap",
            "I_TF_scalar",
            "I_TF=(lambda_00^TF*epsilon_TF/2)[int_partialOmega phi n_i partial^i chi_U dS - int_Omega phi U^2 d^3x]",
            "After one more integration by parts, beta safety requires a scalar-hair overlap condition, not just divergence form.",
            "SCALAR_HAIR_OVERLAP_EXPOSED",
        ),
        (
            "OR4141_3_zero_law",
            "trace-free beta zero",
            "delta_beta_TF=0 if epsilon_TF=0 OR {B_TF=0, I_TF=0, S_TF,bulk=0, S_TF,gauge=0}",
            "There are two clean roads: coefficient match or boundary/current orthogonality with no bulk/gauge remnants.",
            "ZERO_LAW_DERIVED_NOT_SIGNED",
        ),
        (
            "OR4141_4_bound_law",
            "trace-free beta bound",
            "|delta_beta_TF| <= (|B_TF|+|I_TF|+|I_phiG|+|I_owner|+|I_boundary|+|I_adoption|+|I_gauge|)/(2N_U2)",
            "If zero fails, the trace-free beta residual is now a concrete absolute-overlap bound.",
            "BOUND_LAW_DERIVED",
        ),
    ]
    rows: List[dict] = []
    for reduction_id, item, formula, meaning, status in data:
        row = row_base()
        row.update(
            {
                "reduction_id": reduction_id,
                "item": item,
                "formula": formula,
                "meaning": meaning,
                "status": status,
                "theorem_zero_signed": "False",
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def zero_or_bound_gate_rows() -> List[dict]:
    data = [
        (
            "ZG4141_0_coefficient",
            "coefficient zero",
            "epsilon_TF=1-sigma_resp*c_I=0",
            "DERIVED_TARGET_UNSIGNED",
            "4138 has the law but not source-fixed current coefficients",
        ),
        (
            "ZG4141_1_boundary",
            "boundary term zero",
            "B_TF=0 on the PPN collar",
            "UNSIGNED_BOUNDARY",
            "no-flux/collar proof has not been mapped to chi_U weighted boundary",
        ),
        (
            "ZG4141_2_current_overlap",
            "current overlap zero",
            "I_TF=int partial^i phi partial_i chi_U=0",
            "UNSIGNED_CORE_TEST",
            "requires scalar profile/adjoint potential orthogonality",
        ),
        (
            "ZG4141_3_scalar_hair",
            "scalar-hair overlap zero",
            "int phi U^2 d^3x equals the compensating boundary term or vanishes",
            "UNSIGNED_SCALAR_HAIR",
            "generic scalar hair would not satisfy this automatically",
        ),
        (
            "ZG4141_4_bulk",
            "curvature/owner/boundary/adoption bulk zero",
            "I_phiG=I_owner=I_boundary=I_adoption=I_gauge=0 or bounded",
            "UNSIGNED_REMAINDERS",
            "trace-free route still fails birth certificate in current corpus",
        ),
        (
            "ZG4141_5_numeric_bound",
            "source-backed beta bound",
            "all numerator overlaps and N_U2 numeric/source-backed with no MISSING markers",
            "NOT_SCORE_READY",
            "lambda_00^TF, phi profile, chi_U, U, N_U2 and remnant integrals missing",
        ),
    ]
    rows: List[dict] = []
    for gate_id, gate, pass_condition, status, blocker in data:
        row = row_base()
        row.update(
            {
                "gate_id": gate_id,
                "gate": gate,
                "pass_condition": pass_condition,
                "status": status,
                "blocker": blocker,
                "gate_passed": "False",
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def beta_density_bound_rows() -> List[dict]:
    data = [
        (
            "BD4141_0_current_profile",
            "J_TF^i",
            "(lambda_00^TF*epsilon_TF/2) partial^i phi",
            "source density times length",
            "lambda_00^TF; epsilon_TF; phi profile; PPN sign convention",
            "MISSING_SOURCE_BACKED_PROFILE",
        ),
        (
            "BD4141_1_boundary",
            "B_TF",
            "(lambda_00^TF*epsilon_TF/2) int_partialOmega chi_U n_i partial^i phi dS",
            "projected beta numerator units",
            "chi_U; collar surface; normal derivative of phi; no-flux theorem or value",
            "MISSING_BOUNDARY_VALUE",
        ),
        (
            "BD4141_2_overlap",
            "I_TF",
            "(lambda_00^TF*epsilon_TF/2) int_Omega partial^i phi partial_i chi_U d^3x",
            "projected beta numerator units",
            "phi profile; chi_U; domain/window",
            "MISSING_CURRENT_OVERLAP",
        ),
        (
            "BD4141_3_scalar_overlap",
            "H_phiU2",
            "int_Omega phi U^2 d^3x",
            "scalar-hair beta numerator units after adjoint integration",
            "source-normalized U; phi; Omega/window; boundary compensation",
            "MISSING_SCALAR_HAIR_OVERLAP",
        ),
        (
            "BD4141_4_bulk_remainders",
            "I_rem_TF",
            "I_phiG+I_owner+I_boundary+I_adoption+I_gauge",
            "projected beta numerator units",
            "curvature routing; owner stress; boundary; adoption; gauge rows",
            "MISSING_REMAINDER_BOUNDS",
        ),
        (
            "BD4141_5_beta_bound",
            "delta_beta_TF",
            "|delta_beta_TF| <= (|B_TF|+|I_TF|+|I_rem_TF|)/(2N_U2)",
            "dimensionless beta",
            "B_TF; I_TF; I_rem_TF; N_U2; total beta envelope",
            "NONCLAIM_BOUND_ROW",
        ),
        (
            "BD4141_6_total_guard",
            "delta_beta_total",
            "|delta_beta_total| <= |delta_beta_source|+|delta_beta_R11|+|delta_beta_TF|+|delta_beta_boundary|+|delta_beta_readout|",
            "dimensionless beta",
            "all beta channels score-ready or theorem-zero",
            "TOTAL_PPN_GUARD_NONCLAIM",
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
            "DG4141_0_current_derived",
            "TRACEFREE_CURRENT_DERIVED",
            "The leading trace-free/improvement beta source is a divergence current J_TF^i=(lambda_00^TF epsilon_TF/2)partial^i phi in the static weak-field branch.",
            "use this as the first concrete trace-free beta current",
        ),
        (
            "DG4141_1_no_shortcut",
            "DIVERGENCE_NOT_ZERO_BY_ITSELF",
            "The beta projection reduces to B_TF and I_TF; divergence form alone does not close local GR.",
            "keep boundary/current-overlap tests active",
        ),
        (
            "DG4141_2_coefficient_or_overlap",
            "ZERO_REQUIRES_COEFFICIENT_OR_ORTHOGONALITY",
            "Trace-free beta is zero if epsilon_TF=0, or if boundary/current/scalar-hair overlaps and all remainders vanish.",
            "derive coefficient adoption or scalar-hair orthogonality next",
        ),
        (
            "DG4141_3_bound_rows",
            "BETA_DENSITY_BOUND_ROWS_FILLED",
            "The first nonclaim rows for J_TF, B_TF, I_TF, scalar-hair overlap and remnant integrals are now explicit.",
            "can become numeric only after phi/U/chi_U/source rows exist",
        ),
        (
            "DG4141_4_next",
            "NEXT_SCALAR_HAIR_ORTHOGONALITY_SELECTED",
            "The most surgical next proof is H_phiU2=int phi U^2 d^3x zero or bound, because it is the adjoint form of I_TF.",
            "4142-Y5-R2FR-scalar-hair-U2-orthogonality-or-beta-overlap-bound.md",
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
            "status_id": "STATUS4141_0",
            "result": DECISION,
            "summary": (
                "4141 derives the concrete trace-free/improvement current in the static weak-field branch: "
                "J_TF^i=(lambda_00^TF epsilon_TF/2) partial^i phi, with epsilon_TF=1-sigma_resp*c_I. "
                "Thus the beta projection is zero only if the coefficient match is source-signed or if the adjoint boundary/current/scalar-hair overlaps vanish with all remnant terms controlled. "
                "This is a sharper route than merely saying a divergence is safe."
            ),
            "tracefree_current_derived": "True",
            "coefficient_zero_signed": "False",
            "boundary_overlap_zero_signed": "False",
            "scalar_hair_overlap_bound_filled": "True",
            "score_ready": "False",
            "claim_state": "no trace-free beta zero, q_loc beta pass, total PPN pass, local-GR pass, Newton limit claim, or public evidence claim",
            "next_target": "4142 scalar-hair U2 orthogonality or beta-overlap bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4141_0",
            "target_doc": "4142-Y5-R2FR-scalar-hair-U2-orthogonality-or-beta-overlap-bound.md",
            "target_script": "scripts/Y5_R2FR_4142_scalar_hair_U2_orthogonality_or_beta_overlap_bound.py",
            "objective": (
                "derive whether the scalar-hair overlap H_phiU2=int_Omega phi U^2 d^3x vanishes from the local phi equation, boundary conditions, support, or source calibration; "
                "if not, emit source-ready bound rows for H_phiU2 and the compensating boundary terms"
            ),
            "success_gate": "H_phiU2 is theorem-zero/compensated by boundary terms, or source-backed enough to bound I_TF and delta_beta_TF",
            "reason": "4141 reduces the trace-free current overlap to scalar-hair U^2 overlap; that is now the narrowest non-circular beta/local-GR test.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4141_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4141_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4141_TRACEFREE_CURRENT_DERIVATION": SOURCE_DIR / "P8_Y5_R2FR_4141_TRACEFREE_CURRENT_DERIVATION.csv",
        "P8_Y5_R2FR_4141_ADJOINT_OVERLAP_REDUCTION": SOURCE_DIR / "P8_Y5_R2FR_4141_ADJOINT_OVERLAP_REDUCTION.csv",
        "P8_Y5_R2FR_4141_ZERO_OR_BOUND_GATES": SOURCE_DIR / "P8_Y5_R2FR_4141_ZERO_OR_BOUND_GATES.csv",
        "P8_Y5_R2FR_4141_BETA_DENSITY_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4141_BETA_DENSITY_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4141_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4141_DECISION_GATES.csv",
        "P8_Y5_R2FR_4141_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4141_STATUS.csv",
        "P8_Y5_R2FR_4141_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4141_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    sections = [
        "# 4141 - Tracefree Current Overlap Zero Or Beta Density Bound",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- The leading trace-free/improvement beta source has a concrete current in the static weak-field branch.",
        "- The route does not prove local GR yet: zero needs coefficient match or adjoint scalar-hair orthogonality plus boundary/remnant silence.",
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
            "## Current Law",
            "",
            "With `epsilon_TF:=1-sigma_resp*c_I`, the leading static weak-field trace-free current is",
            "",
            "`J_TF^i=(lambda_00^TF*epsilon_TF/2) partial^i phi`.",
            "",
            "Its divergence is",
            "",
            "`partial_i J_TF^i=(lambda_00^TF*epsilon_TF/2) Delta phi=(lambda_00^TF*epsilon_TF/3)(Gamma_eff+C)`.",
            "",
            "So coefficient signing, not wishful smallness, is the clean zero route.",
            "",
            "## Adjoint Overlap",
            "",
            "`B_TF=(lambda_00^TF*epsilon_TF/2) int_partialOmega chi_U n_i partial^i phi dS`.",
            "",
            "`I_TF=(lambda_00^TF*epsilon_TF/2) int_Omega partial^i phi partial_i chi_U d^3x`.",
            "",
            "After integration by parts:",
            "",
            "`I_TF=(lambda_00^TF*epsilon_TF/2)[int_partialOmega phi n_i partial^i chi_U dS - int_Omega phi U^2 d^3x]`.",
            "",
            "That exposes the next target: scalar-hair overlap with `U^2`.",
            "",
            "## Zero Or Bound Gates",
            "",
            "| gate | status | blocker |",
            "|---|---|---|",
        ]
    )
    for row in zero_or_bound_gate_rows():
        sections.append(f"| {row['gate']} | {row['status']} | {row['blocker']} |")
    sections.extend(
        [
            "",
            "## Bound Rows",
            "",
            "| symbol | status | required inputs |",
            "|---|---|---|",
        ]
    )
    for row in beta_density_bound_rows():
        sections.append(f"| {row['symbol']} | {row['status']} | {row['required_inputs']} |")
    sections.extend(
        [
            "",
            "## Claim Ceiling",
            "",
            "- No trace-free beta zero, `q_loc` beta pass, total PPN pass, local-GR pass, Newton-limit claim, or public evidence claim follows from 4141.",
            "- The useful movement is that the next proof is now the scalar-hair overlap `int phi U^2`, not a generic missing coefficient.",
            "",
            "## Next Target",
            "",
            "- `4142-Y5-R2FR-scalar-hair-U2-orthogonality-or-beta-overlap-bound.md`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4141_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4141_TRACEFREE_CURRENT_DERIVATION": current_derivation_rows,
        "P8_Y5_R2FR_4141_ADJOINT_OVERLAP_REDUCTION": overlap_reduction_rows,
        "P8_Y5_R2FR_4141_ZERO_OR_BOUND_GATES": zero_or_bound_gate_rows,
        "P8_Y5_R2FR_4141_BETA_DENSITY_BOUND_ROWS": beta_density_bound_rows,
        "P8_Y5_R2FR_4141_DECISION_GATES": decision_gate_rows,
        "P8_Y5_R2FR_4141_STATUS": status_rows,
        "P8_Y5_R2FR_4141_NEXT_TARGET": next_target_rows,
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
        "VAL4141_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add(
        "VAL4141_1_doc",
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
    add("VAL4141_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    current_text = flatten_rows([outputs["P8_Y5_R2FR_4141_TRACEFREE_CURRENT_DERIVATION"]])
    current_ok = all(
        token in current_text
        for token in [
            "K_L^{00}",
            "epsilon_TF:=1-sigma_resp*c_I",
            "S_TF^{(4)}",
            "J_TF^i",
            "partial_i J_TF^i",
            "S_TF,bulk",
        ]
    )
    add("VAL4141_3_current_derivation", "current derivation includes K_L00, coefficient mismatch, source density, J_TF, divergence and bulk ledger", current_ok, "current tokens checked")

    overlap_text = flatten_rows([outputs["P8_Y5_R2FR_4141_ADJOINT_OVERLAP_REDUCTION"]])
    overlap_ok = all(
        token in overlap_text
        for token in [
            "B_TF",
            "I_TF",
            "int_Omega phi U^2",
            "delta_beta_TF=0",
            "BOUND_LAW_DERIVED",
        ]
    )
    add("VAL4141_4_overlap_reduction", "overlap reduction includes boundary, current overlap, scalar U2 overlap, zero law and bound law", overlap_ok, "overlap tokens checked")

    gate_text = flatten_rows([outputs["P8_Y5_R2FR_4141_ZERO_OR_BOUND_GATES"]])
    gate_ok = all(
        token in gate_text
        for token in [
            "epsilon_TF",
            "B_TF=0",
            "I_TF",
            "int phi U^2",
            "I_phiG",
            "NOT_SCORE_READY",
        ]
    )
    add("VAL4141_5_zero_gates", "zero gates cover coefficient, boundary, current overlap, scalar hair, remainders and numeric bound", gate_ok, "gate tokens checked")

    bound_text = flatten_rows([outputs["P8_Y5_R2FR_4141_BETA_DENSITY_BOUND_ROWS"]])
    bound_ok = all(
        token in bound_text
        for token in [
            "J_TF^i",
            "B_TF",
            "I_TF",
            "H_phiU2",
            "I_rem_TF",
            "delta_beta_TF",
            "delta_beta_total",
        ]
    )
    add("VAL4141_6_bound_rows", "bound rows include J, boundary, overlap, scalar-hair, remnants, beta and total guard", bound_ok, "bound tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4141_DECISION_GATES"]])
    decision_ok = all(
        token in decision_text
        for token in [
            "TRACEFREE_CURRENT_DERIVED",
            "DIVERGENCE_NOT_ZERO_BY_ITSELF",
            "ZERO_REQUIRES_COEFFICIENT_OR_ORTHOGONALITY",
            "BETA_DENSITY_BOUND_ROWS_FILLED",
            "NEXT_SCALAR_HAIR_ORTHOGONALITY_SELECTED",
        ]
    )
    add("VAL4141_7_decisions", "decisions record current derivation, no divergence shortcut, zero choices, bound rows and next scalar-hair target", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4141_STATUS"])
    status_ok = (
        bool(status)
        and status[0].get("result") == DECISION
        and status[0].get("tracefree_current_derived") == "True"
        and status[0].get("coefficient_zero_signed") == "False"
        and status[0].get("boundary_overlap_zero_signed") == "False"
        and status[0].get("scalar_hair_overlap_bound_filled") == "True"
    )
    add("VAL4141_8_status", "status records derived current, unsigned coefficient/boundary/overlap and filled scalar-hair bound row", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4141_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4142-Y5-R2FR-scalar-hair-U2-orthogonality-or-beta-overlap-bound.md"
    add("VAL4141_9_next_target", "next target is scalar-hair U2 orthogonality or beta-overlap bound", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4141_10_no_claim_flags", "all generated rows remain no-claim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4141*")) or any(FORMALIZATION.rglob("4141-Y5-R2FR*"))
    add(
        "VAL4141_11_scope",
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
    add("VAL4141_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4141_VALIDATION.csv"
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

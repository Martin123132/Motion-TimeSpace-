from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3245"
DOC = ROOT / "3245-Y5-R2FR-MAB-coercivity-and-first-Jtot-component-bound-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3245_SOURCE_REGISTER.csv",
    "coercivity": OUT / "P8_Y5_R2FR_3245_MAB_COERCIVITY_CERTIFICATE_ATTEMPT.csv",
    "schur": OUT / "P8_Y5_R2FR_3245_BLOCK_POSITIVITY_AND_SCHUR_GUARD.csv",
    "jcomponent": OUT / "P8_Y5_R2FR_3245_FIRST_JTOT_COMPONENT_BOUND_INTERFACE.csv",
    "score_row": OUT / "P8_Y5_R2FR_3245_FIRST_SCORE_ROW_REQUIREMENTS.csv",
    "amplitude": OUT / "P8_Y5_R2FR_3245_AMPLITUDE_SCORING_TRANSFER.csv",
    "gates": OUT / "P8_Y5_R2FR_3245_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3245_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3245_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3245_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            low = line.lower()
            if any(needle in low for needle in lowered):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:220]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3245_3244",
            ROOT / "3244-Y5-R2FR-single-parent-density-boundary-reference-proof-or-finite-Jtot-bound-under-AX1090.md",
            "Jtot zero-or-bound and amplitude handoff",
            ["J_A^tot", "m0", "Z_*", "M_AB"],
        ),
        (
            "SRC3245_2977",
            ROOT / "2977-Y5-R2FR-response-doublet-MAB-Zbasis-owner-and-no-linear-source-lock-or-DeltaK-deltaM-row-under-AX1090.md",
            "response-doublet M_AB/Z owner gap",
            ["M_AB", "positive", "H_AB", "J_Z"],
        ),
        (
            "SRC3245_1025",
            ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
            "older exact second-variation/Hessian contract",
            ["second-variation", "Z_X", "M_X", "Hessian"],
        ),
        (
            "SRC3245_1026",
            ROOT / "1026-Y5-R10-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
            "older parent metric/Hessian route failure",
            ["M_AB", "parent metric", "Hessian", "cross"],
        ),
        (
            "SRC3245_2992",
            ROOT / "2992-Y5-R2FR-extra-double-zero-and-zero-odd-source-proof-or-epsilon-Qv-extra-bound-under-AX1090.md",
            "canonical positive-gap theorem pattern",
            ["positive", "gap", "Hessian", "mass gap"],
        ),
        (
            "SRC3245_2993",
            ROOT / "2993-Y5-R2FR-parent-extra-sector-source-normal-form-pack-or-first-epsilon-Qv-extra-numeric-row-under-AX1090.md",
            "extra-sector source pack and positive gap audit",
            ["positive", "Hessian", "source pack", "J_Z"],
        ),
        (
            "SRC3245_3234",
            ROOT / "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md",
            "Poynting/collar flux finite component",
            ["Poynting", "J_Poynting_bound", "T_EM", "finite bound"],
        ),
        (
            "SRC3245_3234_flux_csv",
            OUT / "P8_Y5_R2FR_3234_FINITE_FLUX_BOUND.csv",
            "machine finite Poynting/collar bound rows",
            ["PB3234_0_boundary_flux", "PB3234_1_collar_source", "C_flux", "C_coll"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def coercivity_rows() -> list[dict[str, Any]]:
    return [
        {
            "cert_id": "MAB3245_0_definition",
            "object": "response Hessian",
            "certificate": "M_AB := partial_A partial_B Gamma_eff|_{Z=0} on the parent-owned vertical response subspace V_Z",
            "derived_result": "formal second-variation object identified",
            "current_status": "OBJECT_DEFINED_NOT_PARENT_SIGNED",
            "claim_allowed": "false",
        },
        {
            "cert_id": "MAB3245_1_symmetry",
            "object": "symmetric bilinear form",
            "certificate": "M_AB=M_BA if Gamma_eff is C2 and Z^A coordinates are fixed on one branch",
            "derived_result": "Schwarz symmetry gives formal symmetry",
            "current_status": "CONDITIONAL_ON_BRANCH_AND_UNITS",
            "claim_allowed": "false",
        },
        {
            "cert_id": "MAB3245_2_coercivity_theorem",
            "object": "positive lower bound",
            "certificate": "m0 := inf_{Z in V_Z, ||Z||_Z=1} <Z,MZ>; if M is self-adjoint, gauge kernels are quotiented, and spectrum(M|V_Z)>=m0>0, then ||Z_*|| <= m0^{-1}||J_tot||",
            "derived_result": "exact coercivity-to-amplitude theorem",
            "current_status": "THEOREM_DERIVED_INPUTS_UNSIGNED",
            "claim_allowed": "false",
        },
        {
            "cert_id": "MAB3245_3_no_zero_modes",
            "object": "kernel guard",
            "certificate": "ker(M) on V_Z is empty after quotient/gauge removal; otherwise use Moore-Penrose inverse and retain kernel source projection",
            "derived_result": "zero-mode failure mode made explicit",
            "current_status": "KERNEL_AUDIT_MISSING",
            "claim_allowed": "false",
        },
        {
            "cert_id": "MAB3245_4_units_norm",
            "object": "common units and norm",
            "certificate": "J_tot and M_AB must use the same Z-normalization, density weight, local volume/collar norm, and branch frame",
            "derived_result": "prevents fake small amplitude from unit mismatch",
            "current_status": "UNITS_AND_NORM_NOT_SOURCED",
            "claim_allowed": "false",
        },
        {
            "cert_id": "MAB3245_5_verdict",
            "object": "current MTS M_AB",
            "certificate": "M_AB coercivity is the right next owner object, but current corpus still lacks parent-signed spectrum/units",
            "derived_result": "do not claim amplitude safety; use m0 acquisition row",
            "current_status": "COERCIVITY_NOT_PROMOTED",
            "claim_allowed": "false",
        },
    ]


def schur_rows() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "SCH3245_0_full_matrix",
            "risk": "single-mode truncation hides negative or flat orthogonal direction",
            "condition": "full response Hessian block matrix is self-adjoint on V_Z",
            "bound_or_test": "compute Rayleigh lower bound on full M_AB, not just a preferred X direction",
            "status": "REQUIRED_GUARD",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "SCH3245_1_schur",
            "risk": "cross-coupling makes a positive diagonal block unstable",
            "condition": "M_YY >= y0 I and Schur(M_X)=M_XX-M_XY M_YY^{-1} M_YX >= x0>0",
            "bound_or_test": "m0 >= min(y0,x0) under same norm; otherwise retain cross-block residual",
            "status": "FORMAL_TEST_DERIVED_INPUTS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "SCH3245_2_source_projection",
            "risk": "J_tot projects onto a kernel even if non-kernel modes are positive",
            "condition": "Pi_kernel J_tot=0 or kernel sector is gauge/topological and not physical",
            "bound_or_test": "if not, amplitude bound has an unbounded kernel term",
            "status": "KERNEL_SOURCE_PROJECTION_OPEN",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "SCH3245_3_boundary_domain",
            "risk": "operator positive under one boundary/domain but evaluated under another",
            "condition": "same local collar/worldtube/domain used for M_AB, J_tot and q_loc arena",
            "bound_or_test": "domain mismatch becomes eps_MAB_domain + eps_boundary_projector",
            "status": "DOMAIN_LOCK_OPEN",
            "valid_for_claim": "false",
        },
    ]


def first_component_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "JTC3245_0_selected",
            "component": "boundary/Poynting flux contribution to B_A subset J_A^tot",
            "source_basis": "3234 finite Poynting/collar flux functional",
            "bound": "|J_A^Poynting| <= ||e_A||_B (C_flux ||S_EM dot n||_B + B_corner_flux) + ||e_A||_coll C_coll ||T_EM(u,n)||_collar",
            "units_requirement": "same action-density or boundary-work units as J_A^tot; e_A normalization declared",
            "current_value": "MISSING_NUMERIC_FLUX_NORMS_AND_CONSTANTS",
            "status": "FIRST_CONCRETE_COMPONENT_INTERFACE",
            "valid_for_claim": "false",
        },
        {
            "component_id": "JTC3245_1_zero_condition",
            "component": "Poynting no-flux zero special case",
            "source_basis": "3234 boundary silence audit",
            "bound": "J_A^Poynting=0 only if S_EM dot n=0 on parent-owned boundary/collar or flux is exact/proper and annihilated",
            "units_requirement": "boundary frame u,n and support class must be parent-owned",
            "current_value": "ZERO_NOT_CLAIMED",
            "status": "ZERO_ROUTE_DEFINED_NOT_ACTIVATED",
            "valid_for_claim": "false",
        },
        {
            "component_id": "JTC3245_2_total_insertion",
            "component": "Jtot update",
            "source_basis": "3244 finite Jtot contract",
            "bound": "||J_tot|| <= ||J_bulk|| + |J_A^Poynting| + ||B_other|| + ||J_oddGamma||",
            "units_requirement": "absolute no-cancellation sum in common norm",
            "current_value": "TOTAL_STILL_MISSING_OTHER_COMPONENTS",
            "status": "TOTAL_BOUND_PARTIALLY_FILLED",
            "valid_for_claim": "false",
        },
    ]


def score_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "field": "component_id",
            "required_for_first_score_row": "JTC3245_0_selected",
            "why": "binds the row to the Poynting/collar component",
            "current_status": "declared",
        },
        {
            "field": "boundary_id",
            "required_for_first_score_row": "parent-owned local boundary/collar/worldtube label",
            "why": "prevents moving the surface after fitting",
            "current_status": "missing",
        },
        {
            "field": "frame_u_n",
            "required_for_first_score_row": "observed frame u and boundary normal n",
            "why": "Poynting stress T_EM(u,n) is frame/surface dependent",
            "current_status": "missing",
        },
        {
            "field": "C_flux_C_coll",
            "required_for_first_score_row": "finite constants mapping flux norm to Jtot norm",
            "why": "needed to convert EM boundary flux into response source covector units",
            "current_status": "missing",
        },
        {
            "field": "flux_norms",
            "required_for_first_score_row": "||S_EM dot n||_B and ||T_EM(u,n)||_collar",
            "why": "the first actual numeric component value comes from these",
            "current_status": "missing",
        },
        {
            "field": "eA_norm",
            "required_for_first_score_row": "||e_A||_B and ||e_A||_collar under the same Z normalization used by M_AB",
            "why": "locks Jtot to the M_AB amplitude denominator",
            "current_status": "missing",
        },
        {
            "field": "units_source_path",
            "required_for_first_score_row": "source path and units convention",
            "why": "blocks fake dimensionless promotion",
            "current_status": "missing",
        },
    ]


def amplitude_rows() -> list[dict[str, Any]]:
    return [
        {
            "transfer_id": "AMP3245_0_if_coercive",
            "input": "m0>0 and first finite Jtot component row",
            "formula": "||Z_*|| <= m0^{-1}(||J_bulk|| + |J_A^Poynting| + ||B_other|| + ||J_oddGamma||)",
            "use": "first partial score of response amplitude",
            "claim_allowed": "false",
        },
        {
            "transfer_id": "AMP3245_1_density_shift",
            "input": "same m0 and Jtot bound",
            "formula": "|Delta Gamma_min| <= (2m0)^{-1}||J_tot||^2",
            "use": "feeds epsilon_Gamma_owner and EH/SGK q_loc residual",
            "claim_allowed": "false",
        },
        {
            "transfer_id": "AMP3245_2_if_noncoercive",
            "input": "m0<=0 or kernel source projection not zero",
            "formula": "amplitude law fails as a local-GR suppression proof; retain kernel/cross-block residual",
            "use": "rejects hidden scalar/local-force claim",
            "claim_allowed": "false",
        },
        {
            "transfer_id": "AMP3245_3_empirical_gate",
            "input": "m0, Jtot components, arena constants",
            "formula": "only compare to PPN/R10/clock/orbital once q_loc arena residual is numeric and no prior/source placeholder remains",
            "use": "keeps tests disciplined",
            "claim_allowed": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG3245_0_coercivity_theorem",
            "claim": "M_AB coercivity theorem shape is valid",
            "condition_passed": "true",
            "status": "Rayleigh/spectral certificate written",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3245_1_current_m0",
            "claim": "current MTS has parent-signed m0>0",
            "condition_passed": "false",
            "status": "M_AB spectrum, units, branch and kernel guard not sourced",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3245_2_first_component",
            "claim": "first Jtot component is source-backed numeric",
            "condition_passed": "false",
            "status": "Poynting component interface exists but flux constants/norms are missing",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3245_3_amplitude_score",
            "claim": "response amplitude can be scored",
            "condition_passed": "false",
            "status": "requires m0 and at least one numeric same-unit Jtot component",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3245_4_local_GR",
            "claim": "local GR/Newton/PPN reduction",
            "condition_passed": "false",
            "status": "amplitude/q_loc transfer not numeric",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3245_0_mab",
            "decision": "Use the Rayleigh/spectral certificate as the M_AB owner contract.",
            "because": "It is the exact bridge from response Hessian to a local amplitude bound.",
            "next_action": "Fill m0, kernel and unit rows before calling the response locally safe.",
        },
        {
            "decision_id": "DEC3245_1_component",
            "decision": "Promote Poynting/collar flux as the first concrete Jtot component interface.",
            "because": "3234 already derived its finite functional and it is physically relevant to EM stress coupling.",
            "next_action": "Acquire or derive C_flux, C_coll, flux norms, boundary frame and e_A normalization.",
        },
        {
            "decision_id": "DEC3245_2_no_claim",
            "decision": "Do not claim amplitude safety or local GR yet.",
            "because": "M_AB coercivity and the first component are not numeric/source-backed.",
            "next_action": "Build a fillable score-row template rather than another abstract theorem.",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3245_0_3246",
            "priority": "selected_primary",
            "next_doc": "3246-Y5-R2FR-first-Poynting-Jtot-score-row-or-boundary-frame-source-acquisition-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3246_first_Poynting_Jtot_score_row_or_boundary_frame_source_acquisition.py",
            "objective": "Try to fill the first concrete Jtot component row: boundary/collar label, u,n frame, C_flux/C_coll, EM stress flux norm, e_A normalization, units and source path; otherwise keep it as the first bounded but nonnumeric component.",
            "exclude": "do not claim Poynting zero from F^2=0; do not claim local GR; do not edit formalization-workbench",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(source_rows: list[dict[str, Any]], generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources_exist = all(row["exists"] == "true" for row in source_rows)
    sources_hit = all(row["evidence_hits"] not in {"MISSING_SOURCE", "NO_MATCH"} for row in source_rows)
    csvs_parse = all(csv_ok(path) for path in generated_csvs)
    outputs_under_post = all(ROOT in path.parents for path in generated_csvs) and ROOT in DOC.parents
    formalization_3245 = list(FW.rglob("*3245*")) if FW.exists() else []
    formalization_clean = len(formalization_3245) == 0
    conditional_not_claim = any(
        row["claim_gate_id"] == "CG3245_0_coercivity_theorem"
        and row["condition_passed"] == "true"
        and row["claim_allowed"] == "false"
        for row in gate_rows()
    )
    physics_blocked = all(
        row["claim_allowed"] == "false"
        for row in gate_rows()
        if row["claim_gate_id"] != "CG3245_0_coercivity_theorem"
    )
    component_nonclaim = all(row["valid_for_claim"] == "false" for row in first_component_rows())
    score_missing = any(row["current_status"] == "missing" for row in score_requirement_rows())
    next_written = bool(next_rows())

    checks = [
        ("VAL3245_0_sources_exist", sources_exist, "all cited source paths exist", str(sources_exist)),
        ("VAL3245_1_source_hits", sources_hit, "source evidence hits are present", str(sources_hit)),
        ("VAL3245_2_csvs_parse", csvs_parse, "all generated CSV files parse", str(csvs_parse)),
        ("VAL3245_3_outputs_under_post_checkpoint", outputs_under_post, "all outputs are under post-checkpoint-work", str(outputs_under_post)),
        ("VAL3245_4_formalization_clean", formalization_clean, "no 3245 outputs in formalization-workbench", f"formalization_3245_count={len(formalization_3245)}"),
        ("VAL3245_5_conditional_not_claim", conditional_not_claim, "coercivity theorem not promoted to current physics claim", str(conditional_not_claim)),
        ("VAL3245_6_physics_claims_blocked", physics_blocked, "m0/component/amplitude/local-GR claims remain blocked", str(physics_blocked)),
        ("VAL3245_7_component_nonclaim", component_nonclaim, "Poynting Jtot component remains nonclaim until numeric", str(component_nonclaim)),
        ("VAL3245_8_score_requirements_missing", score_missing, "score-row requirements expose missing fields", str(score_missing)),
        ("VAL3245_9_next_written", next_written, "3246 next target written", str(next_written)),
        ("VAL3245_10_doc_written", DOC.exists(), "3245 markdown checkpoint exists", str(DOC.exists())),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": bool_str(passed),
            "requirement": requirement,
            "evidence": evidence_text,
        }
        for validation_id, passed, requirement, evidence_text in checks
    ]
    rows.append(
        {
            "validation_id": "VAL3245_OVERALL",
            "passed": bool_str(all(row["passed"] == "true" for row in rows)),
            "requirement": "3245 validation overall",
            "evidence": "all required validation rows passed",
        }
    )
    return rows


def build_doc(
    source_rows: list[dict[str, Any]],
    coercivity: list[dict[str, Any]],
    schur: list[dict[str, Any]],
    jcomponent: list[dict[str, Any]],
    score_row: list[dict[str, Any]],
    amplitude: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 3245 - M_AB Coercivity and First Jtot Component Bound under AX1090",
            f"Generated: `{RUN_UTC}`",
            "Status: `Y5_R2FR_3245_MAB_Rayleigh_coercivity_certificate_written_first_Poynting_Jtot_component_interface_added_nonclaim`",
            "Claim ceiling: `coercivity_theorem_only_no_parent_m0_no_numeric_Jtot_component_no_amplitude_score_no_q_loc_zero_no_local_GR_no_Newton_no_PPN_claim`",
            "## Summary",
            "- `3245` turns `M_AB` into an exact spectral owner contract: `m0 := inf_{||Z||_Z=1}<Z,MZ>`, with gauge/kernel removal, common units, and same-domain locking.",
            "- The amplitude law is now mechanically usable if `m0>0`: `||Z_*|| <= m0^{-1}||J_tot||` and `|Delta Gamma_min| <= (2m0)^{-1}||J_tot||^2`.",
            "- Current MTS still cannot claim this because no parent-signed `M_AB` spectrum, units, kernel projection or branch norm exists.",
            "- The first concrete `J_tot` component interface is selected: the Poynting/collar boundary flux from `3234`, because it already has a finite bound functional and is directly tied to EM stress coupling.",
            "- Next work should try to fill that first row numerically/sourced: boundary/collar label, frame `u,n`, `C_flux/C_coll`, flux norms, `e_A` normalization, units and source path.",
            "## M_AB Coercivity Certificate Attempt",
            md_table(coercivity, ["cert_id", "object", "certificate", "derived_result", "current_status", "claim_allowed"]),
            "## Block Positivity and Schur Guard",
            md_table(schur, ["guard_id", "risk", "condition", "bound_or_test", "status", "valid_for_claim"]),
            "## First Jtot Component Bound Interface",
            md_table(jcomponent, ["component_id", "component", "source_basis", "bound", "units_requirement", "current_value", "status", "valid_for_claim"]),
            "## First Score Row Requirements",
            md_table(score_row, ["field", "required_for_first_score_row", "why", "current_status"]),
            "## Amplitude Scoring Transfer",
            md_table(amplitude, ["transfer_id", "input", "formula", "use", "claim_allowed"]),
            "## Claim Gates",
            md_table(gates, ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Next Target",
            md_table(next_target, ["next_id", "priority", "next_doc", "next_script", "objective", "exclude", "valid_for_claim"]),
            "## Source Register",
            md_table(source_rows, ["source_id", "source_path", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["validation_id", "passed", "requirement", "evidence"]),
            "## Generated Evidence",
            "\n".join(f"- `{path}`" for path in OUTPUTS.values()),
        ]
    )


def main() -> None:
    for path in OUTPUTS.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    DOC.parent.mkdir(parents=True, exist_ok=True)

    source_rows = source_register()
    coercivity = coercivity_rows()
    schur = schur_rows()
    jcomponent = first_component_rows()
    score_row = score_requirement_rows()
    amplitude = amplitude_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["coercivity"], coercivity)
    write_csv(OUTPUTS["schur"], schur)
    write_csv(OUTPUTS["jcomponent"], jcomponent)
    write_csv(OUTPUTS["score_row"], score_row)
    write_csv(OUTPUTS["amplitude"], amplitude)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    generated_csvs = [
        OUTPUTS["sources"],
        OUTPUTS["coercivity"],
        OUTPUTS["schur"],
        OUTPUTS["jcomponent"],
        OUTPUTS["score_row"],
        OUTPUTS["amplitude"],
        OUTPUTS["gates"],
        OUTPUTS["decision"],
        OUTPUTS["next"],
    ]
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, coercivity, schur, jcomponent, score_row, amplitude, gates, decisions, next_target, validation),
        encoding="utf-8",
    )
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, coercivity, schur, jcomponent, score_row, amplitude, gates, decisions, next_target, validation),
        encoding="utf-8",
    )

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    failed = [row for row in validation if row["passed"] != "true"]
    if failed:
        raise SystemExit(f"3245 validation failed: {failed}")


if __name__ == "__main__":
    main()

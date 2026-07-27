from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_FIRST_RESIDUAL_GATE_2607"
CHECKPOINT_ID = "2607"

DOC = ROOT / "2607-Y5-R2FR-source-support-or-boundary-no-flux-first-residual-zero-bound.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_FIRST_RESIDUAL_GATE_2607_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_FIRST_RESIDUAL_GATE_2607_LINEAGE_LEDGER.csv",
    "source_support": OUT / "P8_Y5_FIRST_RESIDUAL_GATE_2607_SOURCE_SUPPORT_AUDIT.csv",
    "boundary_noflux": OUT / "P8_Y5_FIRST_RESIDUAL_GATE_2607_BOUNDARY_NOFLUX_AUDIT.csv",
    "source_power": OUT / "P8_Y5_FIRST_RESIDUAL_GATE_2607_SOURCE_POWER_CONVENTION.csv",
    "two_slot_owner": OUT / "P8_Y5_FIRST_RESIDUAL_GATE_2607_TWO_SLOT_OWNER_PROOF_AUDIT.csv",
    "hidden_source": OUT / "P8_Y5_FIRST_RESIDUAL_GATE_2607_HIDDEN_SOURCE_LEDGER.csv",
    "zl_dl_contract": OUT / "P8_Y5_FIRST_RESIDUAL_GATE_2607_ZL_DL_CONTRACT.csv",
    "estar_acquisition": OUT / "P8_Y5_FIRST_RESIDUAL_GATE_2607_ESTAR_SOURCE_NORM_ACQUISITION.csv",
    "first_residual": OUT / "P8_Y5_FIRST_RESIDUAL_GATE_2607_FIRST_RESIDUAL_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_FIRST_RESIDUAL_GATE_2607_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_FIRST_RESIDUAL_GATE_2607_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_FIRST_RESIDUAL_GATE_2607_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_FIRST_RESIDUAL_GATE_2607_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2607_VALIDATION.csv",
}

COPY_TARGETS = {
    "source_support": LOCAL_BOUNDS / "First_residual_source_support_2607_NONCLAIM.csv",
    "hidden_source": LOCAL_BOUNDS / "Hidden_source_current_ledger_2607_NONCLAIM.csv",
    "first_residual": LOCAL_BOUNDS / "First_residual_status_2607_NONCLAIM.csv",
    "next_target": QUEUE / "JR2607_CENTERED_ORIGIN_NO_LINEAR_MARKER_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def false_flags() -> dict[str, bool]:
    return {
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "accepted_for_scoring": False,
    }


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2607_00_2606_handoff_doc",
            "source_path": ROOT / "2606-Y5-R2FR-parent-kinetic-coefficient-or-boundary-amplitude-theorem.md",
            "needles": ["NEXT2606_0_selected", "RV2606_10_verdict", "VAL2606_OVERALL"],
            "role": "current branch handoff selecting source-support or boundary no-flux first residual gate",
        },
        {
            "source_id": "SRC2607_01_2606_residual_vector",
            "source_path": OUT / "P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_FINITE_RESIDUAL_VECTOR.csv",
            "needles": ["RV2606_0_source_leak", "RV2606_3_boundary_flux", "RV2606_10_verdict"],
            "role": "current finite local residual vector requiring source and boundary closure before no-hair",
        },
        {
            "source_id": "SRC2607_02_1752_source_boundary_gate",
            "source_path": ROOT / "1752-Y5-R2FR-source-support-or-boundary-no-flux-first-residual-zero-bound.md",
            "needles": ["SSA1752_2_source_bound_law", "BNA1752_5_verdict", "VAL1752_OVERALL"],
            "role": "prior source-support/no-flux first residual zero-bound checkpoint",
        },
        {
            "source_id": "SRC2607_03_1753_power_convention",
            "source_path": ROOT / "1753-Y5-R2FR-source-support-parent-invariant-or-A-src-coefficient-row.md",
            "needles": ["PCA1753_0_definitions", "ASRC1753_3_weak_linear_silence", "VAL1753_OVERALL"],
            "role": "prior p_total=1+p_int bookkeeping repair and A_src threshold ledger",
        },
        {
            "source_id": "SRC2607_04_1754_ZL_DL_contract",
            "source_path": ROOT / "1754-Y5-R2FR-ZL-DL-parent-leakage-vector-or-A-src-norm-acquisition.md",
            "needles": ["ZLC1754_1_bounded_map", "SST1754_2_linear_silence_bound", "VAL1754_OVERALL"],
            "role": "prior Z_L/D_L leakage vector and far-local U_B^2 source theorem contract",
        },
        {
            "source_id": "SRC2607_05_1755_source_silent_attempt",
            "source_path": ROOT / "1755-Y5-R2FR-source-silent-fixed-point-theorem-or-E-star-source-norm-row.md",
            "needles": ["SSF1755_4_finite_bound_if_signed", "DEC1755_1_best_route", "VAL1755_OVERALL"],
            "role": "prior source-silent fixed point proof attempt and E* acquisition fallback",
        },
        {
            "source_id": "SRC2607_06_1756_hidden_source_ledger",
            "source_path": ROOT / "1756-Y5-R2FR-two-slot-source-free-owner-or-hidden-source-counterexample-ledger.md",
            "needles": ["HSC1756_9_verdict", "DEC1756_2_best_next", "VAL1756_OVERALL"],
            "role": "prior two-slot owner proof attempt naming hidden source counterexamples",
        },
        {
            "source_id": "SRC2607_07_1756_hidden_source_csv",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1756_HIDDEN_SOURCE_COUNTEREXAMPLE_LEDGER.csv",
            "needles": ["HSC1756_0_shifted_origin", "HSC1756_3_coupling_chain_source", "HSC1756_9_verdict"],
            "role": "machine-readable hidden source channels from the prior proof attempt",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        missing_needles = path_has_needles(spec["source_path"], spec["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": spec["source_id"],
                    "source_path": spec["source_path"],
                    "exists": spec["source_path"].exists(),
                    "missing_needles": missing_needles,
                    "source_pass": spec["source_path"].exists() and not missing_needles,
                    "role": spec["role"],
                    **false_flags(),
                }
            )
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "LIN2607_0_2606",
            "checkpoint": "2606",
            "question": "What residual must close first for the no-hair branch?",
            "result": "The local no-hair branch needs J_eff=0 and boundary_flux=0; R_source and R_boundary are the first live residuals.",
            "status": "CURRENT_HANDOFF_REBASED",
            "next_dependency": "source support or boundary no-flux first residual zero/bound",
        },
        {
            "step_id": "LIN2607_1_1752",
            "checkpoint": "1752",
            "question": "Can R_source or R_boundary be algebraically bounded?",
            "result": "Yes conditionally: R_source=U_B S_cg and finite source support gives a sharp bound; boundary no-flux is closure-only.",
            "status": "CONDITIONAL_BOUND_FORM_RETAINED",
            "next_dependency": "parent source support invariant or A_src norm",
        },
        {
            "step_id": "LIN2607_2_1753",
            "checkpoint": "1753",
            "question": "Was the source power counted correctly?",
            "result": "Yes after repair: p_total=1+p_int, so the explicit U_B in R_source=U_B S_cg cannot be double-counted.",
            "status": "BOOKKEEPING_REPAIRED_NONCLAIM",
            "next_dependency": "Z_L/D_L leakage vector and source norm",
        },
        {
            "step_id": "LIN2607_3_1754",
            "checkpoint": "1754",
            "question": "Can the internal source silence route give U_B^2?",
            "result": "Conditionally: if D_L<=C_H U_B and S_cg(D_L=0,Y)=0 with regular E* norms, then R_source is O(U_B^2) far-local.",
            "status": "THEOREM_CONTRACT_READY_INPUTS_MISSING",
            "next_dependency": "source-silent fixed point or E* norm",
        },
        {
            "step_id": "LIN2607_4_1755",
            "checkpoint": "1755",
            "question": "Can S_cg(D_L=0,Y)=0 be proved?",
            "result": "Only conditionally: two-slot source-free action would do it, but shifted origins, marker covectors, worldtube vertices, boundary and history tails remain legal.",
            "status": "SOURCE_SILENCE_NOT_PARENT_SIGNED",
            "next_dependency": "two-slot source-free owner or hidden source ledger",
        },
        {
            "step_id": "LIN2607_5_1756",
            "checkpoint": "1756",
            "question": "What blocks the two-slot source-free owner proof?",
            "result": "Hidden source currents are now named explicitly: shifted origin, marker, matter/worldtube, coupling chain, boundary, history, tower, even-source and kernel channels.",
            "status": "HIDDEN_SOURCE_LEDGER_IMPORTED",
            "next_dependency": "centered-origin/no-linear-marker proof or A_hidden bound",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def source_support_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SSA2607_0_residual_definition",
            "first residual source leak",
            "R_source=(1-Pi_B)S_cg=U_B S_cg",
            "EXACT_DEFINITION_REBASED_FROM_2606_AND_1752",
            "definition is safe; blocker is source-current ownership",
        ),
        (
            "SSA2607_1_support_power_convention",
            "source power convention",
            "if S_cg=U_B^p_int S_* then R_source=U_B^(1+p_int)S_* and p_total=1+p_int",
            "EXACT_BOOKKEEPING_IDENTITY",
            "prevents double-counting the external U_B switch",
        ),
        (
            "SSA2607_2_finite_source_bound",
            "finite source support bound",
            "if ||S_*||_{E*}<=A_src then ||R_source||_{E*}<=U_B^(1+p_int) A_src",
            "CONDITIONAL_BOUND_THEOREM",
            "MISSING_A_SRC_OR_A1_A2_ESTAR_NORM; MISSING_ARENA_PROJECTION",
        ),
        (
            "SSA2607_3_linear_silence_bound",
            "far-local U_B^2 source route",
            "if D_L<=C_H U_B, S_cg(0,Y)=0, ||S_1||_{E*}<=A_1 and ||S_2||_{E*}<=A_2, then ||R_source||<=C_H A_1 U_B^2 + C_H^2 A_2 U_B^3",
            "EXACT_CONDITIONAL_THEOREM_SHAPE",
            "MISSING_SOURCE_SILENT_FIXED_POINT; MISSING_C_H_A1_A2_ESTAR; TRANSITION_SHELL_NOT_CONTROLLED",
        ),
        (
            "SSA2607_4_exact_zero_test",
            "exact source zero",
            "R_source=0 requires U_B=0, S_cg=0 from parent kernel/two-slot proof, or exact local projector identity",
            "EXACT_ZERO_BLOCKED",
            "finite logistic screening is not exact zero and hidden sources remain legal",
        ),
        (
            "SSA2607_5_verdict",
            "source support verdict",
            "source route is the cleanest first-residual route, but it is a finite nonclaim residual until hidden source currents are killed or bounded",
            "SOURCE_ROUTE_SHARPENED_NOT_CLOSED",
            "MISSING_CENTERED_ORIGIN; MISSING_NO_LINEAR_MARKER; MISSING_MATTER_DESCENT; MISSING_COUPLING_DOUBLE_ZERO; MISSING_ESTAR_NORMS",
        ),
    ]
    return [
        with_stamp(
            {
                "audit_id": audit_id,
                "object": object_name,
                "formula_or_statement": statement,
                "current_status": status,
                "missing_to_promote": missing,
                **false_flags(),
            }
        )
        for audit_id, object_name, statement, status, missing in rows
    ]


def boundary_noflux_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BNA2607_0_nohair_identity",
            "coercive no-hair identity",
            "positive bulk norm plus J_eff=0 plus boundary_flux=0 forces delta_m=0 and grad delta_m=0",
            "EXACT_CONDITIONAL_THEOREM",
            "source zero and boundary zero are not parent-owned",
        ),
        (
            "BNA2607_1_boundary_zero_route",
            "boundary no-flux route",
            "R_boundary=0 if the parent boundary action fixes no normal flux/no growing branch before local readout",
            "CONDITIONAL_IDENTITY_ONLY",
            "MISSING_PARENT_BOUNDARY_ACTION; MISSING_FLUX_ZERO; MISSING_NO_GROWING_BRANCH_CLASS",
        ),
        (
            "BNA2607_2_boundary_finite_bound",
            "finite boundary response route",
            "if exact no-flux fails, boundary response must be carried as an explicit arena-projected residual coefficient",
            "FINITE_BOUND_INPUT_REQUIRED",
            "MISSING_BOUNDARY_RESPONSE_COEFFICIENT; MISSING_PROJECTION_NORMS; MISSING_SHELL_QUARANTINE",
        ),
        (
            "BNA2607_3_transition_shell_warning",
            "transition shell",
            "far-local U_B suppression cannot be applied inside a transition shell with U_B=O(1)",
            "SHELL_RESIDUAL_RETAINED",
            "MISSING_TRANSITION_SHELL_PROJECTOR_OR_EXACT_CANCELLATION",
        ),
        (
            "BNA2607_4_verdict",
            "boundary no-flux verdict",
            "boundary no-flux remains closure-only in the current corpus; it cannot be used to claim local GR",
            "BOUNDARY_ZERO_NOT_CLAIMED",
            "MISSING_PARENT_BOUNDARY_OWNER_OR_FINITE_BOUND_ROW",
        ),
    ]
    return [
        with_stamp(
            {
                "audit_id": audit_id,
                "object": object_name,
                "formula_or_statement": statement,
                "current_status": status,
                "missing_to_promote": missing,
                **false_flags(),
            }
        )
        for audit_id, object_name, statement, status, missing in rows
    ]


def source_power_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SPC2607_0_definition",
            "J_src=R_source=U_B S_cg; if S_cg=U_B^p_int S_* then R_source=U_B^p_total S_* with p_total=1+p_int",
            "EXACT_BOOKKEEPING_IDENTITY",
            "all 2607 source rows use p_total=1+p_int",
        ),
        (
            "SPC2607_1_bounded_Scg",
            "bounded S_cg means p_int=0 and p_total=1",
            "VALID_BUT_WEAK_ROUTE",
            "requires very small A_src and still needs E*/arena norms",
        ),
        (
            "SPC2607_2_linear_silence",
            "S_cg=D_L S_1+O(D_L^2) plus D_L<=C_H U_B gives p_int>=1 and p_total>=2",
            "BEST_DERIVABLE_ROUTE",
            "requires source-silent fixed point and regular source map",
        ),
        (
            "SPC2607_3_exact_zero",
            "R_source=0 is stronger than any power law and requires parent source-kernel silence",
            "ZERO_ROUTE_BLOCKED",
            "hidden source currents remain legal",
        ),
    ]
    return [
        with_stamp(
            {
                "convention_id": convention_id,
                "statement": statement,
                "status": status,
                "effect": effect,
                **false_flags(),
            }
        )
        for convention_id, statement, status, effect in rows
    ]


def two_slot_owner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "TSO2607_0_parent_quotient_map",
            "parent quotient map",
            "q(Phi) separates quotient/equivalence variables from vertical leakage variables X",
            "NEEDED_FOR_SOURCE_FREE_LOCAL_SECTOR",
            "MISSING_PARENT_QUOTIENT_MAP_SIGNATURE",
        ),
        (
            "TSO2607_1_two_slot_action",
            "two-slot action",
            "S_parent=S_core[q(Phi),Psi,theta]+S_X^kin[X]+f(chi_D)C_obs[X,q(Phi),Psi]+S_matter[q(Phi),Psi,theta]",
            "EXACT_CONDITIONAL_ANSATZ",
            "MISSING_PARENT_OWNERSHIP_OF_EACH_SLOT",
        ),
        (
            "TSO2607_2_variation_at_fixed_point",
            "variation at fixed point",
            "if X=0 is the homogeneous kinetic origin and hidden sources vanish, then delta_X S_parent|local=L_X X and S_cg(D_L=0,Y)=0",
            "EXACT_CONDITIONAL_VARIATION_ROUTE",
            "MISSING_ZERO_ORIGIN_AND_NO_HIDDEN_SOURCE_THEOREM",
        ),
        (
            "TSO2607_3_coupling_silence",
            "coupling silence",
            "coupling route needs f(0)=0 and f'(0)=0 or delta_X chi_D=0 at the fixed point",
            "DOUBLE_ZERO_REQUIRED",
            "MISSING_PARENT_COUPLING_DOUBLE_ZERO_OR_INDEPENDENCE_PROOF",
        ),
        (
            "TSO2607_4_boundary_history_silence",
            "boundary/history silence",
            "boundary and retained history terms must not leave affine local tails at D_L=0",
            "NEEDED_NOT_PARENT_SIGNED",
            "MISSING_BOUNDARY_NOFLUX_AND_HISTORY_TAIL_ZERO_CERTIFICATE",
        ),
        (
            "TSO2607_5_verdict",
            "two-slot owner proof",
            "the proof shape is viable but current parent action does not sign all source-free clauses",
            "PROOF_ATTEMPT_FAILS_CURRENT_PARENT_SIGNATURE",
            "go after centered origin and no-linear-marker first, then coupling/boundary/history",
        ),
    ]
    return [
        with_stamp(
            {
                "proof_id": proof_id,
                "clause": clause,
                "statement": statement,
                "current_status": status,
                "blocker": blocker,
                **false_flags(),
            }
        )
        for proof_id, clause, statement, status, blocker in rows
    ]


def hidden_source_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "HSC2607_0_shifted_origin",
            "shifted kinetic origin",
            "S_X=1/2 <X-X0(q),L_X(X-X0(q))>",
            "J_shift=-L_X X0(q) at X=0",
            "MISSING_CENTERED_ORIGIN_THEOREM",
            "A_shift=||L_X X0||_{E*}",
        ),
        (
            "HSC2607_1_linear_marker_covector",
            "linear material/domain/readout marker",
            "F_1(X)=ell_marker(X)",
            "J_marker=ell_marker in E*",
            "MISSING_NO_LINEAR_MARKER_COVECTOR_THEOREM",
            "A_marker=||ell_marker||_{E*}",
        ),
        (
            "HSC2607_2_matter_worldtube_vertex",
            "matter/worldtube X vertex",
            "S_matter includes V_m[X,rho_A,W_source] outside quotient q",
            "J_matter=delta_X V_m|_{X=0}",
            "MISSING_QUOTIENT_INVARIANT_MATTER_DESCENT_AND_MARKER_EXCLUSION",
            "A_matter per material/source class",
        ),
        (
            "HSC2607_3_coupling_chain_source",
            "observable coupling chain source",
            "delta_X[f(chi_D)C_obs]=f'(0)C_obs delta_X chi_D + f(0)delta_X C_obs",
            "J_chain=f'(0)C_obs partial_X chi_D unless double-zero or independence holds",
            "MISSING_COUPLING_DOUBLE_ZERO_OR_DELTA_X_CHI_D_ZERO",
            "A_chain",
        ),
        (
            "HSC2607_4_boundary_flux",
            "boundary/local projection flux",
            "boundary lift or Pi_local dB_X enters the X Euler-Lagrange equation",
            "J_boundary=Pi_local dB_X",
            "MISSING_BOUNDARY_PRIMITIVE_SILENCE_AND_PROJECTED_FLUX_ZERO",
            "A_boundary",
        ),
        (
            "HSC2607_5_history_tail",
            "retained memory/history tail",
            "nonlocal history term leaves affine local tail at D_L=0",
            "J_hist=delta_X S_hist|_{X=0}",
            "MISSING_HISTORY_TAIL_ZERO_THEOREM",
            "A_hist",
        ),
        (
            "HSC2607_6_integrated_out_tower",
            "integrated-out non-EH tower",
            "solving X with nonzero source produces <J,L^{-1}J> and local R10/R11 leakage",
            "J_tower maps into non-EH coefficients after reduction",
            "MISSING_NO_EXTRA_SCALAR_OR_NO_TOWER_CERTIFICATE",
            "K_R10/K_PPN/K_clock/K_orbital",
        ),
        (
            "HSC2607_7_even_source_normalization",
            "physical even measured-GM/source-normalization residual",
            "mu_extra_even or c_domain_source_normalization_operator survives X -> -X",
            "J_mu contributes to measured source normalization rather than auxiliary odd X",
            "MISSING_PHYSICAL_LOCK_TO_ZERO_EVEN_RESIDUAL",
            "A_mu_even",
        ),
        (
            "HSC2607_8_operator_kernel",
            "operator kernel/zero mode",
            "L_X has uncontrolled kernel or gauge mode with nonzero boundary/readout projection",
            "J_kernel is not erased by positivity on the orthogonal complement",
            "MISSING_KERNEL_PROJECTION_SILENCE",
            "A_kernel",
        ),
        (
            "HSC2607_9_verdict",
            "hidden source verdict",
            "J_hidden=sum(J_shift,J_marker,J_matter,J_chain,J_boundary,J_hist,J_tower,J_mu,J_kernel)",
            "current corpus cannot prove J_hidden=0",
            "HIDDEN_SOURCE_VECTOR_ACTIVE",
            "A_hidden envelope or clause-by-clause zero proof",
        ),
    ]
    return [
        with_stamp(
            {
                "counterexample_id": counterexample_id,
                "channel": channel,
                "allowed_term": allowed_term,
                "induced_source": induced_source,
                "missing_zero_proof": missing_zero_proof,
                "finite_bound_needed": finite_bound_needed,
                "current_status": "HIDDEN_SOURCE_VECTOR_ACTIVE" if counterexample_id == "HSC2607_9_verdict" else "COUNTEREXAMPLE_RETAINED",
                **false_flags(),
            }
        )
        for counterexample_id, channel, allowed_term, induced_source, missing_zero_proof, finite_bound_needed in rows
    ]


def zl_dl_contract_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ZLC2607_0_signed_coordinates",
            "z_L^A={z_theta,z_dotB,z_Bgrad_i,z_grad_i,z_shear_ij,z_rot_ij}",
            "candidate coordinate bundle for leakage distance D_L",
            "CANDIDATE_NOT_PARENT_SIGNED",
            "MISSING_PARENT_COARSE_GRAINING_MAP_AND_FRAME_REFERENCE",
        ),
        (
            "ZLC2607_1_bounded_map",
            "Z_L^A=U_B H_L^A(X_B), ||H_L||_G<=C_H",
            "if G_AB positive, D_L=sqrt(G_AB Z_L^A Z_L^B)<=C_H U_B",
            "EXACT_CONDITIONAL_DISTANCE_BOUND",
            "MISSING_G_AB_PARENT_METRIC; MISSING_H_L_BOUND; MISSING_C_H_VALUE",
        ),
        (
            "ZLC2607_2_gradient_bound",
            "nabla Z_L=(nabla U_B)H_L+U_B nabla H_L",
            "far-local gradient is O(U_B/L_B) if tail derivative and H_L log-gradient are bounded",
            "CONDITIONAL_FAR_LOCAL_GRADIENT_BOUND",
            "MISSING_L_B; MISSING_H_L_LOG_GRADIENT; TRANSITION_SHELL_NOT_SAFE",
        ),
        (
            "ZLC2607_3_source_silence_link",
            "D_L<=C_H U_B plus S_cg(0,Y)=0 converts source regularity into p_total>=2",
            "source suppression requires both distance bound and source-silent fixed point",
            "CONTRACT_BUILT_PARENT_SIGNATURE_MISSING",
            "MISSING_SOURCE_SILENT_FIXED_POINT",
        ),
        (
            "ZLC2607_4_verdict",
            "Z_L/D_L source route",
            "good route, not yet proof: it supplies the distance side but not hidden-source silence",
            "SOURCE_DISTANCE_CONTRACT_NONCLAIM",
            "MISSING_Z_L_PARENT_SIGNATURE_AND_HIDDEN_SOURCE_ZERO",
        ),
    ]
    return [
        with_stamp(
            {
                "contract_id": contract_id,
                "contract": contract,
                "derived_use": derived_use,
                "current_status": status,
                "blocker": blocker,
                **false_flags(),
            }
        )
        for contract_id, contract, derived_use, status, blocker in rows
    ]


def estar_acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ESN2607_0_E_space_owner",
            "E",
            "local energy space for the positive elliptic functional",
            "source-backed function space, boundary conditions, measure and operator domain",
            "MISSING_E_SPACE_OWNER",
        ),
        (
            "ESN2607_1_Estar_owner",
            "E*",
            "dual norm for S_cg and hidden source currents",
            "dual of E with units, projection map and arena restriction declared",
            "MISSING_ESTAR_NORM_OWNER",
        ),
        (
            "ESN2607_2_A1",
            "A_1=||partial_D S_cg(0,Y)||_{E*}",
            "linear source coefficient in S_cg=D_L S_1+O(D_L^2)",
            "finite numeric or theorem-bounded coefficient in same E* norm",
            "MISSING_A1_ESTAR_NORM",
        ),
        (
            "ESN2607_3_A2",
            "A_2=||S_2||_{E*}",
            "quadratic remainder coefficient in the source expansion",
            "finite numeric or theorem-bounded remainder over a declared D_L radius",
            "MISSING_A2_ESTAR_REMAINDER",
        ),
        (
            "ESN2607_4_CH",
            "C_H",
            "leakage-map bound in D_L<=C_H U_B",
            "source-backed bound with local-domain assumptions",
            "MISSING_H_BOUND",
        ),
        (
            "ESN2607_5_arena_projection",
            "P_arena",
            "projects E* source norm into R10/WEP/PPN/clock/orbital readouts",
            "operator norm and units for each arena with source paths",
            "MISSING_ARENA_PROJECTION_NORMS",
        ),
        (
            "ESN2607_6_shell_quarantine",
            "Q_trans/P_shell",
            "separates far-local U_B^2 theorem from transition shell U_B=O(1) domains",
            "parent projector or explicit finite shell residual row",
            "MISSING_TRANSITION_SHELL_PROJECTOR",
        ),
        (
            "ESN2607_7_Ahidden",
            "A_hidden",
            "finite envelope for J_hidden if zero proof fails",
            "sum or norm budget for A_shift,A_marker,A_matter,A_chain,A_boundary,A_hist,A_tower,A_mu,A_kernel",
            "MISSING_HIDDEN_SOURCE_ESTAR_ENVELOPE",
        ),
    ]
    return [
        with_stamp(
            {
                "row_id": row_id,
                "quantity": quantity,
                "role": role,
                "needed_input": needed_input,
                "current_status": status,
                **false_flags(),
            }
        )
        for row_id, quantity, role, needed_input, status in rows
    ]


def first_residual_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FRS2607_0_source_leak_definition",
            "R_source",
            "R_source=U_B S_cg",
            "source leakage row is defined exactly",
            "DEFINITION_READY_NONCLAIM",
            "PPN/R10/WEP/clocks/orbital",
        ),
        (
            "FRS2607_1_source_finite_bound",
            "R_source_bound",
            "||R_source||<=U_B^(1+p_int)A_src, or <=C_H A_1 U_B^2+C_H^2 A_2 U_B^3 under linear silence",
            "finite source bound is theorem-shaped but input-incomplete",
            "FINITE_BOUND_ACTIVE",
            "all_local",
        ),
        (
            "FRS2607_2_source_exact_zero",
            "R_source_zero",
            "R_source=0 only from exact U_B=0, source-kernel/two-slot silence, or local projector identity",
            "hidden source ledger blocks exact zero",
            "EXACT_ZERO_BLOCKED",
            "all_local",
        ),
        (
            "FRS2607_3_hidden_source_vector",
            "J_hidden",
            "J_hidden=sum(J_shift,J_marker,J_matter,J_chain,J_boundary,J_hist,J_tower,J_mu,J_kernel)",
            "named source-current vector replaces vague missing-source language",
            "HIDDEN_SOURCE_VECTOR_ACTIVE",
            "all_local",
        ),
        (
            "FRS2607_4_boundary_flux_zero",
            "R_boundary_zero",
            "R_boundary=0 if no-flux/no-growing boundary class is parent-owned",
            "boundary zero remains closure-only",
            "ZERO_BLOCKED",
            "PPN/local",
        ),
        (
            "FRS2607_5_boundary_finite_bound",
            "R_boundary_bound",
            "boundary response coefficient must be finite and arena-projected if exact no-flux fails",
            "finite response row required",
            "FINITE_BOUND_INPUT_REQUIRED",
            "PPN/local/orbital",
        ),
        (
            "FRS2607_6_shell_quarantine",
            "R_shell",
            "transition shell cannot inherit far-local U_B^2 suppression unless parent-projected or explicitly quarantined",
            "shell remains active sibling residual",
            "SHELL_RESIDUAL_ACTIVE",
            "PPN/R10",
        ),
        (
            "FRS2607_7_verdict",
            "first residual gate",
            "source route is narrowed to hidden-source zero proof or A_hidden/E* finite envelope; boundary route remains secondary closure-only",
            "first residual is no longer vague but it is still active",
            "FIRST_RESIDUAL_ACTIVE_BUT_NOW_NAMED",
            "all_local",
        ),
    ]
    return [
        with_stamp(
            {
                "residual_id": residual_id,
                "quantity": quantity,
                "formula_or_description": formula_or_description,
                "result": result,
                "current_status": status,
                "arena_links": arena_links,
                **false_flags(),
            }
        )
        for residual_id, quantity, formula_or_description, result, status, arena_links in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2607_0_source_zero", "R_source=0 is parent-proved", "BLOCKED_HIDDEN_SOURCE_VECTOR_ACTIVE"),
        ("CG2607_1_source_finite_score", "finite R_source can be scored against local arenas", "BLOCKED_ESTAR_AHIDDEN_ARENA_PROJECTIONS_MISSING"),
        ("CG2607_2_boundary_zero", "R_boundary=0 is parent-proved", "BLOCKED_PARENT_NOFLUX_BOUNDARY_UNSIGNED"),
        ("CG2607_3_shell_safe", "transition shell is projected/quarantined", "BLOCKED_TRANSITION_SHELL_PROJECTOR_MISSING"),
        ("CG2607_4_nohair_branch", "J_eff=0 and boundary_flux=0 local no-hair branch can be used", "BLOCKED_FIRST_RESIDUALS_ACTIVE"),
        ("CG2607_5_local_GR_Newton", "local GR/Newton/PPN/R10/WEP branch can claim", "BLOCKED_NO_LOCAL_REENTRY"),
    ]
    return [
        with_stamp(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_pass": False,
                "status": "BLOCKED_NO_CLAIM",
                "blocker": blocker,
                **false_flags(),
            }
        )
        for gate_id, claim, blocker in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2607_0_source_status",
            "decision": "keep source route as primary",
            "reason": "R_source has the cleanest algebra: exact definition, repaired power convention, and a path to U_B^2 if hidden sources vanish",
            "effect": "attack hidden source currents rather than inventing a plateau axiom",
        },
        {
            "decision_id": "DEC2607_1_zero_status",
            "decision": "do not claim exact source zero",
            "reason": "two-slot source-free proof is conditional and hidden source channels remain legal in the current corpus",
            "effect": "source residual remains active and nonclaim",
        },
        {
            "decision_id": "DEC2607_2_boundary_status",
            "decision": "keep boundary no-flux as secondary",
            "reason": "boundary no-flux can close the no-hair identity only after parent boundary ownership; otherwise it is closure-only",
            "effect": "no local-GR claim may use boundary silence as a hand-set condition",
        },
        {
            "decision_id": "DEC2607_3_best_next",
            "decision": "select centered-origin/no-linear-marker proof or A_hidden bound",
            "reason": "shifted origin and marker covector are the lowest-level hidden sources; killing them attacks F_1 directly with less scrutiny than fitting coefficients",
            "effect": "2608 should target X0(q)=0 and ell_marker=0 before coupling-chain/boundary/history cleanup",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2607_0_selected",
            "selection_status": "selected",
            "target_file": "2608-Y5-R2FR-centered-origin-no-linear-marker-symmetry-proof-or-Ahidden-bound.md",
            "target_script": "scripts/Y5_R2FR_centered_origin_no_linear_marker_symmetry_proof_or_Ahidden_bound_2608.py",
            "task": "try to prove X0(q)=0 and ell_marker=0 from parent symmetry/invariance; otherwise create A_shift and A_marker finite E* residual rows",
            "success_condition": "shifted-origin and linear-marker hidden source rows become parent-zero or finite source-backed nonclaim rows",
            "fallback_condition": "if these clauses fail, move to coupling-chain double-zero or A_chain bound",
            "guardrails": "no plateau axiom; no hidden boundary tuning; no local-GR claim; no GitHub; no formalization-workbench edits",
        },
        {
            "route_id": "NEXT2607_1_coupling_fallback",
            "selection_status": "held_fallback",
            "target_file": "2608b-Y5-R2FR-coupling-chain-source-double-zero-proof-or-Achain-bound.md",
            "target_script": "scripts/Y5_R2FR_coupling_chain_source_double_zero_proof_or_Achain_bound_2608b.py",
            "task": "try to derive f(0)=f'(0)=0 or delta_X chi_D=0 at the local fixed point; otherwise carry A_chain",
            "success_condition": "coupling-chain hidden source is zero by parent structure or finite bounded in E*",
            "fallback_condition": "source E*/arena projection ledger if no hidden-source zero proof closes",
            "guardrails": "do not tune f to pass a local test after the fact",
        },
        {
            "route_id": "NEXT2607_2_finite_fallback",
            "selection_status": "held_fallback",
            "target_file": "2608c-Y5-R2FR-E-star-hidden-source-envelope-and-arena-projection-ledger.md",
            "target_script": "scripts/Y5_R2FR_Estar_hidden_source_envelope_and_arena_projection_ledger_2608c.py",
            "task": "source E/E*/A_hidden and arena projection rows if zero proof does not close",
            "success_condition": "finite hidden-source envelope exists without claim-grade promotion",
            "fallback_condition": "local branch remains closure-only",
            "guardrails": "finite residual scoring only after units, norms and source paths are real",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, target in COPY_TARGETS.items():
        source = OUTPUTS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2607_{key}",
                    "source_path": source,
                    "target_path": target,
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                    **false_flags(),
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(data: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_true_fields = {"valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "valid_prediction_row"}
    for rows in data.values():
        for row in rows:
            for field in forbidden_true_fields:
                if row.get(field) is True:
                    return False
    return True


def missing_rows_not_ready(data: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in data.values():
        for row in rows:
            joined = " ".join(row_value(value) for value in row.values())
            if "MISSING" in joined:
                if row.get("score_ready") is True or row.get("claim_allowed") is True or row.get("valid_prediction_row") is True:
                    return False
    return True


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(with_stamp({"check_id": check_id, "status": "PASS" if condition else "FAIL", "notes": notes, "detail": detail, "valid_for_claim": False}))

    add("VAL2607_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited source paths exist and needles are present")
    add("VAL2607_01_lineage_complete", {"2606", "1752", "1753", "1754", "1755", "1756"}.issubset({row["checkpoint"] for row in data["lineage"]}), "lineage covers current handoff plus prior source route")
    add("VAL2607_02_source_definition", any(row["audit_id"] == "SSA2607_0_residual_definition" for row in data["source_support"]), "R_source definition is recorded")
    add("VAL2607_03_power_convention", any(row["convention_id"] == "SPC2607_0_definition" and "p_total=1+p_int" in row["statement"] for row in data["source_power"]), "source power convention is repaired")
    add("VAL2607_04_finite_bound_present", any(row["audit_id"] == "SSA2607_3_linear_silence_bound" for row in data["source_support"]), "far-local U_B^2 finite bound is retained")
    add("VAL2607_05_exact_zero_blocked", any(row["audit_id"] == "SSA2607_4_exact_zero_test" and row["current_status"] == "EXACT_ZERO_BLOCKED" for row in data["source_support"]), "exact source zero remains blocked")
    add("VAL2607_06_boundary_blocked", any(row["audit_id"] == "BNA2607_4_verdict" and row["current_status"] == "BOUNDARY_ZERO_NOT_CLAIMED" for row in data["boundary_noflux"]), "boundary no-flux remains unclaimed")
    add("VAL2607_07_two_slot_not_promoted", any(row["proof_id"] == "TSO2607_5_verdict" and row["current_status"] == "PROOF_ATTEMPT_FAILS_CURRENT_PARENT_SIGNATURE" for row in data["two_slot_owner"]), "two-slot owner proof is not promoted")
    add("VAL2607_08_hidden_sources_named", any(row["counterexample_id"] == "HSC2607_9_verdict" and row["current_status"] == "HIDDEN_SOURCE_VECTOR_ACTIVE" for row in data["hidden_source"]), "hidden source vector is explicit and active")
    add("VAL2607_09_zl_contract_nonclaim", any(row["contract_id"] == "ZLC2607_4_verdict" and row["current_status"] == "SOURCE_DISTANCE_CONTRACT_NONCLAIM" for row in data["zl_dl_contract"]), "Z_L/D_L contract remains nonclaim")
    add("VAL2607_10_estar_rows_nonclaim", all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["estar_acquisition"]), "E*/A_hidden acquisition rows remain nonclaim")
    add("VAL2607_11_first_residual_active", any(row["residual_id"] == "FRS2607_7_verdict" and row["current_status"] == "FIRST_RESIDUAL_ACTIVE_BUT_NOW_NAMED" for row in data["first_residual"]), "first residual is active but sharply named")
    add("VAL2607_12_claim_gates_safe", all(row["claim_allowed"] is False and row["gate_pass"] is False for row in data["claim_gates"]), "all claim gates remain blocked")
    add("VAL2607_13_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row promotes scoring or claim flags")
    add("VAL2607_14_missing_not_ready", missing_rows_not_ready(data), "no MISSING_* row is marked ready")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*FIRST_RESIDUAL_GATE_2607*", "2607-Y5-R2FR-source-support-or-boundary-no-flux-first-residual-zero-bound.md", "*JR2607_CENTERED_ORIGIN_NO_LINEAR_MARKER_NEXT*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2607_15_no_formalization_artifacts", not formalization_artifacts, "no 2607 first-residual artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))
    add("VAL2607_16_decision_next", any(row["decision_id"] == "DEC2607_3_best_next" for row in data["decisions"]), "decision selects centered-origin/no-linear-marker route")
    add("VAL2607_17_next_selected", any(row["route_id"] == "NEXT2607_0_selected" and row["selection_status"] == "selected" for row in data["next"]), "next target selected")
    add("VAL2607_18_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")
    add("VAL2607_19_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2607_CSV_{path.stem}", parsed, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2607_COPY_CSV_{key}", parsed, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(with_stamp({"check_id": "VAL2607_OVERALL", "status": "PASS" if overall else "FAIL", "notes": "2607 first residual source-support/no-flux gate rebases source route and names hidden source current vector", "detail": "", "valid_for_claim": False}))
    return rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(row_value(row.get(field, "")).replace("|", "/") for field in fields) + " |")
    return "\n".join([header, divider, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2607: R2FR Source Support Or Boundary No-Flux First Residual Zero/Bound",
        "",
        "**Status:** private nonclaim current-branch rebase. This checkpoint does not claim local GR, Newton, PPN, R10, WEP, clocks, or orbital closure.",
        "",
        "**Main result:** the source route is the best route, but it is not closed. The exact first source residual is `R_source=U_B S_cg`; with the repaired convention, if `S_cg=U_B^p_int S_*`, then `R_source=U_B^(1+p_int)S_*`. The strongest derivable far-local branch is conditional: `D_L<=C_H U_B`, source silence `S_cg(D_L=0,Y)=0`, and finite `E*` norms give `||R_source||<=C_H A_1 U_B^2+C_H^2 A_2 U_B^3`. The attempted exact-zero proof fails in the current parent signature because hidden source currents remain legal. Boundary no-flux also remains closure-only. Therefore the next honest target is not more hand-waving about a plateau; it is a centered-origin/no-linear-marker proof or finite `A_hidden` source rows.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Lineage Ledger",
        markdown_table(data["lineage"], ["step_id", "checkpoint", "question", "result", "status", "next_dependency", "valid_for_claim", "claim_allowed"]),
        "",
        "## Source Support Audit",
        markdown_table(data["source_support"], ["audit_id", "object", "formula_or_statement", "current_status", "missing_to_promote", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Boundary No-Flux Audit",
        markdown_table(data["boundary_noflux"], ["audit_id", "object", "formula_or_statement", "current_status", "missing_to_promote", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Source Power Convention",
        markdown_table(data["source_power"], ["convention_id", "statement", "status", "effect", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Two-Slot Owner Proof Audit",
        markdown_table(data["two_slot_owner"], ["proof_id", "clause", "statement", "current_status", "blocker", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Hidden Source Ledger",
        markdown_table(data["hidden_source"], ["counterexample_id", "channel", "allowed_term", "induced_source", "missing_zero_proof", "finite_bound_needed", "current_status", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## ZL/DL Contract",
        markdown_table(data["zl_dl_contract"], ["contract_id", "contract", "derived_use", "current_status", "blocker", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## E* Source Norm Acquisition",
        markdown_table(data["estar_acquisition"], ["row_id", "quantity", "role", "needed_input", "current_status", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## First Residual Status",
        markdown_table(data["first_residual"], ["residual_id", "quantity", "formula_or_description", "result", "current_status", "arena_links", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_pass", "status", "blocker", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
        "## Private Verdict",
        "",
        "This is progress, but not the kind that lets us brag yet. The fog has cleared around the local-GR bridge: the first source residual is not a mystery blob anymore; it is a hidden-current vector. If `X0(q)=0` and `ell_marker=0` can be derived, the local branch gets materially stronger. If they cannot, we stop pretending and carry `A_shift` and `A_marker` as finite residuals. Either way, this is the right pressure point.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def build_data() -> dict[str, list[dict[str, Any]]]:
    data = {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "source_support": source_support_rows(),
        "boundary_noflux": boundary_noflux_rows(),
        "source_power": source_power_rows(),
        "two_slot_owner": two_slot_owner_rows(),
        "hidden_source": hidden_source_rows(),
        "zl_dl_contract": zl_dl_contract_rows(),
        "estar_acquisition": estar_acquisition_rows(),
        "first_residual": first_residual_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    return data


def main() -> None:
    data = build_data()

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["lineage_ledger"], data["lineage"])
    write_csv(OUTPUTS["source_support"], data["source_support"])
    write_csv(OUTPUTS["boundary_noflux"], data["boundary_noflux"])
    write_csv(OUTPUTS["source_power"], data["source_power"])
    write_csv(OUTPUTS["two_slot_owner"], data["two_slot_owner"])
    write_csv(OUTPUTS["hidden_source"], data["hidden_source"])
    write_csv(OUTPUTS["zl_dl_contract"], data["zl_dl_contract"])
    write_csv(OUTPUTS["estar_acquisition"], data["estar_acquisition"])
    write_csv(OUTPUTS["first_residual"], data["first_residual"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2607_OVERALL")
    print(f"wrote {DOC}")
    print(f"validation={OUTPUTS['validation']}")
    print(f"overall={overall['status']}")


if __name__ == "__main__":
    main()

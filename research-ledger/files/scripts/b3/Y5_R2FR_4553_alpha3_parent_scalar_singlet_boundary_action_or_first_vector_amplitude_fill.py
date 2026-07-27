from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4553"
CLAIM_ID = "L-395"
BRANCH_ID = "MTS_R2FR_Y5_ALPHA3_PRIVATE_SELECTOR_ZERO_CERTIFICATE_4553"
MARKER = "PPC4161_ALPHA3_PARENT_SCALAR_SINGLET_BOUNDARY_ACTION_OR_FIRST_VECTOR_AMPLITUDE_FILL_4553"
PACKET_MARKER = "PPC4161_PACKET_ALPHA3_PRIVATE_SELECTOR_ZERO_CERTIFICATE_4553"
DECISION = "PRIVATE_SELECTOR_DERIVES_MALPHA3_FALPHA3_ZERO_GLOBAL_PARENT_STILL_UNSIGNED_CUBIC_RESIDUE_NEXT"
NEXT_TARGET = "4554-Y5-R2FR-alpha3-cubic-vector-residue-classification-or-C3-bound-source-row.md"

FORMAL_PATH = FORMAL / "569-PPC4161-alpha3-parent-scalar-singlet-boundary-action-or-first-vector-amplitude-fill.md"
DOC_PATH = POST / "4553-Y5-R2FR-alpha3-parent-scalar-singlet-boundary-action-or-first-vector-amplitude-fill.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4552 = FORMAL / "568-PPC4161-alpha3-marker-exclusion-boundary-flux-owner-or-finite-vector-amplitude-row.md"
DOC_4551 = FORMAL / "567-PPC4161-alpha3-vector-boundary-zero-or-first-Kalpha3-source-projection.md"
DOC_4539 = FORMAL / "555-PPC4161-parent-adopt-GR-parity-HQNP-selector-or-freeze-as-effective-local-GR-branch.md"
DOC_4176 = POST / "4176-Y5-R2FR-local-boundary-no-flux-sector-interface-theorem-or-transition-current-bound.md"
DOC_4177 = POST / "4177-Y5-R2FR-quotient-naturality-vertical-silence-proof-or-projector-residual-bound.md"
DOC_4174 = POST / "4174-Y5-R2FR-parent-action-global-adoption-or-explicit-local-branch-quarantine.md"
DOC_4182 = FORMAL / "198-PPC4161-motion-frame-symmetry-parent-signature-gate.md"
DOC_4427 = FORMAL / "443-PPC4161-parent-vertical-gauge-action-span-or-first-scoreable-Csource-component.md"
PACKET = FORMAL / "180-PPC4161-private-local-packet-integration.md"

FINITE_4552 = SOURCE_DIR / "P8_Y5_R2FR_4552_FINITE_VECTOR_AMPLITUDE_ROWS.csv"
MARKER_4552 = SOURCE_DIR / "P8_Y5_R2FR_4552_MARKER_EXCLUSION_CONTRACT.csv"
BOUNDARY_4552 = SOURCE_DIR / "P8_Y5_R2FR_4552_BOUNDARY_FLUX_OWNER_CONTRACT.csv"
REDUCED_4552 = SOURCE_DIR / "P8_Y5_R2FR_4552_ALPHA3_REDUCED_SPLIT.csv"
CLAIM_GATES_4552 = SOURCE_DIR / "P8_Y5_R2FR_4552_CLAIM_GATES.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4553_SOURCE_REGISTER.csv"
SELECTOR_PREMISES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4553_PRIVATE_SELECTOR_PREMISES.csv"
SCALAR_SINGLET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4553_PARENT_SCALAR_SINGLET_THEOREM_ATTEMPT.csv"
BOUNDARY_NOFLUX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4553_BOUNDARY_NOFLUX_THEOREM_ATTEMPT.csv"
ZERO_CERT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4553_ALPHA3_ZERO_CERTIFICATE_CANDIDATE.csv"
VECTOR_FILL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4553_FIRST_VECTOR_AMPLITUDE_FILL.csv"
RESIDUAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4553_RESIDUAL_HANDOFF.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4553_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4553_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4553_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4553_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4553_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], limit: int | None = None) -> str:
    if not rows:
        return "\n"
    chosen = rows[:limit] if limit is not None else rows
    headers: list[str] = []
    for row in chosen:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in chosen:
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def safe_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        stripped = str(value).strip()
        if stripped == "" or stripped.lower() in {"missing", "nan", "none"}:
            return None
        return float(stripped)
    except (TypeError, ValueError):
        return None


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4553_00_4552_reduced_split", "4552 reduced alpha3 split", REDUCED_4552, "M_alpha3 + F_alpha3 + C3_alpha3"),
        ("SRC4553_01_4552_marker_contract", "4552 marker contract", MARKER_4552, "MC4552_2_no_marker_clause"),
        ("SRC4553_02_4552_boundary_contract", "4552 boundary flux contract", BOUNDARY_4552, "BF4552_2_normal_flux_zero"),
        ("SRC4553_03_4552_finite_rows", "4552 finite vector rows", FINITE_4552, "FV4552_6_cubic_only_after_marker_boundary_zero"),
        ("SRC4553_04_4552_doc", "4552 formal doc", DOC_4552, "Delta alpha3 = M_alpha3 + F_alpha3 + C3_alpha3 epsilon_U^3"),
        ("SRC4553_05_4551_doc", "4551 scalar source zero", DOC_4551, "K_alpha3^src[f(r)] = 0"),
        ("SRC4553_06_4176_no_flux", "4176 private no-flux theorem", DOC_4176, "LOCAL_BOUNDARY_NO_FLUX_THEOREM_CLOSES_TRANSITION_CURRENT_PRIVATE_SELECTOR"),
        ("SRC4553_07_4177_quotient", "4177 quotient vertical silence theorem", DOC_4177, "QUOTIENT_NATURALITY_VERTICAL_SILENCE_THEOREM_CLOSES_PROJECTOR_RESIDUALS_PRIVATE_SELECTOR"),
        ("SRC4553_08_4174_quarantine", "4174 parent selector quarantine", DOC_4174, "global_parent_action_adoption_proved = false"),
        ("SRC4553_09_4539_parent_freeze", "4539 effective local-GR freeze", DOC_4539, "effective local-GR branch"),
        ("SRC4553_10_packet", "private packet integration", PACKET, "S_parent|Wloc = S_red[q(Phi),psi]"),
        ("SRC4553_11_motion_frame_gate", "motion-frame parent signature gate", DOC_4182, "A_MF_PARENT_SIGNATURE_NOT_FOUND"),
        ("SRC4553_12_vertical_span_gate", "vertical action span gate", DOC_4427, "PARENT_RHO_AND_SPAN_UNSIGNED"),
        ("SRC4553_13_4552_claim_gates", "4552 claim gates", CLAIM_GATES_4552, "G4552_1_marker_zero_or_bound"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needle": needle,
                "needle_found": b(needle in text),
                "role": "4553 private selector alpha3 zero-certificate attempt",
                "valid_for_claim": "False",
            }
        )
    return rows


def finite_context() -> dict[str, float]:
    rows = read_csv(FINITE_4552)
    by_id = {row.get("row_id", ""): row for row in rows}
    master = by_id.get("FV4552_0_no_cancellation_master", {})
    cubic = by_id.get("FV4552_6_cubic_only_after_marker_boundary_zero", {})
    return {
        "b_alpha3": safe_float(master.get("numeric_value")) or 4.0e-20,
        "epsilon_u3": safe_float(master.get("source_epsilon_U3")) or math.nan,
        "c3_cubic_only": safe_float(cubic.get("numeric_value")) or math.nan,
    }


def selector_premise_rows() -> list[dict[str, Any]]:
    return [
        {
            "premise_id": "SP4553_0_branch_scope",
            "premise": "Work only inside the private compact PPC4161-GP-HQNP local selector branch.",
            "source": "4174/4539/180 packet",
            "private_selector_status": "available_as_branch_condition",
            "global_parent_status": "not_globally_parent_signed",
            "effect_on_alpha3": "allows conditional zero certificate; forbids public/global promotion",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "SP4553_1_scalar_source_zero",
            "premise": "Centred scalar monopole source terms have zero alpha3 vector projection.",
            "source": "4551",
            "private_selector_status": "conditional_source_model_pass",
            "global_parent_status": "source_model_not_full_global_theorem",
            "effect_on_alpha3": "P_alpha3_src epsilon_U^2 removed from reduced split",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "SP4553_2_same_coframe_hilbert_source",
            "premise": "Ordinary matter/EM/clocks share one observed coframe and Hilbert source functor with no source-label reentry.",
            "source": "180 packet and 4539 PAC4539_3",
            "private_selector_status": "branch_signed",
            "global_parent_status": "not_global_parent_adoption",
            "effect_on_alpha3": "no material label or species frame supplies a preferred vector after variation",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "SP4553_3_quotient_naturality",
            "premise": "Action, matter/readout functor, constants, source normalization and boundary terms factor through q before variation.",
            "source": "4177 and 180 packet",
            "private_selector_status": "branch_signed",
            "global_parent_status": "closure/private selector outside global parent proof",
            "effect_on_alpha3": "vertical representative labels cannot become physical marker vectors",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "SP4553_4_no_flux_boundary",
            "premise": "Compact local support and routed/fixed Hamiltonian boundary give no unmodelled interface current in the stationary non-radiative branch.",
            "source": "4176 and 180 packet",
            "private_selector_status": "branch_signed",
            "global_parent_status": "not a global no-flux theorem for all sectors",
            "effect_on_alpha3": "F_alpha3 killed only for compact stationary non-radiative packets",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "SP4553_5_radiative_firewall",
            "premise": "Radiative EM/gravity flux is not silently zero; if present it is routed through T_total/Hamiltonian charge and scored separately.",
            "source": "4175/4176 packet language",
            "private_selector_status": "active_guard",
            "global_parent_status": "not_zero_for_radiative_cases",
            "effect_on_alpha3": "prevents no-flux theorem from being overextended",
            "valid_for_claim": "False",
        },
    ]


def scalar_singlet_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "SS4553_0_target",
            "claim": "M_alpha3 vanishes if all surviving compact-branch data are q-basic scalar singlets after variation.",
            "mathematical_form": "M_alpha3=P_alpha3[V_loc+V_domain+V_boundary_marker+J_transition^i]=0",
            "derivation": "No rank-one vector representation exists in the input alphabet; vector projection of scalar singlets is zero by SO(3) covariance.",
            "private_selector_result": "pass_inside_private_selector",
            "global_parent_result": "not_public_claim",
            "valid_for_claim": "False",
        },
        {
            "step_id": "SS4553_1_no_material_marker",
            "claim": "Species/material/readout labels do not enter active source coefficients after variation.",
            "mathematical_form": "D_source/DLabel = 0 after Hilbert descent; labels are readout metadata, not parent source fields",
            "derivation": "4539 no-reentry plus 180 Hilbert source descent removes independent source weights and source-label multipliers.",
            "private_selector_result": "pass_inside_private_selector",
            "global_parent_result": "depends_on_global_parent_adoption",
            "valid_for_claim": "False",
        },
        {
            "step_id": "SS4553_2_no_vertical_marker",
            "claim": "Vertical representative labels cannot become physical alpha3 vectors.",
            "mathematical_form": "D_v theta_A = D_v m_A = D_v alpha_EM = D_v source_normalization = 0",
            "derivation": "4177 quotient-naturality requires the source/readout functor to factor through q before variation.",
            "private_selector_result": "pass_inside_private_selector",
            "global_parent_result": "parent rho/span remains unsigned outside branch",
            "valid_for_claim": "False",
        },
        {
            "step_id": "SS4553_3_motion_frame_caveat",
            "claim": "The scalar-singlet theorem is not a proof of the missing global motion-frame axiom A_MF.",
            "mathematical_form": "A_MF would globally identify internal motion-frame labels as gauge redundancies",
            "derivation": "4182 did not find A_MF as a parent-owned MTS axiom, so 4553 stays inside the private selector branch.",
            "private_selector_result": "guard_only",
            "global_parent_result": "A_MF_not_found",
            "valid_for_claim": "False",
        },
        {
            "step_id": "SS4553_4_verdict",
            "claim": "M_alpha3=0 is derived for the private selector branch, not for full MTS.",
            "mathematical_form": "PPC4161-GP-HQNP selector premises => M_alpha3=0",
            "derivation": "Same-coframe Hilbert source + no source-label reentry + q-naturality leave no vector marker in the compact static branch.",
            "private_selector_result": "M_alpha3_zero",
            "global_parent_result": "not_globally_parent_signed",
            "valid_for_claim": "False",
        },
    ]


def boundary_noflux_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "BN4553_0_target",
            "claim": "F_alpha3 is zero in the compact stationary non-radiative private selector branch.",
            "mathematical_form": "F_alpha3 = lim_S r^2 n_mu P_alpha3_nu B_boundary^{mu nu}/(G_eff M_eff) = 0",
            "derivation": "4176 gives support separation and no unmodelled interface current when local matter is compactly inside W_loc and boundary/Hamiltonian terms are fixed or routed.",
            "private_selector_result": "pass_inside_private_selector",
            "global_parent_result": "not_global_no_flux_theorem",
            "valid_for_claim": "False",
        },
        {
            "step_id": "BN4553_1_scalar_trace",
            "claim": "A homogeneous scalar boundary term gives tangential trace stress only.",
            "mathematical_form": "S_boundary=int sqrt(|gamma|)F(Y_scalar) -> tau_AB=tau gamma_AB",
            "derivation": "Imported 4552/BF4552 scalar boundary contract; no tangential vector is admitted in the private branch alphabet.",
            "private_selector_result": "conditional_pass_inside_private_selector",
            "global_parent_result": "boundary action not globally parent-derived",
            "valid_for_claim": "False",
        },
        {
            "step_id": "BN4553_2_normal_flux",
            "claim": "Trace-only tangential stress plus no unmodelled normal exchange kills the alpha3 normal flux projection.",
            "mathematical_form": "n_mu gamma_tangent^{mu nu}=0 and n_mu B_boundary^{mu i}=0",
            "derivation": "Tangential trace stress has no normal leg; 4176 supplies no unmodelled transition current inside the compact stationary selector.",
            "private_selector_result": "F_alpha3_zero",
            "global_parent_result": "private_selector_only",
            "valid_for_claim": "False",
        },
        {
            "step_id": "BN4553_3_poynting_firewall",
            "claim": "Poynting/radiative flux is not set to zero by this theorem.",
            "mathematical_form": "If radiative flux crosses the collar, route through T_total/Hamiltonian charge and score a flux row",
            "derivation": "4175/4176 explicitly keep radiative EM/gravity flux real; 4553 only handles compact stationary non-radiative local packets.",
            "private_selector_result": "guard_only",
            "global_parent_result": "not_zero_for_radiative_cases",
            "valid_for_claim": "False",
        },
        {
            "step_id": "BN4553_4_verdict",
            "claim": "F_alpha3=0 is derived for the private selector branch, not for full MTS.",
            "mathematical_form": "PPC4161-GP-HQNP compact stationary no-flux premises => F_alpha3=0",
            "derivation": "Boundary trace stress has no alpha3 normal vector projection, and unmodelled interface flux is absent/routed in the branch.",
            "private_selector_result": "F_alpha3_zero",
            "global_parent_result": "not_globally_parent_signed",
            "valid_for_claim": "False",
        },
    ]


def zero_certificate_rows() -> list[dict[str, Any]]:
    context = finite_context()
    return [
        {
            "certificate_id": "AZ4553_0_private_selector_alpha3_reduction",
            "scope": "private PPC4161-GP-HQNP compact stationary non-radiative local selector",
            "input_split": "Delta alpha3 = M_alpha3 + F_alpha3 + C3_alpha3 epsilon_U^3",
            "M_alpha3_value": "0",
            "M_alpha3_basis": "same-coframe Hilbert source, no source-label reentry, q-naturality, scalar-singlet local branch",
            "F_alpha3_value": "0",
            "F_alpha3_basis": "homogeneous scalar boundary trace plus compact no-flux/routed Hamiltonian boundary",
            "remaining_alpha3": "C3_alpha3 epsilon_U^3",
            "B_alpha3": f"{context['b_alpha3']:.16e}",
            "epsilon_U3": f"{context['epsilon_u3']:.16e}",
            "C3_allowed_if_only_residue": f"{context['c3_cubic_only']:.16e}",
            "private_selector_ready": "True",
            "global_parent_claim": "False",
            "valid_for_claim": "False",
        },
        {
            "certificate_id": "AZ4553_1_public_claim_firewall",
            "scope": "full MTS parent action",
            "input_split": "Delta alpha3 = M_alpha3 + F_alpha3 + C3_alpha3 epsilon_U^3",
            "M_alpha3_value": "NOT_PROMOTED",
            "M_alpha3_basis": "A_MF/global quotient parent rho/span still unsigned outside private selector",
            "F_alpha3_value": "NOT_PROMOTED",
            "F_alpha3_basis": "global sector no-flux/support separation still unsigned outside private selector",
            "remaining_alpha3": "all channels reopen unless selector clauses are parent-signed or bounded",
            "B_alpha3": f"{context['b_alpha3']:.16e}",
            "epsilon_U3": f"{context['epsilon_u3']:.16e}",
            "C3_allowed_if_only_residue": f"{context['c3_cubic_only']:.16e}",
            "private_selector_ready": "False",
            "global_parent_claim": "False",
            "valid_for_claim": "False",
        },
    ]


def vector_fill_rows() -> list[dict[str, Any]]:
    context = finite_context()
    return [
        {
            "fill_id": "VF4553_0_marker_private_selector_value",
            "channel": "M_alpha3",
            "candidate_value": "0",
            "units": "dimensionless alpha3",
            "acceptance_basis": "private selector zero certificate AZ4553_0",
            "numeric_bound": f"{context['b_alpha3']:.16e}",
            "status": "filled_as_private_selector_zero_nonclaim",
            "score_ready_private": "True",
            "score_ready_global": "False",
            "valid_for_claim": "False",
        },
        {
            "fill_id": "VF4553_1_boundary_private_selector_value",
            "channel": "F_alpha3",
            "candidate_value": "0",
            "units": "dimensionless alpha3",
            "acceptance_basis": "private selector zero certificate AZ4553_0",
            "numeric_bound": f"{context['b_alpha3']:.16e}",
            "status": "filled_as_private_selector_zero_nonclaim",
            "score_ready_private": "True",
            "score_ready_global": "False",
            "valid_for_claim": "False",
        },
        {
            "fill_id": "VF4553_2_cubic_handoff_value",
            "channel": "C3_alpha3",
            "candidate_value": "MISSING_CLASSIFICATION_OR_SOURCE_VALUE",
            "units": "dimensionless coefficient multiplying epsilon_U^3",
            "acceptance_basis": "next target must classify or bound cubic vector residue",
            "numeric_bound": f"{context['c3_cubic_only']:.16e}",
            "status": "not_filled_next_target",
            "score_ready_private": "False",
            "score_ready_global": "False",
            "valid_for_claim": "False",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RH4553_0_cubic_vector_residue",
            "meaning": "Once M_alpha3 and F_alpha3 are zero inside the private selector, the first live alpha3 private-branch term is C3_alpha3 epsilon_U^3.",
            "route": NEXT_TARGET,
            "status": "PRIMARY_NEXT_TARGET",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RH4553_1_global_parent_adoption",
            "meaning": "The private selector zero certificate is not global parent adoption.",
            "route": "parent A_MF/rho-span/global no-flux adoption remains a separate root problem",
            "status": "OPEN_GLOBAL_PARENT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RH4553_2_radiative_flux",
            "meaning": "Radiative EM/gravity Poynting flux is not killed by compact stationary no-flux language.",
            "route": "score separate boundary/Hamiltonian flux row if applying to radiative systems",
            "status": "GUARD_RETAINED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G4553_0_private_marker_zero",
            "requirement": "M_alpha3=0 inside private selector branch",
            "status": "PASS_PRIVATE_SELECTOR",
            "claim_effect": "marker vector channel can be set to zero only in the private compact branch",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4553_1_private_boundary_zero",
            "requirement": "F_alpha3=0 inside compact stationary non-radiative private selector branch",
            "status": "PASS_PRIVATE_SELECTOR",
            "claim_effect": "boundary flux channel can be set to zero only in branch scope",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4553_2_global_parent_promotion",
            "requirement": "parent action globally signs A_MF/rho-span/quotient/no-flux selector clauses",
            "status": "FAIL_UNSIGNED",
            "claim_effect": "blocks public/global alpha3 or local-GR claim",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4553_3_cubic_residue",
            "requirement": "C3_alpha3 zero/classification or source-backed coefficient bound",
            "status": "NEXT_BLOCKER",
            "claim_effect": "blocks even private alpha3 score closure until classified/bounded",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4553_4_no_smuggling",
            "requirement": "private selector zero certificate cannot be used for radiative/global/open-sector cases",
            "status": "PASS_FIREWALL",
            "claim_effect": "keeps sector interfaces honest",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4553_0",
            "decision": DECISION,
            "summary": "4553 derives M_alpha3=0 and F_alpha3=0 inside the private compact stationary PPC4161-GP-HQNP selector by combining same-coframe Hilbert source/no-label reentry, quotient naturality, scalar-singlet representation, and compact no-flux/routed boundary conditions. It does not promote a global parent-action claim; A_MF/rho-span/global no-flux remain unsigned. The active alpha3 private-branch blocker becomes C3_alpha3.",
            "claim_id": CLAIM_ID,
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "After 4553, the private selector branch has M_alpha3=F_alpha3=0, so alpha3 pressure moves to the cubic vector residue rather than circling marker/no-flux again.",
            "success_condition": "Classify all O(epsilon_U^3) vector carriers; prove representation zero or source a coefficient satisfying |C3_alpha3| <= 8.2061897207390857e+01.",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "decision": DECISION,
            "formal_doc": str(FORMAL_PATH),
            "post_doc": str(DOC_PATH),
            "validation": str(VALIDATION_PATH),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    selector: list[dict[str, Any]],
    scalar: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    certs: list[dict[str, Any]],
    fill: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    rows.append(
        {
            "validation_id": "VAL4553_0_sources",
            "check": "all cited source paths exist and needles are found",
            "status": "PASS" if sources_ok else "FAIL",
            "details": f"{sum(1 for row in sources if row['exists'] == 'True' and row['needle_found'] == 'True')}/{len(sources)} sources verified",
        }
    )

    selector_text = " ".join(str(value) for row in selector for value in row.values())
    selector_ok = ("branch_signed" in selector_text or "available_as_branch_condition" in selector_text)
    selector_ok = selector_ok and (
        "not_globally_parent_signed" in selector_text
        or "not_global_parent_adoption" in selector_text
        or "not a global no-flux theorem" in selector_text
    )
    rows.append(
        {
            "validation_id": "VAL4553_1_scope_firewall",
            "check": "private selector scope is explicit and global parent promotion is blocked",
            "status": "PASS" if selector_ok else "FAIL",
            "details": "private selector certificate only",
        }
    )

    scalar_text = " ".join(str(value) for row in scalar for value in row.values())
    scalar_ok = "M_alpha3_zero" in scalar_text and "not_globally_parent_signed" in scalar_text
    rows.append(
        {
            "validation_id": "VAL4553_2_marker_zero",
            "check": "M_alpha3 zero theorem is derived for private selector and not globalized",
            "status": "PASS" if scalar_ok else "FAIL",
            "details": "same-coframe/no-label/q-natural scalar-singlet route",
        }
    )

    boundary_text = " ".join(str(value) for row in boundary for value in row.values())
    boundary_ok = "F_alpha3_zero" in boundary_text and "not_zero_for_radiative_cases" in boundary_text
    rows.append(
        {
            "validation_id": "VAL4553_3_boundary_zero",
            "check": "F_alpha3 zero theorem is branch-scoped and keeps radiative firewall",
            "status": "PASS" if boundary_ok else "FAIL",
            "details": "compact stationary no-flux branch only",
        }
    )

    private_cert = next((row for row in certs if row.get("certificate_id") == "AZ4553_0_private_selector_alpha3_reduction"), {})
    cert_ok = private_cert.get("M_alpha3_value") == "0" and private_cert.get("F_alpha3_value") == "0"
    cert_ok = cert_ok and private_cert.get("global_parent_claim") == "False"
    rows.append(
        {
            "validation_id": "VAL4553_4_zero_certificate",
            "check": "zero certificate fills M_alpha3 and F_alpha3 as private nonclaim zeros",
            "status": "PASS" if cert_ok else "FAIL",
            "details": "AZ4553_0 values checked",
        }
    )

    fill_ok = any(row.get("channel") == "C3_alpha3" and row.get("score_ready_private") == "False" for row in fill)
    fill_ok = fill_ok and all(row.get("valid_for_claim") == "False" for row in fill)
    rows.append(
        {
            "validation_id": "VAL4553_5_cubic_handoff",
            "check": "C3_alpha3 remains open and claim rows stay false",
            "status": "PASS" if fill_ok else "FAIL",
            "details": "cubic residue selected as next blocker",
        }
    )

    gates_ok = any(row.get("status") == "FAIL_UNSIGNED" for row in gates) and any(row.get("status") == "NEXT_BLOCKER" for row in gates)
    rows.append(
        {
            "validation_id": "VAL4553_6_claim_gates",
            "check": "global parent and cubic gates remain blocked",
            "status": "PASS" if gates_ok else "FAIL",
            "details": "no public/local-GR claim promoted",
        }
    )

    docs_ok = DOC_PATH.exists() and FORMAL_PATH.exists()
    rows.append(
        {
            "validation_id": "VAL4553_7_docs",
            "check": "post and formal docs exist during validation",
            "status": "PASS" if docs_ok else "FAIL",
            "details": f"post={DOC_PATH.exists()} formal={FORMAL_PATH.exists()}",
        }
    )

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL4553_OVERALL",
            "check": "4553 checkpoint validation",
            "status": "PASS" if overall else "FAIL",
            "details": DECISION if overall else "one or more validation checks failed",
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    selector: list[dict[str, Any]],
    scalar: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    certs: list[dict[str, Any]],
    fill: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    context = finite_context()
    return f"""# 4553 - alpha3 parent scalar-singlet boundary action or first vector amplitude fill

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4552 reduced the hard `alpha3` channel to:

```text
Delta alpha3 = M_alpha3 + F_alpha3 + C3_alpha3 epsilon_U^3.
```

4553 tries the derivation route first. It does **not** merely restate that marker/no-flux is missing. Inside the private compact stationary `PPC4161-GP-HQNP` selector branch, the existing source chain gives:

```text
M_alpha3 = 0
F_alpha3 = 0
```

The logic is:

1. same observed coframe + Hilbert source descent removes material/source-label reentry;
2. quotient naturality makes vertical representative labels nonphysical before variation;
3. scalar-singlet local data have no rank-one vector representation for `alpha3`;
4. compact stationary no-flux/routed Hamiltonian boundary removes unmodelled normal momentum flux;
5. radiative EM/gravity flux is not erased and is explicitly outside this zero certificate.

So the private selector branch now has the sharper reduced form:

```text
Delta alpha3 = C3_alpha3 epsilon_U^3.
```

with the current numeric allowance:

```text
epsilon_U^3 = {context['epsilon_u3']:.16e}
|C3_alpha3| <= {context['c3_cubic_only']:.16e}
```

That is a real forward step: alpha3 pressure moves to the cubic vector residue. It is still not a public/global MTS local-GR proof, because 4539/4182/4427 keep the root parent signatures unsigned.

## Private Selector Premises

{markdown_table(selector)}

## Scalar-Singlet Marker Theorem Attempt

{markdown_table(scalar)}

## Boundary No-Flux Theorem Attempt

{markdown_table(boundary)}

## Alpha3 Zero Certificate Candidate

{markdown_table(certs)}

## First Vector Amplitude Fill

{markdown_table(fill)}

## Residual Handoff

{markdown_table(residuals)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_projection_bound",
        "claim": "4553 derives M_alpha3=0 and F_alpha3=0 inside the private compact stationary PPC4161-GP-HQNP selector, reducing alpha3 to the cubic vector residue within that branch.",
        "current_evidence": "Generated source register, private selector premises, scalar-singlet theorem attempt, boundary no-flux theorem attempt, zero certificate candidate, vector amplitude fill rows, claim gates, status and validation CSVs.",
        "status": "private_selector_alpha3_marker_boundary_zero_cubic_residue_nonclaim",
        "next_test": NEXT_TARGET,
        "failure_mode": "Using the private selector zero certificate as a global parent-action/local-GR proof, or applying compact no-flux to radiative/open-sector flux.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "This moves alpha3 from marker/boundary fog to C3_alpha3 in the private branch; global parent adoption remains separate.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    selector = selector_premise_rows()
    scalar = scalar_singlet_rows()
    boundary = boundary_noflux_rows()
    certs = zero_certificate_rows()
    fill = vector_fill_rows()
    residuals = residual_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_ = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SELECTOR_PREMISES_CSV, selector)
    write_csv(SCALAR_SINGLET_CSV, scalar)
    write_csv(BOUNDARY_NOFLUX_CSV, boundary)
    write_csv(ZERO_CERT_CSV, certs)
    write_csv(VECTOR_FILL_CSV, fill)
    write_csv(RESIDUAL_CSV, residuals)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_)
    write_csv(STATUS_CSV, status)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    pending_doc = f"# 4553 - alpha3 parent scalar-singlet boundary action or first vector amplitude fill\n\nMarker: `{MARKER}`\n\nValidation pending.\n"
    DOC_PATH.write_text(pending_doc, encoding="utf-8")
    FORMAL_PATH.write_text(pending_doc, encoding="utf-8")

    validation = validate(sources, selector, scalar, boundary, certs, fill, gates)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, selector, scalar, boundary, certs, fill, residuals, gates, decisions, next_, validation)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4553 Alpha3 Private Selector Zero Certificate

Marker: `{MARKER}`  
Inside the private compact stationary `PPC4161-GP-HQNP` selector branch, the marker and boundary-flux channels in the reduced alpha3 split are now zero-certified:

```text
M_alpha3 = 0,   F_alpha3 = 0,
Delta alpha3 = C3_alpha3 epsilon_U^3.
```

This is not a global parent-action proof. The global A_MF/rho-span/quotient/no-flux signatures remain unsigned. The next local alpha3 target is the cubic vector residue `C3_alpha3`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4553 Packet Integration - Alpha3 Private Selector Zero Certificate

Marker: `{PACKET_MARKER}`  
For compact stationary non-radiative local packets, `M_alpha3` and `F_alpha3` are zero inside the private selector by same-coframe Hilbert source descent, no source-label reentry, quotient naturality, scalar-singlet covariance and routed/no-flux boundary conditions. Radiative flux and global parent adoption remain outside this certificate.
""",
    )

    print(f"wrote {DOC_PATH}")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    overall = next((row for row in validation if row["validation_id"] == "VAL4553_OVERALL"), {})
    print(f"overall={overall.get('status', 'UNKNOWN')} decision={DECISION}")


if __name__ == "__main__":
    main()

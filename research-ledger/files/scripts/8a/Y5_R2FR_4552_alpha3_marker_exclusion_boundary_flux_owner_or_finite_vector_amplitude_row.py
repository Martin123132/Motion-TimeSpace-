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

CHECKPOINT = "4552"
CLAIM_ID = "L-394"
BRANCH_ID = "MTS_R2FR_Y5_ALPHA3_MARKER_BOUNDARY_FLUX_4552"
MARKER = "PPC4161_ALPHA3_MARKER_EXCLUSION_BOUNDARY_FLUX_OWNER_OR_FINITE_VECTOR_AMPLITUDE_ROW_4552"
PACKET_MARKER = "PPC4161_PACKET_ALPHA3_MARKER_EXCLUSION_BOUNDARY_FLUX_OWNER_OR_FINITE_VECTOR_AMPLITUDE_ROW_4552"
DECISION = "ALPHA3_REDUCED_TO_MARKER_AND_BOUNDARY_FLUX_ZERO_OR_FINITE_AMPLITUDE_ROWS_NONCLAIM"
NEXT_TARGET = "4553-Y5-R2FR-alpha3-parent-scalar-singlet-boundary-action-or-first-vector-amplitude-fill.md"

FORMAL_PATH = FORMAL / "568-PPC4161-alpha3-marker-exclusion-boundary-flux-owner-or-finite-vector-amplitude-row.md"
DOC_PATH = POST / "4552-Y5-R2FR-alpha3-marker-exclusion-boundary-flux-owner-or-finite-vector-amplitude-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4551 = FORMAL / "567-PPC4161-alpha3-vector-boundary-zero-or-first-Kalpha3-source-projection.md"
DOC_4545 = FORMAL / "561-PPC4161-attractor-stationarity-and-boundary-silence-from-Bianchi-Hamiltonian-local-conservation.md"
PACKET = FORMAL / "180-PPC4161-private-local-packet-integration.md"
PRODUCTS_4550 = SOURCE_DIR / "P8_Y5_R2FR_4550_OBSERVABLE_PRODUCT_BOUNDS.csv"
DOMAIN_4549 = SOURCE_DIR / "P8_Y5_R2FR_4549_LOCAL_DOMAIN_BMIN_ROWS.csv"
KPROJ_4551 = SOURCE_DIR / "P8_Y5_R2FR_4551_KALPHA3_SOURCE_PROJECTION_ROWS.csv"
BOUNDARY_ZERO_4551 = SOURCE_DIR / "P8_Y5_R2FR_4551_BOUNDARY_VECTOR_ZERO_THEOREM.csv"
BLOCKERS_4551 = SOURCE_DIR / "P8_Y5_R2FR_4551_REMAINING_BLOCKERS.csv"
BOUNDARY_OWNER = SOURCE_DIR / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv"
BOUNDARY_REPAIR = SOURCE_DIR / "P8_BOUNDARY_SCALAR_PREMISE_REPAIR_LEDGER.csv"
BOUNDARY_ALPHA3_ATTEMPT = SOURCE_DIR / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv"
ALPHA3_TEMPLATE = SOURCE_DIR / "P8_ALPHA3_NUMERIC_PRODUCT_INPUT_TEMPLATE.csv"
ALPHA3_ZERO_GATE = SOURCE_DIR / "P8_ALPHA3_THEOREM_ZERO_GATE.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4552_SOURCE_REGISTER.csv"
REDUCED_SPLIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4552_ALPHA3_REDUCED_SPLIT.csv"
MARKER_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4552_MARKER_EXCLUSION_CONTRACT.csv"
BOUNDARY_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4552_BOUNDARY_FLUX_OWNER_CONTRACT.csv"
FINITE_VECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4552_FINITE_VECTOR_AMPLITUDE_ROWS.csv"
SURVIVAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4552_SURVIVAL_DECISION_MATRIX.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4552_REMAINING_BLOCKERS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4552_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4552_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4552_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4552_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4552_VALIDATION.csv"


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
    if limit is not None and len(rows) > limit:
        remaining = len(rows) - limit
        filler = " |" * max(len(headers) - 2, 0)
        lines.append(f"| ... | {remaining} additional rows in CSV |{filler}")
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
        {
            "source_id": "SRC4552_00_4551_remaining_blockers",
            "label": "4551 active alpha3 blocker ledger",
            "path": BLOCKERS_4551,
            "needle": "BLOCK4551_0_marker_exclusion",
        },
        {
            "source_id": "SRC4552_01_4551_kprojection",
            "label": "4551 Kalpha3 residual rows",
            "path": KPROJ_4551,
            "needle": "K4551_2_marker_vector_residual",
        },
        {
            "source_id": "SRC4552_02_4551_boundary_zero",
            "label": "4551 boundary vector zero theorem",
            "path": BOUNDARY_ZERO_4551,
            "needle": "BZ4551_2_no_flux",
        },
        {
            "source_id": "SRC4552_03_boundary_owner",
            "label": "boundary scalar action owner audit",
            "path": BOUNDARY_OWNER,
            "needle": "O7_parent_owner_verdict",
        },
        {
            "source_id": "SRC4552_04_boundary_repair",
            "label": "boundary scalar premise repair ledger",
            "path": BOUNDARY_REPAIR,
            "needle": "R1_no_marker_exclusion",
        },
        {
            "source_id": "SRC4552_05_boundary_alpha3_attempt",
            "label": "boundary alpha3 no-flux theorem attempt",
            "path": BOUNDARY_ALPHA3_ATTEMPT,
            "needle": "T5_parent_owner_audit",
        },
        {
            "source_id": "SRC4552_06_alpha3_template",
            "label": "alpha3 numeric product fallback template",
            "path": ALPHA3_TEMPLATE,
            "needle": "A3_BOUNDARY_NUMERIC_OR_ZERO",
        },
        {
            "source_id": "SRC4552_07_alpha3_zero_gate",
            "label": "alpha3 theorem zero gate",
            "path": ALPHA3_ZERO_GATE,
            "needle": "TG_boundary_zero",
        },
        {
            "source_id": "SRC4552_08_private_packet_poynting_boundary",
            "label": "packet Poynting/boundary routing",
            "path": PACKET,
            "needle": "Nonzero radiative EM boundary flux is routed",
        },
        {
            "source_id": "SRC4552_09_4545_counterexample_guard",
            "label": "4545 Ward/Hamiltonian no-smuggling guard",
            "path": DOC_4545,
            "needle": "Ward/Bianchi conservation cannot be used as a no-vector/no-flux theorem",
        },
        {
            "source_id": "SRC4552_10_4551_formal_doc",
            "label": "4551 scalar source projection doc",
            "path": DOC_4551,
            "needle": "K_alpha3^src[f(r)] = 0",
        },
        {
            "source_id": "SRC4552_11_4550_product_bound",
            "label": "4550 alpha3 numeric product bound",
            "path": PRODUCTS_4550,
            "needle": "PB4550_alpha3",
        },
        {
            "source_id": "SRC4552_12_4549_domain_epsilon",
            "label": "4549 selected local epsilon domain",
            "path": DOMAIN_4549,
            "needle": "D4549_0_inner_solar_1_to_30_AU",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        path = spec["path"]
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "source_id": spec["source_id"],
                "label": spec["label"],
                "source_path": str(path),
                "exists": b(path.exists()),
                "needle": spec["needle"],
                "needle_found": b(spec["needle"] in text),
                "used_for": "alpha3 marker/boundary flux split and finite fallback rows",
                "valid_for_claim": "False",
            }
        )
    return rows


def alpha3_product_row() -> dict[str, str]:
    rows = read_csv(PRODUCTS_4550)
    for row in rows:
        if row.get("observable") == "alpha3" or row.get("product_id") == "PB4550_alpha3":
            return row
    return {}


def selected_domain_row() -> dict[str, str]:
    rows = read_csv(DOMAIN_4549)
    for row in rows:
        if row.get("domain_id") == "D4549_0_inner_solar_1_to_30_AU":
            return row
    return rows[0] if rows else {}


def numeric_context() -> dict[str, float]:
    alpha3 = alpha3_product_row()
    domain = selected_domain_row()
    bound = safe_float(alpha3.get("bound")) or 4.0e-20
    epsilon_u = safe_float(domain.get("epsilon_U_domain")) or math.nan
    epsilon_u2 = safe_float(domain.get("epsilon_U_squared")) or math.nan
    epsilon_u3 = epsilon_u * epsilon_u2
    return {
        "bound": bound,
        "half_bound": bound / 2.0,
        "third_bound": bound / 3.0,
        "epsilon_u": epsilon_u,
        "epsilon_u2": epsilon_u2,
        "epsilon_u3": epsilon_u3,
        "cubic_only_c3": bound / epsilon_u3 if epsilon_u3 and epsilon_u3 > 0 else math.nan,
        "cubic_equal_third_c3": (bound / 3.0) / epsilon_u3 if epsilon_u3 and epsilon_u3 > 0 else math.nan,
    }


def reduced_split_rows() -> list[dict[str, Any]]:
    context = numeric_context()
    return [
        {
            "law_id": "RS4552_0_imported_4551_source_zero",
            "object": "scalar source projection",
            "law": "K_alpha3^src[f(r)] = 0 for centred stationary SO(3) scalar monopole f(r)",
            "derivation": "4551 representation/parity projection: alpha3 is vector/preferred-frame; scalar shells integrate to zero vector.",
            "result": "P_alpha3_src epsilon_U^2 -> 0 on the selected scalar point-mass source-model branch",
            "status": "imported_conditional_source_projection_zero",
            "valid_for_claim": "False",
        },
        {
            "law_id": "RS4552_1_reduced_alpha3_split",
            "object": "Delta alpha3",
            "law": "Delta alpha3 = M_alpha3 + F_alpha3 + C3_alpha3 epsilon_U^3",
            "derivation": "After the scalar source channel is projected out, any surviving vector/preferred-frame signal must be a marker/domain vector M_alpha3, a boundary normal-momentum flux F_alpha3, or higher-order vector residue.",
            "result": "alpha3 problem is reduced to two zero-or-bound channels plus cubic residue",
            "status": "derived_reduction_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "law_id": "RS4552_2_marker_channel_definition",
            "object": "M_alpha3",
            "law": "M_alpha3 = P_alpha3[spin/velocity/off-centre/domain-vector/anisotropic-transition-current/preferred-frame marker]",
            "derivation": "Those objects carry the missing rank-one vector representation which scalar monopoles do not carry.",
            "result": "M_alpha3=0 only if parent dynamics admits no such local/domain/boundary marker in the private compact branch",
            "status": "exact_channel_definition",
            "valid_for_claim": "False",
        },
        {
            "law_id": "RS4552_3_boundary_flux_definition",
            "object": "F_alpha3",
            "law": "F_alpha3 = lim_S r^2 n_mu P_alpha3_nu B_boundary^{mu nu}/(G_eff M_eff)",
            "derivation": "Boundary alpha3 is a preferred-momentum flux projection; Ward ownership does not imply amplitude absence.",
            "result": "F_alpha3=0 only if the parent boundary variation has scalar trace stress and zero normal momentum flux",
            "status": "exact_channel_definition",
            "valid_for_claim": "False",
        },
        {
            "law_id": "RS4552_4_no_cancellation_budget",
            "object": "alpha3 observable bound",
            "law": "|M_alpha3| + |F_alpha3| + |C3_alpha3| epsilon_U^3 <= B_alpha3",
            "derivation": "Use no-cancellation sufficient condition; do not hide one channel behind another.",
            "result": f"B_alpha3={context['bound']:.16e}; epsilon_U^3={context['epsilon_u3']:.16e}",
            "status": "finite_bound_ready_nonclaim",
            "valid_for_claim": "False",
        },
    ]


def marker_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "MC4552_0_target",
            "claim": "M_alpha3 is the only remaining non-boundary vector/preferred-frame source after scalar source projection zero.",
            "mathematical_form": "M_alpha3 = P_alpha3[V_loc + V_domain + V_boundary_marker + J_transition^i]",
            "passes_if": "the channel is explicitly represented and no scalar term is counted twice",
            "current_owner": "definition_from_4551_projection_rows",
            "status": "definition_pass",
            "fallback_if_missing": "none",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "MC4552_1_scalar_singlet_zero",
            "claim": "q-basic scalar singlet data cannot produce M_alpha3.",
            "mathematical_form": "If all local/domain/boundary data transform as SO(3) scalar singlets, P_alpha3[scalar]=0.",
            "passes_if": "parent action and quotient map only admit scalar singlet local data in the compact static branch",
            "current_owner": "mathematical_representation_lemma_only",
            "status": "conditional_math_pass",
            "fallback_if_missing": "retain M_alpha3 finite amplitude row",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "MC4552_2_no_marker_clause",
            "claim": "No material marker, spin axis, orbital velocity label, domain drift vector, off-centre source vector, or anisotropic projector leaks into the local readout.",
            "mathematical_form": "V_marker=V_spin=V_velocity=V_domain=V_offcentre=V_transition=0",
            "passes_if": "parent quotient/current map kills every rank-one vector representation before the PPN readout",
            "current_owner": "not_parent_signed",
            "status": "open_owner_gap",
            "fallback_if_missing": "|M_alpha3| <= B_alpha3 or assigned sub-budget",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "MC4552_3_countermodel_guard",
            "claim": "Any surviving vector marker can source alpha3 even while Ward/Bianchi conservation is formally satisfied.",
            "mathematical_form": "P_alpha3[V_i f(r)] proportional V_i integral f(r)dOmega need not vanish",
            "passes_if": "used as a firewall against smuggling marker absence from conservation",
            "current_owner": "4545/4551 guard",
            "status": "active_guard",
            "fallback_if_missing": "alpha3 local branch overclaims",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "MC4552_4_contract_verdict",
            "claim": "Current corpus parent-derives M_alpha3=0.",
            "mathematical_form": "parent_action -> scalar_singlet_local_branch -> M_alpha3=0",
            "passes_if": "MC4552_1 and MC4552_2 are parent-owned, not merely asserted",
            "current_owner": "fail",
            "status": "zero_not_promoted_keep_finite_row",
            "fallback_if_missing": "source or derive a numeric bound on M_alpha3",
            "valid_for_claim": "False",
        },
    ]


def boundary_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "BF4552_0_target",
            "claim": "F_alpha3 is the boundary normal-momentum flux projection that survives scalar source zero.",
            "mathematical_form": "F_alpha3 = lim_S r^2 n_mu P_alpha3_nu B_boundary^{mu nu}/(G_eff M_eff)",
            "passes_if": "boundary alpha3 is treated as a flux amplitude, not a symbolic epsilon name",
            "current_owner": "definition_from_boundary_alpha3_attempt",
            "status": "definition_pass",
            "fallback_if_missing": "none",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "BF4552_1_scalar_trace_boundary",
            "claim": "A homogeneous scalar boundary action produces tangential trace stress only.",
            "mathematical_form": "S_boundary=int sqrt(|gamma|)F(Y_scalar homogeneous) -> tau_AB=tau gamma_AB",
            "passes_if": "full boundary variation is scalar-only, homogeneous, marker-free and no shear/current labels are admitted",
            "current_owner": "conditional_math_pass_from_O1/T1",
            "status": "conditional_math_pass",
            "fallback_if_missing": "retain boundary vector amplitude row",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "BF4552_2_normal_flux_zero",
            "claim": "Trace-only tangential boundary stress gives no alpha3 normal momentum flux when all normal exchange terms are included and zero.",
            "mathematical_form": "n_mu gamma_tangent^{mu nu}=0 and n_mu B_boundary^{mu i}=0",
            "passes_if": "stationary collar plus boundary Euler/Hamiltonian no-flux/topological exactness actually sets the normal flux amplitude to zero",
            "current_owner": "not_parent_signed",
            "status": "open_owner_gap",
            "fallback_if_missing": "|F_alpha3| <= B_alpha3 or assigned sub-budget",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "BF4552_3_poynting_flux_firewall",
            "claim": "Radiative EM/Poynting flux is not erased by the boundary theorem.",
            "mathematical_form": "nonzero radiative flux is routed through T_total/Hamiltonian charge; if present it reopens F_alpha3 or a separate flux row",
            "passes_if": "no-flux branch is restricted to compact stationary non-radiative local packets",
            "current_owner": "private_packet_4175_4176",
            "status": "active_guard",
            "fallback_if_missing": "do not use F_alpha3=0 for radiative systems",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "BF4552_4_contract_verdict",
            "claim": "Current corpus parent-derives F_alpha3=0.",
            "mathematical_form": "parent_boundary_action -> scalar trace + no normal momentum flux -> F_alpha3=0",
            "passes_if": "O0-O6/T1-T4 are all parent-owned",
            "current_owner": "fail",
            "status": "zero_not_promoted_keep_finite_row",
            "fallback_if_missing": "source or derive a numeric bound on F_alpha3",
            "valid_for_claim": "False",
        },
    ]


def finite_vector_rows() -> list[dict[str, Any]]:
    context = numeric_context()
    bound = context["bound"]
    half = context["half_bound"]
    third = context["third_bound"]
    epsilon_u3 = context["epsilon_u3"]
    cubic_only = context["cubic_only_c3"]
    cubic_third = context["cubic_equal_third_c3"]
    return [
        {
            "row_id": "FV4552_0_no_cancellation_master",
            "channel": "marker_plus_boundary_plus_cubic",
            "amplitude_symbol": "|M_alpha3| + |F_alpha3| + |C3_alpha3| epsilon_U^3",
            "exact_requirement": "|M_alpha3| + |F_alpha3| + |C3_alpha3| epsilon_U^3 <= B_alpha3",
            "total_bound": f"{bound:.16e}",
            "assigned_budget": f"{bound:.16e}",
            "units": "dimensionless alpha3",
            "numeric_value": f"{bound:.16e}",
            "source_epsilon_U3": f"{epsilon_u3:.16e}",
            "status": "master_no_cancellation_condition_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "row_id": "FV4552_1_marker_only_budget",
            "channel": "marker/domain vector",
            "amplitude_symbol": "|M_alpha3|",
            "exact_requirement": "|M_alpha3| <= B_alpha3 if F_alpha3=0 and cubic residue=0",
            "total_bound": f"{bound:.16e}",
            "assigned_budget": f"{bound:.16e}",
            "units": "dimensionless alpha3",
            "numeric_value": f"{bound:.16e}",
            "source_epsilon_U3": f"{epsilon_u3:.16e}",
            "status": "finite_marker_amplitude_row_waiting_for_parent_or_numeric_source",
            "valid_for_claim": "False",
        },
        {
            "row_id": "FV4552_2_boundary_only_budget",
            "channel": "boundary normal momentum flux",
            "amplitude_symbol": "|F_alpha3|",
            "exact_requirement": "|F_alpha3| <= B_alpha3 if M_alpha3=0 and cubic residue=0",
            "total_bound": f"{bound:.16e}",
            "assigned_budget": f"{bound:.16e}",
            "units": "dimensionless alpha3",
            "numeric_value": f"{bound:.16e}",
            "source_epsilon_U3": f"{epsilon_u3:.16e}",
            "status": "finite_boundary_flux_row_waiting_for_parent_or_numeric_source",
            "valid_for_claim": "False",
        },
        {
            "row_id": "FV4552_3_marker_boundary_equal_split",
            "channel": "marker and boundary only",
            "amplitude_symbol": "|M_alpha3|, |F_alpha3|",
            "exact_requirement": "|M_alpha3| <= B_alpha3/2 and |F_alpha3| <= B_alpha3/2 if cubic residue=0",
            "total_bound": f"{bound:.16e}",
            "assigned_budget": f"{half:.16e}",
            "units": "dimensionless alpha3",
            "numeric_value": f"{half:.16e}",
            "source_epsilon_U3": f"{epsilon_u3:.16e}",
            "status": "two_channel_equal_split_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "row_id": "FV4552_4_three_way_equal_split",
            "channel": "marker boundary cubic amplitude",
            "amplitude_symbol": "|M_alpha3|, |F_alpha3|, |C3_alpha3|epsilon_U^3",
            "exact_requirement": "each <= B_alpha3/3 under equal safety split",
            "total_bound": f"{bound:.16e}",
            "assigned_budget": f"{third:.16e}",
            "units": "dimensionless alpha3",
            "numeric_value": f"{third:.16e}",
            "source_epsilon_U3": f"{epsilon_u3:.16e}",
            "status": "three_channel_equal_split_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "row_id": "FV4552_5_cubic_coefficient_equal_split",
            "channel": "higher-order vector residue coefficient",
            "amplitude_symbol": "|C3_alpha3|",
            "exact_requirement": "|C3_alpha3| <= (B_alpha3/3)/epsilon_U^3 under three-way split",
            "total_bound": f"{bound:.16e}",
            "assigned_budget": f"{third:.16e}",
            "units": "dimensionless coefficient multiplying epsilon_U^3",
            "numeric_value": f"{cubic_third:.16e}",
            "source_epsilon_U3": f"{epsilon_u3:.16e}",
            "status": "finite_cubic_coefficient_split_row_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "row_id": "FV4552_6_cubic_only_after_marker_boundary_zero",
            "channel": "higher-order vector residue coefficient",
            "amplitude_symbol": "|C3_alpha3|",
            "exact_requirement": "|C3_alpha3| <= B_alpha3/epsilon_U^3 if M_alpha3=F_alpha3=0",
            "total_bound": f"{bound:.16e}",
            "assigned_budget": f"{bound:.16e}",
            "units": "dimensionless coefficient multiplying epsilon_U^3",
            "numeric_value": f"{cubic_only:.16e}",
            "source_epsilon_U3": f"{epsilon_u3:.16e}",
            "status": "finite_cubic_only_budget_nonclaim",
            "valid_for_claim": "False",
        },
    ]


def survival_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "SD4552_0_scalar_source_only",
            "M_alpha3": "0 by no-marker scalar singlet premise",
            "F_alpha3": "0 by scalar boundary no-flux premise",
            "C3_alpha3": "bounded by FV4552_6",
            "outcome": "alpha3 can survive as local branch if cubic vector residue is classified/bounded",
            "claim_allowed_now": "False",
        },
        {
            "case_id": "SD4552_1_marker_open_boundary_zero",
            "M_alpha3": "finite row required",
            "F_alpha3": "0 if boundary no-flux parent-owned",
            "C3_alpha3": "bounded or zero",
            "outcome": "must source or derive |M_alpha3| before any PPN pass",
            "claim_allowed_now": "False",
        },
        {
            "case_id": "SD4552_2_marker_zero_boundary_open",
            "M_alpha3": "0 if parent scalar-singlet/no-marker signed",
            "F_alpha3": "finite row required",
            "C3_alpha3": "bounded or zero",
            "outcome": "must source or derive |F_alpha3| before any PPN pass",
            "claim_allowed_now": "False",
        },
        {
            "case_id": "SD4552_3_both_open",
            "M_alpha3": "finite row required",
            "F_alpha3": "finite row required",
            "C3_alpha3": "bounded or zero",
            "outcome": "alpha3 branch remains blocked until both vector amplitudes are killed or bounded",
            "claim_allowed_now": "False",
        },
        {
            "case_id": "SD4552_4_radiative_flux_case",
            "M_alpha3": "case-dependent",
            "F_alpha3": "not zero by stationary compact theorem",
            "C3_alpha3": "case-dependent",
            "outcome": "radiative EM/gravity flux must be routed through T_total/Hamiltonian charge and scored separately",
            "claim_allowed_now": "False",
        },
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLOCK4552_0_parent_scalar_singlet",
            "what_is_now_known": "A scalar singlet cannot source the alpha3 vector projection.",
            "remaining_gap": "Parent action has not proved all local/domain/boundary data are scalar singlets in the compact branch.",
            "next_action": "derive q-basic scalar-singlet local packet theorem or keep M_alpha3 finite",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4552_1_marker_exclusion",
            "what_is_now_known": "Any marker/spin/velocity/off-centre/domain vector supplies the missing alpha3 vector representation.",
            "remaining_gap": "No parent exclusion theorem yet for all such vector markers.",
            "next_action": "parent-sign no-marker clause or source numeric |M_alpha3| row",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4552_2_boundary_flux_owner",
            "what_is_now_known": "Scalar trace boundary stress can kill alpha3 flux only if normal momentum flux is truly zero.",
            "remaining_gap": "Boundary action/no-flux owner O0-O6 remains unsigned; Ward ownership is not zero.",
            "next_action": "derive boundary scalar action/no-flux from parent variation or source numeric |F_alpha3| row",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4552_3_cubic_vector_residue",
            "what_is_now_known": "Cubic vector residue has a finite coefficient budget once M_alpha3 and F_alpha3 are zero/bounded.",
            "remaining_gap": "C3_alpha3 is not classified by representation or sourced numerically.",
            "next_action": "classify O(epsilon_U^3) vector terms after marker/boundary decision",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G4552_0_source_projection_zero",
            "requirement": "scalar source projection zero imported from 4551",
            "status": "PASS_CONDITIONAL_SOURCE_MODEL",
            "claim_effect": "removes scalar source product from alpha3 split only inside selected branch",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4552_1_marker_zero_or_bound",
            "requirement": "M_alpha3=0 parent-signed or numeric |M_alpha3| bound row filled",
            "status": "BLOCKED",
            "claim_effect": "blocks alpha3 PPN promotion",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4552_2_boundary_flux_zero_or_bound",
            "requirement": "F_alpha3=0 parent-signed or numeric |F_alpha3| bound row filled",
            "status": "BLOCKED",
            "claim_effect": "blocks alpha3 PPN promotion",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4552_3_cubic_residue_zero_or_bound",
            "requirement": "C3_alpha3 representation-zero or coefficient bound",
            "status": "PENDING_AFTER_VECTOR_CHANNELS",
            "claim_effect": "needed after marker/boundary channels close",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4552_4_no_public_or_ppn_claim",
            "requirement": "No alpha3/local-GR claim promoted while G4552_1 or G4552_2 is blocked.",
            "status": "PASS_NONCLAIM_GUARD",
            "claim_effect": "keeps checkpoint as private derivation/fallback plumbing",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4552_0",
            "decision": DECISION,
            "summary": "4552 turns the alpha3 blocker into a cleaner exact split: after scalar source projection zero, alpha3 can only survive through marker/domain vector amplitude M_alpha3, boundary normal-momentum flux F_alpha3, or cubic vector residue. Zero proofs are stated as contracts; because parent ownership is still missing, finite amplitude rows are produced and all claim gates remain nonclaim.",
            "claim_id": CLAIM_ID,
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "alpha3 is now reduced to two zero-or-bound vector channels. The cleanest win is to parent-sign scalar-singlet/no-marker and scalar-boundary/no-flux; otherwise fill the first finite vector amplitude row.",
            "success_condition": "Either M_alpha3=F_alpha3=0 is parent-derived, or both amplitudes have sourced numeric rows satisfying the no-cancellation alpha3 budget.",
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
    reduced: list[dict[str, Any]],
    marker: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    rows.append(
        {
            "validation_id": "VAL4552_0_sources",
            "check": "all cited source paths exist and needles are found",
            "status": "PASS" if sources_ok else "FAIL",
            "details": f"{sum(1 for row in sources if row['exists'] == 'True' and row['needle_found'] == 'True')}/{len(sources)} sources verified",
        }
    )

    split_text = " ".join(str(value) for row in reduced for value in row.values())
    split_ok = all(token in split_text for token in ["M_alpha3", "F_alpha3", "C3_alpha3", "epsilon_U^3"])
    rows.append(
        {
            "validation_id": "VAL4552_1_reduced_split",
            "check": "reduced alpha3 split explicitly contains marker, boundary flux and cubic channels",
            "status": "PASS" if split_ok else "FAIL",
            "details": "Delta alpha3 = M_alpha3 + F_alpha3 + C3_alpha3 epsilon_U^3",
        }
    )

    marker_text = " ".join(str(value) for row in marker for value in row.values())
    marker_ok = "no-marker" in marker_text or "No material marker" in marker_text
    marker_ok = marker_ok and "finite" in marker_text and "not_parent_signed" in marker_text
    rows.append(
        {
            "validation_id": "VAL4552_2_marker_contract",
            "check": "marker exclusion contract has zero route and finite fallback",
            "status": "PASS" if marker_ok else "FAIL",
            "details": "M_alpha3 retained unless scalar-singlet/no-marker is parent-signed",
        }
    )

    boundary_text = " ".join(str(value) for row in boundary for value in row.values())
    boundary_ok = "normal momentum flux" in boundary_text and "Poynting" in boundary_text and "not_parent_signed" in boundary_text
    rows.append(
        {
            "validation_id": "VAL4552_3_boundary_contract",
            "check": "boundary flux contract has no-flux route, Poynting guard and finite fallback",
            "status": "PASS" if boundary_ok else "FAIL",
            "details": "F_alpha3 retained unless scalar-boundary/no-flux is parent-signed",
        }
    )

    finite_values = [safe_float(row.get("numeric_value")) for row in finite]
    finite_ok = bool(finite_values) and all(value is not None and value > 0 for value in finite_values)
    finite_ok = finite_ok and all(row.get("valid_for_claim") == "False" for row in finite)
    rows.append(
        {
            "validation_id": "VAL4552_4_finite_rows",
            "check": "finite vector rows have positive numeric values and remain nonclaim",
            "status": "PASS" if finite_ok else "FAIL",
            "details": f"{len(finite)} finite rows checked",
        }
    )

    gates_ok = all(row.get("valid_for_claim") == "False" for row in gates) and any(row.get("status") == "BLOCKED" for row in gates)
    rows.append(
        {
            "validation_id": "VAL4552_5_claim_guard",
            "check": "no alpha3/local-GR claim is promoted",
            "status": "PASS" if gates_ok else "FAIL",
            "details": "claim gates remain blocked/nonclaim",
        }
    )

    docs_ok = DOC_PATH.exists() and FORMAL_PATH.exists()
    rows.append(
        {
            "validation_id": "VAL4552_6_docs",
            "check": "post and formal docs exist during validation",
            "status": "PASS" if docs_ok else "FAIL",
            "details": f"post={DOC_PATH.exists()} formal={FORMAL_PATH.exists()}",
        }
    )

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL4552_OVERALL",
            "check": "4552 checkpoint validation",
            "status": "PASS" if overall else "FAIL",
            "details": DECISION if overall else "one or more validation checks failed",
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    reduced: list[dict[str, Any]],
    marker: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    survival: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    context = numeric_context()
    return f"""# 4552 - alpha3 marker exclusion, boundary flux owner, or finite vector amplitude row

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4551 killed the scalar source part of `alpha3` on the centred point-mass source-model branch:

```text
K_alpha3^src[f(r)] = 0
```

4552 now prevents that win from being overread. The actual reduced alpha3 branch is:

```text
Delta alpha3 = M_alpha3 + F_alpha3 + C3_alpha3 epsilon_U^3
```

where:

- `M_alpha3` is any surviving marker/domain/preferred-frame vector channel;
- `F_alpha3` is boundary normal-momentum flux;
- `C3_alpha3 epsilon_U^3` is the first retained higher-order vector residue.

So the alpha3 question is no longer vague. Either the parent action kills `M_alpha3` and `F_alpha3`, or those amplitudes need real finite rows. No theorem is promoted yet, because the no-marker and boundary no-flux owner clauses are still unsigned.

Numerically, for the selected 1--30 AU source-model row:

```text
B_alpha3   = {context['bound']:.16e}
epsilon_U  = {context['epsilon_u']:.16e}
epsilon_U^2= {context['epsilon_u2']:.16e}
epsilon_U^3= {context['epsilon_u3']:.16e}
```

The no-cancellation gate is:

```text
|M_alpha3| + |F_alpha3| + |C3_alpha3| epsilon_U^3 <= {context['bound']:.16e}.
```

If marker and boundary channels are both zero, the cubic coefficient allowance is:

```text
|C3_alpha3| <= {context['cubic_only_c3']:.16e}.
```

That is a real narrowing of the route, not a public PPN/local-GR pass.

## Reduced Alpha3 Split

{markdown_table(reduced)}

## Marker Exclusion Contract

{markdown_table(marker)}

## Boundary Flux Owner Contract

{markdown_table(boundary)}

## Finite Vector Amplitude Rows

{markdown_table(finite)}

## Survival Decision Matrix

{markdown_table(survival)}

## Remaining Blockers

{markdown_table(blockers)}

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
        "claim": "4552 reduces the alpha3 problem to exact marker-vector, boundary-flux and cubic-residue channels after the scalar source projection zero.",
        "current_evidence": "Generated source register, reduced alpha3 split, marker exclusion contract, boundary flux owner contract, finite vector amplitude rows, survival matrix, claim gates, status and validation CSVs.",
        "status": "alpha3_marker_boundary_flux_split_nonclaim",
        "next_test": NEXT_TARGET,
        "failure_mode": "Treating scalar source projection zero as a full alpha3/PPN pass while M_alpha3 or F_alpha3 remains unsigned or unbounded.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "Alpha3 is now a zero-or-bound channel problem: derive no-marker/no-flux from the parent action or fill finite vector amplitudes.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    reduced = reduced_split_rows()
    marker = marker_contract_rows()
    boundary = boundary_contract_rows()
    finite = finite_vector_rows()
    survival = survival_rows()
    blockers = blocker_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_ = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(REDUCED_SPLIT_CSV, reduced)
    write_csv(MARKER_CONTRACT_CSV, marker)
    write_csv(BOUNDARY_CONTRACT_CSV, boundary)
    write_csv(FINITE_VECTOR_CSV, finite)
    write_csv(SURVIVAL_CSV, survival)
    write_csv(BLOCKERS_CSV, blockers)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_)
    write_csv(STATUS_CSV, status)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    pending_doc = f"# 4552 - alpha3 marker exclusion, boundary flux owner, or finite vector amplitude row\n\nMarker: `{MARKER}`\n\nValidation pending.\n"
    DOC_PATH.write_text(pending_doc, encoding="utf-8")
    FORMAL_PATH.write_text(pending_doc, encoding="utf-8")

    validation = validate(sources, reduced, marker, boundary, finite, gates)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, reduced, marker, boundary, finite, survival, blockers, gates, decisions, next_, validation)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4552 Alpha3 Marker/Boundary Flux Split

Marker: `{MARKER}`  
4552 reduces the hard alpha3 local-PPN wall to a clean zero-or-bound split:

```text
Delta alpha3 = M_alpha3 + F_alpha3 + C3_alpha3 epsilon_U^3.
```

The scalar point-mass source channel is already projected out by 4551. The live parent-action targets are now no-marker scalar-singlet ownership for `M_alpha3=0` and scalar boundary/no-normal-flux ownership for `F_alpha3=0`. Until those are derived or finite amplitude rows are filled, alpha3 remains a private nonclaim gate. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4552 Packet Integration - Alpha3 Marker/Boundary Flux Split

Marker: `{PACKET_MARKER}`  
The packet now treats alpha3 as a reduced vector-channel problem. Scalar source leakage is not the active threat; marker/domain vectors and boundary normal-momentum flux are. Radiative Poynting/EM flux is not erased by no-flux language and must be routed through `T_total`/Hamiltonian charge if present.
""",
    )

    print(f"wrote {DOC_PATH}")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    overall = next((row for row in validation if row["validation_id"] == "VAL4552_OVERALL"), {})
    print(f"overall={overall.get('status', 'UNKNOWN')} decision={DECISION}")


if __name__ == "__main__":
    main()

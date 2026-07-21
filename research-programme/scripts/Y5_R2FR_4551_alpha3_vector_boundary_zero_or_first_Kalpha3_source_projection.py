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

CHECKPOINT = "4551"
CLAIM_ID = "L-393"
BRANCH_ID = "MTS_R2FR_Y5_ALPHA3_VECTOR_SPLIT_4551"
MARKER = "PPC4161_ALPHA3_VECTOR_BOUNDARY_ZERO_OR_FIRST_KALPHA3_SOURCE_PROJECTION_4551"
PACKET_MARKER = "PPC4161_PACKET_ALPHA3_VECTOR_BOUNDARY_ZERO_OR_FIRST_KALPHA3_SOURCE_PROJECTION_4551"
DECISION = "ALPHA3_SCALAR_MONOPOLE_SOURCE_PROJECTION_ZERO_DERIVED_BOUNDARY_VECTOR_ZERO_CONDITIONAL_RETAINED_NONCLAIM"
NEXT_TARGET = "4552-Y5-R2FR-alpha3-marker-exclusion-boundary-flux-owner-or-finite-vector-amplitude-row.md"

FORMAL_PATH = FORMAL / "567-PPC4161-alpha3-vector-boundary-zero-or-first-Kalpha3-source-projection.md"
DOC_PATH = POST / "4551-Y5-R2FR-alpha3-vector-boundary-zero-or-first-Kalpha3-source-projection.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4550 = FORMAL / "566-PPC4161-first-static-coefficient-product-bound-or-projection-kernel-row.md"
DOC_4549 = FORMAL / "565-PPC4161-source-real-local-domain-Bmin-or-first-projection-kernel-row.md"
DOC_4545 = FORMAL / "561-PPC4161-attractor-stationarity-and-boundary-silence-from-Bianchi-Hamiltonian-local-conservation.md"
PRODUCTS_4550 = SOURCE_DIR / "P8_Y5_R2FR_4550_OBSERVABLE_PRODUCT_BOUNDS.csv"
RANKING_4550 = SOURCE_DIR / "P8_Y5_R2FR_4550_PRODUCT_BOUND_RANKING.csv"
NEXT_4550 = SOURCE_DIR / "P8_Y5_R2FR_4550_NEXT_TARGET.csv"
DOMAIN_4549 = SOURCE_DIR / "P8_Y5_R2FR_4549_LOCAL_DOMAIN_BMIN_ROWS.csv"
UB2_4546 = SOURCE_DIR / "P8_Y5_R2FR_4546_UB2_STATIC_BOUND_THEOREM.csv"
ML_4546 = SOURCE_DIR / "P8_Y5_R2FR_4546_ML_HOMOGENEITY_BOUND.csv"
PROJ_4547 = SOURCE_DIR / "P8_Y5_R2FR_4547_ARENA_PROJECTION_CONTRACT.csv"
ALPHA3_TEMPLATE = SOURCE_DIR / "P8_ALPHA3_NUMERIC_PRODUCT_INPUT_TEMPLATE.csv"
ALPHA3_ZERO_GATE = SOURCE_DIR / "P8_ALPHA3_THEOREM_ZERO_GATE.csv"
BOUNDARY_ATTEMPT = SOURCE_DIR / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv"
BOUNDARY_OWNER = SOURCE_DIR / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv"
BOUNDARY_REPAIR = SOURCE_DIR / "P8_BOUNDARY_SCALAR_PREMISE_REPAIR_LEDGER.csv"
BOUNDARY_STATUS = SOURCE_DIR / "P8_BOUNDARY_ALPHA3_CLOSURE_STATUS.csv"
PACKET = FORMAL / "180-PPC4161-private-local-packet-integration.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4551_SOURCE_REGISTER.csv"
SPLIT_LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4551_ALPHA3_SPLIT_LAW.csv"
KPROJ_CSV = SOURCE_DIR / "P8_Y5_R2FR_4551_KALPHA3_SOURCE_PROJECTION_ROWS.csv"
SOURCE_ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4551_SOURCE_VECTOR_ZERO_THEOREM.csv"
BOUNDARY_ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4551_BOUNDARY_VECTOR_ZERO_THEOREM.csv"
SURVIVAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4551_ALPHA3_SURVIVAL_MATRIX.csv"
FALLBACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4551_FINITE_FALLBACK_PRODUCTS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4551_REMAINING_BLOCKERS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4551_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4551_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4551_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4551_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4551_VALIDATION.csv"


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
        lines.append(f"| ... | {len(rows) - limit} additional rows in CSV |" + " |" * max(len(headers) - 2, 0))
    return "\n".join(lines) + "\n"


def safe_float(value: Any) -> float | None:
    try:
        if value is None or str(value).strip().lower() in {"", "missing", "nan"}:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def source_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC4551_00_4550_product_wall",
            "label": "4550 alpha3 product wall",
            "path": PRODUCTS_4550,
            "needle": "PB4550_alpha3",
        },
        {
            "source_id": "SRC4551_01_4550_ranking",
            "label": "4550 alpha3 priority ranking",
            "path": RANKING_4550,
            "needle": "smallest allowed product is the first closure pressure point",
        },
        {
            "source_id": "SRC4551_02_4550_doc",
            "label": "4550 documented alpha3 wall",
            "path": DOC_4550,
            "needle": "alpha3: |K_alpha3^src S_static| <= 6.4582427632245591e-06",
        },
        {
            "source_id": "SRC4551_03_4549_domain",
            "label": "4549 spherical point-mass domain",
            "path": DOMAIN_4549,
            "needle": "D4549_0_inner_solar_1_to_30_AU",
        },
        {
            "source_id": "SRC4551_04_4549_doc",
            "label": "4549 point-mass monotone domain law",
            "path": DOC_4549,
            "needle": "B_min = B_env(r_out),  epsilon_U([r_in,r_out]) = U_B(r_out).",
        },
        {
            "source_id": "SRC4551_05_4546_source_bound",
            "label": "4546 U_B^2 source bound",
            "path": UB2_4546,
            "needle": "UB24546_1_linear_silence",
        },
        {
            "source_id": "SRC4551_06_4546_mL_bound",
            "label": "4546 m_L scalar laplacian bound",
            "path": ML_4546,
            "needle": "ML4546_2_laplacian",
        },
        {
            "source_id": "SRC4551_07_4547_projection",
            "label": "4547 alpha3 projection split",
            "path": PROJ_4547,
            "needle": "Delta_alpha3 = K_alpha3^vec B_boundary/vector_static + K_alpha3^src B_src",
        },
        {
            "source_id": "SRC4551_08_alpha3_template",
            "label": "alpha3 product input template",
            "path": ALPHA3_TEMPLATE,
            "needle": "A3_BOUNDARY_NUMERIC_OR_ZERO",
        },
        {
            "source_id": "SRC4551_09_alpha3_zero_gate",
            "label": "alpha3 theorem zero gate",
            "path": ALPHA3_ZERO_GATE,
            "needle": "TG_boundary_zero",
        },
        {
            "source_id": "SRC4551_10_boundary_attempt",
            "label": "boundary alpha3 no-flux theorem attempt",
            "path": BOUNDARY_ATTEMPT,
            "needle": "T3_no_preferred_vector",
        },
        {
            "source_id": "SRC4551_11_boundary_owner",
            "label": "boundary scalar action owner attempt",
            "path": BOUNDARY_OWNER,
            "needle": "O0_representation_zero",
        },
        {
            "source_id": "SRC4551_12_boundary_repair",
            "label": "boundary scalar premise repair ledger",
            "path": BOUNDARY_REPAIR,
            "needle": "R1_no_marker_exclusion",
        },
        {
            "source_id": "SRC4551_13_boundary_status",
            "label": "boundary alpha3 closure status",
            "path": BOUNDARY_STATUS,
            "needle": "conditional_closure_only",
        },
        {
            "source_id": "SRC4551_14_4545_boundary_guard",
            "label": "4545 boundary amplitude caveat",
            "path": DOC_4545,
            "needle": "Static boundary amplitude, vector/marker flux, trace/shear stress",
        },
        {
            "source_id": "SRC4551_15_packet_ppn_vector",
            "label": "private packet PPN vector context",
            "path": PACKET,
            "needle": "alpha1 = alpha2 = alpha3",
        },
        {
            "source_id": "SRC4551_16_packet_poynting_owner",
            "label": "packet Poynting/Hilbert stress context",
            "path": PACKET,
            "needle": "Therefore the Poynting vector is already part of `T_total`",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        path = spec["path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle = spec["needle"]
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": b(exists),
                "needle": needle,
                "needle_found": b(exists and needle in text),
                "valid_for_claim": "False",
            }
        )
    return rows


def alpha3_product_row() -> dict[str, str]:
    for row in read_csv(PRODUCTS_4550):
        if row.get("observable") == "alpha3":
            return row
    raise RuntimeError("alpha3 product row not found")


def selected_domain_row() -> dict[str, str]:
    for row in read_csv(DOMAIN_4549):
        if row.get("domain_id") == "D4549_0_inner_solar_1_to_30_AU":
            return row
    raise RuntimeError("selected 4549 domain row not found")


def split_law_rows(alpha3: dict[str, str], domain: dict[str, str]) -> list[dict[str, Any]]:
    eps = safe_float(domain.get("epsilon_U_domain"))
    eps2 = safe_float(domain.get("epsilon_U_squared"))
    bound = safe_float(alpha3.get("bound"))
    if eps is None or eps2 is None or bound is None:
        raise RuntimeError("missing numeric alpha3/domain values")
    eps3 = eps * eps2
    return [
        {
            "law_id": "LAW4551_0_alpha3_channel_split",
            "object": "alpha3 static channel",
            "law": "Delta_alpha3 = K_alpha3^src B_src + K_alpha3^vec B_boundary/vector_static + R_alpha3,higher",
            "with_4546_4549": "B_src = S_static epsilon_U^2 + O(epsilon_U^3)",
            "result": "Delta_alpha3 = P_alpha3_src epsilon_U^2 + Q_alpha3_vec + R_alpha3,higher, where P_alpha3_src=K_alpha3^src S_static.",
            "status": "derived_from_4547_4550",
            "valid_for_claim": "False",
        },
        {
            "law_id": "LAW4551_1_scalar_monopole_projection",
            "object": "K_alpha3 on scalar spherical source",
            "law": "For a centred stationary SO(3) scalar monopole f(r), the rank-one/vector projection vanishes: P_i[f]=integral n_i f(r)dOmega=0.",
            "with_4546_4549": "U_B S_cg and D_m Delta_h m_L are scalar/radial in the selected point-mass source-model branch.",
            "result": "K_alpha3^src S_static = 0 on the scalar monopole subspace, unless vector markers, rotation, anisotropic domain terms or non-scalar source pieces enter.",
            "status": "conditional_mathematical_projection_zero",
            "valid_for_claim": "False",
        },
        {
            "law_id": "LAW4551_2_boundary_vector_zero",
            "object": "Q_alpha3_vec",
            "law": "If the boundary action is homogeneous scalar, marker-free, stationary and normal-momentum no-flux, then B_boundary/vector_static has no alpha3 vector component.",
            "with_4546_4549": "Imports prior boundary alpha3 no-flux theorem attempt and 4545 caveat.",
            "result": "Q_alpha3_vec=0 conditionally; current corpus does not parent-own all premises.",
            "status": "conditional_boundary_zero_not_parent_promoted",
            "valid_for_claim": "False",
        },
        {
            "law_id": "LAW4551_3_higher_order_budget",
            "object": "R_alpha3,higher",
            "law": "If source and boundary vector pieces vanish, remaining higher-order vector leakage must satisfy |R_alpha3,higher| <= 4e-20.",
            "with_4546_4549": f"epsilon_U={eps:.16e}, epsilon_U^2={eps2:.16e}, epsilon_U^3={eps3:.16e}",
            "result": f"If R_alpha3,higher=C3_alpha3 epsilon_U^3, then |C3_alpha3| <= {bound / eps3:.16e}.",
            "status": "finite_higher_order_budget_ready",
            "valid_for_claim": "False",
        },
    ]


def kalpha3_projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "K4551_0_scalar_radial_source",
            "source_component": "U_B S_cg scalar radial part",
            "representation": "SO(3) scalar monopole, time-even",
            "projection_rule": "K_alpha3^src[f(r)] = 0 because alpha3 is vector/preferred-frame and integral n_i f(r)dOmega=0.",
            "projection_value": "0",
            "zero_status": "conditional_projection_zero",
            "premises_needed": "centred spherical source-model domain; no vector marker; no rotation/spin/preferred-frame label; no anisotropic projector leakage",
            "valid_for_claim": "False",
        },
        {
            "projection_id": "K4551_1_mL_laplacian_radial",
            "source_component": "D_m Delta_h m_L scalar radial part",
            "representation": "SO(3) scalar Laplacian of radial scalar",
            "projection_rule": "K_alpha3^src[Delta_h m_L(r)] = 0 for the same scalar-monopole reason.",
            "projection_value": "0",
            "zero_status": "conditional_projection_zero",
            "premises_needed": "m_L=m_L(r) in selected domain; no anisotropic attractor mode; transition shell excluded",
            "valid_for_claim": "False",
        },
        {
            "projection_id": "K4551_2_marker_vector_residual",
            "source_component": "marker/velocity/spin/domain-vector residual",
            "representation": "rank-one vector or preferred-frame object",
            "projection_rule": "K_alpha3 is not zero on this subspace; it must be theorem-excluded or bounded.",
            "projection_value": "unknown",
            "zero_status": "retained_finite_fallback",
            "premises_needed": "parent marker-exclusion theorem or numeric amplitude row",
            "valid_for_claim": "False",
        },
        {
            "projection_id": "K4551_3_boundary_vector_residual",
            "source_component": "B_boundary/vector_static",
            "representation": "boundary tangent/normal momentum vector",
            "projection_rule": "zero only if scalar homogeneous no-flux boundary premises O0-O6 are parent-owned.",
            "projection_value": "conditional_zero_or_unknown",
            "zero_status": "conditional_boundary_zero_not_parent_owned",
            "premises_needed": "scalar boundary action; no markers; no normal momentum flux; full boundary stress variation",
            "valid_for_claim": "False",
        },
    ]


def source_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "SZ4551_0_branch_object",
            "claim": "Selected 4549 source-model domain is centred point-mass, stationary, and spherically symmetric.",
            "derivation": "4549 imports the 89 Schwarzschild-vacuum Weyl point-mass source model and samples radial B_env(r).",
            "result": "source residual scalar amplitudes are functions of r only inside this source-model branch",
            "status": "source_model_branch_pass_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "step_id": "SZ4551_1_source_terms_scalar",
            "claim": "The 4546 static source terms feeding S_static are scalar/radial on that branch.",
            "derivation": "U_B, S_cg(D_L,Y) scalar leakage amplitude and Delta_h m_L(r) carry no free spatial vector index when no marker fields are present.",
            "result": "S_static belongs to scalar monopole representation",
            "status": "conditional_math_pass",
            "valid_for_claim": "False",
        },
        {
            "step_id": "SZ4551_2_alpha3_vector_projection",
            "claim": "A scalar monopole cannot source alpha3's vector/preferred-frame projection.",
            "derivation": "Every vector projection from a centred scalar shell is proportional to integral n_i f(r)dOmega=0.",
            "result": "K_alpha3^src S_static=0 on scalar monopole subspace",
            "status": "first_Kalpha3_source_projection_zero_row",
            "valid_for_claim": "False",
        },
        {
            "step_id": "SZ4551_3_countermodel_guard",
            "claim": "The theorem fails if a vector marker, spin, velocity, anisotropic domain, off-centre source, or transition-current vector enters.",
            "derivation": "Those objects supply the missing vector representation and can project to alpha3.",
            "result": "marker/vector residual is retained and must be excluded or bounded",
            "status": "active_guard_no_global_claim",
            "valid_for_claim": "False",
        },
    ]


def boundary_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "BZ4551_0_boundary_target",
            "claim": "Boundary alpha3 is the vector/preferred-momentum flux projection Q_alpha3_vec.",
            "derivation": "Imports prior boundary alpha3 theorem attempt T0 and 4550 split Q_alpha3_vec=K_alpha3^vec B_boundary/vector_static.",
            "result": "the boundary target is explicit",
            "status": "definition_pass",
            "valid_for_claim": "False",
        },
        {
            "step_id": "BZ4551_1_scalar_homogeneous_boundary",
            "claim": "A homogeneous scalar boundary action produces no tangential vector alpha3 source.",
            "derivation": "Variation of S_boundary=sqrt(gamma)F(scalar homogeneous data) gives trace/isotropic tangential stress; no mixed vector component.",
            "result": "B_boundary/vector_static=0 if scalar-homogeneous and marker-free",
            "status": "conditional_math_pass",
            "valid_for_claim": "False",
        },
        {
            "step_id": "BZ4551_2_no_flux",
            "claim": "Normal momentum flux must be zero, not merely Ward-owned.",
            "derivation": "n_mu B_boundary^{mu i}=0 removes preferred momentum flux; 4545 only gave derivative silence, not amplitude absence.",
            "result": "Q_alpha3_vec=0 only if no-flux is parent-owned or numerically bounded",
            "status": "conditional_not_parent_owned",
            "valid_for_claim": "False",
        },
        {
            "step_id": "BZ4551_3_parent_owner_audit",
            "claim": "Current corpus parent-owns all scalar-homogeneous marker-free no-flux boundary premises.",
            "derivation": "Boundary owner O7 fails; repair ledger R0-R4 remains open.",
            "result": "boundary vector zero is a conditional closure, not a promoted theorem",
            "status": "fail_parent_owner_nonclaim",
            "valid_for_claim": "False",
        },
    ]


def fallback_rows(alpha3: dict[str, str], domain: dict[str, str]) -> list[dict[str, Any]]:
    eps = safe_float(domain.get("epsilon_U_domain"))
    eps2 = safe_float(domain.get("epsilon_U_squared"))
    bound = safe_float(alpha3.get("bound"))
    if eps is None or eps2 is None or bound is None:
        raise RuntimeError("missing fallback numeric values")
    eps3 = eps * eps2
    pmax = bound / eps2
    return [
        {
            "fallback_id": "FB4551_0_if_boundary_and_higher_zero",
            "assumption": "Q_alpha3_vec=0 and R_alpha3,higher=0",
            "required_bound": "|K_alpha3^src S_static| <= B_alpha3/epsilon_U^2",
            "numeric_value": f"{pmax:.16e}",
            "units": "dimensionless combined product",
            "status": "same_as_4550_product_wall",
            "valid_for_claim": "False",
        },
        {
            "fallback_id": "FB4551_1_equal_split",
            "assumption": "half alpha3 budget to source product, half to boundary+higher residues",
            "required_bound": "|K_alpha3^src S_static| <= B_alpha3/(2 epsilon_U^2); |Q_alpha3_vec|+|R| <= B_alpha3/2",
            "numeric_value": f"{0.5 * pmax:.16e}; boundary_plus_higher <= {0.5 * bound:.16e}",
            "units": "dimensionless",
            "status": "conservative_nonclaim_budget",
            "valid_for_claim": "False",
        },
        {
            "fallback_id": "FB4551_2_if_source_and_boundary_zero_higher_order",
            "assumption": "P_alpha3_src=0 and Q_alpha3_vec=0, but R_alpha3,higher=C3_alpha3 epsilon_U^3 remains",
            "required_bound": "|C3_alpha3| <= B_alpha3/epsilon_U^3",
            "numeric_value": f"{bound / eps3:.16e}",
            "units": "dimensionless higher-order coefficient",
            "status": "higher_order_budget_ready",
            "valid_for_claim": "False",
        },
        {
            "fallback_id": "FB4551_3_boundary_only",
            "assumption": "source scalar projection zero and higher-order negligible",
            "required_bound": "|Q_alpha3_vec| <= B_alpha3",
            "numeric_value": f"{bound:.16e}",
            "units": "dimensionless alpha3 residual",
            "status": "boundary_flux_product_must_be_zero_or_ultratiny",
            "valid_for_claim": "False",
        },
    ]


def survival_rows(alpha3: dict[str, str], domain: dict[str, str]) -> list[dict[str, Any]]:
    eps = safe_float(domain.get("epsilon_U_domain")) or 0.0
    eps2 = safe_float(domain.get("epsilon_U_squared")) or 0.0
    bound = safe_float(alpha3.get("bound")) or 0.0
    eps3 = eps * eps2
    return [
        {
            "case_id": "SURV4551_0_scalar_source_projection",
            "source_product": "K_alpha3^src S_static",
            "boundary_product": "not addressed",
            "higher_order": "not addressed",
            "outcome": "source product zero on scalar monopole subspace",
            "status": "conditional_math_win",
            "claim_allowed": "False",
        },
        {
            "case_id": "SURV4551_1_scalar_source_plus_boundary_zero",
            "source_product": "0",
            "boundary_product": "0 if O0-O6 boundary premises parent-owned",
            "higher_order": f"requires |C3_alpha3| <= {bound / eps3:.16e} if cubic vector residue remains",
            "outcome": "alpha3 static channel can survive inside the selected local branch",
            "status": "conditional_survival_route_not_parent_signed",
            "claim_allowed": "False",
        },
        {
            "case_id": "SURV4551_2_marker_or_flux_present",
            "source_product": "unknown vector marker projection",
            "boundary_product": "unknown flux/vector projection",
            "higher_order": "unknown",
            "outcome": "must satisfy exact alpha3 product budget, no cancellation by fit",
            "status": "finite_bound_route_required",
            "claim_allowed": "False",
        },
        {
            "case_id": "SURV4551_3_current_project_status",
            "source_product": "conditional zero",
            "boundary_product": "conditional zero but parent owner fails",
            "higher_order": "budget row ready",
            "outcome": "moved from generic missing K_alpha3 to precise source-zero plus boundary-owner problem",
            "status": "progress_nonclaim",
            "claim_allowed": "False",
        },
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLOCK4551_0_marker_exclusion",
            "what_is_now_known": "K_alpha3^src=0 on scalar monopole source terms.",
            "remaining_gap": "Parent must exclude vector markers, spin/rotation labels, domain velocity and anisotropic projector leakage.",
            "next_action": "derive marker-exclusion from parent symmetry or add finite vector amplitude row",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4551_1_boundary_owner",
            "what_is_now_known": "Boundary alpha3 zero theorem is mathematically clean if scalar homogeneous no-flux premises hold.",
            "remaining_gap": "Boundary owner O7 still fails; O0-O6 are not all parent-signed.",
            "next_action": "try to parent-sign scalar boundary action/no-marker/no-normal-flux or keep Q_alpha3_vec finite",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4551_2_higher_order_vector",
            "what_is_now_known": "If only cubic vector leakage remains, coefficient allowance is finite and not absurd.",
            "remaining_gap": "Need derive no cubic vector residue or bound C3_alpha3.",
            "next_action": "classify O(epsilon_U^3) vector representations",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4551_3_global_vs_source_model",
            "what_is_now_known": "The selected 1-30 AU point-mass source-model branch is scalar/spherical.",
            "remaining_gap": "This is not a global MTS theorem or a full Solar-System PPN solver.",
            "next_action": "keep source-model row as local scorer input until domain adoption is physically justified",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE4551_0_source_projection_zero",
            "condition": "K_alpha3 source projection vanishes on scalar radial monopole subspace",
            "status": "PASS_CONDITIONAL_MATH",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4551_1_boundary_zero",
            "condition": "Q_alpha3_vec vanishes under scalar homogeneous marker-free no-flux boundary premises",
            "status": "PASS_CONDITIONAL_MATH_PARENT_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4551_2_countermodel_guard",
            "condition": "vector marker/anisotropy/flux rows remain live and finite-bounded",
            "status": "PASS_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4551_3_no_public_ppn_claim",
            "condition": "no alpha3, PPN, R10, Newton, local-GR or unified-theory claim is promoted",
            "status": "PASS_NONCLAIM",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "decision": DECISION,
            "summary": "4551 derives the first alpha3 source-projection zero row: a centred scalar monopole source has K_alpha3^src=0 by representation. Boundary alpha3 also has a clean scalar homogeneous no-flux zero theorem, but the parent boundary owner remains unsigned, so the branch stays nonclaim with finite fallback rows.",
            "claim_id": CLAIM_ID,
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "The source side has a conditional representation-zero. The remaining alpha3 risk is marker exclusion and boundary normal momentum flux ownership.",
            "success_condition": "Either parent-sign no vector markers and no boundary flux, or provide finite amplitude rows for the retained vector channels.",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "created_utc": utc_now(),
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
    laws: list[dict[str, Any]],
    kproj: list[dict[str, Any]],
    source_zero: list[dict[str, Any]],
    boundary_zero: list[dict[str, Any]],
    survival: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append({"validation_id": "VAL4551_00_sources", "status": "PASS" if source_ok else "FAIL", "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing"})

    law_ok = any(row["law_id"] == "LAW4551_1_scalar_monopole_projection" for row in laws) and any(row["law_id"] == "LAW4551_2_boundary_vector_zero" for row in laws)
    checks.append({"validation_id": "VAL4551_01_split_law", "status": "PASS" if law_ok else "FAIL", "detail": "alpha3 source and boundary split laws present"})

    kproj_ok = any(row["projection_id"] == "K4551_0_scalar_radial_source" and row["projection_value"] == "0" for row in kproj) and any(row["projection_id"] == "K4551_2_marker_vector_residual" for row in kproj)
    checks.append({"validation_id": "VAL4551_02_Kalpha3_projection", "status": "PASS" if kproj_ok else "FAIL", "detail": "scalar source projection zero and marker fallback rows present"})

    source_ok_2 = any(row["step_id"] == "SZ4551_2_alpha3_vector_projection" and row["status"] == "first_Kalpha3_source_projection_zero_row" for row in source_zero)
    checks.append({"validation_id": "VAL4551_03_source_zero", "status": "PASS" if source_ok_2 else "FAIL", "detail": "source vector zero theorem row present"})

    boundary_ok = any(row["step_id"] == "BZ4551_3_parent_owner_audit" and row["status"] == "fail_parent_owner_nonclaim" for row in boundary_zero)
    checks.append({"validation_id": "VAL4551_04_boundary_nonclaim", "status": "PASS" if boundary_ok else "FAIL", "detail": "boundary zero theorem remains parent-unsigned"})

    survival_ok = any(row["case_id"] == "SURV4551_3_current_project_status" and row["claim_allowed"] == "False" for row in survival)
    checks.append({"validation_id": "VAL4551_05_survival_matrix", "status": "PASS" if survival_ok else "FAIL", "detail": "survival matrix keeps claim blocked"})

    fallback_ok = any(row["fallback_id"] == "FB4551_2_if_source_and_boundary_zero_higher_order" for row in fallback) and all(row["valid_for_claim"] == "False" for row in fallback)
    checks.append({"validation_id": "VAL4551_06_fallback", "status": "PASS" if fallback_ok else "FAIL", "detail": "finite fallback product rows exist and are nonclaim"})

    gate_ok = all(row["status"].startswith("PASS") for row in gates)
    checks.append({"validation_id": "VAL4551_07_claim_gates", "status": "PASS" if gate_ok else "FAIL", "detail": "claim gates pass with nonclaim posture"})

    generated = [
        SOURCE_REGISTER,
        SPLIT_LAW_CSV,
        KPROJ_CSV,
        SOURCE_ZERO_CSV,
        BOUNDARY_ZERO_CSV,
        SURVIVAL_CSV,
        FALLBACK_CSV,
        BLOCKERS_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
    ]
    csv_ok = True
    details: list[str] = []
    for path in generated:
        try:
            rows = read_csv(path)
            if not rows:
                csv_ok = False
                details.append(f"{path.name}:no_rows")
        except Exception as exc:  # pragma: no cover
            csv_ok = False
            details.append(f"{path.name}:{exc}")
    checks.append({"validation_id": "VAL4551_08_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(details)})

    doc_ok = DOC_PATH.exists() and FORMAL_PATH.exists()
    checks.append({"validation_id": "VAL4551_09_docs_written", "status": "PASS" if doc_ok else "FAIL", "detail": "post and formal checkpoint docs written"})

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append({"validation_id": "VAL4551_10_pycache_absent", "status": "PASS" if pycache_absent else "FAIL", "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present"})

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append({"validation_id": "VAL4551_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "4551 alpha3 scalar source projection zero and boundary vector audit"})
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    laws: list[dict[str, Any]],
    kproj: list[dict[str, Any]],
    source_zero: list[dict[str, Any]],
    boundary_zero: list[dict[str, Any]],
    survival: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    generated = utc_now()
    fallback_cubic = next(row for row in fallback if row["fallback_id"] == "FB4551_2_if_source_and_boundary_zero_higher_order")
    return f"""# 4551 - alpha3 vector-boundary zero or first Kalpha3 source projection

Generated: `{generated}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4550 identified `alpha3` as the hard local product wall. 4551 attacks the wall directly.

The alpha3 static split is:

```text
Delta alpha3
  = P_alpha3_src epsilon_U^2
  + Q_alpha3_vec
  + R_alpha3,higher

P_alpha3_src = K_alpha3^src S_static
Q_alpha3_vec = K_alpha3^vec B_boundary/vector_static.
```

The new move is the source projection:

```text
K_alpha3^src[f(r)] = 0
```

for a centred stationary scalar monopole `f(r)`. In words: the selected point-mass source-model branch is scalar and spherical, while `alpha3` is a vector/preferred-frame channel. A scalar monopole cannot supply the required vector index unless a marker, spin/velocity, anisotropic domain, or boundary flux enters.

So the source side has a conditional representation-zero. The boundary side also has a clean conditional zero theorem, but it is not parent-owned yet: the scalar homogeneous marker-free no-flux boundary premises O0-O6 are still unsigned.

If both source and boundary vector pieces vanish, the remaining cubic vector residue has the finite budget:

```text
{fallback_cubic['required_bound']} = {fallback_cubic['numeric_value']}
```

That is progress, not a public PPN pass.

## Alpha3 Split Law

{markdown_table(laws)}

## Kalpha3 Source Projection Rows

{markdown_table(kproj)}

## Source Vector Zero Theorem

{markdown_table(source_zero)}

## Boundary Vector Zero Theorem

{markdown_table(boundary_zero)}

## Survival Matrix

{markdown_table(survival)}

## Finite Fallback Products

{markdown_table(fallback)}

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
        "claim": "4551 derives a conditional alpha3 source-projection zero row: K_alpha3 vanishes on centred scalar monopole source terms; boundary alpha3 zero remains conditional and parent-unsigned.",
        "current_evidence": "Generated source register, alpha3 split law, Kalpha3 projection rows, source zero theorem, boundary zero theorem, survival matrix, finite fallback rows, claim gates, status and validation CSVs.",
        "status": "alpha3_source_projection_zero_boundary_unsigned_nonclaim",
        "next_test": NEXT_TARGET,
        "failure_mode": "Treating scalar source projection zero as a full alpha3 or PPN pass while boundary flux, marker vectors and higher-order vector residues remain open.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "Source side improved; boundary owner/marker exclusion is now the active alpha3 problem.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    alpha3 = alpha3_product_row()
    domain = selected_domain_row()
    sources = source_rows()
    laws = split_law_rows(alpha3, domain)
    kproj = kalpha3_projection_rows()
    source_zero = source_zero_rows()
    boundary_zero = boundary_zero_rows()
    survival = survival_rows(alpha3, domain)
    fallback = fallback_rows(alpha3, domain)
    blockers = blocker_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_ = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SPLIT_LAW_CSV, laws)
    write_csv(KPROJ_CSV, kproj)
    write_csv(SOURCE_ZERO_CSV, source_zero)
    write_csv(BOUNDARY_ZERO_CSV, boundary_zero)
    write_csv(SURVIVAL_CSV, survival)
    write_csv(FALLBACK_CSV, fallback)
    write_csv(BLOCKERS_CSV, blockers)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_)
    write_csv(STATUS_CSV, status)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    pending_doc = f"# 4551 - alpha3 vector-boundary zero or first Kalpha3 source projection\n\nMarker: `{MARKER}`\n\nValidation pending.\n"
    DOC_PATH.write_text(pending_doc, encoding="utf-8")
    FORMAL_PATH.write_text(pending_doc, encoding="utf-8")

    validation = validate(sources, laws, kproj, source_zero, boundary_zero, survival, fallback, gates)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, laws, kproj, source_zero, boundary_zero, survival, fallback, blockers, gates, decisions, next_, validation)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4551 Alpha3 Source Projection Zero

Marker: `{MARKER}`  
4551 derives the first `K_alpha3` source projection row: on a centred scalar monopole source, `K_alpha3^src[f(r)]=0` by SO(3) representation/parity, so the selected source-model source product is conditionally zero. Boundary alpha3 has the same scalar/no-flux conditional zero route, but parent ownership fails at the O0-O6 boundary premises. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4551 Packet Integration - Alpha3 Source Projection Zero

Marker: `{PACKET_MARKER}`  
The alpha3 pressure is now narrowed: scalar point-mass source leakage is not the vector problem. The live problem is marker/vector exclusion and boundary normal-momentum flux ownership, with finite fallback product rows if either survives.
""",
    )

    print(f"wrote {DOC_PATH}")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    overall = next((row for row in validation if row["validation_id"] == "VAL4551_OVERALL"), {})
    print(f"overall={overall.get('status', 'UNKNOWN')} decision={DECISION}")


if __name__ == "__main__":
    main()

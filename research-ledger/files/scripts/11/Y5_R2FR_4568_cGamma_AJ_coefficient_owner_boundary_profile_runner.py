from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4568"
CLAIM_ID = "L-410"
BRANCH_ID = "MTS_R2FR_Y5_CGAMMA_AJ_OWNER_PROFILE_RUNNER_4568"
MARKER = "PPC4161_CGAMMA_AJ_COEFFICIENT_OWNER_BOUNDARY_PROFILE_RUNNER_4568"
PACKET_MARKER = "PPC4161_PACKET_CGAMMA_AJ_OWNER_PROFILE_RUNNER_4568"
DECISION = "AJ_EFF_OWNER_LAW_AND_PROFILE_RUNNER_WRITTEN_PARENT_NUMERIC_INPUTS_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4569-Y5-R2FR-parent-source-current-covariance-or-A_src-zero-source-norm-row.md"

FORMAL_PATH = FORMAL / "584-PPC4161-cGamma-AJ-coefficient-owner-boundary-profile-runner.md"
DOC_PATH = POST / "4568-Y5-R2FR-cGamma-AJ-coefficient-owner-boundary-profile-runner.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4567 = FORMAL / "583-PPC4161-cGamma-static-source-homogeneity-and-boundary-amplitude-zero-or-AJ-profile-row.md"
CSV_4567_NORMAL = SOURCE_DIR / "P8_Y5_R2FR_4567_AJ_PROFILE_NORMAL_FORM.csv"
CSV_4567_REQ = SOURCE_DIR / "P8_Y5_R2FR_4567_AJ_PROFILE_REQUIREMENT_ROWS.csv"
CSV_4567_BOUNDARY = SOURCE_DIR / "P8_Y5_R2FR_4567_BOUNDARY_AMPLITUDE_LEDGER.csv"
CSV_4546_INPUTS = SOURCE_DIR / "P8_Y5_R2FR_4546_INPUT_REQUIREMENTS.csv"
CSV_4546_UB2 = SOURCE_DIR / "P8_Y5_R2FR_4546_UB2_STATIC_BOUND_THEOREM.csv"
CSV_4546_ML = SOURCE_DIR / "P8_Y5_R2FR_4546_ML_HOMOGENEITY_BOUND.csv"
CSV_4547_ACQ = SOURCE_DIR / "P8_Y5_R2FR_4547_INPUT_ACQUISITION_QUEUE.csv"
CSV_4550_PRODUCT_LAW = SOURCE_DIR / "P8_Y5_R2FR_4550_STATIC_PRODUCT_BOUND_LAW.csv"
CSV_4550_PRODUCTS = SOURCE_DIR / "P8_Y5_R2FR_4550_OBSERVABLE_PRODUCT_BOUNDS.csv"
CSV_4550_SELECTED = SOURCE_DIR / "P8_Y5_R2FR_4550_SELECTED_DOMAIN_EPSILON.csv"
CSV_4551_ALPHA3 = SOURCE_DIR / "P8_Y5_R2FR_4551_KALPHA3_SOURCE_PROJECTION_ROWS.csv"
CSV_4555_RANKING = SOURCE_DIR / "P8_Y5_R2FR_4555_ACTIVE_PRODUCT_PRESSURE_RANKING.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4568_SOURCE_REGISTER.csv"
OWNER_LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4568_AJ_COEFFICIENT_OWNER_LAW.csv"
ZERO_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4568_AJ_ZERO_ROUTE_AUDIT.csv"
PROFILE_RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4568_AJ_PROFILE_RUNNER_ROWS.csv"
BOUNDARY_INTERFACE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4568_BOUNDARY_PROFILE_INTERFACE.csv"
ACQUISITION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4568_NEXT_INPUT_ACQUISITION_QUEUE.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4568_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4568_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4568_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4568_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4568_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


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


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
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
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4568_00_4567_doc", "4567 AJ profile law", DOC_4567, "A_J_eff := A_src + A_lap"),
        ("SRC4568_01_4567_normal", "4567 AJ normal form", CSV_4567_NORMAL, "AJ4567_5_static_residual_law"),
        ("SRC4568_02_4567_req", "4567 profile requirements", CSV_4567_REQ, "AR4567_3_arena_static_general"),
        ("SRC4568_03_4567_boundary", "4567 boundary ledger", CSV_4567_BOUNDARY, "B4567_1_static_trace_vector_shear"),
        ("SRC4568_04_4546_inputs", "4546 input requirements", CSV_4546_INPUTS, "REQ4546_1_source_norm"),
        ("SRC4568_05_4546_UB2", "4546 source U_B2 theorem", CSV_4546_UB2, "UB24546_1_linear_silence"),
        ("SRC4568_06_4546_mL", "4546 mL homogeneity theorem", CSV_4546_ML, "ML4546_2_laplacian"),
        ("SRC4568_07_4547_acq", "4547 acquisition queue", CSV_4547_ACQ, "ACQ4547_4_projection_kernel"),
        ("SRC4568_08_4550_law", "4550 static product law", CSV_4550_PRODUCT_LAW, "LAW4550_0_static_product_identity"),
        ("SRC4568_09_4550_products", "4550 observable product bounds", CSV_4550_PRODUCTS, "PB4550_xi"),
        ("SRC4568_10_4550_domain", "4550 selected epsilon domain", CSV_4550_SELECTED, "SEL4550_0"),
        ("SRC4568_11_4551_alpha3", "4551 alpha3 source projection", CSV_4551_ALPHA3, "K_alpha3"),
        ("SRC4568_12_4555_ranking", "4555 active product ranking", CSV_4555_RANKING, "xi"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needle": needle,
                "needle_found": b(needle in text),
                "role": "4568 AJ coefficient owner/profile-runner bridge",
                "valid_for_claim": "False",
            }
        )
    return rows


def owner_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "owner_id": "OWN4568_0_A_src",
            "coefficient": "A_src",
            "owner_formula": "A_src := ||P_loc[H_L (D_{D_L} S_cg)|_{D_L=0}]|| <= C_H A_1",
            "derivation": "From S_cg(D_L,Y)=D_L S_1(Y)+O(D_L^2), D_L=U_B H_L; hence P_loc[U_B S_cg]=U_B^2 P_loc[H_L S_1]+O(U_B^3).",
            "owned_by": "parent source-current covariance plus leakage-coordinate norm",
            "closure_route": "A_src=0 if the parent proves S_1=0, H_L=0 on the local collar, or P_loc[H_L S_1]=0 by source-kernel symmetry",
            "current_status": "FORMULA_DERIVED_NUMERIC_VALUE_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "owner_id": "OWN4568_1_A_lap",
            "coefficient": "A_lap",
            "owner_formula": "A_lap := D_m C_lap_m/L_B^2",
            "derivation": "From m_L=m_*+D_L^2 m_2+O(D_L^3) with far-local derivative scale L_B, |D_m Delta_h m_L| <= U_B^2 D_m C_lap_m/L_B^2.",
            "owned_by": "parent m_L attractor equation, diffusion coefficient D_m, and far-local length/regularity scale",
            "closure_route": "A_lap=0 if m_2 is constant/harmonic on the collar, D_m=0 in the local branch, or parent attractor homogeneity forces Delta_h m_L=0",
            "current_status": "FORMULA_DERIVED_NUMERIC_VALUE_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "owner_id": "OWN4568_2_A_drift",
            "coefficient": "A_drift",
            "owner_formula": "A_drift=0 on the stationary compact branch",
            "derivation": "4566/4545 stationarity gives D_t Xi_0=0 and derivative drift silence under conserved local invariants, scalar boundary charges, and no incoming homogeneous/kernel mode.",
            "owned_by": "Hamiltonian stationarity and no-incoming-kernel branch premises",
            "closure_route": "off-branch systems must reintroduce A_drift or a D_t B_static product row",
            "current_status": "PASS_CONDITIONAL_STATIONARY_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "owner_id": "OWN4568_3_B_boundary_static",
            "coefficient": "B_boundary_static",
            "owner_formula": "B_boundary,a := ||K_a P_loc boundary_in_static||",
            "derivation": "Boundary terms are not multiplied by the same U_B^2 bulk law unless a compact no-flux/no-incoming collar or channel projection theorem owns them.",
            "owned_by": "boundary action, symplectic flux/no-influx condition, and arena projection kernel K_a",
            "closure_route": "B_boundary,a=0 only for parent-signed no-hair/no-influx or channel-specific projection silence",
            "current_status": "RETAINED_BOUNDARY_PROFILE_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "owner_id": "OWN4568_4_A_J_eff",
            "coefficient": "A_J_eff",
            "owner_formula": "A_J_eff := A_src + A_lap on the stationary compact branch",
            "derivation": "4567 law plus 4550 identity: S_static=C_H A_1 + D_m C_lap_m/L_B^2 is exactly A_src + A_lap.",
            "owned_by": "source-current owner plus m_L-attractor owner; no independent fudge coefficient allowed",
            "closure_route": "A_J_eff=0 only if both A_src=0 and A_lap=0 on the same branch, with no cancellation credit",
            "current_status": "OWNER_SPLIT_WRITTEN_VALUES_UNSIGNED",
            "valid_for_claim": "False",
        },
    ]


def zero_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "ZR4568_0_source_kernel",
            "target": "A_src=0",
            "proof_attempt": "Differentiate parent source current with respect to leakage distance at D_L=0; show the derivative is q-vertical/projector-silent.",
            "success_condition": "(D_{D_L} S_cg)|0 = 0 or P_loc[H_L (D_{D_L} S_cg)|0]=0",
            "current_result": "OPEN_PARENT_SOURCE_COVARIANCE",
            "why_not_closed": "current corpus has the regular expansion and U_B^2 bound, not a parent theorem killing the first derivative",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "False",
        },
        {
            "route_id": "ZR4568_1_attractor_homogeneity",
            "target": "A_lap=0",
            "proof_attempt": "Use parent m_L equation to show the local fixed branch is spatially constant/harmonic on the readout collar.",
            "success_condition": "Delta_h m_L=0 or C_lap_m=0 on D_loc",
            "current_result": "OPEN_PARENT_ATTRACTOR_EQUATION",
            "why_not_closed": "4546 supplies a second-derivative envelope but not the parent equation that forces the envelope coefficient to zero",
            "next_action": "4570-Y5-R2FR-parent-mL-attractor-equation-or-A_lap-source-row.md",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ZR4568_2_boundary_nohair",
            "target": "B_boundary,a=0",
            "proof_attempt": "Use compact no-flux/no-incoming collar to erase static trace/vector/shear boundary projections.",
            "success_condition": "K_a P_loc boundary_in_static=0 for each arena from the same boundary theorem",
            "current_result": "CONDITIONAL_PRIVATE_COLLAR_GLOBAL_UNSIGNED",
            "why_not_closed": "private collar silence exists as a route, but global/open/radiative sectors still need explicit boundary rows",
            "next_action": "4571-Y5-R2FR-boundary-nohair-profile-row-or-channel-bound-runner.md",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ZR4568_3_no_cancellation",
            "target": "observable pass",
            "proof_attempt": "Demand |K_a A_J_eff| epsilon_U^2 + |B_boundary,a| + |R_higher,a| <= B_a with no cancellation credit.",
            "success_condition": "each term independently below its allocated bound or theorem-zero",
            "current_result": "RUNNER_SCHEMA_READY_INPUTS_MISSING",
            "why_not_closed": "A_src/A_lap values, K_a kernels and boundary rows are still symbolic",
            "next_action": "fill owner/source rows before using runner for claims",
            "valid_for_claim": "False",
        },
    ]


def profile_runner_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in read_csv(CSV_4550_PRODUCTS):
        product_id = source.get("product_id", "")
        observable = source.get("observable", "")
        rows.append(
            {
                "runner_id": f"RUN4568_{product_id}" if product_id else f"RUN4568_{len(rows)}",
                "source_product_id": product_id,
                "arena": source.get("arena", ""),
                "observable": observable,
                "epsilon_U_squared": source.get("epsilon_U_squared", ""),
                "AJ_product_symbol": source.get("product_symbol", "").replace("S_static", "A_J_eff"),
                "boundary_symbol": source.get("boundary_symbol", ""),
                "no_cancellation_test": source.get("exact_no_cancellation_condition", "").replace("S_static", "A_J_eff"),
                "max_AJ_product_if_boundary_and_higher_zero": source.get("max_product_if_boundary_and_higher_zero", ""),
                "half_budget_AJ_product": source.get("max_product_equal_half_budget", ""),
                "half_budget_boundary_plus_higher": source.get("max_boundary_plus_higher_equal_half_budget", ""),
                "runner_status": "SCHEMA_READY_INPUTS_MISSING",
                "required_inputs": "A_src, A_lap, K_a, B_boundary_a, R_higher_a",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    if not rows:
        rows.append(
            {
                "runner_id": "RUN4568_NO_4550_PRODUCTS",
                "source_product_id": "missing",
                "arena": "missing",
                "observable": "missing",
                "epsilon_U_squared": "missing",
                "AJ_product_symbol": "missing",
                "boundary_symbol": "missing",
                "no_cancellation_test": "missing 4550 observable product bounds",
                "max_AJ_product_if_boundary_and_higher_zero": "missing",
                "half_budget_AJ_product": "missing",
                "half_budget_boundary_plus_higher": "missing",
                "runner_status": "FAIL_SOURCE_TABLE_MISSING",
                "required_inputs": "restore P8_Y5_R2FR_4550_OBSERVABLE_PRODUCT_BOUNDS.csv",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def boundary_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "interface_id": "BI4568_0_scalar_bulk_not_boundary",
            "statement": "A_J_eff owns only the U_B^2 bulk source and m_L terms; it does not absorb static boundary hair.",
            "formula": "B_static,a <= epsilon_U^2 A_J_eff + B_boundary,a + R_higher,a",
            "status": "SEPARATION_ENFORCED",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "BI4568_1_private_compact_zero",
            "statement": "In the private compact no-flux/no-incoming selector, B_boundary,a may be set to zero only if the same collar theorem covers the arena projection.",
            "formula": "K_a P_loc boundary_in_static=0",
            "status": "CONDITIONAL_PRIVATE_ROUTE",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "BI4568_2_open_sector_bound",
            "statement": "For open, radiative, rotating or off-centre systems, B_boundary,a must be carried as a separate finite product row.",
            "formula": "|B_boundary,a| <= B_a - epsilon_U^2 |K_a A_J_eff| - |R_higher,a|",
            "status": "BOUND_ROW_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "BI4568_3_no_retuning",
            "statement": "The same A_src/A_lap/worldtube profile must feed PPN, R10, clocks and orbital tests; no per-arena retuning of A_J_eff.",
            "formula": "A_J_eff is shared; only K_a and B_boundary,a are arena-specific projections",
            "status": "NO_RETUNING_CONTRACT",
            "valid_for_claim": "False",
        },
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "ACQ4568_0_A_src_zero_or_value",
            "input": "A_src = ||P_loc[H_L (D_{D_L} S_cg)|0]||",
            "derive_first": "prove parent source-current derivative is projector-silent on the local collar",
            "fallback": "source C_H A_1 as a nonclaim numeric/profile row",
            "priority": "highest",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "ACQ4568_1_A_lap_zero_or_value",
            "input": "A_lap = D_m C_lap_m/L_B^2",
            "derive_first": "derive parent m_L attractor homogeneity or harmonicity",
            "fallback": "source D_m, C_lap_m and L_B as nonclaim numeric/profile rows",
            "priority": "high",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "ACQ4568_2_boundary_profile",
            "input": "B_boundary,a",
            "derive_first": "parent no-hair/no-influx theorem covering scalar, vector and shear boundary projections",
            "fallback": "finite channel-specific boundary rows with no-cancellation accounting",
            "priority": "high",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "ACQ4568_3_projection_kernels",
            "input": "K_a for xi, alpha3, zeta3, orbital, R10, clock",
            "derive_first": "shared worldtube/profile projection from the same local readout map",
            "fallback": "schema-only runner remains nonclaim until kernels are supplied",
            "priority": "medium",
            "valid_for_claim": "False",
        },
    ]


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G4568_0_owner_split",
            "requirement": "A_J_eff split into source and m_L owners",
            "status": "PASS_FORMULA_DERIVED",
            "claim_effect": "no independent tuning coefficient remains hidden in A_J_eff",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4568_1_static_product_bridge",
            "requirement": "4550 S_static budgets mapped to A_J_eff budgets",
            "status": "PASS_RUNNER_SCHEMA_WRITTEN",
            "claim_effect": "old product-bound machinery now targets the new coefficient law",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4568_2_numeric_inputs",
            "requirement": "A_src/A_lap/K_a/B_boundary values or zeros",
            "status": "FAIL_INPUTS_UNSIGNED",
            "claim_effect": "runner cannot certify PPN/R10/local-GR pass",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4568_3_boundary_firewall",
            "requirement": "boundary not absorbed into bulk coefficient",
            "status": "PASS_FIREWALL",
            "claim_effect": "prevents smuggled boundary cancellation",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4568_4_next_selection",
            "requirement": "choose first coefficient to derive",
            "status": "PASS_NEXT_SELECTED",
            "claim_effect": "next route targets A_src parent source-current covariance",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4568_0",
            "decision": DECISION,
            "meaning": "4568 converts A_J_eff from a label into owned pieces: A_src from the source-current derivative, A_lap from the m_L attractor Laplacian, and B_boundary_static as a separate boundary profile. It also maps the 4550 product bounds onto A_J_eff without allowing claims.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4568_0",
            "next_target": NEXT_TARGET,
            "objective": "try to prove A_src=0, or derive a source-normalized A_src row, from parent source-current covariance",
            "derive_first": "show (D_{D_L} S_cg)|0 is q-vertical/projector-silent under the MTS source grammar",
            "fallback": "keep A_src finite and fill a nonclaim C_H A_1 source-norm row",
            "avoid": "using A_J_eff as a free fit or hiding boundary terms inside A_src",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT,
            "result": DECISION,
            "A_src_owner_formula_written": "True",
            "A_lap_owner_formula_written": "True",
            "boundary_profile_separated": "True",
            "profile_runner_rows_written": "True",
            "numeric_AJ_values_available": "False",
            "public_local_GR_claim_allowed": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    owners: list[dict[str, Any]],
    zero_routes: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    rows.append({"validation_id": "VAL4568_0_sources", "check": "all source paths and needles validate", "status": "PASS" if source_ok else "FAIL", "details": f"{len(sources)} sources"})

    owner_text = "\n".join(str(value) for row in owners for value in row.values())
    owner_ok = all(token in owner_text for token in ["A_src", "D_{D_L} S_cg", "A_lap", "D_m C_lap_m/L_B^2", "A_J_eff := A_src + A_lap"])
    owner_ok = owner_ok and all(row["valid_for_claim"] == "False" for row in owners)
    rows.append({"validation_id": "VAL4568_1_owner_law", "check": "A_src/A_lap/AJ owner laws are written", "status": "PASS" if owner_ok else "FAIL", "details": f"{len(owners)} owner rows"})

    zero_text = "\n".join(str(value) for row in zero_routes for value in row.values())
    zero_ok = all(token in zero_text for token in ["OPEN_PARENT_SOURCE_COVARIANCE", "OPEN_PARENT_ATTRACTOR_EQUATION", "CONDITIONAL_PRIVATE_COLLAR_GLOBAL_UNSIGNED", "RUNNER_SCHEMA_READY_INPUTS_MISSING"])
    rows.append({"validation_id": "VAL4568_2_zero_routes", "check": "zero routes are explicit and not overclaimed", "status": "PASS" if zero_ok else "FAIL", "details": f"{len(zero_routes)} zero-route rows"})

    runner_text = "\n".join(str(value) for row in runner for value in row.values())
    runner_ok = "A_J_eff" in runner_text and "SCHEMA_READY_INPUTS_MISSING" in runner_text and len(runner) >= 5
    runner_ok = runner_ok and all(row["valid_for_claim"] == "False" for row in runner)
    rows.append({"validation_id": "VAL4568_3_profile_runner", "check": "4550 observable product budgets mapped to A_J_eff", "status": "PASS" if runner_ok else "FAIL", "details": f"{len(runner)} runner rows"})

    boundary_text = "\n".join(str(value) for row in boundary for value in row.values())
    boundary_ok = all(token in boundary_text for token in ["SEPARATION_ENFORCED", "CONDITIONAL_PRIVATE_ROUTE", "BOUND_ROW_REQUIRED", "NO_RETUNING_CONTRACT"])
    rows.append({"validation_id": "VAL4568_4_boundary_interface", "check": "boundary/profile separation and no-retuning contract are present", "status": "PASS" if boundary_ok else "FAIL", "details": f"{len(boundary)} boundary rows"})

    acquisition_text = "\n".join(str(value) for row in acquisition for value in row.values())
    acquisition_ok = all(token in acquisition_text for token in ["A_src", "A_lap", "B_boundary", "K_a"])
    rows.append({"validation_id": "VAL4568_5_acquisition_queue", "check": "next input acquisition queue targets owned pieces", "status": "PASS" if acquisition_ok else "FAIL", "details": f"{len(acquisition)} acquisition rows"})

    gates_text = "\n".join(str(value) for row in gates for value in row.values())
    gates_ok = all(token in gates_text for token in ["PASS_FORMULA_DERIVED", "PASS_RUNNER_SCHEMA_WRITTEN", "FAIL_INPUTS_UNSIGNED", "PASS_FIREWALL", "PASS_NEXT_SELECTED"])
    rows.append({"validation_id": "VAL4568_6_gates", "check": "gates move branch forward without claim", "status": "PASS" if gates_ok else "FAIL", "details": f"{len(gates)} gates"})

    decision_ok = decision and decision[0]["decision"] == DECISION and decision[0]["valid_for_claim"] == "False"
    next_ok = next_target and next_target[0]["next_target"] == NEXT_TARGET
    status_ok = status and status[0]["profile_runner_rows_written"] == "True" and status[0]["public_local_GR_claim_allowed"] == "False"
    rows.append({"validation_id": "VAL4568_7_decision_status", "check": "decision/status select A_src source-current target", "status": "PASS" if decision_ok and next_ok and status_ok else "FAIL", "details": NEXT_TARGET})

    csv_files = [
        SOURCE_REGISTER,
        OWNER_LAW_CSV,
        ZERO_AUDIT_CSV,
        PROFILE_RUNNER_CSV,
        BOUNDARY_INTERFACE_CSV,
        ACQUISITION_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
    ]
    csv_ok = True
    parsed_counts: list[str] = []
    for path in csv_files:
        try:
            with path.open("r", encoding="utf-8", newline="") as handle:
                count = sum(1 for _ in csv.DictReader(handle))
            parsed_counts.append(f"{path.name}:{count}")
            csv_ok = csv_ok and count > 0
        except Exception as exc:  # noqa: BLE001
            parsed_counts.append(f"{path.name}:ERR:{exc}")
            csv_ok = False
    rows.append({"validation_id": "VAL4568_8_csv_parse", "check": "generated CSV files parse and have rows", "status": "PASS" if csv_ok else "FAIL", "details": "; ".join(parsed_counts)})

    cache_dir = Path(__file__).resolve().parent / "__pycache__"
    cache_ok = not cache_dir.exists()
    rows.append({"validation_id": "VAL4568_9_pycache_absent", "check": "scripts __pycache__ absent after cleanup", "status": "PASS" if cache_ok else "FAIL", "details": str(cache_dir)})

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"validation_id": "VAL4568_10_overall", "check": "overall 4568 checkpoint validation", "status": "PASS" if overall else "FAIL", "details": "A_J_eff owner law/profile runner complete; numeric inputs unsigned" if overall else "one or more validations failed"})
    return rows


def write_doc(
    path: Path,
    title: str,
    sources: list[dict[str, Any]],
    owners: list[dict[str, Any]],
    zero_routes: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# {title}

Branch: `{BRANCH_ID}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private and nonclaim.

## What Moved

4568 turns `A_J_eff` from a placeholder into an owned coefficient split:

```text
A_src := ||P_loc[H_L (D_D_L S_cg)|_{{D_L=0}}]|| <= C_H A_1
A_lap := D_m C_lap_m/L_B^2
A_J_eff := A_src + A_lap
B_static,a <= epsilon_U^2 A_J_eff + B_boundary,a + R_higher,a.
```

This is not a numerical pass. It is the contract that prevents `A_J_eff` from becoming a free tuning knob. The next real derivation is `A_src`: either prove the parent source-current derivative is projector-silent, or fill a source-normalized nonclaim row.

## Source Register

{markdown_table(sources)}

## Coefficient Owner Law

{markdown_table(owners)}

## Zero Route Audit

{markdown_table(zero_routes)}

## A_J Profile Runner Rows

{markdown_table(runner)}

## Boundary/Profile Interface

{markdown_table(boundary)}

## Next Input Acquisition Queue

{markdown_table(acquisition)}

## Promotion Gates

{markdown_table(gates)}

## Decision

{markdown_table(decision)}

## Next Target

{markdown_table(next_target)}

## Validation

{markdown_table(validation)}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        if text and not text.endswith("\n"):
            handle.write("\n")
        handle.write(block.strip() + "\n")


def append_claim_once() -> None:
    if not CLAIMS_PATH.exists():
        return
    with CLAIMS_PATH.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = []
        fieldnames = [name for name in (reader.fieldnames or []) if name is not None]
        for existing in reader:
            extras = existing.pop(None, None)
            if extras:
                extra_text = " ".join(str(item) for item in extras if item)
                if extra_text:
                    existing["risk"] = " ".join(part for part in [existing.get("risk", ""), extra_text] if part).strip()
                    if "risk" not in fieldnames:
                        fieldnames.append("risk")
            rows.append(existing)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4568 derives the owner split for A_J_eff into A_src and A_lap, keeps B_boundary_static separate, and maps the existing static product runner onto A_J_eff without promoting local-GR/PPN/R10 claims.",
        "current_evidence": "Generated source register, coefficient owner law, zero route audit, profile-runner rows, boundary/profile interface, acquisition queue, promotion gates, status and validation CSVs.",
        "status": "AJ_eff_owner_split_profile_runner_nonclaim_inputs_unsigned",
        "next_test": NEXT_TARGET,
        "key_risk": "Using A_J_eff as a free fit, absorbing boundary terms into the bulk coefficient, or treating schema-ready runner rows as numerical evidence.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "A_src parent source-current covariance, A_lap attractor equation, boundary profiles and K_a kernels still need derivation/source rows.",
    }
    for key in row:
        if key not in fieldnames:
            fieldnames.append(key)
    rows.append(row)
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    cache_dir = Path(__file__).resolve().parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    sources = source_rows()
    owners = owner_law_rows()
    zero_routes = zero_route_rows()
    runner = profile_runner_rows()
    boundary = boundary_interface_rows()
    acquisition = acquisition_rows()
    gates = promotion_rows()
    decision = decision_rows()
    next_target = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(OWNER_LAW_CSV, owners)
    write_csv(ZERO_AUDIT_CSV, zero_routes)
    write_csv(PROFILE_RUNNER_CSV, runner)
    write_csv(BOUNDARY_INTERFACE_CSV, boundary)
    write_csv(ACQUISITION_CSV, acquisition)
    write_csv(PROMOTION_CSV, gates)
    write_csv(DECISION_CSV, decision)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    validation = validate(sources, owners, zero_routes, runner, boundary, acquisition, gates, decision, next_target, status)
    write_csv(VALIDATION_PATH, validation)

    write_doc(
        FORMAL_PATH,
        "4568 - cGamma AJ coefficient owner boundary profile runner",
        sources,
        owners,
        zero_routes,
        runner,
        boundary,
        acquisition,
        gates,
        decision,
        next_target,
        validation,
    )
    write_doc(
        DOC_PATH,
        "4568 - Y5 R2FR cGamma AJ Coefficient Owner Boundary Profile Runner",
        sources,
        owners,
        zero_routes,
        runner,
        boundary,
        acquisition,
        gates,
        decision,
        next_target,
        validation,
    )

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4568 cGamma A_J Owner/Profile Runner

Marker: `{MARKER}`  
`A_J_eff` is no longer an unowned label:

```text
A_src := ||P_loc[H_L (D_D_L S_cg)|_0]|| <= C_H A_1
A_lap := D_m C_lap_m/L_B^2
A_J_eff := A_src + A_lap
B_static,a <= epsilon_U^2 A_J_eff + B_boundary,a + R_higher,a.
```

The 4550 static product budgets now run on `A_J_eff` directly, but all rows remain nonclaim because `A_src`, `A_lap`, `B_boundary,a` and `K_a` are not parent-signed numeric/source rows. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4568 Packet Integration - cGamma A_J Owner/Profile Runner

Marker: `{PACKET_MARKER}`  
Packet rule: `A_J_eff` must be treated as the shared owned coefficient `A_src + A_lap`, not a fit knob. Boundary profiles remain separate from the bulk coefficient. Runner rows are schema-ready only until source-current covariance, m_L attractor rows, boundary rows and projection kernels are supplied. Next target: `{NEXT_TARGET}`.
""",
    )

    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {FORMAL_PATH}")
    print(f"Wrote {VALIDATION_PATH}")
    print(f"Decision: {DECISION}")


if __name__ == "__main__":
    main()

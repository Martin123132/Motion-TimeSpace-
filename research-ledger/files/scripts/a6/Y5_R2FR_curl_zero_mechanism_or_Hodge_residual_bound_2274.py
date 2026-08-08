from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_CURL_ZERO_MECHANISM_OR_HODGE_RESIDUAL_BOUND_2274"
DOC = ROOT / "2274-Y5-R2FR-curl-zero-mechanism-or-Hodge-residual-bound.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2274_00_2273_doc",
        "source_key": "2273_doc",
        "source_path": ROOT / "2273-Y5-R2FR-exact-psi-gradient-lift-curl-smoothing-gate.md",
        "needles": ["COD2273_0_general", "SHP2273_0_hodge_projection", "NEXT2273_0_primary"],
        "role": "handoff: curl obstruction and Hodge residual route selected",
    },
    {
        "source_id": "SRC2274_01_2273_validation",
        "source_key": "2273_validation",
        "source_path": OUT / "P8_Y5_BRR545_2273_VALIDATION.csv",
        "needles": ["VAL2273_OVERALL", "PASS"],
        "role": "confirms 2273 passed before 2274 starts",
    },
    {
        "source_id": "SRC2274_02_2273_exact_equations",
        "source_key": "2273_exact_equations",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2273_EXACT_LIFT_EQUATIONS.csv",
        "needles": ["ELE2273_2_exactness_condition", "Omega_A,mn"],
        "role": "machine-readable exactness equations",
    },
    {
        "source_id": "SRC2274_03_2273_curl",
        "source_key": "2273_curl",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2273_CURL_OBSTRUCTION_DERIVATION.csv",
        "needles": ["COD2273_0_general", "FAILS_GENERALLY"],
        "role": "generic curl obstruction derivation",
    },
    {
        "source_id": "SRC2274_04_2273_projection",
        "source_key": "2273_projection",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2273_SMOOTHING_HODGE_PROJECTION_GATE.csv",
        "needles": ["SHP2273_0_hodge_projection", "BOUND_TEMPLATE_ONLY"],
        "role": "Hodge projection and residual-bound gate",
    },
    {
        "source_id": "SRC2274_05_2272_lift",
        "source_key": "2272_lift",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2272_ALGEBRAIC_COVARIANCE_LIFT.csv",
        "needles": ["ACL2272_1_right_inverse", "deltaU = (1/2) deltaC C^{-1} U"],
        "role": "algebraic right inverse used as alpha before exact projection",
    },
    {
        "source_id": "SRC2274_06_2271_formulas",
        "source_key": "2271_formulas",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2271_COVARIANCE_PULLBACK_FORMULAS.csv",
        "needles": ["PBF2271_1_q_tangent", "PBF2271_3_q_zero_channel_relation"],
        "role": "q tangent and q=0 channel relation",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2274_SOURCE_REGISTER.csv",
    "mechanisms": OUT / "P8_Y5_PARENT_QLOC_2274_CURL_ZERO_MECHANISM_TESTS.csv",
    "diffeo_test": OUT / "P8_Y5_PARENT_QLOC_2274_DIFFEO_LIE_LIFT_TEST.csv",
    "scale_bound": OUT / "P8_Y5_PARENT_QLOC_2274_SCALE_SEPARATED_CURL_BOUND.csv",
    "hodge_bound": OUT / "P8_Y5_PARENT_QLOC_2274_HODGE_RESIDUAL_BOUND_TEMPLATE.csv",
    "qr_intake": OUT / "P8_Y5_PARENT_QLOC_2274_QR_BOUND_INPUT_LEDGER.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2274_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2274_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2274_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2274_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2274_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2274_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_mechanisms": QUEUE / "JR2274_CURL_ZERO_MECHANISM_TESTS_NONCLAIM.csv",
    "queue_bound": QUEUE / "JR2274_HODGE_RESIDUAL_BOUND_TEMPLATE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_curl_zero_mechanism_refusal_2274.csv",
    "beta_docs": BETA_DOCS / "RAB_CURL_ZERO_MECHANISM_2274_NONCLAIM.csv",
}


def stringify(value: Any) -> str:
    if isinstance(value, Path):
        return str(value)
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(value) for key, value in row.items()})


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    def cell(value: Any) -> str:
        return stringify(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path) if path.exists() else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": path,
                "exists": path.exists(),
                "needles": "; ".join(needles),
                "needles_present": all(needle in text for needle in needles),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def mechanism_rows() -> list[dict[str, Any]]:
    return [
        {
            "mechanism_id": "CZM2274_0_constant_affine_cell",
            "candidate": "constant-M affine carrier cell",
            "zero_condition": "partial M=0 and partial_m u_A,r=0 over the coarse cell",
            "derivation": "Omega_A,mn=partial_m(M_n^r u_A,r)-partial_n(M_m^r u_A,r)=0 if both M and the carrier one-forms are constant in the cell.",
            "what_it_buys": "exact curl-zero in an ideal tangent cell",
            "why_not_claim": "real radial q profiles have Phi, deltaq, C, and carrier gradients varying across a finite cell",
            "status": "EXACT_ONLY_IN_IDEAL_TANGENT_CELL",
            "valid_for_claim": False,
        },
        {
            "mechanism_id": "CZM2274_1_carrier_aligned_scaling",
            "candidate": "carrier-aligned scalar scaling",
            "zero_condition": "delta u_A=d zeta_A=f_A(psi_A)d psi_A with zeta_A=F_A(psi_A)",
            "derivation": "d(f_A(psi_A)d psi_A)=f_A'(psi_A)d psi_A wedge d psi_A=0.",
            "what_it_buys": "a genuine exact scalar-field variation for a scaling of each carrier",
            "why_not_claim": "the q tangent is anisotropic in t/r covariance channels and no parent carrier inventory proves it decomposes into these aligned scalings",
            "status": "EXACT_MECHANISM_REQUIRES_UNSOURCED_CARRIER_DECOMPOSITION",
            "valid_for_claim": False,
        },
        {
            "mechanism_id": "CZM2274_2_lie_drag",
            "candidate": "diffeomorphic/Lie-drag lift",
            "zero_condition": "delta u_A=L_xi u_A=d(i_xi u_A) because du_A=0",
            "derivation": "Cartan identity gives L_xi u_A=i_xi du_A+d(i_xi u_A)=d(i_xi u_A).",
            "what_it_buys": "an exact lift generated by a vector field xi",
            "why_not_claim": "its covariance variation is L_xi C, which is gauge/readout-like and does not automatically equal the physical q tangent in areal gauge",
            "status": "EXACT_LIFT_BUT_Q_MATCH_AND_GAUGE_STATUS_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "mechanism_id": "CZM2274_3_hodge_projection",
            "candidate": "Hodge exact projection",
            "zero_condition": "replace alpha_A=delta u_A^alg by d zeta_A=P_exact alpha_A",
            "derivation": "the exact projection is curl-free by construction; the rejected coexact part rho_A=alpha_A-d zeta_A carries the obstruction",
            "what_it_buys": "a lawful psi variation plus an explicit residual to bound",
            "why_not_claim": "the current corpus does not source cell geometry, kernel, norm, carrier amplitudes, or the induced q_R map",
            "status": "BEST_NONCLAIM_BACKSTOP",
            "valid_for_claim": False,
        },
    ]


def diffeo_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "DLT2274_0_exact_lift_identity",
            "object": "Lie-dragged carrier one-form",
            "formula": "delta u_A=L_xi u_A=d(i_xi u_A)",
            "interpretation": "This is a real exact psi-gradient lift candidate.",
            "blocker": "It may be pure gauge/readout deformation rather than a physical q mode.",
            "valid_for_claim": False,
        },
        {
            "test_id": "DLT2274_1_radial_static_match",
            "object": "static radial covariance tensor",
            "formula": "deltaC_tt=xi C_tt'; deltaC_rr=xi C_rr'+2 C_rr xi'",
            "interpretation": "A radial diffeo can generate paired tt/rr covariance changes.",
            "blocker": "q-target requires deltaC_tt=-(A/2)deltaq and deltaC_rr=(B/2)deltaq, giving a nontrivial xi ODE.",
            "valid_for_claim": False,
        },
        {
            "test_id": "DLT2274_2_q_target_ode",
            "object": "q tangent matching condition",
            "formula": "from deltaC_tt: deltaq=-2 xi C_tt'/A; then rr requires -B xi C_tt'/A=xi C_rr'+2 C_rr xi'",
            "interpretation": "q-match is not automatic; it is a sourced differential constraint on xi and the background.",
            "blocker": "no parent source proves the ODE, and areal gauge fixes angular radius so radial diffeo is not freely physical",
            "valid_for_claim": False,
        },
        {
            "test_id": "DLT2274_3_areal_gauge_guard",
            "object": "areal radial gauge",
            "formula": "L_xi(r^2 dOmega^2)=2 r xi^r dOmega^2",
            "interpretation": "a radial diffeo changes the angular sector unless compensated by gauge/readout reset",
            "blocker": "local GR claim cannot be built by smuggling a coordinate transformation into a physical q suppression theorem",
            "valid_for_claim": False,
        },
    ]


def scale_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "SSB2274_0_curl_size",
            "quantity": "curl obstruction scale",
            "bound": "||Omega|| <= K1 ||alpha||/L_cg if M and u vary on macro scale L_cg",
            "derivation": "Omega contains derivative-of-M and derivative-of-u terms; each contributes order one macro derivative times alpha.",
            "required_inputs": "K1, coarse-cell norm, macro variation length L_cg, carrier amplitudes",
            "status": "DIMENSIONAL_BOUND_TEMPLATE",
            "valid_for_claim": False,
        },
        {
            "bound_id": "SSB2274_1_hodge_residual",
            "quantity": "coexact residual fraction",
            "bound": "epsilon_curl=||rho||/||alpha|| <= K2 ell_cg/L_cg",
            "derivation": "Poincare/Hodge estimate on a cell: residual one-form is bounded by cell size times curl norm.",
            "required_inputs": "K2, ell_cg, boundary conditions, Hodge domain, smoothing kernel",
            "status": "PROMISING_SCALE_SEPARATION_BACKSTOP",
            "valid_for_claim": False,
        },
        {
            "bound_id": "SSB2274_2_q_residual",
            "quantity": "induced q residual",
            "bound": "|q_R| <= Kq epsilon_curl |deltaq_alg| plus projection/source terms",
            "derivation": "the q-channel residual is a linear readout of deltaC_res=<rho u+u rho>_smooth at first order",
            "required_inputs": "Kq, q readout map, arena scale, deltaq_alg normalization",
            "status": "NOT_SCORE_READY",
            "valid_for_claim": False,
        },
    ]


def hodge_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "template_id": "HBT2274_0_exact_projection_problem",
            "target": "find zeta_A",
            "equation": "zeta_A=argmin_z ||d z-alpha_A||^2_cell",
            "outputs_needed": "d zeta_A; rho_A=alpha_A-d zeta_A; epsilon_curl",
            "claim_gate": "epsilon_curl sourced and induced q_R below local bounds",
            "status": "TEMPLATE_ONLY",
            "valid_for_claim": False,
        },
        {
            "template_id": "HBT2274_1_parent_zero_theorem",
            "target": "rho channel silence",
            "equation": "<rho_A u_A+u_A rho_A>_smooth projected to q = 0",
            "outputs_needed": "kernel symmetry; phase average; boundary theorem",
            "claim_gate": "parent-signed zero theorem",
            "status": "UNSIGNED_ZERO_ROUTE",
            "valid_for_claim": False,
        },
        {
            "template_id": "HBT2274_2_finite_bound_route",
            "target": "finite q_R",
            "equation": "q_R <= Kq K2 (ell_cg/L_cg) |deltaq_alg|",
            "outputs_needed": "ell_cg, L_cg, K2, Kq, local-test tolerance",
            "claim_gate": "all constants sourced; no fitted cancellation; arena-specific residual vector computed",
            "status": "BOUND_INPUTS_MISSING",
            "valid_for_claim": False,
        },
    ]


def qr_intake_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "QBI2274_0_ell_cg",
            "quantity": "ell_cg",
            "meaning": "coarse-graining/smoothing cell scale",
            "required_source": "parent smoothing kernel or explicit microscopic averaging scale",
            "current_value": "MISSING_PARENT_SMOOTHING_SCALE",
            "units": "length",
            "status": "missing",
            "valid_for_claim": False,
        },
        {
            "input_id": "QBI2274_1_L_cg",
            "quantity": "L_cg",
            "meaning": "macro variation length for C, Phi, and deltaq in the local arena",
            "required_source": "arena geometry or parent field profile",
            "current_value": "MISSING_MACRO_VARIATION_LENGTH",
            "units": "length",
            "status": "missing",
            "valid_for_claim": False,
        },
        {
            "input_id": "QBI2274_2_Kq",
            "quantity": "Kq",
            "meaning": "operator norm from residual covariance to q_R/PPN readout",
            "required_source": "q readout map and local PPN projection",
            "current_value": "MISSING_Q_READOUT_NORM",
            "units": "dimensionless",
            "status": "missing",
            "valid_for_claim": False,
        },
        {
            "input_id": "QBI2274_3_tolerance",
            "quantity": "arena_tolerance",
            "meaning": "R10/PPN/clock/orbital allowed q residual",
            "required_source": "test-specific bound table",
            "current_value": "MISSING_ARENA_BOUND",
            "units": "dimensionless or arena-specific",
            "status": "missing",
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2274_0_exact_zero_claim",
            "attempted_claim": "The curl obstruction is solved exactly for the physical q tangent.",
            "runner_result": "BLOCKED",
            "blocked_by": "exact mechanisms are either ideal-cell, carrier-decomposition, or diffeo/gauge conditional",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2274_1_hodge_bound_claim",
            "attempted_claim": "The Hodge residual is small enough for local tests.",
            "runner_result": "BLOCKED",
            "blocked_by": "ell_cg/L_cg, kernel, Kq, and local tolerance are missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2274_2_local_gr_claim",
            "attempted_claim": "MTS has now derived the local GR limit.",
            "runner_result": "BLOCKED",
            "blocked_by": "no exact q=0 protection theorem and no finite q_R score row",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2274_0_exact_mechanism_exists",
            "claim": "mathematical mechanisms exist that make Omega=0 under strict conditions",
            "gate_pass": True,
            "reason": "constant/affine, carrier-aligned, and Lie-drag cases are exact under their own hypotheses",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2274_1_physical_q_zero",
            "claim": "physical q tangent has Omega=0 in the parent theory",
            "gate_pass": False,
            "reason": "no parent carrier inventory, gauge status, or kernel theorem selects the q tangent",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2274_2_scale_bound",
            "claim": "curl residual is bounded by ell_cg/L_cg below local-test limits",
            "gate_pass": False,
            "reason": "scale constants and local readout norm are missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2274_3_local_GR",
            "claim": "derived local GR limit",
            "gate_pass": False,
            "reason": "exact q protection or sourced finite q_R bound remains absent",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2274_0_gain",
            "decision": "CURL_ZERO_MECHANISMS_IDENTIFIED",
            "reason": "There are real mathematical routes to Omega=0, but each requires extra parent structure.",
            "next_action": "Do not call the local branch derived until the extra structure is sourced.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2274_1_best_route",
            "decision": "HODGE_SCALE_BOUND_IS_BEST_BACKSTOP",
            "reason": "Even if exact zero fails, scale separation can convert the obstruction into a bounded q_R input.",
            "next_action": "Source ell_cg, L_cg, Kq, and arena tolerances.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2274_2_derivation_route",
            "decision": "CARRIER_INVENTORY_IS_THE_BEST_DERIVATION_TARGET",
            "reason": "The carrier-aligned scaling mechanism is exact, but only if the parent psi ensemble decomposes the q channel cleanly.",
            "next_action": "Try to construct the minimal carrier inventory that realizes q without curl.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2274_3_next",
            "decision": "MINIMAL_CARRIER_INVENTORY_OR_SCALE_BOUND_NEXT",
            "reason": "This is the least hand-wavy way forward: either derive the carrier split or quantify the residual.",
            "next_action": "2275-Y5-R2FR-minimal-carrier-inventory-or-scale-separated-qR-bound.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2274_0_primary",
            "next_target": "2275-Y5-R2FR-minimal-carrier-inventory-or-scale-separated-qR-bound.md",
            "script": "scripts/Y5_R2FR_minimal_carrier_inventory_or_scale_separated_qR_bound_2275.py",
            "objective": "try to build a parent carrier inventory that realizes the q tangent by exact carrier-aligned scalings; if not, turn ell_cg/L_cg into a finite q_R residual-bound intake",
            "selection_status": "selected",
            "success_condition": "either a curl-free q carrier split is parent-signed, or the Hodge residual is bounded with sourced scale/readout inputs and kept nonclaim until tested",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    source_by_copy = {
        "queue_mechanisms": OUTPUTS["mechanisms"],
        "queue_bound": OUTPUTS["hodge_bound"],
        "branch_wep": OUTPUTS["refusal"],
        "beta_docs": OUTPUTS["decision"],
    }
    return [
        {
            "copy_id": copy_id,
            "source_path": source_by_copy[copy_id],
            "target_path": target,
            "target_exists": target.exists(),
            "target_parses": csv_parses(target) if target.exists() else False,
            "reason": "branch copy for downstream carrier-inventory and residual-bound audits",
        }
        for copy_id, target in COPY_TARGETS.items()
    ]


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def false_flag_check() -> bool:
    guarded_fields = {"score_ready", "score_eligible", "accepted_ready", "valid_for_claim", "claim_allowed"}
    for path in generated_csvs():
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                for field in guarded_fields.intersection(row):
                    if row[field].strip().lower() == "true":
                        return False
                if "gate_pass" in row and row.get("valid_for_claim", "").strip().lower() == "true":
                    return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_ok = all(row["exists"] for row in source_rows)
    needles_ok = all(row["needles_present"] for row in source_rows)

    prior_text = read_text(OUT / "P8_Y5_BRR545_2273_VALIDATION.csv")
    prior_ok = "VAL2273_OVERALL" in prior_text and "PASS" in prior_text

    mechanisms = mechanism_rows()
    diffeo = diffeo_test_rows()
    scale = scale_bound_rows()
    hodge = hodge_bound_rows()
    qr = qr_intake_rows()
    refusals = refusal_rows()
    claims = claim_gate_rows()

    exact_candidates = any(row["status"].startswith("EXACT") for row in mechanisms) and any(
        row["candidate"] == "Hodge exact projection" for row in mechanisms
    )
    diffeo_guard = any(row["test_id"] == "DLT2274_3_areal_gauge_guard" for row in diffeo)
    scale_template = any("ell_cg/L_cg" in row["bound"] for row in scale)
    hodge_template = any("argmin" in row["equation"] for row in hodge)
    qr_inputs_missing = all(row["valid_for_claim"] is False and row["status"] == "missing" for row in qr)
    refusal_blocks = all(row["runner_result"] == "BLOCKED" and row["valid_for_claim"] is False for row in refusals)
    local_claim_blocked = any(row["claim_id"] == "CG2274_3_local_GR" and row["gate_pass"] is False for row in claims)
    physical_q_blocked = any(row["claim_id"] == "CG2274_1_physical_q_zero" and row["gate_pass"] is False for row in claims)
    next_selected = any(row["route_id"] == "NEXT2274_0_primary" and row["selection_status"] == "selected" for row in next_target_rows())
    csvs_parse = all(csv_parses(path) for path in generated_csvs())
    no_claim_flags = false_flag_check()
    copies_ok = all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*2274*")) if FORMALIZATION.exists() else True

    checks = [
        ("VAL2274_0_sources_exist", source_ok, "all cited source paths exist"),
        ("VAL2274_1_needles_present", needles_ok, "all cited source needles are present"),
        ("VAL2274_2_prior_validation", prior_ok, "2273 validation passes"),
        ("VAL2274_3_exact_candidates", exact_candidates, "curl-zero candidate mechanisms recorded"),
        ("VAL2274_4_diffeo_guard", diffeo_guard, "Lie-drag exact lift guarded by areal-gauge/q-match test"),
        ("VAL2274_5_scale_template", scale_template, "scale-separated ell_cg/L_cg bound template written"),
        ("VAL2274_6_hodge_template", hodge_template, "Hodge projection minimization template written"),
        ("VAL2274_7_qr_inputs_missing", qr_inputs_missing, "q_R bound inputs remain missing and nonclaim"),
        ("VAL2274_8_refusal_blocks", refusal_blocks, "refusal runner blocks exact-zero/local-GR claims"),
        ("VAL2274_9_physical_q_blocked", physical_q_blocked, "physical q curl-zero remains blocked"),
        ("VAL2274_10_local_claim_blocked", local_claim_blocked, "local GR claim remains blocked"),
        ("VAL2274_11_next_selected", next_selected, "2275 target selected"),
        ("VAL2274_12_csv_parse", csvs_parse, "all generated 2274 CSVs parse"),
        ("VAL2274_13_no_claim_flags", no_claim_flags, "no generated claim-validity flags are true"),
        ("VAL2274_14_branch_copies", copies_ok, "branch/queue copies exist and parse"),
        ("VAL2274_15_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL2274_16_formalization_no_2274", formalization_clean, "formalization-workbench has no 2274 output files"),
    ]

    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    overall = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2274_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2274 identifies exact curl-zero mechanisms under strict hypotheses, rejects them as current physical-q claims, stages a scale-separated Hodge residual bound, and selects 2275",
        }
    )
    return rows


def write_doc() -> None:
    sources = source_register_rows()
    mechanisms = mechanism_rows()
    diffeo = diffeo_test_rows()
    scale = scale_bound_rows()
    hodge = hodge_bound_rows()
    qr = qr_intake_rows()
    refusals = refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    copies = branch_copy_rows()
    validation = validation_rows()

    sections = [
        "# 2274 - Y5/R2FR Curl-Zero Mechanism Or Hodge Residual Bound",
        "",
        "## Verdict",
        "",
        "This checkpoint is a proper step forward, but not a victory lap. We found exact ways to make the curl obstruction vanish: ideal constant/affine cells, carrier-aligned scalar scalings, and Lie-dragged carriers. The problem is that none of these is yet proven to be the physical q tangent selected by the parent MTS action.",
        "",
        "The most useful result is the fallback structure: if exact zero is not parent-signed, the obstruction can be projected into an exact part plus a coexact Hodge residual. Under scale separation, the residual should enter as `epsilon_curl <= K ell_cg/L_cg`, but the needed scale, norm, kernel, and q-readout constants are still missing.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources),
        "",
        "## Curl-Zero Mechanism Tests",
        table(["mechanism_id", "candidate", "zero_condition", "derivation", "what_it_buys", "why_not_claim", "status", "valid_for_claim"], mechanisms),
        "",
        "## Diffeomorphic / Lie Lift Test",
        table(["test_id", "object", "formula", "interpretation", "blocker", "valid_for_claim"], diffeo),
        "",
        "## Scale-Separated Curl Bound",
        table(["bound_id", "quantity", "bound", "derivation", "required_inputs", "status", "valid_for_claim"], scale),
        "",
        "## Hodge Residual Bound Template",
        table(["template_id", "target", "equation", "outputs_needed", "claim_gate", "status", "valid_for_claim"], hodge),
        "",
        "## q_R Bound Input Ledger",
        table(["input_id", "quantity", "meaning", "required_source", "current_value", "units", "status", "valid_for_claim"], qr),
        "",
        "## Refusal Runner",
        table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusals),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], claims),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions),
        "",
        "## Next Target",
        table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition"], next_rows),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], copies),
        "",
        "## Validation",
        table(["check_id", "result", "detail"], validation),
        "",
        "## Working Interpretation",
        "",
        "This answers the coupling hunch in a sharper way: yes, the coupling/lift is the weak joint, but it is no longer mysterious. The clean derivation route is to prove a carrier inventory that makes the q channel an exact carrier-aligned scaling. The pragmatic testing route is to source `ell_cg/L_cg` and convert the Hodge residual into a q_R bound. Either way, we have something to attack rather than a vague gap.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["mechanisms"], mechanism_rows())
    write_csv(OUTPUTS["diffeo_test"], diffeo_test_rows())
    write_csv(OUTPUTS["scale_bound"], scale_bound_rows())
    write_csv(OUTPUTS["hodge_bound"], hodge_bound_rows())
    write_csv(OUTPUTS["qr_intake"], qr_intake_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["mechanisms"], COPY_TARGETS["queue_mechanisms"])
    shutil.copyfile(OUTPUTS["hodge_bound"], COPY_TARGETS["queue_bound"])
    shutil.copyfile(OUTPUTS["refusal"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["decision"], COPY_TARGETS["beta_docs"])
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows())

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

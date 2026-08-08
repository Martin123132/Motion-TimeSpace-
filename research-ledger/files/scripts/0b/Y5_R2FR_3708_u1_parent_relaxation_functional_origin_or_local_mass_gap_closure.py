from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3708"
BRANCH_ID = "MTS_R2FR_Y5_U1_PARENT_RELAXATION_FUNCTIONAL_OR_LOCAL_MASS_GAP_CLOSURE_3708"
DOC = ROOT / "3708-Y5-R2FR-u1-parent-relaxation-functional-origin-or-local-mass-gap-closure.md"

DOC_3698 = ROOT / "3698-Y5-R2FR-parent-entropy-free-energy-object-or-u1-closure-runner.md"
REC_3698 = RESIDUALS / "P8_Y5_R2FR_3698_RELATIVE_ENTROPY_CONSTRUCTION_ROWS.csv"
FISHER_3698 = RESIDUALS / "P8_Y5_R2FR_3698_FISHER_ALIGNMENT_ROWS.csv"
U1_3698 = RESIDUALS / "P8_Y5_R2FR_3698_U1_CLOSURE_RUNNER_ROWS.csv"
DOC_3699 = ROOT / "3699-Y5-R2FR-parent-bath-observable-map-and-source-silence-fill.md"
BATH_3699 = RESIDUALS / "P8_Y5_R2FR_3699_BATH_DISTRIBUTION_ROWS.csv"
PROJ_3699 = RESIDUALS / "P8_Y5_R2FR_3699_QUOTIENT_PROJECTION_ROWS.csv"
SOURCE_GATES_3699 = RESIDUALS / "P8_Y5_R2FR_3699_SOURCE_GATE_ROWS.csv"
DOC_3700 = ROOT / "3700-Y5-R2FR-second-order-source-residual-vector-and-local-test-runner.md"
TENSOR_3700 = RESIDUALS / "P8_Y5_R2FR_3700_RESIDUAL_TENSOR_ROWS.csv"
ARENA_3700 = RESIDUALS / "P8_Y5_R2FR_3700_ARENA_RUNNER_ROWS.csv"
DOC_3701 = ROOT / "3701-Y5-R2FR-local-test-source-row-acquisition-and-residual-matrix.md"
MISSING_3701 = RESIDUALS / "P8_Y5_R2FR_3701_MISSING_MTS_INPUT_ROWS.csv"
READY_3701 = RESIDUALS / "P8_Y5_R2FR_3701_SCORE_READINESS_ROWS.csv"
DOC_3707 = ROOT / "3707-Y5-R2FR-PN-lambdaH-parent-source-product-origin-or-R10-score-gate.md"
SCORE_3707 = RESIDUALS / "P8_Y5_R2FR_3707_R10_SCORE_GATE_ROWS.csv"
ANCHOR_3707 = RESIDUALS / "P8_Y5_R2FR_3707_OFFICIAL_ANCHOR_SCORE_ROWS.csv"
INPUT_3707 = RESIDUALS / "P8_Y5_R2FR_3707_PARENT_INPUT_AUDIT_ROWS.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def sci(value: float) -> str:
    return f"{value:.12e}"


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3698", DOC_3698, "D_KL=0.5 I_AB z^A z^B", "relative-entropy/Fisher u1 derivation"),
        ("rec_3698", REC_3698, "REC3698_3_free_energy_penalty", "free-energy penalty rows"),
        ("fisher_3698", FISHER_3698, "mu_H^2 >=", "Fisher mass-gap map"),
        ("u1_3698", U1_3698, "u_1_parent", "u1 symbolic runner rows"),
        ("doc_3699", DOC_3699, "Y_A^perp", "bath observable/source-silence mechanism"),
        ("bath_3699", BATH_3699, "p_z", "bath distribution rows"),
        ("projection_3699", PROJ_3699, "Y_A^perp", "Fisher projection rows"),
        ("source_gates_3699", SOURCE_GATES_3699, "Poynting", "matter/EM/Poynting/Newton/clock source gates"),
        ("doc_3700", DOC_3700, "z2_bound", "second-order residual vector bridge"),
        ("tensor_3700", TENSOR_3700, "R_iAB", "residual tensor rows"),
        ("arena_3700", ARENA_3700, "R10", "arena runner schemas"),
        ("doc_3701", DOC_3701, "LOCAL_TEST_EXTERNAL_SOURCE_ANCHORS", "external source anchors"),
        ("missing_3701", MISSING_3701, "MISS3701_5_z2_bound", "missing MTS-side local inputs"),
        ("ready_3701", READY_3701, "READY3701_0_R10", "score-readiness ledger"),
        ("doc_3707", DOC_3707, "P_N <=", "R10 parent coefficient score gate"),
        ("score_3707", SCORE_3707, "R10SG3707_066", "R10 candidate score rows"),
        ("anchor_3707", ANCHOR_3707, "ANCH3707_0_official_alpha1", "official anchor score consequence"),
        ("input_3707", INPUT_3707, "PIN3707_0_muH_lambdaH", "parent input audit"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(timestamp),
            "source_id": source_id,
            "role": role,
            "path": str(path),
            "needle": needle,
            "exists": exists,
            "needle_found": needle in text if exists else False,
            "claim_allowed": False,
        })
    return rows


def fisher_gap_derivation_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "derivation_id": "FGD3708_0_parent_bath",
            "statement": "parent local bath family",
            "formula": "p_z(xi|X_B,q)=p_0 exp[z^A Y_A^perp-W(z;X_B,q)]",
            "result": "leakage coordinates are bath deformations in ker(Dq), not direct changes of local matter/EM/clock/coupling observables",
            "status": "CONDITIONAL_PARENT_CONSTRUCTION_FROM_3698_3699",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "derivation_id": "FGD3708_1_fisher_entropy",
            "statement": "relative-entropy stiffness",
            "formula": "D_KL(p_z||p_0)=0.5 I_AB^perp z^A z^B+O(z^3)",
            "result": "positive Fisher covariance supplies the sign of the local leakage penalty after exact nulls are quotiented out",
            "status": "DERIVED_IF_P0_YA_DEFINED",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "derivation_id": "FGD3708_2_free_energy_to_u1",
            "statement": "free-energy/action conversion",
            "formula": "Delta F_cg=T_eff D_KL; u_1_parent=0.5*T_eff*lambda_min(G_H^-1/2 I_H^perp G_H^-1/2)",
            "result": "u_1 is no longer a naked fitted Yukawa mass; it can be a Fisher-gap product",
            "status": "STRUCTURAL_DERIVATION_NONCLAIM_UNITS_MISSING",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "derivation_id": "FGD3708_3_corrected_gap",
            "statement": "corrected local mass gap",
            "formula": "Xi_H := mu_H^2 = T_eff*iota_H - R_loss, with iota_H=lambda_min(G_H^-1/2 I_H^perp G_H^-1/2) and R_loss=R_domain+R_source_slope-lambda_min_corr",
            "result": "lambda_H=Xi_H^-1/2 is derived only if T_eff, iota_H and R_loss are source-owned",
            "status": "GAP_VARIABLE_DEFINED",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "derivation_id": "FGD3708_4_R10_rewrite",
            "statement": "R10 score in Fisher-gap variables",
            "formula": "alpha_eff_clean=0.5*P_N/Xi_H^2; require P_N <= 2*(1-eta)*alpha_bound_R10(Xi_H^-1/2)*Xi_H^2",
            "result": "R10/local Newton screening becomes a two-product problem: Fisher gap Xi_H and source product P_N",
            "status": "EXECUTABLE_NONCLAIM_SCORE_REWRITE",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "derivation_id": "FGD3708_5_second_order_bridge",
            "statement": "local arena residual bridge",
            "formula": "epsilon_i <= 0.5*rho_i*((C_H||J_y+B_y||/Xi_H)^2+B_edge^2+B_boundary^2)+epsilon_edge+epsilon_proj+epsilon_boundary",
            "result": "the same Fisher gap controls PPN, clocks, EM/Poynting, WEP and orbital residual amplitudes",
            "status": "LOCAL_ARENA_GATE_REWRITTEN",
            "claim_allowed": False,
        },
    ]


def gap_score_rows(timestamp: str, score_rows_3707: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, row in enumerate(score_rows_3707):
        xi_h = float(row["mu_H_sq_m2"])
        eta10_pn = float(row["P_N_max_eta10_m4"])
        rows.append({
            **base(timestamp),
            "gap_score_id": f"FGS3708_{index:03d}",
            "source_score_id": row["score_id"],
            "lambda_um": row["lambda_um"],
            "Xi_H_required_clean_m2": sci(xi_h),
            "u1_required_clean_m2": row["u1_clean_required_m2"],
            "T_eff_iota_H_required_clean_m2": sci(xi_h),
            "P_N_max_eta0_m4": row["P_N_max_eta0_m4"],
            "P_N_max_eta10_m4": row["P_N_max_eta10_m4"],
            "P_N_max_eta50_m4": row["P_N_max_eta50_m4"],
            "sqrt_P_N_max_eta10_m2": row["sqrt_P_N_max_eta10_m2"],
            "gap_formula": "Xi_H=T_eff*iota_H-R_loss; clean row sets R_loss=0",
            "score_formula": "P_N <= 2*(1-eta)*alpha_bound_R10(Xi_H^-1/2)*Xi_H^2",
            "score_status": "NONCLAIM_REQUIRES_PARENT_TEFF_IOTA_RLOSS_PN_ETA_AND_REVIEWED_CURVE",
            "claim_allowed": False,
        })
    return rows


def anchor_gap_rows(timestamp: str, anchor_rows_3707: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for row in anchor_rows_3707:
        xi_h = float(row["mu_H_sq_m2"])
        rows.append({
            **base(timestamp),
            "anchor_gap_id": "FGA3708_0_alpha1_anchor_gap",
            "source_anchor_id": row["anchor_id"],
            "lambda_um": row["lambda_um"],
            "Xi_H_required_clean_m2": sci(xi_h),
            "u1_required_clean_m2": row["u1_clean_required_m2"],
            "T_eff_iota_H_required_clean_m2": sci(xi_h),
            "P_N_max_eta0_m4": row["P_N_max_eta0_m4"],
            "P_N_max_eta10_m4": row["P_N_max_eta10_m4"],
            "meaning": "at the official alpha=1 anchor, a clean Fisher gap at least this large corresponds to lambda_H=38.6 um",
            "claim_allowed": False,
        })
    return rows


def parent_contract_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("PCI3708_0_p0", "p_0(xi|X_B,q)", "source normalized local bath/reference distribution", "MISSING_PARENT_BATH_ROW"),
        ("PCI3708_1_Yperp", "Y_A^perp", "parent leakage observables after Fisher projection against resolved matter/EM/Poynting/Newton/clock scores", "MISSING_PARENT_LEAKAGE_OBSERVABLES"),
        ("PCI3708_2_IH", "I_H^perp", "Fisher covariance positive on horizontal leakage modes after vertical nulls removed", "MISSING_NUMERIC_FISHER_MATRIX"),
        ("PCI3708_3_Teff", "T_eff", "effective free-energy/action conversion scale with units matching local mass-gap convention", "MISSING_TEMPERATURE_UNITS_ROW"),
        ("PCI3708_4_Rloss", "R_loss", "domain/source-slope/correction loss term in Xi_H=T_eff*iota_H-R_loss", "MISSING_CORRECTION_BOUND"),
        ("PCI3708_5_PN", "P_N", "K_N*rho_Newton*C_H^2||J_y+B_y||^2 source product", "MISSING_SOURCE_PRODUCT"),
        ("PCI3708_6_eta", "eta_boundary+eta_edge", "boundary/edge theorem-zero or finite source budget", "MISSING_BOUNDARY_EDGE_SOURCE_VALUE"),
        ("PCI3708_7_rho_i", "rho_i residual tensors", "second-order local observable tensors for PPN, Newton, EM/Poynting, clocks, WEP, orbits", "MISSING_PARENT_RESIDUAL_TENSORS"),
        ("PCI3708_8_curve", "alpha_bound_R10(lambda)", "reviewed or official R10 bound curve", "CANDIDATE_CURVE_ONLY"),
    ]
    return [
        {
            **base(timestamp),
            "contract_id": contract_id,
            "quantity": quantity,
            "required_object": required_object,
            "status": status,
            "claim_allowed": False,
        }
        for contract_id, quantity, required_object, status in specs
    ]


def arena_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("LAG3708_0_R10", "short-range Newton/R10", "alpha_eff_clean=0.5*P_N/Xi_H^2 + alpha_boundary_edge", "P_N <= 2*(1-eta)*alpha_bound_R10(Xi_H^-1/2)*Xi_H^2", "needs Xi_H, P_N, eta and reviewed curve"),
        ("LAG3708_1_PPN", "PPN/local metric", "S_PPN <= 0.5*rho_PPN*(C_HJ/Xi_H)^2 + K_Kperp||Kperp||/N_PPN + K_q||q_loc||/N_PPN", "S_PPN <= epsilon_PPN", "needs rho_PPN, Kperp, q_loc and normalizer vector"),
        ("LAG3708_2_EM", "Maxwell/EM/Poynting stress", "epsilon_EM <= 0.5*rho_EM*(C_HJ/Xi_H)^2 + alpha_source_leak + current_normalization_error", "EM residual <= sourced alpha/stress/Poynting tolerance", "needs EM residual tensor and resolved Poynting score"),
        ("LAG3708_3_clock", "precision clocks/time", "|delta nu/nu| <= 0.5*rho_clock*(C_HJ/Xi_H)^2 + clock_projection_error", "clock residual <= sourced clock tolerance", "needs clock residual tensor and time-convention lock"),
        ("LAG3708_4_WEP", "WEP/species", "eta_species <= 0.5||rho_species_a-rho_species_b||*(C_HJ/Xi_H)^2 + species_projection_error", "eta_species <= sourced WEP tolerance", "needs species score map"),
        ("LAG3708_5_orbital", "orbital dynamics", "delta_orbit <= K_orbit*0.5*rho_Newton*z0^2*exp(-2r*sqrt(Xi_H))*(1+r*sqrt(Xi_H))^2 + boundary", "orbital residual <= ephemeris tolerance", "needs orbital kernel and source model"),
    ]
    return [
        {
            **base(timestamp),
            "arena_gate_id": gate_id,
            "arena": arena,
            "mts_bound_in_fisher_gap_variables": mts_bound,
            "pass_condition": pass_condition,
            "required_inputs": required_inputs,
            "status": "NONCLAIM_GATE_READY_VALUES_MISSING",
            "claim_allowed": False,
        }
        for gate_id, arena, mts_bound, pass_condition, required_inputs in specs
    ]


def decision_rows(timestamp: str, gap_rows: list[dict[str, object]], anchor_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    tightest = min(gap_rows, key=lambda row: float(row["P_N_max_eta10_m4"]))
    anchor = anchor_rows[0]
    return [
        {
            **base(timestamp),
            "decision_id": "DEC3708_0_u1_route_promoted_to_fisher_gap_contract",
            "decision": "Treat u_1/local screening as a Fisher-gap product Xi_H=T_eff*iota_H-R_loss, not as a free Yukawa mass.",
            "rationale": "3698-3700 supply a constructive entropy/source-silence/residual route; 3707 supplies the score gate.",
            "status": "BEST_CURRENT_DERIVATION_ROUTE_NONCLAIM",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "decision_id": "DEC3708_1_R10_reduced_to_two_parent_products",
            "decision": "For R10, the local branch now needs only Fisher gap Xi_H and source product P_N plus eta/curve review.",
            "rationale": "alpha_eff_clean=0.5*P_N/Xi_H^2 and the bound is P_N <= 2*(1-eta)*alpha_bound(Xi_H^-1/2)*Xi_H^2.",
            "status": "EXECUTABLE_SCORE_FORM_NONCLAIM",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "decision_id": "DEC3708_2_anchor_requirement",
            "decision": f"Official alpha=1 anchor requires clean Xi_H={anchor['Xi_H_required_clean_m2']} m^-2 and P_N_max_eta10={anchor['P_N_max_eta10_m4']} m^-4.",
            "rationale": "This is the clearest source-backed sanity target for future parent coefficients.",
            "status": "ANCHOR_REQUIREMENT_RECORDED",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "decision_id": "DEC3708_3_candidate_tightest_requirement",
            "decision": f"Tightest private candidate curve row is lambda={tightest['lambda_um']} um, Xi_H={tightest['Xi_H_required_clean_m2']} m^-2, P_N_max_eta10={tightest['P_N_max_eta10_m4']} m^-4.",
            "rationale": "This is only private candidate-curve pressure; it is useful for coefficient stress testing, not claims.",
            "status": "PRIVATE_SMOKE_REQUIREMENT_RECORDED",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "decision_id": "DEC3708_4_next_target",
            "decision": "Next work should source or derive the first Xi_H and P_N rows, starting with R10 because its score gate is now shortest.",
            "rationale": "More theory wording will not beat the gate; the exact parent rows are now named.",
            "status": "ADVANCE_TO_SOURCE_PRODUCT_FILL",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3708_0_p0_Y", "p_0 and Y_A^perp are parent-defined and quotient-null"),
        ("CG3708_1_fisher_gap", "I_H^perp, T_eff and R_loss produce a positive sourced Xi_H"),
        ("CG3708_2_source_product", "P_N is parent-derived or bounded from K_N, rho_Newton, C_H and J_y+B_y"),
        ("CG3708_3_eta_boundary", "eta_boundary+eta_edge is theorem-zero or finite source value"),
        ("CG3708_4_R10_curve", "R10 alpha_bound(lambda) is official/reviewed"),
        ("CG3708_5_residual_tensors", "rho_i residual tensors are sourced for PPN, EM/Poynting, clock, WEP and orbital arenas"),
        ("CG3708_6_public", "local GR/Newton/Maxwell/R10 public claim allowed"),
    ]
    return [
        {
            **base(timestamp),
            "claim_gate_id": gate_id,
            "requirement": requirement,
            "status": "BLOCKED",
            "claim_allowed": False,
        }
        for gate_id, requirement in specs
    ]


def status_rows(timestamp: str, anchor_gap: list[dict[str, object]], gap_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    tightest = min(gap_rows, key=lambda row: float(row["P_N_max_eta10_m4"]))
    anchor = anchor_gap[0]
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3708_0",
            "status": "U1_RECAST_AS_FISHER_GAP_PRODUCT_R10_SCORE_GATE_CONNECTED_NONCLAIM",
            "summary": (
                "3708 stitches the existing 3698-3700 derivation chain to the 3707 score gate. "
                "The clean local mass gap is Xi_H=T_eff*iota_H-R_loss, with lambda_H=Xi_H^-1/2 and "
                "alpha_eff_clean=0.5*P_N/Xi_H^2. "
                f"At the official 38.6 um anchor, clean Xi_H={anchor['Xi_H_required_clean_m2']} m^-2 and "
                f"P_N_max_eta10={anchor['P_N_max_eta10_m4']} m^-4. "
                f"The tightest private candidate row has lambda={tightest['lambda_um']} um, Xi_H={tightest['Xi_H_required_clean_m2']} m^-2, "
                f"and P_N_max_eta10={tightest['P_N_max_eta10_m4']} m^-4."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3708_0",
            "target_doc": "3709-Y5-R2FR-Fisher-gap-and-PN-parent-source-row-fill-or-closure-demotion.md",
            "target_script": "scripts/Y5_R2FR_3709_Fisher_gap_and_PN_parent_source_row_fill_or_closure_demotion.py",
            "objective": "try to source or derive the first numeric/symbolic parent rows for Xi_H=T_eff*iota_H-R_loss and P_N; if not possible, demote the local mass-gap route to explicit closure while preserving the R10/PPN/EM score gates",
            "success_gate": "at least one of Xi_H or P_N becomes parent-source bounded enough for a nonclaim R10 smoke score, or the exact missing rows are isolated without adding another closure assumption",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    derivations: list[dict[str, object]],
    gap_scores: list[dict[str, object]],
    anchor_gap: list[dict[str, object]],
    contracts: list[dict[str, object]],
    arena_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    tightest = min(gap_scores, key=lambda row: float(row["P_N_max_eta10_m4"]))
    anchor = anchor_gap[0]
    lines = [
        "# 3708 Y5 R2FR u1 Parent Relaxation Functional Origin Or Local Mass Gap Closure",
        "",
        "Private checkpoint. No GitHub action. No public claim.",
        "",
        "## Status",
        "",
        f"- `{status[0]['status']}`",
        f"- {status[0]['summary']}",
        "",
        "## Main Result",
        "",
        "- The old question `where does u_1 come from?` is now sharpened into a Fisher-gap product.",
        "- Define `iota_H := lambda_min(G_H^-1/2 I_H^perp G_H^-1/2)` and `R_loss:=R_domain+R_source_slope-lambda_min_corr`.",
        "- Then `Xi_H := mu_H^2 = T_eff*iota_H - R_loss`, `lambda_H=Xi_H^-1/2`, and the clean aligned branch has `u_1=Xi_H/2`.",
        "- The R10 score becomes `alpha_eff_clean=0.5*P_N/Xi_H^2`, hence `P_N <= 2*(1-eta)*alpha_bound_R10(Xi_H^-1/2)*Xi_H^2`.",
        "- This is progress because `lambda_H` is no longer a free range parameter if `T_eff`, `I_H^perp`, and correction losses are parent-filled.",
        "- It remains nonclaim because those parent rows, `P_N`, `eta`, and the reviewed curve are not filled.",
        "- `valid_for_claim=false`: this is a private derivation/score contract, not a local-GR/R10/PPN/EM pass.",
        "",
        "## Numeric Consequences",
        "",
        f"- Official anchor: `lambda=38.6 um`, `Xi_H_clean={anchor['Xi_H_required_clean_m2']} m^-2`, `u1_clean={anchor['u1_required_clean_m2']} m^-2`, `P_N_max_eta10={anchor['P_N_max_eta10_m4']} m^-4`.",
        f"- Tightest private candidate row: `lambda={tightest['lambda_um']} um`, `Xi_H_clean={tightest['Xi_H_required_clean_m2']} m^-2`, `P_N_max_eta10={tightest['P_N_max_eta10_m4']} m^-4`.",
        f"- Gap score rows generated: `{len(gap_scores)}`.",
        "",
        "## Derivation Chain",
        "",
    ]
    for row in derivations:
        lines.append(f"- `{row['derivation_id']}` `{row['status']}`: {row['formula']}")
    lines.extend(["", "## Parent Contract Rows", ""])
    for row in contracts:
        lines.append(f"- `{row['contract_id']}` `{row['quantity']}`: `{row['status']}` | {row['required_object']}")
    lines.extend(["", "## Local Arena Gates", ""])
    for row in arena_gates:
        lines.append(f"- `{row['arena_gate_id']}` `{row['arena']}`: {row['mts_bound_in_fisher_gap_variables']}")
    lines.extend(["", "## Decisions", ""])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` | {row['decision']}")
    lines.extend(["", "## Claim Gates", ""])
    for row in claim_gates:
        lines.append(f"- `{row['claim_gate_id']}`: `{row['status']}` | {row['requirement']}")
    lines.extend(["", "## Source Register", ""])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: exists={row['exists']} needle_found={row['needle_found']} path=`{row['path']}`")
    lines.extend(["", "## Next Target", ""])
    lines.append(f"- `{next_target[0]['target_doc']}`")
    lines.append(f"- Objective: {next_target[0]['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    generated_paths: list[Path],
    sources: list[dict[str, object]],
    derivations: list[dict[str, object]],
    gap_scores: list[dict[str, object]],
    anchor_gap: list[dict[str, object]],
    contracts: list[dict[str, object]],
    arena_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    timestamp = stamp()
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("sources_exist", "all cited local sources exist", all(bool(row["exists"]) for row in sources), ""))
    checks.append(("needles_found", "all source needles found", all(bool(row["needle_found"]) for row in sources), ""))
    checks.append(("outputs_exist", "all generated paths exist", all(path.exists() for path in generated_paths), ""))
    csv_parse_ok = True
    csv_error = ""
    try:
        for path in [path for path in generated_paths if path.suffix.lower() == ".csv"]:
            if not parse_csv(path):
                csv_parse_ok = False
                csv_error = f"empty csv: {path}"
                break
    except Exception as exc:  # pragma: no cover
        csv_parse_ok = False
        csv_error = str(exc)
    checks.append(("csv_parse", "all generated CSV files parse and are nonempty", csv_parse_ok, csv_error))
    derivation_text = " ".join(str(row["formula"]) for row in derivations)
    checks.append(("fisher_gap_derivation", "Fisher gap and R10 rewrite formulas are present", "Xi_H" in derivation_text and "alpha_eff_clean" in derivation_text and "T_eff*iota_H" in derivation_text, ""))
    checks.append(("score_rows", "gap score rows preserve R10 candidate curve count and positive values", len(gap_scores) == 67 and all(float(row["Xi_H_required_clean_m2"]) > 0 and float(row["P_N_max_eta10_m4"]) > 0 for row in gap_scores), f"rows={len(gap_scores)}"))
    checks.append(("anchor_gap", "official alpha=1 anchor gap row exists and is positive", len(anchor_gap) == 1 and float(anchor_gap[0]["Xi_H_required_clean_m2"]) > 0 and float(anchor_gap[0]["P_N_max_eta10_m4"]) > 0, ""))
    required_contracts = {"p_0(xi|X_B,q)", "Y_A^perp", "I_H^perp", "T_eff", "R_loss", "P_N", "eta_boundary+eta_edge", "rho_i residual tensors", "alpha_bound_R10(lambda)"}
    checks.append(("contracts_complete", "parent contract rows include all current blockers", {row["quantity"] for row in contracts} >= required_contracts, ""))
    checks.append(("arena_gates", "all six local arena gates are rewritten in Fisher gap variables", len(arena_gates) == 6 and all("Xi_H" in row["mts_bound_in_fisher_gap_variables"] for row in arena_gates), ""))
    checks.append(("decisions_nonclaim", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3709", "next target advances to Fisher gap and PN source row fill", str(next_target[0]["target_doc"]).startswith("3709-") and "Fisher-gap" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains the core 3708 equations", all(term in doc_text for term in ["Xi_H := mu_H^2", "alpha_eff_clean=0.5*P_N/Xi_H^2", "P_N <=", "valid_for_claim"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3708*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3708 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
    return [
        {
            **base(timestamp),
            "validation_id": check_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "details": details,
        }
        for check_id, description, passed, details in checks
    ]


def main() -> int:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    scores_3707 = parse_csv(SCORE_3707)
    anchors_3707 = parse_csv(ANCHOR_3707)
    sources = source_register(timestamp)
    derivations = fisher_gap_derivation_rows(timestamp)
    gap_scores = gap_score_rows(timestamp, scores_3707)
    anchor_gap = anchor_gap_rows(timestamp, anchors_3707)
    contracts = parent_contract_rows(timestamp)
    arena_gates = arena_gate_rows(timestamp)
    decisions = decision_rows(timestamp, gap_scores, anchor_gap)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp, anchor_gap, gap_scores)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3708_SOURCE_REGISTER.csv",
        "derivations": RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv",
        "gap_scores": RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_SCORE_ROWS.csv",
        "anchor_gap": RESIDUALS / "P8_Y5_R2FR_3708_OFFICIAL_ANCHOR_FISHER_GAP_ROWS.csv",
        "contracts": RESIDUALS / "P8_Y5_R2FR_3708_PARENT_INPUT_CONTRACT_ROWS.csv",
        "arena_gates": RESIDUALS / "P8_Y5_R2FR_3708_LOCAL_ARENA_GATE_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3708_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3708_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3708_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3708_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3708_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["derivations"], derivations)
    write_csv(outputs["gap_scores"], gap_scores)
    write_csv(outputs["anchor_gap"], anchor_gap)
    write_csv(outputs["contracts"], contracts)
    write_csv(outputs["arena_gates"], arena_gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, derivations, gap_scores, anchor_gap, contracts, arena_gates, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, derivations, gap_scores, anchor_gap, contracts, arena_gates, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3708 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3708 checkpoint: u1 recast as Fisher-gap product and connected to R10/local arena score gates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

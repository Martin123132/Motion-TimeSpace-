from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_HCORE_QR_SOURCE_EQUATION_OR_BOUNDARY_OWNER_2502"
CHECKPOINT_ID = "2502"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
QR_RAW = ROOT / "source-intake" / "qr-hat" / "raw"

RAW_QRHAT = QR_RAW / "QRHAT1255_CASSINI_GAMMA_PHENOMENOLOGICAL_BOUND_NONCLAIM.csv"
DOC = ROOT / "2502-Y5-R2FR-parent-Hcore-QR-source-equation-or-boundary-charge-owner.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2502_SOURCE_REGISTER.csv",
    "hcore_qr": OUT / "P8_Y5_NO_SHADOW_2502_HCORE_QR_SOURCE_EQUATION_AUDIT.csv",
    "uv_spine": OUT / "P8_Y5_NO_SHADOW_2502_UV_REDUCTION_SPINE.csv",
    "coefficient_law": OUT / "P8_Y5_NO_SHADOW_2502_NEWTON_PPN_COEFFICIENT_LAW.csv",
    "epsilonM": OUT / "P8_Y5_NO_SHADOW_2502_EPSILONM_SOURCE_CLOSURE_LEDGER.csv",
    "qr_binding": OUT / "P8_Y5_NO_SHADOW_2502_QR_DELTA_P_BINDING_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2502_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2502_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2502_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2502_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2502_VALIDATION.csv",
}

COPY_TARGETS = {
    "hcore_qr": LOCAL_BOUNDS / "Hcore_QR_source_equation_audit_2502_NONCLAIM.csv",
    "uv_spine": LOCAL_BOUNDS / "UV_reduction_spine_2502_NONCLAIM.csv",
    "coefficient_law": BETA_DOCS / "V_Newton_PPN_coefficient_law_2502_NONCLAIM.csv",
    "epsilonM": QUEUE / "JR2502_EPSILONM_SOURCE_CLOSURE_LEDGER_NONCLAIM.csv",
    "next_target": QUEUE / "JR2502_WORLDTUBE_HILBERT_SOURCE_SELECTOR_OR_REQ_FILL_NEXT.csv",
}

SOURCES = [
    {
        "source_id": "SRC2502_00_2501_handoff",
        "source_path": ROOT / "2501-Y5-R2FR-QR-parent-zero-signature-or-live-delta-p-input-row.md",
        "needles": ["NEXT2501_0_selected", "QRZ2501_5_verdict", "LIVE2501_0_QRHAT1255_Cassini_ceiling"],
        "role": "live Q_R parent-zero or nonclaim delta_p ceiling handoff",
    },
    {
        "source_id": "SRC2502_01_1884_zero_flux",
        "source_path": ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md",
        "needles": ["NBC1884_1_exact_zero_flux_lemma", "NBC1884_4_no_boundary_charge_parent_signature", "VAL1884_OVERALL"],
        "role": "exact zero-flux lemma and no-boundary-charge parent signature blocker",
    },
    {
        "source_id": "SRC2502_02_2174_hcore",
        "source_path": ROOT / "2174-Y5-R2FR-Hcore-canonical-bracket-closure-or-auxiliary-route-demotion.md",
        "needles": ["CUS2174_3_core_expansion", "DF2174_4_second_class", "VAL2174_OVERALL"],
        "role": "conditional H_core u-sector second-class mechanism",
    },
    {
        "source_id": "SRC2502_03_2177_v_readout",
        "source_path": ROOT / "2177-Y5-R2FR-v-only-visible-quotient-readout-owner-or-current-readout-lock.md",
        "needles": ["VOR2177_2_constraint_surface", "PPN2177_5_verdict", "VAL2177_OVERALL"],
        "role": "v-only constrained readout and conditional PPN shape",
    },
    {
        "source_id": "SRC2502_04_2178_v_source",
        "source_path": ROOT / "2178-Y5-R2FR-constraint-before-readout-ordering-and-v-PPN-source-convention-or-readout-lock.md",
        "needles": ["VS2178_2_required_solution", "PPN2178_2_beta_law", "VAL2178_OVERALL"],
        "role": "Newton sign/amplitude target and beta drift law",
    },
    {
        "source_id": "SRC2502_05_2179_v_coefficients",
        "source_path": ROOT / "2179-Y5-R2FR-parent-v-field-action-normalization-and-beta-quadratic-zero-or-finite-row.md",
        "needles": ["VAC2179_5_current_verdict", "BKA2179_2_pure_linear_branch", "VAL2179_OVERALL"],
        "role": "K_v/C_v source-normalization and kappa_v beta residual laws",
    },
    {
        "source_id": "SRC2502_06_2180_mass_glue",
        "source_path": ROOT / "2180-Y5-R2FR-PiM-JH-mass-current-to-v-source-coefficient-glue-or-delta-kappa-fill.md",
        "needles": ["NGL2180_2_observable_newton_residual", "KGL2180_1_kappa_decomposition", "VAL2180_OVERALL"],
        "role": "delta_KC and epsilon_M split for Newton source normalization",
    },
    {
        "source_id": "SRC2502_07_2181_commutator",
        "source_path": ROOT / "2181-Y5-R2FR-PiM-commutator-worldtube-source-glue-zero-or-epsilonM-fill.md",
        "needles": ["PCA2181_0_product_rule", "EMD2181_4_total_envelope", "VAL2181_OVERALL"],
        "role": "Pi_M commutator and epsilon_M no-cancellation envelope",
    },
    {
        "source_id": "SRC2502_08_2182_topological_hilbert",
        "source_path": ROOT / "2182-Y5-R2FR-topological-Hilbert-equality-R_eq-zero-or-epsilonM-bound-fill.md",
        "needles": ["TEA2182_0_identity_target", "CG2182_5_Newton_local_GR", "VAL2182_OVERALL"],
        "role": "topological-Hilbert equality gate and R_eq/B_zero blockers",
    },
    {
        "source_id": "SRC2502_09_qrhat_guardrail",
        "source_path": RAW_QRHAT,
        "needles": ["QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM", "phenomenological_upper_bound_not_theory_prediction"],
        "role": "Cassini-derived nonclaim q_R_hat ceiling guardrail",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv_first_row(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows[0] if rows else {}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:  # pragma: no cover
        return False, 0, str(error)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def hcore_qr_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "HQR2502_0_cell_current_equation",
            "object": "C_R or R_AB exterior current",
            "statement": "partial_r(W partial_r C_R)=J_R; in local exterior J_R=0 gives W partial_r C_R=Q_R.",
            "status": "EXACT_EXISTING_CONDITIONAL",
            "what_it_buys": "identifies Q_R as the exterior reciprocal charge",
            "what_is_missing": "does not set Q_R=0",
            "valid_for_claim": False,
        },
        {
            "audit_id": "HQR2502_1_hcore_u_skeleton",
            "object": "u=C_R/2 H_core skeleton",
            "statement": "H_core=H_vis+1/2 A_u^-1 p_u^2+1/2 K_u u^2+I_u p_u+J_u u+...",
            "status": "CONDITIONAL_SKELETON_NOT_PARENT_SIGNED",
            "what_it_buys": "turns the vague local plateau into explicit I_u/J_u/boundary/matter/readout conditions",
            "what_is_missing": "parent H_core invariance, I_u=0, J_u=0, boundary differentiability and matter/readout descent",
            "valid_for_claim": False,
        },
        {
            "audit_id": "HQR2502_2_second_class_route",
            "object": "u,p_u auxiliary elimination",
            "statement": "If Lambda_R u is parent-owned and I_u=J_u=0 with silent boundary/matter/readout, u≈0 and p_u≈0 remove the radial-cell mode.",
            "status": "EXACT_CONDITIONAL_NOT_CURRENT_CLAIM",
            "what_it_buys": "would kill bulk C_R and hence the bulk source of Q_R hair",
            "what_is_missing": "the premises are not signed in one parent package",
            "valid_for_claim": False,
        },
        {
            "audit_id": "HQR2502_3_Ru_v_route",
            "object": "R_u and v=ln(T/sqrt(S))",
            "statement": "R_u flips u and fixes v; after u=0 the coframe reconstructs from v alone.",
            "status": "REAL_CONDITIONAL_GAIN",
            "what_it_buys": "current T/sqrt(S) readout can survive after constraint-first reduction",
            "what_is_missing": "parent order: u=0 before clocks, rods, photons, source mass, boundary endpoints and matter readout",
            "valid_for_claim": False,
        },
        {
            "audit_id": "HQR2502_4_boundary_owner",
            "object": "boundary/corner Q_R owner",
            "statement": "Bulk u=0 does not by itself kill boundary charge; Q_R=0 needs differentiable boundary action, zero compact flux and no readout tail.",
            "status": "BOUNDARY_OWNER_UNSIGNED",
            "what_it_buys": "prevents C_R/r hair from re-entering after bulk elimination",
            "what_is_missing": "worldtube/source selector, topological-Hilbert equality, R_eq=0 and B_zero_flux=0",
            "valid_for_claim": False,
        },
        {
            "audit_id": "HQR2502_5_current_verdict",
            "object": "parent-owned Q_R source equation",
            "statement": "Current corpus does not yet derive a parent E_R=delta H_core/delta C_R equation plus boundary/source owner that forces Q_R=0.",
            "status": "PARENT_QR_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "what_it_buys": "keeps local-GR proof honest",
            "what_is_missing": "constraint-before-readout, v action normalization, mass-current glue, topological-Hilbert equality and boundary zero flux",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def uv_spine_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "spine_id": "UV2502_0_variables",
            "result": "a=ln T, b=ln sqrt(S), u=a+b=C_R/2, v=a-b=ln(T/sqrt(S)).",
            "status": "EXACT_DEFINITION",
            "claim_effect": "separates reciprocal-cell mode u from visible radial potential candidate v",
            "remaining_gate": "parent has to justify constraint-first reduction",
            "valid_for_claim": False,
        },
        {
            "spine_id": "UV2502_1_constrained_readout",
            "result": "On u=0: T=exp(v/2), sqrt(S)=exp(-v/2), A=T^2=exp(v), B=S=exp(-v).",
            "status": "EXACT_CONDITIONAL_READOUT",
            "claim_effect": "current coframe can be reconstructed from v after u=0",
            "remaining_gate": "ordinary observables must read the constrained representative, not the off-shell pair",
            "valid_for_claim": False,
        },
        {
            "spine_id": "UV2502_2_newton_target",
            "result": "For positive U=GM/r, slow-particle Newtonian limit requires v=-2U/c^2+O(U^2/c^4).",
            "status": "EXACT_SOURCE_NORMALIZATION_TARGET",
            "claim_effect": "fixes sign and amplitude of the local potential",
            "remaining_gate": "derive K_v/C_v and matter source coupling from the parent action",
            "valid_for_claim": False,
        },
        {
            "spine_id": "UV2502_3_gamma_shape",
            "result": "If v=-2U/c^2+O(U^2/c^4), then gamma=1 at first order in the constrained v-readout branch.",
            "status": "CONDITIONAL_GAMMA_SHAPE_PASS",
            "claim_effect": "gamma is no longer the hardest local gate",
            "remaining_gate": "source normalization, beta, conservation, matter universality and boundary endpoints",
            "valid_for_claim": False,
        },
        {
            "spine_id": "UV2502_4_beta_law",
            "result": "For v=-2x+kappa_v x^2+O(x^3), x=U/c^2, beta=1+kappa_v/2.",
            "status": "EXACT_BETA_DRIFT_LAW",
            "claim_effect": "beta reduces to the kappa_v zero-or-bound problem",
            "remaining_gate": "prove kappa_v=0/gauge or source a finite kappa_v row",
            "valid_for_claim": False,
        },
        {
            "spine_id": "UV2502_5_status",
            "result": "The local branch has narrowed from raw Q_R vibes to u-constraint order, v source normalization and kappa_v beta residuals.",
            "status": "ROUTE_NARROWED_NOT_CLAIMABLE",
            "claim_effect": "this is real structural progress, not a public pass",
            "remaining_gate": "worldtube-Hilbert source selector and zero boundary flux",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def coefficient_law_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "law_id": "LAW2502_0_delta_KC",
            "quantity": "delta_KC",
            "formula": "delta_KC := C_v c^4/(16*pi*G_ref*K_v)-1",
            "meaning": "action-side error in the v source normalization",
            "status": "EXACT_DEFINITION_FROM_2180",
            "needed_for_zero": "parent derives target K_v/C_v ratio",
            "valid_for_claim": False,
        },
        {
            "law_id": "LAW2502_1_epsilon_M",
            "quantity": "epsilon_M",
            "formula": "epsilon_M := M_source[v]/M_eff[Pi_M J_H]-1",
            "meaning": "mass-current/source-measure mismatch",
            "status": "EXACT_DEFINITION_FROM_2180",
            "needed_for_zero": "same Hilbert source worldtube, fixed Pi_M, zero commutator, zero extra channels",
            "valid_for_claim": False,
        },
        {
            "law_id": "LAW2502_2_Delta_Newton_v",
            "quantity": "Delta_Newton_v",
            "formula": "Delta_Newton_v := (1+delta_KC)(1+epsilon_M)-1",
            "meaning": "observable Newton amplitude residual in the constrained v branch",
            "status": "EXACT_NO_CANCELLATION_LINK",
            "needed_for_zero": "delta_KC=0 and epsilon_M=0 independently, or finite rows with no cancellation credit",
            "valid_for_claim": False,
        },
        {
            "law_id": "LAW2502_3_kappa_v",
            "quantity": "kappa_v",
            "formula": "kappa_v = -eta_v + kappa_source_quad + kappa_PiM + kappa_boundary + kappa_readout + kappa_operator",
            "meaning": "absolute beta-tail source ledger",
            "status": "EXACT_LEDGER_DEFINITION_FROM_2180",
            "needed_for_zero": "every beta-tail component zero/gauge/source-backed, no cancellation credit",
            "valid_for_claim": False,
        },
        {
            "law_id": "LAW2502_4_beta",
            "quantity": "beta_minus_1",
            "formula": "beta-1 = kappa_v/2",
            "meaning": "PPN beta residual after constrained v readout",
            "status": "EXACT_FROM_2178_2179",
            "needed_for_zero": "kappa_v=0 or finite kappa_v row inside full PPN vector",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def epsilonM_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "closure_id": "EM2502_0_identity",
            "object": "topological-Hilbert equality",
            "formula_or_condition": "Pi_M J_H = J_M_top + dB_zero + R_eq",
            "status": "EXACT_CONDITIONAL_IDENTITY",
            "blocker": "R_eq=0 and B_zero_flux=0 are not parent-derived",
            "next_evidence": "same compact Hilbert source worldtube and fixed topological representative",
            "valid_for_claim": False,
        },
        {
            "closure_id": "EM2502_1_commutator",
            "object": "projected-current product rule",
            "formula_or_condition": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
            "status": "EXACT_OBSTRUCTION",
            "blocker": "[d,Pi_M]J_H=0 is conditional, not automatic",
            "next_evidence": "fixed Pi_M chain map or finite I_commutator bound",
            "valid_for_claim": False,
        },
        {
            "closure_id": "EM2502_2_boundary",
            "object": "B_zero compact boundary flux",
            "formula_or_condition": "integral_boundary dB_zero = 0 on the compact linked boundary",
            "status": "BOUNDARY_ZERO_NOT_DERIVED",
            "blocker": "reference/worldtube/projector-stress silence is unsigned",
            "next_evidence": "fixed reference plus zero-flux theorem or finite B_zero_flux row",
            "valid_for_claim": False,
        },
        {
            "closure_id": "EM2502_3_worldtube",
            "object": "source worldtube selector",
            "formula_or_condition": "W_source, rho_H dV_H, observed time generator and linking surface are parent-selected before readout",
            "status": "WORLDTUBE_SELECTOR_NOT_DERIVED",
            "blocker": "post-readout source choice would be a fitted GM mask",
            "next_evidence": "parent-owned compact Hilbert source selector",
            "valid_for_claim": False,
        },
        {
            "closure_id": "EM2502_4_epsilon_bound",
            "object": "epsilon_M absolute envelope",
            "formula_or_condition": "abs(epsilon_M)<=abs(epsilon_worldtube)+abs(I_commutator)+abs(R_eq)+abs(B_zero_flux)+abs(epsilon_extra)+abs(epsilon_calibration)",
            "status": "EXACT_ABSOLUTE_NONCLAIM_LEDGER",
            "blocker": "all component rows are missing theorem-zero or numeric source-backed values",
            "next_evidence": "zero package or source-backed finite rows",
            "valid_for_claim": False,
        },
        {
            "closure_id": "EM2502_5_verdict",
            "object": "epsilon_M=0 for current branch",
            "formula_or_condition": "Measured source closure for Newton/local-GR",
            "status": "EPSILON_M_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "blocker": "topological route is promising but not yet the same measured Hilbert source object",
            "next_evidence": "2183/2503 worldtube-Hilbert selector or finite R_eq/B_zero/I_commutator row",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def qr_binding_rows() -> list[dict[str, Any]]:
    raw = read_csv_first_row(RAW_QRHAT)
    q_text = raw.get("q_R_hat", "MISSING_Q_R_HAT")
    try:
        q_value = float(q_text)
        delta_p_ceiling = abs(q_value) / 2.0
        delta_p_text = f"{delta_p_ceiling:.12e}"
        raw_status = "FINITE_NONCLAIM_CEILING"
    except (TypeError, ValueError):
        delta_p_text = "MISSING_DELTA_P_BOUND"
        raw_status = "MISSING_OR_NONNUMERIC"

    rows = [
        {
            "binding_id": "QRB2502_0_zero_flux",
            "route": "Q_R=0 theorem",
            "input": "Q_R=0 plus W>0, J_R=0 exterior, C_R(infinity)=0",
            "result": "C_R=0 and delta_p=0",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "binding_id": "QRB2502_1_finite_qrhat_guardrail",
            "route": "finite q_R_hat ceiling",
            "input": q_text,
            "result": f"abs(delta_p)<=abs(q_R_hat)/2 = {delta_p_text}",
            "status": raw_status,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "binding_id": "QRB2502_2_v_branch_relation",
            "route": "u/v constrained branch",
            "input": "u=C_R/2=0 before readout; v source normalized by parent action",
            "result": "Q_R hair is absent only if boundary/source/readout cannot reintroduce u or C_R",
            "status": "BETTER_ROUTE_BUT_STILL_CONDITIONAL",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "binding_id": "QRB2502_3_full_vector",
            "route": "local PPN/Newton vector",
            "input": "delta_p, beta/kappa_v, delta_KC, epsilon_M, boundary/readout tails",
            "result": "vector remains not score-ready",
            "status": "LOCAL_GR_CLAIM_BLOCKED",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2502_0_internal_progress",
            "claim": "2502 may treat the u/v/H_core chain as the best current derivation route",
            "status": "PASS_INTERNAL_NONCLAIM",
            "reason": "existing sources derive exact conditional reductions and coefficient laws",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2502_1_QR_zero",
            "claim": "parent theory derives Q_R=0",
            "status": "BLOCKED",
            "reason": "bulk u=0 route still lacks parent order, boundary zero flux and source/readout silence",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2502_2_Newton",
            "claim": "Newton limit is derived",
            "status": "BLOCKED",
            "reason": "delta_KC and epsilon_M are not parent-zero or source-backed finite values",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2502_3_PPN_beta",
            "claim": "PPN beta=1 is derived",
            "status": "BLOCKED",
            "reason": "kappa_v zero/gauge theorem is not signed and no finite kappa_v row is live",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2502_4_local_GR",
            "claim": "local GR/Newton reduction is derived",
            "status": "BLOCKED",
            "reason": "source normalization, conservation, boundary, matter universality and PPN vector gates remain open",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2502_5_no_shortcuts",
            "claim": "closure, gamma-only, fitted-GM or closed-wrong-charge route can pass",
            "status": "PASS_GUARDRAIL",
            "reason": "2502 explicitly rejects all shortcut promotions",
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2502_0_gain",
            "decision": "LOCAL_ROUTE_NARROWED_TO_UV_SOURCE_SPINE",
            "reason": "raw Q_R zero is not derived, but u=0 plus v-only readout gives an exact conditional route",
            "effect": "future work should stop circling generic Q_R and attack source/order coefficients",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2502_1_newton",
            "decision": "NEWTON_REQUIRES_DELTAKC_AND_EPSILONM",
            "reason": "Delta_Newton_v=(1+delta_KC)(1+epsilon_M)-1",
            "effect": "both action coefficient ratio and mass-current glue must close or become finite rows",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2502_2_beta",
            "decision": "BETA_REDUCED_TO_KAPPA_V",
            "reason": "beta-1=kappa_v/2 in the constrained v branch",
            "effect": "prove kappa_v=0/gauge or source a finite kappa_v row",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2502_3_source",
            "decision": "TOPOLOGICAL_ROUTE_PROMISING_BUT_NOT_SAME_OBJECT_YET",
            "reason": "closed J_M_top is not measured mass unless Pi_M J_H=J_M_top+dB_zero and zero boundary flux",
            "effect": "next target is worldtube-Hilbert source selector and R_eq/B_zero zero or finite rows",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2502_4_github",
            "decision": "NO_GITHUB_ACTION",
            "reason": "branch is private derivation/gatekeeping and not a clean public WIP snapshot",
            "effect": "continue private goal work only",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2502_0_selected",
            "selection_status": "selected",
            "target_file": "2503-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R-eq-fill.md",
            "target_script": "scripts/Y5_R2FR_worldtube_Hilbert_source_selector_and_zero_boundary_flux_or_R_eq_fill_2503.py",
            "task": "derive the parent-owned compact Hilbert source worldtube, same-frame source measure, topological representative, and zero boundary flux for the constrained v branch; otherwise fill R_eq/B_zero/I_commutator finite rows",
            "acceptance_target": "W_source, rho_H dV_H, observed time generator, J_M_top=PD(W_source), R_eq=0, B_zero_flux=0, and no extra current channels are parent-signed; otherwise source-backed nonclaim rows exist",
            "guardrails": "do not use a closed wrong topological charge, late equality multiplier, reference-only zero, post-readout worldtube, fitted GM calibration, gamma-only pass, or GitHub action",
            "valid_for_claim": False,
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "hcore_qr": OUTPUTS["hcore_qr"],
        "uv_spine": OUTPUTS["uv_spine"],
        "coefficient_law": OUTPUTS["coefficient_law"],
        "epsilonM": OUTPUTS["epsilonM"],
        "next_target": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2502_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(
            stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": notes,
                    "detail": detail,
                    "valid_for_claim": False,
                }
            )
        )

    add("VAL2502_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2502_01_hcore_verdict",
        any(row["audit_id"] == "HQR2502_5_current_verdict" and row["status"] == "PARENT_QR_ZERO_NOT_DERIVED_CURRENT_CORPUS" for row in data["hcore_qr"]),
        "H_core/Q_R source equation remains unsigned rather than overclaimed",
    )
    add(
        "VAL2502_02_uv_spine",
        any(row["spine_id"] == "UV2502_1_constrained_readout" and row["status"] == "EXACT_CONDITIONAL_READOUT" for row in data["uv_spine"]),
        "u/v constrained readout spine is recorded",
    )
    add(
        "VAL2502_03_newton_ppn_laws",
        any(row["law_id"] == "LAW2502_2_Delta_Newton_v" for row in data["coefficient_law"])
        and any(row["law_id"] == "LAW2502_4_beta" for row in data["coefficient_law"]),
        "Delta_Newton_v and beta/kappa_v laws are present",
    )
    add(
        "VAL2502_04_epsilonM_blocked",
        any(row["closure_id"] == "EM2502_5_verdict" and row["status"] == "EPSILON_M_ZERO_NOT_DERIVED_CURRENT_CORPUS" for row in data["epsilonM"]),
        "epsilon_M source closure remains blocked",
    )
    add(
        "VAL2502_05_qr_binding_nonclaim",
        all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["qr_binding"]),
        "Q_R/delta_p rows remain nonclaim and not score-ready",
    )
    add(
        "VAL2502_06_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["gates"]),
        "all claim gates deny public/local-GR/Newton promotion",
    )
    add(
        "VAL2502_07_next_target",
        any(row["route_id"] == "NEXT2502_0_selected" for row in data["next"]),
        "2503 worldtube-Hilbert source selector target selected",
    )
    add(
        "VAL2502_08_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2502*", "*P8_Y5_NO_SHADOW_2502*", "*JR2502*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2502_09_no_formalization_artifacts", not formalization_artifacts, "no 2502 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2502_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2502_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2502_OVERALL",
        overall,
        "2502 integrates Q_R/H_core with the u/v local source spine, keeps claims blocked, and selects worldtube-Hilbert source closure next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2502 Y5 R2FR Parent Hcore QR Source Equation Or Boundary Charge Owner",
        "",
        "**Status:** private nonclaim synthesis checkpoint. It does not derive local GR/Newton, but it does splice the live `Q_R/delta_p` branch into the stronger `u/v/H_core` reduction chain.",
        "",
        "**Main result:** raw `Q_R=0` is still not parent-derived. The best route is now sharper: derive parent-owned `u=0` before readout, reconstruct the local coframe from `v`, derive `v=-2U/c^2`, prove `delta_KC=0`, `epsilon_M=0`, and `kappa_v=0`, then close boundary/source/readout re-entry. If this fails, the finite residuals are now named: `delta_KC`, `epsilon_M`, `kappa_v`, `R_eq`, `B_zero_flux`, and `I_commutator`.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Hcore / QR Source Equation Audit",
        markdown_table(data["hcore_qr"], ["audit_id", "object", "statement", "status", "what_it_buys", "what_is_missing", "valid_for_claim"]),
        "",
        "## U/V Reduction Spine",
        markdown_table(data["uv_spine"], ["spine_id", "result", "status", "claim_effect", "remaining_gate", "valid_for_claim"]),
        "",
        "## Newton / PPN Coefficient Law",
        markdown_table(data["coefficient_law"], ["law_id", "quantity", "formula", "meaning", "status", "needed_for_zero", "valid_for_claim"]),
        "",
        "## Epsilon_M Source Closure Ledger",
        markdown_table(data["epsilonM"], ["closure_id", "object", "formula_or_condition", "status", "blocker", "next_evidence", "valid_for_claim"]),
        "",
        "## QR / Delta_p Binding Status",
        markdown_table(data["qr_binding"], ["binding_id", "route", "input", "result", "status", "score_ready", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "status", "reason", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BETA_DOCS.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register_rows(),
        "hcore_qr": hcore_qr_rows(),
        "uv_spine": uv_spine_rows(),
        "coefficient_law": coefficient_law_rows(),
        "epsilonM": epsilonM_rows(),
        "qr_binding": qr_binding_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["hcore_qr"], data["hcore_qr"])
    write_csv(OUTPUTS["uv_spine"], data["uv_spine"])
    write_csv(OUTPUTS["coefficient_law"], data["coefficient_law"])
    write_csv(OUTPUTS["epsilonM"], data["epsilonM"])
    write_csv(OUTPUTS["qr_binding"], data["qr_binding"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()

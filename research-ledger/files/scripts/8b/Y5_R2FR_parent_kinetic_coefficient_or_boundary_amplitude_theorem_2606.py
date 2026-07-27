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

BRANCH_ID = "MTS_R2FR_KINETIC_ELLIPTIC_REBASE_2606"
CHECKPOINT_ID = "2606"

DOC = ROOT / "2606-Y5-R2FR-parent-kinetic-coefficient-or-boundary-amplitude-theorem.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_LINEAGE_LEDGER.csv",
    "kinetic_gap": OUT / "P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_KINETIC_GAP_THEOREM.csv",
    "boundary_amplitude": OUT / "P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_BOUNDARY_AMPLITUDE_THEOREM.csv",
    "coefficient_audit": OUT / "P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_COEFFICIENT_PROVENANCE_AUDIT.csv",
    "elliptic_ownership": OUT / "P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_ELLIPTIC_FUNCTIONAL_OWNERSHIP_GATE.csv",
    "variation_theorem": OUT / "P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_VARIATION_THEOREM.csv",
    "finite_residual_vector": OUT / "P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_FINITE_RESIDUAL_VECTOR.csv",
    "candidate_rows": OUT / "P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_CANDIDATE_ROWS.csv",
    "claim_gates": OUT / "P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2606_VALIDATION.csv",
}

COPY_TARGETS = {
    "elliptic_ownership": LOCAL_BOUNDS / "Parent_elliptic_functional_ownership_gate_2606_NONCLAIM.csv",
    "finite_residual_vector": LOCAL_BOUNDS / "Finite_local_residual_vector_2606_NONCLAIM.csv",
    "next_target": QUEUE / "JR2606_SOURCE_SUPPORT_OR_BOUNDARY_NOFLUX_NEXT.csv",
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


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2606_00_2605_handoff_doc",
            "source_path": ROOT / "2605-Y5-R2FR-gap-beta-tau-source-package-validator-or-parent-row.md",
            "needles": ["NEXT2605_0_selected", "MPC2605_0_mu_m2_gradient", "VAL2605_OVERALL"],
            "role": "current branch handoff selecting parent kinetic coefficient or boundary amplitude theorem",
        },
        {
            "source_id": "SRC2606_01_2605_candidates",
            "source_path": OUT / "P8_Y5_PACKAGE_VALIDATOR_REBASE_2605_MU_PHI_CANDIDATE_ROWS.csv",
            "needles": ["MPC2605_0_mu_m2_gradient", "MPC2605_2_Phi_S_gradient", "MPC2605_5_Qalg_feed"],
            "role": "current symbolic mu/Phi candidate rows",
        },
        {
            "source_id": "SRC2606_02_2605_acquisition",
            "source_path": OUT / "P8_Y5_PACKAGE_VALIDATOR_REBASE_2605_ACQUISITION_QUEUE.csv",
            "needles": ["ACQ2605_0_kappa_m", "ACQ2605_2_A_S", "ACQ2605_5_DeltaK"],
            "role": "current coefficient and boundary acquisition queue",
        },
        {
            "source_id": "SRC2606_03_1750_doc",
            "source_path": ROOT / "1750-Y5-R2FR-parent-kinetic-coefficient-or-boundary-amplitude-theorem.md",
            "needles": ["KGT1750_0_variational_completion", "BAT1750_5_verdict", "NEXT1750_0_primary", "VAL1750_OVERALL"],
            "role": "prior kinetic coefficient and boundary amplitude theorem",
        },
        {
            "source_id": "SRC2606_04_1750_kinetic",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1750_KINETIC_GAP_THEOREM.csv",
            "needles": ["KGT1750_1_canonical_normalization", "KGT1750_2_trace_stiffness_separation", "KGT1750_5_verdict"],
            "role": "R-lock variational kinetic/gap theorem",
        },
        {
            "source_id": "SRC2606_05_1750_boundary",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1750_BOUNDARY_AMPLITUDE_THEOREM.csv",
            "needles": ["BAT1750_1_nohair_zero_case", "BAT1750_2_finite_source_bound", "BAT1750_5_verdict"],
            "role": "conditional nohair and finite Phi_S amplitude theorem",
        },
        {
            "source_id": "SRC2606_06_1750_coefficients",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1750_COEFFICIENT_PROVENANCE_AUDIT.csv",
            "needles": ["CPA1750_0_D_m", "CPA1750_7_A_S", "CPA1750_10_verdict"],
            "role": "coefficient provenance blocker audit",
        },
        {
            "source_id": "SRC2606_07_1751_doc",
            "source_path": ROOT / "1751-Y5-R2FR-parent-elliptic-functional-ownership-or-finite-residual-vector.md",
            "needles": ["EFO1751_7_verdict", "VAR1751_5_finite_branch", "NEXT1751_0_primary", "VAL1751_OVERALL"],
            "role": "prior parent elliptic functional ownership or finite residual vector",
        },
        {
            "source_id": "SRC2606_08_1751_ownership",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1751_ELLIPTIC_FUNCTIONAL_OWNERSHIP_CONTRACT.csv",
            "needles": ["EFO1751_0_functional_candidate", "EFO1751_4_source_owner", "EFO1751_7_verdict"],
            "role": "elliptic functional ownership contract",
        },
        {
            "source_id": "SRC2606_09_1751_variation",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1751_VARIATION_THEOREM.csv",
            "needles": ["VAR1751_0_constant_coefficient_variation", "VAR1751_4_nohair_branch", "VAR1751_5_finite_branch"],
            "role": "exact conditional variation theorem",
        },
        {
            "source_id": "SRC2606_10_1751_residual_vector",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1751_FINITE_RESIDUAL_VECTOR.csv",
            "needles": ["RV1751_0_source_leak", "RV1751_3_boundary_flux", "RV1751_10_verdict"],
            "role": "finite local residual vector replacing hidden plateau",
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
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "LIN2606_0_2605",
            "checkpoint": "2605",
            "question": "Which parent coefficients are now concrete bottlenecks?",
            "result": "mu_m2/Phi_S contracts require kappa_m/Z_m, F2/L0, A_S, boundary class, source support, projection norms and DeltaK.",
            "status": "CURRENT_HANDOFF_REBASED",
            "next_dependency": "kinetic coefficient or boundary amplitude theorem",
        },
        {
            "step_id": "LIN2606_1_1750",
            "checkpoint": "1750",
            "question": "Can the coefficient/amplitude theorem be derived?",
            "result": "Yes conditionally: variational R-lock gives mu_m2=mu_B/D_m, Phi_S=sqrt(D_m)|delta_m|_boundary, and finite/nohair amplitude laws.",
            "status": "CONDITIONAL_THEOREM_DERIVED_NONCLAIM",
            "next_dependency": "parent elliptic functional ownership",
        },
        {
            "step_id": "LIN2606_2_1751",
            "checkpoint": "1751",
            "question": "Is the elliptic functional parent-owned enough for local-GR reentry?",
            "result": "No. The functional contract is written, but source, boundary, stress exchange, coefficients and residual rows remain unowned.",
            "status": "OWNERSHIP_NOT_CLOSED_RESIDUAL_VECTOR_ACTIVE",
            "next_dependency": "source support or boundary no-flux first residual zero/bound",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def kinetic_gap_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "KGT2606_0_variational_completion",
            "object": "stationary R-lock equation",
            "premise": "D_m Delta_h delta_m - mu_B delta_m = -J_eff",
            "derived_result": "if this is the Euler equation of E_m=int[0.5 D_m |grad delta_m|^2 + 0.5 mu_B delta_m^2 - J_eff delta_m], then D_m is the kinetic coefficient and mu_B is the quadratic restoring coefficient",
            "status": "EXACT_CONDITIONAL_VARIATIONAL_COMPLETION",
            "missing_to_promote": "MISSING_PARENT_E_M;MISSING_D_M_SIGN_UNITS;MISSING_MU_B_FLOOR;MISSING_FIELD_STATUS;MISSING_SOURCE_DEFINITION",
        },
        {
            "theorem_id": "KGT2606_1_canonical_normalization",
            "object": "canonical field conversion",
            "premise": "phi=sqrt(D_m) delta_m",
            "derived_result": "E_m=int[0.5 |grad phi|^2 + 0.5 (mu_B/D_m) phi^2 - (J_eff/sqrt(D_m)) phi], so mu_m2=mu_B/D_m and ell_scr=sqrt(D_m/mu_B)",
            "status": "EXACT_CONDITIONAL_CANONICAL_GAP",
            "missing_to_promote": "MISSING_VARIATIONAL_OWNERSHIP;MISSING_D_M;MISSING_MU_B;MISSING_UNITS",
        },
        {
            "theorem_id": "KGT2606_2_trace_stiffness_separation",
            "object": "Gamma_eff trace response",
            "premise": "F2=a_F lambda_R=a_F mu_B/gamma_B",
            "derived_result": "readout trace stiffness F2 is not automatically the same as the dynamical screening gap mu_B/D_m; local safety needs both bounded separately",
            "status": "EXACT_SEPARATION_DERIVED",
            "missing_to_promote": "MISSING_a_F;MISSING_lambda_R;MISSING_gamma_B;MISSING_TRACE_GRADIENT_OWNERSHIP",
        },
        {
            "theorem_id": "KGT2606_3_old_bridge_compatibility",
            "object": "old kappa_m branch",
            "premise": "old bridge uses mu_m2=F2/(kappa_m L0^2)",
            "derived_result": "it matches R-lock only if the parent map identifies kappa_m with D_m and F2/L0 with mu_B conventions",
            "status": "BRIDGE_COMPATIBILITY_CONDITION_DERIVED",
            "missing_to_promote": "MISSING_PARENT_MAP_KAPPA_D;MISSING_PARENT_MAP_F2_MU;MISSING_L0_CONVENTION",
        },
        {
            "theorem_id": "KGT2606_4_verdict",
            "object": "kinetic/gap theorem",
            "premise": "D_m route is sharper than kappa_m placeholder",
            "derived_result": "2606 accepts mu_m2=mu_B/D_m as the clean conditional contract but not as a prediction",
            "status": "THEOREM_CONTRACT_DERIVED_PARENT_OWNERSHIP_MISSING",
            "missing_to_promote": "MISSING_PARENT_ELLIPTIC_FUNCTIONAL;MISSING_SOURCE_BOUNDARY_PREMISES",
        },
    ]
    return [with_stamp({**row, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def boundary_amplitude_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "BAT2606_0_coercive_energy_identity",
            "object": "positive screened operator",
            "premise": "(-D_m Delta_h + mu_B) delta_m = J_eff with D_m>0, mu_B>=mu_min>0",
            "derived_result": "multiplying by delta_m gives int D_m|grad delta_m|^2 + int mu_B delta_m^2 = int J_eff delta_m + boundary_flux",
            "status": "EXACT_CONDITIONAL_ENERGY_IDENTITY",
            "missing_to_promote": "MISSING_SOURCE_TERM;MISSING_BOUNDARY_FLUX_CLASS;MISSING_DOMAIN_REGULARITY;MISSING_OPERATOR_OWNERSHIP",
        },
        {
            "theorem_id": "BAT2606_1_nohair_zero_case",
            "object": "zero source and silent boundary",
            "premise": "J_eff=0 and boundary_flux=0 with coercive D_m,mu_B",
            "derived_result": "energy identity forces delta_m=0; hence Phi_S=0 and the screened local profile is exact-zero in that branch",
            "status": "EXACT_CONDITIONAL_NOHAIR_THEOREM",
            "missing_to_promote": "MISSING_SOURCE_SILENCE;MISSING_BOUNDARY_NOFLUX;MISSING_PARENT_OWNED_COERCIVITY",
        },
        {
            "theorem_id": "BAT2606_2_finite_source_bound",
            "object": "finite source amplitude",
            "premise": "nonzero J_eff and finite boundary mismatch",
            "derived_result": "||delta_m|| is bounded by boundary term plus source/mu_B; in canonical units Phi_S <= sqrt(D_m)[M_bdy exp(-d/ell_scr)+M_src+M_mL+M_nl]",
            "status": "CONDITIONAL_AMPLITUDE_BOUND_DERIVED",
            "missing_to_promote": "MISSING_M_BDY;MISSING_M_SRC;MISSING_M_ML;MISSING_M_NL;MISSING_D_M;MISSING_MU_B",
        },
        {
            "theorem_id": "BAT2606_3_shell_obstruction_retained",
            "object": "transition shell",
            "premise": "transition support intersects local domain or boundary projector is not owned",
            "derived_result": "generic U_B or width suppression cannot hide the shell; shell current must be exact-zero/projected out by parent identity or included as finite Q_trans/Q_proj",
            "status": "ANTI_CHEAT_GUARD_RETAINED",
            "missing_to_promote": "MISSING_SHELL_PROJECTOR;MISSING_QTRANS_BOUND;MISSING_BOUNDARY_CLASS",
        },
        {
            "theorem_id": "BAT2606_4_verdict",
            "object": "boundary amplitude theorem",
            "premise": "coercive operator gives exact zero or finite amplitude law",
            "derived_result": "2606 derives the exact branch split: nohair if source/boundary vanish, finite residual vector otherwise",
            "status": "THEOREM_CONTRACT_DERIVED_PREMISES_UNSIGNED",
            "missing_to_promote": "MISSING_SOURCE_SUPPORT;MISSING_BOUNDARY_NOFLUX;MISSING_RESIDUAL_INPUTS",
        },
    ]
    return [with_stamp({**row, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def coefficient_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("CPA2606_0_D_m", "D_m", "kinetic/diffusion coefficient for variational R-lock completion", "SUPPORTED_BY_EQUATION_REGISTER_NOT_PARENT_ACTION", "needs parent action/energy slot, sign, units and source"),
        ("CPA2606_1_mu_B", "mu_B", "quadratic restoring coefficient in local stationary memory equation", "SYMBOLIC_RELAXATION_COEFFICIENT", "needs mu_B floor, source of gamma_B lambda_R or Pi_B/tau_L, and units"),
        ("CPA2606_2_gamma_lambda", "gamma_B;lambda_R", "mobility and curvature of R with mu_B=gamma_B lambda_R", "CONDITIONAL_R_LOCK_ONLY", "R functional, mobility law and microscopic origin not parent-derived"),
        ("CPA2606_3_a_F", "a_F", "trace-readout locking coefficient F2=a_F lambda_R", "MISSING_PARENT_COEFFICIENT", "needed to keep readout stiffness from spoiling local PPN bounds"),
        ("CPA2606_4_kappa_m_Zm", "kappa_m/Z_m", "old gradient-completion kinetic coefficient", "MISSING_Z_M_SIGN_AND_VALUE", "sign, value and source remain missing in old branch"),
        ("CPA2606_5_A_S", "A_S/Phi_S", "boundary/source amplitude at matching surface", "MISSING_PARENT_SOURCE", "requires source support, boundary class and no-growing-branch/no-flux theorem"),
        ("CPA2606_6_boundary_class", "boundary/no-flux/shell class", "condition selecting decaying/nohair branch", "CLOSURE_ONLY_CURRENTLY", "hidden shell/no-flux shortcut rejected"),
        ("CPA2606_7_projection", "A_ref;projection norms", "observable normalization for Q_alg/Q_trans", "MISSING_OPERATOR_PROJECTION_NORMS", "cannot score local arenas without map"),
        ("CPA2606_8_verdict", "coefficient provenance package", "all coefficient rows needed for local claim", "NOT_CLAIM_GRADE", "theorem contracts are sharper but no coefficient row is source-backed enough to score"),
    ]
    return [
        with_stamp(
            {
                "audit_id": audit_id,
                "quantity": quantity,
                "role": role,
                "current_status": status,
                "needed_to_promote": needed,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for audit_id, quantity, role, status, needed in rows
    ]


def elliptic_ownership_rows() -> list[dict[str, Any]]:
    rows = [
        ("EFO2606_0_functional_candidate", "parent-owned local elliptic functional", "E_m=int_Omega sqrt(h)[0.5 D_m h^ij partial_i delta_m partial_j delta_m + 0.5 mu_B delta_m^2 - J_eff delta_m] + E_boundary", "CONTRACT_WRITTEN", "must be derived from parent action/open-system variational principle, not introduced only at local readout"),
        ("EFO2606_1_field_status", "m or delta_m is an independent varied field", "variation is performed before projection, domain selection, and observed readout", "CANDIDATE_NOT_SIGNED", "parent field status and no-metric-composite exclusion unsigned"),
        ("EFO2606_2_positive_coefficients", "D_m>0 and mu_B>=mu_min>0", "coercivity gives nohair/amplitude bounds", "NOT_DERIVED_AS_PARENT_FLOORS", "D_m sign/units and mu_B floor not parent-owned"),
        ("EFO2606_3_covariant_or_controlled_frame", "elliptic h^ij operator is legitimate stationary reduction", "parent supplies u^mu/coframe or covariant hyperbolic action whose stationary local limit is elliptic", "OPEN_SYSTEM_STATUS_ONLY", "effective open-system route is not yet a closed fundamental action"),
        ("EFO2606_4_source_owner", "J_eff is parent-defined", "J_eff collects source, m_L drift, coefficient-gradient, boundary/readout and nonlinear terms with no hidden cancellation", "MISSING_SOURCE_MAP", "source silence and source support powers are not parent-owned"),
        ("EFO2606_5_boundary_owner", "E_boundary/no-flux/no-growing branch is parent-owned", "boundary term is fixed before local test and not tuned to remove PPN residuals", "CLOSURE_ONLY_CURRENTLY", "boundary/no-charge and shell projector unsigned"),
        ("EFO2606_6_stress_exchange_owner", "Hilbert stress and open-system exchange are routed", "using the functional also routes T_m, q^nu and K_hat divergence into residual ledgers", "HARD_RESIDUAL_CONTRACT_NONCLAIM", "screening stress cannot be deleted after using it for local suppression"),
        ("EFO2606_7_verdict", "parent elliptic functional ownership", "EFO2606_0 through EFO2606_6 all parent-signed or source-backed", "OWNERSHIP_NOT_CLOSED", "finite residual vector remains live"),
    ]
    return [
        with_stamp(
            {
                "contract_id": contract_id,
                "clause": clause,
                "required_statement": required,
                "current_status": status,
                "blocker": blocker,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for contract_id, clause, required, status, blocker in rows
    ]


def variation_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        ("VAR2606_0_constant_coefficient_variation", "fixed D_m, mu_B, m_L and h_ij in local domain", "delta E_m=0 gives -D_m Delta_h delta_m + mu_B delta_m = J_eff", "EXACT_CONDITIONAL_VARIATION"),
        ("VAR2606_1_variable_Dm_correction", "D_m=D_m(X_B(x)) varies", "Euler equation becomes -nabla_i(D_m nabla^i delta_m)+mu_B delta_m=J_eff, with coefficient-gradient residuals", "EXACT_CORRECTION_IDENTIFIED"),
        ("VAR2606_2_variable_mL_correction", "m_L=m_L(X_B(x)) varies", "m=m_L+delta_m gives source terms from Delta_h m_L and coefficient gradients; m_L drift cannot be hidden inside delta_m=0", "EXACT_CORRECTION_IDENTIFIED"),
        ("VAR2606_3_source_boundary_identity", "finite source and boundary terms", "coercive identity: int D_m|grad delta_m|^2+int mu_B delta_m^2 = int J_eff delta_m + boundary_flux", "EXACT_CONDITIONAL_ENERGY_IDENTITY"),
        ("VAR2606_4_nohair_branch", "J_eff=0 and boundary_flux=0", "positive D_m and mu_B force delta_m=0, grad delta_m=0, Phi_S=0, and screened profile exact-zero", "EXACT_ZERO_THEOREM_CONDITIONAL"),
        ("VAR2606_5_finite_branch", "one or more premises fail", "all unsilenced source, coefficient, boundary, shell, trace, stress and K_perp pieces must enter finite residual rows", "FINITE_RESIDUAL_BRANCH_REQUIRED"),
    ]
    return [with_stamp({"theorem_id": theorem_id, "case": case, "derived_result": result, "status": status, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}) for theorem_id, case, result, status in rows]


def finite_residual_vector_rows() -> list[dict[str, Any]]:
    rows = [
        ("RV2606_0_source_leak", "R_source", "(1-Pi_B) S_cg", "local source leakage if S_cg is not zero or Pi_B is not exactly local", "MISSING_SOURCE_SUPPORT_THEOREM", "PPN/R10/WEP"),
        ("RV2606_1_mL_drift", "R_mL", "D_m Delta_h m_L + grad D_m dot grad m_L", "environmental equilibrium drift reappears even when delta_m is small", "MISSING_LOCAL_FIXED_POINT_OR_CONSTANT_mL", "PPN/local"),
        ("RV2606_2_coefficient_gradient", "R_coeff", "grad D_m dot grad delta_m + grad mu_B response terms", "constant-coefficient gap is unsafe if coefficients vary locally", "MISSING_COEFFICIENT_GRADIENT_BOUND", "PPN/R10"),
        ("RV2606_3_boundary_flux", "R_boundary", "boundary_flux or ambient memory mismatch", "nohair proof fails if the local exterior boundary carries an offset", "MISSING_BOUNDARY_NOFLUX_OR_AMBIENT_MATCH", "PPN/local"),
        ("RV2606_4_shell_projector", "R_shell", "transition shell Q_trans/Q_proj contribution", "generic width or U_B suppression cannot hide a local shell", "MISSING_SHELL_PROJECTOR_OR_BOUND", "PPN/R10"),
        ("RV2606_5_trace_gradient", "R_trace", "nabla[L_cg^-2 F_L(X_B)]", "R-lock removes F_1 but not environmental trace gradients", "MISSING_TRACE_BASELINE_CONSTANCY", "PPN/clocks"),
        ("RV2606_6_trace_stiffness", "R_F2", "a_F lambda_R memory-jump quadratic response", "large trace stiffness can fail local bounds even when dynamic gap screens", "MISSING_aF_lambdaR_SOURCE_AND_BOUND", "PPN/R10"),
        ("RV2606_7_memory_stress", "R_Tm", "Hilbert stress from D_m/Z_m gradients, potential, source/bath and boundary terms", "screening kinetic term carries stress that cannot be deleted", "MISSING_MEMORY_STRESS_BOUND", "PPN/local"),
        ("RV2606_8_Kperp", "R_Kperp", "divergence/free transverse tensor residual", "scalar elliptic functional does not kill homogeneous K_perp modes", "MISSING_KPERP_ZERO_OR_BOUND", "PPN/polarization"),
        ("RV2606_9_projection_norms", "R_project", "A_ref, N_div, N_G, N_D and arena maps", "residuals cannot score without observable projection norms", "MISSING_OPERATOR_PROJECTION_NORMS", "all_local"),
        ("RV2606_10_verdict", "finite residual vector", "sum of active R_i rows with no cancellation unless parent identity exists", "finite residual branch replaces hidden local-GR claim", "RESIDUAL_VECTOR_ACTIVE_NONCLAIM", "all_local"),
    ]
    return [
        with_stamp(
            {
                "residual_id": residual_id,
                "quantity": quantity,
                "formula_or_description": formula,
                "role": role,
                "current_status": status,
                "arena_links": arenas,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for residual_id, quantity, formula, role, status, arenas in rows
    ]


def candidate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CAN2606_0_E_m", "E_m functional", "int sqrt(h)[0.5D_m|grad delta_m|^2+0.5mu_B delta_m^2-J_eff delta_m]+E_boundary", "PARENT_OWNERSHIP_CONTRACT_ONLY"),
        ("CAN2606_1_mu_gap", "mu_m^2", "mu_B/D_m only if E_m parent-owned", "THEOREM_CONTRACT_ONLY"),
        ("CAN2606_2_PhiS_boundary", "Phi_S", "sqrt(D_m)|delta_m|_boundary", "THEOREM_CONTRACT_ONLY"),
        ("CAN2606_3_nohair", "Phi_S_zero", "Phi_S=0 only if J_eff=0 and boundary_flux=0 under owned coercive functional", "CONDITIONAL_ZERO_PREMISES_UNSIGNED"),
        ("CAN2606_4_finite_residual_vector", "R_local_vector", "R_source+R_mL+R_coeff+R_boundary+R_shell+R_trace+R_F2+R_Tm+R_Kperp+R_project", "ACTIVE_NONCLAIM_FALLBACK"),
    ]
    return [with_stamp({"row_id": row_id, "quantity": quantity, "formula_or_contract": formula, "current_status": status, "accepted_as_contract": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}) for row_id, quantity, formula, status in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2606_0_Rlock_gap", "mu_m2=mu_B/D_m is claim-grade", "BLOCKED_PARENT_ELLIPTIC_FUNCTIONAL_UNSIGNED"),
        ("CG2606_1_kinetic_coeff", "D_m or kappa_m/Z_m is source-backed", "BLOCKED_COEFFICIENT_SIGN_UNITS_SOURCE"),
        ("CG2606_2_trace_coeff", "F2/a_F/lambda_R is source-backed and PPN-safe", "BLOCKED_TRACE_STIFFNESS_SOURCE"),
        ("CG2606_3_nohair", "Phi_S=0 nohair theorem closes", "BLOCKED_SOURCE_BOUNDARY_PREMISES_UNSIGNED"),
        ("CG2606_4_finite_residual_vector", "finite residual vector can score", "BLOCKED_RESIDUAL_INPUTS_MISSING"),
        ("CG2606_5_local_reentry", "local GR/Newton/PPN/R10/WEP branch can claim", "BLOCKED_NO_LOCAL_REENTRY"),
    ]
    return [with_stamp({"gate_id": gate_id, "claim": claim, "gate_pass": False, "status": "BLOCKED_NO_CLAIM", "blocker": blocker, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}) for gate_id, claim, blocker in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2606_0_kinetic_status",
            "decision": "accept variational R-lock gap as the preferred conditional contract",
            "reason": "if E_m is parent-owned, D_m is the kinetic coefficient and mu_m2=mu_B/D_m",
            "effect": "use D_m/mu_B route before reviving unowned kappa_m placeholders",
        },
        {
            "decision_id": "DEC2606_1_boundary_status",
            "decision": "accept exact branch split: nohair or finite residual",
            "reason": "coercive energy identity gives Phi_S=0 only when source and boundary flux vanish; otherwise finite residual rows are mandatory",
            "effect": "no plateau axiom is allowed",
        },
        {
            "decision_id": "DEC2606_2_ownership_status",
            "decision": "do not promote local GR",
            "reason": "parent elliptic functional ownership is not closed; source, boundary, stress and projection rows remain live",
            "effect": "all local-GR/Newton/PPN/R10/WEP claims remain blocked",
        },
        {
            "decision_id": "DEC2606_3_best_next",
            "decision": "select source-support or boundary no-flux first residual zero/bound",
            "reason": "closing either R_source or R_boundary is the fastest way to test the nohair branch honestly",
            "effect": "2607 should try to zero/bound one live residual row instead of re-arguing the whole functional",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2606_0_selected",
            "selection_status": "selected",
            "target_file": "2607-Y5-R2FR-source-support-or-boundary-no-flux-first-residual-zero-bound.md",
            "target_script": "scripts/Y5_R2FR_source_support_or_boundary_no_flux_first_residual_zero_bound_2607.py",
            "task": "try to close the first residual row needed by the nohair branch: source support R_source=0/bound or boundary flux R_boundary=0/bound; otherwise keep finite residual rows explicit",
            "success_condition": "one residual row becomes parent-zero or source-bounded without promoting local claims until the full vector closes",
            "fallback_condition": "attack shell projector or explicit Q_trans row if source/no-flux rows remain blocked",
            "guardrails": "no plateau axiom; no hidden boundary tuning; no deleting memory stress; no local-GR claim; no GitHub; no formalization-workbench edits",
        },
        {
            "route_id": "NEXT2606_1_shell_fallback",
            "selection_status": "held_fallback",
            "target_file": "2607b-Y5-R2FR-boundary-shell-projector-or-explicit-Qtrans-row.md",
            "target_script": "scripts/Y5_R2FR_boundary_shell_projector_or_explicit_Qtrans_row_2607b.py",
            "task": "attack shell projector/explicit Q_trans if source/no-flux rows remain blocked",
            "success_condition": "transition shell is parent-projected, exact-zero, or enters an explicit finite Q_trans/Q_proj row",
            "fallback_condition": "retain shell as explicit local residual",
            "guardrails": "no generic width suppression; no U_B shell hiding; no local-GR claim",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target_path in COPY_TARGETS.items():
        source_path = OUTPUTS[copy_id]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2606_{copy_id}",
                    "source_path": source_path,
                    "target_path": target_path,
                    "source_exists": source_path.exists(),
                    "target_exists": target_path.exists(),
                    "valid_for_claim": False,
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


def missing_rows_are_not_ready(data: dict[str, list[dict[str, Any]]]) -> bool:
    fields_to_scan = ("current_status", "missing_to_promote", "blocker", "needed_to_promote", "status")
    for rows in data.values():
        for row in rows:
            joined = ";".join(str(row.get(field, "")) for field in fields_to_scan)
            if "MISSING" in joined and (row.get("score_ready") is True or row.get("claim_allowed") is True or row.get("valid_prediction_row") is True):
                return False
    return True


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(with_stamp({"check_id": check_id, "status": "PASS" if condition else "FAIL", "notes": notes, "detail": detail, "valid_for_claim": False}))

    add("VAL2606_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited source paths exist and needles are present")
    add("VAL2606_01_lineage_complete", {"LIN2606_0_2605", "LIN2606_1_1750", "LIN2606_2_1751"} == {row["step_id"] for row in data["lineage"]}, "lineage covers 2605 plus prior 1750-1751")
    add("VAL2606_02_kinetic_gap_recorded", any(row["theorem_id"] == "KGT2606_1_canonical_normalization" for row in data["kinetic_gap"]), "R-lock canonical gap contract is recorded")
    add("VAL2606_03_trace_separated", any(row["theorem_id"] == "KGT2606_2_trace_stiffness_separation" for row in data["kinetic_gap"]), "trace stiffness separated from dynamic gap")
    add("VAL2606_04_nohair_theorem_recorded", any(row["theorem_id"] == "BAT2606_1_nohair_zero_case" for row in data["boundary_amplitude"]), "conditional nohair theorem is recorded")
    add("VAL2606_05_finite_amplitude_bound", any(row["theorem_id"] == "BAT2606_2_finite_source_bound" for row in data["boundary_amplitude"]), "finite Phi_S amplitude bound is recorded")
    add("VAL2606_06_coefficient_audit_blocks", any(row["audit_id"] == "CPA2606_8_verdict" and row["current_status"] == "NOT_CLAIM_GRADE" for row in data["coefficient_audit"]), "coefficient provenance blocks claim-grade promotion")
    add("VAL2606_07_elliptic_ownership_blocks", any(row["contract_id"] == "EFO2606_7_verdict" and row["current_status"] == "OWNERSHIP_NOT_CLOSED" for row in data["elliptic_ownership"]), "elliptic functional ownership remains blocked")
    add("VAL2606_08_variation_theorem_complete", {"VAR2606_0_constant_coefficient_variation", "VAR2606_4_nohair_branch", "VAR2606_5_finite_branch"}.issubset({row["theorem_id"] for row in data["variation_theorem"]}), "variation theorem covers exact, nohair and finite branches")
    add("VAL2606_09_residual_vector_active", any(row["residual_id"] == "RV2606_10_verdict" and row["current_status"] == "RESIDUAL_VECTOR_ACTIVE_NONCLAIM" for row in data["finite_residual_vector"]), "finite residual vector is active and nonclaim")
    add("VAL2606_10_candidate_contracts_nonclaim", all(row["valid_prediction_row"] is False and row["claim_allowed"] is False for row in data["candidate_rows"]), "candidate rows are accepted only as nonclaim contracts")
    add("VAL2606_11_claim_gates_safe", all(row["claim_allowed"] is False and row["gate_pass"] is False for row in data["claim_gates"]), "all claim gates remain blocked")
    add("VAL2606_12_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row promotes scoring or claim flags")
    add("VAL2606_13_missing_not_ready", missing_rows_are_not_ready(data), "no MISSING_* row is marked ready")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2606-Y5-R2FR-parent-kinetic*", "*Y5_R2FR_parent_kinetic*2606*", "*P8_Y5_KINETIC_ELLIPTIC_REBASE_2606*", "*JR2606*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2606_14_no_formalization_artifacts", not formalization_artifacts, "no 2606 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))
    add("VAL2606_15_next_selected", any(row["route_id"] == "NEXT2606_0_selected" and "2607-Y5-R2FR-source-support" in row["target_file"] for row in data["next"]), "2607 source-support or boundary no-flux target selected")
    add("VAL2606_16_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2606_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2606_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2606_OVERALL", overall, "2606 rebases kinetic coefficient, boundary amplitude, elliptic ownership and finite residual vector, then selects first residual zero/bound next")
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [row_value(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2606 Y5 R2FR parent kinetic coefficient or boundary amplitude theorem",
        "",
        "**Status:** private nonclaim rebase checkpoint. The 2605 coefficient target is sharpened using the 1750 kinetic/boundary theorem and the 1751 elliptic-functional ownership gate.",
        "",
        "**Main result:** this is a real derivation step but not a local-GR pass. If the stationary memory equation is parent-owned as a positive elliptic functional, then `D_m` is the kinetic coefficient, `mu_B` is the restoring coefficient, `mu_m2=mu_B/D_m`, and `Phi_S=sqrt(D_m)|delta_m|_boundary`. The coercive identity gives the exact split: `Phi_S=0` only when `J_eff=0` and `boundary_flux=0`; otherwise the local branch must carry an explicit finite residual vector. Current MTS does not yet parent-own the functional, source map, boundary/no-flux class, stress exchange, projection norms, or residual inputs, so no GR/Newton/PPN/R10/WEP claim is made.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Lineage Ledger",
        markdown_table(data["lineage"], ["step_id", "checkpoint", "question", "result", "status", "next_dependency", "valid_for_claim", "claim_allowed"]),
        "",
        "## Kinetic Gap Theorem",
        markdown_table(data["kinetic_gap"], ["theorem_id", "object", "premise", "derived_result", "status", "missing_to_promote", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Boundary Amplitude Theorem",
        markdown_table(data["boundary_amplitude"], ["theorem_id", "object", "premise", "derived_result", "status", "missing_to_promote", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Coefficient Provenance Audit",
        markdown_table(data["coefficient_audit"], ["audit_id", "quantity", "role", "current_status", "needed_to_promote", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Elliptic Functional Ownership Gate",
        markdown_table(data["elliptic_ownership"], ["contract_id", "clause", "required_statement", "current_status", "blocker", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Variation Theorem",
        markdown_table(data["variation_theorem"], ["theorem_id", "case", "derived_result", "status", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Finite Residual Vector",
        markdown_table(data["finite_residual_vector"], ["residual_id", "quantity", "formula_or_description", "role", "current_status", "arena_links", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Candidate Rows",
        markdown_table(data["candidate_rows"], ["row_id", "quantity", "formula_or_contract", "current_status", "accepted_as_contract", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
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
        "## Practical Status",
        "",
        "This is the fork in the road written cleanly. Either source support and boundary flux vanish and the no-hair branch gets teeth, or they do not and the finite residual vector becomes the honest object to test. That is exactly the kind of bridge-to-GR discipline we want: no magic plateau, no hidden shell, no deleted stress.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "kinetic_gap": kinetic_gap_rows(),
        "boundary_amplitude": boundary_amplitude_rows(),
        "coefficient_audit": coefficient_audit_rows(),
        "elliptic_ownership": elliptic_ownership_rows(),
        "variation_theorem": variation_theorem_rows(),
        "finite_residual_vector": finite_residual_vector_rows(),
        "candidate_rows": candidate_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["lineage_ledger"], data["lineage"])
    write_csv(OUTPUTS["kinetic_gap"], data["kinetic_gap"])
    write_csv(OUTPUTS["boundary_amplitude"], data["boundary_amplitude"])
    write_csv(OUTPUTS["coefficient_audit"], data["coefficient_audit"])
    write_csv(OUTPUTS["elliptic_ownership"], data["elliptic_ownership"])
    write_csv(OUTPUTS["variation_theorem"], data["variation_theorem"])
    write_csv(OUTPUTS["finite_residual_vector"], data["finite_residual_vector"])
    write_csv(OUTPUTS["candidate_rows"], data["candidate_rows"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2606_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

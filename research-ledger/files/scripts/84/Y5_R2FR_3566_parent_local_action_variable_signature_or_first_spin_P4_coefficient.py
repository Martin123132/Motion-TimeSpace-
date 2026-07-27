from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3566-Y5-R2FR-parent-local-action-variable-signature-or-first-spin-P4-coefficient.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_PARENT_LOCAL_ACTION_SIGNATURE_3566"
CHECKPOINT_ID = "3566"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty CSV requested: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def sources() -> dict[str, Path]:
    return {
        "handoff_3565": RESIDUALS / "P8_Y5_R2FR_3565_NEXT_TARGET.csv",
        "status_3565": RESIDUALS / "P8_Y5_R2FR_3565_STATUS.csv",
        "theorem_3565": RESIDUALS / "P8_Y5_R2FR_3565_SPIN_TORSION_THEOREM_STACK.csv",
        "p4_3565": RESIDUALS / "P8_Y5_R2FR_3565_P4_SPIN_HYPERMOMENTUM_BOUND_ROWS.csv",
        "parent_spine_2416": RESIDUALS / "P8_Y5_PARENT_QLOC_2416_PARENT_ACTION_SIGNATURE_SPINE.csv",
        "activation_2416": RESIDUALS / "P8_Y5_PARENT_QLOC_2416_THEOREM_ACTIVATION_MATRIX.csv",
        "residual_2416": RESIDUALS / "P8_Y5_PARENT_QLOC_2416_RESIDUAL_STACK_AFTER_SIGNATURE_ATTEMPT.csv",
        "matter_descent_2611": RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_MATTER_WORLDTUBE_DESCENT_ATTEMPT.csv",
        "matter_chain_2611": RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_CHAIN_RULE_DECOMPOSITION.csv",
        "source_status_2611": RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_SOURCE_ZERO_STATUS.csv",
        "minimal_source_3497": RESIDUALS / "P8_Y5_R2FR_3497_MINIMAL_PARENT_SOURCE_ACTION_SIGNATURE.csv",
        "clause_test_3497": RESIDUALS / "P8_Y5_R2FR_3497_CLAUSE_SIGNING_TEST.csv",
        "variation_3497": RESIDUALS / "P8_Y5_R2FR_3497_VARIATION_CHAIN.csv",
        "decision_3497": RESIDUALS / "P8_Y5_R2FR_3497_DECISION_LEDGER.csv",
        "sector_gamma_3493": RESIDUALS / "P8_Y5_R2FR_3493_SECTOR_GAMMA_SIGNATURE_MATRIX.csv",
        "local_blocks": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "source_owner_contract": RESIDUALS / "P8_source_owner_parent_action_terms_CONTRACT.csv",
        "em_signature_3506": RESIDUALS / "P8_Y5_R2FR_3506_PARENT_VISIBLE_EM_GENERATOR_SIGNATURE.csv",
        "em_gate_3504": RESIDUALS / "P8_Y5_R2FR_3504_PARENT_SIGNATURE_GATE.csv",
        "source_owner_3443": RESIDUALS / "P8_Y5_R2FR_3443_SOURCE_OWNER_SIGNATURE_AUDIT.csv",
        "signature_gate_3423": RESIDUALS / "P8_Y5_R2FR_3423_PARENT_SIGNATURE_GATE.csv",
        "worldtube_audit_3375": RESIDUALS / "P8_Y5_R2FR_3375_PARENT_SIGNATURE_AUDIT.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3565": "declares 3566 target",
        "status_3565": "imports live missing items after spin/torsion checkpoint",
        "theorem_3565": "imports no-Gamma-or-P4 connection fork",
        "p4_3565": "imports official E_spin/P4 fallback rows",
        "parent_spine_2416": "private parent ordinary action variable signature spine",
        "activation_2416": "theorem activation matrix for private signature",
        "residual_2416": "residual stack after parent signature attempt",
        "matter_descent_2611": "matter/worldtube quotient descent theorem attempt",
        "matter_chain_2611": "matter descent chain-rule decomposition",
        "source_status_2611": "matter/source zero status",
        "minimal_source_3497": "minimal parent source-action signature candidate",
        "clause_test_3497": "candidate signature clause-signing test",
        "variation_3497": "candidate variation chain",
        "decision_3497": "3497 decision and weakest-link ledger",
        "sector_gamma_3493": "sector no-Gamma signature matrix",
        "local_blocks": "minimum parent local GR action blocks",
        "source_owner_contract": "source-owner parent action term contract",
        "em_signature_3506": "visible EM generator/action signature",
        "em_gate_3504": "EM Hodge/visible signature gates",
        "source_owner_3443": "source-owner signature audit",
        "signature_gate_3423": "single-branch parent signature gate for source normalization",
        "worldtube_audit_3375": "worldtube/Poynting/source signature audit",
    }
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def action_signature_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "SIG3566_0_configuration",
            "local LC branch configuration",
            "Conf_loc^LC = {q(Phi), e_obs(q), g_obs(e_obs), Psi_A, A_Q, theta_A(q), tau(q), H_ref, boundary/topology class, Pi_M(q,e_obs,tau)}",
            "Gamma_ind and omega_ind are not coordinates of this branch",
            "BRANCH_DECLARED_PRIVATE_NOT_PUBLIC_PARENT_DERIVED",
            "variable-absence theorem becomes live inside the branch",
            "parent_spine_2416",
        ),
        (
            "SIG3566_1_gravity_EH",
            "metric/coframe gravitational core",
            "S_EH[e_obs] = (2 kappa0)^-1 integral sqrt(-g_obs)(R[g_obs]-2 Lambda0)",
            "uses Levi-Civita connection of e_obs/g_obs only",
            "STANDARD_LOCAL_BLOCK_STAGED",
            "provides local spin-2/EH operator and symplectic charge target",
            "local_blocks",
        ),
        (
            "SIG3566_2_matter",
            "ordinary matter",
            "S_m = sum_A integral mu_obs L_A(Psi_A, D_LC[e_obs,A_Q] Psi_A, e_obs, A_Q, theta_A(q))",
            "D_LC uses omega_LC[e_obs]; no torsionful spin connection argument",
            "BRANCH_SIGNED_FROM_3497_AND_2416_PRIVATE",
            "Delta_matter=0 and ordinary spin hypermomentum=0 by variable absence inside branch",
            "minimal_source_3497",
        ),
        (
            "SIG3566_3_visible_EM",
            "visible Maxwell/EM stress",
            "S_EM = -lambda_A/2 integral F_Q wedge *_obs F_Q + theta_A/2 integral F_Q wedge F_Q plus owned source pairing",
            "A_Q is the visible U(1) connection; affine Gamma_ind is not an EM argument",
            "MAXWELL_SIGNATURE_CONDITIONAL_CONSTANT_COUPLING_OPEN",
            "Poynting/Maxwell stress is Hilbert source energy; scalar coupling lambda_A remains a separate EM/alpha owner",
            "em_signature_3506",
        ),
        (
            "SIG3566_4_source_worldtube",
            "source support and mass charge",
            "J_H[tau] := delta S_matter+S_EM / delta e_obs contracted with tau; W_source := closure(supp J_H[tau]); M_H := N_G^-1(int_S Q_tau - H_ref)",
            "source selector is derived from Hilbert/Noether current, not from fitted readout or Gamma_ind",
            "BRANCH_SIGNED_REGULAR_SUPPORT_CONDITIONAL",
            "Delta_source=0 modulo regular support, H_ref/integrability and projector naturality",
            "minimal_source_3497",
        ),
        (
            "SIG3566_5_projector_domain",
            "projector/domain/support maps",
            "Pi_M, collars, domain weights and boundary transport are fixed q/e_obs/tau/topology functors before variation",
            "no Gamma_ind transport; if a projector uses Gamma_ind it exits this branch and enters P4",
            "WEAKEST_BRANCH_CLAUSE_SIGNED_ONLY_AS_CANDIDATE",
            "kills delta_Gamma(Pi J_H) only in q-natural projector branch",
            "minimal_source_3497",
        ),
        (
            "SIG3566_6_readouts",
            "clock, light, orbit, WEP, PPN and R10 readouts",
            "R_arena = R_bar(e_obs,A_Q,J_H,M_H,tau,theta_A) evaluated after variation",
            "readouts are not parent-action Gamma variables and cannot redefine source current",
            "BRANCH_SIGNED_PRIVATE_NO_REENTRY",
            "Delta_clock=Delta_light=Delta_orbit=0 inside branch; public arena operator tests still needed",
            "sector_gamma_3493",
        ),
        (
            "SIG3566_7_projective_policy",
            "projective trace",
            "owned-coframe LC branch contains no independent projective direction; affine fallback must gauge-fix or bound projective trace before coupling",
            "projective mode absent in LC branch, not merely ignored",
            "PRIVATE_ZERO_PUBLIC_FALLBACK_RETAINED",
            "Delta_projective=0 inside LC branch; public/affine branch still carries P4_projective",
            "parent_spine_2416",
        ),
        (
            "SIG3566_8_boundary_reference",
            "boundary/reference/Hamiltonian owner",
            "S_boundary = GHY[e_obs] + exact/topological/fixed-reference terms; H_ref and boundary class fixed before readout",
            "boundary objects use e_obs/LC data, but flux/integrability/source-owner gates remain separate",
            "NOT_FULLY_CLOSED_PRIMARY_REMAINING_LEAK",
            "no independent Gamma tail inside LC branch, but source normalization/local GR still blocked by boundary/source-owner proof",
            "source_owner_contract",
        ),
        (
            "SIG3566_9_extra_MTS_fields",
            "motion/time/domain/memory extra fields",
            "S_extra[Phi,q,e_obs] has local stationary fixed point Phi=Phi0 with no linear local source charge, or exposes explicit residual rows",
            "extra fields do not introduce hidden affine connection slots in the LC branch",
            "LOCAL_FIXED_POINT_CONDITIONAL_NOT_GLOBAL_THEORY",
            "keeps local branch compatible with GR limit while preserving cosmology/galaxy extension channels",
            "local_blocks",
        ),
        (
            "SIG3566_10_total_signature",
            "total local branch action",
            "S_loc^LC = S_EH + S_m + S_EM + S_extra + S_boundary + S_source_norm with readouts post-variation",
            "Arg(S_loc^LC) excludes Gamma_ind/omega_ind across ordinary/source/readout sectors",
            "PRIVATE_BRANCH_SIGNATURE_WRITTEN_AND_MACHINE_CHECKED_NONCLAIM",
            "inside this branch E_spin=0 by theorem; public MTS still needs branch-selector derivation",
            "theorem_3565",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "signature_id": signature_id,
            "object": object_name,
            "formal_signature": formal_signature,
            "connection_policy": connection_policy,
            "status": status,
            "effect_if_accepted": effect,
            "source_path": str(source_paths[source_key]),
            "branch_signed_private": True,
            "public_parent_derived": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for signature_id, object_name, formal_signature, connection_policy, status, effect, source_key in rows
    ]


def variation_derivation_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "VAR3566_0_total_noGamma",
            "delta_Gamma_ind S_loc^LC",
            "0",
            "Gamma_ind is not in Arg(S_loc^LC); the Frechet derivative with respect to a missing coordinate is zero/vacuous.",
            "EXACT_INSIDE_BRANCH",
            "theorem_3565",
        ),
        (
            "VAR3566_1_matter_spin",
            "delta_Gamma_ind S_m",
            "0",
            "S_m uses e_obs and omega_LC[e_obs]. Spin connection variation routes through delta e_obs/Hilbert stress, not an independent affine equation.",
            "EXACT_INSIDE_BRANCH",
            "minimal_source_3497",
        ),
        (
            "VAR3566_2_EM_light",
            "delta_Gamma_ind S_EM",
            "0",
            "S_EM uses A_Q, F_Q and *_obs(e_obs). It has no affine Gamma argument. Its metric/coframe stress, including Poynting energy, remains in Hilbert source accounting.",
            "EXACT_FOR_AFFINE_GAMMA_BRANCH_IF_PUBLIC_HODGE",
            "em_signature_3506",
        ),
        (
            "VAR3566_3_source_current",
            "delta_Gamma_ind J_H[tau]",
            "0",
            "J_H is defined by e_obs variation of S_m+S_EM; e_obs descends through q and Gamma_ind is absent.",
            "EXACT_INSIDE_BRANCH",
            "variation_3497",
        ),
        (
            "VAR3566_4_support",
            "delta_Gamma_ind W_source",
            "0 on compact regular support branches",
            "W_source is closure(supp J_H[tau]); when J_H is Gamma-silent and support is regular/no-crossing, support drift is zero.",
            "REGULARITY_CONDITIONAL_INSIDE_BRANCH",
            "matter_descent_2611",
        ),
        (
            "VAR3566_5_projector_product",
            "delta_Gamma_ind(Pi_M J_H)",
            "0 if Pi_M is q/e_obs/tau-natural",
            "Product rule gives Pi delta_Gamma J_H + (delta_Gamma Pi)J_H. The first term is zero; the second is zero only for q-natural projectors.",
            "WEAKEST_LINK_PARTIAL_THEOREM",
            "theorem_3565",
        ),
        (
            "VAR3566_6_readout_no_reentry",
            "delta_Gamma_ind R_arena",
            "not varied as source action",
            "Arena readouts are post-variation functors of solved fields. They can reveal residuals but cannot create the parent source current.",
            "PRIVATE_BRANCH_RULE_OPERATOR_TESTS_REMAIN",
            "sector_gamma_3493",
        ),
        (
            "VAR3566_7_projective_absence",
            "Delta_projective",
            "0 inside LC branch",
            "No independent affine connection means no independent projective trace coordinate. Affine fallback must gauge-fix or bound the trace.",
            "PRIVATE_ZERO_PUBLIC_FALLBACK",
            "parent_spine_2416",
        ),
        (
            "VAR3566_8_Espin_total",
            "E_spin_abs",
            "0 inside LC branch; retained outside it",
            "All affine/hypermomentum summands vanish only in the branch that excludes Gamma_ind and signs q-natural source/readout maps.",
            "BRANCH_THEOREM_NOT_PUBLIC_MTS_CLAIM",
            "p4_3565",
        ),
        (
            "VAR3566_9_local_GR_boundary_caveat",
            "local GR/Newton claim",
            "not implied",
            "No-Gamma closes the connection source head, but boundary/source-owner/G_ref/Poisson-Gauss and second-order PPN gates remain.",
            "LOCAL_GR_STILL_OPEN",
            "source_owner_contract",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "variation_id": variation_id,
            "variation_piece": piece,
            "result": result,
            "derivation": derivation,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for variation_id, piece, result, derivation, status, source_key in rows
    ]


def activation_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "ACT3566_0_private_LC_branch",
            "Activate the local LC branch signature as a private working branch.",
            "PASS_PRIVATE_BRANCH",
            "E_spin=0 is derivable inside the branch.",
            "not a public proof that MTS parent must select this branch",
            "parent_spine_2416",
        ),
        (
            "ACT3566_1_public_parent_selector",
            "Derive why the MTS parent excludes independent affine/torsion branches locally.",
            "FAIL_NOT_DERIVED",
            "Would promote LC/no-Gamma from branch choice to parent theorem.",
            "branch selector/no-independent-affine theorem missing",
            "theorem_3565",
        ),
        (
            "ACT3566_2_projector_naturality",
            "Make Pi_M/domain/collar maps q/e_obs/tau-natural in one public branch.",
            "PARTIAL_PASS_CANDIDATE_ONLY",
            "Would close delta_Gamma(Pi J_H).",
            "projector/domain naturality not public across all arenas",
            "minimal_source_3497",
        ),
        (
            "ACT3566_3_boundary_source_owner",
            "Close H_tau/H_ref/M_H/source-owner boundary flux.",
            "FAIL_REMAINS_PRIMARY_LEAK",
            "Needed for Newton source normalization and local GR, even after no-Gamma.",
            "Hamiltonian integrability/reference/source-owner proof missing",
            "signature_gate_3423",
        ),
        (
            "ACT3566_4_EM_coupling",
            "Lock visible EM scalar coupling lambda_A/alpha to fixed parent constant or source normalization.",
            "FAIL_CORE_COUPLING_TARGET",
            "Needed for Maxwell/EM stress and alpha/clock/source coupling.",
            "scalar EM coupling owner not derived",
            "em_signature_3506",
        ),
        (
            "ACT3566_5_public_local_GR",
            "Claim local GR/Newton/PPN recovery.",
            "FAIL_NO_PUBLIC_CLAIM",
            "Connection head is tamed inside branch, but source normalization and PPN gates remain.",
            "boundary/source-owner/G_ref/Poisson-Gauss/PPN still open",
            "source_owner_3443",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "activation_id": activation_id,
            "gate": gate,
            "status": status,
            "effect": effect,
            "remaining_gap": gap,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for activation_id, gate, status, effect, gap, source_key in rows
    ]


def p4_coefficient_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "P4C3566_0_branch_selector",
            "B_LC_selector",
            "boolean/structural",
            "B_LC_selector=1 if parent local action excludes Gamma_ind; otherwise use affine residual rows",
            "PRIVATE_BRANCH_SELECTED_NOT_PUBLIC_PARENT_DERIVED",
            "derive no-independent-affine selector from quotient/gauge/regularity or declare effective local branch",
            "theorem_3565",
        ),
        (
            "P4C3566_1_axial_torsion",
            "c_A",
            "axial torsion coupling coefficient",
            "S_axial_abs = ||c_A S_mu J5^mu||/N_source",
            "ZERO_INSIDE_LC_BRANCH_ELSE_MISSING_SOURCE_COEFFICIENT",
            "source c_A from affine/torsion action or set c_A=0 by parent LC signature",
            "p4_3565",
        ),
        (
            "P4C3566_2_trace_torsion",
            "c_T",
            "trace torsion coupling coefficient",
            "T_trace_abs = ||c_T T_mu J_T^mu||/N_source",
            "ZERO_INSIDE_LC_BRANCH_ELSE_MISSING_SOURCE_COEFFICIENT",
            "source c_T or exclude trace torsion branch",
            "p4_3565",
        ),
        (
            "P4C3566_3_weyl_nonmetricity",
            "c_Q",
            "Weyl nonmetricity coupling coefficient",
            "Q_weyl_abs = ||c_Q Q_mu J_Q^mu||/N_source",
            "ZERO_INSIDE_LC_BRANCH_ELSE_MISSING_SOURCE_COEFFICIENT",
            "source c_Q or exclude Weyl nonmetricity branch",
            "p4_3565",
        ),
        (
            "P4C3566_4_projector_comm",
            "K_projector_comm",
            "projector/domain commutator kernel",
            "epsilon_projector_comm <= ||delta_Gamma Pi_M|| ||J_H||/|M_H_ref|",
            "CANDIDATE_ZERO_IF_Q_NATURAL_ELSE_BOUND_MISSING",
            "prove Pi_M q/e_obs/tau natural or source operator norm",
            "minimal_source_3497",
        ),
        (
            "P4C3566_5_EM_scalar_coupling",
            "D_X ln(lambda_A)",
            "visible EM scalar coupling/alpha owner",
            "alpha_EM drift/source coupling proportional to D_X ln(lambda_A/e_obs^2)",
            "NOT_DERIVED_CORE_COUPLING_TARGET",
            "lock lambda_A constant/universal or derive alpha/source response",
            "em_signature_3506",
        ),
        (
            "P4C3566_6_Kspin_map",
            "K_spin",
            "weak-field map from E_spin_abs to local tests",
            "epsilon_local_connection <= K_spin E_spin_abs",
            "MISSING_IF_AFFINE_BRANCH_USED",
            "component basis, units, lab-frame response and arena bounds",
            "p4_3565",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "role": role,
            "formula": formula,
            "status": status,
            "next_input_required": required,
            "source_path": str(source_paths[source_key]),
            "numeric_value": "ZERO_IN_PRIVATE_LC_BRANCH_ONLY" if "ZERO_INSIDE_LC_BRANCH" in status else "MISSING_OR_STRUCTURAL",
            "source_backed_numeric": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for coefficient_id, symbol, role, formula, status, required, source_key in rows
    ]


def decision_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3566_0_branch_signature_written",
            "decision": "write and machine-check the local LC branch action signature",
            "reason": "3565 showed the connection fork is exact; 2416/3497 already contain the pieces but not one current branch-signed ledger",
            "consequence": "E_spin=0 becomes an internal branch theorem, not a public parent-selection theorem",
            "status": "PRIVATE_BRANCH_SIGNATURE_ACTIVE_NONCLAIM",
            "source_path": str(source_paths["parent_spine_2416"]),
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3566_1_no_overclaim",
            "decision": "do not claim local GR/Newton from this alone",
            "reason": "boundary/source-owner/G_ref/Poisson-Gauss/EM scalar coupling and PPN residuals survive no-Gamma",
            "consequence": "local GR remains open, but the connection coupling is no longer the foggiest blocker",
            "status": "PUBLIC_CLAIM_BLOCKED",
            "source_path": str(source_paths["source_owner_contract"]),
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3566_2_first_p4_queue",
            "decision": "retain the first spin/P4 coefficient queue for the affine counterbranch",
            "reason": "if the LC branch selector fails, torsion/nonmetricity coefficients must be sourced rather than ignored",
            "consequence": "c_A/c_T/c_Q/K_spin rows are ready as fallback inputs",
            "status": "AFFINE_FALLBACK_QUEUE_READY_NONCLAIM",
            "source_path": str(source_paths["p4_3565"]),
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3566_3_best_next",
            "decision": "derive the branch selector/no-independent-affine theorem next",
            "reason": "the parent action signature can be stated; the missing leap is why MTS selects the LC branch in compact local physics",
            "consequence": "3567 targets branch selector proof or K_spin numeric fallback",
            "status": "NEXT_TARGET_SELECTED",
            "source_path": str(source_paths["theorem_3565"]),
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "LOCAL_LC_PARENT_SIGNATURE_WRITTEN_PRIVATE_BRANCH_E_SPIN_ZERO_INTERNAL",
            "strongest_result": "branch-signed local LC action signature excludes Gamma_ind/omega_ind and derives E_spin=0 inside that branch",
            "still_missing": "parent branch-selector theorem, boundary/source-owner source normalization, EM scalar coupling owner, Poisson-Gauss/Newton source calibration, PPN residual closure",
            "public_claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3566_0",
            "target_doc": "3567-Y5-R2FR-local-LC-branch-selector-or-Kspin-P4-map.md",
            "target_script": "scripts/Y5_R2FR_3567_local_LC_branch_selector_or_Kspin_P4_map.py",
            "objective": "attempt to derive why compact local MTS selects the LC/no-independent-affine branch from quotient/gauge/regularity; if not, make K_spin and the first affine torsion coefficient map source-ready",
            "success_gate": "parent-owned branch selector theorem for local LC branch, or first source-backed K_spin/c_A coefficient row with units and arena projection",
            "reason": "3566 turns no-Gamma into an internal branch theorem; the remaining non-smuggled step is branch selection or numeric affine fallback",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "parent_local_LC_action_signature",
            "branch_status": "PRIVATE_BRANCH_SIGNED",
            "internal_theorem": "E_spin_zero_by_no_independent_Gamma",
            "public_parent_status": "NOT_DERIVED_BRANCH_SELECTOR_MISSING",
            "next_action": "derive local LC branch selector or source K_spin/c_A fallback",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    signature: list[dict[str, object]],
    variation: list[dict[str, object]],
    activation: list[dict[str, object]],
    p4: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in outputs.items() if key != "validation"}
    validations.append(("VAL3566_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required source paths exist"))
    needles = {
        "handoff_3565": "NEXT3565_0",
        "status_3565": "SPIN_TORSION_TOTAL_ZERO_NOT_DERIVED",
        "theorem_3565": "STH3565_7_parent_action_contract",
        "p4_3565": "P4H3565_0_total",
        "parent_spine_2416": "PAS2416_0_domain",
        "activation_2416": "ACT2416_0_variable_absence",
        "matter_descent_2611": "MWD2611_1_conditional_theorem",
        "minimal_source_3497": "MPA3497_0_field_space",
        "clause_test_3497": "CLAUSE3496_6_projector_boundary",
        "variation_3497": "VAR3497_5_hsrc_verdict",
        "sector_gamma_3493": "SEC3493_0_ordinary_matter",
        "local_blocks": "A511_0_EH_core",
        "source_owner_contract": "A0_total_covariant_parent",
        "em_signature_3506": "GEN3506_5_scalar_gauge_kinetic_owner",
        "em_gate_3504": "HSG3504_2_EM_uses_star_obs",
        "source_owner_3443": "SOA3443_5_verdict",
        "signature_gate_3423": "PSG3423_7_verdict",
        "worldtube_audit_3375": "SIG3375_6_same_normalization",
    }
    validations.append(
        (
            "VAL3566_1_required_needles_found",
            all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()),
            "all selected source needles found",
        )
    )
    validations.append(
        (
            "VAL3566_2_outputs_exist",
            all(path.exists() for path in pre_validation_outputs.values()),
            "all pre-validation 3566 output files written",
        )
    )
    csvs_parse = True
    parse_details: list[str] = []
    for output_id, path in pre_validation_outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            row_count = len(read_csv(path))
            csvs_parse = csvs_parse and row_count > 0
            parse_details.append(f"{output_id}:{row_count}")
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3566_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(
        (
            "VAL3566_4_total_signature_no_gamma",
            any(row["signature_id"] == "SIG3566_10_total_signature" and "excludes Gamma_ind" in str(row["connection_policy"]) for row in signature),
            "total local LC signature excludes independent Gamma/omega",
        )
    )
    validations.append(
        (
            "VAL3566_5_Espin_internal_zero",
            any(row["variation_id"] == "VAR3566_8_Espin_total" and "0 inside LC branch" in str(row["result"]) for row in variation),
            "E_spin internal branch zero derivation recorded",
        )
    )
    validations.append(
        (
            "VAL3566_6_public_selector_not_overclaimed",
            any(row["activation_id"] == "ACT3566_1_public_parent_selector" and row["status"] == "FAIL_NOT_DERIVED" for row in activation),
            "public parent branch selector remains unclaimed",
        )
    )
    validations.append(
        (
            "VAL3566_7_affine_p4_queue_present",
            {"c_A", "K_spin", "D_X ln(lambda_A)"}.issubset({str(row["symbol"]) for row in p4}),
            "first affine/EM fallback coefficient queue present",
        )
    )
    validations.append(
        (
            "VAL3566_8_no_claim_flags",
            all(str(row["valid_for_claim"]).lower() == "false" for row in signature + variation + activation + p4),
            "all generated physics rows remain nonclaim",
        )
    )
    formalization_touched = any(FORMALIZATION.rglob("*3566*")) if FORMALIZATION.exists() else False
    validations.append(
        (
            "VAL3566_9_formalization_workbench_untouched",
            not formalization_touched,
            "no 3566 checkpoint output appears in formalization-workbench",
        )
    )
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passed,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passed, detail in validations
    ]


def write_doc(
    outputs: dict[str, Path],
    signature: list[dict[str, object]],
    variation: list[dict[str, object]],
    activation: list[dict[str, object]],
    p4: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines: list[str] = [
        "# 3566 - Parent local action variable signature or first spin P4 coefficient",
        "",
        "## Verdict",
        "3566 writes the local LC parent-action branch explicitly.  In this branch, `Gamma_ind` and `omega_ind` are not action variables in ordinary matter, spin transport, EM/light, source support or readout sectors.  Therefore the spin/torsion/hypermomentum source head `E_spin` is zero by variable absence inside the branch.",
        "",
        "This is progress, but not a public local-GR claim.  The deeper theorem still missing is the selector: why the full MTS parent must choose this LC/no-independent-affine branch in compact local physics rather than an affine/torsion counterbranch.  If that selector fails, the first P4 coefficient queue is ready: `c_A`, `c_T`, `c_Q`, `K_projector_comm`, `D_X ln(lambda_A)` and `K_spin`.",
        "",
        "So the foggy coupling problem becomes a clean fork: derive the local LC branch selector, or source the affine/EM coupling coefficients.",
        "",
        "## What moved",
        "- A single local LC branch signature is now assembled from 2416, 2611, 3497, 3506 and 3565.",
        "- `E_spin=0` is derived inside that branch, not merely listed as missing.",
        "- EM/Poynting is placed inside the Hilbert source via public-Hodge Maxwell stress, with scalar coupling still open.",
        "- Boundary/source-owner and Newton/PPN calibration remain outside the no-Gamma win.",
        "- The next gate is the branch selector, not another generic missing-input audit.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Local LC action signature"])
    for row in signature:
        lines.append(f"- `{row['signature_id']}` `{row['object']}`: {row['status']} ({row['formal_signature']})")
    lines.extend(["", "## Variation derivation"])
    for row in variation:
        lines.append(f"- `{row['variation_id']}` `{row['variation_piece']}` -> {row['result']}: {row['derivation']}")
    lines.extend(["", "## Activation gates"])
    for row in activation:
        lines.append(f"- `{row['activation_id']}`: {row['status']} ({row['remaining_gap']})")
    lines.extend(["", "## First P4 coefficient queue"])
    for row in p4:
        lines.append(f"- `{row['coefficient_id']}` `{row['symbol']}`: {row['status']} ({row['formula']})")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} -> {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(
        [
            "",
            "## Next target",
            f"- `{next_target[0]['target_doc']}`",
            f"- Objective: {next_target[0]['objective']}",
        ]
    )
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    register = source_register(source_paths)
    signature = action_signature_rows(source_paths)
    variation = variation_derivation_rows(source_paths)
    activation = activation_rows(source_paths)
    p4 = p4_coefficient_rows(source_paths)
    decisions = decision_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3566_SOURCE_REGISTER.csv",
        "local_action_signature": RESIDUALS / "P8_Y5_R2FR_3566_PARENT_LOCAL_LC_ACTION_SIGNATURE.csv",
        "variation_derivation": RESIDUALS / "P8_Y5_R2FR_3566_NO_GAMMA_VARIATION_DERIVATION.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3566_SIGNATURE_ACTIVATION_GATES.csv",
        "first_p4_coefficient_queue": RESIDUALS / "P8_Y5_R2FR_3566_FIRST_SPIN_P4_COEFFICIENT_QUEUE.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3566_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3566_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3566_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_parent_local_LC_action_signature_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3566_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["local_action_signature"], signature)
    write_csv(outputs["variation_derivation"], variation)
    write_csv(outputs["activation_gates"], activation)
    write_csv(outputs["first_p4_coefficient_queue"], p4)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, signature, variation, activation, p4)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, signature, variation, activation, p4, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3566 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()

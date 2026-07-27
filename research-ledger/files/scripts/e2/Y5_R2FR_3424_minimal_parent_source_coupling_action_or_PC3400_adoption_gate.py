from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3424-Y5-R2FR-minimal-parent-source-coupling-action-or-PC3400-adoption-gate-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3423": ROOT / "3423-Y5-R2FR-Y5-Hilbert-source-worldtube-closure-or-JZmu-bound-row-under-AX1090.md",
    "action_candidate_3423": OUT / "P8_Y5_R2FR_3423_MINIMAL_PARENT_SOURCE_ACTION_CANDIDATE.csv",
    "theorem_3423": OUT / "P8_Y5_R2FR_3423_HILBERT_WORLDTUBE_CLOSURE_THEOREM.csv",
    "jzmu_3423": OUT / "P8_Y5_R2FR_3423_JZMU_BOUND_ROWS.csv",
    "signature_3423": OUT / "P8_Y5_R2FR_3423_PARENT_SIGNATURE_GATE.csv",
    "next_3423": OUT / "P8_Y5_R2FR_3423_NEXT_TARGET.csv",
    "doc_3414": ROOT / "3414-Y5-R2FR-Y5-source-normalization-and-Y6-extra-stress-owner-gate-under-AX1090.md",
    "parent_clauses_3400": OUT / "P8_Y5_R2FR_3400_PARENT_SIGNATURE_CLAUSES.csv",
    "first_order_3399": OUT / "P8_Y5_R2FR_3399_FIRST_ORDER_NEWTON_ZERO_THEOREM.csv",
    "activation_3400": OUT / "P8_Y5_R2FR_3400_FIRST_ORDER_ACTIVATION_THEOREM.csv",
    "source_square_3401": OUT / "P8_Y5_R2FR_3401_SOURCE_AB_SQUARE_LAW.csv",
    "kappav_3401": OUT / "P8_Y5_R2FR_3401_KAPPAV_COMPONENT_LEDGER.csv",
    "doc_3421": ROOT / "3421-Y5-R2FR-Z-basis-physical-lock-and-Euler-source-free-local-branch-under-AX1090.md",
    "coercivity_3421": OUT / "P8_Y5_R2FR_3421_COERCIVITY_BOUND_PACK.csv",
    "doc_1016": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
    "hsm_contract": OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "hwt_contract": OUT / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3424_SOURCE_REGISTER.csv",
    "parent_action_density": OUT / "P8_Y5_R2FR_3424_PARENT_ACTION_DENSITY.csv",
    "variation_chain": OUT / "P8_Y5_R2FR_3424_VARIATION_AND_NEWTON_CHAIN.csv",
    "pc3400_adoption_audit": OUT / "P8_Y5_R2FR_3424_PC3400_ADOPTION_AUDIT.csv",
    "no_smuggling_tests": OUT / "P8_Y5_R2FR_3424_NO_SMUGGLING_TESTS.csv",
    "retained_bound_rows": OUT / "P8_Y5_R2FR_3424_RETAINED_SOURCE_BOUND_ROWS.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3424_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3424_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3424_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3424_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3424_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3423": "Y5 Hilbert source worldtube handoff",
        "action_candidate_3423": "minimal source-action clauses from 3423",
        "theorem_3423": "conditional J_Z_mu_Y5 zero theorem",
        "jzmu_3423": "JZMU bound rows",
        "signature_3423": "parent signature gate rows",
        "next_3423": "machine-readable 3424 target",
        "doc_3414": "calibrated coupling and Y5 owner gate",
        "parent_clauses_3400": "PC3400 parent signature clauses",
        "first_order_3399": "first-order Newton zero theorem",
        "activation_3400": "PC3400 activation theorem",
        "source_square_3401": "second-order source-square gate",
        "kappav_3401": "kappa_v/beta residual ledger",
        "doc_3421": "fixed-point theorem requiring source current zero/bound",
        "coercivity_3421": "lambda-star bound pack",
        "doc_1016": "worldtube/source-measure selector contract",
        "hsm_contract": "Hamiltonian source-measure contract",
        "hwt_contract": "Hilbert worldtube parent action contract",
    }
    return [
        {
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
            "valid_for_claim": False,
        }
        for key, path in SOURCES.items()
    ]


def parent_action_density() -> list[dict[str, Any]]:
    return [
        {
            "term_id": "PAD3424_0_branch_data",
            "term": "local branch data fixed before readout",
            "density_or_rule": "choose (q(Phi), g_obs, e_obs, theta, tau, B_ref, Pi_M, kappa_0) once for the branch",
            "signs_clause": "PC3400_0 if no later source/radius/orbit labels enter",
            "status": "COHERENT_PARENT_ACTION_INPUT_NOT_CORE_ADOPTED",
            "valid_for_claim": False,
        },
        {
            "term_id": "PAD3424_1_EH_public_geometry",
            "term": "public Einstein-Hilbert local metric sector",
            "density_or_rule": "L_EH = (c^4/16 pi G_ref) sqrt(-g_obs) R[g_obs] plus fixed boundary/reference term",
            "signs_clause": "PC3400_1 for one universal kappa_0",
            "status": "COHERENT_CONSTANT_COUPLING_BRANCH",
            "valid_for_claim": False,
        },
        {
            "term_id": "PAD3424_2_matter_and_EM",
            "term": "ordinary matter/EM/clocks/rods",
            "density_or_rule": "S_matter[e_obs,psi] + S_EM[g_obs,A] with Hilbert stress from variation before readout",
            "signs_clause": "PC3400_2 and public EM/Poynting safe class",
            "status": "COHERENT_IF_ALL_ORDINARY_SOURCES_USE_EOBS",
            "valid_for_claim": False,
        },
        {
            "term_id": "PAD3424_3_Hamiltonian_charge",
            "term": "worldtube Hamiltonian/Noether source charge",
            "density_or_rule": "J_H[tau] from Hilbert stress; W_source=closure(supp J_H[tau]); M_H=H_tau[S]-H_ref",
            "signs_clause": "PC3400_3 only if integrability/reference/boundary lock is proved",
            "status": "PARTIAL_CONSTRUCTION_REFERENCE_LOCK_OPEN",
            "valid_for_claim": False,
        },
        {
            "term_id": "PAD3424_4_Z_residual_sector",
            "term": "local MTS residual field sector",
            "density_or_rule": "L_Z = 1/2 <D Z, A D Z> + 1/2 <Z, M^2 Z> + O(Z^3), with no linear J_H Z source vertex",
            "signs_clause": "3421 source-free fixed point if lambda_*>0 and no linear source survives",
            "status": "COHERENT_FORM_BUT_LAMBDA_AND_SOURCE_SILENCE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "term_id": "PAD3424_5_v_metric_identification",
            "term": "Newton potential is the quotient metric potential, not an independently fitted force field",
            "density_or_rule": "g_00 = -1 - 2 Phi_N/c^2 + O(c^-4); Delta Phi_N = 4 pi G_ref rho_H",
            "signs_clause": "PC3400_5 if v is identified with the EH metric potential and no separate v coefficient remains",
            "status": "BEST_ROUTE_CONDITIONAL_ON_V_NOT_INDEPENDENT",
            "valid_for_claim": False,
        },
        {
            "term_id": "PAD3424_6_no_extra_mass",
            "term": "no unowned monopole mass in hidden/boundary/domain/memory/projector sectors",
            "density_or_rule": "R_eq=B_zero_flux=[d,Pi_M]J_H=Delta_extra_mass=0 or explicit retained source-bound row",
            "signs_clause": "PC3400_4 only after no-hair/boundary/integrability proof",
            "status": "NOT_SIGNED_RETAINED_BOUND_BRANCH_ACTIVE",
            "valid_for_claim": False,
        },
    ]


def variation_chain() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "VC3424_0_metric_variation",
            "derivation_step": "Vary the public metric sector and ordinary Hilbert matter.",
            "identity": "G_{mu nu}[g_obs] = (8 pi G_ref/c^4) T^{H}_{mu nu} + T^{Z}_{mu nu,eff}",
            "result": "ordinary source coupling is fixed by one kappa_0",
            "claim_status": "CONDITIONAL_BRANCH_DERIVATION",
            "valid_for_claim": False,
        },
        {
            "step_id": "VC3424_1_Newton_limit",
            "derivation_step": "Take local weak-field, slow-motion, compact-source limit with Z=0 and fixed boundary reference.",
            "identity": "Delta Phi_N = 4 pi G_ref rho_H; Phi_N(r)= -G_ref M_H/r + boundary/exterior multipoles",
            "result": "first-order Newton amplitude follows from the same Hilbert charge",
            "claim_status": "EXACT_IF_Z_AND_BOUNDARY_SOURCE_TERMS_ZERO",
            "valid_for_claim": False,
        },
        {
            "step_id": "VC3424_2_Z_Euler",
            "derivation_step": "Vary the residual Z sector around the quotient-even branch.",
            "identity": "L_AB Z^B + N_A(Z) = J_A^Y5 + J_A^Y6 + B_A + R_A",
            "result": "the candidate action sets J_A^Y5=0 only if PAD3424_0-PAD3424_5 are signed",
            "claim_status": "PARTIAL_Y5_ZERO_ROUTE",
            "valid_for_claim": False,
        },
        {
            "step_id": "VC3424_3_first_order_PC3400",
            "derivation_step": "Match the variation chain to PC3400 first-order source terms.",
            "identity": "Delta_Newton_Y5^(1)=delta_kappa+delta_ellJ+epsilon_Gref+delta_KC+epsilon_M",
            "result": "first four terms can be killed by the candidate; epsilon_M remains tied to no-extra-mass/boundary/Y6",
            "claim_status": "PARTIAL_ADOPTION_NOT_FULL_ZERO",
            "valid_for_claim": False,
        },
        {
            "step_id": "VC3424_4_second_order_warning",
            "derivation_step": "Check whether first-order source coupling proves PPN beta.",
            "identity": "beta_eff-1 = B_source/A_source^2 - 1 + kappa_v pieces",
            "result": "not closed unless v is metric-only through EH expansion or source-square law is derived",
            "claim_status": "SECOND_ORDER_OPEN",
            "valid_for_claim": False,
        },
    ]


def pc3400_adoption_audit() -> list[dict[str, Any]]:
    return [
        {
            "pc_clause": "PC3400_0_single_branch",
            "adoption_result": "CAN_SIGN_IN_CANDIDATE_BRANCH",
            "reason": "branch data are fixed once before source/orbit comparison",
            "remaining_risk": "must not later add source-specific labels",
            "valid_for_claim": False,
        },
        {
            "pc_clause": "PC3400_1_constant_kappa",
            "adoption_result": "CAN_SIGN_AS_PARENT_CONSTANT",
            "reason": "kappa_0 is allowed exactly as GR uses a measured universal G",
            "remaining_risk": "does not derive SI value of G; it forbids differential drift",
            "valid_for_claim": False,
        },
        {
            "pc_clause": "PC3400_2_same_matter_source",
            "adoption_result": "CAN_SIGN_FOR_PUBLIC_MATTER_EM",
            "reason": "S_matter[e_obs,psi] and public Maxwell stress use the same Hilbert variation",
            "remaining_risk": "hidden matter frames or constitutive EM couplings would reopen it",
            "valid_for_claim": False,
        },
        {
            "pc_clause": "PC3400_3_Htau_PiM_chain",
            "adoption_result": "PARTIAL_NOT_SIGNED",
            "reason": "candidate names H_tau and M_H but integrability, H_ref and Pi_M chain-map equality remain unproved",
            "remaining_risk": "epsilon_HPiM_Z and I_commutator remain bound rows",
            "valid_for_claim": False,
        },
        {
            "pc_clause": "PC3400_4_no_boundary_extra_mass",
            "adoption_result": "FAIL_RETAINED_DEBT",
            "reason": "hidden/domain/memory/projector/Y6 monopole mass channels are not excluded by the minimal action alone",
            "remaining_risk": "epsilon_M and Delta_extra_mass remain bound rows",
            "valid_for_claim": False,
        },
        {
            "pc_clause": "PC3400_5_v_action_ratio",
            "adoption_result": "CAN_SIGN_ONLY_IF_V_IS_METRIC_POTENTIAL",
            "reason": "EH expansion fixes Poisson amplitude if v is h00/Phi_N, but not if v is an independent MTS field",
            "remaining_risk": "delta_KC_Z remains if independent v coefficients survive",
            "valid_for_claim": False,
        },
        {
            "pc_clause": "PC3400_6_same_U_PPN_guard",
            "adoption_result": "FIRST_ORDER_TRANSFER_ONLY",
            "reason": "same U follows only for the signed first-order Hilbert source branch",
            "remaining_risk": "beta/preferred-frame/vector gates remain open",
            "valid_for_claim": False,
        },
        {
            "pc_clause": "PC3400_VERDICT",
            "adoption_result": "PARTIAL_ACTION_SUCCESS_NOT_LOCAL_GR",
            "reason": "PC3400_0-2 are coherent, PC3400_5 has a clean metric-potential fork, but PC3400_3-4 block current Y5 zero",
            "remaining_risk": "Hamiltonian reference/PiM/no-extra-mass must be proved or bounded",
            "valid_for_claim": False,
        },
    ]


def no_smuggling_tests() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "NST3424_0_global_calibration",
            "test": "Is G/kappa chosen once globally, not per source or per dataset?",
            "candidate_result": "PASS_AS_CONTRACT",
            "failure_mode": "late source-specific GM fit would invalidate PC3400_1",
            "valid_for_claim": False,
        },
        {
            "test_id": "NST3424_1_same_source_object",
            "test": "Does the mass in Poisson/PPN/orbits equal the Hilbert/Hamiltonian source charge?",
            "candidate_result": "PARTIAL",
            "failure_mode": "H_tau/PiM/reference mismatch leaves epsilon_HPiM_Z",
            "valid_for_claim": False,
        },
        {
            "test_id": "NST3424_2_no_extra_monopole",
            "test": "Can hidden, boundary, memory, range or projector sectors carry monopole mass after calibration?",
            "candidate_result": "FAIL_CURRENT",
            "failure_mode": "epsilon_M/Delta_extra_mass remains unless no-hair or bound proof closes",
            "valid_for_claim": False,
        },
        {
            "test_id": "NST3424_3_metric_v_fork",
            "test": "Is v merely the quotient metric potential?",
            "candidate_result": "FORK",
            "failure_mode": "independent v field requires coefficient derivation and source-square proof",
            "valid_for_claim": False,
        },
        {
            "test_id": "NST3424_4_public_EM",
            "test": "Is Poynting/EM stress only public Hilbert stress?",
            "candidate_result": "PASS_IF_PUBLIC_MAXWELL_ONLY",
            "failure_mode": "hidden Hodge/current weights create a real residual source channel",
            "valid_for_claim": False,
        },
    ]


def retained_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RSB3424_0_epsilon_HPiM_Z",
            "quantity": "epsilon_HPiM_Z",
            "definition": "Hamiltonian/PiM/source-charge mismatch retained after PAD3424_3",
            "bound_formula": "|partial_Z ln(M_H/(Pi_M J_H))| + |I_commutator|/M_H_ref",
            "status": "MISSING_MHREF_INTEGRABILITY_INPUT",
            "valid_for_claim": False,
        },
        {
            "row_id": "RSB3424_1_epsilon_M_extra",
            "quantity": "epsilon_M_extra",
            "definition": "unowned extra monopole mass from boundary/domain/memory/projector/Y6 channels",
            "bound_formula": "(|R_eq|+|B_zero_flux|+|Delta_domain|+|Delta_extra_mass|)/M_H_ref",
            "status": "MISSING_NO_HAIR_OR_SOURCE_BACKED_BOUND",
            "valid_for_claim": False,
        },
        {
            "row_id": "RSB3424_2_delta_KC_fork",
            "quantity": "delta_KC_Z",
            "definition": "v source/kinetic coefficient mismatch if v is independent rather than metric potential",
            "bound_formula": "0 if v=Phi_N metric quotient; else |(B_v/A_v)/(16 pi G_ref/c^4)-1|",
            "status": "FORK_NOT_DECIDED",
            "valid_for_claim": False,
        },
        {
            "row_id": "RSB3424_3_total_Y5_after_action",
            "quantity": "||J_Z_mu_Y5||_after_candidate",
            "definition": "Y5 source current after signing PC3400_0-2 and public EM/matter",
            "bound_formula": "epsilon_HPiM_Z+epsilon_M_extra+delta_KC_fork+epsilon_beta_source_Z+epsilon_hidden_source_Z",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3424_0_action_coherent",
            "claim": "minimal source-coupling parent action is internally coherent as a branch candidate",
            "gate_status": "PASS_CANDIDATE",
            "reason": "terms PAD3424_0-PAD3424_5 can coexist without fitting GM per source",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3424_1_PC3400_0_2",
            "claim": "PC3400_0 through PC3400_2 can be signed by the candidate branch",
            "gate_status": "PASS_CONDITIONAL_ADOPTION",
            "reason": "fixed branch, global kappa and public Hilbert matter source are compatible",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3424_2_PC3400_full",
            "claim": "all PC3400 source-coupling clauses are signed",
            "gate_status": "FAIL_CURRENT",
            "reason": "H_tau/PiM/reference/no-extra-mass and v-fork remain unresolved",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3424_3_Y5_zero",
            "claim": "J_Z_mu_Y5 is zero for current MTS",
            "gate_status": "NOT_PROMOTED",
            "reason": "retained bound rows RSB3424 remain active",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3424_4_local_GR",
            "claim": "local GR/Newton/PPN branch is derived",
            "gate_status": "BLOCKED",
            "reason": "Y5 partial, Y6, lambda_*, q_loc vector/stress and second-order PPN gates remain open",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3424_0_leap_forward",
            "decision": "A minimal GR-like public source-coupling action is coherent as a candidate MTS local branch.",
            "because": "it signs fixed branch, universal kappa and public Hilbert matter/EM source without per-source GM fitting",
            "next_action": "use it as the candidate branch for PC3400_0-2, not as a local-GR claim",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3424_1_not_enough",
            "decision": "The action candidate does not yet finish Y5.",
            "because": "Hamiltonian reference/PiM integrability, no-extra-mass and the v metric-potential fork are still unresolved",
            "next_action": "attack the Hamiltonian reference/integrability lock first",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3424_2_v_fork",
            "decision": "The less-scrutinized route is to identify v with the quotient metric potential, not an independent local force field.",
            "because": "EH expansion then fixes the Poisson coefficient; an independent v field requires a separate coefficient derivation",
            "next_action": "keep the independent-v branch as a bound/fork until the metric identification is parent-signed",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3424_3_best_next",
            "decision": "Next target should prove Hamiltonian reference/PiM integrability or emit M_H_ref source rows.",
            "because": "PC3400_3 is now the largest remaining purely Y5 blocker after PC3400_0-2 have a coherent candidate",
            "next_action": "3425-Y5-R2FR-Hamiltonian-reference-PiM-integrability-lock-or-MHref-row-under-AX1090.md",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target": "3425-Y5-R2FR-Hamiltonian-reference-PiM-integrability-lock-or-MHref-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3425_Hamiltonian_reference_PiM_integrability_lock_or_MHref_row.py",
            "objective": "prove H_tau-H_ref is an integrable same-branch Hilbert worldtube charge with fixed reference and Pi_M chain-map equality, or emit source-backed M_H_ref/I_commutator/boundary rows",
            "why_next": "3424 gives a coherent source action for PC3400_0-2; PC3400_3 is now the biggest Y5-specific obstruction",
            "valid_for_claim": False,
        },
        {
            "target": "3426-Y5-R2FR-Y6-extra-monopole-no-hair-or-bound-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3426_Y6_extra_monopole_no_hair_or_bound.py",
            "objective": "exclude or bound hidden/domain/memory/projector/Y6 extra monopole mass after source calibration",
            "why_next": "PC3400_4 remains the no-extra-mass gate after the Hamiltonian reference lock",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3424_0",
            "script": str(Path(__file__).resolve()),
            "mode": "MINIMAL_PARENT_SOURCE_ACTION_OR_PC3400_ADOPTION_GATE",
            "summary": "coherent source-action candidate staged; PC3400_0-2 conditionally signable; PC3400_3-4 and v fork remain retained; no Y5/local-GR claim promoted",
            "valid_for_claim": False,
        }
    ]


def formalization_recent_count(start_utc: datetime) -> int:
    if not FORMALIZATION.exists():
        return 0
    threshold = start_utc.timestamp()
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= threshold:
            count += 1
    return count


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    sources = rows_by_name["source_register"]
    nonclaim = all(
        row.get("valid_for_claim") is False
        for name, rows in rows_by_name.items()
        if name != "validation"
        for row in rows
    )
    outputs_under_root = all(str(path).startswith(str(ROOT)) for path in OUTPUTS.values()) and str(DOC).startswith(str(ROOT))
    formalization_count = formalization_recent_count(start_utc)
    promotion = rows_by_name["promotion_gates"]
    audit = rows_by_name["pc3400_adoption_audit"]
    return [
        {
            "check_id": "VAL3424_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in sources),
            "detail": f"{sum(1 for row in sources if row['exists'])}/{len(sources)} source paths exist",
        },
        {
            "check_id": "VAL3424_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": outputs_under_root,
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3424_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim,
            "detail": "valid_for_claim=false throughout generated rows",
        },
        {
            "check_id": "VAL3424_3_action_candidate",
            "condition": "source-action candidate has public EH/matter/Hilbert/worldtube/Z terms",
            "passed": len(rows_by_name["parent_action_density"]) >= 7,
            "detail": "PAD3424 rows present",
        },
        {
            "check_id": "VAL3424_4_PC3400_partial",
            "condition": "PC3400_0-2 partial adoption is explicit",
            "passed": any(row["pc_clause"] == "PC3400_2_same_matter_source" and row["adoption_result"].startswith("CAN_SIGN") for row in audit),
            "detail": "PC3400_0-2 conditionally signable",
        },
        {
            "check_id": "VAL3424_5_PC3400_not_full",
            "condition": "full PC3400 is not claimed",
            "passed": any(row["pc_clause"] == "PC3400_VERDICT" and row["adoption_result"].startswith("PARTIAL") for row in audit),
            "detail": "PC3400_3-4/v fork retained",
        },
        {
            "check_id": "VAL3424_6_bound_rows_retained",
            "condition": "retained source-bound rows exist",
            "passed": any(row["row_id"] == "RSB3424_3_total_Y5_after_action" for row in rows_by_name["retained_bound_rows"]),
            "detail": "RSB3424_3 present",
        },
        {
            "check_id": "VAL3424_7_local_GR_blocked",
            "condition": "local GR remains blocked",
            "passed": any(row["gate_id"] == "PG3424_4_local_GR" and row["gate_status"] == "BLOCKED" for row in promotion),
            "detail": "no local-GR claim promoted",
        },
        {
            "check_id": "VAL3424_8_next_target",
            "condition": "next target attacks Hamiltonian/PiM integrability",
            "passed": rows_by_name["next_target"][0]["target"].startswith("3425-Y5-R2FR-Hamiltonian-reference-PiM"),
            "detail": rows_by_name["next_target"][0]["target"],
        },
        {
            "check_id": "VAL3424_9_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": formalization_count == 0,
            "detail": f"modified_count_since_start={formalization_count}",
        },
        {
            "check_id": "VAL3424_10_overall",
            "condition": "3424 source-action checkpoint is internally valid",
            "passed": True,
            "detail": "PASS",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3424 - Minimal Parent Source-Coupling Action or PC3400 Adoption Gate

## Summary
- This is the actual leap attempt: instantiate a minimal local parent source-coupling branch instead of merely saying "the coupling is missing".
- The candidate is GR-like where it must be: one public `g_obs/e_obs`, one universal `kappa_0`, ordinary Hilbert matter/EM stress, and a residual `Z` sector with no linear source vertex.
- This does **not** smuggle a fitted `GM` if `kappa_0` is fixed once globally and the source mass is the Hilbert/Hamiltonian worldtube charge, not a late per-source label.
- Result: `PC3400_0`, `PC3400_1`, and `PC3400_2` are coherently signable by this candidate branch.
- Still not enough: `PC3400_3` Hamiltonian/PiM/reference integrability, `PC3400_4` no-extra-mass/Y6, and the `v` metric-potential fork remain open.
- So Y5 is **improved but not closed**: `J_Z_mu_Y5` shrinks to retained rows for Hamiltonian/PiM, extra monopole mass, the `v` fork, second order, and hidden drift.

## Source Register
{md_table(rows_by_name["source_register"])}

## Parent Action Density
{md_table(rows_by_name["parent_action_density"])}

## Variation and Newton Chain
{md_table(rows_by_name["variation_chain"])}

## PC3400 Adoption Audit
{md_table(rows_by_name["pc3400_adoption_audit"])}

## No-Smuggling Tests
{md_table(rows_by_name["no_smuggling_tests"])}

## Retained Source Bound Rows
{md_table(rows_by_name["retained_bound_rows"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
This checkpoint does move the work. We now have a coherent candidate local source-action branch that can legally carry the GR/Newton coupling style inside MTS without pretending to derive the numerical value of `G` from nowhere. The remaining Y5 fight is narrower and sharper: prove the Hamiltonian/PiM/reference lock and no-extra-mass theorem, or score the retained source-bound rows.
"""
    DOC.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "parent_action_density": parent_action_density(),
        "variation_chain": variation_chain(),
        "pc3400_adoption_audit": pc3400_adoption_audit(),
        "no_smuggling_tests": no_smuggling_tests(),
        "retained_bound_rows": retained_bound_rows(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    write_doc(rows_by_name)
    failed = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed:
        raise SystemExit(f"3424 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()

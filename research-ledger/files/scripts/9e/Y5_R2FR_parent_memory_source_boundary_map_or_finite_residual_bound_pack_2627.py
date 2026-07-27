from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2627-Y5-R2FR-parent-memory-source-boundary-map-or-finite-residual-bound-pack.md"

PREFIX = "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "lineage": RESIDUALS / f"{PREFIX}_LINEAGE_LEDGER.csv",
    "variation_map": RESIDUALS / f"{PREFIX}_JX_VARIATION_MAP.csv",
    "component_gate": RESIDUALS / f"{PREFIX}_JX_COMPONENT_ZERO_GATE.csv",
    "boundary_gate": RESIDUALS / f"{PREFIX}_BOUNDARY_ZERO_GATE.csv",
    "residual_pack": RESIDUALS / f"{PREFIX}_FINITE_RESIDUAL_BOUND_PACK.csv",
    "constraint_bridge": RESIDUALS / f"{PREFIX}_CONSTRAINT_AUXILIARY_BRIDGE.csv",
    "countermodels": RESIDUALS / f"{PREFIX}_COUNTERMODEL_LEDGER.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2627_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2627_00_2626_handoff",
        "role": "2626 selects parent memory source-boundary map",
        "path": ROOT / "2626-Y5-R2FR-parent-memory-operator-owner-hunt-or-memory-residual-template.md",
        "needles": ["DEC2626_3_best_next", "PARENT_MEMORY_SOURCE_BOUNDARY_MAP_IS_NEXT", "MOA2626_9_verdict"],
    },
    {
        "source_id": "SRC2627_01_2626_validation",
        "role": "2626 validation pass",
        "path": RESIDUALS / "P8_Y5_BRR545_2626_VALIDATION.csv",
        "needles": ["VAL2626_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC2627_02_two_slot_contract_972",
        "role": "two-slot action and relative Bianchi identity",
        "path": ROOT / "972-Y5-R10-parent-two-slot-memory-action-and-Bianchi-identity-or-residual-source-fill.md",
        "needles": ["TSC972_7_verdict", "RSF972_1_JX_source_norm", "BIANCHI_CONTRACT_READY_PARENT_UNSIGNED"],
    },
    {
        "source_id": "SRC2627_03_jx_decomposition_973",
        "role": "source-free kinetic and J_X decomposition gate",
        "path": ROOT / "973-Y5-R10-source-free-SXkin-and-boundary-zero-proof-or-first-memory-residual-source-row.md",
        "needles": ["JXD973_6_verdict", "JX_ZERO_NOT_PROVED", "FRS973_0_boundary_alpha3_flux"],
    },
    {
        "source_id": "SRC2627_04_matter_descent_943",
        "role": "quotient observed-coframe matter blindness contract",
        "path": ROOT / "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
        "needles": ["DER943_1_matter_action_blindness", "CFC943_7_contract_verdict", "CGATE943_1_matter_coupling"],
    },
    {
        "source_id": "SRC2627_05_boundary_417",
        "role": "boundary exchange/no-hair blockers and local pressure anchors",
        "path": ROOT / "417-boundary-exchange-nohair-theorem-attempt.md",
        "needles": ["boundary_exchange_nohair_derived", "Bianchi_gate_owned", "projected_local_flux_zero"],
    },
    {
        "source_id": "SRC2627_06_extra_silence_506",
        "role": "positive source-free operator plus zero boundary/source silence mechanism",
        "path": ROOT / "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
        "needles": ["T506_EH_plus_silent_reduction", "E506_memory_kernel_silence", "DEC506_0_partial_derivation"],
    },
    {
        "source_id": "SRC2627_07_acceptance_gates_507",
        "role": "theorem-zero and numeric-bound acceptance gates",
        "path": ROOT / "507-field-specific-silence-queue-kappa-domain-memory-motion.md",
        "needles": ["G507_0_theorem_zero", "G507_1_numeric_bound", "memory_kernel"],
    },
    {
        "source_id": "SRC2627_08_scalar_demoted_1856",
        "role": "physical scalar route rejected; constraint/auxiliary route selected",
        "path": ROOT / "1856-Y5-R2FR-derive-X-sector-from-MTS-primitives-or-reject-physical-scalar.md",
        "needles": ["REJECT_AS_FUNDAMENTAL_CURRENT_BRANCH", "DEC1856_1_best_route", "constraint/auxiliary/quotient-first"],
    },
    {
        "source_id": "SRC2627_09_parent_signature_2507",
        "role": "no current parent signature; object-language no-source-only slot selected",
        "path": ROOT / "2507-Y5-R2FR-parent-signature-synthesis-quotient-source-glue-or-GR-import-lock.md",
        "needles": ["NO_PARENT_SIGNATURE_SIGNED", "OBJECT_LANGUAGE_NO_SOURCE_ONLY_SLOT_NEXT", "CM2507_0_relative_source_weight"],
    },
    {
        "source_id": "SRC2627_10_projection_guard_856",
        "role": "memory projection repair and conservation guard",
        "path": ROOT / "856-Y5-R10-memory-projection-repair-or-independent-calibration-source-test.md",
        "needles": ["RPC856_3_conservation_guard", "branch_invariant_memory_projection_repair_contract", "D856_1"],
    },
]


def ensure_dirs() -> None:
    for path in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def b(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty csv rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        return bool(read_csv(path))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        text = read_text(source["path"])
        exists = source["path"].exists()
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "source_id": source["source_id"],
                "role": source["role"],
                "source_path": str(source["path"]),
                "exists": b(exists),
                "needles_present": b(needles_present),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": "False",
            }
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    return [
        {
            "lineage_id": "LIN2627_0_2626",
            "input": "2626",
            "imported_result": "parent memory owner not found; source-boundary map selected",
            "current_use": "turn the missing J_X and boundary data into explicit theorem gates",
            "claim_status": "nonclaim_handoff",
            "valid_for_claim": "False",
        },
        {
            "lineage_id": "LIN2627_1_972_973",
            "input": "972/973",
            "imported_result": "two-slot action and J_X component decomposition already written as relative contracts",
            "current_use": "lift those contracts into the active R2/f(R) post-checkpoint branch",
            "claim_status": "relative_contract_parent_unsigned",
            "valid_for_claim": "False",
        },
        {
            "lineage_id": "LIN2627_2_943",
            "input": "943",
            "imported_result": "matter blindness follows by quotient observed-coframe descent if parent-signed",
            "current_use": "identify the exact condition for J_X^matter=0",
            "claim_status": "conditional_chain_rule_not_parent_signed",
            "valid_for_claim": "False",
        },
        {
            "lineage_id": "LIN2627_3_417_506_507",
            "input": "417/506/507",
            "imported_result": "zero-source/zero-boundary positive-operator mechanism and acceptance gates",
            "current_use": "keep theorem-zero and numeric-bound standards sharp",
            "claim_status": "gate_ready_inputs_open",
            "valid_for_claim": "False",
        },
        {
            "lineage_id": "LIN2627_4_1856_2507",
            "input": "1856/2507",
            "imported_result": "physical scalar route demoted; parent signature/object-language gaps remain",
            "current_use": "avoid turning X into a fundamental fifth-force scalar unless a parent derivation appears",
            "claim_status": "constraint_auxiliary_route_preferred",
            "valid_for_claim": "False",
        },
    ]


def variation_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "map_id": "JVM2627_0_two_slot_action",
            "object": "two-slot memory action",
            "derived_form": "S = S_core[q,Psi,theta] + 1/2 int_D sqrt(gamma)(A^ij nabla_i X nabla_j X + m_X^2 X^2) + int_D sqrt(gamma) f(chi_D) C_obs[X,q(Phi),Psi,theta] + S_boundary",
            "current_status": "RELATIVE_CONTRACT_NOT_PARENT_SIGNED",
            "source_support": "972 writes this as an exact contract but parent ownership remains unsigned",
            "valid_for_claim": "False",
        },
        {
            "map_id": "JVM2627_1_bulk_variation",
            "object": "bulk X equation",
            "derived_form": "delta_X S gives L_X X = J_X with L_X=-nabla_i(A^ij nabla_j)+m_X^2 and J_X collecting affine, matter, observed-slot, chi-wall, boundary-history, and memory-tail terms",
            "current_status": "RELATIVE_VARIATION_DERIVED",
            "source_support": "967/970/972/973 agree on the operator/source form",
            "valid_for_claim": "False",
        },
        {
            "map_id": "JVM2627_2_boundary_variation",
            "object": "boundary X condition",
            "derived_form": "boundary variation contains int_partialD sqrt(h) delta X n_i A^ij nabla_j X + delta_X S_boundary, so zero theorem needs Dirichlet, zero-flux, exact/topological local-zero, or a sourced boundary_lift_norm",
            "current_status": "BOUNDARY_TERM_IDENTIFIED_NOT_PARENT_SELECTED",
            "source_support": "417 and 973 keep boundary primitive/local flux/no-hair gates open",
            "valid_for_claim": "False",
        },
        {
            "map_id": "JVM2627_3_positive_operator_implication",
            "object": "memory silence theorem",
            "derived_form": "If L_X is positive, J_X=0, and the boundary term is zero/nonnegative with zero modes removed, then int_D X L_X X=0 implies X=0 modulo allowed universal constants",
            "current_status": "RELATIVE_THEOREM_ONLY",
            "source_support": "506/967 give the non-cheat energy identity route",
            "valid_for_claim": "False",
        },
        {
            "map_id": "JVM2627_4_current_verdict",
            "object": "J_X source-boundary map",
            "derived_form": "The exact map is now specified, but total J_X=0 is not parent-proved because the zero-origin, matter descent, chi-wall, boundary, and history gates do not all close",
            "current_status": "JX_ZERO_NOT_PROVED",
            "source_support": "973 component gate plus 943/417/1856/2507 blockers",
            "valid_for_claim": "False",
        },
    ]


def component_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "JX2627_0_kinetic_affine",
            "component": "J_X^kin_affine",
            "zero_condition": "S_X^kin is centered homogeneous quadratic with no affine shift X0(q) and no linear term",
            "current_status": "NOT_PARENT_SIGNED",
            "failure_mode": "shifted origin or hidden representative marker creates a source term",
            "next_action": "derive zero-origin/evenness from primitive constraint/auxiliary structure or retain shifted-source norm",
            "valid_for_claim": "False",
        },
        {
            "component_id": "JX2627_1_matter",
            "component": "J_X^matter",
            "zero_condition": "ordinary matter depends only on descended observed coframe e_obs=Obs_e(q(Phi)), matter fields, and quotient-owned constants; X is quotient-null",
            "current_status": "CONDITIONAL_ONLY",
            "failure_mode": "Weyl/disformal/mass/source-label channel makes matter feel X",
            "next_action": "prove quotient matter functor/no-shadow-frame/no-source-only-slot or retain b_g, b_dis, b_A, q_nonH rows",
            "valid_for_claim": "False",
        },
        {
            "component_id": "JX2627_2_observed_slot",
            "component": "J_X^obs",
            "zero_condition": "observed/source coupling is multiplied by f(chi_D) with f(0)=0 on the local exterior branch",
            "current_status": "RELATIVE_ZERO_AT_LOCAL_BRANCH_ORIGIN_UNSIGNED",
            "failure_mode": "double-zero gate is a closure choice unless parent action owns f and C_obs slot",
            "next_action": "source parent origin of the two-slot split and coupling list",
            "valid_for_claim": "False",
        },
        {
            "component_id": "JX2627_3_chi_wall",
            "component": "J_X^chi_wall",
            "zero_condition": "f_prime(0)=0, chi_D does not move with X in the local variation, and domain-wall stress is absent/exact",
            "current_status": "CONDITIONAL_ONLY",
            "failure_mode": "selector/domain wall produces a surface source even if f(0)=0",
            "next_action": "derive no wall stress or retain J_chi_wall_norm",
            "valid_for_claim": "False",
        },
        {
            "component_id": "JX2627_4_boundary",
            "component": "J_X^boundary",
            "zero_condition": "Dirichlet, zero-flux plus zero mode removal, or exact/topological boundary primitive with zero local projection",
            "current_status": "NOT_DERIVED",
            "failure_mode": "boundary hair drives alpha3, Gdot, alpha2, xi, gamma/R10 residuals",
            "next_action": "prove boundary no-hair or source boundary_lift_norm/projection coefficients",
            "valid_for_claim": "False",
        },
        {
            "component_id": "JX2627_5_history",
            "component": "J_X^history",
            "zero_condition": "memory kernel is local, causal, stable, source-free, and has no long tail in compact local exterior",
            "current_status": "NOT_DERIVED",
            "failure_mode": "history tail creates clock/Gdot/cosmology-to-local leakage",
            "next_action": "derive local Lyapunov/kernel silence or retain history_tail_norm",
            "valid_for_claim": "False",
        },
        {
            "component_id": "JX2627_6_total_verdict",
            "component": "J_X_total",
            "zero_condition": "all components JX2627_0..5 vanish and boundary zero/gap gates pass",
            "current_status": "JX_ZERO_NOT_PROVED",
            "failure_mode": "any one live component makes memory finite residual instead of theorem-zero",
            "next_action": "prefer constraint/auxiliary elimination route; otherwise fill residual bound rows",
            "valid_for_claim": "False",
        },
    ]


def boundary_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "boundary_id": "BZ2627_0_variational_boundary_term",
            "gate": "identify X boundary term",
            "status": "TERM_IDENTIFIED",
            "mathematical_condition": "delta_X S_boundary cancels or fixes n_i A^ij nabla_j X on partial D",
            "gap": "parent boundary condition not selected",
            "valid_for_claim": "False",
        },
        {
            "boundary_id": "BZ2627_1_dirichlet",
            "gate": "Dirichlet local no-hair",
            "status": "CONDITIONAL_ROUTE",
            "mathematical_condition": "X|partialD=0 or fixed universal calibration value",
            "gap": "could be imposed closure; not parent-derived",
            "valid_for_claim": "False",
        },
        {
            "boundary_id": "BZ2627_2_neumann_zero_mean",
            "gate": "zero flux plus zero mean/topological class",
            "status": "CONDITIONAL_ROUTE",
            "mathematical_condition": "n.A.grad X=0 and constant/topological mode removed or universal",
            "gap": "zero-mode and parent-selected class not signed",
            "valid_for_claim": "False",
        },
        {
            "boundary_id": "BZ2627_3_exact_topological",
            "gate": "exact/topological boundary primitive",
            "status": "CONDITIONAL_ROUTE_NOT_DERIVED",
            "mathematical_condition": "boundary current is exact or pure bookkeeping with zero local representative",
            "gap": "417 says boundary primitive, Bianchi gate, projected flux, and secular drift fail",
            "valid_for_claim": "False",
        },
        {
            "boundary_id": "BZ2627_4_wall_stress",
            "gate": "no metric/domain wall stress",
            "status": "NOT_DERIVED",
            "mathematical_condition": "metric variation of boundary/domain selector has no local stress or is Ward-owned",
            "gap": "boundary polarization/local wall stress not parent-signed",
            "valid_for_claim": "False",
        },
        {
            "boundary_id": "BZ2627_5_current_verdict",
            "gate": "boundary zero package",
            "status": "BOUNDARY_ZERO_NOT_PARENT_DERIVED",
            "mathematical_condition": "one boundary route must pass from parent action, or finite boundary residual rows must be used",
            "gap": "no local-GR memory zero claim",
            "valid_for_claim": "False",
        },
    ]


def residual_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RBP2627_0_lambda_gap",
            "arena": "all local",
            "quantity": "lambda_gap or m_X/range lower bound",
            "bound_or_anchor": "formula only: lambda_gap >= a_min lambda_1(D)+m_min^2",
            "units": "1/length^2",
            "missing_mts_input": "MISSING_A_MIN;MISSING_LAMBDA1_D;MISSING_MX2",
            "row_status": "TEMPLATE_NOT_SCOREABLE",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RBP2627_1_JX_norm",
            "arena": "all local",
            "quantity": "||J_X|| <= sum component norms",
            "bound_or_anchor": "component decomposition only",
            "units": "operator-normalized source units",
            "missing_mts_input": "MISSING_J_KIN_AFFINE;MISSING_J_MATTER;MISSING_J_CHID;MISSING_J_BOUNDARY;MISSING_J_HISTORY",
            "row_status": "TEMPLATE_NOT_SCOREABLE",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RBP2627_2_boundary_lift",
            "arena": "PPN/Gdot/R10/local flux",
            "quantity": "boundary_lift_norm",
            "bound_or_anchor": "417 pressure anchors only: alpha3 4e-20, Gdot 9.6e-15/yr, alpha2 2e-9, xi 4e-9, gamma-scale 2.3e-5",
            "units": "mixed arena units",
            "missing_mts_input": "MISSING_BOUNDARY_FLUX_PROJECTION_COEFFICIENT;MISSING_BOUNDARY_NORM",
            "row_status": "SOURCE_BACKED_ANCHORS_NOT_MTS_SCORE",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RBP2627_3_X_amplitude",
            "arena": "all local",
            "quantity": "||X||_L2",
            "bound_or_anchor": "||X||_L2 <= (||J_X|| + boundary_lift_norm)/lambda_gap",
            "units": "X units times sqrt(volume)",
            "missing_mts_input": "MISSING_NUMERIC_JX;MISSING_BOUNDARY_LIFT;MISSING_LAMBDA_GAP",
            "row_status": "TEMPLATE_NOT_SCOREABLE",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RBP2627_4_local_projection",
            "arena": "R10/PPN/clock/Gdot/orbital/WEP",
            "quantity": "Delta O_i <= K_i ||X|| + K_i_grad ||grad X||",
            "bound_or_anchor": "projection formula only",
            "units": "arena-specific",
            "missing_mts_input": "MISSING_K_R10;MISSING_K_PPN;MISSING_K_CLOCK;MISSING_K_GDOT;MISSING_K_ORBITAL;MISSING_K_WEP",
            "row_status": "TEMPLATE_NOT_SCOREABLE",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RBP2627_5_score_gate",
            "arena": "all local",
            "quantity": "valid_for_claim",
            "bound_or_anchor": "false until theorem-zero or numeric sourced MTS coefficients with bound comparisons exist",
            "units": "boolean",
            "missing_mts_input": "REQUIRES_ALL_PREVIOUS_ROWS",
            "row_status": "FORCED_FALSE",
            "valid_for_claim": "False",
        },
    ]


def constraint_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "bridge_id": "CAB2627_0_physical_scalar_route",
            "route": "propagating X scalar as fundamental local degree of freedom",
            "current_status": "DEMOTED_TO_EFT_CLOSURE_SCAFFOLD",
            "reason": "1856 finds no primitive owner, Z_X, M_X^2, source projection, or same-branch action derivation",
            "use_allowed": "private residual/testing template only",
            "forbidden_use": "derived local-GR/Newton/PPN/R10 claim",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "CAB2627_1_auxiliary_constraint_route",
            "route": "constraint/auxiliary/quotient-first elimination",
            "current_status": "BEST_DERIVATION_ROUTE",
            "reason": "eliminates the source before physical phase space and matter readout, avoiding new fifth-force scalar hair",
            "use_allowed": "next derivation target",
            "forbidden_use": "claiming elimination before constraint algebra, boundary charge, degree count, and matter descent close",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "CAB2627_2_object_language_route",
            "route": "no source-only parent-action slots",
            "current_status": "PARALLEL_REQUIRED_PARENT_SIGNATURE",
            "reason": "2507 shows source-only coefficients w_A/kappa_A remain legal countermodels unless parent grammar forbids them",
            "use_allowed": "coupling/source glue proof target",
            "forbidden_use": "absorbing source weights into measured G without a theorem",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "CAB2627_3_current_choice",
            "route": "use X residual map as nonclaim scaffold while attacking auxiliary/constraint elimination",
            "current_status": "SELECTED",
            "reason": "this preserves all local test pressure while moving toward a derivable GR/Newton branch",
            "use_allowed": "2628 target",
            "forbidden_use": "re-promoting physical scalar memory as a fundamental route without new evidence",
            "valid_for_claim": "False",
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM2627_0_shifted_memory_origin",
            "countermodel": "X has an affine origin X0(q) or hidden representative marker",
            "blocks": "J_X^kin_affine=0",
            "required_kill_clause": "parent-centered even/homogeneous origin or auxiliary constraint elimination",
            "retained": "True",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM2627_1_matter_frame_leak",
            "countermodel": "ordinary matter carries Weyl/disformal/mass/source-label dependence on X",
            "blocks": "J_X^matter=0 and WEP/source universality",
            "required_kill_clause": "quotient observed-coframe matter functor plus no-shadow-frame and no-source-only-slot theorems",
            "retained": "True",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM2627_2_domain_wall_source",
            "countermodel": "chi_D or local selector variation creates wall stress/source",
            "blocks": "J_X^chi_wall=0 and boundary zero",
            "required_kill_clause": "f(0)=f'(0)=0 from parent plus no moving-boundary stress",
            "retained": "True",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM2627_3_boundary_hair",
            "countermodel": "boundary primitive or local flux carries finite alpha3/Gdot/PPN/R10 hair",
            "blocks": "boundary zero and local extra-sector silence",
            "required_kill_clause": "exact/topological no-hair, fixed subtraction, or sourced finite residual bound",
            "retained": "True",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM2627_4_history_tail",
            "countermodel": "compact-local memory has a long causal tail or calibration response source",
            "blocks": "J_X^history=0 and branch-invariant projection",
            "required_kill_clause": "local stable source-free kernel or conservation-signed response source",
            "retained": "True",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2627_0_JX_zero",
            "claim": "total J_X vanishes in the local exterior",
            "current_evidence": "component map written; zero conditions not all parent-signed",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2627_1_boundary_zero",
            "claim": "boundary flux/lift vanishes",
            "current_evidence": "conditional routes only; 417 blockers remain",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2627_2_memory_zero",
            "claim": "positive operator proves X=0",
            "current_evidence": "source and boundary gates fail",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2627_3_residual_score",
            "claim": "finite memory residual is scoreable against R10/PPN/clock/orbital",
            "current_evidence": "source-backed anchors exist but MTS projection/source coefficients are missing",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2627_4_constraint_elimination",
            "claim": "constraint/auxiliary route eliminates X before physical phase space",
            "current_evidence": "best route selected by 1856 but algebra/boundary/degree/matter gates unsigned",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2627_5_local_GR_Newton",
            "claim": "local GR/Newton derivation follows",
            "current_evidence": "memory/source/boundary/object-language gates remain open",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2627_0_source_map",
            "decision": "JX_SOURCE_MAP_DERIVED_AS_CONTRACT_NOT_ZERO",
            "rationale": "variation gives the exact component map, but components are not all parent-zero",
            "next_action": "use component gates as theorem requirements or residual rows",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2627_1_boundary",
            "decision": "BOUNDARY_ZERO_NOT_PARENT_DERIVED",
            "rationale": "Dirichlet/zero-flux/exact routes are mathematically valid but not selected by the parent",
            "next_action": "derive boundary no-hair or retain boundary_lift_norm",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2627_2_scalar_policy",
            "decision": "PHYSICAL_SCALAR_REMAINS_CLOSURE_ONLY",
            "rationale": "1856 demotes physical Xhat as fundamental; using it as a claim route would invite fifth-force failure",
            "next_action": "do not promote the scalar memory branch without new primitive owner evidence",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2627_3_best_next",
            "decision": "CONSTRAINT_AUXILIARY_MEMORY_SOURCE_ELIMINATION_NEXT",
            "rationale": "the least fragile path to local GR is to eliminate X before matter/readout, not tune a propagating scalar quiet",
            "next_action": "derive or reject the constraint/auxiliary source-elimination theorem while preserving residual interface",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2628-Y5-R2FR-constraint-auxiliary-memory-source-elimination-or-residual-interface.md",
            "script": "scripts/Y5_R2FR_constraint_auxiliary_memory_source_elimination_or_residual_interface_2628.py",
            "objective": "prove or reject the route where X is an auxiliary/constraint/quotient-null object eliminated before physical phase space and matter readout; if it fails, keep the finite residual interface explicit",
            "include": "constraint algebra, auxiliary equation, boundary charge, degree count, matter descent, no-source-only object-language link, residual interface",
            "exclude": "physical scalar local-GR claim, R10/PPN/clock/orbital pass, invented coefficients, GitHub action, formalization-workbench edits",
            "valid_for_claim": "False",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("COPY2627_jx_gate", "jx_component_zero_gate", OUTPUTS["component_gate"], LOCAL_BOUNDS / "Memory_JX_component_zero_gate_2627_NONCLAIM.csv"),
        ("COPY2627_boundary_gate", "boundary_zero_gate", OUTPUTS["boundary_gate"], LOCAL_BOUNDS / "Memory_boundary_zero_gate_2627_NONCLAIM.csv"),
        ("COPY2627_residual_pack", "finite_residual_bound_pack", OUTPUTS["residual_pack"], LOCAL_BOUNDS / "Memory_finite_residual_bound_pack_2627_NONCLAIM.csv"),
        ("COPY2627_constraint_bridge", "constraint_auxiliary_bridge", OUTPUTS["constraint_bridge"], LOCAL_BOUNDS / "Memory_constraint_auxiliary_bridge_2627_NONCLAIM.csv"),
        ("COPY2627_next_target", "next_target", OUTPUTS["next_target"], RAB_QUEUE / "JR2627_CONSTRAINT_AUXILIARY_MEMORY_SOURCE_ELIMINATION_NEXT.csv"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, label, source, destination in copy_specs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": copy_id,
                "label": label,
                "source_path": str(source),
                "destination_path": str(destination),
                "destination_exists": b(destination.exists()),
                "csv_parses": b(csv_parses(destination)),
                "row_count": len(read_csv(destination)) if destination.exists() else 0,
            }
        )
    return rows


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            if row.get("valid_for_claim", "False") != "False":
                return False
            if row.get("claim_allowed", "False") != "False":
                return False
            if row.get("gate_pass", "False") == "True":
                return False
    return True


def missing_not_claim_ready(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            joined = " ".join(str(value) for value in row.values())
            if "MISSING_" in joined and row.get("valid_for_claim", "False") != "False":
                return False
    return True


def validation_rows(generated_paths: list[Path], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    variation_rows = read_csv(OUTPUTS["variation_map"])
    component_rows = read_csv(OUTPUTS["component_gate"])
    boundary_rows = read_csv(OUTPUTS["boundary_gate"])
    residual_rows = read_csv(OUTPUTS["residual_pack"])
    bridge_rows = read_csv(OUTPUTS["constraint_bridge"])
    gate_rows = read_csv(OUTPUTS["claim_gates"])
    decision_rows_read = read_csv(OUTPUTS["decision"])
    formalization_patterns = [
        "2627-Y5-R2FR-parent-memory-source-boundary-map-or-finite-residual-bound-pack.md",
        "Y5_R2FR_parent_memory_source_boundary_map_or_finite_residual_bound_pack_2627.py",
        f"{PREFIX}*",
        "P8_Y5_BRR545_2627_VALIDATION.csv",
        "Memory_JX_component_zero_gate_2627_NONCLAIM.csv",
        "Memory_boundary_zero_gate_2627_NONCLAIM.csv",
        "Memory_finite_residual_bound_pack_2627_NONCLAIM.csv",
        "Memory_constraint_auxiliary_bridge_2627_NONCLAIM.csv",
        "JR2627_CONSTRAINT_AUXILIARY_MEMORY_SOURCE_ELIMINATION_NEXT.csv",
    ]
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in formalization_patterns:
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    pycache_path = ROOT / "scripts" / "__pycache__"
    checks = [
        (
            "VAL2627_00_sources_exist",
            all(row["exists"] == "True" and row["needles_present"] == "True" for row in source_rows),
            "all cited source paths exist and needles are present",
        ),
        (
            "VAL2627_01_variation_map_written",
            any(row["map_id"] == "JVM2627_4_current_verdict" and row["current_status"] == "JX_ZERO_NOT_PROVED" for row in variation_rows),
            "J_X variation/source map written without zero claim",
        ),
        (
            "VAL2627_02_component_gate_blocks_claim",
            any(row["component_id"] == "JX2627_6_total_verdict" and row["current_status"] == "JX_ZERO_NOT_PROVED" for row in component_rows),
            "component zero gate keeps total J_X unproved",
        ),
        (
            "VAL2627_03_boundary_not_derived",
            any(row["boundary_id"] == "BZ2627_5_current_verdict" and row["status"] == "BOUNDARY_ZERO_NOT_PARENT_DERIVED" for row in boundary_rows),
            "boundary zero package is not parent-derived",
        ),
        (
            "VAL2627_04_residual_pack_nonclaim",
            all(row["valid_for_claim"] == "False" and row["row_status"] != "SCOREABLE" for row in residual_rows),
            "finite residual rows remain nonclaim templates/anchors",
        ),
        (
            "VAL2627_05_scalar_demoted_bridge",
            any(row["bridge_id"] == "CAB2627_0_physical_scalar_route" and row["current_status"] == "DEMOTED_TO_EFT_CLOSURE_SCAFFOLD" for row in bridge_rows),
            "physical scalar route stays demoted",
        ),
        (
            "VAL2627_06_constraint_route_selected",
            any(row["bridge_id"] == "CAB2627_1_auxiliary_constraint_route" and row["current_status"] == "BEST_DERIVATION_ROUTE" for row in bridge_rows),
            "constraint/auxiliary route is selected as the best derivation route",
        ),
        (
            "VAL2627_07_claim_gates_safe",
            all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in gate_rows),
            "all memory/source/local-GR claim gates are false",
        ),
        (
            "VAL2627_08_no_claim_flags",
            no_claim_flags([OUTPUTS["variation_map"], OUTPUTS["component_gate"], OUTPUTS["boundary_gate"], OUTPUTS["residual_pack"], OUTPUTS["constraint_bridge"], OUTPUTS["countermodels"], OUTPUTS["decision"], OUTPUTS["next_target"]]),
            "no generated claim-sensitive row is valid_for_claim=true or claim_allowed=true",
        ),
        (
            "VAL2627_09_missing_not_ready",
            missing_not_claim_ready([OUTPUTS["component_gate"], OUTPUTS["residual_pack"]]),
            "no MISSING_* row is marked claim-ready",
        ),
        (
            "VAL2627_10_decision_next",
            any(row["decision_id"] == "DEC2627_3_best_next" and row["decision"] == "CONSTRAINT_AUXILIARY_MEMORY_SOURCE_ELIMINATION_NEXT" for row in decision_rows_read),
            "decision selects constraint/auxiliary memory source elimination",
        ),
        (
            "VAL2627_11_branch_copies",
            all(row["destination_exists"] == "True" and row["csv_parses"] == "True" for row in branch_rows),
            "branch/local/queue copies exist and parse",
        ),
        (
            "VAL2627_12_formalization_untouched",
            len(formalization_hits) == 0,
            "no 2627 outputs found under formalization-workbench",
        ),
        (
            "VAL2627_13_csv_parse",
            all(csv_parses(path) for path in generated_paths),
            "all generated 2627 CSVs parse",
        ),
        (
            "VAL2627_14_pycache_absent",
            not pycache_path.exists(),
            "scripts __pycache__ absent",
        ),
    ]
    rows = [
        {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "False",
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2627_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2627 parent memory source-boundary map or finite residual bound pack",
            "valid_for_claim": "False",
        }
    )
    return rows


def escape_md(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape_md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def build_doc(tables: dict[str, list[dict[str, Any]]]) -> str:
    generated_at = datetime.now(timezone.utc).isoformat()
    return f"""# 2627 — Y5 R2/f(R) Parent Memory Source-Boundary Map Or Finite Residual Bound Pack

Generated: `{generated_at}`

Status: `Y5_R2FR_2627_JX_source_boundary_map_contract_written_JX_zero_not_proved_scalar_closure_constraint_route_selected_nonclaim`

Claim ceiling: no `J_X=0` proof, no boundary-zero proof, no memory theorem-zero, no finite residual score, no R10/PPN/clock/orbital/WEP pass, no EH/Newton/local-GR claim is made.

## Summary

2627 writes the exact thing the memory route was missing: the source-boundary contract for `J_X`. The variation is now explicit enough to stop hand-waving:

`L_X X = J_X`, with `J_X = J_kin_affine + J_matter + J_obs + J_chi_wall + J_boundary + J_history`.

The useful gain is that each zero condition is now named. The hard truth is that the total zero is still not proven. Matter blindness needs quotient observed-coframe descent; boundary silence needs parent-selected no-hair; the history tail needs local stable kernel silence; and the physical propagating scalar route is demoted by the later 1856 result.

So the best route is not to worship the scalar. Use the scalar equations as a nonclaim residual scaffold, then attack the more native route: `X` as auxiliary/constraint/quotient-null, eliminated before physical phase space and matter readout. That is the cleanest path toward derived local GR/Newton.

## Source Register

{markdown_table(tables["source_register"])}

## Lineage Ledger

{markdown_table(tables["lineage"])}

## JX Variation Map

{markdown_table(tables["variation_map"])}

## JX Component Zero Gate

{markdown_table(tables["component_gate"])}

## Boundary Zero Gate

{markdown_table(tables["boundary_gate"])}

## Finite Residual Bound Pack

{markdown_table(tables["residual_pack"])}

## Constraint / Auxiliary Bridge

{markdown_table(tables["constraint_bridge"])}

## Countermodel Ledger

{markdown_table(tables["countermodels"])}

## Claim Gates

{markdown_table(tables["claim_gates"])}

## Decision Ledger

{markdown_table(tables["decision"])}

## Next Target

{markdown_table(tables["next_target"])}

## Branch Copies

{markdown_table(tables["branch_copies"])}

## Validation

{markdown_table(tables["validation"])}

## Plain-English Verdict

This is progress, but not a victory lap. We now know exactly what must vanish for memory silence:

1. no shifted kinetic origin;
2. no matter-frame/source-label coupling to `X`;
3. no observed-slot coupling at the local branch;
4. no `chi_D` wall source;
5. no boundary lift/local flux;
6. no history tail.

Current corpus does not prove all six. The cleanest next move is the constraint/auxiliary route: show `X` is not a physical scalar at all, but a pre-readout constraint/null/auxiliary object. If that works, local GR becomes much less grim because there is no scalar hair to hide. If it fails, the residual interface is already waiting with the correct source rows.
"""


def main() -> None:
    ensure_dirs()
    tables = {
        "source_register": source_register_rows(),
        "lineage": lineage_rows(),
        "variation_map": variation_map_rows(),
        "component_gate": component_gate_rows(),
        "boundary_gate": boundary_gate_rows(),
        "residual_pack": residual_pack_rows(),
        "constraint_bridge": constraint_bridge_rows(),
        "countermodels": countermodel_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for name, rows in tables.items():
        write_csv(OUTPUTS[name], rows)
    branch_rows = copy_branch_outputs()
    tables["branch_copies"] = branch_rows
    write_csv(OUTPUTS["branch_copies"], branch_rows)
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(generated_paths, branch_rows)
    tables["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC_PATH.write_text(build_doc(tables), encoding="utf-8")
    print(DOC_PATH)
    print(OUTPUTS["validation"])


if __name__ == "__main__":
    main()

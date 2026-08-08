from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_NORMAL_FORM_2485"
CHECKPOINT_ID = "2485"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2485-Y5-R2FR-parent-normal-form-field-symmetry-derivative-grammar.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_NORMAL_FORM_2485_SOURCE_REGISTER.csv",
    "field_sort": OUT / "P8_Y5_PARENT_NORMAL_FORM_2485_FIELD_SORT_TABLE.csv",
    "quotient_descent": OUT / "P8_Y5_PARENT_NORMAL_FORM_2485_QUOTIENT_DESCENT_MAP.csv",
    "symmetry_noether": OUT / "P8_Y5_PARENT_NORMAL_FORM_2485_SYMMETRY_NOETHER_LEDGER.csv",
    "derivative_grammar": OUT / "P8_Y5_PARENT_NORMAL_FORM_2485_DERIVATIVE_GRAMMAR.csv",
    "normal_form": OUT / "P8_Y5_PARENT_NORMAL_FORM_2485_NORMAL_FORM_CONTRACT.csv",
    "coefficient_slots": OUT / "P8_Y5_PARENT_NORMAL_FORM_2485_COEFFICIENT_SLOT_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_NORMAL_FORM_2485_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_PARENT_NORMAL_FORM_2485_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_NORMAL_FORM_2485_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_NORMAL_FORM_2485_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2485_VALIDATION.csv",
}

COPY_TARGETS = {
    "field_sort": LOCAL_BOUNDS / "Parent_field_sort_table_2485_NONCLAIM.csv",
    "quotient_descent": LOCAL_BOUNDS / "Parent_quotient_descent_map_2485_NONCLAIM.csv",
    "normal_form": LOCAL_BOUNDS / "Parent_normal_form_contract_2485_NONCLAIM.csv",
    "coefficient_slots": LOCAL_BOUNDS / "Parent_coefficient_slot_ledger_2485_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2485_PARENT_FIELD_SORT_QUOTIENT_MAP_SIGNATURE.csv",
}

SOURCES = [
    {
        "source_id": "SRC2485_00_2484_doc",
        "source_path": ROOT / "2484-Y5-R2FR-EH-uniqueness-hypotheses-or-parent-normal-form-blocker.md",
        "needles": ["NEXT2484_0_selected", "THM2484_2_parent_normal_form_requirement", "VAL2484_OVERALL"],
        "role": "handoff requiring parent normal-form skeleton",
    },
    {
        "source_id": "SRC2485_01_1768_normal_form",
        "source_path": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
        "needles": ["ANF1768_0_parent_action_partition", "ANF1768_1_geometry_left_hand_owner", "VAL1768_OVERALL"],
        "role": "older parent action partition and source-map owner rule",
    },
    {
        "source_id": "SRC2485_02_2404_candidate_action",
        "source_path": ROOT / "2404-Y5-R2FR-minimal-parent-action-first-variation-GR-Newton-gate-or-operator-residual-pack.md",
        "needles": ["S_min=S_EH", "CANDIDATE_NOT_DERIVED", "VAL2404_OVERALL"],
        "role": "candidate EH first variation and non-derived warning",
    },
    {
        "source_id": "SRC2485_03_2406_residual_sectors",
        "source_path": ROOT / "2406-Y5-R2FR-sector-by-sector-MTS-residual-variation-and-local-scaling-silence-or-operator-bounds.md",
        "needles": ["SVC2406_0_higher_derivative", "SVC2406_6_verdict", "VAL2406_OVERALL"],
        "role": "non-EH residual sector inventory",
    },
    {
        "source_id": "SRC2485_04_2236_derivative_grammar",
        "source_path": ROOT / "2236-Y5-R2FR-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md",
        "needles": ["SORT2236_0_auxiliary_coordinate", "GRAM2236_5_verdict", "VAL2236_OVERALL"],
        "role": "proof that derivative bans require parent object-language signature",
    },
    {
        "source_id": "SRC2485_05_2237_vertical_null",
        "source_path": ROOT / "2237-Y5-R2FR-RAB-vertical-null-presymplectic-degeneracy-or-finite-ZR-intake.md",
        "needles": ["NULL2237_0_parent_L_theta", "NULL2237_5_verdict", "VAL2237_OVERALL"],
        "role": "parent theta/Omega and vertical-null requirements",
    },
    {
        "source_id": "SRC2485_06_2300_q_normal_form",
        "source_path": ROOT / "2300-Y5-R2FR-minimal-parent-action-q-source-vector-normal-form-or-closure-declaration.md",
        "needles": ["QSLOT2300_0_EH_GR", "QEUL2300_0_q_equation", "VAL2300_OVERALL"],
        "role": "q source-vector normal form and Weyl/source residual warning",
    },
    {
        "source_id": "SRC2485_07_2466_source_bridge",
        "source_path": ROOT / "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
        "needles": ["CUR2466_A_Hilbert_energy_current", "HIL2466_0_define_T", "VAL2466_OVERALL"],
        "role": "Hilbert source-current bridge and no fitted-GM guardrail",
    },
    {
        "source_id": "SRC2485_08_2481_source_norm",
        "source_path": ROOT / "2481-Y5-R2FR-Hilbert-worldtube-source-normalization-zero-certificate-or-Enorm-row.md",
        "needles": ["ENORM2481_0_E_norm", "THM2481_1_mass_readout_cancels_ellJ", "VAL2481_OVERALL"],
        "role": "source-normalization residual vector",
    },
    {
        "source_id": "SRC2485_09_2482_kappa",
        "source_path": ROOT / "2482-Y5-R2FR-kappaG-parent-calibration-or-dynamic-worldtube-closure.md",
        "needles": ["KAP2482_1_parent_origin", "EN2482_0_e_kappaG", "VAL2482_OVERALL"],
        "role": "parent coefficient owner blocker",
    },
    {
        "source_id": "SRC2485_10_1425_common_mode",
        "source_path": ROOT / "1425-Y5-R10-RAB-universal-metric-common-mode-WEP-zero-or-finite-source-demotion.md",
        "needles": ["CMZ1425_0_target", "PREM1425_0_parent_q_map", "VAL1425_9_overall"],
        "role": "matter quotient/common-mode premise warning",
    },
    {
        "source_id": "SRC2485_11_1427_parent_signature",
        "source_path": ROOT / "1427-Y5-R10-RAB-parent-action-signature-or-branch-locked-WEP-input-manifest.md",
        "needles": ["SIG1427_0_action_shape", "SIG1427_4_verdict", "VAL1427_7_overall"],
        "role": "ordinary matter action signature as closure candidate only",
    },
    {
        "source_id": "SRC2485_12_2484_validation",
        "source_path": OUT / "P8_Y5_BRR545_2484_VALIDATION.csv",
        "needles": ["VAL2484_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
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
                }
            )
        )
    return rows


def field_sort_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "field_id": "FS2485_0_public_geometry",
            "symbol": "g_mu_nu or e^a_mu",
            "sort": "public metric/coframe",
            "normal_form_role": "single gravitational readout varied for the local EH branch",
            "candidate_status": "RETAIN_AS_PUBLIC_CANDIDATE",
            "missing_signature": "parent field list and quotient map proving this is the only public gravitational variable",
            "downstream_residual_if_unsigned": "e_EH_hyp",
            "valid_for_claim": False,
        },
        {
            "field_id": "FS2485_1_matter",
            "symbol": "Psi",
            "sort": "ordinary matter fields",
            "normal_form_role": "source of Hilbert stress T_H through one descended metric/coframe",
            "candidate_status": "CONDITIONAL_METRIC_MATTER_BRANCH",
            "missing_signature": "ordinary matter action argument list, no source-only prefactors, constants owner",
            "downstream_residual_if_unsigned": "E_norm;finite_WEP_source_residual",
            "valid_for_claim": False,
        },
        {
            "field_id": "FS2485_2_clock_time",
            "symbol": "theta_obs,tau",
            "sort": "clock/time coframe or readout direction",
            "normal_form_role": "defines Hilbert source current and local clock branch",
            "candidate_status": "CONDITIONAL_SOURCE_CLOCK",
            "missing_signature": "tau normalization, clock compatibility, exchange identity, tau_source=tau_charge=tau_clock=tau_readout",
            "downstream_residual_if_unsigned": "e_clock_exchange;c_memory_frame",
            "valid_for_claim": False,
        },
        {
            "field_id": "FS2485_3_q_private",
            "symbol": "q",
            "sort": "private reciprocal/source-vector representative",
            "normal_form_role": "must be first-class/vertical absent or carried as finite source-vector residual",
            "candidate_status": "RETAIN_AS_PRIVATE_OR_RESIDUAL",
            "missing_signature": "q first-class removal, Ricci/Weyl split, source-vector zero or bound",
            "downstream_residual_if_unsigned": "c_q_source;B_qW;C_qT;tail_q",
            "valid_for_claim": False,
        },
        {
            "field_id": "FS2485_4_auxiliary_compatibility",
            "symbol": "R_AB,lambda_R,lambda_C",
            "sort": "auxiliary/constraint compatibility variables",
            "normal_form_role": "must eliminate algebraically or be finite residual fields",
            "candidate_status": "AUXILIARY_SORT_UNSIGNED",
            "missing_signature": "vertical-null presymplectic certificate, no vertical metric, zero boundary charge",
            "downstream_residual_if_unsigned": "c_aux;Z_R;q_R",
            "valid_for_claim": False,
        },
        {
            "field_id": "FS2485_5_projector_readout",
            "symbol": "Pi_M,P_loc",
            "sort": "projector/readout map",
            "normal_form_role": "must commute with variation/exterior derivative or appear as operator residual",
            "candidate_status": "READOUT_OPERATOR_UNSIGNED",
            "missing_signature": "delta_g Pi_M=0 and [d,Pi_M]J_H=0 before local source readout",
            "downstream_residual_if_unsigned": "c_projector_operator",
            "valid_for_claim": False,
        },
        {
            "field_id": "FS2485_6_memory_coframe",
            "symbol": "Q_tau,C_tau,theta_X",
            "sort": "memory/current-chain/coframe residual variables",
            "normal_form_role": "must descend to public coframe or remain as preferred-frame/clock residual",
            "candidate_status": "FRAME_TAU_LOCK_UNSIGNED",
            "missing_signature": "terminal public coframe and tau-lock theorem",
            "downstream_residual_if_unsigned": "c_memory_frame;PPN_alpha_i",
            "valid_for_claim": False,
        },
        {
            "field_id": "FS2485_7_boundary_reference",
            "symbol": "B_ref,S_GHY,Q_boundary,H_ref",
            "sort": "boundary/reference/corner data",
            "normal_form_role": "makes variation well posed and fixes local boundary/falloff before readout",
            "candidate_status": "BOUNDARY_CLASS_UNSIGNED",
            "missing_signature": "boundary variational class, zero compact flux, reference lock",
            "downstream_residual_if_unsigned": "c_boundary_operator;DeltaE_boundary",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def quotient_descent_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "map_id": "QD2485_0_parent_quotient",
            "map_statement": "q_parent: Phi_parent -> (e_obs,g_obs,theta_obs,ordinary matter readout)",
            "required_identity": "public observables depend only on q_parent(Phi), not on representative variables",
            "current_status": "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "blocker": "field-by-field quotient map and ker(Dq) generators missing",
            "claim_effect": "cannot use vertical silence or common-mode matter theorem as proof yet",
            "valid_for_claim": False,
        },
        {
            "map_id": "QD2485_1_matter_descent",
            "map_statement": "S_matter = S_matter[Psi,e_obs(q_parent(Phi)),theta_obs]",
            "required_identity": "delta_v S_matter=0 for vertical representative variations v in ker(Dq), except retained constants/readout residuals",
            "current_status": "CLOSURE_CANDIDATE_ONLY",
            "blocker": "ordinary matter argument list and no source-prefactor theorem are unsigned",
            "claim_effect": "WEP/common-mode and Hilbert-source universality remain conditional",
            "valid_for_claim": False,
        },
        {
            "map_id": "QD2485_2_auxiliary_verticality",
            "map_statement": "R_AB, q, memory and projector representatives are absent from public geometry or live in controlled fibres",
            "required_identity": "Dq[v_X]=0 plus zero boundary Hamiltonian charge for each eliminated representative",
            "current_status": "PARTIAL_CONDITIONAL_THEOREM_ONLY",
            "blocker": "parent theta/Omega, vertical generators, no-vertical-metric and boundary charge theorems missing",
            "claim_effect": "derivative bans and residual zero claims cannot be promoted",
            "valid_for_claim": False,
        },
        {
            "map_id": "QD2485_3_readout_order",
            "map_statement": "variation is performed before readout/projector operations",
            "required_identity": "Pi_M is fixed chain map or its variation/commutator terms are included in S_res",
            "current_status": "OBSTRUCTION_EXPLICIT_NOT_ZEROED",
            "blocker": "delta_g Pi_M and [d,Pi_M]J_H not parent-zeroed",
            "claim_effect": "source normalization/local vacuum cannot silently drop projector residuals",
            "valid_for_claim": False,
        },
        {
            "map_id": "QD2485_4_constants_owner",
            "map_statement": "masses, charges, alpha_EM and clock standards are quotient-owned or residual-owned",
            "required_identity": "no hidden composition/source marker survives in local matter response",
            "current_status": "HARD_BLOCKER_UNSIGNED",
            "blocker": "constants/action-scale owner and radiative stability not derived",
            "claim_effect": "EM/particle/clock extensions cannot be used as local-GR proof shortcuts",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def symmetry_noether_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "symmetry_id": "SYM2485_0_diffeomorphism",
            "generator": "xi^mu",
            "required_action": "delta_xi S_parent = boundary term for all parent fields",
            "noether_output": "nabla_mu(E_geom+E_MTS-kappa_MTS T_H)^{mu nu}=0 after quotient/descent",
            "current_status": "MISSING_PARENT_DIFF_GENERATOR",
            "missing_for_claim": "field transformations for q,tau,memory,projector,boundary plus differentiable charge",
            "valid_for_claim": False,
        },
        {
            "symmetry_id": "SYM2485_1_local_lorentz_if_coframe",
            "generator": "lambda^a_b",
            "required_action": "coframe action is invariant under local frame rotations or frame gauge is fixed before variation",
            "noether_output": "no antisymmetric stress/preferred-frame leak from coframe variables",
            "current_status": "COFRAME_GAUGE_UNSIGNED",
            "missing_for_claim": "terminal public coframe and memory/frame residual silence",
            "valid_for_claim": False,
        },
        {
            "symmetry_id": "SYM2485_2_vertical_gauge",
            "generator": "v_X in ker(Dq)",
            "required_action": "representative variables generate null directions of parent presymplectic form with zero boundary charge",
            "noether_output": "auxiliary/q/R_AB variables cannot carry independent local stress or derivative energy",
            "current_status": "MISSING_PARENT_OMEGA_VERTICAL_NULL",
            "missing_for_claim": "theta_MTS, Omega_parent, v_X and boundary-zero theorem",
            "valid_for_claim": False,
        },
        {
            "symmetry_id": "SYM2485_3_clock_exchange",
            "generator": "tau/time readout compatibility",
            "required_action": "clock/source/readout sectors satisfy a parent exchange identity",
            "noether_output": "Hilbert current worldtube charge is conserved or exchange residual is explicit",
            "current_status": "MISSING_DYNAMIC_EXCHANGE_IDENTITY",
            "missing_for_claim": "nabla_mu J_M^mu + I_tau + I_A = 0 and jump/support theorem",
            "valid_for_claim": False,
        },
        {
            "symmetry_id": "SYM2485_4_boundary_charge",
            "generator": "allowed boundary/corner transformations",
            "required_action": "boundary symplectic flux and reference shifts are fixed or zero",
            "noether_output": "no hidden B_ref/H_ref/source-worldtube charge enters local tests",
            "current_status": "BOUNDARY_SYMMETRY_UNSIGNED",
            "missing_for_claim": "shared falloff class, differentiable Hamiltonian, zero compact linked-boundary flux",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def derivative_grammar_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "grammar_id": "DG2485_0_cosmological_density",
            "operator": "sqrt(-g) a0",
            "slot": "zeroth-derivative public geometry",
            "normal_form_status": "ALLOWED_CONDITIONAL",
            "reason": "local diffeomorphism invariant scalar density",
            "required_owner": "a0/Lambda branch convention and local subtraction rule",
            "valid_for_claim": False,
        },
        {
            "grammar_id": "DG2485_1_EH_scalar",
            "operator": "sqrt(-g) a1 R[e]",
            "slot": "two-derivative public geometry",
            "normal_form_status": "TARGET_LEADING_OPERATOR",
            "reason": "EH-leading term in the conditional uniqueness route",
            "required_owner": "parent coefficient a1=1/(2*kappa_MTS) and field/symmetry signature",
            "valid_for_claim": False,
        },
        {
            "grammar_id": "DG2485_2_topological_boundary",
            "operator": "S_top + S_GHY + B_ref + corner terms",
            "slot": "boundary/topological completion",
            "normal_form_status": "ALLOWED_ONLY_WITH_BOUNDARY_CLASS",
            "reason": "needed for well-posed variation but cannot carry hidden local stress",
            "required_owner": "boundary/falloff/reference lock and zero flux theorem",
            "valid_for_claim": False,
        },
        {
            "grammar_id": "DG2485_3_higher_curvature",
            "operator": "R^2, R_munu R^munu, R box R, higher derivative public operators",
            "slot": "higher-derivative geometry",
            "normal_form_status": "RETAIN_AS_c_HD_UNLESS_FORBIDDEN_OR_BOUNDED",
            "reason": "2406 keeps c_HD live; derivative-order uniqueness needs this absent at leading local order",
            "required_owner": "parent object-language theorem, topological classification, or source-backed local bound",
            "valid_for_claim": False,
        },
        {
            "grammar_id": "DG2485_4_vertical_derivatives",
            "operator": "D R_AB, D q, vertical metric/connection terms",
            "slot": "private/auxiliary kinetic energy",
            "normal_form_status": "RETAIN_FINITE_BRANCH_UNLESS_VERTICAL_NULL_PROVED",
            "reason": "2236/2237 show derivative bans are exact only after parent-null proof",
            "required_owner": "ker(Dq)=ker(Omega_parent), no vertical metric, zero boundary charge",
            "valid_for_claim": False,
        },
        {
            "grammar_id": "DG2485_5_nonminimal_matter",
            "operator": "f(X,Phi,labels)L_m, A(X)J_m, source-only prefactors",
            "slot": "ordinary matter nonminimal/source-shadow terms",
            "normal_form_status": "RETAIN_AS_SHADOW_OR_FINITE_SOURCE_RESIDUAL",
            "reason": "1768/1425/1427 keep source-prefactor countermodels alive",
            "required_owner": "matter quotient descent, constants owner, no-source-prefactor theorem",
            "valid_for_claim": False,
        },
        {
            "grammar_id": "DG2485_6_projector_postvariation",
            "operator": "Pi_M applied after variation, [d,Pi_M]J_H, delta_g Pi_M",
            "slot": "readout/projector residual",
            "normal_form_status": "RETAIN_AS_c_projector_operator",
            "reason": "post-variation readout can alter source normalization and local vacuum",
            "required_owner": "fixed-chain-map theorem or explicit operator bound",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def normal_form_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "contract_id": "NF2485_0_parent_action_skeleton",
            "formula": "S_parent[Phi]=int_M sqrt(-g)[a0+a1 R[e]+L_matter(Psi,e_obs,theta_obs)+L_aux+L_q+L_tau/memory+sum_i c_i O_i]+S_top+S_boundary",
            "interpretation": "one parent action inventory; every source-like or geometry-like term has an owner before tests",
            "current_status": "SKELETON_WRITTEN_NOT_PARENT_DERIVED",
            "missing_for_claim": "field/sort signature, quotient map, symmetry generator, derivative grammar, coefficient owner, residual zero/bound rows",
            "valid_for_claim": False,
        },
        {
            "contract_id": "NF2485_1_reduced_local_branch",
            "formula": "S_red -> int sqrt(-g)[a0+a1 R[e]] + S_matter[Psi,e_obs,theta_obs] + S_boundary + S_res",
            "interpretation": "desired local GR branch after auxiliary/private variables descend or are integrated out",
            "current_status": "TARGET_REDUCTION_CONDITIONAL",
            "missing_for_claim": "prove S_res=0 or bounded below local thresholds without cancellations",
            "valid_for_claim": False,
        },
        {
            "contract_id": "NF2485_2_public_field_equation",
            "formula": "a1 G_munu + a0 g_munu + DeltaE_MTS_munu + DeltaE_boundary_munu = 1/2 T_H_munu + J_shadow_munu",
            "interpretation": "operator equation before any GR/Newton promotion; coefficient convention can be rescaled after a1 is parent-owned",
            "current_status": "FIELD_EQUATION_SHAPE_NONCLAIM",
            "missing_for_claim": "a1/kappa_MTS, residual silence, source normalization, boundary class",
            "valid_for_claim": False,
        },
        {
            "contract_id": "NF2485_3_Newton_Poisson_gate",
            "formula": "nabla^2 U = 4*pi*G_parent rho_H + S_res, with G_parent derived from a1 only after normal form ownership",
            "interpretation": "Newton follows only after parent coupling and residual source vanish/bound",
            "current_status": "DOWNSTREAM_GATE_NOT_CLOSED",
            "missing_for_claim": "G_parent owner, E_norm zero/bound, C_metric factors, PPN second-order equations",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def coefficient_slot_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "slot_id": "CS2485_0_a1_kappa",
            "symbol": "a1 or kappa_MTS",
            "owner_question": "what parent scale/coupling multiplies R[e]",
            "current_status": "MISSING_COEFFICIENT_OWNER",
            "residual_if_missing": "e_kappaG",
            "next_input": "derive a1 from parent normalization or mark G as empirical coupling explicitly",
            "valid_for_claim": False,
        },
        {
            "slot_id": "CS2485_1_a0_lambda",
            "symbol": "a0 or Lambda_parent",
            "owner_question": "cosmological/local subtraction term",
            "current_status": "MISSING_LOCAL_SUBTRACTION_CONVENTION",
            "residual_if_missing": "Lambda/local background residual",
            "next_input": "separate cosmological constant branch from local Poisson subtraction",
            "valid_for_claim": False,
        },
        {
            "slot_id": "CS2485_2_c_HD",
            "symbol": "c_HD",
            "owner_question": "higher-curvature and higher-derivative coefficients",
            "current_status": "RETAIN_NONCLAIM",
            "residual_if_missing": "higher-derivative local metric response",
            "next_input": "prove derivative grammar excludes them or bound them in PPN/R10",
            "valid_for_claim": False,
        },
        {
            "slot_id": "CS2485_3_c_aux",
            "symbol": "c_aux,Z_R,q_R",
            "owner_question": "auxiliary/compatibility fields eliminate without stress",
            "current_status": "RETAIN_NONCLAIM",
            "residual_if_missing": "auxiliary metric stress or finite R_AB branch",
            "next_input": "parent theta/Omega vertical-null proof or finite source-backed rows",
            "valid_for_claim": False,
        },
        {
            "slot_id": "CS2485_4_c_q_source",
            "symbol": "B_qW,C_qT,Q_q_body,Pi_q,tail_q",
            "owner_question": "q source-vector channels vanish or are bounded",
            "current_status": "RETAIN_NONCLAIM",
            "residual_if_missing": "q exterior Weyl/source-vector residual",
            "next_input": "q first-class removal or Ricci/Weyl split with source-backed bounds",
            "valid_for_claim": False,
        },
        {
            "slot_id": "CS2485_5_c_projector",
            "symbol": "c_projector_operator",
            "owner_question": "projector/readout commutator and metric variation",
            "current_status": "RETAIN_NONCLAIM",
            "residual_if_missing": "source normalization and local-vacuum readout error",
            "next_input": "fixed-chain-map theorem or commutator bound",
            "valid_for_claim": False,
        },
        {
            "slot_id": "CS2485_6_c_memory_frame",
            "symbol": "c_memory_frame,PPN alpha_i",
            "owner_question": "memory/coframe/tau variables leave no preferred-frame stress",
            "current_status": "RETAIN_NONCLAIM",
            "residual_if_missing": "clock drift/preferred-frame residual",
            "next_input": "terminal public coframe and tau-lock proof or PPN bounds",
            "valid_for_claim": False,
        },
        {
            "slot_id": "CS2485_7_E_norm",
            "symbol": "E_norm",
            "owner_question": "Hilbert source mass, worldtube charge and coupling normalization match Newton source",
            "current_status": "RETAIN_NONCLAIM",
            "residual_if_missing": "e_surface_drift,e_clock_exchange,e_jump_support,e_hilbert_shadow,e_kappaG",
            "next_input": "field-sort/quotient map first, then dynamic exchange and jump/support theorem",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2485_0_skeleton_written",
            "claim": "Minimal parent normal-form skeleton is written.",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "Field/sort, quotient, symmetry, derivative grammar and coefficient slots are explicit.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2485_1_parent_action_signed",
            "claim": "MTS parent action is fully signed.",
            "gate_status": "BLOCKED",
            "reason": "Skeleton is a contract, not a derived action inventory.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2485_2_field_quotient_signed",
            "claim": "Typed field list and quotient map are parent-derived.",
            "gate_status": "BLOCKED",
            "reason": "q_parent, ker(Dq), matter descent and constants owner remain unsigned.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2485_3_EH_uniqueness_applies",
            "claim": "EH uniqueness theorem applies to MTS local branch.",
            "gate_status": "BLOCKED",
            "reason": "diffeomorphism generator, derivative grammar and residual silence are not signed.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2485_4_Newton_local_GR",
            "claim": "Newton/local-GR reduction is derived.",
            "gate_status": "BLOCKED",
            "reason": "requires EH origin, kappa owner, residual bounds, source normalization and PPN equations.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2485_5_no_shortcuts",
            "claim": "No EH import, fitted GM, source-prefactor hiding, no-derivative-by-taste, or residual cancellation is used.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "all such moves are retained as explicit blockers or residual slots.",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2485_0_result",
            "decision": "Accept the parent normal-form skeleton as the working private scaffold.",
            "reason": "It connects EH, source normalization, q/R_AB residuals, WEP/common-mode and boundary terms in one object-language ledger.",
            "effect": "future derivations can target exact slots instead of circling coupling fog.",
        },
        {
            "decision_id": "DEC2485_1_not_a_claim",
            "decision": "Do not promote EH/local-GR/Newton.",
            "reason": "The skeleton is not yet a derived parent action, and the quotient map is unsigned.",
            "effect": "e_EH_import, e_kappaG, e_EH_hyp, DeltaE_MTS and E_norm remain active.",
        },
        {
            "decision_id": "DEC2485_2_best_next",
            "decision": "Attack field-sort and quotient-map signature first.",
            "reason": "Without q_parent and ker(Dq), symmetry, derivative bans, matter descent and vertical silence cannot be theorem claims.",
            "effect": "2486 should try to sign the typed field list and quotient map or split residual owners cleanly.",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2485_0_selected",
            "selection_status": "selected",
            "target_file": "2486-Y5-R2FR-parent-field-sort-and-quotient-map-signature-or-residual-owner-split.md",
            "target_script": "scripts/Y5_R2FR_parent_field_sort_and_quotient_map_signature_or_residual_owner_split_2486.py",
            "task": "try to sign the typed parent field list and quotient map q_parent, including ker(Dq) vertical generators, matter descent, constants owner, and readout order; if not, split every unsigned variable into explicit residual owners",
            "acceptance_target": "field-sort/quotient theorem attempt, Dq/vertical generator ledger, matter-descent gate, residual-owner split, no local-GR claim",
            "guardrails": "no EH import; no fitted GM; no declaring variables vertical without Dq/Omega proof; no no-derivative-by-taste; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "field_sort": OUTPUTS["field_sort"],
        "quotient_descent": OUTPUTS["quotient_descent"],
        "normal_form": OUTPUTS["normal_form"],
        "coefficient_slots": OUTPUTS["coefficient_slots"],
        "acquisition_queue": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2485_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
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
                }
            )
        )

    add("VAL2485_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2485_01_field_sorts_written",
        len(data["fields"]) >= 8 and all(row["valid_for_claim"] is False for row in data["fields"]),
        "field/sort table covers public, matter, q, auxiliary, projector, memory and boundary slots as nonclaim",
    )
    add(
        "VAL2485_02_quotient_unsigned",
        any(row["map_id"] == "QD2485_0_parent_quotient" and row["current_status"] == "CONTRACT_WRITTEN_NOT_PARENT_SIGNED" for row in data["quotient"]),
        "parent quotient map is written but unsigned",
    )
    add(
        "VAL2485_03_symmetry_unsigned",
        any(row["symmetry_id"] == "SYM2485_0_diffeomorphism" and row["current_status"] == "MISSING_PARENT_DIFF_GENERATOR" for row in data["symmetry"]),
        "diffeomorphism generator remains missing",
    )
    add(
        "VAL2485_04_derivative_grammar_guard",
        any(row["grammar_id"] == "DG2485_4_vertical_derivatives" and "RETAIN_FINITE_BRANCH" in row["normal_form_status"] for row in data["grammar"]),
        "vertical derivative bans are not claimed by taste",
    )
    add(
        "VAL2485_05_normal_form_skeleton",
        any(row["contract_id"] == "NF2485_0_parent_action_skeleton" for row in data["normal_form"]),
        "parent action skeleton row exists",
    )
    add(
        "VAL2485_06_coefficients_nonclaim",
        all(row["valid_for_claim"] is False for row in data["coefficients"]),
        "all coefficient/residual slots remain nonclaim",
    )
    add("VAL2485_07_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no gate allows Newton/local-GR/R10 claim")
    add(
        "VAL2485_08_next_target_written",
        any(row["route_id"] == "NEXT2485_0_selected" for row in data["next"]),
        "2486 field-sort/quotient target selected",
    )
    add("VAL2485_09_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2485*", "*P8_Y5_PARENT_NORMAL_FORM_2485*", "*JR2485*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2485_10_no_formalization_artifacts", not formalization_artifacts, "no 2485 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2485_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2485_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2485_OVERALL",
        overall,
        "2485 writes the parent normal-form skeleton, keeps all GR/Newton claims blocked, and selects field-sort/quotient signature next",
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
        "# 2485 Y5 R2FR Parent Normal Form Field Symmetry Derivative Grammar",
        "",
        "**Status:** the parent normal-form skeleton is now explicit, but it is not yet a derived MTS parent action. This is a scaffolding checkpoint, not a GR/Newton claim.",
        "",
        "**Main result:** the strongest route is to make MTS earn EH/GR through one parent action inventory. The skeleton is `S_parent[Phi]=int sqrt(-g)[a0+a1 R[e]+L_matter(Psi,e_obs,theta_obs)+L_aux+L_q+L_tau/memory+sum_i c_i O_i]+S_top+S_boundary`. Current evidence does not sign the field list, quotient map, symmetry generator, derivative grammar, coefficient owner, or residual zero/bound clauses, so all local-GR/Newton gates remain shut.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Parent Field/Sort Table",
        markdown_table(data["fields"], ["field_id", "symbol", "sort", "normal_form_role", "candidate_status", "missing_signature", "downstream_residual_if_unsigned", "valid_for_claim"]),
        "",
        "## Quotient And Descent Map",
        markdown_table(data["quotient"], ["map_id", "map_statement", "required_identity", "current_status", "blocker", "claim_effect", "valid_for_claim"]),
        "",
        "## Symmetry And Noether Ledger",
        markdown_table(data["symmetry"], ["symmetry_id", "generator", "required_action", "noether_output", "current_status", "missing_for_claim", "valid_for_claim"]),
        "",
        "## Derivative Grammar",
        markdown_table(data["grammar"], ["grammar_id", "operator", "slot", "normal_form_status", "reason", "required_owner", "valid_for_claim"]),
        "",
        "## Parent Normal Form Contract",
        markdown_table(data["normal_form"], ["contract_id", "formula", "interpretation", "current_status", "missing_for_claim", "valid_for_claim"]),
        "",
        "## Coefficient Slot Ledger",
        markdown_table(data["coefficients"], ["slot_id", "symbol", "owner_question", "current_status", "residual_if_missing", "next_input", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register_rows(),
        "fields": field_sort_rows(),
        "quotient": quotient_descent_rows(),
        "symmetry": symmetry_noether_rows(),
        "grammar": derivative_grammar_rows(),
        "normal_form": normal_form_rows(),
        "coefficients": coefficient_slot_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["field_sort"], data["fields"])
    write_csv(OUTPUTS["quotient_descent"], data["quotient"])
    write_csv(OUTPUTS["symmetry_noether"], data["symmetry"])
    write_csv(OUTPUTS["derivative_grammar"], data["grammar"])
    write_csv(OUTPUTS["normal_form"], data["normal_form"])
    write_csv(OUTPUTS["coefficient_slots"], data["coefficients"])
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

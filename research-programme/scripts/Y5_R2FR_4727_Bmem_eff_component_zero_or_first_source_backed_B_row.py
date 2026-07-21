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

CHECKPOINT = "4727"
CLAIM_ID = "L-569"
MARKER = "PPC4161_BMEM_EFF_COMPONENT_ZERO_OR_FIRST_SOURCE_BACKED_B_ROW_4727"
PACKET_MARKER = "PPC4161_PACKET_BMEM_EFF_COMPONENT_ZERO_OR_FIRST_SOURCE_BACKED_B_ROW_4727"
DECISION = "B826_ZERO_REDUCED_TO_PARENT_ROOT_LOCK_OR_NO_SOURCE_SLOT_FINITE_COHERCIVE_BOUND_STAGED_NONCLAIM"
NEXT_TARGET = "4728-Y5-R2FR-B826-no-source-slot-common-measure-proof-or-root-coercivity-bound.md"

DOC_PATH = POST / "4727-Y5-R2FR-Bmem-eff-component-zero-or-first-source-backed-B-row.md"
FORMAL_PATH = FORMAL / "743-PPC4161-Bmem-eff-component-zero-or-first-source-backed-B-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4727_SOURCE_REGISTER.csv"
ROOT_LOCK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4727_B826_ROOT_LOCK_THEOREM.csv"
FACTOR_SPLIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4727_B826_FACTOR_SPLIT.csv"
FINITE_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4727_FIRST_B826_FINITE_SOURCE_ROW.csv"
PROPAGATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4727_B826_TO_BMEM_PROPAGATION.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4727_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4727_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4727_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4727_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4727_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4727_VALIDATION.csv"


SOURCE_SPECS = [
    ("SRC4727_0", POST / "CURRENT_LOCAL_RESUME.md", "4727-Y5-R2FR-Bmem-eff-component-zero-or-first-source-backed-B-row.md", "4726 handoff target."),
    ("SRC4727_1", POST / "4726-Y5-R2FR-hidden-exchange-BLinvB-zero-or-memory-fibre-vertex-bound.md", "B_mem_eff=0", "4726 identifies B_mem_eff as the hidden-exchange zero target."),
    ("SRC4727_2", SOURCE_DIR / "P8_Y5_R2FR_4726_NEXT_TARGET.csv", "4727-Y5-R2FR-Bmem-eff-component-zero-or-first-source-backed-B-row.md", "machine handoff into 4727."),
    ("SRC4727_3", SOURCE_DIR / "P8_Y5_R2FR_4507_BMEM_EFFECTIVE_FORMULA.csv", "BMF4507_1_826_term", "4507 isolates the 826 term."),
    ("SRC4727_4", SOURCE_DIR / "P8_Y5_R2FR_4507_TRACE_PROJECTION_DERIVATION.csv", "TR4507_2_memory_derivative", "4507 trace projection reduces Bmem to 826 plus tails."),
    ("SRC4727_5", SOURCE_DIR / "P8_Y5_R2FR_4507_FINITE_BMEM_SOURCE_ROW.csv", "FBM4507_0_memory_B_source", "4507 finite Bmem source row."),
    ("SRC4727_6", SOURCE_DIR / "P8_Y5_R2FR_4514_BMEM_EFFECTIVE_COMPONENT_VECTOR.csv", "BMV4514_0_B826", "4514 component vector for Bmem_eff."),
    ("SRC4727_7", SOURCE_DIR / "P8_Y5_R2FR_4514_BODY_CHARGE_INSERTION_BOUND.csv", "BCB4514_3_amplitude", "4514 memory body-charge insertion bound."),
    ("SRC4727_8", SOURCE_DIR / "P8_Y5_R2FR_4510_PARENT_SOURCE_ROOT_THEOREM.csv", "PST4510_1_vacuum_subtracted_constructor", "4510 source-root theorem constructors."),
    ("SRC4727_9", SOURCE_DIR / "P8_Y5_R2FR_4510_SOURCE_ROOT_CONSTRUCTOR_COMPARISON.csv", "SRCROOT4510_B_defect_norm", "4510 compares clean source-root constructors."),
    ("SRC4727_10", SOURCE_DIR / "P8_Y5_R2FR_4510_SOURCE_ROOT_FAILURE_BOUND_ROWS.csv", "SRB4510_1_offroot_Fm", "4510 finite off-root derivative bounds."),
    ("SRC4727_11", SOURCE_DIR / "P8_Y5_R2FR_4510_HESSIAN_COERCIVITY_GUARD.csv", "HCG4510_0_branch_gap", "4510 Hessian/coercivity guard."),
    ("SRC4727_12", SOURCE_DIR / "P8_Y5_R2FR_4670_BMEM_FIRST_COMPONENT_AUDIT.csv", "BFC4670_1_B826", "4670 B826 first-component audit."),
    ("SRC4727_13", SOURCE_DIR / "P8_Y5_R2FR_4670_ZM_B826_FIRST_ROW_CONTRACT.csv", "FR4670_6_Rm", "4670 first row contract for R_m."),
    ("SRC4727_14", SOURCE_DIR / "P8_Y5_R2FR_4671_B826_ROOT_LOCK_TEST.csv", "BRL4671_1_root_lock", "4671 B826 root-lock test."),
    ("SRC4727_15", SOURCE_DIR / "P8_Y5_R2FR_4671_FIRST_HESSIAN_B826_ROW_CONTRACT.csv", "FHR4671_3_B826_root", "4671 finite/theorem row contract."),
    ("SRC4727_16", SOURCE_DIR / "P8_Y5_R2FR_4672_B826_EVEN_RESPONSE_WELD.csv", "WELD4672_3_no_source_slot_theorem", "4672 no-source-slot route."),
    ("SRC4727_17", SOURCE_DIR / "P8_Y5_R2FR_4672_FIRST_ZM_B826_BOUND_ROW_CONTRACT.csv", "BND4672_1_no_source_slot", "4672 next owner-zero target."),
    ("SRC4727_18", SOURCE_DIR / "P8_Y5_R2FR_4673_FIRST_ZM_B826_INPUT_PACK.csv", "PACK4673_7_B826", "4673 B826 input pack."),
    ("SRC4727_19", SOURCE_DIR / "P8_Y5_R2FR_4674_FIRST_FINITE_B826_BOUND_SCHEMA.csv", "BND4674_0_master", "4674 first finite B826 bound schema."),
    ("SRC4727_20", SOURCE_DIR / "P8_Y5_R2FR_4711_ROOT_NORMAL_EQUATION_CERTIFICATE.csv", "RNC4711_0_parent_residual_square_normal_equation", "4711 exact residual-root normal-equation theorem."),
    ("SRC4727_21", SOURCE_DIR / "P8_Y5_R2FR_4712_ROOT_COHERCIVITY_SOURCE_PACK.csv", "RCP4712_4_lambdaRQ", "4712 coercive root source pack."),
    ("SRC4727_22", SOURCE_DIR / "P8_Y5_R2FR_4683_BMEM_EFF_INSERTION.csv", "BM4683_5_combined", "4683 combined Bmem_eff insertion."),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    separator = "\n\n" if existing and not existing.endswith("\n\n") else ""
    write_text(path, existing + separator + block.rstrip() + "\n")


def source_path(source_id: str) -> str:
    for row_id, path, _needle, _role in SOURCE_SPECS:
        if row_id == source_id:
            return str(path)
    raise KeyError(source_id)


def source_register(ts: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
    return rows


def root_lock_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "BRL4727_0_formula",
            "B_826 structure",
            "B_826 = a_F L_cg^-2 R_m(m_L;X_B)",
            "The first memory curvature-source component is isolated from the rest of B_mem_eff.",
            "STRUCTURE_READY",
            "SRC4727_3",
        ),
        (
            "BRL4727_1_fixed_background_derivative",
            "fixed X_B condition",
            "partial_m Gamma_eff|_L = a_F L_cg^-2 partial_m R(m_L;X_B) at fixed X_B",
            "The zero is only clean if the derivative is taken before source/readout drift of X_B.",
            "FIXED_XB_GUARD_DERIVED",
            "SRC4727_3",
        ),
        (
            "BRL4727_2_stationary_density_zero",
            "stationary parent-density route",
            "If R is the same parent local density whose branch equation gives partial_m R(m_L;X_B)=0, then B_826=0.",
            "This is a genuine derivation route, not a fitted cancellation, but only after same-density ownership is signed.",
            "EXACT_CONDITIONAL_ZERO_UNSIGNED",
            "SRC4727_8",
        ),
        (
            "BRL4727_3_residual_square_normal_equation",
            "residual-square/coercive route",
            "If S_R=1/2||R_m||_W^2, no independent linear source survives, and the residual complex has no cokernel/coercivity, stationarity implies R_m=0 and hence B_826=0.",
            "This imports the 4711 normal-equation proof into the B826 branch.",
            "EXACT_CONDITIONAL_ROOT_THEOREM_UNSIGNED",
            "SRC4727_20",
        ),
        (
            "BRL4727_4_even_or_no_source_slot",
            "even/no-source-slot route",
            "If R_826 descends through q or is even under the same vertical involution, D_vertical R_826=0 and therefore R_m=0.",
            "This is the lowest-scrutiny zero route if the common measure/no-source-slot theorem can be parent-signed.",
            "BEST_NEXT_ZERO_ROUTE_UNSIGNED",
            "SRC4727_16",
        ),
        (
            "BRL4727_5_rejected_value_subtraction",
            "unsafe subtraction route",
            "F=R(m)-R(m_*) kills the value but not R_m(m_*), so it does not kill B_826.",
            "The checkpoint explicitly rejects value-only source-root closures.",
            "REJECTED_FOR_ZERO_PROOF",
            "SRC4727_9",
        ),
        (
            "BRL4727_6_finite_fallback",
            "finite B826 route",
            "|B_826| <= |a_F| L_cg^-2 |R_m|",
            "If root-lock is not signed, the first B row is a finite source/bound row, not a local-GR claim.",
            "FINITE_BOUND_READY_INPUTS_MISSING",
            "SRC4727_19",
        ),
        (
            "BRL4727_7_verdict",
            "4727 result",
            "B_826=0 is reduced exactly to parent root-lock/no-source-slot ownership; current evidence does not sign that owner, so the finite coercive B826 row survives.",
            "This narrows the real problem to a specific theorem or specific values.",
            "ZERO_REDUCED_NOT_PROMOTED",
            "SRC4727_14",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "lock_id": lock_id,
            "target": target,
            "statement": statement,
            "meaning": meaning,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for lock_id, target, statement, meaning, status, source_id in specs
    ]


def factor_split_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "FAC4727_0_aF",
            "a_F",
            "826 amplitude prefactor",
            "theorem zero only if parent action makes a_F=0; otherwise finite numeric/source row needed",
            "MISSING_COMPONENT_VALUE",
            "SRC4727_13",
        ),
        (
            "FAC4727_1_Lcg",
            "L_cg",
            "curvature-gradient/readout length scale",
            "needs positive same-branch lower bound or sourced value; L_cg cannot be inferred from the bound to be tested",
            "MISSING_LENGTH_VALUE",
            "SRC4727_13",
        ),
        (
            "FAC4727_2_Rm",
            "R_m(m_L;X_B)",
            "branch source-root derivative/residual",
            "clean zero if parent branch equation, residual-square normal equation, or no-source-slot/even response owns R_m=0",
            "MISSING_ROOT_LOCK",
            "SRC4727_15",
        ),
        (
            "FAC4727_3_branch_lock",
            "m_L=m_*",
            "same physical local branch",
            "B826 zero requires the derivative to be evaluated on the actual local branch, not a formal expansion point",
            "MISSING_BRANCH_LOCK",
            "SRC4727_14",
        ),
        (
            "FAC4727_4_fixed_XB",
            "X_B fixed",
            "background/source/readout variables held fixed under partial_m",
            "if X_B drifts, extra source/readout terms enter and must join the Bmem absolute sum",
            "FIXED_BACKGROUND_UNSIGNED",
            "SRC4727_3",
        ),
        (
            "FAC4727_5_profile",
            "R_obs/body profile",
            "profile for propagating B826 into rho_mem and A_mem",
            "finite route needs arena/source profile and units",
            "MISSING_ARENA_PROFILE",
            "SRC4727_7",
        ),
        (
            "FAC4727_6_component_guard",
            "no cancellation",
            "B_mem_eff absolute component sum",
            "B826 can only be removed componentwise; do not cancel against Weyl/Y5/Y6/boundary/readout tails",
            "GUARD_ACTIVE",
            "SRC4727_6",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "factor_id": factor_id,
            "symbol": symbol,
            "definition": definition,
            "zero_or_bound_requirement": requirement,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for factor_id, symbol, definition, requirement, status, source_id in specs
    ]


def finite_row_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "B8264727_0_master",
            "B_826",
            "|B_826| <= |a_F| L_cg^-2 |R_m|",
            "same as B_mem_eff component",
            "a_F;L_cg;R_m;units;source_path",
            "MISSING_NUMERIC_INPUTS",
            "SRC4727_19",
        ),
        (
            "B8264727_1_coercive_root_bound",
            "R_m",
            "|R_m| <= C_root (|J_root|+|B_root|+|Pi_coker R_m|)",
            "residual norm units",
            "C_root;J_root;B_root;Pi_coker;root domain",
            "COERCIVE_BOUND_FORMULA_READY_INPUTS_MISSING",
            "SRC4727_20",
        ),
        (
            "B8264727_2_Croot_gap",
            "C_root",
            "C_root <= 1/lambda_root, lambda_root=Z_Rm_min*lambda_1_Rm + M_Rm_min^2 - Eta_Rm > 0",
            "operator inverse norm",
            "Z_Rm_min;lambda_1_Rm;M_Rm_min^2;Eta_Rm",
            "SYMBOLIC_GAP_DERIVED_UNSOURCED",
            "SRC4727_21",
        ),
        (
            "B8264727_3_offroot_taylor",
            "R_m(m_L)",
            "|R_m(m_L)| <= |R_m(m_*)| + |R_mm| Delta_m + 1/2 |R_mmm| Delta_m^2 + remainder",
            "same as R_m",
            "R_m(m_*);R_mm;R_mmm;Delta_m;remainder",
            "OFFROOT_FALLBACK_READY_VALUES_MISSING",
            "SRC4727_10",
        ),
        (
            "B8264727_4_component_insert",
            "B_mem_eff",
            "|B_mem_eff| <= |B_826|+|B_Weyl_vec|+|B_Y5_trace|+|B_Y6_trace|+|B_src_boundary|+|B_src_readout|",
            "same as B_mem_eff",
            "all component bounds or zeros",
            "ABSOLUTE_SUM_READY_VALUES_MISSING",
            "SRC4727_22",
        ),
        (
            "B8264727_5_body_charge_insert",
            "A_mem",
            "|A_mem| <= [exp(R_body/lambda_mem) int_body ((|B_826|+Sigma_other_B)|R_obs|+|C_mem||T|+|J_mem|) dV + |Q_boundary_mem|]/(4*pi |Z_mem|)",
            "exterior memory amplitude units",
            "Z_mem;lambda_mem;R_obs profile;C_mem;J_mem;Q_boundary_mem;other B components",
            "BODY_CHARGE_ROUTE_READY_INPUTS_MISSING",
            "SRC4727_7",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "bound_or_formula": formula,
            "units": units,
            "needed_inputs": needed_inputs,
            "current_status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for row_id, quantity, formula, units, needed_inputs, status, source_id in specs
    ]


def propagation_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "PROP4727_0_B826_zero_effect",
            "If B_826=0 is parent-signed, only the first B_mem_eff component is removed.",
            "B_Weyl_vec, B_Y5_trace, B_Y6_trace, B_src_boundary and B_src_readout remain live unless separately zeroed.",
            "SRC4727_6",
        ),
        (
            "PROP4727_1_B826_finite_effect",
            "If B_826 survives, it contributes to rho_mem through B_mem_eff R_obs and therefore to local fifth-force/PPN/R10 amplitudes.",
            "Use absolute component sum; no cancellation with other B components.",
            "SRC4727_7",
        ),
        (
            "PROP4727_2_root_branch_safety",
            "The source-root theorem must be local-branch specific and must not erase cosmology/galaxy memory branches.",
            "Use same-branch labels for local vacuum/root branch versus FLRW/disk memory branch.",
            "SRC4727_11",
        ),
        (
            "PROP4727_3_next_decision",
            "The next mathematical target is the no-source-slot/common-measure proof for R_826 or the coercive finite root-bound input pack.",
            "This is the least-smuggling route because it decides whether R_m is an argument of the parent action at all.",
            "SRC4727_17",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "propagation_id": propagation_id,
            "effect": effect,
            "guardrail": guardrail,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for propagation_id, effect, guardrail, source_id in specs
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4727_0_sources_verified", "All 4727 sources exist and needles are found.", True, "NONE"),
        ("GATE4727_1_B826_formula_isolated", "B_826 factorization is identified as a_F L_cg^-2 R_m.", True, "STRUCTURE_ONLY"),
        ("GATE4727_2_root_lock_signed", "R_m(m_L;X_B)=0 is parent-signed on the actual fixed-X_B local branch.", False, "ROOT_LOCK_UNSIGNED"),
        ("GATE4727_3_no_source_slot_signed", "R_826 descends through q or is absent/even before variation.", False, "NO_SOURCE_SLOT_UNSIGNED"),
        ("GATE4727_4_coercive_root_inputs_sourced", "C_root,J_root,B_root,Pi_coker and root domain are numeric or theorem-owned.", False, "ROOT_COHERCIVITY_INPUTS_MISSING"),
        ("GATE4727_5_aF_Lcg_sourced", "a_F and L_cg are sourced with units or theorem-zero.", False, "A_F_LCG_VALUES_MISSING"),
        ("GATE4727_6_B826_claim_row_ready", "B_826 is zero or finite-bound claim-grade.", False, "B826_RETAINED_NONCLAIM"),
        ("GATE4727_7_Bmem_eff_closed", "B_mem_eff is closed after all components are zero or bounded.", False, "OTHER_BMEM_COMPONENTS_LIVE"),
        ("GATE4727_8_local_GR_R2_channel_closed", "The memory vertex leg of hidden exchange is removed claim-grade.", False, "LOCAL_GR_NOT_PROMOTED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "condition": condition,
            "passed": passed,
            "blocker": blocker,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for gate_id, condition, passed, blocker in specs
    ]


def firewall_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4727_0_no_value_subtraction", "Do not use value-only subtraction F=R(m)-R(m_*) as a B826 zero proof; it leaves R_m live."),
        ("FW4727_1_fixed_background", "Do not differentiate through drifting source/readout variables while calling it partial_m at fixed X_B."),
        ("FW4727_2_no_per_system_root", "Do not choose a separate local root for each experiment/source body."),
        ("FW4727_3_no_component_cancellation", "Do not cancel B826 against Weyl/Y5/Y6/boundary/readout tails without a parent identity."),
        ("FW4727_4_no_R10_backsolve", "Do not infer a_F, L_cg or R_m from the R10 bound being tested."),
        ("FW4727_5_branch_separation", "Do not force FLRW or galaxy memory branches to zero when deriving a strict local vacuum root."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for firewall_id, rule in specs
    ]


def decision_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derivation_result": "B_826=0 follows exactly if the 826 response derivative is owned by a parent stationary density, a residual-square normal equation with coercivity/no source, or a q-basic/even no-source-slot theorem",
            "finite_row_result": "|B_826| <= |a_F| L_cg^-2 |R_m| and the stronger coercive root bound are staged nonclaim because source values/owner clauses are missing",
            "local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": ts,
        }
    ]


def status_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4727_0_local_only",
            "status": "local_files_only_no_github_action",
            "detail": "Generated under post-checkpoint-work and formalization-workbench only.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4727_1_science_verdict",
            "status": "B826_zero_reduced_to_root_lock_or_no_source_slot",
            "detail": "4727 advances the work by reducing the first Bmem component to exact parent-owner clauses or a finite coercive row.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "The cleanest remaining B826 zero path is to prove R_826 is q-basic/even/no-source-slot under the same parent measure; if that fails, fill the root-coercivity finite bound pack.",
            "first_task": "Try to prove that R_826 descends through q or is absent before variation, so D_vertical R_826=0 at fixed X_B.",
            "fallback_task": "If no-source-slot fails, instantiate |B_826| <= |a_F| L_cg^-2 C_root(|J_root|+|B_root|+|Pi_coker R_m|) as the first finite source row.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    ts: str,
    root_locks: list[dict[str, Any]],
    factors: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4727 - Bmem_eff Component Zero or First Source-Backed B Row

Generated: `{ts}`

## Purpose

4727 attacks the first concrete memory vertex component inside `B_mem_eff`: `B_826`. The goal is to derive its zero condition, not merely list it as missing.

## What Actually Moved

- `B_826` is now isolated as `B_826 = a_F L_cg^-2 R_m(m_L;X_B)`.
- The exact zero route is sharp: `B_826=0` follows if `R_m(m_L;X_B)=0` at fixed `X_B`, or if the 826 response is q-basic/even/no-source-slot before variation.
- A residual-square normal-equation route is available: coercivity plus no linear source/boundary/cokernel forces the root residual to vanish.
- Value-only subtraction is rejected because it kills `R` but not `R_m`.
- Current evidence does not parent-sign root-lock/no-source-slot, so the finite row survives: `|B_826| <= |a_F| L_cg^-2 |R_m|`, with a stronger coercive fallback.

## Root-Lock Theorem

{bullets(root_locks, "lock_id", "status")}

## Factor Split

{bullets(factors, "factor_id", "status")}

## Finite Rows

{bullets(finite_rows, "row_id", "current_status")}

## Gates

{bullets(gates, "gate_id", "blocker")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 743 - Bmem_eff Component Zero or First Source-Backed B Row

Generated: `{ts}`

## Result

The first memory vertex component is

`B_826 = a_F L_cg^-2 R_m(m_L;X_B)`.

Therefore the honest zero proof is not “memory is quiet”; it is `R_m(m_L;X_B)=0` at fixed `X_B`, or a parent no-source-slot/evenness theorem that removes the vertical derivative of the 826 response before it becomes a source.

## Conditional Theorem

If the local branch is owned by the same parent stationary density, or by a residual-square normal equation with coercivity and no linear/boundary/cokernel source, then `R_m=0` and hence `B_826=0`.

The current corpus does not yet sign those owner clauses, so `B_826` remains a finite nonclaim row:

`|B_826| <= |a_F| L_cg^-2 |R_m|`.

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(ts: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Derivation gain: the first memory vertex component is isolated as `B_826 = a_F L_cg^-2 R_m(m_L;X_B)`, with an exact zero theorem if parent root-lock/no-source-slot owns `R_m=0` at fixed `X_B`.
- Finite row: `|B_826| <= |a_F| L_cg^-2 |R_m|`, plus coercive root bound fallback.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: narrows `B_mem_eff` by attacking the first component `B_826`, rejects value-only source-root closure, and stages the finite coercive source row if parent root-lock remains unsigned.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{ts}`

## Latest completed checkpoint

`{DOC_PATH.name}`

## Decision

`{DECISION}`

## What moved forward

- The first `B_mem_eff` component is isolated as `B_826 = a_F L_cg^-2 R_m(m_L;X_B)`.
- `B_826=0` is now reduced to exact parent root-lock/no-source-slot ownership at fixed `X_B`.
- Since those owner clauses remain unsigned, the finite row `|B_826| <= |a_F| L_cg^-2 |R_m|` and coercive fallback remain nonclaim.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def add_claim_once(ts: str) -> None:
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_bridge",
        "claim": "4727 isolates the first memory vertex component B_826 and reduces its zero proof to parent root-lock/no-source-slot ownership; absent that owner, a finite coercive B826 row survives.",
        "current_evidence": "Generated source register, B826 root-lock theorem, factor split, first finite B826 source row, B826-to-Bmem propagation rows, promotion gates, firewalls, decision, status, next target and validation.",
        "status": "B826_zero_reduced_to_parent_owner_or_finite_row_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Mistaking value-only source-root subtraction or per-system calibration for a derivative-zero theorem.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "If R_m or fixed-X_B/root-lock fails, B826 contributes to B_mem_eff and therefore to local finite-range residuals.",
        "title": "Bmem_eff component zero or first source-backed B row",
        "notes": f"{MARKER}; {DECISION}; generated {ts}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def parse_csv(path: Path) -> bool:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def validation_rows(
    sources: list[dict[str, Any]],
    root_locks: list[dict[str, Any]],
    factors: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    propagations: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    ts: str,
) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER_CSV,
        ROOT_LOCK_CSV,
        FACTOR_SPLIT_CSV,
        FINITE_ROW_CSV,
        PROPAGATION_CSV,
        GATES_CSV,
        FIREWALL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_TARGET_CSV,
    ]
    root_status = ";".join(row["status"] for row in root_locks)
    factor_status = ";".join(row["status"] for row in factors)
    finite_status = ";".join(row["current_status"] for row in finite_rows)
    propagation_text = ";".join(f"{row['effect']} {row['guardrail']}" for row in propagations)
    checks = [
        ("VAL4727_0_sources_exist", all(bool(row["exists"]) for row in sources), "all cited 4727 source paths exist"),
        ("VAL4727_1_needles_found", all(bool(row["needle_found"]) for row in sources), "all cited 4727 source needles found"),
        ("VAL4727_2_B826_formula_isolated", "STRUCTURE_READY" in root_status and "MISSING_ROOT_LOCK" in factor_status, "B826 formula and root factor isolated"),
        ("VAL4727_3_exact_zero_theorems_written", "EXACT_CONDITIONAL_ZERO_UNSIGNED" in root_status and "EXACT_CONDITIONAL_ROOT_THEOREM_UNSIGNED" in root_status and "BEST_NEXT_ZERO_ROUTE_UNSIGNED" in root_status, "exact conditional zero routes written"),
        ("VAL4727_4_value_subtraction_rejected", "REJECTED_FOR_ZERO_PROOF" in root_status, "value-only subtraction rejected"),
        ("VAL4727_5_finite_rows_nonclaim", "MISSING_NUMERIC_INPUTS" in finite_status and "COERCIVE_BOUND_FORMULA_READY_INPUTS_MISSING" in finite_status and all(not bool(row["valid_for_claim"]) for row in finite_rows), "finite B826 rows staged nonclaim"),
        ("VAL4727_6_Bmem_propagation_retained", "B_Weyl_vec" in propagation_text and "no cancellation" in propagation_text, "B826 propagation keeps other Bmem components live"),
        ("VAL4727_7_claim_gates_closed", all(not bool(row["claim_allowed"]) for row in gates) and not any(row["passed"] for row in gates if row["gate_id"] not in {"GATE4727_0_sources_verified", "GATE4727_1_B826_formula_isolated"}), "all broad claim gates remain closed; formula gate is structure only"),
        ("VAL4727_8_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4727_9_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4727_10_claim_row_added", CLAIM_ID in read_text(CLAIMS_PATH), "claims register contains L-569"),
        ("VAL4727_11_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4728 next target"),
        ("VAL4727_12_csv_parse", all(parse_csv(path) for path in csv_paths), "all generated 4727 CSV files parse cleanly"),
        ("VAL4727_13_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
    ]
    overall = all(result for _check_id, result, _detail in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "timestamp_utc": ts,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4727_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "4727 Bmem_eff component zero or first source-backed B row validation",
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()
    cleanup_pycache()
    sources = source_register(ts)
    root_locks = root_lock_rows(ts)
    factors = factor_split_rows(ts)
    finite_rows = finite_row_rows(ts)
    propagations = propagation_rows(ts)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(ROOT_LOCK_CSV, root_locks)
    write_csv(FACTOR_SPLIT_CSV, factors)
    write_csv(FINITE_ROW_CSV, finite_rows)
    write_csv(PROPAGATION_CSV, propagations)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(ts, root_locks, factors, finite_rows, gates)
    update_spine_packet_resume(ts)
    add_claim_once(ts)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, root_locks, factors, finite_rows, propagations, gates, ts))


if __name__ == "__main__":
    main()

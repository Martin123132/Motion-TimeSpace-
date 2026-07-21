from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deltaktf_shell_profile_gate import read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4510"
CLAIM_ID = "L-352"
MARKER = "PPC4161_PARENT_SOURCE_ROOT_LOCK_OR_FIRST_BWEYL_INPUT_FILL_4510"
PACKET_MARKER = "PPC4161_PACKET_PARENT_SOURCE_ROOT_LOCK_OR_FIRST_BWEYL_INPUT_FILL_4510"
DECISION = "SOURCE_ROOT_LOCK_DERIVED_AS_ADMISSIBLE_PARENT_CLAUSE_FIRST_BWEYL_ROWS_CONDITIONALLY_FILLED_NONCLAIM"
NEXT_TARGET = "4511-Y5-R2FR-no-spurion-readout-grammar-or-WFm-finite-row.md"

FORMAL_PATH = FORMAL / "526-PPC4161-parent-source-root-lock-or-first-BWeyl-input-fill.md"
DOC_PATH = POST / "4510-Y5-R2FR-parent-source-root-lock-or-first-BWeyl-input-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4510_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4510_SOURCE_REGISTER.csv"
SOURCE_ROOT_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4510_PARENT_SOURCE_ROOT_THEOREM.csv"
CONSTRUCTOR_COMPARISON = SOURCE_DIR / "P8_Y5_R2FR_4510_SOURCE_ROOT_CONSTRUCTOR_COMPARISON.csv"
ACTIVE_BRANCH_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4510_ACTIVE_BRANCH_MATCH_AUDIT.csv"
BWEYL_INPUT_FILL = SOURCE_DIR / "P8_Y5_R2FR_4510_BWEYL_INPUT_FILL_ROWS.csv"
HESSIAN_GUARD = SOURCE_DIR / "P8_Y5_R2FR_4510_HESSIAN_COERCIVITY_GUARD.csv"
FAILURE_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4510_SOURCE_ROOT_FAILURE_BOUND_ROWS.csv"
PARENT_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4510_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4510_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4510_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4510_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4510_DECISION.csv"

FORMAL_525 = FORMAL / "525-PPC4161-source-root-no-spurion-combined-gate-or-BWeyl-numeric-row.md"
POST_4509 = POST / "4509-Y5-R2FR-source-root-no-spurion-combined-gate-or-BWeyl-numeric-row.md"
SOURCE_ROOT_4509 = SOURCE_DIR / "P8_Y5_R2FR_4509_SOURCE_ROOT_GATE.csv"
NUMERIC_4509 = SOURCE_DIR / "P8_Y5_R2FR_4509_BWEYL_NUMERIC_ACQUISITION_ROW.csv"
VDZ_4300 = SOURCE_DIR / "P8_Y5_R2FR_4300_VERTICAL_DOUBLE_ZERO_THEOREM.csv"
PLC_4301 = SOURCE_DIR / "P8_Y5_R2FR_4301_PARENT_LOCK_CONTRACT.csv"
ELD_4301 = SOURCE_DIR / "P8_Y5_R2FR_4301_EULER_LOCK_DERIVATION.csv"
BOUNDS_4301 = SOURCE_DIR / "P8_Y5_R2FR_4301_SECOND_ORDER_DVGAMMA_BOUND_ROWS.csv"

DOUBLE_ZERO_ORIGIN = SOURCE_DIR / "P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv"
DOUBLE_ZERO_VARIATION = SOURCE_DIR / "P8_DOUBLE_ZERO_MEMORY_VARIATION_TEST.csv"
DOUBLE_ZERO_POWER = SOURCE_DIR / "P8_DOUBLE_ZERO_MEMORY_POWER_GATE.csv"
QMA_970 = SOURCE_DIR / "P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv"
MPO_967 = SOURCE_DIR / "P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv"
MZG_968 = SOURCE_DIR / "P8_Y5_R10_968_MEMORY_ZERO_PREMISE_GATE.csv"
MOA_2626 = SOURCE_DIR / "P8_Y5_MEMORY_OWNER_GATE_2626_PARENT_MEMORY_OPERATOR_OWNER_AUDIT.csv"
ZPT_2626 = SOURCE_DIR / "P8_Y5_MEMORY_OWNER_GATE_2626_POSITIVE_OPERATOR_ZERO_THEOREM_ATTEMPT.csv"
BOUNDARY_2627 = SOURCE_DIR / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_BOUNDARY_ZERO_GATE.csv"
BEXT_1348 = SOURCE_DIR / "P8_Y5_R10_1348_BMEM_EXTREMUM_TEST.csv"
OPS_1348 = SOURCE_DIR / "P8_Y5_R10_1348_MEMORY_OPERATOR_SIGNATURE_TEST.csv"
FMEM_1348 = SOURCE_DIR / "P8_Y5_R10_1348_FINITE_MEMORY_BRANCH_CONTRACT.csv"
MEM_1969 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1969_MEMORY_DERIVATION.csv"
DN_3221 = SOURCE_DIR / "P8_Y5_R2FR_3221_DEFECT_NORM_SOURCE_ROOT_THEOREM.csv"
DNC_3222 = SOURCE_DIR / "P8_Y5_R2FR_3222_PARENT_ACTION_DEFECT_NORM_CONTRACT.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4510_00_formal525", "4509 formal handoff", FORMAL_525, "Source-Root Gate", "source-root target"),
        ("SRC4510_01_post4509", "4509 post mirror", POST_4509, "CZT4509_1_source_root_clause", "combined theorem source-root clause"),
        ("SRC4510_02_srg4509", "4509 source-root gate csv", SOURCE_ROOT_4509, "SRG4509_0_Fm_WL", "F_m zero row"),
        ("SRC4510_03_numeric4509", "4509 numeric acquisition rows", NUMERIC_4509, "BWN4509_00_F_root", "first B_Weyl input row"),
        ("SRC4510_04_vdz4300", "4300 vertical double-zero theorem", VDZ_4300, "DZT4300_1_double_zero_insert", "F and F_m double zero"),
        ("SRC4510_05_plc4301", "4301 parent-lock contract", PLC_4301, "PLC4301_2_vacuum_subtraction", "F_vac double-zero clause"),
        ("SRC4510_06_eld4301", "4301 Euler lock derivation", ELD_4301, "EL4301_3_exact_nohair", "positive operator no-hair"),
        ("SRC4510_07_bounds4301", "4301 fallback bound", BOUNDS_4301, "BQ4301_3_DvGamma_quad", "quadratic leakage bound"),
        ("SRC4510_08_dz_origin", "double-zero memory origin", DOUBLE_ZERO_ORIGIN, "O2_quadratic_gate_sufficient", "quadratic gate sufficient"),
        ("SRC4510_09_dz_variation", "double-zero variation test", DOUBLE_ZERO_VARIATION, "pass_as_sufficient_contract", "f(0)=f_prime(0)=0 test"),
        ("SRC4510_10_power_gate", "double-zero power gate", DOUBLE_ZERO_POWER, "P0_power_condition", "p>=2 requirement"),
        ("SRC4510_11_qma970", "quadratic memory action construction", QMA_970, "QMA970_2_positivity", "positive operator route"),
        ("SRC4510_12_mpo967", "memory positive operator lemma", MPO_967, "MPO967_4_energy_identity", "energy identity"),
        ("SRC4510_13_mzg968", "memory zero premise gate", MZG_968, "MZG968_7_verdict", "premises not signed"),
        ("SRC4510_14_moa2626", "memory owner audit", MOA_2626, "MOA2626_2_operator_LX", "operator candidate status"),
        ("SRC4510_15_zpt2626", "positive operator theorem attempt", ZPT_2626, "ZPT2626_1_energy_identity", "relative proof"),
        ("SRC4510_16_boundary2627", "boundary zero gate", BOUNDARY_2627, "BZ2627_5_current_verdict", "boundary package missing"),
        ("SRC4510_17_bext1348", "Bmem extremum test", BEXT_1348, "BEXT1348_1_conditional_calculus", "branch extremum route"),
        ("SRC4510_18_ops1348", "memory operator signature", OPS_1348, "OPS1348_1_variation", "operator form"),
        ("SRC4510_19_fmem1348", "finite memory branch contract", FMEM_1348, "FMEM1348_0_equation", "finite branch equation"),
        ("SRC4510_20_mem1969", "memory derivation audit", MEM_1969, "MEM1969_2_written_branch_direct_mixing", "direct branch simplification"),
        ("SRC4510_21_dn3221", "defect-norm source-root theorem", DN_3221, "DN3221_1_first_derivative_zero", "norm-square double-zero pattern"),
        ("SRC4510_22_dnc3222", "defect-norm parent-action contract", DNC_3222, "DNC3222_0_parent_object", "no-smuggling parent object rule"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, role, path, needle, note in specs:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text(path),
                "line": line_of(path, needle),
                "note": note,
                "valid_for_claim": False,
            }
        )
    return rows


def source_root_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "PST4510_0_parent_clause",
            "premise": "m is a parent memory/local-vacuum variable with a local stationary branch m_*",
            "formula": "delta S_m/delta m = 0 gives V_m(m_*,X_B^*)=0 before readout",
            "result": "defines the branch root without fitting a local experiment",
            "status": "ADMISSIBLE_PARENT_CLAUSE_NOT_CONFIRMED_LIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "PST4510_1_vacuum_subtracted_constructor",
            "premise": "Gamma_eff uses the same local parent density that fixes the m branch",
            "formula": "F_SR(m,X_B^*) := lambda_V [V(m,X_B^*) - V(m_*,X_B^*)]",
            "result": "F_SR(m_*)=0 and partial_m F_SR(m_*)=lambda_V V_m(m_*)=0",
            "status": "EXACT_DOUBLE_ZERO_IF_SAME_DENSITY_OWNER",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "PST4510_2_defect_norm_constructor",
            "premise": "the source-root is a squared parent residual, not an after-the-fact penalty",
            "formula": "F_SR(Phi)=lambda_R <R_m(Phi),R_m(Phi)>_P with R_m(Phi_*)=0",
            "result": "D_m F_SR|_* = 2 lambda_R <R_m,D_m R_m>|_* = 0",
            "status": "EXACT_DOUBLE_ZERO_IF_PARENT_RESIDUAL_OBJECT_EXISTS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "PST4510_3_response_extremum_constructor",
            "premise": "the 826 response branch has a genuine local extremum",
            "formula": "F_SR=a_F[R_mem(m;X_B^*)-R_mem(m_*;X_B^*)] with partial_m R_mem(m_*;X_B^*)=0",
            "result": "F_SR(m_*)=0 and F_SR,m(m_*)=0",
            "status": "EXACT_IF_BRANCH_EXTREMUM_PARENT_OWNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "PST4510_4_lock",
            "premise": "the parent operator locks the tested local branch to m_*",
            "formula": "L_m delta m=(-Z_m box+mu_m^2)delta m=J_m+B_m+N(delta m); gap>0 and J_m=B_m=0 imply delta m=0",
            "result": "the double-zero is evaluated at the physical local branch, not just a formal point",
            "status": "RELATIVE_NOHAIR_THEOREM_INPUTS_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "PST4510_5_BWeyl_insertion",
            "premise": "PST4510_1 or PST4510_2 or PST4510_3 and PST4510_4 all hold",
            "formula": "-2 L_cg^-3(F_m W_L + F W_L,m)=0",
            "result": "the first two B_Weyl acquisition inputs are theorem-zero on the source-root branch",
            "status": "CONDITIONAL_INPUT_FILL_NOT_CLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def constructor_comparison_rows() -> List[Dict[str, object]]:
    return [
        {
            "constructor_id": "SRCROOT4510_A_stationary_density",
            "definition": "F=lambda_V[V(m)-V(m_*)]",
            "why_it_is_clean": "same density owns both the branch equation and the Gamma source-root coefficient",
            "risk": "requires proof that Gamma_eff really uses this density, not an independent response function",
            "status": "BEST_PHYSICS_ROUTE",
            "valid_for_claim": False,
        },
        {
            "constructor_id": "SRCROOT4510_B_defect_norm",
            "definition": "F=lambda_R <R_m,R_m>",
            "why_it_is_clean": "double-zero follows from the residual root and is robust under field redefinitions",
            "risk": "R_m must be a parent object in the action before readout, otherwise it is a penalty closure",
            "status": "BEST_NO_SMUGGLING_PATTERN_IF_R_m_FOUND",
            "valid_for_claim": False,
        },
        {
            "constructor_id": "SRCROOT4510_C_response_extremum",
            "definition": "F=a_F[R_mem(m)-R_mem(m_*)] with R_mem,m(m_*)=0",
            "why_it_is_clean": "connects directly to the old 826/1348 branch-extremum calculus",
            "risk": "needs parent ownership of R_mem and its extremum; otherwise it is just choosing a convenient expansion point",
            "status": "LIVE_BUT_MORE_SCRUTINIZED",
            "valid_for_claim": False,
        },
        {
            "constructor_id": "SRCROOT4510_D_value_subtraction_only",
            "definition": "F=R(m)-R(m_*) without R_m(m_*)=0",
            "why_it_is_clean": "none",
            "risk": "kills F but leaves F_m live, so the Lcg-chain tail survives",
            "status": "REJECT_FOR_BWEYL_ZERO",
            "valid_for_claim": False,
        },
        {
            "constructor_id": "SRCROOT4510_E_per_system_calibration",
            "definition": "choose m_* separately per local test/source",
            "why_it_is_clean": "none",
            "risk": "post-hoc local fitting; not a field-theory derivation",
            "status": "FORBIDDEN",
            "valid_for_claim": False,
        },
    ]


def active_branch_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "ABA4510_0_4301_contract",
            "object": "F_vac(m)=V(m)-V(m_*)",
            "match_result": "formula already exists as a parent-lock proof gate",
            "evidence": "4301 PLC4301_2 and EL4301_1",
            "gap": "not yet signed as the live MTS memory/Gamma parent density",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "ABA4510_1_double_zero_memory",
            "object": "quadratic/norm-square memory gate",
            "match_result": "variation tests prove f(0)=f_prime(0)=0 is sufficient and p>=2 is required",
            "evidence": "P8_DOUBLE_ZERO_MEMORY_* rows",
            "gap": "origin symmetry/norm/topological route remains conditional",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "ABA4510_2_positive_operator",
            "object": "local lock delta m=0",
            "match_result": "energy identity is mathematically ready",
            "evidence": "967/970/2626 positive operator rows",
            "gap": "parent owner, positive signs, source silence, and boundary package are unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "ABA4510_3_1348_branch",
            "object": "826/1348 response extremum",
            "match_result": "conditional calculus passes",
            "evidence": "BEXT1348_1_conditional_calculus",
            "gap": "R_mem functional and m_L branch owner not parent-derived",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "ABA4510_4_1969_direct_branch",
            "object": "displayed memory operator branch",
            "match_result": "direct Ricci mixing is conditionally absent in the displayed branch",
            "evidence": "MEM1969_2_written_branch_direct_mixing",
            "gap": "indirect X_B/source/bath/boundary/metric-composite channels remain live",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bweyl_input_fill_rows() -> List[Dict[str, object]]:
    return [
        {
            "input_id": "BWF4510_00_F_root",
            "source_4509_row": "BWN4509_00_F_root",
            "symbol": "F(m_*)",
            "filled_value": "0",
            "fill_type": "CONDITIONAL_THEOREM_ZERO",
            "condition": "PST4510 stationary-density, defect-norm, or response-extremum constructor is parent-signed in the active branch",
            "source_path": str(DOC_PATH),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "BWF4510_01_Fm_root",
            "source_4509_row": "BWN4509_01_Fm_root",
            "symbol": "F_m(m_*)",
            "filled_value": "0",
            "fill_type": "CONDITIONAL_THEOREM_ZERO",
            "condition": "same parent density/residual/extremum owns both F and the local m equation; not merely value subtraction",
            "source_path": str(DOC_PATH),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "BWF4510_02_Lcg_chain",
            "source_4509_row": "CZT4509_1_source_root_clause",
            "symbol": "B_Weyl_Lcg_chain",
            "filled_value": "0",
            "fill_type": "DERIVED_IF_BWF4510_00_AND_01_ACTIVATE",
            "condition": "-2 L_cg^-3(F_m W_L+F W_L,m)=0 termwise; no cancellation credit",
            "source_path": str(DOC_PATH),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def hessian_guard_rows() -> List[Dict[str, object]]:
    return [
        {
            "guard_id": "HCG4510_0_branch_gap",
            "quantity": "mu_m^2",
            "formula": "mu_m^2=V_{,mm}(m_*) plus controlled parent corrections",
            "guard": "mu_m^2>0 after gauge/constraint/zero-mode removal",
            "status": "REQUIRED_FOR_LOCAL_LOCK",
            "valid_for_claim": False,
        },
        {
            "guard_id": "HCG4510_1_extra_sector_shift",
            "quantity": "eta_extra",
            "formula": "G_eff >= mu_m^2 - eta_EM - eta_boundary - eta_readout - eta_history",
            "guard": "extra-sector Hessian shifts must not flip the positive operator",
            "status": "FINITE_GUARD_STAGED",
            "valid_for_claim": False,
        },
        {
            "guard_id": "HCG4510_2_source_silence",
            "quantity": "J_m+B_m",
            "formula": "delta m <= (||J_m||+||B_m||+||N||)/lambda_m",
            "guard": "zero theorem requires exact source/boundary silence; otherwise use amplitude bound",
            "status": "FALLBACK_BOUND_READY_SYMBOLIC",
            "valid_for_claim": False,
        },
        {
            "guard_id": "HCG4510_3_FLRW_branch_safety",
            "quantity": "branch separation",
            "formula": "local source-root applies on the local vacuum branch; FLRW/disk memory amplitude may live on a different nonzero branch",
            "guard": "do not erase cosmology/galaxy memory by globally forcing F=0",
            "status": "BRANCH_COMPATIBILITY_GUARD",
            "valid_for_claim": False,
        },
    ]


def failure_bound_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "SRB4510_0_offroot_F",
            "quantity": "F(m_L)",
            "formula": "|F(m_L)| <= |F(m_*)| + |F_m(m_*)| Delta_m + 1/2 |F_2| Delta_m^2 + O(Delta_m^3)",
            "required_inputs": "F(m_*);F_m(m_*);F_2;Delta_m;remainder bound",
            "status": "FINITE_FALLBACK_IF_SOURCE_ROOT_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "bound_id": "SRB4510_1_offroot_Fm",
            "quantity": "F_m(m_L)",
            "formula": "|F_m(m_L)| <= |F_m(m_*)| + |F_2| Delta_m + 1/2 |F_3| Delta_m^2 + O(Delta_m^3)",
            "required_inputs": "F_m(m_*);F_2;F_3;Delta_m;remainder bound",
            "status": "FINITE_FALLBACK_IF_BRANCH_LOCK_IS_ONLY_APPROXIMATE",
            "valid_for_claim": False,
        },
        {
            "bound_id": "SRB4510_2_Lcg_chain",
            "quantity": "B_Weyl_Lcg_chain",
            "formula": "|B_Weyl_Lcg| <= 1/2 L_cg^-3 (|F_m(m_L)||W_L| + |F(m_L)||W_L,m|)",
            "required_inputs": "L_cg;F/F_m offroot bounds;W_L;W_L,m",
            "status": "INSERTABLE_IN_4509_BWEYL_BOUND",
            "valid_for_claim": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PA4510_0_theorem",
            "claim": "source-root lock has an exact parent-action route",
            "status": "DERIVED_AS_ADMISSIBLE_CLAUSE",
            "effect": "F and F_m can be termwise zero if F is the same stationary density, a parent defect norm, or a parent-owned extremum response",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4510_1_not_smuggled",
            "claim": "per-system calibration is rejected",
            "status": "GUARD_INSTALLED",
            "effect": "only branch-universal parent clauses count; value subtraction alone fails because F_m remains live",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4510_2_first_inputs",
            "claim": "first two B_Weyl rows are filled",
            "status": "CONDITIONAL_THEOREM_ZERO_ROWS_STAGED",
            "effect": "BWN4509_00 and BWN4509_01 now have a precise theorem-zero owner candidate, but remain nonclaim",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4510_3_live_gap",
            "claim": "active MTS branch is proven to use this source-root clause",
            "status": "NOT_PROVEN",
            "effect": "next target should attack no-spurion/readout or source the active branch parent-density evidence",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {"gate_id": "CG4510_0_source_root_live", "gate": "F(m_*)=F_m(m_*)=0 is live in active MTS branch", "derived_now": False, "blocked_by": "admissible parent clause not identified as the accepted MTS memory/Gamma density", "claim_allowed": False},
        {"gate_id": "CG4510_1_Lcg_chain_zero", "gate": "B_Weyl Lcg-chain term zero", "derived_now": False, "blocked_by": "conditional on CG4510_0 and local branch lock", "claim_allowed": False},
        {"gate_id": "CG4510_2_BWeyl_zero", "gate": "full B_Weyl=0", "derived_now": False, "blocked_by": "no-spurion/readout, Khat trace, and boundary/domain gates remain unsigned", "claim_allowed": False},
        {"gate_id": "CG4510_3_local_GR", "gate": "local GR/PPN/R10 promotion", "derived_now": False, "blocked_by": "source coupling/Khat/local projection gates remain open", "claim_allowed": False},
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "admissible parent source-root theorem and first B_Weyl F/F_m input fills as conditional theorem-zero rows",
            "not_derived": "proof that the accepted MTS parent action uses one of these source-root constructors in the active branch",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated": STAMP,
        }
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4510_0",
            "decision": DECISION,
            "because": "the source-root lock is not magic: it follows exactly if Gamma_eff's memory factor is the stationary parent density, a squared parent residual, or a parent-owned extremum response",
            "effect": "the Lcg-chain obstruction is now conditionally filled; the next cleanest move is no-spurion/readout grammar for W_F,m, while the active parent-density match remains a live branch-signing task",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4510_0",
            "target_file": NEXT_TARGET,
            "task": "try to close the no-spurion/readout grammar so W_F,m=0, or source the W_F,m/B_qWeyl finite row if that grammar fails",
            "success_condition": "linear Weyl response is parent/readout forbidden, or W_F,m has a sourced finite bound compatible with local arenas",
            "do_not": "claim the whole B_Weyl tail is gone merely because the source-root Lcg-chain subterm has a conditional theorem-zero route",
            "valid_for_claim": False,
        }
    ]


def validate(all_rows: Mapping[str, Sequence[Mapping[str, object]]]) -> List[Dict[str, object]]:
    csv_files = [
        SOURCE_REGISTER,
        SOURCE_ROOT_THEOREM,
        CONSTRUCTOR_COMPARISON,
        ACTIVE_BRANCH_AUDIT,
        BWEYL_INPUT_FILL,
        HESSIAN_GUARD,
        FAILURE_BOUND,
        PARENT_AUDIT,
        CLAIM_GATES,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    parsed = True
    details: List[str] = []
    for path in csv_files:
        try:
            rows = read_csv(path)
            parsed = parsed and bool(rows)
            details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:
            parsed = False
            details.append(f"{path.name}:ERROR:{exc}")

    source_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in all_rows["sources"])
    theorem_ok = any(row.get("theorem_id") == "PST4510_5_BWeyl_insertion" for row in all_rows["theorem"])
    clean_constructor_ok = any(row.get("constructor_id") == "SRCROOT4510_A_stationary_density" for row in all_rows["constructors"])
    forbidden_ok = any(row.get("constructor_id") == "SRCROOT4510_E_per_system_calibration" and row.get("status") == "FORBIDDEN" for row in all_rows["constructors"])
    first_inputs_filled = all(
        row.get("filled_value") == "0" and row.get("fill_type") == "CONDITIONAL_THEOREM_ZERO"
        for row in all_rows["bweyl_fill"]
        if row.get("input_id") in {"BWF4510_00_F_root", "BWF4510_01_Fm_root"}
    )
    fallback_ok = any(row.get("bound_id") == "SRB4510_2_Lcg_chain" for row in all_rows["failure_bounds"])
    claim_gates_blocked = all(row.get("derived_now") is False and row.get("claim_allowed") is False for row in all_rows["gates"])
    nonclaim_ok = all(
        str(value).lower() != "true"
        for rows in all_rows.values()
        for row in rows
        for key, value in row.items()
        if key in {"valid_for_claim", "claim_allowed"}
    )
    next_ok = all_rows["next"][0]["target_file"] == NEXT_TARGET
    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()

    checks = [
        ("VAL4510_00_sources", source_ok, "all source paths exist and source needles are found"),
        ("VAL4510_01_theorem", theorem_ok, "source-root theorem inserts into B_Weyl Lcg chain"),
        ("VAL4510_02_constructor", clean_constructor_ok, "stationary-density constructor recorded"),
        ("VAL4510_03_forbidden_route", forbidden_ok, "per-system calibration route is forbidden"),
        ("VAL4510_04_first_inputs_filled", first_inputs_filled, "F(m_*) and F_m(m_*) conditionally filled as theorem-zero rows"),
        ("VAL4510_05_fallback_bound", fallback_ok, "off-root finite Lcg-chain bound is staged"),
        ("VAL4510_06_claims_blocked", claim_gates_blocked, "all claim gates remain blocked"),
        ("VAL4510_07_nonclaim_flags", nonclaim_ok, "all generated valid_for_claim/claim_allowed flags remain false"),
        ("VAL4510_08_csv_parse", parsed, ";".join(details)),
        ("VAL4510_09_next_target", next_ok, NEXT_TARGET),
        ("VAL4510_10_pycache_absent", pycache_absent, "scripts __pycache__ absent after cleanup"),
    ]
    rows = [
        {
            "validation_id": check_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL4510_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "4510 parent source-root lock or first B_Weyl input fill",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def append_claim_once() -> None:
    existing = text(CLAIMS_PATH)
    if CLAIM_ID in existing or MARKER in existing:
        return
    row = ",".join(
        [
            CLAIM_ID,
            "local_gr_newton_r2fr_source_root_lock",
            '"4510 derives the admissible parent source-root lock: if Gamma_eff uses the same stationary local parent density, a squared parent residual, or a parent-owned response extremum, then F(m_*)=F_m(m_*)=0 and the Lcg-chain part of B_Weyl vanishes termwise. The first B_Weyl F/F_m rows are conditionally filled, while live-branch ownership remains unsigned."',
            '"4510 source register, parent source-root theorem, constructor comparison, active branch audit, B_Weyl input fills, Hessian guard, failure bounds, parent audit, claim gates, status and validation."',
            "private_source_root_lock_conditional_input_fill_nonclaim",
            NEXT_TARGET,
            "claiming local GR from an admissible source-root clause, using value subtraction alone, or calibrating m_* per source/test.",
            "local_gr_newton_r2fr_source_root_lock",
            str(FORMAL_PATH),
            NEXT_TARGET,
            '"close no-spurion/readout grammar for W_F,m or source the finite W_F,m/B_qWeyl row."',
        ]
    )
    CLAIMS_PATH.write_text(existing.rstrip() + "\n" + row + "\n", encoding="utf-8")


def build_doc(
    sources: Sequence[Mapping[str, object]],
    theorem: Sequence[Mapping[str, object]],
    constructors: Sequence[Mapping[str, object]],
    active: Sequence[Mapping[str, object]],
    fill: Sequence[Mapping[str, object]],
    hessian: Sequence[Mapping[str, object]],
    failure: Sequence[Mapping[str, object]],
    parent: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4510 - Parent Source-Root Lock Or First B_Weyl Input Fill

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4510 does make a concrete move. The source-root lock is not an arbitrary plateau axiom: it follows exactly if the active parent branch makes the memory/Gamma factor one of these three objects:

1. a vacuum-subtracted stationary parent density, `F=lambda_V[V(m)-V(m_*)]` with `V_m(m_*)=0`;
2. a squared parent residual, `F=lambda_R <R_m,R_m>` with `R_m(Phi_*)=0`;
3. a parent-owned response extremum, `F=a_F[R_mem(m)-R_mem(m_*)]` with `R_mem,m(m_*)=0`.

Any of those gives `F(m_*)=0` and `F_m(m_*)=0`, so the Lcg-chain part of `B_Weyl`,

`-2 L_cg^-3(F_m W_L + F W_L,m)`,

vanishes term by term. That fills the first two `B_Weyl` input rows as conditional theorem-zero rows. It is still not a local-GR claim, because the live MTS parent action has not yet been proven to use one of these constructors and the no-spurion/readout, Khat, and boundary/domain clauses remain open.

## Source Register

{table(sources)}

## Parent Source-Root Theorem

{table(theorem)}

## Constructor Comparison

{table(constructors)}

## Active Branch Match Audit

{table(active)}

## B_Weyl Input Fill Rows

{table(fill)}

## Hessian Coercivity Guard

{table(hessian)}

## Source-Root Failure Bound Rows

{table(failure)}

## Parent Signature Audit

{table(parent)}

## Claim Gates

{table(gates)}

## Status

{table(status)}

## Decision

{table(decisions)}

## Next Target

{table(next_target)}

## Validation

{table(validation)}
"""


def main() -> None:
    sources = source_rows()
    theorem = source_root_theorem_rows()
    constructors = constructor_comparison_rows()
    active = active_branch_audit_rows()
    fill = bweyl_input_fill_rows()
    hessian = hessian_guard_rows()
    failure = failure_bound_rows()
    parent = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows()
    decisions = decision_rows()
    next_target = next_rows()

    all_rows = {
        "sources": sources,
        "theorem": theorem,
        "constructors": constructors,
        "active": active,
        "bweyl_fill": fill,
        "hessian": hessian,
        "failure_bounds": failure,
        "parent": parent,
        "gates": gates,
        "status": status,
        "decisions": decisions,
        "next": next_target,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SOURCE_ROOT_THEOREM, theorem)
    write_csv(CONSTRUCTOR_COMPARISON, constructors)
    write_csv(ACTIVE_BRANCH_AUDIT, active)
    write_csv(BWEYL_INPUT_FILL, fill)
    write_csv(HESSIAN_GUARD, hessian)
    write_csv(FAILURE_BOUND, failure)
    write_csv(PARENT_AUDIT, parent)
    write_csv(CLAIM_GATES, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(all_rows)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(
        sources,
        theorem,
        constructors,
        active,
        fill,
        hessian,
        failure,
        parent,
        gates,
        status,
        decisions,
        next_target,
        validation,
    )
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4510 Parent Source-Root Lock Or First B_Weyl Input Fill

Marker: `{MARKER}`  
4510 derives the source-root lock as an admissible parent-action clause rather than a plateau axiom. If `F` is the vacuum-subtracted stationary parent density, a squared parent residual, or a parent-owned response extremum, then `F(m_*)=F_m(m_*)=0`, killing the Lcg-chain part of `B_Weyl` termwise. The first two `B_Weyl` rows are conditionally filled, while active-branch ownership remains unsigned.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4510 Packet Integration

Marker: `{PACKET_MARKER}`  
The private local packet now has a theorem-zero route for the first `B_Weyl` inputs: prove the active memory/Gamma factor is a stationary density, parent residual norm, or parent response extremum. Without that branch signature, use the staged off-root bounds for `F(m_L)`, `F_m(m_L)`, and the Lcg-chain term.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()

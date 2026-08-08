from __future__ import annotations

import csv
import io
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

CHECKPOINT = "4514"
CLAIM_ID = "L-356"
MARKER = "PPC4161_BWEYL_VECTOR_INSERTION_INTO_BMEM_EFF_OR_BODY_CHARGE_BOUND_4514"
PACKET_MARKER = "PPC4161_PACKET_BWEYL_VECTOR_INSERTION_INTO_BMEM_EFF_OR_BODY_CHARGE_BOUND_4514"
DECISION = "BWEYL_VECTOR_INSERTED_INTO_BMEM_EFF_BODY_CHARGE_BOUND_STAGED_NONCLAIM"
NEXT_TARGET = "4515-Y5-R2FR-Y5-Y6-source-trace-tail-or-Cmem-Jmem-source-coupling-vector.md"

FORMAL_PATH = FORMAL / "530-PPC4161-BWeyl-vector-insertion-into-Bmem-eff-or-body-charge-bound.md"
DOC_PATH = POST / "4514-Y5-R2FR-BWeyl-vector-insertion-into-Bmem-eff-or-body-charge-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4514_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4514_SOURCE_REGISTER.csv"
INSERTION_LAW = SOURCE_DIR / "P8_Y5_R2FR_4514_BMEM_BWEYL_INSERTION_LAW.csv"
BMEM_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4514_BMEM_EFFECTIVE_COMPONENT_VECTOR.csv"
BODY_CHARGE_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4514_BODY_CHARGE_INSERTION_BOUND.csv"
SOURCE_TAIL_LEDGER = SOURCE_DIR / "P8_Y5_R2FR_4514_REMAINING_SOURCE_TAIL_LEDGER.csv"
PARENT_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4514_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4514_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4514_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4514_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4514_DECISION.csv"

FORMAL_529 = FORMAL / "529-PPC4161-boundary-domain-readout-tail-or-final-BWeyl-vector.md"
POST_4513 = POST / "4513-Y5-R2FR-boundary-domain-readout-tail-or-final-BWeyl-vector.md"
VECTOR_4513 = SOURCE_DIR / "P8_Y5_R2FR_4513_FINAL_BWEYL_VECTOR.csv"
TAIL_BOUND_4513 = SOURCE_DIR / "P8_Y5_R2FR_4513_TAIL_FINITE_BOUND_ROWS.csv"
FORMULA_4507 = SOURCE_DIR / "P8_Y5_R2FR_4507_BMEM_EFFECTIVE_FORMULA.csv"
FINITE_4507 = SOURCE_DIR / "P8_Y5_R2FR_4507_FINITE_BMEM_SOURCE_ROW.csv"
TRACE_4507 = SOURCE_DIR / "P8_Y5_R2FR_4507_TRACE_PROJECTION_DERIVATION.csv"
BWEYL_4508 = SOURCE_DIR / "P8_Y5_R2FR_4508_BWEYL_FINITE_BOUND_ROW.csv"
BODY_4506 = SOURCE_DIR / "P8_Y5_R2FR_4506_BODY_CHARGE_INPUT_ROW.csv"
OP_4506 = SOURCE_DIR / "P8_Y5_R2FR_4506_MEMORY_OPERATOR_SIGNATURE.csv"
CLAIMS_4506 = SOURCE_DIR / "P8_Y5_R2FR_4506_CLAIM_GATES.csv"
SFE_1354 = SOURCE_DIR / "P8_Y5_R10_1354_SOURCE_FUNCTIONAL_EVENNESS_ATTEMPT.csv"
JZ_1354 = SOURCE_DIR / "P8_Y5_R10_1354_Y5Y6_JZ_COEFFICIENT_FILL.csv"
DEC_1354 = SOURCE_DIR / "P8_Y5_R10_1354_DECISION_LEDGER.csv"
SN_AUDIT = SOURCE_DIR / "P8_SOURCE_NORMALIZATION_CHANNEL_AUDIT.csv"
SN_FILL = SOURCE_DIR / "P8_SOURCE_NORMALIZATION_COEFFICIENT_FILL.csv"
SN_STACK = SOURCE_DIR / "P8_source_normalized_Newton_branch_STACK.csv"
SRC_CURRENT = SOURCE_DIR / "P8_source_current_Ward_universality_CONTRACT.csv"
SRC_OWNER = SOURCE_DIR / "P8_source_owner_parent_action_terms_CONTRACT.csv"

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


def csv_line(values: Sequence[object]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer)
    writer.writerow(values)
    return buffer.getvalue().strip("\r\n")


def falseish(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "none", ""}


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4514_00_formal529", "4513 formal handoff", FORMAL_529, "Final B_Weyl Vector", "complete B_Weyl vector"),
        ("SRC4514_01_post4513", "4513 post handoff", POST_4513, "NT4513_0", "declares Bmem insertion target"),
        ("SRC4514_02_vector4513", "4513 final B_Weyl vector", VECTOR_4513, "BWFV4513_6_combined", "combined B_Weyl vector row"),
        ("SRC4514_03_tail4513", "4513 tail finite bound", TAIL_BOUND_4513, "TFB4513_0_tail_total", "tail finite bound"),
        ("SRC4514_04_formula4507", "4507 Bmem formula", FORMULA_4507, "BMF4507_0_effective", "B_mem_eff formula"),
        ("SRC4514_05_finite4507", "4507 finite Bmem row", FINITE_4507, "FBM4507_0_memory_B_source", "finite Bmem source row"),
        ("SRC4514_06_nocancel4507", "4507 no-cancellation guard", FINITE_4507, "FBM4507_1_no_cancellation_guard", "no cancellation guard"),
        ("SRC4514_07_trace4507", "4507 trace derivation", TRACE_4507, "TR4507_3_zero_theorem", "Bmem zero theorem"),
        ("SRC4514_08_bweyl4508", "4508 B_Weyl finite bound", BWEYL_4508, "BW4508_0_total", "older B_Weyl finite row"),
        ("SRC4514_09_body4506", "4506 body-charge row", BODY_4506, "BCIN4506_0_memory_density", "memory body-charge schema"),
        ("SRC4514_10_zero4506", "4506 zero switch", BODY_4506, "BCIN4506_2_zero_switch", "body-charge zero switch"),
        ("SRC4514_11_op4506", "4506 memory operator", OP_4506, "MOP4506_2_nohair_guard", "positive operator no-hair guard"),
        ("SRC4514_12_gate4506", "4506 claim gates", CLAIMS_4506, "CG4506_1_memory_nohair", "memory no-hair blocked"),
        ("SRC4514_13_sfe1354", "1354 source-functional evenness", SFE_1354, "SFE1354_6_verdict", "source evenness not proved"),
        ("SRC4514_14_jz1354", "1354 Y5/Y6 coefficient fill", JZ_1354, "JZ1354_Y5_0_radial_Meff_hair", "Y5 live coefficient rows"),
        ("SRC4514_15_jz1354_y6", "1354 Y6 coefficient fill", JZ_1354, "JZ1354_Y6_3_metric_response_tail", "Y6 live coefficient rows"),
        ("SRC4514_16_dec1354", "1354 decision", DEC_1354, "DEC1354_1_Y5_priority", "Y5 priority"),
        ("SRC4514_17_sn_audit", "source normalization audit", SN_AUDIT, "C1_domain_projector", "source-normalization channels"),
        ("SRC4514_18_sn_fill", "source normalization fill", SN_FILL, "F0_c_domain_source_normalization_operator", "source coefficient fill route"),
        ("SRC4514_19_sn_stack", "source-normalized Newton stack", SN_STACK, "SN6_zero_mu_extra_and_source_residuals", "Newton source stack residuals"),
        ("SRC4514_20_source_current", "source current Ward contract", SRC_CURRENT, "SC4_no_nonHilbert_source_current", "non-Hilbert source current"),
        ("SRC4514_21_source_owner", "source owner parent action terms", SRC_OWNER, "A9_memory_kernel_local_silence", "memory source owner route"),
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


def insertion_law_rows() -> List[Dict[str, object]]:
    return [
        {
            "law_id": "BIL4514_0_decomposition",
            "object": "B_mem_eff",
            "statement": "Insert the completed 4513 B_Weyl vector as the Weyl/metric-response component of the 4507 effective memory curvature-source coefficient.",
            "formula": "B_mem_eff = B_826 + B_Weyl_vec + B_Y5_trace + B_Y6_trace + B_src_boundary + B_src_readout",
            "result": "B_Weyl no longer floats as an uninserted tail; it is now a named coefficient in rho_mem",
            "status": "DERIVED_INSERTION_LAW",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "law_id": "BIL4514_1_BWeyl_vector",
            "object": "B_Weyl_vec",
            "statement": "Use the complete 4513 no-cancellation vector for B_Weyl rather than the older partial 4508 bound.",
            "formula": "|B_Weyl_vec| <= 1/4 sum_abs(Lcg_chain, W_Fm, R_K_trace,m, W_boundary,m, W_domain,m, W_readout,m)",
            "result": "source-root, no-spurion, Khat-trace and BDR tail rows enter as one component family",
            "status": "COMPLETE_VECTOR_IMPORTED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "law_id": "BIL4514_2_no_double_count",
            "object": "B_src_boundary/B_src_readout",
            "statement": "The boundary/readout entries inside B_Weyl are metric-response trace tails; the separate 4507 B_src_boundary/B_src_readout slots are source-functional/source-normalization tails and are retained unless a parent identity maps them together.",
            "formula": "B_src_boundary/readout != W_boundary/readout contribution unless parent equivalence is signed",
            "result": "prevents both double-count erasure and fake cancellation",
            "status": "NO_DOUBLE_COUNT_GUARD_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "law_id": "BIL4514_3_zero_theorem",
            "object": "B_mem_eff zero",
            "statement": "B_mem_eff vanishes termwise if B_826=0, the full B_Weyl vector is zero, and the Y5/Y6/source boundary/readout trace tails are zero in the same parent branch.",
            "formula": "B_826=B_Weyl_vec=B_Y5_trace=B_Y6_trace=B_src_boundary=B_src_readout=0 => B_mem_eff=0",
            "result": "this is the same-branch theorem condition needed before memory no-hair can fire",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "law_id": "BIL4514_4_finite_bound",
            "object": "finite B_mem_eff",
            "statement": "If any component remains unsigned, B_mem_eff is bounded by an absolute sum with no cancellation credit.",
            "formula": "|B_mem_eff| <= |B_826|+|B_Weyl_vec|+|B_Y5_trace|+|B_Y6_trace|+|B_src_boundary|+|B_src_readout|",
            "result": "finite body-charge scoring can proceed once each component has theorem-zero or source-backed values",
            "status": "FINITE_NO_CANCELLATION_BOUND_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bmem_vector_rows() -> List[Dict[str, object]]:
    return [
        {
            "component_id": "BMV4514_0_B826",
            "component": "B_826 = a_F L_cg^-2 R_m(m_L;X_B)",
            "source": "4507 BMF4507_1",
            "zero_condition": "branch extremum/parent source-root signs R_m=0 with X_B fixed and m_L parent-owned",
            "finite_fallback": "source a_F, L_cg, R_m and body/source profile",
            "current_status": "CONDITIONAL_ZERO_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "component_id": "BMV4514_1_BWeyl_vec",
            "component": "B_Weyl_vec",
            "source": "4513 final B_Weyl vector",
            "zero_condition": "all six B_Weyl vector components zero in same branch",
            "finite_fallback": "1/4 absolute component sum from 4513",
            "current_status": "COMPLETE_VECTOR_STAGED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "component_id": "BMV4514_2_Y5_trace",
            "component": "B_Y5_trace",
            "source": "1354 Y5 source-normalization rows",
            "zero_condition": "measured-GM/source-normalization is quotient/source pullback and exchange-even",
            "finite_fallback": "eight Y5 J_Z coefficient rows",
            "current_status": "LIVE_HIGHEST_PRIORITY_SOURCE_TAIL",
            "valid_for_claim": False,
        },
        {
            "component_id": "BMV4514_3_Y6_trace",
            "component": "B_Y6_trace",
            "source": "1354 Y6 extra-stress rows",
            "zero_condition": "extra stress is topological/invisible/exchange-even or metric-response matched",
            "finite_fallback": "four Y6 J_Z coefficient rows",
            "current_status": "LIVE_EXTRA_STRESS_TAIL",
            "valid_for_claim": False,
        },
        {
            "component_id": "BMV4514_4_source_boundary",
            "component": "B_src_boundary",
            "source": "source-normalization/boundary rows",
            "zero_condition": "source-functional boundary/reference shift has no linear memory response",
            "finite_fallback": "boundary source-normalization coefficient row",
            "current_status": "LIVE_UNLESS_PARENT_IDENTITY_MAPS_TO_BWEYL_BOUNDARY",
            "valid_for_claim": False,
        },
        {
            "component_id": "BMV4514_5_source_readout",
            "component": "B_src_readout",
            "source": "source-normalization/readout rows",
            "zero_condition": "readout/source calibration is pure postprocessing or fixed source pullback",
            "finite_fallback": "readout/calibration source-normalization coefficient row",
            "current_status": "LIVE_UNLESS_PARENT_IDENTITY_MAPS_TO_BWEYL_READOUT",
            "valid_for_claim": False,
        },
        {
            "component_id": "BMV4514_6_combined",
            "component": "B_mem_eff",
            "source": "4514 insertion law",
            "zero_condition": "all components BMV4514_0 through BMV4514_5 zero in same parent branch",
            "finite_fallback": "absolute sum inserted into memory body-charge amplitude",
            "current_status": "BODY_CHARGE_READY_STRUCTURE_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def body_charge_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "BCB4514_0_density",
            "quantity": "rho_mem",
            "formula": "rho_mem = B_mem_eff R_obs + C_mem T + J_mem",
            "required_inputs": "B_mem_eff vector; R_obs profile; C_mem; T profile; J_mem; units; source paths",
            "current_status": "STRUCTURE_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "BCB4514_1_density_abs",
            "quantity": "|rho_mem|",
            "formula": "|rho_mem| <= |B_mem_eff||R_obs| + |C_mem||T| + |J_mem|",
            "required_inputs": "component absolute bounds and no-cancellation policy",
            "current_status": "NO_CANCELLATION_BOUND_DERIVED",
            "valid_for_claim": False,
        },
        {
            "bound_id": "BCB4514_2_body_charge",
            "quantity": "Q_mem0",
            "formula": "Q_mem0=4*pi int_0^R dr r^2 rho_mem(r) sinh(r/lambda_mem)/(r/lambda_mem)+Q_boundary_mem",
            "required_inputs": "lambda_mem=sqrt(Z_mem/M2_mem); body profile; Q_boundary_mem",
            "current_status": "IMPORTED_FROM_4506_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "BCB4514_3_amplitude",
            "quantity": "A_mem",
            "formula": "|A_mem| <= [exp(R_body/lambda_mem) int_body (|B_mem_eff||R_obs|+|C_mem||T|+|J_mem|) dV + |Q_boundary_mem|]/(4*pi |Z_mem|)",
            "required_inputs": "Z_mem; M2_mem; lambda_mem; R_body; R_obs/T/J profiles; Q_boundary_mem; screening",
            "current_status": "FINITE_BODY_CHARGE_BOUND_DERIVED_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "BCB4514_4_nohair",
            "quantity": "delta_m local silence",
            "formula": "positive L_mem plus B_mem_eff=C_mem=J_mem=Q_boundary_mem=0 => delta_m=0 and A_mem=0",
            "required_inputs": "positive Z_mem/M2_mem; zero-mode removal; all source components zero in same branch",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_LIVE_SIGNED",
            "valid_for_claim": False,
        },
        {
            "bound_id": "BCB4514_5_arena",
            "quantity": "E_mem[arena]",
            "formula": "E_mem[arena] <= tau_mem_arena |A_mem| + source-normalization transfer terms",
            "required_inputs": "tau_R10; tau_PPN; tau_clock; tau_orbital; same-frame normalization",
            "current_status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
        },
    ]


def source_tail_rows() -> List[Dict[str, object]]:
    return [
        {
            "tail_id": "STL4514_0_Y5_priority",
            "tail": "Y5 measured-GM/source-normalization",
            "why_live": "1354 rejects source-functional evenness and marks Y5 as highest-priority coupling target",
            "zero_route": "quotient/source pullback plus fixed calibrated mass-flux projector and no derivative/source hair",
            "finite_route": "eight Y5 J_Z rows from 1354",
            "next_action": "derive Y5 pullback/evenness or convert rows into source-backed finite inputs",
            "valid_for_claim": False,
        },
        {
            "tail_id": "STL4514_1_Y6_extra_stress",
            "tail": "Y6 extra stress",
            "why_live": "extra stress can spoil Khat/Ward/local-GR even if Gamma/F branch is double-zero",
            "zero_route": "topological invisibility, EH metric-response match, or exchange-even extra stress",
            "finite_route": "four Y6 J_Z rows from 1354",
            "next_action": "route Y6 through R11/nonEH coefficient vector or prove metric-response invisibility",
            "valid_for_claim": False,
        },
        {
            "tail_id": "STL4514_2_Cmem",
            "tail": "C_mem matter trace coupling",
            "why_live": "4506 says matter-blind/product-functor descent is conditional, not parent-signed",
            "zero_route": "S_matter depends only on q(Phi), Psi, theta and m is vertical to q in same frame",
            "finite_route": "C_mem*T source profile in BCB4514",
            "next_action": "derive matter-functor/source-label forgetting or source C_mem",
            "valid_for_claim": False,
        },
        {
            "tail_id": "STL4514_3_Jmem",
            "tail": "J_mem direct/source current",
            "why_live": "memory no-hair requires J_mem=0 in addition to B_mem_eff=0",
            "zero_route": "source-current Ward universality plus no non-Hilbert source current and memory kernel silence",
            "finite_route": "J_mem source profile in BCB4514",
            "next_action": "derive source-current owner/no-retained-source constraint or source J_mem",
            "valid_for_claim": False,
        },
        {
            "tail_id": "STL4514_4_Qboundary_mem",
            "tail": "Q_boundary_mem",
            "why_live": "positive operator no-hair still fails if boundary charge/flux remains",
            "zero_route": "fixed no-flux/topological boundary class with zero linked local flux",
            "finite_route": "Q_boundary_mem in Q_mem0 and A_mem bound",
            "next_action": "reuse 4513 boundary theorem as candidate, but source-normalization boundary charge still needs same-branch signing",
            "valid_for_claim": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PA4514_0_insertion",
            "claim": "B_Weyl vector is inserted into B_mem_eff",
            "status": "DERIVED",
            "effect": "Weyl work now feeds the body-charge route instead of remaining a separate audit",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4514_1_body_charge",
            "claim": "memory body-charge bound is written with B_mem_eff vector",
            "status": "DERIVED_NONCLAIM_BOUND",
            "effect": "future numeric/source rows can be scored through Q_mem/A_mem",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4514_2_source_tails",
            "claim": "Y5/Y6/source tails are zero",
            "status": "NOT_PROVEN",
            "effect": "next derivation must hit source-normalization/source coupling, not another B_Weyl split",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4514_3_memory_nohair",
            "claim": "memory branch is locally silent",
            "status": "NOT_CLAIMED",
            "effect": "requires B_mem_eff=C_mem=J_mem=Q_boundary_mem=0 plus positive operator",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4514_4_local_GR",
            "claim": "local GR/Newton/R10/PPN branch passes",
            "status": "BLOCKED_NONCLAIM",
            "effect": "same-frame source normalization, arena transfer and finite/source-backed coefficients remain required",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4514_0_Bmem_eff_zero",
            "gate": "B_mem_eff=0 live in active branch",
            "derived_now": False,
            "blocked_by": "B_Weyl vector plus Y5/Y6/source trace tails are not same-branch signed",
            "claim_allowed": False,
        },
        {
            "gate_id": "CG4514_1_body_charge_bound",
            "gate": "finite memory body-charge row score-ready",
            "derived_now": False,
            "blocked_by": "Z_mem, M2_mem, profiles, C_mem, J_mem, Q_boundary_mem and source paths missing",
            "claim_allowed": False,
        },
        {
            "gate_id": "CG4514_2_memory_nohair",
            "gate": "positive operator no-hair makes delta_m=0",
            "derived_now": False,
            "blocked_by": "source and boundary zero conditions not parent-signed",
            "claim_allowed": False,
        },
        {
            "gate_id": "CG4514_3_local_GR",
            "gate": "local GR/Newton/R10/PPN promotion",
            "derived_now": False,
            "blocked_by": "source coupling, Y5/Y6, C/J/boundary, and arena transfer gates remain open",
            "claim_allowed": False,
        },
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "B_Weyl vector insertion into B_mem_eff and memory body-charge amplitude bound",
            "not_derived": "Y5/Y6 source trace tails, C_mem/J_mem/Q_boundary_mem zeros or numeric source-backed values",
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
            "decision_id": "DEC4514_0",
            "decision": DECISION,
            "because": "4513 completed B_Weyl as a vector; the correct next move is to put it into B_mem_eff and the memory body-charge law",
            "effect": "the remaining live work is source-normalization/source-coupling tails, not another Weyl or boundary audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4514_0",
            "target_file": NEXT_TARGET,
            "task": "derive or finite-bound Y5/Y6 source trace tails and C_mem/J_mem source couplings in the B_mem_eff body-charge row",
            "success_condition": "B_mem_eff source-tail vector has theorem-zero conditions or source-backed finite rows ready for the A_mem bound",
            "do_not": "loop back to B_Weyl decomposition or claim memory no-hair without C_mem/J_mem/Q_boundary_mem and positive-operator gates",
            "valid_for_claim": False,
        }
    ]


def all_generated_csvs() -> List[Path]:
    return [
        SOURCE_REGISTER,
        INSERTION_LAW,
        BMEM_VECTOR,
        BODY_CHARGE_BOUND,
        SOURCE_TAIL_LEDGER,
        PARENT_AUDIT,
        CLAIM_GATES,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]


def validate(all_rows: Mapping[str, Sequence[Mapping[str, object]]]) -> List[Dict[str, object]]:
    parsed = True
    details: List[str] = []
    for path in all_generated_csvs():
        try:
            rows = read_csv(path)
            parsed = parsed and bool(rows)
            details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:
            parsed = False
            details.append(f"{path.name}:ERROR:{exc}")

    source_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in all_rows["sources"])
    insertion_ok = any(row.get("law_id") == "BIL4514_0_decomposition" for row in all_rows["law"])
    vector_ok = any(row.get("component_id") == "BMV4514_6_combined" for row in all_rows["vector"])
    body_ok = any(row.get("bound_id") == "BCB4514_3_amplitude" for row in all_rows["body"])
    source_tail_ok = any(row.get("tail_id") == "STL4514_0_Y5_priority" for row in all_rows["source_tail"])
    gates_blocked = all(falseish(row.get("claim_allowed")) for row in all_rows["gates"])
    flags_false = True
    for rows in all_rows.values():
        for row in rows:
            if "valid_for_claim" in row and not falseish(row["valid_for_claim"]):
                flags_false = False
            if "claim_allowed" in row and not falseish(row["claim_allowed"]):
                flags_false = False
    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()

    checks = [
        ("VAL4514_00_sources", source_ok, "all source paths exist and source needles are found"),
        ("VAL4514_01_insertion_law", insertion_ok, "B_Weyl insertion law exists"),
        ("VAL4514_02_component_vector", vector_ok, "B_mem_eff component vector includes combined row"),
        ("VAL4514_03_body_bound", body_ok, "memory body-charge amplitude bound exists"),
        ("VAL4514_04_source_tail", source_tail_ok, "Y5 source-normalization next tail is recorded"),
        ("VAL4514_05_claims_blocked", gates_blocked, "all claim gates remain blocked"),
        ("VAL4514_06_nonclaim_flags", flags_false, "all generated valid_for_claim/claim_allowed flags remain false"),
        ("VAL4514_07_csv_parse", parsed, ";".join(details)),
        ("VAL4514_08_next_target", all_rows["next"][0]["target_file"] == NEXT_TARGET, NEXT_TARGET),
        ("VAL4514_09_pycache_absent", pycache_absent, "scripts __pycache__ absent after cleanup"),
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
            "validation_id": "VAL4514_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "4514 B_Weyl vector insertion into B_mem_eff or body-charge bound",
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
    row = csv_line(
        [
            CLAIM_ID,
            "local_gr_newton_r2fr_BWeyl_Bmem_body_charge",
            "4514 inserts the completed B_Weyl vector into B_mem_eff and then into the memory body-charge law. The effective coefficient is B_mem_eff = B_826 + B_Weyl_vec + B_Y5_trace + B_Y6_trace + B_src_boundary + B_src_readout, with a no-double-count guard separating metric-response B_Weyl boundary/readout tails from source-functional tails. The finite A_mem bound is derived, but Y5/Y6 source tails, C_mem/J_mem/Q_boundary_mem, positive operator values and arena projections remain unsigned.",
            "4514 source register, insertion law, Bmem component vector, body-charge bound, source-tail ledger, parent audit, claim gates, status and validation.",
            "private_BWeyl_inserted_Bmem_body_charge_bound_nonclaim",
            NEXT_TARGET,
            "claiming memory no-hair/local GR from B_Weyl work alone, double-counting boundary/readout tails, or absorbing source-normalization into fitted G.",
            "local_gr_newton_r2fr_BWeyl_Bmem_body_charge",
            str(FORMAL_PATH),
            NEXT_TARGET,
            "derive or finite-bound Y5/Y6 source trace tails and C_mem/J_mem source couplings.",
        ]
    )
    CLAIMS_PATH.write_text(existing.rstrip() + "\n" + row + "\n", encoding="utf-8")


def build_doc(
    sources: Sequence[Mapping[str, object]],
    law: Sequence[Mapping[str, object]],
    vector: Sequence[Mapping[str, object]],
    body: Sequence[Mapping[str, object]],
    source_tail: Sequence[Mapping[str, object]],
    parent: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4514 - B_Weyl Vector Insertion Into B_mem_eff Or Body-Charge Bound

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4514 moves the work forward from the completed `B_Weyl` vector into the actual memory source channel.

The insertion law is:

`B_mem_eff = B_826 + B_Weyl_vec + B_Y5_trace + B_Y6_trace + B_src_boundary + B_src_readout`.

Here `B_Weyl_vec` is the complete 4513 vector. The separate `B_src_boundary` and `B_src_readout` slots are **not** silently erased: they are source-functional/source-normalization tails from 4507/1354, while the boundary/readout entries inside `B_Weyl_vec` are metric-response trace tails. They can only be identified if a parent identity signs that equivalence.

The body-charge insertion is now:

`rho_mem = B_mem_eff R_obs + C_mem T + J_mem`,

and the finite amplitude envelope is:

`|A_mem| <= [exp(R_body/lambda_mem) int_body (|B_mem_eff||R_obs|+|C_mem||T|+|J_mem|) dV + |Q_boundary_mem|]/(4*pi |Z_mem|)`.

So the next bottleneck is not Weyl anymore. It is source-normalization/source coupling: `Y5`, `Y6`, `C_mem`, `J_mem`, `Q_boundary_mem`, plus `Z_mem/M2_mem` and arena transfer rows.

## Source Register

{table(sources)}

## B_mem / B_Weyl Insertion Law

{table(law)}

## B_mem Effective Component Vector

{table(vector)}

## Body-Charge Insertion Bound

{table(body)}

## Remaining Source Tail Ledger

{table(source_tail)}

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
    law = insertion_law_rows()
    vector = bmem_vector_rows()
    body = body_charge_rows()
    source_tail = source_tail_rows()
    parent = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows()
    decisions = decision_rows()
    next_target = next_rows()

    all_rows = {
        "sources": sources,
        "law": law,
        "vector": vector,
        "body": body,
        "source_tail": source_tail,
        "parent": parent,
        "gates": gates,
        "status": status,
        "decisions": decisions,
        "next": next_target,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(INSERTION_LAW, law)
    write_csv(BMEM_VECTOR, vector)
    write_csv(BODY_CHARGE_BOUND, body)
    write_csv(SOURCE_TAIL_LEDGER, source_tail)
    write_csv(PARENT_AUDIT, parent)
    write_csv(CLAIM_GATES, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(all_rows)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, law, vector, body, source_tail, parent, gates, status, decisions, next_target, validation)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4514 B_Weyl Vector Insertion Into B_mem_eff Or Body-Charge Bound

Marker: `{MARKER}`  
4514 inserts the completed `B_Weyl` vector into `B_mem_eff` and then into the memory body-charge equation. The effective source coefficient is `B_mem_eff=B_826+B_Weyl_vec+B_Y5_trace+B_Y6_trace+B_src_boundary+B_src_readout`; `rho_mem=B_mem_eff R_obs+C_mem T+J_mem`. A no-double-count guard separates metric-response boundary/readout tails inside `B_Weyl_vec` from source-functional boundary/readout tails. The finite `A_mem` envelope is derived, but Y5/Y6 source tails, `C_mem`, `J_mem`, `Q_boundary_mem`, operator values and arena projections remain nonclaim.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4514 Packet Integration

Marker: `{PACKET_MARKER}`  
The private packet now routes the full `B_Weyl` vector into the memory body-charge gate. The next packet step is source coupling: derive or bound Y5/Y6 source trace tails plus `C_mem`, `J_mem` and `Q_boundary_mem`, rather than reopening the Weyl/tail split.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()

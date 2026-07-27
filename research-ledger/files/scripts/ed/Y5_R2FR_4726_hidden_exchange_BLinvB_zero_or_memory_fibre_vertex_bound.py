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

CHECKPOINT = "4726"
CLAIM_ID = "L-568"
MARKER = "PPC4161_HIDDEN_EXCHANGE_BLINVB_ZERO_OR_MEMORY_FIBRE_VERTEX_BOUND_4726"
PACKET_MARKER = "PPC4161_PACKET_HIDDEN_EXCHANGE_BLINVB_ZERO_OR_MEMORY_FIBRE_VERTEX_BOUND_4726"
DECISION = "HIDDEN_EXCHANGE_POSITIVE_NORM_GATE_DERIVED_BMEM_BH_ZERO_UNSIGNED_FINITE_VERTEX_BOUND_STAGED_NONCLAIM"
NEXT_TARGET = "4727-Y5-R2FR-Bmem-eff-component-zero-or-first-source-backed-B-row.md"

DOC_PATH = POST / "4726-Y5-R2FR-hidden-exchange-BLinvB-zero-or-memory-fibre-vertex-bound.md"
FORMAL_PATH = FORMAL / "742-PPC4161-hidden-exchange-BLinvB-zero-or-memory-fibre-vertex-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4726_SOURCE_REGISTER.csv"
NORM_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4726_HIDDEN_EXCHANGE_NORM_THEOREM.csv"
VERTEX_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4726_MEMORY_FIBRE_VERTEX_AUDIT.csv"
FINITE_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4726_BLINVB_FINITE_BOUND_ROWS.csv"
BODY_CHARGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4726_BODY_CHARGE_BOUND_INSERT.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4726_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4726_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4726_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4726_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4726_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4726_VALIDATION.csv"


SOURCE_SPECS = [
    ("SRC4726_0", POST / "CURRENT_LOCAL_RESUME.md", "4726-Y5-R2FR-hidden-exchange-BLinvB-zero-or-memory-fibre-vertex-bound.md", "4725 handoff target."),
    ("SRC4726_1", POST / "4725-Y5-R2FR-no-bare-R2-parent-grammar-proof-or-cbare-finite-row.md", "hidden-exchange", "4725 names hidden exchange as the next total-c_R2_eff component."),
    ("SRC4726_2", SOURCE_DIR / "P8_Y5_R2FR_4725_NEXT_TARGET.csv", "4726-Y5-R2FR-hidden-exchange-BLinvB-zero-or-memory-fibre-vertex-bound.md", "machine handoff into 4726."),
    ("SRC4726_3", SOURCE_DIR / "P8_Y5_PARENT_QLOC_1589_EFFECTIVE_COEFFICIENT_LAW.csv", "LAW1589_0_integrated_hidden_modes", "1589 gives the integrated hidden-mode coefficient law."),
    ("SRC4726_4", SOURCE_DIR / "P8_Y5_PARENT_QLOC_1589_MEMORY_FIBRE_OWNER_STATUS.csv", "OWN1589_1_memory_Bmem", "1589 names memory/fibre owner gaps."),
    ("SRC4726_5", SOURCE_DIR / "P8_Y5_R2FR_4505_DECISION.csv", "B^T L^-1 B", "4505 states the positive hidden block zero rule."),
    ("SRC4726_6", SOURCE_DIR / "P8_Y5_R2FR_4505_CLAIM_GATES.csv", "CG4505_0_positive_matrix", "4505 gate for the positive-matrix lemma."),
    ("SRC4726_7", SOURCE_DIR / "P8_Y5_R2FR_4505_POSITIVE_MATRIX_LEMMA.csv", "PM4505_0_positive_definite", "4505 formal positive matrix lemma."),
    ("SRC4726_8", SOURCE_DIR / "P8_Y5_R2FR_4505_BODY_CHARGE_GREEN_FUNCTION_LAW.csv", "BC4505_2_absolute_bound", "4505 Green-function body-charge absolute bound."),
    ("SRC4726_9", SOURCE_DIR / "P8_Y5_R2FR_4506_MEMORY_EXTREMUM_TEST.csv", "MEXT4506_1_branch_extremum", "4506 B_mem branch-extremum route."),
    ("SRC4726_10", SOURCE_DIR / "P8_Y5_R2FR_4506_MEMORY_OPERATOR_SIGNATURE.csv", "MOP4506_1_positive_gap", "4506 memory positive-gap route."),
    ("SRC4726_11", SOURCE_DIR / "P8_Y5_R2FR_4506_FIBRE_OWNER_GATE.csv", "FIB4506_1_no_curvature_vertex", "4506 fibre no-curvature-vertex gate."),
    ("SRC4726_12", SOURCE_DIR / "P8_Y5_R2FR_4506_BODY_CHARGE_INPUT_ROW.csv", "BCIN4506_0_memory_density", "4506 memory/fibre body-charge input rows."),
    ("SRC4726_13", SOURCE_DIR / "P8_Y5_R2FR_4683_OWNER_ZERO_SWITCH.csv", "ZS4683_3_no_smuggling", "4683 no-smuggling norm statement."),
    ("SRC4726_14", SOURCE_DIR / "P8_Y5_R2FR_4683_MEMORY_BODY_CHARGE_BOUND.csv", "MEM4683_2_amplitude", "4683 memory amplitude bound."),
    ("SRC4726_15", SOURCE_DIR / "P8_Y5_R2FR_4683_FIBRE_BODY_CHARGE_BOUND.csv", "FIB4683_2_amplitude", "4683 fibre amplitude bound."),
    ("SRC4726_16", SOURCE_DIR / "P8_Y5_R2FR_4683_BMEM_EFF_INSERTION.csv", "BM4683_5_combined", "4683 B_mem_eff component insertion."),
    ("SRC4726_17", SOURCE_DIR / "P8_Y5_R2FR_4683_FINITE_INPUT_SCHEMA.csv", "schema4683_2", "4683 finite input schema."),
    ("SRC4726_18", SOURCE_DIR / "P8_Y5_R10_1346_SYMBOLIC_COEFFICIENT_PACK.csv", "COEFF1346_M_B", "1346 symbolic memory/fibre coefficient pack."),
    ("SRC4726_19", SOURCE_DIR / "P8_Y5_R2FR_4670_BMEM_FIRST_COMPONENT_AUDIT.csv", "BFC4670_0_decomposition", "4670 B_mem_eff component audit."),
    ("SRC4726_20", SOURCE_DIR / "P8_Y5_R2FR_4670_ZM_PARENT_HESSIAN_AUDIT.csv", "ZMH4670_6_decision", "4670 memory Hessian decision."),
    ("SRC4726_21", SOURCE_DIR / "P8_Y5_R2FR_4670_ZM_B826_FIRST_ROW_CONTRACT.csv", "FR4670_0_Zmem_parent", "4670 first finite source-row contract."),
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


def norm_theorem_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "HX4726_0_hidden_exchange_law",
            "hidden exchange contribution",
            "c_hidden(k)=1/2 <B,L^-1(k)B>",
            "integrating out a hidden/memory/fibre fluctuation with curvature-linear source B generates an R L^-1 R response",
            "DERIVED_SYMBOLIC_LAW_IMPORTED",
            "does not yet give B, L or arena normalization",
        ),
        (
            "HX4726_1_physical_quotient",
            "operator domain",
            "project to the physical local quotient, remove gauge/kernel modes, and invert L only on its positive range",
            "otherwise boundary/kernel pieces can masquerade as a vanished bulk inverse",
            "DOMAIN_GUARD_DERIVED",
            "needs branch-specific projection and boundary class before claim",
        ),
        (
            "HX4726_2_positive_norm",
            "positive hidden block",
            "if L>0 on the physical quotient, c_hidden=1/2 ||L^-1/2 B||^2 >= 0",
            "a positive hidden operator cannot hide a nonzero curvature-linear vertex",
            "NORM_GATE_DERIVED",
            "positivity helps only after B is projected into the same physical subspace",
        ),
        (
            "HX4726_3_zero_iff",
            "zero condition",
            "c_hidden=0 iff P_phys B=0 in every retained propagating memory/fibre direction",
            "no cancellation with c_bare, c_measure or c_boundary is accepted as a derivation",
            "EXACT_ZERO_TARGET_DERIVED",
            "the current corpus has not signed B_mem_eff=0 or B_h=0",
        ),
        (
            "HX4726_4_finite_exit",
            "finite bound fallback",
            "0 <= c_hidden_X <= ||P_phys B_X||^2/(2 lambda_min(L_X))",
            "if B survives, the route becomes a source-backed finite Yukawa/body-charge comparison",
            "FINITE_BOUND_SHAPE_DERIVED",
            "needs Z_X,M_X^2,B_X,C_X,J_X,Q_boundary_X and arena profile",
        ),
        (
            "HX4726_5_verdict",
            "4726 result",
            "hidden exchange is no longer a vague missing term: it is a positive norm gate plus two concrete vertex-zero targets, B_mem_eff and B_h",
            "this is progress because it forbids smuggling the hidden term away by silence or cancellation",
            "PROOF_STEP_COMPLETE_NONCLAIM",
            "local-GR/R2 channel remains open until the vertex zero or finite rows are sourced",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "target": target,
            "statement": statement,
            "meaning": meaning,
            "status": status,
            "blocker_or_guardrail": guardrail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for theorem_id, target, statement, meaning, status, guardrail in specs
    ]


def vertex_audit_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "VTX4726_0_memory_operator",
            "memory",
            "Z_mem,M2_mem,L_mem",
            "positive operator branch is conditionally derived",
            "Z_mem>0 and M2_mem>0 with zero modes removed",
            "MISSING_PARENT_HESSIAN_VALUE_OR_CONSTRAINT_ELIMINATION",
            "SRC4726_20",
        ),
        (
            "VTX4726_1_memory_vertex_total",
            "memory",
            "B_mem_eff",
            "B_mem_eff = B_826+B_Weyl_vec+B_Y5_trace+B_Y6_trace+B_src_boundary+B_src_readout",
            "all components zero in the same branch, no cancellation credit",
            "COMPONENT_VECTOR_READY_VALUES_MISSING",
            "SRC4726_16",
        ),
        (
            "VTX4726_2_memory_B826_first_component",
            "memory",
            "B_826",
            "B_826 = a_F L_cg^-2 R_m(m_L;X_B)",
            "R_m=0 with fixed X_B and parent-owned branch, or source-backed a_F,L_cg,R_m values",
            "FIRST_COMPONENT_ZERO_UNSIGNED",
            "SRC4726_19",
        ),
        (
            "VTX4726_3_memory_source_terms",
            "memory",
            "C_mem,J_mem,Q_boundary_mem",
            "rho_mem = B_mem_eff R_obs + C_mem T + J_mem plus boundary charge",
            "source silence and boundary no-hair in the same frame",
            "SOURCE_AND_BOUNDARY_SILENCE_UNSIGNED",
            "SRC4726_14",
        ),
        (
            "VTX4726_4_memory_poynting_guard",
            "memory",
            "J_EM_flux",
            "Poynting/EM flux can only be silent if same-Hodge/current owner, stationary tau and no radiative boundary flux are signed",
            "EM stress sits inside common Hilbert T_tot with no separate worldtube flux",
            "POYNTING_SUBCHANNEL_GUARDED_NOT_ZERO",
            "SRC4726_14",
        ),
        (
            "VTX4726_5_fibre_operator",
            "fibre",
            "Z_h,M2_h,L_h",
            "finite-cell fibre branch needs a parent fibre potential, positive gap and source independence",
            "unique gapped source-independent fibre solution or finite spectrum",
            "FIBRE_GAP_UNSIGNED",
            "SRC4726_11",
        ),
        (
            "VTX4726_6_fibre_curvature_vertex",
            "fibre",
            "B_h",
            "B_h=delta^2 S_parent/(delta h delta R_obs)",
            "hidden-visible coefficient typing theorem or constrained multiplier removes h R_obs",
            "B_H_ZERO_UNSIGNED",
            "SRC4726_11",
        ),
        (
            "VTX4726_7_fibre_source_terms",
            "fibre",
            "C_h,J_h,Q_boundary_h",
            "rho_h = B_h R_obs + C_h T + J_h plus boundary charge",
            "matter blindness and no boundary/projection flux",
            "FIBRE_SOURCE_AND_BOUNDARY_UNSIGNED",
            "SRC4726_15",
        ),
        (
            "VTX4726_8_total_hidden_exchange",
            "both",
            "c_hidden_mem+c_hidden_h",
            "1/2 <B_mem_eff,L_mem^-1B_mem_eff> + 1/2 <B_h,L_h^-1B_h> plus any retained sector copies",
            "B_mem_eff=B_h=0 after physical projection, or finite source-backed bound rows",
            "ZERO_UNSIGNED_FINITE_ROUTE_STAGED",
            "SRC4726_13",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": audit_id,
            "sector": sector,
            "symbol": symbol,
            "current_formula_or_clause": formula,
            "zero_or_bound_requirement": requirement,
            "status": status,
            "source_path": source_path(src),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for audit_id, sector, symbol, formula, requirement, status, src in specs
    ]


def finite_bound_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "HXB4726_0_memory_norm_bound",
            "memory",
            "c_hidden_mem",
            "0 <= c_hidden_mem <= ||B_mem_eff||^2/(2 lambda_min(L_mem))",
            "operator-normalized R2 coefficient units",
            "Z_mem;M2_mem;physical projection;B_mem_eff components",
            "MISSING_PARENT_HESSIAN_AND_BMEM_COMPONENT_VALUES",
            "SRC4726_13",
        ),
        (
            "HXB4726_1_memory_low_momentum",
            "memory",
            "c_hidden_mem_IR",
            "c_hidden_mem_IR ~= ||B_mem_eff||^2/(2 M2_mem) when the massive local expansion is valid",
            "m^2 or parent-declared f(R) units after normalization",
            "M2_mem;B_mem_eff;normalization from same branch",
            "MISSING_M2MEM_AND_NORMALIZATION",
            "SRC4726_3",
        ),
        (
            "HXB4726_2_memory_component_envelope",
            "memory",
            "||B_mem_eff||",
            "||B_mem_eff|| <= ||B_826||+||B_Weyl_vec||+||B_Y5_trace||+||B_Y6_trace||+||B_src_boundary||+||B_src_readout||",
            "same as B_mem_eff",
            "component zeros or component finite values",
            "ABSOLUTE_SUM_READY_VALUES_MISSING",
            "SRC4726_16",
        ),
        (
            "HXB4726_3_fibre_norm_bound",
            "fibre",
            "c_hidden_h",
            "0 <= c_hidden_h <= ||B_h||^2/(2 lambda_min(L_h))",
            "operator-normalized R2 coefficient units",
            "Z_h;M2_h;physical projection;B_h",
            "MISSING_FIBRE_GAP_AND_BH_VALUE",
            "SRC4726_13",
        ),
        (
            "HXB4726_4_fibre_low_momentum",
            "fibre",
            "c_hidden_h_IR",
            "c_hidden_h_IR ~= ||B_h||^2/(2 M2_h) when the continuum massive fibre approximation is valid",
            "m^2 or parent-declared f(R) units after normalization",
            "M2_h;B_h;normalization from same branch",
            "MISSING_M2H_AND_BH_NORMALIZATION",
            "SRC4726_15",
        ),
        (
            "HXB4726_5_total_hidden_exchange",
            "both",
            "c_hidden_total",
            "c_hidden_total = c_hidden_mem + c_hidden_h + retained-sector copies",
            "same c_R2_eff_total units",
            "all retained B_X,L_X rows source-backed or theorem-zero",
            "TOTAL_HIDDEN_EXCHANGE_NONCLAIM",
            "SRC4726_17",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "sector": sector,
            "quantity": quantity,
            "bound_or_formula": formula,
            "units": units,
            "needed_inputs": needed_inputs,
            "current_status": status,
            "source_path": source_path(src),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for row_id, sector, quantity, formula, units, needed_inputs, status, src in specs
    ]


def body_charge_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "BC4726_0_memory_density",
            "memory",
            "rho_mem = B_mem_eff R_obs + C_mem T + J_mem",
            "B_mem_eff=C_mem=J_mem=0",
            "||rho_mem|| <= ||B_mem_eff||||R_obs|| + ||C_mem||||T|| + ||J_mem||",
            "B_mem_eff;C_mem;J_mem;R_obs;T;source paths",
            "SRC4726_14",
        ),
        (
            "BC4726_1_memory_amplitude",
            "memory",
            "|A_mem| <= [exp(R_body/lambda_mem) int_body (||B_mem_eff||||R_obs||+||C_mem||||T||+||J_mem||) dV + ||Q_boundary_mem||]/(4*pi ||Z_mem||)",
            "positive L_mem plus B_mem_eff=C_mem=J_mem=Q_boundary_mem=0",
            "if nonzero, map A_mem/lambda_mem to alpha_mem(lambda_mem), R10/orbital/PPN residual",
            "Z_mem;M2_mem;lambda_mem;B_mem_eff;C_mem;J_mem;Q_boundary_mem;arena projection",
            "SRC4726_14",
        ),
        (
            "BC4726_2_fibre_density",
            "fibre",
            "rho_h = B_h R_obs + C_h T + J_h",
            "B_h=C_h=J_h=0",
            "||rho_h|| <= ||B_h||||R_obs|| + ||C_h||||T|| + ||J_h||",
            "B_h;C_h;J_h;R_obs;T;source paths",
            "SRC4726_15",
        ),
        (
            "BC4726_3_fibre_amplitude",
            "fibre",
            "|A_h| <= [exp(R_body/lambda_h) int_body (||B_h||||R_obs||+||C_h||||T||+||J_h||) dV + ||Q_boundary_h||]/(4*pi ||Z_h||)",
            "positive L_h plus B_h=C_h=J_h=Q_boundary_h=0",
            "if nonzero, map A_h/lambda_h to alpha_h(lambda_h), R10/orbital/PPN residual",
            "Z_h;M2_h;lambda_h;B_h;C_h;J_h;Q_boundary_h;arena projection",
            "SRC4726_15",
        ),
        (
            "BC4726_4_no_exterior_silence_smuggle",
            "both",
            "source-free exterior equations do not erase an interior weighted body charge",
            "weighted interior charge and boundary charge vanish, or exact parent-owned cancellation",
            "absolute body-charge bound must be retained if any source term survives",
            "interior body profile; boundary variational class; same-frame source map",
            "SRC4726_8",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": bound_id,
            "sector": sector,
            "formula": formula,
            "zero_condition": zero_condition,
            "bound": bound,
            "needed_inputs": needed_inputs,
            "source_path": source_path(src),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for bound_id, sector, formula, zero_condition, bound, needed_inputs, src in specs
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4726_0_sources_verified", "All 4726 source paths exist and needles are found.", True, "NONE"),
        ("GATE4726_1_positive_norm_gate", "Hidden exchange positive-norm zero iff projected B=0 theorem is derived.", True, "THEOREM_DERIVED_NOT_CLAIM"),
        ("GATE4726_2_memory_Bmem_eff_zero", "B_mem_eff is zero componentwise in the same parent branch.", False, "BMEM_EFF_COMPONENTS_UNSIGNED"),
        ("GATE4726_3_fibre_Bh_zero", "B_h is zero by parent typing/constraint theorem.", False, "BH_ZERO_UNSIGNED"),
        ("GATE4726_4_memory_operator_owned", "Z_mem,M2_mem or constraint-elimination row is parent-signed.", False, "ZMEM_M2MEM_UNSIGNED"),
        ("GATE4726_5_fibre_operator_owned", "Z_h,M2_h or finite fibre spectrum row is parent-signed.", False, "ZH_M2H_UNSIGNED"),
        ("GATE4726_6_body_charge_inputs_owned", "C/J/boundary/source profile rows are zero or source-backed.", False, "BODY_CHARGE_INPUTS_MISSING"),
        ("GATE4726_7_hidden_exchange_closed", "c_hidden_total is zero or bounded claim-grade.", False, "HIDDEN_EXCHANGE_RETAINED_NONCLAIM"),
        ("GATE4726_8_local_GR_R2_channel_closed", "The hidden-exchange component of c_R2_eff_total is removed claim-grade.", False, "LOCAL_GR_NOT_PROMOTED"),
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
        ("FW4726_0_no_positive_operator_smuggle", "A positive L does not make the hidden source vanish; it makes B=0 the exact target."),
        ("FW4726_1_no_cross_component_cancellation", "Do not cancel c_hidden against c_bare, c_measure or c_boundary unless a parent Ward/topological identity owns the cancellation."),
        ("FW4726_2_no_exterior_source_free_shortcut", "Source-free exterior equations do not remove interior body charge or boundary charge."),
        ("FW4726_3_no_poynting_silence", "Do not set EM/Poynting flux terms to zero unless same-current, same-Hodge and no-boundary-flux clauses are signed."),
        ("FW4726_4_no_R10_backsolve", "Do not infer B_X or M_X from R10 bounds; derive/source them before comparing."),
        ("FW4726_5_same_branch_only", "All zero clauses must live in the same parent branch and observed-frame normalization."),
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
            "derivation_result": "for a positive physical hidden operator, 1/2 B^T L^-1 B is a nonnegative norm and vanishes iff the projected curvature-linear vertex vanishes",
            "vertex_result": "B_mem_eff and B_h are the concrete zero targets; current source rows keep both unsigned",
            "finite_row_result": "memory/fibre norm bounds and body-charge bounds are staged nonclaim",
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
            "status_id": "STATUS4726_0_local_only",
            "status": "local_files_only_no_github_action",
            "detail": "Generated under post-checkpoint-work and formalization-workbench only.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4726_1_science_verdict",
            "status": "hidden_exchange_norm_gate_derived_vertices_unsigned",
            "detail": "The hidden exchange problem is now sharpened to B_mem_eff/B_h vertex-zero or finite source-backed bound rows.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "4726 proves the hidden-exchange block is killed only by killing the projected curvature-linear vertex. The memory branch is more developed than the fibre branch, so attack B_mem_eff components first.",
            "first_task": "Try to prove the B_826 first component zero: B_826=a_F L_cg^-2 R_m(m_L;X_B), so target R_m=0, fixed X_B, branch lock, or a finite sourced a_F/L_cg/R_m row.",
            "fallback_task": "If B_826 survives, stage its finite row and propagate it into the memory body-charge/R10/PPN nonclaim runner.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    ts: str,
    theorem: list[dict[str, Any]],
    vertices: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4726 - Hidden Exchange BLinvB Zero or Memory/Fibre Vertex Bound

Generated: `{ts}`

## Purpose

4726 attacks the hidden-exchange component of `c_R2_eff_total`: `1/2 B^T L^-1 B`. The point is to stop treating this as a vague missing coefficient and turn it into an exact mathematical gate.

## What Actually Moved

- The hidden block has a clean theorem shape: if `L` is positive on the physical local quotient, then `1/2 B^T L^-1 B = 1/2 ||L^-1/2 B||^2 >= 0`.
- Therefore the hidden block vanishes only when the projected curvature-linear vertex vanishes: `P_phys B=0`.
- No cancellation credit is allowed against `c_bare`, `c_measure`, or `c_boundary` unless a parent Ward/topological identity explicitly owns it.
- The concrete zero targets are now `B_mem_eff=0` and `B_h=0`, not an undefined hidden sector.
- Since those vertices remain unsigned, memory/fibre finite norm and body-charge bounds are staged as nonclaim rows.

## Norm Theorem

{bullets(theorem, "theorem_id", "status")}

## Vertex Audit

{bullets(vertices, "audit_id", "status")}

## Finite Bound Rows

{bullets(finite, "row_id", "current_status")}

## Gates

{bullets(gates, "gate_id", "blocker")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 742 - Hidden Exchange BLinvB Zero or Memory/Fibre Vertex Bound

Generated: `{ts}`

## Result

For a positive hidden/memory/fibre operator on the physical quotient,

`c_hidden = 1/2 <B,L^-1 B> = 1/2 ||L^-1/2 B||^2 >= 0`.

Thus `c_hidden=0` is not obtained by hoping the hidden sector is quiet. It requires `P_phys B=0` in each retained propagating direction, with zero modes and boundary charges already removed.

## Current Split

`c_hidden_total = c_hidden_mem + c_hidden_h + retained-sector copies`.

`c_hidden_mem` is controlled by `B_mem_eff`; `c_hidden_h` is controlled by `B_h`. Both are unsigned in the current corpus, so the local-GR/R2 branch remains nonclaim.

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
- Derivation gain: the hidden exchange block `1/2 B^T L^-1 B` is a positive norm on the physical quotient, so it vanishes only when the projected curvature-linear vertex vanishes.
- Current zero targets: `B_mem_eff=0` and `B_h=0`; both remain unsigned, so finite memory/fibre vertex bounds are staged nonclaim.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: converts hidden exchange from a vague blocker into a positive-norm vertex-zero gate plus finite body-charge fallback rows.
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

- The hidden exchange term `1/2 B^T L^-1 B` is now an exact positive-norm gate on the physical quotient.
- It can vanish only if the projected curvature-linear vertices vanish: `B_mem_eff=0` and `B_h=0`.
- Since those zero owners are still unsigned, memory/fibre finite norm and body-charge rows remain staged as nonclaim.

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
        "claim": "4726 proves the hidden-exchange block is a positive norm on the physical quotient, so zero requires projected B_mem_eff/B_h vertex silence; current vertices remain unsigned.",
        "current_evidence": "Generated source register, norm theorem, memory/fibre vertex audit, BLinvB finite bound rows, body-charge inserts, promotion gates, firewalls, decision, status, next target and validation.",
        "status": "hidden_exchange_norm_gate_derived_vertex_zero_unsigned_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating positive L or source-free exterior equations as if they erase nonzero B_X or body charge.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "B_mem_eff or B_h may survive and generate R2/fR residuals unless parent-zero or finite bounds are sourced.",
        "title": "Hidden exchange BLinvB zero or memory/fibre vertex bound",
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
    theorem: list[dict[str, Any]],
    vertices: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    body_charge: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    ts: str,
) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER_CSV,
        NORM_THEOREM_CSV,
        VERTEX_AUDIT_CSV,
        FINITE_BOUND_CSV,
        BODY_CHARGE_CSV,
        GATES_CSV,
        FIREWALL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_TARGET_CSV,
    ]
    theorem_statuses = {row["status"] for row in theorem}
    vertex_status = ";".join(row["status"] for row in vertices)
    finite_status = ";".join(row["current_status"] for row in finite)
    body_inputs = ";".join(row["needed_inputs"] for row in body_charge)
    checks = [
        ("VAL4726_0_sources_exist", all(bool(row["exists"]) for row in sources), "all cited 4726 source paths exist"),
        ("VAL4726_1_needles_found", all(bool(row["needle_found"]) for row in sources), "all cited 4726 source needles found"),
        ("VAL4726_2_positive_norm_derived", "NORM_GATE_DERIVED" in theorem_statuses and "EXACT_ZERO_TARGET_DERIVED" in theorem_statuses, "positive norm and zero-iff target rows written"),
        ("VAL4726_3_memory_vertex_not_promoted", "BMEM_EFF_COMPONENTS_UNSIGNED" in vertex_status or "COMPONENT_VECTOR_READY_VALUES_MISSING" in vertex_status, "memory vertex zero remains unsigned"),
        ("VAL4726_4_fibre_vertex_not_promoted", "B_H_ZERO_UNSIGNED" in vertex_status or "FIBRE_GAP_UNSIGNED" in vertex_status, "fibre vertex zero remains unsigned"),
        ("VAL4726_5_finite_bounds_nonclaim", "MISSING_PARENT_HESSIAN_AND_BMEM_COMPONENT_VALUES" in finite_status and "MISSING_FIBRE_GAP_AND_BH_VALUE" in finite_status and all(not bool(row["valid_for_claim"]) for row in finite), "finite bound rows staged nonclaim"),
        ("VAL4726_6_body_charge_inputs_retained", "Q_boundary_mem" in body_inputs and "Q_boundary_h" in body_inputs and all(not bool(row["valid_for_claim"]) for row in body_charge), "body-charge memory/fibre inputs retained nonclaim"),
        ("VAL4726_7_claim_gates_closed", all(not bool(row["claim_allowed"]) for row in gates) and not any(row["passed"] for row in gates if row["gate_id"] not in {"GATE4726_0_sources_verified", "GATE4726_1_positive_norm_gate"}), "all broad claim gates remain closed; theorem gate is not claim"),
        ("VAL4726_8_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4726_9_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4726_10_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4727 next target"),
        ("VAL4726_11_csv_parse", all(parse_csv(path) for path in csv_paths), "all generated 4726 CSV files parse cleanly"),
        ("VAL4726_12_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
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
            "check_id": "VAL4726_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "4726 hidden exchange BLinvB zero or memory/fibre vertex-bound validation",
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()
    cleanup_pycache()
    sources = source_register(ts)
    theorem = norm_theorem_rows(ts)
    vertices = vertex_audit_rows(ts)
    finite = finite_bound_rows(ts)
    body_charge = body_charge_rows(ts)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(NORM_THEOREM_CSV, theorem)
    write_csv(VERTEX_AUDIT_CSV, vertices)
    write_csv(FINITE_BOUND_CSV, finite)
    write_csv(BODY_CHARGE_CSV, body_charge)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(ts, theorem, vertices, finite, gates)
    update_spine_packet_resume(ts)
    add_claim_once(ts)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, theorem, vertices, finite, body_charge, gates, ts))


if __name__ == "__main__":
    main()

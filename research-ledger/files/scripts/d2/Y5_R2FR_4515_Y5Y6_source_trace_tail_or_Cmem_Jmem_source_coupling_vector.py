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

CHECKPOINT = "4515"
CLAIM_ID = "L-357"
MARKER = "PPC4161_Y5Y6_SOURCE_TRACE_TAIL_OR_CMEM_JMEM_SOURCE_COUPLING_VECTOR_4515"
PACKET_MARKER = "PPC4161_PACKET_Y5Y6_SOURCE_TRACE_TAIL_OR_CMEM_JMEM_SOURCE_COUPLING_VECTOR_4515"
DECISION = "SOURCE_FUNCTOR_DESCENT_THEOREM_DERIVED_CONDITIONALLY_SOURCE_COUPLING_VECTOR_STAGED_NONCLAIM"
NEXT_TARGET = "4516-Y5-R2FR-source-functor-parent-signature-or-first-Y5-coefficient-fill.md"

FORMAL_PATH = FORMAL / "531-PPC4161-Y5-Y6-source-trace-tail-or-Cmem-Jmem-source-coupling-vector.md"
DOC_PATH = POST / "4515-Y5-R2FR-Y5-Y6-source-trace-tail-or-Cmem-Jmem-source-coupling-vector.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4515_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4515_SOURCE_REGISTER.csv"
SOURCE_FUNCTOR_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4515_SOURCE_FUNCTOR_DESCENT_THEOREM.csv"
Y5_TRACE_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4515_Y5_SOURCE_TRACE_VECTOR.csv"
Y6_TRACE_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4515_Y6_EXTRA_STRESS_TRACE_VECTOR.csv"
CMEM_JMEM_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4515_CMEM_JMEM_COUPLING_VECTOR.csv"
SOURCE_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4515_SOURCE_COUPLING_BOUND.csv"
PARENT_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4515_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4515_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4515_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4515_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4515_DECISION.csv"

FORMAL_530 = FORMAL / "530-PPC4161-BWeyl-vector-insertion-into-Bmem-eff-or-body-charge-bound.md"
POST_4514 = POST / "4514-Y5-R2FR-BWeyl-vector-insertion-into-Bmem-eff-or-body-charge-bound.md"
TAIL_LEDGER_4514 = SOURCE_DIR / "P8_Y5_R2FR_4514_REMAINING_SOURCE_TAIL_LEDGER.csv"
BMEM_VECTOR_4514 = SOURCE_DIR / "P8_Y5_R2FR_4514_BMEM_EFFECTIVE_COMPONENT_VECTOR.csv"
BODY_BOUND_4514 = SOURCE_DIR / "P8_Y5_R2FR_4514_BODY_CHARGE_INSERTION_BOUND.csv"
SFE_1354 = SOURCE_DIR / "P8_Y5_R10_1354_SOURCE_FUNCTIONAL_EVENNESS_ATTEMPT.csv"
JZ_1354 = SOURCE_DIR / "P8_Y5_R10_1354_Y5Y6_JZ_COEFFICIENT_FILL.csv"
SN_AUDIT = SOURCE_DIR / "P8_SOURCE_NORMALIZATION_CHANNEL_AUDIT.csv"
SN_FILL = SOURCE_DIR / "P8_SOURCE_NORMALIZATION_COEFFICIENT_FILL.csv"
SRC_CURRENT = SOURCE_DIR / "P8_source_current_Ward_universality_CONTRACT.csv"
SRC_OWNER = SOURCE_DIR / "P8_source_owner_parent_action_terms_CONTRACT.csv"
HILBERT_DIV = SOURCE_DIR / "P8_Y5_HILBERT_CURRENT_2467_DIVERGENCE_IDENTITY.csv"
HILBERT_EXCHANGE = SOURCE_DIR / "P8_Y5_HILBERT_CURRENT_2467_EXCHANGE_CURRENT_IDENTITY.csv"
HILBERT_VERDICT = SOURCE_DIR / "P8_Y5_HILBERT_CURRENT_2467_PROMOTION_VERDICT.csv"
EM_FLUX = SOURCE_DIR / "P8_Y5_I_matter_EM_flux_status.csv"
EM_JQ = SOURCE_DIR / "P8_Y5_Jq_matter_EM_Poynting_subcomponent_status.csv"
JOINT_OWNER = SOURCE_DIR / "P8_Y5_joint_TQ_NQ_JQ_owner_packet_status.csv"

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


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4515_00_formal530", "4514 formal handoff", FORMAL_530, MARKER.replace("4515", "4514").replace("Y5Y6_SOURCE_TRACE_TAIL_OR_CMEM_JMEM_SOURCE_COUPLING_VECTOR", "BWEYL_VECTOR_INSERTION_INTO_BMEM_EFF_OR_BODY_CHARGE_BOUND"), "Bmem/body-charge handoff"),
        ("SRC4515_01_post4514", "4514 post handoff", POST_4514, "NT4514_0", "declares 4515 source-coupling target"),
        ("SRC4515_02_tail4514", "4514 remaining source tail ledger", TAIL_LEDGER_4514, "STL4514_0_Y5_priority", "Y5/Y6/Cmem/Jmem/Qboundary source tails"),
        ("SRC4515_03_bmem4514", "4514 Bmem vector", BMEM_VECTOR_4514, "BMV4514_6_combined", "Bmem effective component vector"),
        ("SRC4515_04_body4514", "4514 body-charge bound", BODY_BOUND_4514, "BCB4514_3_amplitude", "A_mem source amplitude bound"),
        ("SRC4515_05_sfe1354", "1354 source functional evenness attempt", SFE_1354, "SFE1354_6_verdict", "source-functional evenness not proved"),
        ("SRC4515_06_jz_y5", "1354 Y5 coefficient rows", JZ_1354, "JZ1354_Y5_0_radial_Meff_hair", "eight Y5 source-normalization rows"),
        ("SRC4515_07_jz_y6", "1354 Y6 coefficient rows", JZ_1354, "JZ1354_Y6_3_metric_response_tail", "four Y6 extra-stress rows"),
        ("SRC4515_08_sn_audit", "source-normalization channel audit", SN_AUDIT, "C1_domain_projector", "hard source-normalization channel"),
        ("SRC4515_09_sn_fill", "source-normalization coefficient fill", SN_FILL, "F0_c_domain_source_normalization_operator", "coefficient fill path"),
        ("SRC4515_10_source_current", "source-current Ward universality", SRC_CURRENT, "SC4_no_nonHilbert_source_current", "non-Hilbert current gate"),
        ("SRC4515_11_source_owner", "source owner parent action contract", SRC_OWNER, "A9_memory_kernel_local_silence", "memory/source owner action terms"),
        ("SRC4515_12_hilbert_div", "Hilbert current divergence", HILBERT_DIV, "DIV2467_1_full_divergence", "exact current divergence identity"),
        ("SRC4515_13_hilbert_exchange", "Hilbert current exchange", HILBERT_EXCHANGE, "EXC2467_1_clock_exchange_form", "dynamic clock/source exchange route"),
        ("SRC4515_14_hilbert_verdict", "Hilbert current promotion verdict", HILBERT_VERDICT, "PV2467_4_overall", "stationary route sharpened, dynamic closure blocked"),
        ("SRC4515_15_em_flux", "EM/Poynting flux status", EM_FLUX, "I_matter_EM_flux", "Poynting flux conditional-zero/finite-bound row"),
        ("SRC4515_16_em_jq", "EM/Poynting Jq subcomponent", EM_JQ, "JQ_MATTER_EM_POYNTING_SUBCOMPONENT_BOUND_FILLED", "EM/Poynting subcomponent bound"),
        ("SRC4515_17_joint_owner", "joint TQ/NQ/JQ owner packet", JOINT_OWNER, "BUILT_NOT_PARENT_SIGNED", "joint current owner packet not parent-signed"),
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


def source_functor_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "SFT4515_0_chain_rule",
            "object": "source functional derivative",
            "statement": "For a source functional that descends through the public quotient, the memory/source derivative splits into quotient-visible, projector/calibration, retained-current and boundary pieces.",
            "formula": "D_m S_src = (delta Sbar_src/delta q) Dq[v_m] + (D_m Pi_M) J_H + Pi_M D_m J_retained + D_m S_boundary",
            "zero_route": "Dq[v_m]=0; D_m Pi_M=0; J_retained=0; D_m S_boundary=0",
            "fallback_bound": "|D_m S_src| <= |S_q||Dq[v_m]|+|D_m Pi_M||J_H|+|Pi_M||D_m J_retained|+|D_m S_boundary|",
            "status": "CHAIN_RULE_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "SFT4515_1_single_source_functor_zero",
            "object": "Y5/Cmem/Jmem common zero",
            "statement": "Y5 source-normalization, C_mem matter-trace coupling and J_mem direct/source current vanish together if the active source is a single q-basic Hilbert-current functor with universal calibration and no retained non-Hilbert current.",
            "formula": "S_active=Sbar[q(Phi),Psi,theta]; v_m in ker(Dq); Pi_M=q-basic; kappa=constant; q_retained=0 => B_Y5_trace=C_mem=J_mem=0",
            "zero_route": "single observed coframe plus closed calibrated mass projector plus source-label forgetting plus Ward/exchange closure",
            "fallback_bound": "retain |B_Y5_trace|, |C_mem||T| and |J_mem| as separate absolute source terms",
            "status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "SFT4515_2_Y5_measured_GM",
            "object": "B_Y5_trace",
            "statement": "Measured-GM/source-normalization cannot be killed by fitting G; it is zero only when the source monopole is the same closed calibrated Hilbert-current projection in every arena.",
            "formula": "B_Y5_trace=0 if D_m(Pi_M J_H)=0 and partial_t,r,lambda,A kappa_eff=0",
            "zero_route": "q-basic Pi_M, closed flux, universal constant kappa_eff, no radial/range/time/species hair",
            "fallback_bound": "|B_Y5_trace| <= sum_i |j_Z,Y5_i| |P_i|",
            "status": "DERIVED_ZERO_CONTRACT_PLUS_FINITE_VECTOR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "SFT4515_3_Y6_extra_stress",
            "object": "B_Y6_trace",
            "statement": "Extra stress is safe only if it is topological/invisible, already part of the owned metric response, or exchange-even; otherwise it is a separate source trace tail.",
            "formula": "B_Y6_trace=0 if T_extra in {topological, EH-owned metric response, exchange-even/no local variation}",
            "zero_route": "no independent anisotropic/source stress and no Khat metric-response mismatch",
            "fallback_bound": "|B_Y6_trace| <= sum_j |j_Z,Y6_j| |X_j|",
            "status": "DERIVED_ZERO_CONTRACT_PLUS_FINITE_VECTOR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "SFT4515_4_EM_Poynting_guard",
            "object": "J_mem EM/Poynting subchannel",
            "statement": "EM/Poynting flow is not ignored: if it is inside the common Hilbert stress under the same Hodge/current owner and stationary/no-radiation collar, it is not a separate J_mem; otherwise it remains an absolute flux term.",
            "formula": "J_mem = J_nonHilbert + J_EM_flux; J_EM_flux=0 only under same_Hodge + same_current_owner + stationary_tau + no_radiative_boundary_flux",
            "zero_route": "EM stress belongs to T_tot and no Poynting flux crosses the worldtube boundary",
            "fallback_bound": "|J_EM_flux| <= |Phi_EM_rad|+|W_public_exchange|+|C_EM_surface_gauge|",
            "status": "POYNTING_CHANNEL_INSERTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "SFT4515_5_body_charge_source_bound",
            "object": "A_mem source envelope",
            "statement": "The 4514 amplitude bound can now be evaluated with one source-coupling vector rather than loose prose.",
            "formula": "|A_mem| <= [exp(R/lambda) int_body (|R_obs| Sigma_B + |C_mem||T| + |J_mem|) dV + |Q_boundary_mem|]/(4*pi |Z_mem|)",
            "zero_route": "Sigma_B=C_mem=J_mem=Q_boundary_mem=0 plus positive Z_mem/M2_mem and zero-mode removal",
            "fallback_bound": "Sigma_B=|B_826|+|B_Weyl_vec|+|B_Y5_trace|+|B_Y6_trace|+|B_src_boundary|+|B_src_readout|",
            "status": "FINITE_SOURCE_COUPLING_BOUND_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def y5_trace_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source in read_csv(JZ_1354):
        if source.get("sector") != "Y5_source_normalization":
            continue
        rows.append(
            {
                "vector_id": f"Y5V4515_{len(rows)}_{source['coefficient_id']}",
                "symbol": source["symbol"],
                "meaning": source["meaning"],
                "zero_condition": source["source_requirement"],
                "finite_contribution": f"|{source['symbol']}| * |P_{len(rows)}|",
                "observable_link": source["observable_link"],
                "current_status": source["current_status"],
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.append(
        {
            "vector_id": "Y5V4515_8_total",
            "symbol": "B_Y5_trace",
            "meaning": "total measured-GM/source-normalization source trace tail",
            "zero_condition": "all eight Y5 rows theorem-zero in the same source-functor branch",
            "finite_contribution": "|B_Y5_trace| <= sum_i |j_Z,Y5_i| |P_i|",
            "observable_link": "R10/R11/PPN/Gdot/source-charge arenas through 4514 A_mem envelope",
            "current_status": "FINITE_VECTOR_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def y6_trace_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source in read_csv(JZ_1354):
        if source.get("sector") != "Y6_extra_stress":
            continue
        rows.append(
            {
                "vector_id": f"Y6V4515_{len(rows)}_{source['coefficient_id']}",
                "symbol": source["symbol"],
                "meaning": source["meaning"],
                "zero_condition": source["source_requirement"],
                "finite_contribution": f"|{source['symbol']}| * |X_{len(rows)}|",
                "observable_link": source["observable_link"],
                "current_status": source["current_status"],
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.append(
        {
            "vector_id": "Y6V4515_4_total",
            "symbol": "B_Y6_trace",
            "meaning": "total extra-stress source trace tail",
            "zero_condition": "all four Y6 rows topological/EH-owned/exchange-even in the same branch",
            "finite_contribution": "|B_Y6_trace| <= sum_j |j_Z,Y6_j| |X_j|",
            "observable_link": "Khat/Ward/PPN/source-stress/R11 plus 4514 A_mem envelope",
            "current_status": "FINITE_VECTOR_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def cmem_jmem_rows() -> List[Dict[str, object]]:
    return [
        {
            "component_id": "SCV4515_0_Cmem",
            "component": "C_mem T",
            "zero_condition": "matter action and trace standard descend through q(Phi) and memory direction is vertical to q with no explicit m-dependence in masses/standards",
            "finite_bound": "|C_mem T| <= |C_mem| |T|",
            "source_bridge": "S_matter=Sbar_m[q(Phi),Psi,theta]; v_m in ker(Dq)",
            "current_status": "CONDITIONAL_ZERO_UNSIGNED_VALUE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "SCV4515_1_Jmem_nonHilbert",
            "component": "J_mem non-Hilbert retained current",
            "zero_condition": "source-current Ward universality plus no retained non-Hilbert source current q_retained=0",
            "finite_bound": "|J_nonHilbert| retained as absolute source profile",
            "source_bridge": "SC4 and A1/A2 owner-current decomposition",
            "current_status": "CONDITIONAL_ZERO_UNSIGNED_VALUE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "SCV4515_2_Jmem_EM_Poynting",
            "component": "J_mem EM/Poynting flux",
            "zero_condition": "EM/Poynting is inside common Hilbert T_tot and no radiative/current flux crosses the local worldtube boundary",
            "finite_bound": "|J_EM_flux| <= |Phi_EM_rad|+|W_public_exchange|+|C_EM_surface_gauge|",
            "source_bridge": "3579/3612 EM-Poynting rows; same Hodge/current owner; stationary tau",
            "current_status": "FINITE_BOUND_IMPORTED_PARENT_OWNER_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "SCV4515_3_Qboundary_mem",
            "component": "Q_boundary_mem",
            "zero_condition": "fixed no-flux/topological boundary class with no linked source-normalization boundary charge",
            "finite_bound": "|Q_boundary_mem| retained in A_mem numerator",
            "source_bridge": "4513 boundary theorem plus source-functional boundary charge signing",
            "current_status": "CONDITIONAL_ZERO_UNSIGNED_VALUE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "SCV4515_4_total_density_source",
            "component": "rho_mem source tail",
            "zero_condition": "B_mem_eff=C_mem=J_mem=0 in same parent branch",
            "finite_bound": "|rho_mem| <= |R_obs| Sigma_B + |C_mem||T| + |J_mem|",
            "source_bridge": "4514 density row plus 4515 source-coupling vector",
            "current_status": "STRUCTURE_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def source_bound_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "SB4515_0_Sigma_B",
            "quantity": "Sigma_B",
            "formula": "Sigma_B=|B_826|+|B_Weyl_vec|+|B_Y5_trace|+|B_Y6_trace|+|B_src_boundary|+|B_src_readout|",
            "required_inputs": "4514 Bmem vector plus Y5/Y6/source boundary/readout theorem-zero or finite values",
            "current_status": "DERIVED_ABSOLUTE_SUM_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "SB4515_1_density",
            "quantity": "|rho_mem|",
            "formula": "|rho_mem| <= |R_obs| Sigma_B + |C_mem||T| + |J_mem|",
            "required_inputs": "R_obs,T profiles; source vector values; units; source paths",
            "current_status": "DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "SB4515_2_amplitude",
            "quantity": "|A_mem|",
            "formula": "|A_mem| <= [exp(R_body/lambda_mem) int_body (|R_obs|Sigma_B+|C_mem||T|+|J_mem|) dV + |Q_boundary_mem|]/(4*pi |Z_mem|)",
            "required_inputs": "Z_mem,M2_mem,lambda_mem,R_body,R_obs,T,J_mem,Q_boundary_mem,screening",
            "current_status": "DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "SB4515_3_nohair",
            "quantity": "local memory silence",
            "formula": "positive L_mem plus Sigma_B=C_mem=J_mem=Q_boundary_mem=0 => delta_m=0 and A_mem=0",
            "required_inputs": "positive operator, zero-mode removal and same-branch source-functor theorem",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_LIVE_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PA4515_0_chain_rule",
            "clause": "source functional derivative split",
            "status": "DERIVED",
            "reason": "ordinary chain rule exposes quotient, projector, retained-current and boundary terms",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4515_1_single_source_functor",
            "clause": "single q-basic Hilbert-current source functor",
            "status": "NOT_PARENT_SIGNED",
            "reason": "SC0-SC7 and A1-A9 remain conditional/open in source-current/source-owner contracts",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4515_2_Y5_vector",
            "clause": "Y5 measured-GM/source-normalization tails",
            "status": "FINITE_VECTOR_STAGED",
            "reason": "eight 1354 rows are imported into a single |B_Y5_trace| sum",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4515_3_Y6_vector",
            "clause": "Y6 extra-stress tails",
            "status": "FINITE_VECTOR_STAGED",
            "reason": "four 1354 rows are imported into a single |B_Y6_trace| sum",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4515_4_Poynting",
            "clause": "EM/Poynting source-current channel",
            "status": "INSERTED_AS_GUARD",
            "reason": "Poynting flow is zero only if Hilbert-owned/no-flux; otherwise it stays inside |J_mem|",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4515_0_source_functor",
            "claim": "B_Y5_trace=C_mem=J_mem=0 live",
            "passed": False,
            "blocker": "single q-basic source functor and no-retained-current clauses are not parent-signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4515_1_Y6",
            "claim": "B_Y6_trace=0 live",
            "passed": False,
            "blocker": "extra stress invisibility/EH-owned response is not parent-signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4515_2_Amem",
            "claim": "A_mem=0/local no-hair",
            "passed": False,
            "blocker": "Sigma_B,C_mem,J_mem,Q_boundary_mem and positive-operator inputs are not all zero/sourced",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4515_3_public_local_GR",
            "claim": "local GR/Newton/PPN/R10 pass",
            "passed": False,
            "blocker": "source-coupling vector is staged nonclaim and no arena projections are claim-valid",
            "valid_for_claim": False,
        },
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "chain-rule source-functor descent theorem; Y5/Y6 finite trace vectors; C_mem/J_mem/Poynting coupling vector; A_mem source envelope",
            "not_derived": "live parent signature for single source functor, Y6 invisibility, numeric/source-backed coefficients, positive operator and arena projections",
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
            "decision_id": "DEC4515_0",
            "decision": DECISION,
            "because": "4514 showed B_Weyl is inserted; the remaining obstruction is source normalization/current ownership, so 4515 derives the exact source-functor condition and finite vector",
            "effect": "next work can either parent-sign the single source functor or fill the first Y5/Y6/Cmem/Jmem source coefficient; no more vague source-tail prose",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4515_0",
            "target_file": NEXT_TARGET,
            "task": "attempt to parent-sign the single q-basic Hilbert-current source functor; if it fails, fill the first source-backed Y5 coefficient row instead of re-auditing the same missing list",
            "success_condition": "SC0-SC7/A1-A9 source-functor clauses close, or at least one Y5/Y6/Cmem/Jmem coefficient becomes theorem-zero or source-backed finite",
            "avoid": "claiming local GR from conditional source-functor descent or hiding EM/Poynting flux outside J_mem",
            "valid_for_claim": False,
        }
    ]


def validate(all_rows: Mapping[str, Sequence[Mapping[str, object]]]) -> List[Dict[str, object]]:
    csv_paths = [
        SOURCE_REGISTER,
        SOURCE_FUNCTOR_THEOREM,
        Y5_TRACE_VECTOR,
        Y6_TRACE_VECTOR,
        CMEM_JMEM_VECTOR,
        SOURCE_BOUND,
        PARENT_AUDIT,
        CLAIM_GATES,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    details = []
    parsed_ok = True
    for path in csv_paths:
        try:
            details.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:  # pragma: no cover
            parsed_ok = False
            details.append(f"{path.name}:FAIL:{exc}")

    sources_ok = all(row["exists"] and row["needle_found"] for row in all_rows["sources"])
    theorem_ok = any(row["theorem_id"] == "SFT4515_1_single_source_functor_zero" for row in all_rows["theorem"])
    y5_ok = len([row for row in all_rows["y5"] if str(row["symbol"]).startswith("j_Z_")]) == 8
    y6_ok = len([row for row in all_rows["y6"] if str(row["symbol"]).startswith(("j_Z_", "b_Z_", "delta_K_"))]) == 4
    poynting_ok = any(row["component_id"] == "SCV4515_2_Jmem_EM_Poynting" for row in all_rows["coupling"])
    bound_ok = any(row["bound_id"] == "SB4515_2_amplitude" for row in all_rows["bound"])
    gates_blocked = all(str(row.get("passed")) == "False" for row in all_rows["gates"])
    flags_false = True
    for rows in all_rows.values():
        for row in rows:
            for key in ("valid_for_claim", "claim_allowed"):
                if key in row and str(row[key]).lower() != "false":
                    flags_false = False
    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()

    checks = [
        ("VAL4515_00_sources", sources_ok, "all source paths exist and source needles are found"),
        ("VAL4515_01_theorem", theorem_ok, "single source-functor zero theorem exists"),
        ("VAL4515_02_y5_vector", y5_ok, "eight Y5 source-normalization rows imported"),
        ("VAL4515_03_y6_vector", y6_ok, "four Y6 extra-stress rows imported"),
        ("VAL4515_04_poynting", poynting_ok, "EM/Poynting guard inserted into J_mem vector"),
        ("VAL4515_05_bound", bound_ok, "A_mem source-coupling finite bound exists"),
        ("VAL4515_06_claims_blocked", gates_blocked, "all claim gates remain blocked"),
        ("VAL4515_07_nonclaim_flags", flags_false, "all generated claim flags remain false"),
        ("VAL4515_08_csv_parse", parsed_ok, ";".join(details)),
        ("VAL4515_09_next_target", all_rows["next"][0]["target_file"] == NEXT_TARGET, NEXT_TARGET),
        ("VAL4515_10_pycache_absent", pycache_absent, "scripts __pycache__ absent after cleanup"),
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
            "validation_id": "VAL4515_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "4515 Y5/Y6 source trace tail or Cmem/Jmem source-coupling vector",
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
            "local_gr_newton_r2fr_source_coupling_vector",
            "4515 derives the source-functor chain-rule theorem: Y5 measured-GM/source-normalization, C_mem matter-trace coupling and J_mem direct/source current vanish together only if the active source is one q-basic Hilbert-current functor with universal calibration, no retained non-Hilbert current and no boundary/Poynting flux. It imports the eight Y5 rows and four Y6 rows into finite source trace vectors and writes the A_mem source-coupling envelope, but the live parent signature and numeric/source-backed coefficients remain unsigned.",
            "4515 source register, source-functor theorem, Y5 trace vector, Y6 trace vector, Cmem/Jmem vector, source bound, parent audit, claim gates, status and validation.",
            "private_source_functor_descent_and_source_coupling_vector_nonclaim",
            NEXT_TARGET,
            "claiming local GR/Newton/PPN/R10 from conditional source-functor descent, ignoring EM/Poynting flux, or absorbing source-normalization into fitted G.",
            "local_gr_newton_r2fr_source_coupling_vector",
            str(FORMAL_PATH),
            NEXT_TARGET,
            "parent-sign the single q-basic Hilbert-current source functor, or fill the first source-backed Y5/Y6/Cmem/Jmem coefficient row.",
        ]
    )
    CLAIMS_PATH.write_text(existing.rstrip() + "\n" + row + "\n", encoding="utf-8")


def build_doc(
    sources: Sequence[Mapping[str, object]],
    theorem: Sequence[Mapping[str, object]],
    y5: Sequence[Mapping[str, object]],
    y6: Sequence[Mapping[str, object]],
    coupling: Sequence[Mapping[str, object]],
    bound: Sequence[Mapping[str, object]],
    parent: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4515 - Y5/Y6 Source Trace Tail Or Cmem/Jmem Source-Coupling Vector

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4515 does the source-coupling move that 4514 exposed.

The key derivation is a chain-rule descent:

`D_m S_src = (delta Sbar_src/delta q) Dq[v_m] + (D_m Pi_M) J_H + Pi_M D_m J_retained + D_m S_boundary`.

Therefore `Y5`, `C_mem` and `J_mem` are not separate mysteries if the parent theory owns one source functor:

`S_active=Sbar[q(Phi),Psi,theta]; v_m in ker(Dq); Pi_M=q-basic; kappa=constant; q_retained=0 => B_Y5_trace=C_mem=J_mem=0`.

This is an exact conditional theorem, not a live claim. The parent signature is still unsigned. The useful forward movement is that the fallback is now concrete:

`|B_Y5_trace| <= sum_i |j_Z,Y5_i| |P_i|`,

`|B_Y6_trace| <= sum_j |j_Z,Y6_j| |X_j|`,

and

`|A_mem| <= [exp(R_body/lambda_mem) int_body (|R_obs|Sigma_B+|C_mem||T|+|J_mem|) dV + |Q_boundary_mem|]/(4*pi |Z_mem|)`.

EM/Poynting flow is explicitly included: if it is Hilbert-owned and no flux crosses the local worldtube, it is not a separate `J_mem`; otherwise it remains inside the absolute `J_mem` bound.

## Source Register

{table(sources)}

## Source-Functor Descent Theorem

{table(theorem)}

## Y5 Source Trace Vector

{table(y5)}

## Y6 Extra-Stress Trace Vector

{table(y6)}

## C_mem / J_mem Coupling Vector

{table(coupling)}

## Source-Coupling Bound

{table(bound)}

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
    theorem = source_functor_theorem_rows()
    y5 = y5_trace_rows()
    y6 = y6_trace_rows()
    coupling = cmem_jmem_rows()
    bound = source_bound_rows()
    parent = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows()
    decisions = decision_rows()
    next_target = next_rows()

    all_rows = {
        "sources": sources,
        "theorem": theorem,
        "y5": y5,
        "y6": y6,
        "coupling": coupling,
        "bound": bound,
        "parent": parent,
        "gates": gates,
        "status": status,
        "decisions": decisions,
        "next": next_target,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SOURCE_FUNCTOR_THEOREM, theorem)
    write_csv(Y5_TRACE_VECTOR, y5)
    write_csv(Y6_TRACE_VECTOR, y6)
    write_csv(CMEM_JMEM_VECTOR, coupling)
    write_csv(SOURCE_BOUND, bound)
    write_csv(PARENT_AUDIT, parent)
    write_csv(CLAIM_GATES, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(all_rows)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, theorem, y5, y6, coupling, bound, parent, gates, status, decisions, next_target, validation)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4515 Y5/Y6 Source Trace Tail Or Cmem/Jmem Source-Coupling Vector

Marker: `{MARKER}`  
4515 derives the source-functor chain-rule condition behind the remaining source tails. If the active source is a single q-basic Hilbert-current functor with universal calibration, no retained non-Hilbert current, no boundary source charge and no Poynting/worldtube flux, then `B_Y5_trace=C_mem=J_mem=0`; with the Y6 invisibility/EH-owned response clause, `B_Y6_trace=0` also. The live branch is not signed, so the eight Y5 rows, four Y6 rows and `C_mem/J_mem/Q_boundary_mem` terms are now staged as a finite source-coupling vector feeding the `A_mem` envelope.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4515 Packet Integration

Marker: `{PACKET_MARKER}`  
The private packet now has a concrete source-coupling vector rather than loose source-tail prose. The next local step is to parent-sign the single q-basic Hilbert-current source functor, or fill the first source-backed Y5/Y6/Cmem/Jmem coefficient row.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()

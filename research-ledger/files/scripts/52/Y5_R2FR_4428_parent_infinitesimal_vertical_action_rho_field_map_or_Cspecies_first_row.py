from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from rho_field_map_gate import evaluate_cspecies_rows, evaluate_rho_rows, evaluate_span_branches, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4428"
CLAIM_ID = "L-269"
MARKER = "PPC4161_PARENT_INFINITESIMAL_VERTICAL_ACTION_RHO_FIELD_MAP_OR_CSPECIES_FIRST_ROW_4428"
PACKET_MARKER = "PPC4161_PACKET_PARENT_INFINITESIMAL_VERTICAL_ACTION_RHO_FIELD_MAP_OR_CSPECIES_FIRST_ROW_4428"
DECISION = "RHO_DIFFEO_IS_ONLY_GAUGE_SUBDISTRIBUTION_HIDDEN_RHO_COMPONENTS_UNMAPPED_CSPECIES_ZERO_AND_BOUND_INTERFACES_STAGED"
NEXT_TARGET = "4429-Y5-R2FR-hidden-rho-internal-shift-from-parent-constraint-or-Cspecies-zero-theorem.md"

FORMAL_PATH = FORMAL / "444-PPC4161-parent-infinitesimal-vertical-action-rho-field-map-or-Cspecies-first-row.md"
DOC_PATH = POST / "4428-Y5-R2FR-parent-infinitesimal-vertical-action-rho-field-map-or-Cspecies-first-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4428_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4428_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4428_DERIVATION_ROWS.csv"
RHO_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4428_RHO_FIELD_MAP_INPUT.csv"
RHO_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4428_RHO_FIELD_MAP_OUTPUT.csv"
SPAN_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4428_RHO_SPAN_BRANCH_INPUT.csv"
SPAN_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4428_RHO_SPAN_BRANCH_OUTPUT.csv"
CSPECIES_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4428_CSPECIES_BRIDGE_INPUT.csv"
CSPECIES_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4428_CSPECIES_BRIDGE_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4428_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4428_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4428_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4428_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "rho_field_map_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4428_parent_infinitesimal_vertical_action_rho_field_map_or_Cspecies_first_row.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4427 = SOURCE_DIR / "P8_Y5_R2FR_4427_NEXT_TARGET.csv"
FORMAL_443 = FORMAL / "443-PPC4161-parent-vertical-gauge-action-span-or-first-scoreable-Csource-component.md"
DOC_4427 = POST / "4427-Y5-R2FR-parent-vertical-gauge-action-span-or-first-scoreable-Csource-component.md"
CSV_4427_SPAN = SOURCE_DIR / "P8_Y5_R2FR_4427_VERTICAL_ACTION_SPAN_OUTPUT.csv"
CSV_4427_CSPECIES = SOURCE_DIR / "P8_Y5_R2FR_4427_FIRST_CSOURCE_COMPONENT_OUTPUT.csv"

CSV_590_FIELD = SOURCE_DIR / "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv"
CSV_1038_FIELD = SOURCE_DIR / "P8_Y5_R10_1038_VERTICAL_GENERATOR_FIELD_MAP.csv"
CSV_1667_Q = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1667_QUOTIENT_MAP_AUDIT.csv"
CSV_1737_VB = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1737_VERTICAL_BASIS_CONTRACT.csv"
CSV_1737_DQM = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1737_DQ_MATRIX_REQUIREMENTS.csv"
CSV_1784_FIELD = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1784_FIELD_ACTION_PACKET.csv"
CSV_2392_CERT = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2392_VERTICAL_KERNEL_CERTIFICATE.csv"

DOC_2396 = POST / "2396-Y5-R2FR-matter-source-lift-and-no-direct-slot-proof-or-source-charge-row.md"
DOC_2399 = POST / "2399-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md"
DOC_2614 = POST / "2614-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md"
DOC_2675 = POST / "2675-Y5-R2FR-species-clock-channel-zero-or-first-bound-fill.md"
DOC_3543 = POST / "3543-Y5-R2FR-constructor-exhaustion-or-first-species-source-coefficient-fill.md"

CSV_NO_SPECIES = SOURCE_DIR / "P8_no_species_source_charge_CONTRACT.csv"
CSV_CONSTANT_UNIV = SOURCE_DIR / "P8_constant_sector_universality_CONTRACT.csv"
CSV_SOURCE_WARD = SOURCE_DIR / "P8_source_current_Ward_universality_CONTRACT.csv"
CSV_SPECIES_RESIDUAL = SOURCE_DIR / "P8_species_source_charge_residual_or_zero.csv"
CSV_OWNER_TERMS = SOURCE_DIR / "P8_source_owner_parent_action_terms_CONTRACT.csv"


def text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def rows_from(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(out)


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4428_00_4427_next", "path": NEXT_4427, "needle": "rho field map", "role": "4427 handoff to rho field-map construction."},
        {"source_id": "SRC4428_01_443_formal", "path": FORMAL_443, "needle": "Im(rho)=ker(Dq)", "role": "4427 exact action-span target."},
        {"source_id": "SRC4428_02_4427_doc", "path": DOC_4427, "needle": "parent-owned infinitesimal action rho", "role": "post-checkpoint handoff."},
        {"source_id": "SRC4428_03_4427_span", "path": CSV_4427_SPAN, "needle": "VGA4427_2_current_vertical_basis", "role": "previous span gate output."},
        {"source_id": "SRC4428_04_4427_cspecies", "path": CSV_4427_CSPECIES, "needle": "CSRC4427_0_species_current", "role": "previous C_species component output."},
        {"source_id": "SRC4428_05_590_field", "path": CSV_590_FIELD, "needle": "metric_or_coframe", "role": "early field-by-field vertical action map."},
        {"source_id": "SRC4428_06_1038_field", "path": CSV_1038_FIELD, "needle": "matter_readout_constants", "role": "Omega/DCX vertical generator field map."},
        {"source_id": "SRC4428_07_1667_q", "path": CSV_1667_Q, "needle": "QMA1667_6_verdict", "role": "quotient map audit."},
        {"source_id": "SRC4428_08_1737_vb", "path": CSV_1737_VB, "needle": "VB1737_5_vtau_readout", "role": "candidate vertical-basis requirements."},
        {"source_id": "SRC4428_09_1737_dqm", "path": CSV_1737_DQM, "needle": "DQM1737_5_Dq_total_kernel", "role": "Dq matrix requirements."},
        {"source_id": "SRC4428_10_1784_field", "path": CSV_1784_FIELD, "needle": "FAP1784_4_matter_readout_constants", "role": "current field-action packet."},
        {"source_id": "SRC4428_11_2392_cert", "path": CSV_2392_CERT, "needle": "VKC2392_0_vertical_basis", "role": "kernel certificate missing parent vertical basis."},
        {"source_id": "SRC4428_12_2396_doc", "path": DOC_2396, "needle": "MSL2396_4_no_direct_slot_zero", "role": "matter/source no-direct-slot theorem route."},
        {"source_id": "SRC4428_13_2399_doc", "path": DOC_2399, "needle": "delta_w_species=0", "role": "species-label forgetting route."},
        {"source_id": "SRC4428_14_2614_doc", "path": DOC_2614, "needle": "delta_w_species=0", "role": "later source functor forgetting theorem route."},
        {"source_id": "SRC4428_15_2675_doc", "path": DOC_2675, "needle": "P8_species_source_charge_residual_or_zero.csv", "role": "species/clock channel split and repaired species row."},
        {"source_id": "SRC4428_16_3543_doc", "path": DOC_3543, "needle": "3.330000e-03*D_mhat_source", "role": "real Ti/Pt source-coupling inequality interface."},
        {"source_id": "SRC4428_17_no_species_contract", "path": CSV_NO_SPECIES, "needle": "S2_constant_sector_universality", "role": "no species source charge sufficient clauses."},
        {"source_id": "SRC4428_18_constant_univ", "path": CSV_CONSTANT_UNIV, "needle": "C3_universal_source_variation", "role": "constant-sector universality clauses."},
        {"source_id": "SRC4428_19_source_ward", "path": CSV_SOURCE_WARD, "needle": "SC3_universal_kappa_coupling", "role": "source-current Ward universality clauses."},
        {"source_id": "SRC4428_20_species_residual", "path": CSV_SPECIES_RESIDUAL, "needle": "SSC2675_0_definition", "role": "species source-charge residual row."},
        {"source_id": "SRC4428_21_owner_terms", "path": CSV_OWNER_TERMS, "needle": "A6_selector_blind_source_action", "role": "parent source owner action terms."},
        {"source_id": "SRC4428_22_gate", "path": GATE_PATH, "needle": "def evaluate_rho_row", "role": "4428 rho gate."},
        {"source_id": "SRC4428_23_generator", "path": GENERATOR_PATH, "needle": "CHECKPOINT = \"4428\"", "role": "4428 generator."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        path = Path(spec["path"])
        needle = str(spec["needle"])
        content = text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": True if not needle else needle in content,
                "line_number": line_of(path, needle),
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "RHO4428_0_split",
            "claim": "The obvious diffeomorphism/local-Lorentz rho is a real gauge direction but only a subdistribution.",
            "derivation": "For tensorial parent fields, rho_diff(xi) is the Lie derivative plus local Lorentz compensation on coframes/spinors. If q stores diffeomorphism/local-Lorentz equivalence classes, Dq(rho_diff)=0. But rho_diff spans coordinate/frame redundancy only; it does not span hidden MTS representative directions such as Z/phi/domain/memory/projector/source-label/readout kernels.",
            "consequence": "This prevents a fake closure: GR gauge covariance is not the hidden-fibre transitivity proof.",
            "status": "EXACT_GAUGE_SUBDISTRIBUTION_RESULT",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "RHO4428_1_hidden_target",
            "claim": "The needed rho is an internal hidden representative action, not merely spacetime covariance.",
            "derivation": "A closing hidden rho must act on auxiliary/residual/domain/memory/projector variables while leaving e_obs, source/readout functors, theta markers, boundary charge and tau pushforward fixed. That means the action must be written componentwise and must satisfy Dq(rho_hid)=0 before matter/readout.",
            "consequence": "The next derivation target is rho_hid from a parent constraint/no-source symmetry, or the branch becomes finite C_species/C_readout.",
            "status": "INTERNAL_RHO_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "RHO4428_2_current_map_attempt",
            "claim": "Current field maps do not close rho_hid.",
            "derivation": "590/1038/1784 give the right field blocks but mark domain/memory/projector, matter/readout/constants, and boundary modes unmapped or not derived. 1737 keeps Dq components finite. 2392 keeps the parent vertical basis and null-kernel charge missing.",
            "consequence": "No local-GR or source-coupling pass can be promoted from rho yet.",
            "status": "HIDDEN_RHO_UNMAPPED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "RHO4428_3_Cspecies_route",
            "claim": "The C_species zero route has an exact theorem shape, but not a signed parent theorem.",
            "derivation": "If the source functor is formed from the total Hilbert/coframe current after species labels are forgotten, and no source-only weights/material markers/non-Hilbert bypasses exist, then delta_w_species=0 and C_species=DERIVED_ZERO. Existing 2399/2614/2675 sources keep this conditional; 3543 supplies a real Ti/Pt inequality for the finite branch.",
            "consequence": "If rho_hid cannot be built next, the best move is to prove this C_species zero theorem or map MTS coefficients into the 3543 inequality.",
            "status": "CSPECIES_ZERO_OR_FINITE_BOUND_INTERFACE_STAGED",
            "valid_for_claim": False,
        },
    ]


def rho_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "RHO4428_0_diff_metric_coframe",
            "branch": "rho_diff",
            "field_block": "metric_or_coframe",
            "rho_formula": "rho_diff(xi)[g]=L_xi g; rho_diff(xi)[e^a]=L_xi e^a+lambda^a_b e^b",
            "q_component": "observed geometry as diffeomorphism/local-Lorentz class",
            "parent_owned": False,
            "field_action_complete": True,
            "Dq_rho_zero": True,
            "source_readout_silent": True,
            "theta_marker_silent": True,
            "boundary_tau_silent": False,
            "contributes_to_kernel_span": False,
            "source_path": str(CSV_590_FIELD),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Standard GR gauge candidate; useful but not the hidden MTS kernel.",
        },
        {
            "row_id": "RHO4428_1_diff_matter_readout",
            "branch": "rho_diff",
            "field_block": "matter_readout_constants",
            "rho_formula": "rho_diff(xi)[psi_A]=L_xi psi_A plus representation connection; rho_diff(xi)[theta_A]=0",
            "q_component": "matter/readout naturality under coordinate/frame gauge",
            "parent_owned": False,
            "field_action_complete": True,
            "Dq_rho_zero": True,
            "source_readout_silent": False,
            "theta_marker_silent": True,
            "boundary_tau_silent": False,
            "contributes_to_kernel_span": False,
            "source_path": str(CSV_1038_FIELD),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Formal covariance is not enough; readout-after-variation and source functor descent are still unsigned.",
        },
        {
            "row_id": "RHO4428_2_hidden_Z_phi",
            "branch": "rho_hidden",
            "field_block": "Z_phi_response_block",
            "rho_formula": "rho_hid(s)[Z^A]=s^A; rho_hid(s)[phi]=s_phi; rho_hid(s)[q]=0 only if Z/phi are pure representatives or constraint-eliminated",
            "q_component": "Dq[partial_Z], Dq[partial_phi], Dsource/readout, Dtheta, Dboundary",
            "parent_owned": False,
            "field_action_complete": False,
            "Dq_rho_zero": False,
            "source_readout_silent": False,
            "theta_marker_silent": False,
            "boundary_tau_silent": False,
            "contributes_to_kernel_span": True,
            "source_path": str(CSV_1737_VB),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "This is the hidden-kernel target, but current Dq tests do not close it.",
        },
        {
            "row_id": "RHO4428_3_hidden_domain_memory_projector",
            "branch": "rho_hidden",
            "field_block": "domain_memory_projector",
            "rho_formula": "rho_hid(s)[chi_D,m,Q_coh,Pi_M,B_edge]=representative shift with q/source/readout fixed",
            "q_component": "domain/memory/projector/source-support part of q and boundary class",
            "parent_owned": False,
            "field_action_complete": False,
            "Dq_rho_zero": False,
            "source_readout_silent": False,
            "theta_marker_silent": False,
            "boundary_tau_silent": False,
            "contributes_to_kernel_span": True,
            "source_path": str(CSV_1784_FIELD),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "This is exactly where boundary/source/projector hair can re-enter.",
        },
        {
            "row_id": "RHO4428_4_hidden_Gamma_Khat_qloc",
            "branch": "rho_hidden",
            "field_block": "Gamma_Khat_qloc",
            "rho_formula": "rho_hid(s)[Gamma,Khat,q_loc]=constraint response or owner-current representative shift",
            "q_component": "q_loc and observed/source residual vector",
            "parent_owned": False,
            "field_action_complete": False,
            "Dq_rho_zero": False,
            "source_readout_silent": False,
            "theta_marker_silent": True,
            "boundary_tau_silent": False,
            "contributes_to_kernel_span": True,
            "source_path": str(CSV_1784_FIELD),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "q_loc cannot be made gauge by naming it; it needs owner-current/constraint derivation.",
        },
        {
            "row_id": "RHO4428_5_hidden_boundary_tau",
            "branch": "rho_hidden",
            "field_block": "boundary_tau_pushforward",
            "rho_formula": "rho_hid(s)[B_edge,tau,P_loc]=exact compact boundary representative plus projectable tau shift",
            "q_component": "boundary charge, source support, tau pushforward",
            "parent_owned": False,
            "field_action_complete": False,
            "Dq_rho_zero": False,
            "source_readout_silent": False,
            "theta_marker_silent": True,
            "boundary_tau_silent": False,
            "contributes_to_kernel_span": True,
            "source_path": str(CSV_2392_CERT),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Boundary/tau silence remains a hard local-GR gate.",
        },
        {
            "row_id": "RHO4428_6_species_constants",
            "branch": "rho_source",
            "field_block": "species_constants_source_functor",
            "rho_formula": "rho_source(s)[theta_A]=0 and source functor F_src({(T_A,A)})=F_src(T_total) after label forgetting",
            "q_component": "source-label and constant-sector quotient",
            "parent_owned": False,
            "field_action_complete": True,
            "Dq_rho_zero": True,
            "source_readout_silent": False,
            "theta_marker_silent": False,
            "boundary_tau_silent": True,
            "contributes_to_kernel_span": False,
            "source_path": str(CSV_NO_SPECIES),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "This is the C_species zero theorem shape, not a signed rho action.",
        },
    ]


def span_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "branch_id": "RSP4428_0_rho_diff",
            "branch_name": "diffeomorphism/local-Lorentz rho",
            "q_map_signed": True,
            "rho_components_complete": True,
            "all_Dq_zero": True,
            "im_rho_equals_kernel": False,
            "rank_bracket_integrable": True,
            "connected_fibres": True,
            "matter_readout_closed": False,
            "source_path": str(CSV_590_FIELD),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "At best this gives coordinate/frame gauge, not the whole hidden MTS kernel.",
        },
        {
            "branch_id": "RSP4428_1_rho_hidden",
            "branch_name": "internal hidden representative rho",
            "q_map_signed": True,
            "rho_components_complete": False,
            "all_Dq_zero": False,
            "im_rho_equals_kernel": False,
            "rank_bracket_integrable": False,
            "connected_fibres": False,
            "matter_readout_closed": False,
            "source_path": str(CSV_1737_VB),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "This is the needed branch; field action and Dq tests are missing.",
        },
        {
            "branch_id": "RSP4428_2_future_full_contract",
            "branch_name": "future rho_hid full closure contract",
            "q_map_signed": True,
            "rho_components_complete": True,
            "all_Dq_zero": True,
            "im_rho_equals_kernel": True,
            "rank_bracket_integrable": True,
            "connected_fibres": True,
            "matter_readout_closed": True,
            "source_path": str(FORMAL_443),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Executable theorem target only; input_valid=false prevents a claim.",
        },
    ]


def cspecies_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "CSP4428_0_Cspecies_zero_theorem",
            "route": "source_functor_label_forgetting",
            "coefficient_symbol": "C_species",
            "value": "DERIVED_ZERO",
            "units": "dimensionless_relative_source_coupling",
            "theorem_or_numeric_source": "requires parent-signed total Hilbert source owner plus no source-only weights, no material markers, no non-Hilbert bypass",
            "projection_formula": "delta_w_species=0 => epsilon_species_A-epsilon_species_B=0",
            "source_path": str(DOC_2614),
            "independent_of_bound": True,
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Clean route, deliberately nonclaim until the parent source functor theorem is signed.",
        },
        {
            "row_id": "CSP4428_1_Cspecies_real_bound_interface",
            "route": "TiPt_two_charge_bound",
            "coefficient_symbol": "C_species",
            "value": "BOUND_ONLY: |3.330000e-03*D_mhat_source + 2.040000e-03*D_e_source| <= 2.8e-15",
            "units": "dimensionless",
            "theorem_or_numeric_source": "3543 source-backed Ti/Pt inequality; MTS coefficient map missing",
            "projection_formula": "Delta_epsilon_TiPt = 3.330000e-03*D_mhat_source + 2.040000e-03*D_e_source",
            "source_path": str(DOC_3543),
            "independent_of_bound": False,
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Real numerical target for finite route, not a prediction until MTS maps into D_mhat_source,D_e_source.",
        },
        {
            "row_id": "CSP4428_2_species_residual_row",
            "route": "epsilon_species_A_residual",
            "coefficient_symbol": "epsilon_species_A",
            "value": "MISSING_PARENT_ZERO_OR_NUMERIC_EPSILON_A",
            "units": "dimensionless",
            "theorem_or_numeric_source": "P8_species_source_charge_residual_or_zero.csv",
            "projection_formula": "epsilon_species_A := partial_A ln(mu_obs/M_inertial)",
            "source_path": str(CSV_SPECIES_RESIDUAL),
            "independent_of_bound": False,
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Retained residual if zero theorem fails.",
        },
    ]


def claim_gate_rows(rho: Sequence[Mapping[str, str]], span: Sequence[Mapping[str, str]], cspecies: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    rho_rows = {row["row_id"]: row for row in rho}
    span_rows = {row["branch_id"]: row for row in span}
    c_rows = {row["row_id"]: row for row in cspecies}
    no_claims = (
        not any(row.get("valid_for_claim") == "True" for row in rho)
        and not any(row.get("valid_for_claim") == "True" for row in span)
        and not any(row.get("valid_for_claim") == "True" for row in cspecies)
    )
    return [
        {"gate_id": "CG4428_0_rho_diff_subdistribution", "claim": "ordinary diffeo/local-Lorentz rho is only a gauge subdistribution", "passed": span_rows["RSP4428_0_rho_diff"].get("current_status") == "RHO_GAUGE_SUBDISTRIBUTION_ONLY", "valid_for_claim": False, "detail": "it does not span hidden MTS kernel directions."},
        {"gate_id": "CG4428_1_hidden_rho_missing", "claim": "internal hidden rho components remain unmapped", "passed": span_rows["RSP4428_1_rho_hidden"].get("current_status") == "RHO_SPAN_TARGET_COMPONENTS_MISSING", "valid_for_claim": False, "detail": "Z/phi/domain/memory/projector/boundary/tau/source components are not closed."},
        {"gate_id": "CG4428_2_future_contract", "claim": "future full rho closure row is executable but nonclaim", "passed": span_rows["RSP4428_2_future_full_contract"].get("current_status") == "RHO_SPAN_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "input_valid=false blocks promotion."},
        {"gate_id": "CG4428_3_species_zero_staged", "claim": "C_species DERIVED_ZERO route is staged but parent theorem unsigned", "passed": c_rows["CSP4428_0_Cspecies_zero_theorem"].get("current_status") == "CSPECIES_INPUT_INVALID_NONCLAIM", "valid_for_claim": False, "detail": "exact route exists; source functor theorem not signed."},
        {"gate_id": "CG4428_4_real_bound_interface", "claim": "real Ti/Pt bound interface is preserved without treating it as MTS prediction", "passed": c_rows["CSP4428_1_Cspecies_real_bound_interface"].get("current_status") == "CSPECIES_BOUND_INTERFACE_ONLY", "valid_for_claim": False, "detail": "3543 inequality is a finite target, not a parent coefficient."},
        {"gate_id": "CG4428_5_source_component_risk", "claim": "species/source row remains explicitly retained", "passed": rho_rows["RHO4428_6_species_constants"].get("current_status") == "RHO_COMPONENT_FORMAL_DQ_ZERO_PARENT_UNSIGNED", "valid_for_claim": False, "detail": "source/readout and theta-marker silence are unsigned."},
        {"gate_id": "CG4428_6_no_claim_outputs", "claim": "4428 emits no local-GR/WEP/PPN/R10 claim", "passed": no_claims, "valid_for_claim": False, "detail": "all outputs remain private nonclaim rows."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4428_0",
            "decision": DECISION,
            "summary": "4428 separates the easy gauge action from the hard hidden action. The diffeomorphism/local-Lorentz rho is legitimate as a coordinate/frame gauge subdistribution, but it cannot span the hidden MTS kernel. The required internal rho_hid must act on Z/phi/domain/memory/projector/Gamma-Khat/boundary/tau while keeping q, source/readout, theta markers and compact charges fixed. Existing maps do not supply that. The fallback is now sharper: either prove C_species=DERIVED_ZERO from label-forgetting/total-Hilbert-source ownership, or map MTS coefficients into the real 3543 Ti/Pt inequality.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4428_0_best_result", "status": "RHO_DIFFEO_ONLY_GAUGE_SUBDISTRIBUTION", "detail": "Standard covariance is useful but does not span hidden MTS representative directions.", "valid_for_claim": False},
        {"status_id": "STAT4428_1_open_derivation", "status": "RHO_HIDDEN_INTERNAL_SHIFT_UNMAPPED", "detail": "Internal Z/phi/domain/memory/projector/boundary/tau/source action remains the next theorem target.", "valid_for_claim": False},
        {"status_id": "STAT4428_2_fallback", "status": "CSPECIES_ZERO_OR_TIPT_BOUND_INTERFACE_STAGED", "detail": "C_species has a theorem-zero route and a real finite Ti/Pt inequality target, both nonclaim.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4428_0",
            "target": NEXT_TARGET,
            "objective": "Construct the internal hidden rho_hid as a parent constraint/representative shift, or prove C_species=DERIVED_ZERO from source-label forgetting.",
            "derive_first": "try rho_hid(s)[Z,phi,chi_D,m,Pi_M,Gamma,Khat,B_edge,tau] with e_obs/source/readout/theta/boundary charge fixed, then test Dq(rho_hid)=0 and Im(rho_hid)=hidden kernel.",
            "fallback": "prove the parent total-Hilbert-source/no-source-weight theorem for C_species=DERIVED_ZERO, or map MTS coefficients into the 3543 Ti/Pt D_mhat/D_e inequality.",
            "avoid": "pretending diffeomorphism gauge spans hidden MTS fibres; leaving boundary/tau/source/readout components implicit; converting a bound into a parent coefficient.",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], rho: Sequence[Mapping[str, str]], span: Sequence[Mapping[str, str]], cspecies: Sequence[Mapping[str, str]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 444 PPC4161 parent infinitesimal vertical action rho field map or C_species first row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4428 is the anti-smuggling checkpoint:

- The standard diffeomorphism/local-Lorentz `rho_diff` is a real gauge direction, but only a subdistribution.
- It cannot honestly span hidden MTS fibres involving `Z`, `phi`, domain/memory/projector, `Gamma/Khat/q_loc`, boundary, tau, source labels, or readout.
- The missing object is an internal `rho_hid` with `Dq(rho_hid)=0` componentwise and `Im(rho_hid)=ker(Dq)` for the hidden kernel.
- The finite coupling fallback is no longer foggy: `C_species=DERIVED_ZERO` needs a source-label-forgetting theorem; otherwise 3543 supplies a real Ti/Pt inequality target.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Rho Field Map Gate

{table(rho)}

## Rho Span Branch Gate

{table(span)}

## C_species Bridge

{table(cspecies)}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4428 - parent infinitesimal vertical action rho field map or C_species first row

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Wrote an explicit `rho` field-map split instead of just saying "missing action".
- Proved the useful negative/positive result: `rho_diff` is genuine gauge structure, but only a subdistribution, not the hidden MTS kernel.
- Identified the exact missing object: internal `rho_hid` acting on hidden/residual/projector/source-support fields while keeping observed/source/readout data fixed.
- Staged both `C_species=DERIVED_ZERO` and the real 3543 Ti/Pt inequality as nonclaim fallback interfaces.

## Decision

{table(decision_rows())}

## Next target

{table(next_rows())}
"""


def upsert_marked_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"
    block = f"{start}\n{section.rstrip()}\n{end}\n"
    if start in existing and end in existing:
        before = existing.split(start)[0]
        after = existing.split(end, 1)[1].lstrip("\n")
        write_text(path, before + block + after)
    else:
        sep = "" if existing.endswith("\n") or not existing else "\n"
        write_text(path, existing + sep + block)


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH) if CLAIMS_PATH.exists() else []
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    rows = [row for row in rows if row.get("claim_id") != CLAIM_ID]
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "4428 writes the parent infinitesimal action rho field-map split. The standard diffeomorphism/local-Lorentz rho is a legitimate gauge subdistribution but does not span hidden MTS kernels. The needed internal rho_hid on Z/phi/domain/memory/projector/Gamma-Khat/boundary/tau/source sectors remains unmapped. C_species is staged with both a DERIVED_ZERO source-label-forgetting theorem route and the real 3543 Ti/Pt finite inequality interface, neither claim-ready.",
        "current_evidence": "4428 source register, derivation rows, rho field map output, rho span branch output, C_species bridge output, claim gates, decision, status, next target and validation CSV.",
        "status": "rho_diff_gauge_subdistribution_hidden_rho_unmapped_cspecies_zero_and_bound_interfaces_staged",
        "next_test": "Construct rho_hid field-by-field and test Dq(rho_hid)=0/Im(rho_hid)=hidden kernel, or prove C_species=DERIVED_ZERO from source-label forgetting.",
        "key_risk": "Pretending diffeomorphism gauge spans hidden MTS fibres; hiding boundary/tau/source/readout leakage; converting empirical bounds into parent coefficients.",
        "sector": "local_gr",
        "evidence": "4428 source register, derivation rows, rho field map output, rho span branch output, C_species bridge output, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Construct rho_hid field-by-field and test Dq(rho_hid)=0/Im(rho_hid)=hidden kernel, or prove C_species=DERIVED_ZERO from source-label forgetting.",
        "risk": "Pretending diffeomorphism gauge spans hidden MTS fibres; hiding boundary/tau/source/readout leakage; converting empirical bounds into parent coefficients.",
    }
    rows.append({name: new_row.get(name, "") for name in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = """## 4428 local spine update: rho_diff is not enough

4428 writes the field-map split that had been implicit. Ordinary diffeomorphism/local-Lorentz gauge supplies a real `rho_diff`, but it only spans coordinate/frame redundancy. The hidden local-GR route needs a separate internal `rho_hid` acting on residual/projector/domain/memory/source-support variables while leaving observed geometry, source/readout, constants, boundary charge and tau pushforward fixed. If that cannot be derived, the coupling branch falls to `C_species`: either source-label forgetting gives `DERIVED_ZERO`, or the 3543 Ti/Pt inequality becomes the finite target.
"""
    packet_section = f"""## 4428 packet update: internal rho or C_species

`{PACKET_MARKER}`

Private packet result: we did not confuse GR gauge with the MTS hidden kernel. The next leap is `rho_hid`, not another covariance pass. If `rho_hid` fails, attack `C_species` via total Hilbert source ownership and source-label forgetting.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    rho = {row["row_id"]: row for row in rows_from(RHO_OUTPUT)}
    span = {row["branch_id"]: row for row in rows_from(SPAN_OUTPUT)}
    cspecies = {row["row_id"]: row for row in rows_from(CSPECIES_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = (
        not any(row.get("valid_for_claim") == "True" for row in rho.values())
        and not any(row.get("valid_for_claim") == "True" for row in span.values())
        and not any(row.get("valid_for_claim") == "True" for row in cspecies.values())
    )
    checks = [
        ("VAL4428_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4428_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4428_2_rho_diff_subdistribution", span["RSP4428_0_rho_diff"].get("current_status") == "RHO_GAUGE_SUBDISTRIBUTION_ONLY", "rho_diff is only a gauge subdistribution"),
        ("VAL4428_3_hidden_rho_missing", span["RSP4428_1_rho_hidden"].get("current_status") == "RHO_SPAN_TARGET_COMPONENTS_MISSING", "internal hidden rho remains missing"),
        ("VAL4428_4_future_contract", span["RSP4428_2_future_full_contract"].get("current_status") == "RHO_SPAN_CONTRACT_READY_NONCLAIM", "future full rho contract remains nonclaim"),
        ("VAL4428_5_Z_phi_open", rho["RHO4428_2_hidden_Z_phi"].get("current_status") == "RHO_COMPONENT_ACTION_INCOMPLETE", "Z/phi hidden rho component remains unmapped"),
        ("VAL4428_6_species_source_unsigned", rho["RHO4428_6_species_constants"].get("current_status") == "RHO_COMPONENT_FORMAL_DQ_ZERO_PARENT_UNSIGNED", "species source branch is formal-only"),
        ("VAL4428_7_Cspecies_zero_nonclaim", cspecies["CSP4428_0_Cspecies_zero_theorem"].get("current_status") == "CSPECIES_INPUT_INVALID_NONCLAIM", "C_species zero route is staged nonclaim"),
        ("VAL4428_8_TiPt_bound_interface", cspecies["CSP4428_1_Cspecies_real_bound_interface"].get("current_status") == "CSPECIES_BOUND_INTERFACE_ONLY", "real Ti/Pt finite bound interface preserved"),
        ("VAL4428_9_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4428_10_claim_gate_no_claim", any(row["gate_id"] == "CG4428_6_no_claim_outputs" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4428_11_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-269"),
        ("VAL4428_12_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4428_13_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4428_14_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4428_15_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4428_16_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4428_17_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(RHO_INPUT, rho_input_rows())
    write_csv(RHO_OUTPUT, evaluate_rho_rows(RHO_INPUT))
    write_csv(SPAN_INPUT, span_input_rows())
    write_csv(SPAN_OUTPUT, evaluate_span_branches(SPAN_INPUT))
    write_csv(CSPECIES_INPUT, cspecies_input_rows())
    write_csv(CSPECIES_OUTPUT, evaluate_cspecies_rows(CSPECIES_INPUT))
    rho = rows_from(RHO_OUTPUT)
    span = rows_from(SPAN_OUTPUT)
    cspecies = rows_from(CSPECIES_OUTPUT)
    gates = claim_gate_rows(rho, span, cspecies)
    write_csv(CLAIM_GATES, gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), rho, span, cspecies, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()

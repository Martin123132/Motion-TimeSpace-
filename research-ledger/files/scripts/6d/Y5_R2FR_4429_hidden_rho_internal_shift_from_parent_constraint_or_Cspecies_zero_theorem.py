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

from hidden_rho_constraint_cspecies_gate import (  # noqa: E402
    evaluate_bound_map_rows,
    evaluate_cspecies_zero_rows,
    evaluate_hidden_rho_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4429"
CLAIM_ID = "L-270"
MARKER = "PPC4161_HIDDEN_RHO_INTERNAL_SHIFT_FROM_PARENT_CONSTRAINT_OR_CSPECIES_ZERO_THEOREM_4429"
PACKET_MARKER = "PPC4161_PACKET_HIDDEN_RHO_INTERNAL_SHIFT_FROM_PARENT_CONSTRAINT_OR_CSPECIES_ZERO_THEOREM_4429"
DECISION = "HIDDEN_RHO_FIRST_CLASS_OR_AUXILIARY_ROUTE_EXACT_BUT_NOT_PARENT_OWNED_CSPECIES_COLLAPSES_TO_SHADOW_NONHILBERT_RESIDUALS"
NEXT_TARGET = "4430-Y5-R2FR-total-Hilbert-source-owner-no-source-weight-signature-or-TiPt-DD-map.md"

FORMAL_PATH = FORMAL / "445-PPC4161-hidden-rho-internal-shift-from-parent-constraint-or-Cspecies-zero-theorem.md"
DOC_PATH = POST / "4429-Y5-R2FR-hidden-rho-internal-shift-from-parent-constraint-or-Cspecies-zero-theorem.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4429_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4429_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4429_DERIVATION_ROWS.csv"
RHO_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4429_HIDDEN_RHO_CONSTRAINT_INPUT.csv"
RHO_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4429_HIDDEN_RHO_CONSTRAINT_OUTPUT.csv"
CSPECIES_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4429_CSPECIES_ZERO_INPUT.csv"
CSPECIES_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4429_CSPECIES_ZERO_OUTPUT.csv"
RESIDUAL_DECOMPOSITION = SOURCE_DIR / "P8_Y5_R2FR_4429_CSPECIES_RESIDUAL_DECOMPOSITION.csv"
BOUND_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4429_TIPT_BOUND_MAP_INPUT.csv"
BOUND_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4429_TIPT_BOUND_MAP_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4429_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4429_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4429_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4429_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "hidden_rho_constraint_cspecies_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4429_hidden_rho_internal_shift_from_parent_constraint_or_Cspecies_zero_theorem.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4428 = SOURCE_DIR / "P8_Y5_R2FR_4428_NEXT_TARGET.csv"
FORMAL_444 = FORMAL / "444-PPC4161-parent-infinitesimal-vertical-action-rho-field-map-or-Cspecies-first-row.md"
DOC_4428 = POST / "4428-Y5-R2FR-parent-infinitesimal-vertical-action-rho-field-map-or-Cspecies-first-row.md"
CSV_4428_RHO = SOURCE_DIR / "P8_Y5_R2FR_4428_RHO_FIELD_MAP_OUTPUT.csv"
CSV_4428_CSPECIES = SOURCE_DIR / "P8_Y5_R2FR_4428_CSPECIES_BRIDGE_OUTPUT.csv"

CSV_FCC1555 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1555_FIRST_CLASS_CONSTRAINT_CONTRACT.csv"
CSV_GAUGE1555 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1555_GAUGE_NOETHER_ROUTE_AUDIT.csv"
CSV_CLASS1562 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1562_CONSTRAINT_CLASS_GATE.csv"
CSV_CFA1668 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1668_CONSTRAINT_FIRST_ACTION_ATTEMPT.csv"
CSV_CFD1675 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1675_CONSTRAINT_FIRST_DESCENT_THEOREM_ATTEMPT.csv"
CSV_CET2628 = SOURCE_DIR / "P8_Y5_CONSTRAINT_ELIMINATION_2628_CONSTRAINT_ELIMINATION_THEOREM_GATE.csv"

DOC_2614 = POST / "2614-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md"
DOC_3543 = POST / "3543-Y5-R2FR-constructor-exhaustion-or-first-species-source-coefficient-fill.md"
CSV_SLF1603 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1603_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv"
CSV_LF1764 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1764_LABEL_FORGETTING_PROOF_ATTEMPT.csv"
CSV_NSP1765 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1765_NO_SOURCE_PREFACTOR_PROOF_ATTEMPT.csv"
CSV_THO1765 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1765_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv"
CSV_SF2613 = SOURCE_DIR / "P8_Y5_HOM_EXCLUSION_GATE_2613_LABEL_FORGETTING_SOURCE_FUNCTOR_AUDIT.csv"
CSV_NO_SPECIES = SOURCE_DIR / "P8_no_species_source_charge_CONTRACT.csv"
CSV_SPECIES_RESIDUAL = SOURCE_DIR / "P8_species_source_charge_residual_or_zero.csv"


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
        {"source_id": "SRC4429_00_4428_next", "path": NEXT_4428, "needle": "rho_hid", "role": "4428 handoff."},
        {"source_id": "SRC4429_01_444_formal", "path": FORMAL_444, "needle": "RHO4428_1_hidden_target", "role": "4428 hidden rho target."},
        {"source_id": "SRC4429_02_4428_doc", "path": DOC_4428, "needle": "internal `rho_hid`", "role": "4428 post doc."},
        {"source_id": "SRC4429_03_4428_rho", "path": CSV_4428_RHO, "needle": "RHO4428_2_hidden_Z_phi", "role": "rho field map output."},
        {"source_id": "SRC4429_04_4428_cspecies", "path": CSV_4428_CSPECIES, "needle": "CSP4428_0_Cspecies_zero_theorem", "role": "C_species bridge output."},
        {"source_id": "SRC4429_05_fcc1555", "path": CSV_FCC1555, "needle": "FCC1555_4_bracket_closure", "role": "first-class constraint requirements."},
        {"source_id": "SRC4429_06_gauge1555", "path": CSV_GAUGE1555, "needle": "GAUGE1555_4_first_class_constraint", "role": "gauge/Noether route audit."},
        {"source_id": "SRC4429_07_class1562", "path": CSV_CLASS1562, "needle": "CLASS1562_5_second_class", "role": "first-class vs auxiliary route."},
        {"source_id": "SRC4429_08_cfa1668", "path": CSV_CFA1668, "needle": "CFA1668_8_verdict", "role": "constraint-first action attempt."},
        {"source_id": "SRC4429_09_cfd1675", "path": CSV_CFD1675, "needle": "CFD1675_6_verdict", "role": "constraint-first descent theorem attempt."},
        {"source_id": "SRC4429_10_cet2628", "path": CSV_CET2628, "needle": "CET2628_4_current_branch_verdict", "role": "general constraint-elimination theorem."},
        {"source_id": "SRC4429_11_slf1603", "path": CSV_SLF1603, "needle": "SLF1603_5_verdict", "role": "source-label forgetting status."},
        {"source_id": "SRC4429_12_lf1764", "path": CSV_LF1764, "needle": "LF1764_1_conditional_theorem", "role": "label-forgotten source theorem."},
        {"source_id": "SRC4429_13_nsp1765", "path": CSV_NSP1765, "needle": "NSP1765_2_exchange_filter", "role": "exchange filter for source weights."},
        {"source_id": "SRC4429_14_tho1765", "path": CSV_THO1765, "needle": "THO1765_4_owner_verdict", "role": "total Hilbert source owner."},
        {"source_id": "SRC4429_15_sf2613", "path": CSV_SF2613, "needle": "SF2613_0_label_forgetting", "role": "source functor label-forgetting audit."},
        {"source_id": "SRC4429_16_doc2614", "path": DOC_2614, "needle": "LF2614_1_conditional_theorem", "role": "2614 species-zero attempt."},
        {"source_id": "SRC4429_17_no_species", "path": CSV_NO_SPECIES, "needle": "S4_source_normalization_species_blind", "role": "no species source charge contract."},
        {"source_id": "SRC4429_18_species_residual", "path": CSV_SPECIES_RESIDUAL, "needle": "SSC2675_0_definition", "role": "species residual row."},
        {"source_id": "SRC4429_19_doc3543", "path": DOC_3543, "needle": "3.330000e-03*D_mhat_source", "role": "real Ti/Pt source-coupling inequality."},
        {"source_id": "SRC4429_20_gate", "path": GATE_PATH, "needle": "def evaluate_hidden_rho_row", "role": "4429 gate script."},
        {"source_id": "SRC4429_21_generator", "path": GENERATOR_PATH, "needle": "CHECKPOINT = \"4429\"", "role": "4429 generator."},
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
            "derivation_id": "HRHO4429_0_first_class_theorem",
            "claim": "A hidden internal rho can be generated by a parent first-class constraint only if the generator is differentiable, charge-silent, bracket-closed and spans the hidden kernel.",
            "derivation": "Let C_I(Phi)=0 be parent-owned constraints and G[epsilon]=int epsilon^I C_I+Q_epsilon. If delta G=i_{rho_epsilon} Omega, {G_epsilon,G_eta}=G_[epsilon,eta] with no anomaly, Q_epsilon is zero/proper on the compact local branch, and q/matter/readout are basic with respect to rho_epsilon, then Dq(rho_epsilon)=0 and Im(rho)=ker(Dq)_hidden after reduction.",
            "consequence": "This is the mathematically clean rho_hid route, but it demands the parent phase-space objects the current corpus still lacks.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "HRHO4429_1_auxiliary_elimination_theorem",
            "claim": "Second-class/algebraic auxiliary elimination can replace rho_hid if hidden variables are solved before q/readout.",
            "derivation": "If E_Lambda=C_X=0 and E_X solve X=Xbar(Q_vis) locally with no nonlocal tail, stress hair, boundary flux or readout re-entry, then variations tangent to the reduced surface have no independent X direction and Dq_X=0 by elimination rather than gauge.",
            "consequence": "For local-GR reduction this may be less fragile than first-class gauge, but the parent solve/no-tail clauses are unsigned.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "HRHO4429_2_current_verdict",
            "claim": "Current MTS does not close first-class rho_hid or auxiliary elimination.",
            "derivation": "1555/1562/1668/1675/2628 consistently show missing parent phase space, constraint origin, generator, bracket/degree count, boundary charge/no-tail, q factorization and matter/source/readout descent.",
            "consequence": "No hidden-rho local-GR pass is claimable from current evidence.",
            "status": "HIDDEN_RHO_ROUTE_EXACT_BUT_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "CSP4429_0_species_zero_theorem",
            "claim": "C_species is DERIVED_ZERO if source labels are forgotten before source coupling and no shadow source route reintroduces them.",
            "derivation": "Let S_m=sum_A S_A+S_int and T_total=delta S_m/delta e_obs be the only ordinary active-source object. If F_src has domain T_total rather than labelled pairs {(T_A,A)}, no source-only weights w_A exist, hidden/material/readout markers cannot feed F_src, non-Hilbert bypasses are excluded, and the remaining common factor is calibrated once, then relative species coupling is not an allowed argument: C_species=0.",
            "consequence": "This is a genuine zero theorem shape for calibrated source coupling.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "CSP4429_1_partial_collapse",
            "claim": "Even without full C_species=0, exchange/Ward structure shrinks the danger from arbitrary species weights to shadow/non-Hilbert/block residuals.",
            "derivation": "The 1765 exchange filter says relative source weights across interacting sectors collapse to a common factor on connected exchange components. Common factors are calibration, not WEP. Thus the retained species residual can be written as delta_w_species = delta_w_block + delta_w_shadow + delta_w_nonHilbert + delta_w_marker/readout.",
            "consequence": "This is not a pass, but it is a real squeeze on the coupling wall.",
            "status": "PARTIAL_DERIVATION_REDUCES_RESIDUAL_SPACE",
            "valid_for_claim": False,
        },
    ]


def hidden_rho_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "HRHO4429_0_first_class_full_contract",
            "sector": "hidden_internal_rho",
            "hidden_variable": "Z/phi/domain/memory/projector/Gamma-Khat/boundary-tau",
            "parent_phase_space_declared": True,
            "constraint_or_aux_equation_declared": True,
            "constraint_origin_parent_owned": True,
            "generator_or_solve_declared": True,
            "first_class_or_auxiliary_closed": True,
            "zero_boundary_charge_or_no_tail": True,
            "Dq_after_elimination_zero": True,
            "matter_readout_descends": True,
            "source_species_silent": True,
            "kernel_span_or_eliminated": True,
            "source_path": str(CSV_CET2628),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Pure theorem target, not current evidence.",
        },
        {
            "row_id": "HRHO4429_1_current_first_class",
            "sector": "first_class_constraint",
            "hidden_variable": "R_AB/Z/phi residual pair",
            "parent_phase_space_declared": False,
            "constraint_or_aux_equation_declared": False,
            "constraint_origin_parent_owned": False,
            "generator_or_solve_declared": False,
            "first_class_or_auxiliary_closed": False,
            "zero_boundary_charge_or_no_tail": False,
            "Dq_after_elimination_zero": False,
            "matter_readout_descends": False,
            "source_species_silent": False,
            "kernel_span_or_eliminated": False,
            "source_path": str(CSV_FCC1555),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "1555 keeps all required first-class objects missing.",
        },
        {
            "row_id": "HRHO4429_2_current_auxiliary_route",
            "sector": "second_class_auxiliary_elimination",
            "hidden_variable": "R_AB/Z auxiliary branch",
            "parent_phase_space_declared": True,
            "constraint_or_aux_equation_declared": True,
            "constraint_origin_parent_owned": False,
            "generator_or_solve_declared": False,
            "first_class_or_auxiliary_closed": False,
            "zero_boundary_charge_or_no_tail": False,
            "Dq_after_elimination_zero": False,
            "matter_readout_descends": False,
            "source_species_silent": False,
            "kernel_span_or_eliminated": False,
            "source_path": str(CSV_CLASS1562),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Auxiliary route is better conditional route but parent origin/solve/no-tail not signed.",
        },
        {
            "row_id": "HRHO4429_3_constraint_first_action",
            "sector": "constraint_first_action_attempt",
            "hidden_variable": "Z/phi/R_AB before q/readout",
            "parent_phase_space_declared": True,
            "constraint_or_aux_equation_declared": True,
            "constraint_origin_parent_owned": False,
            "generator_or_solve_declared": False,
            "first_class_or_auxiliary_closed": False,
            "zero_boundary_charge_or_no_tail": False,
            "Dq_after_elimination_zero": False,
            "matter_readout_descends": False,
            "source_species_silent": False,
            "kernel_span_or_eliminated": False,
            "source_path": str(CSV_CFA1668),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "1668 rejects magic multipliers and leaves constraint origin unsigned.",
        },
        {
            "row_id": "HRHO4429_4_constraint_descent",
            "sector": "Dq_zero_by_constraint_descent",
            "hidden_variable": "Z local residual",
            "parent_phase_space_declared": True,
            "constraint_or_aux_equation_declared": True,
            "constraint_origin_parent_owned": False,
            "generator_or_solve_declared": False,
            "first_class_or_auxiliary_closed": False,
            "zero_boundary_charge_or_no_tail": False,
            "Dq_after_elimination_zero": False,
            "matter_readout_descends": False,
            "source_species_silent": False,
            "kernel_span_or_eliminated": False,
            "source_path": str(CSV_CFD1675),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Descent theorem shape is exact but q factorization and readout descent are missing.",
        },
    ]


def cspecies_zero_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "CSZ4429_0_full_zero_contract",
            "theorem_piece": "full source-label forgetting zero theorem",
            "total_hilbert_owner": True,
            "source_domain_label_forgotten": True,
            "no_source_only_weights": True,
            "no_hidden_marker_return": True,
            "nonhilbert_bypass_excluded": True,
            "exchange_connected_or_common": True,
            "common_calibration_only": True,
            "source_path": str(DOC_2614),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Pure C_species=DERIVED_ZERO theorem target.",
        },
        {
            "row_id": "CSZ4429_1_current_label_forgetting",
            "theorem_piece": "current source functor label forgetting",
            "total_hilbert_owner": False,
            "source_domain_label_forgotten": True,
            "no_source_only_weights": False,
            "no_hidden_marker_return": False,
            "nonhilbert_bypass_excluded": False,
            "exchange_connected_or_common": False,
            "common_calibration_only": True,
            "source_path": str(CSV_SF2613),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Label-forgotten domain is clean, but parent source functor is unsigned and shadow returns remain.",
        },
        {
            "row_id": "CSZ4429_2_exchange_collapse",
            "theorem_piece": "exchange-connected ordinary sectors collapse relative weights",
            "total_hilbert_owner": True,
            "source_domain_label_forgotten": False,
            "no_source_only_weights": True,
            "no_hidden_marker_return": False,
            "nonhilbert_bypass_excluded": False,
            "exchange_connected_or_common": True,
            "common_calibration_only": True,
            "source_path": str(CSV_NSP1765),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Partial derivation: arbitrary species weights reduce to block/shadow/non-Hilbert residuals.",
        },
        {
            "row_id": "CSZ4429_3_total_hilbert_owner",
            "theorem_piece": "total Hilbert source owner",
            "total_hilbert_owner": True,
            "source_domain_label_forgotten": False,
            "no_source_only_weights": False,
            "no_hidden_marker_return": False,
            "nonhilbert_bypass_excluded": False,
            "exchange_connected_or_common": True,
            "common_calibration_only": True,
            "source_path": str(CSV_THO1765),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Owner clause is clean as a contract, but source-shadow and non-Hilbert bypass still live.",
        },
    ]


def residual_decomposition_rows() -> List[Dict[str, object]]:
    return [
        {"term_id": "CSD4429_0_total", "symbol": "C_species", "meaning": "relative active source coupling from species/material labels", "status": "RETAINED_NONCLAIM", "formula_piece": "C_species = C_block + C_shadow + C_nonHilbert + C_marker_readout", "valid_for_claim": False},
        {"term_id": "CSD4429_1_block", "symbol": "C_block", "meaning": "disconnected conserved exchange-block source weight", "status": "COLLAPSES_TO_COMMON_IF_EXCHANGE_GRAPH_CONNECTED", "formula_piece": "C_block=0 if all ordinary sectors exchange/bind through one Hilbert current", "valid_for_claim": False},
        {"term_id": "CSD4429_2_shadow", "symbol": "C_shadow", "meaning": "separate source-shadow functional or source-only weight", "status": "LIVE_UNTIL_PARENT_GRAMMAR_EXCLUDES", "formula_piece": "not exists S_source=sum_A w_A S_A outside S_matter", "valid_for_claim": False},
        {"term_id": "CSD4429_3_nonHilbert", "symbol": "C_nonHilbert", "meaning": "active source current not equal to total Hilbert/coframe derivative", "status": "LIVE_UNTIL_NO_NONHILBERT_BYPASS", "formula_piece": "J_src = kappa T_Hilbert + J_NH; require J_NH=0", "valid_for_claim": False},
        {"term_id": "CSD4429_4_marker_readout", "symbol": "C_marker_readout", "meaning": "hidden/material/readout marker re-entry into source coefficient", "status": "LIVE_UNTIL_NO_HIDDEN_RETURN", "formula_piece": "partial_marker F_src=partial_hidden F_src=partial_readout F_src=0", "valid_for_claim": False},
    ]


def bound_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "TBM4429_0_real_TiPt_interface",
            "coefficient": "D_mhat_source,D_e_source",
            "value": "BOUND_ONLY: |3.330000e-03*D_mhat_source + 2.040000e-03*D_e_source| <= 2.8e-15",
            "units": "dimensionless",
            "projection_formula": "Delta_epsilon_TiPt = 3.330000e-03*D_mhat_source + 2.040000e-03*D_e_source",
            "source_path": str(DOC_3543),
            "mts_coefficient_map_present": False,
            "source_leg_present": False,
            "independent_of_bound": False,
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Real bound target, not an MTS prediction.",
        },
        {
            "row_id": "TBM4429_1_zero_theorem_projection",
            "coefficient": "D_mhat_source,D_e_source",
            "value": "DERIVED_ZERO",
            "units": "dimensionless",
            "projection_formula": "C_species=0 => D_mhat_source=D_e_source=0 in source-label-forgetting branch",
            "source_path": str(DOC_2614),
            "mts_coefficient_map_present": True,
            "source_leg_present": True,
            "independent_of_bound": True,
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Allowed future zero projection; input-invalid until the C_species theorem is parent-signed.",
        },
    ]


def claim_gate_rows(rho: Sequence[Mapping[str, str]], cspecies: Sequence[Mapping[str, str]], bounds: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    rho_rows = {row["row_id"]: row for row in rho}
    c_rows = {row["row_id"]: row for row in cspecies}
    b_rows = {row["row_id"]: row for row in bounds}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in rho) and not any(row.get("valid_for_claim") == "True" for row in cspecies) and not any(row.get("valid_for_claim") == "True" for row in bounds)
    return [
        {"gate_id": "CG4429_0_hidden_rho_contract", "claim": "full first-class/auxiliary hidden-rho theorem staged as exact nonclaim", "passed": rho_rows["HRHO4429_0_first_class_full_contract"].get("current_status") == "HIDDEN_RHO_CONSTRAINT_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "the route is exact but not current evidence."},
        {"gate_id": "CG4429_1_current_first_class_blocked", "claim": "current corpus does not own first-class hidden rho", "passed": rho_rows["HRHO4429_1_current_first_class"].get("current_status") == "HIDDEN_RHO_CONSTRAINT_BLOCKED_BY_CURRENT_CORPUS", "valid_for_claim": False, "detail": "1555 keeps parent phase space/generator/brackets/charge missing."},
        {"gate_id": "CG4429_2_auxiliary_unsigned", "claim": "auxiliary route is partial and unsigned", "passed": rho_rows["HRHO4429_2_current_auxiliary_route"].get("current_status") == "HIDDEN_RHO_CONSTRAINT_ORIGIN_UNSIGNED", "valid_for_claim": False, "detail": "second-class route needs parent origin, solve and no-tail proof."},
        {"gate_id": "CG4429_3_Cspecies_zero_contract", "claim": "C_species=DERIVED_ZERO theorem staged", "passed": c_rows["CSZ4429_0_full_zero_contract"].get("current_status") == "CSPECIES_ZERO_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "exact theorem target remains input-invalid."},
        {"gate_id": "CG4429_4_partial_collapse", "claim": "species coupling shrinks to block/shadow/non-Hilbert/marker residuals", "passed": c_rows["CSZ4429_2_exchange_collapse"].get("current_status") == "CSPECIES_COLLAPSES_TO_SHADOW_AND_NONHILBERT_RESIDUALS", "valid_for_claim": False, "detail": "this is the real progress in calibrated source coupling."},
        {"gate_id": "CG4429_5_TiPt_interface", "claim": "real Ti/Pt bound interface remains non-prediction until MTS map exists", "passed": b_rows["TBM4429_0_real_TiPt_interface"].get("current_status") == "CSPECIES_BOUND_INTERFACE_MTS_MAP_MISSING", "valid_for_claim": False, "detail": "bound is preserved without inverting it into theory."},
        {"gate_id": "CG4429_6_no_claim_outputs", "claim": "4429 emits no local-GR/WEP/PPN/R10 claim", "passed": no_claims, "valid_for_claim": False, "detail": "all outputs remain private nonclaim rows."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4429_0",
            "decision": DECISION,
            "summary": "4429 took the actual derivation swing. The hidden-rho route is exact if MTS supplies either a differentiable first-class generator with zero/proper compact charge and bracket closure, or a local auxiliary elimination with no tail before q/readout. Current files do not supply those parent objects. The source-coupling route did improve: C_species has an exact DERIVED_ZERO theorem shape, and even before full zero the exchange/Ward filter collapses arbitrary species weights into a smaller residual vector: block, shadow source, non-Hilbert bypass, and marker/readout return.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4429_0_hidden_rho", "status": "FIRST_CLASS_OR_AUXILIARY_RHO_ROUTE_EXACT_UNSIGNED", "detail": "Need parent phase space, generator/solve, charge/no-tail, bracket/degree, Dq and matter/readout descent.", "valid_for_claim": False},
        {"status_id": "STAT4429_1_cspecies", "status": "CSPECIES_ZERO_THEOREM_EXACT_PARENT_SIGNATURE_UNSIGNED", "detail": "Zero follows from total Hilbert source owner plus source-label forgetting and no shadow returns.", "valid_for_claim": False},
        {"status_id": "STAT4429_2_partial_gain", "status": "SPECIES_RESIDUAL_REDUCED_TO_BLOCK_SHADOW_NONHILBERT_MARKER_VECTOR", "detail": "Arbitrary species weights are no longer the right finite object.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4429_0",
            "target": NEXT_TARGET,
            "objective": "Prove the total Hilbert source owner/no-source-weight signature that makes C_species=DERIVED_ZERO, or map MTS coefficients into the Ti/Pt D_mhat/D_e inequality.",
            "derive_first": "show ordinary active source is only T_total=delta S_matter/delta e_obs, source functor domain is T_total not labelled pairs, no source-shadow w_A slot exists, and non-Hilbert/marker/readout returns vanish.",
            "fallback": "build the finite coefficient map from MTS source-coupling objects into D_mhat_source and D_e_source for the 3543 Ti/Pt inequality.",
            "avoid": "claiming hidden rho without parent generator/solve; treating common calibration as WEP; converting MICROSCOPE bound into an MTS coefficient.",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], rho: Sequence[Mapping[str, str]], cspecies: Sequence[Mapping[str, str]], bounds: Sequence[Mapping[str, str]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 445 PPC4161 hidden rho internal shift from parent constraint or C_species zero theorem

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4429 makes two concrete moves:

- Hidden `rho_hid` can close only through a real parent first-class generator or a real auxiliary elimination before `q` and readout. The theorem is exact, but current MTS does not own the required generator/solve.
- `C_species=DERIVED_ZERO` has a clean calibrated-source theorem: total Hilbert source owner, label-forgotten source domain, no source-only weights, no hidden/material/readout return, no non-Hilbert bypass, and common calibration only.
- The useful partial result is stronger than “missing coupling”: arbitrary species weights collapse to a smaller residual vector `C_block + C_shadow + C_nonHilbert + C_marker_readout`.
- The 3543 Ti/Pt inequality remains the real finite bound interface, not a prediction until MTS coefficients map into `D_mhat_source,D_e_source`.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Hidden Rho Constraint Gate

{table(rho)}

## C_species Zero Gate

{table(cspecies)}

## C_species Residual Decomposition

{table(residual_decomposition_rows())}

## Ti/Pt Bound Map Gate

{table(bounds)}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4429 - hidden rho internal shift from parent constraint or C_species zero theorem

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Tried the internal `rho_hid` route as a first-class/auxiliary parent constraint theorem, not as a label.
- Kept it nonclaim because the parent generator/solve, boundary/no-tail, brackets and descent evidence are still absent.
- Strengthened the calibrated-source side: `C_species=DERIVED_ZERO` has an exact parent signature, and partial Ward/exchange logic reduces the residual vector.
- Kept the 3543 Ti/Pt bound as a real finite target without converting it into an MTS coefficient.

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
        "claim": "4429 proves exact conditional routes for hidden rho_hid via first-class generator or auxiliary elimination, but current MTS lacks parent-owned generator/solve, boundary/no-tail, bracket/degree and descent evidence. It also sharpens C_species: DERIVED_ZERO follows from total Hilbert source owner, source-label forgetting, no source-only weights, no hidden/material/readout return, no non-Hilbert bypass and common calibration only. Current evidence gives a partial collapse to block/shadow/non-Hilbert/marker residuals plus the 3543 Ti/Pt finite interface.",
        "current_evidence": "4429 source register, derivation rows, hidden rho constraint output, C_species zero output, residual decomposition, Ti/Pt bound map output, claim gates, decision, status, next target and validation CSV.",
        "status": "hidden_rho_constraint_exact_unsigned_cspecies_zero_exact_partial_residual_collapse",
        "next_test": "Prove total Hilbert source owner/no-source-weight signature for C_species=DERIVED_ZERO, or map MTS coefficients into D_mhat_source/D_e_source.",
        "key_risk": "Claiming hidden rho without a parent generator/solve; treating common calibration as WEP; converting MICROSCOPE bounds into MTS coefficients.",
        "sector": "local_gr",
        "evidence": "4429 source register, derivation rows, hidden rho constraint output, C_species zero output, residual decomposition, Ti/Pt bound map output, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Prove total Hilbert source owner/no-source-weight signature for C_species=DERIVED_ZERO, or map MTS coefficients into D_mhat_source/D_e_source.",
        "risk": "Claiming hidden rho without a parent generator/solve; treating common calibration as WEP; converting MICROSCOPE bounds into MTS coefficients.",
    }
    rows.append({name: new_row.get(name, "") for name in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = """## 4429 local spine update: hidden rho or calibrated source zero

4429 tries the internal hidden-rho route properly. It can close only if a parent first-class generator or local auxiliary elimination is actually owned before `q` and readout; current MTS does not yet provide that object. The better immediate source-coupling advance is `C_species`: the exact zero theorem is now total Hilbert source owner + label-forgotten source domain + no source-only weights + no hidden/material/readout return + no non-Hilbert bypass. Even before full zero, arbitrary species weights collapse to `C_block + C_shadow + C_nonHilbert + C_marker_readout`.
"""
    packet_section = f"""## 4429 packet update: residual vector shrunk

`{PACKET_MARKER}`

Private packet result: hidden `rho_hid` remains unsigned, but the coupling wall moved. `C_species` is no longer a vague danger; it is a four-piece residual vector unless the total-Hilbert-source/no-source-weight theorem closes.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    rho = {row["row_id"]: row for row in rows_from(RHO_OUTPUT)}
    cspecies = {row["row_id"]: row for row in rows_from(CSPECIES_OUTPUT)}
    bounds = {row["row_id"]: row for row in rows_from(BOUND_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in rho.values()) and not any(row.get("valid_for_claim") == "True" for row in cspecies.values()) and not any(row.get("valid_for_claim") == "True" for row in bounds.values())
    checks = [
        ("VAL4429_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4429_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4429_2_hidden_rho_contract", rho["HRHO4429_0_first_class_full_contract"].get("current_status") == "HIDDEN_RHO_CONSTRAINT_CONTRACT_READY_NONCLAIM", "full hidden-rho theorem contract is staged"),
        ("VAL4429_3_current_first_class_blocked", rho["HRHO4429_1_current_first_class"].get("current_status") == "HIDDEN_RHO_CONSTRAINT_BLOCKED_BY_CURRENT_CORPUS", "current first-class route is blocked"),
        ("VAL4429_4_auxiliary_unsigned", rho["HRHO4429_2_current_auxiliary_route"].get("current_status") == "HIDDEN_RHO_CONSTRAINT_ORIGIN_UNSIGNED", "auxiliary route is partial and unsigned"),
        ("VAL4429_5_cspecies_zero_contract", cspecies["CSZ4429_0_full_zero_contract"].get("current_status") == "CSPECIES_ZERO_CONTRACT_READY_NONCLAIM", "C_species zero theorem staged"),
        ("VAL4429_6_partial_collapse", cspecies["CSZ4429_2_exchange_collapse"].get("current_status") == "CSPECIES_COLLAPSES_TO_SHADOW_AND_NONHILBERT_RESIDUALS", "partial residual collapse captured"),
        ("VAL4429_7_residual_decomposition", len(rows_from(RESIDUAL_DECOMPOSITION)) == 5 and "C_shadow" in text(RESIDUAL_DECOMPOSITION), "C_species residual decomposition written"),
        ("VAL4429_8_TiPt_interface", bounds["TBM4429_0_real_TiPt_interface"].get("current_status") == "CSPECIES_BOUND_INTERFACE_MTS_MAP_MISSING", "Ti/Pt bound interface preserved as nonprediction"),
        ("VAL4429_9_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4429_10_claim_gate_no_claim", any(row["gate_id"] == "CG4429_6_no_claim_outputs" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4429_11_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-270"),
        ("VAL4429_12_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4429_13_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4429_14_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4429_15_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4429_16_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4429_17_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(RHO_INPUT, hidden_rho_input_rows())
    write_csv(RHO_OUTPUT, evaluate_hidden_rho_rows(RHO_INPUT))
    write_csv(CSPECIES_INPUT, cspecies_zero_input_rows())
    write_csv(CSPECIES_OUTPUT, evaluate_cspecies_zero_rows(CSPECIES_INPUT))
    write_csv(RESIDUAL_DECOMPOSITION, residual_decomposition_rows())
    write_csv(BOUND_INPUT, bound_input_rows())
    write_csv(BOUND_OUTPUT, evaluate_bound_map_rows(BOUND_INPUT))
    rho = rows_from(RHO_OUTPUT)
    cspecies = rows_from(CSPECIES_OUTPUT)
    bounds = rows_from(BOUND_OUTPUT)
    gates = claim_gate_rows(rho, cspecies, bounds)
    write_csv(CLAIM_GATES, gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), rho, cspecies, bounds, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()

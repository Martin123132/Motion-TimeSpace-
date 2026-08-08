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

from vertical_gauge_action_span_gate import evaluate_component_rows, evaluate_span_rows, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4427"
CLAIM_ID = "L-268"
MARKER = "PPC4161_PARENT_VERTICAL_GAUGE_ACTION_SPAN_OR_FIRST_SCOREABLE_CSOURCE_COMPONENT_4427"
PACKET_MARKER = "PPC4161_PACKET_PARENT_VERTICAL_GAUGE_ACTION_SPAN_OR_FIRST_SCOREABLE_CSOURCE_COMPONENT_4427"
DECISION = "VERTICAL_ACTION_SPAN_THEOREM_EXACT_BUT_PARENT_RHO_AND_IM_RHO_EQUALS_KER_DQ_UNSIGNED_CSPECIES_FIRST_COMPONENT_CONTRACT_STAGED"
NEXT_TARGET = "4428-Y5-R2FR-parent-infinitesimal-vertical-action-rho-field-map-or-Cspecies-first-row.md"

FORMAL_PATH = FORMAL / "443-PPC4161-parent-vertical-gauge-action-span-or-first-scoreable-Csource-component.md"
DOC_PATH = POST / "4427-Y5-R2FR-parent-vertical-gauge-action-span-or-first-scoreable-Csource-component.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4427_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4427_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4427_DERIVATION_ROWS.csv"
SPAN_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4427_VERTICAL_ACTION_SPAN_INPUT.csv"
SPAN_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4427_VERTICAL_ACTION_SPAN_OUTPUT.csv"
COMPONENT_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4427_FIRST_CSOURCE_COMPONENT_INPUT.csv"
COMPONENT_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4427_FIRST_CSOURCE_COMPONENT_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4427_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4427_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4427_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4427_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "vertical_gauge_action_span_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4427_parent_vertical_gauge_action_span_or_first_scoreable_Csource_component.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4426 = SOURCE_DIR / "P8_Y5_R2FR_4426_NEXT_TARGET.csv"
FORMAL_442 = FORMAL / "442-PPC4161-hidden-invariant-triviality-transitive-fibre-proof-or-first-finite-Csource-vector.md"
DOC_4426 = POST / "4426-Y5-R2FR-hidden-invariant-triviality-transitive-fibre-proof-or-first-finite-Csource-vector.md"
DOC_1541 = POST / "1541-Y5-quotient-map-vertical-generator-kernel-certificate.md"
DOC_1667 = POST / "1667-Y5-R2FR-parent-field-chart-and-quotient-map-Dq-on-Zphi-or-retained-Dq-leak.md"
DOC_1737 = POST / "1737-Y5-R2FR-q-map-Dq-vertical-basis-source-row-or-coframe-functor-zero.md"
DOC_1784 = POST / "1784-Y5-R2FR-parent-Omega-DCX-vertical-action-packet-or-DqZ-geometry-row.md"
DOC_2392 = POST / "2392-Y5-R2FR-vertical-kernel-presymplectic-null-and-matter-invisible-or-kernel-charge-row.md"

CSV_1667_CHART = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1667_PARENT_FIELD_CHART_CANDIDATE.csv"
CSV_1667_Q = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1667_QUOTIENT_MAP_AUDIT.csv"
CSV_1667_DQ = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv"
CSV_1737_VB = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1737_VERTICAL_BASIS_CONTRACT.csv"
CSV_1737_DQM = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1737_DQ_MATRIX_REQUIREMENTS.csv"
CSV_1784_PACKET = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1784_OMEGA_DCX_VERTICAL_PACKET_GATE.csv"
CSV_1784_FIELD = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1784_FIELD_ACTION_PACKET.csv"
CSV_2392_CERT = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2392_VERTICAL_KERNEL_CERTIFICATE.csv"
CSV_2392_THEOREM = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2392_VERTICAL_KERNEL_NULLNESS_THEOREM.csv"
CSV_4426_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4426_SURVIVING_GENERATOR_CSOURCE_VECTOR.csv"
CSV_4426_VECTOR_OUT = SOURCE_DIR / "P8_Y5_R2FR_4426_CSOURCE_VECTOR_OUTPUT.csv"


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
        {"source_id": "SRC4427_00_4426_next", "path": NEXT_4426, "needle": "4427-Y5-R2FR-parent-vertical-gauge-action-span-or-first-scoreable-Csource-component.md", "role": "4426 handoff to the parent action/span gate."},
        {"source_id": "SRC4427_01_442_formal", "path": FORMAL_442, "needle": "connected hidden fibre that is one transitive parent gauge", "role": "4426 transitive-fibre lemma needing a span proof."},
        {"source_id": "SRC4427_02_4426_doc", "path": DOC_4426, "needle": "vertical gauge action/span", "role": "post-checkpoint handoff."},
        {"source_id": "SRC4427_03_1541_doc", "path": DOC_1541, "needle": "KERNEL_NOT_PROVED", "role": "older Dq[v_m] kernel certificate failure."},
        {"source_id": "SRC4427_04_1667_doc", "path": DOC_1667, "needle": "FIELD_CHART_CANDIDATE_NOT_PARENT_SIGNED", "role": "parent field chart and q/Dq status."},
        {"source_id": "SRC4427_05_1737_doc", "path": DOC_1737, "needle": "DQ_KERNEL_UNSIGNED_RETAIN_FINITE_ROWS", "role": "q-map, Dq and vertical basis source rows."},
        {"source_id": "SRC4427_06_1784_doc", "path": DOC_1784, "needle": "PARENT_OMEGA_DCX_VERTICAL_PACKET_NOT_SIGNED", "role": "Omega/DCX vertical-action packet remains formal."},
        {"source_id": "SRC4427_07_2392_doc", "path": DOC_2392, "needle": "MISSING_PARENT_VERTICAL_BASIS", "role": "kernel nullness certificate failure."},
        {"source_id": "SRC4427_08_1667_chart", "path": CSV_1667_CHART, "needle": "PFC1667_7_chart_verdict", "role": "candidate parent field chart."},
        {"source_id": "SRC4427_09_1667_q", "path": CSV_1667_Q, "needle": "QMA1667_6_verdict", "role": "quotient map audit."},
        {"source_id": "SRC4427_10_1667_dq", "path": CSV_1667_DQ, "needle": "DQT1667_6_verdict", "role": "Dq tests not closed."},
        {"source_id": "SRC4427_11_1737_vb", "path": CSV_1737_VB, "needle": "VB1737_5_vtau_readout", "role": "candidate vertical basis list."},
        {"source_id": "SRC4427_12_1737_dq_matrix", "path": CSV_1737_DQM, "needle": "DQM1737_5_Dq_total_kernel", "role": "Dq matrix requirements."},
        {"source_id": "SRC4427_13_1784_packet", "path": CSV_1784_PACKET, "needle": "ODP1784_8_verdict", "role": "parent Omega/DCX packet gate."},
        {"source_id": "SRC4427_14_1784_field", "path": CSV_1784_FIELD, "needle": "FAP1784_4_matter_readout_constants", "role": "field-by-field vertical action packet."},
        {"source_id": "SRC4427_15_2392_cert", "path": CSV_2392_CERT, "needle": "VKC2392_0_vertical_basis", "role": "kernel certificate missing parent vertical basis."},
        {"source_id": "SRC4427_16_2392_theorem", "path": CSV_2392_THEOREM, "needle": "VKN2392_5_verdict", "role": "kernel-nullness theorem contract."},
        {"source_id": "SRC4427_17_4426_vector", "path": CSV_4426_VECTOR, "needle": "C_species", "role": "surviving C_source vector component list."},
        {"source_id": "SRC4427_18_4426_vector_output", "path": CSV_4426_VECTOR_OUT, "needle": "CSVIN4426_5_species", "role": "previous component gate output for species constants."},
        {"source_id": "SRC4427_19_gate", "path": GATE_PATH, "needle": "def evaluate_span_row", "role": "4427 action-span gate."},
        {"source_id": "SRC4427_20_generator", "path": GENERATOR_PATH, "needle": "CHECKPOINT = \"4427\"", "role": "4427 generator."},
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
            "derivation_id": "VGA4427_0_span_theorem",
            "claim": "A parent vertical action whose infinitesimal image equals ker(Dq) supplies the transitive-fibre proof demanded by 4426.",
            "derivation": "Let q:M_parent->Q_obs be a regular quotient chart and let rho:Lie(G_vert)->T M_parent be a parent infinitesimal action. If Dq(rho(xi))=0 for all xi and Im(rho)_Phi=ker(Dq)_Phi, then the action distribution equals the vertical distribution. If the distribution is integrable and each local fibre is connected, every point in q^{-1}(q0) lies on the same G_vert orbit. The 4426 lemma then gives O(q^{-1}(q0))^G=R for admissible hidden scalars.",
            "consequence": "This is the exact bridge from local q/Dq geometry to hidden-invariant triviality.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "VGA4427_1_current_gap",
            "claim": "Current MTS has q/chart/basis fragments, not a parent-owned rho field map with Im(rho)=ker(Dq).",
            "derivation": "1667 gives a field-chart candidate, 1737 gives candidate vertical basis requirements, 1784 gives a formal Omega/DCX-to-generator packet, and 2392 gives the null-kernel certificate. All four retain missing parent action, field-by-field map, rank/bracket, matter/readout and boundary clauses.",
            "consequence": "The transitive-fibre theorem is stronger than the current corpus evidence.",
            "status": "PARENT_RHO_AND_SPAN_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "VGA4427_2_no_smuggling_rule",
            "claim": "Do not call candidate vertical directions gauge unless rho and Dq(rho)=0 are written componentwise.",
            "derivation": "A named vertical basis can still change source/readout, material markers, boundary projectors or tau pushforward. Therefore the action/span proof must include q, e_obs/source/readout/theta, boundary/projector and tau components.",
            "consequence": "The next derivation must write the actual infinitesimal action map, not another label audit.",
            "status": "COMPONENTWISE_RHO_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "VGA4427_3_first_component_choice",
            "claim": "If the parent action span cannot be signed yet, the first finite source component to attack is C_species.",
            "derivation": "C_species is the cleanest coupling bottleneck because it connects species constants/source labels to WEP, clocks, R10 and source-mass projections. A zero requires a parent universality/no-marker theorem; a finite value requires real parent coefficient rows, not comparator bounds.",
            "consequence": "The fallback now has a first target rather than a seven-way fog bank.",
            "status": "CSPECIES_FIRST_ROW_STAGED_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def span_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "VGA4427_0_exact_span_theorem",
            "clause": "future parent vertical action span theorem",
            "q_map_declared": True,
            "field_chart_declared": True,
            "vertical_distribution_declared": True,
            "generator_list_declared": True,
            "parent_action_declared": True,
            "infinitesimal_action_map_declared": True,
            "Dq_generator_zero": True,
            "span_equals_kernel": True,
            "integrability_connected_fibre": True,
            "matter_readout_invariant": True,
            "source_path": str(FORMAL_442),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Pure theorem target. input_valid=false because it is not yet signed by a parent MTS action.",
        },
        {
            "row_id": "VGA4427_1_current_field_chart_dq",
            "clause": "current q/chart/Dq evidence",
            "q_map_declared": True,
            "field_chart_declared": True,
            "vertical_distribution_declared": True,
            "generator_list_declared": False,
            "parent_action_declared": False,
            "infinitesimal_action_map_declared": False,
            "Dq_generator_zero": False,
            "span_equals_kernel": False,
            "integrability_connected_fibre": False,
            "matter_readout_invariant": False,
            "source_path": str(CSV_1667_CHART),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "1667/1737 provide useful chart and Dq language, but not a generator action/span proof.",
        },
        {
            "row_id": "VGA4427_2_current_vertical_basis",
            "clause": "candidate vertical basis without parent action",
            "q_map_declared": True,
            "field_chart_declared": True,
            "vertical_distribution_declared": True,
            "generator_list_declared": True,
            "parent_action_declared": False,
            "infinitesimal_action_map_declared": False,
            "Dq_generator_zero": False,
            "span_equals_kernel": False,
            "integrability_connected_fibre": False,
            "matter_readout_invariant": False,
            "source_path": str(CSV_1737_VB),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "The list exists as requirements, but each vector still lacks componentwise Dq zero and matter/readout silence.",
        },
        {
            "row_id": "VGA4427_3_omega_dcx_packet",
            "clause": "Omega/DCX-to-vertical-generator packet",
            "q_map_declared": True,
            "field_chart_declared": True,
            "vertical_distribution_declared": True,
            "generator_list_declared": True,
            "parent_action_declared": False,
            "infinitesimal_action_map_declared": True,
            "Dq_generator_zero": False,
            "span_equals_kernel": False,
            "integrability_connected_fibre": False,
            "matter_readout_invariant": False,
            "source_path": str(CSV_1784_PACKET),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "1784 has the right covector/vector shape, but no parent Omega inverse or field-by-field generator certificate.",
        },
        {
            "row_id": "VGA4427_4_kernel_null_certificate",
            "clause": "presymplectic-null and matter-invisible kernel certificate",
            "q_map_declared": True,
            "field_chart_declared": True,
            "vertical_distribution_declared": True,
            "generator_list_declared": False,
            "parent_action_declared": False,
            "infinitesimal_action_map_declared": False,
            "Dq_generator_zero": False,
            "span_equals_kernel": False,
            "integrability_connected_fibre": False,
            "matter_readout_invariant": False,
            "source_path": str(CSV_2392_CERT),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "2392 gives the right null-kernel certificate but all parent extraction rows remain missing.",
        },
        {
            "row_id": "VGA4427_5_future_full_contract",
            "clause": "full future MTS parent action/span closure",
            "q_map_declared": True,
            "field_chart_declared": True,
            "vertical_distribution_declared": True,
            "generator_list_declared": True,
            "parent_action_declared": True,
            "infinitesimal_action_map_declared": True,
            "Dq_generator_zero": True,
            "span_equals_kernel": True,
            "integrability_connected_fibre": True,
            "matter_readout_invariant": True,
            "source_path": str(CSV_2392_THEOREM),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Executable closure row only. It cannot claim until the actual parent rho map and kernel equality are sourced.",
        },
    ]


def component_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "CSRC4427_0_species_current",
            "component": "species_charge_constants",
            "coefficient_symbol": "C_species",
            "value": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "units": "MISSING_PARENT_UNITS",
            "parent_variation_basis": "MISSING_SPECIES_CURRENT_BASIS",
            "observable_projection": "WEP_clock_R10_source_mass_projection_required",
            "source_path": str(CSV_4426_VECTOR),
            "empirical_anchor": "MISSING_PARENT_THEOREM_OR_NUMERIC_ROW",
            "independent_of_bound": False,
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "First finite component selected because the coupling fork is the current bottleneck.",
        },
        {
            "row_id": "CSRC4427_1_species_zero_contract",
            "component": "species_charge_constants",
            "coefficient_symbol": "C_species",
            "value": "DERIVED_ZERO",
            "units": "dimensionless_relative_source_coupling",
            "parent_variation_basis": "parent_species_current_universality_basis_required",
            "observable_projection": "WEP_clock_R10_source_mass_projection",
            "source_path": str(CSV_4426_VECTOR_OUT),
            "empirical_anchor": "parent_no_marker_universality_theorem_required",
            "independent_of_bound": True,
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "This is the clean proof target, deliberately input-invalid until the parent theorem is actually written.",
        },
        {
            "row_id": "CSRC4427_2_readout_risk",
            "component": "readout_projector",
            "coefficient_symbol": "C_readout",
            "value": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "units": "MISSING_PARENT_UNITS",
            "parent_variation_basis": "MISSING_READOUT_AFTER_VARIATION_BASIS",
            "observable_projection": "measured_G_PPN_clock_WEP_projection_required",
            "source_path": str(CSV_4426_VECTOR),
            "empirical_anchor": "MISSING_READOUT_FUNCTOR_THEOREM_OR_NUMERIC_ROW",
            "independent_of_bound": False,
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Kept as the shadow danger behind C_species; not the first component unless species closes.",
        },
    ]


def claim_gate_rows(span: Sequence[Mapping[str, str]], components: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    span_rows = {row["row_id"]: row for row in span}
    component_rows = {row["row_id"]: row for row in components}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in span) and not any(row.get("valid_for_claim") == "True" for row in components)
    return [
        {"gate_id": "CG4427_0_exact_span_theorem", "claim": "parent action with Im(rho)=ker(Dq) closes the 4426 transitive-fibre route", "passed": span_rows["VGA4427_0_exact_span_theorem"].get("current_status") == "VERTICAL_ACTION_SPAN_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "exact theorem staged; not current evidence."},
        {"gate_id": "CG4427_1_current_chart_unsigned", "claim": "current q/chart evidence is a signed vertical action proof", "passed": span_rows["VGA4427_1_current_field_chart_dq"].get("current_status") == "FIELD_CHART_DQ_READY_ACTION_UNSIGNED", "valid_for_claim": False, "detail": "chart/Dq language exists but generator/action/span is absent."},
        {"gate_id": "CG4427_2_basis_unsigned", "claim": "candidate vertical basis is a parent action spanning the kernel", "passed": span_rows["VGA4427_2_current_vertical_basis"].get("current_status") == "GENERATOR_LIST_READY_ACTION_UNSIGNED", "valid_for_claim": False, "detail": "basis list survives as requirements, not a signed rho map."},
        {"gate_id": "CG4427_3_future_contract", "claim": "future full closure row is executable but nonclaim", "passed": span_rows["VGA4427_5_future_full_contract"].get("current_status") == "VERTICAL_ACTION_SPAN_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "input_valid=false prevents promotion."},
        {"gate_id": "CG4427_4_Cspecies_selected", "claim": "C_species is selected as the first finite component", "passed": component_rows["CSRC4427_0_species_current"].get("current_status") == "FIRST_CSOURCE_COMPONENT_CONTRACT_ONLY", "valid_for_claim": False, "detail": "selected, but value/units/basis/source theorem are missing."},
        {"gate_id": "CG4427_5_no_claim_outputs", "claim": "4427 emits no local-GR/WEP/PPN/R10 claim", "passed": no_claims, "valid_for_claim": False, "detail": "all outputs remain private nonclaim rows."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4427_0",
            "decision": DECISION,
            "summary": "4427 does make a real forward move: it reduces the 4426 hidden-triviality problem to one exact parent-action condition, Im(rho)=ker(Dq), plus connected/integrable fibres and matter/readout invariance. The present corpus has q/chart/basis/Omega-DCX/null-kernel fragments, but not the parent-owned infinitesimal action rho or a componentwise Dq(rho)=0 and span proof. The fallback is narrowed to the first coupling component C_species rather than a generic missing-coupling cloud.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4427_0_best_result", "status": "VERTICAL_ACTION_SPAN_THEOREM_EXACT", "detail": "If rho is parent-owned and Im(rho)=ker(Dq), 4426 transitive-fibre triviality follows.", "valid_for_claim": False},
        {"status_id": "STAT4427_1_current_gap", "status": "PARENT_RHO_FIELD_MAP_AND_SPAN_EQUALITY_UNSIGNED", "detail": "Existing files provide chart/basis/packet requirements but not the parent action map.", "valid_for_claim": False},
        {"status_id": "STAT4427_2_fallback", "status": "CSPECIES_FIRST_COMPONENT_STAGED_NONCLAIM", "detail": "First finite component is now C_species, requiring universality/no-marker theorem or real numeric coefficient.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4427_0",
            "target": NEXT_TARGET,
            "objective": "Write the actual parent infinitesimal vertical action rho field map and test Dq(rho)=0 componentwise, or fill the first C_species coefficient row.",
            "derive_first": "define rho(xi)[Phi] on metric/coframe, Gamma/Khat/q_loc, domain/memory/projector, matter/constants/readout and boundary modes; then test Dq(rho)=0 and Im(rho)=ker(Dq).",
            "fallback": "fill C_species with DERIVED_ZERO from a parent universality/no-marker theorem, or a numeric/source-backed finite coefficient independent of comparator bounds.",
            "avoid": "renaming a candidate basis as a gauge action; omitting source/readout/theta/boundary/tau components; using WEP/R10 bounds as parent coefficients.",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], span: Sequence[Mapping[str, str]], components: Sequence[Mapping[str, str]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 443 PPC4161 parent vertical gauge action span or first scoreable C_source component

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4427 pushes the local-GR route one rung forward:

- Exact theorem: if a parent infinitesimal vertical action `rho` satisfies `Dq(rho(xi))=0` and `Im(rho)=ker(Dq)` on connected regular fibres, the 4426 transitive-fibre lemma follows.
- Current MTS has useful fragments (`q`, field chart, vertical-basis requirements, Omega/DCX packet, kernel-null certificate), but no parent-owned `rho` map or span equality.
- The first finite fallback component is now `C_species`, because that is the coupling/source-label place where WEP, clocks, R10 and source mass all meet.
- No local-GR, Newton, WEP, PPN, R10, clock, orbital or public claim is made.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Vertical Action Span Gate

{table(span)}

## First C_source Component Gate

{table(components)}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4427 - parent vertical gauge action span or first scoreable C_source component

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Derived the exact action-span theorem needed to make the 4426 transitive-fibre route real.
- Refused promotion because the current corpus has no parent-owned `rho` with `Dq(rho)=0` and `Im(rho)=ker(Dq)`.
- Narrowed the finite coupling fallback to `C_species` first, with `C_readout` kept as the immediate shadow-risk.
- Selected 4428 as the actual field-map hunt rather than another missingness loop.

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
        "claim": "4427 derives the exact parent vertical-action span theorem needed by the hidden-triviality route: a parent infinitesimal action rho with Dq(rho)=0, Im(rho)=ker(Dq), connected/integrable fibres and matter/readout invariance would close the 4426 transitive-fibre lemma. Current MTS has q/chart/basis/Omega-DCX/null-kernel fragments but not the parent-owned rho map or span equality. The finite fallback is narrowed to the first component C_species.",
        "current_evidence": "4427 source register, derivation rows, vertical action span output, first C_source component output, claim gates, decision, status, next target and validation CSV.",
        "status": "vertical_action_span_theorem_exact_parent_rho_and_span_unsigned_cspecies_first_component_staged",
        "next_test": "Write rho field-by-field and test Dq(rho)=0 plus Im(rho)=ker(Dq), or fill C_species with DERIVED_ZERO/numeric parent provenance.",
        "key_risk": "Renaming a candidate vertical basis as a gauge action; omitting source/readout/theta/boundary/tau components; importing comparator bounds as parent coefficients.",
        "sector": "local_gr",
        "evidence": "4427 source register, derivation rows, vertical action span output, first C_source component output, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Write rho field-by-field and test Dq(rho)=0 plus Im(rho)=ker(Dq), or fill C_species with DERIVED_ZERO/numeric parent provenance.",
        "risk": "Renaming a candidate vertical basis as a gauge action; omitting source/readout/theta/boundary/tau components; importing comparator bounds as parent coefficients.",
    }
    rows.append({name: new_row.get(name, "") for name in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = """## 4427 local spine update: action-span theorem

4427 identifies the exact parent-object needed to make the hidden-fibre route real: an infinitesimal vertical action `rho` with `Dq(rho)=0` and `Im(rho)=ker(Dq)`. If the local fibres are connected/integrable and matter/readout are invariant, the 4426 transitive-fibre triviality theorem follows. Current MTS has fragments of the chart, basis, Omega/DCX and null-kernel certificates, but not the signed parent `rho` field map. The fallback is now focused on `C_species` first.
"""
    packet_section = f"""## 4427 packet update: parent rho or C_species

`{PACKET_MARKER}`

Private packet result: the next real leap is not another audit; it is writing `rho(xi)[Phi]` field-by-field. If that fails, the finite coupling branch starts with `C_species`, because source labels/species constants are the first place a hidden coupling can become WEP/R10/clock-visible.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    span = {row["row_id"]: row for row in rows_from(SPAN_OUTPUT)}
    components = {row["row_id"]: row for row in rows_from(COMPONENT_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in span.values()) and not any(row.get("valid_for_claim") == "True" for row in components.values())
    checks = [
        ("VAL4427_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4427_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4427_2_exact_span_theorem", span["VGA4427_0_exact_span_theorem"].get("current_status") == "VERTICAL_ACTION_SPAN_CONTRACT_READY_NONCLAIM", "exact action-span theorem staged as nonclaim"),
        ("VAL4427_3_current_chart_unsigned", span["VGA4427_1_current_field_chart_dq"].get("current_status") == "FIELD_CHART_DQ_READY_ACTION_UNSIGNED", "current q/chart evidence lacks generator/action/span"),
        ("VAL4427_4_basis_unsigned", span["VGA4427_2_current_vertical_basis"].get("current_status") == "GENERATOR_LIST_READY_ACTION_UNSIGNED", "candidate vertical basis lacks parent action"),
        ("VAL4427_5_future_contract", span["VGA4427_5_future_full_contract"].get("current_status") == "VERTICAL_ACTION_SPAN_CONTRACT_READY_NONCLAIM", "future full closure row remains nonclaim"),
        ("VAL4427_6_Cspecies_selected", components["CSRC4427_0_species_current"].get("current_status") == "FIRST_CSOURCE_COMPONENT_CONTRACT_ONLY", "C_species selected as first component but not score-ready"),
        ("VAL4427_7_Cspecies_zero_contract_nonclaim", components["CSRC4427_1_species_zero_contract"].get("current_status") == "FIRST_CSOURCE_COMPONENT_INPUT_INVALID_NONCLAIM", "DERIVED_ZERO route is staged but input-invalid"),
        ("VAL4427_8_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4427_9_claim_gate_no_claim", any(row["gate_id"] == "CG4427_5_no_claim_outputs" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4427_10_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-268"),
        ("VAL4427_11_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4427_12_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4427_13_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4427_14_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4427_15_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4427_16_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(SPAN_INPUT, span_input_rows())
    write_csv(SPAN_OUTPUT, evaluate_span_rows(SPAN_INPUT))
    write_csv(COMPONENT_INPUT, component_input_rows())
    write_csv(COMPONENT_OUTPUT, evaluate_component_rows(COMPONENT_INPUT))
    span = rows_from(SPAN_OUTPUT)
    components = rows_from(COMPONENT_OUTPUT)
    gates = claim_gate_rows(span, components)
    write_csv(CLAIM_GATES, gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), span, components, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()

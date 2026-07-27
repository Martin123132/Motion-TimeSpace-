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

from hidden_fibre_transitivity_gate import evaluate_transitivity_rows, evaluate_vector_rows, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
RUN_TRIVIALITY = POST / "runs" / "20260602-064500-local-quotient-invariant-algebra-triviality-gate" / "results"

CHECKPOINT = "4426"
CLAIM_ID = "L-267"
MARKER = "PPC4161_HIDDEN_INVARIANT_TRIVIALITY_TRANSITIVE_FIBRE_PROOF_OR_FIRST_FINITE_CSOURCE_VECTOR_4426"
PACKET_MARKER = "PPC4161_PACKET_HIDDEN_INVARIANT_TRIVIALITY_TRANSITIVE_FIBRE_PROOF_OR_FIRST_FINITE_CSOURCE_VECTOR_4426"
DECISION = "TRANSITIVE_FIBRE_TRIVIALITY_THEOREM_EXACT_BUT_GAUGE_ACTION_AND_GENERATOR_ELIMINATION_UNSIGNED_CSOURCE_VECTOR_CONTRACT_STAGED"
NEXT_TARGET = "4427-Y5-R2FR-parent-vertical-gauge-action-span-or-first-scoreable-Csource-component.md"

FORMAL_PATH = FORMAL / "442-PPC4161-hidden-invariant-triviality-transitive-fibre-proof-or-first-finite-Csource-vector.md"
DOC_PATH = POST / "4426-Y5-R2FR-hidden-invariant-triviality-transitive-fibre-proof-or-first-finite-Csource-vector.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4426_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4426_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4426_DERIVATION_ROWS.csv"
TRANSITIVITY_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4426_TRANSITIVE_FIBRE_INPUT.csv"
TRANSITIVITY_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4426_TRANSITIVE_FIBRE_OUTPUT.csv"
GENERATOR_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4426_SURVIVING_GENERATOR_CSOURCE_VECTOR.csv"
CSOURCE_VECTOR_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4426_CSOURCE_VECTOR_INPUT.csv"
CSOURCE_VECTOR_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4426_CSOURCE_VECTOR_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4426_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4426_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4426_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4426_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "hidden_fibre_transitivity_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4426_hidden_invariant_triviality_transitive_fibre_proof_or_first_finite_Csource_vector.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4425 = SOURCE_DIR / "P8_Y5_R2FR_4425_NEXT_TARGET.csv"
FORMAL_441 = FORMAL / "441-PPC4161-hidden-invariant-no-extension-or-live-Cparent-WEP-import-row.md"
DOC_1092 = POST / "1092-Y5-R10-hidden-invariant-algebra-triviality-or-balpha-tau-projection.md"
DOC_1115 = POST / "1115-Y5-R10-local-invariant-algebra-triviality-or-finite-coupling-prior-widths.md"
DOC_2200 = POST / "2200-Y5-R2FR-hidden-invariant-algebra-triviality-or-PPN-vector-source-row.md"
CSV_1092_HIT = SOURCE_DIR / "P8_Y5_R10_1092_HIDDEN_INVARIANT_TRIVIALITY_ATTEMPT.csv"
CSV_1092_GEN = SOURCE_DIR / "P8_Y5_R10_1092_SURVIVING_GENERATOR_LEDGER.csv"
CSV_1092_NH = SOURCE_DIR / "P8_Y5_R10_1092_SCALAR_NOHAIR_ROUTE_AUDIT.csv"
CSV_1051_ISO = SOURCE_DIR / "P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv"
CSV_1114_NHV = SOURCE_DIR / "P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv"
CSV_1220_PTOL = SOURCE_DIR / "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv"
RUN_TRIV_CHAIN = RUN_TRIVIALITY / "triviality_chain.csv"
RUN_INV_GEN = RUN_TRIVIALITY / "invariant_generators.csv"
RUN_GATE = RUN_TRIVIALITY / "gate_results.csv"
RUN_DECISION = RUN_TRIVIALITY / "decision.csv"
CSOURCE_SEED = SOURCE_DIR / "P8_Y5_R2FR_4425_CPARENT_WEP_IMPORT_OUTPUT.csv"


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
        {"source_id": "SRC4426_00_4425_next", "path": NEXT_4425, "needle": "4426-Y5-R2FR-hidden-invariant-triviality-transitive-fibre-proof-or-first-finite-Csource-vector.md", "role": "4425 handoff."},
        {"source_id": "SRC4426_01_441_formal", "path": FORMAL_441, "needle": "O(C_hid)^inv = R", "role": "4425 exact no-extension target."},
        {"source_id": "SRC4426_02_1092_doc", "path": DOC_1092, "needle": "Current verdict", "role": "older hidden-invariant triviality attempt."},
        {"source_id": "SRC4426_03_1092_hit", "path": CSV_1092_HIT, "needle": "HIT1092_5_verdict", "role": "hidden invariant triviality not derived."},
        {"source_id": "SRC4426_04_1092_generators", "path": CSV_1092_GEN, "needle": "GEN1092_6_readout_projector", "role": "surviving generator ledger."},
        {"source_id": "SRC4426_05_1092_nohair", "path": CSV_1092_NH, "needle": "SNH1092_4_verdict", "role": "scalar no-hair input pack unsigned."},
        {"source_id": "SRC4426_06_1051_obstruction", "path": CSV_1051_ISO, "needle": "ISO1051_0_hidden_scalar_I", "role": "generic hidden scalar obstruction."},
        {"source_id": "SRC4426_07_1114_no_hidden", "path": CSV_1114_NHV, "needle": "NHV1114_6_verdict", "role": "no hidden-visible coefficient morphism not derived."},
        {"source_id": "SRC4426_08_1220_typed", "path": CSV_1220_PTOL, "needle": "PTOL1220_7_verdict", "role": "typed parent object-language signature not derived."},
        {"source_id": "SRC4426_09_run_triviality", "path": RUN_TRIV_CHAIN, "needle": "Local invariant algebra is geometry plus constants", "role": "local quotient invariant algebra target."},
        {"source_id": "SRC4426_10_run_generators", "path": RUN_INV_GEN, "needle": "finite_cell_fibre_spectrum", "role": "candidate invariant generators."},
        {"source_id": "SRC4426_11_run_gate", "path": RUN_GATE, "needle": "extra_generators_eliminated", "role": "run gate fails generator elimination."},
        {"source_id": "SRC4426_12_run_decision", "path": RUN_DECISION, "needle": "extra_generators_remaining", "role": "run decision records remaining generators."},
        {"source_id": "SRC4426_13_1115_doc", "path": DOC_1115, "needle": "Generator Kill-List", "role": "generator kill-list and finite prior widths."},
        {"source_id": "SRC4426_14_2200_doc", "path": DOC_2200, "needle": "DO_NOT_REPEAT_HIDDEN_TRIVIALITY_WITHOUT_NEW_PARENT_INPUT", "role": "older warning not to loop hidden route without new parent input."},
        {"source_id": "SRC4426_15_4425_import", "path": CSOURCE_SEED, "needle": "CPIMP4425_3_live_import_contract", "role": "current finite C_source import contract seed."},
        {"source_id": "SRC4426_16_gate", "path": GATE_PATH, "needle": "def evaluate_transitivity_row", "role": "4426 transitivity/vector gate."},
        {"source_id": "SRC4426_17_generator", "path": GENERATOR_PATH, "needle": "TRANSITIVE_FIBRE_TRIVIALITY", "role": "4426 generator."},
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
        {"derivation_id": "HFT4426_0_transitive_fibre_lemma", "claim": "A connected transitive hidden fibre has only constant smooth invariant scalars.", "derivation": "Let F_q be a connected fibre of q:Conf_parent->Q_obs and let G_vert act transitively on F_q. If admissible hidden scalars are G_vert-invariant functions I:F_q->R, then for any p1,p2 in F_q there is g with p2=g.p1, hence I(p2)=I(p1). Therefore O(F_q)^G=R on that branch.", "consequence": "This is the exact hidden-invariant triviality theorem needed by 4425.", "status": "EXACT_CONDITIONAL_THEOREM", "valid_for_claim": False},
        {"derivation_id": "HFT4426_1_coupling_consequence", "claim": "If the transitive-fibre lemma is parent-signed, source-coupling drift from hidden invariants dies.", "derivation": "Any c(I_hid) active-source coefficient is common-mode because I_hid is constant on the fibre; relative C_source components cannot be generated by hidden representative motion.", "consequence": "The no-source-only coupling route would move from typed closure toward a parent theorem.", "status": "EXACT_IF_PARENT_SIGNED", "valid_for_claim": False},
        {"derivation_id": "HFT4426_2_current_gap", "claim": "Current MTS does not prove the hidden fibre is one transitive representative orbit.", "derivation": "Existing quotient and vertical-kernel rows do not parent-sign a gauge group action spanning the whole kernel, connected regular fibres, or elimination of finite-cell/domain/memory/species/readout generators.", "consequence": "O(C_hid)^inv=R is not claimable yet.", "status": "GAUGE_ACTION_SPAN_AND_GENERATORS_UNSIGNED", "valid_for_claim": False},
        {"derivation_id": "HFT4426_3_generator_vector", "claim": "The surviving generator list can be turned into a finite C_source residual vector.", "derivation": "Each surviving invariant generator defines one possible coefficient channel C_fibre, C_domain, C_chiD, C_memory, C_time, C_species, C_readout. The local comparison branch should carry the absolute vector until each component is theorem-zero or numeric/source-backed.", "consequence": "The fallback is no longer generic missingness; it is a concrete coefficient-vector worklist.", "status": "FINITE_VECTOR_CONTRACT_STAGED", "valid_for_claim": False},
        {"derivation_id": "HFT4426_4_no_loop_rule", "claim": "Do not re-run hidden triviality without new parent input.", "derivation": "Older 1092/1115/1924/2200 passes already show triviality fails unless transitivity, no-hair/profile-zero, typed-domain, or generator-elimination evidence changes.", "consequence": "4427 should attack gauge action/span directly or score one vector component.", "status": "NEXT_ATTACK_SELECTED", "valid_for_claim": False},
    ]


def transitivity_input_rows() -> List[Dict[str, object]]:
    return [
        {"row_id": "HFT4426_0_current_q_kernel", "clause": "q-map and vertical kernel evidence", "q_map_defined": True, "vertical_distribution_defined": True, "gauge_action_parent_signed": False, "action_spans_kernel": False, "fibre_connected_regular": False, "invariant_observable_policy": False, "generator_elimination_complete": False, "radiative_readout_closure": False, "source_path": str(FORMAL_441), "input_valid": False, "valid_for_claim": False, "notes": "q-kernel language exists, but it is not yet a parent-signed transitive gauge fibre."},
        {"row_id": "HFT4426_1_exact_transitive_lemma", "clause": "connected homogeneous fibre theorem", "q_map_defined": True, "vertical_distribution_defined": True, "gauge_action_parent_signed": True, "action_spans_kernel": True, "fibre_connected_regular": True, "invariant_observable_policy": True, "generator_elimination_complete": False, "radiative_readout_closure": False, "source_path": str(CSV_1092_HIT), "input_valid": False, "valid_for_claim": False, "notes": "Pure theorem row: if the hidden fibre is a connected transitive orbit, invariant scalars are constants; generator/readout clauses still open."},
        {"row_id": "HFT4426_2_generator_debt_current", "clause": "surviving generators block triviality", "q_map_defined": True, "vertical_distribution_defined": True, "gauge_action_parent_signed": False, "action_spans_kernel": False, "fibre_connected_regular": False, "invariant_observable_policy": True, "generator_elimination_complete": False, "radiative_readout_closure": False, "source_path": str(CSV_1092_GEN), "input_valid": False, "valid_for_claim": False, "notes": "Finite cell, domain, selector, memory, species and readout generators remain live."},
        {"row_id": "HFT4426_3_nohair_alternative", "clause": "positive no-hair/profile-zero alternative", "q_map_defined": True, "vertical_distribution_defined": True, "gauge_action_parent_signed": False, "action_spans_kernel": False, "fibre_connected_regular": False, "invariant_observable_policy": True, "generator_elimination_complete": False, "radiative_readout_closure": False, "source_path": str(CSV_1092_NH), "input_valid": False, "valid_for_claim": False, "notes": "No-hair could kill scalar generators, but owner/sign/source/boundary inputs are unsigned."},
        {"row_id": "HFT4426_4_future_full_contract", "clause": "full future transitive-fibre triviality contract", "q_map_defined": True, "vertical_distribution_defined": True, "gauge_action_parent_signed": True, "action_spans_kernel": True, "fibre_connected_regular": True, "invariant_observable_policy": True, "generator_elimination_complete": True, "radiative_readout_closure": True, "source_path": str(RUN_GATE), "input_valid": False, "valid_for_claim": False, "notes": "Executable target only; input_valid=false prevents a claim."},
    ]


def generator_vector_rows() -> List[Dict[str, object]]:
    return [
        {"vector_id": "CSV4426_0_finite_cell", "generator": "finite_cell_fibre_spectrum", "coefficient_symbol": "C_fibre", "observable_links": "R10;PPN;clock;source_mass", "kill_route": "prove pure basis/gauge relabeling or universal integration-out", "finite_route": "source mass-gap/scalar-charge coefficient and range projection", "status": "SURVIVES_NONCLAIM", "valid_for_claim": False},
        {"vector_id": "CSV4426_1_domain_class", "generator": "relative_boundary_domain_class", "coefficient_symbol": "C_domain", "observable_links": "local_GR;PPN;R10;orbital", "kill_route": "derive physical local trivial class", "finite_route": "source domain-class coupling and boundary response", "status": "SURVIVES_NONCLAIM", "valid_for_claim": False},
        {"vector_id": "CSV4426_2_chiD", "generator": "domain_selector_chi_D", "coefficient_symbol": "C_chiD", "observable_links": "local_GR;R10;cosmology_split", "kill_route": "derive selector as boundary bookkeeping or fixed local branch", "finite_route": "source selector-stress/source-switch coefficient", "status": "SURVIVES_NONCLAIM", "valid_for_claim": False},
        {"vector_id": "CSV4426_3_memory", "generator": "memory_or_class_scalar", "coefficient_symbol": "C_memory", "observable_links": "clock;PPN;R10;cosmology", "kill_route": "prove local value and gradient silence", "finite_route": "source memory-gradient coefficient and local profile", "status": "SURVIVES_NONCLAIM", "valid_for_claim": False},
        {"vector_id": "CSV4426_4_time_arrow", "generator": "orientation_time_arrow", "coefficient_symbol": "C_time", "observable_links": "preferred_frame;clock;PPN", "kill_route": "show contained in observed coframe, constant, or pure gauge", "finite_route": "source preferred-frame/time-asymmetry coefficient", "status": "SURVIVES_NONCLAIM", "valid_for_claim": False},
        {"vector_id": "CSV4426_5_species", "generator": "species_charge_constants", "coefficient_symbol": "C_species", "observable_links": "WEP;clock;R10;source_mass", "kill_route": "derive constant-sector universality and source-label forgetting", "finite_route": "source beta_source/species coefficient matrix", "status": "SURVIVES_NONCLAIM", "valid_for_claim": False},
        {"vector_id": "CSV4426_6_readout", "generator": "readout_projector", "coefficient_symbol": "C_readout", "observable_links": "measured_G;PPN;clock;WEP", "kill_route": "prove readout-after-variation and no EFT/readout backreaction", "finite_route": "source readout/reduced-action coefficient", "status": "SURVIVES_NONCLAIM", "valid_for_claim": False},
    ]


def csource_vector_input_rows() -> List[Dict[str, object]]:
    return [
        {"row_id": "CSVIN4426_0_fibre", "component": "finite_cell_fibre_spectrum", "generator": "finite_cell_fibre_spectrum", "coefficient_symbol": "C_fibre", "value": "MISSING_NUMERIC_OR_DERIVED_ZERO", "units": "MISSING_PARENT_UNITS", "parent_variation_basis": "MISSING_FIBRE_BASIS", "observable_projection": "R10_PPN_clock_source_mass_projection_required", "source_path": str(CSV_1092_GEN), "empirical_anchor": "MISSING_ANCHOR_OR_THEOREM_ZERO", "independent_of_bound": False, "input_valid": False, "valid_for_claim": False, "notes": "Finite-cell spectrum is now a named vector component, not an unnamed loophole."},
        {"row_id": "CSVIN4426_1_domain", "component": "relative_domain_class", "generator": "relative_boundary_domain_class", "coefficient_symbol": "C_domain", "value": "MISSING_NUMERIC_OR_DERIVED_ZERO", "units": "MISSING_PARENT_UNITS", "parent_variation_basis": "MISSING_DOMAIN_BASIS", "observable_projection": "local_GR_PPN_R10_orbital_projection_required", "source_path": str(RUN_INV_GEN), "empirical_anchor": "MISSING_ANCHOR_OR_THEOREM_ZERO", "independent_of_bound": False, "input_valid": False, "valid_for_claim": False, "notes": "Domain class must be killed or bounded explicitly."},
        {"row_id": "CSVIN4426_2_chiD", "component": "domain_selector_chi_D", "generator": "domain_selector_chi_D", "coefficient_symbol": "C_chiD", "value": "MISSING_NUMERIC_OR_DERIVED_ZERO", "units": "MISSING_PARENT_UNITS", "parent_variation_basis": "MISSING_SELECTOR_BASIS", "observable_projection": "local_GR_R10_cosmology_split_projection_required", "source_path": str(RUN_TRIV_CHAIN), "empirical_anchor": "MISSING_ANCHOR_OR_THEOREM_ZERO", "independent_of_bound": False, "input_valid": False, "valid_for_claim": False, "notes": "Selector survives unless it is pure bookkeeping or a sourced residual."},
        {"row_id": "CSVIN4426_3_memory", "component": "memory_or_class_scalar", "generator": "memory_or_class_scalar", "coefficient_symbol": "C_memory", "value": "MISSING_NUMERIC_OR_DERIVED_ZERO", "units": "MISSING_PARENT_UNITS", "parent_variation_basis": "MISSING_MEMORY_BASIS", "observable_projection": "clock_PPN_R10_cosmology_projection_required", "source_path": str(CSV_1092_NH), "empirical_anchor": "MISSING_ANCHOR_OR_THEOREM_ZERO", "independent_of_bound": False, "input_valid": False, "valid_for_claim": False, "notes": "Memory scalar must satisfy no-hair/profile-zero or get a finite profile coefficient."},
        {"row_id": "CSVIN4426_4_time", "component": "orientation_time_arrow", "generator": "orientation_time_arrow", "coefficient_symbol": "C_time", "value": "MISSING_NUMERIC_OR_DERIVED_ZERO", "units": "MISSING_PARENT_UNITS", "parent_variation_basis": "MISSING_TIME_ARROW_BASIS", "observable_projection": "preferred_frame_clock_PPN_projection_required", "source_path": str(CSV_1092_GEN), "empirical_anchor": "MISSING_ANCHOR_OR_THEOREM_ZERO", "independent_of_bound": False, "input_valid": False, "valid_for_claim": False, "notes": "Time-arrow/orientation must be coframe-contained, constant, gauge, or bounded."},
        {"row_id": "CSVIN4426_5_species", "component": "species_charge_constants", "generator": "species_charge_constants", "coefficient_symbol": "C_species", "value": "MISSING_NUMERIC_OR_DERIVED_ZERO", "units": "MISSING_PARENT_UNITS", "parent_variation_basis": "MISSING_SPECIES_BASIS", "observable_projection": "WEP_clock_R10_source_mass_projection_required", "source_path": str(CSV_1220_PTOL), "empirical_anchor": "MISSING_ANCHOR_OR_THEOREM_ZERO", "independent_of_bound": False, "input_valid": False, "valid_for_claim": False, "notes": "Species constants are the coupling danger; they need universality or finite beta rows."},
        {"row_id": "CSVIN4426_6_readout", "component": "readout_projector", "generator": "readout_projector", "coefficient_symbol": "C_readout", "value": "MISSING_NUMERIC_OR_DERIVED_ZERO", "units": "MISSING_PARENT_UNITS", "parent_variation_basis": "MISSING_READOUT_BASIS", "observable_projection": "measured_G_PPN_clock_WEP_projection_required", "source_path": str(CSOURCE_SEED), "empirical_anchor": "MISSING_ANCHOR_OR_THEOREM_ZERO", "independent_of_bound": False, "input_valid": False, "valid_for_claim": False, "notes": "Readout re-entry must be proved after variation or bounded as a reduced-action tail."},
    ]


def claim_gate_rows(trans: Sequence[Mapping[str, str]], vector: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    rows = {row["row_id"]: row for row in trans}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in trans) and not any(row.get("valid_for_claim") == "True" for row in vector)
    return [
        {"gate_id": "CG4426_0_exact_lemma", "claim": "connected transitive hidden fibre implies invariant scalars are constants", "passed": rows["HFT4426_1_exact_transitive_lemma"].get("current_status") == "TRANSITIVE_FIBRE_THEOREM_READY_GENERATOR_DEBTS_SURVIVE", "valid_for_claim": False, "detail": "the theorem is exact but not parent-signed as current MTS evidence."},
        {"gate_id": "CG4426_1_current_transitivity", "claim": "current corpus signs the vertical gauge action spans the full hidden kernel", "passed": False, "valid_for_claim": False, "detail": "q/vertical language exists, but gauge action, span and connected fibre regularity are unsigned."},
        {"gate_id": "CG4426_2_generator_debts", "claim": "all hidden invariant generators are eliminated", "passed": False, "valid_for_claim": False, "detail": "finite-cell, domain, selector, memory, time/species/readout generators survive."},
        {"gate_id": "CG4426_3_future_contract", "claim": "future full transitive-fibre contract is executable", "passed": rows["HFT4426_4_future_full_contract"].get("current_status") == "HIDDEN_FIBRE_TRIVIALITY_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "full contract is staged with input_valid=false."},
        {"gate_id": "CG4426_4_vector_staged", "claim": "surviving generators are mapped into a finite C_source vector", "passed": len(vector) == 7 and all(row.get("current_status") == "FINITE_CSOURCE_VECTOR_COMPONENT_CONTRACT_ONLY" for row in vector), "valid_for_claim": False, "detail": "vector worklist exists, but components lack numeric/zero values."},
        {"gate_id": "CG4426_5_no_claim_outputs", "claim": "4426 generated no claim-ready row", "passed": no_claims, "valid_for_claim": False, "detail": "no local-GR/Newton/WEP/R10 claim is emitted."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4426_0",
            "decision": DECISION,
            "summary": "4426 proves the exact conditional route: if the hidden fibre over each local observed state is a connected transitive parent gauge/representative orbit, then every admissible hidden invariant scalar is constant on that fibre. That would kill hidden-source coefficient drift. Current MTS still lacks the parent-signed gauge action, full kernel span, connected regular fibre proof, generator elimination and readout closure. The fallback therefore becomes a concrete seven-component C_source vector rather than another vague missing-coupling note.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4426_0_best_result", "status": "TRANSITIVE_FIBRE_TRIVIALITY_LEMMA_EXACT", "detail": "A connected homogeneous/gauge hidden fibre has only constant invariant scalars.", "valid_for_claim": False},
        {"status_id": "STAT4426_1_open_proof", "status": "PARENT_GAUGE_ACTION_SPAN_AND_GENERATOR_ELIMINATION_UNSIGNED", "detail": "Current corpus does not sign the group action spanning the vertical kernel or kill surviving generators.", "valid_for_claim": False},
        {"status_id": "STAT4426_2_finite_branch", "status": "SEVEN_COMPONENT_CSOURCE_VECTOR_STAGED_NONCLAIM", "detail": "Finite fallback is now C_fibre,C_domain,C_chiD,C_memory,C_time,C_species,C_readout.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4426_0",
            "target": NEXT_TARGET,
            "objective": "Derive the parent vertical gauge action and prove its tangent spans the q-kernel, or fill the first scoreable finite C_source component.",
            "derive_first": "construct G_vert acting on q^{-1}(q_obs), prove connected regular fibres and span Lie(G_vert).Phi = ker(Dq), then map each surviving generator into gauge/constant/readout-only status.",
            "fallback": "choose one C_source component from the seven-component vector and fill numeric or DERIVED_ZERO value, units, parent variation basis, observable projection and source path.",
            "avoid": "repeating hidden triviality without new parent input; calling quotient verticality transitivity; using comparator bounds as coefficients; claiming local GR from a conditional lemma.",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], trans: Sequence[Mapping[str, str]], vector: Sequence[Mapping[str, str]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 442 PPC4161 hidden invariant triviality transitive fibre proof or first finite C_source vector

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4426 makes the hidden-invariant fork mathematically cleaner:

- Exact theorem: a connected hidden fibre that is one transitive parent gauge/representative orbit has no nonconstant hidden invariant scalar.
- If parent-signed, this kills `c(I_hid) O_source` drift without fitting.
- Current MTS does **not** yet sign the required gauge action, full kernel span, connected fibre regularity, generator elimination, or readout closure.
- The fallback is now a concrete seven-component finite `C_source` vector: `C_fibre`, `C_domain`, `C_chiD`, `C_memory`, `C_time`, `C_species`, `C_readout`.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Transitive Fibre Gate

{table(trans)}

## Surviving Generator C_source Vector

{table(generator_vector_rows())}

## C_source Vector Input Gate

{table(vector)}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4426 - hidden invariant triviality transitive fibre proof or first finite C_source vector

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Proved the exact conditional transitive-fibre lemma: connected homogeneous hidden fibres have only constant invariant scalars.
- Refused promotion because current MTS lacks parent-signed vertical gauge action, full kernel span and generator elimination.
- Converted the surviving hidden generators into a seven-component finite `C_source` vector.
- Selected a sharper next move: prove the vertical gauge action/span or fill one scoreable vector component.

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
        "claim": "4426 proves the exact conditional transitive-fibre lemma for hidden invariant triviality: if each hidden fibre is a connected transitive parent gauge/representative orbit, then hidden invariant scalars are constants and cannot feed relative source coefficients. Current MTS does not yet sign the gauge action, kernel span, connected fibre regularity, generator elimination or readout closure. A seven-component finite C_source vector is staged as the fallback worklist.",
        "current_evidence": "4426 source register, derivation rows, transitive fibre output, C_source vector rows, claim gates, decision, status, next target and validation CSV.",
        "status": "transitive_fibre_triviality_exact_parent_gauge_span_unsigned_csource_vector_staged",
        "next_test": "Derive parent vertical gauge action/span, or fill one finite C_source component with numeric/DERIVED_ZERO value and projection.",
        "key_risk": "Calling quotient verticality transitivity; repeating hidden triviality without new parent input; hiding source coupling in readout or comparator bounds.",
        "sector": "local_gr",
        "evidence": "4426 source register, derivation rows, transitive fibre output, C_source vector rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Derive parent vertical gauge action/span, or fill one finite C_source component with numeric/DERIVED_ZERO value and projection.",
        "risk": "Calling quotient verticality transitivity; repeating hidden triviality without new parent input; hiding source coupling in readout or comparator bounds.",
    }
    rows.append({name: new_row.get(name, "") for name in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = """## 4426 local spine update: hidden triviality needs transitive fibres

4426 turns `O(C_hid)^inv = R` into a real geometry theorem: if the hidden fibre over an observed local state is a connected transitive parent gauge/representative orbit, invariant hidden scalars are constants. That is the clean route to killing hidden-source coupling drift. Current MTS still has not signed the vertical gauge action, kernel span, connected fibre regularity or generator elimination, so no local-GR/Newton claim fires. The finite fallback is now concrete: a seven-component `C_source` vector covering fibre spectrum, domain class, selector, memory, time-arrow, species constants and readout.
"""
    packet_section = f"""## 4426 packet update: transitive-fibre lemma

`{PACKET_MARKER}`

Private packet result: we found the right mathematical lock. Hidden invariants vanish if the hidden sector is only representative motion along one connected gauge orbit. If the orbit proof fails, coupling is not mystical anymore; it is the explicit vector `C_fibre + C_domain + C_chiD + C_memory + C_time + C_species + C_readout`.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    trans = {row["row_id"]: row for row in rows_from(TRANSITIVITY_OUTPUT)}
    vector = rows_from(CSOURCE_VECTOR_OUTPUT)
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in trans.values()) and not any(row.get("valid_for_claim") == "True" for row in vector)
    checks = [
        ("VAL4426_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4426_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every source needle is present"),
        ("VAL4426_2_exact_lemma", trans["HFT4426_1_exact_transitive_lemma"].get("current_status") == "TRANSITIVE_FIBRE_THEOREM_READY_GENERATOR_DEBTS_SURVIVE", "exact transitive-fibre lemma is staged"),
        ("VAL4426_3_current_q_kernel_unsigned", trans["HFT4426_0_current_q_kernel"].get("current_status") == "VERTICAL_KERNEL_DEFINED_GAUGE_ACTION_UNSIGNED", "current q-kernel lacks signed gauge action"),
        ("VAL4426_4_generator_debt", trans["HFT4426_2_generator_debt_current"].get("current_status") == "VERTICAL_KERNEL_DEFINED_GAUGE_ACTION_UNSIGNED", "generator debt remains live"),
        ("VAL4426_5_future_contract", trans["HFT4426_4_future_full_contract"].get("current_status") == "HIDDEN_FIBRE_TRIVIALITY_CONTRACT_READY_NONCLAIM", "future full contract is executable nonclaim"),
        ("VAL4426_6_vector_count", len(vector) == 7, "seven C_source vector components written"),
        ("VAL4426_7_vector_nonclaim", all(row.get("score_ready") == "False" for row in vector), "no C_source component is score-ready"),
        ("VAL4426_8_no_claim_outputs", no_claims, "no generated row is claim-ready"),
        ("VAL4426_9_claim_gates_block", any(row["gate_id"] == "CG4426_5_no_claim_outputs" and row["passed"] == "True" for row in gates), "claim gates explicitly block public claim"),
        ("VAL4426_10_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-267"),
        ("VAL4426_11_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4426_12_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4426_13_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4426_14_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4426_15_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4426_16_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(TRANSITIVITY_INPUT, transitivity_input_rows())
    write_csv(TRANSITIVITY_OUTPUT, evaluate_transitivity_rows(TRANSITIVITY_INPUT))
    write_csv(GENERATOR_VECTOR, generator_vector_rows())
    write_csv(CSOURCE_VECTOR_INPUT, csource_vector_input_rows())
    write_csv(CSOURCE_VECTOR_OUTPUT, evaluate_vector_rows(CSOURCE_VECTOR_INPUT))
    trans = rows_from(TRANSITIVITY_OUTPUT)
    vector = rows_from(CSOURCE_VECTOR_OUTPUT)
    gates = claim_gate_rows(trans, vector)
    write_csv(CLAIM_GATES, gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), trans, vector, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()

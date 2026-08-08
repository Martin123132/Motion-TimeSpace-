from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1232"
TITLE = "1232-Y5-R10-parent-interaction-graph-certificate-or-component-fraction-source-pack"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
GRAPH_CERT_PATH = OUT_DIR / f"{PACK_ID}_INTERACTION_GRAPH_CERTIFICATE_ATTEMPT.csv"
GRAPH_EDGES_PATH = OUT_DIR / f"{PACK_ID}_ORDINARY_MATTER_GRAPH_EDGE_AUDIT.csv"
FRACTION_SOURCE_PACK_PATH = OUT_DIR / f"{PACK_ID}_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv"
FRACTION_FORMULA_PATH = OUT_DIR / f"{PACK_ID}_COMPONENT_FRACTION_FORMULA_LEDGER.csv"
QUARANTINE_PATH = OUT_DIR / f"{PACK_ID}_TOY_PROXY_QUARANTINE.csv"
RUNNER_FEED_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_FEED_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1232_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def is_false(row: dict[str, object], key: str) -> bool:
    return not parse_bool(row.get(key, False))


def source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > RUN_STARTED_UTC
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1232_0_1231_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1231_NEXT_TARGET.csv",
            "needle": "NEXT1231_0_1232",
            "purpose": "1231 handoff to interaction graph or component-fraction source pack",
        },
        {
            "source_id": "SRC1232_1_1231_graph",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1231_MATTER_CATEGORY_CONNECTEDNESS_ATTEMPT.csv",
            "needle": "CMC1231_1_interaction_graph_lemma",
            "purpose": "conditional interaction-graph theorem",
        },
        {
            "source_id": "SRC1232_2_1231_delta_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1231_DELTA_W_COMPONENT_MAP.csv",
            "needle": "DWM1231_1_TiPt_difference",
            "purpose": "Ti/Pt Delta_w component formula",
        },
        {
            "source_id": "SRC1232_3_1231_basis",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1231_DISCONNECTED_COMPONENT_RESIDUAL_BASIS.csv",
            "needle": "DCW1231_4_EM_Coulomb_binding",
            "purpose": "disconnected residual component basis",
        },
        {
            "source_id": "SRC1232_4_1080_material",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv",
            "needle": "MAT1080_4_full_tensor_upgrade",
            "purpose": "finite WEP material composition/tensor candidates",
        },
        {
            "source_id": "SRC1232_5_983_constituents",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv",
            "needle": "M983_1_TiAlloy",
            "purpose": "MICROSCOPE alloy composition context",
        },
        {
            "source_id": "SRC1232_6_1061_convention",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv",
            "needle": "MCON1061_0_test_pair",
            "purpose": "Ti/Pt sign/material convention",
        },
        {
            "source_id": "SRC1232_7_1077_toy_status",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1077_MATERIAL_VECTOR_SOURCE_ROW_STATUS.csv",
            "needle": "MVS1077_1_required_claim_material",
            "purpose": "toy material vector quarantine status",
        },
        {
            "source_id": "SRC1232_8_1087_no_cancel",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1087_ALL_MATERIAL_NO_CANCELLATION_POLICY.csv",
            "needle": "AMC1087_1_basis_completeness",
            "purpose": "no one-pair cancellation/no incomplete basis policy",
        },
        {
            "source_id": "SRC1232_9_1228_intake",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1228_ACCEPTANCE_GATE_MATRIX.csv",
            "needle": "ACCEPT1228_4_tau_WEP",
            "purpose": "official MICROSCOPE tau/readout gate remains blocked",
        },
    ]

    source_register = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    graph_cert = [
        {
            "cert_id": "IGC1232_0_target",
            "claim_piece": "parent ordinary-matter interaction graph certificate",
            "formal_statement": "Construct G_ord=(V,E) from parent-owned action terms, with V={electron, light-quark, gluon/QCD, photon/EM, nuclear binding, measure/readout owner} and E nonzero parent interaction/current morphisms.",
            "result": "TARGET_SHARPENED",
            "missing_for_claim": "parent action must sign each vertex and edge as an owned ordinary-matter morphism",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "cert_id": "IGC1232_1_graph_connectedness_lemma",
            "claim_piece": "connected graph implies common source scale",
            "formal_statement": "If every edge in G_ord is a parent-owned nonzero morphism of the action-density/source functor and G_ord is connected, then natural source weights are constant on V.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_claim": "the graph is a template, not a parent-signed certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "cert_id": "IGC1232_2_template_physics",
            "claim_piece": "ordinary Ti/Pt matter is not plausibly disconnected physically",
            "formal_statement": "The electron, EM, quark, gluon, and nuclear-binding rows are linked in ordinary composite matter by interaction/current structure, so the connectedness route remains attractive.",
            "result": "PLAUSIBILITY_ONLY_NOT_MTS_PROOF",
            "missing_for_claim": "MTS parent action must derive the interaction graph rather than borrow it as background taste",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "cert_id": "IGC1232_3_current_signature",
            "claim_piece": "current corpus signs G_ord connectedness",
            "formal_statement": "Existing MTS files already provide parent-owned vertices and nonzero morphism edges for the whole ordinary-matter graph.",
            "result": "NOT_PARENT_SIGNED",
            "missing_for_claim": "parent matter functor, current owner, hbar/measure owner, and readout closure remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "cert_id": "IGC1232_4_verdict",
            "claim_piece": "interaction graph closes Delta_w",
            "formal_statement": "IGC1232_1 would close relative source weights only after every graph edge and source functor is parent-signed.",
            "result": "GRAPH_CERTIFICATE_NOT_CLOSED",
            "missing_for_claim": "build parent interaction graph certificate or keep component-fraction source pack",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    graph_edges = [
        {
            "edge_id": "EDGE1232_0_electron_photon",
            "from_component": "electron/leptonic",
            "to_component": "EM/photon/Coulomb",
            "candidate_morphism": "visible EM current coupling J_e^mu A_mu",
            "needed_parent_owner": "EM/current normalization owner plus matter functor",
            "current_status": "TEMPLATE_EDGE_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "EDGE1232_1_quark_photon",
            "from_component": "light-quark mass",
            "to_component": "EM/photon/Coulomb",
            "candidate_morphism": "quark electric charge/current coupling",
            "needed_parent_owner": "fixed representation charge/current owner",
            "current_status": "TEMPLATE_EDGE_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "EDGE1232_2_quark_gluon",
            "from_component": "light-quark mass",
            "to_component": "QCD/gluon binding",
            "candidate_morphism": "QCD color interaction and hadronization/bound-state map",
            "needed_parent_owner": "ordinary matter gauge/strong-sector action owner",
            "current_status": "TEMPLATE_EDGE_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "EDGE1232_3_QCD_nuclear",
            "from_component": "QCD/gluon binding",
            "to_component": "nuclear surface/asymmetry",
            "candidate_morphism": "nucleon/nuclear binding map",
            "needed_parent_owner": "composite material response and nuclear binding functor",
            "current_status": "TEMPLATE_EDGE_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "EDGE1232_4_EM_nuclear",
            "from_component": "EM/photon/Coulomb",
            "to_component": "nuclear surface/asymmetry",
            "candidate_morphism": "Coulomb term in nuclear/material binding",
            "needed_parent_owner": "material tensor basis and alpha/EM coefficient owner",
            "current_status": "TEMPLATE_EDGE_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "EDGE1232_5_measure_readout_all",
            "from_component": "measure/readout owner",
            "to_component": "all material components",
            "candidate_morphism": "species-blind measure/current/readout descent",
            "needed_parent_owner": "hbar/measure/current owner and MICROSCOPE readout kernel",
            "current_status": "UNSIGNED_AND_DATA_PENDING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    fraction_source_pack = [
        {
            "pack_id": "FSP1232_0_alloy_composition_context",
            "target_quantity": "PtRh10 and TA6V alloy mass fractions",
            "required_source_or_method": "MICROSCOPE official/test-mass composition source in same TA6V_minus_PtRh10 convention",
            "current_local_evidence": "P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv; P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv",
            "current_status": "SOURCE_BACKED_CONTEXT_AVAILABLE_NONCLAIM",
            "blocks_claim": "still not a component energy-fraction tensor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "FSP1232_1_isotopic_abundances_masses",
            "target_quantity": "isotopic abundances and atomic/nuclear masses for Ti, Al, V, Pt, Rh",
            "required_source_or_method": "official nuclide/isotopic table with uncertainty/provenance",
            "current_local_evidence": "nominal A values only",
            "current_status": "MISSING_CLAIM_GRADE_ISOTOPIC_TABLE",
            "blocks_claim": "cannot compute source-component energy fractions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "FSP1232_2_electron_fraction",
            "target_quantity": "F_{B,e}",
            "required_source_or_method": "Z, isotope mix, electron rest/chemical binding convention, material mass normalization",
            "current_local_evidence": "Y_e proxy rows available from 983/1076",
            "current_status": "PROXY_ONLY_NOT_FRACTION",
            "blocks_claim": "proxy Y_e is not an energy fraction in the Delta_w basis",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "FSP1232_3_light_quark_fraction",
            "target_quantity": "F_{B,q}",
            "required_source_or_method": "nucleon sigma terms or selected phenomenological mass-decomposition basis with citations",
            "current_local_evidence": "none in parent MTS basis",
            "current_status": "MISSING_PARENT_OR_PHENOMENOLOGICAL_BASIS",
            "blocks_claim": "delta w_q cannot be mapped to Ti/Pt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "FSP1232_4_QCD_gluon_fraction",
            "target_quantity": "F_{B,g}",
            "required_source_or_method": "mass budget convention, residual bulk term, and no double-counting rule",
            "current_local_evidence": "none in parent MTS basis",
            "current_status": "MISSING_PARENT_OR_PHENOMENOLOGICAL_BASIS",
            "blocks_claim": "common/bulk QCD mode cannot be separated from residual source weights",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "FSP1232_5_EM_Coulomb_fraction",
            "target_quantity": "F_{B,EM}",
            "required_source_or_method": "nuclear Coulomb energy model or DD alpha/Coulomb basis explicitly marked external",
            "current_local_evidence": "DD alpha/Coulomb smoke delta in 1080/1081",
            "current_status": "SMOKE_DELTA_AVAILABLE_NOT_FULL_FRACTION",
            "blocks_claim": "external DD basis is not yet MTS parent source basis",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "FSP1232_6_nuclear_surface_asymmetry_fraction",
            "target_quantity": "F_{B,nuc}",
            "required_source_or_method": "nuclear binding/surface/asymmetry model with isotope/alloy averaging",
            "current_local_evidence": "DD surface smoke delta in 1080/1081",
            "current_status": "SMOKE_DELTA_AVAILABLE_NOT_FULL_FRACTION",
            "blocks_claim": "surface row is a useful external basis piece, not a full MTS tensor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "FSP1232_7_measure_readout_fraction",
            "target_quantity": "DeltaK_TiPt and tau_WEP",
            "required_source_or_method": "official CMSM/MICROSCOPE arrays accepted by 1228 gates plus source-worldtube/readout normalization",
            "current_local_evidence": "1228 intake contract only",
            "current_status": "DATA_PENDING",
            "blocks_claim": "tau_WEP and readout reentry component cannot be scored",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    fraction_formulas = [
        {
            "formula_id": "FORM1232_0_alloy_average",
            "target": "component fraction in material B",
            "formula": "F_{B,c}=sum_{elements E in B} x_{B,E} sum_i p_{E,i} F_{E,i,c}",
            "inputs": "alloy mass fractions x; isotope fractions p; isotope component fractions F",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "formula_id": "FORM1232_1_delta_fraction",
            "target": "Ti/Pt differential component fraction",
            "formula": "DeltaF_{TiPt,c}=F_{TA6V,c}-F_{PtRh10,c}",
            "inputs": "same convention as MCON1061_0_test_pair",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "formula_id": "FORM1232_2_delta_w_prediction",
            "target": "Delta_w_TiPt",
            "formula": "Delta_w_TiPt=sum_c DeltaF_{TiPt,c} delta w_c + DeltaK_TiPt",
            "inputs": "DeltaF rows; component priors; readout/measure residual",
            "status": "NONCLAIM_TEMPLATE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "formula_id": "FORM1232_3_wep_product",
            "target": "MICROSCOPE WEP source-weight product",
            "formula": "abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15",
            "inputs": "Delta_w_TiPt; official tau_WEP; eta bound",
            "status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    quarantine = [
        {
            "row_id": "QUAR1232_0_983_proxy_vectors",
            "local_rows": "P8_Y5_R10_983_MATERIAL_PROXY_CHARGE_VECTORS.csv",
            "allowed_use": "debug/proxy contrast only",
            "forbidden_use": "Delta_w component fractions or WEP claim",
            "reason": "Y_e/neutron/coulomb proxies are not parent-basis energy fractions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "QUAR1232_1_1076_toy_vector",
            "local_rows": "P8_Y5_R10_1076_TOY_MATERIAL_VECTOR_FROM_651.csv",
            "allowed_use": "algebra smoke tests only",
            "forbidden_use": "claim-valid material tensor",
            "reason": "nominal alloy vector explicitly marked toy/nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "QUAR1232_2_DD_smoke_deltas",
            "local_rows": "P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv",
            "allowed_use": "external phenomenological comparator rows",
            "forbidden_use": "MTS parent source-basis proof",
            "reason": "DD alpha/surface basis is useful but not parent-derived MTS basis",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "QUAR1232_3_one_pair_cancellation",
            "local_rows": "P8_Y5_R10_1087_ALL_MATERIAL_NO_CANCELLATION_POLICY.csv",
            "allowed_use": "guardrail",
            "forbidden_use": "tuned Ti/Pt cancellation as theory result",
            "reason": "one-pair cancellation is not invariant across material pairs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_feed = [
        {
            "feed_id": "FEED1232_0_to_DWM1231_1",
            "target": "DWM1231_1_TiPt_difference",
            "update": "component-fraction source pack and formulas staged; no numeric Delta_w row promoted",
            "claim_rows_delta": 0,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1232_1_to_ARENA1231_0",
            "target": "ARENA1231_0_WEP_MICROSCOPE",
            "update": "WEP law remains not scoreable until DeltaF, delta_w priors, DeltaK, and tau_WEP exist",
            "claim_rows_delta": 0,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1232_2_to_IGC1232",
            "target": "interaction graph certificate",
            "update": "template graph edges written but not parent-signed",
            "claim_rows_delta": 0,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1232_0_graph_not_closed",
            "decision": "do not claim the parent interaction graph certificate",
            "because": "all useful edges are templates until parent action signs the vertices, morphisms, and source functor",
            "next_action": "either derive parent graph ownership or keep component-fraction source pack",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1232_1_source_pack_created",
            "decision": "use source-pack route as finite fallback",
            "because": "Ti/Pt Delta_w now has exact required component fractions and source requirements",
            "next_action": "fill source pack only from official/provenance-grade sources or parent derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1232_2_no_proxy_claim",
            "decision": "quarantine proxy/toy material rows",
            "because": "proxy vectors are good smoke tests but not component energy fractions in the parent Delta_w basis",
            "next_action": "keep them for debugging, never for claim promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1232_0_graph_certificate",
            "claim": "ordinary matter interaction graph parent-signed and connected",
            "status": "BLOCKED",
            "reason": "IGC1232_4 result=GRAPH_CERTIFICATE_NOT_CLOSED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1232_1_component_fractions",
            "claim": "claim-grade Ti/Pt component fractions",
            "status": "BLOCKED",
            "reason": "FSP1232 rows still include missing isotope, mass-decomposition, parent-basis, and readout inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1232_2_Delta_w_score",
            "claim": "numeric Delta_w_TiPt prediction",
            "status": "BLOCKED",
            "reason": "FORM1232_2 is nonclaim template only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1232_3_WEP",
            "claim": "WEP/MICROSCOPE pass",
            "status": "BLOCKED",
            "reason": "tau_WEP and Delta_w_TiPt are not claim-grade",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1232_4_local_GR",
            "claim": "local GR/Newton source reduction",
            "status": "BLOCKED",
            "reason": "finite source residual branch remains active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1232_0_1233",
            "target_file": "1233-Y5-R10-component-fraction-intake-validator-or-parent-graph-edge-owner-proof.md",
            "target_script": "scripts/Y5_R10_component_fraction_intake_validator_or_parent_graph_edge_owner_proof.py",
            "task": "build a validator for future component-fraction rows and, in parallel, attack one parent graph edge owner proof starting with current/EM or quark-gluon ownership",
            "success_condition": "future fraction rows cannot enter without provenance/schema/unit checks, and at least one graph edge owner proof is either signed or explicitly demoted",
            "do_not_do": "do not claim Delta_w=0, WEP, PPN, local GR, or use toy/proxy rows as claim data",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_paths = [
        SOURCE_REGISTER_PATH,
        GRAPH_CERT_PATH,
        GRAPH_EDGES_PATH,
        FRACTION_SOURCE_PACK_PATH,
        FRACTION_FORMULA_PATH,
        QUARANTINE_PATH,
        RUNNER_FEED_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(GRAPH_CERT_PATH, graph_cert)
    write_csv(GRAPH_EDGES_PATH, graph_edges)
    write_csv(FRACTION_SOURCE_PACK_PATH, fraction_source_pack)
    write_csv(FRACTION_FORMULA_PATH, fraction_formulas)
    write_csv(QUARANTINE_PATH, quarantine)
    write_csv(RUNNER_FEED_PATH, runner_feed)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(NEXT_PATH, next_target)

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:ERROR:{exc}")

    all_sources_exist = all(parse_bool(row["path_exists"]) for row in source_register)
    all_needles_found = all(parse_bool(row["needle_found"]) for row in source_register)
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for table in [
            source_register,
            graph_cert,
            graph_edges,
            fraction_source_pack,
            fraction_formulas,
            quarantine,
            runner_feed,
            decisions,
            claim_gates,
            next_target,
        ]
        for row in table
    )
    graph_conditional = any(row["cert_id"] == "IGC1232_1_graph_connectedness_lemma" for row in graph_cert)
    graph_not_closed = any(row["cert_id"] == "IGC1232_4_verdict" and row["result"] == "GRAPH_CERTIFICATE_NOT_CLOSED" for row in graph_cert)
    edge_rows_present = len(graph_edges) >= 5 and all("NOT_PARENT_SIGNED" in row["current_status"] or "DATA_PENDING" in row["current_status"] for row in graph_edges)
    source_pack_present = len(fraction_source_pack) >= 8 and any(row["pack_id"] == "FSP1232_7_measure_readout_fraction" for row in fraction_source_pack)
    formula_template_present = any(row["formula_id"] == "FORM1232_2_delta_w_prediction" for row in fraction_formulas)
    quarantine_present = len(quarantine) >= 4
    gates_blocked = all(row["status"] == "BLOCKED" and is_false(row, "claim_allowed") for row in claim_gates)
    next_is_1233 = next_target[0]["target_file"].startswith("1233-Y5-R10-component-fraction-intake-validator")
    fw_recent = formalization_recent_count()

    validation = [
        validation_row(
            "VAL1232_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(parse_bool(row['path_exists']) for row in source_register)}/{len(source_register)} sources exist",
        ),
        validation_row(
            "VAL1232_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(parse_bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        ),
        validation_row(
            "VAL1232_2_graph_conditional",
            "graph connectedness theorem remains conditional",
            graph_conditional,
            "IGC1232_1 present",
        ),
        validation_row(
            "VAL1232_3_graph_not_closed",
            "interaction graph certificate is not promoted",
            graph_not_closed,
            "IGC1232_4 result=GRAPH_CERTIFICATE_NOT_CLOSED",
        ),
        validation_row(
            "VAL1232_4_edge_rows_present",
            "graph edge audit rows are present and unsigned",
            edge_rows_present,
            f"edge_rows={len(graph_edges)}",
        ),
        validation_row(
            "VAL1232_5_source_pack_present",
            "component-fraction source pack exists",
            source_pack_present,
            f"source_pack_rows={len(fraction_source_pack)}",
        ),
        validation_row(
            "VAL1232_6_formula_template_present",
            "Delta_w component formula template exists",
            formula_template_present,
            "FORM1232_2_delta_w_prediction present",
        ),
        validation_row(
            "VAL1232_7_quarantine_present",
            "toy/proxy rows are quarantined",
            quarantine_present,
            f"quarantine_rows={len(quarantine)}",
        ),
        validation_row(
            "VAL1232_8_claim_gates_blocked",
            "all claim gates remain blocked",
            gates_blocked,
            f"blocked_gates={sum(row['status'] == 'BLOCKED' for row in claim_gates)}/{len(claim_gates)}",
        ),
        validation_row(
            "VAL1232_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_generated_nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1232_10_next_target_1233",
            "next target builds validator or edge-owner proof",
            next_is_1233,
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1232_11_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_counts),
        ),
        validation_row(
            "VAL1232_12_formalization_untouched",
            "formalization-workbench untouched during run",
            fw_recent == 0,
            f"formalization_recent_write_count_since_run_start={fw_recent}",
        ),
    ]
    validation.append(
        validation_row(
            "VAL1232_13_overall",
            "overall 1232 validation",
            all(row["status"] == "PASS" for row in validation),
            "1232 keeps the parent interaction graph conditional and stages a strict nonclaim Ti/Pt component-fraction source pack",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1232 does **not** certify the parent ordinary-matter interaction graph. It writes the graph theorem and edge audit, but every useful edge is still a template until the parent action signs the matter/current/measure owners.",
        "",
        "**Main progress:** the finite fallback is now source-pack shaped: `Delta_w_TiPt=sum_c DeltaF_TiPt,c delta w_c + DeltaK_TiPt`, with exact rows for alloy composition context, isotope/mass inputs, electron/light-quark/QCD/EM/nuclear fractions, and MICROSCOPE readout/tau inputs.",
        "",
        "**No-claim guard:** toy/proxy material vectors are quarantined. No `Delta_w`, WEP, PPN, clock, orbital, local-GR, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Interaction Graph Certificate Attempt",
        markdown_table(graph_cert, list(graph_cert[0].keys())),
        "",
        "## Ordinary Matter Graph Edge Audit",
        markdown_table(graph_edges, list(graph_edges[0].keys())),
        "",
        "## Ti/Pt Component-Fraction Source Pack",
        markdown_table(fraction_source_pack, list(fraction_source_pack[0].keys())),
        "",
        "## Component-Fraction Formula Ledger",
        markdown_table(fraction_formulas, list(fraction_formulas[0].keys())),
        "",
        "## Toy/Proxy Quarantine",
        markdown_table(quarantine, list(quarantine[0].keys())),
        "",
        "## Runner Feed Update",
        markdown_table(runner_feed, list(runner_feed[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Next Target",
        markdown_table(next_target, list(next_target[0].keys())),
        "",
        "## Validation",
        markdown_table(validation, list(validation[0].keys())),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()

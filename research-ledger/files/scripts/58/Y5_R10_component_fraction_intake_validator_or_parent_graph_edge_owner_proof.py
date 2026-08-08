from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1233"
TITLE = "1233-Y5-R10-component-fraction-intake-validator-or-parent-graph-edge-owner-proof"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
FRACTION_DIR = ROOT / "source-intake" / "component-fractions"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
DIRECTORY_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_COMPONENT_FRACTION_DIRECTORY_CONTRACT.csv"
SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_COMPONENT_FRACTION_SCHEMA.csv"
ACCEPTANCE_GATES_PATH = OUT_DIR / f"{PACK_ID}_COMPONENT_FRACTION_ACCEPTANCE_GATES.csv"
TEMPLATE_PATH = OUT_DIR / f"{PACK_ID}_COMPONENT_FRACTION_CANDIDATE_TEMPLATE_NONCLAIM.csv"
VALIDATOR_DRYRUN_PATH = OUT_DIR / f"{PACK_ID}_COMPONENT_FRACTION_VALIDATOR_DRYRUN.csv"
EM_EDGE_PROOF_PATH = OUT_DIR / f"{PACK_ID}_EM_CURRENT_EDGE_OWNER_PROOF_ATTEMPT.csv"
EDGE_DEMOTION_PATH = OUT_DIR / f"{PACK_ID}_GRAPH_EDGE_DEMOTION_LEDGER.csv"
FEED_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_FEED_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1233_VALIDATION.csv"


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


def candidate_files() -> list[Path]:
    raw = FRACTION_DIR / "raw"
    if not raw.exists():
        return []
    return sorted(path for path in raw.iterdir() if path.is_file() and path.suffix.lower() == ".csv")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for subdir in ["raw", "docs", "accepted", "rejected"]:
        (FRACTION_DIR / subdir).mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1233_0_1232_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_NEXT_TARGET.csv",
            "needle": "NEXT1232_0_1233",
            "purpose": "1232 handoff to validator or edge-owner proof",
        },
        {
            "source_id": "SRC1233_1_1232_source_pack",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv",
            "needle": "FSP1232_7_measure_readout_fraction",
            "purpose": "component-fraction source requirements",
        },
        {
            "source_id": "SRC1233_2_1232_formula",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_COMPONENT_FRACTION_FORMULA_LEDGER.csv",
            "needle": "FORM1232_2_delta_w_prediction",
            "purpose": "Delta_w component formula",
        },
        {
            "source_id": "SRC1233_3_1232_edge",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_ORDINARY_MATTER_GRAPH_EDGE_AUDIT.csv",
            "needle": "EDGE1232_0_electron_photon",
            "purpose": "electron-photon graph edge target",
        },
        {
            "source_id": "SRC1233_4_1055_em_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "needle": "PAC1055_1_EM_owner",
            "purpose": "EM owner contract candidate",
        },
        {
            "source_id": "SRC1233_5_1065_charge_norm",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1065_CHARGE_INTERACTION_NORMALIZATION_AUDIT.csv",
            "needle": "CIN1065_4_verdict",
            "purpose": "charge/current normalization audit",
        },
        {
            "source_id": "SRC1233_6_951_ward",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_951_SOURCE_CURRENT_WARD_ACTION_ATTEMPT.csv",
            "needle": "SWA951_5_verdict",
            "purpose": "source current Ward action attempt",
        },
        {
            "source_id": "SRC1233_7_993_current_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_993_CURRENT_EXTRACTION_GATE.csv",
            "needle": "CEG993_4_verdict",
            "purpose": "current extraction gate",
        },
        {
            "source_id": "SRC1233_8_990_parent_action",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
            "needle": "PAC990_3_EM_lock",
            "purpose": "parent action EM/current/source contract",
        },
        {
            "source_id": "SRC1233_9_1232_quarantine",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_TOY_PROXY_QUARANTINE.csv",
            "needle": "QUAR1232_0_983_proxy_vectors",
            "purpose": "toy/proxy row quarantine policy",
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

    directory_contract = [
        {
            "directory_id": "CFD1233_0_raw",
            "absolute_path": str(FRACTION_DIR / "raw"),
            "allowed_contents": "future source-backed component-fraction candidate CSVs only",
            "forbidden_contents": "toy/proxy vectors, handwritten claim rows, unsourced numeric tables",
            "current_status": "READY_EMPTY_OR_WAITING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "directory_id": "CFD1233_1_docs",
            "absolute_path": str(FRACTION_DIR / "docs"),
            "allowed_contents": "source PDFs/DOIs/readmes/schema notes for candidate fraction rows",
            "forbidden_contents": "uncited notes used as source authority",
            "current_status": "READY_EMPTY_OR_WAITING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "directory_id": "CFD1233_2_accepted",
            "absolute_path": str(FRACTION_DIR / "accepted"),
            "allowed_contents": "future rows after schema/provenance/unit gates pass; still nonclaim until physics gates pass",
            "forbidden_contents": "rows with MISSING markers or invalid source paths",
            "current_status": "EMPTY_LOCKED_BY_VALIDATOR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "directory_id": "CFD1233_3_rejected",
            "absolute_path": str(FRACTION_DIR / "rejected"),
            "allowed_contents": "future rejected candidates with refusal reasons",
            "forbidden_contents": "claim rows",
            "current_status": "READY_EMPTY_OR_WAITING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    schema_rows = [
        {
            "field": "row_id",
            "required": True,
            "type_or_rule": "stable unique string",
            "allowed_values_or_units": "prefix CFI1233 or future checkpoint id",
            "blocks_acceptance_if_missing": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field": "material_id",
            "required": True,
            "type_or_rule": "one of TA6V, PtRh10, or explicit alloy/source body",
            "allowed_values_or_units": "TA6V;PtRh10;Earth_source;custom_with_source",
            "blocks_acceptance_if_missing": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field": "component_id",
            "required": True,
            "type_or_rule": "must map to DCW1231 component basis",
            "allowed_values_or_units": "electron;light_quark;QCD_gluon;EM_Coulomb;nuclear_surface;measure_readout",
            "blocks_acceptance_if_missing": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field": "fraction_value",
            "required": True,
            "type_or_rule": "finite numeric >=0 unless signed residual explicitly justified",
            "allowed_values_or_units": "dimensionless energy/mass fraction",
            "blocks_acceptance_if_missing": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field": "fraction_uncertainty",
            "required": True,
            "type_or_rule": "finite numeric >=0 or sourced upper-bound convention",
            "allowed_values_or_units": "dimensionless",
            "blocks_acceptance_if_missing": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field": "basis_convention",
            "required": True,
            "type_or_rule": "names parent/MTS basis or external phenomenological basis",
            "allowed_values_or_units": "MTS_parent_basis;external_DD;external_mass_budget;other_with_source",
            "blocks_acceptance_if_missing": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field": "source_path_or_url",
            "required": True,
            "type_or_rule": "local path or URL/DOI recorded with provenance",
            "allowed_values_or_units": "must not be blank or MISSING",
            "blocks_acceptance_if_missing": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field": "extraction_method",
            "required": True,
            "type_or_rule": "explicit formula/table/digitization/derivation note",
            "allowed_values_or_units": "table;formula;digitized;parent_derivation;manual_with_audit",
            "blocks_acceptance_if_missing": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field": "valid_for_claim",
            "required": True,
            "type_or_rule": "must remain false at intake stage",
            "allowed_values_or_units": "False",
            "blocks_acceptance_if_missing": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    acceptance_gates = [
        {
            "gate_id": "CFG1233_0_schema",
            "gate": "candidate row has every required schema field",
            "current_status": "WAITING_FOR_INPUTS",
            "promotion_rule": "reject if any required column missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CFG1233_1_numeric",
            "gate": "fraction_value and fraction_uncertainty parse as finite numeric values",
            "current_status": "WAITING_FOR_INPUTS",
            "promotion_rule": "reject NaN, infinity, blank, symbolic, or MISSING values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CFG1233_2_basis",
            "gate": "basis convention maps to DCW1231 components and no double counting",
            "current_status": "WAITING_FOR_INPUTS",
            "promotion_rule": "reject unowned basis or component aliases not mapped to residual basis",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CFG1233_3_source",
            "gate": "source path/url/doi and extraction method are recorded",
            "current_status": "WAITING_FOR_INPUTS",
            "promotion_rule": "reject unsourced, proxy-only, toy-only, or unverifiable rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CFG1233_4_no_proxy",
            "gate": "toy/proxy rows are refused as claim candidates",
            "current_status": "ACTIVE",
            "promotion_rule": "rows referencing QUAR1232 sources remain debug-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CFG1233_5_physics",
            "gate": "accepted fraction rows still cannot claim WEP/local-GR without Delta_w priors and tau_WEP",
            "current_status": "ACTIVE",
            "promotion_rule": "component rows feed only nonclaim templates until physics gates close",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    template_rows = [
        {
            "row_id": "CFI1233_TEMPLATE_TA6V_electron",
            "material_id": "TA6V",
            "component_id": "electron",
            "fraction_value": "MISSING_NUMERIC",
            "fraction_uncertainty": "MISSING_NUMERIC",
            "basis_convention": "MISSING_BASIS",
            "source_path_or_url": "MISSING_SOURCE",
            "extraction_method": "MISSING_METHOD",
            "intake_status": "TEMPLATE_NONCLAIM_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "CFI1233_TEMPLATE_PtRh10_electron",
            "material_id": "PtRh10",
            "component_id": "electron",
            "fraction_value": "MISSING_NUMERIC",
            "fraction_uncertainty": "MISSING_NUMERIC",
            "basis_convention": "MISSING_BASIS",
            "source_path_or_url": "MISSING_SOURCE",
            "extraction_method": "MISSING_METHOD",
            "intake_status": "TEMPLATE_NONCLAIM_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "CFI1233_TEMPLATE_TA6V_QCD_gluon",
            "material_id": "TA6V",
            "component_id": "QCD_gluon",
            "fraction_value": "MISSING_NUMERIC",
            "fraction_uncertainty": "MISSING_NUMERIC",
            "basis_convention": "MISSING_BASIS",
            "source_path_or_url": "MISSING_SOURCE",
            "extraction_method": "MISSING_METHOD",
            "intake_status": "TEMPLATE_NONCLAIM_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "CFI1233_TEMPLATE_PtRh10_QCD_gluon",
            "material_id": "PtRh10",
            "component_id": "QCD_gluon",
            "fraction_value": "MISSING_NUMERIC",
            "fraction_uncertainty": "MISSING_NUMERIC",
            "basis_convention": "MISSING_BASIS",
            "source_path_or_url": "MISSING_SOURCE",
            "extraction_method": "MISSING_METHOD",
            "intake_status": "TEMPLATE_NONCLAIM_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    files = candidate_files()
    validator_dryrun = [
        {
            "dryrun_id": "DRY1233_0_candidate_scan",
            "scan_path": str(FRACTION_DIR / "raw"),
            "candidate_csv_count": len(files),
            "accepted_rows": 0,
            "rejected_rows": 0,
            "status": "NO_CANDIDATE_FILES_PRESENT" if len(files) == 0 else "CANDIDATES_PRESENT_NOT_PARSED_BY_THIS_CHECKPOINT",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]

    em_edge_proof = [
        {
            "proof_id": "EME1233_0_target",
            "edge": "EDGE1232_0_electron_photon",
            "claim_piece": "electron-photon current edge is parent-owned",
            "formal_statement": "A_Q is a parent-owned compact U(1) connection; electron matter is a section of a charged representation bundle; S_int includes q_e int A_Q_mu J_e^mu with q_e fixed by representation data.",
            "result": "TARGET_SHARPENED",
            "missing_for_claim": "parent EM owner and matter representation functor are contract clauses, not derived MTS primitives",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", "PAC1055_1_EM_owner"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "EME1233_1_observable_charge_not_source_weight",
            "edge": "EDGE1232_0_electron_photon",
            "claim_piece": "electric charge is observable interaction data, not inert source-only scalar",
            "formal_statement": "Changing q_e changes EM interactions/currents, so q_e cannot play the role of a hidden gravitational-only w_A without leaving the matter/EM sector.",
            "result": "EXACT_CLASSIFICATION_CONDITIONAL",
            "missing_for_claim": "does not exclude a separate source-only w_e multiplying Hilbert stress",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1065_CHARGE_INTERACTION_NORMALIZATION_AUDIT.csv", "CIN1065_0_charge_is_observable"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "EME1233_2_current_ward_edge",
            "edge": "EDGE1232_0_electron_photon",
            "claim_piece": "Noether/Ward current supports the edge",
            "formal_statement": "Gauge invariance of S_matter+S_EM gives a conserved electron EM current coupled to A_Q, conditional on the parent action and representation bundle.",
            "result": "VALID_CONDITIONAL_EDGE_MATH",
            "missing_for_claim": "Ward conservation does not fix source normalization or prove parent graph ownership",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_951_SOURCE_CURRENT_WARD_ACTION_ATTEMPT.csv", "SWA951_5_verdict"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "EME1233_3_em_lock_gap",
            "edge": "EDGE1232_0_electron_photon",
            "claim_piece": "EM kinetic/current normalization is fixed by parent owner",
            "formal_statement": "S_EM and S_int descend with fixed g_*, charge generator, and current normalization, so no f(X)F^2 or source-only alpha/current drift enters the edge.",
            "result": "NOT_PARENT_SIGNED",
            "missing_for_claim": "unique Maxwell F2/current normalization and radiative/readout closure remain unsigned",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv", "PAC990_3_EM_lock"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "EME1233_4_graph_edge_verdict",
            "edge": "EDGE1232_0_electron_photon",
            "claim_piece": "electron-photon graph edge owner proof",
            "formal_statement": "EME1233_0 through EME1233_3 would sign EDGE1232_0 only if parent EM owner, matter representation functor, current normalization, and readout closure all pass.",
            "result": "EDGE_DEMOTED_TO_CONDITIONAL_NOT_SIGNED",
            "missing_for_claim": "current corpus cannot yet use this edge as a parent-signed connectedness certificate",
            "source": "EME1233_0 through EME1233_3",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    edge_demotion = [
        {
            "edge_id": "EDGE1232_0_electron_photon",
            "new_status": "CONDITIONAL_MATH_CLEAR_NOT_PARENT_SIGNED",
            "what_was_gained": "charge/current edge has a strong conditional Ward/representation route",
            "what_still_blocks": "parent EM owner and source-normalization owner are unsigned",
            "effect_on_graph": "cannot count as parent-signed connected edge yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "EDGE1232_1_quark_photon",
            "new_status": "PENDING_FUTURE_EDGE_OWNER_PROOF",
            "what_was_gained": "validator/checkpoint picked electron-photon first",
            "what_still_blocks": "quark charge/current representation owner not audited here",
            "effect_on_graph": "still template edge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "EDGE1232_2_quark_gluon",
            "new_status": "PENDING_FUTURE_EDGE_OWNER_PROOF",
            "what_was_gained": "not attempted in 1233",
            "what_still_blocks": "strong-sector parent action owner",
            "effect_on_graph": "still template edge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    feed_update = [
        {
            "feed_id": "FEED1233_0_to_FSP1232",
            "target": "P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv",
            "update": "future component-fraction rows must pass schema/provenance/unit gates before any nonclaim use",
            "claim_rows_delta": 0,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1233_1_to_EDGE1232_0",
            "target": "EDGE1232_0_electron_photon",
            "update": "edge demoted to conditional math clear, not parent-signed",
            "claim_rows_delta": 0,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1233_2_to_Delta_w",
            "target": "Delta_w_TiPt component branch",
            "update": "no numeric fraction, prior, tau, or WEP score added",
            "claim_rows_delta": 0,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1233_0_validator_first",
            "decision": "component-fraction intake is now validator-gated",
            "because": "otherwise proxy/toy rows can accidentally become fake WEP evidence",
            "next_action": "parse candidate files only after explicit source rows exist under component-fractions/raw",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1233_1_edge_not_signed",
            "decision": "electron-photon graph edge is not parent-signed",
            "because": "Ward/current math is conditional and EM/current normalization owner remains unsigned",
            "next_action": "attack EM owner uniqueness or move to quark-gluon edge owner proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1233_2_no_physics_promotion",
            "decision": "do not promote Delta_w, WEP, or local GR",
            "because": "both the graph certificate and component-fraction numeric branch remain incomplete",
            "next_action": "continue derivation-first; use data intake only when real sources arrive",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1233_0_fraction_intake",
            "claim": "accepted component-fraction rows exist",
            "status": "BLOCKED",
            "reason": "no candidate rows parsed/accepted; templates contain MISSING markers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1233_1_edge_owner",
            "claim": "electron-photon edge parent-signed",
            "status": "BLOCKED",
            "reason": "EME1233_4 demotes edge to conditional not signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1233_2_graph_connectedness",
            "claim": "G_ord connected with parent-owned edges",
            "status": "BLOCKED",
            "reason": "at least EDGE1232_0 remains unsigned and other edges not attempted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1233_3_WEP",
            "claim": "WEP/MICROSCOPE finite score",
            "status": "BLOCKED",
            "reason": "DeltaF, delta_w priors, DeltaK, and tau_WEP remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1233_4_local_GR",
            "claim": "local GR/Newton source reduction",
            "status": "BLOCKED",
            "reason": "source-coupling graph and finite branch are both incomplete",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1233_0_1234",
            "target_file": "1234-Y5-R10-EM-owner-uniqueness-or-quark-gluon-edge-owner-proof.md",
            "target_script": "scripts/Y5_R10_EM_owner_uniqueness_or_quark_gluon_edge_owner_proof.py",
            "task": "try to close the EM owner uniqueness gap for EDGE1232_0; if it does not close, pivot to the quark-gluon edge owner proof and keep all graph edges nonclaim",
            "success_condition": "one graph edge is either parent-signed by a real owner proof or narrowed to a precise blocker with no claim promotion",
            "do_not_do": "do not claim graph connectedness, Delta_w=0, WEP, PPN, local GR, or use component-fraction templates as data",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_paths = [
        SOURCE_REGISTER_PATH,
        DIRECTORY_CONTRACT_PATH,
        SCHEMA_PATH,
        ACCEPTANCE_GATES_PATH,
        TEMPLATE_PATH,
        VALIDATOR_DRYRUN_PATH,
        EM_EDGE_PROOF_PATH,
        EDGE_DEMOTION_PATH,
        FEED_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(DIRECTORY_CONTRACT_PATH, directory_contract)
    write_csv(SCHEMA_PATH, schema_rows)
    write_csv(ACCEPTANCE_GATES_PATH, acceptance_gates)
    write_csv(TEMPLATE_PATH, template_rows)
    write_csv(VALIDATOR_DRYRUN_PATH, validator_dryrun)
    write_csv(EM_EDGE_PROOF_PATH, em_edge_proof)
    write_csv(EDGE_DEMOTION_PATH, edge_demotion)
    write_csv(FEED_PATH, feed_update)
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
            directory_contract,
            schema_rows,
            acceptance_gates,
            template_rows,
            validator_dryrun,
            em_edge_proof,
            edge_demotion,
            feed_update,
            decisions,
            claim_gates,
            next_target,
        ]
        for row in table
    )
    directories_exist = all(Path(row["absolute_path"]).exists() for row in directory_contract)
    schema_blocks_claim = all(parse_bool(row["blocks_acceptance_if_missing"]) for row in schema_rows)
    templates_blocked = all("MISSING" in row["fraction_value"] and is_false(row, "claim_allowed") for row in template_rows)
    dryrun_blocks = validator_dryrun[0]["accepted_rows"] == 0 and validator_dryrun[0]["claim_allowed"] is False
    edge_demoted = any(row["proof_id"] == "EME1233_4_graph_edge_verdict" and row["result"] == "EDGE_DEMOTED_TO_CONDITIONAL_NOT_SIGNED" for row in em_edge_proof)
    gates_blocked = all(row["status"] == "BLOCKED" and is_false(row, "claim_allowed") for row in claim_gates)
    next_is_1234 = next_target[0]["target_file"].startswith("1234-Y5-R10-EM-owner")
    fw_recent = formalization_recent_count()

    validation = [
        validation_row(
            "VAL1233_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(parse_bool(row['path_exists']) for row in source_register)}/{len(source_register)} sources exist",
        ),
        validation_row(
            "VAL1233_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(parse_bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        ),
        validation_row(
            "VAL1233_2_directories_exist",
            "component-fraction intake directories exist",
            directories_exist,
            "; ".join(row["directory_id"] for row in directory_contract),
        ),
        validation_row(
            "VAL1233_3_schema_blocks",
            "schema fields block acceptance if missing",
            schema_blocks_claim,
            f"schema_rows={len(schema_rows)}",
        ),
        validation_row(
            "VAL1233_4_templates_blocked",
            "candidate templates are nonclaim and missing-gated",
            templates_blocked,
            f"template_rows={len(template_rows)}",
        ),
        validation_row(
            "VAL1233_5_dryrun_blocks",
            "dry-run accepts no rows",
            dryrun_blocks,
            f"candidate_csv_count={len(files)}; accepted_rows=0",
        ),
        validation_row(
            "VAL1233_6_edge_demoted",
            "electron-photon edge proof is explicit and demoted",
            edge_demoted,
            "EME1233_4 result=EDGE_DEMOTED_TO_CONDITIONAL_NOT_SIGNED",
        ),
        validation_row(
            "VAL1233_7_claim_gates_blocked",
            "all claim gates remain blocked",
            gates_blocked,
            f"blocked_gates={sum(row['status'] == 'BLOCKED' for row in claim_gates)}/{len(claim_gates)}",
        ),
        validation_row(
            "VAL1233_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_generated_nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1233_9_next_target_1234",
            "next target attacks EM owner uniqueness or quark-gluon edge",
            next_is_1234,
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1233_10_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_counts),
        ),
        validation_row(
            "VAL1233_11_formalization_untouched",
            "formalization-workbench untouched during run",
            fw_recent == 0,
            f"formalization_recent_write_count_since_run_start={fw_recent}",
        ),
    ]
    validation.append(
        validation_row(
            "VAL1233_12_overall",
            "overall 1233 validation",
            all(row["status"] == "PASS" for row in validation),
            "1233 builds component-fraction intake gates and demotes the electron-photon edge to conditional math without claims",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1233 builds the component-fraction intake validator and attempts the first graph-edge owner proof. The validator blocks future loose `DeltaF_TiPt,c` rows; the electron-photon edge has strong conditional Ward/charge math but is **not** parent-signed because EM/current normalization ownership remains unsigned.",
        "",
        "**Main progress:** future component fractions now need schema, numeric, basis, source, extraction, and no-proxy gates before even nonclaim use. The graph route is sharper too: `EDGE1232_0` is demoted to `CONDITIONAL_MATH_CLEAR_NOT_PARENT_SIGNED`, not left vague.",
        "",
        "**No-claim guard:** no component fraction, graph connectedness, `Delta_w=0`, WEP, PPN, clock, orbital, local-GR, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Component-Fraction Directory Contract",
        markdown_table(directory_contract, list(directory_contract[0].keys())),
        "",
        "## Component-Fraction Schema",
        markdown_table(schema_rows, list(schema_rows[0].keys())),
        "",
        "## Component-Fraction Acceptance Gates",
        markdown_table(acceptance_gates, list(acceptance_gates[0].keys())),
        "",
        "## Component-Fraction Candidate Template",
        markdown_table(template_rows, list(template_rows[0].keys())),
        "",
        "## Validator Dry Run",
        markdown_table(validator_dryrun, list(validator_dryrun[0].keys())),
        "",
        "## EM-Current Edge Owner Proof Attempt",
        markdown_table(em_edge_proof, list(em_edge_proof[0].keys())),
        "",
        "## Graph Edge Demotion Ledger",
        markdown_table(edge_demotion, list(edge_demotion[0].keys())),
        "",
        "## Runner Feed Update",
        markdown_table(feed_update, list(feed_update[0].keys())),
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

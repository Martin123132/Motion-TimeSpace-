from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1078-parent-action-object-language-measure-current-owner-proof-stack" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1078_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1078_WEP_BOUND_IMPORT.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def local_bound_row(row_id: str) -> dict[str, str]:
    for row in read_csv(LOCAL_BOUNDS):
        if row.get("row_id") == row_id:
            return row
    raise ValueError(f"missing local bound row {row_id}")


def split_reference(reference: str) -> tuple[str, str]:
    parts = [part.strip() for part in reference.split(";")]
    url = next((part for part in parts if part.startswith("http")), "")
    doi = next((part.replace("doi:", "").strip() for part in parts if part.lower().startswith("doi:")), "")
    return url, doi


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1078_0_1077_next", "source-intake/mts_residuals/P8_Y5_R10_1077_NEXT_TARGET.csv", "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md", "1077 handoff."),
        ("SRC1078_1_1077_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1077_VALIDATION.csv", "V1077_SUMMARY", "1077 validation summary."),
        ("SRC1078_2_1077_theorem", "source-intake/mts_residuals/P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv", "WCO1077_1_conditional_theorem", "conditional theorem-zero source."),
        ("SRC1078_3_1077_clauses", "source-intake/mts_residuals/P8_Y5_R10_1077_CLAUSE_SIGNATURE_MATRIX.csv", "CLAUSE1077_2_current_owner", "unsigned clause matrix."),
        ("SRC1078_4_1077_counterexamples", "source-intake/mts_residuals/P8_Y5_R10_1077_ZERO_THEOREM_COUNTEREXAMPLE_AUDIT.csv", "CE1077_0_species_action_weight", "surviving counterexample list."),
        ("SRC1078_5_1077_finite", "source-intake/mts_residuals/P8_Y5_R10_1077_FINITE_ROUTE_REQUIREMENTS.csv", "FIN1077_2_C_parent", "finite route requirements."),
        ("SRC1078_6_1077_material", "source-intake/mts_residuals/P8_Y5_R10_1077_MATERIAL_VECTOR_SOURCE_ROW_STATUS.csv", "MVS1077_0_toy_delta_TA6V_minus_PtRh10", "toy material vector status."),
        ("SRC1078_7_1066_scalar", "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_5_verdict", "object-language scalar exclusion attempt."),
        ("SRC1078_8_1067_action", "source-intake/mts_residuals/P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv", "ASO1067_5_verdict", "action-scale owner attempt."),
        ("SRC1078_9_1062_parent", "source-intake/mts_residuals/P8_Y5_R10_1062_PARENT_PRODUCT_THEOREM_ATTEMPT.csv", "THM1062_6_verdict", "prior parent theorem attempt."),
        ("SRC1078_10_1076_owner", "source-intake/mts_residuals/P8_Y5_R10_1076_COUPLING_OWNER_GATES.csv", "OWN1076_2_current_owner", "coupling owner gate source."),
        ("SRC1078_11_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        needle_found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle_found).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def object_language_rows() -> list[dict[str, str]]:
    return [
        {
            "object_language_id": "OL1078_0_target",
            "claim": "parent object-language typing signs allowed matter-action arguments",
            "allowed_argument_types": "observed geometry/coframe/metric; matter fields; gauge connections/currents; representation constants; universal constants",
            "forbidden_argument_types": "species-indexed inert source-only scalar w_A; disconnected label weight not carried by a field/current/representation",
            "proof_attempt": "promote 1066 from exclusion taste to a syntactic theorem of the parent action object language",
            "result": "TARGET_SHARPENED",
            "gap": "grammar exists as desired contract, not as a derived theorem from parent MTS primitives",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "object_language_id": "OL1078_1_positive_syntax",
            "claim": "positive syntax can list legitimate parent arguments",
            "allowed_argument_types": "fields, currents, representation data, orientation/measure data, and universal constants",
            "forbidden_argument_types": "bare species source weights outside those objects",
            "proof_attempt": "if every source term is a functorial expression of these objects, relative composition weights cannot be inserted after the fact",
            "result": "CONDITIONAL_FROM_1066",
            "gap": "the functorial-expression premise is still a parent axiom, not derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "object_language_id": "OL1078_2_forbidden_slot",
            "claim": "species-indexed inert w_A is forbidden",
            "allowed_argument_types": "observable species data only when carried by a field/current/representation",
            "forbidden_argument_types": "independent action multiplier w_A multiplying S_A",
            "proof_attempt": "show w_A has no transformation law, no current, no variation, and no representation owner in the parent category",
            "result": "NOT_PARENT_SIGNED",
            "gap": "absence of an owner is evidence of ugliness, not a proof of impossibility",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "object_language_id": "OL1078_3_counterexample",
            "claim": "disconnected species constants are impossible",
            "allowed_argument_types": "connected matter functor with one normalization",
            "forbidden_argument_types": "simple-object label constants c_A or w_A",
            "proof_attempt": "try to kill label constants by connectedness of the matter functor",
            "result": "COUNTEREXAMPLE_SURVIVES",
            "gap": "a direct-sum matter category can still carry independent constants unless the parent functor forbids them",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "object_language_id": "OL1078_4_verdict",
            "claim": "object-language proof closes theorem-zero premise",
            "allowed_argument_types": "positive list retained as contract",
            "forbidden_argument_types": "source-only scalar slot",
            "proof_attempt": "assemble positive syntax, forbidden-slot argument, and counterexample audit",
            "result": "OBJECT_LANGUAGE_NOT_SIGNED",
            "gap": "counterexample survives without a parent-derived object language",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def action_measure_rows() -> list[dict[str, str]]:
    return [
        {
            "action_measure_id": "AM1078_0_target",
            "claim": "one hbar_parent/measure owner fixes ordinary matter normalization",
            "proof_attempt": "show S_parent/hbar_parent has a single integration measure and a single action scale for all ordinary matter sectors",
            "result": "TARGET_SHARPENED",
            "gap": "this would be the cleanest way to kill w_A S_A",
            "blocks_if_unsigned": "species action weights remain legal finite WEP branch inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "action_measure_id": "AM1078_1_classical_eom",
            "claim": "classical equations alone fix action normalization",
            "proof_attempt": "use Euler-Lagrange equations to remove a constant multiplier per disconnected matter sector",
            "result": "OBSTRUCTION_ACKNOWLEDGED",
            "gap": "classical equations are insensitive to an overall sector multiplier until the sector couples as a source",
            "blocks_if_unsigned": "relative source strength can enter without changing isolated free-fall equations",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "action_measure_id": "AM1078_2_quantum_measure",
            "claim": "path-integral/statistical measure owner kills independent w_A S_A",
            "proof_attempt": "if all matter histories are weighted by the same parent hbar/measure, sector-specific action rescalings are not gauge-free choices",
            "result": "CONDITIONAL_FROM_1067",
            "gap": "1067 supplies a good conditional route but not a parent derivation",
            "blocks_if_unsigned": "finite WEP product must retain normalization coefficient C_parent",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "action_measure_id": "AM1078_3_missing_parent_measure",
            "claim": "parent corpus already contains a signed measure axiom",
            "proof_attempt": "search prior owner results for hbar/measure closure",
            "result": "NOT_PARENT_SIGNED",
            "gap": "no parent statistical/measure axiom is signed strongly enough to carry WEP theorem-zero",
            "blocks_if_unsigned": "species-blind action measure remains a closure requirement",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "action_measure_id": "AM1078_4_verdict",
            "claim": "action-measure proof closes theorem-zero premise",
            "proof_attempt": "assemble classical, quantum-measure, and source-coupling checks",
            "result": "ACTION_MEASURE_NOT_SIGNED",
            "gap": "the needed measure owner is plausible but currently an unsigned parent contract",
            "blocks_if_unsigned": "theorem-zero is closure-only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def current_owner_rows() -> list[dict[str, str]]:
    return [
        {
            "current_owner_id": "CO1078_0_target",
            "claim": "one current/source normalization owner fixes all ordinary matter source couplings",
            "proof_attempt": "derive the gravitational source and any gauge/Noether current from one parent current functor before readout",
            "result": "TARGET_SHARPENED",
            "gap": "current owner must be prior to material/readout projection",
            "blocks_if_unsigned": "J_A -> c_A J_A remains a legal source-normalization counterexample",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "current_owner_id": "CO1078_1_noether_route",
            "claim": "Noether/gauge representation data fix source normalization",
            "proof_attempt": "use representation charges to own gauge-current normalization",
            "result": "PARTIAL_FOR_GAUGE_ONLY",
            "gap": "gauge-current normalization does not by itself fix the Hilbert gravitational source normalization for WEP",
            "blocks_if_unsigned": "composition-dependent mass/source response can still enter",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "current_owner_id": "CO1078_2_hilbert_source_route",
            "claim": "Hilbert stress from variation before readout owns the gravitational source",
            "proof_attempt": "define T_mu_nu = delta S_matter / delta e_obs before any post-variation material selector is allowed",
            "result": "CONDITIONAL",
            "gap": "variation-before-readout is a strong contract, but the parent readout/order axiom is not signed here",
            "blocks_if_unsigned": "post-variation selector F(T_A,A) can mimic WEP residuals",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "current_owner_id": "CO1078_3_current_rescaling_counterexample",
            "claim": "current rescaling J_A -> c_A J_A is impossible",
            "proof_attempt": "try to absorb c_A into representation charge or field normalization",
            "result": "COUNTEREXAMPLE_SURVIVES",
            "gap": "without a single owner, source current normalization can be moved into a species coefficient",
            "blocks_if_unsigned": "finite route needs C_parent and source/material vectors",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "current_owner_id": "CO1078_4_verdict",
            "claim": "current-owner proof closes theorem-zero premise",
            "proof_attempt": "assemble Noether, Hilbert-source, and rescaling checks",
            "result": "CURRENT_OWNER_NOT_SIGNED",
            "gap": "Noether route is partial; Hilbert/readout route is conditional; rescaling counterexample survives",
            "blocks_if_unsigned": "WEP theorem-zero cannot be claimed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def counterexample_kill_rows() -> list[dict[str, str]]:
    return [
        {
            "counterexample_id": "CEK1078_0_species_action_weight",
            "counterexample": "S_matter = sum_A w_A S_A",
            "kill_clause_required": "single parent hbar/action-measure owner plus no inert source-only scalar slot",
            "proof_status": "UNSIGNED",
            "result": "SURVIVES",
            "why_survives": "classical equations do not kill sector action multipliers before source coupling",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CEK1078_1_current_rescaling",
            "counterexample": "J_A -> c_A J_A",
            "kill_clause_required": "single current/source normalization owner",
            "proof_status": "UNSIGNED",
            "result": "SURVIVES",
            "why_survives": "current owner is not parent-signed; Noether route is gauge-only partial",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CEK1078_2_disconnected_material_components",
            "counterexample": "independent constants on disconnected material components",
            "kill_clause_required": "connected parent matter functor or no label-only constants theorem",
            "proof_status": "UNSIGNED",
            "result": "SURVIVES",
            "why_survives": "direct-sum matter sectors can carry label constants unless the parent object language forbids them",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CEK1078_3_post_variation_selector",
            "counterexample": "post-variation selector F(T_A,A)",
            "kill_clause_required": "variation-before-readout and official readout-kernel closure",
            "proof_status": "UNSIGNED",
            "result": "SURVIVES",
            "why_survives": "source/readout ordering remains a contract, not a signed theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def theorem_zero_demotion_rows() -> list[dict[str, str]]:
    return [
        {
            "demotion_id": "TZD1078_0_conditional",
            "statement": "the exact conditional theorem-zero from 1077 is retained",
            "status": "CONDITIONAL_THEOREM_RETAINED",
            "reason": "if object-language, action-measure, and current-owner premises are signed, P_WEP=0 follows",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "demotion_id": "TZD1078_1_missing_premises",
            "statement": "core premises remain unsigned",
            "status": "OBJECT_ACTION_CURRENT_UNSIGNED",
            "reason": "OL1078_4_verdict; AM1078_4_verdict; CO1078_4_verdict",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "demotion_id": "TZD1078_2_demote",
            "statement": "theorem-zero route is demoted to closure-only",
            "status": "CLOSURE_ONLY_UNSIGNED",
            "reason": "surviving counterexamples are legal until the parent action signs the owner clauses",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "demotion_id": "TZD1078_3_finite_route",
            "statement": "finite WEP route remains sourced-input route",
            "status": "FINITE_ROUTE_RETAINED_AS_SOURCED_INPUT_ONLY",
            "reason": "requires real material vector, Earth/source vector, C_parent owner, and official readout kernel",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "demotion_id": "TZD1078_4_verdict",
            "statement": "no WEP/local-GR product claim follows from 1078",
            "status": "NO_WEP_CLAIM",
            "reason": "conditional theorem is not parent-signed and finite product inputs are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def finite_route_demotion_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "FRD1078_0_material_vector",
            "object": "R_TA6V - R_PtRh10",
            "status": "TOY_ONLY_NONCLAIM",
            "required_to_unblock": "source-backed material response vector for actual MICROSCOPE composition/readout convention",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "FRD1078_1_source_vector",
            "object": "R_source^Earth",
            "status": "MISSING_SOURCE_VECTOR",
            "required_to_unblock": "source worldtube/current vector or common-mode theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "FRD1078_2_coupling_owner",
            "object": "C_parent coupling owner",
            "status": "MISSING_COUPLING_OWNER",
            "required_to_unblock": "signed current/source normalization owner or sourced finite coefficient",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "FRD1078_3_readout_kernel",
            "object": "K_MICROSCOPE official readout kernel",
            "status": "MISSING_OFFICIAL_ARRAYS",
            "required_to_unblock": "official segment-level orbit/readout arrays or accepted reconstruction contract",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "FRD1078_4_product_runner",
            "object": "WEP product runner",
            "status": "MUST_REFUSE",
            "required_to_unblock": "numeric claim-valid prediction row and numeric sourced bound row",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def product_prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1078_0_WEP_theorem_zero_or_finite_route_nonclaim",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_SIGNED_THEOREM_ZERO_OR_FINITE_SOURCED_VECTORS",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1078_THEOREM_ZERO_DEMOTION.csv",
            "inputs_present": "conditional theorem;demotion gates;bound row",
            "required_inputs": "signed object language; signed action measure; signed current owner OR real material/source/C_parent/readout finite vectors",
            "derivation_status": "THEOREM_ZERO_CLOSURE_ONLY_FINITE_ROUTE_MISSING",
            "valid_for_claim": "false",
            "notes": "runner must refuse because product value is a missing marker, not a prediction",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    row = local_bound_row("R1_WEP_source_charge")
    url, doi = split_reference(row.get("reference_path_or_url", ""))
    return [
        {
            "bound_id": "BOUND1078_0_MICROSCOPE_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": row["upper_bound"],
            "bound_units": row["units"],
            "bound_source": url,
            "source_row": f"{row['dataset_id']}:{row['row_id']};doi:{doi}",
            "bound_type": "upper_abs_WEP_proxy_bound",
            "valid_for_claim": "true",
            "notes": "source-backed numeric bound only; prediction remains invalid",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1078_0_WEP_parent_action_product_stub",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "passed_rows": str(status.get("passed_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject closure-only theorem-zero and missing finite vectors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1078_0_conditional_theorem",
            "claim_component": "conditional theorem-zero",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "conditional theorem is retained but cannot be used as a claim until premises are signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1078_1_object_language",
            "claim_component": "parent object-language typing",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "OL1078_4_verdict=OBJECT_LANGUAGE_NOT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1078_2_action_measure",
            "claim_component": "species-blind action measure",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "AM1078_4_verdict=ACTION_MEASURE_NOT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1078_3_current_owner",
            "claim_component": "single current/source owner",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "CO1078_4_verdict=CURRENT_OWNER_NOT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1078_4_finite_vectors",
            "claim_component": "finite WEP source/material vectors",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "FRD1078 gates retain toy/missing source, coupling, and official readout inputs",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1078_5_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": "false",
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1078_0_conditional_theorem",
            "decision": "retain conditional theorem-zero as a closure theorem",
            "because": "the algebraic logic is clean if object/action/current owner clauses are signed",
            "next_action": "do not use it as evidence until the premises are parent-derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1078_1_demote_theorem_zero",
            "decision": "demote theorem-zero to closure-only unsigned",
            "because": "all three proof stacks leave counterexamples alive",
            "next_action": "route WEP through finite sourced inputs unless a narrow owner proof is found",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1078_2_finite_route",
            "decision": "keep finite WEP as sourced-input route",
            "because": "material, source, coupling-owner, and official readout vectors are not complete",
            "next_action": "source real finite WEP vectors if the current-owner proof fails",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1078_3_next_target",
            "decision": "try the narrow current/source normalization owner proof first",
            "because": "it is the least broad premise and the one that blocks both theorem-zero and finite coefficient ownership",
            "next_action": "write 1079 current-owner narrow proof or finite WEP source-vector contract",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1078_0_1079",
            "next_target": "1079-Y5-R10-parent-current-owner-narrow-proof-or-finite-WEP-source-vector.md",
            "objective": "try the narrow current/source normalization owner proof first; if it remains unsigned, begin finite WEP sourced-input acquisition with a real source vector/material tensor contract.",
            "include": "current functor owner; Hilbert source variation-before-readout; representation/current normalization; source-vector contract; material-vector contract; runner refusal",
            "exclude": "tau=1; Delta_w=0 by taste; toy vector as evidence; measured-G absorption; public claim; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_rows_parse(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
    except csv.Error:
        return False
    return True


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    object_rows: list[dict[str, str]],
    action_rows: list[dict[str, str]],
    current_rows: list[dict[str, str]],
    counter_rows: list[dict[str, str]],
    demotion_rows: list[dict[str, str]],
    finite_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1078_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1078_1_object_language_unsigned", any(row["object_language_id"] == "OL1078_4_verdict" and row["result"] == "OBJECT_LANGUAGE_NOT_SIGNED" for row in object_rows), "object-language proof does not close"))
    checks.append(("V1078_2_action_measure_unsigned", any(row["action_measure_id"] == "AM1078_4_verdict" and row["result"] == "ACTION_MEASURE_NOT_SIGNED" for row in action_rows), "action-measure proof does not close"))
    checks.append(("V1078_3_current_owner_unsigned", any(row["current_owner_id"] == "CO1078_4_verdict" and row["result"] == "CURRENT_OWNER_NOT_SIGNED" for row in current_rows), "current-owner proof does not close"))
    checks.append(("V1078_4_counterexamples_survive", len(counter_rows) == 4 and all(row["result"] == "SURVIVES" for row in counter_rows), "all 1077 theorem-zero counterexamples still survive"))
    checks.append(("V1078_5_theorem_zero_demoted", any(row["demotion_id"] == "TZD1078_2_demote" and row["status"] == "CLOSURE_ONLY_UNSIGNED" for row in demotion_rows), "theorem-zero is explicitly demoted to closure-only"))
    checks.append(("V1078_6_finite_route_blocks", len(finite_rows) == 5 and all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in finite_rows), "finite WEP route gates all block claims"))
    checks.append(("V1078_7_prediction_nonclaim_missing", any("MISSING_SIGNED_THEOREM_ZERO" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows), "prediction row remains missing theorem or finite sourced vectors"))
    checks.append(("V1078_8_bound_numeric", bool(bound_rows_) and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "bound import is positive numeric"))
    checks.append(("V1078_9_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "runner reports no valid prediction rows and claim false"))
    checks.append(("V1078_10_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1078_11_next_target", any(row["next_target"].startswith("1079-Y5-R10-parent-current-owner") for row in next_rows), "1079 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1078_12_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1078_13_csv_parse", all(path.exists() and csv_rows_parse(path) for path in outputs.values() if path.suffix == ".csv" and path.name != "P8_Y5_BRR545_1078_VALIDATION.csv"), "all 1078 CSV outputs parse cleanly"))
    checks.append(("V1078_14_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1078_SUMMARY", True, "theorem-zero demoted to closure-only; finite WEP kept as sourced-input route; WEP/product claim blocked"))
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]


def write_doc(
    source_rows: list[dict[str, str]],
    object_rows: list[dict[str, str]],
    action_rows: list[dict[str, str]],
    current_rows: list[dict[str, str]],
    counter_rows: list[dict[str, str]],
    demotion_rows: list[dict[str, str]],
    finite_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparison_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1078 - Parent action object-language, measure, current-owner proof stack",
            "",
            "## Current verdict",
            "1078 tries to close the WEP theorem-zero route from inside the parent action. It does not get the signatures: object-language typing, action-measure ownership, and current/source normalization ownership all remain unsigned. So the conditional theorem is retained as a useful closure theorem, but theorem-zero is demoted to closure-only and finite WEP stays a sourced-input route.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Object-language proof attempt",
            md_table(object_rows, ["object_language_id", "claim", "result", "gap"]),
            "## Action-measure proof attempt",
            md_table(action_rows, ["action_measure_id", "claim", "result", "gap"]),
            "## Current-owner proof attempt",
            md_table(current_rows, ["current_owner_id", "claim", "result", "gap"]),
            "## Counterexample kill matrix",
            md_table(counter_rows, ["counterexample_id", "counterexample", "kill_clause_required", "result", "why_survives"]),
            "## Theorem-zero demotion",
            md_table(demotion_rows, ["demotion_id", "statement", "status", "reason", "claim_allowed"]),
            "## Finite route demotion gates",
            md_table(finite_rows, ["gate_id", "object", "status", "required_to_unblock", "claim_allowed"]),
            "## Nonclaim product candidate",
            md_table(prediction_rows, ["prediction_id", "product_symbol", "product_value", "derivation_status", "valid_for_claim"]),
            "## Bound import",
            md_table(bound_rows_, ["bound_id", "product_symbol", "bound_value", "bound_units", "valid_for_claim"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparison_rows, ["comparison_id", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    object_rows = object_language_rows()
    action_rows = action_measure_rows()
    current_rows = current_owner_rows()
    counter_rows = counterexample_kill_rows()
    demotion_rows = theorem_zero_demotion_rows()
    finite_rows = finite_route_demotion_gate_rows()
    prediction_rows = product_prediction_rows()
    bound_rows_ = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1078_SOURCE_REGISTER.csv",
        "object_language": OUT / "P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv",
        "action_measure": OUT / "P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv",
        "current_owner": OUT / "P8_Y5_R10_1078_CURRENT_OWNER_PROOF_ATTEMPT.csv",
        "counterexamples": OUT / "P8_Y5_R10_1078_COUNTEREXAMPLE_KILL_MATRIX.csv",
        "demotion": OUT / "P8_Y5_R10_1078_THEOREM_ZERO_DEMOTION.csv",
        "finite_gates": OUT / "P8_Y5_R10_1078_FINITE_ROUTE_DEMOTION_GATES.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1078_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1078_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1078_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1078_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1078_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1078_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["object_language"], object_rows)
    write_csv(outputs["action_measure"], action_rows)
    write_csv(outputs["current_owner"], current_rows)
    write_csv(outputs["counterexamples"], counter_rows)
    write_csv(outputs["demotion"], demotion_rows)
    write_csv(outputs["finite_gates"], finite_rows)
    write_csv(outputs["prediction"], prediction_rows, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    claim_rows = claim_gate_rows(product_status)

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_result["comparisons"])
    write_csv(outputs["claim_gates"], claim_rows)

    remove_pycache()
    validation_rows = validate_outputs(
        outputs,
        source_rows,
        object_rows,
        action_rows,
        current_rows,
        counter_rows,
        demotion_rows,
        finite_rows,
        prediction_rows,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        object_rows,
        action_rows,
        current_rows,
        counter_rows,
        demotion_rows,
        finite_rows,
        prediction_rows,
        bound_rows_,
        product_status_rows_,
        product_result["comparisons"],
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()

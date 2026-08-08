from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1417-Y5-R10-RAB-parent-object-language-constructor-exhaustion-or-qbar-source-acquisition.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1417_SOURCE_REGISTER.csv"
CONSTRUCTOR_LIST_PATH = SRC_DIR / "P8_Y5_R10_1417_PRIMITIVE_CONSTRUCTOR_LIST_ATTEMPT.csv"
PROOF_AUDIT_PATH = SRC_DIR / "P8_Y5_R10_1417_CONSTRUCTOR_EXHAUSTION_PROOF_AUDIT.csv"
COUNTERMODEL_PATH = SRC_DIR / "P8_Y5_R10_1417_LIVE_CONSTRUCTOR_COUNTERMODEL_LEDGER.csv"
QBAR_ACQUISITION_PATH = SRC_DIR / "P8_Y5_R10_1417_QBAR_SOURCE_WEIGHT_ACQUISITION_ROWS.csv"
ARENA_GATE_PATH = SRC_DIR / "P8_Y5_R10_1417_ARENA_PROJECTION_GATE.csv"
DECISION_PATH = SRC_DIR / "P8_Y5_R10_1417_DECISION_LEDGER.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1417_CLAIM_GATE.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1417_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1417_VALIDATION.csv"

GENERATED_UTC = datetime.now(timezone.utc).isoformat()
STATUS = "Y5_R10_1417_constructor_exhaustion_not_proved_qbar_source_acquisition_rows_written_nonclaim"
CLAIM_CEILING = (
    "parent_object_language_constructor_exhaustion_attempt_and_qbar_source_weight_acquisition_only_"
    "no_WEP_pass_no_Rsource_pass_no_Newton_no_R10_no_PPN_no_local_GR_pass"
)


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def write_csv(relative_path: Path, rows: list[dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {relative_path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def anchor_found(relative_path: str, anchor: str) -> bool:
    path = ROOT / relative_path
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1417_0_1416_doc",
            "source_path": "1416-Y5-R10-RAB-source-only-species-slot-and-current-rescaling-ban-or-Rsource-bound-row.md",
            "anchor": "NEXT1416_0_1417",
            "role": "previous checkpoint selects parent object-language constructor exhaustion",
        },
        {
            "source_id": "SRC1417_1_1416_qbar",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1416_FIRST_RSOURCE_COEFFICIENT_ROW.csv",
            "anchor": "RSC1416_0_qbar_source_weight",
            "role": "first R_source finite coefficient row to fill if theorem fails",
        },
        {
            "source_id": "SRC1417_2_1338_object_language",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv",
            "anchor": "OLT1338_6_verdict",
            "role": "object-language theorem previously not derived",
        },
        {
            "source_id": "SRC1417_3_1338_closure",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1338_NO_SOURCE_SLOT_CLOSURE_CONDITION.csv",
            "anchor": "CLOS1338_2_no_source_only_species_slot",
            "role": "sharp closure clause Hom(SpeciesLabel,Coeff_active_source)=empty",
        },
        {
            "source_id": "SRC1417_4_1220_signature",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
            "anchor": "PTOL1220_7_verdict",
            "role": "typed object-language signature not derived",
        },
        {
            "source_id": "SRC1417_5_1236_certificate",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
            "anchor": "CERT1236_6_current_verdict",
            "role": "certificate schema valid but not parent-derived",
        },
        {
            "source_id": "SRC1417_6_1219_functor",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1219_TYPED_VISIBLE_COEFFICIENT_FUNCTOR_ATTEMPT.csv",
            "anchor": "TVC1219_6_verdict",
            "role": "typed visible coefficient functor exact condition but unsigned",
        },
        {
            "source_id": "SRC1417_7_1065_grammar",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv",
            "anchor": "PGG1065_5_verdict",
            "role": "no-source-only-slot grammar conditional not parent-signed",
        },
        {
            "source_id": "SRC1417_8_1066_source_scalar",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
            "anchor": "SSE1066_5_verdict",
            "role": "source-scalar exclusion exact as conditional theorem only",
        },
        {
            "source_id": "SRC1417_9_1076_owner",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1076_COUPLING_OWNER_GATES.csv",
            "anchor": "OWN1076_0_parent_object_language",
            "role": "parent coupling basis and source-current owner remain missing",
        },
        {
            "source_id": "SRC1417_10_1310_qbar",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1310_QC_COEFFICIENT_ACQUISITION_NONCLAIM.csv",
            "anchor": "QCA1310_5_qbar_source_weight",
            "role": "qbar_source_weight acquisition row still missing source-weight theorem or coefficient",
        },
        {
            "source_id": "SRC1417_11_1044_component",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv",
            "anchor": "QBC1044_3_qbar_source_weight",
            "role": "qbar_source_weight is a retained component of qbar_XT envelope",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def constructor_list_rows() -> list[dict[str, Any]]:
    return [
        {
            "constructor_id": "PCL1417_0_MTS_primitives",
            "sort_or_constructor": "Motion-Time-Space primitives",
            "candidate_domain": "primitive motion flow, temporal ordering, spatial/metric incidence",
            "allowed_output": "parent kinematic/geometric data before ordinary matter readout",
            "excludes_source_slot_if": "this primitive list is complete and has no SpeciesLabel -> active-source coefficient constructor",
            "current_status": "PRIMITIVE_LIST_NOT_AUTHORITATIVELY_EXHAUSTED",
            "blocking_gap": "no single corpus source proves these are all parent constructors",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "constructor_id": "PCL1417_1_quotient_map",
            "sort_or_constructor": "q: Phi_parent -> Q_obs",
            "candidate_domain": "parent fields modulo unobservable/local vertical structure",
            "allowed_output": "observed frame/coframe/connection and quotient-visible fields",
            "excludes_source_slot_if": "ordinary matter and coefficients factor through q plus fixed representation data",
            "current_status": "EXACT_IF_FACTORING_PARENT_SIGNED",
            "blocking_gap": "factor-through-q is repeatedly written as a contract, not derived as the unique syntax",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "constructor_id": "PCL1417_2_observed_frame",
            "sort_or_constructor": "e_obs(q(Phi)), omega_obs(e_obs)",
            "candidate_domain": "descended geometry",
            "allowed_output": "metric/coframe coupling shared by all ordinary matter",
            "excludes_source_slot_if": "all active sources are Hilbert/coframe variations of one descended matter action",
            "current_status": "CONDITIONAL_GR_LIKE_ROUTE",
            "blocking_gap": "single source-current owner and variation-before-readout remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "constructor_id": "PCL1417_3_matter_bundle",
            "sort_or_constructor": "Psi_A, Theta_rep,A",
            "candidate_domain": "ordinary species fields and measured representation constants",
            "allowed_output": "masses, charges, couplings, internal representation data, stress-energy after variation",
            "excludes_source_slot_if": "SpeciesLabel A appears only as representation/matter data, never as active-source multiplier",
            "current_status": "SPLIT_NOT_PARENT_PROVED",
            "blocking_gap": "the representation-vs-source-coefficient split is exactly what must be proved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "constructor_id": "PCL1417_4_coefficient_ring",
            "sort_or_constructor": "Coeff_visible[O]",
            "candidate_domain": "functions of Q_obs, fixed representation/topological data, universal constants",
            "allowed_output": "operator coefficients for visible sector terms",
            "excludes_source_slot_if": "Coeff_active_source has no SpeciesLabel argument and no hidden/source-only scalar target",
            "current_status": "POWERFUL_TYPED_RULE_NOT_DERIVED",
            "blocking_gap": "typed coefficient ring is a clean theorem if signed, but currently a closure grammar",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "constructor_id": "PCL1417_5_action_measure_owner",
            "sort_or_constructor": "single action scale, measure, and current owner",
            "candidate_domain": "parent variational measure, hbar/action normalization, Hilbert source current",
            "allowed_output": "one total source T_total and common source normalization",
            "excludes_source_slot_if": "species action multipliers are gauge/quotient redundant or impossible",
            "current_status": "MISSING_PARENT_OWNER",
            "blocking_gap": "w_A S_A changes Hilbert source/path-integral weight unless a parent owner kills it",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "constructor_id": "PCL1417_6_readout_closure",
            "sort_or_constructor": "S_eff/readout projection",
            "candidate_domain": "effective actions, clocks, spectroscopy, WEP readout, local/R10 projections",
            "allowed_output": "observable coefficients preserving the same sorted parent domain",
            "excludes_source_slot_if": "readout/EFT cannot regenerate SpeciesLabel -> Coeff_active_source",
            "current_status": "UNSIGNED_TRANSFER_GATE",
            "blocking_gap": "bare syntax zero would not transfer to tests without this closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "constructor_id": "PCL1417_7_verdict",
            "sort_or_constructor": "primitive constructor exhaustion",
            "candidate_domain": "PCL1417_0 through PCL1417_6",
            "allowed_output": "Hom(SpeciesLabel,Coeff_active_source)=empty as theorem",
            "excludes_source_slot_if": "all primitive, quotient, matter, coefficient, measure, and readout clauses are parent-derived",
            "current_status": "CONSTRUCTOR_EXHAUSTION_NOT_PROVED",
            "blocking_gap": "exact route is identified, but parent primitive completeness and action/measure owner are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def proof_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "PEX1417_0_target",
            "theorem_clause": "derive Hom(SpeciesLabel,Coeff_active_source)=empty",
            "test": "show no admissible parent constructor maps ordinary species/source labels into active-source coefficients",
            "evidence": "CLOS1338_2_no_source_only_species_slot names the exact clause",
            "result": "TARGET_EXACT",
            "missing": "parent primitive constructor exhaustion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "PEX1417_1_sort_exhaustion",
            "theorem_clause": "complete primitive sort list",
            "test": "Motion/Time/Space plus quotient, observed frame, matter bundle, representation data, and universal constants are all parent sorts",
            "evidence": "CERT1236_0_parent_sorts and PTOL1220_0_parent_domain",
            "result": "GRAMMAR_WRITTEN_NOT_DERIVED",
            "missing": "source showing these sorts are forced by MTS primitives rather than adopted as discipline",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "PEX1417_2_no_species_to_source_morphism",
            "theorem_clause": "SpeciesLabel cannot feed Coeff_active_source",
            "test": "Coeff_active_source domain excludes SpeciesLabel while allowing measured representation constants",
            "evidence": "TVC1219_1/TVC1219_2 and PTOL1220_3 give exact conditional type rule",
            "result": "EXACT_IF_TYPED_GRAMMAR_SIGNED",
            "missing": "typed grammar is not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "PEX1417_3_common_source_current",
            "theorem_clause": "active source is total Hilbert/coframe current",
            "test": "T_total = delta S_matter/delta e_obs before material/readout/source-worldtube projection",
            "evidence": "OWN1076_2_current_owner and 1415/1416 source-current ledgers",
            "result": "CURRENT_OWNER_MISSING",
            "missing": "single current/source normalization owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "PEX1417_4_action_measure_normalization",
            "theorem_clause": "species action multipliers are quotient/gauge artifacts or impossible",
            "test": "w_A S_A cannot alter Hilbert source, path-integral weight, or source normalization",
            "evidence": "FMQ1066_4 and FNL1065_4 say this obstruction remains live",
            "result": "NOT_PARENT_SIGNED",
            "missing": "single parent action-scale/measure/hbar owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "PEX1417_5_readout_transfer",
            "theorem_clause": "typed exclusion survives EFT/readout",
            "test": "S_eff, spectroscopy, clocks, WEP, R10, PPN, and local projections cannot regenerate source-only slots",
            "evidence": "CERT1236_4 and PTOL1220_5",
            "result": "UNSIGNED",
            "missing": "radiative/readout closure theorem or finite transfer priors",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "PEX1417_6_counterexample_test",
            "theorem_clause": "all live source-slot countermodels are syntactically illegal",
            "test": "w_A(X), kappa_A(X), J_A -> c_A J_A, hidden marker source selector are all ill-typed",
            "evidence": "1416 countermodel ledger keeps them live",
            "result": "FAILED",
            "missing": "constructor exhaustion does not yet kill the countermodels",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "PEX1417_7_verdict",
            "theorem_clause": "parent object-language constructor exhaustion",
            "test": "combine primitive sort exhaustion, no species-source morphism, current owner, action measure owner, and readout closure",
            "evidence": "PCL1417_7_verdict",
            "result": "NOT_PROVED_CURRENT_CORPUS",
            "missing": "demote to qbar_source_weight acquisition rows until parent syntax is signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM1417_0_species_weight_action",
            "constructor": "SpeciesLabel -> w_A(X) -> S_matter=sum_A w_A S_A",
            "why_it_survives": "locality, covariance, and additivity do not forbid a scalar multiplier",
            "damage": "rescales Hilbert source and qbar_source_weight",
            "killed_by": "parent action-scale owner plus no SpeciesLabel source coefficient constructor",
            "status": "LIVE_UNTIL_PARENT_GRAMMAR_SIGNED",
            "maps_to_row": "QSA1417_0_qbar_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1417_1_kappaA_source_map",
            "constructor": "SpeciesLabel -> kappa_A(X) -> active source selection",
            "why_it_survives": "can be inserted after material labelling unless variation-before-readout/source functor is signed",
            "damage": "source-dependent Newton/WEP/R10 response",
            "killed_by": "total Hilbert source current owner before readout",
            "status": "LIVE_UNTIL_CURRENT_OWNER_SIGNED",
            "maps_to_row": "QSA1417_0_qbar_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1417_2_current_rescaling",
            "constructor": "J_A -> c_A(X) J_A",
            "why_it_survives": "Noether/current normalization is not yet globally owned",
            "damage": "source/test current normalization residual",
            "killed_by": "single T_Q/current owner with fixed charge/current normalization",
            "status": "LIVE_UNTIL_CURRENT_OWNER_SIGNED",
            "maps_to_row": "QSA1417_1_current_rescaling_link",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1417_3_hidden_marker_source_selector",
            "constructor": "hidden marker or branch label retyped as source coefficient argument",
            "why_it_survives": "no-extension/no-marker theorem is not parent-derived",
            "damage": "lets qbar_source_weight depend on a hidden/local scalar despite typed visible grammar",
            "killed_by": "no-extension theorem plus readout closure",
            "status": "LIVE_UNTIL_NO_EXTENSION_SIGNED",
            "maps_to_row": "QSA1417_2_hidden_marker_guard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def qbar_acquisition_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "QSA1417_0_qbar_source_weight",
            "quantity": "qbar_source_weight",
            "definition": "dimensionless active-source species/source prefactor sensitivity",
            "formula_or_source_need": "qbar_source_weight := partial_X ln kappa_A or Delta kappa_A/kappa_univ in the parent coupling basis",
            "theorem_zero_condition": "PCL1417_7 constructor exhaustion parent-signed and PEX1417_7 result becomes PROVED",
            "finite_input_required": "value or bound for kappa_A/source-only weight, source species map, sign convention, X_I parent basis",
            "current_value": "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT",
            "units": "dimensionless",
            "observable_links": "WEP_source_charge;Newton_GM;R10;R11;PPN;local_GR",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1416_FIRST_RSOURCE_COEFFICIENT_ROW.csv",
            "source_anchor": "RSC1416_0_qbar_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "QSA1417_1_current_rescaling_link",
            "quantity": "current_rescaling_residual",
            "definition": "source/test current normalization component coupled to qbar_source_weight",
            "formula_or_source_need": "delta_source_current := partial_X ln c_A or finite beta_source,A in same parent basis as qbar_source_weight",
            "theorem_zero_condition": "single Noether/current owner and variation-before-readout parent-signed",
            "finite_input_required": "c_A/beta_source,A value or bound, current normalization units, source path, sign convention",
            "current_value": "MISSING_CURRENT_OWNER_OR_COEFFICIENT",
            "units": "dimensionless or declared parent current-normalization units",
            "observable_links": "WEP_source_charge;R10_source_side;Newton_GM;local_GR",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1416_FIRST_RSOURCE_COEFFICIENT_ROW.csv",
            "source_anchor": "RSC1416_1_current_rescaling",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "QSA1417_2_hidden_marker_guard",
            "quantity": "source-slot hidden/marker return",
            "definition": "guard against hidden scalar, branch label, domain selector, or readout marker being retyped as source coefficient data",
            "formula_or_source_need": "prove no-extension/no-marker theorem or retain finite source-marker coupling row",
            "theorem_zero_condition": "CERT1236_3 and readout closure parent-signed",
            "finite_input_required": "marker/source coupling coefficient, allowed domain, readout transfer, source path",
            "current_value": "MISSING_NO_EXTENSION_OR_MARKER_SOURCE_COEFFICIENT",
            "units": "dimensionless",
            "observable_links": "WEP;R10;clock;PPN;local_GR",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
            "source_anchor": "CERT1236_3_no_extension_marker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "QSA1417_3_parent_basis",
            "quantity": "qbar_source_weight parent basis",
            "definition": "basis X_I and normalization in which source-weight coefficients are measured or zeroed",
            "formula_or_source_need": "declare parent coupling coordinates, units, sign convention, and projection maps before arenas",
            "theorem_zero_condition": "typed parent object language and current owner supply a unique basis with no source coefficient slot",
            "finite_input_required": "basis name, coordinate units, sign convention, source path, map to qbar_XT/R_source",
            "current_value": "MISSING_PARENT_COUPLING_BASIS",
            "units": "not_declared",
            "observable_links": "all R_source/qbar arenas",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1076_COUPLING_OWNER_GATES.csv",
            "source_anchor": "OWN1076_0_parent_object_language",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "QSA1417_4_verdict",
            "quantity": "qbar_source_weight acquisition pack",
            "definition": "constructor exhaustion failed, so qbar_source_weight remains finite nonclaim source acquisition debt",
            "formula_or_source_need": "score-ready only if QSA1417_0 through QSA1417_3 are theorem-zero or source-backed with units/sign/projections",
            "theorem_zero_condition": "PEX1417_7 becomes PROVED and readout transfer is signed",
            "finite_input_required": "values/bounds, units, parent basis, arena tau/projection factors, source paths, no-cancellation envelope",
            "current_value": "TEMPLATE_ONLY_NONCLAIM",
            "units": "not_applicable",
            "observable_links": "WEP;Newton_GM;R10;R11;PPN;local_GR",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1417_CONSTRUCTOR_EXHAUSTION_PROOF_AUDIT.csv",
            "source_anchor": "PEX1417_7_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def arena_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "ARG1417_0_WEP",
            "arena": "WEP_source_charge",
            "needed_projection": "eta_AB source/test map using qbar_source_weight, current_rescaling, material tensor, source worldtube, orbit/readout tau",
            "current_status": "BLOCKED_MISSING_QBAR_SOURCE_VALUE_AND_TAU_WEP",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ARG1417_1_Newton_GM",
            "arena": "Newton_GM",
            "needed_projection": "separate common measured G calibration from relative source weights",
            "current_status": "BLOCKED_NO_ABSORPTION_INTO_MEASURED_G",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ARG1417_2_R10_R11",
            "arena": "R10/R11 short-range/local source side",
            "needed_projection": "map qbar_source_weight into alpha(lambda) or local residual with real bound/source curves",
            "current_status": "BLOCKED_MISSING_ARENA_PROJECTION_AND_COEFFICIENT",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ARG1417_3_PPN_local_GR",
            "arena": "PPN/local_GR",
            "needed_projection": "show source-slot residual vanishes or is bounded below PPN/local limits after GR reduction",
            "current_status": "BLOCKED_CONSTRUCTOR_EXHAUSTION_NOT_PROVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ARG1417_4_no_cancellation",
            "arena": "cross-arena score policy",
            "needed_projection": "absolute/no-cancellation envelope for qbar_source_weight + qbar_marker + qbar_constants + current_rescaling",
            "current_status": "BLOCKED_COMPONENT_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ARG1417_5_verdict",
            "arena": "all local/source arenas",
            "needed_projection": "claim opens only when theorem-zero or source-backed rows and arena projections are real",
            "current_status": "ALL_CLAIMS_BLOCKED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1417_0_constructor_verdict",
            "decision": "do not promote constructor exhaustion",
            "reason": "primitive completeness, action-scale/measure owner, current owner, and readout transfer remain unsigned",
            "next_action": "keep Hom(SpeciesLabel,Coeff_active_source)=empty as target theorem or explicit closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1417_1_qbar_branch",
            "decision": "qbar_source_weight remains finite nonclaim row",
            "reason": "source-only active-source coefficients are not syntactically illegal yet",
            "next_action": "source theorem-zero certificate or source-backed qbar_source_weight coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1417_2_best_next",
            "decision": "target action-scale/current owner lock next",
            "reason": "constructor grammar alone stalls because w_A S_A can be classical-normalization-like but source/quantum-active",
            "next_action": "try to prove one parent action-scale/current-owner lock, else build qbar_source_weight coefficient acquisition ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1417_0_constructor_exhaustion",
            "claim": "Hom(SpeciesLabel,Coeff_active_source)=empty is derived from MTS primitives",
            "allowed": False,
            "reason": "PCL1417_7 and PEX1417_7 are not proved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1417_1_qbar_zero",
            "claim": "qbar_source_weight=0 by theorem",
            "allowed": False,
            "reason": "constructor exhaustion/current owner/action-scale owner unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1417_2_qbar_numeric",
            "claim": "qbar_source_weight is numerically bounded",
            "allowed": False,
            "reason": "no sourced coefficient value, units, sign, parent basis, or arena projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1417_3_local_claims",
            "claim": "WEP/Newton/R10/PPN/local-GR pass",
            "allowed": False,
            "reason": CLAIM_CEILING,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1417_0_1418",
            "target_doc": "1418-Y5-R10-RAB-action-scale-current-owner-lock-or-qbar-source-weight-acquisition-ledger.md",
            "target_script": "scripts/Y5_R10_RAB_action_scale_current_owner_lock_or_qbar_source_weight_acquisition_ledger.py",
            "task": "try to prove a single parent action-scale/current-owner lock that makes w_A S_A and J_A -> c_A J_A quotient/gauge-impossible; if it fails, build source-ready qbar_source_weight acquisition rows by arena",
            "success_condition": "either source-only weights are theorem-zero by a signed action/current owner, or qbar_source_weight has explicit source acquisition requirements for WEP/Newton/R10/PPN/local_GR",
            "do_not_claim": "WEP pass; R_source pass; R10 pass; local-GR pass; qbar_source_weight=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "next_id": "NEXT1417_1_parallel_data",
            "target_doc": "future-qbar-source-weight-bound-input-source-hunt.md",
            "target_script": "future_source_row_route",
            "task": "if derivation route keeps failing, identify literature/data constraints that can bound relative source-weight or source-charge coefficients without importing unity shortcuts",
            "success_condition": "source path, value/bound, uncertainty, units, sign convention, material/source map, and arena projection are all present",
            "do_not_claim": "placeholder numeric row as evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    constructors: list[dict[str, Any]],
    proof_audit: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    qbar_rows: list[dict[str, Any]],
    arena_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        CONSTRUCTOR_LIST_PATH,
        PROOF_AUDIT_PATH,
        COUNTERMODEL_PATH,
        QBAR_ACQUISITION_PATH,
        ARENA_GATE_PATH,
        DECISION_PATH,
        CLAIM_GATE_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
                "generated_utc": GENERATED_UTC,
            }
        )

    add(
        "VAL1417_0_sources",
        all(row["path_exists"] and row["anchor_found"] for row in sources),
        "all cited local source paths exist and anchors are present",
    )
    add(
        "VAL1417_1_constructor_list",
        any(row["constructor_id"] == "PCL1417_7_verdict" and row["current_status"] == "CONSTRUCTOR_EXHAUSTION_NOT_PROVED" for row in constructors),
        "primitive constructor list is explicit and verdict remains not proved",
    )
    add(
        "VAL1417_2_proof_audit",
        any(row["proof_id"] == "PEX1417_7_verdict" and row["result"] == "NOT_PROVED_CURRENT_CORPUS" for row in proof_audit),
        "constructor exhaustion proof attempt fails honestly",
    )
    add(
        "VAL1417_3_countermodels",
        {"CM1417_0_species_weight_action", "CM1417_1_kappaA_source_map", "CM1417_2_current_rescaling"}.issubset({row["countermodel_id"] for row in countermodels}),
        "live constructor countermodels include species weight, kappa source map, and current rescaling",
    )
    add(
        "VAL1417_4_qbar_rows",
        any(row["row_id"] == "QSA1417_0_qbar_source_weight" and row["current_value"].startswith("MISSING_") for row in qbar_rows)
        and all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in qbar_rows),
        "qbar_source_weight acquisition rows exist and remain nonclaim",
    )
    add(
        "VAL1417_5_arena_gates",
        any(row["gate_id"] == "ARG1417_5_verdict" and row["current_status"] == "ALL_CLAIMS_BLOCKED" for row in arena_gates),
        "all arena gates remain blocked",
    )
    add(
        "VAL1417_6_claim_refusal",
        all(row["allowed"] is False and row["claim_allowed"] is False for row in claim_gates),
        "constructor, qbar zero, numeric bound, and local claims are refused",
    )
    add(
        "VAL1417_7_decision",
        any(row["decision_id"] == "DEC1417_2_best_next" and "action-scale/current owner" in row["decision"] for row in decisions),
        "decision ledger selects action-scale/current owner lock next",
    )
    add(
        "VAL1417_8_next_target",
        any(row["next_id"] == "NEXT1417_0_1418" for row in next_targets),
        "next target 1418 is staged",
    )
    add(
        "VAL1417_9_scope",
        all((ROOT / path).resolve().is_relative_to(ROOT.resolve()) for path in output_paths),
        "outputs are confined to post-checkpoint-work paths",
    )
    add(
        "VAL1417_10_overall",
        True,
        "1417 fails constructor exhaustion and writes qbar_source_weight acquisition rows as nonclaim",
    )
    if any(row["status"] == "FAIL" for row in rows):
        for row in rows:
            if row["check_id"] == "VAL1417_10_overall":
                row["status"] = "FAIL"
                row["detail"] = "one or more 1417 validation checks failed"
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    constructors: list[dict[str, Any]],
    proof_audit: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    qbar_rows: list[dict[str, Any]],
    arena_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = f"""# 1417 - Parent Object-Language Constructor Exhaustion Or qbar_source_weight Acquisition

**Current verdict:** the clean constructor-exhaustion theorem is not proved. The desired theorem is exactly `Hom(SpeciesLabel,Coeff_active_source)=empty`, but the current corpus still lacks a parent-derived primitive constructor list, a single action-scale/measure owner, a single source-current owner, and readout/EFT transfer closure.

**Discipline move:** no WEP, Newton-GM, R10, PPN, or local-GR claim is made. `qbar_source_weight` remains a finite nonclaim acquisition row unless the parent action/current owner makes the source-only constructor syntactically impossible.

**Status:** `{STATUS}`

## Source Register

{md_table(sources)}

## Primitive Constructor List Attempt

{md_table(constructors)}

## Constructor Exhaustion Proof Audit

{md_table(proof_audit)}

## Live Constructor Countermodels

{md_table(countermodels)}

## qbar_source_weight Acquisition Rows

{md_table(qbar_rows)}

## Arena Projection Gate

{md_table(arena_gates)}

## Decision Ledger

{md_table(decisions)}

## Claim Gate

{md_table(claim_gates)}

## Next Target

{md_table(next_targets)}

## Validation

{md_table(validations)}
"""
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    constructors = constructor_list_rows()
    proof_audit = proof_audit_rows()
    countermodels = countermodel_rows()
    qbar_rows = qbar_acquisition_rows()
    arena_gates = arena_gate_rows()
    decisions = decision_rows()
    claim_gates = claim_gate_rows()
    next_targets = next_target_rows()
    validations = validation_rows(
        sources,
        constructors,
        proof_audit,
        countermodels,
        qbar_rows,
        arena_gates,
        decisions,
        claim_gates,
        next_targets,
    )

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(CONSTRUCTOR_LIST_PATH, constructors)
    write_csv(PROOF_AUDIT_PATH, proof_audit)
    write_csv(COUNTERMODEL_PATH, countermodels)
    write_csv(QBAR_ACQUISITION_PATH, qbar_rows)
    write_csv(ARENA_GATE_PATH, arena_gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATE_PATH, claim_gates)
    write_csv(NEXT_TARGET_PATH, next_targets)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, constructors, proof_audit, countermodels, qbar_rows, arena_gates, decisions, claim_gates, next_targets, validations)

    if any(row["status"] != "PASS" for row in validations):
        raise SystemExit("1417 validation failed")

    print(STATUS)


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1389-Y5-R10-RAB-Delta-w-material-source-map-or-action-measure-owner-proof.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1389_SOURCE_REGISTER.csv"
OWNER_PROOF_PATH = SRC_DIR / "P8_Y5_R10_1389_ACTION_MEASURE_OWNER_PROOF_ATTEMPT.csv"
MATERIAL_MAP_PATH = SRC_DIR / "P8_Y5_R10_1389_MATERIAL_SOURCE_CLASS_MAP.csv"
COUPLING_CONVENTION_PATH = SRC_DIR / "P8_Y5_R10_1389_COUPLING_EXPANSION_CONVENTION.csv"
ARENA_REQUIREMENTS_PATH = SRC_DIR / "P8_Y5_R10_1389_ARENA_REQUIREMENT_MATRIX.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1389_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1389_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1389_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1389_VALIDATION.csv"

STATUS = (
    "action_measure_owner_conditional_theorem_written_"
    "Delta_w_material_source_map_ready_nonclaim"
)
CLAIM_CEILING = (
    "conditional_owner_theorem_and_material_source_map_only_no_parent_signed_Delta_w_zero_"
    "no_numeric_beta_no_R10_no_WEP_no_PPN_no_Newton_no_clock_no_orbital_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1389_0_1388_doc",
        "source_path": "1388-Y5-R10-RAB-Delta-w-source-beta-validator-or-action-measure-owner-return.md",
        "required_anchor": "NEXT1388_0_1389",
        "purpose": "handoff to material/source map or action-measure owner proof",
    },
    {
        "source_id": "SRC1389_1_1388_next",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1388_NEXT_TARGET.csv",
        "required_anchor": "NEXT1388_0_1389",
        "purpose": "machine-readable 1389 target",
    },
    {
        "source_id": "SRC1389_2_1388_validator",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1388_DELTA_W_SOURCE_BETA_VALIDATOR.csv",
        "required_anchor": "DWV1388_7_verdict",
        "purpose": "strict validator refuses scoring without sourced coupling inputs",
    },
    {
        "source_id": "SRC1389_3_1388_owner_gate",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1388_ACTION_MEASURE_OWNER_RETURN_GATE.csv",
        "required_anchor": "AMR1388_4_return_verdict",
        "purpose": "parent owner-return theorem remains unsigned",
    },
    {
        "source_id": "SRC1389_4_1388_refusal",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1388_SCORING_REFUSAL_MATRIX.csv",
        "required_anchor": "SFM1388_5_local_GR",
        "purpose": "local-GR scoring remains blocked",
    },
    {
        "source_id": "SRC1389_5_1387_first_fill",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1387_DELTA_W_SOURCE_BETA_FIRST_FILL.csv",
        "required_anchor": "DWB1387_6_first_fill_verdict",
        "purpose": "first-fill rows being refined into class map",
    },
    {
        "source_id": "SRC1389_6_1078_action_measure",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv",
        "required_anchor": "AM1078_4_verdict",
        "purpose": "prior action-measure proof attempt",
    },
    {
        "source_id": "SRC1389_7_1078_object_language",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv",
        "required_anchor": "OL1078_4_verdict",
        "purpose": "prior object-language proof attempt",
    },
    {
        "source_id": "SRC1389_8_1079_current_owner",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
        "required_anchor": "NCO1079_5_species_action_weight",
        "purpose": "current owner cannot kill pre-variation action weights",
    },
    {
        "source_id": "SRC1389_9_1229_single_GN",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv",
        "required_anchor": "CLC1229_7_single_GN_normalization",
        "purpose": "measured-G absorption guard",
    },
    {
        "source_id": "SRC1389_10_1036_beta_product",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv",
        "required_anchor": "BETA1036_2_R10_alpha_match",
        "purpose": "finite source-test beta product law",
    },
    {
        "source_id": "SRC1389_11_this_script",
        "source_path": "scripts/Y5_R10_RAB_Delta_w_material_source_map_or_action_measure_owner_proof.py",
        "required_anchor": "STATUS",
        "purpose": "1389 generator",
    },
]


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        columns = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: clean(row.get(column, "")) for column in columns})


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(clean(row.get(column, "")).replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def anchor_found(path: Path, anchor: str) -> bool:
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCE_ROWS:
        source_path = ROOT / source["source_path"]
        exists = source_path.exists()
        found = anchor_found(source_path, source["required_anchor"])
        rows.append(
            {
                **source,
                "exists": str(exists),
                "anchor_found": str(found),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def owner_proof_rows() -> list[dict[str, str]]:
    return [
        {
            "proof_id": "AMP1389_0_counterexample_target",
            "clause": "target the surviving pre-variation action weight counterexample",
            "attempted_derivation": "treat S_matter=sum_A w_A S_A as admissible unless parent syntax, measure, or category ownership forbids it",
            "result": "COUNTEREXAMPLE_TARGET_EXPLICIT",
            "gap": "none for target definition",
            "consequence": "the proof must kill w_A before Hilbert variation, not after",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "AMP1389_1_single_parent_action_measure",
            "clause": "single parent action scale and measure",
            "attempted_derivation": "if the parent action has one measure owner and no sector-label scalar slots, relative w_A has no admissible object-language location",
            "result": "CONDITIONAL_THEOREM_CLAUSE",
            "gap": "the current corpus has not parent-signed the single action-measure owner strongly enough",
            "consequence": "relative weights are killed only under the unsigned owner premise",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "AMP1389_2_connected_matter_naturality",
            "clause": "connected ordinary-matter category",
            "attempted_derivation": "a natural positive scalar over one connected ordinary-matter category is common, so w_A=w_*",
            "result": "CONDITIONAL_WITH_DIRECT_SUM_COUNTERMODEL",
            "gap": "a disconnected direct-sum matter category can still carry independent constants unless the parent functor forbids them",
            "consequence": "connectedness can reduce w_A to w_*, but connectedness is not derived",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "AMP1389_3_quantum_measure_not_gauge",
            "clause": "relative action weights are not harmless gauge factors",
            "attempted_derivation": "constant w_A leaves isolated classical Euler-Lagrange form unchanged but changes Hilbert source normalization and relative quantum/statistical action weights",
            "result": "DEMOTION_TO_GAUGE_REJECTED",
            "gap": "must either forbid w_A or measure it/bound it",
            "consequence": "finite Delta_w rows are physically meaningful if the parent owner theorem fails",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "AMP1389_4_current_owner_limited",
            "clause": "current/Hilbert owner",
            "attempted_derivation": "vary first, read source later; test whether this erases a w_A already inside S_matter",
            "result": "CURRENT_OWNER_PARTIAL_NOT_ENOUGH",
            "gap": "Hilbert stress inherits pre-variation w_A",
            "consequence": "current owner must be combined with object-language/action-measure owner",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "AMP1389_5_common_calibration",
            "clause": "common derivative-silent factor",
            "attempted_derivation": "if w_A=w_* for all ordinary matter and partial_t,r,A,lambda,frame ln w_*=0, absorb w_* into measured G_N",
            "result": "CALIBRATION_LEMMA_CONDITIONAL",
            "gap": "universality and derivative silence are not yet signed",
            "consequence": "common w_* is harmless only after a silence proof",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "AMP1389_6_theorem_if_signed",
            "clause": "conditional Delta_w/beta zero theorem",
            "attempted_derivation": "object-language owner + action-measure owner + connected matter functor + current owner + derivative silence imply Delta_w_A=0 and beta_w,A=0 for ordinary matter",
            "result": "EXACT_CONDITIONAL_THEOREM_READY",
            "gap": "the parent signatures are not all present in the current corpus",
            "consequence": "clean local-GR source coupling is available only as a conditional theorem",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "AMP1389_7_current_verdict",
            "clause": "current parent proof status",
            "attempted_derivation": "compare required theorem clauses to 1078, 1079, 1229, 1387, and 1388 evidence",
            "result": "ACTION_MEASURE_OWNER_NOT_PARENT_SIGNED",
            "gap": "object-language owner, action-measure owner, connectedness, and derivative silence do not close together",
            "consequence": "continue with nonclaim material/source map and no local scoring",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def material_map_rows() -> list[dict[str, str]]:
    return [
        {
            "class_id": "MSC1389_0_bulk_neutral_baryonic",
            "material_source_class": "bulk neutral baryonic matter",
            "source_role": "macroscopic source/test mass for laboratory and solar-system arenas",
            "delta_symbol": "Delta_w_bulk",
            "beta_symbol": "beta_w,bulk",
            "observable_legs": "Newton;WEP;R10;PPN;orbital",
            "required_provenance": "parent theorem-zero, composition model, or sourced bound for neutral bulk matter",
            "units": "dimensionless Delta_w; beta in canonical inverse-field or locked dimensionless convention",
            "current_status": "MAP_READY_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "class_id": "MSC1389_1_electronic_atomic",
            "material_source_class": "electronic/atomic mass and clock standards",
            "source_role": "test material and clock readout standard",
            "delta_symbol": "Delta_w_e",
            "beta_symbol": "beta_w,e",
            "observable_legs": "WEP;clocks/constants;R10 test leg",
            "required_provenance": "atomic/electronic sector action owner or material beta bound",
            "units": "dimensionless Delta_w; beta convention locked to canonical phi",
            "current_status": "MAP_READY_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "class_id": "MSC1389_2_nuclear_binding",
            "material_source_class": "nuclear binding/composite rest mass",
            "source_role": "composition-dependent part of macroscopic masses",
            "delta_symbol": "Delta_w_nuc",
            "beta_symbol": "beta_w,nuc",
            "observable_legs": "WEP;clocks/constants;orbital composition",
            "required_provenance": "nuclear binding source map or theorem that binding inherits the common matter owner",
            "units": "dimensionless Delta_w; beta convention locked to canonical phi",
            "current_status": "MAP_READY_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "class_id": "MSC1389_3_EM_binding_sector",
            "material_source_class": "electromagnetic binding/charge sector",
            "source_role": "material binding, charge-response, and possible EM bridge",
            "delta_symbol": "Delta_w_EM",
            "beta_symbol": "beta_w,EM",
            "observable_legs": "WEP;clocks/constants;EM/fine-structure;R10 material leg",
            "required_provenance": "EM sector action descent or finite alpha/clock coupling bound",
            "units": "dimensionless Delta_w; beta convention locked to canonical phi",
            "current_status": "MAP_READY_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "class_id": "MSC1389_4_self_gravitating_orbital",
            "material_source_class": "self-gravitating orbital bodies",
            "source_role": "planetary/solar source mass and self-energy response",
            "delta_symbol": "Delta_w_orb",
            "beta_symbol": "beta_w,orb",
            "observable_legs": "orbital;PPN;Newton;local GR",
            "required_provenance": "source-body worldtube map, self-energy treatment, and measured-G calibration rule",
            "units": "dimensionless Delta_w; beta convention locked to canonical phi",
            "current_status": "MAP_READY_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "class_id": "MSC1389_5_R10_lab_pair",
            "material_source_class": "short-range laboratory source/test pair",
            "source_role": "R10 source and test legs in alpha(lambda)",
            "delta_symbol": "Delta_w_R10,S;Delta_w_R10,T",
            "beta_symbol": "beta_w,R10,S;beta_w,R10,T",
            "observable_legs": "R10",
            "required_provenance": "actual material composition, canonical beta convention, K(lambda), tail envelope, and real bound curve",
            "units": "dimensionless alpha after product kernel",
            "current_status": "MAP_READY_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "class_id": "MSC1389_6_map_verdict",
            "material_source_class": "material/source map verdict",
            "source_role": "nonclaim coefficient routing",
            "delta_symbol": "Delta_w_A",
            "beta_symbol": "beta_w,A",
            "observable_legs": "Newton;WEP;R10;PPN;clocks;orbital;local GR",
            "required_provenance": "every class above must be theorem-zero or source-backed before scoring",
            "units": "per-row units above",
            "current_status": "MATERIAL_MAP_READY_VALUES_MISSING_NONCLAIM",
            "valid_for_claim": "False",
        },
    ]


def coupling_convention_rows() -> list[dict[str, str]]:
    return [
        {
            "convention_id": "CEC1389_0_field_normalization",
            "statement": "all beta rows must use one canonical scalar convention phi_c",
            "formula": "phi_c chosen so beta_w,A := partial_phi_c ln w_A(phi_c)",
            "required_inputs": "canonical phi normalization; parent kinetic coefficient; field-redefinition invariant range",
            "status": "CONVENTION_REQUIRED_INPUTS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "convention_id": "CEC1389_1_weight_expansion",
            "statement": "expand each material/source action weight around the local background",
            "formula": "w_A(phi_c)=w_*[1+Delta_w_A+beta_w,A phi_c + 1/2 kappa_w,A phi_c^2 + ...]",
            "required_inputs": "w_* calibration rule; Delta_w_A; beta_w,A; expansion point; material/source class A",
            "status": "EXPANSION_READY_VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "convention_id": "CEC1389_2_constant_vs_derivative",
            "statement": "constant relative weights and derivative couplings are different physics",
            "formula": "Delta_w_A affects source normalization/composition; beta_w,A sources finite exchange",
            "required_inputs": "separate Delta_w and beta rows, no measured-G absorption unless common and silent",
            "status": "GUARD_READY_NONCLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "convention_id": "CEC1389_3_product_law",
            "statement": "finite exchange uses source-test product",
            "formula": "alpha_ST(lambda)=K_ST(lambda) beta_w,S beta_w,T + epsilon_tail(lambda)",
            "required_inputs": "beta source leg; beta test leg; K_ST(lambda); epsilon tail; range/mass-gap law",
            "status": "PRODUCT_LAW_READY_VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "convention_id": "CEC1389_4_observed_mass_charge",
            "statement": "material charge is the log derivative of the observed source/readout quantity",
            "formula": "Q_A^w = partial_phi_c ln M_A^obs = beta_w,A + inherited mass/binding terms",
            "required_inputs": "M_A decomposition, binding fractions, inherited sector beta rows, readout convention",
            "status": "OBSERVED_CHARGE_READY_DECOMPOSITION_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "convention_id": "CEC1389_5_verdict",
            "statement": "coupling convention is structured but not numeric",
            "formula": "score only after CEC1389_0 through CEC1389_4 are source-backed",
            "required_inputs": "canonical convention, class map, beta legs, kernels, and bounds",
            "status": "CONVENTION_SCAFFOLD_READY_NO_SCORE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def arena_requirement_rows() -> list[dict[str, str]]:
    return [
        {
            "arena_id": "ARM1389_0_Newton",
            "arena": "Newton/source normalization",
            "required_material_inputs": "Delta_w_bulk or theorem-zero; common w_* silence; measured-G calibration rule",
            "required_kernel": "source mass normalization kernel",
            "current_status": "BLOCKED_INPUTS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "ARM1389_1_WEP",
            "arena": "WEP/source charge",
            "required_material_inputs": "Delta_w_e, Delta_w_nuc, Delta_w_EM, beta_w class matrix",
            "required_kernel": "composition/material contrast kernel",
            "current_status": "BLOCKED_INPUTS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "ARM1389_2_R10",
            "arena": "R10 alpha(lambda)",
            "required_material_inputs": "beta_w,R10,S; beta_w,R10,T; R10 material pair; mu_m^2",
            "required_kernel": "K_ST(lambda), epsilon_tail(lambda), real bound curve",
            "current_status": "BLOCKED_INPUTS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "ARM1389_3_PPN",
            "arena": "PPN/local residual vector",
            "required_material_inputs": "bulk source beta, self-energy/orbital source row, measured-G residual",
            "required_kernel": "weak-field residual vector through second order",
            "current_status": "BLOCKED_INPUTS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "ARM1389_4_clocks",
            "arena": "clocks/constants",
            "required_material_inputs": "electronic, nuclear, and EM binding beta rows",
            "required_kernel": "clock transition/readout kernel",
            "current_status": "BLOCKED_INPUTS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "ARM1389_5_orbital",
            "arena": "orbital systems",
            "required_material_inputs": "orbital source class, self-energy treatment, bulk matter beta",
            "required_kernel": "worldtube/orbital residual kernel",
            "current_status": "BLOCKED_INPUTS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "ARM1389_6_local_GR",
            "arena": "local GR reduction",
            "required_material_inputs": "action-weight theorem-zero or complete finite class residual pack",
            "required_kernel": "Newton+WEP+R10+PPN+clock+orbital closure gates",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE1389_0_sources",
            "gate": "all cited local sources exist and anchors are present",
            "status": "PASS",
            "reason": "source register validates against local corpus",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1389_1_owner_proof",
            "gate": "action-measure owner theorem closes",
            "status": "BLOCKED_PARENT_UNSIGNED",
            "reason": "proof is exact conditional but owner clauses are not parent-signed together",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1389_2_material_map",
            "gate": "material/source class map exists",
            "status": "PASS_NONCLAIM_MAP",
            "reason": "classes are now explicit but every coefficient remains missing/nonclaim",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1389_3_coupling_convention",
            "gate": "Delta_w/beta expansion convention is defined",
            "status": "PASS_SCHEMA_ONLY",
            "reason": "constant Delta_w, derivative beta, product alpha, and observed-charge rules are separated",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1389_4_arena_scores",
            "gate": "Newton/WEP/R10/PPN/clock/orbital scores may be reported",
            "status": "BLOCKED_INPUTS_MISSING",
            "reason": "class coefficients and arena kernels are not source-backed",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1389_5_local_claim",
            "gate": "local GR reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1389 is a conditional proof plus nonclaim map, not a derived GR limit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1389_0_theorem_status",
            "decision": "keep the zero route as an exact conditional theorem",
            "because": "if the parent object-language/action-measure owner clauses close, Delta_w_A and beta_w,A can be theorem-zero",
            "next_action": "try a narrower common-calibration derivative-silence lemma",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1389_1_material_map",
            "decision": "promote Delta_w_A from abstract symbol to material/source class rows",
            "because": "finite coupling tests need source/test legs, clock standards, EM/nuclear binding, and orbital source rows",
            "next_action": "fill or bound the easiest class rows only after provenance and kernels exist",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1389_2_no_numeric_runner",
            "decision": "do not run numeric local scoring from this checkpoint",
            "because": "the map has no sourced coefficients, no canonical beta values, and no arena kernels",
            "next_action": "use 1390 to attempt the common calibration silence proof or create first nonclaim bulk-source bound row",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1389_0_1390",
            "next_doc": "1390-Y5-R10-RAB-common-calibration-silence-or-first-material-coefficient-bound.md",
            "next_script": "scripts/Y5_R10_RAB_common_calibration_silence_or_first_material_coefficient_bound.py",
            "task": "try to prove that a common w_* is derivative/source/range/frame silent; if not, create the first nonclaim bulk material coefficient bound row with required kernels and provenance fields",
            "success_condition": "either common calibration is narrowed to a signed lemma candidate, or the bulk neutral matter coefficient row is ready for future sourcing without enabling local scoring",
            "do_not_claim": "local GR;Newton limit;PPN pass;R10 pass;WEP pass;q_loc=0;numeric alpha(lambda);GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def csv_rows(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validation_rows(
    sources: list[dict[str, str]],
    proof: list[dict[str, str]],
    material_map: list[dict[str, str]],
    convention: list[dict[str, str]],
    arenas: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_pass = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    proof_verdict = any(
        row["proof_id"] == "AMP1389_7_current_verdict"
        and row["result"] == "ACTION_MEASURE_OWNER_NOT_PARENT_SIGNED"
        and row["claim_allowed"] == "False"
        for row in proof
    )
    conditional_theorem = any(
        row["proof_id"] == "AMP1389_6_theorem_if_signed"
        and row["result"] == "EXACT_CONDITIONAL_THEOREM_READY"
        and row["valid_for_claim"] == "False"
        for row in proof
    )
    map_ready = any(
        row["class_id"] == "MSC1389_6_map_verdict"
        and row["current_status"] == "MATERIAL_MAP_READY_VALUES_MISSING_NONCLAIM"
        and row["valid_for_claim"] == "False"
        for row in material_map
    )
    class_count_ok = len([row for row in material_map if row["class_id"].startswith("MSC1389_")]) >= 7
    convention_ready = any(
        row["convention_id"] == "CEC1389_5_verdict"
        and row["status"] == "CONVENTION_SCAFFOLD_READY_NO_SCORE"
        and row["claim_allowed"] == "False"
        for row in convention
    )
    arenas_blocked = all(
        row["current_status"].startswith("BLOCKED")
        and row["claim_allowed"] == "False"
        and row["valid_for_claim"] == "False"
        for row in arenas
    )
    local_claim_blocked = any(
        row["gate_id"] == "GATE1389_5_local_claim"
        and row["status"] == "BLOCKED_NO_CLAIM"
        and row["claim_allowed"] == "False"
        for row in gates
    )
    prior_gate = csv_rows(Path("source-intake/mts_residuals/P8_Y5_R10_1388_CLAIM_GATE.csv"))
    prior_local_blocked = any(
        row["gate_id"] == "GATE1388_5_local_claim" and row["status"] == "BLOCKED_NO_CLAIM"
        for row in prior_gate
    )
    outputs = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        OWNER_PROOF_PATH,
        MATERIAL_MAP_PATH,
        COUPLING_CONVENTION_PATH,
        ARENA_REQUIREMENTS_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
        Path("scripts/Y5_R10_RAB_Delta_w_material_source_map_or_action_measure_owner_proof.py"),
    ]
    formalization_touched = any("formalization-workbench" in str((ROOT / output).resolve()) for output in outputs)
    scope_ok = all((ROOT / output).resolve().is_relative_to(ROOT.resolve()) for output in outputs) and not formalization_touched
    overall = (
        source_pass
        and proof_verdict
        and conditional_theorem
        and map_ready
        and class_count_ok
        and convention_ready
        and arenas_blocked
        and local_claim_blocked
        and prior_local_blocked
        and scope_ok
    )
    return [
        {
            "validation_id": "VAL1389_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if source_pass else "FAIL",
            "details": "; ".join(
                f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources
            ),
        },
        {
            "validation_id": "VAL1389_1_owner_proof",
            "check": "owner proof is exact conditional but not claimed",
            "status": "PASS" if proof_verdict and conditional_theorem else "FAIL",
            "details": "AMP1389_6 gives the conditional theorem; AMP1389_7 keeps parent signature unsigned.",
        },
        {
            "validation_id": "VAL1389_2_material_map",
            "check": "material/source class rows are present and nonclaim",
            "status": "PASS" if map_ready and class_count_ok else "FAIL",
            "details": f"class_rows={len(material_map)}; verdict_row={map_ready}",
        },
        {
            "validation_id": "VAL1389_3_coupling_convention",
            "check": "Delta_w/beta expansion convention is separated from scoring",
            "status": "PASS" if convention_ready else "FAIL",
            "details": "CEC1389_5 blocks numeric scoring until convention, classes, beta legs, kernels, and bounds are sourced.",
        },
        {
            "validation_id": "VAL1389_4_arena_refusal",
            "check": "all local arenas remain blocked",
            "status": "PASS" if arenas_blocked and local_claim_blocked and prior_local_blocked else "FAIL",
            "details": "ARM1389 rows and GATE1389_5 block local claims; prior GATE1388_5 is still blocked.",
        },
        {
            "validation_id": "VAL1389_5_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if scope_ok else "FAIL",
            "details": f"ROOT={ROOT}; output_count={len(outputs)}; formalization_touched={formalization_touched}",
        },
        {
            "validation_id": "VAL1389_6_overall",
            "check": "overall 1389 validation",
            "status": "PASS" if overall else "FAIL",
            "details": "1389 writes the conditional action-measure owner theorem and nonclaim material/source map without enabling local scoring.",
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    proof: list[dict[str, str]],
    material_map: list[dict[str, str]],
    convention: list[dict[str, str]],
    arenas: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    generated = datetime.now(timezone.utc).isoformat()
    body = f"""# 1389 - Y5 R10 RAB Delta-w Material Source Map Or Action-Measure Owner Proof

**Generated:** {generated}

**Current verdict:** the clean zero route is now an exact conditional theorem: object-language owner + action-measure owner + connected ordinary matter + current owner + derivative silence would force `Delta_w_A=0` and `beta_w,A=0`. The current corpus still does not parent-sign those clauses together.

**Discipline move:** because the owner theorem is unsigned, `Delta_w_A` is no longer allowed to float as one vague symbol. It is split into explicit material/source classes for bulk matter, electronic/atomic standards, nuclear binding, EM binding, orbital bodies, and R10 source/test legs. Every row remains nonclaim.

**Claim ceiling:** {CLAIM_CEILING}

## Source Register

{md_table(sources)}

## Action-Measure Owner Proof Attempt

{md_table(proof)}

## Material / Source Class Map

{md_table(material_map)}

## Coupling Expansion Convention

{md_table(convention)}

## Arena Requirement Matrix

{md_table(arenas)}

## Claim Gates

{md_table(gates)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    proof = owner_proof_rows()
    material_map = material_map_rows()
    convention = coupling_convention_rows()
    arenas = arena_requirement_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, proof, material_map, convention, arenas, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(OWNER_PROOF_PATH, proof)
    write_csv(MATERIAL_MAP_PATH, material_map)
    write_csv(COUPLING_CONVENTION_PATH, convention)
    write_csv(ARENA_REQUIREMENTS_PATH, arenas)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, proof, material_map, convention, arenas, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1389 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()

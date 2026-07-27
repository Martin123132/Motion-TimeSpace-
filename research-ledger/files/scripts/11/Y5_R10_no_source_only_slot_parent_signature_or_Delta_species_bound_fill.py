from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1214"
TITLE = "1214-Y5-R10-no-source-only-slot-parent-signature-or-Delta-species-bound-fill"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
SIGNATURE_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_NO_SOURCE_ONLY_SLOT_SIGNATURE_AUDIT.csv"
BOUND_FILL_PATH = OUT_DIR / f"{PACK_ID}_DELTA_SPECIES_BOUND_FILL.csv"
ARENA_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_ARENA_PROJECTION_LEDGER.csv"
FEED_PATH = OUT_DIR / f"{PACK_ID}_SSR1213_FEED_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1214_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def load_csv(path: Path) -> list[dict[str, str]]:
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


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def bool_false(row: dict[str, object], key: str) -> bool:
    value = row.get(key, False)
    if isinstance(value, bool):
        return not value
    return str(value).strip().lower() == "false"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1214_0_1213_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1213_NEXT_TARGET.csv",
            "needle": "1214-Y5-R10-no-source-only-slot-parent-signature-or-Delta-species-bound-fill.md",
            "purpose": "1213 handoff selecting the no-source-only-slot / Delta species target",
        },
        {
            "source_id": "SRC1214_1_1213_species_bound",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1213_SOURCE_SIDE_BOUND_DECOMPOSITION.csv",
            "needle": "SSB1213_1_species_weight",
            "purpose": "B_species_weight source-side bound decomposition",
        },
        {
            "source_id": "SRC1214_2_1213_species_row",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1213_SOURCE_SIDE_OBSTRUCTION_ROWS.csv",
            "needle": "SSR1213_1_Delta_species_weight",
            "purpose": "row to be filled or fed by 1214",
        },
        {
            "source_id": "SRC1214_3_1065_zero_clause",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1065_WA_THEOREM_ZERO_CLAUSES.csv",
            "needle": "WTZ1065_4_verdict",
            "purpose": "earlier no-source-only-slot theorem-zero verdict",
        },
        {
            "source_id": "SRC1214_4_1067_action_scale",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv",
            "needle": "ASO1067_5_verdict",
            "purpose": "action-scale owner obstruction for species action weights",
        },
        {
            "source_id": "SRC1214_5_1079_current_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
            "needle": "NCO1079_6_verdict",
            "purpose": "narrow current-owner partial theorem and pre-variation species-weight survival",
        },
        {
            "source_id": "SRC1214_6_1088_MOMS_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
            "needle": "MOMS1088_4_no_species_weights",
            "purpose": "minimal ordinary-matter signature clause that would kill species weights",
        },
        {
            "source_id": "SRC1214_7_1088_conditional_zero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
            "needle": "THM1088_6_current_corpus_verdict",
            "purpose": "conditional qbar/source-current zero theorem not promoted",
        },
        {
            "source_id": "SRC1214_8_1090_axioms",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv",
            "needle": "AX1090_2_common_quantum_measure",
            "purpose": "missing common quantum/action measure axiom blocks no species weights",
        },
        {
            "source_id": "SRC1214_9_1090_closure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1090_CLOSURE_DEMOTION_REGISTER.csv",
            "needle": "CLOS1090_0_MOMS",
            "purpose": "MOMS retained only as closure candidate",
        },
        {
            "source_id": "SRC1214_10_1091_residuals",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1091_FINITE_RESIDUAL_ROUTE_MAP.csv",
            "needle": "FR1091_5_qbar_source_label",
            "purpose": "finite residual route for source labels and material constants",
        },
        {
            "source_id": "SRC1214_11_1080_finite_pack",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1080_FINITE_WEP_INPUT_PACK_NONCLAIM.csv",
            "needle": "FIP1080_0_product_formula",
            "purpose": "finite WEP input pack for source/material/coupling/readout rows",
        },
        {
            "source_id": "SRC1214_12_1081_DD_smoke",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1081_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv",
            "needle": "DDS1081_2_equal_two_component_unit",
            "purpose": "numeric external DD smoke sensitivity rows retained as nonclaim scaffold",
        },
        {
            "source_id": "SRC1214_13_local_bounds",
            "local_path": "source-intake/local_bounds/local_bound_claims.csv",
            "needle": "R10_fifth_force",
            "purpose": "local WEP/PPN/Gdot/R10 bound anchor table",
        },
    ]

    source_rows: list[dict[str, object]] = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_rows.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    signature_audit = [
        {
            "audit_id": "NSS1214_0_target",
            "clause": "no source-only species slot",
            "attempt": "prove the parent matter language has no independent w_A(X) S_A or material-only source multiplier before variation",
            "result": "TARGET_EXACT",
            "obstruction": "must be signed by the parent object language/action-measure owner, not assumed by taste",
            "effect_on_Delta_species": "would imply Delta_species_weight=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSS1214_1_MOMS_no_species_weight",
            "clause": "MOMS1088_4_no_species_weights",
            "attempt": "use the minimal ordinary-matter signature to exclude pre-action species weights",
            "result": "CONDITIONAL_ONLY",
            "obstruction": "MOMS1088_7 is not parent-derived and CLOS1090_0 demotes MOMS to closure candidate",
            "effect_on_Delta_species": "zero only on closure branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSS1214_2_action_measure_owner",
            "clause": "common hbar/action measure/current normalization",
            "attempt": "make w_A S_A a gauge/quotient redundancy or impossible syntax",
            "result": "NOT_PARENT_SIGNED",
            "obstruction": "AX1090_2 and ASO1067_5 remain unsigned; classical EOM scaling does not kill Hilbert-source scaling",
            "effect_on_Delta_species": "pre-variation weights remain legal finite residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSS1214_3_current_owner_partial",
            "clause": "Hilbert source/current owner",
            "attempt": "use variation-before-readout to forbid source selectors and current rescalings after Hilbert variation",
            "result": "PARTIAL_SUBTHEOREM",
            "obstruction": "NCO1079_6 says pre-variation species weights survive current ownership",
            "effect_on_Delta_species": "kills some post-variation cheating, not Delta_species_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSS1214_4_common_G_absorption_guard",
            "clause": "measured G absorbs only common universal factors",
            "attempt": "absorb relative species/source weights into local calibration",
            "result": "FORBIDDEN_EXCEPT_COMMON_MODE",
            "obstruction": "relative, time, range, frame, source, or species dependence is physical residual, not calibration",
            "effect_on_Delta_species": "Delta_species must be bounded explicitly unless zero theorem signs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSS1214_5_verdict",
            "clause": "Delta_species_weight theorem-zero",
            "attempt": "assemble MOMS, action-measure owner, current owner, and common-mode guard",
            "result": "ZERO_NOT_PARENT_SIGNED",
            "obstruction": "object-language/action-measure clauses remain unsigned; closure-only theorem cannot feed R10/PPN/WEP claims",
            "effect_on_Delta_species": "route to finite bound row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    bound_rows = [
        {
            "bound_id": "DSB1214_0_B_species_weight_total",
            "target": "SSR1213_1_Delta_species_weight.B_species_weight",
            "formula": "B_species_weight <= B_pre_action_weight + B_constant_sector + B_source_label + B_shadow_marker + B_time_range_frame + B_projection_map",
            "basis": "1213 absolute no-cancellation rule plus 1088/1090/1091 finite residual route",
            "required_inputs": "B_pre_action_weight;B_constant_sector;B_source_label;B_shadow_marker;B_time_range_frame;B_projection_map;same_norm_id;source_paths",
            "value_or_status": "MISSING_COMPONENT_VALUES",
            "units": "same_as_source_side_norm",
            "source_path": str(BOUND_FILL_PATH.relative_to(ROOT)),
            "current_status": "BOUND_FORM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "DSB1214_1_pre_action_weight",
            "target": "B_pre_action_weight",
            "formula": "C_w * ||Delta w_A||_absolute",
            "basis": "pre-variation w_A S_A survives unless common action-measure owner signs",
            "required_inputs": "C_w;Delta_w_A prior or theorem-zero;parent action-measure source",
            "value_or_status": "MISSING_PARENT_MEASURE_OWNER_OR_PRIOR",
            "units": "same_as_source_side_norm",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv",
            "current_status": "UNFILLED_COMPONENT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "DSB1214_2_constant_sector",
            "target": "B_constant_sector",
            "formula": "sum_i |b_i * tau_i| over alpha, mu, nuclear, clock, and mass-response channels",
            "basis": "1091 finite residual route retains constant-sector coefficients unless fixed by parent representation data",
            "required_inputs": "b_alpha;tau_clock_or_WEP_R10_projection;b_mu;b_nuc;b_clock_i;Xhat normalization",
            "value_or_status": "PARTIAL_ALPHA_CLOCK_BOUND_ONLY_NO_LOCAL_TRANSFER",
            "units": "mixed_until_projection_normalized",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1091_FINITE_RESIDUAL_ROUTE_MAP.csv",
            "current_status": "UNFILLED_COMPONENT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "DSB1214_3_source_label",
            "target": "B_source_label",
            "formula": "|qbar_source_label| * |tau_source_projection|",
            "basis": "source labels remain retained unless source-label forgetting / no-source-only-slot theorem signs",
            "required_inputs": "qbar_source_label prior or theorem-zero;tau_source_projection;arena map",
            "value_or_status": "MISSING_SOURCE_LABEL_PRIOR_AND_PROJECTION",
            "units": "same_as_source_side_norm",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1091_FINITE_RESIDUAL_ROUTE_MAP.csv",
            "current_status": "UNFILLED_COMPONENT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "DSB1214_4_shadow_marker_time_range_frame",
            "target": "B_shadow_marker + B_time_range_frame",
            "formula": "||shadow/domain/material_marker|| + ||Delta_w_time|| + ||Delta_w_range(lambda)|| + ||Delta_w_frame||",
            "basis": "MOMS/no-hidden-domain and operator-domain no-hidden-visible-hom remain closure-only",
            "required_inputs": "domain_marker_bound;range_profile;Gdot_or_time_bound;PPN_frame_bound;R10 kernel",
            "value_or_status": "MISSING_DOMAIN_RANGE_TIME_FRAME_INPUTS",
            "units": "same_as_source_side_norm",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv",
            "current_status": "UNFILLED_COMPONENT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "DSB1214_5_projection_map",
            "target": "B_projection_map",
            "formula": "arena absolute projection factors: tau_WEP, tau_R10(lambda), C_gamma, C_beta, K_clock, K_orbital",
            "basis": "a finite species residual is not testable until projected into the arena using the same branch/norm",
            "required_inputs": "arena kernels and source/test material vectors in one normalization",
            "value_or_status": "MISSING_ARENA_PROJECTION_MAPS",
            "units": "dimensionless_projection_or_declared_arena_units",
            "source_path": str(ARENA_LEDGER_PATH.relative_to(ROOT)),
            "current_status": "UNFILLED_COMPONENT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    arena_rows = [
        {
            "arena_id": "ARENA1214_0_WEP",
            "arena": "MICROSCOPE_WEP",
            "bound_anchor": "R1_WEP_source_charge upper_bound=2.8e-15 dimensionless",
            "projection_needed": "C_parent, R_source^Earth, R_TA6V_minus_PtRh10, K_MICROSCOPE, or direct parent eta product",
            "current_status": "BOUND_ANCHOR_ONLY_PRODUCT_MISSING",
            "blocks_claim": "missing same-basis product",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "ARENA1214_1_PPN",
            "arena": "PPN_gamma_beta",
            "bound_anchor": "R3_gamma=2.3e-05; R4_beta=7.8e-05",
            "projection_needed": "C_gamma_source_weight, C_beta_source_weight, weak-field source response map",
            "current_status": "PROJECTION_OPERATOR_MISSING",
            "blocks_claim": "cannot infer PPN residual from species weight without response operator",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "ARENA1214_2_R10",
            "arena": "R10_short_range",
            "bound_anchor": "R10_fifth_force symbolic alpha(lambda)",
            "projection_needed": "lambda_X, K_w(lambda), Delta_w_source, Delta_w_test, tau_R10(lambda), real alpha(lambda) curve",
            "current_status": "CURVE_AND_PRODUCT_MISSING",
            "blocks_claim": "symbolic curve plus missing product cannot score R10",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "ARENA1214_3_Gdot_time",
            "arena": "LLR_Gdot_or_time_dependence",
            "bound_anchor": "R9_Gdot upper_bound=9.6e-15 yr^-1",
            "projection_needed": "Delta_w_time map, source mass/time response, same-frame Gdot convention",
            "current_status": "TIME_RESPONSE_MAP_MISSING",
            "blocks_claim": "cannot absorb or bound time-varying relative weights without map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "ARENA1214_4_clocks",
            "arena": "clock_redshift_and_alpha_drift",
            "bound_anchor": "R2_clock_redshift plus existing b_alpha*tau_clock product chain",
            "projection_needed": "tau_clock, Xhat normalization, separation of alpha/mass/nuclear channels",
            "current_status": "CLOCK_PRODUCT_NOT_LOCAL_SPECIES_TRANSFER_MISSING_PROJECTION",
            "blocks_claim": "clock product cannot be transferred to WEP/R10 without projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "ARENA1214_5_orbital",
            "arena": "orbital_solar_system",
            "bound_anchor": "PPN/LLR rows in local_bound_claims",
            "projection_needed": "source-mass normalization, worldtube/orbital response, preferred-frame split",
            "current_status": "ORBITAL_SOURCE_RESPONSE_MISSING",
            "blocks_claim": "no local-GR/orbital pass from species bound row alone",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    feed_rows = [
        {
            "feed_id": "FEED1214_0_to_SSR1213_1",
            "target_row": "SSR1213_1_Delta_species_weight",
            "field_to_fill": "B_species_weight",
            "source_row": "DSB1214_0_B_species_weight_total",
            "update_value": "B_pre_action_weight + B_constant_sector + B_source_label + B_shadow_marker + B_time_range_frame + B_projection_map",
            "claim_policy": "formula-only feed; valid only after every component is numeric/source-backed or theorem-zero in the same norm",
            "current_status": "FEED_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1214_1_to_SSR1213_0",
            "target_row": "SSR1213_0_G_source_side_bound",
            "field_to_fill": "B_species_weight",
            "source_row": "DSB1214_0_B_species_weight_total",
            "update_value": "nonclaim symbolic component of G_source_side_bound",
            "claim_policy": "does not make G_source_side numeric; it only replaces one MISSING label by a decomposed missing-input row",
            "current_status": "SOURCE_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1214_0_zero_attempt",
            "condition": "Can no-source-only-slot be parent-signed now?",
            "decision": "No. It is an exact conditional theorem under MOMS/action-measure assumptions, but the parent source remains unsigned.",
            "result": "Delta_species_weight is not theorem-zero.",
            "next_action": "use the finite bound row and keep closure-only theorem separate from claims.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1214_1_bound_fill",
            "condition": "Can SSR1213_1 be improved without faking a number?",
            "decision": "Yes. Replace the vague species-weight missing input by an absolute component envelope.",
            "result": "DSB1214_0 now feeds SSR1213_1 and SSR1213_0 as a formula-only nonclaim row.",
            "next_action": "fill or theorem-zero components one at a time, starting with the most source-backed local arena.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1214_2_next_route",
            "condition": "What is the least dishonest next target?",
            "decision": "Build a B_species finite projection input pack rather than repeating the zero proof.",
            "result": "WEP has the strongest bound anchor; R10/PPN/Gdot/clocks remain projection-gated.",
            "next_action": "1215 should try to source one component value or prove one component zero in the same norm.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1214_0_no_source_only_slot",
            "gate": "parent no-source-only-slot signature signed",
            "status": "BLOCKED",
            "reason": "MOMS/action-measure/object-language premises remain closure-only or unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1214_1_Delta_species_zero",
            "gate": "Delta_species_weight=0 theorem-zero",
            "status": "BLOCKED",
            "reason": "pre-variation species weights survive current-owner theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1214_2_B_species_numeric",
            "gate": "B_species_weight numeric/source-backed",
            "status": "BLOCKED",
            "reason": "component values and same-norm arena projections are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1214_3_source_side_numeric",
            "gate": "SSR1213_0 G_source_side_bound numeric",
            "status": "BLOCKED",
            "reason": "1214 fills only the formula decomposition for one component, not numeric values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1214_4_local_GR_R10_WEP",
            "gate": "local-GR/R10/WEP pass",
            "status": "BLOCKED",
            "reason": "no theorem-zero and no finite product row passes",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1214_0_1215",
            "target_file": "1215-Y5-R10-Bspecies-finite-projection-input-pack-or-component-zero.md",
            "target_script": "scripts/Y5_R10_Bspecies_finite_projection_input_pack_or_component_zero.py",
            "task": "try to source or theorem-zero the first component of DSB1214_0 in the same norm: WEP source label/material response first, then PPN/R10/Gdot/clock projections",
            "success_condition": "at least one B_species component becomes numeric/source-backed or theorem-zero without measured-G absorption, unity shortcuts, or cancellation",
            "do_not_do": "do not claim local GR; do not use MOMS closure as proof; do not treat DD smoke or WEP bound anchors as MTS predictions; do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "absolute_path", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    audit_fields = ["audit_id", "clause", "attempt", "result", "obstruction", "effect_on_Delta_species", "valid_for_claim", "claim_allowed"]
    bound_fields = ["bound_id", "target", "formula", "basis", "required_inputs", "value_or_status", "units", "source_path", "current_status", "valid_for_claim", "claim_allowed"]
    arena_fields = ["arena_id", "arena", "bound_anchor", "projection_needed", "current_status", "blocks_claim", "valid_for_claim", "claim_allowed"]
    feed_fields = ["feed_id", "target_row", "field_to_fill", "source_row", "update_value", "claim_policy", "current_status", "valid_for_claim", "claim_allowed"]
    decision_fields = ["decision_id", "condition", "decision", "result", "next_action", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(SIGNATURE_AUDIT_PATH, signature_audit, audit_fields)
    write_csv(BOUND_FILL_PATH, bound_rows, bound_fields)
    write_csv(ARENA_LEDGER_PATH, arena_rows, arena_fields)
    write_csv(FEED_PATH, feed_rows, feed_fields)
    write_csv(DECISION_PATH, decisions, decision_fields)
    write_csv(CLAIM_GATES_PATH, claim_gates, gate_fields)
    write_csv(NEXT_PATH, next_rows, next_fields)

    csvs_to_parse = [
        SOURCE_REGISTER_PATH,
        SIGNATURE_AUDIT_PATH,
        BOUND_FILL_PATH,
        ARENA_LEDGER_PATH,
        FEED_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]
    csv_parse_ok = True
    parse_details: list[str] = []
    for csv_path in csvs_to_parse:
        try:
            rows = load_csv(csv_path)
            parse_details.append(f"{csv_path.name}:{len(rows)}")
        except Exception as exc:  # noqa: BLE001
            csv_parse_ok = False
            parse_details.append(f"{csv_path.name}:ERROR:{exc}")

    local_bound_ids = {row.get("row_id"): row for row in load_csv(LOCAL_BOUNDS)}
    required_bound_ids = ["R1_WEP_source_charge", "R3_gamma", "R4_beta", "R9_Gdot", "R10_fifth_force"]
    local_bounds_present = all(row_id in local_bound_ids for row_id in required_bound_ids)
    numeric_anchor_values: list[float] = []
    for row_id in ["R1_WEP_source_charge", "R3_gamma", "R4_beta", "R9_Gdot"]:
        try:
            numeric_anchor_values.append(float(local_bound_ids[row_id]["upper_bound"]))
        except Exception:  # noqa: BLE001
            numeric_anchor_values.append(float("nan"))
    numeric_bounds_positive = all(value > 0 for value in numeric_anchor_values)

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if mtime >= RUN_STARTED_UTC:
                    formalization_recent.append(path)

    all_sources_exist = all(bool(row["path_exists"]) for row in source_rows)
    all_needles_found = all(bool(row["needle_found"]) for row in source_rows)
    zero_not_promoted = any(row["audit_id"] == "NSS1214_5_verdict" and row["result"] == "ZERO_NOT_PARENT_SIGNED" for row in signature_audit)
    bound_total_present = any(row["bound_id"] == "DSB1214_0_B_species_weight_total" for row in bound_rows)
    feed_present = any(row["feed_id"] == "FEED1214_0_to_SSR1213_1" for row in feed_rows)
    arena_projection_blocked = all("MISSING" in row["current_status"] or "ONLY" in row["current_status"] for row in arena_rows)
    no_missing_claim_rows = all(not (not bool_false(row, "valid_for_claim") and "MISSING" in " ".join(str(value) for value in row.values())) for row in bound_rows + arena_rows + feed_rows)
    no_claim = all(
        bool_false(row, "valid_for_claim") and bool_false(row, "claim_allowed")
        for row in signature_audit + bound_rows + arena_rows + feed_rows + decisions + claim_gates + next_rows
    )
    formalization_untouched = len(formalization_recent) == 0
    next_1215 = next_rows[0]["target_file"].startswith("1215-")

    validation_rows = [
        validation_row("VAL1214_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1214_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1214_2_zero_not_promoted", "no-source-only-slot zero is not promoted", zero_not_promoted, "NSS1214_5 verdict keeps zero unsigned"),
        validation_row("VAL1214_3_bound_total_present", "B_species total bound row exists", bound_total_present, "DSB1214_0 feeds SSR1213_1"),
        validation_row("VAL1214_4_feed_present", "SSR1213 feed row exists", feed_present, "FEED1214_0_to_SSR1213_1 present"),
        validation_row("VAL1214_5_arena_projection_blocked", "arena projections remain blocked", arena_projection_blocked, "WEP/PPN/R10/Gdot/clock/orbital rows require source-backed maps"),
        validation_row("VAL1214_6_local_bounds_present", "local bound anchors present", local_bounds_present, ";".join(required_bound_ids)),
        validation_row("VAL1214_7_numeric_bounds_positive", "numeric bound anchors positive", numeric_bounds_positive, ",".join(str(value) for value in numeric_anchor_values)),
        validation_row("VAL1214_8_no_missing_claim_rows", "no row with MISSING is valid for claim", no_missing_claim_rows, "all missing rows remain nonclaim"),
        validation_row("VAL1214_9_nonclaim_policy", "all generated rows remain nonclaim", no_claim, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1214_10_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1214_11_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
        validation_row("VAL1214_12_next_target", "next target is staged", next_1215, next_rows[0]["target_file"]),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1214_13_overall",
            "overall 1214 validation",
            validation_pass,
            "1214 no-source-only-slot audit and Delta_species bound-fill pack is reproducible and nonclaim" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1214 Y5/R10 No-Source-Only-Slot Parent Signature Or Delta Species Bound Fill

**Current verdict:** 1214 does **not** parent-sign the no-source-only-slot theorem. The clean zero route still exists only as a MOMS/action-measure closure theorem, not as a derived local-GR/R10/WEP claim.

**Main progress:** `SSR1213_1_Delta_species_weight` now has a decomposed nonclaim bound row: `B_species_weight <= B_pre_action_weight + B_constant_sector + B_source_label + B_shadow_marker + B_time_range_frame + B_projection_map`.

**Practical meaning:** the coupling problem has been sharpened. Species/source coupling is no longer one foggy missing label; it is a finite list of components that must be killed by theorem or filled with source-backed, same-norm projection rows.

## Source Register

{markdown_table(source_rows, source_fields)}

## No-Source-Only-Slot Signature Audit

{markdown_table(signature_audit, audit_fields)}

## Delta Species Bound Fill

{markdown_table(bound_rows, bound_fields)}

## Arena Projection Ledger

{markdown_table(arena_rows, arena_fields)}

## SSR1213 Feed Update

{markdown_table(feed_rows, feed_fields)}

## Decision Ledger

{markdown_table(decisions, decision_fields)}

## Claim Gates

{markdown_table(claim_gates, gate_fields)}

## Next Target

{markdown_table(next_rows, next_fields)}

## Validation

{markdown_table(validation_rows, validation_fields)}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"validation_pass={validation_pass}")
    print("Delta_species_zero_claimed=false")
    print("B_species_bound_row=DSB1214_0_B_species_weight_total")


if __name__ == "__main__":
    main()

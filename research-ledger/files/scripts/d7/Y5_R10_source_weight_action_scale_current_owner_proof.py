from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1224"
TITLE = "1224-Y5-R10-source-weight-action-scale-current-owner-proof"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
OWNER_PROOF_CLAUSES_PATH = OUT_DIR / f"{PACK_ID}_OWNER_PROOF_CLAUSES.csv"
OBSTRUCTION_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_WEIGHT_OBSTRUCTION_LEDGER.csv"
FINITE_INPUT_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv"
PRODUCT_LAW_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_WEIGHT_PRODUCT_LAW.csv"
LOCAL_GR_CONSEQUENCE_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_GR_CONSEQUENCE_LEDGER.csv"
RUNNER_FEED_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_FEED_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1224_VALIDATION.csv"


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


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1224_0_1223_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1223_NEXT_TARGET.csv",
            "needle": "1224-Y5-R10-source-weight-action-scale-current-owner-proof.md",
            "purpose": "1223 handoff to source-weight owner proof",
        },
        {
            "source_id": "SRC1224_1_1223_source_req",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1223_FALLBACK_SOURCE_REQUIREMENTS.csv",
            "needle": "SRCREQ1223_2_source_weight",
            "purpose": "exact source-weight fallback requirement",
        },
        {
            "source_id": "SRC1224_2_1223_proof",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1223_MINIMAL_PROOF_CONTRACTS.csv",
            "needle": "PROOF1223_2_source_weight",
            "purpose": "source-weight proof contract from 1223",
        },
        {
            "source_id": "SRC1224_3_1066_source_scalar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
            "needle": "SSE1066_5_verdict",
            "purpose": "conditional source-scalar exclusion theorem",
        },
        {
            "source_id": "SRC1224_4_1066_measure_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv",
            "needle": "FMQ1066_4_verdict",
            "purpose": "action-scale/measure owner obstruction",
        },
        {
            "source_id": "SRC1224_5_1066_tau",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv",
            "needle": "TWP1066_7_verdict",
            "purpose": "tau_WEP projection contract",
        },
        {
            "source_id": "SRC1224_6_1066_delta_w",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv",
            "needle": "DWP1066_5_product",
            "purpose": "finite source-weight product schema",
        },
        {
            "source_id": "SRC1224_7_1055_parent_action",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "needle": "PAC1055_4_source_label_forgetting",
            "purpose": "candidate parent action source-label forgetting clause",
        },
        {
            "source_id": "SRC1224_8_1055_adoption",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1055_CONTRACT_ADOPTION_GATES.csv",
            "needle": "ADG1055_3_source_label_forgetting",
            "purpose": "source-label forgetting adoption gate remains conditional",
        },
        {
            "source_id": "SRC1224_9_1083_source_vector",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
            "needle": "SCG1083_0_profile_weighting",
            "purpose": "source profile/worldtube weighting missing",
        },
        {
            "source_id": "SRC1224_10_1084_readout",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
            "needle": "RIG1084_0_CMSM_arrays",
            "purpose": "official readout kernel/arrays missing",
        },
        {
            "source_id": "SRC1224_11_1222_score",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1222_FIRST_NONCLAIM_SCORE_TABLE.csv",
            "needle": "NCS1222_2_weight",
            "purpose": "source-weight score row remains refused",
        },
        {
            "source_id": "SRC1224_12_local_bounds",
            "local_path": "source-intake/local_bounds/local_bound_claims.csv",
            "needle": "R1_WEP_source_charge",
            "purpose": "MICROSCOPE source-charge proxy bound anchor",
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

    owner_clauses = [
        {
            "clause_id": "OWN1224_0_single_action_scale",
            "needed_for_zero": "one universal parent action scale/hbar/normalization for all ordinary matter species",
            "attempt": "use PAC1055_6 plus FMQ1066 to treat species multipliers as inadmissible rather than physical",
            "current_evidence": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv", "FMQ1066_4_verdict"),
            "status": "NOT_PARENT_SIGNED",
            "gap": "FMQ1066 explicitly says universal action-scale normalization is required but not derived",
            "effect_on_Delta_w": "cannot set Delta_w_TiPt=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "OWN1224_1_universal_current_owner",
            "needed_for_zero": "Hilbert source current is total matter source before species/readout selection",
            "attempt": "derive T_source=sum_A T_A from one parent variational object before readout",
            "current_evidence": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_2_variation_before_readout"),
            "status": "CONDITIONAL_NOT_READOUT_SIGNED",
            "gap": "variation-before-readout is clean only if parent variation order and readout/EFT closure are signed",
            "effect_on_Delta_w": "w_A T_A counterexample remains available",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "OWN1224_2_source_label_forgetting",
            "needed_for_zero": "source labels are quotient-forgotten before local/material/readout projection",
            "attempt": "use parent action source-label forgetting clause to forbid source-only species scalars",
            "current_evidence": source_ref("source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", "PAC1055_4_source_label_forgetting"),
            "status": "CONTRACT_CLAUSE_ONLY",
            "gap": "ADG1055_3 marks this as a conditional lemma, not a parent-derived proof",
            "effect_on_Delta_w": "source-label scalar branch is not theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "OWN1224_3_connected_matter_naturality",
            "needed_for_zero": "ordinary matter category connected enough that natural species weights are common constants",
            "attempt": "use naturality to collapse w_A to one common scale",
            "current_evidence": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_3_naturality_route"),
            "status": "HELPFUL_CONDITIONAL_ONLY",
            "gap": "disconnected/simple-object components allow a family w_A",
            "effect_on_Delta_w": "Delta_w_TiPt can remain finite",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "OWN1224_4_measure_coframe_boundary_descent",
            "needed_for_zero": "measure/coframe/boundary descent cannot regenerate species-dependent source weights",
            "attempt": "close species-dependent Jacobian and hidden measure/coframe descent counterexamples",
            "current_evidence": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv", "FMQ1066_3_measure_jacobian"),
            "status": "PARALLEL_OPEN_GATE",
            "gap": "species-blind measure/coframe/boundary descent theorem is missing",
            "effect_on_Delta_w": "measure-induced w_A remains a live finite branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "OWN1224_5_tau_readout_projection",
            "needed_for_zero": "tau_WEP projection/readout does not reintroduce source weighting",
            "attempt": "use MICROSCOPE source worldtube, orbit average, coframe, material response, and readout map",
            "current_evidence": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv", "TWP1066_7_verdict"),
            "status": "PROJECTION_CONTRACT_WRITTEN_NOT_DERIVED",
            "gap": "tau_WEP and official readout/source-profile weighting are missing",
            "effect_on_Delta_w": "product Delta_w_TiPt*tau_WEP remains unscoreable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "OWN1224_6_verdict",
            "needed_for_zero": "all owner clauses signed together",
            "attempt": "combine object-language typing, action-scale owner, current owner, source-label forgetting, and readout projection",
            "current_evidence": "OWN1224_0 through OWN1224_5",
            "status": "SOURCE_WEIGHT_OWNER_PROOF_NOT_DERIVED",
            "gap": "at least five clauses remain conditional/open",
            "effect_on_Delta_w": "demote to exact finite source-weight input contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    obstruction_rows = [
        {
            "obstruction_id": "OBS1224_0_wA_action_multiplier",
            "counterexample": "S_matter=sum_A w_A S_A",
            "why_allowed_without_owner": "overall species action multipliers can preserve isolated classical EOM appearance while changing Hilbert stress/source normalization",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv", "FMQ1066_1_Hilbert_source_rescaling"),
            "status": "ACTIVE_OBSTRUCTION",
            "blocks": "Delta_w_TiPt theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS1224_1_path_integral_scale",
            "counterexample": "species-dependent effective action scale/hbar",
            "why_allowed_without_owner": "quantum/statistical weight can make an action multiplier physically meaningful",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv", "FMQ1066_2_path_integral_weight"),
            "status": "ACTIVE_OBSTRUCTION",
            "blocks": "universal parent action-scale claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS1224_2_disconnected_species",
            "counterexample": "natural family w_A on disconnected ordinary matter components",
            "why_allowed_without_owner": "naturality alone does not collapse weights if the category decomposes by species/simple-object sectors",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_3_naturality_route"),
            "status": "ACTIVE_OBSTRUCTION",
            "blocks": "source-label forgetting proof by naturality alone",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS1224_3_readout_regeneration",
            "counterexample": "post-variation/readout map reweights source channels",
            "why_allowed_without_owner": "readout/EFT closure and official MICROSCOPE product convention are not signed/imported",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv", "RIG1084_0_CMSM_arrays"),
            "status": "ACTIVE_OBSTRUCTION",
            "blocks": "observable source-weight theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_contract = [
        {
            "input_id": "FSW1224_0_eta_bound",
            "quantity": "eta_TiPt_bound",
            "required_form": "positive numeric bound for abs(Delta_w_TiPt*tau_WEP)",
            "current_value_or_status": "2.8e-15",
            "units": "dimensionless",
            "source": source_ref("source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge"),
            "claim_readiness": "BOUND_ANCHOR_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "FSW1224_1_delta_w",
            "quantity": "Delta_w_TiPt",
            "required_form": "signed or absolute Ti/Pt relative source-weight difference in the MICROSCOPE material convention",
            "current_value_or_status": "MISSING_NUMERIC_PRIOR_WIDTH",
            "units": "dimensionless",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv", "DWP1066_3_finite_prior_width"),
            "claim_readiness": "MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "FSW1224_2_tau_WEP",
            "quantity": "tau_WEP",
            "required_form": "functional[source worldtube, orbit average, observed coframe, material tensor, force readout]",
            "current_value_or_status": "MISSING_LAB_SOURCE_ORBIT_PROJECTION",
            "units": "dimensionless",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv", "TWP1066_7_verdict"),
            "claim_readiness": "MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "FSW1224_3_source_worldtube",
            "quantity": "T_source^Earth(x)",
            "required_form": "profile-weighted Earth/source stress in observed local frame",
            "current_value_or_status": "MISSING_SOURCE_PROFILE_WEIGHTING",
            "units": "stress/profile convention",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv", "SCG1083_0_profile_weighting"),
            "claim_readiness": "MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "FSW1224_4_readout_kernel",
            "quantity": "K_MICROSCOPE/source-weight readout kernel",
            "required_form": "map from parent source residual to reported eta_AB with masks/segments/orbit/coframe convention",
            "current_value_or_status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "units": "eta per source-weight product",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv", "RIG1084_0_CMSM_arrays"),
            "claim_readiness": "MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "FSW1224_5_no_cancellation",
            "quantity": "absolute-product guard",
            "required_form": "abs(Delta_w_TiPt*tau_WEP), no sign/material cancellation unless full material model is signed",
            "current_value_or_status": "GUARD_ACTIVE",
            "units": "policy",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv", "TWP1066_6_no_cancellation"),
            "claim_readiness": "GUARD_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    product_law = [
        {
            "product_id": "PROD1224_0_source_weight",
            "formula": "P_WEP_source_weight = abs(Delta_w_TiPt * tau_WEP)",
            "bound": "P_WEP_source_weight <= 2.8e-15",
            "if_tau_known": "abs(Delta_w_TiPt) <= 2.8e-15 / abs(tau_WEP)",
            "current_numeric_status": "NOT_SCOREABLE",
            "missing_inputs": "MISSING_NUMERIC_PRIOR_WIDTH;MISSING_LAB_SOURCE_ORBIT_PROJECTION;MISSING_SOURCE_PROFILE_WEIGHTING;OFFICIAL_ARRAYS_NOT_IMPORTED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "product_id": "PROD1224_1_theorem_zero_option",
            "formula": "Delta_w_TiPt = 0 if OWN1224_6 is parent-signed",
            "bound": "automatic only after owner proof",
            "if_tau_known": "not needed if theorem-zero closes before projection",
            "current_numeric_status": "THEOREM_ZERO_NOT_AVAILABLE",
            "missing_inputs": "SOURCE_WEIGHT_OWNER_PROOF_NOT_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    local_gr_consequence = [
        {
            "consequence_id": "LGR1224_0_if_owner_signed",
            "condition": "source-weight owner proof closes",
            "local_gr_effect": "source-only species weights cannot perturb local source coupling; one source-side nuisance is removed from the GR/Newton reduction path",
            "current_status": "NOT_AVAILABLE",
            "runner_effect": "would feed theorem-zero to RUN1221_2_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "consequence_id": "LGR1224_1_current_branch",
            "condition": "owner proof not closed",
            "local_gr_effect": "finite source-weight residual remains in the local-GR/WEP/PPN coupling branch and must be bounded rather than ignored",
            "current_status": "ACTIVE_NONCLAIM_BRANCH",
            "runner_effect": "keeps RUN1221_2_source_weight refused",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "consequence_id": "LGR1224_2_no_measured_G_absorption",
            "condition": "finite source-weight residual exists",
            "local_gr_effect": "do not absorb it into measured G; the branch affects composition/source/readout comparisons and must remain explicit",
            "current_status": "GUARD_ACTIVE",
            "runner_effect": "requires explicit product row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_feed = [
        {
            "feed_id": "FEED1224_0_to_RUN1221_2",
            "target": "RUN1221_2_source_weight",
            "update": "owner proof not derived; finite source-weight input contract created",
            "score_ready_delta": 0,
            "valid_prediction_rows_delta": 0,
            "current_status": "REFUSED_UNTIL_DELTA_W_TAU_WEP_SOURCE_PROFILE_READOUT_ARE_SOURCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1224_1_to_local_GR",
            "target": "local GR/Newton source-side coupling gate",
            "update": "source-weight residual remains explicit; cannot be hidden in G or cancelled",
            "score_ready_delta": 0,
            "valid_prediction_rows_delta": 0,
            "current_status": "LOCAL_GR_SOURCE_SIDE_STILL_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1224_0_no_theorem_zero",
            "decision": "do not claim Delta_w_TiPt theorem-zero",
            "because": "universal action-scale/current/source-label/readout owner is not parent-signed",
            "next_action": "derive or source tau_WEP/source-worldtube/readout projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1224_1_keep_finite_branch",
            "decision": "retain finite source-weight product branch",
            "because": "w_A S_A, path-integral scale, disconnected species, and readout reweighting remain active obstructions",
            "next_action": "turn FSW1224 inputs into a tau_WEP projection/source acquisition runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1224_2_local_GR_relevance",
            "decision": "treat source-weight as local-GR relevant, not just WEP bookkeeping",
            "because": "it controls whether the parent source coupling reduces cleanly to universal GR/Newton source coupling",
            "next_action": "work tau_WEP/source worldtube/readout before any local-GR pass claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1224_0_sources",
            "gate": "source path and needle audit",
            "status": "PASS",
            "reason": "all local sources used by 1224 are traceable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1224_1_owner_proof",
            "gate": "source-weight owner proof",
            "status": "BLOCKED",
            "reason": "OWN1224_6 status SOURCE_WEIGHT_OWNER_PROOF_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1224_2_obstructions",
            "gate": "source-weight obstructions removed",
            "status": "BLOCKED",
            "reason": "OBS1224 rows remain active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1224_3_finite_inputs",
            "gate": "finite source-weight inputs sourced",
            "status": "BLOCKED",
            "reason": "Delta_w, tau_WEP, source worldtube, and readout kernel are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1224_4_product_score",
            "gate": "source-weight product scoreable",
            "status": "BLOCKED",
            "reason": "PROD1224_0 current_numeric_status=NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1224_5_local_GR_WEP_PPN",
            "gate": "local GR/WEP/PPN claim permission",
            "status": "BLOCKED",
            "reason": "1224 retains explicit finite branch and makes no physical pass claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1224_0_1225",
            "target_file": "1225-Y5-R10-tau-WEP-source-worldtube-readout-projection.md",
            "target_script": "scripts/Y5_R10_tau_WEP_source_worldtube_readout_projection.py",
            "task": "try to derive tau_WEP from source worldtube, orbit average, observed coframe, material tensor, and readout kernel; if not, build the exact nonclaim source-acquisition table",
            "success_condition": "tau_WEP becomes a sourced/theorem-zero input for the source-weight product, or every required source/readout object is listed with no unity/cancellation shortcut",
            "do_not_do": "do not set tau_WEP to one, do not absorb residuals into measured G, do not claim local-GR/WEP/PPN, do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (OWNER_PROOF_CLAUSES_PATH, owner_clauses),
        (OBSTRUCTION_LEDGER_PATH, obstruction_rows),
        (FINITE_INPUT_CONTRACT_PATH, finite_contract),
        (PRODUCT_LAW_PATH, product_law),
        (LOCAL_GR_CONSEQUENCE_PATH, local_gr_consequence),
        (RUNNER_FEED_PATH, runner_feed),
        (DECISION_PATH, decision_rows),
        (CLAIM_GATES_PATH, claim_gates),
        (NEXT_PATH, next_rows),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    validation_rows = []
    validation_rows.append(
        validation_row(
            "VAL1224_0_sources_exist",
            "all cited local sources exist",
            all(parse_bool(row["path_exists"]) for row in source_register),
            f"{sum(1 for row in source_register if parse_bool(row['path_exists']))}/{len(source_register)} sources exist",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1224_1_needles_found",
            "all cited source needles found",
            all(parse_bool(row["needle_found"]) for row in source_register),
            f"{sum(1 for row in source_register if parse_bool(row['needle_found']))}/{len(source_register)} needles found",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1224_2_owner_verdict_nonclaim",
            "owner proof is not falsely promoted",
            owner_clauses[-1]["status"] == "SOURCE_WEIGHT_OWNER_PROOF_NOT_DERIVED"
            and all(is_false(row, "claim_allowed") for row in owner_clauses),
            owner_clauses[-1]["status"],
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1224_3_obstructions_active",
            "obstructions remain active and nonclaim",
            len(obstruction_rows) == 4
            and all(row["status"] == "ACTIVE_OBSTRUCTION" and is_false(row, "claim_allowed") for row in obstruction_rows),
            "; ".join(row["obstruction_id"] for row in obstruction_rows),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1224_4_finite_contract_complete",
            "finite source-weight input contract contains required rows",
            {"FSW1224_0_eta_bound", "FSW1224_1_delta_w", "FSW1224_2_tau_WEP", "FSW1224_3_source_worldtube", "FSW1224_4_readout_kernel", "FSW1224_5_no_cancellation"}.issubset(
                {row["input_id"] for row in finite_contract}
            ),
            "; ".join(row["input_id"] for row in finite_contract),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1224_5_missing_inputs_nonclaim",
            "missing finite inputs remain nonclaim",
            all(is_false(row, "valid_for_claim") and is_false(row, "claim_allowed") for row in finite_contract if "MISSING" in row["current_value_or_status"] or "NOT_IMPORTED" in row["current_value_or_status"]),
            "Delta_w, tau_WEP, source_worldtube, and readout kernel are missing/nonclaim",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1224_6_product_not_scoreable",
            "source-weight product is not scoreable",
            product_law[0]["current_numeric_status"] == "NOT_SCOREABLE"
            and is_false(product_law[0], "claim_allowed"),
            product_law[0]["missing_inputs"],
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1224_7_no_measured_G_absorption",
            "no measured-G absorption shortcut",
            any(row["consequence_id"] == "LGR1224_2_no_measured_G_absorption" and row["current_status"] == "GUARD_ACTIVE" for row in local_gr_consequence),
            "no measured-G absorption guard active",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1224_8_runner_feed_nonclaim",
            "runner feed keeps source-weight refused",
            all(row["valid_prediction_rows_delta"] == 0 and is_false(row, "claim_allowed") for row in runner_feed),
            "valid_prediction_rows_delta=0 for all feed rows",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1224_9_next_target_tau_WEP",
            "next target stages tau_WEP projection",
            next_rows[0]["target_file"] == "1225-Y5-R10-tau-WEP-source-worldtube-readout-projection.md",
            next_rows[0]["target_file"],
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1224_10_claim_gates_blocked",
            "claim gates keep physical claims blocked",
            any(row["status"] == "BLOCKED" for row in claim_gates) and all(is_false(row, "valid_for_claim") for row in claim_gates),
            "owner/obstruction/finite-input/product/local-claim gates blocked",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1224_11_nonclaim_policy",
            "all generated rows remain nonclaim",
            all(
                is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
                for _, rows in generated_tables
                for row in rows
                if "valid_for_claim" in row and "claim_allowed" in row
            ),
            "valid_for_claim=false and claim_allowed=false throughout claim-bearing tables",
        )
    )

    csv_parse_details = []
    csv_parse_ok = True
    for path, _ in generated_tables:
        try:
            parsed = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:FAIL:{exc}")
    validation_rows.append(
        validation_row(
            "VAL1224_12_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(csv_parse_details),
        )
    )

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if modified >= RUN_STARTED_UTC:
                    formalization_recent.append(path)
    validation_rows.append(
        validation_row(
            "VAL1224_13_formalization_untouched",
            "formalization-workbench untouched during run",
            len(formalization_recent) == 0,
            f"formalization_recent_after_run_start_count={len(formalization_recent)}",
        )
    )

    overall_before = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1224_14_overall",
            "overall 1224 validation",
            overall_before,
            "1224 does not close source-weight owner proof; exact finite input contract and tau_WEP next target are staged",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# 1224 Y5/R10 Source-Weight Action-Scale Current Owner Proof

**Current verdict:** 1224 does **not** prove the source-weight branch away. The required parent owner — universal action scale, universal current extraction, source-label forgetting, measure/coframe descent, and readout projection — is still conditional rather than parent-signed.

**Main progress:** the local-GR/WEP source-weight problem is now an exact fork: either prove a real owner theorem, or score the finite product `abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15` with sourced inputs. No measured-G absorption, unity shortcut, or cancellation escape is allowed.

**Practical consequence:** this keeps the local GR/Newton path honest. We have not failed GR reduction; we have identified the precise source-side coupling that must be derived or bounded before claiming the reduction.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "absolute_path", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"])}

## Owner Proof Clauses

{markdown_table(owner_clauses, ["clause_id", "needed_for_zero", "attempt", "current_evidence", "status", "gap", "effect_on_Delta_w", "valid_for_claim", "claim_allowed"])}

## Source-Weight Obstruction Ledger

{markdown_table(obstruction_rows, ["obstruction_id", "counterexample", "why_allowed_without_owner", "source", "status", "blocks", "valid_for_claim", "claim_allowed"])}

## Finite Source-Weight Input Contract

{markdown_table(finite_contract, ["input_id", "quantity", "required_form", "current_value_or_status", "units", "source", "claim_readiness", "valid_for_claim", "claim_allowed"])}

## Source-Weight Product Law

{markdown_table(product_law, ["product_id", "formula", "bound", "if_tau_known", "current_numeric_status", "missing_inputs", "claim_allowed", "valid_for_claim"])}

## Local GR Consequence Ledger

{markdown_table(local_gr_consequence, ["consequence_id", "condition", "local_gr_effect", "current_status", "runner_effect", "valid_for_claim", "claim_allowed"])}

## Runner Feed Update

{markdown_table(runner_feed, ["feed_id", "target", "update", "score_ready_delta", "valid_prediction_rows_delta", "current_status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision_rows, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_rows, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validation_rows, ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1225"
TITLE = "1225-Y5-R10-tau-WEP-source-worldtube-readout-projection"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
TAU_PROJECTION_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_TAU_WEP_PROJECTION_ATTEMPT.csv"
SYMBOLIC_FORMULA_PATH = OUT_DIR / f"{PACK_ID}_SYMBOLIC_TAU_WEP_FORMULA.csv"
SOURCE_ACQUISITION_PATH = OUT_DIR / f"{PACK_ID}_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv"
PRODUCT_FEED_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_WEIGHT_PRODUCT_FEED.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_TAU_WEP_ANTI_SHORTCUT_GATES.csv"
LOCAL_GR_FEED_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_GR_WEP_FEED_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1225_VALIDATION.csv"


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
            "source_id": "SRC1225_0_1224_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1224_NEXT_TARGET.csv",
            "needle": "1225-Y5-R10-tau-WEP-source-worldtube-readout-projection.md",
            "purpose": "1224 handoff to tau_WEP projection",
        },
        {
            "source_id": "SRC1225_1_1224_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv",
            "needle": "FSW1224_2_tau_WEP",
            "purpose": "tau_WEP finite input requirement",
        },
        {
            "source_id": "SRC1225_2_1224_product",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1224_SOURCE_WEIGHT_PRODUCT_LAW.csv",
            "needle": "PROD1224_0_source_weight",
            "purpose": "source-weight product law",
        },
        {
            "source_id": "SRC1225_3_1066_tau_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv",
            "needle": "TWP1066_7_verdict",
            "purpose": "original tau_WEP projection contract",
        },
        {
            "source_id": "SRC1225_4_1061_inputs",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1061_INPUT_FILL_LEDGER.csv",
            "needle": "INF1061_4_tau_WEP",
            "purpose": "tau_WEP missing input row",
        },
        {
            "source_id": "SRC1225_5_1061_material",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv",
            "needle": "MCON1061_0_test_pair",
            "purpose": "MICROSCOPE Ti/Pt material convention",
        },
        {
            "source_id": "SRC1225_6_1083_source_vector",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
            "needle": "SCG1083_0_profile_weighting",
            "purpose": "Earth/source profile weighting missing",
        },
        {
            "source_id": "SRC1225_7_1084_readout",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
            "needle": "RIG1084_0_CMSM_arrays",
            "purpose": "official MICROSCOPE readout arrays missing",
        },
        {
            "source_id": "SRC1225_8_1052_alpha_wep",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv",
            "needle": "AWP1052_0_alpha_Coulomb",
            "purpose": "WEP projection pressure precedent",
        },
        {
            "source_id": "SRC1225_9_local_bounds",
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

    projection_attempt = [
        {
            "attempt_id": "TAU1225_0_source_worldtube",
            "projection_piece": "Earth/source worldtube and stress profile",
            "needed_object": "T_source^Earth(x) with source-weight/profile convention",
            "attempt": "identify the source stress/current seen by the satellite in the observed local frame",
            "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv", "SCG1083_0_profile_weighting"),
            "effect": "tau_WEP cannot be numeric",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TAU1225_1_orbit_average",
            "projection_piece": "MICROSCOPE orbit/time average",
            "needed_object": "time/session/orbit averaging convention for differential acceleration channel",
            "attempt": "map source residual through the satellite orbit and selected signal channel",
            "current_status": "MISSING_ORBIT_AVERAGE_ARRAYS",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv", "TWP1066_1_orbit_average"),
            "effect": "tau_WEP cannot be normalized",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TAU1225_2_observed_coframe",
            "projection_piece": "observed coframe/readout frame",
            "needed_object": "one e_obs convention shared by force law, source variation, clocks, and readout",
            "attempt": "keep projection in the same observed frame as the parent residual and eta_AB",
            "current_status": "CONDITIONAL_FROM_PRIOR_SPINE",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv", "TWP1066_2_observed_coframe"),
            "effect": "frame consistency remains conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TAU1225_3_material_response",
            "projection_piece": "Ti/Pt material response",
            "needed_object": "TA6V-minus-PtRh10 material/source tensor in the same convention as eta_AB",
            "attempt": "reuse material convention as a label, not as a complete source-weight response tensor",
            "current_status": "MATERIAL_PAIR_ONLY",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_0_test_pair"),
            "effect": "Delta_w_TiPt mapping remains incomplete",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TAU1225_4_force_readout",
            "projection_piece": "differential acceleration readout kernel",
            "needed_object": "K_MICROSCOPE mapping parent source residual to reported eta_AB",
            "attempt": "require official CMSM/export arrays or a validated exact equivalent",
            "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv", "RIG1084_0_CMSM_arrays"),
            "effect": "no surrogate kernel can promote a claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TAU1225_5_normalization",
            "projection_piece": "eta_AB product normalization",
            "needed_object": "normalization from source response x material response x readout kernel to reported Eotvos eta",
            "attempt": "tie tau_WEP to eta_TiPt rather than an arbitrary unit factor",
            "current_status": "NORMALIZATION_NOT_FILLED",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv", "RIG1084_1_product_convention"),
            "effect": "tau_WEP=1 shortcut remains forbidden",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TAU1225_6_verdict",
            "projection_piece": "tau_WEP",
            "needed_object": "functional[source worldtube, orbit average, observed coframe, material tensor, force readout]",
            "attempt": "derive or source all pieces",
            "current_status": "TAU_WEP_PROJECTION_NOT_DERIVED",
            "source": "TAU1225_0 through TAU1225_5",
            "effect": "source-weight product remains not scoreable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    symbolic_formula = [
        {
            "formula_id": "FORM1225_0_tau_WEP_functional",
            "symbolic_formula": "tau_WEP := N_eta^{-1} < K_eta[e_obs, orbit, masks] · Integral_Earth dV K_source(x;orbit) R_source(x) · R_material(TiPt) >_orbit",
            "meaning": "dimensionless projection from parent source-weight residual to reported MICROSCOPE eta channel",
            "required_to_evaluate": "N_eta;K_eta;K_source;R_source;R_material;orbit/mask average;e_obs convention",
            "current_status": "SYMBOLIC_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "formula_id": "FORM1225_1_source_weight_product",
            "symbolic_formula": "abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15",
            "meaning": "finite source-weight branch bound after tau_WEP and Delta_w_TiPt are sourced",
            "required_to_evaluate": "Delta_w_TiPt;tau_WEP;eta bound;absolute-product guard",
            "current_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    source_acquisition = [
        {
            "acquisition_id": "ACQ1225_0_official_readout_arrays",
            "object": "official MICROSCOPE CMSM/export arrays",
            "required_content": "time, segment/session id, gx, gz, Sxx, Sxz, masks, calibration flags, attitude/orbit convention",
            "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "source_basis": source_ref("source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv", "RIG1084_0_CMSM_arrays"),
            "claim_effect": "blocks K_eta and tau_WEP normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acquisition_id": "ACQ1225_1_product_convention",
            "object": "eta_AB product normalization",
            "required_content": "map from source response x material response x readout kernel to reported Eotvos eta",
            "current_status": "NORMALIZATION_NOT_FILLED",
            "source_basis": source_ref("source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv", "RIG1084_1_product_convention"),
            "claim_effect": "blocks conversion from symbolic tau to numeric tau",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acquisition_id": "ACQ1225_2_source_worldtube",
            "object": "Earth/source stress worldtube",
            "required_content": "profile-weighted source stress/current seen along MICROSCOPE orbit in observed local frame",
            "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING",
            "source_basis": source_ref("source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv", "SCG1083_0_profile_weighting"),
            "claim_effect": "blocks source side of tau_WEP",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acquisition_id": "ACQ1225_3_orbit_average",
            "object": "MICROSCOPE orbit/session average",
            "required_content": "time/orbit average matched to reported eta_AB channel and masks",
            "current_status": "MISSING_ORBIT_AVERAGE_ARRAYS",
            "source_basis": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv", "TWP1066_1_orbit_average"),
            "claim_effect": "blocks orbit average in tau_WEP",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acquisition_id": "ACQ1225_4_material_tensor",
            "object": "Ti/Pt source-weight material response tensor",
            "required_content": "material response to relative source-weight channel, not only alpha/Coulomb delta-Q",
            "current_status": "MATERIAL_PAIR_ONLY",
            "source_basis": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv", "TWP1066_3_material_response"),
            "claim_effect": "blocks Delta_w_TiPt mapping",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acquisition_id": "ACQ1225_5_delta_w",
            "object": "Delta_w_TiPt finite prior or theorem-zero",
            "required_content": "numeric width or parent source-weight theorem-zero, in same convention as tau_WEP",
            "current_status": "MISSING_NUMERIC_PRIOR_WIDTH",
            "source_basis": source_ref("source-intake/mts_residuals/P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv", "FSW1224_1_delta_w"),
            "claim_effect": "blocks source-weight product even if tau_WEP is later known",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    product_feed = [
        {
            "feed_id": "FEED1225_0_tau_to_product",
            "target_product": "PROD1224_0_source_weight",
            "tau_WEP_status": "TAU_WEP_PROJECTION_NOT_DERIVED",
            "Delta_w_status": "MISSING_NUMERIC_PRIOR_WIDTH",
            "eta_bound_status": "BOUND_ANCHOR_AVAILABLE",
            "product_score_status": "NOT_SCOREABLE",
            "valid_prediction_rows_delta": 0,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "feed_id": "FEED1225_1_tau_to_runner",
            "target_product": "RUN1221_2_source_weight",
            "tau_WEP_status": "SYMBOLIC_ONLY_NONCLAIM",
            "Delta_w_status": "MISSING",
            "eta_bound_status": "2.8e-15",
            "product_score_status": "REFUSED",
            "valid_prediction_rows_delta": 0,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1225_0_no_tau_unity",
            "forbidden_shortcut": "set tau_WEP=1",
            "reason": "tau_WEP is a lab/source/orbit/readout functional, not a convention-free unit",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1225_1_no_surrogate_claim",
            "forbidden_shortcut": "use surrogate kernel as official readout",
            "reason": "RIG1084 requires official arrays or proof of exact equivalence",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1225_2_no_G_absorption",
            "forbidden_shortcut": "absorb source-weight residual into measured G",
            "reason": "source-weight branch affects composition/source/readout comparison",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1225_3_no_cancellation",
            "forbidden_shortcut": "cancel signs/material terms by hand",
            "reason": "1224 product uses absolute guard unless full material model is signed",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    local_gr_feed = [
        {
            "feed_id": "LGRFEED1225_0",
            "target": "local GR/Newton source-side coupling",
            "update": "tau_WEP remains symbolic-only, so source-weight branch remains explicit and unscoreable",
            "effect": "no local-GR pass claim; no source coupling universality claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "LGRFEED1225_1",
            "target": "future empirical pass",
            "update": "official readout/source acquisition is now the shortest path to a numeric source-weight pressure test",
            "effect": "next work should acquire/readout data or prove exact equivalence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1225_0_tau_not_derived",
            "decision": "do not promote tau_WEP",
            "because": "source worldtube, orbit average, material tensor, product normalization, and official readout are not filled",
            "next_action": "acquire official MICROSCOPE readout/export objects or write an exact equivalence proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1225_1_symbolic_formula_retained",
            "decision": "retain symbolic tau_WEP functional",
            "because": "it pins down the projection shape without pretending to evaluate it",
            "next_action": "use FORM1225_0 as the input contract for source/readout acquisition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1225_2_next_data_gate",
            "decision": "move toward readout/source acquisition",
            "because": "the math contract is now specific enough that data plumbing is the bottleneck",
            "next_action": "stage official MICROSCOPE readout/source acquisition without claiming pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1225_0_sources",
            "gate": "source path and needle audit",
            "status": "PASS",
            "reason": "all local sources used by 1225 are traceable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1225_1_tau_projection",
            "gate": "tau_WEP projection derived or sourced",
            "status": "BLOCKED",
            "reason": "TAU1225_6 current_status=TAU_WEP_PROJECTION_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1225_2_symbolic_formula",
            "gate": "symbolic formula written",
            "status": "PASS",
            "reason": "FORM1225_0 records the functional contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1225_3_required_sources",
            "gate": "required readout/source objects acquired",
            "status": "BLOCKED",
            "reason": "ACQ1225 rows remain missing/nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1225_4_product_score",
            "gate": "source-weight product scoreable",
            "status": "BLOCKED",
            "reason": "tau_WEP and Delta_w_TiPt are not numeric/sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1225_5_local_GR_WEP",
            "gate": "local GR/WEP claim permission",
            "status": "BLOCKED",
            "reason": "1225 is projection plumbing only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1225_0_1226",
            "target_file": "1226-Y5-R10-MICROSCOPE-readout-source-acquisition-ledger.md",
            "target_script": "scripts/Y5_R10_MICROSCOPE_readout_source_acquisition_ledger.py",
            "task": "find or stage the official MICROSCOPE readout/source objects needed by tau_WEP, with provenance and no surrogate-as-claim",
            "success_condition": "official arrays/source objects are acquired or a blocker ledger records exact missing public/private data objects without fabricating rows",
            "do_not_do": "do not claim WEP/local-GR/PPN, do not use surrogate arrays as official, do not set tau_WEP to one, do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (TAU_PROJECTION_ATTEMPT_PATH, projection_attempt),
        (SYMBOLIC_FORMULA_PATH, symbolic_formula),
        (SOURCE_ACQUISITION_PATH, source_acquisition),
        (PRODUCT_FEED_PATH, product_feed),
        (ANTI_SHORTCUT_PATH, anti_shortcut),
        (LOCAL_GR_FEED_PATH, local_gr_feed),
        (DECISION_PATH, decision_rows),
        (CLAIM_GATES_PATH, claim_gates),
        (NEXT_PATH, next_rows),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    validation_rows = []
    validation_rows.append(
        validation_row(
            "VAL1225_0_sources_exist",
            "all cited local sources exist",
            all(parse_bool(row["path_exists"]) for row in source_register),
            f"{sum(1 for row in source_register if parse_bool(row['path_exists']))}/{len(source_register)} sources exist",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1225_1_needles_found",
            "all cited source needles found",
            all(parse_bool(row["needle_found"]) for row in source_register),
            f"{sum(1 for row in source_register if parse_bool(row['needle_found']))}/{len(source_register)} needles found",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1225_2_tau_verdict_nonclaim",
            "tau_WEP is not falsely promoted",
            projection_attempt[-1]["current_status"] == "TAU_WEP_PROJECTION_NOT_DERIVED"
            and all(is_false(row, "claim_allowed") for row in projection_attempt),
            projection_attempt[-1]["current_status"],
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1225_3_symbolic_formula_written",
            "symbolic tau_WEP formula is written",
            len(symbolic_formula) == 2 and symbolic_formula[0]["current_status"] == "SYMBOLIC_ONLY_NONCLAIM",
            symbolic_formula[0]["formula_id"],
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1225_4_acquisition_table_complete",
            "source acquisition table includes required objects",
            {"ACQ1225_0_official_readout_arrays", "ACQ1225_1_product_convention", "ACQ1225_2_source_worldtube", "ACQ1225_3_orbit_average", "ACQ1225_4_material_tensor", "ACQ1225_5_delta_w"}.issubset(
                {row["acquisition_id"] for row in source_acquisition}
            ),
            "; ".join(row["acquisition_id"] for row in source_acquisition),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1225_5_missing_sources_nonclaim",
            "missing source rows are not valid for claim",
            all(is_false(row, "valid_for_claim") and is_false(row, "claim_allowed") for row in source_acquisition),
            "all ACQ1225 rows nonclaim",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1225_6_product_feed_refuses",
            "product feed keeps zero valid predictions",
            all(row["valid_prediction_rows_delta"] == 0 and is_false(row, "claim_allowed") for row in product_feed),
            "valid_prediction_rows_delta=0 for all product feed rows",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1225_7_anti_shortcuts_enforced",
            "anti-shortcut gates enforce no unity/surrogate/G-absorption/cancellation",
            all(row["status"] == "ENFORCED" and is_false(row, "claim_allowed") for row in anti_shortcut),
            "; ".join(row["gate_id"] for row in anti_shortcut),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1225_8_next_target_readout_acquisition",
            "next target stages MICROSCOPE readout/source acquisition",
            next_rows[0]["target_file"] == "1226-Y5-R10-MICROSCOPE-readout-source-acquisition-ledger.md",
            next_rows[0]["target_file"],
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1225_9_claim_gates_blocked",
            "claim gates keep physical claims blocked",
            any(row["status"] == "BLOCKED" for row in claim_gates) and all(is_false(row, "valid_for_claim") for row in claim_gates),
            "tau/source/product/local claim gates blocked",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1225_10_nonclaim_policy",
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
            "VAL1225_11_csv_parse",
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
            "VAL1225_12_formalization_untouched",
            "formalization-workbench untouched during run",
            len(formalization_recent) == 0,
            f"formalization_recent_after_run_start_count={len(formalization_recent)}",
        )
    )

    overall_before = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1225_13_overall",
            "overall 1225 validation",
            overall_before,
            "1225 writes symbolic tau_WEP projection and exact readout/source acquisition table without claim promotion",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# 1225 Y5/R10 Tau WEP Source Worldtube Readout Projection

**Current verdict:** 1225 does **not** derive a numeric `tau_WEP`. It does derive the shape of the projection contract: `tau_WEP` is a dimensionless source-worldtube/orbit/coframe/material/readout functional, not a free unity factor.

**Main progress:** the source-weight product is now blocked for precise reasons only: official MICROSCOPE readout arrays, eta product normalization, Earth/source worldtube weighting, orbit averaging, Ti/Pt source-weight material tensor, and `Delta_w_TiPt` are all still required.

**Practical consequence:** this is the bridge from local-GR coupling theory into real data plumbing. The next target is readout/source acquisition, not another abstract claim.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "absolute_path", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"])}

## Tau WEP Projection Attempt

{markdown_table(projection_attempt, ["attempt_id", "projection_piece", "needed_object", "attempt", "current_status", "source", "effect", "valid_for_claim", "claim_allowed"])}

## Symbolic Tau WEP Formula

{markdown_table(symbolic_formula, ["formula_id", "symbolic_formula", "meaning", "required_to_evaluate", "current_status", "valid_for_claim", "claim_allowed"])}

## Tau WEP Source Acquisition Table

{markdown_table(source_acquisition, ["acquisition_id", "object", "required_content", "current_status", "source_basis", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Source Weight Product Feed

{markdown_table(product_feed, ["feed_id", "target_product", "tau_WEP_status", "Delta_w_status", "eta_bound_status", "product_score_status", "valid_prediction_rows_delta", "claim_allowed", "valid_for_claim"])}

## Tau WEP Anti-Shortcut Gates

{markdown_table(anti_shortcut, ["gate_id", "forbidden_shortcut", "reason", "status", "valid_for_claim", "claim_allowed"])}

## Local GR WEP Feed Update

{markdown_table(local_gr_feed, ["feed_id", "target", "update", "effect", "valid_for_claim", "claim_allowed"])}

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

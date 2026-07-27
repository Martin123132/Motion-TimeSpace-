from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_TAU_PPN_OR_COMMON_FRAME_SIGNATURE_2322"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2322-Y5-R2FR-tau-PPN-or-common-frame-parent-signature.md"

PATHS = {
    "2321_doc": ROOT / "2321-Y5-R2FR-alpha-cg-projection-owner-fill-or-deltaw-material-vector-acquisition.md",
    "2321_validation": OUT / "P8_Y5_BRR545_2321_VALIDATION.csv",
    "2321_conditional": OUT / "P8_Y5_PARENT_QLOC_2321_CONDITIONAL_FILL_ROWS.csv",
    "2321_blockers": OUT / "P8_Y5_PARENT_QLOC_2321_ALPHA_CG_PROJECTION_BLOCKER_AUDIT.csv",
    "2160_scalar": OUT / "P8_Y5_PARENT_QLOC_2160_SCALAR_TENSOR_PPN_MAP.csv",
    "2160_vector": OUT / "P8_Y5_PARENT_QLOC_2160_PPN_RESIDUAL_VECTOR_ENVELOPE.csv",
    "2160_claims": OUT / "P8_Y5_PARENT_QLOC_2160_CLAIM_GATE.csv",
    "2104_projection": OUT / "P8_Y5_PARENT_QLOC_2104_CG_PPN_PROJECTION.csv",
    "2104_frame": OUT / "P8_Y5_PARENT_QLOC_2104_FRAME_DEGENERACY_CONDITIONS.csv",
    "2105_norm": OUT / "P8_Y5_PARENT_QLOC_2105_NORMALIZATION_CONTRACT.csv",
    "2105_runner": OUT / "P8_Y5_PARENT_QLOC_2105_GAMMA_RUNNER.csv",
    "2159_moms": OUT / "P8_Y5_PARENT_QLOC_2159_MOMS_SIGNATURE_ATTEMPT.csv",
    "2159_translation": OUT / "P8_Y5_PARENT_QLOC_2159_CG_PPN_TRANSLATION_GATE.csv",
    "2159_claims": OUT / "P8_Y5_PARENT_QLOC_2159_LOCAL_CLAIM_GATE.csv",
    "2318_functor": OUT / "P8_Y5_PARENT_QLOC_2318_PARENT_COEFFICIENT_FUNCTOR_CONSTRUCTION_ATTEMPT.csv",
    "2318_obligations": OUT / "P8_Y5_PARENT_QLOC_2318_FUNCTOR_PROOF_OBLIGATION_LEDGER.csv",
    "2202_effective": OUT / "P8_Y5_PARENT_QLOC_2202_ALPHA_CG_EFFECTIVE_ROW.csv",
    "2203_readout": OUT / "P8_Y5_PARENT_QLOC_2203_ALPHA_READOUT_ROW.csv",
    "2203_gm": OUT / "P8_Y5_PARENT_QLOC_2203_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
    "2208_blockers": OUT / "P8_Y5_PARENT_QLOC_2208_PPN_BLOCKER_LEDGER.csv",
    "2208_green": OUT / "P8_Y5_PARENT_QLOC_2208_PPN_GREEN_OPERATOR_LOWERING.csv",
    "2210_range": OUT / "P8_Y5_PARENT_QLOC_2210_RANGE_OPERATOR_DERIVATION.csv",
}

SOURCES = [
    ("SRC2322_00_2321_doc", "2321_doc", PATHS["2321_doc"], ["NEXT2321_0", "tau-PPN-or-common-frame"], "2321 handoff"),
    ("SRC2322_01_2321_validation", "2321_validation", PATHS["2321_validation"], ["VAL2321_OVERALL", "PASS"], "2321 validation"),
    ("SRC2322_02_2321_conditional", "2321_conditional", PATHS["2321_conditional"], ["CF2321_2_alpha_cg_normal_form", "tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X)"], "alpha_cg normal form"),
    ("SRC2322_03_2321_blockers", "2321_blockers", PATHS["2321_blockers"], ["ACG2321_4_tau_PPN", "MISSING_TAU_PPN"], "tau blocker"),
    ("SRC2322_04_2160_scalar", "2160_scalar", PATHS["2160_scalar"], ["STM2160_0_common_frame_ansatz", "STM2160_2_effective_ppn_charge"], "scalar-tensor PPN map"),
    ("SRC2322_05_2160_vector", "2160_vector", PATHS["2160_vector"], ["PPV2160_0_cg", "MISSING_ZX_TAU_RANGE"], "PPN vector envelope"),
    ("SRC2322_06_2160_claims", "2160_claims", PATHS["2160_claims"], ["CG2160_6_local_GR_PPN", "False"], "2160 claim gates"),
    ("SRC2322_07_2104_projection", "2104_projection", PATHS["2104_projection"], ["PRJ2104_1_common_conformal_branch", "standard scalar-tensor weak-field projection template"], "c_g to PPN projection"),
    ("SRC2322_08_2104_frame", "2104_frame", PATHS["2104_frame"], ["FDG2104_5_verdict", "NO_FREE_DEGENERACY_CLAIM"], "frame degeneracy guard"),
    ("SRC2322_09_2105_norm", "2105_norm", PATHS["2105_norm"], ["NC2105_0_raw_to_canonical", "alpha_eff = N_X c_g"], "normalization contract"),
    ("SRC2322_10_2105_runner", "2105_runner", PATHS["2105_runner"], ["RUN2105_VERDICT", "REFUSES_SCORE"], "gamma runner refusal"),
    ("SRC2322_11_2159_moms", "2159_moms", PATHS["2159_moms"], ["MOM2159_7_verdict", "FAIL_CURRENT_CLAIM"], "ordinary matter signature attempt"),
    ("SRC2322_12_2159_translation", "2159_translation", PATHS["2159_translation"], ["CGT2159_0_universal_common_frame", "NOT_PARENT_SIGNED"], "translation gate"),
    ("SRC2322_13_2159_claims", "2159_claims", PATHS["2159_claims"], ["LCG2159_5_local_GR_Newton", "False"], "local claim gates"),
    ("SRC2322_14_2318_functor", "2318_functor", PATHS["2318_functor"], ["PCF2318_5_verdict", "PARENT_COEFFICIENT_FUNCTOR_NOT_CONSTRUCTED"], "coefficient functor"),
    ("SRC2322_15_2318_obligations", "2318_obligations", PATHS["2318_obligations"], ["OBL2318_4_readout_closure", "RADIATIVE_READOUT_CLOSURE_UNSIGNED"], "functor obligations"),
    ("SRC2322_16_2202_effective", "2202_effective", PATHS["2202_effective"], ["AER2202_0_effective_target", "tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X)"], "effective alpha row"),
    ("SRC2322_17_2203_readout", "2203_readout", PATHS["2203_readout"], ["ARW2203_0_alpha_readout", "MISSING_FIXED_READOUT_FUNCTOR"], "readout component"),
    ("SRC2322_18_2203_gm", "2203_gm", PATHS["2203_gm"], ["MGV2203_7_calibration_PPN_tail", "MISSING_GAUSS_ORBITAL_PPN_RESIDUAL"], "measured GM obstruction"),
    ("SRC2322_19_2208_blockers", "2208_blockers", PATHS["2208_blockers"], ["PPNB2208_3_PPN_gauge", "MISSING_PPN_GAUGE_TRANSFORM"], "PPN blocker ledger"),
    ("SRC2322_20_2208_green", "2208_green", PATHS["2208_green"], ["PPNL2208_3_source_normalization", "SOURCE_NORMALIZATION_BLOCKER_CONNECTED"], "PPN Green lowering"),
    ("SRC2322_21_2210_range", "2210_range", PATHS["2210_range"], ["ROD2210_5_verdict", "RANGE_OWNER_LAW_DERIVED_VALUES_BLOCKED"], "range owner law"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2322_SOURCE_REGISTER.csv",
    "tau_audit": OUT / "P8_Y5_PARENT_QLOC_2322_TAU_PPN_COMMON_FRAME_DERIVATION_AUDIT.csv",
    "conditional_tau": OUT / "P8_Y5_PARENT_QLOC_2322_CONDITIONAL_TAU_NORMALIZATION_ROWS.csv",
    "signature": OUT / "P8_Y5_PARENT_QLOC_2322_PARENT_SIGNATURE_CLAUSE_LEDGER.csv",
    "score_update": OUT / "P8_Y5_PARENT_QLOC_2322_SCORE_OBJECT_UPDATE.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2322_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2322_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2322_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2322_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2322_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2322_0_tau_audit", OUTPUTS["tau_audit"], BETA_DOCS / "TAU_PPN_COMMON_FRAME_DERIVATION_AUDIT_2322_NONCLAIM.csv"),
    ("COPY2322_1_conditional_tau", OUTPUTS["conditional_tau"], RAB_QUEUE / "JR2322_CONDITIONAL_TAU_NORMALIZATION_NONCLAIM.csv"),
    ("COPY2322_2_signature", OUTPUTS["signature"], RAB_QUEUE / "JR2322_PARENT_SIGNATURE_CLAUSE_LEDGER_NONCLAIM.csv"),
    ("COPY2322_3_score_update", OUTPUTS["score_update"], MICRO_RESIDUALS / "alpha_cg_score_object_update_nonclaim_2322.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
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
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "missing_needles=" + ";".join(missing)
    return True, "all_needles_found"


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, key, path, needles, role in SOURCES:
        found, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needles": ";".join(needles),
                "needles_found": bool_text(found),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def build_tau_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "TPA2322_0_common_frame_premise",
            "target": "universal common matter frame",
            "attempted_statement": "S_matter uses one metric g_m=A_g(Xhat)^2 g_E for ordinary matter, rods, clocks, source masses, and Cassini/Shapiro readout",
            "result": "CONDITIONAL_PREMISE_ONLY",
            "why": "2160/2104 write the scalar-tensor ansatz; 2159 says parent ordinary-matter signature is not derived",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TPA2322_1_tau_standard_scalar_tensor",
            "target": "tau_PPN normalization",
            "attempted_statement": "in the standard massless unscreened scalar-tensor branch, the PPN gamma law reads gamma-1=-2 alpha_eff^2/(1+alpha_eff^2), so tau_PPN=1 by definition of alpha_eff",
            "result": "EXACT_CONDITIONAL_TAU_EQUALS_ONE",
            "why": "tau is not an extra fitted factor once the common-frame scalar-tensor PPN branch is parent-signed",
            "blocks_score": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TPA2322_2_tau_not_screening",
            "target": "separate tau_PPN from S_PPN",
            "attempted_statement": "tau_PPN is the readout/projection normalization; finite range and screening belong in S_PPN(lambda_X,env)",
            "result": "DECOMPOSITION_LOCKED",
            "why": "2210 owns the range law conditionally; screening/profile response remains a separate missing input",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TPA2322_3_readout_gauge_tail",
            "target": "observed PPN readout",
            "attempted_statement": "fixed-before-readout, measured-GM, and PPN-gauge maps must not add alpha_readout or calibration tails",
            "result": "NOT_DERIVED",
            "why": "2203 and 2208 retain readout, measured-GM, source-normalization, and PPN-gauge blockers",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TPA2322_4_verdict",
            "target": "active-branch tau_PPN",
            "attempted_statement": "set tau_PPN=1 in active MTS scoring",
            "result": "NOT_ALLOWED_YET",
            "why": "the equality is exact only inside the parent-signed common-frame scalar-tensor branch; active branch still lacks the parent signature and tail zeroes",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
    ]


def build_conditional_tau_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CTN2322_0_canonical_alpha",
            "conditional_branch": "universal common-frame scalar-tensor",
            "formula": "alpha_eff=N_X*c_g=c_g/sqrt(Z_X)",
            "tau_value": "tau_PPN=1",
            "requires": "parent-signed common matter frame; canonical Xhat block; no disformal/species/readout tails",
            "status": "EXACT_CONDITIONAL_NORMALIZATION",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CTN2322_1_gamma_law",
            "conditional_branch": "massless/solar-long unscreened scalar-tensor",
            "formula": "gamma-1=-2*alpha_eff^2/(1+alpha_eff^2)",
            "tau_value": "no additional tau factor",
            "requires": "S_PPN=1 and alpha_vec_tail=0",
            "status": "STANDARD_CONDITIONAL_RELATION_IMPORTED",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CTN2322_2_active_normal_form",
            "conditional_branch": "current active MTS branch",
            "formula": "alpha_cg^PPN=tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X)",
            "tau_value": "tau_PPN symbolic",
            "requires": "parent matter-frame signature or separate source-backed tau_PPN",
            "status": "ACTIVE_SCORE_OBJECT_REMAINS_SYMBOLIC",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2322_0_parent_action_object",
            "signature_clause": "one parent ordinary-matter action before readout",
            "required_statement": "S_parent selects S_matter once, before projection, fitting, and detector calibration",
            "current_status": "SCHEMA_AVAILABLE_NOT_DERIVED",
            "source_basis": "MOM2159_0_action_object;OBL2318_0_parent_object",
            "blocks_tau_one": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2322_1_universal_metric",
            "signature_clause": "one ordinary matter metric",
            "required_statement": "all ordinary matter sees g_m=A_g(Xhat)^2 g_E with no independent disformal/species/shadow metric",
            "current_status": "NOT_PARENT_SIGNED",
            "source_basis": "CGT2159_0_universal_common_frame;STM2160_0_common_frame_ansatz",
            "blocks_tau_one": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2322_2_coeff_functor",
            "signature_clause": "no hidden-visible coefficient hom",
            "required_statement": "visible coefficients descend through quotient/fixed representation data only",
            "current_status": "PARENT_COEFFICIENT_FUNCTOR_NOT_CONSTRUCTED",
            "source_basis": "PCF2318_5_verdict;OBL2318_5_verdict",
            "blocks_tau_one": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2322_3_fixed_before_readout",
            "signature_clause": "variation before readout",
            "required_statement": "readout maps, detector thresholds, source worldtubes, and measured-GM calibration do not regenerate a PPN tail",
            "current_status": "RADIATIVE_READOUT_CLOSURE_UNSIGNED",
            "source_basis": "OBL2318_4_readout_closure;ARW2203_0_alpha_readout;MGV2203_7_calibration_PPN_tail",
            "blocks_tau_one": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2322_4_ppn_gauge_source",
            "signature_clause": "observed PPN gauge and source normalization",
            "required_statement": "weak-field metric is transformed to the observed PPN gauge with fixed G_ref/source mass and no absorbed tail",
            "current_status": "MISSING_PPN_GAUGE_TRANSFORM_AND_SOURCE_NORMALIZATION",
            "source_basis": "PPNB2208_2_source_normalization;PPNB2208_3_PPN_gauge;PPNL2208_3_source_normalization",
            "blocks_tau_one": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2322_5_verdict",
            "signature_clause": "common-frame parent signature closes",
            "required_statement": "SIG2322_0 through SIG2322_4 pass together",
            "current_status": "COMMON_FRAME_SIGNATURE_NOT_DERIVED",
            "source_basis": "2322 synthesis",
            "blocks_tau_one": "true",
            "valid_for_claim": "false",
        },
    ]


def build_score_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SOU2322_0_allowed_conditional_score_object",
            "score_object": "alpha_cg^PPN",
            "formula": "tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X)",
            "update": "tau_PPN can be replaced by 1 only inside the parent-signed standard common-frame scalar-tensor branch",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SOU2322_1_forbidden_shortcut",
            "score_object": "tau_PPN=1 by convention in active branch",
            "formula": "not allowed",
            "update": "would smuggle the common-frame/readout theorem as notation",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SOU2322_2_local_GR_status",
            "score_object": "local GR/Newton recovery",
            "formula": "requires full absolute PPN residual vector theorem-zero or source-bounded",
            "update": "2322 reduces one ambiguity but does not score the vector",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2322_0_sources",
            "gate": "source paths and needles valid",
            "passed": "true",
            "claim_effect": "audit reproducible",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2322_1_conditional_tau",
            "gate": "tau_PPN=1 derived in strict scalar-tensor common-frame branch",
            "passed": "true",
            "claim_effect": "conditional theorem only; not active score",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2322_2_common_frame_signature",
            "gate": "common-frame parent signature signed",
            "passed": "false",
            "claim_effect": "tau_PPN cannot be set to 1 in active branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2322_3_readout_tail_zero",
            "gate": "readout/gauge/source-normalization tails theorem-zero",
            "passed": "false",
            "claim_effect": "alpha_readout and calibration tails remain in PPN vector",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2322_4_alpha_score",
            "gate": "alpha_cg score-ready",
            "passed": "false",
            "claim_effect": "Z_X, range/S_PPN, common frame, and tails remain missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2322_5_local_GR_Newton",
            "gate": "local GR/Newton recovery derived",
            "passed": "false",
            "claim_effect": "still a target, not a result",
            "valid_for_claim": "false",
        },
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2322_0_tau_one_active",
            "claim": "set tau_PPN=1 in the active MTS branch",
            "allowed": "false",
            "reason": "tau_PPN=1 is exact only after the common-frame scalar-tensor parent signature and readout/gauge clauses are signed",
            "blocking_rows": "SIG2322_0 through SIG2322_5",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2322_1_set_SPPN_one",
            "claim": "set S_PPN=1 by convention",
            "allowed": "false",
            "reason": "range/screening/profile response is separate from tau_PPN and still depends on parent Z/M/domain/source data",
            "blocking_rows": "TPA2322_2_tau_not_screening;ROD2210_5_verdict",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2322_2_drop_readout_tail",
            "claim": "drop alpha_readout and measured-GM calibration tails",
            "allowed": "false",
            "reason": "2203/2208 keep readout, source-normalization, and PPN gauge as explicit blockers",
            "blocking_rows": "SIG2322_3_fixed_before_readout;SIG2322_4_ppn_gauge_source",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2322_3_local_GR",
            "claim": "2322 derives local GR/Newton",
            "allowed": "false",
            "reason": "2322 proves a conditional normalization rule, not the full residual-vector theorem",
            "blocking_rows": "CG2322_5_local_GR_Newton;SOU2322_2_local_GR_status",
            "valid_for_claim": "false",
        },
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2322_0",
            "next_target": "2323-Y5-R2FR-common-matter-frame-action-signature-or-readout-tail-row.md",
            "why": "2322 shows tau_PPN=1 is not a free coefficient in the strict common-frame branch; the remaining hard target is proving the parent matter-frame/readout signature or keeping alpha_readout as an explicit PPN component.",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2322_1",
            "next_target": "2323b-Y5-R2FR-PPN-gauge-source-normalization-tail-bound.md",
            "why": "fallback if the common-frame theorem stalls; bound the gauge/source-normalization/readout tail rather than dropping it.",
            "claim_status": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dest in BRANCH_COPY_SPECS:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": relative_path(src),
                "branch_copy_path": str(dest),
                "copy_exists": bool_text(dest.exists()),
                "row_count": str(len(read_csv_rows(dest))),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation_rows(source_rows: list[dict[str, Any]], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths += [Path(row["branch_copy_path"]) for row in branch_copy_rows]
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": "false",
            }
        )

    add("VAL2322_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists")
    add("VAL2322_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found")
    tau_rows = read_csv_rows(OUTPUTS["conditional_tau"])
    add("VAL2322_02_conditional_tau_one", any(row.get("row_id") == "CTN2322_0_canonical_alpha" and row.get("tau_value") == "tau_PPN=1" for row in tau_rows), "strict common-frame tau_PPN=1 conditional row exists")
    signature_rows = read_csv_rows(OUTPUTS["signature"])
    add("VAL2322_03_signature_blocks_tau", any(row.get("row_id") == "SIG2322_5_verdict" and row.get("current_status") == "COMMON_FRAME_SIGNATURE_NOT_DERIVED" for row in signature_rows), "common-frame parent signature remains unsigned")
    score_rows = read_csv_rows(OUTPUTS["score_update"])
    add("VAL2322_04_score_objects_nonready", all(row.get("score_ready") == "false" for row in score_rows), "score object updates remain non-score-ready")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2322_05_claim_gates_block", any(row.get("row_id") == "CG2322_5_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim remains blocked")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2322_06_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks premature tau/local-GR claims")
    add("VAL2322_07_next_target", len(read_csv_rows(OUTPUTS["next"])) >= 1, "next target selected")
    add("VAL2322_08_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")
    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2322_09_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        checkpoint_patterns = ("*P8_Y5*2322*.csv", "*2322-Y5*.md", "*TAU_PPN_COMMON_FRAME*2322*", "*MTS_R2FR_TAU_PPN_OR_COMMON_FRAME_SIGNATURE_2322*")
        for pattern in checkpoint_patterns:
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2322_10_formalization_untouched_by_2322", not formalization_hits, "no 2322 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2322_OVERALL", all(row["status"] == "PASS" for row in rows), "2322 derives tau_PPN=1 only as a strict common-frame scalar-tensor conditional, keeps active-branch tau symbolic, preserves readout/source/gauge blockers, and blocks local-GR/Newton claims.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    tau_audit_rows: list[dict[str, Any]],
    conditional_tau_rows: list[dict[str, Any]],
    signature_rows: list[dict[str, Any]],
    score_update_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2322 - tau_PPN Or Common Frame Parent Signature

## Summary

2322 closes a small but important loophole. In the strict universal common-frame scalar-tensor branch,
`tau_PPN` is not an extra fit knob: once ordinary matter sees one metric
`g_m=A_g(Xhat)^2 g_E`, the canonical coupling is `alpha_eff=c_g/sqrt(Z_X)` and the standard PPN gamma law uses that
coupling directly. In that branch, `tau_PPN=1` by normalization.

But that is conditional only. The active MTS branch still cannot set `tau_PPN=1`, because the parent common-frame
matter action, coefficient functor, readout closure, measured-GM/source normalization, and PPN gauge transform are
not signed. So the current score object stays
`alpha_cg^PPN=tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X)` unless the common-frame signature is proved.

This is progress, chume: not fireworks, but a cleaner blade. We now know exactly what theorem would let `tau_PPN`
collapse to `1`, and exactly why we are not allowed to use it yet.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## tau_PPN/Common-Frame Derivation Audit

{markdown_table(tau_audit_rows, ["row_id", "target", "attempted_statement", "result", "why", "blocks_score", "valid_for_claim"])}

## Conditional tau Normalization Rows

{markdown_table(conditional_tau_rows, ["row_id", "conditional_branch", "formula", "tau_value", "requires", "status", "score_ready", "valid_for_claim"])}

## Parent Signature Clause Ledger

{markdown_table(signature_rows, ["row_id", "signature_clause", "required_statement", "current_status", "source_basis", "blocks_tau_one", "valid_for_claim"])}

## Score Object Update

{markdown_table(score_update_rows, ["row_id", "score_object", "formula", "update", "score_ready", "valid_for_claim"])}

## Claim Gates

{markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"])}

## Branch Copies

{markdown_table(branch_copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_output = {
        "sources": build_sources(),
        "tau_audit": build_tau_audit_rows(),
        "conditional_tau": build_conditional_tau_rows(),
        "signature": build_signature_rows(),
        "score_update": build_score_update_rows(),
        "claims": build_claim_rows(),
        "refusal": build_refusal_rows(),
        "next": build_next_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(OUTPUTS[key], rows)
    branch_copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], branch_copy_rows)
    validation_rows = build_validation_rows(rows_by_output["sources"], branch_copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_doc(
        rows_by_output["sources"],
        rows_by_output["tau_audit"],
        rows_by_output["conditional_tau"],
        rows_by_output["signature"],
        rows_by_output["score_update"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2322 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

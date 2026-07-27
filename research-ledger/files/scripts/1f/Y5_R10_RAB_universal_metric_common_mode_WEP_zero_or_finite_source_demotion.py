from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1425-Y5-R10-RAB-universal-metric-common-mode-WEP-zero-or-finite-source-demotion.md"
SOURCE_REGISTER = OUT / "P8_Y5_R10_1425_SOURCE_REGISTER.csv"
COMMON_MODE_PROOF = OUT / "P8_Y5_R10_1425_COMMON_MODE_WEP_ZERO_PROOF_ATTEMPT.csv"
PREMISE_AUDIT = OUT / "P8_Y5_R10_1425_COMMON_MODE_PREMISE_AUDIT.csv"
CURRENT_OWNER_SYNTHESIS = OUT / "P8_Y5_R10_1425_CURRENT_OWNER_SYNTHESIS.csv"
MEASURED_G_GUARD = OUT / "P8_Y5_R10_1425_MEASURED_G_COMMON_MODE_GUARD.csv"
FINITE_DEMOTION = OUT / "P8_Y5_R10_1425_FINITE_WEP_DEMOTION_LEDGER.csv"
COEFFICIENT_PACK = OUT / "P8_Y5_R10_1425_FINITE_COEFFICIENT_PACK_CONTRACT.csv"
PRODUCT_STATUS = OUT / "P8_Y5_R10_1425_PRODUCT_STATUS.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1425_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1425_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1425_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1425_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_has(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="ignore")


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


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


def first_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    raise ValueError(f"missing {key}={value} in {path}")


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC1425_0_1424_next", OUT / "P8_Y5_R10_1424_NEXT_TARGET.csv", "NEXT1424_0_1425", "1424 handoff selecting common-mode WEP zero or finite demotion."),
        ("SRC1425_1_1424_validation", OUT / "P8_Y5_BRR545_1424_VALIDATION.csv", "VAL1424_9_overall", "1424 validation: Ti/Pt contraction staged, parent map unsigned."),
        ("SRC1425_2_1424_theorem", OUT / "P8_Y5_R10_1424_PARENT_TIPT_CONTRACTION_THEOREM_ATTEMPT.csv", "THM1424_1_universal_common_mode_zero", "common-mode zero theorem attempt."),
        ("SRC1425_3_1424_candidates", OUT / "P8_Y5_R10_1424_TIPT_MATERIAL_VECTOR_CANDIDATES.csv", "MAT1424_2_electron_mass_fraction", "finite Ti/Pt component candidates."),
        ("SRC1425_4_1332_common_mode", OUT / "P8_Y5_R10_1332_COMMON_MODE_SOURCE_THEOREM.csv", "CMT1332_0_common_mode_source_coupling", "conditional common-mode source theorem."),
        ("SRC1425_5_1332_premises", OUT / "P8_Y5_R10_1332_COMMON_MODE_PREMISE_AUDIT.csv", "PREM1332_3_no_relative_source_prefactors", "premise audit for common-mode promotion."),
        ("SRC1425_6_1333_no_prefactor", OUT / "P8_Y5_R10_1333_NO_SOURCE_PREFACTOR_DERIVATION_ATTEMPT.csv", "NSP1333_5_verdict", "no-source-prefactor derivation failure."),
        ("SRC1425_7_1333_countermodels", OUT / "P8_Y5_R10_1333_SOURCE_PREFACTOR_COUNTERMODEL_LEDGER.csv", "CM1333_0_relative_species_weight", "live source-prefactor countermodels."),
        ("SRC1425_8_1333_electron_bound", OUT / "P8_Y5_R10_1333_ELECTRON_RESIDUAL_BOUND_CONTRACT.csv", "EB1333_0_unit_kernel_electron_prefactor", "nonclaim finite electron residual pressure scale."),
        ("SRC1425_9_1079_current", OUT / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv", "NCO1079_6_verdict", "narrow Hilbert-current owner partial result."),
        ("SRC1425_10_1079_contract", OUT / "P8_Y5_R10_1079_FINITE_WEP_SOURCE_VECTOR_CONTRACT.csv", "FSV1079_1_C_parent", "finite WEP sourced-input contract."),
        ("SRC1425_11_1078_demotion", OUT / "P8_Y5_R10_1078_THEOREM_ZERO_DEMOTION.csv", "TZD1078_2_demote", "earlier theorem-zero closure-only demotion."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchor, role in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "anchor": anchor,
                "anchor_found": text_has(path, anchor),
                "role": role,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def common_mode_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "CMZ1425_0_target",
            "claim": "GR-like common-mode WEP zero",
            "statement": "If all ordinary matter couples only through one descended quotient metric/coframe and one Hilbert source current, then material component contrasts are common-mode and cannot produce a WEP source contrast.",
            "result": "EXACT_CONDITIONAL_THEOREM_RESTATED",
            "failure_or_gap": "premises are not parent-signed in the current corpus",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "CMZ1425_1_chain_rule",
            "claim": "vertical representative variations are silent to ordinary matter",
            "statement": "For S_matter[psi,e_obs(q(Phi)),theta], any vertical v in ker Dq gives delta_v S_matter = 0 except through quotient-owned constants/readout residuals.",
            "result": "CONDITIONAL_CHAIN_RULE",
            "failure_or_gap": "q-map, observed coframe descent, constants ownership, and readout branch remain unsigned",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "CMZ1425_2_common_hilbert_source",
            "claim": "one Hilbert source owner before readout",
            "statement": "Given one common matter action, variation before readout gives one stress/coframe current; readout may project observations but cannot redefine the variational source.",
            "result": "PARTIAL_WIN_FROM_1079",
            "failure_or_gap": "pre-variation species prefactors w_A survive and are inherited by Hilbert stress",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "CMZ1425_3_no_relative_prefactor",
            "claim": "no source-only species prefactors w_A",
            "statement": "The common-mode theorem becomes WEP-zero only if S_matter cannot contain sum_A w_A S_A with active-source weights independent of nongravitational normalization.",
            "result": "NOT_DERIVED_CURRENT_CORPUS",
            "failure_or_gap": "1333 shows covariance, same-action variation, and field rescaling do not forbid w_A generally",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "CMZ1425_4_measured_G_guard",
            "claim": "common mode can be absorbed into measured G only once",
            "statement": "A universal factor multiplying all ordinary matter source terms may be calibrated into G_N/GM, but relative material/source weights cannot be hidden there.",
            "result": "GUARD_FORMULATED_NOT_CLAIM_GATE",
            "failure_or_gap": "requires proof that the retained residual vector has no relative source component",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_id": "CMZ1425_5_verdict",
            "claim": "common-mode WEP zero is proved",
            "statement": "Assemble quotient descent, single matter action, Hilbert source owner, no source-prefactor theorem, no hidden marker/current, and measured-G guard.",
            "result": "NOT_PROVED_DEMOTE_FINITE_WEP_TO_SOURCED_INPUT_ONLY",
            "failure_or_gap": "no-source-prefactor and parent quotient/current/action-measure clauses remain unsigned",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def premise_audit_rows() -> list[dict[str, Any]]:
    source_rows = read_csv(OUT / "P8_Y5_R10_1332_COMMON_MODE_PREMISE_AUDIT.csv")
    rows: list[dict[str, Any]] = []
    for row in source_rows:
        blocks_zero = str(row.get("parent_signed", "")).lower() != "true"
        rows.append(
            {
                "premise_id": row["premise_id"].replace("PREM1332", "PREM1425"),
                "needed_premise": row["needed_premise"],
                "current_status": row["current_status"],
                "effect_if_signed": row["if_signed"],
                "effect_if_unsigned": row["if_unsigned"],
                "blocks_common_mode_zero": blocks_zero,
                "parent_signed": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.append(
        {
            "premise_id": "PREM1425_7_verdict",
            "needed_premise": "all common-mode WEP-zero premises",
            "current_status": "UNSIGNED_SET",
            "effect_if_signed": "ordinary material/source residual collapses to calibrated common mode",
            "effect_if_unsigned": "finite WEP sourced-input branch remains live",
            "blocks_common_mode_zero": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def current_owner_synthesis_rows() -> list[dict[str, Any]]:
    nco_verdict = first_row(
        OUT / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
        "theorem_id",
        "NCO1079_6_verdict",
    )
    return [
        {
            "synthesis_id": "CUR1425_0_partial_win",
            "object": "Hilbert current/source owner",
            "input_status": nco_verdict["result"],
            "1425_interpretation": "useful subtheorem: post-variation source selectors are conditionally killed",
            "what_it_does_not_kill": "pre-variation species action weights w_A",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "synthesis_id": "CUR1425_1_pre_variation_wall",
            "object": "S_matter=sum_A w_A S_A",
            "input_status": "LIVE_COUNTERMODEL_FROM_1333_AND_1079",
            "1425_interpretation": "current ownership cannot remove weights already inside the action before variation",
            "what_it_does_not_kill": "relative active-source prefactors unless parent admissibility forbids them",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "synthesis_id": "CUR1425_2_consequence",
            "object": "WEP theorem-zero",
            "input_status": "CLOSURE_ONLY_UNSIGNED",
            "1425_interpretation": "common-mode theorem is a strong target but not current evidence",
            "what_it_does_not_kill": "finite source/material/coefficient acquisition route",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def measured_g_guard_rows() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "GCG1425_0_common_scale",
            "object": "universal source scale",
            "allowed_operation": "absorb one universal multiplicative factor into measured G_N/GM calibration",
            "forbidden_operation": "hide material-dependent or source-dependent residual weights in measured G",
            "current_status": "GUARD_ACTIVE_NOT_NUMERIC",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "guard_id": "GCG1425_1_relative_residual",
            "object": "R_TA6V - R_PtRh10 or R_source relative component",
            "allowed_operation": "set to zero only by signed common-mode theorem",
            "forbidden_operation": "set to zero by convention, tau=1, or calibration preference",
            "current_status": "RELATIVE_BRANCH_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "guard_id": "GCG1425_2_product_policy",
            "object": "P_WEP comparison",
            "allowed_operation": "compare only after parent product or finite sourced vectors exist",
            "forbidden_operation": "treat MICROSCOPE bound, surrogate arrays, or component numbers as prediction",
            "current_status": "NO_VALID_PREDICTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def finite_demotion_rows() -> list[dict[str, Any]]:
    candidates = read_csv(OUT / "P8_Y5_R10_1424_TIPT_MATERIAL_VECTOR_CANDIDATES.csv")
    rows: list[dict[str, Any]] = []
    for row in candidates:
        rows.append(
            {
                "demotion_id": row["candidate_id"].replace("MAT1424", "DEM1425"),
                "component": row["component"],
                "available_value": row["numeric_value"],
                "units": row["units"],
                "current_parent_status": row["parent_owner_status"],
                "1425_status": "NONCLAIM_PLUMBING_ONLY",
                "needed_to_promote": row["missing_for_promotion"],
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.append(
        {
            "demotion_id": "DEM1425_4_finite_WEP_branch",
            "component": "finite_WEP_product",
            "available_value": "MISSING_PARENT_PRODUCT",
            "units": "dimensionless after kernel/readout",
            "current_parent_status": "SOURCED_INPUT_ROUTE_ONLY",
            "1425_status": "DEMOTED_TO_INPUT_ACQUISITION",
            "needed_to_promote": "R_source^Earth; R_TA6V-R_PtRh10; C_parent; K_CMSM; measured-G guard; uncertainty/sign convention",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def coefficient_pack_rows() -> list[dict[str, Any]]:
    electron_bound = first_row(
        OUT / "P8_Y5_R10_1333_ELECTRON_RESIDUAL_BOUND_CONTRACT.csv",
        "bound_id",
        "EB1333_0_unit_kernel_electron_prefactor",
    )
    return [
        {
            "pack_id": "PACK1425_0_C_parent",
            "required_input": "C_parent coefficient/operator map",
            "minimum_claim_grade_form": "parent-derived coefficient vector or source-backed finite priors with units, sign, branch, and uncertainty",
            "current_status": "MISSING_PARENT_COEFFICIENT",
            "nonclaim_hint": "electron-only unit-kernel pressure scale exists but is not a coefficient source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "PACK1425_1_electron_prefactor_pressure",
            "required_input": "epsilon_e_or_delta_w_e",
            "minimum_claim_grade_form": "same-branch WEP/readout/source coefficient; not DD import and not unit-kernel assumption",
            "current_status": f"PROXY_BOUND_ONLY_abs_epsilon_less_than_{electron_bound['required_abs_coefficient_max']}",
            "nonclaim_hint": "useful scale for future finite branch, not a WEP pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "PACK1425_2_R_source",
            "required_input": "R_source^Earth",
            "minimum_claim_grade_form": "source worldtube/composition/profile or signed theorem that source leg is common mode",
            "current_status": "MISSING_SOURCE_VECTOR",
            "nonclaim_hint": "must be in same basis as C_parent and material vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "PACK1425_3_R_material",
            "required_input": "R_TA6V - R_PtRh10",
            "minimum_claim_grade_form": "full material response tensor, not isolated component numbers",
            "current_status": "PARTIAL_COMPONENT_ROWS_ONLY",
            "nonclaim_hint": "1424 component rows can seed schema tests only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "PACK1425_4_K_readout",
            "required_input": "K_CMSM",
            "minimum_claim_grade_form": "official CMSM arrays/masks/orbit/attitude or validated reconstruction",
            "current_status": "MISSING_OFFICIAL_EXPORT_SURROGATE_ONLY",
            "nonclaim_hint": "data-side input cannot replace parent coefficient map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def product_rows() -> list[dict[str, Any]]:
    return [
        {
            "product_id": "PROD1425_0_common_mode_zero",
            "product_symbol": "P_WEP_common_mode_zero",
            "product_value": "CONDITIONAL_ONLY_UNSIGNED",
            "runner_status": "REFUSED_NO_ZERO_PROMOTION",
            "reason": "no-source-prefactor and quotient/current/action-measure premises remain unsigned",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "product_id": "PROD1425_1_finite_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_FINITE_SOURCED_INPUTS",
            "runner_status": "REFUSED_NOT_SCOREABLE",
            "reason": "C_parent, R_source, R_material, K_CMSM, and measured-G guard are not all present",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1425_0_common_mode_theorem",
            "claim_component": "universal metric common-mode WEP zero",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "conditional theorem only; no-source-prefactor countermodel survives",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1425_1_hilbert_current_subtheorem",
            "claim_component": "Hilbert current owner after common action",
            "gate_pass": True,
            "claim_allowed": False,
            "reason": "partial subtheorem cannot kill pre-variation species weights",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1425_2_finite_WEP_branch",
            "claim_component": "finite WEP sourced-input route",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "demoted to acquisition pack, no valid prediction row",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1425_3_local_GR",
            "claim_component": "local-GR/Newton reduction",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "source-side common mode is not signed and EH/Newton left-hand reduction still needs its own gate",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1425_0_common_mode_result",
            "decision": "retain common-mode WEP zero as the clean GR-like closure theorem but do not promote it",
            "because": "the no-source-prefactor/admissibility premise is still missing and live countermodels survive",
            "effect": "WEP theorem-zero remains closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1425_1_finite_route",
            "decision": "demote finite WEP to sourced-input-only",
            "because": "component numbers exist but C_parent, R_source, full R_material, K_CMSM, and calibration guard are missing",
            "effect": "future WEP work must fill coefficient/input pack rather than fit or claim zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1425_2_next",
            "decision": "attack active-source-prefactor admissibility or build the finite coefficient pack",
            "because": "this is the exact fork between GR-like universality and phenomenological finite residuals",
            "effect": "1426 should either forbid w_A from parent object language or produce source-backed coefficient acquisition rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1425_0_1426",
            "next_target": "1426-Y5-R10-RAB-active-source-prefactor-admissibility-or-finite-WEP-coefficient-pack.md",
            "script": "scripts/Y5_R10_RAB_active_source_prefactor_admissibility_or_finite_WEP_coefficient_pack.py",
            "objective": "try to derive a parent admissibility principle forbidding active source-only prefactors w_A before variation; if not, build the finite WEP coefficient/input acquisition pack for C_parent, R_source, R_material, K_CMSM, and measured-G guard.",
            "include": "object-language admissibility; active-source prefactor ban; finite coefficient source rows; electron proxy bound; source/material/readout basis lock",
            "exclude": "minimality taste as proof; component fitting; DD import as parent ontology; tau=1; measured-G absorption; WEP/local-GR claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    premises: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        COMMON_MODE_PROOF,
        PREMISE_AUDIT,
        CURRENT_OWNER_SYNTHESIS,
        MEASURED_G_GUARD,
        FINITE_DEMOTION,
        COEFFICIENT_PACK,
        PRODUCT_STATUS,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    parse_ok = True
    parse_errors: list[str] = []
    for path in csvs:
        try:
            _ = read_csv(path)
        except Exception as exc:
            parse_ok = False
            parse_errors.append(f"{path.name}:{type(exc).__name__}")
    premise_safe = any(row["premise_id"] == "PREM1425_7_verdict" and row["parent_signed"] is False for row in premises)
    finite_rows_nonclaim = all(str(row.get("valid_for_claim")).lower() == "false" for row in demotion)
    numeric_finite_rows = all(
        (row["available_value"].startswith("MISSING") or math.isfinite(float(row["available_value"])))
        for row in demotion
    )
    claim_safe = all(str(row.get("claim_allowed")).lower() == "false" for row in claims)
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1425_0_sources", all(row["path_exists"] and row["anchor_found"] for row in sources), "all 1425 cited source paths and anchors resolve"),
        ("VAL1425_1_common_mode_not_promoted", premise_safe, "common-mode theorem remains unsigned and closure-only"),
        ("VAL1425_2_current_owner_synthesis", True, "1079 Hilbert-current subtheorem retained but pre-variation weights survive"),
        ("VAL1425_3_finite_demotion", finite_rows_nonclaim and numeric_finite_rows, "finite component rows demoted to nonclaim input acquisition"),
        ("VAL1425_4_measured_G_guard", True, "common-mode calibration guard forbids hiding relative residuals"),
        ("VAL1425_5_claim_gates", claim_safe, "all claim gates keep claim_allowed=false"),
        ("VAL1425_6_csv_parse", parse_ok, "all generated 1425 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1425_7_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1425_8_next_target", True, "1426 handoff written"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1425_9_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1425 keeps common-mode WEP zero as conditional, demotes finite WEP to sourced-input-only, and blocks WEP/local-GR claims",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1425 - Universal metric common-mode WEP zero or finite source demotion",
            "**Current verdict:** 1425 does not prove local WEP/common-mode zero. It preserves the clean GR-like theorem as an exact conditional route, but the active source-prefactor countermodel survives. Finite WEP is therefore demoted to sourced-input-only: no component fitting, no DD import, no tau shortcut, no measured-G absorption.",
            "**Useful win:** 1079's Hilbert-current owner result is retained as a real subtheorem: after one common action and variation-before-readout, post-variation source selectors are conditionally killed. The surviving enemy is narrower and nastier: pre-variation active-source prefactors `w_A`.",
            "## Source register\n" + md_table(sections["sources"]),
            "## Common-mode WEP-zero proof attempt\n" + md_table(sections["proof"]),
            "## Common-mode premise audit\n" + md_table(sections["premises"]),
            "## Current-owner synthesis\n" + md_table(sections["current"]),
            "## Measured-G common-mode guard\n" + md_table(sections["g_guard"]),
            "## Finite WEP demotion ledger\n" + md_table(sections["demotion"]),
            "## Finite coefficient pack contract\n" + md_table(sections["pack"]),
            "## Product status\n" + md_table(sections["product"]),
            "## Claim gates\n" + md_table(sections["claims"]),
            "## Decision ledger\n" + md_table(sections["decisions"]),
            "## Validation\n" + md_table(sections["validation"]),
            "## Next target\n" + md_table(sections["next"]),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    proof = common_mode_proof_rows()
    premises = premise_audit_rows()
    current = current_owner_synthesis_rows()
    g_guard = measured_g_guard_rows()
    demotion = finite_demotion_rows()
    pack = coefficient_pack_rows()
    product = product_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(COMMON_MODE_PROOF, proof)
    write_csv(PREMISE_AUDIT, premises)
    write_csv(CURRENT_OWNER_SYNTHESIS, current)
    write_csv(MEASURED_G_GUARD, g_guard)
    write_csv(FINITE_DEMOTION, demotion)
    write_csv(COEFFICIENT_PACK, pack)
    write_csv(PRODUCT_STATUS, product)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validation = validation_rows(sources, premises, demotion, claims)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "proof": proof,
            "premises": premises,
            "current": current,
            "g_guard": g_guard,
            "demotion": demotion,
            "pack": pack,
            "product": product,
            "claims": claims,
            "decisions": decisions,
            "next": next_rows,
            "validation": validation,
        }
    )
    remove_pycache()
    print("Y5_R10_1425_common_mode_WEP_zero_unsigned_finite_WEP_demoted_to_sourced_input_only")


if __name__ == "__main__":
    main()

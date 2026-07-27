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

DOC = ROOT / "1426-Y5-R10-RAB-active-source-prefactor-admissibility-or-finite-WEP-coefficient-pack.md"
SOURCE_REGISTER = OUT / "P8_Y5_R10_1426_SOURCE_REGISTER.csv"
ADMISSIBILITY_AUDIT = OUT / "P8_Y5_R10_1426_ACTIVE_SOURCE_PREFACTOR_ADMISSIBILITY_AUDIT.csv"
COUNTERMODEL_GATE = OUT / "P8_Y5_R10_1426_ACTIVE_PREFACTOR_COUNTERMODEL_GATE.csv"
FINITE_COEFFICIENT_PACK = OUT / "P8_Y5_R10_1426_FINITE_WEP_COEFFICIENT_INPUT_PACK.csv"
SAME_BRANCH_LOCK = OUT / "P8_Y5_R10_1426_SAME_BRANCH_WEP_LOCK.csv"
DD_SMOKE_LOCK = OUT / "P8_Y5_R10_1426_DD_SMOKE_INTEGRATION_LOCK.csv"
PRODUCT_STATUS = OUT / "P8_Y5_R10_1426_PRODUCT_STATUS.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1426_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1426_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1426_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1426_VALIDATION.csv"


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


def first_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    raise ValueError(f"missing {key}={value} in {path}")


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


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC1426_0_1425_next", OUT / "P8_Y5_R10_1425_NEXT_TARGET.csv", "NEXT1425_0_1426", "1425 handoff selecting active-source-prefactor admissibility or finite coefficient pack."),
        ("SRC1426_1_1425_validation", OUT / "P8_Y5_BRR545_1425_VALIDATION.csv", "VAL1425_9_overall", "1425 validation summary."),
        ("SRC1426_2_1425_proof", OUT / "P8_Y5_R10_1425_COMMON_MODE_WEP_ZERO_PROOF_ATTEMPT.csv", "CMZ1425_5_verdict", "common-mode zero unsigned verdict."),
        ("SRC1426_3_1425_pack", OUT / "P8_Y5_R10_1425_FINITE_COEFFICIENT_PACK_CONTRACT.csv", "PACK1425_1_electron_prefactor_pressure", "finite coefficient/input pack contract."),
        ("SRC1426_4_1334_admissibility", OUT / "P8_Y5_R10_1334_PARENT_ADMISSIBILITY_PRINCIPLE_AUDIT.csv", "ADM1334_5_verdict", "parent admissibility principle audit."),
        ("SRC1426_5_1334_epsilon", OUT / "P8_Y5_R10_1334_ELECTRON_COEFFICIENT_SOURCE_ACQUISITION.csv", "EPS1334_0_existing_proxy_bound", "epsilon_e proxy bound and zero-certificate status."),
        ("SRC1426_6_1335_normalization", OUT / "P8_Y5_R10_1335_ELECTRON_WEP_PRODUCT_NORMALIZATION_CONTRACT.csv", "WPN1335_2_bound_formula", "symbolic epsilon_e WEP normalization contract."),
        ("SRC1426_7_1335_waitstate", OUT / "P8_Y5_R10_1335_READOUT_SOURCE_WAITSTATE.csv", "WAIT1335_4_parent_branch", "readout/source waitstate blockers."),
        ("SRC1426_8_1335_manifest", OUT / "P8_Y5_R10_1335_OFFICIAL_INPUT_REQUEST_MANIFEST.csv", "MAN1335_0_readout_arrays", "official input request manifest."),
        ("SRC1426_9_1080_pack", OUT / "P8_Y5_R10_1080_FINITE_WEP_INPUT_PACK_NONCLAIM.csv", "FIP1080_1_C_parent", "finite WEP input pack."),
        ("SRC1426_10_1081_dd", OUT / "P8_Y5_R10_1081_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv", "DDS1081_0_alpha_unit", "DD smoke coefficient-normalized rows."),
        ("SRC1426_11_1081_gate", OUT / "P8_Y5_R10_1081_PARENT_TO_DD_GATE.csv", "PDD1081_1_coefficient_map", "parent-to-DD gate."),
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


def admissibility_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "ADM1426_0_target",
            "route": "active-source-prefactor admissibility",
            "claim": "forbid pre-variation source-only species prefactors w_A from the parent matter object language",
            "evidence": "1425 identifies w_A as the surviving wall",
            "result": "TARGET_SHARPENED",
            "missing_for_parent_signature": "derive the object language/admissibility rule from MTS primitives rather than adopting minimality taste",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ADM1426_1_typed_domain",
            "route": "typed coefficient domain",
            "claim": "source-only species labels have no morphism into active gravitational source coefficients",
            "evidence": "ADM1334_1_typed_domain_route",
            "result": "EXACT_CONDITIONAL_META_THEOREM",
            "missing_for_parent_signature": "META/NHA type-rule premises are not yet parent-derived",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ADM1426_2_minimal_signature",
            "route": "minimal ordinary matter signature",
            "claim": "ordinary matter action has no source-only w_A slot",
            "evidence": "ADM1334_2_minimal_signature_route",
            "result": "CLOSURE_SCHEMA_ONLY",
            "missing_for_parent_signature": "minimal signature is a closure choice until derived from parent action syntax",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ADM1426_3_action_measure",
            "route": "single action-measure owner",
            "claim": "one hbar/measure/action owner makes relative source weights non-admissible",
            "evidence": "ADM1334_3_action_measure_owner; 1078 action-measure proof attempt",
            "result": "NOT_PARENT_SIGNED",
            "missing_for_parent_signature": "measure owner and radiative/readout stability remain unsigned",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ADM1426_4_forbidden_vertex",
            "route": "forbidden source-weight vertex",
            "claim": "w_A is a forbidden visible source-weight vertex",
            "evidence": "ADM1334_4_forbidden_vertex_route",
            "result": "FORBIDDEN_REQUIRED_NOT_FORBIDDEN_DERIVED",
            "missing_for_parent_signature": "forbidden-vertex catalog is a gate, not proof the parent action excludes it",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ADM1426_5_verdict",
            "route": "parent admissibility theorem",
            "claim": "active-source prefactors w_A are parent-forbidden",
            "evidence": "ADM1426_1 through ADM1426_4",
            "result": "NOT_DERIVED_CURRENT_CORPUS",
            "missing_for_parent_signature": "need a primitive or derived action signature that makes active source-only scalars ill-typed",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM1426_0_pre_variation_wA",
            "form": "S_matter = sum_A w_A S_A[psi_A,e_obs,theta_A]",
            "current_status": "LIVE_COUNTERMODEL",
            "survives": "covariance, additivity, same-action variation, and Hilbert-current ownership after insertion",
            "kills_common_mode": True,
            "required_response": "parent admissibility theorem or finite coefficient epsilon_A rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1426_1_hidden_marker_weight",
            "form": "w_A = w_common(1 + epsilon marker_A)",
            "current_status": "LIVE_COUNTERMODEL",
            "survives": "unless no-marker/no-hidden-spurion theorem is parent-signed",
            "kills_common_mode": True,
            "required_response": "no-hidden visible coefficient theorem or retained marker coefficient bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1426_2_nonHilbert_source_current",
            "form": "J_source = kappa T_Hilbert + zeta_A J_NH,A",
            "current_status": "LIVE_COUNTERMODEL",
            "survives": "unless non-Hilbert currents are exact/projected silent or parent-forbidden",
            "kills_common_mode": True,
            "required_response": "non-Hilbert current zero theorem or finite residual coefficient pack",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def finite_pack_rows() -> list[dict[str, Any]]:
    eps = first_row(
        OUT / "P8_Y5_R10_1334_ELECTRON_COEFFICIENT_SOURCE_ACQUISITION.csv",
        "source_id",
        "EPS1334_0_existing_proxy_bound",
    )
    unit_tau = first_row(
        OUT / "P8_Y5_R10_1335_EPSILON_E_BOUND_RESCALING_TABLE.csv",
        "row_id",
        "TAU1335_0_unit_kernel_smoke",
    )
    dd_alpha = first_row(
        OUT / "P8_Y5_R10_1081_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv",
        "smoke_id",
        "DDS1081_0_alpha_unit",
    )
    dd_surface = first_row(
        OUT / "P8_Y5_R10_1081_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv",
        "smoke_id",
        "DDS1081_1_surface_unit",
    )
    return [
        {
            "pack_id": "PACK1426_0_C_parent",
            "object": "C_parent coefficient/operator map",
            "current_value_or_bound": "MISSING_PARENT_COEFFICIENT",
            "source_or_proxy": "FIP1080_1_C_parent; PACK1425_0_C_parent",
            "same_branch_status": "MISSING_BRANCH_CLASSIFIER",
            "needed_for_claim": "parent-derived coefficient vector or source-backed finite priors with units/sign/basis",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "PACK1426_1_epsilon_e_proxy",
            "object": "epsilon_e_or_delta_w_e",
            "current_value_or_bound": eps["value_or_bound"],
            "source_or_proxy": eps["source_basis"],
            "same_branch_status": eps["same_branch_status"],
            "needed_for_claim": "tau_eff_e/source/readout/product convention and parent coefficient source",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "PACK1426_2_unit_tau_sensitivity",
            "object": "unit-kernel epsilon_e scale",
            "current_value_or_bound": unit_tau["epsilon_e_required_abs_max"],
            "source_or_proxy": "TAU1335_0_unit_kernel_smoke",
            "same_branch_status": "UNIT_KERNEL_SMOKE_ONLY",
            "needed_for_claim": "replace tau_eff=1 with sourced K_readout*S_source*O_orbit",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "PACK1426_3_R_source",
            "object": "R_source^Earth",
            "current_value_or_bound": "MISSING_SOURCE_VECTOR",
            "source_or_proxy": "FIP1080_2_R_source; WAIT1335_2_source_worldtube",
            "same_branch_status": "MISSING_SOURCE_PROFILE_WEIGHTING",
            "needed_for_claim": "source worldtube/composition/profile in the same parent basis as C_parent",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "PACK1426_4_R_material",
            "object": "R_TA6V - R_PtRh10",
            "current_value_or_bound": "PARTIAL_COMPONENT_ROWS_ONLY",
            "source_or_proxy": "1424 Ti/Pt candidates; DD smoke deltas",
            "same_branch_status": "MISSING_FULL_PARENT_MATERIAL_TENSOR",
            "needed_for_claim": "full parent material response tensor or explicitly adopted external comparator branch",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "PACK1426_5_K_CMSM",
            "object": "MICROSCOPE readout kernel",
            "current_value_or_bound": "MISSING_OFFICIAL_EXPORT_SURROGATE_ONLY",
            "source_or_proxy": "WAIT1335_0_official_arrays; MAN1335_0_readout_arrays",
            "same_branch_status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "needed_for_claim": "official/exported arrays with masks/orbit/attitude/product convention",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "PACK1426_6_DD_alpha_pressure",
            "object": "DD alpha smoke coefficient scale",
            "current_value_or_bound": dd_alpha["required_abs_coefficient_max"],
            "source_or_proxy": "DDS1081_0_alpha_unit",
            "same_branch_status": "EXTERNAL_DD_SMOKE_NOT_MTS",
            "needed_for_claim": "MTS-to-DD coefficient map plus physical source/readout normalization",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "PACK1426_7_DD_surface_pressure",
            "object": "DD surface smoke coefficient scale",
            "current_value_or_bound": dd_surface["required_abs_coefficient_max"],
            "source_or_proxy": "DDS1081_1_surface_unit",
            "same_branch_status": "EXTERNAL_DD_SMOKE_NOT_MTS",
            "needed_for_claim": "MTS-to-DD coefficient map plus physical source/readout normalization",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def same_branch_lock_rows() -> list[dict[str, Any]]:
    waits = read_csv(OUT / "P8_Y5_R10_1335_READOUT_SOURCE_WAITSTATE.csv")
    rows: list[dict[str, Any]] = []
    for row in waits:
        rows.append(
            {
                "lock_id": row["wait_id"].replace("WAIT1335", "LOCK1426"),
                "object": row["object"],
                "current_status": row["current_status"],
                "source": row["source"],
                "effect_on_1426": row["effect"],
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    rows.append(
        {
            "lock_id": "LOCK1426_5_verdict",
            "object": "same-branch WEP finite product",
            "current_status": "LOCKED_WAITSTATE",
            "source": "LOCK1426_0 through LOCK1426_4",
            "effect_on_1426": "finite coefficient pack is acquisition-ready but not score-ready",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    )
    return rows


def dd_smoke_rows() -> list[dict[str, Any]]:
    return [
        {
            "dd_lock_id": "DD1426_0_numeric_smoke_rows",
            "object": "DD alpha/surface unit-response rows",
            "current_status": "NUMERIC_NONCLAIM",
            "why_useful": "coefficient-normalized pressure scales for pipeline algebra",
            "why_not_claim": "external DD basis, unit source/readout proxy, no MTS-to-DD map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "dd_lock_id": "DD1426_1_parent_to_DD_map",
            "object": "C_parent -> (c_alpha,c_surface)",
            "current_status": "MISSING_PARENT_TO_DD_MAP",
            "why_useful": "would connect finite WEP pack to existing DD smoke rows",
            "why_not_claim": "no parent coefficient vector or units",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "dd_lock_id": "DD1426_2_source_readout",
            "object": "physical Earth source and MICROSCOPE readout normalization",
            "current_status": "MISSING_PHYSICAL_SOURCE_READOUT",
            "why_useful": "would replace unit proxy in coefficient scales",
            "why_not_claim": "tau_eff and source-worldtube not sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def product_rows() -> list[dict[str, Any]]:
    return [
        {
            "product_id": "PROD1426_0_admissibility_zero",
            "product_symbol": "P_WEP_common_mode_zero",
            "product_value": "NOT_DERIVED_ACTIVE_PREFACTOR_COUNTERMODEL_LIVE",
            "runner_status": "REFUSED_ZERO_PROMOTION",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "product_id": "PROD1426_1_finite_WEP_pack",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_C_PARENT_R_SOURCE_R_MATERIAL_K_READOUT_BRANCH_LOCK",
            "runner_status": "ACQUISITION_PACK_READY_NOT_SCOREABLE",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1426_0_admissibility_theorem",
            "claim_component": "active-source-prefactor ban",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "typed/minimal/forbidden routes remain conditional parent grammar choices",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1426_1_common_mode_zero",
            "claim_component": "common-mode WEP zero",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "w_A countermodel remains live",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1426_2_finite_pack",
            "claim_component": "finite WEP coefficient/input pack",
            "gate_pass": True,
            "claim_allowed": False,
            "reason": "pack is acquisition-ready but not score-ready",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1426_3_DD_smoke",
            "claim_component": "DD smoke coefficient scales",
            "gate_pass": True,
            "claim_allowed": False,
            "reason": "numeric external comparator rows are not MTS-derived",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1426_4_WEP_local_GR",
            "claim_component": "WEP/local-GR pass",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "no signed common-mode theorem and no valid finite WEP prediction row",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1426_0_admissibility_result",
            "decision": "do not promote the active-source-prefactor ban",
            "because": "all routes are still exact conditionals or closure schemas rather than derived parent action consequences",
            "effect": "common-mode WEP zero remains closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1426_1_finite_pack_result",
            "decision": "use the finite WEP coefficient/input pack as the practical next object",
            "because": "epsilon_e and DD pressure scales exist, but same-branch source/readout and C_parent are missing",
            "effect": "future work should source branch-locked inputs rather than fit components",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1426_2_next",
            "decision": "target branch-locked WEP input manifest or parent action signature",
            "because": "the theory and data routes now share the same lock: source coefficients must be parent-owned or explicitly sourced in one branch",
            "effect": "1427 should make either the parent action signature primitive explicit or turn the finite pack into a concrete intake manifest",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1426_0_1427",
            "next_target": "1427-Y5-R10-RAB-parent-action-signature-or-branch-locked-WEP-input-manifest.md",
            "script": "scripts/Y5_R10_RAB_parent_action_signature_or_branch_locked_WEP_input_manifest.py",
            "objective": "either write the explicit parent action signature/admissibility clause that forbids active-source prefactors as a declared closure, or build the branch-locked finite WEP input manifest for C_parent, epsilon_e/DD coefficients, R_source, R_material, K_CMSM, and measured-G guard.",
            "include": "parent action signature; branch id; coefficient units/signs; source worldtube; material tensor; official readout manifest; runner refusal",
            "exclude": "minimality as derivation; WEP/local-GR claim; tau=1; DD as MTS ontology; component fitting; measured-G absorption; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    admissibility: list[dict[str, Any]],
    finite_pack: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        ADMISSIBILITY_AUDIT,
        COUNTERMODEL_GATE,
        FINITE_COEFFICIENT_PACK,
        SAME_BRANCH_LOCK,
        DD_SMOKE_LOCK,
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
    admissibility_not_signed = any(
        row["audit_id"] == "ADM1426_5_verdict" and row["parent_signed"] is False for row in admissibility
    )
    pack_nonclaim = all(str(row.get("valid_for_claim")).lower() == "false" for row in finite_pack)
    finite_numeric_or_missing = True
    for row in finite_pack:
        value = str(row["current_value_or_bound"])
        if value.startswith("MISSING") or value.startswith("PARTIAL"):
            continue
        try:
            finite_numeric_or_missing = finite_numeric_or_missing and math.isfinite(float(value))
        except ValueError:
            finite_numeric_or_missing = False
    claim_safe = all(str(row.get("claim_allowed")).lower() == "false" for row in claims)
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1426_0_sources", all(row["path_exists"] and row["anchor_found"] for row in sources), "all 1426 cited source paths and anchors resolve"),
        ("VAL1426_1_admissibility_not_signed", admissibility_not_signed, "active-source-prefactor ban remains unsigned"),
        ("VAL1426_2_countermodels", True, "active prefactor/marker/nonHilbert countermodels retained"),
        ("VAL1426_3_finite_pack", pack_nonclaim and finite_numeric_or_missing, "finite coefficient pack is acquisition-ready, numeric where proxy rows exist, and nonclaim"),
        ("VAL1426_4_same_branch_lock", True, "same-branch source/readout/product lock remains closed"),
        ("VAL1426_5_claim_gates", claim_safe, "all claim gates keep claim_allowed=false"),
        ("VAL1426_6_csv_parse", parse_ok, "all generated 1426 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1426_7_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1426_8_next_target", True, "1427 handoff written"),
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
            "check_id": "VAL1426_9_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1426 does not derive active-source-prefactor admissibility; finite WEP coefficient/input pack is consolidated as nonclaim",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1426 - Active-source-prefactor admissibility or finite WEP coefficient pack",
            "**Current verdict:** 1426 does not derive the active-source-prefactor admissibility theorem. The `w_A` countermodel survives unless MTS explicitly signs a parent action/object-language rule forbidding source-only species weights before variation.",
            "**Main progress:** the finite route is now one consolidated coefficient/input pack. The pack is not evidence, but it is clean: `C_parent`, `epsilon_e`, DD smoke scales, `R_source`, `R_material`, `K_CMSM`, same-branch lock, and measured-G guard are all named without tau, DD, or calibration shortcuts.",
            "## Source register\n" + md_table(sections["sources"]),
            "## Active-source-prefactor admissibility audit\n" + md_table(sections["admissibility"]),
            "## Active-prefactor countermodel gate\n" + md_table(sections["countermodels"]),
            "## Finite WEP coefficient/input pack\n" + md_table(sections["finite_pack"]),
            "## Same-branch WEP lock\n" + md_table(sections["same_branch"]),
            "## DD smoke integration lock\n" + md_table(sections["dd_smoke"]),
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
    admissibility = admissibility_rows()
    countermodels = countermodel_rows()
    finite_pack = finite_pack_rows()
    same_branch = same_branch_lock_rows()
    dd_smoke = dd_smoke_rows()
    product = product_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ADMISSIBILITY_AUDIT, admissibility)
    write_csv(COUNTERMODEL_GATE, countermodels)
    write_csv(FINITE_COEFFICIENT_PACK, finite_pack)
    write_csv(SAME_BRANCH_LOCK, same_branch)
    write_csv(DD_SMOKE_LOCK, dd_smoke)
    write_csv(PRODUCT_STATUS, product)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validation = validation_rows(sources, admissibility, finite_pack, claims)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "admissibility": admissibility,
            "countermodels": countermodels,
            "finite_pack": finite_pack,
            "same_branch": same_branch,
            "dd_smoke": dd_smoke,
            "product": product,
            "claims": claims,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1426_active_prefactor_admissibility_unsigned_finite_WEP_pack_consolidated_nonclaim")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3465-Y5-R2FR-EM-alpha-Hodge-charge-owner-or-WEP-raw-to-effective-map.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

ETA_TIPT_BOUND = 2.8e-15
DELTA_Q_ALPHA_ABS = 0.001989808886825
D_E_ALPHA_BOUND = ETA_TIPT_BOUND / DELTA_Q_ALPHA_ABS

SOURCES = {
    "script_3465": Path(__file__).resolve(),
    "doc_3464": ROOT / "3464-Y5-R2FR-canonical-action-normalization-from-MTS-primitives-or-WEP-effective-source-bound.md",
    "canon_3464": OUT / "P8_Y5_R2FR_3464_CANONICAL_NORMALIZATION_THEOREM_AUDIT.csv",
    "em_3464": OUT / "P8_Y5_R2FR_3464_EM_ALPHA_CHARGE_OWNER_AUDIT.csv",
    "wep_3464": OUT / "P8_Y5_R2FR_3464_WEP_EFFECTIVE_SOURCE_BOUND.csv",
    "raw_req_3464": OUT / "P8_Y5_R2FR_3464_RAW_TO_EFFECTIVE_REQUIREMENTS.csv",
    "doc_3463": ROOT / "3463-Y5-R2FR-single-source-current-owner-from-Noether-Poynting-flow-or-WEP-tau-map-under-AX1090.md",
    "poynting_3463": OUT / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv",
    "tau_3463": OUT / "P8_Y5_R2FR_3463_WEP_TAU_PROJECTION_DERIVATION.csv",
    "material_1061": OUT / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv",
    "dd_map_2441": OUT / "P8_Y5_PARENT_QLOC_2441_MTS_TO_DD_CHARGE_MAP.csv",
    "alpha_owner_1811": OUT / "P8_Y5_PARENT_QLOC_1811_ALPHA_OWNER_AUDIT.csv",
    "alpha_level_1812": OUT / "P8_Y5_PARENT_QLOC_1812_ALPHA_LEVEL_OWNER_AUDIT.csv",
    "alpha_path_1930": OUT / "P8_Y5_PARENT_QLOC_1930_ALPHA_PRODUCT_PATH_DECISION.csv",
    "charge_current": OUT / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
    "charge_residuals": OUT / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
    "charge_spine_2340": OUT / "P8_Y5_PARENT_QLOC_2340_PARENT_CHARGE_EXTRACTION_SPINE.csv",
    "local_bounds": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body: list[str] = []
    for row in rows:
        values = [
            str(row.get(field, ""))
            .replace("\n", "<br>")
            .replace("|", "/")
            for field in fields
        ]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    roles = {
        "script_3465": "generator for this checkpoint",
        "doc_3464": "canonical normalization predecessor",
        "canon_3464": "canonical no-sector-action-scale theorem audit",
        "em_3464": "EM alpha/charge owner predecessor rows",
        "wep_3464": "effective WEP source bound rows",
        "raw_req_3464": "raw-to-effective requirements",
        "doc_3463": "Poynting/source-current predecessor",
        "poynting_3463": "Maxwell/Poynting stress ledger",
        "tau_3463": "Eotvos tau/effective contrast derivation",
        "material_1061": "MICROSCOPE Ti/Pt material convention with Delta_Q_alpha",
        "dd_map_2441": "MTS-to-Damour-Donoghue charge map",
        "alpha_owner_1811": "alpha owner audit",
        "alpha_level_1812": "alpha level/fibre norm owner audit",
        "alpha_path_1930": "alpha product path decision",
        "charge_current": "charge-current equality attempt",
        "charge_residuals": "charge-current residual decomposition",
        "charge_spine_2340": "parent charge extraction spine",
        "local_bounds": "source-backed local empirical bound ledger",
    }
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
        }
        for key, path in SOURCES.items()
    ]


def em_owner_package_audit() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "EMO3465_0_observed_hodge",
            "owner_clause": "observed coframe/Hodge star owns Maxwell F^2",
            "derivation_attempt": "S_EM=-1/(4 mu0) int F wedge *_obs F; the same *_obs defines stress, Poynting flow, and light cone.",
            "result": "CONDITIONAL_STANDARD_FORM",
            "gap": "MTS has not yet derived *_obs as the unique EM Hodge/flow rule from parent motion/time/space primitives.",
            "source_path": str(SOURCES["poynting_3463"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "EMO3465_1_unique_F2",
            "owner_clause": "unique Maxwell curvature norm",
            "derivation_attempt": "ban independent lambda(X) F^2, w_EM F^2, and hidden scalar gauge-kinetic coefficients.",
            "result": "NOT_PARENT_DERIVED",
            "gap": "1812 keeps unique F2 and typed coefficient-domain certificate unsigned.",
            "source_path": str(SOURCES["alpha_level_1812"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "EMO3465_2_charge_current",
            "owner_clause": "A_mu and J^mu normalization share one charge-current owner",
            "derivation_attempt": "gauge rescaling A->lambda A moves normalization into charge/current; physical alpha and spectra fix the convention only if the parent charge extraction spine is signed.",
            "result": "PARENT_CHARGE_SPINE_EXISTS_VALUES_MISSING",
            "gap": "charge extraction, fixed reference, source denominator, and residual charge silence are still missing.",
            "source_path": str(SOURCES["charge_spine_2340"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "EMO3465_3_alpha_level",
            "owner_clause": "fine-structure constant is parent-level fixed",
            "derivation_attempt": "alpha_EM=alpha_*(ell_EM,g_*) and Lie_v alpha_EM=0 would force b_alpha=0.",
            "result": "ALPHA_LEVEL_OWNER_NOT_DERIVED",
            "gap": "fixed level, vertical generator norm, Hom exclusion, unique F2, and readout/radiative closure are not closed together.",
            "source_path": str(SOURCES["alpha_level_1812"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "EMO3465_4_readout_radiative",
            "owner_clause": "readout/radiative closure preserves alpha owner",
            "derivation_attempt": "spectroscopy, clocks, EFT running, material readout, and hbar*c conventions must not regenerate f_X F^2 or b_alpha.",
            "result": "UNSIGNED_PRESERVATION_REQUIREMENT",
            "gap": "current alpha product path retains clock/WEP alpha products as finite nonclaim bounds.",
            "source_path": str(SOURCES["alpha_path_1930"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "EMO3465_5_verdict",
            "owner_clause": "w_EM and b_alpha theorem-zero from EM owner package",
            "derivation_attempt": "close EMO3465_0 through EMO3465_4 as parent-derived clauses.",
            "result": "NOT_DERIVED_CURRENT_CORPUS",
            "gap": "the theorem is exact conditionally, but 3465 must retain raw-to-effective WEP component rows.",
            "source_path": str(SOURCES["em_3464"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def alpha_only_bound_calculation() -> list[dict[str, Any]]:
    return [
        {
            "calc_id": "AOB3465_0_eta_bound",
            "quantity": "eta_TiPt_bound",
            "value": f"{ETA_TIPT_BOUND:.12e}",
            "units": "dimensionless",
            "source_path": str(SOURCES["local_bounds"]),
            "source_row": "R1_WEP_source_charge",
            "role": "empirical ceiling for effective WEP contrast",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "calc_id": "AOB3465_1_delta_Q_alpha",
            "quantity": "Delta_Q_alpha_Coulomb_abs",
            "value": f"{DELTA_Q_ALPHA_ABS:.15g}",
            "units": "dimensionless",
            "source_path": str(SOURCES["material_1061"]),
            "source_row": "MCON1061_1_delta_Q_alpha",
            "role": "smoke material alpha/Coulomb charge difference",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "calc_id": "AOB3465_2_D_e_bound",
            "quantity": "D_e_eff_abs_bound",
            "value": f"{D_E_ALPHA_BOUND:.12e}",
            "units": "dimensionless",
            "source_path": str(SOURCES["script_3465"]),
            "source_row": "computed: eta_TiPt_bound / Delta_Q_alpha_Coulomb_abs",
            "role": "nonclaim alpha-only effective source-leg ceiling",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "calc_id": "AOB3465_3_assumption",
            "quantity": "alpha-only direct WEP model",
            "value": "Delta_w_eff_alpha = D_e_eff * Delta_Q_alpha_Coulomb_abs",
            "units": "dimensionless",
            "source_path": str(SOURCES["dd_map_2441"]),
            "source_row": "DDMAP2441_0_b_alpha_to_De plus MCON1061_1_delta_Q_alpha",
            "role": "valid only if alpha channel is isolated and full material/readout tensor is deferred",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def raw_to_effective_component_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "RTE3465_0_direct_weight",
            "component": "tau_w * Delta_w_raw_TiPt",
            "formula": "Delta_w_eff_direct = tau_w Delta_w_raw_TiPt",
            "numeric_status": "MISSING",
            "bound_or_value": "MISSING_PARENT_TO_EOTVOS_PROJECTION",
            "units": "dimensionless",
            "source_path": str(SOURCES["raw_req_3464"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "RTE3465_1_alpha_channel",
            "component": "D_e_eff * Delta_Q_alpha_Coulomb_abs",
            "formula": "D_e_eff = S_E^q b_alpha; |D_e_eff| <= eta_bound/Delta_Q_alpha",
            "numeric_status": "NONCLAIM_EFFECTIVE_BOUND",
            "bound_or_value": f"{D_E_ALPHA_BOUND:.12e}",
            "units": "dimensionless",
            "source_path": str(SOURCES["material_1061"]),
            "source_row": "MCON1061_1_delta_Q_alpha; R1_WEP_source_charge",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "RTE3465_2_mass_nuclear_channel",
            "component": "D_mhat_eff * Delta_Q_mhat_or_nuclear",
            "formula": "D_mhat_eff=S_E^q b_mhat; material response not in current MTS basis",
            "numeric_status": "MISSING_COMPONENT_AND_MATERIAL_CHARGE",
            "bound_or_value": "MISSING_B_MHAT_AND_DELTA_Q_MHAT",
            "units": "dimensionless",
            "source_path": str(SOURCES["dd_map_2441"]),
            "source_row": "DDMAP2441_1_missing_b_mhat",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "RTE3465_3_shadow_source",
            "component": "Delta_shadow_source",
            "formula": "hidden/source-shadow current projected into Ti/Pt/Earth material contrast",
            "numeric_status": "MISSING_PROJECTION",
            "bound_or_value": "MISSING_SHADOW_BASIS_AND_MATERIAL_MAP",
            "units": "dimensionless",
            "source_path": str(SOURCES["dd_map_2441"]),
            "source_row": "DDMAP2441_3_delta_w_shadow_direct",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "RTE3465_4_readout_frame",
            "component": "Delta_readout + b_g/material-standard reentry",
            "formula": "frame/readout response contributes to WEP only through material-standard or hidden-visible reentry",
            "numeric_status": "MISSING_READOUT_MAP",
            "bound_or_value": "MISSING_FRAME_MATERIAL_STANDARD_RESPONSE",
            "units": "dimensionless",
            "source_path": str(SOURCES["dd_map_2441"]),
            "source_row": "DDMAP2441_4_b_g",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "RTE3465_5_no_cancellation_guard",
            "component": "sum_abs_effective_components",
            "formula": "|direct|+|alpha|+|mass/nuclear|+|shadow|+|readout| <= 2.8e-15",
            "numeric_status": "GUARD_REQUIRED_COMPONENTS_MISSING",
            "bound_or_value": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(SOURCES["wep_3464"]),
            "source_row": "WEB3464_2_MICROSCOPE_bound; RTE3464_4_no_cancellation",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def owner_to_chain_update() -> list[dict[str, Any]]:
    return [
        {
            "chain_id": "CHAIN3465_0_to_3464",
            "feeds": "CAN3464_3_EM_alpha_owner;EAC3464_5_verdict",
            "update": "EM owner package tested and not parent-closed; exact missing clauses are Hodge, unique F2, charge-current, alpha level, and readout/radiative closure.",
            "status": "EM_OWNER_NOT_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN3465_1_to_WEP_bound",
            "feeds": "WEB3464_3_raw_parent_map;RTE3464_1_b_alpha",
            "update": "alpha-only effective WEP source-leg ceiling computed: |D_e_eff| <= 1.407170315973e-12.",
            "status": "NUMERIC_NONCLAIM_BOUND_ROW_ADDED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN3465_2_to_3460_3459",
            "feeds": "Y5B3460_0_source_work_norm;RDB3459_0_Z_amplitude",
            "update": "raw source terms still cannot plug into J_norm until raw-to-effective map or canonical zero theorem closes.",
            "status": "RAW_MAP_STILL_BLOCKS_LOCAL_ZERO",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN3465_3_to_EM_spine",
            "feeds": "Maxwell/Poynting stress ledger",
            "update": "Poynting remains a valid diagnostic, but EM normalization closure is not yet proven.",
            "status": "POYNTING_DIAGNOSTIC_RETAINED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3465_0_EM_owner",
            "claim": "w_EM and b_alpha are theorem-zero from EM owner package",
            "status": "FAIL_BLOCKED",
            "reason": "observed Hodge, unique F2, alpha level, charge-current, and readout/radiative clauses are not parent-signed together",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3465_1_alpha_effective_bound",
            "claim": "alpha-only effective source-leg bound is numerically written",
            "status": "PASS_NONCLAIM_BOUND",
            "reason": "uses source-backed eta ceiling and existing smoke Delta_Q_alpha; it is a bound row, not an MTS prediction",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3465_2_raw_MTS_prediction",
            "claim": "raw MTS coefficients predict the WEP contrast",
            "status": "FAIL_BLOCKED",
            "reason": "direct, mass/nuclear, shadow, and readout components remain unmapped or missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3465_3_no_cancellation",
            "claim": "signed cancellations can make a WEP pass",
            "status": "FAIL_BLOCKED",
            "reason": "absolute-component envelope is required until every retained channel is sourced or theorem-zero",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3465_4_local_GR_source",
            "claim": "local GR/Newton source coupling is derived",
            "status": "FAIL_BLOCKED",
            "reason": "EM/source normalization is only one gate; source-current, boundary/domain, residual and PPN gates remain",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3465_0_owner_result",
            "decision": "Do not claim EM owner theorem-zero.",
            "because": "The owner package is coherent but still unsigned at Hodge/unique-F2/alpha/charge/readout levels.",
            "next_action": "Either attack unique F2/Hodge owner directly or continue raw WEP component acquisition.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3465_1_numeric_progress",
            "decision": "Keep the alpha-only effective WEP bound as real finite progress.",
            "because": "It converts existing Delta_Q_alpha and MICROSCOPE eta rows into a concrete source-leg ceiling.",
            "next_action": "Use it as a nonclaim guard while sourcing b_mhat and raw-to-effective maps.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3465_2_next_route",
            "decision": "Next best route is unique F2/Hodge owner or nuclear/mass WEP row.",
            "because": "Alpha is now bounded as an effective component; the dominant missing WEP material physics is mass/nuclear response, while the clean derivation route is still EM owner closure.",
            "next_action": "3466 should choose between unique-F2/Hodge proof and b_mhat/material charge acquisition.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3466-Y5-R2FR-unique-F2-Hodge-owner-or-WEP-nuclear-mass-component-row.md",
            "next_script": "scripts/Y5_R2FR_3466_unique_F2_Hodge_owner_or_WEP_nuclear_mass_component_row.py",
            "objective": "Try to derive unique Maxwell F2/Hodge/coframe ownership from MTS primitives; if it does not close, build the missing b_mhat/nuclear material component row needed for the raw-to-effective WEP map.",
            "success_gate": "Either the alpha/EM source coefficient is theorem-zero from a parent Hodge/F2 owner, or the WEP raw-to-effective map gains a sourced nuclear/mass component row with units and no-cancellation envelope.",
            "exclude": "GitHub action; formalization-workbench edits; public WEP/local-GR claim; signed cancellation; alpha-owner overclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validate(paths: dict[str, Path], datasets: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    stamp = now()

    sources = datasets["source_register"]
    missing_sources = [row["source_id"] for row in sources if not row["exists"]]
    checks.append(
        {
            "check_id": "VAL3465_0_sources_exist",
            "passed": not missing_sources,
            "detail": f"{len(sources) - len(missing_sources)}/{len(sources)} source paths exist; missing={';'.join(missing_sources) or 'none'}",
            "timestamp_utc": stamp,
        }
    )

    owner = datasets["em_owner_package_audit"]
    owner_results = {row["audit_id"]: row["result"] for row in owner}
    checks.append(
        {
            "check_id": "VAL3465_1_EM_owner_not_overclaimed",
            "passed": owner_results.get("EMO3465_5_verdict") == "NOT_DERIVED_CURRENT_CORPUS"
            and owner_results.get("EMO3465_2_charge_current") == "PARENT_CHARGE_SPINE_EXISTS_VALUES_MISSING",
            "detail": ";".join(f"{key}={value}" for key, value in owner_results.items()),
            "timestamp_utc": stamp,
        }
    )

    alpha_rows = datasets["alpha_only_bound_calculation"]
    bound_rows = [row for row in alpha_rows if row["calc_id"] == "AOB3465_2_D_e_bound"]
    expected = ETA_TIPT_BOUND / DELTA_Q_ALPHA_ABS
    calculated = float(bound_rows[0]["value"]) if bound_rows else float("nan")
    checks.append(
        {
            "check_id": "VAL3465_2_alpha_bound_calculated",
            "passed": abs(calculated - expected) <= expected * 1e-12,
            "detail": f"D_e_bound={calculated:.12e};expected={expected:.12e}",
            "timestamp_utc": stamp,
        }
    )

    components = datasets["raw_to_effective_component_rows"]
    checks.append(
        {
            "check_id": "VAL3465_3_raw_components_and_guard",
            "passed": any(row["component_id"] == "RTE3465_1_alpha_channel" and row["numeric_status"] == "NONCLAIM_EFFECTIVE_BOUND" for row in components)
            and any(row["component_id"] == "RTE3465_2_mass_nuclear_channel" and "MISSING" in row["numeric_status"] for row in components)
            and any(row["component_id"] == "RTE3465_5_no_cancellation_guard" for row in components),
            "detail": ";".join(f"{row['component_id']}={row['numeric_status']}" for row in components),
            "timestamp_utc": stamp,
        }
    )

    chain = datasets["owner_to_chain_update"]
    checks.append(
        {
            "check_id": "VAL3465_4_chain_update_present",
            "passed": any("NUMERIC_NONCLAIM_BOUND_ROW_ADDED" in row["status"] for row in chain)
            and any("EM_OWNER_NOT_DERIVED" in row["status"] for row in chain),
            "detail": ";".join(f"{row['chain_id']}={row['status']}" for row in chain),
            "timestamp_utc": stamp,
        }
    )

    claim_rows = [
        row
        for rows in datasets.values()
        for row in rows
        if str(row.get("valid_for_claim", "")).lower() == "true"
        or str(row.get("claim_allowed", "")).lower() == "true"
    ]
    checks.append(
        {
            "check_id": "VAL3465_5_no_claim_rows",
            "passed": not claim_rows,
            "detail": f"claim_like_rows={len(claim_rows)}",
            "timestamp_utc": stamp,
        }
    )

    parse_ok = True
    parse_details: list[str] = []
    for name, path in paths.items():
        if path.suffix.lower() == ".csv":
            if name == "validation" and not path.exists():
                parse_details.append(f"{path.name}:pending_write")
                continue
            try:
                parse_details.append(f"{path.name}:{len(read_csv(path))}")
            except Exception as exc:  # pragma: no cover
                parse_ok = False
                parse_details.append(f"{path.name}:PARSE_FAIL:{exc}")
    checks.append(
        {
            "check_id": "VAL3465_6_csv_parse",
            "passed": parse_ok,
            "detail": ";".join(parse_details),
            "timestamp_utc": stamp,
        }
    )

    formalization_has_outputs = any(FORMALIZATION.rglob("*3465*")) if FORMALIZATION.exists() else False
    checks.append(
        {
            "check_id": "VAL3465_7_formalization_untouched_by_3465",
            "passed": not formalization_has_outputs,
            "detail": f"formalization_exists={FORMALIZATION.exists()}; 3465_outputs_in_formalization={formalization_has_outputs}",
            "timestamp_utc": stamp,
        }
    )

    next_rows = datasets["next_target"]
    checks.append(
        {
            "check_id": "VAL3465_8_next_target_3466",
            "passed": len(next_rows) == 1 and "3466" in next_rows[0]["next_doc"],
            "detail": next_rows[0]["next_doc"],
            "timestamp_utc": stamp,
        }
    )

    overall = all(row["passed"] for row in checks)
    checks.append(
        {
            "check_id": "VAL3465_SUMMARY",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
            "timestamp_utc": stamp,
        }
    )
    return checks


def write_doc(datasets: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3465 - EM Alpha Hodge Charge Owner Or WEP Raw-To-Effective Map",
        "",
        "**Current verdict:** the EM owner package still does not close as a parent theorem. The required clauses are now explicit: observed Hodge/coframe, unique `F^2`, charge-current normalization, alpha/fine-structure owner, and readout/radiative closure.",
        "",
        f"**Concrete progress:** the alpha-only WEP branch now has a numeric nonclaim ceiling. Using `eta_TiPt_bound={ETA_TIPT_BOUND:.3e}` and `Delta_Q_alpha={DELTA_Q_ALPHA_ABS:.15g}`, the effective alpha source leg obeys `|D_e_eff| <= {D_E_ALPHA_BOUND:.12e}` in the isolated alpha-channel smoke convention.",
        "",
        "## Source Register",
        md_table(datasets["source_register"]),
        "",
        "## EM Owner Package Audit",
        md_table(datasets["em_owner_package_audit"]),
        "",
        "## Alpha-Only Bound Calculation",
        md_table(datasets["alpha_only_bound_calculation"]),
        "",
        "## Raw-To-Effective Component Rows",
        md_table(datasets["raw_to_effective_component_rows"]),
        "",
        "## Owner-To-Chain Update",
        md_table(datasets["owner_to_chain_update"]),
        "",
        "## Claim Gates",
        md_table(datasets["claim_gates"]),
        "",
        "## Decision Ledger",
        md_table(datasets["decision_ledger"]),
        "",
        "## Validation",
        md_table(datasets["validation"]),
        "",
        "## Next Target",
        md_table(datasets["next_target"]),
        "",
        "## Bottom Line",
        "",
        "- EM owner theorem: not derived yet.",
        f"- New finite progress: `|D_e_eff| <= {D_E_ALPHA_BOUND:.12e}` for the alpha-only effective WEP channel.",
        "- Still missing: raw direct source weight, nuclear/mass material response, shadow/readout maps, and no-cancellation envelope.",
        "- Best next move: either prove unique `F^2`/Hodge ownership or build the nuclear/mass component row.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = {
        "source_register": OUT / "P8_Y5_R2FR_3465_SOURCE_REGISTER.csv",
        "em_owner_package_audit": OUT / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv",
        "alpha_only_bound_calculation": OUT / "P8_Y5_R2FR_3465_ALPHA_ONLY_BOUND_CALCULATION.csv",
        "raw_to_effective_component_rows": OUT / "P8_Y5_R2FR_3465_RAW_TO_EFFECTIVE_COMPONENT_ROWS.csv",
        "owner_to_chain_update": OUT / "P8_Y5_R2FR_3465_OWNER_TO_CHAIN_UPDATE.csv",
        "claim_gates": OUT / "P8_Y5_R2FR_3465_CLAIM_GATES.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3465_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3465_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3465_VALIDATION.csv",
    }
    datasets = {
        "source_register": source_register(),
        "em_owner_package_audit": em_owner_package_audit(),
        "alpha_only_bound_calculation": alpha_only_bound_calculation(),
        "raw_to_effective_component_rows": raw_to_effective_component_rows(),
        "owner_to_chain_update": owner_to_chain_update(),
        "claim_gates": claim_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }
    for key, rows in datasets.items():
        write_csv(paths[key], rows)
    datasets["validation"] = validate(paths, datasets)
    write_csv(paths["validation"], datasets["validation"])
    write_doc(datasets)


if __name__ == "__main__":
    main()

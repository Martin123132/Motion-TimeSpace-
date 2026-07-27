from __future__ import annotations

import csv
import math
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3993"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3993-Y5-R2FR-DD-proxy-to-parent-basis-map-or-source-weight-zero.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3993_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3993_PARENT_DD_MAP_THEOREM.csv",
    "zero": SRC / "P8_Y5_R2FR_3993_UNIVERSAL_HILBERT_ZERO_ROUTE.csv",
    "components": SRC / "P8_Y5_R2FR_3993_PARENT_TO_DD_COMPONENT_BASIS.csv",
    "em": SRC / "P8_Y5_R2FR_3993_EM_POYNTING_MAP_LEDGER.csv",
    "cases": SRC / "P8_Y5_R2FR_3993_DD_PROXY_BOUND_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_3993_DD_PROXY_BOUND_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_3993_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3993_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3993_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3993_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3993_VALIDATION.csv",
}

NEXT_DOC = "3994-Y5-R2FR-no-extra-F2-operator-domain-or-finite-EM-DD-coefficient-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3994_no_extra_F2_operator_domain_or_finite_EM_DD_coefficient_bound.py"

DD_COMPONENTS = ["Q_hatm_full", "Q_delta_m", "Q_m_e", "Q_e_full"]
EARTH_COMPONENTS = ["Q_hatm_full_Earth", "Q_delta_m_Earth", "Q_m_e_Earth", "Q_e_full_Earth"]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3993_00_3992_next", SRC / "P8_Y5_R2FR_3992_NEXT_TARGET.csv", "NEXT3992_0", "3992 handoff"),
        ("SRC3993_01_3992_theorem", SRC / "P8_Y5_R2FR_3992_WEP_EFFECTIVE_NORMALIZATION_THEOREM.csv", "WEN3992_2_raw_tau_factorization", "3992 raw tau law"),
        ("SRC3993_02_3992_proxy", SRC / "P8_Y5_R2FR_3992_MATERIAL_EARTH_DD_PROXY_DENOMINATOR.csv", "DDP3992_coeff_bound", "3992 DD proxy coefficient bound"),
        ("SRC3993_03_3487_bridge", SRC / "P8_Y5_R2FR_3487_PARENT_TO_DD_BRIDGE_DERIVATION.csv", "BRIDGE3487_4_parent_bridge_equation", "parent-to-DD bridge equation"),
        ("SRC3993_04_3267_signature", SRC / "P8_Y5_R2FR_3267_PARENT_DD_SIGNATURE_THEOREM.csv", "SIG3267_0_parent_low_energy_vector", "parent low-energy DD signature"),
        ("SRC3993_05_3544_map", SRC / "P8_Y5_R2FR_3544_MTS_TO_DD_SOURCE_MAP.csv", "MAP3544_4_absolute_no_cancellation", "MTS-to-DD absolute envelope"),
        ("SRC3993_06_3544_status", SRC / "P8_Y5_MTS_to_DD_source_map_status.csv", "STAT3544_0_map", "MTS-to-DD map status"),
        ("SRC3993_07_3562_nohom", SRC / "P8_Y5_R2FR_3562_NO_SOURCE_ONLY_HOM_THEOREM.csv", "NH3562_1_noHom_relative_weight_theorem", "no-source-only Hom theorem"),
        ("SRC3993_08_3990_nohom", SRC / "P8_Y5_R2FR_3990_NO_HOM_GRAMMAR_THEOREM.csv", "NHG3990_0_target", "3990 no-Hom grammar"),
        ("SRC3993_09_3251_naturality", SRC / "P8_Y5_R2FR_3251_NOHOM_CONNECTED_NATURALITY_THEOREM.csv", "NHE3251_3_connected_graph", "connected naturality collapse"),
        ("SRC3993_10_material_class", SRC / "P8_Y5_R2FR_3872_MATERIAL_SOURCE_CLASS_MAP.csv", "MAT3872_4_poynting_radiation", "material/Poynting source classes"),
        ("SRC3993_11_poynting", SRC / "P8_Y5_R2FR_3502_EM_POYNTING_SOURCE_FLUX_VECTOR.csv", "EMF3502_1_radiative_poynting_flux", "Poynting flux residual"),
        ("SRC3993_12_maxwell_norm", SRC / "P8_Y5_R2FR_3863_MAXWELL_NORMALIZATION_OWNER_THEOREM.csv", "MNO3863_2_normalization_owner_theorem", "Maxwell normalization theorem"),
        ("SRC3993_13_maxwell_stress", SRC / "P8_Y5_R2FR_3883_MAXWELL_STRESS_POYNTING_DERIVATION.csv", "MX3883_4_poynting", "Maxwell/Poynting stress accounting"),
        ("SRC3993_14_arena_stack", SRC / "P8_Y5_R2FR_3914_LOCAL_GR_NEWTON_MAXWELL_ARENA_STACK.csv", "ARE3914_2_Maxwell", "local GR/Newton/Maxwell stack"),
        ("SRC3993_15_component_rows", SRC / "P8_Y5_R2FR_3650_BETA_SOURCE_ALPHA_ROWS.csv", "BSA3650_7_total_guard", "EM/source alpha component vector"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": exists,
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def readout_interval() -> tuple[float, float]:
    rows = read_csv(SRC / "P8_Y5_R2FR_3262_TAU_WEP_FACTORIZATION.csv")
    for row in rows:
        if row.get("tau_id") == "TAU3262_1_readout_X":
            text = row["numeric_status"]
            left, _, right = text.partition("<= tau_readout_X <=")
            return float(left.strip()), float(right.strip())
    raise RuntimeError("TAU3262_1_readout_X missing")


def eta_bound() -> float:
    rows = read_csv(SRC / "P8_Y5_R2FR_3991_REAL_SOURCE_WEIGHT_BOUND_ANCHORS.csv")
    for row in rows:
        if row.get("anchor_id") == "ANCH3991_0_WEP_MICROSCOPE_product":
            return float(row["real_observable_bound"])
    raise RuntimeError("3991 WEP anchor missing")


def material_rows() -> dict[str, dict[str, str]]:
    rows = read_csv(SRC / "P8_Y5_R2FR_3473_FULL_DD_MATERIAL_ROWS.csv")
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        if row.get("material_id") in {"PtRh10", "TA6V"} and row.get("arena") == "MICROSCOPE_TIPT_EARTH_FIELD":
            out[row["material_id"]] = row
    if set(out) != {"PtRh10", "TA6V"}:
        raise RuntimeError("MICROSCOPE DD material rows missing")
    return out


def earth_row() -> dict[str, str]:
    rows = read_csv(SRC / "P8_Y5_R2FR_3482_EARTH_FULL_DD_SOURCE_VECTOR_NONCLAIM.csv")
    for row in rows:
        if row.get("source_vector_id") == "EARTH3482_0_bulk_full_DD_four_charge":
            return row
    raise RuntimeError("Earth DD source vector missing")


def dd_proxy() -> dict[str, Any]:
    mats = material_rows()
    earth = earth_row()
    delta: dict[str, float] = {}
    source: dict[str, float] = {}
    product: dict[str, float] = {}
    dot = 0.0
    for material_key, earth_key in zip(DD_COMPONENTS, EARTH_COMPONENTS):
        delta[material_key] = float(mats["TA6V"][material_key]) - float(mats["PtRh10"][material_key])
        source[material_key] = float(earth[earth_key])
        product[material_key] = delta[material_key] * source[material_key]
        dot += product[material_key]
    low, high = readout_interval()
    abs_dot = abs(dot)
    return {
        "delta": delta,
        "source": source,
        "product": product,
        "dot": dot,
        "abs_dot": abs_dot,
        "readout_low": low,
        "readout_high": high,
        "tau_low": low * abs_dot,
        "tau_high": high * abs_dot,
        "eta_bound": eta_bound(),
        "single_coeff_bound": eta_bound() / (low * abs_dot) if abs_dot > 0 else math.inf,
    }


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "PDM3993_0_chain_rule_map",
            "claim_piece": "parent-to-DD chain-rule map",
            "mathematical_form": "If the parent generator X changes low-energy constants theta_i=(mhat/Lambda_QCD, delta_m/Lambda_QCD, m_e/Lambda_QCD, alpha_EM), then C_i:=L_X ln theta_i and eta_AB^DD=tau_readout * sum_i Q_E^i DeltaQ_AB^i C_i + R_parent_to_DD.",
            "derived_result": "the DD proxy is promoted only by a parent-owned coefficient vector C_i and a residual R_parent_to_DD",
            "status": "EXACT_CONDITIONAL_CHAIN_RULE_MAP_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PDM3993_1_universal_Hilbert_zero",
            "claim_piece": "universal Hilbert source zero route",
            "mathematical_form": "If the parent source coupling is only E_munu=kappa_common T_H_munu with one observed coframe, one action-density line, no source/species Hom, no independent low-energy-constant vertex and no readout/worldtube re-entry, then C_i^relative=0 and eta_AB^DD=0 for WEP source-weight channels.",
            "derived_result": "the DD/WEP relative channel is theorem-zero under the Hilbert-universal branch rather than bounded by material data",
            "status": "EXACT_CONDITIONAL_ZERO_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PDM3993_2_finite_vector_if_zero_fails",
            "claim_piece": "finite parent coefficient vector",
            "mathematical_form": "If the zero route fails, the no-cancellation envelope is |eta_AB| <= tau_readout * sum_i |Q_E^i DeltaQ_AB^i C_i| + |R_nonDD| + |R_readout| + |R_Poynting|.",
            "derived_result": "any nonzero parent-to-DD map must enter as explicit C_i and residual rows",
            "status": "FINITE_VECTOR_BOUND_LAW_DERIVED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PDM3993_3_EM_Poynting_split",
            "claim_piece": "EM/Poynting split",
            "mathematical_form": "Minimal stationary Maxwell stress is inside T_H and contributes common Hilbert mass; independent F^2 normalization, alpha_EM drift, material EM binding response, or boundary Poynting flux populate C_alpha/R_Poynting residuals.",
            "derived_result": "Poynting is not ignored: it is either counted once in Hilbert stress or retained as a finite WEP/source residual",
            "status": "EM_POYNTING_ROUTE_LOCALIZED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def zero_route_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "ZDD3993_0_single_Hilbert_source",
            "required_clause": "active source is the total Hilbert stress only",
            "mathematical_role": "removes independent species/material active-source weights",
            "current_status": "CONDITIONAL_FROM_3988_3990_NOT_PARENT_SIGNED",
            "source_path": str(SRC / "P8_Y5_R2FR_3990_NO_HOM_GRAMMAR_THEOREM.csv"),
            "closes_if_signed": "Delta_w_species and DD relative source channel",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "ZDD3993_1_connected_action_line",
            "required_clause": "ordinary matter sectors live on one connected action-density/source graph",
            "mathematical_role": "collapses relative weights to a common calibration",
            "current_status": "EXACT_CONDITIONAL_CONNECTED_NATURALITY_UNSIGNED",
            "source_path": str(SRC / "P8_Y5_R2FR_3251_NOHOM_CONNECTED_NATURALITY_THEOREM.csv"),
            "closes_if_signed": "relative material prefactors",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "ZDD3993_2_no_constant_vertex",
            "required_clause": "no parent vertical generator changes SM constants differently by material channel",
            "mathematical_role": "sets C_hatm=C_delta_m=C_me=C_alpha=0 for WEP relative response",
            "current_status": "NOT_PARENT_SIGNED",
            "source_path": str(SRC / "P8_Y5_R2FR_3267_PARENT_DD_SIGNATURE_THEOREM.csv"),
            "closes_if_signed": "parent-to-DD coefficient vector",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "ZDD3993_3_Maxwell_owner",
            "required_clause": "minimal same-coframe Maxwell stress with no extra F2/alpha/readout/Poynting leakage",
            "mathematical_role": "keeps EM binding and Poynting in common Hilbert source or bounded flux",
            "current_status": "CONDITIONAL_THEOREM_OPEN_EXTRA_F2_AND_FLUX",
            "source_path": str(SRC / "P8_Y5_R2FR_3863_MAXWELL_NORMALIZATION_OWNER_THEOREM.csv"),
            "closes_if_signed": "C_alpha, w_EM, Phi_EM_rad residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "ZDD3993_4_verdict",
            "required_clause": "all zero clauses signed together",
            "mathematical_role": "permits eta_DD_source=0 without using MICROSCOPE bound inversion",
            "current_status": "ZERO_ROUTE_NOT_CURRENT_CLAIM",
            "source_path": str(SRC / "P8_Y5_R2FR_3562_NO_SOURCE_ONLY_HOM_THEOREM.csv"),
            "closes_if_signed": "source-weight WEP branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def component_rows(timestamp: str) -> list[dict[str, Any]]:
    proxy = dd_proxy()
    rows: list[dict[str, Any]] = []
    component_specs = [
        ("C_common_Hilbert", "universal_d_g_common", "common Hilbert source calibration", "cancels in TA6V-PtRh10 relative channel", "COMMON_MODE_ONLY"),
        ("C_hatm", "Q_hatm_full", "average light-quark/QCD-scale response", "DeltaQ_hatm * Q_Earth_hatm * C_hatm", "PARENT_COEFFICIENT_MISSING"),
        ("C_delta_m", "Q_delta_m", "isospin-breaking mass response", "DeltaQ_delta_m * Q_Earth_delta_m * C_delta_m", "PARENT_COEFFICIENT_MISSING"),
        ("C_me", "Q_m_e", "electron-mass response", "DeltaQ_m_e * Q_Earth_m_e * C_me", "PARENT_COEFFICIENT_MISSING"),
        ("C_alpha_EM", "Q_e_full", "EM/Coulomb/fine-structure response", "DeltaQ_e * Q_Earth_e * C_alpha_EM", "PARENT_EM_COEFFICIENT_MISSING"),
        ("C_nonDD_material", "R_nonDD", "nuclear/surface/material marker residual outside DD proxy", "absolute residual row, not projected into DD denominator", "FINITE_RESIDUAL_REQUIRED"),
        ("C_readout_boundary", "R_readout", "readout/worldtube/boundary selector residual", "absolute residual row", "FINITE_RESIDUAL_REQUIRED"),
        ("C_Poynting_flux", "R_Poynting", "radiative/background Poynting flux source leakage", "absolute flux/source drift residual", "FINITE_OR_ZERO_FLUX_REQUIRED"),
    ]
    for row_id, (symbol, dd_basis, meaning, formula, status) in enumerate(component_specs):
        if dd_basis in DD_COMPONENTS:
            coefficient_weight = proxy["product"][dd_basis]
            single_channel_bound = proxy["eta_bound"] / (proxy["readout_low"] * abs(coefficient_weight)) if coefficient_weight != 0 else math.inf
        else:
            coefficient_weight = ""
            single_channel_bound = ""
        rows.append(
            {
                "component_id": f"PDM3993_{row_id}_{symbol}",
                "parent_symbol": symbol,
                "dd_or_residual_basis": dd_basis,
                "meaning": meaning,
                "eta_contribution": formula,
                "coefficient_weight_TA6V_PtRh10_Earth": coefficient_weight,
                "single_channel_bound_if_only_component": single_channel_bound,
                "current_status": status,
                "source_path": str(SRC / "P8_Y5_R2FR_3544_MTS_TO_DD_SOURCE_MAP.csv"),
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def em_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "em_id": "EMDD3993_0_minimal_bound_stress",
            "channel": "bound_EM_field_stress",
            "map_to_DD_or_source": "inside total Hilbert source/common mass if same observed Hodge and stationary worldtube",
            "zero_or_bound": "zero relative WEP residual; not zero total mass contribution",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "source_path": str(SRC / "P8_Y5_R2FR_3883_MAXWELL_STRESS_POYNTING_DERIVATION.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "em_id": "EMDD3993_1_independent_F2_or_alpha",
            "channel": "nonminimal_F2_alpha_source",
            "map_to_DD_or_source": "C_alpha_EM/Q_e_full plus possible clock/source-normalization residual",
            "zero_or_bound": "requires no-extra-F2/operator-domain theorem or finite C_alpha bound",
            "status": "NEXT_BEST_GATE",
            "source_path": str(SRC / "P8_Y5_R2FR_3863_MAXWELL_NORMALIZATION_OWNER_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "em_id": "EMDD3993_2_radiative_poynting",
            "channel": "boundary_Poynting_flux",
            "map_to_DD_or_source": "R_Poynting source-mass/source-drift residual, not a material DD charge unless stationary-averaged into source response",
            "zero_or_bound": "closed stationary source worldtube or finite flux bound",
            "status": "RETAINED_FLUX_COEFFICIENT_REQUIRED",
            "source_path": str(SRC / "P8_Y5_R2FR_3502_EM_POYNTING_SOURCE_FLUX_VECTOR.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "em_id": "EMDD3993_3_internal_Lorentz_exchange",
            "channel": "matter_EM_internal_exchange",
            "map_to_DD_or_source": "zero in total Hilbert stress if matter and EM current are varied in the same parent action",
            "zero_or_bound": "same current owner and total-stress conservation",
            "status": "CONDITIONAL_ZERO_IN_TOTAL_STRESS",
            "source_path": str(SRC / "P8_Y5_R2FR_3502_EM_POYNTING_SOURCE_FLUX_VECTOR.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    proxy = dd_proxy()
    coeff = proxy["single_coeff_bound"]
    return [
        {
            "case_id": "CASE3993_0_universal_Hilbert_zero",
            "route": "zero_theorem",
            "coefficient": 0.0,
            "coefficient_bound": coeff,
            "parent_map_status": "CONDITIONAL_ZERO_PARENT_UNSIGNED",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3993_1_DD_proxy_unit_map_bound",
            "route": "DD_proxy_unit_map",
            "coefficient": coeff,
            "coefficient_bound": coeff,
            "parent_map_status": "TOY_K_PARENT_TO_DD_EQUALS_ONE_NOT_EVIDENCE",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3993_2_small_finite_vector_smoke",
            "route": "finite_vector_smoke",
            "coefficient": 0.25 * coeff,
            "coefficient_bound": coeff,
            "parent_map_status": "NUMERIC_SMOKE_ONLY_NOT_EVIDENCE",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3993_3_missing_parent_map",
            "route": "raw_MTS_parent_map",
            "coefficient": "",
            "coefficient_bound": coeff,
            "parent_map_status": "MISSING_PARENT_TO_DD_MAP",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3993_4_EM_Poynting_open",
            "route": "EM_Poynting_residual",
            "coefficient": "",
            "coefficient_bound": coeff,
            "parent_map_status": "MISSING_NO_EXTRA_F2_OR_FLUX_BOUND",
            "timestamp_utc": timestamp,
        },
    ]


def evaluate_case(row: dict[str, Any]) -> dict[str, Any]:
    proxy = dd_proxy()
    coeff_text = str(row["coefficient"])
    coeff_bound = float(row["coefficient_bound"])
    result: dict[str, Any] = {
        "case_id": row["case_id"],
        "route": row["route"],
        "input_status": row["parent_map_status"],
        "eta_bound_abs": proxy["eta_bound"],
        "tau_proxy_low": proxy["tau_low"],
        "coefficient": "MISSING",
        "eta_proxy_abs": "MISSING",
        "coefficient_bound": f"{coeff_bound:.12e}",
        "passes_proxy_bound": False,
        "score_ready": False,
        "claim_allowed": False,
        "valid_for_claim": False,
    }
    if coeff_text == "":
        return result
    coeff = float(coeff_text)
    eta_proxy = abs(coeff) * proxy["tau_low"]
    result.update(
        {
            "coefficient": f"{coeff:.12e}",
            "eta_proxy_abs": f"{eta_proxy:.12e}",
            "passes_proxy_bound": eta_proxy <= proxy["eta_bound"] * (1.0 + 1.0e-12),
        }
    )
    return result


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows = [evaluate_case(row) for row in cases]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    proxy = dd_proxy()
    return [
        {
            "decision_id": "DEC3993_0",
            "finding": "parent-to-DD map has an exact chain-rule normal form",
            "evidence": "C_i=L_X ln theta_i and eta=tau_readout sum_i Q_E^i DeltaQ_AB^i C_i + residuals",
            "limitation": "the parent does not yet supply C_i from MTS primitives",
            "next_action": "attack no-extra-F2/operator-domain first because EM/Poynting is the sharpest live coefficient route",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3993_1",
            "finding": "DD proxy gives a finite comparator coefficient bound",
            "evidence": f"|C_DD_proxy| <= {proxy['single_coeff_bound']:.12e} if K_parent_to_DD=1",
            "limitation": "K_parent_to_DD=1 is a toy/proxy assumption, not parent-owned",
            "next_action": "either prove universal Hilbert/no-Hom zero, or source the finite C_i vector",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM3993_0_no_raw_DD_claim",
            "claim": "raw MTS parent-to-DD source-weight map is derived",
            "allowed": False,
            "reason": "chain-rule form exists but parent coefficients C_i are not supplied by a signed parent action",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3993_1_no_WEP_pass",
            "claim": "MTS passes MICROSCOPE WEP source-weight bound",
            "allowed": False,
            "reason": "zero theorem is unsigned and finite coefficient vector is missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3993_2_no_EM_closure",
            "claim": "EM/Poynting source route is closed",
            "allowed": False,
            "reason": "minimal Maxwell stress route is conditional, while no-extra-F2 and radiative flux bounds remain open",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3993_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "prove the no-extra-F2/operator-domain clause for EM source normalization or build the first finite EM/DD coefficient bound",
            "success_condition": "C_alpha_EM/w_EM/Phi_EM_rad is theorem-zero or converted into a numeric/source-backed coefficient row against the 3993 DD proxy bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PARENT_DD_CHAIN_RULE_AND_ZERO_ROUTE_DERIVED_EM_POYNTING_GATE_LOCALIZED",
            "headline": "DD proxy is now either comparator-only, theorem-zero via Hilbert/no-Hom universality, or a finite parent coefficient vector with EM/Poynting exposed",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    proxy = dd_proxy()
    found = sum(bool(row["needle_found"]) for row in sources)
    lines = [
        "# 3993 - DD Proxy To Parent Basis Map Or Source-Weight Zero",
        "",
        f"Timestamp: `{timestamp}`",
        "",
        "## Result",
        "",
        "This checkpoint turns the DD proxy into a parent-map gate instead of leaving it as a loose comparator.",
        "",
        "The exact normal form is:",
        "",
        "`eta_AB^DD = tau_readout * sum_i Q_E^i DeltaQ_AB^i C_i + R_parent_to_DD`",
        "",
        "with `C_i = L_X ln theta_i` for low-energy constants `theta_i=(mhat/Lambda_QCD, delta_m/Lambda_QCD, m_e/Lambda_QCD, alpha_EM)`.",
        "",
        "## Zero Route",
        "",
        "If MTS source coupling is only the total Hilbert stress with one observed coframe, one action-density line, no source/species Hom, no independent low-energy-constant vertex, and no readout/worldtube re-entry, then the relative DD/WEP channel is zero:",
        "",
        "`C_i^relative = 0`, hence `eta_AB^DD = 0`.",
        "",
        "This is still conditional, not a current claim.",
        "",
        "## Finite Route",
        "",
        "If the zero route fails, every nonzero parent-to-DD path must enter the finite vector:",
        "",
        "`|eta_AB| <= tau_readout * sum_i |Q_E^i DeltaQ_AB^i C_i| + |R_nonDD| + |R_readout| + |R_Poynting|`.",
        "",
        f"The current DD proxy bound remains `|C_DD_proxy| <= {proxy['single_coeff_bound']:.12e}` only under the nonclaim toy assumption `K_parent_to_DD=1`.",
        "",
        "## EM/Poynting Route",
        "",
        "Bound, stationary Maxwell stress belongs inside the Hilbert source once. Independent `F^2` normalization, `alpha_EM` drift, material EM binding response, or radiative Poynting flux become explicit residual coefficients.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: status `{row['input_status']}`, eta_proxy `{row['eta_proxy_abs']}`, passes={row['passes_proxy_bound']}, claim={row['claim_allowed']}"
        )
    lines.extend(
        [
            "",
            "## Current Closure Gate",
            "",
            "The narrow next target is the EM operator-domain/no-extra-F2 gate, because it controls the most concrete visible-sector route into `C_alpha_EM`, material EM binding, and Poynting/source normalization.",
            "",
            "## Source Register",
            "",
            f"`{found}/{len(sources)}` source needles found.",
        ]
    )
    for row in sources:
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` needle `{row['needle']}` found={row['needle_found']}"
        )
    lines.extend(
        [
            "",
            "## Next Target",
            "",
            f"`{NEXT_DOC}`",
            "",
            "Prove the no-extra-F2/operator-domain clause or build the first finite EM/DD coefficient bound.",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def update_spine(timestamp: str) -> None:
    proxy = dd_proxy()
    header = "## 3993 - DD Parent Map And EM/Poynting Gate"
    block = "\n".join(
        [
            "",
            header,
            "",
            f"- Timestamp: `{timestamp}`",
            "- Status: `PARENT_DD_CHAIN_RULE_AND_ZERO_ROUTE_DERIVED_EM_POYNTING_GATE_LOCALIZED`",
            "- Exact chain rule:",
            "  `eta_AB^DD = tau_readout * sum_i Q_E^i DeltaQ_AB^i C_i + R_parent_to_DD`, with `C_i=L_X ln theta_i`.",
            "- Zero route:",
            "  universal Hilbert source + no-Hom/action-line/readout closure gives `C_i^relative=0` and kills the DD/WEP source-weight channel.",
            "- Finite route:",
            f"  DD proxy comparator gives `|C_DD_proxy| <= {proxy['single_coeff_bound']:.12e}` only if a future parent map identifies the DD proxy coefficient.",
            "- EM/Poynting:",
            "  minimal stationary Maxwell stress is Hilbert source; independent `F^2`, `alpha_EM`, material EM binding, or Poynting flux are explicit residual coefficients.",
            f"- Next: `{NEXT_DOC}`.",
            "",
        ]
    )
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    if header not in existing:
        SPINE_PATH.write_text(existing.rstrip() + block, encoding="utf-8")


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    zero: list[dict[str, Any]],
    components: list[dict[str, Any]],
    em: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": timestamp})

    proxy = dd_proxy()
    add("VAL3993_00_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3993_01_needles_found", all(row["needle_found"] for row in sources), "every cited source needle found")
    add("VAL3993_02_chain_rule", any(row["theorem_id"] == "PDM3993_0_chain_rule_map" for row in theorem), "chain-rule map theorem present")
    add("VAL3993_03_zero_route", any(row["theorem_id"] == "PDM3993_1_universal_Hilbert_zero" for row in theorem), "universal Hilbert zero theorem present")
    add("VAL3993_04_finite_law", any(row["theorem_id"] == "PDM3993_2_finite_vector_if_zero_fails" for row in theorem), "finite vector law present")
    add("VAL3993_05_zero_clauses", len(zero) >= 5, "zero route clause rows present")
    add("VAL3993_06_components", len(components) >= 8, "parent-to-DD component basis rows present")
    add("VAL3993_07_component_has_alpha", any(row["parent_symbol"] == "C_alpha_EM" for row in components), "EM alpha component row present")
    add("VAL3993_08_component_has_poynting", any(row["parent_symbol"] == "C_Poynting_flux" for row in components), "Poynting component row present")
    add("VAL3993_09_em_rows", len(em) >= 4, "EM/Poynting ledger rows present")
    add("VAL3993_10_proxy_bound_finite", math.isfinite(proxy["single_coeff_bound"]) and proxy["single_coeff_bound"] > 0.0, "DD proxy coefficient bound finite")
    zero_case = next(row for row in results if row["case_id"] == "CASE3993_0_universal_Hilbert_zero")
    unit_case = next(row for row in results if row["case_id"] == "CASE3993_1_DD_proxy_unit_map_bound")
    missing_case = next(row for row in results if row["case_id"] == "CASE3993_3_missing_parent_map")
    em_case = next(row for row in results if row["case_id"] == "CASE3993_4_EM_Poynting_open")
    add("VAL3993_11_zero_case", zero_case["eta_proxy_abs"] != "MISSING" and float(zero_case["eta_proxy_abs"]) == 0.0, "zero case evaluates to eta=0")
    add("VAL3993_12_unit_proxy_case", str(unit_case["passes_proxy_bound"]).lower() == "true" and str(unit_case["valid_for_claim"]).lower() == "false", "unit proxy case passes only nonclaim")
    add("VAL3993_13_missing_blocks", missing_case["eta_proxy_abs"] == "MISSING" and str(missing_case["passes_proxy_bound"]).lower() == "false", "missing parent map blocks")
    add("VAL3993_14_em_blocks", em_case["eta_proxy_abs"] == "MISSING" and str(em_case["passes_proxy_bound"]).lower() == "false", "EM/Poynting open branch blocks")
    add("VAL3993_15_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL3993_16_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL3993_17_doc_exists", DOC_PATH.exists() and "EM/Poynting Route" in read_text(DOC_PATH), "document written")
    add("VAL3993_18_spine_updated", SPINE_PATH.exists() and "## 3993 - DD Parent Map And EM/Poynting Gate" in read_text(SPINE_PATH), "spine updated")
    add("VAL3993_19_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL3993_20_compile", compile_ok, "script compiles")
    add("VAL3993_21_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL3993_22_status_exists", OUTPUTS["status"].exists(), "status file exists")
    add("VAL3993_23_results_nonclaim", not any(str(row["valid_for_claim"]).lower() == "true" for row in results), "all evaluator results remain nonclaim")
    return rows


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    zero = zero_route_rows(timestamp)
    components = component_rows(timestamp)
    em = em_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decision = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["zero"], zero)
    write_csv(OUTPUTS["components"], components)
    write_csv(OUTPUTS["em"], em)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["claim_gate"], claim_gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    update_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validation = build_validation_rows(timestamp, sources, theorem, zero, components, em, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)

    failed = [row for row in validation if str(row["passed"]).lower() != "true"]
    print(f"3993 validation: {len(validation) - len(failed)}/{len(validation)} passed")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()

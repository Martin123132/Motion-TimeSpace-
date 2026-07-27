from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3472-Y5-R2FR-visible-source-owner-theorem-or-full-DD-vector-upgrade.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
ETA_TIPT_BOUND = 2.8e-15

SOURCES: dict[str, dict[str, Any]] = {
    "script_3472": {"type": "local", "path": Path(__file__).resolve(), "role": "generator"},
    "doc_3471": {"type": "local", "path": ROOT / "3471-Y5-R2FR-bme-clock-material-row-or-electron-mass-zero-theorem.md", "role": "3471 handoff"},
    "next_3471": {"type": "local", "path": OUT / "P8_Y5_R2FR_3471_NEXT_TARGET.csv", "role": "3472 target statement"},
    "contract_3469": {"type": "local", "path": OUT / "P8_Y5_R2FR_3469_VISIBLE_COEFFICIENT_OWNER_CONTRACT.csv", "role": "visible coefficient owner contract"},
    "vector_3468": {"type": "local", "path": OUT / "P8_Y5_R2FR_3468_RETAINED_COEFFICIENT_VECTOR.csv", "role": "retained coefficient vector"},
    "theorem_3468": {"type": "local", "path": OUT / "P8_Y5_R2FR_3468_CONSTANT_SECTOR_THEOREM_ATTEMPT.csv", "role": "visible constant theorem attempt"},
    "hom_3468": {"type": "local", "path": OUT / "P8_Y5_R2FR_3468_HIDDEN_TO_SM_COEFFICIENT_MORPHISM_GATES.csv", "role": "hidden-to-visible morphism gates"},
    "grammar_2612": {"type": "local", "path": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_PREFACTOR_CLASSIFICATION.csv", "role": "direct matter/source-prefactor status"},
    "typing_2650": {"type": "local", "path": OUT / "P8_Y5_SOURCE_PREF_OBJECTLANG_2650_SOURCE_PREFACTOR_TYPING_GATE.csv", "role": "object-language typing gate"},
    "dd_tex": {"type": "local", "path": ROOT / "source-intake" / "external-sources" / "damour_donoghue_1007.2792_source" / "DamourDonoghueEPfinal.tex", "role": "Damour-Donoghue full four-charge formulas"},
    "element_3264": {"type": "local", "path": OUT / "P8_Y5_R2FR_3264_DD_ELEMENT_CHARGES_NONCLAIM.csv", "role": "MICROSCOPE alloy element A/Z inputs"},
    "material_3264": {"type": "local", "path": OUT / "P8_Y5_R2FR_3264_DD_MATERIAL_CHARGES_NONCLAIM.csv", "role": "previous reduced two-charge alloy averages"},
    "composition_1909": {"type": "local", "path": OUT / "P8_Y5_PARENT_QLOC_1909_TIPT_ALLOY_COMPOSITION_SOURCE_BACKED_NONCLAIM.csv", "role": "source-backed MICROSCOPE alloy composition"},
    "material_3312": {"type": "local", "path": OUT / "P8_Y5_R2FR_3312_UPGRADED_MATERIAL_CHARGES.csv", "role": "upgraded material charge proxy ledger"},
    "pair_3312": {"type": "local", "path": OUT / "P8_Y5_R2FR_3312_UPGRADED_PAIR_DELTAS.csv", "role": "upgraded pair charge proxy ledger"},
    "arena_3470": {"type": "local", "path": OUT / "P8_Y5_R2FR_3470_ARENA_CONFIG_TEMPLATE.csv", "role": "MICROSCOPE eta bound used by current runner"},
    "bme_3471": {"type": "local", "path": OUT / "P8_Y5_R2FR_3471_WEP_VECTOR_INPUT_BME_PATCH_ROW.csv", "role": "previous b_me patch row"},
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


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
    body = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", "<br>").replace("|", "/") for field in fields]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def parse_float(value: Any) -> float | None:
    text = str(value).strip() if value is not None else ""
    if not text or "MISSING" in text or "alloy" in text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def source_register() -> list[dict[str, Any]]:
    stamp = now()
    rows: list[dict[str, Any]] = []
    for source_id, meta in SOURCES.items():
        path = meta["path"]
        rows.append(
            {
                "timestamp_utc": stamp,
                "source_id": source_id,
                "source_type": meta["type"],
                "source_path": str(path),
                "exists": path.exists(),
                "role": meta["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def visible_source_owner_attempt() -> list[dict[str, Any]]:
    contract_path = SOURCES["contract_3469"]["path"]
    return [
        {
            "attempt_id": "VSO3472_0_owner_sort",
            "claim_tested": "The visible source coefficients are parent-level data, not arena-fit afterthoughts.",
            "mathematical_form": "Theta_vis = {alpha,mhat/Lambda_3,delta_m/Lambda_3,m_e/Lambda_3,nuclear EFT coeffs,readout coeffs} in RepData_fixed union q^*C^∞(B)",
            "result": "EXACT_CONDITIONAL",
            "blocker": "VCO3469_0 remains unsigned",
            "source_path": str(contract_path),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "VSO3472_1_vertical_chain_rule",
            "claim_tested": "If visible source data descend through q, all local vertical derivatives vanish together.",
            "mathematical_form": "v in ker(Dq), Theta_vis=q^*Theta_bar => L_v Theta_vis=0",
            "result": "PROVED_CONDITIONAL_CHAIN_RULE",
            "blocker": "does not prove the premise that each visible source coefficient is q-basic",
            "source_path": str(contract_path),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "VSO3472_2_no_hidden_visible_morphism",
            "claim_tested": "No hidden MTS invariant can enter alpha, Yukawa/Higgs ratios, QCD ratios, nuclear EFT, or readout coefficients.",
            "mathematical_form": "Hom(I_hidden,Theta_vis)=empty except constants",
            "result": "NOT_PARENT_PROVED",
            "blocker": "countermodel remains: f(I_hidden) can multiply F^2, y_e H e L, quark mass ratios, or nuclear EFT terms unless the parent grammar forbids it",
            "source_path": str(SOURCES["hom_3468"]["path"]),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "VSO3472_3_source_variation_order",
            "claim_tested": "The source map is varied before WEP/clock/R10 readout, so experiments cannot create new coefficients.",
            "mathematical_form": "delta S_parent -> owned currents and coefficients -> Pi_arena",
            "result": "CLEAN_CONTRACT_NOT_COMPLETE_THEOREM",
            "blocker": "typing gate exists but parent action has not promoted it to a no-extra-source theorem",
            "source_path": str(SOURCES["typing_2650"]["path"]),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "VSO3472_SUMMARY",
            "claim_tested": "Can b_alpha, b_mhat, b_delta_m, b_me, b_bind, and b_readout be zeroed structurally?",
            "mathematical_form": "VisibleSourceOwner + readout preservation => D_hatm=D_delta=D_me=D_e=D_bind=D_readout=0",
            "result": "NO_PARENT_SIGNED_ZERO_USE_FULL_DD_VECTOR",
            "blocker": "source-owner theorem is coherent but not parent-owned; proceed with full sourced DD vector",
            "source_path": str(contract_path),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
    ]


def formula_audit() -> list[dict[str, Any]]:
    tex = SOURCES["dd_tex"]["path"].read_text(encoding="utf-8", errors="replace")
    checks = {
        "Qhatm": ("Q_{\\hat m}", "0.093", "0.036", "0.020", "1.4"),
        "Qdeltam": ("Q_{\\delta m}", "0.0017"),
        "Qme": ("Q_{m_e}", "5.5", "10^{-4}"),
        "Qe": ("Q_e", "-1.4", "8.2", "7.7"),
    }
    rows: list[dict[str, Any]] = []
    lines = tex.splitlines()
    for name, tokens in checks.items():
        line_number = ""
        for index, line in enumerate(lines, start=1):
            window = " ".join(lines[max(0, index - 2) : min(len(lines), index + 5)])
            if all(token in window for token in tokens):
                line_number = str(index)
                break
        rows.append(
            {
                "formula_id": f"DDF3472_{len(rows)}_{name}",
                "charge": name,
                "source_path": str(SOURCES["dd_tex"]["path"]),
                "line_number": line_number,
                "tokens_checked": ";".join(tokens),
                "status": "FOUND_FULL_DD_FORMULA" if line_number else "MISSING_FORMULA",
                "valid_for_claim": False,
            }
        )
    return rows


def dd_charges(A: float, Z: float) -> dict[str, float]:
    q_p = Z / A
    q_delta = (A - 2.0 * Z) / A
    q_c = Z * (Z - 1.0) / (A ** (4.0 / 3.0))
    return {
        "q_p_Z_over_A": q_p,
        "q_delta_A_minus_2Z_over_A": q_delta,
        "q_C_ZZminus1_Aminus4thirds": q_c,
        "Q_hatm_full": 0.093 - 0.036 / (A ** (1.0 / 3.0)) - 0.020 * (q_delta**2) - 1.4e-4 * q_c,
        "Q_delta_m": 0.0017 * q_delta,
        "Q_m_e": 5.5e-4 * q_p,
        "Q_e_full": (-1.4 + 8.2 * q_p + 7.7 * q_c) * 1.0e-4,
        "Qhatm_prime_reduced": -0.036 / (A ** (1.0 / 3.0)) - 1.4e-4 * q_c,
        "Qe_prime_reduced": 7.7e-4 * q_c,
    }


def element_rows() -> list[dict[str, Any]]:
    source_rows = read_csv(SOURCES["element_3264"]["path"])
    rows: list[dict[str, Any]] = []
    for source in source_rows:
        material_id = source["material_id"]
        if material_id not in {"PtRh10", "TA6V"}:
            continue
        fraction = parse_float(source["mass_fraction"])
        A = parse_float(source["A_context"])
        Z = parse_float(source["Z"])
        if fraction is None or A is None or Z is None:
            raise ValueError(f"missing element input in {source}")
        charges = dd_charges(A, Z)
        row = {
            "element_charge_id": f"EL3472_{material_id}_{source['element']}",
            "material_id": material_id,
            "element": source["element"],
            "mass_fraction": f"{fraction:.12e}",
            "A_context": f"{A:.12e}",
            "Z": f"{Z:.12e}",
            "source_path": str(SOURCES["element_3264"]["path"]),
            "formula_source_path": str(SOURCES["dd_tex"]["path"]),
            "status": "FULL_DD_FOUR_CHARGE_ELEMENT_PROXY",
            "valid_for_claim": False,
        }
        row.update({key: f"{value:.12e}" for key, value in charges.items()})
        rows.append(row)
    return rows


def material_rows(element_output_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for material_id in ["PtRh10", "TA6V"]:
        elements = [row for row in element_output_rows if row["material_id"] == material_id]
        if not elements:
            raise ValueError(f"missing element rows for {material_id}")
        fraction_sum = sum(float(row["mass_fraction"]) for row in elements)
        charge_names = [
            "q_p_Z_over_A",
            "q_delta_A_minus_2Z_over_A",
            "q_C_ZZminus1_Aminus4thirds",
            "Q_hatm_full",
            "Q_delta_m",
            "Q_m_e",
            "Q_e_full",
            "Qhatm_prime_reduced",
            "Qe_prime_reduced",
        ]
        averaged = {
            name: sum(float(row["mass_fraction"]) * float(row[name]) for row in elements)
            for name in charge_names
        }
        output = {
            "material_charge_id": f"MAT3472_{material_id}",
            "arena": "WEP_MICROSCOPE_TiPt",
            "material_id": material_id,
            "mass_fraction_sum": f"{fraction_sum:.12e}",
            "basis": "full Damour-Donoghue four-charge basis; mass-fraction alloy average; F_A=1 proxy",
            "source_path": str(OUT / "P8_Y5_R2FR_3472_DD_FOUR_CHARGE_ELEMENT_ROWS.csv"),
            "formula_source_path": str(SOURCES["dd_tex"]["path"]),
            "status": "FULL_DD_FOUR_CHARGE_MATERIAL_PROXY",
            "valid_for_claim": False,
        }
        output.update({key: f"{value:.12e}" for key, value in averaged.items()})
        rows.append(output)
    return rows


def pair_vector(material_output_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    left = next(row for row in material_output_rows if row["material_id"] == "TA6V")
    right = next(row for row in material_output_rows if row["material_id"] == "PtRh10")
    charge_names = ["Q_hatm_full", "Q_delta_m", "Q_m_e", "Q_e_full"]
    deltas = {f"Delta_{name}": float(left[name]) - float(right[name]) for name in charge_names}
    norm = math.sqrt(sum(value * value for value in deltas.values()))
    rows = [
        {
            "pair_id": "DDV3472_0_MICROSCOPE_TA6V_minus_PtRh10",
            "arena": "WEP_MICROSCOPE_TiPt",
            "left_minus_right": "TA6V_minus_PtRh10",
            **{key: f"{value:.12e}" for key, value in deltas.items()},
            "delta_vector_norm": f"{norm:.12e}",
            "eta_formula": "eta_TiPt = Delta_Q_hatm*D_hatm + Delta_Q_delta_m*D_delta_m + Delta_Q_m_e*D_me + Delta_Q_e*D_e + residual",
            "rank_single_pair": 1,
            "nullspace_dimension_in_four_channel_basis": 3,
            "source_path": str(OUT / "P8_Y5_R2FR_3472_DD_FOUR_CHARGE_MATERIAL_ROWS.csv"),
            "valid_for_claim": False,
        }
    ]
    return rows


def single_component_ceilings(pair_rows_out: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pair = pair_rows_out[0]
    mapping = [
        ("D_hatm_eff", "Delta_Q_hatm_full"),
        ("D_delta_m_eff", "Delta_Q_delta_m"),
        ("D_me_eff", "Delta_Q_m_e"),
        ("D_e_eff", "Delta_Q_e_full"),
    ]
    rows: list[dict[str, Any]] = []
    for symbol, delta_key in mapping:
        delta = abs(float(pair[delta_key]))
        ceiling = ETA_TIPT_BOUND / delta if delta > 0 else math.inf
        rows.append(
            {
                "ceiling_id": f"SCC3472_{len(rows)}_{symbol}",
                "arena": "WEP_MICROSCOPE_TiPt",
                "symbol": symbol,
                "delta_key": delta_key,
                "delta_abs": f"{delta:.12e}",
                "eta_bound_abs": f"{ETA_TIPT_BOUND:.12e}",
                "single_component_ceiling_abs": f"{ceiling:.12e}",
                "meaning": "only valid if all other DD channels and residual are zero",
                "status": "NONCLAIM_SINGLE_CHANNEL_SMOKE_CEILING",
                "valid_for_claim": False,
            }
        )
    return rows


def full_vector_runner(pair_rows_out: list[dict[str, Any]], ceilings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pair = pair_rows_out[0]
    rows: list[dict[str, Any]] = [
        {
            "result_id": "FVR3472_0_equation",
            "arena": "WEP_MICROSCOPE_TiPt",
            "observable": "eta_TiPt_abs",
            "model_form": pair["eta_formula"],
            "known_numeric_inputs": "four DD material-difference sensitivities sourced",
            "missing_live_inputs": "D_hatm_eff;D_delta_m_eff;D_me_eff;D_e_eff;direct_residual",
            "rank_status": "RANK_ONE_STRIP_IN_FOUR_CHANNEL_SPACE",
            "row_status": "SCHEMA_UPGRADED_NOT_PREDICTIVE",
            "valid_for_claim": False,
        }
    ]
    saturated_sum = 0.0
    for ceiling in ceilings:
        saturated_sum += ETA_TIPT_BOUND
        rows.append(
            {
                "result_id": f"FVR3472_{len(rows)}_{ceiling['symbol']}",
                "arena": "WEP_MICROSCOPE_TiPt",
                "observable": ceiling["symbol"],
                "model_form": f"{ceiling['delta_key']}*{ceiling['symbol']}",
                "known_numeric_inputs": f"{ceiling['delta_key']} abs={ceiling['delta_abs']}",
                "missing_live_inputs": ceiling["symbol"],
                "rank_status": "SINGLE_COMPONENT_PROJECTION_ONLY",
                "single_component_ceiling_abs": ceiling["single_component_ceiling_abs"],
                "saturated_abs_contribution": f"{ETA_TIPT_BOUND:.12e}",
                "row_status": "NONCLAIM_CEILING_ONLY",
                "valid_for_claim": False,
            }
        )
    rows.append(
        {
            "result_id": "FVR3472_SUMMARY",
            "arena": "WEP_MICROSCOPE_TiPt",
            "observable": "full_DD_WEP_vector",
            "model_form": "one MICROSCOPE material pair supplies one scalar strip through four source coefficients",
            "known_numeric_inputs": f"delta_vector_norm={pair['delta_vector_norm']}; eta_bound={ETA_TIPT_BOUND:.12e}",
            "missing_live_inputs": "parent-owned coefficient vector and direct residual bound",
            "rank_status": "UNDERDETERMINED_NULLSPACE_DIM_3",
            "single_component_saturated_sum_abs": f"{saturated_sum:.12e}",
            "row_status": "FAIL_BLOCKED_FULL_VECTOR_UNDERDETERMINED_NO_PARENT_COEFFICIENTS",
            "valid_for_claim": False,
        }
    )
    return rows


def claim_gates(theorem_rows: list[dict[str, Any]], formula_rows: list[dict[str, Any]], pair_rows_out: list[dict[str, Any]], runner_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    formulas_ok = all(row["status"] == "FOUND_FULL_DD_FORMULA" for row in formula_rows)
    pair = pair_rows_out[0]
    summary = next(row for row in runner_rows if row["result_id"] == "FVR3472_SUMMARY")
    return [
        {
            "gate_id": "CG3472_0_source_owner_theorem",
            "requirement": "visible source-owner theorem parent-signed",
            "passed": False,
            "evidence": next(row for row in theorem_rows if row["attempt_id"] == "VSO3472_SUMMARY")["result"],
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3472_1_full_dd_formulas",
            "requirement": "Q_hatm, Q_delta_m, Q_m_e, and Q_e formulas found in local DD source",
            "passed": formulas_ok,
            "evidence": ";".join(f"{row['charge']}:{row['status']}" for row in formula_rows),
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3472_2_pair_vector_finite",
            "requirement": "MICROSCOPE four-channel pair vector finite and nonzero",
            "passed": float(pair["delta_vector_norm"]) > 0.0,
            "evidence": f"delta_vector_norm={pair['delta_vector_norm']}",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3472_3_no_single_pair_claim",
            "requirement": "single material pair cannot claim a full four-channel bound",
            "passed": False,
            "evidence": f"{summary['rank_status']}; {summary['row_status']}",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3472_4_no_public_claim",
            "requirement": "all generated rows remain private nonclaim rows",
            "passed": True,
            "evidence": "valid_for_claim=false throughout 3472",
            "valid_for_claim": False,
        },
    ]


def decision_rows(pair_rows_out: list[dict[str, Any]], runner_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary = next(row for row in runner_rows if row["result_id"] == "FVR3472_SUMMARY")
    return [
        {
            "decision_id": "DEC3472_0_no_zero_theorem",
            "decision": "Do not zero visible source coefficients yet.",
            "rationale": "The source-owner theorem is mathematically clean but still lacks parent-action ownership clauses.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3472_1_full_vector_upgrade",
            "decision": "Replace isolated WEP coefficient thinking with the full DD four-channel vector.",
            "rationale": pair_rows_out[0]["eta_formula"],
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3472_2_wep_status",
            "decision": "WEP/local-source coupling remains blocked but is now blocked in the right basis.",
            "rationale": f"{summary['rank_status']}: {summary['missing_live_inputs']}",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3473-Y5-R2FR-full-DD-multiarena-rank-or-parent-source-owner-proof.md",
            "next_script": "scripts/Y5_R2FR_3473_full_DD_multiarena_rank_or_parent_source_owner_proof.py",
            "objective": "Either add independent WEP/clock/R10 rows to raise the full DD source-vector rank, or prove the parent source-owner theorem that makes the rank problem irrelevant by zeroing the source vector.",
            "success_gate": "Full DD matrix rank and nullspace are explicit across available arenas, or parent source-owner theorem is signed strongly enough to remove the WEP source vector.",
            "exclude": "GitHub action; formalization-workbench edits; public WEP/local-GR claim; treating single-channel ceilings as full bounds.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def formalization_git_status() -> str:
    try:
        result = subprocess.run(
            ["git", "status", "--short", "--", "formalization-workbench"],
            cwd=ROOT.parent,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError:
        return "GIT_NOT_AVAILABLE"
    if result.returncode != 0:
        if "not a git repository" in result.stderr.lower():
            return "NOT_A_GIT_REPOSITORY"
        return f"GIT_STATUS_FAILED:{result.stderr.strip()}"
    return result.stdout.strip()


def validation_rows(
    output_paths: list[Path],
    source_rows: list[dict[str, Any]],
    formula_rows: list[dict[str, Any]],
    element_output_rows: list[dict[str, Any]],
    material_output_rows: list[dict[str, Any]],
    pair_rows_out: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    malformed: list[str] = []
    for path in output_paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            read_csv(path)
        except Exception as exc:
            malformed.append(f"{path.name}:{exc}")
    missing_sources = [row["source_id"] for row in source_rows if not parse_bool(row["exists"])]
    formulas_ok = all(row["status"] == "FOUND_FULL_DD_FORMULA" for row in formula_rows)
    element_finite = all(all(math.isfinite(float(row[key])) for key in ["Q_hatm_full", "Q_delta_m", "Q_m_e", "Q_e_full"]) for row in element_output_rows)
    material_fraction_ok = all(abs(float(row["mass_fraction_sum"]) - 1.0) < 1e-9 for row in material_output_rows)
    pair = pair_rows_out[0]
    summary = next(row for row in runner_rows if row["result_id"] == "FVR3472_SUMMARY")
    formalization_outputs = [str(path) for path in output_paths if str(path).lower().startswith(str(FORMALIZATION).lower())]
    git_status = formalization_git_status()
    checks = [
        ("VAL3472_0_sources_exist", not missing_sources, ";".join(missing_sources) or "all local sources exist"),
        ("VAL3472_1_csv_parse", not malformed, ";".join(malformed) or "all output csv files parse"),
        ("VAL3472_2_formulas_found", formulas_ok, ";".join(f"{row['charge']}:{row['status']}" for row in formula_rows)),
        ("VAL3472_3_element_charges_finite", element_finite, f"element_rows={len(element_output_rows)}"),
        ("VAL3472_4_material_fraction_sums", material_fraction_ok, ";".join(f"{row['material_id']}={row['mass_fraction_sum']}" for row in material_output_rows)),
        ("VAL3472_5_pair_vector_nonzero", float(pair["delta_vector_norm"]) > 0.0, f"delta_vector_norm={pair['delta_vector_norm']}"),
        ("VAL3472_6_rank_block_preserved", summary["rank_status"] == "UNDERDETERMINED_NULLSPACE_DIM_3", summary["rank_status"]),
        ("VAL3472_7_no_claim", True, "all 3472 rows valid_for_claim=false"),
        ("VAL3472_8_no_formalization_outputs", not formalization_outputs, ";".join(formalization_outputs) or "no outputs under formalization-workbench"),
        ("VAL3472_9_git_formalization_clean", git_status in {"", "NOT_A_GIT_REPOSITORY"}, git_status or "git reports no formalization-workbench changes"),
    ]
    rows = [
        {"check_id": check_id, "passed": bool(passed), "detail": detail, "valid_for_claim": False}
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL3472_SUMMARY",
            "passed": all(parse_bool(row["passed"]) for row in rows),
            "detail": "PASS" if all(parse_bool(row["passed"]) for row in rows) else "FAIL",
            "valid_for_claim": False,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    formula_rows: list[dict[str, Any]],
    element_output_rows: list[dict[str, Any]],
    material_output_rows: list[dict[str, Any]],
    pair_rows_out: list[dict[str, Any]],
    ceilings: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    summary = next(row for row in runner_rows if row["result_id"] == "FVR3472_SUMMARY")
    pair = pair_rows_out[0]
    doc = f"""# 3472: Visible Source-Owner Theorem Or Full DD Vector Upgrade

## Current Verdict
- **Actual progress:** the WEP material/source side is now represented in the full Damour-Donoghue four-charge basis, not just isolated `b_alpha`, `b_mhat`, and `b_me` smoke rows.
- **No structural pass yet:** the source-owner theorem is coherent, but still unsigned by the parent MTS action.
- **Local/WEP coupling remains blocked in the right basis:** `{summary['rank_status']}` with `{summary['missing_live_inputs']}`.
- **MICROSCOPE pair vector:** `{pair['eta_formula']}`.

## Concrete Progress
- Generated element, material, and pair rows for `Q_hatm`, `Q_delta_m`, `Q_m_e`, and `Q_e`.
- Preserved old reduced two-charge work as a limit/proxy rather than pretending it was the full coupling story.
- Made the nullspace explicit: one MICROSCOPE material pair is one scalar strip in a four-channel coefficient space.
- Kept all outputs private/nonclaim.

## Source-Owner Theorem Attempt
{md_table(theorem_rows)}

## Full DD Formula Audit
{md_table(formula_rows)}

## Element Rows
{md_table(element_output_rows)}

## Material Rows
{md_table(material_output_rows)}

## Pair Vector
{md_table(pair_rows_out)}

## Single-Component Ceilings
{md_table(ceilings)}

## Full Vector Runner
{md_table(runner_rows)}

## Claim Gates
{md_table(gates)}

## Decision
{md_table(decisions)}

## Next Target
{md_table(next_rows)}

## Source Register
{md_table(source_rows)}

## Validation
{md_table(validation)}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register()
    theorem_rows = visible_source_owner_attempt()
    formulas = formula_audit()
    elements = element_rows()
    materials = material_rows(elements)
    pair = pair_vector(materials)
    ceilings = single_component_ceilings(pair)
    runner = full_vector_runner(pair, ceilings)
    gates = claim_gates(theorem_rows, formulas, pair, runner)
    decisions = decision_rows(pair, runner)
    next_rows = next_target()
    output_map = {
        OUT / "P8_Y5_R2FR_3472_SOURCE_REGISTER.csv": source_rows,
        OUT / "P8_Y5_R2FR_3472_VISIBLE_SOURCE_OWNER_THEOREM_ATTEMPT.csv": theorem_rows,
        OUT / "P8_Y5_R2FR_3472_DD_FOUR_CHARGE_FORMULA_AUDIT.csv": formulas,
        OUT / "P8_Y5_R2FR_3472_DD_FOUR_CHARGE_ELEMENT_ROWS.csv": elements,
        OUT / "P8_Y5_R2FR_3472_DD_FOUR_CHARGE_MATERIAL_ROWS.csv": materials,
        OUT / "P8_Y5_R2FR_3472_DD_FOUR_CHARGE_PAIR_VECTOR.csv": pair,
        OUT / "P8_Y5_R2FR_3472_WEP_FOUR_CHANNEL_SINGLE_COMPONENT_CEILINGS_NONCLAIM.csv": ceilings,
        OUT / "P8_Y5_R2FR_3472_WEP_FULL_VECTOR_RUNNER_NONCLAIM.csv": runner,
        OUT / "P8_Y5_R2FR_3472_CLAIM_GATES.csv": gates,
        OUT / "P8_Y5_R2FR_3472_DECISION_LEDGER.csv": decisions,
        OUT / "P8_Y5_R2FR_3472_NEXT_TARGET.csv": next_rows,
    }
    for path, rows in output_map.items():
        write_csv(path, rows)
    validation = validation_rows([*output_map.keys(), DOC], source_rows, formulas, elements, materials, pair, runner)
    validation_path = OUT / "P8_Y5_BRR545_3472_VALIDATION.csv"
    write_csv(validation_path, validation)
    write_doc(source_rows, theorem_rows, formulas, elements, materials, pair, ceilings, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()

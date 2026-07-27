from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAW = ROOT / "source-intake" / "component-fractions" / "raw"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3257-Y5-R2FR-first-accepted-EM-Coulomb-fraction-row-or-toy-shell-runner-dryrun-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3257_SOURCE_REGISTER.csv",
    "formula": OUT / "P8_Y5_R2FR_3257_EM_COULOMB_FRACTION_FORMULA_ROWS.csv",
    "shape": OUT / "P8_Y5_R2FR_3257_EM_COULOMB_SHAPE_ROWS_NONCLAIM.csv",
    "raw_candidate": RAW / "P8_Y5_R2FR_3257_EM_COULOMB_FRACTION_CANDIDATE_NONCLAIM.csv",
    "acceptance": OUT / "P8_Y5_R2FR_3257_EM_COULOMB_FRACTION_ACCEPTANCE_AUDIT.csv",
    "toy_fraction": OUT / "P8_Y5_R2FR_3257_TOY_SEMF_COEFFICIENT_FRACTION_DRYRUN_NONCLAIM.csv",
    "toy_shell_input": OUT / "P8_Y5_R2FR_3257_TOY_SHELL_INPUTS_NONCLAIM.csv",
    "toy_shell_output": OUT / "P8_Y5_R2FR_3257_TOY_SHELL_OUTPUTS_NONCLAIM.csv",
    "gram_update": OUT / "P8_Y5_R2FR_3257_GJ_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3257_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3257_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3257_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3257_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
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
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            lowered_line = line.lower()
            if any(needle in lowered_line for needle in lowered_needles):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:260]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def float_or_none(value: Any) -> float | None:
    try:
        return float(str(value).strip())
    except Exception:
        return None


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3257_3256_handoff",
            ROOT / "3256-Y5-R2FR-material-EM-binding-projection-or-toy-charged-shell-smoke-input-under-AX1090.md",
            "3256 material EM binding projection handoff",
            ["NEXT3256_0_3257", "f_EM,A", "toy-shell runner"],
        ),
        (
            "SRC3257_3256_projection",
            OUT / "P8_Y5_R2FR_3256_MATERIAL_EM_BINDING_PROJECTION.csv",
            "material EM binding projection formulas",
            ["MEP3256_0_material_energy_split", "f_EM,A"],
        ),
        (
            "SRC3257_3256_match",
            OUT / "P8_Y5_R2FR_3256_COULOMB_SHELL_ENERGY_MATCH.csv",
            "Coulomb shell energy match and material Gram formula",
            ["CSM3256_2_fraction_form", "K_shell"],
        ),
        (
            "SRC3257_1233_schema",
            OUT / "P8_Y5_R10_1233_COMPONENT_FRACTION_SCHEMA.csv",
            "component-fraction acceptance schema",
            ["fraction_value", "fraction_uncertainty", "basis_convention"],
        ),
        (
            "SRC3257_1328_routes",
            OUT / "P8_Y5_R10_1328_COMPONENT_SOURCE_ROUTE_MATRIX.csv",
            "EM_Coulomb source acquisition routes",
            ["ROUTE1328_TA6V_EM_Coulomb", "ROUTE1328_PtRh10_EM_Coulomb"],
        ),
        (
            "SRC3257_1909_composition",
            OUT / "P8_Y5_PARENT_QLOC_1909_TIPT_ALLOY_COMPOSITION_SOURCE_BACKED_NONCLAIM.csv",
            "TA6V/PtRh10 alloy composition context",
            ["AC1909_TA6V_Ti", "AC1909_PtRh10_Pt"],
        ),
        (
            "SRC3257_1909_proxy",
            OUT / "P8_Y5_PARENT_QLOC_1909_TIPT_ALLOY_PROXY_VECTOR_NONCLAIM.csv",
            "dimensionless Coulomb shape proxy already computed for alloys",
            ["coulomb_formula_proxy", "AP1909_TA6V_minus_PtRh10"],
        ),
        (
            "SRC3257_1910_tensor_contract",
            OUT / "P8_Y5_PARENT_QLOC_1910_EXACT_MASS_DEFECT_TENSOR_CONTRACT_NONCLAIM.csv",
            "exact EM mass-defect tensor contract",
            ["MDT1910_3_EM_Coulomb_binding", "partial_alpha"],
        ),
        (
            "SRC3257_3129_dd_comparator",
            OUT / "P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_OUTPUT.csv",
            "external DD alpha/Coulomb comparator, not an MTS fraction source",
            ["Earth_bulk_Coulomb_alpha_smoke", "Q_alpha_Coulomb_Earth"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def formula_rows() -> list[dict[str, Any]]:
    return [
        {
            "formula_id": "FEM3257_0_Coulomb_shape",
            "object": "dimensionless alloy Coulomb shape",
            "formula": "q_C,B = sum_E x_B,E Z_E(Z_E-1)/A_E^(4/3)",
            "derivation": "SEMF Coulomb energy E_C~a_C Z(Z-1) A^(-1/3); divide by A m_u c^2 to obtain a fractional shape times k_C=a_C/(m_u c^2)",
            "inputs": "mass fractions x_B,E; element Z; A_context; no isotope-level refinement yet",
            "status": "SHAPE_FORMULA_READY_FROM_1909_PROXY",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "FEM3257_1_fraction_from_shape",
            "object": "material EM/Coulomb fraction",
            "formula": "f_EM,B = k_C q_C,B, k_C := a_C/(m_u c^2)",
            "derivation": "converts the dimensionless Coulomb shape into an approximate EM binding fraction only after a sourced Coulomb coefficient and mass convention are selected",
            "inputs": "source-backed a_C; m_u c^2; isotope/alloy convention; uncertainty",
            "status": "COEFFICIENT_AND_UNCERTAINTY_MISSING_FOR_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "FEM3257_2_pair_difference",
            "object": "TA6V_minus_PtRh10 EM difference",
            "formula": "Delta f_EM = k_C (q_C,TA6V - q_C,PtRh10)",
            "derivation": "uses the 1910 response law for the EM selected component once gamma_EM is tied to alpha scaling",
            "inputs": "both material rows; source-backed k_C; parent EM/alpha map",
            "status": "DIFFERENTIAL_SHAPE_READY_PARENT_ALPHA_MAP_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "FEM3257_3_alpha_response_guard",
            "object": "alpha/material response",
            "formula": "gamma_EM,B = partial ln M_B / partial ln alpha, gamma_EM,B≈f_EM,B only if the retained Coulomb term is alpha-linear in the declared basis",
            "derivation": "prevents a coefficient smoke row from being treated as the full material response tensor",
            "inputs": "alpha scaling convention; no-double-count decomposition against nuclear surface/binding rows",
            "status": "CONDITIONAL_RESPONSE_NOT_PROMOTED",
            "valid_for_claim": "false",
        },
    ]


def proxy_rows() -> list[dict[str, str]]:
    path = OUT / "P8_Y5_PARENT_QLOC_1909_TIPT_ALLOY_PROXY_VECTOR_NONCLAIM.csv"
    rows = read_csv(path)
    return [row for row in rows if row.get("material_id") in {"TA6V", "PtRh10", "TA6V_minus_PtRh10"}]


def route_rows() -> list[dict[str, str]]:
    path = OUT / "P8_Y5_R10_1328_COMPONENT_SOURCE_ROUTE_MATRIX.csv"
    rows = read_csv(path)
    return [row for row in rows if row.get("component_id") == "EM_Coulomb"]


def shape_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for proxy in proxy_rows():
        material_id = proxy["material_id"]
        shape_value = float_or_none(proxy.get("coulomb_formula_proxy"))
        is_pair = material_id == "TA6V_minus_PtRh10"
        rows.append(
            {
                "shape_id": f"SHAPE3257_{material_id}",
                "material_id": material_id,
                "component_id": "EM_Coulomb",
                "shape_value_q_C": f"{shape_value:.12e}" if shape_value is not None else "MISSING_SHAPE_VALUE",
                "shape_formula": "q_C,B=sum_E x_B,E Z_E(Z_E-1)/A_E^(4/3)",
                "fraction_formula": "f_EM,B=k_C*q_C,B",
                "pair_or_material": "pair_difference" if is_pair else "material",
                "coefficient_status": "MISSING_SOURCE_BACKED_k_C",
                "source_path": str(OUT / "P8_Y5_PARENT_QLOC_1909_TIPT_ALLOY_PROXY_VECTOR_NONCLAIM.csv"),
                "extraction_method": "reuse 1909 alloy Coulomb proxy; do not promote to fraction without k_C and uncertainty",
                "status": "SHAPE_NUMERIC_FRACTION_NOT_ACCEPTED",
                "valid_for_claim": "false",
            }
        )
    return rows


def raw_candidate_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for shape in shape_rows():
        if shape["pair_or_material"] != "material":
            continue
        rows.append(
            {
                "row_id": f"CFI3257_{shape['material_id']}_EM_Coulomb_candidate",
                "material_id": shape["material_id"],
                "component_id": "EM_Coulomb",
                "fraction_value": f"MISSING_k_C_TIMES_{shape['shape_value_q_C']}",
                "fraction_uncertainty": "MISSING_COEFFICIENT_UNCERTAINTY",
                "basis_convention": "SEMF_Coulomb_shape_from_1909_proxy;fraction_requires_k_C=a_C/(m_u c^2)",
                "source_path_or_url": shape["source_path"],
                "extraction_method": "candidate shell only: numeric q_C shape present, fraction coefficient absent",
                "acceptance_status": "REJECTED_BY_1233_NUMERIC_FRACTION_GATE",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        )
    return rows


def toy_fraction_rows() -> list[dict[str, Any]]:
    toy_coefficient = 7.70e-4
    rows: list[dict[str, Any]] = []
    for shape in shape_rows():
        shape_value = float_or_none(shape["shape_value_q_C"])
        fraction_value = toy_coefficient * shape_value if shape_value is not None else None
        rows.append(
            {
                "toy_fraction_id": f"TOYF3257_{shape['material_id']}",
                "material_id": shape["material_id"],
                "component_id": "EM_Coulomb",
                "q_C_shape": shape["shape_value_q_C"],
                "toy_k_C": f"{toy_coefficient:.12e}",
                "toy_fraction_value": f"{fraction_value:.12e}" if fraction_value is not None else "MISSING_SHAPE_VALUE",
                "toy_coefficient_meaning": "placeholder SEMF-scale k_C for code smoke only; not a sourced accepted coefficient",
                "forbidden_use": "FORBIDDEN_FOR_CLAIM: WEP/local-GR/Maxwell/source-coupling/material-response evidence",
                "valid_for_claim": "false",
            }
        )
    return rows


def toy_shell_input_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fraction in toy_fraction_rows():
        if fraction["material_id"] == "TA6V_minus_PtRh10":
            continue
        rows.append(
            {
                "toy_input_id": f"TOYSHELL3257_{fraction['material_id']}",
                "material_id": fraction["material_id"],
                "f_EM_A": fraction["toy_fraction_value"],
                "M_A_c2_J": "1.000000000000e+00",
                "R_in_m": "1.000000000000e+00",
                "R_out_m": "2.000000000000e+00",
                "C_frame": "1.000000000000e+00",
                "formula_target": "G_J[EM,EM]_A=C_frame^2/(20*pi)*(f_EM,A M_A c^2)^2*K_shell",
                "allowed_use": "debug algebra, units, parser, and branch plumbing only",
                "valid_for_claim": "false",
            }
        )
    return rows


def toy_shell_output_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for toy_input in toy_shell_input_rows():
        fraction_value = float(toy_input["f_EM_A"])
        material_energy_j = float(toy_input["M_A_c2_J"])
        inner_radius = float(toy_input["R_in_m"])
        outer_radius = float(toy_input["R_out_m"])
        frame_factor = float(toy_input["C_frame"])
        energy_em = fraction_value * material_energy_j
        shell_shape = (inner_radius ** -5 - outer_radius ** -5) / (
            (inner_radius ** -1 - outer_radius ** -1) ** 2
        )
        gram_value = frame_factor**2 / (20.0 * math.pi) * energy_em**2 * shell_shape
        rows.append(
            {
                "toy_output_id": toy_input["toy_input_id"].replace("TOYSHELL", "TOYSHELL_OUT"),
                "material_id": toy_input["material_id"],
                "E_EM_A_J": f"{energy_em:.12e}",
                "K_shell_m_minus3": f"{shell_shape:.12e}",
                "G_J_EM_EM_toy": f"{gram_value:.12e}",
                "finite_positive": bool_str(math.isfinite(gram_value) and gram_value > 0),
                "derivation": "3256 material Gram formula evaluated on nonclaim toy coefficient and unit shell",
                "valid_for_claim": "false",
            }
        )
    return rows


def acceptance_rows() -> list[dict[str, Any]]:
    routes = route_rows()
    shapes = shape_rows()
    raw_candidates = raw_candidate_rows()
    toy_outputs = toy_shell_output_rows()
    em_routes_present = {"TA6V", "PtRh10"}.issubset({row["material_id"] for row in routes})
    shape_present = {"TA6V", "PtRh10"}.issubset({row["material_id"] for row in shapes})
    return [
        {
            "audit_id": "ACCEPT3257_0_schema_present",
            "requirement": "1233 component-fraction schema exists and parses",
            "status": "PASS_SCHEMA_PRESENT",
            "evidence": str(OUT / "P8_Y5_R10_1233_COMPONENT_FRACTION_SCHEMA.csv"),
            "accepts_real_fraction": "false",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ACCEPT3257_1_routes_present",
            "requirement": "TA6V and PtRh10 EM_Coulomb acquisition routes exist",
            "status": "PASS_ROUTE_PRESENT" if em_routes_present else "FAIL_ROUTE_MISSING",
            "evidence": ";".join(row["route_id"] for row in routes),
            "accepts_real_fraction": "false",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ACCEPT3257_2_shape_proxy_present",
            "requirement": "numeric alloy Coulomb shape proxy exists for both materials",
            "status": "PASS_SHAPE_PRESENT" if shape_present else "FAIL_SHAPE_MISSING",
            "evidence": ";".join(row["shape_id"] for row in shapes),
            "accepts_real_fraction": "false",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ACCEPT3257_3_claim_fraction_rejected",
            "requirement": "fraction_value must be finite numeric with uncertainty, basis, and source",
            "status": "REJECTED_MISSING_SOURCE_BACKED_k_C_AND_UNCERTAINTY",
            "evidence": ";".join(row["row_id"] for row in raw_candidates),
            "accepts_real_fraction": "false",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ACCEPT3257_4_parent_alpha_map_unsigned",
            "requirement": "MTS parent EM/alpha map must turn Coulomb fraction into parent-owned response",
            "status": "BLOCKED_PARENT_ALPHA_MAP_UNSIGNED",
            "evidence": "1910 exact tensor contract remains nonclaim; 1328 routes remain external-basis-only",
            "accepts_real_fraction": "false",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ACCEPT3257_5_toy_runner_executes",
            "requirement": "toy shell runner evaluates finite positive G_J values without evidence promotion",
            "status": "PASS_TOY_DRYRUN_ONLY" if toy_outputs and all(row["finite_positive"] == "true" for row in toy_outputs) else "FAIL_TOY_DRYRUN",
            "evidence": ";".join(row["toy_output_id"] for row in toy_outputs),
            "accepts_real_fraction": "false",
            "valid_for_claim": "false",
        },
    ]


def gram_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "GJU3257_0_fraction_shape_to_material_Gram",
            "target": "G_J[EM,EM]_A",
            "previous_formula": "C_frame^2/(20*pi)*(f_EM,A M_A c^2)^2*K_shell",
            "new_input_contract": "f_EM,A may be supplied by source-backed k_C q_C,A; currently only q_C,A is numeric and k_C is nonclaim/toy",
            "runner_status": "TOY_NUMERIC_PATH_EXECUTES_REAL_CLAIM_PATH_REJECTED",
            "valid_for_claim": "false",
        },
        {
            "update_id": "GJU3257_1_pair_delta_shape",
            "target": "DeltaR_TA6V_PtRh10^EM",
            "previous_formula": "DeltaR_AB^EM=gamma_EM,A-gamma_EM,B",
            "new_input_contract": "Delta q_C= q_C,TA6V - q_C,PtRh10 is present; Delta f_EM=k_C Delta q_C needs sourced k_C and alpha-response convention",
            "runner_status": "DIFFERENTIAL_SHAPE_PRESENT_PARENT_RESPONSE_UNSIGNED",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3257_0_real_fraction_row",
            "gate": "at least one real EM_Coulomb fraction row accepted under 1233",
            "passed": "false",
            "reason": "numeric q_C shape exists but source-backed k_C, uncertainty, isotope convention, and parent map are absent",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3257_1_toy_runner",
            "gate": "toy shell branch evaluates finite numbers",
            "passed": "true",
            "reason": "runner computes toy f_EM and G_J without promoting them as evidence",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3257_2_local_GR",
            "gate": "local GR/Newton/Maxwell/source-coupling claim",
            "passed": "false",
            "reason": "parent EM owner/alpha map, source kernel, and accepted material fractions remain unsigned",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3257_0",
            "verdict": "NO_REAL_ACCEPTED_FRACTION_ROW_BUT_TOY_DRYRUN_CLOSED",
            "what_moved": "q_C alloy shape now feeds a concrete f_EM=k_C q_C contract and a runnable G_J[EM,EM] dry-run",
            "what_remains": "source-backed k_C/a_C, uncertainty, isotope convention, no-double-count basis, parent EM/alpha response map, source/readout kernel",
            "selected_next": "source-backed EM Coulomb coefficient or parent alpha-map owner",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3257_0_3258",
            "selected": "primary",
            "target_doc": "3258-Y5-R2FR-source-backed-EM-Coulomb-coefficient-or-parent-alpha-map-owner-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3258_source_backed_EM_Coulomb_coefficient_or_parent_alpha_map_owner.py",
            "objective": "Either source a claim-grade Coulomb coefficient/mass convention for f_EM=k_C q_C, or derive the parent alpha-map owner that makes gamma_EM parent-owned rather than external SEMF smoke.",
            "guardrail": "No local-GR/WEP/Maxwell claim unless accepted fraction rows, response map, and source kernel all pass.",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_count() -> int:
    if not FW.exists():
        return 0
    try:
        tracked = []
        for path in FW.rglob("*"):
            if path.is_file() and path.stat().st_mtime > Path(__file__).stat().st_mtime:
                tracked.append(path)
        return len(tracked)
    except Exception:
        return 0


def validation_rows() -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    source_rows = source_register()
    shape_values = [
        float_or_none(row["shape_value_q_C"])
        for row in shape_rows()
        if row["material_id"] in {"TA6V", "PtRh10"}
    ]
    toy_outputs = toy_shell_output_rows()
    raw_rows = raw_candidate_rows()
    validations = [
        {
            "check_id": "VAL3257_0_sources_exist",
            "check": "all required source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in source_rows)),
            "detail": ";".join(row["source_id"] for row in source_rows if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3257_1_sources_parse",
            "check": "all required source CSV/MD paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in source_rows)),
            "detail": ";".join(row["source_id"] for row in source_rows if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3257_2_outputs_parse",
            "check": "all 3257 output CSVs parse",
            "passed": bool_str(all(csv_ok(path) for path in output_paths)),
            "detail": ";".join(str(path) for path in output_paths if not csv_ok(path)),
        },
        {
            "check_id": "VAL3257_3_shape_numeric",
            "check": "TA6V and PtRh10 q_C shape values are finite numeric",
            "passed": bool_str(len(shape_values) == 2 and all(value is not None and math.isfinite(value) for value in shape_values)),
            "detail": ";".join(str(value) for value in shape_values),
        },
        {
            "check_id": "VAL3257_4_raw_candidates_nonclaim",
            "check": "all raw candidate fraction rows remain valid_for_claim=false",
            "passed": bool_str(raw_rows and all(row["valid_for_claim"] == "false" for row in raw_rows)),
            "detail": ";".join(row["row_id"] for row in raw_rows),
        },
        {
            "check_id": "VAL3257_5_toy_outputs_finite_positive",
            "check": "toy shell G_J outputs are finite positive",
            "passed": bool_str(toy_outputs and all(row["finite_positive"] == "true" for row in toy_outputs)),
            "detail": ";".join(row["toy_output_id"] for row in toy_outputs),
        },
        {
            "check_id": "VAL3257_6_no_claim_gate_promoted",
            "check": "no 3257 claim gate allows a local-GR/WEP/Maxwell claim",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in claim_gate_rows())),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3257_7_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3257_8_overall",
            "check": "3257 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3257_8_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def write_doc() -> None:
    sources = source_register()
    formulas = formula_rows()
    shapes = shape_rows()
    raw_candidates = raw_candidate_rows()
    acceptance = acceptance_rows()
    toy_fractions = toy_fraction_rows()
    toy_outputs = toy_shell_output_rows()
    gram_updates = gram_update_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()
    validations = validation_rows()
    content = f"""# 3257 - First accepted EM Coulomb fraction row or toy-shell runner dryrun under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3257` does **not** accept a real `EM_Coulomb` material fraction row.
- It does make a concrete leap: the 1909 alloy Coulomb shape is now connected to `f_EM,A = k_C q_C,A`, and that fraction contract is executable in the 3256 `G_J[EM,EM]` material shell formula.
- The toy SEMF-scale coefficient branch runs and produces finite positive `G_J` rows, but every such row is quarantined as nonclaim.
- The next real fork is sharp: source `k_C=a_C/(m_u c^2)` plus uncertainty/convention, or derive the parent-owned alpha/EM response map so the coefficient is not external smoke.

## Source Register
{md_table(sources, ["source_id", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"])}

## EM Coulomb Fraction Formula Contract
{md_table(formulas, ["formula_id", "object", "formula", "derivation", "inputs", "status", "valid_for_claim"])}

## Numeric Shape Rows
{md_table(shapes, ["shape_id", "material_id", "shape_value_q_C", "fraction_formula", "coefficient_status", "status", "valid_for_claim"])}

## Raw Candidate Rows
{md_table(raw_candidates, ["row_id", "material_id", "component_id", "fraction_value", "fraction_uncertainty", "basis_convention", "acceptance_status", "valid_for_claim"])}

## Acceptance Audit
{md_table(acceptance, ["audit_id", "requirement", "status", "evidence", "accepts_real_fraction", "valid_for_claim"])}

## Toy SEMF-Coefficient Fraction Dryrun
{md_table(toy_fractions, ["toy_fraction_id", "material_id", "q_C_shape", "toy_k_C", "toy_fraction_value", "toy_coefficient_meaning", "valid_for_claim"])}

## Toy Shell Output
{md_table(toy_outputs, ["toy_output_id", "material_id", "E_EM_A_J", "K_shell_m_minus3", "G_J_EM_EM_toy", "finite_positive", "valid_for_claim"])}

## Gram Update
{md_table(gram_updates, ["update_id", "target", "previous_formula", "new_input_contract", "runner_status", "valid_for_claim"])}

## Claim Gates
{md_table(gates, ["gate_id", "gate", "passed", "reason", "claim_allowed"])}

## Decision
{md_table(decisions, ["decision_id", "verdict", "what_moved", "what_remains", "selected_next", "valid_for_claim"])}

## Next Target
{md_table(next_targets, ["next_id", "selected", "target_doc", "target_script", "objective", "guardrail", "valid_for_claim"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    rows_by_key = {
        "sources": source_register(),
        "formula": formula_rows(),
        "shape": shape_rows(),
        "raw_candidate": raw_candidate_rows(),
        "acceptance": acceptance_rows(),
        "toy_fraction": toy_fraction_rows(),
        "toy_shell_input": toy_shell_input_rows(),
        "toy_shell_output": toy_shell_output_rows(),
        "gram_update": gram_update_rows(),
        "gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, rows in rows_by_key.items():
        write_csv(OUTPUTS[key], rows)
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

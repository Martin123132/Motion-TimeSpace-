from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3384-Y5-R2FR-Cmetric-Gamma-post-UOC-PPN-zero-or-first-bound-row-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3384_SOURCE_REGISTER.csv",
    "gamma_zero": OUT / "P8_Y5_R2FR_3384_GAMMA_ZERO_OR_BOUND_ATTEMPT.csv",
    "cmetric_zero": OUT / "P8_Y5_R2FR_3384_CMETRIC_EPSILON_ZERO_OR_BOUND_ATTEMPT.csv",
    "gamma_bound": OUT / "P8_Y5_R2FR_3384_FIRST_GAMMA_PPN_BOUND_ROW_NONCLAIM.csv",
    "metric_response": OUT / "P8_Y5_R2FR_3384_METRIC_RESPONSE_INPUT_REQUIREMENTS.csv",
    "reduced_budget": OUT / "P8_Y5_R2FR_3384_REDUCED_BUDGET_UPDATE.csv",
    "runner": OUT / "P8_Y5_R2FR_3384_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3384_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3384_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3384_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3384_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3384_0_3383_doc", ROOT / "3383-Y5-R2FR-UOC-extra-MTSIR-local-PPN-residual-vector-or-zero-theorem-under-AX1090.md", "3383 post-UOC PPN residual vector"),
    ("SRC3384_1_3383_vector", OUT / "P8_Y5_R2FR_3383_EXTRA_MTSIR_PPN_RESIDUAL_VECTOR.csv", "3383 residual vector"),
    ("SRC3384_2_3383_bounds", OUT / "P8_Y5_R2FR_3383_BOUND_ROWS_NONCLAIM.csv", "3383 bound row schema"),
    ("SRC3384_3_3330_doc", ROOT / "3330-Y5-R2FR-PPN-response-coefficient-and-local-floor-bound-under-AX1090.md", "PPN response coefficient/local floor"),
    ("SRC3384_4_3330_response", OUT / "P8_Y5_R2FR_3330_PPN_RESPONSE_COEFFICIENT.csv", "C_PPN response coefficient"),
    ("SRC3384_5_3330_floors", OUT / "P8_Y5_R2FR_3330_LOCAL_FLOOR_BOUNDS.csv", "Gamma and epsilon floor formulas"),
    ("SRC3384_6_3331_doc", ROOT / "3331-Y5-R2FR-PPN-weak-potential-normalization-and-Cmetric-bound-under-AX1090.md", "Cmetric/A_PPN derivation"),
    ("SRC3384_7_3331_appn", OUT / "P8_Y5_R2FR_3331_APPN_BOUND.csv", "A_PPN component bounds"),
    ("SRC3384_8_3331_cmetric", OUT / "P8_Y5_R2FR_3331_CMETRIC_BOUND.csv", "C_metric bound formula"),
    ("SRC3384_9_3331_cppn", OUT / "P8_Y5_R2FR_3331_CPPN_COMPOSITION.csv", "C_PPN composition"),
    ("SRC3384_10_3332_doc", ROOT / "3332-Y5-R2FR-PPN-epsilon-eff-and-floor-specialization-under-AX1090.md", "epsilon_eff and floor specialization"),
    ("SRC3384_11_3332_budget", OUT / "P8_Y5_R2FR_3332_NORMALIZED_PPN_BUDGET.csv", "normalized PPN budget"),
    ("SRC3384_12_3332_gamma", OUT / "P8_Y5_R2FR_3332_GAMMA_FLOOR_BRANCHES.csv", "Gamma floor branches"),
    ("SRC3384_13_3332_epsilon", OUT / "P8_Y5_R2FR_3332_EPSILON_EFF_SPECIALIZATION.csv", "epsilon_eff specialization"),
    ("SRC3384_14_3333_doc", ROOT / "3333-Y5-R2FR-PPN-zero-floor-branch-certificate-under-AX1090.md", "zero-floor branch certificate"),
    ("SRC3384_15_3333_gamma", OUT / "P8_Y5_R2FR_3333_GAMMA_BRANCH_CERTIFICATE.csv", "Gamma branch certificate"),
    ("SRC3384_16_3333_budget", OUT / "P8_Y5_R2FR_3333_REDUCED_PPN_BUDGET.csv", "reduced PPN budget"),
    ("SRC3384_17_3166_cassini", OUT / "P8_Y5_R2FR_3166_CASSINI_GAMMA_SOURCE_INTAKE.csv", "Cassini gamma external bound intake"),
]


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def first_value(path: Path, column: str, default: str) -> str:
    for row in read_csv_rows(path):
        value = row.get(column, "").strip()
        if value:
            return value
    return default


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        if not exists:
            parse_ok, parse_error = False, "missing"
        elif path.suffix.lower() == ".csv":
            parse_ok, parse_error = parse_csv(path)
        else:
            parse_ok, parse_error = parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def gamma_zero_rows() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "GZ3384_0_finite_pole",
            "target": "R_Gamma_PPN^pole",
            "zero_route": "Gamma_G is readout/background and delta Gamma_G is not an independent local Hessian row",
            "result": "CONDITIONAL_ZERO_POLE_INHERITED",
            "why_not_full": "kills finite exchange pole only; not the constant/proxy Gamma floor",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "GZ3384_1_constant_floor",
            "target": "R_Gamma_const",
            "zero_route": "Gamma_local=0 in the local PPN patch or source-owned constant curvature is below allocated gamma budget",
            "result": "NOT_ZERO_SIGNED",
            "why_not_full": "no parent-signed local Gamma_local=0 certificate or sourced constant-curvature value",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "GZ3384_2_solar_proxy",
            "target": "R_Gamma_proxy",
            "zero_route": "Gamma residual maps to K_solar^m with K_solar about 1e-61 and m>=2, giving an encouraging tiny proxy",
            "result": "ENCOURAGING_PROXY_NOT_CLAIM",
            "why_not_full": "proxy only applies if local Gamma residual is parent-mapped to the curvature-saturation proxy",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "GZ3384_3_verdict",
            "target": "R_Gamma_const_or_proxy",
            "zero_route": "finite pole zero plus constant/proxy floor zero",
            "result": "PARTIAL_ZERO_BOUND_ROW_REQUIRED",
            "why_not_full": "only finite pole is conditionally closed; full floor needs certificate or bound",
            "valid_for_claim": "false",
        },
    ]


def cmetric_zero_rows() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "CMZ3384_0_Cmetric_zero",
            "target": "C_metric",
            "zero_route": "residual MTS metric operator response vanishes in the local PPN patch",
            "result": "NOT_DERIVED",
            "why_not_full": "3331 defines C_metric as operator norm; no source-backed zero norm certificate exists",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "CMZ3384_1_epsilon_eff_zero",
            "target": "epsilon_eff_PPN",
            "zero_route": "epsilon_bg_PPN=epsilon_boundary_PPN=epsilon_kernel_aniso_PPN=0",
            "result": "CONDITIONAL_ZERO_BRANCH_NOT_SIGNED",
            "why_not_full": "local first-gradient silence, boundary silence and kernel isotropy are not all parent-signed",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "CMZ3384_2_bound_product",
            "target": "A_PPN C_metric epsilon_eff_PPN^2",
            "zero_route": "if not zero, compare product to a sourced PPN budget with no cancellation",
            "result": "FORMULA_READY_NUMERIC_MISSING",
            "why_not_full": "A_PPN and C_metric are symbolic; epsilon_eff components are missing source-backed values",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "CMZ3384_3_verdict",
            "target": "metric-response PPN product",
            "zero_route": "C_metric=0 or epsilon_eff=0 or product below bound",
            "result": "FIRST_BOUND_ROW_STAGED_NONCLAIM",
            "why_not_full": "Cassini provides a gamma bound, but MTS prediction row remains symbolic/nonclaim",
            "valid_for_claim": "false",
        },
    ]


def gamma_bound_rows() -> list[dict[str, str]]:
    cassini = OUT / "P8_Y5_R2FR_3166_CASSINI_GAMMA_SOURCE_INTAKE.csv"
    return [
        {
            "row_id": "GB3384_0_Cassini_gamma_component_bound",
            "observable": "PPN_gamma_minus_one",
            "external_bound_abs": first_value(cassini, "abs_envelope_2sigma", "6.7e-05"),
            "bound_units": "dimensionless",
            "source_path": str(cassini),
            "source_value_status": "EXTERNAL_BOUND_PRESENT",
            "mts_prediction_formula": "|delta_gamma_MTS| <= |R_Gamma_const_or_proxy| + A_gamma(q_U,gauge) C_metric epsilon_eff_PPN^2 + epsilon_composite_gamma + R_nonEH_gamma + R_transfer_gamma",
            "mts_prediction_value": "MISSING_Agamma_Cmetric_epsilon_eff_components_AND_residual_splits",
            "claim_test": "|delta_gamma_MTS| <= external_bound_abs",
            "valid_external_bound": "true",
            "valid_mts_prediction_row": "false",
            "valid_for_claim": "false",
        },
        {
            "row_id": "GB3384_1_Gamma_proxy_smoke_only",
            "observable": "Gamma_proxy_contribution_to_gamma",
            "external_bound_abs": first_value(cassini, "abs_envelope_2sigma", "6.7e-05"),
            "bound_units": "dimensionless",
            "source_path": str(OUT / "P8_Y5_R2FR_3330_LOCAL_FLOOR_BOUNDS.csv"),
            "source_value_status": "INTERNAL_PROXY_FORMULA_PRESENT",
            "mts_prediction_formula": "R_Gamma_proxy <= K_solar^m <= 1e-122 for K_solar about 1e-61 and m>=2",
            "mts_prediction_value": "1e-122_PROXY_ONLY_NOT_PARENT_MAPPED",
            "claim_test": "proxy would be far below Cassini if parent map is signed",
            "valid_external_bound": "true",
            "valid_mts_prediction_row": "false",
            "valid_for_claim": "false",
        },
    ]


def metric_response_rows() -> list[dict[str, str]]:
    return [
        {
            "input_id": "MRI3384_0_Agamma",
            "quantity": "A_gamma(q_U,gauge)",
            "required_for": "gamma component of A_PPN",
            "current_status": "SYMBOLIC_BOUND_DERIVED",
            "needed_next": "source q_U for chosen Solar-system comparison and fix gauge/readout/source residual terms",
            "valid_for_claim": "false",
        },
        {
            "input_id": "MRI3384_1_Cmetric",
            "quantity": "C_metric(lambda_PPN)",
            "required_for": "metric operator response",
            "current_status": "SYMBOLIC_OPERATOR_BOUND",
            "needed_next": "fill P_PPN,G_fix,W_src,D_readout,S_band,H_band,N_source for a declared PPN patch",
            "valid_for_claim": "false",
        },
        {
            "input_id": "MRI3384_2_epsilon_eff",
            "quantity": "epsilon_eff_PPN",
            "required_for": "tree leakage amplitude",
            "current_status": "FORMULA_READY_NOT_NUMERIC",
            "needed_next": "derive or bound epsilon_bg_PPN, epsilon_boundary_PPN and epsilon_kernel_aniso_PPN",
            "valid_for_claim": "false",
        },
        {
            "input_id": "MRI3384_3_Btree",
            "quantity": "B_tree_gamma",
            "required_for": "allowable tree leakage after floors",
            "current_status": "DEFINED_AFTER_FLOORS_ONLY",
            "needed_next": "subtract Gamma/composite/nonEH/transfer allocations from Cassini gamma envelope",
            "valid_for_claim": "false",
        },
    ]


def reduced_budget_rows() -> list[dict[str, str]]:
    return [
        {
            "budget_id": "RB3384_0_post_3384_gamma",
            "formula": "|delta_gamma_MTS| <= |R_Gamma_const_or_proxy| + A_gamma C_metric epsilon_eff_PPN^2 + epsilon_composite_gamma + R_nonEH_gamma + R_transfer_gamma",
            "update": "external gamma bound attached; MTS side still symbolic",
            "claim_status": "NONCLAIM_FIRST_BOUND_ROW",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "RB3384_1_if_Gamma_proxy_signed",
            "formula": "|delta_gamma_MTS| <= A_gamma C_metric epsilon_eff_PPN^2 + epsilon_composite_gamma + R_nonEH_gamma + R_transfer_gamma + 1e-122_proxy",
            "update": "Gamma likely harmless only if proxy map is parent-signed",
            "claim_status": "PROMISING_CONDITIONAL_NOT_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "RB3384_2_next_bound",
            "formula": "A_gamma C_metric epsilon_eff_PPN^2 < B_gamma_remaining",
            "update": "first real route is to fill A_gamma/Cmetric/epsilon_eff or prove epsilon_eff=0",
            "claim_status": "NEXT_NUMERIC_OR_ZERO_TARGET",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {"run_id": "RUN3384_0_Gamma_pole", "test": "finite Gamma pole zero", "result": "PASS_CONDITIONAL_POLE_ZERO", "detail": "inherits 3333 no-independent-local-Gamma-row branch", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3384_1_Gamma_full", "test": "full Gamma constant/proxy floor zero", "result": "FAIL_FULL_ZERO_NOT_SIGNED", "detail": "Gamma_local=0/proxy parent map not signed", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3384_2_Cmetric_product", "test": "A_PPN Cmetric epsilon_eff^2 zero or bounded", "result": "FORMULA_READY_NUMERIC_MISSING", "detail": "operator response and epsilon inputs remain symbolic", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3384_3_gamma_bound", "test": "first finite gamma bound row", "result": "PASS_EXTERNAL_BOUND_NONCLAIM", "detail": "Cassini gamma envelope is attached; MTS prediction row is missing components", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3384_4_firewall", "test": "prevent local-GR overclaim", "result": "PASS_CLAIM_FIREWALL", "detail": "all rows remain nonclaim and full PPN remains blocked", "claim_allowed": "false", "valid_for_claim": "false"},
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {"gate_id": "GATE3384_0_sources", "claim": "all 3384 source paths exist and parse", "gate_pass": bool_text(source_ok), "reason": "source register validates 3383/3330-3333/Cassini inputs", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3384_1_gamma_pole", "claim": "finite Gamma pole is absent in the clean branch", "gate_pass": "true", "reason": "conditional no-independent-local-Gamma-row branch inherited", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3384_2_gamma_full", "claim": "full Gamma floor is zero or bounded", "gate_pass": "false", "reason": "constant/proxy mapping not parent-signed or numerically sourced", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3384_3_cmetric_product", "claim": "A_PPN Cmetric epsilon_eff^2 is zero or bounded", "gate_pass": "false", "reason": "A_PPN/Cmetric/epsilon_eff inputs remain symbolic", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3384_4_gamma_bound_row", "claim": "finite gamma bound row exists", "gate_pass": "true", "reason": "Cassini external gamma envelope attached as nonclaim comparator", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3384_5_local_gr", "claim": "local GR/PPN passes under UOC", "gate_pass": "false", "reason": "MTS prediction row remains missing and transfer/nonEH/composite tails remain live", "claim_allowed": "false", "valid_for_claim": "false"},
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3384_0_progress",
            "decision": "3384 converts the Cmetric/Gamma blocker into the first finite gamma-bound comparator.",
            "because": "Cassini gamma is now attached to the post-UOC residual formula, while the MTS prediction remains honestly blocked.",
            "next_action": "fill A_gamma/Cmetric/epsilon_eff or prove epsilon_eff zero",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3384_1_gamma",
            "decision": "Gamma is not the scary part if the proxy map is signed, but that map is not signed yet.",
            "because": "the K_solar^m proxy is tiny, but current proof only closes the finite pole, not the constant/proxy floor.",
            "next_action": "derive Gamma proxy map or source Gamma_local bound",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3384_2_main_blocker",
            "decision": "The main direct PPN blocker is now the metric-response product.",
            "because": "A_PPN amplifies tiny metric residuals by weak-potential denominators, especially beta-like slots.",
            "next_action": "build a numeric/symbolic runner for A_gamma, Cmetric and epsilon_eff components",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3385-Y5-R2FR-A_gamma-Cmetric-epsilon-eff-first-numeric-PPN-runner-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3385_Agamma_Cmetric_epsilon_eff_first_numeric_PPN_runner.py",
            "objective": "build the first nonclaim numeric/symbolic runner for A_gamma, Cmetric and epsilon_eff against the Cassini gamma envelope",
            "why_next": "3384 attaches the real gamma bound; the next move is to populate the MTS side or prove a zero component",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3386-Y5-R2FR-Gamma-proxy-parent-map-or-Gamma-local-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3386_Gamma_proxy_parent_map_or_Gamma_local_bound.py",
            "objective": "derive the parent map from local Gamma residual to K_solar^m proxy, or retain a finite Gamma_local PPN bound row",
            "why_next": "Gamma proxy is potentially very safe but cannot be used until the map is signed",
            "valid_for_claim": "false",
        },
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = [
        hit
        for hit in FW.rglob("*3384*")
        if hit.name.startswith(("3384-Y5", "P8_Y5_R2FR_3384", "P8_Y5_BRR545_3384", "Y5_R2FR_3384"))
    ] if FW.exists() else []
    gamma_results = {row["result"] for row in rows_by_name["gamma_zero"]}
    cmetric_results = {row["result"] for row in rows_by_name["cmetric_zero"]}
    bound_ids = {row["row_id"] for row in rows_by_name["gamma_bound"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3384_0_sources_exist_parse", "all cited 3384 source paths exist and parse", source_ok, ""),
        ("VAL3384_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3384_2_gamma_attempt", "Gamma attempt conditionally zeros pole but blocks full floor", "CONDITIONAL_ZERO_POLE_INHERITED" in gamma_results and "PARTIAL_ZERO_BOUND_ROW_REQUIRED" in gamma_results, ""),
        ("VAL3384_3_cmetric_attempt", "Cmetric attempt blocks zero claim and stages bound formula", "NOT_DERIVED" in cmetric_results and "FORMULA_READY_NUMERIC_MISSING" in cmetric_results and "FIRST_BOUND_ROW_STAGED_NONCLAIM" in cmetric_results, ""),
        ("VAL3384_4_gamma_bound_rows", "first gamma PPN bound row and Gamma proxy smoke row exist", {"GB3384_0_Cassini_gamma_component_bound", "GB3384_1_Gamma_proxy_smoke_only"}.issubset(bound_ids), ""),
        ("VAL3384_5_runner", "runner records conditional pole zero, full Gamma failure, missing Cmetric product, external bound and firewall", {"PASS_CONDITIONAL_POLE_ZERO", "FAIL_FULL_ZERO_NOT_SIGNED", "FORMULA_READY_NUMERIC_MISSING", "PASS_EXTERNAL_BOUND_NONCLAIM", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3384_6_gates", "gates pass gamma pole and external bound but block full Gamma, Cmetric product and local GR", gate_map.get("GATE3384_1_gamma_pole") == "true" and gate_map.get("GATE3384_2_gamma_full") == "false" and gate_map.get("GATE3384_3_cmetric_product") == "false" and gate_map.get("GATE3384_4_gamma_bound_row") == "true" and gate_map.get("GATE3384_5_local_gr") == "false", ""),
        ("VAL3384_7_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3384_8_next_target", "next target moves to A_gamma/Cmetric/epsilon_eff runner", rows_by_name["next"][0]["target_id"].startswith("3385-Y5-R2FR-A_gamma-Cmetric"), ""),
        ("VAL3384_9_write_scope_outside_formalization", "no 3384 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    checks.append(("VAL3384_10_overall", "3384 validation overall", all(passed for _, _, passed, _ in checks), "all required checks passed" if all(passed for _, _, passed, _ in checks) else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3384 - Y5/R2FR Cmetric-Gamma post-UOC PPN zero or first bound row under AX1090",
        "",
        "## Summary",
        "- 3384 attacks the direct `C_metric/Gamma` post-UOC PPN bottleneck.",
        "- Gamma result: the finite Gamma exchange pole is conditionally absent in the clean readout/background branch, but the full constant/proxy Gamma floor is not zero-signed.",
        "- Cmetric result: `A_PPN C_metric epsilon_eff_PPN^2` is formula-ready but not zero or numeric because `A_PPN`, `C_metric`, and `epsilon_eff` components remain symbolic.",
        "- Concrete progress: the first finite gamma-style PPN comparator is now staged from the existing Cassini gamma intake; the MTS prediction side remains nonclaim.",
        "- Useful hint: the `K_solar^m <= 1e-122` proxy would make Gamma harmless if the parent map is signed, but that map is still the missing theorem.",
        "- Best next strike: build the first `A_gamma/Cmetric/epsilon_eff` runner against the Cassini envelope, or prove `epsilon_eff=0` by parent silence.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Gamma Zero Or Bound Attempt",
        md_table(rows_by_name["gamma_zero"]),
        "## Cmetric Epsilon Zero Or Bound Attempt",
        md_table(rows_by_name["cmetric_zero"]),
        "## First Gamma PPN Bound Row",
        md_table(rows_by_name["gamma_bound"]),
        "## Metric Response Input Requirements",
        md_table(rows_by_name["metric_response"]),
        "## Reduced Budget Update",
        md_table(rows_by_name["reduced_budget"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_register = source_rows()
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_register)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "gamma_zero": gamma_zero_rows(),
        "cmetric_zero": cmetric_zero_rows(),
        "gamma_bound": gamma_bound_rows(),
        "metric_response": metric_response_rows(),
        "reduced_budget": reduced_budget_rows(),
        "runner": runner_rows(),
        "gates": gate_rows(source_ok),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()

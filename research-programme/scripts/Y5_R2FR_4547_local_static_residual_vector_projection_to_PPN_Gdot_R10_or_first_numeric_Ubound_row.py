from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4547"
CLAIM_ID = "L-389"
BRANCH_ID = "MTS_R2FR_Y5_STATIC_RESIDUAL_PROJECTION_4547"
MARKER = "PPC4161_LOCAL_STATIC_RESIDUAL_VECTOR_PROJECTION_TO_PPN_GDOT_R10_OR_FIRST_NUMERIC_UBOUND_ROW_4547"
PACKET_MARKER = "PPC4161_PACKET_LOCAL_STATIC_RESIDUAL_VECTOR_PROJECTION_TO_PPN_GDOT_R10_OR_FIRST_NUMERIC_UBOUND_ROW_4547"
DECISION = "STATIC_RESIDUAL_PROJECTION_CONTRACT_AND_EPSILON_U_BOUND_ROWS_WRITTEN_NUMERIC_INPUTS_MISSING_NONCLAIM"
NEXT_TARGET = "4548-Y5-R2FR-fill-first-epsilonU-local-range-row-or-static-bound-runner-smoke.md"

FORMAL_PATH = FORMAL / "563-PPC4161-local-static-residual-vector-projection-to-PPN-Gdot-R10-or-first-numeric-Ubound-row.md"
DOC_PATH = POST / "4547-Y5-R2FR-local-static-residual-vector-projection-to-PPN-Gdot-R10-or-first-numeric-Ubound-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4547_SOURCE_REGISTER.csv"
STATIC_VECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4547_STATIC_RESIDUAL_VECTOR.csv"
ARENA_PROJECTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4547_ARENA_PROJECTION_CONTRACT.csv"
PASS_INEQUALITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4547_PASS_INEQUALITY_ROWS.csv"
EPSILON_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4547_EPSILON_U_BOUND_ROWS.csv"
GDOT_R10_INTERFACE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4547_GDOT_R10_INTERFACE_DECISION.csv"
INPUT_ACQUISITION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4547_INPUT_ACQUISITION_QUEUE.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4547_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4547_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4547_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4547_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4547_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
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
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC4547_00_4546_status",
            "label": "4546 status",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4546_STATUS.csv",
            "needle": "STATIC_SOURCE_AND_ML_HOMOGENEITY_EXACT_ZERO_CONDITIONAL_UB2_BOUND_IMPORTED_ACTIVE_NONCLAIM",
            "role": "imports current static residual state",
        },
        {
            "source_id": "SRC4547_01_4546_static_budget",
            "label": "4546 static Jres budget",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4546_STATIC_JRES_BUDGET.csv",
            "needle": "SJ4546_0_static_budget",
            "role": "defines the shared B_static envelope",
        },
        {
            "source_id": "SRC4547_02_4546_requirements",
            "label": "4546 input requirements",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4546_INPUT_REQUIREMENTS.csv",
            "needle": "REQ4546_4_worldtube_profile",
            "role": "keeps shared source profile/no-retuning requirement",
        },
        {
            "source_id": "SRC4547_03_4188_runner",
            "label": "4188 product-bound runner",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4188_CGAMMA_PRODUCT_BOUND_RUNNER.csv",
            "needle": "RUN4188_B4173_11_R10",
            "role": "imports PPN/Gdot/R10 local threshold rows",
        },
        {
            "source_id": "SRC4547_04_4542_strictest",
            "label": "4542 strictest cGamma bounds",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4542_STRICTEST_CGAMMA_PRODUCT_BOUNDS.csv",
            "needle": "B4542_CGamma_vector",
            "role": "imports strict alpha3/xi/Gdot/R10 locks",
        },
        {
            "source_id": "SRC4547_05_template",
            "label": "local residual prediction template",
            "path": SOURCE_DIR / "MTS_local_residual_predictions_TEMPLATE.csv",
            "needle": "R10_fifth_force",
            "role": "maps residual vector rows to local observables",
        },
        {
            "source_id": "SRC4547_06_alpha3_template",
            "label": "alpha3 numeric template",
            "path": SOURCE_DIR / "P8_ALPHA3_NUMERIC_PRODUCT_INPUT_TEMPLATE.csv",
            "needle": "A3_BOUNDARY_NUMERIC_OR_ZERO",
            "role": "keeps ultratight alpha3 row as individual channel gate",
        },
        {
            "source_id": "SRC4547_07_constant_GM_gate",
            "label": "constant GM derivative/range gate",
            "path": SOURCE_DIR / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
            "needle": "CGM4_range_dependence",
            "role": "separates Gdot time drift from radial/range/R10 hair",
        },
        {
            "source_id": "SRC4547_08_worldtube_gate",
            "label": "2224 worldtube profile gate",
            "path": SOURCE_DIR / "P8_Y5_PARENT_QLOC_2224_WORLDTUBE_PROFILE_GATE.csv",
            "needle": "one compact profile should feed all local arenas",
            "role": "forbids per-arena source-profile retuning",
        },
        {
            "source_id": "SRC4547_09_4546_UB2",
            "label": "4546 U_B2 theorem",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4546_UB2_STATIC_BOUND_THEOREM.csv",
            "needle": "UB24546_1_linear_silence",
            "role": "imports U_B2 source leakage formula",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        path = Path(spec["path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle = str(spec["needle"])
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": b(exists),
                "needle": needle,
                "needle_found": b(exists and needle in text),
                "role": spec["role"],
                "valid_for_claim": "False",
            }
        )
    return rows


def load_runner_rows() -> list[dict[str, str]]:
    rows = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4188_CGAMMA_PRODUCT_BOUND_RUNNER.csv")
    wanted = {"RUN4188_B4173_02_xi", "RUN4188_B4173_05_alpha3", "RUN4188_B4173_08_zeta3", "RUN4188_B4173_10_Gdot", "RUN4188_B4173_11_R10", "RUN4188_B4173_14_orbit_combo"}
    return [row for row in rows if row["runner_id"] in wanted]


def static_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "vector_id": "SV4547_0_B_static",
            "symbol": "B_static",
            "definition": "B_static := C_H A_1 epsilon_U^2 + D_m C_lap_m epsilon_U^2/L_B^2 + B_boundary_static + O(epsilon_U^3)",
            "source": str(SOURCE_DIR / "P8_Y5_R2FR_4546_STATIC_JRES_BUDGET.csv"),
            "meaning": "shared local static residual envelope after 4545 derivative silence",
            "numeric_value": "missing",
            "units": "source/profile norm units before arena projection",
            "valid_for_claim": "False",
        },
        {
            "vector_id": "SV4547_1_source_piece",
            "symbol": "B_src",
            "definition": "B_src := C_H A_1 epsilon_U^2",
            "source": str(SOURCE_DIR / "P8_Y5_R2FR_4546_UB2_STATIC_BOUND_THEOREM.csv"),
            "meaning": "source leakage contribution from P_loc[U_B S_cg]",
            "numeric_value": "missing",
            "units": "same as B_static",
            "valid_for_claim": "False",
        },
        {
            "vector_id": "SV4547_2_mL_piece",
            "symbol": "B_mL",
            "definition": "B_mL := D_m C_lap_m epsilon_U^2/L_B^2",
            "source": str(SOURCE_DIR / "P8_Y5_R2FR_4546_ML_HOMOGENEITY_BOUND.csv"),
            "meaning": "spatial/laplacian attractor inhomogeneity contribution",
            "numeric_value": "missing",
            "units": "same as B_static",
            "valid_for_claim": "False",
        },
        {
            "vector_id": "SV4547_3_boundary_piece",
            "symbol": "B_boundary_static",
            "definition": "B_boundary_static := ||P_loc boundary_in_static||",
            "source": str(SOURCE_DIR / "P8_Y5_R2FR_4546_INPUT_REQUIREMENTS.csv"),
            "meaning": "retained trace/shear/vector boundary amplitude after derivative silence",
            "numeric_value": "missing",
            "units": "same as B_static after projection",
            "valid_for_claim": "False",
        },
    ]


def arena_projection_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in load_runner_rows():
        effective = row["effective_product"]
        observable = row["observable"]
        arena = row["arena"]
        if effective == "C_Gamma_Gdot":
            projection = "Delta_Gdot/G_static = J_Gdot^t D_t B_static; 4545 makes derivative channel conditionally zero, so static B_static does not by itself create Gdot."
            kernel = "J_Gdot^t and proof D_t B_static=0"
        elif effective == "C_Gamma_R10":
            projection = "alpha_MTS(lambda) = K_R10(lambda) B_static(lambda)"
            kernel = "K_R10(lambda) curve and B_static radial/range profile"
        elif effective == "C_Gamma_vector":
            projection = f"Delta_{observable} = K_{observable}^vec B_boundary/vector_static + K_{observable}^src B_src"
            kernel = f"K_{observable} vector/flux projection; no scalar cancellation"
        elif effective == "C_Gamma_stress":
            projection = f"Delta_{observable} = K_{observable}^stress B_static"
            kernel = f"K_{observable} stress-conservation projection"
        else:
            projection = f"Delta_{observable} = K_{observable}^scalar B_static"
            kernel = f"K_{observable} scalar/metric projection"
        rows.append(
            {
                "projection_id": "AP4547_" + row["runner_id"].replace("RUN4188_B4173_", ""),
                "arena": arena,
                "observable": observable,
                "effective_product": effective,
                "bound": row["max_abs_effective_product"],
                "units": row["units"],
                "projection_formula": projection,
                "required_kernel_or_proof": kernel,
                "shared_profile_policy": "same B_static/source profile for all arenas; no retuning",
                "numeric_ready": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def pass_inequality_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for proj in arena_projection_rows():
        observable = proj["observable"]
        if proj["effective_product"] == "C_Gamma_Gdot":
            inequality = "If D_t B_static=0, static contribution to Gdot is zero; otherwise |J_Gdot^t D_t B_static| <= 2.42e-14 yr^-1."
        elif proj["effective_product"] == "C_Gamma_R10":
            inequality = "For every lambda in the tested curve, |K_R10(lambda) B_static(lambda)| <= alpha_bound(lambda); anchor alpha<=1 is smoke only."
        else:
            inequality = f"|{proj['projection_formula'].split('=')[0].strip()}| <= {proj['bound']} {proj['units']}"
        rows.append(
            {
                "pass_id": "PI4547_" + observable.replace("(", "").replace(")", "").replace("/", "_").replace(" ", "_"),
                "observable": observable,
                "bound": proj["bound"],
                "units": proj["units"],
                "pass_inequality": inequality,
                "status": "formula_ready_inputs_missing",
                "valid_for_claim": "False",
            }
        )
    return rows


def epsilon_bound_rows() -> list[dict[str, Any]]:
    selected = [
        ("alpha3", "4e-20", "dimensionless", "K_alpha3", "hardest vector/flux PPN lock"),
        ("xi", "4e-09", "dimensionless", "K_xi", "preferred-location/static anisotropy lock"),
        ("R10_alpha_anchor", "1", "dimensionless", "K_R10(lambda)", "short-range fifth-force anchor only; full curve still required"),
        ("Gdot_static_derivative", "2.42e-14", "yr^-1", "J_Gdot^t D_t", "only if static envelope drifts; 4545 aims to zero this"),
    ]
    rows = []
    for observable, bound, units, kernel, note in selected:
        if observable == "Gdot_static_derivative":
            formula = "If D_t B_static is not theorem-zero, require |J_Gdot^t D_t B_static| <= 2.42e-14 yr^-1; no epsilon_U-only bound exists without a time-variation model."
        else:
            formula = f"epsilon_U <= sqrt(({bound} - B_boundary_{observable}) / ({kernel} * (C_H A_1 + D_m C_lap_m/L_B^2))) when numerator positive."
        rows.append(
            {
                "row_id": "EUB4547_" + observable,
                "observable": observable,
                "target_bound": bound,
                "bound_units": units,
                "kernel": kernel,
                "epsilon_U_bound_formula": formula,
                "missing_inputs": "kernel, B_boundary_channel, C_H A_1, D_m C_lap_m/L_B^2, local domain/range",
                "note": note,
                "numeric_value": "missing",
                "valid_for_claim": "False",
            }
        )
    return rows


def gdot_r10_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "interface_id": "IF4547_0_Gdot",
            "channel": "Gdot",
            "4547_decision": "static B_static does not automatically source Gdot; Gdot needs D_t B_static or derivative hair",
            "current_status": "conditionally_quiet_from_4545_but_not_full_local_GR",
            "next_input": "D_t B_static theorem-zero or numeric derivative row in yr^-1",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "IF4547_1_R10",
            "channel": "R10",
            "4547_decision": "static radial/range part of B_static can source alpha(lambda); anchor alpha<=1 is not a full curve pass",
            "current_status": "curve_kernel_missing",
            "next_input": "K_R10(lambda), B_static(lambda), alpha_bound(lambda) curve",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "IF4547_2_PPN",
            "channel": "PPN",
            "4547_decision": "static B_static maps to scalar, vector, stress and anisotropy rows through separate kernels; alpha3 and xi are the tightest locks",
            "current_status": "projection_kernels_missing",
            "next_input": "K_alpha3, K_xi, K_zeta3, K_orbit_combo, no-cancellation policy",
            "valid_for_claim": "False",
        },
    ]


def input_acquisition_rows() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "ACQ4547_0_epsilon_U",
            "input": "epsilon_U = sup_Dloc U_B",
            "why_first": "sets every U_B^2 static residual scale",
            "source_or_method": "evaluate B_env/Pi_B on chosen local exterior domain or derive parent local-range bound",
            "status": "missing",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "ACQ4547_1_CHA1",
            "input": "C_H A_1",
            "why_first": "source leakage coefficient in B_src",
            "source_or_method": "parent leakage-coordinate norm plus source-map first derivative norm",
            "status": "missing",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "ACQ4547_2_mL_lap",
            "input": "D_m C_lap_m/L_B^2",
            "why_first": "spatial attractor homogeneity coefficient in B_mL",
            "source_or_method": "D_m, far-local gradient length, laplacian regularity constants",
            "status": "missing",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "ACQ4547_3_boundary_static",
            "input": "B_boundary_channel",
            "why_first": "alpha3/xi can be dominated by retained boundary vector/shear pieces",
            "source_or_method": "theorem-zero boundary nohair certificate or numeric product row",
            "status": "missing",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "ACQ4547_4_projection_kernel",
            "input": "K_channel",
            "why_first": "converts B_static norm into observable residual units",
            "source_or_method": "shared worldtube/profile projection into PPN/R10/Gdot kernels",
            "status": "missing",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG4547_0_projection_contract",
            "gate": "static residual projection contract",
            "status": "PASS_FORMULA_NONCLAIM",
            "meaning": "B_static has been mapped to PPN/Gdot/R10 inequality rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4547_1_numeric_bounds",
            "gate": "epsilon_U and coefficient numeric rows",
            "status": "BLOCKED_INPUTS_MISSING",
            "meaning": "epsilon_U, C_H A_1, D_m C_lap_m/L_B^2, boundary_static and kernels are not filled",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4547_2_R10",
            "gate": "R10/fifth-force pass",
            "status": "BLOCKED_CURVE_KERNEL_MISSING",
            "meaning": "single alpha<=1 anchor is smoke only; full lambda curve needed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4547_3_local_GR",
            "gate": "local GR/Newton/PPN",
            "status": "BLOCKED_NONCLAIM_PROJECTION_STAGE",
            "meaning": "projection equations exist, but no channel has score-ready values",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4547_0",
            "decision": DECISION,
            "meaning": "4547 converts the 4546 static residual envelope into arena-specific pass inequalities and epsilon_U bound formulas. This moves the branch toward actual scoring without inventing constants or retuning profiles per arena.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4547_0",
            "target": NEXT_TARGET,
            "objective": "fill the first epsilon_U/local-range row or run a symbolic static-bound smoke runner over the projection table",
            "derive_first": "derive or evaluate epsilon_U=sup_Dloc U_B on a named local exterior domain with source path",
            "fallback": "keep epsilon_U symbolic and run schema-only pass/fail smoke using ACQ4547 queue",
            "avoid": "turning alpha3/R10 anchors into claims without kernels and curve data",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT,
            "result": DECISION,
            "static_projection_contract_written": "True",
            "pass_inequality_rows_written": "True",
            "epsilon_U_bound_rows_written": "True",
            "numeric_epsilon_U_available": "False",
            "projection_kernels_available": "False",
            "R10_curve_ready": "False",
            "public_local_GR_claim_allowed": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    static_vector: list[dict[str, Any]],
    projections: list[dict[str, Any]],
    inequalities: list[dict[str, Any]],
    epsilon_bounds: list[dict[str, Any]],
    interfaces: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append({"validation_id": "VAL4547_00_sources", "status": "PASS" if source_ok else "FAIL", "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing"})

    bstatic = any(row["symbol"] == "B_static" and "epsilon_U^2" in row["definition"] for row in static_vector)
    checks.append({"validation_id": "VAL4547_01_static_vector", "status": "PASS" if bstatic else "FAIL", "detail": "shared B_static envelope is defined"})

    arenas = {row["effective_product"] for row in projections}
    projection_ok = {"C_Gamma_metric", "C_Gamma_vector", "C_Gamma_stress", "C_Gamma_Gdot", "C_Gamma_R10"}.issubset(arenas)
    checks.append({"validation_id": "VAL4547_02_projection_rows", "status": "PASS" if projection_ok else "FAIL", "detail": "PPN/Gdot/R10 projection rows are present"})

    inequalities_ok = any("alpha_bound(lambda)" in row["pass_inequality"] for row in inequalities) and any("2.42e-14" in row["pass_inequality"] for row in inequalities)
    checks.append({"validation_id": "VAL4547_03_pass_inequalities", "status": "PASS" if inequalities_ok else "FAIL", "detail": "R10 curve and Gdot lock inequalities are explicit"})

    eub_ok = any(row["observable"] == "alpha3" and "sqrt" in row["epsilon_U_bound_formula"] for row in epsilon_bounds) and any(row["observable"] == "Gdot_static_derivative" and "no epsilon_U-only bound" in row["epsilon_U_bound_formula"] for row in epsilon_bounds)
    checks.append({"validation_id": "VAL4547_04_epsilon_bounds", "status": "PASS" if eub_ok else "FAIL", "detail": "epsilon_U bound formulas include alpha3 and Gdot caveat"})

    interface_ok = any(row["channel"] == "R10" and "curve_kernel_missing" in row["current_status"] for row in interfaces)
    checks.append({"validation_id": "VAL4547_05_interfaces", "status": "PASS" if interface_ok else "FAIL", "detail": "R10 interface keeps curve requirement"})

    acquisition_ok = all(row["valid_for_claim"] == "False" for row in acquisition) and any(row["queue_id"] == "ACQ4547_0_epsilon_U" for row in acquisition)
    checks.append({"validation_id": "VAL4547_06_acquisition_queue", "status": "PASS" if acquisition_ok else "FAIL", "detail": "first numeric acquisition queue is explicit and nonclaim"})

    gates_ok = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gates)
    local_block = any(row["claim_gate_id"] == "CG4547_3_local_GR" and row["status"].startswith("BLOCKED") for row in gates)
    checks.append({"validation_id": "VAL4547_07_claim_firewall", "status": "PASS" if gates_ok and local_block else "FAIL", "detail": "no local GR/Newton/PPN claim from projection table"})

    csv_paths = [
        SOURCE_REGISTER,
        STATIC_VECTOR_CSV,
        ARENA_PROJECTION_CSV,
        PASS_INEQUALITY_CSV,
        EPSILON_BOUND_CSV,
        GDOT_R10_INTERFACE_CSV,
        INPUT_ACQUISITION_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
    ]
    csv_ok = True
    details: list[str] = []
    for path in csv_paths:
        try:
            if not read_csv(path):
                csv_ok = False
                details.append(f"{path.name}:empty")
        except Exception as exc:
            csv_ok = False
            details.append(f"{path.name}:{exc}")
    checks.append({"validation_id": "VAL4547_08_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(details)})

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append({"validation_id": "VAL4547_09_pycache_absent", "status": "PASS" if pycache_absent else "FAIL", "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present"})

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append({"validation_id": "VAL4547_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "4547 static residual projection and epsilon_U bound rows"})
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    static_vector: list[dict[str, Any]],
    projections: list[dict[str, Any]],
    inequalities: list[dict[str, Any]],
    epsilon_bounds: list[dict[str, Any]],
    interfaces: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4547 - Local static residual vector projection to PPN/Gdot/R10 or first numeric U-bound row

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4546 gave the static residual envelope:

```text
B_static := C_H A_1 epsilon_U^2
          + D_m C_lap_m epsilon_U^2/L_B^2
          + B_boundary_static
          + O(epsilon_U^3).
```

4547 turns that into arena pass rows. The shared rule is:

```text
Delta O_a = K_a B_static
```

with one shared source/profile object; no PPN/R10/Gdot retuning is allowed.

For a static channel, the generic pass inequality is:

```text
|K_a B_static| <= B_a.
```

Equivalently, if the boundary piece is separately zero/bounded:

```text
epsilon_U <= sqrt((B_a - B_boundary,a)
                  / (K_a (C_H A_1 + D_m C_lap_m/L_B^2))).
```

This is not a claim because `epsilon_U`, the coefficient products, boundary amplitudes and arena kernels are not filled. But it is now a scorer-shaped object. The tightest symbolic rows are `alpha3`, `xi`, `R10`, and the Gdot derivative caveat.

## Static Residual Vector

{markdown_table(static_vector)}

## Arena Projection Contract

{markdown_table(projections)}

## Pass Inequality Rows

{markdown_table(inequalities)}

## Epsilon_U Bound Rows

{markdown_table(epsilon_bounds)}

## Gdot/R10 Interface Decision

{markdown_table(interfaces)}

## Input Acquisition Queue

{markdown_table(acquisition)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_target)}

## Status

{markdown_table(status)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_projection_bound",
        "claim": "4547 maps the 4546 static residual envelope into PPN/Gdot/R10 pass inequalities and epsilon_U bound formulas using one shared source/profile object; no numeric claim is allowed until epsilon_U, kernels, coefficients and boundary rows are supplied.",
        "current_evidence": "Generated source register, static residual vector, arena projection contract, pass inequalities, epsilon_U bound rows, Gdot/R10 interface decision, acquisition queue, claim gates, status and validation CSVs.",
        "status": "projection_contract_and_epsilon_bound_rows_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Using symbolic epsilon_U formulas as local-GR evidence before local range and projection kernels are sourced.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "R10 curve, alpha3 boundary/domain rows and projection kernels remain missing.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    static_vector = static_vector_rows()
    projections = arena_projection_rows()
    inequalities = pass_inequality_rows()
    epsilon_bounds = epsilon_bound_rows()
    interfaces = gdot_r10_interface_rows()
    acquisition = input_acquisition_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(STATIC_VECTOR_CSV, static_vector)
    write_csv(ARENA_PROJECTION_CSV, projections)
    write_csv(PASS_INEQUALITY_CSV, inequalities)
    write_csv(EPSILON_BOUND_CSV, epsilon_bounds)
    write_csv(GDOT_R10_INTERFACE_CSV, interfaces)
    write_csv(INPUT_ACQUISITION_CSV, acquisition)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, static_vector, projections, inequalities, epsilon_bounds, interfaces, acquisition, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, static_vector, projections, inequalities, epsilon_bounds, interfaces, acquisition, gates, decisions, next_target, status, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4547 Local Static Residual Projection To PPN/Gdot/R10

Marker: `{MARKER}`  
4547 maps the shared `B_static = C_H A_1 epsilon_U^2 + D_m C_lap_m epsilon_U^2/L_B^2 + B_boundary_static + O(epsilon_U^3)` envelope into arena inequalities `|K_a B_static| <= B_a`. It writes first epsilon_U pass formulas for `alpha3`, `xi`, `R10` and the Gdot derivative caveat. No local claim is made because `epsilon_U`, kernels, coefficient products and boundary amplitudes remain missing. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4547 Packet Integration - Static Residual Scorer Contract

Marker: `{PACKET_MARKER}`  
The local packet now has a scorer-shaped static residual vector: one shared `B_static`, arena projection kernels, pass inequalities, and an acquisition queue. This is the bridge from derivation to empirical local tests, not a pass yet.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()

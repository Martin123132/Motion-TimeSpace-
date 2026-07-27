from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1401-Y5-R10-RAB-finite-EM-local-residual-source-map-and-PPN-pressure-gate.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1401_SOURCE_REGISTER.csv"
RESIDUAL_SOURCE_MAP_PATH = SRC_DIR / "P8_Y5_R10_1401_RESIDUAL_SOURCE_MAP.csv"
PRESSURE_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1401_PRESSURE_TARGET_LEDGER.csv"
PPN_GATE_PATH = SRC_DIR / "P8_Y5_R10_1401_PPN_PRESSURE_GATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1401_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1401_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1401_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1401_VALIDATION.csv"

STATUS = (
    "Y5_R10_1401_finite_EM_residual_source_map_and_PPN_pressure_gate_"
    "nonclaim_missing_tau_kernel_ppn_projection"
)
CLAIM_CEILING = (
    "finite_EM_residual_source_map_only_no_lambda_A_zero_no_alphaEM_bound_no_WEP_no_clock_"
    "no_R10_no_PPN_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1401_0_1400_doc",
        "source_path": "1400-Y5-R10-RAB-joined-EM-coupling-owner-contract-or-finite-local-residual-vector.md",
        "required_anchor": "NEXT1400_0_1401",
        "purpose": "handoff selecting finite EM residual source map and PPN pressure gate",
    },
    {
        "source_id": "SRC1401_1_1400_vector",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1400_FINITE_EM_LOCAL_RESIDUAL_VECTOR.csv",
        "required_anchor": "REM1400_9_local_PPN",
        "purpose": "authoritative finite EM residual vector",
    },
    {
        "source_id": "SRC1401_2_1400_gates",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1400_EM_LOCAL_ARENA_PROJECTION_GATES.csv",
        "required_anchor": "ELG1400_4_local_PPN",
        "purpose": "prior local PPN gate",
    },
    {
        "source_id": "SRC1401_3_988_joint",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv",
        "required_anchor": "JAV988_1_clock_product",
        "purpose": "clock product bound and cross-arena policy",
    },
    {
        "source_id": "SRC1401_4_988_WEP",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv",
        "required_anchor": "WEP988_WAS651_1_surface_binding",
        "purpose": "WEP beta_source pressure targets",
    },
    {
        "source_id": "SRC1401_5_989_beta_source",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_989_BETA_SOURCE_OWNER_LEDGER.csv",
        "required_anchor": "BSO989_4_failure_action",
        "purpose": "beta_source_alpha owner ledger and target-only status",
    },
    {
        "source_id": "SRC1401_6_1392_bulk_template",
        "source_path": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_1392_BULK_ALPHA_TEMPLATE_NONCLAIM.csv",
        "required_anchor": "K_bulk_ST(lambda)",
        "purpose": "R10 symbolic bulk alpha template",
    },
    {
        "source_id": "SRC1401_7_R10_anchor",
        "source_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
        "required_anchor": "R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM",
        "purpose": "R10 source-backed anchor-only bounds",
    },
    {
        "source_id": "SRC1401_8_R10_digitized",
        "source_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "required_anchor": "R10_BOUND_PLACEHOLDER_0",
        "purpose": "live R10 bound curve still placeholder invalid",
    },
    {
        "source_id": "SRC1401_9_1398_prior",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1398_LAMBDA_A_PRIOR_BOUND_VECTOR.csv",
        "required_anchor": "LAP1398_5_R10_bound_channel",
        "purpose": "finite lambda_A prior channels",
    },
    {
        "source_id": "SRC1401_10_this_script",
        "source_path": "scripts/Y5_R10_RAB_finite_EM_local_residual_source_map_and_PPN_pressure_gate.py",
        "required_anchor": "STATUS",
        "purpose": "1401 generator",
    },
]


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        columns = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: clean(row.get(column, "")) for column in columns})


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(clean(row.get(column, "")).replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def anchor_found(path: Path, anchor: str) -> bool:
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCE_ROWS:
        source_path = ROOT / source["source_path"]
        rows.append(
            {
                **source,
                "exists": str(source_path.exists()),
                "anchor_found": str(anchor_found(source_path, source["required_anchor"])),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def residual_source_map_rows() -> list[dict[str, str]]:
    return [
        {
            "map_id": "RSM1401_0_lambda_A",
            "residual_id": "REM1400_0_lambda_A",
            "quantity": "lambda_A",
            "source_status": "missing parent coefficient or zero theorem",
            "best_available_input": "none",
            "pressure_use": "cannot score; defines finite branch symbolically",
            "blocking_status": "MISSING_PARENT_COEFFICIENT",
            "next_action": "derive no-pullback/owner theorem or assign explicit nonclaim prior for sensitivity only",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "map_id": "RSM1401_1_norm_drift",
            "residual_id": "REM1400_1_norm_drift",
            "quantity": "rho_NQ",
            "source_status": "fixed generator norm missing",
            "best_available_input": "none",
            "pressure_use": "cannot separate from lambda_A in b_alpha_EM",
            "blocking_status": "MISSING_FIXED_N_Q",
            "next_action": "derive fixed T_Q norm or keep rho_NQ as explicit finite residual",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "map_id": "RSM1401_2_readout",
            "residual_id": "REM1400_2_readout",
            "quantity": "rho_readout",
            "source_status": "readout descent missing",
            "best_available_input": "none",
            "pressure_use": "prevents clock bounds from becoming alphaEM theorem bounds",
            "blocking_status": "MISSING_READOUT_DESCENT",
            "next_action": "derive Hodge/coframe/hbar*c quotient silence or source readout derivative",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "map_id": "RSM1401_3_b_alpha_EM",
            "residual_id": "REM1400_3_b_alpha_EM",
            "quantity": "b_alpha_EM",
            "source_status": "derivative map missing",
            "best_available_input": "clock product bound only: |b_alpha*tau_clock_time| <= 2.1e-18 yr^-1",
            "pressure_use": "clock pressure only; no standalone b_alpha_EM bound",
            "blocking_status": "PRODUCT_BOUND_ONLY",
            "next_action": "derive tau_clock/domain map before using clock as alphaEM bound",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "map_id": "RSM1401_4_beta_source_alpha",
            "residual_id": "REM1400_4_beta_source_alpha",
            "quantity": "beta_source_alpha",
            "source_status": "target-only WEP pressure",
            "best_available_input": "alpha-only <=4.797780522732e-05; robust surface-including <=2.887280314062e-05",
            "pressure_use": "survival target for finite branch, not a derived source normalization",
            "blocking_status": "TARGET_ONLY_NOT_DERIVED",
            "next_action": "derive source normalization owner or treat as explicit fitted/empirical parameter",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "map_id": "RSM1401_5_clock",
            "residual_id": "REM1400_5_clock",
            "quantity": "C_clock_EM",
            "source_status": "product bound only",
            "best_available_input": "JAV988_1 clock product row",
            "pressure_use": "clock pressure on b_alpha_EM*tau_clock",
            "blocking_status": "MISSING_TAU_CLOCK",
            "next_action": "derive tau_clock or local domain transfer before scoring",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "map_id": "RSM1401_6_WEP",
            "residual_id": "REM1400_6_WEP",
            "quantity": "C_WEP_EM",
            "source_status": "source/tau/binding map missing",
            "best_available_input": "MICROSCOPE-style pressure targets from 988 rows only",
            "pressure_use": "WEP pressure gate; no pass",
            "blocking_status": "MISSING_SOURCE_TAU_BINDING_MAP",
            "next_action": "derive beta_source_alpha*tau_WEP and normalized composition map",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "map_id": "RSM1401_7_beta_EM",
            "residual_id": "REM1400_7_beta_EM",
            "quantity": "beta_EM(lambda_A)",
            "source_status": "material binding map missing",
            "best_available_input": "symbolic beta_EM row from 1396/1400",
            "pressure_use": "feeds WEP and R10, cannot score",
            "blocking_status": "MISSING_BINDING_MAP",
            "next_action": "derive no-alpha matter vertex or source EM binding sensitivity coefficients",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "map_id": "RSM1401_8_R10",
            "residual_id": "REM1400_8_R10",
            "quantity": "C_R10_EM(lambda)",
            "source_status": "R10 kernel/tail/full bound curve missing",
            "best_available_input": "anchor-only noncurve rows plus invalid placeholder digitized curve",
            "pressure_use": "R10 pressure gate only",
            "blocking_status": "MISSING_KERNEL_TAIL_REAL_BOUND_CURVE",
            "next_action": "source K_bulk_ST(lambda), tail, beta maps, and full claim-ready R10 bound curve",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "map_id": "RSM1401_9_local_PPN",
            "residual_id": "REM1400_9_local_PPN",
            "quantity": "R_EM_local",
            "source_status": "explicit vector but unbounded",
            "best_available_input": "component-level pressure map from RSM1401_0 through RSM1401_8",
            "pressure_use": "local PPN/Newton/GR gate",
            "blocking_status": "LOCAL_VECTOR_UNBOUNDED",
            "next_action": "derive local projection coefficients A_gamma,A_beta,A_alpha1,A_G or block local-GR claim",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def pressure_target_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "PT1401_0_clock_product",
            "arena": "clock/fine-structure",
            "observable": "Yb+ E3/E2-style alpha product bookkeeping",
            "target_or_bound": "|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1",
            "source": "P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv::JAV988_1_clock_product",
            "claim_status": "PRODUCT_BOUND_ONLY_NOT_STANDALONE_ALPHA",
            "blocks": "b_alpha_EM;C_clock_EM;R_EM_local",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "target_id": "PT1401_1_WEP_alpha_only",
            "arena": "WEP",
            "observable": "alpha/Coulomb composition channel",
            "target_or_bound": "required_abs_beta_source_alpha <= 4.797780522732e-05",
            "source": "P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv::WEP988_WAS651_0_alpha_Coulomb",
            "claim_status": "TARGET_ONLY_SOURCE_NORMALIZATION_NOT_DERIVED",
            "blocks": "beta_source_alpha;C_WEP_EM;R_EM_local",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "target_id": "PT1401_2_WEP_robust_surface",
            "arena": "WEP",
            "observable": "surface/binding composition channel",
            "target_or_bound": "required_abs_beta_source_alpha <= 2.887280314062e-05",
            "source": "P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv::WEP988_WAS651_1_surface_binding",
            "claim_status": "TARGET_ONLY_SOURCE_NORMALIZATION_NOT_DERIVED",
            "blocks": "beta_source_alpha;beta_EM;C_WEP_EM;R_EM_local",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "target_id": "PT1401_3_R10_anchor_2020",
            "arena": "R10",
            "observable": "Eot-Wash 2020 alpha=1 threshold anchor",
            "target_or_bound": "alpha_bound=1 at lambda=3.86e-5 m",
            "source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM",
            "claim_status": "ANCHOR_ONLY_NON_CURVE",
            "blocks": "C_R10_EM(lambda);R_EM_local",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "target_id": "PT1401_4_R10_digitized_live",
            "arena": "R10",
            "observable": "live digitized alpha(lambda) curve",
            "target_or_bound": "MISSING_DIGITIZED_ALPHA_BOUND",
            "source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv::R10_BOUND_PLACEHOLDER_0",
            "claim_status": "PLACEHOLDER_INVALID",
            "blocks": "C_R10_EM(lambda);R_EM_local",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "target_id": "PT1401_5_local_PPN",
            "arena": "local PPN/Newton/GR",
            "observable": "PPN residual vector from finite EM coupling branch",
            "target_or_bound": "MISSING_LOCAL_PROJECTION_THRESHOLDS",
            "source": "P8_Y5_R10_1400_FINITE_EM_LOCAL_RESIDUAL_VECTOR.csv::REM1400_9_local_PPN",
            "claim_status": "NO_PPN_PRESSURE_NUMBERS_YET",
            "blocks": "local GR/Newton/PPN claim",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def ppn_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "PPN1401_0_gamma",
            "ppn_or_local_channel": "gamma-1 / spatial curvature per unit mass",
            "residual_dependency": "A_gamma · R_EM_local",
            "needed_projection": "A_gamma(lambda_A,rho_NQ,rho_readout,b_alpha,beta_source,C_WEP,beta_EM)",
            "current_status": "MISSING_LOCAL_PROJECTION_COEFFICIENT",
            "pressure_result": "BLOCKED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "PPN1401_1_beta",
            "ppn_or_local_channel": "beta-1 / nonlinear superposition",
            "residual_dependency": "A_beta · R_EM_local + quadratic finite-EM terms",
            "needed_projection": "A_beta and quadratic local source coefficients",
            "current_status": "MISSING_LOCAL_PROJECTION_COEFFICIENT",
            "pressure_result": "BLOCKED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "PPN1401_2_alpha1_alpha2",
            "ppn_or_local_channel": "preferred-frame / source-current residuals",
            "residual_dependency": "current/readout components beta_source_alpha and rho_readout",
            "needed_projection": "source-current owner or preferred-frame projection map",
            "current_status": "MISSING_CURRENT_READOUT_OWNER",
            "pressure_result": "BLOCKED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "PPN1401_3_WEP_local",
            "ppn_or_local_channel": "composition-dependent free fall",
            "residual_dependency": "C_WEP_EM and beta_EM(lambda_A)",
            "needed_projection": "composition charge normalization and tau_WEP local domain map",
            "current_status": "TARGET_ONLY_NOT_PASS",
            "pressure_result": "BLOCKED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "PPN1401_4_effective_G",
            "ppn_or_local_channel": "effective Newton coupling / inverse-square leakage",
            "residual_dependency": "C_R10_EM(lambda) and local finite-range tail",
            "needed_projection": "finite-range-to-local limit, K_bulk_ST(lambda), epsilon_tail, real bound curve",
            "current_status": "R10_NOT_SCOREABLE",
            "pressure_result": "BLOCKED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "PPN1401_5_verdict",
            "ppn_or_local_channel": "local GR/Newton/PPN reentry",
            "residual_dependency": "all components of R_EM_local",
            "needed_projection": "every component theorem-zero, source-backed bounded, or below threshold",
            "current_status": "PPN_PRESSURE_GATE_WRITTEN_NO_PASS",
            "pressure_result": "LOCAL_GR_BLOCKED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "claim_id": "GATE1401_0_residual_complete",
            "claim": "R_EM_local is fully sourced/bounded",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "lambda_A, rho_NQ, rho_readout, b_alpha_EM, beta_EM, R10 kernel/tail, and PPN projections are missing",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1401_1_clock",
            "claim": "clock/fine-structure branch passes",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "only product bound exists; standalone b_alpha_EM and tau_clock map missing",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1401_2_WEP",
            "claim": "WEP branch passes",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "beta_source targets are pressure-only and source/tau/binding maps are missing",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1401_3_R10",
            "claim": "R10 alpha(lambda) branch passes",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "bound curve is placeholder-invalid and MTS R10 alpha remains symbolic",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1401_4_local_GR",
            "claim": "local GR/Newton/PPN reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "PPN pressure projections are missing and R_EM_local is unbounded",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1401_0_pressure_status",
            "decision": "keep finite EM branch as pressure map only",
            "reason": "some targets exist, but all claim-critical transfer maps are missing",
            "consequence": "no empirical or local-GR pass from 1401",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1401_1_first_bottleneck",
            "decision": "attack the shared tau/domain transfer next",
            "reason": "clock, WEP, R10, and local PPN cannot be compared until tau_clock, tau_WEP, tau_R10, and local projection domains are related or explicitly separated",
            "consequence": "next target is a domain/tau transfer theorem or arena isolation ledger",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1401_2_R10_policy",
            "decision": "do not run R10 as a claim",
            "reason": "R10 bound curve is still placeholder-invalid and MTS alpha(lambda) is symbolic",
            "consequence": "R10 remains a future smoke-test lane only",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1401_0_1402",
            "target_doc": "1402-Y5-R10-RAB-local-domain-tau-transfer-theorem-or-arena-isolation-ledger.md",
            "target_script": "scripts/Y5_R10_RAB_local_domain_tau_transfer_theorem_or_arena_isolation_ledger.py",
            "task": "derive or reject a shared local domain/tau transfer map tying tau_clock, tau_WEP, tau_R10, and local PPN projections for the finite EM branch",
            "success_condition": "either one parent domain map allows cross-arena pressure comparison, or each arena is explicitly isolated so clock screening cannot be misused as WEP/R10/local relief",
            "do_not_claim": "lambda_A=0;alphaEM bound;WEP pass;clock pass;R10 pass;PPN pass;Newton limit;local GR;q_loc=0;GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, str]],
    residual_map: list[dict[str, str]],
    targets: list[dict[str, str]],
    ppn: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    residual_ids = {row["residual_id"] for row in residual_map}
    expected_core = {
        "REM1400_0_lambda_A",
        "REM1400_1_norm_drift",
        "REM1400_2_readout",
        "REM1400_3_b_alpha_EM",
        "REM1400_4_beta_source_alpha",
        "REM1400_5_clock",
        "REM1400_6_WEP",
        "REM1400_7_beta_EM",
        "REM1400_8_R10",
        "REM1400_9_local_PPN",
    }
    residual_complete = expected_core == residual_ids
    residual_nonclaim = all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in residual_map)
    target_nonclaim = all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in targets)
    has_clock_target = any(row["target_id"] == "PT1401_0_clock_product" and "2.1e-18" in row["target_or_bound"] for row in targets)
    has_wep_targets = any(row["target_id"] == "PT1401_1_WEP_alpha_only" and "4.797780522732e-05" in row["target_or_bound"] for row in targets) and any(row["target_id"] == "PT1401_2_WEP_robust_surface" and "2.887280314062e-05" in row["target_or_bound"] for row in targets)
    has_r10_block = any(row["target_id"] == "PT1401_4_R10_digitized_live" and row["claim_status"] == "PLACEHOLDER_INVALID" for row in targets)
    ppn_blocked = all(row["claim_allowed"] == "False" and row["pressure_result"] in {"BLOCKED", "LOCAL_GR_BLOCKED"} for row in ppn)
    gate_blocked = all(row["claim_allowed"] == "False" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        RESIDUAL_SOURCE_MAP_PATH,
        PRESSURE_TARGET_PATH,
        PPN_GATE_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    scope_ok = all("formalization-workbench" not in str(ROOT / path) for path in output_paths)
    all_ok = (
        source_ok
        and residual_complete
        and residual_nonclaim
        and target_nonclaim
        and has_clock_target
        and has_wep_targets
        and has_r10_block
        and ppn_blocked
        and gate_blocked
        and scope_ok
    )
    now = datetime.now(timezone.utc).isoformat()
    return [
        {
            "check_id": "VAL1401_0_sources",
            "status": "PASS" if source_ok else "FAIL",
            "detail": "all cited source paths exist and anchors are present",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1401_1_residual_map",
            "status": "PASS" if residual_complete and residual_nonclaim else "FAIL",
            "detail": "all ten REM1400 components are mapped and remain nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1401_2_pressure_targets",
            "status": "PASS" if target_nonclaim and has_clock_target and has_wep_targets and has_r10_block else "FAIL",
            "detail": "clock/WEP pressure targets are imported and R10 live curve remains placeholder-blocked",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1401_3_ppn_gate",
            "status": "PASS" if ppn_blocked else "FAIL",
            "detail": "PPN pressure gate is written and blocks local-GR claims",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1401_4_claim_refusal",
            "status": "PASS" if gate_blocked else "FAIL",
            "detail": "clock, WEP, R10, PPN, Newton, and local-GR claims are refused",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1401_5_scope",
            "status": "PASS" if scope_ok else "FAIL",
            "detail": "outputs are confined to post-checkpoint-work paths",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1401_6_overall",
            "status": "PASS" if all_ok else "FAIL",
            "detail": "1401 turns R_EM_local into a source/pressure map without promoting empirical or local claims",
            "generated_utc": now,
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    residual_map: list[dict[str, str]],
    targets: list[dict[str, str]],
    ppn: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    body = f"""# 1401 Y5 R10 RAB: Finite EM Local Residual Source Map And PPN Pressure Gate

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

**Current verdict:** `R_EM_local` is now pressure-mapped, not solved. Clock and WEP supply useful stress targets, but they are product/target-only; R10 remains blocked by symbolic MTS alpha and a placeholder-invalid live bound curve; local PPN has no projection coefficients yet.

**Discipline move:** every finite EM residual component is now classified as theorem-zero, source-backed, target-only, product-only, or missing. At present none are claim-ready, so the finite EM branch remains a test discipline tool rather than a GR/Newton pass.

## Source Register

{md_table(sources)}

## Residual Source Map

{md_table(residual_map)}

## Pressure Target Ledger

{md_table(targets)}

## PPN Pressure Gate

{md_table(ppn)}

## Claim Gates

{md_table(gates)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    residual_map = residual_source_map_rows()
    targets = pressure_target_rows()
    ppn = ppn_gate_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, residual_map, targets, ppn, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(RESIDUAL_SOURCE_MAP_PATH, residual_map)
    write_csv(PRESSURE_TARGET_PATH, targets)
    write_csv(PPN_GATE_PATH, ppn)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, residual_map, targets, ppn, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1401 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()

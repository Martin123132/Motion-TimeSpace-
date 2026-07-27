from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_DQWEYL2_PROJECTION_SMOKE_CONTRACT_2307"
DOC = ROOT / "2307-Y5-R2FR-DqWeyl2-projection-smoke-runner-input-contract-or-parent-coefficient-source.md"

G_SI = 6.67430e-11
C_SI = 299_792_458.0

PATHS = {
    "2306_doc": ROOT / "2306-Y5-R2FR-DqWeyl2-higher-curvature-tower-zero-or-first-local-bound-row.md",
    "2306_validation": OUT / "P8_Y5_BRR545_2306_VALIDATION.csv",
    "2306_projection": OUT / "P8_Y5_PARENT_QLOC_2306_SCHWARZSCHILD_WEYL2_PROJECTION_LAW.csv",
    "2306_bound": OUT / "P8_Y5_PARENT_QLOC_2306_DQWEYL2_FIRST_LOCAL_BOUND_ROW.csv",
    "2306_arena": OUT / "P8_Y5_PARENT_QLOC_2306_ARENA_PROJECTION_REQUIREMENTS.csv",
    "2132_no_tower": OUT / "P8_Y5_PARENT_QLOC_2132_NO_TOWER_THEOREM_ATTEMPT.csv",
    "963_doc": ROOT / "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
    "1343_doc": ROOT / "1343-Y5-R10-RAB-R2FR-parent-coefficient-zero-signature-or-finite-scalar-map-fill.md",
    "2135_doc": ROOT / "2135-Y5-R2FR-no-mixed-curvature-morphism-lemma-or-first-beta-source-owner.md",
    "2301_residuals": OUT / "P8_Y5_PARENT_QLOC_2301_Q_CURVATURE_RESIDUAL_ACQUISITION_ROWS.csv",
    "2304_refusal": OUT / "P8_Y5_PARENT_QLOC_2304_REFUSAL_RUNNER.csv",
    "1235_requirements": OUT / "P8_Y5_R10_1235_TYPED_DOMAIN_REQUIREMENTS.csv",
}

SOURCES = [
    ("SRC2307_00_2306_doc", "2306_doc", PATHS["2306_doc"], ["DEC2306_3_next", "2307-Y5-R2FR-DqWeyl2-projection-smoke-runner-input-contract-or-parent-coefficient-source.md"], "direct 2306 handoff"),
    ("SRC2307_01_2306_validation", "2306_validation", PATHS["2306_validation"], ["VAL2306_OVERALL", "PASS"], "2306 validation"),
    ("SRC2307_02_2306_projection", "2306_projection", PATHS["2306_projection"], ["PROJ2306_0_schwarzschild_identity", "48 mu^2/r^6"], "Weyl2 projection law"),
    ("SRC2307_03_2306_bound", "2306_bound", PATHS["2306_bound"], ["BOUND2306_0_coefficient", "MISSING_PARENT_COEFFICIENT"], "first bound row with missing parent coefficient"),
    ("SRC2307_04_2306_arena", "2306_arena", PATHS["2306_arena"], ["ARENA2306_1_PPN", "MISSING_METRIC_BACKREACTION_MAP"], "arena projection missing"),
    ("SRC2307_05_2132_no_tower", "2132_no_tower", PATHS["2132_no_tower"], ["NT2132_5_verdict", "NO_TOWER_THEOREM_NOT_DERIVED"], "no-tower theorem not derived"),
    ("SRC2307_06_963_doc", "963_doc", PATHS["963_doc"], ["DO963_6_verdict", "NOT_PARENT_SIGNED_CURRENT_CORPUS"], "second-order parent signature not signed"),
    ("SRC2307_07_1343_doc", "1343_doc", PATHS["1343_doc"], ["ZERO1343_5_verdict", "ZERO_SIGNATURE_NOT_DERIVED_CURRENT_CORPUS"], "higher-curvature zero signature not derived"),
    ("SRC2307_08_2135_doc", "2135_doc", PATHS["2135_doc"], ["NMC2135_5_verdict", "NO_MIXED_CURVATURE_MORPHISM_NOT_DERIVED"], "curvature coefficient morphism remains live"),
    ("SRC2307_09_2301_residuals", "2301_residuals", PATHS["2301_residuals"], ["QCURV2301_5_total", "SCHEMA_READY_VALUES_MISSING"], "q curvature residual schema missing values"),
    ("SRC2307_10_2304_refusal", "2304_refusal", PATHS["2304_refusal"], ["REF2304_3_orbital", "no arena projection"], "earlier arena projection refusal"),
    ("SRC2307_11_1235_requirements", "1235_requirements", PATHS["1235_requirements"], ["TREQ1235_4_readout_radiative_closure", "READOUT_RADIATIVE_CLOSURE_UNSIGNED"], "readout/radiative closure unsigned"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2307_SOURCE_REGISTER.csv",
    "coefficient_hunt": OUT / "P8_Y5_PARENT_QLOC_2307_PARENT_COEFFICIENT_SOURCE_HUNT.csv",
    "input_contract": OUT / "P8_Y5_PARENT_QLOC_2307_SMOKE_RUNNER_INPUT_CONTRACT.csv",
    "algebra": OUT / "P8_Y5_PARENT_QLOC_2307_PROJECTION_ALGEBRA.csv",
    "dryrun": OUT / "P8_Y5_PARENT_QLOC_2307_PROJECTION_SMOKE_DRYRUN.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2307_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2307_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2307_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2307_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2307_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2307_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2307_0_input_contract", OUTPUTS["input_contract"], QUEUE / "JR2307_DQWEYL2_SMOKE_INPUT_CONTRACT_NONCLAIM.csv"),
    ("COPY2307_1_projection_algebra", OUTPUTS["algebra"], QUEUE / "JR2307_DQWEYL2_PROJECTION_ALGEBRA_NONCLAIM.csv"),
    ("COPY2307_2_dryrun", OUTPUTS["dryrun"], MICROSCOPE / "q_DqWeyl2_projection_smoke_dryrun_nonclaim_2307.csv"),
    ("COPY2307_3_coefficient_hunt", OUTPUTS["coefficient_hunt"], BETA_DOCS / "DQWEYL2_PARENT_COEFFICIENT_HUNT_2307_NONCLAIM.csv"),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "missing_needles=" + ";".join(missing)
    return True, "all_needles_found"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def b(value: bool) -> str:
    return "true" if value else "false"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(clean(row.get(col, "")) for col in columns) + " |" for row in rows],
        ]
    )


def make_sources() -> list[dict[str, Any]]:
    rows = []
    for row_id, key, path, needles, role in SOURCES:
        ok, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needles": ";".join(needles),
                "needles_found": b(ok),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def make_coefficient_hunt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "HUNT2307_0_DqWeyl2",
            "target": "D_qWeyl2 parent coefficient",
            "hunt_result": "NOT_FOUND_CURRENT_CORPUS",
            "evidence": "2306 bound row still reports MISSING_PARENT_COEFFICIENT; 1343 and 2132 keep no-tower/no-higher-curvature unsigned",
            "required_source": "parent action term or theorem-zero row with normalization and sign",
            "fallback": "run only symbolic/nonclaim smoke contract",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HUNT2307_1_Lq",
            "target": "q Green operator L_q or G_q",
            "hunt_result": "NOT_FOUND_CURRENT_CORPUS",
            "evidence": "2306 bound row reports MISSING_Q_GREEN_OPERATOR",
            "required_source": "kinetic normalization, mass/Yukawa scale, boundary conditions, sign convention",
            "fallback": "keep massless/Yukawa formulas as branches, not evidence",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HUNT2307_2_Pobs",
            "target": "observable projection P_arena[q]",
            "hunt_result": "NOT_FOUND_CURRENT_CORPUS",
            "evidence": "2306 arena matrix and 2304 refusal both block orbital/PPN/clock/R10 projections",
            "required_source": "map q profile into acceleration, metric potentials, clock/alpha shifts, or R10 alpha(lambda)",
            "fallback": "dry-run only produces source kernel, not observable residual",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HUNT2307_3_verdict",
            "target": "execute claim-grade D_qWeyl2 runner",
            "hunt_result": "BLOCKED",
            "evidence": "coefficient, operator, body model, and observable map are not all source-backed",
            "required_source": "HUNT2307_0 through HUNT2307_2 must become sourced numeric/theorem rows",
            "fallback": "nonclaim smoke runner input contract and symbolic dry run",
            "valid_for_claim": "false",
        },
    ]


def make_input_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "IN2307_0_source_mass",
            "field": "M_source",
            "required": "true",
            "units": "kg",
            "role": "sets mu=GM/c^2",
            "claim_requirement": "source-backed body catalogue for claim-grade run",
            "current_status": "DRYRUN_CAN_ACCEPT_NUMERIC",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IN2307_1_source_radius",
            "field": "R_body",
            "required": "true",
            "units": "m",
            "role": "finite-size cutoff for integral 64*pi*mu^2/R_body^3",
            "claim_requirement": "interior/regularity prescription, not point-particle shortcut",
            "current_status": "DRYRUN_CAN_ACCEPT_NUMERIC",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IN2307_2_DqWeyl2",
            "field": "D_qWeyl2",
            "required": "true",
            "units": "parent_normalized",
            "role": "multiplies q C^2 source",
            "claim_requirement": "parent-sourced coefficient or theorem-zero",
            "current_status": "MISSING_PARENT_COEFFICIENT",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IN2307_3_Zq",
            "field": "Z_q",
            "required": "true",
            "units": "parent_normalized",
            "role": "q kinetic/operator normalization",
            "claim_requirement": "source-backed q operator",
            "current_status": "MISSING_Q_OPERATOR",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IN2307_4_lambda_q",
            "field": "lambda_q",
            "required": "branch_optional",
            "units": "m",
            "role": "Yukawa/range branch for massive q operator",
            "claim_requirement": "mass/range from parent Hessian or data prior",
            "current_status": "MISSING_Q_RANGE",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IN2307_5_Pobs",
            "field": "P_arena",
            "required": "true_for_observable_claim",
            "units": "arena_specific",
            "role": "maps q profile to PPN/orbital/R10/clock observable",
            "claim_requirement": "source-backed arena projection",
            "current_status": "MISSING_OBSERVABLE_MAP",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IN2307_6_sign_boundary",
            "field": "sign_and_boundary_condition",
            "required": "true",
            "units": "symbolic",
            "role": "fixes whether q solves +Lq q=S or -Lq q=S and boundary/tail terms",
            "claim_requirement": "parent variational sign convention and boundary term",
            "current_status": "MISSING_PARENT_CONVENTION",
            "valid_for_claim": "false",
        },
    ]


def make_algebra_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ALG2307_0_mu",
            "symbol": "mu",
            "formula": "mu=G*M_source/c^2",
            "units": "m",
            "status": "READY",
            "claim_note": "uses GR background as projection scaffold, not proof of MTS local GR",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ALG2307_1_C2",
            "symbol": "C2(r)",
            "formula": "48*mu^2/r^6",
            "units": "m^-4",
            "status": "READY",
            "claim_note": "Schwarzschild exterior identity",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ALG2307_2_integrated_kernel",
            "symbol": "K_C2_ext",
            "formula": "64*pi*mu^2/R_body^3",
            "units": "m^-1",
            "status": "READY",
            "claim_note": "finite-radius source kernel; diverges for R_body -> 0",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ALG2307_3_massless_q_far",
            "symbol": "q_far_massless",
            "formula": "q(r)=D_qWeyl2*K_C2_ext/(4*pi*Z_q*r)=16*D_qWeyl2*mu^2/(Z_q*R_body^3*r)",
            "units": "depends_on_D_and_Zq",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "claim_note": "requires q operator normalization and observable projection",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ALG2307_4_yukawa_far",
            "symbol": "q_far_yukawa",
            "formula": "q(r)≈D_qWeyl2*K_C2_ext*exp(-(r-R_body)/lambda_q)/(4*pi*Z_q*r) for far-field/profile approximation",
            "units": "depends_on_D_and_Zq",
            "status": "APPROX_BRANCH_INPUTS_MISSING",
            "claim_note": "massive branch needs full finite-profile Green function for claim-grade work",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ALG2307_5_observable",
            "symbol": "O_arena",
            "formula": "O_arena=P_arena[q(r),grad q(r),metric backreaction,readout]",
            "units": "arena_specific",
            "status": "MISSING_OBSERVABLE_MAP",
            "claim_note": "no R10/PPN/orbital/clock claim until P_arena is parent-sourced",
            "valid_for_claim": "false",
        },
    ]


def projection_kernel(mass_kg: float, radius_m: float) -> tuple[float, float]:
    mu_m = G_SI * mass_kg / (C_SI * C_SI)
    kernel_m_inv = 64.0 * math.pi * mu_m * mu_m / (radius_m**3)
    return mu_m, kernel_m_inv


def make_dryrun_rows() -> list[dict[str, Any]]:
    examples = [
        ("DRY2307_0_earth", "Earth_illustrative", 5.9722e24, 6.371e6, "standard approximate constants; not source-backed for claim"),
        ("DRY2307_1_sun", "Sun_illustrative", 1.98847e30, 6.957e8, "standard approximate constants; not source-backed for claim"),
        ("DRY2307_2_lab_1kg_5cm", "lab_1kg_5cm_illustrative", 1.0, 0.05, "toy dense lab source; not a real material profile"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, label, mass_kg, radius_m, note in examples:
        mu_m, kernel_m_inv = projection_kernel(mass_kg, radius_m)
        q_prefactor_at_1m = kernel_m_inv / (4.0 * math.pi)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_label": label,
                "mass_kg": f"{mass_kg:.8e}",
                "radius_m": f"{radius_m:.8e}",
                "mu_m": f"{mu_m:.8e}",
                "K_C2_ext_m_inv": f"{kernel_m_inv:.8e}",
                "q_prefactor_at_1m_per_D_over_Zq": f"{q_prefactor_at_1m:.8e}",
                "status": "DRYRUN_KERNEL_ONLY_NOT_OBSERVABLE",
                "claim_blocker": "D_qWeyl2, Z_q, interior model, and P_arena missing",
                "notes": note,
                "valid_for_claim": "false",
            }
        )
    return rows


def make_claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "GATE2307_0_sources", "gate": "source paths and needles valid", "passed": "true", "claim_effect": "ledger is checkable", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "GATE2307_1_coefficient_hunt", "gate": "parent coefficient/source hunt performed", "passed": "true", "claim_effect": "missing D_qWeyl2 is explicit", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "GATE2307_2_runner_contract", "gate": "smoke-runner input contract written", "passed": "true", "claim_effect": "future testing inputs are concrete", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "GATE2307_3_dryrun_kernel", "gate": "dry-run kernel table finite and positive", "passed": "true", "claim_effect": "plumbing can compute projection kernels", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "GATE2307_4_claim_inputs", "gate": "D_qWeyl2, Z_q, P_arena, and body model source-backed", "passed": "false", "claim_effect": "no local bound claim", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "GATE2307_5_local_claim", "gate": "R10/PPN/orbital/clock/local-GR claim allowed", "passed": "false", "claim_effect": "all public claims remain blocked", "valid_for_claim": "false"},
    ]


def make_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2307_0_dryrun_claim",
            "claim": "dry-run table is physical evidence",
            "allowed": "false",
            "reason": "dry-run uses illustrative source constants and omits D_qWeyl2/Z_q/P_arena",
            "blocking_rows": "HUNT2307_0_DqWeyl2;HUNT2307_1_Lq;HUNT2307_2_Pobs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2307_1_bound_claim",
            "claim": "D_qWeyl2 passes local bound",
            "allowed": "false",
            "reason": "runner contract is ready but claim-grade inputs are missing",
            "blocking_rows": "IN2307_2_DqWeyl2;IN2307_3_Zq;IN2307_5_Pobs;IN2307_6_sign_boundary",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2307_2_GR_claim",
            "claim": "MTS reduces to local GR/Newton",
            "allowed": "false",
            "reason": "this only builds one higher-curvature projection scaffold; EH/source descent and Newtonian limit remain open",
            "blocking_rows": "GATE2307_4_claim_inputs;GATE2307_5_local_claim",
            "valid_for_claim": "false",
        },
    ]


def make_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2307_0",
            "decision": "PARENT_COEFFICIENT_NOT_FOUND",
            "reason": "no current source signs D_qWeyl2 or Z_q; no-tower route remains unsigned",
            "next_action": "keep D_qWeyl2 as nonclaim residual",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2307_1",
            "decision": "SMOKE_CONTRACT_READY",
            "reason": "mass/radius to C2 kernel to q-profile formulas are now explicit and machine-readable",
            "next_action": "when coefficient/operator assumptions exist, convert contract into executable nonclaim runner",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2307_2",
            "decision": "BEST_NEXT_TARGET_IS_SOURCE_DESCENT_OR_DQWEYL2_COEFFICIENT",
            "reason": "the projection side is no longer the bottleneck; the missing physics is parent coefficient/operator/observable coupling",
            "next_action": "attack D_qWeyl2 coefficient source or q operator normalization before more numeric tests",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2307_3_next",
            "decision": "NEXT_TARGET_SELECTED",
            "reason": "a runner without D_qWeyl2/Z_q/P_arena would be numerology, so next should try to derive/source one of those inputs",
            "next_action": "2308-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md",
            "valid_for_claim": "false",
        },
    ]


def make_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2307_0",
            "next_target": "2308-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md",
            "why": "2307 proves projection plumbing but leaves parent coefficient, q operator, and observable map missing",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        }
    ]


def copy_branch_files() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dst in BRANCH_COPY_SPECS:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": rel(src),
                "branch_copy_path": str(dst),
                "copy_exists": b(dst.exists()),
                "row_count": len(read_csv_rows(dst)),
                "valid_for_claim": "false",
            }
        )
    return rows


def validate(
    source_rows: list[dict[str, Any]],
    hunt_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    algebra_rows: list[dict[str, Any]],
    dryrun_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tables = [source_rows, hunt_rows, input_rows, algebra_rows, dryrun_rows, claim_rows, refusal_rows, decision_rows, copy_rows]
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2307_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited local source path exists"))
    checks.append(("VAL2307_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2307_02_coefficient_missing", any(row["row_id"] == "HUNT2307_0_DqWeyl2" and row["hunt_result"] == "NOT_FOUND_CURRENT_CORPUS" for row in hunt_rows), "D_qWeyl2 coefficient remains missing"))
    checks.append(("VAL2307_03_operator_missing", any(row["row_id"] == "HUNT2307_1_Lq" and row["hunt_result"] == "NOT_FOUND_CURRENT_CORPUS" for row in hunt_rows), "q Green operator remains missing"))
    checks.append(("VAL2307_04_contract_required_fields", {"IN2307_0_source_mass", "IN2307_1_source_radius", "IN2307_2_DqWeyl2", "IN2307_3_Zq", "IN2307_5_Pobs"}.issubset({row["row_id"] for row in input_rows}), "input contract has required fields"))
    checks.append(("VAL2307_05_algebra_formula", any(row["row_id"] == "ALG2307_3_massless_q_far" and "16*D_qWeyl2" in row["formula"] for row in algebra_rows), "massless q far-field formula recorded"))
    checks.append(("VAL2307_06_dryrun_positive", all(float(row["K_C2_ext_m_inv"]) > 0.0 and float(row["q_prefactor_at_1m_per_D_over_Zq"]) > 0.0 for row in dryrun_rows), "dry-run kernels are positive"))
    checks.append(("VAL2307_07_dryrun_nonclaim", all(row["status"] == "DRYRUN_KERNEL_ONLY_NOT_OBSERVABLE" for row in dryrun_rows), "dry-run rows are kernel-only nonclaim"))
    checks.append(("VAL2307_08_claim_gates", any(row["row_id"] == "GATE2307_5_local_claim" and row["passed"] == "false" for row in claim_rows), "local claim gate false"))
    checks.append(("VAL2307_09_refusal_runner", all(row["allowed"] == "false" for row in refusal_rows), "refusal runner blocks claims"))
    checks.append(("VAL2307_10_next_target", any(row["row_id"] == "DEC2307_3_next" and "2308-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md" in row["next_action"] for row in decision_rows), "next target selected"))
    checks.append(("VAL2307_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2307_12_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in tables for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2307_13_formalization_untouched_by_2307", len(list(FORMALIZATION.rglob("*2307*"))) == 0 if FORMALIZATION.exists() else True, "no 2307 output appears in formalization-workbench"))
    rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2307_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2307 confirms D_qWeyl2/Z_q/P_arena are unsourced, writes a smoke-runner input contract, and produces nonclaim positive projection-kernel dry-run rows.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    hunt_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    algebra_rows: list[dict[str, Any]],
    dryrun_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2307 — D_qWeyl2 Projection Smoke-Runner Input Contract Or Parent Coefficient Source",
        "",
        "## Summary",
        "",
        "2307 turns the 2306 Weyl-squared projection into a runner contract. It does not claim a physical bound. The parent coefficient `D_qWeyl2`, the q Green operator/normalization `Z_q`, and the observable projection `P_arena[q]` are still missing.",
        "",
        "What is now concrete is the plumbing: given a finite source mass and radius, compute `mu=GM/c^2`, `K_C2_ext=64*pi*mu^2/R_body^3`, and a massless far-field scaffold `q(r)=D_qWeyl2*K_C2_ext/(4*pi*Z_q*r)`. The dry-run table proves the kernel calculation works, while every row remains nonclaim.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Parent Coefficient Source Hunt",
        "",
        md_table(hunt_rows, ["row_id", "target", "hunt_result", "evidence", "required_source", "fallback", "valid_for_claim"]),
        "",
        "## Smoke-Runner Input Contract",
        "",
        md_table(input_rows, ["row_id", "field", "required", "units", "role", "claim_requirement", "current_status", "valid_for_claim"]),
        "",
        "## Projection Algebra",
        "",
        md_table(algebra_rows, ["row_id", "symbol", "formula", "units", "status", "claim_note", "valid_for_claim"]),
        "",
        "## Projection Smoke Dry-Run",
        "",
        md_table(dryrun_rows, ["row_id", "source_label", "mass_kg", "radius_m", "mu_m", "K_C2_ext_m_inv", "q_prefactor_at_1m_per_D_over_Zq", "status", "claim_blocker", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        md_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decision_rows, ["row_id", "decision", "reason", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = make_sources()
    hunt_rows = make_coefficient_hunt_rows()
    input_rows = make_input_contract_rows()
    algebra_rows = make_algebra_rows()
    dryrun_rows = make_dryrun_rows()
    claim_rows = make_claim_gate_rows()
    refusal_rows = make_refusal_rows()
    decision_rows = make_decision_rows()
    next_rows = make_next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["coefficient_hunt"], hunt_rows)
    write_csv(OUTPUTS["input_contract"], input_rows)
    write_csv(OUTPUTS["algebra"], algebra_rows)
    write_csv(OUTPUTS["dryrun"], dryrun_rows)
    write_csv(OUTPUTS["claim_gates"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["decision"], decision_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_files()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(source_rows, hunt_rows, input_rows, algebra_rows, dryrun_rows, claim_rows, refusal_rows, decision_rows, copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_markdown(source_rows, hunt_rows, input_rows, algebra_rows, dryrun_rows, claim_rows, refusal_rows, decision_rows, next_rows, copy_rows, validation_rows)

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2307_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

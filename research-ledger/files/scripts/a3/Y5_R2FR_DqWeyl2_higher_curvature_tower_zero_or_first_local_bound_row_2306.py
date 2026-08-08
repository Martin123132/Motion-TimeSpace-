from __future__ import annotations

import csv
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

BRANCH_ID = "MTS_R2FR_DQWEYL2_TOWER_OR_LOCAL_BOUND_2306"
DOC = ROOT / "2306-Y5-R2FR-DqWeyl2-higher-curvature-tower-zero-or-first-local-bound-row.md"

PATHS = {
    "2305_doc": ROOT / "2305-Y5-R2FR-BqWeyl-linear-zero-typed-grammar-signature-or-quadratic-Weyl-residual-row.md",
    "2305_validation": OUT / "P8_Y5_BRR545_2305_VALIDATION.csv",
    "2305_quadratic": OUT / "P8_Y5_PARENT_QLOC_2305_QUADRATIC_WEYL_RESIDUAL_ROW.csv",
    "2305_next": OUT / "P8_Y5_PARENT_QLOC_2305_NEXT_TARGET.csv",
    "2132_no_tower": OUT / "P8_Y5_PARENT_QLOC_2132_NO_TOWER_THEOREM_ATTEMPT.csv",
    "2132_validation": OUT / "P8_Y5_BRR545_2132_VALIDATION.csv",
    "963_doc": ROOT / "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
    "1343_doc": ROOT / "1343-Y5-R10-RAB-R2FR-parent-coefficient-zero-signature-or-finite-scalar-map-fill.md",
    "2135_doc": ROOT / "2135-Y5-R2FR-no-mixed-curvature-morphism-lemma-or-first-beta-source-owner.md",
    "2301_residuals": OUT / "P8_Y5_PARENT_QLOC_2301_Q_CURVATURE_RESIDUAL_ACQUISITION_ROWS.csv",
    "2304_refusal": OUT / "P8_Y5_PARENT_QLOC_2304_REFUSAL_RUNNER.csv",
    "1768_doc": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
    "1235_requirements": OUT / "P8_Y5_R10_1235_TYPED_DOMAIN_REQUIREMENTS.csv",
}

SOURCES = [
    ("SRC2306_00_2305_doc", "2305_doc", PATHS["2305_doc"], ["DEC2305_3_next", "2306-Y5-R2FR-DqWeyl2-higher-curvature-tower-zero-or-first-local-bound-row.md"], "direct 2305 handoff"),
    ("SRC2306_01_2305_validation", "2305_validation", PATHS["2305_validation"], ["VAL2305_OVERALL", "PASS"], "2305 validation"),
    ("SRC2306_02_2305_quadratic", "2305_quadratic", PATHS["2305_quadratic"], ["DQW2305_0_DqWeyl2", "NONCLAIM_RESIDUAL_ROW"], "D_qWeyl2 residual handoff"),
    ("SRC2306_03_2305_next", "2305_next", PATHS["2305_next"], ["2306-Y5-R2FR-DqWeyl2-higher-curvature-tower-zero-or-first-local-bound-row.md"], "next target csv"),
    ("SRC2306_04_2132_no_tower", "2132_no_tower", PATHS["2132_no_tower"], ["NT2132_5_verdict", "NO_TOWER_THEOREM_NOT_DERIVED"], "no integrated higher-curvature tower theorem failed"),
    ("SRC2306_05_2132_validation", "2132_validation", PATHS["2132_validation"], ["VAL2132_OVERALL", "PASS"], "2132 validation"),
    ("SRC2306_06_963_doc", "963_doc", PATHS["963_doc"], ["DO963_6_verdict", "NOT_PARENT_SIGNED_CURRENT_CORPUS"], "parent second-order signature not signed"),
    ("SRC2306_07_1343_doc", "1343_doc", PATHS["1343_doc"], ["ZERO1343_5_verdict", "ZERO_SIGNATURE_NOT_DERIVED_CURRENT_CORPUS"], "higher-curvature coefficient zero signature not derived"),
    ("SRC2306_08_2135_doc", "2135_doc", PATHS["2135_doc"], ["NMC2135_5_verdict", "NO_MIXED_CURVATURE_MORPHISM_NOT_DERIVED"], "curvature coefficient morphism remains live"),
    ("SRC2306_09_2301_residuals", "2301_residuals", PATHS["2301_residuals"], ["QCURV2301_5_total", "SCHEMA_READY_VALUES_MISSING"], "q curvature residual total still missing values"),
    ("SRC2306_10_2304_refusal", "2304_refusal", PATHS["2304_refusal"], ["REF2304_3_orbital", "no arena projection"], "earlier refusal due missing Weyl projection"),
    ("SRC2306_11_1768_doc", "1768_doc", PATHS["1768_doc"], ["SCL1768_5_post_variation_projector", "FORBIDDEN_BY_NORMAL_FORM_CONTRACT_UNSIGNED"], "projector/source maps unsigned"),
    ("SRC2306_12_1235_requirements", "1235_requirements", PATHS["1235_requirements"], ["TREQ1235_4_readout_radiative_closure", "READOUT_RADIATIVE_CLOSURE_UNSIGNED"], "radiative/readout closure unsigned"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2306_SOURCE_REGISTER.csv",
    "zero": OUT / "P8_Y5_PARENT_QLOC_2306_DQWEYL2_ZERO_THEOREM_ATTEMPT.csv",
    "projection": OUT / "P8_Y5_PARENT_QLOC_2306_SCHWARZSCHILD_WEYL2_PROJECTION_LAW.csv",
    "bound": OUT / "P8_Y5_PARENT_QLOC_2306_DQWEYL2_FIRST_LOCAL_BOUND_ROW.csv",
    "arena": OUT / "P8_Y5_PARENT_QLOC_2306_ARENA_PROJECTION_REQUIREMENTS.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2306_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2306_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2306_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2306_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2306_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2306_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2306_0_projection_law", OUTPUTS["projection"], QUEUE / "JR2306_SCHWARZSCHILD_WEYL2_PROJECTION_LAW_NONCLAIM.csv"),
    ("COPY2306_1_bound_row", OUTPUTS["bound"], QUEUE / "JR2306_DQWEYL2_FIRST_LOCAL_BOUND_ROW_NONCLAIM.csv"),
    ("COPY2306_2_microscope_residual", OUTPUTS["bound"], MICROSCOPE / "q_DqWeyl2_first_local_bound_row_nonclaim_2306.csv"),
    ("COPY2306_3_beta_docs", OUTPUTS["zero"], BETA_DOCS / "DQWEYL2_TOWER_ZERO_ATTEMPT_2306_NONCLAIM.csv"),
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


def make_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ZERO2306_0_target",
            "zero_clause": "D_qWeyl2=0 from parent second-order/no-tower action",
            "attempt": "TARGET_SHARP",
            "reasoning": "A strict EH-like parent action with no bare Weyl2 term and no eliminated scalar/projector/memory regeneration would remove q C^2 source terms.",
            "current_status": "NOT_PROVEN",
            "missing_piece": "parent second-order action, no bare Weyl2, no integrated tower, radiative/readout closure",
            "source_keys": "2132_no_tower;963_doc;1343_doc",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ZERO2306_1_no_bare_weyl2",
            "zero_clause": "no bare q C^2 or C^2 operator",
            "attempt": "UNSIGNED",
            "reasoning": "1343 explicitly keeps no bare higher-curvature operators, including Weyl2, unsigned.",
            "current_status": "MISSING_PARENT_SIGNATURE",
            "missing_piece": "parent action operator inventory excluding Weyl2 before reduction",
            "source_keys": "1343_doc",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ZERO2306_2_no_integrated_tower",
            "zero_clause": "no eliminated variable regenerates Weyl2/R2/Ricci2/nonlocal towers",
            "attempt": "UNSIGNED",
            "reasoning": "2132 and 963 both warn that integrating out auxiliary/projector/memory variables can regenerate higher curvature.",
            "current_status": "NO_TOWER_THEOREM_NOT_DERIVED",
            "missing_piece": "beta_A=0/M_A=infinity/no-kernel/no-readout clauses for every eliminated sector",
            "source_keys": "2132_no_tower;963_doc",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ZERO2306_3_no_curvature_morphism",
            "zero_clause": "hidden invariants cannot feed curvature coefficients",
            "attempt": "FAILED_CURRENT_CORPUS",
            "reasoning": "2135 records F(I_hid)R as a legal covariant countermodel if hidden scalar invariants survive; analogous coefficient feed-through cannot be ignored.",
            "current_status": "CURVATURE_MORPHISM_NOT_EXCLUDED",
            "missing_piece": "fixed EH/curvature coefficient owner and hidden invariant triviality",
            "source_keys": "2135_doc",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ZERO2306_4_verdict",
            "zero_clause": "claim D_qWeyl2=0 now",
            "attempt": "ZERO_THEOREM_NOT_DERIVED",
            "reasoning": "The zero route is exact if all parent action/no-tower clauses are signed, but every required parent clause is currently unsigned.",
            "current_status": "RETAIN_FINITE_RESIDUAL_BOUND_ROW",
            "missing_piece": "source-backed D_qWeyl2 coefficient or complete no-tower theorem",
            "source_keys": "all_above",
            "valid_for_claim": "false",
        },
    ]


def make_projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PROJ2306_0_schwarzschild_identity",
            "quantity": "C2_Schw",
            "formula": "C_{abcd}C^{abcd}=48 mu^2/r^6 with mu=GM/c^2 in Schwarzschild exterior vacuum",
            "status": "EXACT_BACKGROUND_IDENTITY",
            "use": "projection kernel for testing a small residual on a GR background, not a proof of GR",
            "missing_for_claim": "parent coefficient D_qWeyl2 and q Green operator",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PROJ2306_1_exterior_volume_integral",
            "quantity": "I_C2_ext(R)",
            "formula": "int_R^infty 4*pi*r^2*C2_Schw dr = 64*pi*mu^2/R^3",
            "status": "EXACT_CUTOFF_SCALING",
            "use": "shows the effective source is body-radius/cutoff sensitive and cannot be point-particle naive",
            "missing_for_claim": "body radius/internal matching prescription and normalization convention",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PROJ2306_2_far_field_scaling",
            "quantity": "q_far_scaling",
            "formula": "for L_q q = -D_qWeyl2 C2 and massless Poisson normalization, q_far scales like D_qWeyl2*mu^2/(R^3*r), up to Green-function convention",
            "status": "SCALING_LAW_NOT_NUMERIC_CLAIM",
            "use": "first analytic shape for local/orbital bound rows",
            "missing_for_claim": "L_q normalization, sign, mass/Yukawa scale, and observable coupling",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PROJ2306_3_point_particle_warning",
            "quantity": "cutoff_dependence",
            "formula": "C2 source integral diverges as R^-3 as R->0",
            "status": "REGULARITY_WARNING",
            "use": "forces body/interior/regularity treatment before using compact-source bounds",
            "missing_for_claim": "finite-size source model or regularized parent geometry",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PROJ2306_4_pontryagin_static_zero",
            "quantity": "CstarC_Schw",
            "formula": "C_{abcd}*C^{abcd}=0 for static spherical Schwarzschild exterior; spin/Kerr branch must be treated separately",
            "status": "EXACT_BACKGROUND_IDENTITY_FOR_STATIC_SPHERICAL",
            "use": "keeps parity-odd D_qWeylDual from being mixed into the static spherical row",
            "missing_for_claim": "rotating-source projection if D_qWeylDual remains active",
            "valid_for_claim": "false",
        },
    ]


def make_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BOUND2306_0_coefficient",
            "input": "D_qWeyl2",
            "value": "MISSING_PARENT_COEFFICIENT",
            "units": "length_squared_or_parent_normalized_pending_convention",
            "status": "MISSING_PARENT_INPUT",
            "needed_to_run": "source path, sign, normalization relative to q equation/action",
            "arena": "all_local_arenas",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BOUND2306_1_operator",
            "input": "L_q_or_G_q",
            "value": "MISSING_Q_GREEN_OPERATOR",
            "units": "operator",
            "status": "MISSING_PARENT_INPUT",
            "needed_to_run": "massless/massive q operator, boundary conditions, Yukawa length, kinetic normalization",
            "arena": "R10;PPN;orbital;clock",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BOUND2306_2_source_cutoff",
            "input": "R_body_or_regularization",
            "value": "MISSING_BODY_RADIUS_OR_INTERIOR_MATCH",
            "units": "length",
            "status": "MISSING_SOURCE_MODEL",
            "needed_to_run": "finite source radius, density profile, or regular parent geometry cutoff because integral scales as R^-3",
            "arena": "lab_R10;solar_system;compact_objects",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BOUND2306_3_projection_kernel",
            "input": "K_C2_ext",
            "value": "64*pi*(GM/c^2)^2/R_body^3",
            "units": "length^-1",
            "status": "ANALYTIC_KERNEL_READY_NONCLAIM",
            "needed_to_run": "combine with D_qWeyl2 and G_q convention",
            "arena": "orbital;PPN;R10_if_projected",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BOUND2306_4_observable_coupling",
            "input": "P_arena[q]",
            "value": "MISSING_OBSERVABLE_MAP",
            "units": "arena_specific",
            "status": "MISSING_ARENA_PROJECTION",
            "needed_to_run": "map q profile into acceleration, PPN potentials, clock shifts, alpha drift, or short-range alpha(lambda)",
            "arena": "R10;PPN;clock;orbital",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BOUND2306_5_acceptance",
            "input": "D_qWeyl2_claim",
            "value": "false",
            "units": "boolean",
            "status": "CLAIM_BLOCKED",
            "needed_to_run": "ZERO2306_4 becomes zero theorem or BOUND2306_0 through BOUND2306_4 become source-backed numeric rows",
            "arena": "all_local_arenas",
            "valid_for_claim": "false",
        },
    ]


def make_arena_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "ARENA2306_0_orbital", "arena": "orbital_precession", "required_projection": "q_far(r) and induced acceleration/potential correction around finite-radius source", "current_status": "KERNEL_SCALING_READY_COUPLING_MISSING", "blocks_claim": "true", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "ARENA2306_1_PPN", "arena": "PPN", "required_projection": "metric-sector backreaction or q-mediated force in standard PPN potentials", "current_status": "MISSING_METRIC_BACKREACTION_MAP", "blocks_claim": "true", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "ARENA2306_2_R10", "arena": "short_range_R10", "required_projection": "map finite source C2 profile to Yukawa alpha(lambda) or prove no lab coupling", "current_status": "MISSING_LAB_SOURCE_AND_Q_COUPLING_MAP", "blocks_claim": "true", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "ARENA2306_3_clocks", "arena": "clocks_alpha", "required_projection": "readout of q or curvature residual into clock frequency/alpha drift", "current_status": "READOUT_RADIATIVE_CLOSURE_UNSIGNED", "blocks_claim": "true", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "ARENA2306_4_static_spin_split", "arena": "static_vs_rotating_sources", "required_projection": "static spherical uses C2 only; rotating/Kerr branch needed for C*C", "current_status": "STATIC_SPLIT_READY_SPIN_BRANCH_MISSING", "blocks_claim": "true", "valid_for_claim": "false"},
    ]


def make_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2306_0_zero", "claim": "D_qWeyl2=0", "allowed": "false", "reason": "no-tower/second-order/higher-curvature parent signature is not derived", "blocking_rows": "ZERO2306_4_verdict", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2306_1_bound", "claim": "D_qWeyl2 passes local bounds", "allowed": "false", "reason": "coefficient, Green operator, body regularization, and observable map are missing", "blocking_rows": "BOUND2306_0_coefficient;BOUND2306_1_operator;BOUND2306_2_source_cutoff;BOUND2306_4_observable_coupling", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2306_2_GR", "claim": "local GR/Newton derived", "allowed": "false", "reason": "quadratic Weyl is only one remaining residual; source descent and EH/Newton derivation are still separate gates", "blocking_rows": "ARENA2306_1_PPN;ARENA2306_3_clocks", "valid_for_claim": "false"},
    ]


def make_claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "GATE2306_0_sources", "gate": "source paths and needles valid", "passed": "true", "claim_effect": "ledger is source-backed", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "GATE2306_1_zero_attempt", "gate": "D_qWeyl2 zero theorem attempted", "passed": "true", "claim_effect": "zero route tested first", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "GATE2306_2_zero_signed", "gate": "D_qWeyl2 zero theorem signed", "passed": "false", "claim_effect": "must retain residual", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "GATE2306_3_projection_law", "gate": "Schwarzschild C2 projection law recorded", "passed": "true", "claim_effect": "first analytic local source scaling exists", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "GATE2306_4_bound_inputs", "gate": "all numeric bound inputs source-backed", "passed": "false", "claim_effect": "bound route not executable yet", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "GATE2306_5_local_claim", "gate": "local GR/PPN/R10/orbital/clock pass", "passed": "false", "claim_effect": "all local claims remain blocked", "valid_for_claim": "false"},
    ]


def make_decision_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "DEC2306_0", "decision": "ZERO_ROUTE_FAILED_CURRENT_CORPUS", "reason": "no-tower/no-higher-curvature parent signature remains unsigned", "next_action": "use nonclaim bound row unless parent action evidence appears", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2306_1", "decision": "FIRST_REAL_PROJECTION_LAW_ADDED", "reason": "C2_Schw and exterior integral give concrete finite-source scaling for future tests", "next_action": "turn projection law into a numeric smoke runner after coefficient/operator assumptions are explicit", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2306_2", "decision": "POINT_PARTICLE_SHORTCUT_REJECTED", "reason": "C2 source integral scales as R_body^-3 and needs regularity/interior matching", "next_action": "require finite-radius source model in any future R10/orbital bound", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2306_3_next", "decision": "NEXT_TARGET_SELECTED", "reason": "projection kernel exists but coefficient/operator/observable maps are missing", "next_action": "2307-Y5-R2FR-DqWeyl2-projection-smoke-runner-input-contract-or-parent-coefficient-source.md", "valid_for_claim": "false"},
    ]


def make_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2306_0",
            "next_target": "2307-Y5-R2FR-DqWeyl2-projection-smoke-runner-input-contract-or-parent-coefficient-source.md",
            "why": "2306 gives the analytic source kernel, so 2307 should either source D_qWeyl2/L_q or build a nonclaim smoke runner showing required inputs",
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
    zero_rows: list[dict[str, Any]],
    projection_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tables = [source_rows, zero_rows, projection_rows, bound_rows, arena_rows, refusal_rows, claim_rows, decision_rows, copy_rows]
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2306_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited local source path exists"))
    checks.append(("VAL2306_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2306_02_zero_failed_honestly", any(row["row_id"] == "ZERO2306_4_verdict" and row["attempt"] == "ZERO_THEOREM_NOT_DERIVED" for row in zero_rows), "D_qWeyl2 zero route is attempted and not promoted"))
    checks.append(("VAL2306_03_projection_identity", any(row["row_id"] == "PROJ2306_0_schwarzschild_identity" and "48 mu^2/r^6" in row["formula"] for row in projection_rows), "Schwarzschild Weyl2 identity recorded"))
    checks.append(("VAL2306_04_integral_scaling", any(row["row_id"] == "PROJ2306_1_exterior_volume_integral" and "64*pi*mu^2/R^3" in row["formula"] for row in projection_rows), "exterior integral scaling recorded"))
    checks.append(("VAL2306_05_cutoff_warning", any(row["row_id"] == "PROJ2306_3_point_particle_warning" and "R^-3" in row["formula"] for row in projection_rows), "finite-size cutoff warning recorded"))
    checks.append(("VAL2306_06_bound_missing_inputs", any(row["row_id"] == "BOUND2306_0_coefficient" and row["status"] == "MISSING_PARENT_INPUT" for row in bound_rows) and any(row["row_id"] == "BOUND2306_4_observable_coupling" and row["status"] == "MISSING_ARENA_PROJECTION" for row in bound_rows), "bound row keeps missing coefficient and observable map explicit"))
    checks.append(("VAL2306_07_kernel_nonclaim", any(row["row_id"] == "BOUND2306_3_projection_kernel" and row["status"] == "ANALYTIC_KERNEL_READY_NONCLAIM" for row in bound_rows), "analytic kernel is staged as nonclaim"))
    checks.append(("VAL2306_08_arena_blocked", all(row["blocks_claim"] == "true" for row in arena_rows), "all arena requirements block claims"))
    checks.append(("VAL2306_09_refusal_runner", all(row["allowed"] == "false" for row in refusal_rows), "refusal runner blocks claims"))
    checks.append(("VAL2306_10_claim_gates", any(row["row_id"] == "GATE2306_5_local_claim" and row["passed"] == "false" for row in claim_rows), "local claim gate false"))
    checks.append(("VAL2306_11_next_target", any(row["row_id"] == "DEC2306_3_next" and "2307-Y5-R2FR-DqWeyl2-projection-smoke-runner-input-contract-or-parent-coefficient-source.md" in row["next_action"] for row in decision_rows), "next target selected"))
    checks.append(("VAL2306_12_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2306_13_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in tables for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2306_14_formalization_untouched_by_2306", len(list(FORMALIZATION.rglob("*2306*"))) == 0 if FORMALIZATION.exists() else True, "no 2306 output appears in formalization-workbench"))
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
            "row_id": "VAL2306_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2306 rejects the D_qWeyl2 zero theorem under current evidence, adds the Schwarzschild Weyl-squared projection law and finite-size cutoff scaling, and stages a nonclaim first local bound row.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    projection_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2306 — D_qWeyl2 Higher-Curvature Tower Zero Or First Local Bound Row",
        "",
        "## Summary",
        "",
        "2306 goes after the live obstruction left by 2305: quadratic Weyl. The zero route does not close from the current corpus because the parent second-order/no-higher-curvature/no-integrated-tower signature is still unsigned.",
        "",
        "The useful progress is that we now have a concrete analytic local-source kernel. On a Schwarzschild exterior background, `C_{abcd}C^{abcd}=48 mu^2/r^6` with `mu=GM/c^2`, and the exterior volume integral from a finite body radius `R` is `64*pi*mu^2/R^3`. That is exactly the kind of scaling a future bound runner needs. It also tells us not to cheat with point particles: the source is cutoff/interior sensitive.",
        "",
        "This remains nonclaim. It is a projection scaffold for future testing, not a local-GR pass.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## D_qWeyl2 Zero-Theorem Attempt",
        "",
        md_table(zero_rows, ["row_id", "zero_clause", "attempt", "reasoning", "current_status", "missing_piece", "valid_for_claim"]),
        "",
        "## Schwarzschild Weyl2 Projection Law",
        "",
        md_table(projection_rows, ["row_id", "quantity", "formula", "status", "use", "missing_for_claim", "valid_for_claim"]),
        "",
        "## First Local Bound Row",
        "",
        md_table(bound_rows, ["row_id", "input", "value", "units", "status", "needed_to_run", "arena", "valid_for_claim"]),
        "",
        "## Arena Projection Requirements",
        "",
        md_table(arena_rows, ["row_id", "arena", "required_projection", "current_status", "blocks_claim", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        md_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
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
    zero_rows = make_zero_rows()
    projection_rows = make_projection_rows()
    bound_rows = make_bound_rows()
    arena_rows = make_arena_rows()
    refusal_rows = make_refusal_rows()
    claim_rows = make_claim_gate_rows()
    decision_rows = make_decision_rows()
    next_rows = make_next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["zero"], zero_rows)
    write_csv(OUTPUTS["projection"], projection_rows)
    write_csv(OUTPUTS["bound"], bound_rows)
    write_csv(OUTPUTS["arena"], arena_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["claim_gates"], claim_rows)
    write_csv(OUTPUTS["decision"], decision_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_files()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(source_rows, zero_rows, projection_rows, bound_rows, arena_rows, refusal_rows, claim_rows, decision_rows, copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_markdown(source_rows, zero_rows, projection_rows, bound_rows, arena_rows, refusal_rows, claim_rows, decision_rows, next_rows, copy_rows, validation_rows)

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2306_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

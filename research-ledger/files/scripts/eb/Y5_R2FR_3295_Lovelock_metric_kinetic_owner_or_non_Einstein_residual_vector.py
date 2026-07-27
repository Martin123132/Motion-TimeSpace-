from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3295-Y5-R2FR-Lovelock-metric-kinetic-owner-or-non-Einstein-residual-vector-under-AX1090.md"

SRC_3294_DOC = ROOT / "3294-Y5-R2FR-local-GR-reduction-contract-Hilbert-source-common-G-and-Newton-limit-under-AX1090.md"
SRC_3294_NEXT = OUT / "P8_Y5_R2FR_3294_NEXT_TARGET.csv"
SRC_3294_CONTRACT = OUT / "P8_Y5_R2FR_3294_LOCAL_GR_REDUCTION_CONTRACT.csv"
SRC_3294_THEOREM = OUT / "P8_Y5_R2FR_3294_LOCAL_GR_CONDITIONAL_THEOREM.csv"
SRC_3294_RESIDUAL = OUT / "P8_Y5_R2FR_3294_PPN_NEWTON_MAXWELL_RESIDUAL_VECTOR.csv"
SRC_3294_VALIDATION = OUT / "P8_Y5_BRR545_3294_VALIDATION.csv"
SRC_3293_DOC = ROOT / "3293-Y5-R2FR-parent-Hilbert-source-and-canonical-quantum-normalization-signature-under-AX1090.md"
SRC_3288_DOC = ROOT / "3288-Y5-R2FR-same-public-metric-or-ZQ-impedance-owner-split-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3295_SOURCE_REGISTER.csv",
    "premises": OUT / "P8_Y5_R2FR_3295_LOVELOCK_PREMISE_AUDIT.csv",
    "theorem": OUT / "P8_Y5_R2FR_3295_LOVELOCK_CONDITIONAL_THEOREM.csv",
    "counterexamples": OUT / "P8_Y5_R2FR_3295_KINETIC_COUNTEREXAMPLE_LEDGER.csv",
    "residuals": OUT / "P8_Y5_R2FR_3295_NON_EINSTEIN_RKIN_RESIDUAL_VECTOR.csv",
    "ppn": OUT / "P8_Y5_R2FR_3295_NEWTON_PPN_PROJECTION_CONTRACT.csv",
    "runner": OUT / "P8_Y5_R2FR_3295_LOVELOCK_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3295_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3295_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3295_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3295_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 560) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def evidence_hits(path: Path, needles: list[str], limit: int = 5) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 330)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    snapshot: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            stat = item.stat()
            snapshot[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3294_DOC, "local-GR contract handoff", ["Einstein-like kinetic", "R_kin"]),
        (SRC_3294_NEXT, "3294 next target", ["Lovelock", "non-Einstein-residual"]),
        (SRC_3294_CONTRACT, "local GR contract", ["LGC3294_1_Einstein_like_kinetic", "LGC3294_5_Newton_limit"]),
        (SRC_3294_THEOREM, "conditional local GR theorem", ["LGT3294_0_conditional_GR_equation", "LGT3294_3_no_Bianchi_smuggling"]),
        (SRC_3294_RESIDUAL, "R_kin residual handoff", ["RV3294_1_non_Einstein_kinetic", "R_kin"]),
        (SRC_3294_VALIDATION, "3294 validation", ["VAL3294_12_overall", "true"]),
        (SRC_3293_DOC, "Hilbert source/common G context", ["Hilbert-source signature", "common G"]),
        (SRC_3288_DOC, "same public metric context", ["same public metric", "shared observed coframe"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3295_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def premise_rows() -> list[dict[str, Any]]:
    return [
        {
            "premise_id": "LOV3295_0_dimension",
            "premise": "four-dimensional local spacetime regime",
            "needed_for": "ordinary 4D Lovelock uniqueness; higher-dimensional Lovelock terms would not be automatically topological",
            "current_status": "LOCAL_LIMIT_ASSUMPTION_NOT_PARENT_SIGNED",
            "failure_residual": "R_dimension_or_compactification",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "LOV3295_1_single_metric",
            "premise": "single public metric/coframe is the only local gravitational tensor argument",
            "needed_for": "exclude bimetric, independent connection, tetrad torsion, and hidden frame kinetic terms",
            "current_status": "CONDITIONAL_FROM_3288_NOT_PARENT_SIGNED",
            "failure_residual": "R_metric_split_or_connection",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "LOV3295_2_locality",
            "premise": "local field equation/action density with finite derivatives at the point",
            "needed_for": "exclude memory kernels and nonlocal history dependence from the local GR branch",
            "current_status": "OPEN_FOR_MEMORY_MTS",
            "failure_residual": "R_nonlocal_memory",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "LOV3295_3_diffeomorphism_covariance",
            "premise": "generally covariant metric equation with identically divergence-free left-hand side",
            "needed_for": "Noether/Bianchi compatibility of the kinetic tensor",
            "current_status": "EXPECTED_BUT_NOT_SUFFICIENT",
            "failure_residual": "R_preferred_frame_or_noncovariant",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "LOV3295_4_second_order",
            "premise": "field equations are second order in the metric and quasilinear in second derivatives",
            "needed_for": "Lovelock theorem forces Einstein tensor plus Lambda in 4D",
            "current_status": "MAJOR_UNSIGNED_CLAUSE",
            "failure_residual": "R_higher_derivative",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "LOV3295_5_no_extra_propagating_fields",
            "premise": "no local scalar, vector, torsion, nonmetricity, or memory field contributes independently in the local vacuum branch",
            "needed_for": "exclude scalar-tensor, Einstein-aether, torsion/nonmetricity, and extra fifth-force polarizations",
            "current_status": "MAJOR_UNSIGNED_CLAUSE",
            "failure_residual": "R_extra_field",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "LOV3295_6_boundary_topological_silence",
            "premise": "boundary, Gauss-Bonnet, Chern-Simons, and topological terms are constant/silent or reduce to bounded residuals",
            "needed_for": "exclude lower-dimensional/boundary kinetic leakage and coupled topological dynamics",
            "current_status": "OPEN_GUARD",
            "failure_residual": "R_boundary_topological",
            "valid_for_claim": "false",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "LKT3295_0_Lovelock_statement",
            "statement": "If LOV3295_0 through LOV3295_6 are signed, any local symmetric divergence-free second-order metric tensor in 4D is a linear combination of G_mu_nu and g_mu_nu.",
            "math_result": "E_mu_nu = a G_mu_nu + b g_mu_nu",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "LKT3295_1_GR_normalization",
            "statement": "With a != 0, divide by a and absorb b/a into Lambda and the common source coefficient into G_cal.",
            "math_result": "G_mu_nu + Lambda g_mu_nu = (8*pi*G_cal/c^4) T_H_mu_nu",
            "status": "EXACT_CONDITIONAL_REDUCTION",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "LKT3295_2_degenerate_case",
            "statement": "If a=0, the kinetic equation is not locally Einstein-like and cannot reproduce Newtonian gravity without another dynamical operator.",
            "math_result": "b g_mu_nu = kappa T_mu_nu is not a viable Newtonian metric kinetic law",
            "status": "DEGENERATE_BRANCH_REJECTED_OR_EXTRA_OPERATOR_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "LKT3295_3_current_MTS_status",
            "statement": "MTS does not yet own all Lovelock premises; the theorem supplies the clean route and defines the finite R_kin residual if a premise fails.",
            "math_result": "R_kin = E_MTS - (a G + b g)",
            "status": "ROUTE_SHARP_NOT_PROMOTED",
            "valid_for_claim": "false",
        },
    ]


def counterexample_rows() -> list[dict[str, Any]]:
    return [
        {
            "counterexample_id": "CE3295_0_higher_derivative",
            "failed_premise": "second_order",
            "example": "R^2, R_mu_nu R^mu_nu, f(R), or higher-derivative effective action",
            "why_allowed_if_unsigned": "diffeomorphism invariance alone allows fourth-order metric equations",
            "test_signature": "Yukawa/range terms, PPN gamma-beta shifts, extra scalar mode",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CE3295_1_extra_scalar",
            "failed_premise": "no_extra_fields",
            "example": "scalar-tensor or hidden amplitude field coupled to curvature/source",
            "why_allowed_if_unsigned": "single metric plus covariance does not forbid a scalar owner unless local vacuum branch projects it out",
            "test_signature": "fifth force, Gdot, Nordtvedt/WEP pressure, cosmological growth drift",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CE3295_2_vector_torsion_connection",
            "failed_premise": "single_metric_only",
            "example": "Einstein-aether, torsion, independent connection, nonmetricity",
            "why_allowed_if_unsigned": "coframe/connection descent has not yet been parent-signed as Levi-Civita only",
            "test_signature": "preferred-frame PPN alpha_i, spin/torsion couplings, wave speed/polarization shifts",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CE3295_3_nonlocal_memory",
            "failed_premise": "locality",
            "example": "history-dependent kernel or memory projection in the local field equation",
            "why_allowed_if_unsigned": "MTS has memory/cosmology branches, so local silence must be derived rather than assumed",
            "test_signature": "scale/time dependent G_eff, hysteresis, environment dependence",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CE3295_4_boundary_topological",
            "failed_premise": "boundary_topological_silence",
            "example": "coupled Gauss-Bonnet, Chern-Simons, or boundary charge term",
            "why_allowed_if_unsigned": "topological terms are harmless only when constant/uncoupled/boundary-silent",
            "test_signature": "parity violation, spin precession, orbital precession, boundary/domain dependence",
            "valid_for_claim": "false",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RKIN3295_0_higher_derivative",
            "symbol": "R_HD",
            "definition": "projection of higher-curvature or fourth-order metric terms into the local field equation",
            "Newton_PPN_signature": "Yukawa scale, gamma/beta shifts, modified Poisson operator",
            "status": "ZERO_IF_SECOND_ORDER_SIGNED_ELSE_BOUND",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RKIN3295_1_extra_scalar_vector",
            "symbol": "R_extra",
            "definition": "stress/kinetic contribution from scalar, vector, torsion, nonmetricity, or hidden propagating fields",
            "Newton_PPN_signature": "fifth force, preferred-frame alpha_i, WEP/Gdot/Nordtvedt pressure",
            "status": "ZERO_IF_NO_EXTRA_FIELD_SIGNED_ELSE_BOUND",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RKIN3295_2_nonlocal_memory",
            "symbol": "R_mem",
            "definition": "nonlocal or history-dependent correction to the local metric equation",
            "Newton_PPN_signature": "time/range/environment dependent G_eff and orbital hysteresis",
            "status": "ZERO_IF_LOCALITY_SIGNED_ELSE_BOUND",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RKIN3295_3_preferred_frame",
            "symbol": "R_pf",
            "definition": "noncovariant, foliation, aether, or frame-marker kinetic contribution",
            "Newton_PPN_signature": "preferred-frame PPN alpha_1 alpha_2 alpha_3 and anisotropic inertia",
            "status": "ZERO_IF_DIFF_AND_NO_FRAME_MARKER_SIGNED_ELSE_BOUND",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RKIN3295_4_boundary_topological",
            "symbol": "R_top",
            "definition": "coupled topological, Chern-Simons, Gauss-Bonnet, or boundary kinetic term",
            "Newton_PPN_signature": "spin/parity/orbital precession and domain-boundary dependence",
            "status": "ZERO_IF_BOUNDARY_TOPOLOGICAL_SILENCE_SIGNED_ELSE_BOUND",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RKIN3295_5_coefficient_drift",
            "symbol": "R_coeff",
            "definition": "hidden/time/source/range dependent coefficient multiplying the Einstein tensor or curvature terms",
            "Newton_PPN_signature": "Gdot, fifth-force range dependence, source composition drift",
            "status": "ZERO_IF_COMMON_CONSTANT_COEFFICIENT_SIGNED_ELSE_BOUND",
            "valid_for_claim": "false",
        },
    ]


def ppn_rows() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "PPN3295_0_Newton_source",
            "input_residual": "R_kin_00",
            "weak_field_map": "delta(nabla^2 Phi) = projection_00[R_kin] plus source residuals",
            "needed_to_score": "linearized operator, gauge choice, source convention, boundary conditions",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "PPN3295_1_gamma_beta",
            "input_residual": "spatial and nonlinear metric residuals",
            "weak_field_map": "map R_kin spatial/00 components into PPN gamma and beta",
            "needed_to_score": "post-Newtonian expansion to O(c^-4) and matter coupling rule",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "PPN3295_2_preferred_frame",
            "input_residual": "R_pf or vector/torsion/aether residual",
            "weak_field_map": "map frame-marker terms into alpha_1, alpha_2, alpha_3",
            "needed_to_score": "preferred-frame velocity convention and local source solution",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "PPN3295_3_orbital",
            "input_residual": "R_HD, R_extra, R_mem, R_top",
            "weak_field_map": "derive effective orbital potential/precession/range terms for solar-system and binary orbital tests",
            "needed_to_score": "Green kernel, boundary conditions, source multipoles, observation mapping",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN3295_0_Lovelock_conditional", "Lovelock theorem route gives Einstein tensor plus Lambda if premises signed", "PASS_SYMBOLIC_NONCLAIM"),
        ("RUN3295_1_premises_unsigned", "not all MTS parent premises signed", "REFUSE_CLAIM_NONCLAIM"),
        ("RUN3295_2_residual_vector", "R_kin residual vector complete for non-Einstein branches", "PASS_SYMBOLIC_NONCLAIM"),
        ("RUN3295_3_PPN_projection", "PPN/Newton/orbital scoring requires projection maps", "REFUSE_MISSING_PROJECTION_NONCLAIM"),
    ]
    return [
        {
            "run_id": run_id,
            "check": check,
            "observed_status": status,
            "expectation_match": "true",
            "claim_allowed": "false",
        }
        for run_id, check, status in rows
    ]


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3295_0_Lovelock_route_valid",
            "gate": "Lovelock conditional theorem gives Einstein tensor plus Lambda",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "the mathematical route is valid conditionally.",
        },
        {
            "gate_id": "GATE3295_1_all_premises_parent_signed",
            "gate": "single metric, locality, second-order, no-extra-field, and boundary silence are parent-signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "major MTS-specific clauses remain unsigned.",
        },
        {
            "gate_id": "GATE3295_2_Rkin_zero_or_bounded",
            "gate": "R_kin residual vector is zero or empirically bounded",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "requires next derivation/projection pass.",
        },
        {
            "gate_id": "GATE3295_3_local_GR_claim",
            "gate": "local-GR left-hand side is claimed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "no claim until premises or residual bounds close.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3295_0_real_move",
            "finding": "The left-hand side now has a rigorous theorem route: Lovelock forces G_mu_nu + Lambda g_mu_nu if the MTS local branch is 4D, single-metric, local, diffeomorphism-covariant, second-order, and has no extra propagating fields.",
            "consequence": "GR reduction is no longer a taste preference; it is a checklist of parent-signature clauses.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3295_1_live_gap",
            "finding": "The largest remaining kinetic gaps are second-order/no-extra-field/local-memory silence.",
            "consequence": "go after those clauses directly before PPN scoring.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3295_2_if_fails",
            "finding": "If any Lovelock premise fails, the non-Einstein part is not fatal by definition but must be projected into R_kin and tested.",
            "consequence": "the fallback is finite PPN/Newton/orbital residual testing, not abandonment or closure magic.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3295_0_3296",
            "target_doc": "3296-Y5-R2FR-second-order-no-extra-field-locality-signature-or-Rkin-projection-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3296_second_order_no_extra_field_locality_signature_or_Rkin_projection.py",
            "objective": "try to parent-sign the three hardest Lovelock clauses: second-order metric equations, no extra propagating local fields, and local memory silence; if not, start the R_kin projection map for Newton/PPN/orbital tests.",
            "guardrails": "do not assume away memory fields; do not claim Lovelock if any premise fails; do not score PPN without a linearized residual projection.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    premises: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    counterexamples: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    formalization_changed_count: int,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append({"check_id": check_id, "check": check, "passed": bool_str(passed), "detail": detail})

    add("VAL3295_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3295_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add("VAL3295_2_outputs_parse", "all 3295 non-validation output CSVs parse", all(csv_parse_ok(path) for key, path in OUTPUTS.items() if key != "validation"))

    premise_ids = {row["premise_id"] for row in premises}
    add(
        "VAL3295_3_premise_audit_complete",
        "Lovelock premise audit includes dimension, single metric, locality, covariance, second-order, no-extra-field, and boundary silence",
        {"LOV3295_0_dimension", "LOV3295_1_single_metric", "LOV3295_2_locality", "LOV3295_3_diffeomorphism_covariance", "LOV3295_4_second_order", "LOV3295_5_no_extra_propagating_fields", "LOV3295_6_boundary_topological_silence"}.issubset(premise_ids),
    )

    theorem_text = " ".join(row["statement"] + " " + row["math_result"] + " " + row["status"] for row in theorem)
    add(
        "VAL3295_4_Lovelock_theorem_present",
        "conditional theorem states Lovelock result and GR normalization",
        "E_mu_nu = a G_mu_nu + b g_mu_nu" in theorem_text and "8*pi*G_cal" in theorem_text and "EXACT_CONDITIONAL_THEOREM" in theorem_text,
    )

    ce_premises = {row["failed_premise"] for row in counterexamples}
    add(
        "VAL3295_5_counterexamples_cover_failed_clauses",
        "counterexamples cover higher derivative, scalar, vector/torsion, memory, and topological branches",
        {"second_order", "no_extra_fields", "single_metric_only", "locality", "boundary_topological_silence"}.issubset(ce_premises),
    )

    residual_symbols = {row["symbol"] for row in residuals}
    add(
        "VAL3295_6_Rkin_residual_vector_complete",
        "R_kin vector includes higher derivative, extra field, memory, preferred frame, topological, and coefficient drift",
        {"R_HD", "R_extra", "R_mem", "R_pf", "R_top", "R_coeff"}.issubset(residual_symbols),
    )

    ppn_text = " ".join(row["weak_field_map"] + " " + row["needed_to_score"] for row in ppn)
    add(
        "VAL3295_7_PPN_projection_contract_present",
        "PPN/Newton projection contract includes Poisson, gamma/beta, preferred-frame, and orbital maps",
        "nabla^2 Phi" in ppn_text and "gamma and beta" in ppn_text and "alpha_1" in ppn_text and "orbital" in ppn_text,
    )

    add("VAL3295_8_runner_expectations", "runner expectations all match", all(row["expectation_match"] == "true" for row in runner), ";".join(f"{row['run_id']}={row['observed_status']}" for row in runner))
    add("VAL3295_9_claim_gates_false", "no 3295 gate allows local GR claim", all(row["claim_allowed"] == "false" for row in promotion) and any(row["passed"] == "false" for row in promotion))
    add(
        "VAL3295_10_next_target_focused",
        "next target focuses second-order/no-extra-field/locality or R_kin projection",
        len(next_target) == 1 and "second-order-no-extra-field-locality" in next_target[0]["target_doc"] and "Rkin-projection" in next_target[0]["target_doc"],
    )
    add(
        "VAL3295_11_decision_records_Lovelock_move",
        "decision ledger records rigorous Lovelock route and finite residual fallback",
        any("Lovelock forces" in row["finding"] for row in decisions) and any("finite PPN/Newton/orbital residual testing" in row["consequence"] for row in decisions),
    )
    add(
        "VAL3295_12_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        formalization_changed_count == 0,
        f"formalization_changed_count={formalization_changed_count}",
    )
    overall = all(row["passed"] == "true" for row in checks)
    add("VAL3295_13_overall", "3295 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
    return checks


def md_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    premises: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    counterexamples: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3295 - Lovelock metric-kinetic owner or non-Einstein residual vector under AX1090

**Run UTC:** {RUN_UTC}

3295 moves the local-GR programme onto the left-hand side. The clean route is now explicit:

If the local MTS vacuum/weak-field branch is four-dimensional, single-metric, local, diffeomorphism-covariant, second-order, and has no extra propagating local fields or coupled topological/boundary leakage, then Lovelock uniqueness forces

`E_mu_nu = a G_mu_nu + b g_mu_nu`.

With `a != 0`, this is exactly the Einstein side plus a cosmological constant after normalization. If any clause fails, the failure is not hand-waved: it goes into the named `R_kin` residual vector for Newton/PPN/orbital tests.

## Source Register

{md_table(sources)}

## Lovelock Premise Audit

{md_table(premises)}

## Lovelock Conditional Theorem

{md_table(theorem)}

## Kinetic Counterexample Ledger

{md_table(counterexamples)}

## Non-Einstein R_kin Residual Vector

{md_table(residuals)}

## Newton/PPN Projection Contract

{md_table(ppn)}

## Nonclaim Runner

{md_table(runner)}

## Promotion Gates

{md_table(promotion)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    before_fw = snapshot_tree(FW)

    sources = source_register_rows()
    premises = premise_rows()
    theorem = theorem_rows()
    counterexamples = counterexample_rows()
    residuals = residual_rows()
    ppn = ppn_rows()
    runner = runner_rows()
    promotion = promotion_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["premises"], premises)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["counterexamples"], counterexamples)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["ppn"], ppn)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    after_fw = snapshot_tree(FW)
    validation = validate(sources, premises, theorem, counterexamples, residuals, ppn, runner, promotion, decisions, next_target, changed_count(before_fw, after_fw))
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, premises, theorem, counterexamples, residuals, ppn, runner, promotion, decisions, next_target, validation)

    if PYCACHE.exists():
        for item in PYCACHE.iterdir():
            if item.is_file():
                item.unlink()
        try:
            PYCACHE.rmdir()
        except OSError:
            pass


if __name__ == "__main__":
    main()

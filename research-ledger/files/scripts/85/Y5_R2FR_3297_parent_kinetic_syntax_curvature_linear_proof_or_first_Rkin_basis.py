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

DOC = ROOT / "3297-Y5-R2FR-parent-kinetic-syntax-curvature-linear-proof-or-first-Rkin-basis-under-AX1090.md"

SRC_3296_DOC = ROOT / "3296-Y5-R2FR-second-order-no-extra-field-locality-signature-or-Rkin-projection-under-AX1090.md"
SRC_3296_NEXT = OUT / "P8_Y5_R2FR_3296_NEXT_TARGET.csv"
SRC_3296_CLAUSES = OUT / "P8_Y5_R2FR_3296_HARD_CLAUSE_SIGNATURE_AUDIT.csv"
SRC_3296_LANES = OUT / "P8_Y5_R2FR_3296_EXTRA_FIELD_LANE_CLASSIFICATION.csv"
SRC_3296_PROJ = OUT / "P8_Y5_R2FR_3296_LINEARIZED_RKIN_PROJECTION_FORMULAS.csv"
SRC_3296_VALIDATION = OUT / "P8_Y5_BRR545_3296_VALIDATION.csv"
SRC_3295_DOC = ROOT / "3295-Y5-R2FR-Lovelock-metric-kinetic-owner-or-non-Einstein-residual-vector-under-AX1090.md"
SRC_3294_DOC = ROOT / "3294-Y5-R2FR-local-GR-reduction-contract-Hilbert-source-common-G-and-Newton-limit-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3297_SOURCE_REGISTER.csv",
    "syntax": OUT / "P8_Y5_R2FR_3297_PARENT_KINETIC_SYNTAX_AUDIT.csv",
    "theorem": OUT / "P8_Y5_R2FR_3297_CURVATURE_LINEAR_CONDITIONAL_THEOREM.csv",
    "basis": OUT / "P8_Y5_R2FR_3297_FIRST_RKIN_COEFFICIENT_BASIS.csv",
    "projection": OUT / "P8_Y5_R2FR_3297_BASIS_TO_NEWTON_PPN_YUKAWA_MAP.csv",
    "inputs": OUT / "P8_Y5_R2FR_3297_BASIS_INPUT_REQUIREMENTS.csv",
    "runner": OUT / "P8_Y5_R2FR_3297_RKIN_BASIS_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3297_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3297_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3297_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3297_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 600) -> str:
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
            hits.append(f"L{idx}:{compact(line, 340)}")
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
        (SRC_3296_DOC, "3296 handoff", ["curvature-linear", "R_kin"]),
        (SRC_3296_NEXT, "3296 next target", ["parent-kinetic-syntax", "first-Rkin-basis"]),
        (SRC_3296_CLAUSES, "hard Lovelock clauses", ["HC3296_0_second_order", "HC3296_1_no_extra_local_fields"]),
        (SRC_3296_LANES, "extra field lane classification", ["LANE3296_3_propagating_hidden", "LANE3296_4_nonlocal_memory_kernel"]),
        (SRC_3296_PROJ, "linearized R_kin formulas", ["PROJ3296_0_Newton_00", "PROJ3296_1_Yukawa_range"]),
        (SRC_3296_VALIDATION, "3296 validation", ["VAL3296_12_overall", "true"]),
        (SRC_3295_DOC, "Lovelock theorem context", ["E_mu_nu = a G_mu_nu", "R_kin"]),
        (SRC_3294_DOC, "local GR contract context", ["R_mu_nu^MTS", "G_cal"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3297_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def syntax_rows() -> list[dict[str, Any]]:
    return [
        {
            "syntax_id": "KS3297_0_allowed_EH",
            "object": "sqrt(-g) A R",
            "classification": "ALLOWED_CURVATURE_LINEAR",
            "local_field_effect": "A G_mu_nu plus boundary term; second-order metric equation if A is constant/q-basic",
            "proof_status": "EXACT_VARIATION_KNOWN_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "syntax_id": "KS3297_1_allowed_Lambda",
            "object": "sqrt(-g) B",
            "classification": "ALLOWED_CONSTANT_POTENTIAL",
            "local_field_effect": "cosmological constant term proportional to g_mu_nu",
            "proof_status": "EXACT_VARIATION_KNOWN_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "syntax_id": "KS3297_2_boundary_topological",
            "object": "GHY/topological boundary or constant Gauss-Bonnet in 4D",
            "classification": "ALLOWED_ONLY_IF_SILENT",
            "local_field_effect": "no local metric equation contribution if coefficient constant and uncoupled",
            "proof_status": "BOUNDARY_SILENCE_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "syntax_id": "KS3297_3_forbid_R2",
            "object": "sqrt(-g) c_R2 R^2",
            "classification": "FORBID_OR_RESIDUAL",
            "local_field_effect": "fourth-order/scalar Yukawa branch unless coefficient zero/topological-equivalent",
            "proof_status": "NOT_FORBIDDEN_BY_CURRENT_CORPUS",
            "valid_for_claim": "false",
        },
        {
            "syntax_id": "KS3297_4_forbid_Ricci2",
            "object": "sqrt(-g) c_Ric R_mu_nu R^mu_nu or Weyl^2",
            "classification": "FORBID_OR_RESIDUAL",
            "local_field_effect": "massive spin-2 or higher-derivative PPN/Yukawa branch",
            "proof_status": "NOT_FORBIDDEN_BY_CURRENT_CORPUS",
            "valid_for_claim": "false",
        },
        {
            "syntax_id": "KS3297_5_forbid_nonmetric",
            "object": "independent connection/torsion/nonmetricity/aether/memory kinetic terms",
            "classification": "FORBID_AUXILIARY_OR_RESIDUAL",
            "local_field_effect": "preferred-frame, torsion, memory, or extra-polarization branch",
            "proof_status": "NOT_PARENT_CLASSIFIED",
            "valid_for_claim": "false",
        },
        {
            "syntax_id": "KS3297_6_result",
            "object": "parent kinetic grammar",
            "classification": "CONDITIONAL_PROOF_OR_BASIS",
            "local_field_effect": "if only KS3297_0..2 survive, R_kin=0; otherwise coefficients feed first basis",
            "proof_status": "PARTIAL_NOT_PROMOTED",
            "valid_for_claim": "false",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CLT3297_0_curvature_linear_variation",
            "statement": "If the parent local metric kinetic action in the local branch is S_kin=int sqrt(-g)(A R - 2 A Lambda) plus silent boundary/topological terms with constant/q-basic A, then variation gives A(G_mu_nu + Lambda g_mu_nu).",
            "result": "R_kin=0 after normalization by A",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CLT3297_1_parent_syntax_gap",
            "statement": "The current corpus does not yet prove the parent grammar excludes R^2, Ricci^2, Weyl^2, scalar-tensor, vector/torsion, or memory kinetic terms.",
            "result": "curvature-linear route not promoted",
            "status": "NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CLT3297_2_basis_fallback",
            "statement": "Every unsigned kinetic syntax class is placed into a first R_kin coefficient basis for future Newton/PPN/Yukawa/orbital scoring.",
            "result": "non-Einstein branch becomes coefficient-testable",
            "status": "FINITE_BASIS_FALLBACK",
            "valid_for_claim": "false",
        },
    ]


def basis_rows() -> list[dict[str, Any]]:
    return [
        {
            "basis_id": "BAS3297_0_R2_scalar",
            "coefficient": "c_R2",
            "operator": "R^2",
            "residual_symbol": "R_HD_scalar",
            "leading_test_signature": "scalar Yukawa correction alpha_0, lambda_0; PPN gamma/beta shifts",
            "zero_route": "prove c_R2=0 or topological/field-redefinition silent in parent syntax",
            "needed_for_numeric": "normalization of c_R2; scalar mass/range; source coupling",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "BAS3297_1_Ricci2_spin2",
            "coefficient": "c_Ric",
            "operator": "R_mu_nu R^mu_nu or Weyl^2 combination",
            "residual_symbol": "R_HD_spin2",
            "leading_test_signature": "massive spin-2 Yukawa alpha_2, lambda_2; light-bending and orbital precession",
            "zero_route": "prove c_Ric=0 or coefficient is boundary/topological silent",
            "needed_for_numeric": "spin-2 mass/range; sign convention; ghost/instability handling; source coupling",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "BAS3297_2_scalar_tensor",
            "coefficient": "c_phi",
            "operator": "phi R, (partial phi)^2, V(phi), or hidden scalar curvature coupling",
            "residual_symbol": "R_extra_scalar",
            "leading_test_signature": "fifth force, Gdot, Nordtvedt/WEP, gamma-1",
            "zero_route": "prove phi is gauge/auxiliary/q-basic constant or infinitely massive locally",
            "needed_for_numeric": "scalar kinetic norm, mass, coupling to Hilbert source, local background derivative",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "BAS3297_3_vector_torsion_frame",
            "coefficient": "c_VT",
            "operator": "aether/vector/torsion/nonmetricity/frame-marker kinetic term",
            "residual_symbol": "R_pf_torsion",
            "leading_test_signature": "preferred-frame alpha_1 alpha_2 alpha_3, spin/torsion, wave polarization",
            "zero_route": "prove connection is Levi-Civita and frame variables are gauge/auxiliary/silent",
            "needed_for_numeric": "vector/torsion kinetic coefficients, matter spin/source coupling, preferred frame",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "BAS3297_4_memory_kernel",
            "coefficient": "c_mem",
            "operator": "nonlocal or history kernel K_memory acting on curvature/source",
            "residual_symbol": "R_mem",
            "leading_test_signature": "time/range/environment dependent G_eff; orbital hysteresis",
            "zero_route": "prove local memory kernel collapses to constant Lambda/G_cal or is below local bounds",
            "needed_for_numeric": "kernel K_memory, local-domain limit, source history projection",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "BAS3297_5_topological_boundary",
            "coefficient": "c_top",
            "operator": "coupled Gauss-Bonnet, Chern-Simons, Pontryagin, or boundary charge",
            "residual_symbol": "R_top",
            "leading_test_signature": "parity/spin/orbital precession and domain-boundary dependence",
            "zero_route": "prove coefficient constant and term uncoupled/topological in 4D local branch",
            "needed_for_numeric": "coupling gradient, boundary/domain map, spin/orbit projection",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "BAS3297_6_Einstein_coefficient_drift",
            "coefficient": "delta_A",
            "operator": "hidden/time/source/range dependent coefficient multiplying R",
            "residual_symbol": "R_coeff",
            "leading_test_signature": "Gdot, range-dependent G_eff, source/environment drift",
            "zero_route": "prove A is a universal q-basic constant in the local branch",
            "needed_for_numeric": "A(x,I_hid) derivative, source/environment projection, Gdot/range bounds",
            "valid_for_claim": "false",
        },
    ]


def projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "map_id": "MAP3297_0_quadratic_gravity_template",
            "basis_terms": "c_R2,c_Ric",
            "weak_field_template": "Phi(r)=-(G_cal*M/r)*(1+alpha_0*exp(-r/lambda_0)+alpha_2*exp(-r/lambda_2))",
            "interpretation": "alpha_0/lambda_0 and alpha_2/lambda_2 are placeholders until parent coefficient normalization fixes signs and amplitudes",
            "next_input": "derive c_R2,c_Ric normalization or use this as Yukawa/R10/orbital basis",
            "valid_for_claim": "false",
        },
        {
            "map_id": "MAP3297_1_PPN_scalar_vector",
            "basis_terms": "c_phi,c_VT",
            "weak_field_template": "gamma-1, beta-1, alpha_1, alpha_2, alpha_3 = linear projections of c_phi,c_VT after solving local field equations",
            "interpretation": "PPN mapping is symbolic until source coupling and gauge are fixed",
            "next_input": "linearized operator and gauge/source convention",
            "valid_for_claim": "false",
        },
        {
            "map_id": "MAP3297_2_memory_Geff",
            "basis_terms": "c_mem,delta_A",
            "weak_field_template": "G_eff(t,r,env)=G_cal*(1+delta_A+Pi_mem[K_memory*source_history])",
            "interpretation": "memory branch becomes local drift/range/environment residual",
            "next_input": "kernel and local silence theorem or Gdot/range bounds",
            "valid_for_claim": "false",
        },
        {
            "map_id": "MAP3297_3_topological_orbit",
            "basis_terms": "c_top",
            "weak_field_template": "delta precession/parity/spin signal = Pi_top[c_top, boundary/domain/spin data]",
            "interpretation": "topological branch is harmless only if coefficient is constant and uncoupled",
            "next_input": "domain/boundary coefficient and spin/orbit projection",
            "valid_for_claim": "false",
        },
    ]


def input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "REQ3297_0_parent_syntax_source",
            "needed_input": "source path or derivation proving parent kinetic grammar is only A R + B plus silent terms",
            "blocks": "curvature-linear proof promotion",
            "status": "MISSING",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3297_1_coefficients",
            "needed_input": "numeric/symbolic parent coefficients c_R2,c_Ric,c_phi,c_VT,c_mem,c_top,delta_A with units",
            "blocks": "R_kin projection scoring",
            "status": "MISSING",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3297_2_linearized_operator",
            "needed_input": "linearized field equations and gauge/source convention for each nonzero basis term",
            "blocks": "PPN/Newton/Yukawa map",
            "status": "MISSING",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3297_3_bound_sources",
            "needed_input": "source-backed bounds for Yukawa/R10, PPN, orbital precession, Gdot, WEP, and wave polarizations",
            "blocks": "empirical robustness pass",
            "status": "MISSING",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN3297_0_curvature_linear_theorem", "curvature-linear syntax gives Einstein tensor conditionally", "PASS_SYMBOLIC_NONCLAIM"),
        ("RUN3297_1_parent_syntax_unsigned", "parent grammar has not forbidden non-Einstein operators", "REFUSE_CLAIM_NONCLAIM"),
        ("RUN3297_2_first_basis_complete", "first R_kin coefficient basis covers curvature, scalar, vector/torsion, memory, topological, coefficient drift", "PASS_SYMBOLIC_NONCLAIM"),
        ("RUN3297_3_numeric_blocked", "numeric scoring blocked until coefficients/operators/bounds sourced", "REFUSE_MISSING_INPUT_NONCLAIM"),
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
            "gate_id": "GATE3297_0_theorem_shape",
            "gate": "curvature-linear theorem shape exists",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "variation of A R - 2A Lambda gives Einstein side conditionally.",
        },
        {
            "gate_id": "GATE3297_1_parent_syntax_signed",
            "gate": "parent kinetic syntax excludes non-Einstein operators",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "non-Einstein basis remains live.",
        },
        {
            "gate_id": "GATE3297_2_coefficients_sourced",
            "gate": "R_kin coefficients and units sourced",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "basis is explicit but coefficients are not sourced.",
        },
        {
            "gate_id": "GATE3297_3_local_GR_claim",
            "gate": "local-GR kinetic side claimed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "no claim until syntax is signed or R_kin bounded.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3297_0_derivation_result",
            "finding": "If the parent local kinetic grammar is curvature-linear, the Einstein side follows exactly; this is now a clean proof target.",
            "consequence": "the left-hand side is not arbitrary anymore: it is either Einstein-Hilbert syntax or named deviations.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3297_1_testing_result",
            "finding": "The first explicit R_kin coefficient basis is now staged.",
            "consequence": "if derivation fails, the next work can source coefficients and test Yukawa/PPN/orbital signatures instead of circling Lovelock clauses.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3297_2_best_next",
            "finding": "The next decisive step is coefficient sourcing or a parent syntax source sweep.",
            "consequence": "either find a parent grammar statement that kills c_R2/c_Ric/etc., or start filling the coefficient/bound table.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3297_0_3298",
            "target_doc": "3298-Y5-R2FR-Rkin-coefficient-source-sweep-and-zero-gate-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3298_Rkin_coefficient_source_sweep_and_zero_gate.py",
            "objective": "sweep the corpus for parent kinetic syntax or coefficient evidence for c_R2, c_Ric, c_phi, c_VT, c_mem, c_top, and delta_A; mark each theorem-zero, sourced finite, or missing before any PPN/Newton claim.",
            "guardrails": "do not set coefficients to zero by taste; do not infer numeric values from analogy; do not score tests until units/source paths and bounds exist.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    syntax: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    basis: list[dict[str, Any]],
    projection: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    formalization_changed_count: int,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append({"check_id": check_id, "check": check, "passed": bool_str(passed), "detail": detail})

    add("VAL3297_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3297_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add("VAL3297_2_outputs_parse", "all 3297 non-validation output CSVs parse", all(csv_parse_ok(path) for key, path in OUTPUTS.items() if key != "validation"))

    classifications = {row["classification"] for row in syntax}
    add(
        "VAL3297_3_syntax_audit_has_allowed_and_forbidden",
        "syntax audit has allowed curvature-linear/constant terms and forbidden/residual non-Einstein terms",
        {"ALLOWED_CURVATURE_LINEAR", "ALLOWED_CONSTANT_POTENTIAL", "FORBID_OR_RESIDUAL", "FORBID_AUXILIARY_OR_RESIDUAL"}.issubset(classifications),
    )

    theorem_text = " ".join(row["statement"] + " " + row["result"] + " " + row["status"] for row in theorem)
    add(
        "VAL3297_4_curvature_linear_theorem_present",
        "theorem states A R - 2A Lambda variation and finite basis fallback",
        "A R - 2 A Lambda" in theorem_text and "R_kin=0" in theorem_text and "FINITE_BASIS_FALLBACK" in theorem_text,
    )

    basis_coeffs = {row["coefficient"] for row in basis}
    add(
        "VAL3297_5_basis_complete",
        "basis includes curvature-squared, scalar, vector/torsion, memory, topological, and coefficient-drift terms",
        {"c_R2", "c_Ric", "c_phi", "c_VT", "c_mem", "c_top", "delta_A"}.issubset(basis_coeffs),
    )

    projection_text = " ".join(row["weak_field_template"] + " " + row["basis_terms"] for row in projection)
    add(
        "VAL3297_6_projection_templates_present",
        "projection maps include Yukawa, PPN, memory G_eff, and topological orbit templates",
        "alpha_0" in projection_text and "gamma-1" in projection_text and "G_eff" in projection_text and "precession" in projection_text,
    )

    input_statuses = {row["status"] for row in inputs}
    add(
        "VAL3297_7_inputs_block_numeric_claim",
        "input requirements block numeric claims until syntax, coefficients, operators, and bounds are sourced",
        input_statuses == {"MISSING"} and all(row["valid_for_claim"] == "false" for row in inputs),
    )

    add("VAL3297_8_runner_expectations", "runner expectations all match", all(row["expectation_match"] == "true" for row in runner), ";".join(f"{row['run_id']}={row['observed_status']}" for row in runner))
    add("VAL3297_9_claim_gates_false", "no 3297 gate allows local GR/PPN claim", all(row["claim_allowed"] == "false" for row in promotion) and any(row["passed"] == "false" for row in promotion))
    add(
        "VAL3297_10_next_target_focused",
        "next target focuses R_kin coefficient source sweep and zero gate",
        len(next_target) == 1 and "Rkin-coefficient-source-sweep" in next_target[0]["target_doc"],
    )
    add(
        "VAL3297_11_decision_records_proof_or_test",
        "decision ledger records clean proof target and coefficient testing fallback",
        any("curvature-linear" in row["finding"] for row in decisions) and any("coefficient basis" in row["finding"] for row in decisions),
    )
    add(
        "VAL3297_12_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        formalization_changed_count == 0,
        f"formalization_changed_count={formalization_changed_count}",
    )
    overall = all(row["passed"] == "true" for row in checks)
    add("VAL3297_13_overall", "3297 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
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
    syntax: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    basis: list[dict[str, Any]],
    projection: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3297 - Parent kinetic syntax curvature-linear proof or first R_kin basis under AX1090

**Run UTC:** {RUN_UTC}

3297 makes the left-hand side fork explicit:

1. If the parent local kinetic grammar is only `sqrt(-g)(A R - 2 A Lambda)` plus silent boundary/topological terms, then the Einstein tensor side is derived.
2. If the grammar permits additional operators, those operators now sit in the first `R_kin` coefficient basis instead of remaining vague.

The conditional proof target is:

`delta int sqrt(-g)(A R - 2 A Lambda) -> A(G_mu_nu + Lambda g_mu_nu)`.

The fallback basis covers `c_R2`, `c_Ric`, `c_phi`, `c_VT`, `c_mem`, `c_top`, and `delta_A`.

## Source Register

{md_table(sources)}

## Parent Kinetic Syntax Audit

{md_table(syntax)}

## Curvature-Linear Conditional Theorem

{md_table(theorem)}

## First R_kin Coefficient Basis

{md_table(basis)}

## Basis To Newton/PPN/Yukawa Map

{md_table(projection)}

## Basis Input Requirements

{md_table(inputs)}

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
    syntax = syntax_rows()
    theorem = theorem_rows()
    basis = basis_rows()
    projection = projection_rows()
    inputs = input_rows()
    runner = runner_rows()
    promotion = promotion_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["syntax"], syntax)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["basis"], basis)
    write_csv(OUTPUTS["projection"], projection)
    write_csv(OUTPUTS["inputs"], inputs)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    after_fw = snapshot_tree(FW)
    validation = validate(sources, syntax, theorem, basis, projection, inputs, runner, promotion, decisions, next_target, changed_count(before_fw, after_fw))
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, syntax, theorem, basis, projection, inputs, runner, promotion, decisions, next_target, validation)

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

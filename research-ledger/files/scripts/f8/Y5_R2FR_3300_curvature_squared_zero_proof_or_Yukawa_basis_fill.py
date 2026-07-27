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

DOC = ROOT / "3300-Y5-R2FR-curvature-squared-zero-proof-or-Yukawa-basis-fill-under-AX1090.md"

SRC_3299_DOC = ROOT / "3299-Y5-R2FR-Rkin-coefficient-ledger-zero-proof-priority-order-under-AX1090.md"
SRC_3299_PRIORITY = OUT / "P8_Y5_R2FR_3299_RKIN_PRIORITY_LEDGER.csv"
SRC_3299_ZERO = OUT / "P8_Y5_R2FR_3299_ZERO_PROOF_ROUTE_LEDGER.csv"
SRC_3299_FINITE = OUT / "P8_Y5_R2FR_3299_FINITE_SOURCE_ROUTE_LEDGER.csv"
SRC_3299_NEXT = OUT / "P8_Y5_R2FR_3299_NEXT_TARGET.csv"
SRC_3299_VALIDATION = OUT / "P8_Y5_BRR545_3299_VALIDATION.csv"
SRC_3297_BASIS = OUT / "P8_Y5_R2FR_3297_FIRST_RKIN_COEFFICIENT_BASIS.csv"
SRC_3297_PROJECTION = OUT / "P8_Y5_R2FR_3297_BASIS_TO_NEWTON_PPN_YUKAWA_MAP.csv"
SRC_3296_PROJECTION = OUT / "P8_Y5_R2FR_3296_LINEARIZED_RKIN_PROJECTION_FORMULAS.csv"
SRC_3295_DOC = ROOT / "3295-Y5-R2FR-Lovelock-metric-kinetic-owner-or-non-Einstein-residual-vector-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3300_SOURCE_REGISTER.csv",
    "conditional_zero": OUT / "P8_Y5_R2FR_3300_CURVATURE_SQUARED_CONDITIONAL_ZERO_PROOF.csv",
    "operator_variation": OUT / "P8_Y5_R2FR_3300_R2_RICCI2_VARIATION_AUDIT.csv",
    "yukawa_basis": OUT / "P8_Y5_R2FR_3300_CURVATURE_SQUARED_YUKAWA_BASIS.csv",
    "ppn_orbital": OUT / "P8_Y5_R2FR_3300_PPN_ORBITAL_FALLBACK_MAP.csv",
    "promotion": OUT / "P8_Y5_R2FR_3300_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3300_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3300_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3300_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 620) -> str:
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
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    for line_number, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered_needles):
            hits.append(f"L{line_number}:{compact(line, 360)}")
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
        (SRC_3299_DOC, "3299 priority handoff", ["curvature-squared", "c_R2", "c_Ric"]),
        (SRC_3299_PRIORITY, "3299 rank order", ["c_R2", "c_Ric"]),
        (SRC_3299_ZERO, "3299 zero route ledger", ["curvature-linear", "Ricci"]),
        (SRC_3299_FINITE, "3299 finite route ledger", ["Yukawa", "PPN"]),
        (SRC_3299_NEXT, "3299 next target", ["curvature-squared-zero-proof", "Yukawa"]),
        (SRC_3299_VALIDATION, "3299 validation", ["VAL3299_12_overall", "true"]),
        (SRC_3297_BASIS, "3297 R_kin basis", ["BAS3297_0_R2_scalar", "BAS3297_1_Ricci2_spin2"]),
        (SRC_3297_PROJECTION, "3297 projection map", ["Yukawa", "PPN"]),
        (SRC_3296_PROJECTION, "3296 linearized projection", ["PROJ3296_0_Newton_00", "PROJ3296_1_Yukawa_range"]),
        (SRC_3295_DOC, "3295 Lovelock guard context", ["Lovelock", "second-order"]),
    ]
    rows: list[dict[str, Any]] = []
    for index, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3300_{index}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def conditional_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "CZ3300_0_local_kinetic_template",
            "clause": "Assume the local metric branch parent kinetic action descends to S_kin^loc = integral sqrt(-g) A_loc (R - 2 Lambda_loc) plus silent boundary/topological terms.",
            "derivation_role": "sets the exact grammar needed to inherit Einstein tensor dynamics without independent curvature-squared operators",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "CZ3300_1_second_order_principal_symbol",
            "clause": "The local metric equation must be second order in g_mu_nu with spin-2 principal symbol only; otherwise R^2/Ricci^2/Weyl^2 terms generate higher-derivative or extra-mode residuals.",
            "derivation_role": "if parent signs this clause, independent bulk c_R2 and c_Ric are forced to zero",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "CZ3300_2_c_R2_zero",
            "clause": "An independent bulk c_R2 R^2 term varies into terms containing R R_mu_nu and nabla_mu nabla_nu R - g_mu_nu box R; these are not present in the Einstein-Hilbert branch.",
            "derivation_role": "therefore c_R2=0 in the local branch if the curvature-linear/second-order parent syntax is signed",
            "status": "PROVES_ZERO_IF_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "CZ3300_3_c_Ric_zero",
            "clause": "Independent Ricci^2 or Weyl^2 terms vary into box R_mu_nu, nabla nabla R, and massive spin-2/high-derivative residual structure absent from Einstein-Hilbert dynamics.",
            "derivation_role": "therefore c_Ric=0 in the local branch if the parent syntax excludes independent quadratic curvature",
            "status": "PROVES_ZERO_IF_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "CZ3300_4_gauss_bonnet_guard",
            "clause": "In four dimensions, constant uncoupled Gauss-Bonnet is locally silent, but generic R^2/Ricci^2/Weyl^2 pieces, nonconstant coefficients, or scalar-coupled Gauss-Bonnet are not silent.",
            "derivation_role": "prevents smuggling a quadratic term through a topological exception",
            "status": "GUARDRAIL_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "CZ3300_5_current_decision",
            "clause": "The zero proof is exact as a conditional theorem, but the parent MTS action has not yet signed the curvature-linear/second-order/no-extra-mode clauses.",
            "derivation_role": "do not claim local-GR pass; move to parent syntax source hunt or finite Yukawa coefficient fill",
            "status": "ZERO_NOT_PROMOTED",
            "valid_for_claim": "false",
        },
    ]


def operator_variation_rows() -> list[dict[str, Any]]:
    return [
        {
            "operator_id": "VAR3300_0_Einstein_Hilbert",
            "operator": "sqrt(-g) A R",
            "metric_variation_signature": "A G_mu_nu plus boundary term for constant/q-basic A",
            "local_mode_added": "none",
            "zero_condition": "allowed local branch core",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "VAR3300_1_cosmological_constant",
            "operator": "sqrt(-g) (-2 A Lambda)",
            "metric_variation_signature": "A Lambda g_mu_nu",
            "local_mode_added": "none",
            "zero_condition": "absorbed into local Lambda/residual bookkeeping",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "VAR3300_2_R_squared",
            "operator": "sqrt(-g) c_R2 R^2",
            "metric_variation_signature": "c_R2 [2 R R_mu_nu - 1/2 g_mu_nu R^2 - 2(nabla_mu nabla_nu - g_mu_nu box)R]",
            "local_mode_added": "scalar/high-derivative Yukawa branch",
            "zero_condition": "c_R2=0 or parent field-redefinition/topological silence proof",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "VAR3300_3_Ricci_squared",
            "operator": "sqrt(-g) c_Ric R_mu_nu R^mu_nu",
            "metric_variation_signature": "terms including box R_mu_nu, nabla_mu nabla_nu R, g_mu_nu box R, and quadratic Ricci contractions",
            "local_mode_added": "massive spin-2/high-derivative branch",
            "zero_condition": "c_Ric=0 or exact silent topological combination with all non-silent pieces removed",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "VAR3300_4_Weyl_squared",
            "operator": "sqrt(-g) c_W C_mu_nu_rho_sigma C^mu_nu_rho_sigma",
            "metric_variation_signature": "Bach-tensor type fourth-order contribution",
            "local_mode_added": "conformal spin-2/high-derivative branch",
            "zero_condition": "c_W=0 or no independent Weyl-squared bulk term",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "VAR3300_5_Gauss_Bonnet",
            "operator": "sqrt(-g) b_GB Gauss-Bonnet = sqrt(-g) b_GB (Riemann^2 - 4 Ricci^2 + R^2)",
            "metric_variation_signature": "locally silent only in 4D with constant uncoupled b_GB and harmless boundary",
            "local_mode_added": "none only under strict guardrail",
            "zero_condition": "not a license for generic c_R2/c_Ric/Weyl terms",
            "valid_for_claim": "false",
        },
    ]


def yukawa_basis_rows() -> list[dict[str, Any]]:
    return [
        {
            "basis_id": "YB3300_0_scalar_R2",
            "coefficient": "c_R2",
            "mode": "scalar_curvature_mode",
            "symbols": "alpha_0, lambda_0, m_0",
            "potential_template": "V(r) = -G_cal m1 m2/r * [1 + alpha_0 exp(-r/lambda_0)]",
            "projection_template": "lambda_0 = 1/m_0; alpha_0 requires parent normalization and Hilbert-source coupling",
            "required_parent_inputs": "c_R2 value or zero theorem; kinetic normalization; scalar mass/range; universal source coupling; units",
            "first_bound_arenas": "R10/Yukawa, PPN gamma/beta, orbital ephemerides",
            "current_status": "SYMBOLIC_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "YB3300_1_spin2_Ricci_Weyl",
            "coefficient": "c_Ric",
            "mode": "massive_spin2_or_Bach_mode",
            "symbols": "alpha_2, lambda_2, m_2",
            "potential_template": "V(r) = -G_cal m1 m2/r * [1 + alpha_2 exp(-r/lambda_2)] plus light-bending/orbital metric-slip corrections",
            "projection_template": "lambda_2 = 1/m_2; alpha_2 and sign require exact operator normalization and ghost/stability handling",
            "required_parent_inputs": "c_Ric/c_W value or zero theorem; spin-2 mass/range; sign convention; source coupling; units",
            "first_bound_arenas": "PPN light bending, orbital precession, R10/Yukawa if finite range",
            "current_status": "SYMBOLIC_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "YB3300_2_combined_quadratic_branch",
            "coefficient": "c_R2+c_Ric",
            "mode": "two-mode_quadratic_curvature_residual",
            "symbols": "alpha_eff(lambda), gamma(r)-1, beta(r)-1",
            "potential_template": "V(r) = -G_cal m1 m2/r * [1 + alpha_0 exp(-r/lambda_0) + alpha_2 exp(-r/lambda_2)]",
            "projection_template": "compare against local bounds only after mode amplitudes and ranges are parent-derived or sourced",
            "required_parent_inputs": "both zero theorem clauses or both finite coefficient maps",
            "first_bound_arenas": "joint R10/PPN/orbital consistency, not cherry-picked single arena",
            "current_status": "SYMBOLIC_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def ppn_orbital_rows() -> list[dict[str, Any]]:
    return [
        {
            "map_id": "PO3300_0_Newtonian_limit",
            "branch": "curvature_squared_zero",
            "condition": "CZ3300_0..4 parent-signed",
            "local_effect": "standard Poisson equation with G_cal and no quadratic-curvature residual source",
            "test_handle": "local GR/Newton branch can proceed to remaining delta_A/c_mem/c_phi/c_VT/c_top checks",
            "current_status": "CONDITIONAL_ONLY",
            "valid_for_claim": "false",
        },
        {
            "map_id": "PO3300_1_R2_PPN",
            "branch": "finite_c_R2",
            "condition": "alpha_0/lambda_0 derived or sourced",
            "local_effect": "metric slip and PPN gamma/beta shift as a function of range and environment",
            "test_handle": "Cassini/light-bending/ephemerides plus R10 if lambda_0 is short-range",
            "current_status": "SYMBOLIC_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "map_id": "PO3300_2_Ricci_Weyl_PPN",
            "branch": "finite_c_Ric",
            "condition": "alpha_2/lambda_2 and stable sign convention derived or sourced",
            "local_effect": "spin-2 metric slip, light-bending change, and perihelion/precession residuals",
            "test_handle": "PPN/orbital first; R10/Yukawa only if a finite range is obtained",
            "current_status": "SYMBOLIC_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "map_id": "PO3300_3_no_single_arena_claim",
            "branch": "finite_quadratic_curvature",
            "condition": "all nonzero modes must clear their own strongest local arenas",
            "local_effect": "a pass in one Yukawa window does not erase PPN/orbital/light-bending constraints",
            "test_handle": "multi-arena consistency gate",
            "current_status": "GUARDRAIL",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3300_0_zero_promote",
            "claim": "promote c_R2=c_Ric=0",
            "requirements": "parent-signed local branch action is curvature-linear, second-order, single metric, no extra local modes, with only constant uncoupled silent topological/boundary terms",
            "current_evidence": "conditional theorem written; parent signature still missing",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3300_1_finite_promote",
            "claim": "score finite quadratic-curvature residuals against local bounds",
            "requirements": "numeric or algebraic c_R2/c_Ric/c_W with units, source paths, source coupling, mass/range, sign convention, and bound curves",
            "current_evidence": "symbolic alpha_0/lambda_0 and alpha_2/lambda_2 schema only",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3300_2_local_GR_claim",
            "claim": "local GR reduction passes the curvature-squared gate",
            "requirements": "GATE3300_0 true, or GATE3300_1 true with residuals below all relevant arenas",
            "current_evidence": "neither gate true",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3300_0",
            "question": "Did 3300 prove the curvature-squared coefficients are zero?",
            "answer": "not as a claim; it produced the exact parent contract that would zero them",
            "reason": "the variation argument is exact, but the parent MTS action has not yet signed the curvature-linear/second-order/no-extra-mode clauses",
            "next_action": "hunt for the parent syntax signature; if absent, fill finite coefficient rows and source bounds",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3300_1",
            "question": "What has moved forward?",
            "answer": "c_R2/c_Ric are no longer a vague missing item; they now have a binary proof gate and a finite Yukawa/PPN fallback map",
            "reason": "the branch either becomes zero by parent grammar or becomes alpha_0/lambda_0 and alpha_2/lambda_2 with explicit arena duties",
            "next_action": "3301 parent-syntax source hunt or quadratic bound acquisition",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3300_0_3301",
            "target_doc": "3301-Y5-R2FR-parent-curvature-linear-signature-hunt-or-quadratic-bound-fill-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3301_parent_curvature_linear_signature_hunt_or_quadratic_bound_fill.py",
            "objective": "search the parent corpus for a real curvature-linear/second-order/no-extra-mode signature; if not found, fill c_R2/c_Ric finite coefficient/bound rows without claiming a local-GR pass",
            "guardrails": "do not infer c_R2=c_Ric=0 from taste; do not use Gauss-Bonnet silence for generic quadratic curvature; do not score symbolic alpha rows as predictions",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    validation_rows: list[dict[str, Any]] = []

    sources = source_register_rows()
    source_paths = [Path(row["path"]) for row in sources]
    outputs_to_parse = [path for key, path in OUTPUTS.items() if key != "validation"]
    conditional_zero = conditional_zero_rows()
    operator_variation = operator_variation_rows()
    yukawa_basis = yukawa_basis_rows()
    ppn_orbital = ppn_orbital_rows()
    gates = promotion_gate_rows()
    next_rows = next_target_rows()

    checks = [
        (
            "VAL3300_0_sources_exist",
            "all cited source paths exist",
            all(path.exists() for path in source_paths),
            "",
        ),
        (
            "VAL3300_1_sources_parse",
            "all cited source paths parse",
            all(parse_ok(path) for path in source_paths),
            "",
        ),
        (
            "VAL3300_2_outputs_parse",
            "all 3300 non-validation output CSVs parse",
            all(csv_parse_ok(path) for path in outputs_to_parse),
            "",
        ),
        (
            "VAL3300_3_zero_covers_R2_Ricci",
            "conditional zero proof covers c_R2 and c_Ric",
            any("c_R2=0" in row["derivation_role"] for row in conditional_zero)
            and any("c_Ric=0" in row["derivation_role"] for row in conditional_zero),
            "",
        ),
        (
            "VAL3300_4_operator_variations_include_quadratic",
            "operator variation audit includes R^2, Ricci^2, Weyl^2, and Gauss-Bonnet guard",
            all(
                any(needle in row["operator"] for row in operator_variation)
                for needle in ["R^2", "R_mu_nu R^mu_nu", "C_mu_nu", "Gauss"]
            ),
            "",
        ),
        (
            "VAL3300_5_yukawa_basis_complete",
            "fallback basis includes alpha_0/lambda_0 and alpha_2/lambda_2",
            any("alpha_0" in row["symbols"] and "lambda_0" in row["symbols"] for row in yukawa_basis)
            and any("alpha_2" in row["symbols"] and "lambda_2" in row["symbols"] for row in yukawa_basis),
            "",
        ),
        (
            "VAL3300_6_ppn_orbital_map_present",
            "PPN/orbital fallback map is present and non-claim",
            len(ppn_orbital) >= 4 and all(row["valid_for_claim"] == "false" for row in ppn_orbital),
            "",
        ),
        (
            "VAL3300_7_no_claim_gates_pass",
            "no 3300 gate allows a local-GR or residual pass claim",
            all(row["passed"] == "false" and row["valid_for_claim"] == "false" for row in gates),
            "",
        ),
        (
            "VAL3300_8_next_target_precise",
            "next target hunts parent curvature-linear signature or fills finite bounds",
            "curvature-linear-signature" in next_rows[0]["target_doc"]
            and "quadratic-bound" in next_rows[0]["target_doc"],
            "",
        ),
    ]

    formalization_after = snapshot_tree(FW)
    formalization_changed = changed_count(formalization_before, formalization_after)
    checks.append(
        (
            "VAL3300_9_formalization_untouched",
            "formalization-workbench modified-file count remains zero by this script",
            formalization_changed == 0,
            f"formalization_changed_count={formalization_changed}",
        )
    )

    overall = all(passed for _, _, passed, _ in checks)
    checks.append(
        (
            "VAL3300_10_overall",
            "3300 validation overall",
            overall,
            "all required checks passed" if overall else "one or more checks failed",
        )
    )

    for check_id, check, passed, detail in checks:
        validation_rows.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_str(passed),
                "detail": detail,
            }
        )
    return validation_rows


def render_doc() -> str:
    source_table = "\n".join(
        f"- `{row['source_id']}`: `{row['path']}` — exists={row['exists']}; parse_ok={row['parse_ok']}; role={row['role']}"
        for row in source_register_rows()
    )
    zero_table = "\n".join(
        f"- `{row['proof_id']}`: {row['clause']} Status: `{row['status']}`."
        for row in conditional_zero_rows()
    )
    variation_table = "\n".join(
        f"- `{row['operator_id']}` `{row['operator']}` -> {row['metric_variation_signature']}"
        for row in operator_variation_rows()
    )
    yukawa_table = "\n".join(
        f"- `{row['basis_id']}` `{row['coefficient']}`: `{row['symbols']}`; {row['potential_template']} Required: {row['required_parent_inputs']}."
        for row in yukawa_basis_rows()
    )
    ppn_table = "\n".join(
        f"- `{row['map_id']}` `{row['branch']}`: {row['local_effect']} Test handle: {row['test_handle']}."
        for row in ppn_orbital_rows()
    )
    gate_table = "\n".join(
        f"- `{row['gate_id']}`: `{row['claim']}` passed={row['passed']}; requirement={row['requirements']}"
        for row in promotion_gate_rows()
    )
    next_row = next_target_rows()[0]

    return f"""# 3300 - Curvature-squared zero proof or Yukawa basis fill under AX1090

Run UTC: `{RUN_UTC}`

## Verdict

This checkpoint makes a real derivation move, not just a missing-input note.

The local curvature-squared branch now has a binary contract:

1. If the parent local kinetic grammar is signed as curvature-linear, second-order, single-metric, and free of extra local modes, then independent bulk `c_R2 R^2`, `c_Ric R_mu_nu R^mu_nu`, and `c_W Weyl^2` terms are zero in the local branch.
2. If that grammar is not parent-signed, the same coefficients must be treated as finite residuals and mapped into `alpha_0/lambda_0` and `alpha_2/lambda_2` Yukawa/PPN/orbital tests.

No local-GR pass is claimed here.

## Exact Conditional Derivation

Take the local metric kinetic branch to be

`S_kin^loc = integral d^4x sqrt(-g) A_loc (R - 2 Lambda_loc) + S_silent_boundary/topological`.

For constant or q-basic `A_loc`, variation of the Einstein-Hilbert term gives the Einstein tensor plus the usual boundary term, and variation of the constant potential gives the cosmological term. This produces

`A_loc (G_mu_nu + Lambda_loc g_mu_nu)`.

An independent bulk `R^2` term is not silent: its metric variation contains `R R_mu_nu` and `(nabla_mu nabla_nu - g_mu_nu box) R`, so it adds scalar/high-derivative local dynamics.

An independent bulk `Ricci^2` or `Weyl^2` term is not silent: it produces fourth-order/spin-2 residual structure such as `box R_mu_nu`, Bach-type terms, metric slip, and orbital/light-bending corrections.

Therefore, under the parent-signed curvature-linear/second-order/no-extra-mode hypothesis, `c_R2 = 0` and `c_Ric = 0`.

## Guardrail

The Gauss-Bonnet exception is narrow. In four dimensions, constant uncoupled Gauss-Bonnet is locally silent, but that does not silence generic `R^2`, `Ricci^2`, `Weyl^2`, nonconstant coefficients, or scalar-coupled topological terms.

## Source Register

{source_table}

## Conditional Zero Ledger

{zero_table}

## Operator Variation Audit

{variation_table}

## Finite Fallback Basis

{yukawa_table}

## PPN/Orbital Fallback

{ppn_table}

## Promotion Gates

{gate_table}

## Decision

- The zero route is exact but conditional.
- The finite route is now schema-ready but non-claim.
- The project should next hunt for a parent-owned curvature-linear signature; if absent, it should source/fill the finite coefficient route.

## Next Target

- `{next_row['target_doc']}`
- `{next_row['target_script']}`
- Objective: {next_row['objective']}
"""


def main() -> None:
    formalization_before = snapshot_tree(FW)

    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["conditional_zero"], conditional_zero_rows())
    write_csv(OUTPUTS["operator_variation"], operator_variation_rows())
    write_csv(OUTPUTS["yukawa_basis"], yukawa_basis_rows())
    write_csv(OUTPUTS["ppn_orbital"], ppn_orbital_rows())
    write_csv(OUTPUTS["promotion"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())

    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))

    if PYCACHE.exists():
        for child in PYCACHE.rglob("*"):
            if child.is_file():
                child.unlink()
        for child in sorted(PYCACHE.rglob("*"), reverse=True):
            if child.is_dir():
                child.rmdir()
        PYCACHE.rmdir()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

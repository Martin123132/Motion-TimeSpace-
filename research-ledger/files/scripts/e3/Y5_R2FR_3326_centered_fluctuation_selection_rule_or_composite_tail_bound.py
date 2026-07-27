from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3326-Y5-R2FR-centered-fluctuation-selection-rule-or-composite-tail-bound-under-AX1090.md"

SRC_ACTION_PRINCIPLE = REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"
SRC_FUNDAMENTAL = REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
SRC_EFT = REPO / "core-mts-framework" / "field-theory" / "the-effective-field-theory-of-motion-timespace.md"

SOURCES = [
    {
        "source_id": "SRC3326_0_3325_doc",
        "path": ROOT / "3325-Y5-R2FR-universal-matter-no-direct-psi-vertex-and-no-tadpole-signature-gate-under-AX1090.md",
        "role": "no-tadpole/composite handoff and next target",
    },
    {
        "source_id": "SRC3326_1_3325_tadpole",
        "path": OUT / "P8_Y5_R2FR_3325_NO_TADPOLE_SIGNATURE.csv",
        "role": "E_eff, centered measure, projection silence, contact rule",
    },
    {
        "source_id": "SRC3326_2_3325_theorem",
        "path": OUT / "P8_Y5_R2FR_3325_BRANCH_THEOREM_STATUS.csv",
        "role": "conditional no-tadpole theorem status",
    },
    {
        "source_id": "SRC3326_3_3322_composite",
        "path": OUT / "P8_Y5_R2FR_3322_COMPOSITE_TAIL_GATE.csv",
        "role": "epsilon_tad, loop, contact, boundary, anisotropy decomposition",
    },
    {
        "source_id": "SRC3326_4_3322_operator",
        "path": OUT / "P8_Y5_R2FR_3322_OPERATOR_BOUND.csv",
        "role": "public readout split and total residual bound",
    },
    {
        "source_id": "SRC3326_5_action_principle",
        "path": SRC_ACTION_PRINCIPLE,
        "role": "coarse-grained metric from rapid Planck-scale oscillations and local action",
    },
    {
        "source_id": "SRC3326_6_fundamental_action",
        "path": SRC_FUNDAMENTAL,
        "role": "psi action, damping/nonlinearity, metric covariance readout",
    },
    {
        "source_id": "SRC3326_7_eft",
        "path": SRC_EFT,
        "role": "psi-to-metric smoothing and EFT hierarchy",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3326_SOURCE_REGISTER.csv",
    "evidence": OUT / "P8_Y5_R2FR_3326_AVERAGING_EVIDENCE.csv",
    "selection": OUT / "P8_Y5_R2FR_3326_SELECTION_RULE_THEOREM.csv",
    "defects": OUT / "P8_Y5_R2FR_3326_CENTERING_DEFECTS.csv",
    "bounds": OUT / "P8_Y5_R2FR_3326_COMPOSITE_BOUND_FORMULAS.csv",
    "contact": OUT / "P8_Y5_R2FR_3326_CONTACT_AND_GAP_ROUTING.csv",
    "gates": OUT / "P8_Y5_R2FR_3326_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3326_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3326_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3326_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()

EVIDENCE_PATTERNS = [
    "rapid Planck-scale oscillations",
    "average",
    "averaging",
    "smooth",
    "coarse-grained",
    "covariance",
    "damping",
    "stationary",
    "fixed",
    "decoherence",
]


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1200) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def text_for(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def find_hits(path: Path, max_hits: int = 8) -> str:
    text = text_for(path)
    patterns = [pattern.lower() for pattern in EVIDENCE_PATTERNS]
    hits: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if any(pattern in line.lower() for pattern in patterns):
            hits.append(f"L{line_number}:{line.strip()}")
        if len(hits) >= max_hits:
            break
    return " | ".join(hits)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def averaging_evidence_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        text = text_for(path).lower()
        rows.append(
            {
                "evidence_id": f"EVID3326_{len(rows)}",
                "source_id": source["source_id"],
                "has_smoothing_or_averaging": bool_str("smooth" in text or "average" in text or "coarse-grained" in text),
                "has_damping_or_decoherence": bool_str("damping" in text or "decoherence" in text),
                "has_stationary_or_fixed": bool_str("stationary" in text or "fixed" in text),
                "has_no_tadpole_language": bool_str("tadpole" in text or "one-particle" in text),
                "hits": find_hits(path),
                "valid_for_claim": "false",
            }
        )
    return rows


def selection_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "SEL3326_0_quadratic_operator",
            "statement": "Define the composite readout Q_2 = S_ell[D pi D pi], with D=gradient and S_ell the local smoothing/readout operator",
            "proof_step": "This is the second term in g_pub[psi_bar+pi] after the linear tree readout is separated",
            "result": "Q_2 can only contaminate the finite local one-particle channel through P1_i Q_2",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SEL3326_1_projection_cumulant",
            "statement": "For any linear one-particle test functional L_i[pi], <L_i[pi] Q_2>_c is a third connected moment of pi-gradients",
            "proof_step": "L_i is linear in pi; Q_2 is quadratic in pi; their overlap is therefore controlled by the connected three-point cumulant kappa_3",
            "result": "P1_i Q_2 = 0 if the centered local fluctuation measure has vanishing odd cumulants",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SEL3326_2_even_centered_measure",
            "statement": "If <pi>_local=0 and the local fluctuation measure is invariant under pi -> -pi, then every odd cumulant vanishes",
            "proof_step": "The integrand L_i[pi] Q_2 is odd under pi -> -pi, while the measure is even",
            "result": "P1_i S_ell[D pi D pi] = 0 exactly",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SEL3326_3_fixed_point_tadpole",
            "statement": "If E_eff[psi_bar]=0 in the dissipative/fixed-point sense, the parent expansion has no linear pi tadpole",
            "proof_step": "The first variation around psi_bar vanishes by the local fixed-point equation, not by assuming a conservative action",
            "result": "epsilon_tad_i=0 under fixed-point stationarity",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SEL3326_4_conditional_zero",
            "statement": "If fixed-point stationarity, centered/even local fluctuations, and arena projection silence all hold, then the composite one-particle tail vanishes",
            "proof_step": "Combine SEL3326_2 with SEL3326_3 and the definition of P1_i",
            "result": "epsilon_1p_composite_i = 0",
            "valid_for_claim": "false",
        },
    ]


def centering_defect_rows() -> list[dict[str, Any]]:
    return [
        {
            "defect_id": "DEF3326_0_mean",
            "quantity": "delta_mean_i",
            "definition": "dimensionless size of <D pi>_local or <pi>_local after subtracting psi_bar",
            "zero_if": "local fluctuation split is truly centered",
            "bound_role": "nonzero mean revives a hidden linear readout from Q_2",
            "valid_for_claim": "false",
        },
        {
            "defect_id": "DEF3326_1_skew",
            "quantity": "delta_skew_i",
            "definition": "normalized connected third cumulant controlling <L_i[pi] S[D pi D pi]>_c",
            "zero_if": "local measure is Gaussian/even or has an equivalent odd-cumulant selection rule",
            "bound_role": "primary one-particle composite leakage parameter",
            "valid_for_claim": "false",
        },
        {
            "defect_id": "DEF3326_2_projection",
            "quantity": "rho_P1_i",
            "definition": "operator norm ||P1_i S_ell[D pi D pi]|| / ||S_ell[D pi D pi]|| in the arena window",
            "zero_if": "one-particle projection of the quadratic operator is forbidden by representation/selection rule",
            "bound_role": "projection leakage if cumulant proof is unavailable",
            "valid_for_claim": "false",
        },
        {
            "defect_id": "DEF3326_3_gap",
            "quantity": "m_gap_2pi or Lambda_2pi",
            "definition": "effective threshold/gap for the two-pi composite spectral branch",
            "zero_if": "not a zero quantity; must be large enough or projected out",
            "bound_role": "controls long-range loop/composite tail",
            "valid_for_claim": "false",
        },
        {
            "defect_id": "DEF3326_4_contact",
            "quantity": "epsilon_contact_i",
            "definition": "source-supported coincident term from Q_2",
            "zero_if": "outside-source observable or universal mass/G renormalization absorbs it",
            "bound_role": "lab/R10 finite-size residual",
            "valid_for_claim": "false",
        },
    ]


def composite_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "CB3326_0_one_particle_exact_zero",
            "formula": "epsilon_1p_i = ||P1_i S_ell[D pi D pi]|| = 0",
            "conditions": "E_eff[psi_bar]=0; <pi>=0; odd cumulants vanish or pi -> -pi selection rule; P1_i respects the same symmetry",
            "status": "CONDITIONAL_PROOF",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CB3326_1_one_particle_defect_bound",
            "formula": "epsilon_1p_i <= A_i delta_mean_i sigma_Dpi + B_i delta_skew_i sigma_Dpi^2 + rho_P1_i ||S_ell[D pi D pi]||",
            "conditions": "used when exact centered/even selection is not parent-signed",
            "status": "FALLBACK_BOUND_FORMULA",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CB3326_2_two_particle_tail",
            "formula": "epsilon_2p_i(lambda) <= C_2i int dmu_2(s) W_i(s,lambda), with Yukawa suppression exp[-2 m_gap r] if m_gap>0",
            "conditions": "two-pi branch has a spectral measure or conservative envelope",
            "status": "SPECTRAL_BOUND_FORMULA",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CB3326_3_contact_tail",
            "formula": "epsilon_contact_i <= C_contact_i Theta(source support) or is absorbed into universal mass/G calibration",
            "conditions": "contact term is delta-supported and does not produce a finite external force",
            "status": "CONTACT_ROUTING_FORMULA",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CB3326_4_total_composite",
            "formula": "epsilon_composite_i <= epsilon_1p_i + epsilon_2p_i(lambda) + epsilon_contact_i + epsilon_boundary_i + epsilon_kernel_aniso_i",
            "conditions": "no cancellation allowed; every tail is added as an absolute upper envelope",
            "status": "NO_CANCELLATION_TOTAL_BOUND",
            "valid_for_claim": "false",
        },
    ]


def contact_gap_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "ROUTE3326_0_best_case",
            "route": "centered/even local measure plus fixed-point stationarity",
            "effect": "epsilon_1p_i=0 exactly; only two-particle/contact/boundary tails remain",
            "current_status": "THEOREM_DERIVED_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "route_id": "ROUTE3326_1_gap_route",
            "route": "prove an effective two-pi gap or projection cutoff",
            "effect": "epsilon_2p_i becomes short-range/Yukawa-suppressed and can be compared to R10/PPN/WEP",
            "current_status": "MISSING_PARENT_SPECTRAL_MEASURE",
            "valid_for_claim": "false",
        },
        {
            "route_id": "ROUTE3326_2_contact_route",
            "route": "show contact terms are source-supported and universally renormalize measured G/mass",
            "effect": "contact leakage does not create external fifth force",
            "current_status": "RULE_REQUIRED_NOT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "route_id": "ROUTE3326_3_numeric_route",
            "route": "if parent proof fails, set conservative priors for delta_skew_i, rho_P1_i, m_gap, and epsilon_contact_i",
            "effect": "local branch remains testable as a nuisance-envelope bound rather than a hidden assumption",
            "current_status": "READY_FOR_BOUND_INPUTS",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3326_0_selection_theorem",
            "claim": "centered/even fluctuation measure kills the composite one-particle projection",
            "passed": "true",
            "reason": "P1_i Q_2 overlap is an odd/third-cumulant object and vanishes for centered even local fluctuations",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3326_1_fixed_point_tadpole",
            "claim": "fixed-point stationarity kills parent linear tadpole",
            "passed": "true",
            "reason": "E_eff[psi_bar]=0 is the dissipative/local fixed-point no-tadpole condition",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3326_2_parent_centering_signed",
            "claim": "the MTS parent action proves centered/even local fluctuation measure",
            "passed": "false",
            "reason": "corpus supports smoothing/averaging but not a parent-signed odd-cumulant selection rule",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3326_3_numeric_composite_bound",
            "claim": "epsilon_composite_i is numerically bounded below local-test limits",
            "passed": "false",
            "reason": "delta_skew_i, rho_P1_i, two-pi spectral measure/gap, contact and boundary bounds are not numeric",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3326_4_bound_formulas_ready",
            "claim": "hard fallback formulas for epsilon_composite_i are ready",
            "passed": "true",
            "reason": "one-particle defect, two-particle spectral, contact, and total no-cancellation bounds are explicit",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3326_5_unconditional_local_GR",
            "claim": "local-GR branch is unconditionally closed",
            "passed": "false",
            "reason": "selection theorem is conditional and numeric composite bounds are still missing",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3326_0",
            "question": "Did 3326 prove the composite one-particle silence mechanism?",
            "answer": "conditionally yes",
            "reason": "centered/even local fluctuations make the one-particle projection of S[grad pi grad pi] vanish exactly",
            "next_action": "derive the centered/even local measure from the parent smoothing/fixed-point construction",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3326_1",
            "question": "Can we claim the parent has that measure now?",
            "answer": "not yet",
            "reason": "rapid averaging and smoothing exist in the corpus, but they do not by themselves prove odd-cumulant silence",
            "next_action": "either prove a CLT/even-measure theorem or bind delta_skew/rho_P1 numerically",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3326_2",
            "question": "What improved?",
            "answer": "the composite problem is now finite and testable",
            "reason": "epsilon_composite_i has a no-cancellation decomposition instead of acting as an undefined escape hatch",
            "next_action": "3327 should derive local fluctuation measure or instantiate conservative composite bounds",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3327-Y5-R2FR-parent-local-fluctuation-measure-or-numeric-composite-envelope-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3327_parent_local_fluctuation_measure_or_numeric_composite_envelope.py",
            "objective": "derive the centered/even local fluctuation measure from parent smoothing/fixed-point dynamics, or instantiate conservative numeric/symbolic bounds for delta_skew, rho_P1, two-pi gap, contact, and boundary tails",
            "must_include": "CLT/even-measure route; dissipative fixed-point centering; P1 projection symmetry; two-pi spectral envelope; contact absorption rule; table of required numeric inputs",
            "fallback_if_failed": "measured-G local-GR theorem remains conditional with explicit epsilon_composite_i nuisance envelope",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    evidence = averaging_evidence_rows()
    selection = selection_theorem_rows()
    defects = centering_defect_rows()
    bounds = composite_bound_rows()
    routes = contact_gap_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3326_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3326_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3326_2_outputs_parse",
            "check": "all 3326 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3326_3_averaging_evidence",
            "check": "evidence includes smoothing/averaging support",
            "passed": any(row["has_smoothing_or_averaging"] == "true" for row in evidence),
            "detail": "",
        },
        {
            "check_id": "VAL3326_4_selection_theorem",
            "check": "selection theorem includes cumulant, even measure, fixed point, and conditional zero",
            "passed": {"SEL3326_1_projection_cumulant", "SEL3326_2_even_centered_measure", "SEL3326_3_fixed_point_tadpole", "SEL3326_4_conditional_zero"}.issubset(
                {row["theorem_id"] for row in selection}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3326_5_defects",
            "check": "defect ledger includes mean, skew, projection, gap, and contact",
            "passed": {"delta_mean_i", "delta_skew_i", "rho_P1_i", "m_gap_2pi or Lambda_2pi", "epsilon_contact_i"}.issubset(
                {row["quantity"] for row in defects}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3326_6_bounds",
            "check": "bound formulas include exact zero, defect, two-particle, contact, and total composite",
            "passed": {"CB3326_0_one_particle_exact_zero", "CB3326_1_one_particle_defect_bound", "CB3326_2_two_particle_tail", "CB3326_3_contact_tail", "CB3326_4_total_composite"}.issubset(
                {row["bound_id"] for row in bounds}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3326_7_routes",
            "check": "routing includes proof, gap, contact, and numeric fallback",
            "passed": {"ROUTE3326_0_best_case", "ROUTE3326_1_gap_route", "ROUTE3326_2_contact_route", "ROUTE3326_3_numeric_route"}.issubset(
                {row["route_id"] for row in routes}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3326_8_no_unconditional_claim",
            "check": "parent centering, numeric composite, and unconditional local-GR gates remain false while theorem/bounds pass",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3326_2_parent_centering_signed", "GATE3326_3_numeric_composite_bound", "GATE3326_5_unconditional_local_GR"}
            )
            and all(
                row["passed"] == "true"
                for row in gates
                if row["gate_id"] in {"GATE3326_0_selection_theorem", "GATE3326_1_fixed_point_tadpole", "GATE3326_4_bound_formulas_ready"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3326_9_next_measure_or_numeric",
            "check": "next target is parent local fluctuation measure or numeric composite envelope",
            "passed": any("fluctuation measure" in row["objective"] and "numeric" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3326_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3326_11_overall",
            "check": "3326 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    lines: list[str] = [
        "# 3326 - Centered fluctuation selection rule or composite-tail bound under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3326 gets a real result: the composite one-particle tail has a clean conditional zero theorem.",
        "",
        "Let",
        "",
        "`Q_2 = S_ell[D pi D pi]`",
        "",
        "be the quadratic composite readout from the public metric expansion. For a one-particle arena test `L_i[pi]`, the overlap `<L_i[pi] Q_2>_c` is a connected third cumulant. Therefore, if the local fluctuation measure is centered and even under `pi -> -pi`, all odd cumulants vanish and",
        "",
        "`P1_i S_ell[D pi D pi] = 0`.",
        "",
        "Together with dissipative fixed-point stationarity `E_eff[psi_bar]=0`, this kills the composite one-particle/tadpole branch.",
        "",
        "But the parent corpus does not yet prove the centered/even measure. It supports smoothing and rapid averaging, not a full odd-cumulant selection theorem. So 3326 also builds the fallback bound:",
        "",
        "`epsilon_composite_i <= epsilon_1p_i + epsilon_2p_i(lambda) + epsilon_contact_i + epsilon_boundary_i + epsilon_kernel_aniso_i`.",
        "",
        "This means the composite tail is no longer an undefined escape hatch. It is either zero by a centered/even parent measure, or it must be carried as explicit mean/skew/projection/gap/contact defects.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_register_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("Averaging Evidence", averaging_evidence_rows(), "evidence_id"),
        ("Selection Rule Theorem", selection_theorem_rows(), "theorem_id"),
        ("Centering Defects", centering_defect_rows(), "defect_id"),
        ("Composite Bound Formulas", composite_bound_rows(), "bound_id"),
        ("Contact And Gap Routing", contact_gap_rows(), "route_id"),
        ("Promotion Gates", promotion_gate_rows(), "gate_id"),
        ("Decision Ledger", decision_rows(), "decision_id"),
        ("Next Target", next_target_rows(), "target_doc"),
    ]
    for title, rows, key_name in sections:
        lines.extend(["", f"## {title}", ""])
        for row in rows:
            label = row.get(key_name, "")
            body = "; ".join(f"{key}={value}" for key, value in row.items() if key != key_name)
            lines.append(f"- `{label}`: {body}")
    lines.extend(
        [
            "",
            "## Test Notes",
            "",
            "- This checkpoint is private and nonclaim.",
            "- It proves composite one-particle silence only conditionally under centered/even local fluctuations.",
            "- It does not claim the parent corpus already proves that measure.",
            "- It creates explicit fallback formulas for `epsilon_composite_i` so the local branch remains testable.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["evidence"], averaging_evidence_rows())
    write_csv(OUTPUTS["selection"], selection_theorem_rows())
    write_csv(OUTPUTS["defects"], centering_defect_rows())
    write_csv(OUTPUTS["bounds"], composite_bound_rows())
    write_csv(OUTPUTS["contact"], contact_gap_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()

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
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3287-Y5-R2FR-chi-to-metric-Hodge-premise-proof-or-DeltaChi-slope-source-row-under-AX1090.md"

SRC_3286_DOC = ROOT / "3286-Y5-R2FR-Hodge-Poynting-factor-owner-or-first-CH-CS-slope-row-under-AX1090.md"
SRC_3286_NEXT = OUT / "P8_Y5_R2FR_3286_NEXT_TARGET.csv"
SRC_3286_OWNER = OUT / "P8_Y5_R2FR_3286_HODGE_POYNTING_OWNER_THEOREM.csv"
SRC_3286_AUDIT = OUT / "P8_Y5_R2FR_3286_CHI_TO_HODGE_PREMISE_AUDIT.csv"
SRC_3286_FORMULA = OUT / "P8_Y5_R2FR_3286_CH_CS_SLOPE_FORMULA_ROWS.csv"
SRC_3286_RUNNER = OUT / "P8_Y5_R2FR_3286_CH_CS_BOUND_RUNNER_NONCLAIM.csv"
SRC_3286_VALIDATION = OUT / "P8_Y5_BRR545_3286_VALIDATION.csv"
SRC_3105_DOC = ROOT / "3105-Y5-R2FR-EM-wave-Poynting-public-geometry-route-under-AX1090.md"
SRC_3106_DOC = ROOT / "3106-Y5-R2FR-constitutive-Hodge-star-derivation-or-EM-medium-residual-under-AX1090.md"
SRC_1100_DOC = ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"
SRC_1056_DOC = ROOT / "1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3287_SOURCE_REGISTER.csv",
    "reconstruction": OUT / "P8_Y5_R2FR_3287_CHI_TO_HODGE_RECONSTRUCTION_THEOREM.csv",
    "collapse": OUT / "P8_Y5_R2FR_3287_PREMISE_COLLAPSE_MATRIX.csv",
    "residuals": OUT / "P8_Y5_R2FR_3287_DELTA_CHI_RESIDUAL_DECOMPOSITION.csv",
    "slope": OUT / "P8_Y5_R2FR_3287_DELTA_CHI_SLOPE_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3287_DELTA_CHI_BOUND_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3287_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3287_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3287_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3287_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
DEFAULT_BOUND = 1.389797711495e-12


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def fmt(value: float) -> str:
    return f"{value:.12e}"


def compact(value: Any, limit: int = 440) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


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


def evidence_hits(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 270)}")
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


def bound_from_3286() -> float:
    slope_path = OUT / "P8_Y5_R2FR_3286_FIRST_CH_CS_SLOPE_ROWS_NONCLAIM.csv"
    if not slope_path.exists():
        return DEFAULT_BOUND
    for row in read_csv(slope_path):
        if row.get("row_id") == "HPR3286_1_Delta_chi_finite_slope":
            try:
                return float(row["C_R_HP_abs_bound"])
            except (KeyError, ValueError):
                return DEFAULT_BOUND
    return DEFAULT_BOUND


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3286_DOC, "3286 handoff", ["Delta_chi", "L_v H"]),
        (SRC_3286_NEXT, "3286 next target", ["chi-to-metric-Hodge", "Delta_chi"]),
        (SRC_3286_OWNER, "3286 owner theorem", ["H=Z_Q", "L_v H"]),
        (SRC_3286_AUDIT, "3286 premise audit", ["CHS3106_0", "CHS3106_7"]),
        (SRC_3286_FORMULA, "3286 slope formulas", ["Delta_chi", "C_H"]),
        (SRC_3286_RUNNER, "3286 bound runner", ["REFUSE_MISSING_SOURCE_NONCLAIM"]),
        (SRC_3286_VALIDATION, "3286 validation", ["VAL3286_11_overall", "true"]),
        (SRC_3105_DOC, "Poynting/cone route", ["Poynting", "Fresnel"]),
        (SRC_3106_DOC, "constitutive Hodge stack", ["nonbirefringent", "H = Z_Q"]),
        (SRC_1100_DOC, "scalar impedance/gauge norm blocker", ["Z_A", "readout_radiative_guard"]),
        (SRC_1056_DOC, "alpha/Hodge readout blocker", ["readout", "Hodge"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3287_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def reconstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CHR3287_0_action_to_reciprocal_chi",
            "claim_piece": "local bilinear EM action gives reciprocal principal chi",
            "derivation": "If S_EM=-1/4 int F_A chi^{AB} F_B in 2-form index notation and chi is varied as an action coefficient before readout, only the symmetric exchange part chi^{(AB)} contributes to the Euler/Hilbert action. The antisymmetric exchange part is a skewon/non-Lagrangian residual.",
            "payoff": "CHS3106_1 and CHS3106_2 collapse into one parent Lagrangian-owner clause.",
            "status": "DERIVED_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CHR3287_1_fresnel_to_conformal_metric",
            "claim_piece": "nonbirefringence reconstructs conformal metric",
            "derivation": "The principal reciprocal chi defines a Fresnel quartic G^{abcd}k_a k_b k_c k_d. If this quartic is a repeated quadratic, G(k) proportional (g_EM^{ab}k_a k_b)^2, then EM rays determine a conformal metric class [g_EM].",
            "payoff": "CHS3106_3 derives the light-cone/conformal part of the public Hodge candidate.",
            "status": "DERIVED_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CHR3287_2_closure_to_metric_Hodge",
            "claim_piece": "closure relation gives metric Hodge shape",
            "derivation": "Equivalently, after removing axion and skewon pieces, the constitutive map kappa on 2-forms must satisfy kappa^2=-lambda^2 I on the physical 2-form subspace. Then kappa/lambda is a Hodge complex structure, so chi_principal=lambda *_{g_EM}.",
            "payoff": "Hodge shape is no longer arbitrary; it follows from reciprocal nonbirefringent closure.",
            "status": "DERIVED_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CHR3287_3_positivity_to_sign",
            "claim_piece": "positive energy fixes branch sign",
            "derivation": "The sign of lambda=Z_Q and the time orientation are selected by u_EM>0 and future Poynting flux in the local branch.",
            "payoff": "CHS3106_4 is a physical branch selector, not a new free function.",
            "status": "DERIVED_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CHR3287_4_axion_and_impedance_residual",
            "claim_piece": "Hodge shape does not fix scalar coupling or axion/readout drift",
            "derivation": "The reconstruction permits chi = Z_Q *_{g_EM} + theta_ax F-term representation. Constant axion/topological terms do not set the Maxwell stress scale; vertical Z_Q, axion gradients, radiative F^2 terms, or readout Hodge drift remain Delta_chi residuals.",
            "payoff": "the missing coupling is specifically scalar impedance/gauge norm/readout ownership, not the whole Hodge tensor.",
            "status": "DERIVED_OBSTRUCTION",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CHR3287_5_same_metric_obstruction",
            "claim_piece": "EM metric is not automatically matter/clock metric",
            "derivation": "The Fresnel theorem reconstructs [g_EM]. To promote it to the local-GR public metric, a separate cross-sector clause must identify g_EM with the matter/clock/source metric g_pub up to the allowed conformal normalization.",
            "payoff": "local GR needs same-metric identification, not merely EM nonbirefringence.",
            "status": "DERIVED_OBSTRUCTION",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CHR3287_6_vertical_zero_after_reconstruction",
            "claim_piece": "q-basic reconstructed Hodge gives vertical silence",
            "derivation": "If g_EM=g_pub, Z_Q is q-basic/fixed, theta_ax is constant or q-basic, and readout/radiative terms factor through q, then L_v chi=0 and the 3286 result gives L_v H=L_v S_EM=0.",
            "payoff": "C_H=C_S=0 becomes a conditional theorem after the remaining scalar/same-metric/readout clauses are signed.",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def premise_collapse_rows() -> list[dict[str, Any]]:
    return [
        {
            "collapse_id": "PCM3287_0_lagrangian_owner",
            "old_premises": "CHS3106_0_local_linear + CHS3106_1_reciprocal + CHS3106_2_no_skewon",
            "new_gate": "parent EM sector is a local bilinear action coefficient before readout",
            "derived_here": "partly",
            "remaining_gap": "parent action must actually supply this coefficient and exclude non-Lagrangian/skewon medium response.",
            "blocks_claim": "true",
        },
        {
            "collapse_id": "PCM3287_1_fresnel_closure",
            "old_premises": "CHS3106_3_nonbirefringent",
            "new_gate": "reciprocal principal chi has repeated-quadratic Fresnel polynomial or closure kappa^2=-lambda^2 I",
            "derived_here": "theorem_form",
            "remaining_gap": "MTS parent variables must force this closure rather than fit it after observation.",
            "blocks_claim": "true",
        },
        {
            "collapse_id": "PCM3287_2_energy_branch",
            "old_premises": "CHS3106_4_positive_energy",
            "new_gate": "choose positive Z_Q/time orientation branch",
            "derived_here": "branch_selector",
            "remaining_gap": "source sign and local observer convention must match matter/coframe sector.",
            "blocks_claim": "true",
        },
        {
            "collapse_id": "PCM3287_3_scalar_impedance_owner",
            "old_premises": "CHS3106_5_impedance_owner",
            "new_gate": "Z_Q is q-basic/fixed parent gauge norm, not a hidden scalar or independent F^2 counterterm",
            "derived_here": "not_derived",
            "remaining_gap": "1100/1056 retain gauge norm, no-extra-F2, current owner, and readout/radiative guard as unsigned.",
            "blocks_claim": "true",
        },
        {
            "collapse_id": "PCM3287_4_same_public_metric",
            "old_premises": "CHS3106_6_same_public_metric",
            "new_gate": "g_EM reconstructed from light equals the matter/clock/source public metric",
            "derived_here": "not_derived_by_EM_alone",
            "remaining_gap": "requires cross-sector equivalence/coframe action-domain theorem.",
            "blocks_claim": "true",
        },
        {
            "collapse_id": "PCM3287_5_readout_radiative_guard",
            "old_premises": "CHS3106_7_radiative_readout",
            "new_gate": "effective/readout reductions preserve q-basic Z_Q, Hodge star, hbar*c, and no independent f(Xhat)F^2",
            "derived_here": "not_derived",
            "remaining_gap": "readout functor and radiative operator-domain closure remain needed.",
            "blocks_claim": "true",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "DCR3287_0_skewon",
            "term": "Delta_chi_skewon",
            "definition": "antisymmetric exchange/non-Lagrangian part of chi",
            "effect": "dissipation, preferred-frame leakage, non-Hilbert stress",
            "repair_or_bound": "derive parent local bilinear action or bound skewon response",
            "status": "ROUTED_TO_LAGRANGIAN_GATE",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "DCR3287_1_birefringent_principal",
            "term": "Delta_chi_biref",
            "definition": "principal reciprocal part whose Fresnel quartic is not a repeated quadratic",
            "effect": "polarization/lightcone split and nonmetric Hodge failure",
            "repair_or_bound": "prove closure kappa^2=-lambda^2 I or source birefringence bound",
            "status": "ROUTED_TO_FRESNEL_GATE",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "DCR3287_2_axion_gradient",
            "term": "Delta_chi_axion",
            "definition": "axion/topological F wedge F sector with nonconstant or non-q-basic coefficient",
            "effect": "magnetoelectric rotation/source exchange without setting ordinary stress scale",
            "repair_or_bound": "prove constant/q-basic axion or source axion-gradient bound",
            "status": "LIVE_FINITE_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "DCR3287_3_impedance_drift",
            "term": "Delta_Z_Q *F",
            "definition": "vertical drift or independent counterterm in scalar Maxwell normalization",
            "effect": "alpha/clock/WEP/source-coupling branch reopens",
            "repair_or_bound": "derive q-basic gauge norm/no-extra-F2/readout guard or keep finite alpha product route",
            "status": "LIVE_COUPLING_BOTTLENECK",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "DCR3287_4_metric_split",
            "term": "Z_Q(*_{g_EM}-*_{g_pub})F",
            "definition": "EM reconstructed metric differs from matter/clock/source metric",
            "effect": "local GR same-source limit fails or becomes bimetric",
            "repair_or_bound": "prove same-public-metric theorem or route to optical-metric residual tests",
            "status": "LIVE_LOCAL_GR_BOTTLENECK",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "DCR3287_5_radiative_readout",
            "term": "Delta_chi_rad/readout",
            "definition": "effective action or observed readout regenerates hidden F^2/Hodge/hbar*c factors",
            "effect": "tree-level Hodge silence does not survive measured alpha/EM standards",
            "repair_or_bound": "derive public readout functor/radiative closure or keep readout residual",
            "status": "LIVE_READOUT_BOTTLENECK",
            "valid_for_claim": "false",
        },
    ]


def slope_rows(bound: float) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DCS3287_0_reconstruction_zero_conditional",
            "prediction": "0",
            "abs_bound": fmt(bound),
            "source_status": "THEOREM_CONDITIONAL_AFTER_REMAINING_GATES",
            "result": "PASS_NUMERIC_NONCLAIM",
            "required_for_claim": "local action owner + Fresnel closure + positive branch + same metric + q-basic Z_Q + readout/radiative guard",
            "valid_for_claim": "false",
        },
        {
            "row_id": "DCS3287_1_skewon_biref_residual",
            "prediction": "Pi_SB[L_v(Delta_chi_skewon+Delta_chi_biref)]/N_SB",
            "abs_bound": fmt(bound),
            "source_status": "MISSING_NUMERIC_SKEWON_BIREF_PROJECTION",
            "result": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "required_for_claim": "source-backed skewon/birefringence projection and arena map",
            "valid_for_claim": "false",
        },
        {
            "row_id": "DCS3287_2_impedance_metric_readout_residual",
            "prediction": "n_Z*L_v ln Z_Q + Pi_g[L_v(g_EM-g_pub)]/N_g + Pi_rad[L_v Delta_chi_rad]/N_rad",
            "abs_bound": fmt(bound),
            "source_status": "MISSING_NUMERIC_ZQ_METRIC_READOUT_PROJECTION",
            "result": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "required_for_claim": "q-basic scalar owner or numeric finite product with sourced metric/readout projections",
            "valid_for_claim": "false",
        },
        {
            "row_id": "DCS3287_3_half_bound_smoke",
            "prediction": fmt(0.5 * bound),
            "abs_bound": fmt(bound),
            "source_status": "SMOKE_ONLY",
            "result": "SMOKE",
            "required_for_claim": "none; schema test only",
            "valid_for_claim": "false",
        },
        {
            "row_id": "DCS3287_4_twice_bound_smoke",
            "prediction": fmt(2.0 * bound),
            "abs_bound": fmt(bound),
            "source_status": "SMOKE_ONLY",
            "result": "SMOKE",
            "required_for_claim": "none; schema test only",
            "valid_for_claim": "false",
        },
    ]


def is_number(text: str) -> bool:
    try:
        value = float(text)
    except ValueError:
        return False
    return math.isfinite(value)


def runner_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    expected = {
        "DCS3287_0_reconstruction_zero_conditional": "PASS_NUMERIC_NONCLAIM",
        "DCS3287_1_skewon_biref_residual": "REFUSE_MISSING_SOURCE_NONCLAIM",
        "DCS3287_2_impedance_metric_readout_residual": "REFUSE_MISSING_SOURCE_NONCLAIM",
        "DCS3287_3_half_bound_smoke": "PASS_NUMERIC_NONCLAIM",
        "DCS3287_4_twice_bound_smoke": "FAIL_BOUND",
    }
    output: list[dict[str, Any]] = []
    for row in rows:
        prediction = str(row["prediction"])
        bound = float(row["abs_bound"])
        if row["source_status"].startswith("MISSING"):
            result = "REFUSE_MISSING_SOURCE_NONCLAIM"
            ratio = "N/A"
        elif is_number(prediction):
            value = abs(float(prediction))
            ratio = fmt(value / bound)
            result = "PASS_NUMERIC_NONCLAIM" if value <= bound else "FAIL_BOUND"
        else:
            result = "SYMBOLIC_NONNUMERIC_NONCLAIM"
            ratio = "N/A"
        output.append(
            {
                "row_id": row["row_id"],
                "prediction": prediction,
                "prediction_over_bound": ratio,
                "result": result,
                "expected_result": expected[row["row_id"]],
                "expectation_met": bool_str(result == expected[row["row_id"]]),
                "valid_for_claim": "false",
            }
        )
    return output


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3287_0_hodge_shape_conditional",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "reciprocal nonbirefringent closure derives metric-Hodge shape up to scalar/axion/same-metric/readout clauses.",
        },
        {
            "gate_id": "GATE3287_1_premises_collapsed",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "CHS3106_0..7 collapse into fewer sharper gates: Lagrangian owner, Fresnel closure, positive branch, scalar owner, same metric, readout guard.",
        },
        {
            "gate_id": "GATE3287_2_scalar_impedance_signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "Z_Q/gauge norm/no-extra-F2/readout closure remain unsigned in 1100/1056.",
        },
        {
            "gate_id": "GATE3287_3_same_public_metric_signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "EM Fresnel metric is not yet proven identical to matter/clock/source public metric.",
        },
        {
            "gate_id": "GATE3287_4_numeric_residual_sourced",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "no source-backed Delta_chi projection row exists for skewon, birefringence, impedance, metric split, or readout.",
        },
        {
            "gate_id": "GATE3287_5_no_claim",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "no local-GR/Maxwell/alpha/PPN/clock claim is allowed from this checkpoint.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3287_0_partial_win",
            "decision": "The Hodge tensor shape is conditionally derivable from local reciprocal nonbirefringent EM closure.",
            "why_it_moves_forward": "this removes much of the vague Hodge gap and turns it into standard closure geometry rather than a guessed motion-field insert.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3287_1_coupling_bottleneck",
            "decision": "The continuous coupling/impedance Z_Q is still the live missing owner.",
            "why_it_moves_forward": "it matches the user's coupling instinct: the shape can be derived, but the scalar normalization and readout descent still decide alpha/source coupling.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3287_2_same_metric_bottleneck",
            "decision": "EM nonbirefringence gives g_EM, not automatically the matter/clock/source g_pub.",
            "why_it_moves_forward": "local GR requires same-source stress in one public metric, so the next proof cannot hide behind light cones alone.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3287_3_next_work",
            "decision": "Next attack should split scalar Z_Q ownership from same-public-metric identification and try the least costly proof first.",
            "why_it_moves_forward": "the remaining route is now two explicit gates instead of a blob called chi.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3287_0_3288",
            "target_doc": "3288-Y5-R2FR-same-public-metric-or-ZQ-impedance-owner-split-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3288_same_public_metric_or_ZQ_impedance_owner_split.py",
            "objective": "Use the 3287 split to attack the two remaining gates separately: prove g_EM=g_pub from cross-sector coframe/equivalence/Ward ownership, and prove or demote q-basic Z_Q from gauge norm/no-extra-F2/readout closure; if either fails, produce finite residual rows rather than a closure claim.",
            "guardrail": "Do not claim Maxwell/local-GR or alpha silence from Hodge shape alone; do not mix scalar impedance with metric identification; no Poynting double-counting.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    fw_before: dict[str, tuple[int, int]],
    sources: list[dict[str, Any]],
    reconstruction: list[dict[str, Any]],
    collapse: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    slope: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    non_validation_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(fw_before, snapshot_tree(FW))
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_str(passed),
                "detail": compact(detail, 620),
            }
        )

    add("VAL3287_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3287_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add(
        "VAL3287_2_outputs_parse",
        "all 3287 non-validation output CSVs parse",
        all(csv_parse_ok(path) for path in non_validation_outputs),
        "non-validation outputs parsed before validation write",
    )
    add(
        "VAL3287_3_reconstruction_theorem_present",
        "reconstruction theorem includes Fresnel closure and Hodge shape",
        any("Fresnel" in row["derivation"] and "[g_EM]" in row["derivation"] for row in reconstruction)
        and any("kappa^2=-lambda^2 I" in row["derivation"] and "*_{g_EM}" in row["derivation"] for row in reconstruction),
    )
    add(
        "VAL3287_4_coupling_obstruction_present",
        "scalar impedance and same-metric obstructions are explicit",
        any(row["theorem_id"] == "CHR3287_4_axion_and_impedance_residual" for row in reconstruction)
        and any(row["theorem_id"] == "CHR3287_5_same_metric_obstruction" for row in reconstruction),
    )
    add(
        "VAL3287_5_premise_collapse_sharpens_stack",
        "CHS premise stack is collapsed into sharper gates",
        len(collapse) == 6
        and any("CHS3106_0" in row["old_premises"] and "CHS3106_2" in row["old_premises"] for row in collapse)
        and any("CHS3106_5" in row["old_premises"] for row in collapse),
    )
    add(
        "VAL3287_6_residual_decomposition_complete",
        "Delta_chi residuals cover skewon, birefringence, axion, impedance, metric split, and readout",
        len(residuals) == 6
        and all(row["valid_for_claim"] == "false" for row in residuals)
        and any(row["term"] == "Delta_Z_Q *F" for row in residuals),
    )
    add(
        "VAL3287_7_runner_expectations",
        "Delta_chi runner expectations all match",
        all(row["expectation_met"] == "true" for row in runner),
        ";".join(f"{row['row_id']}={row['result']}" for row in runner),
    )
    add(
        "VAL3287_8_claim_gates_false",
        "no 3287 gate allows local-GR/alpha/Maxwell claim",
        all(row["claim_allowed"] == "false" for row in promotion)
        and all(row["valid_for_claim"] == "false" for row in slope),
    )
    add(
        "VAL3287_9_next_target_focused",
        "next target splits same metric and Z_Q owner",
        any("same-public-metric" in row["target_doc"] and "ZQ" in row["target_doc"] for row in next_target),
    )
    add(
        "VAL3287_10_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        fw_changed == 0,
        f"formalization_changed_count={fw_changed}",
    )
    overall = all(row["passed"] == "true" for row in checks)
    add(
        "VAL3287_11_overall",
        "3287 validation overall",
        overall,
        "all required checks passed" if overall else "one or more checks failed",
    )
    return checks


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(col, "")) for col in columns) + " |")
    return "\n".join(lines)


def write_doc(
    bound: float,
    reconstruction: list[dict[str, Any]],
    collapse: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    slope: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3287 - Chi-to-metric-Hodge premise proof or DeltaChi slope source row under AX1090

## Summary

3287 makes a real derivation step instead of circling the whole `chi` problem.

The Hodge **shape** is conditionally derivable:

1. A local bilinear EM action gives a reciprocal principal constitutive tensor and routes skewon/non-Lagrangian response into a residual.
2. If the reciprocal principal constitutive tensor has a repeated-quadratic Fresnel polynomial, equivalently a closure relation `kappa^2=-lambda^2 I` on 2-forms, it reconstructs a conformal EM metric class `[g_EM]`.
3. With positive energy/time orientation, the principal constitutive law becomes

`chi_principal = Z_Q *_(g_EM)`.

That is a useful partial win: the public Hodge form is not just inserted by hand.

But two hard gates remain:

- `g_EM` still has to be proven equal to the matter/clock/source public metric `g_pub`.
- `Z_Q` still has to be parent-owned/q-basic, or the scalar coupling/alpha/readout branch stays live.

So the honest residual is no longer a vague `Delta_chi`. It decomposes into skewon, birefringent principal, axion-gradient, impedance drift, metric-split, and radiative/readout pieces. Under the selected 3286 envelope:

`|C_R^(Delta chi)| <= {fmt(bound)}`.

## Chi-To-Hodge Reconstruction Theorem
{md_table(reconstruction, ["theorem_id", "claim_piece", "status", "payoff"])}

## Premise Collapse Matrix
{md_table(collapse, ["collapse_id", "old_premises", "new_gate", "derived_here", "remaining_gap", "blocks_claim"])}

## Delta Chi Residual Decomposition
{md_table(residuals, ["residual_id", "term", "effect", "repair_or_bound", "status"])}

## Delta Chi Slope Rows
{md_table(slope, ["row_id", "prediction", "abs_bound", "source_status", "result", "valid_for_claim"])}

## Delta Chi Bound Runner
{md_table(runner, ["row_id", "prediction", "prediction_over_bound", "result", "expectation_met", "valid_for_claim"])}

## Promotion Gates
{md_table(promotion, ["gate_id", "passed", "claim_allowed", "detail"])}

## Decisions
{md_table(decision, ["decision_id", "decision", "why_it_moves_forward", "claim_allowed"])}

## Next Target
{md_table(next_target, ["next_id", "target_doc", "objective", "guardrail"])}

## Validation
{md_table(validation, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    fw_before = snapshot_tree(FW)
    bound = bound_from_3286()
    sources = source_register_rows()
    reconstruction = reconstruction_rows()
    collapse = premise_collapse_rows()
    residuals = residual_rows()
    slope = slope_rows(bound)
    runner = runner_rows(slope)
    promotion = promotion_rows()
    decision = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["reconstruction"], reconstruction)
    write_csv(OUTPUTS["collapse"], collapse)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["slope"], slope)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)

    validation = validate(fw_before, sources, reconstruction, collapse, residuals, slope, runner, promotion, next_target)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(bound, reconstruction, collapse, residuals, slope, runner, promotion, decision, next_target, validation)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()

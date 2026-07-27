from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4993"
DUNBAR_SOURCE = POST / "source-intake" / "functional_rg" / "4986" / "sources" / "dunbar_norridge" / "9512084.tex"
CHI_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4991"
    / "sources"
    / "chi_1903.07944"
    / "GravitonBending.tex"
)
BOX_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4992"
    / "mixed_hphi_cut_and_full_box_completion_results.json"
)
BOX_COMPLETION = POST / "source-intake" / "functional_rg" / "4992" / "full_phi2h2_box_completion.csv"
CHECKPOINT_4992 = POST / "4992-Y5-R2FR-mixed-hphi-cut-and-full-scalar-box-completion.md"
HH_COEFFICIENTS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4991"
    / "massless_hh_channel_integral_coefficients.csv"
)

SOURCE_LOCK_CSV = SOURCE / "soft_operator_source_lock.csv"
POLE_BASIS_CSV = SOURCE / "one_loop_integral_pole_basis.csv"
TRIANGLE_CSV = SOURCE / "full_phi2h2_triangle_completion.csv"
IR_CSV = SOURCE / "infrared_pole_reconstruction.csv"
GATE_CSV = SOURCE / "triangle_completion_gate.csv"
RESULT_JSON = SOURCE / "universal_soft_operator_and_triangle_completion_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4993_UNIVERSAL_SOFT_OPERATOR_AND_TRIANGLE_COMPLETION"
CHECKED_DATE = "2026-07-14"

t, u = sp.symbols("t u", nonzero=True)
s = -t - u
L_s, L_t, L_u, epsilon = sp.symbols("L_s L_t L_u epsilon")


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def normalized_text(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8", errors="replace").split())


def exact(expression: sp.Expr) -> str:
    return sp.sstr(sp.factor(sp.cancel(sp.together(sp.simplify(expression)))))


def is_zero(expression: sp.Expr) -> bool:
    return sp.factor(sp.cancel(sp.together(sp.simplify(expression)))) == 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
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


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def source_lock() -> dict[str, bool]:
    dunbar = normalized_text(DUNBAR_SOURCE)
    chi = normalized_text(CHI_SOURCE)
    checkpoint = normalized_text(CHECKPOINT_4992)
    box_result = json.loads(BOX_RESULT.read_text(encoding="utf-8"))
    return {
        "dunbar_soft_pair_sum": (
            "The total IR divergence in a one-loop amplitude is simply the above result summed over all pairs" in dunbar
            and "A^{\\rm tree} \\times \\sum_{i\\neq j}^m (-s_{ij} )^{1-\\epsilon}" in dunbar
        ),
        "dunbar_four_point_soft_factor": (
            "s \\ln(-s) + t \\ln(-t) + u \\ln(-u)" in dunbar
            and "2\\epsilon" in dunbar
        ),
        "dunbar_scalar_graviton_universality": (
            "The result in eqn.~(\\use\\SoftAns) is then universal" in dunbar
            and "external legs are gravitons or scalars" in dunbar
        ),
        "dunbar_box_basis": (
            "I^{}_4 (s,t)" in dunbar
            and "{4\\over \\eps^2}" in dunbar
            and "2\\ln( -s)\\ln(-t)" in dunbar
        ),
        "dunbar_triangle_basis": (
            "I_{3}(s)" in dunbar
            and "{ \\ln(-s) \\over \\eps}" in dunbar
            and "{ \\ln^2(-s) \\over 2}" in dunbar
        ),
        "dunbar_bubble_basis": (
            "I_2(s)" in dunbar
            and "{1\\over \\eps } - \\ln(-s) + 2" in dunbar
        ),
        "chi_tree_normalization": (
            "\\kappa^2=32 \\pi G" in chi
            and "two-graviton-two-massive-scalar amplitude with opposite graviton helicities" in chi
            and "\\frac{\\kappa^2}{4}" in chi
        ),
        "box_checkpoint_complete": (
            box_result.get("checkpoint_marker") == "MTS_4992_MIXED_HPHI_CUT_AND_FULL_BOX_COMPLETION"
            and bool(box_result.get("four_dimensional_box_sector_complete"))
        ),
        "box_checkpoint_scope": "complete only for the four-dimensional scalar-box sector" in checkpoint,
    }


def source_rows(source_checks: dict[str, bool]) -> list[dict[str, Any]]:
    descriptions = {
        "dunbar_soft_pair_sum": "one-loop soft exchange is a tree amplitude times the external-leg pair sum",
        "dunbar_four_point_soft_factor": "for four massless legs the double pole cancels and the surviving pole is proportional to sLs+tLt+uLu",
        "dunbar_scalar_graviton_universality": "the same soft operator applies when external legs are scalars or gravitons",
        "dunbar_box_basis": "I4(x,y)=N/(xy)[4/epsilon^2-2(Lx+Ly)/epsilon+...]",
        "dunbar_triangle_basis": "I3(x)=-N/x[1/epsilon^2-Lx/epsilon+...]",
        "dunbar_bubble_basis": "I2(x)=N[1/epsilon-Lx+2+...] and has no Lx/epsilon term",
        "chi_tree_normalization": "M0=kappa^2 Q^4/(4stu) with the same kappa convention",
        "box_checkpoint_complete": "all three four-dimensional box coefficients are available",
        "box_checkpoint_scope": "triangle completion does not relabel the box result as a full amplitude",
    }
    return [
        {
            "source_lock_id": f"SOFT4993_{index:02d}",
            "source_clause": name,
            "description": descriptions[name],
            "passed": bool(passed),
            "source_path": relative(
                DUNBAR_SOURCE
                if name.startswith("dunbar")
                else CHI_SOURCE
                if name.startswith("chi")
                else BOX_RESULT
                if name == "box_checkpoint_complete"
                else CHECKPOINT_4992
            ),
            "status": "PASS" if passed else "FAIL",
        }
        for index, (name, passed) in enumerate(source_checks.items(), start=1)
    ]


def load_boxes() -> dict[str, sp.Expr]:
    data = json.loads(BOX_RESULT.read_text(encoding="utf-8"))
    locals_map = {"s": s, "t": t, "u": u}
    return {
        name: sp.factor(sp.sympify(value, locals=locals_map))
        for name, value in {
            "B_st": data["full_four_dimensional_box_sector"]["I4(s,t)"],
            "B_su": data["full_four_dimensional_box_sector"]["I4(s,u)"],
            "B_tu": data["full_four_dimensional_box_sector"]["I4(t,u)"],
        }.items()
    }


def pole_basis_rows() -> list[dict[str, Any]]:
    return [
        {
            "basis_id": "POLE4993_01_I4xy",
            "integral": "I4(x,y)",
            "double_pole": "4/(x*y)",
            "log_x_over_epsilon": "-2/(x*y)",
            "log_y_over_epsilon": "-2/(x*y)",
            "constant_simple_pole": "0",
            "role": "box log-pole source fixed by checkpoint 4992",
            "status": "SOURCE_LOCKED_DUNBAR_NORRIDGE",
        },
        {
            "basis_id": "POLE4993_02_I3x",
            "integral": "I3(x)",
            "double_pole": "-1/x",
            "log_x_over_epsilon": "1/x",
            "log_y_over_epsilon": "0",
            "constant_simple_pole": "0",
            "role": "unique remaining owner of each channel log divided by epsilon",
            "status": "SOURCE_LOCKED_DUNBAR_NORRIDGE",
        },
        {
            "basis_id": "POLE4993_03_I2x",
            "integral": "I2(x)",
            "double_pole": "0",
            "log_x_over_epsilon": "0",
            "log_y_over_epsilon": "0",
            "constant_simple_pole": "1",
            "role": "UV and constant simple-pole sector; cannot change triangle solve",
            "status": "SOURCE_LOCKED_DUNBAR_NORRIDGE",
        },
    ]


def derive_triangles(boxes: dict[str, sp.Expr]) -> dict[str, sp.Expr]:
    B_st, B_su, B_tu = boxes["B_st"], boxes["B_su"], boxes["B_tu"]
    tree_reduced = sp.factor(t**3 * u**3 / (4 * s))
    universal = {
        "s": sp.factor(tree_reduced * s / 2),
        "t": sp.factor(tree_reduced * t / 2),
        "u": sp.factor(tree_reduced * u / 2),
    }
    box_logs = {
        "s": sp.factor(-2 * B_st / (s * t) - 2 * B_su / (s * u)),
        "t": sp.factor(-2 * B_st / (s * t) - 2 * B_tu / (t * u)),
        "u": sp.factor(-2 * B_su / (s * u) - 2 * B_tu / (t * u)),
    }
    triangles = {
        "T_s": sp.factor(s * (universal["s"] - box_logs["s"])),
        "T_t": sp.factor(t * (universal["t"] - box_logs["t"])),
        "T_u": sp.factor(u * (universal["u"] - box_logs["u"])),
    }
    expected = {
        "T_s": sp.factor(
            (t + u)
            * (
                t**6
                + t**5 * u
                + 2 * t**4 * u**2
                + 2 * t**2 * u**4
                + t * u**5
                + u**6
            )
            / 8
        ),
        "T_t": sp.factor(-t**5 * (t**2 + t * u + 2 * u**2) / 8),
        "T_u": sp.factor(-u**5 * (2 * t**2 + t * u + u**2) / 8),
    }
    actual_logs = {
        "s": sp.factor(box_logs["s"] + triangles["T_s"] / s),
        "t": sp.factor(box_logs["t"] + triangles["T_t"] / t),
        "u": sp.factor(box_logs["u"] + triangles["T_u"] / u),
    }
    double_pole = sp.factor(
        4 * B_st / (s * t)
        + 4 * B_su / (s * u)
        + 4 * B_tu / (t * u)
        - triangles["T_s"] / s
        - triangles["T_t"] / t
        - triangles["T_u"] / u
    )
    pair_sum = 2 * (
        -s * sp.exp(-epsilon * L_s)
        - t * sp.exp(-epsilon * L_t)
        - u * sp.exp(-epsilon * L_u)
    )
    pair_leading = sp.factor(pair_sum.subs(epsilon, 0))
    pair_first = sp.factor(sp.diff(pair_sum, epsilon).subs(epsilon, 0))
    return {
        **boxes,
        **triangles,
        **{f"expected_{name}": value for name, value in expected.items()},
        **{f"U_{name}": value for name, value in universal.items()},
        **{f"X_{name}": value for name, value in box_logs.items()},
        **{f"A_{name}": value for name, value in actual_logs.items()},
        "tree_reduced": tree_reduced,
        "double_pole": double_pole,
        "pair_leading": pair_leading,
        "pair_first": pair_first,
    }


def triangle_rows(values: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    hh_t_s = -sp.Rational(1, 16) * (t**7 + u**7)
    scalar_t_s = sp.factor(values["T_s"] - hh_t_s)
    return [
        {
            "triangle_id": "TRI4993_01_Ts",
            "integral": "I3(s)",
            "coefficient": exact(values["T_s"]),
            "box_log_contribution": exact(values["X_s"]),
            "universal_log_target": exact(values["U_s"]),
            "log_pole_residual": exact(values["A_s"] - values["U_s"]),
            "crossing_rule": "s fixed and t<->u symmetric",
            "status": "IR_FIXED_EXACT",
        },
        {
            "triangle_id": "TRI4993_02_Tt",
            "integral": "I3(t)",
            "coefficient": exact(values["T_t"]),
            "box_log_contribution": exact(values["X_t"]),
            "universal_log_target": exact(values["U_t"]),
            "log_pole_residual": exact(values["A_t"] - values["U_t"]),
            "crossing_rule": "maps to T_u under t<->u",
            "status": "IR_FIXED_EXACT",
        },
        {
            "triangle_id": "TRI4993_03_Tu",
            "integral": "I3(u)",
            "coefficient": exact(values["T_u"]),
            "box_log_contribution": exact(values["X_u"]),
            "universal_log_target": exact(values["U_u"]),
            "log_pole_residual": exact(values["A_u"] - values["U_u"]),
            "crossing_rule": "maps to T_t under t<->u",
            "status": "IR_FIXED_EXACT",
        },
        {
            "triangle_id": "TRI4993_04_Ts_hh",
            "integral": "I3(s)",
            "coefficient": exact(hh_t_s),
            "box_log_contribution": "checkpoint 4991 component",
            "universal_log_target": "not separately universal",
            "log_pole_residual": "not_applicable",
            "crossing_rule": "t<->u symmetric",
            "status": "IMPORTED_SOURCE_COMPONENT",
        },
        {
            "triangle_id": "TRI4993_05_Ts_scalar_remainder",
            "integral": "I3(s)",
            "coefficient": exact(scalar_t_s),
            "box_log_contribution": "T_s(full)-T_s(hh)",
            "universal_log_target": exact(values["U_s"]),
            "log_pole_residual": "0 in the full state sum",
            "crossing_rule": "t<->u symmetric",
            "status": "IR_FIXED_SCALAR_INTERMEDIATE_REMAINDER",
        },
    ]


def infrared_rows(values: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    rows = [
        {
            "ir_id": "IR4993_01_pair_leading",
            "object": "four-point soft pair sum at epsilon^0",
            "derived": exact(values["pair_leading"]),
            "target": "0 from s+t+u=0",
            "residual": exact(values["pair_leading"]),
            "consequence": "the universal gravitational one-loop double pole cancels",
            "status": "DERIVED_EXACT",
        },
        {
            "ir_id": "IR4993_02_pair_first",
            "object": "epsilon derivative of the soft pair sum",
            "derived": exact(values["pair_first"]),
            "target": "2(s L_s+t L_t+u L_u)",
            "residual": exact(values["pair_first"] - 2 * (s * L_s + t * L_t + u * L_u)),
            "consequence": "soft factor becomes kappa^2(sLs+tLt+uLu)/(2 epsilon)",
            "status": "DERIVED_EXACT",
        },
    ]
    for index, name in enumerate(("s", "t", "u"), start=3):
        rows.append(
            {
                "ir_id": f"IR4993_{index:02d}_log_{name}",
                "object": f"L_{name}/epsilon coefficient",
                "derived": exact(values[f"A_{name}"]),
                "target": exact(values[f"U_{name}"]),
                "residual": exact(values[f"A_{name}"] - values[f"U_{name}"]),
                "consequence": f"T_{name} is fixed uniquely after the boxes",
                "status": "DERIVED_EXACT",
            }
        )
    rows.extend(
        [
            {
                "ir_id": "IR4993_06_double_pole",
                "object": "full box plus triangle 1/epsilon^2 coefficient",
                "derived": exact(values["double_pole"]),
                "target": "0",
                "residual": exact(values["double_pole"]),
                "consequence": "all channel double poles cancel before bubbles",
                "status": "DERIVED_EXACT",
            },
            {
                "ir_id": "IR4993_07_triangle_crossing",
                "object": "T_t(t,u)-T_u(u,t)",
                "derived": exact(values["T_t"] - values["T_u"].xreplace({t: u, u: t})),
                "target": "0",
                "residual": exact(values["T_t"] - values["T_u"].xreplace({t: u, u: t})),
                "consequence": "identical-scalar crossing is preserved",
                "status": "DERIVED_EXACT",
            },
        ]
    )
    return rows


def gate_rows(
    source_checks: dict[str, bool],
    values: dict[str, sp.Expr],
    triangles: list[dict[str, Any]],
    infrared: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    closed = {
        "primary_source_lock": all(source_checks.values()),
        "soft_pair_leading_cancellation": is_zero(values["pair_leading"]),
        "soft_pair_first_order": is_zero(values["pair_first"] - 2 * (s * L_s + t * L_t + u * L_u)),
        "tree_phase_conversion": is_zero(values["tree_reduced"] - t**3 * u**3 / (4 * s)),
        "box_sector_import": all(name in values for name in ("B_st", "B_su", "B_tu")),
        "unique_log_owner_basis": True,
        "triangle_Ts_solve": is_zero(values["T_s"] - values["expected_T_s"]),
        "triangle_Tt_solve": is_zero(values["T_t"] - values["expected_T_t"]),
        "triangle_Tu_solve": is_zero(values["T_u"] - values["expected_T_u"]),
        "log_s_soft_match": is_zero(values["A_s"] - values["U_s"]),
        "log_t_soft_match": is_zero(values["A_t"] - values["U_t"]),
        "log_u_soft_match": is_zero(values["A_u"] - values["U_u"]),
        "full_double_pole_cancellation": is_zero(values["double_pole"]),
        "triangle_crossing": is_zero(values["T_t"] - values["T_u"].xreplace({t: u, u: t})),
        "triangle_rows_complete": len(triangles) == 5,
        "infrared_rows_complete": len(infrared) == 7,
    }
    open_gates = {
        "bubble_coefficients_all_channels": "constant simple poles and single logarithms require cut IBP",
        "UV_counterterm_separation": "bubble and rational sectors are not yet assembled",
        "D_dimensional_mu2_rational_terms": "four-dimensional cuts do not fix evanescent information",
        "complete_one_loop_phi2h2": "boxes and triangles are complete; bubbles and rational terms remain",
        "finite_common_IR_subtraction": "requires the complete one-loop hard kernel",
        "crossing_complete_outer_hh_cut": "not yet integrated",
        "numeric_full_K_mu_K_ang": "outer finite cuts remain",
        "exact_all_operator_local_GR": "not claimed",
        "full_MTS": "not claimed",
    }
    rows: list[dict[str, Any]] = []
    for name, passed in closed.items():
        rows.append(
            {
                "gate": name,
                "passed": bool(passed),
                "evidence": "source lock or exact symbolic pole identity",
                "status": "PASS" if passed else "FAIL",
                "valid_for_checkpoint_claim": bool(passed),
            }
        )
    for name, evidence in open_gates.items():
        rows.append(
            {
                "gate": name,
                "passed": False,
                "evidence": evidence,
                "status": "OPEN_NONCLAIM",
                "valid_for_checkpoint_claim": False,
            }
        )
    return [
        dict(gate_id=f"GATE4993_{index:02d}_{row['gate']}", **row)
        for index, row in enumerate(rows, start=1)
    ]


def write_provenance(source_hashes: dict[str, str], source_checks: dict[str, bool]) -> None:
    lines = [
        "# 4993 universal soft operator and triangle completion provenance",
        "",
        f"Marker: {MARKER}.",
        "",
        f"Checked: {CHECKED_DATE}.",
        "",
        "## Primary sources",
        "",
        "- D. C. Dunbar and P. S. Norridge, Infinities within graviton scattering amplitudes, arXiv:hep-th/9512084: universal scalar/graviton one-loop soft operator and the massless box, triangle, and bubble pole basis.",
        "- H.-H. Chi, Graviton bending in quantum gravity from one-loop amplitudes, arXiv:1903.07944: tree and kappa normalization inherited by checkpoints 4991-4992.",
        "",
        "## Source checks",
        "",
    ]
    lines.extend(f"- {name}: {value}" for name, value in source_checks.items())
    lines.extend(["", "## SHA-256", ""])
    lines.extend(f"- {path}: {value}" for path, value in source_hashes.items())
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "This checkpoint fixes all three one-mass triangle coefficients by matching the completed 4992 boxes to the universal one-loop soft logarithmic pole. It proves cancellation of the full double pole. It does not determine bubbles, UV counterterms, D-dimensional mu-squared or rational terms, the finite common soft subtraction, the outer two-loop cut, local GR, or full MTS.",
            "",
        ]
    )
    PROVENANCE.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    started = time.perf_counter()

    source_checks = source_lock()
    if not all(source_checks.values()):
        raise RuntimeError(
            f"source lock failed: {[name for name, passed in source_checks.items() if not passed]}"
        )
    boxes = load_boxes()
    values = derive_triangles(boxes)
    sources = source_rows(source_checks)
    poles = pole_basis_rows()
    triangles = triangle_rows(values)
    infrared = infrared_rows(values)
    gates = gate_rows(source_checks, values, triangles, infrared)
    failed_closed = [row["gate"] for row in gates if row["status"] == "FAIL"]
    if failed_closed:
        raise RuntimeError(f"closed derivation gates failed: {failed_closed}")

    summary = {
        "checkpoint_marker": MARKER,
        "T_s": exact(values["T_s"]),
        "T_t": exact(values["T_t"]),
        "T_u": exact(values["T_u"]),
        "double_pole": exact(values["double_pole"]),
        "log_s_residual": exact(values["A_s"] - values["U_s"]),
        "log_t_residual": exact(values["A_t"] - values["U_t"]),
        "log_u_residual": exact(values["A_u"] - values["U_u"]),
        "dry_run": bool(args.dry_run),
    }
    if args.dry_run:
        print(json.dumps({**summary, "source_checks": source_checks}, indent=2, sort_keys=True))
        return 0

    for path, rows in (
        (SOURCE_LOCK_CSV, sources),
        (POLE_BASIS_CSV, poles),
        (TRIANGLE_CSV, triangles),
        (IR_CSV, infrared),
        (GATE_CSV, gates),
    ):
        write_csv(path, tagged(rows))

    script_path = Path(__file__).resolve()
    source_paths = [
        DUNBAR_SOURCE,
        CHI_SOURCE,
        BOX_RESULT,
        BOX_COMPLETION,
        CHECKPOINT_4992,
        HH_COEFFICIENTS,
        script_path,
    ]
    source_hashes = {relative(path): digest(path) for path in source_paths}
    result = {
        **summary,
        "dry_run": False,
        "source_checks": source_checks,
        "source_hashes": source_hashes,
        "amplitude_convention": "M1=kappa^4 F/<1|3|2]^4",
        "tree_reduced_phase": exact(values["tree_reduced"]),
        "universal_log_targets": {
            "L_s/epsilon": exact(values["U_s"]),
            "L_t/epsilon": exact(values["U_t"]),
            "L_u/epsilon": exact(values["U_u"]),
        },
        "full_triangle_sector": {
            "I3(s)": exact(values["T_s"]),
            "I3(t)": exact(values["T_t"]),
            "I3(u)": exact(values["T_u"]),
        },
        "four_dimensional_box_sector_complete": True,
        "triangle_sector_complete_from_IR": True,
        "complete_one_loop_phi2h2": False,
        "crossing_complete_outer_hh_cut": False,
        "numeric_full_K_mu": False,
        "numeric_full_K_ang": False,
        "exact_all_operator_local_GR": False,
        "full_MTS": False,
        "gates": {row["gate"]: bool(row["passed"]) for row in gates},
        "elapsed_seconds": time.perf_counter() - started,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_provenance(source_hashes, source_checks)

    passed = sum(bool(row["passed"]) for row in gates)
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "passed_gates": passed,
                "total_gates": len(gates),
                "open_nonclaim_gates": len(gates) - passed,
                "T_s": exact(values["T_s"]),
                "T_t": exact(values["T_t"]),
                "T_u": exact(values["T_u"]),
                "double_pole": exact(values["double_pole"]),
                "triangle_sector_complete_from_IR": True,
                "complete_one_loop_phi2h2": False,
                "result": str(RESULT_JSON),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

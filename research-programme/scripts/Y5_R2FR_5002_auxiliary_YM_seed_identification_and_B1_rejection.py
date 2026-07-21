from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FUNCTIONAL = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL / "5002"
GLUON_BASIS = (
    FUNCTIONAL
    / "4992"
    / "sources"
    / "boels_luo_1710.10208"
    / "Results"
    / "GluonsSymms.txt"
)
PAPER_SOURCE = (
    FUNCTIONAL
    / "4992"
    / "sources"
    / "boels_luo_1710.10208"
    / "LoopsFromTrees_v2.tex"
)
COMPARISON_CSV = SOURCE / "auxiliary_yang_mills_seed_comparison.csv"
GATE_CSV = SOURCE / "auxiliary_yang_mills_seed_identification_gate.csv"
RESULT_JSON = SOURCE / "auxiliary_yang_mills_seed_identification_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5002-Y5-R2FR-auxiliary-YM-seed-identification-and-B1-rejection.md"
MARKER = "MTS_5002_AUXILIARY_YM_SEED_IDENTIFICATION"


def exact(value: sp.Expr | int) -> str:
    return sp.sstr(sp.factor(sp.cancel(sp.together(sp.sympify(value)))))


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def dot(metric: sp.Matrix, left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    return sp.factor((left.T * metric * right)[0])


def mathematica_list_elements(text: str) -> list[str]:
    stripped = text.strip()
    if not stripped.startswith("{") or not stripped.endswith("}"):
        raise RuntimeError("sourced gluon basis is not a Mathematica list")
    body = stripped[1:-1]
    elements: list[str] = []
    start = 0
    round_depth = 0
    square_depth = 0
    curly_depth = 0
    for index, character in enumerate(body):
        if character == "(":
            round_depth += 1
        elif character == ")":
            round_depth -= 1
        elif character == "[":
            square_depth += 1
        elif character == "]":
            square_depth -= 1
        elif character == "{":
            curly_depth += 1
        elif character == "}":
            curly_depth -= 1
        elif character == "," and round_depth == square_depth == curly_depth == 0:
            elements.append(body[start:index].strip())
            start = index + 1
    elements.append(body[start:].strip())
    return elements


def compile_auxiliary_element(
    element: str,
    element_index: int,
) -> tuple[object, tuple[tuple[str, str, str], ...]]:
    dot_pattern = re.compile(r"ss\[\s*(p[123]|\\\[Xi\][1-4]R)\s*,\s*(p[123]|\\\[Xi\][1-4]R)\s*\]")
    dot_arguments: list[tuple[str, str, str]] = []

    def replace_dot(match: re.Match[str]) -> str:
        def normalize(token: str) -> str:
            return token if token.startswith("p") else "e" + re.search(r"[1-4]", token).group()

        left = normalize(match.group(1))
        right = normalize(match.group(2))
        name = f"d_{left}_{right}"
        dot_arguments.append((name, left, right))
        return name

    expression = dot_pattern.sub(replace_dot, element).replace("^", "**")
    expression = re.sub(r"\bs1\b", "invariant_s", expression)
    expression = re.sub(r"\bs2\b", "invariant_t", expression)
    if "ss[" in expression or re.search(r"[^A-Za-z0-9_+\-*/().\s]", expression):
        raise RuntimeError(f"unparsed token in sourced auxiliary element {element_index}")
    return compile(expression, f"GluonsSymms_element_{element_index}", "eval"), tuple(sorted(set(dot_arguments)))


def evaluate_auxiliary_element(
    compiled: tuple[object, tuple[tuple[str, str, str], ...]],
    metric: sp.Matrix,
    momenta: list[sp.Matrix],
    polarizations: list[sp.Matrix],
) -> sp.Expr:
    momentum_1, momentum_2, momentum_3, momentum_4 = momenta
    polarization_1, polarization_2, polarization_3, polarization_4 = polarizations
    vectors = {
        "p1": momentum_1,
        "p2": momentum_2,
        "p3": momentum_3,
        "p4": momentum_4,
        "e1": polarization_1,
        "e2": polarization_2,
        "e3": polarization_3,
        "e4": polarization_4,
    }
    environment: dict[str, sp.Expr] = {
        "invariant_s": dot(metric, momentum_1 + momentum_2, momentum_1 + momentum_2),
        "invariant_t": dot(metric, momentum_2 + momentum_3, momentum_2 + momentum_3),
    }
    code, dot_arguments = compiled
    for name, left, right in dot_arguments:
        environment[name] = dot(metric, vectors[left], vectors[right])
    return sp.factor(eval(code, {"__builtins__": {}}, environment))


def transverse_polarization(
    metric: sp.Matrix,
    momentum: sp.Matrix,
    trial: sp.Matrix,
    reference: sp.Matrix,
) -> sp.Matrix:
    return sp.simplify(trial - dot(metric, momentum, trial) * reference / dot(metric, momentum, reference))


def cubic_current_third_leg(
    metric: sp.Matrix,
    momentum_a: sp.Matrix,
    momentum_b: sp.Matrix,
    polarization_a: sp.Matrix,
    polarization_b: sp.Matrix,
) -> sp.Matrix:
    momentum_internal = -(momentum_a + momentum_b)
    return sp.simplify(
        dot(metric, polarization_a, polarization_b) * (momentum_a - momentum_b)
        + dot(metric, momentum_b - momentum_internal, polarization_a) * polarization_b
        + dot(metric, momentum_internal - momentum_a, polarization_b) * polarization_a
    )


def ordered_exchange_channel(
    metric: sp.Matrix,
    momentum_a: sp.Matrix,
    momentum_b: sp.Matrix,
    momentum_c: sp.Matrix,
    momentum_d: sp.Matrix,
    polarization_a: sp.Matrix,
    polarization_b: sp.Matrix,
    polarization_c: sp.Matrix,
    polarization_d: sp.Matrix,
) -> sp.Expr:
    channel_momentum = momentum_a + momentum_b
    left_current = cubic_current_third_leg(
        metric,
        momentum_a,
        momentum_b,
        polarization_a,
        polarization_b,
    )
    right_current = sp.simplify(
        dot(metric, channel_momentum - momentum_c, polarization_d) * polarization_c
        + dot(metric, polarization_c, polarization_d) * (momentum_c - momentum_d)
        + dot(metric, momentum_d - channel_momentum, polarization_c) * polarization_d
    )
    return sp.factor(dot(metric, left_current, right_current) / dot(metric, channel_momentum, channel_momentum))


def color_ordered_yang_mills_tree(
    metric: sp.Matrix,
    momenta: list[sp.Matrix],
    polarizations: list[sp.Matrix],
) -> sp.Expr:
    momentum_1, momentum_2, momentum_3, momentum_4 = momenta
    polarization_1, polarization_2, polarization_3, polarization_4 = polarizations
    exchange_s = ordered_exchange_channel(
        metric,
        momentum_1,
        momentum_2,
        momentum_3,
        momentum_4,
        polarization_1,
        polarization_2,
        polarization_3,
        polarization_4,
    )
    exchange_t = ordered_exchange_channel(
        metric,
        momentum_2,
        momentum_3,
        momentum_4,
        momentum_1,
        polarization_2,
        polarization_3,
        polarization_4,
        polarization_1,
    )
    contact = sp.factor(
        2 * dot(metric, polarization_1, polarization_3) * dot(metric, polarization_2, polarization_4)
        - dot(metric, polarization_1, polarization_2) * dot(metric, polarization_3, polarization_4)
        - dot(metric, polarization_1, polarization_4) * dot(metric, polarization_2, polarization_3)
    )
    return sp.factor(exchange_s + exchange_t + contact)


def external_kinematics(cosine: sp.Rational, sine: sp.Rational) -> tuple[sp.Matrix, list[sp.Matrix]]:
    metric = sp.diag(1, -1, -1, -1)
    momentum_1 = sp.Matrix([1, 0, 0, 1])
    momentum_2 = sp.Matrix([1, 0, 0, -1])
    momentum_3 = sp.Matrix([-1, -sine, 0, -cosine])
    momentum_4 = -(momentum_1 + momentum_2 + momentum_3)
    return metric, [momentum_1, momentum_2, momentum_3, momentum_4]


def main() -> int:
    SOURCE.mkdir(parents=True, exist_ok=True)
    elements = mathematica_list_elements(GLUON_BASIS.read_text(encoding="utf-8"))
    if len(elements) != 7:
        raise RuntimeError("unexpected sourced symmetric-gluon basis length")
    compiled_elements = [compile_auxiliary_element(elements[index], index + 1) for index in range(2)]
    angle_rows = [
        ("A1", sp.Rational(3, 5), sp.Rational(4, 5)),
        ("A2", sp.Rational(5, 13), sp.Rational(12, 13)),
    ]
    trial_sets = [
        [[2, 1, 3, 4], [1, -2, 2, 3], [3, 2, -1, 1], [2, -3, 1, -2]],
        [[1, 3, -2, 2], [2, 1, 4, -1], [-1, 2, 3, 1], [3, -1, 2, 4]],
        [[4, -1, 2, 3], [-2, 3, 1, 2], [2, 4, -3, 1], [1, 2, 4, -3]],
    ]
    comparison_rows: list[dict[str, object]] = []
    ratios: dict[int, list[sp.Expr]] = {1: [], 2: []}
    feynman_ward_residuals: list[sp.Expr] = []
    auxiliary_ward_residuals: dict[int, list[sp.Expr]] = {1: [], 2: []}

    for angle_id, cosine, sine in angle_rows:
        metric, momenta = external_kinematics(cosine, sine)
        invariant_s = dot(metric, momenta[0] + momenta[1], momenta[0] + momenta[1])
        invariant_t = dot(metric, momenta[1] + momenta[2], momenta[1] + momenta[2])
        references = [momenta[1], momenta[0], momenta[0], momenta[1]]
        for trial_index, trials in enumerate(trial_sets, start=1):
            polarizations = [
                transverse_polarization(metric, momentum, sp.Matrix(trial), reference)
                for momentum, trial, reference in zip(momenta, trials, references)
            ]
            amplitude = color_ordered_yang_mills_tree(metric, momenta, polarizations)
            if amplitude == 0:
                raise RuntimeError("comparison sample has zero Yang-Mills tree")
            auxiliary_values = [
                evaluate_auxiliary_element(compiled, metric, momenta, polarizations)
                for compiled in compiled_elements
            ]
            for element_index, value in enumerate(auxiliary_values, start=1):
                ratio = sp.factor(value / (invariant_s * invariant_t * amplitude))
                ratios[element_index].append(ratio)
                comparison_rows.append(
                    {
                        "sample_id": f"{angle_id}_P{trial_index}_E{element_index}",
                        "angle_cosine": exact(cosine),
                        "angle_sine": exact(sine),
                        "polarization_set": trial_index,
                        "auxiliary_element": element_index,
                        "s": exact(invariant_s),
                        "t": exact(invariant_t),
                        "A_YM": exact(amplitude),
                        "auxiliary_value": exact(value),
                        "auxiliary_over_st_A_YM": exact(ratio),
                        "matches_single_constant": "pending",
                    }
                )
            for leg_index in range(4):
                ward_polarizations = list(polarizations)
                ward_polarizations[leg_index] = momenta[leg_index]
                feynman_ward_residuals.append(
                    sp.factor(color_ordered_yang_mills_tree(metric, momenta, ward_polarizations))
                )
                for element_index, compiled in enumerate(compiled_elements, start=1):
                    auxiliary_ward_residuals[element_index].append(
                        sp.factor(evaluate_auxiliary_element(compiled, metric, momenta, ward_polarizations))
                    )

    unique_ratios = {index: sorted({exact(value) for value in values}) for index, values in ratios.items()}
    selected_elements = [index for index, values in unique_ratios.items() if len(values) == 1]
    selected_element = selected_elements[0] if selected_elements == [2] else None
    selected_ratio = unique_ratios[2][0] if selected_element == 2 else "UNRESOLVED"
    for row in comparison_rows:
        row["matches_single_constant"] = str(
            row["auxiliary_element"] == selected_element
            and row["auxiliary_over_st_A_YM"] == selected_ratio
        )

    gate_rows = [
        {
            "gate_id": "G5002_1_source_files_exist",
            "passed": str(GLUON_BASIS.exists() and PAPER_SOURCE.exists()),
            "detail": f"{relative(GLUON_BASIS)}; {relative(PAPER_SOURCE)}",
        },
        {
            "gate_id": "G5002_2_feynman_tree_Ward_identity",
            "passed": str(all(residual == 0 for residual in feynman_ward_residuals)),
            "detail": f"{len(feynman_ward_residuals)} exact leg-replacement checks",
        },
        {
            "gate_id": "G5002_3_auxiliary_elements_gauge_invariant",
            "passed": str(
                all(residual == 0 for residuals in auxiliary_ward_residuals.values() for residual in residuals)
            ),
            "detail": "both candidates satisfy their own Ward identities",
        },
        {
            "gate_id": "G5002_4_element_2_constant_match",
            "passed": str(unique_ratios[2] == ["8"]),
            "detail": f"unique ratios={unique_ratios[2]}",
        },
        {
            "gate_id": "G5002_5_element_1_rejected",
            "passed": str(len(unique_ratios[1]) > 1),
            "detail": f"nonconstant ratios={unique_ratios[1]}",
        },
        {
            "gate_id": "G5002_6_unique_physical_seed",
            "passed": str(selected_element == 2),
            "detail": f"selected auxiliary element={selected_element}",
        },
    ]
    all_gates_pass = all(row["passed"] == "True" for row in gate_rows)
    if not all_gates_pass:
        raise RuntimeError("auxiliary Yang-Mills seed identification gate failed")

    write_csv(COMPARISON_CSV, comparison_rows)
    write_csv(GATE_CSV, gate_rows)
    result = {
        "checkpoint_marker": MARKER,
        "status": "PHYSICAL_YANG_MILLS_SEED_IDENTIFIED",
        "selected_auxiliary_element": selected_element,
        "identity": "GluonsSymms_element_2 = 8*s*t*A_YM",
        "rejected_candidate": "GluonsSymms_element_1",
        "rejection_reason": "gauge invariant but not proportional to s*t*A_YM for generic transverse polarizations",
        "element_unique_ratios": unique_ratios,
        "sample_count": len(angle_rows) * len(trial_sets),
        "ward_check_count": len(feynman_ward_residuals),
        "source_files": [relative(GLUON_BASIS), relative(PAPER_SOURCE)],
        "comparison_csv": relative(COMPARISON_CSV),
        "gate_csv": relative(GATE_CSV),
        "all_gates_pass": all_gates_pass,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PROVENANCE.write_text(
        "# 5002 provenance\n\n"
        f"- Auxiliary basis: `{relative(GLUON_BASIS)}`.\n"
        f"- Paper source: `{relative(PAPER_SOURCE)}`.\n"
        "- Independent comparator: color-ordered four-gluon tree reconstructed from both cubic exchange channels and the quartic contact vertex.\n"
        "- Conventions were fixed internally by exact four-leg Ward identities before any auxiliary comparison.\n"
        "- Two rational scattering angles and three independent transverse-polarization sets were evaluated exactly.\n"
        "- The second auxiliary list element equals `8*s*t*A_YM` in every sample; the first has sample-dependent ratios and is rejected for this cut.\n",
        encoding="utf-8",
    )
    DOCUMENT.write_text(
        "# 5002 — Auxiliary Yang–Mills seed identification and B1 rejection\n\n"
        "## Result\n\n"
        "The physical minimal Yang–Mills seed in the checked `GluonsSymms.txt` auxiliary ordering is its **second** list element, not its first:\n\n"
        "```text\nGluonsSymms element 2 = 8 s t A_YM(1,2,3,4).\n```\n\n"
        "This identity was established by an independent color-ordered Feynman-rule reconstruction, not by trusting the basis label. Both cubic channels and the quartic vertex were included, and all four exact Ward replacements vanish. Across six generic transverse samples, element 2 has the constant ratio `8`; element 1 has varying ratios and is therefore a different gauge-invariant tensor.\n\n"
        "## Consequence\n\n"
        "The element-1 `hh` branch generated during 5000–5001 is a useful diagnostic but is not the minimal Einstein/Yang–Mills shared cut. It must not supersede the independently closed 4998 boxes. Those outputs are quarantined before the physical element-2 reconstruction is rerun.\n\n"
        "## Source-label caution\n\n"
        "The paper narrative names a minimal tensor `B_1 = s t A_YM`, but this does not license identifying it with the first raw auxiliary-list position. The executable identity above fixes the auxiliary ordering and normalization directly.\n\n"
        "## Claim boundary\n\n"
        "This checkpoint corrects an internal cut seed. It does not by itself close the remaining generic-dimensional evanescent coefficient or the outer MTS kernel.\n\n"
        f"- Comparison: `{relative(COMPARISON_CSV)}`\n"
        f"- Gates: `{relative(GATE_CSV)}`\n"
        f"- Result: `{relative(RESULT_JSON)}`\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

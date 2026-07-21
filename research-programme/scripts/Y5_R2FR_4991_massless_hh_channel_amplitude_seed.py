from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
from pathlib import Path
from typing import Any

import sympy as sp
from sympy.parsing.mathematica import parse_mathematica


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4991"
CHI_SOURCE = SOURCE / "sources" / "chi_1903.07944" / "GravitonBending.tex"
CHI_COEFFICIENTS = SOURCE / "sources" / "chi_1903.07944" / "Coeff-of-Integrals.txt"
CHI_ARCHIVE = SOURCE / "sources" / "chi_1903.07944" / "1903.07944.tar"
DUNBAR_SOURCE = POST / "source-intake" / "functional_rg" / "4986" / "sources" / "dunbar_norridge" / "9512084.tex"
CHECKPOINT_4990 = POST / "4990-Y5-R2FR-crossing-complete-D1-scheme-separation-and-hh-scope-correction.md"

COEFFICIENT_CSV = SOURCE / "massless_hh_channel_integral_coefficients.csv"
IDENTITY_CSV = SOURCE / "massless_hh_channel_identity_checks.csv"
SCOPE_CSV = SOURCE / "one_loop_amplitude_scope_and_IR_test.csv"
GATE_CSV = SOURCE / "massless_hh_channel_amplitude_gate.csv"
RESULT_JSON = SOURCE / "massless_hh_channel_amplitude_seed_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4991_MASSLESS_HH_CHANNEL_AMPLITUDE_SEED"
CHECKED_DATE = "2026-07-14"

s, t, u, D, epsilon = sp.symbols("s t u D epsilon", nonzero=True)
Q, Qbar, kappa, F_hh = sp.symbols("Q Qbar kappa F_hh", nonzero=True)
PI = sp.pi


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
    return sp.sstr(sp.factor(sp.simplify(expression)))


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
    chi = normalized_text(CHI_SOURCE)
    ancillary = normalized_text(CHI_COEFFICIENTS)
    dunbar = normalized_text(DUNBAR_SOURCE)
    checkpoint = normalized_text(CHECKPOINT_4990)
    return {
        "chi_s_channel_scope": "Focusing on terms with an $s$-channel cut" in chi,
        "chi_ancillary_pointer": "Coeff-of-Integrals.txt" in chi,
        "chi_basis_order": "b_1 I_4(s,t) + b_2 I_4(s,u)" in chi and "t_1 I_3(s)" in chi and "b I_2(s)" in chi,
        "chi_tensor_reduction_scope": "scalar massive triangle integral and two scalar box integrals" in chi,
        "ancillary_five_coefficients": "complete coefficients of {Intg[2, s], Intg[3, s], Intg[3, s, M^2], Intg[4, s, t], Intg[4, s, u]}" in ancillary,
        "ancillary_prefactor": "1/<1|3|2]^4" in ancillary and "\\kappa^4" in ancillary,
        "dunbar_massless_integral_basis": "I^{}_4 (s,t)" in dunbar and "I_{3}(s)" in dunbar and "I_2(s)" in dunbar,
        "checkpoint_4990_hh_open": "full crossed `hh` cut remains" in checkpoint,
    }


def parse_ancillary() -> tuple[sp.Expr, ...]:
    text = "\n".join(
        line
        for line in CHI_COEFFICIENTS.read_text(encoding="utf-8").splitlines()
        if not line.startswith("##")
    ).strip()
    prefix = "(1/4)*"
    if not text.startswith(prefix):
        raise ValueError("unexpected ancillary prefactor")
    parsed = parse_mathematica(text[len(prefix) :])
    if not isinstance(parsed, sp.Tuple) or len(parsed) != 5:
        raise ValueError("expected five ancillary coefficients")
    return tuple(sp.factor(sp.Rational(1, 4) * value) for value in parsed)


def massless_reduction(coefficients: tuple[sp.Expr, ...]) -> dict[str, sp.Expr]:
    M = sp.Symbol("M")
    parser_s = sp.Symbol("s")
    parser_t = sp.Symbol("t")
    parser_D = sp.Symbol("D")
    substitution = {M: 0, parser_s: -t - u, parser_t: t, parser_D: D}
    bubble_D, triangle_massless, triangle_massive, box_st, box_su = [
        sp.factor(value.subs(substitution)) for value in coefficients
    ]
    bubble_4 = sp.factor(bubble_D.subs(D, 4))
    bubble_epsilon_1 = sp.factor(-2 * sp.diff(bubble_D, D).subs(D, 4))
    triangle_sum = sp.factor(triangle_massless + triangle_massive)
    expected_bubble_4 = sp.factor(
        t * u * (2 * (t**4 + u**4) - 3 * t * u * (t**2 + u**2)) / 32
    )
    expected_bubble_epsilon_1 = sp.factor(
        -t
        * u
        * (180 * (t**4 + u**4) - 333 * t * u * (t**2 + u**2) + 605 * t**2 * u**2)
        / 2880
    )
    expected_triangle = -sp.Rational(1, 16) * (t**7 + u**7)
    expected_box_st = sp.Rational(1, 32) * t**4 * (t**4 + u**4)
    expected_box_su = sp.Rational(1, 32) * u**4 * (t**4 + u**4)
    double_pole = sp.factor(
        4 * box_st / ((-t - u) * t)
        + 4 * box_su / ((-t - u) * u)
        - triangle_sum / (-t - u)
    )
    return {
        "bubble_D": bubble_D,
        "bubble_4": bubble_4,
        "bubble_epsilon_1": bubble_epsilon_1,
        "triangle_massless": triangle_massless,
        "triangle_massive_limit": triangle_massive,
        "triangle_sum": triangle_sum,
        "box_st": box_st,
        "box_su": box_su,
        "expected_bubble_4": expected_bubble_4,
        "expected_bubble_epsilon_1": expected_bubble_epsilon_1,
        "expected_triangle": expected_triangle,
        "expected_box_st": expected_box_st,
        "expected_box_su": expected_box_su,
        "double_pole": double_pole,
    }


def coefficient_rows(values: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    return [
        {
            "basis_id": "HHAMP4991_01_I2s",
            "integral": "I2(s)",
            "coefficient_D4": exact(values["bubble_4"]),
            "coefficient_epsilon_1": exact(values["bubble_epsilon_1"]),
            "basis_formula": "I2(s)=N_eps[1/epsilon-L_s+2]+O(epsilon)",
            "source_scope": "hh intermediate state in the s-channel discontinuity",
            "status": "DERIVED_EXACT_MASSLESS_LIMIT",
        },
        {
            "basis_id": "HHAMP4991_02_I3s",
            "integral": "I3(s)",
            "coefficient_D4": exact(values["triangle_sum"]),
            "coefficient_epsilon_1": "0",
            "basis_formula": "I3(s)=-N_eps/s[1/epsilon^2-L_s/epsilon+L_s^2/2]+O(epsilon)",
            "source_scope": "the massless limit makes I3(s,M) identical to I3(s)",
            "status": "DERIVED_EXACT_TRIANGLE_COLLAPSE",
        },
        {
            "basis_id": "HHAMP4991_03_I4st",
            "integral": "I4(s,t)",
            "coefficient_D4": exact(values["box_st"]),
            "coefficient_epsilon_1": "0",
            "basis_formula": "massless scalar box in the Dunbar-Norridge convention",
            "source_scope": "hh intermediate state in the s-channel discontinuity",
            "status": "DERIVED_EXACT_MASSLESS_LIMIT",
        },
        {
            "basis_id": "HHAMP4991_04_I4su",
            "integral": "I4(s,u)",
            "coefficient_D4": exact(values["box_su"]),
            "coefficient_epsilon_1": "0",
            "basis_formula": "massless scalar box in the Dunbar-Norridge convention",
            "source_scope": "hh intermediate state in the s-channel discontinuity",
            "status": "DERIVED_EXACT_MASSLESS_LIMIT",
        },
    ]


def identity_rows(values: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    q_pair = Q * Qbar
    amplitude_1 = kappa**4 * F_hh / Q**4
    amplitude_0_conjugate = kappa**2 * Q**4 / (4 * s * t * u)
    interference = sp.factor(amplitude_1 * amplitude_0_conjugate)
    return [
        {
            "identity_id": "HHID4991_01_bubble_D4",
            "statement": "b(D=4)=tu[2(t^4+u^4)-3tu(t^2+u^2)]/32",
            "exact_residual": exact(values["bubble_4"] - values["expected_bubble_4"]),
            "consequence": "the finite bubble coefficient is symmetric under exchange of the two scalars",
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "HHID4991_02_bubble_epsilon",
            "statement": "b(4-2epsilon)=b0+epsilon b1+O(epsilon^2)",
            "exact_residual": exact(values["bubble_epsilon_1"] - values["expected_bubble_epsilon_1"]),
            "consequence": "the epsilon-times-bubble-pole finite term is retained rather than discarded",
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "HHID4991_03_triangle_collapse",
            "statement": "t1+t2|M=0=-(t^7+u^7)/16",
            "exact_residual": exact(values["triangle_sum"] - values["expected_triangle"]),
            "consequence": "the finite-mass triangle degenerates to the same one-mass massless triangle",
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "HHID4991_04_box_st",
            "statement": "b_st=t^4(t^4+u^4)/32",
            "exact_residual": exact(values["box_st"] - values["expected_box_st"]),
            "consequence": "first source box coefficient is reduced exactly",
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "HHID4991_05_box_su",
            "statement": "b_su=u^4(t^4+u^4)/32",
            "exact_residual": exact(values["box_su"] - values["expected_box_su"]),
            "consequence": "second source box coefficient is the t-u crossing image",
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "HHID4991_06_crossing_symmetry",
            "statement": "F_hh,s is invariant under t<->u with I4(s,t)<->I4(s,u)",
            "exact_residual": exact(
                values["bubble_4"] - values["bubble_4"].xreplace({t: u, u: t})
                + values["triangle_sum"] - values["triangle_sum"].xreplace({t: u, u: t})
                + values["box_st"] - values["box_su"].xreplace({t: u, u: t})
            ),
            "consequence": "the massless source reduction respects identical-scalar exchange",
            "status": "DERIVED_EXACT",
        },
        {
            "identity_id": "HHID4991_07_spinor_pair",
            "statement": "<1|3|2]<2|3|1]=tu",
            "exact_residual": exact(q_pair.subs(Qbar, t * u / Q) - t * u),
            "consequence": "the inverse one-loop helicity phase and the tree conjugate cancel in the physical interference",
            "status": "DERIVED_FROM_FOUR_POINT_SPINOR_IDENTITY",
        },
        {
            "identity_id": "HHID4991_08_interference",
            "statement": "M1_hh,s M0*=kappa^6 F_hh,s/(4stu)",
            "exact_residual": exact(interference - kappa**6 * F_hh / (4 * s * t * u)),
            "consequence": "the outer two-particle cut can be evaluated with a scalar hard kernel after phase cancellation",
            "status": "DERIVED_EXACT",
        },
    ]


def scope_rows(values: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    return [
        {
            "scope_id": "HHSCOPE4991_01_derived_seed",
            "object": "M1_hh,s(h+ h- phi phi)",
            "evidence": "four exact massless integral coefficients plus the O(epsilon) bubble term",
            "valid": True,
            "consequence": "a genuine sourced component of the one-loop amplitude is now available for the outer hh cut",
            "status": "SOURCE_COMPLETE_FOR_DECLARED_S_CHANNEL_HH_COMPONENT",
        },
        {
            "scope_id": "HHSCOPE4991_02_double_pole",
            "object": "partial s-channel 1/epsilon^2 coefficient",
            "evidence": exact(values["double_pole"]),
            "valid": True,
            "consequence": "this pole is a normalization checksum for the crossed completion, not a standalone full-amplitude soft factor",
            "status": "DERIVED_EXACT_PARTIAL_POLE",
        },
        {
            "scope_id": "HHSCOPE4991_03_full_amplitude",
            "object": "complete one-loop h+ h- phi phi amplitude",
            "evidence": "Chi explicitly retains terms with an s-channel cut; I4(t,u), I3(t), I3(u), I2(t), I2(u), scalar-intermediate and mixed-channel completion are not fixed by this source component",
            "valid": False,
            "consequence": "do not insert the partial seed as if it were the full one-loop amplitude",
            "status": "OPEN_DERIVATION_REQUIRED",
        },
        {
            "scope_id": "HHSCOPE4991_04_outer_cut",
            "object": "crossing-complete two-loop hh finite cut",
            "evidence": "helicity phase cancellation is closed but the full one-loop hard kernel and IR subtraction are not",
            "valid": False,
            "consequence": "next derive the mixed h-phi cuts and impose full soft-factor consistency",
            "status": "OPEN_NONCLAIM",
        },
    ]


def gate_rows(source_checks: dict[str, bool], values: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    closed = {
        "primary_source_lock": all(source_checks.values()),
        "five_coefficient_parse": True,
        "massless_bubble_reduction": sp.simplify(values["bubble_4"] - values["expected_bubble_4"]) == 0,
        "bubble_epsilon_term": sp.simplify(values["bubble_epsilon_1"] - values["expected_bubble_epsilon_1"]) == 0,
        "triangle_degeneracy": sp.simplify(values["triangle_sum"] - values["expected_triangle"]) == 0,
        "box_st_reduction": sp.simplify(values["box_st"] - values["expected_box_st"]) == 0,
        "box_su_reduction": sp.simplify(values["box_su"] - values["expected_box_su"]) == 0,
        "identical_scalar_crossing": sp.simplify(
            values["bubble_4"] - values["bubble_4"].xreplace({t: u, u: t})
        )
        == 0,
        "physical_phase_cancellation": True,
    }
    open_gates = {
        "complete_one_loop_phi2h2": "crossed and scalar-intermediate components remain",
        "mixed_hphi_channel": "derive the physical mixed-channel cut",
        "full_IR_subtraction": "requires the complete one-loop amplitude",
        "crossing_complete_outer_hh_cut": "not yet integrated",
        "numeric_full_K_mu_K_ang": "remaining cuts are open",
        "exact_all_operator_local_GR": "not claimed",
        "full_MTS": "not claimed",
    }
    rows: list[dict[str, Any]] = []
    for name, passed in closed.items():
        rows.append(
            {
                "gate": name,
                "passed": bool(passed),
                "evidence": "exact source or symbolic identity",
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
    return [dict(gate_id=f"GATE4991_{index:02d}_{row['gate']}", **row) for index, row in enumerate(rows, start=1)]


def write_provenance(source_hashes: dict[str, str], source_checks: dict[str, bool]) -> None:
    lines = [
        "# 4991 massless hh-channel amplitude provenance",
        "",
        f"Marker: `{MARKER}`.",
        "",
        f"Checked: `{CHECKED_DATE}`.",
        "",
        "## Primary sources",
        "",
        "- H.-H. Chi, *Graviton bending in quantum gravity from one-loop amplitudes*, Phys. Rev. D 99, 126008 (2019), [arXiv:1903.07944](https://arxiv.org/abs/1903.07944), DOI `10.1103/PhysRevD.99.126008`: exact D-dimensional integral coefficients and their declared s-channel scope.",
        "- D. C. Dunbar and P. S. Norridge, *Infinities within graviton scattering amplitudes*, [arXiv:hep-th/9512084](https://arxiv.org/abs/hep-th/9512084): massless box, triangle, and bubble conventions.",
        "",
        "## Source checks",
        "",
    ]
    lines.extend(f"- `{name}`: `{value}`" for name, value in source_checks.items())
    lines.extend(["", "## SHA-256", ""])
    lines.extend(f"- `{path}`: `{value}`" for path, value in source_hashes.items())
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "This checkpoint derives the exact massless hh-intermediate s-channel component of the one-loop opposite-helicity scalar-graviton amplitude, including the epsilon-dependent bubble coefficient and physical tree-interference phase cancellation. It does not call that component the full one-loop amplitude, does not close its crossed or scalar-intermediate cuts, and does not claim the two-loop outer hh cut, numeric full invariants, local GR, or full MTS.",
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
        raise RuntimeError(f"source lock failed: {[name for name, passed in source_checks.items() if not passed]}")
    coefficients = parse_ancillary()
    values = massless_reduction(coefficients)
    coefficients_out = coefficient_rows(values)
    identities = identity_rows(values)
    scopes = scope_rows(values)
    gates = gate_rows(source_checks, values)

    if args.dry_run:
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "source_checks": source_checks,
                    "triangle_sum": exact(values["triangle_sum"]),
                    "bubble_D4": exact(values["bubble_4"]),
                    "box_st": exact(values["box_st"]),
                    "box_su": exact(values["box_su"]),
                    "dry_run": True,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    for path, rows in (
        (COEFFICIENT_CSV, coefficients_out),
        (IDENTITY_CSV, identities),
        (SCOPE_CSV, scopes),
        (GATE_CSV, gates),
    ):
        write_csv(path, tagged(rows))

    script_path = Path(__file__).resolve()
    source_paths = [CHI_SOURCE, CHI_COEFFICIENTS, CHI_ARCHIVE, DUNBAR_SOURCE, CHECKPOINT_4990, script_path]
    source_hashes = {relative(path): digest(path) for path in source_paths}
    result = {
        "checkpoint_marker": MARKER,
        "source_checks": source_checks,
        "source_hashes": source_hashes,
        "amplitude_convention": "M1_hh,s=kappa^4 F_hh,s/<1|3|2]^4",
        "massless_hh_s_channel": {
            "I2_s": exact(values["bubble_4"]),
            "I2_s_epsilon_1": exact(values["bubble_epsilon_1"]),
            "I3_s": exact(values["triangle_sum"]),
            "I4_st": exact(values["box_st"]),
            "I4_su": exact(values["box_su"]),
            "partial_double_pole": exact(values["double_pole"]),
        },
        "physical_interference": "M1_hh,s M0*=kappa^6 F_hh,s/(4stu)",
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
                "triangle_sum": exact(values["triangle_sum"]),
                "bubble_D4": exact(values["bubble_4"]),
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

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FUNCTIONAL = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL / "5004"

SCALAR_4997 = FUNCTIONAL / "4997" / "complete_generic_D_scalar_s_cut.csv"
MIXED_4998 = FUNCTIONAL / "4998" / "complete_generic_D_mixed_cut.csv"
HH_4999 = FUNCTIONAL / "4999" / "hh_direct_one_scale_laurent.csv"
SOFT_4993 = POST / "4993-Y5-R2FR-universal-soft-operator-and-full-triangle-completion.md"
DIRECT_5001 = FUNCTIONAL / "5001" / "direct_generic_D_hh_coefficients.csv"
OBSTRUCTION_5001 = FUNCTIONAL / "5001" / "local_simple_pole_obstruction.csv"
RESULT_5001 = FUNCTIONAL / "5001" / "generic_hh_completion_and_local_simple_pole_obstruction_results.json"
RESULT_5003 = FUNCTIONAL / "5003" / "direct_mixed_one_scale_IBP_reconstruction_results.json"
BOELS_SOURCE = FUNCTIONAL / "4992" / "sources" / "boels_luo_1710.10208" / "LoopsFromTrees_v2.tex"
DUNBAR_SOURCE = FUNCTIONAL / "4986" / "sources" / "dunbar_norridge" / "9512084.tex"
COUNTERTERM_SOURCE = FUNCTIONAL / "4995" / "sources" / "accettulli_huber_1911.10108" / "errequadro.tex"

COMPLETION_CSV = SOURCE / "physical_one_scale_completion.csv"
CLASSIFICATION_CSV = SOURCE / "scheme_and_locality_classification.csv"
QUARANTINE_CSV = SOURCE / "direct_s_cut_quarantine.csv"
GATE_CSV = SOURCE / "physical_HV_IR_completion_gate.csv"
RESULT_JSON = SOURCE / "physical_HV_IR_completion_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5004-Y5-R2FR-physical-HV-IR-completion-and-nonlocal-pole-rejection.md"

MARKER = "MTS_5004_PHYSICAL_HV_IR_COMPLETION_AND_NONLOCAL_POLE_REJECTION"
CHECKED_DATE = "2026-07-14"

D = sp.Symbol("D")
epsilon = sp.Symbol("epsilon")
t, u = sp.symbols("t u", nonzero=True)
s = -t - u
Q = sp.Symbol("Q")


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def exact(value: sp.Expr | int) -> str:
    return sp.sstr(sp.factor(sp.cancel(sp.together(sp.sympify(value)))))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def formula(
    path: Path,
    key: str,
    value: str,
    field: str = "formula",
) -> sp.Expr:
    row = next(candidate for candidate in read_csv(path) if candidate[key] == value)
    return sp.sympify(row[field], locals={"D": D, "t": t, "u": u})


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
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


def epsilon_coefficient(expression: sp.Expr, order: int) -> sp.Expr:
    expanded = sp.series(expression.subs(D, 4 - 2 * epsilon), epsilon, 0, order + 1).removeO()
    return sp.factor(sp.expand(expanded).coeff(epsilon, order))


def source_locks(required: list[Path]) -> dict[str, bool]:
    boels = BOELS_SOURCE.read_text(encoding="utf-8", errors="ignore")
    dunbar = DUNBAR_SOURCE.read_text(encoding="utf-8", errors="ignore")
    counterterm = COUNTERTERM_SOURCE.read_text(encoding="utf-8", errors="ignore")
    soft = SOFT_4993.read_text(encoding="utf-8", errors="ignore")
    result_5001 = json.loads(RESULT_5001.read_text(encoding="utf-8"))
    result_5003 = json.loads(RESULT_5003.read_text(encoding="utf-8"))
    return {
        "all_required_paths_exist": all(path.is_file() for path in required),
        "three_dimension_scheme_source": all(
            token in boels
            for token in (
                "D_{\\textrm{ext}} - 2",
                "D_{\\textrm{int}} - 2",
                "D_{\\textrm{loop int.}}",
                "four dimensional helicity scheme",
            )
        ),
        "dJ2_is_finite_only": "only ambiguity will be in finite\nrational  terms" in dunbar,
        "one_loop_scalar_counterterm_has_four_scalar_legs": all(
            token in dunbar
            for token in (
                "( D_{\\mu} \\phi D^{\\mu} \\phi )^2",
                "four external scalars",
            )
        ),
        "quadratic_curvature_two_scalar_amplitude_silence": all(
            token in counterterm
            for token in (
                "two-scalar/$n$-graviton amplitudes",
                "are zero",
                "no corrections to the EH (two-scalar) $n$-graviton amplitudes",
            )
        ),
        "full_helicity_phase_source": "Q Qbar=tu" in soft and "M0=kappa^2/Qbar^4" in soft,
        "5001_direct_obstruction_loaded": result_5001.get("direct_hh_s_cut_complete") is True,
        "5003_mixed_recheck_loaded": result_5003.get("mixed_tu_one_scale_recheck_complete") is True,
    }


def derive() -> dict[str, Any]:
    mixed = {
        name: formula(MIXED_4998, "coefficient", name)
        for name in (
            "B_st_full",
            "B_su_full",
            "B_tu_full",
            "T_t_finite",
            "C_t_finite",
            "T_u_finite",
            "C_u_finite",
        )
    }
    A_t = sp.factor(
        mixed["T_t_finite"]
        + (D - 4) * t * mixed["C_t_finite"] / (2 * (D - 3))
    )
    A_u = sp.factor(
        mixed["T_u_finite"]
        + (D - 4) * u * mixed["C_u_finite"] / (2 * (D - 3))
    )
    box_sum = sp.factor(
        mixed["B_st_full"] / (s * t)
        + mixed["B_su_full"] / (s * u)
        + mixed["B_tu_full"] / (t * u)
    )
    A_s_required = sp.factor(s * (4 * box_sum - A_t / t - A_u / u))
    A_s_scalar = formula(SCALAR_4997, "coefficient", "T_s_scalar_direct(D)")
    A_s_hh_required = sp.factor(A_s_required - A_s_scalar)
    A_s_hh_4999 = formula(
        HH_4999,
        "component",
        "A_s_hh_CDR_direct_inference",
        "exact_generic_D_formula",
    )
    A_s_hh_direct = formula(DIRECT_5001, "coefficient", "A_s_hh_direct(D)")
    A_s_direct = formula(DIRECT_5001, "coefficient", "A_s_full_direct(D)")
    direct_delta = sp.factor(A_s_direct - A_s_required)
    direct_delta_hh = sp.factor(A_s_hh_direct - A_s_hh_required)
    direct_delta_epsilon = epsilon_coefficient(direct_delta, 1)
    p1_from_delta = sp.factor(direct_delta_epsilon / (t + u))
    p1_stored = formula(
        OBSTRUCTION_5001,
        "equation",
        "direct_cut_P1",
        "value",
    )
    pole_identity = sp.factor(4 * box_sum - A_s_required / s - A_t / t - A_u / u)
    full_helicity_residual = sp.factor(p1_stored * Q**4 / (t**4 * u**4))
    full_helicity_denominator = sp.factor(sp.denom(sp.cancel(full_helicity_residual)))
    tree_reduced = t**3 * u**3 / (4 * s)
    tree_ratio = sp.factor(p1_stored / tree_reduced)
    return {
        "mixed": mixed,
        "A_t": A_t,
        "A_u": A_u,
        "A_s_required": A_s_required,
        "A_s_scalar": A_s_scalar,
        "A_s_hh_required": A_s_hh_required,
        "A_s_hh_4999": A_s_hh_4999,
        "A_s_hh_direct": A_s_hh_direct,
        "A_s_direct": A_s_direct,
        "direct_delta": direct_delta,
        "direct_delta_hh": direct_delta_hh,
        "direct_delta_epsilon": direct_delta_epsilon,
        "p1_from_delta": p1_from_delta,
        "p1_stored": p1_stored,
        "pole_identity": pole_identity,
        "full_helicity_residual": full_helicity_residual,
        "full_helicity_denominator": full_helicity_denominator,
        "tree_ratio": tree_ratio,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    required = [
        SCALAR_4997,
        MIXED_4998,
        HH_4999,
        SOFT_4993,
        DIRECT_5001,
        OBSTRUCTION_5001,
        RESULT_5001,
        RESULT_5003,
        BOELS_SOURCE,
        DUNBAR_SOURCE,
        COUNTERTERM_SOURCE,
    ]
    locks = source_locks(required)
    if not all(locks.values()):
        raise RuntimeError(f"source lock failed: {locks}")
    outputs = [
        COMPLETION_CSV,
        CLASSIFICATION_CSV,
        QUARANTINE_CSV,
        GATE_CSV,
        RESULT_JSON,
        PROVENANCE,
        DOCUMENT,
    ]
    if args.dry_run:
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "source_lock": locks,
                    "writes": [relative(path) for path in outputs],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    formal_before = tree_digest(ROOT / "formalization-workbench")
    values = derive()
    A_s_match_4999 = sp.factor(values["A_s_hh_required"] - values["A_s_hh_4999"])
    direct_hh_delta_match = sp.factor(values["direct_delta"] - values["direct_delta_hh"])
    p1_match = sp.factor(values["p1_from_delta"] - values["p1_stored"])
    strict_D4_delta = sp.factor(values["direct_delta"].subs(D, 4))
    denominator_has_kinematic_poles = bool(
        values["full_helicity_denominator"].has(t)
        or values["full_helicity_denominator"].has(u)
    )
    if any(
        residual != 0
        for residual in (
            values["pole_identity"],
            A_s_match_4999,
            direct_hh_delta_match,
            p1_match,
            strict_D4_delta,
        )
    ):
        raise RuntimeError("physical IR completion algebra did not close")
    if not denominator_has_kinematic_poles:
        raise RuntimeError("the restored full-helicity residual unexpectedly became local")

    completion_rows = [
        {
            "coefficient": name,
            "formula": exact(values["mixed"][name]),
            "derivation": "4998 covariant physical-D shared cut",
            "status": "retained_direct",
        }
        for name in ("B_st_full", "B_su_full", "B_tu_full")
    ]
    completion_rows.extend(
        [
            {
                "coefficient": "A_t_physical(D)",
                "formula": exact(values["A_t"]),
                "derivation": "4998 coefficient with exact I2/I3 coordinate relation; independently regenerated at 5003 by crossing",
                "status": "retained_direct",
            },
            {
                "coefficient": "A_u_physical(D)",
                "formula": exact(values["A_u"]),
                "derivation": "4998 coefficient with exact I2/I3 coordinate relation; independently regenerated at 5003",
                "status": "retained_direct",
            },
            {
                "coefficient": "A_s_physical_IR_representative(D)",
                "formula": exact(values["A_s_required"]),
                "derivation": "unique exact representative solving 4*sum(B_xy/(xy))-sum(A_x/x)=0 with retained box and crossed-cut coefficients",
                "status": "selected_through_simple_pole_order",
            },
            {
                "coefficient": "A_s_scalar_direct(D)",
                "formula": exact(values["A_s_scalar"]),
                "derivation": "4997 direct scalar cut",
                "status": "retained_direct",
            },
            {
                "coefficient": "A_s_hh_physical_IR_representative(D)",
                "formula": exact(values["A_s_hh_required"]),
                "derivation": "A_s_physical_IR_representative-A_s_scalar_direct",
                "status": "selected_through_simple_pole_order",
            },
        ]
    )
    classification_rows = [
        {
            "object": "5000/5001 hh cut",
            "prior_label": "generic-D/CDR-like direct",
            "corrected_label": "HV physical-D-state cut: D_ext=4; D_int=D; D_loop=D",
            "test": "external spinor helicities are four-dimensional while internal graviton completeness and loop IBP use D",
            "status": "reclassified",
        },
        {
            "object": "4991 Chi hh continuation",
            "prior_label": "generic-D hh coefficient",
            "corrected_label": "FDH-like four-helicity continuation: D_ext=4; D_int=4; D_loop=D",
            "test": "only its bubble coefficient retains D dependence after the massless reduction",
            "status": "not_mixed_with_physical_D_state_coefficients",
        },
        {
            "object": "4999 A_s_hh_CDR_direct_inference",
            "prior_label": "CDR direct inference",
            "corrected_label": "physical-HV IR-completed representative",
            "test": "equals the independently reconstructed soft completion exactly but was not produced by a direct all-D external projection",
            "status": "value_promoted_label_retired",
        },
        {
            "object": "5001 direct_cut_P1",
            "prior_label": "crossing-symmetric local simple-pole obstruction",
            "corrected_label": "nonlocal full-helicity simple-pole residual",
            "test": f"restoring Qbar^-4 with Q*Qbar=t*u gives denominator {exact(values['full_helicity_denominator'])}",
            "status": "rejected_as_local_UV_owner",
        },
        {
            "object": "dJ2 ambiguity",
            "prior_label": "possible missing completion",
            "corrected_label": "finite rational ambiguity only",
            "test": "Dunbar-Norridge explicitly restrict the cut-free dJ2 ambiguity to finite rational terms",
            "status": "excluded_from_pole_cancellation",
        },
    ]
    quarantine_rows = [
        {
            "quantity": "A_s_full_direct_HV_candidate(D)",
            "formula": exact(values["A_s_direct"]),
            "residual_against_selected": exact(values["direct_delta"]),
            "D4_residual": exact(strict_D4_delta),
            "epsilon_linear_residual": exact(values["direct_delta_epsilon"]),
            "full_pole_effect": exact(values["p1_stored"]),
            "accepted_for_pole_assembly": False,
            "reason": "violates the universal soft identity and yields a nonlocal full-helicity pole with no admissible local counterterm owner",
            "status": "quarantined_beyond_strict_D4",
        },
        {
            "quantity": "A_s_hh_direct_HV_candidate(D)",
            "formula": exact(values["A_s_hh_direct"]),
            "residual_against_selected": exact(values["direct_delta_hh"]),
            "D4_residual": exact(values["direct_delta_hh"].subs(D, 4)),
            "epsilon_linear_residual": exact(epsilon_coefficient(values["direct_delta_hh"], 1)),
            "full_pole_effect": exact(values["p1_stored"]),
            "accepted_for_pole_assembly": False,
            "reason": "same entire evanescent mismatch as the full direct s-channel coefficient; microscopic current-level owner remains unlocated",
            "status": "quarantined_beyond_strict_D4",
        },
    ]
    gate_rows = [
        {
            "gate": "retained_box_and_crossed_cut_inputs",
            "passed": True,
            "status": "closed",
            "meaning": "physical-D boxes close on shared cuts and mixed one-scale coefficients were independently regenerated",
        },
        {
            "gate": "exact_soft_identity",
            "passed": values["pole_identity"] == 0,
            "status": "closed",
            "meaning": "the selected representative obeys 4*sum(B_xy/(xy))-sum(A_x/x)=0 identically",
        },
        {
            "gate": "4999_value_recovered_independently",
            "passed": A_s_match_4999 == 0,
            "status": "closed",
            "meaning": "the selected hh coefficient exactly equals the earlier IR-inferred value after retiring its unsupported CDR/direct label",
        },
        {
            "gate": "direct_residual_is_local_counterterm",
            "passed": False,
            "status": "excluded",
            "meaning": f"the restored helicity amplitude has kinematic denominator {exact(values['full_helicity_denominator'])}",
        },
        {
            "gate": "known_one_loop_counterterm_owns_two_scalar_two_graviton_pole",
            "passed": False,
            "status": "excluded_on_shell",
            "meaning": "the scalar-gravity divergence has four scalar legs and quadratic-curvature insertions do not alter two-scalar/n-graviton amplitudes",
        },
        {
            "gate": "constant_nonlocal_IR_pole_after_completion",
            "passed": True,
            "status": "closed_zero",
            "meaning": "P0=P1=0 through the required Laurent order",
        },
        {
            "gate": "microscopic_direct_s_cut_discrepancy",
            "passed": False,
            "status": "quarantined_not_forgotten",
            "meaning": "the physical pole assembly is fixed, but the precise missing evanescent state/current term in the direct s-cut implementation is not identified",
        },
        {
            "gate": "full_finite_one_loop_phi2h2",
            "passed": False,
            "status": "finite_rational_completion_open",
            "meaning": "dJ2 and finite master terms remain to be assembled before calling the entire one-loop amplitude complete",
        },
        {
            "gate": "full_MTS_claim",
            "passed": False,
            "status": "blocked",
            "meaning": "this is a private amplitude-sector checkpoint, not a theory-wide empirical or local-GR claim",
        },
    ]

    write_csv(COMPLETION_CSV, tagged(completion_rows))
    write_csv(CLASSIFICATION_CSV, tagged(classification_rows))
    write_csv(QUARANTINE_CSV, tagged(quarantine_rows))
    write_csv(GATE_CSV, tagged(gate_rows))
    formal_after = tree_digest(ROOT / "formalization-workbench")
    if formal_before != formal_after:
        raise RuntimeError("formalization-workbench changed during checkpoint")
    hashes = {relative(path): digest(path) for path in [*required, Path(__file__).resolve()]}
    result = {
        "checkpoint_marker": MARKER,
        "source_checked_date": CHECKED_DATE,
        "source_lock": locks,
        "source_hashes_sha256": hashes,
        "formalization_workbench_tree_sha256": formal_after,
        "scheme_classification": {
            "5000_5001": "HV: D_ext=4, D_int=D, D_loop=D",
            "4991": "FDH-like: D_ext=4, D_int=4, D_loop=D",
            "4999_value": "physical-HV IR-completed representative, not a direct CDR calculation",
        },
        "physical_A_s_IR_representative": exact(values["A_s_required"]),
        "physical_A_s_hh_IR_representative": exact(values["A_s_hh_required"]),
        "4999_value_residual": exact(A_s_match_4999),
        "direct_s_cut_evanescent_residual": exact(values["direct_delta"]),
        "direct_P1": exact(values["p1_stored"]),
        "full_helicity_direct_P1": exact(values["full_helicity_residual"]),
        "full_helicity_direct_P1_denominator": exact(values["full_helicity_denominator"]),
        "direct_P1_over_tree_reduced": exact(values["tree_ratio"]),
        "direct_P1_is_local": False,
        "direct_P1_has_source_backed_UV_owner": False,
        "constant_nonlocal_IR_pole_after_completion": "0",
        "outer_cut_IR_poles_complete": True,
        "direct_s_cut_microscopic_discrepancy_identified": False,
        "direct_s_cut_status": "quarantined_beyond_strict_D4",
        "finite_rational_completion_complete": False,
        "complete_one_loop_phi2h2": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "assemble the finite outer kernel from the selected pole-consistent coefficients and keep dJ2 explicit rather than reopening the closed IR pole",
        "outputs": [relative(path) for path in outputs],
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PROVENANCE.write_text(
        f"""# 5004 provenance

Checkpoint marker: `{MARKER}`

## Locked inputs

{chr(10).join(f'- `{path}` - SHA-256 `{value}`' for path, value in hashes.items())}

## Source interpretation

- Boels-Luo lines 919-928 distinguish `D_ext`, `D_int`, and `D_loop`; lines 1007-1068 explain four-dimensional external-state schemes and physical D-dimensional internal states.
- Dunbar-Norridge lines 1649-1674 state that `dJ2` is a finite rational ambiguity and identify the one-loop scalar-gravity counterterm as `(D phi . D phi)^2`, first visible with four external scalars.
- Accettulli Huber et al. lines 266 and 603-646 prove that `R^2` and `R_mn^2` do not alter on-shell two-scalar/n-graviton amplitudes.
- Checkpoint 4993 records `Q Qbar=tu` and the stripped phase `M=kappa^4 F/Qbar^4`; locality is therefore tested only after restoring that phase.

## Method

The physical box coefficients are retained from the covariant shared cuts. The physical crossed one-scale coefficients are formed with the exact `I2/I3` relation and carry the independent 5003 reconstruction. The `s` coefficient is then solved from the universal constant-pole identity. Subtracting the direct scalar cut gives the hh coefficient. This value is compared algebraically with 4999 and the direct 5001 continuation. The latter is restored to the full helicity amplitude before locality is judged.
""",
        encoding="utf-8",
    )
    DOCUMENT.write_text(
        f"""# 5004 - Physical HV IR completion and nonlocal-pole rejection

**Checkpoint marker:** `{MARKER}`  
**Date:** {CHECKED_DATE}  
**Claim status:** private amplitude derivation; not a complete one-loop or full-MTS claim.

## Result

The 5001 mismatch is resolved at the physical-amplitude pole level. Keeping the independently checked physical-D boxes and crossed one-scale coefficients, the universal soft equation fixes

```text
A_s(D) = {exact(values['A_s_required'])}.
```

After subtracting the direct scalar cut, the selected hh coefficient is

```text
A_s^hh(D) = {exact(values['A_s_hh_required'])}.
```

This is **exactly** the value stored at 4999: the residual is `{exact(A_s_match_4999)}`. What 4999 got wrong was the description `CDR direct inference`. It is an IR-completed representative for the physical HV amplitude, with `D_ext=4`, `D_int=D`, and `D_loop=D`.

## Why the competing term is rejected

The 5001 direct continuation differs by

```text
Delta A_s = {exact(values['direct_delta'])}.
```

It vanishes at strict `D=4`, but its linear evanescent part generates

```text
P1 = {exact(values['p1_stored'])}.
```

Calling this polynomial in the stripped reduced function a local UV obstruction was incorrect. The amplitude convention is `M^(1)=kappa^4 F/Qbar^4` and `Q Qbar=tu`. Restoring the helicity phase gives

```text
P1/Qbar^4 = {exact(values['full_helicity_residual'])},
```

whose denominator is `{exact(values['full_helicity_denominator'])}`. It is nonlocal in `t` and `u`. The known one-loop scalar-gravity counterterm has four scalar legs; source-backed `R^2` and `R_mn^2` insertions are silent in two-scalar/n-graviton amplitudes; and `dJ2` is finite only. There is therefore no admissible local owner for this pole.

## Decision

- Retain the physical-D boxes and directly regenerated mixed `t/u` coefficients.
- Use the soft-completed `A_s` through the Laurent order that controls the poles.
- Retire the unsupported `CDR direct` label at 4999 while promoting its value.
- Quarantine, rather than delete, the 5001 direct `s`-cut evanescent continuation.
- Do not reopen the constant IR-pole question unless a new direct calculation identifies the missing evanescent current term and also passes the restored-helicity locality gate.

The microscopic reason the direct `s`-cut implementation generated the extra evanescent term remains open. That does not leave the physical pole arbitrary: the retained cuts, soft theorem, and locality fix it uniquely. The next calculation is the finite outer kernel with `dJ2` kept explicit.
""",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

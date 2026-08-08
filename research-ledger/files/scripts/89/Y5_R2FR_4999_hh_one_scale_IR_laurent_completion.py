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
SOURCE = FUNCTIONAL / "4999"

MIXED_4998 = FUNCTIONAL / "4998" / "complete_generic_D_mixed_cut.csv"
BOX_4998 = FUNCTIONAL / "4998" / "generic_D_full_box_and_hh_inference.csv"
RESULT_4998 = FUNCTIONAL / "4998" / "covariant_mixed_projector_and_box_completion_results.json"
VALIDATION_4998 = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4998_VALIDATION.csv"
SCALAR_4997 = FUNCTIONAL / "4997" / "complete_generic_D_scalar_s_cut.csv"
RECONCILIATION_4997 = FUNCTIONAL / "4997" / "one_scale_coordinate_reconciliation.csv"
TRIANGLES_4993 = FUNCTIONAL / "4993" / "full_phi2h2_triangle_completion.csv"
HH_4991 = FUNCTIONAL / "4991" / "massless_hh_channel_integral_coefficients.csv"
IDENTITY_4995 = FUNCTIONAL / "4995" / "one_scale_master_identity.csv"

LAURENT_CSV = SOURCE / "IR_laurent_lower_sector_solve.csv"
HH_CSV = SOURCE / "hh_direct_one_scale_laurent.csv"
SCHEME_CSV = SOURCE / "evanescent_hh_scheme_translation.csv"
GATE_CSV = SOURCE / "hh_one_scale_IR_laurent_gate.csv"
RESULT_JSON = SOURCE / "hh_one_scale_IR_laurent_completion_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "4999-Y5-R2FR-hh-one-scale-IR-Laurent-completion.md"

MARKER = "MTS_4999_HH_ONE_SCALE_IR_LAURENT_COMPLETION"
CHECKED_DATE = "2026-07-14"

D = sp.Symbol("D")
epsilon = sp.Symbol("epsilon")
t = sp.Symbol("t", nonzero=True)
u = sp.Symbol("u", nonzero=True)
s = -t - u


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


def expression(value: str) -> sp.Expr:
    return sp.sympify(value, locals={"D": D, "epsilon": epsilon, "s": s, "t": t, "u": u})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
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


def source_lock() -> dict[str, bool]:
    result = json.loads(RESULT_4998.read_text(encoding="utf-8"))
    validation = read_csv(VALIDATION_4998)
    identity = read_csv(IDENTITY_4995)
    reconciliation = read_csv(RECONCILIATION_4997)
    return {
        "4998_covariant_mixed_cut": result.get("generic_D_mixed_cut_complete") is True,
        "4998_generic_D_boxes": result.get("generic_D_full_box_sector_complete") is True,
        "4998_validation": bool(validation) and all(row["passed"] == "True" for row in validation),
        "4997_scalar_direct_cut": any(row["coefficient"] == "T_s_scalar_direct(D)" for row in read_csv(SCALAR_4997)),
        "4997_translation_residue": any(row["identity"] == "mandatory_translation_pole_residue" and row["residual"] == "0" for row in reconciliation),
        "4995_master_identity": any(row["identity"] == "exact_one_scale_master_relation" and row["residual"] == "0" for row in identity),
        "4993_full_IR_triangle": any(row["triangle_id"] == "TRI4993_01_Ts" for row in read_csv(TRIANGLES_4993)),
        "4991_FDH_hh_seed": any(row["basis_id"] == "HHAMP4991_02_I3s" for row in read_csv(HH_4991)),
    }


def coefficient_map(path: Path, key: str) -> dict[str, sp.Expr]:
    return {row[key]: expression(row["formula"]) for row in read_csv(path) if row.get(key) and row.get("formula")}


def epsilon_coefficients(value: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    continued = sp.factor(value.subs(D, 4 - 2 * epsilon))
    return sp.factor(continued.subs(epsilon, 0)), sp.factor(sp.diff(continued, epsilon).subs(epsilon, 0))


def derive() -> dict[str, sp.Expr]:
    mixed = coefficient_map(MIXED_4998, "coefficient")
    scalar = coefficient_map(SCALAR_4997, "coefficient")
    ratio = lambda channel: sp.factor((D - 4) * channel / (2 * (D - 3)))

    B_st = mixed["B_st_full"]
    B_su = mixed["B_su_full"]
    B_tu = mixed["B_tu_full"]
    A_t = sp.factor(mixed["T_t_finite"] + ratio(t) * mixed["C_t_finite"])
    A_u = sp.factor(mixed["T_u_finite"] + ratio(u) * mixed["C_u_finite"])

    B_st_0, B_st_1 = epsilon_coefficients(B_st)
    B_su_0, B_su_1 = epsilon_coefficients(B_su)
    B_tu_0, B_tu_1 = epsilon_coefficients(B_tu)
    A_t_0, A_t_1 = epsilon_coefficients(A_t)
    A_u_0, A_u_1 = epsilon_coefficients(A_u)

    box_sum_0 = sp.factor(B_st_0 / (s * t) + B_su_0 / (s * u) + B_tu_0 / (t * u))
    box_sum_1 = sp.factor(B_st_1 / (s * t) + B_su_1 / (s * u) + B_tu_1 / (t * u))
    A_s_0 = sp.factor(s * (4 * box_sum_0 - A_t_0 / t - A_u_0 / u))
    A_s_1 = sp.factor(s * (4 * box_sum_1 - A_t_1 / t - A_u_1 / u))

    T_scalar = scalar["T_s_scalar_direct(D)"]
    scalar_0, scalar_1 = epsilon_coefficients(T_scalar)
    hh_0 = sp.factor(A_s_0 - scalar_0)
    hh_1 = sp.factor(A_s_1 - scalar_1)

    hh_rows = read_csv(HH_4991)
    hh_fdh_0 = expression(next(row["coefficient_D4"] for row in hh_rows if row["basis_id"] == "HHAMP4991_02_I3s"))
    C_hh_0 = expression(next(row["coefficient_D4"] for row in hh_rows if row["basis_id"] == "HHAMP4991_01_I2s"))
    hh_fdh_1 = sp.factor(-s * C_hh_0)
    scalar_translation = expression(next(row["right_hand_side"] for row in read_csv(RECONCILIATION_4997) if row["identity"] == "D4_triangle_coordinate_difference"))
    full_IR_target = expression(next(row["coefficient"] for row in read_csv(TRIANGLES_4993) if row["triangle_id"] == "TRI4993_01_Ts"))

    A_s_IR_representative = sp.factor(
        s * (4 * (B_st / (s * t) + B_su / (s * u) + B_tu / (t * u)) - A_t / t - A_u / u)
    )
    hh_IR_representative = sp.factor(A_s_IR_representative - T_scalar)

    return {
        "B_st_0": B_st_0,
        "B_st_1": B_st_1,
        "B_su_0": B_su_0,
        "B_su_1": B_su_1,
        "B_tu_0": B_tu_0,
        "B_tu_1": B_tu_1,
        "A_t_0": A_t_0,
        "A_t_1": A_t_1,
        "A_u_0": A_u_0,
        "A_u_1": A_u_1,
        "A_s_0": A_s_0,
        "A_s_1": A_s_1,
        "scalar_0": scalar_0,
        "scalar_1": scalar_1,
        "hh_0": hh_0,
        "hh_1": hh_1,
        "hh_fdh_0": hh_fdh_0,
        "hh_fdh_1": hh_fdh_1,
        "scalar_translation": scalar_translation,
        "full_IR_target": full_IR_target,
        "A_s_IR_representative": A_s_IR_representative,
        "hh_IR_representative": hh_IR_representative,
        "P0": sp.factor(4 * box_sum_0 - A_s_0 / s - A_t_0 / t - A_u_0 / u),
        "P1": sp.factor(4 * box_sum_1 - A_s_1 / s - A_t_1 / t - A_u_1 / u),
    }


def laurent_rows(values: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    rows = []
    for channel in ("t", "u", "s"):
        rows.append(
            {
                "channel": channel,
                "physical_coefficient": f"A_{channel}=T_{channel}+[(D-4){channel}/(2(D-3))]C_{channel}",
                "epsilon_0": exact(values[f"A_{channel}_0"]),
                "epsilon_1": exact(values[f"A_{channel}_1"]),
                "derivation": "4998 direct crossed cut" if channel != "s" else "unique IR Laurent solve from complete boxes and crossed cuts",
                "status": "closed_through_linear_epsilon",
            }
        )
    rows.extend(
        [
            {
                "channel": "all",
                "physical_coefficient": "constant 1/epsilon^2 equation",
                "epsilon_0": exact(values["P0"]),
                "epsilon_1": "not_applicable",
                "derivation": "4 sum B0/(xy)-sum A0/x",
                "status": "closed",
            },
            {
                "channel": "all",
                "physical_coefficient": "constant 1/epsilon equation from coefficient continuation",
                "epsilon_0": "not_applicable",
                "epsilon_1": exact(values["P1"]),
                "derivation": "4 sum B1/(xy)-sum A1/x; bubbles included through A=T+rC",
                "status": "closed",
            },
        ]
    )
    return rows


def hh_rows(values: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    return [
        {
            "component": "A_s_full_direct",
            "epsilon_0": exact(values["A_s_0"]),
            "epsilon_1": exact(values["A_s_1"]),
            "exact_generic_D_formula": exact(values["A_s_IR_representative"]),
            "exact_formula_status": "IR_minimal_representative_not_direct_cut_proof",
            "status": "Laurent_coefficients_closed_through_O_epsilon",
        },
        {
            "component": "A_s_scalar_direct",
            "epsilon_0": exact(values["scalar_0"]),
            "epsilon_1": exact(values["scalar_1"]),
            "exact_generic_D_formula": "4997 source formula",
            "exact_formula_status": "direct_cut_complete",
            "status": "closed",
        },
        {
            "component": "A_s_hh_CDR_direct_inference",
            "epsilon_0": exact(values["hh_0"]),
            "epsilon_1": exact(values["hh_1"]),
            "exact_generic_D_formula": exact(values["hh_IR_representative"]),
            "exact_formula_status": "candidate_beyond_linear_epsilon_not_promoted",
            "status": "Laurent_coefficients_closed_through_O_epsilon",
        },
    ]


def scheme_rows(values: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    return [
        {
            "quantity": "hh_FDH_source",
            "epsilon_0": exact(values["hh_fdh_0"]),
            "epsilon_1": exact(values["hh_fdh_1"]),
            "meaning": "4991 four-helicity state sum in the physical one-scale coordinate",
            "status": "source_locked",
        },
        {
            "quantity": "hh_CDR_minus_FDH",
            "epsilon_0": exact(values["hh_0"] - values["hh_fdh_0"]),
            "epsilon_1": exact(values["hh_1"] - values["hh_fdh_1"]),
            "meaning": "evanescent internal-graviton completion required by shared-cut plus IR consistency",
            "status": "derived_through_linear_epsilon",
        },
        {
            "quantity": "epsilon_0_translation_checksum",
            "epsilon_0": exact(values["hh_0"] - values["hh_fdh_0"] - values["scalar_translation"]),
            "epsilon_1": "not_applicable",
            "meaning": "hh scheme shift exactly equals the 4997 scalar coordinate translation",
            "status": "closed",
        },
        {
            "quantity": "full_s_IR_target_checksum",
            "epsilon_0": exact(values["A_s_0"] - values["full_IR_target"]),
            "epsilon_1": "not_applicable",
            "meaning": "direct full-state coefficient reproduces the universal 4993 IR triangle",
            "status": "closed",
        },
    ]


def write_document(values: dict[str, sp.Expr]) -> None:
    text = f"""# 4999 - hh one-scale IR Laurent completion

**Checkpoint marker:** `{MARKER}`  
**Date:** {CHECKED_DATE}  
**Claim status:** private amplitude derivation; not a complete one-loop, outer-cut, local-GR, or full-MTS claim.

## Result

The physical one-scale coefficient is the basis-invariant combination

```text
A_x(D)=T_x(D)+(D-4)x/[2(D-3)] C_x(D).
```

Write `A_x(4-2 epsilon)=A_x,0+epsilon A_x,1+O(epsilon^2)`. The generic-D boxes and crossed `t/u` cuts from 4998 leave no freedom in the IR-visible `s` coefficient. The constant double- and simple-pole equations are

```text
4 sum B_xy,0/(xy)-sum A_x,0/x=0,
4 sum B_xy,1/(xy)-sum A_x,1/x=0.
```

Both residuals vanish exactly. The solved full `s` coefficients are

```text
A_s,0 = {exact(values['A_s_0'])}
A_s,1 = {exact(values['A_s_1'])}.
```

Subtracting the exact scalar direct cut from 4997 gives the missing internal-graviton contribution

```text
A_s,0^(hh) = {exact(values['hh_0'])}
A_s,1^(hh) = {exact(values['hh_1'])}.
```

## Evanescent correction

The 4991 source sums only the two four-dimensional helicities while integrating in `D=4-2 epsilon`. Its direct physical one-scale coefficients are

```text
A_s,0^(hh,FDH) = {exact(values['hh_fdh_0'])}
A_s,1^(hh,FDH) = {exact(values['hh_fdh_1'])}.
```

The finite `epsilon^0` CDR-minus-FDH shift is

```text
{exact(values['hh_0'] - values['hh_fdh_0'])}.
```

This equals the independently derived 4997 scalar one-scale coordinate translation exactly. It explains why simply importing the 4991 triangle into the generic-D state sum gives the wrong direct coefficient even though every box has the correct four-dimensional limit.

## Boundary of the result

The Laurent coefficients through linear `epsilon` are fixed because they own the constant `1/epsilon^2` and `1/epsilon` poles. Extending the displayed IR-minimal rational representative to arbitrary `D` is not licensed by those two equations. The `epsilon^2` coefficient can feed a finite cut-free rational term and therefore remains part of the `d J2` reconstruction. The next calculation is a direct `mu^2`-moment/projector reduction that must either validate the candidate beyond linear order or replace it.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    required = [MIXED_4998, BOX_4998, RESULT_4998, VALIDATION_4998, SCALAR_4997, RECONCILIATION_4997, TRIANGLES_4993, HH_4991, IDENTITY_4995]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("missing inputs: " + "; ".join(missing))
    locks = source_lock()
    if not all(locks.values()):
        raise RuntimeError(f"source lock failed: {locks}")
    outputs = [LAURENT_CSV, HH_CSV, SCHEME_CSV, GATE_CSV, RESULT_JSON, PROVENANCE, DOCUMENT]
    if args.dry_run:
        print(json.dumps({"checkpoint_marker": MARKER, "source_lock": locks, "writes": [relative(path) for path in outputs]}, indent=2, sort_keys=True))
        return 0

    formal_before = tree_digest(ROOT / "formalization-workbench")
    values = derive()
    if values["P0"] != 0 or values["P1"] != 0:
        raise RuntimeError("IR Laurent solve failed")
    if sp.factor(values["A_s_0"] - values["full_IR_target"]) != 0:
        raise RuntimeError("4993 full IR target mismatch")
    if sp.factor(values["hh_0"] - values["hh_fdh_0"] - values["scalar_translation"]) != 0:
        raise RuntimeError("evanescent translation checksum failed")

    laurent = laurent_rows(values)
    hh = hh_rows(values)
    scheme = scheme_rows(values)
    gates = [
        {"gate": "basis_invariant_one_scale_coefficient", "passed": True, "status": "closed", "meaning": "A=T+[(D-4)x/(2(D-3))]C"},
        {"gate": "constant_double_pole_solve", "passed": True, "status": "closed", "meaning": "A_s,0 uniquely fixed"},
        {"gate": "constant_simple_pole_solve", "passed": True, "status": "closed", "meaning": "A_s,1 uniquely fixed"},
        {"gate": "hh_direct_laurent_through_linear_epsilon", "passed": True, "status": "closed", "meaning": "full minus exact scalar direct cut"},
        {"gate": "FDH_CDR_translation", "passed": True, "status": "closed", "meaning": "finite shift equals independent scalar coordinate translation"},
        {"gate": "exact_generic_D_hh_lower_sector", "passed": False, "status": "open", "meaning": "IR equations license only epsilon^0 and epsilon^1"},
        {"gate": "cut_free_dJ2_remainder", "passed": False, "status": "open", "meaning": "epsilon^2/rational projector moment remains"},
        {"gate": "outer_cut_or_full_MTS", "passed": False, "status": "open", "meaning": "not licensed here"},
    ]
    write_csv(LAURENT_CSV, tagged(laurent))
    write_csv(HH_CSV, tagged(hh))
    write_csv(SCHEME_CSV, tagged(scheme))
    write_csv(GATE_CSV, tagged(gates))
    write_document(values)

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
        "basis_invariant_one_scale_definition": "A_x(D)=T_x(D)+(D-4)*x/[2(D-3)]*C_x(D)",
        "full_s_laurent": {"epsilon_0": exact(values["A_s_0"]), "epsilon_1": exact(values["A_s_1"])},
        "hh_s_laurent": {"epsilon_0": exact(values["hh_0"]), "epsilon_1": exact(values["hh_1"])},
        "hh_CDR_minus_FDH": {"epsilon_0": exact(values["hh_0"] - values["hh_fdh_0"]), "epsilon_1": exact(values["hh_1"] - values["hh_fdh_1"])},
        "IR_visible_hh_lower_sector_complete_through_linear_epsilon": True,
        "exact_generic_D_hh_lower_sector_complete": False,
        "cut_free_dJ2_remainder_complete": False,
        "complete_one_loop_phi2h2": False,
        "outer_cut_complete": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "direct mu-squared projector-moment reduction through epsilon^2 and the cut-free dJ2 term",
        "outputs": [relative(path) for path in outputs],
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PROVENANCE.write_text(
        "\n".join(
            [
                "# 4999 hh one-scale IR Laurent provenance",
                "",
                f"Marker: `{MARKER}`.",
                "",
                "The calculation reparses the completed generic-D boxes and crossed cuts, converts every triangle/bubble pair to the exact one-scale coefficient A=T+rC, and solves the constant double- and simple-pole equations. It then subtracts the independently completed scalar direct cut. No arbitrary-D continuation beyond the licensed epsilon^0 and epsilon^1 coefficients is promoted.",
                "",
                "## SHA-256",
                "",
                *[f"- `{path}`: `{value}`" for path, value in hashes.items()],
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

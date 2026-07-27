from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

import sympy as sp
from sympy.parsing.mathematica import parse_mathematica


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4972"
WILSON_SELECTION = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4963"
    / "C3_Wilson_selection_and_running.csv"
)
STATE_COUNTS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4971"
    / "Bern_R3_field_content_branches.csv"
)
ABREU_MAIN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4971"
    / "src-2002.12374"
    / "source"
    / "main.tex"
)
ABREU_PPPP = ABREU_MAIN.parent / "anc" / "2loopRemainder" / "pppp_s-channel.m"
ABREU_MPPP = ABREU_MAIN.parent / "anc" / "2loopRemainder" / "mppp_s-channel.m"
AS_2509_NOTES = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4928"
    / "src2509"
    / "notes.tex"
)
AS_2509_RESULT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_R2FR_4928_CONDITIONAL_PREDICTION.csv"
)
AS_2312_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4929"
    / "src2312"
    / "ess_cubic.tex"
)
RESULT_4971 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4971"
    / "C3_parent_matching_and_anchor_results.json"
)

NORMALIZATION_CSV = SOURCE / "C3_EAA_to_amplitude_normalization.csv"
ANCHOR_ESTIMATES_CSV = SOURCE / "C3_local_anchor_estimates.csv"
NONLOCAL_COMPLETION_CSV = SOURCE / "C3_nonlocal_log_completion.csv"
IDENTIFIABILITY_CSV = SOURCE / "C3_finite_conversion_identifiability.csv"
HELICITY_CSV = SOURCE / "C3_helicity_matching_predictions.csv"
RESULT_JSON = SOURCE / "C3_EAA_to_amplitude_matching_results.json"

MARKER = "MTS_4972_C3_EAA_TO_AMPLITUDE_MATCHING"
CHECKED_DATE = "2026-07-13"
SYMMETRIC_S = 1.0
SYMMETRIC_T = -0.5
SYMMETRIC_U = -0.5
SYMMETRIC_STU = SYMMETRIC_S * SYMMETRIC_T * SYMMETRIC_U

EXPECTED_HASHES = {
    WILSON_SELECTION: "c130ad2c49cce89682726377d459d3af7119a330c82af10a6c18bed770f7dfa0",
    STATE_COUNTS: "de37558cce41f97a37159ca4a2f28250df5b8ae37034b8154fa34a97b08c2bda",
    ABREU_MAIN: "11acdee89baad0298aafc5cc975be9d981d985bb37d2da86914281ca2c997fc8",
    ABREU_PPPP: "42128b16a7451b6213abd06c0eae9bfa649f5890df365c04f6209fd6b5630483",
    ABREU_MPPP: "6d426fbba39e4a02413fd17f5d4869a33c3cabb4263d88dd8e9e8e8a7a52c2a5",
    AS_2509_NOTES: "25ee14542211cd5769ae0f39519efb0edcba5d917cb46b949015b9e78bdbda1f",
    AS_2509_RESULT: "6b91ac5fe33497089146d89d860d1278e42709aa2a191119a3deb9c98d46a5a2",
    AS_2312_SOURCE: "b23b0974509278be22c8917f531a2963d415184d9052e27860c65fad80943a1d",
    RESULT_4971: "87461a2c25be6c9589384fa604d2b4bf85c529ffb40dc3f551643db2ddeb98b3",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
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


def parse_abreu_remainder(path: Path) -> sp.Expr:
    source_text = path.read_text(encoding="utf-8")
    normalized = source_text.replace("cGB[mu]", "cgb").replace(
        "cR3[mu]", "cr3"
    )
    normalized = re.sub(r"\bS\b", "ss", normalized)
    normalized = re.sub(r"\bT\b", "tt", normalized)
    return parse_mathematica(normalized)


def normalization_map() -> tuple[list[dict[str, Any]], dict[str, bool]]:
    newton, ratio, c_r3, c_gb = sp.symbols("G_N r_C3 c_R3 c_GB", nonzero=True)
    kappa_squared = 32 * sp.pi * newton
    abreu_coefficient = sp.simplify(
        c_r3 * (kappa_squared / 4) / (4 * sp.pi) ** 4
    )
    solved_c_r3 = sp.solve(
        sp.Eq(newton * ratio, abreu_coefficient), c_r3
    )[0]
    physical_c = c_r3 - c_gb / 2
    essential_tree_c = sp.simplify(
        physical_c.subs({c_r3: solved_c_r3, c_gb: 0})
    )
    bern_coordinate = sp.simplify(-essential_tree_c / (32 * sp.pi**3))

    all_plus = parse_abreu_remainder(ABREU_PPPP)
    single_minus = parse_abreu_remainder(ABREU_MPPP)
    source_cgb, source_cr3, mandelstam_s, mandelstam_t = sp.symbols(
        "cgb cr3 ss tt"
    )
    mandelstam_u = -mandelstam_s - mandelstam_t
    stu = mandelstam_s * mandelstam_t * mandelstam_u
    all_plus_physical = sp.factor(
        sp.diff(all_plus, source_cr3) - 2 * sp.diff(all_plus, source_cgb)
    )
    single_minus_physical = sp.factor(
        sp.diff(single_minus, source_cr3)
        - 2 * sp.diff(single_minus, source_cgb)
    )

    checks = {
        "abreu_action_reduces_to_Gc_over_32pi3": sp.simplify(
            abreu_coefficient - newton * c_r3 / (32 * sp.pi**3)
        )
        == 0,
        "cR3_map_exact": sp.simplify(solved_c_r3 - 32 * sp.pi**3 * ratio)
        == 0,
        "Bern_tree_map_exact": sp.simplify(bern_coordinate + ratio) == 0,
        "all_plus_physical_projector_exact": sp.simplify(
            all_plus_physical + 120 * stu
        )
        == 0,
        "single_minus_physical_projector_exact": sp.simplify(
            single_minus_physical + 12 * stu
        )
        == 0,
    }
    rows = tagged(
        [
            {
                "map_id": "MAP4972_00_EAA",
                "object": "parent essential EAA coefficient",
                "equation": "L_EAA contains G_C3 C^3 with r_C3=G_C3/G_N",
                "result": "coefficient of C^3 is G_N*r_C3",
                "status": "SOURCE_LOCKED",
            },
            {
                "map_id": "MAP4972_01_ABREU",
                "object": "Abreu R3 action coefficient",
                "equation": "c_R3*(kappa/2)^2/(4*pi)^4; kappa^2=32*pi*G_N",
                "result": "G_N*c_R3/(32*pi^3)",
                "status": "SYMBOLICALLY_DERIVED",
            },
            {
                "map_id": "MAP4972_02_TREE",
                "object": "strict-four-dimensional essential tree representative",
                "equation": "c_GB=0; G_N*r_C3=G_N*c_R3/(32*pi^3)",
                "result": "c_tree=c_R3=32*pi^3*r_C3",
                "status": "EXACT_TREE_LEVEL_NORMALIZATION",
            },
            {
                "map_id": "MAP4972_03_BERN",
                "object": "Bern-oriented amplitude coordinate",
                "equation": "A_Bern=-c_tree/(32*pi^3)",
                "result": "A_Bern_tree=-r_C3",
                "status": "EXACT_TREE_LEVEL_NORMALIZATION",
            },
            {
                "map_id": "MAP4972_04_PHYSICAL",
                "object": "finite loop-completed amplitude coordinate",
                "equation": "c_phys(mu_m)=32*pi^3*r_C3^S+delta_c_fin(mu_m)",
                "result": "one additive finite conversion remains beyond the exact tree map",
                "status": "NONLOCAL_FINITE_CONVERSION_ISOLATED",
            },
        ]
    )
    return rows, checks


def selected_parent_values() -> dict[str, float]:
    rows = {row["selection_id"]: row for row in read_csv(WILSON_SELECTION)}
    massless = rows["C3SEL4963_massless_envelope"]
    finite_gap = rows["C3SEL4963_finite_gap_envelope"]
    return {
        "r_min": float(finite_gap["A_C3_selected_min"]),
        "r_max": float(finite_gap["A_C3_selected_max"]),
        "b_min": float(massless["B_C3_source_min"]),
        "b_max": float(massless["B_C3_source_max"]),
    }


def state_count_values() -> dict[str, float]:
    rows = {row["branch"]: row for row in read_csv(STATE_COUNTS)}
    return {
        "SM45": float(rows["SM45"]["total_Nb_minus_Nf"]),
        "SM45_PLUS_MOTION": float(
            rows["SM45_PLUS_MOTION"]["total_Nb_minus_Nf"]
        ),
    }


def external_comparators() -> list[dict[str, Any]]:
    source_rows = read_csv(AS_2509_RESULT)
    natural_row = next(
        row for row in source_rows if row["branch"] == "natural_regulator_reproduced"
    )
    natural_ratio = float(natural_row["G_C3_over_G_N"])
    older_text = AS_2312_SOURCE.read_text(encoding="utf-8")
    older_match = re.search(
        r"A\s*=\s*-3\.988\s*\\cdot\s*10\^\{-6\}", older_text
    )
    if older_match is None:
        raise ValueError("could not source-lock the 2312 Wilson coefficient")
    return [
        {
            "branch": "AS2509_NATURAL_PURE_GRAVITY",
            "field_count_N": 2.0,
            "r_C3": natural_ratio,
            "source": relative(AS_2509_RESULT),
            "role": "external pure-gravity natural-regulator comparator",
        },
        {
            "branch": "AS2312_MES_PURE_GRAVITY",
            "field_count_N": 2.0,
            "r_C3": -3.988e-6,
            "source": relative(AS_2312_SOURCE),
            "role": "external pure-gravity MES comparator",
        },
    ]


def anchor_and_helicity_rows(
    parent: dict[str, float], state_counts: dict[str, float]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    branches: list[dict[str, Any]] = []
    for branch, state_count in state_counts.items():
        for endpoint, ratio in (("min", parent["r_min"]), ("max", parent["r_max"])):
            branches.append(
                {
                    "branch": f"MTS_{branch}_{endpoint}",
                    "field_count_N": state_count,
                    "r_C3": ratio,
                    "source": relative(WILSON_SELECTION),
                    "role": "current parent local-EFT selected envelope",
                }
            )
    branches.extend(external_comparators())

    anchors: list[dict[str, Any]] = []
    helicities: list[dict[str, Any]] = []
    for branch in branches:
        ratio = float(branch["r_C3"])
        state_count = float(branch["field_count_N"])
        c_tree = 32.0 * math.pi**3 * ratio
        bern_tree = -ratio
        beta_bern = state_count / (7680.0 * math.pi**3)
        lambda_over_mu_zero_conversion = math.exp(240.0 * c_tree / state_count)
        anchors.append(
            {
                **branch,
                "c_tree": c_tree,
                "A_Bern_tree": bern_tree,
                "beta_A_physical": beta_bern,
                "delta_c_fin": 0.0,
                "lambda_over_mu_matching": lambda_over_mu_zero_conversion,
                "delta_c_needed_to_zero_c_phys": -c_tree,
                "d_ln_lambda_over_mu_d_delta_c": 240.0 / state_count,
                "status": "LOCAL_EFT_MATCHING_PRESCRIPTION_NOT_FULL_AMPLITUDE_CLAIM",
            }
        )
        all_plus_shift = -60.0 * c_tree * SYMMETRIC_STU
        single_minus_shift = -6.0 * c_tree * SYMMETRIC_STU
        helicities.extend(
            [
                {
                    "branch": branch["branch"],
                    "helicity": "++++",
                    "s": SYMMETRIC_S,
                    "t": SYMMETRIC_T,
                    "u": SYMMETRIC_U,
                    "stu": SYMMETRIC_STU,
                    "c_tree": c_tree,
                    "delta_remainder": all_plus_shift,
                    "projected_A_Bern": all_plus_shift
                    / (1920.0 * math.pi**3 * SYMMETRIC_STU),
                    "status": "EXACT_LOCAL_C3_TREE_INSERTION",
                },
                {
                    "branch": branch["branch"],
                    "helicity": "-+++",
                    "s": SYMMETRIC_S,
                    "t": SYMMETRIC_T,
                    "u": SYMMETRIC_U,
                    "stu": SYMMETRIC_STU,
                    "c_tree": c_tree,
                    "delta_remainder": single_minus_shift,
                    "projected_A_Bern": single_minus_shift
                    / (192.0 * math.pi**3 * SYMMETRIC_STU),
                    "status": "EXACT_LOCAL_C3_TREE_INSERTION",
                },
            ]
        )
    return tagged(anchors), tagged(helicities)


def nonlocal_completion_rows(
    parent: dict[str, float], state_counts: dict[str, float]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch, state_count in state_counts.items():
        for b_endpoint, local_b in (
            ("min", parent["b_min"]),
            ("max", parent["b_max"]),
        ):
            local_c_log_slope = 64.0 * math.pi**3 * local_b
            physical_c_log_slope = -state_count / 240.0
            required_nonlocal_slope = physical_c_log_slope - local_c_log_slope
            rows.append(
                {
                    "branch": branch,
                    "B_C3_endpoint": b_endpoint,
                    "B_C3_ln_g": local_b,
                    "d_r_C3_d_ln_k": 2.0 * local_b,
                    "d_c_local_d_ln_k": local_c_log_slope,
                    "d_c_physical_d_ln_mu": physical_c_log_slope,
                    "d_delta_c_nonlocal_d_ln_mu": required_nonlocal_slope,
                    "closure_identity": "64*pi^3*B_C3+d(delta_c_NL)/dln(mu)=-N/240",
                    "finite_constant": "delta_c_fin(mu_m) remains one matching datum",
                    "status": "NONLOCAL_LOG_SLOPE_DERIVED_FINITE_CONSTANT_OPEN",
                }
            )
    return tagged(rows)


def identifiability_rows() -> tuple[list[dict[str, Any]], dict[str, bool]]:
    symbolic_pi = sp.pi
    matrix = sp.Matrix(
        [
            [-60 * SYMMETRIC_STU * 32 * symbolic_pi**3, -60 * SYMMETRIC_STU],
            [-6 * SYMMETRIC_STU * 32 * symbolic_pi**3, -6 * SYMMETRIC_STU],
        ]
    )
    nullspace = matrix.nullspace()
    expected_null = sp.Matrix([1, -32 * symbolic_pi**3])
    null_exact = len(nullspace) == 1 and sp.simplify(
        matrix * expected_null
    ) == sp.zeros(2, 1)
    rows = tagged(
        [
            {
                "test_id": "ID4972_00_TWO_HELICITY",
                "unknowns": "r_C3^S,delta_c_fin",
                "observables": "Delta_R_pppp,Delta_R_mppp at one matching scale",
                "matrix_rank": matrix.rank(),
                "nullity": 2 - matrix.rank(),
                "null_direction": "delta r=epsilon; delta(delta_c_fin)=-32*pi^3*epsilon",
                "result": "helicity cross-check validates C3 structure but cannot split local and finite nonlocal constants",
                "status": "EXACT_RANK_ONE_NO_GO",
            },
            {
                "test_id": "ID4972_01_RUNNING",
                "unknowns": "nonlocal logarithmic slope,delta_c_fin",
                "observables": "physical beta plus local FRG infrared slope",
                "matrix_rank": 1,
                "nullity": 1,
                "null_direction": "additive delta_c_fin",
                "result": "RG consistency fixes the full logarithmic slope but not the finite matching constant",
                "status": "LOG_DERIVED_ONE_FINITE_CONSTANT_REMAINS",
            },
            {
                "test_id": "ID4972_02_SOURCE_PRESCRIPTION",
                "unknowns": "delta_c_fin",
                "observables": "k0=M_Pl and log-subtracted local Wilson coefficient",
                "matrix_rank": 0,
                "nullity": 1,
                "null_direction": "finite Wilsonian-to-on-shell scheme conversion",
                "result": "delta_c_fin=0 is a usable source prescription, not a derivation from the local EAA",
                "status": "CONDITIONAL_LOCAL_EFT_ANCHOR_ONLY",
            },
        ]
    )
    return rows, {
        "two_helicity_matrix_rank_one": matrix.rank() == 1,
        "finite_conversion_null_direction_exact": null_exact,
    }


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    source_hashes: dict[str, str] = {}
    for path, expected_hash in EXPECTED_HASHES.items():
        if not path.exists():
            raise FileNotFoundError(path)
        actual_hash = digest(path)
        if actual_hash != expected_hash:
            raise ValueError(
                f"source hash mismatch for {path}: {actual_hash} != {expected_hash}"
            )
        source_hashes[relative(path)] = actual_hash

    normalization_rows, normalization_checks = normalization_map()
    parent = selected_parent_values()
    state_counts = state_count_values()
    anchor_rows, helicity_rows = anchor_and_helicity_rows(parent, state_counts)
    nonlocal_rows = nonlocal_completion_rows(parent, state_counts)
    identifiability, identifiability_checks = identifiability_rows()

    branch_pairs: dict[str, dict[str, float]] = {}
    for row in helicity_rows:
        branch_pairs.setdefault(row["branch"], {})[row["helicity"]] = float(
            row["delta_remainder"]
        )
    cross_helicity_exact = all(
        math.isclose(values["++++"], 10.0 * values["-+++"], rel_tol=2e-15)
        for values in branch_pairs.values()
    )
    projected_coordinates_agree = all(
        math.isclose(
            float(row["projected_A_Bern"]),
            -float(row["c_tree"]) / (32.0 * math.pi**3),
            rel_tol=2e-15,
            abs_tol=1e-18,
        )
        for row in helicity_rows
    )
    nonlocal_closure = all(
        math.isclose(
            float(row["d_c_local_d_ln_k"])
            + float(row["d_delta_c_nonlocal_d_ln_mu"]),
            float(row["d_c_physical_d_ln_mu"]),
            rel_tol=2e-15,
            abs_tol=1e-15,
        )
        for row in nonlocal_rows
    )
    checks = {
        **normalization_checks,
        **identifiability_checks,
        "current_parent_interval_ordered_negative": parent["r_min"]
        < parent["r_max"]
        < 0.0,
        "state_counts_source_locked": state_counts
        == {"SM45": -60.0, "SM45_PLUS_MOTION": -59.0},
        "six_anchor_rows_generated": len(anchor_rows) == 6,
        "twelve_helicity_rows_generated": len(helicity_rows) == 12,
        "four_nonlocal_completion_rows_generated": len(nonlocal_rows) == 4,
        "cross_helicity_factor_ten_exact": cross_helicity_exact,
        "both_helicities_recover_same_Bern_coordinate": projected_coordinates_agree,
        "nonlocal_log_completion_closes_physical_running": nonlocal_closure,
        "all_anchor_values_finite": all(
            math.isfinite(float(row["lambda_over_mu_matching"]))
            and float(row["lambda_over_mu_matching"]) > 0.0
            for row in anchor_rows
        ),
    }

    write_csv(NORMALIZATION_CSV, normalization_rows)
    write_csv(ANCHOR_ESTIMATES_CSV, anchor_rows)
    write_csv(NONLOCAL_COMPLETION_CSV, nonlocal_rows)
    write_csv(IDENTIFIABILITY_CSV, identifiability)
    write_csv(HELICITY_CSV, helicity_rows)

    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_hashes": source_hashes,
        "selected_parent": parent,
        "state_counts": state_counts,
        "normalization": {
            "c_tree": "32*pi^3*r_C3",
            "A_Bern_tree": "-r_C3",
            "c_physical": "32*pi^3*r_C3+delta_c_fin",
        },
        "nonlocal_completion": {
            "local_slope": "dc_local/dlnk=64*pi^3*B_C3",
            "physical_slope": "dc_phys/dlnmu=-N/240",
            "required_nonlocal_slope": "d(delta_c_NL)/dlnmu=-N/240-64*pi^3*B_C3",
            "remaining_unknown": "one finite constant delta_c_fin at the matching scale",
        },
        "anchor_formula": "lambda/mu_m=exp[240*(32*pi^3*r_C3+delta_c_fin)/N]",
        "source_prescription": "delta_c_fin=0 at mu_m=k0=M_Pl is calculated as a conditional local-EFT branch only",
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "valid_for_full_MTS_claim": False,
        "claim_ceiling": "exact_tree_normalization_and_nonlocal_log_completion; finite_on_shell_conversion_not_derived",
    }
    RESULT_JSON.parent.mkdir(parents=True, exist_ok=True)
    RESULT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(f"{MARKER}_CHECKS={len(checks)}", flush=True)
    print(f"{MARKER}_PASSED={sum(bool(value) for value in checks.values())}", flush=True)
    print(
        f"{MARKER}_FAILED={sum(not bool(value) for value in checks.values())}",
        flush=True,
    )
    print(f"{MARKER}_RESULT_SHA256={digest(RESULT_JSON)}", flush=True)
    if not result["all_checks_pass"]:
        failed = [key for key, value in checks.items() if not value]
        print(f"{MARKER}_FAILED_IDS={','.join(failed)}", flush=True)
        return 1
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

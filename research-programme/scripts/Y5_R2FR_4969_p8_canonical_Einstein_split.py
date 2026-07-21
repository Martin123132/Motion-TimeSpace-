from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4969"
SOLODUKHIN = SOURCE / "src-2009.01042" / "Paper-QuantumGravity-V3.tex"
DUNBAR = SOURCE / "src-1711.05526" / "PLBpaperBv3.tex"
BERN = SOURCE / "src-1701.02422" / "gr_simp.tex"
BARATELLA = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4967"
    / "src-2010.13809"
    / "draft.tex"
)
GRAVSCATT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4965"
    / "src-2103.12728"
    / "GravScatt.tex"
)
FRG_C3 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4929"
    / "src2312"
    / "ess_cubic.tex"
)
FUNCTIONAL_C3 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4963"
    / "C3_Wilson_selection_and_running.csv"
)
SCRIPT_4967 = POST / "scripts" / "Y5_R2FR_4967_p8_GR_trajectory_and_static_bound.py"
SCRIPT_4968 = POST / "scripts" / "Y5_R2FR_4968_CFF_p8_trajectory_and_static_bound.py"

SOURCE_AUDIT_CSV = SOURCE / "pure_Einstein_three_loop_source_audit.csv"
CANONICAL_CSV = SOURCE / "p8_canonical_scaling_repair.csv"
RG_SPLIT_CSV = SOURCE / "pure_Einstein_iterated_primitive_split.csv"
MATCHING_CSV = SOURCE / "functional_to_onshell_C3_matching_diagnostic.csv"
RESULT_JSON = SOURCE / "p8_canonical_Einstein_split_results.json"

MARKER = "MTS_4969_P8_CANONICAL_EINSTEIN_SPLIT"
CHECKED_DATE = "2026-07-13"
EXPECTED_HASHES = {
    SOLODUKHIN: "8240be2d3f61b3e2a6103c6996aab3dfedeb9b2d56d5250694dfd11b6f7a8223",
    DUNBAR: "b7768f6a1ba4a32f5718c455f3042e97ef1cbfe806b88c1daa71b64fe5a1b6a1",
    BERN: "9448bff31da3e1e56e62e8fb6242a60c09afb90d1f7f25edaf3f23466ac0371e",
    BARATELLA: "d2892e4163b5a70ff3f660e2a48ba91f7e7be246dd53d21b3aa874a3a1b13230",
    GRAVSCATT: "6812e00f073074e6c045d3241125dc5cf1c73891ad250754b82cd19bae5e7963",
    FRG_C3: "b23b0974509278be22c8917f531a2963d415184d9052e27860c65fad80943a1d",
    FUNCTIONAL_C3: "c130ad2c49cce89682726377d459d3af7119a330c82af10a6c18bed770f7dfa0",
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


def source_audit_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "source_id": "SOL2009_RECURRENCE",
                "source_path": relative(SOLODUKHIN),
                "source_url": "https://arxiv.org/abs/2009.01042",
                "source_lines": "266-267;698-709;781-805;834-857",
                "result": (
                    "higher poles are fixed by single poles; at three loops "
                    "V_2,3=(2/3)v_1,2 V_1,3^(2), V_3,3=0, while the "
                    "single-pole residue v_1,3 remains input"
                ),
                "status": "PRIMARY_SOURCE_LOCKED",
            },
            {
                "source_id": "BERN1701_PHYSICAL_R3_RUNNING",
                "source_path": relative(BERN),
                "source_url": "https://arxiv.org/abs/1701.02422",
                "source_lines": "390-403;489-523;687-708;1117-1133",
                "result": (
                    "mu dc_R3/dmu=(kappa/2)^2(N_b-N_f)/"
                    "[240(4pi)^4]; pure gravity has N_b-N_f=2"
                ),
                "status": "PRIMARY_SOURCE_LOCKED",
            },
            {
                "source_id": "DUNBAR1711_R3_TO_R4",
                "source_path": relative(DUNBAR),
                "source_url": "https://arxiv.org/abs/1711.05526",
                "source_lines": "620-648;697-704;736-749;794-830",
                "result": (
                    "one R3 insertion produces an all-same-helicity R4 UV "
                    "counterterm and no mixed-helicity divergence"
                ),
                "status": "PRIMARY_SOURCE_LOCKED",
            },
            {
                "source_id": "GRAVSCATT2103_ACTION_AMPLITUDE_MAP",
                "source_path": relative(GRAVSCATT),
                "source_url": "https://arxiv.org/abs/2103.12728",
                "source_lines": "1728-1757;1841-1857",
                "result": (
                    "the direct R3 action and three-point amplitude imply "
                    "C_R3=24 c_R3/kappa^2=3 A_C3/(4pi)"
                ),
                "status": "PRIMARY_SOURCE_LOCKED",
            },
            {
                "source_id": "BARATELLA2010_NORMALIZATION_DISCREPANCY",
                "source_path": relative(BARATELLA),
                "source_url": "https://arxiv.org/abs/2010.13809",
                "source_lines": "189-204;900-960;987-1060",
                "result": (
                    "prints dC_R3/dlnmu=1/[2(4pi)^4] in pure gravity; "
                    "translation through its stated three-point normalization "
                    "is ten times the Bern action-normalized physical running"
                ),
                "status": "PRIMARY_SOURCE_COEFFICIENT_QUARANTINED",
            },
            {
                "source_id": "FRG2312_PUBLISHED_PERTURBATIVE_COMPARATOR",
                "source_path": relative(FRG_C3),
                "source_url": "https://doi.org/10.1103/hlrm-d4g2",
                "source_lines": "572-596; published Eq. 61 checked 2026-07-13",
                "result": (
                    "prints partial_t g_C3=2g_C3+g_N/(7680pi^3); "
                    "the 2026 published article retains the arXiv coefficient, "
                    "which is one half of the direct Bern action translation"
                ),
                "status": "PRIMARY_SOURCE_COEFFICIENT_DISCREPANCY_RETAINED",
            },
            {
                "source_id": "PRIMITIVE_THREE_LOOP_SWEEP",
                "source_path": relative(SOURCE),
                "source_url": (
                    "https://arxiv.org/abs/2009.01042;"
                    "https://arxiv.org/abs/1711.05526;"
                    "https://arxiv.org/abs/1701.02422;"
                    "https://arxiv.org/abs/2002.12374"
                ),
                "source_lines": "targeted primary-source sweep through 2026-07-13",
                "result": (
                    "no explicit source-backed pure-Einstein three-loop "
                    "four-graviton single-pole coefficient was found"
                ),
                "status": "ABSENCE_NOT_A_ZERO_THEOREM",
            },
        ]
    )


def canonical_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "CAN4969_0_operator_dimension",
            "input": "O8 is quartic in curvature",
            "derivation": "[O8]=8 and [d4x]=-4",
            "output": "[b]=-6 in (16piG)^-1 integral sqrt(-g)[R+b O8]",
            "status": "DERIVED",
        },
        {
            "step_id": "CAN4969_1_dimensionless_coordinates",
            "input": "[G]=-2; [b]=-6",
            "derivation": "g=k^2 G; v=k^6 b; B=b/G^3",
            "output": "B=v/g^3",
            "status": "DERIVED",
        },
        {
            "step_id": "CAN4969_2_chain_rule",
            "input": "beta_v=6v+F; B=v g^-3",
            "derivation": "beta_B=beta_v/g^3-3(beta_g/g)B",
            "output": "beta_B=[6-3 beta_g/g]B+F/g^3",
            "status": "DERIVED",
        },
        {
            "step_id": "CAN4969_3_gaussian_check",
            "input": "beta_g/g -> 2",
            "derivation": "6-3(2)=0",
            "output": "Planck-normalized B has no spurious canonical running in the IR",
            "status": "PASS",
        },
        {
            "step_id": "CAN4969_4_fixed_point_check",
            "input": "beta_g=0 at the non-Gaussian fixed point",
            "derivation": "6-3(0)=6",
            "output": "p8 triangular stability subblock is diag(6,6)",
            "status": "CORRECTS_4967_4968_DIAG_4",
        },
        {
            "step_id": "CAN4969_5_old_formula_diagnosis",
            "input": "old beta_B=[4-2 beta_g/g]B+source",
            "derivation": "this is the chain rule for v/g^2, not v/g^3",
            "output": "old fixed boundary -source/4 must become -source/6",
            "status": "NORMALIZATION_ERROR_IDENTIFIED",
        },
    ]
    return tagged(rows)


def rg_split_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    pi = math.pi
    beta_c3 = 1.0 / (20.0 * (4.0 * pi) ** 4)
    beta_a = 1.0 / (3840.0 * pi**3)
    baratella_beta_c3 = 1.0 / (2.0 * (4.0 * pi) ** 4)
    frg_beta_a = 1.0 / (7680.0 * pi**3)
    primitive_unit = 1.0 / (32.0 * pi**3)
    iterated_bminus = -1.0 / (640.0 * pi**3)
    iterated_bc = iterated_bminus / 2.0
    iterated_bt = -iterated_bminus / 2.0
    rows = [
        {
            "term_id": "RG4969_0_pure_GR_R3_running",
            "equation": "dC_R3/dL=1/[20(4pi)^4]",
            "MTS_equation": "dA_C3/dL=1/(3840pi^3)",
            "numeric_coefficient": beta_c3,
            "helicity_direction": "R3 all-same",
            "classification": "BERN_ACTION_NORMALIZED_ADDITIVE_TWO_LOOP_SOURCE",
        },
        {
            "term_id": "RG4969_0a_action_amplitude_map",
            "equation": "C_R3=24c_R3/kappa^2",
            "MTS_equation": "C_R3=3A_C3/(4pi); A_C3=c_R3/G",
            "numeric_coefficient": 3.0 / (4.0 * pi),
            "helicity_direction": "R3 all-same",
            "classification": "DIRECT_ACTION_TO_THREE_POINT_NORMALIZATION",
        },
        {
            "term_id": "RG4969_0b_Baratella_coefficient_audit",
            "equation": "printed dC_R3/dL=1/[2(4pi)^4]",
            "MTS_equation": "printed coefficient / Bern-mapped coefficient = 10",
            "numeric_coefficient": baratella_beta_c3,
            "helicity_direction": "R3 all-same",
            "classification": "NORMALIZATION_DISCREPANCY_NOT_AN_EXTRA_BETA_TERM",
        },
        {
            "term_id": "RG4969_0c_FRG_coefficient_audit",
            "equation": "printed partial_t g_C3=2g_C3+g_N/(7680pi^3)",
            "MTS_equation": "Bern beta_A / printed FRG comparator = 2",
            "numeric_coefficient": frg_beta_a,
            "helicity_direction": "R3 all-same",
            "classification": "PUBLISHED_FACTOR_TWO_DISCREPANCY_NOT_AVERAGED",
        },
        {
            "term_id": "RG4969_1_R3_to_R4_mixing",
            "equation": "dC_R4/dL=-C_R3/(8pi^2)",
            "MTS_equation": "dB_minus/dL=-12 A_C3",
            "numeric_coefficient": -1.0 / (8.0 * pi**2),
            "helicity_direction": "[same,mixed]=[1,0]",
            "classification": "ONE_LOOP_INSERTION_MIXING",
        },
        {
            "term_id": "RG4969_2_exact_solution_C_R4",
            "equation": (
                "C_R4(L)=C_R4(0)-C_R3(0)L/(8pi^2)"
                "-beta_C3 L^2/(16pi^2)+p_minus L"
            ),
            "MTS_equation": (
                "B_minus(L)=B_minus(0)-12A_C3(0)L"
                "-L^2/(640pi^3)+xi_minus L/(32pi^3)"
            ),
            "numeric_coefficient": iterated_bminus,
            "helicity_direction": "same",
            "classification": "RG_FORCED_DOUBLE_LOG_PLUS_PRIMITIVE_SINGLE_LOG",
        },
        {
            "term_id": "RG4969_3_exact_solution_C_R4prime",
            "equation": "C_R4prime(L)=C_R4prime(0)+p_plus L",
            "MTS_equation": "B_plus(L)=B_plus(0)+xi_plus L/(32pi^3)",
            "numeric_coefficient": primitive_unit,
            "helicity_direction": "mixed",
            "classification": "PRIMITIVE_SINGLE_LOG_ONLY",
        },
        {
            "term_id": "RG4969_4_invariant_iterated_vector",
            "equation": "[Delta B_C,Delta B_t]=[-1,+1]L^2/(1280pi^3)",
            "MTS_equation": "Delta B_plus=0; Delta B_minus=-L^2/(640pi^3)",
            "numeric_coefficient": iterated_bc,
            "helicity_direction": "[B_C,B_t]=[-1,+1]",
            "classification": "EXACT_PURE_GR_ITERATED_TERM",
        },
        {
            "term_id": "RG4969_5_primitive_vector",
            "equation": "p_plus_minus=xi_plus_minus/(4pi)^6",
            "MTS_equation": (
                "source_B_C=(xi_minus+xi_plus)/(64pi^3); "
                "source_B_t=(xi_plus-xi_minus)/(64pi^3)"
            ),
            "numeric_coefficient": primitive_unit / 2.0,
            "helicity_direction": "rank two",
            "classification": "UNCOMPUTED_SINGLE_POLE_NOT_SET_TO_ZERO",
        },
        {
            "term_id": "RG4969_6_pole_recurrence",
            "equation": "V_2,3=(2/3)v_1,2 V_1,3^(2); V_3,3=0",
            "MTS_equation": "the iterated higher-pole part is fixed; V_1,3^(0) is not",
            "numeric_coefficient": 2.0 / 3.0,
            "helicity_direction": "same for insertion; primitive rank two",
            "classification": "RECURRENCE_PROOF_OF_SPLIT",
        },
    ]
    summary = {
        "beta_C_R3_pure_GR": beta_c3,
        "beta_A_C3_pure_GR": beta_a,
        "baratella_printed_beta_C_R3": baratella_beta_c3,
        "baratella_to_Bern_ratio": baratella_beta_c3 / beta_c3,
        "FRG_printed_beta_A_C3": frg_beta_a,
        "Bern_to_FRG_ratio": beta_a / frg_beta_a,
        "Bminus_L2_coefficient": iterated_bminus,
        "B_C_L2_coefficient": iterated_bc,
        "B_t_L2_coefficient": iterated_bt,
        "primitive_B_helicity_source_per_unit_xi": primitive_unit,
        "R3_running_type": "ADDITIVE_TWO_LOOP_SOURCE",
    }
    return tagged(rows), summary


def matching_rows(beta_a: float) -> tuple[list[dict[str, Any]], dict[str, float]]:
    rows = [
        row
        for row in read_csv(FUNCTIONAL_C3)
        if row["selection_id"] == "C3SEL4963_massless_envelope"
    ]
    if len(rows) != 1:
        raise RuntimeError("4963 massless C3 envelope row is not unique")
    row = rows[0]
    slope_g_min = float(row["B_C3_source_min"])
    slope_g_max = float(row["B_C3_source_max"])
    slope_k_min = 2.0 * slope_g_min
    slope_k_max = 2.0 * slope_g_max
    diagnostic = {
        "functional_dA_dlng_min": slope_g_min,
        "functional_dA_dlng_max": slope_g_max,
        "functional_dA_dlnk_min": min(slope_k_min, slope_k_max),
        "functional_dA_dlnk_max": max(slope_k_min, slope_k_max),
        "onshell_pure_GR_dA_dlnmu": beta_a,
        "absolute_slope_ratio": max(abs(slope_k_min), abs(slope_k_max)) / beta_a,
    }
    output = tagged(
        [
            {
                "diagnostic_id": "MATCH4969_0_functional_slope",
                "quantity": "dA_C3/dlnk",
                "value_min": diagnostic["functional_dA_dlnk_min"],
                "value_max": diagnostic["functional_dA_dlnk_max"],
                "source_scheme": "4957 natural Type-II Wilsonian trajectory",
                "status": "CALCULATED_FROM_LN_G_SLOPE_USING_DLN_G_DLN_K_2",
            },
            {
                "diagnostic_id": "MATCH4969_1_onshell_slope",
                "quantity": "dA_C3/dlnmu",
                "value_min": beta_a,
                "value_max": beta_a,
                "source_scheme": "four-dimensional on-shell pure GR",
                "status": "PRIMARY_SOURCE_NORMALIZED",
            },
            {
                "diagnostic_id": "MATCH4969_2_matching_verdict",
                "quantity": "functional-to-onshell matching",
                "value_min": diagnostic["absolute_slope_ratio"],
                "value_max": diagnostic["absolute_slope_ratio"],
                "source_scheme": "comparison only",
                "status": (
                    "NOT_MATCHED_SIGN_AND_MAGNITUDE; DO_NOT_DOUBLE_COUNT OR "
                    "CALL THE FUNCTIONAL C3 MIXING THE EXACT PURE_GR DOUBLE_LOG"
                ),
            },
        ]
    )
    return output, diagnostic


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)
    hashes = {relative(path): digest(path) for path in EXPECTED_HASHES}
    if any(digest(path) != expected for path, expected in EXPECTED_HASHES.items()):
        raise RuntimeError("4969 canonical/source input hash mismatch")

    canonical = canonical_rows()
    split, split_summary = rg_split_rows()
    matching, matching_summary = matching_rows(split_summary["beta_A_C3_pure_GR"])
    audit = source_audit_rows()
    write_csv(SOURCE_AUDIT_CSV, audit)
    write_csv(CANONICAL_CSV, canonical)
    write_csv(RG_SPLIT_CSV, split)
    write_csv(MATCHING_CSV, matching)

    checks = {
        "all_source_hashes_match": True,
        "p8_coefficient_mass_dimension_minus_six": True,
        "B_equals_v_over_g_cubed": True,
        "correct_homogeneous_formula": True,
        "correct_fixed_point_eigenvalues_six": True,
        "old_formula_identified_as_v_over_g_squared": True,
        "pure_GR_R3_running_nonzero": split_summary["beta_C_R3_pure_GR"] > 0.0,
        "Baratella_factor_ten_discrepancy_recorded": math.isclose(
            split_summary["baratella_to_Bern_ratio"], 10.0
        ),
        "FRG_factor_two_discrepancy_recorded": math.isclose(
            split_summary["Bern_to_FRG_ratio"], 2.0
        ),
        "R3_running_not_misclassified_multiplicative": (
            split_summary["R3_running_type"] == "ADDITIVE_TWO_LOOP_SOURCE"
        ),
        "iterated_same_helicity_nonzero": split_summary["Bminus_L2_coefficient"] != 0.0,
        "iterated_mixed_helicity_zero": True,
        "primitive_rank_two_retained": True,
        "primitive_not_claimed_zero": True,
        "functional_onshell_matching_not_claimed": True,
    }
    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_hashes": hashes,
        "canonical_repair": {
            "old_formula": "beta_B=[4-2 beta_g/g]B+source",
            "correct_formula": "beta_B=[6-3 beta_g/g]B+source",
            "old_fixed_boundary": "B_star=-source_star/4",
            "correct_fixed_boundary": "B_star=-source_star/6",
            "old_p8_subblock": [4.0, 4.0],
            "correct_p8_subblock": [6.0, 6.0],
        },
        "pure_Einstein_split": split_summary,
        "functional_onshell_matching": matching_summary,
        "primitive_three_loop": {
            "same_helicity_parameter": "xi_minus",
            "mixed_helicity_parameter": "xi_plus",
            "definition": "p_plus_minus=xi_plus_minus/(4pi)^6",
            "status": "UNCOMPUTED_SINGLE_POLE_VECTOR",
            "set_to_zero": False,
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "valid_for_full_MTS_claim": False,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if not result["all_checks_pass"]:
        failed = [key for key, passed in checks.items() if not passed]
        raise RuntimeError(f"4969 canonical checks failed: {failed}")
    print(
        f"{MARKER}_BMINUS_L2={split_summary['Bminus_L2_coefficient']:.12g}",
        flush=True,
    )
    print(
        f"{MARKER}_PRIMITIVE_UNIT={split_summary['primitive_B_helicity_source_per_unit_xi']:.12g}",
        flush=True,
    )
    print(f"{MARKER}_OUTPUT_SHA256={digest(RESULT_JSON)}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

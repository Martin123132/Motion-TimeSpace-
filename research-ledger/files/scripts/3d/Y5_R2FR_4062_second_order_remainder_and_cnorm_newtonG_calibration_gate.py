from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4062-Y5-R2FR-second-order-remainder-and-cnorm-newtonG-calibration-gate.md"

DECISION = "QUADRATIC_REMAINDER_ZERO_IF_LOCAL_FIXED_POINT_ELSE_BOUND_CNORM_ROUTED_TO_CALIBRATED_NEWTON_G"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4062_00_4061_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4061_NEXT_TARGET.csv",
        "quadratic remainder plus universal source-normalization/Newton-G calibration",
        "4061 selects the second-order/c_norm calibration gate.",
    ),
    "SRC4062_01_4060_quad": (
        SOURCE_DIR / "P8_Y5_R2FR_4060_CHAIN_FALLBACK_BOUND_VECTOR.csv",
        "CB4060_2_quadratic_remainder",
        "4060 leaves a finite second-order remainder if the fixed-point perturbation is not exactly zero.",
    ),
    "SRC4062_02_4047_zero": (
        SOURCE_DIR / "P8_Y5_R2FR_4047_SELECTED_ZERO_THEOREM.csv",
        "CZT4047_4_total_zero",
        "4047 supplies the private selected-branch c_norm zero theorem.",
    ),
    "SRC4062_03_4047_split": (
        SOURCE_DIR / "P8_Y5_R2FR_4047_CNORM_COMPONENT_DECOMPOSITION.csv",
        "CN4047_3_total",
        "4047 decomposes c_norm into G_obs, M_eff, and epsilon_mu derivative channels.",
    ),
    "SRC4062_04_4047_calibration": (
        SOURCE_DIR / "P8_Y5_R2FR_4047_ZEROED_CHANNEL_ROLLUP.csv",
        "ROLL4047_7_calibration",
        "4047 distinguishes harmless constant calibration from derivative hair.",
    ),
    "SRC4062_05_4046_memory": (
        SOURCE_DIR / "P8_Y5_R2FR_4046_TAIL_ZERO_THEOREM.csv",
        "TZT4046_1_zero_amplitude",
        "4046 gives local reset/no-incoming memory zero for the compact branch.",
    ),
    "SRC4062_06_4056_newton": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_CONDITIONAL_LOCAL_GR_THEOREM.csv",
        "LGT4056_1_Newton",
        "4056 states the calibrated Newton/Poisson limit of the packet.",
    ),
    "SRC4062_07_4056_adoption": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_PACKET_ADOPTION_GATE.csv",
        "ADOPT4056_4_side_channels",
        "4056 records the side-channel adoption clause needed for c_norm/memory silence.",
    ),
    "SRC4062_08_newton_stack": (
        SOURCE_DIR / "P8_source_normalized_Newton_branch_STACK.csv",
        "SN7_constant_universal_Geff",
        "older Newton branch stack identifies constant universal G_eff as the coupling gate.",
    ),
    "SRC4062_09_norm_stack": (
        SOURCE_DIR / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
        "S5_Newton_gate",
        "source-normalization stack records the older Newton gate and its failure mode.",
    ),
    "SRC4062_10_4038_cnorm": (
        SOURCE_DIR / "P8_Y5_R2FR_4038_REMAINING_LOCAL_RESIDUAL_VECTOR.csv",
        "route common mode into calibrated kappa_obs/Newton G",
        "4038 already identified the correct treatment of c_norm common mode.",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4062_SOURCE_REGISTER.csv",
    "quadratic_gate": SOURCE_DIR / "P8_Y5_R2FR_4062_QUADRATIC_REMAINDER_GATE.csv",
    "cnorm_calibration": SOURCE_DIR / "P8_Y5_R2FR_4062_CNORM_NEWTON_G_CALIBRATION_LAW.csv",
    "newton_reduction": SOURCE_DIR / "P8_Y5_R2FR_4062_NEWTON_GR_REDUCTION_CONTRACT.csv",
    "fallback_bounds": SOURCE_DIR / "P8_Y5_R2FR_4062_FALLBACK_BOUND_VECTOR.csv",
    "decision": SOURCE_DIR / "P8_Y5_R2FR_4062_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4062_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4062_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4062_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4062_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows(current_timestamp: str) -> List[Dict[str, object]]:
    source_table: List[Dict[str, object]] = []
    for source_id, source_tuple in SOURCES.items():
        path, needle, role = source_tuple
        text = read_text(path)
        source_table.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": current_timestamp,
            }
        )
    return source_table


def quadratic_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "QRG4062_0_normal_order",
            "object": "Gamma_ren",
            "law": "Gamma_ren(Y_* + deltaY) = 1/2 H_AB deltaY^A deltaY^B + O(deltaY^3)",
            "selected_branch_condition": "local fixed point/reset branch has deltaY=0 in the compact stationary collar",
            "selected_branch_result": "Delta_K_quad = 0",
            "fallback_if_unsigned": "Q_quad <= C_Ploc C_2 |deltaY| |nabla deltaY| / L_*^2",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "gate_id": "QRG4062_1_reset_support",
            "object": "deltaY",
            "law": "deltaY collects memory tail, source-normalization, chain, domain, boundary, and nonEH local deviations",
            "selected_branch_condition": "4046 reset, 4047 c_norm zero, 4060 chain first variation, and 4061 CDB kernel zeros are adopted together",
            "selected_branch_result": "all first-order drivers of finite deltaY vanish in the compact branch",
            "fallback_if_unsigned": "finite amplitude and Hessian rows are required before R10/PPN claims",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "gate_id": "QRG4062_2_guard",
            "object": "second-order safety",
            "law": "zero first variation is not by itself a full finite-amplitude proof",
            "selected_branch_condition": "exact fixed point deltaY=0 or a real small-amplitude bound with declared norm",
            "selected_branch_result": "selected branch may set Q_quad=0 only under exact local fixed-point/reset data",
            "fallback_if_unsigned": "retain Q_quad as explicit second-order error term",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def cnorm_calibration_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "law_id": "CNG4062_0_constant_allowed",
            "object": "G_N calibration",
            "formula": "G_N := c^4 kappa_eff/(8*pi), with kappa_eff = kappa_* Z_0",
            "meaning": "a single universal constant calibration is allowed; GR also treats G as an empirical coupling",
            "selected_branch_result": "no numerical prediction of G_N is claimed or required for reduction to GR/Newton",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "law_id": "CNG4062_1_derivatives_forbidden",
            "object": "c_norm derivative hair",
            "formula": "Delta_cnorm = |D ln G_obs| + |D ln M_eff| + |D ln(1+epsilon_mu)|",
            "meaning": "time, radial, range, species, frame, domain, and memory derivatives cannot be hidden inside measured GM",
            "selected_branch_result": "Delta_cnorm_selected = 0 from fixed coupling, same Hilbert source, no source-prefactor, reset, and q-basic projector/domain clauses",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "law_id": "CNG4062_2_calibration_firewall",
            "object": "readout firewall",
            "formula": "calibrate constant G_N once; forbid D_source G_N, D_r G_N, D_t G_N, D_species G_N, and D_frame G_N",
            "meaning": "measured-GM fitting cannot launder a fifth force, WEP violation, Gdot, or range-dependent coupling",
            "selected_branch_result": "universal constant common mode is routed to Newton G; all nonconstant c_norm rows are zero or bounded",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def newton_reduction_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "contract_id": "NRC4062_0_EH_source",
            "requirement": "EH 00 equation and same Hilbert source",
            "formula": "G_00^(1) = kappa_eff T_00 -> nabla^2 Phi = 4*pi*G_N*rho_H",
            "if_satisfied": "Newton/Poisson limit follows with calibrated G_N",
            "if_failed": "not a GR/Newton reduction; route failed term to fallback residual",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "contract_id": "NRC4062_1_Gauss_GM",
            "requirement": "one conserved source mass and no extra monopole",
            "formula": "mu_obs = G_N M_H + mu_extra, with mu_extra=0 in the selected branch",
            "if_satisfied": "Kepler/orbital GM is the same Hilbert mass that sources the metric",
            "if_failed": "fill boundary/domain/memory/nonEH/source-charge residual rows",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "contract_id": "NRC4062_2_no_derivative_hair",
            "requirement": "constant universal coupling",
            "formula": "partial_t,r,lambda,A,frame G_N = 0 and partial_t,r,A,frame M_H = 0 in the compact exterior",
            "if_satisfied": "local Newton branch is not a fitted plateau; it is a constant-coupling limit",
            "if_failed": "compare against Gdot, R10/inverse-square, WEP, clocks, and orbital residual bounds",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "contract_id": "NRC4062_3_PPN_next",
            "requirement": "second-order weak-field readout",
            "formula": "gamma=1, beta=1, alpha_i=xi=zeta_i=0 after the same calibrated G_N normalization",
            "if_satisfied": "candidate local GR branch can move from packet theorem to explicit PPN readout",
            "if_failed": "PPN residual vector stays active",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def fallback_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "FB4062_0_quadratic",
            "used_if": "local fixed point/reset data are not exact",
            "bound_formula": "Q_quad <= C_Ploc C_2 |deltaY| |nabla deltaY| / L_*^2",
            "arena_links": "finite second-order Delta_K residual; PPN beta/gamma; R10 alpha(lambda)",
            "needed_inputs": "Hessian norm C_2, amplitude deltaY, gradient scale, L_*",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "bound_id": "FB4062_1_Gdot",
            "used_if": "fixed universal coupling branch is rejected",
            "bound_formula": "|partial_t ln G_N| <= epsilon_Gdot",
            "arena_links": "orbital ephemerides, clocks, pulsars, cosmology consistency",
            "needed_inputs": "time-window, clock/orbital convention, source-backed Gdot bound",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "bound_id": "FB4062_2_range",
            "used_if": "range/radial derivative hair survives",
            "bound_formula": "|partial_r ln mu_obs| + |partial_lambda ln G_N| <= epsilon_range",
            "arena_links": "R10 inverse-square, orbital residuals, galaxy/local separation guard",
            "needed_inputs": "radial profile, lambda convention, alpha(lambda) comparison",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "bound_id": "FB4062_3_species",
            "used_if": "source/species normalization is not source-label blind",
            "bound_formula": "|Delta ln G_A - Delta ln G_B| <= epsilon_WEP",
            "arena_links": "WEP/Eotvos, composition dependence, clocks",
            "needed_inputs": "species labels, source action weights, WEP projection map",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "bound_id": "FB4062_4_master",
            "used_if": "any second-order or c_norm clause is unsigned",
            "bound_formula": "Delta_local_calib <= Q_quad + epsilon_Gdot + epsilon_range + epsilon_WEP + epsilon_frame + epsilon_extra",
            "arena_links": "no-cancellation local calibration residual",
            "needed_inputs": "all rows above plus frame/nonEH/source-extra residuals",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def static_rows(current_timestamp: str) -> Dict[str, List[Dict[str, object]]]:
    return {
        "decision": [
            {
                "decision_id": "DEC4062_0",
                "decision": DECISION,
                "physics_meaning": "MTS may reduce to GR/Newton with one calibrated universal G_N, but not with hidden time/range/source/species derivative hair",
                "selected_branch": "Q_quad=0 and Delta_cnorm=0 if exact fixed-point/reset and fixed-coupling same-source clauses are parent-adopted",
                "fallback_branch": "finite quadratic and c_norm derivative bounds remain active if any clause is rejected",
                "valid_for_public_claim": False,
                "timestamp_utc": current_timestamp,
            }
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4062_0",
                "claim": "selected parent branch has calibrated Newton-G common mode with no c_norm derivative hair",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "conditional on parent packet adoption and exact local fixed-point/reset data",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4062_1",
                "claim": "MTS predicts the numerical value of Newton's constant",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "4062 routes one universal constant to empirical calibration; no absolute numerical G derivation is claimed",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4062_2",
                "claim": "MTS publicly derives full local GR/PPN",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "explicit weak-field PPN beta/gamma/readout calculation and formal adoption remain",
                "timestamp_utc": current_timestamp,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4062_0",
                "next_doc": "4063-Y5-R2FR-explicit-EH-weak-field-newton-ppn-readout-contract.md",
                "next_script": "scripts/Y5_R2FR_4063_explicit_EH_weak_field_newton_ppn_readout_contract.py",
                "reason": "after calibration law, explicitly derive the weak-field EH-to-Newton/PPN readout with the same Hilbert source and calibrated G_N",
                "timestamp_utc": current_timestamp,
            }
        ],
        "status": [
            {
                "status_id": "STAT4062",
                "status": "CNORM_ROUTED_TO_CALIBRATED_NEWTON_G_QUADRATIC_GUARD_ACTIVE_PUBLIC_CLAIM_BLOCKED",
                "local_GR_claim": False,
                "public_claim": False,
                "timestamp_utc": current_timestamp,
            }
        ],
    }


def validate_sources(source_table: List[Dict[str, object]]) -> Tuple[bool, str]:
    missing = [row["source_id"] for row in source_table if not row["exists"]]
    absent_needles = [row["source_id"] for row in source_table if not row["needle_found"]]
    if missing or absent_needles:
        return False, f"missing={missing}; absent_needles={absent_needles}"
    return True, "all cited source paths exist and needles are present"


def validate_csv_parse(paths: Iterable[Path]) -> Tuple[bool, str]:
    details: List[str] = []
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as input_file:
                parsed_rows = list(csv.DictReader(input_file))
            details.append(f"{path.name}:rows={len(parsed_rows)}")
    except Exception as exc:  # pragma: no cover
        return False, repr(exc)
    return True, "; ".join(details)


def validate_no_public_claim(row_groups: Iterable[List[Dict[str, object]]]) -> Tuple[bool, str]:
    offenders: List[str] = []
    for rows in row_groups:
        for row in rows:
            for key in ("valid_for_public_claim", "allowed_public", "public_claim", "local_GR_claim"):
                if key in row and str(row[key]).lower() == "true":
                    offenders.append(str(row))
    if offenders:
        return False, f"public claim flags found: {offenders}"
    return True, "all claim-bearing rows preserve public false"


def validate_script_compile() -> Tuple[bool, str]:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError as exc:
        return False, str(exc)
    return True, "script compiles"


def validation_rows(
    source_table: List[Dict[str, object]],
    generated_csvs: List[Path],
    row_groups: List[List[Dict[str, object]]],
) -> List[Dict[str, object]]:
    source_ok, source_detail = validate_sources(source_table)
    csv_ok, csv_detail = validate_csv_parse(generated_csvs)
    claims_ok, claims_detail = validate_no_public_claim(row_groups)
    compile_ok, compile_detail = validate_script_compile()
    formal_outputs = list(FORMALIZATION.rglob("*4062*")) if FORMALIZATION.exists() else []
    joined_rows = str(row_groups)
    return [
        {"check_id": "VAL4062_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4062_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4062_02_no_public_claim", "passed": claims_ok, "detail": claims_detail},
        {
            "check_id": "VAL4062_03_decision",
            "passed": DECISION in joined_rows,
            "detail": "decision records quadratic fixed-point fork and c_norm Newton-G calibration",
        },
        {
            "check_id": "VAL4062_04_no_numerical_G_claim",
            "passed": "no absolute numerical G derivation is claimed" in joined_rows,
            "detail": "absolute G prediction is explicitly forbidden",
        },
        {
            "check_id": "VAL4062_05_derivative_firewall",
            "passed": "D_source G_N" in joined_rows and "epsilon_WEP" in joined_rows,
            "detail": "time/range/source/species derivative hair is routed to zero-or-bound rows",
        },
        {
            "check_id": "VAL4062_06_no_formalization_outputs",
            "passed": len(formal_outputs) == 0,
            "detail": "4062 writes only post-checkpoint/source-intake outputs" if not formal_outputs else str(formal_outputs),
        },
        {"check_id": "VAL4062_07_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4062 - Second-Order Remainder and c_norm/Newton-G Calibration Gate

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Formalization modified: `false`
- Public local-GR claim: `false`

## Result

4062 separates two things that must not be mixed:

1. a constant universal calibration of Newton's constant;
2. forbidden derivative hair hidden inside measured `GM`.

The selected branch law is:

```text
G_N := c^4 kappa_eff/(8*pi),    kappa_eff = kappa_* Z_0
Delta_cnorm = |D ln G_obs| + |D ln M_eff| + |D ln(1+epsilon_mu)|.
```

A constant `G_N` is allowed as calibration. GR itself does not derive the numerical value of `G`; it uses one empirically calibrated universal coupling. The MTS requirement is therefore not "predict G's number today"; it is:

```text
D_t G_N = D_r G_N = D_lambda G_N = D_species G_N = D_frame G_N = 0
```

inside the compact local branch, unless a bound row is supplied.

## Second-Order Guard

After 4060 normal-ordering:

```text
Gamma_ren(Y_* + deltaY) = 1/2 H_AB deltaY^A deltaY^B + O(deltaY^3).
```

If the local fixed-point/reset branch gives exact `deltaY=0`, then `Q_quad=0`. If not, the branch keeps:

```text
Q_quad <= C_Ploc C_2 |deltaY| |nabla deltaY| / L_*^2.
```

## What Moved

The Newton/GR route is now cleaner:

- one universal constant coupling may be calibrated;
- nonconstant `Gdot`, radial/range dependence, WEP/species dependence, frame drift, and extra monopoles are not calibration and must be zero or bounded;
- the next job is an explicit EH weak-field readout showing Poisson/Newton and PPN use the same Hilbert source and calibrated `G_N`.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    quadratic_gate = quadratic_gate_rows(current_timestamp)
    cnorm_calibration = cnorm_calibration_rows(current_timestamp)
    newton_reduction = newton_reduction_rows(current_timestamp)
    fallback = fallback_rows(current_timestamp)
    static = static_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["quadratic_gate"], quadratic_gate)
    write_csv(OUTPUTS["cnorm_calibration"], cnorm_calibration)
    write_csv(OUTPUTS["newton_reduction"], newton_reduction)
    write_csv(OUTPUTS["fallback_bounds"], fallback)
    write_csv(OUTPUTS["decision"], static["decision"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["quadratic_gate"],
        OUTPUTS["cnorm_calibration"],
        OUTPUTS["newton_reduction"],
        OUTPUTS["fallback_bounds"],
        OUTPUTS["decision"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    all_row_groups = [
        sources,
        quadratic_gate,
        cnorm_calibration,
        newton_reduction,
        fallback,
        static["decision"],
        static["claim_gate"],
        static["next_target"],
        static["status"],
    ]
    validation = validation_rows(sources, generated_csvs, all_row_groups)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"decision: {DECISION}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()

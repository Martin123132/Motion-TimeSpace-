from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3907"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3907-Y5-R2FR-Gstar-from-MTS-scales-or-measured-coupling-policy-runner.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3907_SOURCE_REGISTER.csv",
    "candidate_map": SRC / "P8_Y5_R2FR_3907_GSTAR_SCALE_CANDIDATE_MAP.csv",
    "no_go": SRC / "P8_Y5_R2FR_3907_GSTAR_UNDERDETERMINATION_LEMMA.csv",
    "policy": SRC / "P8_Y5_R2FR_3907_MEASURED_COUPLING_POLICY_RUNNER.csv",
    "derivatives": SRC / "P8_Y5_R2FR_3907_GSTAR_DERIVATIVE_ZERO_GATES.csv",
    "decision": SRC / "P8_Y5_R2FR_3907_BRANCH_DECISION.csv",
    "next": SRC / "P8_Y5_R2FR_3907_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3907_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3907_VALIDATION.csv",
}

SCALE_CANDIDATE = "kappa_* ?= N_top * kappa_MTS * w_common * ell_J * R_frame * C_extra"
NO_GO_LEMMA = (
    "local GR/Newton reduction fixes only the product kappa_* T_H; "
    "an absolute value for G_* is underdetermined until a parent action normalization, "
    "source-current unit, and Hilbert mass calibration are independently fixed"
)
MEASURED_POLICY = (
    "G_* may be a measured superselected coupling: claim derivative/source/range silence if proved, "
    "but do not claim prediction of the numerical value of G"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    return str(path.relative_to(PCW)) if path.is_relative_to(PCW) else str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3907_00_next", SRC / "P8_Y5_R2FR_3906_NEXT_TARGET.csv", "NEXT3906_0", "3906 selected Gstar scale target"),
        ("SRC3907_01_gstar", SRC / "P8_Y5_R2FR_3906_GSTAR_OWNER_MATRIX.csv", "G3906_3_derivation_target", "3906 Gstar derivation target"),
        ("SRC3907_02_residuals", SRC / "P8_Y5_R2FR_3906_NON_EH_AND_GSTAR_RESIDUAL_ROWS.csv", "RES3906_1_Gdot", "3906 active Gstar residual rows"),
        ("SRC3907_03_ellJ", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_0_total", "ellJ source-current owner residual law"),
        ("SRC3907_04_product", SRC / "P8_EM_product_lock_factor_vector_ellJ_Rframe.csv", "PLFV3512_5_Z_product", "G/w/ellJ/frame/source product factor"),
        ("SRC3907_05_y5y6", SRC / "P8_Y5_Y6_source_coupling_lock_status.csv", "STAT3541_3_next", "Y5/Y6 source coupling lock status"),
        ("SRC3907_06_source_current", SRC / "P8_source_current_Ward_universality_CONTRACT.csv", "SC3_universal_kappa_coupling", "source current Ward universality"),
        ("SRC3907_07_ward", SRC / "P8_Ward_source_owner_identity_CONTRACT.csv", "C4_constant_universal_coupling", "Ward source owner identity"),
        ("SRC3907_08_worldtube", SRC / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_WORLDTUBE_HILBERT_COUPLING_SELECTOR_THEOREM.csv", "WSC2577_6_coupling_baseline_zero", "worldtube Hilbert coupling selector"),
        ("SRC3907_09_kappa_contract", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU6_constant_only_calibration_policy", "constant-only calibration policy"),
        ("SRC3907_10_global_superselection", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS6_constant_offset_policy", "global coupling constant offset policy"),
        ("SRC3907_11_validation", SRC / "P8_Y5_BRR545_3906_VALIDATION.csv", "VAL3906_15_next_target", "3906 validation"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": found,
                "role": role,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def candidate_map_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "GMAP3907_0_product",
            "candidate": SCALE_CANDIDATE,
            "meaning": "only known plausible product chain joining EH coupling, source-current normalization, action scale and frame/source factors",
            "status": "CANDIDATE_MAP_NOT_DERIVED",
            "failure": "N_top, kappa_MTS, w_common, ell_J, R_frame and C_extra are not all parent-owned with units and no fitted-GM dependence",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GMAP3907_1_ellJ",
            "candidate": "ell_J fixes current normalization J_M=ell_J T_H[tau]",
            "meaning": "ell_J can cancel in Hilbert mass readout only if fixed before readout and not fitted from orbital GM",
            "status": "CONDITIONAL_FACTOR_UNSIGNED",
            "failure": "Pi_M/H_tau/reference/frame chain still carries residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GMAP3907_2_kappa",
            "candidate": "kappa_MTS or kappa_* as parent action prefactor",
            "meaning": "can own the GR coupling but does not compute its value without a normalization law",
            "status": "OWNER_NOT_VALUE_DERIVATION",
            "failure": "no inspected source supplies kappa_*=F(MTS primitive scales)",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GMAP3907_3_topological",
            "candidate": "N_top/topological charge fixes absolute normalization",
            "meaning": "would be the strongest route because an integer/cohomology class could remove continuous fitting",
            "status": "OPEN_NO_SOURCE_ROW",
            "failure": "current rows use topological/source class conditionally but not as an absolute G normalization",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def no_go_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "lemma_id": "NG3907_0_statement",
            "statement": NO_GO_LEMMA,
            "proof_sketch": "rescale kappa_* -> lambda kappa_* and T_H -> T_H/lambda by changing source-current normalization; the field equation and orbital GM product are unchanged until source units are fixed independently",
            "consequence": "a local GR/Newton recovery can validate the coupling product but cannot by itself predict numerical G",
            "status": "UNDERDETERMINATION_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "lemma_id": "NG3907_1_anti_circularity",
            "statement": "measured orbital GM cannot be used as both input source mass and proof of G_*",
            "proof_sketch": "choosing G_* or ell_J from the same exterior motion being explained makes the Newton bridge tautological",
            "consequence": "G_* value claim requires parent scale map or independent metrology/source calibration",
            "status": "ANTI_CIRCULARITY_PROVED_AS_POLICY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "lemma_id": "NG3907_2_not_fatal",
            "statement": "failure to derive numerical G is not a failure of GR reduction",
            "proof_sketch": "GR itself treats G as a coupling measured by experiment; MTS can do the same if it proves derivative/source/range silence",
            "consequence": "local branch can still be competitive as a GR-reduction branch, but not as a prediction of G's value",
            "status": "MEASURED_COUPLING_BRANCH_ALLOWED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def policy_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "policy_id": "POL3907_0_value",
            "quantity": "G_* numerical value",
            "rule": "MEASURED_NOT_PREDICTED unless a source-backed F(kappa_MTS,ell_J,...) exists",
            "runner_effect": "do not score failure to predict G as local-GR failure; do score any drift/source/range dependence",
            "status": "MEASURED_COUPLING_POLICY_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "policy_id": "POL3907_1_derivatives",
            "quantity": "partial G_* residuals",
            "rule": "must be theorem-zero or bounded: time, radius, species/material, range, frame/domain",
            "runner_effect": "activate derivative zero gates before any local-GR/Newton claim",
            "status": "DERIVATIVE_GATES_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "policy_id": "POL3907_2_source_mass",
            "quantity": "Hilbert mass/source normalization",
            "rule": "source mass must be Hilbert/worldtube calibrated independently of orbital GM",
            "runner_effect": "epsilon_Hilbert_mass_norm remains active until source current and Pi_M/H_tau lock",
            "status": "SOURCE_NORMALIZATION_GATE_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def derivative_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DG3907_0_time", "dln_Gstar_dt", "partial_t ln G_*", "zero if G_* in global superselection sector", "Gdot/clock"),
        ("DG3907_1_radial", "partial_r_ln_Gstar", "partial_r ln G_*", "zero if no radial/domain/boundary dependence of coupling", "orbital/R10/radial source"),
        ("DG3907_2_species", "partial_A_ln_Gstar", "material/source-label derivative", "zero if source functor forgets species labels", "WEP/source charge"),
        ("DG3907_3_range", "alpha_Gstar_lambda", "finite-range coupling amplitude", "zero if G_* is not mediated by local range field", "R10/Yukawa"),
        ("DG3907_4_frame", "partial_frame_ln_Gstar", "frame/tau/readout derivative", "zero if same observed frame/tau/source/orbit branch is fixed before readout", "PPN/clocks/orbits"),
        ("DG3907_5_product", "Dln_Z_product", "D ln(G_ref*w_common*ell_J*R_frame*C_extra)", "zero only if every product factor is independently zero-owned", "Newton/Gdot/PPN/R10"),
    ]
    return [
        {
            "gate_id": gate_id,
            "symbol": symbol,
            "definition": definition,
            "zero_route": zero_route,
            "observable_link": observable_link,
            "status": "MISSING_ZERO_PROOF_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, symbol, definition, zero_route, observable_link in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3907_0_no_prediction",
            "decision": "do not claim MTS predicts the numerical value of Newton's constant",
            "reason": "current inspected corpus lacks a parent scale map fixing kappa_* absolutely",
            "effect": "G_* is a measured superselected coupling in the local GR branch",
            "status": "VALUE_DERIVATION_REJECTED_FOR_NOW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3907_1_keep_competitive",
            "decision": "keep the local GR branch alive",
            "reason": "a measured coupling is standard for GR; the nontrivial MTS obligation is derivative/source/range silence",
            "effect": "shift pressure to derivative gates and source normalization, not pointless re-circling over G's number",
            "status": "LOW_ENERGY_BRANCH_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3907_2_next",
            "decision": "attack measured-coupling derivative zero gates next",
            "reason": "these are testable and required for local GR/Newton even if G itself is measured",
            "effect": "next step should prove or bound dG/dt, radial G, species coupling, range dependence and product-factor drift",
            "status": "NEXT_ROUTE_SELECTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3907_0",
            "target_checkpoint": "3908-Y5-R2FR-measured-Gstar-derivative-zero-gates-or-bound-runner.md",
            "script": "scripts/Y5_R2FR_3908_measured_Gstar_derivative_zero_gates_or_bound_runner.py",
            "objective": "prove or bound the measured-coupling derivative gates: dG/dt, radial G, species/source coupling, range dependence, frame drift and product-factor drift",
            "why_next": "3907 rejects a numerical G prediction for now but makes local-GR competitiveness depend on derivative/source/range silence, which is testable and directly tied to existing residual rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_GSTAR_VALUE_UNDERDETERMINED_MEASURED_POLICY_LOCKED",
            "claim": "NO_NUMERICAL_G_PREDICTION",
            "summary": "no source-backed MTS scale map fixes G_*; local branch should treat G_* as measured superselected coupling while proving or bounding derivative/source/range residuals",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    candidate_map: list[dict[str, Any]],
    no_go: list[dict[str, Any]],
    policy: list[dict[str, Any]],
    derivatives: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    timestamp: str,
) -> None:
    doc = f"""# 3907 - Gstar from MTS Scales or Measured Coupling Policy Runner

Generated: `{timestamp}`

## Result

3907 tries the direct `G_*` derivation route and rejects it for now.

Candidate map:

`{SCALE_CANDIDATE}`

No-cheat lemma:

`{NO_GO_LEMMA}`

Measured-coupling policy:

`{MEASURED_POLICY}`

Verdict: the current corpus can own `G_*` as a constant low-energy coupling, but cannot honestly claim to predict its numerical value. This is not fatal: GR also measures `G`. The real MTS local-test obligation is now sharper: prove or bound all derivatives and hidden source-dependences of `G_*`.

## Gstar Scale Candidate Map

{markdown_table(candidate_map, ["row_id", "candidate", "meaning", "status", "failure"])}

## Gstar Underdetermination Lemma

{markdown_table(no_go, ["lemma_id", "statement", "proof_sketch", "consequence", "status"])}

## Measured Coupling Policy Runner

{markdown_table(policy, ["policy_id", "quantity", "rule", "runner_effect", "status"])}

## Gstar Derivative Zero Gates

{markdown_table(derivatives, ["gate_id", "symbol", "definition", "zero_route", "observable_link", "status"])}

## Branch Decision

{markdown_table(decision, ["decision_id", "decision", "reason", "effect", "status"])}

## Source Register

Resolved `{sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

Do not spend another hundred checkpoints trying to magic `G` out of local GR alone. The only honest routes are:

1. derive a real parent scale map for `kappa_*`;
2. or treat `G_*` as measured and prove it is universal, constant, source-blind and range-blind.

Given current evidence, route 2 is the disciplined route. It keeps MTS competitive without pretending to predict something it has not derived.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3907 GSTAR MEASURED COUPLING POLICY -->
## 3907 Gstar Scale Attempt and Measured-Coupling Policy

Timestamp: `{timestamp}`

Candidate map:
`{SCALE_CANDIDATE}`

No-cheat lemma:
`{NO_GO_LEMMA}`

Policy:
`{MEASURED_POLICY}`

Decision: no numerical `G` prediction for now. Treat `G_*` as a measured superselected coupling and attack derivative/source/range gates next.
<!-- END 3907 GSTAR MEASURED COUPLING POLICY -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3907 GSTAR MEASURED COUPLING POLICY -->"
    end = "<!-- END 3907 GSTAR MEASURED COUPLING POLICY -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    candidate_map: list[dict[str, Any]],
    no_go: list[dict[str, Any]],
    policy: list[dict[str, Any]],
    derivatives: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = [row for row in sources if row["exists"] and row["needle_found"]]
    checks.append(("VAL3907_0_sources", "all source paths and needles resolve", len(resolved) == len(sources), f"{len(resolved)}/{len(sources)} sources resolved"))
    checks.append(("VAL3907_1_candidate", "candidate scale map emitted", any(row["row_id"] == "GMAP3907_0_product" for row in candidate_map), "GMAP3907_0"))
    checks.append(("VAL3907_2_no_go", "underdetermination lemma emitted", any(row["lemma_id"] == "NG3907_0_statement" and "UNDERDETERMINATION" in str(row["status"]) for row in no_go), "NG3907_0"))
    checks.append(("VAL3907_3_policy", "measured coupling policy active", any(row["policy_id"] == "POL3907_0_value" and "MEASURED" in str(row["status"]) for row in policy), "POL3907_0"))
    required_derivatives = {"dln_Gstar_dt", "partial_r_ln_Gstar", "partial_A_ln_Gstar", "alpha_Gstar_lambda", "partial_frame_ln_Gstar", "Dln_Z_product"}
    checks.append(("VAL3907_4_derivatives", "derivative gates complete", required_derivatives.issubset({str(row["symbol"]) for row in derivatives}), f"{len(derivatives)} gates"))
    checks.append(("VAL3907_5_decision", "no numerical G prediction decision recorded", any(row["decision_id"] == "DEC3907_0_no_prediction" and "REJECTED" in str(row["status"]) for row in decision), "DEC3907_0"))
    checks.append(("VAL3907_6_all_nonclaim", "all generated rows are nonclaim", all(str(row.get("valid_for_claim", False)) == "False" for collection in [candidate_map, no_go, policy, derivatives, decision] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3907_7_doc", "markdown checkpoint exists with no-cheat lemma", DOC_PATH.exists() and NO_GO_LEMMA in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3907_8_spine", "spine updated with 3907 block", SPINE_PATH.exists() and "BEGIN 3907 GSTAR MEASURED COUPLING POLICY" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3907_9_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3907*")
            if path.is_file() and ("3907-Y5" in path.name or "P8_Y5_R2FR_3907" in path.name or "P8_Y5_BRR545_3907" in path.name)
        ]
    checks.append(("VAL3907_10_formalization_untouched", "no generated 3907 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3907_11_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3907_12_next_target", "next target attacks derivative gates", any("derivative-zero-gates" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3908 derivative gates"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    candidate_map = candidate_map_rows(timestamp)
    no_go = no_go_rows(timestamp)
    policy = policy_rows(timestamp)
    derivatives = derivative_rows(timestamp)
    decision = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["candidate_map"], candidate_map)
    write_csv(OUTPUTS["no_go"], no_go)
    write_csv(OUTPUTS["policy"], policy)
    write_csv(OUTPUTS["derivatives"], derivatives)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, candidate_map, no_go, policy, derivatives, decision, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, candidate_map, no_go, policy, derivatives, decision, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_GSTAR_VALUE_UNDERDETERMINED_MEASURED_POLICY_LOCKED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

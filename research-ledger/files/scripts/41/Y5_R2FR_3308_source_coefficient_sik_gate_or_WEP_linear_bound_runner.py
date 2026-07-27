from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3308-Y5-R2FR-source-coefficient-sik-gate-or-WEP-linear-bound-runner-under-AX1090.md"

SRC_3307_DOC = ROOT / "3307-Y5-R2FR-material-source-charge-model-for-DeltaXi-WEP-bounds-under-AX1090.md"
SRC_3307_BASIS = OUT / "P8_Y5_R2FR_3307_MATERIAL_CHARGE_BASIS.csv"
SRC_3307_MATERIALS = OUT / "P8_Y5_R2FR_3307_MATERIAL_PROXY_CHARGES.csv"
SRC_3307_PAIRS = OUT / "P8_Y5_R2FR_3307_WEP_PAIR_CHARGE_DELTAS.csv"
SRC_3307_BOUNDS = OUT / "P8_Y5_R2FR_3307_WEP_BOUND_ROWS_NONCLAIM.csv"
SRC_3307_LAWS = OUT / "P8_Y5_R2FR_3307_DELTA_XI_LINEAR_MODEL.csv"
SRC_3307_NEXT = OUT / "P8_Y5_R2FR_3307_NEXT_TARGET.csv"
SRC_3307_VALIDATION = OUT / "P8_Y5_BRR545_3307_VALIDATION.csv"
SRC_3306_WEP = OUT / "P8_Y5_R2FR_3306_WEP_SOURCE_ANCHORS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3308_SOURCE_REGISTER.csv",
    "sik_gate": OUT / "P8_Y5_R2FR_3308_SOURCE_COEFFICIENT_SIK_GATE.csv",
    "matrix": OUT / "P8_Y5_R2FR_3308_WEP_LINEAR_CONSTRAINT_MATRIX.csv",
    "unit_proxy": OUT / "P8_Y5_R2FR_3308_UNIT_MODE_FACTOR_SENSITIVITY_PROXY.csv",
    "runner": OUT / "P8_Y5_R2FR_3308_LINEAR_BOUND_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3308_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3308_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3308_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3308_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
CHARGE_KEYS = ["Delta_q_B", "Delta_q_p", "Delta_q_n", "Delta_q_C", "Delta_q_D"]


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 820) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
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


def evidence_hits(path: Path, needles: list[str], limit: int = 5) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    for line_number, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered_needles):
            hits.append(f"L{line_number}:{compact(line, 420)}")
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


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3307_DOC, "3307 material charge model", ["Delta_Xi_i", "s_ik"]),
        (SRC_3307_BASIS, "3307 charge basis", ["q_B", "q_C"]),
        (SRC_3307_MATERIALS, "3307 proxy material charges", ["Be_proxy", "Pt_proxy"]),
        (SRC_3307_PAIRS, "3307 WEP pair charge deltas", ["MICROSCOPE", "EOTWASH"]),
        (SRC_3307_BOUNDS, "3307 nonclaim bound rows", ["eta_sigma_proxy", "Delta_q_vector"]),
        (SRC_3307_LAWS, "3307 DeltaXi linear model", ["s_0", "s_2"]),
        (SRC_3307_NEXT, "3307 next target", ["source-coefficient-sik", "linear WEP"]),
        (SRC_3307_VALIDATION, "3307 validation", ["VAL3307_12_overall", "true"]),
        (SRC_3306_WEP, "3306 WEP anchors", ["MICROSCOPE", "Eot-Wash"]),
    ]
    rows: list[dict[str, Any]] = []
    for index, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3308_{index}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def sik_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_object_id": "SIK3308_0_scalar_zero",
            "coefficient_family": "s_0k",
            "zero_condition": "all scalar nonuniversal source coefficients s_0B,s_0p,s_0n,s_0C,s_0D vanish or project out of all material contrasts",
            "if_zero": "Delta_Xi_0[A,B]=0 and scalar finite mode does not violate WEP through composition",
            "if_nonzero": "WEP rows constrain alpha0_star Xi_0[E] range_0(lambda) (s_0 dot Delta_q)",
            "current_status": "NOT_PARENT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "gate_object_id": "SIK3308_1_spin2_zero",
            "coefficient_family": "s_2k",
            "zero_condition": "all spin2 nonuniversal source coefficients s_2B,s_2p,s_2n,s_2C,s_2D vanish or project out of all material contrasts",
            "if_zero": "Delta_Xi_2[A,B]=0 and massive spin-2 finite mode does not violate WEP through composition",
            "if_nonzero": "WEP rows constrain alpha2_star Xi_2[E] range_2(lambda) (s_2 dot Delta_q)",
            "current_status": "NOT_PARENT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "gate_object_id": "SIK3308_2_combined",
            "coefficient_family": "s_ik",
            "zero_condition": "both scalar and spin2 nonuniversal source coefficient families vanish or are bounded below WEP residuals",
            "if_zero": "finite-mode source composition gate closes, pending Z/U/range checks",
            "if_nonzero": "must run linear WEP constraints with exact materials and confidence handling",
            "current_status": "BOUND_RUNNER_ONLY",
            "valid_for_claim": "false",
        },
    ]


def get_anchor_lookup() -> dict[str, dict[str, str]]:
    return {row["anchor_id"]: row for row in read_csv(SRC_3306_WEP)}


def eta_sigma_for_anchor(anchor_id: str, bound_row: dict[str, str]) -> tuple[str, str]:
    if bound_row["eta_sigma_proxy"] != "MISSING_COMBINED_UNCERTAINTY":
        return bound_row["eta_sigma_proxy"], "combined_stat_syst_proxy_from_3307"
    anchor = get_anchor_lookup().get(anchor_id, {})
    stat = anchor.get("eta_stat_uncertainty", "")
    try:
        float(stat)
        return stat, "stat_uncertainty_proxy_only_systematic_missing"
    except ValueError:
        return "MISSING_ETA_SIGMA", "missing_uncertainty"


def row_norm(row: dict[str, str]) -> float:
    return math.sqrt(sum(float(row[key]) ** 2 for key in CHARGE_KEYS))


def linear_constraint_rows() -> list[dict[str, Any]]:
    bound_lookup = {row["anchor_id"]: row for row in read_csv(SRC_3307_BOUNDS)}
    rows: list[dict[str, Any]] = []
    for pair in read_csv(SRC_3307_PAIRS):
        anchor_id = pair["anchor_id"]
        bound = bound_lookup[anchor_id]
        eta_sigma, eta_sigma_source = eta_sigma_for_anchor(anchor_id, bound)
        delta_vector = [float(pair[key]) for key in CHARGE_KEYS]
        delta_norm = row_norm(pair)
        for mode, coeff_prefix, mode_factor in [
            ("scalar", "s_0", "K_0(lambda_0)=alpha0_star Xi_0[E](1+r/lambda_0)exp(-r/lambda_0)"),
            ("spin2", "s_2", "K_2(lambda_2)=alpha2_star Xi_2[E](1+r/lambda_2)exp(-r/lambda_2)"),
        ]:
            rows.append(
                {
                    "constraint_id": f"LC3308_{mode}_{anchor_id}",
                    "mode": mode,
                    "anchor_id": anchor_id,
                    "test_body_pair": bound["test_body_pair"],
                    "attractor_source": bound["attractor_source"],
                    "Delta_q_B": pair["Delta_q_B"],
                    "Delta_q_p": pair["Delta_q_p"],
                    "Delta_q_n": pair["Delta_q_n"],
                    "Delta_q_C": pair["Delta_q_C"],
                    "Delta_q_D": pair["Delta_q_D"],
                    "Delta_q_norm_proxy": f"{delta_norm:.12g}",
                    "linear_form": f"{coeff_prefix}B*Delta_q_B + {coeff_prefix}p*Delta_q_p + {coeff_prefix}n*Delta_q_n + {coeff_prefix}C*Delta_q_C + {coeff_prefix}D*Delta_q_D",
                    "mode_factor": mode_factor,
                    "eta_sigma_proxy": eta_sigma,
                    "eta_sigma_source": eta_sigma_source,
                    "constraint_template": f"|{mode_factor} * ({coeff_prefix} dot Delta_q_AB)| <= eta_bound_ABE",
                    "current_status": "SYMBOLIC_BOUND_NOT_CLAIM",
                    "valid_for_claim": "false",
                }
            )
    return rows


def unit_mode_proxy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for constraint in linear_constraint_rows():
        try:
            eta_sigma = float(constraint["eta_sigma_proxy"])
            delta_norm = float(constraint["Delta_q_norm_proxy"])
            proxy_bound = eta_sigma / delta_norm if delta_norm > 0 else math.inf
            proxy = f"{proxy_bound:.12g}"
        except ValueError:
            proxy = "MISSING_PROXY_BOUND"
        rows.append(
            {
                "proxy_id": f"UP3308_{constraint['constraint_id']}",
                "constraint_id": constraint["constraint_id"],
                "meaning": "diagnostic only: bound on |s_i direction| if |K_i|=1 and exact material proxies were valid",
                "unit_mode_factor_proxy_bound": proxy,
                "why_nonclaim": "K_i, exact materials, confidence convention, and source charge are not filled",
                "valid_for_claim": "false",
            }
        )
    return rows


def runner_rows() -> list[dict[str, Any]]:
    matrix = linear_constraint_rows()
    proxies = unit_mode_proxy_rows()
    nonclaim = all(row["valid_for_claim"] == "false" for row in matrix + proxies)
    return [
        {
            "runner_id": "RUN3308_0_constraint_matrix",
            "test": "linear constraints exist for scalar and spin2 modes for both WEP anchors",
            "result": "PASS_NONCLAIM" if len(matrix) == 4 else "FAIL",
            "detail": ";".join(row["constraint_id"] for row in matrix),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3308_1_unit_proxy",
            "test": "unit mode-factor sensitivity proxies exist",
            "result": "PASS_NONCLAIM" if len(proxies) == 4 and nonclaim else "FAIL",
            "detail": ";".join(row["unit_mode_factor_proxy_bound"] for row in proxies),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3308_2_claim_permission",
            "test": "linear WEP constraints claim-ready",
            "result": "REFUSE_CLAIM_K_FACTORS_AND_EXACT_DATA_MISSING",
            "detail": "K_i(lambda), exact materials, source-body charge Xi_i[E], confidence conversion, and s_ik derivation remain missing",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3308_0_sik_zero",
            "claim": "s_0k=s_2k=0 by parent source projector",
            "requirements": "parent-derived source projector proves no material charge direction enters finite-mode source charge",
            "current_evidence": "not parent-derived",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3308_1_linear_WEP_bound",
            "claim": "WEP data bounds s_ik combinations below required local-GR tolerance",
            "requirements": "claim-ready K_i(lambda), exact material/source charge model, confidence conversion, and no cancellation loophole",
            "current_evidence": "symbolic linear matrix and unit-factor proxy only",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3308_2_source_composition_safe",
            "claim": "source-composition branch is safe for local GR",
            "requirements": "GATE3308_0 or GATE3308_1 passes",
            "current_evidence": "neither route passes",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3308_0",
            "question": "Did 3308 derive s_ik from the parent projector?",
            "answer": "no",
            "reason": "no parent source projector algebra is available, so s_ik remains an unknown source-coefficient vector",
            "next_action": "either derive s_ik=0 from parent matter variation or fill exact WEP data inputs for linear bounds",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3308_1",
            "question": "What useful progress exists?",
            "answer": "the Ti/Pt and Be/Ti WEP anchors are now linear constraints on s_0k and s_2k combinations",
            "reason": "the runner maps each experiment to |K_i(lambda) (s_i dot Delta_q)| <= eta_bound",
            "next_action": "build K_i(lambda) from alpha_star, source charge, and finite-mode range, or acquire exact material/confidence inputs",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3308_0_3309",
            "target_doc": "3309-Y5-R2FR-mode-factor-Klambda-and-exact-WEP-inputs-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3309_mode_factor_Klambda_and_exact_WEP_inputs.py",
            "objective": "derive the mode factor K_i(lambda)=alpha_i_star Xi_i[E](1+r/lambda_i)exp(-r/lambda_i), and replace proxy material/confidence rows with exact WEP inputs where source-backed data are available",
            "guardrails": "do not claim WEP safety from unit-mode proxies; do not combine scalar and spin2 constraints unless the parent derives a common K or cancellation rule",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_paths = [Path(row["path"]) for row in source_rows]
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    sik_gates = sik_gate_rows()
    matrix = linear_constraint_rows()
    proxies = unit_mode_proxy_rows()
    runners = runner_rows()
    gates = promotion_gate_rows()
    next_rows = next_target_rows()

    checks = [
        (
            "VAL3308_0_sources_exist",
            "all cited source paths exist",
            all(path.exists() for path in source_paths),
            "",
        ),
        (
            "VAL3308_1_sources_parse",
            "all cited source paths parse",
            all(parse_ok(path) for path in source_paths),
            "",
        ),
        (
            "VAL3308_2_outputs_parse",
            "all 3308 non-validation output CSVs parse",
            all(csv_parse_ok(path) for path in output_paths),
            "",
        ),
        (
            "VAL3308_3_sik_gate_complete",
            "s_ik gate covers scalar, spin2, and combined families",
            all(any(token in row["coefficient_family"] for row in sik_gates) for token in ["s_0", "s_2", "s_ik"]),
            "",
        ),
        (
            "VAL3308_4_constraint_matrix_complete",
            "linear matrix has scalar/spin2 constraints for MICROSCOPE and Eot-Wash anchors",
            len(matrix) == 4
            and all(any(mode == row["mode"] for row in matrix) for mode in ["scalar", "spin2"])
            and all(any(anchor in row["anchor_id"] for row in matrix) for anchor in ["MICROSCOPE", "EOTWASH"]),
            "",
        ),
        (
            "VAL3308_5_mode_factor_present",
            "constraints include K_i(lambda) mode factors",
            all("K_" in row["mode_factor"] and "lambda" in row["mode_factor"] for row in matrix),
            "",
        ),
        (
            "VAL3308_6_unit_proxy_nonclaim",
            "unit mode-factor proxies exist and remain nonclaim",
            len(proxies) == 4 and all(row["valid_for_claim"] == "false" for row in proxies),
            "",
        ),
        (
            "VAL3308_7_runner_refuses_claim",
            "runner refuses claim until K/exact data are filled",
            any(row["result"] == "REFUSE_CLAIM_K_FACTORS_AND_EXACT_DATA_MISSING" for row in runners),
            "",
        ),
        (
            "VAL3308_8_claim_gates_false",
            "all promotion gates remain false",
            all(row["passed"] == "false" and row["valid_for_claim"] == "false" for row in gates),
            "",
        ),
        (
            "VAL3308_9_next_target_Klambda",
            "next target derives K(lambda) and exact WEP inputs",
            "mode-factor-Klambda" in next_rows[0]["target_doc"],
            "",
        ),
    ]

    formalization_after = snapshot_tree(FW)
    formalization_changed = changed_count(formalization_before, formalization_after)
    checks.append(
        (
            "VAL3308_10_formalization_untouched",
            "formalization-workbench modified-file count remains zero by this script",
            formalization_changed == 0,
            f"formalization_changed_count={formalization_changed}",
        )
    )

    overall = all(passed for _, _, passed, _ in checks)
    checks.append(
        (
            "VAL3308_11_overall",
            "3308 validation overall",
            overall,
            "all required checks passed" if overall else "one or more checks failed",
        )
    )

    return [
        {
            "check_id": check_id,
            "check": check,
            "passed": bool_str(passed),
            "detail": detail,
        }
        for check_id, check, passed, detail in checks
    ]


def render_doc() -> str:
    source_table = "\n".join(
        f"- `{row['source_id']}`: `{row['path']}` — exists={row['exists']}; role={row['role']}"
        for row in source_register_rows()
    )
    gate_table = "\n".join(
        f"- `{row['gate_object_id']}` `{row['coefficient_family']}`: {row['zero_condition']}"
        for row in sik_gate_rows()
    )
    matrix_table = "\n".join(
        f"- `{row['constraint_id']}`: `{row['constraint_template']}` with Delta_q_norm={row['Delta_q_norm_proxy']} eta_sigma={row['eta_sigma_proxy']}."
        for row in linear_constraint_rows()
    )
    proxy_table = "\n".join(
        f"- `{row['proxy_id']}`: unit K proxy bound `{row['unit_mode_factor_proxy_bound']}` ({row['why_nonclaim']})."
        for row in unit_mode_proxy_rows()
    )
    runner_table = "\n".join(
        f"- `{row['runner_id']}`: `{row['result']}` — {row['detail']}"
        for row in runner_rows()
    )
    promotion_table = "\n".join(
        f"- `{row['gate_id']}`: passed={row['passed']}; claim={row['claim']}"
        for row in promotion_gate_rows()
    )
    decision_table = "\n".join(
        f"- `{row['decision_id']}`: {row['answer']} — {row['reason']}"
        for row in decision_rows()
    )
    next_row = next_target_rows()[0]

    return f"""# 3308 - Source coefficient s_ik gate or WEP linear bound runner under AX1090

Run UTC: `{RUN_UTC}`

## Verdict

The WEP fallback is now a linear constraint system.

For each finite mode `i`,

`Delta_Xi_i[A,B] = s_i dot Delta_q_AB`.

Each WEP anchor therefore constrains

`|K_i(lambda_i) (s_i dot Delta_q_AB)| <= eta_bound_ABE`,

where

`K_i(lambda_i)=alpha_i_star Xi_i[E] (1+r/lambda_i) exp(-r/lambda_i)`.

This is not a claim runner yet. It is a clean algebraic gate: either derive `s_ik=0`, derive `K_i(lambda_i)`, or use exact WEP material/source data to bound the allowed source-coefficient combinations.

## Source Register

{source_table}

## s_ik Gate

{gate_table}

## Linear Constraint Matrix

{matrix_table}

## Unit Mode-Factor Sensitivity Proxy

{proxy_table}

## Runner

{runner_table}

## Promotion Gates

{promotion_table}

## Decision

{decision_table}

## Next Target

- `{next_row['target_doc']}`
- `{next_row['target_script']}`
- Objective: {next_row['objective']}
"""


def main() -> None:
    formalization_before = snapshot_tree(FW)

    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["sik_gate"], sik_gate_rows())
    write_csv(OUTPUTS["matrix"], linear_constraint_rows())
    write_csv(OUTPUTS["unit_proxy"], unit_mode_proxy_rows())
    write_csv(OUTPUTS["runner"], runner_rows())
    write_csv(OUTPUTS["promotion"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())

    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))

    if PYCACHE.exists():
        for child in PYCACHE.rglob("*"):
            if child.is_file():
                child.unlink()
        for child in sorted(PYCACHE.rglob("*"), reverse=True):
            if child.is_dir():
                child.rmdir()
        PYCACHE.rmdir()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

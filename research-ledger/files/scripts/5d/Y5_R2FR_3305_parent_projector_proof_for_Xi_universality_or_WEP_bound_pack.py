from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3305-Y5-R2FR-parent-projector-proof-for-Xi-universality-or-WEP-bound-pack-under-AX1090.md"

SRC_3304_DOC = ROOT / "3304-Y5-R2FR-source-projection-overlap-law-for-alpha-factors-under-AX1090.md"
SRC_3304_XI = OUT / "P8_Y5_R2FR_3304_XI_OVERLAP_DEFINITION.csv"
SRC_3304_PAIR = OUT / "P8_Y5_R2FR_3304_PAIRWISE_FORCE_LAW.csv"
SRC_3304_UNIV = OUT / "P8_Y5_R2FR_3304_XI_UNIVERSALITY_PROOF_CLAUSES.csv"
SRC_3304_WEP = OUT / "P8_Y5_R2FR_3304_WEP_SOURCE_RESIDUAL_MAP.csv"
SRC_3304_NEXT = OUT / "P8_Y5_R2FR_3304_NEXT_TARGET.csv"
SRC_3304_VALIDATION = OUT / "P8_Y5_BRR545_3304_VALIDATION.csv"
SRC_3293_HILBERT = OUT / "P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv"
SRC_3294_CONTRACT = OUT / "P8_Y5_R2FR_3294_LOCAL_GR_REDUCTION_CONTRACT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3305_SOURCE_REGISTER.csv",
    "derivation": OUT / "P8_Y5_R2FR_3305_PARENT_PROJECTOR_IDENTITY_DERIVATION.csv",
    "audit": OUT / "P8_Y5_R2FR_3305_PROJECTOR_PROOF_CLAUSE_AUDIT.csv",
    "wep_pack": OUT / "P8_Y5_R2FR_3305_WEP_BOUND_PACK_SCHEMA.csv",
    "runner": OUT / "P8_Y5_R2FR_3305_PROJECTOR_OR_WEP_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3305_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3305_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3305_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3305_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 780) -> str:
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
            hits.append(f"L{line_number}:{compact(line, 400)}")
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
        (SRC_3304_DOC, "3304 source-overlap law", ["V_AB", "Xi_0", "Xi_2"]),
        (SRC_3304_XI, "3304 Xi definitions", ["XI3304_0_scalar_source_charge", "XI3304_1_spin2_source_charge"]),
        (SRC_3304_PAIR, "3304 pairwise force law", ["PAIR3304_0_general_pair_potential", "Xi_0[A]"]),
        (SRC_3304_UNIV, "3304 universality clauses", ["XIU3304_2_projector_same_as_pure_limit", "MISSING_LINEARIZED_PARENT_PROJECTOR"]),
        (SRC_3304_WEP, "3304 WEP residual map", ["WEP3304_0_scalar_delta", "eta_AB"]),
        (SRC_3304_NEXT, "3304 next target", ["parent-projector-proof", "WEP-bound-pack"]),
        (SRC_3304_VALIDATION, "3304 validation", ["VAL3304_10_overall", "true"]),
        (SRC_3293_HILBERT, "3293 Hilbert source theorem", ["Hilbert-source", "NOT_PARENT_SIGNED"]),
        (SRC_3294_CONTRACT, "3294 local GR contract", ["single public metric", "Hilbert source"]),
    ]
    rows: list[dict[str, Any]] = []
    for index, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3305_{index}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def projector_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "PIP3305_0_metric_decomposition",
            "statement": "Write the public metric perturbation in diagonal local modes: delta g_pub_mu_nu = e^(0)_mu_nu phi_0 + e^(2)_mu_nu H_2 + e^(m)_mu_nu h_m + residuals.",
            "derivation_role": "separates scalar finite mode, massive spin-2 finite mode, and massless graviton readout",
            "status": "REQUIRES_PARENT_LINEARIZED_PROJECTOR",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PIP3305_1_matter_variation",
            "statement": "If matter depends on finite modes only through g_pub, then delta S_m = (1/2) integral sqrt(-g) T_H^mu_nu delta g_pub_mu_nu.",
            "derivation_role": "turns finite-mode source charge into a Hilbert-stress projection instead of a new coupling",
            "status": "EXACT_IF_SINGLE_PUBLIC_METRIC_AND_HILBERT_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PIP3305_2_mode_charges",
            "statement": "Q_0[A] = (1/2) integral_A sqrt(-g) T_H^mu_nu e^(0)_mu_nu and Q_2[A] = (1/2) integral_A sqrt(-g) T_H^mu_nu e^(2)_mu_nu, up to the chosen mode normalization.",
            "derivation_role": "defines source-projection charges from the same stress tensor that defines Newtonian mass",
            "status": "CONDITIONAL_SOURCE_CHARGE_FORMULA",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PIP3305_3_universality_theorem",
            "statement": "If e^(0), e^(2), normalization, EM/binding-energy accounting, and readout are the pure metric local projectors, then Xi_0[A]=Xi_2[A]=1 for all bodies in the nonrelativistic local limit.",
            "derivation_role": "conditional proof route to universal alpha scoring",
            "status": "THEOREM_CONDITIONAL_NOT_PROMOTED",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PIP3305_4_failure_branch",
            "statement": "If any direct hidden/matter coupling, species selector, non-Hilbert current, EM double count, or readout split survives, Xi_i[A] becomes body dependent and must be bounded as a WEP/source residual.",
            "derivation_role": "prevents smuggling Xi_i[A]=1 without parent proof",
            "status": "BOUND_BRANCH_ACTIVE",
            "valid_for_claim": "false",
        },
    ]


def proof_clause_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "PCA3305_0_single_public_metric",
            "needed": "one public metric owns matter readout and finite mode decomposition",
            "current_evidence": "conditional from 3294, not parent-signed",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PCA3305_1_Hilbert_source_only",
            "needed": "matter variation is exhausted by T_H^mu_nu delta g_pub_mu_nu",
            "current_evidence": "exact conditional theorem from 3293, not parent-signed",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PCA3305_2_linearized_projectors",
            "needed": "parent local action supplies e^(0)_mu_nu and e^(2)_mu_nu matching pure metric projectors",
            "current_evidence": "missing linearized parent projector",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PCA3305_3_no_direct_hidden_matter_coupling",
            "needed": "no finite mode couples directly to matter outside g_pub",
            "current_evidence": "not parent-signed",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PCA3305_4_EM_binding_Poynting_accounted",
            "needed": "EM stress, Poynting flux, binding energy, and clock sectors enter once through T_H",
            "current_evidence": "guarded by earlier Hilbert/EM branch, not fully signed",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def wep_bound_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "WBP3305_0_material_pair",
            "field": "test_body_pair",
            "symbol": "A,B",
            "required_value": "material labels and composition fractions for the WEP comparison",
            "units": "dimensionless labels/fractions",
            "status": "SOURCE_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "WBP3305_1_source_body",
            "field": "attractor_source",
            "symbol": "E",
            "required_value": "source body composition or justified universal source approximation",
            "units": "dimensionless labels/fractions",
            "status": "SOURCE_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "WBP3305_2_scalar_delta",
            "field": "scalar source residual",
            "symbol": "Delta_Xi_0[A,B]",
            "required_value": "Xi_0[A]-Xi_0[B] or bound",
            "units": "dimensionless",
            "status": "DERIVATION_OR_BOUND_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "WBP3305_3_spin2_delta",
            "field": "spin2 source residual",
            "symbol": "Delta_Xi_2[A,B]",
            "required_value": "Xi_2[A]-Xi_2[B] or bound",
            "units": "dimensionless",
            "status": "DERIVATION_OR_BOUND_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "WBP3305_4_mode_strengths",
            "field": "finite mode strengths",
            "symbol": "alpha0_star, alpha2_star",
            "required_value": "mode residues after Z/U normalization",
            "units": "dimensionless",
            "status": "WAITING_ON_3303_ZU_FACTORS",
            "valid_for_claim": "false",
        },
        {
            "row_id": "WBP3305_5_ranges",
            "field": "finite mode ranges",
            "symbol": "lambda_0, lambda_2",
            "required_value": "ranges from parent coefficients or bounds",
            "units": "length",
            "status": "WAITING_ON_PARENT_COEFFICIENTS",
            "valid_for_claim": "false",
        },
        {
            "row_id": "WBP3305_6_wep_bound",
            "field": "Eotvos bound",
            "symbol": "eta_bound(lambda, materials, source)",
            "required_value": "sourced WEP bound with experiment, materials, range regime, and confidence",
            "units": "dimensionless",
            "status": "SOURCE_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "WBP3305_7_acceptance_inequality",
            "field": "WEP acceptance",
            "symbol": "|sum_i alpha_i_star Xi_i[E] Delta_Xi_i[A,B] (1+r/lambda_i) exp(-r/lambda_i)| <= eta_bound",
            "required_value": "all quantities numeric/sourced before scoring",
            "units": "dimensionless",
            "status": "NONCLAIM_TEMPLATE",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    proof_pass = all(row["passed"] == "true" for row in proof_clause_audit_rows())
    wep_schema_ready = len(wep_bound_pack_rows()) >= 8
    return [
        {
            "runner_id": "RUN3305_0_projector_proof",
            "test": "all parent projector proof clauses pass",
            "result": "PASS_XI_UNIVERSAL" if proof_pass else "FAIL_KEEP_XI_LIVE",
            "detail": ";".join(f"{row['clause_id']}={row['passed']}" for row in proof_clause_audit_rows()),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3305_1_WEP_pack_schema",
            "test": "WEP/source bound pack has required symbolic fields",
            "result": "PASS_NONCLAIM" if wep_schema_ready else "FAIL",
            "detail": ";".join(row["symbol"] for row in wep_bound_pack_rows()),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3305_2_universal_alpha_permission",
            "test": "universal alpha scoring allowed",
            "result": "REFUSE_UNIVERSAL_ALPHA" if not proof_pass else "ALLOW_AFTER_REVIEW",
            "detail": "Xi_i[A] remains live unless RUN3305_0 passes and is reviewed",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3305_0_projector_theorem",
            "claim": "Xi_0[A]=Xi_2[A]=1 follows from parent projector identity",
            "requirements": "all projector audit clauses pass with parent-signed evidence",
            "current_evidence": "missing parent linearized projectors and fully signed source/readout clauses",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3305_1_WEP_bound_claim",
            "claim": "nonuniversal Xi residuals are empirically safe",
            "requirements": "numeric Delta_Xi, alpha_star, lambda, source Xi, and sourced eta_bound rows",
            "current_evidence": "schema only",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3305_2_local_GR_source_projection",
            "claim": "source-projection part of local-GR branch is closed",
            "requirements": "GATE3305_0 true or GATE3305_1 true",
            "current_evidence": "neither route closed",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3305_0",
            "question": "Did the parent projector proof close Xi universality?",
            "answer": "no",
            "reason": "the identity is derived conditionally, but parent linearized projectors and fully signed source/readout clauses are absent",
            "next_action": "extract or derive the linearized public metric projector e^(0), e^(2) from the parent action",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3305_1",
            "question": "What is ready if the proof does not close?",
            "answer": "a WEP/source-composition bound-pack schema for Delta_Xi_0 and Delta_Xi_2",
            "reason": "nonuniversal finite-mode coupling becomes an Eotvos-style residual with explicit required inputs",
            "next_action": "either prove projectors or acquire WEP/source bound rows",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3305_0_3306",
            "target_doc": "3306-Y5-R2FR-linearized-public-metric-projector-extraction-or-WEP-data-acquisition-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3306_linearized_public_metric_projector_extraction_or_WEP_data_acquisition.py",
            "objective": "hunt or derive the parent linearized public-metric projectors e^(0)_mu_nu and e^(2)_mu_nu; if not available, acquire sourced WEP bound rows for the Delta_Xi residuals",
            "guardrails": "do not assume pure metric projectors; do not use WEP bounds until materials, source body, ranges, and confidence are sourced",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_paths = [Path(row["path"]) for row in source_rows]
    outputs_to_parse = [path for key, path in OUTPUTS.items() if key != "validation"]
    derivation = projector_derivation_rows()
    audit = proof_clause_audit_rows()
    wep_pack = wep_bound_pack_rows()
    runners = runner_rows()
    gates = promotion_gate_rows()
    next_rows = next_target_rows()

    checks = [
        (
            "VAL3305_0_sources_exist",
            "all cited source paths exist",
            all(path.exists() for path in source_paths),
            "",
        ),
        (
            "VAL3305_1_sources_parse",
            "all cited source paths parse",
            all(parse_ok(path) for path in source_paths),
            "",
        ),
        (
            "VAL3305_2_outputs_parse",
            "all 3305 non-validation output CSVs parse",
            all(csv_parse_ok(path) for path in outputs_to_parse),
            "",
        ),
        (
            "VAL3305_3_projector_derivation_has_deltaSm",
            "projector derivation includes delta S_m and mode-charge identities",
            any("delta S_m" in row["statement"] for row in derivation)
            and any("Q_0[A]" in row["statement"] and "Q_2[A]" in row["statement"] for row in derivation),
            "",
        ),
        (
            "VAL3305_4_projector_audit_blocks_claim",
            "projector audit blocks Xi universality claim",
            all(row["passed"] == "false" for row in audit),
            "",
        ),
        (
            "VAL3305_5_WEP_pack_complete",
            "WEP bound pack includes Delta_Xi, alpha, lambda, eta_bound, and acceptance inequality",
            all(
                any(token in row["symbol"] for row in wep_pack)
                for token in ["Delta_Xi_0", "Delta_Xi_2", "alpha0_star", "lambda_0", "eta_bound"]
            ),
            "",
        ),
        (
            "VAL3305_6_runner_refuses_universal_alpha",
            "runner refuses universal alpha while projector proof fails",
            any(row["result"] == "REFUSE_UNIVERSAL_ALPHA" for row in runners),
            "",
        ),
        (
            "VAL3305_7_claim_gates_false",
            "all 3305 promotion gates remain false",
            all(row["passed"] == "false" and row["valid_for_claim"] == "false" for row in gates),
            "",
        ),
        (
            "VAL3305_8_next_target_projector_or_data",
            "next target extracts projectors or acquires WEP data",
            "linearized-public-metric-projector" in next_rows[0]["target_doc"]
            and "WEP-data-acquisition" in next_rows[0]["target_doc"],
            "",
        ),
    ]

    formalization_after = snapshot_tree(FW)
    formalization_changed = changed_count(formalization_before, formalization_after)
    checks.append(
        (
            "VAL3305_9_formalization_untouched",
            "formalization-workbench modified-file count remains zero by this script",
            formalization_changed == 0,
            f"formalization_changed_count={formalization_changed}",
        )
    )

    overall = all(passed for _, _, passed, _ in checks)
    checks.append(
        (
            "VAL3305_10_overall",
            "3305 validation overall",
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
    derivation_table = "\n".join(
        f"- `{row['step_id']}`: {row['statement']} Status: `{row['status']}`."
        for row in projector_derivation_rows()
    )
    audit_table = "\n".join(
        f"- `{row['clause_id']}`: passed={row['passed']}; needed={row['needed']}; evidence={row['current_evidence']}"
        for row in proof_clause_audit_rows()
    )
    wep_table = "\n".join(
        f"- `{row['row_id']}` `{row['symbol']}`: {row['required_value']} Status: `{row['status']}`."
        for row in wep_bound_pack_rows()
    )
    runner_table = "\n".join(
        f"- `{row['runner_id']}`: `{row['result']}` — {row['detail']}"
        for row in runner_rows()
    )
    gate_table = "\n".join(
        f"- `{row['gate_id']}`: passed={row['passed']}; claim={row['claim']}"
        for row in promotion_gate_rows()
    )
    decision_table = "\n".join(
        f"- `{row['decision_id']}`: {row['answer']} — {row['reason']}"
        for row in decision_rows()
    )
    next_row = next_target_rows()[0]

    return f"""# 3305 - Parent projector proof for Xi universality or WEP bound pack under AX1090

Run UTC: `{RUN_UTC}`

## Verdict

The parent projector proof has been attempted in exact conditional form.

If matter sees finite modes only through the public metric, then

`delta S_m = (1/2) integral sqrt(-g) T_H^mu_nu delta g_pub_mu_nu`.

With

`delta g_pub_mu_nu = e^(0)_mu_nu phi_0 + e^(2)_mu_nu H_2 + ...`,

the finite-mode charges are Hilbert-stress projectors:

`Q_0[A] = (1/2) integral_A sqrt(-g) T_H^mu_nu e^(0)_mu_nu`,

`Q_2[A] = (1/2) integral_A sqrt(-g) T_H^mu_nu e^(2)_mu_nu`.

That would prove `Xi_0[A]=Xi_2[A]=1` only if the parent supplies the pure-metric projectors and no direct hidden/source/readout coupling survives. Current evidence does not sign those clauses, so the WEP/source-composition pack remains active.

## Source Register

{source_table}

## Projector Identity Derivation

{derivation_table}

## Proof Clause Audit

{audit_table}

## WEP Bound Pack Schema

{wep_table}

## Runner

{runner_table}

## Promotion Gates

{gate_table}

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
    write_csv(OUTPUTS["derivation"], projector_derivation_rows())
    write_csv(OUTPUTS["audit"], proof_clause_audit_rows())
    write_csv(OUTPUTS["wep_pack"], wep_bound_pack_rows())
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

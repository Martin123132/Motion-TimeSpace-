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

DOC = ROOT / "3304-Y5-R2FR-source-projection-overlap-law-for-alpha-factors-under-AX1090.md"

SRC_3303_DOC = ROOT / "3303-Y5-R2FR-universal-Hilbert-source-check-for-quadratic-amplitudes-under-AX1090.md"
SRC_3303_LAW = OUT / "P8_Y5_R2FR_3303_GENERALIZED_ALPHA_AMPLITUDE_LAW.csv"
SRC_3303_REQ = OUT / "P8_Y5_R2FR_3303_SOURCE_PROJECTION_REQUIREMENTS.csv"
SRC_3303_DECISION = OUT / "P8_Y5_R2FR_3303_DECISION_LEDGER.csv"
SRC_3303_NEXT = OUT / "P8_Y5_R2FR_3303_NEXT_TARGET.csv"
SRC_3303_VALIDATION = OUT / "P8_Y5_BRR545_3303_VALIDATION.csv"
SRC_3293_HILBERT = OUT / "P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv"
SRC_3293_LOCAL = OUT / "P8_Y5_R2FR_3293_LOCAL_GR_MATTER_COUPLING_REDUCTION.csv"
SRC_3294_CONTRACT = OUT / "P8_Y5_R2FR_3294_LOCAL_GR_REDUCTION_CONTRACT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3304_SOURCE_REGISTER.csv",
    "overlap": OUT / "P8_Y5_R2FR_3304_XI_OVERLAP_DEFINITION.csv",
    "pairwise": OUT / "P8_Y5_R2FR_3304_PAIRWISE_FORCE_LAW.csv",
    "universality": OUT / "P8_Y5_R2FR_3304_XI_UNIVERSALITY_PROOF_CLAUSES.csv",
    "wep": OUT / "P8_Y5_R2FR_3304_WEP_SOURCE_RESIDUAL_MAP.csv",
    "decision": OUT / "P8_Y5_R2FR_3304_DECISION_LEDGER.csv",
    "promotion": OUT / "P8_Y5_R2FR_3304_PROMOTION_GATES.csv",
    "next": OUT / "P8_Y5_R2FR_3304_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3304_VALIDATION.csv",
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
        (SRC_3303_DOC, "3303 amplitude import decision", ["alpha_0", "Xi_0", "Xi_2"]),
        (SRC_3303_LAW, "3303 alpha law", ["ALAW3303_0_scalar", "ALAW3303_1_spin2"]),
        (SRC_3303_REQ, "3303 projection requirements", ["Xi_0", "Xi_2"]),
        (SRC_3303_DECISION, "3303 decision", ["DEC3303_1", "source projection"]),
        (SRC_3303_NEXT, "3303 next target", ["source-projection-overlap", "Xi_0"]),
        (SRC_3303_VALIDATION, "3303 validation", ["VAL3303_10_overall", "true"]),
        (SRC_3293_HILBERT, "3293 Hilbert source theorem", ["Hilbert-source", "NOT_PARENT_SIGNED"]),
        (SRC_3293_LOCAL, "3293 local source coupling", ["source density", "Maxwell_stress"]),
        (SRC_3294_CONTRACT, "3294 local GR contract", ["single public metric", "Hilbert source"]),
    ]
    rows: list[dict[str, Any]] = []
    for index, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3304_{index}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def overlap_definition_rows() -> list[dict[str, Any]]:
    return [
        {
            "overlap_id": "XI3304_0_scalar_source_charge",
            "quantity": "Xi_0[A]",
            "definition": "Xi_0[A] = Q_0[A] / Q_0^pure[A], where Q_0[A] is the scalar finite-mode charge obtained by projecting the descended matter source of body A onto the scalar mode",
            "pure_metric_limit": "Xi_0[A]=1 for every body A when the scalar mode couples only through the same universal Hilbert stress trace used in pure metric quadratic gravity",
            "nonuniversal_signal": "Xi_0[A] depends on composition, binding energy, EM fraction, clock sector, or hidden source label",
            "valid_for_claim": "false",
        },
        {
            "overlap_id": "XI3304_1_spin2_source_charge",
            "quantity": "Xi_2[A]",
            "definition": "Xi_2[A] = Q_2[A] / Q_2^pure[A], where Q_2[A] is the massive spin-2 finite-mode charge obtained by projecting the descended matter source of body A onto the spin-2 mode",
            "pure_metric_limit": "Xi_2[A]=1 for every body A when the massive spin-2 mode couples only through the same conserved Hilbert tensor as the massless graviton",
            "nonuniversal_signal": "Xi_2[A] depends on stress anisotropy, EM stress treatment, hidden connection/readout factors, or species weights",
            "valid_for_claim": "false",
        },
        {
            "overlap_id": "XI3304_2_pair_charge",
            "quantity": "Xi_i[A] Xi_i[B]",
            "definition": "finite-mode force between bodies A and B depends on the product of their normalized source charges, not on a body-independent alpha unless Xi_i is universal",
            "pure_metric_limit": "Xi_i[A] Xi_i[B]=1 for all A,B",
            "nonuniversal_signal": "fifth-force strength becomes composition-pair dependent",
            "valid_for_claim": "false",
        },
    ]


def pairwise_force_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "PAIR3304_0_general_pair_potential",
            "formula": "V_AB(r) = -G_cal m_A m_B/r [1 + alpha0_star Xi_0[A] Xi_0[B] exp(-r/lambda_0) + alpha2_star Xi_2[A] Xi_2[B] exp(-r/lambda_2)]",
            "definitions": "alpha0_star=(1/3)Z_0U_0 and alpha2_star=(-4/3)Z_2U_2; Xi factors carry source projection/composition dependence",
            "pure_limit": "Xi_0[A]=Xi_0[B]=Xi_2[A]=Xi_2[B]=1 and Z_i=U_i=1",
            "valid_for_claim": "false",
        },
        {
            "law_id": "PAIR3304_1_universal_reduction",
            "formula": "If Xi_i[A]=Xi_i[B]=1 for all bodies, the pair law reduces to the 3303 generalized alpha law with alpha_i=alpha_i_star",
            "definitions": "universal Hilbert source makes finite-mode charge proportional to inertial/Newtonian mass",
            "pure_limit": "recovers pure metric +1/3 and -4/3 when Z_i=U_i=1",
            "valid_for_claim": "false",
        },
        {
            "law_id": "PAIR3304_2_source_weight_warning",
            "formula": "If Xi_i[A] != Xi_i[B] for different materials, alpha_i cannot be entered as one universal R10/PPN number",
            "definitions": "the branch becomes a WEP/source-composition problem before it is a simple Yukawa curve problem",
            "pure_limit": "no warning when Xi_i is universal",
            "valid_for_claim": "false",
        },
    ]


def universality_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "XIU3304_0_same_matter_action",
            "clause": "one descended matter action S_m[g_pub,Psi,theta] owns all local source tensors and currents",
            "effect_if_signed": "source charge Q_i[A] is derived from the same variational object that defines inertial mass",
            "current_status": "EXACT_CONDITIONAL_FROM_3293_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "XIU3304_1_no_species_weights",
            "clause": "no post-variation species weights, source labels, or hidden material selectors multiply finite-mode source charge",
            "effect_if_signed": "Xi_i[A] cannot acquire arbitrary material dependence after variation",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "XIU3304_2_projector_same_as_pure_limit",
            "clause": "finite scalar/spin-2 projectors act on the Hilbert stress in the same way as the pure metric quadratic branch",
            "effect_if_signed": "Xi_0=Xi_2=1 after normalization in the nonrelativistic local limit",
            "current_status": "MISSING_LINEARIZED_PARENT_PROJECTOR",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "XIU3304_3_EM_and_binding_energy_included",
            "clause": "EM stress, Poynting flow, binding energy, and clock/readout contributions enter the same Hilbert tensor with no double count",
            "effect_if_signed": "composition-dependent EM/binding-energy leakage does not create Xi differences",
            "current_status": "CONDITIONAL_FROM_HILBERT_EM_BRANCH_NOT_FULLY_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "XIU3304_4_public_metric_readout",
            "clause": "the metric used to define matter stress is the same metric read by rods/clocks/orbital bodies",
            "effect_if_signed": "readout factors stay in U_i rather than masquerading as source-charge nonuniversality",
            "current_status": "CONDITIONAL_FROM_3294_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def wep_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "WEP3304_0_scalar_delta",
            "quantity": "Delta_Xi_0[A,B] = Xi_0[A] - Xi_0[B]",
            "observable_template": "eta_AB,E^(0) ~= alpha0_star Xi_0[E] Delta_Xi_0[A,B] (1+r/lambda_0) exp(-r/lambda_0)",
            "meaning": "scalar finite-mode composition residual for two test bodies A,B falling toward source E",
            "status": "BOUND_REQUIRED_IF_XI_NOT_PROVEN_UNIVERSAL",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "WEP3304_1_spin2_delta",
            "quantity": "Delta_Xi_2[A,B] = Xi_2[A] - Xi_2[B]",
            "observable_template": "eta_AB,E^(2) ~= alpha2_star Xi_2[E] Delta_Xi_2[A,B] (1+r/lambda_2) exp(-r/lambda_2)",
            "meaning": "massive spin-2 finite-mode composition residual",
            "status": "BOUND_REQUIRED_IF_XI_NOT_PROVEN_UNIVERSAL",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "WEP3304_2_combined",
            "quantity": "eta_AB,E",
            "observable_template": "eta_AB,E ~= sum_i alpha_i_star Xi_i[E] Delta_Xi_i[A,B] (1+r/lambda_i) exp(-r/lambda_i) for small residuals",
            "meaning": "first-order Eotvos-style residual; must be below WEP bounds before any finite-mode claim",
            "status": "NONCLAIM_TEST_FORM",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3304_0",
            "question": "Are Xi_0 and Xi_2 proven universal?",
            "answer": "no",
            "reason": "the exact universality clauses are written, but the parent action/projector/readout evidence is still conditional or missing",
            "next_action": "derive the projector from the descended matter action or keep WEP residual rows alive",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3304_1",
            "question": "What changed?",
            "answer": "the coupling gap is now a body-pair source-charge law plus an explicit WEP residual, not an undefined missing coupling",
            "reason": "finite-mode tests now know whether they are universal-alpha tests or composition-dependent source tests",
            "next_action": "attempt the parent projector proof for Xi_i[A]=1; if it fails, populate WEP bound inputs",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3304_0_Xi_universal",
            "claim": "Xi_0[A]=Xi_2[A]=1 for all local matter bodies",
            "requirements": "same matter action, no species weights, pure-limit projectors, EM/binding energy included once, public metric readout",
            "current_evidence": "all clauses are conditional or missing",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3304_1_WEP_safe",
            "claim": "composition residuals are below WEP/source bounds",
            "requirements": "numeric or bounded Delta_Xi_i[A,B], alpha_i_star, lambda_i, and source Xi_i[E] with WEP bound source",
            "current_evidence": "symbolic residual map only",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3304_2_universal_alpha_scoring",
            "claim": "finite quadratic branch can be scored with one universal alpha(lambda)",
            "requirements": "GATE3304_0 true or composition residuals proven negligible",
            "current_evidence": "not ready",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3304_0_3305",
            "target_doc": "3305-Y5-R2FR-parent-projector-proof-for-Xi-universality-or-WEP-bound-pack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3305_parent_projector_proof_for_Xi_universality_or_WEP_bound_pack.py",
            "objective": "try to prove Xi_i[A]=1 from the parent matter projector; if not, build the WEP/source-composition bound pack for Delta_Xi_0 and Delta_Xi_2",
            "guardrails": "do not collapse pairwise Xi_i[A]Xi_i[B] into one alpha unless universality is proven; do not ignore EM/Poynting/binding-energy source contributions",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_paths = [Path(row["path"]) for row in source_rows]
    outputs_to_parse = [path for key, path in OUTPUTS.items() if key != "validation"]
    overlap_rows = overlap_definition_rows()
    pairwise_rows = pairwise_force_rows()
    universality_rows = universality_clause_rows()
    wep_rows = wep_residual_rows()
    gates = promotion_gate_rows()
    next_rows = next_target_rows()

    checks = [
        (
            "VAL3304_0_sources_exist",
            "all cited source paths exist",
            all(path.exists() for path in source_paths),
            "",
        ),
        (
            "VAL3304_1_sources_parse",
            "all cited source paths parse",
            all(parse_ok(path) for path in source_paths),
            "",
        ),
        (
            "VAL3304_2_outputs_parse",
            "all 3304 non-validation output CSVs parse",
            all(csv_parse_ok(path) for path in outputs_to_parse),
            "",
        ),
        (
            "VAL3304_3_Xi_definitions_present",
            "Xi_0[A] and Xi_2[A] definitions are present",
            any("Xi_0[A]" in row["quantity"] for row in overlap_rows)
            and any("Xi_2[A]" in row["quantity"] for row in overlap_rows),
            "",
        ),
        (
            "VAL3304_4_pairwise_force_law_present",
            "pairwise force law keeps Xi_i[A]Xi_i[B] body dependence",
            any("Xi_0[A] Xi_0[B]" in row["formula"] and "Xi_2[A] Xi_2[B]" in row["formula"] for row in pairwise_rows),
            "",
        ),
        (
            "VAL3304_5_universality_clauses_complete",
            "universality proof clauses include matter action, species weights, projectors, EM/binding, and readout",
            all(
                any(needle in row["clause_id"] for row in universality_rows)
                for needle in ["same_matter", "no_species", "projector", "EM", "public_metric"]
            ),
            "",
        ),
        (
            "VAL3304_6_WEP_residuals_present",
            "WEP residual map includes scalar, spin-2, and combined Eotvos templates",
            all(any(row["residual_id"].startswith(prefix) for row in wep_rows) for prefix in ["WEP3304_0", "WEP3304_1", "WEP3304_2"]),
            "",
        ),
        (
            "VAL3304_7_claim_gates_false",
            "all Xi/WEP/universal-alpha gates remain false",
            all(row["passed"] == "false" and row["valid_for_claim"] == "false" for row in gates),
            "",
        ),
        (
            "VAL3304_8_next_target_projector_or_WEP",
            "next target is parent projector proof or WEP bound pack",
            "parent-projector-proof" in next_rows[0]["target_doc"] and "WEP-bound-pack" in next_rows[0]["target_doc"],
            "",
        ),
    ]

    formalization_after = snapshot_tree(FW)
    formalization_changed = changed_count(formalization_before, formalization_after)
    checks.append(
        (
            "VAL3304_9_formalization_untouched",
            "formalization-workbench modified-file count remains zero by this script",
            formalization_changed == 0,
            f"formalization_changed_count={formalization_changed}",
        )
    )

    overall = all(passed for _, _, passed, _ in checks)
    checks.append(
        (
            "VAL3304_10_overall",
            "3304 validation overall",
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
    overlap_table = "\n".join(
        f"- `{row['overlap_id']}` `{row['quantity']}`: {row['definition']}"
        for row in overlap_definition_rows()
    )
    force_table = "\n".join(
        f"- `{row['law_id']}`: `{row['formula']}`"
        for row in pairwise_force_rows()
    )
    universality_table = "\n".join(
        f"- `{row['clause_id']}`: {row['clause']} Status: `{row['current_status']}`."
        for row in universality_clause_rows()
    )
    wep_table = "\n".join(
        f"- `{row['residual_id']}` `{row['quantity']}`: `{row['observable_template']}`"
        for row in wep_residual_rows()
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

    return f"""# 3304 - Source-projection overlap law for alpha factors under AX1090

Run UTC: `{RUN_UTC}`

## Verdict

The coupling problem is now a source-charge overlap law.

The finite-mode force between two bodies is not safely represented by one universal `alpha_i` unless the source-projection factors are universal:

`V_AB(r) = -G_cal m_A m_B/r [1 + alpha0_star Xi_0[A] Xi_0[B] exp(-r/lambda_0) + alpha2_star Xi_2[A] Xi_2[B] exp(-r/lambda_2)]`.

So the clean route to local GR is either:

1. prove `Xi_0[A]=Xi_2[A]=1` for all local matter from the parent Hilbert/source projector; or
2. keep the WEP/source-composition residuals alive and bound `Delta_Xi_i[A,B]`.

No universal-alpha or local-GR claim is made here.

## Source Register

{source_table}

## Xi Definitions

{overlap_table}

## Pairwise Force Law

{force_table}

## Universality Clauses

{universality_table}

## WEP Residual Map

{wep_table}

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
    write_csv(OUTPUTS["overlap"], overlap_definition_rows())
    write_csv(OUTPUTS["pairwise"], pairwise_force_rows())
    write_csv(OUTPUTS["universality"], universality_clause_rows())
    write_csv(OUTPUTS["wep"], wep_residual_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["promotion"], promotion_gate_rows())
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

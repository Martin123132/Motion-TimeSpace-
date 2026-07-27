from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3898"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3898-Y5-R2FR-parent-readout-coefficient-zero-or-gamma-Gdot-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3898_SOURCE_REGISTER.csv",
    "slots": SRC / "P8_Y5_R2FR_3898_READOUT_ALLOWED_FORBIDDEN_SLOTS.csv",
    "coeff": SRC / "P8_Y5_R2FR_3898_PARENT_READOUT_COEFFICIENT_ZERO_ATTEMPT.csv",
    "fill": SRC / "P8_Y5_R2FR_3898_GAMMA_GDOT_FILL_FORMULAS.csv",
    "gate": SRC / "P8_Y5_R2FR_3898_LOCAL_GR_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3898_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3898_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3898_VALIDATION.csv",
}

SCALAR_READOUT_RULE = "Obs_g[X] may use scalar coefficients multiplying existing GR tensors, but may not manufacture vector or traceless-tensor structures without parent vector/tensor data"
VECTOR_ZERO = "c_vec=0 by representation: scalar X cannot source a vector g_0i preferred-frame readout without u^i, spin, boundary normal, or projector anisotropy"
ANISO_ZERO = "c_aniso=0 by representation: scalar X cannot source a traceless spatial tensor without anisotropic parent data"
CONFORMAL_GAMMA_ZERO = "c_space-c_lapse=0 only if X enters the observed metric as a common conformal/calibration factor"
GDOT_ZERO = "delta(Gdot/G)=0 only if X is stationary or the Newtonian calibration absorbs constant X with partial_t X=0"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    return str(path.relative_to(PCW)) if path.is_relative_to(PCW) else str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3898_00_next", SRC / "P8_Y5_R2FR_3897_NEXT_TARGET.csv", "NEXT3897_0", "3897 selected parent readout coefficient target"),
        ("SRC3898_01_ki", SRC / "P8_Y5_R2FR_3897_MEMORY_KI_PROJECTION_DERIVATION.csv", "KI3897_0_alpha3", "3897 K_i projection map"),
        ("SRC3898_02_readout", SRC / "P8_Y5_R2FR_3897_MEMORY_READOUT_DECOMPOSITION.csv", "RO3897_0_decomp", "3897 readout decomposition"),
        ("SRC3898_03_zero", SRC / "P8_Y5_R2FR_3897_SYMMETRY_ZERO_CANDIDATE_ROWS.csv", "ZK3897_0_preferred_frame", "3897 symmetry-zero candidates"),
        ("SRC3898_04_physical", SRC / "P8_Y5_R2FR_3897_FIRST_PHYSICAL_MEMORY_ROW_SKELETON.csv", "PHY3897_1_gamma_coefficient_row", "3897 physical row skeleton"),
        ("SRC3898_05_validation", SRC / "P8_Y5_BRR545_3897_VALIDATION.csv", "VAL3897_15_next_target", "3897 validation"),
        ("SRC3898_06_3889_grammar", SRC / "P8_Y5_R2FR_3889_PARENT_OBJECT_LANGUAGE_NO_DIRECT_SOURCE_THEOREM.csv", "Hom_parent", "parent object-language no-direct-source theorem"),
        ("SRC3898_07_3890_action", SRC / "P8_Y5_R2FR_3890_PARENT_ACTION_GRAMMAR_INSERTION.csv", "S_matter^q", "candidate parent grammar insertion"),
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


def slot_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"slot_id": "SLOT3898_0_allowed_scalar", "slot": "scalar/conformal coefficient", "rule": "allowed: X multiplies g_GR or existing scalar potentials", "effect": "can affect gamma/G calibration unless conformal equality holds", "status": "ALLOWED_SCALAR_SLOT", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"slot_id": "SLOT3898_1_forbidden_vector", "slot": "vector preferred-frame readout", "rule": "forbidden unless parent supplies u^i, spin/current, moving wall, or anisotropic projector", "effect": "kills alpha3/alpha2 source if signed", "status": "FORBIDDEN_BY_SCALAR_PARENT_GRAMMAR_CANDIDATE", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"slot_id": "SLOT3898_2_forbidden_aniso", "slot": "traceless anisotropic tensor readout", "rule": "forbidden unless parent supplies T_ij, boundary normal n_i n_j, or projector anisotropy", "effect": "kills xi source if signed", "status": "FORBIDDEN_BY_SCALAR_PARENT_GRAMMAR_CANDIDATE", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"slot_id": "SLOT3898_3_open_disformal", "slot": "lapse/spatial mismatch", "rule": "not forbidden by scalarity; scalar X may couple differently to g_00 and g_ij unless conformal readout is signed", "effect": "gamma remains open through c_space-c_lapse", "status": "OPEN_SCALAR_SLOT", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"slot_id": "SLOT3898_4_open_calibration", "slot": "G/clock/EM calibration response", "rule": "not forbidden by scalarity; constants may respond to X unless quotient calibration is signed", "effect": "Gdot/clock remain open", "status": "OPEN_CALIBRATION_SLOT", "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def coefficient_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"coeff_id": "COEFF3898_0_c_vec", "coefficient": "c_vec", "attempted_zero": VECTOR_ZERO, "status": "PASS_IF_PARENT_SCALAR_GRAMMAR_SIGNED", "remaining_escape": "velocity/spin/current, moving wall, boundary normal, or projector anisotropy", "local_bound_relief": "alpha3/alpha2 preferred-frame pressure can be avoided by symmetry", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"coeff_id": "COEFF3898_1_c_aniso", "coefficient": "c_aniso", "attempted_zero": ANISO_ZERO, "status": "PASS_IF_PARENT_SCALAR_GRAMMAR_SIGNED", "remaining_escape": "anisotropic boundary/projector/domain tensor", "local_bound_relief": "xi preferred-location pressure can be avoided by symmetry", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"coeff_id": "COEFF3898_2_c_gamma", "coefficient": "c_space-c_lapse", "attempted_zero": CONFORMAL_GAMMA_ZERO, "status": "NOT_ZERO_BY_SCALARITY_ALONE", "remaining_escape": "disformal/lapse-only/spatial-only readout", "local_bound_relief": "requires conformal observed metric or numeric bound", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"coeff_id": "COEFF3898_3_c_G", "coefficient": "c_G and partial_t X", "attempted_zero": GDOT_ZERO, "status": "NOT_ZERO_BY_SCALARITY_ALONE", "remaining_escape": "time-varying memory/history tail or changing calibration", "local_bound_relief": "requires stationary X or numeric Gdot bound", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"coeff_id": "COEFF3898_4_c_R10", "coefficient": "c_R10, lambda_X", "attempted_zero": "c_R10=0 only if memory does not mediate an independent scalar fifth-force channel to source mass", "status": "OPEN_MEDIATOR_COUPLING", "remaining_escape": "Yukawa mediator/source coupling", "local_bound_relief": "requires R10 alpha(lambda) bound comparison", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"coeff_id": "COEFF3898_5_c_clock", "coefficient": "c_clock_ab", "attempted_zero": "c_clock_ab=0 only if EM/mass calibration constants are quotient-owned and X-null", "status": "OPEN_EM_CALIBRATION_UNTIL_SIGNED", "remaining_escape": "fine-structure/mass-ratio/clock calibration response", "local_bound_relief": "requires clock coefficient or exact quotient calibration", "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def fill_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"fill_id": "FILL3898_0_alpha3", "observable": "alpha3", "runner_coefficient": "K_alpha3=0", "condition": "c_vec=0 and c_aniso=0 parent-signed; no boundary/projector vector leakage", "bound_formula": "Delta alpha3=0", "fill_status": "CANDIDATE_ZERO_ROW_READY_PARENT_UNSIGNED", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"fill_id": "FILL3898_1_xi", "observable": "xi", "runner_coefficient": "K_xi=0", "condition": "c_aniso=0 and topological projector/domain signed", "bound_formula": "Delta xi=0", "fill_status": "CANDIDATE_ZERO_ROW_READY_PARENT_UNSIGNED", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"fill_id": "FILL3898_2_gamma", "observable": "gamma-1", "runner_coefficient": "K_gamma=|c_space-c_lapse|", "condition": "derive conformal equality or numeric mismatch", "bound_formula": "|gamma-1| <= |c_space-c_lapse| X_bound <= 2.3e-5", "fill_status": "FORMULA_READY_COEFFICIENT_MISSING", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"fill_id": "FILL3898_3_Gdot", "observable": "Gdot/G", "runner_coefficient": "K_Gdot=|c_G| with partial_t X bound", "condition": "derive stationary X or c_G/time-derivative bound", "bound_formula": "|Gdot/G| <= |c_G| |partial_t X| <= 9.6e-15 yr^-1", "fill_status": "FORMULA_READY_COEFFICIENT_MISSING", "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"gate_id": "LGG3898_0_vector_zero", "gate": "c_vec preferred-frame coefficient", "result": "zero by scalar representation if parent grammar forbids vector slots", "status": "CANDIDATE_PASS_PARENT_UNSIGNED", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3898_1_aniso_zero", "gate": "c_aniso preferred-location coefficient", "result": "zero by scalar representation if parent grammar forbids anisotropic slots", "status": "CANDIDATE_PASS_PARENT_UNSIGNED", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3898_2_gamma", "gate": "gamma scalar coefficient", "result": "not zero by scalarity alone; conformal equality or numeric coefficient required", "status": "OPEN_CONFORMAL_OR_BOUND", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3898_3_Gdot", "gate": "Gdot scalar coefficient", "result": "not zero by scalarity alone; stationarity/calibration or numeric derivative required", "status": "OPEN_STATIONARY_OR_BOUND", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3898_4_local_GR", "gate": "local-GR promotion", "result": "no claim until parent signs no vector/aniso leakage and scalar channels are conformal/stationary or bounded", "status": "BLOCKED_NO_CLAIM_COEFFICIENT_SPLIT_DERIVED", "claim_allowed": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3898_0",
            "target_checkpoint": "3899-Y5-R2FR-conformal-readout-stationary-memory-proof-or-scalar-bound-fill.md",
            "script": "scripts/Y5_R2FR_3899_conformal_readout_stationary_memory_proof_or_scalar_bound_fill.py",
            "objective": "try to prove conformal observed readout c_space=c_lapse and stationary local memory partial_t X=0; if either fails, fill scalar bound rows for gamma and Gdot",
            "why_next": "3898 likely neutralizes the brutal preferred-frame channels by symmetry, leaving gamma and Gdot as the real scalar coefficient fight",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PARENT_READOUT_COEFFICIENT_SPLIT",
            "claim": "NO_LOCAL_GR_CLAIM",
            "summary": "candidate proof zeros vector/anisotropic coefficients under scalar parent readout; gamma and Gdot remain open scalar channels needing conformal/stationary proof or numeric bounds",
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
    slots: list[dict[str, Any]],
    coeff: list[dict[str, Any]],
    fill: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    timestamp: str,
) -> None:
    doc = f"""# 3898 - Parent Readout Coefficient Zero or Gamma/Gdot Fill

Generated: `{timestamp}`

## Result

3898 attacks the readout coefficients directly.

Parent readout rule:

`{SCALAR_READOUT_RULE}`

Candidate wins:

- `{VECTOR_ZERO}`;
- `{ANISO_ZERO}`.

Hard stop:

- `{CONFORMAL_GAMMA_ZERO}`;
- `{GDOT_ZERO}`.

So the route improves: the brutal preferred-frame/location rows can become symmetry-zero if the parent readout grammar is signed. But `gamma`, `Gdot`, `R10`, and clock/EM calibration are not solved by scalarity alone.

## Allowed and Forbidden Readout Slots

{markdown_table(slots, ["slot_id", "slot", "rule", "effect", "status"])}

## Coefficient-Zero Attempt

{markdown_table(coeff, ["coeff_id", "coefficient", "attempted_zero", "status", "remaining_escape", "local_bound_relief"])}

## Gamma/Gdot Fill Formulas

{markdown_table(fill, ["fill_id", "observable", "runner_coefficient", "condition", "bound_formula", "fill_status"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "result", "status", "claim_allowed"])}

## Source Register

Resolved `{sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is a real split in the local-GR problem. Preferred-frame trouble is probably not the main monster if the readout is genuinely scalar. The next monster is proving conformal readout/stationary memory, or bounding the scalar gamma/Gdot leakage honestly.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3898 PARENT READOUT COEFFICIENT SPLIT -->
## 3898 Parent Readout Coefficient Zero or Gamma/Gdot Fill

Timestamp: `{timestamp}`

Result: `PASS_PARENT_READOUT_COEFFICIENT_SPLIT`.

Parent readout rule:
`{SCALAR_READOUT_RULE}`

Candidate coefficient zeros:
- `{VECTOR_ZERO}`;
- `{ANISO_ZERO}`.

Open scalar channels:
- `{CONFORMAL_GAMMA_ZERO}`;
- `{GDOT_ZERO}`;

Decision: no local-GR claim. Preferred-frame/location rows look symmetry-controllable; gamma and Gdot are the next real scalar leakage fight.

Next gate: `3899`, conformal readout and stationary memory proof or scalar bound fill.
<!-- END 3898 PARENT READOUT COEFFICIENT SPLIT -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3898 PARENT READOUT COEFFICIENT SPLIT -->"
    end = "<!-- END 3898 PARENT READOUT COEFFICIENT SPLIT -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    slots: list[dict[str, Any]],
    coeff: list[dict[str, Any]],
    fill: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = [row for row in sources if row["exists"] and row["needle_found"]]
    checks.append(("VAL3898_0_sources", "all source paths and needles resolve", len(resolved) == len(sources), f"{len(resolved)}/{len(sources)} sources resolved"))
    checks.append(("VAL3898_1_slots", "allowed/forbidden slots present", {"SLOT3898_1_forbidden_vector", "SLOT3898_2_forbidden_aniso", "SLOT3898_3_open_disformal"}.issubset({str(row["slot_id"]) for row in slots}), f"{len(slots)} slots"))
    checks.append(("VAL3898_2_cvec", "c_vec candidate zero exists", any(row["coefficient"] == "c_vec" and "PASS_IF_PARENT" in str(row["status"]) for row in coeff), "COEFF3898_0"))
    checks.append(("VAL3898_3_caniso", "c_aniso candidate zero exists", any(row["coefficient"] == "c_aniso" and "PASS_IF_PARENT" in str(row["status"]) for row in coeff), "COEFF3898_1"))
    checks.append(("VAL3898_4_gamma_open", "gamma not zero by scalarity alone", any(row["coefficient"] == "c_space-c_lapse" and "NOT_ZERO" in str(row["status"]) for row in coeff), "COEFF3898_2"))
    checks.append(("VAL3898_5_Gdot_open", "Gdot not zero by scalarity alone", any(row["coefficient"] == "c_G and partial_t X" and "NOT_ZERO" in str(row["status"]) for row in coeff), "COEFF3898_3"))
    checks.append(("VAL3898_6_fill", "gamma/Gdot fill formulas exist", {"FILL3898_2_gamma", "FILL3898_3_Gdot"}.issubset({str(row["fill_id"]) for row in fill}), f"{len(fill)} fills"))
    checks.append(("VAL3898_7_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3898_4_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3898_4"))
    checks.append(("VAL3898_8_all_nonclaim", "all generated rows are nonclaim", all(str(row.get("valid_for_claim", row.get("claim_allowed", False))) == "False" for collection in [slots, coeff, fill, gate] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3898_9_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "real split" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3898_10_spine", "spine updated with 3898 block", SPINE_PATH.exists() and "BEGIN 3898 PARENT READOUT COEFFICIENT SPLIT" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3898_11_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3898*")
            if path.is_file() and ("3898-Y5" in path.name or "P8_Y5_R2FR_3898" in path.name or "P8_Y5_BRR545_3898" in path.name)
        ]
    checks.append(("VAL3898_12_formalization_untouched", "no generated 3898 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3898_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3898_14_next_target", "next target attacks conformal/stationary scalar channel", any("conformal-readout-stationary" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3899 conformal/stationary"))
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
    slots = slot_rows(timestamp)
    coeff = coefficient_rows(timestamp)
    fill = fill_rows(timestamp)
    gate = gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["slots"], slots)
    write_csv(OUTPUTS["coeff"], coeff)
    write_csv(OUTPUTS["fill"], fill)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, slots, coeff, fill, gate, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, slots, coeff, fill, gate, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_PARENT_READOUT_COEFFICIENT_SPLIT")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3897"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3897-Y5-R2FR-derive-memory-Ki-projection-or-fill-first-physical-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3897_SOURCE_REGISTER.csv",
    "readout": SRC / "P8_Y5_R2FR_3897_MEMORY_READOUT_DECOMPOSITION.csv",
    "ki": SRC / "P8_Y5_R2FR_3897_MEMORY_KI_PROJECTION_DERIVATION.csv",
    "zeros": SRC / "P8_Y5_R2FR_3897_SYMMETRY_ZERO_CANDIDATE_ROWS.csv",
    "physical": SRC / "P8_Y5_R2FR_3897_FIRST_PHYSICAL_MEMORY_ROW_SKELETON.csv",
    "gate": SRC / "P8_Y5_R2FR_3897_LOCAL_GR_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3897_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3897_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3897_VALIDATION.csv",
}

READOUT_DECOMP = "D_X g_obs = 2 c_conf X g_GR + c_lapse X U dt^2 + c_space X U delta_ij dx^i dx^j + c_vec X V_(i) dt dx^i + c_aniso X T_ij dx^i dx^j + gradient terms"
GAMMA_FORMULA = "delta gamma = (c_space-c_lapse) X_mem"
GDOT_FORMULA = "delta(Gdot/G) = c_G partial_t X_mem"
R10_FORMULA = "alpha_R10 = c_R10 X_mem, so |alpha_R10| <= |c_R10| X_bound"
CLOCK_FORMULA = "delta ln(nu_a/nu_b) = c_clock_ab X_mem + c_clock_grad_ab grad X_mem"


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
        ("SRC3897_00_next", SRC / "P8_Y5_R2FR_3896_NEXT_TARGET.csv", "NEXT3896_0", "3896 selected K_i projection target"),
        ("SRC3897_01_runner", SRC / "P8_Y5_R2FR_3896_MEMORY_SUPPRESSION_RUNNER_DRYRUN.csv", "LIVE3896_placeholder", "3896 executable runner"),
        ("SRC3897_02_bounds", SRC / "P8_Y5_R2FR_3896_LOCAL_BOUND_ANCHOR_ROWS.csv", "BND3896_0_alpha3", "3896 local bound anchors"),
        ("SRC3897_03_schema", SRC / "P8_Y5_R2FR_3896_MEMORY_SUPPRESSION_INPUT_SCHEMA.csv", "K_i", "3896 runner K_i input schema"),
        ("SRC3897_04_validation", SRC / "P8_Y5_BRR545_3896_VALIDATION.csv", "VAL3896_13_next_target", "3896 validation"),
        ("SRC3897_05_3890_direct", SRC / "P8_Y5_R2FR_3890_DIRECT_SOURCE_ZERO_UPDATE.csv", "DZU3890_1_delta_w", "direct hidden/source zero context"),
        ("SRC3897_06_3892_projector", SRC / "P8_Y5_R2FR_3892_PROJECTOR_ABSOLUTE_TOPOLOGICAL_CERTIFICATE.csv", "PC3892", "projector/topological silence context"),
        ("SRC3897_07_3895_zero", SRC / "P8_Y5_R2FR_3895_MEMORY_BOUNDARY_HISTORY_ZERO_ATTEMPT.csv", "ZERO3895_4_history_exact", "history exact-zero rejection"),
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


def readout_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "piece_id": "RO3897_0_decomp",
            "readout_piece": "linear memory-to-metric map",
            "formula": READOUT_DECOMP,
            "meaning": "separates scalar/conformal, lapse, spatial, vector, anisotropic, and gradient response channels",
            "status": "DERIVED_PROJECTION_BASIS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "piece_id": "RO3897_1_scalar_only",
            "readout_piece": "scalar-isotropic closure",
            "formula": "c_vec=0 and c_aniso=0 if X_mem is a scalar parent auxiliary and the observed readout contains no vector/tensor hidden representative",
            "meaning": "preferred-frame/location channels cannot be sourced by a pure scalar isotropic readout at linear order",
            "status": "CANDIDATE_SYMMETRY_ZERO_PARENT_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "piece_id": "RO3897_2_gamma",
            "readout_piece": "PPN gamma channel",
            "formula": GAMMA_FORMULA,
            "meaning": "gamma only sees the mismatch between spatial and lapse response coefficients",
            "status": "DERIVED_SYMBOLIC_K_GAMMA",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "piece_id": "RO3897_3_Gdot",
            "readout_piece": "local G drift channel",
            "formula": GDOT_FORMULA,
            "meaning": "Gdot requires time-varying memory or a nonzero c_G calibration response",
            "status": "DERIVED_SYMBOLIC_K_GDOT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def ki_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "ki_id": "KI3897_0_alpha3",
            "arena": "PPN/preferred-frame",
            "observable": "alpha3",
            "projection_formula": "K_alpha3=0 if c_vec=0, c_aniso=0, no spin/current memory readout, and no moving boundary projector; otherwise K_alpha3=|D_X alpha3|",
            "derived_status": "CANDIDATE_ZERO_BY_SCALAR_ISOTROPY",
            "needed_parent_clause": "X_mem scalar; readout has no vector/tensor representative; boundary/projector silent",
            "bound_anchor": "4e-20",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "ki_id": "KI3897_1_alpha2",
            "arena": "PPN/preferred-frame",
            "observable": "alpha2",
            "projection_formula": "K_alpha2=0 under the same scalar-isotropic/no-vector readout; otherwise K_alpha2=|D_X alpha2|",
            "derived_status": "CANDIDATE_ZERO_BY_SCALAR_ISOTROPY",
            "needed_parent_clause": "no preferred-frame vector in D_X g_obs",
            "bound_anchor": "2e-9",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "ki_id": "KI3897_2_xi",
            "arena": "PPN/preferred-location",
            "observable": "xi",
            "projection_formula": "K_xi=0 if c_aniso=0 and projector/domain are topological; otherwise K_xi=|D_X xi|",
            "derived_status": "CANDIDATE_ZERO_BY_ISOTROPY_TOPOLOGY",
            "needed_parent_clause": "no anisotropic background tensor and projector certificate signed",
            "bound_anchor": "4e-9",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "ki_id": "KI3897_3_gamma",
            "arena": "PPN/light deflection/R10 gamma-scale",
            "observable": "gamma-1",
            "projection_formula": "K_gamma=|c_space-c_lapse| with delta gamma=(c_space-c_lapse)X_mem",
            "derived_status": "SYMBOLIC_COEFFICIENT_DERIVED_NUMERIC_VALUE_MISSING",
            "needed_parent_clause": "derive c_space and c_lapse from observed metric readout",
            "bound_anchor": "2.3e-5",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "ki_id": "KI3897_4_Gdot",
            "arena": "clock/orbital/local-G drift",
            "observable": "Gdot/G",
            "projection_formula": "K_Gdot=|c_G| for delta(Gdot/G)=c_G partial_t X_mem",
            "derived_status": "SYMBOLIC_COEFFICIENT_DERIVED_NUMERIC_VALUE_MISSING",
            "needed_parent_clause": "derive c_G and partial_t X_mem bound from calibration/readout map",
            "bound_anchor": "9.6e-15 yr^-1",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "ki_id": "KI3897_5_R10",
            "arena": "short-range fifth force",
            "observable": "alpha_R10(lambda)",
            "projection_formula": R10_FORMULA,
            "derived_status": "SYMBOLIC_COEFFICIENT_DERIVED_BOUND_CURVE_STILL_NEEDED",
            "needed_parent_clause": "derive c_R10 and lambda_X from local memory mediator",
            "bound_anchor": "R10 alpha(lambda) curve",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "ki_id": "KI3897_6_clock",
            "arena": "clock/EM stress",
            "observable": "clock-ratio drift",
            "projection_formula": CLOCK_FORMULA,
            "derived_status": "SYMBOLIC_COEFFICIENT_DERIVED_NUMERIC_VALUE_MISSING",
            "needed_parent_clause": "derive c_clock_ab and EM/mass calibration dependence on X_mem",
            "bound_anchor": "clock comparison bound row not yet selected",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "ki_id": "KI3897_7_orbital",
            "arena": "orbital/Newtonian limit",
            "observable": "delta orbital residual",
            "projection_formula": "K_orbital is built from K_gamma, K_Gdot, K_beta, and any Yukawa radial derivative d alpha_R10/dX",
            "derived_status": "COMPOSITE_SYMBOLIC_MAP",
            "needed_parent_clause": "derive beta/nonlinear metric response and local source calibration",
            "bound_anchor": "orbital residual bound row not yet selected",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def zero_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "zero_id": "ZK3897_0_preferred_frame",
            "zero_candidate": "alpha3 and alpha2",
            "reason": "A scalar isotropic memory perturbation has no vector preferred-frame tensor at linear order, so it cannot populate g_0i preferred-frame structures.",
            "parent_signature_required": "c_vec=0 plus no spin/current hidden readout and fixed boundary/projector",
            "status": "CANDIDATE_EXACT_ZERO_NOT_CLAIMED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "zero_id": "ZK3897_1_preferred_location",
            "zero_candidate": "xi",
            "reason": "A scalar isotropic local branch has no anisotropic location tensor unless boundary/projector/domain data introduces one.",
            "parent_signature_required": "c_aniso=0 plus projector topological certificate",
            "status": "CANDIDATE_EXACT_ZERO_NOT_CLAIMED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "zero_id": "ZK3897_2_not_zero",
            "zero_candidate": "gamma/Gdot/R10/clock",
            "reason": "These channels can be sourced by scalar lapse/spatial/calibration/time-variation coefficients, so they require numeric coefficients or parent symmetry.",
            "parent_signature_required": "c_space=c_lapse, c_G=0, c_R10=0, c_clock=0, or finite bound",
            "status": "NOT_ZERO_BY_SCALARITY_ALONE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def physical_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PHY3897_0_alpha3_symmetry_row",
            "arena": "alpha3",
            "candidate_K_i": "0",
            "physical_condition": "scalar-isotropic readout with c_vec=c_aniso=0 and fixed boundary/projector",
            "runner_use": "if parent-signed, alpha3 memory channel is exact-zero before numeric X_bound",
            "row_status": "CANDIDATE_PHYSICAL_ZERO_PARENT_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PHY3897_1_gamma_coefficient_row",
            "arena": "gamma",
            "candidate_K_i": "|c_space-c_lapse|",
            "physical_condition": "derive lapse/spatial response coefficients from observed metric readout",
            "runner_use": "Delta_gamma_bound=|c_space-c_lapse| X_bound",
            "row_status": "PHYSICAL_FORMULA_READY_COEFFICIENTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PHY3897_2_Gdot_coefficient_row",
            "arena": "Gdot",
            "candidate_K_i": "|c_G| with partial_t X bound",
            "physical_condition": "derive G calibration response and history/time derivative bound",
            "runner_use": "Delta_Gdot/G <= |c_G| |partial_t X_mem|",
            "row_status": "PHYSICAL_FORMULA_READY_COEFFICIENTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"gate_id": "LGG3897_0_readout", "gate": "readout decomposition", "result": "D_X g_obs decomposed into scalar/lapse/spatial/vector/anisotropic/gradient channels", "status": "PASS_SYMBOLIC_MAP", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3897_1_symmetry_zero", "gate": "preferred-frame/location zeros", "result": "alpha3/alpha2/xi can be zero by scalar-isotropy if parent readout forbids vector/anisotropic channels", "status": "CANDIDATE_PASS_PARENT_UNSIGNED", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3897_2_scalar_channels", "gate": "scalar-sensitive channels", "result": "gamma/Gdot/R10/clock/orbital remain coefficient-bound, not zero by scalarity alone", "status": "OPEN_COEFFICIENTS_REQUIRED", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3897_3_local_GR", "gate": "local-GR promotion", "result": "no claim until c_vec/c_aniso zeros and scalar coefficients are parent-derived or bounded", "status": "BLOCKED_NO_CLAIM_PROJECTION_MAP_DERIVED", "claim_allowed": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3897_0",
            "target_checkpoint": "3898-Y5-R2FR-parent-readout-coefficient-zero-or-gamma-Gdot-fill.md",
            "script": "scripts/Y5_R2FR_3898_parent_readout_coefficient_zero_or_gamma_Gdot_fill.py",
            "objective": "try to prove c_vec=c_aniso=0 from the parent observed-readout grammar, then derive or bound c_space-c_lapse and c_G for gamma and Gdot",
            "why_next": "3897 identifies which local bounds are symmetry-zero candidates and which require scalar readout coefficients; the most valuable next move is signing the readout coefficients, not another generic audit",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_MEMORY_KI_PROJECTION_MAP_DERIVED",
            "claim": "NO_LOCAL_GR_CLAIM",
            "summary": "derived symbolic K_i projection map; alpha3/alpha2/xi become candidate symmetry-zero channels under scalar-isotropic readout, while gamma/Gdot/R10/clock/orbital need scalar coefficients",
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
    readout: list[dict[str, Any]],
    ki: list[dict[str, Any]],
    zeros: list[dict[str, Any]],
    physical: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    timestamp: str,
) -> None:
    doc = f"""# 3897 - Derive Memory K_i Projection or Fill First Physical Row

Generated: `{timestamp}`

## Result

3897 derives the symbolic observable projection map for the memory residual.

Readout decomposition:

`{READOUT_DECOMP}`

Main consequences:

- `alpha3`, `alpha2`, and `xi` are candidate exact-zero channels if the parent readout is scalar-isotropic and forbids vector/anisotropic hidden representatives;
- `gamma`, `Gdot`, `R10`, clock, and orbital channels are not killed by scalarity alone;
- the next real derivation target is therefore the parent readout coefficients: `c_vec`, `c_aniso`, `c_space-c_lapse`, `c_G`, `c_R10`, and clock/EM calibration coefficients.

## Readout Decomposition

{markdown_table(readout, ["piece_id", "readout_piece", "formula", "meaning", "status"])}

## K_i Projection Derivation

{markdown_table(ki, ["ki_id", "arena", "observable", "projection_formula", "derived_status", "needed_parent_clause", "bound_anchor"])}

## Symmetry-Zero Candidate Rows

{markdown_table(zeros, ["zero_id", "zero_candidate", "reason", "parent_signature_required", "status"])}

## First Physical Memory Row Skeleton

{markdown_table(physical, ["row_id", "arena", "candidate_K_i", "physical_condition", "runner_use", "row_status"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "result", "status", "claim_allowed"])}

## Source Register

Resolved `{sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is the useful split: the brutal preferred-frame bounds may be avoidable by symmetry, but only if the parent readout really forbids vector/anisotropic memory leakage. The scalar-sensitive channels remain the live fight.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3897 MEMORY KI PROJECTION MAP -->
## 3897 Memory Observable Projection Map

Timestamp: `{timestamp}`

Result: `PASS_MEMORY_KI_PROJECTION_MAP_DERIVED`.

Readout basis:
`{READOUT_DECOMP}`

Candidate symmetry-zero channels:
- `K_alpha3=0`, `K_alpha2=0` if `c_vec=0`, `c_aniso=0`, no spin/current hidden readout, and boundary/projector are fixed;
- `K_xi=0` if `c_aniso=0` and the projector/domain certificate is topological.

Scalar-sensitive channels:
- `{GAMMA_FORMULA}`;
- `{GDOT_FORMULA}`;
- `{R10_FORMULA}`;
- `{CLOCK_FORMULA}`.

Decision: no local-GR claim. The next hard gate is deriving parent readout coefficient zeros and scalar coefficient values.

Next gate: `3898`, parent readout coefficient zero or gamma/Gdot fill.
<!-- END 3897 MEMORY KI PROJECTION MAP -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3897 MEMORY KI PROJECTION MAP -->"
    end = "<!-- END 3897 MEMORY KI PROJECTION MAP -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    readout: list[dict[str, Any]],
    ki: list[dict[str, Any]],
    zeros: list[dict[str, Any]],
    physical: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = [row for row in sources if row["exists"] and row["needle_found"]]
    checks.append(("VAL3897_0_sources", "all source paths and needles resolve", len(resolved) == len(sources), f"{len(resolved)}/{len(sources)} sources resolved"))
    checks.append(("VAL3897_1_decomp", "readout decomposition exists", any(row["piece_id"] == "RO3897_0_decomp" and "c_vec" in str(row["formula"]) for row in readout), "RO3897_0"))
    observables = {str(row["observable"]) for row in ki}
    checks.append(("VAL3897_2_ki_coverage", "K_i coverage includes local arenas", {"alpha3", "alpha2", "xi", "gamma-1", "Gdot/G", "alpha_R10(lambda)", "clock-ratio drift", "delta orbital residual"}.issubset(observables), f"{len(observables)} observables"))
    checks.append(("VAL3897_3_alpha3_zero", "alpha3 candidate zero row exists", any(row["observable"] == "alpha3" and "CANDIDATE_ZERO" in str(row["derived_status"]) for row in ki), "KI3897_0"))
    checks.append(("VAL3897_4_gamma_formula", "gamma coefficient formula exists", any(row["observable"] == "gamma-1" and "c_space-c_lapse" in str(row["projection_formula"]) for row in ki), "KI3897_3"))
    checks.append(("VAL3897_5_Gdot_formula", "Gdot coefficient formula exists", any(row["observable"] == "Gdot/G" and "partial_t X_mem" in str(row["projection_formula"]) for row in ki), "KI3897_4"))
    checks.append(("VAL3897_6_not_all_zero", "scalar-sensitive channels remain open", any(row["zero_id"] == "ZK3897_2_not_zero" and "NOT_ZERO" in str(row["status"]) for row in zeros), "ZK3897_2"))
    checks.append(("VAL3897_7_physical_rows", "first physical row skeleton exists", {"PHY3897_0_alpha3_symmetry_row", "PHY3897_1_gamma_coefficient_row", "PHY3897_2_Gdot_coefficient_row"}.issubset({str(row["row_id"]) for row in physical}), f"{len(physical)} rows"))
    checks.append(("VAL3897_8_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3897_3_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3897_3"))
    checks.append(("VAL3897_9_all_nonclaim", "all generated rows are nonclaim", all(str(row.get("valid_for_claim", row.get("claim_allowed", False))) == "False" for collection in [readout, ki, zeros, physical, gate] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3897_10_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "useful split" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3897_11_spine", "spine updated with 3897 block", SPINE_PATH.exists() and "BEGIN 3897 MEMORY KI PROJECTION MAP" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3897_12_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3897*")
            if path.is_file() and ("3897-Y5" in path.name or "P8_Y5_R2FR_3897" in path.name or "P8_Y5_BRR545_3897" in path.name)
        ]
    checks.append(("VAL3897_13_formalization_untouched", "no generated 3897 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3897_14_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3897_15_next_target", "next target attacks parent readout coefficients", any("parent-readout-coefficient-zero" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3898 readout coefficients"))
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
    readout = readout_rows(timestamp)
    ki = ki_rows(timestamp)
    zeros = zero_rows(timestamp)
    physical = physical_rows(timestamp)
    gate = gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["readout"], readout)
    write_csv(OUTPUTS["ki"], ki)
    write_csv(OUTPUTS["zeros"], zeros)
    write_csv(OUTPUTS["physical"], physical)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, readout, ki, zeros, physical, gate, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, readout, ki, zeros, physical, gate, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_MEMORY_KI_PROJECTION_MAP_DERIVED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

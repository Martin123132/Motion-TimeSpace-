from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3892"
BRANCH = "MTS_R2FR_Y5_BOUNDARY_PROJECTOR_TOPOLOGICAL_CERTIFICATE_OR_FILL_ALPHA3_PROJECTOR_INPUTS_3892"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3892-Y5-R2FR-boundary-projector-topological-certificate-or-fill-alpha3-projector-inputs.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3891_NEXT = OUT / "P8_Y5_R2FR_3891_NEXT_TARGET.csv"
CSV_3891_BP = OUT / "P8_Y5_R2FR_3891_BOUNDARY_PROJECTOR_SILENCE_ATTEMPT.csv"
CSV_3891_FILL = OUT / "P8_Y5_R2FR_3891_NUMERIC_FILL_ROWS.csv"
CSV_3891_GATE = OUT / "P8_Y5_R2FR_3891_LOCAL_GR_DECISION_GATE.csv"
CSV_3891_VALIDATION = OUT / "P8_Y5_BRR545_3891_VALIDATION.csv"
CSV_BOUNDARY_ALPHA3 = OUT / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv"
CSV_BOUNDARY_DECISION = OUT / "P8_BOUNDARY_ALPHA3_DECISION.csv"
CSV_BCOH = OUT / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv"
CSV_BFLUX = OUT / "P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv"
CSV_PIM_CONTRACT = OUT / "P8_PiM_projector_variation_stress_CONTRACT.csv"
CSV_PIM_SILENCE = OUT / "P8_Y5_BRR545_PROJECTOR_SYMPLECTIC_SILENCE_THEOREM_ATTEMPT.csv"
CSV_R11_FILL = OUT / "P8_R11_BOUNDARY_STRESS_CLOSURE_FILL_PACK.csv"
CSV_LOCAL_LOCK = OUT / "P8_Y5_BRR545_LOCAL_LOCK_MAP.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3892_SOURCE_REGISTER.csv",
    "boundary_certificate": OUT / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv",
    "projector_certificate": OUT / "P8_Y5_R2FR_3892_PROJECTOR_ABSOLUTE_TOPOLOGICAL_CERTIFICATE.csv",
    "fill": OUT / "P8_Y5_R2FR_3892_ALPHA3_PROJECTOR_NUMERIC_FILL_ROWS.csv",
    "gate": OUT / "P8_Y5_R2FR_3892_LOCAL_GR_DECISION_GATE.csv",
    "runner": OUT / "P8_Y5_R2FR_3892_RUNNER_UPDATE.csv",
    "next": OUT / "P8_Y5_R2FR_3892_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3892_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3892_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3892_00_next", CSV_3891_NEXT, "NEXT3891_0", "3891 selected boundary/projector certificate target"),
    ("SRC3892_01_bp", CSV_3891_BP, "BPS3891_0_boundary_guard", "boundary/projector guard"),
    ("SRC3892_02_fill", CSV_3891_FILL, "NF3891_1_boundary_alpha3", "numeric fill rows"),
    ("SRC3892_03_gate", CSV_3891_GATE, "LGG3891_7_local_GR", "3891 local-GR gate"),
    ("SRC3892_04_validation", CSV_3891_VALIDATION, "VAL3891_14_next_target", "3891 validation"),
    ("SRC3892_05_boundary_alpha3", CSV_BOUNDARY_ALPHA3, "T7_conclusion", "boundary alpha3 theorem attempt"),
    ("SRC3892_06_boundary_decision", CSV_BOUNDARY_DECISION, "D2_numeric_fallback", "boundary decision"),
    ("SRC3892_07_BCOH", CSV_BCOH, "BCT549_6_certificate_verdict", "boundary cohomology nohair verdict"),
    ("SRC3892_08_BFLUX", CSV_BFLUX, "FB549_0_boundary_flux_bound", "boundary flux fill row"),
    ("SRC3892_09_PIM_contract", CSV_PIM_CONTRACT, "PV6_modified_exterior_residual_map", "projector variation contract"),
    ("SRC3892_10_PIM_silence", CSV_PIM_SILENCE, "PST550_7_certificate_verdict", "projector silence verdict"),
    ("SRC3892_11_R11_fill", CSV_R11_FILL, "F6_projector_stress", "projector stress fill row"),
    ("SRC3892_12_local_lock", CSV_LOCAL_LOCK, "BRL547_0_boundary_alpha3", "local lock alpha3 row"),
]

BOUNDARY_CERT = "S_B = S_top[relative class] + int_boundary sqrt(|gamma|) F(s), with D_A s=0, no marker/vector/shear fields, fixed corner/reference class, and no normal exchange"
BOUNDARY_ZERO = "Under BOUNDARY_CERT, tau_AB proportional gamma_AB and n_mu P_loc_nu T_B^{mu nu}=0, so alpha3_boundary=0; derivative-silent scalar monopole may renormalize GM but must not carry beta/xi/Gdot hair"
PROJECTOR_CERT = "Pi_M J = ell_M(J) omega_M_top, with d omega_M_top=0, delta_g Pi_M=0, [d,Pi_M]J=0, fixed homology/domain, and Pi_M J_H equal to the same dressed Hilbert source charge before readout"
PROJECTOR_ZERO = "Under PROJECTOR_CERT, delta(Pi_M J_H) has no projector stress term and d(Pi_M J_H)=Pi_M dJ_H, so T_extra_munu^Pi=0 and projector PPN residuals vanish"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        cells = [str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_boundary_projector_certificate_or_fill",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def boundary_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("BC3892_0_certificate", "boundary certificate package", BOUNDARY_CERT, "EXACT_SUFFICIENT_CERTIFICATE", "not currently parent-owned as a global MTS theorem"),
        ("BC3892_1_alpha3_zero", "alpha3 boundary zero", BOUNDARY_ZERO, "CONDITIONAL_ZERO_IF_CERTIFICATE_SIGNED", "certificate clauses unsigned, so no claim"),
        ("BC3892_2_scalar_monopole", "scalar monopole handling", "constant derivative-silent scalar boundary monopole can shift measured GM only; partial_t=partial_r=partial_frame=0 required", "CONDITIONAL_CALIBRATION_ONLY", "beta/xi/Gdot remain live if derivative silence not signed"),
        ("BC3892_3_forbidden_shortcut", "rejected shortcut", "X_D=0 or scalar volume no-flux does not imply n_mu P_loc_nu K_boundary^{mu nu}=0", "REJECT_SHORTCUT", "prevents false alpha3 pass"),
        ("BC3892_4_verdict", "boundary status", "boundary certificate is ready as a parent-action clause, but current branch lacks parent ownership of scalar-only marker-free boundary class and fixed relative cohomology", "CERTIFICATE_READY_PARENT_UNSIGNED", "numeric fill rows remain active"),
    ]
    return [
        {
            "boundary_id": row_id,
            "piece": piece,
            "statement_or_math": statement,
            "status": status,
            "remaining_failure": failure,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, failure in raw_rows
    ]


def projector_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("PC3892_0_certificate", "projector certificate package", PROJECTOR_CERT, "EXACT_SUFFICIENT_CERTIFICATE", "source-charge equality and domain/homology owner unsigned"),
        ("PC3892_1_projector_zero", "projector stress zero", PROJECTOR_ZERO, "CONDITIONAL_ZERO_IF_CERTIFICATE_SIGNED", "certificate not parent-owned"),
        ("PC3892_2_product_rule", "product rule retained", "delta(Pi_M J_H)=Pi_M delta J_H+(delta Pi_M)J_H; d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H", "EXACT_GUARD", "both extra terms remain unless certificate signs them zero"),
        ("PC3892_3_wrong_projector", "wrong-current guard", "a closed topological current is not enough unless Pi_M J_H equals the same dressed Hilbert/worldtube source charge", "REJECT_WRONG_CONSERVED_OBJECT", "avoids conserving the wrong mass"),
        ("PC3892_4_verdict", "projector status", "absolute/topological projector route is mathematically clean but not signed for the current MTS branch", "CERTIFICATE_READY_PARENT_UNSIGNED", "projector PPN fill rows remain active"),
    ]
    return [
        {
            "projector_id": row_id,
            "piece": piece,
            "statement_or_math": statement,
            "status": status,
            "remaining_failure": failure,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, failure in raw_rows
    ]


def fill_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("AF3892_0_alpha3_boundary", "alpha3_boundary", "dimensionless", "alpha3_boundary = c_B_flux_to_alpha3 * epsilon_B_flux_abs", "abs(alpha3_boundary) <= 4e-20", "MISSING_c_B_flux_to_alpha3_OR_THEOREM_ZERO;MISSING_epsilon_B_flux_abs_OR_THEOREM_ZERO"),
        ("AF3892_1_xi_boundary", "xi_boundary", "dimensionless", "xi_boundary = c_B_flux_to_xi * epsilon_B_flux_abs + c_B_STF * epsilon_B_STF", "abs(xi_boundary) <= 4e-09", "MISSING_c_B_flux_to_xi;MISSING_epsilon_B_STF"),
        ("AF3892_2_beta_boundary", "delta_beta_boundary", "dimensionless", "delta_beta_boundary = c_B_flux_to_beta * epsilon_B_flux_abs + c_B_mono2 * epsilon_B_mono2", "abs(delta_beta_boundary) <= 7.8e-05", "MISSING_beta_boundary_coefficients"),
        ("AF3892_3_Gdot_boundary", "Gdot_boundary", "yr^-1", "Gdot_boundary = partial_t ln(1+epsilon_B_flux_abs) + partial_t epsilon_B_mono", "abs(Gdot_boundary) <= 9.6e-15 yr^-1", "MISSING_boundary_time_profile"),
        ("AF3892_4_projector_gamma_beta", "Delta_projector_gamma_beta", "dimensionless_pair", "{delta_gamma_Pi,delta_beta_Pi}=P_{gamma,beta}[T_extra_munu^Pi]", "abs(delta_gamma_Pi)<=2.3e-05 and abs(delta_beta_Pi)<=7.8e-05", "MISSING_projector_weak_field_map"),
        ("AF3892_5_projector_preferred", "Delta_projector_alpha_xi_zeta", "dimensionless_vector", "{alpha1,alpha2,alpha3,xi,zeta_i}_Pi=P_pref[T_extra_munu^Pi]", "each component below its PPN bound with no cancellation credit", "MISSING_projector_preferred_frame_map"),
        ("AF3892_6_projector_R10", "alpha_projector(lambda)", "range_dependent", "alpha_projector(lambda)=K_Pi(lambda) Q_Pi^H q_Pi^test/G_N", "abs(alpha_projector(lambda)) <= alpha_bound(lambda)", "MISSING_projector_range_profile_and_bound_curve"),
    ]
    return [
        {
            "fill_id": row_id,
            "symbol": symbol,
            "units": units,
            "prediction_formula": formula,
            "pass_rule": rule,
            "current_input_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, units, formula, rule, status in raw_rows
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("LGG3892_0_boundary_certificate", "boundary topological/no-flux certificate", BOUNDARY_CERT, "FAIL_PARENT_UNSIGNED"),
        ("LGG3892_1_boundary_alpha3", "boundary alpha3 zero", BOUNDARY_ZERO, "PASS_IF_CERTIFICATE_SIGNED_ONLY"),
        ("LGG3892_2_projector_certificate", "absolute/topological projector certificate", PROJECTOR_CERT, "FAIL_PARENT_UNSIGNED"),
        ("LGG3892_3_projector_stress", "projector stress zero", PROJECTOR_ZERO, "PASS_IF_CERTIFICATE_SIGNED_ONLY"),
        ("LGG3892_4_fill_rows", "alpha3/projector numeric fill", "boundary and projector prediction formulas emitted", "PASS_FILL_READY_NONCLAIM"),
        ("LGG3892_5_local_GR", "local-GR promotion", "boundary and projector certificates signed or fill rows pass, plus memory/R11/residual-lock close", "BLOCKED_NO_CLAIM"),
    ]
    return [
        {
            "gate_id": row_id,
            "gate": gate,
            "requirement": req,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, req, status in raw_rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("RUNU3892_0_boundary", "boundary_certificate", "only set boundary alpha3/xi/beta/Gdot rows to zero if the full scalar/topological marker-free certificate is signed", "NO_PARTIAL_BOUNDARY_ZERO"),
        ("RUNU3892_1_projector", "projector_certificate", "only drop projector stress if Pi_M is absolute/topological and equals the same Hilbert source charge before readout", "NO_WRONG_CURRENT_ZERO"),
        ("RUNU3892_2_fill", "numeric_fill", "if either certificate is unsigned, run emitted fill formulas with sourced coefficients and no cancellation credit", "FILL_FORMULAS_READY"),
        ("RUNU3892_3_claim", "local_GR_claim", "false until boundary/projector/memory/R11/residual-lock all close", "NO_LOCAL_GR_CLAIM"),
        ("RUNU3892_4_next", "next_attack", "move to memory/R11 factorization or start sourcing boundary/projector numeric coefficients", "NEXT_3893"),
    ]
    return [
        {
            "update_id": row_id,
            "runner_field": field,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, rule, status in raw_rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3892_0",
            "target_checkpoint": "3893-Y5-R2FR-memory-R11-factorization-or-boundary-projector-numeric-source-fill.md",
            "script": "scripts/Y5_R2FR_3893_memory_R11_factorization_or_boundary_projector_numeric_source_fill.py",
            "objective": "attack compact-local memory silence and universal R11 Sigma_loc factorization; if either remains unsigned, begin sourcing the boundary/projector numeric coefficients emitted by 3892",
            "why_next": "3892 reduces boundary/projector to exact certificates plus explicit fill formulas, leaving memory and R11 factorization as the other dominant local-GR blockers",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3892_0",
            "branch": BRANCH,
            "summary": "boundary and projector exact certificates written; both remain parent-unsigned, so alpha3/xi/beta/Gdot and projector PPN/R10 fill formulas are active nonclaim rows",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    boundary: list[dict[str, object]],
    projector: list[dict[str, object]],
    fill: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3892 - Boundary/Projector Topological Certificate or Fill Alpha3/Projector Inputs

Generated: `{timestamp}`

## Result

3892 writes the exact certificates needed to zero the two dominant local blockers.

Boundary certificate:

`{BOUNDARY_CERT}`

Boundary zero:

`{BOUNDARY_ZERO}`

Projector certificate:

`{PROJECTOR_CERT}`

Projector zero:

`{PROJECTOR_ZERO}`

These are mathematically clean sufficient routes. They are not yet parent-owned in the current branch, so the correct outcome is not a local-GR claim: it is an executable fill interface for boundary alpha3/xi/beta/Gdot and projector PPN/R10 components.

## Boundary Certificate

{markdown_table(boundary, ["boundary_id", "piece", "statement_or_math", "status", "remaining_failure"])}

## Projector Certificate

{markdown_table(projector, ["projector_id", "piece", "statement_or_math", "status", "remaining_failure"])}

## Alpha3/Projector Numeric Fill Rows

{markdown_table(fill, ["fill_id", "symbol", "units", "prediction_formula", "pass_rule", "current_input_status"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "requirement", "status", "claim_allowed"])}

## Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

The local branch is now sharper: boundary/projector can be killed exactly only by strong topological certificates, not by scalar no-flux vibes. Since those certificates are unsigned, the honest path is to either parent-sign them or fill the numeric formulas emitted here.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3892 BOUNDARY PROJECTOR CERTIFICATES -->"
    end = "<!-- END 3892 BOUNDARY PROJECTOR CERTIFICATES -->"
    block = f"""{start}

## 3892 - Boundary/projector topological certificates

Boundary certificate:

`{BOUNDARY_CERT}`

Projector certificate:

`{PROJECTOR_CERT}`

Status: exact sufficient certificates written. Both remain parent-unsigned in the current candidate branch. Active fill formulas now cover boundary alpha3/xi/beta/Gdot and projector gamma/beta/preferred-frame/R10 components.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3892_PROJECTOR_ABSOLUTE_TOPOLOGICAL_CERTIFICATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3892_ALPHA3_PROJECTOR_NUMERIC_FILL_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3892_VALIDATION.csv`

Next gate: `3893`, memory/R11 factorization or numeric source fill.

<!-- Generated by 3892 at {timestamp} -->
{end}
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if start in existing and end in existing:
        before = existing.split(start)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        new_text = f"{before}\n\n{block}\n\n{after}".rstrip() + "\n"
    else:
        new_text = existing.rstrip() + "\n\n" + block + "\n"
    SPINE_PATH.write_text(new_text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    boundary: list[dict[str, object]],
    projector: list[dict[str, object]],
    fill: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    checks.append(("VAL3892_0_sources", "all cited source paths exist and needles are found", resolved == len(sources), f"{resolved}/{len(sources)} sources resolved"))
    checks.append(("VAL3892_1_boundary_certificate", "boundary certificate is explicit", any("S_B = S_top" in str(row["statement_or_math"]) for row in boundary), "BC3892_0"))
    checks.append(("VAL3892_2_boundary_shortcut", "scalar no-flux shortcut remains rejected", any("X_D=0" in str(row["statement_or_math"]) for row in boundary), "BC3892_3"))
    checks.append(("VAL3892_3_projector_certificate", "projector certificate is explicit", any("Pi_M J = ell_M" in str(row["statement_or_math"]) for row in projector), "PC3892_0"))
    checks.append(("VAL3892_4_projector_wrong_current", "wrong conserved current guard exists", any("wrong-current" in str(row["piece"]) or "wrong mass" in str(row["remaining_failure"]) for row in projector), "PC3892_3"))
    required_symbols = {"alpha3_boundary", "xi_boundary", "delta_beta_boundary", "Gdot_boundary", "Delta_projector_gamma_beta", "Delta_projector_alpha_xi_zeta", "alpha_projector(lambda)"}
    found_symbols = {str(row["symbol"]) for row in fill}
    checks.append(("VAL3892_5_fill_coverage", "fill formulas cover boundary and projector observables", required_symbols.issubset(found_symbols), f"{len(found_symbols)} fill rows"))
    checks.append(("VAL3892_6_local_gr_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3892_5_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3892_5"))
    checks.append(("VAL3892_7_all_nonclaim", "all generated analytic rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [boundary, projector, fill, gate, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3892_8_runner", "runner requires full certificate before zeroing", any(row["runner_field"] == "boundary_certificate" and "full" in str(row["rule"]) for row in runner), "RUNU3892_0"))
    checks.append(("VAL3892_9_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "not by scalar no-flux vibes" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3892_10_spine", "spine updated with 3892 block", SPINE_PATH.exists() and "BEGIN 3892 BOUNDARY PROJECTOR CERTIFICATES" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3892_11_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [path for path in FWB.rglob("*3892*") if path.is_file() and ("3892-Y5" in path.name or "P8_Y5_R2FR_3892" in path.name or "P8_Y5_BRR545_3892" in path.name)]
    checks.append(("VAL3892_12_formalization_untouched", "no generated 3892 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3892_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3892_14_next_target", "next target attacks memory/R11 or numeric fill", any("memory-R11-factorization" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3893 memory/R11"))
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
    boundary = boundary_rows(timestamp)
    projector = projector_rows(timestamp)
    fill = fill_rows(timestamp)
    gate = gate_rows(timestamp)
    runner = runner_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["boundary_certificate"], boundary)
    write_csv(OUTPUTS["projector_certificate"], projector)
    write_csv(OUTPUTS["fill"], fill)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, boundary, projector, fill, gate, runner, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, boundary, projector, fill, gate, runner, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_BOUNDARY_PROJECTOR_CERTIFICATES_OR_FILL_ROWS")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

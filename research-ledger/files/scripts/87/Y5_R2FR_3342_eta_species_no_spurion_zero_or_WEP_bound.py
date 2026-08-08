from __future__ import annotations

import csv
import hashlib
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3342-Y5-R2FR-eta-species-no-spurion-zero-or-WEP-bound-under-AX1090.md"

SOURCES = [
    {
        "source_id": "SRC3342_0_3341_doc",
        "path": ROOT / "3341-Y5-R2FR-source-coupling-residual-vector-runner-under-AX1090.md",
        "role": "3341 strict residual-vector runner handoff",
    },
    {
        "source_id": "SRC3342_1_3341_contract",
        "path": OUT / "P8_Y5_R2FR_3341_COMPONENT_RUNNER_CONTRACT.csv",
        "role": "runner contract for FRV3340_1_eta_species",
    },
    {
        "source_id": "SRC3342_2_3341_requirements",
        "path": OUT / "P8_Y5_R2FR_3341_NEXT_SOURCE_REQUIREMENTS.csv",
        "role": "next source requirement selecting eta_species first",
    },
    {
        "source_id": "SRC3342_3_3340_residual_schema",
        "path": OUT / "P8_Y5_R2FR_3340_FINITE_RESIDUAL_VECTOR_SCHEMA.csv",
        "role": "finite residual vector schema",
    },
    {
        "source_id": "SRC3342_4_3340_parent_evidence",
        "path": OUT / "P8_Y5_R2FR_3340_PARENT_CLAUSE_EVIDENCE_SCORE.csv",
        "role": "current parent signature status",
    },
    {
        "source_id": "SRC3342_5_3292_spurion_split",
        "path": OUT / "P8_Y5_R2FR_3292_HILBERT_SOURCE_VS_SPURION_SPLIT.csv",
        "role": "source-only spurion split and hidden spurion countermodel",
    },
    {
        "source_id": "SRC3342_6_3293_hilbert_signature",
        "path": OUT / "P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv",
        "role": "conditional Hilbert-source no-spurion theorem",
    },
    {
        "source_id": "SRC3342_7_3339_measured_g",
        "path": OUT / "P8_Y5_R2FR_3339_MEASURED_G_ABSORPTION_THEOREM.csv",
        "role": "measured-G common-mode absorption and relative-weight survival",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3342_SOURCE_REGISTER.csv",
    "web_sources": OUT / "P8_Y5_R2FR_3342_WEB_SOURCE_REGISTER.csv",
    "no_spurion_theorem": OUT / "P8_Y5_R2FR_3342_NO_SPURION_THEOREM_AUDIT.csv",
    "current_verdict": OUT / "P8_Y5_R2FR_3342_CURRENT_CORPUS_VERDICT.csv",
    "measured_g": OUT / "P8_Y5_R2FR_3342_MEASURED_G_COMMON_MODE_AUDIT.csv",
    "wep_map": OUT / "P8_Y5_R2FR_3342_WEP_OBSERVABLE_MAP.csv",
    "material_response": OUT / "P8_Y5_R2FR_3342_MATERIAL_RESPONSE_PLACEHOLDERS.csv",
    "wep_bounds": OUT / "P8_Y5_R2FR_3342_WEP_BOUND_ROWS.csv",
    "component_row": OUT / "P8_Y5_R2FR_3342_FRV3340_ETA_SPECIES_COMPONENT_ROW.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3342_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3342_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3342_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3342_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()

MICROSCOPE_ETA_CENTRAL = -1.5e-15
MICROSCOPE_ETA_STAT = 2.3e-15
MICROSCOPE_ETA_SYST = 1.5e-15
MICROSCOPE_SIGMA_QUAD = math.sqrt(MICROSCOPE_ETA_STAT**2 + MICROSCOPE_ETA_SYST**2)
MICROSCOPE_ABS_CENTRAL_PLUS_SIGMA = abs(MICROSCOPE_ETA_CENTRAL) + MICROSCOPE_SIGMA_QUAD


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def parse_float(value: str) -> float | None:
    try:
        if value == "" or value.startswith("MISSING"):
            return None
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def local_source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def web_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "web_source_id": "WEB3342_0_MICROSCOPE_PRL_DOI",
            "title": "MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle",
            "authors": "Touboul et al.",
            "year": "2022",
            "doi": "10.1103/PhysRevLett.129.121102",
            "url": "https://link.aps.org/doi/10.1103/PhysRevLett.129.121102",
            "arxiv": "https://arxiv.org/abs/2209.15487",
            "extraction_method": "paper-stated Ti/Pt Eotvos result transcribed into nonclaim bound rows",
            "quoted_result_used": "eta(Ti,Pt)=(-1.5 +/- 2.3(stat) +/- 1.5(syst))e-15",
            "confidence": "source-backed_primary_result",
            "valid_for_claim": "false",
        }
    ]


def parent_signature_closed() -> bool:
    evidence_path = OUT / "P8_Y5_R2FR_3340_PARENT_CLAUSE_EVIDENCE_SCORE.csv"
    if not evidence_path.exists():
        return False
    rows = read_csv(evidence_path)
    return bool(rows) and all(row.get("passes_parent_signature") == "true" for row in rows)


def no_spurion_theorem_rows() -> list[dict[str, Any]]:
    parent_closed = parent_signature_closed()
    return [
        {
            "audit_id": "NS3342_0_target",
            "clause": "eta_species=0 target",
            "statement": "eta_species is the relative source-only gravitational weight after common measured-G calibration.",
            "derivation_step": "To set eta_species=0, the parent object language must have no w_A/kappa_A that affects source strength without also appearing in matter dynamics and readout.",
            "source_path": str(OUT / "P8_Y5_R2FR_3340_FINITE_RESIDUAL_VECTOR_SCHEMA.csv"),
            "status": "TARGET_DEFINED",
            "theorem_zero_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "NS3342_1_conditional_zero",
            "clause": "Hilbert-source no-spurion theorem",
            "statement": "If all local sources are Hilbert/Noether variations of one descended matter functional S_m[g_obs(q(Phi)),Psi,theta], then post-variation source-only selectors T_source=sum_A kappa_A T_A are not variables of the theory.",
            "derivation_step": "A selector introduced after variation is not a variation of S_m; if kappa_A is physical it must enter S_m/readout and is no longer source-only.",
            "source_path": str(OUT / "P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv"),
            "status": "EXACT_CONDITIONAL_THEOREM",
            "theorem_zero_allowed": bool_str(parent_closed),
            "valid_for_claim": "false",
        },
        {
            "audit_id": "NS3342_2_hidden_countermodel",
            "clause": "hidden spurion return",
            "statement": "If a hidden invariant I_hid controls w_A(I_hid) or kappa_A(I_hid), then eta_A-eta_B survives as a relative WEP/source-composition residual.",
            "derivation_step": "A single measured G_N can absorb only the common mode; independent species weights remain observable in differential accelerations.",
            "source_path": str(OUT / "P8_Y5_R2FR_3292_HILBERT_SOURCE_VS_SPURION_SPLIT.csv"),
            "status": "LIVE_COUNTERMODEL_UNTIL_PARENT_SYNTAX_SIGNED",
            "theorem_zero_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "NS3342_3_current_verdict",
            "clause": "current MTS ownership",
            "statement": "The no-spurion theorem is real, but the current corpus has not signed the parent Hilbert-source syntax required to apply it as an MTS-owned zero.",
            "derivation_step": "3340 evidence rows mark HSC3340_3_no_spurion_weights as countermodel-filter-defined, not eliminated by parent syntax.",
            "source_path": str(OUT / "P8_Y5_R2FR_3340_PARENT_CLAUSE_EVIDENCE_SCORE.csv"),
            "status": "THEOREM_ZERO_NOT_PROMOTED",
            "theorem_zero_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def current_verdict_rows() -> list[dict[str, Any]]:
    parent_closed = parent_signature_closed()
    return [
        {
            "verdict_id": "VER3342_0_zero_proof",
            "question": "Did 3342 prove eta_species=0 from current parent syntax?",
            "answer": "no" if not parent_closed else "yes",
            "reason": "Parent Hilbert-source/no-spurion syntax is conditional and not corpus-signed." if not parent_closed else "All HSC3340 evidence rows pass parent signature.",
            "consequence": "Use WEP/source-composition finite bound fallback for FRV3340_1.",
            "valid_for_claim": "false",
        },
        {
            "verdict_id": "VER3342_1_progress",
            "question": "Did 3342 move beyond just saying missing?",
            "answer": "yes",
            "reason": "It turns eta_species into a concrete theorem-zero condition plus a source-backed MICROSCOPE Ti/Pt residual row.",
            "consequence": "The source vector now has a real first empirical channel input, while local-GR remains blocked until all channels close.",
            "valid_for_claim": "false",
        },
    ]


def measured_g_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "G3342_0_common_mode",
            "claim": "Measured G_N absorbs only one universal common source scale.",
            "formula": "J^{mu nu}=kappa_* sum_A T_A^{mu nu} -> measured G_N rho in the Newtonian slot",
            "eta_species_effect": "none if all eta_A are equal",
            "source_path": str(OUT / "P8_Y5_R2FR_3339_MEASURED_G_ABSORPTION_THEOREM.csv"),
            "status": "COMMON_MODE_CALIBRATION_ONLY",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "G3342_1_relative_mode",
            "claim": "Species-relative weights cannot be hidden in one measured G_N.",
            "formula": "J^{mu nu}=kappa_* sum_A (1+eta_A)T_A^{mu nu}; eta_A-eta_B survives WEP projection",
            "eta_species_effect": "bounded by WEP/source-composition tests or zeroed by no-spurion theorem",
            "source_path": str(OUT / "P8_Y5_R2FR_3339_MEASURED_G_ABSORPTION_THEOREM.csv"),
            "status": "RELATIVE_WEIGHT_REMAINS_PHYSICAL",
            "valid_for_claim": "false",
        },
    ]


def wep_observable_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "map_id": "WEP3342_0_eotvos_definition",
            "observable": "eta_AB",
            "formula": "eta_AB = 2(a_A-a_B)/(a_A+a_B)",
            "maps_to": "differential source/test response after common G_N calibration",
            "assumptions": "weak-field local comparison branch; common environmental acceleration cancels in the differential ratio",
            "valid_for_claim": "false",
        },
        {
            "map_id": "WEP3342_1_eta_species_channel",
            "observable": "eta_species(A,B)",
            "formula": "|eta_species(A,B)| <= |eta_AB|/|R_AB|",
            "maps_to": "FRV3340_1_eta_species component under a material response factor R_AB",
            "assumptions": "no cancellation; R_AB derived from material charge/composition response or set to private unit response for smoke only",
            "valid_for_claim": "false",
        },
        {
            "map_id": "WEP3342_2_no_cancellation",
            "observable": "absolute source residual",
            "formula": "component_contribution = abs(component_value * response_factor)",
            "maps_to": "3341 runner contract",
            "assumptions": "ABS_SUM_NO_CANCELLATION; do not let opposite species channels cancel unless a parent theorem proves cancellation",
            "valid_for_claim": "false",
        },
    ]


def material_response_rows() -> list[dict[str, Any]]:
    return [
        {
            "material_row_id": "MAT3342_0_MICROSCOPE_TiPt",
            "material_pair": "Titanium alloy / Platinum alloy",
            "arena": "MICROSCOPE WEP satellite differential acceleration",
            "response_factor_R_AB": "1.0",
            "response_factor_status": "PRIVATE_UNIT_RESPONSE_FOR_COMPONENT_SMOKE_ONLY",
            "missing_for_full_claim": "derive nuclear/EM/binding-energy/composition charges for Ti and Pt; map them to the MTS source-only eta_species basis",
            "source_path": str(OUTPUTS["web_sources"]),
            "valid_for_component_bound": "true",
            "valid_for_claim": "false",
        }
    ]


def wep_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "BND3342_0_MICROSCOPE_TiPt_sigma_quad",
            "observable": "eta_TiPt",
            "central_value": f"{MICROSCOPE_ETA_CENTRAL:.6e}",
            "stat_uncertainty": f"{MICROSCOPE_ETA_STAT:.6e}",
            "syst_uncertainty": f"{MICROSCOPE_ETA_SYST:.6e}",
            "bound_value": f"{MICROSCOPE_SIGMA_QUAD:.6e}",
            "bound_type": "quadrature_1sigma_uncertainty",
            "units": "dimensionless_Eotvos_ratio",
            "source_url": "https://link.aps.org/doi/10.1103/PhysRevLett.129.121102",
            "source_path": str(OUTPUTS["web_sources"]),
            "extraction_method": "paper-stated final Ti/Pt result",
            "valid_for_component_bound": "true",
            "valid_for_full_eta_species": "false",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BND3342_1_MICROSCOPE_TiPt_abs_central_plus_sigma",
            "observable": "eta_TiPt",
            "central_value": f"{MICROSCOPE_ETA_CENTRAL:.6e}",
            "stat_uncertainty": f"{MICROSCOPE_ETA_STAT:.6e}",
            "syst_uncertainty": f"{MICROSCOPE_ETA_SYST:.6e}",
            "bound_value": f"{MICROSCOPE_ABS_CENTRAL_PLUS_SIGMA:.6e}",
            "bound_type": "abs_central_plus_quadrature_1sigma_channel_envelope",
            "units": "dimensionless_Eotvos_ratio",
            "source_url": "https://link.aps.org/doi/10.1103/PhysRevLett.129.121102",
            "source_path": str(OUTPUTS["web_sources"]),
            "extraction_method": "conservative channel envelope from stated central/stat/syst values",
            "valid_for_component_bound": "true",
            "valid_for_full_eta_species": "false",
            "valid_for_claim": "false",
        },
    ]


def component_row() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "CAND3342_FRV3340_1_eta_species_MICROSCOPE_TiPt_nonclaim",
            "component_id": "FRV3340_1_eta_species",
            "symbol": "eta_species",
            "mode": "WEP_TiPt_channel_bound_nonclaim",
            "theorem_zero": "false",
            "zero_authority": "NOT_PARENT_SIGNED_HSC3340",
            "component_value": f"{MICROSCOPE_ABS_CENTRAL_PLUS_SIGMA:.6e}",
            "response_factor": "1.000000e+00",
            "component_contribution": f"{MICROSCOPE_ABS_CENTRAL_PLUS_SIGMA:.6e}",
            "component_units": "dimensionless_Eotvos_ratio",
            "source_path": str(OUTPUTS["wep_bounds"]),
            "source_url": "https://link.aps.org/doi/10.1103/PhysRevLett.129.121102",
            "equation_ref": "MICROSCOPE_FINAL_eta_TiPt_abs_central_plus_sigma_quad",
            "arena": "WEP_TiPt_MICROSCOPE",
            "no_cancellation_guard": "ABS_SUM_NO_CANCELLATION",
            "runner_contract_path": str(OUT / "P8_Y5_R2FR_3341_COMPONENT_RUNNER_CONTRACT.csv"),
            "valid_for_component_bound": "true",
            "valid_for_claim": "false",
            "claim_blocker": "Ti/Pt is one WEP channel and material response factor is not derived into full MTS eta_species basis; parent no-spurion theorem is not signed.",
        }
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    parent_closed = parent_signature_closed()
    return [
        {
            "gate_id": "GATE3342_0_no_spurion_theorem_shape",
            "claim": "eta_species theorem-zero condition has an exact conditional theorem",
            "passed": "true",
            "reason": "3293 excludes source-only selectors under a signed Hilbert-source parent action.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3342_1_parent_signed_zero",
            "claim": "eta_species=0 is parent-signed for MTS",
            "passed": bool_str(parent_closed),
            "reason": "Current 3340 parent evidence rows still do not sign HSC3340_3_no_spurion_weights." if not parent_closed else "All parent evidence rows pass.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3342_2_wep_source_anchor",
            "claim": "real WEP source anchor is recorded",
            "passed": "true",
            "reason": "MICROSCOPE final Ti/Pt Eotvos result is recorded with DOI, URL, year, values, and extraction method.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3342_3_component_bound_staged",
            "claim": "FRV3340_1 has a finite Ti/Pt component row",
            "passed": "true",
            "reason": "A source-backed nonclaim component value is staged with units, source path, equation ref, arena, and no-cancellation guard.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3342_4_full_eta_species_claim",
            "claim": "full eta_species component is claim-ready",
            "passed": "false",
            "reason": "A single Ti/Pt channel plus unit response smoke factor is not a complete max_{A,B}|eta_A-eta_B| bound in the MTS basis.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3342_5_local_GR_claim",
            "claim": "local-GR source-coupling branch is claim-ready",
            "passed": "false",
            "reason": "Other FRV3340 channels remain open and the parent no-spurion theorem is not signed.",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3342_0",
            "question": "Did derivation-first close eta_species?",
            "answer": "not yet",
            "reason": "The theorem-zero route is exact but conditional; the parent syntax has not eliminated hidden/source-only spurions.",
            "next_action": "Keep no-spurion as a parent-action target, but use source-backed WEP rows for finite residual scoring.",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3342_1",
            "question": "What concrete progress was made?",
            "answer": "first source-backed empirical coupling row staged",
            "reason": "MICROSCOPE Ti/Pt supplies a real dimensionless WEP bound for eta_species channel discipline.",
            "next_action": "Either derive Ti/Pt material response into the MTS source basis or move to epsilon_EM public-Hodge/Poynting residual.",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3343-Y5-R2FR-epsilon-EM-public-Hodge-Poynting-zero-or-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3343_epsilon_EM_public_Hodge_Poynting_zero_or_bound.py",
            "objective": "attack FRV3340_4_epsilon_EM by deriving public Maxwell/Hodge/Poynting stress ownership; if it fails, stage finite alpha/Hodge/current/Poynting residual bounds without claiming local-GR",
            "why_next": "3341 listed epsilon_EM second; user explicitly flagged Poynting/waves as likely relevant to the background field; EM stress is a high-leverage local-GR/Maxwell bridge.",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3343b-Y5-R2FR-eta-species-material-response-factor-map.md",
            "target_script": "scripts/Y5_R2FR_3343b_eta_species_material_response_factor_map.py",
            "objective": "derive or source R_AB material response factors for Ti/Pt and other WEP channels so WEP bounds become MTS-basis eta_species bounds",
            "why_next": "needed before the MICROSCOPE Ti/Pt row can be promoted from channel discipline to full eta_species evidence",
            "valid_for_claim": "false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]], limit: int = 20) -> str:
    if not rows:
        return "_No rows._"
    fieldnames: list[str] = []
    for row in rows[:limit]:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows[:limit]:
        values = [compact(row.get(key, ""), 260).replace("|", "\\|") for key in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    if len(rows) > limit:
        lines.append(f"\n_Truncated in markdown: showing {limit} of {len(rows)} rows._")
    return "\n".join(lines)


def render_doc() -> str:
    return "\n\n".join(
        [
            "# 3342 — eta_species No-Spurion Zero Or WEP Bound Under AX1090",
            f"Generated: `{RUN_UTC}`",
            "## Summary\n"
            "- Derivation-first result: `eta_species=0` is an exact conditional theorem if the parent action has one signed Hilbert-source matter functional and no source-only spurions.\n"
            "- Current-corpus result: the theorem is **not promoted** because HSC3340_3 remains countermodel-filter-defined, not parent-signed.\n"
            "- Concrete progress: a real MICROSCOPE Ti/Pt WEP channel bound is staged as a nonclaim FRV3340_1 component row with units, source URL, equation reference, arena, and absolute-sum guard.\n"
            "- No local-GR, PPN, Maxwell, WEP universality, or full `eta_species` claim is made.",
            "## Exact Conditional No-Spurion Audit\n" + markdown_table(no_spurion_theorem_rows()),
            "## Current Corpus Verdict\n" + markdown_table(current_verdict_rows()),
            "## Measured-G Common Mode\n" + markdown_table(measured_g_rows()),
            "## WEP Observable Map\n" + markdown_table(wep_observable_map_rows()),
            "## Material Response Placeholder Guard\n" + markdown_table(material_response_rows()),
            "## MICROSCOPE WEP Bound Rows\n" + markdown_table(wep_bound_rows()),
            "## FRV3340 eta_species Component Row\n" + markdown_table(component_row()),
            "## Promotion Gates\n" + markdown_table(promotion_gate_rows()),
            "## Decision Ledger\n" + markdown_table(decision_rows()),
            "## Next Target\n" + markdown_table(next_target_rows()),
            "## Source Note\n"
            "The MICROSCOPE numbers are recorded as source-backed private checkpoint inputs, not public MTS claims. The staged value is `abs(-1.5e-15)+sqrt((2.3e-15)^2+(1.5e-15)^2)=4.245906e-15` for the Ti/Pt channel only.",
        ]
    ) + "\n"


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    local_sources = local_source_rows()
    web_sources = web_source_rows()
    theorem_rows = no_spurion_theorem_rows()
    bounds = wep_bound_rows()
    components = component_row()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_changed = changed_count(formalization_before, snapshot_tree(FW))
    component = components[0]
    component_value = parse_float(component["component_value"])
    response_factor = parse_float(component["response_factor"])
    expected_component = MICROSCOPE_ABS_CENTRAL_PLUS_SIGMA
    checks = [
        {
            "check_id": "VAL3342_0_local_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3342_1_local_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3342_2_outputs_parse",
            "check": "all 3342 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3342_3_web_source_provenance",
            "check": "web source rows include DOI, URL, year, extraction method, and no MISSING markers",
            "passed": all(
                row.get("doi")
                and row.get("url", "").startswith("https://")
                and row.get("year")
                and row.get("extraction_method")
                and "MISSING" not in ";".join(str(value) for value in row.values())
                for row in web_sources
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3342_4_theorem_conditional_not_promoted",
            "check": "no-spurion theorem is exact conditional but not promoted under current parent status",
            "passed": any(row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem_rows)
            and any(row["status"] == "THEOREM_ZERO_NOT_PROMOTED" for row in theorem_rows)
            and any(row["gate_id"] == "GATE3342_1_parent_signed_zero" and row["passed"] == "false" for row in gates),
            "detail": "",
        },
        {
            "check_id": "VAL3342_5_wep_bounds_numeric_positive",
            "check": "WEP bound rows have positive finite numeric bound values and recognized units",
            "passed": all(
                parse_float(row["bound_value"]) is not None
                and parse_float(row["bound_value"]) > 0
                and row["units"] == "dimensionless_Eotvos_ratio"
                for row in bounds
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3342_6_bound_formula_matches",
            "check": "MICROSCOPE abs-central-plus-quadrature-sigma value matches expected computation",
            "passed": component_value is not None and abs(component_value - expected_component) < 1e-22,
            "detail": f"component_value={component['component_value']}; expected={expected_component:.6e}",
        },
        {
            "check_id": "VAL3342_7_component_row_runner_shape",
            "check": "FRV3340_1 component row has units, equation ref, arena, existing source path, and absolute-sum guard",
            "passed": component["component_id"] == "FRV3340_1_eta_species"
            and component_value is not None
            and response_factor is not None
            and Path(component["source_path"]).exists()
            and component["component_units"] == "dimensionless_Eotvos_ratio"
            and component["equation_ref"] != ""
            and component["arena"] == "WEP_TiPt_MICROSCOPE"
            and component["no_cancellation_guard"] == "ABS_SUM_NO_CANCELLATION",
            "detail": "",
        },
        {
            "check_id": "VAL3342_8_no_claim",
            "check": "full eta_species and local-GR gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3342_4_full_eta_species_claim", "GATE3342_5_local_GR_claim"}
            )
            and component["valid_for_claim"] == "false",
            "detail": "",
        },
        {
            "check_id": "VAL3342_9_next_target",
            "check": "next target includes epsilon_EM public-Hodge/Poynting route and eta material-response route",
            "passed": any("Poynting" in row["objective"] for row in next_target_rows())
            and any("material response" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3342_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": formalization_changed == 0,
            "detail": f"formalization_changed_count={formalization_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3342_11_overall",
            "check": "3342 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], local_source_rows())
    write_csv(OUTPUTS["web_sources"], web_source_rows())
    write_csv(OUTPUTS["no_spurion_theorem"], no_spurion_theorem_rows())
    write_csv(OUTPUTS["current_verdict"], current_verdict_rows())
    write_csv(OUTPUTS["measured_g"], measured_g_rows())
    write_csv(OUTPUTS["wep_map"], wep_observable_map_rows())
    write_csv(OUTPUTS["material_response"], material_response_rows())
    write_csv(OUTPUTS["wep_bounds"], wep_bound_rows())
    write_csv(OUTPUTS["component_row"], component_row())
    write_csv(OUTPUTS["promotion_gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()

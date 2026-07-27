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
DOC = ROOT / "3351-Y5-R2FR-parent-decoupled-field-silence-or-bound-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

GEV_CM3_TO_KG_M3 = 1.78266192e-21
RHO_DM_NOMINAL_GEV_CM3 = 0.47
RHO_DM_HIGH_GEV_CM3 = 1.50
RHO_SOLID_REFERENCE_KG_M3 = 1000.0

LOCAL_SOURCES = [
    ("LSRC3351_0_3350_doc", ROOT / "3350-Y5-R2FR-local-ordinary-source-arena-inventory-under-AX1090.md", "3350 arena split handoff"),
    ("LSRC3351_1_3350_arena", OUT / "P8_Y5_R2FR_3350_LOCAL_ARENA_DEFINITION.csv", "3350 local arena definitions"),
    ("LSRC3351_2_3350_decoupled", OUT / "P8_Y5_R2FR_3350_DECOUPLED_BLOCK_AUDIT.csv", "3350 decoupled block audit"),
    ("LSRC3351_3_3350_residuals", OUT / "P8_Y5_R2FR_3350_EXPLICIT_RESIDUAL_ROWS.csv", "3350 explicit residual rows"),
    ("LSRC3351_4_3350_gates", OUT / "P8_Y5_R2FR_3350_RAB_ZERO_ROUTE_UPDATE.csv", "3350 RAB route update"),
    ("LSRC3351_5_3347_trichotomy", OUT / "P8_Y5_R2FR_3347_SHADOW_TRICHOTOMY_DECISION.csv", "3347 source-shadow trichotomy"),
    ("LSRC3351_6_3347_zero", OUT / "P8_Y5_R2FR_3347_ZERO_THEOREM_ATTEMPT.csv", "3347 zero theorem attempt"),
    ("LSRC3351_7_3346_normal_form", OUT / "P8_Y5_R2FR_3346_PARENT_ACTION_NORMAL_FORM.csv", "3346 candidate parent action normal form"),
]

WEB_SOURCES = [
    {
        "web_source_id": "WEB3351_0_PDG_dark_matter_2025",
        "title": "Particle Data Group Review: Dark Matter",
        "url": "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-dark-matter.pdf",
        "usage": "source anchor for local dark-matter density scale used only as a decoupled-background density fallback",
        "extracted_values": "nominal/private scale 0.47 GeV/cm^3; conservative high envelope 1.5 GeV/cm^3",
        "valid_for_claim": "false",
    },
    {
        "web_source_id": "WEB3351_1_PDG_2023_dark_matter_archive",
        "title": "Particle Data Group Review archive: Dark Matter",
        "url": "https://pdg.lbl.gov/2023/reviews/rpp2023-rev-dark-matter.pdf",
        "usage": "continuity anchor for local density conventions if 2025 endpoint changes",
        "extracted_values": "density-scale continuity only",
        "valid_for_claim": "false",
    },
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3351_LOCAL_SOURCE_REGISTER.csv",
    "web_sources": OUT / "P8_Y5_R2FR_3351_WEB_SOURCE_REGISTER.csv",
    "trichotomy": OUT / "P8_Y5_R2FR_3351_DECOUPLED_FIELD_TRICHOTOMY.csv",
    "silence": OUT / "P8_Y5_R2FR_3351_SILENCE_THEOREM_ATTEMPT.csv",
    "density": OUT / "P8_Y5_R2FR_3351_DENSITY_ANCHOR_ROWS.csv",
    "residuals": OUT / "P8_Y5_R2FR_3351_FINITE_RESIDUAL_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3351_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3351_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3351_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3351_VALIDATION.csv",
}


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


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        if path.suffix.lower() == ".csv":
            read_csv(path)
        else:
            path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


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


def local_source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, role in LOCAL_SOURCES:
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def web_source_rows() -> list[dict[str, Any]]:
    return WEB_SOURCES


def kg_m3(gev_cm3: float) -> float:
    return gev_cm3 * GEV_CM3_TO_KG_M3


def trichotomy_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "TRI3351_0_absent_parent_slot",
            "candidate": "no T_D argument in S_parent and no post-variation source projector",
            "classification": "theorem-zero route",
            "local_effect": "epsilon_decoupled_field=0",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "case_id": "TRI3351_1_variational_parent_block",
            "candidate": "T_D = (-2/sqrt(-g)) delta S_D / delta g",
            "classification": "real parent action content",
            "local_effect": "must be listed as geometry/matter/field sector and coupled consistently",
            "status": "ACTION_INVENTORY_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "case_id": "TRI3351_2_smooth_universal_background",
            "candidate": "smooth ambient T_D with universal metric coupling",
            "classification": "density/cosmological or common-background branch",
            "local_effect": "not a material R_AB slot; differential WEP effect cancels at leading common acceleration, but PPN/orbital/tidal density residual remains",
            "status": "DENSITY_ANCHOR_FALLBACK",
            "valid_for_claim": "false",
        },
        {
            "case_id": "TRI3351_3_clumped_or_local_decoupled_source",
            "candidate": "local clump/domain-wall/contact hidden source",
            "classification": "finite residual needing direct density/gradient/contact bound",
            "local_effect": "could enter WEP/PPN/orbital channels if gradients or local density are non-negligible",
            "status": "NO_NUMERIC_LOCAL_CLUMP_BOUND_YET",
            "valid_for_claim": "false",
        },
        {
            "case_id": "TRI3351_4_nonuniversal_projector",
            "candidate": "P_D(T_H,labels) or readout-created decoupled response",
            "classification": "source-shadow/readout residual, not decoupled matter density",
            "local_effect": "belongs to epsilon_readout_source_shadow or epsilon_source_shadow, not epsilon_decoupled_field",
            "status": "ROUTE_SEPARATED",
            "valid_for_claim": "false",
        },
    ]


def silence_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "SIL3351_0_parent_absence",
            "claim_piece": "parent decoupled field silence",
            "mathematical_form": "Args(S_parent) excludes S_D, T_D, P_D, and readout source projectors in the local ordinary arena",
            "result": "WOULD_IMPLY_EPSILON_DECOUPLED_FIELD_ZERO",
            "blocker": "3346 normal form is candidate/conditional, not a signed field-by-field parent action certificate",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SIL3351_1_bianchi_filter",
            "claim_piece": "nonvariational T_D filter",
            "mathematical_form": "nabla_mu E^{mu nu}=0 requires nabla_mu(T_H^{mu nu}+T_D^{mu nu})=0; if ordinary EOM give nabla_mu T_H^{mu nu}=0 then T_D must be separately conserved or rejected",
            "result": "SEPARATELY_CONSERVED_OR_INCONSISTENT",
            "blocker": "separately conserved blocks still need parent inventory or finite density/coupling bounds",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SIL3351_2_WEP_common_background",
            "claim_piece": "smooth universal background is not a material response factor",
            "mathematical_form": "a_D^A=a_D^B for co-located test bodies under universal coupling, so eta_AB receives no leading material-differential term from a smooth common field",
            "result": "WEP_MATERIAL_RESPONSE_SILENCED_CONDITIONALLY",
            "blocker": "gradients/tides/nonuniversal couplings/readout projectors require separate residual rows",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SIL3351_3_density_fallback",
            "claim_piece": "if ambient T_D remains, use density anchor not material R_AB",
            "mathematical_form": "epsilon_decoupled_field_density <= (g_D/g_N) P_D rho_D/rho_ref",
            "result": "FINITE_DENSITY_INTERFACE_DEFINED",
            "blocker": "g_D and P_D are parent/coupling/projection unknowns",
            "valid_for_claim": "false",
        },
    ]


def density_anchor_rows() -> list[dict[str, Any]]:
    nominal = kg_m3(RHO_DM_NOMINAL_GEV_CM3)
    high = kg_m3(RHO_DM_HIGH_GEV_CM3)
    return [
        {
            "density_id": "DENS3351_0_nominal_local_DM_scale",
            "source_kind": "ambient decoupled/background density anchor",
            "rho_GeV_cm3": f"{RHO_DM_NOMINAL_GEV_CM3:.6e}",
            "rho_kg_m3": f"{nominal:.6e}",
            "rho_ref_kg_m3": f"{RHO_SOLID_REFERENCE_KG_M3:.6e}",
            "rho_over_ref": f"{nominal / RHO_SOLID_REFERENCE_KG_M3:.6e}",
            "source_url": "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-dark-matter.pdf",
            "use": "private density-scale anchor only",
            "valid_for_density_anchor": "true",
            "valid_for_claim": "false",
        },
        {
            "density_id": "DENS3351_1_conservative_high_local_DM_scale",
            "source_kind": "ambient decoupled/background density envelope",
            "rho_GeV_cm3": f"{RHO_DM_HIGH_GEV_CM3:.6e}",
            "rho_kg_m3": f"{high:.6e}",
            "rho_ref_kg_m3": f"{RHO_SOLID_REFERENCE_KG_M3:.6e}",
            "rho_over_ref": f"{high / RHO_SOLID_REFERENCE_KG_M3:.6e}",
            "source_url": "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-dark-matter.pdf",
            "use": "conservative high-density scale for residual-interface smoke",
            "valid_for_density_anchor": "true",
            "valid_for_claim": "false",
        },
    ]


def finite_residual_rows() -> list[dict[str, Any]]:
    high = kg_m3(RHO_DM_HIGH_GEV_CM3)
    density_ratio = high / RHO_SOLID_REFERENCE_KG_M3
    return [
        {
            "residual_id": "FR3351_0_epsilon_decoupled_field_density_anchor",
            "symbol": "epsilon_decoupled_field",
            "branch": "smooth ambient density fallback",
            "formula": "epsilon_decoupled_field <= |g_D/g_N| |P_D| rho_D/rho_ref",
            "density_component_value": f"{density_ratio:.6e}",
            "density_component_units": "dimensionless_vs_1000kg_m3_reference",
            "source_url": "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-dark-matter.pdf",
            "claim_blocker": "coupling ratio g_D/g_N and projection P_D are not parent-derived or empirically bounded here",
            "valid_for_component_bound": "true",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "FR3351_1_epsilon_decoupled_field_clump_open",
            "symbol": "epsilon_decoupled_field",
            "branch": "local clump/contact/domain residual",
            "formula": "epsilon_decoupled_field_clump <= |g_D/g_N| |P_D| rho_D,local/rho_ref",
            "density_component_value": "open_local_clump_density",
            "density_component_units": "requires_local_density_or_gradient_bound",
            "source_url": "local_corpus",
            "claim_blocker": "no local hidden clump/contact density source row acquired",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "FR3351_2_readout_shadow_separated",
            "symbol": "epsilon_readout_source_shadow",
            "branch": "projector/readout not density",
            "formula": "handled by parent no-projector or projector norm bound, not by rho_D",
            "density_component_value": "not_applicable",
            "density_component_units": "not_density_branch",
            "source_url": "local_corpus",
            "claim_blocker": "parent no-projector signature remains unsigned",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3351_0_absence_theorem_written",
            "claim": "parent absence of decoupled T_D would zero epsilon_decoupled_field",
            "passed": "true",
            "reason": "3351 states the exact Args(S_parent) silence condition",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3351_1_parent_absence_signed",
            "claim": "current MTS parent action excludes T_D in local ordinary arenas",
            "passed": "false",
            "reason": "normal form remains candidate and field-by-field parent inventory is not closed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3351_2_density_anchor_acquired",
            "claim": "ambient decoupled-density fallback has a source-backed scale",
            "passed": "true",
            "reason": "PDG dark matter density scale is converted into SI and density-ratio rows",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3351_3_coupling_projection_bound",
            "claim": "decoupled residual has a complete numeric bound",
            "passed": "false",
            "reason": "density scale exists, but g_D/g_N and P_D are still open",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3351_4_local_GR_claim",
            "claim": "local GR/Newton source-coupling branch is claim-ready",
            "passed": "false",
            "reason": "parent decoupled absence and coupling/projection bound remain open",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3351_0",
            "question": "Did 3351 prove parent decoupled-field silence?",
            "answer": "no",
            "reason": "it derives the exact silence condition, but the current parent action is not signed enough to apply it",
            "next_action": "attack g_D/P_D coupling-projection ownership or close the parent absence clause",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3351_1",
            "question": "Did 3351 produce a real fallback rather than another missing row?",
            "answer": "yes",
            "reason": "it adds a source-backed density anchor and a finite residual interface, while refusing to claim without coupling/projection bounds",
            "next_action": "3352 should try to prove g_D P_D=0 or obtain a real bound for the decoupled coupling/projection factor",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3352-Y5-R2FR-decoupled-coupling-projection-zero-or-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3352_decoupled_coupling_projection_zero_or_bound.py",
            "objective": "prove g_D P_D=0 from parent action/source-map ownership, or acquire a source-backed finite coupling/projection bound for epsilon_decoupled_field",
            "why_next": "3351 supplied a density scale; the remaining nonclaim factor is the decoupled coupling/projection owner",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3352b-Y5-R2FR-boundary-contact-silence-or-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3352b_boundary_contact_silence_or_bound.py",
            "objective": "parallel cleanup: prove boundary/contact silence or bound epsilon_boundary_contact",
            "why_next": "boundary/contact residual is separated from decoupled density but still blocks local-GR promotion",
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
    return "\n".join(lines)


def render_doc() -> str:
    return "\n\n".join(
        [
            "# 3351 — Parent Decoupled-Field Silence Or Bound Under AX1090",
            f"Generated: `{RUN_UTC}`",
            "## Summary\n"
            "- This checkpoint attacks `epsilon_decoupled_field`, the parent field-equation residual left by 3350.\n"
            "- The theorem-zero route is exact but conditional: if `Args(S_parent)` has no `T_D`, `S_D`, `P_D`, or readout source projector in the local ordinary arena, then `epsilon_decoupled_field=0`.\n"
            "- Current MTS cannot promote that zero yet, so 3351 adds a source-backed ambient-density fallback using the PDG dark-matter density scale.\n"
            "- The fallback is still nonclaim: density is now anchored, but the coupling/projection factor `g_D P_D` is not derived or bounded.",
            "## Web Source Register\n" + markdown_table(web_source_rows()),
            "## Decoupled Field Trichotomy\n" + markdown_table(trichotomy_rows()),
            "## Silence Theorem Attempt\n" + markdown_table(silence_theorem_rows()),
            "## Density Anchor Rows\n" + markdown_table(density_anchor_rows()),
            "## Finite Residual Rows\n" + markdown_table(finite_residual_rows()),
            "## Promotion Gates\n" + markdown_table(promotion_gate_rows()),
            "## Decision Ledger\n" + markdown_table(decision_rows()),
            "## Next Target\n" + markdown_table(next_target_rows()),
        ]
    ) + "\n"


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    local_sources = local_source_rows()
    density = density_anchor_rows()
    residuals = finite_residual_rows()
    gates = promotion_gate_rows()
    formalization_changed = changed_count(formalization_before, snapshot_tree(FW))
    high_row = next(row for row in density if row["density_id"] == "DENS3351_1_conservative_high_local_DM_scale")
    checks = [
        {
            "check_id": "VAL3351_0_local_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3351_1_local_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3351_2_web_sources_well_formed",
            "check": "all web source URLs are nonempty http links",
            "passed": all(row["url"].startswith("http") for row in web_source_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3351_3_outputs_parse",
            "check": "all 3351 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3351_4_trichotomy_complete",
            "check": "trichotomy covers absent, variational, smooth background, clumped, and projector branches",
            "passed": {row["case_id"] for row in trichotomy_rows()}
            == {"TRI3351_0_absent_parent_slot", "TRI3351_1_variational_parent_block", "TRI3351_2_smooth_universal_background", "TRI3351_3_clumped_or_local_decoupled_source", "TRI3351_4_nonuniversal_projector"},
            "detail": "",
        },
        {
            "check_id": "VAL3351_5_density_numeric_positive",
            "check": "density anchors are positive finite SI conversions",
            "passed": all(math.isfinite(float(row["rho_kg_m3"])) and float(row["rho_kg_m3"]) > 0.0 for row in density),
            "detail": "",
        },
        {
            "check_id": "VAL3351_6_high_density_ratio_expected",
            "check": "conservative high density ratio is finite and tiny against 1000 kg/m^3 reference",
            "passed": math.isfinite(float(high_row["rho_over_ref"])) and 0.0 < float(high_row["rho_over_ref"]) < 1e-20,
            "detail": f"rho_over_ref={high_row['rho_over_ref']}",
        },
        {
            "check_id": "VAL3351_7_residuals_nonclaim",
            "check": "finite residual rows remain nonclaim and separate density from coupling/projection",
            "passed": all(row["valid_for_claim"] == "false" for row in residuals)
            and any(row["residual_id"] == "FR3351_0_epsilon_decoupled_field_density_anchor" and row["valid_for_component_bound"] == "true" for row in residuals),
            "detail": "",
        },
        {
            "check_id": "VAL3351_8_no_overclaim",
            "check": "parent absence, coupling projection, and local-GR gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3351_1_parent_absence_signed", "GATE3351_3_coupling_projection_bound", "GATE3351_4_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3351_9_next_target_coupling_projection",
            "check": "next target attacks g_D P_D coupling/projection",
            "passed": any("g_D P_D" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3351_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": formalization_changed == 0,
            "detail": f"formalization_changed_count={formalization_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3351_11_overall",
            "check": "3351 validation overall",
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
    write_csv(OUTPUTS["local_sources"], local_source_rows())
    write_csv(OUTPUTS["web_sources"], web_source_rows())
    write_csv(OUTPUTS["trichotomy"], trichotomy_rows())
    write_csv(OUTPUTS["silence"], silence_theorem_rows())
    write_csv(OUTPUTS["density"], density_anchor_rows())
    write_csv(OUTPUTS["residuals"], finite_residual_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()

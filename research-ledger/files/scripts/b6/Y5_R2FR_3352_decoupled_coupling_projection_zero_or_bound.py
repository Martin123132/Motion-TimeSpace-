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
DOC = ROOT / "3352-Y5-R2FR-decoupled-coupling-projection-zero-or-bound-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

LOCAL_SOURCES = [
    ("LSRC3352_0_3351_doc", ROOT / "3351-Y5-R2FR-parent-decoupled-field-silence-or-bound-under-AX1090.md", "3351 decoupled density handoff"),
    ("LSRC3352_1_3351_silence", OUT / "P8_Y5_R2FR_3351_SILENCE_THEOREM_ATTEMPT.csv", "3351 silence theorem attempt"),
    ("LSRC3352_2_3351_density", OUT / "P8_Y5_R2FR_3351_DENSITY_ANCHOR_ROWS.csv", "3351 density anchors"),
    ("LSRC3352_3_3351_residuals", OUT / "P8_Y5_R2FR_3351_FINITE_RESIDUAL_ROWS.csv", "3351 finite residual rows"),
    ("LSRC3352_4_3351_gates", OUT / "P8_Y5_R2FR_3351_PROMOTION_GATES.csv", "3351 promotion gates"),
    ("LSRC3352_5_3350_residuals", OUT / "P8_Y5_R2FR_3350_EXPLICIT_RESIDUAL_ROWS.csv", "3350 explicit residual rows"),
    ("LSRC3352_6_3346_forbidden", OUT / "P8_Y5_R2FR_3346_FORBIDDEN_ARGUMENT_INVENTORY.csv", "3346 forbidden parent arguments"),
    ("LSRC3352_7_3346_normal_form", OUT / "P8_Y5_R2FR_3346_PARENT_ACTION_NORMAL_FORM.csv", "3346 candidate parent normal form"),
]

WEB_SOURCES = [
    {
        "web_source_id": "WEB3352_0_PDG_dark_matter_2025",
        "title": "Particle Data Group Review: Dark Matter",
        "url": "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-dark-matter.pdf",
        "usage": "inherits 3351 local density scale for the universal/background branch",
        "valid_for_claim": "false",
    },
    {
        "web_source_id": "WEB3352_1_MICROSCOPE_final",
        "title": "MICROSCOPE Mission final equivalence-principle result",
        "url": "https://link.aps.org/doi/10.1103/PhysRevLett.129.121102",
        "usage": "keeps WEP material-response branch separated from density/coupling branch",
        "valid_for_claim": "false",
    },
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3352_LOCAL_SOURCE_REGISTER.csv",
    "web_sources": OUT / "P8_Y5_R2FR_3352_WEB_SOURCE_REGISTER.csv",
    "fork": OUT / "P8_Y5_R2FR_3352_COUPLING_PROJECTION_FORK.csv",
    "zero": OUT / "P8_Y5_R2FR_3352_GDPD_ZERO_THEOREM_ATTEMPT.csv",
    "branches": OUT / "P8_Y5_R2FR_3352_BRANCH_RESIDUAL_BOUNDS.csv",
    "component": OUT / "P8_Y5_R2FR_3352_EPSILON_DECOUPLED_COMPONENT_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3352_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3352_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3352_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3352_VALIDATION.csv",
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


def high_density_ratio() -> float:
    rows = read_csv(OUT / "P8_Y5_R2FR_3351_DENSITY_ANCHOR_ROWS.csv")
    for row in rows:
        if row["density_id"] == "DENS3351_1_conservative_high_local_DM_scale":
            return float(row["rho_over_ref"])
    raise RuntimeError("Missing 3351 conservative density ratio")


def coupling_projection_fork_rows() -> list[dict[str, Any]]:
    return [
        {
            "fork_id": "FORK3352_0_parent_absent",
            "branch": "parent-zero",
            "condition": "S_D, T_D, P_D, and readout source projectors are absent from Args(S_parent)",
            "g_D_over_g_N": "0",
            "P_D": "0",
            "gD_PD": "0",
            "epsilon_decoupled_field_effect": "0",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "fork_id": "FORK3352_1_universal_metric_background",
            "branch": "universal-density",
            "condition": "T_D is a smooth universally metric-coupled background source",
            "g_D_over_g_N": "1",
            "P_D": "1",
            "gD_PD": "1",
            "epsilon_decoupled_field_effect": "density-only common/background residual; not material R_AB",
            "status": "FINITE_DENSITY_COMPONENT_AVAILABLE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "fork_id": "FORK3352_2_nonuniversal_projection",
            "branch": "projector-or-fifth-force",
            "condition": "T_D couples through nonuniversal source projector, hidden frame, or readout map",
            "g_D_over_g_N": "alpha_D",
            "P_D": "P_D(labels,arena)",
            "gD_PD": "alpha_D P_D",
            "epsilon_decoupled_field_effect": "requires source-backed coupling/projection bound; cannot use density alone",
            "status": "OPEN_FINITE_BOUND_BRANCH",
            "valid_for_claim": "false",
        },
        {
            "fork_id": "FORK3352_3_local_clump",
            "branch": "local-clump-contact",
            "condition": "local hidden density/contact/domain object is present",
            "g_D_over_g_N": "alpha_D_local",
            "P_D": "P_D,local",
            "gD_PD": "alpha_D_local P_D,local",
            "epsilon_decoupled_field_effect": "requires local density/gradient/contact search, not solar-neighbourhood smooth density",
            "status": "OPEN_LOCAL_BOUND_BRANCH",
            "valid_for_claim": "false",
        },
    ]


def zero_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "GDPD3352_0_absent_slot",
            "claim_piece": "g_D P_D = 0 by absent parent slot",
            "mathematical_form": "if T_D notin Args(S_parent) and P_D notin SourceMap(S_parent), then delta S_parent/delta g has no decoupled source projector",
            "result": "EXACT_CONDITIONAL_ZERO",
            "blocker": "3346 normal form is candidate/conditional; no field-by-field parent absence certificate yet",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "GDPD3352_1_universal_branch",
            "claim_piece": "universal metric coupling is not a material response projector",
            "mathematical_form": "g_D/g_N=1 and P_D=1 for total metric source, but eta_AB material response remains zero at leading common-field order",
            "result": "DENSITY_BACKGROUND_BRANCH_SEPARATED",
            "blocker": "still a field-equation density residual, not a full local-GR theorem-zero",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "GDPD3352_2_nonuniversal_projector",
            "claim_piece": "nonuniversal g_D P_D is source-shadow/hidden-frame content",
            "mathematical_form": "alpha_D P_D(labels) is an extra source-map/hidden-frame argument and must be forbidden by parent grammar or bounded",
            "result": "ROUTED_TO_EXPLICIT_RESIDUAL",
            "blocker": "no source-backed alpha_D P_D bound in current corpus",
            "valid_for_claim": "false",
        },
    ]


def branch_residual_rows() -> list[dict[str, Any]]:
    ratio = high_density_ratio()
    return [
        {
            "branch_bound_id": "BB3352_0_parent_zero",
            "branch": "parent-zero",
            "formula": "epsilon_decoupled_field = 0",
            "gD_PD_assumption": "0",
            "density_ratio": "not_used",
            "component_bound": "0",
            "bound_status": "THEOREM_IF_PARENT_SIGNED",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_bound_id": "BB3352_1_universal_density_smoke",
            "branch": "universal-density",
            "formula": "epsilon_decoupled_field_density <= rho_D/rho_ref for g_D P_D=1",
            "gD_PD_assumption": "1",
            "density_ratio": f"{ratio:.6e}",
            "component_bound": f"{ratio:.6e}",
            "bound_status": "SOURCE_BACKED_DENSITY_COMPONENT_NONCLAIM",
            "valid_for_component_bound": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_bound_id": "BB3352_2_nonuniversal_open",
            "branch": "projector-or-fifth-force",
            "formula": "epsilon_decoupled_field <= |alpha_D P_D| rho_D/rho_ref",
            "gD_PD_assumption": "alpha_D P_D open",
            "density_ratio": f"{ratio:.6e}",
            "component_bound": f"|alpha_D P_D|*{ratio:.6e}",
            "bound_status": "SYMBOLIC_UNTIL_COUPLING_PROJECTION_BOUND",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_bound_id": "BB3352_3_local_clump_open",
            "branch": "local-clump-contact",
            "formula": "epsilon_decoupled_field <= |alpha_D,local P_D,local| rho_D,local/rho_ref",
            "gD_PD_assumption": "alpha_D_local P_D_local open",
            "density_ratio": "rho_D,local/rho_ref open",
            "component_bound": "open",
            "bound_status": "NO_LOCAL_DENSITY_OR_GRADIENT_BOUND",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
    ]


def component_update_rows() -> list[dict[str, Any]]:
    ratio = high_density_ratio()
    return [
        {
            "component_id": "COMP3352_0_epsilon_decoupled_universal_density",
            "symbol": "epsilon_decoupled_field",
            "mode": "universal_density_component_nonclaim",
            "theorem_zero": "false",
            "component_value": f"{ratio:.6e}",
            "component_units": "dimensionless_density_ratio_vs_1000kg_m3",
            "coupling_projection_factor": "g_D P_D = 1 on universal metric branch only",
            "source_path": str(OUT / "P8_Y5_R2FR_3351_DENSITY_ANCHOR_ROWS.csv"),
            "valid_for_component_bound": "true",
            "valid_for_claim": "false",
            "claim_blocker": "universal density component does not prove parent absence; nonuniversal/projector and local-clump branches remain open",
        },
        {
            "component_id": "COMP3352_1_epsilon_decoupled_parent_zero_contract",
            "symbol": "epsilon_decoupled_field",
            "mode": "parent_absence_zero_contract",
            "theorem_zero": "true_if_parent_signed",
            "component_value": "0",
            "component_units": "dimensionless",
            "coupling_projection_factor": "g_D P_D = 0",
            "source_path": str(OUT / "P8_Y5_R2FR_3346_PARENT_ACTION_NORMAL_FORM.csv"),
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
            "claim_blocker": "parent absence of T_D/S_D/P_D is not field-by-field signed",
        },
        {
            "component_id": "COMP3352_2_epsilon_decoupled_nonuniversal_open",
            "symbol": "epsilon_decoupled_field",
            "mode": "nonuniversal_projector_branch",
            "theorem_zero": "false",
            "component_value": f"|alpha_D P_D|*{ratio:.6e}",
            "component_units": "symbolic_dimensionless",
            "coupling_projection_factor": "alpha_D P_D open",
            "source_path": str(OUT / "P8_Y5_R2FR_3351_FINITE_RESIDUAL_ROWS.csv"),
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
            "claim_blocker": "requires source-backed alpha_D/P_D bound or parent no-projector theorem",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3352_0_fork_derived",
            "claim": "g_D P_D fork is explicitly separated into parent-zero, universal-density, nonuniversal, and local-clump branches",
            "passed": "true",
            "reason": "3352 coupling-projection fork rows cover all active branches",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3352_1_parent_zero_signed",
            "claim": "g_D P_D=0 is parent-signed for current MTS",
            "passed": "false",
            "reason": "parent absence of T_D/S_D/P_D remains candidate, not field-by-field signed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3352_2_universal_density_component",
            "claim": "universal-density branch has a numeric nonclaim component",
            "passed": "true",
            "reason": "3351 density ratio is reused with g_D P_D=1 branch assumption",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3352_3_nonuniversal_bound",
            "claim": "nonuniversal/projector branch has a complete source-backed bound",
            "passed": "false",
            "reason": "alpha_D P_D remains symbolic",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3352_4_local_clump_bound",
            "claim": "local clump/contact branch has a complete source-backed bound",
            "passed": "false",
            "reason": "rho_D,local/gradient/contact density is not acquired",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3352_5_local_GR_claim",
            "claim": "local GR/Newton source-coupling branch is claim-ready",
            "passed": "false",
            "reason": "parent zero, nonuniversal projector, local clump, and boundary/contact branches still block promotion",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3352_0",
            "question": "Did 3352 prove g_D P_D=0?",
            "answer": "not for current MTS",
            "reason": "the zero theorem is exact if the parent action excludes T_D/S_D/P_D, but current parent syntax is not signed",
            "next_action": "attack parent absence field-by-field or bound the nonuniversal projector branch",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3352_1",
            "question": "Did 3352 move the residual forward?",
            "answer": "yes",
            "reason": "the universal-density branch now has a numeric component 2.673993e-24, while the remaining open parts are isolated to alpha_D P_D and local clump/contact density",
            "next_action": "3353 should decide whether to close parent no-T_D syntax or source nonuniversal fifth-force/projector bounds",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3353-Y5-R2FR-parent-no-TD-syntax-or-nonuniversal-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3353_parent_no_TD_syntax_or_nonuniversal_bound.py",
            "objective": "either field-by-field sign the parent absence of T_D/S_D/P_D, or acquire source-backed nonuniversal/projector coupling bounds for alpha_D P_D",
            "why_next": "3352 reduced the decoupled density branch to a tiny numeric component; the open blocker is nonuniversal/projector coupling or parent syntax",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3352b-Y5-R2FR-boundary-contact-silence-or-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3352b_boundary_contact_silence_or_bound.py",
            "objective": "parallel cleanup: prove boundary/contact silence or bound epsilon_boundary_contact",
            "why_next": "boundary/contact remains separated from decoupled density and still blocks local-GR promotion",
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
            "# 3352 — Decoupled Coupling-Projection Zero Or Bound Under AX1090",
            f"Generated: `{RUN_UTC}`",
            "## Summary\n"
            "- This checkpoint attacks the remaining `g_D P_D` factor in `epsilon_decoupled_field`.\n"
            "- The result is a clean fork: parent absence gives `g_D P_D=0`; universal metric-coupled background gives a tiny density component; nonuniversal/projector and local-clump branches remain open.\n"
            "- The universal-density branch now has a numeric nonclaim component `2.673993e-24`, inherited from the 3351 density anchor.\n"
            "- Local GR is still not promoted because the parent-zero and nonuniversal/projector branches remain unsigned/unbounded.",
            "## Web Source Register\n" + markdown_table(web_source_rows()),
            "## Coupling Projection Fork\n" + markdown_table(coupling_projection_fork_rows()),
            "## GDPD Zero Theorem Attempt\n" + markdown_table(zero_theorem_rows()),
            "## Branch Residual Bounds\n" + markdown_table(branch_residual_rows()),
            "## Epsilon Decoupled Component Update\n" + markdown_table(component_update_rows()),
            "## Promotion Gates\n" + markdown_table(promotion_gate_rows()),
            "## Decision Ledger\n" + markdown_table(decision_rows()),
            "## Next Target\n" + markdown_table(next_target_rows()),
        ]
    ) + "\n"


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    local_sources = local_source_rows()
    fork = coupling_projection_fork_rows()
    branches = branch_residual_rows()
    components = component_update_rows()
    gates = promotion_gate_rows()
    formalization_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3352_0_local_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3352_1_local_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3352_2_web_sources_well_formed",
            "check": "all web source URLs are nonempty http links",
            "passed": all(row["url"].startswith("http") for row in web_source_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3352_3_outputs_parse",
            "check": "all 3352 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3352_4_fork_complete",
            "check": "fork covers parent-zero, universal-density, nonuniversal, and local-clump branches",
            "passed": {row["fork_id"] for row in fork}
            == {"FORK3352_0_parent_absent", "FORK3352_1_universal_metric_background", "FORK3352_2_nonuniversal_projection", "FORK3352_3_local_clump"},
            "detail": "",
        },
        {
            "check_id": "VAL3352_5_universal_component_numeric",
            "check": "universal-density component is positive finite and nonclaim",
            "passed": any(
                row["branch_bound_id"] == "BB3352_1_universal_density_smoke"
                and math.isfinite(float(row["component_bound"]))
                and float(row["component_bound"]) > 0.0
                and row["valid_for_claim"] == "false"
                for row in branches
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3352_6_component_update_nonclaim",
            "check": "component update has numeric universal row and open nonuniversal row",
            "passed": any(row["component_id"] == "COMP3352_0_epsilon_decoupled_universal_density" and row["valid_for_component_bound"] == "true" for row in components)
            and any(row["component_id"] == "COMP3352_2_epsilon_decoupled_nonuniversal_open" and row["valid_for_component_bound"] == "false" for row in components),
            "detail": "",
        },
        {
            "check_id": "VAL3352_7_no_overclaim",
            "check": "parent zero, nonuniversal, local clump, and local-GR gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3352_1_parent_zero_signed", "GATE3352_3_nonuniversal_bound", "GATE3352_4_local_clump_bound", "GATE3352_5_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3352_8_next_target_parent_or_nonuniversal",
            "check": "next target attacks parent no-TD syntax or nonuniversal coupling bound",
            "passed": any("T_D/S_D/P_D" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3352_9_no_missing_in_numeric_component",
            "check": "numeric component row contains no MISSING markers",
            "passed": all("MISSING_" not in "|".join(str(value) for value in row.values()) for row in components if row["component_id"] == "COMP3352_0_epsilon_decoupled_universal_density"),
            "detail": "",
        },
        {
            "check_id": "VAL3352_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": formalization_changed == 0,
            "detail": f"formalization_changed_count={formalization_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3352_11_overall",
            "check": "3352 validation overall",
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
    write_csv(OUTPUTS["fork"], coupling_projection_fork_rows())
    write_csv(OUTPUTS["zero"], zero_theorem_rows())
    write_csv(OUTPUTS["branches"], branch_residual_rows())
    write_csv(OUTPUTS["component"], component_update_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()

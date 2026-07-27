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
DOC = ROOT / "3353-Y5-R2FR-parent-no-TD-syntax-or-nonuniversal-bound-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

LOCAL_SOURCES = [
    ("LSRC3353_0_3352_doc", ROOT / "3352-Y5-R2FR-decoupled-coupling-projection-zero-or-bound-under-AX1090.md", "3352 coupling/projection handoff"),
    ("LSRC3353_1_3352_fork", OUT / "P8_Y5_R2FR_3352_COUPLING_PROJECTION_FORK.csv", "3352 coupling projection fork"),
    ("LSRC3353_2_3352_zero", OUT / "P8_Y5_R2FR_3352_GDPD_ZERO_THEOREM_ATTEMPT.csv", "3352 zero theorem attempt"),
    ("LSRC3353_3_3352_bounds", OUT / "P8_Y5_R2FR_3352_BRANCH_RESIDUAL_BOUNDS.csv", "3352 branch bounds"),
    ("LSRC3353_4_3352_component", OUT / "P8_Y5_R2FR_3352_EPSILON_DECOUPLED_COMPONENT_UPDATE.csv", "3352 component update"),
    ("LSRC3353_5_3346_normal", OUT / "P8_Y5_R2FR_3346_PARENT_ACTION_NORMAL_FORM.csv", "3346 parent normal form"),
    ("LSRC3353_6_3346_allowed", OUT / "P8_Y5_R2FR_3346_ALLOWED_ARGUMENT_INVENTORY.csv", "3346 allowed argument inventory"),
    ("LSRC3353_7_3346_forbidden", OUT / "P8_Y5_R2FR_3346_FORBIDDEN_ARGUMENT_INVENTORY.csv", "3346 forbidden argument inventory"),
    ("LSRC3353_8_3346_closure", OUT / "P8_Y5_R2FR_3346_CLOSURE_CERTIFICATE_ATTEMPT.csv", "3346 closure status"),
    ("LSRC3353_9_3342_wep", OUT / "P8_Y5_R2FR_3342_WEP_BOUND_ROWS.csv", "3342 MICROSCOPE WEP bound rows"),
    ("LSRC3353_10_3351_density", OUT / "P8_Y5_R2FR_3351_DENSITY_ANCHOR_ROWS.csv", "3351 density anchor rows"),
]

WEB_SOURCES = [
    {
        "web_source_id": "WEB3353_0_MICROSCOPE_final",
        "title": "MICROSCOPE Mission final equivalence-principle result",
        "url": "https://link.aps.org/doi/10.1103/PhysRevLett.129.121102",
        "usage": "source-backed WEP number used for an intentionally weak alpha_D P_D smoke bound",
        "valid_for_claim": "false",
    },
    {
        "web_source_id": "WEB3353_1_PDG_dark_matter_2025",
        "title": "Particle Data Group Review: Dark Matter",
        "url": "https://pdg.lbl.gov/2025/reviews/rpp2025-rev-dark-matter.pdf",
        "usage": "source-backed smooth density scale used in the denominator of the alpha_D P_D smoke bound",
        "valid_for_claim": "false",
    },
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3353_LOCAL_SOURCE_REGISTER.csv",
    "web_sources": OUT / "P8_Y5_R2FR_3353_WEB_SOURCE_REGISTER.csv",
    "syntax": OUT / "P8_Y5_R2FR_3353_PARENT_NO_TD_SYNTAX_AUDIT.csv",
    "zero": OUT / "P8_Y5_R2FR_3353_NO_TD_ZERO_CERTIFICATE_ATTEMPT.csv",
    "bounds": OUT / "P8_Y5_R2FR_3353_NONUNIVERSAL_ALPHA_BOUND_ROWS.csv",
    "component": OUT / "P8_Y5_R2FR_3353_EPSILON_DECOUPLED_COMPONENT_REPACK.csv",
    "gates": OUT / "P8_Y5_R2FR_3353_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3353_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3353_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3353_VALIDATION.csv",
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


def wep_bound_value() -> float:
    rows = read_csv(OUT / "P8_Y5_R2FR_3342_WEP_BOUND_ROWS.csv")
    for row in rows:
        if row["bound_id"] == "BND3342_1_MICROSCOPE_TiPt_abs_central_plus_sigma":
            return float(row["bound_value"])
    raise RuntimeError("Missing 3342 MICROSCOPE abs-plus-sigma row")


def density_ratio() -> float:
    rows = read_csv(OUT / "P8_Y5_R2FR_3351_DENSITY_ANCHOR_ROWS.csv")
    for row in rows:
        if row["density_id"] == "DENS3351_1_conservative_high_local_DM_scale":
            return float(row["rho_over_ref"])
    raise RuntimeError("Missing 3351 density ratio")


def alpha_smoke_bound() -> float:
    return wep_bound_value() / density_ratio()


def syntax_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "syntax_id": "SYN3353_0_candidate_action_args",
            "clause": "candidate S_parent argument list",
            "evidence": "S_geom[Phi;q] + S_matter[Psi_A,e_obs(q(Phi)),A_Q(q(Phi)),theta_A] + S_EM[...] + S_boundary[...]",
            "TD_slot_status": "NO_EXPLICIT_TD_SD_PD_SLOT_IN_CANDIDATE",
            "parent_signed": "false",
            "promotion_gap": "candidate normal form is not field-by-field parent action",
            "valid_for_claim": "false",
        },
        {
            "syntax_id": "SYN3353_1_forbidden_decoupled_block",
            "clause": "unlisted conserved nonordinary source block T_D is forbidden unless arena-inventoried and bounded",
            "evidence": "ARG3346_F5_uninventoried_decoupled_block",
            "TD_slot_status": "FORBIDDEN_IF_PARENT_DOMAIN_SIGNED",
            "parent_signed": "false",
            "promotion_gap": "forbidden clause is a typed contract, not yet parent-owned theorem",
            "valid_for_claim": "false",
        },
        {
            "syntax_id": "SYN3353_2_source_projector",
            "clause": "P_D or alpha_D P_D(labels) is a source projector/hidden-frame branch",
            "evidence": "ARG3346_F2_source_projector and ARG3346_F3_hidden_frame",
            "TD_slot_status": "ROUTED_TO_FORBIDDEN_PROJECTOR_OR_FRAME",
            "parent_signed": "false",
            "promotion_gap": "no field-by-field exclusion of all P_D/readout/projector aliases",
            "valid_for_claim": "false",
        },
        {
            "syntax_id": "SYN3353_3_boundary_exception",
            "clause": "boundary/improvement terms may be allowed only if classified",
            "evidence": "ARG3346_A5_boundary_terms and CLOSE3346_3_boundary_inventory",
            "TD_slot_status": "BOUNDARY_CONTACT_NOT_TD_BUT_STILL_OPEN",
            "parent_signed": "false",
            "promotion_gap": "boundary/contact silence is separate and not closed",
            "valid_for_claim": "false",
        },
    ]


def zero_certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "cert_id": "ZERO3353_0_candidate_no_TD",
            "claim_piece": "candidate parent normal form contains no T_D/S_D/P_D term",
            "result": "CANDIDATE_PASS",
            "mathematical_effect": "would set g_D P_D=0 if the candidate normal form is exhaustive",
            "why_not_promoted": "candidate normal form is not a signed parent action",
            "valid_for_claim": "false",
        },
        {
            "cert_id": "ZERO3353_1_alias_closure",
            "claim_piece": "all aliases of decoupled source projectors are excluded",
            "result": "NOT_CLOSED",
            "mathematical_effect": "alpha_D P_D cannot return under source-shadow, hidden-frame, reduced-readout, or boundary names",
            "why_not_promoted": "alias inventory is incomplete until parent action syntax is field-by-field closed",
            "valid_for_claim": "false",
        },
        {
            "cert_id": "ZERO3353_2_current_verdict",
            "claim_piece": "current MTS g_D P_D zero",
            "result": "NOT_PROMOTED",
            "mathematical_effect": "zero theorem exists but is not claim-ready",
            "why_not_promoted": "nonuniversal/projector branch remains live as explicit residual",
            "valid_for_claim": "false",
        },
    ]


def nonuniversal_bound_rows() -> list[dict[str, Any]]:
    eta = wep_bound_value()
    ratio = density_ratio()
    alpha_bound = alpha_smoke_bound()
    return [
        {
            "bound_id": "AB3353_0_MICROSCOPE_density_projection_smoke",
            "quantity": "abs(alpha_D P_D)",
            "branch": "nonuniversal density-to-WEP unit projection smoke",
            "formula": "|alpha_D P_D| <= |eta_TiPt| / (rho_D/rho_ref)",
            "eta_bound": f"{eta:.6e}",
            "density_ratio": f"{ratio:.6e}",
            "alphaD_PD_bound": f"{alpha_bound:.6e}",
            "units": "dimensionless_projection_factor",
            "source_paths": f"{OUT / 'P8_Y5_R2FR_3342_WEP_BOUND_ROWS.csv'}; {OUT / 'P8_Y5_R2FR_3351_DENSITY_ANCHOR_ROWS.csv'}",
            "interpretation": "finite but extremely weak; only valid under an unproven unit WEP projection from density residual to eta_TiPt",
            "valid_for_component_bound": "true",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "AB3353_1_parent_projector_zero_contract",
            "quantity": "alpha_D P_D",
            "branch": "parent no-projector syntax",
            "formula": "alpha_D P_D = 0 if P_D notin Args(S_parent) and no hidden-frame/readout alias exists",
            "eta_bound": "not_used",
            "density_ratio": "not_used",
            "alphaD_PD_bound": "0_if_parent_signed",
            "units": "dimensionless_projection_factor",
            "source_paths": str(OUT / "P8_Y5_R2FR_3346_PARENT_ACTION_NORMAL_FORM.csv"),
            "interpretation": "preferred derivation route; not parent-signed yet",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
    ]


def component_repack_rows() -> list[dict[str, Any]]:
    ratio = density_ratio()
    alpha_bound = alpha_smoke_bound()
    return [
        {
            "component_id": "COMP3353_0_universal_density_branch",
            "symbol": "epsilon_decoupled_field",
            "branch": "universal density nonclaim",
            "component_value": f"{ratio:.6e}",
            "status": "SOURCE_BACKED_DENSITY_COMPONENT",
            "valid_for_component_bound": "true",
            "valid_for_claim": "false",
        },
        {
            "component_id": "COMP3353_1_nonuniversal_smoke_bound",
            "symbol": "alpha_D P_D",
            "branch": "unit WEP projection smoke",
            "component_value": f"{alpha_bound:.6e}",
            "status": "FINITE_BUT_WEAK_AND_PROJECTION_ASSUMED",
            "valid_for_component_bound": "true",
            "valid_for_claim": "false",
        },
        {
            "component_id": "COMP3353_2_parent_zero_contract",
            "symbol": "g_D P_D",
            "branch": "parent syntax zero",
            "component_value": "0_if_parent_signed",
            "status": "PREFERRED_BUT_NOT_PROMOTED",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3353_0_candidate_no_TD_syntax",
            "claim": "candidate parent syntax contains no explicit T_D/S_D/P_D slot",
            "passed": "true",
            "reason": "3346 normal form lists q-visible geometry, ordinary matter, EM/current, constants, and boundary only",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3353_1_parent_no_TD_promoted",
            "claim": "parent no-TD/no-PD syntax is field-by-field signed for current MTS",
            "passed": "false",
            "reason": "3346 closure certificate remains NOT_CLOSED",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3353_2_nonuniversal_smoke_bound",
            "claim": "nonuniversal alpha_D P_D has a finite source-backed smoke bound",
            "passed": "true",
            "reason": "MICROSCOPE eta bound divided by PDG density ratio gives a finite but weak projection-assumed bound",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3353_3_nonuniversal_claim_bound",
            "claim": "nonuniversal alpha_D P_D has a claim-ready physical bound",
            "passed": "false",
            "reason": "unit WEP projection is not parent-derived and local clump/projector branches remain open",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3353_4_local_GR_claim",
            "claim": "local GR/Newton source-coupling branch is claim-ready",
            "passed": "false",
            "reason": "parent syntax, source-shadow/readout, boundary/contact, and local clump branches remain open",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3353_0",
            "question": "Did 3353 field-by-field sign parent absence of T_D/S_D/P_D?",
            "answer": "no",
            "reason": "candidate syntax excludes them, but the parent action certificate remains non-exhaustive",
            "next_action": "do alias closure around source-shadow/readout/hidden-frame/boundary names or attack boundary-contact branch",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3353_1",
            "question": "Did 3353 produce a useful nonuniversal bound?",
            "answer": "weak smoke only",
            "reason": "alpha_D P_D <= eta/rho_ratio is finite but huge because local dark density is tiny relative to material density",
            "next_action": "prefer parent-zero syntax over empirical alpha_D P_D fitting unless a better projection observable is derived",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3354-Y5-R2FR-source-shadow-readout-alias-closure-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3354_source_shadow_readout_alias_closure.py",
            "objective": "close or bound the aliases by which T_D/P_D can return: source-shadow, hidden-frame, reduced-readout, and boundary/contact names",
            "why_next": "3353 shows candidate parent syntax excludes T_D/P_D, but alias closure is the reason it cannot be promoted",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3352b-Y5-R2FR-boundary-contact-silence-or-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3352b_boundary_contact_silence_or_bound.py",
            "objective": "parallel cleanup: prove boundary/contact silence or bound epsilon_boundary_contact",
            "why_next": "boundary/contact remains a named alias route for hidden source return",
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
            "# 3353 — Parent No-TD Syntax Or Nonuniversal Bound Under AX1090",
            f"Generated: `{RUN_UTC}`",
            "## Summary\n"
            "- This checkpoint attacks the open `alpha_D P_D` branch left by 3352.\n"
            "- Candidate parent syntax contains no explicit `T_D/S_D/P_D` slot, but this is not promoted because alias closure is incomplete.\n"
            "- A finite nonuniversal smoke bound is staged: `|alpha_D P_D| <= eta_TiPt/(rho_D/rho_ref)`, which is source-backed but physically weak and projection-assumed.\n"
            "- The preferred route is still parent-zero syntax; empirical fitting is the ugly fallback.",
            "## Web Source Register\n" + markdown_table(web_source_rows()),
            "## Parent No-TD Syntax Audit\n" + markdown_table(syntax_audit_rows()),
            "## No-TD Zero Certificate Attempt\n" + markdown_table(zero_certificate_rows()),
            "## Nonuniversal Alpha Bound Rows\n" + markdown_table(nonuniversal_bound_rows()),
            "## Epsilon Decoupled Component Repack\n" + markdown_table(component_repack_rows()),
            "## Promotion Gates\n" + markdown_table(promotion_gate_rows()),
            "## Decision Ledger\n" + markdown_table(decision_rows()),
            "## Next Target\n" + markdown_table(next_target_rows()),
        ]
    ) + "\n"


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    local_sources = local_source_rows()
    syntax = syntax_audit_rows()
    bounds = nonuniversal_bound_rows()
    components = component_repack_rows()
    gates = promotion_gate_rows()
    formalization_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3353_0_local_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3353_1_local_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3353_2_web_sources_well_formed",
            "check": "all web source URLs are nonempty http links",
            "passed": all(row["url"].startswith("http") for row in web_source_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3353_3_outputs_parse",
            "check": "all 3353 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3353_4_syntax_audit_complete",
            "check": "syntax audit covers candidate args, forbidden decoupled block, projector alias, and boundary exception",
            "passed": {row["syntax_id"] for row in syntax}
            == {"SYN3353_0_candidate_action_args", "SYN3353_1_forbidden_decoupled_block", "SYN3353_2_source_projector", "SYN3353_3_boundary_exception"},
            "detail": "",
        },
        {
            "check_id": "VAL3353_5_alpha_smoke_bound_numeric",
            "check": "alpha_D P_D smoke bound is finite positive",
            "passed": any(
                row["bound_id"] == "AB3353_0_MICROSCOPE_density_projection_smoke"
                and math.isfinite(float(row["alphaD_PD_bound"]))
                and float(row["alphaD_PD_bound"]) > 0.0
                for row in bounds
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3353_6_alpha_smoke_bound_weak",
            "check": "alpha_D P_D smoke bound is explicitly weak, not a hidden pass",
            "passed": any(
                row["bound_id"] == "AB3353_0_MICROSCOPE_density_projection_smoke"
                and float(row["alphaD_PD_bound"]) > 1.0
                and row["valid_for_claim"] == "false"
                for row in bounds
            ),
            "detail": f"alpha_bound={alpha_smoke_bound():.6e}",
        },
        {
            "check_id": "VAL3353_7_component_routes_nonclaim",
            "check": "component repack has universal, nonuniversal smoke, and parent-zero routes all nonclaim",
            "passed": {row["component_id"] for row in components}
            == {"COMP3353_0_universal_density_branch", "COMP3353_1_nonuniversal_smoke_bound", "COMP3353_2_parent_zero_contract"}
            and all(row["valid_for_claim"] == "false" for row in components),
            "detail": "",
        },
        {
            "check_id": "VAL3353_8_no_overclaim",
            "check": "parent no-TD, physical nonuniversal bound, and local-GR gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3353_1_parent_no_TD_promoted", "GATE3353_3_nonuniversal_claim_bound", "GATE3353_4_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3353_9_next_target_alias_closure",
            "check": "next target attacks source-shadow/readout alias closure",
            "passed": any("aliases" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3353_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": formalization_changed == 0,
            "detail": f"formalization_changed_count={formalization_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3353_11_overall",
            "check": "3353 validation overall",
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
    write_csv(OUTPUTS["syntax"], syntax_audit_rows())
    write_csv(OUTPUTS["zero"], zero_certificate_rows())
    write_csv(OUTPUTS["bounds"], nonuniversal_bound_rows())
    write_csv(OUTPUTS["component"], component_repack_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()

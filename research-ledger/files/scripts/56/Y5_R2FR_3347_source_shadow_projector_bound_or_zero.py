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
DOC = ROOT / "3347-Y5-R2FR-source-shadow-projector-bound-or-zero-under-AX1090.md"

RUN_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = [
    ("SRC3347_0_3346_normal_form", OUT / "P8_Y5_R2FR_3346_PARENT_ACTION_NORMAL_FORM.csv", "3346 parent action normal form"),
    ("SRC3347_1_3346_forbidden_args", OUT / "P8_Y5_R2FR_3346_FORBIDDEN_ARGUMENT_INVENTORY.csv", "3346 forbidden source/projector arguments"),
    ("SRC3347_2_2617_identity", OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SINGLE_SOURCE_MAP_IDENTITY_THEOREM.csv", "single source-map identity theorem"),
    ("SRC3347_3_2617_shadow_zero", OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SOURCE_SHADOW_ZERO_ATTEMPT.csv", "source-shadow zero attempt"),
    ("SRC3347_4_2614_requirements", OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_PARENT_SIGNATURE_REQUIREMENTS.csv", "species/source prefactor parent clauses"),
    ("SRC3347_5_3339_measured_G", OUT / "P8_Y5_R2FR_3339_MEASURED_G_ABSORPTION_THEOREM.csv", "measured-G common-mode absorption theorem"),
    ("SRC3347_6_3342_wep_bounds", OUT / "P8_Y5_R2FR_3342_WEP_BOUND_ROWS.csv", "MICROSCOPE Ti/Pt WEP channel bound"),
    ("SRC3347_7_3342_eta_component", OUT / "P8_Y5_R2FR_3342_FRV3340_ETA_SPECIES_COMPONENT_ROW.csv", "eta_species finite component row"),
    ("SRC3347_8_3345_weight_collapse", OUT / "P8_Y5_R2FR_3345_SOURCE_WEIGHT_COLLAPSE_THEOREM.csv", "source weight collapse theorem"),
    ("SRC3347_9_2616_exchange_graph", OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv", "ordinary exchange graph theorem"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3347_SOURCE_REGISTER.csv",
    "normal_form": OUT / "P8_Y5_R2FR_3347_SOURCE_SHADOW_PROJECTOR_NORMAL_FORM.csv",
    "zero_attempt": OUT / "P8_Y5_R2FR_3347_ZERO_THEOREM_ATTEMPT.csv",
    "trichotomy": OUT / "P8_Y5_R2FR_3347_SHADOW_TRICHOTOMY_DECISION.csv",
    "newtonian": OUT / "P8_Y5_R2FR_3347_LOCAL_NEWTONIAN_PROJECTION.csv",
    "bounds": OUT / "P8_Y5_R2FR_3347_EPSILON_SOURCE_SHADOW_BOUND_ROWS.csv",
    "promotion": OUT / "P8_Y5_R2FR_3347_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3347_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3347_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3347_VALIDATION.csv",
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


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, role in SOURCES:
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


def load_eta_component() -> dict[str, str]:
    path = OUT / "P8_Y5_R2FR_3342_FRV3340_ETA_SPECIES_COMPONENT_ROW.csv"
    rows = read_csv(path)
    if not rows:
        raise RuntimeError("3342 eta_species component row is empty")
    return rows[0]


def source_shadow_normal_form_rows() -> list[dict[str, Any]]:
    return [
        {
            "form_id": "SSF3347_0_identity",
            "object": "identity source map",
            "mathematical_form": "T_active = T_H := (-2/sqrt(-g_obs)) delta(S_matter+S_EM)/delta g_obs",
            "interpretation": "the active local source is exactly the Hilbert/Noether source of the same action that defines ordinary dynamics",
            "effect_after_G_calibration": "ordinary Newtonian source normalization is one measured constant G_N",
            "status": "EXACT_CONDITIONAL_IF_PARENT_ARGS_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "form_id": "SSF3347_1_projector_decomposition",
            "object": "candidate source projector",
            "mathematical_form": "P_src = I + C_0 I + Pi_rel, so T_active=(1+C_0)T_H + Pi_rel(T_H)",
            "interpretation": "C_0 is a universal common mode; Pi_rel is the dangerous composition/source-shadow part",
            "effect_after_G_calibration": "C_0 is absorbed into measured G_N; Pi_rel survives as WEP/source-composition residual",
            "status": "DERIVED_LOCAL_DECOMPOSITION",
            "valid_for_claim": "false",
        },
        {
            "form_id": "SSF3347_2_epsilon_definition",
            "object": "epsilon_source_shadow",
            "mathematical_form": "epsilon_source_shadow := ||Pi_rel(T_H)||_arena / ||T_H||_arena",
            "interpretation": "finite residual measuring nonidentity source projector leakage after common-mode calibration",
            "effect_after_G_calibration": "bounded by differential acceleration/source-composition channels, not by a single Cavendish G value",
            "status": "BOUND_INTERFACE_DEFINED",
            "valid_for_claim": "false",
        },
    ]


def zero_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "Z3347_0_statement",
            "claim": "epsilon_source_shadow = 0",
            "derivation": "If Args(S_parent) admits only q-visible geometry, ordinary fields, public EM/current, fixed constants, and classified boundary terms, then no post-variation P_src or F_shadow is typed.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "blocker": "3346 normal form is a candidate inventory, not a parent-signed field-by-field syntax certificate",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "Z3347_1_variational_case",
            "claim": "a variational shadow is not hidden",
            "derivation": "If DeltaT_shadow = (-2/sqrt(-g)) delta(DeltaS)/delta g_obs, then DeltaS is a real parent action term and must be listed as matter, EM, geometry, or boundary/improvement content.",
            "proof_status": "DERIVED_RECLASSIFICATION",
            "blocker": "requires field-by-field parent action inventory to show no such DeltaS remains unlisted",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "Z3347_2_nonvariational_case",
            "claim": "a nonvariational shadow is rejected or bounded",
            "derivation": "Bianchi/Noether gives nabla_mu E^{mu nu}=0 and matter EOM give nabla_mu T_H^{mu nu}=0, so an inserted J_shadow must be conserved by itself; then it is boundary/improvement silence or a separately conserved residual block.",
            "proof_status": "DERIVED_FILTER",
            "blocker": "decoupled conserved blocks and boundary falloff are not fully arena-signed",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "Z3347_3_common_mode",
            "claim": "a universal source rescaling is not a local-GR residual",
            "derivation": "T_active=(1+C_0)T_H gives kappa_eff=kappa(1+C_0); Newtonian calibration measures G_N proportional to kappa_eff, so C_0 disappears from local differential/source-shape tests.",
            "proof_status": "DERIVED_ABSORPTION",
            "blocker": "only the relative projector Pi_rel is bounded here; global/cosmological calibration is a separate branch",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "Z3347_4_current_verdict",
            "claim": "current MTS source-shadow zero",
            "derivation": "The no-projector theorem is strong enough as a parent-action contract, but current files do not yet sign every no-shadow/no-boundary/no-decoupled-block clause.",
            "proof_status": "NOT_PROMOTED_TO_MTS_ZERO",
            "blocker": "carry epsilon_source_shadow as explicit finite residual until 3347/3347b clauses close",
            "valid_for_claim": "false",
        },
    ]


def trichotomy_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "TRI3347_0_identity",
            "candidate": "P_src = I + C_0 I",
            "classification": "identity plus measured-G common mode",
            "action": "absorb C_0 into G_N; no WEP/source-composition residual",
            "survives_as_residual": "false",
            "valid_for_claim": "false",
        },
        {
            "case_id": "TRI3347_1_variational",
            "candidate": "P_src(T_H)-T_H = delta DeltaS/delta g_obs",
            "classification": "real action content",
            "action": "move DeltaS into parent action inventory or forbid it by Args(S_parent)",
            "survives_as_residual": "true_until_parent_inventory_closes",
            "valid_for_claim": "false",
        },
        {
            "case_id": "TRI3347_2_boundary",
            "candidate": "J_shadow = nabla_alpha U^{alpha mu nu}",
            "classification": "boundary/improvement",
            "action": "zero under signed local falloff/no-flux condition, otherwise bound boundary contact residual",
            "survives_as_residual": "true_until_boundary_signed",
            "valid_for_claim": "false",
        },
        {
            "case_id": "TRI3347_3_nonvariational",
            "candidate": "J_shadow inserted into RHS without DeltaS",
            "classification": "Bianchi-inconsistent unless separately conserved",
            "action": "reject as parent field theory or classify as decoupled residual block",
            "survives_as_residual": "true_if_separately_conserved_block_exists",
            "valid_for_claim": "false",
        },
        {
            "case_id": "TRI3347_4_relative_projector",
            "candidate": "Pi_rel(T_H) labelled by material/species/source composition",
            "classification": "observable source-shadow leakage",
            "action": "bound epsilon_source_shadow using WEP/source-composition tests with no-cancellation guard",
            "survives_as_residual": "true_until_zero_or_bound_promoted",
            "valid_for_claim": "false",
        },
    ]


def local_newtonian_rows() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "NEW3347_0_field_equation",
            "weak_field_form": "nabla^2 Phi_N = 4 pi G_* [rho_H + rho_shadow]",
            "source_shadow_form": "rho_shadow = C_0 rho_H + Pi_rel(rho_H)",
            "after_calibration": "G_N = G_*(1+C_0) for a universal common mode",
            "observable_residual": "Pi_rel only",
            "status": "DERIVED_PROJECTION",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "NEW3347_1_eotvos_channel",
            "weak_field_form": "eta_AB ~= epsilon_source_shadow * R_AB for a differential material response R_AB",
            "source_shadow_form": "R_AB is the response of the test/source materials to Pi_rel",
            "after_calibration": "common Earth/source acceleration and common G_N cancel in eta_AB",
            "observable_residual": "|epsilon_source_shadow| <= |eta_AB|/|R_AB|",
            "status": "BOUND_FORMULA_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "NEW3347_2_no_cancellation",
            "weak_field_form": "epsilon_budget >= sum_i |epsilon_i R_i| unless parent theorem proves cancellations",
            "source_shadow_form": "absolute component accounting",
            "after_calibration": "do not hide opposite signs across material channels",
            "observable_residual": "conservative private bound rows",
            "status": "NO_CANCELLATION_GUARD",
            "valid_for_claim": "false",
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    eta_row = load_eta_component()
    eta_bound = float(eta_row["component_contribution"])
    response_factor = float(eta_row["response_factor"])
    epsilon_bound = eta_bound / response_factor
    return [
        {
            "bound_id": "BND3347_0_MICROSCOPE_TiPt_unit_response",
            "symbol": "epsilon_source_shadow",
            "observable": "eta_TiPt",
            "bound_formula": "|epsilon_source_shadow| <= |eta_TiPt| / |R_TiPt|",
            "response_factor": f"{response_factor:.6e}",
            "epsilon_bound": f"{epsilon_bound:.6e}",
            "units": "dimensionless_projector_fraction",
            "source_path": eta_row["source_path"],
            "source_url": eta_row["source_url"],
            "arena": eta_row["arena"],
            "extraction_method": "inherited from 3342 eta_species MICROSCOPE component row; unit response smoke only",
            "valid_for_component_bound": "true",
            "valid_for_claim": "false",
            "claim_blocker": "R_TiPt is not derived from MTS source-shadow basis; only one WEP material channel is staged",
        },
        {
            "bound_id": "BND3347_1_common_mode_absorbed",
            "symbol": "C_0",
            "observable": "measured_G_N",
            "bound_formula": "G_N = G_* (1+C_0)",
            "response_factor": "universal",
            "epsilon_bound": "absorbed_not_WEP_bound",
            "units": "dimensionless_common_mode",
            "source_path": str(OUT / "P8_Y5_R2FR_3339_MEASURED_G_ABSORPTION_THEOREM.csv"),
            "source_url": "local_corpus",
            "arena": "local_Newtonian_calibration",
            "extraction_method": "derived common-mode calibration identity",
            "valid_for_component_bound": "true",
            "valid_for_claim": "false",
            "claim_blocker": "common source normalization is not a local differential residual but may matter for global calibration branches",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3347_0_zero_theorem_shape",
            "claim": "source-shadow/projector zero theorem has an exact conditional proof",
            "passed": "true",
            "reason": "identity-source, variational reclassification, Bianchi filter, and common-mode absorption are explicit",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3347_1_parent_signed_zero",
            "claim": "epsilon_source_shadow=0 is parent-signed for current MTS",
            "passed": "false",
            "reason": "3346 normal form is not a closed field-by-field parent action certificate",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3347_2_finite_bound_staged",
            "claim": "finite epsilon_source_shadow component bound is staged",
            "passed": "true",
            "reason": "MICROSCOPE Ti/Pt unit-response smoke row gives a dimensionless nonclaim component bound",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3347_3_local_GR_claim",
            "claim": "local GR/Newton calibrated source-coupling branch is claim-ready",
            "passed": "false",
            "reason": "source-shadow zero is not parent-signed and material response basis is not derived",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3347_0",
            "question": "Did 3347 prove away source projectors for current MTS?",
            "answer": "no",
            "reason": "the theorem is exact as a parent-action contract, but current MTS has not signed the no-projector/no-boundary/no-decoupled-block clauses",
            "next_action": "derive the material/source response basis R_AB or close the parent inventory clauses directly",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3347_1",
            "question": "Did 3347 move the source-coupling problem forward?",
            "answer": "yes",
            "reason": "it reduces source-shadow freedom to identity/common-mode, variational parent content, boundary/improvement, decoupled block, or a bounded relative projector",
            "next_action": "attack R_AB/material charge basis before adding more empirical channels",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3348-Y5-R2FR-source-shadow-response-basis-or-zero-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3348_source_shadow_response_basis_or_zero.py",
            "objective": "derive the material/source response basis R_AB for epsilon_source_shadow from Hilbert/Noether matter content, or prove R_AB has no independent ordinary slot",
            "why_next": "the finite WEP bound exists but cannot become a serious local-GR bound until R_AB is derived rather than set to unit smoke response",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3347b-Y5-R2FR-coefficient-domain-field-by-field-certificate.md",
            "target_script": "scripts/Y5_R2FR_3347b_coefficient_domain_field_by_field_certificate.py",
            "objective": "parallel route: field-by-field certificate for epsilon_coeff_domain and hidden coefficients",
            "why_next": "prevents hidden coefficient maps from recreating the source-shadow response through clocks, charges, masses, or frames",
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
            "# 3347 — Source-Shadow Projector Bound Or Zero Under AX1090",
            f"Generated: `{RUN_UTC}`",
            "## Summary\n"
            "- This checkpoint attacks the source-shadow/projector gap directly, not merely by naming it.\n"
            "- The clean theorem is: if the parent action admits no post-variation source map, then `T_active=T_H`; any universal common mode is absorbed into measured `G_N`.\n"
            "- Any nonidentity source map is forced into a trichotomy: real variational action content, boundary/improvement silence, separately conserved residual block, or observable relative projector.\n"
            "- Current MTS still cannot claim `epsilon_source_shadow=0`, but it now has a finite nonclaim MICROSCOPE Ti/Pt smoke bound and a precise next derivation target: the material response basis `R_AB`.",
            "## Source-Shadow Normal Form\n" + markdown_table(source_shadow_normal_form_rows()),
            "## Zero Theorem Attempt\n" + markdown_table(zero_theorem_rows()),
            "## Shadow Trichotomy Decision\n" + markdown_table(trichotomy_rows()),
            "## Local Newtonian Projection\n" + markdown_table(local_newtonian_rows()),
            "## Epsilon Source-Shadow Bound Rows\n" + markdown_table(bound_rows()),
            "## Promotion Gates\n" + markdown_table(promotion_gate_rows()),
            "## Decision Ledger\n" + markdown_table(decision_rows()),
            "## Next Target\n" + markdown_table(next_target_rows()),
        ]
    ) + "\n"


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = source_rows()
    zero_rows = zero_theorem_rows()
    tri_rows = trichotomy_rows()
    bounds = bound_rows()
    gates = promotion_gate_rows()
    formalization_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3347_0_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3347_1_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3347_2_outputs_parse",
            "check": "all 3347 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3347_3_zero_attempt_has_proof_filter",
            "check": "zero attempt includes conditional theorem, variational reclassification, Bianchi filter, and current nonpromotion",
            "passed": {row["theorem_id"] for row in zero_rows}
            == {"Z3347_0_statement", "Z3347_1_variational_case", "Z3347_2_nonvariational_case", "Z3347_3_common_mode", "Z3347_4_current_verdict"},
            "detail": "",
        },
        {
            "check_id": "VAL3347_4_trichotomy_complete",
            "check": "trichotomy covers identity/common, variational, boundary, nonvariational, and relative projector cases",
            "passed": {row["case_id"] for row in tri_rows}
            == {"TRI3347_0_identity", "TRI3347_1_variational", "TRI3347_2_boundary", "TRI3347_3_nonvariational", "TRI3347_4_relative_projector"},
            "detail": "",
        },
        {
            "check_id": "VAL3347_5_bound_numeric_positive",
            "check": "epsilon_source_shadow component bound is positive finite numeric",
            "passed": any(
                row["symbol"] == "epsilon_source_shadow"
                and math.isfinite(float(row["epsilon_bound"]))
                and float(row["epsilon_bound"]) > 0.0
                for row in bounds
                if row["bound_id"] == "BND3347_0_MICROSCOPE_TiPt_unit_response"
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3347_6_bound_nonclaim",
            "check": "bound rows remain nonclaim and source-backed",
            "passed": all(row["valid_for_claim"] == "false" and Path(row["source_path"]).exists() for row in bounds),
            "detail": "",
        },
        {
            "check_id": "VAL3347_7_no_missing_markers",
            "check": "new bound rows contain no MISSING markers",
            "passed": all("MISSING_" not in "|".join(str(value) for value in row.values()) for row in bounds),
            "detail": "",
        },
        {
            "check_id": "VAL3347_8_no_overclaim",
            "check": "source-shadow zero and local-GR gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3347_1_parent_signed_zero", "GATE3347_3_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3347_9_next_target_response_basis",
            "check": "next target attacks material/source response basis",
            "passed": any("R_AB" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3347_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": formalization_changed == 0,
            "detail": f"formalization_changed_count={formalization_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3347_11_overall",
            "check": "3347 validation overall",
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
    write_csv(OUTPUTS["sources"], source_rows())
    write_csv(OUTPUTS["normal_form"], source_shadow_normal_form_rows())
    write_csv(OUTPUTS["zero_attempt"], zero_theorem_rows())
    write_csv(OUTPUTS["trichotomy"], trichotomy_rows())
    write_csv(OUTPUTS["newtonian"], local_newtonian_rows())
    write_csv(OUTPUTS["bounds"], bound_rows())
    write_csv(OUTPUTS["promotion"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()

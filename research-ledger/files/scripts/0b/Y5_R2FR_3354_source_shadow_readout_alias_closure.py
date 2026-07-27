from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3354-Y5-R2FR-source-shadow-readout-alias-closure-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

LOCAL_SOURCES = [
    ("LSRC3354_0_3353_doc", ROOT / "3353-Y5-R2FR-parent-no-TD-syntax-or-nonuniversal-bound-under-AX1090.md", "3353 handoff: no T_D syntax was candidate-only because aliases remained open"),
    ("LSRC3354_1_3353_next", OUT / "P8_Y5_R2FR_3353_NEXT_TARGET.csv", "3353 next target naming source-shadow/readout alias closure"),
    ("LSRC3354_2_3353_zero", OUT / "P8_Y5_R2FR_3353_NO_TD_ZERO_CERTIFICATE_ATTEMPT.csv", "3353 no-TD zero certificate attempt"),
    ("LSRC3354_3_3353_gates", OUT / "P8_Y5_R2FR_3353_PROMOTION_GATES.csv", "3353 promotion gates"),
    ("LSRC3354_4_3346_allowed", OUT / "P8_Y5_R2FR_3346_ALLOWED_ARGUMENT_INVENTORY.csv", "3346 allowed parent action arguments"),
    ("LSRC3354_5_3346_forbidden", OUT / "P8_Y5_R2FR_3346_FORBIDDEN_ARGUMENT_INVENTORY.csv", "3346 forbidden parent action arguments"),
    ("LSRC3354_6_3346_closure", OUT / "P8_Y5_R2FR_3346_CLOSURE_CERTIFICATE_ATTEMPT.csv", "3346 closure certificate status"),
    ("LSRC3354_7_3350_residuals", OUT / "P8_Y5_R2FR_3350_EXPLICIT_RESIDUAL_ROWS.csv", "3350 explicit local residual rows"),
    ("LSRC3354_8_3352_fork", OUT / "P8_Y5_R2FR_3352_COUPLING_PROJECTION_FORK.csv", "3352 decoupled coupling fork"),
    ("LSRC3354_9_3353_alpha", OUT / "P8_Y5_R2FR_3353_NONUNIVERSAL_ALPHA_BOUND_ROWS.csv", "3353 alpha_D P_D smoke/zero rows"),
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3354_LOCAL_SOURCE_REGISTER.csv",
    "alias_inventory": OUT / "P8_Y5_R2FR_3354_ALIAS_FAMILY_INVENTORY.csv",
    "lemma_steps": OUT / "P8_Y5_R2FR_3354_ALIAS_ZERO_LEMMA_STEPS.csv",
    "residual_update": OUT / "P8_Y5_R2FR_3354_RESIDUAL_ROUTE_UPDATE.csv",
    "branch_reduction": OUT / "P8_Y5_R2FR_3354_BRANCH_REDUCTION_LEDGER.csv",
    "gates": OUT / "P8_Y5_R2FR_3354_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3354_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3354_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3354_VALIDATION.csv",
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
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parseable(path: Path) -> bool:
    try:
        if path.suffix.lower() == ".csv":
            read_csv(path)
        else:
            path.read_text(encoding="utf-8")
        return True
    except Exception:
        return False


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot_tree(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    files: dict[str, str] = {}
    for file_path in sorted(path.rglob("*")):
        if file_path.is_file():
            files[str(file_path.relative_to(path))] = hash_file(file_path)
    return files


def table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(compact(row.get(key, ""), 260).replace("|", "\\|") for key in headers) + " |")
    return "\n".join(lines) + "\n"


def local_source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, usage in LOCAL_SOURCES:
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parseable": bool_str(path.exists() and parseable(path)),
                "usage": usage,
                "valid_for_claim": "false",
            }
        )
    return rows


def alias_inventory_rows() -> list[dict[str, Any]]:
    return [
        {
            "alias_id": "ALIAS3354_0_source_weight_shadow",
            "alias_family": "source-shadow/source-weight",
            "how_TD_PD_returns": "post-variation source weight w_A(X), kappa_A(I_hid), F_shadow(T_D,labels), or P_material(T_H)",
            "forbidden_or_allowed_clause": "ARG3346_F1_source_weight; ARG3346_F2_source_projector",
            "closure_condition": "single Hilbert source owner and no independent source-map argument in Args(S_parent)",
            "lemma_effect": "T_eff = -2/sqrt(g) delta S_ord/delta g_obs; no separate T_D/P_D slot can contribute",
            "current_result": "CONDITIONAL_ZERO_IF_PARENT_DOMAIN_SIGNED",
            "residual_if_not_closed": "epsilon_source_shadow",
            "closed_if_parent_signed": "true",
            "valid_for_claim": "false",
        },
        {
            "alias_id": "ALIAS3354_1_hidden_frame",
            "alias_family": "hidden-frame/disformal matter geometry",
            "how_TD_PD_returns": "g_A = C_A(I_hid)^2 g_obs or labelled disformal frame makes ordinary matter see hidden variables",
            "forbidden_or_allowed_clause": "ARG3346_A1_q_visible_geometry; ARG3346_F3_hidden_frame",
            "closure_condition": "ordinary matter and EM couple only to e_obs(q(Phi)), g_obs(q(Phi)), and fixed representation data",
            "lemma_effect": "for v_D in ker(Dq), delta_v g_obs = delta_v e_obs = 0, so delta_v S_matter = 0",
            "current_result": "CONDITIONAL_ZERO_IF_OBSERVED_GEOMETRY_DESCENT_SIGNED",
            "residual_if_not_closed": "c_g; b_dis; PPN/WEP/clock residuals",
            "closed_if_parent_signed": "true",
            "valid_for_claim": "false",
        },
        {
            "alias_id": "ALIAS3354_2_reduced_readout",
            "alias_family": "readout/projector backreaction",
            "how_TD_PD_returns": "P_read, R_read, fitted masks, or reduced-EFT projection inserted before variation",
            "forbidden_or_allowed_clause": "ARG3346_F4_readout_argument; CLOSE3346_2_readout",
            "closure_condition": "readout is post-solution bookkeeping, not a varied parent-action argument",
            "lemma_effect": "readout can change reported observables but not the parent Hilbert source or local field equation",
            "current_result": "CONDITIONAL_DEMOTION_TO_S_RED_IF_PARENT_EXCLUSION_SIGNED",
            "residual_if_not_closed": "epsilon_readout_backreaction; epsilon_readout_source_shadow",
            "closed_if_parent_signed": "true",
            "valid_for_claim": "false",
        },
        {
            "alias_id": "ALIAS3354_3_boundary_contact",
            "alias_family": "boundary/improvement/contact",
            "how_TD_PD_returns": "surface term, contact term, or improvement current supplies an effective local source",
            "forbidden_or_allowed_clause": "ARG3346_A5_boundary_terms; CLOSE3346_3_boundary_inventory",
            "closure_condition": "boundary term is exact, zero-flux, or independently carried as a finite residual with source-backed bound",
            "lemma_effect": "bulk local source is unchanged only after zero-flux/contact silence is signed",
            "current_result": "NOT_CLOSED",
            "residual_if_not_closed": "epsilon_boundary_contact",
            "closed_if_parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "alias_id": "ALIAS3354_4_decoupled_block_name",
            "alias_family": "renamed decoupled source block",
            "how_TD_PD_returns": "unlisted T_D/S_D/P_D reappears as an arena source, hidden reservoir, or labelled projector",
            "forbidden_or_allowed_clause": "ARG3346_F5_uninventoried_decoupled_block; ZERO3353_1_alias_closure",
            "closure_condition": "field-by-field parent domain excludes T_D/S_D/P_D and all aliases, or inventories and bounds them",
            "lemma_effect": "if absent from Args(S_parent), g_D P_D = 0; otherwise branch stays explicit residual",
            "current_result": "CONDITIONAL_ZERO_BUT_NOT_PROMOTED",
            "residual_if_not_closed": "epsilon_decoupled_field; alpha_D P_D",
            "closed_if_parent_signed": "true",
            "valid_for_claim": "false",
        },
    ]


def lemma_step_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma_id": "LEM3354_0_vertical_descent",
            "statement": "If v_D is vertical, Dq(v_D)=0, and S_parent depends on hidden variables only through q(Phi), then delta_vD S_bulk = 0.",
            "derivation": "delta_v S_bar[q(Phi)] = <delta S_bar/dq, Dq(v_D)> = 0",
            "kills_aliases": "hidden-frame when geometry descends; renamed decoupled block if no direct slot exists",
            "status": "EXACT_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "LEM3354_1_single_source_owner",
            "statement": "If ordinary matter/EM are varied before source labels are exposed, the local source is the Hilbert stress of that same action.",
            "derivation": "T_H^{mu nu} = -2/sqrt(|g|) delta S_ord/delta g_{mu nu}; adding F_shadow requires an extra action argument.",
            "kills_aliases": "source-shadow/source-weight/projector maps",
            "status": "EXACT_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "LEM3354_2_readout_after_variation",
            "statement": "If R_read is applied after solving the parent equations, it cannot add a parent Euler-Lagrange source term.",
            "derivation": "delta S_parent is computed before the map O -> R_read(O); pre-variation insertion is a separate reduced action S_red.",
            "kills_aliases": "readout/projector backreaction in parent local GR branch",
            "status": "EXACT_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "LEM3354_3_boundary_silence",
            "statement": "Boundary/improvement terms do not affect the bulk local source only if their variation is exact/zero-flux or the contact term is bounded.",
            "derivation": "delta S_boundary gives surface/contact contributions; these vanish locally only under a boundary condition or an explicit residual bound.",
            "kills_aliases": "boundary/contact route only after separate proof",
            "status": "OPEN_NOT_CLOSED",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "LEM3354_4_alias_closure_composite",
            "statement": "The no-TD theorem promotes only if LEM3354_0, LEM3354_1, LEM3354_2, and LEM3354_3 all close inside the same parent action domain.",
            "derivation": "no T_D/P_D slot + no source projector + no hidden frame + no pre-variation readout + no contact leakage => g_D P_D = 0",
            "kills_aliases": "full source-shadow/readout/hidden-frame/boundary alias closure",
            "status": "NOT_PROMOTED_BECAUSE_BOUNDARY_AND_PARENT_SIGNATURE_REMAIN_OPEN",
            "valid_for_claim": "false",
        },
    ]


def residual_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RES3354_0_epsilon_source_shadow",
            "symbol": "epsilon_source_shadow",
            "previous_status": "open source-shadow/projector branch",
            "3354_update": "conditional zero if ARG3346_F1 and ARG3346_F2 are signed absent from Args(S_parent)",
            "remaining_gap": "parent action domain is not field-by-field signed",
            "component_status": "CONDITIONAL_ZERO_NOT_PROMOTED",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3354_1_epsilon_readout_source_shadow",
            "symbol": "epsilon_readout_source_shadow",
            "previous_status": "apparent source from readout/projector operation",
            "3354_update": "demoted to S_red/readout artifact if ARG3346_F4 exclusion is signed",
            "remaining_gap": "readout exclusion not yet parent-owned for every reduced branch",
            "component_status": "CONDITIONAL_DEMOTION_NOT_PROMOTED",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3354_2_hidden_frame_residuals",
            "symbol": "c_g; b_dis; PPN/WEP/clock residuals",
            "previous_status": "hidden geometry/disformal branch",
            "3354_update": "conditional zero if ordinary matter geometry is only e_obs(q(Phi)) and g_obs(q(Phi))",
            "remaining_gap": "observed-geometry descent still uses the 3346 contract, not a signed parent action",
            "component_status": "CONDITIONAL_ZERO_NOT_PROMOTED",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3354_3_epsilon_boundary_contact",
            "symbol": "epsilon_boundary_contact",
            "previous_status": "boundary/contact source term not included in ordinary bulk Hilbert material stress",
            "3354_update": "unchanged live route; must be zero-flux/exact or bounded next",
            "remaining_gap": "no boundary condition or contact amplitude bound yet",
            "component_status": "OPEN_PRIMARY_NEXT_TARGET",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3354_4_alphaD_PD",
            "symbol": "alpha_D P_D",
            "previous_status": "finite but weak MICROSCOPE/density smoke bound",
            "3354_update": "preferred route remains syntactic zero by alias exclusion, not empirical fitting",
            "remaining_gap": "source-shadow/readout/hidden-frame aliases conditionally routed; boundary/contact remains open",
            "component_status": "NONCLAIM_SMOKE_PLUS_PARENT_ZERO_CONTRACT",
            "valid_for_claim": "false",
        },
    ]


def branch_reduction_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "BR3354_0_before",
            "description": "Before 3354, no-TD syntax could be evaded by source-shadow, hidden-frame, readout/projector, boundary/contact, or renamed decoupled blocks.",
            "open_alias_count": 5,
            "conditionally_closed_count": 0,
            "still_open_count": 5,
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BR3354_1_after_conditional_parent_contract",
            "description": "Under the 3346 parent-domain contract, source-shadow, hidden-frame, readout, and renamed decoupled-block aliases reduce to syntactic absence/vertical descent.",
            "open_alias_count": 5,
            "conditionally_closed_count": 4,
            "still_open_count": 1,
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BR3354_2_after_claim_rules",
            "description": "For actual claim logic, conditional closures do not promote until the parent action and boundary/contact route are signed.",
            "open_alias_count": 5,
            "conditionally_closed_count": 4,
            "still_open_count": 2,
            "still_open_names": "parent-domain signature; boundary/contact zero-flux or bound",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3354_0_source_shadow_conditional_closed",
            "claim": "source-shadow/source-weight cannot return if parent has single Hilbert source owner and no source projector argument",
            "passed": "true",
            "reason": "ARG3346_F1/F2 provide the exact syntax exclusion route; LEM3354_1 identifies the variational owner",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3354_1_hidden_frame_conditional_closed",
            "claim": "hidden-frame/disformal aliases cannot return if matter geometry descends through q",
            "passed": "true",
            "reason": "vertical variations in ker(Dq) leave e_obs(q(Phi)) and g_obs(q(Phi)) unchanged",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3354_2_readout_conditional_demoted",
            "claim": "readout/projector aliases are demoted to post-solution S_red if excluded from parent variation",
            "passed": "true",
            "reason": "pre-variation readout is a different reduced action, not the parent local GR theorem",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3354_3_boundary_contact_closed",
            "claim": "boundary/contact aliases are exact, zero-flux, or source-backed bounded",
            "passed": "false",
            "reason": "3354 isolates this as the live route but does not prove zero flux or a contact bound",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3354_4_parent_alias_closure_promoted",
            "claim": "the full parent action is signed against all T_D/P_D aliases",
            "passed": "false",
            "reason": "3346 closure certificate remains NOT_CLOSED and boundary/contact remains open",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3354_5_local_GR_claim",
            "claim": "local GR/Newton source-coupling branch is claim-ready",
            "passed": "false",
            "reason": "conditional alias reductions are useful, but parent-domain and boundary/contact proof are still required",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3354_0",
            "question": "Did 3354 close source-shadow/readout aliases enough to move forward?",
            "answer": "yes conditionally, not claim-ready",
            "reason": "source-shadow, hidden-frame, readout, and renamed decoupled-block routes now have explicit zero/demotion lemmas tied to parent syntax",
            "next_action": "attack boundary/contact zero-flux or contact bound, then return to parent-domain signature",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3354_1",
            "question": "Should we fit alpha_D P_D empirically next?",
            "answer": "not as the best route",
            "reason": "3353 bound is finite but huge; the cleaner path is to derive alpha_D P_D = 0 from parent syntax and alias closure",
            "next_action": "prove epsilon_boundary_contact = 0 or stage a real finite contact bound",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3355-Y5-R2FR-boundary-contact-zero-flux-or-contact-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3355_boundary_contact_zero_flux_or_contact_bound.py",
            "objective": "prove boundary/contact terms are exact or zero-flux in the local ordinary arena, or produce a finite source-backed epsilon_boundary_contact bound",
            "why_next": "3354 reduces the alias problem to parent-domain signature plus the boundary/contact escape hatch",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3356-Y5-R2FR-parent-domain-signature-collapse-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3356_parent_domain_signature_collapse.py",
            "objective": "after boundary/contact cleanup, collapse 3346 conditional contracts into one parent-domain signature certificate",
            "why_next": "conditional zeros only promote after the parent action domain is signed field-by-field",
            "valid_for_claim": "false",
        },
    ]


def render_doc() -> str:
    parts = [
        "# 3354 — Source-Shadow / Readout Alias Closure Under AX1090",
        "",
        f"Generated: `{RUN_UTC}`",
        "",
        "## Summary",
        "- This checkpoint does the thing 3353 asked for: it tries to stop `T_D/P_D` returning under alias names.",
        "- The useful result is real but conditional: source-shadow, hidden-frame, readout, and renamed decoupled-block routes reduce to zero/demotion lemmas if the 3346 parent-domain contract is signed.",
        "- The not-yet-killed route is boundary/contact leakage. That becomes the next concrete target rather than a vague missing-input fog.",
        "- No local-GR/Newton claim is promoted here; this is a narrowing theorem gate.",
        "",
        "## Local Source Register",
        table(local_source_rows()),
        "## Alias Family Inventory",
        table(alias_inventory_rows()),
        "## Alias Zero Lemma Steps",
        table(lemma_step_rows()),
        "## Residual Route Update",
        table(residual_update_rows()),
        "## Branch Reduction Ledger",
        table(branch_reduction_rows()),
        "## Promotion Gates",
        table(promotion_gate_rows()),
        "## Decision Ledger",
        table(decision_rows()),
        "## Next Target",
        table(next_target_rows()),
    ]
    return "\n".join(parts)


def validate_outputs(formalization_before: dict[str, str]) -> list[dict[str, Any]]:
    local_sources = local_source_rows()
    aliases = alias_inventory_rows()
    lemmas = lemma_step_rows()
    residuals = residual_update_rows()
    branches = branch_reduction_rows()
    gates = promotion_gate_rows()
    outputs_to_parse = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_after = snapshot_tree(FW)
    formalization_changed = sum(
        1
        for key in set(formalization_before) | set(formalization_after)
        if formalization_before.get(key) != formalization_after.get(key)
    )
    checks: list[dict[str, Any]] = [
        {
            "check_id": "VAL3354_0_local_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3354_1_local_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parseable"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3354_2_outputs_parse",
            "check": "all 3354 non-validation outputs parse",
            "passed": all(path.exists() and parseable(path) for path in outputs_to_parse),
            "detail": "",
        },
        {
            "check_id": "VAL3354_3_alias_inventory_complete",
            "check": "alias inventory covers source-shadow, hidden-frame, readout, boundary/contact, and decoupled-block routes",
            "passed": {row["alias_id"] for row in aliases}
            == {
                "ALIAS3354_0_source_weight_shadow",
                "ALIAS3354_1_hidden_frame",
                "ALIAS3354_2_reduced_readout",
                "ALIAS3354_3_boundary_contact",
                "ALIAS3354_4_decoupled_block_name",
            },
            "detail": "",
        },
        {
            "check_id": "VAL3354_4_lemma_has_actual_zero_mechanism",
            "check": "lemma rows contain variational vertical-descent and single-source-owner mechanisms",
            "passed": any(row["lemma_id"] == "LEM3354_0_vertical_descent" and "Dq(v_D)=0" in row["statement"] for row in lemmas)
            and any(row["lemma_id"] == "LEM3354_1_single_source_owner" for row in lemmas),
            "detail": "",
        },
        {
            "check_id": "VAL3354_5_boundary_remains_open",
            "check": "boundary/contact branch is isolated but not falsely closed",
            "passed": any(row["alias_id"] == "ALIAS3354_3_boundary_contact" and row["current_result"] == "NOT_CLOSED" for row in aliases)
            and any(row["gate_id"] == "GATE3354_3_boundary_contact_closed" and row["passed"] == "false" for row in gates),
            "detail": "",
        },
        {
            "check_id": "VAL3354_6_conditional_closures_nonclaim",
            "check": "all conditional alias closures remain nonclaim",
            "passed": all(row["valid_for_claim"] == "false" for row in aliases + lemmas + residuals + branches + gates),
            "detail": "",
        },
        {
            "check_id": "VAL3354_7_no_local_GR_overclaim",
            "check": "local GR/Newton claim remains false",
            "passed": any(row["gate_id"] == "GATE3354_5_local_GR_claim" and row["passed"] == "false" for row in gates),
            "detail": "",
        },
        {
            "check_id": "VAL3354_8_next_target_boundary",
            "check": "next target explicitly attacks boundary/contact",
            "passed": any("boundary/contact" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3354_9_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": formalization_changed == 0,
            "detail": f"formalization_changed_count={formalization_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3354_10_overall",
            "check": "3354 validation overall",
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
    write_csv(OUTPUTS["alias_inventory"], alias_inventory_rows())
    write_csv(OUTPUTS["lemma_steps"], lemma_step_rows())
    write_csv(OUTPUTS["residual_update"], residual_update_rows())
    write_csv(OUTPUTS["branch_reduction"], branch_reduction_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()

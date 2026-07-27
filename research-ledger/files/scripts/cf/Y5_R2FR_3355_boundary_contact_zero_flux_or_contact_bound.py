from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3355-Y5-R2FR-boundary-contact-zero-flux-or-contact-bound-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

LOCAL_SOURCES = [
    ("LSRC3355_0_3354_doc", ROOT / "3354-Y5-R2FR-source-shadow-readout-alias-closure-under-AX1090.md", "3354 isolates boundary/contact as live alias route"),
    ("LSRC3355_1_3354_next", OUT / "P8_Y5_R2FR_3354_NEXT_TARGET.csv", "3354 next target"),
    ("LSRC3355_2_3354_alias", OUT / "P8_Y5_R2FR_3354_ALIAS_FAMILY_INVENTORY.csv", "boundary/contact alias row"),
    ("LSRC3355_3_3354_residual", OUT / "P8_Y5_R2FR_3354_RESIDUAL_ROUTE_UPDATE.csv", "epsilon_boundary_contact residual update"),
    ("LSRC3355_4_3350_residuals", OUT / "P8_Y5_R2FR_3350_EXPLICIT_RESIDUAL_ROWS.csv", "original explicit residual row"),
    ("LSRC3355_5_boundary_noflux", OUT / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "prior boundary alpha3 no-flux theorem attempt"),
    ("LSRC3355_6_boundary_premises", OUT / "P8_BOUNDARY_ALPHA3_PREMISE_OWNERSHIP.csv", "premise ownership audit for boundary no-flux"),
    ("LSRC3355_7_boundary_scalar_owner", OUT / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv", "scalar boundary owner attempt"),
    ("LSRC3355_8_boundary_status", OUT / "P8_BOUNDARY_ALPHA3_CLOSURE_STATUS.csv", "boundary alpha3 closure status"),
    ("LSRC3355_9_alpha3_gate", OUT / "P8_ALPHA3_THEOREM_ZERO_GATE.csv", "alpha3 theorem-zero gate"),
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3355_LOCAL_SOURCE_REGISTER.csv",
    "decomposition": OUT / "P8_Y5_R2FR_3355_BOUNDARY_CONTACT_DECOMPOSITION.csv",
    "zero_lemmas": OUT / "P8_Y5_R2FR_3355_ZERO_FLUX_LEMMA_ROWS.csv",
    "epsilon_split": OUT / "P8_Y5_R2FR_3355_EPSILON_BOUNDARY_CONTACT_SPLIT.csv",
    "contact_bound": OUT / "P8_Y5_R2FR_3355_CONTACT_BOUND_TEMPLATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3355_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3355_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3355_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3355_VALIDATION.csv",
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


def decomposition_rows() -> list[dict[str, Any]]:
    return [
        {
            "piece_id": "BC3355_0_bulk_variational_boundary",
            "piece": "ordinary bulk variation with compact support inside the local arena",
            "mathematical_form": "delta S_B = integral_boundary Pi_B delta phi; if supp(delta phi) cap boundary = empty, delta S_B = 0",
            "source_effect": "no local Euler-Lagrange source contribution in the bulk",
            "status": "EXACT_ZERO_FOR_LOCAL_COMPACT_SUPPORT_VARIATIONS",
            "surviving_hazard": "does not cover contact/interface support or nonlocal readout boundaries",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "BC3355_1_scalar_stationary_boundary",
            "piece": "homogeneous scalar stationary boundary collar",
            "mathematical_form": "S_B = integral_boundary sqrt(|gamma|) F(scalar invariants), tau_AB proportional to gamma_AB",
            "source_effect": "no tangential vector, shear, or preferred-frame alpha3 projection",
            "status": "CONDITIONAL_ZERO_FROM_EXISTING_BOUNDARY_ALPHA3_WORK",
            "surviving_hazard": "premises O0-O6 are not parent-owned",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "BC3355_2_constant_monopole",
            "piece": "conserved universal boundary monopole",
            "mathematical_form": "mu_B = constant, partial_t mu_B = partial_r mu_B = partial_frame mu_B = 0",
            "source_effect": "renormalizes measured GM but does not create a local vector force",
            "status": "CONDITIONAL_CALIBRATION_ONLY",
            "surviving_hazard": "derivative silence for beta/xi/Gdot rows not parent-derived",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "BC3355_3_contact_interface",
            "piece": "boundary intersects material support or carries marker/vector/normal-flux data",
            "mathematical_form": "delta S_contact / delta g_{mu nu} contributes a distributional T_contact^{mu nu}",
            "source_effect": "can source epsilon_boundary_contact and PPN/WEP/orbital residuals",
            "status": "OPEN_REDUCED_SURVIVOR",
            "surviving_hazard": "needs a collar-separation theorem or a numeric contact amplitude bound",
            "valid_for_claim": "false",
        },
    ]


def zero_lemma_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma_id": "ZFL3355_0_compact_support_bulk_zero",
            "claim": "Boundary variations do not enter local bulk equations for compact-support test variations.",
            "derivation": "The first variation separates into bulk plus boundary terms; choosing variations supported inside the local ordinary arena kills the boundary integral exactly.",
            "premises_needed": "local arena has an interior collar and the tested equation is a bulk Euler-Lagrange equation",
            "result": "PASS_AS_LOCAL_MATH_LEMMA",
            "claim_ceiling": "does not prove global/boundary/contact silence",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "ZFL3355_1_trace_tangential_no_normal_flux",
            "claim": "Pure tangential trace stress has no normal projected momentum flux.",
            "derivation": "n_mu gamma_tangent^{mu nu}=0, so n_mu P_loc_nu tau gamma_tangent^{mu nu}=0.",
            "premises_needed": "boundary stress is pure tangential trace and all normal exchange is separately zero",
            "result": "PASS_IF_SCALAR_STATIONARY_BOUNDARY_PREMISES_HELD",
            "claim_ceiling": "premises not parent-owned",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "ZFL3355_2_no_vector_channel",
            "claim": "Scalar homogeneous boundary data cannot source preferred-frame/vector residuals.",
            "derivation": "SO(3) scalar singlet has no surviving vector representation; alpha3-type vector projection is zero.",
            "premises_needed": "no tangent marker, spin direction, domain velocity, hidden frame, or vector boundary field",
            "result": "PASS_IF_NO_MARKER_FIELD_PREMISE_HELD",
            "claim_ceiling": "marker exclusion not parent-owned",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "ZFL3355_3_contact_survivor",
            "claim": "A genuine contact/interface term is not killed by compact-support or scalar no-flux arguments if support overlaps the local source.",
            "derivation": "A distributional T_contact in the same support as ordinary matter contributes to the Hilbert source unless its coefficient is zero or bounded.",
            "premises_needed": "none; this is the retained counter-branch",
            "result": "OPEN",
            "claim_ceiling": "must prove collar separation or bound contact amplitude",
            "valid_for_claim": "false",
        },
    ]


def epsilon_split_rows() -> list[dict[str, Any]]:
    return [
        {
            "split_id": "EPSB3355_0_bulk_boundary",
            "symbol": "epsilon_boundary_bulk",
            "definition": "bulk local source contribution from an exterior boundary term",
            "value_or_bound": "0_under_compact_support_local_variation",
            "status": "EXACT_LOCAL_LEMMA_NOT_GLOBAL_CLAIM",
            "valid_for_component_bound": "true",
            "valid_for_claim": "false",
        },
        {
            "split_id": "EPSB3355_1_vector_flux",
            "symbol": "epsilon_boundary_vector_flux",
            "definition": "preferred-frame/vector flux from scalar stationary boundary collar",
            "value_or_bound": "0_if_scalar_stationary_marker_free_no_flux_premises_parent_owned",
            "status": "CONDITIONAL_ZERO_NOT_PARENT_OWNED",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "split_id": "EPSB3355_2_monopole_calibration",
            "symbol": "epsilon_boundary_monopole",
            "definition": "constant universal boundary monopole in measured GM",
            "value_or_bound": "absorbed_into_GM_if_constant_universal",
            "status": "CONDITIONAL_CALIBRATION_ROUTE",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "split_id": "EPSB3355_3_contact",
            "symbol": "epsilon_boundary_contact",
            "definition": "distributional contact/interface source in the local material support",
            "value_or_bound": "MISSING_CONTACT_COEFFICIENT_OR_COLLAR_SEPARATION_ZERO",
            "status": "OPEN_PRIMARY_SURVIVOR",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
    ]


def contact_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "CB3355_0_contact_norm_template",
            "quantity": "abs(epsilon_boundary_contact)",
            "formula": "||T_contact||_local / ||T_H^ordinary||",
            "needed_inputs": "contact support measure, contact stress amplitude, ordinary Hilbert source normalization, local collar geometry",
            "current_numeric_value": "MISSING_NUMERIC_CONTACT_AMPLITUDE",
            "zero_route": "0 if support(contact) cap support(local ordinary variations) = empty and boundary data carry no marker/vector/normal-flux field",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CB3355_1_surface_to_volume_template",
            "quantity": "abs(epsilon_boundary_contact)",
            "formula": "(A_contact/V_local) * |B_contact| / |T_H^ordinary|",
            "needed_inputs": "A_contact, V_local, B_contact units, source normalization",
            "current_numeric_value": "MISSING_GEOMETRY_AND_B_CONTACT",
            "zero_route": "0 if local arena uses compact interior collar with no material boundary intersection",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3355_0_bulk_boundary_zero",
            "claim": "bulk local equations receive no exterior boundary source under compact-support local variations",
            "passed": "true",
            "reason": "standard variational split makes boundary integral vanish for interior compact-support variations",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3355_1_scalar_stationary_vector_flux_zero",
            "claim": "scalar stationary boundary carries no preferred-frame/vector flux",
            "passed": "true",
            "reason": "prior alpha3 no-flux theorem supplies a conditional trace/no-vector mechanism",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3355_2_contact_interface_zero_or_bound",
            "claim": "contact/interface source is zero or source-backed bounded",
            "passed": "false",
            "reason": "no collar-separation parent theorem and no numeric contact amplitude are supplied",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3355_3_boundary_contact_closed",
            "claim": "epsilon_boundary_contact is closed for the local GR branch",
            "passed": "false",
            "reason": "bulk boundary is narrowed, but genuine contact/interface leakage remains open",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3355_4_local_GR_claim",
            "claim": "local GR/Newton source-coupling branch is claim-ready",
            "passed": "false",
            "reason": "contact survivor plus parent-domain signature still block promotion",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3355_0",
            "question": "Did 3355 improve the boundary/contact situation?",
            "answer": "yes: boundary was split into exact bulk-zero, conditional no-flux, monopole-calibration, and genuine contact survivor",
            "reason": "this replaces one vague epsilon_boundary_contact with four typed sub-branches",
            "next_action": "prove local collar separation/contact support exclusion, or source a numeric contact bound",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3355_1",
            "question": "Can we now promote local GR?",
            "answer": "no",
            "reason": "the actual survivor is no longer generic boundary fluff; it is the contact/interface branch plus parent-domain signature",
            "next_action": "try collar separation first, then parent-domain signature collapse",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3356-Y5-R2FR-local-collar-contact-support-exclusion-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3356_local_collar_contact_support_exclusion.py",
            "objective": "prove the ordinary local source arena admits a compact interior collar whose variations do not intersect boundary/contact support, or keep a numeric contact-bound template active",
            "why_next": "3355 reduced boundary/contact to the genuine contact/interface survivor",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3357-Y5-R2FR-parent-domain-signature-collapse-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3357_parent_domain_signature_collapse.py",
            "objective": "collapse 3346, 3354, and the boundary/contact cleanup into one parent-domain signature certificate",
            "why_next": "conditional zeros only promote after the parent action domain is signed field-by-field",
            "valid_for_claim": "false",
        },
    ]


def render_doc() -> str:
    return "\n".join(
        [
            "# 3355 — Boundary / Contact Zero-Flux Or Contact Bound Under AX1090",
            "",
            f"Generated: `{RUN_UTC}`",
            "",
            "## Summary",
            "- This checkpoint attacks the boundary/contact escape hatch isolated by 3354.",
            "- Useful progress: generic boundary leakage is split into typed branches. Ordinary bulk boundary terms are exactly silent for compact-support local variations.",
            "- The old alpha3 boundary work also gives a conditional scalar-stationary no-vector/no-flux route.",
            "- The survivor is now precise: genuine contact/interface support overlapping the local material source, unless a collar-separation theorem or numeric contact bound is supplied.",
            "- No local-GR/Newton claim is promoted here.",
            "",
            "## Local Source Register",
            table(local_source_rows()),
            "## Boundary Contact Decomposition",
            table(decomposition_rows()),
            "## Zero-Flux Lemma Rows",
            table(zero_lemma_rows()),
            "## Epsilon Boundary Contact Split",
            table(epsilon_split_rows()),
            "## Contact Bound Template",
            table(contact_bound_rows()),
            "## Promotion Gates",
            table(promotion_gate_rows()),
            "## Decision Ledger",
            table(decision_rows()),
            "## Next Target",
            table(next_target_rows()),
        ]
    )


def validate_outputs() -> list[dict[str, Any]]:
    local_sources = local_source_rows()
    decomposed = decomposition_rows()
    lemmas = zero_lemma_rows()
    eps = epsilon_split_rows()
    contact = contact_bound_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    write_targets_outside_fw = all(not path.resolve().is_relative_to(FW.resolve()) for path in output_paths + [DOC])
    checks: list[dict[str, Any]] = [
        {
            "check_id": "VAL3355_0_local_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3355_1_local_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parseable"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3355_2_outputs_parse",
            "check": "all 3355 non-validation outputs parse",
            "passed": all(path.exists() and parseable(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3355_3_decomposition_complete",
            "check": "boundary/contact decomposition includes bulk, scalar no-flux, monopole, and contact survivor",
            "passed": {row["piece_id"] for row in decomposed}
            == {
                "BC3355_0_bulk_variational_boundary",
                "BC3355_1_scalar_stationary_boundary",
                "BC3355_2_constant_monopole",
                "BC3355_3_contact_interface",
            },
            "detail": "",
        },
        {
            "check_id": "VAL3355_4_bulk_zero_actual_lemma",
            "check": "compact-support bulk boundary zero lemma is present",
            "passed": any(row["lemma_id"] == "ZFL3355_0_compact_support_bulk_zero" and row["result"] == "PASS_AS_LOCAL_MATH_LEMMA" for row in lemmas),
            "detail": "",
        },
        {
            "check_id": "VAL3355_5_contact_survivor_retained",
            "check": "contact/interface survivor remains open and not falsely closed",
            "passed": any(row["split_id"] == "EPSB3355_3_contact" and row["status"] == "OPEN_PRIMARY_SURVIVOR" for row in eps)
            and any(row["gate_id"] == "GATE3355_2_contact_interface_zero_or_bound" and row["passed"] == "false" for row in gates),
            "detail": "",
        },
        {
            "check_id": "VAL3355_6_contact_template_nonclaim",
            "check": "contact bound templates are nonclaim and missing numeric inputs are explicit",
            "passed": all(row["valid_for_claim"] == "false" and "MISSING" in row["current_numeric_value"] for row in contact),
            "detail": "",
        },
        {
            "check_id": "VAL3355_7_no_local_GR_overclaim",
            "check": "local GR/Newton claim remains false",
            "passed": any(row["gate_id"] == "GATE3355_4_local_GR_claim" and row["passed"] == "false" for row in gates),
            "detail": "",
        },
        {
            "check_id": "VAL3355_8_write_scope_outside_formalization",
            "check": "all 3355 write targets are outside formalization-workbench",
            "passed": write_targets_outside_fw,
            "detail": f"write_targets={len(output_paths) + 1}",
        },
        {
            "check_id": "VAL3355_9_next_target_contact_support",
            "check": "next target attacks contact support/collar separation",
            "passed": any("contact support" in row["objective"] or "collar" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3355_10_overall",
            "check": "3355 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["local_sources"], local_source_rows())
    write_csv(OUTPUTS["decomposition"], decomposition_rows())
    write_csv(OUTPUTS["zero_lemmas"], zero_lemma_rows())
    write_csv(OUTPUTS["epsilon_split"], epsilon_split_rows())
    write_csv(OUTPUTS["contact_bound"], contact_bound_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs())
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()

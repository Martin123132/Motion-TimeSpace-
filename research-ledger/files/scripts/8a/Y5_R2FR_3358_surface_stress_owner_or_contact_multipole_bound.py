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
DOC = ROOT / "3358-Y5-R2FR-surface-stress-owner-or-contact-multipole-bound-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

LOCAL_SOURCES = [
    ("LSRC3358_0_3357_doc", ROOT / "3357-Y5-R2FR-parent-domain-signature-collapse-under-AX1090.md", "3357 source-side collapse and 3358 handoff"),
    ("LSRC3358_1_3357_scope", OUT / "P8_Y5_R2FR_3357_CLAIM_SCOPE_SEPARATION.csv", "3357 claim scope separation"),
    ("LSRC3358_2_3357_residuals", OUT / "P8_Y5_R2FR_3357_RESIDUAL_COLLAPSE_MATRIX.csv", "3357 residual collapse matrix"),
    ("LSRC3358_3_3356_eps", OUT / "P8_Y5_R2FR_3356_EPSILON_CONTACT_UPDATE.csv", "3356 surface/integrated contact survivors"),
    ("LSRC3358_4_3355_contact_template", OUT / "P8_Y5_R2FR_3355_CONTACT_BOUND_TEMPLATE.csv", "3355 contact bound templates"),
    ("LSRC3358_5_3355_boundary_split", OUT / "P8_Y5_R2FR_3355_BOUNDARY_CONTACT_DECOMPOSITION.csv", "3355 boundary/contact split"),
    ("LSRC3358_6_boundary_alpha3", OUT / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "prior boundary no-flux theorem attempt"),
    ("LSRC3358_7_boundary_premises", OUT / "P8_BOUNDARY_ALPHA3_PREMISE_OWNERSHIP.csv", "prior boundary premise ownership"),
    ("LSRC3358_8_boundary_owner", OUT / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv", "prior scalar boundary owner attempt"),
    ("LSRC3358_9_3346_normal", OUT / "P8_Y5_R2FR_3346_PARENT_ACTION_NORMAL_FORM.csv", "3346 parent normal form with S_boundary and Hilbert source"),
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3358_LOCAL_SOURCE_REGISTER.csv",
    "trichotomy": OUT / "P8_Y5_R2FR_3358_SURFACE_CONTACT_TRICHOTOMY.csv",
    "owner_theorem": OUT / "P8_Y5_R2FR_3358_SURFACE_STRESS_OWNER_THEOREM.csv",
    "multipole_bound": OUT / "P8_Y5_R2FR_3358_CONTACT_MULTIPOLE_BOUND_SCHEMA.csv",
    "epsilon_update": OUT / "P8_Y5_R2FR_3358_EPSILON_SURFACE_SOURCE_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3358_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3358_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3358_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3358_VALIDATION.csv",
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
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_str(path.exists()),
            "parseable": bool_str(path.exists() and parseable(path)),
            "usage": usage,
            "valid_for_claim": "false",
        }
        for source_id, path, usage in LOCAL_SOURCES
    ]


def trichotomy_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "TRI3358_0_ordinary_Hilbert_surface",
            "branch": "surface/contact stress is part of the same ordinary matter+EM action varied before readout",
            "mathematical_form": "T_surface^{mu nu} := -2/sqrt(|g_obs|) delta S_surface_ord/delta g_obs, with S_surface_ord subset S_matter+S_EM",
            "effect": "not an extra source; it is included in T_H^matter+T_H^EM",
            "status": "CONDITIONAL_OWNER_ZERO_RESIDUAL",
            "remaining_gap": "parent action has not signed every surface/contact term as ordinary Hilbert-owned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "TRI3358_1_universal_scalar_monopole",
            "branch": "surface/contact stress is scalar, stationary, marker-free, and universal",
            "mathematical_form": "delta M_contact = constant monopole, no vector/shear/preferred-frame projection",
            "effect": "renormalizes measured GM but does not create WEP/PPN vector/source-shadow residuals",
            "status": "CONDITIONAL_CALIBRATION_ROUTE",
            "remaining_gap": "constant-universal and derivative-silence premises are not parent-owned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "TRI3358_2_nonordinary_contact_multipoles",
            "branch": "surface/contact stress carries nonordinary labels, marker fields, vector flux, composition dependence, or hidden source support",
            "mathematical_form": "Delta T_contact decomposes into monopole, dipole/vector, quadrupole/shear, composition, and time-drift multipoles",
            "effect": "can alter Newton/PPN/orbital source normalization",
            "status": "OPEN_PRIMARY_SURVIVOR",
            "remaining_gap": "needs source-backed no-cancellation multipole bound or theorem zero",
            "valid_for_claim": "false",
        },
    ]


def owner_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "OWN3358_0_same_action_owner",
            "claim": "If a surface term is included in the same varied ordinary matter+EM action, its stress is ordinary Hilbert-owned.",
            "derivation": "Vary S_ord = S_bulk + S_surface with respect to g_obs before readout; distributional surface stress is part of T_H, not a separate T_D/P_D source.",
            "kills_residual": "epsilon_boundary_contact_as_extra_source",
            "status": "EXACT_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "OWN3358_1_unowned_counterbranch",
            "claim": "If the surface term depends on hidden labels, source projectors, readout masks, or non-Hilbert variables, it is not killed by the Hilbert owner identity.",
            "derivation": "Such dependence is an extra action argument outside S_matter+S_EM and reopens the source-shadow/projector branch.",
            "kills_residual": "none; retains nonordinary contact multipole branch",
            "status": "OPEN_COUNTERBRANCH",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "OWN3358_2_monopole_calibration",
            "claim": "If the only unowned piece is a constant universal scalar monopole, it can be absorbed into measured GM.",
            "derivation": "Exterior Newtonian monopole depends on total calibrated mass; constant universal shift does not create composition, vector, or time-drift residual by itself.",
            "kills_residual": "WEP/PPN vector residuals conditionally; not absolute GM derivation",
            "status": "CONDITIONAL_CALIBRATION_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "OWN3358_3_no_cancellation_policy",
            "claim": "Unknown contact multipoles must be bounded by an absolute envelope, not cancelled against other unknowns.",
            "derivation": "Use sum of absolute monopole, composition, vector/dipole, quadrupole/shear, and drift components before any total-score claim.",
            "kills_residual": "post-hoc cancellation route",
            "status": "POLICY_GATE",
            "valid_for_claim": "false",
        },
    ]


def multipole_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "CMB3358_0_absolute_contact_envelope",
            "quantity": "epsilon_contact_integrated_abs",
            "formula": "|DeltaM_nonuniv|/M_H + |DeltaM_comp|/M_H + |D_contact|/(M_H R) + |Q_contact|/(M_H R^2) + |dotM_contact|/(M_H H_ref)",
            "needed_inputs": "M_H, R, DeltaM_nonuniv, DeltaM_comp, D_contact, Q_contact, dotM_contact, units, source paths, ordinary-Hilbert owner flag",
            "current_numeric_value": "MISSING_CONTACT_MULTIPOLE_INPUTS",
            "observable_links": "Newton_GM; PPN; WEP; orbital; clocks_if_dotM",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CMB3358_1_universal_monopole_switch",
            "quantity": "epsilon_contact_integrated_abs",
            "formula": "0 for residual tests iff DeltaM_contact is universal, stationary, marker-free, and included in measured GM calibration",
            "needed_inputs": "universal_monopole_certificate, stationarity_certificate, no_marker_certificate, measured_GM_calibration_rule",
            "current_numeric_value": "MISSING_PARENT_MONOPOLE_CERTIFICATE",
            "observable_links": "Newton_GM_calibration; PPN_no_vector; WEP_no_composition",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CMB3358_2_ordinary_owner_switch",
            "quantity": "epsilon_contact_integrated_abs",
            "formula": "0 as extra residual iff S_contact subset S_matter+S_EM and varied into T_H before readout",
            "needed_inputs": "surface_action_path, variation_equation, no_hidden_labels, no_readout_projector, Hilbert_source_normalization",
            "current_numeric_value": "MISSING_PARENT_SURFACE_OWNER_CERTIFICATE",
            "observable_links": "local_GR_source; Newton_source; EM_stress",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
    ]


def epsilon_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "ESU3358_0_extra_contact_if_ordinary_owned",
            "symbol": "epsilon_boundary_contact_integrated",
            "branch": "ordinary Hilbert-owned surface/contact",
            "value_or_bound": "0_as_extra_residual",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "update_id": "ESU3358_1_monopole_calibration",
            "symbol": "epsilon_contact_vector_or_composition",
            "branch": "universal scalar stationary monopole",
            "value_or_bound": "0_for_vector_composition_drift_if_premises_hold",
            "status": "CONDITIONAL_CALIBRATION_NOT_PARENT_SIGNED",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "update_id": "ESU3358_2_nonordinary_multipole",
            "symbol": "epsilon_contact_integrated_abs",
            "branch": "nonordinary contact multipoles",
            "value_or_bound": "MISSING_ABSOLUTE_MULTIPOLE_ENVELOPE_INPUTS",
            "status": "OPEN_PRIMARY_SURVIVOR",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3358_0_surface_owner_theorem",
            "claim": "ordinary Hilbert-owned surface/contact stress is not an extra residual",
            "passed": "true",
            "reason": "if S_contact is varied inside S_matter+S_EM, its distributional stress belongs to T_H",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3358_1_current_parent_surface_owner",
            "claim": "current corpus parent-signs every surface/contact term as ordinary Hilbert-owned or absent",
            "passed": "false",
            "reason": "surface owner certificate and no-hidden-label/no-readout clauses are not closed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3358_2_monopole_route",
            "claim": "universal scalar stationary monopole route is mathematically safe for non-vector residuals",
            "passed": "true",
            "reason": "constant universal monopole can be measured-GM calibration rather than source-shadow residual",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3358_3_contact_multipole_bound_ready",
            "claim": "nonordinary contact multipoles have numeric/source-backed absolute bounds",
            "passed": "false",
            "reason": "multipole envelope schema is written but all numeric inputs/certificates are missing",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3358_4_integrated_Newton_PPN_closed",
            "claim": "integrated Newton/PPN source normalization is closed against surface/contact stress",
            "passed": "false",
            "reason": "requires parent surface owner, universal monopole certificate, or numeric multipole bounds",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3358_5_local_GR_claim",
            "claim": "local GR/Newton branch is claim-ready",
            "passed": "false",
            "reason": "surface/integrated source calibration and left-hand EH/Newton operator remain open",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3358_0",
            "question": "Did 3358 reduce the source-side survivor?",
            "answer": "yes: surface/contact is now a trichotomy, not a fog bank",
            "reason": "ordinary-owned contact is included in Hilbert stress; universal monopole is calibration; only nonordinary contact multipoles survive",
            "next_action": "either parent-sign the surface owner/monopole route or source actual multipole bounds",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3358_1",
            "question": "Should the next attack stay source-side or move left-hand EH/Newton?",
            "answer": "move to left-hand EH/Newton while keeping 3358 as the source-side residual contract",
            "reason": "source side now has a clean conditional packet and explicit survivor; full GR still needs the geometric operator to reduce",
            "next_action": "3359 left-hand EH/Newton operator recovery",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3359-Y5-R2FR-left-hand-EH-Newton-operator-recovery-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3359_left_hand_EH_Newton_operator_recovery.py",
            "objective": "attack the left-hand geometric side: derive or bound non-Einstein operator residues so the cleaned source-side theorem can actually reduce to GR/Newton",
            "why_next": "3358 makes the source-side survivor explicit; now the left-hand geometric operator must be attacked",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3360-Y5-R2FR-contact-multipole-source-acquisition-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3360_contact_multipole_source_acquisition.py",
            "objective": "if parent surface ownership cannot be signed, acquire concrete contact multipole bounds with source paths, units, and no-cancellation envelope",
            "why_next": "this is the fallback if surface/contact cannot be derived zero",
            "valid_for_claim": "false",
        },
    ]


def render_doc() -> str:
    return "\n".join(
        [
            "# 3358 — Surface-Stress Owner Or Contact-Multipole Bound Under AX1090",
            "",
            f"Generated: `{RUN_UTC}`",
            "",
            "## Summary",
            "- This checkpoint attacks the surface/integrated source survivor left by 3357.",
            "- Surface/contact is now split into three routes: ordinary Hilbert-owned stress, universal scalar monopole calibration, or nonordinary contact multipoles.",
            "- Real gain: if contact stress is varied inside `S_matter + S_EM`, it is not an extra source; it is already part of the Hilbert source.",
            "- Remaining survivor: nonordinary contact multipoles need either a parent-zero theorem or a source-backed no-cancellation bound.",
            "- No full Newton/PPN/local-GR claim is promoted.",
            "",
            "## Local Source Register",
            table(local_source_rows()),
            "## Surface Contact Trichotomy",
            table(trichotomy_rows()),
            "## Surface Stress Owner Theorem",
            table(owner_theorem_rows()),
            "## Contact Multipole Bound Schema",
            table(multipole_bound_rows()),
            "## Epsilon Surface Source Update",
            table(epsilon_update_rows()),
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
    trichotomy = trichotomy_rows()
    owner = owner_theorem_rows()
    multipole = multipole_bound_rows()
    eps = epsilon_update_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    write_targets_outside_fw = all(not path.resolve().is_relative_to(FW.resolve()) for path in output_paths + [DOC])
    checks: list[dict[str, Any]] = [
        {
            "check_id": "VAL3358_0_local_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3358_1_local_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parseable"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3358_2_outputs_parse",
            "check": "all 3358 non-validation outputs parse",
            "passed": all(path.exists() and parseable(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3358_3_trichotomy_complete",
            "check": "surface/contact trichotomy covers ordinary-owned, universal monopole, and nonordinary multipoles",
            "passed": {row["branch_id"] for row in trichotomy}
            == {"TRI3358_0_ordinary_Hilbert_surface", "TRI3358_1_universal_scalar_monopole", "TRI3358_2_nonordinary_contact_multipoles"},
            "detail": "",
        },
        {
            "check_id": "VAL3358_4_owner_theorem_present",
            "check": "ordinary Hilbert-owned surface theorem is present and conditional",
            "passed": any(row["theorem_id"] == "OWN3358_0_same_action_owner" and row["status"] == "EXACT_CONDITIONAL" for row in owner),
            "detail": "",
        },
        {
            "check_id": "VAL3358_5_multipole_bound_schema_nonclaim",
            "check": "contact multipole bound schemas are nonclaim and explicitly missing inputs",
            "passed": all(row["valid_for_claim"] == "false" and "MISSING" in row["current_numeric_value"] for row in multipole),
            "detail": "",
        },
        {
            "check_id": "VAL3358_6_nonordinary_survivor_retained",
            "check": "nonordinary contact multipoles remain the primary survivor",
            "passed": any(row["update_id"] == "ESU3358_2_nonordinary_multipole" and row["status"] == "OPEN_PRIMARY_SURVIVOR" for row in eps)
            and any(row["gate_id"] == "GATE3358_3_contact_multipole_bound_ready" and row["passed"] == "false" for row in gates),
            "detail": "",
        },
        {
            "check_id": "VAL3358_7_no_overclaim",
            "check": "parent surface owner, integrated Newton/PPN, and local GR claims remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3358_1_current_parent_surface_owner", "GATE3358_4_integrated_Newton_PPN_closed", "GATE3358_5_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3358_8_next_target_left_hand",
            "check": "next target attacks left-hand EH/Newton operator recovery",
            "passed": any("left-hand" in row["objective"] and "GR/Newton" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3358_9_write_scope_outside_formalization",
            "check": "all 3358 write targets are outside formalization-workbench",
            "passed": write_targets_outside_fw,
            "detail": f"write_targets={len(output_paths) + 1}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3358_10_overall",
            "check": "3358 validation overall",
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
    write_csv(OUTPUTS["trichotomy"], trichotomy_rows())
    write_csv(OUTPUTS["owner_theorem"], owner_theorem_rows())
    write_csv(OUTPUTS["multipole_bound"], multipole_bound_rows())
    write_csv(OUTPUTS["epsilon_update"], epsilon_update_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs())
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()

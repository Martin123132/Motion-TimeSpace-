from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R2FR_Y5_PHI_ANCHOR_ZERO_BOUNDARY_3582"
CHECKPOINT_ID = "3582"
DOC = ROOT / "3582-Y5-R2FR-Phi-anchor-zero-boundary-condition-or-first-finite-flux-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sources() -> dict[str, Path]:
    return {
        "next_3581": RESIDUALS / "P8_Y5_R2FR_3581_NEXT_TARGET.csv",
        "package_3581": RESIDUALS / "P8_Y5_R2FR_3581_STATIONARY_ANNULUS_PACKAGE_THEOREM.csv",
        "clauses_3581": RESIDUALS / "P8_Y5_R2FR_3581_ACTIVATION_CLAUSES.csv",
        "finite_3581": RESIDUALS / "P8_Y5_R2FR_3581_FINITE_ROWS.csv",
        "status_3581": RESIDUALS / "P8_Y5_R2FR_3581_STATUS.csv",
        "transport_3580": RESIDUALS / "P8_Y5_R2FR_3580_STATIONARY_COLLAR_TRANSPORT_LAW.csv",
        "flux_3580": RESIDUALS / "P8_Y5_R2FR_3580_FLUX_BOUND_ROWS.csv",
        "status_3580": RESIDUALS / "P8_Y5_R2FR_3580_STATUS.csv",
        "maxwell_3463": RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv",
        "poynting_3579_doc": ROOT / "3579-Y5-R2FR-public-EM-Poynting-Htau-curl-zero-or-flux-bound.md",
        "poynting_3234_doc": ROOT / "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md",
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3582_SOURCE_REGISTER.csv",
        "anchor_theorem": RESIDUALS / "P8_Y5_R2FR_3582_PHI_ANCHOR_ASYMPTOTIC_ZERO_THEOREM.csv",
        "anchor_clauses": RESIDUALS / "P8_Y5_R2FR_3582_ANCHOR_CLAUSE_AUDIT.csv",
        "bound_rows": RESIDUALS / "P8_Y5_R2FR_3582_PHI_ANCHOR_BOUND_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3582_ACTIVATION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3582_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3582_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_Phi_anchor_zero_boundary_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3582_VALIDATION.csv",
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": "3582 Phi_anchor asymptotic zero boundary proof input",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def anchor_theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "PAZ3582_0_anchor_definition",
            "infinity Poynting/Killing flux anchor",
            "Phi_infty[K] := lim_{R->infty} int_{S_R} T_EM^{mu nu} K_mu n_nu dA = lim_{R->infty} int_{S_R} n.(E x H) dA",
            "This is exactly the 3580 allowed anchor option Phi_infty, now named as the asymptotic boundary readout.",
            "ANCHOR_OBJECT_DEFINED",
            "transport_3580",
        ),
        (
            "PAZ3582_1_stationary_falloff_clause",
            "stationary finite-source Maxwell exterior",
            "E = Q rhat/(4 pi epsilon0 R^2)+O(R^-3), B = O(R^-3), and no transverse radiative O(R^-1) fields",
            "For compact stationary charges/currents in an asymptotically flat exterior, the non-radiative multipole field has Coulomb/dipole falloff rather than wave falloff.",
            "STANDARD_PUBLIC_EM_ASYMPTOTIC_INPUT",
            "maxwell_3463",
        ),
        (
            "PAZ3582_2_zero_flux_estimate",
            "net radial flux vanishes at infinity",
            "n.(E x H)=O(R^-5), dA=O(R^2), hence Phi_infty=O(R^-3)->0",
            "The asymptotic Poynting flux can circulate angularly in crossed static fields, but its net radial/Killing-energy flux through S_R tends to zero.",
            "DERIVED_CONDITIONAL_PUBLIC_EM_ZERO",
            "maxwell_3463",
        ),
        (
            "PAZ3582_3_transport_into_annulus",
            "same-annulus zero anchor transport",
            "If 3580 transport clauses close on the same P_ann, Phi_anchor=Phi_infty=0 propagates to S_out and S_in.",
            "This fills the anchor slot in the 3581 switch; it does not fill tau, surface, worldtube, gauge, or seam ownership.",
            "ANCHOR_SLOT_FILLED_CONDITIONALLY",
            "package_3581",
        ),
        (
            "PAZ3582_4_radiation_escape_clause",
            "finite-flux escape hatch",
            "If O(R^-1) radiative fields, incoming waves, external driving, or non-stationary sources are present, Phi_infty need not vanish and FAR3581_0 must be a finite measured/source-backed row.",
            "This prevents cheating: the proof closes only the stationary no-radiation boundary branch.",
            "FINITE_ROW_REQUIRED_IF_BOUNDARY_FAILS",
            "finite_3581",
        ),
        (
            "PAZ3582_5_scope_guard",
            "public EM anchor only",
            "Phi_anchor=0 does not prove the MTS EM coupling normalization, fine-structure constant, Newtonian limit, PPN pass, or local GR.",
            "The result is useful because it removes one Poynting-specific obstruction without pretending the whole local branch is solved.",
            "NO_OVERCLAIM_GUARD",
            "status_3581",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "mathematical_form": mathematical_form,
            "derivation": derivation,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for theorem_id, claim_piece, mathematical_form, derivation, status, source_key in rows
    ]


def anchor_clause_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "PAC3582_0_anchor_surface",
            "Z_anchor_surface",
            "choose S_R in the asymptotic stationary exterior as the anchor surface",
            "PASS_CONDITIONAL_PUBLIC_EM",
            "Anchor is at infinity, not an arbitrary interior surface.",
            "transport_3580",
        ),
        (
            "PAC3582_1_stationary_source",
            "Z_stationary_source",
            "source/current is stationary in the exterior readout frame",
            "PASS_IF_3580_TAU_WORLDLINE_CLAUSES_CLOSE",
            "This still depends on the same tau/worldtube ownership package.",
            "transport_3580",
        ),
        (
            "PAC3582_2_asymptotic_flat_falloff",
            "Z_asymptotic_falloff",
            "non-radiative Coulomb/dipole Maxwell falloff at large R",
            "PASS_CONDITIONAL_PUBLIC_EM",
            "This is a standard exterior boundary condition, not a new fitted MTS parameter.",
            "maxwell_3463",
        ),
        (
            "PAC3582_3_no_radiative_1overR",
            "Z_no_radiative_1overR",
            "no transverse O(R^-1) incoming/outgoing wave component in the branch",
            "PASS_BY_BOUNDARY_BRANCH_SELECTION",
            "If this fails, the finite-flux row is mandatory.",
            "poynting_3579_doc",
        ),
        (
            "PAC3582_4_radial_flux_estimate",
            "Z_radial_flux_zero",
            "area growth cannot beat O(R^-5) radial Poynting density",
            "PASS_DERIVED",
            "This is the actual proof step: O(R^-5) times O(R^2) tends to zero.",
            "maxwell_3463",
        ),
        (
            "PAC3582_5_same_package_transport",
            "Z_same_Pann_transport",
            "the infinity anchor must be linked to the same P_ann used by 3581",
            "MISSING_SAME_PACKAGE_OWNER_FOR_PUBLIC_CLAIM",
            "3582 fills the anchor; it does not yet prove every 3581 package object is parent-owned.",
            "package_3581",
        ),
        (
            "PAC3582_6_anchor_result",
            "Z_anchor",
            "Phi_anchor=0 on the stationary asymptotic public EM branch",
            "PASS_CONDITIONAL_PUBLIC_EM_ZERO_ANCHOR",
            "This closes the Poynting-specific anchor row conditionally, while keeping the full MTS/local-GR switch false.",
            "finite_3581",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": clause_id,
            "symbol": symbol,
            "clause": clause,
            "status": status,
            "notes": notes,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for clause_id, symbol, clause, status, notes, source_key in rows
    ]


def bound_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "PAB3582_0_Phi_infty",
            "Phi_infty",
            "lim_{R->infty} int_{S_R} n.(E x H) dA",
            "0",
            "W in SI or geometrized Killing-energy/time",
            "DERIVED_ZERO_UNDER_STATIONARY_ASYMPTOTIC_FALLOFF",
            "maxwell_3463",
        ),
        (
            "PAB3582_1_Phi_anchor_abs",
            "Phi_anchor_abs",
            "|Phi_anchor| with anchor=Phi_infty",
            "0",
            "same as Phi_infty",
            "FILLED_CONDITIONALLY_REPLACES_FAR3581_0_ON_THIS_BRANCH",
            "finite_3581",
        ),
        (
            "PAB3582_2_R_ann_abs_reduced",
            "R_ann_abs",
            "Delta_tau_surface_abs + Delta_surface_owner_abs + J_cross_EM_abs + C_EM_surface_gauge_abs + B_corner_flux_abs",
            "MISSING_GEOMETRY_OWNER_RESIDUALS",
            "mixed residual bound units",
            "PHI_ANCHOR_TERM_REMOVED_ONLY_IF_3582_BRANCH_CONDITIONS_HOLD",
            "package_3581",
        ),
        (
            "PAB3582_3_I_matter_EM_flux_reduced",
            "I_matter_EM_flux",
            "I_matter_EM_flux <= A_F sup_BF R_ann_abs_reduced",
            "MISSING_REMAINING_RESIDUAL_VALUES",
            "H_tau source contribution units",
            "HTAU_FEED_READY_WITH_ANCHOR_ZERO_NONCLAIM",
            "poynting_3579_doc",
        ),
        (
            "PAB3582_4_finite_escape",
            "Phi_anchor_abs",
            "finite measured/source-backed flux if radiative O(R^-1) terms or external driving are present",
            "MISSING_NUMERIC_FINITE_FLUX",
            "W or geometrized Killing-energy/time",
            "REQUIRED_IF_NO_RADIATION_BOUNDARY_REJECTED",
            "poynting_3234_doc",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "value": value,
            "units": units,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, symbol, definition, value, units, status, source_key in rows
    ]


def gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "GATE3582_0_sources",
            "PASS",
            "all source paths and selected anchors exist",
            "next_3581",
        ),
        (
            "GATE3582_1_asymptotic_anchor",
            "PASS_CONDITIONAL_PUBLIC_EM",
            "Phi_infty=0 follows from stationary finite-source Maxwell falloff with no O(R^-1) radiative field",
            "maxwell_3463",
        ),
        (
            "GATE3582_2_anchor_slot",
            "PASS_CONDITIONAL_PUBLIC_EM_ZERO_ANCHOR",
            "FAR3581_0 is filled by a theorem-zero on the asymptotic no-radiation branch",
            "finite_3581",
        ),
        (
            "GATE3582_3_full_3581_switch",
            "FAIL_CURRENT_CLAIM",
            "Z_tau, Z_surface, Z_worldtube, Z_gauge, and Z_no_seams remain unsigned",
            "status_3581",
        ),
        (
            "GATE3582_4_local_GR",
            "FAIL_CURRENT_CLAIM",
            "anchor zero is one public EM boundary condition, not a derivation of local GR/Newton",
            "status_3581",
        ),
        (
            "GATE3582_5_finite_escape",
            "PASS_GUARD",
            "radiative/external branches are routed to a finite Phi_anchor row instead of being forced to zero",
            "poynting_3234_doc",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, status, detail, source_key in rows
    ]


def status_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "PHI_ANCHOR_ZERO_DERIVED_CONDITIONALLY_PUBLIC_EM_LOCAL_BRANCH_STILL_BLOCKED",
            "strongest_result": "The Poynting-specific anchor is no longer a pure missing row: on a stationary asymptotically flat public Maxwell branch with finite compact source and no O(R^-1) radiative field, Phi_infty=0 because n.(E x H)=O(R^-5) and the sphere area is O(R^2). This conditionally fills Phi_anchor_abs=0 for the 3581 package.",
            "still_missing": "same-P_ann parent ownership of tau_obs, S_in/S_out, compact no-crossing worldtube support, EM gauge/corner silence, regulator seam ledger, and parent-owned EM normalization/charge-current coupling",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_paths["package_3581"]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3582_0",
            "target_doc": "3583-Y5-R2FR-same-Pann-tau-surface-worldtube-owner-or-residual-stack.md",
            "target_script": "scripts/Y5_R2FR_3583_same_Pann_tau_surface_worldtube_owner_or_residual_stack.py",
            "objective": "try to parent-own the same stationary package geometry: tau_obs, S_in/S_out, and compact no-crossing worldtube support, now that the Poynting anchor itself has a conditional public EM zero",
            "success_gate": "Z_tau, Z_surface, and Z_worldtube close on the same P_ann branch, or their residuals are reduced to explicit finite terms without re-opening Phi_anchor",
            "reason": "3582 removes the cleanest Poynting-specific obstruction; the remaining blocker is package geometry ownership, not another EM flux trick",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_paths: dict[str, Path],
    out_paths: dict[str, Path],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in out_paths.items() if key != "validation"}
    needles = {
        "next_3581": "NEXT3581_0",
        "package_3581": "SAP3581_1_activation_implication",
        "clauses_3581": "ACT3581_10_activation",
        "finite_3581": "FAR3581_0_Phi_anchor_abs",
        "status_3581": "STATIONARY_ANNULUS_PACKAGE_SWITCH_READY",
        "transport_3580": "TRL3580_4_anchor_zero",
        "flux_3580": "LFB3580_1_flux_anchor",
        "status_3580": "POYNTING_TRANSPORT_THEOREM",
        "maxwell_3463": "EM3463_2_poynting",
        "poynting_3579_doc": "I_matter_EM_flux",
        "poynting_3234_doc": "Poynting",
    }
    validations.append(("VAL3582_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3582 source paths exist"))
    validations.append(("VAL3582_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected 3582 anchors found"))
    validations.append(("VAL3582_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3582 output files written"))
    csvs_parse = True
    parse_details: list[str] = []
    for output_id, path in pre_validation_outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            row_count = len(read_csv(path))
            csvs_parse = csvs_parse and row_count > 0
            parse_details.append(f"{output_id}:{row_count}")
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3582_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3582_4_zero_theorem_present", any(row["status"] == "DERIVED_CONDITIONAL_PUBLIC_EM_ZERO" for row in theorem), "asymptotic zero theorem row present"))
    validations.append(("VAL3582_5_anchor_clause_promoted_conditionally", any(row["symbol"] == "Z_anchor" and "PASS_CONDITIONAL" in str(row["status"]) for row in clauses), "Z_anchor conditionally promoted"))
    validations.append(("VAL3582_6_phi_anchor_value_zero", any(row["symbol"] == "Phi_anchor_abs" and row["value"] == "0" for row in bounds), "Phi_anchor_abs zero row present"))
    validations.append(("VAL3582_7_full_switch_still_blocked", any(row["gate_id"] == "GATE3582_3_full_3581_switch" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "full 3581 switch remains blocked"))
    validations.append(("VAL3582_8_no_claim_flags", all(str(row.get("valid_for_claim", False)).lower() == "false" for row in theorem + clauses + bounds + gates + status + next_target), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3582_9_finite_escape_present", any(row["row_id"] == "PAB3582_4_finite_escape" for row in bounds), "finite-flux escape row present"))
    validations.append(("VAL3582_10_next_target_selected", any(row["next_id"] == "NEXT3582_0" for row in next_target), "same-Pann geometry next target selected"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in theorem + clauses + bounds + gates + status)
    validations.append(("VAL3582_11_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = any(FORMALIZATION.rglob("*3582*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3582_12_formalization_workbench_untouched", not formalization_touched, "no 3582 checkpoint output appears in formalization-workbench"))
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passes, detail in validations
    ]


def write_doc(
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 3582 — Phi anchor zero boundary condition or first finite flux row",
        "",
        "## Verdict",
        "3582 makes a real forward move: the Poynting anchor is not left as a vague missing object.  On the stationary asymptotic public-EM branch, choose the anchor surface at infinity:",
        "",
        "`Phi_infty[K] = lim_{R->infty} int_{S_R} T_EM^{mu nu} K_mu n_nu dA = lim_{R->infty} int_{S_R} n.(E x H) dA`.",
        "",
        "For a compact stationary Maxwell source with no transverse radiative `O(R^-1)` field, `E=O(R^-2)` and `B=O(R^-3)`, so `n.(E x H)=O(R^-5)` and the surface integral is `O(R^-3)->0`.  Therefore `Phi_anchor_abs=0` is conditionally filled for this no-radiation boundary branch.",
        "",
        "This is not a local-GR claim.  It closes the Poynting-specific anchor slot only; the same-package geometry owner remains live: `tau_obs`, `S_in/S_out`, compact no-crossing worldtube support, EM gauge/corners, and regulator seams.",
        "",
        "## Theorem rows",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['mathematical_form']} ({row['status']})")
    lines.extend(["", "## Clause audit"])
    for row in clauses:
        lines.append(f"- `{row['clause_id']}` `{row['symbol']}`: {row['status']} — {row['notes']}")
    lines.extend(["", "## Bound rows"])
    for row in bounds:
        lines.append(f"- `{row['row_id']}` `{row['symbol']}`: {row['value']} [{row['units']}] ({row['status']})")
    lines.extend(["", "## Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
        lines.append(f"- Still missing: {row['still_missing']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target"])
    for row in next_target:
        lines.append(f"- `{row['next_id']}` -> `{row['target_doc']}`")
        lines.append(f"- Objective: {row['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    out_paths = outputs()
    register = source_register(source_paths)
    theorem = anchor_theorem_rows(source_paths)
    clauses = anchor_clause_rows(source_paths)
    bounds = bound_rows(source_paths)
    gates = gate_rows(source_paths)
    status = status_rows(source_paths)
    next_target = next_target_rows()
    for key, rows in {
        "source_register": register,
        "anchor_theorem": theorem,
        "anchor_clauses": clauses,
        "bound_rows": bounds,
        "activation_gates": gates,
        "status": status,
        "next_target": next_target,
        "canonical_status": status,
    }.items():
        write_csv(out_paths[key], rows)
    validation = validation_rows(source_paths, out_paths, theorem, clauses, bounds, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(theorem, clauses, bounds, gates, status, next_target, validation)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise SystemExit(f"3582 validation failed: {failures}")
    print(f"wrote {DOC}")
    for key, path in out_paths.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()

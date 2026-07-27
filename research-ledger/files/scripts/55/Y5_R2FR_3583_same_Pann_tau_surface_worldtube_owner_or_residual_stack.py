from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R2FR_Y5_SAME_PANN_GEOMETRY_OWNER_3583"
CHECKPOINT_ID = "3583"
DOC = ROOT / "3583-Y5-R2FR-same-Pann-tau-surface-worldtube-owner-or-residual-stack.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sources() -> dict[str, Path]:
    return {
        "next_3582": RESIDUALS / "P8_Y5_R2FR_3582_NEXT_TARGET.csv",
        "status_3582": RESIDUALS / "P8_Y5_R2FR_3582_STATUS.csv",
        "anchor_clauses_3582": RESIDUALS / "P8_Y5_R2FR_3582_ANCHOR_CLAUSE_AUDIT.csv",
        "anchor_bounds_3582": RESIDUALS / "P8_Y5_R2FR_3582_PHI_ANCHOR_BOUND_ROWS.csv",
        "package_3581": RESIDUALS / "P8_Y5_R2FR_3581_STATIONARY_ANNULUS_PACKAGE_THEOREM.csv",
        "clauses_3581": RESIDUALS / "P8_Y5_R2FR_3581_ACTIVATION_CLAUSES.csv",
        "finite_3581": RESIDUALS / "P8_Y5_R2FR_3581_FINITE_ROWS.csv",
        "tau_owner_2067": RESIDUALS / "P8_Y5_PARENT_QLOC_2067_STATIONARY_TAU_OWNER_ATTEMPT.csv",
        "surface_owner_2066": RESIDUALS / "P8_Y5_PARENT_QLOC_2066_STATIONARY_SURFACE_OWNER_ATTEMPT.csv",
        "surface_requirements_2065": RESIDUALS / "P8_Y5_PARENT_QLOC_2065_ACTUAL_SURFACE_REQUIREMENTS.csv",
        "worldtube_2388": RESIDUALS / "P8_Y5_PARENT_QLOC_2388_WORLDTUBE_SUPPORT_CERTIFICATE.csv",
        "annulus_1730": RESIDUALS / "P8_Y5_PARENT_QLOC_1730_ANNULUS_SUPPORT_AUDIT.csv",
        "aext_1731": RESIDUALS / "P8_Y5_PARENT_QLOC_1731_AEXT_SUPPORT_THEOREM_ATTEMPT.csv",
        "transport_3580": RESIDUALS / "P8_Y5_R2FR_3580_STATIONARY_COLLAR_TRANSPORT_LAW.csv",
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3583_SOURCE_REGISTER.csv",
        "domain_theorem": RESIDUALS / "P8_Y5_R2FR_3583_SAME_PANN_DOMAIN_THEOREM.csv",
        "geometry_clauses": RESIDUALS / "P8_Y5_R2FR_3583_GEOMETRY_CLAUSE_AUDIT.csv",
        "residual_stack": RESIDUALS / "P8_Y5_R2FR_3583_GEOMETRY_RESIDUAL_STACK.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3583_ACTIVATION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3583_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3583_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_same_Pann_geometry_owner_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3583_VALIDATION.csv",
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
            "role": "3583 same-Pann stationary exterior geometry owner input",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def domain_theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "SPD3583_0_Estat_object",
            "single stationary exterior-domain certificate",
            "E_stat := (D_ext, K=tau_obs, r, W_source, Sigma_tau, S_in, S_out, Phi_infty)",
            "D_ext is the source-free annulus generated after choosing one parent-owned stationary flow K, one K-invariant radial/exterior function r, and one compact source worldtube W_source before readout.",
            "CERTIFICATE_OBJECT_DEFINED",
            "surface_owner_2066",
        ),
        (
            "SPD3583_1_tau_from_Estat",
            "tau and same-tau normalization",
            "L_K g_obs=0, K(r)=0, K|infty normalized once => nabla_(mu tau_nu)=0 and tau_source=tau_boundary=tau_readout",
            "A single normalized Killing generator supplies both the stationarity identity and the no tau-switch rule.",
            "DERIVED_IF_ESTAT_PARENT_SIGNED",
            "tau_owner_2067",
        ),
        (
            "SPD3583_2_surfaces_from_Estat",
            "actual annulus surfaces",
            "S_R := Sigma_tau cap {r=R}; boundary(D_stat)=S_out union (-S_in) with no time caps",
            "Regular level sets of the same r in the same slice make the variational/readout/source surfaces one object rather than three separately chosen surfaces.",
            "DERIVED_IF_ESTAT_PARENT_SIGNED",
            "surface_requirements_2065",
        ),
        (
            "SPD3583_3_worldtube_from_Estat",
            "compact support and no crossing",
            "closure(supp J_H[tau]) subset int(S_in), L_K W_source=0, and A_ext cap W_source=empty => J_cross=0 in the annulus",
            "If support is compact, K-invariant, and strictly inside S_in, the exterior annulus has no matter/charge crossing term.",
            "DERIVED_IF_ESTAT_PARENT_SIGNED",
            "worldtube_2388",
        ),
        (
            "SPD3583_4_seams_from_Estat",
            "single smooth annulus no-seam condition",
            "D_stat is one smooth K-invariant annulus with no cutoff, excision, smoothing, patch, or reference seam => B_corner_flux=0",
            "A single smooth exterior domain removes the regulator seam residual; if a patch is needed, this row fails and a finite seam row is mandatory.",
            "DERIVED_IF_ESTAT_REGULARITY_SIGNED",
            "surface_owner_2066",
        ),
        (
            "SPD3583_5_residual_collapse",
            "geometry residual collapse",
            "Phi_anchor_abs=0 from 3582 and E_stat=>Delta_tau_surface_abs=Delta_surface_owner_abs=J_cross_EM_abs=B_corner_flux_abs=0",
            "The annulus residual is reduced to C_EM_surface_gauge_abs plus any failure of E_stat. This is a real narrowing of the local branch.",
            "GEOMETRY_STACK_COLLAPSES_CONDITIONALLY",
            "anchor_bounds_3582",
        ),
        (
            "SPD3583_6_live_blocker",
            "parent-domain owner remains the hard problem",
            "Z_Estat is not yet parent-derived from the MTS action or quotient map",
            "3583 does not pretend the parent theory has already selected the stationary exterior domain. It identifies the exact object that must be derived next.",
            "MISSING_PARENT_STATIONARY_EXTERIOR_DOMAIN_THEOREM",
            "status_3582",
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


def geometry_clause_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "GCA3583_0_Estat",
            "Z_Estat",
            "parent-owned stationary exterior-domain certificate E_stat exists before readout",
            "MISSING_PARENT_STATIONARY_EXTERIOR_DOMAIN_OWNER",
            "This is now the single hard geometry owner, not five independent assumptions.",
            "status_3582",
        ),
        (
            "GCA3583_1_tau",
            "Z_tau",
            "tau_obs is the E_stat Killing generator",
            "PASS_IF_ESTAT_SIGNED",
            "Follows from L_K g_obs=0 inside the same exterior domain.",
            "tau_owner_2067",
        ),
        (
            "GCA3583_2_same_tau",
            "Z_same_tau",
            "source, Hamiltonian, boundary, clock/readout tau all use the same normalized K",
            "PASS_IF_ESTAT_ASYMPTOTIC_NORMALIZATION_SIGNED",
            "A single K normalized at the branch boundary prevents tau swapping.",
            "tau_owner_2067",
        ),
        (
            "GCA3583_3_surface",
            "Z_surface",
            "S_in and S_out are regular level surfaces of the same r on Sigma_tau",
            "PASS_IF_ESTAT_REGULAR_LEVEL_SETS_SIGNED",
            "Actual-surface equivalence is inherited from one domain object.",
            "surface_owner_2066",
        ),
        (
            "GCA3583_4_worldtube",
            "Z_worldtube",
            "W_source is compact, K-invariant, and strictly inside S_in",
            "PASS_IF_ESTAT_COMPACT_INVARIANT_SUPPORT_SIGNED",
            "No support in the annulus means no crossing current term.",
            "worldtube_2388",
        ),
        (
            "GCA3583_5_no_seams",
            "Z_no_seams",
            "E_stat uses one smooth annulus with no active regulator or patch boundary",
            "PASS_IF_ESTAT_SMOOTH_SINGLE_ANNULUS_SIGNED",
            "Otherwise B_corner_flux_abs must stay finite and sourced.",
            "surface_owner_2066",
        ),
        (
            "GCA3583_6_anchor",
            "Z_anchor",
            "Phi_anchor_abs=0 from stationary asymptotic public EM branch",
            "PASS_FROM_3582_CONDITIONAL",
            "The anchor is no longer the live geometry blocker.",
            "anchor_bounds_3582",
        ),
        (
            "GCA3583_7_gauge",
            "Z_gauge",
            "EM gauge/corner certificate on S_in union S_out",
            "MISSING_EM_GAUGE_CORNER_CERTIFICATE",
            "Still separate from E_stat unless a later closed-surface/exact-form theorem removes it.",
            "finite_3581",
        ),
        (
            "GCA3583_8_activation",
            "Z_Poynting",
            "full public EM/Poynting zero switch after 3583",
            "FAIL_CURRENT_CLAIM_ESTAT_AND_GAUGE_UNSIGNED",
            "With 3582 and 3583, the branch is narrowed but not claim-grade.",
            "package_3581",
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


def residual_stack_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "GRS3583_0_Phi_anchor_abs",
            "Phi_anchor_abs",
            "0",
            "from 3582 stationary asymptotic public EM theorem",
            "same as Phi_infty",
            "ZERO_IF_3582_BRANCH_CONDITIONS_HOLD",
            "anchor_bounds_3582",
        ),
        (
            "GRS3583_1_Delta_tau_surface_abs",
            "Delta_tau_surface_abs",
            "0 if Z_Estat, else epsilon_Killing + epsilon_same_tau",
            "E_stat supplies one normalized Killing K",
            "energy/time or Hamiltonian numerator",
            "CONDITIONAL_ZERO_OR_FINITE_ESTAT_RESIDUAL",
            "tau_owner_2067",
        ),
        (
            "GRS3583_2_Delta_surface_owner_abs",
            "Delta_surface_owner_abs",
            "0 if Z_Estat, else epsilon_surface_equivalence",
            "S_in/S_out are level sets of the same r in Sigma_tau",
            "Hamiltonian numerator",
            "CONDITIONAL_ZERO_OR_FINITE_ESTAT_RESIDUAL",
            "surface_requirements_2065",
        ),
        (
            "GRS3583_3_J_cross_EM_abs",
            "J_cross_EM_abs",
            "0 if Z_Estat, else epsilon_crossing_flux",
            "W_source compact, K-invariant, and disjoint from the annulus",
            "energy/time after EM work weighting",
            "CONDITIONAL_ZERO_OR_FINITE_ESTAT_RESIDUAL",
            "worldtube_2388",
        ),
        (
            "GRS3583_4_B_corner_flux_abs",
            "B_corner_flux_abs",
            "0 if Z_Estat smooth single-annulus, else epsilon_seam_flux",
            "no cutoff/excision/smoothing/patch/reference seam",
            "Hamiltonian numerator",
            "CONDITIONAL_ZERO_OR_FINITE_ESTAT_RESIDUAL",
            "surface_owner_2066",
        ),
        (
            "GRS3583_5_C_EM_surface_gauge_abs",
            "C_EM_surface_gauge_abs",
            "MISSING_EM_GAUGE_CORNER_VALUE_OR_ZERO_THEOREM",
            "not solved by E_stat alone",
            "Hamiltonian numerator",
            "STILL_LIVE_NON_GEOMETRY_RESIDUAL",
            "finite_3581",
        ),
        (
            "GRS3583_6_Estat_residual_norm",
            "epsilon_Estat",
            "epsilon_Killing + epsilon_same_tau + epsilon_surface_equivalence + epsilon_crossing_flux + epsilon_seam_flux",
            "finite fallback if parent action cannot sign E_stat",
            "Hamiltonian numerator or normalized dimensionless residual",
            "NO_CANCELLATION_GEOMETRY_STACK",
            "finite_3581",
        ),
        (
            "GRS3583_7_R_ann_abs_after_3583",
            "R_ann_abs",
            "C_EM_surface_gauge_abs + epsilon_Estat",
            "3582 removes Phi_anchor and 3583 collapses tau/surface/worldtube/seam into epsilon_Estat",
            "Hamiltonian numerator or normalized dimensionless residual",
            "REDUCED_RESIDUAL_STACK_NONCLAIM",
            "anchor_bounds_3582",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "symbol": symbol,
            "value_or_bound": value_or_bound,
            "derivation": derivation,
            "units": units,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, symbol, value_or_bound, derivation, units, status, source_key in rows
    ]


def gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "GATE3583_0_sources",
            "PASS",
            "all source paths and selected anchors exist",
            "next_3582",
        ),
        (
            "GATE3583_1_Estat_reducer",
            "PASS_CONDITIONAL_THEOREM",
            "one E_stat certificate implies tau, same-tau, surfaces, worldtube no-crossing, and no seams",
            "package_3581",
        ),
        (
            "GATE3583_2_anchor_carried",
            "PASS_CONDITIONAL_PUBLIC_EM_ZERO_ANCHOR",
            "Phi_anchor_abs=0 is carried from 3582 and not reopened",
            "anchor_bounds_3582",
        ),
        (
            "GATE3583_3_geometry_claim",
            "FAIL_CURRENT_CLAIM",
            "E_stat has not yet been derived from the parent MTS action or quotient map",
            "status_3582",
        ),
        (
            "GATE3583_4_gauge_corner",
            "FAIL_CURRENT_CLAIM",
            "C_EM_surface_gauge_abs remains unsigned or unbounded",
            "finite_3581",
        ),
        (
            "GATE3583_5_local_GR",
            "FAIL_CURRENT_CLAIM",
            "local GR/Newton still requires parent action, coupling normalization, denominator positivity, and PPN residual closure",
            "package_3581",
        ),
    ]
    resolved: list[dict[str, object]] = []
    for gate_id, status, detail, source_key in rows:
        source_path = source_paths[source_key]
        resolved.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "gate_id": gate_id,
                "status": status,
                "detail": detail,
                "source_path": str(source_path),
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return resolved


def status_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "SAME_PANN_GEOMETRY_REDUCED_TO_SINGLE_ESTAT_OWNER_NOT_PARENT_SIGNED",
            "strongest_result": "The tau/surface/worldtube/no-seam blockers are no longer independent loose assumptions. A single stationary exterior-domain certificate E_stat=(D_ext,K,r,W_source,Sigma_tau,S_in,S_out,Phi_infty) would imply Z_tau, Z_same_tau, Z_surface, Z_worldtube, and Z_no_seams on the same P_ann branch. With the 3582 Phi_anchor zero carried forward, R_ann_abs reduces to C_EM_surface_gauge_abs + epsilon_Estat.",
            "still_missing": "parent derivation of E_stat from the MTS action/quotient map, EM gauge/corner silence or finite value, source coupling normalization, positive same-frame denominator, and PPN/local-GR residual closure",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_paths["status_3582"]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3583_0",
            "target_doc": "3584-Y5-R2FR-parent-Estat-stationary-exterior-domain-theorem-or-epsilon-stack.md",
            "target_script": "scripts/Y5_R2FR_3584_parent_Estat_stationary_exterior_domain_theorem_or_epsilon_stack.py",
            "objective": "try to derive E_stat from the parent MTS action/quotient map as the local stationary exterior branch, or define the finite epsilon_Estat stack with measurable/source-backed terms",
            "success_gate": "E_stat is parent-signed before readout, or epsilon_Killing/epsilon_same_tau/epsilon_surface/epsilon_crossing/epsilon_seam are explicit finite residual rows",
            "reason": "3583 shows E_stat is now the central geometry gate; solving gauge first would be useful but would not connect MTS to local GR as directly",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_paths: dict[str, Path],
    out_paths: dict[str, Path],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in out_paths.items() if key != "validation"}
    needles = {
        "next_3582": "NEXT3582_0",
        "status_3582": "PHI_ANCHOR_ZERO_DERIVED_CONDITIONALLY_PUBLIC_EM",
        "anchor_clauses_3582": "PAC3582_6_anchor",
        "anchor_bounds_3582": "PAB3582_1_Phi_anchor_abs",
        "package_3581": "SAP3581_1_activation_implication",
        "clauses_3581": "ACT3581_3_tau_Killing",
        "finite_3581": "FAR3581_1_Delta_tau_surface_abs",
        "tau_owner_2067": "STO2067_1_Killing_identity",
        "surface_owner_2066": "SSO2066_1_domain_Dstat",
        "surface_requirements_2065": "ASR2065_3_surface_equivalence",
        "worldtube_2388": "WSC2388_5_no_crossing",
        "annulus_1730": "ASA1730_2_source_free_annulus",
        "aext_1731": "AST1731_0_geometry_antecedent",
        "transport_3580": "TRL3580_3_surface_transport",
    }
    validations.append(("VAL3583_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3583 source paths exist"))
    validations.append(("VAL3583_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected 3583 anchors found"))
    validations.append(("VAL3583_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3583 output files written"))
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
    validations.append(("VAL3583_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3583_4_Estat_object_present", any(row["theorem_id"] == "SPD3583_0_Estat_object" for row in theorem), "E_stat object theorem row present"))
    validations.append(("VAL3583_5_geometry_reducer_present", any(row["theorem_id"] == "SPD3583_5_residual_collapse" for row in theorem), "geometry residual collapse row present"))
    required_symbols = {"Z_Estat", "Z_tau", "Z_same_tau", "Z_surface", "Z_worldtube", "Z_no_seams", "Z_anchor", "Z_gauge", "Z_Poynting"}
    validations.append(("VAL3583_6_clause_symbols_present", required_symbols.issubset({str(row["symbol"]) for row in clauses}), "all 3583 clause symbols present"))
    validations.append(("VAL3583_7_anchor_not_reopened", any(row["symbol"] == "Phi_anchor_abs" and "ZERO" in str(row["status"]) for row in residuals), "3582 anchor zero carried forward"))
    validations.append(("VAL3583_8_reduced_stack_present", any(row["row_id"] == "GRS3583_7_R_ann_abs_after_3583" and "epsilon_Estat" in str(row["value_or_bound"]) for row in residuals), "reduced R_ann stack present"))
    validations.append(("VAL3583_9_full_claim_blocked", any(row["gate_id"] == "GATE3583_3_geometry_claim" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "geometry claim remains blocked until parent E_stat is signed"))
    validations.append(("VAL3583_10_no_claim_flags", all(str(row.get("valid_for_claim", False)).lower() == "false" for row in theorem + clauses + residuals + gates + status + next_target), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3583_11_next_target_selected", any(row["next_id"] == "NEXT3583_0" for row in next_target), "parent E_stat next target selected"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in theorem + clauses + residuals + gates + status)
    validations.append(("VAL3583_12_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = any(FORMALIZATION.rglob("*3583*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3583_13_formalization_workbench_untouched", not formalization_touched, "no 3583 checkpoint output appears in formalization-workbench"))
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
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 3583 — same-Pann tau/surface/worldtube owner or residual stack",
        "",
        "## Verdict",
        "3583 turns the remaining same-annulus geometry problem into one precise object: `E_stat=(D_ext,K,r,W_source,Sigma_tau,S_in,S_out,Phi_infty)`.  If the parent theory owns `E_stat` before readout, then the previously separate blockers `Z_tau`, `Z_same_tau`, `Z_surface`, `Z_worldtube`, and `Z_no_seams` close together on the same `P_ann` branch.",
        "",
        "This is a forward reduction, not a claim.  `E_stat` is not yet derived from the MTS parent action or quotient map.  With the `3582` asymptotic anchor carried forward, the annulus residual narrows to:",
        "",
        "`R_ann_abs = C_EM_surface_gauge_abs + epsilon_Estat`.",
        "",
        "So the Poynting/local-EM branch is now mainly blocked by two things: parent ownership of `E_stat`, and the EM gauge/corner term.",
        "",
        "## Domain theorem rows",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['mathematical_form']} ({row['status']})")
    lines.extend(["", "## Geometry clause audit"])
    for row in clauses:
        lines.append(f"- `{row['clause_id']}` `{row['symbol']}`: {row['status']} — {row['notes']}")
    lines.extend(["", "## Residual stack"])
    for row in residuals:
        lines.append(f"- `{row['row_id']}` `{row['symbol']}`: {row['value_or_bound']} ({row['status']})")
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
    theorem = domain_theorem_rows(source_paths)
    clauses = geometry_clause_rows(source_paths)
    residuals = residual_stack_rows(source_paths)
    gates = gate_rows(source_paths)
    status = status_rows(source_paths)
    next_target = next_target_rows()
    for key, rows in {
        "source_register": register,
        "domain_theorem": theorem,
        "geometry_clauses": clauses,
        "residual_stack": residuals,
        "activation_gates": gates,
        "status": status,
        "next_target": next_target,
        "canonical_status": status,
    }.items():
        write_csv(out_paths[key], rows)
    validation = validation_rows(source_paths, out_paths, theorem, clauses, residuals, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(theorem, clauses, residuals, gates, status, next_target, validation)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise SystemExit(f"3583 validation failed: {failures}")
    print(f"wrote {DOC}")
    for key, path in out_paths.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()

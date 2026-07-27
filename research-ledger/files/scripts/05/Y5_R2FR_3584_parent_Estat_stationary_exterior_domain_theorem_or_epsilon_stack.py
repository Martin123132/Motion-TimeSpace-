from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_ESTAT_STATIONARY_EXTERIOR_3584"
CHECKPOINT_ID = "3584"
DOC = ROOT / "3584-Y5-R2FR-parent-Estat-stationary-exterior-domain-theorem-or-epsilon-stack.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sources() -> dict[str, Path]:
    return {
        "next_3583": RESIDUALS / "P8_Y5_R2FR_3583_NEXT_TARGET.csv",
        "status_3583": RESIDUALS / "P8_Y5_R2FR_3583_STATUS.csv",
        "domain_3583": RESIDUALS / "P8_Y5_R2FR_3583_SAME_PANN_DOMAIN_THEOREM.csv",
        "residuals_3583": RESIDUALS / "P8_Y5_R2FR_3583_GEOMETRY_RESIDUAL_STACK.csv",
        "lovelock_1339": RESIDUALS / "P8_Y5_R10_1339_LOVELOCK_CONDITIONAL_THEOREM.csv",
        "newton_1339": RESIDUALS / "P8_Y5_R10_1339_NEWTON_TRANSFER_BLOCKERS.csv",
        "parent_action_1196": RESIDUALS / "P8_Y5_R10_1196_PARENT_ACTION_BLOCK_ATTEMPT.csv",
        "action_coverage_1276": RESIDUALS / "P8_Y5_R10_1276_A511_ACTION_BLOCK_COVERAGE.csv",
        "matter_clause_1411": RESIDUALS / "P8_Y5_R10_1411_PARENT_ACTION_LOCK_CLAUSE.csv",
        "matter_proof_1411": RESIDUALS / "P8_Y5_R10_1411_COMMON_LOCK_PROOF_CHAIN.csv",
        "current_owner_1418": RESIDUALS / "P8_Y5_R10_1418_ACTION_SCALE_CURRENT_OWNER_LOCK_ATTEMPT.csv",
        "tau_owner_2067": RESIDUALS / "P8_Y5_PARENT_QLOC_2067_STATIONARY_TAU_OWNER_ATTEMPT.csv",
        "worldtube_2388": RESIDUALS / "P8_Y5_PARENT_QLOC_2388_WORLDTUBE_SUPPORT_CERTIFICATE.csv",
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3584_SOURCE_REGISTER.csv",
        "estat_theorem": RESIDUALS / "P8_Y5_R2FR_3584_PARENT_ESTAT_THEOREM_ATTEMPT.csv",
        "stationarity_clauses": RESIDUALS / "P8_Y5_R2FR_3584_STATIONARITY_CLAUSE_AUDIT.csv",
        "epsilon_stack": RESIDUALS / "P8_Y5_R2FR_3584_ESTAT_EPSILON_STACK.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3584_ACTIVATION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3584_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3584_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_parent_Estat_stationary_exterior_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3584_VALIDATION.csv",
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
            "role": "3584 parent E_stat stationarity theorem input",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def estat_theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "PET3584_0_target",
            "E_stat target imported from 3583",
            "E_stat=(D_ext,K,r,W_source,Sigma_tau,S_in,S_out,Phi_infty)",
            "3583 proves that this single object would close the tau/surface/worldtube/no-seam geometry stack.",
            "TARGET_DEFINED_BY_3583",
            "domain_3583",
        ),
        (
            "PET3584_1_operator_route",
            "local exterior operator route",
            "4D + local + diffeo invariant + metric-only + Levi-Civita + second-order + boundary-harmless => E_mn=aG_mn+bg_mn",
            "The Lovelock conditional theorem gives an EH-style exterior operator if the MTS parent branch signs the premises.",
            "CONDITIONAL_EH_OPERATOR_AVAILABLE",
            "lovelock_1339",
        ),
        (
            "PET3584_2_symmetry_inheritance",
            "stationarity inheritance lemma",
            "If F(Phi)=0, L_K F=0, boundary/source data are K-invariant, and the exterior solution is unique modulo gauge, then L_K Phi=0",
            "The K-flow of a solution is another solution with the same data. Uniqueness modulo gauge forces equality, which is the cleanest non-smuggled route to stationary E_stat.",
            "MATHEMATICAL_LEMMA_CLEAN_CONDITIONAL",
            "parent_action_1196",
        ),
        (
            "PET3584_3_no_homogeneous_kernel",
            "no nonstationary homogeneous exterior mode",
            "ker(D F_ext) contains no physical time-dependent/radiative mode compatible with the chosen boundary class",
            "This is the real hard clause. Without it, boundary symmetry does not forbid hidden waves, memory tails, or extra-field hair.",
            "MISSING_NO_RADIATIVE_HOMOGENEOUS_KERNEL_THEOREM",
            "action_coverage_1276",
        ),
        (
            "PET3584_4_source_boundary_route",
            "compact stationary source boundary",
            "L_K J_H=0, closure(supp J_H) compact inside S_in, and source/current owner fixed before readout",
            "Source stationarity and compactness must come from the parent matter/current owner, not from a fitted annulus.",
            "MISSING_PARENT_SOURCE_CURRENT_OWNER_FOR_ESTAT",
            "current_owner_1418",
        ),
        (
            "PET3584_5_Estat_construction",
            "construct E_stat if clauses sign",
            "K from boundary symmetry; Sigma_tau orthogonal/compatible slice; r K-invariant exterior radius; S_in/S_out regular level surfaces; W_source compact",
            "If PET3584_1..4 sign together, 3583's E_stat is parent-owned and the geometry stack collapses without an added plateau axiom.",
            "E_STAT_DERIVED_IF_ALL_CLAUSES_SIGN",
            "domain_3583",
        ),
        (
            "PET3584_6_current_verdict",
            "3584 verdict",
            "E_stat is not claim-grade because uniqueness/no-radiative-kernel, extra-field silence, and source-current owner are unsigned",
            "The route is mathematically credible but not yet a proof of local GR. The honest output is the epsilon_Estat stack.",
            "PARENT_ESTAT_NOT_PROVED_CURRENT_CORPUS",
            "status_3583",
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


def stationarity_clause_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "SCA3584_0_parent_operator",
            "Z_parent_operator",
            "parent local exterior operator is EH/Lovelock-compatible or has a bounded non-EH residual",
            "CONDITIONAL_ONLY",
            "Lovelock route is clean but its MTS premises are not parent-derived.",
            "lovelock_1339",
        ),
        (
            "SCA3584_1_boundary_K",
            "Z_boundary_K",
            "one asymptotic/boundary time generator K is fixed before readout",
            "MISSING_PARENT_BOUNDARY_TIME_GENERATOR",
            "Needed so stationarity is inherited from a branch symmetry, not chosen after the fit.",
            "tau_owner_2067",
        ),
        (
            "SCA3584_2_source_K",
            "Z_source_K",
            "source/current/worldtube data are K-invariant and compact",
            "MISSING_PARENT_SOURCE_CURRENT_OWNER",
            "Matter/current owner remains the source-side local-GR coupling problem.",
            "worldtube_2388",
        ),
        (
            "SCA3584_3_uniqueness",
            "Z_unique_ext",
            "exterior boundary-value problem has unique solution modulo gauge",
            "MISSING_EXTERIOR_UNIQUENESS_THEOREM",
            "This is what converts symmetric data into a symmetric solution.",
            "parent_action_1196",
        ),
        (
            "SCA3584_4_no_homogeneous_mode",
            "Z_no_hom_mode",
            "no radiative/time-dependent homogeneous exterior mode survives the boundary class",
            "MISSING_NO_RADIATIVE_HOMOGENEOUS_KERNEL_THEOREM",
            "This is the dangerous clause: without it, E_stat can fail even when boundary data are stationary.",
            "action_coverage_1276",
        ),
        (
            "SCA3584_5_extra_silence",
            "Z_extra_silence",
            "MTS extra fields have no unsourced stationary-exterior hair at local order",
            "MISSING_EXTRA_FIELD_SILENCE_OR_RESIDUAL",
            "Needed because EH stationarity is not enough if retained MTS fields source the observed geometry.",
            "action_coverage_1276",
        ),
        (
            "SCA3584_6_Estat",
            "Z_Estat",
            "parent-owned E_stat follows from SCA3584_0..5",
            "FAIL_CURRENT_CLAIM_PREMISES_UNSIGNED",
            "The theorem route is exact conditional; the current corpus has not signed the premises.",
            "domain_3583",
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


def epsilon_stack_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "ESE3584_0_epsilon_boundary_K",
            "epsilon_boundary_K",
            "norm(L_K boundary/reference data)",
            "finite residual if no parent-owned boundary time generator exists",
            "dimensionless or Hamiltonian-normalized boundary norm",
            "MISSING_NUMERIC_OR_PARENT_ZERO",
            "tau_owner_2067",
        ),
        (
            "ESE3584_1_epsilon_source_K",
            "epsilon_source_K",
            "norm(L_K J_H) + tail/support leakage",
            "finite residual if source/current/worldtube is not K-invariant and compact",
            "source-current norm or energy/time",
            "MISSING_NUMERIC_OR_PARENT_ZERO",
            "worldtube_2388",
        ),
        (
            "ESE3584_2_epsilon_unique",
            "epsilon_unique_ext",
            "norm of nonunique exterior solution branch at fixed boundary/source data",
            "finite residual for failure of exterior uniqueness modulo gauge",
            "field/operator norm",
            "MISSING_NUMERIC_OR_PARENT_ZERO",
            "parent_action_1196",
        ),
        (
            "ESE3584_3_epsilon_hom",
            "epsilon_hom_mode",
            "projection of radiative/time-dependent homogeneous exterior modes into R_ann",
            "finite residual if no-radiation/no-hair kernel theorem fails",
            "Hamiltonian numerator or normalized residual",
            "MISSING_NUMERIC_OR_PARENT_ZERO",
            "action_coverage_1276",
        ),
        (
            "ESE3584_4_epsilon_extra",
            "epsilon_extra_hair",
            "local-order observed-geometry source from retained non-EH MTS fields",
            "finite residual if extra-field silence is not proved",
            "PPN/source norm",
            "MISSING_NUMERIC_OR_PARENT_ZERO",
            "newton_1339",
        ),
        (
            "ESE3584_5_epsilon_Estat",
            "epsilon_Estat",
            "epsilon_boundary_K + epsilon_source_K + epsilon_unique_ext + epsilon_hom_mode + epsilon_extra_hair",
            "the exact failure stack replacing a parent E_stat theorem",
            "same normalization as R_ann residual",
            "NO_CANCELLATION_ESTAT_STACK_READY_VALUES_MISSING",
            "residuals_3583",
        ),
        (
            "ESE3584_6_Rann_after_3584",
            "R_ann_abs",
            "C_EM_surface_gauge_abs + epsilon_Estat",
            "same reduced residual as 3583, now with epsilon_Estat decomposed into parent-action stationarity failures",
            "Hamiltonian numerator or normalized residual",
            "REDUCED_AND_DECOMPOSED_NONCLAIM",
            "residuals_3583",
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
            "meaning": meaning,
            "units": units,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, symbol, definition, meaning, units, status, source_key in rows
    ]


def gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("GATE3584_0_sources", "PASS", "all source paths and selected anchors exist", "next_3583"),
        ("GATE3584_1_symmetry_lemma", "PASS_CONDITIONAL_THEOREM", "stationarity follows from K-invariant equations/data plus uniqueness modulo gauge", "parent_action_1196"),
        ("GATE3584_2_EH_operator", "PASS_CONDITIONAL_ONLY", "Lovelock gives EH operator only if MTS signs the premises", "lovelock_1339"),
        ("GATE3584_3_Estat_claim", "FAIL_CURRENT_CLAIM", "no-radiative homogeneous kernel, extra-field silence, and source-current owner are unsigned", "domain_3583"),
        ("GATE3584_4_Newton_GR", "FAIL_CURRENT_CLAIM", "Newton/local-GR transfer still needs source closure, GM calibration, coupling normalization, and PPN residual closure", "newton_1339"),
        ("GATE3584_5_epsilon_stack", "PASS_NONCLAIM_FALLBACK", "epsilon_Estat stack is explicit if E_stat cannot be parent-signed", "residuals_3583"),
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
            "status": "PARENT_ESTAT_ROUTE_DERIVED_AS_UNIQUENESS_LEMMA_BUT_NOT_SIGNED",
            "strongest_result": "3584 identifies the non-smuggled derivation route for E_stat: K-invariant parent exterior equations plus K-invariant boundary/source data plus uniqueness modulo gauge imply L_K fields=0, so the stationary exterior domain follows. This is an actual theorem pattern, not a plateau axiom.",
            "still_missing": "MTS parent proof of the EH/non-EH operator premises, parent-owned boundary K, compact K-invariant source/current owner, exterior uniqueness/no homogeneous radiative kernel, extra-field no-hair/silence, EM gauge/corner term, source coupling normalization, and Newton/PPN calibration",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_paths["domain_3583"]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3584_0",
            "target_doc": "3585-Y5-R2FR-no-homogeneous-exterior-mode-or-extra-hair-epsilon-row.md",
            "target_script": "scripts/Y5_R2FR_3585_no_homogeneous_exterior_mode_or_extra_hair_epsilon_row.py",
            "objective": "attack the hardest unsigned clause in the E_stat theorem: prove no radiative/time-dependent homogeneous exterior mode or retained extra-field hair survives the local stationary boundary class, or write epsilon_hom_mode and epsilon_extra_hair rows",
            "success_gate": "Z_no_hom_mode and Z_extra_silence close conditionally from the parent operator class, or epsilon_hom_mode/epsilon_extra_hair get explicit source-backed norm definitions",
            "reason": "boundary symmetry plus uniqueness is the clean route to E_stat; the dangerous obstruction is hidden homogeneous/extrafield hair",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_paths: dict[str, Path],
    out_paths: dict[str, Path],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    epsilons: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in out_paths.items() if key != "validation"}
    needles = {
        "next_3583": "NEXT3583_0",
        "status_3583": "SAME_PANN_GEOMETRY_REDUCED_TO_SINGLE_ESTAT",
        "domain_3583": "SPD3583_6_live_blocker",
        "residuals_3583": "GRS3583_7_R_ann_abs_after_3583",
        "lovelock_1339": "LOV1339_0_conditional_EH_selection",
        "newton_1339": "NEW1339_0_EH_operator",
        "parent_action_1196": "PAB1196_4_parent_ownership_clauses",
        "action_coverage_1276": "AC1276_0_EH_core",
        "matter_clause_1411": "PAC1411_0_parent_signature",
        "matter_proof_1411": "PRF1411_4_local_GR_relevance",
        "current_owner_1418": "ACL1418_6_verdict",
        "tau_owner_2067": "STO2067_5_EH_or_R11_operator",
        "worldtube_2388": "WSC2388_5_no_crossing",
    }
    validations.append(("VAL3584_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3584 source paths exist"))
    validations.append(("VAL3584_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected 3584 anchors found"))
    validations.append(("VAL3584_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3584 output files written"))
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
    validations.append(("VAL3584_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3584_4_symmetry_lemma_present", any(row["theorem_id"] == "PET3584_2_symmetry_inheritance" for row in theorem), "stationarity inheritance lemma present"))
    validations.append(("VAL3584_5_no_hom_blocker_present", any(row["symbol"] == "Z_no_hom_mode" and "MISSING" in str(row["status"]) for row in clauses), "no homogeneous mode blocker present"))
    validations.append(("VAL3584_6_epsilon_stack_present", any(row["symbol"] == "epsilon_Estat" for row in epsilons), "epsilon_Estat stack present"))
    validations.append(("VAL3584_7_Estat_not_overclaimed", any(row["gate_id"] == "GATE3584_3_Estat_claim" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "E_stat remains unclaimed"))
    validations.append(("VAL3584_8_no_claim_flags", all(str(row.get("valid_for_claim", False)).lower() == "false" for row in theorem + clauses + epsilons + gates + status + next_target), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3584_9_next_target_selected", any(row["next_id"] == "NEXT3584_0" for row in next_target), "no-homogeneous-mode next target selected"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in theorem + clauses + epsilons + gates + status)
    validations.append(("VAL3584_10_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_3584*")) or any(FORMALIZATION.rglob("3584-Y5-R2FR*"))
    validations.append(("VAL3584_11_formalization_workbench_untouched", not formalization_touched, "no 3584 checkpoint output appears in formalization-workbench"))
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
    epsilons: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 3584 — parent E_stat stationary exterior theorem or epsilon stack",
        "",
        "## Verdict",
        "3584 finds the clean non-smuggled route to `E_stat`: if the parent exterior equations, boundary data, and source/current data are invariant under one time generator `K`, and the exterior boundary-value problem is unique modulo gauge with no radiative homogeneous kernel, then the `K`-flowed solution is the same solution.  Therefore `L_K fields=0` and the stationary exterior domain follows.",
        "",
        "That is a real theorem pattern, not a closure axiom.  But MTS does not yet own the premises: EH/non-EH operator selection, boundary `K`, compact K-invariant source/current owner, uniqueness/no-homogeneous-mode, and extra-field silence remain unsigned.",
        "",
        "So `E_stat` is not claimed.  The honest fallback is:",
        "",
        "`epsilon_Estat = epsilon_boundary_K + epsilon_source_K + epsilon_unique_ext + epsilon_hom_mode + epsilon_extra_hair`.",
        "",
        "## E_stat theorem attempt",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['mathematical_form']} ({row['status']})")
    lines.extend(["", "## Stationarity clause audit"])
    for row in clauses:
        lines.append(f"- `{row['clause_id']}` `{row['symbol']}`: {row['status']} — {row['notes']}")
    lines.extend(["", "## Epsilon stack"])
    for row in epsilons:
        lines.append(f"- `{row['row_id']}` `{row['symbol']}`: {row['definition']} ({row['status']})")
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
    theorem = estat_theorem_rows(source_paths)
    clauses = stationarity_clause_rows(source_paths)
    epsilons = epsilon_stack_rows(source_paths)
    gates = gate_rows(source_paths)
    status = status_rows(source_paths)
    next_target = next_target_rows()
    for key, rows in {
        "source_register": register,
        "estat_theorem": theorem,
        "stationarity_clauses": clauses,
        "epsilon_stack": epsilons,
        "activation_gates": gates,
        "status": status,
        "next_target": next_target,
        "canonical_status": status,
    }.items():
        write_csv(out_paths[key], rows)
    validation = validation_rows(source_paths, out_paths, theorem, clauses, epsilons, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(theorem, clauses, epsilons, gates, status, next_target, validation)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise SystemExit(f"3584 validation failed: {failures}")
    print(f"wrote {DOC}")
    for key, path in out_paths.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()

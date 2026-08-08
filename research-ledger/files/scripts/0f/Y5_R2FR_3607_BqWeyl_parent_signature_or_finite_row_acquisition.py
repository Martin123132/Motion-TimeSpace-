from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3607"
BRANCH_ID = "MTS_R2FR_Y5_BQWEYL_SIGNATURE_OR_FINITE_ACQ_3607"
DOC = ROOT / "3607-Y5-R2FR-BqWeyl-parent-signature-or-finite-row-acquisition.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def sources() -> dict[str, tuple[Path, str]]:
    return {
        "next_3606": (RESIDUALS / "P8_Y5_R2FR_3606_NEXT_TARGET.csv", "NEXT3606_0"),
        "status_3606": (RESIDUALS / "P8_Y5_R2FR_3606_STATUS.csv", "BQWEYL_INDEX_THEOREM"),
        "bounds_3606": (RESIDUALS / "P8_Y5_R2FR_3606_BQWEYL_BOUND_ROWS.csv", "BQB3606_1_BqWeyl"),
        "theorem_3606": (RESIDUALS / "P8_Y5_R2FR_3606_BQWEYL_NO_SPURION_THEOREM.csv", "BQW3606_5_finite_bound_law"),
        "gates_3606": (RESIDUALS / "P8_Y5_R2FR_3606_PROMOTION_GATES.csv", "PROM3606_2_current_zero_claim"),
        "parent_signature_gate": (RESIDUALS / "P8_Y5_PARENT_QLOC_2304_PARENT_SIGNATURE_GATE.csv", "PTG2304_7_verdict"),
        "first_source_input": (RESIDUALS / "P8_Y5_PARENT_QLOC_2304_BQWEYL_FIRST_SOURCE_INPUT.csv", "BQI2304_1_BqWeyl_parent_coefficient"),
        "index_lemma": (RESIDUALS / "P8_Y5_PARENT_QLOC_2304_OBJECT_LANGUAGE_INDEX_LEMMA.csv", "OLI2304_6_verdict"),
        "countermodels": (RESIDUALS / "P8_Y5_PARENT_QLOC_2304_CURVATURE_COUNTERMODEL_LEDGER.csv", "CM2304_0_weyl_spurion"),
        "claim_gates_2304": (RESIDUALS / "P8_Y5_PARENT_QLOC_2304_CLAIM_GATES.csv", "GATE2304_3_numeric_bound_input"),
        "bound_nonclaim_2302": (RESIDUALS / "P8_Y5_PARENT_QLOC_2302_BQWEYL_BOUND_ROW_NONCLAIM.csv", "BQB2302_2_profile_response"),
        "dqweyl2_inputs": (RESIDUALS / "P8_Y5_R2FR_2754_DQWEYL2_INPUT_CONTRACT.csv", "IN2754_1_Zq"),
        "dqweyl2_no_tower": (RESIDUALS / "P8_Y5_R2FR_2754_DQWEYL2_NO_TOWER_ZERO_ATTEMPT.csv", "TOWER2754_3_verdict"),
        "weyl2_projection": (RESIDUALS / "P8_Y5_R2FR_2754_SCHWARZSCHILD_WEYL2_PROJECTION_GATE.csv", "PROJ2754_2_far_field"),
        "dqweyl2_runner_gate": (RESIDUALS / "P8_Y5_R2FR_2755_DQWEYL2_RUNNER_ACTIVATION_GATE.csv", "DACT2755_3_bound_route"),
        "ppn_kernel": (RESIDUALS / "P8_Y5_R2FR_2889_COMMON_WEYL_PPN_KERNEL_ROW_NONCLAIM.csv", "PPNK2889_0_common_weyl_gamma"),
        "bqweyl_status": (RESIDUALS / "P8_Y5_NO_SHADOW_2530_BQWEYL_BOUND_ROW_STATUS.csv", "BQB2530_2_q_operator"),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3607_SOURCE_REGISTER.csv",
        "parent_signature_audit": RESIDUALS / "P8_Y5_R2FR_3607_BQWEYL_PARENT_SIGNATURE_AUDIT.csv",
        "finite_acquisition_rows": RESIDUALS / "P8_Y5_R2FR_3607_BQWEYL_FINITE_ACQUISITION_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3607_BQWEYL_ACTIVATION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3607_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3607_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_BqWeyl_parent_signature_or_finite_acquisition_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3607_VALIDATION.csv",
    }


def source_register_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    rows = []
    for source_id, (path, needle) in source_map.items():
        exists = path.exists()
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def parent_signature_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("PSA3607_0_parent_typed_language", "parent typed object-language", "one parent grammar/action domain derived from MTS primitives before fitting", "MISSING_PARENT_SIGNATURE", "without it the no-spurion theorem is a closure contract, not parent action", "parent_signature_gate"),
        ("PSA3607_1_object_language_exhaustion", "object-language exhaustion", "Allowed[S_vis] exhausted by Image(ParentGenerate)", "MISSING_OBJECT_LANGUAGE_EXHAUSTION", "extra local counterterm algebra can reintroduce P^{abcd}", "parent_signature_gate"),
        ("PSA3607_2_q_representation", "q scalar/quotient/pure-density representation", "q has no Weyl-index type and no hidden four-index slot", "MISSING_Q_FIELD_CONTENT_CERTIFICATE", "q P^{abcd} C_abcd remains legal as a countermodel", "parent_signature_gate"),
        ("PSA3607_3_no_spurion_projector", "no Weyl spurion/projector/readout kernel", "parent normal form forbids P^{abcd}C_abcd source/readout maps", "MISSING_NO_SPURION_SIGNATURE", "linear B_qWeyl can survive through spurion/projector/readout channel", "countermodels"),
        ("PSA3607_4_hidden_frame_extensions", "hidden frame exclusion", "no hidden conformal/disformal/readout frame supplies the missing tensor", "MISSING_FRAME_DESCENT_SIGNATURE", "effect can move into clocks, matter constants or PPN", "countermodels"),
        ("PSA3607_5_curvature_morphism", "curvature morphism exclusion", "hidden invariants cannot feed curvature coefficients", "MISSING_CURVATURE_MORPHISM_EXCLUSION", "F(I_hid)R or F(I_hid)C^2 remains legal", "countermodels"),
        ("PSA3607_6_no_higher_curvature_tower", "quadratic/higher-curvature tower exclusion", "no q C^2, Ricci2, R2 or nonlocal tower is generated", "MISSING_HIGHER_CURVATURE_SIGNATURE", "linear B_qWeyl cleanup would overclaim without D_qWeyl2 guard", "dqweyl2_no_tower"),
        ("PSA3607_7_verdict", "parent-sign Z_BqWeyl_linear", "all parent signature clauses pass before local scoring", "ZERO_THEOREM_NOT_ACTIVATED_CURRENT_CORPUS", "3607 cannot parent-sign B_qWeyl=0 from current evidence", "gates_3606"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": audit_id,
            "clause": clause,
            "required_evidence": required,
            "current_status": current_status,
            "failure_if_open": failure,
            "source_path": p[source_id],
            "clause_passed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for audit_id, clause, required, current_status, failure, source_id in rows
    ]


def finite_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("BACQ3607_0_Z_linear", "Z_BqWeyl_linear", "theorem switch for linear B_qWeyl absence", "boolean", "CONDITIONAL_FALSE", "all PSA3607 parent-signature rows true", "index_lemma", "ZERO_SWITCH_NOT_LIVE"),
        ("BACQ3607_1_BqWeyl", "B_qWeyl", "parent coefficient for q P*C or equivalent q-Weyl mixing", "parent_normalized", "MISSING_PARENT_SIGNATURE_OR_NUMERIC_COEFFICIENT", "source path, sign, uncertainty, action normalization and no-spurion alternative", "first_source_input", "REQUIRED_FIRST_DANGEROUS"),
        ("BACQ3607_2_Zq", "Z_q", "q kinetic/operator normalization", "operator_normalization", "MISSING_Q_OPERATOR_NORMALIZATION", "q local action Hessian, q-X bridge, or no-pole deletion certificate", "dqweyl2_inputs", "REQUIRED_SHARED_Q_OPERATOR"),
        ("BACQ3607_3_Mq_lambda", "M_q^2_or_lambda_q", "q range/mass gap for Yukawa/local response", "length_or_mass_units", "MISSING_RANGE_OR_NO_POLE_THEOREM", "same normalization as Z_q and branch boundary condition", "dqweyl2_inputs", "REQUIRED_IF_NOT_MASSLESS"),
        ("BACQ3607_4_CWeyl_profile", "C_Weyl_local_profile", "local Weyl/tidal curvature source profile", "length^-2_or_declared_norm", "MISSING_DOMAIN_PROFILE", "source geometry, local branch domain, finite body/interior convention and no point-particle shortcut", "bound_nonclaim_2302", "REQUIRED_PROFILE_INPUT"),
        ("BACQ3607_5_tau_R10", "tau_BqWeyl_R10", "projection into R10/contact/short-range branch", "arena_specific", "MISSING_R10_PROJECTION", "q profile to alpha/lambda or contact residual convention; real bound curve if claim-bound", "first_source_input", "REQUIRED_ARENA_PROJECTION"),
        ("BACQ3607_6_tau_PPN", "tau_BqWeyl_PPN", "projection into PPN gamma/beta/preferred-frame residuals", "arena_specific", "MISSING_PPN_PROJECTION", "metric/readout/backreaction kernel and no-other-channel proof", "ppn_kernel", "REQUIRED_ARENA_PROJECTION"),
        ("BACQ3607_7_tau_clock", "tau_BqWeyl_clock", "projection into clock/redshift/frequency drift", "arena_specific", "MISSING_CLOCK_PROJECTION", "clock-standard quotient descent and q-Weyl response kernel", "first_source_input", "REQUIRED_ARENA_PROJECTION"),
        ("BACQ3607_8_tau_orbital", "tau_BqWeyl_orbital", "projection into orbital precession/source-GM residual", "arena_specific", "MISSING_ORBITAL_PROJECTION", "orbital readout map, source geometry and no fitted-GM laundering", "first_source_input", "REQUIRED_ARENA_PROJECTION"),
        ("BACQ3607_9_DqWeyl2_guard", "D_qWeyl2", "quadratic Weyl/higher-curvature guard", "length_squared_or_parent_normalized", "RETAIN_NONCLAIM_RESIDUAL", "no-higher-curvature/no-tower theorem or finite D_qWeyl2 coefficient/operator rows", "dqweyl2_inputs", "SEPARATE_GUARD_REQUIRED"),
        ("BACQ3607_10_C2_projection", "C2_Schw_or_source_C2", "Schwarzschild/exterior C_abcd C^abcd projection identity", "length^-4", "ANALYTIC_KERNEL_READY_INPUTS_MISSING", "D_qWeyl2, Z_q, lambda_q, boundary condition and observable map", "weyl2_projection", "GUARD_KERNEL_NONCLAIM"),
        ("BACQ3607_11_acceptance_rule", "E_BqWeyl_acceptance", "E_BqWeyl can leave epsilon_Dq_vq only by zero switch or complete finite row pack", "boolean", "CLAIM_REFUSED", "Z_BqWeyl_linear=true or every finite input row source-backed, unit-matched and arena-projected", "bounds_3606", "ACCEPTANCE_GATE"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "input_id": input_id,
            "symbol": symbol,
            "role": role,
            "units": units,
            "current_value": value,
            "required_to_promote": required,
            "source_path": p[source_id],
            "status": status,
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for input_id, symbol, role, units, value, required, source_id, status in rows
    ]


def activation_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("ACT3607_0_index_theorem_available", "linear index lemma", "PASS_CONDITIONAL", "metric/epsilon-only one-Weyl terms vanish", "index_lemma"),
        ("ACT3607_1_parent_signature", "parent no-spurion signature", "FAIL_CURRENT_CLAIM", "all parent signature clauses are unsigned or missing", "parent_signature_gate"),
        ("ACT3607_2_finite_inputs", "finite BqWeyl input pack", "FAIL_CURRENT_CLAIM", "B_qWeyl, Z_q/G_q, C_Weyl profile and arena projections are missing", "first_source_input"),
        ("ACT3607_3_DqWeyl2_guard", "D_qWeyl2 guard", "PASS_GUARD", "quadratic Weyl remains separate and unpromoted", "dqweyl2_inputs"),
        ("ACT3607_4_no_local_vacuum_shortcut", "no local-vacuum shortcut", "PASS_GUARD", "Weyl/tidal curvature survives exterior vacuum", "first_source_input"),
        ("ACT3607_5_no_epsilonDq_vq_cleanup", "epsilon_Dq_vq cleanup", "FAIL_CURRENT_CLAIM", "E_BqWeyl cannot leave epsilon_Dq_vq", "status_3606"),
        ("ACT3607_6_next_route", "next route selected", "PASS_ROUTE_SELECTED", "q operator normalization is the shared finite-path bottleneck", "dqweyl2_inputs"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "consequence": consequence,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, consequence, source_id in rows
    ]


def status_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "BQWEYL_PARENT_SIGNATURE_FAILED_FINITE_INPUT_PACK_STAGED",
            "strongest_result": "3607 audits the no-Weyl-spurion route clause-by-clause and finds it is not parent-signed. It stages the finite BqWeyl acquisition pack: B_qWeyl, Z_q/G_q, M_q/lambda_q, C_Weyl profile, arena projections, units, and D_qWeyl2 guard.",
            "decision": "do not promote B_qWeyl=0; do not score a finite bound yet; move next to q-operator normalization because it is shared by B_qWeyl and D_qWeyl2 finite routes",
            "still_missing": "parent typed grammar, object-language exhaustion, q representation, no Pabcd spurion/projector/readout, hidden-frame exclusion, curvature morphism exclusion, B_qWeyl coefficient, Z_q/G_q, M_q/lambda_q, C_Weyl profile, R10/PPN/clock/orbital projections and D_qWeyl2 no-tower closure",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["first_source_input"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3607_0",
            "target_doc": "3608-Y5-R2FR-q-operator-normalization-or-BqWeyl-bound-runner-blocker.md",
            "target_script": "scripts/Y5_R2FR_3608_q_operator_normalization_or_BqWeyl_bound_runner_blocker.py",
            "objective": "try to derive or source Z_q/G_q and the q operator domain/norm shared by B_qWeyl and D_qWeyl2; if not, keep the finite Weyl bound runner blocked with exact missing inputs",
            "success_gate": "finite BqWeyl or D_qWeyl2 scoring cannot start until q operator normalization, domain, boundary condition and norm convention are parent-owned or source-backed",
            "reason": "3607 shows parent no-spurion is not live and finite BqWeyl inputs are staged; Z_q/G_q is the shared bottleneck for any numeric Weyl route",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_map: dict[str, tuple[Path, str]],
    out_paths: dict[str, Path],
    signature: list[dict[str, object]],
    finite: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(("VAL3607_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3607 source paths exist"))
    validations.append(("VAL3607_1_needles_found", all(path.exists() and contains(path, needle) for path, needle in source_map.values()), "all selected 3607 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3607_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3607 csv output files written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3607_3_csv_parse", parse_ok, "; ".join(parse_details)))
    required_signature = {
        "parent typed object-language",
        "object-language exhaustion",
        "q scalar/quotient/pure-density representation",
        "no Weyl spurion/projector/readout kernel",
        "hidden frame exclusion",
        "curvature morphism exclusion",
        "quadratic/higher-curvature tower exclusion",
    }
    validations.append(("VAL3607_4_signature_audit_complete", required_signature.issubset({str(row["clause"]) for row in signature}), "parent signature audit covers all no-spurion clauses"))
    required_inputs = {"B_qWeyl", "Z_q", "M_q^2_or_lambda_q", "C_Weyl_local_profile", "tau_BqWeyl_R10", "tau_BqWeyl_PPN", "tau_BqWeyl_clock", "tau_BqWeyl_orbital", "D_qWeyl2"}
    validations.append(("VAL3607_5_finite_rows_present", required_inputs.issubset({str(row["symbol"]) for row in finite}), "finite BqWeyl acquisition rows present"))
    validations.append(("VAL3607_6_parent_signature_blocked", any(row["gate_id"] == "ACT3607_1_parent_signature" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "parent no-spurion signature remains blocked"))
    validations.append(("VAL3607_7_finite_inputs_blocked", any(row["gate_id"] == "ACT3607_2_finite_inputs" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "finite BqWeyl input pack remains blocked"))
    validations.append(("VAL3607_8_DqWeyl2_guard", any(row["gate_id"] == "ACT3607_3_DqWeyl2_guard" and row["status"] == "PASS_GUARD" for row in gates), "DqWeyl2 guard remains active"))
    validations.append(("VAL3607_9_next_target_selected", any(row["next_id"] == "NEXT3607_0" for row in next_target), "3608 q-operator target selected"))
    validations.append(("VAL3607_10_no_claim_flags", not any(str(row.get("valid_for_claim", "False")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true" for table in [signature, finite, gates, status] for row in table), "all generated physics rows remain nonclaim"))
    source_paths = [Path(str(row["source_path"])) for table in [signature, finite, gates, status] for row in table if row.get("source_path")]
    validations.append(("VAL3607_11_generated_source_paths_exist", all(path.exists() for path in source_paths), "every generated row source_path exists"))
    formal_hits = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*3607*"):
            if ".venv" in path.parts:
                continue
            if path.name.startswith("3607-") or path.name.startswith("Y5_R2FR_3607") or "P8_Y5_R2FR_3607" in path.name:
                formal_hits.append(path)
    validations.append(("VAL3607_12_formalization_workbench_untouched", len(formal_hits) == 0, "no 3607 checkpoint output appears in formalization-workbench outside package/venv noise"))
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
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


def write_doc(signature, finite, gates, status, next_target, validation) -> None:
    lines = [
        "# 3607 - BqWeyl parent signature or finite row acquisition",
        "",
        "## Verdict",
        "3607 does the boring-but-necessary gatekeeping: the no-Weyl-spurion zero route is strong, but it is not parent-signed in the current corpus.",
        "",
        "So `B_qWeyl=0` is not promoted.  The finite path is now staged as a real acquisition pack: `B_qWeyl`, `Z_q/G_q`, `M_q/lambda_q`, `C_Weyl` profile, `tau_arena` projections, units, and the `D_qWeyl2` guard.",
        "",
        "The shared bottleneck is now q-operator normalization.  Without `Z_q/G_q`, neither the linear `B_qWeyl` route nor the quadratic `D_qWeyl2` route can be scored.",
        "",
        "## Parent Signature Audit",
    ]
    for row in signature:
        lines.append(f"- `{row['audit_id']}` / `{row['clause']}`: {row['current_status']} - {row['failure_if_open']}")
    lines.extend(["", "## Finite Acquisition Rows"])
    for row in finite:
        lines.append(f"- `{row['input_id']}` / `{row['symbol']}`: {row['status']} - {row['role']}")
    lines.extend(["", "## Activation Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
        lines.append(f"- Decision: {row['decision']}")
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
    source_map = sources()
    out_paths = outputs()
    register = source_register_rows(source_map)
    signature = parent_signature_rows(source_map)
    finite = finite_rows(source_map)
    gates = activation_rows(source_map)
    status = status_rows(source_map)
    next_target = next_target_rows()

    write_csv(out_paths["source_register"], register)
    write_csv(out_paths["parent_signature_audit"], signature)
    write_csv(out_paths["finite_acquisition_rows"], finite)
    write_csv(out_paths["activation_gates"], gates)
    write_csv(out_paths["status"], status)
    write_csv(out_paths["next_target"], next_target)
    write_csv(out_paths["canonical_status"], status)

    validation = validation_rows(source_map, out_paths, signature, finite, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(signature, finite, gates, status, next_target, validation)

    print(f"wrote {DOC}")
    for output_id, path in out_paths.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()

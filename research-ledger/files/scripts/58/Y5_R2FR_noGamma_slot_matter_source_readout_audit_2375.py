from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_NOGAMMA_SLOT_MATTER_SOURCE_READOUT_AUDIT_2375"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2375-Y5-R2FR-noGamma-slot-matter-source-readout-audit.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    sources = [
        ("SRC2375_2374_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2374_NEXT_TARGET.csv", "NEXT2374_0_selected", "2374 selected no-Gamma slot audit"),
        ("SRC2375_2374_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2374_VALIDATION.csv", "VAL2374_OVERALL", "2374 validation"),
        ("SRC2375_2374_seed", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2374_NO_GAMMA_SLOT_AUDIT_SEED.csv", "NGS2374_6_verdict", "2374 no-Gamma sector seed"),
        ("SRC2375_2374_p4", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2374_P4_HYPERMOMENTUM_RESIDUAL_ROW.csv", "P4R2374_0_hypermomentum_total", "2374 P4 fallback row"),
        ("SRC2375_2334_slots", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2334_GAMMA_SLOT_SECTOR_AUDIT.csv", "NGSA2334_9_verdict", "2334 sector Gamma-slot audit"),
        ("SRC2375_2334_stack", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2334_NO_GAMMA_THEOREM_STACK.csv", "NGT2334_4_result", "2334 no-Gamma theorem stack"),
        ("SRC2375_2334_p4", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2334_P4_DELTA_COMPONENT_QUEUE.csv", "P4DQ2334_0_total", "2334 P4 component queue"),
        ("SRC2375_2334_decision", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2334_DECISION_LEDGER.csv", "DEC2334_2_best_next", "2334 decision ledger"),
        ("SRC2375_2334_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2334_NEXT_TARGET.csv", "NEXT2334_0", "2334 source/readout certificate target"),
        ("SRC2375_2334_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2334_VALIDATION.csv", "VAL2334_OVERALL", "2334 validation"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in sources:
        path = POST_ROOT / source_path
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": source_path,
                "needle": needle,
                "role": role,
                "path_exists": str(path.exists()).lower(),
                "needle_found": str(contains(path, needle)).lower(),
                "valid_for_claim": "false",
            }
        )
    return rows


def gamma_slot_sector_audit() -> list[dict[str, object]]:
    rows = [
        (
            "NGSA2375_0_stack_target",
            "total ordinary local branch",
            "Does S_total_ord contain an independent affine Gamma_ind argument anywhere in matter, source, clock, light, orbit, boundary or readout?",
            "EXACT_CONDITIONAL_THEOREM_STACK",
            "sector-by-sector parent argument list is not signed for source/readout/boundary/projective slots",
            "Delta_abs",
        ),
        (
            "NGSA2375_1_ordinary_matter",
            "ordinary matter",
            "Does ordinary matter use S_A[Psi_A,e_obs,omega_LC[e_obs],A_owned,theta_A] with no Gamma_ind?",
            "CONDITIONAL_SUPPORTED_BY_MUMC",
            "candidate source-blind/owned-coframe signature is private-not-derived and direct representative dependence still needs exclusion",
            "Delta_matter",
        ),
        (
            "NGSA2375_2_spinor_transport",
            "spinor and spin transport",
            "Is the spin connection omega_LC[e_obs] coframe-owned rather than an independent torsionful connection?",
            "CONDITIONAL_SPIN_GUARD_NOT_GLOBAL",
            "spin/torsion/nonmetricity alternatives are not parent-excluded for every ordinary sector",
            "Delta_spin",
        ),
        (
            "NGSA2375_3_EM_light",
            "EM and lightcone readout",
            "Does light/EM use owned gauge connection and metric null structure, not affine Gamma_ind?",
            "PARTIAL_GAUGE_OWNER_NOT_FULL_READOUT",
            "optical, Shapiro, ray and detector readout maps are not all written as downstream Gamma-free functionals",
            "Delta_light",
        ),
        (
            "NGSA2375_4_source_worldtube",
            "source mass and finite worldtube",
            "Does source support/GM/worldtube action contain no Gamma_ind, boundary torsion or source-only connection current?",
            "UNSIGNED_PRIMARY_LEAK_PATH",
            "finite-source boundary and measured-GM support map can still re-enter as non-Hilbert source current",
            "Delta_source",
        ),
        (
            "NGSA2375_5_clock_readout",
            "clock and frequency readout",
            "Are clocks downstream matter/gauge functionals of e_obs/g_obs and theta, not independent Gamma probes?",
            "UNSIGNED_READOUT_SLOT",
            "atomic clock, frequency transfer, synchronization and detector model argument lists are not parent-signed",
            "Delta_clock",
        ),
        (
            "NGSA2375_6_orbital_readout",
            "test-body and orbital readout",
            "Is orbital motion derived from the same LC/coframe action rather than an independent autoparallel Gamma_ind law?",
            "UNSIGNED_READOUT_SLOT",
            "geodesic/autoparallel choice and finite-body marker map remain explicit parent clauses to sign",
            "Delta_orbit",
        ),
        (
            "NGSA2375_7_boundary_domain",
            "boundary/domain/improvement terms",
            "Are boundary, domain and improvement terms either exact/projected silent or Gamma-free?",
            "UNSIGNED_PARALLEL_GATE",
            "worldtube flux, marker boundaries and improvement currents still need zero theorem or finite envelope",
            "Delta_boundary",
        ),
        (
            "NGSA2375_8_projective_trace",
            "projective trace",
            "Is the projective mode gauge, fixed, or unobservable in all source/readout sectors?",
            "UNSIGNED_PARALLEL_CAVEAT",
            "projective certificate/policy remains outside this no-Gamma proof",
            "Delta_projective",
        ),
        (
            "NGSA2375_9_verdict",
            "all sectors",
            "Can 2375 promote no-Gamma/no-hypermomentum for the whole local branch?",
            "NOT_PARENT_SIGNED_RETAIN_P4_COMPONENTS",
            "matter branch is promising, but source/readout/boundary/projective slots are still unsigned",
            "Delta_abs",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "sector": sector,
            "slot_question": question,
            "evidence_status": status,
            "open_gap": gap,
            "p4_component": component,
        }
        for row_id, sector, question, status, gap, component in rows
    ]


def no_gamma_theorem_stack() -> list[dict[str, object]]:
    rows = [
        (
            "NGT2375_0_variational_absence",
            "variable-absence lemma",
            "For an action S[y] whose domain excludes Gamma_ind, the functional derivative delta S / delta Gamma_ind is zero/vacuous in the reduced variable space.",
            "EXACT_MATH_CONDITIONAL",
            "sector action domain must actually exclude Gamma_ind",
        ),
        (
            "NGT2375_1_coframe_chain_rule",
            "coframe-owned connection lemma",
            "If omega_obs=omega_LC[e_obs], variation of omega is induced by variation of e_obs and is counted in the metric/coframe field equation, not an independent Gamma equation.",
            "EXACT_MATH_CONDITIONAL",
            "spinor and transport sectors must be explicitly written with omega_LC[e_obs]",
        ),
        (
            "NGT2375_2_sector_sum",
            "sector-sum lemma",
            "If each sector derivative delta S_i/delta Gamma_ind vanishes, then Delta_abs is zero without cancellation because every summand is individually zero.",
            "EXACT_MATH_CONDITIONAL",
            "all sector slots must be signed, not merely ordinary matter",
        ),
        (
            "NGT2375_3_no_reentry",
            "readout no-reentry lemma",
            "A readout map does not source Gamma if it is downstream of the variational problem and does not define an extra source-labelled action/current.",
            "CONDITIONAL_CONTRACT_NEEDED",
            "clock, light, orbit, boundary and marker maps need explicit downstream/no-current clauses",
        ),
        (
            "NGT2375_4_result",
            "2375 theorem result",
            "The no-Gamma theorem is mathematically sharp but remains a conditional branch until source/readout/boundary/projective slots are parent-signed or P4-bounded.",
            "CONDITIONAL_THEOREM_NOT_CORPUS_PROMOTED",
            "source/readout argument-list certificate or P4 component map",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "lemma": lemma,
            "statement": statement,
            "proof_status": status,
            "missing_parent_input": missing,
        }
        for row_id, lemma, statement, status, missing in rows
    ]


def p4_delta_component_queue() -> list[dict[str, object]]:
    rows = [
        (
            "P4DQ2375_0_total",
            "Delta_abs",
            "||Delta_matter|| + ||Delta_spin|| + ||Delta_source|| + ||Delta_clock|| + ||Delta_light|| + ||Delta_orbit|| + ||Delta_boundary|| + ||Delta_projective||",
            "all no-Gamma sector slots parent-signed",
            "MISSING_COMPONENT_ZERO_PROOFS_OR_BOUNDS",
            "hypermomentum norm or normalized arena-specific envelope",
        ),
        (
            "P4DQ2375_1_matter",
            "Delta_matter",
            "||delta S_matter / delta Gamma_ind||",
            "ordinary matter has no Gamma_ind slot",
            "ZERO_IF_PRIVATE_MUMC_BRANCH_ADOPTED_ELSE_BOUND",
            "hypermomentum norm",
        ),
        (
            "P4DQ2375_2_spin",
            "Delta_spin",
            "||spin/torsion/nonmetricity connection current||",
            "spin connection is omega_LC[e_obs] and no Einstein-Cartan/metric-affine branch is active",
            "MISSING_SPIN_BRANCH_EXCLUSION_OR_BOUND",
            "spin-current or normalized torsion envelope",
        ),
        (
            "P4DQ2375_3_source",
            "Delta_source",
            "||delta S_source/worldtube/GM / delta Gamma_ind||",
            "source support and GM calibration are downstream Hilbert/coframe functionals",
            "MISSING_SOURCE_WORLDTUBE_ARGUMENT_LIST",
            "source-current or normalized GM envelope",
        ),
        (
            "P4DQ2375_4_clock",
            "Delta_clock",
            "||delta S_clock/readout / delta Gamma_ind||",
            "clock model is downstream of Gamma-free matter/gauge action",
            "MISSING_CLOCK_ARGUMENT_LIST",
            "clock frequency residual envelope",
        ),
        (
            "P4DQ2375_5_light",
            "Delta_light",
            "||delta S_light/ray/detector / delta Gamma_ind||",
            "light propagation/readout uses owned EM and g_obs/LC null structure only",
            "MISSING_LIGHT_READOUT_ARGUMENT_LIST",
            "lightcone/Shapiro/deflection residual envelope",
        ),
        (
            "P4DQ2375_6_orbit",
            "Delta_orbit",
            "||delta S_orbit/test-body/readout / delta Gamma_ind||",
            "orbital readout is Hilbert matter motion in g_obs, not independent autoparallel law",
            "MISSING_ORBIT_ARGUMENT_LIST",
            "orbital/PPN residual envelope",
        ),
        (
            "P4DQ2375_7_boundary_projective",
            "Delta_boundary + Delta_projective",
            "||boundary/improvement Gamma current|| + ||projective trace coupling||",
            "compact support/improvement silence plus projective gauge/fixed/unobservable certificate",
            "MISSING_BOUNDARY_AND_PROJECTIVE_CERTIFICATE",
            "source-current or normalized projective envelope",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "component": component,
            "formal_definition": definition,
            "zero_switch": zero_switch,
            "status": status,
            "units": units,
        }
        for row_id, component, definition, zero_switch, status, units in rows
    ]


def decision_ledger() -> list[dict[str, object]]:
    rows = [
        (
            "DEC2375_0_theorem_result",
            "no-Gamma theorem is exact as a conditional sector-sum lemma",
            "variable absence plus coframe-owned connection gives zero hypermomentum without cancellation",
            "this is the right derivation route, not a numerical patch",
            "CONDITIONAL_MATH_READY",
        ),
        (
            "DEC2375_1_no_promotion",
            "do not promote Levi-Civita/no-hypermomentum yet",
            "source, clock, light, orbit, boundary and projective slots are not parent-signed",
            "retain P4 component queue and no public/local-GR claim",
            "RETAIN_P4_COMPONENTS",
        ),
        (
            "DEC2375_2_best_next",
            "write source/readout no-Gamma action-argument certificate next",
            "one explicit argument-list contract could close several leak paths at once",
            "if certificate fails, fill P4 Delta_source/clock/light/orbit units and maps",
            "SELECT_SOURCE_READOUT_ARGUMENT_LIST_NEXT",
        ),
        (
            "DEC2375_3_public_policy",
            "no GitHub evidence update from this checkpoint",
            "2375 is a private derivation/fallback gate, not a publishable GR-reduction result",
            "keep working in post-checkpoint-work",
            "NO_GITHUB_EVIDENCE_UPDATE",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, decision, reason, consequence, status in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2375_0_no_gamma_active", "no-Gamma branch parent-signed for all sectors", "FAIL", "conditional theorem only"),
        ("CG2375_1_no_hypermomentum", "Delta_lambda^{mu nu}=0 for ordinary local branch", "FAIL", "source/readout slots unsigned"),
        ("CG2375_2_Levi_Civita", "Gamma_obs=LC(g_obs), T=0, Q=0 derived", "FAIL", "needs no-Gamma plus EH/Palatini/projective closure"),
        ("CG2375_3_P4_score", "P4 Delta components have numeric units/maps/bounds", "FAIL", "component queue only"),
        ("CG2375_4_local_GR_Newton", "local GR/Newton recovery derived", "FAIL", "connection and EH/GM gates still open"),
        ("CG2375_5_github_public_update", "safe to push as public evidence", "FAIL", "private checkpoint only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "gate_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, gate, status, effect in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2375_0_conditional_as_active", "the no-Gamma theorem is now active in MTS", "false", "the theorem shape is proved but the sector argument list is not parent-signed"),
        ("REF2375_1_matter_closes_readout", "ordinary matter no-Gamma automatically closes clocks, light and orbits", "false", "readout maps can re-enter as source-labelled currents unless explicitly downstream/Gamma-free"),
        ("REF2375_2_ignore_source_worldtube", "source/worldtube Gamma slot can be ignored", "false", "Newton/GM matching depends on source support and finite-boundary behavior"),
        ("REF2375_3_p4_as_pass", "the P4 queue is an empirical pass", "false", "P4 rows still lack component values, units, projection kernels and arena bounds"),
        ("REF2375_4_github", "publish this as GR reduction evidence", "false", "2375 is a private structural audit; it does not close local GR/Newton"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "claim": claim,
            "allowed": allowed,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, claim, allowed, reason in rows
    ]


def next_target() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT2375_0_selected",
            "2376-Y5-R2FR-source-readout-noGamma-action-argument-certificate.md",
            "scripts/Y5_R2FR_source_readout_noGamma_action_argument_certificate_2376.py",
            "explicitly list source, clock, light, orbit, boundary and readout action arguments and prove none contain Gamma_ind",
            "if any slot remains open, convert it to a P4 Delta component with units and projection map",
        ),
        (
            "NEXT2375_1_fallback",
            "2376b-Y5-R2FR-P4-Delta-component-values-units-map.md",
            "scripts/Y5_R2FR_P4_Delta_component_values_units_map_2376b.py",
            "fill Delta_source/clock/light/orbit/boundary/projective components, units, weak-field map and arena bounds",
            "keep nonclaim until all source paths and same-frame projections are present",
        ),
        (
            "NEXT2375_2_parallel",
            "2376c-Y5-R2FR-projective-trace-certificate-or-policy.md",
            "scripts/Y5_R2FR_projective_trace_certificate_or_policy_2376c.py",
            "prove projective trace is gauge, fixed, or unobservable across source/readout sectors",
            "otherwise retain projective residual policy",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "next_file": file_name,
            "next_script": script_name,
            "success_condition": success,
            "fallback_condition": fallback,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, file_name, script_name, success, fallback in rows
    ]


def all_output_files() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_2375_SOURCE_REGISTER.csv",
        "gamma_slot_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_2375_GAMMA_SLOT_SECTOR_AUDIT.csv",
        "theorem_stack": RESIDUALS / "P8_Y5_PARENT_QLOC_2375_NO_GAMMA_THEOREM_STACK.csv",
        "p4_delta_queue": RESIDUALS / "P8_Y5_PARENT_QLOC_2375_P4_DELTA_COMPONENT_QUEUE.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_2375_DECISION_LEDGER.csv",
        "claim_gates": RESIDUALS / "P8_Y5_PARENT_QLOC_2375_CLAIM_GATES.csv",
        "refusal_runner": RESIDUALS / "P8_Y5_PARENT_QLOC_2375_REFUSAL_RUNNER.csv",
        "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_2375_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2375_VALIDATION.csv",
    }


def check_no_positive_claim_flags(paths: list[Path]) -> bool:
    sensitive = {
        "parent_signed",
        "theorem_zero",
        "numeric_prediction_present",
        "same_branch_locked",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "passes_public_claim",
        "local_gr_claim",
        "epsilon_zero_active",
        "vector_complete",
    }
    positive_values = {"true", "pass", "passed", "ready", "yes", "1"}
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in sensitive and str(value).strip().lower() in positive_values:
                    return False
    return True


def validation_rows(outputs: dict[str, Path]) -> list[dict[str, object]]:
    source_rows = read_csv(outputs["source_register"])
    generated_paths = [path for key, path in outputs.items() if key != "validation"]
    parsed_ok = True
    for path in generated_paths:
        try:
            parsed_ok = parsed_ok and bool(read_csv(path))
        except Exception:
            parsed_ok = False

    slots = read_csv(outputs["gamma_slot_audit"])
    theorem = read_csv(outputs["theorem_stack"])
    p4 = read_csv(outputs["p4_delta_queue"])
    decisions = read_csv(outputs["decision_ledger"])
    gates = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])

    checks = [
        ("VAL2375_00_required_sources_exist", all(row["path_exists"] == "true" for row in source_rows), "all required source paths exist"),
        ("VAL2375_01_required_needles_found", all(row["needle_found"] == "true" for row in source_rows), "all source needles found"),
        ("VAL2375_02_outputs_exist", all(path.exists() for path in generated_paths), "all 2375 output files written"),
        ("VAL2375_03_csv_parse", parsed_ok, "all generated CSV files parse and contain rows"),
        (
            "VAL2375_04_conditional_theorem_stack",
            any(row["row_id"] == "NGT2375_4_result" and row["proof_status"] == "CONDITIONAL_THEOREM_NOT_CORPUS_PROMOTED" for row in theorem),
            "conditional theorem result recorded without promotion",
        ),
        (
            "VAL2375_05_sector_slots_present",
            len(slots) >= 10 and any(row["row_id"] == "NGSA2375_9_verdict" for row in slots),
            "major matter/source/readout slots present",
        ),
        (
            "VAL2375_06_no_promotion",
            any(row["row_id"] == "NGSA2375_9_verdict" and row["evidence_status"].startswith("NOT_PARENT_SIGNED") for row in slots),
            "no-Gamma branch not promoted",
        ),
        (
            "VAL2375_07_p4_components_present",
            len(p4) >= 8 and any(row["row_id"] == "P4DQ2375_0_total" for row in p4),
            "P4 component queue covers matter/source/readout/boundary",
        ),
        (
            "VAL2375_08_next_certificate_selected",
            any(row["row_id"] == "DEC2375_2_best_next" and row["status"] == "SELECT_SOURCE_READOUT_ARGUMENT_LIST_NEXT" for row in decisions)
            and any(row["row_id"] == "NEXT2375_0_selected" for row in next_rows),
            "source/readout argument-list certificate selected next",
        ),
        (
            "VAL2375_09_local_claims_block",
            any(row["row_id"] == "CG2375_4_local_GR_Newton" and row["gate_status"] == "FAIL" for row in gates),
            "local GR/Newton claim gate remains false",
        ),
        (
            "VAL2375_10_no_positive_claim_flags",
            check_no_positive_claim_flags(generated_paths),
            "all generated claim/readiness flags remain negative",
        ),
        (
            "VAL2375_11_formalization_untouched",
            not any(FORMALIZATION_WORKBENCH in path.parents for path in generated_paths),
            "generator writes only under post-checkpoint-work",
        ),
    ]
    rows = [
        {
            "row_id": row_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, ok, detail in checks
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2375_OVERALL",
            "status": "PASS" if overall_ok else "FAIL",
            "detail": "2375 valid: no-Gamma theorem sharpened as conditional sector-sum audit, P4 components retained, source/readout argument certificate selected next"
            if overall_ok
            else "2375 validation failed",
            "valid_for_claim": "false",
        }
    )
    return rows


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    slots = read_csv(outputs["gamma_slot_audit"])
    theorem = read_csv(outputs["theorem_stack"])
    p4 = read_csv(outputs["p4_delta_queue"])
    decisions = read_csv(outputs["decision_ledger"])
    gates = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])
    generated = [rel(path) for path in outputs.values()]

    text = f"""# 2375 - noGamma Slot Matter Source Readout Audit

## Result

The no-Gamma route is mathematically clean but not yet active.

The conditional theorem is:

If every ordinary/local sector has no independent `Gamma_ind` argument, then every `delta S_i / delta Gamma_ind` vanishes by variable absence, and `Delta_abs=0` without cancellation.

The ordinary matter branch is promising inside the private MUMC/owned-coframe branch, but the source/worldtube, clock, light, orbit, boundary and projective trace slots are not parent-signed.  Therefore Levi-Civita/no-hypermomentum/local-GR are **not** promoted here.

The useful gain is that the next target is now concrete: write the source/readout action-argument certificate.  If that certificate fails, the same rows become P4 component bounds.

## Gamma Slot Sector Audit

{md_table(slots, ["row_id", "sector", "evidence_status", "open_gap", "p4_component"])}

## no-Gamma Theorem Stack

{md_table(theorem, ["row_id", "lemma", "proof_status", "missing_parent_input"])}

## P4 Delta Component Queue

{md_table(p4, ["row_id", "component", "status", "zero_switch"])}

## Decision Ledger

{md_table(decisions, ["row_id", "decision", "status", "consequence"])}

## Claim Gates

{md_table(gates, ["row_id", "gate", "gate_status", "claim_effect"])}

## Next Target

{md_table(next_rows, ["row_id", "next_file", "success_condition", "fallback_condition"])}

## Generated Files

"""
    text += "\n".join(f"- `{path}`" for path in generated)
    text += """

## Practical Status

This is the cleanest version of the connection route so far.  We are no longer arguing vaguely about whether MTS "has GR"; we are auditing the action arguments sector by sector.  If the next certificate closes, the spin/torsion connection gate gets much cleaner.  If it fails, P4 becomes the honest residual branch.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    outputs = all_output_files()
    write_csv(outputs["source_register"], source_register())
    write_csv(outputs["gamma_slot_audit"], gamma_slot_sector_audit())
    write_csv(outputs["theorem_stack"], no_gamma_theorem_stack())
    write_csv(outputs["p4_delta_queue"], p4_delta_component_queue())
    write_csv(outputs["decision_ledger"], decision_ledger())
    write_csv(outputs["claim_gates"], claim_gates())
    write_csv(outputs["refusal_runner"], refusal_runner())
    write_csv(outputs["next_target"], next_target())
    write_csv(outputs["validation"], validation_rows(outputs))
    write_doc(outputs)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {outputs['validation']}")


if __name__ == "__main__":
    main()

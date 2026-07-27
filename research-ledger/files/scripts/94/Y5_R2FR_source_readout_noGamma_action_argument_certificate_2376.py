from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_SOURCE_READOUT_NOGAMMA_ARGUMENT_CERTIFICATE_2376"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2376-Y5-R2FR-source-readout-noGamma-action-argument-certificate.md"
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
        ("SRC2376_2375_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2375_NEXT_TARGET.csv", "NEXT2375_0_selected", "2375 selected SRNG argument certificate"),
        ("SRC2376_2375_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2375_VALIDATION.csv", "VAL2375_OVERALL", "2375 validation"),
        ("SRC2376_2375_slots", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2375_GAMMA_SLOT_SECTOR_AUDIT.csv", "NGSA2375_9_verdict", "2375 no-Gamma slot audit"),
        ("SRC2376_2335_certificate", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2335_SOURCE_READOUT_ARGUMENT_CERTIFICATE.csv", "SRNG2335_6_verdict", "2335 SRNG certificate"),
        ("SRC2376_2335_theorem", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2335_SRNG_THEOREM_ATTEMPT.csv", "THM2335_3_SRNG_sum", "2335 SRNG theorem attempt"),
        ("SRC2376_2335_p4", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2335_P4_DELTA_STATUS_AFTER_SRNG.csv", "P4S2335_6_reduced_total", "2335 P4 status after SRNG"),
        ("SRC2376_2335_decision", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2335_DECISION_LEDGER.csv", "DEC2335_2_best_next", "2335 decision ledger"),
        ("SRC2376_2335_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2335_NEXT_TARGET.csv", "NEXT2335_0", "2335 downstream functor target"),
        ("SRC2376_2335_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2335_VALIDATION.csv", "VAL2335_OVERALL", "2335 validation"),
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


def srng_argument_certificate() -> list[dict[str, object]]:
    rows = [
        (
            "SRNG2376_0_total_clause",
            "total source/readout branch",
            "parent-action restriction",
            "S_source uses Psi_src,e_obs,omega_LC[e_obs],A_owned,theta_src; O_clock/O_light/O_orbit/O_readout are downstream functors of solved observed fields",
            "Gamma_ind; source-only affine current; fitted readout mask inside variation; independent autoparallel law",
            "Source-Readout No-Gamma (SRNG): no source/readout object appears in the variational action with Gamma_ind as an argument.",
            "CERTIFICATE_WRITTEN_NOT_PARENT_SIGNED",
            "Delta_source+Delta_clock+Delta_light+Delta_orbit",
            "parent adoption or deeper quotient/naturality derivation",
        ),
        (
            "SRNG2376_1_source_worldtube",
            "source worldtube and GM support",
            "source action / support selector",
            "W_source=closure(supp J_H[tau]); J_H from same Hilbert/coframe matter action; compact support and fixed linking surfaces",
            "Gamma_ind current; fitted radius/source mask; boundary torsion; post-readout GM rescaling",
            "source support is selected from the Hilbert current of the same Gamma-free matter action, not by a new connection-sensitive source law",
            "CONDITIONAL_FROM_WORLDTUBE_SELECTOR_NOT_SIGNED",
            "Delta_source",
            "compactness, boundary/reference lock, M_H_ref and coupling descent are not parent-signed",
        ),
        (
            "SRNG2376_2_clock",
            "clock and frequency readout",
            "downstream observation functor",
            "O_clock[solution fields, e_obs, A_owned, theta_clock, tau]",
            "Gamma_ind probe term; source-labelled clock current; separate clock frame",
            "clock readout is not a term in S_ord; it reads the same solved observed coframe/gauge branch",
            "CONTRACT_FORM_WRITTEN_NOT_PARENT_SIGNED",
            "Delta_clock",
            "clock model and tau/frame lock still need explicit parent signature",
        ),
        (
            "SRNG2376_3_light",
            "light, EM, Shapiro and deflection readout",
            "EM action plus downstream null/ray readout",
            "A_owned, e_obs/g_obs, omega_LC[e_obs], detector constants; WKB/null readout after variation",
            "affine Gamma_ind as optical connection; independent ray-autoparallel postulate",
            "light propagation is owned by EM/gauge plus metric/coframe readout, not by an independent affine connection",
            "CONTRACT_FORM_WRITTEN_NOT_PARENT_SIGNED",
            "Delta_light",
            "Maxwell/WKB and detector readout need parent-side statement in MTS language",
        ),
        (
            "SRNG2376_4_orbit",
            "orbital/test-body readout",
            "test-body limit / downstream trajectory readout",
            "point/compact body action from same e_obs/g_obs matter branch; trajectory readout after variation",
            "independent Gamma_ind autoparallel law; fitted orbit frame; marker current inside source variation",
            "test-body motion must be the limit of Hilbert/coframe matter, not an added affine-autoparallel rule",
            "CONTRACT_FORM_WRITTEN_NOT_PARENT_SIGNED",
            "Delta_orbit",
            "test-body reduction and marker/domain map still need parent certificate",
        ),
        (
            "SRNG2376_5_boundary",
            "boundary/domain/improvement",
            "support and integration boundary policy",
            "fixed compact support, exact/projected-silent improvement, fixed reference boundary data",
            "Gamma-sensitive boundary current; readout-selected domain; cancellation by sign",
            "boundary terms do not enter Delta_abs if compact support and improvement flux are parent-fixed or projected exact",
            "NOT_CLOSED_REQUIRES_SEPARATE_BOUNDARY_CERTIFICATE",
            "Delta_boundary",
            "worldtube flux and improvement current zero theorem/bound is still live",
        ),
        (
            "SRNG2376_6_verdict",
            "all source/readout sectors",
            "certificate verdict",
            "source/readout can be made Gamma-free by SRNG as a single parent clause",
            "calling SRNG derived before quotient/naturality or parent adoption is signed",
            "SRNG is a clean parent-action contract that would zero Delta_source/clock/light/orbit, but it is not yet derived from deeper MTS primitives",
            "PARTIAL_CERTIFICATE_READY_NOT_DERIVED",
            "conditional: Delta_source+Delta_clock+Delta_light+Delta_orbit",
            "derive SRNG from quotient/naturality or adopt it as a private working parent clause; boundary/projective remain separate",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "sector": sector,
            "object_type": obj_type,
            "allowed_arguments": allowed,
            "forbidden_arguments": forbidden,
            "certificate_clause": clause,
            "status": status,
            "closes_delta": closes,
            "remaining_gap": gap,
        }
        for row_id, sector, obj_type, allowed, forbidden, clause, status, closes, gap in rows
    ]


def srng_theorem_attempt() -> list[dict[str, object]]:
    rows = [
        (
            "THM2376_0_downstream_readout",
            "downstream readout lemma",
            "If O_i is evaluated after solving the variational problem and is not an action/current term, then O_i does not contribute delta S/delta Gamma_ind.",
            "EXACT_CONDITIONAL_LEMMA",
            "must prove clocks/light/orbits are downstream functors, not hidden action/source terms",
        ),
        (
            "THM2376_1_hilbert_source_selector",
            "Hilbert source selector lemma",
            "If W_source is selected from the support of the Hilbert current of the same Gamma-free matter action, it introduces no independent Gamma source current.",
            "EXACT_CONDITIONAL_LEMMA",
            "compactness, M_H_ref, boundary/reference lock and same-frame tau are unsigned",
        ),
        (
            "THM2376_2_orbit_test_body",
            "test-body no-autoparallel lemma",
            "If test-body motion is a limit of the same Hilbert/coframe matter action, an independent Gamma_ind autoparallel law is inadmissible.",
            "EXACT_CONDITIONAL_LEMMA",
            "test-body limit and marker/domain maps must be written in parent variables",
        ),
        (
            "THM2376_3_SRNG_sum",
            "SRNG zero sum",
            "Under SRNG plus the no-Gamma matter branch, Delta_source=Delta_clock=Delta_light=Delta_orbit=0 without cancellation.",
            "CONDITIONAL_THEOREM_READY",
            "SRNG is written here as a contract, not derived or adopted as active MTS parent action",
        ),
        (
            "THM2376_4_boundary_warning",
            "boundary warning",
            "SRNG does not by itself kill boundary/improvement/projective trace residuals unless those are separately fixed, exact, gauge, or bounded.",
            "LIMIT_EXPLICIT",
            "Delta_boundary and Delta_projective remain live",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "claim_piece": piece,
            "statement": statement,
            "result": result,
            "obstruction": obstruction,
        }
        for row_id, piece, statement, result, obstruction in rows
    ]


def p4_status_after_srng() -> list[dict[str, object]]:
    rows = [
        ("P4S2376_0_source", "Delta_source", "ZERO_IF_SRNG_PARENT_SIGNED_ELSE_BOUND", "SRNG_CONTRACT_NOT_SIGNED", "source/worldtube no-Gamma adoption or finite source-current bound"),
        ("P4S2376_1_clock", "Delta_clock", "ZERO_IF_DOWNSTREAM_CLOCK_FUNCTOR_SIGNED_ELSE_BOUND", "CLOCK_ARGUMENT_LIST_NOT_SIGNED", "clock readout parent functor or frequency residual bound"),
        ("P4S2376_2_light", "Delta_light", "ZERO_IF_EM_LIGHT_READOUT_SIGNED_ELSE_BOUND", "LIGHT_ARGUMENT_LIST_NOT_SIGNED", "EM/WKB/null readout certificate or PPN light bound"),
        ("P4S2376_3_orbit", "Delta_orbit", "ZERO_IF_TEST_BODY_LIMIT_SIGNED_ELSE_BOUND", "ORBIT_ARGUMENT_LIST_NOT_SIGNED", "test-body/marker parent map or orbital residual bound"),
        ("P4S2376_4_boundary", "Delta_boundary", "STILL_OPEN_SEPARATE_CERTIFICATE", "BOUNDARY_ZERO_OR_BOUND_MISSING", "boundary no-flux/improvement theorem or source-backed bound"),
        ("P4S2376_5_projective", "Delta_projective", "STILL_OPEN_PARALLEL_CERTIFICATE", "PROJECTIVE_TRACE_POLICY_MISSING", "projective gauge/fixed/unobservable certificate or residual policy"),
        ("P4S2376_6_reduced_total", "Delta_abs_reduced", "IF_SRNG_AND_MATTER_BRANCH_SIGNED_THEN_REDUCE_TO_DELTA_SPIN_BOUNDARY_PROJECTIVE", "REDUCTION_CONDITIONAL_ONLY", "SRNG adoption plus spin/boundary/projective closure"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "component": component,
            "status_after_SRNG": status_after,
            "current_status": current,
            "needed_for_score": needed,
        }
        for row_id, component, status_after, current, needed in rows
    ]


def decision_ledger() -> list[dict[str, object]]:
    rows = [
        (
            "DEC2376_0_SRNG_contract",
            "SRNG source-readout no-Gamma contract is now explicit",
            "it forbids Gamma_ind in source/readout actions and keeps clocks/light/orbits downstream",
            "several leak paths can close together if adopted or derived",
            "CONTRACT_READY_NONCLAIM",
        ),
        (
            "DEC2376_1_no_public_promotion",
            "do not promote SRNG as current MTS theorem",
            "contract is written but not derived from deeper quotient/naturality or adopted in formal spine",
            "no local-GR/Newton/WEP/PPN claim",
            "NO_PROMOTION",
        ),
        (
            "DEC2376_2_best_next",
            "try to derive downstream observation functor naturality next",
            "if q/naturality forces readouts downstream, SRNG becomes less axiomatic",
            "otherwise adopt SRNG privately or fill P4 component bounds",
            "SELECT_DOWNSTREAM_FUNCTOR_DERIVATION_NEXT",
        ),
        (
            "DEC2376_3_public_policy",
            "no GitHub evidence update",
            "this is a private contract/derivation gate",
            "continue in post-checkpoint-work",
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
        ("CG2376_0_SRNG_active", "SRNG active in parent action", "FAIL", "contract only"),
        ("CG2376_1_source_readout_zero", "Delta_source/clock/light/orbit theorem-zero", "FAIL", "zero only if SRNG parent-signed"),
        ("CG2376_2_boundary_projective", "boundary/projective residuals closed", "FAIL", "still open"),
        ("CG2376_3_P4_score", "P4 components score-ready", "FAIL", "no numeric units/maps/bounds yet"),
        ("CG2376_4_local_GR_Newton", "local GR/Newton recovery derived", "FAIL", "connection/EH/GM gates remain"),
        ("CG2376_5_github", "safe public evidence update", "FAIL", "private checkpoint only"),
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
        ("REF2376_0_contract_as_derivation", "SRNG is derived from MTS now", "false", "2376 writes the exact contract but does not derive it from deeper q/naturality"),
        ("REF2376_1_ignore_boundary", "source/readout no-Gamma also closes boundary/projective terms", "false", "boundary/improvement and projective trace are separate residual channels"),
        ("REF2376_2_autoparallel_import", "orbits use LC because GR says so", "false", "test-body motion must be derived as the Hilbert/coframe matter limit or residualized"),
        ("REF2376_3_local_gr", "2376 proves local GR/Newton", "false", "SRNG would close one connection subgate only; EH, GM normalization, boundary and projective gates remain"),
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
            "NEXT2376_0_selected",
            "2377-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md",
            "scripts/Y5_R2FR_downstream_observation_functor_naturality_or_SRNG_adoption_2377.py",
            "prove clocks/light/orbits/readouts are downstream natural functors of q-observed solved fields, not new source-current arguments",
            "if not derived, retain SRNG as private branch contract or fill P4 component bounds",
        ),
        (
            "NEXT2376_1_parallel",
            "2377b-Y5-R2FR-boundary-projective-residual-split.md",
            "scripts/Y5_R2FR_boundary_projective_residual_split_2377b.py",
            "split boundary/improvement and projective trace into independent zero/bound policies",
            "retain E_boundary/Delta_projective residuals if unsigned",
        ),
        (
            "NEXT2376_2_fallback",
            "2377c-Y5-R2FR-P4-source-readout-component-bounds.md",
            "scripts/Y5_R2FR_P4_source_readout_component_bounds_2377c.py",
            "fill Delta_source/clock/light/orbit units, weak-field maps and source-backed bounds",
            "keep nonclaim until same-frame and source-backed",
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
        "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_2376_SOURCE_REGISTER.csv",
        "srng_certificate": RESIDUALS / "P8_Y5_PARENT_QLOC_2376_SOURCE_READOUT_ARGUMENT_CERTIFICATE.csv",
        "srng_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_2376_SRNG_THEOREM_ATTEMPT.csv",
        "p4_status": RESIDUALS / "P8_Y5_PARENT_QLOC_2376_P4_DELTA_STATUS_AFTER_SRNG.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_2376_DECISION_LEDGER.csv",
        "claim_gates": RESIDUALS / "P8_Y5_PARENT_QLOC_2376_CLAIM_GATES.csv",
        "refusal_runner": RESIDUALS / "P8_Y5_PARENT_QLOC_2376_REFUSAL_RUNNER.csv",
        "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_2376_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2376_VALIDATION.csv",
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

    cert = read_csv(outputs["srng_certificate"])
    theorem = read_csv(outputs["srng_theorem"])
    p4 = read_csv(outputs["p4_status"])
    decisions = read_csv(outputs["decision_ledger"])
    gates = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])

    checks = [
        ("VAL2376_00_required_sources_exist", all(row["path_exists"] == "true" for row in source_rows), "all required source paths exist"),
        ("VAL2376_01_required_needles_found", all(row["needle_found"] == "true" for row in source_rows), "all source needles found"),
        ("VAL2376_02_outputs_exist", all(path.exists() for path in generated_paths), "all 2376 output files written"),
        ("VAL2376_03_csv_parse", parsed_ok, "all generated CSV files parse and contain rows"),
        (
            "VAL2376_04_SRNG_written",
            any(row["row_id"] == "SRNG2376_0_total_clause" and row["status"] == "CERTIFICATE_WRITTEN_NOT_PARENT_SIGNED" for row in cert),
            "SRNG total contract written as nonclaim",
        ),
        (
            "VAL2376_05_SRNG_not_promoted",
            any(row["row_id"] == "SRNG2376_6_verdict" and row["status"].endswith("NOT_DERIVED") for row in cert),
            "SRNG not promoted as derived",
        ),
        (
            "VAL2376_06_theorem_limits",
            any(row["row_id"] == "THM2376_4_boundary_warning" and row["result"] == "LIMIT_EXPLICIT" for row in theorem),
            "boundary/projective limitation explicit",
        ),
        (
            "VAL2376_07_p4_status_components",
            len(p4) >= 7 and any(row["row_id"] == "P4S2376_6_reduced_total" for row in p4),
            "source/readout/boundary/projective P4 status rows present",
        ),
        (
            "VAL2376_08_next_derivation_selected",
            any(row["row_id"] == "DEC2376_2_best_next" and row["status"] == "SELECT_DOWNSTREAM_FUNCTOR_DERIVATION_NEXT" for row in decisions)
            and any(row["row_id"] == "NEXT2376_0_selected" for row in next_rows),
            "downstream observation functor derivation selected next",
        ),
        (
            "VAL2376_09_local_claims_block",
            any(row["row_id"] == "CG2376_4_local_GR_Newton" and row["gate_status"] == "FAIL" for row in gates),
            "local GR/Newton claim gate remains false",
        ),
        (
            "VAL2376_10_no_positive_claim_flags",
            check_no_positive_claim_flags(generated_paths),
            "all generated claim/readiness flags remain negative",
        ),
        (
            "VAL2376_11_formalization_untouched",
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
            "row_id": "VAL2376_OVERALL",
            "status": "PASS" if overall_ok else "FAIL",
            "detail": "2376 valid: SRNG source/readout no-Gamma certificate written nonclaim, conditional zero effect recorded, boundary/projective/P4 retained, downstream functor derivation selected"
            if overall_ok
            else "2376 validation failed",
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
    cert = read_csv(outputs["srng_certificate"])
    theorem = read_csv(outputs["srng_theorem"])
    p4 = read_csv(outputs["p4_status"])
    decisions = read_csv(outputs["decision_ledger"])
    gates = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])
    generated = [rel(path) for path in outputs.values()]

    text = f"""# 2376 - Source-Readout noGamma Action-Argument Certificate

## Result

The source/readout no-Gamma certificate is now explicit:

`SRNG`: source support, clocks, light, orbits and readout maps may use the observed coframe/metric, `omega_LC[e_obs]`, owned gauge fields, constants and solved fields, but not an independent `Gamma_ind` argument inside the variational source/action.

Under SRNG plus the no-Gamma ordinary matter branch:

`Delta_source = Delta_clock = Delta_light = Delta_orbit = 0`

without cancellation.

But SRNG is a private contract, not yet a derived parent theorem.  Boundary/improvement and projective trace also remain separate residual channels.  So this improves the connection route, but it does not close local GR/Newton.

## SRNG Argument Certificate

{md_table(cert, ["row_id", "sector", "status", "closes_delta", "remaining_gap"])}

## SRNG Theorem Attempt

{md_table(theorem, ["row_id", "claim_piece", "result", "obstruction"])}

## P4 Delta Status After SRNG

{md_table(p4, ["row_id", "component", "status_after_SRNG", "current_status", "needed_for_score"])}

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

This is a real structural gain.  We now have a compact clause that would zero the source/readout Gamma components together.  The remaining honest question is whether SRNG can be derived from downstream observation functor naturality, or whether it must stay as a private parent-action restriction with P4 fallback bounds.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    outputs = all_output_files()
    write_csv(outputs["source_register"], source_register())
    write_csv(outputs["srng_certificate"], srng_argument_certificate())
    write_csv(outputs["srng_theorem"], srng_theorem_attempt())
    write_csv(outputs["p4_status"], p4_status_after_srng())
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

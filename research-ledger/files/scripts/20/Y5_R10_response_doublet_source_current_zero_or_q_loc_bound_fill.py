from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def missing(value: object) -> bool:
    text = str(value or "").strip()
    return text == "" or text.upper().startswith("MISSING")


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def path_exists(path_text: str) -> bool:
    text = str(path_text or "").strip()
    if missing(text):
        return False
    if text in {"THEOREM_ONLY", "BOUND_TEMPLATE_ONLY", "NOT_NUMERIC", "FORBIDDEN"}:
        return False
    return source_path(text).exists()


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(col, "")) for col in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1011_0_1010_next", "source-intake/mts_residuals/P8_Y5_R10_1010_NEXT_TARGET.csv", "response-doublet-source-current-zero", "1010 handoff target."),
        ("SRC1011_1_1010_theorem", "source-intake/mts_residuals/P8_Y5_R10_1010_THEOREM_ATTEMPT.csv", "GKT1010_3_Euler_closure", "1010 Euler/double-zero blocker."),
        ("SRC1011_2_1010_runner", "source-intake/mts_residuals/P8_Y5_R10_1010_RUNNER.csv", "GKR1010_1_response_doublet_even_density", "response-doublet route refused as derivation."),
        ("SRC1011_3_1010_residual", "source-intake/mts_residuals/P8_Y5_R10_1010_RESIDUAL_RETENTION_LEDGER.csv", "QRES1010_3_source_boundary_gap", "source/boundary gap retained."),
        ("SRC1011_4_doublet_contract", "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv", "RD516_4_zero_odd_source", "response-doublet source-current contract."),
        ("SRC1011_5_doublet_variation", "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv", "AV517_4_Euler_equation", "Euler source term obstruction."),
        ("SRC1011_6_euler_source", "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv", "Y5_source_normalization", "Y5/Y6 source blockers."),
        ("SRC1011_7_metric_response", "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_METRIC_RESPONSE_LEDGER.csv", "MR517_2_Z_metric_lock", "metric-response leakage."),
        ("SRC1011_8_obstruction", "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_OBSTRUCTION_LEDGER.csv", "OB517_0_Y5_even_scalar", "hard obstruction ledger."),
        ("SRC1011_9_gate_tests", "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_VARIATION_GATE_TESTS.csv", "G517_2_current_MTS_derivation", "current MTS derivation fails."),
        ("SRC1011_10_decision", "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_VARIATION_DECISION.csv", "D517_2", "Y5 next pressure decision."),
        ("SRC1011_11_odd_contract", "source-intake/mts_residuals/P8_ODD_RESIDUAL_EXCHANGE_CONTRACT.csv", "O2_even_matter_readout", "odd residual exchange contract."),
        ("SRC1011_12_odd_theorem", "source-intake/mts_residuals/P8_ODD_RESIDUAL_EXCHANGE_THEOREM.csv", "E5_current_corpus", "exchange theorem current-corpus limit."),
        ("SRC1011_13_bound_spec", "source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv", "QB516_0_compact_shell_budget", "q_loc bound runner spec."),
        ("SRC1011_14_bound_trigger", "source-intake/mts_residuals/P8_QLOC_BOUND_TRIGGER_LEDGER.csv", "BT517_1_Y5_unsolved", "bound trigger ledger."),
        ("SRC1011_15_bound_register", "source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_BOUND_REGISTER.csv", "LRV_DOMAIN_R11_SOURCE_NORMALIZATION", "local residual bound register."),
        ("SRC1011_16_scorecard", "source-intake/mts_residuals/P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv", "epsilon_domain_projector", "local bound scorecard."),
    ]
    rows = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": path_text,
                "exists": str(path.exists()).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "generated_utc": stamp(),
            }
        )
    return rows


def doublet_theorem_rows() -> list[dict[str, str]]:
    rows = [
        {
            "clause_id": "RDT1011_0_parent_doublets",
            "claim_piece": "R_+^A,R_-^A exist for every physical local residual channel",
            "mathematical_form": "Z^A=(R_+^A-R_-^A)/2 and R_even^A=(R_+^A+R_-^A)/2",
            "current_evidence": "odd residual contract says parent doublets are not derived for every residual channel.",
            "status": "not_derived",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "RDT1011_1_exchange_symmetry",
            "claim_piece": "exchange is exact parent symmetry",
            "mathematical_form": "E: R_+^A <-> R_-^A forbids linear Z source terms",
            "current_evidence": "exchange exactness is only a conditional template.",
            "status": "conditional_template",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "RDT1011_2_even_matter_readout",
            "claim_piece": "matter/clocks/source measures couple only to even quotient variables",
            "mathematical_form": "S_matter=S_matter[Psi,e_obs(R_even)] and delta_Z S_matter=0",
            "current_evidence": "Y0 and Y5 ledgers show matter trace/source normalization can remain exchange-even and not zeroed.",
            "status": "not_derived_hard_for_Y5",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "RDT1011_3_source_current_zero",
            "claim_piece": "J_Z=0 on compact local branch",
            "mathematical_form": "Euler: L_AB Z^B = J_A + boundary/source terms; J_A=0",
            "current_evidence": "AV517_4 is blocked by source-current rows; Y5 hard_fail_current and Y6 retained_debt.",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "RDT1011_4_boundary_zero",
            "claim_piece": "B_Z=0/no odd boundary charge",
            "mathematical_form": "boundary/source work vanishes in local compact collar",
            "current_evidence": "Y2 is only conditional and MR517_3 boundary/domain terms are open.",
            "status": "conditional_not_closed",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "RDT1011_5_positive_operator",
            "claim_piece": "L_AB positive after gauge/constraint removal",
            "mathematical_form": "integral Z^A L_AB Z^B = boundary_flux + source_work",
            "current_evidence": "positive theorem is conditional only; it cannot activate without J_Z=B_Z=0.",
            "status": "formal_candidate_only",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "RDT1011_6_PPN_lock",
            "claim_piece": "Z^A equals the physical q_loc/PPN/source-normalization residual vector",
            "mathematical_form": "Z^A=Y_loc^A through beta/gamma/alpha_i/xi/Gdot/R11 order",
            "current_evidence": "OB517_2 and RD516_5 say PPN lock is not derived.",
            "status": "not_derived",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "RDT1011_7_verdict",
            "claim_piece": "response-doublet source-current/boundary zero theorem",
            "mathematical_form": "RDT1011_0 through RDT1011_6 all parent-signed",
            "current_evidence": "formal double-zero survives, but source-current zero, Y5/Y6, PPN lock, and boundary terms block promotion.",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def bound_fill_rows() -> list[dict[str, str]]:
    rows = [
        {
            "bound_id": "QBF1011_0_compact_shell_budget",
            "quantity": "max |P_loc d_rel J_rel| or equivalent q_loc leakage",
            "candidate_value": "7.432631961576971e-06",
            "units": "dimensionless_proxy",
            "bound_or_gate": "requires mapping into PPN/source-normalization units",
            "source_path": "source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv",
            "status": "anchor_proxy_not_claim_curve",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "QBF1011_1_alpha3_pressure",
            "quantity": "alpha3-equivalent q_loc channel",
            "candidate_value": "MISSING_QLOC_TO_ALPHA3_COEFFICIENT",
            "units": "dimensionless",
            "bound_or_gate": "abs(alpha3) <= 4e-20 where alpha3 applies",
            "source_path": "source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv",
            "status": "mapping_missing",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "QBF1011_2_Gdot_GMdot",
            "quantity": "dln_mu_obs_dt or dln_Meff_dt",
            "candidate_value": "MISSING_TIME_COMPONENT_AND_UNITS",
            "units": "yr^-1",
            "bound_or_gate": "use Gdot/source-normalization ledgers after time component is derived",
            "source_path": "source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv",
            "status": "time_projection_missing",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "QBF1011_3_PPN_metric_tail",
            "quantity": "Delta_PPN from q_loc",
            "candidate_value": "MISSING_WEAK_FIELD_METRIC_SOLUTION",
            "units": "dimensionless_vector",
            "bound_or_gate": "gamma,beta,alpha_i,xi official local gates",
            "source_path": "source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_BOUND_REGISTER.csv",
            "status": "PPN_mapping_missing",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "QBF1011_4_R11_operator",
            "quantity": "c_GK_operator_vector",
            "candidate_value": "MISSING_OPERATOR_VECTOR",
            "units": "operator_family_units_required",
            "bound_or_gate": "R11/non-EH operator ledgers",
            "source_path": "source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_BOUND_REGISTER.csv",
            "status": "operator_vector_missing",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "QBF1011_5_Y5_source_normalization",
            "quantity": "c_domain_source_normalization_operator or measured-GM residual",
            "candidate_value": "MISSING_Y5_OWNER_OR_NUMERIC_COEFFICIENT",
            "units": "dimensionless_or_operator_units",
            "bound_or_gate": "source-normalized Newton/R11 gate",
            "source_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
            "status": "Y5_hard_fail_current",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "QBF1011_6_Y6_extra_stress",
            "quantity": "T_extra residual vector",
            "candidate_value": "MISSING_Y6_STRESS_BOUND",
            "units": "stress_or_PPN_units_required",
            "bound_or_gate": "extra stress topological/invisible or PPN bounded",
            "source_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
            "status": "retained_debt",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def evaluate_bound(row: dict[str, str]) -> dict[str, str]:
    reasons: list[str] = []
    if not path_exists(row["source_path"]):
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if missing(row["candidate_value"]):
        reasons.append("MISSING_NUMERIC_OR_THEOREM_ZERO_VALUE")
    if missing(row["units"]):
        reasons.append("MISSING_UNITS")
    if row["status"] in {"mapping_missing", "time_projection_missing", "PPN_mapping_missing", "operator_vector_missing", "Y5_hard_fail_current", "retained_debt"}:
        reasons.append(f"{row['status'].upper()}_BLOCKS_CLAIM")
    if not flag(row["valid_for_claim"]):
        reasons.append("VALID_FOR_CLAIM_FALSE")
    claim_allowed = not reasons and flag(row["valid_for_claim"])
    return {
        "runner_id": row["bound_id"].replace("QBF", "QBR"),
        "bound_id": row["bound_id"],
        "quantity": row["quantity"],
        "verdict": "PASS_QLOC_BOUND_ROW" if claim_allowed else "RETAINED_NONCLAIM_QLOC_BOUND_ROW",
        "score_ready": str(row["bound_id"] == "QBF1011_0_compact_shell_budget").lower(),
        "claim_allowed": str(claim_allowed).lower(),
        "valid_for_claim": str(claim_allowed).lower(),
        "failure_reasons": ";".join(reasons),
        "generated_utc": stamp(),
    }


def bound_runner_rows(bounds: list[dict[str, str]]) -> list[dict[str, str]]:
    return [evaluate_bound(row) for row in bounds]


def claim_gate_rows(theorem: list[dict[str, str]], bound_runner: list[dict[str, str]]) -> list[dict[str, str]]:
    theorem_failed = any(row["clause_id"] == "RDT1011_7_verdict" and row["status"] == "fail_current_claim" for row in theorem)
    bounds_nonclaim = all(not flag(row["claim_allowed"]) for row in bound_runner)
    anchor_present = any(row["bound_id"] == "QBF1011_0_compact_shell_budget" and row["verdict"] == "RETAINED_NONCLAIM_QLOC_BOUND_ROW" for row in bound_runner)
    gates = [
        ("CG1011_0_response_doublet_zero", "response-doublet source-current/boundary zero theorem passes", "false", "Y5/Y6, PPN lock, and boundary source terms remain unsigned"),
        ("CG1011_1_Y5_source_normalization", "source-normalization even scalar is zero by exchange symmetry", "false", "Y5 is exchange-even and hard-fail current"),
        ("CG1011_2_Y6_extra_stress", "extra stress is invisible/topological by doublet symmetry", "false", "Y6 can be conserved and nonzero"),
        ("CG1011_3_q_loc_bound_claim", "q_loc residual bounds are claim-ready", "false", "bound rows are templates/proxies without coefficient mappings"),
        ("CG1011_4_Htau_MHref_local_GR", "H_tau/M_H_ref/local-GR gates can reopen", "false", "q_loc and source-normalization remain retained residuals"),
        ("CG1011_5_bound_branch_ready", "q_loc bound branch is staged as nonclaim", str(anchor_present and bounds_nonclaim).lower(), "bound rows exist but do not claim pass"),
        ("CG1011_6_guardrail", "response-doublet proof-or-bound guardrail is installed", str(theorem_failed and bounds_nonclaim).lower(), "zero theorem is not promoted and bound rows stay nonclaim"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for gate_id, claim, gate_pass, reason in gates
    ]


def decision_rows() -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC1011_0_formal_double_zero_survives",
            "decision": "The response-doublet double-zero remains a serious route, but only as a conditional theorem.",
            "because": "quadratic Gamma_eff gives F_1=0 at Z=0 if Z is the physical residual and J_Z=B_Z=0.",
            "next_action": "do not discard it; attack the source-current owner theorem directly",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1011_1_Y5_is_root_pressure",
            "decision": "Y5 source-normalization is the hardest immediate blocker for Newton/GR recovery.",
            "because": "source normalization is exchange-even, so odd-doublet symmetry does not automatically erase it.",
            "next_action": "derive a mass/source-normalization owner theorem or fill measured-GM/R11 coefficients",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1011_2_q_loc_bounds_not_ready",
            "decision": "The q_loc bound branch is staged but not claim-ready.",
            "because": "compact-shell proxy lacks PPN/source-normalization coefficient mapping; alpha3/R11/Gdot rows remain missing.",
            "next_action": "build a Y5 source-normalization owner-or-numeric-bound implementation",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
            "objective": "derive whether measured-GM/source normalization is owned by the parent current chain and zero/topological locally; if not, implement numeric q_loc/R11/source-normalization bound rows",
            "include": "Y5 source-normalization, measured GM, M_eff, Pi_M J_H, R11 operator vector, compact-shell proxy mapping, alpha3/R11/Gdot coefficient rows, units, source paths",
            "exclude": "odd symmetry overclaim, plateau axiom, fitted cancellation, H_tau pass, M_H_ref pass, local-GR claim, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED:
            changed.append(path)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    bounds: list[dict[str, str]],
    bound_runner: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    validations = [
        ("V1011_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and needles are present"),
        ("V1011_1_theorem_blocks_claim", any(row["clause_id"] == "RDT1011_7_verdict" and row["status"] == "fail_current_claim" for row in theorem) and all(not flag(row["valid_for_claim"]) for row in theorem), "response-doublet zero theorem remains nonclaim"),
        ("V1011_2_Y5_Y6_recorded", any(row["clause_id"] == "RDT1011_2_even_matter_readout" for row in theorem) and any(row["bound_id"] == "QBF1011_5_Y5_source_normalization" for row in bounds) and any(row["bound_id"] == "QBF1011_6_Y6_extra_stress" for row in bounds), "Y5 and Y6 blockers are explicitly recorded"),
        ("V1011_3_bound_rows_nonclaim", len(bounds) >= 7 and all(not flag(row["valid_for_claim"]) for row in bounds), "q_loc bound-fill rows remain nonclaim"),
        ("V1011_4_bound_runner_nonclaim", len(bound_runner) == len(bounds) and all(not flag(row["claim_allowed"]) for row in bound_runner), "bound runner keeps all rows nonclaim"),
        ("V1011_5_compact_proxy_retained", any(row["bound_id"] == "QBF1011_0_compact_shell_budget" and row["score_ready"] == "true" and row["verdict"] == "RETAINED_NONCLAIM_QLOC_BOUND_ROW" for row in bound_runner), "compact-shell proxy is retained but not claim-ready"),
        ("V1011_6_claim_gates_blocked", all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in claims), "doublet, q_loc bound, H_tau, M_H_ref, and local-GR claims stay blocked"),
        ("V1011_7_guardrail_written", any(row["gate_id"] == "CG1011_6_guardrail" and flag(row["gate_pass"]) for row in claims), "response-doublet proof-or-bound guardrail is installed"),
        ("V1011_8_decision_written", any(row["decision_id"] == "DEC1011_1_Y5_is_root_pressure" for row in decisions), "Y5 source-normalization root-pressure decision is written"),
        ("V1011_9_next_target_written", len(next_target) == 1 and "1012-Y5-R10-Y5-source-normalization-owner" in next_target[0]["next_target"], "1012 target row is present and nonclaim"),
        ("V1011_10_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": cid, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for cid, passed, detail in validations]
    rows.insert(0, {"check_id": "V1011_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1011 response-doublet proof-or-bound validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    bounds: list[dict[str, str]],
    bound_runner: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1011 Y5 R10 response-doublet source-current zero or q_loc bound fill",
            "",
            "**Status:** the response-doublet double-zero remains a viable conditional route, but the current corpus does not prove `J_Z=0`, `B_Z=0`, Y5 source-normalization silence, Y6 extra-stress invisibility, or PPN lock. q_loc bound-fill rows are staged as nonclaim.",
            "",
            "**Claim ceiling:** no response-doublet local-GR pass, q_loc bound pass, H_tau, M_H_ref, Newton/GR reduction, or PPN pass is allowed from 1011.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Response-doublet theorem attempt",
            md_table(theorem, ["clause_id", "claim_piece", "mathematical_form", "current_evidence", "status", "valid_for_claim"]),
            "## q_loc bound-fill rows",
            md_table(bounds, ["bound_id", "quantity", "candidate_value", "units", "bound_or_gate", "status", "valid_for_claim"]),
            "## q_loc bound runner",
            md_table(bound_runner, ["runner_id", "bound_id", "quantity", "verdict", "score_ready", "claim_allowed", "failure_reasons"]),
            "## Claim gate",
            md_table(claims, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Validation",
            md_table(validations, ["check_id", "result", "detail", "generated_utc"]),
            "## Next target",
            md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    theorem = doublet_theorem_rows()
    bounds = bound_fill_rows()
    bound_runner = bound_runner_rows(bounds)
    claims = claim_gate_rows(theorem, bound_runner)
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, theorem, bounds, bound_runner, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1011_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_1011_QLOC_BOUND_FILL_ROWS.csv", bounds)
    write_csv(OUT / "P8_Y5_R10_1011_QLOC_BOUND_RUNNER.csv", bound_runner)
    write_csv(OUT / "P8_Y5_R10_1011_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_1011_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1011_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1011_VALIDATION.csv", validations)
    write_doc(sources, theorem, bounds, bound_runner, claims, decisions, next_target, validations)


if __name__ == "__main__":
    main()

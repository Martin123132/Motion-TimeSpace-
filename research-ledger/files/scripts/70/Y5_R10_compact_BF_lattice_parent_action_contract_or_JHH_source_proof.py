from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC_NAME = "927-Y5-R10-compact-BF-lattice-parent-action-contract-or-JHH-source-proof.md"
STATUS = "Y5_R10_927_compact_BF_lattice_parent_action_contract_written_JHH_source_proof_not_closed"
CLAIM_CEILING = "compact_BF_lattice_parent_contract_only_no_numeric_KBFH_no_WEP_R10_PPN_Newton_or_local_GR_claim"
NEXT_TARGET = "928-Y5-R10-instantiate-compact-BF-lattice-or-retain-KBFH-residual-bound-row.md"
GENERATED = datetime.now(timezone.utc).isoformat()
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        cells = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def b(value: bool) -> str:
    return "true" if value else "false"


def source_specs() -> list[dict[str, str]]:
    return [
        {
            "source_id": "926_doc",
            "path": "926-Y5-R10-BM-charge-unit-quantization-or-source-worldtube-equality-proof.md",
            "role": "immediate compact BF lattice conditional theorem",
            "needle": "K_BF_H/k_M = R_BJ = N_B/N_H",
        },
        {
            "source_id": "926_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_926_VALIDATION.csv",
            "role": "proves 926 validation passed",
            "needle": "V926_11_validation_rows_ready",
        },
        {
            "source_id": "926_BF_lattice",
            "path": "source-intake/mts_residuals/P8_Y5_R10_926_BF_LATTICE_THEOREM_ATTEMPT.csv",
            "role": "compact BF lattice clauses BF926_0 through BF926_5",
            "needle": "BF926_4_ratio_lattice",
        },
        {
            "source_id": "926_source_worldtube",
            "path": "source-intake/mts_residuals/P8_Y5_R10_926_SOURCE_WORLDTUBE_EQUALITY_ATTEMPT.csv",
            "role": "source-worldtube equality proof clauses",
            "needle": "SWT926_1_Hilbert_to_Hamiltonian_charge",
        },
        {
            "source_id": "924_doc",
            "path": "924-Y5-R10-Hamiltonian-mass-charge-normalization-contract-or-FM-bound-row-expansion.md",
            "role": "BF/source parent action candidate",
            "needle": "S = k_M integral B_M wedge dA_M + K_BF_H integral A_M wedge J_H^H",
        },
        {
            "source_id": "537_parent_contract",
            "path": "537-Y5-Hilbert-worldtube-parent-action-contract-or-PiM-input-fill.md",
            "role": "same-worldtube Hilbert/topological equality contract",
            "needle": "PAC537_5_Hilbert_topological_charge_equality",
        },
        {
            "source_id": "542_source_measure",
            "path": "542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md",
            "role": "conditional source-measure theorem and residual fallback",
            "needle": "SMT542_2_observed_worldtube_source",
        },
        {
            "source_id": "worldtube_certificate",
            "path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv",
            "role": "missing same-worldtube/topological certificate rows",
            "needle": "HWG535_2_topological_representative_matches_worldtube_boundary",
        },
    ]


def build_sources() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in source_specs():
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": b(exists),
                "needle_found": b(needle_found),
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "current_result": "the exact parent-action contract for the compact BF lattice route is written, but current MTS has not instantiated it",
            "what_changed": "the future parent action now has explicit clauses for compact periods, large-gauge invariance, source lattice, same-worldtube match, and Gauss readout",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def parent_action_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "CBF927_0_compact_parent_fields",
            "required_clause": "A_M is a compact 1-form gauge field and B_M is a compact 2-form gauge field on the local branch.",
            "mathematical_form": "a_M=A_M/(2*pi), b_M=B_M/(2*pi); periods of da_M and b_M are integral",
            "derives": "BF926_0;BF926_3",
            "current_status": "not_instantiated_in_current_parent_action",
            "if_missing": "B_M charge unit remains arbitrary",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "contract_id": "CBF927_1_large_gauge_invariance",
            "required_clause": "The exponentiated action is invariant under large A_M and B_M gauge transformations.",
            "mathematical_form": "exp(i S_M) invariant for integral shifts of a_M and b_M",
            "derives": "BF926_1",
            "current_status": "not_parent_signed",
            "if_missing": "k_M and K_BF_H can be continuous normalization choices",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "contract_id": "CBF927_2_normalized_BF_action",
            "required_clause": "The mass gauge sector is written in normalized compact variables.",
            "mathematical_form": "S_M = 2*pi*k_M int b_M wedge da_M + 2*pi*K_H int a_M wedge j_H^H",
            "derives": "BF source equation with integer-lattice variables",
            "current_status": "contract_only",
            "if_missing": "924 action remains symbolic and unit-incomplete",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "contract_id": "CBF927_3_source_current_lattice",
            "required_clause": "j_H^H is the normalized observed Hilbert source current on an integral source lattice.",
            "mathematical_form": "int_C j_H^H = N_H in Z",
            "derives": "BF926_2;SWT926_1",
            "current_status": "not_parent_signed",
            "if_missing": "denominator of R_BJ is not a source charge",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "contract_id": "CBF927_4_same_worldtube_boundary_class",
            "required_clause": "The B_M boundary flux and j_H^H source charge link the same Hilbert source worldtube.",
            "mathematical_form": "partial C links W_source=supp(J_H[e_obs]); int_boundaryC b_M=N_B; int_C j_H^H=N_H",
            "derives": "SWT926_0;SWT926_2",
            "current_status": "certificate_missing",
            "if_missing": "topology can conserve the wrong charge",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "contract_id": "CBF927_5_variation_owns_ratio",
            "required_clause": "The A_M variation gives the BF/source equation without hidden boundary/source terms.",
            "mathematical_form": "k_M db_M = K_H j_H^H + residual; residual=0 or retained",
            "derives": "R_BJ ratio law",
            "current_status": "residual_not_proved_zero",
            "if_missing": "K_BF_H/k_M receives unowned correction terms",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "contract_id": "CBF927_6_source_measure_glue",
            "required_clause": "The integral source charge equals the Hamiltonian source charge before orbital readout.",
            "mathematical_form": "int_C J_H^H = Q_tau[W] = H_tau[S]-H_ref = M_source[W]",
            "derives": "SWT926_1 and measured source denominator",
            "current_status": "not_derived",
            "if_missing": "compact source lattice is not measured mass",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "contract_id": "CBF927_7_Gauss_PPN_readout_after_glue",
            "required_clause": "The same source charge controls weak-field Gauss law and PPN followthrough.",
            "mathematical_form": "surface_integral grad Phi dot dS = 4*pi*G_ref*Q_tau; Delta_PPN below locks",
            "derives": "Newton/PPN test connection after source glue",
            "current_status": "not_reached",
            "if_missing": "ratio cannot be used for local-GR claims",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def proof_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "step_id": "PROOF927_0_write_normalized_action",
            "operation": "replace symbolic 924 action with compact normalized variables",
            "mathematical_result": "S_M = 2*pi*k_M int b_M wedge da_M + 2*pi*K_H int a_M wedge j_H^H",
            "status": "contract_written_not_instantiated",
            "remaining_gap": "current parent action has not specified compact field periods",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "step_id": "PROOF927_1_large_gauge_gate",
            "operation": "demand exponentiated-action invariance under large gauge transformations",
            "mathematical_result": "k_M integer and source charges on an allowed lattice",
            "status": "conditional_standard_BF_route",
            "remaining_gap": "large-gauge transformation class not derived from MTS parent variables",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "step_id": "PROOF927_2_variation",
            "operation": "vary a_M",
            "mathematical_result": "k_M db_M = K_H j_H^H when residual boundary/source terms vanish",
            "status": "conditional_with_residual_guard",
            "remaining_gap": "residual=0 not proved for current MTS",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "step_id": "PROOF927_3_integrate_chain",
            "operation": "integrate the source equation over C linking W_source",
            "mathematical_result": "k_M N_B = K_H N_H, hence K_H/k_M=N_B/N_H",
            "status": "conditional_ratio_derivation",
            "remaining_gap": "N_B and N_H not parent-signed and same-worldtube link not certified",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "step_id": "PROOF927_4_source_readout",
            "operation": "attempt to identify N_H with Q_tau/M_unit and measured M_source",
            "mathematical_result": "N_H = Q_tau/q_H only if Hilbert worldtube and Hamiltonian charge share the same source lattice",
            "status": "not_closed",
            "remaining_gap": "J_H^H=Q_tau=M_source remains open",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def jhh_source_proof_rows() -> list[dict[str, object]]:
    return [
        {
            "clause_id": "JHH927_0_single_observed_frame",
            "needed_identity": "one observed coframe/metric owns matter source, clocks, and orbital readout",
            "math_form": "S_matter=S_matter[e_obs,psi_m]; J_H from delta S_matter/delta e_obs",
            "status": "not_parent_signed",
            "failure_mode": "source and readout frames can split",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "clause_id": "JHH927_1_worldtube_support",
            "needed_identity": "source worldtube is fixed by J_H support before fitting",
            "math_form": "W_source=supp(J_H[e_obs])",
            "status": "definition_guardrail_only",
            "failure_mode": "source support can be retuned per system",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "clause_id": "JHH927_2_integral_source_lattice",
            "needed_identity": "J_H^H descends to the compact BF source lattice",
            "math_form": "J_H^H = q_H j_H^H; int_C j_H^H=N_H in Z",
            "status": "not_derived",
            "failure_mode": "BF source charge is not the Hilbert mass source",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "clause_id": "JHH927_3_Hamiltonian_equality",
            "needed_identity": "integral_C J_H^H equals Q_tau and dressed M_source before orbital readout",
            "math_form": "int_C J_H^H=Q_tau[W]=H_tau[S]-H_ref=M_source[W]",
            "status": "not_derived",
            "failure_mode": "integer source lattice is not measured mass",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "clause_id": "JHH927_4_same_boundary_class",
            "needed_identity": "B_M flux boundary and J_H^H source lattice refer to the same W_source",
            "math_form": "partial C links W_source and no independent topological source label exists",
            "status": "certificate_missing",
            "failure_mode": "wrong topological charge receives credit",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "ACC927_0_compact_periods",
            "requirement": "A_M/B_M compact periods are parent-derived",
            "current_status": "missing",
            "if_pass": "B_M unit becomes a lattice charge",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "ACC927_1_source_lattice",
            "requirement": "J_H^H is the same integral lattice current",
            "current_status": "missing",
            "if_pass": "N_H becomes source denominator",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "ACC927_2_same_worldtube",
            "requirement": "B_M boundary class and Hilbert source worldtube match",
            "current_status": "missing",
            "if_pass": "topological wrong-charge loophole closes",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "ACC927_3_residual_zero",
            "requirement": "boundary/reference/extra/source residual in A_M variation is zero or retained",
            "current_status": "missing",
            "if_pass": "ratio equation is clean rather than corrected",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "ACC927_4_measured_GM_readout",
            "requirement": "Q_tau from the same source lattice controls Gauss/orbital/PPN readout",
            "current_status": "not_reached",
            "if_pass": "ratio becomes test-ready instead of just formal",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def blocker_rows() -> list[dict[str, object]]:
    return [
        {
            "blocker_id": "BLK927_0_parent_instantiation",
            "missing_input": "actual MTS parent action block with compact A_M/B_M periods",
            "why_needed": "contract rows cannot promote without a source parent term",
            "next_action": "instantiate compact BF lattice against current MTS symbols or demote to residual coupling",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK927_1_same_worldtube_certificate",
            "missing_input": "certificate tying B_M flux boundary class to W_source=supp(J_H)",
            "why_needed": "prevents wrong topological charge credit",
            "next_action": "prove same-class map or retain source residual",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK927_2_JHH_Qtau",
            "missing_input": "int_C J_H^H=Q_tau=M_source",
            "why_needed": "connects source lattice denominator to measured mass source",
            "next_action": "close HSM541_1/HSM541_2 or retain frame/source-measure residual",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "BD927_0_contract",
            "branch": "compact_BF_lattice_parent_action",
            "verdict": "contract_written_not_instantiated",
            "reason": "the action clauses needed to derive N_B/N_H are explicit but not owned by current MTS",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD927_1_source_proof",
            "branch": "JHH_source_worldtube_proof",
            "verdict": "not_closed",
            "reason": "same-worldtube source lattice and Hamiltonian equality are still missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD927_2_next",
            "branch": "next_derivation_target",
            "verdict": "selected",
            "reason": "instantiate the compact BF lattice with current MTS parent symbols or convert K_BF_H into an explicit residual row",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CGATE927_0_numeric_ratio",
            "claim": "K_BF_H/k_M is numeric or +/-1",
            "blocker": "contract is not instantiated; N_B=N_H=1 not proved",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE927_1_local_bounds",
            "claim": "WEP/R10/clock/PPN FM rows can score",
            "blocker": "ratio/source/projection inputs remain missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE927_2_Newton_local_GR",
            "claim": "source-normalized Newton or local GR is derived",
            "blocker": "Gauss/orbital/PPN followthrough not reached",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "try to instantiate the compact BF lattice with current MTS parent symbols; if not possible, retain K_BF_H as an explicit residual coupling with source-backed bound rows",
            "include": "symbol-to-contract map, compact-period evidence audit, same-worldtube certificate attempt, residual-coupling fallback rows",
            "exclude": "numeric pass claims, +/-1 promotion without proof, post-fit G/M absorption, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def formalization_changed_count() -> int:
    formalization = ROOT.parent / "formalization-workbench"
    if not formalization.exists():
        return 0
    return sum(
        1
        for path in formalization.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def all_false(rows: list[dict[str, object]], fields: tuple[str, ...]) -> bool:
    return all(str(row.get(field, "")).strip().lower() != "true" for row in rows for field in fields)


def validation_rows(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    proof: list[dict[str, object]],
    jhh: list[dict[str, object]],
    acceptance: list[dict[str, object]],
    blockers: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior = OUT / "P8_Y5_BRR545_926_VALIDATION.csv"
    prior_rows = read_csv(prior) if prior.exists() else []
    prior_ok = bool(prior_rows) and all(row.get("result") == "pass" for row in prior_rows)
    needed_contracts = {"CBF927_0_compact_parent_fields", "CBF927_3_source_current_lattice", "CBF927_4_same_worldtube_boundary_class", "CBF927_6_source_measure_glue"}
    contract_ids = {str(row.get("contract_id")) for row in contract}
    proof_ratio = any("K_H/k_M=N_B/N_H" in str(row.get("mathematical_result", "")) for row in proof)
    jhh_gaps = any(str(row.get("status", "")).lower() in {"not_derived", "certificate_missing", "not_parent_signed"} for row in jhh)
    acceptance_false = all(row.get("valid_for_claim") == "false" for row in acceptance)
    generated = contract + proof + jhh + acceptance + blockers + decisions + gates
    changed = formalization_changed_count()
    false_fields = ("claim_allowed", "valid_for_claim")
    return [
        {
            "check_id": "V927_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "missing source path or needle",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V927_1_prior_926_clean",
            "result": "pass" if prior_ok else "fail",
            "detail": "P8_Y5_BRR545_926_VALIDATION.csv clean" if prior_ok else "926 validation missing or not clean",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V927_2_contract_core_clauses_present",
            "result": "pass" if needed_contracts.issubset(contract_ids) else "fail",
            "detail": "compact fields, source lattice, same-worldtube class, and source glue clauses present",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V927_3_conditional_ratio_derivation_written",
            "result": "pass" if proof_ratio else "fail",
            "detail": "conditional K_H/k_M=N_B/N_H proof chain written",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V927_4_JHH_source_proof_not_overclaimed",
            "result": "pass" if jhh_gaps else "fail",
            "detail": "J_H^H source proof gaps remain explicit",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V927_5_acceptance_gates_nonclaim",
            "result": "pass" if acceptance_false and len(acceptance) >= 5 else "fail",
            "detail": "contract acceptance gates are explicit and nonclaim",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V927_6_claim_gates_false",
            "result": "pass" if all_false(gates, false_fields) else "fail",
            "detail": "numeric ratio, local-bound, and local-GR gates remain false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V927_7_all_generated_rows_nonclaim",
            "result": "pass" if all_false(generated, false_fields) else "fail",
            "detail": "all generated rows keep guarded claim fields false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V927_8_formalization_workbench_untouched",
            "result": "pass" if changed == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={changed}",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V927_9_next_target_selected",
            "result": "pass" if NEXT_TARGET.startswith("928-") else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V927_10_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
            "generated_utc": GENERATED,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    summary: list[dict[str, object]],
    contract: list[dict[str, object]],
    proof: list[dict[str, object]],
    jhh: list[dict[str, object]],
    acceptance: list[dict[str, object]],
    blockers: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 927 - Y5/R10 Compact BF Lattice Parent-Action Contract Or JHH Source Proof

Private parent-action contract checkpoint. This is not a public WEP, clock, PPN, R10, Newton, local-GR, or unified-field claim.

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

Current result: **the exact compact BF contract is now written, but the current MTS parent action has not instantiated it.**

The desired parent-action block is:

```text
S_M = 2*pi*k_M int b_M wedge da_M + 2*pi*K_H int a_M wedge j_H^H
```

with compact fields, large-gauge invariance, integer periods, a source-current lattice, and a same-Hilbert-worldtube certificate. If all of that lands, the ratio becomes:

```text
K_H/k_M = N_B/N_H
```

But this checkpoint does **not** promote that ratio. It writes the contract and shows exactly why the proof is still open for current MTS.

## Non-Claim Summary

{md_table(summary, ["status", "claim_ceiling", "current_result", "what_changed", "next_target", "valid_for_claim", "generated_utc"])}

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])}

## Compact BF Parent-Action Contract

{md_table(contract, ["contract_id", "required_clause", "mathematical_form", "derives", "current_status", "if_missing", "valid_for_claim", "generated_utc"])}

## Variation And Gauge Proof Attempt

{md_table(proof, ["step_id", "operation", "mathematical_result", "status", "remaining_gap", "valid_for_claim", "generated_utc"])}

## J_H^H Source Proof Clauses

{md_table(jhh, ["clause_id", "needed_identity", "math_form", "status", "failure_mode", "valid_for_claim", "generated_utc"])}

## Acceptance Gates

{md_table(acceptance, ["gate_id", "requirement", "current_status", "if_pass", "valid_for_claim", "generated_utc"])}

## Blocker Ledger

{md_table(blockers, ["blocker_id", "missing_input", "why_needed", "next_action", "valid_for_claim", "generated_utc"])}

## Branch Decision

{md_table(decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Claim Gate

{md_table(gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Next Target

{md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Validation

{md_table(validation, ["check_id", "result", "detail", "generated_utc"])}
"""
    (ROOT / DOC_NAME).write_text(body, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = build_sources()
    summary = summary_rows()
    contract = parent_action_contract_rows()
    proof = proof_attempt_rows()
    jhh = jhh_source_proof_rows()
    acceptance = acceptance_gate_rows()
    blockers = blocker_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    next_target = next_rows()
    validation = validation_rows(sources, contract, proof, jhh, acceptance, blockers, decisions, gates)

    write_csv(OUT / "P8_Y5_R10_927_SOURCE_REGISTER.csv", sources, ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_927_NONCLAIM_SUMMARY.csv", summary, ["status", "claim_ceiling", "current_result", "what_changed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_927_COMPACT_BF_PARENT_ACTION_CONTRACT.csv", contract, ["contract_id", "required_clause", "mathematical_form", "derives", "current_status", "if_missing", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_927_VARIATION_AND_GAUGE_PROOF_ATTEMPT.csv", proof, ["step_id", "operation", "mathematical_result", "status", "remaining_gap", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_927_JHH_SOURCE_PROOF_CLAUSES.csv", jhh, ["clause_id", "needed_identity", "math_form", "status", "failure_mode", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_927_ACCEPTANCE_GATES.csv", acceptance, ["gate_id", "requirement", "current_status", "if_pass", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_927_BLOCKER_LEDGER.csv", blockers, ["blocker_id", "missing_input", "why_needed", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_927_BRANCH_DECISION.csv", decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_927_CLAIM_GATE.csv", gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_927_NEXT_TARGET.csv", next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_BRR545_927_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(sources, summary, contract, proof, jhh, acceptance, blockers, decisions, gates, next_target, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"validation failed: {failed}")
    print(STATUS)
    print(f"wrote {ROOT / DOC_NAME}")
    print(f"next target: {NEXT_TARGET}")


if __name__ == "__main__":
    main()

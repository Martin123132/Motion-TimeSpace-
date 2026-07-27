from __future__ import annotations

import csv
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "972-Y5-R10-parent-two-slot-memory-action-and-Bianchi-identity-or-residual-source-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    since = SCRIPT_START_UTC.timestamp()
    count = 0
    try:
        for directory, _subdirs, filenames in os.walk(FORMALIZATION):
            for filename in filenames:
                path = Path(directory) / filename
                try:
                    if path.stat().st_mtime > since:
                        count += 1
                except OSError:
                    return -2
    except OSError:
        return -2
    return count


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "971_doc",
            "path": "971-Y5-R10-active-memory-zero-vs-double-zero-decoupling-branch-choice-or-runner-fill.md",
            "role": "handoff selecting two-slot/Bianchi target",
            "needle": "972-Y5-R10-parent-two-slot-memory-action-and-Bianchi-identity-or-residual-source-fill.md",
        },
        {
            "source_id": "971_bianchi_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_971_BIANCHI_VARIATION_GATE.csv",
            "role": "two-slot conservation/source/boundary blockers",
            "needle": "BVG971_6_verdict",
        },
        {
            "source_id": "971_split_attempt",
            "path": "source-intake/mts_residuals/P8_Y5_R10_971_PARENT_SPLIT_DERIVATION_ATTEMPT.csv",
            "role": "relative two-slot derivation attempt",
            "needle": "PSD971_7_verdict",
        },
        {
            "source_id": "971_residual_minimums",
            "path": "source-intake/mts_residuals/P8_Y5_R10_971_RESIDUAL_MINIMUM_ROWS.csv",
            "role": "retained memory residual minimum source rows",
            "needle": "RMIN971_6_claim_policy",
        },
        {
            "source_id": "967_memory_lemma",
            "path": "source-intake/mts_residuals/P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
            "role": "relative positive-operator theorem",
            "needle": "MPO967_6_verdict",
        },
        {
            "source_id": "968_memory_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
            "role": "missing X/operator/source/boundary/K inputs",
            "needle": "MOI968_8_verdict",
        },
        {
            "source_id": "476_variation_test",
            "path": "source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_VARIATION_TEST.csv",
            "role": "double-zero local variation requirement",
            "needle": "pass_as_sufficient_contract",
        },
        {
            "source_id": "417_boundary",
            "path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "role": "boundary/Bianchi/no-hair blocker",
            "needle": "Bianchi_gate_owned",
        },
        {
            "source_id": "506_energy_identity",
            "path": "source-intake/mts_residuals/P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
            "role": "extra-sector positive operator and memory silence identities",
            "needle": "E506_vector_tensor_positive_operator",
        },
        {
            "source_id": "507_acceptance_gates",
            "path": "source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_ACCEPTANCE_GATES.csv",
            "role": "theorem-zero/numeric-bound acceptance standards",
            "needle": "G507_0_theorem_zero",
        },
        {
            "source_id": "943_coframe_contract",
            "path": "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
            "role": "matter/coframe descent contract remains unsigned",
            "needle": "contract_exact_but_unsigned",
        },
        {
            "source_id": "945_q_kernel",
            "path": "945-Y5-R10-parent-q-map-Obs-e-functor-construction-or-first-frame-leak-bound-pack.md",
            "role": "q-kernel ownership gap",
            "needle": "QMAP945_6_verdict",
        },
        {
            "source_id": "963_no_tower",
            "path": "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
            "role": "no-integrated-out tower blocker",
            "needle": "NES963_3_no_integrated_out_tower",
        },
    ]
    rows = []
    for spec in specs:
        absolute_path = source_path(spec["path"])
        exists = absolute_path.exists()
        needle_found = spec["needle"] in read_text(absolute_path) if exists else False
        rows.append(
            {
                **spec,
                "absolute_path": str(absolute_path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def two_slot_action_contract() -> list[dict[str, str]]:
    specs = [
        {
            "contract_id": "TSC972_0_field_domain",
            "contract_piece": "parent field domain",
            "mathematical_form": "Phi_parent contains q/Phi geometry, X, chi_D, Psi, theta, and boundary data before readout",
            "contract_status": "REQUIRED_NOT_PARENT_SIGNED",
            "failure_if_missing": "two-slot action is a closure ansatz rather than parent action",
        },
        {
            "contract_id": "TSC972_1_core_action",
            "contract_piece": "GR/source core",
            "mathematical_form": "S_core[q,Psi,theta] is the EH/Newton source branch plus ordinary matter functor",
            "contract_status": "BACKGROUND_CONTRACT_ONLY",
            "failure_if_missing": "memory-zero proof would not connect to GR limit",
        },
        {
            "contract_id": "TSC972_2_active_X_kinetic",
            "contract_piece": "ungated X kinetic/operator slot",
            "mathematical_form": "S_X^kin=1/2 int_D sqrt(g)(A^ij nabla_i X nabla_j X + m_X^2 X^2)+S_boundary[X]",
            "contract_status": "RELATIVE_FORM_READY_NOT_PARENT_SIGNED",
            "failure_if_missing": "L_X degenerates or has no parent owner",
        },
        {
            "contract_id": "TSC972_3_observed_coupling_slot",
            "contract_piece": "double-zero observed/source coupling",
            "mathematical_form": "S_C=int sqrt(g) f(chi_D) C_obs[X,q(Phi),Psi,theta] with f(0)=f_prime(0)=0",
            "contract_status": "RELATIVE_FORM_READY_ORIGIN_UNSIGNED",
            "failure_if_missing": "selector/source exchange can return or double-zero becomes arbitrary closure",
        },
        {
            "contract_id": "TSC972_4_no_cross_slot_leak",
            "contract_piece": "no hidden X source outside C_obs",
            "mathematical_form": "delta_X(S_core+S_matter+S_chi+S_boundary_extra)=0 in local exterior except owned S_X boundary",
            "contract_status": "NOT_DERIVED",
            "failure_if_missing": "J_X survives even when f(0)=0",
        },
        {
            "contract_id": "TSC972_5_boundary_package",
            "contract_piece": "boundary/no-tail clause",
            "mathematical_form": "Pi_X delta X|partialD=0 and Pi_local dB_X=0, or Dirichlet/zero-flux/zero-mean class",
            "contract_status": "NOT_DERIVED",
            "failure_if_missing": "X boundary hair survives the positive-operator identity",
        },
        {
            "contract_id": "TSC972_6_covariance",
            "contract_piece": "total action covariance",
            "mathematical_form": "delta_xi S_parent=0 for the whole two-slot action, not for each slot separately",
            "contract_status": "RELATIVE_NOETHER_CONTRACT_READY",
            "failure_if_missing": "Bianchi identity cannot be used to cancel exchange terms",
        },
        {
            "contract_id": "TSC972_7_verdict",
            "contract_piece": "two-slot parent action contract",
            "mathematical_form": "S_parent=S_core+S_X^kin+int f(chi_D)C_obs+S_boundary",
            "contract_status": "CONTRACT_READY_PARENT_UNSIGNED",
            "failure_if_missing": "no local-GR or memory-zero claim; retain residual source rows",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def bianchi_identity_derivation() -> list[dict[str, str]]:
    specs = [
        {
            "identity_id": "BID972_0_covariant_variation",
            "step": "diffeomorphism variation of total action",
            "mathematical_form": "0=delta_xi S_parent=int sqrt(g)(E_q L_xi q + E_X L_xi X + E_chi L_xi chi_D + E_Psi L_xi Psi)+boundary",
            "status": "RELATIVE_IDENTITY_IF_CONTRACT_ADOPTED",
            "gap": "parent action contract not signed",
        },
        {
            "identity_id": "BID972_1_total_stress_identity",
            "step": "Noether/Bianchi identity",
            "mathematical_form": "nabla_mu(T_core^{mu nu}+T_X^{mu nu}+T_chi^{mu nu}+f T_C^{mu nu}) = E_X nabla^nu X + E_chi nabla^nu chi_D + E_Psi nabla^nu Psi + boundary",
            "status": "RELATIVE_DERIVED",
            "gap": "requires all stress pieces to come from the same covariant parent action",
        },
        {
            "identity_id": "BID972_2_X_equation_local_branch",
            "step": "active X equation at chi_D=0",
            "mathematical_form": "E_X=L_X X + f(chi_D) C_X; at chi_D=0 with f(0)=0, E_X=L_X X",
            "status": "RELATIVE_DERIVED",
            "gap": "L_X positivity/source-free/boundary data unsigned",
        },
        {
            "identity_id": "BID972_3_chi_equation_local_branch",
            "step": "selector equation at chi_D=0",
            "mathematical_form": "E_chi=E_chi^0 + f_prime(chi_D) C_obs; at chi_D=0 with f_prime(0)=0, memory coupling does not force chi_D",
            "status": "RELATIVE_DERIVED",
            "gap": "parent origin of double zero is not signed",
        },
        {
            "identity_id": "BID972_4_metric_stress_local_branch",
            "step": "memory stress at local zero",
            "mathematical_form": "T_memory=T_X^kin[X]+f(0)T_C; if positive operator gives X=0 and f(0)=0, T_memory=0",
            "status": "CONDITIONAL_DERIVED",
            "gap": "X=0 theorem still blocked by source/boundary/operator premises",
        },
        {
            "identity_id": "BID972_5_exchange_accounting",
            "step": "Bianchi exchange accounting",
            "mathematical_form": "nabla_mu(fT_C^{mu nu}) terms are balanced by E_chi nabla^nu chi_D and E_X nabla^nu X inside the total identity",
            "status": "RELATIVE_DERIVED_NOT_OWNER_SIGNED",
            "gap": "417 says Bianchi gate term and projected local flux are not derived",
        },
        {
            "identity_id": "BID972_6_verdict",
            "step": "two-slot Bianchi identity",
            "mathematical_form": "the identity is internally consistent as a contract, but does not parent-sign source-free X or boundary silence",
            "status": "BIANCHI_CONTRACT_READY_PARENT_UNSIGNED",
            "gap": "cannot claim local GR until contract ownership and zero theorem gates close",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def local_zero_gate() -> list[dict[str, str]]:
    specs = [
        {
            "gate_id": "LZG972_0_parent_contract",
            "gate": "two-slot action belongs to S_parent",
            "status": "false",
            "reason": "contract written but not extracted from primitive parent action",
        },
        {
            "gate_id": "LZG972_1_operator_positive",
            "gate": "L_X is self-adjoint positive with controlled kernel",
            "status": "false",
            "reason": "A^ij, m_X^2, gauge/zero-mode data are not parent-signed",
        },
        {
            "gate_id": "LZG972_2_source_zero",
            "gate": "all non-boundary X sources vanish at chi_D=0",
            "status": "false",
            "reason": "source-free S_X^kin, quotient matter blindness, and no hidden marker remain unsigned",
        },
        {
            "gate_id": "LZG972_3_boundary_zero",
            "gate": "boundary flux/lift vanishes",
            "status": "false",
            "reason": "417 boundary primitive, local projection flux, and secular drift gates fail",
        },
        {
            "gate_id": "LZG972_4_double_zero_origin",
            "gate": "f(0)=f_prime(0)=0 is parent-derived",
            "status": "false",
            "reason": "476 derives it as a requirement, not as parent origin",
        },
        {
            "gate_id": "LZG972_5_no_tower",
            "gate": "integrating out X cannot create non-EH/R10/R11 leakage",
            "status": "false",
            "reason": "963 no-integrated-out-tower gate is not derived",
        },
        {
            "gate_id": "LZG972_6_observable_zero_or_bound",
            "gate": "observable residual vector is zero or source-backed below bounds",
            "status": "false",
            "reason": "K_R10/K_PPN/K_clock/K_Gdot/K_orbital remain missing",
        },
        {
            "gate_id": "LZG972_7_verdict",
            "gate": "local memory zero theorem activates",
            "status": "false",
            "reason": "relative Bianchi contract helps, but theorem-zero acceptance gates are not met",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def residual_source_fill_ledger() -> list[dict[str, str]]:
    specs = [
        {
            "source_row_id": "RSF972_0_lambda_gap",
            "needed_quantity": "lambda_gap/m_X/operator lower bound",
            "why_priority": "first denominator for any retained X amplitude",
            "current_entry": "MISSING_A_MIN;MISSING_LAMBDA1_D;MISSING_MX2",
            "source_action": "find parent Hessian/operator sign row or keep residual unscored",
            "claim_status": "BLOCKED",
        },
        {
            "source_row_id": "RSF972_1_JX_source_norm",
            "needed_quantity": "J_X decomposition and norm",
            "why_priority": "distinguishes theorem-zero from finite driven memory",
            "current_entry": "MISSING_J_MATTER;MISSING_J_CHID;MISSING_J_BOUNDARY;MISSING_J_HISTORY",
            "source_action": "derive zero-source theorem or source finite current with units",
            "claim_status": "BLOCKED",
        },
        {
            "source_row_id": "RSF972_2_boundary_lift",
            "needed_quantity": "boundary_lift_norm/zero-flux proof",
            "why_priority": "positive operator cannot kill boundary hair without it",
            "current_entry": "MISSING_BOUNDARY_DATA",
            "source_action": "prove exact/topological no-tail or source finite boundary row",
            "claim_status": "BLOCKED",
        },
        {
            "source_row_id": "RSF972_3_double_zero_origin",
            "needed_quantity": "parent origin for f(0)=f_prime(0)=0",
            "why_priority": "prevents local selector/source coupling from being arbitrary closure",
            "current_entry": "MISSING_PARENT_SYMMETRY_OR_DETERMINANT_OR_NORM_SQUARE",
            "source_action": "derive symmetry/determinant/norm-square route or label as closure",
            "claim_status": "BLOCKED",
        },
        {
            "source_row_id": "RSF972_4_R10_projection",
            "needed_quantity": "K_R10 and alpha(lambda)",
            "why_priority": "first empirical fifth-force interface if X is finite",
            "current_entry": "MISSING_R10_PROJECTION;MISSING_REAL_BOUND_CURVE_LINK",
            "source_action": "source projection coefficient and real alpha(lambda) bound before scoring",
            "claim_status": "BLOCKED",
        },
        {
            "source_row_id": "RSF972_5_PPN_clock_orbital_projection",
            "needed_quantity": "K_PPN/K_clock/K_Gdot/K_orbital",
            "why_priority": "prevents finite memory from hiding outside R10",
            "current_entry": "MISSING_ARENA_PROJECTIONS",
            "source_action": "write arena projection maps with official/local bound sources",
            "claim_status": "BLOCKED",
        },
        {
            "source_row_id": "RSF972_6_score_gate",
            "needed_quantity": "valid_for_claim",
            "why_priority": "keeps source-fill honest",
            "current_entry": "false",
            "source_action": "turn true only after numeric/theorem-zero inputs, units, source paths, and bound comparison pass",
            "claim_status": "FORCED_FALSE",
        },
    ]
    return [
        {
            **spec,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def claim_gates() -> list[dict[str, str]]:
    specs = [
        {
            "gate_id": "CGATE972_0_two_slot_parent_action",
            "claim": "two-slot memory action is parent-signed",
            "current_evidence": "contract ready only",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE972_1_Bianchi_identity",
            "claim": "Bianchi identity closes the two-slot memory exchange",
            "current_evidence": "relative Noether identity written; ownership unsigned",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE972_2_memory_zero",
            "claim": "memory/class scalar X vanishes locally",
            "current_evidence": "positive-operator route blocked by source/boundary/operator premises",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE972_3_no_tower",
            "claim": "no integrated-out scalar/non-EH tower remains",
            "current_evidence": "963 no-tower gate remains not derived",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE972_4_residual_score",
            "claim": "retained memory residual is scoreable",
            "current_evidence": "source-fill ledger contains MISSING rows only",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE972_5_local_GR",
            "claim": "local GR/Newton promotion follows from memory sector",
            "current_evidence": "no theorem-zero and no residual pass",
            "gate_pass": "false",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def decisions() -> list[dict[str, str]]:
    specs = [
        {
            "decision_id": "DEC972_0_two_slot_contract",
            "topic": "two-slot action",
            "result": "exact_contract_written_parent_unsigned",
            "reason": "the action split avoids operator degeneracy and has a clean local branch, but is not parent-owned",
            "next_action": "try to sign source-free S_X^kin and boundary/no-tail package",
        },
        {
            "decision_id": "DEC972_1_Bianchi",
            "topic": "Bianchi identity",
            "result": "relative_Noether_identity_ready",
            "reason": "total covariant action would conserve total stress on shell, including fT_C exchange",
            "next_action": "derive ownership of the total action and local boundary projection silence",
        },
        {
            "decision_id": "DEC972_2_residual_fill",
            "topic": "retained residual source fill",
            "result": "minimum_rows_opened_nonclaim",
            "reason": "if parent signatures fail, memory must be scored through lambda/J/boundary/K rows",
            "next_action": "source only real/theorem-zero rows; no placeholders count",
        },
        {
            "decision_id": "DEC972_3_best_next",
            "topic": "next checkpoint",
            "result": "source_free_SXkin_and_boundary_zero_or_first_residual_row",
            "reason": "the Bianchi algebra is no longer the main mystery; the blocker is source-free kinetic ownership plus boundary zero",
            "next_action": "attempt source-free S_X^kin and boundary zero proof before numeric residual scoring",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "973-Y5-R10-source-free-SXkin-and-boundary-zero-proof-or-first-memory-residual-source-row.md",
            "objective": "try to prove the ungated memory kinetic sector is source-free and boundary-silent; if it fails, fill the first real retained memory residual source row",
            "include": "J_X=0 decomposition, quotient matter blindness, boundary flux/no-tail, positive operator inputs, lambda/J/boundary source rows",
            "exclude": "local-GR claim, invented coefficients, unsourced bound rows, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    bianchi_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    formalization_count = formalization_changed_after_start()
    rows = [
        {
            "check_id": "V972_0_source_paths_exist",
            "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail",
            "detail": "all cited local source paths exist",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V972_1_source_needles_found",
            "result": "pass" if all(row["needle_found"] == "true" for row in sources) else "fail",
            "detail": "all source needles found",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V972_2_two_slot_contract_ready",
            "result": "pass"
            if any(row["contract_id"] == "TSC972_7_verdict" and row["contract_status"] == "CONTRACT_READY_PARENT_UNSIGNED" for row in contract_rows)
            else "fail",
            "detail": "two-slot action contract written and kept nonclaim",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V972_3_Bianchi_relative_identity",
            "result": "pass"
            if any(row["identity_id"] == "BID972_6_verdict" and row["status"] == "BIANCHI_CONTRACT_READY_PARENT_UNSIGNED" for row in bianchi_rows)
            else "fail",
            "detail": "relative Noether/Bianchi identity written without parent-signing claim",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V972_4_zero_gates_false",
            "result": "pass" if all(row["status"] == "false" for row in zero_rows) else "fail",
            "detail": "all local zero theorem gates remain false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V972_5_residual_source_fill_nonclaim",
            "result": "pass" if all(row["valid_for_claim"] == "false" for row in residual_rows) else "fail",
            "detail": "residual source-fill ledger opened with no claim rows",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V972_6_claim_gates_false",
            "result": "pass" if all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows) else "fail",
            "detail": "all memory/local-GR claim gates remain false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V972_7_decisions_nonclaim",
            "result": "pass" if all(row["claim_allowed"] == "false" for row in decision_rows) else "fail",
            "detail": "decision ledger remains nonclaim",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V972_8_next_target_written",
            "result": "pass" if len(target_rows) == 1 and target_rows[0]["valid_for_claim"] == "false" else "fail",
            "detail": "973 source-free S_X/boundary-zero target selected",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V972_9_formalization_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization-workbench modified-file count since script start is {formalization_count}",
            "generated_utc": stamp(),
        },
    ]
    rows.append(
        {
            "check_id": "V972_10_validation_rows_ready",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "972 validation pack assembled",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    bianchi_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 972 Y5 R10: Parent Two-Slot Memory Action And Bianchi Identity Or Residual Source Fill

Status: `Y5_R10_972_two_slot_Bianchi_contract_ready_parent_unsigned_residual_source_fill_opened_nonclaim`

Claim ceiling: no parent two-slot action proof, no Bianchi closure claim, no memory theorem-zero, no residual bound pass, no R10/R11 pass, no EH/Newton/local-GR claim is made.

## Readout

This checkpoint gets the algebra into the right shape.

The two-slot action contract is:

`S_parent = S_core[q,Psi,theta] + S_X^kin[X,D,q] + int sqrt(g) f(chi_D) C_obs[X,q(Phi),Psi,theta] + S_boundary`.

If that whole object is a covariant parent action, then the Noether identity is ordinary and honest:

`nabla_mu(T_core^{{mu nu}}+T_X^{{mu nu}}+T_chi^{{mu nu}}+fT_C^{{mu nu}}) = E_X nabla^nu X + E_chi nabla^nu chi_D + E_Psi nabla^nu Psi + boundary`.

At `chi_D=0`, `f(0)=f_prime(0)=0` keeps `L_X X=0` active and removes the local observed/source exchange. If the positive-operator, source-zero, and boundary-zero premises are also signed, then `X=0` and memory stress vanishes locally.

So the route is mathematically coherent. It is not yet parent-signed. The remaining blocker is sharper now: prove ungated `S_X^kin` is source-free and boundary-silent, or start filling real retained memory residual rows. No mist, no fake local-GR pass.

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Two-Slot Action Contract

{md_table(contract_rows, ["contract_id", "contract_piece", "contract_status", "failure_if_missing"])}

## Bianchi Identity Derivation

{md_table(bianchi_rows, ["identity_id", "step", "status", "gap"])}

## Local Zero Theorem Gate

{md_table(zero_rows, ["gate_id", "gate", "status", "reason"])}

## Residual Source Fill Ledger

{md_table(residual_rows, ["source_row_id", "needed_quantity", "why_priority", "current_entry", "source_action", "claim_status", "valid_for_claim"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    contract_rows = two_slot_action_contract()
    bianchi_rows = bianchi_identity_derivation()
    zero_rows = local_zero_gate()
    residual_rows = residual_source_fill_ledger()
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        contract_rows,
        bianchi_rows,
        zero_rows,
        residual_rows,
        claim_rows,
        decision_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_972_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_972_TWO_SLOT_ACTION_CONTRACT.csv",
        contract_rows,
        ["contract_id", "contract_piece", "mathematical_form", "contract_status", "failure_if_missing", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_972_BIANCHI_IDENTITY_DERIVATION.csv",
        bianchi_rows,
        ["identity_id", "step", "mathematical_form", "status", "gap", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_972_LOCAL_ZERO_THEOREM_GATE.csv",
        zero_rows,
        ["gate_id", "gate", "status", "reason", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_972_RESIDUAL_SOURCE_FILL_LEDGER.csv",
        residual_rows,
        ["source_row_id", "needed_quantity", "why_priority", "current_entry", "source_action", "claim_status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_972_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_972_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_972_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_972_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(
        sources,
        contract_rows,
        bianchi_rows,
        zero_rows,
        residual_rows,
        claim_rows,
        decision_rows,
        target_rows,
        validation_rows,
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "971-Y5-R10-active-memory-zero-vs-double-zero-decoupling-branch-choice-or-runner-fill.md"
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
    since = SCRIPT_START_UTC.astimezone().strftime("%Y-%m-%dT%H:%M:%S")
    literal = str(FORMALIZATION).replace("'", "''")
    command = (
        "$since=[datetime]::Parse('"
        + since
        + "'); "
        + "$count=(Get-ChildItem -LiteralPath '"
        + literal
        + "' -Recurse -File | Where-Object { $_.LastWriteTime -gt $since } | Measure-Object).Count; "
        + "Write-Output $count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    try:
        return int(completed.stdout.strip().splitlines()[-1])
    except (IndexError, ValueError):
        return -2


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "970_doc",
            "path": "970-Y5-R10-minimal-quadratic-memory-action-construction-or-strict-residual-runner.md",
            "role": "branch fork handoff",
            "needle": "ADB970_3_verdict",
        },
        {
            "source_id": "970_branch_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_970_ACTIVE_VS_DOUBLE_ZERO_BRANCH_AUDIT.csv",
            "role": "active operator vs double-zero audit",
            "needle": "ADB970_2_hybrid_active_hidden_gated_observed",
        },
        {
            "source_id": "970_source_boundary",
            "path": "source-intake/mts_residuals/P8_Y5_R10_970_SOURCE_BOUNDARY_GATE.csv",
            "role": "source/boundary blockers",
            "needle": "SBG970_8_verdict",
        },
        {
            "source_id": "970_residual_schema",
            "path": "source-intake/mts_residuals/P8_Y5_R10_970_STRICT_RESIDUAL_RUNNER_SCHEMA.csv",
            "role": "strict retained residual input schema",
            "needle": "RRS970_6_K_R10",
        },
        {
            "source_id": "967_memory_lemma_doc",
            "path": "967-Y5-R10-readout-after-variation-parent-schema-theorem-or-memory-positive-operator-lemma.md",
            "role": "positive-operator lemma and readout-after-variation schema",
            "needle": "MPO967_6_verdict",
        },
        {
            "source_id": "968_memory_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
            "role": "memory operator missing inputs",
            "needle": "MOI968_8_verdict",
        },
        {
            "source_id": "476_double_zero_doc",
            "path": "476-double-zero-memory-coupling-origin-or-coefficient-runner.md",
            "role": "double-zero requirement and origin gap",
            "needle": "p >= 2 is the minimum local-GR-safe memory gate",
        },
        {
            "source_id": "476_variation_test",
            "path": "source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_VARIATION_TEST.csv",
            "role": "quadratic gate variation test",
            "needle": "pass_as_sufficient_contract",
        },
        {
            "source_id": "943_coframe_contract",
            "path": "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
            "role": "observed coframe/matter coupling descent contract",
            "needle": "contract_exact_but_unsigned",
        },
        {
            "source_id": "944_descent_proof",
            "path": "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md",
            "role": "conditional quotient descent proof and counterexamples",
            "needle": "QDG944_7_total",
        },
        {
            "source_id": "945_q_candidate",
            "path": "945-Y5-R10-parent-q-map-Obs-e-functor-construction-or-first-frame-leak-bound-pack.md",
            "role": "q-candidate and kernel ownership gap",
            "needle": "QMAP945_6_verdict",
        },
        {
            "source_id": "963_no_tower",
            "path": "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
            "role": "no-integrated-out-tower blocker",
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


def branch_selection_audit() -> list[dict[str, str]]:
    specs = [
        {
            "branch_id": "BSA971_0_active_operator_only",
            "candidate_branch": "active_positive_operator_only",
            "mathematical_content": "S_parent contains S_X^kin and local branch tries L_X X=0 -> X=0",
            "benefit": "real theorem-zero route if source and boundary silence are parent-signed",
            "failure": "J_X, boundary flux, X owner, and arena couplings are not signed",
            "status": "NOT_SELECTABLE_AS_CLAIM",
        },
        {
            "branch_id": "BSA971_1_double_zero_all_memory",
            "candidate_branch": "double_zero_gates_entire_memory_action",
            "mathematical_content": "S_mem=f(chi_D)L_mem[X] with f(0)=f_prime(0)=0",
            "benefit": "local stress and selector exchange vanish at chi_D=0",
            "failure": "if f gates the kinetic/operator term, the local X equation degenerates and no X=0 proof follows",
            "status": "REJECT_AS_THEOREM_ZERO_ROUTE",
        },
        {
            "branch_id": "BSA971_2_two_slot_hybrid",
            "candidate_branch": "active_hidden_operator_plus_double_zero_observed_coupling",
            "mathematical_content": "S_parent=S_core+S_X^kin[X]+f(chi_D)C_obs[X,q(Phi),Psi]+S_matter[q(Phi),Psi,theta]",
            "benefit": "keeps L_X active while double-zero silences observed/source coupling at chi_D=0",
            "failure": "parent split, Bianchi ownership, source silence, boundary data, and no-tower certificate are unsigned",
            "status": "BEST_DERIVATION_TARGET_NOT_PARENT_SIGNED",
        },
        {
            "branch_id": "BSA971_3_retained_residual",
            "candidate_branch": "finite_memory_residual_runner",
            "mathematical_content": "treat X as retained finite local residual with lambda_gap, source norm, boundary lift, and K_i projections",
            "benefit": "honest empirical route if derivation stalls",
            "failure": "all required numerical/source-backed inputs remain missing",
            "status": "FALLBACK_READY_NONCLAIM",
        },
        {
            "branch_id": "BSA971_4_verdict",
            "candidate_branch": "971 branch choice",
            "mathematical_content": "select two-slot hybrid as next derivation target, not as a claim",
            "benefit": "least self-defeating route: active equation remains active, observed coupling is locally gated",
            "failure": "no parent-action ownership yet",
            "status": "TWO_SLOT_HYBRID_SELECTED_AS_NONCLAIM_TARGET",
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


def parent_split_derivation_attempt() -> list[dict[str, str]]:
    specs = [
        {
            "step_id": "PSD971_0_two_slot_ansatz",
            "claim_tested": "parent action can split memory into kinetic/operator slot and observed/source coupling slot",
            "mathematical_form": "S_parent=S_core[q,Psi]+S_X^kin[X,D,q]+f(chi_D)C_obs[X,q,Psi]+S_boundary",
            "derivation_status": "CANDIDATE_WRITTEN",
            "gap": "not extracted from a signed parent action",
        },
        {
            "step_id": "PSD971_1_X_variation",
            "claim_tested": "X equation remains active at chi_D=0",
            "mathematical_form": "delta_X S: L_X X + f(chi_D) delta_X C_obs = 0; at chi_D=0 and f(0)=0, L_X X=0",
            "derivation_status": "RELATIVE_CHAIN_VALID",
            "gap": "requires f to gate only C_obs, not S_X^kin; L_X positivity and boundary data still unsigned",
        },
        {
            "step_id": "PSD971_2_chi_variation",
            "claim_tested": "domain selector is not forced by memory coupling",
            "mathematical_form": "delta_chi S contains f_prime(chi_D) C_obs + other chi terms; f_prime(0)=0 kills the memory exchange term",
            "derivation_status": "RELATIVE_CHAIN_VALID",
            "gap": "parent origin of f(0)=f_prime(0)=0 remains conditional",
        },
        {
            "step_id": "PSD971_3_metric_variation",
            "claim_tested": "observed memory stress is silent locally",
            "mathematical_form": "T_memory=T_X^kin[X]+f(0)T_C; if L_X plus boundary proves X=0, then T_X^kin=0 and f(0)T_C=0",
            "derivation_status": "CONDITIONAL_OK",
            "gap": "depends on active X=0 proof; otherwise T_X^kin remains a finite stress residual",
        },
        {
            "step_id": "PSD971_4_matter_source",
            "claim_tested": "ordinary matter does not source X at chi_D=0",
            "mathematical_form": "J_X=J_X^kin + f(0)J_X^obs; with source-free S_X^kin and f(0)=0, J_X=0",
            "derivation_status": "NOT_DERIVED",
            "gap": "source-free S_X^kin and quotient matter blindness are not parent-signed",
        },
        {
            "step_id": "PSD971_5_boundary_source",
            "claim_tested": "boundary/local projection cannot inject X",
            "mathematical_form": "boundary_flux_X=0 and Pi_local dB_X=0",
            "derivation_status": "NOT_DERIVED",
            "gap": "boundary no-hair/Bianchi/local projection silence remains open",
        },
        {
            "step_id": "PSD971_6_no_tower",
            "claim_tested": "solving X after the split does not regenerate local scalar/non-EH leakage",
            "mathematical_form": "if X=0 before reduction, no <J,L^{-1}J> tail; if not, retained R10/R11 residual rows are mandatory",
            "derivation_status": "NOT_DERIVED",
            "gap": "no-extra-scalar/no-integrated-out-tower certificate remains unsigned",
        },
        {
            "step_id": "PSD971_7_verdict",
            "claim_tested": "two-slot split proves local memory zero",
            "mathematical_form": "two-slot split avoids operator degeneracy but still needs source, boundary, positivity, and no-tower signatures",
            "derivation_status": "RELATIVE_ROUTE_FOUND_PARENT_UNSIGNED",
            "gap": "cannot claim local GR; next checkpoint must parent-sign the two-slot action or fill residual inputs",
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


def bianchi_variation_gate() -> list[dict[str, str]]:
    specs = [
        {
            "gate_id": "BVG971_0_operator_not_gated",
            "gate": "S_X^kin is not multiplied by f(chi_D)",
            "pass_status": "candidate_only",
            "reason": "needed to avoid degenerating L_X at chi_D=0",
            "required_source": "parent action term separating S_X^kin from C_obs",
        },
        {
            "gate_id": "BVG971_1_coupling_double_zero",
            "gate": "only C_obs/source coupling is multiplied by f with f(0)=f_prime(0)=0",
            "pass_status": "conditional",
            "reason": "476 proves this as a local-silence requirement, not as parent origin",
            "required_source": "parent symmetry/determinant/norm-square origin for f",
        },
        {
            "gate_id": "BVG971_2_bianchi_conservation",
            "gate": "Bianchi identity remains owned after the split",
            "pass_status": "false",
            "reason": "gated coupling can exchange stress with chi_D/domain sector unless total stress accounting is signed",
            "required_source": "nabla_mu(T_core+T_X+T_chi+fT_C)=0 on parent equations",
        },
        {
            "gate_id": "BVG971_3_source_free_kinetic_X",
            "gate": "S_X^kin has no ordinary matter/source/worldtube vertex",
            "pass_status": "false",
            "reason": "943/944/945 make matter blindness conditional; 968 lists J_X=0 as missing",
            "required_source": "quotient descent plus source-free X kinetic sector",
        },
        {
            "gate_id": "BVG971_4_boundary_zero",
            "gate": "S_X boundary term gives zero compact local flux",
            "pass_status": "false",
            "reason": "boundary exchange/no-hair and local projection silence remain unsigned",
            "required_source": "parent-selected D and boundary primitive/no-tail certificate",
        },
        {
            "gate_id": "BVG971_5_observed_coupling_map",
            "gate": "all residual observable couplings are zero or source-backed",
            "pass_status": "false",
            "reason": "R10/PPN/clock/Gdot/orbital K_i projections are missing",
            "required_source": "arena projection rows with units and bound sources",
        },
        {
            "gate_id": "BVG971_6_verdict",
            "gate": "two-slot split accepted as parent proof",
            "pass_status": "false",
            "reason": "the split is the best nonclaim route, but parent ownership and conservation are not signed",
            "required_source": "all BVG971_0..5 signed",
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


def residual_minimum_rows() -> list[dict[str, str]]:
    specs = [
        {
            "row_id": "RMIN971_0_lambda_gap",
            "quantity": "lambda_gap or m_X",
            "why_needed": "sets the memory amplitude/range denominator if X is retained",
            "current_value": "MISSING_A_MIN;MISSING_LAMBDA1_D;MISSING_MX2",
            "acceptance_condition": "numeric or theorem-zero parent source path with units",
        },
        {
            "row_id": "RMIN971_1_JX_norm",
            "quantity": "||J_X|| and source decomposition",
            "why_needed": "decides whether active operator proves zero or drives finite X",
            "current_value": "MISSING_J_MATTER;MISSING_J_CHID;MISSING_J_BOUNDARY;MISSING_J_HISTORY",
            "acceptance_condition": "zero theorem or finite source norm with units/source path",
        },
        {
            "row_id": "RMIN971_2_boundary_lift",
            "quantity": "boundary_lift_norm",
            "why_needed": "captures local boundary hair if no-hair fails",
            "current_value": "MISSING_BOUNDARY_DATA",
            "acceptance_condition": "zero flux proof or finite norm with boundary/source provenance",
        },
        {
            "row_id": "RMIN971_3_K_R10",
            "quantity": "K_R10 and alpha(lambda)",
            "why_needed": "maps finite X to fifth-force/R10 tests",
            "current_value": "MISSING_R10_PROJECTION;MISSING_REAL_ALPHA_BOUND_LINK",
            "acceptance_condition": "source-backed projection and real bound curve",
        },
        {
            "row_id": "RMIN971_4_K_PPN",
            "quantity": "K_PPN vector",
            "why_needed": "maps X or grad X to gamma/beta/preferred-frame coefficients",
            "current_value": "MISSING_PPN_PROJECTION",
            "acceptance_condition": "weak-field projection with official/local bound source",
        },
        {
            "row_id": "RMIN971_5_K_clock_Gdot_orbital",
            "quantity": "K_clock, K_Gdot, K_orbital",
            "why_needed": "prevents memory residual hiding outside R10/PPN",
            "current_value": "MISSING_CLOCK_PROJECTION;MISSING_GDOT_PROJECTION;MISSING_ORBITAL_PROJECTION",
            "acceptance_condition": "arena-specific projection with units/source path",
        },
        {
            "row_id": "RMIN971_6_claim_policy",
            "quantity": "valid_for_claim",
            "why_needed": "prevents placeholders from becoming evidence",
            "current_value": "false",
            "acceptance_condition": "true only when every required quantity is numeric/theorem-zero, sourced, unit-checked, and bound-compared",
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
            "gate_id": "CGATE971_0_two_slot_parent_action",
            "claim": "parent MTS owns two-slot memory action",
            "current_evidence": "relative ansatz written, not extracted from parent action",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE971_1_active_X_zero",
            "claim": "active X equation proves X=0 locally",
            "current_evidence": "L_X route found but source/boundary/positivity inputs unsigned",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE971_2_double_zero_source_silence",
            "claim": "double-zero coupling silences observed/source memory branch",
            "current_evidence": "valid conditional chain, parent origin of f and Bianchi accounting unsigned",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE971_3_bianchi_safe_split",
            "claim": "two-slot split preserves conservation/covariance",
            "current_evidence": "total stress accounting not signed",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE971_4_residual_score",
            "claim": "finite memory residual is scoreable",
            "current_evidence": "minimum rows still contain MISSING markers",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE971_5_local_GR",
            "claim": "memory branch supports local GR/Newton promotion",
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
            "decision_id": "DEC971_0_branch_choice",
            "topic": "branch selection",
            "result": "two_slot_hybrid_selected_as_next_derivation_target",
            "reason": "it avoids the 970 problem by keeping the X operator active while gating only observed/source coupling",
            "next_action": "try to parent-sign the two-slot action and Bianchi accounting",
        },
        {
            "decision_id": "DEC971_1_claim_status",
            "topic": "claim status",
            "result": "nonclaim",
            "reason": "the two-slot split is a relative derivation route, not a parent-owned theorem",
            "next_action": "keep all memory/local-GR gates false",
        },
        {
            "decision_id": "DEC971_2_residual_policy",
            "topic": "if two-slot proof fails",
            "result": "retained_residual_runner_required",
            "reason": "finite X must be bounded through lambda_gap, J_X, boundary lift, and K_i rather than hidden by closure",
            "next_action": "fill residual minimum rows only from real source paths",
        },
        {
            "decision_id": "DEC971_3_best_next",
            "topic": "next checkpoint",
            "result": "parent_two_slot_action_and_bianchi_identity_or_residual_source_fill",
            "reason": "the next locked door is conservation/ownership of the split, not more notation",
            "next_action": "attempt a parent two-slot clause; if it fails, begin real residual input acquisition",
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
            "next_target": "972-Y5-R10-parent-two-slot-memory-action-and-Bianchi-identity-or-residual-source-fill.md",
            "objective": "try to parent-sign the two-slot memory action S_X^kin plus double-zero observed coupling and its Bianchi identity; if not, start source-backed residual input fill",
            "include": "S_X^kin ownership, f(chi_D)C_obs ownership, total stress conservation, zero-source/boundary gates, residual lambda/J/K rows",
            "exclude": "local-GR claim, invented coefficients, readout closure as theorem-zero, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    branch_rows: list[dict[str, str]],
    split_rows: list[dict[str, str]],
    bianchi_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    formalization_count = formalization_changed_after_start()
    rows = [
        {
            "check_id": "V971_0_source_paths_exist",
            "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail",
            "detail": "all cited local source paths exist",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V971_1_source_needles_found",
            "result": "pass" if all(row["needle_found"] == "true" for row in sources) else "fail",
            "detail": "all source needles found",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V971_2_two_slot_selected_nonclaim",
            "result": "pass"
            if any(row["branch_id"] == "BSA971_4_verdict" and row["status"] == "TWO_SLOT_HYBRID_SELECTED_AS_NONCLAIM_TARGET" for row in branch_rows)
            else "fail",
            "detail": "two-slot hybrid selected only as nonclaim derivation target",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V971_3_X_variation_active",
            "result": "pass"
            if any(row["step_id"] == "PSD971_1_X_variation" and row["derivation_status"] == "RELATIVE_CHAIN_VALID" for row in split_rows)
            else "fail",
            "detail": "relative X-variation keeps L_X active at chi_D=0",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V971_4_parent_unsigned_verdict",
            "result": "pass"
            if any(row["step_id"] == "PSD971_7_verdict" and row["derivation_status"] == "RELATIVE_ROUTE_FOUND_PARENT_UNSIGNED" for row in split_rows)
            else "fail",
            "detail": "split route is not parent-signed",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V971_5_bianchi_gate_blocks_claim",
            "result": "pass"
            if any(row["gate_id"] == "BVG971_6_verdict" and row["pass_status"] == "false" for row in bianchi_rows)
            else "fail",
            "detail": "Bianchi/variation gate blocks parent proof claim",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V971_6_residual_rows_nonclaim",
            "result": "pass" if all(row["valid_for_claim"] == "false" for row in residual_rows) else "fail",
            "detail": "residual minimum rows remain nonclaim",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V971_7_claim_gates_false",
            "result": "pass" if all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows) else "fail",
            "detail": "all branch/local-GR claim gates remain false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V971_8_decisions_nonclaim",
            "result": "pass" if all(row["claim_allowed"] == "false" for row in decision_rows) else "fail",
            "detail": "decision ledger remains nonclaim",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V971_9_next_target_written",
            "result": "pass" if len(target_rows) == 1 and target_rows[0]["valid_for_claim"] == "false" else "fail",
            "detail": "972 two-slot/Bianchi or residual-fill target selected",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V971_10_formalization_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization-workbench modified-file count since script start is {formalization_count}",
            "generated_utc": stamp(),
        },
    ]
    rows.append(
        {
            "check_id": "V971_11_validation_rows_ready",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "971 validation pack assembled",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    branch_rows: list[dict[str, str]],
    split_rows: list[dict[str, str]],
    bianchi_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 971 Y5 R10: Active Memory Zero Vs Double-Zero Decoupling Branch Choice Or Runner Fill

Status: `Y5_R10_971_two_slot_hybrid_route_found_parent_unsigned_residual_minimum_rows_retained_nonclaim`

Claim ceiling: no two-slot parent action proof, no active memory zero theorem, no double-zero theorem-zero, no memory residual bound pass, no R10/R11 pass, no EH/Newton/local-GR claim is made.

## Readout

This checkpoint finds the best current route through the 970 fork.

The route is not to gate the whole memory action. That kills the local stress, yes, but it also risks killing the operator that was supposed to prove `X=0`.

The cleaner route is a two-slot split:

`S_parent = S_core + S_X^kin[X] + f(chi_D) C_obs[X,q(Phi),Psi] + S_boundary`.

Then at the local branch `chi_D=0` with `f(0)=f_prime(0)=0`:

- the `X` equation remains active: `L_X X = 0`;
- the observed/source coupling is locally silent;
- the selector exchange term is silent;
- if positivity, source-free kinetic sector, and boundary zero are signed, `X=0` follows without a plateau axiom.

That is genuinely better than the 970 alternatives. But it is not yet a parent theorem. The current corpus does not sign the two-slot action, Bianchi accounting, source-free `S_X^kin`, boundary no-hair, or no-integrated-out-tower certificate. So 971 selects the two-slot hybrid as the next derivation target, not as evidence.

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Branch Selection Audit

{md_table(branch_rows, ["branch_id", "candidate_branch", "benefit", "failure", "status"])}

## Parent Split Derivation Attempt

{md_table(split_rows, ["step_id", "claim_tested", "derivation_status", "gap"])}

## Bianchi Variation Gate

{md_table(bianchi_rows, ["gate_id", "gate", "pass_status", "reason", "required_source"])}

## Residual Minimum Rows

{md_table(residual_rows, ["row_id", "quantity", "why_needed", "current_value", "acceptance_condition", "valid_for_claim"])}

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
    branch_rows = branch_selection_audit()
    split_rows = parent_split_derivation_attempt()
    bianchi_rows = bianchi_variation_gate()
    residual_rows = residual_minimum_rows()
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        branch_rows,
        split_rows,
        bianchi_rows,
        residual_rows,
        claim_rows,
        decision_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_971_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_971_BRANCH_SELECTION_AUDIT.csv",
        branch_rows,
        ["branch_id", "candidate_branch", "mathematical_content", "benefit", "failure", "status", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_971_PARENT_SPLIT_DERIVATION_ATTEMPT.csv",
        split_rows,
        ["step_id", "claim_tested", "mathematical_form", "derivation_status", "gap", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_971_BIANCHI_VARIATION_GATE.csv",
        bianchi_rows,
        ["gate_id", "gate", "pass_status", "reason", "required_source", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_971_RESIDUAL_MINIMUM_ROWS.csv",
        residual_rows,
        ["row_id", "quantity", "why_needed", "current_value", "acceptance_condition", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_971_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_971_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_971_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_971_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(
        sources,
        branch_rows,
        split_rows,
        bianchi_rows,
        residual_rows,
        claim_rows,
        decision_rows,
        target_rows,
        validation_rows,
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "967-Y5-R10-readout-after-variation-parent-schema-theorem-or-memory-positive-operator-lemma.md"
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
            "source_id": "966_doc",
            "path": "966-Y5-R10-local-invariant-generator-elimination-or-R2FR-curve-digitizer.md",
            "role": "handoff: readout projector selected as first generator to remove",
            "needle": "GE966_0_readout_projector",
        },
        {
            "source_id": "966_contracts",
            "path": "source-intake/mts_residuals/P8_Y5_R10_966_PARTIAL_THEOREM_CONTRACTS.csv",
            "role": "readout domain and memory positive operator contracts",
            "needle": "PTC966_3_positive_memory_operator",
        },
        {
            "source_id": "422_readout",
            "path": "422-matter-functor-blindness-readout-after-variation-theorem-attempt.md",
            "role": "original readout-after-variation no-cheat theorem contract",
            "needle": "readout_after_variation_contract_written",
        },
        {
            "source_id": "421_fibre",
            "path": "421-finite-fibre-spectrum-decoupling-theorem-attempt.md",
            "role": "readout-selected component and finite-fibre scalar counterexample source",
            "needle": "readout_selected_active_block",
        },
        {
            "source_id": "423_minimality",
            "path": "423-parent-action-minimality-no-extension-theorem-attempt.md",
            "role": "post-readout EFT and active projector countermodel source",
            "needle": "post_readout_reduced_action",
        },
        {
            "source_id": "417_boundary",
            "path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "role": "memory/boundary exchange and Bianchi blocker source",
            "needle": "Bianchi_gate_owned",
        },
        {
            "source_id": "963_scalar",
            "path": "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
            "role": "no-extra-scalar and finite scalar/R2-fR blocker source",
            "needle": "NES963_2_no_local_kinetic_scalar",
        },
        {
            "source_id": "965_algebra",
            "path": "965-Y5-R10-primitive-quotient-no-natural-marker-theorem-or-R2FR-full-curve-intake.md",
            "role": "local invariant algebra and memory/class scalar blocker",
            "needle": "ALG965_5_memory_class_scalar",
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


def readout_schema_theorem_attempt() -> list[dict[str, str]]:
    specs = [
        {
            "attempt_id": "RAV967_0_domain_separation",
            "theorem_piece": "separate parent configuration, solution space, and observables",
            "claim_shape": "Conf_parent --S_parent--> equations; Sol(S_parent) --R_read--> Obs",
            "status": "formal_schema_clean",
            "proof_or_failure": "if R_read is only a map on Sol(S_parent), it is not in the variational domain of S_parent",
            "blocks": "readout as parent action argument",
            "remaining_gap": "corpus still must sign that every published/reduced readout obeys this domain separation",
        },
        {
            "attempt_id": "RAV967_1_no_variation_slot",
            "theorem_piece": "no readout variation slot",
            "claim_shape": "delta S_parent/delta P_read is absent because P_read not in Conf_parent",
            "status": "conditional_theorem",
            "proof_or_failure": "the variational derivative cannot be formed for a non-argument; any term depending on P_read defines a different parent theory",
            "blocks": "P_read source term",
            "remaining_gap": "parent action schema exclusion is a contract unless the corpus defines Conf_parent with this exclusion",
        },
        {
            "attempt_id": "RAV967_2_order_of_operations",
            "theorem_piece": "variation before readout",
            "claim_shape": "vary S_parent, solve E_A=0, then evaluate R_read(Phi_sol)",
            "status": "conditional_pass",
            "proof_or_failure": "readout changes reported observables, not the parent Euler-Lagrange equations",
            "blocks": "readout-selected Euler-Lagrange terms",
            "remaining_gap": "reduced EFT shortcuts must be explicitly forbidden from theorem-zero credit",
        },
        {
            "attempt_id": "RAV967_3_reduced_action_tax",
            "theorem_piece": "reduced action no-cheat rule",
            "claim_shape": "S_red[O]=S_parent[section(O)] varied as an action is new EFT, not parent readout",
            "status": "guardrail_pass_not_elimination",
            "proof_or_failure": "a varied reduced action can generate projector terms, so it must be retained and tested rather than counted as parent-zero",
            "blocks": "closure-zero promoted from reduced action",
            "remaining_gap": "does not forbid someone adding S_red; it only demotes it to a retained branch",
        },
        {
            "attempt_id": "RAV967_4_chain_rule_scope",
            "theorem_piece": "matter/source chain rule",
            "claim_shape": "delta S_matter/delta hidden Z vanishes only if S_matter factors through observed geometry and universal constants",
            "status": "not_closed_by_readout_alone",
            "proof_or_failure": "readout silence does not prove matter factorization or species/fibre blindness",
            "blocks": "overclaim that readout theorem proves local GR",
            "remaining_gap": "must still prove matter factorization, no species prefactors, finite-fibre blindness, and same-frame EH/source",
        },
        {
            "attempt_id": "RAV967_5_verdict",
            "theorem_piece": "readout projector generator elimination",
            "claim_shape": "post-readout projector cannot source parent equations",
            "status": "CONDITIONAL_SCHEMA_THEOREM_WRITTEN_NOT_PARENT_SIGNED",
            "proof_or_failure": "the logical theorem is clean under domain separation, but the current corpus has not globally signed that parent schema",
            "blocks": "unconditional generator removal",
            "remaining_gap": "parent action definition must explicitly exclude readout variables and reduced-action backreaction",
        },
    ]
    rows = []
    for spec in specs:
        rows.append({**spec, "claim_allowed": "false", "valid_for_claim": "false", "generated_utc": stamp()})
    return rows


def readout_countermodel_audit() -> list[dict[str, str]]:
    specs = [
        (
            "RCM967_0_reduced_EFT",
            "varied readout-reduced action S_red[P_read Phi]",
            "legal_as_new_EFT",
            "adds projector-dependent Euler-Lagrange terms while looking like observation",
            "exclude from parent theorem-zero; retain as explicit residual branch",
            "not_killed_by_readout_contract_alone",
        ),
        (
            "RCM967_1_section_choice",
            "representative section s:Obs->Conf_parent varied as physical",
            "live_if_section_backreacts",
            "active representative labels return through section dependence",
            "prove section is gauge/readout-only or pay variation tax",
            "not_parent_killed",
        ),
        (
            "RCM967_2_material_probe",
            "probe/readout apparatus treated as matter source",
            "legal_if_real_apparatus",
            "measurement device stress-energy is ordinary matter, not pure readout",
            "include apparatus in S_matter before variation or idealize as nonbackreacting after variation",
            "ordinary_matter_not_generator_zero",
        ),
        (
            "RCM967_3_nonlocal_observable_fit",
            "nonlocal observable map tuned to local branch",
            "interpretation_risk",
            "can hide a posthoc domain/projector choice in reporting rather than equations",
            "record provenance and forbid using readout maps as fitted physical selectors",
            "policy_guardrail",
        ),
        (
            "RCM967_4_hidden_marker_return",
            "material marker renamed as readout label",
            "live_without_no_marker_theorem",
            "if the marker enters S_parent before readout, domain separation does not remove it",
            "requires primitive no-natural-marker theorem or retained residual",
            "not_killed",
        ),
    ]
    rows = []
    for counter_id, countermodel, admissibility, damage, required_blocker, current_status in specs:
        rows.append(
            {
                "counter_id": counter_id,
                "countermodel": countermodel,
                "admissibility": admissibility,
                "damage": damage,
                "required_blocker": required_blocker,
                "current_status": current_status,
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def memory_positive_operator_lemma() -> list[dict[str, str]]:
    specs = [
        {
            "lemma_id": "MPO967_0_setup",
            "piece": "local scalar/memory variable",
            "statement": "Let X be a memory/class scalar on a selected compact local exterior D with parent equation L_X X = J_X.",
            "status": "lemma_setup",
            "missing_parent_input": "actual parent X variable, selected D, and equation owner",
            "result_if_supplied": "enables non-plateau local silence proof",
        },
        {
            "lemma_id": "MPO967_1_operator",
            "piece": "positive elliptic operator",
            "statement": "L_X=-nabla_i(A^{ij}nabla_j)+m_X^2 with A^{ij} positive and m_X^2>=0 in the local branch.",
            "status": "conditional_requirement",
            "missing_parent_input": "A^{ij}, m_X^2, sign, and local branch reduction",
            "result_if_supplied": "gives nonnegative bulk energy integral",
        },
        {
            "lemma_id": "MPO967_2_boundary",
            "piece": "boundary and zero-mode removal",
            "statement": "Dirichlet X=0, or zero flux plus zero mean/topological boundary data, removes constant and boundary hair.",
            "status": "conditional_requirement",
            "missing_parent_input": "boundary condition from parent selector/relative-current sector",
            "result_if_supplied": "prevents hidden constant/domain class from surviving",
        },
        {
            "lemma_id": "MPO967_3_zero_source",
            "piece": "source silence",
            "statement": "J_X=0 in the local ordinary exterior, including no matter vertex, no chi_D wall source, and no readout source.",
            "status": "conditional_requirement",
            "missing_parent_input": "matter blindness, Bianchi-safe chi_D, and readout schema theorem",
            "result_if_supplied": "removes the driving term for local scalar hair",
        },
        {
            "lemma_id": "MPO967_4_energy_identity",
            "piece": "zero theorem",
            "statement": "0=int_D X L_X X = int_D A^{ij}nabla_i X nabla_j X + m_X^2 X^2 plus nonnegative/zero boundary term.",
            "status": "RELATIVE_THEOREM_PROVEN_UNDER_PREMISES",
            "missing_parent_input": "premises MPO967_0..3",
            "result_if_supplied": "forces grad X=0 and, with mass/zero-mode removal, X=0",
        },
        {
            "lemma_id": "MPO967_5_constant_mode",
            "piece": "massless constant exception",
            "statement": "If m_X=0 and boundary/mean do not remove constants, X may be a constant; it is harmless only if universal and source-independent.",
            "status": "exception_recorded",
            "missing_parent_input": "constant-sector universality and source-independence",
            "result_if_supplied": "constant mode becomes calibration, otherwise retained residual",
        },
        {
            "lemma_id": "MPO967_6_verdict",
            "piece": "memory positive-operator local silence",
            "statement": "The non-plateau mathematical lemma closes relative to signed positivity/source/boundary premises.",
            "status": "RELATIVE_LEMMA_READY_PARENT_INPUTS_UNSIGNED",
            "missing_parent_input": "parent L_X, J_X=0, boundary data, D selector, and coupling map",
            "result_if_supplied": "would eliminate the memory/class scalar generator locally",
        },
    ]
    rows = []
    for spec in specs:
        rows.append({**spec, "claim_allowed": "false", "valid_for_claim": "false", "generated_utc": stamp()})
    return rows


def memory_amplitude_bound_law() -> list[dict[str, str]]:
    specs = [
        {
            "bound_id": "MB967_0_gap",
            "quantity": "lambda_gap",
            "law": "lambda_gap >= a_min*lambda_1(D)+m_min^2 after zero-mode removal",
            "use": "sets the denominator for any retained memory amplitude",
            "missing_inputs": "a_min; lambda_1(D); m_min^2; boundary class",
        },
        {
            "bound_id": "MB967_1_L2_amplitude",
            "quantity": "||X||_L2",
            "law": "||X||_L2 <= ||J_X||_L2/lambda_gap plus boundary_lift_norm",
            "use": "turns failed zero theorem into a finite residual estimate",
            "missing_inputs": "J_X norm; lambda_gap; boundary lift",
        },
        {
            "bound_id": "MB967_2_gradient",
            "quantity": "||grad X||_L2",
            "law": "a_min||grad X||_L2^2 + m_min^2||X||_L2^2 <= ||J_X||_L2||X||_L2 plus boundary terms",
            "use": "bounds clock/PPN/fifth-force gradients",
            "missing_inputs": "operator signs; source norm; boundary terms",
        },
        {
            "bound_id": "MB967_3_pointwise",
            "quantity": "||X||_infty",
            "law": "||X||_infty <= C_ell(D,A,m)(||J_X||_Lp + boundary_norm) for p above dimension/2",
            "use": "maps memory scalar into observable residual ceilings",
            "missing_inputs": "elliptic constant; p-norm source; domain regularity",
        },
        {
            "bound_id": "MB967_4_observable_projection",
            "quantity": "residual vector",
            "law": "Delta O_i <= K_i||X|| + K_i_grad||grad X|| with arena-specific couplings",
            "use": "connects failed memory silence to clock/Gdot/R10/PPN bound rows",
            "missing_inputs": "K_i; observable projection; source paths; units",
        },
        {
            "bound_id": "MB967_5_claim_policy",
            "quantity": "claim gate",
            "law": "no row valid_for_claim=true until lambda_gap, J_X, boundary data, and K_i are numeric and sourced",
            "use": "prevents symbolic amplitude law from becoming evidence",
            "missing_inputs": "all parent and arena projection values",
        },
    ]
    rows = []
    for spec in specs:
        rows.append({**spec, "claim_allowed": "false", "valid_for_claim": "false", "generated_utc": stamp()})
    return rows


def generator_transition_ledger() -> list[dict[str, str]]:
    specs = [
        (
            "GTR967_0_readout_projector",
            "post-readout projector",
            "not_eliminated",
            "conditional_schema_theorem_written",
            "parent action domain signature missing",
            "closure_policy_strengthened_not_theorem_zero",
        ),
        (
            "GTR967_1_memory_scalar",
            "memory/class scalar",
            "not_eliminated",
            "relative_positive_operator_lemma_ready",
            "parent operator/source/boundary inputs missing",
            "can now be attacked by signing premises or bounded with amplitude law",
        ),
        (
            "GTR967_2_finite_fibre",
            "finite-cell fibre spectrum",
            "not_eliminated",
            "helped_indirectly",
            "still needs matter blindness and unique h0 theorem",
            "readout lock would prevent active block returning through reduced action",
        ),
        (
            "GTR967_3_local_invariant_algebra",
            "I_loc(Q_MTS)",
            "not_eliminated",
            "one schema theorem and one relative lemma sharpened",
            "no generator fully removed in the parent corpus",
            "next checkpoint must sign a premise or demote explicit closure",
        ),
    ]
    rows = []
    for transition_id, generator, previous_status, new_status, blocker, consequence in specs:
        rows.append(
            {
                "transition_id": transition_id,
                "generator": generator,
                "previous_status": previous_status,
                "new_status": new_status,
                "blocker": blocker,
                "consequence": consequence,
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def claim_gates() -> list[dict[str, str]]:
    specs = [
        ("CGATE967_0_readout_removed", "readout projector generator removed", "parent action domain excludes readout and reduced EFT backreaction", "conditional schema only", False),
        ("CGATE967_1_memory_zero", "memory/class scalar theorem-zero", "positive parent operator, zero source, and zero/topological boundary data", "relative lemma ready but inputs unsigned", False),
        ("CGATE967_2_memory_bound", "memory residual bound claim", "numeric sourced lambda_gap, source, boundary, and observable couplings", "symbolic amplitude law only", False),
        ("CGATE967_3_R2FR_zero", "R2/fR scalar branch killed", "no local scalar mode and no integrated-out tower", "not parent-signed", False),
        ("CGATE967_4_local_invariant_algebra", "local invariant algebra triviality", "all generators eliminated or universalized", "not eliminated", False),
        ("CGATE967_5_local_GR", "local GR/Newton promotion", "same-frame EH/source plus no-marker plus residual closure", "not proven", False),
    ]
    rows = []
    for gate_id, claim, required, current, passed in specs:
        rows.append(
            {
                "gate_id": gate_id,
                "claim": claim,
                "required_condition": required,
                "current_evidence": current,
                "gate_pass": flag(passed),
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def decisions() -> list[dict[str, str]]:
    specs = [
        (
            "DEC967_0_readout",
            "readout theorem",
            "conditional_schema_theorem_clean_not_parent_signed",
            "mathematically, a readout map on solution space cannot source parent equations; projectors only return if varied through a reduced action or hidden marker",
            "make the parent action domain/exclusion clause explicit before giving theorem-zero credit",
        ),
        (
            "DEC967_1_memory",
            "memory positive-operator lemma",
            "relative_lemma_ready",
            "energy identity gives a real non-plateau silence route, with constant zero-mode caveat",
            "try to sign parent L_X positivity, J_X=0, and boundary/zero-mode premises",
        ),
        (
            "DEC967_2_empirical",
            "memory residual fallback",
            "bound_law_written_nonclaim",
            "if silence fails, the residual is no longer vague: it needs lambda_gap, source norm, boundary lift, and observable couplings",
            "do not run numeric claims until those inputs are sourced",
        ),
        (
            "DEC967_3_project",
            "local GR route",
            "closer_but_not_claimed",
            "we have a proper way to remove one generator and a proper way to bound another, but parent signatures are still missing",
            "next best target is parent-domain signature plus memory operator input audit",
        ),
    ]
    rows = []
    for decision_id, topic, result, reason, next_action in specs:
        rows.append(
            {
                "decision_id": decision_id,
                "topic": topic,
                "result": result,
                "reason": reason,
                "next_action": next_action,
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md",
            "objective": "try to sign the parent action domain clause that excludes readout variables, and audit whether the parent corpus contains a positive memory operator with zero source and boundary data",
            "include": "Conf_parent field list; S_parent arguments; no reduced EFT backreaction clause; L_X sign; J_X source map; boundary/zero-mode data; observable coupling placeholders",
            "exclude": "local-GR claim, invented numeric memory bounds, R2/fR curve claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    readout_rows: list[dict[str, str]],
    counter_rows: list[dict[str, str]],
    memory_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    transition_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_paths_ok = all(row["exists"] == "true" for row in sources)
    source_needles_ok = all(row["needle_found"] == "true" for row in sources)
    readout_verdict_ok = any(
        row["attempt_id"] == "RAV967_5_verdict"
        and row["status"] == "CONDITIONAL_SCHEMA_THEOREM_WRITTEN_NOT_PARENT_SIGNED"
        for row in readout_rows
    )
    countermodels_retained = len(counter_rows) >= 5 and all(row["claim_allowed"] == "false" for row in counter_rows)
    memory_relative_ready = any(
        row["lemma_id"] == "MPO967_6_verdict"
        and row["status"] == "RELATIVE_LEMMA_READY_PARENT_INPUTS_UNSIGNED"
        for row in memory_rows
    )
    energy_identity_recorded = any(
        row["lemma_id"] == "MPO967_4_energy_identity"
        and row["status"] == "RELATIVE_THEOREM_PROVEN_UNDER_PREMISES"
        for row in memory_rows
    )
    amplitude_nonclaim = len(bound_rows) >= 6 and all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in bound_rows)
    transitions_nonclaim = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in transition_rows)
    no_claim_gates = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in decision_rows)
    target_written = bool(target_rows) and target_rows[0]["valid_for_claim"] == "false"
    no_formalization_edits = formalization_changed_after_start() == 0
    rows = []
    checks = [
        ("V967_0_source_paths_exist", source_paths_ok, "all cited local source paths exist"),
        ("V967_1_source_needles_found", source_needles_ok, "all source needles found"),
        ("V967_2_readout_verdict_not_overclaimed", readout_verdict_ok, "readout theorem is conditional schema only, not parent-signed"),
        ("V967_3_countermodels_retained", countermodels_retained, "readout countermodels remain retained/nonclaim"),
        ("V967_4_memory_relative_lemma_ready", memory_relative_ready, "memory positive-operator lemma verdict recorded"),
        ("V967_5_energy_identity_recorded", energy_identity_recorded, "energy identity theorem under premises recorded"),
        ("V967_6_amplitude_bound_nonclaim", amplitude_nonclaim, "memory amplitude law rows remain nonclaim"),
        ("V967_7_transitions_nonclaim", transitions_nonclaim, "generator transition rows make no claims"),
        ("V967_8_claim_gates_false", no_claim_gates, "all claim gates remain false"),
        ("V967_9_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim"),
        ("V967_10_next_target_written", target_written, "968 next target selected"),
        ("V967_11_formalization_untouched", no_formalization_edits, "formalization-workbench modified-file count since script start is zero"),
    ]
    for check_id, result, detail in checks:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if result else "fail",
                "detail": detail,
                "generated_utc": stamp(),
            }
        )
    rows.append(
        {
            "check_id": "V967_12_validation_rows_ready",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "967 validation pack assembled",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    readout_rows: list[dict[str, str]],
    counter_rows: list[dict[str, str]],
    memory_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    transition_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 967 Y5 R10: Readout-After-Variation Parent Schema Theorem Or Memory Positive-Operator Lemma

Status: `Y5_R10_967_readout_schema_conditional_not_parent_signed_memory_positive_operator_relative_lemma_ready_nonclaim`

Claim ceiling: no readout projector theorem-zero, no memory scalar theorem-zero, no R2/fR zero, no R10 pass, no PPN pass, no EH/Newton/local-GR claim is made.

## Readout

The readout projector route is mathematically clean but still not fully parent-signed. If readout is strictly a map from the solution space to observables, `R_read: Sol(S_parent)->Obs`, then it cannot contribute to `delta S_parent` because it is not an action argument. Any projector that is varied through a reduced action is a new EFT branch and must pay the residual/variation tax.

That is a real schema theorem, but not yet a corpus-wide parent theorem: the parent action domain still has to explicitly exclude readout variables and forbid reduced-action backreaction from earning theorem-zero credit.

The useful new math gain is the memory positive-operator lemma. Under signed positivity, zero-source, and boundary/zero-mode premises, the energy identity forces the local memory scalar to vanish without smuggling in a plateau axiom. If those premises fail, the same setup gives a finite amplitude-bound law instead of hand-waving.

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Readout Schema Theorem Attempt

{md_table(readout_rows, ["attempt_id", "theorem_piece", "status", "proof_or_failure", "remaining_gap"])}

## Readout Countermodel Audit

{md_table(counter_rows, ["counter_id", "countermodel", "admissibility", "damage", "required_blocker", "current_status"])}

## Memory Positive-Operator Lemma

{md_table(memory_rows, ["lemma_id", "piece", "status", "statement", "missing_parent_input"])}

## Memory Amplitude Bound Law

{md_table(bound_rows, ["bound_id", "quantity", "law", "use", "missing_inputs"])}

## Generator Transition Ledger

{md_table(transition_rows, ["transition_id", "generator", "previous_status", "new_status", "blocker", "consequence"])}

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
    readout_rows = readout_schema_theorem_attempt()
    counter_rows = readout_countermodel_audit()
    memory_rows = memory_positive_operator_lemma()
    bound_rows = memory_amplitude_bound_law()
    transition_rows = generator_transition_ledger()
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        readout_rows,
        counter_rows,
        memory_rows,
        bound_rows,
        transition_rows,
        claim_rows,
        decision_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_967_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_967_READOUT_SCHEMA_THEOREM_ATTEMPT.csv",
        readout_rows,
        [
            "attempt_id",
            "theorem_piece",
            "claim_shape",
            "status",
            "proof_or_failure",
            "blocks",
            "remaining_gap",
            "claim_allowed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_967_READOUT_COUNTERMODEL_AUDIT.csv",
        counter_rows,
        ["counter_id", "countermodel", "admissibility", "damage", "required_blocker", "current_status", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
        memory_rows,
        ["lemma_id", "piece", "statement", "status", "missing_parent_input", "result_if_supplied", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_967_MEMORY_AMPLITUDE_BOUND_LAW.csv",
        bound_rows,
        ["bound_id", "quantity", "law", "use", "missing_inputs", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_967_GENERATOR_TRANSITION_LEDGER.csv",
        transition_rows,
        ["transition_id", "generator", "previous_status", "new_status", "blocker", "consequence", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_967_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_967_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_967_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_967_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, readout_rows, counter_rows, memory_rows, bound_rows, transition_rows, claim_rows, decision_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()

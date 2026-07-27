from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md"
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
            "source_id": "967_doc",
            "path": "967-Y5-R10-readout-after-variation-parent-schema-theorem-or-memory-positive-operator-lemma.md",
            "role": "handoff: parent-domain signature and memory operator inputs selected",
            "needle": "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md",
        },
        {
            "source_id": "967_readout_csv",
            "path": "source-intake/mts_residuals/P8_Y5_R10_967_READOUT_SCHEMA_THEOREM_ATTEMPT.csv",
            "role": "readout schema theorem attempt",
            "needle": "RAV967_5_verdict",
        },
        {
            "source_id": "967_memory_csv",
            "path": "source-intake/mts_residuals/P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
            "role": "memory positive-operator relative lemma",
            "needle": "MPO967_6_verdict",
        },
        {
            "source_id": "407_parent_sketch",
            "path": "407-primitive-relational-quotient-action-sketch.md",
            "role": "primitive relational quotient/readout parent-action sketch",
            "needle": "configuration_space_sketch_written",
        },
        {
            "source_id": "410_functor",
            "path": "410-quotient-matter-functor-theorem-attempt.md",
            "role": "quotient matter functor and reduced readout EFT counterexample",
            "needle": "reduced_readout_EFT",
        },
        {
            "source_id": "422_readout",
            "path": "422-matter-functor-blindness-readout-after-variation-theorem-attempt.md",
            "role": "readout-after-variation no-cheat contract and parent factorization gaps",
            "needle": "readout_after_variation_contract_written",
        },
        {
            "source_id": "423_minimality",
            "path": "423-parent-action-minimality-no-extension-theorem-attempt.md",
            "role": "Conf_parent/no-extension blocker and post-readout EFT route",
            "needle": "post_readout_reduced_action",
        },
        {
            "source_id": "417_boundary",
            "path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "role": "memory/boundary exchange and Bianchi gate blocker",
            "needle": "Bianchi_gate_owned",
        },
        {
            "source_id": "421_fibre",
            "path": "421-finite-fibre-spectrum-decoupling-theorem-attempt.md",
            "role": "finite scalar/fibre source and mass-gap blocker",
            "needle": "fifth_force_fibre_mode_excluded",
        },
        {
            "source_id": "963_scalar",
            "path": "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
            "role": "no-extra-scalar and finite scalar-mode parent-signature audit",
            "needle": "NES963_2_no_local_kinetic_scalar",
        },
        {
            "source_id": "955_matter_schema",
            "path": "955-Y5-R10-minimal-matter-action-source-coupling-lemma-or-species-weight-residual-runner.md",
            "role": "minimal matter schema/no source-only slots analogue",
            "needle": "MMA955_6_verdict",
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


def parent_domain_signature_audit() -> list[dict[str, str]]:
    specs = [
        {
            "audit_id": "PDS968_0_conf_parent_field_list",
            "signature_piece": "closed Conf_parent field list",
            "required_to_sign": "explicit typed parent configuration object with admitted variables and excluded readout/projector variables",
            "current_evidence": "407 has a configuration-space sketch; 423 says primitive universal property/no-extension is not derived",
            "status": "sketch_exists_not_closed_signature",
            "blocks": "readout exclusion cannot be corpus-wide theorem-zero",
            "next_action": "turn sketch into a parent-domain certificate or keep readout closure policy",
        },
        {
            "audit_id": "PDS968_1_S_parent_arguments",
            "signature_piece": "S_parent argument list",
            "required_to_sign": "S_parent[Phi] depends only on parent fields, matter fields, observed geometry construction, and universal constants",
            "current_evidence": "422 writes variation-order contract but marks parent factorization/formalization incomplete",
            "status": "contract_written_not_parent_signed",
            "blocks": "delta S/delta P_read absence remains conditional",
            "next_action": "write a field-by-field action-domain ledger",
        },
        {
            "audit_id": "PDS968_2_readout_exclusion",
            "signature_piece": "P_read/R_read/P_active excluded from S_parent",
            "required_to_sign": "readout maps are functions on Sol(S_parent) only and never action arguments",
            "current_evidence": "967 proves the schema theorem under this premise; 422 calls it conditional no-cheat rule",
            "status": "relative_schema_theorem_available_parent_signature_missing",
            "blocks": "post-readout projector generator not eliminated",
            "next_action": "promote as explicit parent-domain clause if no contradictory source exists",
        },
        {
            "audit_id": "PDS968_3_reduced_EFT_backreaction",
            "signature_piece": "no varied reduced-action backreaction",
            "required_to_sign": "any S_red made after readout is not allowed to earn parent theorem-zero credit",
            "current_evidence": "423 and 967 retain post-readout reduced actions as countermodels/new EFT branches",
            "status": "guardrail_pass_not_forbidden_theorem",
            "blocks": "reduced action can still exist as a retained branch",
            "next_action": "keep variation tax; do not claim absolute exclusion",
        },
        {
            "audit_id": "PDS968_4_material_probe",
            "signature_piece": "measurement/probe apparatus distinction",
            "required_to_sign": "real apparatus stress enters S_matter before variation; ideal readout is nonbackreacting after variation",
            "current_evidence": "967 identifies material probe as ordinary matter, not pure readout",
            "status": "classification_written_not_full_parent_clause",
            "blocks": "apparatus/source confusion can fake readout silence",
            "next_action": "include in parent-domain certificate",
        },
        {
            "audit_id": "PDS968_5_no_hidden_marker_return",
            "signature_piece": "no hidden marker renamed as readout",
            "required_to_sign": "readout labels cannot be material markers inside S_parent",
            "current_evidence": "423/965 keep material marker and invariant scalar countermodels live",
            "status": "not_signed",
            "blocks": "domain separation does not remove a marker that enters before readout",
            "next_action": "needs primitive no-natural-marker theorem or retained residual",
        },
        {
            "audit_id": "PDS968_6_verdict",
            "signature_piece": "parent domain signature",
            "required_to_sign": "PDS968_0 through PDS968_5 all pass",
            "current_evidence": "conditional readout theorem exists, but parent domain and no-hidden-marker signatures are missing",
            "status": "NOT_PARENT_SIGNED_CURRENT_CORPUS",
            "blocks": "readout projector generator remains conditional closure, not theorem-zero",
            "next_action": "build a source-backed parent-domain certificate or keep all readout rows nonclaim",
        },
    ]
    rows = []
    for spec in specs:
        rows.append({**spec, "claim_allowed": "false", "valid_for_claim": "false", "generated_utc": stamp()})
    return rows


def readout_exclusion_clause() -> list[dict[str, str]]:
    specs = [
        (
            "REC968_0_parent_domain_clause",
            "Domain clause",
            "Conf_parent excludes P_read, R_read, fitted masks, post-solution sections, and readout-selected active blocks.",
            "candidate_clause_ready",
            "would activate RAV967_1 if parent-signed",
        ),
        (
            "REC968_1_solution_space_readout",
            "Readout clause",
            "R_read is a map Sol(S_parent)->Obs and has no Euler-Lagrange equation of its own.",
            "candidate_clause_ready",
            "would prevent ideal readout from sourcing parent equations",
        ),
        (
            "REC968_2_reduced_action_tax",
            "Reduced-EFT clause",
            "If a readout-reduced functional is varied, it defines a retained EFT branch, not a parent theorem-zero proof.",
            "policy_guardrail_ready",
            "prevents closure-zero from being mislabelled as theorem-zero",
        ),
        (
            "REC968_3_apparatus_clause",
            "Apparatus clause",
            "Physical measuring devices are ordinary matter sources included before variation or idealized as nonbackreacting probes.",
            "candidate_clause_ready",
            "separates source matter from observational map",
        ),
        (
            "REC968_4_hidden_marker_clause",
            "Hidden-marker clause",
            "No material marker, boundary class, domain selector, or species label may be reintroduced by renaming it as readout data.",
            "blocked_by_no_marker_theorem",
            "requires primitive no-natural-marker theorem; not solved by readout alone",
        ),
        (
            "REC968_5_verdict",
            "Readout exclusion certificate",
            "The clause is precise enough to install, but not derived from a primitive universal property.",
            "CERTIFICATE_READY_AS_CONTRACT_NOT_DERIVATION",
            "safe for private spine discipline; not a local-GR claim",
        ),
    ]
    rows = []
    for clause_id, clause_type, clause_text, status, consequence in specs:
        rows.append(
            {
                "clause_id": clause_id,
                "clause_type": clause_type,
                "clause_text": clause_text,
                "status": status,
                "consequence": consequence,
                "parent_signed": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def memory_operator_input_audit() -> list[dict[str, str]]:
    specs = [
        ("MOI968_0_X_variable", "memory/class scalar X", "actual parent field or quotient scalar X with equation owner", "memory/class scalar named as blocker; no explicit parent X owner found", "MISSING_PARENT_OWNER"),
        ("MOI968_1_domain_D", "selected compact local exterior D", "parent-selected D with regular boundary and local branch conditions", "415/416 leave selector and candidate-domain circularity open", "MISSING_PARENT_SELECTED_DOMAIN"),
        ("MOI968_2_operator_L", "operator L_X", "explicit L_X=-nabla_i(A^ij nabla_j)+m_X^2 from parent variation", "967 gives lemma form only; no parent operator extracted", "MISSING_OPERATOR_FORM"),
        ("MOI968_3_positivity", "A^ij positivity", "A^ij positive definite or semidefinite with controlled kernel", "no source-backed A^ij or sign certificate found", "MISSING_SIGN_CERTIFICATE"),
        ("MOI968_4_mass_gap", "m_X^2 and lambda_gap", "m_X^2>=0 plus zero-mode removal or positive first eigenvalue", "no numeric/symbolic parent m_X^2 or lambda_1(D) source", "MISSING_GAP_INPUTS"),
        ("MOI968_5_zero_source", "J_X=0", "no matter vertex, no chi_D wall source, no readout source, no boundary exchange source", "matter blindness, Bianchi-safe chi_D, and boundary no-hair remain unsigned", "MISSING_ZERO_SOURCE_THEOREM"),
        ("MOI968_6_boundary_data", "boundary/zero-mode data", "Dirichlet, topological zero, zero flux plus zero mean, or universal constant mode", "boundary exchange/no-hair and relative class selection are not parent-derived", "MISSING_BOUNDARY_DATA"),
        ("MOI968_7_observable_couplings", "K_i observable couplings", "clock/Gdot/R10/PPN projection couplings from X and grad X to residual vector", "967 bound law is symbolic only; no sourced K_i rows", "MISSING_ARENA_PROJECTIONS"),
        ("MOI968_8_verdict", "memory zero activation", "all inputs MOI968_0..7 supplied", "positive-operator lemma remains relative; activation inputs absent", "INPUTS_MISSING_NO_THEOREM_ZERO"),
    ]
    rows = []
    for input_id, input_name, required, evidence, status in specs:
        rows.append(
            {
                "input_id": input_id,
                "input_name": input_name,
                "required_for_967_lemma": required,
                "current_evidence": evidence,
                "status": status,
                "ready_for_theorem_zero": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def memory_zero_premise_gate() -> list[dict[str, str]]:
    specs = [
        ("MZG968_0_parent_X", "parent X owner exists", False, "MISSING_PARENT_OWNER"),
        ("MZG968_1_selected_D", "local domain D selected by parent", False, "MISSING_PARENT_SELECTED_DOMAIN"),
        ("MZG968_2_positive_L", "positive operator L_X signed", False, "MISSING_OPERATOR_FORM_AND_SIGN"),
        ("MZG968_3_zero_source", "J_X=0 signed", False, "MISSING_ZERO_SOURCE_THEOREM"),
        ("MZG968_4_boundary_zero", "boundary/zero-mode data remove hair", False, "MISSING_BOUNDARY_DATA"),
        ("MZG968_5_constant_universal", "constant mode universal if present", False, "MISSING_CONSTANT_SECTOR_UNIVERSALITY"),
        ("MZG968_6_observable_map", "observable projection couplings sourced", False, "MISSING_ARENA_PROJECTIONS"),
        ("MZG968_7_verdict", "memory positive-operator zero theorem activates", False, "PREMISES_NOT_SIGNED"),
    ]
    rows = []
    for gate_id, premise, gate_pass, reason in specs:
        rows.append(
            {
                "gate_id": gate_id,
                "premise": premise,
                "gate_pass": flag(gate_pass),
                "reason": reason,
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def residual_input_template() -> list[dict[str, str]]:
    specs = [
        ("MRI968_0_lambda_gap", "lambda_gap", "1/length^2", "MISSING_A_MIN;MISSING_LAMBDA1_D;MISSING_MX2", "sets amplitude denominator"),
        ("MRI968_1_source_norm", "||J_X||", "operator_source_units", "MISSING_JX_SOURCE_MAP", "drives nonzero memory amplitude"),
        ("MRI968_2_boundary_lift", "boundary_lift_norm", "same_as_X", "MISSING_BOUNDARY_DATA", "captures boundary hair if zero theorem fails"),
        ("MRI968_3_clock_coupling", "K_clock", "observable_per_X", "MISSING_CLOCK_PROJECTION", "maps X to clock/redshift residual"),
        ("MRI968_4_Gdot_coupling", "K_Gdot", "per_time_per_X", "MISSING_GDOT_PROJECTION", "maps X to time-varying effective G"),
        ("MRI968_5_R10_coupling", "K_R10", "alpha_per_X", "MISSING_R10_PROJECTION", "maps X to fifth-force alpha(lambda) branch"),
        ("MRI968_6_PPN_coupling", "K_PPN", "PPN_per_X", "MISSING_PPN_PROJECTION", "maps X/grad X to gamma/beta/preferred-frame residuals"),
        ("MRI968_7_units_sources", "source_paths", "paths", "MISSING_SOURCE_PATHS", "required before any row becomes valid_for_claim"),
    ]
    rows = []
    for row_id, quantity, units, placeholder, role in specs:
        rows.append(
            {
                "row_id": row_id,
                "quantity": quantity,
                "units": units,
                "current_value": placeholder,
                "role": role,
                "ready_for_runner": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def claim_gates() -> list[dict[str, str]]:
    specs = [
        ("CGATE968_0_parent_domain_signature", "parent domain excludes readout variables", "closed Conf_parent/S_parent argument certificate", "not parent-signed"),
        ("CGATE968_1_readout_generator_removed", "readout projector removed from I_loc", "CGATE968_0 plus no hidden marker return", "not proven"),
        ("CGATE968_2_memory_zero", "memory/class scalar theorem-zero", "positive L_X, J_X=0, boundary/zero-mode data", "inputs missing"),
        ("CGATE968_3_memory_bound", "memory residual can be numerically bounded", "lambda_gap, J_X, boundary lift, K_i, source paths", "placeholders only"),
        ("CGATE968_4_local_invariant_algebra", "local invariant algebra triviality", "readout and memory plus remaining generators eliminated", "not proven"),
        ("CGATE968_5_local_GR", "local GR/Newton/PPN promotion", "same-frame EH/source, no-marker, and local residual closure", "not proven"),
    ]
    rows = []
    for gate_id, claim, required, current in specs:
        rows.append(
            {
                "gate_id": gate_id,
                "claim": claim,
                "required_condition": required,
                "current_evidence": current,
                "gate_pass": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def decisions() -> list[dict[str, str]]:
    specs = [
        (
            "DEC968_0_parent_domain",
            "readout exclusion signature",
            "not_parent_signed",
            "the exact clause is now written, but current sources show a sketch/contract rather than a closed parent configuration theorem",
            "make a parent-domain certificate if the project chooses explicit closure; otherwise keep deriving primitive minimality",
        ),
        (
            "DEC968_1_memory_operator",
            "positive-operator lemma activation",
            "inputs_missing",
            "the energy identity is mathematically useful but no parent L_X, J_X=0, domain, boundary, or arena projection inputs are sourced",
            "hunt for a parent memory operator owner or demote memory to residual template",
        ),
        (
            "DEC968_2_residual_template",
            "memory finite residual",
            "template_ready_nonclaim",
            "if zero theorem fails, the residual inputs are now concrete rather than vibes",
            "fill only with numeric/source-backed rows before any empirical comparison",
        ),
        (
            "DEC968_3_next_hinge",
            "best next target",
            "operator_owner_hunt",
            "signing readout as a closure clause is easier, but deriving local GR needs the memory/source/domain owner next",
            "try to derive the parent memory operator from existing action sketches or explicitly mark it as retained residual",
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
            "next_target": "969-Y5-R10-parent-memory-operator-owner-hunt-or-readout-domain-certificate.md",
            "objective": "hunt for an actual parent owner of the memory operator L_X and source J_X; if no owner exists, write a readout-domain certificate as explicit closure and keep memory as retained residual input",
            "include": "parent action sketches, memory/class scalar equations, boundary/current sector, Bianchi ownership, L_X positivity, J_X zero-source, residual template",
            "exclude": "local-GR claim, invented memory coefficients, numeric bound claims, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    parent_rows: list[dict[str, str]],
    readout_rows: list[dict[str, str]],
    memory_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_paths_ok = all(row["exists"] == "true" for row in sources)
    source_needles_ok = all(row["needle_found"] == "true" for row in sources)
    parent_not_signed = any(
        row["audit_id"] == "PDS968_6_verdict" and row["status"] == "NOT_PARENT_SIGNED_CURRENT_CORPUS"
        for row in parent_rows
    )
    readout_clause_ready_nonclaim = any(
        row["clause_id"] == "REC968_5_verdict"
        and row["status"] == "CERTIFICATE_READY_AS_CONTRACT_NOT_DERIVATION"
        and row["parent_signed"] == "false"
        for row in readout_rows
    )
    memory_inputs_missing = sum(1 for row in memory_rows if row["status"].startswith("MISSING") or row["status"].endswith("MISSING_NO_THEOREM_ZERO"))
    zero_gates_false = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in zero_rows)
    residual_placeholders_blocked = all(
        row["ready_for_runner"] == "false" and row["valid_for_claim"] == "false" and "MISSING" in row["current_value"]
        for row in residual_rows
    )
    no_claim_gates = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in decision_rows)
    target_written = bool(target_rows) and target_rows[0]["valid_for_claim"] == "false"
    no_formalization_edits = formalization_changed_after_start() == 0
    rows = []
    checks = [
        ("V968_0_source_paths_exist", source_paths_ok, "all cited local source paths exist"),
        ("V968_1_source_needles_found", source_needles_ok, "all source needles found"),
        ("V968_2_parent_domain_not_signed", parent_not_signed, "parent domain signature remains unsigned"),
        ("V968_3_readout_clause_nonclaim_ready", readout_clause_ready_nonclaim, "readout exclusion certificate ready only as contract"),
        ("V968_4_memory_inputs_missing", memory_inputs_missing >= 7, f"{memory_inputs_missing} memory activation inputs remain missing"),
        ("V968_5_memory_zero_gates_false", zero_gates_false, "all memory zero premise gates remain false"),
        ("V968_6_residual_placeholders_blocked", residual_placeholders_blocked, "all memory residual template rows are blocked placeholders"),
        ("V968_7_claim_gates_false", no_claim_gates, "all claim gates remain false"),
        ("V968_8_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim"),
        ("V968_9_next_target_written", target_written, "969 next target selected"),
        ("V968_10_formalization_untouched", no_formalization_edits, "formalization-workbench modified-file count since script start is zero"),
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
            "check_id": "V968_11_validation_rows_ready",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "968 validation pack assembled",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    parent_rows: list[dict[str, str]],
    readout_rows: list[dict[str, str]],
    memory_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 968 Y5 R10: Parent Domain Signature And Memory Operator Input Audit

Status: `Y5_R10_968_parent_domain_signature_not_signed_readout_certificate_contract_ready_memory_operator_inputs_missing_nonclaim`

Claim ceiling: no readout projector theorem-zero, no memory scalar theorem-zero, no memory residual bound claim, no R2/fR zero, no R10 pass, no EH/Newton/local-GR claim is made.

## Readout

This checkpoint tried to turn the clean 967 readout theorem into an actual parent signature. It does not close as a derivation. The exact readout-exclusion clause is now written and usable as a private discipline contract, but the current corpus still has a parent-action sketch and no-extension guardrails rather than a closed `Conf_parent`/`S_parent` field-domain certificate.

The memory route is sharper too, but still unsigned. The positive-operator lemma is ready relative to premises, yet the actual activation inputs are missing: parent `X`, selected local domain `D`, operator `L_X`, positivity/gap data, `J_X=0`, boundary/zero-mode data, and observable couplings.

So we have not won local GR here. But the next gap is concrete: either find the parent memory operator owner, or honestly keep memory as a retained residual with the input template below. No fog, no vibes, no gremlins.

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Parent Domain Signature Audit

{md_table(parent_rows, ["audit_id", "signature_piece", "status", "blocks", "next_action"])}

## Readout Exclusion Clause

{md_table(readout_rows, ["clause_id", "clause_type", "status", "clause_text", "parent_signed"])}

## Memory Operator Input Audit

{md_table(memory_rows, ["input_id", "input_name", "status", "required_for_967_lemma", "current_evidence"])}

## Memory Zero Premise Gate

{md_table(zero_rows, ["gate_id", "premise", "gate_pass", "reason"])}

## Memory Residual Input Template

{md_table(residual_rows, ["row_id", "quantity", "units", "current_value", "role"])}

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
    parent_rows = parent_domain_signature_audit()
    readout_rows = readout_exclusion_clause()
    memory_rows = memory_operator_input_audit()
    zero_rows = memory_zero_premise_gate()
    residual_rows = residual_input_template()
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        parent_rows,
        readout_rows,
        memory_rows,
        zero_rows,
        residual_rows,
        claim_rows,
        decision_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_968_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_968_PARENT_DOMAIN_SIGNATURE_AUDIT.csv",
        parent_rows,
        ["audit_id", "signature_piece", "required_to_sign", "current_evidence", "status", "blocks", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_968_READOUT_EXCLUSION_CLAUSE.csv",
        readout_rows,
        ["clause_id", "clause_type", "clause_text", "status", "consequence", "parent_signed", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
        memory_rows,
        ["input_id", "input_name", "required_for_967_lemma", "current_evidence", "status", "ready_for_theorem_zero", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_968_MEMORY_ZERO_PREMISE_GATE.csv",
        zero_rows,
        ["gate_id", "premise", "gate_pass", "reason", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_968_RESIDUAL_INPUT_TEMPLATE.csv",
        residual_rows,
        ["row_id", "quantity", "units", "current_value", "role", "ready_for_runner", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_968_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_968_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_968_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_968_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, parent_rows, readout_rows, memory_rows, zero_rows, residual_rows, claim_rows, decision_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()

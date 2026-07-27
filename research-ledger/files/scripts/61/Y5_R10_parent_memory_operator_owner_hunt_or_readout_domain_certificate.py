from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "969-Y5-R10-parent-memory-operator-owner-hunt-or-readout-domain-certificate.md"
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
            "source_id": "968_doc",
            "path": "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md",
            "role": "handoff: memory operator owner hunt and readout certificate",
            "needle": "969-Y5-R10-parent-memory-operator-owner-hunt-or-readout-domain-certificate.md",
        },
        {
            "source_id": "968_memory_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
            "role": "missing memory operator input audit",
            "needle": "MOI968_8_verdict",
        },
        {
            "source_id": "968_readout_clause",
            "path": "source-intake/mts_residuals/P8_Y5_R10_968_READOUT_EXCLUSION_CLAUSE.csv",
            "role": "readout-domain certificate clauses",
            "needle": "REC968_5_verdict",
        },
        {
            "source_id": "967_memory_lemma",
            "path": "source-intake/mts_residuals/P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
            "role": "relative positive-operator memory lemma",
            "needle": "MPO967_6_verdict",
        },
        {
            "source_id": "557_positive_operator",
            "path": "source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_POSITIVE_OPERATOR_ATTEMPT.csv",
            "role": "earlier positive operator attempt for bulk/memory/range sectors",
            "needle": "positive massive elliptic operator",
        },
        {
            "source_id": "557_force_law",
            "path": "source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_FORCE_LAW_MAP.csv",
            "role": "finite memory/range fallback force-law map",
            "needle": "memory_history_kernel",
        },
        {
            "source_id": "476_double_zero",
            "path": "source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv",
            "role": "double-zero memory gate origin attempt",
            "needle": "O6_verdict",
        },
        {
            "source_id": "417_boundary",
            "path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "role": "boundary exchange and Bianchi ownership blockers",
            "needle": "Bianchi_gate_owned",
        },
        {
            "source_id": "421_fibre",
            "path": "421-finite-fibre-spectrum-decoupling-theorem-attempt.md",
            "role": "finite-fibre scalar and mass-gap owner attempt",
            "needle": "universal_stationary_spectrum_derived",
        },
        {
            "source_id": "856_projection",
            "path": "source-intake/mts_residuals/P8_Y5_R10_856_MEMORY_PROJECTION_REPAIR_CONTRACT.csv",
            "role": "cosmology memory projection source/conservation guard",
            "needle": "RPC856_1_response_source",
        },
        {
            "source_id": "963_scalar_owner",
            "path": "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
            "role": "R2/fR scalar owner audit",
            "needle": "CO963_4_verdict",
        },
        {
            "source_id": "407_parent_sketch",
            "path": "407-primitive-relational-quotient-action-sketch.md",
            "role": "primitive quotient/readout action sketch",
            "needle": "S_readout_observables",
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


def memory_operator_owner_hunt() -> list[dict[str, str]]:
    specs = [
        {
            "owner_id": "MOO969_0_557_positive_bulk_operator",
            "candidate_owner": "bulk/memory/range positive massive elliptic operator",
            "evidence": "557 has the form (-Delta_A+m_X^2)X=0 and the energy integral, but marks source charge and memory locality not derived",
            "owner_status": "FORM_AVAILABLE_OWNER_NOT_DERIVED",
            "missing_to_activate": "parent X owner; rho_X=0; Q_X[source]=0; memory locality; boundary flux zero",
            "claim_effect_if_closed": "would activate MPO967 for a bulk/range-like local scalar",
        },
        {
            "owner_id": "MOO969_1_476_double_zero_gate",
            "candidate_owner": "double-zero chi_D memory gate",
            "evidence": "476 shows f(0)=0 and f_prime(0)=0 is sufficient; quadratic/determinant routes exist as contracts",
            "owner_status": "COUPLING_GATE_CONTRACT_NOT_OPERATOR_OWNER",
            "missing_to_activate": "parent-derived f(chi_D), parent L_mem, finite L_mem, Bianchi-safe chi_D",
            "claim_effect_if_closed": "would silence chi_D-local memory stress at the local zero branch",
        },
        {
            "owner_id": "MOO969_2_417_boundary_current",
            "candidate_owner": "boundary/current no-hair sector",
            "evidence": "417 has bulk_memory_current conditional support and Ward-owner route, but Bianchi and boundary exchange fail",
            "owner_status": "BOUNDARY_OWNER_NOT_DERIVED",
            "missing_to_activate": "exact/zero b_2; physical local representative; Bianchi cancellation; secular drift zero",
            "claim_effect_if_closed": "would supply boundary/zero-mode data and help J_X=0",
        },
        {
            "owner_id": "MOO969_3_421_finite_fibre",
            "candidate_owner": "finite-fibre unique gapped stationary solution",
            "evidence": "421 says unique h0/mass gap/source independence would work, but universal stationary spectrum and decoupling fail",
            "owner_status": "MASS_GAP_OWNER_NOT_DERIVED",
            "missing_to_activate": "parent fibre potential; Hessian sign; source-independent h0; matter blindness",
            "claim_effect_if_closed": "would convert finite-fibre scalar into universal constants",
        },
        {
            "owner_id": "MOO969_4_856_cosmology_projection",
            "candidate_owner": "memory response projection branch",
            "evidence": "856 requires b_response to be independently sourced or zero and conservation to be signed",
            "owner_status": "LIKELIHOOD_PROJECTION_NOT_PARENT_OPERATOR",
            "missing_to_activate": "independent q_B source; physical conservation accounting; local operator map",
            "claim_effect_if_closed": "could become a sourced cosmology response, not local theorem-zero by itself",
        },
        {
            "owner_id": "MOO969_5_963_scalar_mode",
            "candidate_owner": "R2/fR or no-extra-scalar owner",
            "evidence": "963 records no executable owner for finite scalar branch and no parent no-extra-scalar signature",
            "owner_status": "NO_EXECUTABLE_OWNER_FOUND",
            "missing_to_activate": "coefficient, scalar mass, coupling, screening, or absolute zero theorem",
            "claim_effect_if_closed": "would decide whether memory scalar becomes R10/PPN residual or theorem-zero",
        },
        {
            "owner_id": "MOO969_6_407_parent_sketch",
            "candidate_owner": "primitive relational quotient/readout parent action sketch",
            "evidence": "407 sketches configuration/readout discipline but says hard proofs are still needed",
            "owner_status": "PARENT_SKETCH_NOT_OPERATOR_EQUATION",
            "missing_to_activate": "actual memory Euler-Lagrange equation and source/boundary terms",
            "claim_effect_if_closed": "could provide the owner if upgraded to full variational principle",
        },
        {
            "owner_id": "MOO969_7_verdict",
            "candidate_owner": "current corpus parent memory operator owner",
            "evidence": "all candidates are forms, contracts, projections, or failed owner audits rather than a signed parent L_X/J_X",
            "owner_status": "NO_PARENT_MEMORY_OPERATOR_OWNER_FOUND_CURRENT_CORPUS",
            "missing_to_activate": "single source-backed parent equation L_X X=J_X with positivity, zero source, boundary data, and observable projections",
            "claim_effect_if_closed": "memory positive-operator theorem remains relative; memory stays retained residual",
        },
    ]
    rows = []
    for spec in specs:
        rows.append({**spec, "claim_allowed": "false", "valid_for_claim": "false", "generated_utc": stamp()})
    return rows


def owner_acceptance_gate() -> list[dict[str, str]]:
    specs = [
        ("MOG969_0_X_owner", "parent field/quotient scalar X is named and varied", False, "no source-backed parent X owner found"),
        ("MOG969_1_equation", "Euler-Lagrange equation has form L_X X=J_X", False, "operator form exists only as conditional template"),
        ("MOG969_2_positive_operator", "L_X has positive A^ij and nonnegative mass/gap", False, "no sign/Hessian/gap certificate"),
        ("MOG969_3_zero_source", "J_X=0 in local ordinary exterior", False, "source charge, chi_D wall, and boundary exchange not killed"),
        ("MOG969_4_boundary", "boundary/zero-mode conditions remove hair", False, "boundary no-hair and local domain selector remain open"),
        ("MOG969_5_observable_map", "X and grad X project to clock/Gdot/R10/PPN with units", False, "projection couplings remain placeholders"),
        ("MOG969_6_no_R2FR_leak", "integrating out X cannot regenerate R2/fR/non-EH operator", False, "no integrated-out tower certificate absent"),
        ("MOG969_7_verdict", "memory operator owner accepted", False, "NO_OWNER_ACCEPTED"),
    ]
    rows = []
    for gate_id, requirement, gate_pass, reason in specs:
        rows.append(
            {
                "gate_id": gate_id,
                "requirement": requirement,
                "gate_pass": flag(gate_pass),
                "reason": reason,
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def readout_domain_certificate() -> list[dict[str, str]]:
    specs = [
        (
            "RDC969_0_domain",
            "Conf_parent excludes readout maps, fitted masks, post-solution sections, and readout-selected active blocks.",
            "CERTIFIED_AS_EXPLICIT_CLOSURE_CONTRACT",
            "not a primitive derivation; it is a no-cheat parent-domain rule for private work",
        ),
        (
            "RDC969_1_solution_map",
            "R_read: Sol(S_parent)->Obs has no Euler-Lagrange equation and is evaluated only after solving parent equations.",
            "CERTIFIED_AS_EXPLICIT_CLOSURE_CONTRACT",
            "activates the readout no-variation rule inside closure-labelled branches",
        ),
        (
            "RDC969_2_reduced_EFT_tax",
            "Any varied readout-reduced action is a new retained EFT branch and cannot supply theorem-zero credit.",
            "CERTIFIED_AS_GUARDRAIL",
            "prevents closure-zero being smuggled into theorem-zero",
        ),
        (
            "RDC969_3_apparatus",
            "Physical measuring apparatus is either ordinary matter included before variation or an ideal nonbackreacting probe after variation.",
            "CERTIFIED_AS_CLASSIFICATION_RULE",
            "keeps measurement stress separate from pure readout",
        ),
        (
            "RDC969_4_hidden_marker_exception",
            "This certificate does not kill material markers or invariant scalars that enter S_parent before readout.",
            "EXPLICIT_EXCEPTION",
            "still needs primitive no-natural-marker theorem or retained residual",
        ),
        (
            "RDC969_5_verdict",
            "Readout-domain certificate is installed as closure discipline, not as local-GR theorem-zero.",
            "CERTIFIED_CLOSURE_NOT_DERIVATION",
            "readout projector can be policy-closed but not counted as a derived local-GR proof",
        ),
    ]
    rows = []
    for cert_id, certificate_clause, status, limitation in specs:
        rows.append(
            {
                "cert_id": cert_id,
                "certificate_clause": certificate_clause,
                "status": status,
                "limitation": limitation,
                "parent_signed": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def retained_memory_residual_status() -> list[dict[str, str]]:
    specs = [
        (
            "RMR969_0_zero_route",
            "memory theorem-zero",
            "blocked",
            "no accepted parent L_X/J_X owner",
            "remain false until owner gate passes",
        ),
        (
            "RMR969_1_finite_route",
            "memory finite residual",
            "template_ready_inputs_missing",
            "968 template names lambda_gap, J_X, boundary lift, and K_i couplings but no values",
            "fill source-backed rows or keep unscored",
        ),
        (
            "RMR969_2_R10_route",
            "fifth-force/Yukawa memory branch",
            "possible_only_if_finite_scalar_owner_exists",
            "557 force-law map exists but operator/charges are not parent-derived",
            "do not digitize/score until alpha/lambda prediction exists",
        ),
        (
            "RMR969_3_clock_Gdot_route",
            "clock/Gdot memory branch",
            "possible_only_if_projection_couplings_exist",
            "boundary/memory drift locks exist, but K_clock and K_Gdot are missing",
            "future residual runner must require units/source paths",
        ),
        (
            "RMR969_4_cosmology_route",
            "cosmology memory response",
            "separate_likelihood_projection_unless_parent_conserved",
            "856 requires independent source or zero plus conservation guard",
            "do not use cosmology projection as local operator proof",
        ),
        (
            "RMR969_5_verdict",
            "memory status after owner hunt",
            "RETAINED_RESIDUAL_UNSCored",
            "operator owner absent and finite residual inputs missing",
            "next work should attempt construction of minimal quadratic memory action or keep residual ledger",
        ),
    ]
    rows = []
    for row_id, branch, status, reason, next_action in specs:
        rows.append(
            {
                "row_id": row_id,
                "branch": branch,
                "status": status,
                "reason": reason,
                "next_action": next_action,
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def minimal_action_construction_targets() -> list[dict[str, str]]:
    specs = [
        {
            "target_id": "MACT969_0_quadratic_action",
            "construction_target": "S_X=1/2 int_D sqrt(g)(A^ij grad_i X grad_j X + m_X^2 X^2) plus allowed boundary terms",
            "why_next": "this is the minimal structure that would supply L_X and positivity",
            "must_prove": "X is a parent variable or auxiliary; A^ij positive; m_X^2>=0; no hidden source terms",
        },
        {
            "target_id": "MACT969_1_source_silence",
            "construction_target": "J_X=0 from matter blindness, readout certificate, Bianchi-safe chi_D, and boundary no-hair",
            "why_next": "zero source is the biggest missing premise after operator form",
            "must_prove": "no matter vertex; no chi_D wall; no boundary exchange; no post-readout source",
        },
        {
            "target_id": "MACT969_2_boundary",
            "construction_target": "Dirichlet/topological/zero-flux plus zero-mean boundary package",
            "why_next": "constant and boundary hair survive without this",
            "must_prove": "parent-selected D and relative-current no-hair",
        },
        {
            "target_id": "MACT969_3_no_integrated_out_tower",
            "construction_target": "integrating out X does not regenerate R2/fR/non-EH operators",
            "why_next": "otherwise a solved memory field reappears as R11/R10 scalar leakage",
            "must_prove": "local field redefinition/topological silence or retained operator row",
        },
        {
            "target_id": "MACT969_4_residual_runner",
            "construction_target": "strict memory residual runner schema",
            "why_next": "if construction fails, memory must be testable rather than vague",
            "must_prove": "numeric sourced lambda_gap, J_X, boundary lift, K_i, units, and bound links",
        },
    ]
    rows = []
    for spec in specs:
        rows.append({**spec, "claim_allowed": "false", "valid_for_claim": "false", "generated_utc": stamp()})
    return rows


def claim_gates() -> list[dict[str, str]]:
    specs = [
        ("CGATE969_0_memory_owner", "parent memory operator owner found", "accepted L_X/J_X owner with sign/source/boundary evidence", "no owner accepted"),
        ("CGATE969_1_memory_zero", "memory positive-operator theorem-zero", "all owner gates pass plus zero source and boundary", "blocked"),
        ("CGATE969_2_memory_residual_score", "memory residual can be scored", "numeric sourced residual inputs and arena bounds", "inputs missing"),
        ("CGATE969_3_readout_theorem", "readout projector derived theorem-zero", "primitive parent domain theorem", "closure certificate only"),
        ("CGATE969_4_local_invariant_algebra", "local invariant algebra triviality", "readout plus memory plus remaining generators closed", "not proven"),
        ("CGATE969_5_local_GR", "local GR/Newton promotion", "same-frame EH/source and no-marker/residual closure", "not proven"),
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
            "DEC969_0_owner_hunt",
            "parent memory operator owner",
            "not_found",
            "all available candidates are conditional forms, contracts, projection rules, or failed owner audits",
            "attempt a minimal quadratic parent memory action construction if derivation-first continues",
        ),
        (
            "DEC969_1_readout",
            "readout domain",
            "closure_certificate_installed",
            "readout can now be used as explicit closure discipline but not as derived local-GR evidence",
            "keep readout rows nonclaim unless primitive parent domain theorem is derived",
        ),
        (
            "DEC969_2_memory_status",
            "memory/class scalar",
            "retained_residual_unscored",
            "positive-operator theorem is relative and finite residual inputs are missing",
            "either construct parent action owner or build strict memory residual runner",
        ),
        (
            "DEC969_3_best_next",
            "next derivation route",
            "minimal_quadratic_memory_action",
            "this is the only route that could supply L_X, positivity, and source/boundary gates in one place",
            "try construction; if it fails, demote to residual runner with no theorem-zero credit",
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
            "next_target": "970-Y5-R10-minimal-quadratic-memory-action-construction-or-strict-residual-runner.md",
            "objective": "try to construct a minimal parent quadratic memory action that supplies L_X, positivity, zero-source, boundary, and no-integrated-out-tower gates; if it fails, create a strict retained memory residual runner schema",
            "include": "quadratic action, Euler-Lagrange operator, source map J_X, chi_D boundary source, Bianchi ownership, zero-mode handling, residual runner fields",
            "exclude": "local-GR claim, invented numeric coefficients, memory bound claim, R2/fR curve claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    readout_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    construction_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_paths_ok = all(row["exists"] == "true" for row in sources)
    source_needles_ok = all(row["needle_found"] == "true" for row in sources)
    verdict_no_owner = any(
        row["owner_id"] == "MOO969_7_verdict"
        and row["owner_status"] == "NO_PARENT_MEMORY_OPERATOR_OWNER_FOUND_CURRENT_CORPUS"
        for row in owner_rows
    )
    all_owner_gates_false = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in gate_rows)
    readout_certified_closure = any(
        row["cert_id"] == "RDC969_5_verdict"
        and row["status"] == "CERTIFIED_CLOSURE_NOT_DERIVATION"
        for row in readout_rows
    )
    residual_retained = any(
        row["row_id"] == "RMR969_5_verdict"
        and row["status"] == "RETAINED_RESIDUAL_UNSCored"
        for row in residual_rows
    )
    construction_targets_ready = len(construction_rows) >= 5 and all(row["claim_allowed"] == "false" for row in construction_rows)
    no_claim_gates = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in decision_rows)
    target_written = bool(target_rows) and target_rows[0]["valid_for_claim"] == "false"
    no_formalization_edits = formalization_changed_after_start() == 0
    rows = []
    checks = [
        ("V969_0_source_paths_exist", source_paths_ok, "all cited local source paths exist"),
        ("V969_1_source_needles_found", source_needles_ok, "all source needles found"),
        ("V969_2_no_memory_owner_found", verdict_no_owner, "memory owner hunt ended with no accepted parent owner"),
        ("V969_3_owner_gates_false", all_owner_gates_false, "all memory owner acceptance gates remain false"),
        ("V969_4_readout_closure_certified", readout_certified_closure, "readout domain certificate installed as closure not derivation"),
        ("V969_5_memory_retained_residual", residual_retained, "memory status demoted to unscored retained residual"),
        ("V969_6_construction_targets_ready", construction_targets_ready, "minimal action construction targets written"),
        ("V969_7_claim_gates_false", no_claim_gates, "all claim gates remain false"),
        ("V969_8_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim"),
        ("V969_9_next_target_written", target_written, "970 next target selected"),
        ("V969_10_formalization_untouched", no_formalization_edits, "formalization-workbench modified-file count since script start is zero"),
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
            "check_id": "V969_11_validation_rows_ready",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "969 validation pack assembled",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    readout_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    construction_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 969 Y5 R10: Parent Memory Operator Owner Hunt Or Readout Domain Certificate

Status: `Y5_R10_969_no_parent_memory_operator_owner_found_readout_domain_certified_as_closure_memory_retained_residual_nonclaim`

Claim ceiling: no memory theorem-zero, no memory residual bound pass, no readout theorem-zero, no R2/fR zero, no R10 pass, no EH/Newton/local-GR claim is made.

## Readout

This checkpoint did the owner hunt properly. The corpus contains useful fragments: a positive-operator form, a double-zero memory coupling gate, boundary/current no-hair contracts, finite-fibre mass-gap ideas, cosmology projection safeguards, and R2/fR scalar owner audits. None is yet an accepted parent owner of `L_X X = J_X`.

So memory is not dead, but it is no longer allowed to hover as mist. It is now an unscored retained residual unless the next step constructs a minimal parent quadratic memory action or sources every residual-runner input.

The readout side is cleaner: the readout-domain certificate is installed as explicit closure discipline. It says what we are allowed to do privately without cheating, but it is not counted as a derived local-GR theorem.

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Memory Operator Owner Hunt

{md_table(owner_rows, ["owner_id", "candidate_owner", "owner_status", "missing_to_activate", "claim_effect_if_closed"])}

## Owner Acceptance Gate

{md_table(gate_rows, ["gate_id", "requirement", "gate_pass", "reason"])}

## Readout Domain Certificate

{md_table(readout_rows, ["cert_id", "status", "certificate_clause", "limitation"])}

## Retained Memory Residual Status

{md_table(residual_rows, ["row_id", "branch", "status", "reason", "next_action"])}

## Minimal Action Construction Targets

{md_table(construction_rows, ["target_id", "construction_target", "why_next", "must_prove"])}

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
    owner_rows = memory_operator_owner_hunt()
    gate_rows = owner_acceptance_gate()
    readout_rows = readout_domain_certificate()
    residual_rows = retained_memory_residual_status()
    construction_rows = minimal_action_construction_targets()
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        owner_rows,
        gate_rows,
        readout_rows,
        residual_rows,
        construction_rows,
        claim_rows,
        decision_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_969_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_969_MEMORY_OPERATOR_OWNER_HUNT.csv",
        owner_rows,
        ["owner_id", "candidate_owner", "evidence", "owner_status", "missing_to_activate", "claim_effect_if_closed", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_969_OWNER_ACCEPTANCE_GATE.csv",
        gate_rows,
        ["gate_id", "requirement", "gate_pass", "reason", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_969_READOUT_DOMAIN_CERTIFICATE.csv",
        readout_rows,
        ["cert_id", "certificate_clause", "status", "limitation", "parent_signed", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_969_RETAINED_MEMORY_RESIDUAL_STATUS.csv",
        residual_rows,
        ["row_id", "branch", "status", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_969_MINIMAL_ACTION_CONSTRUCTION_TARGETS.csv",
        construction_rows,
        ["target_id", "construction_target", "why_next", "must_prove", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_969_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_969_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_969_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_969_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, owner_rows, gate_rows, readout_rows, residual_rows, construction_rows, claim_rows, decision_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()

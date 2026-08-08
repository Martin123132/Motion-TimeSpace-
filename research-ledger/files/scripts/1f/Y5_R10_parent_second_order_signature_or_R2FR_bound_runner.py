from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md"
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
            "source_id": "962_doc",
            "path": "962-Y5-R10-R2-fR-zero-clause-proof-or-scalar-mode-bound-source-acquisition.md",
            "role": "handoff: R2/fR relative zero theorem",
            "needle": "R2Z962_5_relative_zero_theorem",
        },
        {
            "source_id": "962_proof_csv",
            "path": "source-intake/mts_residuals/P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv",
            "role": "machine-readable relative zero proof attempt",
            "needle": "RELATIVE_THEOREM_PROVEN_PARENT_PREMISE_UNSIGNED",
        },
        {
            "source_id": "440_second_order",
            "path": "440-metric-only-second-order-sector-reduction-attempt.md",
            "role": "sector-by-sector metric-only/second-order reduction attempt",
            "needle": "metric-only second-order route",
        },
        {
            "source_id": "439_premise_ladder",
            "path": "439-EH-only-exterior-parent-premise-ladder.md",
            "role": "EH-only parent premise ladder and P6 blocker",
            "needle": "P6_second_order_metric_equations",
        },
        {
            "source_id": "423_minimality",
            "path": "423-parent-action-minimality-no-extension-theorem-attempt.md",
            "role": "minimality/no-extension theorem attempt",
            "needle": "parent_universal_property_derived",
        },
        {
            "source_id": "511_fixed_point_action",
            "path": "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
            "role": "minimal parent-action fixed-point ansatz",
            "needle": "A511_3_extra_field_silence",
        },
        {
            "source_id": "710_scalar_descent",
            "path": "710-Y5-R10-scalar-class-zero-premise-parent-action-clause-or-frame-transfer-guard.md",
            "role": "scalar/class no-prefactor/no-kinetic descent candidate",
            "needle": "DPC710_4_no_local_kinetic_mode",
        },
        {
            "source_id": "956_GR_spine",
            "path": "956-Y5-R10-source-side-GR-reduction-spine-and-left-hand-EH-gate-map.md",
            "role": "source-side GR spine and left-hand EH gate map",
            "needle": "LHG956_0_EH_core_selection",
        },
        {
            "source_id": "R11_executable",
            "path": "source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv",
            "role": "current executable-vector placeholder for finite R2/fR branch",
            "needle": "R2_fR_scalar_mode",
        },
    ]
    rows = []
    for spec in specs:
        path = source_path(spec["path"])
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def derivative_order_audit() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "DO963_0_962_relative_theorem",
            "premise": "R2/fR relative zero theorem",
            "evidence": "962 proves nonlinear f(R) is excluded if the parent local exterior is exactly metric-only, second-order, and no-extra-scalar.",
            "status": "relative_theorem_available",
            "failure_mode": "does not by itself prove MTS parent satisfies the premise",
            "closes_R2FR_if_true": "conditional_only",
            "next_action": "audit parent action for exact second-order/no-extra-scalar signature",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "DO963_1_439_P6",
            "premise": "parent forbids higher-derivative local metric equations",
            "evidence": "439 labels P6_second_order_metric_equations as central_blocker_not_derived and V6_second_order_restriction as central_open.",
            "status": "not_parent_signed",
            "failure_mode": "R2/f(R), Ricci/Weyl squared, and nonlocal operators remain legal unless zeroed, topological, decoupled, or coefficient-mapped",
            "closes_R2FR_if_true": "yes",
            "next_action": "derive a symmetry/regularity/minimality theorem forbidding higher-curvature local propagating equations",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "DO963_2_440_sector_reduction",
            "premise": "solved extra sectors do not regenerate higher-curvature operators",
            "evidence": "440 warns that integrating out a field can create f(R), R^2, Yukawa, or nonlocal terms.",
            "status": "not_parent_signed",
            "failure_mode": "a harmless-looking auxiliary/scalar sector could reappear as an effective R2/fR operator",
            "closes_R2FR_if_true": "yes_for_integrate_out_leak",
            "next_action": "require a no-integrated-out-curvature-tower certificate for every eliminated sector",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "DO963_3_511_fixed_point",
            "premise": "fixed-point parent action has EH core plus silent extra fields",
            "evidence": "511 supplies an ansatz with EH core and extra-field silence conditions including C(Phi0)=0 and dC(Phi0)=0.",
            "status": "ansatz_not_derivation",
            "failure_mode": "the ansatz contains extra fields and ellipsis terms; it does not prove no higher-curvature metric operator is generated",
            "closes_R2FR_if_true": "partial",
            "next_action": "turn the fixed-point ansatz into a parent-derived action theorem or keep it closure-only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "DO963_4_710_scalar_descent",
            "premise": "no scalar/class R-prefactor and no local kinetic scalar mode",
            "evidence": "710 writes DPC710_2_no_R_prefactor and DPC710_4_no_local_kinetic_mode as candidate clauses, not parent-signed results.",
            "status": "candidate_not_parent_signed",
            "failure_mode": "scalar/class labels can still make delta_AEH_scalar, finite-range R10/PPN effects, or a scalar-tensor/f(R)-like branch",
            "closes_R2FR_if_true": "partial_for_scalar_class_not_pure_curvature",
            "next_action": "derive scalar/class descent from quotient geometry or retain scalar rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "DO963_5_423_minimality",
            "premise": "parent minimality/no-extension forbids adding material/invariant marker operators",
            "evidence": "423 records parent_universal_property_derived=fail and local_invariant_algebra_triviality_derived=fail.",
            "status": "not_parent_signed",
            "failure_mode": "covariant marker extensions or quotient-invariant scalars can still be legal parent fields",
            "closes_R2FR_if_true": "indirectly_by_forbidding_extra_scalar_generators",
            "next_action": "prove Q_MTS is a primitive minimal quotient object with no natural marker functor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "DO963_6_verdict",
            "premise": "absolute parent second-order/no-extra-scalar signature",
            "evidence": "current sources provide a clean sufficient contract and a relative R2/fR zero theorem, but not the parent theorem that activates it.",
            "status": "NOT_PARENT_SIGNED_CURRENT_CORPUS",
            "failure_mode": "absolute c_R2=c_fR=0 remains unclaimed; finite scalar-mode fallback remains nonclaim",
            "closes_R2FR_if_true": "would_close",
            "next_action": "target no-higher-derivative/minimality theorem or implement nonclaim bound runner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def no_extra_scalar_signature() -> list[dict[str, str]]:
    return [
        {
            "signature_id": "NES963_0_field_split",
            "required_clause": "all non-observed scalar/class variables are either absent, pure gauge, topological, or varied and retained",
            "current_status": "closure_policy_not_theorem",
            "risk_if_missing": "hidden scalar can source local stress, clock drift, or fifth-force rows",
            "would_help_R2FR": "prevents scalar-tensor route to effective f(R)",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "signature_id": "NES963_1_no_R_prefactor",
            "required_clause": "no quotient/class scalar multiplies R or the EH prefactor in the observed frame",
            "current_status": "candidate_clause_not_parent_signed",
            "risk_if_missing": "F(sigma)R produces delta_AEH_scalar and can mimic f(R)/scalar-tensor leakage",
            "would_help_R2FR": "kills scalar prefactor branch",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "signature_id": "NES963_2_no_local_kinetic_scalar",
            "required_clause": "no local propagating scalar/class kinetic mode survives in compact ordinary exterior",
            "current_status": "candidate_clause_not_parent_signed",
            "risk_if_missing": "finite scalar range produces R10/PPN/WEP/Gdot channels",
            "would_help_R2FR": "removes scalaron-like fallback if pure R2 is absent",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "signature_id": "NES963_3_no_integrated_out_tower",
            "required_clause": "integrating out auxiliary/projector/memory variables cannot generate R2, f(R), Ricci/Weyl, or nonlocal metric operators",
            "current_status": "not_derived",
            "risk_if_missing": "parent can look second-order before reduction while the effective observed action is higher-curvature",
            "would_help_R2FR": "directly blocks hidden origin of c_R2/c_fR",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "signature_id": "NES963_4_no_marker_extension",
            "required_clause": "no covariant material marker or invariant scalar is an admissible parent-action extension unless retained as physical residual",
            "current_status": "not_derived",
            "risk_if_missing": "extra scalar generators remain legal by covariance and can carry local charges",
            "would_help_R2FR": "removes the primitive loophole behind scalar extensions",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "signature_id": "NES963_5_verdict",
            "required_clause": "no-extra-scalar parent signature",
            "current_status": "BLOCKED_NOT_PARENT_SIGNED",
            "risk_if_missing": "R2/fR zero theorem stays conditional and finite scalar-mode runner remains necessary",
            "would_help_R2FR": "would close scalar side of parent second-order signature",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def coefficient_owner_audit() -> list[dict[str, str]]:
    return [
        {
            "owner_id": "CO963_0_parent_zero_owner",
            "coefficient": "c_R2_or_c_fR",
            "candidate_owner": "parent exact second-order/no-extra-scalar theorem",
            "owner_status": "relative_theorem_ready_parent_signature_missing",
            "required_evidence": "proof that S_ext has no higher-derivative local metric operator and no integrated-out scalar curvature tower",
            "claim_effect": "would set coefficient to theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "owner_id": "CO963_1_topological_owner",
            "coefficient": "c_R2_or_c_fR",
            "candidate_owner": "4D topological Gauss-Bonnet/boundary combination",
            "owner_status": "not_current_row",
            "required_evidence": "exact GB combination and zero local/boundary flux certificate",
            "claim_effect": "would demote local variation to harmless boundary/topological term",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "owner_id": "CO963_2_redefinition_owner",
            "coefficient": "c_R2_or_c_fR",
            "candidate_owner": "field redefinition redundancy",
            "owner_status": "not_certified",
            "required_evidence": "matter/source/readout and boundary equivalence under the redefinition",
            "claim_effect": "would remove observable R2/fR leakage without changing clocks, mass, or PPN readout",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "owner_id": "CO963_3_numeric_owner",
            "coefficient": "c_R2_or_c_fR",
            "candidate_owner": "finite scalar-mode residual row",
            "owner_status": "MISSING_PARENT_INPUT",
            "required_evidence": "numeric coefficient, units, normalization, scalar mass, scalar coupling, screening flag, and source path",
            "claim_effect": "would make R10/PPN comparison possible but not theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "owner_id": "CO963_4_verdict",
            "coefficient": "c_R2_or_c_fR",
            "candidate_owner": "current corpus",
            "owner_status": "NO_EXECUTABLE_OWNER_FOUND",
            "required_evidence": "choose and prove one owner route above",
            "claim_effect": "absolute R2/fR branch remains blocked",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def bound_runner_spec() -> list[dict[str, str]]:
    return [
        {
            "spec_id": "R2RUN963_0_model_input",
            "runner_component": "MTS scalar-mode prediction",
            "required_fields": "model_id; c_R2_or_fRR; coefficient_units; normalization; branch_context",
            "current_value": "MISSING_PARENT_INPUT",
            "acceptance_rule": "reject if coefficient is missing, dimensionless units are undeclared, or status is closure-only",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "spec_id": "R2RUN963_1_mass_coupling_map",
            "runner_component": "scalaron mass/coupling map",
            "required_fields": "m_s_or_lambda_s; alpha_s; screening_flag; formula_reference",
            "current_value": "formula_known_but_MTS_inputs_missing",
            "acceptance_rule": "reject if alpha/lambda are inferred without parent coefficient or explicit unscreened assumption",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "spec_id": "R2RUN963_2_R10_bound_curve",
            "runner_component": "R10 alpha(lambda) bound data",
            "required_fields": "lambda_value; lambda_units; alpha_bound; source_url; extraction_method; valid_for_claim",
            "current_value": "anchors_exist_full_curve_missing",
            "acceptance_rule": "anchor_only_non_curve rows may run smoke tests but cannot prove pass",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "spec_id": "R2RUN963_3_PPN_branch",
            "runner_component": "PPN gamma/beta projection",
            "required_fields": "gamma_predicted; beta_predicted; regime; source bound; screening/context",
            "current_value": "Cassini_source_string_recorded_no_MTS_projection",
            "acceptance_rule": "reject if scalar range/regime does not map cleanly to solar-system PPN observable",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "spec_id": "R2RUN963_4_decision_logic",
            "runner_component": "claim gate",
            "required_fields": "zero_theorem_signed OR all numeric prediction and bound rows sourced",
            "current_value": "neither_condition_met",
            "acceptance_rule": "claim_allowed=false unless zero theorem signed or abs(alpha_predicted)<=alpha_bound with valid full source rows",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE963_0_parent_second_order_signature",
            "claim": "MTS parent action forbids higher-curvature scalar metric operators",
            "required_condition": "P6 second-order restriction plus no-integrated-out curvature tower plus no-extra-scalar signature",
            "current_evidence": "all are candidate/central-open, not parent-signed",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE963_1_absolute_R2FR_zero",
            "claim": "c_R2=c_fR=0 in MTS",
            "required_condition": "parent second-order signature activates 962 relative theorem",
            "current_evidence": "relative theorem exists; activator premise missing",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE963_2_R2FR_runner_ready",
            "claim": "finite R2/fR scalar branch can be scored",
            "required_condition": "numeric MTS coefficient/mass/coupling plus full bound curve or PPN projection",
            "current_evidence": "runner spec written; inputs missing",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE963_3_local_GR_promotion",
            "claim": "local EH/Newton/GR branch promotes",
            "required_condition": "R2/fR zero, connection gate, source-normalization/GM, and PPN gates all close",
            "current_evidence": "R2/fR absolute zero and connection/source gates remain open",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC963_0_signature_result",
            "topic": "parent second-order signature",
            "result": "not_parent_signed",
            "reason": "the current corpus has an EH/Lovelock contract and a relative R2/fR kill theorem, but P6/no-extra-scalar/no-integrate-out-tower remain open",
            "next_action": "attack no-higher-derivative/minimality theorem directly",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC963_1_R2FR_status",
            "topic": "R2/fR scalar branch",
            "result": "boxed_but_not_killed",
            "reason": "it is now clear what kills it: exact parent second-order/no-extra-scalar signature; current evidence does not prove that signature",
            "next_action": "keep scalar-mode bound runner spec nonclaim until either zero theorem or finite coefficient exists",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC963_2_best_route",
            "topic": "next route",
            "result": "derive_minimality_no_higher_derivative_before_curve_digitization",
            "reason": "full R10 curve digitization is useful only after MTS admits a finite scalar; derivation-first can remove the whole leak",
            "next_action": "try parent no-higher-derivative minimality theorem; if it fails, implement the nonclaim R2/fR runner from the spec",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md",
            "objective": "try to prove a parent no-higher-derivative/minimality theorem that activates the 962 R2/fR zero result; if it fails, implement a strict nonclaim R2/fR scalar-mode runner with missing-input gates",
            "include": "primitive quotient/minimality; no natural marker functor; no integrated-out curvature tower; second-order P6 activator; R2/fR runner spec",
            "exclude": "torsion full proof, EH/local-GR claim, invented coefficients, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    derivative_rows: list[dict[str, str]],
    scalar_rows: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    signature_blocked = any(row["audit_id"] == "DO963_6_verdict" and row["status"] == "NOT_PARENT_SIGNED_CURRENT_CORPUS" for row in derivative_rows)
    scalar_blocked = any(row["signature_id"] == "NES963_5_verdict" and row["current_status"] == "BLOCKED_NOT_PARENT_SIGNED" for row in scalar_rows)
    no_owner = any(row["owner_id"] == "CO963_4_verdict" and row["owner_status"] == "NO_EXECUTABLE_OWNER_FOUND" for row in owner_rows)
    runner_nonclaim = all(row["ready_for_runner"] == "false" and row["valid_for_claim"] == "false" for row in runner_rows)
    claim_safe = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    no_formalization_edits = formalization_changed_after_start() == 0
    outputs_inside_root = all(
        str(path.resolve()).startswith(str(ROOT.resolve()))
        for path in [
            DOC,
            OUT / "P8_Y5_R10_963_SOURCE_REGISTER.csv",
            OUT / "P8_Y5_R10_963_DERIVATIVE_ORDER_AUDIT.csv",
            OUT / "P8_Y5_R10_963_NO_EXTRA_SCALAR_SIGNATURE.csv",
            OUT / "P8_Y5_R10_963_R2FR_COEFFICIENT_OWNER_AUDIT.csv",
            OUT / "P8_Y5_R10_963_R2FR_BOUND_RUNNER_SPEC.csv",
            OUT / "P8_Y5_R10_963_CLAIM_GATE.csv",
            OUT / "P8_Y5_R10_963_DECISION_LEDGER.csv",
            OUT / "P8_Y5_R10_963_NEXT_TARGET.csv",
            OUT / "P8_Y5_BRR545_963_VALIDATION.csv",
        ]
    )
    checks = [
        ("V963_0_sources_checked", sources_ok, "all cited local source paths exist and needles were found"),
        ("V963_1_signature_blocked", signature_blocked, "parent second-order signature remains unsigned"),
        ("V963_2_no_extra_scalar_blocked", scalar_blocked, "no-extra-scalar signature remains unsigned"),
        ("V963_3_no_R2FR_owner", no_owner, "no executable R2/fR coefficient owner found"),
        ("V963_4_runner_nonclaim", runner_nonclaim, "R2/fR runner spec remains nonclaim and not ready"),
        ("V963_5_claim_gates_false", claim_safe, "claim gates all reject absolute pass"),
        ("V963_6_decisions_ready", len(decision_rows) == 3, "decision ledger has three rows"),
        ("V963_7_next_target_ready", len(target_rows) == 1, "next target row written"),
        ("V963_8_formalization_untouched", no_formalization_edits, "formalization-workbench modified-file count since script start is zero"),
        ("V963_9_outputs_inside_post_checkpoint", outputs_inside_root, "all outputs resolve inside post-checkpoint-work"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "V963_10_validation_rows_ready",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "963 validation pack assembled",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    derivative_rows: list[dict[str, str]],
    scalar_rows: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 963 Y5 R10: Parent Second-Order Signature Or R2/fR Bound Runner

Status: `Y5_R10_963_parent_second_order_signature_not_signed_R2FR_runner_spec_written_nonclaim`

Claim ceiling: no EH, R2/fR zero, R10, PPN, Newton, measured-GM, or local-GR pass is claimed.

## Readout

The `R2/fR` leak is now boxed, but not killed. Checkpoint 962 proved the relative theorem: exact local second-order metric-only parent dynamics with no scalar implies `c_R2=c_fR=0`. Checkpoint 963 asks whether the current parent corpus actually signs that premise. It does not.

The precise missing lock is not “do more algebra.” It is a parent no-higher-derivative/minimality theorem: no higher-curvature local metric operators, no integrated-out scalar curvature tower, and no quotient-invariant marker/scalar extension that can re-enter as `F(sigma)R`, `R^2`, `f(R)`, or a finite scalaron.

That sounds harsh, but it is useful harsh: the theory now has a named gate rather than vague danger smoke.

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Derivative-Order Audit

{md_table(derivative_rows, ["audit_id", "premise", "status", "failure_mode", "next_action"])}

## No-Extra-Scalar Signature

{md_table(scalar_rows, ["signature_id", "required_clause", "current_status", "risk_if_missing", "would_help_R2FR"])}

## R2/fR Coefficient Owner Audit

{md_table(owner_rows, ["owner_id", "candidate_owner", "owner_status", "required_evidence", "claim_effect"])}

## R2/fR Bound Runner Spec

{md_table(runner_rows, ["spec_id", "runner_component", "required_fields", "current_value", "acceptance_rule", "ready_for_runner"])}

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
    derivative_rows = derivative_order_audit()
    scalar_rows = no_extra_scalar_signature()
    owner_rows = coefficient_owner_audit()
    runner_rows = bound_runner_spec()
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        derivative_rows,
        scalar_rows,
        owner_rows,
        runner_rows,
        claim_rows,
        decision_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_963_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_963_DERIVATIVE_ORDER_AUDIT.csv",
        derivative_rows,
        ["audit_id", "premise", "evidence", "status", "failure_mode", "closes_R2FR_if_true", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_963_NO_EXTRA_SCALAR_SIGNATURE.csv",
        scalar_rows,
        ["signature_id", "required_clause", "current_status", "risk_if_missing", "would_help_R2FR", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_963_R2FR_COEFFICIENT_OWNER_AUDIT.csv",
        owner_rows,
        ["owner_id", "coefficient", "candidate_owner", "owner_status", "required_evidence", "claim_effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_963_R2FR_BOUND_RUNNER_SPEC.csv",
        runner_rows,
        ["spec_id", "runner_component", "required_fields", "current_value", "acceptance_rule", "ready_for_runner", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_963_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_963_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_963_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_963_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, derivative_rows, scalar_rows, owner_rows, runner_rows, claim_rows, decision_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()

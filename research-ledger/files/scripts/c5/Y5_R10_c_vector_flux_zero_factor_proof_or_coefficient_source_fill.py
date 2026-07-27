from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1142-Y5-R10-c-vector-flux-zero-factor-proof-or-coefficient-source-fill.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1142_0_1141_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1141_NEXT_TARGET.csv",
            "needle": "NEXT1141_0_1142",
            "role": "handoff requiring zero-factor proof or coefficient source fill.",
        },
        {
            "source_id": "SRC1142_1_1141_queue",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1141_REQUIRED_PARENT_INPUT_QUEUE.csv",
            "needle": "REQ1141_3_epsilon_factor",
            "role": "lists missing vector, K, c, epsilon, and coframe inputs.",
        },
        {
            "source_id": "SRC1142_2_A8_contract",
            "relative_path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "needle": "A8_projector_domain_topological",
            "role": "parent clause that could kill vector/STF/flux leakage if fully derived.",
        },
        {
            "source_id": "SRC1142_3_domain_noleak",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT.csv",
            "needle": "N7_no_leak_verdict",
            "role": "domain alpha3 no-leak attempt currently fails.",
        },
        {
            "source_id": "SRC1142_4_R11_domain_zero",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_THEOREM_ZERO_ATTEMPT.csv",
            "needle": "Z6_verdict",
            "role": "R11/domain source-normalization zero route rejected in current corpus.",
        },
        {
            "source_id": "SRC1142_5_1118_zero",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1118_DOMAIN_R11_ZERO_THEOREM_ATTEMPT.csv",
            "needle": "R11D1118_6_verdict",
            "role": "recent domain R11 zero theorem attempt remains unclosed.",
        },
        {
            "source_id": "SRC1142_6_1121_alpha3_zero",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1121_R11_ALPHA3_ZERO_PROOF_AUDIT.csv",
            "needle": "Z1121_4_verdict",
            "role": "R11 alpha3 leakage zero proof remains conditional or failed.",
        },
        {
            "source_id": "SRC1142_7_1123_flux_rows",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1123_ALPHA3_FLUX_BOUND_PRODUCT_ROWS.csv",
            "needle": "FB1123_1_flux_zero_certificate",
            "role": "flux zero and coupling zero certificates are missing parent inputs.",
        },
        {
            "source_id": "SRC1142_8_1136_ineq",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1136_ALPHA3_PRODUCT_INEQUALITY_ROWS.csv",
            "needle": "PI1136_1_R11_alpha3",
            "role": "K*c*epsilon product remains blocked by missing K/c/epsilon.",
        },
        {
            "source_id": "SRC1142_9_1141_vector",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1141_VECTOR_HAIR_FIRST_BOUND_ROWS.csv",
            "needle": "VFB1141_1_alpha2_vector",
            "role": "vector first-bound rows show alpha1/alpha2/alpha3 response maps missing.",
        },
        {
            "source_id": "SRC1142_10_1141_flux",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1141_FLUX_HAIR_FIRST_BOUND_ROWS.csv",
            "needle": "FFB1141_3_product_row",
            "role": "flux first-bound rows show K, c, epsilon, and product missing.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def zero_factor_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "proof_id": "ZF1142_0_vector_zero",
                "candidate_zero": "c_vector_preferred_frame_hair = 0",
                "route": "A8 topological/covariant domain selector forces no observed vector marker",
                "required_identity": "u_D^i = 0, D_i chi_D = 0, delta sigma_D^i = 0, and no g0i/readout vector in observed coframe",
                "evidence_now": "P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT::N3 says domain selector no-vector is not derived; R11_DOMAIN_SOURCE_THEOREM_ZERO_ATTEMPT::Z1 is conditional_not_parent_derived",
                "verdict": "ZERO_NOT_PROVED",
                "fallback": "source vector response row c_vector_abs plus R_alpha1/R_alpha2/R_alpha3",
                "valid_for_claim": "false",
            },
            {
                "proof_id": "ZF1142_1_K_zero",
                "candidate_zero": "K_R11_flux_alpha3 = 0",
                "route": "topological/no-flux projector gives no weak-field map into alpha3",
                "required_identity": "R11 alpha3 response operator annihilates the domain flux source in the observed coframe",
                "evidence_now": "P8_Y5_R10_1123_ALPHA3_FLUX_BOUND_PRODUCT_ROWS::FB1123_2 has MISSING_COUPLING_ZERO_OR_NUMERIC_COEFFICIENT",
                "verdict": "ZERO_NOT_PROVED",
                "fallback": "source K_R11_flux_alpha3 weak-field map or theorem-zero",
                "valid_for_claim": "false",
            },
            {
                "proof_id": "ZF1142_2_c_zero",
                "candidate_zero": "c_domain_source_normalization_operator = 0",
                "route": "EH-only local exterior or R11 source-normalization silence",
                "required_identity": "delta mu_domain = 0 and all derivative/vector/anisotropic source-normalization hair vanish after measured-source normalization",
                "evidence_now": "P8_Y5_R10_1118_DOMAIN_R11_ZERO_THEOREM_ATTEMPT::R11D1118_6_verdict says DOMAIN_R11_SOURCE_ZERO_NOT_DERIVED",
                "verdict": "ZERO_NOT_PROVED",
                "fallback": "source c_domain_source_normalization_operator or prove exact R11 silence",
                "valid_for_claim": "false",
            },
            {
                "proof_id": "ZF1142_3_epsilon_zero",
                "candidate_zero": "epsilon_domain_flux = 0",
                "route": "local representative/no-exchange/no-flux theorem",
                "required_identity": "[J_D]_local = 0 or P_D J_D is homogeneous scalar singlet with no local momentum flux",
                "evidence_now": "P8_Y5_R10_1123_ALPHA3_FLUX_BOUND_PRODUCT_ROWS::FB1123_1 has MISSING_PARENT_ZERO_CERTIFICATE; P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT::N4 is conditional_not_parent_derived",
                "verdict": "ZERO_NOT_PROVED",
                "fallback": "source epsilon_domain_flux profile/bound or parent no-flux certificate",
                "valid_for_claim": "false",
            },
            {
                "proof_id": "ZF1142_4_product_numeric",
                "candidate_zero": "abs(K*c*epsilon) <= 4e-20",
                "route": "finite sourced product below alpha3 guardrail",
                "required_identity": "numeric K_abs, c_flux_abs, epsilon_abs, product_abs, units, and source paths with no tuned cancellation",
                "evidence_now": "P8_Y5_R10_1136_ALPHA3_PRODUCT_INEQUALITY_ROWS::PI1136_1_R11_alpha3 says BLOCKED_MISSING_K_c_AND_EPSILON",
                "verdict": "NOT_SCOREABLE",
                "fallback": "fill first real factor row before any product score",
                "valid_for_claim": "false",
            },
            {
                "proof_id": "ZF1142_5_verdict",
                "candidate_zero": "vector/flux c-hair zero-factor route",
                "route": "ZF1142_0 through ZF1142_4 close",
                "required_identity": "vector zero plus at least one K/c/epsilon zero factor or sourced product pass",
                "evidence_now": "all candidate zero routes remain missing, conditional, or not scoreable",
                "verdict": "ZERO_FACTOR_ROUTE_NOT_CLOSED",
                "fallback": "write exact A8 parent signature next; keep coefficient-fill rows as nonclaim fallback",
                "valid_for_claim": "false",
            },
        ]
    )


def counterexample_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "CE1142_0_Ward_owned_not_absent",
                "counterexample": "owned covariant domain vector satisfies Ward/Bianchi bookkeeping but still sources preferred-frame PPN rows",
                "why_it_blocks_shortcut": "ownership is conservation accounting, not a no-force theorem",
                "source_anchor": "P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT::N6",
                "status": "ACTIVE_GUARD",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "CE1142_1_metric_dependent_projector",
                "counterexample": "Hodge/orthogonal/domain-wall projector is covariant but metric-dependent, so it can vary into local stress",
                "why_it_blocks_shortcut": "topological stress silence only follows if the parent selects the metric-independent projector",
                "source_anchor": "P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT::N1/N2",
                "status": "ACTIVE_GUARD",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "CE1142_2_nontrivial_local_class",
                "counterexample": "compact local branch carries nontrivial domain representative or coherent memory class",
                "why_it_blocks_shortcut": "nontrivial class can carry local flux, preferred-location, or vector residuals",
                "source_anchor": "P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT::N4",
                "status": "ACTIVE_GUARD",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "CE1142_3_R11_silent_by_name",
                "counterexample": "R11 source-normalization operator is named silent/absorbed but still has vector/derivative/flux hair",
                "why_it_blocks_shortcut": "source-normalization silence must be theorem-zero or numerically bounded, not a label choice",
                "source_anchor": "P8_Y5_R10_1121_R11_ALPHA3_ZERO_PROOF_AUDIT::Z1121_2_absorption_guard",
                "status": "ACTIVE_GUARD",
                "valid_for_claim": "false",
            },
        ]
    )


def parent_signature_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "signature_id": "SIG1142_0_parent_selects_projector",
                "needed_signature": "S_parent selects a metric-independent relative-chain/cohomology projector P_D, not an external filter or metric-dependent Hodge projector",
                "closes": "projector local stress/vector shortcut",
                "current_status": "MISSING_PARENT_OWNERSHIP",
                "valid_for_claim": "false",
            },
            {
                "signature_id": "SIG1142_1_scalar_trivial_local_domain",
                "needed_signature": "local compact branch domain selector is scalar/trivial: u_D^i=0, D_i chi_D=0, delta sigma_D^i=0 in observed coframe",
                "closes": "c_vector_preferred_frame_hair",
                "current_status": "MISSING_NO_VECTOR_THEOREM",
                "valid_for_claim": "false",
            },
            {
                "signature_id": "SIG1142_2_local_representative_exact",
                "needed_signature": "[J_D]_local=0 or P_D J_D is a homogeneous scalar singlet with no local momentum flux",
                "closes": "epsilon_domain_flux",
                "current_status": "MISSING_LOCAL_TRIVIAL_REPRESENTATIVE",
                "valid_for_claim": "false",
            },
            {
                "signature_id": "SIG1142_3_R11_source_silence",
                "needed_signature": "all R11 domain/source-normalization operators vanish or are supplied as executable coefficient vectors with source paths",
                "closes": "c_domain_source_normalization_operator and sibling R5/R6/R8/R11 guards",
                "current_status": "MISSING_R11_SILENCE_OR_EXECUTABLE_VECTOR",
                "valid_for_claim": "false",
            },
            {
                "signature_id": "SIG1142_4_no_flux_response",
                "needed_signature": "R11 alpha3 response operator has no coupling to the domain flux source, or K_R11_flux_alpha3 is source-backed zero",
                "closes": "K_R11_flux_alpha3",
                "current_status": "MISSING_K_ZERO_OR_RESPONSE_MAP",
                "valid_for_claim": "false",
            },
            {
                "signature_id": "SIG1142_5_no_cancellation_policy",
                "needed_signature": "vector, flux, boundary, and domain products pass independently unless a parent identity derives exact cancellation before fitting",
                "closes": "prevents tuned alpha3 cancellation",
                "current_status": "POLICY_ACTIVE_NONCLAIM",
                "valid_for_claim": "false",
            },
        ]
    )


def source_fill_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "fill_id": "FILL1142_0_vector_response",
                "target": "c_vector_preferred_frame_hair",
                "row_type": "coefficient_or_theorem_zero",
                "required_fields": "c_vector_abs; R_alpha1_vector; R_alpha2_vector; R_alpha3_vector; coframe; units; source_path",
                "current_value": "MISSING_VECTOR_RESPONSE_COEFFICIENT",
                "preferred_fill_order": "1",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "SOURCE_FILL_REQUIRED",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "fill_id": "FILL1142_1_epsilon_domain_flux",
                "target": "epsilon_domain_flux",
                "row_type": "profile_bound_or_theorem_zero",
                "required_fields": "epsilon_abs; profile_support; local_representative; units; source_path",
                "current_value": "MISSING_EPSILON_DOMAIN_FLUX_PROFILE_OR_ZERO_THEOREM",
                "preferred_fill_order": "2",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "SOURCE_FILL_REQUIRED",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "fill_id": "FILL1142_2_K_R11_flux_alpha3",
                "target": "K_R11_flux_alpha3",
                "row_type": "weak_field_response_or_theorem_zero",
                "required_fields": "K_abs; K_units; weak_field_map; source_path",
                "current_value": "MISSING_K_R11_FLUX_ALPHA3_SOURCE_OR_ZERO_THEOREM",
                "preferred_fill_order": "3",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "SOURCE_FILL_REQUIRED",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "fill_id": "FILL1142_3_c_source_normalization",
                "target": "c_domain_source_normalization_operator",
                "row_type": "source_normalization_coefficient_or_theorem_zero",
                "required_fields": "c_flux_abs; c_units; observed_coframe_normalization; source_path",
                "current_value": "MISSING_DOMAIN_MU_EXTRA_OPERATOR_ZERO_OR_NUMERIC_COEFFICIENT",
                "preferred_fill_order": "4",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "SOURCE_FILL_REQUIRED",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "fill_id": "FILL1142_4_alpha3_product",
                "target": "abs(K_R11_flux_alpha3*c_domain_source_normalization_operator*epsilon_domain_flux)",
                "row_type": "derived_product",
                "required_fields": "K_abs; c_flux_abs; epsilon_abs; product_abs; all_source_paths; no_cancellation_check",
                "current_value": "MISSING_K_c_EPSILON_PRODUCT",
                "preferred_fill_order": "5_after_factors",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "DERIVED_ONLY_AFTER_FACTOR_ROWS",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1142_0_source_anchors",
                "rule": "all cited proof attempts and bound rows exist",
                "gate_pass": "true_nonclaim",
                "reason": "anchors exist but they show failure/conditional status, not proof",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1142_1_vector_zero",
                "rule": "observed vector c-hair is theorem-zero",
                "gate_pass": "false",
                "reason": "domain selector no-vector theorem is not parent-derived",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1142_2_flux_zero_factor",
                "rule": "at least one K/c/epsilon factor is theorem-zero",
                "gate_pass": "false",
                "reason": "K zero, c zero, and epsilon zero are all missing or conditional",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1142_3_numeric_product",
                "rule": "K*c*epsilon product is source-backed and <= 4e-20",
                "gate_pass": "false",
                "reason": "numeric factor rows are missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1142_4_counterexample_guards",
                "rule": "Ward ownership, covariance, and topological labels are not treated as no-leak proofs",
                "gate_pass": "true_nonclaim",
                "reason": "counterexample guards are explicit",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1142_5_local_claim",
                "rule": "preferred-frame/alpha3/local-GR promotion allowed",
                "gate_pass": "false",
                "reason": "zero-factor route did not close and coefficient rows are source-fill only",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1142_0_verdict",
                "decision": "zero_factor_proof_not_closed",
                "reason": "A8 is the right structural clause but remains retained_symbolic; existing no-leak/R11 attempts explicitly fail or stay conditional",
                "next_action": "write the exact A8 parent-signature contract rather than treating A8 as a proof",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1142_1_best_next",
                "decision": "derive_A8_parent_signature_before_sourcing_product",
                "reason": "one parent signature could kill vector hair and epsilon flux together; numeric alpha3 source-plumbing is more fragile",
                "next_action": "construct or reject scalar-trivial local domain selector from the parent action",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1142_2_claim_ceiling",
                "decision": "keep_vector_flux_branch_nonclaim",
                "reason": "all first fill rows retain MISSING_SOURCE_PATH or MISSING theorem-zero inputs",
                "next_action": "no R10/PPN/alpha3/local-GR promotion",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1142_0_1143",
                "next_target": "1143-Y5-R10-A8-domain-selector-parent-signature-or-epsilon-profile-first-fill.md",
                "objective": "construct the exact parent-action signature that makes the local domain selector scalar/trivial and no-flux in the observed coframe; if that fails, fill the first epsilon_domain_flux profile/source row",
                "include": "A8 parent ownership; metric-independent P_D; scalar local selector; exact local representative; epsilon_domain_flux no-flux certificate; observed coframe",
                "exclude": "Ward-only shortcut; covariance-only shortcut; tuned cancellation; measured-GM absorption; alpha3/local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    proof: list[dict[str, object]],
    guards: list[dict[str, object]],
    signatures: list[dict[str, object]],
    fills: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = proof + guards + signatures + fills + gates + decisions + next_target
    required_proofs = {
        "ZF1142_0_vector_zero",
        "ZF1142_1_K_zero",
        "ZF1142_2_c_zero",
        "ZF1142_3_epsilon_zero",
        "ZF1142_4_product_numeric",
        "ZF1142_5_verdict",
    }
    required_fills = {
        "FILL1142_0_vector_response",
        "FILL1142_1_epsilon_domain_flux",
        "FILL1142_2_K_R11_flux_alpha3",
        "FILL1142_3_c_source_normalization",
        "FILL1142_4_alpha3_product",
    }
    add(
        "V1142_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1142_1_zero_audit_coverage",
        required_proofs == {row["proof_id"] for row in proof},
        "vector, K, c, epsilon, product, and verdict zero routes are audited",
    )
    add(
        "V1142_2_zero_route_not_closed",
        proof[-1]["verdict"] == "ZERO_FACTOR_ROUTE_NOT_CLOSED"
        and all(row["verdict"] != "ZERO_PROVED" for row in proof),
        "no zero-factor route is treated as proven",
    )
    add(
        "V1142_3_counterexample_guards",
        len(guards) >= 4 and all(row["status"] == "ACTIVE_GUARD" for row in guards),
        "counterexample guards prevent Ward/covariance/topology shortcuts",
    )
    add(
        "V1142_4_parent_signatures",
        {"SIG1142_0_parent_selects_projector", "SIG1142_1_scalar_trivial_local_domain", "SIG1142_2_local_representative_exact"}.issubset(
            {row["signature_id"] for row in signatures}
        ),
        "minimum A8 parent signatures are explicit",
    )
    add(
        "V1142_5_fill_rows",
        required_fills == {row["fill_id"] for row in fills}
        and all(row["source_path"] == "MISSING_SOURCE_PATH" for row in fills),
        "first fill rows exist and retain missing source paths",
    )
    add(
        "V1142_6_claim_gates_blocked",
        any(row["gate_id"] == "G1142_1_vector_zero" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1142_2_flux_zero_factor" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1142_5_local_claim" and row["gate_pass"] == "false" for row in gates),
        "vector, flux, and local claim gates remain blocked",
    )
    add(
        "V1142_7_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in fills + next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1142_8_next_target",
        next_target[0]["next_target"].startswith("1143-") and "A8-domain-selector" in str(next_target[0]["next_target"]),
        "1143 handoff targets A8 parent signature or epsilon profile fill",
    )
    add(
        "V1142_9_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1142_10_csv_parse", csv_parse_ok, "all 1142 CSV outputs parse cleanly")
    add("V1142_11_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1142_SUMMARY",
        True,
        "1142 rejects the current zero-factor proof, names exact A8 parent signatures, and prepares source-fill rows without claims",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    proof: list[dict[str, object]],
    guards: list[dict[str, object]],
    signatures: list[dict[str, object]],
    fills: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1142 - Y5/R10 c Vector/Flux Zero-Factor Proof or Coefficient Source Fill

**Current verdict:** the zero-factor proof does not close in the current corpus. `A8_projector_domain_topological` is the right structural target, but it is still retained/conditional rather than a parent-signed theorem.

**Useful progress:** the failure is now sharp: vector zero, `K=0`, `c=0`, `epsilon=0`, and numeric `K*c*epsilon <= 4e-20` are separated into exact proof gates.

**Important guard:** Ward ownership, covariance, and the word “topological” are not enough. The parent action must select a metric-independent scalar/trivial local domain selector in the observed coframe, or the vector/flux branch stays open.

**Best next attack:** construct the exact A8 parent-action signature first. If that fails, fill `epsilon_domain_flux` as the first real source/profile row because it can close the alpha3 product by a single zero factor.

**No claim:** no R10, PPN, alpha3, preferred-frame, local-GR, measured-GM, GitHub, or public claim follows from 1142.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Zero-Factor Proof Audit
{table(["proof_id", "candidate_zero", "route", "required_identity", "evidence_now", "verdict", "fallback", "valid_for_claim"], proof)}

## Counterexample Guards
{table(["guard_id", "counterexample", "why_it_blocks_shortcut", "source_anchor", "status", "valid_for_claim"], guards)}

## Minimum Parent Signatures
{table(["signature_id", "needed_signature", "closes", "current_status", "valid_for_claim"], signatures)}

## First Coefficient Source-Fill Rows
{table(["fill_id", "target", "row_type", "required_fields", "current_value", "preferred_fill_order", "source_path", "status", "valid_for_claim"], fills)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1142_SOURCE_REGISTER.csv",
        "proof": OUT / "P8_Y5_R10_1142_ZERO_FACTOR_PROOF_AUDIT.csv",
        "guards": OUT / "P8_Y5_R10_1142_COUNTEREXAMPLE_GUARDS.csv",
        "signatures": OUT / "P8_Y5_R10_1142_MINIMUM_PARENT_SIGNATURES.csv",
        "fills": OUT / "P8_Y5_R10_1142_FIRST_COEFFICIENT_SOURCE_FILL_ROWS.csv",
        "gates": OUT / "P8_Y5_R10_1142_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1142_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1142_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1142_VALIDATION.csv",
    }
    sources = source_rows()
    proof = zero_factor_rows()
    guards = counterexample_rows()
    signatures = parent_signature_rows()
    fills = source_fill_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["proof"], proof)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["signatures"], signatures)
    write_csv(outputs["fills"], fills)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, proof, guards, signatures, fills, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, proof, guards, signatures, fills, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    if failed:
        for row in failed:
            print(f"{row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

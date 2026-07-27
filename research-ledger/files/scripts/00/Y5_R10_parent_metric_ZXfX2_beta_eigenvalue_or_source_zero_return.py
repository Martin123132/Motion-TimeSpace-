from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1026-Y5-R10-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


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
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1026_0_1025_next", "source-intake/mts_residuals/P8_Y5_R10_1025_NEXT_TARGET.csv", "1026-Y5-R10-parent-metric", "1025 handoff to parent metric/eigenvalue."),
        ("SRC1026_1_1025_locks", "source-intake/mts_residuals/P8_Y5_R10_1025_FIELD_NORMALIZATION_LOCKS.csv", "FNL1025_1_canonical_metric", "1025 metric/eigenvalue locks."),
        ("SRC1026_2_1025_hessian", "source-intake/mts_residuals/P8_Y5_R10_1025_PARENT_HESSIAN_AUDIT.csv", "PHA1025_4_cross_Hessian", "1025 cross-Hessian blocker."),
        ("SRC1026_3_617_field_space", "source-intake/mts_residuals/P8_Y5_R10_617_FIELD_SPACE_NORMALIZATION_ATTEMPT.csv", "FS617_2_canonical_vacuum_metric", "617 canonical metric contract."),
        ("SRC1026_4_617_beta", "source-intake/mts_residuals/P8_Y5_R10_617_BETA_EIGENVALUE_CANDIDATE_LEDGER.csv", "BS617_1_beta3", "617 beta candidate ledger."),
        ("SRC1026_5_616_parent_contract", "source-intake/mts_residuals/P8_Y5_R10_616_PARENT_X_BLOCK_OWNER_CONTRACT.csv", "PC616_2_field_space_metric_lock", "616 parent X owner contract."),
        ("SRC1026_6_210_metric", "210-GK-alphaK-parent-invariant-or-fixed-closure.md", "parent metric `M_AB` derived | fail", "210 field-space metric precedent."),
        ("SRC1026_7_211_ward", "211-GK-parent-metric-Ward-identity-attempt.md", "derive `M_AB` as a Hessian or Ward/current norm", "211 parent metric Ward attempt."),
        ("SRC1026_8_223_constraint", "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md", "trace/traceless split fixes", "223 trace/traceless owner clue."),
        ("SRC1026_9_224_vdef", "224-defect-potential-Vdef-or-X-route-demotion.md", "full defect potential is not parent-derived", "224 defect potential demotion."),
        ("SRC1026_10_511_fixed_point", "511-minimal-parent-action-local-GR-fixed-point-ansatz.md", "FP511_1_double_zero_nonEH_coupling", "511 fixed-point/double-zero contract."),
        ("SRC1026_11_516_doublet", "516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md", "Gamma_eff = Gamma0 + 1/2 M_AB", "516 response-doublet quadratic candidate."),
        ("SRC1026_12_517_variation", "517-response-doublet-action-variation-ledger-or-run-q_loc-bound.md", "AV517_1_scalar_density", "517 response-doublet variation ledger."),
        ("SRC1026_13_618_nopole", "source-intake/mts_residuals/P8_Y5_R10_618_NO_POLE_CERTIFICATE_AUDIT.csv", "NPC618_6_no_pole_promotion", "618 no-pole certificate status."),
        ("SRC1026_14_618_sourcezero", "source-intake/mts_residuals/P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv", "SZ618_0_qbar_XT_chain_rule", "618 source-zero certificate status."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="ignore") if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def parent_metric_rows() -> list[dict[str, str]]:
    return [
        {
            "metric_id": "PM1026_0_metric_target",
            "target": "derive parent field-space metric restricted to X",
            "candidate_statement": "G_XX := M_AB e_X^A e_X^B and Z_X f_X^2 := G_XX f_X^2",
            "current_evidence": "210/211/224 identify M_AB as the missing parent metric, not a derived object",
            "status": "TARGET_DEFINED_NOT_OWNED",
            "missing_for_claim": "parent M_AB, normalized X direction e_X, and field units",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "metric_id": "PM1026_1_Ward_identity_attempt",
            "target": "derive M_AB from a Ward/current norm",
            "candidate_statement": "M_AB = <J_A,J_B> or Hessian/current norm fixed by a parent symmetry",
            "current_evidence": "211 asks for a Ward/current norm; 1008/1010 warn Ward identities assign ownership but do not prove piecewise silence",
            "status": "WARD_ROUTE_CONDITIONAL_NOT_METRIC_LOCK",
            "missing_for_claim": "inner product, current basis, sign, units, and stress variation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "metric_id": "PM1026_2_defect_Hessian_attempt",
            "target": "derive M_AB from a defect potential Hessian",
            "candidate_statement": "M_AB = partial_A partial_B V_def|_0",
            "current_evidence": "224 gives partial trace/flow support but says full V_def and M_AB are not parent-derived",
            "status": "PARTIAL_TRACE_FLOW_SUPPORT_NOT_FULL_METRIC",
            "missing_for_claim": "full defect potential, Weyl/Q/J_rel weights, cross terms, and positive metric",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "metric_id": "PM1026_3_response_doublet_attempt",
            "target": "use even response doublets for double-zero and positive metric",
            "candidate_statement": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "current_evidence": "516/517 make the double-zero route coherent if M_AB is parent-owned; it remains candidate_written_not_matched",
            "status": "DOUBLE_ZERO_CONDITIONAL_PARENT_MATCH_MISSING",
            "missing_for_claim": "map Z^A to current MTS X, parent-owned M_AB, boundary/domain silence, and metric variation lock",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "metric_id": "PM1026_4_canonical_vacuum_lock",
            "target": "lock field metric to vacuum scale",
            "candidate_statement": "Z_X f_X^2 = rho_vac^(1/2)",
            "current_evidence": "617 calls this a clean contract but not signed; 1025 retains it as FNL1025_1",
            "status": "CLEAN_CONTRACT_NOT_SIGNED",
            "missing_for_claim": "parent Ward/metric theorem equating the X norm to the vacuum density scale",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "metric_id": "PM1026_5_cross_block_guard",
            "target": "make the X scalar truncation legal",
            "candidate_statement": "Hessian block either diagonalizes into X plus positive orthogonal sectors or all cross terms are bounded",
            "current_evidence": "1025 PHA1025_4 says mixed X-sector Hessian proof is missing",
            "status": "MISSING_BLOCK_DIAGONAL_OR_POSITIVE_MATRIX_PROOF",
            "missing_for_claim": "projector onto X, positive Schur complement, or retained residual vector",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "metric_id": "PM1026_6_verdict",
            "target": "parent metric lock",
            "candidate_statement": "parent_signed(M_AB,e_X,V_def) -> Z_X f_X^2=rho_vac^(1/2)",
            "current_evidence": "no inspected source supplies all objects from one parent branch",
            "status": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "M_AB, e_X, V_def/H_X, units, and stress/Bianchi variation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def beta_eigenvalue_rows() -> list[dict[str, str]]:
    return [
        {
            "beta_id": "BE1026_0_spectral_definition",
            "target": "define beta without post-hoc fitting",
            "candidate_statement": "beta_eff is an eigenvalue of H_X := rho_vac^(-1/2) G_X^{-1/2} (partial_X^2 V_eff) G_X^{-1/2}",
            "current_evidence": "617/1025 isolate beta_eff but do not derive the metric or Hessian spectrum",
            "status": "CONDITIONAL_DEFINITION_ONLY",
            "missing_for_claim": "parent G_X, V_eff, branch, spectrum, and units",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "beta_id": "BE1026_1_spatial_trace_beta3",
            "target": "derive U''(0)=3",
            "candidate_statement": "three equal spatial trace channels give beta=3 if X is exactly the normalized spatial-trace mode",
            "current_evidence": "617/1025 keep beta=3 as best low-scrutiny theorem target, not signed",
            "status": "BEST_TARGET_NOT_THEOREM",
            "missing_for_claim": "trace projector, isotropic eigenvalue degeneracy, no time/Weyl leakage, parent metric",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "beta_id": "BE1026_2_time_or_constraint_modes",
            "target": "reject model-chosen beta=4,5,6 promotion",
            "candidate_statement": "extra time/constraint/regular modes can shift beta only if their eigenvalues are parent-owned",
            "current_evidence": "616/617 list beta 4,5,6 as candidates with weaker ownership",
            "status": "CANDIDATES_DEMOTED",
            "missing_for_claim": "mode count, constraint algebra, and spectral theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "beta_id": "BE1026_3_direct_backsolve",
            "target": "forbid range backsolve",
            "candidate_statement": "beta=5.206677122050 directly hits lambda=38.6um",
            "current_evidence": "617 labels direct 38.6um backsolve closure_only",
            "status": "FORBIDDEN_AS_DERIVATION",
            "missing_for_claim": "independent parent spectrum reproducing the number before R10 comparison",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "beta_id": "BE1026_4_verdict",
            "target": "beta eigenvalue ownership",
            "candidate_statement": "parent_signed(H_X spectrum) -> beta_eff, then lambda_X=ell_vac/sqrt(beta_eff)",
            "current_evidence": "no parent-signed spectrum exists in the inspected corpus",
            "status": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "normalized Hessian spectrum and trace/eigenvalue theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def source_zero_return_rows() -> list[dict[str, str]]:
    return [
        {
            "return_id": "SZR1026_0_route_trigger",
            "route": "finite metric/eigenvalue route",
            "current_status": "NOT_PROMOTED",
            "because": "M_AB, e_X, Z_X f_X^2, and beta are not signed",
            "next_use": "return to source-zero/no-pole before any alpha claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "return_id": "SZR1026_1_no_pole",
            "route": "quotient/no-pole",
            "current_status": "STILL_STRONGEST_IF_CLOSED",
            "because": "no physical X Green function would make K_X=0 instead of merely small",
            "next_use": "requires parent projection, first-class constraint, and zero boundary charge",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "return_id": "SZR1026_2_qbar_XT",
            "route": "matter source-zero",
            "current_status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "because": "SZ618_0 gives qbar_XT=0 if matter descends through the observed quotient and Lie_vX(theta_A)=0",
            "next_use": "try to parent-sign the matter/coframe descent or write a bounded qbar_XT row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "return_id": "SZR1026_3_Qbar_XH",
            "route": "Hamiltonian/source projection zero",
            "current_status": "NOT_DERIVED",
            "because": "boundary charge and Pi_M^H projection remain open",
            "next_use": "retain Qbar_XH source row unless boundary/projector theorem closes",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "return_id": "SZR1026_4_KX",
            "route": "no Green function",
            "current_status": "CONDITIONAL_ONLY",
            "because": "K_X=0 needs no physical X pole after first-class quotient and boundary audit",
            "next_use": "retain K_X row unless no-pole certificate closes",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "return_id": "SZR1026_5_verdict",
            "route": "next target",
            "current_status": "SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW",
            "because": "finite metric/eigenvalue ownership failed current claim; coupling is the live route",
            "next_use": "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def branch_verdict_rows() -> list[dict[str, str]]:
    return [
        {
            "verdict_id": "BV1026_0_parent_metric",
            "branch": "M_AB / field-space metric",
            "status": "not_parent_signed",
            "because": "M_AB is repeatedly identified as the missing parent metric, but no file derives it with X direction, sign, units, and stress variation",
            "allowed_statement": "M_AB is the right ownership target",
            "forbidden_statement": "M_AB is already derived for MTS local X",
            "next_action": "do not promote finite lambda until M_AB/e_X is signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "verdict_id": "BV1026_1_beta",
            "branch": "beta eigenvalue",
            "status": "not_parent_signed",
            "because": "beta=3 is a clean spatial-trace target but remains a target, not a spectrum theorem",
            "allowed_statement": "beta=3 remains the least-posthoc finite theorem target",
            "forbidden_statement": "beta=3 or lambda=50.85um is a prediction",
            "next_action": "only reopen beta after a parent metric/spectrum source exists",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "verdict_id": "BV1026_2_finite_route",
            "branch": "finite R10 route",
            "status": "demoted_to_closure_sidecar",
            "because": "range and amplitude would still be independently chosen without one normalization ledger",
            "allowed_statement": "finite route is useful private pressure testing",
            "forbidden_statement": "finite route derives local GR",
            "next_action": "freeze finite route until source rows are real",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "verdict_id": "BV1026_3_source_zero_return",
            "branch": "source-zero/no-pole",
            "status": "selected_next",
            "because": "removing/silencing the source is a cleaner GR-reduction route than tuning the finite range",
            "allowed_statement": "next work should attack qbar_XT/J_X or bounded coupling rows",
            "forbidden_statement": "WEP/covariance alone proves source-zero",
            "next_action": "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    gates = [
        ("CG1026_0_sources_registered", "all cited source paths exist and expected needles are present", "true", "source register is intact", "false"),
        ("CG1026_1_parent_metric_lock", "Z_X f_X^2=rho_vac^(1/2) is parent-signed", "false", "M_AB/e_X/units are missing", "false"),
        ("CG1026_2_beta_eigenvalue", "U''(0)=3 or beta_eff is parent-signed", "false", "no normalized Hessian spectrum theorem exists", "false"),
        ("CG1026_3_finite_lambda_claim", "lambda_X is a finite prediction", "false", "metric/eigenvalue lock failed", "false"),
        ("CG1026_4_source_zero", "J_X/qbar_XT source-zero is parent-signed", "false", "matter descent remains conditional", "false"),
        ("CG1026_5_no_pole", "K_X=0 from no physical X pole", "false", "constraint and boundary certificates remain open", "false"),
        ("CG1026_6_alpha_claim", "alpha(lambda) row may be scored as evidence", "false", "range/amplitude/source inputs are missing", "false"),
        ("CG1026_7_no_cancellation_guard", "no-cancellation guard active", "true", "unknown metric/source/boundary components cannot cancel into a fake pass", "false"),
        ("CG1026_8_local_GR_claim", "local GR/Newton reduction is derived", "false", "finite route and source-zero/no-pole routes are still unsigned", "false"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "claim_allowed": claim_allowed,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for gate_id, claim, gate_pass, reason, claim_allowed in gates
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1026_0_metric_result",
            "decision": "The parent metric route remains unowned.",
            "because": "M_AB appears as the right object, but current corpus does not derive M_AB restricted to X with units/sign/stress variation.",
            "next_action": "do not claim Z_X f_X^2 or lambda_X from the finite route",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1026_1_beta_result",
            "decision": "Beta=3 survives as a private theorem target only.",
            "because": "spatial trace is the cleanest story, but not a parent spectrum theorem.",
            "next_action": "freeze beta claims until a parent metric/spectrum source appears",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1026_2_finite_route",
            "decision": "The finite Hessian/R10 route is demoted to closure sidecar.",
            "because": "range and amplitude still lack one normalization ledger.",
            "next_action": "use it only as nonclaim pressure testing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1026_3_next_target",
            "decision": "Next target is qbar_XT/J_X source-zero or bounded coupling row.",
            "because": "local-GR reduction is stronger if the matter source coupling vanishes by parent descent or is explicitly bounded.",
            "next_action": "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
            "objective": "derive qbar_XT=0/J_X=0 from parent matter/coframe descent, or create a claim-blocked bounded qbar_XT source row with units, source path, arena, and no-cancellation guard",
            "include": "matter action descent, observed coframe pullback, Lie_vX(theta_A), species constants, hidden/source/domain terms, bounded qbar_XT schema, Qbar_XH/K_X dependency, no-cancellation guard",
            "exclude": "WEP-only proof, covariance-only proof, placeholder zero, unsourced qbar_XT value, finite-lambda claim, R10/PPN/local-GR claim, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file():
            modified = datetime.fromtimestamp(candidate.stat().st_mtime, timezone.utc)
            if modified >= STARTED:
                changed.append(candidate)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    metric: list[dict[str, str]],
    beta: list[dict[str, str]],
    source_zero: list[dict[str, str]],
    verdicts: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    metric_required = {f"PM1026_{idx}_{name}" for idx, name in [
        (0, "metric_target"),
        (1, "Ward_identity_attempt"),
        (2, "defect_Hessian_attempt"),
        (3, "response_doublet_attempt"),
        (4, "canonical_vacuum_lock"),
        (5, "cross_block_guard"),
        (6, "verdict"),
    ]}
    beta_required = {f"BE1026_{idx}_{name}" for idx, name in [
        (0, "spectral_definition"),
        (1, "spatial_trace_beta3"),
        (2, "time_or_constraint_modes"),
        (3, "direct_backsolve"),
        (4, "verdict"),
    ]}
    source_required = {f"SZR1026_{idx}_{name}" for idx, name in [
        (0, "route_trigger"),
        (1, "no_pole"),
        (2, "qbar_XT"),
        (3, "Qbar_XH"),
        (4, "KX"),
        (5, "verdict"),
    ]}
    checks = [
        ("V1026_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and expected needles are present"),
        ("V1026_1_metric_rows_complete", metric_required.issubset({row["metric_id"] for row in metric}), "parent metric attempt covers M_AB, Ward, defect Hessian, doublet, vacuum lock, cross block, and verdict"),
        ("V1026_2_metric_nonclaim", all(row["valid_for_claim"] == "false" for row in metric) and any(row["metric_id"] == "PM1026_6_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in metric), "parent metric lock remains nonclaim"),
        ("V1026_3_beta_rows_complete", beta_required.issubset({row["beta_id"] for row in beta}), "beta attempt covers spectral definition, beta3, other candidates, direct backsolve, and verdict"),
        ("V1026_4_beta_nonclaim", all(row["valid_for_claim"] == "false" for row in beta) and any(row["beta_id"] == "BE1026_4_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in beta), "beta eigenvalue remains nonclaim"),
        ("V1026_5_source_return_complete", source_required.issubset({row["return_id"] for row in source_zero}), "source-zero return rows are complete"),
        ("V1026_6_source_return_selected", any(row["return_id"] == "SZR1026_5_verdict" and "1027-Y5-R10-qbarXT" in row["next_use"] for row in source_zero), "1027 source-zero/bounded coupling target selected"),
        ("V1026_7_verdicts_complete", {"BV1026_0_parent_metric", "BV1026_1_beta", "BV1026_2_finite_route", "BV1026_3_source_zero_return"}.issubset({row["verdict_id"] for row in verdicts}), "branch verdicts are complete"),
        ("V1026_8_claim_gates_blocked", all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in gates), "all claim gates refuse promotion"),
        ("V1026_9_no_cancellation_guard", any(row["gate_id"] == "CG1026_7_no_cancellation_guard" and flag(row["gate_pass"]) for row in gates), "no-cancellation guard is active"),
        ("V1026_10_decision_written", any(row["decision_id"] == "DEC1026_3_next_target" for row in decisions), "1027 decision row is written"),
        ("V1026_11_next_target_written", len(next_target) == 1 and "1027-Y5-R10-qbarXT" in next_target[0]["next_target"], "1027 next target row is present"),
        ("V1026_12_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1026_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1026 parent metric/eigenvalue and source-zero return validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    metric: list[dict[str, str]],
    beta: list[dict[str, str]],
    source_zero: list[dict[str, str]],
    verdicts: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1026 Y5 R10 parent metric ZXfX2 beta eigenvalue or source zero return",
            "",
            "**Status:** The parent metric route was tried and sharpened. `M_AB`, the X direction `e_X`, the vacuum metric lock `Z_X f_X^2=rho_vac^(1/2)`, and the beta spectrum remain unowned. The finite Hessian/R10 route is therefore demoted to a closure sidecar, and the next serious route returns to `qbar_XT/J_X` source-zero or bounded coupling rows.",
            "",
            "**Claim ceiling:** no `Z_X f_X^2` lock, no beta prediction, no finite lambda claim, no alpha(lambda) pass, no R10/PPN pass, and no local-GR/Newton reduction is allowed from 1026.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Parent metric attempt",
            md_table(metric, ["metric_id", "target", "candidate_statement", "current_evidence", "status", "missing_for_claim", "valid_for_claim"]),
            "## Beta eigenvalue attempt",
            md_table(beta, ["beta_id", "target", "candidate_statement", "current_evidence", "status", "missing_for_claim", "valid_for_claim"]),
            "## Source-zero return",
            md_table(source_zero, ["return_id", "route", "current_status", "because", "next_use", "valid_for_claim"]),
            "## Branch verdicts",
            md_table(verdicts, ["verdict_id", "branch", "status", "because", "allowed_statement", "forbidden_statement", "next_action", "valid_for_claim"]),
            "## Claim gates",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
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
    metric = parent_metric_rows()
    beta = beta_eigenvalue_rows()
    source_zero = source_zero_return_rows()
    verdicts = branch_verdict_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, metric, beta, source_zero, verdicts, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1026_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1026_PARENT_METRIC_ATTEMPT.csv", metric)
    write_csv(OUT / "P8_Y5_R10_1026_BETA_EIGENVALUE_ATTEMPT.csv", beta)
    write_csv(OUT / "P8_Y5_R10_1026_SOURCE_ZERO_RETURN.csv", source_zero)
    write_csv(OUT / "P8_Y5_R10_1026_BRANCH_VERDICTS.csv", verdicts)
    write_csv(OUT / "P8_Y5_R10_1026_CLAIM_GATES.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1026_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1026_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1026_VALIDATION.csv", validations)
    write_doc(sources, metric, beta, source_zero, verdicts, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()

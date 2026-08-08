from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md"
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
        ("SRC1023_0_1022_next", "source-intake/mts_residuals/P8_Y5_R10_1022_NEXT_TARGET.csv", "q-vX-action", "1022 handoff to q/v_X/action descent certificate."),
        ("SRC1023_1_1022_vertical", "source-intake/mts_residuals/P8_Y5_R10_1022_VERTICAL_QUOTIENT_CONSTRUCTION.csv", "VQC1022_7_verdict", "1022 vertical quotient verdict."),
        ("SRC1023_2_1022_scalar", "source-intake/mts_residuals/P8_Y5_R10_1022_SCALAR_NOHAIR_CONSTRUCTION.csv", "SNH1022_6_verdict", "1022 scalar fallback verdict."),
        ("SRC1023_3_581_chain", "source-intake/mts_residuals/P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv", "QVT581_7_alpha_result", "581 quotient theorem chain."),
        ("SRC1023_4_581_certificate", "source-intake/mts_residuals/P8_Y5_R10_581_NO_POLE_CERTIFICATE_TEMPLATE.csv", "NPC581_6_claim_gate", "581 no-pole certificate template."),
        ("SRC1023_5_637_qmap", "source-intake/mts_residuals/P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv", "QM637_2_vertical_kernel", "637 q map/kernel result."),
        ("SRC1023_6_637_action", "source-intake/mts_residuals/P8_Y5_R10_637_PARENT_ACTION_DERIVATION_ATTEMPT.csv", "PA637_3_action_descent", "637 parent action descent attempt."),
        ("SRC1023_7_637_obs", "source-intake/mts_residuals/P8_Y5_R10_637_OBS_FUNCTOR_DERIVATION.csv", "OF637_1_chain_rule", "637 matter/observed functor chain rule."),
        ("SRC1023_8_590_field_map", "source-intake/mts_residuals/P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv", "boundary_edge", "590 field-by-field vertical action gaps."),
        ("SRC1023_9_590_closure", "source-intake/mts_residuals/P8_Y5_R10_590_MAPPING_CLOSURE_GATE.csv", "MCG590_2_vertical_generator", "590 mapping closure gate."),
        ("SRC1023_10_583_momentum", "source-intake/mts_residuals/P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv", "NMC583_3_momentum_map", "583 momentum map contract."),
        ("SRC1023_11_670_nopole", "source-intake/mts_residuals/P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv", "NQ670_8_no_pole_result", "670 no-pole proof result."),
        ("SRC1023_12_670_sourcefree", "source-intake/mts_residuals/P8_Y5_R10_670_POSITIVE_SOURCEFREE_PROOF_CHAIN.csv", "PSF670_6_zero_profile_result", "670 positive source-free fallback."),
        ("SRC1023_13_669_residuals", "source-intake/mts_residuals/P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv", "RV669_0_Z_X", "669 scalar/source residual vector."),
    ]
    rows = []
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


def certificate_rows() -> list[dict[str, str]]:
    rows = [
        {
            "certificate_id": "QVC1023_0_parent_q",
            "required_object": "parent quotient map q",
            "pass_condition": "q is canonical parent reduction, not post-readout projection; Dq[v_X]=0 for the actual local X direction",
            "current_evidence": "637 gives conditional q if v_X is in the parent null distribution",
            "current_status": "partial_conditional",
            "missing_for_claim": "prove actual local Xhat variations equal the null/relative-exact generator on the local branch",
            "claim_effect_if_signed": "X is representative data, not a physical local field",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "certificate_id": "QVC1023_1_NX_integrability",
            "required_object": "integrable null distribution N_X",
            "pass_condition": "N_X is parent-owned, invariant under parent symmetries, and integrable on the compact local domain",
            "current_evidence": "637/581 state the construction conditionally",
            "current_status": "not_parent_signed",
            "missing_for_claim": "field-space distribution and global/domain admissibility",
            "claim_effect_if_signed": "q fibres are legitimate representative orbits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "certificate_id": "QVC1023_2_action_descent",
            "required_object": "parent action descent",
            "pass_condition": "S_parent[Phi]=S_red[q(Phi)]+fixed boundary/topological terms before variation",
            "current_evidence": "637 PA637_3 is a conditional theorem with retained boundary/domain terms",
            "current_status": "conditional_only",
            "missing_for_claim": "explicit parent Lagrangian and proof retained boundary/domain terms are silent",
            "claim_effect_if_signed": "no independent X Hessian, Green function, or K_X",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "certificate_id": "QVC1023_3_matter_descent",
            "required_object": "ordinary matter quotient functor",
            "pass_condition": "S_matter=Sbar_m[Obs(q(Phi)),psi,theta_A] and L_vX theta_A=0 for constants/material markers",
            "current_evidence": "637 chain rule is math-pass for metric/frame part",
            "current_status": "conditional_theorem_only",
            "missing_for_claim": "no-marker constants, EM/material labels, and hidden conformal/disformal channel exclusion",
            "claim_effect_if_signed": "qbar_XT=0 and no ordinary matter X source",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "certificate_id": "QVC1023_4_vertical_action",
            "required_object": "field-by-field v_X",
            "pass_condition": "v_X is specified on metric/coframe, canonical data, memory/projector/domain fields, matter readout, and boundary fields",
            "current_evidence": "590 field map lists candidates but marks multiple blocks missing/unmapped",
            "current_status": "missing",
            "missing_for_claim": "actual MTS parent transformation law",
            "claim_effect_if_signed": "DCdagger/Omega-flat map becomes a calculation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "certificate_id": "QVC1023_5_momentum_map",
            "required_object": "differentiable first-class generator",
            "pass_condition": "delta G_X=Omega(delta Phi,v_X), G_X=int epsilon C_X+Q_X, and bracket closes with no active K_boundary",
            "current_evidence": "583 and 590 give the contract but parent theta/Omega/DC_X/Q_X are missing",
            "current_status": "not_derived",
            "missing_for_claim": "parent symplectic potential, DC_X, boundary differentiability, and algebra closure",
            "claim_effect_if_signed": "X is constraint/gauge, not physical source field",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "certificate_id": "QVC1023_6_boundary_silence",
            "required_object": "local boundary/edge silence",
            "pass_condition": "Q_X=0/proper/exact and Pi_M^H[Q_X]=0 with no edge cocycle on compact branch",
            "current_evidence": "1019-1021 show B_X primitive and projector orthogonality remain unsigned",
            "current_status": "blocked",
            "missing_for_claim": "B_X primitive, weighted-Stokes zero/bound, projector orthogonality, and cocycle",
            "claim_effect_if_signed": "Qbar_XH=0 and no edge alpha branch",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "certificate_id": "QVC1023_7_degree_count",
            "required_object": "constraint rank and reduced nondegeneracy",
            "pass_condition": "primary+secondary first-class pair removes X pair; reduced Omega has no proper X stabilizer",
            "current_evidence": "581/590 require this but do not compute it",
            "current_status": "not_checked",
            "missing_for_claim": "rank calculation, no-stabilizer theorem, and reduced phase-space proof",
            "claim_effect_if_signed": "zero Hessian becomes gauge evidence rather than under-specified dynamics",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "certificate_id": "QVC1023_8_verdict",
            "required_object": "single q/v_X/action descent certificate",
            "pass_condition": "QVC1023_0 through QVC1023_7 all parent-signed together",
            "current_evidence": "multiple conditional pieces exist, but no single parent certificate closes",
            "current_status": "fail_current_claim_demote_current_branch",
            "missing_for_claim": "q, v_X, action, matter, boundary, and degree certificates",
            "claim_effect_if_signed": "K_X=qbar_XT=Qbar_XH=0 and local X alpha inactive",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def coupling_audit_rows() -> list[dict[str, str]]:
    rows = [
        {
            "audit_id": "CDA1023_0_metric_chain_rule",
            "object": "metric/coframe matter variation",
            "result": "conditional_math_pass",
            "reason": "DObs(Dq[v_X])=0 kills the metric/frame pullback only if v_X is truly vertical",
            "remaining_coupling": "none from metric/frame channel if q/v_X closes",
            "demotion_effect": "if q/v_X fails, this becomes a finite qbar_XT or matter-coupling row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "CDA1023_1_constants_markers",
            "object": "theta_A constants/material labels",
            "result": "not_closed",
            "reason": "L_vX theta_A=0 is not parent-owned for EM, clocks, masses, or material labels",
            "remaining_coupling": "constant/material marker X-dependence",
            "demotion_effect": "retain qbar_XT and WEP/clock/fifth-force residual rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "CDA1023_2_hidden_frame",
            "object": "hidden conformal/disformal X channel",
            "result": "counterexample_filter_only",
            "reason": "637 says hidden X-frame dependence is observable and must factor through q or be finite-coupled",
            "remaining_coupling": "F_X prime or disformal coefficient if present",
            "demotion_effect": "source/coefficient route, not quotient theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "CDA1023_3_projector_boundary",
            "object": "projector/boundary coupling",
            "result": "open",
            "reason": "B_X, Pi_M^H[Q_edge], K_boundary, and source split remain unsigned",
            "remaining_coupling": "edge/source projection into measured Hamiltonian mass",
            "demotion_effect": "retain EDGEBOUND and Qbar_edge_XH rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "CDA1023_4_verdict",
            "object": "coupling descent verdict",
            "result": "coupling_not_theorem_zero",
            "reason": "matter descent and boundary/projector descent are conditional, not parent-signed",
            "remaining_coupling": "qbar_XT;Qbar_XH;edge terms;clock/WEP channels",
            "demotion_effect": "move to scalar/source input pack",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def demotion_rows() -> list[dict[str, str]]:
    rows = [
        {
            "demotion_id": "DEM1023_0_scope",
            "demoted_object": "current quotient/vertical no-pole route",
            "demotion": "demoted_to_conditional_only_for_current_MTS",
            "reason": "the single certificate fails at field-by-field v_X, action descent, matter/no-marker descent, boundary silence, and degree count",
            "what_survives": "conditional theorem target remains valid if a future parent action supplies the certificate",
            "next_required_row": "SNH1023 scalar/source input pack",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "demotion_id": "DEM1023_1_scalar_operator",
            "demoted_object": "scalar no-hair fallback",
            "demotion": "promoted_to_next_work_target_not_claim",
            "reason": "it is now the honest executable branch after quotient certificate failure",
            "what_survives": "positive energy identity can still kill X if all inputs close",
            "next_required_row": "Z_X;M_X2;J_X;boundary_flux_X;lambda_X",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "demotion_id": "DEM1023_2_sourced_residual",
            "demoted_object": "finite coupling/source branch",
            "demotion": "retained_as_scoreable_if_scalar_nohair_fails",
            "reason": "nonzero J_X or matter coupling must be tested, not hidden",
            "what_survives": "R10/R11 alpha/source rows",
            "next_required_row": "K_X;Qbar_XH;qbar_XT;alpha_X(lambda);EDGEBOUND terms",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "demotion_id": "DEM1023_3_claim_ceiling",
            "demoted_object": "local-GR/R10/R11 local silence",
            "demotion": "blocked",
            "reason": "no theorem-zero branch or valid source-bound branch closes",
            "what_survives": "discipline: no public/local claim from this chain",
            "next_required_row": "1024 scalar no-hair input pack",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def scalar_input_rows() -> list[dict[str, str]]:
    rows = [
        {
            "input_id": "SNH1023_0_Z_X",
            "quantity": "Z_X",
            "needed_for": "positive kinetic term",
            "required_source": "parent Hessian second variation with field units",
            "current_status": "MISSING_PARENT_INPUT",
            "if_missing": "no scalar no-hair theorem; score residual",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "SNH1023_1_M_X2",
            "quantity": "M_X^2",
            "needed_for": "positive mass gap and lambda_X",
            "required_source": "parent Hessian curvature/range derivation with units",
            "current_status": "MISSING_PARENT_INPUT",
            "if_missing": "zero/long-range/tachyonic mode remains possible",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "SNH1023_2_J_X_zero",
            "quantity": "J_X=0",
            "needed_for": "source-free exterior equation",
            "required_source": "matter/hidden/source variation proof or sourced current bound",
            "current_status": "MISSING_SOURCE_ZERO_PROOF",
            "if_missing": "qbar_XT/source coupling row required",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "SNH1023_3_boundary_flux_zero",
            "quantity": "boundary_flux_X=0",
            "needed_for": "positive energy identity conclusion",
            "required_source": "boundary class/no-hair/projector silence or flux bound",
            "current_status": "MISSING_BOUNDARY_LOCK",
            "if_missing": "EDGEBOUND and Qbar_edge rows remain live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "SNH1023_4_alpha_coefficients",
            "quantity": "K_X;Qbar_XH;qbar_XT;lambda_X",
            "needed_for": "R10/R11 residual scoring if no-hair fails",
            "required_source": "source-normalized coefficient rows with units and no-cancellation envelope",
            "current_status": "MISSING_ARENA_PROJECTION",
            "if_missing": "no local empirical pass",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def claim_gate_rows() -> list[dict[str, str]]:
    rows = [
        ("CG1023_0_sources_registered", "1023 source chain exists", True, "all cited quotient, matter, vertical, and fallback files are found", False),
        ("CG1023_1_q_vX_certificate", "q/v_X/action certificate closes", False, "single certificate fails at multiple required clauses", False),
        ("CG1023_2_coupling_zero", "matter/coupling descent theorem-zero", False, "constants/markers, hidden frame, and boundary/projector coupling remain open", False),
        ("CG1023_3_scalar_nohair_claim", "scalar no-hair theorem", False, "Z_X, M_X2, J_X=0, and boundary_flux_X=0 remain missing", False),
        ("CG1023_4_residual_score_claim", "finite residual score", False, "alpha/source coefficient rows are missing", False),
        ("CG1023_5_demotion_written", "current quotient route demoted", True, "current MTS keeps quotient route conditional and moves executable work to scalar/source inputs", False),
        ("CG1023_6_local_GR_claim", "local GR/Newton reduction", False, "no local branch closes theorem-zero or source-bound pass", False),
        ("CG1023_7_guardrail", "no fake quotient credit", True, "post-readout quotient and scalar-as-edge-proof are forbidden", False),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": str(gate_pass).lower(),
            "reason": reason,
            "claim_allowed": str(claim_allowed).lower(),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for gate_id, claim, gate_pass, reason, claim_allowed in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC1023_0_certificate_result",
            "decision": "The q/v_X/action descent certificate does not close for current MTS.",
            "because": "conditional q-map pieces exist, but no field-by-field vertical action, parent action descent, matter/no-marker descent, boundary silence, or degree count is signed.",
            "next_action": "do not spend no-pole credit from quotient route",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1023_1_demotion",
            "decision": "Demote the current local branch to scalar no-hair/source-coefficient work.",
            "because": "this is the honest executable route after the quotient certificate fails in current files.",
            "next_action": "fill scalar positive operator/source/boundary inputs before testing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1023_2_future_reopen",
            "decision": "The quotient route can be reopened only by a real parent action certificate.",
            "because": "future q/v_X proof would still be the cleanest local-GR route if it supplies all missing clauses together.",
            "next_action": "require q, v_X, action descent, matter descent, boundary silence, and degree count in one source-backed row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1023_3_next_target",
            "decision": "Next target is scalar no-hair input pack or residual coefficient runner.",
            "because": "Z_X, M_X2, J_X=0, boundary_flux_X=0, and alpha coefficients are now the executable local branch inputs.",
            "next_action": "1024-Y5-R10-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1024-Y5-R10-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md",
            "objective": "fill or reject the scalar no-hair input pack: Z_X, M_X^2, J_X=0, boundary_flux_X=0, lambda_X, and fallback alpha coefficients with units and source paths",
            "include": "parent Hessian signs, field units, self-adjoint domain, matter/source zero proof, boundary flux zero/bound, lambda_X, K_X, Qbar_XH, qbar_XT, no-cancellation envelope",
            "exclude": "quotient no-pole credit without certificate, scalar no-hair as edge exactness, source-free by assertion, placeholder coefficients, R10/R11 pass, local-GR claim, GitHub action",
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
    certificate: list[dict[str, str]],
    coupling: list[dict[str, str]],
    demotion: list[dict[str, str]],
    scalar_inputs: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    certificate_required = {f"QVC1023_{index}_{suffix}" for index, suffix in [
        (0, "parent_q"),
        (1, "NX_integrability"),
        (2, "action_descent"),
        (3, "matter_descent"),
        (4, "vertical_action"),
        (5, "momentum_map"),
        (6, "boundary_silence"),
        (7, "degree_count"),
        (8, "verdict"),
    ]}
    coupling_required = {"CDA1023_0_metric_chain_rule", "CDA1023_1_constants_markers", "CDA1023_2_hidden_frame", "CDA1023_3_projector_boundary", "CDA1023_4_verdict"}
    demotion_required = {"DEM1023_0_scope", "DEM1023_1_scalar_operator", "DEM1023_2_sourced_residual", "DEM1023_3_claim_ceiling"}
    scalar_required = {"SNH1023_0_Z_X", "SNH1023_1_M_X2", "SNH1023_2_J_X_zero", "SNH1023_3_boundary_flux_zero", "SNH1023_4_alpha_coefficients"}
    checks = [
        ("V1023_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and expected needles are present"),
        ("V1023_1_certificate_complete", certificate_required.issubset({row["certificate_id"] for row in certificate}), "q/v_X/action/matter/boundary/degree certificate clauses are complete"),
        ("V1023_2_certificate_fails", any(row["certificate_id"] == "QVC1023_8_verdict" and row["current_status"] == "fail_current_claim_demote_current_branch" for row in certificate), "single quotient certificate fails current claim"),
        ("V1023_3_coupling_audit_complete", coupling_required.issubset({row["audit_id"] for row in coupling}), "coupling descent audit covers metric, markers, hidden frame, boundary/projector, and verdict"),
        ("V1023_4_coupling_nonzero_open", any(row["audit_id"] == "CDA1023_4_verdict" and row["result"] == "coupling_not_theorem_zero" for row in coupling), "coupling is not theorem-zero"),
        ("V1023_5_demotion_complete", demotion_required.issubset({row["demotion_id"] for row in demotion}), "demotion rows cover quotient, scalar, sourced, and claim ceiling effects"),
        ("V1023_6_scalar_inputs_complete", scalar_required.issubset({row["input_id"] for row in scalar_inputs}), "scalar no-hair/source input rows are complete"),
        ("V1023_7_scalar_inputs_nonclaim", all(row["valid_for_claim"] == "false" and ("MISSING" in row["current_status"]) for row in scalar_inputs), "scalar/source inputs remain missing and nonclaim"),
        ("V1023_8_claim_gates_blocked", all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in gates), "all claim gates remain nonclaim"),
        ("V1023_9_demotion_gate_written", any(row["gate_id"] == "CG1023_5_demotion_written" and flag(row["gate_pass"]) for row in gates), "demotion gate is installed"),
        ("V1023_10_guardrail_written", any(row["gate_id"] == "CG1023_7_guardrail" and flag(row["gate_pass"]) for row in gates), "no fake quotient credit guardrail is installed"),
        ("V1023_11_decision_written", any(row["decision_id"] == "DEC1023_3_next_target" for row in decisions), "1024 decision row is written"),
        ("V1023_12_next_target_written", len(next_target) == 1 and "1024-Y5-R10-scalar-nohair" in next_target[0]["next_target"], "1024 next target row is present"),
        ("V1023_13_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1023_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1023 q/vX certificate and scalar demotion validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    certificate: list[dict[str, str]],
    coupling: list[dict[str, str]],
    demotion: list[dict[str, str]],
    scalar_inputs: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1023 Y5 R10 q vX action descent certificate or scalar nohair demotion",
            "",
            "**Status:** The single `q/v_X/action` certificate does not close for current MTS. Conditional quotient pieces exist, but the field-by-field vertical action, parent action descent, matter/no-marker descent, boundary silence, and degree count are not parent-signed. The current local branch is therefore demoted to scalar no-hair/source-coefficient work, while the quotient route remains a future theorem target.",
            "",
            "**Claim ceiling:** no quotient no-pole theorem, no coupling-zero theorem, no scalar no-hair theorem, no R10/R11 pass, no PPN pass, and no local-GR/Newton reduction is allowed from 1023.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## q/v_X certificate",
            md_table(certificate, ["certificate_id", "required_object", "pass_condition", "current_evidence", "current_status", "missing_for_claim", "claim_effect_if_signed", "valid_for_claim"]),
            "## Coupling descent audit",
            md_table(coupling, ["audit_id", "object", "result", "reason", "remaining_coupling", "demotion_effect", "valid_for_claim"]),
            "## Demotion ledger",
            md_table(demotion, ["demotion_id", "demoted_object", "demotion", "reason", "what_survives", "next_required_row", "valid_for_claim"]),
            "## Scalar/source input pack",
            md_table(scalar_inputs, ["input_id", "quantity", "needed_for", "required_source", "current_status", "if_missing", "valid_for_claim"]),
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
    certificate = certificate_rows()
    coupling = coupling_audit_rows()
    demotion = demotion_rows()
    scalar_inputs = scalar_input_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, certificate, coupling, demotion, scalar_inputs, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1023_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1023_QVX_CERTIFICATE.csv", certificate)
    write_csv(OUT / "P8_Y5_R10_1023_COUPLING_DESCENT_AUDIT.csv", coupling)
    write_csv(OUT / "P8_Y5_R10_1023_DEMOTION_LEDGER.csv", demotion)
    write_csv(OUT / "P8_Y5_R10_1023_SCALAR_SOURCE_INPUT_PACK.csv", scalar_inputs)
    write_csv(OUT / "P8_Y5_R10_1023_CLAIM_GATES.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1023_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1023_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1023_VALIDATION.csv", validations)
    write_doc(sources, certificate, coupling, demotion, scalar_inputs, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()

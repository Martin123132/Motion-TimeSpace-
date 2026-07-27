from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_MINIMAL_PARENT_MATTER_COUPLING_ACTION_OR_DOMAIN_MOTION_INPUT_2420"
CHECKPOINT_ID = "2420"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2420-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2420_SOURCE_REGISTER.csv",
    "coupling_gate": OUT / "P8_Y5_PARENT_QLOC_2420_MINIMAL_PARENT_COUPLING_GATE.csv",
    "activation_matrix": OUT / "P8_Y5_PARENT_QLOC_2420_SOURCE_DESCENT_ACTIVATION_MATRIX.csv",
    "q_route": OUT / "P8_Y5_PARENT_QLOC_2420_Q_VERTICAL_NOPOLE_ROUTE_LEDGER.csv",
    "residual_stack": OUT / "P8_Y5_PARENT_QLOC_2420_RESIDUAL_FALLBACK_STACK.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2420_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2420_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2420_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2420_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2420_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2420_MINIMAL_PARENT_COUPLING_GATE_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2420_RESIDUAL_STACK_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_MINIMAL_COUPLING_DECISION_2420_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        body.append(
            "| "
            + " | ".join(
                str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
                for column in columns
            )
            + " |"
        )
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2420_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2420-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2420*",
        "*P8_Y5_BRR545_2420*",
        "*Y5_R2FR_minimal_parent_matter_coupling_action_or_domain_motion_input_2420*",
        "*JR2420*",
        "*PARENT_QLOC_MINIMAL_COUPLING_DECISION_2420*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2419_handoff",
            ROOT / "2419-Y5-R2FR-source-worldtube-projector-chainmap-zero-or-readout-reentry-bound-pack.md",
            ["CMG2419_6_verdict", "NEXT2419_0_selected", "VAL2419_OVERALL"],
            "immediate handoff: source-current descent/fixed-domain owner selected as the next chain-map zero antecedent.",
        ),
        (
            "2357_minimal_action",
            ROOT / "2357-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md",
            ["MCA2357_6_descent_result_if_parent_adopted", "DEC2357_0_result", "CG2357_0_matter_coupling_derived", "VAL2357_OVERALL"],
            "minimal parent matter-coupling action candidate and non-derivation verdict.",
        ),
        (
            "2358_q_vertical",
            ROOT / "2358-Y5-R2FR-q-object-vertical-generator-open-branch-proof-or-domain-bound.md",
            ["QVA2358_7_open_branch_verdict", "DQB2358_0_total", "VAL2358_OVERALL"],
            "q-object/open-branch verticality failure and finite Dq envelope.",
        ),
        (
            "2359_q_chart_nopole",
            ROOT / "2359-Y5-R2FR-parent-q-field-chart-equivalence-relation-or-no-pole-selector.md",
            ["FCE2359_5_chart_verdict", "RSL2359_1_second_class_route", "VAL2359_OVERALL"],
            "q field-chart candidate not derived; second-class/no-pole route selected.",
        ),
        (
            "2360_second_class",
            ROOT / "2360-Y5-R2FR-second-class-auxiliary-origin-no-derivative-grammar-or-finite-leak.md",
            ["SCA2360_6_verdict", "NDG2360_6_verdict", "NEXT2360_0_selected"],
            "second-class/no-pole theorem remains conditional; parent origin of C_R selected.",
        ),
        (
            "2361_CR_origin",
            ROOT / "2361-Y5-R2FR-parent-origin-of-CR-from-phase-cell-current-chain-or-finite-qR-row.md",
            ["CR2361_7_verdict", "DEC2361_4_psi_quotient", "NEXT2361_0_selected"],
            "C_R=2 ln J_q identity found but parent origin not derived; psi determinant/quotient route selected.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def coupling_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="MPC2420_0_handoff", clause="2419 chain-map zero dependency", formal_statement="source-worldtube/projector zero needs J_H=q^*Jbar_H, fixed W_source/domain, fixed Pi_W, and same-frame M_H_ref", current_status="CHAINMAP_ZERO_DEPENDS_ON_PARENT_COUPLING", missing_input="minimal parent action plus q/v verticality plus support owner"),
        base_row(row_id="MPC2420_1_minimal_action_form", clause="minimal parent matter action", formal_statement="S_matter = Sbar_matter[q(Phi), Psi, theta, ebar(q), connection_bar(q)] with no independent source-only geometry slot", current_status="CANDIDATE_CONTRACT_ONLY", missing_input="parent derivation from MTS core variables"),
        base_row(row_id="MPC2420_2_factorization", clause="matter factorization", formal_statement="all matter stress/current variations factor through q(Phi) and the reduced observed geometry", current_status="EXACT_IF_ACTION_ADOPTED", missing_input="action adoption certificate"),
        base_row(row_id="MPC2420_3_no_source_only_slot", clause="no hidden source slot", formal_statement="no M_H_ref, W_source, tau, boundary marker, or selector coefficient can enter S_matter outside q/Psi/theta", current_status="REQUIRED_NOT_PARENT_SIGNED", missing_input="operator grammar and source slot exclusion"),
        base_row(row_id="MPC2420_4_variation_before_readout", clause="variation-before-readout", formal_statement="delta S is taken before source readout/projection/GM calibration; readout is post-variation evidence map", current_status="CARRIED_AS_REQUIRED_GUARD", missing_input="selector no-reentry proof remains external"),
        base_row(row_id="MPC2420_5_fixed_support_owner", clause="source support owner", formal_statement="W_source=closure(supp Jbar_H) is owned in the reduced current complex and does not move under vertical representative shifts", current_status="NOT_DERIVED", missing_input="q/v verticality plus compact-support descent"),
        base_row(row_id="MPC2420_6_boundary_silence", clause="boundary/local projection silence", formal_statement="proper boundary terms vanish or are fixed reduced-boundary charges; no vertical boundary tail enters local exterior source readout", current_status="NOT_DERIVED", missing_input="boundary class and domain-motion rows"),
        base_row(row_id="MPC2420_7_current_corpus_verdict", clause="derived MTS coupling?", formal_statement="current corpus does not derive the minimal parent matter action as unique MTS core law", current_status="NOT_DERIVED_FROM_CURRENT_MTS_CORE", missing_input="parent ordinary action or quotient kinematic certificate"),
        base_row(row_id="MPC2420_8_conditional_output", clause="conditional source-current descent theorem", formal_statement="if MPC2420_1..6 plus q/v verticality close, then delta_v S_matter=0 mod Euler/gauge/proper boundary and J_H=q^*Jbar_H", current_status="EXACT_CONDITIONAL_OUTPUT_NOT_ACTIVE", missing_input="q/v open-branch proof or finite domain-motion input"),
    ]


def activation_matrix_rows() -> list[dict[str, Any]]:
    return [
        base_row(clause_id="SAM2420_0_parent_action_adoption", antecedent="minimal parent matter action derived from MTS variables", evidence_source="2357", evidence_status="missing", activates="MPC2420_1..3", passed=False),
        base_row(clause_id="SAM2420_1_q_object", antecedent="q is a parent quotient/object, not a post-hoc readout label", evidence_source="2358/2359", evidence_status="candidate_only", activates="matter factorization and descent", passed=False),
        base_row(clause_id="SAM2420_2_vertical_generator", antecedent="v_X in ker(Dq) for the local representative branch", evidence_source="2358", evidence_status="not_derived", activates="delta_v S_matter=0", passed=False),
        base_row(clause_id="SAM2420_3_no_pole_auxiliary", antecedent="C_R/no-pole auxiliary is parent-signed and has no derivative grammar", evidence_source="2360", evidence_status="conditional_not_closed", activates="regular local exterior reaction silence", passed=False),
        base_row(clause_id="SAM2420_4_CR_origin", antecedent="C_R=0/no reciprocal hair follows from parent law, not boundary normalization", evidence_source="2361", evidence_status="not_derived", activates="q_R finite leak suppression", passed=False),
        base_row(clause_id="SAM2420_5_source_support", antecedent="W_source and linking surface are reduced-current objects before readout", evidence_source="2419", evidence_status="not_parent_signed", activates="fixed-domain chain-map zero", passed=False),
        base_row(clause_id="SAM2420_6_MHref", antecedent="same-frame positive M_H_ref/H_tau/H_ref sourced by the parent current", evidence_source="2419/2357", evidence_status="missing", activates="score-ready residual normalization", passed=False),
        base_row(clause_id="SAM2420_7_verdict", antecedent="all activation antecedents close jointly", evidence_source="2420", evidence_status="blocked", activates="source-current descent/local-GR route", passed=False),
    ]


def q_route_rows() -> list[dict[str, Any]]:
    return [
        base_row(route_id="QNP2420_0_qv_open_branch", route="q/v open-branch verticality", source_checkpoint="2358", result="OPEN_BRANCH_VERTICALITY_NOT_DERIVED", effect_on_coupling="minimal coupling cannot fire as theorem"),
        base_row(route_id="QNP2420_1_q_chart", route="parent q field-chart/equivalence relation", source_checkpoint="2359", result="Q_FIELD_CHART_NOT_DERIVED", effect_on_coupling="q remains candidate kinematics, not public parent structure"),
        base_row(route_id="QNP2420_2_second_class", route="second-class auxiliary/no-pole origin", source_checkpoint="2360", result="CONDITIONAL_THEOREM_NOT_CLOSED_FOR_CLAIM", effect_on_coupling="no-pole route still lacks parent origin and no-derivative grammar"),
        base_row(route_id="QNP2420_3_CR_current_chain", route="phase-cell/current-chain origin of C_R", source_checkpoint="2361", result="C_R=2 ln J_q exact but Q_R hair remains", effect_on_coupling="ordinary current route rejected as standalone derivation"),
        base_row(route_id="QNP2420_4_psi_quotient", route="psi determinant/quotient map", source_checkpoint="2361", result="SELECT_NEXT_ATTACK", effect_on_coupling="least circular route to make q/C_R absent, vertical, or stationary before matter/readout"),
        base_row(route_id="QNP2420_5_verdict", route="current best route", source_checkpoint="2420", result="COUPLING_CONTRACT_VALID_BUT_NOT_PARENT_DERIVED", effect_on_coupling="next step is psi determinant quotient proof or finite q_R coefficients"),
    ]


def residual_stack_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="RFS2420_0_source_domain_motion", quantity="epsilon_source_domain_motion_abs", formula="E_worldtube + E_domain_motion + E_current_escape + boundary/proper-tail terms", status="MISSING_PARENT_SUPPORT_OWNER", score_ready=False),
        base_row(row_id="RFS2420_1_chainmap_readout", quantity="epsilon_chainmap_readout_abs", formula="I_commutator_abs + R_eq_abs + E_worldtube + E_projector_stress + E_domain_motion + E_current_escape + E_exterior + E_MHref_guard", status="INHERITED_NONCLAIM_FROM_2419", score_ready=False),
        base_row(row_id="RFS2420_2_Dq_open_branch", quantity="epsilon_Dq_open_branch_abs", formula="|DObs_e| + |Dsource_readout| + |Dtheta_marker| + |Dboundary_projector| + |Dtau_pushforward| + |boundary_charge|", status="INHERITED_NONCLAIM_FROM_2358", score_ready=False),
        base_row(row_id="RFS2420_3_qR_QR_hair", quantity="q_R/Q_R finite residual", formula="W_R C_R' = Q_R with C_R=2 ln J_q unless no-charge theorem or psi quotient kills hair", status="MISSING_NO_CHARGE_OR_PSI_QUOTIENT_PROOF", score_ready=False),
        base_row(row_id="RFS2420_4_MHref_guard", quantity="M_H_ref/H_tau/H_ref", formula="positive same-frame Hamiltonian/source reference charge, not observed orbital GM", status="MISSING_PARENT_SOURCE_NORMALIZATION", score_ready=False),
        base_row(row_id="RFS2420_5_parent_coefficients", quantity="finite coefficient pack", formula="K_X, Qbar_XH, lambda_X, projection transfer, arena tau rows", status="SOURCE_READY_SCHEMA_ONLY", score_ready=False),
        base_row(row_id="RFS2420_6_public_claim_state", quantity="local evidence status", formula="no R10/WEP/PPN/clock/orbital/local-GR pass until zero proof or sourced finite bounds exist", status="NOT_SCORE_READY", score_ready=False),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2420_0_matter_coupling_derived", gate="minimal parent matter action derived from MTS core", passed=False, claim_effect="coupling remains candidate contract"),
        base_row(gate_id="CG2420_1_source_current_descent", gate="J_H=q^*Jbar_H and vertical matter current zero", passed=False, claim_effect="source-current descent not promoted"),
        base_row(gate_id="CG2420_2_fixed_source_domain", gate="W_source/domain/linking surface fixed before readout", passed=False, claim_effect="domain-motion rows retained"),
        base_row(gate_id="CG2420_3_q_vertical", gate="q/v vertical generator proof", passed=False, claim_effect="Dq open-branch row retained"),
        base_row(gate_id="CG2420_4_no_pole_CR", gate="C_R/no-pole parent origin derived", passed=False, claim_effect="q_R/Q_R finite hair row retained"),
        base_row(gate_id="CG2420_5_R10_WEP_PPN", gate="local empirical branches score-ready", passed=False, claim_effect="no R10/WEP/PPN/clock/orbital claim"),
        base_row(gate_id="CG2420_6_local_GR_Newton", gate="local GR/Newton reduction derived", passed=False, claim_effect="no public local-GR claim"),
        base_row(gate_id="CG2420_7_GitHub", gate="public/GitHub update allowed", passed=False, claim_effect="private checkpoint only"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2420_0_result", decision="MINIMAL_PARENT_COUPLING_GATE_NOT_CLOSED", rationale="the action contract is clean but not derived from current MTS core and cannot compensate for open q/v verticality", consequence="source-current descent remains conditional"),
        base_row(decision_id="DEC2420_1_progress", decision="COUPLING_GAP_NOW_HAS_EXACT_CONTRACT", rationale="we know exactly what a parent action must sign: q-factorization, no source-only slot, variation-before-readout, fixed support/domain, boundary silence", consequence="this is a real narrowing, not a loop"),
        base_row(decision_id="DEC2420_2_best_route", decision="PSI_DETERMINANT_QUOTIENT_MAP_NEXT", rationale="ordinary current route left Q_R hair; psi quotient route is least circular way to make q/C_R absent, vertical, or stationary", consequence="target 2421"),
        base_row(decision_id="DEC2420_3_fallback", decision="FINITE_DOMAIN_MOTION_AND_QR_ROWS_IF_PROOF_FAILS", rationale="if the quotient theorem fails, the honest branch is sourced finite coefficients rather than closure axioms", consequence="keep residual stack source-ready but nonclaim"),
        base_row(decision_id="DEC2420_4_public_policy", decision="NO_GITHUB_NO_LOCAL_GR_CLAIM", rationale="local-GR/Newton still depends on unsigned parent coupling/q geometry", consequence="continue private derivation work"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(route_id="NEXT2420_0_selected", selection_status="selected", target_file="2421-Y5-R2FR-psi-determinant-quotient-map-or-finite-qR-coefficients.md", target_script="scripts/Y5_R2FR_psi_determinant_quotient_map_or_finite_qR_coefficients_2421.py", objective="construct the psi determinant/quotient map that makes q/C_R absent, vertical, or stationary before matter/readout; otherwise source finite q_R coefficients", success_condition="Dq[v]=0 or q_R/Q_R hair is zero by parent geometry, not closure axiom; if not, finite coefficients are explicit nonclaim rows", do_not_do="do not declare q vertical by label, normalize C_R by boundary choice, or import GR exterior equations as proof"),
        base_row(route_id="NEXT2420_1_parallel", selection_status="held_parallel", target_file="2421b-Y5-R2FR-topological-PiW-representative-or-projector-stress-bound.md", target_script="scripts/Y5_R2FR_topological_PiW_representative_or_projector_stress_bound_2421b.py", objective="prove Pi_W is fixed topological chain-map representative or source projector-stress rows", success_condition="[d,Pi_W]J_H=0 and delta Pi_W=0 are signed, or projector-stress components are bounded", do_not_do="do not treat Hodge/domain projectors as topological without parent proof"),
    ]


def copy_branch_rows(gate: list[dict[str, Any]], residuals: list[dict[str, Any]], decision: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["coupling_gate"], BRANCH_COPIES["queue"], gate),
        ("branch_wep", OUTPUTS["residual_stack"], BRANCH_COPIES["branch_wep"], residuals),
        ("beta_docs", OUTPUTS["decision"], BRANCH_COPIES["beta_docs"], decision),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, source_rows in copy_specs:
        write_csv(target_path, source_rows)
        parse_ok, row_count, parse_detail = csv_rows_parse(target_path)
        rows.append(base_row(copy_id=copy_id, source_path=str(source_path), target_path=str(target_path), copied=target_path.exists(), parse_ok=parse_ok, row_count=row_count, parse_detail=parse_detail))
    return rows


def all_generated_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, value in data.items():
        if key != "validation":
            rows.extend(value)
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources = data["source_register"]
    rows.append(base_row(validation_id="VAL2420_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['path_exists'])}/{len(sources)} sources exist"))
    rows.append(base_row(validation_id="VAL2420_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['needles_found'])}/{len(sources)} source needle sets found"))

    coupling_text = " ".join(str(row) for row in data["coupling_gate"])
    rows.append(base_row(validation_id="VAL2420_02_contract_written", status="PASS" if "S_matter = Sbar_matter" in coupling_text and "no independent source-only geometry slot" in coupling_text else "FAIL", detail="minimal parent coupling contract recorded"))
    rows.append(base_row(validation_id="VAL2420_03_not_promoted", status="PASS" if "NOT_DERIVED_FROM_CURRENT_MTS_CORE" in coupling_text and "EXACT_CONDITIONAL_OUTPUT_NOT_ACTIVE" in coupling_text else "FAIL", detail="coupling remains conditional, not a claim"))

    activation = data["activation_matrix"]
    rows.append(base_row(validation_id="VAL2420_04_activation_blocked", status="PASS" if all(not bool(row["passed"]) for row in activation) else "FAIL", detail="all source-current descent activation antecedents remain unpassed"))

    q_text = " ".join(str(row) for row in data["q_route"])
    rows.append(base_row(validation_id="VAL2420_05_q_route_selected", status="PASS" if "SELECT_NEXT_ATTACK" in q_text and "COUPLING_CONTRACT_VALID_BUT_NOT_PARENT_DERIVED" in q_text else "FAIL", detail="psi determinant/quotient route selected after q/v and C_R failures"))

    residual_text = " ".join(str(row) for row in data["residual_stack"])
    required_residuals = ["epsilon_source_domain_motion_abs", "epsilon_chainmap_readout_abs", "epsilon_Dq_open_branch_abs", "q_R/Q_R", "M_H_ref"]
    rows.append(base_row(validation_id="VAL2420_06_residual_coverage", status="PASS" if all(term in residual_text for term in required_residuals) else "FAIL", detail="domain, chainmap, Dq, q_R hair, and M_H_ref residuals retained"))
    rows.append(base_row(validation_id="VAL2420_07_residuals_nonready", status="PASS" if all(not bool(row["score_ready"]) for row in data["residual_stack"]) else "FAIL", detail="residual stack remains non-score-ready"))

    rows.append(base_row(validation_id="VAL2420_08_claim_gates", status="PASS" if all(not bool(row["passed"]) for row in data["claim_gates"]) else "FAIL", detail="local-GR/Newton/R10/WEP/PPN/GitHub claims blocked"))
    rows.append(base_row(validation_id="VAL2420_09_next_target", status="PASS" if any(row["route_id"] == "NEXT2420_0_selected" and "psi-determinant" in row["target_file"] for row in data["next_target"]) else "FAIL", detail="2421 psi determinant quotient map selected"))

    parse_details: list[str] = []
    parse_ok_all = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parse_ok, row_count, detail = csv_rows_parse(path)
        parse_ok_all = parse_ok_all and parse_ok
        parse_details.append(f"{path.name}:{row_count}:{detail}")
    rows.append(base_row(validation_id="VAL2420_10_csv_parse", status="PASS" if parse_ok_all else "FAIL", detail="; ".join(parse_details)))

    branch_ok = all(row["copied"] and row["parse_ok"] for row in data["branch_copies"])
    rows.append(base_row(validation_id="VAL2420_11_branch_copies", status="PASS" if branch_ok else "FAIL", detail=";".join(str(row["target_path"]) for row in data["branch_copies"])))

    generated = all_generated_rows(data)
    no_claim_flags = all(str(row.get("valid_for_claim")).lower() == "false" and str(row.get("claim_allowed")).lower() == "false" for row in generated)
    rows.append(base_row(validation_id="VAL2420_12_no_claim_flags", status="PASS" if no_claim_flags else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    formalization_dirty = formalization_has_2420_artifacts()
    rows.append(base_row(validation_id="VAL2420_13_formalization_untouched_by_outputs", status="PASS" if not formalization_dirty else "FAIL", detail="script outputs stay inside post-checkpoint-work"))

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(base_row(validation_id="VAL2420_OVERALL", status="PASS" if overall else "FAIL", detail="2420 installs the minimal parent coupling gate as an exact nonclaim contract, keeps source-current descent/local-GR blocked, and selects psi determinant quotient proof next"))
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2420 — Minimal Parent Matter-Coupling Action Or Domain-Motion Input

## Result

The minimal parent matter-coupling action remains the cleanest route, but it is **not yet derived from current MTS core variables**.

The exact contract is now explicit: if matter couples only through a parent quotient `q(Phi)`, with no independent source-only slot, variation before readout, fixed reduced source support/domain, and boundary silence, then the desired source-current descent follows conditionally:

`delta_v S_matter = 0 mod Euler/gauge/proper-boundary` and `J_H = q^* Jbar_H`.

But this cannot be promoted because the upstream `q/v` verticality and no-pole/`C_R` origin route is still open.  The useful identity from 2361 is `C_R = 2 ln J_q`; ordinary current conservation still allows `Q_R` hair unless a parent no-charge/quotient theorem kills it.  So the next serious derivation target is the `psi` determinant/quotient map, not another current loop.

## Source Register

{md_table(data["source_register"], ["source_id", "path_exists", "needles_found", "role", "source_path"])}

## Minimal Parent Coupling Gate

{md_table(data["coupling_gate"], ["row_id", "clause", "formal_statement", "current_status", "missing_input", "valid_for_claim"])}

## Source-Current Descent Activation Matrix

{md_table(data["activation_matrix"], ["clause_id", "antecedent", "evidence_source", "evidence_status", "activates", "passed"])}

## Q / Verticality / No-Pole Route Ledger

{md_table(data["q_route"], ["route_id", "route", "source_checkpoint", "result", "effect_on_coupling"])}

## Residual Fallback Stack

{md_table(data["residual_stack"], ["row_id", "quantity", "formula", "status", "score_ready", "valid_for_claim"])}

## Claim Gates

{md_table(data["claim_gates"], ["gate_id", "gate", "passed", "claim_effect"])}

## Decision Ledger

{md_table(data["decision"], ["decision_id", "decision", "rationale", "consequence"])}

## Next Target

{md_table(data["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"])}

## Generated Files

{md_table([base_row(output_id=key, path=str(path), exists=path.exists()) for key, path in OUTPUTS.items()], ["output_id", "path", "exists"])}

## Branch Copies

{md_table(data["branch_copies"], ["copy_id", "copied", "parse_ok", "row_count", "target_path"])}

## Validation

{md_table(data["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Practical Status

- Coupling is now a precise parent-action contract, not a vague missing ingredient.
- The contract would be strong enough to feed the local-GR/Newton route if `q/v` verticality, fixed support/domain, and `M_H_ref` source normalization were parent-signed.
- Current status is still nonclaim: no R10, WEP, PPN, clock, orbital, local-GR, Newton, public, or GitHub claim is allowed from 2420.
- Best next attack: prove the `psi` determinant/quotient map that makes `q/C_R` absent, vertical, or stationary before matter/readout; if it fails, source finite `q_R`/domain-motion coefficients.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    remove_pycache()
    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "coupling_gate": coupling_gate_rows(),
        "activation_matrix": activation_matrix_rows(),
        "q_route": q_route_rows(),
        "residual_stack": residual_stack_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key, rows in data.items():
        write_csv(OUTPUTS[key], rows)

    data["branch_copies"] = copy_branch_rows(data["coupling_gate"], data["residual_stack"], data["decision"])
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    overall = next(row for row in data["validation"] if row["validation_id"] == "VAL2420_OVERALL")
    print(f"{overall['validation_id']},{overall['status']},{overall['detail']}")
    print(str(DOC))


if __name__ == "__main__":
    main()

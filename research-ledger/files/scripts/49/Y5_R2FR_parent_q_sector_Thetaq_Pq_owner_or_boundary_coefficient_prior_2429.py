from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_Q_SECTOR_THETAQ_PQ_OWNER_OR_BOUNDARY_COEFFICIENT_PRIOR_2429"
CHECKPOINT_ID = "2429"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2429-Y5-R2FR-parent-q-sector-Thetaq-Pq-owner-or-boundary-coefficient-prior.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2429_SOURCE_REGISTER.csv",
    "route_menu": OUT / "P8_Y5_PARENT_QLOC_2429_Q_PARENT_ROUTE_MENU.csv",
    "theta_template": OUT / "P8_Y5_PARENT_QLOC_2429_THETAQ_PQ_TEMPLATE_CONTRACT.csv",
    "owner_gate": OUT / "P8_Y5_PARENT_QLOC_2429_THETAQ_OWNER_GATE.csv",
    "nohair_firstclass": OUT / "P8_Y5_PARENT_QLOC_2429_NOHAIR_FIRSTCLASS_ROUTE_LEDGER.csv",
    "boundary_priors": OUT / "P8_Y5_PARENT_QLOC_2429_BOUNDARY_COEFFICIENT_PRIOR_TEMPLATE.csv",
    "selection": OUT / "P8_Y5_PARENT_QLOC_2429_ACTION_SELECTION_DECISION.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2429_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2429_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2429_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2429_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2429_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2429_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_prior": QUEUE / "JR2429_BOUNDARY_COEFFICIENT_PRIOR_NONCLAIM.csv",
    "queue_template": QUEUE / "JR2429_THETAQ_PQ_TEMPLATE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "Thetaq_Pq_owner_or_boundary_prior_nonclaim_2429.csv",
    "beta_docs": BETA_DOCS / "THETAQ_PQ_OWNER_OR_BOUNDARY_PRIOR_2429_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2429_00_2428_handoff",
        "source_path": ROOT / "2428-Y5-R2FR-parent-boundary-charge-formula-Bq-or-alpha3-projection-bound.md",
        "needles": ["NEXT2428_0_selected", "BQF2428_4_verdict", "VAL2428_OVERALL"],
        "role": "current handoff selecting q-sector Theta_q/P_q ownership",
    },
    {
        "source_id": "SRC2429_01_2428_validation",
        "source_path": OUT / "P8_Y5_BRR545_2428_VALIDATION.csv",
        "needles": ["VAL2428_OVERALL", "PASS"],
        "role": "confirms 2428 passed before 2429",
    },
    {
        "source_id": "SRC2429_02_2428_formula",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2428_PARENT_BOUNDARY_CHARGE_FORMULA.csv",
        "needles": ["BQF2428_2_candidate_Qq", "CONTRACT_READY_NOT_PARENT_SIGNED"],
        "role": "B_q/Q_q formula requires Theta_q/P_q",
    },
    {
        "source_id": "SRC2429_03_2428_owner",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2428_BQ_OWNER_GATE.csv",
        "needles": ["BQG2428_5_verdict", "FAIL_CURRENT_CLAIM_BQ_NOT_PARENT_OWNED"],
        "role": "B_q owner gates blocked safely",
    },
    {
        "source_id": "SRC2429_04_2428_alpha3",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2428_ALPHA3_PROJECTION_COEFFICIENT_TEMPLATE.csv",
        "needles": ["A3P2428_0_formula", "4e-20"],
        "role": "alpha3 coefficient rule input",
    },
    {
        "source_id": "SRC2429_05_2295_precedent",
        "source_path": ROOT / "2295-Y5-R2FR-parent-q-sector-Thetaq-Pq-owner-or-boundary-coefficient-prior.md",
        "needles": ["TPQ2295_5_verdict", "TOG2295_5_verdict", "VAL2295_OVERALL"],
        "role": "prior Theta_q/P_q owner checkpoint",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


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
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                source_path=path,
                path_exists=path.exists(),
                required_needles="; ".join(needles),
                found_needles="; ".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=source["role"],
            )
        )
    return rows


def route_menu_rows() -> list[dict[str, Any]]:
    return [
        base_row(route_id="QC2429_0_absent_quotient", route="q is not a primitive parent field", theta_pq_status="Theta_q=0 and P_q=0 if q is absent before variation", boundary_effect="B_q=0 if quotient/nonprimitive q is parent-proved before variation", missing_for_claim="prove q is coordinate/readout artefact before variation, not deleted after local tests", priority=1, current_status="BEST_THEOREM_ROUTE_NOT_PARENT_SIGNED"),
        base_row(route_id="QC2429_1_first_class_vertical_constraint", route="q is a first-class vertical gauge/constraint direction", theta_pq_status="Theta_q exists on parent fields and Omega-flat(v_q)=delta C_q; P_q is owned by momentum-map constraint", boundary_effect="B_q/Q_q vanish only for proper compact transformations unless Q_q exact/proper and K_boundary=0 are proved", missing_for_claim="parent Omega, D C_q, all-field v_q, bracket closure, degree count, and matter descent", priority=2, current_status="BEST_ACTIVE_ROUTE_BUT_INCOMPLETE"),
        base_row(route_id="QC2429_2_positive_sourcefree_physical_q", route="q is physical positive operator but source-free locally", theta_pq_status="for first-derivative quadratic sector, Theta_q^mu=Z_q nabla^mu q delta q plus mixing/projector terms", boundary_effect="B_q and Phi_boundary vanish only if J_q=0 and boundary flux=0/no-hair are parent-proved", missing_for_claim="Z_q/M_q^2 signs, source-zero, boundary-flux zero, topology and projector mixing", priority=3, current_status="VIABLE_NOHAIR_ROUTE_INPUTS_MISSING"),
        base_row(route_id="QC2429_3_sourced_residual", route="q is a physical sourced residual field", theta_pq_status="Theta_q/P_q are standard once L_q is chosen, but branch must be empirically scored", boundary_effect="alpha(lambda), alpha3, PPN, WEP, clock, and orbital coefficient rows become live", missing_for_claim="not a GR derivation by itself; becomes testable residual framework", priority=4, current_status="EMPIRICAL_FALLBACK_ONLY"),
        base_row(route_id="QC2429_4_universal_frame_marker", route="matter sees q-dependent Weyl/disformal/readout frame", theta_pq_status="standard finite-sector Theta_q if q has kinetic block", boundary_effect="source/test coupling is product-like unless one leg is explicitly inside Qbar", missing_for_claim="creates fifth-force/clock/WEP countermodel unless marker theorem-zero closes", priority=5, current_status="COUNTERMODEL_NOT_SOLUTION"),
    ]


def theta_template_rows() -> list[dict[str, Any]]:
    return [
        base_row(template_id="TPQ2429_0_general_variation", object="finite-order parent q sector", formula="delta L_q=E_A delta Y_q^A+nabla_mu Theta_q^mu(delta Y_q)", owned_if="L_q is selected with field normalization, derivative order, density convention, and boundary class", current_status="GENERAL_TEMPLATE_DERIVED_NOT_PARENT_SELECTED", claim_effect="defines upstream object needed for Q_q, B_q, K_boundary and no-hair identities", score_ready=False),
        base_row(template_id="TPQ2429_1_first_derivative", object="first-derivative template", formula="Theta_q^mu(delta Y)=Pi_A^mu delta Y^A, Pi_A^mu:=partial L_q/partial(nabla_mu Y^A)", owned_if="L_q has no higher derivatives or higher-derivative boundary terms have been reduced by auxiliary fields", current_status="FORMULA_READY_LQ_MISSING", claim_effect="turns a chosen L_q into a computable symplectic potential", score_ready=False),
        base_row(template_id="TPQ2429_2_finite_jet", object="higher finite-jet template", formula="Theta_q^mu=sum_{r=0}^{N-1} Pi_A^{mu alpha_1...alpha_r} nabla_{alpha_1}...nabla_{alpha_r} delta Y^A", owned_if="finite derivative order N and corner/counterterm conventions are declared", current_status="FORMULA_READY_FINITE_JET_ORDER_MISSING", claim_effect="fixes which epsilon_q jets must vanish for proper boundary silence", score_ready=False),
        base_row(template_id="TPQ2429_3_Noether_Pq", object="P_q from vertical generator", formula="insert delta_epsilon Y^A=R^A_q epsilon_q+R^{A mu}_q nabla_mu epsilon_q+... into Theta_q; P_q^mu is the package whose divergence enters C_q", owned_if="v_q action on every parent field and tensor/density convention for C_q are fixed", current_status="CONTRACT_READY_FIELD_ACTION_AND_CONVENTION_MISSING", claim_effect="connects Theta_q to B_q=sigma n_mu P_q^mu+...", score_ready=False),
        base_row(template_id="TPQ2429_4_positive_q_example", object="minimal positive scalar-like q residual example", formula="L_q=-1/2 Z_q nabla_mu q nabla^mu q -1/2 M_q^2 q^2 + J_q q gives Theta_q^mu=-Z_q nabla^mu q delta q", owned_if="q is retained amplitude, Z_q>0, M_q^2>0, J_q and boundary data are source-owned", current_status="EXAMPLE_ONLY_NOT_SELECTED", claim_effect="if J_q=0 and boundary flux=0, no-hair can set q=0; otherwise alpha(lambda) is live", score_ready=False),
        base_row(template_id="TPQ2429_5_verdict", object="Theta_q/P_q owner status", formula="Theta_q/P_q template is mathematically ready, but no parent q block is selected or proved", owned_if="one candidate in QC2429 closes its owner gates", current_status="FAIL_CURRENT_CLAIM_THETAQ_PQ_NOT_PARENT_OWNED", claim_effect="use nonclaim priors/templates for boundary coefficients until parent block is signed", score_ready=False),
    ]


def owner_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="TOG2429_0_parent_route", needed="select one parent q route", test="absent quotient, first-class vertical constraint, positive sourcefree field, or sourced residual is chosen before scoring", current_status="ROUTE_NOT_PARENT_SELECTED", if_missing="Theta_q/P_q remain a menu rather than an action"),
        base_row(gate_id="TOG2429_1_field_content", needed="field list and transformation law", test="Y_q^A and delta_epsilon Y_q^A are declared for metric/coframe, q, extra modes, domain/memory, matter, and boundary fields", current_status="FIELD_ACTION_INCOMPLETE", if_missing="P_q cannot be computed from Theta_q"),
        base_row(gate_id="TOG2429_2_operator_signs", needed="positive/no-pole or residual operator", test="Z_q, M_q^2, kinetic sign, projector mixing, and Hessian positivity are parent-owned", current_status="OPERATOR_SIGNS_MISSING", if_missing="local-GR reduction cannot tell no-hair from hidden dynamics"),
        base_row(gate_id="TOG2429_3_source_zero", needed="source-zero or sourced residual split", test="J_q=0 theorem or explicit source beta rows are selected", current_status="SOURCE_ZERO_OR_BETA_SPLIT_MISSING", if_missing="source leakage regenerates q even if boundary is controlled"),
        base_row(gate_id="TOG2429_4_boundary_flux", needed="boundary no-flux or coefficient row", test="Phi_boundary_local_q=0 theorem or alpha3/R10 boundary coefficients are source-backed", current_status="BOUNDARY_FLUX_ZERO_OR_BOUND_MISSING", if_missing="K_boundary_alpha3_q and edge R10 templates remain nonclaim"),
        base_row(gate_id="TOG2429_5_verdict", needed="claim-grade Theta_q/P_q owner", test="TOG2429_0 through TOG2429_4 pass together", current_status="FAIL_CURRENT_CLAIM_THETAQ_PQ_OWNER_MISSING", if_missing="demote to nonclaim coefficient priors/templates"),
    ]


def nohair_firstclass_rows() -> list[dict[str, Any]]:
    return [
        base_row(route_id="NFR2429_0_positive_energy", route="positive source-free operator", identity="integral[Z_q |nabla q|^2 + M_q^2 q^2] + Phi_boundary_local_q = integral q J_q", success_condition="Z_q>0, M_q^2>0, J_q=0, Phi_boundary_local_q=0 and topology/projector caveats closed", current_status="PROMISING_NOT_PARENT_SIGNED"),
        base_row(route_id="NFR2429_1_first_class", route="first-class momentum-map owner", identity="i_{v_q} Omega = delta C_q with differentiable G_q and proper boundary charge", success_condition="Omega/DCq/v_q/bracket/degree-count/matter descent close together", current_status="BEST_STRUCTURAL_ZERO_ROUTE_INCOMPLETE"),
        base_row(route_id="NFR2429_2_absent_quotient", route="q absent before variation", identity="no independent q slot, so Theta_q=P_q=B_q=0", success_condition="parent quotient map and object language exclude q before variation without circular GR import", current_status="BEST_CLEAN_ROUTE_NOT_DERIVED"),
        base_row(route_id="NFR2429_3_sourced_residual", route="finite residual fallback", identity="q solves sourced operator and is bounded by alpha3/R10/PPN/WEP/clock/orbital rows", success_condition="coefficient rows become source-backed and no-cancellation tails active", current_status="EMPIRICAL_FALLBACK_NOT_GR_DERIVATION"),
    ]


def boundary_prior_rows() -> list[dict[str, Any]]:
    return [
        base_row(prior_id="BCP2429_0_K_boundary_alpha3_q", coefficient="K_boundary_alpha3_q", arena="alpha3", bound_rule="if Phi_boundary_local_q is sourced and nonzero, |K_boundary_alpha3_q| <= 4e-20/|Phi_boundary_local_q|", bound_source="4e-20", missing_inputs="Phi_boundary_local_q numeric/source-backed or theorem-zero; normalization; uncertainty policy", current_status="NONCLAIM_PRIOR_SCHEMA_READY_INPUTS_MISSING", score_ready=False),
        base_row(prior_id="BCP2429_1_Phi_boundary_local_q", coefficient="Phi_boundary_local_q", arena="alpha3;R10;orbital", bound_rule="Phi_boundary_local_q=0 by no-flux theorem, or numeric amplitude with units and source path", bound_source="theorem_zero_or_numeric", missing_inputs="boundary norm, surface, units, time/source normalization, topology/corner policy", current_status="NONCLAIM_PRIOR_SCHEMA_READY_INPUTS_MISSING", score_ready=False),
        base_row(prior_id="BCP2429_2_edge_R10_coefficients_q", coefficient="K_edge_q;Qbar_edge_qH;qbar_qT", arena="alpha_R10(lambda)", bound_rule="|alpha_edge_q|=|K_edge_q Qbar_edge_qH qbar_qT| must be <= alpha_bound(lambda) after curve promotion", bound_source="review-candidate alpha_bound(lambda) only", missing_inputs="K_edge_q(lambda), Qbar_edge_qH(lambda), qbar_qT, lambda support, promoted bound curve", current_status="NONCLAIM_PRIOR_SCHEMA_READY_INPUTS_MISSING", score_ready=False),
    ]


def selection_rows() -> list[dict[str, Any]]:
    return [
        base_row(selection_id="SEL2429_0_do_not_select_yet", decision="Do not select a public parent q action at 2429.", reason="candidate routes exist but no source file proves the required L_q/Theta_q/P_q package", next_action="use templates as contracts for next derivation step"),
        base_row(selection_id="SEL2429_1_best_derivation_next", decision="Best derivation route is quotient/first-class first, positive no-hair second.", reason="these routes can reduce to local GR rather than merely survive empirical bounds", next_action="try source-free positive q no-hair or first-class momentum-map owner before coefficient priors"),
        base_row(selection_id="SEL2429_2_fallback_prior", decision="If owner route stalls, use alpha3/R10 coefficient priors as private diagnostics.", reason="inequalities are known but numeric K/Phi/Qbar values would be invented today", next_action="nonclaim rows only"),
    ]


def refusal_rows(groups: list[list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in groups:
        for row in group:
            ident = row.get("template_id") or row.get("gate_id") or row.get("route_id") or row.get("prior_id") or row.get("selection_id")
            attempted = row.get("object") or row.get("needed") or row.get("route") or row.get("coefficient") or row.get("decision") or ident
            result = row.get("current_status") or "NONCLAIM"
            reason = row.get("owned_if") or row.get("if_missing") or row.get("success_condition") or row.get("missing_inputs") or row.get("reason") or "VALID_FOR_CLAIM_FALSE"
            rows.append(base_row(refusal_id=f"REF2429_{ident}", attempted_claim=attempted, result=result, reason=f"{reason}; VALID_FOR_CLAIM_FALSE", score_ready=False))
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(claim_id="CGATE2429_0_parent_q_owner", claim="parent q-sector action owns Theta_q/P_q", gate_pass=False, reason="candidate routes are ranked and templates written, but no L_q/field-content/operator/source/boundary package is parent-selected"),
        base_row(claim_id="CGATE2429_1_local_GR_no_pole", claim="q is absent/gauge/sourcefree enough to reduce locally to GR/Newton", gate_pass=False, reason="absent quotient, first-class constraint, or positive no-hair route is not closed"),
        base_row(claim_id="CGATE2429_2_alpha3_prior", claim="alpha3 q coefficient prior is executable", gate_pass=False, reason="K_boundary_alpha3_q and Phi_boundary_local_q remain missing"),
        base_row(claim_id="CGATE2429_3_R10_prior", claim="R10 q edge coefficient prior is executable", gate_pass=False, reason="K_edge_q, Qbar_edge_qH, qbar_qT, lambda support, and promoted bound curve remain incomplete"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2429_0_parent_route_status", decision="DO_NOT_PRETEND_PARENT_Q_ACTION_IS_SELECTED", rationale="generic Theta_q/P_q machinery is derived, but no source proves any candidate route", consequence="attack absent/quotient, first-class, or positive/nohair source-zero route directly"),
        base_row(decision_id="DEC2429_1_best_route", decision="QUOTIENT_FIRSTCLASS_FIRST_POSITIVE_NOHAIR_SECOND", rationale="quotient/constraint gives true no-pole if it closes; positive no-hair can derive local silence; sourced residual is testable but not GR reduction", consequence="try no-hair/first-class owner before coefficient priors"),
        base_row(decision_id="DEC2429_2_next_target", decision="SOURCEFREE_POSITIVE_NOHAIR_OR_FIRSTCLASS_OWNER_GATE_NEXT", rationale="most concrete route converting Theta_q/P_q templates into local-GR reduction without inventing coefficients", consequence="2430 q sourcefree positive nohair or firstclass owner gate"),
        base_row(decision_id="DEC2429_3_claim_policy", decision="KEEP_PRIVATE_NONCLAIM", rationale="no parent q action or executable coefficient prior exists", consequence="no GitHub action"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2429_0_selected",
            selection_status="selected",
            target_file="2430-Y5-R2FR-q-sourcefree-positive-nohair-or-firstclass-owner-gate.md",
            target_script="scripts/Y5_R2FR_q_sourcefree_positive_nohair_or_firstclass_owner_gate_2430.py",
            objective="try to derive the source-free positive q-sector no-hair identity with Z_q>0, M_q^2>0, J_q=0, and Phi_boundary_local_q=0, while testing the first-class constraint alternative; if both fail, fill the first nonclaim alpha3/R10 prior row",
            success_condition="positive no-hair identity or first-class momentum-map owner closes, or coefficient-prior rows remain explicit nonclaim templates",
            do_not_do="do not invent Z/M/J/K/Phi/Qbar values, delete GR charges, score naked linear c_g, cancel residuals, claim R10/local-GR pass, edit formalization-workbench, or push GitHub",
        )
    ]


def copy_branch_rows(priors: list[dict[str, Any]], templates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue_prior", OUTPUTS["boundary_priors"], COPY_TARGETS["queue_prior"], priors),
        ("queue_template", OUTPUTS["theta_template"], COPY_TARGETS["queue_template"], templates),
        ("branch_wep", OUTPUTS["boundary_priors"], COPY_TARGETS["branch_wep"], priors),
        ("beta_docs", OUTPUTS["boundary_priors"], COPY_TARGETS["beta_docs"], priors),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, copied_rows in copy_specs:
        write_csv(target_path, copied_rows)
        rows.append(
            base_row(
                copy_id=f"BC2429_{copy_id}",
                source_path=source_path,
                target_path=target_path,
                target_exists=target_path.exists(),
                row_count=len(copied_rows),
                purpose="Theta_q/P_q owner or boundary coefficient prior nonclaim copy",
            )
        )
    return rows


def formalization_has_2429_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2429-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2429*",
        "*P8_Y5_BRR545_2429*",
        "*Y5_R2FR_parent_q_sector_Thetaq_Pq_owner_or_boundary_coefficient_prior_2429*",
        "*JR2429*",
        "*THETAQ_PQ_OWNER_OR_BOUNDARY_PRIOR_2429*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def flags_safe(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "gate_pass"):
                value = row.get(key)
                if value is True or stringify(value).lower() == "true":
                    return False
    return True


def build_validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    templates = rows_by_name["theta_template"]
    owner = rows_by_name["owner_gate"]
    priors = rows_by_name["boundary_priors"]
    selection = rows_by_name["selection"]
    next_rows = rows_by_name["next_target"]

    csv_results = []
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        parses, row_count, message = csv_parses(path)
        csv_results.append((name, parses, row_count, message))
    for copy_key, copy_path in COPY_TARGETS.items():
        parses, row_count, message = csv_parses(copy_path)
        csv_results.append((f"copy_{copy_key}", parses, row_count, message))

    checks = [
        ("VAL2429_SOURCES_EXIST", all(row["path_exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL2429_NEEDLES_FOUND", all(row["needles_found"] for row in source_rows), "all source needles found"),
        ("VAL2429_THETA_TEMPLATE", any(row["template_id"] == "TPQ2429_5_verdict" and "NOT_PARENT_OWNED" in row["current_status"] for row in templates), "Theta_q/P_q template written and not parent-promoted"),
        ("VAL2429_OWNER_GATES", any(row["gate_id"] == "TOG2429_5_verdict" and "OWNER_MISSING" in row["current_status"] for row in owner), "owner gates identify missing route and field/action package"),
        ("VAL2429_PRIORS_NONCLAIM", all(not row["score_ready"] for row in priors), "alpha3/R10 coefficient priors remain nonclaim"),
        ("VAL2429_NO_ACTION_SELECTION", any(row["selection_id"] == "SEL2429_0_do_not_select_yet" for row in selection), "no public parent q action selected"),
        ("VAL2429_NEXT_SELECTED", any(row["route_id"] == "NEXT2429_0_selected" and "sourcefree-positive-nohair" in row["target_file"] for row in next_rows), "no-hair/first-class owner selected next"),
        ("VAL2429_FLAGS_SAFE", flags_safe(rows_by_name), "no claim/score flags are true"),
        ("VAL2429_BRANCH_COPIES", all(row["target_exists"] for row in branch_copy_rows), "branch copy files written"),
        ("VAL2429_CSV_PARSE", all(item[1] and item[2] > 0 for item in csv_results), "all generated CSV and branch copies parse with rows"),
        ("VAL2429_NO_FORMALIZATION_OUTPUT", not formalization_has_2429_artifacts(), "no 2429 artifacts written into formalization-workbench"),
    ]

    rows = [
        base_row(validation_id=validation_id, status="PASS" if passed else "FAIL", detail=detail, fatal=not passed)
        for validation_id, passed, detail in checks
    ]
    overall_passed = all(row["status"] == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2429_OVERALL",
            status="PASS" if overall_passed else "FAIL",
            detail="2429 ranks q parent routes, writes Theta_q/P_q templates, refuses action selection, keeps coefficient priors nonclaim, and selects q no-hair/first-class owner gate next",
            fatal=not overall_passed,
        )
    )
    return rows


def write_document(rows_by_name: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> None:
    content = f"""# 2429 Y5 R2FR Parent q-Sector Thetaq/Pq Owner Or Boundary Coefficient Prior

## Result

2429 makes the parent-action menu explicit for the q boundary sector: `Theta_q` and `P_q` can be computed once a lawful `L_q` or constraint route is selected.

No parent `L_q`, `Theta_q`, or `P_q` owner is selected here. The templates are contracts, not claims. The action-selection fork is now explicit: quotient/first-class first, positive source-free no-hair second, empirical residual last. Alpha3/R10 coefficient priors remain private nonclaim scaffolding.

## Practical Status

- **Useful:** `Theta_q/P_q` machinery is written at the level of variational templates.
- **Blocked:** no parent q action/constraint route is selected.
- **Best route:** quotient/first-class no-pole first; positive no-hair second.
- **Fallback:** alpha3/R10 coefficient priors stay nonclaim.
- **Next target:** source-free positive no-hair or first-class owner gate.

## Source Register

{table(["source_id", "source_path", "path_exists", "needles_found", "role"], rows_by_name["source_register"])}

## q Parent Route Menu

{table(["route_id", "route", "theta_pq_status", "boundary_effect", "missing_for_claim", "priority", "current_status"], rows_by_name["route_menu"])}

## Thetaq/Pq Template Contract

{table(["template_id", "object", "formula", "owned_if", "current_status", "claim_effect", "score_ready"], rows_by_name["theta_template"])}

## Thetaq Owner Gate

{table(["gate_id", "needed", "test", "current_status", "if_missing"], rows_by_name["owner_gate"])}

## Nohair/First-Class Route Ledger

{table(["route_id", "route", "identity", "success_condition", "current_status"], rows_by_name["nohair_firstclass"])}

## Boundary Coefficient Prior Template

{table(["prior_id", "coefficient", "arena", "bound_rule", "bound_source", "missing_inputs", "current_status", "score_ready"], rows_by_name["boundary_priors"])}

## Action Selection Decision

{table(["selection_id", "decision", "reason", "next_action"], rows_by_name["selection"])}

## Refusal Runner

{table(["refusal_id", "attempted_claim", "result", "reason", "score_ready"], rows_by_name["refusal"])}

## Claim Gates

{table(["claim_id", "claim", "gate_pass", "reason"], rows_by_name["claim_gates"])}

## Decision Ledger

{table(["decision_id", "decision", "rationale", "consequence"], rows_by_name["decision"])}

## Next Target

{table(["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"], rows_by_name["next_target"])}

## Validation

{table(["validation_id", "status", "detail", "fatal"], validation_rows)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    templates = theta_template_rows()
    priors = boundary_prior_rows()
    rows_by_name = {
        "source_register": source_register_rows(),
        "route_menu": route_menu_rows(),
        "theta_template": templates,
        "owner_gate": owner_gate_rows(),
        "nohair_firstclass": nohair_firstclass_rows(),
        "boundary_priors": priors,
        "selection": selection_rows(),
        "refusal": refusal_rows([templates, owner_gate_rows(), nohair_firstclass_rows(), priors, selection_rows()]),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    branch_copy_rows = copy_branch_rows(priors, templates)
    rows_by_name["branch_copies"] = branch_copy_rows
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows)

    validation_rows = build_validation_rows(rows_by_name, branch_copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_document(rows_by_name, validation_rows)
    remove_pycache()

    overall = next(row for row in validation_rows if row["validation_id"] == "VAL2429_OVERALL")
    print(f"{DOC}")
    print(f"{OUTPUTS['validation']}")
    print(f"VAL2429_OVERALL={overall['status']}")


if __name__ == "__main__":
    main()

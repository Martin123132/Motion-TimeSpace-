from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_JQ_SOURCE_LEG_ZERO_THEOREM_OR_COMPONENT_BOUND_VECTOR_2431"
CHECKPOINT_ID = "2431"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2431-Y5-R2FR-Jq-source-leg-zero-theorem-or-component-bound-vector.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2431_SOURCE_REGISTER.csv",
    "descent_theorem": OUT / "P8_Y5_PARENT_QLOC_2431_JQ_DESCENT_ZERO_THEOREM.csv",
    "component_vector": OUT / "P8_Y5_PARENT_QLOC_2431_JQ_COMPONENT_BOUND_VECTOR.csv",
    "bound_law": OUT / "P8_Y5_PARENT_QLOC_2431_JQ_TO_Q_RESIDUAL_BOUND_LAW.csv",
    "arena_impact": OUT / "P8_Y5_PARENT_QLOC_2431_LOCAL_ARENA_IMPACT_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2431_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2431_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2431_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2431_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2431_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_component_vector": QUEUE / "JR2431_JQ_COMPONENT_BOUND_VECTOR_NONCLAIM.csv",
    "queue_descent": QUEUE / "JR2431_JQ_DESCENT_ZERO_THEOREM_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "Jq_component_bound_vector_nonclaim_2431.csv",
    "beta_docs": BETA_DOCS / "JQ_SOURCE_LEG_COMPONENT_VECTOR_2431_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2431_00_2430_handoff",
        "source_path": ROOT / "2430-Y5-R2FR-q-sourcefree-positive-nohair-or-firstclass-owner-gate.md",
        "needles": ["NEXT2430_0_selected", "JQ2430_7_total_verdict", "VAL2430_OVERALL"],
        "role": "fresh handoff selecting J_q source-leg zero theorem or component-bound vector",
    },
    {
        "source_id": "SRC2431_01_2430_validation",
        "source_path": OUT / "P8_Y5_BRR545_2430_VALIDATION.csv",
        "needles": ["VAL2430_OVERALL", "PASS"],
        "role": "confirms 2430 passed before 2431",
    },
    {
        "source_id": "SRC2431_02_2430_jq_audit",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2430_JQ_SOURCE_CHANNEL_ZERO_AUDIT.csv",
        "needles": ["JQ2430_7_total_verdict", "JQ_TOTAL_ZERO_NOT_PROVED"],
        "role": "current J_q source channels",
    },
    {
        "source_id": "SRC2431_03_2430_residual_bound",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2430_FINITE_Q_RESIDUAL_BOUND_LAW.csv",
        "needles": ["QRB2430_1_norm_bound", "NO_CANCELLATION_BOUND_READY"],
        "role": "finite q residual bound law if J_q survives",
    },
    {
        "source_id": "SRC2431_04_2425_product_law",
        "source_path": ROOT / "2425-Y5-R2FR-parent-finite-quadratic-q-row-and-source-test-coupling-split.md",
        "needles": ["LAW2425_2_R10_alpha_match", "LAW2425_3_common_Weyl_cg"],
        "role": "source/test product law and c_g squared guard",
    },
    {
        "source_id": "SRC2431_05_2297_precedent",
        "source_path": ROOT / "2297-Y5-R2FR-Jq-source-zero-or-component-bound-pack.md",
        "needles": ["JZT2297_1_ordinary_matter_chain_rule", "JZT2297_4_verdict"],
        "role": "older q-sector J_q zero/component-bound precedent",
    },
    {
        "source_id": "SRC2431_06_2367_precedent",
        "source_path": ROOT / "2367-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack.md",
        "needles": ["JQZ2367_1_matter_descent", "JQPACK2367_9_claim_gate"],
        "role": "later j_q numerator/source-pack precedent",
    },
    {
        "source_id": "SRC2431_07_2317_hidden_visible",
        "source_path": ROOT / "2317-Y5-R2FR-no-hidden-visible-hom-jq-zero-or-finite-coefficient-prior.md",
        "needles": ["VAL2317_OVERALL", "finite coupling prior interface"],
        "role": "hidden-visible coefficient leakage countermodel/functor precedent",
    },
    {
        "source_id": "SRC2431_08_2428_boundary",
        "source_path": ROOT / "2428-Y5-R2FR-parent-boundary-charge-formula-Bq-or-alpha3-projection-bound.md",
        "needles": ["BQF2428_2_candidate_Qq", "A3P2428_0_formula"],
        "role": "boundary charge and alpha3 projection interface",
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


def descent_theorem_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            theorem_id="JZT2431_0_definition",
            target="J_q source functional",
            statement="For the positive-q branch, the source leg is the vertical variation coefficient J_q[eta] := delta_eta S_nonq evaluated along the q direction and projected onto the q equation.",
            result="DEFINITION_SHARPENED",
            missing_for_claim="parent q normalization, variation domain, and projection convention",
            theorem_zero=False,
        ),
        base_row(
            theorem_id="JZT2431_1_descent_lemma",
            target="exact chain-rule zero",
            statement="If every non-q sector functional F_i satisfies F_i[Phi,psi]=Fbar_i[Obs(Phi),psi] and v_q is in ker(D Obs), then delta_vq F_i=0 and that sector contributes zero to J_q.",
            result="EXACT_CONDITIONAL_THEOREM",
            missing_for_claim="parent observed-object functor and all-field vertical generator",
            theorem_zero=False,
        ),
        base_row(
            theorem_id="JZT2431_2_bulk_matter_subcase",
            target="ordinary matter bulk",
            statement="Ordinary bulk matter is theorem-zero only in the same branch where masses, EM constants, clocks, source weights, and observed coframe all descend through q-blind observables.",
            result="MATHEMATICALLY_CLEAN_PARENT_UNSIGNED",
            missing_for_claim="minimal ordinary-matter signature for q plus no-marker constants",
            theorem_zero=False,
        ),
        base_row(
            theorem_id="JZT2431_3_body_worldtube_guard",
            target="source body/interior matching",
            statement="Even if bulk exterior J_q vanishes, a body/source-worldtube charge or boundary condition can source the exterior q profile through matching.",
            result="EXTERIOR_ZERO_INSUFFICIENT",
            missing_for_claim="Q_q[body]=0 theorem or source-backed body charge bound",
            theorem_zero=False,
        ),
        base_row(
            theorem_id="JZT2431_4_no_hidden_visible_Hom",
            target="visible coefficient leakage",
            statement="A global J_q=0 theorem needs no hidden-to-visible coefficient/readout map: Hom(hidden invariants, visible constants/frames/readouts)=0 or quotient-constant.",
            result="BEST_DERIVATION_ROUTE_IDENTIFIED",
            missing_for_claim="parent coefficient functor/target category and radiative/readout closure",
            theorem_zero=False,
        ),
        base_row(
            theorem_id="JZT2431_5_total_verdict",
            target="J_q=0",
            statement="J_q=0 is not proved by the current corpus; the exact descent theorem is available only as a parent contract, so finite component bounds remain mandatory.",
            result="JQ_ZERO_NOT_PROMOTED_COMPONENT_VECTOR_REQUIRED",
            missing_for_claim="all component zero clauses or source-backed absolute bounds",
            theorem_zero=False,
        ),
    ]


def component_vector_rows() -> list[dict[str, Any]]:
    rows = [
        ("JQC2431_0_bulk_matter", "J_q^matter_bulk", "ordinary matter vertical source", "zero if matter action descends through q-blind observed geometry and q-blind constants", "B_matter_q", "action_density_or_dual_Hminus1", "PPN;WEP;clock;R10", "CONDITIONAL_ZERO_NOT_PROMOTED"),
        ("JQC2431_1_universal_frame", "J_q^frame", "common Weyl/disformal observed-frame source", "zero if observed frame maps are quotient-pure and have no q derivative", "B_frame_q", "dual_Hminus1", "R10;PPN;WEP;clock", "OPEN_CG_SQUARED_IF_FINITE"),
        ("JQC2431_2_material_marker", "J_q^marker", "EM/material constants and composition markers", "zero if alpha_EM, mass ratios, nuclear/transition coefficients are q-blind superselection/readout data", "B_marker_q", "dual_Hminus1", "EM;clock;WEP;particle", "OPEN_NO_HIDDEN_VISIBLE_HOM_MISSING"),
        ("JQC2431_3_body_worldtube", "J_q^body", "source interior/worldtube matching charge", "zero if Q_q[body]=0 or matching data are q-orthogonal", "B_body_q", "charge_or_boundary_dual", "R10;orbital;Newton;PPN", "OPEN_BODY_CHARGE_NOT_ZERO"),
        ("JQC2431_4_boundary_reference", "J_q^boundary", "boundary/reference/counterterm flux", "zero if B_q/Q_q and reference terms are exact/proper-zero in the physical source boundary class", "B_boundary_q", "boundary_dual", "alpha3;R10;orbital", "OPEN_SOURCE_BOUNDARY_NOT_COMPACT_PROPER"),
        ("JQC2431_5_projector_domain", "J_q^projector", "domain/projector/readout selection source", "zero if domain/projector maps are fixed before variation or descend through q-blind observables", "B_projector_q", "dual_Hminus1", "PPN;alpha3;orbital;R10", "OPEN_VARIATION_ORDER_NOT_SIGNED"),
        ("JQC2431_6_memory_history", "J_q^memory", "memory/history kernel source", "zero if local memory kernel has no q projection or is topological/first-class", "B_memory_q", "dual_Hminus1", "time;clock;Gdot;cosmology-local", "OPEN_MEMORY_TAIL_NOT_ZERO"),
        ("JQC2431_7_source_normalization", "J_q^source_norm", "measured GM/source calibration and active weight", "zero if measured source mass/charge projector is q-orthogonal and does not double count GR mass", "B_source_norm_q", "dimensionless_or_charge", "Newton;PPN;R10;WEP", "OPEN_SOURCE_NORMALIZATION_NOT_SIGNED"),
        ("JQC2431_8_curvature_vertex", "J_q^curvature", "explicit q-curvature or hidden-visible vertex", "zero if parent object language forbids q R, q R^2, q F^2, q Weyl^2 and equivalent target maps", "B_curvature_q", "dual_Hminus1", "R10;PPN;local_geometry;EM", "OPEN_VERTEX_EXCLUSION_NOT_SIGNED"),
        ("JQC2431_9_total_abs", "J_q^abs", "absolute no-cancellation envelope", "J_q^abs=sum_i ||J_q^i||_*; theorem-zero only if every component is zero in same branch", "B_total_q", "dual_Hminus1", "all_local_arenas", "SCHEMA_READY_VALUES_MISSING"),
    ]
    return [
        base_row(
            component_id=component_id,
            symbol=symbol,
            definition=definition,
            zero_condition=zero_condition,
            bound_symbol=bound_symbol,
            units=units,
            observable_links=observable_links,
            current_status=current_status,
            theorem_zero=False,
            source_backed=False,
            score_ready=False,
        )
        for component_id, symbol, definition, zero_condition, bound_symbol, units, observable_links, current_status in rows
    ]


def bound_law_rows() -> list[dict[str, Any]]:
    return [
        base_row(bound_id="JQB2431_0_functional_norm", object="source norm", formula="||J_q||_* <= sum_i ||J_q^i||_* := B_total_q", status="NO_CANCELLATION_COMPONENT_SUM", missing_inputs="component norms, units, source files, uncertainty policy"),
        base_row(bound_id="JQB2431_1_q_amplitude", object="q residual amplitude", formula="||q||_H1 <= (B_total_q + ||Phi_boundary_q||_*)/c_q", status="FINITE_RESIDUAL_BOUND_READY_SYMBOLIC", missing_inputs="coercivity c_q, boundary norm, Green domain"),
        base_row(bound_id="JQB2431_2_source_test_beta", object="source/test exchange", formula="|alpha_q(lambda)| <= |K_q^R10(lambda)| beta_s_abs(lambda) beta_t_abs(lambda)+epsilon_tail_abs(lambda)", status="PRODUCT_LAW_RETAINED", missing_inputs="K_q, beta_s_abs, beta_t_abs, lambda support, promoted bound curve"),
        base_row(bound_id="JQB2431_3_common_frame", object="universal common frame contribution", formula="common Weyl/disformal frame contributes quadratically to two-body exchange, c_g^2, unless one leg is explicitly inside Qbar", status="LINEAR_CG_SHORTCUT_REJECTED", missing_inputs="parent frame map and source/test leg accounting"),
        base_row(bound_id="JQB2431_4_verdict", object="scoring permission", formula="No component-bound score is allowed until each live component has theorem-zero or numeric source-backed absolute bound rows.", status="CLAIM_BLOCKED", missing_inputs="source-backed coefficients"),
    ]


def arena_impact_rows() -> list[dict[str, Any]]:
    return [
        base_row(arena_id="ARENA2431_0_local_GR", arena="local GR/Newton", impact="Blocked unless J_q^abs=0, Phi_boundary_q=0, q operator is coercive, and projection tails vanish in one parent branch.", status="BLOCKED"),
        base_row(arena_id="ARENA2431_1_R10", arena="R10/fifth force", impact="If any finite q exchange survives, R10 sees source-test product beta_s beta_t with no-cancellation tails.", status="NONCLAIM_SCHEMA_READY"),
        base_row(arena_id="ARENA2431_2_PPN_alpha3", arena="PPN/alpha3", impact="Boundary/reference/worldtube q channels feed alpha3 through K_boundary_alpha3_q Phi_boundary_local_q plus absolute tails.", status="NONCLAIM_SCHEMA_READY"),
        base_row(arena_id="ARENA2431_3_WEP_clock_EM", arena="WEP/clocks/EM", impact="Material marker and visible coefficient leakage feed composition, clock, and EM constraints unless no-hidden-visible-Hom closes.", status="NONCLAIM_SCHEMA_READY"),
        base_row(arena_id="ARENA2431_4_orbital_source_norm", arena="orbital/Newton source normalization", impact="Body worldtube and measured-GM source normalization require q-orthogonality or finite charge bounds.", status="NONCLAIM_SCHEMA_READY"),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(claim_id="CGATE2431_0_Jq_zero", claim="J_q=0 in the local branch", gate_pass=False, reason="exact descent theorem exists but parent observed-object functor/no-marker/no-boundary/no-memory clauses are unsigned"),
        base_row(claim_id="CGATE2431_1_component_bounds", claim="finite J_q component vector is score-ready", gate_pass=False, reason="component rows are symbolic; no numeric source-backed bounds or theorem-zero status"),
        base_row(claim_id="CGATE2431_2_local_GR", claim="local GR/Newton reduction follows", gate_pass=False, reason="J_q, Phi_boundary_q, coercivity and projection gates are not all closed"),
        base_row(claim_id="CGATE2431_3_R10_PPN_WEP_clock", claim="local empirical tests can score q branch", gate_pass=False, reason="K/beta/Phi/projection inputs are not sourced"),
        base_row(claim_id="CGATE2431_4_no_hidden_visible", claim="hidden-visible coefficient leakage is impossible", gate_pass=False, reason="parent coefficient functor/target category not constructed"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2431_0_derivation", decision="KEEP_DERIVATION_ROUTE_PRIMARY", rationale="the exact descent lemma can kill many J_q channels if the parent observed-coefficient functor is built", consequence="attack coefficient/readout descent next"),
        base_row(decision_id="DEC2431_1_no_zero_claim", decision="DO_NOT_PROMOTE_JQ_ZERO", rationale="bulk matter theorem is conditional and body/frame/marker/boundary/projector/memory/source-normalization channels remain open", consequence="component vector remains live"),
        base_row(decision_id="DEC2431_2_bounds", decision="USE_ABSOLUTE_COMPONENT_BOUND_IF_DERIVATION_FAILS", rationale="nonzero source channels produce finite q residuals, not local-GR silence", consequence="future empirical runner must use B_total_q and no-cancellation tails"),
        base_row(decision_id="DEC2431_3_cg", decision="REJECT_LINEAR_CG_SCORING", rationale="source-test exchange uses product law; universal common frame appears quadratically unless packed into Qbar", consequence="keeps R10/fifth-force accounting honest"),
        base_row(decision_id="DEC2431_4_public", decision="NO_GITHUB_ACTION", rationale="private derivation/source audit only", consequence="continue goal work privately"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2431_0_selected",
            selection_status="selected",
            target_file="2432-Y5-R2FR-parent-observed-coefficient-functor-or-first-Jq-bound-row.md",
            target_script="scripts/Y5_R2FR_parent_observed_coefficient_functor_or_first_Jq_bound_row_2432.py",
            task="try to construct the parent observed-coefficient/readout functor that makes visible constants, frames, clocks, masses, EM coefficients and source weights q-blind; if it fails, fill the first source-backed J_q component-bound row as nonclaim",
            acceptance_target="no-hidden-visible coefficient/readout Hom theorem closes, or first finite J_q component row has units/projection/source/provenance and valid_for_claim=false",
            guardrails="do not invent coefficient values, cancel components, claim local GR/R10/PPN/WEP/clock/orbital pass, edit formalization-workbench, or push GitHub",
        ),
        base_row(
            route_id="NEXT2431_1_parallel",
            selection_status="held_parallel",
            target_file="2432b-Y5-R2FR-body-worldtube-Qq-zero-or-source-charge-bound.md",
            target_script="scripts/Y5_R2FR_body_worldtube_Qq_zero_or_source_charge_bound_2432b.py",
            task="separately attack the body/worldtube charge that can source exterior q even when bulk J_q is zero",
            acceptance_target="Q_q[body]=0 theorem or source-backed charge-bound template",
            guardrails="do not promote exterior vacuum silence to full source matching",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue_component_vector", OUTPUTS["component_vector"], COPY_TARGETS["queue_component_vector"], "J_q component vector nonclaim queue"),
        ("queue_descent", OUTPUTS["descent_theorem"], COPY_TARGETS["queue_descent"], "J_q exact descent theorem nonclaim queue"),
        ("branch_wep", OUTPUTS["component_vector"], COPY_TARGETS["branch_wep"], "WEP/local residual J_q component vector"),
        ("beta_docs", OUTPUTS["component_vector"], COPY_TARGETS["beta_docs"], "beta-source J_q component vector"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target, note in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=source,
                target_path=target,
                source_exists=source.exists(),
                target_exists=target.exists(),
                notes=note,
            )
        )
    return rows


def validation_rows(all_outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_rows = all_outputs["source_register"]
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_hits: list[Path] = []
    for pattern in ["*2431-Y5-R2FR*", "*P8_Y5_PARENT_QLOC_2431*", "*P8_Y5_BRR545_2431*", "*JR2431*", "*JQ_SOURCE_LEG_COMPONENT_VECTOR_2431*"]:
        formalization_hits.extend(FORMALIZATION.rglob(pattern) if FORMALIZATION.exists() else [])

    checks = [
        ("VAL2431_00_sources_exist", all(row["path_exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL2431_01_source_needles", all(row["needles_found"] for row in source_rows), "all cited source needles are present"),
        ("VAL2431_02_exact_descent_theorem", any(row["theorem_id"] == "JZT2431_1_descent_lemma" and row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in all_outputs["descent_theorem"]), "exact conditional descent theorem is present"),
        ("VAL2431_03_Jq_zero_not_promoted", any(row["theorem_id"] == "JZT2431_5_total_verdict" and row["result"] == "JQ_ZERO_NOT_PROMOTED_COMPONENT_VECTOR_REQUIRED" for row in all_outputs["descent_theorem"]), "J_q zero is not promoted"),
        ("VAL2431_04_component_vector_complete", len(all_outputs["component_vector"]) >= 10 and any(row["component_id"] == "JQC2431_9_total_abs" for row in all_outputs["component_vector"]), "component vector includes total absolute envelope"),
        ("VAL2431_05_no_cancellation_bound", any(row["bound_id"] == "JQB2431_0_functional_norm" and row["status"] == "NO_CANCELLATION_COMPONENT_SUM" for row in all_outputs["bound_law"]), "no-cancellation functional norm is present"),
        ("VAL2431_06_cg_guard", any(row["bound_id"] == "JQB2431_3_common_frame" and row["status"] == "LINEAR_CG_SHORTCUT_REJECTED" for row in all_outputs["bound_law"]), "c_g squared/product-law guard retained"),
        ("VAL2431_07_claims_blocked", all(not row["gate_pass"] for row in all_outputs["claim_gates"]), "all claim gates remain false"),
        ("VAL2431_08_next_target_written", any(row["route_id"] == "NEXT2431_0_selected" for row in all_outputs["next_target"]), "next target selected"),
        ("VAL2431_09_branch_copies", all(row["target_exists"] for row in all_outputs["branch_copies"]), "branch copies were written"),
        ("VAL2431_10_no_formalization_artifacts", len(formalization_hits) == 0, "no 2431 artifacts were written to formalization-workbench"),
    ]
    for check_id, passed, notes in checks:
        rows.append(
            base_row(
                check_id=check_id,
                status="PASS" if passed else "FAIL",
                notes=notes,
                detail="" if passed else "required checkpoint condition failed",
            )
        )
    for path in output_csvs:
        parses, row_count, message = csv_parses(path)
        rows.append(
            base_row(
                check_id=f"VAL2431_CSV_{path.stem}",
                status="PASS" if parses and row_count > 0 else "FAIL",
                notes=f"CSV parses with {row_count} rows",
                detail=message,
            )
        )
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        base_row(
            check_id="VAL2431_OVERALL",
            status="PASS" if overall else "FAIL",
            notes="2431 writes the exact conditional J_q descent theorem, refuses J_q=0 promotion, emits a component-bound vector with no-cancellation/product-law guards, and selects parent observed-coefficient functor or first J_q bound row next",
            detail="",
        )
    )
    return rows


def write_markdown(all_outputs: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2431 - Y5/R2FR Jq Source-Leg Zero Theorem Or Component-Bound Vector",
        "",
        "## Result",
        "- 2431 turns the coupling problem into a precise theorem/fallback fork.",
        "- Exact theorem: if every visible matter/readout/source coefficient descends through q-blind observed objects and `v_q in ker(D Obs)`, then that sector contributes zero to `J_q` by the chain rule.",
        "- Current corpus does not sign the parent observed-coefficient/readout functor, so `J_q=0` is not promoted.",
        "- Instead, `J_q` is decomposed into an absolute component-bound vector: matter, frame, marker, body/worldtube, boundary/reference, projector/domain, memory/history, source normalization, and curvature vertices.",
        "- This is the coupling battlefield in clean form: derive the functor and kill the vector, or source the vector and test the finite residual branch.",
        "",
        "## Practical Status",
        "This is good news in the Mayweather sense: the route is now defensible. We do not need `J_q` to magically vanish; we need either a parent functor that makes it vanish, or honest component bounds that let local tests judge it.",
        "",
        "## Source Register",
        table(["source_id", "source_path", "path_exists", "needles_found", "role"], all_outputs["source_register"]),
        "",
        "## J_q Descent Zero Theorem",
        table(["theorem_id", "target", "statement", "result", "missing_for_claim", "theorem_zero", "valid_for_claim"], all_outputs["descent_theorem"]),
        "",
        "## J_q Component Bound Vector",
        table(["component_id", "symbol", "definition", "zero_condition", "bound_symbol", "units", "observable_links", "current_status", "valid_for_claim"], all_outputs["component_vector"]),
        "",
        "## J_q To q Residual Bound Law",
        table(["bound_id", "object", "formula", "status", "missing_inputs", "valid_for_claim"], all_outputs["bound_law"]),
        "",
        "## Local Arena Impact",
        table(["arena_id", "arena", "impact", "status", "valid_for_claim"], all_outputs["arena_impact"]),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], all_outputs["claim_gates"]),
        "",
        "## Decisions",
        table(["decision_id", "decision", "rationale", "consequence", "valid_for_claim"], all_outputs["decisions"]),
        "",
        "## Next Target",
        table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], all_outputs["next_target"]),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "source_exists", "target_exists", "notes"], all_outputs["branch_copies"]),
        "",
        "## Validation",
        table(["check_id", "status", "notes", "detail"], all_outputs["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for path in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        path.mkdir(parents=True, exist_ok=True)

    all_outputs: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "descent_theorem": descent_theorem_rows(),
        "component_vector": component_vector_rows(),
        "bound_law": bound_law_rows(),
        "arena_impact": arena_impact_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key, rows in all_outputs.items():
        write_csv(OUTPUTS[key], rows)

    all_outputs["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], all_outputs["branch_copies"])
    all_outputs["validation"] = validation_rows(all_outputs)
    write_csv(OUTPUTS["validation"], all_outputs["validation"])
    write_markdown(all_outputs)

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    print(DOC)
    print(OUTPUTS["validation"])
    print(f"VAL2431_OVERALL={all_outputs['validation'][-1]['status']}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_JR_SOURCE_BOUND_2249"
DOC = ROOT / "2249-Y5-R2FR-RAB-JR-source-zero-or-component-bound-pack.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2249_00_2248_doc",
        "source_key": "2248_handoff",
        "source_path": ROOT / "2248-Y5-R2FR-RAB-sourcefree-positive-RAB-nohair-identity-or-alpha3-prior-first-fill.md",
        "needles": ["DEC2248_2_next", "NEXT2248_0_primary"],
        "role": "selects J_R source-zero/component-bound pack as 2249 target",
    },
    {
        "source_id": "SRC2249_01_2248_validation",
        "source_key": "2248_validation",
        "source_path": OUT / "P8_Y5_BRR545_2248_VALIDATION.csv",
        "needles": ["VAL2248_OVERALL", "PASS"],
        "role": "confirms 2248 passed before 2249 starts",
    },
    {
        "source_id": "SRC2249_02_2248_identity",
        "source_key": "2248_identity",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2248_RAB_CONDITIONAL_NOHAIR_IDENTITY.csv",
        "needles": ["NH2248_3_zero_theorem", "CONDITIONAL_THEOREM_PROVED_PREMISES_UNSIGNED"],
        "role": "conditional R_AB no-hair identity requiring J_R=0",
    },
    {
        "source_id": "SRC2249_03_2248_JR",
        "source_key": "2248_jr_decomposition",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2248_JR_SOURCE_ZERO_DECOMPOSITION.csv",
        "needles": ["JR2248_6_total_verdict", "JR_TOTAL_ZERO_NOT_PROVED"],
        "role": "current R_AB source decomposition blocker",
    },
    {
        "source_id": "SRC2249_04_1801_doc",
        "source_key": "1801_jx_source_pack",
        "source_path": ROOT / "1801-Y5-R2FR-JX-source-zero-or-component-bound-pack.md",
        "needles": ["JZS1801_8_verdict", "JX_SOURCE_ZERO_NOT_PROVED_COMPONENT_BOUNDS_REQUIRED"],
        "role": "older J_X source-zero/component-bound pattern",
    },
    {
        "source_id": "SRC2249_05_1801_validation",
        "source_key": "1801_validation",
        "source_path": OUT / "P8_Y5_BRR545_1801_VALIDATION.csv",
        "needles": ["VAL1801_OVERALL", "PASS"],
        "role": "confirms J_X source-bound precedent passed",
    },
    {
        "source_id": "SRC2249_06_2158_doc",
        "source_key": "2158_source_identity",
        "source_path": ROOT / "2158-Y5-R2FR-JX-qbarXT-source-zero-or-bounded-coupling-component-pack.md",
        "needles": ["SZI2158_2_zero_theorem", "JQD2158_7_total_abs_guard"],
        "role": "latest source-zero identity and no-cancellation coupling vector",
    },
    {
        "source_id": "SRC2249_07_2158_validation",
        "source_key": "2158_validation",
        "source_path": OUT / "P8_Y5_BRR545_2158_VALIDATION.csv",
        "needles": ["VAL2158_OVERALL", "PASS"],
        "role": "confirms 2158 source identity passed as nonclaim",
    },
    {
        "source_id": "SRC2249_08_2158_decomposition",
        "source_key": "2158_decomposition",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2158_JX_QBARXT_DECOMPOSITION.csv",
        "needles": ["JQD2158_7_total_abs_guard", "SCHEMA_READY_VALUES_MISSING"],
        "role": "absolute no-cancellation source/test coupling vector",
    },
    {
        "source_id": "SRC2249_09_2158_bounds",
        "source_key": "2158_bounds",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2158_BOUNDED_COUPLING_COMPONENT_PACK.csv",
        "needles": ["BCP2158_0_cg", "BCP2158_10_total"],
        "role": "bounded coupling component symbols for arena rows",
    },
    {
        "source_id": "SRC2249_10_2158_arenas",
        "source_key": "2158_arenas",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2158_ARENA_PROJECTION_ROWS.csv",
        "needles": ["APR2158_5_local_GR", "BLOCKED_PENDING_SOURCE_SILENCE_OR_BOUNDS"],
        "role": "arena projection contract if source silence fails",
    },
    {
        "source_id": "SRC2249_11_1044_pullback",
        "source_key": "1044_pullback",
        "source_path": ROOT / "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md",
        "needles": ["MPD1044_7_exact_theorem_if_signed", "QBC1044_5_total_abs_guard"],
        "role": "exact ordinary matter pullback theorem and fallback envelope",
    },
    {
        "source_id": "SRC2249_12_1088_moms",
        "source_key": "1088_moms",
        "source_path": ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
        "needles": ["MOMS1088_7_verdict", "THM1088_5_conclusion"],
        "role": "minimal ordinary-matter signature contract",
    },
    {
        "source_id": "SRC2249_13_1088_validation",
        "source_key": "1088_validation",
        "source_path": OUT / "P8_Y5_BRR545_1088_VALIDATION.csv",
        "needles": ["V1088_SUMMARY", "pass"],
        "role": "confirms MOMS source-zero theorem is conditional only",
    },
    {
        "source_id": "SRC2249_14_1344_body_charge",
        "source_key": "1344_body_charge",
        "source_path": ROOT / "1344-Y5-R10-RAB-no-XR-vertex-theorem-or-retained-scalar-source-charge-row.md",
        "needles": ["VERT1344_3_body_charge", "QX1344_0_generic_template"],
        "role": "body/interior source-charge lesson: exterior silence does not erase source charge",
    },
    {
        "source_id": "SRC2249_15_1344_validation",
        "source_key": "1344_validation",
        "source_path": OUT / "P8_Y5_BRR545_1344_VALIDATION.csv",
        "needles": ["VAL1344_9_overall", "PASS"],
        "role": "confirms body source-charge template was retained nonclaim",
    },
    {
        "source_id": "SRC2249_16_1720_functor",
        "source_key": "1720_functor",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1720_0_parent_quotient_map", "MFS1720_8_verdict"],
        "role": "matter functor signature remains unsigned",
    },
    {
        "source_id": "SRC2249_17_1761_no_direct_vertex",
        "source_key": "1761_no_direct_vertex",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_1761_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv",
        "needles": ["NDV1761_0_target", "NDV1761_4_current_verdict"],
        "role": "no-direct-source-vertex grammar is a contract, not a claim",
    },
    {
        "source_id": "SRC2249_18_1786_boundary",
        "source_key": "1786_boundary",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_1786_BOUNDARY_MATTER_CLOSURE_GATE.csv",
        "needles": ["BMC1786_1_matter_interface", "BMC1786_5_verdict"],
        "role": "boundary/matter closure gate remains open",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2249_SOURCE_REGISTER.csv",
    "jr_zero_attempt": OUT / "P8_Y5_PARENT_QLOC_2249_JR_ZERO_THEOREM_ATTEMPT.csv",
    "jr_component_decomposition": OUT / "P8_Y5_PARENT_QLOC_2249_JR_COMPONENT_DECOMPOSITION.csv",
    "body_charge_law": OUT / "P8_Y5_PARENT_QLOC_2249_BODY_CHARGE_SOURCE_LAW.csv",
    "component_bound_template": OUT / "P8_Y5_PARENT_QLOC_2249_JR_COMPONENT_BOUND_TEMPLATE.csv",
    "observable_projection": OUT / "P8_Y5_PARENT_QLOC_2249_OBSERVABLE_PROJECTION_LINKS.csv",
    "acceptance_gate": OUT / "P8_Y5_PARENT_QLOC_2249_ACCEPTANCE_GATE.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2249_COUNTERMODEL_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2249_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2249_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2249_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2249_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2249_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_jr_bounds": QUEUE / "JR2249_JR_COMPONENT_BOUND_TEMPLATE_NONCLAIM.csv",
    "queue_body_charge": QUEUE / "JR2249_BODY_CHARGE_SOURCE_LAW_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_JR_source_bound_nonclaim_2249.csv",
    "beta_docs": BETA_DOCS / "RAB_JR_SOURCE_BOUND_2249_NONCLAIM.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall = [row for row in rows if "overall" in row.get(id_key, "").lower() or "summary" in row.get(id_key, "").lower()]
    check_rows = overall or rows
    return all(row.get(result_key, "").lower() == "pass" for row in check_rows)


def false_flags() -> dict[str, bool]:
    return {
        "theorem_zero": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": rel(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and all(needle in text for needle in source["needles"]),
                "validation_overall_pass": validation_pass(path) if "validation" in source["source_key"] else "",
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def src(*keys: str) -> str:
    by_key = {source["source_key"]: source["source_path"] for source in SOURCES}
    return ";".join(rel(by_key[key]) for key in keys)


def jr_zero_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "JZT2249_0_definition",
            "J_R total source in the candidate R_AB equation",
            "J_R := J_R^bulk + J_R^body/worldtube + J_R^boundary + J_R^readout + J_R^history + J_R^projector + J_R^counterterm",
            "This replaces a single foggy coupling with a component vector that can be zero-proved or bounded without cancellation.",
            "DECOMPOSITION_WRITTEN_NOT_ZERO",
            "MISSING_COMPONENT_ZERO_OR_ABS_BOUNDS",
        ),
        (
            "JZT2249_1_ordinary_matter_pullback",
            "ordinary matter bulk source",
            "If ordinary matter depends only on quotient observables q(Phi), constants are vertical-trivial, lifts are gauge/EOM/boundary, and no shadow/readout/source weights exist, then the ordinary bulk term vanishes.",
            "This is the exact 1044/1088/2158 chain-rule theorem, specialized as a future R_AB parent-action contract.",
            "EXACT_CONDITIONAL_THEOREM_PARENT_UNSIGNED",
            "MISSING_MOMS_SIGNATURE_FOR_RAB_VERTICAL",
        ),
        (
            "JZT2249_2_body_charge_warning",
            "body/interior source charge",
            "Even if J_R=0 in an exterior vacuum domain, a body/worldtube charge Q_R[body] can source boundary data for R_AB.",
            "This is the key repair: exterior source silence is not enough for local GR unless the matching charge is zero or bounded.",
            "EXTERIOR_ZERO_INSUFFICIENT_BODY_CHARGE_OPEN",
            "MISSING_QR_BODY_ZERO_OR_BOUND",
        ),
        (
            "JZT2249_3_boundary_history_readout",
            "non-bulk source tails",
            "Boundary, history, readout, projector and counterterm tails must vanish separately or enter an absolute envelope.",
            "No hidden cancellation is allowed between source components.",
            "TAIL_CHANNELS_OPEN",
            "MISSING_TAIL_ZERO_OR_BOUNDS",
        ),
        (
            "JZT2249_4_verdict",
            "J_R=0 theorem status",
            "J_R=0 is not proved; only an exact conditional source-silence route and a nonclaim component-bound route are now assembled.",
            "Keep the 2248 no-hair theorem conditional and do not claim local GR/Newton.",
            "JR_ZERO_NOT_PROVED_COMPONENT_BOUNDS_REQUIRED",
            "MISSING_PARENT_SIGNATURE_OR_SOURCE_BACKED_COMPONENTS",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "target": target,
            "statement": statement,
            "result": result,
            "current_status": status,
            "missing_input": missing,
            "source_paths": src("2248_jr_decomposition", "1044_pullback", "1088_moms", "2158_source_identity", "1344_body_charge"),
            **false_flags(),
        }
        for attempt_id, target, statement, result, status, missing in rows
    ]


def jr_component_decomposition_rows() -> list[dict[str, Any]]:
    components = [
        ("JRD2249_0_matter_bulk", "J_R_matter_bulk", "ordinary matter variation projected onto R_AB", "zero if MOMS-style ordinary matter signature descends through q and R_AB is quotient-vertical", "MISSING_MATTER_DESCENT_FOR_RAB"),
        ("JRD2249_1_curvature_vertex", "J_R_curvature_vertex", "linear R_AB-curvature or hidden-sector vertex", "zero only if the parent object language forbids B_R R_obs or equivalent curvature-source terms", "MISSING_NO_RAB_CURVATURE_VERTEX"),
        ("JRD2249_2_body_worldtube", "J_R_body_worldtube", "interior/source-worldtube charge that fixes exterior boundary data", "zero if Q_R[body]=0 by source matching, symmetry, screening, or parent charge law", "MISSING_QR_BODY_ZERO_OR_BOUND"),
        ("JRD2249_3_boundary_edge", "J_R_boundary_edge", "edge, corner, reference, and boundary collar source term", "zero if no-flux/exact-boundary theorem covers the physical source boundary, not just compact representative transforms", "MISSING_PHYSICAL_BOUNDARY_EDGE_RULE"),
        ("JRD2249_4_readout", "J_R_readout", "post-variation measured-G/source normalization or calibration re-entry", "zero if variation-before-readout and no-shadow-frame clauses are parent signed", "MISSING_READOUT_NO_REENTRY"),
        ("JRD2249_5_history", "J_R_history", "memory/history tail acting as an effective source", "zero if compact-local stable kernel theorem excludes source-memory injection", "MISSING_HISTORY_KERNEL_ZERO_OR_BOUND"),
        ("JRD2249_6_projector", "J_R_projector", "projection/constraint commutator leakage into R_AB", "zero if projector commutes with source extraction and R_AB vertical direction is owned", "MISSING_PROJECTOR_COMMUTATOR_ZERO"),
        ("JRD2249_7_counterterm", "J_R_counterterm", "reference/subtraction/counterterm source dependence", "zero if counterterms are fixed topological/reference constants before variation", "MISSING_COUNTERTERM_SOURCE_RULE"),
        ("JRD2249_8_total_abs_guard", "J_R_abs_total", "absolute no-cancellation envelope", "|J_R| <= sum_i |J_R_i| with every component theorem-zero or source-backed", "MISSING_COMPONENT_VALUES_AND_SOURCE_PATHS"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": component_id,
            "component": component,
            "meaning": meaning,
            "zero_or_bound_condition": condition,
            "current_status": "NOT_ZERO_PROVED" if component_id != "JRD2249_8_total_abs_guard" else "ABS_ENVELOPE_SCHEMA_READY_VALUES_MISSING",
            "missing_input": missing,
            "no_cancellation_policy": "component signs cannot be used to cancel; each source channel must be zero-proved or bounded in absolute value",
            "source_paths": src("2248_jr_decomposition", "2158_decomposition", "1344_body_charge", "1786_boundary"),
            **false_flags(),
        }
        for component_id, component, meaning, condition, missing in components
    ]


def body_charge_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "law_id": "BCL2249_0_density",
            "object": "rho_R source density",
            "formula": "rho_R = B_RR R_obs + C_RT T + J_R_matter_bulk + J_R_readout + J_R_history + J_R_projector + J_R_counterterm",
            "interpretation": "R_AB local hair is sourced by body/interior and nonbulk channels unless every coefficient vanishes or is bounded.",
            "current_status": "SOURCE_DENSITY_TEMPLATE_NONCLAIM",
            "needed_inputs": "B_RR;C_RT;J_R_components;units;body measure;source paths",
            "source_paths": src("1344_body_charge", "2248_identity"),
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "law_id": "BCL2249_1_body_charge",
            "object": "Q_R[body]",
            "formula": "Q_R[body] = int_body sqrt(gamma) W_R rho_R + Q_R_boundary",
            "interpretation": "The exterior equation may be homogeneous while Q_R[body] still fixes a nonzero exterior R_AB profile.",
            "current_status": "BODY_CHARGE_TEMPLATE_NONCLAIM",
            "needed_inputs": "W_R;body model;screening/matching rule;Q_R_boundary;normalization",
            "source_paths": src("1344_body_charge", "05_reciprocity_attempt") if False else src("1344_body_charge", "2248_handoff"),
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "law_id": "BCL2249_2_exterior_profile",
            "object": "exterior R_AB profile",
            "formula": "R_AB(r) ~ Q_R[body] G_R(r;lambda_R,Z_R,domain) plus boundary/history tails",
            "interpretation": "A local no-hair claim needs Q_R[body]=0, not merely J_R=0 away from the body.",
            "current_status": "PROFILE_TEMPLATE_NONCLAIM",
            "needed_inputs": "lambda_R;Z_R;domain Green function;tail envelope",
            "source_paths": src("2248_identity", "2158_arenas"),
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "law_id": "BCL2249_3_zero_switch",
            "object": "Q_R[body]=0 theorem",
            "formula": "Q_R[body]=0 iff B_RR=C_RT=J_R_components=Q_R_boundary=0 in the same parent branch, or the R_AB direction is absent/constraint-only.",
            "interpretation": "This is the clean bridge from source silence to local GR; it remains unsigned.",
            "current_status": "ZERO_SWITCH_REJECTED_UNTIL_PARENT_SIGNED",
            "needed_inputs": "parent no-source signature or body-charge bound rows",
            "source_paths": src("2248_identity", "1088_moms", "1344_body_charge"),
            **false_flags(),
        },
    ]


def component_bound_template_rows() -> list[dict[str, Any]]:
    bounds = [
        ("JBT2249_0_BRR", "B_RR", "curvature-source vertex", "|B_RR| <= theorem_zero_or_source_bound", "R10;PPN;local_GR"),
        ("JBT2249_1_CRT", "C_RT", "matter trace/source vertex", "|C_RT| <= theorem_zero_or_source_bound", "R10;WEP;PPN;orbital"),
        ("JBT2249_2_qbar_RT", "qbar_RT", "test/source matter response to R_AB", "|qbar_RT| <= |qbar_geom|+|qbar_constants|+|qbar_marker|+|qbar_source_weight|+|qbar_nonH|", "R10;WEP;clock"),
        ("JBT2249_3_QR_body", "Q_R_body", "body/worldtube source charge", "|Q_R_body| <= int_body abs(W_R rho_R)+|Q_R_boundary|", "R10;PPN;orbital;local_GR"),
        ("JBT2249_4_QR_boundary", "Q_R_boundary", "boundary/edge/reference source charge", "|Q_R_boundary| <= |edge|+|corner|+|reference|+|support_tail|", "boundary;R10;orbital"),
        ("JBT2249_5_Creadout_R", "C_readout_R", "post-variation readout/source-normalization tail", "|C_readout_R| <= theorem_zero_or_calibration_bound", "orbital;clock;PPN"),
        ("JBT2249_6_Khistory_R", "K_history_R", "history kernel source tail", "||K_history_R|| weighted by source support and decay envelope", "orbital;clock;local_GR"),
        ("JBT2249_7_projector_R", "Delta_projector_R", "projector/constraint commutator leakage", "||[Pi_source,P_R]|| or theorem-zero commutator", "PPN;local_GR;R10"),
        ("JBT2249_8_total_abs", "JR_abs_envelope", "absolute no-cancellation total", "sum_abs_components in common source normalization", "all_local_arenas"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "formula_or_bound": formula,
            "current_status": "SCHEMA_READY_VALUES_MISSING" if row_id == "JBT2249_8_total_abs" else "MISSING_ZERO_THEOREM_OR_SOURCE_BOUND",
            "units": "declared_common_RAB_source_normalization_required",
            "source_path": src("2158_bounds", "1044_pullback", "1344_body_charge"),
            "observable_link": observable,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, symbol, definition, formula, observable in bounds
    ]


def observable_projection_rows() -> list[dict[str, Any]]:
    rows = [
        ("OPL2249_0_R10", "R10 short-range", "alpha_R(lambda)=K_R(lambda) Qbar_RH(lambda) qbar_RT + edge/history/readout tails", "K_R;lambda_R;Qbar_RH;qbar_RT;Q_R_body;real alpha_bound(lambda)", "MISSING_ARENA_PROJECTION"),
        ("OPL2249_1_PPN", "PPN/preferred-frame", "PPN_R_vec <= tau_PPN dot abs(B_RR,C_RT,Q_R_body,C_readout_R,Delta_projector_R)", "tau_PPN;source-normalized coefficients;Solar-system profile", "MISSING_TAU_PPN_AND_COMPONENTS"),
        ("OPL2249_2_WEP", "WEP/source composition", "eta_AB <= tau_WEP dot abs(differential qbar_RT components)", "material sensitivities;component bounds;same-frame source masses", "MISSING_WEP_COMPONENT_VECTOR"),
        ("OPL2249_3_clocks", "clocks/redshift/constants", "clock_R <= tau_clock dot abs(qbar_constants,Creadout_R,Khistory_R)", "clock sensitivities;constant derivative bounds;readout rule", "MISSING_CLOCK_PROJECTION"),
        ("OPL2249_4_orbital", "orbital/source-support", "orbital_R <= tau_orbital dot abs(Q_R_body,Q_R_boundary,Khistory_R,Creadout_R)", "worldtube support;source normalization;history kernel", "MISSING_ORBITAL_PROJECTION"),
        ("OPL2249_5_local_GR", "local GR/Newton", "derived only if no-hair activation plus Q_R[body]=0 and observable projection tails vanish", "2248 nohair gates;2249 source gates;boundary/operator gates", "BLOCKED_PENDING_SOURCE_SILENCE_OR_BOUNDS"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "projection_id": projection_id,
            "arena": arena,
            "formula_or_contract": formula,
            "required_inputs": required,
            "current_status": status,
            "claim_effect": "no claim/no score",
            "source_paths": src("2158_arenas", "2248_identity", "1344_body_charge"),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for projection_id, arena, formula, required, status in rows
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("AC2249_0_JR_zero", "J_R=0 source theorem", "FAIL_PARENT_UNSIGNED_COMPONENTS", "ordinary matter chain-rule route is exact but unsigned; body/boundary/readout/history/projector components remain open"),
        ("AC2249_1_body_charge", "Q_R[body]=0 or bounded", "FAIL_BODY_CHARGE_INPUTS_MISSING", "exterior vacuum is insufficient without source-worldtube matching"),
        ("AC2249_2_component_bounds", "finite component envelope", "SCHEMA_READY_VALUES_MISSING", "all symbolic component rows need source-backed values or theorem-zero certificates"),
        ("AC2249_3_no_cancellation", "no hidden cancellation credit", "POLICY_ACTIVE_NOT_SCORE", "absolute component envelope is required"),
        ("AC2249_4_verdict", "R_AB source leg ready for no-hair/local-GR", "JR_SOURCE_LEG_NOT_ZERO_AND_NOT_BOUNDED", "2249 improves the coupling contract but does not close the branch"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "current_status": status,
            "reason": reason,
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in rows
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        ("CM2249_0_shadow_matter_frame", "ordinary matter uses an R_AB-sensitive hidden/shadow frame while visible q geometry descends", "MOMS/no-shadow clauses remain unsigned", "parent ordinary-matter signature excluding hidden frames"),
        ("CM2249_1_body_charge", "source body has Q_R[body] even when exterior J_R=0", "source-worldtube matching is not zero-proved", "Q_R[body]=0 theorem or sourced body-charge bound"),
        ("CM2249_2_curvature_vertex", "parent action contains B_RR R_AB R_obs or equivalent curvature-source vertex", "no-R_AB curvature vertex theorem is missing", "parent object-language no-vertex proof or B_RR bound"),
        ("CM2249_3_source_weight", "species/source weight creates a source current without obvious WEP-breaking metric frame", "no source-only prefactor theorem is unsigned", "MOMS source-weight exclusion or delta-kappa bound"),
        ("CM2249_4_readout_history", "readout/history kernel reintroduces a source after variation", "variation-before-readout and compact kernel theorems are unsigned", "readout/kernal zero theorem or finite tail bounds"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": countermodel_id,
            "countermodel": countermodel,
            "survives_current_constraints": True,
            "why_survives": why,
            "what_kills_it": kills,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for countermodel_id, countermodel, why, kills in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CL2249_0_JR_zero", "J_R=0 in local exterior and source matching", "BLOCKED", "JZT2249_4 verdict is JR_ZERO_NOT_PROVED_COMPONENT_BOUNDS_REQUIRED"),
        ("CL2249_1_QR_body", "Q_R[body]=0 or bound-ready", "BLOCKED", "BCL2249 body charge rows are symbolic and nonclaim"),
        ("CL2249_2_RAB_nohair", "2248 positive no-hair theorem activates", "BLOCKED", "source leg remains unsigned"),
        ("CL2249_3_empirical_scores", "R10/PPN/WEP/clock/orbital score rows are runnable", "BLOCKED", "component values and arena projections are missing"),
        ("CL2249_4_local_GR_Newton", "local GR/Newton reduction is derived", "BLOCKED", "source/body charge and projection gates remain open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2249_0_exact_contract",
            "decision": "JR_SOURCE_ZERO_CONTRACT_SHARPENED",
            "reason": "ordinary matter source silence is an exact conditional chain-rule theorem, but R_AB also needs body/worldtube and curvature-source silence",
            "next_action": "do not activate no-hair; fill or derive source components",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2249_1_body_charge_repair",
            "decision": "EXTERIOR_VACUUM_NOT_ENOUGH",
            "reason": "Q_R[body] can source the exterior R_AB profile even if J_R=0 away from the body",
            "next_action": "promote body/source-worldtube charge to a first-class blocker",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2249_2_next",
            "decision": "PARENT_MATTER_CURVATURE_SOURCE_SIGNATURE_OR_FIRST_BODY_CHARGE_ROW_NEXT",
            "reason": "the least-handwavy route is either a parent no-source signature for R_AB or a sourced Q_R[body]/B_RR/C_RT row",
            "next_action": "2250-Y5-R2FR-RAB-parent-matter-curvature-source-signature-or-first-body-charge-row.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2249_0_primary",
            "next_target": "2250-Y5-R2FR-RAB-parent-matter-curvature-source-signature-or-first-body-charge-row.md",
            "script": "scripts/Y5_R2FR_RAB_parent_matter_curvature_source_signature_or_first_body_charge_row_2250.py",
            "objective": "try to parent-sign the R_AB ordinary-matter/curvature no-source signature; if unsigned, stage the first Q_R[body], B_RR, or C_RT source-charge row as nonclaim",
            "selection_status": "selected",
            "success_condition": "R_AB source signature closes, or at least one body/source coefficient becomes theorem-zero/source-backed while all local claims remain blocked",
            "forbidden_shortcuts": "exterior-vacuum-only proof; source cancellation; invented coefficients; local-GR/R10/PPN pass claim; GitHub action; formalization-workbench edit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2249_1_parallel_boundary",
            "next_target": "2250b-Y5-R2FR-RAB-boundary-worldtube-charge-zero-or-tail-bound.md",
            "script": "scripts/Y5_R2FR_RAB_boundary_worldtube_charge_zero_or_tail_bound_2250b.py",
            "objective": "prove boundary/source-worldtube charge zero or emit Q_R_boundary/Phi_boundary tail bounds",
            "selection_status": "held_parallel",
            "success_condition": "boundary source charge theorem or nonclaim tail coefficient row",
            "forbidden_shortcuts": "using compact-collar lemma on physical source edges without proof",
            "valid_for_claim": False,
        },
    ]


def copy_branch_rows() -> list[dict[str, Any]]:
    plan = [
        ("queue_jr_bounds", OUTPUTS["component_bound_template"], COPY_TARGETS["queue_jr_bounds"], "R_AB J_R component-bound nonclaim queue"),
        ("queue_body_charge", OUTPUTS["body_charge_law"], COPY_TARGETS["queue_body_charge"], "body/source-worldtube charge nonclaim queue"),
        ("branch_wep", OUTPUTS["component_bound_template"], COPY_TARGETS["branch_wep"], "WEP branch locked source-coupling vector copy"),
        ("beta_docs", OUTPUTS["component_bound_template"], COPY_TARGETS["beta_docs"], "beta-source docs source-coupling vector copy"),
    ]
    rows = []
    for copy_id, source_path, target_path, reason in plan:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": f"BC2249_{copy_id}",
                "source_path": rel(source_path),
                "target_path": rel(target_path),
                "target_exists": target_path.exists(),
                "target_parses": parse_csv(target_path),
                "reason": reason,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def validation_rows(paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    zero_attempt = read_csv(OUTPUTS["jr_zero_attempt"])
    components = read_csv(OUTPUTS["jr_component_decomposition"])
    body = read_csv(OUTPUTS["body_charge_law"])
    bounds = read_csv(OUTPUTS["component_bound_template"])
    projections = read_csv(OUTPUTS["observable_projection"])
    acceptance = read_csv(OUTPUTS["acceptance_gate"])
    countermodels = read_csv(OUTPUTS["countermodels"])
    claims = read_csv(OUTPUTS["claim_gates"])
    decisions = read_csv(OUTPUTS["decision"])
    next_targets = read_csv(OUTPUTS["next_target"])
    branch_copies = read_csv(OUTPUTS["branch_copies"])

    def check(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}

    csv_parse_ok = True
    for path in paths:
        try:
            parse_csv(path)
        except Exception:
            csv_parse_ok = False

    formalization_2249 = []
    if FORMALIZATION.exists():
        formalization_2249 = list(FORMALIZATION.rglob("*2249*"))

    all_generated_rows = [row for path in paths for row in read_csv(path)]
    rows = [
        check("VAL2249_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        check("VAL2249_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        check("VAL2249_2_prior_validations", all(row["validation_overall_pass"] in ("", "True") for row in source_rows), "2248/1801/2158/1088/1344 validations pass where checked"),
        check("VAL2249_3_JR_zero_refused", any(row["attempt_id"] == "JZT2249_4_verdict" and row["current_status"] == "JR_ZERO_NOT_PROVED_COMPONENT_BOUNDS_REQUIRED" for row in zero_attempt), "J_R=0 is not promoted"),
        check("VAL2249_4_body_charge_warning", any(row["law_id"] == "BCL2249_3_zero_switch" and row["current_status"] == "ZERO_SWITCH_REJECTED_UNTIL_PARENT_SIGNED" for row in body), "body charge zero switch is rejected until signed"),
        check("VAL2249_5_component_abs_guard", any(row["component_id"] == "JRD2249_8_total_abs_guard" and row["current_status"] == "ABS_ENVELOPE_SCHEMA_READY_VALUES_MISSING" for row in components), "absolute no-cancellation component guard is present"),
        check("VAL2249_6_bounds_nonclaim", all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in bounds), "component bound templates remain nonclaim"),
        check("VAL2249_7_projections_blocked", all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in projections), "observable projections remain blocked"),
        check("VAL2249_8_acceptance_blocks", any(row["gate_id"] == "AC2249_4_verdict" and row["current_status"] == "JR_SOURCE_LEG_NOT_ZERO_AND_NOT_BOUNDED" for row in acceptance), "acceptance gate blocks source-leg readiness"),
        check("VAL2249_9_countermodels_retained", all(row["survives_current_constraints"] == "True" for row in countermodels), "countermodels remain live"),
        check("VAL2249_10_claim_gates_blocked", all(row["status"] == "BLOCKED" for row in claims), "all claim gates are blocked"),
        check("VAL2249_11_decision_next", any(row["decision_id"] == "DEC2249_2_next" and "PARENT_MATTER_CURVATURE_SOURCE" in row["decision"] for row in decisions), "decision selects parent source signature/body-charge row next"),
        check("VAL2249_12_next_selected", any(row["route_id"] == "NEXT2249_0_primary" and row["selection_status"] == "selected" for row in next_targets), "next target selected"),
        check("VAL2249_13_csv_parse", csv_parse_ok, "all generated 2249 CSVs parse"),
        check("VAL2249_14_no_claim_flags", all(row.get("valid_for_claim", "False") != "True" and row.get("claim_allowed", "False") != "True" and row.get("theorem_zero", "False") != "True" and row.get("score_ready", "False") != "True" for row in all_generated_rows), "no generated theorem/score/claim flags are true"),
        check("VAL2249_15_branch_copies", all(row["target_exists"] == "True" and row["target_parses"] == "True" for row in branch_copies), "branch/queue copies exist and parse"),
        check("VAL2249_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        check("VAL2249_17_formalization_no_2249", not formalization_2249, "formalization-workbench has no 2249 outputs"),
    ]
    rows.append(
        check(
            "VAL2249_OVERALL",
            all(row["result"] == "PASS" for row in rows),
            "2249 sharpens J_R into source-zero/body-charge/component-bound contracts, refuses claims, and selects parent source signature or first body-charge row next",
        )
    )
    return rows


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_doc(
    source_rows: list[dict[str, Any]],
    zero_attempt: list[dict[str, Any]],
    components: list[dict[str, Any]],
    body: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    projections: list[dict[str, Any]],
    acceptance: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2249 - Y5/R2FR R_AB J_R Source-Zero or Component-Bound Pack",
            "## Verdict\n\n2249 tries the derivation route first. The ordinary-matter source-silence theorem is exact as a conditional chain-rule result, but it is not parent-signed for the `R_AB` branch.\n\nThe important tightening is that `J_R=0` in the exterior is not enough by itself. A body/source-worldtube charge `Q_R[body]` can still set exterior `R_AB` hair through boundary matching. So the coupling problem is now a concrete vector: prove every component zero, or fill source-backed absolute bounds. No local-GR/Newton, R10, PPN, WEP, clock, orbital, or alpha3 claim is allowed from this checkpoint.",
            "## Source Register\n" + markdown_table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"]),
            "## J_R Zero Theorem Attempt\n" + markdown_table(zero_attempt, ["attempt_id", "target", "statement", "current_status", "missing_input", "valid_for_claim"]),
            "## J_R Component Decomposition\n" + markdown_table(components, ["component_id", "component", "meaning", "current_status", "missing_input", "valid_for_claim"]),
            "## Body Charge Source Law\n" + markdown_table(body, ["law_id", "object", "formula", "current_status", "needed_inputs", "valid_for_claim"]),
            "## Component Bound Template\n" + markdown_table(bounds, ["row_id", "symbol", "definition", "formula_or_bound", "current_status", "observable_link", "valid_for_claim"]),
            "## Observable Projection Links\n" + markdown_table(projections, ["projection_id", "arena", "formula_or_contract", "current_status", "claim_effect", "valid_for_claim"]),
            "## Acceptance Gate\n" + markdown_table(acceptance, ["gate_id", "gate", "current_status", "reason", "gate_pass", "valid_for_claim"]),
            "## Countermodel Ledger\n" + markdown_table(countermodels, ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "## Claim Gates\n" + markdown_table(claims, ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
            "## Decision Ledger\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "## Next Target\n" + markdown_table(next_targets, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "## Branch Copies\n" + markdown_table(branch_copies, ["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"]),
            "## Validation\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\nThis is the cleanest shape of the coupling problem so far. The next leap is not more broad auditing; it is a source-signature strike: either derive that the parent action has no `R_AB` matter/curvature/body source slot, or admit the body charge and make it empirical with real bounds. That is a genuine fork, not a loop.",
        ]
    ) + "\n"


def main() -> None:
    source_rows = source_register_rows()
    zero_attempt = jr_zero_attempt_rows()
    components = jr_component_decomposition_rows()
    body = body_charge_law_rows()
    bounds = component_bound_template_rows()
    projections = observable_projection_rows()
    acceptance = acceptance_gate_rows()
    countermodels = countermodel_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["jr_zero_attempt"], zero_attempt)
    write_csv(OUTPUTS["jr_component_decomposition"], components)
    write_csv(OUTPUTS["body_charge_law"], body)
    write_csv(OUTPUTS["component_bound_template"], bounds)
    write_csv(OUTPUTS["observable_projection"], projections)
    write_csv(OUTPUTS["acceptance_gate"], acceptance)
    write_csv(OUTPUTS["countermodels"], countermodels)
    write_csv(OUTPUTS["claim_gates"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_targets)

    branch_copies = copy_branch_rows()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    remove_pycache()
    generated = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)
    remove_pycache()

    DOC.write_text(
        build_doc(source_rows, zero_attempt, components, body, bounds, projections, acceptance, countermodels, claims, decisions, next_targets, branch_copies, validation),
        encoding="utf-8",
    )

    if not validation_pass(OUTPUTS["validation"]):
        raise SystemExit(f"2249 validation failed: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_Q_REMOVAL_CERTIFICATE_2311"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2311-Y5-R2FR-parent-q-removal-certificate-degree-count-boundary-neutrality-or-independent-Hessian-source-pack.md"

PATHS = {
    "2310_doc": ROOT / "2310-Y5-R2FR-q-branch-selection-no-pole-or-independent-Hessian-first-source-row.md",
    "2310_validation": OUT / "P8_Y5_BRR545_2310_VALIDATION.csv",
    "2310_no_pole": OUT / "P8_Y5_PARENT_QLOC_2310_NO_POLE_THEOREM_GATE.csv",
    "2310_independent": OUT / "P8_Y5_PARENT_QLOC_2310_INDEPENDENT_Q_FIRST_SOURCE_ROW.csv",
    "2296_doc": ROOT / "2296-Y5-R2FR-q-sourcefree-positive-nohair-or-firstclass-owner-gate.md",
    "2296_firstclass": OUT / "P8_Y5_PARENT_QLOC_2296_FIRSTCLASS_OWNER_GATE.csv",
    "2296_nohair": OUT / "P8_Y5_PARENT_QLOC_2296_Q_CONDITIONAL_NOHAIR_IDENTITY.csv",
    "2297_doc": ROOT / "2297-Y5-R2FR-Jq-source-zero-or-component-bound-pack.md",
    "2297_body": OUT / "P8_Y5_PARENT_QLOC_2297_BODY_CHARGE_SOURCE_LAW.csv",
    "2297_bounds": OUT / "P8_Y5_PARENT_QLOC_2297_JQ_COMPONENT_BOUND_TEMPLATE.csv",
    "2300_doc": ROOT / "2300-Y5-R2FR-minimal-parent-action-q-source-vector-normal-form-or-closure-declaration.md",
    "2300_slots": OUT / "P8_Y5_PARENT_QLOC_2300_PARENT_ACTION_Q_SLOT_INVENTORY.csv",
    "2300_firstclass": OUT / "P8_Y5_PARENT_QLOC_2300_Q_FIRSTCLASS_REMOVAL_CONTRACT.csv",
    "2301_firstclass": OUT / "P8_Y5_PARENT_QLOC_2301_Q_FIRSTCLASS_REMOVAL_ATTEMPT.csv",
    "2302_doc": ROOT / "2302-Y5-R2FR-q-representation-or-firstclass-certificate-or-BqWeyl-bound-row.md",
    "637_qmap": OUT / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv",
    "1023_doc": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
    "1157_doc": ROOT / "1157-Y5-R10-parent-q-map-null-generator-proof-or-cg-bound-first-fill.md",
}

SOURCES = [
    ("SRC2311_00_2310_doc", "2310_doc", PATHS["2310_doc"], ["DEC2310_4_next", "NP2310_6_activation_verdict"], "direct 2310 handoff"),
    ("SRC2311_01_2310_validation", "2310_validation", PATHS["2310_validation"], ["VAL2310_OVERALL", "PASS"], "2310 validation"),
    ("SRC2311_02_2310_no_pole", "2310_no_pole", PATHS["2310_no_pole"], ["NP2310_0_theorem_statement", "NO_POLE_NOT_ACTIVATED_CURRENT"], "incoming no-pole theorem gate"),
    ("SRC2311_03_2310_independent", "2310_independent", PATHS["2310_independent"], ["IQSRC2310_6_claim_gate", "CLAIM_BLOCKED"], "incoming independent-q fallback pack"),
    ("SRC2311_04_2296_doc", "2296_doc", PATHS["2296_doc"], ["conditional local q no-hair theorem", "FIRSTCLASS"], "2296 no-hair/first-class source"),
    ("SRC2311_05_2296_firstclass", "2296_firstclass", PATHS["2296_firstclass"], ["FC2296_7_verdict", "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED"], "first-class owner gate"),
    ("SRC2311_06_2296_nohair", "2296_nohair", PATHS["2296_nohair"], ["NH2296_4_firstclass_alternative", "ALTERNATIVE_CONDITIONAL_THEOREM_STATED"], "conditional first-class no-pole theorem"),
    ("SRC2311_07_2297_doc", "2297_doc", PATHS["2297_doc"], ["Q_q[body]", "EXTERIOR_VACUUM_NOT_ENOUGH"], "source/body charge warning"),
    ("SRC2311_08_2297_body", "2297_body", PATHS["2297_body"], ["BCL2297_1_body_charge", "Q_q[body]"], "body charge source law"),
    ("SRC2311_09_2297_bounds", "2297_bounds", PATHS["2297_bounds"], ["JBT2297_3_Qq_body", "MISSING_ZERO_THEOREM_OR_SOURCE_BOUND"], "q source component bound template"),
    ("SRC2311_10_2300_doc", "2300_doc", PATHS["2300_doc"], ["q first-class removal", "QFC2300_6_verdict"], "minimal parent q source normal form"),
    ("SRC2311_11_2300_slots", "2300_slots", PATHS["2300_slots"], ["QSLOT2300_2_q_constraint", "FIRSTCLASS_REMOVAL_ROUTE"], "q constraint slot"),
    ("SRC2311_12_2300_firstclass", "2300_firstclass", PATHS["2300_firstclass"], ["QFC2300_6_verdict", "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED"], "first-class removal contract"),
    ("SRC2311_13_2301_firstclass", "2301_firstclass", PATHS["2301_firstclass"], ["QFC2301_6_verdict", "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED"], "later first-class removal attempt"),
    ("SRC2311_14_2302_doc", "2302_doc", PATHS["2302_doc"], ["EVID2302_2_firstclass_package", "CLEANEST_ROUTE_BUT_UNSIGNED"], "q first-class package evidence"),
    ("SRC2311_15_637_qmap", "637_qmap", PATHS["637_qmap"], ["QM637_2_vertical_kernel", "Dq[v_X]=0"], "conditional quotient map vertical kernel"),
    ("SRC2311_16_1023_doc", "1023_doc", PATHS["1023_doc"], ["QVC1023_8_verdict", "fail_current_claim_demote_current_branch"], "q/vX/action certificate fails"),
    ("SRC2311_17_1157_doc", "1157_doc", PATHS["1157_doc"], ["QMAP1157_8_verdict", "PARENT_Q_MAP_NULL_GENERATOR_NOT_DERIVED"], "parent q-map/null-generator proof missing"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2311_SOURCE_REGISTER.csv",
    "certificate": OUT / "P8_Y5_PARENT_QLOC_2311_REMOVAL_CERTIFICATE_AUDIT.csv",
    "degree": OUT / "P8_Y5_PARENT_QLOC_2311_DEGREE_COUNT_THEOREM.csv",
    "boundary": OUT / "P8_Y5_PARENT_QLOC_2311_BOUNDARY_SOURCE_NEUTRALITY.csv",
    "proof": OUT / "P8_Y5_PARENT_QLOC_2311_NO_POLE_PROOF_STATUS.csv",
    "fallback": OUT / "P8_Y5_PARENT_QLOC_2311_INDEPENDENT_HESSIAN_FALLBACK_PACK.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2311_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2311_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2311_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2311_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2311_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2311_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2311_0_certificate", OUTPUTS["certificate"], BETA_DOCS / "Q_REMOVAL_CERTIFICATE_AUDIT_2311_NONCLAIM.csv"),
    ("COPY2311_1_degree", OUTPUTS["degree"], BETA_DOCS / "Q_DEGREE_COUNT_THEOREM_2311_NONCLAIM.csv"),
    ("COPY2311_2_boundary", OUTPUTS["boundary"], RAB_QUEUE / "JR2311_Q_BOUNDARY_SOURCE_NEUTRALITY_NONCLAIM.csv"),
    ("COPY2311_3_fallback", OUTPUTS["fallback"], MICRO_RESIDUALS / "q_independent_Hessian_fallback_pack_nonclaim_2311.csv"),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "missing_needles=" + ";".join(missing)
    return True, "all_needles_found"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
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
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = []
        for field in fields:
            values.append(str(row.get(field, "")).replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, key, path, needles, role in SOURCES:
        ok, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needles": ";".join(needles),
                "needles_found": b(ok),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def build_certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "QRC2311_0_parent_quotient",
            "certificate_clause": "q is defined before variation as a parent quotient/readout map pi:Y->Y_red",
            "exact_requirement": "q labels only reduced observables; vertical representatives are not physical coordinates",
            "current_evidence": "637 gives conditional quotient-map logic; 1157 says parent q-map/null-generator is not derived",
            "status": "NOT_PARENT_SIGNED",
            "blocks": "cannot delete q column from Hessian by declaration",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QRC2311_1_actual_vertical_generator",
            "certificate_clause": "actual local q/X variation is tangent to ker(Dpi)",
            "exact_requirement": "v_q or v_X must be specified on metric/coframe/matter/readout/boundary fields and satisfy Dpi[v]=0",
            "current_evidence": "QM637_2 is conditional; 1023 and 1157 keep actual local Xhat/q direction open",
            "status": "CONDITIONAL_ONLY",
            "blocks": "physical residual q cannot be ruled out",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QRC2311_2_parent_Omega",
            "certificate_clause": "full parent presymplectic form exists on geometry, q, matter, boundary, and readout variables",
            "exact_requirement": "Omega_Y must be known before first-class status can be asserted",
            "current_evidence": "FC2296/QFC2300/QFC2301 all mark parent Omega missing",
            "status": "MISSING_PARENT_OMEGA",
            "blocks": "cannot identify gauge-null q flow",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QRC2311_3_momentum_map",
            "certificate_clause": "i_v Omega_Y = delta G_q plus differentiable boundary term",
            "exact_requirement": "a parent-owned generator G_q[epsilon]=int epsilon C_q + Q_q[epsilon] must produce the q flow",
            "current_evidence": "momentum-map/generator rows are missing in 2296/2300/2301",
            "status": "MISSING_MOMENTUM_MAP",
            "blocks": "q could be physical, second-class, or boundary hair rather than gauge",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QRC2311_4_bracket_closure",
            "certificate_clause": "q generators close first-class without anomalous boundary term",
            "exact_requirement": "{G_q[epsilon],G_q[eta]} must close into constraints plus zero/proper boundary",
            "current_evidence": "bracket closure is missing in 2296/2300/2301",
            "status": "MISSING_BRACKET_CLOSURE",
            "blocks": "an anomaly/edge mode can make q physical",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QRC2311_5_degree_count",
            "certificate_clause": "the first-class constraints remove the q canonical pair",
            "exact_requirement": "rank of q gauge orbit/constraint pair equals q phase-space rank; reduced Omega is nondegenerate without q",
            "current_evidence": "degree count is missing in 2296/2300/2301",
            "status": "MISSING_DEGREE_COUNT",
            "blocks": "no-pole could be confused with under-specified dynamics",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QRC2311_6_action_matter_readout_descent",
            "certificate_clause": "bulk action, matter, constants, clocks, and readouts descend to quotient",
            "exact_requirement": "S=S_red[pi(Phi)] plus proper terms; O=O_red[pi(Phi)]; no q material marker",
            "current_evidence": "1023 records action and matter/no-marker descent as conditional or missing",
            "status": "MISSING_DESCENT_CERTIFICATE",
            "blocks": "q source/readout tails can survive reduction",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QRC2311_7_boundary_source_neutrality",
            "certificate_clause": "boundary, body, worldtube, and source tails are zero/proper",
            "exact_requirement": "Q_q[body], Q_q boundary, Pi_q, edge cocycles, readout/history/projector/counterterm tails vanish or are proper gauge",
            "current_evidence": "2297 shows exterior vacuum silence is insufficient because Q_q[body] can source q hair",
            "status": "MISSING_BOUNDARY_SOURCE_NEUTRALITY",
            "blocks": "even a bulk gauge-looking q can return as edge/source hair",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QRC2311_8_verdict",
            "certificate_clause": "activate q-removal/no-pole certificate",
            "exact_requirement": "QRC2311_0 through QRC2311_7 must pass in the same parent branch",
            "current_evidence": "multiple exact conditional theorem fragments exist, but the combined certificate fails current evidence",
            "status": "CERTIFICATE_NOT_CLOSED_CURRENT",
            "blocks": "no local-GR/Newton promotion; use next source hunt or fallback pack",
            "valid_for_claim": "false",
        },
    ]


def build_degree_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DC2311_0_phase_space_setup",
            "statement": "for N_q local q components the unreduced q sector contributes canonical coordinates (q^A,p_A)",
            "formula": "dim Gamma_q = 2 N_q before constraints, modulo functional analytic domain choices",
            "status": "GENERAL_THEOREM",
            "current_blocker": "N_q/rank and q parent coordinate are not owned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DC2311_1_firstclass_removal_count",
            "statement": "one rank-r first-class family removes 2r phase-space directions",
            "formula": "dim Gamma_red = dim Gamma - 2 rank(G_q) after constraint surface plus quotient by gauge orbits",
            "status": "EXACT_SYMPLECTIC_COUNT_IF_GENERATOR_SIGNED",
            "current_blocker": "G_q and rank(G_q) are missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DC2311_2_no_q_pole_condition",
            "statement": "q has no physical pole iff the q canonical pair lies entirely in the first-class orbit/constraint directions",
            "formula": "rank(G_q)=N_q and span(Ham(G_q)) contains delta/delta q directions; H_red^{-1} is built after quotient and has no q column",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "current_blocker": "vertical-generator identification and degree count missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DC2311_3_secondclass_or_auxiliary_countermodel",
            "statement": "if q is second-class/algebraic instead of first-class, it may have no wave pole but can leave Schur-complement contact terms",
            "formula": "Delta S_eff = -1/2 J_q H_qq^{-1} J_q plus higher-curvature/source terms",
            "status": "LIVE_COUNTERMODEL",
            "current_blocker": "H_qq/J_q/sign/source rows missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DC2311_4_boundary_edge_exception",
            "statement": "improper gauge transformations with nonzero boundary charge add physical edge degrees",
            "formula": "G_q[epsilon]=int epsilon C_q+Q_q[epsilon]; if delta Q_q != 0 for allowed epsilon, q-edge hair remains",
            "status": "EXACT_GUARD",
            "current_blocker": "Q_q boundary/body neutrality missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DC2311_5_verdict",
            "statement": "degree-count theorem is ready but not activated",
            "formula": "no-pole requires rank(G_q)=N_q plus proper boundary/source neutrality in the same parent branch",
            "status": "DEGREE_COUNT_NOT_PARENT_SIGNED",
            "current_blocker": "Omega, generator, bracket closure, rank, and boundary charge rows",
            "valid_for_claim": "false",
        },
    ]


def build_boundary_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSN2311_0_proper_gauge_charge",
            "channel": "constraint boundary charge",
            "neutrality_condition": "Q_q[epsilon]=0 or exact/proper for all local allowed gauge parameters",
            "why_needed": "otherwise q-removal leaves physical edge modes",
            "current_status": "NOT_SIGNED",
            "source_or_fallback": "QFC2300_5_boundary_charge; QFC2301_5_boundary_charge",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSN2311_1_body_worldtube_charge",
            "channel": "Q_q[body]",
            "neutrality_condition": "source body/worldtube carries no q charge or a sourced absolute bound",
            "why_needed": "exterior vacuum equation can still have nonzero q profile from body matching",
            "current_status": "MISSING_ZERO_THEOREM_OR_BOUND",
            "source_or_fallback": "BCL2297_1_body_charge; JBT2297_3_Qq_body",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSN2311_2_boundary_edge_tail",
            "channel": "Q_q_boundary, Pi_q, edge/corner/reference terms",
            "neutrality_condition": "physical boundary collar has no q edge flux or is bounded in absolute value",
            "why_needed": "compact proper transformations do not automatically cover physical source boundaries",
            "current_status": "MISSING_PHYSICAL_BOUNDARY_RULE",
            "source_or_fallback": "2297 boundary component rows",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSN2311_3_readout_history_projector_tail",
            "channel": "readout/history/projector/counterterm/constants",
            "neutrality_condition": "variation-before-readout, no shadow-source frame, stable projector/domain, fixed constants",
            "why_needed": "post-variation operations can reintroduce effective q source",
            "current_status": "MISSING_TAIL_ZERO_OR_BOUND",
            "source_or_fallback": "JQD2297_4 through JQD2297_8",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSN2311_4_no_cancellation_policy",
            "channel": "total q source/edge vector",
            "neutrality_condition": "each component is theorem-zero or source-backed; no sign cancellation between unknown channels",
            "why_needed": "prevents fitting away the local-GR obstruction",
            "current_status": "POLICY_READY_VALUES_MISSING",
            "source_or_fallback": "JQD2297_9_total_abs_guard",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSN2311_5_verdict",
            "channel": "boundary/source neutrality certificate",
            "neutrality_condition": "BSN2311_0 through BSN2311_4 pass together",
            "why_needed": "no-pole proof needs no residual edge/source hair",
            "current_status": "BOUNDARY_SOURCE_NEUTRALITY_NOT_PROVED",
            "source_or_fallback": "source-backed q body/boundary/tail pack required if proof fails",
            "valid_for_claim": "false",
        },
    ]


def build_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPP2311_0_theorem",
            "proof_step": "no-pole theorem statement",
            "content": "If pi:Y->Y_red is parent-owned, S=S_red∘pi up to proper terms, O=O_red∘pi, q directions are first-class vertical with rank N_q, and q boundary/source charges vanish, then reduced local physics has no q pole.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "claim_effect": "would delete q Green-function and D_qWeyl2 response rows after reduction",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPP2311_1_hessian_kernel",
            "proof_step": "bulk Hessian degeneracy",
            "content": "Since S=S_red∘pi and Dpi[v_q]=0, first and second variations along v_q vanish up to proper boundary terms; the full Hessian has q-vertical null directions before reduction.",
            "status": "EXACT_IF_DESCENT_AND_VERTICALITY_SIGNED",
            "claim_effect": "no physical inverse is taken in q directions",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPP2311_2_reduced_inverse",
            "proof_step": "reduced propagator",
            "content": "The physical Green operator is H_red^{-1} on T(Y_red), not a pseudo-inverse on vertical q directions; therefore it has no q column/source response.",
            "status": "EXACT_IF_DEGREE_COUNT_SIGNED",
            "claim_effect": "no q-mediated fifth-force pole",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPP2311_3_source_silence",
            "proof_step": "matter/readout source annihilation",
            "content": "If matter, clocks, constants, and readouts descend through pi, then source variations pair only with reduced directions and J_q=0 as a theorem, not a fit.",
            "status": "EXACT_IF_MATTER_FUNCTOR_SIGNED",
            "claim_effect": "ordinary matter cannot excite q",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPP2311_4_boundary_silence",
            "proof_step": "edge/source exclusion",
            "content": "If all q boundary/body/source charges are zero or proper, no exterior q profile is set by worldtube matching or edge hair.",
            "status": "EXACT_IF_BSN2311_SIGNED",
            "claim_effect": "bulk no-pole is not spoiled by boundaries",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPP2311_5_current_activation",
            "proof_step": "current MTS activation",
            "content": "The proof cannot be activated because parent Omega, momentum map, bracket closure, degree count, descent, and boundary/source neutrality are not signed together.",
            "status": "NO_POLE_PROOF_NOT_ACTIVATED_CURRENT",
            "claim_effect": "local GR/Newton remains target not claim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPP2311_6_failure_consequence",
            "proof_step": "if proof fails",
            "content": "If any certificate clause remains false in the parent action, q must be treated as independent dynamic or auxiliary and all q coefficients/source projections must enter the bound pack.",
            "status": "FALLBACK_TRIGGER_DEFINED",
            "claim_effect": "prevents smuggling no-pole credit into score runners",
            "valid_for_claim": "false",
        },
    ]


def build_fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FB2311_0_trigger",
            "fallback_input": "fallback branch predicate",
            "required_value": "QRC2311_8 != CERTIFICATE_CLOSED and q not proven auxiliary-only with bounded Schur terms",
            "current_status": "TRIGGER_READY_CERTIFICATE_FAILED",
            "units": "boolean",
            "source_path": "P8_Y5_PARENT_QLOC_2311_REMOVAL_CERTIFICATE_AUDIT.csv",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FB2311_1_Zq",
            "fallback_input": "Z_q",
            "required_value": "signed kinetic Hessian or theorem-zero/auxiliary condition",
            "current_status": "MISSING_PARENT_HESSIAN",
            "units": "action_density_normalization_dependent",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FB2311_2_Mq2_lambda",
            "fallback_input": "M_q^2 and lambda_q",
            "required_value": "M_q^2 in same normalization; lambda_q=sqrt(Z_q/M_q^2) if dynamic massive",
            "current_status": "MISSING_PARENT_HESSIAN",
            "units": "Z_q/length^2 and length",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FB2311_3_DqWeyl2",
            "fallback_input": "D_qWeyl2",
            "required_value": "parent coefficient or theorem-zero from no-spurion/no-pole route",
            "current_status": "MISSING_PARENT_COEFFICIENT",
            "units": "q-action convention dependent",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FB2311_4_Jq_components",
            "fallback_input": "J_q component vector",
            "required_value": "matter, curvature, body, boundary, readout, history, projector, counterterm, constants each theorem-zero or source-backed",
            "current_status": "MISSING_COMPONENT_ZERO_OR_BOUNDS",
            "units": "q Euler-source units",
            "source_path": rel(PATHS["2297_bounds"]),
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FB2311_5_body_boundary_tails",
            "fallback_input": "Q_q[body], Q_q_boundary, Pi_q, tail envelope",
            "required_value": "zero theorem or absolute bound, no sign cancellation",
            "current_status": "MISSING_ZERO_THEOREM_OR_BOUND",
            "units": "source charge / boundary charge",
            "source_path": rel(PATHS["2297_body"]),
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FB2311_6_arena_projection",
            "fallback_input": "R10/PPN/clock/orbital/local-GR projection tensors",
            "required_value": "tau_R10, tau_PPN, tau_clock, tau_orbital, qbar/Qbar/K products in one normalization",
            "current_status": "MISSING_ARENA_PROJECTION",
            "units": "arena dependent",
            "source_path": "MISSING_ARENA_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FB2311_7_claim_gate",
            "fallback_input": "independent q score permission",
            "required_value": "FB2311_1 through FB2311_6 numeric/source-backed or theorem-zero",
            "current_status": "CLAIM_BLOCKED",
            "units": "boolean",
            "source_path": "FB2311_1;FB2311_2;FB2311_3;FB2311_4;FB2311_5;FB2311_6",
            "valid_for_claim": "false",
        },
    ]


def build_decisions() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2311_0_theorem_status",
            "decision": "no-pole theorem is exact conditional but not activated",
            "reason": "the proof is mathematically sharp, but current parent evidence lacks Omega, generator, bracket, degree, descent, and boundary/source neutrality in one branch",
            "next_action": "do not claim local GR/Newton yet",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2311_1_best_derivation_attack",
            "decision": "attack parent Omega/momentum-map source first",
            "reason": "without Omega and G_q the first-class/no-pole route cannot even start; coefficient hunting would be premature",
            "next_action": "look for or construct the q presymplectic potential, Omega, and differentiable generator",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2311_2_boundary_policy",
            "decision": "boundary/source neutrality is promoted to equal priority with bulk degree count",
            "reason": "2297 proves exterior vacuum silence is insufficient if Q_q[body] or edge tails survive",
            "next_action": "every q source/edge channel must be zero-proved or source-bounded",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2311_3_fallback_policy",
            "decision": "fallback source pack is staged but not yet the primary route",
            "reason": "derive-first remains best; fallback becomes mandatory only if parent q removal fails after Omega/generator hunt",
            "next_action": "keep FB2311 rows as nonclaim intake",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2311_4_next",
            "decision": "NEXT_TARGET_SELECTED",
            "reason": "the first missing brick is the parent symplectic certificate; if that cannot be found, switch to bounded independent q source pack",
            "next_action": "2312-Y5-R2FR-parent-q-Omega-momentum-map-generator-or-independent-q-bound-pack.md",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2311_0_sources", "gate": "source paths and needles valid", "passed": "true", "claim_effect": "audit is reproducible", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2311_1_theorem_written", "gate": "exact conditional no-pole theorem and degree count written", "passed": "true", "claim_effect": "math route is precise", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2311_2_parent_Omega", "gate": "parent Omega and generator signed", "passed": "false", "claim_effect": "first-class route cannot activate", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2311_3_degree_count", "gate": "rank/degree count removes q pair", "passed": "false", "claim_effect": "no q pole not proved", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2311_4_boundary_source", "gate": "boundary/source neutrality proved", "passed": "false", "claim_effect": "q edge/source hair remains live", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2311_5_independent_pack", "gate": "fallback source pack score-ready", "passed": "false", "claim_effect": "cannot score independent q branch", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2311_6_local_GR_Newton", "gate": "derived local GR/Newton recovery allowed", "passed": "false", "claim_effect": "still a target, not a result", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2311_0_no_pole_claim", "claim": "q no-pole/local GR branch is proven", "allowed": "false", "reason": "parent certificate fails at Omega/generator/degree/descent/boundary clauses", "blocking_rows": "QRC2311_8_verdict", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2311_1_delete_q_rows", "claim": "delete D_qWeyl2/q source rows now", "allowed": "false", "reason": "q-removal certificate is not activated", "blocking_rows": "NPP2311_5_current_activation", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2311_2_score_fallback", "claim": "score independent q tests now", "allowed": "false", "reason": "fallback pack lacks parent coefficients, source bounds, and arena projections", "blocking_rows": "FB2311_7_claim_gate", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2311_3_exterior_vacuum_only", "claim": "exterior vacuum silence proves local GR", "allowed": "false", "reason": "body/worldtube and boundary charges can set exterior q profile", "blocking_rows": "BSN2311_1_body_worldtube_charge;BSN2311_5_verdict", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2311_0",
            "next_target": "2312-Y5-R2FR-parent-q-Omega-momentum-map-generator-or-independent-q-bound-pack.md",
            "why": "Omega and momentum-map ownership are the first hard gate for first-class/no-pole q removal; without them we must pivot to bounded independent q",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dst in BRANCH_COPY_SPECS:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": rel(src),
                "branch_copy_path": str(dst),
                "copy_exists": b(dst.exists()),
                "row_count": len(read_csv_rows(dst)),
                "valid_for_claim": "false",
            }
        )
    return rows


def validate(
    source_rows: list[dict[str, Any]],
    certificate_rows: list[dict[str, Any]],
    degree_rows: list[dict[str, Any]],
    boundary_rows: list[dict[str, Any]],
    proof_rows: list[dict[str, Any]],
    fallback_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tables = [source_rows, certificate_rows, degree_rows, boundary_rows, proof_rows, fallback_rows, decision_rows, claim_rows, refusal_rows, copy_rows]
    formalization_output_markers = (
        "2311-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_2311",
        "P8_Y5_BRR545_2311",
        "Q_REMOVAL_CERTIFICATE_AUDIT_2311",
        "Q_DEGREE_COUNT_THEOREM_2311",
        "JR2311_",
        "q_independent_Hessian_fallback_pack_nonclaim_2311",
        "Y5_R2FR_parent_q_removal_certificate_degree_count_boundary_neutrality_or_independent_Hessian_source_pack_2311",
    )
    formalization_hits = [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in formalization_output_markers)
    ] if FORMALIZATION.exists() else []

    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2311_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists"))
    checks.append(("VAL2311_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2311_02_certificate_verdict", any(row["row_id"] == "QRC2311_8_verdict" and row["status"] == "CERTIFICATE_NOT_CLOSED_CURRENT" for row in certificate_rows), "q-removal certificate verdict is nonclaim"))
    checks.append(("VAL2311_03_degree_count_theorem", any(row["row_id"] == "DC2311_2_no_q_pole_condition" and "rank(G_q)=N_q" in row["formula"] for row in degree_rows), "degree-count no-pole condition is explicit"))
    checks.append(("VAL2311_04_boundary_neutrality", any(row["row_id"] == "BSN2311_5_verdict" and row["current_status"] == "BOUNDARY_SOURCE_NEUTRALITY_NOT_PROVED" for row in boundary_rows), "boundary/source neutrality remains blocked"))
    checks.append(("VAL2311_05_no_pole_proof_status", any(row["row_id"] == "NPP2311_5_current_activation" and row["status"] == "NO_POLE_PROOF_NOT_ACTIVATED_CURRENT" for row in proof_rows), "no-pole proof not activated"))
    checks.append(("VAL2311_06_fallback_pack", {"FB2311_1_Zq", "FB2311_2_Mq2_lambda", "FB2311_3_DqWeyl2", "FB2311_4_Jq_components", "FB2311_6_arena_projection"}.issubset({row["row_id"] for row in fallback_rows}), "independent q fallback pack staged"))
    checks.append(("VAL2311_07_next_target", any(row["row_id"] == "DEC2311_4_next" and "2312-Y5-R2FR-parent-q-Omega-momentum-map-generator-or-independent-q-bound-pack.md" in row["next_action"] for row in decision_rows), "next target selected"))
    checks.append(("VAL2311_08_claims_blocked", any(row["row_id"] == "CG2311_6_local_GR_Newton" and row["passed"] == "false" for row in claim_rows), "local GR/Newton claim remains blocked"))
    checks.append(("VAL2311_09_refusals_block", all(row["allowed"] == "false" for row in refusal_rows), "refusal runner blocks premature claims"))
    checks.append(("VAL2311_10_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2311_11_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in tables for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2311_12_formalization_untouched_by_2311", len(formalization_hits) == 0, "no 2311 checkpoint output appears in formalization-workbench"))

    rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2311_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2311 proves the no-pole route only as an exact conditional theorem, rejects current activation due missing parent Omega/generator/degree/descent/boundary evidence, and stages the independent q fallback source pack.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    certificate_rows: list[dict[str, Any]],
    degree_rows: list[dict[str, Any]],
    boundary_rows: list[dict[str, Any]],
    proof_rows: list[dict[str, Any]],
    fallback_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2311 — Parent q Removal Certificate: Degree Count And Boundary Neutrality",
        "",
        "## Summary",
        "",
        "2311 gets the no-pole route into its sharp form. The good news: the route is mathematically real. If `q` is a parent-owned quotient/first-class direction, the degree count removes the q canonical pair, the reduced Green operator has no `q` column, and local GR/Newton recovery is cleaner than tuning a scalar.",
        "",
        "The hard news: current MTS does not yet sign the certificate. The missing first brick is not another numeric coefficient; it is the parent presymplectic object and momentum map. Without `Omega_Y`, `G_q`, bracket closure, degree count, action/matter/readout descent, and boundary/source neutrality in one branch, the no-pole theorem stays conditional.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Removal Certificate Audit",
        "",
        md_table(certificate_rows, ["row_id", "certificate_clause", "exact_requirement", "current_evidence", "status", "blocks", "valid_for_claim"]),
        "",
        "## Degree Count Theorem",
        "",
        md_table(degree_rows, ["row_id", "statement", "formula", "status", "current_blocker", "valid_for_claim"]),
        "",
        "## Boundary Source Neutrality",
        "",
        md_table(boundary_rows, ["row_id", "channel", "neutrality_condition", "why_needed", "current_status", "source_or_fallback", "valid_for_claim"]),
        "",
        "## No-Pole Proof Status",
        "",
        md_table(proof_rows, ["row_id", "proof_step", "content", "status", "claim_effect", "valid_for_claim"]),
        "",
        "## Independent Hessian Fallback Pack",
        "",
        md_table(fallback_rows, ["row_id", "fallback_input", "required_value", "current_status", "units", "source_path", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decision_rows, ["row_id", "decision", "reason", "next_action", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        md_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = build_sources()
    certificate_rows = build_certificate_rows()
    degree_rows = build_degree_rows()
    boundary_rows = build_boundary_rows()
    proof_rows = build_proof_rows()
    fallback_rows = build_fallback_rows()
    decision_rows = build_decisions()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["certificate"], certificate_rows)
    write_csv(OUTPUTS["degree"], degree_rows)
    write_csv(OUTPUTS["boundary"], boundary_rows)
    write_csv(OUTPUTS["proof"], proof_rows)
    write_csv(OUTPUTS["fallback"], fallback_rows)
    write_csv(OUTPUTS["decisions"], decision_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(
        source_rows,
        certificate_rows,
        degree_rows,
        boundary_rows,
        proof_rows,
        fallback_rows,
        decision_rows,
        claim_rows,
        refusal_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows)
    write_markdown(
        source_rows,
        certificate_rows,
        degree_rows,
        boundary_rows,
        proof_rows,
        fallback_rows,
        decision_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
        validation_rows,
    )

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2311_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

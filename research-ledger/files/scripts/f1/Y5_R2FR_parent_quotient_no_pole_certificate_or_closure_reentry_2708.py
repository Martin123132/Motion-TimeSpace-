from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2708"
BRANCH_ID = "Y5_R2FR_PARENT_QUOTIENT_NO_POLE_CERTIFICATE_OR_CLOSURE_REENTRY_2708"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "2708-Y5-R2FR-parent-quotient-no-pole-certificate-or-closure-reentry.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2708_SOURCE_REGISTER.csv",
    "certificate_matrix": RESIDUALS / "P8_Y5_R2FR_2708_NO_POLE_CERTIFICATE_MATRIX.csv",
    "conditional_theorem": RESIDUALS / "P8_Y5_R2FR_2708_CONDITIONAL_NO_POLE_SOURCE_ZERO_THEOREM.csv",
    "closure_axiom": RESIDUALS / "P8_Y5_R2FR_2708_LOCAL_GR_REENTRY_CLOSURE_AXIOM.csv",
    "countermodel_guard": RESIDUALS / "P8_Y5_R2FR_2708_COUNTERMODEL_GUARD.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2708_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2708_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2708_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2708_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2708_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_certificate_matrix": LOCAL_BOUNDS / "parent_quotient_no_pole_certificate_matrix_2708_NONCLAIM.csv",
    "local_closure_axiom": LOCAL_BOUNDS / "local_GR_reentry_closure_axiom_2708_NONCLAIM.csv",
    "source_weight_axiom": SOURCE_WEIGHT / "LOCAL_GR_REENTRY_CLOSURE_AXIOM_2708_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2708_MINIMAL_PARENT_ACTION_SIGNATURE_SYNTHESIS_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2708_2707_HANDOFF",
        "relative_path": "2707-Y5-R2FR-parent-action-coefficient-owner-extraction.md",
        "required_needles": ["NEXT2707_0_selected", "TRI2707_B_quotient_no_pole", "CD2707_0_object"],
        "purpose": "imports 2708 no-pole certificate target and closure discipline",
    },
    {
        "source_id": "SRC2708_410_FUNCTOR",
        "relative_path": "410-quotient-matter-functor-theorem-attempt.md",
        "required_needles": ["Conditional Functor Theorem", "quotient_matter_functor_parent_derived", "R0 stays closure_zero"],
        "purpose": "imports earliest quotient-matter functor theorem and failure mode",
    },
    {
        "source_id": "SRC2708_626_DESCENT",
        "relative_path": "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md",
        "required_needles": ["Descent Criterion", "QIM626_0_descent_equivalence", "quotient_invariant_matter_action_signed"],
        "purpose": "imports descent criterion for quotient-invariant matter action",
    },
    {
        "source_id": "SRC2708_2158_PREMISES",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2158_SOURCE_ZERO_PREMISE_GATE.csv",
        "required_needles": ["SPG2158_0_vertical_kernel", "SPG2158_6_boundary_domain_silence", "SPG2158_7_verdict"],
        "purpose": "imports source-zero premise gates",
    },
    {
        "source_id": "SRC2708_2158_IDENTITY",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2158_SOURCE_ZERO_IDENTITY.csv",
        "required_needles": ["SZI2158_2_zero_theorem", "SZI2158_3_not_enough", "SZI2158_4_verdict"],
        "purpose": "imports exact source-zero theorem and counterexample guard",
    },
    {
        "source_id": "SRC2708_1088_SIGNATURE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
        "required_needles": ["MOMS1088_0_action_form", "MOMS1088_6_no_shadow_domain", "MOMS1088_7_verdict"],
        "purpose": "imports minimal ordinary-matter signature clauses",
    },
    {
        "source_id": "SRC2708_1088_THEOREM",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
        "required_needles": ["THM1088_1_visible_fields", "THM1088_5_conclusion", "THM1088_6_current_corpus_verdict"],
        "purpose": "imports conditional qbar_XT/J_matter zero theorem",
    },
    {
        "source_id": "SRC2708_1088_COUNTER",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1088_COUNTERMODEL_RETENTION.csv",
        "required_needles": ["CM1088_0_species_weight", "CM1088_2_shadow_frame", "CM1088_4_boundary_domain_marker"],
        "purpose": "imports retained countermodels",
    },
    {
        "source_id": "SRC2708_991_ROUTE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_991_THEOREM_ROUTE_AUDIT.csv",
        "required_needles": ["HPT991_5_representative_zero_not_enough", "HPT991_6_coupling_descent", "HPT991_7_verdict"],
        "purpose": "prevents representative zero from becoming observed local-GR proof",
    },
    {
        "source_id": "SRC2708_991_CREDIT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_991_REPRESENTATIVE_ZERO_CREDIT_LEDGER.csv",
        "required_needles": ["RZC991_0_representative_vertical_zero", "cannot kill observed boundary/source/readout flux"],
        "purpose": "imports narrow representative-zero credit",
    },
    {
        "source_id": "SRC2708_990_CONTRACT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
        "required_needles": ["PAC990_0_parent_fields_and_quotient", "PAC990_5_Ward_Bianchi", "PAC990_6_PPN_readout"],
        "purpose": "imports parent action and GR/Newton re-entry requirements",
    },
    {
        "source_id": "SRC2708_2106_NO_POLE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2106_NO_POLE_RETURN_LEDGER.csv",
        "required_needles": ["NPR2106_1_no_pole_route", "NPR2106_3_required_certificate", "NPR2106_4_fallback_if_fails"],
        "purpose": "imports no-physical-pole certificate route",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def certificate_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "NPC2708_0_parent_qmap",
            "certificate_clause": "parent quotient map q and observed bundle Q_obs are explicitly owned",
            "mathematical_role": "defines v_X in ker(Dq) and observed geometry/gauge data",
            "current_evidence": "410/626/1088 write the map as a condition; 990 marks parent fields/quotient closure-visible not signed",
            "current_status": "CONDITIONAL_ONLY_NOT_PARENT_SIGNED",
            "blocks_if_missing": "no-pole theorem has no owned quotient object",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "NPC2708_1_vertical_kernel",
            "certificate_clause": "same v_X used in local source rows satisfies Dq[v_X]=0",
            "mathematical_role": "chain-rule zero for observed fields",
            "current_evidence": "SPG2158_0 is conditional only; 1088 visible-field zero is conditional on signature",
            "current_status": "CONDITIONAL_ONLY",
            "blocks_if_missing": "qbar_geom and source-current geometry channels remain live",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "NPC2708_2_action_descent_or_gauge_degeneracy",
            "certificate_clause": "S_parent descends through q or is gauge-degenerate/topological along v_X",
            "mathematical_role": "removes physical local X pole",
            "current_evidence": "NPR2106_1 names route; 991 HPT parent L owner not signed",
            "current_status": "NOT_SIGNED",
            "blocks_if_missing": "Xhat may be a physical finite residual rather than a quotient direction",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "NPC2708_3_degree_count",
            "certificate_clause": "constraint/Hilbert degree count removes Xhat from local propagating spectrum",
            "mathematical_role": "no physical X pole",
            "current_evidence": "2707/2706 identify missing parent degree signature",
            "current_status": "MISSING_DEGREE_COUNT",
            "blocks_if_missing": "finite local pole branch cannot be killed structurally",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "NPC2708_4_matter_MOMS",
            "certificate_clause": "ordinary matter obeys MOMS signature: quotient geometry/gauge data, fixed constants, no species weights, no shadow frame",
            "mathematical_role": "qbar_XT=0 and J_matter=0",
            "current_evidence": "MOMS1088_7 is not derived; THM1088_5 proves zero only under unsigned assumptions",
            "current_status": "CONDITIONAL_THEOREM_NOT_PROMOTED",
            "blocks_if_missing": "species weights, variable constants, shadow frames and material markers survive",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "NPC2708_5_boundary_domain_silence",
            "certificate_clause": "boundary, support, domain selector, projector and non-Hilbert tails are zero or explicitly bounded",
            "mathematical_role": "representative zero becomes observed source/readout zero",
            "current_evidence": "SPG2158_6 missing; RZC991 says representative zero cannot kill observed boundary/source/readout flux",
            "current_status": "MISSING_BOUNDARY_DOMAIN_SILENCE",
            "blocks_if_missing": "observed local source flux can survive quotient language",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "NPC2708_6_Ward_Bianchi",
            "certificate_clause": "hidden/projector/domain/boundary variables are varied, on shell, topological, or retained as residuals",
            "mathematical_role": "conservation-compatible GR/Newton reduction",
            "current_evidence": "PAC990_5 remains open",
            "current_status": "OPEN",
            "blocks_if_missing": "silent Euler leaks can fake local-GR recovery",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "NPC2708_7_GR_readout",
            "certificate_clause": "weak-field observed equations reduce to GR/Newton/PPN after source charge and readout are fixed",
            "mathematical_role": "actual local empirical gate",
            "current_evidence": "PAC990_6 not ready",
            "current_status": "NOT_REACHED",
            "blocks_if_missing": "even a no-pole theorem is not by itself a full local-GR pass",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "NPC2708_8_verdict",
            "certificate_clause": "all clauses close in one parent branch",
            "mathematical_role": "C_X=0 and local no-pole/source-zero route",
            "current_evidence": "no inspected source closes all clauses together",
            "current_status": "CERTIFICATE_NOT_CLOSED",
            "blocks_if_missing": "finite local branch stays closure-only and no local-GR claim is allowed",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def conditional_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM2708_0_assumptions",
            "step": "assume certificate",
            "statement": "Assume q, v_X, action descent/gauge degeneracy, degree count, MOMS matter signature, boundary silence and Ward/Bianchi clauses are all parent-signed in one local branch.",
            "result": "ASSUMPTION_SET_EXACT",
            "claim_status": "conditional_only",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "theorem_id": "THM2708_1_no_pole",
            "step": "remove physical pole",
            "statement": "If S_parent descends through q or is gauge-degenerate along v_X and the local degree count removes v_X from the Hilbert spectrum, then Xhat is not a physical propagating pole.",
            "result": "NO_ACTIVE_X_POLE_IF_CERTIFICATE_SIGNED",
            "claim_status": "conditional_only",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "theorem_id": "THM2708_2_observed_fields",
            "step": "chain-rule observed silence",
            "statement": "Dq[v_X]=0 and observed fields E(q(Phi)), g(q(Phi)), A_obs(q(Phi)) imply Lie_vX observed geometry and gauge data vanish.",
            "result": "OBSERVED_FIELD_VARIATION_ZERO_IF_QMAP_SIGNED",
            "claim_status": "conditional_only",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "theorem_id": "THM2708_3_matter_source_zero",
            "step": "matter variation",
            "statement": "Under MOMS, delta_v S_matter is gauge/EOM/boundary-only with fixed representation constants and no weights/shadow frames, so J_matter=0 and qbar_XT=0.",
            "result": "SOURCE_ZERO_IF_MOMS_SIGNED",
            "claim_status": "conditional_only",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "theorem_id": "THM2708_4_boundary_observed_zero",
            "step": "boundary/domain/readout",
            "statement": "If boundary, support, projector, domain and non-Hilbert tails are zero or retained as bounded residuals, representative zero is allowed to become observed local-source zero.",
            "result": "OBSERVED_ZERO_IF_BOUNDARY_SILENCE_SIGNED",
            "claim_status": "conditional_only",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "theorem_id": "THM2708_5_CX_zero",
            "step": "coupling product",
            "statement": "No physical pole plus J_matter=0/qbar_XT=0/source-boundary silence makes the local C_X channel vanish without choosing small finite coefficients.",
            "result": "C_X_ZERO_IF_FULL_CERTIFICATE_SIGNED",
            "claim_status": "conditional_only",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "theorem_id": "THM2708_6_current_corpus_verdict",
            "step": "compare to current corpus",
            "statement": "The theorem form is exact, but current files supply contracts and countermodel guards rather than a parent-signed certificate.",
            "result": "CONDITIONAL_THEOREM_NOT_PROMOTED",
            "claim_status": "blocked_by_unsigned_certificate",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def closure_axiom_rows() -> list[dict[str, Any]]:
    return [
        {
            "axiom_id": "LGR2708_0_name",
            "axiom_component": "Local GR Re-entry Closure Axiom",
            "exact_requirement": "There exists a parent-owned quotient q:Phi->Q_obs and vertical distribution V=ker(Dq) such that all local non-GR variables in V are gauge, topological, constrained, or explicitly retained residuals.",
            "why_needed": "prevents finite Xhat closure variables from being treated as physical poles and quotient-zero variables at the same time",
            "current_status": "AXIOM_WRITTEN_NOT_ASSUMED_AS_CLAIM",
            "promotion_condition": "derive from a parent action or explicitly label as closure in every local-GR statement",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "axiom_id": "LGR2708_1_action",
            "axiom_component": "Action descent/no-pole",
            "exact_requirement": "S_parent[Phi,Psi]=S_GR[Q_obs,Psi]+S_top[V]+exact_boundary, or delta_v S_parent is pure gauge/constraint for all v in V, with a closed local degree count.",
            "why_needed": "gives no active local X pole rather than a fitted fifth force",
            "current_status": "CLOSURE_AXIOM_ONLY",
            "promotion_condition": "supply explicit L_parent, symplectic/current owner, constraints and degree count",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "axiom_id": "LGR2708_2_matter",
            "axiom_component": "Matter/source descent",
            "exact_requirement": "S_matter=sum_A S_A[Psi_A,E(q(Phi)),Omega(E(q(Phi))),A_obs(q(Phi)),theta_A] with fixed theta_A, no species/source weights, no shadow frames and owned matter lift.",
            "why_needed": "proves J_matter=0 and qbar_XT=0 structurally",
            "current_status": "CLOSURE_AXIOM_ONLY",
            "promotion_condition": "derive MOMS from parent ordinary-matter action",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "axiom_id": "LGR2708_3_boundary",
            "axiom_component": "Boundary/support/readout silence",
            "exact_requirement": "Boundary charge, support shift, projector/source domain and post-variation readout tails vanish by theorem or are retained as source-backed residual bounds.",
            "why_needed": "representative zero cannot otherwise become observed zero",
            "current_status": "CLOSURE_AXIOM_ONLY",
            "promotion_condition": "prove boundary/domain silence or fill absolute residual vector rows",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "axiom_id": "LGR2708_4_conservation",
            "axiom_component": "Ward/Bianchi closure",
            "exact_requirement": "All selectors, boundaries and hidden/projector variables are varied, on shell, topological, or retained so nabla_mu T_total^{mu nu}=0 has no silent Euler leak.",
            "why_needed": "keeps GR/Newton reduction conservation-compatible",
            "current_status": "CLOSURE_AXIOM_ONLY",
            "promotion_condition": "derive Ward/Bianchi identity from parent action with retained residual list",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "axiom_id": "LGR2708_5_empirical_reentry",
            "axiom_component": "GR/Newton/PPN readout",
            "exact_requirement": "After no-pole/source-zero closure, the observed weak-field operator and source charge produce Poisson/Newton and PPN gamma=beta=1, alpha_i=xi=0, no Gdot and no finite-range residue.",
            "why_needed": "no-pole alone is not the full local-GR test pass",
            "current_status": "FUTURE_GATE",
            "promotion_condition": "derive weak-field source charge and PPN vector after the closure theorem is signed",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "axiom_id": "LGR2708_6_usage_rule",
            "axiom_component": "allowed language",
            "exact_requirement": "Until derived, say 'local GR route requires LGR2708 closure axiom' or 'finite branch is closure-only'; never say the local branch reduces to GR/Newton.",
            "why_needed": "prevents hidden overclaim and branch mixing",
            "current_status": "ACTIVE_PRIVATE_RULE",
            "promotion_condition": "replace by parent-signed theorem and validation gate",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def countermodel_guard_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM2708_0_species_weight",
            "legal_without_certificate": "S_matter -> sum_A w_A(X) S_A",
            "damage": "visible geometry descends but material source current is nonzero",
            "killed_by": "MOMS no species/source weights",
            "current_status": "RETAINED",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "countermodel_id": "CM2708_1_variable_constants",
            "legal_without_certificate": "theta_A(X) changes masses, charges, alpha_EM or clock constants",
            "damage": "qbar_XT survives through constants even if geometry descends",
            "killed_by": "constant superselection or retained finite residuals",
            "current_status": "RETAINED",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "countermodel_id": "CM2708_2_shadow_frame",
            "legal_without_certificate": "matter sees A_A(X)^2 g_obs or disformal/source-only metric data",
            "damage": "local fifth-force/WEP residual hides outside quotient coframe",
            "killed_by": "no shadow frame/domain axiom",
            "current_status": "RETAINED",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "countermodel_id": "CM2708_3_boundary_domain",
            "legal_without_certificate": "source support, boundary charge, projector or domain selector shifts under v_X",
            "damage": "representative zero does not imply observed source/readout zero",
            "killed_by": "boundary/support/domain silence or absolute residual bounds",
            "current_status": "RETAINED",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "countermodel_id": "CM2708_4_representative_zero_overcredit",
            "legal_without_certificate": "v_X is representative-zero but observed source/readout flux remains",
            "damage": "fake local-GR proof from quotient language alone",
            "killed_by": "observed boundary/source/readout descent",
            "current_status": "RETAINED_BY_991_GUARD",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG2708_0_certificate",
            "gate": "parent no-pole/source-zero certificate closes",
            "status": "FAIL_CERTIFICATE_NOT_CLOSED",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "q-map, action descent, degree count, MOMS, boundary and Ward/Bianchi clauses are not signed together",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2708_1_conditional_theorem",
            "gate": "conditional no-pole theorem is written",
            "status": "PASS_CONDITIONAL_NONCLAIM",
            "gate_passed": "true",
            "claim_allowed": "false",
            "reason": "the theorem is exact only under unsigned certificate assumptions",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2708_2_closure_axiom",
            "gate": "exact local-GR re-entry closure axiom written",
            "status": "PASS_NONCLAIM_AXIOM",
            "gate_passed": "true",
            "claim_allowed": "false",
            "reason": "closure axiom is explicit and not promoted as proof",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2708_3_finite_branch",
            "gate": "finite Xhat branch may be evidence",
            "status": "BLOCKED_CLOSURE_ONLY",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "2707 demotion remains in force",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2708_4_private",
            "gate": "GitHub/public action",
            "status": "PRIVATE_NO_ACTION",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "private checkpoint only",
            "timestamp_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2708_0_certificate",
            "decision": "NO_POLE_CERTIFICATE_NOT_CLOSED",
            "rationale": "the exact clauses are known, but current corpus still provides contracts/countermodel guards rather than one parent-signed branch",
            "next_action": "do not promote C_X=0 or local GR/Newton",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2708_1_axiom",
            "decision": "LOCAL_GR_REENTRY_CLOSURE_AXIOM_WRITTEN",
            "rationale": "if we cannot derive it yet, the axiom must be explicit so future work cannot smuggle it in",
            "next_action": "try to construct or falsify a minimal parent action signature satisfying the axiom",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2708_2_next",
            "decision": "MINIMAL_PARENT_ACTION_SIGNATURE_SYNTHESIS_NEXT",
            "rationale": "the only real leap forward is to propose a parent action/signature and test it against the no-pole certificate clauses",
            "next_action": "2709 minimal parent action signature synthesis or closure axiom falsification",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2708_0_selected",
            "selection": "selected_primary",
            "target_doc": "2709-Y5-R2FR-minimal-parent-action-signature-synthesis-or-closure-falsification.md",
            "target_script": "scripts/Y5_R2FR_minimal_parent_action_signature_synthesis_or_closure_falsification_2709.py",
            "task": "attempt to construct the minimal parent action/signature that satisfies LGR2708: quotient q, no-pole action descent, MOMS matter functor, boundary silence, Ward/Bianchi retention and GR/Newton weak-field re-entry; if any clause contradicts current MTS structure, record the falsifier and keep the closure axiom explicit",
            "success_condition": "one parent-action signature candidate passes the clause audit as a theorem target, or a specific clause is falsified/demoted with no hidden local-GR claim",
            "forbidden_shortcuts": "adopt LGR2708 as proof; borrow representative zero as observed zero; add fitted finite coefficients; GitHub action; formalization-workbench edits",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS2708_0_no_pole",
            "topic": "no-pole/source-zero route",
            "status": "CONDITIONAL_THEOREM_NOT_PROMOTED",
            "meaning": "the structural GR-like route is mathematically shaped but not parent-signed",
            "next_action": "construct/falsify minimal parent action signature",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2708_1_closure",
            "topic": "local-GR re-entry closure",
            "status": "EXACT_AXIOM_WRITTEN",
            "meaning": "future work has a precise closure axiom instead of a foggy plateau",
            "next_action": "derive or falsify axiom clauses",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2708_2_finite_branch",
            "topic": "finite local Xhat branch",
            "status": "CLOSURE_ONLY_REAFFIRMED",
            "meaning": "no finite local coefficient is evidence until re-entered by parent theorem or source row",
            "next_action": "do not run local empirical scores yet",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2708_3_private",
            "topic": "public/GitHub",
            "status": "NO_ACTION_PRIVATE",
            "meaning": "all artifacts remain private in post-checkpoint-work",
            "next_action": "keep private",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": key,
            "path": str(path),
            "relative_path": str(path.relative_to(ROOT)),
            "exists_after_run": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for key, path in BRANCH_OUTPUTS.items()
    ]


def validate(generated_paths: dict[str, Path], rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "passed": as_bool(passed), "detail": detail, "timestamp_utc": stamp()})

    sources = rows_by_name["source_register"]
    add("VAL2708_0_sources_exist", all(row["exists"] == "true" for row in sources), "all cited local source paths exist")
    add("VAL2708_1_needles_found", all(not row["missing_needles"] for row in sources), "all required source needles were found")

    matrix = rows_by_name["certificate_matrix"]
    add("VAL2708_2_certificate_verdict_present", any(row["clause_id"] == "NPC2708_8_verdict" and row["current_status"] == "CERTIFICATE_NOT_CLOSED" for row in matrix), "no-pole certificate verdict is present and blocked")
    add("VAL2708_3_certificate_nonclaim", all(row["claim_pass"] == "false" and row["valid_for_claim"] == "false" for row in matrix), "all certificate clauses remain nonclaim")

    theorem = rows_by_name["conditional_theorem"]
    add("VAL2708_4_conditional_CX_zero_written", any(row["theorem_id"] == "THM2708_5_CX_zero" for row in theorem), "conditional C_X zero theorem step written")
    add("VAL2708_5_theorem_not_promoted", all(row["valid_for_claim"] == "false" for row in theorem), "conditional theorem is not promoted")

    axiom = rows_by_name["closure_axiom"]
    add("VAL2708_6_closure_axiom_written", any(row["axiom_id"] == "LGR2708_0_name" for row in axiom), "local-GR re-entry closure axiom written")
    add("VAL2708_7_usage_rule_present", any(row["axiom_id"] == "LGR2708_6_usage_rule" for row in axiom), "allowed-language usage rule present")

    counters = rows_by_name["countermodel_guard"]
    add("VAL2708_8_countermodels_retained", len(counters) >= 5 and all(row["current_status"].startswith("RETAINED") for row in counters), "countermodels are retained")
    add("VAL2708_9_claims_blocked", all(row["claim_allowed"] == "false" for row in rows_by_name["claim_gates"]), "all claim gates keep claim_allowed=false")
    add("VAL2708_10_next_2709", any(row["next_id"] == "NEXT2708_0_selected" and "2709" in row["target_doc"] for row in rows_by_name["next_target"]), "2709 target selected")
    add("VAL2708_11_no_formalization_outputs", not any("formalization-workbench" in str(path).lower() for path in generated_paths.values()), "no output path points into formalization-workbench")
    add("VAL2708_12_no_github_outputs", not any(".git" in str(path).lower() or "github" in str(path).lower() for path in generated_paths.values()), "no GitHub/public-output path was written")

    for key, path in generated_paths.items():
        ok, count, detail = parse_csv(path)
        add(f"VAL2708_PARSE_{key}", ok and count > 0, f"{detail}; rows={count}")

    core = [row for row in rows if not row["check_id"].startswith("VAL2708_PARSE_validation")]
    add(
        "VAL2708_OVERALL",
        all(row["passed"] == "true" for row in core),
        "2708 writes the conditional no-pole/source-zero theorem, keeps it nonclaim, records the exact local-GR re-entry closure axiom, and selects minimal parent-action signature synthesis for 2709",
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        ("No-Pole Certificate Matrix", rows_by_name["certificate_matrix"]),
        ("Conditional No-Pole Source-Zero Theorem", rows_by_name["conditional_theorem"]),
        ("Local GR Re-Entry Closure Axiom", rows_by_name["closure_axiom"]),
        ("Countermodel Guard", rows_by_name["countermodel_guard"]),
        ("Source Register", rows_by_name["source_register"]),
        ("Claim Gates", rows_by_name["claim_gates"]),
        ("Decisions", rows_by_name["decision_ledger"]),
        ("Next Target", rows_by_name["next_target"]),
        ("Project Status", rows_by_name["project_status"]),
        ("Validation", rows_by_name["validation"]),
    ]
    lines = [
        "# 2708: Parent Quotient No-Pole Certificate Or Closure Re-Entry",
        "",
        f"**Branch:** `{BRANCH_ID}`",
        "",
        "## Private Verdict",
        "",
        "2708 gets the no-pole/source-zero route into its cleanest form. If a parent action signs the quotient map, vertical kernel, action descent or gauge degeneracy, degree count, MOMS matter signature, boundary/domain silence, and Ward/Bianchi retention, then the local `Xhat` pole is not physical and the `C_X` channel is zero without fitted small couplings. Current corpus does not sign those clauses together, so no local-GR/Newton claim is promoted. The gain is that the required local-GR re-entry closure axiom is now exact and visible.",
        "",
        "## Bottom Line",
        "",
        "- Conditional theorem: sharp and GR-like, but not parent-signed.",
        "- Closure axiom: now explicit, so it cannot be smuggled into evidence language.",
        "- Finite branch: still closure-only after 2707.",
        "- Best next move: 2709 tries to construct or falsify a minimal parent action signature satisfying the axiom.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "certificate_matrix": certificate_matrix_rows(),
        "conditional_theorem": conditional_theorem_rows(),
        "closure_axiom": closure_axiom_rows(),
        "countermodel_guard": countermodel_guard_rows(),
        "claim_gates": claim_gate_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }

    for name, path in OUTPUTS.items():
        if name in {"validation", "branch_copies"}:
            continue
        write_csv(path, rows_by_name[name])

    write_csv(BRANCH_OUTPUTS["local_certificate_matrix"], rows_by_name["certificate_matrix"])
    write_csv(BRANCH_OUTPUTS["local_closure_axiom"], rows_by_name["closure_axiom"])
    write_csv(BRANCH_OUTPUTS["source_weight_axiom"], rows_by_name["closure_axiom"])
    write_csv(BRANCH_OUTPUTS["rab_next"], rows_by_name["next_target"])

    branch_rows = branch_copy_rows()
    rows_by_name["branch_copies"] = branch_rows
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    generated_paths = {name: path for name, path in OUTPUTS.items() if name != "validation"}
    generated_paths.update(BRANCH_OUTPUTS)
    validation = validate(generated_paths, rows_by_name)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)

    write_doc(rows_by_name)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

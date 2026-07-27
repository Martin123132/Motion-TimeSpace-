from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_Q_BRANCH_SELECTION_NO_POLE_OR_Q_HESSIAN_2310"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2310-Y5-R2FR-q-branch-selection-no-pole-or-independent-Hessian-first-source-row.md"

PATHS = {
    "2309_doc": ROOT / "2309-Y5-R2FR-q-X-operator-identity-bridge-or-independent-q-Hessian.md",
    "2309_validation": OUT / "P8_Y5_BRR545_2309_VALIDATION.csv",
    "2309_trichotomy": OUT / "P8_Y5_PARENT_QLOC_2309_QX_TRICHOTOMY_THEOREM.csv",
    "2309_bridge": OUT / "P8_Y5_PARENT_QLOC_2309_QX_BRIDGE_SIGNATURE_ATTEMPT.csv",
    "2309_independent": OUT / "P8_Y5_PARENT_QLOC_2309_INDEPENDENT_Q_HESSIAN_ROW.csv",
    "2309_refusal": OUT / "P8_Y5_PARENT_QLOC_2309_REFUSAL_RUNNER.csv",
    "2308_normal": OUT / "P8_Y5_PARENT_QLOC_2308_Q_LOCAL_ACTION_NORMAL_FORM_CONTRACT.csv",
    "2301_rep": OUT / "P8_Y5_PARENT_QLOC_2301_Q_REPRESENTATION_TYPE_GATE.csv",
    "2301_firstclass": OUT / "P8_Y5_PARENT_QLOC_2301_Q_FIRSTCLASS_REMOVAL_ATTEMPT.csv",
    "637_qmap": OUT / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv",
    "1023_doc": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
    "1157_doc": ROOT / "1157-Y5-R10-parent-q-map-null-generator-proof-or-cg-bound-first-fill.md",
    "2302_doc": ROOT / "2302-Y5-R2FR-q-representation-or-firstclass-certificate-or-BqWeyl-bound-row.md",
}

SOURCES = [
    ("SRC2310_00_2309_doc", "2309_doc", PATHS["2309_doc"], ["TRI2309_4_verdict", "BRANCH_SELECTION_NOT_PARENT_SIGNED", "NEXT2309_0"], "direct 2309 handoff"),
    ("SRC2310_01_2309_validation", "2309_validation", PATHS["2309_validation"], ["VAL2309_OVERALL", "PASS"], "2309 validation"),
    ("SRC2310_02_2309_trichotomy", "2309_trichotomy", PATHS["2309_trichotomy"], ["TRI2309_0_quotient_vertical_case", "TRI2309_2_independent_q_case"], "q branch trichotomy"),
    ("SRC2310_03_2309_bridge", "2309_bridge", PATHS["2309_bridge"], ["BR2309_4_verdict", "QX_BRIDGE_NOT_ACTIVATED"], "q=aX bridge blocked"),
    ("SRC2310_04_2309_independent", "2309_independent", PATHS["2309_independent"], ["IQH2309_4_claim_gate", "CLAIM_BLOCKED"], "independent q Hessian missing"),
    ("SRC2310_05_2309_refusal", "2309_refusal", PATHS["2309_refusal"], ["REF2309_1_treat_vertical_as_physical", "false"], "no mixing vertical and propagating q"),
    ("SRC2310_06_2308_normal", "2308_normal", PATHS["2308_normal"], ["NF2308_3_no_pole", "BETTER_GR_ROUTE_NOT_SIGNED"], "no-pole alternative from q action contract"),
    ("SRC2310_07_2301_rep", "2301_rep", PATHS["2301_rep"], ["QREP2301_5_verdict", "FAIL_CURRENT_CLAIM"], "q representation not signed"),
    ("SRC2310_08_2301_firstclass", "2301_firstclass", PATHS["2301_firstclass"], ["QFC2301_6_verdict", "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED"], "first-class removal not proven"),
    ("SRC2310_09_637_qmap", "637_qmap", PATHS["637_qmap"], ["QM637_2_vertical_kernel", "Dq[v_X]=0"], "conditional vertical-kernel theorem"),
    ("SRC2310_10_1023_doc", "1023_doc", PATHS["1023_doc"], ["QVC1023_8_verdict", "fail_current_claim_demote_current_branch"], "single q/vX/action certificate failed"),
    ("SRC2310_11_1157_doc", "1157_doc", PATHS["1157_doc"], ["QMAP1157_8_verdict", "PARENT_Q_MAP_NULL_GENERATOR_NOT_DERIVED"], "parent q map/null-generator proof missing"),
    ("SRC2310_12_2302_doc", "2302_doc", PATHS["2302_doc"], ["EVID2302_2_firstclass_package", "CLEANEST_ROUTE_BUT_UNSIGNED"], "first-class route is cleanest but unsigned"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2310_SOURCE_REGISTER.csv",
    "scorecard": OUT / "P8_Y5_PARENT_QLOC_2310_BRANCH_SELECTION_SCORECARD.csv",
    "no_pole": OUT / "P8_Y5_PARENT_QLOC_2310_NO_POLE_THEOREM_GATE.csv",
    "independent": OUT / "P8_Y5_PARENT_QLOC_2310_INDEPENDENT_Q_FIRST_SOURCE_ROW.csv",
    "auxiliary": OUT / "P8_Y5_PARENT_QLOC_2310_AUXILIARY_Q_SCHUR_ROUTE.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2310_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2310_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2310_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2310_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2310_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2310_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2310_0_scorecard", OUTPUTS["scorecard"], RAB_QUEUE / "JR2310_Q_BRANCH_SELECTION_SCORECARD_NONCLAIM.csv"),
    ("COPY2310_1_no_pole", OUTPUTS["no_pole"], BETA_DOCS / "Q_NO_POLE_THEOREM_GATE_2310_NONCLAIM.csv"),
    ("COPY2310_2_independent_q", OUTPUTS["independent"], MICRO_RESIDUALS / "q_independent_first_source_row_nonclaim_2310.csv"),
    ("COPY2310_3_auxiliary_q", OUTPUTS["auxiliary"], RAB_QUEUE / "JR2310_AUXILIARY_Q_SCHUR_ROUTE_NONCLAIM.csv"),
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
        vals = []
        for field in fields:
            vals.append(str(row.get(field, "")).replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
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


def build_scorecard() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSEL2310_0_no_pole_quotient",
            "candidate_branch": "q quotient/first-class/no-pole removal",
            "physics_payoff": "cleanest local GR/Newton recovery: no extra propagating scalar and no q-mediated fifth force",
            "current_support": "conditional quotient spine exists in 637/1023/1157/2302 and 2308 flags this as the better GR route",
            "current_blocker": "q object, actual vertical generator, first-class algebra, degree count, matter descent, boundary/source neutrality",
            "selection": "SELECT_AS_PRIMARY_DERIVATION_ROUTE_NOT_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSEL2310_1_q_equals_X_bridge",
            "candidate_branch": "q=aX physical-identity bridge",
            "physics_payoff": "would reuse X operator laws by exact pullback",
            "current_support": "2309 writes exact pullback laws",
            "current_blocker": "q=aX, scale a, shared domain, X values, and source convention are not signed",
            "selection": "REJECT_AS_CURRENT_ROUTE_KEEP_FORMULAS_ONLY",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSEL2310_2_independent_dynamic_q",
            "candidate_branch": "independent propagating q Hessian",
            "physics_payoff": "honest fallback if q is physical; can be bounded by R10/PPN/clock/orbital arenas",
            "current_support": "2308 minimal q action contract and 2309 independent q row",
            "current_blocker": "Z_q, M_q^2, D_qWeyl2, J_q/boundary tail, and arena projections are missing",
            "selection": "STAGE_AS_FALLBACK_FIRST_SOURCE_ROW_NOT_PRIMARY",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSEL2310_3_auxiliary_q",
            "candidate_branch": "auxiliary/algebraic q Schur-complement branch",
            "physics_payoff": "no q wave pole, but leaves higher-curvature contact operators that still need bounds",
            "current_support": "2309 keeps auxiliary q as live countermodel",
            "current_blocker": "algebraic Hessian, source vector, sign, and no-tower theorem are not sourced",
            "selection": "LIVE_FALLBACK_COUNTERMODEL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BSEL2310_4_verdict",
            "candidate_branch": "working branch selection",
            "physics_payoff": "least-scrutiny path is to prove q is removed before local physics; if it fails, source independent q honestly",
            "current_support": "conditional no-pole theorem and fallback source rows are both now explicit",
            "current_blocker": "primary branch is not claim-grade until a single parent certificate signs all no-pole clauses",
            "selection": "PRIMARY_NO_POLE_DERIVATION_SELECTED_FALLBACK_Q_HESSIAN_STAGED",
            "valid_for_claim": "false",
        },
    ]


def build_no_pole_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NP2310_0_theorem_statement",
            "clause": "conditional no-pole theorem",
            "required_evidence": "parent quotient pi, first-class generator, action/matter/readout descent, degree count, and boundary/source neutrality",
            "mathematical_content": "if S=S_red∘pi, O=O_red∘pi, e_q is vertical/first-class, and all q boundary/source charges vanish, then the reduced propagator G_red=H_red^{-1} has no q column and no q pole",
            "current_status": "CONDITIONAL_THEOREM_WRITTEN",
            "missing_piece": "all clauses must be signed in one parent branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NP2310_1_parent_quotient_object",
            "clause": "q is a real parent quotient/readout object",
            "required_evidence": "q(Phi) or pi: Y -> Y_red with domain and units, not an after-the-fact label",
            "mathematical_content": "q must define the reduced coordinates before variation",
            "current_status": "NOT_SIGNED",
            "missing_piece": "QREP2301_5_verdict and QMAP1157_8_verdict remain failed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NP2310_2_actual_vertical_generator",
            "clause": "the actual local q/X direction is vertical",
            "required_evidence": "Dq[v_X]=0 for the physical local direction, not only for an abstract null orbit",
            "mathematical_content": "vertical directions are killed by pi and cannot be treated as propagating q modes",
            "current_status": "CONDITIONAL_ONLY",
            "missing_piece": "QM637_2 is conditional; 1157 says local Xhat may still be physical residual",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NP2310_3_firstclass_degree_count",
            "clause": "first-class generator removes the q canonical pair",
            "required_evidence": "Omega, momentum map, bracket closure, and degree count in one parent symplectic package",
            "mathematical_content": "the physical inverse Hessian is computed on the quotient, not on a gauge-degenerate full Hessian",
            "current_status": "NOT_SIGNED",
            "missing_piece": "QFC2301_0 through QFC2301_3 are missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NP2310_4_action_matter_readout_descent",
            "clause": "bulk, matter, clocks, constants, and readouts descend",
            "required_evidence": "S_bulk=S_red∘pi plus matter/readout functor with no q markers or hidden frame leak",
            "mathematical_content": "if observables and matter descend, source variations annihilate vertical q directions",
            "current_status": "NOT_SIGNED",
            "missing_piece": "1023 records action, matter/no-marker, and hidden channel descent as conditional or missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NP2310_5_boundary_source_neutrality",
            "clause": "boundary/body q charges and tails vanish or are proper gauge",
            "required_evidence": "Q_q[body], edge cocycles, boundary primitive, and local projector tails are zero/proper",
            "mathematical_content": "bulk quotient silence is not enough if source worldtubes or boundary hair set exterior q data",
            "current_status": "NOT_SIGNED",
            "missing_piece": "2301/2302/1023/1157 keep boundary and source neutrality open",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NP2310_6_activation_verdict",
            "clause": "activate q no-pole branch",
            "required_evidence": "NP2310_1 through NP2310_5 all pass together",
            "mathematical_content": "D_qWeyl2 and q Green-function rows are deleted after reduction rather than fitted",
            "current_status": "NO_POLE_NOT_ACTIVATED_CURRENT",
            "missing_piece": "single parent certificate",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NP2310_7_local_GR_payoff",
            "clause": "why this is the primary route",
            "required_evidence": "no-pole theorem activation",
            "mathematical_content": "if activated, local GR/Newton recovery is cleaner than tuning a light q scalar because there is no local q-mediated residual to suppress",
            "current_status": "PRIMARY_ROUTE_FOR_DERIVATION_NOT_EVIDENCE",
            "missing_piece": "same as NP2310_6",
            "valid_for_claim": "false",
        },
    ]


def build_independent_q_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "IQSRC2310_0_branch_precondition",
            "input": "branch predicate",
            "meaning": "use independent q only if no-pole/quotient removal and q=aX bridge both fail",
            "required_source_or_formula": "not(NP2310 activated) and not(BR2309 activated)",
            "units": "boolean",
            "current_status": "FALLBACK_ONLY",
            "source_path": rel(PATHS["2309_doc"]),
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IQSRC2310_1_Zq",
            "input": "Z_q",
            "meaning": "q kinetic Hessian sign and normalization",
            "required_source_or_formula": "delta_q^2 S_parent contains 1/2 Z_q (nabla q)^2 in the same q units",
            "units": "action_density_normalization_dependent",
            "current_status": "MISSING_PARENT_HESSIAN",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IQSRC2310_2_Mq2_lambda",
            "input": "M_q^2 and lambda_q",
            "meaning": "q mass/gap and finite range",
            "required_source_or_formula": "lambda_q=sqrt(Z_q/M_q^2) if Z_q>0 and M_q^2>0; massless branch needs separate domain/no-hair theorem",
            "units": "M_q^2 matches Z_q/length^2",
            "current_status": "MISSING_PARENT_HESSIAN",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IQSRC2310_3_DqWeyl2",
            "input": "D_qWeyl2",
            "meaning": "q coupling to C_abcd C^abcd in the same action convention",
            "required_source_or_formula": "parent action coefficient in S_q or theorem-zero from no-pole/no-spurion route",
            "units": "chosen so D_qWeyl2 q C^2 has action density units",
            "current_status": "MISSING_PARENT_COEFFICIENT",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IQSRC2310_4_Jq_boundary_tail",
            "input": "J_q plus boundary/source tail",
            "meaning": "ordinary matter, body, clock, coframe, and boundary q source",
            "required_source_or_formula": "matter descent source-zero proof or absolute bound rows for all source channels",
            "units": "same as q Euler-equation source",
            "current_status": "MISSING_SOURCE_ZERO_OR_BOUND",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IQSRC2310_5_arena_projection",
            "input": "P_arena, qbar, Qbar, K products",
            "meaning": "observable projection into R10, PPN, clocks, orbital systems, and local GR residual vector",
            "required_source_or_formula": "arena-specific projection law with no-cancellation envelope",
            "units": "arena_dependent",
            "current_status": "MISSING_ARENA_PROJECTION",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IQSRC2310_6_claim_gate",
            "input": "independent q branch promotion",
            "meaning": "independent q can be scored only after IQSRC2310_1 through IQSRC2310_5 are sourced",
            "required_source_or_formula": "all rows numeric/source-backed or theorem-zero",
            "units": "boolean",
            "current_status": "CLAIM_BLOCKED",
            "source_path": "IQSRC2310_1;IQSRC2310_2;IQSRC2310_3;IQSRC2310_4;IQSRC2310_5",
            "valid_for_claim": "false",
        },
    ]


def build_auxiliary_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "AUX2310_0_predicate",
            "case": "Z_q=0 algebraic/auxiliary q",
            "formula": "M_q^2 q + D_qWeyl2 C^2 + J_q + boundary_tail = 0",
            "consequence": "no propagating q pole, but q can generate contact/higher-curvature terms",
            "status": "LIVE_COUNTERMODEL_NOT_SELECTED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "AUX2310_1_schur_effective_action",
            "case": "integrate out auxiliary q",
            "formula": "q=-(D_qWeyl2 C^2+J_q+tail)/M_q^2; Delta S_eff ~ -1/(2 M_q^2)(D_qWeyl2 C^2+J_q+tail)^2",
            "consequence": "Weyl-squared source becomes a higher-curvature/contact operator, not a Yukawa force",
            "status": "EXACT_CONDITIONAL_FORMULA",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "AUX2310_2_missing_inputs",
            "case": "source requirements",
            "formula": "need M_q^2, D_qWeyl2, J_q, boundary_tail, sign, and cutoff/domain",
            "consequence": "cannot use auxiliary branch to claim local GR until contact operators are zeroed or bounded",
            "status": "MISSING_PARENT_INPUTS",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "AUX2310_3_role",
            "case": "workflow role",
            "formula": "if no-pole fails and Z_q is source-zero while M_q^2 survives, switch to Schur-complement bound route",
            "consequence": "keeps an escape route without pretending q propagates",
            "status": "FALLBACK_AFTER_NO_POLE_OR_DYNAMIC_Q_DECISION",
            "valid_for_claim": "false",
        },
    ]


def build_decisions() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2310_0_primary_route",
            "decision": "select no-pole/quotient removal as the primary derivation route",
            "reason": "it is the least-scrutiny path to derived local GR/Newton because it removes the local q pole rather than tuning a new scalar force",
            "next_action": "prove the parent q-removal certificate clauses, not fit q coefficients first",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2310_1_claim_status",
            "decision": "do not activate the no-pole claim",
            "reason": "the current corpus lacks the one-branch parent certificate: quotient object, vertical generator, first-class degree count, action/matter descent, boundary/source neutrality",
            "next_action": "treat no-pole as theorem target only",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2310_2_fallback",
            "decision": "stage independent q Hessian first-source rows",
            "reason": "if q is physical, every local test must use Z_q, M_q^2, D_qWeyl2, J_q, and arena projection from the same normalization",
            "next_action": "fill source rows only if parent q-removal certificate fails",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2310_3_q_equals_X",
            "decision": "do not use q=aX bridge as current route",
            "reason": "2309 blocks the bridge; formulas remain available but inactive",
            "next_action": "avoid copying X/L_X values into q runners",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2310_4_next",
            "decision": "NEXT_TARGET_SELECTED",
            "reason": "the next useful leap is a parent q-removal certificate with explicit degree count and boundary/source neutrality; if it fails, immediately convert IQSRC2310 rows into a bound pack",
            "next_action": "2311-Y5-R2FR-parent-q-removal-certificate-degree-count-boundary-neutrality-or-independent-Hessian-source-pack.md",
            "valid_for_claim": "false",
        },
    ]


def build_claim_gates() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2310_0_sources", "gate": "all source paths and needles valid", "passed": "true", "claim_effect": "ledger is checkable", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2310_1_branch_selection", "gate": "primary route selected for derivation", "passed": "true", "claim_effect": "workflow is no longer ambiguous", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2310_2_no_pole_activation", "gate": "no-pole theorem parent-signed", "passed": "false", "claim_effect": "cannot claim q local residual vanishes", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2310_3_independent_q_inputs", "gate": "independent q Hessian source-backed", "passed": "false", "claim_effect": "cannot run q local PPN/R10 score", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2310_4_local_GR_Newton", "gate": "derived local GR/Newton recovery allowed", "passed": "false", "claim_effect": "still a derivation target, not a result", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2310_5_public_update", "gate": "GitHub/public update recommended from this checkpoint", "passed": "false", "claim_effect": "keep private until no-pole certificate or fallback source pack is cleaner", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2310_0_claim_no_pole", "claim": "q no-pole/local GR branch is proven", "allowed": "false", "reason": "NP2310_1 through NP2310_5 are not signed together", "blocking_rows": "NP2310_6_activation_verdict", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2310_1_fit_q_scalar_now", "claim": "run independent q scalar PPN/R10 fits now", "allowed": "false", "reason": "IQSRC2310 source rows are missing and branch is fallback only", "blocking_rows": "IQSRC2310_6_claim_gate", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2310_2_copy_X_operator", "claim": "copy X/L_X into q branch", "allowed": "false", "reason": "q=aX bridge remains blocked by 2309", "blocking_rows": "BSEL2310_1_q_equals_X_bridge", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2310_3_public_push", "claim": "publish this as a completed local-GR proof", "allowed": "false", "reason": "checkpoint is a private route decision and source contract, not a proof", "blocking_rows": "CG2310_4_local_GR_Newton;CG2310_5_public_update", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2310_0",
            "next_target": "2311-Y5-R2FR-parent-q-removal-certificate-degree-count-boundary-neutrality-or-independent-Hessian-source-pack.md",
            "why": "prove q removal/no-pole first because it is the clean GR path; if any certificate clause fails, immediately switch to source-backed independent q Hessian/bound pack",
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
    score_rows: list[dict[str, Any]],
    no_pole_rows: list[dict[str, Any]],
    independent_rows: list[dict[str, Any]],
    auxiliary_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tables = [source_rows, score_rows, no_pole_rows, independent_rows, auxiliary_rows, decision_rows, claim_rows, refusal_rows, copy_rows]
    formalization_output_markers = (
        "2310-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_2310",
        "P8_Y5_BRR545_2310",
        "JR2310_",
        "Q_NO_POLE_THEOREM_GATE_2310",
        "q_independent_first_source_row_nonclaim_2310",
        "Y5_R2FR_q_branch_selection_no_pole_or_independent_Hessian_first_source_row_2310",
    )
    formalization_hits = [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in formalization_output_markers)
    ] if FORMALIZATION.exists() else []

    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2310_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists"))
    checks.append(("VAL2310_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2310_02_primary_route_selected", any(row["row_id"] == "BSEL2310_4_verdict" and row["selection"] == "PRIMARY_NO_POLE_DERIVATION_SELECTED_FALLBACK_Q_HESSIAN_STAGED" for row in score_rows), "primary no-pole derivation route selected with fallback staged"))
    checks.append(("VAL2310_03_no_pole_theorem_written", any(row["row_id"] == "NP2310_0_theorem_statement" and "G_red=H_red^{-1} has no q column" in row["mathematical_content"] for row in no_pole_rows), "conditional no-pole theorem is explicit"))
    checks.append(("VAL2310_04_no_pole_not_activated", any(row["row_id"] == "NP2310_6_activation_verdict" and row["current_status"] == "NO_POLE_NOT_ACTIVATED_CURRENT" for row in no_pole_rows), "no-pole claim remains blocked"))
    checks.append(("VAL2310_05_independent_q_first_rows", {"IQSRC2310_1_Zq", "IQSRC2310_2_Mq2_lambda", "IQSRC2310_3_DqWeyl2", "IQSRC2310_4_Jq_boundary_tail", "IQSRC2310_5_arena_projection"}.issubset({row["row_id"] for row in independent_rows}), "independent q fallback source rows are staged"))
    checks.append(("VAL2310_06_auxiliary_countermodel", any(row["row_id"] == "AUX2310_1_schur_effective_action" for row in auxiliary_rows), "auxiliary Schur route is retained as countermodel"))
    checks.append(("VAL2310_07_qX_not_current_route", any(row["row_id"] == "DEC2310_3_q_equals_X" and "do not use" in row["decision"] for row in decision_rows), "q=aX bridge is not used as current route"))
    checks.append(("VAL2310_08_claims_blocked", any(row["row_id"] == "CG2310_4_local_GR_Newton" and row["passed"] == "false" for row in claim_rows), "local GR/Newton claim remains blocked"))
    checks.append(("VAL2310_09_refusals_block_claims", all(row["allowed"] == "false" for row in refusal_rows), "refusal runner blocks premature claims"))
    checks.append(("VAL2310_10_next_target", any(row["row_id"] == "DEC2310_4_next" and "2311-Y5-R2FR-parent-q-removal-certificate-degree-count-boundary-neutrality-or-independent-Hessian-source-pack.md" in row["next_action"] for row in decision_rows), "next target selected"))
    checks.append(("VAL2310_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2310_12_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in tables for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2310_13_formalization_untouched_by_2310", len(formalization_hits) == 0, "no 2310 checkpoint output appears in formalization-workbench"))

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
            "row_id": "VAL2310_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2310 makes a nonclaim route choice: pursue q no-pole/quotient removal first as the clean GR-recovery route, while staging independent q Hessian and auxiliary Schur rows as fallbacks.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    score_rows: list[dict[str, Any]],
    no_pole_rows: list[dict[str, Any]],
    independent_rows: list[dict[str, Any]],
    auxiliary_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2310 — q Branch Selection: No-Pole Or Independent q Hessian",
        "",
        "## Summary",
        "",
        "2310 stops the route from smearing into three incompatible stories. The primary private derivation route is now the no-pole/quotient-removal branch, because that is the cleanest route to local GR/Newton recovery: if `q` is removed before reduction, there is no local `q` pole to suppress and no fifth-force scalar to tune.",
        "",
        "This is not a claim. The current corpus still lacks the one-branch parent certificate for quotient object, actual vertical generator, first-class degree count, action/matter/readout descent, and boundary/source neutrality. If that certificate cannot be signed, the fallback is an independent `q` Hessian source pack, not a borrowed `X/L_X` operator.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Branch Selection Scorecard",
        "",
        md_table(score_rows, ["row_id", "candidate_branch", "physics_payoff", "current_support", "current_blocker", "selection", "valid_for_claim"]),
        "",
        "## No-Pole Theorem Gate",
        "",
        md_table(no_pole_rows, ["row_id", "clause", "required_evidence", "mathematical_content", "current_status", "missing_piece", "valid_for_claim"]),
        "",
        "## Independent q First Source Row",
        "",
        md_table(independent_rows, ["row_id", "input", "meaning", "required_source_or_formula", "units", "current_status", "source_path", "valid_for_claim"]),
        "",
        "## Auxiliary q Schur Route",
        "",
        md_table(auxiliary_rows, ["row_id", "case", "formula", "consequence", "status", "valid_for_claim"]),
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
    score_rows = build_scorecard()
    no_pole_rows = build_no_pole_gate()
    independent_rows = build_independent_q_rows()
    auxiliary_rows = build_auxiliary_rows()
    decision_rows = build_decisions()
    claim_rows = build_claim_gates()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["scorecard"], score_rows)
    write_csv(OUTPUTS["no_pole"], no_pole_rows)
    write_csv(OUTPUTS["independent"], independent_rows)
    write_csv(OUTPUTS["auxiliary"], auxiliary_rows)
    write_csv(OUTPUTS["decisions"], decision_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(
        source_rows,
        score_rows,
        no_pole_rows,
        independent_rows,
        auxiliary_rows,
        decision_rows,
        claim_rows,
        refusal_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows)
    write_markdown(
        source_rows,
        score_rows,
        no_pole_rows,
        independent_rows,
        auxiliary_rows,
        decision_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
        validation_rows,
    )

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2310_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

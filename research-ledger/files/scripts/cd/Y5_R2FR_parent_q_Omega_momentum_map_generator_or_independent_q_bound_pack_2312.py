from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_Q_OMEGA_MOMENTUM_MAP_2312"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2312-Y5-R2FR-parent-q-Omega-momentum-map-generator-or-independent-q-bound-pack.md"

PATHS = {
    "2311_doc": ROOT / "2311-Y5-R2FR-parent-q-removal-certificate-degree-count-boundary-neutrality-or-independent-Hessian-source-pack.md",
    "2311_validation": OUT / "P8_Y5_BRR545_2311_VALIDATION.csv",
    "2311_certificate": OUT / "P8_Y5_PARENT_QLOC_2311_REMOVAL_CERTIFICATE_AUDIT.csv",
    "2311_fallback": OUT / "P8_Y5_PARENT_QLOC_2311_INDEPENDENT_HESSIAN_FALLBACK_PACK.csv",
    "582_momentum": OUT / "P8_Y5_R10_582_MOMENTUM_MAP_CLOSURE_THEOREM.csv",
    "582_gate": OUT / "P8_Y5_R10_582_NOPOLE_GATE_STATUS.csv",
    "590_dcdagger": OUT / "P8_Y5_R10_590_DCDAGGER_VERTICAL_MAP.csv",
    "670_vgen": OUT / "P8_Y5_R10_670_VERTICAL_GENERATOR_CERTIFICATE.csv",
    "581_nopole": OUT / "P8_Y5_R10_581_NO_POLE_CERTIFICATE_TEMPLATE.csv",
    "581_boundary": OUT / "P8_Y5_R10_581_BOUNDARY_CHARGE_AUDIT.csv",
    "2016_doc": ROOT / "2016-Y5-R2FR-Aframe-no-physical-pole-gauge-constraint-theorem-or-finite-prior-runner.md",
    "2017_doc": ROOT / "2017-Y5-R2FR-Aframe-split-gauge-generator-boundary-charge-zero-or-finite-A-source-row.md",
    "2300_firstclass": OUT / "P8_Y5_PARENT_QLOC_2300_Q_FIRSTCLASS_REMOVAL_CONTRACT.csv",
    "2301_firstclass": OUT / "P8_Y5_PARENT_QLOC_2301_Q_FIRSTCLASS_REMOVAL_ATTEMPT.csv",
    "637_qmap": OUT / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv",
    "2297_body": OUT / "P8_Y5_PARENT_QLOC_2297_BODY_CHARGE_SOURCE_LAW.csv",
    "2297_bounds": OUT / "P8_Y5_PARENT_QLOC_2297_JQ_COMPONENT_BOUND_TEMPLATE.csv",
}

SOURCES = [
    ("SRC2312_00_2311_doc", "2311_doc", PATHS["2311_doc"], ["DEC2311_4_next", "NPP2311_5_current_activation"], "direct 2311 handoff"),
    ("SRC2312_01_2311_validation", "2311_validation", PATHS["2311_validation"], ["VAL2311_OVERALL", "PASS"], "2311 validation"),
    ("SRC2312_02_2311_certificate", "2311_certificate", PATHS["2311_certificate"], ["QRC2311_2_parent_Omega", "MISSING_PARENT_OMEGA"], "q removal certificate blocker"),
    ("SRC2312_03_2311_fallback", "2311_fallback", PATHS["2311_fallback"], ["FB2311_7_claim_gate", "CLAIM_BLOCKED"], "independent-q fallback handoff"),
    ("SRC2312_04_582_momentum", "582_momentum", PATHS["582_momentum"], ["MMT582_0_constraint_generator", "MMT582_4_no_pole_result"], "general momentum-map closure theorem template"),
    ("SRC2312_05_582_gate", "582_gate", PATHS["582_gate"], ["NPG582_0_momentum_map_owner", "fail_current_claim"], "no-pole momentum-map gate status"),
    ("SRC2312_06_590_dcdagger", "590_dcdagger", PATHS["590_dcdagger"], ["DVM590_2_momentum_map_identity", "DVM590_3_precise_map"], "DCdagger to Omega-flat map template"),
    ("SRC2312_07_670_vgen", "670_vgen", PATHS["670_vgen"], ["VGC670_0_parent_Omega", "VGC670_5_bracket_closure"], "vertical generator certificate checklist"),
    ("SRC2312_08_581_nopole", "581_nopole", PATHS["581_nopole"], ["NPC581_3_constraint_rank", "NPC581_6_claim_gate"], "no-pole certificate template"),
    ("SRC2312_09_581_boundary", "581_boundary", PATHS["581_boundary"], ["BCA581_5_verdict", "blocked"], "boundary charge audit template"),
    ("SRC2312_10_2016_doc", "2016_doc", PATHS["2016_doc"], ["ANP2016_3_first_class_generator", "MISSING_PARENT_OMEGA_DCA_VERTICAL_GENERATOR"], "A-frame no-pole precedent"),
    ("SRC2312_11_2017_doc", "2017_doc", PATHS["2017_doc"], ["SGG2017_2_constraint_candidate", "FORMAL_GENERATOR_DERIVED_TO_BOUNDARY_TERM"], "A-frame generator skeleton precedent"),
    ("SRC2312_12_2300_firstclass", "2300_firstclass", PATHS["2300_firstclass"], ["QFC2300_0_parent_Omega", "MISSING_PARENT_OMEGA"], "q first-class contract"),
    ("SRC2312_13_2301_firstclass", "2301_firstclass", PATHS["2301_firstclass"], ["QFC2301_6_verdict", "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED"], "q first-class attempt"),
    ("SRC2312_14_637_qmap", "637_qmap", PATHS["637_qmap"], ["QM637_2_vertical_kernel", "Dq[v_X]=0"], "conditional q quotient vertical kernel"),
    ("SRC2312_15_2297_body", "2297_body", PATHS["2297_body"], ["BCL2297_1_body_charge", "Q_q[body]"], "q body charge fallback"),
    ("SRC2312_16_2297_bounds", "2297_bounds", PATHS["2297_bounds"], ["JBT2297_3_Qq_body", "MISSING_ZERO_THEOREM_OR_SOURCE_BOUND"], "q component bound fallback"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2312_SOURCE_REGISTER.csv",
    "transfer": OUT / "P8_Y5_PARENT_QLOC_2312_TEMPLATE_TRANSFER_AUDIT.csv",
    "candidates": OUT / "P8_Y5_PARENT_QLOC_2312_Q_MOMENTUM_MAP_CANDIDATES.csv",
    "shift": OUT / "P8_Y5_PARENT_QLOC_2312_Q_SHIFT_GENERATOR_DERIVATION.csv",
    "closure": OUT / "P8_Y5_PARENT_QLOC_2312_MOMENTUM_MAP_CLOSURE_GATES.csv",
    "fallback": OUT / "P8_Y5_PARENT_QLOC_2312_INDEPENDENT_Q_BOUND_PACK_UPDATE.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2312_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2312_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2312_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2312_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2312_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2312_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2312_0_transfer", OUTPUTS["transfer"], BETA_DOCS / "Q_TEMPLATE_TRANSFER_AUDIT_2312_NONCLAIM.csv"),
    ("COPY2312_1_candidates", OUTPUTS["candidates"], BETA_DOCS / "Q_MOMENTUM_MAP_CANDIDATES_2312_NONCLAIM.csv"),
    ("COPY2312_2_closure", OUTPUTS["closure"], RAB_QUEUE / "JR2312_Q_MOMENTUM_MAP_CLOSURE_GATES_NONCLAIM.csv"),
    ("COPY2312_3_fallback", OUTPUTS["fallback"], MICRO_RESIDUALS / "q_independent_bound_pack_update_nonclaim_2312.csv"),
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


def build_transfer_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "XFER2312_0_general_theorem",
            "template_source": "581/582/590/670 momentum-map/no-pole templates",
            "transfer_result": "SHAPE_TRANSFERS",
            "reason": "the symplectic theorem i_v Omega=delta G, bracket closure, degree count, and boundary differentiability are field-independent",
            "q_specific_blocker": "the objects Omega_q, v_q, C_q, Q_q, rank(G_q), and q boundary domain still need q-specific parent sources",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "XFER2312_1_Aframe_precedent",
            "template_source": "2016/2017 A-frame split-gauge generator",
            "transfer_result": "DO_NOT_COPY_FORMULA",
            "reason": "A has a split tetrad/gauge structure with delta X and delta A; q has no sourced analogous pair",
            "q_specific_blocker": "copying C_A=pi_X+D_i pi_A into q would be a category error",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "XFER2312_2_shift_scalar_option",
            "template_source": "canonical scalar shift generator",
            "transfer_result": "EXACT_IF_THETA_Q_EXISTS",
            "reason": "if Theta_q=int pi_q delta q, then the shift generator can be computed exactly",
            "q_specific_blocker": "Theta_q and pi_q are not parent-sourced; q may be quotient/readout or auxiliary rather than shift gauge",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "XFER2312_3_quotient_option",
            "template_source": "637 quotient vertical kernel plus 590 momentum-map identity",
            "transfer_result": "CONDITIONAL_ROUTE_ONLY",
            "reason": "if q is the quotient map and v_q is parent-null, the no-pole theorem is natural",
            "q_specific_blocker": "actual v_q field action and parent null generator remain unsigned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "XFER2312_4_verdict",
            "template_source": "all templates",
            "transfer_result": "MOMENTUM_MAP_TEMPLATE_READY_Q_PROOF_NOT_CLOSED",
            "reason": "the math scaffold is now exact enough, but current files do not source the q symplectic data",
            "q_specific_blocker": "source Theta_q/Omega_q or pivot to fallback bound pack",
            "valid_for_claim": "false",
        },
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "GQ2312_0_abstract_contract",
            "candidate": "abstract parent momentum-map generator",
            "formula": "i_{v_q} Omega_Y = delta G_q[epsilon], G_q[epsilon]=int_Sigma epsilon C_q + Q_q[epsilon]",
            "works_if": "Omega_Y, v_q, C_q, Q_q, differentiability, bracket closure, rank, and boundary/source neutrality are parent-signed",
            "current_status": "CONTRACT_ONLY",
            "missing_object": "Omega_Y;v_q;C_q;Q_q;rank(G_q);K_boundary",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GQ2312_1_canonical_shift",
            "candidate": "q is a shift-gauge coordinate",
            "formula": "Theta_q=int_Sigma pi_q delta q; v_epsilon q=epsilon; G_q[epsilon]=-int_Sigma epsilon pi_q + Q_q[epsilon]",
            "works_if": "action/readouts independent of q except through quotient, pi_q≈0 is first-class, and boundary term is proper/zero",
            "current_status": "EXACT_DERIVATION_IF_THETA_Q_SOURCED",
            "missing_object": "Theta_q;pi_q;q-shift action;boundary Q_q;degree count",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GQ2312_2_constraint_multiplier",
            "candidate": "q is a Lagrange multiplier enforcing C_q=0",
            "formula": "S contains int q C_parent; p_q≈0 primary and C_parent≈0 secondary; q itself has no propagating pole",
            "works_if": "constraint algebra closes and source/boundary/readout terms do not make q physical",
            "current_status": "AUXILIARY_OR_DIRAC_ROUTE_NOT_PARENT_SIGNED",
            "missing_object": "C_parent;Dirac algorithm;secondary constraints;boundary/source neutrality",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GQ2312_3_quotient_null",
            "candidate": "q is quotient/readout and local direction is parent-null",
            "formula": "Dq[v]=0 and Omega_Y(delta Phi,v)=delta G_q with G_q proper/zero",
            "works_if": "q map and v are both parent-owned and action/matter/readout descend",
            "current_status": "CONDITIONAL_ONLY",
            "missing_object": "parent q map;actual v_q;Omega_Y;descent;boundary zero",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GQ2312_4_independent_dynamic",
            "candidate": "q is an independent scalar field",
            "formula": "Theta_q exists but i_v Omega_q is not a constraint generator; q has L_q and source response",
            "works_if": "not a no-pole route; use Z_q,M_q^2,D_qWeyl2,J_q and arena projection",
            "current_status": "FALLBACK_IF_GAUGE_ROUTES_FAIL",
            "missing_object": "Z_q;M_q^2;D_qWeyl2;J_q;arena projection",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GQ2312_5_verdict",
            "candidate": "q momentum-map source hunt",
            "formula": "no candidate is currently parent-signed",
            "works_if": "GQ2312_1 or GQ2312_2 or GQ2312_3 acquires q-specific parent sources",
            "current_status": "GQ_NOT_ACTIVATED_CURRENT",
            "missing_object": "q symplectic potential or q constraint source",
            "valid_for_claim": "false",
        },
    ]


def build_shift_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SHIFT2312_0_assumption",
            "step": "canonical q shift assumption",
            "derivation": "assume the parent symplectic potential has a q block Theta_q=int_Sigma pi_q delta q plus boundary terms",
            "result": "this is an assumption/target, not current evidence",
            "status": "SOURCE_MISSING",
            "needed_to_promote": "parent action variation showing Theta_q and pi_q",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SHIFT2312_1_contraction",
            "step": "contract Omega with q-shift vector",
            "derivation": "for v_epsilon q=epsilon and v_epsilon pi_q=0, i_{v_epsilon} Omega_q = -delta int_Sigma epsilon pi_q plus boundary terms",
            "result": "G_q[epsilon]=-int_Sigma epsilon pi_q+Q_q[epsilon] up to sign convention",
            "status": "EXACT_FORMULA_IF_THETA_Q_EXISTS",
            "needed_to_promote": "Theta_q, boundary convention, and allowed epsilon domain",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SHIFT2312_2_constraint",
            "step": "first-class constraint candidate",
            "derivation": "the shift gauge constraint is pi_q≈0; it removes q only if action, matter, readout, and boundary are q-shift invariant",
            "result": "rank(G_q)=N_q would remove the q canonical pair",
            "status": "CONDITIONAL_FIRSTCLASS_CANDIDATE",
            "needed_to_promote": "invariance/descent proof and rank count",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SHIFT2312_3_bracket",
            "step": "bracket closure",
            "derivation": "{G_q[epsilon],G_q[eta]}=K_q_boundary[epsilon,eta] for abelian shifts",
            "result": "first-class only if K_q_boundary=0/proper",
            "status": "BOUNDARY_COCYCLE_UNCOMPUTED",
            "needed_to_promote": "boundary charge/cocycle calculation",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SHIFT2312_4_verdict",
            "step": "shift route activation",
            "derivation": "SHIFT2312_0 through SHIFT2312_3 must be source-backed in the same parent branch",
            "result": "do not activate q no-pole from shift route",
            "status": "SHIFT_GENERATOR_NOT_PARENT_SIGNED",
            "needed_to_promote": "Theta_q/pi_q source or explicit q-constraint action",
            "valid_for_claim": "false",
        },
    ]


def build_closure_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CLOSE2312_0_Omega", "gate": "parent Omega_Y and q block Theta_q/Omega_q sourced", "required_for": "any Hamiltonian q generator", "current_status": "MISSING_PARENT_OMEGA_Q_BLOCK", "claim_effect": "no first-class q proof", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CLOSE2312_1_vertical_action", "gate": "v_q action on geometry, q, matter, readout, boundary fields", "required_for": "knowing what G_q generates", "current_status": "MISSING_FIELD_BY_FIELD_VQ", "claim_effect": "cannot prove Dq[v]=0 for actual local branch", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CLOSE2312_2_generator", "gate": "C_q and Q_q define a differentiable G_q", "required_for": "Hamiltonian momentum map", "current_status": "MISSING_CQ_QQ", "claim_effect": "no legal generator", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CLOSE2312_3_bracket", "gate": "bracket closes with K_boundary=0/proper", "required_for": "first-class status", "current_status": "MISSING_BRACKET_CLOSURE", "claim_effect": "q may be second-class/edge mode", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CLOSE2312_4_degree", "gate": "rank(G_q)=N_q removes q canonical pair", "required_for": "no q physical pole", "current_status": "MISSING_RANK_DEGREE_COUNT", "claim_effect": "no-pole not proved", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CLOSE2312_5_descent", "gate": "bulk/matter/readout descend and source/boundary charges vanish", "required_for": "no residual q source", "current_status": "MISSING_DESCENT_AND_SOURCE_NEUTRALITY", "claim_effect": "q can return as source hair", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CLOSE2312_6_verdict", "gate": "q momentum-map closure", "required_for": "activate q no-pole/local-GR route", "current_status": "MOMENTUM_MAP_NOT_CLOSED_CURRENT", "claim_effect": "fallback pack remains live", "valid_for_claim": "false"},
    ]


def build_fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BND2312_0_trigger",
            "bound_input": "fallback activation trigger",
            "source_requirement": "CLOSE2312_6 remains not closed after q-specific Omega/G_q source hunt",
            "current_status": "TRIGGER_READY_NOT_SCORE_READY",
            "arena": "all_local_arenas",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BND2312_1_dynamic_q_operator",
            "bound_input": "Z_q, M_q^2, lambda_q",
            "source_requirement": "same-normalization q Hessian with units and sign",
            "current_status": "MISSING_PARENT_HESSIAN",
            "arena": "R10;PPN;clock;orbital;local_GR",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BND2312_2_curvature_coupling",
            "bound_input": "D_qWeyl2 and other curvature vertices",
            "source_requirement": "parent coefficient or theorem-zero; no borrowed X coefficient",
            "current_status": "MISSING_PARENT_COEFFICIENT",
            "arena": "local_GR;PPN;orbital;R10",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BND2312_3_source_vector",
            "bound_input": "J_q components, Q_q[body], Q_q_boundary, tails",
            "source_requirement": "componentwise theorem-zero or absolute source-backed bound",
            "current_status": "MISSING_SOURCE_ZERO_OR_BOUND",
            "arena": "R10;PPN;clock;orbital;alpha3",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BND2312_4_projection",
            "bound_input": "tau_R10, tau_PPN, tau_clock, tau_orbital, qbar/Qbar/K",
            "source_requirement": "arena projection in same q normalization",
            "current_status": "MISSING_ARENA_PROJECTION",
            "arena": "all_empirical_local_arenas",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BND2312_5_claim_gate",
            "bound_input": "independent q bound score",
            "source_requirement": "BND2312_1 through BND2312_4 all source-backed or theorem-zero",
            "current_status": "CLAIM_BLOCKED",
            "arena": "all_local_arenas",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2312_0_template_result",
            "decision": "momentum-map theorem template transfers only as shape",
            "reason": "581/582/590/670 give the exact symplectic contract, but not q-specific Omega/G_q data",
            "next_action": "do not claim q first-class from template inheritance",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2312_1_shift_result",
            "decision": "canonical q-shift generator derived conditionally",
            "reason": "if Theta_q=int pi_q delta q, then G_q=-int epsilon pi_q+Q_q is exact up to convention",
            "next_action": "hunt parent source for Theta_q/pi_q or q constraint action",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2312_2_activation_status",
            "decision": "q momentum-map generator not activated",
            "reason": "Theta_q/Omega_q, v_q, C_q, Q_q, bracket, degree count, and source/boundary neutrality are missing",
            "next_action": "keep no-pole theorem conditional and fallback pack live",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2312_3_fallback_policy",
            "decision": "independent-q bound pack remains nonclaim fallback",
            "reason": "without first-class closure, q may be dynamic, auxiliary, second-class, or edge-sourced",
            "next_action": "do not score until operator/source/projection rows are filled",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2312_4_next",
            "decision": "NEXT_TARGET_SELECTED",
            "reason": "the exact next source object is Theta_q/Omega_q or an explicit q constraint action; without it, move to bound-runner activation",
            "next_action": "2313-Y5-R2FR-q-symplectic-potential-source-or-independent-q-bound-runner-activation.md",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2312_0_sources", "gate": "source paths and needles valid", "passed": "true", "claim_effect": "audit is reproducible", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2312_1_template", "gate": "momentum-map theorem template identified", "passed": "true", "claim_effect": "math scaffold exists", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2312_2_shift_derivation", "gate": "canonical q-shift generator formula derived", "passed": "true", "claim_effect": "candidate G_q form is exact if Theta_q exists", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2312_3_q_Omega", "gate": "Theta_q/Omega_q parent-sourced", "passed": "false", "claim_effect": "cannot own G_q", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2312_4_firstclass", "gate": "bracket/degree/source neutrality closed", "passed": "false", "claim_effect": "no-pole not activated", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2312_5_bound_pack", "gate": "independent q bound pack score-ready", "passed": "false", "claim_effect": "cannot score fallback branch", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2312_6_local_GR_Newton", "gate": "derived local GR/Newton recovery allowed", "passed": "false", "claim_effect": "still target not result", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2312_0_template_claim", "claim": "q first-class follows from X/A momentum-map templates", "allowed": "false", "reason": "template shape transfers but q-specific Omega/G_q objects are missing", "blocking_rows": "XFER2312_4_verdict", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2312_1_shift_claim", "claim": "canonical q-shift no-pole is proven", "allowed": "false", "reason": "Theta_q/pi_q and q-shift invariance are not parent-sourced", "blocking_rows": "SHIFT2312_4_verdict", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2312_2_delete_q_residuals", "claim": "delete q residual/source rows now", "allowed": "false", "reason": "momentum-map closure fails current evidence", "blocking_rows": "CLOSE2312_6_verdict", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2312_3_score_bound_pack", "claim": "score independent q branch now", "allowed": "false", "reason": "bound pack still lacks operator, coefficients, source vector, and projection", "blocking_rows": "BND2312_5_claim_gate", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2312_0",
            "next_target": "2313-Y5-R2FR-q-symplectic-potential-source-or-independent-q-bound-runner-activation.md",
            "why": "Theta_q/Omega_q or an explicit q constraint action is the first concrete missing object; if absent, activate the independent-q bound-runner path instead of more no-pole laps",
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
    transfer_rows: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]],
    shift_rows: list[dict[str, Any]],
    closure_rows: list[dict[str, Any]],
    fallback_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tables = [source_rows, transfer_rows, candidate_rows, shift_rows, closure_rows, fallback_rows, decision_rows, claim_rows, refusal_rows, copy_rows]
    formalization_output_markers = (
        "2312-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_2312",
        "P8_Y5_BRR545_2312",
        "Q_TEMPLATE_TRANSFER_AUDIT_2312",
        "Q_MOMENTUM_MAP_CANDIDATES_2312",
        "JR2312_",
        "q_independent_bound_pack_update_nonclaim_2312",
        "Y5_R2FR_parent_q_Omega_momentum_map_generator_or_independent_q_bound_pack_2312",
    )
    formalization_hits = [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in formalization_output_markers)
    ] if FORMALIZATION.exists() else []

    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2312_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists"))
    checks.append(("VAL2312_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2312_02_template_transfer_guard", any(row["row_id"] == "XFER2312_4_verdict" and row["transfer_result"] == "MOMENTUM_MAP_TEMPLATE_READY_Q_PROOF_NOT_CLOSED" for row in transfer_rows), "template transfer is guarded"))
    checks.append(("VAL2312_03_candidate_verdict", any(row["row_id"] == "GQ2312_5_verdict" and row["current_status"] == "GQ_NOT_ACTIVATED_CURRENT" for row in candidate_rows), "q generator candidate verdict remains nonclaim"))
    checks.append(("VAL2312_04_shift_derivation", any(row["row_id"] == "SHIFT2312_1_contraction" and "G_q[epsilon]" in row["result"] for row in shift_rows), "canonical shift generator formula is written"))
    checks.append(("VAL2312_05_shift_not_activated", any(row["row_id"] == "SHIFT2312_4_verdict" and row["status"] == "SHIFT_GENERATOR_NOT_PARENT_SIGNED" for row in shift_rows), "shift route not activated"))
    checks.append(("VAL2312_06_closure_blocked", any(row["row_id"] == "CLOSE2312_6_verdict" and row["current_status"] == "MOMENTUM_MAP_NOT_CLOSED_CURRENT" for row in closure_rows), "momentum-map closure remains blocked"))
    checks.append(("VAL2312_07_fallback_pack", any(row["row_id"] == "BND2312_5_claim_gate" and row["current_status"] == "CLAIM_BLOCKED" for row in fallback_rows), "fallback bound pack remains nonclaim"))
    checks.append(("VAL2312_08_next_target", any(row["row_id"] == "DEC2312_4_next" and "2313-Y5-R2FR-q-symplectic-potential-source-or-independent-q-bound-runner-activation.md" in row["next_action"] for row in decision_rows), "next target selected"))
    checks.append(("VAL2312_09_claims_blocked", any(row["row_id"] == "CG2312_6_local_GR_Newton" and row["passed"] == "false" for row in claim_rows), "local GR/Newton claim remains blocked"))
    checks.append(("VAL2312_10_refusals_block", all(row["allowed"] == "false" for row in refusal_rows), "refusal runner blocks premature claims"))
    checks.append(("VAL2312_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2312_12_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in tables for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2312_13_formalization_untouched_by_2312", len(formalization_hits) == 0, "no 2312 checkpoint output appears in formalization-workbench"))

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
            "row_id": "VAL2312_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2312 imports only the momentum-map theorem shape, derives the exact canonical q-shift generator conditionally, refuses q no-pole activation without Theta_q/Omega_q and G_q sources, and keeps the independent-q bound pack live.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    transfer_rows: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]],
    shift_rows: list[dict[str, Any]],
    closure_rows: list[dict[str, Any]],
    fallback_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2312 — Parent q Omega / Momentum-Map Generator Or Bound Pack",
        "",
        "## Summary",
        "",
        "2312 finds the usable theorem template but refuses to overdraw it. The older `581/582/590/670` chain gives the exact momentum-map shape: `i_v Ω = δG`, differentiability, bracket closure, degree count, and boundary silence. That shape transfers to `q`; the old `X/A` formulae do not.",
        "",
        "The new constructive result is the conditional canonical shift calculation: if the parent action supplies `Θ_q = ∫ π_q δq`, then a q-shift `v_ε q=ε` has generator `G_q[ε] = -∫ ε π_q + Q_q[ε]`, up to convention. But `Θ_q`, `π_q`, `C_q`, and `Q_q` are not parent-sourced, so the no-pole branch remains conditional and the independent-q bound pack stays live.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Template Transfer Audit",
        "",
        md_table(transfer_rows, ["row_id", "template_source", "transfer_result", "reason", "q_specific_blocker", "valid_for_claim"]),
        "",
        "## q Momentum-Map Candidates",
        "",
        md_table(candidate_rows, ["row_id", "candidate", "formula", "works_if", "current_status", "missing_object", "valid_for_claim"]),
        "",
        "## Canonical q-Shift Generator Derivation",
        "",
        md_table(shift_rows, ["row_id", "step", "derivation", "result", "status", "needed_to_promote", "valid_for_claim"]),
        "",
        "## Momentum-Map Closure Gates",
        "",
        md_table(closure_rows, ["row_id", "gate", "required_for", "current_status", "claim_effect", "valid_for_claim"]),
        "",
        "## Independent q Bound Pack Update",
        "",
        md_table(fallback_rows, ["row_id", "bound_input", "source_requirement", "current_status", "arena", "valid_for_claim"]),
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
    transfer_rows = build_transfer_rows()
    candidate_rows = build_candidate_rows()
    shift_rows = build_shift_rows()
    closure_rows = build_closure_rows()
    fallback_rows = build_fallback_rows()
    decision_rows = build_decision_rows()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["transfer"], transfer_rows)
    write_csv(OUTPUTS["candidates"], candidate_rows)
    write_csv(OUTPUTS["shift"], shift_rows)
    write_csv(OUTPUTS["closure"], closure_rows)
    write_csv(OUTPUTS["fallback"], fallback_rows)
    write_csv(OUTPUTS["decisions"], decision_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(
        source_rows,
        transfer_rows,
        candidate_rows,
        shift_rows,
        closure_rows,
        fallback_rows,
        decision_rows,
        claim_rows,
        refusal_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows)
    write_markdown(
        source_rows,
        transfer_rows,
        candidate_rows,
        shift_rows,
        closure_rows,
        fallback_rows,
        decision_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
        validation_rows,
    )

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2312_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

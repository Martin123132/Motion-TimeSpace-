from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_SPIN_CONNECTION_COFRAME_OWNED_OR_AXIAL_TORSION_P4_ROW_2348"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2348-Y5-R2FR-spin-connection-coframe-owned-or-axial-torsion-P4-row.md"

PATHS = {
    "2347_doc": ROOT / "2347-Y5-R2FR-noGamma-SRNG-adoption-or-P4-hypermomentum-component-row.md",
    "2347_spin": OUT / "P8_Y5_PARENT_QLOC_2347_SPIN_CONNECTION_NEXT_PROOF_OBLIGATION.csv",
    "2347_p4": OUT / "P8_Y5_PARENT_QLOC_2347_P4_HYPERMOMENTUM_COMPONENT_ROW.csv",
    "2347_next": OUT / "P8_Y5_PARENT_QLOC_2347_NEXT_TARGET.csv",
    "2333_nohyper": OUT / "P8_Y5_PARENT_QLOC_2333_NOHYPERMOMENTUM_LEVICIVITA_PROOF_AUDIT.csv",
    "2333_p4": OUT / "P8_Y5_PARENT_QLOC_2333_P4_HYPERMOMENTUM_RESIDUAL_ROW.csv",
    "2334_slots": OUT / "P8_Y5_PARENT_QLOC_2334_GAMMA_SLOT_SECTOR_AUDIT.csv",
    "2334_stack": OUT / "P8_Y5_PARENT_QLOC_2334_NO_GAMMA_THEOREM_STACK.csv",
    "2042_nohyper": OUT / "P8_Y5_PARENT_QLOC_2042_NO_HYPERMOMENTUM_THEOREM_ATTEMPT.csv",
    "2041_connection": OUT / "P8_Y5_PARENT_QLOC_2041_TORSION_CONNECTION_DECISION_LEDGER.csv",
}

SOURCES = [
    ("SRC2348_00_2347_doc", "2347_doc", ["Spin Connection Next Proof Obligation", "SPIN2347_0_target"], "2347 narrative selected spin connection as next clean residual"),
    ("SRC2348_01_2347_spin", "2347_spin", ["SPIN2347_0_target", "coframe-owned spin connection"], "machine-readable 2348 proof obligation"),
    ("SRC2348_02_2347_p4", "2347_p4", ["P4H2347_2_spin", "spin/torsion/nonmetricity"], "live spin/torsion hypermomentum component"),
    ("SRC2348_03_2347_next", "2347_next", ["NEXT2347_0", "spin-connection-coframe-owned"], "target pointer from 2347"),
    ("SRC2348_04_2333_nohyper", "2333_nohyper", ["NHL2333_2_chain_rule_spin_connection", "EXACT_CONDITIONAL_CLAUSE"], "earlier coframe-owned spin-connection clause"),
    ("SRC2348_05_2333_p4", "2333_p4", ["P4R2333_2_axial_torsion_guard", "MISSING_SPIN_TORSION_COEFFICIENT"], "existing axial torsion guard row"),
    ("SRC2348_06_2334_slots", "2334_slots", ["NGSA2334_2_spinor_transport", "CONDITIONAL_SPIN_GUARD_NOT_GLOBAL"], "sector audit of spinor/transport Gamma slot"),
    ("SRC2348_07_2334_stack", "2334_stack", ["NGT2334_1_coframe_chain_rule", "EXACT_MATH_CONDITIONAL"], "conditional chain-rule lemma"),
    ("SRC2348_08_2042_nohyper", "2042_nohyper", ["NH2042_2_chain_rule", "NH2042_3_spin_guard"], "no-hypermomentum theorem attempt and spin counterbranch"),
    ("SRC2348_09_2041_connection", "2041_connection", ["LC2041_4_P4_fallback", "axial torsion"], "connection fallback menu"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2348_SOURCE_REGISTER.csv",
    "audit": OUT / "P8_Y5_PARENT_QLOC_2348_SPIN_CONNECTION_COFRAME_OWNED_AUDIT.csv",
    "proof": OUT / "P8_Y5_PARENT_QLOC_2348_CHAIN_RULE_PROOF_STACK.csv",
    "p4": OUT / "P8_Y5_PARENT_QLOC_2348_AXIAL_TORSION_P4_COMPONENT_ROW.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2348_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2348_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2348_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2348_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2348_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2348_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2348_0_spin_audit", OUTPUTS["audit"], BETA_DOCS / "SPIN_CONNECTION_COFRAME_OWNED_AUDIT_2348_NONCLAIM.csv"),
    ("COPY2348_1_axial_p4", OUTPUTS["p4"], MICRO_RESIDUALS / "P4_AXIAL_TORSION_COMPONENT_ROW_2348_NONCLAIM.csv"),
    ("COPY2348_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2348_SPIN_CONNECTION_DECISION_LEDGER_NONCLAIM.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_key, needles, role in SOURCES:
        path = PATHS[source_key]
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": source_key,
                "source_path": str(path),
                "exists": bool_text(exists),
                "required": "true",
                "needles": ";".join(needles),
                "needles_found": bool_text(exists and not missing),
                "missing_needles": ";".join(missing),
                "source_role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def build_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPIN2348_0_target",
            "clause": "coframe-owned spin connection target",
            "formal_statement": "omega_obs = omega_LC[e_obs] for spinors, spin transport and local ordinary matter; no independent torsionful omega_ind/Gamma_ind appears in those sector arguments.",
            "status": "TARGET_SHARPENED",
            "obstruction": "must be parent-signed as a variable-domain clause, not merely assumed from GR language",
            "effect_if_closed": "Delta_spin = 0 by variable absence and chain rule",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPIN2348_1_exact_conditional_zero",
            "clause": "spin hypermomentum zero under owned coframe",
            "formal_statement": "If S_spin = Sbar[psi, e_obs, omega_LC[e_obs], A_owned, theta] and has no omega_ind/Gamma_ind slot, then delta S_spin / delta Gamma_ind = 0.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "obstruction": "ordinary spin and transport sectors are not globally signed in the parent action",
            "effect_if_closed": "ordinary spin does not create an independent torsion/nonmetricity source",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPIN2348_2_chain_rule_owner",
            "clause": "dependent spin connection variation",
            "formal_statement": "When omega_LC[e_obs] is dependent, delta omega is induced by delta e_obs; its contribution belongs to the coframe/Hilbert stress equation, not a separate Gamma equation.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "obstruction": "requires explicit dependent-variable calculus in the parent ordinary branch",
            "effect_if_closed": "prevents double-counting GR spin connection as a new physical affine source",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPIN2348_3_parent_signature_gap",
            "clause": "parent action variable-domain signature",
            "formal_statement": "Arg(S_ord) must list e_obs/g_obs, omega_LC[e_obs], owned gauge fields and theta, and exclude omega_ind/Gamma_ind for every ordinary local sector.",
            "status": "MISSING_PARENT_SIGNATURE",
            "obstruction": "the corpus has contracts and audits, not a final signed common parent action",
            "effect_if_closed": "would promote the spin zero from conditional theorem to branch theorem",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPIN2348_4_EC_metric_affine_counterbranch",
            "clause": "Einstein-Cartan/metric-affine alternative",
            "formal_statement": "If omega_ind/Gamma_ind is an independent variable coupled to spin current, axial torsion response is generically nonzero and must be retained as a P4 residual.",
            "status": "COUNTERBRANCH_RETAINS_P4",
            "obstruction": "no parent exclusion of independent torsionful/spin connection branch",
            "effect_if_closed": "none; this row blocks a silent torsion-zero assumption",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPIN2348_5_projective_guard",
            "clause": "projective trace caveat",
            "formal_statement": "Even a Palatini route needs the projective trace gauge/fix/unobservable policy for spin transport, source, clocks, light and orbits.",
            "status": "SEPARATE_UNSIGNED_GATE",
            "obstruction": "projective trace silence has not been closed in this branch",
            "effect_if_closed": "would remove trace leakage after no-hypermomentum closure",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPIN2348_6_verdict",
            "clause": "promote Delta_spin=0",
            "formal_statement": "Current corpus proves spin connection is coframe-owned for all relevant local sectors.",
            "status": "NOT_PUBLICLY_DERIVED_RETAIN_AXIAL_TORSION_P4_ROW",
            "obstruction": "parent variable signature, independent torsion exclusion and projective guard remain unsigned",
            "effect_if_closed": "not closed; keep Delta_spin as a nonclaim residual row",
            "valid_for_claim": "false",
        },
    ]


def build_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CHAIN2348_0_variable_absence",
            "lemma": "variable-absence derivative",
            "statement": "For S[y] on a reduced configuration space that excludes Gamma_ind, the independent functional derivative delta S / delta Gamma_ind is zero/vacuous.",
            "proof_status": "EXACT_MATH_CONDITIONAL",
            "missing_parent_input": "sector action domain must actually exclude Gamma_ind",
            "use": "base no-hypermomentum logic",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CHAIN2348_1_spin_bundle_pullback",
            "lemma": "spin connection as pullback from coframe",
            "statement": "omega_obs is the Levi-Civita spin connection determined by e_obs; it is not an independent coordinate on the local ordinary branch.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_parent_input": "parent must name omega_LC[e_obs] rather than omega_ind in spin/transport slots",
            "use": "blocks treating GR spin connection notation as torsion dynamics",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CHAIN2348_2_chain_rule_to_hilbert",
            "lemma": "dependent variation owner",
            "statement": "delta S_spin / delta e_obs includes the induced delta omega_LC[e_obs] term; no separate spin hypermomentum equation is generated.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_parent_input": "explicit dependent-variable variation convention",
            "use": "assigns spin backreaction to Hilbert/coframe stress",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CHAIN2348_3_no_cancellation",
            "lemma": "componentwise zero",
            "statement": "Delta_spin is zero only when the spin derivative is individually absent; no cancellation with source, boundary or projective terms is allowed.",
            "proof_status": "STRUCTURAL_RULE",
            "missing_parent_input": "none beyond component domains",
            "use": "keeps local-GR reduction non-tuned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CHAIN2348_4_failure_condition",
            "lemma": "independent torsion counterterm",
            "statement": "If S_spin contains c_A S_mu J5^mu or any independent torsion/nonmetricity source, Delta_spin is generically nonzero.",
            "proof_status": "COUNTERBRANCH_EXPLICIT",
            "missing_parent_input": "coefficient, units, weak-field map and arena projection",
            "use": "defines the P4 axial-torsion fallback",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CHAIN2348_5_parent_contract",
            "lemma": "future parent action contract",
            "statement": "A future parent action must either sign S_spin[psi,e_obs,omega_LC[e_obs],A_owned,theta] with no independent connection slot, or expose the torsion/nonmetricity coefficients as P4 residuals.",
            "proof_status": "CONTRACT_READY_NOT_SIGNED",
            "missing_parent_input": "common parent action text",
            "use": "turns this checkpoint into a concrete acceptance test for the parent action",
            "valid_for_claim": "false",
        },
    ]


def build_p4_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4S2348_0_spin_total",
            "quantity": "Delta_spin_abs",
            "component": "total spin/torsion/nonmetricity residual",
            "formula": "S_axial_abs + T_trace_abs + Q_weyl_abs + Q_shear_abs + Delta_spin_boundary_abs + Delta_spin_projective_abs",
            "units": "normalized hypermomentum envelope or dimensionless local-response bound",
            "current_value": "MISSING_COMPONENT_VALUES",
            "source_path": "MISSING_PARENT_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4S2348_1_axial_torsion",
            "quantity": "S_axial_abs",
            "component": "axial spin-torsion response",
            "formula": "||c_A S_mu J5^mu|| / N_source",
            "units": "dimensionless after N_source normalization",
            "current_value": "MISSING_SPIN_TORSION_COEFFICIENT",
            "source_path": "MISSING_PARENT_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4S2348_2_trace_torsion",
            "quantity": "T_trace_abs",
            "component": "trace torsion response",
            "formula": "||c_T T_mu J_T^mu|| / N_source",
            "units": "dimensionless after N_source normalization",
            "current_value": "MISSING_TRACE_TORSION_COEFFICIENT",
            "source_path": "MISSING_PARENT_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4S2348_3_weyl_nonmetricity",
            "quantity": "Q_weyl_abs",
            "component": "Weyl nonmetricity response",
            "formula": "||c_Q Q_mu J_Q^mu|| / N_source",
            "units": "dimensionless after N_source normalization",
            "current_value": "MISSING_WEYL_NONMETRICITY_COEFFICIENT",
            "source_path": "MISSING_PARENT_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4S2348_4_shear_nonmetricity",
            "quantity": "Q_shear_abs",
            "component": "traceless/shear nonmetricity response",
            "formula": "||c_Qs Q_tl J_Qs|| / N_source",
            "units": "dimensionless after N_source normalization",
            "current_value": "MISSING_SHEAR_NONMETRICITY_COEFFICIENT",
            "source_path": "MISSING_PARENT_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4S2348_5_weak_field_map",
            "quantity": "epsilon_P4_spin_abs",
            "component": "weak-field spin residual mapped to local tests",
            "formula": "epsilon_P4_spin_abs <= K_spin * Delta_spin_abs",
            "units": "PPN/WEP/clock/orbital residual units after arena projection",
            "current_value": "MISSING_WEAK_FIELD_MAP_AND_K_SPIN",
            "source_path": "MISSING_ARENA_PROJECTION",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4S2348_6_no_claim",
            "quantity": "local_GR_spin_gate",
            "component": "claim policy",
            "formula": "claim_allowed = Z_spin_zero OR sourced_numeric_bound_passes_all_local_arenas",
            "units": "boolean gate",
            "current_value": "FALSE",
            "source_path": "P8_Y5_PARENT_QLOC_2348_CLAIM_GATES.csv",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "DEC2348_0_result", "decision": "do not promote Delta_spin=0 as public theorem", "reason": "the coframe-owned spin connection proof is exact but conditional on an unsigned parent variable-domain clause", "consequence": "retain axial torsion/nonmetricity P4 row", "status": "CONDITIONAL_THEOREM_P4_RETAINED", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2348_1_clean_win", "decision": "keep the coframe-owned lemma as the desired parent-action contract", "reason": "it gives a derivable GR-like spin connection without fitting or cancellation", "consequence": "future parent action must explicitly own omega_LC[e_obs]", "status": "CONTRACT_READY", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2348_2_counterbranch", "decision": "treat independent torsionful/metric-affine spin connection as nonzero unless excluded", "reason": "engineering rule: nothing just vanishes if it has a live coefficient and source", "consequence": "P4S2348 rows remain nonclaim placeholders until sourced or theorem-zeroed", "status": "TORSION_COUNTERBRANCH_EXPLICIT", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2348_3_next", "decision": "attack projective trace silence next", "reason": "even no-hypermomentum/Palatini closure leaks unless projective trace is gauge/fixed/unobservable across local readouts", "consequence": "next target is a projective-trace zero proof or P4 projective row", "status": "SELECT_PROJECTIVE_TRACE_NEXT", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2348_4_public_policy", "decision": "no GitHub update from 2348", "reason": "this is a private proof-contract and residual-staging checkpoint, not a local-GR claim", "consequence": "continue private derivation work", "status": "NO_GITHUB_EVIDENCE_UPDATE", "valid_for_claim": "false"},
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2348_0_spin_zero_public", "gate": "Delta_spin=0 derived publicly", "passed": "false", "claim_effect": "conditional theorem only", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2348_1_parent_signature", "gate": "parent ordinary branch signs omega_LC[e_obs] and excludes omega_ind/Gamma_ind", "passed": "false", "claim_effect": "required for theorem promotion", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2348_2_independent_torsion_excluded", "gate": "Einstein-Cartan/metric-affine spin branch excluded or residualized", "passed": "false", "claim_effect": "axial torsion P4 row retained", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2348_3_projective_guard", "gate": "projective trace silent across local readouts", "passed": "false", "claim_effect": "next connection-side caveat", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2348_4_p4_score_ready", "gate": "axial torsion P4 row has values, units, source paths and local projections", "passed": "false", "claim_effect": "nonclaim placeholder only", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2348_5_local_GR_Newton", "gate": "local GR/Newton connection recovery derived", "passed": "false", "claim_effect": "spin, projective and boundary gates remain", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2348_0_conditional_as_proof", "claim": "coframe-owned spin connection is now a public MTS theorem", "allowed": "false", "reason": "the theorem is exact only after the parent action signs the variable domain", "blocking_rows": "SPIN2348_3_parent_signature_gap;CG2348_1_parent_signature", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2348_1_torsion_zero_by_taste", "claim": "axial torsion vanishes because we prefer the GR branch", "allowed": "false", "reason": "independent torsionful/metric-affine branches must be excluded by action or bounded", "blocking_rows": "SPIN2348_4_EC_metric_affine_counterbranch;P4S2348_1_axial_torsion", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2348_2_p4_as_empirical_pass", "claim": "the P4 axial torsion row is a local-test pass", "allowed": "false", "reason": "component coefficients, units, normalization, source paths and arena projection are missing", "blocking_rows": "P4S2348_0_spin_total;P4S2348_5_weak_field_map", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2348_3_srng_closes_spin", "claim": "private SRNG closes spin/torsion",
         "allowed": "false", "reason": "SRNG only reduced source/readout Gamma leakage; spin connection ownership is a separate gate", "blocking_rows": "SPIN2348_0_target;P4S2348_0_spin_total", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2348_4_local_GR_claim", "claim": "2348 proves local GR/Newton reduction", "allowed": "false", "reason": "2348 supplies a sharp contract and fallback, while projective/boundary/source gates remain open", "blocking_rows": "CG2348_3_projective_guard;CG2348_5_local_GR_Newton", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "NEXT2348_0", "next_target": "2349-Y5-R2FR-projective-trace-silence-or-P4-projective-component-row.md", "why": "the coframe-owned spin route is conditionally clean, but any Palatini/no-hypermomentum route still needs the projective trace made gauge/fixed/unobservable or bounded", "route_type": "connection_derivation_next_step", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "NEXT2348_1", "next_target": "2349b-Y5-R2FR-parent-ordinary-action-variable-signature.md", "why": "direct way to promote coframe-owned spin from conditional theorem to parent-signed branch theorem", "route_type": "parent_action_contract_parallel", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "NEXT2348_2", "next_target": "2349c-Y5-R2FR-boundary-improvement-current-zero-or-P4-boundary-row.md", "why": "boundary/improvement terms remain a separate route by which connection/source leakage can re-enter", "route_type": "parallel_nonclaim", "valid_for_claim": "false"},
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source, destination in BRANCH_COPY_SPECS:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": str(source.relative_to(ROOT)),
                "branch_copy_path": str(destination),
                "copy_exists": bool_text(destination.exists()),
                "row_count": len(read_csv_rows(destination)),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation(
    sources: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    proof_rows: list[dict[str, Any]],
    p4_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append({"timestamp_utc": timestamp(), "branch_id": BRANCH_ID, "row_id": row_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": "false"})

    add("VAL2348_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists")
    add("VAL2348_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found")
    add("VAL2348_02_exact_conditional_theorem_recorded", any(row["row_id"] == "SPIN2348_1_exact_conditional_zero" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in audit_rows), "coframe-owned spin zero theorem recorded as exact conditional")
    add("VAL2348_03_public_promotion_blocked", any(row["row_id"] == "SPIN2348_6_verdict" and row["status"] == "NOT_PUBLICLY_DERIVED_RETAIN_AXIAL_TORSION_P4_ROW" for row in audit_rows), "spin zero not publicly promoted")
    add("VAL2348_04_chain_rule_owner_present", any(row["row_id"] == "CHAIN2348_2_chain_rule_to_hilbert" and "Hilbert" in row["use"] for row in proof_rows), "dependent omega variation assigned to Hilbert/coframe stress")
    add("VAL2348_05_counterbranch_explicit", any(row["row_id"] == "CHAIN2348_4_failure_condition" and row["proof_status"] == "COUNTERBRANCH_EXPLICIT" for row in proof_rows), "independent torsion counterbranch retained")
    add("VAL2348_06_p4_rows_nonready", all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in p4_rows), "P4 spin rows are non-score-ready and nonclaim")
    add("VAL2348_07_p4_missing_inputs_flagged", any("MISSING_SPIN_TORSION_COEFFICIENT" in row["current_value"] for row in p4_rows) and any("MISSING_WEAK_FIELD_MAP" in row["current_value"] for row in p4_rows), "P4 rows explicitly flag missing coefficients and weak-field map")
    add("VAL2348_08_claim_gates_blocked", all(row["passed"] == "false" and row["valid_for_claim"] == "false" for row in claim_rows), "all claim gates remain blocked")
    add("VAL2348_09_refusals_block_shortcuts", all(row["allowed"] == "false" for row in refusal_rows), "shortcut claims refused")
    add("VAL2348_10_next_selected", any(row["row_id"] == "NEXT2348_0" and "projective-trace" in row["next_target"] for row in next_rows), "projective-trace next target recorded")
    add("VAL2348_11_branch_copies_parse", all(row["copy_exists"] == "true" and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse")
    generated_groups = [sources, audit_rows, proof_rows, p4_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows]
    add("VAL2348_12_no_claim_flags", all(row.get("valid_for_claim") == "false" for group in generated_groups for row in group), "no generated row is valid_for_claim=true")
    checkpoint_needles = [
        "SPIN_CONNECTION_COFRAME_OWNED_AUDIT_2348",
        "P4_AXIAL_TORSION_COMPONENT_ROW_2348",
        "JR2348_SPIN_CONNECTION",
        "Y5_R2FR_spin_connection",
    ]
    formalization_hits: list[str] = []
    if FORMALIZATION.exists():
        for needle in checkpoint_needles:
            try:
                result = subprocess.run(["rg", "-n", "--fixed-strings", needle, str(FORMALIZATION)], capture_output=True, text=True, timeout=30, check=False)
            except (OSError, subprocess.TimeoutExpired):
                result = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="")
            if result.returncode == 0 and result.stdout.strip():
                formalization_hits.extend(result.stdout.strip().splitlines())
    add("VAL2348_13_formalization_untouched_by_2348", not formalization_hits, "no 2348 checkpoint output appears in formalization-workbench")
    add("VAL2348_14_no_github_policy", any(row["row_id"] == "DEC2348_4_public_policy" and row["status"] == "NO_GITHUB_EVIDENCE_UPDATE" for row in decision_rows), "public GitHub update not recommended from 2348")
    add("VAL2348_OVERALL", all(row["status"] == "PASS" for row in rows), "2348 records exact conditional coframe-owned spin theorem, refuses public promotion, stages axial torsion P4 fallback, and selects projective-trace silence next.")
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    proof_rows: list[dict[str, Any]],
    p4_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2348 - Spin Connection Coframe Owned Or Axial Torsion P4 Row",
        "",
        "## Summary",
        "",
        "2348 takes the cleanest remaining connection head from 2347: `Delta_spin`.",
        "",
        "The good news is real: the coframe-owned spin-connection route is an exact conditional theorem.",
        "If the ordinary local branch writes spinors and spin transport with `omega_obs = omega_LC[e_obs]`,",
        "then the spin connection is a dependent coframe object. Its variation is counted in the",
        "coframe/Hilbert stress equation, not in a separate independent `Gamma_ind` equation.",
        "",
        "The hard stop is equally real: the parent action has not yet signed that variable-domain clause",
        "globally. Therefore `Delta_spin = 0` is not promoted as a public MTS theorem. The axial torsion /",
        "nonmetricity P4 row stays live, explicitly nonclaim and not score-ready.",
        "",
        "## Source Register",
        "",
        markdown_table(sources, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Spin Connection Coframe-Owned Audit",
        "",
        markdown_table(audit_rows, ["row_id", "clause", "formal_statement", "status", "obstruction", "effect_if_closed", "valid_for_claim"]),
        "",
        "## Chain Rule Proof Stack",
        "",
        markdown_table(proof_rows, ["row_id", "lemma", "statement", "proof_status", "missing_parent_input", "use", "valid_for_claim"]),
        "",
        "## Axial Torsion P4 Component Row",
        "",
        markdown_table(p4_rows, ["row_id", "quantity", "component", "formula", "units", "current_value", "source_path", "score_ready", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(decision_rows, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        markdown_table(next_rows, ["row_id", "next_target", "why", "route_type", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = build_sources()
    audit_rows = build_audit_rows()
    proof_rows = build_proof_rows()
    p4_rows = build_p4_rows()
    decision_rows = build_decision_rows()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["audit"], audit_rows)
    write_csv(OUTPUTS["proof"], proof_rows)
    write_csv(OUTPUTS["p4"], p4_rows)
    write_csv(OUTPUTS["decision"], decision_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = build_validation(sources, audit_rows, proof_rows, p4_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_doc(sources, audit_rows, proof_rows, p4_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows, validation_rows)
    print(f"2348 checkpoint generated: {DOC}")
    print(f"Validation: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

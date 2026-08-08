from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_BOUNDARY_DATA_LEAK_ZERO_CERTIFICATE_OR_FIRST_DELTA_REF_BOUND_ROW_2456"
CHECKPOINT_ID = "2456"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2456-Y5-R2FR-boundary-data-leak-zero-certificate-or-first-Delta-ref-bound-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2456_SOURCE_REGISTER.csv",
    "zero_audit": OUT / "P8_Y5_PARENT_QLOC_2456_BOUNDARY_LEAK_ZERO_AUDIT.csv",
    "dirichlet_branch": OUT / "P8_Y5_PARENT_QLOC_2456_DIRICHLET_REFERENCE_BRANCH.csv",
    "finite_bound_rows": OUT / "P8_Y5_PARENT_QLOC_2456_FIRST_DELTA_REF_BOUND_ROWS.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2456_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2456_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2456_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2456_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2456_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_zero_audit": QUEUE / "JR2456_BOUNDARY_LEAK_ZERO_AUDIT_NONCLAIM.csv",
    "queue_bound_rows": QUEUE / "JR2456_FIRST_DELTA_REF_BOUND_ROWS_NONCLAIM.csv",
    "hamiltonian_bound": HAMILTONIAN / "Delta_ref_boundary_leak_bound_rows_2456_NONCLAIM.csv",
    "local_bound": LOCAL_BOUNDS / "Delta_ref_boundary_leak_bound_rows_2456_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2456_00_2455_doc",
        "source_path": ROOT / "2455-Y5-R2FR-source-blind-boundary-reference-embedding-or-finite-Delta-ref-row.md",
        "needles": ["EMB2455_2_zero_condition", "DBR2455_0_partial_q_Bref_bound", "NEXT2455_0_selected", "VAL2455_OVERALL"],
        "role": "handoff deriving exact B_ref boundary leak law and selecting 2456",
    },
    {
        "source_id": "SRC2456_01_2455_zero_csv",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2455_BOUNDARY_DATA_ZERO_CERTIFICATE.csv",
        "needles": ["ZC2455_1_boundary_metric", "MISSING_BOUNDARY_METRIC_ZERO_CERTIFICATE", "ZC2455_6_same_frame_N_E"],
        "role": "machine-readable missing zero certificates from 2455",
    },
    {
        "source_id": "SRC2456_02_2455_bound_csv",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2455_DELTA_REF_BOUND_ROW_TEMPLATE.csv",
        "needles": ["DBR2455_0_partial_q_Bref_bound", "MISSING_BOUND_INPUTS", "DBR2455_4_total_Delta_ref_bound"],
        "role": "finite Delta_ref bound template that 2456 sharpens",
    },
    {
        "source_id": "SRC2456_03_tau_status",
        "source_path": ROOT / "1002-Y5-R10-Bref-stationary-tau-theorem-or-Delta-ref-time-profile-row.md",
        "needles": ["STA1002_1_tau_identity", "STA1002_6_theorem_verdict", "fail_current_claim"],
        "role": "tau identity and stationary-reference blocker",
    },
    {
        "source_id": "SRC2456_04_frame_status",
        "source_path": ROOT / "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
        "needles": ["CFA1003_1_quotient_coframe_descent", "CFA1003_6_theorem_verdict", "fail_current_claim"],
        "role": "coframe/reference covariance blocker",
    },
    {
        "source_id": "SRC2456_05_MHref_denominator",
        "source_path": ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
        "needles": ["CG1006_0_MHref_positive_same_frame", "ORBITAL_GM_IMPORT_NOT_EXCLUDED", "V1006_SUMMARY"],
        "role": "same-frame denominator and anti-circularity guardrail",
    },
    {
        "source_id": "SRC2456_06_reference_lock",
        "source_path": ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
        "needles": ["HRL1017_4_tau_lock", "HRL1017_6_FB5540_zero_law", "CG1017_0_reference_lock_written"],
        "role": "Hamiltonian reference/tau lock and Delta_ref blocker",
    },
    {
        "source_id": "SRC2456_07_boundary_exactness",
        "source_path": ROOT / "1843-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "needles": ["BDC1843_5_verdict", "ETB1843_1_weighted_Stokes_identity", "VAL1843_OVERALL"],
        "role": "boundary-domain/cohomology precedent and no-Stokes-shortcut guard",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: bool) -> str:
    return "True" if value else "False"


def metadata(valid_for_claim: bool = False, claim_allowed: bool = False) -> dict[str, str]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": truth(valid_for_claim),
        "claim_allowed": truth(claim_allowed),
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def cell(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def table(columns: list[str], rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                **metadata(),
                "source_id": source["source_id"],
                "source_path": str(path),
                "exists": truth(path.exists()),
                "needles": ";".join(source["needles"]),
                "missing_needles": ";".join(missing),
                "source_pass": truth(path.exists() and not missing),
                "role": source["role"],
            }
        )
    return rows


def zero_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "ZL2456_0_boundary_data_map",
            "component": "beta_ref=(S,sigma_AB,tau,C_top,B_ct)",
            "zero_condition": "D_q beta_ref=D_source beta_ref=0",
            "attempted_derivation": "If parent reference data beta_ref descends from a fixed boundary class before q/source/readout, the chain rule gives D_a beta_ref=0 for a in {q,source}.",
            "current_evidence": "2455 gives exact leak law, but no parent beta_ref descent theorem is signed.",
            "blocking_input": "MISSING_PARENT_BOUNDARY_DATA_DESCENT",
            "status": "BLOCKED_NONCLAIM",
        },
        {
            "audit_id": "ZL2456_1_surface_domain",
            "component": "S/domain",
            "zero_condition": "D_q S=D_source S=0",
            "attempted_derivation": "Choose the linking/worldtube boundary as part of the variational problem, not as a post-fit observed-GM surface.",
            "current_evidence": "1843 warns that boundary-domain exactness needs a signed domain/cohomology certificate; 2455 marks the surface rule missing.",
            "blocking_input": "MISSING_SOURCE_BLIND_SURFACE_DOMAIN_RULE",
            "status": "BLOCKED_NONCLAIM",
        },
        {
            "audit_id": "ZL2456_2_boundary_metric",
            "component": "sigma_AB",
            "zero_condition": "D_q sigma_AB=D_source sigma_AB=0",
            "attempted_derivation": "Dirichlet boundary ensemble imposes delta sigma_AB=0 on the reference boundary, so B_ref cannot inherit q/source leakage through intrinsic geometry.",
            "current_evidence": "This is a valid conditional route, but current MTS has not parent-signed the Dirichlet ensemble or its embedding Hessian.",
            "blocking_input": "MISSING_BOUNDARY_METRIC_ZERO_CERTIFICATE",
            "status": "BLOCKED_NONCLAIM",
        },
        {
            "audit_id": "ZL2456_3_tau",
            "component": "tau",
            "zero_condition": "D_q tau=D_source tau=0",
            "attempted_derivation": "Use one parent-selected time generator for reference charge, clocks, source and readout.",
            "current_evidence": "1002 and 1017 keep tau identity/lock conditional and unsigned.",
            "blocking_input": "MISSING_TAU_REFERENCE_ZERO_CERTIFICATE",
            "status": "BLOCKED_NONCLAIM",
        },
        {
            "audit_id": "ZL2456_4_topological_class",
            "component": "C_top",
            "zero_condition": "D_q C_top=D_source C_top=0",
            "attempted_derivation": "Treat C_top as a superselected boundary class fixed before source/readout variations.",
            "current_evidence": "This is compatible with the boundary-class strategy, but no parent topology/superselection certificate is present in the active chain.",
            "blocking_input": "MISSING_CTOP_SUPERSELECTION_CERTIFICATE",
            "status": "BLOCKED_NONCLAIM",
        },
        {
            "audit_id": "ZL2456_5_counterterm",
            "component": "B_ct",
            "zero_condition": "D_q B_ct=D_source B_ct=0",
            "attempted_derivation": "Counterterm convention must be fixed by the boundary variational principle and cannot be tuned to cancel source leakage.",
            "current_evidence": "2455 identifies B_ct as a leak channel; no counterterm rule/covariance proof is signed.",
            "blocking_input": "MISSING_COUNTERTERM_ZERO_CERTIFICATE",
            "status": "BLOCKED_NONCLAIM",
        },
        {
            "audit_id": "ZL2456_6_embedding_Hessian",
            "component": "L_embed and C_sigma",
            "zero_condition": "kernel(L_embed)=rigid isometries only, or finite C_sigma bound supplied",
            "attempted_derivation": "If delta sigma_AB=0, embedding drift is pure rigid reference gauge; otherwise bound response by C_sigma ||D_a sigma||.",
            "current_evidence": "2455 stages the Hessian/operator norm need, but no convex/regular embedding class or numeric norm is sourced.",
            "blocking_input": "MISSING_EMBEDDING_HESSIAN_OR_OPERATOR_NORM",
            "status": "BLOCKED_NONCLAIM",
        },
        {
            "audit_id": "ZL2456_7_same_frame_denominator",
            "component": "N_E or M_H_ref",
            "zero_condition": "positive same-frame normalization in the same tau/coframe",
            "attempted_derivation": "Normalize Delta_ref leakage only after parent supplies a positive source charge denominator, not by orbital GM or fitted readout.",
            "current_evidence": "1006 and 1017 explicitly block same-frame M_H_ref and reject orbital-GM denominator laundering.",
            "blocking_input": "MISSING_SAME_FRAME_N_E_OR_MHREF",
            "status": "BLOCKED_NONCLAIM",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def dirichlet_branch_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "branch_id_local": "DIR2456_0_definition",
            "statement": "Define beta_ref(Phi)=(S,sigma_AB,tau,C_top,B_ct) as the parent reference-boundary data.",
            "formula": "B_ref=B_ref[beta_ref(Phi)]",
            "proof_role": "turns the reference problem into a boundary-data map problem",
            "conditional_proof_status": "FORMAL_SETUP",
            "promotion_status": "NONCLAIM",
        },
        {
            "branch_id_local": "DIR2456_1_fixed_boundary_ensemble",
            "statement": "A Dirichlet/fixed-boundary ensemble restricts allowed local readout/source variations to ker(D beta_ref).",
            "formula": "T_D={delta Phi : D beta_ref(delta Phi)=0}",
            "proof_role": "prevents smuggling an observed-GM surface or fitted mass into the reference subtraction",
            "conditional_proof_status": "CONDITIONAL_PARENT_CONTRACT",
            "promotion_status": "NONCLAIM",
        },
        {
            "branch_id_local": "DIR2456_2_component_zero",
            "statement": "Inside T_D, the component leak vector vanishes.",
            "formula": "D_a S=D_a sigma_AB=D_a tau=D_a C_top=D_a B_ct=0 for a in {q,source}",
            "proof_role": "componentwise zero certificate for 2455 leak law",
            "conditional_proof_status": "CONDITIONAL_THEOREM",
            "promotion_status": "NONCLAIM",
        },
        {
            "branch_id_local": "DIR2456_3_chain_rule_zero",
            "statement": "The 2455 variation law then gives exact reference silence.",
            "formula": "D_a B_ref=<dB/dsigma,D_a sigma>+<dB/dtau,D_a tau>+<dB/dC_top,D_a C_top>+D_a B_ct=0",
            "proof_role": "would close partial_q Delta_ref=partial_source Delta_ref=0 if the parent action signs DIR2456_1",
            "conditional_proof_status": "PASS_AS_CONTRACT",
            "promotion_status": "NONCLAIM",
        },
        {
            "branch_id_local": "DIR2456_4_current_verdict",
            "statement": "Current MTS does not yet prove it is in the Dirichlet/fixed-boundary ensemble.",
            "formula": "parent action must supply beta_ref descent, tau/coframe lock, C_top superselection, B_ct rule, embedding Hessian, and same-frame denominator",
            "proof_role": "prevents promoting the branch to local-GR evidence",
            "conditional_proof_status": "FAIL_CURRENT_CLAIM_BUT_ROUTE_IS_SHARPENED",
            "promotion_status": "BLOCKED",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def finite_bound_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "DBR2456_0_partial_q_Bref_bound",
            "quantity": "partial_q_Bref_over_N_E",
            "bound_formula": "(C_sigma*norm_Dq_sigma + C_tau*norm_Dq_tau + C_top*abs_Dq_Ctop + abs_Dq_Bct)/N_E",
            "required_inputs": "C_sigma;norm_Dq_sigma;C_tau;norm_Dq_tau;C_top;abs_Dq_Ctop;abs_Dq_Bct;N_E;units;source_path;equation_ref",
            "current_value": "MISSING_BOUND_INPUTS",
            "units": "dimensionless_after_N_E_normalization",
            "claim_blocker": "MISSING_NUMERIC_OR_THEOREM_ZERO_COMPONENTS",
            "score_ready": "False",
        },
        {
            "row_id": "DBR2456_1_partial_source_Bref_bound",
            "quantity": "partial_source_Bref_over_N_E",
            "bound_formula": "(C_sigma*norm_Dsource_sigma + C_tau*norm_Dsource_tau + C_top*abs_Dsource_Ctop + abs_Dsource_Bct)/N_E",
            "required_inputs": "C_sigma;norm_Dsource_sigma;C_tau;norm_Dsource_tau;C_top;abs_Dsource_Ctop;abs_Dsource_Bct;N_E;units;source_path;equation_ref",
            "current_value": "MISSING_BOUND_INPUTS",
            "units": "dimensionless_after_N_E_normalization",
            "claim_blocker": "MISSING_NUMERIC_OR_THEOREM_ZERO_COMPONENTS",
            "score_ready": "False",
        },
        {
            "row_id": "DBR2456_2_boundary_metric_leak_norm",
            "quantity": "C_sigma*norm_Da_sigma/N_E",
            "bound_formula": "max_a C_sigma ||D_a sigma_AB||/N_E for a in {q,source}",
            "required_inputs": "regular_embedding_class;C_sigma;norm_Dq_sigma;norm_Dsource_sigma;N_E;source_path",
            "current_value": "MISSING_EMBEDDING_OPERATOR_NORM_AND_DSIGMA_PROFILE",
            "units": "dimensionless_after_N_E_normalization",
            "claim_blocker": "MISSING_BOUNDARY_METRIC_PROFILE",
            "score_ready": "False",
        },
        {
            "row_id": "DBR2456_3_tau_leak_norm",
            "quantity": "C_tau*norm_Da_tau/N_E",
            "bound_formula": "max_a C_tau ||D_a tau||/N_E for a in {q,source}",
            "required_inputs": "tau_frame_id;C_tau;norm_Dq_tau;norm_Dsource_tau;N_E;source_path",
            "current_value": "MISSING_TAU_LOCK_OR_TAU_PROFILE",
            "units": "dimensionless_after_N_E_normalization",
            "claim_blocker": "MISSING_TAU_REFERENCE_ZERO_OR_BOUND",
            "score_ready": "False",
        },
        {
            "row_id": "DBR2456_4_Ctop_and_counterterm_leak_norm",
            "quantity": "(C_top*abs_Da_Ctop+abs_Da_Bct)/N_E",
            "bound_formula": "max_a (C_top |D_a C_top|+|D_a B_ct|)/N_E for a in {q,source}",
            "required_inputs": "C_top_superselection_rule;B_ct_rule;Dq_Ctop;Dsource_Ctop;Dq_Bct;Dsource_Bct;N_E;source_path",
            "current_value": "MISSING_TOPOLOGY_AND_COUNTERTERM_PROFILES",
            "units": "dimensionless_after_N_E_normalization",
            "claim_blocker": "MISSING_CTOP_OR_COUNTERTERM_CERTIFICATE",
            "score_ready": "False",
        },
        {
            "row_id": "DBR2456_5_total_Delta_ref_bound",
            "quantity": "Delta_ref_q_source_component_over_N_E",
            "bound_formula": "abs(partial_q_Bref*Delta_q)+abs(partial_source_Bref*Delta_source) over N_E with no cancellation",
            "required_inputs": "DBR2456_0;DBR2456_1;Delta_q_scale;Delta_source_scale;same_frame_N_E;source_path",
            "current_value": "NOT_COMPUTED_COMPONENTS_MISSING",
            "units": "dimensionless",
            "claim_blocker": "MISSING_COMPONENTS_AND_DENOMINATOR",
            "score_ready": "False",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2456_0_dirichlet_contract",
            "claim": "Dirichlet/fixed-boundary contract would make B_ref q/source silent",
            "gate_status": "PASS_AS_CONTRACT",
            "reason": "2456 proves the chain-rule implication from fixed beta_ref to D_a B_ref=0",
            "gate_pass": "True",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2456_1_parent_signed_zero",
            "claim": "Current parent action signs D_q/source beta_ref=0",
            "gate_status": "BLOCKED",
            "reason": "surface, sigma_AB, tau, C_top, B_ct, embedding Hessian and same-frame denominator remain unsigned",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2456_2_first_bound_row",
            "claim": "Delta_ref boundary leak has a source-backed finite numerical bound",
            "gate_status": "BLOCKED",
            "reason": "2456 writes schema rows but no numeric/source-backed norms or denominator exist",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2456_3_no_shortcuts",
            "claim": "Observed-GM surface, orbital GM denominator, or counterterm cancellation can substitute for the parent proof",
            "gate_status": "REFUSED",
            "reason": "that would launder the readout into the theorem and break the local-GR derivation standard",
            "gate_pass": "True",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2456_4_local_GR",
            "claim": "RCS2446_0, S_E^q, PPN, Newton or local-GR branch passes",
            "gate_status": "BLOCKED",
            "reason": "Delta_ref/reference-lock pieces are now sharper but not closed",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2456_0_zero_proof_attempted",
            "decision": "Do not claim componentwise boundary-data zero from current MTS.",
            "reason": "the zero proof reduces exactly to parent-signed beta_ref descent/fixed-boundary ensemble, which is not present yet",
            "effect": "Delta_ref theorem-zero stays blocked",
        },
        {
            "decision_id": "DEC2456_1_route_retained",
            "decision": "Retain the Dirichlet/fixed-boundary reference route as the least-smuggled proof path.",
            "reason": "it derives D_a B_ref=0 by variational boundary conditions rather than by plateau axiom or numerical cancellation",
            "effect": "next work should construct the parent action boundary contract",
        },
        {
            "decision_id": "DEC2456_2_bound_rows_staged",
            "decision": "Stage the first Delta_ref boundary leak bound rows as nonclaim.",
            "reason": "if the parent zero route fails, the exact 2455 law already supplies the honest residual vector",
            "effect": "source acquisition can fill norms without changing claims",
        },
        {
            "decision_id": "DEC2456_3_no_github",
            "decision": "Keep this checkpoint private and do not update GitHub.",
            "reason": "the active branch is still proof-gate scaffolding and would be easy to misread publicly",
            "effect": "all outputs stay in post-checkpoint-work",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2456_0_selected",
            "selection_status": "selected",
            "target_file": "2457-Y5-R2FR-parent-Dirichlet-boundary-action-contract-or-Delta-ref-bound-values.md",
            "target_script": "scripts/Y5_R2FR_parent_Dirichlet_boundary_action_contract_or_Delta_ref_bound_values_2457.py",
            "task": "construct the parent action boundary contract that fixes beta_ref=(S,sigma_AB,tau,C_top,B_ct) before q/source/readout, or fill first real Delta_ref leak norms and same-frame denominator rows",
            "acceptance_target": "parent-signed fixed-boundary ensemble with tau/coframe/C_top/B_ct/embedding clauses, or numeric/source-backed nonclaim bound rows",
            "guardrails": "no plateau axiom; no observed-GM/fitted-mass boundary; no orbital-GM denominator; no counterterm cancellation; no local-GR claim; no GitHub",
        }
    ]
    return [{**metadata(), **row} for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("queue_zero_audit", OUTPUTS["zero_audit"], COPY_TARGETS["queue_zero_audit"]),
        ("queue_bound_rows", OUTPUTS["finite_bound_rows"], COPY_TARGETS["queue_bound_rows"]),
        ("hamiltonian_bound", OUTPUTS["finite_bound_rows"], COPY_TARGETS["hamiltonian_bound"]),
        ("local_bound", OUTPUTS["finite_bound_rows"], COPY_TARGETS["local_bound"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copy_specs:
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, target)
        rows.append(
            {
                **metadata(),
                "copy_id": copy_id,
                "source_path": str(source),
                "target_path": str(target),
                "source_exists": truth(source.exists()),
                "target_exists": truth(target.exists()),
            }
        )
    return rows


def csv_parse_status(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as exc:  # pragma: no cover - diagnostic only
        return False, 0, repr(exc)


def formalization_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    hits: list[Path] = []
    for path in FORMALIZATION.rglob("*2456*"):
        hits.append(path)
    return hits


def validation_rows(
    source_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    dirichlet_rows: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "notes": notes,
                "detail": detail,
            }
        )

    add(
        "VAL2456_00_sources_exist",
        all(row["source_pass"] == "True" for row in source_rows),
        "all cited source paths exist and needles are present",
        ";".join(row["source_id"] for row in source_rows if row["source_pass"] != "True"),
    )
    add(
        "VAL2456_01_zero_audit_componentwise",
        len(zero_rows) >= 8 and all(row["status"] == "BLOCKED_NONCLAIM" for row in zero_rows),
        "all boundary-data leak components are audited and remain nonclaim",
    )
    add(
        "VAL2456_02_dirichlet_contract_written",
        any(row["branch_id_local"] == "DIR2456_3_chain_rule_zero" and row["conditional_proof_status"] == "PASS_AS_CONTRACT" for row in dirichlet_rows),
        "Dirichlet/fixed-boundary chain-rule zero is written as a contract",
    )
    add(
        "VAL2456_03_current_zero_not_promoted",
        any(row["branch_id_local"] == "DIR2456_4_current_verdict" and row["promotion_status"] == "BLOCKED" for row in dirichlet_rows),
        "current parent action does not promote the zero proof",
    )
    add(
        "VAL2456_04_bound_rows_nonclaim",
        len(finite_rows) >= 6 and all(row["valid_for_claim"] == "False" and row["score_ready"] == "False" for row in finite_rows),
        "first Delta_ref boundary leak rows are schema-only/nonclaim",
    )
    add(
        "VAL2456_05_claim_gates_safe",
        all(row["claim_allowed"] == "False" for row in gate_rows) and any(row["gate_id"] == "GATE2456_4_local_GR" and row["gate_status"] == "BLOCKED" for row in gate_rows),
        "no local-GR/PPN/Newton claim is allowed from 2456",
    )
    add(
        "VAL2456_06_next_target_written",
        len(next_rows) == 1 and next_rows[0]["route_id"] == "NEXT2456_0_selected",
        "2457 parent Dirichlet boundary-action contract target selected",
    )
    add(
        "VAL2456_07_branch_copies",
        len(branch_rows) == 4 and all(row["target_exists"] == "True" for row in branch_rows),
        "nonclaim branch copies exist",
    )
    hits = formalization_hits()
    add(
        "VAL2456_08_no_formalization_artifacts",
        not hits,
        "no 2456 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in hits),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parse_status(path)
        add(
            f"VAL2456_CSV_{path.stem}",
            ok,
            f"CSV parses with {count} rows" if ok else "CSV parse failed",
            detail or str(path),
        )

    for key, path in COPY_TARGETS.items():
        ok, count, detail = csv_parse_status(path)
        add(
            f"VAL2456_COPY_CSV_{key}",
            ok,
            f"copy CSV parses with {count} rows" if ok else "copy CSV parse failed",
            detail or str(path),
        )

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2456_OVERALL",
        overall,
        "2456 proves the fixed-boundary route as a conditional contract and stages nonclaim Delta_ref bound rows while keeping local-GR blocked",
    )
    return [{**metadata(), **row} for row in rows]


def write_doc(
    source_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    dirichlet_rows: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_rows_value: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validation_rows_value: list[dict[str, Any]],
) -> None:
    doc = "\n\n".join(
        [
            "# 2456 Y5 R2FR Boundary Data Leak Zero Certificate Or First Delta-ref Bound Row",
            "**Status:** zero proof attempted. The useful result is a sharpened Dirichlet/fixed-boundary route: if the parent action fixes `beta_ref=(S,sigma_AB,tau,C_top,B_ct)` before local q/source/readout variations, then the 2455 boundary-reference leak law gives `D_a B_ref=0`. Current MTS does not yet sign that parent boundary contract, so no `Delta_ref`, `RCS2446_0`, `S_E^q`, PPN, Newton, or local-GR pass is claimed.",
            "**Private reading:** this is not a dead end and not a victory lap. It is the clean boxing-footwork version: the local branch can win on derivation if we can show the parent action owns a fixed boundary ensemble. Without that, the honest fallback is a finite residual vector, not a theorem-zero switch.",
            "## Source Register\n" + table(["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"], source_rows),
            "## Boundary Data Leak Zero Audit\n" + table(["audit_id", "component", "zero_condition", "attempted_derivation", "current_evidence", "blocking_input", "status"], zero_rows),
            "## Dirichlet Reference Branch Contract\n" + table(["branch_id_local", "statement", "formula", "proof_role", "conditional_proof_status", "promotion_status"], dirichlet_rows),
            "## First Delta-ref Boundary Leak Bound Rows\n" + table(["row_id", "quantity", "bound_formula", "required_inputs", "current_value", "units", "claim_blocker", "score_ready"], finite_rows),
            "## Claim Gates\n" + table(["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"], gate_rows),
            "## Decision Ledger\n" + table(["decision_id", "decision", "reason", "effect"], decision_rows_value),
            "## Next Target\n" + table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], next_rows),
            "## Branch Copies\n" + table(["copy_id", "source_path", "target_path", "source_exists", "target_exists"], branch_rows),
            "## Validation\n" + table(["check_id", "status", "notes", "detail"], validation_rows_value),
        ]
    )
    DOC.write_text(doc + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    zero_rows = zero_audit_rows()
    dirichlet_rows = dirichlet_branch_rows()
    finite_rows = finite_bound_rows()
    gate_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["zero_audit"], zero_rows)
    write_csv(OUTPUTS["dirichlet_branch"], dirichlet_rows)
    write_csv(OUTPUTS["finite_bound_rows"], finite_rows)
    write_csv(OUTPUTS["claim_gates"], gate_rows)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validations = validation_rows(source_rows, zero_rows, dirichlet_rows, finite_rows, gate_rows, next_rows, branch_rows)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(source_rows, zero_rows, dirichlet_rows, finite_rows, gate_rows, decisions, next_rows, branch_rows, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_DIRICHLET_BOUNDARY_ACTION_CONTRACT_OR_DELTA_REF_BOUND_VALUES_2457"
CHECKPOINT_ID = "2457"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2457-Y5-R2FR-parent-Dirichlet-boundary-action-contract-or-Delta-ref-bound-values.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2457_SOURCE_REGISTER.csv",
    "parent_contract": OUT / "P8_Y5_PARENT_QLOC_2457_PARENT_ACTION_CONTRACT.csv",
    "domain_theorem": OUT / "P8_Y5_PARENT_QLOC_2457_VARIATIONAL_DOMAIN_THEOREM.csv",
    "signature_audit": OUT / "P8_Y5_PARENT_QLOC_2457_CONTRACT_SIGNATURE_AUDIT.csv",
    "bound_inputs": OUT / "P8_Y5_PARENT_QLOC_2457_DELTA_REF_BOUND_VALUE_INPUTS.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2457_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2457_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2457_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2457_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2457_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_contract": QUEUE / "JR2457_PARENT_DIRICHLET_BOUNDARY_ACTION_CONTRACT_NONCLAIM.csv",
    "queue_signature": QUEUE / "JR2457_CONTRACT_SIGNATURE_AUDIT_NONCLAIM.csv",
    "hamiltonian_bound_inputs": HAMILTONIAN / "Delta_ref_bound_value_inputs_2457_NONCLAIM.csv",
    "local_bound_inputs": LOCAL_BOUNDS / "Delta_ref_bound_value_inputs_2457_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2457_00_2456_doc",
        "source_path": ROOT / "2456-Y5-R2FR-boundary-data-leak-zero-certificate-or-first-Delta-ref-bound-row.md",
        "needles": ["DIR2456_3_chain_rule_zero", "NEXT2456_0_selected", "VAL2456_OVERALL"],
        "role": "handoff proving fixed-boundary route as conditional contract",
    },
    {
        "source_id": "SRC2457_01_2456_branch",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2456_DIRICHLET_REFERENCE_BRANCH.csv",
        "needles": ["DIR2456_3_chain_rule_zero", "PASS_AS_CONTRACT", "DIR2456_4_current_verdict"],
        "role": "machine-readable Dirichlet branch contract",
    },
    {
        "source_id": "SRC2457_02_2456_zero_audit",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2456_BOUNDARY_LEAK_ZERO_AUDIT.csv",
        "needles": ["ZL2456_0_boundary_data_map", "MISSING_PARENT_BOUNDARY_DATA_DESCENT", "ZL2456_7_same_frame_denominator"],
        "role": "componentwise blockers for boundary data leak zero proof",
    },
    {
        "source_id": "SRC2457_03_2456_bound_rows",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2456_FIRST_DELTA_REF_BOUND_ROWS.csv",
        "needles": ["DBR2456_0_partial_q_Bref_bound", "MISSING_BOUND_INPUTS", "DBR2456_5_total_Delta_ref_bound"],
        "role": "nonclaim finite bound fallback rows",
    },
    {
        "source_id": "SRC2457_04_2455_law",
        "source_path": ROOT / "2455-Y5-R2FR-source-blind-boundary-reference-embedding-or-finite-Delta-ref-row.md",
        "needles": ["EMB2455_1_variation_law", "EMB2455_2_zero_condition", "EMB2455_5_verdict"],
        "role": "exact variation law that the parent contract must feed",
    },
    {
        "source_id": "SRC2457_05_1017_reference_lock",
        "source_path": ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
        "needles": ["HRL1017_2_reference_lock", "HRL1017_4_tau_lock", "CG1017_0_reference_lock_written"],
        "role": "Hamiltonian reference and tau-lock requirements",
    },
    {
        "source_id": "SRC2457_06_1843_boundary_guard",
        "source_path": ROOT / "1843-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "needles": ["BDC1843_5_verdict", "ETB1843_1_weighted_Stokes_identity", "VAL1843_OVERALL"],
        "role": "boundary exactness guard against Stokes-only shortcuts",
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


def parent_contract_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "contract_id": "PAC2457_0_parent_fields",
            "clause": "Parent configuration space contains bulk fields Phi plus a fixed boundary datum beta_0.",
            "formula": "C_D(beta_0)={Phi : beta_ref(Phi)|dM=beta_0}",
            "derivation_role": "turns boundary reference silence into a property of the configuration bundle",
            "current_signature": "MISSING_PARENT_CONFIGURATION_BUNDLE",
            "status": "CONTRACT_WRITTEN_NOT_SIGNED",
        },
        {
            "contract_id": "PAC2457_1_action_form",
            "clause": "Parent action is varied at fixed beta_0.",
            "formula": "S_D[Phi;beta_0]=int_M L_MTS(Phi)+int_dM B_D(Phi;beta_0)+S_matter[q(Phi),Psi;beta_0]",
            "derivation_role": "makes beta_0 a boundary condition, not a fitted output or readout-dependent surface",
            "current_signature": "MISSING_PARENT_ACTION_WITH_FIXED_BETA0",
            "status": "CONTRACT_WRITTEN_NOT_SIGNED",
        },
        {
            "contract_id": "PAC2457_2_variation_domain",
            "clause": "Allowed q/source/readout variations are tangent to C_D(beta_0).",
            "formula": "delta_a Phi in T_Phi C_D(beta_0) => D_a beta_ref=0 for a in {q,source}",
            "derivation_role": "supplies the missing componentwise zero in 2456 without a plateau axiom",
            "current_signature": "MISSING_VARIATIONAL_DOMAIN_CERTIFICATE",
            "status": "CONDITIONAL_THEOREM",
        },
        {
            "contract_id": "PAC2457_3_reference_functional",
            "clause": "B_ref is a functional only of beta_ref and fixed counterterm class.",
            "formula": "B_ref(Phi)=B_ref[beta_ref(Phi);B_ct(beta_0,C_top0)]",
            "derivation_role": "prevents hidden dependence on source mass, observed-GM radius, local q, or frame readout",
            "current_signature": "MISSING_REFERENCE_FUNCTIONAL_OWNERSHIP",
            "status": "CONTRACT_WRITTEN_NOT_SIGNED",
        },
        {
            "contract_id": "PAC2457_4_tau_coframe_lock",
            "clause": "The same tau/coframe defines source charge, reference charge, clocks, and readout.",
            "formula": "tau_source=tau_charge=tau_clock=tau_boundary=tau_readout=tau_0 and D_a tau_0=0",
            "derivation_role": "connects reference silence to same-frame normalization instead of a reference-only trick",
            "current_signature": "MISSING_TAU_COFRAME_LOCK",
            "status": "CONTRACT_WRITTEN_NOT_SIGNED",
        },
        {
            "contract_id": "PAC2457_5_no_shortcut_guard",
            "clause": "No observed-GM/fitted surface, orbital-GM denominator, or counterterm cancellation can fill a missing clause.",
            "formula": "claim_allowed=False if beta_0, N_E/M_H_ref, or B_ct are inferred from the target readout",
            "derivation_role": "keeps local-GR reduction derivational rather than post-hoc",
            "current_signature": "GUARDRAIL_INSTALLED",
            "status": "GUARDRAIL_PASS_NONCLAIM",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def domain_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "VDT2457_0_hypotheses",
            "statement": "Assume Phi(a) is a q/source variation curve inside C_D(beta_0).",
            "formula": "beta_ref(Phi(a))=beta_0 for all a near 0",
            "proof_step": "differentiate the fixed-boundary constraint",
            "result": "D_a beta_ref=0",
            "promotion_status": "CONDITIONAL_ONLY",
        },
        {
            "theorem_id": "VDT2457_1_component_expansion",
            "statement": "The fixed beta_ref condition expands componentwise.",
            "formula": "D_a S=D_a sigma_AB=D_a tau=D_a C_top=D_a B_ct=0",
            "proof_step": "apply projections from beta_ref to each component",
            "result": "all 2455 leak channels vanish inside the domain",
            "promotion_status": "CONDITIONAL_ONLY",
        },
        {
            "theorem_id": "VDT2457_2_chain_rule_to_Bref",
            "statement": "Insert component zeros into the 2455 variation law.",
            "formula": "D_a B_ref=<dB/dsigma,D_a sigma>+<dB/dtau,D_a tau>+<dB/dC_top,D_a C_top>+D_a B_ct=0",
            "proof_step": "all terms vanish independently; no cancellation is used",
            "result": "partial_q B_ref=partial_source B_ref=0",
            "promotion_status": "PASS_AS_CONTRACT",
        },
        {
            "theorem_id": "VDT2457_3_to_Delta_ref",
            "statement": "If Delta_ref depends on the reference branch only through B_ref/H_ref fixed by beta_0, its q/source derivative also vanishes.",
            "formula": "D_a Delta_ref=0 provided H_ref=H_ref[beta_0] and N_E/M_H_ref is same-frame parent-owned",
            "proof_step": "compose the fixed-reference result with same-frame denominator ownership",
            "result": "would close the reference part of RCS2446_0/FB554_0",
            "promotion_status": "BLOCKED_ON_DENOMINATOR_AND_PARENT_SIGNATURE",
        },
        {
            "theorem_id": "VDT2457_4_current_verdict",
            "statement": "The proof is mathematically exact but not currently claim-grade.",
            "formula": "PAC2457 clauses signed => D_a Delta_ref=0; current corpus lacks the signatures",
            "proof_step": "separate theorem contract from active evidence claim",
            "result": "FAIL_CURRENT_CLAIM_BUT_PARENT_ACTION_CONTRACT_IS_EXACT",
            "promotion_status": "BLOCKED",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def signature_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("SIG2457_0_configuration_bundle", "C_D(beta_0) declared by the parent theory", "MISSING_PARENT_CONFIGURATION_BUNDLE", "without this, fixed beta_0 is an imposed closure"),
        ("SIG2457_1_boundary_surface", "S/domain fixed before source/readout", "MISSING_SOURCE_BLIND_SURFACE_DOMAIN_RULE", "prevents observed-GM boundary laundering"),
        ("SIG2457_2_boundary_metric", "sigma_AB fixed or source-blind by parent boundary condition", "MISSING_BOUNDARY_METRIC_ZERO_CERTIFICATE", "main B_ref embedding input"),
        ("SIG2457_3_tau_coframe", "tau/coframe fixed and shared by charge/clocks/readout", "MISSING_TAU_COFRAME_LOCK", "same-frame reference and PPN bridge"),
        ("SIG2457_4_topology", "C_top superselected before local variation", "MISSING_CTOP_SUPERSELECTION_CERTIFICATE", "prevents source-selected class switching"),
        ("SIG2457_5_counterterm", "B_ct fixed by boundary variational principle", "MISSING_COUNTERTERM_ZERO_CERTIFICATE", "prevents cancellation-based proof"),
        ("SIG2457_6_embedding", "embedding Hessian/operator norm controlled", "MISSING_EMBEDDING_HESSIAN_OR_OPERATOR_NORM", "prevents hidden non-rigid reference drift"),
        ("SIG2457_7_denominator", "positive same-frame N_E/M_H_ref exists", "MISSING_SAME_FRAME_N_E_OR_MHREF", "normalizes residual without circular orbital-GM import"),
    ]
    return [
        {
            **metadata(),
            "signature_id": signature_id,
            "required_signature": required,
            "current_fill": current,
            "why_required": why,
            "status": "BLOCKED_NONCLAIM",
        }
        for signature_id, required, current, why in rows
    ]


def bound_input_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "input_id": "BVI2457_0_use_zero_contract_if_signed",
            "quantity": "Delta_ref_q_source_component_over_N_E",
            "value_rule": "0 only if all PAC2457/SIG2457 clauses are parent-signed",
            "current_value": "NOT_ALLOWED_AS_VALUE",
            "required_source": "parent action with fixed beta_0 plus same-frame denominator proof",
            "valid_for_claim": "False",
            "status": "BLOCKED_NONCLAIM",
        },
        {
            "input_id": "BVI2457_1_metric_norm_value",
            "quantity": "C_sigma*max(||D_q sigma||,||D_source sigma||)/N_E",
            "value_rule": "finite numeric/source-backed upper bound",
            "current_value": "MISSING_VALUE",
            "required_source": "embedding operator norm and boundary metric derivative profile",
            "valid_for_claim": "False",
            "status": "MISSING_BOUND_VALUE",
        },
        {
            "input_id": "BVI2457_2_tau_norm_value",
            "quantity": "C_tau*max(||D_q tau||,||D_source tau||)/N_E",
            "value_rule": "finite numeric/source-backed upper bound",
            "current_value": "MISSING_VALUE",
            "required_source": "tau lock theorem or tau variation profile",
            "valid_for_claim": "False",
            "status": "MISSING_BOUND_VALUE",
        },
        {
            "input_id": "BVI2457_3_topology_counterterm_value",
            "quantity": "max(C_top|D_a C_top|+|D_a B_ct|)/N_E",
            "value_rule": "zero by superselection/counterterm rule or finite sourced bound",
            "current_value": "MISSING_VALUE",
            "required_source": "C_top rule, B_ct rule, derivative profile and N_E",
            "valid_for_claim": "False",
            "status": "MISSING_BOUND_VALUE",
        },
        {
            "input_id": "BVI2457_4_total_first_bound_value",
            "quantity": "first claim-grade Delta_ref boundary leak bound",
            "value_rule": "sum absolute components only; no cancellation",
            "current_value": "NOT_COMPUTED_COMPONENTS_MISSING",
            "required_source": "BVI2457_1 through BVI2457_3 plus same-frame denominator",
            "valid_for_claim": "False",
            "status": "BLOCKED_NONCLAIM",
        },
    ]
    return [{**metadata(), **row, "claim_allowed": "False"} for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2457_0_contract_exact",
            "claim": "The exact parent action contract sufficient for B_ref q/source silence is written.",
            "gate_status": "PASS_AS_CONTRACT",
            "reason": "PAC2457 and VDT2457 reduce the problem to fixed beta_0 variational ownership",
            "gate_pass": "True",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2457_1_parent_signature",
            "claim": "The current corpus proves the parent action satisfies PAC2457.",
            "gate_status": "BLOCKED",
            "reason": "no source file yet signs the configuration bundle, boundary action, tau/coframe lock, topology, counterterm, embedding and denominator clauses",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2457_2_zero_value",
            "claim": "Delta_ref q/source leak equals zero for current MTS.",
            "gate_status": "BLOCKED",
            "reason": "zero value is allowed only after all contract signatures are present",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2457_3_bound_value",
            "claim": "A finite source-backed nonzero Delta_ref bound is ready.",
            "gate_status": "BLOCKED",
            "reason": "bound value input rows are schema-only with missing values",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2457_4_local_GR",
            "claim": "Local GR/Newton/PPN branch passes.",
            "gate_status": "BLOCKED",
            "reason": "reference silence is now exactly contracted but not parent-signed or normalized",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2457_0_contract_not_closure",
            "decision": "Treat fixed boundary data as a parent-action contract, not a plateau axiom.",
            "reason": "the zero follows from the variational domain if the parent theory owns beta_0",
            "effect": "the local branch has a derivational route instead of a closure-only patch",
        },
        {
            "decision_id": "DEC2457_1_no_promotion",
            "decision": "Do not promote Delta_ref=0 in the current corpus.",
            "reason": "the exact contract is not the same as evidence that MTS already satisfies it",
            "effect": "RCS2446_0/S_E^q/local-GR remain blocked",
        },
        {
            "decision_id": "DEC2457_2_next_hunt",
            "decision": "Search the corpus for an existing parent action/signature matching PAC2457 before inventing new physics.",
            "reason": "if your older work already contains the fixed-boundary idea, we should connect it rather than create duplicate structure",
            "effect": "2458 should be a source hunt plus promote-or-demote gate",
        },
        {
            "decision_id": "DEC2457_3_fallback_values",
            "decision": "If no parent action signature exists, fill finite bound values instead of forcing zero.",
            "reason": "the same leak law gives honest residuals and preserves empirical testability",
            "effect": "bound-input rows are queued as nonclaim",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2457_0_selected",
            "selection_status": "selected",
            "target_file": "2458-Y5-R2FR-parent-action-signature-hunt-or-reference-route-demotion.md",
            "target_script": "scripts/Y5_R2FR_parent_action_signature_hunt_or_reference_route_demotion_2458.py",
            "task": "scan the corpus for an actual parent action/boundary-condition signature matching PAC2457; if absent, demote the zero route to an explicit closure and move to finite Delta_ref bound values",
            "acceptance_target": "source-backed signature rows for fixed beta_0/tau/coframe/C_top/B_ct/embedding/N_E, or explicit demotion plus first bound-value acquisition ledger",
            "guardrails": "no new axiom unless labeled closure; no GR import; no observed-GM boundary; no orbital-GM denominator; no local-GR claim; no GitHub",
        }
    ]
    return [{**metadata(), **row} for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("queue_contract", OUTPUTS["parent_contract"], COPY_TARGETS["queue_contract"]),
        ("queue_signature", OUTPUTS["signature_audit"], COPY_TARGETS["queue_signature"]),
        ("hamiltonian_bound_inputs", OUTPUTS["bound_inputs"], COPY_TARGETS["hamiltonian_bound_inputs"]),
        ("local_bound_inputs", OUTPUTS["bound_inputs"], COPY_TARGETS["local_bound_inputs"]),
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
    return list(FORMALIZATION.rglob("*2457*"))


def validation_rows(
    source_rows: list[dict[str, Any]],
    parent_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    signature_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append({"check_id": check_id, "status": "PASS if passed else FAIL", "notes": notes, "detail": detail})
        rows[-1]["status"] = "PASS" if passed else "FAIL"

    add(
        "VAL2457_00_sources_exist",
        all(row["source_pass"] == "True" for row in source_rows),
        "all cited source paths exist and needles are present",
        ";".join(row["source_id"] for row in source_rows if row["source_pass"] != "True"),
    )
    add(
        "VAL2457_01_parent_contract_written",
        len(parent_rows) >= 6 and any(row["contract_id"] == "PAC2457_2_variation_domain" for row in parent_rows),
        "parent Dirichlet boundary-action contract clauses are written",
    )
    add(
        "VAL2457_02_chain_rule_theorem_exact",
        any(row["theorem_id"] == "VDT2457_2_chain_rule_to_Bref" and row["promotion_status"] == "PASS_AS_CONTRACT" for row in theorem_rows),
        "fixed beta_0 implies D_a B_ref=0 as a conditional theorem",
    )
    add(
        "VAL2457_03_current_claim_blocked",
        any(row["theorem_id"] == "VDT2457_4_current_verdict" and row["promotion_status"] == "BLOCKED" for row in theorem_rows),
        "current corpus is not promoted to Delta_ref zero",
    )
    add(
        "VAL2457_04_signature_audit_blocked",
        len(signature_rows) >= 8 and all(row["status"] == "BLOCKED_NONCLAIM" for row in signature_rows),
        "all required signatures remain explicit blockers",
    )
    add(
        "VAL2457_05_bound_values_nonclaim",
        len(bound_rows) >= 5 and all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in bound_rows),
        "bound value rows remain nonclaim and uncomputed",
    )
    add(
        "VAL2457_06_claim_gates_safe",
        all(row["claim_allowed"] == "False" for row in gate_rows) and any(row["gate_id"] == "GATE2457_4_local_GR" and row["gate_status"] == "BLOCKED" for row in gate_rows),
        "local-GR/PPN/Newton claims remain blocked",
    )
    add(
        "VAL2457_07_next_target_written",
        len(next_rows) == 1 and next_rows[0]["route_id"] == "NEXT2457_0_selected",
        "2458 parent action signature hunt target selected",
    )
    add(
        "VAL2457_08_branch_copies",
        len(branch_rows) == 4 and all(row["target_exists"] == "True" for row in branch_rows),
        "nonclaim branch copies exist",
    )
    hits = formalization_hits()
    add(
        "VAL2457_09_no_formalization_artifacts",
        not hits,
        "no 2457 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in hits),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parse_status(path)
        add(
            f"VAL2457_CSV_{path.stem}",
            ok,
            f"CSV parses with {count} rows" if ok else "CSV parse failed",
            detail or str(path),
        )

    for key, path in COPY_TARGETS.items():
        ok, count, detail = csv_parse_status(path)
        add(
            f"VAL2457_COPY_CSV_{key}",
            ok,
            f"copy CSV parses with {count} rows" if ok else "copy CSV parse failed",
            detail or str(path),
        )

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2457_OVERALL",
        overall,
        "2457 writes the exact parent Dirichlet boundary action contract and keeps it nonclaim until sourced",
    )
    return [{**metadata(), **row} for row in rows]


def write_doc(
    source_rows: list[dict[str, Any]],
    parent_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    signature_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = "\n\n".join(
        [
            "# 2457 Y5 R2FR Parent Dirichlet Boundary Action Contract Or Delta-ref Bound Values",
            "**Status:** exact parent-action contract written. If MTS can source a parent variational principle on `C_D(beta_0)` with fixed `beta_ref=(S,sigma_AB,tau,C_top,B_ct)`, then the 2455/2456 leak law gives `D_a B_ref=0` without a plateau axiom. Current corpus has not yet sourced those signatures, so no `Delta_ref`, PPN, Newton, or local-GR claim is made.",
            "**Private reading:** this is the proper leap forward. The branch is no longer a vague wish that the reference term is quiet; it is a concrete contract the parent theory must satisfy. Either the corpus already contains this signature and we promote carefully, or it does not and we demote the zero route to closure/nonclaim while using finite bounds.",
            "## Source Register\n" + table(["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"], source_rows),
            "## Parent Action Contract\n" + table(["contract_id", "clause", "formula", "derivation_role", "current_signature", "status"], parent_rows),
            "## Variational Domain Theorem\n" + table(["theorem_id", "statement", "formula", "proof_step", "result", "promotion_status"], theorem_rows),
            "## Contract Signature Audit\n" + table(["signature_id", "required_signature", "current_fill", "why_required", "status"], signature_rows),
            "## Delta-ref Bound Value Inputs\n" + table(["input_id", "quantity", "value_rule", "current_value", "required_source", "valid_for_claim", "status"], bound_rows),
            "## Claim Gates\n" + table(["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"], gate_rows),
            "## Decision Ledger\n" + table(["decision_id", "decision", "reason", "effect"], decisions),
            "## Next Target\n" + table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], next_rows),
            "## Branch Copies\n" + table(["copy_id", "source_path", "target_path", "source_exists", "target_exists"], branch_rows),
            "## Validation\n" + table(["check_id", "status", "notes", "detail"], validations),
        ]
    )
    DOC.write_text(doc + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    parent_rows = parent_contract_rows()
    theorem_rows = domain_theorem_rows()
    signature_rows = signature_audit_rows()
    bound_rows = bound_input_rows()
    gate_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["parent_contract"], parent_rows)
    write_csv(OUTPUTS["domain_theorem"], theorem_rows)
    write_csv(OUTPUTS["signature_audit"], signature_rows)
    write_csv(OUTPUTS["bound_inputs"], bound_rows)
    write_csv(OUTPUTS["claim_gates"], gate_rows)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validations = validation_rows(source_rows, parent_rows, theorem_rows, signature_rows, bound_rows, gate_rows, next_rows, branch_rows)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(source_rows, parent_rows, theorem_rows, signature_rows, bound_rows, gate_rows, decisions, next_rows, branch_rows, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()

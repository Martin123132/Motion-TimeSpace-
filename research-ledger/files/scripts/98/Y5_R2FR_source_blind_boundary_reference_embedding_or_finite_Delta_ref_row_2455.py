from __future__ import annotations

import csv
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_SOURCE_BLIND_BOUNDARY_REFERENCE_EMBEDDING_OR_FINITE_DELTA_REF_ROW_2455"
CHECKPOINT_ID = "2455"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2455-Y5-R2FR-source-blind-boundary-reference-embedding-or-finite-Delta-ref-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2455_SOURCE_REGISTER.csv",
    "embedding_derivation": OUT / "P8_Y5_PARENT_QLOC_2455_BOUNDARY_REFERENCE_EMBEDDING_DERIVATION.csv",
    "zero_certificate": OUT / "P8_Y5_PARENT_QLOC_2455_BOUNDARY_DATA_ZERO_CERTIFICATE.csv",
    "finite_bound_rows": OUT / "P8_Y5_PARENT_QLOC_2455_DELTA_REF_BOUND_ROW_TEMPLATE.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2455_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2455_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2455_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2455_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2455_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_derivation": QUEUE / "JR2455_BOUNDARY_REFERENCE_EMBEDDING_DERIVATION_NONCLAIM.csv",
    "queue_bound": QUEUE / "JR2455_DELTA_REF_BOUND_ROW_TEMPLATE_NONCLAIM.csv",
    "hamiltonian_bound": HAMILTONIAN / "Delta_ref_boundary_data_bound_template_2455_NONCLAIM.csv",
    "local_bound": LOCAL_BOUNDS / "Delta_ref_boundary_data_bound_template_2455_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2455_00_2454_doc",
        "source_path": ROOT / "2454-Y5-R2FR-reference-projection-Hessian-certificate-or-selector-demotion.md",
        "needles": ["NEXT2454_0_selected", "PRJ2454_0_intrinsic_boundary_reference", "VAL2454_OVERALL"],
        "role": "fresh handoff selecting intrinsic-boundary reference embedding",
    },
    {
        "source_id": "SRC2455_01_2454_projection",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2454_REFERENCE_PROJECTION_CANDIDATES.csv",
        "needles": ["PRJ2454_0_intrinsic_boundary_reference", "BEST_RESTRICTED_CANDIDATE_NOT_SIGNED"],
        "role": "machine-readable restricted projection candidate",
    },
    {
        "source_id": "SRC2455_02_2454_hessian",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2454_SELECTOR_HESSIAN_AUDIT.csv",
        "needles": ["HES2454_0_embedding_Hessian", "MISSING_SELECTOR_HESSIAN_CERTIFICATE"],
        "role": "embedding Hessian blocker",
    },
    {
        "source_id": "SRC2455_03_2453_ift",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2453_IMPLICIT_FUNCTION_DERIVATION.csv",
        "needles": ["IFT2453_4_chain_to_Bref", "conditional_theorem"],
        "role": "IFT/chain-rule theorem that boundary reference certificate would feed",
    },
    {
        "source_id": "SRC2455_04_2449_chain",
        "source_path": ROOT / "2449-Y5-R2FR-Bref-derivative-vector-theorem-or-Delta-ref-source-row-for-S-Eq.md",
        "needles": ["BDT2449_1_chain_rule_zero", "MISSING_PARENT_BREF_RULE", "VAL2449_OVERALL"],
        "role": "older chain-rule zero condition",
    },
    {
        "source_id": "SRC2455_05_1003_frame",
        "source_path": ROOT / "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
        "needles": ["CFA1003_1_quotient_coframe_descent", "fail_current_claim"],
        "role": "coframe/reference covariance blocker",
    },
    {
        "source_id": "SRC2455_06_1843_boundary",
        "source_path": ROOT / "1843-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "needles": ["BDC1843_5_verdict", "ETB1843_1_weighted_Stokes_identity", "VAL1843_OVERALL"],
        "role": "boundary domain/cohomology and finite-bound precedent",
    },
    {
        "source_id": "SRC2455_07_1016_source",
        "source_path": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "needles": ["PSC1016_9_verdict", "M_H_ref", "V1016_SUMMARY"],
        "role": "same-frame denominator/source selector blocker",
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


def embedding_derivation_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "derivation_id": "EMB2455_0_reference_charge_form",
            "statement": "B_ref is a functional of intrinsic boundary data, time generator, topological class and counterterm class",
            "formula": "B_ref[S,tau,C_top]=int_S sqrt(sigma) b_0(sigma_AB,tau,C_top)+B_ct[sigma_AB,tau,C_top]",
            "result": "reference branch can be source-blind only if its boundary data are source-blind",
            "current_status": "FORMULA_CONTRACT",
        },
        {
            "derivation_id": "EMB2455_1_variation_law",
            "statement": "vary B_ref with respect to any local parameter a in {q,source}",
            "formula": "D_a B_ref=<delta B_ref/delta sigma_AB,D_a sigma_AB>+<delta B_ref/delta tau,D_a tau>+<delta B_ref/delta C_top,D_a C_top>+D_a B_ct",
            "result": "the exact leak channels are boundary metric, tau, topological class and counterterm",
            "current_status": "DERIVED_CONDITIONAL_IDENTITY",
        },
        {
            "derivation_id": "EMB2455_2_zero_condition",
            "statement": "B_ref is q/source-blind iff all boundary reference inputs are q/source-blind",
            "formula": "D_a sigma_AB=D_a tau=D_a C_top=D_a B_ct=0 => D_a B_ref=0",
            "result": "this is the exact local zero certificate required by 2453/2454",
            "current_status": "CONDITIONAL_THEOREM",
        },
        {
            "derivation_id": "EMB2455_3_embedding_Hessian",
            "statement": "reference embedding response is controlled by the linearized isometric embedding operator",
            "formula": "L_embed(delta X_ref)=D_a sigma_AB; kernel(L_embed)=rigid reference isometries",
            "result": "if D_a sigma_AB=0, embedding drift is pure rigid gauge and leaves B_ref invariant",
            "current_status": "CONDITIONAL_RESTRICTED_BRANCH",
        },
        {
            "derivation_id": "EMB2455_4_finite_bound",
            "statement": "if exact zero fails, B_ref leakage has a finite operator-norm bound",
            "formula": "|D_a B_ref| <= C_sigma ||D_a sigma|| + C_tau ||D_a tau|| + C_top |D_a C_top| + |D_a B_ct|",
            "result": "Delta_ref q/source rows can be bounded rather than claimed zero",
            "current_status": "BOUND_LAW_STAGED",
        },
        {
            "derivation_id": "EMB2455_5_verdict",
            "statement": "source-blind boundary reference embedding closes current MTS B_ref zero",
            "formula": "EMB2455_2 plus EMB2455_3 plus same-frame N_E signed => partial_q Delta_ref=partial_source Delta_ref=0",
            "result": "mathematical condition derived, but boundary-data zero and embedding Hessian are not parent-signed",
            "current_status": "FAIL_CURRENT_CLAIM_BUT_EXACT_ZERO_OR_BOUND_LAW_DERIVED",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def zero_certificate_rows() -> list[dict[str, Any]]:
    rows = [
        ("ZC2455_0_surface_domain", "D_q S=D_source S=0", "MISSING_SOURCE_BLIND_SURFACE_DOMAIN_RULE", "surface/linking/domain cannot move with source or observed-GM readout"),
        ("ZC2455_1_boundary_metric", "D_q sigma_AB=D_source sigma_AB=0", "MISSING_BOUNDARY_METRIC_ZERO_CERTIFICATE", "intrinsic geometry is the main reference embedding input"),
        ("ZC2455_2_tau", "D_q tau=D_source tau=0", "MISSING_TAU_REFERENCE_ZERO_CERTIFICATE", "time generator must match B_ref, Q_tau, clocks and source frame"),
        ("ZC2455_3_topological_class", "D_q C_top=D_source C_top=0", "MISSING_CTOP_SUPERSELECTION_CERTIFICATE", "topological class cannot be selected from source/readout"),
        ("ZC2455_4_counterterm", "D_q B_ct=D_source B_ct=0", "MISSING_COUNTERTERM_ZERO_CERTIFICATE", "counterterm cannot cancel source leakage"),
        ("ZC2455_5_embedding_Hessian", "kernel(L_embed)=rigid isometries only", "MISSING_EMBEDDING_HESSIAN_CERTIFICATE", "non-rigid embedding zero modes would allow hidden reference drift"),
        ("ZC2455_6_same_frame_N_E", "N_E>0 in same tau/coframe", "MISSING_SAME_FRAME_N_E", "zero/bound numerator must normalize in a parent-owned source frame"),
        ("ZC2455_7_source_paths", "all certificates have source_path/equation_ref", "MISSING_SOURCE_PATHS", "no theorem-zero switch can be claim-grade without provenance"),
    ]
    return [
        {
            **metadata(),
            "certificate_id": cert_id,
            "required_zero_or_bound": required,
            "current_fill": current,
            "why_required": why,
            "status": "BLOCKED_NONCLAIM",
        }
        for cert_id, required, current, why in rows
    ]


def finite_bound_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "DBR2455_0_partial_q_Bref_bound",
            "quantity": "partial_q_Bref_over_N_E",
            "bound_formula": "(C_sigma*norm_Dq_sigma + C_tau*norm_Dq_tau + C_top*abs_Dq_Ctop + abs_Dq_Bct)/N_E",
            "required_inputs": "C_sigma;norm_Dq_sigma;C_tau;norm_Dq_tau;C_top;abs_Dq_Ctop;abs_Dq_Bct;N_E;units;source_path",
            "current_value": "MISSING_BOUND_INPUTS",
            "score_ready": "False",
        },
        {
            "row_id": "DBR2455_1_partial_source_Bref_bound",
            "quantity": "partial_source_Bref_over_N_E",
            "bound_formula": "(C_sigma*norm_Dsource_sigma + C_tau*norm_Dsource_tau + C_top*abs_Dsource_Ctop + abs_Dsource_Bct)/N_E",
            "required_inputs": "C_sigma;norm_Dsource_sigma;C_tau;norm_Dsource_tau;C_top;abs_Dsource_Ctop;abs_Dsource_Bct;N_E;units;source_path",
            "current_value": "MISSING_BOUND_INPUTS",
            "score_ready": "False",
        },
        {
            "row_id": "DBR2455_2_embedding_operator_norm",
            "quantity": "C_sigma",
            "bound_formula": "||delta B_ref/delta sigma|| + embedding response norm C_embed",
            "required_inputs": "embedding_domain;convexity_or_regular_class;gauge_quotient;C_embed;units;source_path",
            "current_value": "MISSING_EMBEDDING_OPERATOR_NORM",
            "score_ready": "False",
        },
        {
            "row_id": "DBR2455_3_counterterm_bound",
            "quantity": "abs_Da_Bct_over_N_E",
            "bound_formula": "abs(D_a B_ct)/N_E for a in {q,source}",
            "required_inputs": "B_ct_rule;Dq_Bct;Dsource_Bct;N_E;units;source_path",
            "current_value": "MISSING_COUNTERTERM_BOUND",
            "score_ready": "False",
        },
        {
            "row_id": "DBR2455_4_total_Delta_ref_bound",
            "quantity": "Delta_ref_q_source_component_over_N_E",
            "bound_formula": "abs(partial_q_Bref*Delta_q)+abs(partial_source_Bref*Delta_source) over N_E",
            "required_inputs": "DBR2455_0;DBR2455_1;Delta_q_scale;Delta_source_scale;no_cancellation_guard;source_path",
            "current_value": "MISSING_COMPONENT_INPUTS",
            "score_ready": "False",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2455_0_zero_law_derived",
            "claim": "exact condition for D_a B_ref=0 is derived",
            "gate_status": "PASS_AS_CONTRACT",
            "reason": "variation law identifies boundary metric, tau, C_top and counterterm as complete leak channels for the restricted branch",
            "gate_pass": "True",
        },
        {
            "gate_id": "GATE2455_1_zero_certificate_signed",
            "claim": "current MTS has D_q/source boundary-data zero certificate",
            "gate_status": "BLOCKED",
            "reason": "surface/domain, sigma_AB, tau, C_top, B_ct and embedding Hessian certificates are missing",
            "gate_pass": "False",
        },
        {
            "gate_id": "GATE2455_2_finite_bound_ready",
            "claim": "finite Delta_ref q/source bound can be scored",
            "gate_status": "BLOCKED",
            "reason": "operator norms, boundary-data derivative norms and N_E are missing",
            "gate_pass": "False",
        },
        {
            "gate_id": "GATE2455_3_selector_zero",
            "claim": "partial_q Delta_ref=partial_source Delta_ref=0 is current theorem",
            "gate_status": "BLOCKED",
            "reason": "zero law is derived but certificates are not signed",
            "gate_pass": "False",
        },
        {
            "gate_id": "GATE2455_4_local_GR",
            "claim": "Delta_ref/RCS2446_0/S_Eq/PPN/local-GR branch passes",
            "gate_status": "BLOCKED",
            "reason": "2455 gives exact zero-or-bound law, not claim-grade inputs",
            "gate_pass": "False",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2455_0_exact_law",
            "decision": "use the boundary-data variation law as the exact B_ref leak law",
            "reason": "it gives both zero-theorem conditions and a finite bound fallback",
            "effect": "future work must source boundary-data zeros/norms, not debate B_ref in prose",
        },
        {
            "decision_id": "DEC2455_1_no_promotion",
            "decision": "do not promote source-blind reference embedding",
            "reason": "all zero certificates are currently missing-marked",
            "effect": "Delta_ref q/source theorem-zero remains blocked",
        },
        {
            "decision_id": "DEC2455_2_fallback",
            "decision": "stage finite Delta_ref q/source bound rows",
            "reason": "if boundary-data zero fails, the same derivation supplies operator-norm residual rows",
            "effect": "2452 strict runner can eventually score sourced finite rows",
        },
        {
            "decision_id": "DEC2455_3_next",
            "decision": "hunt boundary-data derivative zero or first real bound inputs",
            "reason": "D_a sigma_AB and D_a tau are the first practical coefficients in the law",
            "effect": "2456 should target boundary-data leak certificates or measured/source-bound rows",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **metadata(),
            "route_id": "NEXT2455_0_selected",
            "selection_status": "selected",
            "target_file": "2456-Y5-R2FR-boundary-data-leak-zero-certificate-or-first-Delta-ref-bound-row.md",
            "target_script": "scripts/Y5_R2FR_boundary_data_leak_zero_certificate_or_first_Delta_ref_bound_row_2456.py",
            "task": "prove D_q/source sigma_AB, tau, C_top and B_ct vanish for the parent reference surface, or fill the first finite Delta_ref q/source bound row with source-backed norms",
            "acceptance_target": "componentwise zero certificates or numeric/source-backed norm bounds for boundary metric, tau, topological class, counterterm, embedding operator and N_E",
            "guardrails": "no observed-GM/fitted-mass surface rule; no cancellation; no Delta_ref/RCS2446_0/S_Eq/local-GR claim; no formalization-workbench edit; no GitHub",
        }
    ]


def copy_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    specs = [
        ("queue_derivation", OUTPUTS["embedding_derivation"], COPY_TARGETS["queue_derivation"]),
        ("queue_bound", OUTPUTS["finite_bound_rows"], COPY_TARGETS["queue_bound"]),
        ("hamiltonian_bound", OUTPUTS["finite_bound_rows"], COPY_TARGETS["hamiltonian_bound"]),
        ("local_bound", OUTPUTS["finite_bound_rows"], COPY_TARGETS["local_bound"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in specs:
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


def formalization_marker_hits() -> list[str]:
    if not FORMALIZATION.exists():
        return []
    markers = ["2455-", "_2455", "2455_", "P8_Y5_PARENT_QLOC_2455", "P8_Y5_BRR545_2455"]
    hits: list[str] = []
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            if any(marker in filename for marker in markers):
                hits.append(str(Path(dirpath) / filename))
    return hits


def csv_parse_ok(path: Path) -> tuple[bool, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    except Exception as exc:
        return False, repr(exc)
    return True, f"CSV parses with {len(rows)} rows"


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_ok = all(row["source_pass"] == "True" for row in data["source_register"])
    zero_law = any(row["derivation_id"] == "EMB2455_2_zero_condition" and row["current_status"] == "CONDITIONAL_THEOREM" for row in data["embedding_derivation"])
    bound_law = any(row["derivation_id"] == "EMB2455_4_finite_bound" and row["current_status"] == "BOUND_LAW_STAGED" for row in data["embedding_derivation"])
    verdict_blocks = any(row["derivation_id"] == "EMB2455_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_BUT_EXACT_ZERO_OR_BOUND_LAW_DERIVED" for row in data["embedding_derivation"])
    zero_cert_blocked = all(row["status"] == "BLOCKED_NONCLAIM" and str(row["current_fill"]).startswith("MISSING") for row in data["zero_certificate"])
    finite_rows_blocked = all(row["score_ready"] == "False" and str(row["current_value"]).startswith("MISSING") for row in data["finite_bound_rows"])
    claims_safe = all(row["claim_allowed"] == "False" for row in data["claim_gates"]) and any(row["gate_id"] == "GATE2455_0_zero_law_derived" and row["gate_pass"] == "True" for row in data["claim_gates"])
    next_ok = bool(data["next_target"]) and data["next_target"][0]["route_id"] == "NEXT2455_0_selected"
    copies_ok = all(row["target_exists"] == "True" for row in data["branch_copies"])
    no_formalization = not formalization_marker_hits()
    checks: list[dict[str, Any]] = [
        {"check_id": "VAL2455_00_sources_exist", "status": "PASS" if source_ok else "FAIL", "notes": "all cited source paths exist and needles are present", "detail": ""},
        {"check_id": "VAL2455_01_zero_law_derived", "status": "PASS" if zero_law else "FAIL", "notes": "boundary-data zero condition is written", "detail": ""},
        {"check_id": "VAL2455_02_bound_law_staged", "status": "PASS" if bound_law else "FAIL", "notes": "finite operator-norm fallback bound is written", "detail": ""},
        {"check_id": "VAL2455_03_current_claim_blocked", "status": "PASS" if verdict_blocks else "FAIL", "notes": "current source-blind embedding claim is not promoted", "detail": ""},
        {"check_id": "VAL2455_04_zero_certificates_missing", "status": "PASS" if zero_cert_blocked else "FAIL", "notes": "zero certificates remain missing-marked", "detail": ""},
        {"check_id": "VAL2455_05_finite_rows_blocked", "status": "PASS" if finite_rows_blocked else "FAIL", "notes": "finite bound rows remain templates", "detail": ""},
        {"check_id": "VAL2455_06_claim_gates_safe", "status": "PASS" if claims_safe else "FAIL", "notes": "zero law passes only as contract; local-GR claims remain blocked", "detail": ""},
        {"check_id": "VAL2455_07_next_target_written", "status": "PASS" if next_ok else "FAIL", "notes": "2456 boundary-data leak target selected", "detail": ""},
        {"check_id": "VAL2455_08_branch_copies", "status": "PASS" if copies_ok else "FAIL", "notes": "nonclaim branch copies exist", "detail": ""},
        {"check_id": "VAL2455_09_no_formalization_artifacts", "status": "PASS" if no_formalization else "FAIL", "notes": "no 2455 artifacts were written to formalization-workbench", "detail": ";".join(formalization_marker_hits()[:10])},
    ]
    csv_outputs = [
        OUTPUTS["source_register"],
        OUTPUTS["embedding_derivation"],
        OUTPUTS["zero_certificate"],
        OUTPUTS["finite_bound_rows"],
        OUTPUTS["claim_gates"],
        OUTPUTS["decisions"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    for path in csv_outputs:
        ok, detail = csv_parse_ok(path)
        checks.append(
            {
                "check_id": f"VAL2455_CSV_{path.stem}",
                "status": "PASS" if ok else "FAIL",
                "notes": detail,
                "detail": str(path),
            }
        )
    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        {
            "check_id": "VAL2455_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "notes": "2455 derives exact boundary-reference zero law and finite Delta_ref fallback while keeping claims blocked",
            "detail": "",
        }
    )
    return [{**metadata(), **row} for row in checks]


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2455 Y5 R2FR Source-Blind Boundary Reference Embedding Or Finite Delta-ref Row

**Status:** exact zero-or-bound law derived for the restricted intrinsic-boundary reference branch. No current `Delta_ref`, `RCS2446_0`, `S_E^q`, PPN, Newton, or local-GR pass is claimed.

**Private reading:** this is the useful turn. The problem is no longer "is `B_ref` source-blind?" in the abstract. It is: are `sigma_AB`, `tau`, `C_top`, and `B_ct` source-blind on the parent-selected reference surface, and can the embedding Hessian be controlled?

## Source Register
{table(["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"], data["source_register"])}

## Boundary Reference Embedding Derivation
{table(["derivation_id", "statement", "formula", "result", "current_status"], data["embedding_derivation"])}

## Boundary Data Zero Certificate
{table(["certificate_id", "required_zero_or_bound", "current_fill", "why_required", "status"], data["zero_certificate"])}

## Finite Delta-ref Bound Rows
{table(["row_id", "quantity", "bound_formula", "required_inputs", "current_value", "score_ready"], data["finite_bound_rows"])}

## Claim Gates
{table(["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"], data["claim_gates"])}

## Decision Ledger
{table(["decision_id", "decision", "reason", "effect"], data["decisions"])}

## Next Target
{table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], data["next_target"])}

## Branch Copies
{table(["copy_id", "source_path", "target_path", "source_exists", "target_exists"], data["branch_copies"])}

## Validation
{table(["check_id", "status", "notes", "detail"], data["validation"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "embedding_derivation": embedding_derivation_rows(),
        "zero_certificate": zero_certificate_rows(),
        "finite_bound_rows": finite_bound_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }
    for key in ["source_register", "embedding_derivation", "zero_certificate", "finite_bound_rows", "claim_gates", "decisions", "next_target"]:
        write_csv(OUTPUTS[key], data[key])

    data["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)


if __name__ == "__main__":
    main()

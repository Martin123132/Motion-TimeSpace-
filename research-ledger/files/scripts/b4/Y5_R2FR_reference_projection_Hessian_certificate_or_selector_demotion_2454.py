from __future__ import annotations

import csv
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_REFERENCE_PROJECTION_HESSIAN_CERTIFICATE_OR_SELECTOR_DEMOTION_2454"
CHECKPOINT_ID = "2454"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2454-Y5-R2FR-reference-projection-Hessian-certificate-or-selector-demotion.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2454_SOURCE_REGISTER.csv",
    "projection_candidates": OUT / "P8_Y5_PARENT_QLOC_2454_REFERENCE_PROJECTION_CANDIDATES.csv",
    "hessian_audit": OUT / "P8_Y5_PARENT_QLOC_2454_SELECTOR_HESSIAN_AUDIT.csv",
    "promotion_test": OUT / "P8_Y5_PARENT_QLOC_2454_SELECTOR_PROMOTION_TEST.csv",
    "demotion_ledger": OUT / "P8_Y5_PARENT_QLOC_2454_DEMOTION_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2454_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2454_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2454_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2454_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2454_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_projection": QUEUE / "JR2454_REFERENCE_PROJECTION_CANDIDATES_NONCLAIM.csv",
    "queue_hessian": QUEUE / "JR2454_SELECTOR_HESSIAN_AUDIT_NONCLAIM.csv",
    "local_demotion": LOCAL_BOUNDS / "Bref_selector_demotion_ledger_2454_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2454_00_2453_doc",
        "source_path": ROOT / "2453-Y5-R2FR-parent-Bref-selector-variational-equation-or-finite-coefficient-row.md",
        "needles": ["NEXT2453_0_selected", "PBT2453_3_non_degenerate_selector", "VAL2453_OVERALL"],
        "role": "fresh handoff: Pi_ref and Hessian are the decisive missing clauses",
    },
    {
        "source_id": "SRC2454_01_2453_clause_audit",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2453_SELECTOR_CLAUSE_AUDIT.csv",
        "needles": ["CLA2453_1_Piref", "CLA2453_3_Hessian", "MISSING_HESSIAN_CERTIFICATE"],
        "role": "machine-readable missing projection/Hessian clauses",
    },
    {
        "source_id": "SRC2454_02_1878_qshape",
        "source_path": ROOT / "1878-Y5-R2FR-qshape-readout-functor-kernel-or-parent-category-principle.md",
        "needles": ["DOBS_E_KERNEL_NOT_DERIVED_CURRENT_CORPUS", "q_shape", "VAL1878_OVERALL"],
        "role": "q-shape/readout projection precedent and failure",
    },
    {
        "source_id": "SRC2454_03_1845_vertical",
        "source_path": ROOT / "1845-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
        "needles": ["BDM1845_0_vertical_quotient", "TESTED_NOT_CLOSED", "Current verdict"],
        "role": "vertical quotient route tested but not closed",
    },
    {
        "source_id": "SRC2454_04_1854_hessian",
        "source_path": ROOT / "1854-Y5-R2FR-parent-Hessian-input-extraction-for-ZX-MX2.md",
        "needles": ["HCA1854_6_verdict", "FAIL_CURRENT_CLAIM_PARENT_HESSIAN_INPUTS_NOT_EXTRACTED", "VAL1854_OVERALL"],
        "role": "parent Hessian precedent: formulas exist but claim-grade Hessian data absent",
    },
    {
        "source_id": "SRC2454_05_1843_projector",
        "source_path": ROOT / "1843-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "needles": ["RVT1843_1_projector_orthogonality", "FAIL_CURRENT_CLAIM", "VAL1843_OVERALL"],
        "role": "boundary projector orthogonality precedent",
    },
    {
        "source_id": "SRC2454_06_1016_worldtube",
        "source_path": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "needles": ["PSC1016_9_verdict", "W_source := closure(supp J_H[tau])", "V1016_SUMMARY"],
        "role": "same-frame source/support selector precedent",
    },
    {
        "source_id": "SRC2454_07_1003_frame",
        "source_path": ROOT / "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
        "needles": ["CFA1003_1_quotient_coframe_descent", "CFA1003_6_theorem_verdict", "fail_current_claim"],
        "role": "coframe/reference covariance predecessor",
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


def projection_candidate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "candidate_id": "PRJ2454_0_intrinsic_boundary_reference",
            "candidate": "Pi_ref^IB: Phi -> (gamma_AB on S, tau_boundary, C_top, counterterm_class)",
            "why_promising": "intrinsic boundary geometry can define a reference embedding without explicit matter labels",
            "zero_mechanism": "if S, gamma_AB, tau and C_top are selected before q/source/readout, then D_q Pi_ref=D_source Pi_ref=0",
            "blocker": "surface/domain and observed coframe may still carry source/readout dependence",
            "status": "BEST_RESTRICTED_CANDIDATE_NOT_SIGNED",
            "demote_now": "False",
        },
        {
            "candidate_id": "PRJ2454_1_qshape_forgetful",
            "candidate": "Pi_ref^qshape: forget q/source labels through q_shape",
            "why_promising": "least post-hoc if a parent category principle makes readout descend",
            "zero_mechanism": "q/source labels disappear before reference selection",
            "blocker": "1878 shows q_shape kernel is weaker than observed coframe/readout kernel",
            "status": "FAIL_CURRENT_CORPUS",
            "demote_now": "True",
        },
        {
            "candidate_id": "PRJ2454_2_vertical_quotient",
            "candidate": "Pi_ref^vert: quotient by vertical fibre directions before variation",
            "why_promising": "would remove local extra branch before field equations",
            "zero_mechanism": "vertical directions become pure gauge in parent presymplectic quotient",
            "blocker": "1845 tests q/v_X/action descent and finds matter, boundary and degree-count clauses unsigned",
            "status": "TESTED_NOT_CLOSED",
            "demote_now": "True",
        },
        {
            "candidate_id": "PRJ2454_3_topological_only",
            "candidate": "Pi_ref^top: keep only C_top/topological class",
            "why_promising": "strongly q/source blind",
            "zero_mechanism": "topological class is insensitive to local source amplitudes if parent-owned",
            "blocker": "too coarse to fix B_ref, tau, counterterm or N_E uniquely",
            "status": "UNDERDETERMINED_SELECTOR",
            "demote_now": "True",
        },
        {
            "candidate_id": "PRJ2454_4_source_support",
            "candidate": "Pi_ref^support: reference selected by W_source=closure(supp J_H[tau])",
            "why_promising": "parent source worldtube selector can be covariant before readout",
            "zero_mechanism": "source support is defined by parent Hilbert current, not fitted GM",
            "blocker": "not source-blind; useful for N_E/source measure, not for B_ref q/source zero",
            "status": "WRONG_OBJECT_FOR_BREF_ZERO_BUT_USEFUL_FOR_DENOMINATOR",
            "demote_now": "False",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def hessian_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "HES2454_0_embedding_Hessian",
            "object": "H_Sigma for intrinsic-boundary reference embedding",
            "minimum_form": "D_Sigma E_Sigma with rigid reference isometries quotiented out",
            "current_evidence": "candidate mathematical branch only",
            "required_certificate": "convex/regular embedding domain, gauge quotient, no zero modes except rigid isometries, source path",
            "status": "MISSING_SELECTOR_HESSIAN_CERTIFICATE",
        },
        {
            "audit_id": "HES2454_1_surface_domain_lock",
            "object": "surface/domain selected before q/source/readout",
            "minimum_form": "D_q S=0 and D_source S=0 for allowed surfaces S",
            "current_evidence": "2448/2449/2451 list this as blocker",
            "required_certificate": "area/radius/linking surface rule independent of source and observed GM",
            "status": "MISSING_SOURCE_BLIND_SURFACE_RULE",
        },
        {
            "audit_id": "HES2454_2_cross_Hessian",
            "object": "mixed selector Hessian with coframe, matter, boundary and source variables",
            "minimum_form": "block diagonal or residual matrix retained with absolute-value envelope",
            "current_evidence": "1854 finds cross-Hessian block missing for local scalar routes",
            "required_certificate": "D_{Sigma,q/source/coframe/matter}E_Sigma=0 or finite residual rows",
            "status": "MISSING_CROSS_HESSIAN_BLOCK",
        },
        {
            "audit_id": "HES2454_3_counterterm_Hessian",
            "object": "counterterm branch stability",
            "minimum_form": "B_ct[Sigma_ref] fixed by same selector and no explicit source/readout slot",
            "current_evidence": "2451 and 2453 require counterterm convention",
            "required_certificate": "counterterm convention source path/equation ref",
            "status": "MISSING_COUNTERTERM_HESSIAN_SIDE_CLAUSE",
        },
        {
            "audit_id": "HES2454_4_same_frame_denominator",
            "object": "N_E/Q_tau denominator",
            "minimum_form": "N_E=Q_tau[Sigma_ref]>0 in same tau/coframe as B_ref and source current",
            "current_evidence": "1016 source selector is conditional; 2453 requires same-frame N_E",
            "required_certificate": "positive Hamiltonian/source denominator before readout",
            "status": "MISSING_SAME_FRAME_N_E",
        },
        {
            "audit_id": "HES2454_5_verdict",
            "object": "Pi_ref + H_Sigma certificate for current MTS",
            "minimum_form": "PRJ2454_0 plus HES2454_0 through HES2454_4 signed",
            "current_evidence": "best candidate found, but decisive certificates absent",
            "required_certificate": "restricted intrinsic-boundary branch must be explicitly adopted and sourced",
            "status": "FAIL_CURRENT_CLAIM_BUT_DO_NOT_DEMOTE_ROUTE_YET",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def promotion_test_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "test_id": "PROM2454_0_projection_exists",
            "test": "there is at least one non-vacuous Pi_ref candidate",
            "result": "PASS_CONDITIONAL",
            "evidence": "PRJ2454_0 intrinsic-boundary reference candidate",
            "blocks_claim": "not by itself",
        },
        {
            "test_id": "PROM2454_1_projection_q_source_blind",
            "test": "D_q Pi_ref=D_source Pi_ref=0",
            "result": "FAIL_CURRENT_CLAIM",
            "evidence": "surface/domain and coframe/readout kernel are unsigned",
            "blocks_claim": "yes",
        },
        {
            "test_id": "PROM2454_2_Hessian_invertible",
            "test": "H_Sigma invertible modulo gauge",
            "result": "FAIL_CURRENT_CLAIM",
            "evidence": "no embedding/domain/gauge quotient Hessian certificate",
            "blocks_claim": "yes",
        },
        {
            "test_id": "PROM2454_3_no_marker_no_GM",
            "test": "no material marker and no observed-GM/fitted-source shortcut",
            "result": "FAIL_CURRENT_CLAIM",
            "evidence": "only guardrail exists; no parent source path/equation ref",
            "blocks_claim": "yes",
        },
        {
            "test_id": "PROM2454_4_promote_selector_zero",
            "test": "promote D_q B_ref=D_source B_ref=0",
            "result": "REFUSED",
            "evidence": "PROM2454_1 through PROM2454_3 fail",
            "blocks_claim": "yes",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def demotion_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "demotion_id": "DEM2454_0_qshape_projection",
            "route": "qshape/forgetful projection route",
            "decision": "DEMOTE_FOR_CURRENT_BREF_SELECTOR",
            "reason": "readout/coframe kernel is weaker than needed for B_ref q/source zero",
            "replacement": "retain finite DObs/coframe leak rows if used",
        },
        {
            "demotion_id": "DEM2454_1_vertical_quotient",
            "route": "vertical quotient removes branch before variation",
            "decision": "DEMOTE_FOR_CURRENT_BREF_SELECTOR",
            "reason": "matter/boundary/action descent is not signed together",
            "replacement": "only revive after a parent presymplectic quotient certificate exists",
        },
        {
            "demotion_id": "DEM2454_2_topological_only",
            "route": "topological-only reference selector",
            "decision": "DEMOTE_AS_UNDERDETERMINED",
            "reason": "cannot uniquely fix B_ref/tau/counterterm/N_E",
            "replacement": "use as one clause inside intrinsic-boundary reference, not the whole selector",
        },
        {
            "demotion_id": "DEM2454_3_intrinsic_boundary",
            "route": "intrinsic-boundary reference selector",
            "decision": "RETAIN_AS_RESTRICTED_PROOF_ROUTE_NOT_CLAIM",
            "reason": "least post-hoc candidate that can plausibly fix B_ref before source/readout",
            "replacement": "2455 must prove source-blind surface/reference embedding certificate or fall back to finite rows",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2454_0_projection_candidate",
            "claim": "a restricted Pi_ref candidate exists",
            "gate_status": "PASS_AS_NONCLAIM_ROUTE",
            "reason": "intrinsic-boundary reference candidate is mathematically coherent but not parent-signed",
            "gate_pass": "True",
        },
        {
            "gate_id": "GATE2454_1_projection_certificate",
            "claim": "Pi_ref is parent-owned and q/source/readout blind",
            "gate_status": "BLOCKED",
            "reason": "source-blind surface/domain and coframe/readout kernel certificates are missing",
            "gate_pass": "False",
        },
        {
            "gate_id": "GATE2454_2_Hessian_certificate",
            "claim": "H_Sigma is invertible modulo gauge",
            "gate_status": "BLOCKED",
            "reason": "embedding Hessian/domain/gauge quotient certificate is missing",
            "gate_pass": "False",
        },
        {
            "gate_id": "GATE2454_3_selector_zero",
            "claim": "D_q B_ref=D_source B_ref=0 is current theorem",
            "gate_status": "BLOCKED",
            "reason": "promotion test refuses selector zero",
            "gate_pass": "False",
        },
        {
            "gate_id": "GATE2454_4_local_GR",
            "claim": "Delta_ref/RCS2446_0/S_Eq/PPN/local-GR branch passes",
            "gate_status": "BLOCKED",
            "reason": "projection route is retained only as nonclaim; finite coefficient rows remain fallback",
            "gate_pass": "False",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2454_0_best_candidate",
            "decision": "retain intrinsic-boundary Pi_ref as the best restricted selector route",
            "reason": "it is source-blind in form if the surface/domain and coframe are parent-owned before readout",
            "effect": "do not demote the B_ref zero route completely yet",
        },
        {
            "decision_id": "DEC2454_1_demote_bad_projectors",
            "decision": "demote qshape-only, vertical-only, and topological-only selectors for current B_ref zero",
            "reason": "each is either too weak, not closed, or underdetermines B_ref",
            "effect": "future proof work focuses on the intrinsic-boundary branch",
        },
        {
            "decision_id": "DEC2454_2_no_promotion",
            "decision": "do not promote Pi_ref/Hessian certificate",
            "reason": "Hessian, surface-domain lock, counterterm branch and same-frame N_E remain unsigned",
            "effect": "2453 IFT proof remains conditional",
        },
        {
            "decision_id": "DEC2454_3_next",
            "decision": "derive source-blind boundary surface/reference embedding next",
            "reason": "this is the smallest missing certificate for PRJ2454_0",
            "effect": "2455 should prove the restricted branch or trigger finite coefficient fallback",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **metadata(),
            "route_id": "NEXT2454_0_selected",
            "selection_status": "selected",
            "target_file": "2455-Y5-R2FR-source-blind-boundary-reference-embedding-or-finite-Delta-ref-row.md",
            "target_script": "scripts/Y5_R2FR_source_blind_boundary_reference_embedding_or_finite_Delta_ref_row_2455.py",
            "task": "prove the intrinsic-boundary reference selector is source/readout blind with an invertible reference embedding Hessian, or demote B_ref zero to finite Delta_ref q/source rows through the 2452 runner",
            "acceptance_target": "surface/domain rule, intrinsic boundary data, tau, C_top, counterterm, embedding Hessian and N_E are parent-owned before q/source/readout; otherwise all claims remain blocked",
            "guardrails": "do not use observed-GM/fitted mass; do not claim Delta_ref/RCS2446_0/S_Eq/local-GR; do not edit formalization-workbench; do not push GitHub",
        }
    ]


def copy_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    specs = [
        ("queue_projection", OUTPUTS["projection_candidates"], COPY_TARGETS["queue_projection"]),
        ("queue_hessian", OUTPUTS["hessian_audit"], COPY_TARGETS["queue_hessian"]),
        ("local_demotion", OUTPUTS["demotion_ledger"], COPY_TARGETS["local_demotion"]),
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
    markers = ["2454-", "_2454", "2454_", "P8_Y5_PARENT_QLOC_2454", "P8_Y5_BRR545_2454"]
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
    best_candidate_ok = any(
        row["candidate_id"] == "PRJ2454_0_intrinsic_boundary_reference"
        and row["status"] == "BEST_RESTRICTED_CANDIDATE_NOT_SIGNED"
        and row["demote_now"] == "False"
        for row in data["projection_candidates"]
    )
    bad_routes_demoted = all(
        row["decision"].startswith("DEMOTE")
        for row in data["demotion_ledger"]
        if row["demotion_id"] in {"DEM2454_0_qshape_projection", "DEM2454_1_vertical_quotient", "DEM2454_2_topological_only"}
    )
    hessian_blocks = any(row["audit_id"] == "HES2454_5_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_BUT_DO_NOT_DEMOTE_ROUTE_YET" for row in data["hessian_audit"])
    promotion_refused = any(row["test_id"] == "PROM2454_4_promote_selector_zero" and row["result"] == "REFUSED" for row in data["promotion_test"])
    claims_safe = all(row["claim_allowed"] == "False" for row in data["claim_gates"])
    next_ok = bool(data["next_target"]) and data["next_target"][0]["route_id"] == "NEXT2454_0_selected"
    copies_ok = all(row["target_exists"] == "True" for row in data["branch_copies"])
    no_formalization = not formalization_marker_hits()
    checks: list[dict[str, Any]] = [
        {"check_id": "VAL2454_00_sources_exist", "status": "PASS" if source_ok else "FAIL", "notes": "all cited source paths exist and needles are present", "detail": ""},
        {"check_id": "VAL2454_01_best_candidate_retained", "status": "PASS" if best_candidate_ok else "FAIL", "notes": "intrinsic-boundary Pi_ref retained as restricted nonclaim route", "detail": ""},
        {"check_id": "VAL2454_02_bad_routes_demoted", "status": "PASS" if bad_routes_demoted else "FAIL", "notes": "qshape, vertical-only and topological-only routes are demoted for current B_ref zero", "detail": ""},
        {"check_id": "VAL2454_03_Hessian_blocks_claim", "status": "PASS" if hessian_blocks else "FAIL", "notes": "Hessian certificate is missing and blocks promotion", "detail": ""},
        {"check_id": "VAL2454_04_promotion_refused", "status": "PASS" if promotion_refused else "FAIL", "notes": "selector-zero promotion is refused", "detail": ""},
        {"check_id": "VAL2454_05_claim_gates_safe", "status": "PASS" if claims_safe else "FAIL", "notes": "all claim gates remain nonclaim", "detail": ""},
        {"check_id": "VAL2454_06_next_target_written", "status": "PASS" if next_ok else "FAIL", "notes": "2455 source-blind boundary embedding target selected", "detail": ""},
        {"check_id": "VAL2454_07_branch_copies", "status": "PASS" if copies_ok else "FAIL", "notes": "nonclaim branch copies exist", "detail": ""},
        {"check_id": "VAL2454_08_no_formalization_artifacts", "status": "PASS" if no_formalization else "FAIL", "notes": "no 2454 artifacts were written to formalization-workbench", "detail": ";".join(formalization_marker_hits()[:10])},
    ]
    csv_outputs = [
        OUTPUTS["source_register"],
        OUTPUTS["projection_candidates"],
        OUTPUTS["hessian_audit"],
        OUTPUTS["promotion_test"],
        OUTPUTS["demotion_ledger"],
        OUTPUTS["claim_gates"],
        OUTPUTS["decisions"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    for path in csv_outputs:
        ok, detail = csv_parse_ok(path)
        checks.append(
            {
                "check_id": f"VAL2454_CSV_{path.stem}",
                "status": "PASS" if ok else "FAIL",
                "notes": detail,
                "detail": str(path),
            }
        )
    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        {
            "check_id": "VAL2454_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "notes": "2454 retains a restricted intrinsic-boundary Pi_ref route, demotes weaker projectors, and refuses current selector-zero promotion",
            "detail": "",
        }
    )
    return [{**metadata(), **row} for row in checks]


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2454 Y5 R2FR Reference Projection Hessian Certificate Or Selector Demotion

**Status:** the `Pi_ref/H_Sigma` route is not dead, but it narrows to a restricted intrinsic-boundary reference branch. q-shape-only, vertical-only, and topological-only projectors are not strong enough for current `B_ref` zero promotion.

**Private reading:** this is useful. The selector-zero route now has one plausible door instead of five foggy doors. That door still needs a parent-signed boundary surface/reference embedding and Hessian certificate.

## Source Register
{table(["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"], data["source_register"])}

## Reference Projection Candidates
{table(["candidate_id", "candidate", "why_promising", "zero_mechanism", "blocker", "status", "demote_now"], data["projection_candidates"])}

## Selector Hessian Audit
{table(["audit_id", "object", "minimum_form", "current_evidence", "required_certificate", "status"], data["hessian_audit"])}

## Selector Promotion Test
{table(["test_id", "test", "result", "evidence", "blocks_claim"], data["promotion_test"])}

## Demotion Ledger
{table(["demotion_id", "route", "decision", "reason", "replacement"], data["demotion_ledger"])}

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
        "projection_candidates": projection_candidate_rows(),
        "hessian_audit": hessian_audit_rows(),
        "promotion_test": promotion_test_rows(),
        "demotion_ledger": demotion_ledger_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }
    for key in ["source_register", "projection_candidates", "hessian_audit", "promotion_test", "demotion_ledger", "claim_gates", "decisions", "next_target"]:
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

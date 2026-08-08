from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2665"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2665-Y5-R2FR-Hamiltonian-source-domain-and-PiM-QbarXH-lock.md"

CHECKPOINT = "2665"
BRANCH_ID = "Y5_R2FR_HAMILTONIAN_SOURCE_DOMAIN_PIM_QBARXH_LOCK_2665"
PREFIX = "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665"
MISSING_TOKENS = (
    "MISSING",
    "UNSIGNED",
    "NOT_PARENT",
    "NOT_DERIVED",
    "BLOCKED",
    "RETAINED",
    "UNFILLED",
    "PLACEHOLDER",
)

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "lock_contract": RESIDUALS / f"{PREFIX}_LOCK_CONTRACT.csv",
    "qbarxh_lock_template": RESIDUALS / f"{PREFIX}_QBARXH_LOCK_TEMPLATE_NONCLAIM.csv",
    "projector_denominator_gate": RESIDUALS / f"{PREFIX}_PROJECTOR_DENOMINATOR_GATE.csv",
    "runner_results": RESIDUALS / f"{PREFIX}_LOCK_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2665_HAMILTONIAN_SOURCE_DOMAIN_PIM_LOCK_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "Hamiltonian_source_domain_PiM_lock_2665_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "QbarXH_PiM_MHref_lock_2665_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2665_QBARXH_PIM_LOCK.csv",
    "quarantine": QUARANTINE / "P8_Y5_2665_LOCK_RUNNER_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2664_doc": {
        "path": ROOT / "2664-Y5-R2FR-source-current-zero-or-QbarXH-first-source-row.md",
        "needles": ["QXH2664_3_projected_Qbar", "DEC2664_2_best_next", "NEXT2664_0_selected"],
        "role": "immediate handoff selecting Hamiltonian source-domain and PiM lock",
    },
    "1016_doc": {
        "path": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "needles": ["PSC1016_3_support_selector", "PSC1016_5_dressed_source_charge", "PSC1016_6_PiM_Hamiltonian_map"],
        "role": "source worldtube, dressed source charge and Hamiltonian PiM candidate",
    },
    "1017_doc": {
        "path": ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
        "needles": ["MHR1017_0_M_H_ref_denominator", "DEC1017_0_reference_lock", "V1017_4_denominator_guard"],
        "role": "M_H_ref denominator and reference/integrability guardrails",
    },
    "1019_doc": {
        "path": ROOT / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "needles": ["PO1019_0_projector_definition", "SP1019_0_M_H_ref", "V1019_6_source_pack_complete"],
        "role": "fixed-frame PiM definition and source-pack denominator schema",
    },
    "1013_doc": {
        "path": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
        "needles": ["PFC1013_0_same_frame_JH", "OBS1013_1_PiM_commutator", "DEC1013_2_next_commutator"],
        "role": "same-frame Hilbert current and PiM commutator obstruction",
    },
    "1014_doc": {
        "path": ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
        "needles": ["PCT1014_6_no_closure_from_algebra", "PCC1014_3_projector_stress_beta_equiv", "V1014_7_claim_gates_blocked"],
        "role": "projector algebra/stress gate showing PiM notation is not closure",
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in list(OUTPUTS.values()) + list(BRANCH_COPIES.values()) + [DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fieldnames]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def has_missing(row: dict[str, Any]) -> bool:
    joined = " ".join(str(value) for value in row.values())
    return any(token in joined for token in MISSING_TOKENS)


def source_register_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": f"SRC2665_{source_id}",
                "role": spec["role"],
                "path": str(path),
                "exists": path.exists(),
                "needles_required": len(spec["needles"]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def lock_contract_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "lock_id": "HLOCK2665_0_target",
            "object": "Qbar_XH lock",
            "contract": "Qbar_XH(lambda)=Pi_M^H[Q_bulk_X^H(lambda)+Q_edge_X^H(lambda)+Q_shadow_X^H(lambda)]/M_H_ref",
            "current_status": "TARGET_EXACT",
            "blocker": "all lock inputs must be parent-owned before alpha(lambda) scoring",
            "next_action": "audit domain, projector and denominator",
        },
        {
            "lock_id": "HLOCK2665_1_source_worldtube",
            "object": "W_source",
            "contract": "W_source := closure(supp J_H[tau]) on a parent-owned Hamiltonian slice, not a fitted mass mask",
            "current_status": "FORMAL_SELECTOR_CONDITIONAL",
            "blocker": "same-frame J_H, tau, compact support and regularity are unsigned",
            "next_action": "retain Delta_worldtube_domain row",
        },
        {
            "lock_id": "HLOCK2665_2_linking_surfaces",
            "object": "Sigma_H, S_inner, S_outer",
            "contract": "linking surfaces are fixed homology representatives around W_source before readout and avoid the source worldtube",
            "current_status": "CONDITIONAL_TOPOLOGICAL_STEP",
            "blocker": "surface class, boundary/corner terms and domain selector are not parent-signed",
            "next_action": "keep surface-pair and boundary terms explicit",
        },
        {
            "lock_id": "HLOCK2665_3_MHref",
            "object": "M_H_ref",
            "contract": "M_H_ref := H_tau[S_outer]-H_ref = integral_{S_outer} Q_tau after integrability and reference lock",
            "current_status": "DEFINITION_GUARDRAIL_NOT_STABLE",
            "blocker": "delta_H_tau_nonintegrable, Delta_ref, boundary/symplectic flux and tau lock remain missing",
            "next_action": "derive M_H_ref denominator next or stage denominator row",
        },
        {
            "lock_id": "HLOCK2665_4_PiM",
            "object": "Pi_M^H",
            "contract": "Pi_M^H[f]=partial f/partial M_H_ref at fixed tau, surface, reference, C_top and chi_B",
            "current_status": "FORMAL_DEFINITION_ONLY",
            "blocker": "without stable M_H_ref and fixed reference, the projector can absorb reference or boundary variation",
            "next_action": "do not treat Pi_M algebra as flux closure",
        },
        {
            "lock_id": "HLOCK2665_5_commutator_stress",
            "object": "[d,Pi_M]J_H and delta Pi_M stress",
            "contract": "Pi_M must commute with the relevant source flux or carry explicit commutator/projector-stress residual rows",
            "current_status": "RETAINED_UNFILLED_OBSTRUCTION",
            "blocker": "projector algebra Pi_M^2=Pi_M does not imply d(Pi_M J_H)=0",
            "next_action": "retain I_commutator and T_PiM rows",
        },
        {
            "lock_id": "HLOCK2665_6_edge_shadow_split",
            "object": "bulk/edge/shadow split",
            "contract": "Q_bulk, Q_edge and Q_shadow are separate source directions with no cancellation credit",
            "current_status": "SPLIT_REQUIRED_NOT_PARENT_OWNED",
            "blocker": "projector orthogonality, source-shadow silence and edge mass-independence are unsigned",
            "next_action": "use absolute envelope",
        },
        {
            "lock_id": "HLOCK2665_7_verdict",
            "object": "Hamiltonian source-domain/PiM/QbarXH lock",
            "contract": "HLOCK2665_1 through HLOCK2665_6 must close together before Qbar_XH can be score-ready",
            "current_status": "HAMILTONIAN_SOURCE_DOMAIN_PIM_LOCK_NOT_PARENT_DERIVED",
            "blocker": "the lock is exact but current MTS has only conditional pieces",
            "next_action": "attack M_H_ref denominator/integrability-reference lock first",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "lock_pass": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def qbarxh_lock_template_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "row_id": "PIM2665_0_source_domain",
            "factor": "W_source",
            "definition": "closure(supp J_H[tau]) with fixed Hamiltonian slice and compact linked exterior",
            "required_inputs": "J_H; e_obs; tau; compactness; regularity; source_path",
            "current_status": "MISSING_PARENT_WORLDTUBE_SELECTOR",
            "units": "domain_selector",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "PIM2665_1_surface_pair",
            "factor": "S_inner/S_outer",
            "definition": "linked surfaces homologous in the source-free exterior and fixed before readout",
            "required_inputs": "surface_pair; homology class; boundary/corner audit; source_path",
            "current_status": "MISSING_LINKING_SURFACE_LOCK",
            "units": "surface_class",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "PIM2665_2_MHref",
            "factor": "M_H_ref",
            "definition": "H_tau[S_outer]-H_ref after Hamiltonian integrability and reference subtraction are locked",
            "required_inputs": "Q_tau_integral; H_ref; reference_rule; integrability_curl; units; source_path",
            "current_status": "MISSING_STABLE_MH_REF",
            "units": "Hamiltonian_mass_or_energy",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "PIM2665_3_PiM_operator",
            "factor": "Pi_M^H",
            "definition": "partial derivative with respect to M_H_ref at fixed tau, surface, reference, C_top and chi_B",
            "required_inputs": "fixed-variable list; solution-space coordinate; M_H_ref; source_path",
            "current_status": "FORMAL_DEFINITION_ONLY",
            "units": "projector_operator",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "PIM2665_4_projector_obstructions",
            "factor": "I_commutator;T_PiM",
            "definition": "finite rows for [d,Pi_M]J_H and projector metric stress if they are not theorem-zero",
            "required_inputs": "commutator theorem or bound; projector-stress PPN map; units; source_path",
            "current_status": "MISSING_I_COMMUTATOR_AND_PROJECTOR_STRESS_MAP",
            "units": "GM_flux_or_PPN_units",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "PIM2665_5_QbarXH_locked",
            "factor": "Qbar_XH(lambda)",
            "definition": "Pi_M^H[Q_bulk_X^H+Q_edge_X^H+Q_shadow_X^H]/M_H_ref",
            "required_inputs": "all source-domain, PiM, MHref, component split, units and source-path fields",
            "current_status": "BLOCKED_BY_DOMAIN_PROJECTOR_DENOMINATOR",
            "units": "parent_X_charge_per_Hamiltonian_mass",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "source_path": "NONCLAIM_LOCK_TEMPLATE",
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def projector_denominator_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("PDG2665_0_same_frame", "J_H, clocks, rods, orbit/readout and H_tau use the same observed coframe", "MISSING_SAME_FRAME_SOURCE_LOCK"),
        ("PDG2665_1_worldtube", "W_source is selected by parent Hilbert support before readout", "MISSING_PARENT_WORLDTUBE_SELECTOR"),
        ("PDG2665_2_integrability", "H_tau is integrable on the relevant solution branch", "MISSING_DELTA_H_TAU_ZERO_OR_BOUND"),
        ("PDG2665_3_reference", "H_ref/reference subtraction is fixed and derivative-silent", "MISSING_REFERENCE_LOCK"),
        ("PDG2665_4_boundary", "boundary/symplectic flux terms are zero or bounded componentwise", "MISSING_BOUNDARY_SYMPLECTIC_LOCK"),
        ("PDG2665_5_projector", "Pi_M^H fixed-variable list is parent-owned and does not vary with source mask", "MISSING_PROJECTOR_LOCK"),
        ("PDG2665_6_units", "M_H_ref and Q_X units feed the alpha(lambda) ledger", "MISSING_DIMENSIONAL_LEDGER"),
        ("PDG2665_7_verdict", "Hamiltonian source-domain and PiM lock is claim-ready", "PIM_QBARXH_LOCK_NOT_CLAIM_READY"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "condition": condition,
            "current_status": status,
            "gate_pass": False,
            "blocks_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for gate_id, condition, status in rows
    ]


def runner_results_rows(lock_rows: list[dict[str, Any]], template_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for row in lock_rows:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "runner_id": f"RUN2665_{row['lock_id']}",
                "input_id": row["lock_id"],
                "input_type": "lock_contract",
                "has_missing_markers": has_missing(row),
                "score_ready": row["score_ready"],
                "runner_status": "REJECTED_LOCK_NOT_PARENT_DERIVED",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    for row in template_rows:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "runner_id": f"RUN2665_{row['row_id']}",
                "input_id": row["row_id"],
                "input_type": "qbarxh_lock_template",
                "has_missing_markers": has_missing(row),
                "score_ready": row["score_ready"],
                "runner_status": "REJECTED_DOMAIN_PROJECTOR_DENOMINATOR_INPUTS_MISSING",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("CG2665_0_worldtube", "source worldtube is parent-selected", "FAIL_WORLDTUBE_SELECTOR_MISSING", "PDG2665_1_worldtube"),
        ("CG2665_1_MHref", "M_H_ref denominator is stable and same-frame", "FAIL_MHREF_MISSING", "PIM2665_2_MHref"),
        ("CG2665_2_PiM", "Pi_M^H projector is locked with fixed variables", "FAIL_PROJECTOR_LOCK_MISSING", "PIM2665_3_PiM_operator"),
        ("CG2665_3_obstructions", "PiM commutator/projector-stress obstructions are zero or bounded", "FAIL_PIM_OBSTRUCTIONS_MISSING", "PIM2665_4_projector_obstructions"),
        ("CG2665_4_Qbar", "Qbar_XH is score-ready", "FAIL_QBARXH_LOCK_TEMPLATE", "PIM2665_5_QbarXH_locked"),
        ("CG2665_5_verdict", "R10/local source projection can be scored or claimed", "CLAIM_BLOCKED", "domain, projector and denominator are unsigned"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "requirement": requirement,
            "current_status": status,
            "evidence_ref": evidence_ref,
            "gate_pass": False,
            "blocks_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for gate_id, requirement, status, evidence_ref in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "decision_id": "DEC2665_0_lock_status",
            "decision": "Hamiltonian source-domain and PiM lock is exact but not derived",
            "reason": "worldtube, M_H_ref, fixed-variable PiM, commutator and projector-stress clauses remain unsigned",
            "next_action": "do not use Qbar_XH numerically",
        },
        {
            "decision_id": "DEC2665_1_no_shortcuts",
            "decision": "bare mass, orbital GM, fitted source radius and reference-only zero are forbidden",
            "reason": "each would use the observed readout as the denominator the theorem is meant to derive",
            "next_action": "carry denominator and numerator pieces together",
        },
        {
            "decision_id": "DEC2665_2_best_next",
            "decision": "attack M_H_ref denominator/integrability-reference lock next",
            "reason": "without stable M_H_ref, Pi_M^H is only notation and Qbar_XH cannot be score-ready",
            "next_action": "derive H_tau integrability plus H_ref/reference silence or stage a denominator row",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2665_0_selected",
            "status": "selected",
            "next_doc": "2666-Y5-R2FR-MHref-integrability-reference-lock-or-denominator-row.md",
            "next_script": "scripts/Y5_R2FR_MHref_integrability_reference_lock_or_denominator_row_2666.py",
            "task": "derive or source-stage the stable M_H_ref denominator: H_tau integrability, H_ref/reference silence, boundary/symplectic flux and units",
            "must_include": "delta_H_tau_nonintegrable, H_ref, Delta_ref, B_zero_flux, Delta_symp, tau/surface pair, source path, units and no-cancellation total",
            "must_exclude": "bare mass denominator, orbital GM denominator, reference-only zero, unnormalized Qbar/R_eq rows, R10/local-GR pass claim, GitHub action, formalization-workbench edits",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("STAT2665_0_progress", "Qbar_XH lock", "DOMAIN_PROJECTOR_DENOMINATOR_CONTRACT_EXPLICIT", "source-domain, PiM and M_H_ref are now one lock gate"),
        ("STAT2665_1_blocker", "M_H_ref", "DENOMINATOR_IS_NEXT_ROOT_BLOCKER", "stable Hamiltonian mass must precede any Qbar or R10 score"),
        ("STAT2665_2_guardrail", "shortcuts", "BARE_MASS_OR_ORBITAL_GM_FORBIDDEN", "readout denominators cannot replace a derived Hamiltonian source charge"),
        ("STAT2665_3_project", "GR/local route", "SOURCE_SIDE_SHARPER_NOT_CLOSED", "the source side is becoming derivable as a chain of exact gates, but not claim-ready"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": status_id,
            "topic": topic,
            "status": status,
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for status_id, topic, status, detail in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    generated = stamp()
    copy_specs = {
        "queue": (OUTPUTS["qbarxh_lock_template"], BRANCH_COPIES["queue"], "Hamiltonian source-domain/PiM input queue"),
        "local_bounds": (OUTPUTS["lock_contract"], BRANCH_COPIES["local_bounds"], "Hamiltonian source-domain/PiM lock contract"),
        "source_weight": (OUTPUTS["qbarxh_lock_template"], BRANCH_COPIES["source_weight"], "QbarXH PiM/MHref lock template"),
        "microscope": (OUTPUTS["qbarxh_lock_template"], BRANCH_COPIES["microscope"], "microscope QbarXH PiM lock copy"),
        "quarantine": (OUTPUTS["runner_results"], BRANCH_COPIES["quarantine"], "lock runner refusal results"),
    }
    rows: list[dict[str, Any]] = []
    for copy_id, (source, destination, role) in copy_specs.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, destination)
        parseable = False
        if destination.exists():
            try:
                read_csv(destination)
                parseable = True
            except Exception:
                parseable = False
        rows.append(
            {
                "copy_id": f"COPY2665_{copy_id}",
                "role": role,
                "source": str(source),
                "destination": str(destination),
                "exists": destination.exists(),
                "parseable_csv": parseable,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def generated_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())


def all_csv_parse(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            read_csv(path)
        except Exception:
            return False
    return True


def formalization_hit_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = [
        "*2665-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2665*",
        "*Y5_R2FR_Hamiltonian_source_domain_and_PiM_QbarXH_lock_2665*",
        "*JR2665*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    lock_ok = any(
        row["lock_id"] == "HLOCK2665_7_verdict"
        and row["current_status"] == "HAMILTONIAN_SOURCE_DOMAIN_PIM_LOCK_NOT_PARENT_DERIVED"
        for row in rows["lock_contract"]
    ) and all(not row["lock_pass"] and not row["score_ready"] and not row["valid_for_claim"] for row in rows["lock_contract"])
    template_ok = any(row["row_id"] == "PIM2665_5_QbarXH_locked" for row in rows["qbarxh_lock_template"]) and all(
        not row["score_ready"] and not row["valid_for_claim"] for row in rows["qbarxh_lock_template"]
    )
    gate_ok = all(not row["gate_pass"] and row["blocks_claim"] for row in rows["projector_denominator_gate"]) and any(
        row["gate_id"] == "PDG2665_7_verdict" and row["current_status"] == "PIM_QBARXH_LOCK_NOT_CLAIM_READY"
        for row in rows["projector_denominator_gate"]
    )
    runner_ok = len(rows["runner_results"]) == len(rows["lock_contract"]) + len(rows["qbarxh_lock_template"]) and all(
        row["runner_status"] in {"REJECTED_LOCK_NOT_PARENT_DERIVED", "REJECTED_DOMAIN_PROJECTOR_DENOMINATOR_INPUTS_MISSING"}
        for row in rows["runner_results"]
    )
    claim_ok = any(
        row["gate_id"] == "CG2665_5_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]
    ) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["claim_gates"])
    next_ok = any("2666-Y5-R2FR-MHref-integrability-reference-lock" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2665_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2665_01_lock_contract", lock_ok, "Hamiltonian source-domain/PiM/QbarXH lock contract is written and nonclaim"),
        ("VAL2665_02_template", template_ok, "QbarXH lock template is staged as nonclaim"),
        ("VAL2665_03_projector_denominator_gate", gate_ok, "projector/denominator gates block claim promotion"),
        ("VAL2665_04_runner_refuses", runner_ok, "runner rejects unsigned lock and missing inputs"),
        ("VAL2665_05_claim_gates_blocked", claim_ok, "R10/local claim gates remain blocked"),
        ("VAL2665_06_next_target", next_ok, "2666 M_H_ref denominator target selected"),
        ("VAL2665_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2665_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2665_09_formalization_untouched", formal_ok, "no 2665 outputs are written under formalization-workbench"),
        ("VAL2665_10_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
    ]
    generated = stamp()
    out = [
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in checks
    ]
    out.append(
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": "VAL2665_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2665 consolidates the Hamiltonian source-domain/PiM/QbarXH lock, forbids denominator shortcuts, and selects M_H_ref integrability/reference lock next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = read_csv(OUTPUTS["validation"])
    content = f"""# 2665 - Hamiltonian Source-Domain And PiM QbarXH Lock

## Purpose

This checkpoint locks the object that `Qbar_XH` needs before it can ever become numeric: a parent-owned source worldtube, a fixed Hamiltonian mass projector `Pi_M^H`, and a stable same-frame denominator `M_H_ref`.

## Result

- The exact lock is written: `Qbar_XH(lambda)=Pi_M^H[Q_bulk_X^H+Q_edge_X^H+Q_shadow_X^H]/M_H_ref`.
- The legal source domain is `W_source=closure(supp J_H[tau])`, not a fitted mass mask or post-readout radius.
- `Pi_M^H` is only formal until `M_H_ref`, fixed reference data and projector variation are owned.
- Bare mass, orbital `GM`, fitted source masks and reference-only zeros are forbidden as denominator shortcuts.
- The next root target is `M_H_ref`: Hamiltonian integrability, reference silence, boundary/symplectic flux and units.

## Source Register

{markdown_table(rows["source_register"])}

## Lock Contract

{markdown_table(rows["lock_contract"])}

## QbarXH Lock Template

{markdown_table(rows["qbarxh_lock_template"])}

## Projector Denominator Gate

{markdown_table(rows["projector_denominator_gate"])}

## Runner Results

{markdown_table(rows["runner_results"])}

## Claim Gates

{markdown_table(rows["claim_gates"])}

## Decision Ledger

{markdown_table(rows["decision"])}

## Next Target

{markdown_table(rows["next_target"])}

## Project Status Snapshot

{markdown_table(rows["project_status"])}

## Branch Copies

{markdown_table(rows["branch_copies"])}

## Validation

{markdown_table(validation)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "lock_contract": lock_contract_rows(),
        "qbarxh_lock_template": qbarxh_lock_template_rows(),
        "projector_denominator_gate": projector_denominator_gate_rows(),
    }
    rows["runner_results"] = runner_results_rows(rows["lock_contract"], rows["qbarxh_lock_template"])
    rows["claim_gates"] = claim_gate_rows()
    rows["decision"] = decision_rows()
    rows["next_target"] = next_target_rows()
    rows["project_status"] = project_status_rows()
    for name, table in rows.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], table)
    rows["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows["branch_copies"])
    remove_pycache()
    rows["validation"] = validation_rows(rows, generated_paths())
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)
    remove_pycache()


if __name__ == "__main__":
    main()

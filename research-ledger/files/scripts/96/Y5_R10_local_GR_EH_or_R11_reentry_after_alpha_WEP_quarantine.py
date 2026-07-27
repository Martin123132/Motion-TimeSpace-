from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "768-Y5-R10-local-GR-EH-or-R11-reentry-after-alpha-WEP-quarantine.md"
NEXT_TARGET = "769-Y5-R10-FB554-0-Hamiltonian-integrability-reference-row-reentry.md"
STATUS = "Y5_R10_768_local_GR_reentry_after_alpha_WEP_quarantine_selects_HPiM_FB5540_live_edge_nonclaim"
CLAIM_CEILING = "EH_R11_source_normalization_reentry_only_no_EH_Newton_PPN_R10_R11_or_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_768_SOURCE_REGISTER.csv"
EH_R11_REENTRY_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_768_EH_R11_REENTRY_AUDIT.csv"
R11_SOURCE_NORMALIZATION_LIVE_EDGE_PATH = RESIDUALS / "P8_Y5_R10_768_R11_SOURCE_NORMALIZATION_LIVE_EDGE.csv"
HAMILTONIAN_PIM_LIVE_EDGE_PATH = RESIDUALS / "P8_Y5_R10_768_HAMILTONIAN_PIM_LIVE_EDGE.csv"
GR_NEWTON_REQUIREMENT_MAP_PATH = RESIDUALS / "P8_Y5_R10_768_GR_NEWTON_REQUIREMENT_MAP.csv"
SOURCE_FILL_SCHEMA_PATH = RESIDUALS / "P8_Y5_R10_768_SOURCE_FILL_SCHEMA.csv"
DECISION_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_768_DECISION_MATRIX.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_768_ROUTE_UPDATE.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_768_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_768_VALIDATION.csv"

CANDIDATE_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_768_FB554_0_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_768_PIM_HAMILTONIAN_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_768_EH_R11_OPERATOR_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_768_PPN_READOUT_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_768_SOURCE_EQUALITY_INPUT_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    EH_R11_REENTRY_AUDIT_PATH,
    R11_SOURCE_NORMALIZATION_LIVE_EDGE_PATH,
    HAMILTONIAN_PIM_LIVE_EDGE_PATH,
    GR_NEWTON_REQUIREMENT_MAP_PATH,
    SOURCE_FILL_SCHEMA_PATH,
    DECISION_MATRIX_PATH,
    ROUTE_UPDATE_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCES: dict[str, dict[str, Any]] = {
    "767_doc": {
        "path": POST_CHECKPOINT / "767-Y5-R10-parent-matter-functor-no-alpha-vertex-or-WEP-closure.md",
        "needles": [
            "Current result: **the parent matter functor/no-alpha-vertex theorem is still not signed",
            "768-Y5-R10-local-GR-EH-or-R11-reentry-after-alpha-WEP-quarantine.md",
        ],
        "role": "immediate alpha/WEP quarantine handoff into local-GR reentry",
    },
    "767_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_767_VALIDATION.csv",
        "needles": ["V767_12_next_target_selected", "pass"],
        "role": "prior 767 validation guard",
    },
    "654_doc": {
        "path": POST_CHECKPOINT / "654-Y5-R10-local-GR-reduction-spine-under-explicit-WEP-closure.md",
        "needles": [
            "WEP/common matter geometry is now carried as explicit closure",
            "EH operator selection, source charge/GM normalization",
        ],
        "role": "local-GR spine under explicit WEP closure",
    },
    "654_spine": {
        "path": RESIDUALS / "P8_Y5_R10_654_LOCAL_GR_SPINE.csv",
        "needles": ["EH_operator_selection", "weak_field_PPN_readout"],
        "role": "local-GR dependency ladder",
    },
    "655_doc": {
        "path": POST_CHECKPOINT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
        "needles": ["EH-only theorem route remains unsigned", "R11 route exists only as a template"],
        "role": "EH-only failure and retained R11 branch",
    },
    "655_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_655_VALIDATION.csv",
        "needles": ["pass"],
        "role": "prior 655 validation guard",
    },
    "655_r11_status": {
        "path": RESIDUALS / "P8_Y5_R10_655_R11_RETAINED_OPERATOR_VECTOR_STATUS.csv",
        "needles": ["R11", "valid_for_claim"],
        "role": "retained non-EH/R11 operator status",
    },
    "656_doc": {
        "path": POST_CHECKPOINT / "656-Y5-R10-R11-executable-vector-minimum-skeleton-under-WEP-closure.md",
        "needles": [
            "Y5_R10_R11_minimum_skeleton_built_nonclaim_under_explicit_WEP_closure",
            "score_ready=false and valid_for_claim=false",
        ],
        "role": "R11 minimum skeleton",
    },
    "656_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_656_VALIDATION.csv",
        "needles": ["pass"],
        "role": "prior 656 validation guard",
    },
    "656_skeleton": {
        "path": RESIDUALS / "P8_Y5_R10_656_R11_MINIMUM_SKELETON.csv",
        "needles": ["source_normalization_operator", "R11_MIN_SKELETON_656"],
        "role": "R11 operator family work order",
    },
    "657_doc": {
        "path": POST_CHECKPOINT / "657-Y5-R10-source-normalization-family-first-real-R11-fill.md",
        "needles": ["first real fill of the retained `source_normalization_operator`", "mu_extra=0"],
        "role": "source-normalization family decomposition",
    },
    "657_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_657_VALIDATION.csv",
        "needles": ["pass"],
        "role": "prior 657 validation guard",
    },
    "657_cmu_fill": {
        "path": RESIDUALS / "P8_Y5_R10_657_CMU_SOURCE_NORMALIZATION_FILL.csv",
        "needles": ["c_mu := epsilon_mu := mu_extra/(G_obs*M_obs) = sum_i epsilon_i"],
        "role": "exact c_mu sum rule",
    },
    "658_doc": {
        "path": POST_CHECKPOINT / "658-Y5-R10-cmu-radial-calibration-zero-or-numeric-envelope.md",
        "needles": ["epsilon_radial_Meff", "theorem-or-envelope target"],
        "role": "radial calibration identity",
    },
    "658_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_658_VALIDATION.csv",
        "needles": ["pass"],
        "role": "prior 658 validation guard",
    },
    "658_radial_identity": {
        "path": RESIDUALS / "P8_Y5_R10_658_RADIAL_IDENTITY.csv",
        "needles": ["epsilon_radial_Meff", "integral_{A_ext} d(Pi_M J)"],
        "role": "exact radial residual identity",
    },
    "659_doc": {
        "path": POST_CHECKPOINT / "659-Y5-R10-parent-source-identity-for-closed-PiM-flux-or-radial-profile-fill.md",
        "needles": ["d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent", "conditional_theorem_proved"],
        "role": "PiM flux obstruction identity",
    },
    "659_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_659_VALIDATION.csv",
        "needles": ["pass"],
        "role": "prior 659 validation guard",
    },
    "659_closure_identity": {
        "path": RESIDUALS / "P8_Y5_R10_659_CLOSURE_IDENTITY.csv",
        "needles": ["ID659_3_obstruction_identity", "[d,Pi_M]J_H"],
        "role": "closed projected flux decomposition",
    },
    "660_doc": {
        "path": POST_CHECKPOINT / "660-Y5-R10-PiM-commutator-zero-or-projector-stress-vector.md",
        "needles": ["commutator can be killed cleanly only by a parent-owned topological/fixed `Pi_M`", "projector-stress vector"],
        "role": "PiM commutator zero gate",
    },
    "660_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_660_VALIDATION.csv",
        "needles": ["pass"],
        "role": "prior 660 validation guard",
    },
    "660_commutator_audit": {
        "path": RESIDUALS / "P8_Y5_R10_660_COMMUTATOR_ZERO_AUDIT.csv",
        "needles": ["CZ660_1_metric_independent_projector", "parent_signed"],
        "role": "commutator zero clause audit",
    },
    "661_doc": {
        "path": POST_CHECKPOINT / "661-Y5-R10-topological-Hilbert-current-equality-or-projector-stress-fill.md",
        "needles": ["J_M_top", "parent worldtube/source-measure glue is still missing"],
        "role": "topological current versus Hilbert current blocker",
    },
    "661_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_661_VALIDATION.csv",
        "needles": ["pass"],
        "role": "prior 661 validation guard",
    },
    "661_obstruction": {
        "path": RESIDUALS / "P8_Y5_R10_661_EQUALITY_OBSTRUCTION_AUDIT.csv",
        "needles": ["Q_M defined from the same parent Hilbert compact-source variation", "missing_parent_worldtube_glue"],
        "role": "Hilbert/topological equality obstruction",
    },
    "662_doc": {
        "path": POST_CHECKPOINT / "662-Y5-R10-Hilbert-worldtube-source-measure-glue-or-equality-residual-bound.md",
        "needles": ["R_glue := Pi_M J_H - J_M_top - dB_zero", "current MTS has not yet signed"],
        "role": "worldtube/source-measure glue theorem attempt",
    },
    "662_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_662_VALIDATION.csv",
        "needles": ["pass"],
        "role": "prior 662 validation guard",
    },
    "662_residual": {
        "path": RESIDUALS / "P8_Y5_R10_662_RESIDUAL_DECOMPOSITION.csv",
        "needles": ["R_worldtube", "R_PiM"],
        "role": "worldtube/source-measure residual decomposition",
    },
    "663_doc": {
        "path": POST_CHECKPOINT / "663-Y5-R10-minimal-parent-action-source-current-Euler-Ward-test-or-residual-input-fill.md",
        "needles": ["The Euler/Ward route survives as real mathematics", "Pi_M^H"],
        "role": "minimal parent action Euler/Ward route",
    },
    "663_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_663_VALIDATION.csv",
        "needles": ["pass"],
        "role": "prior 663 validation guard",
    },
    "663_chain": {
        "path": RESIDUALS / "P8_Y5_R10_663_EULER_WARD_CHAIN_RESULT.csv",
        "needles": ["EW663_5_PiM_Hamiltonian_identification", "Pi_M^H"],
        "role": "Euler/Ward chain result",
    },
    "664_doc": {
        "path": POST_CHECKPOINT / "664-Y5-R10-Hamiltonian-PiM-integrability-source-equality-or-first-residual-fill.md",
        "needles": ["delta H_tau = int_S(delta Q_tau - i_tau theta)", "FB554_0_HPiM_integrability_reference_bound"],
        "role": "Hamiltonian PiM integrability/source equality gate",
    },
    "664_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_664_VALIDATION.csv",
        "needles": ["pass"],
        "role": "prior 664 validation guard",
    },
    "664_first_residual": {
        "path": RESIDUALS / "P8_Y5_R10_664_FIRST_RESIDUAL_FILL.csv",
        "needles": ["FB554_0_HPiM_integrability_reference_bound", "selected_first"],
        "role": "first Hamiltonian PiM residual fill row",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post_checkpoint(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed_count = 0
    for scanned_path in FORMALIZATION.rglob("*"):
        if scanned_path.is_file() and datetime.fromtimestamp(scanned_path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            changed_count += 1
    return changed_count


def validation_clean(number: int) -> bool:
    validation_path = RESIDUALS / f"P8_Y5_BRR545_{number}_VALIDATION.csv"
    validation_rows = read_csv_rows(validation_path)
    return validation_path.exists() and bool(validation_rows) and all(row.get("result") == "pass" for row in validation_rows)


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(source_spec["path"]),
            "exists": bool_string(Path(source_spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(source_spec["path"]), source_spec["needles"])),
            "role": source_spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, source_spec in SOURCES.items()
    ]


def eh_r11_reentry_audit_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "EHR768_0_WEP_guard",
            "gate": "WEP/common matter geometry",
            "current_state_after_767": "explicit_closure_quarantined_not_parent_theorem",
            "imported_basis": "767 boxes WEP/no-alpha safety as closure/fallback; 654 carries WEP closure only as a private branch condition",
            "why_it_matters": "WEP closure may organize the local branch but cannot pay the EH, Newton, PPN, R10, or local-GR proof debt",
            "next_action": "keep WEP label visible on every downstream row",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "EHR768_1_EH_only",
            "gate": "Einstein-Hilbert operator selection",
            "current_state_after_767": "blocked_current_state_from_655",
            "imported_basis": "655 says the EH-only theorem route remains unsigned",
            "why_it_matters": "a one-frame matter closure does not force the exterior field operator to be EH",
            "next_action": "do not claim EH-only unless extra sectors, LC compatibility, boundary terms, source normalization, and PPN readout close",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "EHR768_2_R11_skeleton",
            "gate": "retained non-EH/R11 vector",
            "current_state_after_767": "minimum_skeleton_exists_template_only_nonclaim",
            "imported_basis": "656 builds branch-specific operator families but leaves coefficients, units, normalization, and weak-field maps missing",
            "why_it_matters": "if EH-only is not proved, the non-EH vector must be executable and scoreable before local GR can be claimed",
            "next_action": "keep R11 as retained operator ledger, not evidence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "EHR768_3_source_normalization",
            "gate": "Newton/source charge normalization",
            "current_state_after_767": "active_live_edge_nonnumeric_sum_rule",
            "imported_basis": "657 decomposes c_mu exactly; 658-662 narrow which pieces can be zeroed",
            "why_it_matters": "Newton recovery needs a stable observed mass/GM source, not just a metric operator",
            "next_action": "route through Hamiltonian PiM source charge before Gauss/PPN",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "EHR768_4_radial_flux",
            "gate": "radial/profile and projected-current flux",
            "current_state_after_767": "exact_identity_written_not_zero",
            "imported_basis": "658 writes epsilon_radial_Meff; 659-660 show PiM commutator/projector stress remains unsigned",
            "why_it_matters": "radial source hair would leak into R10/R11/PPN and fake or spoil Newtonian source normalization",
            "next_action": "do not assign radial zero until PiM/source-current identity is parent-owned or bounded",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "EHR768_5_Hamiltonian_PiM",
            "gate": "Hamiltonian PiM source charge",
            "current_state_after_767": "selected_live_edge_FB554_0",
            "imported_basis": "663 selects Pi_M^H as clean repair; 664 selects FB554_0 integrability/reference as first residual fill/proof row",
            "why_it_matters": "without an integrable fixed-reference Hamiltonian charge, Pi_M^H is notation, not a physical source-mass operator",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def r11_source_normalization_live_edge_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "edge_id": "RSN768_0_cmu_sum_rule",
            "object": "c_mu",
            "formula": "c_mu := epsilon_mu := mu_extra/(G_obs*M_obs) = sum_i epsilon_i",
            "current_state": "exact_decomposition_nonnumeric_nonclaim",
            "missing_lock": "each epsilon_i needs theorem-zero or source-backed numeric bound; no cancellation credit",
            "observable_pressure": "Newton source normalization; WEP; PPN beta/gamma; Gdot; R10; R11",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_657_CMU_SOURCE_NORMALIZATION_FILL.csv"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "edge_id": "RSN768_1_radial_identity",
            "object": "epsilon_radial_Meff",
            "formula": "epsilon_radial_Meff=[c_M/M_eff(r1)] integral_{A_ext} d(Pi_M J)",
            "current_state": "exact_residual_law_written_identity_not_zero",
            "missing_lock": "projected mass current must be closed or bounded across local exterior annulus",
            "observable_pressure": "radial fifth-force/R10 residual; orbital GM stability; PPN source charge",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_658_RADIAL_IDENTITY.csv"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "edge_id": "RSN768_2_flux_obstruction",
            "object": "d(Pi_M J_H)",
            "formula": "d(Pi_M J_H)= -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent",
            "current_state": "exact_obstruction_decomposition_not_zero",
            "missing_lock": "extra projection, PiM commutator, and parent anomaly terms must vanish or be bounded",
            "observable_pressure": "source-normalization; R10/R11; PPN preferred-frame and gamma/beta residuals",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_659_CLOSURE_IDENTITY.csv"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "edge_id": "RSN768_3_worldtube_glue",
            "object": "R_glue",
            "formula": "R_glue := Pi_M J_H - J_M_top - dB_zero = R_worldtube + R_measure + R_PiM + R_top + R_boundary + R_extra",
            "current_state": "conditional_theorem_written_parent_unsigned",
            "missing_lock": "parent worldtube selector, same-frame measure, PiM chain map, boundary, and extra-sector silence",
            "observable_pressure": "Newton source charge; orbital denominator; local clocks; PPN and R10",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_662_RESIDUAL_DECOMPOSITION.csv"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "edge_id": "RSN768_4_HPiM_repair",
            "object": "Pi_M^H",
            "formula": "(4*pi*G_ref)^-1 int_S Pi_M J_H = int_S Q_tau",
            "current_state": "best_repair_candidate_not_promotion",
            "missing_lock": "Hamiltonian charge integrability, fixed reference, same-frame source measure, old PiM demotion/equivalence, C-term silence, PPN readout",
            "observable_pressure": "Newtonian mass operator; PPN; R10/R11; local-GR branch",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_663_EULER_WARD_CHAIN_RESULT.csv"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def hamiltonian_pim_live_edge_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "hpi_id": "HPI768_0_integrability_target",
            "lock": "finite integrable Hamiltonian mass functional",
            "expression": "delta H_tau = int_S(delta Q_tau - i_tau theta)",
            "current_state": "target_defined_not_parent_derived",
            "missing_inputs": "explicit MTS theta; Q_tau; constraint split; delta^2H_tau=0 proof; normalized M_H_ref",
            "why_first": "if H_tau is not integrable, Pi_M^H cannot define the local source mass",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hpi_id": "HPI768_1_reference_lock",
            "lock": "fixed boundary/reference subtraction",
            "expression": "partial_{source,r,t,frame} B_ref = 0",
            "current_state": "fail_current_claim",
            "missing_inputs": "source-independent reference branch; no frame/readout/radius/time absorption",
            "why_first": "otherwise the source mass can be hidden in reference choice",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_664_OBSTRUCTION_LEDGER.csv"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hpi_id": "HPI768_2_tau_lock",
            "lock": "same observed time generator",
            "expression": "tau_source=tau_charge=tau_orbit and delta tau=0",
            "current_state": "open",
            "missing_inputs": "one observed coframe/time theorem tying clocks, charge, and orbital readout",
            "why_first": "source equality and Gdot/PPN readout become frame-dependent without this lock",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hpi_id": "HPI768_3_symplectic_boundary_flux",
            "lock": "no extra symplectic/boundary leakage",
            "expression": "int_boundary(delta Q_tau-i_tau theta)_extra=0 or fixed",
            "current_state": "fail_current_claim",
            "missing_inputs": "Delta_symp=0; B_zero_flux=0; projector/boundary no-hair theorem",
            "why_first": "extra boundary flux becomes an unscored source-normalization channel",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_664_FIRST_RESIDUAL_FILL.csv"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hpi_id": "HPI768_4_source_equality_downstream",
            "lock": "same worldtube source equals Hamiltonian charge",
            "expression": "M_source[W]=G_ref^-1 int_S Q_tau",
            "current_state": "not_signed_after_integrability",
            "missing_inputs": "same-frame worldtube source measure; Delta_frame; Delta_cal; Delta_boundary; Delta_extra",
            "why_first": "this is second after FB554_0; it should not be attempted by substituting orbital GM",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_664_SOURCE_EQUALITY_ATTEMPT.csv"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hpi_id": "HPI768_5_next_selected",
            "lock": "first fill/proof row",
            "expression": "FB554_0 = abs(delta_H_tau_nonintegrable_over_MH)+abs(Delta_ref_over_MH)+abs(symplectic_boundary_flux_over_MH)",
            "current_state": "selected_first_reentry_target",
            "missing_inputs": "prove each component zero or fill with source-backed units, assumptions, and valid_for_claim=true rows",
            "why_first": "it is the bottleneck before source equality, radial C-terms, Gauss readout, and PPN",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_664_FIRST_RESIDUAL_FILL.csv"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def gr_newton_requirement_map_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "GN768_0_WEP_visibility",
            "reduction_need": "one matter/source/clock geometry kept visible as closure, not theorem",
            "current_artifact": "767 WEP quarantine plus 654 local-GR spine",
            "missing_derivation": "parent matter functor/no-alpha/no-mass vertex remains unsigned",
            "downstream_tests": "WEP; clocks; local constants; source frame",
            "claim_status": "closure_only_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "GN768_1_operator_equations",
            "reduction_need": "EH field equations or executable retained non-EH/R11 vector",
            "current_artifact": "655 EH/R11 gate and 656 R11 skeleton",
            "missing_derivation": "EH-only not parent-selected; R11 coefficients/units/weak-field maps missing",
            "downstream_tests": "PPN gamma/beta/alpha_i/xi; R10 fifth force; gravitational-wave/local-GR consistency",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "GN768_2_source_charge",
            "reduction_need": "stable observed mass/GM source charge before orbital fitting",
            "current_artifact": "657 c_mu sum rule; 658-662 PiM/source-current obstruction chain",
            "missing_derivation": "PiM/Hilbert/worldtube/source-measure glue and radial closure not signed",
            "downstream_tests": "Newtonian inverse-square normalization; orbital dynamics; R10/R11 source residuals",
            "claim_status": "active_live_edge",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "GN768_3_HPiM_integrability",
            "reduction_need": "integrable fixed-reference Hamiltonian mass charge",
            "current_artifact": "664 FB554_0 selected first",
            "missing_derivation": "theta/Q_tau/B_ref/tau lock and boundary flux zero theorem or bound",
            "downstream_tests": "Newton source normalization; Gdot; PPN; R10/R11; local-GR source term",
            "claim_status": "next_target_selected",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "GN768_4_PPN_readout",
            "reduction_need": "gamma=beta=1, alpha_i=xi=0, no Gdot, no finite-range residue",
            "current_artifact": "654/655/664 map PPN as downstream readout, not current proof",
            "missing_derivation": "weak-field expansion of selected operator plus source charge and residual vector",
            "downstream_tests": "Cassini; perihelion; lunar laser ranging; clocks; R10",
            "claim_status": "not_ready",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def source_fill_schema_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "fill_id": "SFS768_0_FB554_0_input",
            "artifact": str(CANDIDATE_ARTIFACTS[0]),
            "required_columns": "component;value;units;source_path;assumptions;zero_theorem_or_bound;valid_for_claim",
            "claim_gate": "all FB554_0 components theorem-zero or source-backed numeric with units",
            "current_status": "schema_only_candidate_missing=true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS768_1_PiM_Hamiltonian_input",
            "artifact": str(CANDIDATE_ARTIFACTS[1]),
            "required_columns": "theta;Q_tau;B_ref;tau_lock;constraint_split;source_path;valid_for_claim",
            "claim_gate": "MTS parent action supplies covariant-phase-space charge data",
            "current_status": "schema_only_candidate_missing=true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS768_2_EH_R11_operator_input",
            "artifact": str(CANDIDATE_ARTIFACTS[2]),
            "required_columns": "operator_family;coefficient;units;normalization;weak_field_map;source_path;valid_for_claim",
            "claim_gate": "EH-only theorem or score-ready retained R11 vector",
            "current_status": "schema_only_candidate_missing=true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS768_3_PPN_readout_input",
            "artifact": str(CANDIDATE_ARTIFACTS[3]),
            "required_columns": "ppn_parameter;prediction;bound;units;operator_source;mass_source;valid_for_claim",
            "claim_gate": "PPN vector derived from same operator and same source charge",
            "current_status": "schema_only_candidate_missing=true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS768_4_source_equality_input",
            "artifact": str(CANDIDATE_ARTIFACTS[4]),
            "required_columns": "worldtube;surface;M_source;Q_tau;Delta_frame;Delta_cal;source_path;valid_for_claim",
            "claim_gate": "same worldtube source equals Hamiltonian charge before orbital fitting",
            "current_status": "schema_only_candidate_missing=true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_matrix_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D768_0_reentry_position",
            "decision": "resume GR/Newton reduction with WEP closure visible but quarantined",
            "rationale": "alpha/WEP work sharpened the closure label; it did not derive the parent matter functor",
            "claim_status": "nonclaim_private_branch",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D768_1_EH_route",
            "decision": "do not restart at EH-only prose",
            "rationale": "655 already shows EH-only remains unsigned; without source charge, even EH prose cannot yield Newton recovery",
            "claim_status": "blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D768_2_R11_route",
            "decision": "keep R11 as retained ledger, not a promoted theory branch",
            "rationale": "656 skeleton lacks coefficient values, units, normalization, and weak-field maps",
            "claim_status": "scaffold_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D768_3_live_edge",
            "decision": "select FB554_0 Hamiltonian PiM integrability/reference as the next live target",
            "rationale": "the source-mass operator must be a real integrable charge before source equality, Gauss, PPN, or R10 can be scored",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_update_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU768_0_allowed",
            "allowed_after_768": "use WEP/common matter frame only as an explicitly labelled closure condition",
            "forbidden_after_768": "cite WEP/common frame as a parent-derived proof or as an EH/PPN/Newton pass",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU768_1_allowed",
            "allowed_after_768": "work from Hamiltonian PiM source charge toward Newton/GR reduction",
            "forbidden_after_768": "substitute orbital GM for source equality before a charge theorem",
            "next_action": "prove or source-fill FB554_0 components",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU768_2_allowed",
            "allowed_after_768": "keep EH-only and retained R11 routes side-by-side as blocked alternatives",
            "forbidden_after_768": "promote R11 skeleton rows as executable coefficient predictions",
            "next_action": "only return to EH/R11 coefficients after source charge/integrability is stable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "alpha/WEP is quarantined; local-GR reentry now points at Hamiltonian PiM source-charge integrability, not at a hidden WEP or EH assumption",
            "hard_blocker": "FB554_0_HPiM_integrability_reference_bound remains missing theorem-zero or source-backed inputs",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_claim_rows_false(row_groups: list[list[dict[str, Any]]]) -> bool:
    rows_with_claim_field = [
        row
        for row_group in row_groups
        for row in row_group
        if "valid_for_claim" in row
    ]
    return bool(rows_with_claim_field) and all(str(row["valid_for_claim"]).lower() == "false" for row in rows_with_claim_field)


def validation_rows(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    source_edges: list[dict[str, Any]],
    hamiltonian_edges: list[dict[str, Any]],
    requirement_map: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_767_clean = validation_clean(767)
    prior_655_to_664_clean = all(validation_clean(number) for number in range(655, 665))
    wep_quarantined = any(row["audit_id"] == "EHR768_0_WEP_guard" and "quarantined" in row["current_state_after_767"] for row in audit)
    eh_blocked = any(row["audit_id"] == "EHR768_1_EH_only" and row["current_state_after_767"].startswith("blocked") for row in audit)
    r11_scaffold = any(row["audit_id"] == "EHR768_2_R11_skeleton" and "skeleton" in row["current_state_after_767"] for row in audit)
    cmu_imported = any(row["edge_id"] == "RSN768_0_cmu_sum_rule" and "sum_i epsilon_i" in row["formula"] for row in source_edges)
    fb5540_selected = any(row["hpi_id"] == "HPI768_5_next_selected" and "FB554_0" in row["expression"] for row in hamiltonian_edges)
    gr_newton_requirements_written = len(requirement_map) >= 5 and any(row["requirement_id"] == "GN768_3_HPiM_integrability" for row in requirement_map)
    candidate_artifacts_not_faked = all(not path.exists() for path in CANDIDATE_ARTIFACTS)
    all_nonclaim = all_claim_rows_false([sources, audit, source_edges, hamiltonian_edges, requirement_map, source_fill, decisions, routes, summary])
    next_target_selected = any(row["next_target"] == NEXT_TARGET for row in decisions) and summary[0]["next_target"] == NEXT_TARGET
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V768_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V768_1_source_needles_present", source_needles_present, "all local source needles present"),
        ("V768_2_prior_767_clean", prior_767_clean, "767 validation has no failures"),
        ("V768_3_prior_655_664_clean", prior_655_to_664_clean, "655-664 validation rows have no failures"),
        ("V768_4_WEP_quarantine_visible", wep_quarantined, "WEP closure remains explicit and nonclaim"),
        ("V768_5_EH_only_blocked", eh_blocked, "EH-only route remains blocked"),
        ("V768_6_R11_skeleton_nonclaim", r11_scaffold, "R11 skeleton retained as scaffold only"),
        ("V768_7_cmu_sum_rule_imported", cmu_imported, "c_mu exact sum rule imported"),
        ("V768_8_FB554_0_live_edge_selected", fb5540_selected, "Hamiltonian PiM FB554_0 selected first"),
        ("V768_9_GR_Newton_map_written", gr_newton_requirements_written, "GR/Newton requirements mapped without promotion"),
        ("V768_10_source_fill_schema_written", len(source_fill) == len(CANDIDATE_ARTIFACTS), "source-fill schema-only rows written"),
        ("V768_11_candidate_artifacts_not_faked", candidate_artifacts_not_faked, "no claim-input artifacts fabricated"),
        ("V768_12_no_claim_rows_promoted", all_nonclaim, "all generated rows valid_for_claim=false"),
        ("V768_13_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V768_14_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V768_15_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V768_16_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    source_edges: list[dict[str, Any]],
    hamiltonian_edges: list[dict[str, Any]],
    requirement_map: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 768 - Y5 R10 Local-GR EH Or R11 Reentry After Alpha/WEP Quarantine

Start point: 767 boxed the parent matter functor/no-alpha-vertex problem. WEP/common matter safety remains useful as a private closure condition, but it is not a parent theorem and cannot be used as a hidden substitute for EH, Newtonian source normalization, PPN, R10, or local-GR recovery.

Current result: **the local-GR route re-enters through Hamiltonian PiM source-charge integrability, not through a smuggled WEP or EH axiom**. EH-only remains unsigned, R11 remains scaffold-only, and the strongest live target is now `FB554_0_HPiM_integrability_reference_bound`.

## Status

| field | value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | {summary[0]["main_result"]} |
| Hard blocker | `{summary[0]["hard_blocker"]}` |
| Next target | `{NEXT_TARGET}` |

## EH/R11 Reentry Audit

{markdown_table(audit, ["audit_id", "gate", "current_state_after_767", "imported_basis", "why_it_matters", "next_action", "valid_for_claim"])}

## R11 Source-Normalization Live Edge

{markdown_table(source_edges, ["edge_id", "object", "formula", "current_state", "missing_lock", "observable_pressure", "valid_for_claim"])}

## Hamiltonian PiM Live Edge

{markdown_table(hamiltonian_edges, ["hpi_id", "lock", "expression", "current_state", "missing_inputs", "why_first", "valid_for_claim"])}

## GR/Newton Requirement Map

{markdown_table(requirement_map, ["requirement_id", "reduction_need", "current_artifact", "missing_derivation", "downstream_tests", "claim_status", "valid_for_claim"])}

## Source-Fill Schema Only

{markdown_table(source_fill, ["fill_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "rationale", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_768", "forbidden_after_768", "next_action", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is a useful re-entry, not a win declaration. The branch is cleaner now because the WEP/alpha issue is quarantined instead of blurred into the GR proof. The price is also clear: before we talk about Newton or local GR, `H_tau` has to become a genuine fixed-reference Hamiltonian source charge. That means the next move is narrow and mathematical: prove `FB554_0=0` componentwise, or fill each component with source-backed bounds and keep the branch nonclaim until it passes.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    audit = eh_r11_reentry_audit_rows(generated_utc)
    source_edges = r11_source_normalization_live_edge_rows(generated_utc)
    hamiltonian_edges = hamiltonian_pim_live_edge_rows(generated_utc)
    requirement_map = gr_newton_requirement_map_rows(generated_utc)
    source_fill = source_fill_schema_rows(generated_utc)
    decisions = decision_matrix_rows(generated_utc)
    routes = route_update_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(sources, audit, source_edges, hamiltonian_edges, requirement_map, source_fill, decisions, routes, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(EH_R11_REENTRY_AUDIT_PATH, audit, ["audit_id", "gate", "current_state_after_767", "imported_basis", "why_it_matters", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(R11_SOURCE_NORMALIZATION_LIVE_EDGE_PATH, source_edges, ["edge_id", "object", "formula", "current_state", "missing_lock", "observable_pressure", "source_paths", "valid_for_claim", "generated_utc"])
    write_csv(HAMILTONIAN_PIM_LIVE_EDGE_PATH, hamiltonian_edges, ["hpi_id", "lock", "expression", "current_state", "missing_inputs", "why_first", "source_paths", "valid_for_claim", "generated_utc"])
    write_csv(GR_NEWTON_REQUIREMENT_MAP_PATH, requirement_map, ["requirement_id", "reduction_need", "current_artifact", "missing_derivation", "downstream_tests", "claim_status", "valid_for_claim", "generated_utc"])
    write_csv(SOURCE_FILL_SCHEMA_PATH, source_fill, ["fill_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_MATRIX_PATH, decisions, ["decision_id", "decision", "rationale", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_UPDATE_PATH, routes, ["route_id", "allowed_after_768", "forbidden_after_768", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, audit, source_edges, hamiltonian_edges, requirement_map, source_fill, decisions, routes, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"768 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()

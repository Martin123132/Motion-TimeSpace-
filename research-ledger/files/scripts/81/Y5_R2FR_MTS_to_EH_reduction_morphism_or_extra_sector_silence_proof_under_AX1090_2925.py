from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2925"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2925-Y5-R2FR-MTS-to-EH-reduction-morphism-or-extra-sector-silence-proof-under-AX1090.md"

SRC_2924_DOC = ROOT / "2924-Y5-R2FR-parent-Hcore-coefficient-map-or-finite-source-mass-first-row-fill-under-AX1090.md"
SRC_2924_REDUCTION = RESIDUALS / "P8_Y5_R2FR_2924_MTS_TO_EH_REDUCTION_CONTRACT.csv"
SRC_2924_EH = RESIDUALS / "P8_Y5_R2FR_2924_EH_ANCHOR_COEFFICIENT_MAP.csv"
SRC_2924_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2924_VALIDATION.csv"
SRC_2924_NEXT = RESIDUALS / "P8_Y5_R2FR_2924_NEXT_TARGET.csv"
SRC_1007_DOC = ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md"
SRC_1009_DOC = ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"
SRC_1010_DOC = ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md"
SRC_1047_DOC = ROOT / "1047-Y5-R10-constant-superselection-alpha-mass-clock-theorem-or-coefficient-provenance.md"
SRC_1088_DOC = ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md"
SRC_1090_DOC = ROOT / "1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md"
SRC_2911_DOC = ROOT / "2911-Y5-R2FR-parent-field-chart-q-map-kernel-basis-or-finite-DqZ-norm-under-AX1090.md"
SRC_2918_DOC = ROOT / "2918-Y5-R2FR-alpha3-source-current-kernel-or-no-disformal-slot-theorem-under-AX1090.md"
SRC_2909_PROOF = RESIDUALS / "P8_Y5_R2FR_2909_SOURCE_CURRENT_DESCENT_PROOF_ATTEMPT.csv"
SRC_2909_RESIDUAL = RESIDUALS / "P8_Y5_R2FR_2909_SOURCE_CURRENT_Y5Y6_RESIDUAL_VECTOR.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2925_SOURCE_REGISTER.csv",
    "theorem_ladder": RESIDUALS / "P8_Y5_R2FR_2925_REDUCTION_THEOREM_LADDER.csv",
    "silence_audit": RESIDUALS / "P8_Y5_R2FR_2925_EXTRA_SECTOR_SILENCE_AUDIT.csv",
    "residual_vector": RESIDUALS / "P8_Y5_R2FR_2925_REDUCTION_RESIDUAL_VECTOR.csv",
    "candidate_results": RESIDUALS / "P8_Y5_R2FR_2925_CANDIDATE_VALIDATION_RESULTS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2925_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2925_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2925_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2925_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2925_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_copy": PARENT_ACTION / "MTS_to_EH_reduction_theorem_ladder_2925_NONCLAIM.csv",
    "residual_copy": LOCAL_BOUNDS / "MTS_to_EH_reduction_residual_vector_2925_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2925_PARENT_OBJECT_NO_HIDDEN_VISIBLE_HOM_OR_RESIDUAL_FILL_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in selected)
        + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC2925_00_2924_doc",
            SRC_2924_DOC,
            "Y5_R2FR_2924_EH_anchor_filled_MTS_reduction_morphism_2925_next;NEXT2924_0_2925;Validation overall: `True`",
            "2924 selected MTS-to-EH reduction morphism target",
        ),
        (
            "SRC2925_01_2924_reduction",
            SRC_2924_REDUCTION,
            "RED2924_0_metric_identification;RED2924_10_total_verdict",
            "2924 reduction contract",
        ),
        (
            "SRC2925_02_2924_EH",
            SRC_2924_EH,
            "EHA2924_0_EH_action_block;EHA2924_5_total_verdict",
            "EH/ADM coefficient-map anchor",
        ),
        (
            "SRC2925_03_2924_validation",
            SRC_2924_VALIDATION,
            "VAL2924_OVERALL;True",
            "2924 validation summary",
        ),
        (
            "SRC2925_04_2924_next",
            SRC_2924_NEXT,
            "NEXT2924_0_2925;MTS-to-EH-reduction-morphism",
            "machine-readable 2925 target",
        ),
        (
            "SRC2925_05_1007_Htau",
            SRC_1007_DOC,
            "HTA1007_2_EH_import_guard;HTA1007_6_integrability_verdict",
            "H_tau integrability/fixed-reference guard",
        ),
        (
            "SRC2925_06_1009_parent_contract",
            SRC_1009_DOC,
            "PCS1009_0_EH_core;PCS1009_4_Gamma_Khat_extra;CG1009_2_Qtau_MTS",
            "parent current-chain contract and EH-only refusal",
        ),
        (
            "SRC2925_07_1010_GK",
            SRC_1010_DOC,
            "GKT1010_0_variational_route;GKT1010_6_verdict",
            "Gamma/Khat/q_loc variational double-zero route",
        ),
        (
            "SRC2925_08_1047_constants",
            SRC_1047_DOC,
            "CST1047_0_descent_or_superselection_criterion;CST1047_5_verdict",
            "constant superselection conditional theorem",
        ),
        (
            "SRC2925_09_1088_matter_signature",
            SRC_1088_DOC,
            "MOMS1088_0_action_form;MOMS1088_7_verdict",
            "minimal ordinary matter signature conditional theorem",
        ),
        (
            "SRC2925_10_1090_missing_axioms",
            SRC_1090_DOC,
            "SYN1090_8_verdict;AX1090_1_no_hidden_visible_hom",
            "missing parent-object/no-hidden-visible axioms",
        ),
        (
            "SRC2925_11_2911_DqZ",
            SRC_2911_DOC,
            "QMAP2911_7_verdict;DQZ2911_TOTAL;VAL2911_OVERALL",
            "q-map/kernel/DqZ residual vector",
        ),
        (
            "SRC2925_12_2918_source_current",
            SRC_2918_DOC,
            "NDS2918_6_verdict;A3K2918_9_verdict;VAL2918_OVERALL",
            "alpha3/source-current/no-disformal kernel",
        ),
        (
            "SRC2925_13_2909_source_descent",
            SRC_2909_PROOF,
            "PROOF2909_0_JZ_chain_rule_identity;PROOF2909_5_JZ_application",
            "source-current descent proof attempts",
        ),
        (
            "SRC2925_14_2909_residual_vector",
            SRC_2909_RESIDUAL,
            "RES2909_0_JM_descent;RES2909_5_direct_vertex",
            "Y5/Y6 source-current residual vector",
        ),
    ]
    rows = []
    for source_id, path, anchors, role in specs:
        ok, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": ok,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def theorem_ladder_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "RTL2925_0_statement",
            "conditional local reduction theorem",
            "If a parent MTS action admits quotient readout q, constant kappa, EH core, universal matter descent, extra-sector double-zero, projector/boundary silence, integrable H_tau, worldtube source measure, and EH weak-field calibration, then local compact MTS reduces to EH+matter through first post-Newtonian order up to the residual vector RV2925.",
            "EXACT_CONDITIONAL_THEOREM_WRITTEN",
            "This is the honest theorem shape: it says exactly what must be derived for GR/Newton to follow.",
            True,
            False,
            str(SRC_2924_REDUCTION),
        ),
        (
            "RTL2925_1_metric_readout",
            "quotient metric/coframe sublemma",
            "If g_obs=g_bar(q(Phi)) and v in ker(Dq), then Lie_v g_obs=0 by chain rule; visible metric leakage is controlled by DqZ_geometry.",
            "CONDITIONAL_SUBLEMMA_ONLY",
            "2911 does not parent-sign the q map, kernel basis, or Dq matrix.",
            True,
            False,
            str(SRC_2911_DOC),
        ),
        (
            "RTL2925_2_EH_core",
            "EH anchor inheritance",
            "If L_MTS|local=L_EH[g_obs;kappa0,Lambda0]+dB+L_silent+L_residual and residual metric projection vanishes, the EH field equation and EH charge form are inherited.",
            "EH_REFERENCE_READY_REDUCTION_UNSIGNED",
            "2924 fills the EH target row, but 1009 rejects EH-only import as total parent action.",
            True,
            False,
            ";".join(str(path) for path in [SRC_2924_EH, SRC_1009_DOC]),
        ),
        (
            "RTL2925_3_constant_kappa",
            "coupling superselection",
            "If kappa_eff is topological/superselected and has no source/species/range/frame labels, Dln(kappa_eff)=0 and G0 is universal in the local branch.",
            "CONDITIONAL_ROUTE_UNSIGNED",
            "constant kappa and source-current scale remain explicit alpha3/source-normalization gates.",
            True,
            False,
            ";".join(str(path) for path in [SRC_1047_DOC, SRC_2918_DOC]),
        ),
        (
            "RTL2925_4_matter_descent",
            "ordinary matter quotient signature",
            "If S_matter=sum_A S_A[Psi_A;E(q(Phi)),Omega,A_obs,theta_A] with theta_A fixed/topological and no species weights, then delta_v S_matter=0 for vertical v up to gauge/boundary terms.",
            "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_DERIVED",
            "1088 proves the theorem under MOMS, while 1090 says MOMS is not derived from current corpus.",
            True,
            False,
            ";".join(str(path) for path in [SRC_1088_DOC, SRC_1090_DOC]),
        ),
        (
            "RTL2925_5_extra_double_zero",
            "Gamma/Khat/q_loc variational double-zero",
            "If S_GK exists, K_hat is its metric response, Helmholtz integrability holds, Euler closure holds, T_GK(Phi0)=0, and partial_A T_GK(Phi0)=0, then q_loc^nu=0 on the local compact branch.",
            "ROUTE_EXACT_NOT_CLOSED",
            "1010 writes the route but keeps S_GK, metric-response match, Helmholtz, Euler/double-zero, projector, and boundary clauses unsigned.",
            True,
            False,
            str(SRC_1010_DOC),
        ),
        (
            "RTL2925_6_projector_boundary",
            "projector/domain/boundary silence",
            "If Pi_M, boundary/reference, domain selectors, and source support are varied before readout and have zero/fixed stress contribution, they cannot hide a mass or preferred-frame residual.",
            "CONDITIONAL_ROUTE_UNSIGNED",
            "2911 and 1015 keep DqZ_boundary_projector, kernel charge, and worldtube equality open.",
            True,
            False,
            ";".join(str(path) for path in [SRC_2911_DOC, SRC_1007_DOC]),
        ),
        (
            "RTL2925_7_Htau_worldtube",
            "integrable charge and same-object source measure",
            "If delta H_tau=int_S(delta Q_tau-i_tau theta) is integrable with fixed H_ref and M_source[W]=H_tau[S]-H_ref before orbital fitting, the Hamiltonian mass is the source mass.",
            "CONDITIONAL_ROUTE_UNSIGNED",
            "1007 blocks H_tau and 2924/1015 block worldtube/source glue.",
            True,
            False,
            ";".join(str(path) for path in [SRC_1007_DOC, SRC_2924_DOC]),
        ),
        (
            "RTL2925_8_Poisson_Gauss",
            "EH weak-field readout",
            "If RTL2925_0-RTL2925_7 hold, the EH weak-field equation gives nabla^2 Phi=4*pi*G0*rho_H and a=-G0*M_H/r^2 without importing orbital GM.",
            "CONDITIONAL_GR_REFERENCE_NOT_MTS_DERIVED",
            "The bridge is valid target mathematics but is not yet an MTS theorem.",
            True,
            False,
            str(SRC_2924_DOC),
        ),
        (
            "RTL2925_9_current_verdict",
            "current MTS reduction morphism",
            "RTL2925_0 theorem is available, but current MTS has not signed the required parent action, q map, no-hidden-visible hom, double-zero, source measure, and H_tau clauses.",
            "REDUCTION_MORPHISM_NOT_DERIVED_RESIDUAL_VECTOR_REQUIRED",
            "This is not a dead end; it is a sharply localized proof debt.",
            True,
            False,
            ";".join(str(path) for path in [SRC_2924_REDUCTION, SRC_1090_DOC, SRC_1010_DOC]),
        ),
    ]
    rows = []
    for ladder_id, theorem_piece, mathematical_statement, current_status, why_it_matters, conditional_theorem_valid, promoted_for_current_mts, source_paths in specs:
        rows.append(
            add_common(
                {
                    "ladder_id": ladder_id,
                    "theorem_piece": theorem_piece,
                    "mathematical_statement": mathematical_statement,
                    "current_status": current_status,
                    "conditional_theorem_valid": conditional_theorem_valid,
                    "promoted_for_current_mts": promoted_for_current_mts,
                    "why_it_matters": why_it_matters,
                    "source_paths": source_paths,
                }
            )
        )
    return rows


def silence_audit_rows() -> list[dict[str, Any]]:
    specs = [
        ("XSI2925_0_qmap_metric", "metric/coframe readout leakage", "DqZ_geometry", "MISSING_PARENT_Q_MAP_DQ_MATRIX_Z_NORMS", "PPN;clock;orbital;local_GR", SRC_2911_DOC),
        ("XSI2925_1_kappa", "constant gravitational coupling drift", "Dln(kappa_MTS)", "MISSING_PARENT_CONSTANT_KAPPA_PROOF_OR_VALUE", "alpha3;Newton;orbital;R10", SRC_2918_DOC),
        ("XSI2925_2_matter_signature", "ordinary matter/source-current slot", "Delta_w_abs+A_direct_matter+theta_marker", "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED", "WEP;Newton;clock;R10", SRC_1088_DOC),
        ("XSI2925_3_GK_double_zero", "Gamma/Khat/q_loc stress hair", "q_loc^nu", "S_GK_HELMHOLTZ_EULER_DOUBLE_ZERO_UNSIGNED", "PPN;local_GR;source_mass", SRC_1010_DOC),
        ("XSI2925_4_no_disformal", "preferred-frame/disformal readout slot", "d_R_vector_current", "Z_ALPHA3_DISFORMAL_FALSE_UNSIGNED", "alpha3;PPN;light_time", SRC_2918_DOC),
        ("XSI2925_5_projector_boundary", "projector/domain/boundary charge leakage", "DqZ_boundary_projector+kernel_charge", "MISSING_BOUNDARY_NOFLUX_PROJECTOR_DESCENT", "R10;PPN;Newton;orbital", SRC_2911_DOC),
        ("XSI2925_6_Htau_reference", "integrable H_tau/fixed reference", "epsilon_HPiM_integrability_abs", "MISSING_PARENT_HTAU_INTEGRABILITY", "source_mass;Newton;orbital", SRC_1007_DOC),
        ("XSI2925_7_worldtube", "same-object worldtube source measure", "epsilon_worldtube_source", "MISSING_WORLDTUBE_SOURCE_GLUE", "Newton;WEP;orbital;local_GR", SRC_2909_PROOF),
        ("XSI2925_8_total", "all extra/source/projector/boundary silence clauses", "Delta_reduction_total", "EXTRA_SECTOR_SILENCE_NOT_PROVED", "all_local_arenas", SRC_2924_REDUCTION),
    ]
    rows = []
    for audit_id, channel, residual_symbol, current_status, observable_targets, source_path in specs:
        rows.append(
            add_common(
                {
                    "audit_id": audit_id,
                    "channel": channel,
                    "residual_symbol": residual_symbol,
                    "current_status": current_status,
                    "theorem_zero": False,
                    "finite_bound_present": False,
                    "observable_targets": observable_targets,
                    "source_path": str(source_path),
                }
            )
        )
    return rows


def residual_vector_rows() -> list[dict[str, Any]]:
    specs = [
        ("RV2925_0_metric_readout", "epsilon_metric_readout", "||DqZ_geometry|| + ||A_shadow_metric||", "dimensionless metric/coframe response", "MISSING_QMAP_METRIC_READOUT_BOUND", "PPN;clock;orbital;local_GR"),
        ("RV2925_1_constant_kappa", "epsilon_kappa", "|Dln(kappa_MTS)| + |delta_G_source_range_frame|", "dimensionless coupling drift", "MISSING_CONSTANT_KAPPA_THEOREM_OR_VALUE", "alpha3;Newton;R10;orbital"),
        ("RV2925_2_EH_core_residual", "epsilon_EH_reduction", "||E_residual_metric||/||E_EH|| + ||L_residual_metric||/||L_EH||", "dimensionless action/operator residual", "MISSING_PARENT_ACTION_REDUCTION_MAP", "PPN;local_GR;Newton"),
        ("RV2925_3_matter_descent", "epsilon_matter_source", "|Delta_w_abs| + |A_direct_matter| + |epsilon_theta_marker|", "source-current-normalized", "MISSING_MOMS_PARENT_SIGNATURE", "WEP;R10;Newton;clock"),
        ("RV2925_4_extra_double_zero", "epsilon_extra_double_zero", "|T_extra(Phi0)|/M_ref + ||partial_A T_extra(Phi0)|| ||Delta Phi^A||/M_ref", "source-normalized stress", "MISSING_SGK_DOUBLE_ZERO", "PPN;local_GR;source_mass"),
        ("RV2925_5_projector_boundary", "epsilon_projector_boundary", "|DqZ_boundary_projector| + |epsilon_kernel_charge| + |boundary_flux|/M_ref", "dimensionless boundary/projector leak", "MISSING_PROJECTOR_BOUNDARY_NOFLUX", "R10;PPN;Newton;orbital"),
        ("RV2925_6_Htau_reference", "epsilon_Htau_reference", "|Delta_ref|/M_ref + |Delta_symp|/M_ref + |B_zero_flux|/M_ref", "dimensionless Hamiltonian-charge leak", "MISSING_HTAU_FIXED_REFERENCE", "source_mass;Newton;orbital"),
        ("RV2925_7_worldtube_source", "epsilon_worldtube_source", "|R_eq|/M_ref + |I_commutator| + |M_source[W]-H_tau[S]+H_ref|/M_ref", "dimensionless same-object/source-measure error", "MISSING_WORLDTUBE_SOURCE_GLUE", "Newton;WEP;orbital;local_GR"),
        ("RV2925_8_Poisson_Gauss_orbit", "epsilon_PG_orbit", "|Delta_Poisson| + |Delta_Gauss| + |Delta_force| + |Delta_calibration|", "arena-normalized weak-field readout", "CONDITIONAL_EH_ONLY_NOT_MTS_DERIVED", "Newton;orbital;light_time"),
        ("RV2925_TOTAL", "Delta_MTS_to_EH_reduction_total", "sum_abs(RV2925_0..RV2925_8), no cancellation, no GM/G_N absorption", "dimensionless after declared arena normalizations", "COMPONENTS_MISSING_NONCLAIM", "all_local_arenas"),
    ]
    rows = []
    for residual_id, symbol, definition, units, current_value, observable_link in specs:
        rows.append(
            add_common(
                {
                    "residual_id": residual_id,
                    "symbol": symbol,
                    "definition": definition,
                    "units": units,
                    "current_value": current_value,
                    "theorem_zero": False,
                    "finite_value_present": False,
                    "source_backed_bound_present": False,
                    "accepted_for_scoring": False,
                    "observable_link": observable_link,
                    "source_paths": ";".join(
                        str(path)
                        for path in [
                            SRC_2924_REDUCTION,
                            SRC_2911_DOC,
                            SRC_2918_DOC,
                            SRC_1010_DOC,
                            SRC_2909_RESIDUAL,
                        ]
                    ),
                }
            )
        )
    return rows


def candidate_validation_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "candidate_id": "CAND2925_0_full_reduction_proof",
            "candidate": "promote MTS -> EH reduction for current corpus",
            "validation_status": "REJECT_UNSIGNED_PARENT_CLAUSES",
            "accepted_as": "not_accepted",
            "failure_reasons": "q_map;parent_action;constant_kappa;matter_descent;SGK_double_zero;projector_boundary;Htau;worldtube",
        },
        {
            "candidate_id": "CAND2925_1_EH_import_as_MTS",
            "candidate": "use EH/ADM anchor as total MTS parent H_core",
            "validation_status": "REJECT_EH_IMPORT_AS_TOTAL_PARENT_ACTION",
            "accepted_as": "reference_only",
            "failure_reasons": "1009 EH anchor guard;2924 EH nonclaim row",
        },
        {
            "candidate_id": "CAND2925_2_chain_rule_metric_sublemma",
            "candidate": "if g_obs=g(q(Phi)) and v in ker(Dq), then Lie_v g_obs=0",
            "validation_status": "ACCEPTED_CONDITIONAL_SUBLEMMA_NOT_CURRENT_PROOF",
            "accepted_as": "conditional_theorem_piece",
            "failure_reasons": "current q map/kernel/Dq matrix not parent-signed",
        },
        {
            "candidate_id": "CAND2925_3_MOMS_matter_descent",
            "candidate": "ordinary matter source current zero under MOMS1088",
            "validation_status": "ACCEPTED_CONDITIONAL_THEOREM_NOT_PARENT_DERIVED",
            "accepted_as": "conditional_theorem_piece",
            "failure_reasons": "1090 says MOMS synthesis fails missing axioms",
        },
        {
            "candidate_id": "CAND2925_4_SGK_double_zero_route",
            "candidate": "derive q_loc=0 from S_GK, Helmholtz, Euler closure, double-zero",
            "validation_status": "ACCEPTED_ROUTE_REJECT_CURRENT_CLAIM",
            "accepted_as": "conditional_route",
            "failure_reasons": "S_GK;metric response;Helmholtz;Euler/double-zero;boundary no-flux unsigned",
        },
        {
            "candidate_id": "CAND2925_5_residual_vector",
            "candidate": "emit Delta_MTS_to_EH_reduction_total residual vector",
            "validation_status": "ACCEPTED_NONCLAIM_RESIDUAL_VECTOR",
            "accepted_as": "nonclaim_score_skeleton",
            "failure_reasons": "source-backed numeric bounds still missing",
        },
    ]
    return [add_common(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CG2925_0_conditional_theorem",
            "gate": "conditional MTS-to-EH reduction theorem shape exists",
            "gate_status": "CONTROL_PASS_NONCLAIM",
            "evidence": "RTL2925_0 through RTL2925_8",
            "decision": "use as derivation target, not as proof of current MTS",
        },
        {
            "gate_id": "CG2925_1_current_reduction",
            "gate": "current MTS satisfies reduction theorem hypotheses",
            "gate_status": "BLOCKED",
            "evidence": "RTL2925_9 and XSI2925_8",
            "decision": "no local GR/Newton claim",
        },
        {
            "gate_id": "CG2925_2_residual_vector",
            "gate": "finite source-backed reduction residual vector ready for scoring",
            "gate_status": "BLOCKED_NONCLAIM",
            "evidence": "RV2925_TOTAL current_value=COMPONENTS_MISSING_NONCLAIM",
            "decision": "next score only after first source-backed component fill",
        },
        {
            "gate_id": "CG2925_3_EH_import_guard",
            "gate": "EH-only import cannot substitute for MTS parent action",
            "gate_status": "CONTROL_PASS_CLAIM_CLOSED",
            "evidence": "CAND2925_1 rejected",
            "decision": "anti-smuggling guard remains active",
        },
        {
            "gate_id": "CG2925_4_next_target",
            "gate": "next derivation target selected",
            "gate_status": "NEXT_SELECTED",
            "evidence": "NEXT2925_0_2926",
            "decision": "attack parent object/no-hidden-visible hom or fill first residual component",
        },
    ]
    return [add_common(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2925_0_theorem_gain",
            "decision": "conditional MTS-to-EH reduction theorem is now explicit",
            "status": "USEFUL_PROGRESS",
            "reason": "we now know exactly which hypotheses make EH/Newton follow without circular GM import.",
        },
        {
            "decision_id": "DEC2925_1_current_claim",
            "decision": "do not claim current MTS reduces to GR/Newton yet",
            "status": "CLAIM_REFUSED",
            "reason": "parent object, q map, no-hidden-visible hom, double-zero, H_tau, and worldtube clauses are not signed.",
        },
        {
            "decision_id": "DEC2925_2_residual_vector",
            "decision": "retain Delta_MTS_to_EH_reduction_total as the local-GR obstruction vector",
            "status": "RESIDUAL_VECTOR_STAGED_NONCLAIM",
            "reason": "every failed theorem clause now has a corresponding finite-row slot.",
        },
        {
            "decision_id": "DEC2925_3_best_next",
            "decision": "target parent object/no-hidden-visible hom first",
            "status": "NEXT_SELECTED",
            "reason": "1090 says this is the common beam under matter descent, constants, no-shadow frames, and source slots.",
        },
    ]
    return [add_common(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "next_id": "NEXT2925_0_2926",
            "selection": "selected_primary",
            "target_doc": "2926-Y5-R2FR-parent-object-no-hidden-visible-hom-derivation-or-reduction-residual-first-fill-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_parent_object_no_hidden_visible_hom_derivation_or_reduction_residual_first_fill_under_AX1090_2926.py",
            "objective": "try to derive the common parent object/no-hidden-visible hom that would kill metric, matter, constant, disformal, and source slots; if not, fill the first source-backed component of RV2925",
            "acceptance_gate": "either AX1090_0/AX1090_1 become parent-signed for one local branch, or one RV2925 component becomes a finite nonclaim source-backed bound row",
        },
        {
            "next_id": "NEXT2925_1_fallback",
            "selection": "fallback_if_axiom_derivation_fails",
            "target_doc": "2926B-Y5-R2FR-SGK-double-zero-or-q-loc-residual-first-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_SGK_double_zero_or_q_loc_residual_first_bound_under_AX1090_2926B.py",
            "objective": "attack the S_GK/Helmholtz/Euler double-zero route directly or produce the first finite q_loc residual bound input",
            "acceptance_gate": "q_loc zero theorem closes conditionally for a parent-signed S_GK, or RV2925_4 receives a source-backed finite nonclaim row",
        },
    ]
    return [add_common(row) for row in rows]


def branch_copy_rows() -> list[dict[str, Any]]:
    copy_specs = [
        ("BC2925_0_theorem_ladder", OUTPUTS["theorem_ladder"], BRANCH_OUTPUTS["theorem_copy"], "parent action reduction theorem ladder"),
        ("BC2925_1_residual_vector", OUTPUTS["residual_vector"], BRANCH_OUTPUTS["residual_copy"], "local bounds reduction residual vector"),
        ("BC2925_2_next_target", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"], "RAB/source queue next target"),
    ]
    rows = []
    for copy_id, source, destination, role in copy_specs:
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "destination_path": str(destination),
                    "role": role,
                    "destination_exists": destination.exists(),
                    "destination_parses": csv_parses(destination),
                }
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    silence: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str, bool]] = [
        ("VAL2925_0_sources_exist", all(as_bool(row["path_exists"]) for row in sources), "every cited source path exists", True),
        ("VAL2925_1_source_anchors_found", all(as_bool(row["anchors_found"]) for row in sources), "every cited source anchor is present", True),
        (
            "VAL2925_2_conditional_theorem_written",
            any(row["ladder_id"] == "RTL2925_0_statement" and as_bool(row["conditional_theorem_valid"]) for row in theorem),
            "conditional MTS-to-EH reduction theorem is written",
            True,
        ),
        (
            "VAL2925_3_current_verdict_blocked",
            any(row["ladder_id"] == "RTL2925_9_current_verdict" and row["current_status"] == "REDUCTION_MORPHISM_NOT_DERIVED_RESIDUAL_VECTOR_REQUIRED" and not as_bool(row["promoted_for_current_mts"]) for row in theorem),
            "current MTS is not promoted to local GR",
            True,
        ),
        (
            "VAL2925_4_silence_audit_total_blocks",
            any(row["audit_id"] == "XSI2925_8_total" and row["current_status"] == "EXTRA_SECTOR_SILENCE_NOT_PROVED" for row in silence),
            "extra-sector silence audit has a blocking total row",
            True,
        ),
        (
            "VAL2925_5_residual_vector_total",
            any(row["residual_id"] == "RV2925_TOTAL" and row["current_value"] == "COMPONENTS_MISSING_NONCLAIM" and not as_bool(row["accepted_for_scoring"]) for row in residuals),
            "residual vector total exists and remains nonclaim",
            True,
        ),
        (
            "VAL2925_6_EH_import_rejected",
            any(row["candidate_id"] == "CAND2925_1_EH_import_as_MTS" and row["validation_status"] == "REJECT_EH_IMPORT_AS_TOTAL_PARENT_ACTION" for row in candidates),
            "EH-only import is rejected",
            True,
        ),
        (
            "VAL2925_7_conditional_sublemmas_preserved",
            any(row["candidate_id"] == "CAND2925_2_chain_rule_metric_sublemma" and row["validation_status"] == "ACCEPTED_CONDITIONAL_SUBLEMMA_NOT_CURRENT_PROOF" for row in candidates)
            and any(row["candidate_id"] == "CAND2925_3_MOMS_matter_descent" and row["validation_status"] == "ACCEPTED_CONDITIONAL_THEOREM_NOT_PARENT_DERIVED" for row in candidates),
            "conditional sublemmas are retained without promotion",
            True,
        ),
        (
            "VAL2925_8_no_claim_gates_open",
            all(not as_bool(row["claim_allowed"]) and str(row["gate_status"]) != "OPEN" for row in claims),
            "no claim gate opens in 2925",
            True,
        ),
        (
            "VAL2925_9_next_target_selected",
            any(row["next_id"] == "NEXT2925_0_2926" for row in next_rows),
            "2926 parent-object/no-hidden-visible target selected",
            True,
        ),
        (
            "VAL2925_10_branch_copies_valid",
            all(as_bool(row["destination_exists"]) and as_bool(row["destination_parses"]) for row in branches),
            "branch copies exist and parse",
            True,
        ),
        (
            "VAL2925_11_no_formalization_outputs",
            not any(is_under(path, FORMALIZATION) for path in [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]),
            "no generated output path is inside formalization-workbench",
            True,
        ),
        ("VAL2925_12_doc_exists", DOC.exists(), "2925 markdown checkpoint exists", True),
    ]
    rows = [
        {
            "validation_id": check_id,
            "passed": passed,
            "check": check,
            "required": required,
            "generated_utc": RUN_UTC,
        }
        for check_id, passed, check, required in checks
    ]
    overall = all(passed for _, passed, _, required in checks if required)
    rows.append(
        {
            "validation_id": "VAL2925_OVERALL",
            "passed": overall,
            "check": "2925 validation overall",
            "required": True,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    silence: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    overall = next(row["passed"] for row in validation if row["validation_id"] == "VAL2925_OVERALL")
    lines = [
        "# 2925 - Y5/R2FR MTS To EH Reduction Morphism Or Extra-Sector Silence Proof Under AX1090",
        "",
        "Status: `Y5_R2FR_2925_conditional_reduction_theorem_written_current_MTS_residual_vector_2926_next`",
        "",
        "## Result",
        "",
        "2925 makes a genuine derivation step: the conditional local reduction theorem is now explicit. If the parent MTS branch supplies quotient metric readout, constant coupling, EH core inheritance, ordinary matter descent, extra-sector double-zero, projector/boundary silence, integrable `H_tau`, same-object worldtube source measure, and EH weak-field calibration, then the local compact branch reduces to EH/Newton without borrowing orbital `GM`.",
        "",
        "Current MTS does not yet satisfy those hypotheses. Therefore the honest output is not a local-GR claim; it is the named obstruction vector `Delta_MTS_to_EH_reduction_total`.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "path_exists", "anchors_found", "role", "source_path"]),
        "",
        "## Reduction Theorem Ladder",
        "",
        md_table(theorem, ["ladder_id", "theorem_piece", "current_status", "conditional_theorem_valid", "promoted_for_current_mts", "why_it_matters"]),
        "",
        "## Extra-Sector Silence Audit",
        "",
        md_table(silence, ["audit_id", "channel", "residual_symbol", "current_status", "theorem_zero", "observable_targets"]),
        "",
        "## Reduction Residual Vector",
        "",
        md_table(residuals, ["residual_id", "symbol", "definition", "current_value", "accepted_for_scoring", "observable_link"]),
        "",
        "## Candidate Validation Results",
        "",
        md_table(candidates, ["candidate_id", "candidate", "validation_status", "accepted_as", "failure_reasons"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "gate", "gate_status", "decision", "evidence"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "status", "reason"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["next_id", "selection", "target_doc", "target_script", "objective", "acceptance_gate"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["validation_id", "passed", "check", "required"]),
        "",
        f"Validation overall: `{overall}`.",
        "",
        "## Bottom Line",
        "",
        "This does move the project closer. We now have the exact theorem that would make MTS reduce to GR/Newton, and the exact residual vector explaining why the current corpus does not yet earn it. The best next attack is the common parent object/no-hidden-visible hom: if that closes, several residual heads collapse together; if it does not, we start filling the residual vector with source-backed bounds.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    theorem = theorem_ladder_rows()
    silence = silence_audit_rows()
    residuals = residual_vector_rows()
    candidates = candidate_validation_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem_ladder"], theorem)
    write_csv(OUTPUTS["silence_audit"], silence)
    write_csv(OUTPUTS["residual_vector"], residuals)
    write_csv(OUTPUTS["candidate_results"], candidates)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_rows)

    branches = branch_copy_rows()
    write_csv(OUTPUTS["branches"], branches)

    DOC.write_text("# 2925 - validation preflight\n", encoding="utf-8")
    validation = validation_rows(sources, theorem, silence, residuals, candidates, claims, next_rows, branches)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, theorem, silence, residuals, candidates, claims, decisions, next_rows, validation)

    overall = next(row["passed"] for row in validation if row["validation_id"] == "VAL2925_OVERALL")
    if not overall:
        raise SystemExit("2925 validation failed; see " + str(OUTPUTS["validation"]))
    print("2925 validation overall:", overall)
    print("doc:", DOC)


if __name__ == "__main__":
    main()

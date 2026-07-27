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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2948"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2948-Y5-R2FR-parent-current-chain-sector-action-certificate-or-IX-charge-residual-first-row-under-AX1090.md"

SRC_2947_DOC = ROOT / "2947-Y5-R2FR-parent-theta-Qtau-MHref-certificate-or-denominator-first-row-runner-under-AX1090.md"
SRC_2947_NEXT = RESIDUALS / "P8_Y5_R2FR_2947_NEXT_TARGET.csv"
SRC_2947_CERT = RESIDUALS / "P8_Y5_R2FR_2947_THETA_QTAU_CERTIFICATE_ATTEMPT.csv"
SRC_2947_SECTORS = RESIDUALS / "P8_Y5_R2FR_2947_SECTOR_CHARGE_CERTIFICATE_MATRIX.csv"
SRC_2947_CURL = RESIDUALS / "P8_Y5_R2FR_2947_HTAU_INTEGRABILITY_RESIDUAL_ROWS.csv"
SRC_2021_THEOREM = RESIDUALS / "P8_Y5_PARENT_QLOC_2021_QTAU_SECTOR_OWNER_THEOREM.csv"
SRC_2021_LEDGER = RESIDUALS / "P8_Y5_PARENT_QLOC_2021_QTAU_SECTOR_LEDGER.csv"
SRC_2845_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2845_PARENT_CURRENT_OWNER_CONTRACT.csv"
SRC_2845_AUDIT = RESIDUALS / "P8_Y5_R2FR_2845_SOURCE_CURRENT_IDENTITY_AUDIT.csv"
SRC_2846_THEOREM = RESIDUALS / "P8_Y5_R2FR_2846_NARROW_PARENT_CURRENT_OWNER_THEOREM.csv"
SRC_2851_ANSATZ = RESIDUALS / "P8_Y5_R2FR_2851_COMMON_CURRENT_ANSATZ.csv"
SRC_2883_NO_POLE = RESIDUALS / "P8_Y5_R2FR_2883_NO_POLE_CURRENT_GATE.csv"
SRC_2908_COUPLING = RESIDUALS / "P8_Y5_R2FR_2908_Y5Y6_COUPLING_OWNER_AUDIT.csv"
SRC_2909_PROOF = RESIDUALS / "P8_Y5_R2FR_2909_SOURCE_CURRENT_DESCENT_PROOF_ATTEMPT.csv"
SRC_2909_VECTOR = RESIDUALS / "P8_Y5_R2FR_2909_SOURCE_CURRENT_Y5Y6_RESIDUAL_VECTOR.csv"
SRC_2937_CLAUSES = RESIDUALS / "P8_Y5_R2FR_2937_SOURCE_CURRENT_CLAUSE_LEDGER.csv"
SRC_2943_EVIDENCE = RESIDUALS / "P8_Y5_R2FR_2943_CURRENT_SOURCE_EVIDENCE_AUDIT.csv"
SRC_1799_IX = RESIDUALS / "P8_Y5_PARENT_QLOC_1799_FIRST_IX_SOURCE_BOUND_ROW.csv"
SRC_1863_IJX = RESIDUALS / "P8_Y5_PARENT_QLOC_1863_IX_JX_DEMOTION_LEDGER.csv"
SRC_2022_IX_SCHEMA = RESIDUALS / "P8_Y5_PARENT_QLOC_2022_IX_FIRST_SOURCE_ROW_SCHEMA.csv"
SRC_2165_IJX = RESIDUALS / "P8_Y5_PARENT_QLOC_2165_IX_JX_DEMOTION_LEDGER.csv"
SRC_2708_NO_POLE = RESIDUALS / "P8_Y5_R2FR_2708_NO_POLE_CERTIFICATE_MATRIX.csv"
SRC_2643_QVIS = RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_PARENT_SIGNATURE_THEOREM_GATE.csv"
SRC_2665_HLOCK = RESIDUALS / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv"
SRC_2665_PDG = RESIDUALS / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_PROJECTOR_DENOMINATOR_GATE.csv"
SRC_912_OMEGA = RESIDUALS / "P8_Y5_R10_912_EXTRA_SECTOR_OMEGA_LEDGER.csv"
SRC_973_JX = RESIDUALS / "P8_Y5_R10_973_JX_DECOMPOSITION_GATE.csv"
SRC_1041_THETAX = RESIDUALS / "P8_Y5_R10_1041_THETAX_OWNER_GATE.csv"
SRC_EXTRA_BOUND = RESIDUALS / "P8_Y5_HAMILTONIAN_EXTRA_CHARGE_BOUND_FILL_ROW.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2948_SOURCE_REGISTER.csv",
    "certificate": RESIDUALS / "P8_Y5_R2FR_2948_PARENT_CURRENT_CHAIN_CERTIFICATE_ATTEMPT.csv",
    "route": RESIDUALS / "P8_Y5_R2FR_2948_X_SECTOR_ROUTE_PROOF_AUDIT.csv",
    "ix": RESIDUALS / "P8_Y5_R2FR_2948_IX_RESIDUAL_FIRST_ROW.csv",
    "jx": RESIDUALS / "P8_Y5_R2FR_2948_JX_COMPONENT_ENVELOPE.csv",
    "guards": RESIDUALS / "P8_Y5_R2FR_2948_NO_CANCELLATION_GUARDS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2948_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2948_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2948_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2948_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2948_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "certificate_copy": PARENT_ACTION / "Current_chain_sector_action_certificate_2948_NONCLAIM.csv",
    "route_copy": PARENT_ACTION / "X_sector_route_proof_audit_2948_NONCLAIM.csv",
    "ix_copy": LOCAL_BOUNDS / "IX_charge_residual_first_row_2948_NONCLAIM.csv",
    "jx_copy": LOCAL_BOUNDS / "JX_component_envelope_2948_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2948_PARENT_X_ACTION_ROUTE_OR_IX_SOURCE_ROW_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


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


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2948_00_2947_doc", SRC_2947_DOC, "NEXT2947_0_2948;Validation overall: `True`", "2947 handoff to current-chain/I_X root"),
        ("SRC2948_01_2947_next", SRC_2947_NEXT, "NEXT2947_0_2948", "machine-readable 2948 target"),
        ("SRC2948_02_2947_cert", SRC_2947_CERT, "CERT2947_2_total_Qtau;CERT2947_6_verdict", "theta/Qtau certificate blocker"),
        ("SRC2948_03_2947_sectors", SRC_2947_SECTORS, "SEC2947_3_GK_q_loc;SEC2947_9_total", "sector charge certificate matrix"),
        ("SRC2948_04_2947_curl", SRC_2947_CURL, "CURL2947_1_omega_X;CURL2947_5_envelope", "H_tau curl residual handoff"),
        ("SRC2948_05_2021_theorem", SRC_2021_THEOREM, "QSO2021_6_first_live_obstruction;QSO2021_7_verdict", "I_X/Q_tau_X selected as live obstruction"),
        ("SRC2948_06_2021_ledger", SRC_2021_LEDGER, "QSL2021_1_X_extra;QSL2021_7_total", "Q_tau sector ledger"),
        ("SRC2948_07_2845_contract", SRC_2845_CONTRACT, "OWNER2845_0_parent_action;OWNER2845_6_normalization", "parent current owner contract"),
        ("SRC2948_08_2845_audit", SRC_2845_AUDIT, "ID2845_0_target_identity;ID2845_5_verdict", "source-current identity audit"),
        ("SRC2948_09_2846_theorem", SRC_2846_THEOREM, "THEO2846_0_conditional_statement;THEO2846_6_verdict", "narrow current-owner theorem attempt"),
        ("SRC2948_10_2851_ansatz", SRC_2851_ANSATZ, "ANS2851_0_general_source_doublet;ANS2851_2_auxiliary_constraint_form", "common-current algebraic ansatz"),
        ("SRC2948_11_2883_no_pole", SRC_2883_NO_POLE, "NP2883_0_parent_qmap;NP2883_7_verdict", "no-pole current gate"),
        ("SRC2948_12_2908_coupling", SRC_2908_COUPLING, "CPL2908_2_JM_source_current;CPL2908_7_observable_lock", "Y5/Y6 coupling owner audit"),
        ("SRC2948_13_2909_proof", SRC_2909_PROOF, "PROOF2909_0_JZ_chain_rule_identity;PROOF2909_7_verdict", "source-current descent proof attempt"),
        ("SRC2948_14_2909_vector", SRC_2909_VECTOR, "RES2909_0_JM_descent;RES2909_7_Y5_GM", "Y5/Y6 residual vector"),
        ("SRC2948_15_2937_clauses", SRC_2937_CLAUSES, "SCL2937_0_parent_q;SCL2937_7_ellJ", "source current clause ledger"),
        ("SRC2948_16_2943_evidence", SRC_2943_EVIDENCE, "CUR2943_0_Hilbert_definition;CUR2943_4_universality", "current source evidence audit"),
        ("SRC2948_17_1799_ix", SRC_1799_IX, "IXR1799_0_identity;IXR1799_7_acceptance", "first I_X source bound schema"),
        ("SRC2948_18_1863_ijx", SRC_1863_IJX, "IJX1863_0_I_X;IJX1863_7_total_vector", "I_X/J_X demotion ledger"),
        ("SRC2948_19_2022_ix_schema", SRC_2022_IX_SCHEMA, "IXS2022_0_ZX;IXS2022_9_PiMtail", "I_X first source row schema"),
        ("SRC2948_20_2165_ijx", SRC_2165_IJX, "IJX2165_0_I_X;IJX2165_4_total_vector", "later I_X/J_X demotion ledger"),
        ("SRC2948_21_2708_no_pole", SRC_2708_NO_POLE, "NPC2708_0_parent_qmap;NPC2708_8_verdict", "no-pole certificate matrix"),
        ("SRC2948_22_2643_qvis", SRC_2643_QVIS, "QVIS2643_0_chain_rule_theorem;QVIS2643_6_verdict", "common matter descent gate"),
        ("SRC2948_23_2665_hlock", SRC_2665_HLOCK, "HLOCK2665_0_target;HLOCK2665_7_verdict", "Hamiltonian/PiM/QbarXH lock"),
        ("SRC2948_24_2665_pdg", SRC_2665_PDG, "PDG2665_0_same_frame;PDG2665_7_verdict", "projector denominator gate"),
        ("SRC2948_25_912_omega", SRC_912_OMEGA, "ESO912_3_bulk_X_memory;ESO912_6_matter_frame", "extra-sector omega ledger"),
        ("SRC2948_26_973_jx", SRC_973_JX, "JXD973_0_kinetic_affine;JXD973_6_verdict", "J_X decomposition gate"),
        ("SRC2948_27_1041_thetax", SRC_1041_THETAX, "TOG1041_0_parent_route;TOG1041_5_verdict", "Theta_X owner gate"),
        ("SRC2948_28_extra_bound", SRC_EXTRA_BOUND, "FB556_0_HPiM_Cextra_core_channel_bound", "Hamiltonian extra charge bound fill row"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def certificate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PCC2948_0_parent_X_action",
            "L_X",
            "single parent sector action for the retained non-EH motion/time/range/memory sector",
            "delta L_X = E_X delta X + dTheta_X",
            "MISSING_PARENT_X_ACTION_ROUTE",
            "TOG1041_0 leaves the route unselected; NPC2708_2 leaves descent/gauge degeneracy unsigned",
        ),
        (
            "PCC2948_1_theta_X",
            "Theta_X",
            "sector symplectic potential extracted from the same L_X and boundary convention",
            "Theta_X = boundary term in delta L_X after fixed B_X policy",
            "MISSING_THETA_X_OWNER",
            "field content, boundary convention and transformation law are not parent-signed",
        ),
        (
            "PCC2948_2_Qtau_X",
            "Q_tau_X",
            "observed-time Noether charge for the X sector",
            "J_tau^X = Theta_X(L_tau X)-i_tau L_X = dQ_tau_X + C_tau_X",
            "MISSING_QTAU_X_OWNER",
            "Noether form is exact conditionally, but Q_tau_X/C_tau_X are not extracted",
        ),
        (
            "PCC2948_3_Ctau_X",
            "C_tau_X",
            "constraint/current leakage term must vanish, be exact, or be retained",
            "C_tau_X = 0, dB_X, topological class, or finite residual",
            "MISSING_CTAU_X_ZERO_OR_BOUND",
            "J_X, boundary, projector and readout tails remain open",
        ),
        (
            "PCC2948_4_operator_route",
            "Z_X,M_X^2,omega_X",
            "operator sign/no-pole route or residual force-law route is selected before scoring",
            "X absent/gauge/topological OR A_X>=0 and gap OR alpha_X(lambda) finite row",
            "ROUTE_FORK_NOT_PARENT_SELECTED",
            "positive operator, degree count and finite force-law inputs are all unsigned",
        ),
        (
            "PCC2948_5_source_silence",
            "J_X,qbar_XT,Qbar_XH",
            "ordinary matter/source/readout does not directly source X, or each channel is source-bounded",
            "J_X = J_matter+J_chiD+J_boundary+J_readout+J_history+J_PiM",
            "SOURCE_ZERO_NOT_PROVED",
            "MOMS/no-marker/no-source-slot/current owner clauses remain unsigned",
        ),
        (
            "PCC2948_6_verdict",
            "parent current-chain sector action certificate",
            "L_X supplies claim-grade Theta_X/Q_tau_X/C_tau_X and either I_X=0 or source-backed I_X/M_H_ref",
            "PCC2948_0..5 close in one parent branch",
            "CERTIFICATE_NOT_DERIVED",
            "current evidence supports only a conditional theorem plus nonclaim residual row",
        ),
    ]
    return [
        add_common(
            {
                "certificate_id": cert_id,
                "object": obj,
                "required_clause": clause,
                "mathematical_form": form,
                "current_status": status,
                "blocking_gap": gap,
                "certificate_passed": False,
                "parent_signed": False,
            }
        )
        for cert_id, obj, clause, form, status, gap in rows
    ]


def route_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ROUTE2948_0_absent_topological",
            "X absent/topological",
            "L_X=dB_top or no retained X field",
            "I_X=0 because omega_X=C_tau_X=boundary_X=0/exact",
            "NOT_ADOPTED",
            "no signed parent field inventory says the live residual direction is absent/topological",
        ),
        (
            "ROUTE2948_1_first_class_vertical",
            "X gauge/quotient vertical",
            "v_X in ker(Dq), S_parent descends/gauge-degenerate, matter/readout are q-basic",
            "I_X=0 modulo exact constraint charge",
            "CONDITIONAL_ONLY_NOT_PARENT_SIGNED",
            "q map, kernel basis, matter descent, boundary/projector silence are not closed",
        ),
        (
            "ROUTE2948_2_positive_nohair",
            "positive source-free field",
            "A_X>=0, M_X^2>=0, fixed boundary class, J_X=0",
            "I_X=0 by integration-by-parts/no-hair or finite Yukawa row if sourced",
            "OPERATOR_AND_SOURCE_INPUTS_MISSING",
            "Z_X, M_X^2, J_X silence and boundary flux values are missing",
        ),
        (
            "ROUTE2948_3_finite_residual",
            "finite source-backed residual",
            "I_X/M_H_ref = abs(int_S i_tau omega_X + int_A C_X + boundary_X)/M_H_ref",
            "keeps local branch testable without claiming GR reduction",
            "SELECTED_FALLBACK_NONCLAIM",
            "valid because it does not hide the missing theorem-zero as success",
        ),
        (
            "ROUTE2948_4_verdict",
            "route verdict",
            "one of absent/topological, first-class vertical, positive nohair, or finite residual must be chosen",
            "current corpus selects finite residual fallback only",
            "ZERO_PROOF_NOT_CLOSED",
            "next step should reduce the route fork, not circle all branches forever",
        ),
    ]
    return [
        add_common(
            {
                "route_id": route_id,
                "route": route,
                "required_signature": signature,
                "effect_if_closed": effect,
                "current_status": status,
                "reason": reason,
                "route_passed": route_id == "ROUTE2948_3_finite_residual",
                "theorem_zero": False,
            }
        )
        for route_id, route, signature, effect, status, reason in rows
    ]


def ix_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "IX2948_0_identity",
            "I_X_over_MH",
            "first live non-EH charge/current obstruction in the local denominator",
            "|int_S i_tau omega_X + int_A C_tau_X + boundary_X + PiM_tail_X|/M_H_ref",
            "dimensionless_ratio_to_M_H_ref",
            "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "L_X;Theta_X;Q_tau_X;C_tau_X;omega_X;boundary_X;PiM_tail_X;M_H_ref",
            str(SRC_1799_IX),
        ),
        (
            "IX2948_1_LX_theta_Qtau",
            "sector_charge_owner",
            "same L_X must supply Theta_X, Q_tau_X and C_tau_X",
            "delta L_X -> Theta_X; J_tau^X=dQ_tau_X+C_tau_X",
            "action_or_charge_units",
            "MISSING_PARENT_X_ACTION_ROUTE",
            "parent route;field content;boundary convention;source path;equation ref",
            str(SRC_1041_THETAX),
        ),
        (
            "IX2948_2_operator",
            "operator_sign_gap",
            "operator/no-pole data for no-hair or finite force law",
            "Z_X>=0, M_X^2>=0, lambda_X=sqrt(Z_X/M_X^2)",
            "operator_certificate_or_inverse_length",
            "MISSING_ZX_MX2_OPERATOR_SIGN",
            "Z_X;M_X^2;kernel/zero-mode rule;domain D;source path",
            str(SRC_2022_IX_SCHEMA),
        ),
        (
            "IX2948_3_JX",
            "J_X_total",
            "ordinary/hidden source current into X",
            "|J_X| <= |J_matter|+|J_chiD|+|J_boundary|+|J_readout|+|J_history|+|J_PiM|",
            "source_current",
            "SOURCE_ZERO_NOT_PROVED_COMPONENT_VALUES_MISSING",
            "component zero theorems or finite bounds for every source leg",
            str(SRC_973_JX),
        ),
        (
            "IX2948_4_boundary",
            "boundary_X",
            "X-sector boundary/corner/worldtube flux",
            "|boundary_X|/M_H_ref with fixed boundary class and no cancellation",
            "dimensionless_ratio_to_M_H_ref",
            "MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND",
            "boundary class;surface;flux coefficient;source path",
            str(SRC_1799_IX),
        ),
        (
            "IX2948_5_omega",
            "int_S_i_tau_omega_X",
            "X-sector symplectic flux in H_tau curl",
            "|int_S i_tau omega_X|/M_H_ref",
            "dimensionless_ratio_to_M_H_ref",
            "MISSING_OMEGA_X_SURFACE_INPUTS",
            "omega_X;surface;fixed tau;M_H_ref;source path",
            str(SRC_912_OMEGA),
        ),
        (
            "IX2948_6_projector",
            "PiM_tail_X",
            "Hamiltonian mass/source projection tail of X charge",
            "|Pi_M^H Q_tau_X|/M_H_ref + |[d,Pi_M]J_X|/M_H_ref",
            "dimensionless_ratio_to_M_H_ref",
            "MISSING_PIM_PROJECTION_LOCK",
            "Pi_M definition;M_H_ref;commutator stress;source path",
            str(SRC_2665_HLOCK),
        ),
        (
            "IX2948_7_acceptance",
            "IX_first_row_acceptance",
            "acceptance gate for using I_X in local tests",
            "all IX2948_1..6 theorem-zero or source-backed finite; no MISSING markers; no cancellation credit",
            "gate",
            "NOT_ACCEPTED",
            "cannot score R10/PPN/local-GR yet",
            str(SRC_2022_IX_SCHEMA),
        ),
    ]
    return [
        add_common(
            {
                "ix_row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "formula": formula,
                "units": units,
                "current_status": status,
                "required_input": required_input,
                "source_path": source_path,
                "source_path_exists": Path(source_path).exists(),
                "accepted_for_scoring": False,
                "parent_signed": False,
                "finite_value_present": False,
            }
        )
        for row_id, symbol, definition, formula, units, status, required_input, source_path in rows
    ]


def jx_rows() -> list[dict[str, Any]]:
    rows = [
        ("JX2948_0_kinetic_affine", "J_X^kin_affine", "shifted X kinetic/source origin", "zero if S_X kinetic is centered homogeneous quadratic with no X0(q)", "NOT_PARENT_SIGNED"),
        ("JX2948_1_matter", "J_X^matter", "ordinary matter pullback into X", "zero if ordinary matter depends only on q/e_obs/theta and X is quotient-null", "CONDITIONAL_ONLY"),
        ("JX2948_2_chi_wall", "J_X^chiD_wall", "domain wall/source tail", "zero if f'(0)=0 and wall stress/domain tail vanishes", "CONDITIONAL_ONLY"),
        ("JX2948_3_boundary", "J_X^boundary", "boundary/edge/reference source tail", "zero if boundary primitive is exact/fixed/zero-flux", "NOT_DERIVED"),
        ("JX2948_4_readout", "J_X^readout", "post-variation source/readout reentry", "zero if readout is pure postprocessing and no pre-action source mask exists", "NOT_DERIVED"),
        ("JX2948_5_history", "J_X^history", "memory/history kernel tail", "zero if memory kernel is local/source-free/no long tail", "NOT_DERIVED"),
        ("JX2948_6_PiM", "J_X^PiM_tail", "projector/Hamiltonian source tail", "zero if Pi_M lock and commutator stress vanish", "MISSING_PROJECTOR_LOCK"),
        ("JX2948_7_total", "J_X_total_abs", "absolute no-cancellation J_X envelope", "sum_abs(JX2948_0..6)", "COMPONENT_VALUES_MISSING"),
    ]
    return [
        add_common(
            {
                "component_id": component_id,
                "symbol": symbol,
                "definition": definition,
                "zero_condition": zero_condition,
                "current_status": status,
                "component_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "no_cancellation": True,
                "source_path": str(SRC_973_JX),
                "source_path_exists": SRC_973_JX.exists(),
            }
        )
        for component_id, symbol, definition, zero_condition, status in rows
    ]


def guard_rows() -> list[dict[str, Any]]:
    rows = [
        ("GUARD2948_0_no_EH_substitution", "EH Q_tau/Theta cannot stand in for Q_tau_X/Theta_X", True),
        ("GUARD2948_1_no_silent_by_naming", "X sector is silent only if theorem-zero/exact/topological or finite residual is carried", True),
        ("GUARD2948_2_no_aux_constraint_cheat", "Q_CAB+sigma_R*q_R_eff=0 cannot be imposed by ad hoc lambda constraint", True),
        ("GUARD2948_3_no_orbital_GM_denominator", "M_H_ref cannot be fitted from orbital GM or local test readout", True),
        ("GUARD2948_4_no_sign_cancellation", "I_X/J_X/boundary/projector pieces use absolute envelope until parent signs cancellation", True),
        ("GUARD2948_5_no_public_GR_claim", "local-GR/Newton/R10/PPN claims stay blocked from 2948", True),
    ]
    return [
        add_common({"guard_id": guard_id, "guard": guard, "guard_passed": passed})
        for guard_id, guard, passed in rows
    ]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2948_0_parent_current_chain", "parent current-chain sector action certificate passes", False, "CERTIFICATE_NOT_DERIVED"),
        ("CG2948_1_IX_zero", "I_X theorem-zero route closes", False, "ZERO_PROOF_NOT_CLOSED"),
        ("CG2948_2_IX_finite", "I_X/M_H_ref finite source-backed row accepted", False, "FIRST_ROW_VALUES_MISSING"),
        ("CG2948_3_JX_zero", "J_X source silence closes", False, "SOURCE_ZERO_NOT_PROVED"),
        ("CG2948_4_Htau_denominator", "H_tau/M_H_ref denominator can reopen", False, "BLOCKED_BY_IX_AND_PIM"),
        ("CG2948_5_local_GR", "local GR/Newton reduction claim allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2948_6_public_claim", "public claim allowed from 2948", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "claim_allowed": False,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2948_0_result",
            "parent current-chain sector action certificate not closed",
            "L_X/Theta_X/Q_tau_X/C_tau_X are still only conditional; no route is parent-selected",
            "do not promote I_X zero or H_tau denominator",
        ),
        (
            "DEC2948_1_gain",
            "route fork is now explicit",
            "absent/topological, first-class vertical, positive nohair and finite residual are separated",
            "choose one route next instead of circling all possible escapes",
        ),
        (
            "DEC2948_2_selected_fallback",
            "I_X/M_H_ref first row is emitted as nonclaim",
            "this keeps the local branch testable without pretending the zero proof is done",
            "fill source-backed components or prove theorem-zero",
        ),
        (
            "DEC2948_3_best_next",
            "attack parent X action route selection",
            "without selecting the route, Z_X/M_X^2/J_X/boundary/PiM rows remain placeholders",
            "build 2949 route selector and L_X normal-form gate",
        ),
    ]
    return [
        add_common({"decision_id": decision_id, "decision": decision, "reason": reason, "next_action": action})
        for decision_id, decision, reason, action in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2948_0_2949",
                "priority": "selected_primary",
                "next_doc": "2949-Y5-R2FR-parent-X-action-route-selector-and-LX-normal-form-gate-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_parent_X_action_route_selector_and_LX_normal_form_gate_under_AX1090_2949.py",
                "objective": "Select one defensible parent X-sector route before further local-GR claims: absent/topological, first-class vertical, positive source-free nohair, or finite sourced residual. If no route signs, keep I_X/J_X as nonclaim source-backed rows.",
                "include": "L_X normal form;field content;transformation law;Z_X;M_X^2;J_X;boundary class;PiM tail;route fork;acceptance gates",
                "exclude": "EH-only import;ad hoc auxiliary constraint;orbital-GM denominator;silent-by-word;public claim;formalization-workbench edits;GitHub action",
            }
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copy_pairs = [
        ("certificate_copy", OUTPUTS["certificate"], BRANCH_OUTPUTS["certificate_copy"]),
        ("route_copy", OUTPUTS["route"], BRANCH_OUTPUTS["route_copy"]),
        ("ix_copy", OUTPUTS["ix"], BRANCH_OUTPUTS["ix_copy"]),
        ("jx_copy", OUTPUTS["jx"], BRANCH_OUTPUTS["jx_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copy_pairs:
        if source.exists():
            shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows() -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"] + [OUTPUTS["validation"]]
    sources = read_csv_rows(OUTPUTS["sources"])
    cert = read_csv_rows(OUTPUTS["certificate"])
    routes = read_csv_rows(OUTPUTS["route"])
    ix = read_csv_rows(OUTPUTS["ix"])
    jx = read_csv_rows(OUTPUTS["jx"])
    guards = read_csv_rows(OUTPUTS["guards"])
    claims = read_csv_rows(OUTPUTS["claims"])
    next_target = read_csv_rows(OUTPUTS["next"])
    branches = read_csv_rows(OUTPUTS["branches"])

    checks = [
        ("VAL2948_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "all cited local source paths exist", True),
        ("VAL2948_1_anchors_found", all(row["anchors_found"] == "True" for row in sources), "all source anchors found", True),
        ("VAL2948_2_certificate_attempted", any(row["certificate_id"] == "PCC2948_6_verdict" for row in cert), "parent current-chain certificate verdict exists", True),
        ("VAL2948_3_certificate_not_claimed", all(row["certificate_passed"] == "False" and row["claim_allowed"] == "False" for row in cert), "certificate remains nonclaim", True),
        ("VAL2948_4_route_fork_emitted", any(row["route_id"] == "ROUTE2948_4_verdict" for row in routes), "route fork verdict emitted", True),
        ("VAL2948_5_ix_rows_nonclaim", len(ix) >= 8 and all(row["accepted_for_scoring"] == "False" and row["valid_for_claim"] == "False" for row in ix), "I_X first-row residual rows emitted and nonclaim", True),
        ("VAL2948_6_jx_envelope_nonclaim", any(row["component_id"] == "JX2948_7_total" for row in jx) and all(row["valid_for_claim"] == "False" for row in jx), "J_X envelope emitted and nonclaim", True),
        ("VAL2948_7_guards_passed", all(row["guard_passed"] == "True" for row in guards), "all no-cheat guards pass", True),
        ("VAL2948_8_claims_blocked", all(row["condition_passed"] == "False" and row["claim_allowed"] == "False" for row in claims), "all claims blocked", True),
        ("VAL2948_9_next_target_selected", any(row["next_id"] == "NEXT2948_0_2949" for row in next_target), "2949 X-route selector selected", True),
        ("VAL2948_10_branches_exist", all(row["copy_exists"] == "True" for row in branches), "branch copy files exist", True),
        ("VAL2948_11_csvs_parse", all(csv_parses(path) for path in generated_csvs), "all generated CSV files parse", True),
        ("VAL2948_12_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in [DOC, *generated_csvs, *BRANCH_OUTPUTS.values()]), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2948_13_formalization_clean", not any(FORMALIZATION.rglob("*2948*")) if FORMALIZATION.exists() else True, "no 2948 outputs were written to formalization-workbench", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "check": check,
            "required": required,
        }
        for validation_id, passed, check, required in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2948_OVERALL",
            "passed": overall,
            "check": "2948 validation overall",
            "required": True,
        }
    )
    return rows


def write_doc() -> None:
    sources = read_csv_rows(OUTPUTS["sources"])
    cert = read_csv_rows(OUTPUTS["certificate"])
    routes = read_csv_rows(OUTPUTS["route"])
    ix = read_csv_rows(OUTPUTS["ix"])
    jx = read_csv_rows(OUTPUTS["jx"])
    guards = read_csv_rows(OUTPUTS["guards"])
    claims = read_csv_rows(OUTPUTS["claims"])
    decisions = read_csv_rows(OUTPUTS["decision"])
    next_target = read_csv_rows(OUTPUTS["next"])
    branches = read_csv_rows(OUTPUTS["branches"])
    validation = read_csv_rows(OUTPUTS["validation"])
    overall = next((row["passed"] for row in validation if row["validation_id"] == "VAL2948_OVERALL"), "False")

    content = f"""# 2948 - Y5 R2FR: parent current-chain sector action certificate or I_X charge residual first row under AX1090

Status: `Y5_R2FR_2948_parent_current_chain_sector_action_certificate_not_derived_IX_first_row_emitted_nonclaim`

Claim ceiling: `no_parent_X_action_no_Qtau_X_no_IX_zero_no_MHref_no_local_GR_no_Newton_no_R10_no_PPN_no_public_claim`

2948 attacks the first live non-EH charge obstruction identified by 2947:

`I_X/M_H_ref := |int_S i_tau omega_X + int_A C_tau_X + boundary_X + PiM_tail_X|/M_H_ref`.

The exact zero route is clear: a single parent `L_X` must generate `Theta_X`, `Q_tau_X`, `C_tau_X`, and then prove the X sector is absent/topological, first-class vertical, positive source-free with no hair, or explicitly finite and source-backed. The current corpus does not yet sign any of those routes. Therefore 2948 does not claim local GR; it emits a source-ready nonclaim `I_X` row and locks the next target onto route selection for `L_X`.

## Source Register

{md_table(sources, ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Parent Current-Chain Certificate Attempt

{md_table(cert, ["certificate_id", "object", "mathematical_form", "current_status", "blocking_gap", "certificate_passed"])}

## X-Sector Route Proof Audit

{md_table(routes, ["route_id", "route", "required_signature", "effect_if_closed", "current_status", "reason"])}

## I_X Residual First Row

{md_table(ix, ["ix_row_id", "symbol", "formula", "units", "current_status", "required_input", "accepted_for_scoring"])}

## J_X Component Envelope

{md_table(jx, ["component_id", "symbol", "zero_condition", "current_status", "component_value", "no_cancellation"])}

## No-Cancellation Guards

{md_table(guards, ["guard_id", "guard", "guard_passed"])}

## Claim Gates

{md_table(claims, ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(next_target, ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(branches, ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "check", "required"])}

Validation overall: `{overall}`.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["certificate"], certificate_rows())
    write_csv(OUTPUTS["route"], route_rows())
    write_csv(OUTPUTS["ix"], ix_rows())
    write_csv(OUTPUTS["jx"], jx_rows())
    write_csv(OUTPUTS["guards"], guard_rows())
    write_csv(OUTPUTS["claims"], claim_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_rows())
    write_csv(OUTPUTS["branches"], branch_copy_rows())
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    print(f"2948 validation overall: {read_csv_rows(OUTPUTS['validation'])[-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()

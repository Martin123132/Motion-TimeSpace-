from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1646"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1646-Y5-R2FR-theta-Qtau-current-owner-or-deltaH-component-source-row.md"

SOURCE_FILES = {
    "1645_doc": ROOT / "1645-Y5-R2FR-Htau-MHref-integrability-reference-lock-or-Mstar-source-row.md",
    "1645_validation": OUT / "P8_Y5_BRR545_1645_VALIDATION.csv",
    "1645_next": OUT / "P8_Y5_PARENT_QLOC_1645_NEXT_TARGET.csv",
    "1645_theorem": OUT / "P8_Y5_PARENT_QLOC_1645_HTAU_INTEGRABILITY_THEOREM.csv",
    "1645_curl": OUT / "P8_Y5_PARENT_QLOC_1645_FIELD_SPACE_CURL_OBSTRUCTION.csv",
    "771_doc": ROOT / "771-Y5-R10-theta-Qtau-current-owner-or-deltaH-component-source-row.md",
    "771_audit": OUT / "P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
    "771_routes": OUT / "P8_Y5_R10_771_CURRENT_OWNER_ROUTE_COMPARISON.csv",
    "771_noether": OUT / "P8_Y5_R10_771_NOETHER_EXTRACTION_TEST.csv",
    "771_schema": OUT / "P8_Y5_R10_771_DELTAH_COMPONENT_SOURCE_ROW_SCHEMA.csv",
    "771_validation": OUT / "P8_Y5_BRR545_771_VALIDATION.csv",
    "993_qtau": OUT / "P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
    "667_doc": ROOT / "667-Y5-R10-explicit-parent-boundary-action-ansatz-and-variation-ledger.md",
    "667_variation": OUT / "P8_Y5_R10_667_VARIATION_LEDGER.csv",
    "667_terms": OUT / "P8_Y5_R10_667_FB5540_TERM_MAP.csv",
    "668_doc": ROOT / "668-Y5-R10-sector-Lagrangian-owner-and-boundary-condition-lock.md",
    "770_curl": OUT / "P8_Y5_R10_770_INTEGRABILITY_CURL_TEST.csv",
}

NEEDLES = {
    "1645_doc": ["Theta_total/Q_tau^MTS current ownership", "without those, the curl cannot be evaluated"],
    "1645_validation": ["VAL1645_OVERALL", "PASS"],
    "1645_next": ["1646-Y5-R2FR-theta-Qtau-current-owner-or-deltaH-component-source-row.md"],
    "1645_theorem": ["HTM1645_5_verdict", "parent theta/Q_tau extraction"],
    "1645_curl": ["ICO1645_5_curl_verdict", "FB5540_delta_H_tau_source_row_required_if_certificate_fails"],
    "771_doc": ["current owner is not accepted", "hybrid EH plus quotient-silent extra route"],
    "771_audit": ["TQ771_6_owner_verdict", "not_accepted_current_corpus"],
    "771_routes": ["COR771_C_hybrid_EH_quotient_extra", "best_next_derivation_route"],
    "771_noether": ["NET771_4_verdict", "fail_current_corpus"],
    "771_schema": ["DHS771_0_deltaH_curl", "schema_only_missing_parent_current_or_numeric_source"],
    "771_validation": ["V771_9_next_target_selected", "pass"],
    "993_qtau": ["QDEC993_5_total", "not_promoted"],
    "667_doc": ["L_parent", "delta_H_tau_nonintegrable_over_MH"],
    "667_variation": ["VL667_2_charge_decomposition", "VL667_3_Hamiltonian_variation"],
    "667_terms": ["TM667_0_delta_H_tau", "TM667_4_M_H_ref"],
    "668_doc": ["L_X, Theta_X, Q_X", "cleanest next target is `L_X`"],
    "770_curl": ["ICT770_1_curl_identity", "exact_test_written_not_evaluated"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1646_SOURCE_REGISTER.csv"
CURRENT_OWNER = OUT / "P8_Y5_PARENT_QLOC_1646_THETA_QTAU_CURRENT_OWNER_AUDIT.csv"
QTAU_STATUS = OUT / "P8_Y5_PARENT_QLOC_1646_QTAU_DECOMPOSITION_STATUS.csv"
NOETHER_TEST = OUT / "P8_Y5_PARENT_QLOC_1646_NOETHER_EXTRACTION_TEST.csv"
DELTAH_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1646_DELTAH_COMPONENT_SOURCE_SCHEMA.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1646_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1646_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1646_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1646_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    CURRENT_OWNER,
    QTAU_STATUS,
    NOETHER_TEST,
    DELTAH_SCHEMA,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    CURRENT_OWNER,
    QTAU_STATUS,
    NOETHER_TEST,
    DELTAH_SCHEMA,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {"valid_for_claim", "valid_for_mts_claim", "claim_allowed", "score_allowed"}
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1646 Theta/Q_tau current-owner audit and deltaH source-row staging",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def current_owner_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TQ1646_0_parent_variation",
            "needed_object": "explicit L_parent and Theta_total",
            "owner_test": "delta L_parent = E_A delta Phi^A + dTheta_total",
            "current_result": "TEMPLATE_AVAILABLE_NOT_CURRENT_OWNER",
            "blocker": "no single explicit local parent current-chain L_parent has EH, matter, extra, boundary, reference, tau, and coupling sectors all varied",
            "claim_effect_if_closed": "delta_H_tau curl becomes computable",
            "source_paths": ";".join([str(SOURCE_FILES["667_doc"]), str(SOURCE_FILES["771_audit"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TQ1646_1_Noether_current",
            "needed_object": "J_tau and Q_tau^MTS",
            "owner_test": "J_tau = Theta_total(Phi,L_tau Phi)-i_tau L_parent = dQ_tau^MTS + C_tau",
            "current_result": "FORMAL_SHAPE_AVAILABLE_NOT_CERTIFICATE",
            "blocker": "Q_X, C_tau, C_extra, C_projector, C_boundary, and C_ref are not extracted for retained sectors",
            "claim_effect_if_closed": "Q_tau^MTS becomes a candidate physical Hamiltonian source charge",
            "source_paths": ";".join([str(SOURCE_FILES["667_variation"]), str(SOURCE_FILES["993_qtau"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TQ1646_2_PJ_origin",
            "needed_object": "P and J_eff from one current",
            "owner_test": "j_X = theta_Y(v_X)-mu_X = X_nu J_eff^nu + (nabla_mu X_nu)P^{mu nu}+dB",
            "current_result": "DISCIPLINE_GATE_INSTALLED_NOT_EXTRACTED",
            "blocker": "P/J cannot be inserted independently; theta_Y, mu_X, v_X, and boundary improvements are still missing for current MTS",
            "claim_effect_if_closed": "DC_X/C_X and local residual rows become parent-current outputs",
            "source_paths": str(SOURCE_FILES["771_audit"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TQ1646_3_tau_boundary_reference",
            "needed_object": "tau action, B_ref, and boundary representative inside the same current",
            "owner_test": "L_tau Phi^A and delta B_ref are defined before readout with fixed improvement convention",
            "current_result": "NOT_PARENT_OWNED",
            "blocker": "observed tau, boundary class, edge charge, and reference subtraction remain split residual branches",
            "claim_effect_if_closed": "prevents arbitrary Q_tau shifts under time/reference choices",
            "source_paths": ";".join([str(SOURCE_FILES["771_audit"]), str(SOURCE_FILES["667_terms"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TQ1646_4_matter_coupling_descent",
            "needed_object": "ordinary matter/coupling descent in the same L_parent",
            "owner_test": "matter, constants, charge normalization, measure, coframe, and connection descend through q(Phi)",
            "current_result": "BLOCKED_BY_COUPLING_DESCENT",
            "blocker": "common geometry/WEP/no-marker/source-normalization route remains closure-level rather than parent-signed",
            "claim_effect_if_closed": "prevents Hamiltonian current proof hiding ordinary-coupling leaks",
            "source_paths": str(SOURCE_FILES["771_audit"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TQ1646_5_owner_verdict",
            "needed_object": "Theta_total/Q_tau^MTS current owner",
            "owner_test": "TQ1646_0 through TQ1646_4 pass together",
            "current_result": "FAIL_CURRENT_CLAIM",
            "blocker": "current owner remains a scaffold; delta_H_tau source row and hybrid route are required",
            "claim_effect_if_closed": "would reactivate the FB5540 theorem-zero path",
            "source_paths": ";".join([str(SOURCE_FILES["771_doc"]), str(SOURCE_FILES["1645_theorem"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def qtau_status_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "piece_id": "QTS1646_0_EH",
            "q_piece": "Q_tau^EH[g_obs,tau]",
            "status": "CONDITIONAL_GR_REFERENCE",
            "role": "baseline observed Hamiltonian charge where local exterior is genuinely EH",
            "why_not_claim": "EH-only import does not own retained MTS, projector, boundary/reference, source-glue, or coupling sectors",
            "next_action": "keep as baseline inside hybrid route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "piece_id": "QTS1646_1_boundary_reference",
            "q_piece": "Q_tau^boundary + delta B_ref",
            "status": "NOT_PARENT_FIXED",
            "role": "finite charge and counterterm/reference shift",
            "why_not_claim": "B_ref and allowed improvements are not selected by a current parent principle",
            "next_action": "derive boundary/reference lock or residualize Delta_ref",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "piece_id": "QTS1646_2_extra",
            "q_piece": "Q_tau^extra + C_extra",
            "status": "NOT_EXTRACTED",
            "role": "motion/time/domain extra-sector charge and constraints",
            "why_not_claim": "L_X, Theta_X, Q_X, omega_X, and C_X are not specified sector-by-sector",
            "next_action": "hybrid quotient-silent route or L_X owner target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "piece_id": "QTS1646_3_projector",
            "q_piece": "Q_tau^projector + C_projector + [d,Pi_M]J_H",
            "status": "NOT_EXTRACTED",
            "role": "mass projector/source-measure projected flux",
            "why_not_claim": "Pi_M parent owner, commutator silence, and Hilbert/topological equality are not closed",
            "next_action": "source-projector route remains downstream of current owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "piece_id": "QTS1646_4_matter_source",
            "q_piece": "C_tau^matter[J_H] and worldtube source glue",
            "status": "CONDITIONAL_NOT_GLUED",
            "role": "links charge to observed source mass before orbital fitting",
            "why_not_claim": "worldtube source equality and Poisson/Gauss/orbital readout remain downstream",
            "next_action": "do not use orbital GM as denominator",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "piece_id": "QTS1646_5_total",
            "q_piece": "Q_tau^MTS = sum pieces above",
            "status": "NOT_PROMOTED",
            "role": "candidate physical Hamiltonian source charge",
            "why_not_claim": "some pieces are conditional, unfixed, not extracted, or not glued",
            "next_action": "select hybrid EH-plus-quotient-extra route as next derivation attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def noether_test_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "test_id": "NET1646_0_parent_variation",
            "extraction_test": "derive Theta_total from L_parent",
            "formula": "delta L_parent = E_A delta Phi^A + dTheta_total",
            "current_status": "MISSING_EXPLICIT_CURRENT_CHAIN_LPARENT",
            "if_passes": "J_tau and j_X extraction become real proof objects",
            "if_fails": "delta_H_tau_nonintegrable source row remains required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "NET1646_1_tau_current",
            "extraction_test": "derive Q_tau from diffeomorphism current",
            "formula": "J_tau = Theta_total(Phi,L_tau Phi)-i_tau L_parent = dQ_tau^MTS + C_tau",
            "current_status": "CONDITIONAL_SHAPE_NO_CURRENT_OWNER",
            "if_passes": "Q_tau^MTS can enter M_H_ref and FB5540 curl",
            "if_fails": "M_H_ref and delta_H_tau remain source-row targets",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "NET1646_2_X_current",
            "extraction_test": "derive P/J/Q_X from vertical or representative current",
            "formula": "j_X = theta_Y(v_X)-mu_X = X_nu J_eff^nu + (nabla_mu X_nu)P^{mu nu} + dB",
            "current_status": "FORMULA_AVAILABLE_SPLIT_NOT_EXTRACTED",
            "if_passes": "C_X and boundary/edge flux become parent-owned",
            "if_fails": "boundary flux and q_loc/edge rows remain residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "NET1646_3_improvement_boundary",
            "extraction_test": "fix B/improvement ambiguity",
            "formula": "Q_tau^MTS and Q_X invariant under allowed dB improvements after B_ref convention fixed",
            "current_status": "REFERENCE_BOUNDARY_NOT_FIXED",
            "if_passes": "prevents arbitrary current improvement from shifting FB5540",
            "if_fails": "Delta_ref and symplectic_boundary_flux stay open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "NET1646_4_verdict",
            "extraction_test": "accept Theta_total/Q_tau current owner",
            "formula": "NET1646_0 through NET1646_3 all pass",
            "current_status": "FAIL_CURRENT_CLAIM",
            "if_passes": "FB5540 curl can be evaluated as theorem problem",
            "if_fails": "write delta_H_tau component source-row schema and move to hybrid route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def deltah_schema_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DHS1646_0_deltaH_curl",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "definition": "absolute field-space curl of the Hamiltonian one-form normalized by M_H_ref",
            "required_columns": "system_id;surface_id;variation_pair;curl_value;M_H_ref;units;frame;tau_id;source_path;assumptions;valid_for_claim",
            "current_status": "SCHEMA_ONLY_MISSING_PARENT_CURRENT_OR_NUMERIC_SOURCE",
            "claim_gate": "theorem-zero or source-backed dimensionless curl bound; no cancellation with Delta_ref/boundary terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DHS1646_1_theta_Qtau_certificate",
            "quantity": "Theta_total_Qtau_owner_certificate",
            "definition": "explicit L_parent, Theta_total, J_tau, Q_tau, C_tau, B_ref, tau action, and boundary convention",
            "required_columns": "sector;L_term;theta_term;Q_tau_term;C_tau_term;boundary_term;tau_action;owner_status;source_path;valid_for_claim",
            "current_status": "SCHEMA_ONLY_MISSING_CERTIFICATE",
            "claim_gate": "all sectors have owner_status=parent_signed or explicitly residualized",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DHS1646_2_QX_boundary_piece",
            "quantity": "Q_X_boundary_or_exact_piece",
            "definition": "extra/representative-sector contribution to Q_tau or proof it is exact/proper/zero",
            "required_columns": "sector;Q_X;exact_or_proper_status;boundary_class;edge_charge;source_path;valid_for_claim",
            "current_status": "SCHEMA_ONLY_MISSING_QX_OWNER",
            "claim_gate": "Q_X zero/exact theorem or source-backed boundary contribution",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1646_0_current_owner_not_accepted",
            "decision": "do not accept Theta_total/Q_tau^MTS current owner for current MTS",
            "reason": "every candidate misses at least one parent-owned sector, boundary/reference, tau, or coupling clause",
            "effect": "H_tau/MHref and local-GR theorem-zero remain blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1646_1_stage_deltaH_schema",
            "decision": "stage delta_H_tau source-row schema as fallback",
            "reason": "if current ownership fails, the curl obstruction must become a source-backed residual row",
            "effect": "future empirical/local gates can score only after real denominator and numerator inputs exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1646_2_select_hybrid_route",
            "decision": "select hybrid EH plus quotient-silent extra route as next derivation attempt",
            "reason": "it keeps the real EH current for observed GR while forcing MTS extra directions to prove exact/proper/quotient silence",
            "effect": "1647 should test the hybrid route before demoting to deltaH residual rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1646_0_current_owner",
            "claim": "Theta_total/Q_tau^MTS is parent-owned for current MTS",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "NO_SINGLE_PARENT_CURRENT_CHAIN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1646_1_Qtau_total",
            "claim": "Q_tau^MTS total can be promoted to physical source charge",
            "gate_pass": False,
            "status": "NOT_PROMOTED",
            "blocker": "BOUNDARY_EXTRA_PROJECTOR_MATTER_PIECES_UNOWNED_OR_UNGLUED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1646_2_deltaH_zero",
            "claim": "delta_H_tau_nonintegrable_over_MH is theorem-zero",
            "gate_pass": False,
            "status": "NO_CLAIM",
            "blocker": "CURRENT_OWNER_NOT_ACCEPTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1646_3_local_GR_PPN_R10",
            "claim": "local GR, PPN, R10, or Newton pass follows from 1646",
            "gate_pass": False,
            "status": "NO_CLAIM",
            "blocker": "H_tau/MHref/current-owner chain remains nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1646_4_guardrail",
            "claim": "current-owner and deltaH source-row guardrail is installed",
            "gate_pass": True,
            "status": "PASS_AS_INTERNAL_GUARDRAIL_ONLY",
            "blocker": "guardrail is not evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1647-Y5-R2FR-hybrid-EH-quotient-current-owner-or-deltaH-curl-source-fill.md",
            "script": "scripts/Y5_R2FR_hybrid_EH_quotient_current_owner_or_deltaH_curl_source_fill.py",
            "objective": "test the hybrid EH plus quotient-silent extra route: keep Q_EH for observed GR and prove extra local directions are quotient-silent/exact/proper or explicitly residualized",
            "success_condition": "representative/extra sectors either contribute zero/exact proper Q_X and no boundary/coupling flux, or produce explicit source-ready deltaH curl component rows",
            "guardrails": "no EH-only promotion; no inserted P/J current; no fitted reference; no orbital-GM denominator; no PPN/local-GR/R10 claim",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for path in GENERATED + [VALIDATION]:
        if path.exists():
            shutil.copy2(path, QUARANTINE / path.name)
            shutil.copy2(path, BRANCH_RESIDUALS / path.name)
    shutil.copy2(CURRENT_OWNER, QUEUE / "JR1646_THETA_QTAU_CURRENT_OWNER_AUDIT_NONCLAIM.csv")
    shutil.copy2(DELTAH_SCHEMA, QUEUE / "JR1646_DELTAH_COMPONENT_SOURCE_SCHEMA_NONCLAIM.csv")
    shutil.copy2(NEXT_TARGET, QUEUE / "JR1646_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, object]]:
    sources = csv_rows(SOURCE_REGISTER)
    current = csv_rows(CURRENT_OWNER)
    qtau = csv_rows(QTAU_STATUS)
    noether = csv_rows(NOETHER_TEST)
    schema = csv_rows(DELTAH_SCHEMA)
    gates = csv_rows(CLAIM_GATE)
    decisions = csv_rows(DECISION)
    next_targets = csv_rows(NEXT_TARGET)
    checks = [
        (
            "VAL1646_0_sources_exist",
            all(bool_string(row["path_exists"]) == "true" and bool_string(row["needles_found"]) == "true" for row in sources),
            "all cited 1646 source paths exist and needles are present",
        ),
        (
            "VAL1646_1_current_owner_rejected",
            any(row["audit_id"] == "TQ1646_5_owner_verdict" and row["current_result"] == "FAIL_CURRENT_CLAIM" for row in current),
            "Theta/Q_tau current owner is not promoted",
        ),
        (
            "VAL1646_2_Qtau_total_not_promoted",
            any(row["piece_id"] == "QTS1646_5_total" and row["status"] == "NOT_PROMOTED" for row in qtau),
            "Q_tau^MTS total remains nonclaim",
        ),
        (
            "VAL1646_3_noether_tests_written",
            any(row["test_id"] == "NET1646_4_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in noether),
            "Noether extraction tests end in current failure",
        ),
        (
            "VAL1646_4_deltaH_schema_ready",
            any(row["row_id"] == "DHS1646_0_deltaH_curl" for row in schema)
            and all(bool_string(row["valid_for_claim"]) == "false" for row in schema),
            "deltaH source-row schema is staged as nonclaim",
        ),
        (
            "VAL1646_5_hybrid_route_selected",
            any(row["decision_id"] == "DEC1646_2_select_hybrid_route" for row in decisions),
            "hybrid EH plus quotient-silent extra route selected next",
        ),
        (
            "VAL1646_6_claim_gates_safe",
            any(row["gate_id"] == "CG1646_4_guardrail" and row["status"] == "PASS_AS_INTERNAL_GUARDRAIL_ONLY" for row in gates)
            and all(bool_string(row["claim_allowed"]) == "false" for row in gates),
            "all claim gates keep MTS claims false",
        ),
        (
            "VAL1646_7_next_target_selected",
            next_targets[0]["next_target"] == "1647-Y5-R2FR-hybrid-EH-quotient-current-owner-or-deltaH-curl-source-fill.md",
            "next target selects hybrid EH quotient current-owner test",
        ),
        (
            "VAL1646_8_csv_parse",
            all(len(csv_rows(path)) > 0 for path in GENERATED),
            "all generated 1646 CSVs parse",
        ),
        (
            "VAL1646_9_no_mts_claim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1646 generated rows keep MTS claim/no-score flags false",
        ),
        (
            "VAL1646_10_branch_copies",
            all((QUARANTINE / path.name).exists() and (BRANCH_RESIDUALS / path.name).exists() for path in GENERATED),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1646_11_queue_copies",
            all(
                path.exists()
                for path in [
                    QUEUE / "JR1646_THETA_QTAU_CURRENT_OWNER_AUDIT_NONCLAIM.csv",
                    QUEUE / "JR1646_DELTAH_COMPONENT_SOURCE_SCHEMA_NONCLAIM.csv",
                    QUEUE / "JR1646_NEXT_TARGET_NONCLAIM.csv",
                ]
            ),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1646_12_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1646_13_formalization_untouched",
            not any(FORMALIZATION.rglob("*1646*")) if FORMALIZATION.exists() else True,
            "no 1646 outputs found under formalization-workbench",
        ),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1646_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1646 Theta/Q_tau current-owner and deltaH source-row validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    sources = csv_rows(SOURCE_REGISTER)
    current = csv_rows(CURRENT_OWNER)
    qtau = csv_rows(QTAU_STATUS)
    noether = csv_rows(NOETHER_TEST)
    schema = csv_rows(DELTAH_SCHEMA)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)
    validation = csv_rows(VALIDATION)
    content = f"""# 1646 - Theta Qtau Current Owner Or deltaH Component Source Row

**Private status:** nonclaim checkpoint. No `Theta_total/Q_tau^MTS` owner, stable Hamiltonian charge, `M_H_ref`, `M_*`, PPN pass, local-GR pass, Newton pass, R10 pass, WEP pass, clock pass, or orbital pass is claimed.

## Verdict

The current-owner test fails for current MTS:

```text
delta L_parent = E_A delta Phi^A + dTheta_total
J_tau = Theta_total(Phi, L_tau Phi) - i_tau L_parent = dQ_tau^MTS + C_tau
```

Those formulae are the right discipline, but the corpus does not yet supply one parent current that owns EH, matter, retained extra fields, projector/source terms, boundary/reference improvements, tau action, and coupling descent together.

The decomposition is now explicit:

```text
Q_tau^MTS = Q_EH + Q_boundary/ref + Q_extra + Q_projector + C_matter/source
```

Only `Q_EH` is a conditional GR reference piece. The total is not promoted. The fallback `delta_H_tau_nonintegrable_over_MH` row is staged, and the next derivation route is hybrid: keep the EH current where GR assumptions genuinely hold, then force MTS extra directions to prove quotient-silent/exact/proper or become residual rows.

## Source Register

{markdown_table(sources, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Theta/Qtau Current Owner Audit

{markdown_table(current, ["audit_id", "needed_object", "owner_test", "current_result", "blocker"])}

## Qtau Decomposition Status

{markdown_table(qtau, ["piece_id", "q_piece", "status", "role", "why_not_claim", "next_action"])}

## Noether Extraction Test

{markdown_table(noether, ["test_id", "extraction_test", "formula", "current_status", "if_fails"])}

## deltaH Component Source Schema

{markdown_table(schema, ["row_id", "quantity", "definition", "current_status", "claim_gate"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "effect"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        CURRENT_OWNER: current_owner_rows(),
        QTAU_STATUS: qtau_status_rows(),
        NOETHER_TEST: noether_test_rows(),
        DELTAH_SCHEMA: deltah_schema_rows(),
        DECISION: decision_rows(),
        CLAIM_GATE: claim_gate_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)
    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    copy_outputs()
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()

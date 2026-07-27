from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3371-Y5-R2FR-hidden-source-support-tail-zero-or-qbar-nonH-bound-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3371_SOURCE_REGISTER.csv",
    "tail_theorem": OUT / "P8_Y5_R2FR_3371_HIDDEN_TAIL_ZERO_THEOREM_ATTEMPT.csv",
    "source_owner": OUT / "P8_Y5_R2FR_3371_SOURCE_OWNER_TRANSFER_AUDIT.csv",
    "bound_rows": OUT / "P8_Y5_R2FR_3371_TAIL_COMPONENT_BOUND_ROWS_NONCLAIM.csv",
    "updated_envelope": OUT / "P8_Y5_R2FR_3371_QBARXT_UPDATED_ENVELOPE_NONCLAIM.csv",
    "countermodels": OUT / "P8_Y5_R2FR_3371_COUNTERMODEL_LEDGER.csv",
    "runner": OUT / "P8_Y5_R2FR_3371_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3371_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3371_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3371_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3371_VALIDATION.csv",
}

LOCAL_SOURCES = [
    (
        "SRC3371_0_3370_doc",
        ROOT / "3370-Y5-R2FR-no-shadow-frame-no-marker-matter-functor-or-first-qbar-component-bound-under-AX1090.md",
        "3370 visible frame/marker source leakage result and handoff",
    ),
    (
        "SRC3371_1_3370_next",
        OUT / "P8_Y5_R2FR_3370_NEXT_TARGET.csv",
        "3370 selects hidden source/support/domain tails as the next target",
    ),
    (
        "SRC3371_2_3370_visible_bound",
        OUT / "P8_Y5_R2FR_3370_QBAR_GEOM_MARKER_BOUND_ROWS_NONCLAIM.csv",
        "3370 visible qbar_geom/qbar_marker bound rows",
    ),
    (
        "SRC3371_3_3369_components",
        OUT / "P8_Y5_R2FR_3369_QBARXT_COMPONENT_ROWS_NONCLAIM.csv",
        "3369 total qbar_XT component envelope",
    ),
    (
        "SRC3371_4_3340_hilbert_clause",
        OUT / "P8_Y5_R2FR_3340_PARENT_HILBERT_SOURCE_CLAUSE.csv",
        "candidate Hilbert-source and public Maxwell/Hodge parent clauses",
    ),
    (
        "SRC3371_5_2594_theorem_stack",
        OUT / "P8_Y5_SOURCE_NORM_2594_THEOREM_STACK.csv",
        "Y5 source-normalization theorem stack",
    ),
    (
        "SRC3371_6_2594_channel_vector",
        OUT / "P8_Y5_SOURCE_NORM_2594_CHANNEL_VECTOR.csv",
        "eight-channel mu_extra source-normalization vector",
    ),
    (
        "SRC3371_7_2905_silence",
        OUT / "P8_Y5_R2FR_2905_EXTRA_RESPONSE_SILENCE_CERTIFICATE.csv",
        "extra-response silence certificate retaining Y5/Y6 source debts",
    ),
    (
        "SRC3371_8_2906_split",
        OUT / "P8_Y5_R2FR_2906_EPSILON_EXTRA_SOURCE_SPLIT.csv",
        "Y5/Y6 source split and no-cancellation envelope",
    ),
    (
        "SRC3371_9_3339_residual_vector",
        OUT / "P8_Y5_R2FR_3339_RESIDUAL_CHANNEL_VECTOR.csv",
        "observable residual projection vector for DeltaJ",
    ),
    (
        "SRC3371_10_2595_gm_transfer",
        OUT / "P8_Y5_GM_TRANSFER_2595_TRANSFER_GATE.csv",
        "GM-transfer/PiM/worldtube source gate",
    ),
    (
        "SRC3371_11_2595_components",
        OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv",
        "R_eq, I_commutator, B_zero_flux, projector stress, M_H_ref and surface lock rows",
    ),
    (
        "SRC3371_12_pim_contract",
        OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "Pi_M parent symplectic projector algebra contract",
    ),
    (
        "SRC3371_13_worldtube_glue",
        OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
        "worldtube/source-measure glue theorem clauses",
    ),
    (
        "SRC3371_14_boundary_status",
        OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
        "boundary/reference flux and denominator row status",
    ),
    (
        "SRC3371_15_1009_doc",
        ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "minimum parent-action sector contract",
    ),
]


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        parse_ok = False
        parse_error = ""
        if exists:
            parse_ok, parse_error = parse_csv(path) if path.suffix.lower() == ".csv" else parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def tail_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "HTZ3371_0_total_hilbert_source",
            "target_tail": "qbar_nonH",
            "conditional_zero_statement": "If the total active source is exactly the Hilbert variation of S_matter+S_EM with respect to the public coframe/metric, and no independent source-only current exists, then q_nonH=J_shadow=0.",
            "derivation_or_test": "Write delta S_source = 1/2 int sqrt(-g_pub) T_total^{mu nu} delta g_pub_{mu nu} + J_Q^mu delta A_mu. If all ordinary source/readout dependence is already in this variation, a separate non-Hilbert current has no parent argument to vary.",
            "current_status": "VALID_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "blocking_gap": "HSC3340_0/HSC3340_1 are candidate clauses, not a parent-signed total action; source-only weights remain countermodels.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HTZ3371_1_support_worldtube_fixed",
            "target_tail": "qbar_support",
            "conditional_zero_statement": "If the compact source worldtube, exterior annulus, linked surfaces and homology class are fixed before readout by the parent source measure, then Lie_X support terms vanish.",
            "derivation_or_test": "For a fixed support class W and fixed exterior surfaces S1,S2, the X-variation of the source integral has no moving-domain term; remaining mass transfer is handled by the Noether/Gauss charge equality.",
            "current_status": "CONDITIONAL_ROUTE_OPEN",
            "blocking_gap": "worldtube glue, M_H_ref, tau-frame lock and surface homology rows are not parent-signed.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HTZ3371_2_domain_projector_chainmap",
            "target_tail": "qbar_domain",
            "conditional_zero_statement": "If Pi_M is a parent-owned q-basic chain map with [d,Pi_M]J_H=0 and delta Pi_M stress either zero or included in T_total, then the domain/projector tail vanishes.",
            "derivation_or_test": "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H. In a source-free exterior with Ward/Euler closure, Pi_M dJ_H=0; if the commutator and projector stress vanish, no domain source-normalization tail remains.",
            "current_status": "VALID_CHAINMAP_THEOREM_CONDITIONAL",
            "blocking_gap": "Pi_M algebra is written but parent origin, commutator zero, projector variation stress and measured-GM transfer are not proved.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HTZ3371_3_boundary_contact_flux",
            "target_tail": "qbar_boundary",
            "conditional_zero_statement": "If boundary/reference/contact terms are exact zero-flux improvements or fixed topological data before readout, they do not shift compact source normalization.",
            "derivation_or_test": "An exact improvement changes the charge by int_S B. It is harmless only when the linked-surface difference vanishes or is fixed independently of source/readout variables.",
            "current_status": "CONDITIONAL_ROUTE_OPEN",
            "blocking_gap": "B_zero_flux, Delta_symp and boundary/contact first rows have no claim-valid theorem-zero or numeric rows.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HTZ3371_4_public_EM_Poynting_source",
            "target_tail": "qbar_nonH;EM_Hodge_stress",
            "conditional_zero_statement": "If Maxwell/Hodge uses the same public metric and hidden-independent normalization, EM energy flux and the Poynting vector are part of T_EM in the same Hilbert source, not a separate background-field force.",
            "derivation_or_test": "From S_EM=-(lambda_0/4) int sqrt(-g_pub) F^2, variation with respect to g_pub gives T_EM, while variation with respect to A gives the public current. The Poynting vector is a component of T_EM in a chosen observer frame.",
            "current_status": "VALID_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "blocking_gap": "HSC3340_4 is conditional; hidden Hodge maps, lambda(y), current normalization or radiative/static double counting remain retained residuals.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HTZ3371_5_same_branch_requirement",
            "target_tail": "qbar_tail_total",
            "conditional_zero_statement": "All hidden-tail zero clauses must hold in the same q/e_obs/tau/M_H_ref branch as 3370 visible source descent.",
            "derivation_or_test": "A zero theorem for source current, support, projector, boundary and EM stress only proves local source coupling if each uses the same denominator, source measure, surfaces and public frame.",
            "current_status": "MISSING_SAME_BRANCH_CERTIFICATE",
            "blocking_gap": "Current source rows repeatedly flag tau, M_H_ref, surface homology and branch mismatch as missing.",
            "valid_for_claim": "false",
        },
    ]


def source_owner_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "SO3371_0_hilbert_source_owner",
            "source_piece": "T_total/J_H",
            "needed_identity": "T_total is the full Hilbert variation of S_matter+S_EM against the public metric/coframe before calibration",
            "current_evidence": "HSC3340_0/HSC3340_1 candidate parent clause",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "residual_if_missing": "q_nonH;J_shadow;source_only_weight",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SO3371_1_no_spurion_weights",
            "source_piece": "species/source weights",
            "needed_identity": "no w_A(X), kappa_A(X), or source-only selector changes gravity without appearing in matter/readout",
            "current_evidence": "HSC3340_3 conditional exclusion",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "residual_if_missing": "epsilon_species_A;qbar_nonH",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SO3371_2_public_EM_Poynting",
            "source_piece": "T_EM and Poynting/radiation stress",
            "needed_identity": "Maxwell/Hodge sector uses the same g_pub and lambda_0; Poynting flux is included in Hilbert T_EM",
            "current_evidence": "HSC3340_4 public Maxwell/Hodge route",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "residual_if_missing": "delta_star;delta_J;P_EM_DeltaT_EM",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SO3371_3_GM_transfer",
            "source_piece": "measured GM/source mass",
            "needed_identity": "B_xi/G_eff = M_H[Pi_M J_H] = int_S Q_M[tau] = M_source[W] before orbital fitting",
            "current_evidence": "P8_Y5_GM_TRANSFER_2595_TRANSFER_GATE.csv",
            "status": "NOT_DERIVED_CURRENT_CORPUS",
            "residual_if_missing": "R_eq_integral;I_commutator;R_worldtube_glue;M_H_ref",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SO3371_4_PiM_chainmap",
            "source_piece": "Pi_M/source-measure projector",
            "needed_identity": "Pi_M is parent-owned, self-adjoint, charge-preserving and has zero commutator/stress in the exterior",
            "current_evidence": "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            "status": "ALGEBRA_WRITTEN_NOT_PARENT_CLOSED",
            "residual_if_missing": "I_commutator;epsilon_projector_stress;qbar_domain",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SO3371_5_worldtube_support",
            "source_piece": "worldtube/support class",
            "needed_identity": "worldtube source measure equals exterior charge on fixed linked surfaces before readout",
            "current_evidence": "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
            "status": "CORE_GLUE_NOT_DERIVED",
            "residual_if_missing": "Delta_W_support;R_worldtube_glue;surface_homology_lock",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SO3371_6_boundary_reference",
            "source_piece": "boundary/reference/contact terms",
            "needed_identity": "B_zero_flux and Delta_symp are zero/fixed or numerically bounded relative to M_H_ref",
            "current_evidence": "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
            "status": "FIRST_ROW_UNFILLED",
            "residual_if_missing": "qbar_boundary;B_zero_flux;Delta_symp;epsilon_boundary_contact",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SO3371_7_no_GM_absorption",
            "source_piece": "calibration/readout",
            "needed_identity": "observed/fitted orbital GM is not used as the proof of source normalization",
            "current_evidence": "YSN2594_4 and SPL2906_2 guard",
            "status": "GUARD_ACTIVE_NOT_THEOREM",
            "residual_if_missing": "epsilon_Y5_GM_absorption_shortcut;epsilon_calibration",
            "valid_for_claim": "false",
        },
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "HTB3371_0_qbar_nonH",
            "symbol": "qbar_nonH",
            "definition": "hidden non-Hilbert/source-shadow current contribution to the extra-response source leg",
            "zero_route": "total active source is public Hilbert variation of S_matter+S_EM with no source-only current or spurion weights",
            "bound_formula": "|qbar_nonH| <= |q_nonH| + |J_shadow|/|J_H| + |epsilon_species_A| + |delta_star| + |delta_J|",
            "required_inputs": "q_nonH,J_shadow,J_H,epsilon_species_A,EM_Hodge/current residuals, source paths and units",
            "current_status": "THEOREM_CONDITIONAL_VALUES_MISSING",
            "observable_links": "source_mass;WEP;Newton;local_GR;EM_Poynting;clock",
            "valid_for_claim": "false",
        },
        {
            "row_id": "HTB3371_1_qbar_support",
            "symbol": "qbar_support",
            "definition": "source worldtube/support shift under X variation",
            "zero_route": "worldtube W, exterior annulus, linked surfaces, homology class and M_H_ref are parent-fixed before readout",
            "bound_formula": "|qbar_support| <= |Delta_W_support| + |R_worldtube_glue|/|M_H_ref| + |surface_homology_drift|",
            "required_inputs": "Delta_W_support,R_worldtube_glue,M_H_ref,surface_homology_lock,tau_frame_lock",
            "current_status": "THEOREM_CONDITIONAL_VALUES_MISSING",
            "observable_links": "orbital_GM;source_mass;PPN;Newton",
            "valid_for_claim": "false",
        },
        {
            "row_id": "HTB3371_2_qbar_domain",
            "symbol": "qbar_domain",
            "definition": "domain/projector/source-measure contribution to qbar_XT",
            "zero_route": "Pi_M and domain selector are parent-owned q-basic chain maps with zero commutator and zero projector stress",
            "bound_formula": "|qbar_domain| <= |epsilon_Qv_projector_piece| + |epsilon_Cv_constraint_missing| + |I_commutator|/|M_H_ref| + |epsilon_projector_stress|",
            "required_inputs": "epsilon_Qv_projector_piece,epsilon_Cv_constraint_missing,I_commutator,M_H_ref,epsilon_projector_stress",
            "current_status": "THEOREM_CONDITIONAL_VALUES_MISSING",
            "observable_links": "Newton;orbital_GM;PPN;source_mass;R11",
            "valid_for_claim": "false",
        },
        {
            "row_id": "HTB3371_3_qbar_boundary",
            "symbol": "qbar_boundary",
            "definition": "boundary/contact/interface source contribution to qbar_XT",
            "zero_route": "boundary/reference/contact terms are exact zero-flux improvements, fixed topological data, or finite bounded residuals",
            "bound_formula": "|qbar_boundary| <= |epsilon_boundary_contact| + |B_X_flux| + |B_zero_flux|/|M_H_ref| + |Delta_symp|/|M_H_ref|",
            "required_inputs": "epsilon_boundary_contact,B_X_flux,B_zero_flux,Delta_symp,M_H_ref,boundary condition source",
            "current_status": "THEOREM_CONDITIONAL_VALUES_MISSING",
            "observable_links": "PPN;R10;orbital_GM;WEP_material;boundary_reference",
            "valid_for_claim": "false",
        },
        {
            "row_id": "HTB3371_4_hidden_tail_total",
            "symbol": "qbar_hidden_tail_bound_abs",
            "definition": "absolute no-cancellation bound for hidden/source/support/domain/boundary tails",
            "zero_route": "HTB3371_0 through HTB3371_3 theorem-zero in the same branch",
            "bound_formula": "|qbar_hidden_tail| <= |qbar_nonH| + |qbar_support| + |qbar_domain| + |qbar_boundary|",
            "required_inputs": "all 3371 component inputs with same branch, denominator and source path",
            "current_status": "SCHEMA_READY_NONCLAIM",
            "observable_links": "qbar_XT;R_nonEH;local_GR;Newton;PPN;R10;orbital",
            "valid_for_claim": "false",
        },
    ]


def updated_envelope_rows() -> list[dict[str, str]]:
    return [
        {
            "envelope_id": "ENV3371_0_qbarXT_full_abs",
            "symbol": "qbar_XT_bound_abs",
            "formula": "|qbar_XT| <= |qbar_geom_marker| + |qbar_hidden_tail|",
            "expanded_formula": "|qbar_XT| <= |tau_g c_g| + |tau_dis b_dis| + sum_A |s_A b_A| + |s_alpha b_alpha| + |q_nonH| + |J_shadow|/|J_H| + |Delta_W_support| + |epsilon_Qv_projector_piece| + |epsilon_Cv_constraint_missing| + |I_commutator|/|M_H_ref| + |epsilon_projector_stress| + |epsilon_boundary_contact| + |B_X_flux| + |B_zero_flux|/|M_H_ref| + |Delta_symp|/|M_H_ref|",
            "source_rows": "3370 visible rows plus 3371 hidden-tail rows",
            "current_status": "ABSOLUTE_ENVELOPE_WRITTEN_VALUES_MISSING",
            "valid_for_claim": "false",
        },
        {
            "envelope_id": "ENV3371_1_if_3370_signed_only",
            "symbol": "qbar_XT_bound_after_visible_zero",
            "formula": "|qbar_XT| <= |qbar_hidden_tail|",
            "expanded_formula": "applies only if qbar_geom=qbar_marker=0 are parent-signed in the same branch",
            "source_rows": "3370 conditional theorem plus 3371 hidden-tail rows",
            "current_status": "CONDITIONAL_BRANCH_NOT_CURRENT_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "envelope_id": "ENV3371_2_if_hidden_tail_signed_only",
            "symbol": "qbar_XT_bound_after_hidden_zero",
            "formula": "|qbar_XT| <= |qbar_geom_marker|",
            "expanded_formula": "applies only if qbar_nonH=qbar_support=qbar_domain=qbar_boundary=0 are parent-signed in the same branch",
            "source_rows": "3371 conditional theorem plus 3370 visible rows",
            "current_status": "CONDITIONAL_BRANCH_NOT_CURRENT_CLAIM",
            "valid_for_claim": "false",
        },
    ]


def countermodel_rows() -> list[dict[str, str]]:
    return [
        {
            "countermodel_id": "CM3371_0_source_only_weight",
            "weak_premise": "matter metric is public",
            "construction": "active gravity source includes w_A(X)T_A or J_shadow while matter/readout sees only g_pub",
            "what_breaks": "qbar_nonH survives despite 3370 no-shadow frame",
            "repair": "parent Hilbert-source owner or q_nonH/J_shadow bound row",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3371_1_public_EM_hidden_Hodge",
            "weak_premise": "Maxwell equations look standard",
            "construction": "hidden Hodge map or lambda(X)F^2 changes EM stress/Poynting source normalization",
            "what_breaks": "EM/Poynting stress is not guaranteed to be the same Hilbert source",
            "repair": "public Maxwell/Hodge parent theorem or EM residual bound",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3371_2_moving_worldtube",
            "weak_premise": "source integral is Hilbert",
            "construction": "support/worldtube or linked surfaces shift under X variation",
            "what_breaks": "moving-domain terms create qbar_support",
            "repair": "fixed worldtube/source-measure theorem or Delta_W_support bound",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3371_3_projector_mask",
            "weak_premise": "Pi_M is algebraically idempotent",
            "construction": "Pi_M depends on metric/domain/readout so [d,Pi_M]J_H or delta Pi_M stress is nonzero",
            "what_breaks": "projector/domain tail creates source-normalization drift",
            "repair": "parent q-basic Pi_M chainmap theorem or I_commutator/projector stress bound",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3371_4_boundary_reference_shift",
            "weak_premise": "boundary term is exact",
            "construction": "exact/reference term has different linked-surface value or source-dependent subtraction",
            "what_breaks": "B_zero_flux or Delta_symp shifts measured source mass",
            "repair": "zero-flux/fixed-reference theorem or boundary residual row",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3371_5_orbital_GM_absorption",
            "weak_premise": "measured GM can normalize source",
            "construction": "fitted orbital GM is used as denominator and proof of source equality",
            "what_breaks": "source-normalized Newton becomes circular",
            "repair": "pre-fit Hamiltonian/Hilbert/worldtube transfer chain",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {
            "run_id": "RUN3371_0_parent_hilbert_source_branch",
            "test": "total source is public Hilbert variation and EM/Poynting stress belongs to same T_total",
            "result": "PASS_CONDITIONAL_THEOREM",
            "detail": "qbar_nonH and EM hidden-source pieces vanish only under the parent-signed source-owner contract",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3371_1_worldtube_support_branch",
            "test": "support/worldtube/surface/homology class fixed before readout",
            "result": "CONDITIONAL_NOT_CLOSED",
            "detail": "worldtube glue and M_H_ref/tau/surface lock are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3371_2_PiM_domain_branch",
            "test": "Pi_M is q-basic chain map with zero commutator and stress",
            "result": "CONDITIONAL_NOT_CLOSED",
            "detail": "projector origin, [d,Pi_M]J_H, delta Pi_M stress and GM transfer remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3371_3_boundary_branch",
            "test": "boundary/reference/contact terms are zero-flux or fixed before readout",
            "result": "CONDITIONAL_NOT_CLOSED",
            "detail": "B_zero_flux, Delta_symp and M_H_ref first rows are unfilled",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3371_4_bound_rows",
            "test": "fallback to qbar_nonH/support/domain/boundary bound rows",
            "result": "SCHEMA_READY_UNSCOREABLE",
            "detail": "all tail formulas are explicit but numeric/source-backed component rows are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3371_5_qbarXT_local_GR",
            "test": "use 3371 to claim qbar_XT=0 or local GR/Newton",
            "result": "REFUSED",
            "detail": "visible 3370, hidden 3371, same-branch and left-hand EH/Newton gates are not all parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3371_0_sources",
            "claim": "all required 3371 source paths exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "source register validates every cited local input",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3371_1_qbar_nonH_zero",
            "claim": "qbar_nonH=0 as parent theorem",
            "gate_pass": "false",
            "reason": "total Hilbert-source owner and no source-only current are conditional, not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3371_2_support_zero",
            "claim": "qbar_support=0 as parent theorem",
            "gate_pass": "false",
            "reason": "worldtube/source-measure glue and surface/tau/M_H_ref lock remain missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3371_3_domain_zero",
            "claim": "qbar_domain=0 as parent theorem",
            "gate_pass": "false",
            "reason": "Pi_M chainmap, commutator zero and projector stress ownership are not parent-closed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3371_4_boundary_zero",
            "claim": "qbar_boundary=0 as parent theorem",
            "gate_pass": "false",
            "reason": "B_zero_flux, Delta_symp and contact/interface rows are not claim-valid",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3371_5_tail_score",
            "claim": "finite hidden-tail bound can be scored",
            "gate_pass": "false",
            "reason": "all numeric component inputs are missing or nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3371_6_local_GR",
            "claim": "local GR/Newton/source coupling is established",
            "gate_pass": "false",
            "reason": "qbar_XT envelope remains nonzero/nonbounded and left-hand local-GR gates remain separate",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3371_0_progress",
            "decision": "3371 converts the hidden-tail problem into four explicit source-owner rows rather than another missing-vibes note.",
            "because": "qbar_nonH, qbar_support, qbar_domain and qbar_boundary now have conditional zero routes and absolute fallback formulas.",
            "next_action": "attack the source-owner transfer chain before attempting any local-GR claim",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3371_1_Poynting_status",
            "decision": "The Poynting vector is useful here as an ownership test, not as a new independent force.",
            "because": "if EM uses the public Maxwell/Hodge action, Poynting/radiation stress is part of T_EM; if hidden Hodge/current normalization exists, it becomes a retained qbar_nonH/EM residual.",
            "next_action": "keep EM stress in the Hilbert-source transfer audit",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3371_2_claim_ceiling",
            "decision": "No qbar_XT/local-GR/Newton promotion is allowed from 3371.",
            "because": "all zero routes are conditional and all fallback rows remain nonnumeric/nonclaim.",
            "next_action": "do not absorb tails into measured GM or assume source equality",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3371_3_best_next",
            "decision": "Best next target is the Hilbert-source transfer chain.",
            "because": "one theorem would simultaneously attack qbar_nonH, qbar_support, qbar_domain, boundary flux, Poynting/EM stress ownership and Newtonian source calibration.",
            "next_action": "try to prove B_xi/G_eff = M_H[Pi_M J_H] = int_S Q_M[tau] = M_source[W] before orbital fitting, else stage first numeric tail row",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3372-Y5-R2FR-Hilbert-source-transfer-chain-or-first-tail-numeric-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3372_Hilbert_source_transfer_chain_or_first_tail_numeric_row.py",
            "objective": "prove the pre-fit Hilbert/Hamiltonian/PiM/worldtube source transfer chain, including public EM/Poynting stress ownership, or create the first source-backed numeric hidden-tail row",
            "why_next": "3371 shows the hidden-tail blocker is mostly one source-owner transfer problem: non-Hilbert source, support motion, PiM/domain commutator, boundary flux, and measured-GM calibration all meet at the same charge chain",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3373-Y5-R2FR-parent-matter-functor-signature-or-explicit-SPM-closure-sync.md",
            "target_script": "scripts/Y5_R2FR_3373_parent_matter_functor_signature_or_explicit_spm_closure_sync.py",
            "objective": "return to the deeper 3370 parent matter-functor signature only after the hidden-tail source-transfer chain is decomposed",
            "why_next": "single-public-metric/no-marker derivation remains important, but source-owner transfer is now the broader shared choke point",
            "valid_for_claim": "false",
        },
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = list(FW.rglob("*3371*")) if FW.exists() else []

    theorem_targets = {row["target_tail"] for row in rows_by_name["tail_theorem"]}
    bound_symbols = {row["symbol"] for row in rows_by_name["bound_rows"]}
    source_pieces = {row["source_piece"] for row in rows_by_name["source_owner"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}

    checks = [
        (
            "VAL3371_0_sources_exist_parse",
            "all cited local source paths exist and parse",
            source_ok,
            "",
        ),
        (
            "VAL3371_1_outputs_parse",
            "all generated CSV outputs parse cleanly",
            len(parse_results) == len(output_csvs) and all(parse_results),
            f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}",
        ),
        (
            "VAL3371_2_tail_theorem_rows",
            "tail theorem covers nonH, support, domain, boundary, EM/Poynting and same-branch",
            {"qbar_nonH", "qbar_support", "qbar_domain", "qbar_boundary", "qbar_nonH;EM_Hodge_stress", "qbar_tail_total"}.issubset(theorem_targets),
            "",
        ),
        (
            "VAL3371_3_source_owner_audit",
            "source-owner audit covers Hilbert, EM/Poynting, GM transfer, PiM, worldtube, boundary and no-GM-absorption",
            {"T_total/J_H", "T_EM and Poynting/radiation stress", "measured GM/source mass", "Pi_M/source-measure projector", "worldtube/support class", "boundary/reference/contact terms", "calibration/readout"}.issubset(source_pieces),
            "",
        ),
        (
            "VAL3371_4_bound_rows",
            "bound rows cover qbar_nonH, qbar_support, qbar_domain, qbar_boundary and hidden-tail total",
            {"qbar_nonH", "qbar_support", "qbar_domain", "qbar_boundary", "qbar_hidden_tail_bound_abs"}.issubset(bound_symbols),
            "",
        ),
        (
            "VAL3371_5_updated_envelope",
            "updated qbarXT envelope combines 3370 visible and 3371 hidden tails",
            any(row["symbol"] == "qbar_XT_bound_abs" for row in rows_by_name["updated_envelope"]),
            "",
        ),
        (
            "VAL3371_6_countermodels",
            "countermodels block source-only, EM hidden-Hodge, moving worldtube, projector, boundary and GM absorption shortcuts",
            len(rows_by_name["countermodels"]) >= 6,
            "",
        ),
        (
            "VAL3371_7_runner_blocks_claim",
            "runner refuses qbarXT/local-GR claim and marks bounds unscoreable",
            "REFUSED" in runner_results and "SCHEMA_READY_UNSCOREABLE" in runner_results,
            "",
        ),
        (
            "VAL3371_8_gates_block_local",
            "promotion gates block nonH, support, domain, boundary, tail score and local GR",
            gate_map.get("GATE3371_1_qbar_nonH_zero") == "false"
            and gate_map.get("GATE3371_2_support_zero") == "false"
            and gate_map.get("GATE3371_3_domain_zero") == "false"
            and gate_map.get("GATE3371_4_boundary_zero") == "false"
            and gate_map.get("GATE3371_5_tail_score") == "false"
            and gate_map.get("GATE3371_6_local_GR") == "false",
            "",
        ),
        (
            "VAL3371_9_no_overclaim_flags",
            "all generated rows with valid_for_claim remain false",
            flags_ok,
            flag_detail,
        ),
        (
            "VAL3371_10_next_target",
            "next target attacks Hilbert-source transfer chain",
            rows_by_name["next"][0]["target_id"].startswith("3372-Y5-R2FR-Hilbert-source-transfer-chain"),
            "",
        ),
        (
            "VAL3371_11_write_scope_outside_formalization",
            "no 3371 files were written under formalization-workbench",
            not formalization_hits,
            f"hits={len(formalization_hits)}",
        ),
    ]
    checks.append(
        (
            "VAL3371_12_overall",
            "3371 validation overall",
            all(passed for _, _, passed, _ in checks),
            "all required checks passed" if all(passed for _, _, passed, _ in checks) else "one or more checks failed",
        )
    )
    return [
        {
            "check_id": check_id,
            "check": check,
            "passed": bool_text(passed),
            "detail": detail,
        }
        for check_id, check, passed, detail in checks
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3371 - Y5/R2FR hidden-source support-tail zero or qbar_nonH bound under AX1090",
        "",
        "## Summary",
        "- 3371 attacks the pieces that still survive after the 3370 visible no-shadow/no-marker route: hidden non-Hilbert source, support/worldtube motion, PiM/domain leakage, boundary/contact flux, and EM/Poynting source ownership.",
        "- Derivation result: each tail has a clean conditional zero theorem, but none is parent-signed in the current corpus.",
        "- The useful conceptual move is that the Poynting vector is not a new independent background force if Maxwell/Hodge is public; it is part of `T_EM`. If the Hodge/current normalization is hidden, it becomes an explicit retained residual.",
        "- Fallback result: the hidden-tail absolute envelope is now explicit: `|qbar_hidden_tail| <= |qbar_nonH| + |qbar_support| + |qbar_domain| + |qbar_boundary|`.",
        "- Current verdict: no `qbar_XT=0`, local GR, Newton, R10, PPN, orbital or source-coupling claim is allowed. The rows are schema-ready but value-missing.",
        "- Best next strike is the Hilbert-source transfer chain: prove the pre-fit equality between Hilbert/Hamiltonian charge, PiM-projected current, worldtube source mass, boundary flux and public EM stress, or fill the first numeric tail row.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Hidden-tail Zero Theorem Attempt",
        md_table(rows_by_name["tail_theorem"]),
        "## Source-owner Transfer Audit",
        md_table(rows_by_name["source_owner"]),
        "## Tail Component Bound Rows",
        md_table(rows_by_name["bound_rows"]),
        "## Updated qbarXT Envelope",
        md_table(rows_by_name["updated_envelope"]),
        "## Countermodel Ledger",
        md_table(rows_by_name["countermodels"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_register = source_rows()
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_register)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "tail_theorem": tail_theorem_rows(),
        "source_owner": source_owner_rows(),
        "bound_rows": bound_rows(),
        "updated_envelope": updated_envelope_rows(),
        "countermodels": countermodel_rows(),
        "runner": runner_rows(),
        "gates": gate_rows(source_ok),
        "decision": decision_rows(),
        "next": next_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()

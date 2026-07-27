from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2215"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2215-Y5-R2FR-MAB-lock-signature-or-pseudoinverse-residual-branch.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2215_SOURCE_REGISTER.csv",
    "lock_audit": OUT / "P8_Y5_PARENT_QLOC_2215_MAB_LOCK_SIGNATURE_AUDIT.csv",
    "theorem_attempt": OUT / "P8_Y5_PARENT_QLOC_2215_HESSIAN_LOCK_THEOREM_ATTEMPT.csv",
    "pseudoinverse": OUT / "P8_Y5_PARENT_QLOC_2215_PSEUDOINVERSE_NULL_BRANCH.csv",
    "arena_null": OUT / "P8_Y5_PARENT_QLOC_2215_ARENA_NULL_PROJECTION_ROWS.csv",
    "signature_acquisition": OUT / "P8_Y5_PARENT_QLOC_2215_MAB_SIGNATURE_ACQUISITION_ROWS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2215_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2215_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2215_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2215_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2215_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2215_MAB_LOCK_OR_NULL_BRANCH_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2215_PSEUDOINVERSE_NULL_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_MAB_LOCK_2215_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        body.append(
            "| "
            + " | ".join(
                str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
                for column in columns
            )
            + " |"
        )
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2215_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2215-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2215*",
        "*P8_Y5_BRR545_2215*",
        "*Y5_R2FR_MAB_lock_signature_or_pseudoinverse_residual_branch_2215*",
        "*JR2215*",
        "*PARENT_QLOC_MAB_LOCK_2215*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2214_handoff",
            ROOT / "2214-Y5-R2FR-algebraic-residual-coefficient-map-or-DqZ-source-descent-proof.md",
            ["NEXT2214_0_2215", "CM2214_0_M_inverse", "VAL2214_OVERALL"],
            "2214 selects M_AB lock or pseudoinverse/null branch as the next choke point.",
        ),
        (
            "2214_coefficient_map",
            OUT / "P8_Y5_PARENT_QLOC_2214_ALGEBRAIC_RESIDUAL_COEFFICIENT_MAP.csv",
            ["CM2214_0_M_inverse", "CM2214_7_verdict", "MISSING_PARENT_SIGNATURE"],
            "machine-readable G_alg/M_AB row and full R_obs map.",
        ),
        (
            "2211_handoff",
            ROOT / "2211-Y5-R2FR-parent-quadratic-residue-ZM-owner-or-constraint-branch.md",
            ["ZMO2211_1_M_from_response_doublet", "ZMC2211_1_M_AB_Hessian", "VAL2211_OVERALL"],
            "2211 identifies M_AB as algebraic Hessian candidate only.",
        ),
        (
            "2211_zm_audit",
            OUT / "P8_Y5_PARENT_QLOC_2211_ZM_OWNER_AUDIT.csv",
            ["ZMO2211_1_M_from_response_doublet", "ZMO2211_5_verdict", "ALGEBRAIC_HESSIAN_CANDIDATE_ONLY"],
            "ZM audit: response-doublet gives shape, parent ownership/sign/units missing.",
        ),
        (
            "2211_coefficients",
            OUT / "P8_Y5_PARENT_QLOC_2211_COEFFICIENT_ACQUISITION_ROWS.csv",
            ["ZMC2211_1_M_AB_Hessian", "ZMC2211_2_domain_self_adjoint", "CANDIDATE_M_AB_FROM_RESPONSE_DOUBLET_NOT_PARENT_SIGNED"],
            "coefficient rows for Hessian, self-adjoint domain and source split.",
        ),
        (
            "2212_rank_zero",
            ROOT / "2212-Y5-R2FR-principal-symbol-ZAB-owner-or-rank-zero-constraint-proof.md",
            ["PSA2212_2_m_chain", "RZC2212_4_invertible_algebraic_lock", "VAL2212_OVERALL"],
            "2212 requires nondegenerate M_AB lock or parent-owned constraint projector.",
        ),
        (
            "2212_contract",
            OUT / "P8_Y5_PARENT_QLOC_2212_RANK_ZERO_CONSTRAINT_CONTRACT.csv",
            ["RZC2212_4_invertible_algebraic_lock", "RZC2212_5_verdict", "MISSING_PARENT_SIGNATURE"],
            "rank-zero contract records M_AB signature as missing.",
        ),
        (
            "2207_response_doublet",
            ROOT / "2207-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md",
            ["GMV2207_0_response_doublet_setup", "KMR2207_2_Khat_identity", "VAL2207_OVERALL"],
            "formal response-doublet variation exists, but K_hat identity/parent signature is blocked.",
        ),
        (
            "2213_residual",
            OUT / "P8_Y5_PARENT_QLOC_2213_ALGEBRAIC_RESIDUAL_ROW.csv",
            ["RALG2213_0_eliminated_coordinate", "RALG2213_1_observed_residual_vector", "RALG2213_5_verdict"],
            "pseudoinverse/null branch inherits 2213 residual formula.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def lock_audit_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            audit_id="LOCK2215_0_shape",
            required_signature="response-doublet quadratic shape",
            mathematical_requirement="Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4) on a regular local fixed point.",
            current_evidence="2207 and 2211 provide the formal response-doublet Hessian candidate.",
            status="PASS_NONCLAIM_SHAPE_ONLY",
            if_missing="no algebraic lock theorem can even be written.",
            if_present="M_AB can be audited as a Hessian candidate, not yet a parent lock.",
            valid_lock_now=False,
        ),
        base_row(
            audit_id="LOCK2215_1_parent_density",
            required_signature="Gamma_eff is a parent-owned scalar density/action term",
            mathematical_requirement="the same parent action owns Gamma_eff, measure, boundary convention and variation domain.",
            current_evidence="2207/2211 keep Gamma_eff ownership and K_hat identity unsigned.",
            status="BLOCKED_PARENT_DENSITY_NOT_SIGNED",
            if_missing="M_AB is a formal coefficient, not an Euler lock.",
            if_present="H_AB:=delta^2 Gamma_eff/dZ^A dZ^B becomes a parent Hessian candidate.",
            valid_lock_now=False,
        ),
        base_row(
            audit_id="LOCK2215_2_field_basis_units",
            required_signature="Z^A basis, inner product and units are parent-normalized",
            mathematical_requirement="Z^A, source S_A and M_AB share a declared pairing so G_alg S has units of Z.",
            current_evidence="2211/2214 mark quotient basis, source convention and units missing.",
            status="MISSING_BASIS_UNITS",
            if_missing="M^-1 cannot be used in any local prediction.",
            if_present="coefficient rows can be dimensionally checked.",
            valid_lock_now=False,
        ),
        base_row(
            audit_id="LOCK2215_3_self_adjoint_domain",
            required_signature="M_AB is symmetric/self-adjoint on the physical local domain",
            mathematical_requirement="<X,M Y>=<M X,Y> after boundary/projector terms are removed or retained.",
            current_evidence="2211 coefficient rows require a self-adjoint domain; 2212 keeps boundary/projector open.",
            status="MISSING_DOMAIN_CERTIFICATE",
            if_missing="eigenvalue/sign language is not legal.",
            if_present="spectral split into positive/null/negative sectors becomes meaningful.",
            valid_lock_now=False,
        ),
        base_row(
            audit_id="LOCK2215_4_positive_coercive",
            required_signature="M_AB positive/coercive on physical non-null quotient directions",
            mathematical_requirement="there is c>0 with <Z_phys,M Z_phys> >= c ||Z_phys||^2.",
            current_evidence="no source gives rank/sign/eigenvalue theorem for M_AB.",
            status="MISSING_RANK_SIGN",
            if_missing="wrong-sign, flat or unstable local branches remain possible.",
            if_present="G_alg=M_phys^{-1} is a bounded algebraic response.",
            valid_lock_now=False,
        ),
        base_row(
            audit_id="LOCK2215_5_null_kernel",
            required_signature="ker(M) is parent-owned gauge/constraint only",
            mathematical_requirement="P_null Z is either gauge, removed by constraint, or explicitly retained as physical residual.",
            current_evidence="2212 asks for quotient projector; 2214 says null directions require M^+ and P_null S=0.",
            status="NULL_PROJECTOR_MISSING",
            if_missing="Z_null can be physical and visible in local arenas.",
            if_present="null branch can be removed or quarantined.",
            valid_lock_now=False,
        ),
        base_row(
            audit_id="LOCK2215_6_source_compatibility",
            required_signature="P_null S=0 for S_A=J_A+B_A+C_A^CDB+R_A",
            mathematical_requirement="sources do not drive null directions, or null forcing is bounded as a residual.",
            current_evidence="source-current, boundary, CDB and readout terms remain live.",
            status="SOURCE_COMPATIBILITY_MISSING",
            if_missing="M Z=S may be inconsistent or force a physical null residual.",
            if_present="pseudoinverse branch can reduce to physical inverse branch.",
            valid_lock_now=False,
        ),
        base_row(
            audit_id="LOCK2215_7_verdict",
            required_signature="all lock clauses close together",
            mathematical_requirement="shape + parent density + basis/units + self-adjoint domain + positive rank + null/source compatibility.",
            current_evidence="only the shape clause passes, and only as nonclaim.",
            status="MAB_LOCK_NOT_PARENT_SIGNED",
            if_missing="strict branch must carry pseudoinverse/null residual rows.",
            if_present="G_alg row can be promoted from symbolic to parent-owned nonclaim coefficient.",
            valid_lock_now=False,
        ),
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            theorem_id="HLT2215_0_abstract_lock_theorem",
            theorem_piece="abstract algebraic lock theorem",
            statement="If M is self-adjoint and coercive on physical quotient directions, ker(M) is gauge/constraint, and P_null S=0, then MZ=S has unique physical solution Z_phys=M_phys^{-1}P_phys S.",
            proof_status="ABSTRACT_THEOREM_VALID",
            current_mts_status="PREMISES_NOT_PARENT_SIGNED",
            implication="a future parent action can close the strict local branch through algebra, not Yukawa range.",
            valid_for_current_claim=False,
        ),
        base_row(
            theorem_id="HLT2215_1_zero_corollary",
            theorem_piece="local silence corollary",
            statement="If additionally S=0, Dq_Z=0, and null directions are gauge/constraint, then Z=0 modulo gauge and R_obs^I=0.",
            proof_status="CONDITIONAL_COROLLARY_VALID",
            current_mts_status="S=0, Dq_Z=0 and null-gauge clauses are open.",
            implication="this is the exact form of the desired local GR/Newton reduction for the strict branch.",
            valid_for_current_claim=False,
        ),
        base_row(
            theorem_id="HLT2215_2_current_application",
            theorem_piece="current MTS application",
            statement="Current evidence cannot replace G_alg by M^{-1} because M_AB lacks parent density, basis, units, self-adjoint domain, sign/rank and null/source compatibility.",
            proof_status="APPLICATION_FAILS_CURRENT_CORPUS",
            current_mts_status="pseudoinverse/null branch is mandatory.",
            implication="do not use M_AB as a lock in local tests yet.",
            valid_for_current_claim=False,
        ),
        base_row(
            theorem_id="HLT2215_3_verdict",
            theorem_piece="2215 theorem verdict",
            statement="The theorem route is mathematically good, but current MTS only reaches a formal Hessian shape. The next honest object is G_alg=M^+ plus null consistency/projection rows.",
            proof_status="CONDITIONAL_ROUTE_RETAINED_NULL_BRANCH_STAGED",
            current_mts_status="no local-GR/Newton claim.",
            implication="next work must derive the parent Hessian signature or bound the null branch.",
            valid_for_current_claim=False,
        ),
    ]


def pseudoinverse_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            branch_row_id="PINV2215_0_general_solution",
            object="strict branch algebraic equation",
            formula="Z^A=(M^+)^{AB}S_B+Z_null^A, with S_B=J_B+B_B+C_B^CDB+R_B^src/readout/projector",
            condition="M_AB not parent-signed invertible/coercive.",
            residual_risk="Z_null may be physical and visible; M^+S carries every unclosed source term.",
            required_closure="rank/sign theorem or explicit null projector plus source compatibility.",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            branch_row_id="PINV2215_1_null_consistency",
            object="null-source compatibility",
            formula="P_null^B S_B=0 is required for a pure constraint/gauge null sector.",
            condition="if P_null S != 0, the algebraic equation is inconsistent or demands extra physics.",
            residual_risk="source-current/boundary/readout terms can drive a local residual even when the Hessian shape exists.",
            required_closure="derive P_null and show J, B, CDB and R_src/readout are orthogonal to it.",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            branch_row_id="PINV2215_2_visible_null",
            object="observable null projection",
            formula="R_obs^I=L_A^I(M^+)^{AB}S_B+L_null,A^I Z_null^A+E_DqZ^I",
            condition="if L_null is nonzero and Z_null is not gauge, local arenas see the null branch.",
            residual_risk="PPN/WEP/clock/orbital residuals can survive without any finite-range lambda.",
            required_closure="prove L_null=0 by quotient/readout descent or keep finite arena rows.",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            branch_row_id="PINV2215_3_negative_or_flat_modes",
            object="wrong-sign/flat Hessian sectors",
            formula="Spec(M)=Spec_+ union Spec_0 union Spec_-; Spec_- or unowned Spec_0 cannot be a stable local lock.",
            condition="rank/sign theorem missing.",
            residual_risk="negative modes suggest instability or a separate physical branch rather than GR recovery.",
            required_closure="parent spectral theorem, gauge removal, or explicit residual demotion.",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            branch_row_id="PINV2215_4_claim_safe_verdict",
            object="strict branch lock status",
            formula="G_alg remains M^+ plus null/projector residuals until M_AB is parent-signed.",
            condition="current corpus.",
            residual_risk="local GR cannot be claimed from algebraic lock alone.",
            required_closure="2216 parent Hessian extraction or null-branch bound rows.",
            score_ready=False,
            valid_prediction_row=False,
        ),
    ]


def arena_null_rows() -> list[dict[str, Any]]:
    arenas = [
        ("ANP2215_0_Newton", "Newton/source-normalized GM", "Delta_GM=L_GM,A(M^+)^{AB}S_B+L_GM,null Z_null+E_GM,DqZ", "source weight or null source can mimic measured GM shift"),
        ("ANP2215_1_PPN", "PPN gamma,beta,alpha_i,xi,Gdot", "Delta_PPN^I=L_PPN,A^I(M^+)^{AB}S_B+L_PPN,null^I Z_null+E_PPN,DqZ^I", "visible null branch appears as weak-field metric residual"),
        ("ANP2215_2_R10", "R10/contact", "F_R10=L_R10,A(M^+)^{AB}S_B+L_R10,null Z_null+E_R10,DqZ", "strict branch still has no lambda; only contact/null residual is legal"),
        ("ANP2215_3_WEP", "WEP/composition", "eta_AB=L_WEP,C^{AB}(M^+)^{CD}Delta S_D+L_WEP,null^{AB}Z_null+E_WEP,DqZ", "null/source species dependence can violate WEP"),
        ("ANP2215_4_clock_EM", "clocks/EM/fine-structure", "Delta_clock/alpha=L_theta,A(M^+)^{AB}S_B+L_theta,null Z_null+Pi_theta Lie_Z(theta)+E_readout,DqZ", "constants/markers can remain visible through null sector"),
        ("ANP2215_5_orbital", "orbital/local dynamics", "Delta_orbit^I=L_orb,A^I(M^+)^{AB}S_B+L_orb,null^I Z_null+E_orb,DqZ^I", "source-worldtube/null branch can survive in compact dynamics"),
        ("ANP2215_6_R11", "non-EH/R11 operator family", "c_R11^I=L_R11,A^I(M^+)^{AB}S_B+L_R11,null^I Z_null+E_R11,DqZ^I", "operator residual cannot be assessed without basis and units"),
    ]
    return [
        base_row(
            arena_row_id=arena_id,
            arena=arena,
            null_projection_formula=formula,
            local_risk=risk,
            current_status="MISSING_L_NULL_AND_M_PLUS_INPUTS",
            required_inputs="M_AB spectral split; P_null; L_null; source compatibility; arena units",
            score_ready=False,
            valid_prediction_row=False,
        )
        for arena_id, arena, formula, risk in arenas
    ]


def signature_acquisition_rows() -> list[dict[str, Any]]:
    specs = [
        ("MSA2215_0_parent_density", "Gamma_eff parent density/action owner", "MISSING_SOURCE_PATH", "locks Hessian to parent Euler equation"),
        ("MSA2215_1_Z_basis", "parent quotient basis for Z^A", "MISSING_SOURCE_PATH", "defines physical directions and units"),
        ("MSA2215_2_pairing_units", "inner product, measure and units for Z/M/S", "MISSING_SOURCE_PATH", "makes G_alg S dimensional"),
        ("MSA2215_3_self_adjoint_domain", "domain/boundary condition making M self-adjoint", "MISSING_SOURCE_PATH", "legalizes spectral decomposition"),
        ("MSA2215_4_rank_sign", "rank/sign/eigenvalue theorem for M_AB", "MISSING_SOURCE_PATH", "decides inverse vs pseudoinverse/wrong-sign branch"),
        ("MSA2215_5_null_projector", "P_null and gauge/constraint status", "MISSING_SOURCE_PATH", "decides if null modes are physical"),
        ("MSA2215_6_source_compatibility", "P_null S=0 proof or residual row", "MISSING_SOURCE_PATH", "prevents null forcing"),
        ("MSA2215_7_L_null", "arena visibility of null directions", "MISSING_SOURCE_PATH", "decides local observable leakage"),
        ("MSA2215_8_Khat_identity", "K_hat equals metric response under same convention", "MISSING_SOURCE_PATH", "connects formal Hessian to current q_loc branch"),
    ]
    rows: list[dict[str, Any]] = []
    for acquisition_id, needed_object, source_path, why_needed in specs:
        rows.append(
            base_row(
                acquisition_id=acquisition_id,
                needed_object=needed_object,
                current_value="MISSING_PARENT_INPUT",
                units="MISSING_UNITS_OR_NOT_APPLICABLE",
                source_path=source_path,
                why_needed=why_needed,
                status="VALID_FOR_CLAIM_FALSE_PENDING_PARENT_SIGNATURE",
                score_ready=False,
                valid_prediction_row=False,
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2215_0_shape",
            gate="response-doublet Hessian shape exists",
            status="PASS_NONCLAIM",
            reason="formal M_AB candidate exists, but shape is not parent lock.",
        ),
        base_row(
            gate_id="CG2215_1_MAB_lock",
            gate="M_AB parent-signed invertible/coercive lock",
            status="BLOCKED_NONCLAIM",
            reason="parent density, units, self-adjoint domain, rank/sign and null projector are missing.",
        ),
        base_row(
            gate_id="CG2215_2_pseudoinverse_branch",
            gate="M^+/null branch staged",
            status="PASS_NONCLAIM",
            reason="general solution and null compatibility/visibility rows are written.",
        ),
        base_row(
            gate_id="CG2215_3_score_ready",
            gate="any local test score-ready",
            status="BLOCKED_NONCLAIM",
            reason="M^+, P_null, L_null, source compatibility and arena units are missing.",
        ),
        base_row(
            gate_id="CG2215_4_local_GR_Newton",
            gate="local GR/Newton claim",
            status="BLOCKED_NONCLAIM",
            reason="strict algebraic lock does not close; source/descent zeros also remain open.",
        ),
        base_row(
            gate_id="CG2215_5_GitHub",
            gate="GitHub/public update",
            status="BLOCKED_NONCLAIM",
            reason="private derivation checkpoint only.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2215_0_gain",
            decision="ABSTRACT_MAB_LOCK_THEOREM_WRITTEN",
            rationale="we now know the exact premises needed for algebraic GR recovery through M_AB.",
            next_action="preserve the theorem as the future parent-action contract.",
        ),
        base_row(
            decision_id="DEC2215_1_application",
            decision="CURRENT_MTS_DOES_NOT_SIGN_MAB_LOCK",
            rationale="only the response-doublet shape passes; parent ownership, units, domain, sign/rank and null/source compatibility fail.",
            next_action="do not use M^{-1}; use M^+ plus null branch.",
        ),
        base_row(
            decision_id="DEC2215_2_next",
            decision="PARENT_HESSIAN_SIGNATURE_OR_NULL_BOUND_NEXT",
            rationale="either derive M_AB from a parent action with spectral data, or quantify/null-project the residual.",
            next_action="2216 should hunt the parent Hessian signature first, with null-bound rows as fallback.",
        ),
        base_row(
            decision_id="DEC2215_3_scope",
            decision="NO_LOCAL_CLAIM",
            rationale="pseudoinverse/null rows make the branch honest but not predictive.",
            next_action="keep all local arenas nonclaim until M^+/P_null/L_null are sourced.",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2215_0_2216",
            selection_status="selected",
            target_file="2216-Y5-R2FR-parent-Hessian-signature-extraction-or-null-bound-rows.md",
            target_script="scripts/Y5_R2FR_parent_Hessian_signature_extraction_or_null_bound_rows_2216.py",
            objective="hunt for or derive the parent Hessian signature: Gamma_eff action owner, Z basis, pairing/units, self-adjoint domain, rank/sign theorem, null projector and source compatibility; if not found, emit source-backed null-bound acquisition rows.",
            success_condition="one M_AB lock premise becomes parent-signed, or every missing spectral/null premise receives a nonclaim acquisition row tied to an arena.",
            do_not_do="do not claim local GR/Newton, do not score local tests, do not use GitHub.",
        ),
        base_row(
            route_id="NEXT2215_1_source_parallel",
            selection_status="held_parallel",
            target_file="2215b-Y5-R2FR-source-current-owner-and-no-marker-proof.md",
            target_script="scripts/Y5_R2FR_source_current_owner_and_no_marker_proof_2215b.py",
            objective="collapse S_A by deriving source-current/no-marker/current-owner theorem.",
            success_condition="J_A/R_src becomes theorem-zero for ordinary matter or finite coefficient rows are filled.",
            do_not_do="do not assume source weights are universal.",
        ),
        base_row(
            route_id="NEXT2215_2_CDB_parallel",
            selection_status="held_parallel",
            target_file="2213b-Y5-R2FR-CDB-principal-symbol-extraction.md",
            target_script="scripts/Y5_R2FR_CDB_principal_symbol_extraction_2213b.py",
            objective="decide whether CDB reopens a principal-symbol/range branch or only adds algebraic/source leakage.",
            success_condition="CDB components classify as kinetic, algebraic, boundary, source, or zero.",
            do_not_do="do not resurrect R10 lambda without a principal symbol.",
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["signature_acquisition"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["pseudoinverse"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["lock_audit"], BRANCH_COPIES["beta_docs"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        copied = False
        parse_ok = False
        count = 0
        if source.exists():
            shutil.copyfile(source, target)
            copied = True
            parse_ok, count, _ = csv_rows_parse(target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=str(source),
                target_path=str(target),
                copied=copied,
                parse_ok=parse_ok,
                row_count=count,
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    lock_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    pseudoinverse_rows_: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    acquisition_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        rows.append(base_row(validation_id=validation_id, status="PASS" if status else "FAIL", detail=detail))

    add("VAL2215_00_sources_exist", all(truthy(row.get("path_exists")) for row in source_rows), f"{sum(truthy(row.get('path_exists')) for row in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2215_01_needles_found", all(truthy(row.get("needles_found")) for row in source_rows), f"{sum(truthy(row.get('needles_found')) for row in source_rows)}/{len(source_rows)} source needle sets found")

    lock_ok = any(row.get("audit_id") == "LOCK2215_0_shape" and row.get("status") == "PASS_NONCLAIM_SHAPE_ONLY" for row in lock_rows)
    lock_ok = lock_ok and any(row.get("audit_id") == "LOCK2215_7_verdict" and row.get("status") == "MAB_LOCK_NOT_PARENT_SIGNED" for row in lock_rows)
    lock_ok = lock_ok and all(not truthy(row.get("valid_lock_now")) for row in lock_rows)
    add("VAL2215_02_lock_audit", lock_ok, "M_AB shape retained but parent lock rejected")

    theorem_ok = any(row.get("theorem_id") == "HLT2215_0_abstract_lock_theorem" and row.get("proof_status") == "ABSTRACT_THEOREM_VALID" for row in theorem_rows)
    theorem_ok = theorem_ok and any(row.get("theorem_id") == "HLT2215_2_current_application" and row.get("proof_status") == "APPLICATION_FAILS_CURRENT_CORPUS" for row in theorem_rows)
    add("VAL2215_03_theorem_attempt", theorem_ok, "abstract lock theorem written and current application blocked")

    pinv_ok = any(row.get("branch_row_id") == "PINV2215_0_general_solution" and "M^+" in str(row.get("formula")) for row in pseudoinverse_rows_)
    pinv_ok = pinv_ok and any(row.get("branch_row_id") == "PINV2215_2_visible_null" and "L_null" in str(row.get("formula")) for row in pseudoinverse_rows_)
    pinv_ok = pinv_ok and all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in pseudoinverse_rows_)
    add("VAL2215_04_pseudoinverse_branch", pinv_ok, "M^+/null branch staged and non-score-ready")

    arena_ok = len(arena_rows) == 7 and all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in arena_rows)
    add("VAL2215_05_arena_null_rows", arena_ok, "seven arena null projection rows staged")

    acquisition_ok = len(acquisition_rows) == 9
    acquisition_ok = acquisition_ok and all(row.get("current_value") == "MISSING_PARENT_INPUT" for row in acquisition_rows)
    acquisition_ok = acquisition_ok and all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in acquisition_rows)
    add("VAL2215_06_signature_acquisition", acquisition_ok, "M_AB signature acquisition rows are explicit and nonclaim")

    claim_ok = any(row.get("gate_id") == "CG2215_1_MAB_lock" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    claim_ok = claim_ok and any(row.get("gate_id") == "CG2215_4_local_GR_Newton" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    add("VAL2215_07_claim_gate", claim_ok, "M_AB lock and local-GR/Newton claims remain blocked")

    decision_ok = any(row.get("decision") == "PARENT_HESSIAN_SIGNATURE_OR_NULL_BOUND_NEXT" for row in decision_rows_)
    add("VAL2215_08_decision", decision_ok, "decision ledger selects parent Hessian signature/null bounds next")

    next_ok = any(row.get("route_id") == "NEXT2215_0_2216" and "Hessian" in str(row.get("target_file")) for row in next_rows)
    add("VAL2215_09_next_target", next_ok, "2216 parent Hessian signature extraction selected")

    csv_details: list[str] = []
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        csv_ok = csv_ok and ok
        csv_details.append(f"{path.name}:{count if ok else detail}")
    add("VAL2215_10_csv_parse", csv_ok, "; ".join(csv_details))

    branch_ok = all(truthy(row.get("copied")) and truthy(row.get("parse_ok")) for row in copy_rows)
    add("VAL2215_11_branch_copies", branch_ok, ";".join(str(row.get("target_path")) for row in copy_rows))

    generated_groups = [source_rows, lock_rows, theorem_rows, pseudoinverse_rows_, arena_rows, acquisition_rows, claim_rows, decision_rows_, next_rows, copy_rows]
    flags_false = all(
        not truthy(row.get("valid_for_claim")) and not truthy(row.get("claim_allowed"))
        for group in generated_groups
        for row in group
    )
    add("VAL2215_12_claim_flags_false", flags_false, "all generated rows keep valid_for_claim=false and claim_allowed=false")

    no_missing_promoted = all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in pseudoinverse_rows_ + arena_rows + acquisition_rows)
    add("VAL2215_13_missing_not_promoted", no_missing_promoted, "missing spectral/null inputs are not promoted to score-ready")

    formalization_clean = not formalization_has_2215_artifacts()
    add("VAL2215_14_formalization_clean", formalization_clean, "formalization-workbench has no 2215 artifacts")

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    add("VAL2215_15_pycache_absent", pycache_absent, str(ROOT / "scripts" / "__pycache__"))

    pass_so_far = all(row.get("status") == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2215_OVERALL",
            status="PASS" if pass_so_far else "FAIL",
            detail="2215 writes the abstract M_AB lock theorem, rejects current parent-lock promotion, stages the M^+/null residual branch, and selects parent Hessian signature extraction next",
        )
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    lock_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    pseudoinverse_rows_: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    acquisition_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2215 - Y5/R2FR MAB Lock Signature Or Pseudoinverse Residual Branch",
        "",
        "## Current Verdict",
        "",
        "2215 proves the exact abstract lock contract but does **not** promote current MTS to that contract. The response-doublet gives the right Hessian shape, but the parent density, quotient basis, units, self-adjoint domain, rank/sign theorem, null projector, and null-source compatibility are not signed.",
        "",
        "So the strict branch cannot use `G_alg=M^{-1}` yet. The honest current object is:",
        "",
        "`Z^A = (M^+)^{AB} S_B + Z_null^A`, with `P_null^B S_B = 0` required before null directions can be called gauge/constraint.",
        "",
        "Observed local residuals therefore carry:",
        "",
        "`R_obs^I = L_A^I (M^+)^{AB} S_B + L_null,A^I Z_null^A + E_DqZ^I`.",
        "",
        "This is not grim. It is the missing lock named precisely. If a parent Hessian signature is later found, this row collapses beautifully. If not, the null branch becomes a finite residual problem.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## M_AB Lock Signature Audit",
        "",
        md_table(lock_rows, ["audit_id", "required_signature", "mathematical_requirement", "current_evidence", "status", "if_missing", "if_present", "valid_lock_now", "valid_for_claim"]),
        "",
        "## Hessian Lock Theorem Attempt",
        "",
        md_table(theorem_rows, ["theorem_id", "theorem_piece", "statement", "proof_status", "current_mts_status", "implication", "valid_for_current_claim", "valid_for_claim"]),
        "",
        "## Pseudoinverse / Null Branch",
        "",
        md_table(pseudoinverse_rows_, ["branch_row_id", "object", "formula", "condition", "residual_risk", "required_closure", "score_ready", "valid_prediction_row", "valid_for_claim"]),
        "",
        "## Arena Null Projection Rows",
        "",
        md_table(arena_rows, ["arena_row_id", "arena", "null_projection_formula", "local_risk", "current_status", "required_inputs", "score_ready", "valid_prediction_row", "valid_for_claim"]),
        "",
        "## M_AB Signature Acquisition Rows",
        "",
        md_table(acquisition_rows, ["acquisition_id", "needed_object", "current_value", "units", "source_path", "why_needed", "status", "score_ready", "valid_prediction_row", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claim_rows, ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decision_rows_, ["decision_id", "decision", "rationale", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(copy_rows, ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Working Interpretation",
        "",
        "The algebraic route is still alive, but it now has a hard condition: `M_AB` must be a real parent Hessian, not just a good-looking symbol. This is the right pressure point. Without it, no local-GR claim; with it, the strict branch finally has a mathematically respectable lock.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    lock_rows = lock_audit_rows()
    theorem_rows = theorem_attempt_rows()
    pseudoinverse_rows_ = pseudoinverse_rows()
    arena_rows = arena_null_rows()
    acquisition_rows = signature_acquisition_rows()
    claim_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    for path, rows in [
        (OUTPUTS["source_register"], source_rows),
        (OUTPUTS["lock_audit"], lock_rows),
        (OUTPUTS["theorem_attempt"], theorem_rows),
        (OUTPUTS["pseudoinverse"], pseudoinverse_rows_),
        (OUTPUTS["arena_null"], arena_rows),
        (OUTPUTS["signature_acquisition"], acquisition_rows),
        (OUTPUTS["claim_gate"], claim_rows),
        (OUTPUTS["decision"], decision_rows_),
        (OUTPUTS["next_target"], next_rows),
    ]:
        write_csv(path, rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], copy_rows)

    remove_pycache()
    validation_rows_ = validation_rows(
        source_rows,
        lock_rows,
        theorem_rows,
        pseudoinverse_rows_,
        arena_rows,
        acquisition_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)

    write_doc(
        source_rows,
        lock_rows,
        theorem_rows,
        pseudoinverse_rows_,
        arena_rows,
        acquisition_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        copy_rows,
        validation_rows_,
    )

    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

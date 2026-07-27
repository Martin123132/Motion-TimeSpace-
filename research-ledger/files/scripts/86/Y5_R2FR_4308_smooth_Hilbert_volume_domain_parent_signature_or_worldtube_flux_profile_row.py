from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4308"
CLAIM_ID = "L-149"
BRANCH = "MTS_R2FR_Y5_SMOOTH_HILBERT_VOLUME_DOMAIN_PARENT_SIGNATURE_OR_WORLDTUBE_FLUX_PROFILE_ROW_4308"
DECISION = "SMOOTH_HILBERT_VOLUME_SIGNATURE_PARTIAL_EXTERIOR_TRACE_DEFECT_ROW_RETAINED_NONCLAIM"
MARKER = "PPC4161_SMOOTH_HILBERT_VOLUME_DOMAIN_PARENT_SIGNATURE_OR_WORLDTUBE_FLUX_PROFILE_ROW_4308"
PACKET_MARKER = "PPC4161_PACKET_SMOOTH_HILBERT_VOLUME_DOMAIN_PARENT_SIGNATURE_OR_WORLDTUBE_FLUX_PROFILE_ROW_4308"
NEXT_TARGET = "4309-Y5-R2FR-source-domain-limit-defect-zero-or-first-numeric-flux-bound.md"

FORMAL_PATH = FORMAL / "324-PPC4161-smooth-Hilbert-volume-domain-parent-signature-or-worldtube-flux-profile-row.md"
DOC_PATH = POST / "4308-Y5-R2FR-smooth-Hilbert-volume-domain-parent-signature-or-worldtube-flux-profile-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4308_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4308_00_4307_doc": (
        POST / "4307-Y5-R2FR-source-domain-owner-or-inner-flux-profile-fill.md",
        "PARENT_SIGNATURE_OR_FIRST_FLUX_ROW_NEXT",
        "4307 handoff: parent-sign smooth Hilbert volume domain or create the first flux row.",
    ),
    "SRC4308_01_4307_formal": (
        FORMAL / "323-PPC4161-source-domain-owner-or-inner-flux-profile-fill.md",
        "partialD_in = empty set  =>  N_inner = 0",
        "4307 smooth-volume branch statement.",
    ),
    "SRC4308_02_4306_boundary": (
        FORMAL / "322-PPC4161-inner-domain-certificate-or-QmH-bound.md",
        "B_inner[phi] = int_partialD_in phi Z_m n.grad u dSigma + B_src[phi]",
        "4306 inner-boundary functional being tested.",
    ),
    "SRC4308_03_hilbert_measure": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "All ordinary local source sectors use the same observed metric/coframe and the same volume measure.",
        "Hilbert volume source measure support.",
    ),
    "SRC4308_04_hilbert_action": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "S_src = S_matter[psi,g_obs,theta]",
        "source action starts as volume Hilbert matter plus EM/binding sectors.",
    ),
    "SRC4308_05_selector": (
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "single Hilbert source functor;",
        "conditional parent-action selector includes the source functor.",
    ),
    "SRC4308_06_no_m_slot": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "with no direct m slot in S_vis",
        "visible Hilbert theorem removes direct m-source forcing conditionally.",
    ),
    "SRC4308_07_operator": (
        FORMAL / "318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md",
        "L_m u = -nabla_i(Z_m h^ij nabla_j u) + M_m^2 u + Delta_H[u],",
        "m-lock operator/domain gate to which the source-domain decision attaches.",
    ),
    "SRC4308_08_lambda": (
        FORMAL / "318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md",
        "lambda_m = Z_min lambda_1(D_loc)+M2_min-Eta_H",
        "lambda/domain handoff remains value-gated.",
    ),
    "SRC4308_09_worldtube_owner": (
        POST / "4211-Y5-R2FR-Htau-MHsource-parent-charge-owner-or-visible-matter-residual-scorecard.md",
        "same-source worldtube",
        "worldtube source owner remains viable but unsigned.",
    ),
    "SRC4308_10_worldtube_equality": (
        POST / "1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md",
        "Pi_M J_H = J_M_top + dB_zero",
        "source-to-Newton equality remains a separate gate.",
    ),
    "SRC4308_11_commutator": (
        POST / "1715-Y5-R2FR-PiM-commutator-fixed-topology-or-Icommutator-source-profile.md",
        "fixed topological chain-map",
        "exterior/topological commutator remains unsigned.",
    ),
}


def base_row() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
        "claim_allowed": "False",
        "valid_for_claim": "False",
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: List[Dict[str, str]], columns: List[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(col, "")).replace("\n", "<br>").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + content.strip() + "\n")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path) if path.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr",
        (
            "4308 attempts to parent-sign the smooth Hilbert volume source-domain route exposed by 4307. "
            "The current corpus supports the source-measure and no-direct-m-slot pieces, but it does not fully "
            "parent-sign that the m-lock operator domain includes the compact source volume, nor the smoothing/no-defect "
            "limit needed to pass from smooth matter to an exterior worldtube readout. Therefore the smooth branch remains "
            "an exact conditional N_inner=0 theorem, while the exterior branch is sharpened by a trace-defect identity "
            "and a first nonclaim flux-profile row."
        ),
        (
            "4308 source register, parent signature audit, volume-to-exterior trace-defect identity, first flux profile "
            "row, branch runner, Npair/lambda handoff, decision, firewall, status, next-target and validation CSV."
        ),
        "private_smooth_Hilbert_volume_signature_partial_trace_defect_flux_row_nonclaim",
        (
            "Either prove the smoothing/no-defect limit and source-volume inclusion for the m-lock domain, or source/bound "
            "the first exterior worldtube trace profile."
        ),
        (
            "Treating Hilbert volume source measure as proof of m-lock domain inclusion, using smooth zero after taking an "
            "exterior excision limit, dropping a trace defect measure, or claiming Newton/local-GR while R_eq, I_commutator "
            "and lambda_m remain open."
        ),
    ]
    with path.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, purpose) in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(needle in text),
                "purpose": purpose,
            }
        )
        rows.append(row)
    return rows


def signature_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "SIG4308_0_local_selector",
            "compact isolated ordinary-matter local collar has a conditional parent-action selector",
            "190 selector theorem",
            "CONDITIONAL_SELECTOR_PRESENT",
            "supports a local branch, not global adoption",
            "yes_conditionally",
        ),
        (
            "SIG4308_1_Hilbert_volume_source",
            "ordinary source sectors are written on one observed Hilbert volume measure",
            "185 source measure/action rows",
            "SOURCE_MEASURE_SUPPORTED",
            "strong evidence for smooth-volume branch",
            "yes_conditionally",
        ),
        (
            "SIG4308_2_no_direct_m_slot",
            "visible matter/EM do not contain an independent m slot on the signed branch",
            "319 visible-Hilbert silence theorem",
            "CONDITIONAL_ZERO_THEOREM",
            "kills direct source forcing into m if branch clauses hold",
            "yes_conditionally",
        ),
        (
            "SIG4308_3_m_lock_domain_includes_source",
            "D_loc/D_m for L_m contains the compact source volume rather than D\\W_H",
            "4302 operator domain is named but not source-inclusion signed",
            "NOT_PARENT_SIGNED_CORE_OPEN",
            "this is the missing clause preventing a full smooth-domain claim",
            "no",
        ),
        (
            "SIG4308_4_no_excision_or_point_limit",
            "ordinary compact source is not replaced by a point/excised hole before the m-lock variation",
            "4307 branch split",
            "BRANCH_CONVENTION_NOT_PARENT_SIGNED",
            "must be signed before borrowing partialD_in=empty",
            "no",
        ),
        (
            "SIG4308_5_smoothing_no_defect",
            "smooth source family has no trace/defect measure when read as exterior worldtube data",
            "new 4308 trace-defect identity",
            "MISSING_LIMIT_THEOREM",
            "without this, exterior flux profile survives",
            "no",
        ),
        (
            "SIG4308_6_boundary_flux_routing",
            "radiative/Poynting/worldtube flux is routed as Hilbert stress or boundary charge, not hidden bulk source",
            "192/319/4307 guardrails",
            "ROUTE_AVAILABLE_ZERO_NOT_SIGNED",
            "good guardrail, not a numeric zero",
            "partial",
        ),
        (
            "SIG4308_7_verdict",
            "smooth Hilbert volume N_inner=0 route",
            "all signature clauses above",
            "PARTIAL_SIGNATURE_EXACT_CONDITIONAL_NOT_CLAIMED",
            "source-measure/no-m-slot pieces improved; domain inclusion and no-defect limit remain open",
            "no",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for sig_id, clause, evidence_basis, status, consequence, signed_now in specs:
        row = base_row()
        row.update(
            {
                "signature_id": sig_id,
                "clause": clause,
                "evidence_basis": evidence_basis,
                "status": status,
                "consequence": consequence,
                "signed_now": signed_now,
                "claim_ready": "False",
            }
        )
        rows.append(row)
    return rows


def trace_identity_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "TRACE4308_0_full_domain",
            "D_m = W_H union A_ext with W_H not removed",
            "partialD_in=empty, B_inner=0",
            "4306/4307 domain identity",
            "smooth volume branch has no inner boundary by construction",
            "DERIVED_CONDITIONAL",
        ),
        (
            "TRACE4308_1_interface_split",
            "If one later splits D_m into W_H and A_ext, the interface terms appear with opposite normals and cancel in the full-domain weak form.",
            "int_partialW phi Z_m n_A.grad u + int_partialW phi Z_m n_W.grad u = 0",
            "integration by parts on subdomains",
            "a worldtube surface is bookkeeping in the full domain, physical in the exterior-only domain",
            "DERIVED_IDENTITY",
        ),
        (
            "TRACE4308_2_exterior_flux",
            "A_ext-only solve sees g_in := Z_m n_A.grad u|partialW_H as an actual boundary datum.",
            "B_inner^A[phi] = int_partialW_H phi g_in dSigma + B_src^A[phi]",
            "4306 trace law applied to A_ext",
            "exterior branch must carry g_in unless no-flux/matching is proved",
            "DERIVED_PROFILE_LAW",
        ),
        (
            "TRACE4308_3_defect_measure",
            "For a smoothing family rho_epsilon, exterior flux converges to a trace-defect distribution if gradients concentrate at partialW_H.",
            "mu_tr := weak-lim_{epsilon->0} g_in,epsilon dSigma",
            "trace/compactness bookkeeping",
            "smooth zero survives the exterior limit only if mu_tr=0 and B_src^A=0",
            "NEW_ZERO_GATE",
        ),
        (
            "TRACE4308_4_zero_sufficient_condition",
            "If u_epsilon -> 0 in H^1 near W_H, no direct m-slot exists, and boundary representatives do not concentrate, then mu_tr=0.",
            "||u_epsilon||_{H1(U_W)} -> 0 and B_src^A -> 0",
            "trace continuity plus 319 no-m-slot branch",
            "this is the exact next theorem to prove if we want the smooth branch to survive exterior readout",
            "CONDITIONAL_LIMIT_THEOREM",
        ),
        (
            "TRACE4308_5_bound_if_not_zero",
            "If the zero condition is not proved, keep an absolute dual-norm envelope.",
            "N_inner <= C_0|Q_m^H| + C_perp||g_perp|| + ||B_src||",
            "4306/4307 fallback",
            "first flux row is mandatory for scoreable local tests",
            "BOUND_ROUTE_RETAINED",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for trace_id, statement, formula, basis, implication, status in specs:
        row = base_row()
        row.update(
            {
                "trace_id": trace_id,
                "statement": statement,
                "formula": formula,
                "basis": basis,
                "implication": implication,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def first_flux_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "FF4308_0_domain_selector",
            "domain_choice",
            "smooth_volume_candidate_with_unsigned_domain_inclusion",
            "dimensionless",
            "PARTIAL_SIGNATURE_NOT_CLAIM_READY",
            "source-measure/no-m-slot supported; m-lock source inclusion/no-defect missing",
            "",
        ),
        (
            "FF4308_1_trace_defect",
            "mu_tr = weak-lim g_in,epsilon dSigma",
            "worldtube trace-defect measure generated by smooth-to-exterior limiting",
            "H^{-1/2}(partialW_H) measure/dual",
            "MISSING_ZERO_THEOREM_OR_VALUE",
            "prove mu_tr=0 from H1 no-hair/no concentration, or source/bound its norm",
            "",
        ),
        (
            "FF4308_2_normal_flux_profile",
            "g_in = Z_m n.grad u|partialW_H",
            "exterior normal m-lock flux profile",
            "same units as Z_m grad u",
            "MISSING_TRACE_VALUE_OR_ZERO_THEOREM",
            "first concrete profile value if smooth-domain signature cannot close",
            "",
        ),
        (
            "FF4308_3_smooth_source_injection",
            "B_src^smooth",
            "artificial inner-boundary source injection on the smooth full-volume branch",
            "H^{-1/2} dual norm",
            "ZERO_IF_SMOOTH_BRANCH_SIGNED",
            "B_src^smooth=0 follows only inside the full-volume branch, not after exterior excision",
            "0 conditional",
        ),
        (
            "FF4308_4_exterior_source_injection",
            "B_src^A",
            "source-boundary representative/injection seen by an exterior annulus",
            "H^{-1/2} dual norm",
            "MISSING_VALUE_OR_REPRESENTATIVE_ZERO",
            "must be zero/bounded separately from g_in",
            "",
        ),
        (
            "FF4308_5_no_cancellation_bound",
            "N_inner_defect_bound",
            "||mu_tr|| + ||B_src^A||, decomposed as C_0|Q_m^H|+C_perp||g_perp||+||B_src||",
            "same norm as N_inner",
            "FORMULA_READY_VALUES_MISSING",
            "absolute envelope; no cancellation between trace defect and boundary injection",
            "",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for flux_id, symbol, definition, units, status, next_action, value_or_theorem in specs:
        row = base_row()
        row.update(
            {
                "flux_id": flux_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "status": status,
                "value_or_theorem": value_or_theorem,
                "source_path": "",
                "next_action": next_action,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RUN4308_0_claim_smooth_now",
            "claim smooth Hilbert volume source-domain route is fully parent-signed now",
            "REJECT",
            "m-lock domain inclusion, no-excision convention and smoothing/no-defect theorem are not signed",
            "keep exact conditional theorem only",
        ),
        (
            "RUN4308_1_conditional_smooth",
            "conditional smooth branch if SIG4308_3, SIG4308_4 and SIG4308_5 are later signed",
            "ALLOW_CONDITIONAL",
            "N_inner=0 and N_pair<=N_EM+N_rest",
            "feed lambda_m gate after EM/rest/source-to-Newton guards",
        ),
        (
            "RUN4308_2_current_best_branch",
            "current evidence with source-measure/no-m-slot support but missing domain/no-defect signature",
            "USE_TRACE_DEFECT_ROW",
            "N_inner <= ||mu_tr|| + ||B_src^A|| <= C_0|Q_m^H|+C_perp||g_perp||+||B_src||",
            "next proof target is mu_tr=0, not another broad audit",
        ),
        (
            "RUN4308_3_exterior_numeric_fallback",
            "if no zero theorem closes",
            "SOURCE_FIRST_BOUND_ROW",
            "score g_in/Q_m^H/g_perp/B_src/C_0/C_perp as nonclaim local-test inputs",
            "R10/PPN/orbital rows remain blocked until real numbers or theorem-zeros exist",
        ),
        (
            "RUN4308_4_Newton_guard",
            "try to reopen Newton/local-GR source normalization from N_inner alone",
            "REJECT",
            "R_eq, I_commutator, calibration, lambda_m and EM/rest gates remain live",
            "do not confuse source-domain silence with Newton source-coupling derivation",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, case, result, reason, next_action in specs:
        row = base_row()
        row.update(
            {
                "runner_id": runner_id,
                "case": case,
                "result": result,
                "reason": reason,
                "next_action": next_action,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def handoff_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "HAND4308_0_smooth_if_signed",
            "N_inner=0",
            "N_pair <= N_EM + N_rest",
            "Delta_m <= (N_EM+N_rest+N_N)/lambda_m",
            "requires full smooth source-domain signature and lambda_m inputs",
            "CONDITIONAL_HANDOFF",
        ),
        (
            "HAND4308_1_trace_defect_current",
            "N_inner <= ||mu_tr|| + ||B_src^A||",
            "N_pair <= ||mu_tr|| + ||B_src^A|| + N_EM + N_rest",
            "Delta_m <= (||mu_tr||+||B_src^A||+N_EM+N_rest+N_N)/lambda_m",
            "current honest branch because no-defect theorem is missing",
            "BOUND_HANDOFF_VALUES_MISSING",
        ),
        (
            "HAND4308_2_monopole_multipole_expansion",
            "||mu_tr|| <= C_0|Q_m^H| + C_perp||g_perp||",
            "N_pair <= C_0|Q_m^H| + C_perp||g_perp|| + ||B_src|| + N_EM + N_rest",
            "same m-lock handoff with explicit worldtube flux components",
            "PROFILE_HANDOFF_READY_INPUTS_MISSING",
            "BOUND_HANDOFF_VALUES_MISSING",
        ),
        (
            "HAND4308_3_no_local_GR_claim",
            "source-domain handoff is not full GR",
            "retain R_eq + I_commutator + calibration + lambda_m + projection constants",
            "local arena scores remain blocked",
            "prevents a closed-wrong-source move",
            "GUARD_ACTIVE",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for handoff_id, inner_bound, npair_formula, delta_m_formula, needed_for_claim, status in specs:
        row = base_row()
        row.update(
            {
                "handoff_id": handoff_id,
                "inner_bound": inner_bound,
                "npair_formula": npair_formula,
                "delta_m_formula": delta_m_formula,
                "needed_for_claim": needed_for_claim,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DEC4308_0_gain",
            "TRACE_DEFECT_LAW_DERIVED",
            "Smooth-volume and exterior-worldtube branches are now connected by an explicit trace-defect measure rather than vibes.",
            "Use mu_tr as the first object to prove zero or bound.",
        ),
        (
            "DEC4308_1_signature",
            "SMOOTH_SIGNATURE_PARTIAL",
            "Hilbert volume source and no-direct-m-slot clauses are supported, but m-lock source-domain inclusion and no-defect limit are not parent-signed.",
            "Do not claim N_inner=0 for the live exterior/source-normalization branch yet.",
        ),
        (
            "DEC4308_2_fallback",
            "FIRST_FLUX_ROW_CREATED",
            "The fallback is no longer a generic missing Q_m^H: it is mu_tr/g_in/B_src^A with a no-cancellation envelope.",
            "Next target should prove mu_tr=0 or source the first trace-bound number.",
        ),
        (
            "DEC4308_3_physics",
            "COUPLING_PROBLEM_SHARPENED",
            "The coupling issue is now localized to whether source matter is inside the m-lock Hilbert volume or becomes a worldtube trace defect.",
            "This is the right place to attack the Newton/GR source coupling route.",
        ),
        (
            "DEC4308_4_next",
            "DEFECT_ZERO_OR_FIRST_NUMERIC_FLUX_BOUND_NEXT",
            "A real next move is possible: prove H1/no-concentration kills mu_tr, or source/bound mu_tr and B_src^A.",
            NEXT_TARGET,
        ),
    ]
    rows: List[Dict[str, str]] = []
    for decision_id, result, reason, next_action in specs:
        row = base_row()
        row.update({"decision_id": decision_id, "result": result, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    rules = [
        "Do not treat Hilbert volume source measure as proof that the m-lock operator domain includes the source volume.",
        "Do not pass from smooth full-domain zero to exterior worldtube zero without proving the trace-defect measure vanishes.",
        "Do not hide B_src^A inside g_in or Q_m^H; boundary representative injection is a separate absolute row.",
        "Do not reduce mu_tr to a scalar monopole unless the multipole tail is zero or bounded.",
        "Do not use any 4308 row as a Newton/local-GR claim while R_eq, I_commutator, lambda_m and projection constants remain open.",
    ]
    rows: List[Dict[str, str]] = []
    for index, rule in enumerate(rules):
        row = base_row()
        row.update({"firewall_id": f"FW4308_{index}", "rule": rule, "status": "ACTIVE"})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4308_0_Hilbert_source", "Hilbert volume source measure", "SUPPORTED_CONDITIONAL", "strong support from 185/190"),
        ("STAT4308_1_no_m_slot", "visible source direct m-slot", "CONDITIONAL_ZERO", "supported by 319 if branch clauses hold"),
        ("STAT4308_2_domain_inclusion", "m-lock source-volume domain inclusion", "OPEN_CORE_CLAUSE", "not parent-signed in current corpus"),
        ("STAT4308_3_trace_defect", "mu_tr", "NEW_PRIMARY_TARGET", "prove zero or source/bound"),
        ("STAT4308_4_Ninner", "N_inner", "EXACT_CONDITIONAL_OR_BOUND", "zero only if domain/no-defect signatures close"),
        ("STAT4308_5_local_GR", "local GR/Newton source route", "STILL_BLOCKED", "needs lambda_m, R_eq/I_commutator, EM/rest and projection gates"),
    ]
    rows: List[Dict[str, str]] = []
    for status_id, item, status, note in specs:
        row = base_row()
        row.update({"status_id": status_id, "item": item, "status": status, "note": note})
        rows.append(row)
    return rows


def next_rows() -> List[Dict[str, str]]:
    row = base_row()
    row.update(
        {
            "next_target_id": "NT4308_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the smooth-to-exterior trace-defect measure mu_tr be proved zero, or must the first numeric/source bound be filled?",
            "preferred_route": "prove H1 no-concentration/no-direct-m-slot/no-boundary-representative concentration so mu_tr=0 and B_src^A=0",
            "fallback_route": "source or bound ||mu_tr||, Q_m^H, g_perp, B_src^A and trace constants as nonclaim local-test inputs",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal_text = f"""# 324 PPC4161 smooth Hilbert volume domain parent signature or worldtube flux profile row

Marker: `{MARKER}`

## Decision

`{DECISION}`

4308 tries to close the 4307 smooth-source branch. The result is honest but useful:

```text
Hilbert volume source measure + no direct m-slot: supported conditionally.
m-lock operator domain includes source volume: not parent-signed.
smooth-to-exterior no-defect limit: not parent-signed.
```

So the smooth branch remains exact but conditional:

```text
if D_m includes W_H and mu_tr=0 and B_src^A=0, then N_inner=0.
```

The exterior branch now has a sharper first object:

```text
mu_tr := weak-lim_epsilon_to_0 g_in,epsilon dSigma,
N_inner <= ||mu_tr|| + ||B_src^A||
          <= C_0 |Q_m^H| + C_perp ||g_perp|| + ||B_src||.
```

## Parent Signature Audit

{md_table(tables["signature"], ["signature_id", "clause", "status", "signed_now", "consequence"])}

## Volume-To-Exterior Trace Identity

{md_table(tables["trace"], ["trace_id", "statement", "formula", "status"])}

## First Flux Profile Row

{md_table(tables["flux"], ["flux_id", "symbol", "definition", "status", "next_action"])}

## Branch Runner

{md_table(tables["runner"], ["runner_id", "case", "result", "reason"])}

## Npair/Lambda Handoff

{md_table(tables["handoff"], ["handoff_id", "inner_bound", "npair_formula", "status"])}

## Result

This moves the coupling problem to a precise place: either source matter lives inside the m-lock Hilbert volume and the trace defect vanishes, or exterior readout sees a real worldtube flux defect. That is the next derivation target.

Next target: `{NEXT_TARGET}`.
"""
    doc_text = f"""# 4308 - smooth Hilbert volume domain parent signature or worldtube flux profile row

## Verdict
- Tried to parent-sign the smooth Hilbert volume source-domain branch.
- Current corpus supports Hilbert volume source measure and conditional no-direct-`m` visible-source silence.
- It does not fully sign m-lock source-volume domain inclusion or the smooth-to-exterior no-defect limit.
- Derived the trace-defect law `mu_tr := weak-lim g_in,epsilon dSigma`; this becomes the first object to prove zero or bound.
- No local-GR/Newton claim fires.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Parent Signature Audit
{md_table(tables["signature"], ["signature_id", "clause", "evidence_basis", "status", "signed_now", "consequence"])}

## Volume-To-Exterior Trace-Defect Identity
{md_table(tables["trace"], ["trace_id", "statement", "formula", "basis", "implication", "status"])}

## First Flux Profile Row
{md_table(tables["flux"], ["flux_id", "symbol", "definition", "units", "status", "value_or_theorem", "next_action"])}

## Branch Decision Runner
{md_table(tables["runner"], ["runner_id", "case", "result", "reason", "next_action"])}

## Npair/Lambda Handoff
{md_table(tables["handoff"], ["handoff_id", "inner_bound", "npair_formula", "delta_m_formula", "needed_for_claim", "status"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Claim Firewall
{md_table(tables["firewall"], ["firewall_id", "rule", "status"])}

## Status
{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal_text, encoding="utf-8")
    DOC_PATH.write_text(doc_text, encoding="utf-8")


def validate_csv(path: Path) -> Tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), f"{path.name} parses with {len(rows)} rows"
    except Exception as exc:
        return False, f"{path.name} parse failure: {exc}"


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        row = base_row()
        row.update({"check_id": check_id, "description": description, "passed": str(passed), "evidence": evidence})
        rows.append(row)

    add("VAL4308_0_sources_exist", "all cited local source paths exist", all(Path(row["source_path"]).exists() for row in tables["sources"]), "source_register")
    add("VAL4308_1_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4308_2_partial_signature", "signature audit keeps smooth branch partial, not claimed", any(row["signature_id"] == "SIG4308_7_verdict" and row["status"] == "PARTIAL_SIGNATURE_EXACT_CONDITIONAL_NOT_CLAIMED" for row in tables["signature"]), "signature_rows")
    add("VAL4308_3_core_open", "m-lock source-domain inclusion remains explicitly open", any(row["signature_id"] == "SIG4308_3_m_lock_domain_includes_source" and row["signed_now"] == "no" for row in tables["signature"]), "signature_rows")
    add("VAL4308_4_trace_defect", "trace-defect measure row exists", any(row["trace_id"] == "TRACE4308_3_defect_measure" for row in tables["trace"]), "trace_rows")
    add("VAL4308_5_first_flux_mu", "first flux rows include mu_tr", any(row["symbol"].startswith("mu_tr") for row in tables["flux"]), "flux_rows")
    add("VAL4308_6_runner_rejects_claim", "runner rejects claiming smooth branch now", any(row["runner_id"] == "RUN4308_0_claim_smooth_now" and row["result"] == "REJECT" for row in tables["runner"]), "runner_rows")
    add("VAL4308_7_handoff_bound", "current handoff includes trace-defect bound", any(row["handoff_id"] == "HAND4308_1_trace_defect_current" for row in tables["handoff"]), "handoff_rows")
    add("VAL4308_8_next_selected", f"next target is {NEXT_TARGET}", tables["next"][0]["next_target"] == NEXT_TARGET, "next_rows")
    add(
        "VAL4308_9_claim_flags_false",
        "all generated rows keep claim flags false",
        all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for table in tables.values() for row in table),
        "generated_tables",
    )
    add(
        "VAL4308_10_flux_rows_nonclaim",
        "all flux rows remain nonclaim/source-unscored",
        all(row.get("score_ready") == "False" and row.get("valid_for_claim") == "False" for row in tables["flux"]),
        "flux_rows",
    )
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4308_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4308_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "generated_docs")
    add("VAL4308_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims_register")
    add("VAL4308_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "unification_spine")
    add("VAL4308_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "private_packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4308_SOURCE_REGISTER.csv",
        "signature": SOURCE_DIR / "P8_Y5_R2FR_4308_PARENT_SIGNATURE_AUDIT.csv",
        "trace": SOURCE_DIR / "P8_Y5_R2FR_4308_VOLUME_TO_EXTERIOR_TRACE_DEFECT_IDENTITY.csv",
        "flux": SOURCE_DIR / "P8_Y5_R2FR_4308_FIRST_FLUX_PROFILE_ROW.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4308_BRANCH_DECISION_RUNNER.csv",
        "handoff": SOURCE_DIR / "P8_Y5_R2FR_4308_NPAIR_LAMBDA_HANDOFF.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4308_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4308_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4308_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4308_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "signature": signature_rows(),
        "trace": trace_identity_rows(),
        "flux": first_flux_rows(),
        "runner": runner_rows(),
        "handoff": handoff_rows(),
        "decision": decision_rows(),
        "firewall": firewall_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }
    for key, rows in tables.items():
        write_csv(paths[key], rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4308 smooth Hilbert volume domain parent signature or worldtube flux profile row

Marker: `{MARKER}`

4308 attempts the smooth-domain parent signature. The corpus supports Hilbert volume source measure and conditional visible-source no-direct-`m` silence, but does not yet parent-sign that the m-lock domain includes the compact source volume or that the smooth-to-exterior limit has no trace defect. The new derived object is `mu_tr := weak-lim g_in,epsilon dSigma`; if `mu_tr=0` and `B_src^A=0`, the 4307 smooth branch survives exterior readout. Otherwise `N_inner <= ||mu_tr|| + ||B_src^A|| <= C_0|Q_m^H|+C_perp||g_perp||+||B_src||`.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4308 packet trace-defect coupling row

Marker: `{PACKET_MARKER}`

Packet update: the coupling gap is localized to the smooth-source/domain-to-exterior trace defect. Prove `mu_tr=0` from no-concentration/no-direct-`m` source conditions, or carry the worldtube flux profile as a first-class residual.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} evidence={row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

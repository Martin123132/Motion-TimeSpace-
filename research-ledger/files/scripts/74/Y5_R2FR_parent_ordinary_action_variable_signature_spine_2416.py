from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_ORDINARY_ACTION_VARIABLE_SIGNATURE_SPINE_2416"
CHECKPOINT_ID = "2416"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2416-Y5-R2FR-parent-ordinary-action-variable-signature-spine.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2416_SOURCE_REGISTER.csv",
    "signature_spine": OUT / "P8_Y5_PARENT_QLOC_2416_PARENT_ACTION_SIGNATURE_SPINE.csv",
    "activation": OUT / "P8_Y5_PARENT_QLOC_2416_THEOREM_ACTIVATION_MATRIX.csv",
    "route_split": OUT / "P8_Y5_PARENT_QLOC_2416_ADOPTION_DERIVATION_FALLBACK_ROUTE_SPLIT.csv",
    "residual_stack": OUT / "P8_Y5_PARENT_QLOC_2416_RESIDUAL_STACK_AFTER_SIGNATURE_ATTEMPT.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2416_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2416_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2416_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2416_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2416_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2416_PARENT_ACTION_SIGNATURE_SPINE_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2416_RESIDUAL_STACK_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_PARENT_ACTION_SIGNATURE_DECISION_2416_NONCLAIM.csv",
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


def formalization_has_2416_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2416-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2416*",
        "*P8_Y5_BRR545_2416*",
        "*Y5_R2FR_parent_ordinary_action_variable_signature_spine_2416*",
        "*JR2416*",
        "*PARENT_QLOC_PARENT_ACTION_SIGNATURE_DECISION_2416*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2415_handoff",
            ROOT / "2415-Y5-R2FR-sector-Gamma-slot-audit-and-private-SRNG-lock.md",
            ["SGA2415_10_verdict", "NEXT2415_0_selected", "VAL2415_OVERALL"],
            "current handoff: no public sector-sum, parent action signature selected next.",
        ),
        (
            "1963_minimal_owned_coframe",
            ROOT / "1963-Y5-R2FR-minimal-owned-coframe-parent-action-or-P4-hypermomentum-row.md",
            ["ACT1963_0_target", "ACT1963_5_no_independent_Gamma_clause", "VAL1963_OVERALL"],
            "minimal owned-coframe action skeleton and no-independent-Gamma clause.",
        ),
        (
            "2329_source_blind_signature",
            ROOT / "2329-Y5-R2FR-parent-action-source-blind-functor-signature.md",
            ["SBF2329_6_verdict", "ACT2329_2_adopt_as_parent_action_definition", "VAL2329_OVERALL"],
            "source-blind matter functor signature and adoption gate.",
        ),
        (
            "2330_adoption_decision",
            ROOT / "2330-Y5-R2FR-parent-action-adoption-vs-deeper-quotient-derivation-decision.md",
            ["DQD2330_5_verdict", "PAR2330_0_name", "VAL2330_OVERALL"],
            "deeper quotient derivation not closed; private MUMC restriction drafted.",
        ),
        (
            "2334_sector_audit",
            ROOT / "2334-Y5-R2FR-noGamma-slot-matter-source-readout-audit.md",
            ["NGSA2334_9_verdict", "NGT2334_4_result", "VAL2334_OVERALL"],
            "sector-sum no-Gamma theorem is exact conditional only.",
        ),
        (
            "2335_srng_certificate",
            ROOT / "2335-Y5-R2FR-source-readout-noGamma-action-argument-certificate.md",
            ["SRNG2335_6_verdict", "THM2335_3_SRNG_sum", "VAL2335_OVERALL"],
            "source/readout no-Gamma certificate and SRNG sum theorem attempt.",
        ),
        (
            "2348_spin_contract",
            ROOT / "2348-Y5-R2FR-spin-connection-coframe-owned-or-axial-torsion-P4-row.md",
            ["SPIN2348_6_verdict", "CHAIN2348_5_parent_contract", "VAL2348_OVERALL"],
            "coframe-owned spin connection is exact conditional, not public.",
        ),
        (
            "2349_projective_contract",
            ROOT / "2349-Y5-R2FR-projective-trace-silence-or-P4-projective-component-row.md",
            ["PROJ2349_5_verdict", "PSTACK2349_4_parent_contract", "VAL2349_OVERALL"],
            "projective trace private zero and public fallback.",
        ),
        (
            "2350_boundary_leak",
            ROOT / "2350-Y5-R2FR-boundary-improvement-current-zero-or-P4-boundary-row.md",
            ["BIC2350_7_verdict", "P4B2350_0_boundary_total", "VAL2350_OVERALL"],
            "boundary/improvement current remains primary private-branch leak.",
        ),
        (
            "2151_source_owner",
            ROOT / "2151-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
            ["SOC2151_7_verdict", "RT2151_5_verdict", "VAL2151_OVERALL"],
            "source-owner and Hamiltonian denominator gate still unsigned.",
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


def signature_spine_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="PAS2416_0_domain", clause="parent local ordinary domain", formal_clause="Conf_local^ord={q(Phi),e_obs/g_obs,Psi_A,A_owned,theta_A,tau,boundary data}; Gamma_ind is not an argument", current_status="PRIVATE_CANDIDATE_NOT_PUBLICLY_DERIVED", effect_if_signed="activates variable-absence no-Gamma theorem", missing_to_claim="derive/adopt as active parent theory, not just branch notation"),
        base_row(row_id="PAS2416_1_action_form", clause="minimal owned-coframe matter action", formal_clause="S_ord=sum_A int mu_obs L_A(j^k Psi_A,e_obs,omega_LC[e_obs],A_owned,theta_A)", current_status="WRITTEN_PRIOR_PRIVATE_BRANCH", effect_if_signed="ordinary matter and spin variations belong to coframe/Hilbert stress, not independent Gamma", missing_to_claim="global sector inventory and spin/torsion counterbranch exclusion"),
        base_row(row_id="PAS2416_2_no_independent_gamma", clause="no independent affine connection slot", formal_clause="delta S_ord/delta Gamma_ind=0 by variable absence", current_status="EXACT_CONDITIONAL_LEMMA", effect_if_signed="Delta_matter+Delta_spin/source-readout Gamma parts can collapse by sector", missing_to_claim="sector-sum proof across matter, source, readout, boundary, projective"),
        base_row(row_id="PAS2416_3_source_blind_MUMC", clause="minimal universal matter coupling/source-blind functor", formal_clause="no species/source-only gravitational weights w_A; theta_A may encode non-gravitational constants only", current_status="PRIVATE_RESTRICTION_READY_NOT_DERIVED", effect_if_signed="blocks source-only species slot and relative source-weight countermodels", missing_to_claim="deeper quotient/Noether source-charge derivation"),
        base_row(row_id="PAS2416_4_srng_readout", clause="source/readout no-Gamma", formal_clause="source selectors, clocks, light and orbital readouts are downstream q-natural maps, not parent-action Gamma variables", current_status="PRIVATE_SRNG_LOCKED_NONCLAIM", effect_if_signed="Delta_source=Delta_clock=Delta_light=Delta_orbit=0", missing_to_claim="public downstream observation functor theorem"),
        base_row(row_id="PAS2416_5_spin_connection", clause="coframe-owned spin connection", formal_clause="omega_obs=omega_LC[e_obs] with no omega_ind/Gamma_ind spin branch", current_status="EXACT_CONDITIONAL_NOT_PUBLIC", effect_if_signed="Delta_spin_abs=0 and axial torsion P4 row can close", missing_to_claim="parent spin action signature and counterbranch exclusion"),
        base_row(row_id="PAS2416_6_projective_trace", clause="projective trace", formal_clause="owned-coframe/no-Gamma branch has no physical projective variable; affine branch must be gauge-fixed or bounded", current_status="PRIVATE_ZERO_PUBLIC_FALLBACK", effect_if_signed="Delta_projective_private=0; public P_projective_abs closes only with all-sector invariance", missing_to_claim="all-sector projective invariance or source-backed projective row"),
        base_row(row_id="PAS2416_7_boundary_owner", clause="boundary/improvement object language", formal_clause="theta_MTS,Q_tau,H_tau,H_ref,M_H_ref,boundary class and improvement currents fixed before readout", current_status="MISSING_PRIMARY_LEAK", effect_if_signed="epsilon_boundary_abs can be zero/bounded in same frame", missing_to_claim="parent charge extraction and boundary object exhaustion"),
        base_row(row_id="PAS2416_8_source_owner", clause="source/Hamiltonian owner", formal_clause="L_X,Theta_X,Q_X,J_X,tau_source=tau_charge=tau_clock=tau_readout,M_H_ref are owned by one parent action", current_status="MISSING_SOURCE_OWNER", effect_if_signed="Newton source normalization and local GR bridge can be attempted without orbital-GM circularity", missing_to_claim="source-owner/FB5540 gate from 2151"),
        base_row(row_id="PAS2416_9_verdict", clause="public parent signature activation", formal_clause="activate PAS2416_0 through PAS2416_8 together", current_status="FAIL_CURRENT_PUBLIC_ACTIVATION", effect_if_signed="conditional no-Gamma/LC/spin/projective lemmas become parent-structure steps", missing_to_claim="boundary/source-owner plus deeper MUMC derivation/adoption decision"),
    ]


def activation_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="ACT2416_0_variable_absence", theorem="delta S/delta Gamma_ind=0 when Gamma_ind absent", activation_requirement="PAS2416_0/PAS2416_2 parent-signed", current_activation="CONDITIONAL_ONLY", public_effect="no public no-Gamma theorem yet"),
        base_row(row_id="ACT2416_1_Kconn_LC", theorem="K_conn_norm=0 in metric/coframe-only LC branch", activation_requirement="no independent Gamma plus no boundary/projective/source leakage", current_activation="CONDITIONAL_ONLY", public_effect="Kconn zero remains nonclaim"),
        base_row(row_id="ACT2416_2_source_blind", theorem="NoSourceOnlySpeciesSlot", activation_requirement="MUMC/source-blind functor active in parent theory", current_activation="PRIVATE_RESTRICTION_ONLY", public_effect="source-weight countermodel not publicly closed"),
        base_row(row_id="ACT2416_3_SRNG", theorem="Delta_source/clock/light/orbit=0", activation_requirement="public downstream q-natural source/readout theorem", current_activation="PRIVATE_SRNG_ONLY", public_effect="public source/readout residual rows remain live"),
        base_row(row_id="ACT2416_4_spin", theorem="Delta_spin_abs=0", activation_requirement="omega_obs=omega_LC[e_obs] parent-signed and torsionful counterbranch excluded", current_activation="CONDITIONAL_ONLY", public_effect="axial torsion P4 row retained"),
        base_row(row_id="ACT2416_5_projective", theorem="projective trace silent", activation_requirement="owned-coframe/no-Gamma plus all-sector projective invariance", current_activation="PRIVATE_ZERO_ONLY", public_effect="P_projective_abs retained"),
        base_row(row_id="ACT2416_6_boundary", theorem="epsilon_boundary_abs=0", activation_requirement="theta/Q_tau/H_tau/H_ref/M_H_ref and boundary object exhaustion", current_activation="NOT_ACTIVE", public_effect="primary private-branch leak retained"),
        base_row(row_id="ACT2416_7_Newton_GR", theorem="local GR/Newton reduction", activation_requirement="all above plus rank-zero source-current identity and source normalization", current_activation="BLOCKED", public_effect="no public local-GR/Newton claim"),
    ]


def route_split_rows() -> list[dict[str, Any]]:
    return [
        base_row(route_id="ROUTE2416_0_private_adoption", route="adopt parent action signature as private working branch", status="USEFUL_NONCLAIM", benefit="lets derivation proceed without smuggling GR", risk="private adoption is not derivation", next_step="keep claim flags false and track residuals"),
        base_row(route_id="ROUTE2416_1_deeper_derivation", route="derive MUMC/source-blind signature from quotient/Noether source-charge identity", status="BEST_PUBLIC_ROUTE_NOT_CLOSED", benefit="would make the no-Gamma sector sum much harder to dismiss", risk="requires real source-charge theorem, not wording", next_step="target parent source/current owner and Noether identity"),
        base_row(route_id="ROUTE2416_2_boundary_charge", route="derive theta/Q_tau/H_tau/H_ref/M_H_ref owner", status="PRIMARY_GR_NEWTONGATE", benefit="attacks the surviving boundary/source normalization leak", risk="cannot borrow EH/Newton mass denominator", next_step="parallel 2416b/2417 boundary charge extraction"),
        base_row(route_id="ROUTE2416_3_p4_fallback", route="retain P4/FB5540 residual source pack", status="HONEST_FALLBACK", benefit="keeps local tests possible if theorem route stalls", risk="not evidence until numeric, sourced and same-frame", next_step="source rows only after theorem attempt"),
        base_row(route_id="ROUTE2416_4_verdict", route="combined route choice", status="DUAL_TRACK_THEORY_FIRST", benefit="write parent signature spine while immediately attacking boundary/source-owner gate", risk="overclaim if private branch is exported", next_step="2417 boundary/source-owner public activation gate"),
    ]


def residual_stack_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="RES2416_0_public_total", quantity="Delta_abs_public", formula="||Delta_matter||+||Delta_spin||+||Delta_source||+||Delta_clock||+||Delta_light||+||Delta_orbit||+||Delta_boundary||+||Delta_projective||", status="LIVE_NONCLAIM", score_ready=False),
        base_row(row_id="RES2416_1_private_signature_guard", quantity="parent_signature_guard", formula="I_not_parent_signed(PAS2416_0..PAS2416_8)", status="LIVE_UNTIL_PUBLIC_ACTIVATION", score_ready=False),
        base_row(row_id="RES2416_2_private_connection", quantity="epsilon_private_connection_abs", formula="epsilon_boundary_abs+parent_signature_guard+source_current_guard+Khat_improvement_guard", status="NARROWED_NOT_CLOSED", score_ready=False),
        base_row(row_id="RES2416_3_boundary", quantity="epsilon_boundary_abs", formula="abs(B_zero_flux)/M_H_ref+abs(Delta_symp)/M_H_ref+abs(R_eq)/M_H_ref+abs(I_commutator)+abs(worldtube_domain)+abs(corner)+abs(K_improvement)", status="PRIMARY_LEAK_INPUTS_MISSING", score_ready=False),
        base_row(row_id="RES2416_4_source_owner", quantity="FB5540_source_owner_pack", formula="(||delta_H_tau_nonintegrable||+||Delta_ref||+||Delta_symp||+||boundary_flux||+||bulk_X||+||edge_X||)/M_H_ref", status="SOURCE_OWNER_INPUTS_MISSING", score_ready=False),
        base_row(row_id="RES2416_5_no_cancellation", quantity="policy", formula="no cancellation credit between private adoption, boundary, source-owner, projective or spin residuals without parent-signed identity", status="GUARD_READY", score_ready=False),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2416_0_signature_written", gate="parent action signature spine written", passed=True, claim_effect="candidate contract exists"),
        base_row(gate_id="CG2416_1_signature_publicly_derived", gate="signature derived from deeper MTS primitives", passed=False, claim_effect="private adoption cannot be public proof"),
        base_row(gate_id="CG2416_2_noGamma_sector_sum_public", gate="no-Gamma sector sum public", passed=False, claim_effect="Delta_abs_public remains live"),
        base_row(gate_id="CG2416_3_boundary_owner", gate="boundary charge/source owner closed", passed=False, claim_effect="epsilon_boundary_abs retained"),
        base_row(gate_id="CG2416_4_MHref_source_normalization", gate="M_H_ref/source normalization parent-owned", passed=False, claim_effect="Newton source bridge blocked"),
        base_row(gate_id="CG2416_5_p4_score_ready", gate="P4/FB5540 stack numeric and sourced", passed=False, claim_effect="not empirical evidence"),
        base_row(gate_id="CG2416_6_local_GR_Newton", gate="local GR/Newton reduction derived", passed=False, claim_effect="blocked by public signature and boundary/source-owner gates"),
        base_row(gate_id="CG2416_7_R10_reopen", gate="R10/fifth-force branch reopened", passed=False, claim_effect="strict branch remains rank-zero unless a real operator is sourced"),
        base_row(gate_id="CG2416_8_GitHub", gate="public/GitHub update", passed=False, claim_effect="private checkpoint only"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2416_0_result", decision="PARENT_SIGNATURE_SPINE_WRITTEN_AS_NONCLAIM", rationale="the exact contract is now visible in one place", consequence="conditional zero lemmas have a clear activation target"),
        base_row(decision_id="DEC2416_1_no_overclaim", decision="DO_NOT_TREAT_PRIVATE_ADOPTION_AS_DERIVATION", rationale="2330 already showed deeper quotient derivation is not closed", consequence="public local-GR claim remains blocked"),
        base_row(decision_id="DEC2416_2_best_next", decision="BOUNDARY_SOURCE_OWNER_GATE_NEXT", rationale="even if the private signature is used, boundary/improvement and M_H_ref/source normalization survive", consequence="attack theta/Q_tau/H_tau/H_ref plus source-current owner"),
        base_row(decision_id="DEC2416_3_fallback", decision="KEEP_P4_FB5540_STACK", rationale="if public signature or boundary theorem fails, residual rows must be numeric and source-backed", consequence="no cancellation or fitted-GM shortcut"),
        base_row(decision_id="DEC2416_4_public_policy", decision="NO_GITHUB_NO_LOCAL_PASS", rationale="stronger spine but no public derivation yet", consequence="continue private derivation work"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2416_0_selected",
            selection_status="selected",
            target_file="2417-Y5-R2FR-boundary-source-owner-public-activation-gate.md",
            target_script="scripts/Y5_R2FR_boundary_source_owner_public_activation_gate_2417.py",
            objective="try to close the surviving boundary/source-owner gate: theta_MTS, Q_tau, H_tau, H_ref, M_H_ref, L_X/Theta_X/Q_X, tau lock, and source-current equality",
            success_condition="either boundary/source-owner clauses are parent-signed and compatible with the parent signature spine, or the FB5540/P4 source pack is explicit and nonclaim",
            do_not_do="do not import EH/Newton mass denominators, orbital GM, private SRNG, or LC/geodesics as public proof",
        ),
        base_row(
            route_id="NEXT2416_1_parallel",
            selection_status="held_parallel",
            target_file="2417b-Y5-R2FR-deeper-quotient-to-MUMC-or-source-blind-counterrow.md",
            target_script="scripts/Y5_R2FR_deeper_quotient_to_MUMC_or_source_blind_counterrow_2417b.py",
            objective="continue the purist derivation of Minimal Universal Matter Coupling/source-blind functor from quotient/Noether source-charge primitives",
            success_condition="derive the source-blind signature without adoption, or keep the private restriction clearly labelled and stage countermodel/fallback rows",
            do_not_do="do not call private MUMC adoption a public derivation",
        ),
    ]


def copy_branch_rows(signature: list[dict[str, Any]], residual: list[dict[str, Any]], decision: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["signature_spine"], BRANCH_COPIES["queue"], signature),
        ("branch_wep", OUTPUTS["residual_stack"], BRANCH_COPIES["branch_wep"], residual),
        ("beta_docs", OUTPUTS["decision"], BRANCH_COPIES["beta_docs"], decision),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, source_rows in copy_specs:
        write_csv(target_path, source_rows)
        parse_ok, row_count, parse_detail = csv_rows_parse(target_path)
        rows.append(base_row(copy_id=copy_id, source_path=str(source_path), target_path=str(target_path), copied=target_path.exists(), parse_ok=parse_ok, row_count=row_count, parse_detail=parse_detail))
    return rows


def all_generated_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, value in data.items():
        if key != "validation":
            rows.extend(value)
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    sources = data["source_register"]
    rows.append(base_row(validation_id="VAL2416_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['path_exists'])}/{len(sources)} sources exist"))
    rows.append(base_row(validation_id="VAL2416_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['needles_found'])}/{len(sources)} source needle sets found"))

    signature_text = " ".join(str(row) for row in data["signature_spine"])
    required_clauses = ["no independent affine connection", "minimal universal matter coupling", "source/readout no-Gamma", "boundary/improvement object language", "source/Hamiltonian owner"]
    rows.append(base_row(validation_id="VAL2416_02_signature_clauses", status="PASS" if all(clause in signature_text for clause in required_clauses) else "FAIL", detail="parent signature spine covers no-Gamma, MUMC, SRNG, boundary and source-owner clauses"))
    rows.append(base_row(validation_id="VAL2416_03_public_activation_blocked", status="PASS" if "FAIL_CURRENT_PUBLIC_ACTIVATION" in signature_text and "MISSING_PRIMARY_LEAK" in signature_text else "FAIL", detail="public activation remains blocked by boundary/source-owner gaps"))

    activation_text = " ".join(str(row) for row in data["activation"])
    rows.append(base_row(validation_id="VAL2416_04_activation_matrix", status="PASS" if "PRIVATE_SRNG_ONLY" in activation_text and "NOT_ACTIVE" in activation_text and "BLOCKED" in activation_text else "FAIL", detail="conditional/private theorem activation states recorded"))

    route_text = " ".join(str(row) for row in data["route_split"])
    rows.append(base_row(validation_id="VAL2416_05_route_split", status="PASS" if "PRIVATE_RESTRICTION_ONLY" not in route_text and "PRIMARY_GR_NEWTONGATE" in route_text and "BEST_PUBLIC_ROUTE_NOT_CLOSED" in route_text else "FAIL", detail="adoption/derivation/boundary/fallback route split recorded"))

    residual_text = " ".join(str(row) for row in data["residual_stack"])
    rows.append(base_row(validation_id="VAL2416_06_residual_stack", status="PASS" if "Delta_abs_public" in residual_text and "epsilon_boundary_abs" in residual_text and "FB5540_source_owner_pack" in residual_text else "FAIL", detail="public/private residual stack retained after signature attempt"))
    rows.append(base_row(validation_id="VAL2416_07_residual_nonready", status="PASS" if all(not row["score_ready"] for row in data["residual_stack"]) else "FAIL", detail="residual stack remains non-score-ready"))

    claim_gate_map = {row["gate_id"]: row for row in data["claim_gates"]}
    blocked_ids = ["CG2416_1_signature_publicly_derived", "CG2416_2_noGamma_sector_sum_public", "CG2416_3_boundary_owner", "CG2416_4_MHref_source_normalization", "CG2416_6_local_GR_Newton", "CG2416_7_R10_reopen", "CG2416_8_GitHub"]
    rows.append(base_row(validation_id="VAL2416_08_claim_gates", status="PASS" if all(not claim_gate_map[row_id]["passed"] for row_id in blocked_ids) else "FAIL", detail="public/local/R10/GitHub claims blocked"))

    next_text = " ".join(str(row) for row in data["next_target"])
    rows.append(base_row(validation_id="VAL2416_09_next_target", status="PASS" if "2417-Y5-R2FR-boundary-source-owner-public-activation-gate.md" in next_text else "FAIL", detail="boundary/source-owner public activation gate selected next"))

    csv_ok = True
    details: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parse_ok, row_count, parse_detail = csv_rows_parse(path)
        csv_ok = csv_ok and parse_ok and row_count > 0
        details.append(f"{path.name}:{row_count}:{parse_detail}")
    rows.append(base_row(validation_id="VAL2416_10_csv_parse", status="PASS" if csv_ok else "FAIL", detail="; ".join(details)))

    copies = data["branch_copies"]
    rows.append(base_row(validation_id="VAL2416_11_branch_copies", status="PASS" if all(row["copied"] and row["parse_ok"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    generated = all_generated_rows(data)
    rows.append(base_row(validation_id="VAL2416_12_no_claim_flags", status="PASS" if all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in generated) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))
    rows.append(base_row(validation_id="VAL2416_13_formalization_untouched_by_outputs", status="PASS" if not formalization_has_2416_artifacts() else "FAIL", detail="script outputs stay inside post-checkpoint-work"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(base_row(validation_id="VAL2416_OVERALL", status=overall, detail="2416 writes the parent ordinary action variable-signature spine as a nonclaim contract, refuses private-adoption/public-derivation confusion, keeps residual stacks live, and selects boundary/source-owner activation next"))
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    overall = next(row for row in data["validation"] if row["validation_id"] == "VAL2416_OVERALL")
    lines = [
        "# 2416 - Y5/R2FR Parent Ordinary Action Variable Signature Spine",
        "",
        "## Result",
        "",
        "2416 writes the parent-action spine we have been circling, but it does **not** pretend the spine is publicly derived.",
        "",
        "The candidate contract is clean: ordinary local matter lives on observed quotient/coframe data, uses `omega_LC[e_obs]` as a dependent coframe object, carries no independent `Gamma_ind` action argument, has no source-only gravitational species weights, and treats source/readout maps as downstream in the private SRNG/OFC branch.",
        "",
        "If that whole contract were parent-signed, several conditional lemmas would snap into place: no-Gamma, `K_conn_norm=0`, coframe-owned spin, source/readout silence, and private projective silence. But current evidence still leaves two public blockers: the contract is a private/adopted branch rather than a deeper derivation, and boundary/source-owner objects (`theta_MTS`, `Q_tau`, `H_tau`, `H_ref`, `M_H_ref`, `L_X/Theta_X/Q_X`) are not closed.",
        "",
        "So this checkpoint improves the framework without overclaiming it: private signature branch allowed, public local-GR/Newton claim blocked, residual stack retained.",
        "",
        "## Source Register",
        "",
        md_table(data["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Parent Action Signature Spine",
        "",
        md_table(data["signature_spine"], ["row_id", "clause", "formal_clause", "current_status", "effect_if_signed", "missing_to_claim", "valid_for_claim"]),
        "",
        "## Theorem Activation Matrix",
        "",
        md_table(data["activation"], ["row_id", "theorem", "activation_requirement", "current_activation", "public_effect", "valid_for_claim"]),
        "",
        "## Adoption Derivation Fallback Route Split",
        "",
        md_table(data["route_split"], ["route_id", "route", "status", "benefit", "risk", "next_step", "valid_for_claim"]),
        "",
        "## Residual Stack After Signature Attempt",
        "",
        md_table(data["residual_stack"], ["row_id", "quantity", "formula", "status", "score_ready", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(data["claim_gates"], ["gate_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(data["decision"], ["decision_id", "decision", "rationale", "consequence", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(data["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(data["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(data["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Practical Status",
        "",
        "This is a real spine, but still private steel rather than public armor. The next best strike is the boundary/source-owner public activation gate: if that closes, the private LC/no-Gamma branch gets much closer to a defensible GR/Newton reduction; if it fails, the FB5540/P4 residual pack is already staged.",
        "",
        f"Validation overall: `{overall['status']}`.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    BETA_DOCS.mkdir(parents=True, exist_ok=True)

    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "signature_spine": signature_spine_rows(),
        "activation": activation_rows(),
        "route_split": route_split_rows(),
        "residual_stack": residual_stack_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["source_register"])
    write_csv(OUTPUTS["signature_spine"], data["signature_spine"])
    write_csv(OUTPUTS["activation"], data["activation"])
    write_csv(OUTPUTS["route_split"], data["route_split"])
    write_csv(OUTPUTS["residual_stack"], data["residual_stack"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision"], data["decision"])
    write_csv(OUTPUTS["next_target"], data["next_target"])

    data["branch_copies"] = copy_branch_rows(data["signature_spine"], data["residual_stack"], data["decision"])
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

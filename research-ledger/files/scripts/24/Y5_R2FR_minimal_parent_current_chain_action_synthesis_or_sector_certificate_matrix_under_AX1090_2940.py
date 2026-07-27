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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2940"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2940-Y5-R2FR-minimal-parent-current-chain-action-synthesis-or-sector-certificate-matrix-under-AX1090.md"

SRC_2939_DOC = ROOT / "2939-Y5-R2FR-parent-Noether-theta-Qtau-extraction-or-source-measure-closure-axiom-under-AX1090.md"
SRC_2939_NOETHER = RESIDUALS / "P8_Y5_R2FR_2939_PARENT_NOETHER_EXTRACTION_ATTEMPT.csv"
SRC_2939_SECTORS = RESIDUALS / "P8_Y5_R2FR_2939_THETA_QTAU_SECTOR_CERTIFICATE_LEDGER.csv"
SRC_2939_CTAU = RESIDUALS / "P8_Y5_R2FR_2939_CTAU_RESIDUAL_DECOMPOSITION.csv"
SRC_2939_NEXT = RESIDUALS / "P8_Y5_R2FR_2939_NEXT_TARGET.csv"
SRC_2908 = RESIDUALS / "P8_Y5_R2FR_2908_PARENT_ACTION_SKELETON.csv"
SRC_2866 = RESIDUALS / "P8_Y5_R2FR_2866_MINIMAL_PARENT_ACTION_CONTRACT.csv"
SRC_2749 = RESIDUALS / "P8_Y5_R2FR_2749_MINIMAL_ACTION_ANSATZ_REGISTER.csv"
SRC_2798_PACK = RESIDUALS / "P8_Y5_R2FR_2798_MINIMAL_SECTOR_CERTIFICATE_PACK.csv"
SRC_2798_RUNNER = RESIDUALS / "P8_Y5_R2FR_2798_SECTOR_CERTIFICATE_RUNNER.csv"
SRC_2922 = RESIDUALS / "P8_Y5_R2FR_2922_HAMILTONIAN_SECTOR_OWNER_AUDIT.csv"
SRC_2925 = RESIDUALS / "P8_Y5_R2FR_2925_EXTRA_SECTOR_SILENCE_AUDIT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2940_SOURCE_REGISTER.csv",
    "synthesis": RESIDUALS / "P8_Y5_R2FR_2940_MINIMAL_PARENT_ACTION_SYNTHESIS_ATTEMPT.csv",
    "sectors": RESIDUALS / "P8_Y5_R2FR_2940_SECTOR_CERTIFICATE_MATRIX.csv",
    "adoption": RESIDUALS / "P8_Y5_R2FR_2940_ACTION_ADOPTION_GATE.csv",
    "ladder": RESIDUALS / "P8_Y5_R2FR_2940_LOCAL_GR_NEWTON_DERIVATION_LADDER.csv",
    "residuals": RESIDUALS / "P8_Y5_R2FR_2940_RESIDUAL_OR_CLOSURE_LEDGER.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2940_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2940_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2940_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2940_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2940_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "synthesis_copy": PARENT_ACTION / "Minimal_parent_current_chain_action_synthesis_2940_NONCLAIM.csv",
    "sector_copy": PARENT_ACTION / "Sector_certificate_matrix_2940_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2940_GK_ACTION_EXISTENCE_OR_PARENT_ACTION_ADOPTION_NEXT_NONCLAIM.csv",
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
        ("SRC2940_00_2939_doc", SRC_2939_DOC, "parent action synthesis;Validation overall: `True`", "2939 handoff and claim ceiling"),
        ("SRC2940_01_2939_noether", SRC_2939_NOETHER, "PNE2939_0_master_formula;PNE2939_6_verdict", "conditional Noether formula and refusal"),
        ("SRC2940_02_2939_sectors", SRC_2939_SECTORS, "SEC2939_3_extra_GK;SEC2939_10_total", "theta/Q_tau sector certificate failures"),
        ("SRC2940_03_2939_ctau", SRC_2939_CTAU, "CTA2939_0_master;CTA2939_8_C_units", "C_tau residual decomposition"),
        ("SRC2940_04_2939_next", SRC_2939_NEXT, "NEXT2939_0_2940", "machine-readable 2940 target"),
        ("SRC2940_05_2908_skeleton", SRC_2908, "ACT2908_2_vertical_generator_current_law;ACT2908_7_total_verdict", "latest parent action skeleton"),
        ("SRC2940_06_2866_contract", SRC_2866, "PACT2866_3_action;PACT2866_9_acceptance", "minimal parent action contract clauses"),
        ("SRC2940_07_2749_ansatz", SRC_2749, "ANS2749_A_EH_lambdaR_silent;FORBIDDEN_EH_IMPORT_AS_MTS_DERIVATION", "minimal action ansatz register"),
        ("SRC2940_08_2798_pack", SRC_2798_PACK, "SEC2798_3_Gamma_Khat_q_loc;HARDEST_BLOCKER", "sector certificate pack"),
        ("SRC2940_09_2798_runner", SRC_2798_RUNNER, "SCR2798_loc;HARDEST_BLOCKER", "sector certificate runner"),
        ("SRC2940_10_2922_hamiltonian", SRC_2922, "HOA2922_2_Theta_Q_owner;HOA2922_9_RAB_or_qRhat", "Hamiltonian/source-mass owner audit"),
        ("SRC2940_11_2925_silence", SRC_2925, "XSI2925_3_GK_double_zero;XSI2925_8_total", "extra-sector silence audit"),
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


def synthesis_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "synthesis_id": "SYN2940_0_total_spine",
            "action_block": "S_parent_min",
            "candidate_statement": "S_parent^min = S_EH[g_obs;kappa0,Lambda0] + S_matter[psi,g_obs] + S_kappa_top[kappa_eff,A3] + S_GK[A_mu,Gamma_eff,Khat,Phi,J_M] + S_PiM_worldtube[Pi_M,J_H,W] + S_boundary_ref[B_ref,tau,S] + S_silent_aux[Z^A]",
            "conditional_derives": "If all sectors are parent-signed, the same parent action supplies theta_MTS, Q_tau^MTS, C_tau, source mass, Newton limit and local residual rows.",
            "current_status": "CONDITIONAL_RESEARCH_SPINE_NOT_ADOPTED",
            "blocking_gap": "GK action existence, Pi_M/worldtube source glue, fixed reference/tau lock, extra-sector silence and matter descent are not jointly signed.",
            "adopt_now": False,
            "source_paths": f"{SRC_2939_NOETHER};{SRC_2908};{SRC_2866};{SRC_2749}",
        },
        {
            "synthesis_id": "SYN2940_1_EH_core",
            "action_block": "S_EH[g_obs]",
            "candidate_statement": "Use the Einstein-Hilbert observed metric/coframe sector only as the local spin-2 comparator and as a future reducible limit.",
            "conditional_derives": "Known GR Noether charge and weak-field beta/gamma after MTS-to-EH reduction is independently signed.",
            "current_status": "REFERENCE_ANCHOR_ONLY",
            "blocking_gap": "EH-only import would prove the target by assuming it; MTS reduction and silent sectors remain unsigned.",
            "adopt_now": False,
            "source_paths": f"{SRC_2749};{SRC_2798_PACK}",
        },
        {
            "synthesis_id": "SYN2940_2_universal_matter",
            "action_block": "S_matter[psi,g_obs]",
            "candidate_statement": "One universal matter action must supply both Hilbert stress and source current with no species/source-only prefactor.",
            "conditional_derives": "WEP/Newton source normalization if matter descent, same coframe and no-marker boundary clauses pass.",
            "current_status": "CONDITIONAL_STANDARD_FORM_UNSIGNED",
            "blocking_gap": "same-action Hilbert current and worldtube source-measure glue are not parent-derived.",
            "adopt_now": False,
            "source_paths": f"{SRC_2908};{SRC_2939_SECTORS}",
        },
        {
            "synthesis_id": "SYN2940_3_kappa_topological",
            "action_block": "S_kappa_top[kappa_eff,A3]",
            "candidate_statement": "Promote constant coupling by a topological or constraint sector only if d(kappa_eff)=0 before readout.",
            "conditional_derives": "No local coupling drift in Newton/R10/dotG channels.",
            "current_status": "CANDIDATE_NOT_ADOPTED",
            "blocking_gap": "constant-kappa owner is not parent-signed and cannot be used as a numeric coupling claim.",
            "adopt_now": False,
            "source_paths": f"{SRC_2939_SECTORS};{SRC_2925}",
        },
        {
            "synthesis_id": "SYN2940_4_GK_current_law",
            "action_block": "S_GK[A_mu,Gamma_eff,Khat,Phi,J_M]",
            "candidate_statement": "Use a Helmholtz-compatible current-law sector whose A_mu variation gives P_loc(nabla^nu Gamma_eff - nabla_mu Khat^{mu nu} - J_M^nu)=0.",
            "conditional_derives": "q_loc suppression, extra-sector C_tau row and the local-GR residual vector if stress, boundary and source terms close.",
            "current_status": "PRIMARY_HARDEST_BLOCKER",
            "blocking_gap": "A_mu, L_K, L_Gamma, J_M, P_loc and boundary no-flux remain formal parent material.",
            "adopt_now": False,
            "source_paths": f"{SRC_2908};{SRC_2798_PACK};{SRC_2925}",
        },
        {
            "synthesis_id": "SYN2940_5_PiM_worldtube",
            "action_block": "S_PiM_worldtube[Pi_M,J_H,W]",
            "candidate_statement": "The mass projector and worldtube source measure must be derived as a parent current/charge object, not fitted from orbital GM.",
            "conditional_derives": "M_source[W] = H_tau[S_outer] - H_ref and therefore a noncircular Newton denominator.",
            "current_status": "PARALLEL_CORE_BLOCKER",
            "blocking_gap": "Pi_M parent origin, projector stress, commutator silence and compact support/source-charge closure are unsigned.",
            "adopt_now": False,
            "source_paths": f"{SRC_2939_CTAU};{SRC_2922}",
        },
        {
            "synthesis_id": "SYN2940_6_boundary_reference",
            "action_block": "S_boundary_ref[B_ref,tau,S]",
            "candidate_statement": "Fix boundary terms, reference subtraction, time generator and linked surfaces before any source/orbit/readout comparison.",
            "conditional_derives": "Hamiltonian integrability and source-blind M_H_ref if no boundary/corner improvement retuning remains.",
            "current_status": "REQUIRED_OPEN",
            "blocking_gap": "fixed H_ref, same-frame tau and boundary no-flux certificates remain unsigned.",
            "adopt_now": False,
            "source_paths": f"{SRC_2939_CTAU};{SRC_2922}",
        },
        {
            "synthesis_id": "SYN2940_7_silent_aux",
            "action_block": "S_silent_aux[Z^A]",
            "candidate_statement": "Extra motion/time/domain/memory variables must be either first-class/vertical, topological, or positive double-zero residuals with no observable stress hair.",
            "conditional_derives": "No local PPN/R10 pollution if DqZ, metric stress and source-current couplings vanish or are bounded.",
            "current_status": "SILENCE_NOT_PROVED",
            "blocking_gap": "Dq map, vertical kernel, stress silence, disformal no-slot and double-zero theorem are not closed.",
            "adopt_now": False,
            "source_paths": f"{SRC_2925};{SRC_2798_PACK}",
        },
        {
            "synthesis_id": "SYN2940_8_verdict",
            "action_block": "adoption verdict",
            "candidate_statement": "The minimal parent current-chain action is now written as a finite spine, but it is not yet a derived MTS action.",
            "conditional_derives": "A finite proof programme and next target selection.",
            "current_status": "SYNTHESIS_USEFUL_ADOPTION_REFUSED",
            "blocking_gap": "sector certificates fail; promote only after each action block has field content, variation, theta/Q_tau, stress and boundary/source clauses.",
            "adopt_now": False,
            "source_paths": f"{SRC_2939_NEXT};{SRC_2798_RUNNER}",
        },
    ]
    return [add_common(row) for row in rows]


def sector_rows() -> list[dict[str, Any]]:
    rows = [
        ("SEC2940_0_EH_core", "EH/local spin-2 core", "g_obs, coframe, tau", "variation gives Einstein tensor plus fixed subtraction", "Theta_EH and Q_tau^EH only after MTS-to-EH reduction", "known GR template cannot be total MTS proof", "REFERENCE_ANCHOR_ONLY", False, "MTS-to-EH reduction and silent-sector no-hair"),
        ("SEC2940_1_matter", "universal matter/source", "psi, g_obs/coframe", "Hilbert stress and source current from one S_matter", "matter Noether/source contribution", "same-action source normalization", "UNSIGNED_MATTER_DESCENT", False, "matter descent and no source-only prefactor"),
        ("SEC2940_2_kappa", "constant coupling", "kappa_eff plus topological/constraint owner", "d(kappa_eff)=0 before readout", "no local Q_tau drift or source label", "dotG/R10/Newton coupling lock", "CANDIDATE_NOT_ADOPTED", False, "parent topological owner absent"),
        ("SEC2940_3_GK_q_loc", "Gamma/Khat/q_loc", "A_mu, Gamma_eff, Khat, Phi, P_loc, J_M", "Euler/Helmholtz equation for q_loc current", "Theta_X, Q_tau^X, C_tau^X", "extra stress/source residual zero or bounded", "PRIMARY_HARDEST_BLOCKER", False, "action existence and first variation not proved"),
        ("SEC2940_4_PiM", "Pi_M/source projector", "Pi_M, J_H, symplectic projector data", "delta(Pi_M J_H) controlled", "projector current contribution", "commutator and projector stress zero/bounded", "PARALLEL_SOURCE_BLOCKER", False, "Pi_M parent origin not derived"),
        ("SEC2940_5_worldtube", "worldtube source glue", "compact worldtube W, source surface S", "source charge equals exterior Hamiltonian flux", "Q_M[tau] surface form", "noncircular mass denominator", "CORE_MASS_BLOCKER", False, "M_source-H_tau-H_ref identity not signed"),
        ("SEC2940_6_boundary_ref", "boundary/reference", "B_ref, corner class, linked surfaces", "fixed variation and no readout retuning", "boundary Q_tau/improvement term", "source-blind H_ref", "REFERENCE_BLOCKER", False, "fixed reference and boundary flux not signed"),
        ("SEC2940_7_tau_frame", "tau/surface/frame", "tau_source=tau_charge=tau_clock=tau_readout", "same generator in all sectors", "same-frame Hamiltonian charge", "clock/orbit/R10 readout lock", "SAME_FRAME_LOCK_MISSING", False, "tau/surface lock not derived"),
        ("SEC2940_8_silent_aux", "silent/auxiliary extra sector", "Z^A, quotient map q, Dq kernel", "first-class/topological/double-zero branch", "zero or exact Q_tau contribution", "no PPN/R10/stress hair", "EXTRA_SECTOR_SILENCE_NOT_PROVED", False, "DqZ and double-zero theorem unsigned"),
        ("SEC2940_9_total", "total parent action", "all above sectors", "all variations before readout", "theta_MTS and Q_tau^MTS", "Bianchi/conservation/source closure", "PARENT_CERTIFICATE_FAILED", False, "at least one critical sector fails; in fact several do"),
    ]
    return [
        add_common(
            {
                "sector_id": sector_id,
                "sector": sector,
                "field_list_required": field_list,
                "first_variation_required": variation,
                "theta_qtau_required": theta_qtau,
                "stress_source_required": stress,
                "current_status": status,
                "sector_certificate_passed": passed,
                "primary_gap": gap,
            }
        )
        for sector_id, sector, field_list, variation, theta_qtau, stress, status, passed, gap in rows
    ]


def adoption_rows() -> list[dict[str, Any]]:
    rows = [
        ("AG2940_0_finite_spine_written", "finite candidate parent spine is written", True, False, "passes only as a nonclaim research skeleton"),
        ("AG2940_1_no_EH_smuggling", "EH-only import is explicitly rejected", True, False, "guardrail passes; EH remains reference/comparator only"),
        ("AG2940_2_each_sector_Lagrangian", "each retained sector has parent-owned L_s", False, True, "GK, Pi_M/worldtube, boundary/reference and silent sectors fail"),
        ("AG2940_3_first_variations", "variations produce required Euler/current equations", False, True, "q_loc and source-projector first variations are formal only"),
        ("AG2940_4_theta_qtau", "theta_MTS and Q_tau^MTS extracted from total action", False, True, "2939 formula exact but not applied to a signed action"),
        ("AG2940_5_stress_bianchi", "extra stresses conserve and satisfy Bianchi/source identities", False, True, "extra-sector silence and matter/source descent not proved"),
        ("AG2940_6_boundary_reference", "boundary/reference/tau surfaces fixed before readout", False, True, "H_ref and same-frame tau lock not signed"),
        ("AG2940_7_source_mass", "worldtube source charge gives M_H_ref without orbital GM import", False, True, "source-measure glue remains conditional"),
        ("AG2940_8_total_adoption", "promote S_parent_min as current MTS parent action", False, True, "adoption refused until all certificate rows pass"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "gate": gate,
                "gate_passed": passed,
                "blocks_adoption": blocks,
                "reason": reason,
            }
        )
        for gate_id, gate, passed, blocks, reason in rows
    ]


def ladder_rows() -> list[dict[str, Any]]:
    rows = [
        ("LAD2940_0_parent_action", "write finite parent action spine", "CONDITIONAL_WRITTEN", "S_parent^min row exists but is not adopted", "action synthesis nonclaim"),
        ("LAD2940_1_noether_current", "extract theta_MTS/Q_tau^MTS/C_tau", "BLOCKED", "requires signed sector Lagrangians", "H_tau integrability"),
        ("LAD2940_2_source_measure", "derive M_source[W]=H_tau-H_ref", "BLOCKED", "Pi_M/worldtube/source glue and fixed H_ref missing", "Newton denominator"),
        ("LAD2940_3_newton_gauss", "recover Poisson/Gauss source law", "BLOCKED", "source mass would be circular without LAD2940_2", "Newtonian mechanics"),
        ("LAD2940_4_local_gr_ppn", "show beta=gamma=1 plus bounded residual vector", "BLOCKED", "q_loc/GK and silent-sector stresses not theorem-zero", "local GR/PPN"),
        ("LAD2940_5_r10_clocks_orbits", "project finite residuals into R10, clock and orbital channels", "BLOCKED", "Qbar_XH/tau/M_H_ref rows depend on previous gates", "empirical robustness"),
    ]
    return [
        add_common(
            {
                "ladder_id": ladder_id,
                "derivation_step": step,
                "status": status,
                "why": why,
                "feeds": feeds,
            }
        )
        for ladder_id, step, status, why, feeds in rows
    ]


def residual_rows() -> list[dict[str, Any]]:
    rows = [
        ("RES2940_0_qloc", "q_loc^nu", "P_loc(nabla^nu Gamma_eff - nabla_mu Khat^{mu nu})", "derive S_GK Helmholtz action and boundary no-flux or retain explicit finite residual", "retained, no claim"),
        ("RES2940_1_ctau", "C_tau_total", "C_EH+C_extra+C_projector+C_boundary_ref+C_matter_source+C_tau_surface+C_Dq+C_units", "zero/bound every component in same frame", "retained, no claim"),
        ("RES2940_2_source_mass", "M_H_ref", "G_ref^-1[H_tau-H_ref]", "derive source measure and fixed reference before orbital GM", "blocked denominator"),
        ("RES2940_3_pim", "[d,Pi_M]J_H and delta Pi_M stress", "projector/source commutator", "prove projector silence or bounded stress row", "retained, no claim"),
        ("RES2940_4_extra_silence", "DqZ_geometry and stress hair", "readout leakage from auxiliary/silent sector", "prove vertical/topological/double-zero branch", "retained, no claim"),
        ("RES2940_5_closure_policy", "closure-only parent action axiom", "adopt S_parent^min by axiom", "allowed only as labelled private algebra; not evidence", "not adopted"),
    ]
    return [
        add_common(
            {
                "residual_id": residual_id,
                "object": obj,
                "definition": definition,
                "required_resolution": required,
                "current_policy": policy,
            }
        )
        for residual_id, obj, definition, required, policy in rows
    ]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2940_0_synthesis", "minimal parent action spine synthesized", True, "PASS_CONDITIONAL_NONCLAIM", False),
        ("CG2940_1_adoption", "S_parent^min is adopted as current MTS parent action", False, "BLOCKED_SECTOR_CERTIFICATES", False),
        ("CG2940_2_theta_qtau", "theta_MTS/Q_tau^MTS extracted", False, "BLOCKED_NO_SIGNED_TOTAL_ACTION", False),
        ("CG2940_3_newton", "Newton mechanics derived noncircularly", False, "BLOCKED_SOURCE_MASS_GLUE", False),
        ("CG2940_4_local_gr", "local GR/PPN branch derived", False, "BLOCKED_GK_QLOC_AND_SILENCE", False),
        ("CG2940_5_r10", "R10/local fifth-force pass claimed", False, "BLOCKED_QBAR_TAU_MHREF", False),
        ("CG2940_6_public_claim", "public empirical/local claim allowed from 2940", False, "NO_PUBLIC_CLAIM", False),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "claim_allowed": allowed,
            }
        )
        for gate_id, claim, passed, status, allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2940_0_result", "minimal parent current-chain action spine written but not adopted", "it organizes the finite theory programme without hiding missing sector variations", "use as map, not as proof"),
        ("DEC2940_1_root_bottleneck", "Gamma/Khat/q_loc action existence is the best next target", "sector audits repeatedly mark GK/q_loc as the hardest local-GR blocker", "attempt Helmholtz/Euler action-existence proof next"),
        ("DEC2940_2_parallel_bottleneck", "Pi_M/worldtube source glue remains parallel second target", "even a good GK action will not give Newton without a noncircular mass denominator", "return after GK action gate or if GK route fails"),
        ("DEC2940_3_no_data_runner_yet", "do not run another local empirical scorer as the main step", "R10/PPN/clock rows depend on Qbar/tau/M_H_ref which depend on the parent action chain", "derive first, test after claim rows become numeric and sourced"),
        ("DEC2940_4_closure_policy", "closure-only action axiom remains available but not adopted", "the project goal is derivability; closure would be a labelled branch, not a win", "keep closure rows nonclaim"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "next_action": next_action,
            }
        )
        for decision_id, decision, reason, next_action in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2940_0_2941",
                "priority": "selected_primary",
                "next_doc": "2941-Y5-R2FR-Gamma-Khat-q_loc-action-existence-Helmholtz-or-parent-action-adoption-gate-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_Gamma_Khat_q_loc_action_existence_Helmholtz_or_parent_action_adoption_gate_under_AX1090_2941.py",
                "objective": "Attempt to prove or reject existence of a Helmholtz-compatible Gamma/Khat/q_loc parent action whose variation owns the local residual current; if it fails, keep q_loc as explicit residual and refuse parent-action adoption.",
                "include": "Helmholtz symmetry; Euler operator; A_mu multiplier option; Khat antisymmetric current; P_loc projection; boundary no-flux; stress/Bianchi residual; adoption gate impact",
                "exclude": "R10/local-GR/Newton claim; empirical scoring; EH-only parent import; GitHub action; formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("synthesis_copy", OUTPUTS["synthesis"], BRANCH_OUTPUTS["synthesis_copy"]),
        ("sector_copy", OUTPUTS["sectors"], BRANCH_OUTPUTS["sector_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows = []
    for copy_id, source_path, copy_path in copies:
        if source_path.exists():
            shutil.copyfile(source_path, copy_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "copy_path": str(copy_path),
                    "source_exists": source_path.exists(),
                    "copy_exists": copy_path.exists(),
                }
            )
        )
    return rows


def validation_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_has_2940 = False
    if FORMALIZATION.exists():
        formalization_has_2940 = any(FORMALIZATION.rglob("*2940*"))
    checks = [
        ("VAL2940_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2940_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all source anchors found", True),
        ("VAL2940_2_synthesis_written", OUTPUTS["synthesis"].exists() and any(row.get("synthesis_id") == "SYN2940_0_total_spine" for row in read_csv_rows(OUTPUTS["synthesis"])), "minimal parent action spine row exists", True),
        ("VAL2940_3_adoption_refused", any(row.get("gate_id") == "AG2940_8_total_adoption" and row.get("gate_passed") == "False" for row in read_csv_rows(OUTPUTS["adoption"])), "total parent action adoption refused", True),
        ("VAL2940_4_sector_claims_false", all(row.get("valid_for_claim") == "False" for row in read_csv_rows(OUTPUTS["sectors"])), "all sector certificate rows remain nonclaim", True),
        ("VAL2940_5_claims_blocked", all(row.get("claim_allowed") == "False" for row in read_csv_rows(OUTPUTS["claims"])), "no Newton/local-GR/R10 claim allowed", True),
        ("VAL2940_6_next_target_selected", any(row.get("next_id") == "NEXT2940_0_2941" for row in read_csv_rows(OUTPUTS["next"])), "2941 GK/q_loc action-existence target selected", True),
        ("VAL2940_7_branches_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copy files exist", True),
        ("VAL2940_8_csvs_parse", all(csv_parses(path) for path in generated_csvs), "all generated CSV files parse", True),
        ("VAL2940_9_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2940_10_formalization_clean", not formalization_has_2940, "no 2940 outputs were written to formalization-workbench", True),
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
    rows.append({"validation_id": "VAL2940_OVERALL", "passed": overall, "check": "2940 validation overall", "required": True})
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    synthesis: list[dict[str, Any]],
    sectors: list[dict[str, Any]],
    adoption: list[dict[str, Any]],
    ladder: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation if row["validation_id"] == "VAL2940_OVERALL")["passed"]
    text = f"""# 2940 - Y5 R2FR: minimal parent current-chain action synthesis or sector certificate matrix under AX1090

Status: `Y5_R2FR_2940_minimal_parent_current_chain_spine_synthesized_but_not_adopted_GK_q_loc_action_existence_selected_next`

Claim ceiling: `conditional_parent_spine_yes_current_parent_action_no_theta_Qtau_no_Newton_no_local_GR_no_R10_no_GitHub_claim`

2940 turns the previous Noether/current-chain work into a finite parent-action spine. This is a map, not a victory lap. The candidate action is useful because it names the exact sectors that must vary before readout; it is refused as a current MTS parent action because several sectors still fail certificate gates.

The minimal nonclaim spine is:

`S_parent^min = S_EH[g_obs;kappa0,Lambda0] + S_matter[psi,g_obs] + S_kappa_top[kappa_eff,A3] + S_GK[A_mu,Gamma_eff,Khat,Phi,J_M] + S_PiM_worldtube[Pi_M,J_H,W] + S_boundary_ref[B_ref,tau,S] + S_silent_aux[Z^A]`.

The best next attack is no longer another empirical runner. It is the `Gamma/Khat/q_loc` action-existence problem: either derive a Helmholtz-compatible sector whose variation owns the local residual current, or retain `q_loc` as an explicit residual and keep local-GR claims blocked.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Minimal Parent Action Synthesis Attempt

{md_table(synthesis, ["synthesis_id", "action_block", "candidate_statement", "current_status", "blocking_gap", "adopt_now"])}

## Sector Certificate Matrix

{md_table(sectors, ["sector_id", "sector", "first_variation_required", "theta_qtau_required", "current_status", "sector_certificate_passed", "primary_gap"])}

## Action Adoption Gate

{md_table(adoption, ["gate_id", "gate", "gate_passed", "blocks_adoption", "reason"])}

## Local GR/Newton Derivation Ladder

{md_table(ladder, ["ladder_id", "derivation_step", "status", "why", "feeds"])}

## Residual Or Closure Ledger

{md_table(residuals, ["residual_id", "object", "definition", "required_resolution", "current_policy"])}

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
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    write_csv(OUTPUTS["sources"], source_rows)

    synthesis = synthesis_rows()
    sectors = sector_rows()
    adoption = adoption_rows()
    ladder = ladder_rows()
    residuals = residual_rows()
    claims = claim_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["synthesis"], synthesis)
    write_csv(OUTPUTS["sectors"], sectors)
    write_csv(OUTPUTS["adoption"], adoption)
    write_csv(OUTPUTS["ladder"], ladder)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(source_rows)
    write_csv(OUTPUTS["validation"], validation)

    write_doc(source_rows, synthesis, sectors, adoption, ladder, residuals, claims, decisions, next_target, branches, validation)

    overall = next(row for row in validation if row["validation_id"] == "VAL2940_OVERALL")["passed"]
    print(f"2940 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()

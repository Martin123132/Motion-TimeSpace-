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
DOC = ROOT / "3376-Y5-R2FR-boundary-zero-flux-or-Bzero-first-row-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3376_SOURCE_REGISTER.csv",
    "zero_theorem": OUT / "P8_Y5_R2FR_3376_BOUNDARY_ZERO_FLUX_THEOREM_ATTEMPT.csv",
    "signature_audit": OUT / "P8_Y5_R2FR_3376_BOUNDARY_SIGNATURE_AUDIT.csv",
    "residual_rows": OUT / "P8_Y5_R2FR_3376_BZERO_FIRST_BOUND_ROWS_NONCLAIM.csv",
    "numeric_scan": OUT / "P8_Y5_R2FR_3376_BZERO_NUMERIC_SCAN.csv",
    "trap_ledger": OUT / "P8_Y5_R2FR_3376_EXACTNESS_TRAP_LEDGER.csv",
    "transfer_update": OUT / "P8_Y5_R2FR_3376_SOURCE_TRANSFER_UPDATE_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3376_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3376_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3376_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3376_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3376_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3376_0_3375_doc", ROOT / "3375-Y5-R2FR-worldtube-source-measure-selector-or-Rworldtube-bound-under-AX1090.md", "3375 source selector handoff"),
    ("SRC3376_1_3375_next", OUT / "P8_Y5_R2FR_3375_NEXT_TARGET.csv", "3375 selected boundary zero/reference target"),
    ("SRC3376_2_3375_residuals", OUT / "P8_Y5_R2FR_3375_RWORLDTUBE_BOUND_ROWS_NONCLAIM.csv", "3375 retained boundary/source residuals"),
    ("SRC3376_3_3374_doc", ROOT / "3374-Y5-R2FR-topological-Hilbert-equality-or-Req-bound-under-AX1090.md", "3374 B_zero handoff"),
    ("SRC3376_4_boundary_status", OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv", "current first-row boundary/reference status"),
    ("SRC3376_5_conditional_chain", OUT / "P8_Y5_BOUNDARY_REFERENCE_CONDITIONAL_THEOREM_CHAIN.csv", "boundary/reference conditional theorem chain"),
    ("SRC3376_6_minimal_action_contract", OUT / "P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv", "minimal action contract for boundary/reference zero"),
    ("SRC3376_7_zero_audit", OUT / "P8_Y5_BOUNDARY_REFERENCE_THEOREM_ZERO_AUDIT.csv", "boundary/reference zero theorem audit"),
    ("SRC3376_8_data_audit", OUT / "P8_Y5_BOUNDARY_REFERENCE_DATA_SOURCE_AUDIT.csv", "boundary/reference data-source audit"),
    ("SRC3376_9_residual_row", OUT / "P8_Y5_BOUNDARY_REFERENCE_RESIDUAL_ROW.csv", "boundary/reference residual row"),
    ("SRC3376_10_scorecard", OUT / "P8_Y5_BOUNDARY_REFERENCE_RESIDUAL_SCORECARD.csv", "boundary/reference residual scorecard"),
    ("SRC3376_11_cohomology_theorem", OUT / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv", "cohomology/no-hair boundary theorem attempt"),
    ("SRC3376_12_cohomology_obstruction", OUT / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_OBSTRUCTION_LEDGER.csv", "cohomology/no-hair obstruction ledger"),
    ("SRC3376_13_flux_fill_row", OUT / "P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv", "boundary flux bound fill row"),
    ("SRC3376_14_rollup_3244", OUT / "P8_Y5_R2FR_3244_BOUNDARY_REFERENCE_ROLLUP.csv", "R2FR boundary/reference rollup"),
    ("SRC3376_15_poynting_3249", OUT / "P8_Y5_R2FR_3249_SOURCE_WORLDTUBE_POYNTING_BOUND_ROW.csv", "Poynting source-worldtube bound row"),
    ("SRC3376_16_flux_norm_3250", OUT / "P8_Y5_R2FR_3250_SOURCE_WORLDTUBE_FLUX_NORM_ROW.csv", "Poynting flux norm row"),
]

NUMERIC_SCAN_TARGETS = [
    ("B_zero_flux", OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv", "first-row boundary status"),
    ("Delta_symp", OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv", "symplectic/reference status"),
    ("epsilon_boundary_reference_abs", OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv", "boundary/reference envelope"),
    ("M_H_ref", OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv", "positive source denominator"),
    ("Phi_Poynting_bound", OUT / "P8_Y5_R2FR_3244_BOUNDARY_REFERENCE_ROLLUP.csv", "physical Poynting boundary flux"),
    ("R_Poynting_worldtube", OUT / "P8_Y5_R2FR_3375_RWORLDTUBE_BOUND_ROWS_NONCLAIM.csv", "3375 Poynting source-worldtube residual"),
]

BAD_STATUS_TOKENS = (
    "MISSING",
    "NOT_COMPUTED",
    "NOT_DERIVED",
    "NOT_YET",
    "CONDITIONAL",
    "CONTRACT",
    "TEMPLATE",
    "UNSIGNED",
    "NONCLAIM",
    "FALSE",
    "FAIL",
)


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


def zero_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "step_id": "BZF3376_0_fixed_linking_annulus",
            "claim_piece": "two surfaces bound the same source-free annulus",
            "statement": "Let A be the compact exterior annulus between S1 and S2, with S1 and S2 linked to the same W_source selected by 3375 and supp(J_H) cap A empty.",
            "derivation": "This makes any surface-charge difference a Stokes problem on a fixed domain instead of a comparison between two different source choices.",
            "current_status": "SETUP_CONDITIONAL_FROM_3375_NOT_FULLY_PARENT_SIGNED",
            "residual_if_missing": "R_Wsupport;R_worldtube_glue",
            "valid_for_claim": "false",
        },
        {
            "step_id": "BZF3376_1_exact_primitive_is_fixed",
            "claim_piece": "improvement/reference form has a parent-fixed primitive",
            "statement": "If B_imp=dC on A and the primitive C is selected by the parent boundary term/reference branch before readout, then int_S2 B_imp-int_S1 B_imp=int_A dB_imp.",
            "derivation": "Exactness is usable only when the primitive and representative are fixed. Otherwise an exact-looking improvement can still carry a finite charge by changing representatives.",
            "current_status": "VALID_CONDITIONAL_LEMMA_PRIMITIVE_NOT_PARENT_SIGNED",
            "residual_if_missing": "B_zero_flux",
            "valid_for_claim": "false",
        },
        {
            "step_id": "BZF3376_2_relative_cohomology_zero",
            "claim_piece": "no harmonic/topological boundary charge",
            "statement": "The relative boundary class must be trivial: [B_imp]=0 in the linked annulus pair and every harmonic/corner component has zero fixed flux.",
            "derivation": "This is the missing correction to the lazy exactness argument: dC handles the exact component, but harmonic/corner pieces are independent finite charges unless excluded or bounded.",
            "current_status": "VALID_CONDITIONAL_TOPOLOGY_CLAUSE_NOT_PARENT_SIGNED",
            "residual_if_missing": "epsilon_Bv_corner_abs;epsilon_Bv_topological_abs",
            "valid_for_claim": "false",
        },
        {
            "step_id": "BZF3376_3_physical_flux_silence",
            "claim_piece": "physical boundary flux is zero or already in Hilbert source measure",
            "statement": "Poynting, matter, projector, memory, domain, and frame flux through the source collar must vanish or be included in H_tau/M_source before the boundary numerator is set to zero.",
            "derivation": "A mathematical exact term cannot erase real energy/current flux. Public EM Hilbert stress belongs in the source measure; hidden or second-frame flux remains a residual.",
            "current_status": "PLACEMENT_DERIVED_INPUT_NORMS_MISSING",
            "residual_if_missing": "Phi_Poynting_bound;R_Poynting_worldtube;Delta_symp",
            "valid_for_claim": "false",
        },
        {
            "step_id": "BZF3376_4_reference_symplectic_lock",
            "claim_piece": "reference and symplectic subtraction are source-blind",
            "statement": "H_ref and the symplectic boundary subtraction must be fixed under source, radius, frame, and tau variations: D_source H_ref=D_r H_ref=D_frame H_ref=D_tau H_ref=0.",
            "derivation": "If the reference moves with the source or readout, Delta_symp can mimic a finite local mass correction even when the exact boundary flux is zero.",
            "current_status": "REFERENCE_LOCK_UNSIGNED",
            "residual_if_missing": "Delta_symp;R_reference_selector",
            "valid_for_claim": "false",
        },
        {
            "step_id": "BZF3376_5_zero_verdict",
            "claim_piece": "B_zero_flux=0 and Delta_symp=0",
            "statement": "If BZF3376_0 through BZF3376_4 are parent-signed in the same q/e_obs/tau/H_ref/M_H_ref branch, then B_zero_flux=0, Delta_symp=0, and epsilon_boundary_reference_abs=0.",
            "derivation": "This is a real derivation route, not a plateau axiom: Stokes on a fixed annulus plus fixed primitive, trivial relative class, no physical flux, and source-blind reference kills the numerator.",
            "current_status": "VALID_CONDITIONAL_THEOREM_NOT_CURRENT_CLAIM",
            "residual_if_missing": "epsilon_boundary_reference_abs",
            "valid_for_claim": "false",
        },
    ]


def signature_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "SIG3376_0_fixed_annulus",
            "required_signature": "S1/S2 link the same parent-selected W_source and A is source-free",
            "evidence": "3375 supplies the conditional selector, but current W_source remains not parent-signed",
            "current_status": "CONDITIONAL_FROM_3375",
            "blocks": "BZF3376_0",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SIG3376_1_fixed_primitive",
            "required_signature": "B_imp=dC with C fixed by parent boundary/reference choice before readout",
            "evidence": "MAC545_3 and BCT549_2 state exactness route but mark it not derived/not parent-owned",
            "current_status": "MISSING_PARENT_SIGNATURE",
            "blocks": "BZF3376_1",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SIG3376_2_relative_class",
            "required_signature": "linked annulus has no harmonic/corner/topological boundary charge",
            "evidence": "BR3244_2 and BCT549_1 retain topological/corner class uncertainty",
            "current_status": "MISSING_TOPOLOGY_CERTIFICATE",
            "blocks": "BZF3376_2",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SIG3376_3_physical_flux",
            "required_signature": "Poynting and other physical flux are zero or included in H_tau/M_source",
            "evidence": "3375 and 3249/3250 place Poynting but flux norms and public-Hodge inputs are missing",
            "current_status": "FLUX_INPUTS_MISSING",
            "blocks": "BZF3376_3",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SIG3376_4_reference_lock",
            "required_signature": "H_ref/symplectic subtraction is source-blind and fixed",
            "evidence": "MAC545_2 and existing reference rows mark reference choice as a contract, not a parent result",
            "current_status": "REFERENCE_LOCK_UNSIGNED",
            "blocks": "BZF3376_4",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SIG3376_5_positive_denominator",
            "required_signature": "M_H_ref>0 in same source/readout frame",
            "evidence": "Boundary first-row status has claim_valid_data_rows=0 and claim_valid_theorem_zero_rows=0 for M_H_ref",
            "current_status": "MISSING_DENOMINATOR",
            "blocks": "epsilon_boundary_reference_abs",
            "valid_for_claim": "false",
        },
    ]


def residual_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "BZB3376_0_B_zero_flux",
            "symbol": "B_zero_flux",
            "definition": "linked-surface flux of exact/improvement/reference boundary form not cancelled by fixed primitive and trivial relative class",
            "bound_formula": "|int_S2 B_imp - int_S1 B_imp|/|M_H_ref|",
            "required_inputs": "S1,S2,A,C_or_Bimp,relative_class_certificate,orientation,M_H_ref,source_path",
            "current_status": "FIRST_ROW_UNFILLED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "BZB3376_1_Delta_symp",
            "symbol": "Delta_symp",
            "definition": "finite Hamiltonian/symplectic/reference subtraction drift between linked surfaces",
            "bound_formula": "|int_dA(omega_extra+omega_ref+omega_PiM)|/|M_H_ref|",
            "required_inputs": "Theta,omega_total,H_ref,PiM,tau,surface lock,M_H_ref",
            "current_status": "FIRST_ROW_UNFILLED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "BZB3376_2_Phi_Poynting_bound",
            "symbol": "Phi_Poynting_bound",
            "definition": "physical EM/Poynting flux through source/collar boundary not included in public Hilbert stress",
            "bound_formula": "mu0^-1 ||E_T||_L2(B)||B_T||_L2(B)/|M_H_ref|",
            "required_inputs": "unit system,E/B boundary norms,collar geometry,public-Hodge certificate,M_H_ref",
            "current_status": "FORMULA_READY_INPUT_NORMS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "row_id": "BZB3376_3_epsilon_boundary_reference_abs",
            "symbol": "epsilon_boundary_reference_abs",
            "definition": "absolute finite-shell boundary/reference envelope",
            "bound_formula": "(|B_zero_flux|+|Delta_symp|+|Phi_Poynting_bound|+corner/topology terms)/|M_H_ref|",
            "required_inputs": "B_zero_flux,Delta_symp,Phi_Poynting_bound,corner/topology rows,M_H_ref",
            "current_status": "ENVELOPE_READY_NUMERIC_MISSING",
            "valid_for_claim": "false",
        },
        {
            "row_id": "BZB3376_4_M_H_ref",
            "symbol": "M_H_ref",
            "definition": "positive same-frame Hamiltonian source mass denominator",
            "bound_formula": "M_H_ref>0 in the same q/e_obs/tau/H_ref/source branch",
            "required_inputs": "H_tau,H_ref,N_G,e_obs,tau,source system,units,positivity certificate",
            "current_status": "MISSING_DENOMINATOR",
            "valid_for_claim": "false",
        },
    ]


def row_mentions_symbol(row: dict[str, str], symbol: str) -> bool:
    haystack = " ".join(str(value) for value in row.values()).lower()
    if symbol.lower() in haystack:
        return True
    aliases = {
        "B_zero_flux": ("B_zero", "boundary flux", "B_imp"),
        "Delta_symp": ("Delta_symp", "symplectic", "H_ref"),
        "epsilon_boundary_reference_abs": ("epsilon_boundary_reference", "boundary_reference", "BR"),
        "M_H_ref": ("M_H_ref", "denominator", "GM"),
        "Phi_Poynting_bound": ("Poynting", "S_EM", "T_EM"),
        "R_Poynting_worldtube": ("R_Poynting", "Poynting"),
    }
    return any(alias.lower() in haystack for alias in aliases.get(symbol, ()))


def row_claimish(row: dict[str, str]) -> bool:
    text = " ".join(str(value) for value in row.values()).upper()
    valid_fields = [
        str(row.get("valid_for_claim", "")).lower(),
        str(row.get("claim_allowed", "")).lower(),
        str(row.get("score_ready", "")).lower(),
        str(row.get("valid_prediction_row", "")).lower(),
    ]
    has_positive_flag = any(value == "true" for value in valid_fields)
    has_bad_token = any(token in text for token in BAD_STATUS_TOKENS)
    return has_positive_flag and not has_bad_token


def numeric_scan_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, (symbol, path, role) in enumerate(NUMERIC_SCAN_TARGETS):
        csv_rows = read_csv_rows(path)
        matching = [row for row in csv_rows if row_mentions_symbol(row, symbol)]
        claimish = [row for row in matching if row_claimish(row)]
        status_excerpt = "NO_MATCHING_ROWS"
        if matching:
            status_excerpt = " | ".join(
                ";".join(
                    str(row.get(key, ""))
                    for key in ("status", "current_status", "current_result", "current_best_evidence", "residual_if_unsigned")
                    if row.get(key, "")
                )
                for row in matching[:3]
            )
            if not status_excerpt:
                status_excerpt = "MATCHING_ROWS_NONCLAIM_OR_SCHEMA_ONLY"
        rows.append(
            {
                "scan_id": f"SCAN3376_{index}_{symbol}",
                "symbol": symbol,
                "source_path": str(path),
                "source_exists": bool_text(path.exists()),
                "matching_rows": str(len(matching)),
                "claim_valid_rows": str(len(claimish)),
                "status_excerpt": status_excerpt,
                "scan_result": "SOURCE_BACKED_NUMERIC_ROW_FOUND" if claimish else "NO_SOURCE_BACKED_NUMERIC_ROW",
                "valid_for_claim": "false",
            }
        )
    return rows


def trap_ledger_rows() -> list[dict[str, str]]:
    return [
        {
            "trap_id": "TRAP3376_0_exact_does_not_mean_zero",
            "tempting_claim": "B_imp is exact, therefore its flux is zero",
            "why_wrong": "an exact representative can still shift a finite surface charge if the primitive/reference is not fixed or if surfaces/classes differ",
            "safe_repair": "require fixed primitive C and same linked annulus before applying Stokes",
            "valid_for_claim": "false",
        },
        {
            "trap_id": "TRAP3376_1_topology_not_silenced_by_local_formula",
            "tempting_claim": "local dC formula removes every boundary component",
            "why_wrong": "harmonic, corner, and relative cohomology pieces are not controlled by the local exact primitive",
            "safe_repair": "prove trivial relative class or retain corner/topological residuals",
            "valid_for_claim": "false",
        },
        {
            "trap_id": "TRAP3376_2_no_flux_not_no_energy",
            "tempting_claim": "boundary is mathematical bookkeeping, so physical flux can be ignored",
            "why_wrong": "Poynting/matter/projector/domain flux through a collar changes H_tau unless included in the source measure",
            "safe_repair": "public Hilbert stress inclusion or explicit flux bound",
            "valid_for_claim": "false",
        },
        {
            "trap_id": "TRAP3376_3_reference_can_hide_mass",
            "tempting_claim": "choose H_ref to make boundary residual vanish",
            "why_wrong": "a source-dependent reference subtraction can absorb the desired GM correction",
            "safe_repair": "prove H_ref is source-blind before fitting or retain Delta_symp/R_reference_selector",
            "valid_for_claim": "false",
        },
    ]


def transfer_update_rows() -> list[dict[str, str]]:
    return [
        {
            "update_id": "STU3376_0_if_boundary_zero_signed",
            "condition": "B_zero_flux=Delta_symp=Phi_Poynting_bound=0 with positive same-frame M_H_ref",
            "source_transfer_effect": "boundary/reference envelope drops from 3372/3374/3375 local source-transfer residuals",
            "remaining_blockers": "weak-field G/kappa/source-current normalization and second-order PPN residuals",
            "current_status": "CONDITIONAL_BRANCH_NOT_CURRENT_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "update_id": "STU3376_1_current_branch",
            "condition": "current MTS corpus",
            "source_transfer_effect": "B_zero_flux, Delta_symp, Poynting/corner/topology terms and M_H_ref stay explicit nonclaim rows",
            "remaining_blockers": "fixed primitive, relative cohomology, reference lock, flux inputs and denominator",
            "current_status": "BOUNDARY_RESIDUAL_RETAINED",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {
            "run_id": "RUN3376_0_boundary_zero_theorem",
            "test": "derive B_zero_flux=0 from fixed annulus, fixed primitive, trivial relative class and no physical flux",
            "result": "PASS_CONDITIONAL_THEOREM",
            "detail": "Stokes gives the zero only after the representative, topology and physical flux clauses are signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3376_1_exactness_trap",
            "test": "claim exactness alone kills boundary flux",
            "result": "REFUSED",
            "detail": "exact labels can carry finite surface charges through representative/reference/class changes",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3376_2_current_parent_signature",
            "test": "promote boundary/reference zero in current corpus",
            "result": "BLOCKED_NOT_PARENT_SIGNED",
            "detail": "primitive, relative cohomology, physical flux, reference lock and M_H_ref are missing or nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3376_3_numeric_scan",
            "test": "find source-backed B_zero/Delta_symp/M_H_ref/Poynting row",
            "result": "NO_NUMERIC_ROW_FOUND",
            "detail": "current boundary/reference rows remain templates, contracts, conditional theorem rows or unfilled first rows",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {"gate_id": "GATE3376_0_sources", "claim": "all required 3376 source paths exist and parse", "gate_pass": bool_text(source_ok), "reason": "source register validates local inputs", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3376_1_Bzero", "claim": "B_zero_flux=0 is parent-signed", "gate_pass": "false", "reason": "fixed primitive and relative class are not parent-owned", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3376_2_Delta_symp", "claim": "Delta_symp=0 is parent-signed", "gate_pass": "false", "reason": "reference and symplectic/projector subtraction are not locked", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3376_3_physical_flux", "claim": "physical Poynting/boundary flux is zero or included", "gate_pass": "false", "reason": "Poynting/source-worldtube norms and public-Hodge certificates are missing", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3376_4_first_row", "claim": "epsilon_boundary_reference_abs first row is score-ready", "gate_pass": "false", "reason": "no source-backed numerator or positive M_H_ref row exists", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3376_5_local_GR", "claim": "boundary/reference route closes local GR", "gate_pass": "false", "reason": "boundary zero is conditional and weak-field/PPN calibration remain open", "claim_allowed": "false", "valid_for_claim": "false"},
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3376_0_progress",
            "decision": "Boundary zero has a real conditional derivation, but exactness alone is rejected.",
            "because": "fixed annulus + fixed primitive + trivial relative class + no physical flux + source-blind reference is sufficient to zero the boundary/reference numerator.",
            "next_action": "do not claim boundary zero until those signatures exist in one parent branch",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3376_1_current_status",
            "decision": "Current MTS still carries boundary/reference residuals.",
            "because": "first-row status has zero claim-valid data/theorem rows for B_zero_flux, Delta_symp, M_H_ref and the boundary envelope.",
            "next_action": "retain B_zero_flux/Delta_symp/Poynting/M_H_ref rows",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3376_2_next_move",
            "decision": "The next useful leap is weak-field source normalization, not another exactness pass.",
            "because": "3375 and 3376 now define the source and boundary contracts conditionally; the remaining local-GR hinge is the same G/kappa/source-current coefficient in H_tau, Poisson/Newton and PPN.",
            "next_action": "attempt G_ref/kappa/N_G normalization derivation or stage delta_kappa/delta_ellJ rows",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3377-Y5-R2FR-weak-field-source-normalization-or-Gref-kappa-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3377_weak_field_source_normalization_or_Gref_kappa_bound.py",
            "objective": "derive the same N_G/G_ref/kappa/source-current scale in H_tau, Poisson/Newton and PPN readout, or stage delta_kappa/delta_ellJ rows",
            "why_next": "source selection and boundary/reference zero are now conditional theorem contracts; calibrated source coupling is the next route to local GR rather than another bookkeeping pass",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3378-Y5-R2FR-parent-action-minimal-line-or-source-bound-inputs-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3378_parent_action_minimal_line_or_source_bound_inputs.py",
            "objective": "write the minimal parent action line that owns e_obs, Theta, Q_tau, B_ref, Pi_M and kappa, or explicitly demote the route to closure-only",
            "why_next": "many remaining gates share one missing object: the explicit parent variation",
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
    formalization_hits = list(FW.rglob("*3376*")) if FW.exists() else []
    step_ids = {row["step_id"] for row in rows_by_name["zero_theorem"]}
    audit_ids = {row["audit_id"] for row in rows_by_name["signature_audit"]}
    residual_symbols = {row["symbol"] for row in rows_by_name["residual_rows"]}
    scan_results = {row["scan_result"] for row in rows_by_name["numeric_scan"]}
    trap_ids = {row["trap_id"] for row in rows_by_name["trap_ledger"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3376_0_sources_exist_parse", "all cited local source paths exist and parse", source_ok, ""),
        ("VAL3376_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3376_2_zero_theorem", "zero theorem covers annulus, primitive, relative class, physical flux, reference lock and verdict", {"BZF3376_0_fixed_linking_annulus", "BZF3376_1_exact_primitive_is_fixed", "BZF3376_2_relative_cohomology_zero", "BZF3376_3_physical_flux_silence", "BZF3376_4_reference_symplectic_lock", "BZF3376_5_zero_verdict"}.issubset(step_ids), ""),
        ("VAL3376_3_signature_audit", "signature audit covers annulus, primitive, topology, physical flux, reference and denominator", {"SIG3376_0_fixed_annulus", "SIG3376_1_fixed_primitive", "SIG3376_2_relative_class", "SIG3376_3_physical_flux", "SIG3376_4_reference_lock", "SIG3376_5_positive_denominator"}.issubset(audit_ids), ""),
        ("VAL3376_4_residual_rows", "residual rows cover B_zero, Delta_symp, Poynting, envelope and M_H_ref", {"B_zero_flux", "Delta_symp", "Phi_Poynting_bound", "epsilon_boundary_reference_abs", "M_H_ref"}.issubset(residual_symbols), ""),
        ("VAL3376_5_numeric_scan_blocks_claim", "numeric scan finds no source-backed numeric rows", scan_results == {"NO_SOURCE_BACKED_NUMERIC_ROW"}, ""),
        ("VAL3376_6_exactness_traps", "trap ledger blocks exactness, topology, no-flux and reference shortcuts", {"TRAP3376_0_exact_does_not_mean_zero", "TRAP3376_1_topology_not_silenced_by_local_formula", "TRAP3376_2_no_flux_not_no_energy", "TRAP3376_3_reference_can_hide_mass"}.issubset(trap_ids), ""),
        ("VAL3376_7_runner_blocks_claim", "runner passes conditional theorem but refuses current claim", "PASS_CONDITIONAL_THEOREM" in runner_results and "REFUSED" in runner_results and "BLOCKED_NOT_PARENT_SIGNED" in runner_results and "NO_NUMERIC_ROW_FOUND" in runner_results, ""),
        ("VAL3376_8_gates_block_local", "promotion gates block Bzero, Delta_symp, physical flux, first row and local GR", gate_map.get("GATE3376_1_Bzero") == "false" and gate_map.get("GATE3376_2_Delta_symp") == "false" and gate_map.get("GATE3376_3_physical_flux") == "false" and gate_map.get("GATE3376_4_first_row") == "false" and gate_map.get("GATE3376_5_local_GR") == "false", ""),
        ("VAL3376_9_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3376_10_next_target", "next target moves to weak-field source normalization or minimal parent action", rows_by_name["next"][0]["target_id"].startswith("3377-Y5-R2FR-weak-field-source-normalization"), ""),
        ("VAL3376_11_write_scope_outside_formalization", "no 3376 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    checks.append(("VAL3376_12_overall", "3376 validation overall", all(passed for _, _, passed, _ in checks), "all required checks passed" if all(passed for _, _, passed, _ in checks) else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3376 - Y5/R2FR boundary zero flux or B_zero first row under AX1090",
        "",
        "## Summary",
        "- 3376 attacks the boundary/reference obstruction after 3375: can `B_zero_flux` and `Delta_symp` be derived to zero, or must they stay as first-row residuals?",
        "- Derivation result: a clean sufficient theorem exists. Fixed linking annulus + parent-fixed primitive + trivial relative boundary class + no physical flux + source-blind reference implies `B_zero_flux=0`, `Delta_symp=0`, and `epsilon_boundary_reference_abs=0`.",
        "- Important guardrail: exactness alone is rejected. An exact-looking boundary term can still carry a finite charge if the primitive, reference, relative class, corner term, or surface branch is not fixed before readout.",
        "- Poynting result: physical wave/EM flux is not a bookkeeping boundary term; it is either inside public Hilbert stress/source measure or retained as `Phi_Poynting_bound` / `R_Poynting_worldtube`.",
        "- Current verdict: the zero theorem is not parent-signed for current MTS. Fixed primitive, relative cohomology, reference lock, physical-flux inputs, and positive `M_H_ref` remain missing or nonclaim.",
        "- Fallback result: `B_zero_flux`, `Delta_symp`, `Phi_Poynting_bound`, `epsilon_boundary_reference_abs`, and `M_H_ref` are explicit nonclaim rows.",
        "- Best next strike is weak-field source normalization: derive the same `N_G/G_ref/kappa/source-current` scale in `H_tau`, Poisson/Newton, and PPN readout, or stage `delta_kappa/delta_ellJ` rows.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Boundary Zero-flux Theorem Attempt",
        md_table(rows_by_name["zero_theorem"]),
        "## Boundary Signature Audit",
        md_table(rows_by_name["signature_audit"]),
        "## B_zero First Bound Rows",
        md_table(rows_by_name["residual_rows"]),
        "## Numeric Scan",
        md_table(rows_by_name["numeric_scan"]),
        "## Exactness Trap Ledger",
        md_table(rows_by_name["trap_ledger"]),
        "## Source-transfer Update",
        md_table(rows_by_name["transfer_update"]),
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
        "zero_theorem": zero_theorem_rows(),
        "signature_audit": signature_audit_rows(),
        "residual_rows": residual_rows(),
        "numeric_scan": numeric_scan_rows(),
        "trap_ledger": trap_ledger_rows(),
        "transfer_update": transfer_update_rows(),
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

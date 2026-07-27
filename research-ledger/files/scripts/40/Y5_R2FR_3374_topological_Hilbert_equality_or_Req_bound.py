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
DOC = ROOT / "3374-Y5-R2FR-topological-Hilbert-equality-or-Req-bound-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3374_SOURCE_REGISTER.csv",
    "same_object_lemma": OUT / "P8_Y5_R2FR_3374_SAME_OBJECT_LEMMA_ATTEMPT.csv",
    "signature_audit": OUT / "P8_Y5_R2FR_3374_PARENT_SIGNATURE_AUDIT.csv",
    "bound_rows": OUT / "P8_Y5_R2FR_3374_REQ_BOUND_ROWS_NONCLAIM.csv",
    "numeric_scan": OUT / "P8_Y5_R2FR_3374_REQ_NUMERIC_SCAN.csv",
    "countermodels": OUT / "P8_Y5_R2FR_3374_COUNTERMODEL_LEDGER.csv",
    "transfer_update": OUT / "P8_Y5_R2FR_3374_SOURCE_TRANSFER_UPDATE_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3374_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3374_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3374_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3374_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3374_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3374_0_3373_doc", ROOT / "3373-Y5-R2FR-PiM-commutator-chainmap-zero-or-Icommutator-bound-under-AX1090.md", "3373 PiM chainmap and R_eq handoff"),
    ("SRC3374_1_3373_next", OUT / "P8_Y5_R2FR_3373_NEXT_TARGET.csv", "3373 next target selecting topological-Hilbert equality"),
    ("SRC3374_2_3373_theorem", OUT / "P8_Y5_R2FR_3373_PIM_CHAINMAP_COMMUTATOR_THEOREM_ATTEMPT.csv", "3373 chainmap theorem rows"),
    ("SRC3374_3_3373_obstructions", OUT / "P8_Y5_R2FR_3373_ICOMMUTATOR_OBSTRUCTION_ROWS_NONCLAIM.csv", "3373 obstruction rows including R_eq guard"),
    ("SRC3374_4_2595_components", OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv", "current R_eq, I_commutator, B_zero_flux, M_H_ref component rows"),
    ("SRC3374_5_2595_gate", OUT / "P8_Y5_GM_TRANSFER_2595_TRANSFER_GATE.csv", "GM transfer gates"),
    ("SRC3374_6_pim_template", OUT / "P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv", "PiM/R_eq input template"),
    ("SRC3374_7_top_attempt", OUT / "P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv", "topological-Hilbert equality attempt"),
    ("SRC3374_8_top_obstructions", OUT / "P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv", "topological-Hilbert equality obstructions"),
    ("SRC3374_9_top_routes", OUT / "P8_TOPOLOGICAL_HILBERT_EQUALITY_ROUTE_TESTS.csv", "topological-Hilbert equality route tests"),
    ("SRC3374_10_top_conditions", OUT / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv", "topological PiM closure conditions"),
    ("SRC3374_11_top_certificate", OUT / "P8_Y5_PIM_TOPO_EQUALITY_CERTIFICATE.csv", "PiM topological equality certificate"),
    ("SRC3374_12_top_gates", OUT / "P8_Y5_PIM_TOPO_EQUALITY_ACCEPTANCE_GATES.csv", "PiM topological equality acceptance gates"),
    ("SRC3374_13_hilbert_worldtube_attempt", OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv", "Hilbert worldtube glue attempt"),
    ("SRC3374_14_hilbert_worldtube_cert", OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv", "Hilbert worldtube certificate gaps"),
    ("SRC3374_15_parent_action_contract", OUT / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv", "Hilbert worldtube parent action contract"),
    ("SRC3374_16_worldtube_glue", OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv", "worldtube/source-measure glue clauses"),
    ("SRC3374_17_boundary_status", OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv", "boundary/reference/M_H_ref first-row status"),
    ("SRC3374_18_1015_doc", ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md", "older same-object lemma and R_eq fallback"),
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


def same_object_lemma_rows() -> list[dict[str, str]]:
    return [
        {
            "lemma_id": "REQ3374_0_fixed_worldtube_domain",
            "claim_piece": "same compact Hilbert source worldtube",
            "statement": "W_source is fixed by the parent Hilbert/source support before orbital or clock readout, and S1,S2 link the same W_source in a fixed exterior class.",
            "derivation": "Without a fixed W_source and linked S2 class, a topological charge can be chosen after the measured-GM target is known.",
            "current_status": "CONDITIONAL_REQUIRED_NOT_PARENT_SIGNED",
            "failure_if_missing": "worldtube/source measure can be a fitted readout mask",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "REQ3374_1_same_Hilbert_charge_scalar",
            "claim_piece": "topological charge scalar is Hilbert-owned",
            "statement": "Q_M is defined from the same observed Hilbert/Noether source measure: Q_M=ell_M(Pi_M J_H)=integral_W rho_H dV_H before readout.",
            "derivation": "This prevents J_M_top from carrying an independent conserved label unrelated to the active gravitational source.",
            "current_status": "CONDITIONAL_REQUIRED_NOT_PARENT_SIGNED",
            "failure_if_missing": "closed topological current can be the wrong conserved object",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "REQ3374_2_PD_representative",
            "claim_piece": "Poincare-dual mass representative",
            "statement": "J_M_top := Q_M omega_M_top, with d omega_M_top=0 and integral_S omega_M_top=1 for every linked sphere S in the fixed class.",
            "derivation": "Once Q_M is Hilbert-owned and omega_M_top is the parent-owned dual representative of W_source, J_M_top is the topological representative of the same compact source class.",
            "current_status": "FORMAL_TOPOLOGICAL_CLAUSE_CONDITIONAL",
            "failure_if_missing": "omega_M_top may represent topology but not the Hilbert source class",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "REQ3374_3_deRham_same_class",
            "claim_piece": "same-class exactness",
            "statement": "If Pi_M J_H and J_M_top are closed representatives of the same de Rham/cohomology class on the compact exterior, then Pi_M J_H - J_M_top = dB_zero.",
            "derivation": "The difference is closed and has zero periods over the exterior generators, so it is exact by de Rham/Poincare duality on the fixed exterior complex.",
            "current_status": "MATHEMATICAL_LEMMA_VALID_CONDITIONAL",
            "failure_if_missing": "R_eq_integral must remain as same-class residual",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "REQ3374_4_boundary_zero_flux",
            "claim_piece": "exact term harmlessness",
            "statement": "The equality is source-transfer safe only if the exact term has zero/fixed linked-surface flux: integral_S2 dB_zero - integral_S1 dB_zero = 0 before readout.",
            "derivation": "Exactness alone does not stop a boundary/reference term from shifting the finite source mass; the linked-surface flux must vanish or be bounded.",
            "current_status": "CONDITIONAL_ROUTE_OPEN_FIRST_ROW_UNFILLED",
            "failure_if_missing": "B_zero_flux and boundary/reference residuals remain",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "REQ3374_5_equality_verdict",
            "claim_piece": "Pi_M J_H = J_M_top + dB_zero",
            "statement": "The same-object theorem holds only if REQ3374_0 through REQ3374_4 are parent-signed in the same q/e_obs/tau/M_H_ref branch.",
            "derivation": "Combining Hilbert-owned source measure, PD topological representative, de Rham exactness, and zero boundary flux gives the desired equality. Current MTS has the lemma, not the signatures.",
            "current_status": "VALID_CONDITIONAL_THEOREM_NOT_CURRENT_CLAIM",
            "failure_if_missing": "R_eq_integral/M_H_ref remains the retained source-transfer row",
            "valid_for_claim": "false",
        },
    ]


def signature_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "SIG3374_0_worldtube_fixed",
            "required_signature": "compact Hilbert source worldtube fixed before readout",
            "evidence": "HWT536_0 and HWG535_0 both missing/not derived",
            "current_status": "MISSING_PARENT_SIGNATURE",
            "blocks": "REQ3374_0",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SIG3374_1_source_measure_owned",
            "required_signature": "Q_M is defined from same observed Hilbert/Noether source measure",
            "evidence": "HWT536_1/HWG535_1/PAC537_1 remain not-yet-derived",
            "current_status": "MISSING_PARENT_SIGNATURE",
            "blocks": "REQ3374_1",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SIG3374_2_topological_representative_matches_worldtube",
            "required_signature": "omega_M_top is the PD representative of the same Hilbert worldtube boundary class",
            "evidence": "PTEC534_3/PTEC534_4 and HWT536_4 not derived/certificate missing",
            "current_status": "MISSING_PARENT_SIGNATURE",
            "blocks": "REQ3374_2;REQ3374_3",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SIG3374_3_boundary_zero",
            "required_signature": "dB_zero exact/reference term has zero compact linked-surface flux",
            "evidence": "B_zero_flux has zero claim-valid data/theorem rows in boundary status",
            "current_status": "MISSING_ZERO_FLUX_OR_BOUND",
            "blocks": "REQ3374_4",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SIG3374_4_extra_charge_silence",
            "required_signature": "nonEH, domain, memory, motion, time, range, boundary and frame sectors carry no independent local mass charge",
            "evidence": "HWT536_7 and OB501_3 retain hidden/boundary/domain/nonHilbert exchange",
            "current_status": "FIELD_SPECIFIC_SILENCE_OPEN",
            "blocks": "local_GR_source_transfer",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "SIG3374_5_MHref_tau_branch",
            "required_signature": "positive same-frame M_H_ref and tau/source/readout branch",
            "evidence": "GMC2595_4/GMC2595_6 and boundary status M_H_ref are missing/nonclaim",
            "current_status": "MISSING_DENOMINATOR_AND_BRANCH_LOCK",
            "blocks": "R_eq_integral/M_H_ref scoring",
            "valid_for_claim": "false",
        },
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "REQB3374_0_R_eq_integral",
            "symbol": "R_eq_integral",
            "definition": "finite-shell same-object residual integral of R_eq := Pi_M J_H - J_M_top - dB_zero",
            "zero_route": "same compact Hilbert worldtube class plus PD topological representative plus zero boundary flux",
            "bound_formula": "|R_eq_integral|/|M_H_ref|",
            "required_inputs": "system_id,r1,r2,R_eq_integral,M_H_ref,units,normalization,source_file,assumptions",
            "current_status": "THEOREM_CONDITIONAL_NUMERIC_MISSING",
            "observable_links": "source_mass;Newton;R11;worldtube_glue;local_GR",
            "valid_for_claim": "false",
        },
        {
            "row_id": "REQB3374_1_B_zero_flux",
            "symbol": "B_zero_flux",
            "definition": "compact linked-surface flux of exact/reference term dB_zero",
            "zero_route": "reference/boundary term fixed before readout with zero linked-surface difference",
            "bound_formula": "|B_zero_flux|/|M_H_ref|",
            "required_inputs": "system_id,r1,r2,B_zero_flux,M_H_ref,reference_choice,source_file,assumptions",
            "current_status": "THEOREM_CONDITIONAL_NUMERIC_MISSING",
            "observable_links": "boundary;clock;orbital;PPN",
            "valid_for_claim": "false",
        },
        {
            "row_id": "REQB3374_2_same_class_residual",
            "symbol": "epsilon_same_class_abs",
            "definition": "absolute same-object equality envelope",
            "zero_route": "R_eq_integral=B_zero_flux=0 with same-branch positive M_H_ref",
            "bound_formula": "(|R_eq_integral| + |B_zero_flux|)/|M_H_ref|",
            "required_inputs": "R_eq_integral,B_zero_flux,M_H_ref,worldtube/surface/tau branch certificates",
            "current_status": "SCHEMA_READY_NONCLAIM",
            "observable_links": "source_transfer;qbar_domain;Newton;local_GR",
            "valid_for_claim": "false",
        },
        {
            "row_id": "REQB3374_3_wrong_object_guard",
            "symbol": "epsilon_wrong_conserved_object",
            "definition": "guard residual for topological charge not proven identical to Hilbert source charge",
            "zero_route": "Q_M defined from same observed Hilbert source measure before readout",
            "bound_formula": "1 unless same-object parent signatures pass, else 0",
            "required_inputs": "worldtube_fixed;source_measure_owned;PD_representative;no_multiplier;no_readout_mask",
            "current_status": "GUARD_ACTIVE_NOT_SCORED",
            "observable_links": "Newton_source;measured_GM;local_GR",
            "valid_for_claim": "false",
        },
    ]


def numeric_scan_rows() -> list[dict[str, str]]:
    scans = [
        ("SCAN3374_0_R_eq_2595", OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv", "R_eq_integral", "current_value"),
        ("SCAN3374_1_B_zero_2595", OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv", "B_zero_flux", "current_value"),
        ("SCAN3374_2_MHref_2595", OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv", "M_H_ref", "current_value"),
        ("SCAN3374_3_R_eq_template", OUT / "P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv", "R_eq_integral", "current_status"),
        ("SCAN3374_4_boundary_status", OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv", "B_zero_flux", "status"),
        ("SCAN3374_5_HWG_certificate", OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv", "topological_representative", "current_status"),
    ]
    rows: list[dict[str, str]] = []
    for scan_id, path, symbol, field in scans:
        csv_rows = read_csv_rows(path)
        matching = [
            row
            for row in csv_rows
            if symbol in row.get("symbol", "")
            or symbol in row.get("quantity", "")
            or symbol in row.get("input_id", "")
            or symbol in row.get("certificate_id", "")
            or symbol in row.get("definition", "")
        ]
        values = ";".join(row.get(field, "") for row in matching) if matching else "MISSING_ROW"
        claim_seen = any(row.get("valid_for_claim", "").lower() == "true" or row.get("score_ready", "").lower() == "true" for row in matching)
        missing_seen = "MISSING" in values.upper() or "NOT_FILLED" in values.upper() or "UNFILLED" in values.upper() or values == "MISSING_ROW"
        rows.append(
            {
                "scan_id": scan_id,
                "symbol": symbol,
                "source_path": str(path),
                "source_path_exists": bool_text(path.exists()),
                "observed_value_or_status": values,
                "score_ready_or_claim_valid_seen": bool_text(claim_seen),
                "missing_or_unfilled_seen": bool_text(missing_seen),
                "scan_result": "NO_SOURCE_BACKED_NUMERIC_ROW" if missing_seen or not claim_seen else "CANDIDATE_ROW_FOUND_REQUIRES_REVIEW",
                "valid_for_claim": "false",
            }
        )
    return rows


def countermodel_rows() -> list[dict[str, str]]:
    return [
        {
            "countermodel_id": "CM3374_0_independent_topological_label",
            "weak_premise": "closed topological current exists",
            "construction": "J_M_top=Q_top omega_M_top with Q_top independent of Hilbert source measure",
            "what_breaks": "conserves the wrong object",
            "repair": "define Q_M from same Hilbert worldtube source before readout",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3374_1_late_multiplier",
            "weak_premise": "equality imposed by constraint",
            "construction": "add Lambda_eq(Pi_M J_H-J_M_top-dB_zero) solely to force Newton closure",
            "what_breaks": "closure is inserted, not derived",
            "repair": "independent parent source/topology reason for equality",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3374_2_boundary_shift",
            "weak_premise": "difference is exact",
            "construction": "dB_zero has nonzero linked-surface flux or source-dependent reference",
            "what_breaks": "finite mass/source normalization shifts",
            "repair": "zero-flux certificate or B_zero_flux bound",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3374_3_hidden_exchange",
            "weak_premise": "Hilbert source current is the only mass channel",
            "construction": "domain/nonEH/memory/boundary/frame sectors exchange projected mass current in the exterior",
            "what_breaks": "Pi_M J_H and J_M_top are not closed representatives of the same class",
            "repair": "field-specific mass-charge silence or extra-channel bound",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3374_4_calibration_mismatch",
            "weak_premise": "same source class implies Newtonian GM",
            "construction": "closed charge has wrong G_ref, tau, M_H_ref or weak-field normalization",
            "what_breaks": "Newton/source transfer can be conserved but misnormalized",
            "repair": "positive same-frame M_H_ref and weak-field Gauss/PPN calibration",
            "valid_for_claim": "false",
        },
    ]


def transfer_update_rows() -> list[dict[str, str]]:
    return [
        {
            "update_id": "STU3374_0_if_same_object_signed",
            "condition": "Pi_M J_H = J_M_top + dB_zero and B_zero_flux=0 are parent-signed",
            "source_transfer_effect": "R_eq_integral and B_zero_flux drop from the source-transfer residual",
            "remaining_blockers": "worldtube source-measure glue;M_H_ref;tau_frame_lock;extra charge silence;weak-field calibration",
            "current_status": "CONDITIONAL_BRANCH_NOT_CURRENT_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "update_id": "STU3374_1_current_branch",
            "condition": "current MTS corpus",
            "source_transfer_effect": "R_eq_integral, B_zero_flux and wrong-conserved-object guard remain explicit",
            "remaining_blockers": "parent worldtube/source measure and numeric/source-backed rows",
            "current_status": "TRANSFER_RESIDUAL_RETAINED",
            "valid_for_claim": "false",
        },
        {
            "update_id": "STU3374_2_next_worldtube",
            "condition": "need parent signatures",
            "source_transfer_effect": "worldtube/source-measure selector is now the sharpest parent theorem target",
            "remaining_blockers": "W_source fixed before readout and Q_M from Hilbert source measure",
            "current_status": "NEXT_TARGET_SELECTED",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {
            "run_id": "RUN3374_0_deRham_lemma",
            "test": "same-class de Rham/Poincare-dual lemma",
            "result": "PASS_CONDITIONAL_LEMMA",
            "detail": "closed representatives of the same compact Hilbert source class differ by exact dB_zero",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3374_1_current_parent_signature",
            "test": "promote Pi_M J_H = J_M_top + dB_zero in current corpus",
            "result": "BLOCKED_NOT_PARENT_SIGNED",
            "detail": "worldtube, source measure, PD representative, boundary zero flux, M_H_ref and extra silence are not signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3374_2_numeric_scan",
            "test": "find source-backed R_eq_integral/M_H_ref or B_zero_flux/M_H_ref row",
            "result": "NO_NUMERIC_ROW_FOUND",
            "detail": "current rows are missing, unfilled, conditional or nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3374_3_wrong_object_guard",
            "test": "use closed topological current as Newton/source evidence without Hilbert ownership",
            "result": "REFUSED",
            "detail": "a closed current can be the wrong object unless Q_M is Hilbert/worldtube-owned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3374_4_Newton_local_GR",
            "test": "use 3374 to claim Newton/local GR",
            "result": "REFUSED",
            "detail": "same-object theorem is conditional and source-transfer/weak-field/PPN gates remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {"gate_id": "GATE3374_0_sources", "claim": "all required 3374 source paths exist and parse", "gate_pass": bool_text(source_ok), "reason": "source register validates every cited local input", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3374_1_same_object_theorem", "claim": "Pi_M J_H = J_M_top + dB_zero as parent theorem", "gate_pass": "false", "reason": "same-object lemma is conditional; parent worldtube/source-measure/topology signatures are missing", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3374_2_boundary_zero", "claim": "B_zero_flux=0 or bounded", "gate_pass": "false", "reason": "boundary/reference first rows have no claim-valid source or zero theorem", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3374_3_Req_bound", "claim": "R_eq_integral/M_H_ref bound row is score-ready", "gate_pass": "false", "reason": "numeric scan found no source-backed R_eq row and M_H_ref remains missing", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3374_4_source_transfer", "claim": "3372 source-transfer chain can promote", "gate_pass": "false", "reason": "R_eq/worldtube/boundary/M_H_ref gates remain open", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3374_5_Newton_local_GR", "claim": "Newton/local-GR source coupling is established", "gate_pass": "false", "reason": "same-object/source-transfer theorem and weak-field calibration are not parent-signed", "claim_allowed": "false", "valid_for_claim": "false"},
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3374_0_progress",
            "decision": "The same-object theorem is now the exact condition, not a vague topology argument.",
            "because": "de Rham/Poincare duality gives Pi_M J_H-J_M_top=dB_zero only after both currents are representatives of the same compact Hilbert source class.",
            "next_action": "do not use closed topology as Newton evidence unless Hilbert ownership is signed",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3374_1_current_status",
            "decision": "Current MTS does not yet prove topological-Hilbert equality.",
            "because": "worldtube, source measure, PD representative, zero boundary flux, extra charge silence and M_H_ref are all missing or nonclaim.",
            "next_action": "retain R_eq_integral/M_H_ref and B_zero_flux/M_H_ref rows",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3374_2_best_next",
            "decision": "Best next target is worldtube/source-measure selector, not another topology pass.",
            "because": "the topology lemma is clean; the missing physical step is proving Q_M is defined from the same Hilbert source worldtube before readout.",
            "next_action": "try to parent-sign W_source=supp(delta S_matter/delta e_obs) and Q_M=Hilbert/Noether source measure, or stage R_worldtube_glue",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3375-Y5-R2FR-worldtube-source-measure-selector-or-Rworldtube-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3375_worldtube_source_measure_selector_or_Rworldtube_bound.py",
            "objective": "prove the compact Hilbert source worldtube and source measure are fixed by the parent action before readout, or stage R_worldtube_glue/surface_homology/M_H_ref rows",
            "why_next": "3374 shows the same-object topology lemma is clean but cannot bite until Q_M is owned by the same Hilbert worldtube source measure",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3376-Y5-R2FR-boundary-zero-flux-or-Bzero-first-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3376_boundary_zero_flux_or_Bzero_first_row.py",
            "objective": "prove exact/reference term zero linked-surface flux or stage B_zero_flux/M_H_ref as the first boundary source-transfer row",
            "why_next": "boundary zero flux is the next finite-shell obstruction after worldtube/source ownership",
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
    formalization_hits = list(FW.rglob("*3374*")) if FW.exists() else []
    lemma_ids = {row["lemma_id"] for row in rows_by_name["same_object_lemma"]}
    audit_ids = {row["audit_id"] for row in rows_by_name["signature_audit"]}
    symbols = {row["symbol"] for row in rows_by_name["bound_rows"]}
    scan_results = {row["scan_result"] for row in rows_by_name["numeric_scan"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3374_0_sources_exist_parse", "all cited local source paths exist and parse", source_ok, ""),
        ("VAL3374_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3374_2_same_object_lemma", "same-object lemma covers worldtube, Hilbert charge, PD representative, deRham exactness, boundary zero and verdict", {"REQ3374_0_fixed_worldtube_domain", "REQ3374_1_same_Hilbert_charge_scalar", "REQ3374_2_PD_representative", "REQ3374_3_deRham_same_class", "REQ3374_4_boundary_zero_flux", "REQ3374_5_equality_verdict"}.issubset(lemma_ids), ""),
        ("VAL3374_3_signature_audit", "signature audit covers worldtube, source measure, topology, boundary, extra silence and M_H_ref", {"SIG3374_0_worldtube_fixed", "SIG3374_1_source_measure_owned", "SIG3374_2_topological_representative_matches_worldtube", "SIG3374_3_boundary_zero", "SIG3374_4_extra_charge_silence", "SIG3374_5_MHref_tau_branch"}.issubset(audit_ids), ""),
        ("VAL3374_4_bound_rows", "bound rows cover R_eq, B_zero, same-class envelope and wrong-object guard", {"R_eq_integral", "B_zero_flux", "epsilon_same_class_abs", "epsilon_wrong_conserved_object"}.issubset(symbols), ""),
        ("VAL3374_5_numeric_scan_blocks_claim", "numeric scan finds no source-backed R_eq/B_zero/M_H_ref row", scan_results == {"NO_SOURCE_BACKED_NUMERIC_ROW"}, ""),
        ("VAL3374_6_countermodels", "countermodels block independent topological label, multiplier, boundary shift, hidden exchange and calibration mismatch", len(rows_by_name["countermodels"]) >= 5, ""),
        ("VAL3374_7_runner_blocks_claim", "runner marks lemma conditional, current block, no numeric row and local-GR refused", "PASS_CONDITIONAL_LEMMA" in runner_results and "BLOCKED_NOT_PARENT_SIGNED" in runner_results and "NO_NUMERIC_ROW_FOUND" in runner_results and "REFUSED" in runner_results, ""),
        ("VAL3374_8_gates_block_local", "promotion gates block same-object theorem, boundary zero, R_eq bound, transfer and local GR", gate_map.get("GATE3374_1_same_object_theorem") == "false" and gate_map.get("GATE3374_2_boundary_zero") == "false" and gate_map.get("GATE3374_3_Req_bound") == "false" and gate_map.get("GATE3374_4_source_transfer") == "false" and gate_map.get("GATE3374_5_Newton_local_GR") == "false", ""),
        ("VAL3374_9_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3374_10_next_target", "next target moves to worldtube/source-measure selector", rows_by_name["next"][0]["target_id"].startswith("3375-Y5-R2FR-worldtube-source-measure-selector"), ""),
        ("VAL3374_11_write_scope_outside_formalization", "no 3374 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    checks.append(("VAL3374_12_overall", "3374 validation overall", all(passed for _, _, passed, _ in checks), "all required checks passed" if all(passed for _, _, passed, _ in checks) else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3374 - Y5/R2FR topological-Hilbert equality or R_eq bound under AX1090",
        "",
        "## Summary",
        "- 3374 attacks the conserved-wrong-object problem: a closed topological current is useful only if it is the same object as the observed Hilbert source current.",
        "- Derivation result: the same-object lemma is mathematically clean. If `Pi_M J_H` and `J_M_top` are closed representatives of the same compact Hilbert worldtube class, then `Pi_M J_H - J_M_top = dB_zero`; with zero linked-surface flux, `R_eq=0`.",
        "- Current verdict: the lemma is not parent-signed. The corpus still lacks the fixed Hilbert worldtube, same Hilbert/Noether source measure, Poincare-dual representative certificate, boundary zero flux, extra-charge silence, and positive same-frame `M_H_ref`.",
        "- Fallback result: `R_eq_integral/M_H_ref`, `B_zero_flux/M_H_ref`, and the wrong-conserved-object guard are explicit nonclaim rows.",
        "- Numeric result: no source-backed `R_eq_integral`, `B_zero_flux`, or `M_H_ref` row exists yet.",
        "- Best next strike is the worldtube/source-measure selector: prove `W_source=supp(delta S_matter/delta e_obs)` and `Q_M` is the Hilbert/Noether source measure before readout, or stage `R_worldtube_glue`.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Same-object Lemma Attempt",
        md_table(rows_by_name["same_object_lemma"]),
        "## Parent Signature Audit",
        md_table(rows_by_name["signature_audit"]),
        "## R_eq Bound Rows",
        md_table(rows_by_name["bound_rows"]),
        "## Numeric Scan",
        md_table(rows_by_name["numeric_scan"]),
        "## Countermodel Ledger",
        md_table(rows_by_name["countermodels"]),
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
        "same_object_lemma": same_object_lemma_rows(),
        "signature_audit": signature_audit_rows(),
        "bound_rows": bound_rows(),
        "numeric_scan": numeric_scan_rows(),
        "countermodels": countermodel_rows(),
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

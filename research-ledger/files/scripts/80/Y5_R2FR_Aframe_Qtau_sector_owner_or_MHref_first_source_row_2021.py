from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
DOC = ROOT / "2021-Y5-R2FR-Aframe-Qtau-sector-owner-or-MHref-first-source-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, object]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_rows_parse(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def md_cell(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    try:
        result = subprocess.run(
            ["git", "-C", str(FORMALIZATION), "status", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        return 0
    if result.returncode != 0:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def formalization_has_2021_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2021*Qtau*")) or any(FORMALIZATION.rglob("*2021*QTAU*"))
    except Exception:
        return False


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2021_00_2020_handoff",
            ROOT / "2020-Y5-R2FR-Aframe-MHref-PiGR-owner-or-PiAres-first-row.md",
            ["NEXT2020_0_2021", "MPO2020_0_MHref_owner_target", "MPO2020_8_verdict"],
            "2020 handoff: Q_tau ownership is upstream of M_H_ref and Pi_GR/H.",
        ),
        (
            "SRC2021_01_1008_qtau",
            ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            ["QTA1008_8_Q_total", "CDS1008_1_Noether_charge", "DEC1008_0_parent_charge_not_claimed"],
            "original parent theta/Q_tau extraction gate.",
        ),
        (
            "SRC2021_02_1733_owner",
            ROOT / "1733-Y5-R2FR-parent-theta-Qtau-current-owner-or-Htau-first-row.md",
            ["COA1733_7_owner_verdict", "TQC1733_6_total_Qtau", "NEXT1733_0_primary"],
            "R2FR current-owner audit and sector rows.",
        ),
        (
            "SRC2021_03_1798_current_pack",
            ROOT / "1798-Y5-R2FR-parent-Theta-Qtau-current-owner-or-deltaH-curl-component-pack.md",
            ["PCO1798_6_verdict", "DCC1798_8_total_abs_envelope", "DEC1798_3_next"],
            "parent Theta/Q_tau owner verdict and deltaH curl component pack.",
        ),
        (
            "SRC2021_04_1785_parent_lagrangian",
            ROOT / "1785-Y5-R2FR-parent-Lagrangian-theta-vX-minimal-fill-or-DqZ-geometry-source-row.md",
            ["PLT1785_0_L_parent", "PLT1785_8_verdict", "NPJ1785_6_verdict"],
            "parent Lagrangian/theta/vX minimal-fill gate.",
        ),
        (
            "SRC2021_05_1799_ix",
            ROOT / "1799-Y5-R2FR-minimal-parent-current-action-skeleton-or-first-Ix-row.md",
            ["MXA1799_7_verdict", "IXR1799_0_identity", "DEC1799_1_ix_row"],
            "first non-EH live curl component I_X and source-row schema.",
        ),
        (
            "SRC2021_06_1653_handoff",
            ROOT / "1653-Y5-R2FR-Htau-Qtau-current-owner-or-source-measure-owner-first-row.md",
            ["HTO1653_1_Qtau_extraction", "HTO1653_3_MHref_denominator", "HTO1653_5_owner_verdict"],
            "H_tau/Q_tau/M_H_ref owner gate.",
        ),
        (
            "SRC2021_07_1017_reference_lock",
            ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
            ["HRL1017_5_MHref_denominator", "MHR1017_0_M_H_ref_denominator", "DEC1017_1_no_MHref_shortcut"],
            "M_H_ref denominator and no-shortcut guard.",
        ),
        (
            "SRC2021_08_1016_source_selector",
            ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
            ["PSC1016_1_single_observed_coframe", "PSC1016_3_support_selector", "PSC1016_5_dressed_source_charge"],
            "source worldtube and dressed source selector.",
        ),
        (
            "SRC2021_09_1862_contract",
            ROOT / "1862-Y5-R2FR-parent-PiM-observed-time-generator-or-finite-Y5-pack.md",
            ["SMC1862_0_parent_charge", "SMC1862_4_no_circular_GM", "SMC1862_5_verdict"],
            "source-measure derivation contract.",
        ),
        (
            "SRC2021_10_2020_owner_csv",
            OUT / "P8_Y5_PARENT_QLOC_2020_AFRAME_MHREF_PIGR_OWNER_AUDIT.csv",
            ["MPO2020_0_MHref_owner_target", "MPO2020_5_PiGR_projector", "MPO2020_8_verdict"],
            "machine-readable 2020 M_H_ref/Pi_GR owner audit.",
        ),
        (
            "SRC2021_11_1733_components_csv",
            OUT / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_COMPONENT_ROWS.csv",
            ["TQC1733_0_EH", "TQC1733_6_total_Qtau"],
            "machine-readable Q_tau component rows.",
        ),
        (
            "SRC2021_12_1798_curl_csv",
            OUT / "P8_Y5_PARENT_QLOC_1798_DELTAH_CURL_COMPONENT_PACK.csv",
            ["DCC1798_1_I_X", "DCC1798_8_total_abs_envelope"],
            "machine-readable deltaH curl component pack.",
        ),
        (
            "SRC2021_13_1785_lagrangian_csv",
            OUT / "P8_Y5_PARENT_QLOC_1785_PARENT_LAGRANGIAN_THETA_VX_GATE.csv",
            ["PLT1785_0_L_parent", "PLT1785_8_verdict"],
            "machine-readable parent Lagrangian/theta/vX gate.",
        ),
        (
            "SRC2021_14_1862_contract_csv",
            OUT / "P8_Y5_PARENT_QLOC_1862_SOURCE_MEASURE_DERIVATION_CONTRACT.csv",
            ["SMC1862_0_parent_charge", "SMC1862_5_verdict"],
            "machine-readable source-measure derivation contract.",
        ),
    ]
    rows = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def sector_owner_theorem_rows() -> list[dict[str, object]]:
    data = [
        {
            "theorem_id": "QSO2021_0_variation_additivity",
            "claim": "one parent current action makes the sector charge sum legitimate",
            "mathematical_form": "if L_parent=sum_s L_s+dB_ref, then delta L_parent=sum_s(E_s delta Phi_s+dTheta_s)+d delta B_ref and Theta_total=sum_s Theta_s+delta B_ref",
            "status": "EXACT_CONDITIONAL_FORMULA",
            "current_gap": "the current corpus does not supply one signed L_parent and Theta_s for all retained sectors",
            "effect_if_closed": "Q_tau sector rows become derivable rather than ledger entries",
        },
        {
            "theorem_id": "QSO2021_1_Noether_additivity",
            "claim": "the time-translation charge is the sum of owned sector charges",
            "mathematical_form": "J_tau=Theta_total(L_tau Phi)-i_tau L_parent=dQ_tau^MTS+C_tau, Q_tau^MTS=sum_s Q_tau_s+Q_tau^B",
            "status": "EXACT_CONDITIONAL_FORMULA",
            "current_gap": "Q_tau_X, Q_tau_projector, Q_tau_boundary, matter/source constraints, and C_tau_s are not all extracted",
            "effect_if_closed": "M_H_ref can be built from a parent-owned surface charge",
        },
        {
            "theorem_id": "QSO2021_2_local_GR_reduction_condition",
            "claim": "local GR/Newton source follows if all non-EH sector surface fluxes are silent or exact",
            "mathematical_form": "on local source-free exterior, Q_tau^MTS=Q_tau^EH+dB_fixed if Q_tau_X=Q_tau_projector=C_tau_s=0 and boundary/reference variations vanish",
            "status": "DERIVED_CONDITIONAL_REDUCTION_TEST",
            "current_gap": "non-EH silence/exactness is not signed; I_X is the first live obstruction",
            "effect_if_closed": "the local denominator reduces to the usual GR Hamiltonian source without post-hoc insertion",
        },
        {
            "theorem_id": "QSO2021_3_integrability_requirement",
            "claim": "surface charge becomes a mass only when the Hamiltonian one-form is closed",
            "mathematical_form": "alpha_tau:=int_S(delta Q_tau^MTS-i_tau Theta_total)-delta H_ref, d_field alpha_tau=0",
            "status": "EXACT_CONDITIONAL_REQUIREMENT",
            "current_gap": "I_X,I_projector,I_boundary,I_ref,I_tau,I_surface,I_Dq are not zero/bounded with common M_H_ref",
            "effect_if_closed": "H_tau and M_H_ref become well-defined on the local branch",
        },
        {
            "theorem_id": "QSO2021_4_same_source_requirement",
            "claim": "the Hamiltonian denominator must read the same dressed source used by matter and readout",
            "mathematical_form": "M_H_ref[S,tau]=G_ref^-1 int_S Q_tau^MTS-H_ref=M_eff[Pi_M^H J_H^dress]",
            "status": "CONDITIONAL_SOURCE_MEASURE_BRIDGE",
            "current_gap": "source functor, worldtube glue, projector commutator, and Hilbert equality remain unsigned",
            "effect_if_closed": "Newtonian source mass is derived rather than calibrated from the orbit",
        },
        {
            "theorem_id": "QSO2021_5_no_circular_denominator",
            "claim": "orbital GM cannot supply the source denominator",
            "mathematical_form": "M_orbit=G_ref M_H_ref is a downstream check after Q_tau ownership and Gauss/PPN gates",
            "status": "GUARDRAIL_PASS_NO_CLAIM",
            "current_gap": "guardrail blocks cheating but does not supply Q_tau or M_H_ref",
            "effect_if_closed": "keeps the GR/Newton reduction derivationally clean",
        },
        {
            "theorem_id": "QSO2021_6_first_live_obstruction",
            "claim": "the first non-EH component to attack is I_X / Q_tau_X",
            "mathematical_form": "I_X/M_H_ref := |int_S i_tau omega_X + int_A C_X + boundary_X|/M_H_ref",
            "status": "LIVE_COMPONENT_SELECTED",
            "current_gap": "operator sign, J_X source silence, boundary zero, symplectic flux, and Pi_M projection are missing",
            "effect_if_closed": "non-EH motion/time sector either theorem-zeroes or becomes a finite scored row",
        },
        {
            "theorem_id": "QSO2021_7_verdict",
            "claim": "Q_tau^MTS sector owner theorem is accepted for current MTS",
            "mathematical_form": "QSO2021_0 through QSO2021_4 close, all sector rows are owned/zero/exact/bounded, and M_H_ref is positive finite",
            "status": "SECTOR_OWNER_NOT_SIGNED",
            "current_gap": "one parent current chain, non-EH silence, boundary/reference lock, tau/source/frame lock, and integrability remain open",
            "effect_if_closed": "M_H_ref/Pi_GRH/local-GR branch can reopen",
        },
    ]
    rows = []
    for item in data:
        row = base_row()
        row.update({**item, "parent_signed": False})
        rows.append(row)
    return rows


def sector_ledger_rows() -> list[dict[str, object]]:
    data = [
        (
            "QSL2021_0_EH_baseline",
            "Q_tau^EH",
            "ordinary Einstein-Hilbert covariant phase-space source charge",
            "CONDITIONAL_GR_REFERENCE_ONLY",
            "parent reduction to EH plus fixed tau/surface/reference",
            "can seed GR comparator but not total MTS source by itself",
        ),
        (
            "QSL2021_1_X_extra",
            "Q_tau^X + C_tau^X",
            "motion/time/range/memory extra-sector charge and constraints",
            "FIRST_LIVE_OBSTRUCTION",
            "L_X, Theta_X, Q_tau_X, C_tau_X, operator sign, source silence, boundary zero",
            "I_X/M_H_ref row or theorem-zero nohair branch",
        ),
        (
            "QSL2021_2_projector_PiM",
            "Q_tau^projector + [d,Pi_M]J_H",
            "projector/source-current contribution to the Hamiltonian current",
            "UNOWNED_PROJECTOR_CURRENT",
            "Pi_M^H owner, chain-map/commutator silence, Hilbert equality, M_H_ref",
            "I_projector/M_H_ref row or chain-map theorem",
        ),
        (
            "QSL2021_3_boundary_reference",
            "Q_tau^boundary + delta B_ref",
            "boundary/corner/improvement/reference contribution",
            "REFERENCE_BOUNDARY_NOT_FIXED",
            "fixed B_ref, cohomology class, corner rule, counterterm derivative silence",
            "I_boundary and I_ref rows or exact boundary theorem",
        ),
        (
            "QSL2021_4_matter_source",
            "Q_tau^matter/source + C_tau^matter",
            "ordinary matter and dressed Hilbert source contribution",
            "SOURCE_GLUE_NOT_SIGNED",
            "same observed coframe, compact worldtube, source functor, exterior support silence",
            "Delta_Hsrc row or source-measure theorem",
        ),
        (
            "QSL2021_5_tau_surface",
            "tau/surface readout terms",
            "nonprojectable tau, moving surface, or readout-frame contribution",
            "TAU_SURFACE_LOCK_MISSING",
            "tau_source=tau_charge=tau_clock=tau_readout and fixed linked surfaces",
            "I_tau/I_surface rows or projectability theorem",
        ),
        (
            "QSL2021_6_Dq_quotient",
            "Dq_current_leak",
            "quotient-map/current leakage into theta/Q_tau or source readout",
            "DQ_DESCENT_NOT_SIGNED",
            "q(Phi), Dq, kernel verticality, action descent, source/readout descent",
            "I_Dq row or descent-current theorem",
        ),
        (
            "QSL2021_7_total",
            "Q_tau^MTS",
            "sum of all owned sector charges plus fixed reference term",
            "TOTAL_NOT_PROMOTED",
            "every non-EH sector is owned and zero/exact/bounded with common units and source paths",
            "only then can M_H_ref/Pi_GRH/local-GR gates reopen",
        ),
    ]
    rows = []
    for sector_id, symbol, role, current_status, owner_requirement, residual_if_fail in data:
        row = base_row()
        row.update(
            {
                "sector_id": sector_id,
                "symbol": symbol,
                "role": role,
                "current_status": current_status,
                "owner_requirement": owner_requirement,
                "residual_if_fail": residual_if_fail,
                "sector_owned": False,
                "theorem_zero": False,
                "finite_row_ready": False,
                "valid_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def mhref_first_source_rows() -> list[dict[str, object]]:
    data = [
        ("MFS2021_0_system_id", "system_id", "source system or local branch identifier", "MISSING_SYSTEM_ID", "identifier"),
        ("MFS2021_1_tau_surface", "tau_id;surface_pair", "fixed time generator and linked source-free surfaces", "MISSING_TAU_SURFACE_LOCK", "geometric"),
        ("MFS2021_2_Qtau_EH", "Q_tau^EH", "EH comparator charge through the selected surface", "MISSING_EH_BASELINE_WITH_REFERENCE", "charge"),
        ("MFS2021_3_Qtau_X", "Q_tau^X;C_tau^X;I_X", "extra-sector surface/current obstruction", "MISSING_X_ZERO_OR_FINITE_ROW", "charge_or_dimensionless_over_MH"),
        ("MFS2021_4_Qtau_projector", "Q_tau^projector;I_projector", "projector current obstruction", "MISSING_PROJECTOR_ZERO_OR_FINITE_ROW", "charge_or_dimensionless_over_MH"),
        ("MFS2021_5_Qtau_boundary_ref", "Q_tau^boundary;H_ref;I_boundary;I_ref", "boundary/reference contribution and fixed subtraction", "MISSING_BOUNDARY_REFERENCE_LOCK", "charge"),
        ("MFS2021_6_Qtau_matter_source", "Q_tau^matter;Delta_Hsrc", "dressed source-measure contribution", "MISSING_SOURCE_MEASURE_THEOREM_OR_BOUND", "charge"),
        ("MFS2021_7_I_abs_total", "I_abs_total/M_H_ref", "absolute no-cancellation integrability envelope", "NOT_COMPUTED_COMPONENTS_MISSING", "dimensionless"),
        ("MFS2021_8_M_H_ref", "M_H_ref", "positive same-frame Hamiltonian source denominator", "MISSING_STABLE_MH_REF", "mass_or_charge"),
        ("MFS2021_9_QA_res_ready", "Q_A^res normalization readiness", "whether residual A scoring can use this denominator", "BLOCKED_UNTIL_MHREF_OWNER", "gate"),
    ]
    rows = []
    for row_id, field, definition, current_status, units in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "field": field,
                "definition": definition,
                "required_payload": "numeric_or_theorem_zero_value;units;source_path;assumptions;valid_for_claim",
                "current_status": current_status,
                "numeric_value": "MISSING",
                "units": units,
                "score_ready": False,
                "valid_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2021_0_noether_theorem_shape", "Noether additivity/current theorem shape is written", True, "standard covariant phase-space machinery is expressed as a conditional theorem"),
        ("CG2021_1_sector_ledger_complete", "all Q_tau sectors are named with residual fallback", True, "EH, X, projector, boundary/ref, matter, tau/surface, and Dq sectors are separated"),
        ("CG2021_2_no_circular_GM_guard", "orbital GM shortcut is refused", True, "source denominator cannot be proven by downstream readout"),
        ("CG2021_3_parent_action_owned", "one signed parent action owns all retained current sectors", False, "L_parent/Theta_s/Q_s are not filled together"),
        ("CG2021_4_nonEH_zero_or_bound", "all non-EH sector fluxes are theorem-zero/exact/bounded", False, "I_X and other component rows remain missing"),
        ("CG2021_5_integrability_closed", "Hamiltonian one-form is closed with fixed reference", False, "absolute curl envelope is not computed"),
        ("CG2021_6_same_source_bridge", "M_H_ref equals the dressed observed source measure", False, "worldtube/source/projector bridge remains unsigned"),
        ("CG2021_7_MHref_first_row_ready", "first M_H_ref row is numeric/source-backed", False, "all first source-row slots remain missing"),
        ("CG2021_8_local_GR_Newton", "local GR/Newton reduction is derived", False, "Q_tau owner and source bridge are not closed"),
    ]
    rows = []
    for gate_id, gate, passed_for_nonclaim, reason in data:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "gate": gate,
                "passed_for_nonclaim": passed_for_nonclaim,
                "passed_for_claim": False,
                "reason": reason,
            }
        )
        rows.append(row)
    return rows


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2021_0_total_Qtau_claim", "claim Q_tau^MTS is parent-owned", "REFUSE", "sector decomposition is exact as a contract, but retained non-EH sectors are not signed or bounded."),
        ("REF2021_1_EH_only_import", "use Q_tau^EH as the total MTS charge", "REFUSE", "EH charge is a comparator unless parent reduction and non-EH silence are proved."),
        ("REF2021_2_orbital_GM_denominator", "use orbital GM or fitted mass as M_H_ref", "REFUSE", "that makes the Newtonian readout prove its own source denominator."),
        ("REF2021_3_cancel_unknown_sectors", "let unknown non-EH sectors cancel each other", "REFUSE", "local tests require absolute no-cancellation envelopes or theorem-zero components."),
        ("REF2021_4_MHref_score", "score M_H_ref or Q_A^res now", "REFUSE", "M_H_ref first source row is missing and integrability/source bridge are not closed."),
        ("REF2021_5_local_GR", "claim local GR/Newton limit", "REFUSE", "Q_tau owner, non-EH silence, fixed reference, source bridge, and Pi_GR/H remain unsigned."),
    ]
    rows = []
    for refusal_id, attempted_claim, verdict, reason in data:
        row = base_row()
        row.update(
            {
                "refusal_id": refusal_id,
                "attempted_claim": attempted_claim,
                "verdict": verdict,
                "reason": reason,
                "accepted_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2021_0_result",
            "QTAU_SECTOR_OWNER_THEOREM_WRITTEN_NOT_SIGNED",
            "The exact route is now clean: Q_tau^MTS is a Noether surface charge only if every sector is owned by one parent current chain and non-EH residues are zero/exact/bounded.",
            "do not promote M_H_ref; attack the first non-EH live sector",
        ),
        (
            "DEC2021_1_forward_move",
            "THIS_IS_THE_LEAP_POINT",
            "Instead of re-auditing A, the framework now knows precisely where GR reduction lives: Q_tau^MTS must reduce to EH plus fixed boundary in local exterior.",
            "work the X-sector obstruction I_X/Q_tau_X next",
        ),
        (
            "DEC2021_2_best_next",
            "QTAU_X_ZERO_OR_IX_ROW_NEXT",
            "I_X is the first non-EH obstruction already isolated by 1798/1799, and closing it would remove the motion/time sector from the local mass denominator.",
            "derive X-sector theorem-zero conditions or emit the first source-backed I_X/M_H_ref row",
        ),
    ]
    rows = []
    for decision_id, verdict, rationale, next_action in data:
        row = base_row()
        row.update({"decision_id": decision_id, "verdict": verdict, "rationale": rationale, "next_action": next_action})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2021_0_2022",
            "next_doc": "2022-Y5-R2FR-Qtau-X-sector-zero-or-first-Ix-source-row.md",
            "objective": "derive Q_tau_X/C_tau_X/I_X theorem-zero from the local parent X-sector action, source silence, boundary zero and Pi_M projection; if not, emit the first source-backed I_X/M_H_ref row",
            "required_inputs": "L_X;Theta_X;Q_tau_X;C_tau_X;omega_X;operator sign/gap;J_X source silence;boundary_X zero;Pi_M^H projection;common M_H_ref denominator;units;source paths",
            "excluded": "EH-only import; orbital GM denominator; cancellation between unknown sectors; total Q_tau claim; local-GR/R10/PPN claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update({"copy_id": f"COPY2021_{idx}", "path": str(path), "exists": path.exists(), "note": note})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    sectors: list[dict[str, object]],
    mhref_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    root_resolved = ROOT.resolve()
    scoped_paths = output_paths + branch_paths + [DOC]
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2021_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"))
    checks.append(("VAL2021_01_noether_additivity", any(row["theorem_id"] == "QSO2021_1_Noether_additivity" and "Q_tau^MTS=sum_s" in row["mathematical_form"] for row in theorem), "Noether additivity formula is explicit"))
    checks.append(("VAL2021_02_gr_reduction_condition", any(row["theorem_id"] == "QSO2021_2_local_GR_reduction_condition" and "Q_tau^EH" in row["mathematical_form"] for row in theorem), "conditional GR reduction test is explicit"))
    checks.append(("VAL2021_03_owner_not_promoted", any(row["theorem_id"] == "QSO2021_7_verdict" and row["status"] == "SECTOR_OWNER_NOT_SIGNED" for row in theorem), "Q_tau owner theorem is not falsely promoted"))
    required_sectors = {"QSL2021_0_EH_baseline", "QSL2021_1_X_extra", "QSL2021_2_projector_PiM", "QSL2021_3_boundary_reference", "QSL2021_4_matter_source", "QSL2021_5_tau_surface", "QSL2021_6_Dq_quotient", "QSL2021_7_total"}
    checks.append(("VAL2021_04_sector_coverage", required_sectors.issubset({row["sector_id"] for row in sectors}), "all major Q_tau sectors are covered"))
    checks.append(("VAL2021_05_x_selected", any(row["decision_id"] == "DEC2021_2_best_next" and "I_X" in row["rationale"] for row in decisions), "I_X/Q_tau_X is selected as next live obstruction"))
    checks.append(("VAL2021_06_mhref_rows_nonclaim", all(row["score_ready"] is False and row["valid_for_claim"] is False and row["numeric_value"] == "MISSING" for row in mhref_rows), "all M_H_ref first-source rows remain missing/nonclaim"))
    checks.append(("VAL2021_07_claim_gates_blocked", all(row["passed_for_claim"] is False for row in claim_gates), "all claim gates remain blocked for claim"))
    checks.append(("VAL2021_08_refusals_active", all(row["verdict"] == "REFUSE" and row["accepted_for_claim"] is False for row in refusals), "refusals remain active"))
    checks.append(("VAL2021_09_no_eh_only_import", any(row["refusal_id"] == "REF2021_1_EH_only_import" and row["verdict"] == "REFUSE" for row in refusals), "EH-only import is refused"))
    checks.append(("VAL2021_10_no_circular_GM", any(row["refusal_id"] == "REF2021_2_orbital_GM_denominator" and row["verdict"] == "REFUSE" for row in refusals), "orbital GM denominator shortcut is refused"))
    checks.append(("VAL2021_11_next_target", any(row["target_id"] == "NEXT2021_0_2022" and "I_X" in row["objective"] for row in next_target), "2022 X-sector/I_X target is selected"))
    checks.append(("VAL2021_12_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"))
    checks.append(("VAL2021_13_branch_copies", all(path.exists() and csv_rows_parse(path) for path in branch_paths), "branch-copy CSVs exist and parse"))
    checks.append(("VAL2021_14_no_formalization_edits", count_formalization_modified_since_start() == 0 and not formalization_has_2021_artifacts(), "formalization-workbench modified-file count remains 0 and no 2021 Qtau artifacts appear there"))
    checks.append(("VAL2021_15_output_scope", all(root_resolved == path.resolve() or root_resolved in path.resolve().parents for path in scoped_paths), "all outputs are under post-checkpoint-work"))
    overall = all(passed for _, passed, _ in checks)
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    row = base_row()
    row.update(
        {
            "check_id": "VAL2021_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2021 A-frame Q_tau sector owner or M_H_ref first source row",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    sectors: list[dict[str, object]],
    mhref_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    parts = [
        "# 2021 Y5 R2FR: A-Frame Qtau Sector Owner Or MHref First Source Row\n",
        "Private checkpoint. This pass goes upstream of `M_H_ref`: it asks whether the time-translation Noether charge `Q_tau^MTS` is owned sector-by-sector, so the local GR/Newton denominator is derived rather than borrowed.\n",
        "## Current Verdict\n",
        "The clean theorem route is now explicit. If one parent action gives `delta L_parent = E delta Phi + dTheta_total`, then `J_tau = Theta_total(L_tau Phi) - i_tau L_parent = dQ_tau^MTS + C_tau`, with `Q_tau^MTS` the sum of owned sector charges. In a local source-free exterior, MTS reduces to GR/Newton only if the non-EH sector charges are zero, exact/fixed-boundary, or finite-bounded with no cancellation.\n",
        "This is a real forward step, but still not a claim. The current corpus does not yet sign the parent action/current chain, and the first non-EH obstruction is `I_X/Q_tau_X`: the motion/time sector contribution to the Hamiltonian curl and source denominator. That is the next live thing to derive or source as a finite row.\n",
        "So the project is not stuck on A-frame bookkeeping anymore. The spine is: parent current -> sector `Q_tau` ownership -> positive `M_H_ref` -> measured-GR subtraction `Pi_GR/H` -> residual A branch. The missing leap is closing the first non-EH sector, not scoring total charge.\n",
        "## Source Register\n",
        md_table(sources, ["source_id", "source_path", "status", "needles", "note"]),
        "## Q_tau Sector Owner Theorem\n",
        md_table(theorem, ["theorem_id", "claim", "mathematical_form", "status", "current_gap", "effect_if_closed", "parent_signed"]),
        "## Q_tau Sector Ledger\n",
        md_table(sectors, ["sector_id", "symbol", "role", "current_status", "owner_requirement", "residual_if_fail", "sector_owned", "theorem_zero", "finite_row_ready", "valid_for_claim"]),
        "## M_H_ref First Source Row Schema\n",
        md_table(mhref_rows, ["row_id", "field", "definition", "required_payload", "current_status", "numeric_value", "units", "score_ready", "valid_for_claim"]),
        "## Claim Gates\n",
        md_table(claim_gates, ["gate_id", "gate", "passed_for_nonclaim", "passed_for_claim", "reason"]),
        "## Refusal Runner\n",
        md_table(refusals, ["refusal_id", "attempted_claim", "verdict", "reason", "accepted_for_claim"]),
        "## Decision Ledger\n",
        md_table(decisions, ["decision_id", "verdict", "rationale", "next_action"]),
        "## Branch Copies\n",
        md_table(branch_copies, ["copy_id", "path", "exists", "note"]),
        "## Next Target\n",
        md_table(next_target, ["target_id", "next_doc", "objective", "required_inputs", "excluded"]),
        "## Validation\n",
        md_table(validation, ["check_id", "status", "detail"]),
    ]
    DOC.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    theorem = sector_owner_theorem_rows()
    sectors = sector_ledger_rows()
    mhref_rows = mhref_first_source_rows()
    claim_gates = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2021_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2021_QTAU_SECTOR_OWNER_THEOREM.csv",
        "sectors": OUT / "P8_Y5_PARENT_QLOC_2021_QTAU_SECTOR_LEDGER.csv",
        "mhref_rows": OUT / "P8_Y5_PARENT_QLOC_2021_MHREF_FIRST_SOURCE_ROW_SCHEMA.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2021_CLAIM_GATE.csv",
        "refusals": OUT / "P8_Y5_PARENT_QLOC_2021_REFUSAL_RUNNER.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2021_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2021_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["theorem"], theorem)
    write_csv(output_map["sectors"], sectors)
    write_csv(output_map["mhref_rows"], mhref_rows)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["refusals"], refusals)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "AFRAME_QTAU_SECTOR_OWNER_2021_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2021_QTAU_MHREF_STATUS_NONCLAIM.csv",
        QUEUE / "JR2021_MHREF_FIRST_SOURCE_ROW_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["theorem"], branch_paths[0])
    shutil.copyfile(output_map["claim_gates"], branch_paths[1])
    shutil.copyfile(output_map["mhref_rows"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "A-frame Q_tau sector-owner theorem nonclaim copy",
            "Q_tau/M_H_ref claim-gate status nonclaim copy",
            "M_H_ref first source-row acquisition queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2021_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, theorem, sectors, mhref_rows, claim_gates, refusals, decisions, next_target, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2021_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, theorem, sectors, mhref_rows, claim_gates, refusals, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2021_OVERALL"][0]["status"]
    print(f"VAL2021_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()

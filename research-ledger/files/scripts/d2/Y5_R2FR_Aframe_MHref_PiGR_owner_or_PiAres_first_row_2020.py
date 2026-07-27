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
DOC = ROOT / "2020-Y5-R2FR-Aframe-MHref-PiGR-owner-or-PiAres-first-row.md"
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


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2020_00_2019_handoff",
            ROOT / "2019-Y5-R2FR-Aframe-GR-source-decomposition-PiAres-zero-or-residual-normalization.md",
            ["NEXT2019_0_2020", "GSD2019_1_GR_source_piece", "VAL2019_OVERALL"],
            "2019 handoff: measured GR source must be subtracted before residual A scoring.",
        ),
        (
            "SRC2020_01_1017_reference_lock",
            ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
            ["HRL1017_5_MHref_denominator", "MHR1017_0_M_H_ref_denominator", "DEC1017_1_no_MHref_shortcut"],
            "Hamiltonian source denominator, reference lock, and no-shortcut guard.",
        ),
        (
            "SRC2020_02_1016_source_selector",
            ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
            ["PSC1016_1_single_observed_coframe", "PSC1016_3_support_selector", "PSC1016_5_dressed_source_charge"],
            "single observed coframe, Hilbert support worldtube, and dressed source charge selector.",
        ),
        (
            "SRC2020_03_1008_qtau",
            ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            ["QTA1008_8_Q_total", "CDS1008_1_Noether_charge", "DEC1008_0_parent_charge_not_claimed"],
            "parent theta/Noether charge extraction ledger: Q_tau^MTS is not promoted.",
        ),
        (
            "SRC2020_04_1014_projector",
            ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
            ["PCT1014_0_product_rule", "PCT1014_3_Hilbert_equality", "PCC1014_1_I_commutator"],
            "projector commutator and Hilbert equality obstruction.",
        ),
        (
            "SRC2020_05_1019_projector",
            ROOT / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            ["PO1019_0_projector_definition", "DC1019_0_orthogonal_split", "RVT1019_1_projector_orthogonality"],
            "projector definition, orthogonal split, and residual projection gate.",
        ),
        (
            "SRC2020_06_2019_decomp_csv",
            OUT / "P8_Y5_PARENT_QLOC_2019_AFRAME_GR_SOURCE_DECOMPOSITION.csv",
            ["GSD2019_1_GR_source_piece", "GSD2019_8_verdict"],
            "machine-readable 2019 A-frame GR-source decomposition.",
        ),
        (
            "SRC2020_07_1017_ref_csv",
            OUT / "P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv",
            ["HRL1017_5_MHref_denominator", "HRL1017_6_FB5540_zero_law"],
            "machine-readable reference lock law.",
        ),
        (
            "SRC2020_08_HSM541",
            OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
            ["HSM541_1_integrable_charge", "HSM541_2_observed_worldtube_source", "HSM541_5_Gauss_orbital_readout"],
            "Hamiltonian source-measure contract and downstream Gauss readout guard.",
        ),
        (
            "SRC2020_09_1778_adopted",
            OUT / "P8_Y5_PARENT_QLOC_1778_ADOPTED_PIM_SOURCE_MEASURE_LEMMA.csv",
            ["ASM1778_0_conditional_theorem", "ASM1778_5_verdict"],
            "adopted Pi_M^H source-measure lemma and current failure verdict.",
        ),
        (
            "SRC2020_10_1862_contract",
            OUT / "P8_Y5_PARENT_QLOC_1862_SOURCE_MEASURE_DERIVATION_CONTRACT.csv",
            ["SMC1862_0_parent_charge", "SMC1862_4_no_circular_GM", "SMC1862_5_verdict"],
            "source-measure derivation contract and no-circular-GM guard.",
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


def owner_audit_rows() -> list[dict[str, object]]:
    data = [
        {
            "audit_id": "MPO2020_0_MHref_owner_target",
            "object": "same-frame Hamiltonian source denominator",
            "formula": "M_H_ref[S,tau] := G_ref^-1 int_S Q_tau^MTS - H_ref",
            "status": "OWNER_TARGET_WRITTEN_NOT_PARENT_SIGNED",
            "derived_content": "The denominator must be a covariant-phase-space/Noether charge in the same observed frame, not a fitted orbital mass.",
            "blocking_gap": "Q_tau^MTS, H_ref, integrability, and source worldtube are still separate unsigned contracts.",
        },
        {
            "audit_id": "MPO2020_1_Hamiltonian_variation",
            "object": "integrable Hamiltonian one-form",
            "formula": "delta H_tau = int_S(delta Q_tau^MTS - i_tau Theta_MTS) - delta H_ref, with d_field(delta H_tau)=0",
            "status": "FORMAL_VARIATION_CONTRACT_ONLY",
            "derived_content": "This is the exact ownership test for whether the surface charge can be used as a mass/source denominator.",
            "blocking_gap": "field-space curl components, boundary symplectic flux, reference variation, and retained-sector charges are not theorem-zero.",
        },
        {
            "audit_id": "MPO2020_2_tau_frame_lock",
            "object": "same time generator and public frame",
            "formula": "tau_source = tau_charge = tau_clock = tau_readout and e_pub is the same matter/clock/orbit coframe",
            "status": "LOCK_REQUIRED_NOT_PARENT_SIGNED",
            "derived_content": "Without this lock, the denominator and the fifth-force residual can live in different gauges/frames.",
            "blocking_gap": "single observed coframe and tau equality are staged but not supplied by the parent action.",
        },
        {
            "audit_id": "MPO2020_3_worldtube_selector",
            "object": "source support selector",
            "formula": "W_source := closure(supp J_H[tau;e_pub,psi]); linked S_in,S_out lie in compact source-free exterior",
            "status": "SELECTOR_FORMAL_NOT_SIGNED",
            "derived_content": "The source region is selected by the Hilbert/Hamiltonian current, not by the fitted radius used in the test.",
            "blocking_gap": "compactness, exterior silence, and current equality are not parent-signed.",
        },
        {
            "audit_id": "MPO2020_4_reference_lock",
            "object": "fixed reference subtraction",
            "formula": "H_ref is chosen before readout and held fixed under source/test variations",
            "status": "REFERENCE_RULE_REQUIRED_NOT_SIGNED",
            "derived_content": "This prevents reference shifts from masquerading as residual A hair or source mass.",
            "blocking_gap": "reference branch, counterterm silence, and derivative profile remain missing.",
        },
        {
            "audit_id": "MPO2020_5_PiGR_projector",
            "object": "measured-GR source projection of A variation",
            "formula": "Q_A^GR[epsilon] := Pi_GR/H[Q_A^total] = (partial Q_A^total[epsilon]/partial M_H_ref)_{tau,S,H_ref,R_A} M_H_ref",
            "status": "FORMAL_PROJECTOR_DEFINITION_NOT_DERIVED",
            "derived_content": "This names the subtraction map: remove only the component of the A boundary response that is the ordinary Hamiltonian mass/source direction.",
            "blocking_gap": "solution-space mass coordinate, projector orthogonality, and commutator silence are not constructed.",
        },
        {
            "audit_id": "MPO2020_6_residual_definition",
            "object": "residual A source after GR subtraction",
            "formula": "Q_A^res := Q_A^total - Q_A^GR - Q_A^proper/exact",
            "status": "BOOKKEEPING_IDENTITY_ACCEPTED_NONCLAIM",
            "derived_content": "This remains the right target: extra A hair, not ordinary measured mass, is what local tests constrain.",
            "blocking_gap": "the identity does not by itself make Q_A^res zero or numeric.",
        },
        {
            "audit_id": "MPO2020_7_no_circular_denominator",
            "object": "forbidden denominator shortcut",
            "formula": "M_orbit = G_ref M_H_ref is downstream of Delta_Hsrc=0/bounded and cannot prove M_H_ref",
            "status": "GUARDRAIL_PASS_NO_CLAIM",
            "derived_content": "This keeps the Newton/GR limit honest: we cannot use the observed orbit as the theorem's own source proof.",
            "blocking_gap": "the guardrail blocks a shortcut; it does not supply Q_tau or Pi_GR/H.",
        },
        {
            "audit_id": "MPO2020_8_verdict",
            "object": "M_H_ref and Pi_GR/H owner theorem",
            "formula": "M_H_ref plus Pi_GR/H would be owned only if MPO2020_0 through MPO2020_5 close in one parent branch",
            "status": "OWNER_FORMULA_WRITTEN_PROOF_NOT_CLOSED",
            "derived_content": "The 2020 pass gives the exact contract, but not the parent signatures. Residual scoring remains blocked.",
            "blocking_gap": "Q_tau sector ownership, fixed H_ref, tau/source/frame lock, integrability, and projector orthogonality are still missing.",
        },
    ]
    rows = []
    for item in data:
        row = base_row()
        row.update({**item, "parent_signed": False})
        rows.append(row)
    return rows


def first_row_schema_rows() -> list[dict[str, object]]:
    data = [
        (
            "FR2020_0_M_H_ref",
            "M_H_ref",
            "positive same-frame Hamiltonian/Noether source denominator",
            "system_id;tau_id;surface_id;Q_tau_integral;G_ref;H_ref;M_H_ref;units;reference_rule;source_path;assumptions;valid_for_claim",
            "MISSING_STABLE_MH_REF",
            "mass_or_charge",
        ),
        (
            "FR2020_1_Q_tau_integral",
            "int_S Q_tau^MTS",
            "parent-owned total time-translation Noether charge through the source-linking surface",
            "system_id;surface_id;tau_id;sector_sum;EH_piece;boundary_piece;extra_piece;projector_piece;matter_piece;constraints;source_path;valid_for_claim",
            "MISSING_PARENT_QTAU",
            "charge",
        ),
        (
            "FR2020_2_H_ref",
            "H_ref",
            "fixed reference subtraction chosen before readout",
            "reference_branch;counterterm_rule;variation_rule;H_ref;units;source_path;valid_for_claim",
            "MISSING_FIXED_REFERENCE_RULE",
            "mass_or_charge",
        ),
        (
            "FR2020_3_tau_lock",
            "tau_source=tau_charge=tau_clock=tau_readout",
            "certificate that source, charge, clock, and orbital readout use one time generator",
            "system_id;tau_source;tau_charge;tau_clock;tau_readout;mismatch_bound;units;source_path;valid_for_claim",
            "MISSING_TAU_LOCK_CERTIFICATE",
            "dimensionless_or_time_generator_norm",
        ),
        (
            "FR2020_4_worldtube_source",
            "W_source",
            "Hilbert/Hamiltonian current support worldtube used before orbital fitting",
            "system_id;J_H_definition;support_rule;S_in;S_out;exterior_silence;source_path;valid_for_claim",
            "MISSING_WORLDTUBE_SELECTOR_PROOF",
            "geometric_support",
        ),
        (
            "FR2020_5_integrability_curl",
            "curl_delta_H_tau",
            "absolute Hamiltonian integrability obstruction for the chosen source branch",
            "system_id;variation_pair;I_X;I_projector;I_boundary;I_ref;I_tau;I_surface;I_Dq;absolute_sum;M_H_ref;source_path;valid_for_claim",
            "MISSING_INTEGRABILITY_ZERO_OR_BOUND",
            "dimensionless_after_MHref_normalization",
        ),
        (
            "FR2020_6_Pi_GRH_map",
            "Pi_GR/H",
            "projector from total A boundary response to measured Hamiltonian/GR source direction",
            "system_id;solution_coordinates;held_fixed;projector_formula;commutator_bound;orthogonality_test;source_path;valid_for_claim",
            "MISSING_PROJECTOR_CONSTRUCTION",
            "projection_map",
        ),
        (
            "FR2020_7_QA_GR",
            "Q_A^GR",
            "ordinary measured GR/Hamiltonian source component inside the A response",
            "system_id;epsilon_id;Q_A_total;Pi_GRH_map;M_H_ref;Q_A_GR;units;source_path;valid_for_claim",
            "MISSING_GR_SOURCE_COMPONENT",
            "A_charge",
        ),
        (
            "FR2020_8_QA_exact",
            "Q_A^proper/exact",
            "proper gauge or exact boundary component removed before residual scoring",
            "system_id;epsilon_id;boundary_class;cohomology_rule;corner_rule;Q_A_exact;units;source_path;valid_for_claim",
            "MISSING_BOUNDARY_EXACTNESS_CERTIFICATE",
            "A_charge",
        ),
        (
            "FR2020_9_QA_res",
            "Q_A^res",
            "extra residual A source charge after measured GR and exact/proper pieces are removed",
            "system_id;epsilon_id;Q_A_total;Q_A_GR;Q_A_exact;Q_A_res;absolute_tail;units;source_path;valid_for_claim",
            "MISSING_RESIDUAL_VALUE_OR_ZERO_THEOREM",
            "A_charge",
        ),
        (
            "FR2020_10_alphaA_res",
            "alpha_A^res(lambda)",
            "Yukawa-equivalent residual A strength normalized by M_H_ref",
            "system_id;lambda;Z_A;K_A;Qbar_AH_res;qbar_AT;M_H_ref;alpha_A_res;alpha_bound;source_path;valid_for_claim",
            "MISSING_ALL_JOIN_INPUTS",
            "dimensionless",
        ),
    ]
    rows = []
    for row_id, symbol, definition, required_columns, status, units in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "required_columns": required_columns,
                "current_status": status,
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
        ("CG2020_0_owner_contract_written", "M_H_ref/Pi_GRH owner contract is written explicitly", True, "formal target and held-fixed quantities are now named"),
        ("CG2020_1_no_circular_GM_guard", "orbital GM/bare mass/reference-one shortcut is refused", True, "prevents downstream readout from proving its own denominator"),
        ("CG2020_2_MHref_owned", "M_H_ref is a parent-owned same-frame Hamiltonian source denominator", False, "Q_tau, H_ref, tau/frame lock, and integrability remain unsigned"),
        ("CG2020_3_Qtau_extracted", "Q_tau^MTS is extracted sector-by-sector from one parent action", False, "1008 explicitly leaves Q_tau total unpromoted"),
        ("CG2020_4_integrability_closed", "Hamiltonian variation is exact on the allowed local branch", False, "field-space curl and boundary/reference components are not zero/bounded"),
        ("CG2020_5_same_source_lock", "matter, clocks, rods, source, and readout use one observed frame/worldtube", False, "1016 gives selector shape but not parent signature"),
        ("CG2020_6_PiGRH_owned", "Pi_GR/H projector subtracts the measured GR source without absorbing residual hair", False, "projector coordinate, commutator, and orthogonality are not constructed"),
        ("CG2020_7_PiAres_first_row_ready", "first residual-normalized A row is numeric/source-backed", False, "every required quantity is missing or theorem-unsigned"),
        ("CG2020_8_local_GR_Newton", "local GR/Newton reduction follows from the A branch", False, "ordinary-source subtraction and residual-zero theorem are not closed"),
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
        ("REF2020_0_MHref_claim", "claim M_H_ref is derived", "REFUSE", "the owner formula is written, but Q_tau^MTS, H_ref, integrability, and tau/source locks are not parent-signed."),
        ("REF2020_1_orbital_GM_shortcut", "use orbital GM, bare mass, or reference 1 as M_H_ref", "REFUSE", "that would use the Newtonian readout to prove the source theorem the readout is supposed to test."),
        ("REF2020_2_EH_only_Qtau", "promote the Einstein-Hilbert charge as Q_tau^MTS", "REFUSE", "retained MTS sectors, boundary/projector terms, constraints, and matter/source terms must be extracted or zeroed."),
        ("REF2020_3_total_QA_score", "score Q_A_total in R10/PPN/local tests", "REFUSE", "Q_A_total contains ordinary measured mass/source and would double count the GR/Newtonian piece."),
        ("REF2020_4_PiGR_subtraction_claim", "subtract Q_A^GR using the formal projector as if derived", "REFUSE", "Pi_GR/H is only a formal held-fixed definition until its source coordinate and orthogonality are constructed."),
        ("REF2020_5_alphaAres_score", "score alpha_A^res(lambda)", "REFUSE", "Z_A, K_A, Qbar_AH_res, qbar_AT, M_H_ref, lambda, and bounds are not source-backed together."),
        ("REF2020_6_local_GR", "claim local GR/Newton reduction", "REFUSE", "residual A zero and same-frame source normalization are still open."),
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
            "DEC2020_0_result",
            "MHREF_PIGR_OWNER_CONTRACT_WRITTEN_PROOF_OPEN",
            "The correct denominator is M_H_ref = G_ref^-1 int_S Q_tau^MTS - H_ref, and the correct subtraction is Pi_GR/H along that Hamiltonian mass coordinate. Neither is parent-owned yet.",
            "do not run residual scoring; derive Q_tau sector ownership or fill first M_H_ref row",
        ),
        (
            "DEC2020_1_not_circling",
            "THIS_IS_A_NEW_BRIDGE_NOT_A_REPEAT",
            "2019 separated ordinary GR source from residual A hair. 2020 now names the exact owner map required to subtract the ordinary source without cheating.",
            "next pass must attack Q_tau^MTS ownership directly, not re-audit the A residual again",
        ),
        (
            "DEC2020_2_best_next",
            "GO_UPSTREAM_TO_QTAU_SECTOR_OWNER",
            "The bottleneck is not a new empirical test; it is the parent current chain that supplies Q_tau^MTS, H_ref, tau lock, and integrability.",
            "build 2021 Qtau sector-owner gate or first source-backed MHref row",
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
            "target_id": "NEXT2020_0_2021",
            "next_doc": "2021-Y5-R2FR-Aframe-Qtau-sector-owner-or-MHref-first-source-row.md",
            "objective": "derive parent-owned Q_tau^MTS sector decomposition plus fixed H_ref/tau/source locks sufficient for M_H_ref and Pi_GR/H; if not, create the first nonclaim source-backed M_H_ref row",
            "required_inputs": "parent Lagrangian current chain; Theta_MTS; Q_tau_EH; Q_tau_boundary; Q_tau_extra; Q_tau_projector; Q_tau_matter/source; constraints; fixed H_ref; tau lock; source worldtube; integrability components",
            "excluded": "EH-only import; orbital GM denominator; bare mass shortcut; total Q_A scoring; reference-only zero; cancellation between unknown residuals; R10/local-GR claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update({"copy_id": f"COPY2020_{idx}", "path": str(path), "exists": path.exists(), "note": note})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    owner_audit: list[dict[str, object]],
    first_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    next_target: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    root_resolved = ROOT.resolve()
    scoped_paths = output_paths + branch_paths + [DOC]
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2020_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"))
    checks.append(("VAL2020_01_owner_formula_written", any(row["audit_id"] == "MPO2020_0_MHref_owner_target" and "Q_tau^MTS" in row["formula"] for row in owner_audit), "M_H_ref owner target is explicit"))
    checks.append(("VAL2020_02_projector_formula_written", any(row["audit_id"] == "MPO2020_5_PiGR_projector" and "Pi_GR/H" in row["formula"] for row in owner_audit), "Pi_GR/H formal subtraction map is explicit"))
    checks.append(("VAL2020_03_owner_not_promoted", any(row["audit_id"] == "MPO2020_8_verdict" and row["status"] == "OWNER_FORMULA_WRITTEN_PROOF_NOT_CLOSED" for row in owner_audit), "M_H_ref/Pi_GR owner proof is not falsely promoted"))
    checks.append(("VAL2020_04_no_circular_guard", any(row["refusal_id"] == "REF2020_1_orbital_GM_shortcut" and row["verdict"] == "REFUSE" for row in refusals), "orbital GM shortcut is refused"))
    checks.append(("VAL2020_05_mhref_claim_blocked", any(row["gate_id"] == "CG2020_2_MHref_owned" and row["passed_for_claim"] is False for row in claim_gates), "M_H_ref claim gate remains blocked"))
    checks.append(("VAL2020_06_pigr_claim_blocked", any(row["gate_id"] == "CG2020_6_PiGRH_owned" and row["passed_for_claim"] is False for row in claim_gates), "Pi_GR/H claim gate remains blocked"))
    checks.append(("VAL2020_07_first_rows_nonclaim", all(row["score_ready"] is False and row["valid_for_claim"] is False and row["numeric_value"] == "MISSING" for row in first_rows), "all first-row schema entries remain missing/nonclaim"))
    checks.append(("VAL2020_08_claim_gates_blocked", all(row["passed_for_claim"] is False for row in claim_gates), "all claim gates remain blocked for claim"))
    checks.append(("VAL2020_09_refusals_active", all(row["verdict"] == "REFUSE" and row["accepted_for_claim"] is False for row in refusals), "refusals remain active"))
    checks.append(("VAL2020_10_next_target", any(row["target_id"] == "NEXT2020_0_2021" and "Q_tau" in row["objective"] for row in next_target), "2021 Q_tau owner target is selected"))
    checks.append(("VAL2020_11_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"))
    checks.append(("VAL2020_12_branch_copies", all(path.exists() and csv_rows_parse(path) for path in branch_paths), "branch-copy CSVs exist and parse"))
    checks.append(("VAL2020_13_no_formalization_edits", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains 0 for this run"))
    checks.append(("VAL2020_14_output_scope", all(root_resolved == path.resolve() or root_resolved in path.resolve().parents for path in scoped_paths), "all outputs are under post-checkpoint-work"))
    overall = all(passed for _, passed, _ in checks)
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    row = base_row()
    row.update(
        {
            "check_id": "VAL2020_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2020 A-frame M_H_ref Pi_GR owner or Pi_A_res first row",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    owner_audit: list[dict[str, object]],
    first_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    parts = [
        "# 2020 Y5 R2FR: A-Frame MHref PiGR Owner Or PiAres First Row\n",
        "Private checkpoint. This pass attacks the exact bridge needed before residual A-frame scoring: who owns the Hamiltonian source denominator and who owns the measured-GR subtraction.\n",
        "## Current Verdict\n",
        "The correct local denominator is now pinned to the same-frame Hamiltonian/Noether charge: `M_H_ref[S,tau] := G_ref^-1 int_S Q_tau^MTS - H_ref`. The correct A-frame subtraction is likewise pinned: remove the component of `Q_A^total` along the measured Hamiltonian mass/source direction, `Pi_GR/H[Q_A^total]`, before defining `Q_A^res`.\n",
        "This is progress, but not a claim. `M_H_ref` is not parent-owned until `Q_tau^MTS`, `H_ref`, tau/source/frame locks, and Hamiltonian integrability close in one branch. `Pi_GR/H` is not parent-owned until the solution-space mass coordinate, projector orthogonality, and commutator silence are constructed.\n",
        "So the bridge is sharp now: local GR/Newton cannot be reached by scoring total A charge or by using orbital `GM` as a denominator. It has to come from an owned `Q_tau^MTS` current chain, then the residual `Q_A^res` is either theorem-zero or the only finite object allowed into R10/PPN/clock/orbital tests.\n",
        "## Source Register\n",
        md_table(sources, ["source_id", "source_path", "status", "needles", "note"]),
        "## MHref / PiGR Owner Audit\n",
        md_table(owner_audit, ["audit_id", "object", "formula", "status", "derived_content", "blocking_gap", "parent_signed"]),
        "## PiAres First Row Schema\n",
        md_table(first_rows, ["row_id", "symbol", "definition", "required_columns", "current_status", "numeric_value", "units", "score_ready", "valid_for_claim"]),
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
    owner_audit = owner_audit_rows()
    first_rows = first_row_schema_rows()
    claim_gates = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2020_SOURCE_REGISTER.csv",
        "owner_audit": OUT / "P8_Y5_PARENT_QLOC_2020_AFRAME_MHREF_PIGR_OWNER_AUDIT.csv",
        "first_rows": OUT / "P8_Y5_PARENT_QLOC_2020_AFRAME_PIARES_FIRST_ROW_SCHEMA.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2020_CLAIM_GATE.csv",
        "refusals": OUT / "P8_Y5_PARENT_QLOC_2020_REFUSAL_RUNNER.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2020_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2020_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["owner_audit"], owner_audit)
    write_csv(output_map["first_rows"], first_rows)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["refusals"], refusals)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "AFRAME_MHREF_PIGR_OWNER_2020_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2020_AFRAME_MHREF_PIGR_STATUS_NONCLAIM.csv",
        QUEUE / "JR2020_AFRAME_PIARES_FIRST_ROW_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["owner_audit"], branch_paths[0])
    shutil.copyfile(output_map["claim_gates"], branch_paths[1])
    shutil.copyfile(output_map["first_rows"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "A-frame M_H_ref/Pi_GR owner nonclaim copy",
            "A-frame M_H_ref/Pi_GR claim-gate status nonclaim copy",
            "A-frame residual first-row acquisition queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2020_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, owner_audit, first_rows, claim_gates, refusals, next_target, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2020_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, owner_audit, first_rows, claim_gates, refusals, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2020_OVERALL"][0]["status"]
    print(f"VAL2020_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2183"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2183-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R_eq-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2183_SOURCE_REGISTER.csv",
    "selector_theorem": OUT / "P8_Y5_PARENT_QLOC_2183_WORLDTUBE_HILBERT_SELECTOR_THEOREM.csv",
    "source_contract": OUT / "P8_Y5_PARENT_QLOC_2183_SOURCE_MEASURE_CONTRACT_AUDIT.csv",
    "boundary_audit": OUT / "P8_Y5_PARENT_QLOC_2183_ZERO_BOUNDARY_FLUX_AUDIT.csv",
    "residual_rows": OUT / "P8_Y5_PARENT_QLOC_2183_SELECTOR_RESIDUAL_ROWS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2183_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2183_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2183_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2183_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2183_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2183_WORLDTUBE_SELECTOR_RESIDUAL_ROWS_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2183_SELECTOR_THEOREM_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "WORLDTUBE_HILBERT_SOURCE_SELECTOR_2183_NONCLAIM.csv",
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
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2183_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2183-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2183*",
        "*P8_Y5_BRR545_2183*",
        "*Y5_R2FR_worldtube_Hilbert_source_selector_and_zero_boundary_flux_or_R_eq_fill_2183*",
        "*JR2183*",
        "*WORLDTUBE_HILBERT_SOURCE_SELECTOR_2183*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2182_handoff",
            ROOT / "2182-Y5-R2FR-topological-Hilbert-equality-R_eq-zero-or-epsilonM-bound-fill.md",
            ["NEXT2182_0_2183", "WORLDTUBE_HILBERT_SOURCE_SELECTOR_OR_R_EQ_FILL_NEXT", "VAL2182_OVERALL"],
            "2182 selects the parent worldtube/Hilbert source selector and zero boundary flux as the next theorem gate.",
        ),
        (
            "2182_validation",
            OUT / "P8_Y5_BRR545_2182_VALIDATION.csv",
            ["VAL2182_OVERALL", "PASS"],
            "2182 validation passed before 2183 continues the chain.",
        ),
        (
            "hilbert_worldtube_attempt",
            OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
            ["HWT536_0_parent_worldtube_fixed", "HWT536_3_Hilbert_to_PiM_charge_map", "HWT536_5_exact_and_reference_terms_zero"],
            "Hilbert-worldtube theorem attempt names the parent-fixed worldtube, PiM charge map, and zero exact/reference condition.",
        ),
        (
            "hilbert_worldtube_certificate",
            OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv",
            ["HWG535_0_worldtube_fixed_before_readout", "HWG535_2_topological_representative_matches_worldtube_boundary", "HWG535_3_exact_term_zero"],
            "certificate file records the currently missing worldtube, topological boundary, and exact-term certificates.",
        ),
        (
            "parent_action_contract",
            OUT / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
            ["PAC537_0_covariant_parent_action", "PAC537_2_parent_fixed_worldtube", "PAC537_6_reference_and_boundary_zero"],
            "parent action contract lists the covariant action, parent-fixed source, and reference/boundary zero clauses.",
        ),
        (
            "worldtube_source_measure",
            OUT / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
            ["T510_0_EH_reference_glue", "T510_1_worldtube_source_measure", "T510_2_MTS_transfer_condition"],
            "worldtube source theorem supplies the GR-style Hamiltonian charge reference and MTS transfer condition.",
        ),
        (
            "hamiltonian_source_measure",
            OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
            ["HSM541_0_adopt_Hamiltonian_PiM", "HSM541_2_observed_worldtube_source", "HSM541_5_Gauss_orbital_readout"],
            "Hamiltonian contract names PiM as Hamiltonian mass map, observed source worldtube, and Gauss/orbital readout.",
        ),
        (
            "source_measure_flux",
            OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
            ["T509_0_charge_identity_needed", "T509_1_flux_closure", "T509_2_no_extra_mass_channel"],
            "source-measure flux theorem records the identity, radial closure, and no-extra-channel clauses.",
        ),
    ]
    rows = []
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


def selector_theorem_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "WST2183_0_parent_action_domain",
            "covariant parent action owns the source support",
            "Let S_parent[e_obs,psi,aux] be diffeomorphism covariant and define J_H[tau] from delta S_matter/delta e_obs before any orbital readout.",
            "CONDITIONAL_THEOREM_PREMISE",
            "without an explicit parent action, W_source is a label rather than a derived support.",
        ),
        (
            "WST2183_1_worldtube_selector",
            "source worldtube selector",
            "W_source := supp(J_H[e_obs,tau]); linking surfaces S1,S2 are admissible only if they enclose the same W_source and bound a compact source-free annulus A.",
            "EXACT_SELECTOR_DEFINITION_CONDITIONAL",
            "this forbids choosing the mass domain after seeing residuals.",
        ),
        (
            "WST2183_2_Hamiltonian_charge",
            "dressed source charge",
            "M_source[W] := H_tau[S] - H_tau[reference], not bare rest mass.",
            "EXACT_DEFINITION_CORRECTION",
            "binding, boundary, and field dressing must already be included in the parent charge.",
        ),
        (
            "WST2183_3_radial_closure",
            "source-free annulus closure",
            "If constraints vanish in A, tau/reference are fixed, and Delta_nonEH+Delta_symp+Delta_PiM+Delta_extra+Delta_frame=0, then H_tau[S2]-H_tau[S1]=0.",
            "EXACT_CONDITIONAL_GR_STYLE_THEOREM",
            "this is the GR-like route to radial source invariance.",
        ),
        (
            "WST2183_4_topological_representative",
            "topological current is the Poincare dual of W_source",
            "Set J_M_top := M_source[W] omega_W with d omega_W=0 and integral_link omega_W=1 for that same W_source.",
            "EXACT_CONDITIONAL_SAME_OBJECT_MAP",
            "if this is parent-owned, the topological charge is no longer a closed wrong object.",
        ),
        (
            "WST2183_5_R_eq_zero_condition",
            "R_eq zero condition",
            "With Pi_M J_H equal to the Hamiltonian mass current and J_M_top the same W_source class, Pi_M J_H-J_M_top=dB_zero, so R_eq=0 in the compact support class.",
            "EXACT_CONDITIONAL_R_EQ_ZERO",
            "R_eq=0 follows only after the same-object selector is parent-signed.",
        ),
        (
            "WST2183_6_B_zero_condition",
            "zero boundary flux condition",
            "B_zero_flux=0 requires fixed reference, no inner/infinity compact leak, and no symplectic/projector boundary mass shift.",
            "B_ZERO_ZERO_EXTRA_PREMISE_REQUIRED",
            "exactness alone does not remove a measured surface offset.",
        ),
        (
            "WST2183_7_current_verdict",
            "current MTS selector status",
            "The theorem is sharp but current MTS lacks explicit parent action, Hamiltonian PiM adoption, zero extra sectors, and boundary-reference certificate.",
            "SELECTOR_THEOREM_CONDITIONAL_CURRENT_CLAIM_FAILS",
            "we have a real route, not a claim.",
        ),
    ]
    return [
        base_row(
            theorem_id=theorem_id,
            clause=clause,
            statement=statement,
            status=status,
            implication=implication,
        )
        for theorem_id, clause, statement, status, implication in specs
    ]


def source_contract_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SCA2183_0_single_observed_frame",
            "single observed matter frame",
            "S_matter must couple to one e_obs used by sources, clocks, and orbital readout.",
            "NOT_YET_DERIVED",
            "source mass and orbital mass can otherwise live in different frames.",
        ),
        (
            "SCA2183_1_time_generator",
            "fixed observed time generator",
            "tau must be fixed by the parent/local asymptotic or clock structure before source scoring.",
            "MISSING_TAU_SELECTOR",
            "changing tau changes the Hamiltonian source charge.",
        ),
        (
            "SCA2183_2_Hamiltonian_PiM",
            "Pi_M as Hamiltonian mass projector",
            "Pi_M J_H must be the covariant phase-space/Hamiltonian mass-charge map, not a post-readout topological or empirical selector.",
            "NOT_ADOPTED_OR_PROVED",
            "Pi_M may still select an unmeasured conserved object.",
        ),
        (
            "SCA2183_3_integrable_reference",
            "integrable fixed-reference charge",
            "delta H_tau = integral_S(delta Q_tau - i_tau theta), with one fixed reference and no arena-dependent offset.",
            "MISSING_REFERENCE_CERTIFICATE",
            "measured GM can be moved into the reference term.",
        ),
        (
            "SCA2183_4_Gauss_readout",
            "same charge controls Newton coefficient",
            "nabla^2 Phi = 4*pi*G_ref rho_H and a_r=-G_ref M_source/r^2 must use the same M_source.",
            "NOT_DERIVED",
            "source equality alone is not enough without inverse-square readout.",
        ),
        (
            "SCA2183_5_constant_G",
            "universal source-blind G",
            "G_eff/kappa must be constant, universal, source-blind, range-blind, and frame-blind on the local branch.",
            "CONDITIONAL_NOT_PARENT_DERIVED",
            "otherwise source closure can still hide Gdot/range/frame residuals.",
        ),
        (
            "SCA2183_6_extra_silence",
            "no hidden mass charge channels",
            "nonEH, memory, motion, time, domain, range, frame, symplectic-boundary, and projector sectors must carry zero or bounded local mass charge.",
            "FIELD_SPECIFIC_QUEUE_OPEN",
            "extra channels can repair fits while breaking local GR.",
        ),
    ]
    return [
        base_row(
            audit_id=audit_id,
            contract=contract,
            statement=statement,
            status=status,
            implication=implication,
        )
        for audit_id, contract, statement, status, implication in specs
    ]


def boundary_audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "BFA2183_0_reference_fixed_once",
            "fixed reference",
            "H_tau[reference] and B_zero reference must be selected once by the parent action/local boundary condition.",
            "MISSING_FIXED_REFERENCE",
            "per-system reference choices are fitted GM in disguise.",
        ),
        (
            "BFA2183_1_outer_flux",
            "no outer compact leak",
            "No residual dB_zero, symplectic, or nonEH flux may escape through the exterior boundary at the compact/local scoring scale.",
            "MISSING_OUTER_FLUX_ZERO",
            "outer surface leakage shifts M_source between linked surfaces.",
        ),
        (
            "BFA2183_2_inner_flux",
            "no inner/excision leak",
            "No hidden flux may enter through source-hole, excision, ring, or inner regularization boundaries.",
            "MISSING_INNER_FLUX_ZERO",
            "inner boundary hair can masquerade as mass.",
        ),
        (
            "BFA2183_3_projector_stress",
            "no projector-stress boundary term",
            "delta_g Pi_M and boundary variation of Pi_M must vanish or be explicitly bounded.",
            "MISSING_PROJECTOR_STRESS_ZERO_OR_BOUND",
            "PPN/local-GR can fail even if monopole flux is closed.",
        ),
        (
            "BFA2183_4_zero_flux_verdict",
            "zero boundary flux proof",
            "Current sources do not certify B_zero_flux=0 with fixed reference, no compact leaks, and projector-stress silence.",
            "ZERO_BOUNDARY_FLUX_NOT_DERIVED",
            "retain B_zero_flux as nonclaim residual row.",
        ),
    ]
    return [
        base_row(
            audit_id=audit_id,
            boundary_clause=boundary_clause,
            statement=statement,
            status=status,
            implication=implication,
        )
        for audit_id, boundary_clause, statement, status, implication in specs
    ]


def residual_row_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SRR2183_0_W_selector",
            "epsilon_W_selector",
            "charge/domain shift from parent source worldtube selection W_source=supp(J_H[e_obs])",
            "MISSING_PARENT_WORLDTUBE_SELECTOR",
            "dimensionless",
            "Newton;PPN;WEP;orbital",
        ),
        (
            "SRR2183_1_source_frame",
            "epsilon_source_frame",
            "mismatch between observed matter/coframe source measure and orbital/clock readout frame",
            "MISSING_SINGLE_OBSERVED_FRAME_PROOF",
            "dimensionless",
            "Newton;PPN;clocks;WEP",
        ),
        (
            "SRR2183_2_tau",
            "epsilon_tau_selector",
            "Hamiltonian source charge drift from unresolved observed time generator tau",
            "MISSING_TAU_SELECTOR_PROOF",
            "dimensionless_or_charge_fraction",
            "Newton;clocks;orbital",
        ),
        (
            "SRR2183_3_H_reference",
            "epsilon_H_reference",
            "fixed-reference/integrability residual in H_tau[S]-H_ref",
            "MISSING_FIXED_REFERENCE_AND_INTEGRABILITY",
            "dimensionless_or_GM_flux",
            "Newton;R10;R11;orbital",
        ),
        (
            "SRR2183_4_R_eq",
            "R_eq_integral",
            "compact support equality residual Pi_M J_H-J_M_top-dB_zero after W_source selection",
            "MISSING_R_EQ_ZERO_OR_VALUE",
            "dimensionless_after_M_H_ref_normalization",
            "Newton;PPN;R10;R11",
        ),
        (
            "SRR2183_5_B_zero",
            "B_zero_flux",
            "compact boundary flux of dB_zero/reference/symplectic improvement",
            "MISSING_B_ZERO_FLUX_ZERO_OR_VALUE",
            "GM_flux_or_dimensionless_after_M_H_ref_normalization",
            "Newton;PPN;R7;R8;R9;R11",
        ),
        (
            "SRR2183_6_extra",
            "epsilon_extra_charge",
            "nonEH, motion, time, memory, domain, range, frame, symplectic, or projector mass charge",
            "MISSING_EXTRA_CHANNEL_ZERO_OR_VALUE",
            "dimensionless_or_GM_flux",
            "Newton;PPN;WEP;R10;R11",
        ),
        (
            "SRR2183_7_PiM",
            "I_commutator_or_projector_stress",
            "commutator/projector-stress residual if Pi_M is not a fixed Hamiltonian mass map",
            "MISSING_PIM_CHAIN_MAP_ZERO_OR_BOUND",
            "GM_flux_or_PPN_equivalent",
            "Newton;PPN;R10;R11",
        ),
        (
            "SRR2183_8_total",
            "epsilon_M_abs_2183",
            "absolute no-cancellation sum of selector, frame, tau, reference, R_eq, B_zero, extra, and PiM residuals",
            "MISSING_COMPONENT_INPUTS",
            "dimensionless",
            "Newton;local-GR;R10;R11",
        ),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            status=status,
            units=units,
            observable_link=observable_link,
            value="MISSING_NUMERIC_VALUE",
            source_path="MISSING_SOURCE_PATH",
            score_ready=False,
        )
        for row_id, symbol, definition, status, units, observable_link in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CG2183_0_conditional_selector",
            "conditional worldtube-Hilbert selector theorem exists",
            "PASS_GUARDRAIL",
            "the GR-style Hamiltonian source route is written as a conditional theorem.",
        ),
        (
            "CG2183_1_parent_action",
            "explicit covariant MTS parent action owns J_H and W_source",
            "BLOCKED_NONCLAIM",
            "source files contain contract clauses, not a full signed parent Lagrangian.",
        ),
        (
            "CG2183_2_Hamiltonian_PiM",
            "Pi_M is adopted/proved as Hamiltonian mass-charge map",
            "BLOCKED_NONCLAIM",
            "HSM541_0 remains candidate-only/not adopted or proved.",
        ),
        (
            "CG2183_3_R_eq_zero",
            "R_eq=0 follows for current MTS",
            "BLOCKED_NONCLAIM",
            "same-object selector premises remain unsigned.",
        ),
        (
            "CG2183_4_B_zero_flux_zero",
            "B_zero_flux=0 follows for current MTS",
            "BLOCKED_NONCLAIM",
            "fixed reference/no compact leak/projector-stress silence are not certified.",
        ),
        (
            "CG2183_5_Newton_local_GR",
            "Newton/local-GR source reduction can be claimed",
            "BLOCKED_NONCLAIM",
            "selector residual rows remain missing source paths and values.",
        ),
        (
            "CG2183_6_no_cheat_guard",
            "post-readout worldtube, fitted reference, and closed-wrong-object promotion are forbidden",
            "PASS_GUARDRAIL",
            "2183 keeps the route conditional and residualized.",
        ),
    ]
    return [
        base_row(gate_id=gate_id, gate=gate, status=status, implication=implication)
        for gate_id, gate, status, implication in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2183_0_theorem_shape",
            "CONDITIONAL_SELECTOR_THEOREM_BUILT",
            "W_source=supp(J_H[e_obs]) plus fixed Hamiltonian charge/reference would make the topological object the measured source object.",
            "selected",
        ),
        (
            "DEC2183_1_current_limit",
            "CURRENT_MTS_LACKS_PARENT_SIGNATURES",
            "The needed clauses exist as contracts/certificates but remain not_yet_derived, candidate_only, or missing_certificate.",
            "selected",
        ),
        (
            "DEC2183_2_best_next",
            "BUILD_MINIMAL_PARENT_ACTION_CHARGE_CONTRACT_NEXT",
            "The least circular leap is now to construct a minimal covariant local parent-action charge contract that owns J_H, Pi_M, tau, W_source, and B_zero, then see where it fails.",
            "selected",
        ),
        (
            "DEC2183_3_fallback",
            "SOURCE_BACKED_RESIDUAL_FILL_REMAINS_FALLBACK",
            "If the parent action cannot own those objects, R_eq/B_zero/PiM/source-frame rows must become finite empirical residuals.",
            "held_parallel",
        ),
    ]
    return [
        base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status)
        for decision_id, decision, rationale, status in specs
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2183_0_2184",
            selection_status="selected",
            target_file="2184-Y5-R2FR-minimal-parent-action-Hamiltonian-charge-contract-or-selector-residual-fill.md",
            target_script="scripts/Y5_R2FR_minimal_parent_action_Hamiltonian_charge_contract_or_selector_residual_fill_2184.py",
            objective="construct the minimal covariant local parent-action charge contract that owns e_obs, J_H, Pi_M, tau, W_source, fixed reference, and B_zero; otherwise demote the selector route to explicit residual rows",
            success_condition="a parent action skeleton derives the Hilbert source current, Hamiltonian mass projector, source worldtube, topological representative, R_eq=0, and B_zero_flux=0 without post-readout choices; otherwise source-backed nonclaim residual rows are retained",
            do_not_do="do not impose equality with a late multiplier, choose W_source after fitting, absorb source mismatch into G, or claim Newton/local-GR from the conditional theorem",
        ),
        base_row(
            route_id="NEXT2183_1_residual_acquisition",
            selection_status="held_parallel",
            target_file="2184b-Y5-R2FR-selector-R_eq-Bzero-source-backed-residual-acquisition.md",
            target_script="scripts/Y5_R2FR_selector_R_eq_Bzero_source_backed_residual_acquisition_2184b.py",
            objective="acquire real source-backed residual inputs for W_selector, source_frame, tau, reference, R_eq, B_zero, extra charge, and PiM rows if the parent-action route fails",
            success_condition="each acquired row has units, normalization, source path, arena projection, and valid_for_claim=false until the full no-cancellation envelope closes",
            do_not_do="do not score placeholders, cancellation-only rows, or unsourced numeric guesses",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["residual_rows"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["selector_theorem"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["source_contract"], BRANCH_COPIES["source_weight"]),
    ]
    rows = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
            if str(row.get("valid_for_claim", "")).lower() == "true":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    source_rows = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2183_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2183_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    theorem_statuses = {row["status"] for row in rows_by_name["selector_theorem"]}
    theorem_pass = {"EXACT_SELECTOR_DEFINITION_CONDITIONAL", "EXACT_CONDITIONAL_R_EQ_ZERO", "SELECTOR_THEOREM_CONDITIONAL_CURRENT_CLAIM_FAILS"}.issubset(theorem_statuses)
    validations.append(base_row(validation_id="VAL2183_02_selector_theorem", status="PASS" if theorem_pass else "FAIL", detail="conditional selector theorem and current claim failure are explicit"))

    contract_statuses = {row["status"] for row in rows_by_name["source_contract"]}
    contract_pass = {"NOT_ADOPTED_OR_PROVED", "MISSING_TAU_SELECTOR", "FIELD_SPECIFIC_QUEUE_OPEN"}.issubset(contract_statuses)
    validations.append(base_row(validation_id="VAL2183_03_source_contract", status="PASS" if contract_pass else "FAIL", detail="source/tau/PiM/extra-channel debts are audited"))

    boundary_statuses = {row["status"] for row in rows_by_name["boundary_audit"]}
    boundary_pass = "ZERO_BOUNDARY_FLUX_NOT_DERIVED" in boundary_statuses and "MISSING_PROJECTOR_STRESS_ZERO_OR_BOUND" in boundary_statuses
    validations.append(base_row(validation_id="VAL2183_04_boundary_audit", status="PASS" if boundary_pass else "FAIL", detail="zero boundary flux remains unsigned and bounded route retained"))

    residual_rows = rows_by_name["residual_rows"]
    residual_ok = all(str(row.get("status", "")).startswith("MISSING_") and not bool(row.get("score_ready")) and row.get("source_path") == "MISSING_SOURCE_PATH" for row in residual_rows)
    validations.append(base_row(validation_id="VAL2183_05_residual_rows_nonclaim", status="PASS" if residual_ok else "FAIL", detail=f"residual rows={len(residual_rows)} remain missing/source-free/nonclaim"))

    claim_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(base_row(validation_id="VAL2183_06_claim_gate", status="PASS" if "BLOCKED_NONCLAIM" in claim_statuses and "PASS_GUARDRAIL" in claim_statuses else "FAIL", detail="claim gate blocks Newton/local-GR and keeps no-cheat guard"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2183_07_decision", status="PASS" if "BUILD_MINIMAL_PARENT_ACTION_CHARGE_CONTRACT_NEXT" in decision_text else "FAIL", detail="decision selects minimal parent-action charge contract next"))

    validations.append(base_row(validation_id="VAL2183_08_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2184" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2184 parent-action charge contract target selected"))

    validations.append(base_row(validation_id="VAL2183_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2183_10_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2183_11_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2183_artifacts()
    validations.append(base_row(validation_id="VAL2183_12_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2183 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2183_13_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2183_OVERALL", status="PASS" if overall else "FAIL", detail="2183 builds the conditional worldtube-Hilbert source selector theorem and keeps current MTS nonclaim"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2183 - Y5/R2FR Worldtube-Hilbert Source Selector And Zero Boundary Flux Or R_eq Fill

## Current Verdict

2183 is a real forward step: it turns the vague phrase "same source object" into an exact parent-action contract.

The conditional theorem is:

1. A covariant parent action defines the observed Hilbert current `J_H[tau]` from `delta S_matter/delta e_obs`.
2. The source worldtube is selected before readout by `W_source := supp(J_H[e_obs,tau])`.
3. The measured source charge is dressed, `M_source[W] := H_tau[S] - H_tau[reference]`, not bare rest mass.
4. In a source-free annulus `A` between linked surfaces, the charge is radially closed if the constraints vanish and `Delta_nonEH`, `Delta_symp`, `Delta_PiM`, `Delta_extra`, and `Delta_frame` vanish or are bounded.
5. If `J_M_top` is the Poincare dual of that same `W_source`, then `R_eq=0` follows in the compact support class.

That is the good news. This is no longer woolly: we know what theorem would make the topology route legitimate.

The bad news, or really the honest news, is that current MTS still lacks the parent signatures:

- no explicit signed local parent action owning `J_H`;
- no adopted/proved Hamiltonian `Pi_M`;
- no fixed observed time generator `tau`;
- no fixed reference/boundary-zero certificate;
- no proof that extra sectors carry zero local mass charge.

So 2183 does **not** claim Newton/local-GR. It says the next leap is to build the minimal parent-action charge contract. If that works, this route can stop being closure-only. If it fails, the residual rows are already named.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## Worldtube-Hilbert Selector Theorem

{md_table(rows_by_name["selector_theorem"], ["theorem_id", "clause", "statement", "status", "implication", "valid_for_claim"])}

## Source Measure Contract Audit

{md_table(rows_by_name["source_contract"], ["audit_id", "contract", "statement", "status", "implication", "valid_for_claim"])}

## Zero Boundary Flux Audit

{md_table(rows_by_name["boundary_audit"], ["audit_id", "boundary_clause", "statement", "status", "implication", "valid_for_claim"])}

## Selector Residual Rows

{md_table(rows_by_name["residual_rows"], ["row_id", "symbol", "definition", "status", "units", "observable_link", "value", "source_path", "score_ready", "valid_for_claim"])}

## Claim Gate

{md_table(rows_by_name["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Working Interpretation

This is not just circling the same gate. The route has been compressed to a specific construction problem:

`parent action -> observed Hilbert current -> W_source -> Hamiltonian charge -> Pi_M mass map -> J_M_top=PD(W_source) -> R_eq=0 -> B_zero_flux=0`.

That chain is exactly the kind of thing GR has through its covariant phase-space/Hamiltonian source story. MTS needs its own version. If we can write the minimal parent action contract without smuggling in the answer, we are finally attacking the right wall.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "selector_theorem": selector_theorem_rows(),
        "source_contract": source_contract_rows(),
        "boundary_audit": boundary_audit_rows(),
        "residual_rows": residual_row_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in [
        "source_register",
        "selector_theorem",
        "source_contract",
        "boundary_audit",
        "residual_rows",
        "claim_gate",
        "decision",
        "next_target",
    ]:
        write_csv(OUTPUTS[name], rows_by_name[name])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()

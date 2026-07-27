from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3553-Y5-R2FR-parent-sector-current-chain-theta-source-pack.md"
CANONICAL_STATUS = OUT / "P8_Y5_parent_sector_current_chain_theta_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3553": {"path": Path(__file__).resolve(), "role": "3553 generator"},
    "doc_3552": {
        "path": ROOT / "3552-Y5-R2FR-Htau-qbasic-charge-extraction-or-DXHtau-bound-pack.md",
        "role": "H_tau q-basic charge extraction handoff",
    },
    "next_3552": {
        "path": OUT / "P8_Y5_R2FR_3552_NEXT_TARGET.csv",
        "role": "3552 selected theta_MTS target",
    },
    "htau_theorem_3552": {
        "path": OUT / "P8_Y5_R2FR_3552_HTAU_QBASIC_THEOREM.csv",
        "role": "H_tau q-basic theorem",
    },
    "charge_chain_3552": {
        "path": OUT / "P8_Y5_R2FR_3552_PARENT_CHARGE_CHAIN_AUDIT.csv",
        "role": "parent charge chain audit",
    },
    "dxhtau_3552": {
        "path": OUT / "P8_Y5_R2FR_3552_DXHTAU_LEAKAGE_BOUND_PACK.csv",
        "role": "D_X H_tau leakage vector",
    },
    "doc_1009": {
        "path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "role": "historical parent sector current-chain contract",
    },
    "sector_contract_1009": {
        "path": OUT / "P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv",
        "role": "parent sector contract",
    },
    "sector_candidates_1009": {
        "path": OUT / "P8_Y5_R10_1009_SECTOR_VARIATION_CANDIDATES.csv",
        "role": "sector first-variation candidates",
    },
    "sector_runner_1009": {
        "path": OUT / "P8_Y5_R10_1009_SECTOR_VARIATION_RUNNER.csv",
        "role": "sector variation runner refusals",
    },
    "theta_gate_2545": {
        "path": OUT / "P8_Y5_NO_SHADOW_2545_THETA_QTAU_GATE_RECHECK.csv",
        "role": "exact boundary-improvement theta/Q_tau gate",
    },
    "min_action_blocks": {
        "path": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "role": "minimum parent local-GR action blocks",
    },
    "first_variation_gates": {
        "path": OUT / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
        "role": "symbol first variation gates",
    },
    "gk_contract": {
        "path": OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
        "role": "Gamma/Khat/q_loc action-existence contract",
    },
    "domain_variation": {
        "path": OUT / "P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv",
        "role": "domain selector variation chain",
    },
    "local_zero_clause": {
        "path": OUT / "P8_PARENT_LOCAL_ZERO_ACTION_CLAUSE.csv",
        "role": "local-zero parent clause",
    },
    "pim_contract": {
        "path": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "role": "Pi_M parent symplectic/projector algebra contract",
    },
    "mass_flux_contract": {
        "path": OUT / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "role": "mass flux/projector Euler calibration contract",
    },
    "worldtube_glue": {
        "path": OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
        "role": "worldtube/source-measure glue clauses",
    },
    "response_doublet": {
        "path": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
        "role": "response doublet action contract",
    },
    "qcoh_contract": {
        "path": OUT / "P8_QCOH_PARENT_ACTION_CONTRACT.csv",
        "role": "coherent load/projector ownership contract",
    },
    "owner_audit_771": {
        "path": OUT / "P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
        "role": "theta/Q_tau owner audit",
    },
    "charge_schema_1008": {
        "path": OUT / "P8_Y5_R10_1008_CHARGE_DECOMPOSITION_SCHEMA.csv",
        "role": "theta/Q_tau decomposition schema",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv_rows(path)
    except (csv.Error, OSError, UnicodeDecodeError):
        return False
    return True


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = [
        "| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "TSP3553_0_sector_first_variation",
            "claim_piece": "sector theta extraction",
            "statement": "For each retained sector i, delta S_i = E_i delta Phi_i + d theta_i defines the sector symplectic potential theta_i.",
            "proof_step": "This is the first-variation identity; it is a theorem only after S_i, field list, boundary class and tau action are supplied.",
            "condition_needed": "action source, fields, variation equation, stress/Euler terms, boundary condition and fixed-before-readout certificate for each sector.",
            "current_status": "EXACT_FORMULA_SECTOR_CERTIFICATES_MISSING",
            "source_path": str(SOURCES["sector_candidates_1009"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TSP3553_1_sum_theta_theorem",
            "claim_piece": "total theta_MTS",
            "statement": "If S_parent=sum_i S_i with compatible field/boundary/tau branches, then theta_MTS=sum_i theta_i plus fixed exact-improvement terms.",
            "proof_step": "Linearity of variation gives delta S_parent=sum_i E_i delta Phi_i + d(sum_i theta_i); exact improvements are harmless only when fixed before readout.",
            "condition_needed": "all retained sectors have parent-signed first variations and improvement ambiguity is fixed.",
            "current_status": "EXACT_CONDITIONAL_THEOREM_UNSIGNED",
            "source_path": str(SOURCES["theta_gate_2545"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TSP3553_2_charge_unblock",
            "claim_piece": "H_tau input",
            "statement": "Once theta_MTS is assembled, delta H_tau can use integral_S(delta Q_tau^MTS - i_tau theta_MTS) without a placeholder theta row.",
            "proof_step": "3552 already isolates theta_MTS as the first missing object in the H_tau theorem.",
            "condition_needed": "Q_tau pieces and integrability still remain separate gates after theta_MTS is assembled.",
            "current_status": "CONDITIONAL_INPUT_ONLY",
            "source_path": str(SOURCES["htau_theorem_3552"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TSP3553_3_no_total_switch",
            "claim_piece": "anti-shortcut",
            "statement": "Declaring S_parent=sum_i S_i by contract does not promote theta_MTS unless every retained sector has a signed theta/stress/boundary/tau certificate.",
            "proof_step": "The total action switch fails if any retained sector hides stress, charge, boundary flux or source coupling.",
            "condition_needed": "sector certificates, no-hidden-stress certificates and fixed-before-readout certificates.",
            "current_status": "GUARD_ACTIVE",
            "source_path": str(SOURCES["sector_runner_1009"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def sector_theta_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector_id": "THS3553_0_EH_core",
            "sector": "EH metric anchor",
            "action_block": "S_EH[g_obs;kappa0,Lambda0]",
            "theta_slot": "theta_EH",
            "theta_status": "REFERENCE_ANCHOR_NOT_TOTAL_PARENT",
            "needed_to_promote": "constant kappa0, fixed Lambda subtraction, same observed metric in matter/clocks and MTS residual reduction certificates",
            "source_path": str(SOURCES["min_action_blocks"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "sector_id": "THS3553_1_kappa_topological",
            "sector": "kappa/topological level",
            "action_block": "S_kappa_top[kappa_eff,A_3]",
            "theta_slot": "theta_kappa_top_or_boundary",
            "theta_status": "CANDIDATE_NOT_ADOPTED",
            "needed_to_promote": "parent adoption, A_3/kappa variation, no source/species/domain labels and boundary level convention",
            "source_path": str(SOURCES["sector_contract_1009"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "sector_id": "THS3553_2_universal_matter",
            "sector": "universal matter/source",
            "action_block": "S_matter[psi,g_obs]",
            "theta_slot": "theta_matter/source",
            "theta_status": "CONDITIONAL_SOURCE_INPUT",
            "needed_to_promote": "same observed coframe, matter descent, source Ward identity and no species-dependent extra coupling",
            "source_path": str(SOURCES["sector_contract_1009"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "sector_id": "THS3553_3_boundary_reference",
            "sector": "boundary/reference",
            "action_block": "S_GHY + fixed exact/topological boundary/reference terms",
            "theta_slot": "theta_boundary + delta B_ref",
            "theta_status": "FIXED_REFERENCE_MISSING",
            "needed_to_promote": "fixed-before-readout reference, improvement ambiguity certificate and zero/fixed boundary flux",
            "source_path": str(SOURCES["theta_gate_2545"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "sector_id": "THS3553_4_Gamma_Khat_extra",
            "sector": "Gamma/Khat/q_loc extra",
            "action_block": "S_GK[g,Phi]",
            "theta_slot": "theta_GK",
            "theta_status": "MISSING_ACTION_EXISTENCE_AND_HELMHOLTZ",
            "needed_to_promote": "construct S_GK or prove no action; if action exists, show Euler closure, double-zero and boundary no-flux",
            "source_path": str(SOURCES["gk_contract"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "sector_id": "THS3553_5_domain_projector_selector",
            "sector": "domain/projector selector",
            "action_block": "S_selector[u,h,X,Qcoh,chi_D]",
            "theta_slot": "theta_selector",
            "theta_status": "PARTIAL_CLAUSE_NOT_PARENT_CLOSED",
            "needed_to_promote": "Euler/topological domain selection, metric-stress accounting, boundary no-flux and local/FLRW branch rule",
            "source_path": str(SOURCES["domain_variation"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "sector_id": "THS3553_6_mass_projector_PiM",
            "sector": "Pi_M/source-measure projector",
            "action_block": "Pi_M/source-measure projector sector",
            "theta_slot": "theta_PiM",
            "theta_status": "NOT_PARENT_DERIVED",
            "needed_to_promote": "parent symplectic projector algebra, product variation, Ward/Euler flux closure and measured-GM calibration",
            "source_path": str(SOURCES["pim_contract"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "sector_id": "THS3553_7_memory_response_doublet",
            "sector": "memory/response doublet",
            "action_block": "response doublet / memory sector",
            "theta_slot": "theta_memory_response",
            "theta_status": "PARTIAL_CANDIDATE_NOT_MATCHED",
            "needed_to_promote": "complete component map, positive operator, zero odd source, PPN lock and boundary no-flux",
            "source_path": str(SOURCES["response_doublet"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "sector_id": "THS3553_8_worldtube_source_glue",
            "sector": "worldtube/source glue",
            "action_block": "source/worldtube matching and mass charge glue",
            "theta_slot": "theta_worldtube/source_glue",
            "theta_status": "CORE_MISSING_PIECE",
            "needed_to_promote": "parent Noether identity, charge form, exterior closure, worldtube matching and Poisson/Newton calibration",
            "source_path": str(SOURCES["worldtube_glue"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "sector_id": "THS3553_9_total_parent_contract",
            "sector": "total parent action",
            "action_block": "S_parent=sum owned retained sectors",
            "theta_slot": "theta_MTS=sum_i theta_i",
            "theta_status": "NOT_PROMOTED",
            "needed_to_promote": "every retained sector has action source, field list, variation equation, theta/Q contribution, stress, boundary, tau action and certificate",
            "source_path": str(SOURCES["sector_contract_1009"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def theta_leak_rows() -> list[dict[str, Any]]:
    return [
        {
            "leak_id": "TL3553_0_total",
            "theta_component": "Delta theta_MTS",
            "formula": "Delta theta_MTS = theta_MTS - sum_i theta_i_owned",
            "non_cancellation_bound": "|i_tau Delta theta_MTS| <= |i_tau Delta theta_EH| + |i_tau Delta theta_boundary| + |i_tau Delta theta_kappa| + |i_tau Delta theta_GK| + |i_tau Delta theta_selector| + |i_tau Delta theta_PiM| + |i_tau Delta theta_matter| + |i_tau Delta theta_memory| + |i_tau Delta theta_worldtube| + |i_tau Delta theta_improvement|",
            "needed_inputs": "owned theta_i or theorem-zero/bound row for every retained sector",
            "current_value": "MISSING_THETA_MTS_SECTOR_VECTOR",
            "units": "Hamiltonian charge variation density after i_tau contraction",
            "feeds": "D_X H_tau; curl(delta H_tau); Q_tau extraction",
            "source_path": str(SOURCES["dxhtau_3552"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "leak_id": "TL3553_1_EH_anchor",
            "theta_component": "Delta theta_EH",
            "formula": "EH theta is available as a reference anchor but not the total MTS theta",
            "non_cancellation_bound": "|i_tau Delta theta_EH| retained unless residual reduction/silence clauses are signed",
            "needed_inputs": "MTS-to-EH reduction guard, hidden-sector silence and same observed metric certificate",
            "current_value": "MISSING_EH_TOTAL_REDUCTION_GUARD",
            "units": "charge variation density",
            "feeds": "EH import guard; local GR comparison",
            "source_path": str(SOURCES["min_action_blocks"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "leak_id": "TL3553_2_boundary_reference",
            "theta_component": "Delta theta_boundary",
            "formula": "boundary/reference/improvement theta not fixed before readout",
            "non_cancellation_bound": "|i_tau Delta theta_boundary| + |i_tau Delta theta_improvement| retained independently",
            "needed_inputs": "fixed reference, exact/corner/topological class, boundary flux condition",
            "current_value": "MISSING_FIXED_BOUNDARY_REFERENCE_THETA",
            "units": "boundary charge variation density",
            "feeds": "H_ref; M_H_ref; H_tau integrability",
            "source_path": str(SOURCES["theta_gate_2545"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "leak_id": "TL3553_3_Gamma_Khat",
            "theta_component": "Delta theta_GK",
            "formula": "Gamma_eff/K_hat/q_loc sector has no Helmholtz-compatible parent action yet",
            "non_cancellation_bound": "|i_tau Delta theta_GK| retained independently",
            "needed_inputs": "S_GK, first variation, theta_GK, stress, Euler closure, double-zero and no-flux",
            "current_value": "MISSING_THETA_GK_ACTION_EXISTENCE",
            "units": "extra-sector charge variation density",
            "feeds": "local GR residual; PPN; source denominator",
            "source_path": str(SOURCES["gk_contract"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "leak_id": "TL3553_4_selector",
            "theta_component": "Delta theta_selector",
            "formula": "domain/projector selector theta from Qcoh/chi_D/local-zero sector",
            "non_cancellation_bound": "|i_tau Delta theta_selector| retained independently",
            "needed_inputs": "selector action variation, metric stress, boundary no-flux, local/FLRW branch rule",
            "current_value": "MISSING_THETA_SELECTOR_STRESS_BOUNDARY",
            "units": "selector charge variation density",
            "feeds": "preferred-frame/domain/local silence residuals",
            "source_path": str(SOURCES["domain_variation"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "leak_id": "TL3553_5_PiM",
            "theta_component": "Delta theta_PiM",
            "formula": "Pi_M/source-measure projector theta and variation terms",
            "non_cancellation_bound": "|i_tau Delta theta_PiM| retained independently",
            "needed_inputs": "parent origin of Pi_M, product variation, projector stress theorem and source calibration",
            "current_value": "MISSING_THETA_PIM_PROJECTOR_ORIGIN",
            "units": "projector charge variation density",
            "feeds": "C_M; source denominator; Newton source charge",
            "source_path": str(SOURCES["pim_contract"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "leak_id": "TL3553_6_matter_source",
            "theta_component": "Delta theta_matter/source",
            "formula": "matter/source current theta and Hilbert-current glue",
            "non_cancellation_bound": "|i_tau Delta theta_matter| + |i_tau Delta theta_worldtube| retained independently",
            "needed_inputs": "universal matter action, Hilbert source current, worldtube measure glue and no species-dependent extra coupling",
            "current_value": "MISSING_THETA_MATTER_WORLDTUBE_GLUE",
            "units": "matter/source charge variation density",
            "feeds": "WEP; Newton source mass; calibrated source coupling",
            "source_path": str(SOURCES["worldtube_glue"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "leak_id": "TL3553_7_memory_response",
            "theta_component": "Delta theta_memory",
            "formula": "memory/response doublet theta",
            "non_cancellation_bound": "|i_tau Delta theta_memory| retained independently",
            "needed_inputs": "full response doublet variation, positive operator, local double-zero and cosmological activation rule",
            "current_value": "MISSING_THETA_MEMORY_RESPONSE_DOUBLET",
            "units": "memory-sector charge variation density",
            "feeds": "local/FLRW branch consistency; cosmological memory",
            "source_path": str(SOURCES["response_doublet"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "TG3553_0_sector_coverage",
            "gate": "all retained sectors represented",
            "required": "EH, kappa/topological, matter, boundary, GK, selector, PiM, memory and worldtube sectors have theta slots",
            "current_status": "COVERED_AS_NONCLAIM_SOURCE_PACK",
            "passes": "False",
            "blocks": "theta_MTS claim",
            "source_path": str(SOURCES["sector_contract_1009"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "TG3553_1_first_variations",
            "gate": "sector first variations",
            "required": "each sector supplies delta S_i=E_i delta Phi_i+d theta_i",
            "current_status": "INCOMPLETE",
            "passes": "False",
            "blocks": "theta_MTS assembly",
            "source_path": str(SOURCES["sector_candidates_1009"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "TG3553_2_no_hidden_stress",
            "gate": "no hidden stress/charge",
            "required": "every non-EH retained stress/charge is zero-owned or explicitly retained",
            "current_status": "UNSIGNED",
            "passes": "False",
            "blocks": "EH import and local-GR claim",
            "source_path": str(SOURCES["first_variation_gates"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "TG3553_3_fixed_improvement",
            "gate": "fixed exact improvements",
            "required": "boundary improvements/reference/counterterms fixed before readout",
            "current_status": "CONTROLLED_ALGEBRA_NOT_GLOBAL_OWNER",
            "passes": "False",
            "blocks": "H_tau/M_H_ref reference stability",
            "source_path": str(SOURCES["theta_gate_2545"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "TG3553_4_same_tau_action",
            "gate": "same tau action",
            "required": "tau acts on all parent and boundary/reference fields before readout",
            "current_status": "PARALLEL_3552_GATE_UNSIGNED",
            "passes": "False",
            "blocks": "Hamiltonian generator ownership",
            "source_path": str(SOURCES["charge_chain_3552"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D3553_0_theta_verdict",
            "question": "Did 3553 assemble live theta_MTS?",
            "decision": "No live claim. It proves the exact sector-sum theorem and creates the current theta source pack, but multiple retained sectors lack first variations.",
            "basis": "1009 supplies sector candidates and refusals; GK, selector, PiM, matter/worldtube, memory and fixed-boundary pieces remain unsigned.",
            "consequence": "theta_MTS is no longer a blank placeholder; it is a sector leakage vector feeding D_X H_tau.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "D3553_1_no_total_action_switch",
            "question": "Can we declare S_parent=sum sectors now?",
            "decision": "No. The sum theorem is exact only after sector certificates exist.",
            "basis": "A total action declaration with missing sector theta/stress/boundary/tau rows would smuggle closure.",
            "consequence": "Keep all H_tau/M_H_ref/Newton/local-GR claims blocked.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "D3553_2_next_target",
            "question": "Which theta sector should be attacked first?",
            "decision": "Gamma/Khat/q_loc extra sector.",
            "basis": "It is the hardest non-EH sector and directly controls local-GR/PPN/source-denominator hair.",
            "consequence": "Move to 3554: S_GK action existence / theta_GK bound.",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS3553_0",
            "checkpoint": "3553 parent sector current-chain theta source pack",
            "claim_allowed": "False",
            "theta_MTS_status": "EXACT_SUM_THEOREM_IF_ALL_SECTOR_VARIATIONS_SIGNED; CURRENTLY_UNSIGNED",
            "sector_pack_status": "all retained theta slots represented as nonclaim source rows",
            "leakage_status": "Delta theta_MTS no-cancellation vector installed",
            "strongest_result": "theta_MTS is reduced to sector first-variation ownership instead of a placeholder",
            "next_target": "3554-Y5-R2FR-Gamma-Khat-sector-action-existence-or-theta-GK-bound.md",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3553_0",
            "target_doc": "3554-Y5-R2FR-Gamma-Khat-sector-action-existence-or-theta-GK-bound.md",
            "target_script": "scripts/Y5_R2FR_3554_Gamma_Khat_sector_action_existence_or_theta_GK_bound.py",
            "objective": "test whether the Gamma_eff/K_hat/q_loc sector admits a parent local action S_GK with Helmholtz integrability, Euler closure, double-zero local residual and boundary no-flux; if not, retain theta_GK/T_GK as explicit nonclaim leakage rows",
            "success_gate": "either theta_GK is parent-owned with a signed first variation, or every GK leakage component has source path, units, arena projection and valid_for_claim=false",
            "reason": "Gamma/Khat is the first hard non-EH theta sector and directly controls local GR, PPN and source-denominator residuals",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    generated_csvs: list[Path],
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    sectors: list[dict[str, Any]],
    leaks: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    all_sources_exist = all(row["exists"] == "True" for row in sources)
    csvs_parse = all(csv_parse_ok(path) for path in generated_csvs)
    sum_theorem_present = any(row["theorem_id"] == "TSP3553_1_sum_theta_theorem" for row in theorem)
    required_sectors = {
        "THS3553_0_EH_core",
        "THS3553_2_universal_matter",
        "THS3553_3_boundary_reference",
        "THS3553_4_Gamma_Khat_extra",
        "THS3553_5_domain_projector_selector",
        "THS3553_6_mass_projector_PiM",
        "THS3553_7_memory_response_doublet",
        "THS3553_8_worldtube_source_glue",
        "THS3553_9_total_parent_contract",
    }
    sectors_covered = required_sectors.issubset({row["sector_id"] for row in sectors})
    all_nonclaim = (
        all(row["valid_for_claim"] == "False" for row in theorem)
        and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in sectors)
        and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in leaks)
        and all(row["valid_for_claim"] == "False" for row in gates)
        and all(row["valid_for_claim"] == "False" for row in decisions)
    )
    leakage_vector_ready = any(row["leak_id"] == "TL3553_0_total" and "+" in row["non_cancellation_bound"] for row in leaks)
    missing_markers_present = all("MISSING_" in row["current_value"] for row in leaks)
    no_formalization_outputs = all(not path.resolve().is_relative_to(FORMALIZATION.resolve()) for path in generated_csvs)

    return [
        {
            "validation_id": "VAL3553_0_sources_exist",
            "passes": bool_text(all_sources_exist),
            "status": "PASS" if all_sources_exist else "FAIL",
            "detail": f"{sum(row['exists'] == 'True' for row in sources)}/{len(sources)} cited source paths exist",
        },
        {
            "validation_id": "VAL3553_1_generated_csvs_parse",
            "passes": bool_text(csvs_parse),
            "status": "PASS" if csvs_parse else "FAIL",
            "detail": f"{len(generated_csvs)} generated CSV files parse with DictReader",
        },
        {
            "validation_id": "VAL3553_2_sum_theta_theorem_present",
            "passes": bool_text(sum_theorem_present),
            "status": "PASS" if sum_theorem_present else "FAIL",
            "detail": "sector-sum theta_MTS theorem is present",
        },
        {
            "validation_id": "VAL3553_3_required_theta_sectors_covered",
            "passes": bool_text(sectors_covered),
            "status": "PASS" if sectors_covered else "FAIL",
            "detail": "EH, matter, boundary, GK, selector, PiM, memory, worldtube and total theta slots are present",
        },
        {
            "validation_id": "VAL3553_4_all_rows_nonclaim",
            "passes": bool_text(all_nonclaim),
            "status": "PASS" if all_nonclaim else "FAIL",
            "detail": "all theorem/sector/leak/gate/decision rows keep claims disabled",
        },
        {
            "validation_id": "VAL3553_5_theta_leakage_non_cancellation",
            "passes": bool_text(leakage_vector_ready and missing_markers_present),
            "status": "PASS" if leakage_vector_ready and missing_markers_present else "FAIL",
            "detail": "Delta theta_MTS rows expose missing sector inputs and use no-cancellation bounds",
        },
        {
            "validation_id": "VAL3553_6_formalization_workbench_untouched",
            "passes": bool_text(no_formalization_outputs),
            "status": "PASS" if no_formalization_outputs else "FAIL",
            "detail": "3553 generated outputs only inside post-checkpoint-work",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3553 - Parent sector current-chain theta source pack",
        "",
        "## Verdict",
        "",
        "- **Exact assembly rule:** if every retained sector has `delta S_i = E_i delta Phi_i + d theta_i`, then `theta_MTS = sum_i theta_i` up to fixed exact-improvement terms.",
        "- **No total-action shortcut:** the sum theorem does not promote `theta_MTS` until every retained sector has action source, field list, stress/Euler accounting, boundary rule, tau action and certificate.",
        "- **Forward movement:** `theta_MTS` is now a sector leakage vector, not a blank missing object.",
        "- **Best next strike:** attack the `Gamma_eff/K_hat/q_loc` sector, because it is the first hard non-EH theta slot and directly controls local-GR/PPN/source hair.",
        "",
        "## Theta Assembly Theorem",
        "",
        markdown_table(
            rows_by_name["theorem"],
            ["theorem_id", "claim_piece", "statement", "current_status"],
        ),
        "",
        "## Sector Theta Pack",
        "",
        markdown_table(
            rows_by_name["sectors"],
            ["sector_id", "sector", "theta_slot", "theta_status", "needed_to_promote"],
        ),
        "",
        "## Theta Leakage Vector",
        "",
        markdown_table(
            rows_by_name["leaks"],
            ["leak_id", "theta_component", "formula", "current_value", "feeds"],
        ),
        "",
        "## Promotion Gates",
        "",
        markdown_table(
            rows_by_name["gates"],
            ["gate_id", "gate", "required", "current_status", "passes"],
        ),
        "",
        "## Decisions",
        "",
        markdown_table(
            rows_by_name["decisions"],
            ["decision_id", "question", "decision", "consequence"],
        ),
        "",
        "## Validation",
        "",
        markdown_table(
            rows_by_name["validation"],
            ["validation_id", "passes", "status", "detail"],
        ),
        "",
        "## Next target",
        "",
        "Move to `3554-Y5-R2FR-Gamma-Khat-sector-action-existence-or-theta-GK-bound.md`: test the `Gamma_eff/K_hat/q_loc` sector for action existence, Helmholtz integrability, Euler closure, double-zero and boundary no-flux.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    theorem = theorem_rows()
    sectors = sector_theta_rows()
    leaks = theta_leak_rows()
    gates = promotion_gate_rows()
    decisions = decision_rows()
    status = status_rows()
    next_target = next_target_rows()

    outputs: dict[Path, tuple[list[dict[str, Any]], list[str]]] = {
        OUT / "P8_Y5_R2FR_3553_SOURCE_REGISTER.csv": (
            sources,
            ["source_id", "path", "exists", "role", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3553_THETA_ASSEMBLY_THEOREM.csv": (
            theorem,
            [
                "theorem_id",
                "claim_piece",
                "statement",
                "proof_step",
                "condition_needed",
                "current_status",
                "source_path",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3553_SECTOR_THETA_SOURCE_PACK.csv": (
            sectors,
            [
                "sector_id",
                "sector",
                "action_block",
                "theta_slot",
                "theta_status",
                "needed_to_promote",
                "source_path",
                "claim_allowed",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3553_THETA_LEAKAGE_VECTOR.csv": (
            leaks,
            [
                "leak_id",
                "theta_component",
                "formula",
                "non_cancellation_bound",
                "needed_inputs",
                "current_value",
                "units",
                "feeds",
                "source_path",
                "claim_allowed",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3553_THETA_PROMOTION_GATES.csv": (
            gates,
            ["gate_id", "gate", "required", "current_status", "passes", "blocks", "source_path", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3553_DECISION_LEDGER.csv": (
            decisions,
            ["decision_id", "question", "decision", "basis", "consequence", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3553_STATUS.csv": (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "theta_MTS_status",
                "sector_pack_status",
                "leakage_status",
                "strongest_result",
                "next_target",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3553_NEXT_TARGET.csv": (
            next_target,
            ["next_id", "target_doc", "target_script", "objective", "success_gate", "reason", "valid_for_claim"],
        ),
        CANONICAL_STATUS: (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "theta_MTS_status",
                "sector_pack_status",
                "leakage_status",
                "strongest_result",
                "next_target",
                "valid_for_claim",
            ],
        ),
    }

    generated_paths: list[Path] = []
    for path, (rows, fields) in outputs.items():
        write_csv(path, rows, fields)
        generated_paths.append(path)

    validation = validation_rows(generated_paths, sources, theorem, sectors, leaks, gates, decisions)
    validation_path = OUT / "P8_Y5_BRR545_3553_VALIDATION.csv"
    write_csv(validation_path, validation, ["validation_id", "passes", "status", "detail"])
    generated_paths.append(validation_path)

    write_doc(
        {
            "theorem": theorem,
            "sectors": sectors,
            "leaks": leaks,
            "gates": gates,
            "decisions": decisions,
            "status": status,
            "next_target": next_target,
            "validation": validation,
        }
    )

    print(f"wrote {DOC}")
    for path in generated_paths:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()

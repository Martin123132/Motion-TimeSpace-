from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def missing(value: object) -> bool:
    text = str(value or "").strip()
    return text == "" or text.upper().startswith("MISSING")


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def path_exists(path_text: str) -> bool:
    text = str(path_text or "").strip()
    if missing(text):
        return False
    if text in {"CANDIDATE_NOT_ADOPTED", "EH_REFERENCE_ONLY", "POST_READOUT", "UNOWNED_SECTOR"}:
        return False
    return source_path(text).exists()


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
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(col, "")) for col in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1009_0_1008_next", "source-intake/mts_residuals/P8_Y5_R10_1008_NEXT_TARGET.csv", "parent action/current-chain contract", "1008 handoff target."),
        ("SRC1009_1_1008_variation", "source-intake/mts_residuals/P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv", "PVA1008_0_parent_action", "parent variation still missing."),
        ("SRC1009_2_1008_piece_ledger", "source-intake/mts_residuals/P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv", "QTA1008_8_Q_total", "Q_tau total not promoted."),
        ("SRC1009_3_1008_claim_gate", "source-intake/mts_residuals/P8_Y5_R10_1008_CLAIM_GATE.csv", "CG1008_0_parent_theta", "theta/Q_tau gates blocked."),
        ("SRC1009_4_min_blocks", "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv", "A511_0_EH_core", "candidate minimum parent local-GR action blocks."),
        ("SRC1009_5_symbol_map", "source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv", "Gamma_eff", "symbol-to-action placement map."),
        ("SRC1009_6_first_variation", "source-intake/mts_residuals/P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv", "FV512_0_metric", "first variation gates."),
        ("SRC1009_7_domain_variation", "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv", "V0_lambda_variation", "domain selector variation chain."),
        ("SRC1009_8_local_zero_clause", "source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_ACTION_CLAUSE.csv", "A1_parent_clause", "local-zero parent clause candidate."),
        ("SRC1009_9_local_zero_variation", "source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_VARIATION_CHAIN.csv", "V5_delta_g_stress", "local-zero metric stress remains debt."),
        ("SRC1009_10_GK_contract", "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv", "GK513_0_action_existence", "Gamma/Khat/q_loc action-existence contract."),
        ("SRC1009_11_PiM_contract", "source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv", "PM0_fixed_exterior_topology", "Pi_M projector algebra contract."),
        ("SRC1009_12_mass_flux", "source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv", "MF0_parent_projector_origin", "mass flux/source normalization contract."),
        ("SRC1009_13_worldtube", "source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv", "W504_1_covariant_parent_Noether_identity", "worldtube/source-measure glue clauses."),
        ("SRC1009_14_response_doublet", "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv", "RD516_0_doublet_variables", "response doublet action route."),
        ("SRC1009_15_Qcoh", "source-intake/mts_residuals/P8_QCOH_PARENT_ACTION_CONTRACT.csv", "C0_parent_variable", "coherent load/projector ownership contract."),
    ]
    rows = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": path_text,
                "exists": str(path.exists()).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "generated_utc": stamp(),
            }
        )
    return rows


def sector_contract_rows() -> list[dict[str, str]]:
    rows = [
        {
            "sector_id": "PCS1009_0_EH_core",
            "action_block": "S_EH[g_obs;kappa0,Lambda0]",
            "parent_fields": "g_obs, coframe, tau",
            "first_variation_target": "theta_EH and Q_tau^EH",
            "current_evidence": "A511_0 gives a clean local spin-2/EH anchor, but only as the baseline piece.",
            "required_to_promote": "constant kappa0, fixed Lambda subtraction, same observed metric in matter/clocks, and MTS residual reduction certificates",
            "status": "baseline_anchor_not_total_parent",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "PCS1009_1_kappa_topological",
            "action_block": "S_kappa_top[kappa_eff,A_3]",
            "parent_fields": "kappa_eff, A_3",
            "first_variation_target": "d kappa_eff = 0 and no local coupling drift",
            "current_evidence": "A511_1 and symbol map give a topological candidate, not an adopted current-chain sector.",
            "required_to_promote": "parent adoption, variation of A_3/kappa_eff, no source/species/domain labels, and boundary level convention",
            "status": "candidate_not_adopted",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "PCS1009_2_universal_matter",
            "action_block": "S_matter[psi,g_obs]",
            "parent_fields": "matter fields psi, g_obs/coframe",
            "first_variation_target": "Hilbert current J_H and universal WEP/source coupling",
            "current_evidence": "A511_2 and MF1 identify the needed source current, but source-current closure/glue is conditional.",
            "required_to_promote": "same observed coframe, matter descent, source Ward identity, and no species-dependent extra coupling",
            "status": "conditional_source_input",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "PCS1009_3_boundary_reference",
            "action_block": "S_GHY + fixed exact/topological boundary/reference terms",
            "parent_fields": "boundary metric, normal, B_ref, counterterm class",
            "first_variation_target": "theta_boundary and Q_tau^boundary without fitted subtraction",
            "current_evidence": "A511_5 and 1008 reject fitted counterterms; no fixed reference theorem is signed.",
            "required_to_promote": "fixed-before-readout reference, improvement ambiguity certificate, and zero/fixed boundary flux",
            "status": "fixed_reference_missing",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "PCS1009_4_Gamma_Khat_extra",
            "action_block": "S_GK[g,Phi] for Gamma_eff/K_hat/q_loc",
            "parent_fields": "Phi^A, Gamma_eff(Phi), K_hat(Phi,g)",
            "first_variation_target": "T_GK, Euler closure, double-zero local residual",
            "current_evidence": "GK513 requires action existence, Helmholtz integrability, Euler closure, double-zero, projector ownership, and boundary no-flux; all are not supplied.",
            "required_to_promote": "construct S_GK or prove no action; if action exists, show T_GK(Phi0)=0 and first variation zero",
            "status": "hard_fail_current_claim",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "PCS1009_5_domain_projector_selector",
            "action_block": "S_selector[u,h,X,Qcoh,chi_D]",
            "parent_fields": "u, h, X, Qcoh, chi_D, lambda_D",
            "first_variation_target": "local selector/projector stress zero or retained",
            "current_evidence": "domain and local-zero chains provide partial formal clauses, but domain selection, metric stress, boundary flux, and R11 silence remain open.",
            "required_to_promote": "Euler/topological domain selection, metric-stress accounting, boundary no-flux, and local/FLRW branch rule",
            "status": "partial_clause_not_parent_closed",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "PCS1009_6_mass_projector_PiM",
            "action_block": "Pi_M/source-measure projector sector",
            "parent_fields": "Pi_M, J_H, exterior homology, boundary symplectic metric",
            "first_variation_target": "d(Pi_M J_H)=0 or exact residual",
            "current_evidence": "PM and MF contracts give algebra and product rule, but parent origin, variation, closure, and absolute calibration are not derived.",
            "required_to_promote": "parent symplectic projector algebra, product variation, Ward/Euler flux closure, and measured-GM calibration",
            "status": "not_parent_derived",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "PCS1009_7_memory_response_doublet",
            "action_block": "response doublet / memory sector",
            "parent_fields": "R_+^A, R_-^A, memory variables",
            "first_variation_target": "local double-zero with cosmological activation allowed",
            "current_evidence": "RD516 is partial and not matched to all physical leakage/source-normalization channels.",
            "required_to_promote": "complete component map, positive operator, zero odd source, PPN lock, and boundary no-flux",
            "status": "partial_candidate_not_matched",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "PCS1009_8_worldtube_source_glue",
            "action_block": "source/worldtube matching and mass charge glue",
            "parent_fields": "worldtube W, exterior annulus A, Q_M[tau], source measure",
            "first_variation_target": "M_source[W] = int_S Q_M[tau] before orbital fitting",
            "current_evidence": "W504 says the route is derivable if parent action is covariant, but mass charge/source measure glue remains not derived.",
            "required_to_promote": "parent Noether identity, charge form, exterior closure, worldtube matching, and Poisson/Newton calibration",
            "status": "core_missing_piece",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "PCS1009_9_total_parent_contract",
            "action_block": "S_parent=sum owned sectors above",
            "parent_fields": "all retained MTS parent fields",
            "first_variation_target": "delta S_parent=E_A delta Phi^A+d theta_MTS; J_tau=dQ_tau^MTS+C_tau",
            "current_evidence": "the corpus has useful sector candidates, not a single signed current-chain action.",
            "required_to_promote": "every retained sector must have action source, field list, variation equation, theta/Q contribution, stress, boundary, tau action, and certificate",
            "status": "not_promoted",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def variation_candidate_rows() -> list[dict[str, str]]:
    base = {
        "target": "sector_first_variation_contract",
        "action_source": "MISSING_ACTION_SOURCE",
        "field_list": "MISSING_FIELD_LIST",
        "variation_equation": "MISSING_VARIATION_EQUATION",
        "theta_contribution": "MISSING_THETA_CONTRIBUTION",
        "Q_tau_contribution": "MISSING_Q_TAU_CONTRIBUTION",
        "stress_contribution": "MISSING_STRESS_CONTRIBUTION",
        "Euler_constraint": "MISSING_EULER_CONSTRAINT",
        "boundary_condition": "MISSING_BOUNDARY_CONDITION",
        "tau_action": "MISSING_TAU_ACTION",
        "source_path": "MISSING_SOURCE_PATH",
        "sector_certificate": "MISSING_SECTOR_CERTIFICATE",
        "no_hidden_stress_certificate": "MISSING_NO_HIDDEN_STRESS_CERTIFICATE",
        "fixed_before_readout_certificate": "MISSING_FIXED_BEFORE_READOUT_CERTIFICATE",
        "valid_for_claim": "false",
    }
    rows: list[dict[str, str]] = []

    def add(candidate_id: str, sector_id: str, candidate: str, **updates: str) -> None:
        row = dict(base)
        row.update({"candidate_id": candidate_id, "sector_id": sector_id, "candidate": candidate, "generated_utc": stamp()})
        row.update(updates)
        rows.append(row)

    add(
        "SVC1009_0_EH_anchor_only",
        "PCS1009_0_EH_core",
        "EH action block is used as full parent action",
        action_source="source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        field_list="g_obs, tau",
        variation_equation="delta S_EH=E_g delta g + d theta_EH",
        theta_contribution="theta_EH",
        Q_tau_contribution="Q_tau^EH",
        source_path="source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    )
    add(
        "SVC1009_1_GK_missing_action",
        "PCS1009_4_Gamma_Khat_extra",
        "Gamma/Khat residual is treated as variational without action existence",
        action_source="source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
        field_list="Phi^A, Gamma_eff, K_hat",
        variation_equation="MISSING_HELMHOLTZ_COMPATIBLE_VARIATION",
        stress_contribution="T_GK symbolic",
        source_path="source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
    )
    add(
        "SVC1009_2_domain_partial_clause",
        "PCS1009_5_domain_projector_selector",
        "domain selector clause is used without metric stress and boundary closure",
        action_source="source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_ACTION_CLAUSE.csv",
        field_list="u,h,X,Qcoh,chi_D,lambda_D",
        variation_equation="source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_VARIATION_CHAIN.csv",
        Euler_constraint="partial local-zero constraints",
        source_path="source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv",
    )
    add(
        "SVC1009_3_PiM_projector_algebra_only",
        "PCS1009_6_mass_projector_PiM",
        "Pi_M algebra is used without parent origin and variation",
        action_source="source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        field_list="Pi_M,J_H,homology,boundary metric",
        variation_equation="delta(Pi_M J_H)=Pi_M delta J_H+(delta Pi_M)J_H",
        stress_contribution="MISSING_PROJECTOR_STRESS_THEOREM",
        source_path="source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv",
    )
    add(
        "SVC1009_4_worldtube_glue_conditional",
        "PCS1009_8_worldtube_source_glue",
        "worldtube/source equality is used before parent charge closure",
        action_source="source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
        field_list="W,A,Q_M,tau",
        variation_equation="delta L=E_A delta phi^A+dTheta",
        Q_tau_contribution="Q_M[tau] conditional",
        source_path="source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
    )
    add(
        "SVC1009_5_response_doublet_partial",
        "PCS1009_7_memory_response_doublet",
        "response doublet is used before full leakage map and PPN lock",
        action_source="source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
        field_list="R_+^A,R_-^A,memory",
        variation_equation="MISSING_FULL_DOUBLET_VARIATION",
        stress_contribution="MISSING_ZERO_ODD_SOURCE_THEOREM",
        source_path="source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
    )
    add(
        "SVC1009_6_total_parent_switch_unsigned",
        "PCS1009_9_total_parent_contract",
        "total parent action is declared by contract without sector certificates",
        action_source="CANDIDATE_NOT_ADOPTED",
        field_list="all retained sectors",
        variation_equation="delta S_parent=sum sector variations",
        theta_contribution="theta_MTS=sum theta_i",
        Q_tau_contribution="Q_tau^MTS=sum Q_i",
        source_path="MISSING_SIGNED_PARENT_ACTION_SOURCE",
    )
    return rows


def evaluate_candidate(row: dict[str, str]) -> dict[str, str]:
    reasons: list[str] = []
    for field in ["action_source", "source_path"]:
        if not path_exists(row.get(field, "")):
            reasons.append(f"MISSING_EXISTING_{field.upper()}")
    for field in [
        "field_list",
        "variation_equation",
        "theta_contribution",
        "Q_tau_contribution",
        "stress_contribution",
        "Euler_constraint",
        "boundary_condition",
        "tau_action",
    ]:
        if missing(row.get(field)):
            reasons.append(f"MISSING_{field.upper()}")
    for field in ["sector_certificate", "no_hidden_stress_certificate", "fixed_before_readout_certificate"]:
        if not str(row.get(field, "")).startswith("PARENT_SIGNED_"):
            reasons.append(f"MISSING_PARENT_SIGNED_{field.upper()}")
    if row["candidate_id"] == "SVC1009_0_EH_anchor_only":
        reasons.append("EH_ANCHOR_REJECTED_AS_TOTAL_PARENT_ACTION")
    if row["candidate_id"] == "SVC1009_6_total_parent_switch_unsigned":
        reasons.append("TOTAL_PARENT_ACTION_SWITCH_REJECTED_WITHOUT_SECTOR_CERTIFICATES")
    if row["sector_id"] == "PCS1009_4_Gamma_Khat_extra":
        reasons.append("GK_ACTION_EXISTENCE_AND_HELMHOLTZ_NOT_PROVED")
    if row["sector_id"] == "PCS1009_6_mass_projector_PiM":
        reasons.append("PIM_PARENT_ORIGIN_AND_VARIATION_NOT_PROVED")
    if row["sector_id"] == "PCS1009_8_worldtube_source_glue":
        reasons.append("WORLDTUBE_SOURCE_GLUE_NOT_PROVED")
    if not flag(row.get("valid_for_claim")):
        reasons.append("VALID_FOR_CLAIM_FALSE")
    verdict = "PASS_SECTOR_VARIATION_CONTRACT" if not reasons else "REFUSED_INCOMPLETE_PARENT_CURRENT_CHAIN_CONTRACT"
    return {
        "runner_id": row["candidate_id"].replace("SVC", "SVR"),
        "candidate_id": row["candidate_id"],
        "sector_id": row["sector_id"],
        "verdict": verdict,
        "score_ready": str(not reasons).lower(),
        "claim_allowed": str(not reasons and flag(row.get("valid_for_claim"))).lower(),
        "valid_for_claim": str(not reasons and flag(row.get("valid_for_claim"))).lower(),
        "failure_reasons": ";".join(reasons),
        "generated_utc": stamp(),
    }


def runner_rows(candidates: list[dict[str, str]]) -> list[dict[str, str]]:
    return [evaluate_candidate(row) for row in candidates]


def claim_gate_rows(sectors: list[dict[str, str]], runner: list[dict[str, str]]) -> list[dict[str, str]]:
    all_refused = all(row["verdict"].startswith("REFUSED") for row in runner)
    total_not_promoted = any(row["sector_id"] == "PCS1009_9_total_parent_contract" and row["status"] == "not_promoted" for row in sectors)
    rows = [
        ("CG1009_0_total_parent_action", "S_parent current-chain action is accepted", "false", "sector action blocks are candidates, not a signed parent action"),
        ("CG1009_1_theta_MTS", "theta_MTS follows from S_parent", "false", "sector theta contributions are incomplete"),
        ("CG1009_2_Qtau_MTS", "Q_tau^MTS follows from S_parent", "false", "sector charges/source constraints are incomplete"),
        ("CG1009_3_GK_q_loc_zero", "Gamma/Khat/q_loc sector is action-owned and double-zero", "false", "GK action existence/Helmholtz/Euler/double-zero clauses are not proved"),
        ("CG1009_4_PiM_source_measure", "Pi_M/source-measure sector is parent-owned", "false", "projector origin, variation, closure, and calibration are not proved"),
        ("CG1009_5_Htau_MHref_local_GR", "H_tau, M_H_ref, and local-GR gates can reopen", "false", "total parent current chain remains incomplete"),
        ("CG1009_6_guardrail", "sector variation contract guardrail is installed", str(all_refused and total_not_promoted).lower(), "shortcuts are refused and total parent action is not promoted"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for gate_id, claim, gate_pass, reason in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC1009_0_contract_not_parent_action",
            "decision": "The minimum parent-action blocks are useful but not yet the parent action.",
            "because": "they lack a single signed field list, first variation, theta/Q split, and stress/boundary accounting across all retained sectors.",
            "next_action": "attack the hardest non-EH sector as an action-existence problem rather than declaring the total action",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1009_1_root_hard_block",
            "decision": "Gamma_eff/K_hat/q_loc is the sharpest next derivation target.",
            "because": "local GR/PPN fails if this sector is bookkeeping rather than a variational stress with Euler closure and double-zero.",
            "next_action": "run a Helmholtz/action-existence obstruction test for S_GK or retain q_loc as explicit residual",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1009_2_source_measure_parallel_debt",
            "decision": "Pi_M/worldtube/source-measure remains a parallel blocker.",
            "because": "even a good local residual zero does not identify the conserved parent charge with measured GM.",
            "next_action": "keep Pi_M/source-measure gates blocked until GK/local residual and mass projector origins are both owned",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "objective": "test whether Gamma_eff/K_hat/q_loc can come from a variational local action with Helmholtz integrability, Euler closure, double-zero, and boundary no-flux; otherwise retain q_loc as explicit residual",
            "include": "candidate S_GK[g,Phi], T_GK, Helmholtz symmetry, Euler equations, T_GK(Phi0)=0, first variation zero, P_loc ownership, boundary/symplectic no-flux, source/equation paths",
            "exclude": "bookkeeping stress, plateau axiom, EH-only import, fitted cancellation, H_tau pass, M_H_ref pass, local-GR claim, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED:
            changed.append(path)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    sectors: list[dict[str, str]],
    candidates: list[dict[str, str]],
    runner: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    validations = [
        ("V1009_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and needles are present"),
        ("V1009_1_sector_contract_complete_shape", len(sectors) >= 10 and any(row["sector_id"] == "PCS1009_9_total_parent_contract" for row in sectors), "sector contract covers EH, non-EH, projector, source, and total parent rows"),
        ("V1009_2_total_contract_not_promoted", any(row["sector_id"] == "PCS1009_9_total_parent_contract" and row["status"] == "not_promoted" and not flag(row["valid_for_claim"]) for row in sectors), "total parent action is explicitly not promoted"),
        ("V1009_3_candidates_nonclaim", len(candidates) >= 7 and all(not flag(row["valid_for_claim"]) for row in candidates), "sector variation candidates remain nonclaim"),
        ("V1009_4_runner_refuses_shortcuts", len(runner) == len(candidates) and all(row["verdict"].startswith("REFUSED") and not flag(row["score_ready"]) for row in runner), "runner refuses every incomplete sector variation shortcut"),
        ("V1009_5_EH_anchor_guard", any(row["candidate_id"] == "SVC1009_0_EH_anchor_only" and "EH_ANCHOR_REJECTED_AS_TOTAL_PARENT_ACTION" in row["failure_reasons"] for row in runner), "EH anchor cannot stand in for total MTS parent action"),
        ("V1009_6_GK_action_guard", any(row["sector_id"] == "PCS1009_4_Gamma_Khat_extra" and "GK_ACTION_EXISTENCE_AND_HELMHOLTZ_NOT_PROVED" in row["failure_reasons"] for row in runner), "Gamma/Khat action existence remains blocked"),
        ("V1009_7_total_switch_guard", any(row["candidate_id"] == "SVC1009_6_total_parent_switch_unsigned" and "TOTAL_PARENT_ACTION_SWITCH_REJECTED_WITHOUT_SECTOR_CERTIFICATES" in row["failure_reasons"] for row in runner), "total parent action declaration is refused without sector certificates"),
        ("V1009_8_claim_gates_blocked", all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in claims), "theta, Q_tau, H_tau, M_H_ref, and local-GR claims stay blocked"),
        ("V1009_9_guardrail_written", any(row["gate_id"] == "CG1009_6_guardrail" and flag(row["gate_pass"]) for row in claims), "sector variation contract guardrail is installed"),
        ("V1009_10_decision_written", any(row["decision_id"] == "DEC1009_1_root_hard_block" for row in decisions), "Gamma/Khat/q_loc hard-block decision is written"),
        ("V1009_11_next_target_written", len(next_target) == 1 and "1010-Y5-R10-Gamma-Khat-action-existence" in next_target[0]["next_target"], "1010 target row is present and nonclaim"),
        ("V1009_12_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()}
        for check_id, passed, detail in validations
    ]
    rows.insert(
        0,
        {
            "check_id": "V1009_SUMMARY",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "1009 parent current-chain action contract validation summary",
            "generated_utc": stamp(),
        },
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    sectors: list[dict[str, str]],
    candidates: list[dict[str, str]],
    runner: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1009 Y5 R10 parent current-chain action contract or sector variation runner",
            "",
            "**Status:** minimum parent-action blocks were organized into a sector contract, but no total parent action is promoted. The route is narrowed to the Gamma/Khat/q_loc action-existence problem next.",
            "",
            "**Claim ceiling:** no parent `theta_MTS`, `Q_tau^MTS`, `H_tau`, `M_H_ref`, `RC994_0`, `FB554_0`, or local-GR claim is allowed from 1009.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Parent sector contract",
            md_table(sectors, ["sector_id", "action_block", "parent_fields", "first_variation_target", "status", "required_to_promote", "valid_for_claim"]),
            "## Sector variation candidates",
            md_table(candidates, ["candidate_id", "sector_id", "candidate", "action_source", "variation_equation", "theta_contribution", "Q_tau_contribution", "valid_for_claim"]),
            "## Sector variation runner",
            md_table(runner, ["runner_id", "candidate_id", "sector_id", "verdict", "score_ready", "claim_allowed", "failure_reasons"]),
            "## Claim gate",
            md_table(claims, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Validation",
            md_table(validations, ["check_id", "result", "detail", "generated_utc"]),
            "## Next target",
            md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    sectors = sector_contract_rows()
    candidates = variation_candidate_rows()
    runner = runner_rows(candidates)
    claims = claim_gate_rows(sectors, runner)
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, sectors, candidates, runner, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1009_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv", sectors)
    write_csv(OUT / "P8_Y5_R10_1009_SECTOR_VARIATION_CANDIDATES.csv", candidates)
    write_csv(OUT / "P8_Y5_R10_1009_SECTOR_VARIATION_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1009_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_1009_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1009_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1009_VALIDATION.csv", validations)
    write_doc(sources, sectors, candidates, runner, claims, decisions, next_target, validations)


if __name__ == "__main__":
    main()

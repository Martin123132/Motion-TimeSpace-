from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3738"
BRANCH_ID = "MTS_R2FR_Y5_BETA_ASSEMBLY_INTERFACE_AND_OPEN_COEFFICIENT_LEDGER_3738"
DOC = ROOT / "3738-Y5-R2FR-beta-assembly-interface-and-open-coefficient-ledger.md"

DOC_3735 = ROOT / "3735-Y5-R2FR-response-matrix-first-pass-Newton-PPN-EM.md"
DOC_3736 = ROOT / "3736-Y5-R2FR-Newton-PPN-response-coefficients-from-weak-field-limit.md"
DOC_3737 = ROOT / "3737-Y5-R2FR-EM-Poynting-response-coefficients-from-Hodge-Maxwell.md"
NORM_3735 = RESIDUALS / "P8_Y5_R2FR_3735_NORM_CONTRACT_ROWS.csv"
BASIS_3735 = RESIDUALS / "P8_Y5_R2FR_3735_BASIS_SUMMARY_ROWS.csv"
B_ENTRIES_3735 = RESIDUALS / "P8_Y5_R2FR_3735_B_MATRIX_ENTRY_ROWS.csv"
GRAM_WEIGHT_3735 = RESIDUALS / "P8_Y5_R2FR_3735_GRAM_WEIGHT_ENTRY_ROWS.csv"
BNP_3736 = RESIDUALS / "P8_Y5_R2FR_3736_BNP_COEFFICIENT_ROWS.csv"
BEM_3737 = RESIDUALS / "P8_Y5_R2FR_3737_BEM_COEFFICIENT_ROWS.csv"
VALIDATION_3735 = RESIDUALS / "P8_Y5_BRR545_3735_VALIDATION.csv"
VALIDATION_3736 = RESIDUALS / "P8_Y5_BRR545_3736_VALIDATION.csv"
VALIDATION_3737 = RESIDUALS / "P8_Y5_BRR545_3737_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3735", DOC_3735, "beta_NP^2=lambda_max", "3735 exact beta response-matrix contract"),
        ("doc_3736", DOC_3736, "B_NP_SHAPES_SHARPENED", "3736 Newton/PPN response coefficients"),
        ("doc_3737", DOC_3737, "B_EM_SHAPES_SHARPENED", "3737 EM/Poynting response coefficients"),
        ("norm_3735", NORM_3735, "beta_EM^2=lambda_max", "source norm formulas"),
        ("basis_3735", BASIS_3735, "Newton_PPN_bridge", "finite domain/observable bases"),
        ("b_entries_3735", B_ENTRIES_3735, "BME3735_B3732_EM_tail", "original B-entry identifiers"),
        ("gram_weight_3735", GRAM_WEIGHT_3735, "WM3735_EM_y_charge", "open Gram and weight rows"),
        ("bnp_3736", BNP_3736, "BNP3736_4_beta_phi", "sharpened B_NP coefficient rows"),
        ("bem_3737", BEM_3737, "BEM3737_6_tail", "sharpened B_EM coefficient rows"),
        ("validation_3735", VALIDATION_3735, "no_formalization_leak", "3735 validation"),
        ("validation_3736", VALIDATION_3736, "no_formalization_leak", "3736 validation"),
        ("validation_3737", VALIDATION_3737, "no_formalization_leak", "3737 validation"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(timestamp),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "role": role,
            "claim_allowed": False,
        })
    return rows


def coefficient_ledger(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_row in parse_csv(BNP_3736):
        rows.append({
            **base(timestamp),
            "coefficient_id": source_row["coefficient_id"],
            "bridge": "Newton_PPN_bridge",
            "matrix": "B_NP",
            "source_checkpoint": "3736",
            "target_b_entry": source_row["target_b_entry"],
            "observable_row": source_row["observable_row"],
            "domain_col": source_row["domain_col"],
            "coefficient_symbol": source_row["coefficient_symbol"],
            "derivation_summary": source_row["weak_field_derivation"],
            "current_status": source_row["current_status"],
            "missing_for_numeric_or_theorem": source_row["missing_for_numeric_or_theorem"],
            "ready_for_beta_numeric": False,
            "source_csv": str(BNP_3736),
            "claim_allowed": False,
        })
    for source_row in parse_csv(BEM_3737):
        rows.append({
            **base(timestamp),
            "coefficient_id": source_row["coefficient_id"],
            "bridge": "EM_Poynting_bridge",
            "matrix": "B_EM",
            "source_checkpoint": "3737",
            "target_b_entry": source_row["target_b_entry"],
            "observable_row": source_row["observable_row"],
            "domain_col": source_row["domain_col"],
            "coefficient_symbol": source_row["coefficient_symbol"],
            "derivation_summary": source_row["hodge_maxwell_derivation"],
            "current_status": source_row["current_status"],
            "missing_for_numeric_or_theorem": source_row["missing_for_numeric_or_theorem"],
            "ready_for_beta_numeric": False,
            "source_csv": str(BEM_3737),
            "claim_allowed": False,
        })
    return rows


def atomic_beta_terms(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("NP001", "Newton_PPN_bridge", "beta_NP", "y_accel", "h_phi", "C_grad", "g_h_phi", "w_y_accel", "BNP3736_0_accel_phi", "single gradient response", "w_y_accel*C_grad^2/g_h_phi"),
        ("NP002", "Newton_PPN_bridge", "beta_NP", "y_accel", "h_bdy", "C_boundary_projection", "g_h_bdy", "w_y_accel", "BNP3736_6_boundary", "boundary also enters acceleration", "w_y_accel*C_boundary_projection^2/g_h_bdy"),
        ("NP003", "Newton_PPN_bridge", "beta_NP", "y_poisson", "h_phi", "C_lap", "g_h_phi", "w_y_poisson", "BNP3736_1_poisson_phi", "Poisson Laplacian response", "w_y_poisson*C_lap^2/g_h_phi"),
        ("NP004", "Newton_PPN_bridge", "beta_NP", "y_poisson", "h_GM", "4*pi*rho_eff_norm", "g_h_GM", "w_y_poisson", "BNP3736_2_poisson_gm", "measured-source normalization response", "w_y_poisson*(4*pi*rho_eff_norm)^2/g_h_GM"),
        ("NP005", "Newton_PPN_bridge", "beta_NP", "y_poisson", "h_bdy", "C_boundary_projection", "g_h_bdy", "w_y_poisson", "BNP3736_6_boundary", "boundary also enters Poisson", "w_y_poisson*C_boundary_projection^2/g_h_bdy"),
        ("NP006", "Newton_PPN_bridge", "beta_NP", "y_gamma", "h_phi", "Phi0_inv", "g_h_phi", "w_y_gamma", "BNP3736_3_gamma_phipsi", "gamma split coefficient on -h_phi/Phi0", "w_y_gamma*Phi0_inv^2/g_h_phi"),
        ("NP007", "Newton_PPN_bridge", "beta_NP", "y_gamma", "h_psi", "Phi0_inv", "g_h_psi", "w_y_gamma", "BNP3736_3_gamma_phipsi", "gamma split coefficient on +h_psi/Phi0", "w_y_gamma*Phi0_inv^2/g_h_psi"),
        ("NP008", "Newton_PPN_bridge", "beta_NP", "y_beta", "h_phi", "C_beta_2PN", "g_h_phi", "w_y_beta", "BNP3736_4_beta_phi", "2PN nonlinear beta response", "w_y_beta*C_beta_2PN^2/g_h_phi"),
        ("NP009", "Newton_PPN_bridge", "beta_NP", "y_pref", "h_pref", "C_preferred_frame", "g_h_pref", "w_y_pref", "BNP3736_5_pref_pref", "preferred-frame/disformal residual", "w_y_pref*C_preferred_frame^2/g_h_pref"),
        ("EM001", "EM_Poynting_bridge", "beta_EM", "y_poynting", "h_chi", "C_poynting_chi", "g_h_chi", "w_y_poynting", "BEM3737_0_poynting_chi", "constitutive Poynting response", "w_y_poynting*C_poynting_chi^2/g_h_chi"),
        ("EM002", "EM_Poynting_bridge", "beta_EM", "y_poynting", "h_Jem", "C_JdotE", "g_h_Jem", "w_y_poynting", "BEM3737_1_poynting_current", "source-current Poynting response", "w_y_poynting*C_JdotE^2/g_h_Jem"),
        ("EM003", "EM_Poynting_bridge", "beta_EM", "y_poynting", "h_EM_tail", "C_EM_tail_projection", "g_h_EM_tail", "w_y_poynting", "BEM3737_6_tail", "tail response into Poynting", "w_y_poynting*C_EM_tail_projection^2/g_h_EM_tail"),
        ("EM004", "EM_Poynting_bridge", "beta_EM", "y_stress", "h_frame", "C_TEM_frame", "g_h_frame", "w_y_stress", "BEM3737_2_stress_frame", "Maxwell stress/frame response", "w_y_stress*C_TEM_frame^2/g_h_frame"),
        ("EM005", "EM_Poynting_bridge", "beta_EM", "y_stress", "h_EM_tail", "C_EM_tail_projection", "g_h_EM_tail", "w_y_stress", "BEM3737_6_tail", "tail response into stress", "w_y_stress*C_EM_tail_projection^2/g_h_EM_tail"),
        ("EM006", "EM_Poynting_bridge", "beta_EM", "y_wave", "h_chi", "C_wave_chi", "g_h_chi", "w_y_wave", "BEM3737_3_wave_chi", "constitutive wave response", "w_y_wave*C_wave_chi^2/g_h_chi"),
        ("EM007", "EM_Poynting_bridge", "beta_EM", "y_wave", "h_EM_tail", "C_EM_tail_projection", "g_h_EM_tail", "w_y_wave", "BEM3737_6_tail", "tail response into wave", "w_y_wave*C_EM_tail_projection^2/g_h_EM_tail"),
        ("EM008", "EM_Poynting_bridge", "beta_EM", "y_pol", "h_chi", "C_birefringence", "g_h_chi", "w_y_pol", "BEM3737_4_pol_chi", "anisotropic/polarization response", "w_y_pol*C_birefringence^2/g_h_chi"),
        ("EM009", "EM_Poynting_bridge", "beta_EM", "y_pol", "h_EM_tail", "C_EM_tail_projection", "g_h_EM_tail", "w_y_pol", "BEM3737_6_tail", "tail response into polarization", "w_y_pol*C_EM_tail_projection^2/g_h_EM_tail"),
        ("EM010", "EM_Poynting_bridge", "beta_EM", "y_charge", "h_alpha", "C_charge_marker", "g_h_alpha", "w_y_charge", "BEM3737_5_charge_marker", "charge/fine-structure marker response", "w_y_charge*C_charge_marker^2/g_h_alpha"),
        ("EM011", "EM_Poynting_bridge", "beta_EM", "y_charge", "h_EM_tail", "C_EM_tail_projection", "g_h_EM_tail", "w_y_charge", "BEM3737_6_tail", "tail response into charge/readout", "w_y_charge*C_EM_tail_projection^2/g_h_EM_tail"),
    ]
    return [
        {
            **base(timestamp),
            "term_id": term_id,
            "bridge": bridge,
            "beta_symbol": beta_symbol,
            "observable_row": observable_row,
            "domain_col": domain_col,
            "coefficient_symbol": coefficient_symbol,
            "gram_symbol": gram_symbol,
            "weight_symbol": weight_symbol,
            "source_coefficient_id": source_coefficient_id,
            "interpretation": interpretation,
            "diagonal_bound_term": diagonal_bound_term,
            "numeric_ready": False,
            "claim_allowed": False,
        }
        for term_id, bridge, beta_symbol, observable_row, domain_col, coefficient_symbol, gram_symbol, weight_symbol, source_coefficient_id, interpretation, diagonal_bound_term in specs
    ]


def beta_formula_rows(timestamp: str) -> list[dict[str, object]]:
    np_bound = (
        "beta_NP_diag^2 <= "
        "w_y_accel*(C_grad^2/g_h_phi + C_boundary_projection^2/g_h_bdy) + "
        "w_y_poisson*(C_lap^2/g_h_phi + (4*pi*rho_eff_norm)^2/g_h_GM + C_boundary_projection^2/g_h_bdy) + "
        "w_y_gamma*Phi0_inv^2*(1/g_h_phi + 1/g_h_psi) + "
        "w_y_beta*C_beta_2PN^2/g_h_phi + "
        "w_y_pref*C_preferred_frame^2/g_h_pref"
    )
    em_bound = (
        "beta_EM_diag^2 <= "
        "w_y_poynting*(C_poynting_chi^2/g_h_chi + C_JdotE^2/g_h_Jem + C_EM_tail_projection^2/g_h_EM_tail) + "
        "w_y_stress*(C_TEM_frame^2/g_h_frame + C_EM_tail_projection^2/g_h_EM_tail) + "
        "w_y_wave*(C_wave_chi^2/g_h_chi + C_EM_tail_projection^2/g_h_EM_tail) + "
        "w_y_pol*(C_birefringence^2/g_h_chi + C_EM_tail_projection^2/g_h_EM_tail) + "
        "w_y_charge*(C_charge_marker^2/g_h_alpha + C_EM_tail_projection^2/g_h_EM_tail)"
    )
    specs = [
        ("FORM3738_0_exact_NP", "Newton_PPN_bridge", "beta_NP", "exact_matrix", "beta_NP^2=lambda_max(G_NP^{-1/2} B_NP^T W_NP B_NP G_NP^{-1/2})", "finite B_NP, positive-definite G_NP, positive-semidefinite W_NP", "EXACT_CONTRACT_FROM_3735"),
        ("FORM3738_1_diag_bound_NP", "Newton_PPN_bridge", "beta_NP", "conservative_diagonal_envelope", np_bound, "diagonal positive G_NP/W_NP entries and coefficient magnitudes; uses Cauchy with no cancellation credit", "SYMBOLIC_BOUND_DERIVED_VALUES_MISSING"),
        ("FORM3738_2_exact_EM", "EM_Poynting_bridge", "beta_EM", "exact_matrix", "beta_EM^2=lambda_max(G_EM^{-1/2} B_EM^T W_EM B_EM G_EM^{-1/2})", "finite B_EM, positive-definite G_EM, positive-semidefinite W_EM", "EXACT_CONTRACT_FROM_3735"),
        ("FORM3738_3_diag_bound_EM", "EM_Poynting_bridge", "beta_EM", "conservative_diagonal_envelope", em_bound, "diagonal positive G_EM/W_EM entries and coefficient magnitudes; tail projected into every EM observable it touches", "SYMBOLIC_BOUND_DERIVED_VALUES_MISSING"),
    ]
    return [
        {
            **base(timestamp),
            "formula_id": formula_id,
            "bridge": bridge,
            "beta_symbol": beta_symbol,
            "formula_type": formula_type,
            "expression": expression,
            "requirements": requirements,
            "status": status,
            "numeric_executable": False,
            "claim_allowed": False,
        }
        for formula_id, bridge, beta_symbol, formula_type, expression, requirements, status in specs
    ]


def open_input_ledger(timestamp: str, coefficients: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for coefficient in coefficients:
        symbol = str(coefficient["coefficient_symbol"])
        priority = "P0" if "2PN" in symbol or "Phi0" in symbol else "P1"
        rows.append({
            **base(timestamp),
            "input_id": f"INPUT3738_COEFF_{coefficient['coefficient_id']}",
            "bridge": coefficient["bridge"],
            "input_type": "response_coefficient",
            "symbol": symbol,
            "current_value": "MISSING_NUMERIC_OR_PARENT_THEOREM",
            "required_property": "finite coefficient magnitude or zero theorem",
            "source_path": coefficient["source_csv"],
            "blocking_status": coefficient["current_status"],
            "priority": priority,
            "next_action": coefficient["missing_for_numeric_or_theorem"],
            "valid_for_numeric_run": False,
            "claim_allowed": False,
        })
    for source_row in parse_csv(GRAM_WEIGHT_3735):
        matrix = source_row["matrix"]
        input_type = "domain_gram" if matrix.startswith("G_") else "observable_weight"
        prefix = "g" if input_type == "domain_gram" else "w"
        symbol = f"{prefix}_{source_row['row_symbol']}"
        rows.append({
            **base(timestamp),
            "input_id": f"INPUT3738_{source_row['entry_id']}",
            "bridge": source_row["bridge"],
            "input_type": input_type,
            "symbol": symbol,
            "current_value": source_row["value"],
            "required_property": source_row["required_property"],
            "source_path": source_row["source_path"],
            "blocking_status": "MISSING_GRAM_WEIGHT_SOURCE_OR_THEOREM",
            "priority": "P0" if source_row["source_path"] == "MISSING_SOURCE_OR_THEOREM_PATH" else "P1",
            "next_action": "derive parent inner product/observable weight or source a finite experimental covariance/readout norm",
            "valid_for_numeric_run": False,
            "claim_allowed": False,
        })
    return rows


def runner_rows(timestamp: str, coefficients: list[dict[str, object]], terms: list[dict[str, object]], open_inputs: list[dict[str, object]]) -> list[dict[str, object]]:
    coefficient_count = len(coefficients)
    numeric_inputs = sum(1 for row in open_inputs if row["valid_for_numeric_run"] == "True" or row["valid_for_numeric_run"] is True)
    missing_inputs = len(open_inputs) - numeric_inputs
    return [{
        **base(timestamp),
        "runner_id": "RUN3738_0_BETA_ASSEMBLY_INTERFACE",
        "bridges": "Newton_PPN_bridge;EM_Poynting_bridge",
        "coefficient_rows": coefficient_count,
        "atomic_bound_terms": len(terms),
        "open_inputs": len(open_inputs),
        "numeric_ready_inputs": numeric_inputs,
        "missing_inputs": missing_inputs,
        "exact_matrix_formula_ready": True,
        "diagonal_bound_formula_ready": True,
        "numeric_executable": False,
        "status": "BETA_INTERFACE_DERIVED_VALUES_MISSING",
        "claim_allowed": False,
    }]


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("THM3738_0_exact_operator_norm", "DERIVED_FROM_3735", "Once B, G, and W are finite and signed, beta is the spectral norm of the weighted response operator.", "This is the exact bridge from local residual rows to a scalar beta score."),
        ("THM3738_1_diagonal_envelope", "DERIVED_CONSERVATIVE_BOUND", "For diagonal positive G/W, Cauchy gives beta^2 <= sum_y w_y sum_j C_yj^2/g_j without using cancellation.", "This gives a safe smoke-run formula before full covariance structure is owned."),
        ("THM3738_2_NP_split", "DERIVED_ASSEMBLY", "The Newton/PPN diagonal envelope splits gamma into h_phi and h_psi and duplicates boundary response into acceleration and Poisson.", "This prevents hiding the gamma denominator or boundary projection in one vague coefficient."),
        ("THM3738_3_EM_tail_split", "DERIVED_ASSEMBLY", "The EM diagonal envelope propagates the retained tail into Poynting, stress, wave, polarization, and charge rows.", "This prevents falsely declaring Maxwell recovery while keeping hidden EM tails."),
        ("THM3738_4_claim_gate", "ANTI_OVERCLAIM", "No beta_NP or beta_EM number is claimable until all coefficients, Gram entries, and weights are numeric/source-owned or theorem-owned.", "The checkpoint builds the machine; it does not claim a local-GR or Maxwell pass."),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "status": status,
            "clause": clause,
            "meaning": meaning,
            "claim_allowed": False,
        }
        for theorem_id, status, clause, meaning in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3738_0_sources", "3735/3736/3737 source rows exist", True, "prior checkpoint files are present"),
        ("CG3738_1_exact_formula", "exact beta matrix formula assembled", True, "lambda_max contracts are carried forward"),
        ("CG3738_2_diagonal_formula", "conservative diagonal beta envelope assembled", True, "Cauchy/no-cancellation envelope is explicit"),
        ("CG3738_3_coefficients_numeric", "all B_NP/B_EM coefficients numeric or theorem-owned", False, "coefficient rows remain missing numeric/source-owned values"),
        ("CG3738_4_gram_positive", "all G_NP/G_EM entries positive-definite", False, "Gram entries remain missing source/theorem ownership"),
        ("CG3738_5_weights_nonnegative", "all W_NP/W_EM entries nonnegative", False, "observable weights/covariances remain missing"),
        ("CG3738_6_numeric_runner", "beta_NP/beta_EM numeric runner executable", False, "open inputs block numeric scoring"),
        ("CG3738_7_claim", "local residual beta claim allowed", False, "must first close coefficient, Gram, and weight ledgers"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, rationale in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3738_0_progress", "BETA_ASSEMBLY_INTERFACE_DERIVED", "The work now has exact and conservative formulas that turn response rows into beta_NP/beta_EM once inputs are supplied."),
        ("DEC3738_1_not_vibes", "MISSING_INPUTS_ARE_EXECUTION_BLOCKERS_NOT_AUDIT_VIBES", "The open ledger is tied to formula terms, so each missing item has a direct role in the future runner."),
        ("DEC3738_2_next", "NEXT_ATTACK_2PN_BETA_AND_GN_NORMALIZATION", "The least-circular leap toward GR/Newton reduction is deriving the parent 2PN beta map and deciding whether G_N is emergent or calibrated."),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "status_id": "STATUS3738_0",
        "status": "BETA_ASSEMBLY_INTERFACE_DERIVED_VALUES_MISSING",
        "summary": "3738 converts the sharpened Newton/PPN and EM response rows into exact beta matrix contracts plus conservative diagonal beta envelopes; numeric claims remain blocked by open coefficients, Gram entries, and weights.",
        "claim_allowed": False,
    }]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "next_id": "NEXT3738_0",
        "target_doc": "3739-Y5-R2FR-parent-2PN-beta-map-and-GN-normalization.md",
        "target_script": "scripts/Y5_R2FR_3739_parent_2PN_beta_map_and_GN_normalization.py",
        "objective": "derive or bound the parent weak-field expansion through 2PN beta and state whether Newton's constant is an emergent coupling, a calibration constant, or a blocked parent input",
        "success_gate": "C_beta_2PN and the measured-G/G_N normalization row become theorem-owned, source-owned, or explicitly demoted to calibrated closure before beta_NP scoring",
        "claim_allowed": False,
    }]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3738 - Beta Assembly Interface and Open Coefficient Ledger",
        "",
        "## Status",
        "- `BETA_ASSEMBLY_INTERFACE_DERIVED_VALUES_MISSING`",
        "- `beta_NP` and `beta_EM` now have both exact matrix contracts and conservative diagonal bound formulas.",
        "- This is a forward step: the response machinery is assembled into a plug-in scoring interface, but numeric claims remain blocked.",
        "",
        "## Exact Matrix Contracts",
    ]
    for row in grouped["formula_rows"]:
        if row["formula_type"] == "exact_matrix":
            lines.append(f"- `{row['formula_id']}` `{row['beta_symbol']}`: {row['expression']} | requirements: {row['requirements']}")
    lines.extend(["", "## Conservative Diagonal Bounds"])
    for row in grouped["formula_rows"]:
        if row["formula_type"] == "conservative_diagonal_envelope":
            lines.append(f"- `{row['formula_id']}` `{row['beta_symbol']}`: {row['expression']}")
    lines.extend(["", "## Atomic Bound Terms"])
    for row in grouped["atomic_terms"]:
        lines.append(f"- `{row['term_id']}` `{row['beta_symbol']}` `{row['observable_row']}` <- `{row['domain_col']}` via `{row['coefficient_symbol']}`: `{row['diagonal_bound_term']}`")
    lines.extend(["", "## Open Input Ledger Summary"])
    coefficient_inputs = [row for row in grouped["open_inputs"] if row["input_type"] == "response_coefficient"]
    gram_inputs = [row for row in grouped["open_inputs"] if row["input_type"] == "domain_gram"]
    weight_inputs = [row for row in grouped["open_inputs"] if row["input_type"] == "observable_weight"]
    lines.append(f"- response coefficients open: {len(coefficient_inputs)}")
    lines.append(f"- domain Gram entries open: {len(gram_inputs)}")
    lines.append(f"- observable weight entries open: {len(weight_inputs)}")
    lines.append("- highest-priority theoretical blockers: `C_beta_2PN`, `Phi0_inv`, `G_N`/measured-G normalization, and the local Gram/weight choices.")
    lines.extend(["", "## Theorem Rows"])
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['clause']} | {row['meaning']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Next Target"])
    next_row = grouped["next_target"][0]
    lines.append(f"- `{next_row['target_doc']}`")
    lines.append(f"- Objective: {next_row['objective']}")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def validation_rows(timestamp: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    coefficients = parse_csv(paths["coefficient_ledger"])
    terms = parse_csv(paths["atomic_terms"])
    formulas = parse_csv(paths["formula_rows"])
    open_inputs = parse_csv(paths["open_inputs"])
    runner = parse_csv(paths["runner"])
    claim_gates = parse_csv(paths["claim_gates"])
    next_target = parse_csv(paths["next_target"])
    validation_paths = [path for key, path in paths.items() if key != "validation"]
    formalization_leaks = []
    if FORMALIZATION.exists():
        formalization_leaks = list(FORMALIZATION.rglob("*3738*"))
    checks = [
        ("sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "all source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "all outputs exist", all(path.exists() for path in validation_paths)),
        ("csv_parse", "all generated CSVs parse", all(len(parse_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("coefficient_rows", "14 coefficient rows carried forward", len(coefficients) == 14),
        ("atomic_terms", "20 atomic beta bound terms assembled", len(terms) == 20),
        ("formula_rows", "exact and diagonal formulas present", len(formulas) == 4 and all(token in read_text(paths["formula_rows"]) for token in ["lambda_max", "Cauchy", "beta_NP_diag", "beta_EM_diag"])),
        ("open_inputs", "coefficient, Gram, and weight inputs present", all(input_type in {row["input_type"] for row in open_inputs} for input_type in ["response_coefficient", "domain_gram", "observable_weight"])),
        ("runner_blocks", "runner blocks numeric beta", runner[0]["numeric_executable"] == "False" and runner[0]["status"] == "BETA_INTERFACE_DERIVED_VALUES_MISSING"),
        ("claim_gates_blocked", "claim gates block promotion", all(row["claim_allowed"] == "False" for row in claim_gates)),
        ("next_target_3739", "next target is 2PN beta/G_N normalization", next_target[0]["target_doc"] == "3739-Y5-R2FR-parent-2PN-beta-map-and-GN-normalization.md"),
        ("doc_core_terms", "doc contains beta and G_N route", all(token in read_text(paths["doc"]) for token in ["beta_NP", "beta_EM", "C_beta_2PN", "G_N", "Conservative Diagonal Bounds"])),
        ("no_formalization_leak", "no 3738 files in formalization-workbench", len(formalization_leaks) == 0),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "",
        }
        for validation_id, description, result in checks
    ]


def main() -> None:
    timestamp = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3738_SOURCE_REGISTER.csv",
        "coefficient_ledger": RESIDUALS / "P8_Y5_R2FR_3738_COMBINED_COEFFICIENT_LEDGER.csv",
        "atomic_terms": RESIDUALS / "P8_Y5_R2FR_3738_ATOMIC_BETA_BOUND_TERMS.csv",
        "formula_rows": RESIDUALS / "P8_Y5_R2FR_3738_BETA_FORMULA_ROWS.csv",
        "open_inputs": RESIDUALS / "P8_Y5_R2FR_3738_OPEN_INPUT_LEDGER.csv",
        "runner": RESIDUALS / "P8_Y5_R2FR_3738_RUNNER_STATUS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3738_THEOREM_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3738_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3738_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3738_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3738_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3738_VALIDATION.csv",
        "doc": DOC,
    }
    coefficients = coefficient_ledger(timestamp)
    atomic_terms = atomic_beta_terms(timestamp)
    open_inputs = open_input_ledger(timestamp, coefficients)
    grouped = {
        "source_register": source_register(timestamp),
        "coefficient_ledger": coefficients,
        "atomic_terms": atomic_terms,
        "formula_rows": beta_formula_rows(timestamp),
        "open_inputs": open_inputs,
        "runner": runner_rows(timestamp, coefficients, atomic_terms, open_inputs),
        "theorems": theorem_rows(timestamp),
        "claim_gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "status": status_rows(timestamp),
        "next_target": next_target_rows(timestamp),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(timestamp, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3738 validation failed: {failures}")
    print("wrote 3738 checkpoint: beta assembly interface derived, numeric values still blocked")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3732"
BRANCH_ID = "MTS_R2FR_Y5_FIRST_ARENA_RESPONSE_SPECIALIZATION_NEWTON_PPN_AND_EM_3732"
DOC = ROOT / "3732-Y5-R2FR-first-arena-response-specialization-Newton-PPN-and-EM.md"

DOC_3731 = ROOT / "3731-Y5-R2FR-parent-JX-current-and-arena-response-matrix.md"
NEXT_3731 = RESIDUALS / "P8_Y5_R2FR_3731_NEXT_TARGET.csv"
VALIDATION_3731 = RESIDUALS / "P8_Y5_BRR545_3731_VALIDATION.csv"
COMPONENTS_3731 = RESIDUALS / "P8_Y5_R2FR_3731_PARENT_CURRENT_COMPONENTS.csv"
RESPONSE_3731 = RESIDUALS / "P8_Y5_R2FR_3731_RESPONSE_MATRIX_ROWS.csv"
SIGMA_3731 = RESIDUALS / "P8_Y5_R2FR_3731_SIGMA_PROJECTION_ROWS.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
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


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3731", DOC_3731, "JX_AND_RESPONSE_MATRIX_CONTRACT_READY", "3731 parent current and response contract"),
        ("next_3731", NEXT_3731, "3732-Y5-R2FR-first-arena-response-specialization-Newton-PPN-and-EM.md", "3731 handoff"),
        ("validation_3731", VALIDATION_3731, "next_target_3732", "3731 validation"),
        ("components_3731", COMPONENTS_3731, "J_EM", "3731 parent current components"),
        ("response_3731", RESPONSE_3731, "EM_Poynting_waves", "3731 response matrix arenas"),
        ("sigma_3731", SIGMA_3731, "Newton_limit", "3731 sigma projection rows"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(ts),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "role": role,
        })
    return rows


def basis_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("NPB3732_0_phi", "Newton_PPN_bridge", "domain", "h_phi", "Poisson potential perturbation delta Phi", "m^2 s^-2 or geometric units"),
        ("NPB3732_1_psi", "Newton_PPN_bridge", "domain", "h_psi", "space-curvature potential perturbation delta Psi", "dimensionless/geometric"),
        ("NPB3732_2_gm", "Newton_PPN_bridge", "domain", "h_GM", "measured-GM/source-normalization perturbation", "dimensionless"),
        ("NPB3732_3_pf", "Newton_PPN_bridge", "domain", "h_pref", "preferred-frame/disformal perturbation coordinate", "dimensionless"),
        ("NPB3732_4_boundary", "Newton_PPN_bridge", "domain", "h_bdy", "boundary/support/local-domain residual coordinate", "arena residual units"),
        ("NPB3732_5_a", "Newton_PPN_bridge", "observable", "y_accel", "local acceleration residual delta a + grad delta Phi", "m s^-2 or geometric"),
        ("NPB3732_6_poisson", "Newton_PPN_bridge", "observable", "y_poisson", "Poisson residual nabla^2 Phi - 4 pi G rho_eff", "source density units"),
        ("NPB3732_7_gamma", "Newton_PPN_bridge", "observable", "y_gamma", "PPN gamma minus one", "dimensionless"),
        ("NPB3732_8_beta", "Newton_PPN_bridge", "observable", "y_beta", "PPN beta minus one", "dimensionless"),
        ("NPB3732_9_pfobs", "Newton_PPN_bridge", "observable", "y_pref", "preferred-frame residual vector", "dimensionless"),
        ("EMB3732_0_hodge", "EM_Poynting_bridge", "domain", "h_chi", "Hodge/constitutive perturbation delta chi", "constitutive units"),
        ("EMB3732_1_frame", "EM_Poynting_bridge", "domain", "h_frame", "metric/frame perturbation H^X entering EM stress", "dimensionless"),
        ("EMB3732_2_current", "EM_Poynting_bridge", "domain", "h_Jem", "electric source-current/readout perturbation", "current density units"),
        ("EMB3732_3_marker", "EM_Poynting_bridge", "domain", "h_alpha", "charge/fine-structure/material marker perturbation", "dimensionless"),
        ("EMB3732_4_tail", "EM_Poynting_bridge", "domain", "h_EM_tail", "boundary/non-Hilbert/material tail residual", "EM residual units"),
        ("EMB3732_5_poynting", "EM_Poynting_bridge", "observable", "y_poynting", "Poynting theorem residual partial_t u + div S + J dot E", "power density units"),
        ("EMB3732_6_stress", "EM_Poynting_bridge", "observable", "y_stress", "Maxwell stress-divergence/momentum-balance residual", "force density units"),
        ("EMB3732_7_wave", "EM_Poynting_bridge", "observable", "y_wave", "wave-speed/dispersion residual", "dimensionless or s^-1"),
        ("EMB3732_8_polarization", "EM_Poynting_bridge", "observable", "y_pol", "polarization/birefringence residual", "dimensionless"),
        ("EMB3732_9_charge", "EM_Poynting_bridge", "observable", "y_charge", "charge/current continuity residual", "charge density rate units"),
    ]
    return [
        {
            **base(ts),
            "basis_id": basis_id,
            "bridge": bridge,
            "basis_type": basis_type,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "source_owned": False,
            "claim_allowed": False,
        }
        for basis_id, bridge, basis_type, symbol, definition, units in rows
    ]


def response_entry_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("B3732_NP_accel_phi", "Newton_PPN_bridge", "B_A", "y_accel", "h_phi", "grad_operator_norm_C_grad", "maps potential perturbation to acceleration residual"),
        ("B3732_NP_poisson_phi", "Newton_PPN_bridge", "B_A", "y_poisson", "h_phi", "laplacian_operator_norm_C_lap", "maps potential perturbation to Poisson residual"),
        ("B3732_NP_poisson_gm", "Newton_PPN_bridge", "B_A", "y_poisson", "h_GM", "4pi_rho_norm_C_GM", "maps measured-G/source normalization into Poisson residual"),
        ("B3732_NP_gamma_phipsi", "Newton_PPN_bridge", "B_A", "y_gamma", "h_phi;h_psi", "C_gamma_metric_ratio", "maps two-potential relation to gamma-1"),
        ("B3732_NP_beta_phi", "Newton_PPN_bridge", "B_A", "y_beta", "h_phi", "C_beta_second_order", "maps second-order potential response to beta-1"),
        ("B3732_NP_pref_pref", "Newton_PPN_bridge", "B_A", "y_pref", "h_pref", "C_preferred_frame", "maps disformal/preferred-frame branch to PPN preferred-frame residual"),
        ("B3732_NP_boundary", "Newton_PPN_bridge", "B_A", "y_accel;y_poisson", "h_bdy", "C_boundary_projection", "maps boundary/support tail into Newton/PPN residuals"),
        ("B3732_EM_poynting_chi", "EM_Poynting_bridge", "B_A", "y_poynting", "h_chi", "C_poynting_chi_derivative", "maps constitutive/Hodge perturbation to Poynting theorem residual"),
        ("B3732_EM_poynting_current", "EM_Poynting_bridge", "B_A", "y_poynting", "h_Jem", "C_JdotE", "maps source-current perturbation to J dot E residual"),
        ("B3732_EM_stress_frame", "EM_Poynting_bridge", "B_A", "y_stress", "h_frame", "C_TEM_frame", "maps frame perturbation into Maxwell stress residual"),
        ("B3732_EM_wave_chi", "EM_Poynting_bridge", "B_A", "y_wave", "h_chi", "C_wave_constitutive", "maps constitutive perturbation into wave speed/dispersion residual"),
        ("B3732_EM_pol_chi", "EM_Poynting_bridge", "B_A", "y_pol", "h_chi", "C_birefringence", "maps anisotropic constitutive perturbation into polarization residual"),
        ("B3732_EM_charge_marker", "EM_Poynting_bridge", "B_A", "y_charge", "h_alpha", "C_charge_marker", "maps charge/fine-structure marker perturbation into continuity/readout residual"),
        ("B3732_EM_tail", "EM_Poynting_bridge", "B_A", "y_poynting;y_stress;y_wave;y_pol;y_charge", "h_EM_tail", "C_EM_tail_projection", "maps retained EM tail into all EM observables"),
    ]
    return [
        {
            **base(ts),
            "entry_id": entry_id,
            "bridge": bridge,
            "matrix": matrix,
            "observable_row": observable_row,
            "domain_col": domain_col,
            "symbolic_entry": symbolic_entry,
            "meaning": meaning,
            "numeric_value": "MISSING_NUMERIC_OR_THEOREM_ENTRY",
            "source_path": "MISSING_SOURCE_OR_DERIVATION_PATH",
            "source_owned": False,
            "claim_allowed": False,
        }
        for entry_id, bridge, matrix, observable_row, domain_col, symbolic_entry, meaning in rows
    ]


def sigma_specialization_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "SIG3732_NP",
            "Newton_PPN_bridge",
            "sigma_NP <= C_trace|c_g| ||T|| + C_dis|b_dis| ||T_UU|| + |Delta_GM| + |boundary_NP| + |tail_NP|",
            "This is the source-current side of local GR/Newton reduction. It vanishes only under quotient/no-shadow plus source-calibration silence.",
            "c_g,b_dis,T,T_UU,Delta_GM,boundary_NP,tail_NP",
        ),
        (
            "SIG3732_EM",
            "EM_Poynting_bridge",
            "sigma_EM <= C_chi||partial_X chi|| ||F^2|| + C_frame||H^X:T_EM|| + C_J||delta_X J_EM|| + |b_alpha C_alpha| + |tail_EM|",
            "This is the source-current side of Maxwell/EM stress recovery. It vanishes only if Hodge/constitutive, frame, charge-marker, and tail variations vanish.",
            "partial_X_chi,H^X,T_EM,delta_X_J_EM,b_alpha,tail_EM",
        ),
    ]
    return [
        {
            **base(ts),
            "sigma_id": sigma_id,
            "bridge": bridge,
            "sigma_formula": formula,
            "meaning": meaning,
            "missing_inputs": missing,
            "ready_for_3729": False,
            "claim_allowed": False,
        }
        for sigma_id, bridge, formula, meaning, missing in rows
    ]


def theorem_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "THM3732_0_Newton_PPN_basis",
            "Newton/PPN recovery can be tested by y_NP=(acceleration residual, Poisson residual, gamma-1, beta-1, preferred-frame residual).",
            "This converts local GR/Newton reduction into observable residual basis rows rather than a verbal target.",
            "DERIVED_BASIS_CONTRACT",
        ),
        (
            "THM3732_1_Newton_PPN_matrix",
            "beta_NP^2=lambda_max(G_NP^{-1/2} B_NP^T W_NP B_NP G_NP^{-1/2}).",
            "A PPN/Newton pass needs B_NP/W_NP/G_NP entries, not just a positive Xi_loc.",
            "DERIVED_RESPONSE_CONTRACT",
        ),
        (
            "THM3732_2_EM_Poynting_basis",
            "EM recovery can be tested by y_EM=(Poynting residual, Maxwell-stress residual, wave residual, polarization residual, charge-continuity residual).",
            "This turns Maxwell/EM stress into a gateable arena parallel to Newton/PPN.",
            "DERIVED_BASIS_CONTRACT",
        ),
        (
            "THM3732_3_EM_Poynting_matrix",
            "beta_EM^2=lambda_max(G_EM^{-1/2} B_EM^T W_EM B_EM G_EM^{-1/2}).",
            "Poynting intuition becomes a matrix norm plus source-current bound, not an assumed background field success.",
            "DERIVED_RESPONSE_CONTRACT",
        ),
        (
            "THM3732_4_zero_conditions",
            "Newton/PPN and EM residuals vanish only if the corresponding sigma bridge is theorem-zero and beta is finite, or if the 3729 residual bound beats a sourced bound_A.",
            "This is the no-smuggling rule for GR/Newton/Maxwell recovery.",
            "ANTI_OVERCLAIM",
        ),
    ]
    return [
        {
            **base(ts),
            "theorem_id": theorem_id,
            "clause": clause,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for theorem_id, clause, meaning, status in rows
    ]


def runner_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "runner_id": "RUN3732_0_FIRST_ARENA_SPECIALIZATION",
        "Newton_PPN_basis_ready": True,
        "EM_Poynting_basis_ready": True,
        "Newton_PPN_matrix_entries_numeric": False,
        "EM_Poynting_matrix_entries_numeric": False,
        "sigma_specializations_numeric": False,
        "ready_for_3729": False,
        "status": "FIRST_ARENA_SPECIALIZATION_READY_VALUES_MISSING",
        "claim_allowed": False,
    }]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    gates = [
        ("CG3732_0_basis", "PASS_NONCLAIM", "Newton/PPN and EM/Poynting basis rows exist"),
        ("CG3732_1_matrix_entries", "BLOCKED", "B_NP/W_NP/G_NP and B_EM/W_EM/G_EM entries are symbolic"),
        ("CG3732_2_sigma_NP", "BLOCKED", "Newton/PPN sigma inputs c_g,b_dis,Delta_GM,boundary/tail are missing"),
        ("CG3732_3_sigma_EM", "BLOCKED", "EM sigma inputs partial_X chi,H^X,delta_X J_EM,b_alpha/tail are missing"),
        ("CG3732_4_3729_feed", "BLOCKED", "no numeric beta_A/sigma_A can feed 3729 yet"),
        ("CG3732_5_claim", "BLOCKED", "no local GR/Newton/Maxwell claim allowed"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate_status": status,
            "required_before_claim": required,
            "claim_allowed": False,
        }
        for gate_id, status, required in gates
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "status_id": "STATUS3732_0",
        "status": "FIRST_ARENA_SPECIALIZATION_READY_VALUES_MISSING",
        "summary": "3732 specializes the 3731 contract into Newton/PPN and EM/Poynting observable bases plus symbolic response entries. It is ready for theorem-zero or numeric source rows, but no arena can score yet.",
        "claim_allowed": False,
    }]


def decision_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3732_0_Newton_PPN_bridge",
            "Newton/PPN is now the primary local-GR reduction bridge.",
            "It directly tests acceleration, Poisson, gamma, beta, and preferred-frame residuals.",
        ),
        (
            "DEC3732_1_EM_bridge",
            "EM/Poynting is retained as the Maxwell-stress bridge.",
            "It tests Poynting balance, Maxwell stress, waves, polarization, and charge continuity.",
        ),
        (
            "DEC3732_2_next",
            "Next derive zero-or-bound clauses for H^X and partial_X chi.",
            "Those two quantities are common bottlenecks: H^X feeds matter/PPN/Newton/EM stress, while partial_X chi controls the Maxwell/Hodge route.",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in rows
    ]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3732_0",
        "target_doc": "3733-Y5-R2FR-HX-and-Hodge-variation-zero-or-bound.md",
        "target_script": "scripts/Y5_R2FR_3733_HX_and_Hodge_variation_zero_or_bound.py",
        "objective": "derive or bound H^X=partial_X g_matter and partial_X chi, because these two coefficients feed Newton/PPN, EM/Poynting, clocks, and source coupling",
        "success_gate": "either quotient/no-shadow gives theorem-zero rows, or finite H^X and partial_X chi bound rows are staged with units and no-cancellation gates",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3732*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    basis = parse_csv(paths["basis"])
    entries = parse_csv(paths["entries"])
    sigma = parse_csv(paths["sigma"])
    theorem_text = read_text(paths["theorems"])
    doc_text = read_text(paths["doc"])
    checks = [
        ("sources_exist", "sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "outputs exist", all(path.exists() for path in generated)),
        ("csv_parse", "CSVs parse", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("basis_rows", "Newton/PPN and EM basis rows present", len(basis) == 20),
        ("domain_and_observable", "domain and observable basis rows present", all(any(row["bridge"] == bridge and row["basis_type"] == kind for row in basis) for bridge in ["Newton_PPN_bridge", "EM_Poynting_bridge"] for kind in ["domain", "observable"])),
        ("matrix_entries", "symbolic response entries present", len(entries) == 14),
        ("sigma_specializations", "two sigma specializations present", len(sigma) == 2),
        ("Newton_formula", "Newton/PPN acceleration and PPN entries present", all(token in read_text(paths["entries"]) for token in ["y_accel", "y_gamma", "y_beta"])),
        ("EM_formula", "EM/Poynting entries present", all(token in read_text(paths["entries"]) for token in ["y_poynting", "y_stress", "y_wave"])),
        ("theorems", "Newton/PPN and EM theorem contracts present", all(token in theorem_text for token in ["Newton/PPN", "EM recovery", "beta_EM^2"])),
        ("claim_gates_blocked", "claim gates block promotion", all(row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("runner_blocks_scoring", "runner blocks scoring", parse_csv(paths["runner"])[0]["ready_for_3729"] == "False"),
        ("next_target_3733", "next target is H^X/Hodge variation", all(token in read_text(paths["next_target"]) for token in ["3733", "H^X", "partial_X chi"])),
        ("doc_core_terms", "doc contains specialization status", all(token in doc_text for token in ["Newton_PPN_bridge", "EM_Poynting_bridge", "partial_X chi", "H^X"])),
        ("no_formalization_leak", "no 3732 files in formalization-workbench", len(formal_files) == 0),
    ]
    return [
        {
            **base(ts),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "",
        }
        for validation_id, description, result in checks
    ]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3732 - First Arena Response Specialization: Newton/PPN and EM",
        "",
        "## Status",
        "- `FIRST_ARENA_SPECIALIZATION_READY_VALUES_MISSING`",
        "- `Newton_PPN_bridge` tests local GR/Newton through acceleration, Poisson, PPN gamma/beta, and preferred-frame residuals.",
        "- `EM_Poynting_bridge` tests Maxwell/EM stress through Poynting, stress, wave, polarization, and charge-continuity residuals.",
        "- Current specialization is claim-blocked until `H^X`, `partial_X chi`, source tails, and response entries are theorem-zero or numeric/source-owned.",
        "",
        "## Basis Rows",
    ]
    for row in grouped["basis"]:
        lines.append(f"- `{row['bridge']}` `{row['basis_type']}` `{row['symbol']}`: {row['definition']}")
    lines.extend(["", "## Response Entries"])
    for row in grouped["entries"]:
        lines.append(f"- `{row['entry_id']}` `{row['observable_row']}` <- `{row['domain_col']}` via `{row['symbolic_entry']}` | {row['meaning']}")
    lines.extend(["", "## Sigma Specializations"])
    for row in grouped["sigma"]:
        lines.append(f"- `{row['sigma_id']}`: {row['sigma_formula']} | missing: {row['missing_inputs']}")
    lines.extend(["", "## Theorem Rows"])
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['clause']} | {row['meaning']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` {row['decision']} | {row['rationale']}")
    lines.extend(["", "## Next Target"])
    lines.append("- `3733-Y5-R2FR-HX-and-Hodge-variation-zero-or-bound.md`")
    lines.append("- Objective: derive or bound `H^X=partial_X g_matter` and `partial_X chi`, because those are the common coefficients behind Newton/PPN and EM/Poynting recovery.")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3732_SOURCE_REGISTER.csv",
        "basis": RESIDUALS / "P8_Y5_R2FR_3732_ARENA_BASIS_ROWS.csv",
        "entries": RESIDUALS / "P8_Y5_R2FR_3732_RESPONSE_ENTRY_ROWS.csv",
        "sigma": RESIDUALS / "P8_Y5_R2FR_3732_SIGMA_SPECIALIZATION_ROWS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3732_THEOREM_ROWS.csv",
        "runner": RESIDUALS / "P8_Y5_R2FR_3732_RUNNER_STATUS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3732_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3732_STATUS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3732_DECISION_ROWS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3732_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3732_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(ts),
        "basis": basis_rows(ts),
        "entries": response_entry_rows(ts),
        "sigma": sigma_specialization_rows(ts),
        "theorems": theorem_rows(ts),
        "runner": runner_rows(ts),
        "claim_gates": claim_gate_rows(ts),
        "status": status_rows(ts),
        "decisions": decision_rows(ts),
        "next_target": next_target_rows(ts),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(ts, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3732 validation failed: {failures}")
    print("wrote 3732 checkpoint: Newton/PPN and EM/Poynting first arena specializations ready, values missing")


if __name__ == "__main__":
    main()

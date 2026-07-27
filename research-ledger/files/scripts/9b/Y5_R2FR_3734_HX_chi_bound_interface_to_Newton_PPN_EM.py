from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3734"
BRANCH_ID = "MTS_R2FR_Y5_HX_CHI_BOUND_INTERFACE_TO_NEWTON_PPN_EM_3734"
DOC = ROOT / "3734-Y5-R2FR-HX-chi-bound-interface-to-Newton-PPN-EM.md"

DOC_3733 = ROOT / "3733-Y5-R2FR-HX-and-Hodge-variation-zero-or-bound.md"
NEXT_3733 = RESIDUALS / "P8_Y5_R2FR_3733_NEXT_TARGET.csv"
VALIDATION_3733 = RESIDUALS / "P8_Y5_BRR545_3733_VALIDATION.csv"
FINITE_3733 = RESIDUALS / "P8_Y5_R2FR_3733_FINITE_BOUND_ROWS.csv"
FEEDS_3733 = RESIDUALS / "P8_Y5_R2FR_3733_ARENA_FEED_ROWS.csv"
ENTRIES_3732 = RESIDUALS / "P8_Y5_R2FR_3732_RESPONSE_ENTRY_ROWS.csv"
BASIS_3732 = RESIDUALS / "P8_Y5_R2FR_3732_ARENA_BASIS_ROWS.csv"


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


def try_float(value: object) -> float | None:
    try:
        parsed = float(str(value))
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3733", DOC_3733, "HX_CHI_ZERO_CONDITIONAL_FINITE_BOUND_SCHEMA_READY", "3733 zero/bound result"),
        ("next_3733", NEXT_3733, "3734-Y5-R2FR-HX-chi-bound-interface-to-Newton-PPN-EM.md", "3733 handoff"),
        ("validation_3733", VALIDATION_3733, "next_target_3734", "3733 validation"),
        ("finite_3733", FINITE_3733, "HX_chi_total_abs", "3733 finite bound rows"),
        ("feeds_3733", FEEDS_3733, "Newton_PPN_bridge", "3733 arena feed formulas"),
        ("entries_3732", ENTRIES_3732, "B3732_EM_poynting_chi", "3732 response entries"),
        ("basis_3732", BASIS_3732, "EM_Poynting_bridge", "3732 basis rows"),
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


def sigma_input_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("SIGIN3734_NP_Hbar", "Newton_PPN_bridge", "Hbar_X", "MISSING_HBAR_X", "nonnegative", "dimensionless", "frame/metric variation envelope from 3733"),
        ("SIGIN3734_NP_T", "Newton_PPN_bridge", "T_norm_NP", "MISSING_T_NORM_NP", "nonnegative", "stress norm", "ordinary/source stress norm in local Newton/PPN arena"),
        ("SIGIN3734_NP_CH", "Newton_PPN_bridge", "C_NP_H", "MISSING_C_NP_H", "nonnegative", "operator coefficient", "projection coefficient from Hbar_X*T_norm into Newton/PPN source residual"),
        ("SIGIN3734_NP_DGM", "Newton_PPN_bridge", "Delta_GM", "MISSING_DELTA_GM", "nonnegative", "dimensionless/source norm", "measured-GM/source-normalization residual"),
        ("SIGIN3734_NP_BDY", "Newton_PPN_bridge", "boundary_NP", "MISSING_BOUNDARY_NP", "nonnegative", "residual norm", "Newton/PPN boundary/support residual"),
        ("SIGIN3734_NP_TAIL", "Newton_PPN_bridge", "tail_NP", "MISSING_TAIL_NP", "nonnegative", "residual norm", "other retained Newton/PPN source tails"),
        ("SIGIN3734_EM_Chibar", "EM_Poynting_bridge", "Chibar_total", "MISSING_CHIBAR_TOTAL", "nonnegative", "constitutive norm", "total Hodge/constitutive variation envelope from 3733"),
        ("SIGIN3734_EM_F2", "EM_Poynting_bridge", "F2_norm", "MISSING_F2_NORM", "nonnegative", "field invariant norm", "local EM field-strength squared norm"),
        ("SIGIN3734_EM_Cchi", "EM_Poynting_bridge", "C_EM_chi", "MISSING_C_EM_CHI", "nonnegative", "operator coefficient", "projection from Chibar_total*F2_norm into EM residual"),
        ("SIGIN3734_EM_Hbar", "EM_Poynting_bridge", "Hbar_X", "MISSING_HBAR_X", "nonnegative", "dimensionless", "frame/metric variation entering EM stress"),
        ("SIGIN3734_EM_TEM", "EM_Poynting_bridge", "T_EM_norm", "MISSING_T_EM_NORM", "nonnegative", "EM stress norm", "Maxwell stress norm"),
        ("SIGIN3734_EM_Cframe", "EM_Poynting_bridge", "C_EM_frame", "MISSING_C_EM_FRAME", "nonnegative", "operator coefficient", "projection from Hbar_X*T_EM into EM stress residual"),
        ("SIGIN3734_EM_DJ", "EM_Poynting_bridge", "delta_J_EM", "MISSING_DELTA_J_EM", "nonnegative", "current norm", "electric source-current/readout perturbation"),
        ("SIGIN3734_EM_CJ", "EM_Poynting_bridge", "C_EM_J", "MISSING_C_EM_J", "nonnegative", "operator coefficient", "projection from current perturbation to Poynting residual"),
        ("SIGIN3734_EM_BALPHA", "EM_Poynting_bridge", "b_alpha_C_alpha", "MISSING_B_ALPHA_C_ALPHA", "nonnegative", "marker residual norm", "charge/fine-structure marker contribution"),
        ("SIGIN3734_EM_TAIL", "EM_Poynting_bridge", "tail_EM", "MISSING_TAIL_EM", "nonnegative", "residual norm", "other retained EM tails"),
    ]
    return [
        {
            **base(ts),
            "input_id": input_id,
            "bridge": bridge,
            "quantity": quantity,
            "value": value,
            "required_sign": required_sign,
            "units": units,
            "meaning": meaning,
            "source_path": "MISSING_SOURCE_OR_THEOREM_PATH",
            "source_owned": False,
            "claim_allowed": False,
        }
        for input_id, bridge, quantity, value, required_sign, units, meaning in specs
    ]


def bridge_formula_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "FORM3734_NP_sigma",
            "Newton_PPN_bridge",
            "sigma_NP = C_NP_H*Hbar_X*T_norm_NP + Delta_GM + boundary_NP + tail_NP",
            "compressed H^X feed into Newton/PPN source residual; c_g/b_dis expansion remains inside Hbar_X unless expanded later",
            "SIGIN3734_NP_Hbar;SIGIN3734_NP_T;SIGIN3734_NP_CH;SIGIN3734_NP_DGM;SIGIN3734_NP_BDY;SIGIN3734_NP_TAIL",
        ),
        (
            "FORM3734_EM_sigma",
            "EM_Poynting_bridge",
            "sigma_EM = C_EM_chi*Chibar_total*F2_norm + C_EM_frame*Hbar_X*T_EM_norm + C_EM_J*delta_J_EM + b_alpha_C_alpha + tail_EM",
            "compressed Hodge/H^X feed into Maxwell/Poynting source residual",
            "SIGIN3734_EM_Chibar;SIGIN3734_EM_F2;SIGIN3734_EM_Cchi;SIGIN3734_EM_Hbar;SIGIN3734_EM_TEM;SIGIN3734_EM_Cframe;SIGIN3734_EM_DJ;SIGIN3734_EM_CJ;SIGIN3734_EM_BALPHA;SIGIN3734_EM_TAIL",
        ),
    ]
    return [
        {
            **base(ts),
            "formula_id": formula_id,
            "bridge": bridge,
            "sigma_formula": sigma_formula,
            "meaning": meaning,
            "input_ids": input_ids,
            "ready_for_3729": False,
            "claim_allowed": False,
        }
        for formula_id, bridge, sigma_formula, meaning, input_ids in rows
    ]


def beta_link_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "BETA3734_NP",
            "Newton_PPN_bridge",
            "beta_NP^2=lambda_max(G_NP^{-1/2} B_NP^T W_NP B_NP G_NP^{-1/2})",
            "P8_Y5_R2FR_3732_RESPONSE_ENTRY_ROWS.csv rows B3732_NP_*",
            "MISSING_B_NP_W_NP_G_NP_NUMERIC_OR_THEOREM",
        ),
        (
            "BETA3734_EM",
            "EM_Poynting_bridge",
            "beta_EM^2=lambda_max(G_EM^{-1/2} B_EM^T W_EM B_EM G_EM^{-1/2})",
            "P8_Y5_R2FR_3732_RESPONSE_ENTRY_ROWS.csv rows B3732_EM_*",
            "MISSING_B_EM_W_EM_G_EM_NUMERIC_OR_THEOREM",
        ),
    ]
    return [
        {
            **base(ts),
            "beta_id": beta_id,
            "bridge": bridge,
            "beta_formula": formula,
            "source_response_rows": source_rows,
            "current_status": status,
            "ready_for_3729": False,
            "claim_allowed": False,
        }
        for beta_id, bridge, formula, source_rows, status in rows
    ]


def runner_rows(ts: str, inputs: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for bridge in ["Newton_PPN_bridge", "EM_Poynting_bridge"]:
        bridge_inputs = [row for row in inputs if row["bridge"] == bridge]
        missing: list[str] = []
        values: dict[str, float] = {}
        for row in bridge_inputs:
            parsed = try_float(row["value"])
            if parsed is None or str(row["source_owned"]) != "True":
                missing.append(str(row["quantity"]))
                continue
            if row["required_sign"] == "nonnegative" and parsed < 0:
                missing.append(f"sign:{row['quantity']}")
                continue
            values[str(row["quantity"])] = parsed
        executable = not missing
        sigma_value: float | str = ""
        status = "BLOCKED_MISSING_SOURCE_OWNED_SIGMA_INPUTS"
        if executable and bridge == "Newton_PPN_bridge":
            sigma_value = values["C_NP_H"] * values["Hbar_X"] * values["T_norm_NP"] + values["Delta_GM"] + values["boundary_NP"] + values["tail_NP"]
            status = "EXECUTABLE_SIGMA_NONCLAIM"
        if executable and bridge == "EM_Poynting_bridge":
            sigma_value = (
                values["C_EM_chi"] * values["Chibar_total"] * values["F2_norm"]
                + values["C_EM_frame"] * values["Hbar_X"] * values["T_EM_norm"]
                + values["C_EM_J"] * values["delta_J_EM"]
                + values["b_alpha_C_alpha"]
                + values["tail_EM"]
            )
            status = "EXECUTABLE_SIGMA_NONCLAIM"
        rows.append({
            **base(ts),
            "runner_id": f"RUN3734_{bridge}",
            "bridge": bridge,
            "formula": "sigma_NP or sigma_EM compressed interface formula",
            "executable": executable,
            "missing_inputs": ";".join(missing),
            "sigma_value": sigma_value,
            "status": status,
            "ready_for_3729": False,
            "claim_allowed": False,
        })
    return rows


def fill_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "FILL3734_NP",
            "Newton_PPN_bridge",
            "sigma_A=sigma_NP from RUN3734_Newton_PPN_bridge; beta_A=beta_NP from BETA3734_NP; ell_A, epsilon_A, bound_A still required by 3729",
            "sigma_NP;beta_NP;ell_NP;epsilon_NP;bound_NP",
        ),
        (
            "FILL3734_EM",
            "EM_Poynting_bridge",
            "sigma_A=sigma_EM from RUN3734_EM_Poynting_bridge; beta_A=beta_EM from BETA3734_EM; ell_A, epsilon_A, bound_A still required by 3729",
            "sigma_EM;beta_EM;ell_EM;epsilon_EM;bound_EM",
        ),
    ]
    return [
        {
            **base(ts),
            "fill_id": fill_id,
            "bridge": bridge,
            "fill_contract": fill_contract,
            "required_for_3729": required,
            "ready_for_3729": False,
            "claim_allowed": False,
        }
        for fill_id, bridge, fill_contract, required in rows
    ]


def theorem_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "THM3734_0_NP_sigma_interface",
            "Hbar_X plus source stress/G calibration/boundary tails determine a compressed sigma_NP input row.",
            "Turns the H^X bound into a Newton/PPN source residual interface.",
            "DERIVED_INTERFACE",
        ),
        (
            "THM3734_1_EM_sigma_interface",
            "Chibar_total and Hbar_X plus EM field/current/marker/tail norms determine a compressed sigma_EM input row.",
            "Turns the Hodge/H^X bound into a Maxwell/Poynting source residual interface.",
            "DERIVED_INTERFACE",
        ),
        (
            "THM3734_2_beta_separation",
            "sigma_A source bounds and beta_A response norms remain separate until 3729 combines them.",
            "Prevents hiding source uncertainty inside response coefficients.",
            "ANTI_SMUGGLING",
        ),
        (
            "THM3734_3_nonclaim",
            "All interface rows stay nonclaim until every input is numeric/source-owned or theorem-zero.",
            "The interface is a socket for future derivations, not a pass.",
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


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    gates = [
        ("CG3734_0_formulas", "PASS_NONCLAIM", "sigma_NP and sigma_EM formulas are written"),
        ("CG3734_1_inputs", "BLOCKED", "all sigma inputs are placeholders"),
        ("CG3734_2_beta", "BLOCKED", "beta_NP and beta_EM matrices are not numeric/source-owned"),
        ("CG3734_3_3729", "BLOCKED", "ell_A, epsilon_A, and bound_A are still needed before 3729 scoring"),
        ("CG3734_4_claim", "BLOCKED", "no Newton/PPN/EM/local-GR claim allowed"),
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


def decision_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3734_0_interface_ready",
            "HX_CHI_TO_SIGMA_INTERFACE_READY",
            "Hbar_X and Chibar_total now have fillable paths into Newton/PPN and EM/Poynting sigma rows.",
        ),
        (
            "DEC3734_1_still_blocked",
            "VALUES_AND_RESPONSE_MATRICES_MISSING",
            "The interface is structurally ready but cannot score until source-owned input values and beta matrices exist.",
        ),
        (
            "DEC3734_2_next",
            "NEXT_ATTACK_RESPONSE_MATRICES_OR_PARENT_ZERO",
            "Best next move is either derive Hbar_X/Chibar_total theorem-zero, or build B_NP/B_EM numeric/theorem response matrices.",
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


def status_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "status_id": "STATUS3734_0",
        "status": "HX_CHI_BOUND_INTERFACE_READY_CURRENTLY_BLOCKED",
        "summary": "3734 connects Hbar_X and Chibar_total to fillable sigma_NP and sigma_EM rows for Newton/PPN and EM/Poynting. Current rows are placeholders and remain blocked for claim/scoring.",
        "claim_allowed": False,
    }]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3734_0",
        "target_doc": "3735-Y5-R2FR-response-matrix-first-pass-Newton-PPN-EM.md",
        "target_script": "scripts/Y5_R2FR_3735_response_matrix_first_pass_Newton_PPN_EM.py",
        "objective": "build the first B_NP/W_NP/G_NP and B_EM/W_EM/G_EM response-matrix contracts so beta_NP and beta_EM can become computable",
        "success_gate": "response matrices have finite basis, symbolic entries, positivity/norm gates, and refusal rows for missing numeric/theorem entries",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3734*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    inputs = parse_csv(paths["sigma_inputs"])
    runner = parse_csv(paths["runner"])
    formulas = read_text(paths["bridge_formulas"])
    doc_text = read_text(paths["doc"])
    checks = [
        ("sources_exist", "sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "outputs exist", all(path.exists() for path in generated)),
        ("csv_parse", "CSVs parse", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("input_schema", "sixteen sigma interface inputs present", len(inputs) == 16),
        ("Hbar_and_Chibar", "Hbar_X and Chibar_total inputs present", all(any(row["quantity"] == quantity for row in inputs) for quantity in ["Hbar_X", "Chibar_total"])),
        ("formula_rows", "sigma_NP and sigma_EM formulas present", all(token in formulas for token in ["sigma_NP", "sigma_EM", "Chibar_total", "Hbar_X"])),
        ("runner_blocks", "runner blocks placeholder scoring", all(row["status"] == "BLOCKED_MISSING_SOURCE_OWNED_SIGMA_INPUTS" for row in runner)),
        ("beta_links", "beta links exist", all(token in read_text(paths["beta_links"]) for token in ["beta_NP", "beta_EM"])),
        ("fill_rows", "3729 fill contracts exist", all(token in read_text(paths["fills"]) for token in ["ell_NP", "ell_EM", "bound_NP", "bound_EM"])),
        ("claim_gates_blocked", "claim gates block promotion", all(row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("next_target_3735", "next target is response matrix pass", all(token in read_text(paths["next_target"]) for token in ["3735", "response", "beta_NP", "beta_EM"])),
        ("doc_core_terms", "doc contains interface status", all(token in doc_text for token in ["Hbar_X", "Chibar_total", "sigma_NP", "sigma_EM"])),
        ("no_formalization_leak", "no 3734 files in formalization-workbench", len(formal_files) == 0),
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
        "# 3734 - H^X/chi Bound Interface to Newton/PPN and EM",
        "",
        "## Status",
        "- `HX_CHI_BOUND_INTERFACE_READY_CURRENTLY_BLOCKED`",
        "- `Hbar_X` now feeds a fillable `sigma_NP` row for the Newton/PPN bridge.",
        "- `Chibar_total` and `Hbar_X` now feed a fillable `sigma_EM` row for the EM/Poynting bridge.",
        "- The interface is still blocked because all values and response matrices are placeholders.",
        "",
        "## Sigma Formulas",
    ]
    for row in grouped["bridge_formulas"]:
        lines.append(f"- `{row['formula_id']}` `{row['bridge']}`: {row['sigma_formula']}")
    lines.extend(["", "## Sigma Inputs"])
    for row in grouped["sigma_inputs"]:
        lines.append(f"- `{row['bridge']}` `{row['quantity']}` = `{row['value']}` | {row['meaning']}")
    lines.extend(["", "## Beta Links"])
    for row in grouped["beta_links"]:
        lines.append(f"- `{row['beta_id']}`: {row['beta_formula']} | status: {row['current_status']}")
    lines.extend(["", "## 3729 Fill Contracts"])
    for row in grouped["fills"]:
        lines.append(f"- `{row['fill_id']}` `{row['bridge']}`: {row['fill_contract']}")
    lines.extend(["", "## Theorem Rows"])
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['clause']} | {row['meaning']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Next Target"])
    lines.append("- `3735-Y5-R2FR-response-matrix-first-pass-Newton-PPN-EM.md`")
    lines.append("- Objective: build the first `B_NP/W_NP/G_NP` and `B_EM/W_EM/G_EM` response-matrix contracts so `beta_NP` and `beta_EM` can become computable.")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3734_SOURCE_REGISTER.csv",
        "sigma_inputs": RESIDUALS / "P8_Y5_R2FR_3734_SIGMA_INPUT_ROWS.csv",
        "bridge_formulas": RESIDUALS / "P8_Y5_R2FR_3734_BRIDGE_FORMULA_ROWS.csv",
        "beta_links": RESIDUALS / "P8_Y5_R2FR_3734_BETA_LINK_ROWS.csv",
        "runner": RESIDUALS / "P8_Y5_R2FR_3734_RUNNER_STATUS.csv",
        "fills": RESIDUALS / "P8_Y5_R2FR_3734_3729_FILL_ROWS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3734_THEOREM_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3734_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3734_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3734_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3734_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3734_VALIDATION.csv",
        "doc": DOC,
    }
    sigma_inputs = sigma_input_rows(ts)
    grouped = {
        "source_register": source_register(ts),
        "sigma_inputs": sigma_inputs,
        "bridge_formulas": bridge_formula_rows(ts),
        "beta_links": beta_link_rows(ts),
        "runner": runner_rows(ts, sigma_inputs),
        "fills": fill_rows(ts),
        "theorems": theorem_rows(ts),
        "claim_gates": claim_gate_rows(ts),
        "decisions": decision_rows(ts),
        "status": status_rows(ts),
        "next_target": next_target_rows(ts),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(ts, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3734 validation failed: {failures}")
    print("wrote 3734 checkpoint: Hbar_X/Chibar_total sigma interface ready and blocked by placeholder inputs")


if __name__ == "__main__":
    main()

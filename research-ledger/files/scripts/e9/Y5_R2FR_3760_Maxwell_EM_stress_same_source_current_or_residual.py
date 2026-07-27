import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3760"
BRANCH = "MTS_R2FR_Y5_MAXWELL_EM_STRESS_SAME_SOURCE_CURRENT_OR_RESIDUAL_3760"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3760-Y5-R2FR-Maxwell-EM-stress-same-source-current-or-residual.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3760_SOURCE_REGISTER.csv",
    "em_theorem": RESIDUALS / "P8_Y5_R2FR_3760_MAXWELL_EM_STRESS_SOURCE_THEOREM.csv",
    "em_residual": RESIDUALS / "P8_Y5_R2FR_3760_EM_SOURCE_RESIDUAL_BUDGET.csv",
    "ppn_interface": RESIDUALS / "P8_Y5_R2FR_3760_EM_TO_PPN_INTERFACE.csv",
    "runner_patch": RESIDUALS / "P8_Y5_R2FR_3760_COUPLING_RUNNER_PATCH.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3760_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3760_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3760_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3760_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3760_VALIDATION.csv",
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str, valid_for_claim: bool = False) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": valid_for_claim,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_paths() -> dict[str, Path]:
    return {
        "SRC3760_0_3759_doc": PCW / "3759-Y5-R2FR-source-universality-or-WEP-coupling-row.md",
        "SRC3760_1_3759_next": RESIDUALS / "P8_Y5_R2FR_3759_NEXT_TARGET.csv",
        "SRC3760_2_3759_em_contract": RESIDUALS / "P8_Y5_R2FR_3759_EM_STRESS_SOURCE_CONTRACT.csv",
        "SRC3760_3_3759_universality": RESIDUALS / "P8_Y5_R2FR_3759_SOURCE_UNIVERSALITY_THEOREM.csv",
        "SRC3760_4_3759_wep_bound": RESIDUALS / "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv",
        "SRC3760_5_3759_runner": RESIDUALS / "P8_Y5_R2FR_3759_COUPLING_RUNNER_PATCH.csv",
        "SRC3760_6_3758_kappa_law": RESIDUALS / "P8_Y5_R2FR_3758_KAPPA_QUOTIENT_FLUX_LAW.csv",
        "SRC3760_7_3754_flux_law": RESIDUALS / "P8_Y5_R2FR_3754_SOURCE_WARD_FLUX_LAW_ROWS.csv",
        "SRC3760_8_source_current_contract": RESIDUALS / "P8_source_current_Ward_universality_CONTRACT.csv",
        "SRC3760_9_owner_identity": RESIDUALS / "P8_Ward_source_owner_identity_CONTRACT.csv",
        "SRC3760_10_gm_matrix": RESIDUALS / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3760 Maxwell/EM stress same-source input",
        }
        for source_id, path in source_paths().items()
    ]


def runner_row(residual_id: str) -> dict[str, str]:
    rows = read_csv(source_paths()["SRC3760_5_3759_runner"])
    return next(row for row in rows if row["residual_id"] == residual_id)


def numeric_bound(residual_id: str) -> float:
    row = runner_row(residual_id)
    value = float(row["bound_value"])
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"invalid bound for {residual_id}: {row['bound_value']}")
    return value


def em_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "EMT3760_0_total_same_action",
            "Use one local source action S_src[psi_A,A_mu,g_eff,theta]=S_material+S_EM+S_int, varied with respect to the same effective metric/coframe that local gravity reads.",
            "This is the parent signature needed to stop EM/binding energy becoming a separate gravitational charge.",
            "REQUIRED_PARENT_ACTION_SIGNATURE",
            False,
        ),
        (
            "EMT3760_1_hilbert_EM_stress",
            "For S_EM=-(1/4) int sqrt(-g_eff) Z_EM F_ab F^ab, the Hilbert stress is T_EM^{ab}=Z_EM(F^{a c}F^b_c - 1/4 g_eff^{ab} F_cd F^cd), up to metric-sign convention.",
            "This makes EM energy-momentum a source term of the same variational action, not an external force patch.",
            "STANDARD_VARIATIONAL_IDENTITY_CONDITIONAL_ON_LOCAL_MAXWELL_ACTION",
            True,
        ),
        (
            "EMT3760_2_Maxwell_Ward_exchange",
            "On Maxwell equations, div T_EM^b = -F^b_c J^c while charged matter carries +F^b_c J^c, so div(T_material+T_EM+T_binding)^b equals only parent exchange q_exchange^b.",
            "The Lorentz force is internal exchange inside the same total source, not WEP-violating leakage.",
            "EXACT_SAME_ACTION_WARD_CANCELLATION",
            True,
        ),
        (
            "EMT3760_3_binding_mass",
            "Composite-body inertial mass and active source charge must include EM binding energy through the same T_total, so composition dependence is not generated by bookkeeping.",
            "This is the WEP bridge from field stress to material source charge.",
            "EXACT_IF_COMPOSITE_READOUT_USES_TOTAL_SOURCE",
            False,
        ),
        (
            "EMT3760_4_emergent_EM_descent",
            "If EM is emergent from MTS modes, its low-energy stress must descend to the same Hilbert/coframe T_EM above, with universal Z_EM and no species-labelled kappa_EM,A.",
            "This is the MTS-specific contract; without it, emergent EM is a residual channel.",
            "MTS_PARENT_DESCENT_REQUIRED",
            False,
        ),
        (
            "EMT3760_5_conditional_result",
            "Same action + universal Z_EM + same total-source readout imply no EM-owned contribution to eta_source_AB, Gdot, or first PPN source mismatch except ordinary total stress already present in GR.",
            "This is a conditional local-GR-compatible EM stress theorem, not yet parent-signed.",
            "CONDITIONAL_THEOREM_NOT_CLAIMED",
            False,
        ),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "statement": statement,
            "premise_or_note": premise_or_note,
            "status": status,
            "derived_inside_3760": derived,
            "parent_signed": False if not derived else "standard_identity",
            "claim_allowed": False,
        }
        for theorem_id, statement, premise_or_note, status, derived in entries
    ]


def em_residual_rows(timestamp: str) -> list[dict[str, object]]:
    wep_bound = numeric_bound("KRV3755_1_species_source")
    gamma_bound = numeric_bound("KRV3755_6_gamma")
    beta_bound = numeric_bound("KRV3755_7_beta")
    entries = [
        (
            "EMR3760_0_WEP_EM_binding",
            "eta_EM_AB",
            "MICROSCOPE/WEP",
            "|Delta_AB f_EM| |delta_kappa_EM| + |Delta_AB ln Z_EM| + |Delta_AB q_EM_exchange|",
            wep_bound,
            "dimensionless",
            "zero if EM stress is same-source and universal",
        ),
        (
            "EMR3760_1_gamma_EM_stress_projection",
            "delta_gamma_EM",
            "Cassini/Shapiro",
            "|epsilon_EM_metric| + |Pi_PPN q_EM_exchange| + |Delta_EM_source_frame|",
            gamma_bound,
            "dimensionless",
            "feeds gamma if EM stress does not project as ordinary total Hilbert stress",
        ),
        (
            "EMR3760_2_beta_EM_nonlinear_source",
            "delta_beta_EM",
            "PPN beta",
            "|epsilon_EM_nonlinear| + |Delta_EM_binding_second_order| + |Pi_beta q_EM_exchange|",
            beta_bound,
            "dimensionless",
            "feeds beta through nonlinear binding/source normalization",
        ),
        (
            "EMR3760_3_Gdot_EM_coupling_drift",
            "dln_Geff_dt_EM",
            "LLR/Gdot",
            "|d_t ln Z_EM| + |R_EM_exchange| + |d_t ln Z_EM_frame|",
            9.6e-15,
            "yr^-1",
            "feeds Gdot if EM normalization drifts relative to the gravitational source readout",
        ),
    ]
    return [
        {
            **base(timestamp),
            "residual_id": residual_id,
            "symbol": symbol,
            "arena": arena,
            "residual_formula": formula,
            "bound_value": bound_value,
            "units": units,
            "zero_condition": zero_condition,
            "prediction_value": "MISSING_NUMERIC_EM_COMPONENTS",
            "score_status": "BOUND_FORMULA_READY_NUMERIC_COMPONENTS_MISSING",
            "valid_prediction_row": False,
            "claim_allowed": False,
        }
        for residual_id, symbol, arena, formula, bound_value, units, zero_condition in entries
    ]


def ppn_interface_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "EP3760_0_total_source_tensor",
            "PPN source projection must use T_total = T_material + T_EM + T_binding + T_parent_exchange_mapped.",
            "If T_parent_exchange_mapped=0, this is the ordinary GR total stress source.",
            "INTERFACE_READY",
        ),
        (
            "EP3760_1_EM_trace_pressure",
            "Maxwell stress is traceless but not gravitationally silent; its energy density and spatial stresses enter the PPN source integrals through T_total.",
            "This prevents the wrong move of ignoring EM because trace(T_EM)=0.",
            "PPN_WARNING_LOCK",
        ),
        (
            "EP3760_2_no_external_Lorentz_force",
            "The Lorentz force cancels between field and charged matter in total stress conservation; only parent exchange beyond this cancellation is a residual.",
            "This keeps EM from masquerading as WEP violation.",
            "WARD_CANCELLATION_INTERFACE",
        ),
        (
            "EP3760_3_next_metric_projection",
            "Once same-source EM stress is parent-signed or residualized, gamma/beta need an explicit weak-field metric projection from T_total.",
            "This is the next PPN route.",
            "NEXT_PPN_GATE",
        ),
    ]
    return [
        {
            **base(timestamp),
            "interface_id": interface_id,
            "statement": statement,
            "impact": impact,
            "status": status,
            "claim_allowed": False,
        }
        for interface_id, statement, impact, status in entries
    ]


def runner_patch_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_row in read_csv(source_paths()["SRC3760_5_3759_runner"]):
        patched = {
            **base(timestamp),
            "patched_runner_row_id": f"RUN3760_{source_row['residual_id']}",
            "source_runner_row": source_row["patched_runner_row_id"],
            "residual_id": source_row["residual_id"],
            "symbol": source_row["symbol"],
            "arena": source_row["arena"],
            "bound_value": source_row["bound_value"],
            "units": source_row["units"],
            "prediction_status_3759": source_row["prediction_status_3759"],
            "score_status_3759": source_row["score_status_3759"],
            "prediction_status_3760": source_row["prediction_status_3759"],
            "score_status_3760": source_row["score_status_3759"],
            "prediction_or_bound_formula_3760": source_row["prediction_or_bound_formula_3759"],
            "conditional_score_ready": source_row["conditional_score_ready"],
            "valid_prediction_row": False,
            "claim_allowed": False,
            "notes": "unchanged from 3759",
        }
        if source_row["residual_id"] == "KRV3755_1_species_source":
            patched.update(
                {
                    "prediction_status_3760": "ZERO_OR_EM_COMPOSITION_RESIDUAL_SAME_SOURCE_LAW",
                    "score_status_3760": "CONDITIONAL_ZERO_OR_EM_WEP_RESIDUAL_BOUND_READY",
                    "prediction_or_bound_formula_3760": "|Delta_AB ln kappa_eff| + |Delta_AB ln Xi| + |Delta_AB ln Z_frame| + |Delta_AB exchange| + eta_EM_AB <= 2.8e-15; eta_EM_AB=0 if EM stress is same-source",
                    "conditional_score_ready": True,
                    "notes": "WEP row now has explicit EM/binding stress channel rather than hidden composition leakage",
                }
            )
        if source_row["residual_id"] == "KRV3755_6_gamma":
            patched.update(
                {
                    "prediction_status_3760": "EM_TOTAL_STRESS_PPN_PROJECTION_REQUIRED",
                    "score_status_3760": "PPN_SOURCE_INTERFACE_READY_NUMERIC_PROJECTION_MISSING",
                    "prediction_or_bound_formula_3760": "delta_gamma_EM <= |epsilon_EM_metric| + |Pi_PPN q_EM_exchange| + |Delta_EM_source_frame|; bound 2.3e-05",
                    "conditional_score_ready": False,
                    "notes": "gamma row now has explicit EM same-source interface, but no PPN projection value yet",
                }
            )
        if source_row["residual_id"] == "KRV3755_7_beta":
            patched.update(
                {
                    "prediction_status_3760": "EM_NONLINEAR_BINDING_PPN_PROJECTION_REQUIRED",
                    "score_status_3760": "PPN_BETA_EM_INTERFACE_READY_NUMERIC_PROJECTION_MISSING",
                    "prediction_or_bound_formula_3760": "delta_beta_EM <= |epsilon_EM_nonlinear| + |Delta_EM_binding_second_order| + |Pi_beta q_EM_exchange|; bound 7.8e-05",
                    "conditional_score_ready": False,
                    "notes": "beta row now has explicit EM binding/source interface, but no numeric second-order projection yet",
                }
            )
        rows.append(patched)
    return rows


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    all_sources = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    gates = [
        ("CG3760_0_sources", "all 3760 source paths exist", all_sources, "path hygiene"),
        ("CG3760_1_standard_EM_stress", "standard Maxwell Hilbert stress identity emitted", True, "conditional on local Maxwell action"),
        ("CG3760_2_same_action_Ward", "same-action Maxwell/matter Ward cancellation emitted", True, "Lorentz force internal to total stress"),
        ("CG3760_3_MTS_EM_descent_parent_signed", "emergent MTS EM descends to same Hilbert source", False, "parent descent not signed"),
        ("CG3760_4_EM_WEP_zero_claim", "EM contribution to WEP zero claimed", False, "same-source EM not parent-signed"),
        ("CG3760_5_EM_numeric_residuals", "EM residual components numeric", False, "component values missing"),
        ("CG3760_6_PPN_gamma_beta_claim", "PPN gamma/beta claim allowed", False, "metric projection still missing"),
        ("CG3760_7_local_gr_claim", "local GR claim allowed", False, "local GR route still has open parent signatures"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "details": details,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, details in gates
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "DEC3760_0",
            "EM can be compatible with WEP/local GR if it is part of the same Hilbert/coframe source action; it is dangerous only as a side-channel source coupling.",
            "treat same-source EM descent as a parent-action gate, not a phenomenological patch",
        ),
        (
            "DEC3760_1",
            "The Lorentz force should not be counted as external WEP violation once matter and EM field stress are combined; only residual parent exchange beyond the cancellation is live.",
            "route q_EM_exchange into residual rows if same-action descent fails",
        ),
        (
            "DEC3760_2",
            "The next meaningful local-GR step is not another coupling list; it is the weak-field PPN projection of total stress into gamma/beta with EM included.",
            "move to PPN source projection after this checkpoint",
        ),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "action": action,
            "claim_allowed": False,
        }
        for decision_id, decision, action in entries
    ]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3760_0",
            "target_doc": "3761-Y5-R2FR-PPN-total-stress-projection-gamma-beta-or-residual.md",
            "target_script": "scripts/Y5_R2FR_3761_PPN_total_stress_projection_gamma_beta_or_residual.py",
            "objective": "derive the weak-field PPN gamma/beta projection from the same total Hilbert/coframe source stress, including EM stress, or emit explicit gamma/beta residual components",
            "reason": "3760 makes EM stress an explicit same-source gate; the next local-GR step is the metric projection into PPN observables",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "MAXWELL_EM_SAME_SOURCE_THEOREM_OR_RESIDUAL_INTERFACE_DERIVED",
            "summary": "3760 derives the conditional Maxwell/EM Hilbert-stress same-source route and emits EM residual budgets for WEP, Gdot, gamma, and beta if same-source descent is not parent-signed.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3760 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3760 csvs parse", all(read_csv(path) for path in generated_csvs)),
        (
            "em_stress_identity",
            "Maxwell Hilbert stress identity emitted",
            any(row["theorem_id"] == "EMT3760_1_hilbert_EM_stress" for row in grouped["em_theorem"]),
        ),
        (
            "ward_cancellation",
            "same-action Ward cancellation emitted",
            any(row["theorem_id"] == "EMT3760_2_Maxwell_Ward_exchange" and row["status"] == "EXACT_SAME_ACTION_WARD_CANCELLATION" for row in grouped["em_theorem"]),
        ),
        (
            "em_wep_residual",
            "EM WEP residual budget emitted",
            any(row["residual_id"] == "EMR3760_0_WEP_EM_binding" and str(row["bound_value"]) == "2.8e-15" for row in grouped["em_residual"]),
        ),
        (
            "em_ppn_interface",
            "EM to PPN interface emitted",
            any(row["interface_id"] == "EP3760_3_next_metric_projection" for row in grouped["ppn_interface"]),
        ),
        (
            "runner_patch_nonclaim",
            "patched runner remains nonclaim",
            all(str(row["claim_allowed"]) == "False" or row["claim_allowed"] is False for row in grouped["runner_patch"]),
        ),
        (
            "ppn_claim_blocked",
            "PPN claim remains false",
            any(row["gate_id"] == "CG3760_6_PPN_gamma_beta_claim" and row["passed"] is False for row in grouped["claim_gates"]),
        ),
        (
            "local_gr_not_claimed",
            "local GR remains unclaimed",
            any(row["gate_id"] == "CG3760_7_local_gr_claim" and row["passed"] is False for row in grouped["claim_gates"]),
        ),
        (
            "next_target",
            "3761 target emitted",
            grouped["next_target"][0]["target_doc"] == "3761-Y5-R2FR-PPN-total-stress-projection-gamma-beta-or-residual.md",
        ),
        (
            "no_formalization_leak",
            "no 3760 files written to formalization-workbench",
            not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3760*")),
        ),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "" if result else "check failed",
        }
        for validation_id, description, result in checks
    ]


def render_doc(grouped: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# 3760 — Maxwell/EM Stress Same-Source Current Or Residual",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Derivation",
        "",
        "The EM gate is not whether electromagnetism exists as a familiar sector; it is whether EM energy, binding energy, and Lorentz exchange are represented inside the same Hilbert/coframe source current used by the local gravitational coupling.",
        "",
        "For a local Maxwell action `S_EM=-(1/4) int sqrt(-g_eff) Z_EM F_ab F^ab`, variation with respect to the same `g_eff` gives `T_EM`. On shell, `div T_EM = -FJ` and charged matter carries `+FJ`, so the Lorentz force cancels inside total stress conservation.",
        "",
        "Therefore EM is WEP/local-GR safe if MTS parent descent gives the same total source tensor. If not, the live residual is an EM composition/source channel feeding WEP, Gdot, gamma, and beta.",
        "",
        "## Maxwell/EM Same-Source Clauses",
    ]
    for row in grouped["em_theorem"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']}")
    lines.extend(["", "## EM Residual Budgets"])
    for row in grouped["em_residual"]:
        lines.append(
            f"- `{row['residual_id']}` `{row['score_status']}`: `{row['symbol']}` in `{row['arena']}` formula `{row['residual_formula']}` bound `{row['bound_value']} {row['units']}`"
        )
    lines.extend(["", "## EM To PPN Interface"])
    for row in grouped["ppn_interface"]:
        lines.append(f"- `{row['interface_id']}` `{row['status']}`: {row['statement']}")
    lines.extend(["", "## Runner Patch"])
    for row in grouped["runner_patch"]:
        lines.append(f"- `{row['patched_runner_row_id']}` `{row['score_status_3760']}`: {row['prediction_or_bound_formula_3760']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}`: {row['gate']} — {row['details']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decision_rows"]:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} Action: {row['action']}.")
    lines.extend(["", "## Next Target"])
    for row in grouped["next_target"]:
        lines.append(f"- `{row['target_doc']}`: {row['objective']}")
    lines.extend(["", "## Validation"])
    for row in grouped["validation"]:
        lines.append(f"- `{row['validation_id']}` `{row['result']}`: {row['description']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    grouped: dict[str, list[dict[str, object]]] = {
        "sources": source_register(timestamp),
        "em_theorem": em_theorem_rows(timestamp),
        "em_residual": em_residual_rows(timestamp),
        "ppn_interface": ppn_interface_rows(timestamp),
        "runner_patch": runner_patch_rows(timestamp),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["em_theorem"], grouped["em_theorem"])
    write_csv(OUTPUTS["em_residual"], grouped["em_residual"])
    write_csv(OUTPUTS["ppn_interface"], grouped["ppn_interface"])
    write_csv(OUTPUTS["runner_patch"], grouped["runner_patch"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decision_rows"], grouped["decision_rows"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3760 validation failed: {failures}")
    print("wrote 3760 checkpoint: Maxwell/EM same-source theorem or residual interface derived")


if __name__ == "__main__":
    main()

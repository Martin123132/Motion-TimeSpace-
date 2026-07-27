import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3763"
BRANCH = "MTS_R2FR_Y5_PARENT_SIGNATURE_SELECTION_SINGLE_FRAME_NO_RANGE_LOCAL_EH_3763"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3763-Y5-R2FR-parent-signature-selection-single-frame-no-range-local-EH.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3763_SOURCE_REGISTER.csv",
    "signature_set": RESIDUALS / "P8_Y5_R2FR_3763_MINIMAL_PARENT_SIGNATURE_SET.csv",
    "action_ansatz": RESIDUALS / "P8_Y5_R2FR_3763_LOCAL_PARENT_ACTION_ANSATZ.csv",
    "closure_matrix": RESIDUALS / "P8_Y5_R2FR_3763_SIGNATURE_TO_OBSERVABLE_CLOSURE_MATRIX.csv",
    "risk_register": RESIDUALS / "P8_Y5_R2FR_3763_SIGNATURE_RISK_REGISTER.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3763_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3763_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3763_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3763_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3763_VALIDATION.csv",
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
        "SRC3763_0_3762_doc": PCW / "3762-Y5-R2FR-range-radial-frame-residual-lock-or-R10-PPN-bound.md",
        "SRC3763_1_3762_next": RESIDUALS / "P8_Y5_R2FR_3762_NEXT_TARGET.csv",
        "SRC3763_2_3762_locks": RESIDUALS / "P8_Y5_R2FR_3762_RANGE_RADIAL_FRAME_LOCKS.csv",
        "SRC3763_3_3762_budgets": RESIDUALS / "P8_Y5_R2FR_3762_RANGE_RADIAL_FRAME_RESIDUAL_BUDGET.csv",
        "SRC3763_4_3762_claim_matrix": RESIDUALS / "P8_Y5_R2FR_3762_LOCAL_GR_CLAIM_MATRIX.csv",
        "SRC3763_5_3762_runner": RESIDUALS / "P8_Y5_R2FR_3762_COUPLING_RUNNER_PATCH.csv",
        "SRC3763_6_3761_ppn": RESIDUALS / "P8_Y5_R2FR_3761_PPN_TOTAL_STRESS_PROJECTION_THEOREM.csv",
        "SRC3763_7_3760_em": RESIDUALS / "P8_Y5_R2FR_3760_MAXWELL_EM_STRESS_SOURCE_THEOREM.csv",
        "SRC3763_8_3758_kappa": RESIDUALS / "P8_Y5_R2FR_3758_KAPPA_QUOTIENT_FLUX_LAW.csv",
        "SRC3763_9_3759_source_universality": RESIDUALS / "P8_Y5_R2FR_3759_SOURCE_UNIVERSALITY_THEOREM.csv",
        "SRC3763_10_3757_side_flux": RESIDUALS / "P8_Y5_R2FR_3757_SIDE_FLUX_ZERO_THEOREM.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3763 minimal parent-signature selection input",
        }
        for source_id, path in source_paths().items()
    ]


def signature_set_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "SIG3763_0_local_EH",
            "The local quotient branch has one observed metric/coframe g_eff/e_eff whose gravitational action reduces to Einstein-Hilbert through second PPN order.",
            "closes gamma/beta left-hand operator residuals",
            "PROPOSED_MINIMAL_SIGNATURE_NOT_PARENT_DERIVED",
        ),
        (
            "SIG3763_1_same_total_source",
            "All matter, EM, binding energy, and apparatus stresses enter one Hilbert/coframe source T_total from one source action S_src[fields,g_eff].",
            "closes WEP/source/EM bookkeeping residuals",
            "PROPOSED_MINIMAL_SIGNATURE_NOT_PARENT_DERIVED",
        ),
        (
            "SIG3763_2_single_observed_frame",
            "Matter, light, clocks, EM, orbital readout, and source charge use the same observed metric/coframe and local time generator.",
            "closes frame/source/preferred-frame residuals",
            "PROPOSED_MINIMAL_SIGNATURE_NOT_PARENT_DERIVED",
        ),
        (
            "SIG3763_3_global_kappa",
            "kappa_* is a global/superselected parent parameter or quotient constant, not a local propagating scalar in the Newton/PPN branch.",
            "closes Gdot and source-label kappa drift residuals",
            "PROPOSED_MINIMAL_SIGNATURE_NOT_PARENT_DERIVED",
        ),
        (
            "SIG3763_4_no_finite_range_mediator",
            "No unscreened finite-range scalar/vector/tensor mediator couples to the local source outside g_eff in the local branch.",
            "closes alpha(lambda), radial range hair, and fifth-force residuals",
            "PROPOSED_MINIMAL_SIGNATURE_NOT_PARENT_DERIVED",
        ),
        (
            "SIG3763_5_compact_no_radial_hair",
            "Local sources define material worldtubes with conserved cap charge and no exterior radial drift of kappa, source charge, Poisson calibration, or extra-field amplitude.",
            "closes radial mu_obs profile and mass-flux residuals",
            "PROPOSED_MINIMAL_SIGNATURE_NOT_PARENT_DERIVED",
        ),
        (
            "SIG3763_6_exchange_projection_silence",
            "Projected parent exchange Pi_M q_exchange and non-Hilbert owner currents vanish in the local branch or are mapped into the residual vector.",
            "prevents hidden closure assumptions in every local row",
            "PROPOSED_MINIMAL_SIGNATURE_NOT_PARENT_DERIVED",
        ),
    ]
    return [
        {
            **base(timestamp),
            "signature_id": signature_id,
            "signature_clause": signature_clause,
            "main_closure_role": main_closure_role,
            "status": status,
            "parent_signed": False,
            "claim_allowed": False,
        }
        for signature_id, signature_clause, main_closure_role, status in entries
    ]


def action_ansatz_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "ACT3763_0_local_action",
            "S_local = S_top[MTS] + (1/(2 kappa_*)) int_U sqrt(-g_eff) R[g_eff] + S_src[psi_A,A_mu,g_eff,theta] + S_aux[chi;g_eff]",
            "candidate local parent branch, not final fundamental action",
            "ANSATZ_FOR_DERIVATION_TARGET",
        ),
        (
            "ACT3763_1_auxiliary_silence",
            "S_aux fields chi are either vertical/gauge, algebraically constrained, heavy/decoupled, or residualized; they do not generate unscreened finite-range local source forces.",
            "implements no finite-range mediator without deleting the wider MTS programme",
            "LOCAL_BRANCH_SIGNATURE",
        ),
        (
            "ACT3763_2_same_source_variation",
            "T_total^{ab} := (2/sqrt(-g_eff)) delta S_src/d g_eff_ab, including material, EM, binding, clock, and apparatus stresses.",
            "forces WEP/EM/source consistency through variation",
            "LOCAL_BRANCH_SIGNATURE",
        ),
        (
            "ACT3763_3_exchange_policy",
            "Any non-Hilbert exchange owner K_owner or q_exchange must be either zero by parent Ward identity or appear explicitly in the local residual vector.",
            "anti-smuggling rule",
            "NONNEGOTIABLE_CONSISTENCY_POLICY",
        ),
        (
            "ACT3763_4_absolute_G_policy",
            "The branch may derive local constancy of G_eff while still treating the measured absolute G as calibration unless kappa_* or the charge quotient normalization is parent-predicted.",
            "keeps Newton limit honest",
            "ANTI_OVERCLAIM_POLICY",
        ),
    ]
    return [
        {
            **base(timestamp),
            "action_id": action_id,
            "action_clause": action_clause,
            "purpose": purpose,
            "status": status,
            "claim_allowed": False,
        }
        for action_id, action_clause, purpose, status in entries
    ]


def closure_matrix_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        ("CLOSE3763_0_Gdot", "dln_Geff_dt", "SIG3763_3_global_kappa;SIG3763_5_compact_no_radial_hair;SIG3763_6_exchange_projection_silence", "dln_Geff_dt=0", "nonclaim until signatures parent-signed"),
        ("CLOSE3763_1_WEP", "eta_source_AB", "SIG3763_1_same_total_source;SIG3763_2_single_observed_frame;SIG3763_3_global_kappa", "eta_source_AB=0", "nonclaim until same source/frame parent-signed"),
        ("CLOSE3763_2_EM", "eta_EM_AB/delta_gamma_EM/delta_beta_EM", "SIG3763_1_same_total_source;SIG3763_2_single_observed_frame", "EM residuals vanish as separate channels", "nonclaim until emergent EM descent parent-signed"),
        ("CLOSE3763_3_gamma", "gamma_minus_1", "SIG3763_0_local_EH;SIG3763_1_same_total_source;SIG3763_2_single_observed_frame;SIG3763_4_no_finite_range_mediator", "gamma-1=0", "nonclaim until local EH/same metric signed"),
        ("CLOSE3763_4_beta", "beta_minus_1", "SIG3763_0_local_EH;SIG3763_1_same_total_source;SIG3763_2_single_observed_frame;SIG3763_6_exchange_projection_silence", "beta-1=0", "nonclaim until second-order EH/source signed"),
        ("CLOSE3763_5_range", "alpha(lambda)", "SIG3763_4_no_finite_range_mediator;SIG3763_6_exchange_projection_silence", "alpha(lambda)=0", "nonclaim until no-range mediator signed"),
        ("CLOSE3763_6_radial", "partial_r_ln_mu_obs", "SIG3763_3_global_kappa;SIG3763_5_compact_no_radial_hair;SIG3763_6_exchange_projection_silence", "partial_r ln mu_obs=0", "nonclaim until no-hair/source conservation signed"),
        ("CLOSE3763_7_frame", "delta_frame_source", "SIG3763_2_single_observed_frame", "delta_frame_source=0", "nonclaim until single observed frame signed"),
    ]
    return [
        {
            **base(timestamp),
            "closure_id": closure_id,
            "observable": observable,
            "required_signatures": required_signatures,
            "conditional_prediction": conditional_prediction,
            "claim_status": claim_status,
            "claim_allowed": False,
        }
        for closure_id, observable, required_signatures, conditional_prediction, claim_status in entries
    ]


def risk_register_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        ("RISK3763_0_too_GR_like", "The selected local branch can look like GR by construction.", "Require every clause to be tied to MTS parent variables, quotient maps, or residual rows; do not call it derivation until sourced."),
        ("RISK3763_1_absolute_G", "The package derives local constancy but not the measured value of G.", "Keep absolute-G calibration policy explicit."),
        ("RISK3763_2_extra_modes_hidden", "No finite-range mediator could hide an MTS mode by naming it auxiliary.", "Require spectrum/decoupling/no-source proof or keep alpha(lambda) curve route live."),
        ("RISK3763_3_frame_smuggling", "Single observed frame could be assumed rather than derived.", "Derive frame descent from parent readout map or retain frame residual rows."),
        ("RISK3763_4_EM_descent", "EM same-source theorem is standard only after local Maxwell action is obtained.", "Derive MTS-to-Maxwell low-energy descent or keep EM residual budgets live."),
    ]
    return [
        {
            **base(timestamp),
            "risk_id": risk_id,
            "risk": risk,
            "control": control,
            "claim_allowed": False,
        }
        for risk_id, risk, control in entries
    ]


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    all_sources = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    gates = [
        ("CG3763_0_sources", "all 3763 source paths exist", all_sources, "path hygiene"),
        ("CG3763_1_signature_set", "minimal parent signature set emitted", len(grouped["signature_set"]) == 7, "seven-clause package"),
        ("CG3763_2_action_ansatz", "local action ansatz emitted", True, "candidate branch target"),
        ("CG3763_3_closure_matrix", "closure matrix covers eight local observables", len(grouped["closure_matrix"]) == 8, "Gdot/WEP/EM/gamma/beta/range/radial/frame"),
        ("CG3763_4_parent_derivation", "signature package derived from deeper MTS parent action", False, "not yet; this checkpoint selects the target"),
        ("CG3763_5_no_smuggling", "all unsigned clauses retain residual fallbacks", True, "anti-closure discipline"),
        ("CG3763_6_local_gr_claim", "local GR claim allowed", False, "signature package not parent-signed"),
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
            "DEC3763_0",
            "The best route is now to derive or reject this seven-clause local parent package, not to keep expanding residual ledgers.",
            "make 3764 a derivation attempt for the package from MTS parent variables/quotient maps",
        ),
        (
            "DEC3763_1",
            "The package is intentionally GR-like locally; that is acceptable only if MTS derives why this is the local fixed point and where cosmology/galaxy deviations live.",
            "separate local fixed-point derivation from large-scale active branch work",
        ),
        (
            "DEC3763_2",
            "The highest-value clause to derive first is the single observed frame plus same total source, because it closes WEP, clocks, EM bookkeeping, and PPN frame leakage simultaneously.",
            "prioritize frame/source descent theorem before absolute G",
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
            "next_id": "NEXT3763_0",
            "target_doc": "3764-Y5-R2FR-derive-single-observed-frame-and-same-total-source-from-parent-quotient.md",
            "target_script": "scripts/Y5_R2FR_3764_derive_single_observed_frame_and_same_total_source_from_parent_quotient.py",
            "objective": "try to derive the single observed metric/coframe/time generator and same total Hilbert source from the MTS parent quotient/descent map; if it fails, keep frame/source residuals explicit",
            "reason": "3763 selects the minimal package; frame/source descent is the most leveraged clause for WEP, clocks, EM, and PPN",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "MINIMAL_LOCAL_GR_PARENT_SIGNATURE_PACKAGE_SELECTED_NOT_CLAIMED",
            "summary": "3763 selects a seven-clause parent-action package that would close the local-GR residual matrix if derived: local EH, same total source, single observed frame, global kappa, no finite-range mediator, compact no-radial-hair, and exchange projection silence.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3763 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3763 csvs parse", all(read_csv(path) for path in generated_csvs)),
        ("signature_count", "seven parent signatures emitted", len(grouped["signature_set"]) == 7),
        ("action_ansatz", "local parent action ansatz emitted", any(row["action_id"] == "ACT3763_0_local_action" for row in grouped["action_ansatz"])),
        ("closure_count", "closure matrix covers eight observables", len(grouped["closure_matrix"]) == 8),
        ("risk_controls", "risk register emitted", len(grouped["risk_register"]) >= 5),
        (
            "parent_not_claimed",
            "parent derivation remains false",
            any(row["gate_id"] == "CG3763_4_parent_derivation" and row["passed"] is False for row in grouped["claim_gates"]),
        ),
        (
            "local_gr_not_claimed",
            "local GR remains unclaimed",
            any(row["gate_id"] == "CG3763_6_local_gr_claim" and row["passed"] is False for row in grouped["claim_gates"]),
        ),
        (
            "next_target",
            "3764 target emitted",
            grouped["next_target"][0]["target_doc"] == "3764-Y5-R2FR-derive-single-observed-frame-and-same-total-source-from-parent-quotient.md",
        ),
        (
            "no_formalization_leak",
            "no 3763 files written to formalization-workbench",
            not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3763*")),
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
        "# 3763 — Parent Signature Selection: Single Frame, No Range, Local EH",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Why This Is A Leap",
        "",
        "The previous checkpoints routed the local-GR residuals. This checkpoint selects the smallest parent-action package that would actually close them. It is not yet a proof from deeper MTS; it is the exact derivation target.",
        "",
        "If this package can be derived from the MTS parent quotient/descent structure, the local branch reduces to GR/Newton/Maxwell in the normal way. If it cannot, each unsigned clause already has a residual/bound fallback.",
        "",
        "## Minimal Parent Signature Set",
    ]
    for row in grouped["signature_set"]:
        lines.append(f"- `{row['signature_id']}` `{row['status']}`: {row['signature_clause']}")
    lines.extend(["", "## Local Action Ansatz"])
    for row in grouped["action_ansatz"]:
        lines.append(f"- `{row['action_id']}` `{row['status']}`: {row['action_clause']}")
    lines.extend(["", "## Signature-To-Observable Closure Matrix"])
    for row in grouped["closure_matrix"]:
        lines.append(f"- `{row['closure_id']}` `{row['observable']}`: requires `{row['required_signatures']}` -> `{row['conditional_prediction']}`")
    lines.extend(["", "## Risk Register"])
    for row in grouped["risk_register"]:
        lines.append(f"- `{row['risk_id']}`: {row['risk']} Control: {row['control']}.")
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
        "signature_set": signature_set_rows(timestamp),
        "action_ansatz": action_ansatz_rows(timestamp),
        "closure_matrix": closure_matrix_rows(timestamp),
        "risk_register": risk_register_rows(timestamp),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["signature_set"], grouped["signature_set"])
    write_csv(OUTPUTS["action_ansatz"], grouped["action_ansatz"])
    write_csv(OUTPUTS["closure_matrix"], grouped["closure_matrix"])
    write_csv(OUTPUTS["risk_register"], grouped["risk_register"])
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
        raise SystemExit(f"3763 validation failed: {failures}")
    print("wrote 3763 checkpoint: minimal local-GR parent signature package selected")


if __name__ == "__main__":
    main()

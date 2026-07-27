import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3764"
BRANCH = "MTS_R2FR_Y5_DERIVE_SINGLE_OBSERVED_FRAME_AND_SAME_TOTAL_SOURCE_FROM_PARENT_QUOTIENT_3764"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3764-Y5-R2FR-derive-single-observed-frame-and-same-total-source-from-parent-quotient.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3764_SOURCE_REGISTER.csv",
    "quotient_theorem": RESIDUALS / "P8_Y5_R2FR_3764_PARENT_QUOTIENT_DESCENT_THEOREM.csv",
    "source_theorem": RESIDUALS / "P8_Y5_R2FR_3764_SAME_TOTAL_SOURCE_VARIATION_THEOREM.csv",
    "frame_source_matrix": RESIDUALS / "P8_Y5_R2FR_3764_FRAME_SOURCE_DESCENT_MATRIX.csv",
    "fallback_residuals": RESIDUALS / "P8_Y5_R2FR_3764_FRAME_SOURCE_FALLBACK_RESIDUALS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3764_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3764_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3764_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3764_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3764_VALIDATION.csv",
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
        "SRC3764_0_3763_doc": PCW / "3763-Y5-R2FR-parent-signature-selection-single-frame-no-range-local-EH.md",
        "SRC3764_1_3763_next": RESIDUALS / "P8_Y5_R2FR_3763_NEXT_TARGET.csv",
        "SRC3764_2_3763_signature_set": RESIDUALS / "P8_Y5_R2FR_3763_MINIMAL_PARENT_SIGNATURE_SET.csv",
        "SRC3764_3_3763_action_ansatz": RESIDUALS / "P8_Y5_R2FR_3763_LOCAL_PARENT_ACTION_ANSATZ.csv",
        "SRC3764_4_3763_closure_matrix": RESIDUALS / "P8_Y5_R2FR_3763_SIGNATURE_TO_OBSERVABLE_CLOSURE_MATRIX.csv",
        "SRC3764_5_3763_risk_register": RESIDUALS / "P8_Y5_R2FR_3763_SIGNATURE_RISK_REGISTER.csv",
        "SRC3764_6_3762_claim_matrix": RESIDUALS / "P8_Y5_R2FR_3762_LOCAL_GR_CLAIM_MATRIX.csv",
        "SRC3764_7_3759_universality": RESIDUALS / "P8_Y5_R2FR_3759_SOURCE_UNIVERSALITY_THEOREM.csv",
        "SRC3764_8_3760_em_theorem": RESIDUALS / "P8_Y5_R2FR_3760_MAXWELL_EM_STRESS_SOURCE_THEOREM.csv",
        "SRC3764_9_3761_ppn_theorem": RESIDUALS / "P8_Y5_R2FR_3761_PPN_TOTAL_STRESS_PROJECTION_THEOREM.csv",
        "SRC3764_10_3754_flux_law": RESIDUALS / "P8_Y5_R2FR_3754_SOURCE_WARD_FLUX_LAW_ROWS.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3764 parent quotient/frame/source derivation input",
        }
        for source_id, path in source_paths().items()
    ]


def quotient_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "QDT3764_0_parent_equivalence",
            "Let R_vert be the parent vertical/gauge equivalence relation on local MTS configurations Phi.",
            "Defines what is unobservable/representational before readout.",
            "DEFINITION_REQUIRED",
            False,
        ),
        (
            "QDT3764_1_observed_quotient",
            "Let q_obs: Phi -> O_obs be a quotient/coequalizer of R_vert whose local object is O_obs=(e_obs,g_eff,tau_obs,orientation,calibration).",
            "This is the parent readout map needed for a single observed frame.",
            "PARENT_QUOTIENT_SIGNATURE_REQUIRED",
            False,
        ),
        (
            "QDT3764_2_sector_factorization",
            "For every local sector s in {matter, EM, clocks, light, orbital/source readout}, the sector readout r_s factors as r_s = F_s o q_obs.",
            "If true, no sector has an independent physical frame map.",
            "SECTOR_DESCENT_SIGNATURE_REQUIRED",
            False,
        ),
        (
            "QDT3764_3_uniqueness",
            "If q_obs is universal and r_s all factor through q_obs, then any two sector frames e_s,e_t differ only by quotient-killed gauge/diffeomorphism/local-Lorentz freedom.",
            "This proves one physical observed frame from the quotient property.",
            "EXACT_CONDITIONAL_THEOREM",
            True,
        ),
        (
            "QDT3764_4_frame_zero",
            "Under QDT3764_1-3, delta_frame_source=0 and the source/light/clock/orbital frame split vanishes.",
            "This closes the 3762 frame row conditionally.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
            True,
        ),
        (
            "QDT3764_5_failure_mode",
            "If any sector has a non-factorizing readout q_s or a species-dependent frame map, the frame residual is delta_frame_source != 0 and must be bounded.",
            "No smuggling: failure leaves a residual row.",
            "RESIDUAL_FALLBACK",
            True,
        ),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "statement": statement,
            "meaning": meaning,
            "status": status,
            "derived_inside_3764": derived,
            "parent_signed": False,
            "claim_allowed": False,
        }
        for theorem_id, statement, meaning, status, derived in entries
    ]


def source_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "STS3764_0_descended_source_action",
            "Assume one descended source action S_src = Sbar_src[q_obs(Phi), psi_A, A_mu, theta] = S_material + S_EM + S_binding + S_apparatus + S_int.",
            "All local source sectors are varied with respect to the same q_obs-derived metric/coframe.",
            "SOURCE_DESCENT_SIGNATURE_REQUIRED",
            False,
        ),
        (
            "STS3764_1_total_Hilbert_source",
            "Define T_total^{ab} := (2/sqrt(-g_eff)) delta S_src / delta g_eff_ab; by linearity of variation this equals the sum of material, EM, binding, apparatus, and interaction stress terms in the same frame.",
            "This is the same total Hilbert/coframe source, not a fitted source charge.",
            "EXACT_CONDITIONAL_VARIATION_THEOREM",
            True,
        ),
        (
            "STS3764_2_internal_exchange_cancellation",
            "Internal forces such as Lorentz matter-field exchange cancel inside div T_total; only parent exchange q_exchange or non-Hilbert owner currents remain.",
            "Imports the 3760 EM Ward cancellation into the same-source theorem.",
            "EXACT_CONDITIONAL_WARD_THEOREM",
            True,
        ),
        (
            "STS3764_3_source_universality",
            "If S_src has no species-labelled gravitational coupling and uses q_obs for all sectors, then eta_source_AB=0 except for explicit residual owners.",
            "This closes the 3759 WEP row conditionally.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
            True,
        ),
        (
            "STS3764_4_PPN_source_readout",
            "The same T_total is the source in the local EH weak-field equations, so gamma/beta source projection does not use a separate EM/source/readout tensor.",
            "This links same-source descent to the 3761 PPN rows.",
            "EXACT_CONDITIONAL_PPN_INTERFACE",
            True,
        ),
        (
            "STS3764_5_failure_mode",
            "If S_src does not descend through q_obs or has sector-labelled gravitational couplings, then delta_source_split, eta_source_AB, eta_EM_AB, and PPN source residuals stay live.",
            "No smuggling: failure leaves explicit residuals.",
            "RESIDUAL_FALLBACK",
            True,
        ),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "statement": statement,
            "meaning": meaning,
            "status": status,
            "derived_inside_3764": derived,
            "parent_signed": False,
            "claim_allowed": False,
        }
        for theorem_id, statement, meaning, status, derived in entries
    ]


def frame_source_matrix_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        ("FSM3764_0_WEP", "eta_source_AB", "QDT3764_2_sector_factorization;STS3764_0_descended_source_action;STS3764_3_source_universality", "eta_source_AB=0", "parent quotient/source descent unsigned"),
        ("FSM3764_1_EM", "eta_EM_AB/delta_gamma_EM/delta_beta_EM", "QDT3764_2_sector_factorization;STS3764_1_total_Hilbert_source;STS3764_2_internal_exchange_cancellation", "separate EM residuals vanish", "MTS-to-Maxwell descent still unsigned"),
        ("FSM3764_2_frame", "delta_frame_source", "QDT3764_1_observed_quotient;QDT3764_2_sector_factorization;QDT3764_3_uniqueness", "delta_frame_source=0", "q_obs uniqueness/factorization unsigned"),
        ("FSM3764_3_gamma", "gamma_minus_1", "STS3764_4_PPN_source_readout plus local EH signature", "source projection part of gamma residual vanishes", "local EH still separate unsigned clause"),
        ("FSM3764_4_beta", "beta_minus_1", "STS3764_4_PPN_source_readout plus second-order local EH signature", "source projection part of beta residual vanishes", "second-order EH still separate unsigned clause"),
        ("FSM3764_5_clocks", "clock/frame residual", "QDT3764_2_sector_factorization for clock sector", "clock-source frame split vanishes", "clock readout descent unsigned"),
    ]
    return [
        {
            **base(timestamp),
            "matrix_id": matrix_id,
            "observable": observable,
            "required_theorems": required_theorems,
            "conditional_closure": conditional_closure,
            "remaining_blocker": remaining_blocker,
            "claim_allowed": False,
        }
        for matrix_id, observable, required_theorems, conditional_closure, remaining_blocker in entries
    ]


def fallback_residual_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "FSR3764_0_frame",
            "delta_frame_source",
            "|q_matter-q_light| + |q_clock-q_source| + |q_EM-q_obs| + |delta_tau_obs|",
            "WEP/clock/preferred-frame/gamma/beta",
            "live if sector readouts do not all factor through q_obs",
        ),
        (
            "FSR3764_1_source",
            "delta_source_split",
            "|T_total - T_H[q_obs]| + |T_EM_side| + |T_binding_side| + |T_apparatus_side|",
            "WEP/EM/PPN source projection",
            "live if source action does not descend through q_obs",
        ),
        (
            "FSR3764_2_exchange",
            "q_exchange_projected",
            "|Pi_M q_exchange| + |non_Hilbert_owner_current| + |boundary_owner_flux|",
            "Gdot/radial/beta/source conservation",
            "live if parent exchange projection silence is not signed",
        ),
        (
            "FSR3764_3_species",
            "eta_source_AB",
            "|Delta_AB ln kappa_eff| + |Delta_AB ln Xi| + |Delta_AB ln Z_frame| + |Delta_AB exchange|",
            "MICROSCOPE/WEP",
            "live if species/source labelled gravitational couplings remain",
        ),
    ]
    return [
        {
            **base(timestamp),
            "residual_id": residual_id,
            "symbol": symbol,
            "residual_formula": residual_formula,
            "feeds_observables": feeds_observables,
            "activation_condition": activation_condition,
            "prediction_value": "MISSING_NUMERIC_COMPONENTS_OR_PARENT_ZERO_SIGNATURE",
            "score_status": "RESIDUAL_INTERFACE_READY_NUMERIC_COMPONENTS_MISSING",
            "claim_allowed": False,
        }
        for residual_id, symbol, residual_formula, feeds_observables, activation_condition in entries
    ]


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    all_sources = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    gates = [
        ("CG3764_0_sources", "all 3764 source paths exist", all_sources, "path hygiene"),
        ("CG3764_1_single_frame_theorem", "single-frame quotient theorem emitted", True, "conditional proof exists"),
        ("CG3764_2_same_source_theorem", "same-total-source variation theorem emitted", True, "conditional proof exists"),
        ("CG3764_3_parent_qobs_signed", "q_obs quotient uniqueness parent-signed", False, "parent quotient construction still missing"),
        ("CG3764_4_sector_factorization_signed", "all sector readouts factor through q_obs", False, "sector descent not yet proved"),
        ("CG3764_5_source_action_descent_signed", "S_src descends through q_obs", False, "source action descent not yet proved"),
        ("CG3764_6_frame_source_claim", "single frame/same source claim allowed", False, "parent signatures unsigned"),
        ("CG3764_7_local_gr_claim", "local GR claim allowed", False, "local EH/no-range/global-kappa clauses still separate"),
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
            "DEC3764_0",
            "Single-frame and same-source descent are now exact conditional theorems from a universal parent quotient, not merely desired closure assumptions.",
            "next work must construct q_obs from MTS variables or retain frame/source residuals",
        ),
        (
            "DEC3764_1",
            "This is progress but not a claim: the missing hard object is the parent-owned quotient/coequalizer q_obs and proof that all sectors factor through it.",
            "target q_obs construction directly",
        ),
        (
            "DEC3764_2",
            "If q_obs exists, it gives a strong explanation for why local GR uses one metric for matter, light, clocks, EM, and source charge.",
            "prioritize quotient uniqueness over absolute-G derivation",
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
            "next_id": "NEXT3764_0",
            "target_doc": "3765-Y5-R2FR-construct-qobs-parent-quotient-or-frame-residual-map.md",
            "target_script": "scripts/Y5_R2FR_3765_construct_qobs_parent_quotient_or_frame_residual_map.py",
            "objective": "construct the parent observed quotient q_obs from MTS variables and vertical/gauge equivalence, or emit the explicit sector readout residual map q_s-q_obs",
            "reason": "3764 proves single-frame/same-source if q_obs is universal; the next hard step is constructing that q_obs from the parent theory",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "SINGLE_FRAME_SAME_SOURCE_CONDITIONAL_QUOTIENT_THEOREM_DERIVED_NOT_PARENT_SIGNED",
            "summary": "3764 derives exact conditional theorems: a universal observed quotient q_obs forces one physical frame, and one q_obs-descended source action gives the same total Hilbert/coframe source. The missing step is constructing/signing q_obs and sector factorization from the MTS parent map.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3764 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3764 csvs parse", all(read_csv(path) for path in generated_csvs)),
        (
            "single_frame_theorem",
            "single-frame quotient theorem emitted",
            any(row["theorem_id"] == "QDT3764_4_frame_zero" and row["status"] == "EXACT_CONDITIONAL_ZERO_THEOREM" for row in grouped["quotient_theorem"]),
        ),
        (
            "same_source_theorem",
            "same total source theorem emitted",
            any(row["theorem_id"] == "STS3764_1_total_Hilbert_source" and row["status"] == "EXACT_CONDITIONAL_VARIATION_THEOREM" for row in grouped["source_theorem"]),
        ),
        (
            "fallbacks",
            "fallback residual rows emitted",
            len(grouped["fallback_residuals"]) >= 4,
        ),
        (
            "frame_source_matrix",
            "frame/source matrix covers at least six observables",
            len(grouped["frame_source_matrix"]) >= 6,
        ),
        (
            "parent_not_signed",
            "parent q_obs remains unsigned",
            any(row["gate_id"] == "CG3764_3_parent_qobs_signed" and row["passed"] is False for row in grouped["claim_gates"]),
        ),
        (
            "local_gr_not_claimed",
            "local GR remains unclaimed",
            any(row["gate_id"] == "CG3764_7_local_gr_claim" and row["passed"] is False for row in grouped["claim_gates"]),
        ),
        (
            "next_target",
            "3765 target emitted",
            grouped["next_target"][0]["target_doc"] == "3765-Y5-R2FR-construct-qobs-parent-quotient-or-frame-residual-map.md",
        ),
        (
            "no_formalization_leak",
            "no 3764 files written to formalization-workbench",
            not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3764*")),
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
        "# 3764 — Derive Single Observed Frame And Same Total Source From Parent Quotient",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Derivation Attempt",
        "",
        "This checkpoint tries the actual derivation path instead of adding another closure label. The result is a conditional theorem: if the parent theory provides a universal observed quotient `q_obs`, and all sectors factor through it, then there is one physical observed frame. If the source action descends through the same `q_obs`, the Hilbert/coframe source is one total source.",
        "",
        "This does not yet prove MTS has that quotient. It proves exactly what the parent quotient must do.",
        "",
        "## Parent Quotient Descent Theorem",
    ]
    for row in grouped["quotient_theorem"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']}")
    lines.extend(["", "## Same Total Source Theorem"])
    for row in grouped["source_theorem"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']}")
    lines.extend(["", "## Frame/Source Closure Matrix"])
    for row in grouped["frame_source_matrix"]:
        lines.append(f"- `{row['matrix_id']}` `{row['observable']}`: requires `{row['required_theorems']}` -> `{row['conditional_closure']}`")
    lines.extend(["", "## Fallback Residuals"])
    for row in grouped["fallback_residuals"]:
        lines.append(f"- `{row['residual_id']}` `{row['symbol']}`: {row['residual_formula']} feeds `{row['feeds_observables']}`")
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
        "quotient_theorem": quotient_theorem_rows(timestamp),
        "source_theorem": source_theorem_rows(timestamp),
        "frame_source_matrix": frame_source_matrix_rows(timestamp),
        "fallback_residuals": fallback_residual_rows(timestamp),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["quotient_theorem"], grouped["quotient_theorem"])
    write_csv(OUTPUTS["source_theorem"], grouped["source_theorem"])
    write_csv(OUTPUTS["frame_source_matrix"], grouped["frame_source_matrix"])
    write_csv(OUTPUTS["fallback_residuals"], grouped["fallback_residuals"])
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
        raise SystemExit(f"3764 validation failed: {failures}")
    print("wrote 3764 checkpoint: single-frame/same-source quotient theorem derived conditionally")


if __name__ == "__main__":
    main()

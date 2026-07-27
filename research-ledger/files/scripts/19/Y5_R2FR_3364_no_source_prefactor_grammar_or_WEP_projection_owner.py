from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3364-Y5-R2FR-no-source-prefactor-grammar-or-WEP-projection-owner-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

LOCAL_SOURCES = [
    ("LSRC3364_0_3363_doc", ROOT / "3363-Y5-R2FR-first-source-normalization-bound-row-under-AX1090.md", "3363 handoff"),
    ("LSRC3364_1_3363_next", OUT / "P8_Y5_R2FR_3363_NEXT_TARGET.csv", "3363 next target"),
    ("LSRC3364_2_3363_bound", OUT / "P8_Y5_R2FR_3363_FIRST_SOURCE_NORMALIZATION_BOUND_ROW.csv", "3363 MICROSCOPE source-normalization bound row"),
    ("LSRC3364_3_3363_projection", OUT / "P8_Y5_R2FR_3363_BOUND_TO_MTS_PROJECTION_REQUIREMENTS.csv", "3363 projection requirements"),
    ("LSRC3364_4_3363_gates", OUT / "P8_Y5_R2FR_3363_PROMOTION_GATES.csv", "3363 promotion gates"),
    ("LSRC3364_5_2645_clause", OUT / "P8_Y5_NO_SOURCE_PREFACTOR_2645_PARENT_ACTION_CLAUSE_ATTEMPT.csv", "no-source-prefactor clause attempt"),
    ("LSRC3364_6_2645_proj", OUT / "P8_Y5_NO_SOURCE_PREFACTOR_2645_PROJECTION_REQUIREMENTS.csv", "no-source-prefactor projection requirements"),
    ("LSRC3364_7_2645_gates", OUT / "P8_Y5_NO_SOURCE_PREFACTOR_2645_CLAIM_GATES.csv", "no-source-prefactor gates"),
    ("LSRC3364_8_2642_proof", OUT / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_PROOF_ATTEMPT.csv", "source-current identity proof attempt"),
    ("LSRC3364_9_2642_bound_pack", OUT / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_COMPONENT_BOUND_PACK.csv", "source-current component bound pack"),
    ("LSRC3364_10_2642_gates", OUT / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_CLAIM_GATES.csv", "source-current identity gates"),
    ("LSRC3364_11_2787_wep_basis", OUT / "P8_Y5_R2FR_2787_PARENT_WEP_BASIS_DERIVATION_ATTEMPT.csv", "parent WEP basis derivation attempt"),
    ("LSRC3364_12_2788_readout", OUT / "P8_Y5_R2FR_2788_PHYSICAL_MICROSCOPE_READOUT_FILL_ROWS.csv", "physical MICROSCOPE readout fill rows"),
    ("LSRC3364_13_2982_tau", OUT / "P8_Y5_R2FR_2982_WEP_TAU_PRODUCT_CONVENTION_COMPLETION_AUDIT.csv", "WEP tau/product convention completion audit"),
    ("LSRC3364_14_2986_eps", OUT / "P8_Y5_R2FR_2986_EPSILON_VWEP_BOUND_ROWS_NONCLAIM.csv", "epsilon_VWEP bound rows"),
    ("LSRC3364_15_2656_contract", OUT / "P8_Y5_MICROSCOPE_READOUT_SOURCE_BOUND_2656_SOURCE_RESIDUAL_BOUND_INPUT_CONTRACT.csv", "MICROSCOPE source residual input contract"),
    ("LSRC3364_16_2656_attempt", OUT / "P8_Y5_MICROSCOPE_READOUT_SOURCE_BOUND_2656_SOURCE_WORLDTUBE_RESIDUAL_BOUND_ATTEMPT.csv", "MICROSCOPE source-worldtube residual attempt"),
    ("LSRC3364_17_3357_scope", OUT / "P8_Y5_R2FR_3357_CLAIM_SCOPE_SEPARATION.csv", "AX1090 source-side scope separation"),
    ("LSRC3364_18_3362_y5", OUT / "P8_Y5_R2FR_3362_Y5_RESULT_ROWS.csv", "3362 Y5 split"),
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3364_LOCAL_SOURCE_REGISTER.csv",
    "prefactor_attempt": OUT / "P8_Y5_R2FR_3364_NO_SOURCE_PREFACTOR_THEOREM_ATTEMPT.csv",
    "wep_projection": OUT / "P8_Y5_R2FR_3364_WEP_PROJECTION_OWNER_AUDIT.csv",
    "bound_update": OUT / "P8_Y5_R2FR_3364_MICROSCOPE_BOUND_STATUS_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3364_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3364_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3364_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3364_VALIDATION.csv",
}


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parseable(path: Path) -> bool:
    try:
        if path.suffix.lower() == ".csv":
            read_csv(path)
        else:
            path.read_text(encoding="utf-8")
        return True
    except Exception:
        return False


def table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(compact(row.get(key, ""), 260).replace("|", "\\|") for key in headers) + " |")
    return "\n".join(lines) + "\n"


def local_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_str(path.exists()),
            "parseable": bool_str(path.exists() and parseable(path)),
            "usage": usage,
            "valid_for_claim": "false",
        }
        for source_id, path, usage in LOCAL_SOURCES
    ]


def prefactor_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "NSP3364_0_conditional_zero_theorem",
            "claim_piece": "no source-only species prefactor",
            "statement": "If the parent grammar permits only a single observed matter functor and the gravitational/source functor sees only the total Hilbert source, then source-only species weights are untypeable.",
            "math_form": "S_ord=sum_A S_A[Psi_A,q(Phi),theta_A]; T_total=delta S_ord/delta q; forbidden: sum_A w_A(Z) S_A or sum_A kappa_A T_A",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "why_it_matters": "Delta_w_AB would be theorem-zero rather than merely bounded",
            "gap": "the current parent action has not signed the typed object-language/no-spurion/no-source-prefactor rule",
            "passes_now": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NSP3364_1_pre_action_weight_countermodel",
            "claim_piece": "countermodel survival",
            "statement": "A covariant pre-action weighted matter sector can preserve Ward identities while creating a source-weight residual.",
            "math_form": "S_matter=sum_A w_A S_A[Psi_A,g_obs]; T_source=sum_A w_A T_A",
            "result": "COUNTERMODEL_SURVIVES",
            "why_it_matters": "Bianchi/Ward conservation can hold even when source universality fails",
            "gap": "only a parent grammar theorem can make w_A untypeable; absence from a preferred ansatz is not enough",
            "passes_now": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NSP3364_2_3362_current_lock_limit",
            "claim_piece": "current/Bianchi lock does not prove equality of constants",
            "statement": "3362 can force variable couplings constant, but it does not force kappa_A=kappa_B.",
            "math_form": "nabla(kappa_A T_A)=0 with nabla T_A=0 can allow constant kappa_A for each A",
            "result": "LIMIT_PROVED",
            "why_it_matters": "the WEP/source-composition row remains live even after derivative coupling is locked",
            "gap": "species-blind common source slot is not signed",
            "passes_now": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NSP3364_3_3357_scope_limit",
            "claim_piece": "AX1090 local bulk source cleanup does not erase pre-action weights",
            "statement": "3357 removes fake bulk source aliases conditionally, but does not by itself forbid an upstream source/species weighting in the parent matter action.",
            "math_form": "pointwise Hilbert source cleanup != proof that w_A cannot appear before variation",
            "result": "SCOPE_SEPARATION",
            "why_it_matters": "local bulk source cleanliness is not the same as source-normalization universality",
            "gap": "integrated source and GM calibration remain open in 3357",
            "passes_now": "false",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NSP3364_4_finite_residual_policy",
            "claim_piece": "Delta_w_AB finite residual retention",
            "statement": "Since the no-prefactor theorem is not signed, Delta_w_AB must remain an explicit finite source-normalization residual bounded by 3363.",
            "math_form": "|Delta_w_TiPt| <= 2.8e-15 only after tau_WEP and no-cancellation projection conditions",
            "result": "FINITE_RESIDUAL_RETAINED",
            "why_it_matters": "this prevents hidden source-weight assumptions from being smuggled into local GR",
            "gap": "projection owner still missing",
            "passes_now": "true",
            "valid_for_claim": "false",
        },
    ]


def wep_projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "WEP3364_0_parent_coefficient",
            "needed_object": "C_parent or Delta_w_AB",
            "required_form": "parent-owned coefficient/theorem-zero source-weight residual with units and branch id",
            "current_status": "MISSING_PARENT_COEFFICIENT",
            "what_3364_derives": "only the slot that must be filled",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "WEP3364_1_source_worldtube",
            "needed_object": "Earth/source vector and worldtube weighting",
            "required_form": "R_source_Earth in the same parent response basis and observed frame",
            "current_status": "MISSING_REQUIRED_LIVE_FILE",
            "what_3364_derives": "point-source shortcut is not legal for relative source channels",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "WEP3364_2_material_tensor",
            "needed_object": "TA6V-PtRh10 material response tensor",
            "required_form": "R_material_TA6V_minus_PtRh10_full_tensor in MTS parent basis",
            "current_status": "MISSING_REQUIRED_LIVE_FILE",
            "what_3364_derives": "MICROSCOPE material labels alone are not an MTS parent response basis",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "WEP3364_3_readout_kernel",
            "needed_object": "official MICROSCOPE readout kernel",
            "required_form": "K_CMSM/readout matrix with masks, orbit, axes, timing, units and provenance",
            "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "what_3364_derives": "tau_WEP=1 shortcut remains forbidden",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "WEP3364_4_tau_product",
            "needed_object": "tau_WEP contraction normalization",
            "required_form": "tau_WEP = branch_locked_orbit_average(K_CMSM * R_source * R_material) with sign/units/masks",
            "current_status": "PARTIAL_FORMULA_ONLY",
            "what_3364_derives": "formal projection law exists but cannot be evaluated",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "WEP3364_5_no_cancellation",
            "needed_object": "componentwise absolute envelope",
            "required_form": "|eta_MTS| <= |tau_WEP Delta_w| + |eta_EM| + |eta_scalar| + |eta_frame| + |eta_readout| + ...",
            "current_status": "POLICY_PRESENT_VALUES_MISSING",
            "what_3364_derives": "3363 bound is legal only as a componentwise target",
            "blocks_score": "true",
            "valid_for_claim": "false",
        },
    ]


def bound_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "BUP3364_0_3363_bound_survives",
            "row_id": "Y5SN3363_0_MICROSCOPE_species_source_weight_bound",
            "external_bound_abs": "2.8e-15",
            "units": "dimensionless",
            "status_after_3364": "EXTERNAL_BOUND_ROW_VALID_NONCLAIM",
            "mts_projection_status_after_3364": "STILL_BLOCKED",
            "reason": "no-source-prefactor theorem and tau_WEP projection owner are not derived",
            "valid_external_bound": "true",
            "valid_mts_prediction_row": "false",
            "valid_for_claim": "false",
        },
        {
            "update_id": "BUP3364_1_conditional_zero_route",
            "row_id": "Delta_w_AB_zero_route",
            "external_bound_abs": "0_if_parent_no_prefactor_grammar_signed",
            "units": "dimensionless",
            "status_after_3364": "CONDITIONAL_ZERO_NOT_CURRENT_CORPUS",
            "mts_projection_status_after_3364": "BLOCKED_BY_COUNTERMODEL",
            "reason": "pre-action w_A S_A remains covariant and Ward-compatible unless grammar forbids it",
            "valid_external_bound": "not_applicable",
            "valid_mts_prediction_row": "false",
            "valid_for_claim": "false",
        },
        {
            "update_id": "BUP3364_2_tauWEP_route",
            "row_id": "tau_WEP_projection",
            "external_bound_abs": "formula_only",
            "units": "dimensionless",
            "status_after_3364": "PARTIAL_FORMAL_PROJECTION_ONLY",
            "mts_projection_status_after_3364": "MISSING_LIVE_FILES_AND_PARENT_BASIS",
            "reason": "K_CMSM, R_source, R_material, C_parent and sign/unit/mask files are not live claim-ready files",
            "valid_external_bound": "false",
            "valid_mts_prediction_row": "false",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3364_0_conditional_no_prefactor_theorem",
            "claim": "if parent grammar forbids source-only weights, Delta_w_AB is zero",
            "passed": "true",
            "reason": "conditional theorem is exact",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3364_1_current_parent_grammar_signed",
            "claim": "current MTS signs that no-source-prefactor grammar",
            "passed": "false",
            "reason": "pre-action w_A S_A countermodel survives",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3364_2_tau_WEP_projection_owner",
            "claim": "tau_WEP/source-readout projection is derived and source-backed",
            "passed": "false",
            "reason": "C_parent, source worldtube, material tensor, and official readout kernel are not claim-ready",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3364_3_MICROSCOPE_bound_promotes_MTS_row",
            "claim": "3363 MICROSCOPE bound can be used as an MTS prediction/bound row",
            "passed": "false",
            "reason": "external bound is valid, but MTS projection remains blocked",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3364_4_local_GR_Newton_source",
            "claim": "source-normalized local GR/Newton source side is derived",
            "passed": "false",
            "reason": "Delta_w finite residual and total DeltaGM source-mass rows remain live",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3364_0",
            "question": "Did 3364 prove no source-only prefactor?",
            "answer": "no, but it proves the exact conditional theorem and the exact countermodel that blocks promotion",
            "reason": "S_matter=sum_A w_A S_A is covariant and Ward-compatible unless parent grammar makes w_A untypeable",
            "next_action": "keep Delta_w_AB as a finite residual or explicitly adopt/prove the typed parent grammar",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3364_1",
            "question": "Did 3364 derive tau_WEP?",
            "answer": "no",
            "reason": "formal product convention exists, but live source/readout/material/coefficient files are missing or requirements-only",
            "next_action": "do not use tau_WEP=1; treat the 3363 bound as an external target until projection files exist",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3364_2",
            "question": "What should be attacked next?",
            "answer": "source-mass DeltaGM projection or explicit finite residual rows",
            "reason": "WEP bounds relative source/species weights; Newtonian local-GR recovery also needs total source charge/mass closure",
            "next_action": "3365 DeltaGM extra mass projection bound/theorem attempt",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3365-Y5-R2FR-DeltaGM-extra-mass-projection-bound-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3365_DeltaGM_extra_mass_projection_bound_row.py",
            "objective": "attack total source-mass normalization: R_nonEH, R_symp, R_extra, R_boundary, R_time_frame, and worldtube support as explicit DeltaGM rows with theorem-zero or numeric/source-backed bounds",
            "why_next": "3364 leaves relative WEP/source weight finite; local Newton/GR still also needs total measured-GM source mass lock",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3366-Y5-R2FR-WEP-live-projection-file-acquisition-or-refusal-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3366_WEP_live_projection_file_acquisition_or_refusal.py",
            "objective": "if the WEP route is prioritized, acquire or refuse the live K_CMSM/source/material/C_parent files needed to make tau_WEP executable",
            "why_next": "tau_WEP is not derivable from the MICROSCOPE bound alone; it needs live projection data or a parent theorem",
            "valid_for_claim": "false",
        },
    ]


def validation_rows() -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = local_source_rows()
    prefactor = prefactor_attempt_rows()
    wep = wep_projection_rows()
    update = bound_update_rows()
    gates = promotion_gate_rows()
    next_rows = next_target_rows()
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append({"check_id": check_id, "check": check, "passed": bool_str(passed), "detail": detail})

    add("VAL3364_0_local_sources_exist", "all cited local source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3364_1_local_sources_parse", "all cited local source paths parse", all(row["parseable"] == "true" for row in sources))
    add("VAL3364_2_outputs_parse", "all 3364 non-validation outputs parse", all(path.exists() and parseable(path) for path in output_paths))
    add(
        "VAL3364_3_conditional_theorem_and_countermodel",
        "prefactor attempt contains exact conditional theorem and surviving countermodel",
        any(row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in prefactor)
        and any(row["result"] == "COUNTERMODEL_SURVIVES" for row in prefactor),
    )
    add(
        "VAL3364_4_wep_projection_components_covered",
        "WEP projection audit covers coefficient, source, material, readout, tau, and no-cancellation pieces",
        {row["projection_id"] for row in wep}
        == {
            "WEP3364_0_parent_coefficient",
            "WEP3364_1_source_worldtube",
            "WEP3364_2_material_tensor",
            "WEP3364_3_readout_kernel",
            "WEP3364_4_tau_product",
            "WEP3364_5_no_cancellation",
        },
    )
    add(
        "VAL3364_5_bound_row_remains_external_nonclaim",
        "3363 MICROSCOPE bound remains valid external row but not MTS projection",
        any(row["valid_external_bound"] == "true" and row["valid_mts_prediction_row"] == "false" for row in update),
    )
    add(
        "VAL3364_6_no_overclaim",
        "parent grammar, tau projection, MICROSCOPE MTS promotion, and local GR/Newton gates remain false",
        all(
            row["passed"] == "false"
            for row in gates
            if row["gate_id"]
            in {
                "GATE3364_1_current_parent_grammar_signed",
                "GATE3364_2_tau_WEP_projection_owner",
                "GATE3364_3_MICROSCOPE_bound_promotes_MTS_row",
                "GATE3364_4_local_GR_Newton_source",
            }
        )
        and all(row["valid_for_claim"] == "false" for row in prefactor + wep + update + gates),
    )
    add(
        "VAL3364_7_next_target_total_source_mass",
        "next target moves to DeltaGM extra mass projection or WEP live projection acquisition",
        any("DeltaGM-extra-mass-projection" in row["target_id"] for row in next_rows)
        and any("WEP-live-projection" in row["target_id"] for row in next_rows),
    )
    add(
        "VAL3364_8_write_scope_outside_formalization",
        "all 3364 write targets are outside formalization-workbench",
        all(FW not in path.parents and path != FW for path in [DOC, *output_paths, OUTPUTS["validation"]]),
        "write_targets=" + str(len([DOC, *output_paths, OUTPUTS["validation"]])),
    )
    overall = all(row["passed"] == "true" for row in checks)
    add("VAL3364_9_overall", "3364 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    prefactor: list[dict[str, Any]],
    wep: list[dict[str, Any]],
    update: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    sections = [
        "# 3364 - No Source Prefactor Grammar Or WEP Projection Owner Under AX1090",
        "",
        f"Generated: `{RUN_UTC}`",
        "",
        "## Summary",
        "- This checkpoint tries to turn the 3363 MICROSCOPE source-weight bound into an MTS source-normalization row.",
        "- Real theorem: if the parent grammar has only one observed matter functor and the source functor sees only total Hilbert stress, source-only species prefactors are untypeable and `Delta_w_AB=0`.",
        "- Real obstruction: the current corpus has not signed that grammar; `S_matter=sum_A w_A S_A` remains covariant and Ward-compatible, so the theorem cannot be promoted.",
        "- WEP projection also remains non-executable: `C_parent`, Earth source worldtube, Ti/Pt material tensor, official readout kernel, and `tau_WEP` are not live claim files.",
        "- Result: 3363's MICROSCOPE row stays a real external bound and a finite residual target, not a local-GR/Newton proof.",
        "",
        "## Local Source Register",
        table(sources),
        "## No Source Prefactor Theorem Attempt",
        table(prefactor),
        "## WEP Projection Owner Audit",
        table(wep),
        "## MICROSCOPE Bound Status Update",
        table(update),
        "## Promotion Gates",
        table(gates),
        "## Decision Ledger",
        table(decisions),
        "## Next Target",
        table(next_rows),
        "## Validation",
        table(validations),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_output = {
        "local_sources": local_source_rows(),
        "prefactor_attempt": prefactor_attempt_rows(),
        "wep_projection": wep_projection_rows(),
        "bound_update": bound_update_rows(),
        "gates": promotion_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(OUTPUTS[key], rows)
    validations = validation_rows()
    write_csv(OUTPUTS["validation"], validations)
    write_doc(
        rows_by_output["local_sources"],
        rows_by_output["prefactor_attempt"],
        rows_by_output["wep_projection"],
        rows_by_output["bound_update"],
        rows_by_output["gates"],
        rows_by_output["decision"],
        rows_by_output["next"],
        validations,
    )
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()

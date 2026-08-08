from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
OUT = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_local_GR_reduction_spine_under_explicit_WEP_closure.py"
DOC_PATH = ROOT / "654-Y5-R10-local-GR-reduction-spine-under-explicit-WEP-closure.md"

STATUS = "Y5_R10_local_GR_reduction_spine_under_explicit_WEP_closure_built_nonclaim"
CLAIM_CEILING = "local_GR_spine_and_debt_map_only_no_WEP_EH_Newton_PPN_R10_or_local_GR_claim"
NEXT_TARGET = "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_register_rows() -> list[dict[str, object]]:
    sources = [
        ("S654_0", "checkpoint_653_doc", ROOT / "653-Y5-R10-parent-matter-functor-signature-or-WEP-closure-demotion.md", "immediate WEP closure demotion"),
        ("S654_1", "validation_653", OUT / "P8_Y5_BRR545_653_VALIDATION.csv", "prior validation"),
        ("S654_2", "WEP_closure_653", OUT / "P8_Y5_R10_653_WEP_CLOSURE_DEMOTION.csv", "explicit WEP closure rows"),
        ("S654_3", "WEP_residual_653", OUT / "P8_Y5_R10_653_RESIDUAL_LEDGER.csv", "WEP residual and beta fallback rows"),
        ("S654_4", "local_EH_silence_506", ROOT / "506-local-EH-reduction-and-extra-sector-silence-theorem.md", "positive-operator/no-flux local EH silence theorem"),
        ("S654_5", "minimal_parent_action_511", ROOT / "511-minimal-parent-action-local-GR-fixed-point-ansatz.md", "minimal local-GR fixed-point contract"),
        ("S654_6", "Euler_Ward_538", ROOT / "538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md", "Euler/Ward chain and PiM blocker"),
        ("S654_7", "identity_stack_391", ROOT / "391-local-GR-stack-after-identity-coframe-closure.md", "older local-GR stack under identity closure"),
        ("S654_8", "sufficiency_audit_396", ROOT / "396-local-GR-reduction-sufficiency-stack-audit.md", "older sufficiency stack status legend"),
        ("S654_9", "human_review_399", ROOT / "399-local-GR-status-for-human-review.md", "human-readable local-GR status memo"),
        ("S654_10", "bound_matrix_639_doc", ROOT / "639-Y5-R10-finite-constant-beta-local-bound-matrix-runner.md", "local bound matrix overview"),
        ("S654_11", "local_bound_matrix_639", OUT / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv", "WEP/clock/PPN/Gdot/R10/R11 local bound matrix"),
        ("S654_12", "min_action_blocks_511", OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv", "minimal parent action blocks"),
        ("S654_13", "fixed_point_conditions_511", OUT / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv", "fixed-point condition ledger"),
        ("S654_14", "local_GR_residual_vector_511", OUT / "P8_MIN_PARENT_LOCAL_GR_RESIDUAL_VECTOR.csv", "local-GR residual vector"),
        ("S654_15", "symbol_action_map_512", OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv", "MTS symbol to local-GR action map"),
        ("S654_16", "generator_script_654", SCRIPT_PATH, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": source_id,
            "label": label,
            "path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for source_id, label, path, role in sources
    ]


def status_legend_rows() -> list[dict[str, object]]:
    return [
        {"status": "derived", "meaning": "parent theorem/action derivation currently signs the row", "claim_allowed": "only_if_all_promotion_gates_pass"},
        {"status": "explicit_closure", "meaning": "assumed branch condition, labelled and not public theorem", "claim_allowed": "false"},
        {"status": "conditional_theorem", "meaning": "mathematical theorem works if premises are supplied", "claim_allowed": "false"},
        {"status": "retained_residual", "meaning": "coefficient/operator remains in executable residual vector", "claim_allowed": "false"},
        {"status": "numeric_target", "meaning": "bound target exists but parent coefficient/source is not derived", "claim_allowed": "false"},
        {"status": "blocked", "meaning": "required derivation/input missing and blocks promotion", "claim_allowed": "false"},
    ]


def WEP_closure_import_rows() -> list[dict[str, object]]:
    return [
        {
            "import_id": "WCI654_0_one_geometry",
            "imported_from": "WCL653_0_one_observed_geometry",
            "local_GR_use": "matter/source/clocks use one observed geometry inside this branch",
            "status_in_654": "explicit_closure",
            "promotion_policy": "may simplify the private branch but cannot count as parent-derived WEP or source-frame proof",
            "valid_for_claim": "false",
        },
        {
            "import_id": "WCI654_1_species_blind_map",
            "imported_from": "WCL653_1_species_blind_geometry_map",
            "local_GR_use": "removes direct species class-metric split inside the closure branch",
            "status_in_654": "explicit_closure",
            "promotion_policy": "must stay visible on any PPN/source-normalization row using one matter frame",
            "valid_for_claim": "false",
        },
        {
            "import_id": "WCI654_2_no_chi_constants",
            "imported_from": "WCL653_2_no_chi_dependent_constants",
            "local_GR_use": "blocks direct alpha/mass composition channel only by closure",
            "status_in_654": "explicit_closure",
            "promotion_policy": "if direct alpha/mass source returns, beta_source_alpha target from 652/653 is active",
            "valid_for_claim": "false",
        },
        {
            "import_id": "WCI654_3_selector_stress",
            "imported_from": "WCL653_3_selector_stress_accounting",
            "local_GR_use": "selector stress must be included in Ward/Bianchi ledger",
            "status_in_654": "explicit_closure_required_before_use",
            "promotion_policy": "cannot derive local GR unless selector Ward identity is closed or residualized",
            "valid_for_claim": "false",
        },
    ]


def local_GR_spine_rows() -> list[dict[str, object]]:
    return [
        {
            "rung_id": "LGS654_0_matter_source_frame",
            "required_for_local_GR": "one observed matter/source/clock/orbital frame",
            "current_status": "explicit_closure",
            "basis": "653 WEP closure demotion",
            "blocks_if_not_promoted": "WEP/source-frame derivation remains unearned",
            "next_action": "carry closure label through every local-GR row",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "LGS654_1_EH_operator_selection",
            "required_for_local_GR": "local compact exterior metric operator is EH plus allowed Lambda/background/boundary subtraction",
            "current_status": "blocked",
            "basis": "506/511/396: EH selection remains central blocker",
            "blocks_if_not_promoted": "field equations may be scalar-tensor, higher-curvature, torsion, vector, or nonlocal rather than GR",
            "next_action": NEXT_TARGET,
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "LGS654_2_constant_G_source_normalization",
            "required_for_local_GR": "constant kappa/G_eff and measured GM source normalization",
            "current_status": "conditional_theorem",
            "basis": "511 topological kappa route plus 538 PiM blocker",
            "blocks_if_not_promoted": "Newtonian limit and Gdot/source calibration remain residualized",
            "next_action": "derive Pi_M as Hamiltonian charge and constant source measure or retain residuals",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "LGS654_3_extra_sector_silence",
            "required_for_local_GR": "every non-EH local extra sector has double zero, positive mass gap, no source charge, and zero boundary flux",
            "current_status": "conditional_theorem",
            "basis": "506 positive source-free operator theorem; 511 fixed-point conditions",
            "blocks_if_not_promoted": "linear non-EH leakage, scalar/vector/tensor hair, memory drift, or source-normalization force",
            "next_action": "field-match Gamma_eff, K_hat, q_loc, chi_D, Qcoh, memory, kappa to action operators",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "LGS654_4_boundary_no_flux",
            "required_for_local_GR": "worldtube/linking-sphere boundary terms have no extra mass flux",
            "current_status": "blocked",
            "basis": "506/511/538 boundary and PiM ledgers",
            "blocks_if_not_promoted": "M_eff/GM can absorb hidden boundary charge",
            "next_action": "derive no-flux/reference subtraction or retain boundary residual vector",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "LGS654_5_domain_projector_preferred_frame",
            "required_for_local_GR": "domain/projector/flow sector is gauge, topological, silent, or bounded below preferred-frame limits",
            "current_status": "retained_residual",
            "basis": "511 A511_4 plus 639 alpha_i/xi rows",
            "blocks_if_not_promoted": "preferred-frame alpha1/alpha2/alpha3/xi and source-normalization residuals remain active",
            "next_action": "derive selector no-stress theorem or execute residual vector against bounds",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "LGS654_6_R10_fifth_force",
            "required_for_local_GR": "finite-range force channels are theorem-zero or have sourced alpha(lambda) predictions below bounds",
            "current_status": "retained_residual",
            "basis": "639 R10 row and 650 cross-arena contract",
            "blocks_if_not_promoted": "short-range/fifth-force residuals remain unscored and cannot be waved away",
            "next_action": "derive mode Hessian/source charges/range or keep R10 pressure-only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "LGS654_7_weak_field_PPN_readout",
            "required_for_local_GR": "derive gamma=beta=1, alpha_i=xi=0, no Gdot/G, and no retained non-EH vector through required order",
            "current_status": "blocked",
            "basis": "511 FP511_7; 639 PPN/Gdot matrix",
            "blocks_if_not_promoted": "even Newton-looking leading order is not full local GR",
            "next_action": "after EH/source/nohair gates, derive PPN vector or run same-pipeline residual bounds",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "LGS654_8_transition_control",
            "required_for_local_GR": "local/cosmology/galaxy transition scale is action-derived, not arena-selected",
            "current_status": "blocked",
            "basis": "511 FP511_8 and 650 parent domain classifier warning",
            "blocks_if_not_promoted": "local GR plus cosmological MTS becomes a patchwork switch",
            "next_action": "derive ell_tr/L_cg or activation rule from operator/source spectrum",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG654_0_WEP_closure_label_visible",
            "gate": "WEP/common matter frame is labelled closure wherever used",
            "result": "pass",
            "consequence": "no hidden WEP theorem promotion",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PG654_1_EH_operator_selected",
            "gate": "local operator is parent-derived EH-only or non-EH vector is executable",
            "result": "fail_blocked",
            "consequence": "next target is EH operator selection / retained R11 vector",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PG654_2_source_charge_closed",
            "gate": "Pi_M/source measure equals Hamiltonian/EH charge with no calibration residual",
            "result": "fail_open",
            "consequence": "Newton/source-normalization is not promoted",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PG654_3_extra_sectors_silent",
            "gate": "double-zero, positive operator, no source charge, and zero boundary flux are field-matched",
            "result": "fail_open",
            "consequence": "extra-sector residual vector remains active",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PG654_4_PPN_vector_derived",
            "gate": "PPN/Gdot/R10/local-bound vector is derived or scored below bounds",
            "result": "fail_not_ready",
            "consequence": "no PPN/local-GR pass",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "PG654_5_local_GR_claim",
            "gate": "claim MTS reduces to GR locally",
            "result": "fail_policy",
            "consequence": "spine is a debt map only",
            "valid_for_claim": "false",
        },
    ]


def observable_bound_rollup_rows() -> list[dict[str, object]]:
    matrix = read_csv(OUT / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv")
    rows: list[dict[str, object]] = []
    for row in matrix:
        row_id = row["row_id"]
        if row_id in {"R0_identity_coframe_direct", "R1_WEP_source_charge"}:
            spine_owner = "LGS654_0_matter_source_frame"
            status = "explicit_closure_or_beta_target"
        elif row_id == "R2_clock_redshift":
            spine_owner = "LGS654_0_matter_source_frame;LGS654_8_transition_control"
            status = "product_bound_only_not_GR_pass"
        elif row_id in {"R3_gamma", "R4_beta", "R5_alpha1", "R6_alpha2", "R7_alpha3", "R8_xi"}:
            spine_owner = "LGS654_1_EH_operator_selection;LGS654_5_domain_projector_preferred_frame;LGS654_7_weak_field_PPN_readout"
            status = "PPN_bound_present_prediction_symbolic"
        elif row_id == "R9_Gdot":
            spine_owner = "LGS654_2_constant_G_source_normalization;LGS654_3_extra_sector_silence"
            status = "Gdot_bound_present_prediction_symbolic"
        elif row_id == "R10_fifth_force":
            spine_owner = "LGS654_6_R10_fifth_force"
            status = "R10_bound_present_prediction_symbolic"
        else:
            spine_owner = "LGS654_1_EH_operator_selection;LGS654_7_weak_field_PPN_readout"
            status = "R11_operator_vector_symbolic"
        rows.append(
            {
                "rollup_id": f"OBR654_{len(rows):02d}",
                "row_id": row_id,
                "observable": row["observable"],
                "bound_value": row["bound_value"],
                "bound_units": row["bound_units"],
                "spine_owner": spine_owner,
                "current_status": status,
                "prediction_numeric_ready": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            }
        )
    return rows


def next_action_queue_rows() -> list[dict[str, object]]:
    return [
        {
            "queue_id": "NAQ654_0",
            "priority": 1,
            "target": NEXT_TARGET,
            "work_item": "Try to derive EH operator selection under explicit WEP closure, or retain a non-EH/R11 coefficient vector.",
            "why_first": "without EH operator selection, no PPN/local-GR derivation can start",
            "acceptance_condition": "metric sector is EH-only by parent action, or every retained operator has a named coefficient and bound route",
            "valid_for_claim": "false",
        },
        {
            "queue_id": "NAQ654_1",
            "priority": 2,
            "target": "656-Y5-R10-PiM-Hamiltonian-source-charge-or-measured-GM-residual.md",
            "work_item": "Revisit Pi_M/source charge as Hamiltonian/EH mass map.",
            "why_first": "Newtonian limit needs source charge before PPN can be meaningful",
            "acceptance_condition": "Pi_M(Phi0)=Pi_EH and first variation zero, or source calibration residual is explicit",
            "valid_for_claim": "false",
        },
        {
            "queue_id": "NAQ654_2",
            "priority": 3,
            "target": "657-Y5-R10-extra-sector-silence-vector-under-local-GR-spine.md",
            "work_item": "Field-match extra sectors to double-zero/mass-gap/no-flux conditions.",
            "why_first": "extra hair is the main way local GR fails after EH/source gates",
            "acceptance_condition": "each extra sector is theorem-zero, pure gauge/topological, or executable residual",
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, object]]:
    spine = local_GR_spine_rows()
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "spine_rungs": len(spine),
            "WEP_status": "explicit_closure",
            "EH_operator_selected": "false",
            "source_charge_closed": "false",
            "PPN_vector_derived": "false",
            "prediction_numeric_ready_rows": "0",
            "local_GR_claim": "false",
            "hardest_next_blocker": "EH operator selection or retained R11 vector",
            "next_target": NEXT_TARGET,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    status_rows: list[dict[str, object]],
    WEP_rows: list[dict[str, object]],
    spine_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    observable_rows: list[dict[str, object]],
    queue_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V654_0_source_paths_exist", all(row["exists"] == "true" for row in source_rows), "all cited local source paths exist"))
    prior = read_csv(OUT / "P8_Y5_BRR545_653_VALIDATION.csv")
    checks.append(("V654_1_prior_653_validation_clean", all(row.get("result") == "pass" for row in prior), "653 validation remains clean"))
    checks.append(("V654_2_status_legend_complete", {"derived", "explicit_closure", "conditional_theorem", "retained_residual", "numeric_target", "blocked"}.issubset({row["status"] for row in status_rows}), "status legend covers required classes"))
    checks.append(("V654_3_WEP_import_closure_not_derived", all("closure" in row["status_in_654"] for row in WEP_rows), "WEP rows imported as closure, not derived"))
    required_rungs = {"LGS654_0_matter_source_frame", "LGS654_1_EH_operator_selection", "LGS654_2_constant_G_source_normalization", "LGS654_3_extra_sector_silence", "LGS654_7_weak_field_PPN_readout"}
    checks.append(("V654_4_spine_core_rungs_present", required_rungs.issubset({row["rung_id"] for row in spine_rows}), "core local-GR spine rungs are present"))
    checks.append(("V654_5_no_spine_claims", all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in spine_rows), "no spine rung is claimable"))
    checks.append(("V654_6_EH_gate_blocks", any(row["gate_id"] == "PG654_1_EH_operator_selected" and row["result"] == "fail_blocked" for row in gate_rows), "EH operator gate blocks promotion"))
    checks.append(("V654_7_local_GR_claim_blocked", any(row["gate_id"] == "PG654_5_local_GR_claim" and row["result"] == "fail_policy" for row in gate_rows), "local-GR claim is blocked"))
    matrix = read_csv(OUT / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv")
    checks.append(("V654_8_observable_rollup_covers_639", len(observable_rows) == len(matrix) and len(observable_rows) >= 12, "observable rollup covers all 639 local bound rows"))
    checks.append(("V654_9_observables_not_numeric_ready", all(row["prediction_numeric_ready"] == "false" for row in observable_rows), "observable predictions remain nonnumeric/nonclaim"))
    checks.append(("V654_10_next_target_655", queue_rows[0]["target"] == NEXT_TARGET and "EH-operator" in NEXT_TARGET, "next target selects EH operator/R11 vector gate"))
    checks.append(("V654_11_summary_blocks_claim", summary[0]["local_GR_claim"] == "false" and summary[0]["EH_operator_selected"] == "false", "summary blocks local-GR claim"))

    fw = ROOT.parent / "formalization-workbench"
    cutoff = datetime(2026, 5, 31, 14, 42, 0).timestamp()
    changed_after_cutoff = 0
    if fw.exists():
        for path in fw.rglob("*"):
            if path.is_file() and path.stat().st_mtime > cutoff:
                changed_after_cutoff += 1
    checks.append(("V654_12_formalization_workbench_unchanged", changed_after_cutoff == 0, f"formalization files changed after cutoff: {changed_after_cutoff}"))

    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now_iso(),
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("|", "\\|").replace("\n", " ")
            values.append(text)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    source_rows: list[dict[str, object]],
    status_rows: list[dict[str, object]],
    WEP_rows: list[dict[str, object]],
    spine_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    observable_rows: list[dict[str, object]],
    queue_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 654 Y5/R10 Local-GR Reduction Spine Under Explicit WEP Closure",
        "",
        "## Verdict",
        "",
        f"- Status: `{STATUS}`",
        f"- Claim ceiling: `{CLAIM_CEILING}`",
        "- WEP/common matter geometry is now carried as explicit closure, not parent-derived proof.",
        "- Under that label, the local-GR route is coherent but still blocked by EH operator selection, source charge/GM normalization, extra-sector silence, boundary no-flux, R10/fifth-force rows, and PPN readout.",
        "- The next highest-leverage gate is EH operator selection or a retained non-EH/R11 vector.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["source_id", "label", "path", "exists", "role"]),
        "",
        "## Status Legend",
        "",
        markdown_table(status_rows, ["status", "meaning", "claim_allowed"]),
        "",
        "## WEP Closure Import",
        "",
        markdown_table(WEP_rows, ["import_id", "imported_from", "local_GR_use", "status_in_654", "promotion_policy"]),
        "",
        "## Local-GR Spine",
        "",
        markdown_table(spine_rows, ["rung_id", "required_for_local_GR", "current_status", "basis", "blocks_if_not_promoted", "next_action"]),
        "",
        "## Promotion Gates",
        "",
        markdown_table(gate_rows, ["gate_id", "gate", "result", "consequence"]),
        "",
        "## Observable Bound Rollup",
        "",
        markdown_table(observable_rows, ["rollup_id", "row_id", "observable", "bound_value", "spine_owner", "current_status", "prediction_numeric_ready"]),
        "",
        "## Next Action Queue",
        "",
        markdown_table(queue_rows, ["queue_id", "priority", "target", "work_item", "acceptance_condition"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["check_id", "result", "detail"]),
        "",
        "## Interpretation",
        "",
        "- This is a good checkpoint: WEP is boxed, but GR is not smuggled in behind it.",
        "- The spine says exactly why `matter sees one geometry` is not enough: the exterior dynamics must still be EH, source-normalized, no-hair, and PPN-clean.",
        "- The next clean target is EH operator selection because every PPN/local-bound row depends on whether non-EH operators are zero or explicitly retained.",
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(summary, ["status", "WEP_status", "EH_operator_selected", "source_charge_closed", "PPN_vector_derived", "prediction_numeric_ready_rows", "local_GR_claim", "hardest_next_blocker", "next_target"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    status_rows = status_legend_rows()
    WEP_rows = WEP_closure_import_rows()
    spine_rows = local_GR_spine_rows()
    gate_rows = promotion_gate_rows()
    observable_rows = observable_bound_rollup_rows()
    queue_rows = next_action_queue_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, status_rows, WEP_rows, spine_rows, gate_rows, observable_rows, queue_rows, summary)

    write_csv(OUT / "P8_Y5_R10_654_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_654_STATUS_LEGEND.csv", status_rows)
    write_csv(OUT / "P8_Y5_R10_654_WEP_CLOSURE_IMPORT.csv", WEP_rows)
    write_csv(OUT / "P8_Y5_R10_654_LOCAL_GR_SPINE.csv", spine_rows)
    write_csv(OUT / "P8_Y5_R10_654_PROMOTION_GATES.csv", gate_rows)
    write_csv(OUT / "P8_Y5_R10_654_OBSERVABLE_BOUND_ROLLUP.csv", observable_rows)
    write_csv(OUT / "P8_Y5_R10_654_NEXT_ACTION_QUEUE.csv", queue_rows)
    write_csv(OUT / "P8_Y5_R10_654_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_BRR545_654_VALIDATION.csv", validation)
    write_doc(source_rows, status_rows, WEP_rows, spine_rows, gate_rows, observable_rows, queue_rows, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote_doc={DOC_PATH}")
    print(f"wrote_csv_dir={OUT}")
    print(f"spine_rungs={summary[0]['spine_rungs']}")
    print(f"local_GR_claim={summary[0]['local_GR_claim']}")
    print(f"validation_rows={len(validation)}")
    print(f"validation_failures={len(failures)}")
    print(f"status={STATUS}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for row in failures:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

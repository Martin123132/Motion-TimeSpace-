from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2180"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2180-Y5-R2FR-PiM-JH-mass-current-to-v-source-coefficient-glue-or-delta-kappa-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2180_SOURCE_REGISTER.csv",
    "mass_glue": OUT / "P8_Y5_PARENT_QLOC_2180_PIM_JH_MASS_CURRENT_GLUE_AUDIT.csv",
    "newton_law": OUT / "P8_Y5_PARENT_QLOC_2180_NEWTON_SOURCE_GLUE_RESIDUAL_LAW.csv",
    "kappa_glue": OUT / "P8_Y5_PARENT_QLOC_2180_KAPPA_BETA_GLUE_LEDGER.csv",
    "finite_rows": OUT / "P8_Y5_PARENT_QLOC_2180_DELTA_KAPPA_GLUE_FINITE_ROWS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2180_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2180_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2180_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2180_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2180_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2180_DELTA_KAPPA_GLUE_FINITE_ROWS_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2180_MASS_CURRENT_GLUE_AUDIT_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PIM_JH_TO_V_SOURCE_GLUE_2180_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2180_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2180-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2180*",
        "*P8_Y5_BRR545_2180*",
        "*Y5_R2FR_PiM_JH_mass_current_to_v_source_coefficient_glue_or_delta_kappa_fill_2180*",
        "*JR2180*",
        "*PIM_JH_TO_V_SOURCE_GLUE_2180*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2179_handoff",
            ROOT / "2179-Y5-R2FR-parent-v-field-action-normalization-and-beta-quadratic-zero-or-finite-row.md",
            ["NEXT2179_0_2180", "MASS_CURRENT_TO_V_SOURCE_COEFFICIENT_GLUE_NEXT"],
            "2179 selects Pi_M J_H/source-measure glue to K_v,C_v and eta_v=0 as the next gate.",
        ),
        (
            "2179_validation",
            OUT / "P8_Y5_BRR545_2179_VALIDATION.csv",
            ["VAL2179_OVERALL", "PASS"],
            "2179 validation passed before 2180 continues the chain.",
        ),
        (
            "1012_source_norm",
            ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
            ["Y5 source-normalization remains retained residual", "Newton_Poisson_orbit"],
            "1012 records that measured-GM/source-normalization ownership is not derived.",
        ),
        (
            "1013_flux_obstruction",
            ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
            ["d(Pi_M J_H)=0 compact-exterior flux closure", "[d,Pi_M]J_H"],
            "1013 supplies the exact Pi_M J_H flux obstruction and commutator gate.",
        ),
        (
            "charge_current_direct",
            OUT / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
            ["CC7_closed_flux_and_Gauss_calibration", "CC8_second_order_limit"],
            "direct charge-current attempt separates first-order Gauss calibration from second-order beta stability.",
        ),
        (
            "noether_closure",
            OUT / "P8_PARENT_NOETHER_CLOSURE_THEOREM.csv",
            ["T505_source_measure_matching", "T505_Newton_limit_corollary"],
            "parent Noether closure theorem gives the exact conditional source-measure matching route.",
        ),
        (
            "1886_source_slot",
            ROOT / "1886-Y5-R2FR-common-matter-no-source-only-slot-proof-or-finite-wR-row.md",
            ["NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED", "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_GUARD"],
            "1886 blocks measured-G absorption and hidden source-only matter slots.",
        ),
        (
            "1885_beta_guard",
            ROOT / "1885-Y5-R2FR-beta-second-order-source-coupling-gate-or-parent-zero-row.md",
            ["NO_GAMMA_ONLY_PROMOTION", "BETA_GATE_NOT_DERIVED_CURRENT_CORPUS"],
            "1885 blocks gamma-only promotion and keeps beta/source residuals live.",
        ),
    ]
    rows = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def mass_glue_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "MCG2180_0_same_frame",
            "same-frame Hilbert current",
            "J_H[e_obs] must be defined by the same observed coframe used by clocks, rods, orbits and the constrained v readout.",
            "CONDITIONAL_NOT_PARENT_DERIVED",
            "same-frame wording is not yet enough to claim source ownership.",
        ),
        (
            "MCG2180_1_parent_PiM",
            "parent-owned Pi_M",
            "Pi_M must be fixed before readout as a parent charge/projector, not chosen as a post-fit measured-GM mask.",
            "MISSING_PARENT_PIM_ORIGIN",
            "1012 and 1013 keep projector origin unsigned.",
        ),
        (
            "MCG2180_2_flux_closure",
            "compact-exterior flux closure",
            "d(Pi_M J_H)=0 requires Pi_M dJ_H plus [d,Pi_M]J_H and extra-current/anomaly terms to vanish or be bounded.",
            "EXACT_OBSTRUCTION_ACTIVE",
            "1013 already shows closure is not automatic.",
        ),
        (
            "MCG2180_3_worldtube_glue",
            "worldtube source equals exterior charge",
            "M_source[W]=integral_S Pi_M J_H=M_eff must hold before orbital fitting.",
            "MISSING_WORLDTUBE_SOURCE_GLUE",
            "a closed wrong charge can still mimic success.",
        ),
        (
            "MCG2180_4_action_ratio_split",
            "action ratio versus mass glue",
            "Pi_M J_H can identify the source measure, but it does not by itself derive the K_v/C_v action coefficient ratio.",
            "SPLIT_PROBLEM_IDENTIFIED",
            "Newton needs both action normalization and mass-current glue.",
        ),
        (
            "MCG2180_5_success_package",
            "mass-current to v-source glue",
            "same-frame J_H, parent Pi_M, flux closure, worldtube glue, no extra mu channels, fixed G_ref, and K_v/C_v target ratio all hold together.",
            "NOT_SATISFIED_CURRENT_CORPUS",
            "Newton/local-GR gates remain blocked.",
        ),
    ]
    return [
        base_row(
            glue_id=glue_id,
            gate=gate,
            statement=statement,
            status=status,
            implication=implication,
        )
        for glue_id, gate, statement, status, implication in specs
    ]


def newton_law_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "NGL2180_0_action_residual",
            "action coefficient residual",
            "delta_KC := C_v c^4/(16piG_ref K_v)-1.",
            "EXACT_FROM_2179",
            "this is the action-side source-normalization error.",
        ),
        (
            "NGL2180_1_mass_glue_residual",
            "mass-current glue residual",
            "epsilon_M := M_source[v]/M_eff[Pi_M J_H]-1.",
            "EXACT_DEFINITION",
            "this is the source-measure mismatch not absorbable into GM without guards.",
        ),
        (
            "NGL2180_2_observable_newton_residual",
            "combined Newton residual",
            "Delta_Newton_v := (1+delta_KC)(1+epsilon_M)-1.",
            "EXACT_NEWTON_GLUE_RESIDUAL",
            "Newton requires the combined residual to vanish or be finite-and-tested.",
        ),
        (
            "NGL2180_3_zero_condition",
            "clean zero theorem",
            "If delta_KC=0 and epsilon_M=0, the constrained v branch gives the correct inverse-square source amplitude.",
            "PASS_CONDITIONAL_ZERO",
            "this is the clean theorem target, not current evidence.",
        ),
        (
            "NGL2180_4_epsilon_decomposition",
            "epsilon_M decomposition",
            "epsilon_M is fed by worldtube glue error, -Pi_M dJ_extra, [d,Pi_M]J_H, A_parent, mu_extra channels and calibration offset.",
            "EXACT_DEBT_MAP",
            "1012/1013 obstruction rows map directly into the new v-source residual.",
        ),
        (
            "NGL2180_5_current_status",
            "current Newton source status",
            "Neither delta_KC nor epsilon_M is parent-zero or source-backed numeric in the current corpus.",
            "NEWTON_SOURCE_GLUE_NOT_DERIVED",
            "finite rows remain mandatory.",
        ),
    ]
    return [
        base_row(
            law_id=law_id,
            object=object_name,
            statement=statement,
            status=status,
            implication=implication,
        )
        for law_id, object_name, statement, status, implication in specs
    ]


def kappa_glue_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "KGL2180_0_beta_law",
            "beta from kappa",
            "beta-1=kappa_v/2.",
            "EXACT_FROM_2179",
            "beta remains tied to the quadratic v tail.",
        ),
        (
            "KGL2180_1_kappa_decomposition",
            "kappa decomposition",
            "kappa_v = -eta_v + kappa_source_quad + kappa_PiM + kappa_boundary + kappa_readout + kappa_operator.",
            "EXACT_LEDGER_DEFINITION",
            "all second-order channels are carried explicitly with no cancellation credit.",
        ),
        (
            "KGL2180_2_PiM_beta_channel",
            "Pi_M/projector beta channel",
            "A potential-dependent M_source/M_eff or nonzero [d,Pi_M]J_H contributes to kappa_PiM after first-order normalization.",
            "MISSING_PIM_BETA_ZERO_OR_VALUE",
            "source-measure glue must hold through O(U^2), not merely at monopole order.",
        ),
        (
            "KGL2180_3_source_slot_channel",
            "quadratic source slot",
            "rho c^2 v^2 or beta_w source-weight terms contribute kappa_source_quad unless no-source-only-slot theorem closes.",
            "MISSING_SOURCE_QUADRATIC_ZERO_OR_VALUE",
            "1886 remains active.",
        ),
        (
            "KGL2180_4_boundary_operator_channel",
            "boundary/readout/operator beta channels",
            "boundary, endpoint, non-EH operator and readout quadratic terms contribute to kappa_v unless theorem-zero or source-backed.",
            "MISSING_BOUNDARY_OPERATOR_ZERO_OR_VALUE",
            "1885 beta vector remains the guardrail.",
        ),
        (
            "KGL2180_5_current_status",
            "kappa zero status",
            "No parent-signed chain proves eta_v=kappa_source_quad=kappa_PiM=kappa_boundary=kappa_readout=kappa_operator=0.",
            "KAPPA_GLUE_NOT_DERIVED",
            "beta remains blocked.",
        ),
    ]
    return [
        base_row(
            kappa_id=kappa_id,
            object=object_name,
            statement=statement,
            status=status,
            implication=implication,
        )
        for kappa_id, object_name, statement, status, implication in specs
    ]


def finite_row_rows() -> list[dict[str, Any]]:
    specs = [
        ("DKG2180_0_delta_KC", "delta_KC", "C_v c^4/(16piG_ref K_v)-1 action coefficient residual", "MISSING_KV_CV_THEOREM_OR_NUMERIC_VALUE", "dimensionless", "Newton;PPN;orbital"),
        ("DKG2180_1_epsilon_M", "epsilon_M", "M_source[v]/M_eff[Pi_M J_H]-1 source-measure glue residual", "MISSING_MASS_GLUE_THEOREM_OR_NUMERIC_VALUE", "dimensionless", "Newton;PPN;R11"),
        ("DKG2180_2_Delta_Newton_v", "Delta_Newton_v", "(1+delta_KC)(1+epsilon_M)-1 combined Newton amplitude residual", "MISSING_COMPONENT_VALUES", "dimensionless", "Newton;orbital;PPN"),
        ("DKG2180_3_I_commutator", "I_commutator", "[d,Pi_M]J_H projected source-measure commutator contribution", "MISSING_COMMUTATOR_ZERO_OR_VALUE", "GM_flux_or_dimensionless", "Newton;R11;PPN"),
        ("DKG2180_4_extra_current", "epsilon_extra_current", "-Pi_M dJ_extra plus A_parent source anomaly contribution", "MISSING_EXTRA_CURRENT_ZERO_OR_VALUE", "GM_flux_or_dimensionless", "Newton;R11;PPN"),
        ("DKG2180_5_kappa_PiM", "kappa_PiM", "second-order beta contribution from potential-dependent mass-current/source-measure glue", "MISSING_PIM_BETA_ZERO_OR_VALUE", "dimensionless", "PPN_beta;local_GR"),
        ("DKG2180_6_kappa_total", "kappa_v_total", "absolute beta-tail vector from eta/source/PiM/boundary/readout/operator channels", "MISSING_KAPPA_COMPONENT_VALUES", "dimensionless", "PPN_beta;local_GR"),
        ("DKG2180_7_total", "epsilon_v_glue_abs", "absolute no-cancellation envelope for Newton and beta glue residuals", "MISSING_COMPONENT_VALUES", "declared_common_norm", "all_local_arenas"),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            status=status,
            units=units,
            observable_link=observable_link,
            value="MISSING_NUMERIC_VALUE",
            source_path="MISSING_SOURCE_PATH",
            score_ready=False,
            no_cancellation_policy=True,
        )
        for row_id, symbol, definition, status, units, observable_link in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2180_0_delta_KC", "action coefficient residual is zero or sourced", "UNSIGNED", "K_v/C_v ratio still not parent-derived"),
        ("CG2180_1_epsilon_M", "mass-current/source-measure glue residual is zero or sourced", "UNSIGNED", "Pi_M J_H closure/worldtube glue remain unsigned"),
        ("CG2180_2_Delta_Newton", "combined Newton residual passes", "UNSIGNED", "Delta_Newton_v has no zero theorem or numeric bound"),
        ("CG2180_3_kappa", "kappa_v beta-tail vector is zero or sourced", "UNSIGNED", "beta remains blocked"),
        ("CG2180_4_no_absorption", "measured-G absorption shortcut rejected", "PASS_GUARDRAIL", "1886/1012 no-absorption guard retained"),
        ("CG2180_5_conditional_package", "clean package would derive Newton source amplitude", "CONDITIONAL_PASS", "requires action ratio and mass glue together"),
        ("CG2180_6_verdict", "Newton/local-GR claim", "BLOCKED_NONCLAIM", "2180 installs glue laws and finite rows, not a claim"),
    ]
    return [
        base_row(
            gate_id=gate_id,
            gate=gate,
            status=status,
            implication=implication,
        )
        for gate_id, gate, status, implication in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2180_0_gain_split",
            "ACTION_RATIO_AND_MASS_GLUE_SPLIT_DERIVED",
            "Newton source recovery needs both delta_KC=0 and epsilon_M=0; Pi_M J_H alone cannot fix K_v/C_v.",
            "selected",
        ),
        (
            "DEC2180_1_gain_law",
            "COMBINED_NEWTON_RESIDUAL_LAW_DERIVED",
            "Delta_Newton_v=(1+delta_KC)(1+epsilon_M)-1 is the live observable amplitude residual.",
            "selected",
        ),
        (
            "DEC2180_2_gain_beta",
            "KAPPA_GLUE_VECTOR_WRITTEN",
            "kappa_v now carries eta_v, source quadratic, Pi_M, boundary, readout and operator channels explicitly.",
            "selected",
        ),
        (
            "DEC2180_3_no_claim",
            "PIM_JH_GLUE_AND_KV_CV_STILL_UNSIGNED",
            "1012/1013 obstruction rows remain active and K_v/C_v still lacks parent coefficient origin.",
            "selected",
        ),
        (
            "DEC2180_4_next",
            "PIM_COMMUTATOR_AND_WORLDTUBE_GLUE_NEXT",
            "the next derivation should attack [d,Pi_M]J_H=0 plus worldtube source equality, while keeping K_v/C_v finite rows live.",
            "selected",
        ),
    ]
    return [
        base_row(
            decision_id=decision_id,
            decision=decision,
            rationale=rationale,
            selection_status=status,
        )
        for decision_id, decision, rationale, status in specs
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2180_0_2181",
            selection_status="selected",
            target_file="2181-Y5-R2FR-PiM-commutator-worldtube-source-glue-zero-or-epsilonM-fill.md",
            target_script="scripts/Y5_R2FR_PiM_commutator_worldtube_source_glue_zero_or_epsilonM_fill_2181.py",
            objective="derive [d,Pi_M]J_H=0 and worldtube source equality for the constrained v branch, or fill epsilon_M/I_commutator finite rows with Newton/PPN projections",
            success_condition="fixed parent Pi_M, zero commutator, zero extra-current/anomaly, worldtube source equality and no measured-G absorption; otherwise epsilon_M is source-backed and nonclaim",
            do_not_do="do not count closed wrong charge as Newton evidence, do not use post-readout projector masks, do not absorb residuals into GM without guards",
        ),
        base_row(
            route_id="NEXT2180_1_action_parallel",
            selection_status="held_parallel",
            target_file="2181b-Y5-R2FR-Kv-Cv-parent-action-coefficient-origin-or-deltaKC-fill.md",
            target_script="scripts/Y5_R2FR_Kv_Cv_parent_action_coefficient_origin_or_deltaKC_fill_2181b.py",
            objective="derive K_v/C_v from the parent v action or fill delta_KC finite rows",
            success_condition="K_v and C_v have source paths/units or delta_KC has a numeric bound row; all nonclaim until the full envelope closes",
            do_not_do="do not import EH normalization or fit G to local tests",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["finite_rows"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["mass_glue"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["newton_law"], BRANCH_COPIES["source_weight"]),
    ]
    rows = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
            if str(row.get("valid_for_claim", "")).lower() == "true":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    source_rows = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2180_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2180_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    glue_statuses = {row["status"] for row in rows_by_name["mass_glue"]}
    glue_pass = "SPLIT_PROBLEM_IDENTIFIED" in glue_statuses and "NOT_SATISFIED_CURRENT_CORPUS" in glue_statuses
    validations.append(base_row(validation_id="VAL2180_02_mass_glue_audit", status="PASS" if glue_pass else "FAIL", detail="mass-current glue is separated from K_v/C_v action normalization"))

    newton_statuses = {row["status"] for row in rows_by_name["newton_law"]}
    newton_pass = "EXACT_NEWTON_GLUE_RESIDUAL" in newton_statuses and "EXACT_DEBT_MAP" in newton_statuses and "NEWTON_SOURCE_GLUE_NOT_DERIVED" in newton_statuses
    validations.append(base_row(validation_id="VAL2180_03_newton_law", status="PASS" if newton_pass else "FAIL", detail="Delta_Newton_v combined residual law derived and kept nonclaim"))

    kappa_statuses = {row["status"] for row in rows_by_name["kappa_glue"]}
    kappa_pass = "EXACT_LEDGER_DEFINITION" in kappa_statuses and "KAPPA_GLUE_NOT_DERIVED" in kappa_statuses
    validations.append(base_row(validation_id="VAL2180_04_kappa_glue", status="PASS" if kappa_pass else "FAIL", detail="kappa beta-tail glue vector written and remains blocked"))

    finite_rows = rows_by_name["finite_rows"]
    finite_ok = all(str(row.get("status", "")).startswith("MISSING_") and not bool(row.get("score_ready")) for row in finite_rows)
    validations.append(base_row(validation_id="VAL2180_05_finite_rows", status="PASS" if finite_ok else "FAIL", detail=f"delta/kappa glue finite rows={len(finite_rows)} remain score_ready=false"))

    claim_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(base_row(validation_id="VAL2180_06_claim_gate", status="PASS" if "BLOCKED_NONCLAIM" in claim_statuses and "PASS_GUARDRAIL" in claim_statuses else "FAIL", detail="Newton/local-GR claim remains blocked and no-absorption guard retained"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2180_07_decision", status="PASS" if "PIM_COMMUTATOR_AND_WORLDTUBE_GLUE_NEXT" in decision_text else "FAIL", detail="decision selects Pi_M commutator and worldtube glue next"))

    validations.append(base_row(validation_id="VAL2180_08_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2181" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2181 commutator/worldtube glue target selected"))

    validations.append(base_row(validation_id="VAL2180_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2180_10_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2180_11_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2180_artifacts()
    validations.append(base_row(validation_id="VAL2180_12_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2180 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2180_13_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2180_OVERALL", status="PASS" if overall else "FAIL", detail="2180 derives Delta_Newton_v mass-current/action-ratio glue law and keeps local-GR blocked"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2180 - Y5/R2FR PiM JH Mass-Current To V Source Coefficient Glue Or Delta/Kappa Fill

## Current Verdict

2180 splits the remaining Newton problem into the two pieces that must both close:

1. the **action coefficient ratio** `delta_KC`;
2. the **mass-current/source-measure glue** `epsilon_M`.

From 2179:

`delta_KC := C_v c^4/(16piG_ref K_v)-1`.

For the parent mass-current chain define:

`epsilon_M := M_source[v]/M_eff[Pi_M J_H]-1`.

Then the actual Newton amplitude residual is:

`Delta_Newton_v := (1+delta_KC)(1+epsilon_M)-1`.

This is the important result. A clean local Newton branch needs `delta_KC=0` **and** `epsilon_M=0`. A closed `Pi_M J_H` charge alone is not enough if it is the wrong charge, the wrong normalization, or a post-readout mask. Likewise, the right `K_v/C_v` ratio is not enough if the source measure is not the same mass used by clocks/orbits.

The beta side remains sharp:

`beta-1=kappa_v/2`,

with:

`kappa_v = -eta_v + kappa_source_quad + kappa_PiM + kappa_boundary + kappa_readout + kappa_operator`.

So 2180 does not claim Newton/GR. It tells us exactly what must be derived next: `[d,Pi_M]J_H=0`, worldtube source equality, no extra-current/anomaly, no source-only quadratic slot, and separately the `K_v/C_v` parent action ratio.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## Pi_M J_H Mass-Current Glue Audit

{md_table(rows_by_name["mass_glue"], ["glue_id", "gate", "statement", "status", "implication", "valid_for_claim"])}

## Newton Source Glue Residual Law

{md_table(rows_by_name["newton_law"], ["law_id", "object", "statement", "status", "implication", "valid_for_claim"])}

## Kappa Beta Glue Ledger

{md_table(rows_by_name["kappa_glue"], ["kappa_id", "object", "statement", "status", "implication", "valid_for_claim"])}

## Delta/Kappa Glue Finite Rows

{md_table(rows_by_name["finite_rows"], ["row_id", "symbol", "definition", "status", "units", "observable_link", "value", "source_path", "score_ready", "valid_for_claim"])}

## Claim Gate

{md_table(rows_by_name["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Working Interpretation

This is not a defeat; it is the opposite of fog. The local branch now has a hard algebraic diagnostic:

`Delta_Newton_v=(1+delta_KC)(1+epsilon_M)-1`.

If the parent theory derives `delta_KC=0` and `epsilon_M=0`, Newton source normalization is no longer a handwave. If it cannot, those become finite empirical rows. Same for beta: `kappa_v` is now a channel ledger, not a vibes problem.

The next best derivation is not broad. It is surgical: prove the `Pi_M` commutator/worldtube glue part of `epsilon_M`, or admit it as a finite source-normalization residual.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "mass_glue": mass_glue_rows(),
        "newton_law": newton_law_rows(),
        "kappa_glue": kappa_glue_rows(),
        "finite_rows": finite_row_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in ["source_register", "mass_glue", "newton_law", "kappa_glue", "finite_rows", "claim_gate", "decision", "next_target"]:
        write_csv(OUTPUTS[name], rows_by_name[name])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()

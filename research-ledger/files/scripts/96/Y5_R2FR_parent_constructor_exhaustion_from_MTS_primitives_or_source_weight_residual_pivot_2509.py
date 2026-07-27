from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_CONSTRUCTOR_EXHAUSTION_OR_SOURCE_WEIGHT_PIVOT_2509"
CHECKPOINT_ID = "2509"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"

DOC = ROOT / "2509-Y5-R2FR-parent-constructor-exhaustion-from-MTS-primitives-or-source-weight-residual-pivot.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2509_SOURCE_REGISTER.csv",
    "constructor_audit": OUT / "P8_Y5_NO_SHADOW_2509_PARENT_CONSTRUCTOR_EXHAUSTION_AUDIT.csv",
    "pivot_gate": OUT / "P8_Y5_NO_SHADOW_2509_DERIVATION_OR_RESIDUAL_PIVOT_GATE.csv",
    "source_weight_runner": OUT / "P8_Y5_NO_SHADOW_2509_SOURCE_WEIGHT_RESIDUAL_RUNNER_STATUS.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2509_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2509_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2509_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2509_VALIDATION.csv",
}

BRANCH_COPIES = {
    "constructor_audit": LOCAL_BOUNDS / "Parent_constructor_exhaustion_audit_2509_NONCLAIM.csv",
    "pivot_gate": BETA_DOCS / "Derivation_or_source_weight_residual_pivot_2509_NONCLAIM.csv",
    "source_weight_runner": QUEUE / "JR2509_SOURCE_WEIGHT_RESIDUAL_RUNNER_STATUS_NONCLAIM.csv",
    "next_target": QUEUE / "JR2509_SOURCE_WEIGHT_RESIDUAL_BOUND_PACK_NEXT.csv",
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
    body: list[str] = []
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


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC2509_00_2508_handoff",
            ROOT / "2508-Y5-R2FR-object-language-no-source-only-slot-proof-or-GR-import-lock.md",
            ["NEXT2508_0_selected", "PARENT_CONSTRUCTOR_EXHAUSTION_OR_RESIDUAL_PIVOT_NEXT", "VAL2508_OVERALL"],
            "2508 selects constructor exhaustion or source-weight residual pivot.",
        ),
        (
            "SRC2509_01_2508_validation",
            OUT / "P8_Y5_BRR545_2508_VALIDATION.csv",
            ["VAL2508_OVERALL", "PASS"],
            "2508 validation passed before 2509 continues the chain.",
        ),
        (
            "SRC2509_02_1904_constructor",
            OUT / "P8_Y5_PARENT_QLOC_1904_PARENT_ACTION_CONSTRUCTOR_EXHAUSTION_ATTEMPT.csv",
            ["CE1904_0_target", "PARENT_ACTION_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED", "IMAGE_MEMBERSHIP_NOT_DERIVED"],
            "1904 already attempted parent constructor exhaustion and refused promotion.",
        ),
        (
            "SRC2509_03_1904_decision",
            OUT / "P8_Y5_PARENT_QLOC_1904_DECISION_LEDGER.csv",
            ["DEC1904_0_constructor", "FINITE_RESIDUAL_BRANCH_RETAINED"],
            "1904 decision retained finite source-weight residuals.",
        ),
        (
            "SRC2509_04_1107_exhaustion",
            OUT / "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
            ["EXH1107_1_chain_rule", "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED"],
            "1107 shows chain-rule zero is exact only after ParentGenerate membership is proved.",
        ),
        (
            "SRC2509_05_1220_typed",
            OUT / "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
            ["PTOL1220_7_verdict", "PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED"],
            "1220 says the typed parent signature remains unsigned.",
        ),
        (
            "SRC2509_06_1236_certificate",
            OUT / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
            ["CERT1236_6_current_verdict", "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED"],
            "1236 writes the typed certificate but refuses to count it as derived.",
        ),
        (
            "SRC2509_07_2033_owner",
            OUT / "P8_Y5_PARENT_QLOC_2033_PARENT_ACTION_OWNER_CERTIFICATE.csv",
            ["OWN2033_7_certificate_verdict", "OWNER_CONTRACT_READY_PARENT_SIGNATURE_MISSING"],
            "2033 compresses local-GR ownership into a missing parent action/variation/current certificate.",
        ),
        (
            "SRC2509_08_2035_exhaustion",
            OUT / "P8_Y5_PARENT_QLOC_2035_EXHAUSTION_GATE.csv",
            ["EXH2035_8_verdict", "QUOTIENT_FACTORISATION_EXHAUSTION_NOT_DERIVED"],
            "2035 rejects quotient-factorisation exhaustion and keeps finite residual sourcing live.",
        ),
        (
            "SRC2509_09_1905_runner",
            OUT / "P8_Y5_PARENT_QLOC_1905_DELTAW_RUNNER_CONTRACT_NONCLAIM.csv",
            ["DWR1905_0_core_vector", "DELTAW_RUNNER_CONTRACT_NONCLAIM_NOT_EXECUTABLE"],
            "1905 stages a finite Delta_w runner contract but leaves it non-executable.",
        ),
        (
            "SRC2509_10_1906_inputs",
            OUT / "P8_Y5_PARENT_QLOC_1906_DELTAW_RUNNER_INPUT_FILL_NONCLAIM.csv",
            ["DWI1906_0_parent_zero_or_values", "DELTAW_RUNNER_INPUTS_NOT_EXECUTABLE_NONCLAIM"],
            "1906 identifies missing Delta_w runner inputs.",
        ),
        (
            "SRC2509_11_1907_acquisition",
            OUT / "P8_Y5_PARENT_QLOC_1907_DELTAW_INPUT_ACQUISITION_LEDGER_NONCLAIM.csv",
            ["DWA1907_0_delta_w_species", "DELTAW_INPUT_ACQUISITION_NONCLAIM_NOT_EXECUTABLE"],
            "1907 gives the acquisition ledger for the finite residual branch.",
        ),
    ]
    rows: list[dict[str, Any]] = []
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
                source_pass=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def constructor_audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CEA2509_0_target",
            "constructor exhaustion target",
            "Coeff_active_source subset Image(ParentGenerate[q(Phi),theta_rep,topological/universal data]) and no independent source-only coefficient algebra exists.",
            "TARGET_SHARP",
            "Would make w_A/kappa_A unformable, not merely small.",
            "not_signed",
        ),
        (
            "CEA2509_1_normal_form",
            "single parent action normal form",
            "S_parent=S_geom+S_hidden+S_matter[q(Phi),Psi,theta]+S_boundary[q(Phi)] contains no w_A S_A slot.",
            "EXACT_IF_PARENT_DERIVED",
            "Current corpus has candidate normal forms, not a derived parent object.",
            "conditional_only",
        ),
        (
            "CEA2509_2_chain_rule",
            "chain-rule zero inside generated image",
            "If c=cbar(q(Phi),theta) and Dq[v_label]=Dtheta[v_label]=0, then Lie_v_label c=0.",
            "EXACT_CONDITIONAL_THEOREM",
            "Algebra is solid but only after membership in Image(ParentGenerate) is proved.",
            "conditional_only",
        ),
        (
            "CEA2509_3_membership",
            "ParentGenerate membership",
            "Every coefficient that reaches source, clocks, masses, WEP, R10, PPN and readout lies in Image(ParentGenerate).",
            "IMAGE_MEMBERSHIP_NOT_DERIVED",
            "This is the core missing primitive-to-parent construction.",
            "core_gap",
        ),
        (
            "CEA2509_4_no_extension",
            "no hidden/marker extension",
            "No hidden invariant, material marker, boundary class, domain selector or readout label extends Coeff_active_source.",
            "NO_EXTENSION_NOT_DERIVED",
            "Surviving scalar/marker countermodels can still feed source coefficients.",
            "core_gap",
        ),
        (
            "CEA2509_5_action_scale_readout",
            "action-scale and readout stability",
            "One action measure/current owner and typed readout/EFT maps preserve the coefficient domain after variation.",
            "ACTION_SCALE_READOUT_NOT_DERIVED",
            "Tree-level grammar is not claim-grade without this.",
            "core_gap",
        ),
        (
            "CEA2509_6_verdict",
            "2509 constructor verdict",
            "Current MTS evidence does not derive constructor exhaustion from primitives beyond the already-audited conditional contracts.",
            "PARENT_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED_PIVOT_REQUIRED",
            "2508 loop guard triggers: stop repeating no-source-slot derivations and pivot to finite residual bounds.",
            "claim_blocked",
        ),
    ]
    return [
        base_row(
            audit_id=audit_id,
            clause=clause,
            formal_statement=statement,
            status=status,
            implication=implication,
            live_status=live_status,
        )
        for audit_id, clause, statement, status, implication, live_status in specs
    ]


def pivot_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("PIV2509_0_repeat_guard", "no-source-slot loop guard", "Do not repeat 1695/1886/1895/1903/2508 unless a new ParentGenerate primitive construction is supplied.", "TRIGGERED", "prevents pseudo-progress"),
        ("PIV2509_1_derivation_route", "constructor exhaustion from primitives", "Requires parent-derived sorted domain, constructor image, no-extension theorem, action-scale owner and readout stability.", "FAILED_CURRENT_EVIDENCE", "no live parent signature"),
        ("PIV2509_2_residual_route", "finite source-weight residual branch", "Use Delta_w/beta_w/J_A/readout transfer residuals with WEP/R10/PPN/clock/orbital projections.", "SELECTED_NEXT", "turns coupling gap into testable interface"),
        ("PIV2509_3_local_label", "local-GR label", "Local EH coefficients remain GR/EH import plus source-weight residual interface.", "RETAINED_NONCLAIM", "no local GR/Newton claim"),
    ]
    return [
        base_row(gate_id=gate_id, gate=gate, rule=rule, status=status, implication=implication)
        for gate_id, gate, rule, status, implication in specs
    ]


def source_weight_runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("SWR2509_0_core_vector", "Delta_w_eff", "P_perp(Delta_w_species+c_A_current+hidden_marker+J_NH+Delta_mu_projector)", "MISSING_PARENT_VALUES_OR_THEOREM_ZERO", "core source-weight vector"),
        ("SWR2509_1_WEP", "eta_TiPt", "tau_WEP K_WEP dot Delta_w_eff", "MISSING_MATERIAL_TENSOR_TAU_AND_PARENT_VALUES", "MICROSCOPE/WEP projection"),
        ("SWR2509_2_R10", "alpha_Delta_w(lambda)", "tau_R10(lambda) K_R10(lambda) Qbar dot Delta_w_eff", "MISSING_R10_KERNEL_BOUND_CURVE_AND_PARENT_VALUES", "short-range/R10 projection"),
        ("SWR2509_3_PPN", "Delta_PPN_source", "M_PPN dot Delta_w_eff plus retained legs", "MISSING_OPERATOR_MATRIX_AND_GR_LIMIT_MATCH", "PPN projection"),
        ("SWR2509_4_clock_orbit", "clock/orbital residual", "K_clock dot Delta_w_eff; K_orbit dot Delta_w_eff", "MISSING_CLOCK_ORBITAL_KERNELS", "clock and orbital projection"),
        ("SWR2509_5_no_cancellation", "absolute envelope", "sum absolute components unless parent identity or sourced covariance proves cancellation", "POLICY_WRITTEN_NONCLAIM", "no-cancellation guard"),
        ("SWR2509_6_verdict", "source-weight runner", "runner is not executable until parent values/theorem-zero and arena kernels are source-backed", "RUNNER_STATUS_NONEXECUTABLE_NEXT_TARGET", "2509b/2510 should fill real inputs"),
    ]
    return [
        base_row(
            runner_id=runner_id,
            quantity=quantity,
            formula=formula,
            current_status=status,
            role=role,
            score_ready=False,
            valid_prediction_row=False,
        )
        for runner_id, quantity, formula, status, role in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2509_0_constructor",
            "DO_NOT_PROMOTE_CONSTRUCTOR_EXHAUSTION",
            "The exact route is known, but ParentGenerate membership, no-extension/no-marker closure, action-scale owner and readout stability are not derived.",
            "selected",
        ),
        (
            "DEC2509_1_not_circling",
            "LOOP_GUARD_ENFORCED",
            "This checkpoint satisfies the 2508 loop guard: the no-source-slot route is not repeated again as if new.",
            "selected",
        ),
        (
            "DEC2509_2_pivot",
            "PIVOT_TO_SOURCE_WEIGHT_RESIDUAL_BOUND_PACK",
            "Since the derivation-first door did not open, the coupling gap now moves to explicit Delta_w/beta_w/readout residual bounds.",
            "selected",
        ),
        (
            "DEC2509_3_project_meaning",
            "COUPLING_GAP_IS_TESTABLE_NOT_HIDDEN",
            "MTS local-GR ownership remains blocked, but the obstruction is now a measurable source-weight residual interface rather than a vague missing coupling.",
            "selected",
        ),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2509_0_selected",
            selection_status="selected",
            target_file="2510-Y5-R2FR-source-weight-residual-bound-pack-WEP-R10-PPN-clock-orbit.md",
            target_script="scripts/Y5_R2FR_source_weight_residual_bound_pack_WEP_R10_PPN_clock_orbit_2510.py",
            objective="build the finite source-weight residual bound pack: Delta_w_eff component schema, WEP/R10/PPN/clock/orbit projection requirements, real-source acquisition ledger, no-cancellation policy, and nonclaim runner dry-run",
            success_condition="each residual has units, source/projection requirement, arena link, score_ready=false unless values and kernels are real; no placeholders can pass",
            do_not_do="do not reattempt no-source-slot proof, do not claim local GR, do not absorb relative weights into measured G, do not score placeholder rows, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2509_1_future_derivation_reentry",
            selection_status="reentry_only_if_new_source",
            target_file="2510b-Y5-R2FR-parent-generate-primitive-source-hunt.md",
            target_script="scripts/Y5_R2FR_parent_generate_primitive_source_hunt_2510b.py",
            objective="only reopen derivation-first if a new corpus source supplies a primitive ParentGenerate construction or sorted parent-domain certificate",
            success_condition="new source path proves parent constructor image from MTS primitives rather than restating the existing grammar",
            do_not_do="do not restate 1904/2508 conditionals as fresh progress",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("constructor_audit", OUTPUTS["constructor_audit"], BRANCH_COPIES["constructor_audit"]),
        ("pivot_gate", OUTPUTS["pivot_gate"], BRANCH_COPIES["pivot_gate"]),
        ("source_weight_runner", OUTPUTS["source_weight_runner"], BRANCH_COPIES["source_weight_runner"]),
        ("next_target", OUTPUTS["next_target"], BRANCH_COPIES["next_target"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=f"COPY2509_{copy_id}", source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                return False
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        validations.append(base_row(check_id=check_id, status="PASS" if status else "FAIL", notes=notes, detail=detail))

    add("VAL2509_00_sources_exist", all(row["path_exists"] for row in rows_by_name["source_register"]), "all cited source paths exist")
    add("VAL2509_01_source_needles", all(row["source_pass"] for row in rows_by_name["source_register"]), "all required source needles are present")

    audit_statuses = {row["status"] for row in rows_by_name["constructor_audit"]}
    add(
        "VAL2509_02_constructor_verdict",
        "PARENT_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED_PIVOT_REQUIRED" in audit_statuses,
        "constructor exhaustion is not promoted",
    )

    pivot_statuses = {row["status"] for row in rows_by_name["pivot_gate"]}
    add(
        "VAL2509_03_pivot_gate",
        "TRIGGERED" in pivot_statuses and "SELECTED_NEXT" in pivot_statuses,
        "loop guard and residual pivot are active",
    )

    runner_statuses = {row["current_status"] for row in rows_by_name["source_weight_runner"]}
    add(
        "VAL2509_04_runner_status",
        "RUNNER_STATUS_NONEXECUTABLE_NEXT_TARGET" in runner_statuses and "MISSING_PARENT_VALUES_OR_THEOREM_ZERO" in runner_statuses,
        "source-weight runner remains nonclaim and non-executable",
    )

    decision_text = " ".join(row["decision"] for row in rows_by_name["decision_ledger"])
    add("VAL2509_05_decision", "PIVOT_TO_SOURCE_WEIGHT_RESIDUAL_BOUND_PACK" in decision_text, "decision ledger selects residual bound pack")
    add("VAL2509_06_next_target", any(row["route_id"] == "NEXT2509_0_selected" for row in rows_by_name["next_target"]), "2510 residual bound pack target selected")
    add("VAL2509_07_no_claim_flags", no_claim_flags(rows_by_name), "all generated rows keep valid_for_claim=false and claim_allowed=false")
    add("VAL2509_08_branch_copies", all(row["copied"] for row in rows_by_name["branch_copies"]), "branch copies were written")

    formalization_artifacts: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*2509*", "*P8_Y5_NO_SHADOW_2509*", "*JR2509*"):
            formalization_artifacts.extend(path for path in FORMALIZATION.rglob(pattern) if path.is_file())
    add("VAL2509_09_no_formalization_artifacts", not formalization_artifacts, "no 2509 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for path in OUTPUTS.values():
        if path == OUTPUTS["validation"]:
            continue
        parsed, count, detail = csv_rows_parse(path)
        add(f"VAL2509_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", detail)

    for key, path in BRANCH_COPIES.items():
        parsed, count, detail = csv_rows_parse(path)
        add(f"VAL2509_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", detail)

    remove_pycache()
    add("VAL2509_10_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts pycache removed")

    overall = all(row["status"] == "PASS" for row in validations)
    add(
        "VAL2509_OVERALL",
        overall,
        "2509 enforces constructor-exhaustion loop guard, rejects current derivation, and pivots to source-weight residual bound pack",
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2509 Y5 R2FR Parent Constructor Exhaustion From MTS Primitives Or Source Weight Residual Pivot

## Current Verdict

2509 closes the no-source-slot derivation loop for now.

The exact constructor-exhaustion theorem is known:

`Coeff_active_source subset Image(ParentGenerate[q(Phi), theta_rep, topological/universal data])`.

If MTS derived that image from primitives, source-only coefficients like `w_A`, `kappa_A`, hidden marker weights, and readout source multipliers would be unformable before variation.

But the current corpus does not derive `ParentGenerate` membership. The older 1107, 1220, 1236, 1904, 2033 and 2035 chains all agree: the theorem is sharp, but the parent constructor/domain certificate is unsigned.

Therefore the 2508 loop guard fires:

**stop repeating the no-source-only proof** unless a genuinely new primitive constructor source appears.

The next serious step is empirical/theory-interface work: build the finite source-weight residual bound pack for WEP, R10, PPN, clocks and orbital systems. This does not make MTS local GR. It makes the coupling obstruction explicit and testable.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "source_pass", "role", "valid_for_claim"])}

## Constructor Exhaustion Audit

{md_table(rows_by_name["constructor_audit"], ["audit_id", "clause", "formal_statement", "status", "implication", "live_status", "valid_for_claim"])}

## Derivation Or Residual Pivot Gate

{md_table(rows_by_name["pivot_gate"], ["gate_id", "gate", "rule", "status", "implication", "valid_for_claim"])}

## Source Weight Residual Runner Status

{md_table(rows_by_name["source_weight_runner"], ["runner_id", "quantity", "formula", "current_status", "role", "score_ready", "valid_prediction_row", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision_ledger"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["check_id", "status", "notes", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "constructor_audit": constructor_audit_rows(),
        "pivot_gate": pivot_gate_rows(),
        "source_weight_runner": source_weight_runner_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()

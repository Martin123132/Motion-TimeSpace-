from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT = "1951"
ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1951-Y5-R2FR-STF-response-functional-or-common-mode-router.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1951_VALIDATION.csv"

SOURCE_FILES = {
    "1950_doc": {
        "path": ROOT / "1950-Y5-R2FR-dimensionless-STF-slip-source-or-zero-theorem.md",
        "needles": ["STF1950_4_zero_theorem_condition", "SRC1950_1_S_TF_direct", "NEXT1950_0_primary"],
    },
    "1950_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1950_VALIDATION.csv",
        "needles": ["VAL1950_OVERALL", "PASS"],
    },
    "1950_decomposition": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1950_STF_DECOMPOSITION_AND_ZERO_ROUTE.csv",
        "needles": ["STF1950_2_hessian_STF_channel", "STF1950_3_kernel_STF_channel"],
    },
    "1950_source": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1950_DIMENSIONLESS_STF_SOURCE_LEDGER.csv",
        "needles": ["SRC1950_1_S_TF_direct", "MISSING_DIRECT_DIMENSIONLESS_STF_RESPONSE"],
    },
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def base_row(row_id: str) -> dict[str, object]:
    return {
        "branch": BRANCH,
        "row_id": row_id,
        "valid_for_claim": False,
        "public_claim": False,
        "created_utc": timestamp(),
    }


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, spec in SOURCE_FILES.items():
        path = spec["path"]
        needles = spec["needles"]
        exists = path.exists()
        content = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        missing_needles = [needle for needle in needles if needle not in content]
        row = base_row(source_id)
        row.update(
            {
                "source_path": str(path),
                "purpose": "1951 STF response functional or common-mode router",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing_needles else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing_needles),
            }
        )
        rows.append(row)
    return rows


def response_functional_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    entries = [
        (
            "FUNC1951_0_radial_STF_basis",
            "Any static O(3)-covariant spatial residual has exactly one Cassini-dangerous radial STF coefficient.",
            "Delta_ij^extra(r)=A_eff(r) delta_ij + B_eff(r) N_ij, N_ij=n_i n_j-delta_ij/3",
            "P_TF[Delta_ij^extra]=B_eff(r) N_ij",
            "DERIVED_DECOMPOSITION_NONCLAIM",
            "This is progress: the dangerous channel is one scalar radial profile, not an uncontrolled tensor cloud.",
        ),
        (
            "FUNC1951_1_hessian_amplitude_law",
            "For a scalar Hessian channel the STF amplitude is exactly f''-f'/r.",
            "P_TF[partial_i partial_j f]=(f''-f'/r) N_ij",
            "B_H(r)=f''(r)-f'(r)/r",
            "DERIVED_LOCAL_AMPLITUDE_LAW",
            "The zero-proof route is now the double-zero law B_H=0, not a vague plateau axiom.",
        ),
        (
            "FUNC1951_2_dimensionless_STF_response",
            "Cassini-visible slip is the normalized readout of the radial STF amplitude.",
            "S_TF[b]=Pi_Cassini[B_eff(r) N_ij;b]",
            "Pi_Cassini includes local inverse operator, light-path projection, and normalization by the solar potential policy",
            "FUNCTIONAL_FORM_BUILT_NOT_NUMERIC",
            "The live blocker is now the missing Pi_Cassini kernel/norm and B_eff profile, not the concept of the observable.",
        ),
        (
            "FUNC1951_3_norm_bound",
            "A nonclaim sufficient bound is available once the readout norm and radial amplitude envelope are sourced.",
            "abs(S_TF) <= ||W_STF||_1 sup_r abs(B_eff(r))",
            "acceptance if ||W_STF||_1 sup|B_eff| <= 6.7e-5",
            "BOUND_TEMPLATE_BUILT_NOT_SOURCED",
            "This gives a concrete data/acquisition target for a Cassini smoke pass without pretending the numbers exist.",
        ),
        (
            "FUNC1951_4_zero_theorem",
            "The parent-zero theorem must force B_eff(r)=0 after all local, boundary, and kernel projections.",
            "B_eff = B_H + B_kernel + B_boundary + B_anisotropic_source = 0",
            "sufficient clauses: f''=f'/r, bounded/localized branch, kernel STF silence, boundary STF silence, source-worldtube anisotropy silence",
            "ZERO_THEOREM_SHAPE_EXACT_BUT_UNSIGNED",
            "If this theorem is signed, Cassini gamma is passed by derivation; until then it remains blocked.",
        ),
        (
            "FUNC1951_5_common_mode_router",
            "The common mode A_eff(r) is not a Cassini-gamma STF source and must be routed to Newtonian/effective-G gates.",
            "Delta_ij^common=A_eff(r) delta_ij; P_TF[Delta_ij^common]=0",
            "route to Xi_N, deltaG_eff/G, cosmology/local matching, and orbital residual gates",
            "COMMON_MODE_ROUTED_NOT_CLAIMED",
            "This prevents us from cheating by hiding a Newtonian problem inside a gamma pass.",
        ),
    ]
    for row_id, statement, math_form, output, status, implication in entries:
        row = base_row(row_id)
        row.update(
            {
                "statement": statement,
                "math_form": math_form,
                "output": output,
                "status": status,
                "implication": implication,
            }
        )
        rows.append(row)
    return rows


def input_ledger_rows() -> list[dict[str, object]]:
    entries = [
        (
            "IN1951_0_gamma_bound_policy",
            "gamma_bound_policy",
            "private conservative Cassini screening threshold",
            "6.700000e-05",
            "dimensionless",
            "NUMERIC_POLICY_AVAILABLE_NONCLAIM",
            "SRC1950_0_gamma_bound_policy",
        ),
        (
            "IN1951_1_B_eff_profile",
            "B_eff(r)",
            "radial coefficient of the projected inverse-operator STF residual",
            "MISSING",
            "dimensionless after inverse local operator",
            "MISSING_PARENT_STF_AMPLITUDE_PROFILE",
            "FUNC1951_0_radial_STF_basis",
        ),
        (
            "IN1951_2_W_STF_norm",
            "||W_STF||_1",
            "Cassini light-path/readout operator norm for the radial STF basis",
            "MISSING",
            "inverse of B_eff units",
            "MISSING_CASSINI_STF_READOUT_NORM",
            "FUNC1951_3_norm_bound",
        ),
        (
            "IN1951_3_S_TF_direct",
            "S_TF",
            "direct dimensionless Cassini-visible STF slip response",
            "MISSING",
            "dimensionless",
            "MISSING_DIRECT_DIMENSIONLESS_STF_RESPONSE",
            "FUNC1951_2_dimensionless_STF_response",
        ),
        (
            "IN1951_4_B_eff_zero_theorem",
            "B_eff=0",
            "parent-signed theorem killing every STF channel after projection",
            "NOT_PARENT_SIGNED",
            "boolean/theorem",
            "MISSING_PARENT_SIGNED_STF_ZERO_THEOREM",
            "FUNC1951_4_zero_theorem",
        ),
        (
            "IN1951_5_A_eff_common_mode",
            "A_eff(r)",
            "gamma-silent common-mode spatial residual routed outside Cassini gamma",
            "MISSING",
            "dimensionless after inverse local operator",
            "MISSING_COMMON_MODE_NEWTONIAN_ROUTING_INPUT",
            "FUNC1951_5_common_mode_router",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, symbol, definition, value, units, status, source_ref in entries:
        row = base_row(row_id)
        row.update(
            {
                "symbol": symbol,
                "definition": definition,
                "value": value,
                "units": units,
                "status": status,
                "source_ref": source_ref,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        (
            "RUN1951_0_direct_functional",
            "S_TF=Pi_Cassini[B_eff N_ij]",
            "abs(S_TF) <= 6.7e-5",
            "MISSING_DIRECT_DIMENSIONLESS_STF_RESPONSE",
            "BLOCKED_MISSING_S_TF",
            "numeric S_TF or sourced B_eff plus W_STF norm",
        ),
        (
            "RUN1951_1_norm_bound",
            "abs(S_TF) <= ||W_STF||_1 sup|B_eff|",
            "||W_STF||_1 sup|B_eff| <= 6.7e-5",
            "MISSING_PARENT_STF_AMPLITUDE_PROFILE;MISSING_CASSINI_STF_READOUT_NORM",
            "BLOCKED_MISSING_BOUND_FACTORS",
            "source W_STF norm and B_eff envelope",
        ),
        (
            "RUN1951_2_zero_theorem",
            "B_eff=0 implies S_TF=0",
            "0 <= 6.7e-5",
            "MISSING_PARENT_SIGNED_STF_ZERO_THEOREM",
            "WOULD_PASS_IF_PARENT_SIGNED_BLOCKED",
            "parent proof of Hessian/kernel/boundary/source STF silence",
        ),
        (
            "RUN1951_3_common_mode_router",
            "P_TF[A_eff delta_ij]=0",
            "Cassini gamma silent; not a local-GR pass",
            "MISSING_COMMON_MODE_NEWTONIAN_ROUTING_INPUT",
            "ROUTED_TO_NEWTONIAN_EFFECTIVE_G_GATES",
            "build Xi_N/deltaG_eff input rather than treating common mode as solved",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, prediction, acceptance_rule, missing_inputs, runner_status, required_fix in entries:
        row = base_row(row_id)
        row.update(
            {
                "prediction": prediction,
                "acceptance_rule": acceptance_rule,
                "missing_inputs": missing_inputs,
                "runner_status": runner_status,
                "required_fix": required_fix,
            }
        )
        rows.append(row)
    return rows


def common_mode_router_rows() -> list[dict[str, object]]:
    entries = [
        (
            "CM1951_0_gamma_silence",
            "A_eff(r) delta_ij",
            "Cassini gamma STF gate",
            "P_TF[A_eff delta_ij]=0",
            "PASS_NONCLAIM",
            "common mode is not counted as Cassini slip",
        ),
        (
            "CM1951_1_newtonian_gate",
            "A_eff(r), Phi_eff(r)",
            "Newtonian acceleration/effective G",
            "Xi_N(r)=delta a_r/a_GR or deltaG_eff/G",
            "OPEN_ROUTED",
            "needs a separate local acceleration/orbital bound",
        ),
        (
            "CM1951_2_cosmology_matching",
            "A_eff local/global split",
            "FLRW/local matching",
            "local common-mode branch must not double-count cosmology memory",
            "OPEN_ROUTED",
            "prevents gamma success from becoming a fake full-GR reduction",
        ),
        (
            "CM1951_3_orbital_gate",
            "radial common-mode force residual",
            "perihelion/range/orbital residuals",
            "route to PPN beta/orbital residual vector after Xi_N exists",
            "OPEN_ROUTED",
            "full local GR still needs this after gamma",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, channel, target_gate, rule, status, implication in entries:
        row = base_row(row_id)
        row.update(
            {
                "channel": channel,
                "target_gate": target_gate,
                "rule": rule,
                "status": status,
                "implication": implication,
            }
        )
        rows.append(row)
    return rows


def blocker_rows() -> list[dict[str, object]]:
    entries = [
        (
            "BLK1951_0_B_eff_profile",
            "B_eff(r) is not derived from the parent action.",
            "the response functional cannot be evaluated",
            "derive B_eff from parent residual operator or prove B_eff=0",
        ),
        (
            "BLK1951_1_readout_norm",
            "The Cassini STF readout kernel/norm W_STF is not sourced.",
            "the norm-bound branch cannot be scored",
            "derive/source W_STF for the same convention used by the gamma policy",
        ),
        (
            "BLK1951_2_zero_theorem",
            "The parent action has not signed Hessian/kernel/boundary/source STF silence.",
            "the theorem-zero branch remains only a shape, not a proof",
            "prove f''=f'/r plus boundary/kernel/source STF silence or demote to finite bound",
        ),
        (
            "BLK1951_3_common_mode",
            "A_eff common-mode residual is not yet routed into a numeric Newtonian gate.",
            "full local GR remains open even if gamma is solved",
            "build Xi_N/deltaG_eff common-mode response runner",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, blocker, effect, required_fix in entries:
        row = base_row(row_id)
        row.update({"blocker": blocker, "effect": effect, "required_fix": required_fix})
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        (
            "CG1951_0_STF_functional_built",
            "A dimensionless STF response functional exists.",
            "PASS_NONCLAIM",
            "S_TF is now an operator readout of B_eff, not an undefined placeholder.",
        ),
        (
            "CG1951_1_hessian_amplitude_law",
            "The scalar Hessian STF amplitude law is derived.",
            "PASS_NONCLAIM",
            "B_H=f''-f'/r gives the exact double-zero target.",
        ),
        (
            "CG1951_2_STF_numeric_or_bound",
            "MTS supplies numeric or bounded S_TF below the Cassini policy threshold.",
            "FAIL_BLOCKED",
            "B_eff profile and W_STF norm are missing.",
        ),
        (
            "CG1951_3_parent_zero_theorem",
            "MTS parent proves B_eff=0 and hence S_TF=0.",
            "FAIL_BLOCKED",
            "the zero theorem is shaped but unsigned.",
        ),
        (
            "CG1951_4_common_mode_solved",
            "Gamma-silent common mode is locally GR-safe.",
            "FAIL_BLOCKED",
            "A_eff still needs Newtonian/effective-G/orbital gates.",
        ),
        (
            "CG1951_5_Cassini_pass",
            "MTS passes the Cassini gamma gate.",
            "FAIL_BLOCKED",
            "functional exists, but no numeric/bounded or theorem-zero S_TF exists.",
        ),
        (
            "CG1951_6_local_GR_reduction",
            "MTS derives local GR/Newton.",
            "FAIL_BLOCKED",
            "gamma and common-mode Newtonian branches remain open.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, claim, status, reason in entries:
        row = base_row(row_id)
        row.update({"claim": claim, "status": status, "reason": reason})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    entries = [
        (
            "DEC1951_0_progress",
            "STF_RESPONSE_FUNCTIONAL_BUILT_NOT_NUMERIC",
            "the missing Cassini object has been reduced to B_eff(r), W_STF, and/or a parent B_eff=0 theorem",
            "try to derive B_eff=0 from parent locality/descent first; if not, source W_STF and bound B_eff",
        ),
        (
            "DEC1951_1_next",
            "ATTEMPT_PARENT_BEFF_ZERO_OR_SOURCE_FIRST_BOUND",
            "the cleanest route is proof of the radial STF double-zero; the fallback is a finite bound",
            "build 1952 B_eff zero theorem attempt with explicit Hessian/kernel/boundary/source clauses",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base_row(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row("NEXT1951_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1952-Y5-R2FR-B_eff-zero-theorem-or-STF-bound-first-fill.md",
            "target_script": "scripts/Y5_R2FR_B_eff_zero_theorem_or_STF_bound_first_fill_1952.py",
            "objective": "prove B_eff=0 from parent Hessian/kernel/boundary/source silence, or create the first finite bound rows for B_eff and W_STF",
            "acceptance_output": "parent-signed zero theorem, or nonclaim bound factors with explicit missing sources",
            "nonclaim_rule": "no Cassini/local-GR claim unless B_eff=0 is parent-signed or abs(S_TF) is evaluated below a sourced bound",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base_row("SNAP1951_0_project_position")
    row.update(
        {
            "strongest_result": "Cassini gamma residual is now a concrete STF response functional S_TF=Pi_Cassini[B_eff N_ij].",
            "what_improved": "the next derivation target is the exact radial amplitude B_eff, with hessian law B_H=f''-f'/r",
            "still_missing": "parent-derived B_eff profile, W_STF readout norm, or parent-signed B_eff=0 theorem",
            "claim_status": "Cassini/local-GR public claims remain blocked, but the route is narrower and more derivable",
        }
    )
    return [row]


CSV_OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1951_SOURCE_REGISTER.csv",
    "response_functional": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1951_STF_RESPONSE_FUNCTIONAL.csv",
    "input_ledger": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1951_STF_INPUT_LEDGER.csv",
    "runner_update": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1951_STF_RUNNER_UPDATE.csv",
    "common_mode_router": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1951_COMMON_MODE_ROUTER.csv",
    "blocker_ledger": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1951_BLOCKER_LEDGER.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1951_CLAIM_GATE.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1951_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1951_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1951_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "STF_RESPONSE_FUNCTIONAL_1951_NONCLAIM.csv",
    "acquisition_queue": RAB_QUEUE / "JR1951_BEFF_ZERO_THEOREM_OR_STF_BOUND_QUEUE.csv",
}


def build_rows_by_name() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base_row("SW1951_0_nonclaim_weight"),
            "artifact": "1951 STF response functional",
            "weight": "DERIVATION_TARGET_NOT_EVIDENCE",
            "reason": "functional form is useful, but no numeric S_TF or parent zero proof exists",
        }
    ]
    acquisition_queue = [
        {
            **base_row("AQ1951_0_parent_zero_attempt"),
            "target": "B_eff=0 theorem",
            "needed_inputs": "parent Hessian law; kernel STF silence; boundary STF silence; source-worldtube anisotropy silence",
            "priority": "HIGH",
            "claim_rule": "only theorem-signed rows can unlock zero branch",
        },
        {
            **base_row("AQ1951_1_bound_fallback"),
            "target": "finite S_TF bound",
            "needed_inputs": "B_eff envelope; W_STF norm; gamma policy normalization",
            "priority": "MEDIUM",
            "claim_rule": "bound branch remains nonclaim until all factors are sourced and numeric",
        },
    ]
    return {
        "source_register": source_register_rows(),
        "response_functional": response_functional_rows(),
        "input_ledger": input_ledger_rows(),
        "runner_update": runner_rows(),
        "common_mode_router": common_mode_router_rows(),
        "blocker_ledger": blocker_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
        "snapshot": snapshot_rows(),
        "source_weight": source_weight,
        "acquisition_queue": acquisition_queue,
    }


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, object]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": False,
        "public_claim": False,
    }


def formalization_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = ("1951-", "*_1951_*", "*Y5*1951*", "*VAL1951*", "*P8*1951*")
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if any(Path(path.name).match(pattern) for pattern in patterns):
            count += 1
    return count


def validate_outputs(rows_by_name: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"])
    rows.append(validation_row("VAL1951_00_sources", "PASS" if sources_ok else "FAIL", "all local source paths exist and needles found"))

    functional_ok = any(row["row_id"] == "FUNC1951_2_dimensionless_STF_response" and row["status"] == "FUNCTIONAL_FORM_BUILT_NOT_NUMERIC" for row in rows_by_name["response_functional"])
    rows.append(validation_row("VAL1951_01_functional", "PASS" if functional_ok else "FAIL", "dimensionless STF response functional recorded"))

    amplitude_ok = any(row["row_id"] == "FUNC1951_1_hessian_amplitude_law" and "f''(r)-f'(r)/r" in str(row["output"]) for row in rows_by_name["response_functional"])
    rows.append(validation_row("VAL1951_02_amplitude_law", "PASS" if amplitude_ok else "FAIL", "hessian amplitude law recorded"))

    input_ok = any(row["symbol"] == "B_eff(r)" and row["status"] == "MISSING_PARENT_STF_AMPLITUDE_PROFILE" for row in rows_by_name["input_ledger"])
    rows.append(validation_row("VAL1951_03_input_ledger", "PASS" if input_ok else "FAIL", "B_eff missing input explicit"))

    runner_statuses = {row["runner_status"] for row in rows_by_name["runner_update"]}
    runner_ok = {"BLOCKED_MISSING_S_TF", "BLOCKED_MISSING_BOUND_FACTORS", "WOULD_PASS_IF_PARENT_SIGNED_BLOCKED", "ROUTED_TO_NEWTONIAN_EFFECTIVE_G_GATES"}.issubset(runner_statuses)
    rows.append(validation_row("VAL1951_04_runner", "PASS" if runner_ok else "FAIL", "runner branches block or route correctly"))

    common_ok = any(row["row_id"] == "CM1951_1_newtonian_gate" and row["status"] == "OPEN_ROUTED" for row in rows_by_name["common_mode_router"])
    rows.append(validation_row("VAL1951_05_common_mode_router", "PASS" if common_ok else "FAIL", "common mode routed to Newtonian/effective-G gate"))

    gates = rows_by_name["claim_gate"]
    claim_ok = any(row["row_id"] == "CG1951_0_STF_functional_built" and row["status"] == "PASS_NONCLAIM" for row in gates) and all(
        row["status"] != "PASS_CLAIM" for row in gates
    )
    rows.append(validation_row("VAL1951_06_claim_gates", "PASS" if claim_ok else "FAIL", "functional passes only as nonclaim; claims remain blocked"))

    blockers_ok = len(rows_by_name["blocker_ledger"]) >= 4 and all(row["required_fix"] for row in rows_by_name["blocker_ledger"])
    rows.append(validation_row("VAL1951_07_blockers", "PASS" if blockers_ok else "FAIL", "blockers have explicit required fixes"))

    next_ok = rows_by_name["next_target"][0]["target_doc"] == "1952-Y5-R2FR-B_eff-zero-theorem-or-STF-bound-first-fill.md"
    rows.append(validation_row("VAL1951_08_next_target", "PASS" if next_ok else "FAIL", "1952 B_eff target selected"))

    claim_flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in rows_by_name.values() for row in table)
    rows.append(validation_row("VAL1951_09_claim_flags_safe", "PASS" if claim_flags_ok else "FAIL", "claim flags all false"))

    csv_parse_ok = True
    for path in CSV_OUTPUTS.values():
        parsed = read_csv(path)
        if not parsed:
            csv_parse_ok = False
    rows.append(validation_row("VAL1951_10_csv_parse", "PASS" if csv_parse_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache_path = ROOT / "scripts" / "__pycache__"
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    rows.append(validation_row("VAL1951_11_pycache_absent", "PASS" if not pycache_path.exists() else "FAIL", "scripts __pycache__ absent"))

    formalization_count = formalization_artifact_count()
    rows.append(
        validation_row(
            "VAL1951_12_formalization_untouched",
            "PASS" if formalization_count == 0 else "FAIL",
            f"formalization_1951_artifact_count={formalization_count}",
        )
    )

    overall_status = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1951_OVERALL", overall_status, "1951 STF response functional or common-mode router"))
    return rows


def markdown_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    lines = [header, separator]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(rows_by_name: dict[str, list[dict[str, object]]], validation_rows: list[dict[str, object]]) -> None:
    sections = [
        ("Source Register", rows_by_name["source_register"]),
        ("STF Response Functional", rows_by_name["response_functional"]),
        ("Input Ledger", rows_by_name["input_ledger"]),
        ("Runner Update", rows_by_name["runner_update"]),
        ("Common Mode Router", rows_by_name["common_mode_router"]),
        ("Blocker Ledger", rows_by_name["blocker_ledger"]),
        ("Claim Gate", rows_by_name["claim_gate"]),
        ("Decision Ledger", rows_by_name["decision_ledger"]),
        ("Next Target", rows_by_name["next_target"]),
        ("Project Status Snapshot", rows_by_name["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1951 Y5 R2FR: STF Response Functional Or Common-Mode Router",
        "",
        "Private checkpoint. This narrows the Cassini/local-GR branch without making a public claim.",
        "",
        "Main result: the gamma-dangerous object is a concrete radial STF response functional, `S_TF=Pi_Cassini[B_eff(r) N_ij]`; the scalar Hessian part obeys the exact amplitude law `B_H=f''-f'/r`; common-mode residuals are routed out of Cassini gamma and into Newtonian/effective-G gates.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    rows_by_name = build_rows_by_name()
    for name, path in CSV_OUTPUTS.items():
        write_csv(path, rows_by_name[name])
    validation_rows = validate_outputs(rows_by_name)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(rows_by_name, validation_rows)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1951_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

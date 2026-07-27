from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2839-Y5-R2FR-finite-RAB-residual-green-kernel-normalization-or-first-source-backed-row-under-AX1090.md"

SRC_2838_NEXT = RESIDUALS / "P8_Y5_R2FR_2838_NEXT_TARGET.csv"
SRC_2838_SIGNATURE = RESIDUALS / "P8_Y5_R2FR_2838_SECOND_CLASS_SIGNATURE_AUDIT.csv"
SRC_2838_CALCULUS = RESIDUALS / "P8_Y5_R2FR_2838_AUXILIARY_ELIMINATION_CALCULUS.csv"
SRC_2838_EQUATION = RESIDUALS / "P8_Y5_R2FR_2838_FINITE_RAB_RESIDUAL_EQUATION_NONCLAIM.csv"
SRC_2838_ROWS = RESIDUALS / "P8_Y5_R2FR_2838_FINITE_RESIDUAL_ACQUISITION_ROWS_NONCLAIM.csv"
SRC_2838_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2838_VALIDATION.csv"
SRC_2236 = BETA_DOCS / "RAB_AUXILIARY_GRAMMAR_2236_NONCLAIM.csv"
SRC_2240 = ROOT / "2240-Y5-R2FR-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md"
SRC_2259 = ROOT / "2259-Y5-R2FR-RAB-compatibility-object-bridge-or-residual-demotion.md"
SRC_10 = ROOT / "10-observer-map-symplectic-contract.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2839_SOURCE_REGISTER.csv",
    "kernel": RESIDUALS / "P8_Y5_R2FR_2839_GREEN_KERNEL_NORMALIZATION.csv",
    "dimensions": RESIDUALS / "P8_Y5_R2FR_2839_DIMENSIONAL_CONTRACT.csv",
    "source_selector": RESIDUALS / "P8_Y5_R2FR_2839_FIRST_SOURCE_ROW_SELECTOR.csv",
    "projection": RESIDUALS / "P8_Y5_R2FR_2839_ARENA_PROJECTION_CONTRACT.csv",
    "zero_or_source": RESIDUALS / "P8_Y5_R2FR_2839_THEOREM_ZERO_OR_SOURCE_ROW_ATTEMPT.csv",
    "guards": RESIDUALS / "P8_Y5_R2FR_2839_GUARDS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2839_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2839_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2839_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2839_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2839_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "kernel_copy": LOCAL_BOUNDS / "RAB_green_kernel_normalization_2839_NONCLAIM.csv",
    "selector_copy": SOURCE_WEIGHT / "RAB_first_source_row_selector_2839_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2839_green_kernel_or_first_source_row_NEXT.csv",
    "portable_decision": BETA_DOCS / "RAB_GREEN_KERNEL_OR_FIRST_SOURCE_ROW_2839_NONCLAIM.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    needles = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in needles if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2839_0_2838_next", SRC_2838_NEXT, "NEXT2838_0_2839", "2838 selected Green-kernel/source-row normalization"),
        ("SRC2839_1_2838_signature", SRC_2838_SIGNATURE, "SIG2838_1_action_image;SIG2838_6_joint_signature", "2838 parent signature failure"),
        ("SRC2839_2_2838_calculus", SRC_2838_CALCULUS, "CALC2838_3_exact_zero_case;CALC2838_4_finite_case", "2838 exact-conditional and finite fallback algebra"),
        ("SRC2839_3_2838_equation", SRC_2838_EQUATION, "FEQ2838_0_normal_form;FEQ2838_1_green_solution;FEQ2838_2_range", "2838 finite residual equation"),
        ("SRC2839_4_2838_rows", SRC_2838_ROWS, "ACQ2838_0_ZR;ACQ2838_1_MR2;ACQ2838_2_JR;ACQ2838_3_PiR;ACQ2838_4_Rreadout;ACQ2838_5_CAB", "2838 acquisition rows"),
        ("SRC2839_5_2838_validation", SRC_2838_VALIDATION, "VAL2838_OVERALL", "2838 validation"),
        ("SRC2839_6_2236", SRC_2236, "FALL2236_0_ZR;FALL2236_1_MR2;FALL2236_2_JR;FALL2236_3_BR;FALL2236_4_projection", "older finite coefficient fallback"),
        ("SRC2839_7_2240", SRC_2240, "ACQ2240_1_ZR;ACQ2240_2_MR2;ACQ2240_3_JR;ACQ2240_4_BR", "parent protection source queue"),
        ("SRC2839_8_2259", SRC_2259, "DM2259_0_ZR;DM2259_5_projection", "residual demotion queue"),
        ("SRC2839_9_10", SRC_10, "R_AB = ln(T^2 S)", "R_AB dimensionless observer-map definition"),
    ]
    return [source_row(*spec) for spec in specs]


def kernel_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "KER2839_0_static_operator",
            "E_R^finite = -Div(Z_R Grad R_AB) + M_R^2 delta_R + S_R = 0",
            "delta_R := R_AB-C_AB[Q]; S_R := J_R+Pi_R+R_readout",
            "finite residual normal form before arena projection",
            "symbolic_normalization_only",
        ),
        (
            "KER2839_1_normalized_operator",
            "(-Laplace + ell_R^-2) delta_R = -S_R/Z_R",
            "ell_R^2 := Z_R/M_R^2 when Z_R>0 and M_R^2>0",
            "puts all source-amplitude ambiguity into S_R/Z_R",
            "symbolic_normalization_only",
        ),
        (
            "KER2839_2_yukawa_kernel",
            "G_ell(r) = exp(-r/ell_R)/(4*pi*r)",
            "(-Laplace + ell_R^-2) G_ell = delta^3(x)",
            "standard static Green kernel for the normalized finite branch",
            "symbolic_kernel_only",
        ),
        (
            "KER2839_3_solution",
            "delta_R(x) = - integral G_ell(|x-x'|) S_R(x')/Z_R d^3x' + boundary_homogeneous",
            "sign convention follows E_R^finite definition; observable sign must be fixed by the parent source convention",
            "gives the exact source-normalization target for first finite rows",
            "symbolic_kernel_only",
        ),
        (
            "KER2839_4_compact_body",
            "outside a compact body: delta_R(r) = q_R_eff exp(-r/ell_R)/(4*pi*r) + boundary_homogeneous",
            "q_R_eff := - integral_body S_R/Z_R d^3x has length units when R_AB is dimensionless",
            "first arena rows should source q_R_eff and ell_R together, not Z_R alone",
            "symbolic_kernel_only",
        ),
    ]
    return [
        nonclaim(
            {
                "kernel_id": row_id,
                "equation": equation,
                "definition": definition,
                "role": role,
                "status": status,
                "numeric_value_present": False,
                "source_backed": False,
                "control_only": True,
            }
        )
        for row_id, equation, definition, role, status in specs
    ]


def dimension_rows() -> list[dict[str, Any]]:
    specs = [
        ("DIM2839_0_RAB", "R_AB", "dimensionless", "R_AB=ln(T^2 S)", "from observer-map definition", True),
        ("DIM2839_1_ell", "ell_R", "length", "ell_R^2=Z_R/M_R^2", "only meaningful if Z_R and M_R^2 signs/units are sourced", False),
        ("DIM2839_2_source_density", "S_R/Z_R", "length^-2", "matches (-Laplace+ell^-2) delta_R", "needed before point-source reduction", False),
        ("DIM2839_3_point_charge", "q_R_eff", "length", "integral of -S_R/Z_R over compact source volume", "minimal amplitude object for local tests", False),
        ("DIM2839_4_projection", "tau_arena*q_R_eff", "arena dependent", "maps delta_R to alpha_R, gamma-1, clock fraction, or orbital acceleration", "must be separately derived for each arena", False),
    ]
    return [
        nonclaim(
            {
                "dimension_id": row_id,
                "symbol": symbol,
                "unit_contract": unit,
                "derivation_or_definition": definition,
                "caveat": caveat,
                "definition_closed": closed,
                "numeric_value_present": False,
                "source_backed": False,
                "control_only": True,
            }
        )
        for row_id, symbol, unit, definition, caveat, closed in specs
    ]


def source_selector_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SEL2839_0_minimal_pair",
            "first finite row must be a pair: ell_R plus q_R_eff or equivalent source amplitude",
            "Z_R alone cannot predict a local signal; M_R^2 alone only gives a range after normalization; J_R alone has no kernel normalization.",
            "SELECTED_SCHEMA_NOT_FILLED",
            "source ell_R and q_R_eff with units, source path, normalization, and arena projection",
        ),
        (
            "SEL2839_1_ZR",
            "standalone Z_R",
            "insufficient by itself because amplitude requires S_R/Z_R and range requires M_R^2/Z_R.",
            "DEFER_STANDALONE_ROW",
            "may be accepted only as part of a complete normalization pack",
        ),
        (
            "SEL2839_2_MR2",
            "standalone M_R^2",
            "insufficient by itself because ell_R needs Z_R and the sign convention must be fixed.",
            "DEFER_STANDALONE_ROW",
            "may be accepted only with Z_R or direct ell_R evidence",
        ),
        (
            "SEL2839_3_JR_PiR_readout",
            "source terms J_R, Pi_R, R_readout",
            "these are decisive, but they must be divided by Z_R or directly normalized to q_R_eff.",
            "SELECT_AFTER_NORMALIZATION",
            "derive or source q_R_eff per body/arena",
        ),
        (
            "SEL2839_4_projection",
            "arena projection tau",
            "no empirical score exists until delta_R is mapped into alpha(lambda), PPN, clock, or orbital observables.",
            "REQUIRED_FOR_SCORING",
            "stage tau_R10/tau_PPN/tau_clock/tau_orbital as separate nonclaim rows",
        ),
    ]
    return [
        nonclaim(
            {
                "selector_id": row_id,
                "candidate": candidate,
                "reason": reason,
                "status": status,
                "next_action": next_action,
                "numeric_value_present": False,
                "source_backed": False,
                "accepted_ready": False,
                "control_only": True,
            }
        )
        for row_id, candidate, reason, status, next_action in specs
    ]


def projection_rows() -> list[dict[str, Any]]:
    specs = [
        ("PROJ2839_0_R10", "R10/Yukawa", "alpha_R(lambda) requires ell_R, q_R_eff for each test body, composition coupling, and force normalization", "MISSING_TAU_R10_AND_BODY_CHARGES", "do not compare to Eot-Wash bounds until amplitude and range are sourced"),
        ("PROJ2839_1_PPN", "PPN/local metric", "gamma-1, beta-1, alpha_i residual vector requires metric readout derivative P_PPN[delta_R]", "MISSING_TAU_PPN", "do not claim GR reduction from kernel shape alone"),
        ("PROJ2839_2_clock", "clock/redshift", "fractional clock shift requires readout map from delta_R to frequency or potential difference", "MISSING_TAU_CLOCK", "guard against readout_regen hiding in clock channel"),
        ("PROJ2839_3_orbital", "orbital/timing", "extra acceleration/timing residual requires gradient projection and source normalization", "MISSING_TAU_ORBITAL", "source range/amplitude before orbital comparisons"),
        ("PROJ2839_4_WEP", "composition/WEP", "composition dependence requires material charge map q_R_eff/m for different bodies", "MISSING_COMPOSITION_CHARGE_MAP", "WEP is impossible to score from universal symbols only"),
    ]
    return [
        nonclaim(
            {
                "projection_id": row_id,
                "arena": arena,
                "required_map": required,
                "current_status": status,
                "guardrail": guardrail,
                "numeric_value_present": False,
                "source_backed": False,
                "accepted_ready": False,
                "control_only": True,
            }
        )
        for row_id, arena, required, status, guardrail in specs
    ]


def zero_or_source_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ZOS2839_0_try_ZR_zero",
            "Z_R theorem-zero",
            "would follow from a parent-signed no-derivative grammar for A_R",
            "NOT_PROVED",
            "2838/2261 say absence of explicit R_AB terms is not a grammar proof",
            "retain finite Z_R/ell_R normalization pack",
        ),
        (
            "ZOS2839_1_try_MR2_zero_or_gap",
            "M_R^2 zero/gap theorem",
            "would require parent Hessian signature and sign/gap proof",
            "NOT_PROVED",
            "no parent Hessian or range scale exists in current rows",
            "source direct ell_R or M_R^2/Z_R",
        ),
        (
            "ZOS2839_2_try_JR_zero",
            "J_R source-silence theorem",
            "would require actual R_AB vertical/basicity before matter coupling",
            "NOT_PROVED",
            "2838 keeps matter descent conditional because observed coframe can vary with R_AB",
            "source q_R_eff or derive coframe-basic source silence",
        ),
        (
            "ZOS2839_3_try_PiR_zero",
            "Pi_R/B_R/Q_R boundary-silence theorem",
            "would require exact boundary/no-edge-current theorem",
            "NOT_PROVED",
            "no primitive boundary generator or edge-current cancellation is signed",
            "source boundary homogeneous term or prove no-hair",
        ),
        (
            "ZOS2839_4_first_source_row",
            "first source-backed row",
            "minimal acceptable row is ell_R plus q_R_eff plus source/projection normalization",
            "SCHEMA_READY_VALUES_MISSING",
            "no numeric parent coefficients or arena projection constants are present",
            "next checkpoint should fill or explicitly fail this first row",
        ),
    ]
    return [
        nonclaim(
            {
                "attempt_id": row_id,
                "target": target,
                "success_condition": condition,
                "current_status": status,
                "blocker": blocker,
                "fallback": fallback,
                "theorem_zero": False,
                "numeric_value_present": False,
                "source_backed": False,
                "accepted_ready": False,
                "control_only": True,
            }
        )
        for row_id, target, condition, status, blocker, fallback in specs
    ]


def guard_rows() -> list[dict[str, Any]]:
    specs = [
        ("GUARD2839_0_not_a_claim", "Green kernel is not an empirical pass", "kernel shape without amplitude/range/projection cannot be scored", "keep all local arenas blocked"),
        ("GUARD2839_1_pair_not_single", "do not accept standalone Z_R as a prediction", "the normalized source is S_R/Z_R and range is Z_R/M_R^2", "first finite row must carry a normalization pack"),
        ("GUARD2839_2_sign_convention", "do not hide sign choices", "observable sign depends on parent source convention and projection tau", "record sign in source row before scoring"),
        ("GUARD2839_3_boundary", "do not drop boundary homogeneous modes", "boundary silence is not proved", "carry boundary term until no-hair theorem or finite bound exists"),
        ("GUARD2839_4_no_placeholder_scores", "do not score placeholders", "all rows are symbolic until source paths, units and normalizations exist", "valid_for_claim remains false"),
    ]
    return [
        nonclaim(
            {
                "guard_id": row_id,
                "guard": guard,
                "because": because,
                "effect": effect,
                "guard_active": True,
                "control_only": True,
            }
        )
        for row_id, guard, because, effect in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    kernel_ready = all(row["status"] in {"symbolic_normalization_only", "symbolic_kernel_only"} for row in rows["kernel"])
    finite_nonclaim = all((not row["numeric_value_present"]) and (not row["source_backed"]) for row in rows["source_selector"] + rows["projection"] + rows["zero_or_source"])
    guards_active = all(row["guard_active"] for row in rows["guards"])
    specs = [
        ("GATE2839_0_sources", "all cited source anchors resolve", sources_ok, "PASS_INTERNAL_NONCLAIM" if sources_ok else "BLOCKED", "reproducible local audit trail"),
        ("GATE2839_1_kernel", "Green-kernel normal form is written", kernel_ready, "PASS_SYMBOLIC_NONCLAIM" if kernel_ready else "BLOCKED", "symbolic kernel derived without numeric prediction"),
        ("GATE2839_2_first_source_row", "first source-backed finite row exists", False, "BLOCKED", "normalization pack is specified but values/source paths are missing"),
        ("GATE2839_3_arena_projection", "arena projection maps are source-backed", False, "BLOCKED", "R10/PPN/clock/orbital/WEP maps remain missing"),
        ("GATE2839_4_nonclaim", "finite rows remain nonclaim", finite_nonclaim, "PASS_NONCLAIM" if finite_nonclaim else "BLOCKED", "no placeholders are score eligible"),
        ("GATE2839_5_guards", "guardrails are active", guards_active, "PASS_GUARDRAIL" if guards_active else "BLOCKED", "no single-coefficient or sign/boundary shortcuts"),
        ("GATE2839_6_local_GR", "local GR/Newton reduction is derived", False, "BLOCKED", "kernel normalization is fallback plumbing, not a theorem-zero proof"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": row_id,
                "claim": claim,
                "gate_passed": passed,
                "status": status,
                "reason": reason,
            }
        )
        for row_id, claim, passed, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2839_0_kernel", "Accept the static Green-kernel normalization as the finite fallback grammar.", "SYMBOLIC_NORMAL_FORM_READY", "it gives a concrete target for source rows without pretending to prove local GR.", "use normalized source amplitude q_R_eff and range ell_R"),
        ("DEC2839_1_source_row", "Reject standalone coefficient rows as insufficient.", "NORMALIZATION_PACK_REQUIRED", "Z_R, M_R^2, source charge and projection constants are entangled in observables.", "first source row must include ell_R, q_R_eff, units, sign convention, and projection target"),
        ("DEC2839_2_zero_attempt", "No component theorem-zero was proved in this checkpoint.", "THEOREM_ZERO_NOT_PROVED", "operator, source, boundary and readout zeroes still require parent signatures.", "next: fill or explicitly fail first source-backed normalization pack"),
    ]
    return [
        nonclaim(
            {
                "decision_id": row_id,
                "decision": decision,
                "result": result,
                "because": because,
                "next_action": next_action,
            }
        )
        for row_id, decision, result, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2839_0_2840",
                "status": "selected_primary",
                "target_doc": "2840-Y5-R2FR-first-finite-RAB-normalization-pack-or-parent-zero-certificate-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_first_finite_RAB_normalization_pack_or_parent_zero_certificate_under_AX1090_2840.py",
                "mission": "try to fill the first finite RAB normalization pack: ell_R, q_R_eff, source sign, units, source path, and one arena projection; if impossible, produce the exact parent-zero certificate still missing",
                "acceptance": "no source row can be accepted unless range, amplitude, units, sign convention, source path and arena projection are all present; otherwise keep local claims blocked",
                "forbidden": "do not score standalone Z_R/M_R^2/J_R rows; do not erase boundary homogeneous modes; do not infer source signs from desired GR behavior",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2839_0_kernel", OUTPUTS["kernel"], BRANCH_OUTPUTS["kernel_copy"], "local-bounds copy of Green-kernel normalization"),
        ("BR2839_1_selector", OUTPUTS["source_selector"], BRANCH_OUTPUTS["selector_copy"], "source-weight copy of first finite source row selector"),
        ("BR2839_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue for first normalization pack"),
        ("BR2839_3_decision", OUTPUTS["decision"], BRANCH_OUTPUTS["portable_decision"], "portable beta-source decision ledger"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in ("source_path", "source_table", "copy_path"):
                value = row.get(key)
                if value is None:
                    continue
                for token in str(value).split(";"):
                    item = token.strip()
                    if not item or item.startswith("http") or item.startswith("MISSING_"):
                        continue
                    path = Path(item)
                    if not path.is_absolute():
                        path = ROOT / item
                    paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            for key in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if str(row.get(key, "")).lower() == "true":
                    return False
            for key in ("theorem_zero", "source_backed", "accepted_ready"):
                if str(row.get(key, "")).lower() == "true":
                    return False
    return True


def no_numeric_predictions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {
        "numeric_value",
        "predicted_value",
        "coefficient_value",
        "alpha_bound",
        "lambda_value",
        "accepted_value",
        "raw_value",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in numeric_keys and str(value).strip():
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime >= start:
                return False
        except OSError:
            return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2839_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2839_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2839_2_kernel_written", any(row["kernel_id"] == "KER2839_1_normalized_operator" for row in rows_by_name["kernel"]), "normalized finite operator row exists"),
        ("VAL2839_3_dimension_contract", any(row["dimension_id"] == "DIM2839_3_point_charge" for row in rows_by_name["dimensions"]), "point-source amplitude unit contract exists"),
        ("VAL2839_4_selector_requires_pack", any(row["selector_id"] == "SEL2839_0_minimal_pair" and row["status"] == "SELECTED_SCHEMA_NOT_FILLED" for row in rows_by_name["source_selector"]), "first finite row requires range plus amplitude pack"),
        ("VAL2839_5_projection_blocked", not any(row["source_backed"] for row in rows_by_name["projection"]), "arena projection rows remain unsourced"),
        ("VAL2839_6_zero_not_proved", not any(row["theorem_zero"] for row in rows_by_name["zero_or_source"]), "no theorem-zero component was promoted"),
        ("VAL2839_7_claim_gates_block_scores", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows local scoring"),
        ("VAL2839_8_next_target_2840", any(row["next_id"] == "NEXT2839_0_2840" and row["selected"] for row in rows_by_name["next"]), "first finite normalization pack selected next"),
        ("VAL2839_9_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2839_10_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2839_11_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2839_12_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2839_13_no_claim_flags", no_claim_flags(rows_by_name), "no score/theorem/source/claim flags are true"),
        ("VAL2839_14_no_numeric_predictions", no_numeric_predictions(rows_by_name), "no numeric prediction/coefficient/bound rows inserted"),
        ("VAL2839_15_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2839_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2839_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2839_OVERALL",
            "passed": overall,
            "detail": "2839 derives the symbolic finite R_AB Green-kernel normalization, proves standalone coefficient rows are insufficient, keeps theorem-zero/source-backed rows unclaimed, and selects the first finite normalization pack next.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2839 - Y5 R2FR Finite RAB Residual Green-Kernel Normalization Or First Source-Backed Row Under AX1090

Status: `Y5_R2FR_2839_green_kernel_normalized_first_source_row_pack_required_nonclaim`

## Private Verdict

2839 moves the finite fallback from a vague "source the residual" instruction into a concrete kernel object.

For the finite branch, define

```text
delta_R := R_AB - C_AB[Q]
S_R := J_R + Pi_R + R_readout
E_R^finite = -Div(Z_R Grad R_AB) + M_R^2 delta_R + S_R = 0
```

If `Z_R>0` and `M_R^2>0`, the normalized static branch is

```text
(-Laplace + ell_R^-2) delta_R = -S_R/Z_R
ell_R^2 = Z_R/M_R^2
G_ell(r) = exp(-r/ell_R)/(4*pi*r)
delta_R(x) = - integral G_ell(|x-x'|) S_R(x')/Z_R d^3x' + boundary_homogeneous
```

That is the useful derivation. It tells us the first finite row cannot be a lonely `Z_R` or `J_R`; it must be a normalization pack: `ell_R`, `q_R_eff`, source sign convention, units, source path, and at least one arena projection. No local-GR/Newton or empirical score is allowed from this checkpoint.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Green-Kernel Normalization

{markdown_table(rows["kernel"], ["kernel_id", "equation", "definition", "role", "status", "numeric_value_present", "valid_for_claim"])}

## Dimensional Contract

{markdown_table(rows["dimensions"], ["dimension_id", "symbol", "unit_contract", "derivation_or_definition", "caveat", "definition_closed", "valid_for_claim"])}

## First Source Row Selector

{markdown_table(rows["source_selector"], ["selector_id", "candidate", "reason", "status", "next_action", "accepted_ready", "valid_for_claim"])}

## Arena Projection Contract

{markdown_table(rows["projection"], ["projection_id", "arena", "required_map", "current_status", "guardrail", "accepted_ready", "valid_for_claim"])}

## Theorem-Zero Or Source Row Attempt

{markdown_table(rows["zero_or_source"], ["attempt_id", "target", "success_condition", "current_status", "blocker", "fallback", "theorem_zero", "valid_for_claim"])}

## Guards

{markdown_table(rows["guards"], ["guard_id", "guard", "because", "effect", "guard_active", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "reason", "claim_allowed"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "next_action", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["kernel"] = kernel_rows()
    rows["dimensions"] = dimension_rows()
    rows["source_selector"] = source_selector_rows()
    rows["projection"] = projection_rows()
    rows["zero_or_source"] = zero_or_source_rows()
    rows["guards"] = guard_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in [
        "sources",
        "kernel",
        "dimensions",
        "source_selector",
        "projection",
        "zero_or_source",
        "guards",
        "gates",
        "decision",
        "next",
    ]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2839_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2839_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()

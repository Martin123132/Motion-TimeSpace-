from __future__ import annotations

import csv
import subprocess
from pathlib import Path
from typing import Iterable


BRANCH_ID = "MTS_R2FR_PSI_DETERMINANT_QUOTIENT_MAP_OR_FINITE_QR_COEFFICIENTS_2362"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2362-Y5-R2FR-psi-determinant-quotient-map-or-finite-qR-coefficients.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "numeric_value_present": "false",
        "source_backed": "false",
        "score_ready": "false",
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    sources = [
        ("SRC2362_2361_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2361_NEXT_TARGET.csv", "NEXT2361_0_selected", "2361 selects the psi determinant/quotient route"),
        ("SRC2362_2361_doc", "2361-Y5-R2FR-parent-origin-of-CR-from-phase-cell-current-chain-or-finite-qR-row.md", "BEST_NEXT_NONCIRCULAR_ROUTE", "2361 rejects the current loop and selects psi quotient"),
        ("SRC2362_2270_map", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2270_PSI_COVARIANCE_TO_PHIQ_MAP.csv", "PCM2270_2_q_zero_condition", "exact q=0 covariance-channel relation"),
        ("SRC2362_2270_tests", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2270_PSI_QUOTIENT_TESTS.csv", "PQT2270_4_verdict", "psi quotient not closed and stiffness/source not sourced"),
        ("SRC2362_2271_formulas", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2271_COVARIANCE_PULLBACK_FORMULAS.csv", "PBF2271_3_q_zero_channel", "exact inverse Phi/q to covariance formulas"),
        ("SRC2362_2271_contract", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2271_PULLBACK_CONTRACT.csv", "PBC2271_8_verdict", "pullback contract remains unsigned"),
        ("SRC2362_2272_lift", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2272_ALGEBRAIC_COVARIANCE_LIFT.csv", "ACL2272_1_right_inverse", "covariance-level right inverse exists conditionally"),
        ("SRC2362_2273_curl", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2273_CURL_OBSTRUCTION_DERIVATION.csv", "COD2273_0_general", "field-level psi-gradient lift has curl obstruction"),
        ("SRC2362_2276_wkb", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2276_WKB_COVARIANCE_DERIVATION.csv", "WKB2276_2_smoothed_covariance", "multimode WKB recovers carrier inventory conditionally"),
        ("SRC2362_2278_exchange", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2278_EXACT_EXCHANGE_CONDITION.csv", "EXC2278_2_tangent_lock", "exact q-zero tangency/exchange condition"),
        ("SRC2362_2279_coefficients", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2279_EXCHANGE_COEFFICIENT_LEDGER.csv", "ECL2279_0_target", "exchange coefficients are target-only and unsourced"),
        ("SRC2362_2281_stiffness", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2281_Q_STIFFNESS_DERIVATION_AUDIT.csv", "QSD2281_6_no_smuggling_test", "q-stiffness only helps if selector is parent-owned"),
        ("SRC2362_2283_finalizer", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2283_Q_CLOSURE_FINALIZER.csv", "QCF2283_2_finite_branch", "finite q residual route promoted as nonclaim executable fallback"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in sources:
        path = POST_ROOT / source_path
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": source_path,
                "needle": needle,
                "role": role,
                "path_exists": str(path.exists()).lower(),
                "needle_found": str(contains(path, needle)).lower(),
                "valid_for_claim": "false",
            }
        )
    return rows


def determinant_quotient_gate() -> list[dict[str, object]]:
    rows = [
        (
            "DQG2362_0_channel_definition",
            "psi covariance to local channel map",
            "g=eta+C, A=1-C_T, B=1+C_R, q=ln(A B)=ln[(1-C_T)(1+C_R)]",
            "EXACT_FORMAL_MAP",
            "this makes q the temporal/radial covariance mismatch",
        ),
        (
            "DQG2362_1_q_zero_relation",
            "determinant/reciprocity surface",
            "q=0 iff (1-C_T)(1+C_R)=1 iff C_R=C_T/(1-C_T)",
            "EXACT_IDENTITY",
            "same target as T^2 S=1 and R_AB=0",
        ),
        (
            "DQG2362_2_tangent_condition",
            "q-zero invariant-manifold condition",
            "Dq=0 on q=0 iff D C_R = D C_T/(1-C_T)^2, up to boundary/source terms",
            "EXACT_TANGENCY_TARGET",
            "phase exchange or dynamics must satisfy this, not merely be nonzero",
        ),
        (
            "DQG2362_3_absent_q",
            "q absent from psi image",
            "the psi map would land only on C_R=C_T/(1-C_T)",
            "FAIL_CURRENT_CLAIM",
            "current covariance ansatz has independent temporal and radial channels",
        ),
        (
            "DQG2362_4_vertical_q",
            "q quotient-vertical",
            "Dq_parent kills q variations and matter/readout descends through the quotient",
            "MISSING_QUOTIENT_MAP",
            "no parent equivalence relation or Dq kernel is signed",
        ),
        (
            "DQG2362_5_stationary_q",
            "q stationary/minimized",
            "parent action or coarse-grained free energy has first variation zero at q=0",
            "MISSING_SELECTOR_FUNCTIONAL",
            "q stiffness without selector is a penalty around a chosen target",
        ),
        (
            "DQG2362_6_verdict",
            "psi determinant quotient verdict",
            "the determinant theorem is exact, but current MTS does not derive q=0 from psi",
            "PSI_QUOTIENT_NOT_CLOSED",
            "move to finite q_R coefficient acquisition unless a new selector theorem appears",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "mathematical_statement": statement,
            "status": status,
            "effect": effect,
        }
        for row_id, gate, statement, status, effect in rows
    ]


def psi_lift_audit() -> list[dict[str, object]]:
    rows = [
        (
            "PLA2362_0_pullback_tangent",
            "exact Phi/q covariance tangents",
            "partial_q C_T=-A/2 and partial_q C_R=B/2 at fixed Phi",
            "EXACT_TANGENT_AVAILABLE",
            "future Hessian/source calculations have a target direction",
        ),
        (
            "PLA2362_1_algebraic_lift",
            "covariance-level lift",
            "deltaU=(1/2) deltaC C^{-1} U when the active covariance block is invertible",
            "CONDITIONAL_RIGHT_INVERSE",
            "represents symmetric covariance tangents but not yet scalar field variations",
        ),
        (
            "PLA2362_2_field_exactness",
            "psi-gradient lift",
            "delta u_A must equal d zeta_A, so d(delta u_A)=0",
            "CURL_OBSTRUCTION_UNSIGNED",
            "algebraic one-form lift generally has curl over finite neighbourhoods",
        ),
        (
            "PLA2362_3_multimode_wkb",
            "multimode carrier inventory",
            "phase-averaged high-frequency psi can produce C_mn=sum W_I k_I,m k_I,n + residuals",
            "CONDITIONAL_CARRIER_INVENTORY",
            "useful but requires smoothing kernel, phase inventory, residual bounds, and parent permission",
        ),
        (
            "PLA2362_4_phase_exchange",
            "nonlinear/phase-lock exchange",
            "exchange must satisfy D C_R = D C_T/(1-C_T)^2 on q=0",
            "COEFFICIENTS_UNSOURCED",
            "random phases give no directed exchange; locked phases need projectors/distribution",
        ),
        (
            "PLA2362_5_q_operator",
            "q stiffness or relaxation",
            "L_q q=-div(Z_q grad q)+M_q^2 q or Dq=-mu_q delta F_q/delta q",
            "CONDITIONAL_OPERATOR_ONLY",
            "suppresses q if coefficients exist, but does not by itself explain why q=0 is the selected manifold",
        ),
        (
            "PLA2362_6_verdict",
            "psi lift verdict",
            "the route supplies formulas and conditional mechanisms, not a parent-signed quotient theorem",
            "DERIVATION_ROUTE_OPEN_NOT_CLAIMED",
            "finite q_R rows must stay live",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "object": obj,
            "result_or_formula": formula,
            "status": status,
            "effect": effect,
        }
        for row_id, obj, formula, status, effect in rows
    ]


def finite_qr_contract() -> list[dict[str, object]]:
    rows = [
        ("FQC2362_0_selector", "q=0 selector theorem", "derive absent/vertical/stationary q from parent psi/covariance structure", "MISSING_SELECTOR_THEOREM", "would replace finite branch with local-GR theorem"),
        ("FQC2362_1_Mq2", "M_q^2 transverse mass/stiffness", "M_q^2=n_q^A H_AB n_q^B with units and source path", "MISSING_PARENT_HESSIAN", "sets algebraic q_R=j_q/M_q^2 response"),
        ("FQC2362_2_Zq", "Z_q gradient coefficient", "derive no-gradient theorem or source Z_q and boundary class", "MISSING_OPERATOR_BOUNDARY_INVENTORY", "controls Q_R/r hair and finite-range leakage"),
        ("FQC2362_3_jq", "j_q source/readout leg", "delta S_matter/delta q or same-frame source coefficient", "MISSING_SOURCE_COEFFICIENT", "sets finite q amplitude and WEP/PPN source sensitivity"),
        ("FQC2362_4_Sq", "S_q invariant-manifold source", "compute Dq source term or exchange residual from carrier dynamics", "MISSING_EXCHANGE_COEFFICIENTS", "drives q away from zero if not cancelled"),
        ("FQC2362_5_Pobs", "observable projection P_obs", "map q into gamma-1, beta-1, clocks, orbital residuals, R10 alpha(lambda), and source normalization", "MISSING_OBSERVABLE_PROJECTION", "needed for empirical testing"),
        ("FQC2362_6_MH_source", "Newton/source normalization", "same Hilbert/worldtube source gives Newtonian Phi and the q residual source", "MISSING_NEWTON_SOURCE_GLUE", "GR/Newton reduction cannot be separated from q testing"),
        ("FQC2362_7_bounds", "local comparator bounds", "use R10/PPN/clocks/orbits only after theory coefficients predict q_R", "COMPARATOR_ONLY_NOT_COEFFICIENTS", "prevents using experimental bounds as theory input"),
        ("FQC2362_8_verdict", "finite q_R readiness", "all finite rows must be numeric, sourced, unit-checked, and same-frame", "NOT_SCORE_READY", "next executable route is source acquisition, not a claim"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "required_resolution": required,
            "status": status,
            "effect": effect,
        }
        for row_id, quantity, required, status, effect in rows
    ]


def decision_ledger() -> list[dict[str, object]]:
    rows = [
        ("DEC2362_0_exact_determinant", "determinant/channel theorem", 1, "RETAIN_AS_EXACT_TARGET", "q=0 is now mathematically sharp and unified with R_AB=0"),
        ("DEC2362_1_psi_absent_vertical", "psi absent/vertical quotient proof", 2, "OPEN_NOT_CLOSED", "no parent equivalence relation, Dq kernel, or matter descent is signed"),
        ("DEC2362_2_psi_stationary", "psi/covariance stationary selector", 3, "OPEN_NOT_CLOSED", "no parent free energy or action first variation selects q=0"),
        ("DEC2362_3_phase_exchange", "phase-lock/exchange tangency", 4, "UNSOURCED", "random phases do not direct exchange and locked distributions/projectors are missing"),
        ("DEC2362_4_q_stiffness", "q stiffness/relaxation operator", 5, "CONDITIONAL_BUT_NOT_SELECTOR", "can bound finite residuals only after coefficients and source are derived"),
        ("DEC2362_5_finite_coefficients", "finite q_R coefficient route", 1, "SELECT_NEXT_EXECUTABLE_ROUTE", "2361 asked for finite q_R sourcing if psi map remains open; it does"),
        ("DEC2362_6_public_claim", "local GR/Newton claim", 99, "BLOCKED", "determinant identity is not parent selection"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "route": route,
            "rank": rank,
            "decision": decision,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, route, rank, decision, reason in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2362_0_absent_q", "psi map makes q absent", "BLOCKED", "independent temporal/radial covariance channels remain"),
        ("CG2362_1_vertical_q", "q is quotient-vertical", "BLOCKED", "no parent q map/equivalence/Dq kernel"),
        ("CG2362_2_stationary_q", "q=0 is stationary parent manifold", "BLOCKED", "no selector functional or Euler equation"),
        ("CG2362_3_q_operator", "finite q operator is theory-owned", "BLOCKED", "M_q^2, Z_q, j_q, P_obs missing"),
        ("CG2362_4_newton", "GR/Newton reduction derived", "BLOCKED", "source normalization and local selector remain open"),
        ("CG2362_5_public", "R10/PPN/clock/orbital pass", "BLOCKED", "no sourced prediction row"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "passes_public_claim": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, claim, status, reason in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2362_0_identity", "q=0 identity proves local GR", "BLOCKED", "identity names the target but does not parent-select it"),
        ("REF2362_1_metric_ansatz", "g[psi] ansatz proves matter metric ownership", "BLOCKED", "covariance, coframe, connection, and matter blindness remain unsigned"),
        ("REF2362_2_algebraic_lift", "covariance-level lift is a field-level psi variation", "BLOCKED", "curl/exactness obstruction remains"),
        ("REF2362_3_phase_lock", "phase locking closes q=0", "BLOCKED", "directed exchange and tangency coefficients are unsourced"),
        ("REF2362_4_penalty", "adding q stiffness derives q=0", "BLOCKED", "penalty suppresses residuals only after selector/coefficients are owned"),
        ("REF2362_5_bounds", "experimental local bounds define q_R coefficients", "BLOCKED", "bounds test predictions; they do not supply parent coefficients"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "attempted_claim": attempted,
            "runner_result": result,
            "blocked_by": blocked_by,
            "score_eligible": "false",
            "valid_for_claim": "false",
        }
        for row_id, attempted, result, blocked_by in rows
    ]


def next_target() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2362_0_selected",
            "next_file": "2363-Y5-R2FR-finite-qR-coefficient-source-pack-or-selector-reentry.md",
            "next_script": "scripts/Y5_R2FR_finite_qR_coefficient_source_pack_or_selector_reentry_2363.py",
            "selected_reason": "psi determinant/quotient map remains open; finite q_R route is the next executable nonclaim branch",
            "success_condition": "source M_q^2, Z_q/no-gradient guard, j_q/S_q, P_obs, and Newton source normalization with units and parent paths",
            "fallback_condition": "if coefficients cannot be sourced, keep R_AB=0/q=0 as closure benchmark only and block local-GR claims",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
    ]


def formalization_status() -> tuple[bool, str]:
    if not FORMALIZATION_WORKBENCH.exists():
        return True, "formalization-workbench path not found; generator has no write targets there"
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT_ROOT), "status", "--short", "--", "formalization-workbench"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return True, f"git unavailable ({exc}); generator writes only under post-checkpoint-work"
    if result.returncode == 0:
        changed = [line for line in result.stdout.splitlines() if line.strip()]
        return len(changed) == 0, "git modified-file count for formalization-workbench is 0" if not changed else f"formalization-workbench has {len(changed)} status rows"
    return True, "project is not a git worktree here; generator writes only under post-checkpoint-work"


def parse_csv_ok(paths: Iterable[Path]) -> tuple[bool, str]:
    for path in paths:
        try:
            rows = read_csv(path)
        except Exception as exc:
            return False, f"{rel(path)} failed to parse: {exc}"
        if not rows:
            return False, f"{rel(path)} has no rows"
    return True, "all generated CSV files parse and contain rows"


def no_positive_claim_flags(paths: Iterable[Path]) -> tuple[bool, str]:
    flag_columns = [
        "parent_signed",
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "passes_public_claim",
        "score_eligible",
    ]
    offenders: list[str] = []
    for path in paths:
        for row in read_csv(path):
            for column in flag_columns:
                if row.get(column, "").strip().lower() == "true":
                    offenders.append(f"{rel(path)}:{row.get('row_id', row.get('source_id', '?'))}:{column}")
    if offenders:
        return False, "; ".join(offenders[:10])
    return True, "all generated claim/readiness flags remain negative"


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(row_id: str, ok: bool, detail: str) -> None:
        rows.append({"row_id": row_id, "status": "PASS" if ok else "FAIL", "detail": detail, "valid_for_claim": "false"})

    missing_sources = [str(row["source_path"]) for row in sources if row["path_exists"] != "true"]
    missing_needles = [str(row["source_id"]) for row in sources if row["needle_found"] != "true"]
    add("VAL2362_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2362_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))
    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2362_02_outputs_exist", all(path.exists() for path in generated), "all 2362 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2362_03_csv_parse", parse_ok, parse_detail)

    gates = {row["row_id"]: row["status"] for row in read_csv(outputs["determinant"])}
    add("VAL2362_04_exact_determinant_recorded", gates.get("DQG2362_1_q_zero_relation") == "EXACT_IDENTITY", "exact determinant q-zero relation recorded")
    add("VAL2362_05_psi_not_promoted", gates.get("DQG2362_6_verdict") == "PSI_QUOTIENT_NOT_CLOSED", "psi quotient route remains unclaimed")
    finite = read_csv(outputs["finite"])
    add("VAL2362_06_finite_rows_nonclaim", all(row.get("score_ready") == "false" for row in finite), "finite q_R rows remain not score-ready")
    decisions = {row["row_id"]: row["decision"] for row in read_csv(outputs["decision"])}
    add("VAL2362_07_finite_next_selected", decisions.get("DEC2362_5_finite_coefficients") == "SELECT_NEXT_EXECUTABLE_ROUTE", "finite coefficient source route selected")
    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2362_08_no_positive_claim_flags", flag_ok, flag_detail)
    formal_ok, formal_detail = formalization_status()
    add("VAL2362_09_formalization_untouched", formal_ok, formal_detail)
    claim_blocked = all(row.get("passes_public_claim") == "false" for row in read_csv(outputs["claims"]))
    add("VAL2362_10_claim_gates_blocked", claim_blocked, "all public claim gates remain blocked")
    add("VAL2362_11_next_selected", read_csv(outputs["next"])[0].get("row_id") == "NEXT2362_0_selected", "2363 finite q_R source-pack target selected")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2362_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2362 valid: exact psi determinant target recorded, quotient not promoted, finite q_R source route selected" if overall else "one or more validation gates failed",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(outputs: dict[str, Path]) -> None:
    def table(headers: list[str], rows: list[dict[str, str]]) -> str:
        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
        ]
        for row in rows:
            lines.append("| " + " | ".join(row.get(header, "").replace("|", "/") for header in headers) + " |")
        return "\n".join(lines)

    determinant = read_csv(outputs["determinant"])
    lift = read_csv(outputs["lift"])
    finite = read_csv(outputs["finite"])
    decisions = read_csv(outputs["decision"])
    next_rows = read_csv(outputs["next"])

    md = f"""# 2362 — Psi Determinant Quotient Map Or Finite `q_R` Coefficients

## Result

The psi/covariance route gives an exact target, but not yet the parent owner.

With `g=eta+C`, `A=1-C_T`, and `B=1+C_R`,

`q = ln(A B) = ln[(1-C_T)(1+C_R)]`.

So `q=0` iff `(1-C_T)(1+C_R)=1`, equivalently `C_R=C_T/(1-C_T)`.  The invariant-manifold condition is also exact: on `q=0`, the local transport/readout must satisfy `D C_R = D C_T/(1-C_T)^2` up to owned boundary/source terms.

That is a real sharpening.  It is not yet a derivation of local GR/Newton, because current MTS does not prove that the psi map lands on this surface, that `q` is quotient-vertical, or that a parent selector/free-energy makes it stationary.  The next executable route is finite `q_R` coefficient sourcing.

## Determinant / Quotient Gate

{table(["row_id", "gate", "status", "effect"], determinant)}

## Psi Lift Audit

{table(["row_id", "object", "status", "effect"], lift)}

## Finite `q_R` Coefficient Contract

{table(["row_id", "quantity", "status", "effect"], finite)}

## Decision Ledger

{table(["row_id", "route", "rank", "decision", "reason"], decisions)}

## Next Target

{table(["row_id", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["determinant"])}`
- `{rel(outputs["lift"])}`
- `{rel(outputs["finite"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is not circling.  It cuts the psi route down to its exact mathematical demand: either the parent theory owns the determinant surface, or the local branch must carry a finite `q_R` prediction with sourced coefficients.  The next step is therefore not another slogan about quotienting; it is `M_q^2`, `Z_q`, `j_q/S_q`, `P_obs`, and Newton-source normalization, with units and source paths.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def main() -> int:
    sources = source_register()
    outputs = {
        "source": RESIDUALS / "P8_Y5_PARENT_QLOC_2362_SOURCE_REGISTER.csv",
        "determinant": RESIDUALS / "P8_Y5_PARENT_QLOC_2362_PSI_DETERMINANT_QUOTIENT_GATE.csv",
        "lift": RESIDUALS / "P8_Y5_PARENT_QLOC_2362_PSI_LIFT_AND_CARRIER_AUDIT.csv",
        "finite": RESIDUALS / "P8_Y5_PARENT_QLOC_2362_FINITE_QR_COEFFICIENT_CONTRACT.csv",
        "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_2362_DECISION_LEDGER.csv",
        "claims": RESIDUALS / "P8_Y5_PARENT_QLOC_2362_CLAIM_GATES.csv",
        "refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_2362_REFUSAL_RUNNER.csv",
        "next": RESIDUALS / "P8_Y5_PARENT_QLOC_2362_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2362_VALIDATION.csv",
    }

    write_csv(outputs["source"], sources)
    write_csv(outputs["determinant"], determinant_quotient_gate())
    write_csv(outputs["lift"], psi_lift_audit())
    write_csv(outputs["finite"], finite_qr_contract())
    write_csv(outputs["decision"], decision_ledger())
    write_csv(outputs["claims"], claim_gates())
    write_csv(outputs["refusal"], refusal_runner())
    write_csv(outputs["next"], next_target())
    validation = validation_rows(outputs, sources)
    write_csv(outputs["validation"], validation)
    write_markdown(outputs)

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

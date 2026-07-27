from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3261-Y5-R2FR-factorize-B_alpha-product-or-sign-fixed-EM-no-counterterm-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3261_SOURCE_REGISTER.csv",
    "factorization": OUT / "P8_Y5_R2FR_3261_B_ALPHA_FACTORIZATION_LAW.csv",
    "scenario": OUT / "P8_Y5_R2FR_3261_FACTOR_SENSITIVITY_RUNNER_NONCLAIM.csv",
    "zero_routes": OUT / "P8_Y5_R2FR_3261_ZERO_FACTOR_ROUTE_AUDIT.csv",
    "no_counterterm": OUT / "P8_Y5_R2FR_3261_FIXED_EM_NO_COUNTERTERM_LEMMA.csv",
    "factor_inputs": OUT / "P8_Y5_R2FR_3261_REQUIRED_FACTOR_INPUTS.csv",
    "gates": OUT / "P8_Y5_R2FR_3261_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3261_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3261_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3261_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
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
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            lowered_line = line.lower()
            if any(needle in lowered_line for needle in lowered_needles):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:280]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def float_or_none(value: Any) -> float | None:
    try:
        return float(str(value).strip())
    except Exception:
        return None


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def product_bound() -> float:
    path = OUT / "P8_Y5_R2FR_3260_DD_WEP_BOUND_OUTPUT_NONCLAIM.csv"
    for row in read_csv(path):
        if row.get("bound_id") == "BOUT3260_4_reported_level_product_bound":
            value = float_or_none(row.get("value"))
            if value is None:
                raise ValueError("missing product bound value")
            return value
    raise ValueError("missing BOUT3260_4_reported_level_product_bound")


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3261_3260_handoff",
            ROOT / "3260-Y5-R2FR-fixed-EM-owner-zero-theorem-or-DD-WEP-bound-runner-under-AX1090.md",
            "3260 selected factorization or fixed-EM no-counterterm target",
            ["NEXT3260_0_3261", "B_alpha^MTS", "1.362001757454e-12"],
        ),
        (
            "SRC3261_3260_bound",
            OUT / "P8_Y5_R2FR_3260_DD_WEP_BOUND_OUTPUT_NONCLAIM.csv",
            "real MICROSCOPE/DD product-bound output",
            ["BOUT3260_4_reported_level_product_bound", "1.362001757454e-12"],
        ),
        (
            "SRC3261_3260_guards",
            OUT / "P8_Y5_R2FR_3260_BOUND_INTERPRETATION_GUARDS.csv",
            "product-only and no-cancellation guards",
            ["GUARD3260_0_product_only", "GUARD3260_1_no_cancellation"],
        ),
        (
            "SRC3261_1400_residual_vector",
            OUT / "P8_Y5_R10_1400_FINITE_EM_LOCAL_RESIDUAL_VECTOR.csv",
            "named EM residual factors",
            ["REM1400_3_b_alpha_EM", "REM1400_4_beta_source_alpha", "REM1400_6_WEP"],
        ),
        (
            "SRC3261_1228_tau_gate",
            OUT / "P8_Y5_R10_1228_ACCEPTANCE_GATE_MATRIX.csv",
            "tau_WEP acceptance gate remains blocked",
            ["ACCEPT1228_4_tau_WEP"],
        ),
        (
            "SRC3261_1899_wep_pack",
            OUT / "P8_Y5_PARENT_QLOC_1899_WEP_INPUT_PACK_NONCLAIM.csv",
            "source/readout/tau input pack requirements",
            ["WIP1899_5_force_map", "WIP1899_6_tau_wep"],
        ),
        (
            "SRC3261_990_parent_action",
            OUT / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
            "parent action EM lock and source charge contract",
            ["PAC990_3_EM_lock", "PAC990_4_source_charge"],
        ),
        (
            "SRC3261_1397_unique_F2",
            OUT / "P8_Y5_R10_1397_UNIQUE_MAXWELL_F2_PROOF_AUDIT.csv",
            "unique Maxwell/no-counterterm audit",
            ["UMF1397_6_exact_conditional_theorem", "UMF1397_7_current_verdict"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def factorization_rows() -> list[dict[str, Any]]:
    bound = product_bound()
    return [
        {
            "factor_id": "FAC3261_0_product",
            "quantity": "B_alpha^MTS",
            "definition": "B_alpha^MTS := beta_source_alpha * b_alpha_EM * tau_WEP",
            "bound_or_formula": f"|B_alpha^MTS| <= {bound:.12e} from MICROSCOPE/DD isolated EM branch",
            "status": "PRODUCT_BOUND_REAL_FACTORS_UNSEPARATED",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "FAC3261_1_b_alpha_EM",
            "quantity": "b_alpha_EM",
            "definition": "canonical parent alpha pullback/drift",
            "bound_or_formula": "b_alpha_EM = -partial_phi ln(C_P N_Q + lambda_A) - rho_readout",
            "status": "MISSING_DERIVATIVE_MAP_OR_FIXED_EM_ZERO",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "FAC3261_2_beta_source_alpha",
            "quantity": "beta_source_alpha",
            "definition": "same-owner source/force normalization multiplying finite alpha WEP branch",
            "bound_or_formula": "eta_AB_alpha = DeltaQ_alpha_AB beta_source_alpha b_alpha_EM tau_WEP",
            "status": "MISSING_SAME_OWNER_SOURCE_THEOREM_OR_NUMERIC_MAP",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "FAC3261_3_tau_WEP",
            "quantity": "tau_WEP",
            "definition": "projection/readout/orbit kernel that maps source residual to measured MICROSCOPE differential acceleration",
            "bound_or_formula": "tau_WEP must come from official/source-equivalent readout arrays or parent reduction theorem; tau_WEP=1 shortcut forbidden",
            "status": "MISSING_ACCEPTED_TAU_INPUT",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "FAC3261_4_inversion",
            "quantity": "single-factor bound",
            "definition": "if any two factors are supplied, the third is bounded",
            "bound_or_formula": "|b_alpha_EM| <= B_bound/(|beta_source_alpha tau_WEP|), and cyclic permutations",
            "status": "EXACT_FACTOR_INVERSION_LAW_READY",
            "valid_for_claim": "false",
        },
    ]


def scenario_rows() -> list[dict[str, Any]]:
    bound = product_bound()
    scenarios = [
        ("SC3261_unity_debug", 1.0, 1.0, "debug only; unity shortcut is forbidden for claims"),
        ("SC3261_tau_tenth", 1.0, 0.1, "tau attenuation example"),
        ("SC3261_source_tenth", 0.1, 1.0, "source-normalization attenuation example"),
        ("SC3261_both_tenth", 0.1, 0.1, "both source and tau attenuated"),
        ("SC3261_both_hundredth", 0.01, 0.01, "strong attenuation example"),
    ]
    rows: list[dict[str, Any]] = []
    for scenario_id, beta_source_alpha, tau_wep, note in scenarios:
        beta_tau = abs(beta_source_alpha * tau_wep)
        b_alpha_bound = bound / beta_tau if beta_tau > 0 else math.inf
        rows.append(
            {
                "scenario_id": scenario_id,
                "beta_source_alpha_assumed": f"{beta_source_alpha:.12e}",
                "tau_WEP_assumed": f"{tau_wep:.12e}",
                "beta_tau_product": f"{beta_tau:.12e}",
                "implied_abs_b_alpha_EM_bound": f"{b_alpha_bound:.12e}",
                "note": note,
                "accepted_as_evidence": "false",
                "valid_for_claim": "false",
            }
        )
    return rows


def zero_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "ZERO3261_0_fixed_EM",
            "zero_factor": "b_alpha_EM=0",
            "required_derivation": "lambda_A=0, Lie_v(C_P N_Q)=0, and rho_readout=0 from fixed EM owner/readout descent",
            "what_it_kills": "WEP alpha branch, clock alpha branch, and local EM composition branch together",
            "current_status": "BEST_ROUTE_BUT_NO_COUNTERTERM_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "route_id": "ZERO3261_1_source_decoupling",
            "zero_factor": "beta_source_alpha=0",
            "required_derivation": "same-owner source theorem says alpha material response does not enter gravitational source/force normalization",
            "what_it_kills": "WEP alpha/source branch only; clock alpha drift may remain",
            "current_status": "NOT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "route_id": "ZERO3261_2_projection_silence",
            "zero_factor": "tau_WEP=0",
            "required_derivation": "official readout/source projection orthogonal to the EM composition residual",
            "what_it_kills": "MICROSCOPE WEP readout only; not local GR or clocks",
            "current_status": "NOT_DERIVED_AND_UNLIKELY_AS_GENERAL_ROUTE",
            "valid_for_claim": "false",
        },
        {
            "route_id": "ZERO3261_3_product_bound",
            "zero_factor": "none",
            "required_derivation": "retain product as finite residual and require |B_alpha^MTS|<=1.362001757454e-12",
            "what_it_kills": "nothing by theorem; constrains residual branch empirically",
            "current_status": "REAL_BOUND_AVAILABLE_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def no_counterterm_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma_id": "NCT3261_0_domain_definition",
            "premise": "The parent action domain contains parent-local gauge curvature invariants only; no post-quotient observed-only counterterm may be added.",
            "formula": "Allowed_2der(parent,U(1)_Q)={mu_P C_P<Phi><F_P,F_P>_P subblock}; not {q^*(mu_obs F_Q^2) with independent lambda_A}",
            "result": "observed lambda_A has no independent slot",
            "status": "EXACT_IF_PARENT_DOMAIN_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "NCT3261_1_projection",
            "premise": "A_Q is the T_Q subblock of the parent connection and the T_Q norm N_Q is fixed.",
            "formula": "g_EM^{-2}=C_P N_Q after quotient/readout, up to quotient-fixed unit factors",
            "result": "alpha drift can only come from parent C_P/N_Q/readout, not a separate species/source coefficient",
            "status": "CONDITIONAL_ON_FIXED_PARENT_NORM",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "NCT3261_2_readout",
            "premise": "coframe/Hodge/hbar*c/readout descent is quotient-fixed along local vertical paths",
            "formula": "rho_readout=0",
            "result": "unit/readout drift cannot fake alpha variation",
            "status": "CONDITIONAL_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "NCT3261_3_zero",
            "premise": "NCT3261_0 through NCT3261_2 plus Lie_v(C_P N_Q)=0",
            "formula": "b_alpha_EM=-Lie_v ln(C_P N_Q)-rho_readout=0",
            "result": "fixed-EM branch gives B_alpha^MTS=0 regardless of beta_source_alpha and tau_WEP",
            "status": "DERIVED_CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "NCT3261_4_current_corpus_verdict",
            "premise": "UMF1397_7 still says Z_unique_F2=false while DeltaS_lambda is allowed",
            "formula": "lambda_A retained unless parent action domain is explicitly signed",
            "result": "no-counterterm theorem is not claimed; DD bound branch remains active",
            "status": "CLAIM_BLOCKED_BY_CURRENT_CORPUS",
            "valid_for_claim": "false",
        },
    ]


def factor_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "REQ3261_0_b_alpha_derivative_map",
            "factor": "b_alpha_EM",
            "needed_input": "C_P, N_Q, lambda_A, derivative map, and rho_readout or fixed-EM zero theorem",
            "current_source": "REM1400_3_b_alpha_EM",
            "status": "MISSING_DERIVATIVE_MAP",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3261_1_beta_source_map",
            "factor": "beta_source_alpha",
            "needed_input": "same-owner current/source theorem or numeric source-force normalization",
            "current_source": "REM1400_4_beta_source_alpha; PAC990_4_source_charge",
            "status": "MISSING_SOURCE_MAP",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3261_2_tau_WEP",
            "factor": "tau_WEP",
            "needed_input": "official/equivalent MICROSCOPE readout arrays or parent reduction theorem",
            "current_source": "ACCEPT1228_4_tau_WEP; WIP1899_6_tau_wep",
            "status": "MISSING_ACCEPTED_TAU",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3261_3_no_cancellation",
            "factor": "channel isolation",
            "needed_input": "no-cancellation theorem or full multi-channel vector fit",
            "current_source": "GUARD3260_1_no_cancellation",
            "status": "MISSING_MULTI_CHANNEL_CONTROL",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3261_0_factorization",
            "gate": "B_alpha product factorization law",
            "passed": "true",
            "reason": "product bound is now split into b_alpha_EM, beta_source_alpha, and tau_WEP with exact inversion laws",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3261_1_fixed_EM_zero",
            "gate": "fixed-EM no-counterterm theorem signed",
            "passed": "false",
            "reason": "operator-domain/no-counterterm/readout clauses remain conditional in the current corpus",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3261_2_real_factor_values",
            "gate": "real separate values for beta_source_alpha, b_alpha_EM, and tau_WEP",
            "passed": "false",
            "reason": "only their product has a MICROSCOPE/DD bound",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3261_3_local_GR",
            "gate": "local GR/Newton/Maxwell promotion",
            "passed": "false",
            "reason": "requires fixed-EM zero theorem or all factor/product residuals below explicit local gates",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3261_0",
            "verdict": "PRODUCT_FACTORIZED_NO_COUNTERTERM_LEMMA_CONDITIONAL",
            "what_moved": "the coupling gap is now three named factors with exact inversion laws and a hard MICROSCOPE/DD product scale",
            "best_next": "attack no-counterterm parent action domain because it zeroes b_alpha_EM globally if signed",
            "fallback_next": "source tau_WEP/readout and beta_source_alpha to turn the product bound into separate factor bounds",
            "valid_for_claim": "false",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3261_0_3262",
            "selected": "primary",
            "target_doc": "3262-Y5-R2FR-parent-action-domain-signature-or-source-tau-factor-intake-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3262_parent_action_domain_signature_or_source_tau_factor_intake.py",
            "objective": "Either sign the parent action domain forbidding quotient-only Maxwell counterterms, or acquire real tau_WEP/source-normalization factor inputs for the B_alpha product.",
            "guardrail": "Do not use unity tau/source shortcuts as claim evidence; they are debug scenarios only.",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_count() -> int:
    if not FW.exists():
        return 0
    script_mtime = Path(__file__).stat().st_mtime
    return sum(1 for path in FW.rglob("*") if path.is_file() and path.stat().st_mtime > script_mtime)


def validation_rows() -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    source_rows = source_register()
    bound = product_bound()
    scenario = scenario_rows()
    unity = next(row for row in scenario if row["scenario_id"] == "SC3261_unity_debug")
    validations = [
        {
            "check_id": "VAL3261_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in source_rows)),
            "detail": ";".join(row["source_id"] for row in source_rows if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3261_1_sources_parse",
            "check": "all cited source CSV/MD paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in source_rows)),
            "detail": ";".join(row["source_id"] for row in source_rows if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3261_2_outputs_parse",
            "check": "all 3261 output CSVs parse",
            "passed": bool_str(all(csv_ok(path) for path in output_paths)),
            "detail": ";".join(str(path) for path in output_paths if not csv_ok(path)),
        },
        {
            "check_id": "VAL3261_3_product_bound_numeric",
            "check": "product bound is finite positive",
            "passed": bool_str(math.isfinite(bound) and bound > 0),
            "detail": f"B_bound={bound:.12e}",
        },
        {
            "check_id": "VAL3261_4_unity_scenario_matches_bound",
            "check": "unity debug scenario returns the product bound as b_alpha bound",
            "passed": bool_str(abs(float(unity["implied_abs_b_alpha_EM_bound"]) - bound) <= bound * 1e-12),
            "detail": unity["implied_abs_b_alpha_EM_bound"],
        },
        {
            "check_id": "VAL3261_5_claim_gates_false",
            "check": "no 3261 claim gate allows local-GR/WEP/Maxwell promotion",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in claim_gate_rows())),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3261_6_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3261_7_overall",
            "check": "3261 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3261_7_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def write_doc() -> None:
    sources = source_register()
    factorization = factorization_rows()
    scenario = scenario_rows()
    zero_routes = zero_route_rows()
    no_counterterm = no_counterterm_rows()
    factor_inputs = factor_input_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()
    validations = validation_rows()
    bound = product_bound()
    content = f"""# 3261 - Factorize B_alpha product or sign fixed EM no-counterterm under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3261` factorizes the MICROSCOPE/DD coupling bound into `B_alpha^MTS = beta_source_alpha * b_alpha_EM * tau_WEP`.
- The product bound is real: `|B_alpha^MTS| <= {bound:.12e}` for the isolated Ti/Pt DD/EM branch.
- The clean derivation route is still fixed EM: sign the parent action domain/no-counterterm/readout chain and get `b_alpha_EM=0`.
- If fixed EM does not close, the fallback is no longer vague: source two factors and the third is bounded by exact inversion.

## Source Register
{md_table(sources, ["source_id", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"])}

## B Alpha Factorization Law
{md_table(factorization, ["factor_id", "quantity", "definition", "bound_or_formula", "status", "valid_for_claim"])}

## Factor Sensitivity Runner
{md_table(scenario, ["scenario_id", "beta_source_alpha_assumed", "tau_WEP_assumed", "beta_tau_product", "implied_abs_b_alpha_EM_bound", "note", "accepted_as_evidence", "valid_for_claim"])}

## Zero Factor Route Audit
{md_table(zero_routes, ["route_id", "zero_factor", "required_derivation", "what_it_kills", "current_status", "valid_for_claim"])}

## Fixed EM No-Counterterm Lemma
{md_table(no_counterterm, ["lemma_id", "premise", "formula", "result", "status", "valid_for_claim"])}

## Required Factor Inputs
{md_table(factor_inputs, ["input_id", "factor", "needed_input", "current_source", "status", "valid_for_claim"])}

## Claim Gates
{md_table(gates, ["gate_id", "gate", "passed", "reason", "claim_allowed"])}

## Decision
{md_table(decisions, ["decision_id", "verdict", "what_moved", "best_next", "fallback_next", "valid_for_claim"])}

## Next Target
{md_table(next_targets, ["next_id", "selected", "target_doc", "target_script", "objective", "guardrail", "valid_for_claim"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_key = {
        "sources": source_register(),
        "factorization": factorization_rows(),
        "scenario": scenario_rows(),
        "zero_routes": zero_route_rows(),
        "no_counterterm": no_counterterm_rows(),
        "factor_inputs": factor_input_rows(),
        "gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, rows in rows_by_key.items():
        write_csv(OUTPUTS[key], rows)
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

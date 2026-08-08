from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3228-Y5-R2FR-Xi-clock-product-row-or-clock-tau-owner-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3228_INPUTS.csv"
DERIVATION = OUT / "P8_Y5_R2FR_3228_XI_CLOCK_PRODUCT_DERIVATION.csv"
CONTRACT = OUT / "P8_Y5_R2FR_3228_PARENT_XI_CLOCK_CONTRACT.csv"
BOUNDS = OUT / "P8_Y5_R2FR_3228_XI_CLOCK_BOUND_INTERFACE.csv"
OBSTRUCTIONS = OUT / "P8_Y5_R2FR_3228_OWNER_OBSTRUCTION_LEDGER.csv"
DECISION = OUT / "P8_Y5_R2FR_3228_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3228_VALIDATION.csv"

INTERFACE_3227 = OUT / "P8_Y5_R2FR_3227_CD_OR_PICLOCK_ACQUISITION_INTERFACE.csv"
PRODUCT_3225 = OUT / "P8_Y5_R2FR_3225_PRODUCT_CONSTRAINTS_FROM_ANCHORS.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def maybe_float(value: object) -> float | None:
    try:
        if value is None:
            return None
        text = str(value).strip()
        if not text or text.lower().startswith("missing") or text.lower() in {"not_applicable", "none", "nan"}:
            return None
        number = float(text)
        if not math.isfinite(number):
            return None
        return number
    except Exception:
        return None


def resolve(location: str, relative_path: str) -> Path:
    if location == "post_checkpoint":
        return ROOT / relative_path
    if location == "mts_residuals":
        return OUT / relative_path
    if location == "formalization":
        return FW / relative_path
    raise ValueError(location)


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:220]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


SOURCES = [
    {
        "input_id": "SRC3228_00_3227_doc",
        "location": "post_checkpoint",
        "relative_path": "3227-Y5-R2FR-Pi-clock-or-CD-source-row-acquisition-under-AX1090.md",
        "role": "3227 handoff selecting direct Xi_clock product row",
        "terms": ["Xi_clock", "2.1e-18", "parent-side product row"],
    },
    {
        "input_id": "SRC3228_01_3227_interface",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3227_CD_OR_PICLOCK_ACQUISITION_INTERFACE.csv",
        "role": "Xi_clock interface and refusal rules",
        "terms": ["XIC3227_0_definition", "XIC3227_3_direct_product_acquisition", "XIC3227_5_refusal_rule"],
    },
    {
        "input_id": "SRC3228_02_3225_products",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3225_PRODUCT_CONSTRAINTS_FROM_ANCHORS.csv",
        "role": "real clock product bound",
        "terms": ["PC3225_0_clock_1sigma", "PC3225_1_clock_2sigma"],
    },
    {
        "input_id": "SRC3228_03_3222_contract",
        "location": "post_checkpoint",
        "relative_path": "3222-Y5-R2FR-defect-norm-parent-action-contract-or-finite-alpha-coefficient-runner-under-AX1090.md",
        "role": "defect-norm parent action contract",
        "terms": ["S_EM", "Z_*", "lambda_D", "R_Q", "Delta Z_A"],
    },
    {
        "input_id": "SRC3228_04_3223_formula",
        "location": "post_checkpoint",
        "relative_path": "3223-Y5-R2FR-RQ-source-search-or-finite-alpha-runner-smoke-inputs-under-AX1090.md",
        "role": "finite alpha formula and R_Z owner hunt",
        "terms": ["R_Z", "b_alpha_m", "D_m R_Q", "Z_min"],
    },
    {
        "input_id": "SRC3228_05_3223_formula_csv",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3223_FINITE_ALPHA_BOUND_FORMULA.csv",
        "role": "machine finite alpha formula",
        "terms": ["FORM3223_1_offroot_bound", "D_m R_Q", "Z_min"],
    },
    {
        "input_id": "SRC3228_06_3226_package",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3226_CD_COEFFICIENT_PACKAGE.csv",
        "role": "C_D and Pi_clock package",
        "terms": ["CD3226_0_definition", "CD3226_1_clock_product"],
    },
    {
        "input_id": "SRC3228_07_3136_doc",
        "location": "post_checkpoint",
        "relative_path": "3136-Y5-R2FR-observed-coframe-clock-functional-owner-under-AX1090.md",
        "role": "conditional clock readout theorem",
        "terms": ["observed clocks measure observed metric proper time", "parent has not signed", "R_clock"],
    },
    {
        "input_id": "SRC3228_08_3136_theorem",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3136_OBSERVED_CLOCK_FUNCTIONAL_THEOREM.csv",
        "role": "machine clock functional theorem",
        "terms": ["observed coframe", "clock", "parent"],
    },
    {
        "input_id": "SRC3228_09_2600_doc",
        "location": "post_checkpoint",
        "relative_path": "2600-Y5-R2FR-Tobs-delta-tau-norm-owner-or-boundary-clock-action-clause.md",
        "role": "Tobs/delta_tau norm owner route",
        "terms": ["C_Tobs_tau", "Delta_JH_delta_tau", "not yet parent-signed"],
    },
    {
        "input_id": "SRC3228_10_2600_norm",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_TOBS_DTAU_2600_NORM_OWNER_ATTEMPT.csv",
        "role": "machine norm-owner attempt",
        "terms": ["C_Tobs_tau", "NOT_PARENT_OWNED", "valid_for_claim"],
    },
]


def product_bound(constraint_id: str) -> float:
    for row in read_csv(PRODUCT_3225):
        if row.get("constraint_id") == constraint_id:
            value = maybe_float(row.get("numeric_bound"))
            if value is None:
                raise ValueError(f"missing numeric bound for {constraint_id}")
            return value
    raise ValueError(f"missing constraint row {constraint_id}")


def build_rows(now: str) -> tuple[list[dict[str, object]], ...]:
    input_rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        input_rows.append(
            {
                **source,
                "path": str(path),
                "exists": b(path.exists()),
                "evidence_hits": evidence(path, source["terms"]),
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )

    clock_1sigma = product_bound("PC3225_0_clock_1sigma")
    clock_2sigma = product_bound("PC3225_1_clock_2sigma")

    derivation_rows = [
        {
            "step_id": "XID3228_0_observable_quantity",
            "claim_piece": "clock observable alpha drift",
            "formula": "|d ln alpha_EM / d tau_obs|",
            "derivation_status": "TARGET_DEFINED",
            "required_clauses": "observed clock time tau_obs; EM fine-structure readout alpha_EM",
            "result_if_signed": "clock data compare directly to parent-side alpha drift",
            "failure_mode": "using internal flow time instead of observed clock time gives an unscored quantity",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "XID3228_1_EM_kinetic_owner",
            "claim_piece": "alpha owner",
            "formula": "S_EM=-1/4 int sqrt(-g_obs) Z_A(Phi) F_obs^2; alpha_EM proportional to Z_A^-1 after fixed charge normalization",
            "derivation_status": "CONDITIONAL_EXACT",
            "required_clauses": "observed Maxwell subblock; fixed charge normalization; no hidden representative Weyl/disformal coefficient",
            "result_if_signed": "d ln alpha_EM/dtau_obs = - d ln Z_A/dtau_obs",
            "failure_mode": "if charge normalization or Hodge/readout carries another coefficient, Xi_clock is not complete",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "XID3228_2_defect_norm_chain_rule",
            "claim_piece": "defect-norm derivative",
            "formula": "Z_A=Z_*+lambda_D <R_Q,R_Q>_P gives |D_tau ln Z_A| <= 2|lambda_D| ||R_Q|| ||D_tau R_Q|| / Z_min",
            "derivation_status": "DERIVED_FROM_3222_CONTRACT_CONDITIONAL",
            "required_clauses": "R_Q parent object; positive Z_min; parent inner product and observed derivative domain",
            "result_if_signed": "alpha drift is controlled by a product of residual amplitude and residual clock derivative",
            "failure_mode": "no parent-signed R_Q/Z_A contract means this remains a contract, not a live theorem",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "XID3228_3_root_taylor_product",
            "claim_piece": "near-root product law",
            "formula": "||R_Q|| <= ||D_m R_Q|| |Delta m| + O(Delta m^2); ||D_tau R_Q|| <= ||D_m R_Q|| |tau_clock_time| + transport error",
            "derivation_status": "DERIVED_CONDITIONALLY",
            "required_clauses": "same branch coordinate m; same operator norm; finite Hessian; transport identity D_tau R_Q = D_m R_Q tau_clock_time + E_transport",
            "result_if_signed": "|d ln alpha_EM/dtau_obs| <= C_D |Delta m tau_clock_time| + E_HO + E_transport",
            "failure_mode": "if tau_clock_time is not the branch velocity in the same R_Q direction, the Xi reduction is not valid",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "XID3228_4_xi_clock_identity",
            "claim_piece": "direct product target",
            "formula": "Xi_clock := C_D |Delta m tau_clock_time| with C_D=2|lambda_D|||D_mR_Q||^2/Z_min",
            "derivation_status": "PRODUCT_LAW_DERIVED_WITH_UNSIGNED_CLAUSES",
            "required_clauses": "XID3228_1 through XID3228_3 plus controlled higher-order/error terms",
            "result_if_signed": "Xi_clock is the parent-side row compared to the clock bound",
            "failure_mode": "do not split or fit C_D/Pi_clock unless the parent action supplies the split",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "XID3228_5_exact_root_silence",
            "claim_piece": "local exact-root clock silence",
            "formula": "R_Q=0 and D_tau R_Q finite imply D_tau ln Z_A=0 for the pure defect-norm term",
            "derivation_status": "EXACT_CONDITIONAL_ZERO",
            "required_clauses": "same local branch really satisfies R_Q=0; no linear Z_A term; no readout/Hodge coefficient leakage",
            "result_if_signed": "the defect-norm alpha channel is locally clock-silent without setting tau_clock_time by hand",
            "failure_mode": "linear kinetic owner, representative leakage, or nonzero R_Q reopens the clock bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    contract_rows = [
        {
            "clause_id": "XIC3228_0_parent_EM_block",
            "required_parent_clause": "observed EM kinetic block descends as Z_A(Phi) F_obs^2",
            "mathematical_need": "S_EM=-1/4 int sqrt(-g_obs) Z_A F_obs^2",
            "current_evidence": "3222 contract writes the defect-norm EM block but does not source-sign it",
            "status": "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "why_it_matters": "owns alpha rather than treating alpha as an external fitted parameter",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "XIC3228_1_alpha_normalization",
            "required_parent_clause": "fixed charge/readout normalization",
            "mathematical_need": "alpha_EM proportional to Z_A^-1, with no extra clock/species coefficient",
            "current_evidence": "1052/1809 warn that clock rows bound products only",
            "status": "UNSIGNED_NORMALIZATION",
            "why_it_matters": "prevents hiding drift in units, charge convention, or clock species",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "XIC3228_2_clock_generator",
            "required_parent_clause": "observed clock time generator",
            "mathematical_need": "D_tau is derivative with respect to tau_obs measured by the descended clock matter",
            "current_evidence": "3136 gives conditional observed-coframe clock theorem",
            "status": "CONDITIONAL_CLOCK_THEOREM_NOT_PARENT_SIGNED",
            "why_it_matters": "clock data score observed time, not an internal flow coordinate",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "XIC3228_3_same_branch_transport",
            "required_parent_clause": "same-branch transport identity",
            "mathematical_need": "D_tau R_Q = D_m R_Q tau_clock_time + E_transport",
            "current_evidence": "not found as a parent row; 3227 only defines tau_clock_time product maps",
            "status": "MISSING_CORE_OWNER",
            "why_it_matters": "this is the exact bridge from defect-norm alpha to clock drift",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "XIC3228_4_finite_remainder",
            "required_parent_clause": "finite Taylor/Hessian remainder",
            "mathematical_need": "E_HO + E_transport bounded below the clock residual budget",
            "current_evidence": "3223/3226 name finite Hessian guards but do not source coefficients",
            "status": "BOUND_TEMPLATE_ONLY",
            "why_it_matters": "keeps Xi_clock from being a first-order mirage with uncontrolled second-order debt",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "XIC3228_5_data_comparison",
            "required_parent_clause": "clock-bound comparison row",
            "mathematical_need": "Xi_clock + E_HO + E_transport <= B_clock",
            "current_evidence": f"B_clock is real: {clock_1sigma:.6e} yr^-1 at 1sigma and {clock_2sigma:.6e} yr^-1 at 2sigma",
            "status": "DATA_SIDE_READY_PARENT_SIDE_MISSING",
            "why_it_matters": "turns the derivation into a falsifiable local coupling bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    bound_rows = [
        {
            "bound_id": "XIB3228_0_clock_1sigma",
            "quantity": "Xi_clock + E_HO + E_transport",
            "required_bound": f"<= {clock_1sigma:.6e}",
            "units": "yr^-1",
            "source": "PC3225_0_clock_1sigma / ACB1052_2",
            "interpretation": "best current 1sigma clock pressure gate",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "XIB3228_1_clock_2sigma",
            "quantity": "Xi_clock + E_HO + E_transport",
            "required_bound": f"<= {clock_2sigma:.6e}",
            "units": "yr^-1",
            "source": "PC3225_1_clock_2sigma / ACB1052_2",
            "interpretation": "best current 2sigma clock pressure gate",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "XIB3228_2_exact_root_branch",
            "quantity": "defect-norm contribution to Xi_clock",
            "required_bound": "0 if R_Q=0 and no leakage",
            "units": "yr^-1",
            "source": "derived from chain rule for lambda_D<R_Q,R_Q>",
            "interpretation": "possible local silence mechanism; not active until same-branch root and no-leakage clauses are signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "XIB3228_3_offroot_branch",
            "quantity": "Xi_clock",
            "required_bound": "C_D |Delta m tau_clock_time| <= B_clock - E_HO - E_transport",
            "units": "yr^-1",
            "source": "3226 package plus 3228 chain-rule derivation",
            "interpretation": "finite branch score equation; needs parent value/bound for the left side",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    obstruction_rows = [
        {
            "obstruction_id": "OBS3228_0_not_just_missing",
            "object": "Xi_clock",
            "what_was_derived": "the product law follows from a logarithmic derivative of Z_A and the defect-norm chain rule",
            "what_is_still_unsigned": "parent-signed EM block, alpha normalization, clock generator, same-branch transport",
            "best_next_attack": "derive D_tau R_Q = D_m R_Q tau_clock_time + E_transport",
            "severity": "CORE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "OBS3228_1_clock_tau_owner",
            "object": "tau_clock_time",
            "what_was_derived": "observed clocks measure proper time if observed-coframe matter descent is parent-signed",
            "what_is_still_unsigned": "the parent action has not signed the observed-coframe matter functor for clock species",
            "best_next_attack": "promote the 3136 conditional theorem into a parent action clause or demote to closure",
            "severity": "HIGH",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "OBS3228_2_alpha_owner",
            "object": "Z_A/alpha_EM",
            "what_was_derived": "if alpha_EM is owned by Z_A then drift is -D_tau ln Z_A",
            "what_is_still_unsigned": "charge normalization and no hidden Hodge/readout coefficient",
            "best_next_attack": "write exact Maxwell-subblock readout/no-leakage clause",
            "severity": "HIGH",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "OBS3228_3_data_side",
            "object": "clock bound",
            "what_was_derived": "data side already supplies a numeric 2.1e-18 yr^-1 pressure gate",
            "what_is_still_unsigned": "none on the bound itself; only theory-side product row",
            "best_next_attack": "compare only after Xi_clock or its upper bound is parent-derived",
            "severity": "LOW_DATA_READY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3228_0_result",
            "decision": "XI_CLOCK_PRODUCT_LAW_DERIVED_CONDITIONALLY_PARENT_OWNER_NOT_SIGNED",
            "because": "the logarithmic derivative of a defect-norm EM kinetic coefficient yields Xi_clock plus explicit higher-order/transport errors, but the parent action has not signed the EM owner, observed clock generator, or same-branch transport identity",
            "claim_status": "NO_ALPHA_NO_CLOCK_NO_WEP_NO_R10_NO_LOCAL_GR_CLAIM",
            "next_action": "attack the same-branch transport identity D_tau R_Q = D_m R_Q tau_clock_time + E_transport, because that is the core bridge from MTS residual dynamics to the clock bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3228_1_next_target",
            "decision": "3229-Y5-R2FR-same-branch-clock-transport-identity-for-DtauRQ-under-AX1090",
            "because": "without this identity Xi_clock remains a conditional product law; with it, the clock gate becomes a real parent-side bound or an exact-root silence theorem",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "derive or refute D_tau R_Q = D_m R_Q tau_clock_time + E_transport from quotient/readout geometry and the EM residual branch",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, derivation_rows, contract_rows, bound_rows, obstruction_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    obstruction_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, DERIVATION, CONTRACT, BOUNDS, OBSTRUCTIONS, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    chain_rule_present = any(row["step_id"] == "XID3228_2_defect_norm_chain_rule" for row in derivation_rows)
    xi_identity_present = any(row["step_id"] == "XID3228_4_xi_clock_identity" for row in derivation_rows)
    exact_zero_present = any(row["step_id"] == "XID3228_5_exact_root_silence" for row in derivation_rows)
    transport_obstruction = any(row["clause_id"] == "XIC3228_3_same_branch_transport" and row["status"] == "MISSING_CORE_OWNER" for row in contract_rows)
    numeric_bounds = sum(maybe_float(str(row["required_bound"]).replace("<=", "").strip()) is not None for row in bound_rows)
    claim_true_count = 0
    claim_allowed_count = 0
    for rows in [input_rows, derivation_rows, contract_rows, bound_rows, obstruction_rows, decision_rows]:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_true_count += 1
            if str(row.get("claim_allowed", "")).lower() == "true":
                claim_allowed_count += 1
    no_fw_outputs = all(FW not in [path, *path.parents] for path in out_paths + [DOC])

    csv_parse_ok = True
    csv_parse_detail: list[str] = []
    for path in out_paths:
        try:
            parsed = read_csv(path)
            if not parsed:
                csv_parse_ok = False
            csv_parse_detail.append(path.name)
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_detail.append(f"{path.name}:{exc}")

    return [
        {"check_id": "VAL3228_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3228_01_chain_rule_present", "pass": b(chain_rule_present), "detail": "D_tau ln Z_A defect-norm chain rule staged", "generated_utc": now},
        {"check_id": "VAL3228_02_xi_identity_present", "pass": b(xi_identity_present), "detail": "Xi_clock identity derived conditionally", "generated_utc": now},
        {"check_id": "VAL3228_03_exact_root_zero_present", "pass": b(exact_zero_present), "detail": "exact-root defect-norm silence clause staged", "generated_utc": now},
        {"check_id": "VAL3228_04_transport_core_missing_explicit", "pass": b(transport_obstruction), "detail": "same-branch transport identity is the core missing owner", "generated_utc": now},
        {"check_id": "VAL3228_05_numeric_clock_bounds", "pass": b(numeric_bounds >= 2), "detail": f"numeric_clock_bounds={numeric_bounds}", "generated_utc": now},
        {"check_id": "VAL3228_06_claims_blocked", "pass": b(claim_true_count == 0 and claim_allowed_count == 0), "detail": f"claim_rows_true={claim_true_count};claim_allowed={claim_allowed_count}", "generated_utc": now},
        {"check_id": "VAL3228_07_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3228_08_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3228_09_next_target", "pass": b(decision_rows[-1]["decision"].startswith("3229-")), "detail": str(decision_rows[-1]["decision"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    obstruction_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3228 - Xi-clock Product Row Or Clock-tau Owner under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3228 does make a mathematical move. It does not merely list a missing row.

If the observed EM kinetic coefficient owns the fine-structure readout,

```text
S_EM = -1/4 int sqrt(-g_obs) Z_A(Phi) F_obs^2,
alpha_EM proportional to Z_A^-1,
```

then the clock observable is controlled by the logarithmic derivative:

```text
|d ln alpha_EM / d tau_obs| = |d ln Z_A / d tau_obs|.
```

For the defect-norm route

```text
Z_A = Z_* + lambda_D <R_Q,R_Q>_P,
```

the chain rule gives

```text
|D_tau ln Z_A| <= 2 |lambda_D| ||R_Q|| ||D_tau R_Q|| / Z_min.
```

Near the same local root branch this becomes

```text
||R_Q|| <= ||D_m R_Q|| |Delta m| + O(Delta m^2),
||D_tau R_Q|| <= ||D_m R_Q|| |tau_clock_time| + E_transport,
```

so the direct clock product is exactly the right target:

```text
Xi_clock := C_D |Delta m tau_clock_time|
C_D := 2 |lambda_D| ||D_m R_Q||^2 / Z_min
|d ln alpha_EM / d tau_obs| <= Xi_clock + E_HO + E_transport.
```

The data side is ready:

```text
Xi_clock + E_HO + E_transport <= 2.1e-18 yr^-1   (1sigma)
Xi_clock + E_HO + E_transport <= 3.2e-18 yr^-1   (2sigma)
```

The parent-side product law is derived conditionally, but not claimable. The core missing owner is now precise:

```text
D_tau R_Q = D_m R_Q tau_clock_time + E_transport.
```

If the exact same local branch has `R_Q=0` and no linear/readout leakage, the defect-norm alpha channel is clock-silent without setting `tau_clock_time` by hand. That is a real possible route, but it is still unsigned.

Current verdict: `XI_CLOCK_PRODUCT_LAW_DERIVED_CONDITIONALLY_PARENT_OWNER_NOT_SIGNED`.

## Xi-clock Product Derivation

{md_table(derivation_rows, ["step_id", "claim_piece", "formula", "derivation_status", "required_clauses", "result_if_signed", "failure_mode", "valid_for_claim"])}

## Parent Xi-clock Contract

{md_table(contract_rows, ["clause_id", "required_parent_clause", "mathematical_need", "current_evidence", "status", "why_it_matters", "valid_for_claim"])}

## Xi-clock Bound Interface

{md_table(bound_rows, ["bound_id", "quantity", "required_bound", "units", "source", "interpretation", "claim_allowed", "valid_for_claim"])}

## Owner Obstruction Ledger

{md_table(obstruction_rows, ["obstruction_id", "object", "what_was_derived", "what_is_still_unsigned", "best_next_attack", "severity", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3228_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3228_XI_CLOCK_PRODUCT_DERIVATION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3228_PARENT_XI_CLOCK_CONTRACT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3228_XI_CLOCK_BOUND_INTERFACE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3228_OWNER_OBSTRUCTION_LEDGER.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3228_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3228_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, derivation_rows, contract_rows, bound_rows, obstruction_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (DERIVATION, derivation_rows),
        (CONTRACT, contract_rows),
        (BOUNDS, bound_rows),
        (OBSTRUCTIONS, obstruction_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, derivation_rows, contract_rows, bound_rows, obstruction_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, derivation_rows, contract_rows, bound_rows, obstruction_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3227-Y5-R2FR-Pi-clock-or-CD-source-row-acquisition-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3227_INPUTS.csv"
PI_AUDIT = OUT / "P8_Y5_R2FR_3227_PI_CLOCK_SOURCE_AUDIT.csv"
SCORECARD = OUT / "P8_Y5_R2FR_3227_CLOCK_SOURCE_CANDIDATE_SCORECARD.csv"
INTERFACE = OUT / "P8_Y5_R2FR_3227_CD_OR_PICLOCK_ACQUISITION_INTERFACE.csv"
TEMPLATE = OUT / "P8_Y5_R2FR_3227_FIRST_USABLE_ROW_TEMPLATE.csv"
DECISION = OUT / "P8_Y5_R2FR_3227_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3227_VALIDATION.csv"

PRODUCT_3225 = OUT / "P8_Y5_R2FR_3225_PRODUCT_CONSTRAINTS_FROM_ANCHORS.csv"
CLOCK_1052 = OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"


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
        "input_id": "SRC3227_00_3226_doc",
        "location": "post_checkpoint",
        "relative_path": "3226-Y5-R2FR-CD-coefficient-package-or-clock-product-saturation-bound-under-AX1090.md",
        "role": "3226 handoff selecting Pi_clock or direct C_D acquisition",
        "terms": ["Pi_clock", "C_D", "3227", "2.1e-18"],
    },
    {
        "input_id": "SRC3227_01_3226_package",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3226_CD_COEFFICIENT_PACKAGE.csv",
        "role": "C_D and Pi_clock package definitions",
        "terms": ["CD3226_0_definition", "CD3226_1_clock_product", "Delta m"],
    },
    {
        "input_id": "SRC3227_02_3226_acquisition",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3226_CD_ACQUISITION_TARGETS.csv",
        "role": "direct C_D and Pi_clock missing-row queue",
        "terms": ["ACQ3226_0_direct_CD", "ACQ3226_1_clock_projection"],
    },
    {
        "input_id": "SRC3227_03_3225_products",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3225_PRODUCT_CONSTRAINTS_FROM_ANCHORS.csv",
        "role": "clock/WEP product constraints from real anchors",
        "terms": ["PC3225_0_clock_1sigma", "PC3225_1_clock_2sigma", "PC3225_2_WEP_alpha"],
    },
    {
        "input_id": "SRC3227_04_1052_doc",
        "location": "post_checkpoint",
        "relative_path": "1052-Y5-R10-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md",
        "role": "clock tau normalization attempt",
        "terms": ["tau_clock_time", "2.1e-18", "not parent-derived"],
    },
    {
        "input_id": "SRC3227_05_1052_clock_bound",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
        "role": "source-backed clock product bound ledger",
        "terms": ["ACB1052_2", "2.1e-18", "3.2e-18"],
    },
    {
        "input_id": "SRC3227_06_1052_tau_audit",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv",
        "role": "tau_clock/Xhat audit",
        "terms": ["TCN1052_0_product_definition", "parent", "tau_clock_time"],
    },
    {
        "input_id": "SRC3227_07_1809_doc",
        "location": "post_checkpoint",
        "relative_path": "1809-Y5-R2FR-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md",
        "role": "current branch repetition of clock product gate",
        "terms": ["2.1e-18", "product-map definitions", "not parent-derived"],
    },
    {
        "input_id": "SRC3227_08_1809_tau_audit",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_PARENT_QLOC_1809_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv",
        "role": "current branch tau audit",
        "terms": ["tau_clock_time", "Xhat", "valid_for_claim"],
    },
    {
        "input_id": "SRC3227_09_3135_doc",
        "location": "post_checkpoint",
        "relative_path": "3135-Y5-R2FR-clock-readout-chain-sign-quarantine-and-limit-gate-under-AX1090.md",
        "role": "observable clock readout chain quarantine",
        "terms": ["R_clock", "d tau_clk", "missing parent-owned"],
    },
    {
        "input_id": "SRC3227_10_3135_lemma",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3135_READOUT_CHAIN_LEMMA.csv",
        "role": "machine readout-chain lemma",
        "terms": ["R_clock", "proper time", "valid_for_claim"],
    },
    {
        "input_id": "SRC3227_11_3136_doc",
        "location": "post_checkpoint",
        "relative_path": "3136-Y5-R2FR-observed-coframe-clock-functional-owner-under-AX1090.md",
        "role": "conditional observed-coframe clock theorem",
        "terms": ["observed clocks measure observed metric proper time", "parent has not signed", "R_clock"],
    },
    {
        "input_id": "SRC3227_12_3136_theorem",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3136_OBSERVED_CLOCK_FUNCTIONAL_THEOREM.csv",
        "role": "machine observed-clock theorem",
        "terms": ["observed coframe", "clock", "parent"],
    },
    {
        "input_id": "SRC3227_13_2599_doc",
        "location": "post_checkpoint",
        "relative_path": "2599-Y5-R2FR-boundary-clock-normalized-tau-owner-or-delta-tau-source-pack.md",
        "role": "boundary clock tau owner attempt",
        "terms": ["tau_obs", "boundary-clock", "remain unsigned"],
    },
    {
        "input_id": "SRC3227_14_2599_delta_tau",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_BOUNDARY_CLOCK_TAU_2599_DELTA_TAU_SOURCE_PACK.csv",
        "role": "delta_tau source pack",
        "terms": ["delta_tau", "valid_for_claim", "source"],
    },
    {
        "input_id": "SRC3227_15_2600_doc",
        "location": "post_checkpoint",
        "relative_path": "2600-Y5-R2FR-Tobs-delta-tau-norm-owner-or-boundary-clock-action-clause.md",
        "role": "Tobs/delta_tau norm owner attempt",
        "terms": ["C_Tobs_tau", "not yet parent-signed", "Delta_JH_delta_tau"],
    },
    {
        "input_id": "SRC3227_16_2600_norm",
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


def best_clock_bound(bound_column: str) -> float:
    rows = read_csv(CLOCK_1052)
    for row in rows:
        if row.get("bound_id") == "ACB1052_2":
            value = maybe_float(row.get(bound_column))
            if value is None:
                raise ValueError(f"missing best clock bound {bound_column}")
            return value
    raise ValueError("missing ACB1052_2")


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
    ledger_1sigma = best_clock_bound("product_bound_1sigma_yr_inv")
    ledger_2sigma = best_clock_bound("product_bound_2sigma_yr_inv")

    pi_rows = [
        {
            "audit_id": "PIC3227_0_definition",
            "target": "Pi_clock",
            "formula": "Pi_clock := |Delta m tau_clock_time|",
            "status": "DEFINED_NOT_SOURCE_SIGNED",
            "evidence": "3226 defines the needed projection product; no parent row supplies Delta m and tau_clock_time together",
            "missing_for_claim": "EM-attached Delta m; parent-owned tau_clock_time; shared normalization and units",
            "next_action": "try a direct Xi_clock product row before forcing an artificial split",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "PIC3227_1_clock_product_anchor",
            "target": "clock anchor",
            "formula": "|b_alpha*tau_clock_time| <= B_clock",
            "status": "SOURCE_BACKED_PRODUCT_BOUND_AVAILABLE",
            "evidence": f"ACB1052_2 gives B_clock={ledger_1sigma:.6e} yr^-1 at 1sigma and {ledger_2sigma:.6e} yr^-1 at 2sigma",
            "missing_for_claim": "standalone b_alpha or MTS-owned product coefficient",
            "next_action": "use this as a bound on Xi_clock := C_D Pi_clock, not as a standalone b_alpha measurement",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "PIC3227_2_delta_m_owner",
            "target": "Delta m",
            "formula": "finite EM off-root amplitude entering |b_alpha_m| <= C_D |Delta m|",
            "status": "MISSING_EM_ATTACHED_SOURCE_ROW",
            "evidence": "3225/3226 keep Delta m as the finite branch amplitude but do not parent-attach it to the EM R_Q/Z_A branch",
            "missing_for_claim": "same-branch amplitude law; source path; units; support domain",
            "next_action": "do not import local amplitude from a different branch without a same-operator map",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "PIC3227_3_tau_clock_owner",
            "target": "tau_clock_time",
            "formula": "tau_clock_time := d chi_X/dt or clock readout derivative after quotient/readout map",
            "status": "CONDITIONAL_READOUT_NOT_PARENT_DYNAMICS",
            "evidence": "1052/1809 define product maps; 3135/3136 derive conditional observable clock readout if observed-coframe matter descent is parent-signed",
            "missing_for_claim": "parent-signed chi_X/tau dynamics or observed-coframe matter functor plus clock species normalization",
            "next_action": "target a product coefficient Xi_clock that bypasses premature tau splitting",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "PIC3227_4_domain_map",
            "target": "clock/alpha same-domain map",
            "formula": "d ln(alpha_EM)/dt = b_alpha tau_clock_time",
            "status": "PRODUCT_MAP_ONLY",
            "evidence": "clock rows constrain a product; they do not decide whether alpha, clock species, and time generator are separable",
            "missing_for_claim": "separation theorem or direct product row for the same observable domain",
            "next_action": "prefer direct product acquisition: Xi_clock := C_D |Delta m tau_clock_time|",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "PIC3227_5_direct_CD_owner",
            "target": "C_D",
            "formula": "C_D := 2 |lambda_D| ||D_m R_Q||^2 / Z_min",
            "status": "DEFINITION_EXACT_INPUTS_MISSING",
            "evidence": "3226 packages the finite coefficient; lambda_D, D_m R_Q, and Z_min remain unsourced",
            "missing_for_claim": "lambda_D; D_m R_Q norm; Z_min; units; source paths",
            "next_action": "source direct C_D only if a parent coefficient package exists; otherwise use Xi_clock product gate",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "PIC3227_6_verdict",
            "target": "Pi_clock acquisition",
            "formula": "Pi_clock standalone row",
            "status": "PI_CLOCK_NOT_SOURCE_SIGNED",
            "evidence": "no inspected source supplies a numeric/source-backed Pi_clock row with Delta m and tau_clock_time in the same branch",
            "missing_for_claim": "either source-backed Pi_clock or direct source-backed Xi_clock",
            "next_action": "stage Xi_clock := C_D Pi_clock as the first claim-shaped acquisition row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    score_rows = [
        {
            "candidate_id": "CAND3227_0_1052_clock_bound",
            "source": "1052 + ACB1052_2",
            "what_it_gives": f"real clock product bound B_clock={ledger_1sigma:.6e} yr^-1",
            "what_it_does_not_give": "Pi_clock or C_D separately",
            "score_use": "usable as Xi_clock upper bound only",
            "blocking_gap": "MTS product coefficient not parent-derived",
            "status": "KEEP_AS_NUMERIC_ANCHOR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "CAND3227_1_1052_1809_tau_audits",
            "source": "1052/1809 tau-clock/Xhat audits",
            "what_it_gives": "product-map definitions for tau_clock_time and chi_X",
            "what_it_does_not_give": "parent-owned tau dynamics or normalization",
            "score_use": "definition support",
            "blocking_gap": "chi_X parent state and local time projection are not derived",
            "status": "CONDITIONAL_ONLY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "CAND3227_2_3135_readout_chain",
            "source": "3135 readout-chain limit gate",
            "what_it_gives": "internal flow sign quarantine and observable clock-readout structure",
            "what_it_does_not_give": "numerical tau_clock_time or EM amplitude",
            "score_use": "protects against rejecting a branch for internal sign alone",
            "blocking_gap": "observed coframe/metric readout owner still required",
            "status": "THEOREM_SHAPE_ONLY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "CAND3227_3_3136_clock_functional",
            "source": "3136 observed-coframe clock theorem",
            "what_it_gives": "conditional theorem: observed-coframe matter descent implies observed clocks measure observed metric proper time",
            "what_it_does_not_give": "parent-signed matter descent or numeric Pi_clock",
            "score_use": "strongest conceptual clock owner route",
            "blocking_gap": "parent has not signed observed coframe, matter coupling, and clock species normalization",
            "status": "BEST_DERIVATION_ROUTE_CONDITIONAL",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "CAND3227_4_2599_boundary_tau",
            "source": "2599 boundary clock tau owner",
            "what_it_gives": "boundary-clock class and delta_tau source-pack shape",
            "what_it_does_not_give": "fixed generator theorem or product coefficient",
            "score_use": "alternate route to tau ownership",
            "blocking_gap": "boundary clock/reference phase space and unique extension remain unsigned",
            "status": "OWNER_ROUTE_INCOMPLETE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "CAND3227_5_2600_Tobs_norm",
            "source": "2600 Tobs/delta_tau norm owner",
            "what_it_gives": "exact response law Delta_JH_delta_tau <= C_Tobs_tau ||delta tau_obs||_B",
            "what_it_does_not_give": "C_Tobs_tau value or clock action clause",
            "score_use": "could become a tau-bound coefficient if norms are parent-owned",
            "blocking_gap": "common domain/codomain norm and boundary action are not parent-signed",
            "status": "COEFFICIENT_ROUTE_INCOMPLETE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "CAND3227_6_3226_direct_CD",
            "source": "3226 C_D package",
            "what_it_gives": "compact finite coefficient definition",
            "what_it_does_not_give": "lambda_D, D_m R_Q, Z_min, or units",
            "score_use": "best direct coefficient target if source rows are found",
            "blocking_gap": "no parent coefficient package discovered",
            "status": "DIRECT_CD_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    interface_rows = [
        {
            "interface_id": "XIC3227_0_definition",
            "quantity": "Xi_clock",
            "formula": "Xi_clock := C_D Pi_clock = C_D |Delta m tau_clock_time|",
            "numeric_bound": "not_applicable",
            "units": "yr^-1 in clock-time convention after source normalization",
            "source_basis": "3225/3226 finite branch plus 1052 clock product anchor",
            "claim_gate": "requires parent-derived/source-backed Xi_clock or both C_D and Pi_clock",
            "status": "DEFINED_PRODUCT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "interface_id": "XIC3227_1_clock_1sigma_bound",
            "quantity": "Xi_clock",
            "formula": "Xi_clock <= B_clock_1sigma",
            "numeric_bound": f"{clock_1sigma:.6e}",
            "units": "yr^-1",
            "source_basis": "PC3225_0_clock_1sigma / ACB1052_2",
            "claim_gate": "diagnostic unless Xi_clock is source-backed",
            "status": "REAL_BOUND_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "interface_id": "XIC3227_2_clock_2sigma_bound",
            "quantity": "Xi_clock",
            "formula": "Xi_clock <= B_clock_2sigma",
            "numeric_bound": f"{clock_2sigma:.6e}",
            "units": "yr^-1",
            "source_basis": "PC3225_1_clock_2sigma / ACB1052_2",
            "claim_gate": "diagnostic unless Xi_clock is source-backed",
            "status": "REAL_BOUND_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "interface_id": "XIC3227_3_direct_product_acquisition",
            "quantity": "Xi_clock",
            "formula": "derive/source C_D |Delta m tau_clock_time| directly from parent clock/EM coupling",
            "numeric_bound": "MISSING_PARENT_VALUE",
            "units": "yr^-1",
            "source_basis": "none yet",
            "claim_gate": "would avoid arbitrary splitting of C_D, Delta m, and tau_clock_time",
            "status": "PREFERRED_NEXT_SOURCE_ROW",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "interface_id": "XIC3227_4_split_acquisition",
            "quantity": "C_D and Pi_clock",
            "formula": "source C_D and Pi_clock separately, then multiply",
            "numeric_bound": "MISSING_SPLIT_VALUES",
            "units": "C_D units times Pi_clock units",
            "source_basis": "3226 package definitions",
            "claim_gate": "both rows must be same branch, same normalization, same clock domain",
            "status": "SECONDARY_ROUTE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "interface_id": "XIC3227_5_refusal_rule",
            "quantity": "claim rule",
            "formula": "no pass if Xi_clock is inferred by setting Pi_clock=1, tau_clock_time=H0, or Delta m=1",
            "numeric_bound": "not_applicable",
            "units": "not_applicable",
            "source_basis": "1052/1809/3226 guardrails",
            "claim_gate": "reject assumed-normalization shortcuts",
            "status": "ACTIVE_GUARD",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    template_rows = [
        {
            "row_id": "ROW3227_0_direct_Xi_clock",
            "target": "Xi_clock",
            "value": "MISSING_PARENT_VALUE",
            "units": "yr^-1",
            "source_path": "MISSING_PARENT_SOURCE",
            "normalization": "same observed clock-time convention as ACB1052_2",
            "required_companion": "derivation showing Xi_clock=C_D|Delta m tau_clock_time| in the EM alpha branch",
            "status": "BEST_FIRST_ROW_TEMPLATE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "ROW3227_1_split_Pi_clock",
            "target": "Pi_clock",
            "value": "MISSING_PARENT_VALUE",
            "units": "clock projection units",
            "source_path": "MISSING_PARENT_SOURCE",
            "normalization": "must include Delta m and tau_clock_time in one source row",
            "required_companion": "C_D value or bound from same EM R_Q/Z_A branch",
            "status": "SECONDARY_ROW_TEMPLATE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "ROW3227_2_split_C_D",
            "target": "C_D",
            "value": "MISSING_PARENT_VALUE",
            "units": "inverse Pi_clock units times yr^-1",
            "source_path": "MISSING_PARENT_SOURCE",
            "normalization": "lambda_D, D_m R_Q, and Z_min all source-backed",
            "required_companion": "Pi_clock value or direct Xi_clock product row",
            "status": "SECONDARY_ROW_TEMPLATE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3227_0_result",
            "decision": "PI_CLOCK_STANDALONE_NOT_SOURCE_SIGNED_XI_CLOCK_PRODUCT_INTERFACE_STAGED",
            "because": "real clock data bound the product channel, but no inspected source supplies a parent-owned standalone Pi_clock or direct C_D coefficient",
            "claim_status": "NO_ALPHA_NO_CLOCK_NO_WEP_NO_R10_NO_LOCAL_GR_CLAIM",
            "next_action": "derive or source Xi_clock := C_D |Delta m tau_clock_time| directly; do not split tau and amplitude unless the parent action forces the split",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3227_1_next_target",
            "decision": "3228-Y5-R2FR-Xi-clock-product-row-or-clock-tau-owner-under-AX1090",
            "because": "Xi_clock is the first claim-shaped clock target: the data side is already bounded at 2.1e-18 yr^-1, so only the parent-side product row is missing",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "first try a direct product derivation from EM coupling/readout; fallback to clock-tau owner if the product route cannot be signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, pi_rows, score_rows, interface_rows, template_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    pi_rows: list[dict[str, object]],
    score_rows: list[dict[str, object]],
    interface_rows: list[dict[str, object]],
    template_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, PI_AUDIT, SCORECARD, INTERFACE, TEMPLATE, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    best_clock_numeric = maybe_float(best_clock_bound("product_bound_1sigma_yr_inv")) == product_bound("PC3225_0_clock_1sigma")
    pi_not_signed = any(row["audit_id"] == "PIC3227_6_verdict" and row["status"] == "PI_CLOCK_NOT_SOURCE_SIGNED" for row in pi_rows)
    xi_defined = any(row["interface_id"] == "XIC3227_0_definition" and "Xi_clock := C_D Pi_clock" in row["formula"] for row in interface_rows)
    xi_numeric_bounds = sum(maybe_float(row.get("numeric_bound")) is not None for row in interface_rows)
    claim_true_count = 0
    invalid_claim_placeholders = 0
    for rows in [input_rows, pi_rows, score_rows, interface_rows, template_rows, decision_rows]:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_true_count += 1
                joined = " ".join(str(value) for value in row.values()).upper()
                if "MISSING" in joined:
                    invalid_claim_placeholders += 1
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
        {"check_id": "VAL3227_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3227_01_best_clock_bound_numeric", "pass": b(best_clock_numeric), "detail": "ACB1052_2 and PC3225_0 both give 2.1e-18 yr^-1", "generated_utc": now},
        {"check_id": "VAL3227_02_pi_clock_not_source_signed", "pass": b(pi_not_signed), "detail": "standalone Pi_clock row remains absent", "generated_utc": now},
        {"check_id": "VAL3227_03_xi_clock_defined", "pass": b(xi_defined), "detail": "Xi_clock := C_D Pi_clock = C_D|Delta m tau_clock_time|", "generated_utc": now},
        {"check_id": "VAL3227_04_xi_clock_numeric_bounds", "pass": b(xi_numeric_bounds >= 2), "detail": f"numeric_bounds={xi_numeric_bounds}", "generated_utc": now},
        {"check_id": "VAL3227_05_claims_blocked", "pass": b(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3227_06_no_placeholder_claims", "pass": b(invalid_claim_placeholders == 0), "detail": f"invalid_claim_placeholders={invalid_claim_placeholders}", "generated_utc": now},
        {"check_id": "VAL3227_07_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3227_08_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3227_09_next_target", "pass": b(decision_rows[-1]["decision"].startswith("3228-")), "detail": str(decision_rows[-1]["decision"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    pi_rows: list[dict[str, object]],
    score_rows: list[dict[str, object]],
    interface_rows: list[dict[str, object]],
    template_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3227 - Pi-clock Or C_D Source Row Acquisition under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3227 tries the clock projection route first:

```text
Pi_clock := |Delta m tau_clock_time|.
```

The standalone `Pi_clock` row is not source-signed. The real clock evidence constrains a product, not the split pieces:

```text
|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1  (best current 1sigma clock row)
|b_alpha*tau_clock_time| <= 3.2e-18 yr^-1  (best current 2sigma clock row)
```

Using the finite branch from 3226,

```text
|b_alpha_m| <= C_D |Delta m|
C_D := 2 |lambda_D| ||D_m R_Q||^2 / Z_min
```

the clean next product target is therefore:

```text
Xi_clock := C_D Pi_clock = C_D |Delta m tau_clock_time|
Xi_clock <= 2.1e-18 yr^-1   (1sigma diagnostic bound)
Xi_clock <= 3.2e-18 yr^-1   (2sigma diagnostic bound)
```

That is the useful leap: do not keep forcing `C_D`, `Delta m`, and `tau_clock_time` apart unless the parent action itself forces that split. A direct `Xi_clock` source row would be cleaner and harder to attack.

Current verdict: `PI_CLOCK_STANDALONE_NOT_SOURCE_SIGNED_XI_CLOCK_PRODUCT_INTERFACE_STAGED`.

## Pi-clock Source Audit

{md_table(pi_rows, ["audit_id", "target", "formula", "status", "evidence", "missing_for_claim", "next_action", "valid_for_claim"])}

## Clock Source Candidate Scorecard

{md_table(score_rows, ["candidate_id", "source", "what_it_gives", "what_it_does_not_give", "score_use", "blocking_gap", "status", "valid_for_claim"])}

## C_D Or Pi-clock Acquisition Interface

{md_table(interface_rows, ["interface_id", "quantity", "formula", "numeric_bound", "units", "source_basis", "claim_gate", "status", "valid_for_claim"])}

## First Usable Row Template

{md_table(template_rows, ["row_id", "target", "value", "units", "source_path", "normalization", "required_companion", "status", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3227_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3227_PI_CLOCK_SOURCE_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3227_CLOCK_SOURCE_CANDIDATE_SCORECARD.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3227_CD_OR_PICLOCK_ACQUISITION_INTERFACE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3227_FIRST_USABLE_ROW_TEMPLATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3227_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3227_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, pi_rows, score_rows, interface_rows, template_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (PI_AUDIT, pi_rows),
        (SCORECARD, score_rows),
        (INTERFACE, interface_rows),
        (TEMPLATE, template_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, pi_rows, score_rows, interface_rows, template_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, pi_rows, score_rows, interface_rows, template_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()

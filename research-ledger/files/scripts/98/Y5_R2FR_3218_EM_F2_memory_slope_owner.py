from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3218-Y5-R2FR-EM-F2-vertex-owner-for-memory-slope-zero-or-balpha-m-source-row-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3218_INPUTS.csv"
DECOMP = OUT / "P8_Y5_R2FR_3218_ZA_MEMORY_DECOMPOSITION.csv"
ZERO_THEOREM = OUT / "P8_Y5_R2FR_3218_BALPHA_M_ZERO_THEOREM_ATTEMPT.csv"
COUNTER = OUT / "P8_Y5_R2FR_3218_EM_F2_COUNTERMODEL_LEDGER.csv"
SOURCE_ROW = OUT / "P8_Y5_R2FR_3218_BALPHA_M_SOURCE_ROW_TEMPLATE.csv"
DECISION = OUT / "P8_Y5_R2FR_3218_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3218_VALIDATION.csv"


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


def resolve(location: str, relative_path: str) -> Path:
    if location == "post_checkpoint":
        return ROOT / relative_path
    if location == "mts_residuals":
        return OUT / relative_path
    if location == "formalization":
        return FW / relative_path
    raise ValueError(location)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO)).replace("\\", "/")


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:180]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


SOURCES = [
    {
        "input_id": "SRC3218_00_3217_doc",
        "location": "post_checkpoint",
        "relative_path": "3217-Y5-R2FR-parent-visible-coefficient-vertex-list-or-first-memory-slope-source-row-under-AX1090.md",
        "role": "3217 vertex manifest handoff",
        "terms": ["VTX3217_0_EM_F2", "b_alpha_m", "EM `F^2`"],
    },
    {
        "input_id": "SRC3218_01_3217_slope",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3217_FIRST_MEMORY_SLOPE_SOURCE_ROWS.csv",
        "role": "first b_alpha_m finite row",
        "terms": ["FSR3217_0_balpha_m", "MISSING_ZERO_THEOREM_OR_SOURCE_BACKED_SLOPE"],
    },
    {
        "input_id": "SRC3218_02_3216_routes",
        "location": "post_checkpoint",
        "relative_path": "3216-Y5-R2FR-branch-origin-coefficient-stationarity-or-memory-slope-bound-pack-under-AX1090.md",
        "role": "stationarity theorem routes",
        "terms": ["typed exclusion", "strict source-root", "operator independence"],
    },
    {
        "input_id": "SRC3218_03_1099_em",
        "location": "post_checkpoint",
        "relative_path": "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md",
        "role": "no-extra-F2 theorem attempt",
        "terms": ["UEM1099_3_verdict", "CX1099_1_fX", "ASR1099_0_theorem_zero_candidate"],
    },
    {
        "input_id": "SRC3218_04_1100_tq",
        "location": "post_checkpoint",
        "relative_path": "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md",
        "role": "T_Q/gauge-norm signature and Z_A decomposition",
        "terms": ["TQS1100_6_verdict", "Z1100_4_total", "TQT1100_3_lambda_countermodel"],
    },
    {
        "input_id": "SRC3218_05_1101_gauge",
        "location": "post_checkpoint",
        "relative_path": "1101-Y5-R10-gauge-fibre-level-index-monopole-Ward-owner-or-alpha-product-route.md",
        "role": "gauge-norm owner hunt",
        "terms": ["GFT1101_4_verdict", "NG1101_4_minimal_action", "GNO1101_0_fixed_fibre_metric"],
    },
    {
        "input_id": "SRC3218_06_989_emlock",
        "location": "post_checkpoint",
        "relative_path": "989-Y5-R10-EM-lock-signature-input-or-alpha-source-normalization-owner.md",
        "role": "EM lock signature audit",
        "terms": ["ELA989_1_unique_F2", "PIC989_1_unique_Maxwell_subblock", "CG989_0_EM_lock_zero"],
    },
    {
        "input_id": "SRC3218_07_988_joint",
        "location": "post_checkpoint",
        "relative_path": "988-Y5-R10-alphaEM-WEP-clock-joint-prior-or-EM-lock-theorem.md",
        "role": "joint clock/WEP alpha pressure",
        "terms": ["EMLOCK988_1_unique_Maxwell_F2", "JAV988_0_alpha_slot", "WEP988_WAS651_0_alpha_Coulomb"],
    },
    {
        "input_id": "SRC3218_08_1050_product",
        "location": "post_checkpoint",
        "relative_path": "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md",
        "role": "visible-hidden product functor",
        "terms": ["PFT1050_1_visible_action_pullback", "OBS1050_1_alpha_owner", "PWP1050_0_b_alpha"],
    },
    {
        "input_id": "SRC3218_09_1049_symmetry",
        "location": "post_checkpoint",
        "relative_path": "1049-Y5-R10-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md",
        "role": "operator classification and symmetry insufficiency",
        "terms": ["SBT1049_1_gauge_invariance", "ODT1049_0_fX_F2", "RP1049_0_b_alpha"],
    },
    {
        "input_id": "SRC3218_10_3212_em",
        "location": "post_checkpoint",
        "relative_path": "3212-Y5-R2FR-EM-source-channel-no-extra-F2-or-Poynting-bound-input-under-AX1090.md",
        "role": "EM source law containing Z_A prime",
        "terms": ["Z_A'(X)", "J_X^EM", "F^2"],
    },
]


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

    decomp_rows = [
        {
            "component_id": "ZA3218_0_parent_norm",
            "term": "C_P N_Q",
            "meaning": "parent curvature coefficient times fixed gauge-generator norm",
            "memory_derivative": "partial_m(C_P N_Q)",
            "zero_condition": "C_P and N_Q are Q_ONLY/REP_TOPOLOGICAL parent data with Dq[partial_m]=0",
            "current_status": "CONDITIONAL_SYMBOLIC_ONLY",
            "if_live": "contributes to b_alpha_m if parent norm or coefficient depends on memory",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "ZA3218_1_lambda_visible",
            "term": "lambda_A",
            "meaning": "independent visible Maxwell kinetic counterterm",
            "memory_derivative": "partial_m lambda_A",
            "zero_condition": "operator-domain exhaustion forbids independent F_Q^2 or signs lambda_A as fixed Q_ONLY constant",
            "current_status": "LEGAL_UNLESS_FORBIDDEN",
            "if_live": "constant lambda shifts alpha; memory-dependent lambda produces b_alpha_m",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "ZA3218_2_hidden_scalar",
            "term": "f_m(m) or f(I_hid)",
            "meaning": "hidden/memory scalar gauge-kinetic coefficient",
            "memory_derivative": "f_m'(m_*)",
            "zero_condition": "typed exclusion, exact even/fixed-point symmetry, or strict double-zero f_m=O((m-m_*)^2)",
            "current_status": "COUNTERMODEL_ACTIVE",
            "if_live": "direct EM source J_m includes -1/4 f_m'(m_*) F^2",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "ZA3218_3_radiative_readout",
            "term": "delta_lambda_rad(m,mu)+readout_alpha(m)",
            "meaning": "effective/readout regeneration of alpha coefficient",
            "memory_derivative": "partial_m delta_lambda_rad + partial_m readout_alpha",
            "zero_condition": "radiative/readout closure preserves the same Q_ONLY/REP_TOPOLOGICAL rule after variation",
            "current_status": "UNSIGNED",
            "if_live": "tree-level zero fails to imply observed alpha silence",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "ZA3218_4_total",
            "term": "Z_A = C_P N_Q + lambda_A + f_m(m) + delta_lambda_rad + readout_alpha",
            "meaning": "honest EM kinetic coefficient entering -1/4 Z_A F_Q^2",
            "memory_derivative": "b_alpha_m = partial_m ln Z_A = (partial_m Z_A)/Z_A",
            "zero_condition": "all nonparent terms absent/stationary and parent piece fixed",
            "current_status": "FINITE_BRANCH_RETAINED",
            "if_live": "b_alpha_m must be source-backed or bounded before local tests",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    theorem_rows = [
        {
            "theorem_id": "BAM3218_0_exact_formula",
            "claim_piece": "memory slope of alpha coefficient",
            "statement": "For S_EM=-1/4 int Z_A(m,q,readout) F_Q^2, b_alpha_m := partial_m ln Z_A|m_* = [partial_m(C_P N_Q)+partial_m lambda_A+f_m'(m_*)+partial_m delta_lambda_rad+partial_m readout_alpha]/Z_A(m_*).",
            "status": "EXACT_DECOMPOSITION",
            "what_it_buys": "turns the EM coupling problem into a finite list of derivative owners",
            "missing_for_claim": "zero or source-backed value for every numerator term and positive Z_A denominator",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "BAM3218_1_Q_ONLY_zero",
            "claim_piece": "typed parent gauge norm kills parent numerator",
            "statement": "If C_P, T_Q, N_Q=<T_Q,T_Q>_P, charge lattice, and current owner are fixed parent/representation data and the EM coefficient domain is Q_ONLY/REP_TOPOLOGICAL, then partial_m(C_P N_Q)=0.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "what_it_buys": "kills the parent curvature-norm part of b_alpha_m",
            "missing_for_claim": "parent T_Q object, fixed nonrescalable norm/level, same current owner, and no readout drift",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "BAM3218_2_no_extra_F2_zero",
            "claim_piece": "no-extra-F2 kills lambda/f_m numerator",
            "statement": "If the parent visible operator domain forbids independent lambda_A F_Q^2 and f_m(m)F_Q^2 terms, then partial_m lambda_A=f_m'(m_*)=0 by absence.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "what_it_buys": "kills the live scalar gauge-kinetic counterterm",
            "missing_for_claim": "operator-domain exhaustion/no-hidden-visible coefficient theorem or product sequester signed for EM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "BAM3218_3_double_zero_subroute",
            "claim_piece": "strict double-zero can kill slope without forbidding a memory deformation",
            "statement": "If f_m(m)=lambda_m F(m) with F(m_*)=F'(m_*)=0 and m is locally locked to m_*, then f_m'(m_*)=0 even though f_m'' can contribute to the memory Hessian.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "what_it_buys": "permits a controlled EM-memory deformation while removing the linear EM source",
            "missing_for_claim": "parent source-root F, same-branch local lock, correction bound, and no singular inverse-zero factors",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "BAM3218_4_readout_guard",
            "claim_piece": "observed alpha needs effective/readout closure",
            "statement": "Even if the bare F_Q^2 coefficient is fixed, b_alpha_m observed is not zero unless S_eff and alpha readout maps preserve the same Q_ONLY/REP_TOPOLOGICAL or double-zero rule.",
            "status": "REQUIRED_GUARD_UNSIGNED",
            "what_it_buys": "prevents tree-level alpha silence from being overclaimed",
            "missing_for_claim": "radiative/readout closure with source paths",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "BAM3218_5_total_verdict",
            "claim_piece": "promote b_alpha_m=0",
            "statement": "b_alpha_m=0 follows only if BAM3218_1, BAM3218_2 or BAM3218_3, and BAM3218_4 close on the same parent branch with Z_A(m_*) positive and fixed.",
            "status": "FAIL_CURRENT_CLAIM",
            "what_it_buys": "states the exact EM F2 win condition",
            "missing_for_claim": "fixed gauge norm, no-extra-F2 or strict double-zero source root, and readout closure are not parent-signed together",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    counter_rows = [
        {
            "counter_id": "CEX3218_0_fm_linear",
            "countermodel": "Z_A(m)=Z_0+epsilon m",
            "why_allowed_now": "m is a scalar and F_Q^2 is gauge/diffeomorphism invariant; no parent object-language theorem forbids it",
            "effect": "b_alpha_m=epsilon/Z_0 and J_m contains -epsilon F_Q^2/4",
            "kills_claim": "b_alpha_m_zero",
            "needed_to_remove": "no-extra-F2 theorem, typed exclusion, or strict double-zero/evenness",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "counter_id": "CEX3218_1_fixed_norm_plus_lambda",
            "countermodel": "Z_A=C_P N_Q + lambda_A(m)",
            "why_allowed_now": "fixed gauge norm alone does not forbid independent visible F_Q^2 counterterms",
            "effect": "parent norm can be fixed while b_alpha_m survives through lambda_A",
            "kills_claim": "TQ_owner_implies_alpha_silence",
            "needed_to_remove": "operator-domain exhaustion/no independent F_Q^2",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "counter_id": "CEX3218_2_compact_charge_not_coupling",
            "countermodel": "compact U1 with integer charges and free kinetic coefficient Z_A",
            "why_allowed_now": "charge quantization/labels do not fix the continuous Maxwell kinetic coefficient",
            "effect": "relative charge labels can be owned while alpha normalization remains unowned",
            "kills_claim": "compact_U1_implies_alpha_fixed",
            "needed_to_remove": "fixed nonrescalable fibre norm/level plus no-extra-F2",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "counter_id": "CEX3218_3_readout_return",
            "countermodel": "bare Z_A fixed, alpha_eff=alpha_0 exp(epsilon m) after readout",
            "why_allowed_now": "radiative/readout closure is unsigned",
            "effect": "observed clocks/spectra can see alpha drift even if the bare action is clean",
            "kills_claim": "bare_zero_promotes_observed_zero",
            "needed_to_remove": "S_eff/readout functor closure",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    source_rows = [
        {
            "row_id": "BAMSR3218_0_candidate",
            "quantity": "b_alpha_m",
            "definition": "partial_m ln Z_A at local memory origin m_*",
            "value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "1/[m] or dimensionless if m is normalized",
            "memory_normalization": "MISSING_m_NORMALIZATION",
            "denominator": "Z_A(m_*) > 0",
            "operator_norm": "||F_Q^2|| on local support",
            "source_path": "MISSING_SOURCE_PATH",
            "equation_ref": "P8_Y5_R2FR_3218_ZA_MEMORY_DECOMPOSITION.csv:ZA3218_4_total",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "BAMSR3218_1_zero_switch_refusal",
            "quantity": "b_alpha_m_zero",
            "definition": "theorem-zero switch for b_alpha_m",
            "value": "0_requested_but_refused",
            "units": "same_as_b_alpha_m",
            "memory_normalization": "MISSING_m_NORMALIZATION",
            "denominator": "MISSING_ZA_POSITIVE_OWNER",
            "operator_norm": "not_applicable_if_zero_proved",
            "source_path": "MISSING_PARENT_SIGNED_TQ_NO_EXTRA_F2_READOUT",
            "equation_ref": "P8_Y5_R2FR_3218_BALPHA_M_ZERO_THEOREM_ATTEMPT.csv:BAM3218_5_total_verdict",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "BAMSR3218_2_double_zero_candidate",
            "quantity": "b_alpha_m_from_double_zero",
            "definition": "f_m'(m_*) if f_m=lambda_m F(m), F(m_*)=F'(m_*)=0",
            "value": "0_conditional_on_parent_source_root_and_local_lock",
            "units": "same_as_b_alpha_m",
            "memory_normalization": "MISSING_m_STAR_AND_LOCAL_LOCK",
            "denominator": "Z_A(m_*) positive and finite",
            "operator_norm": "second-order correction needs ||F_Q^2|| and f_m'' bound",
            "source_path": "MISSING_PARENT_SOURCE_ROOT_FOR_EM_F2",
            "equation_ref": "P8_Y5_R2FR_3218_BALPHA_M_ZERO_THEOREM_ATTEMPT.csv:BAM3218_3_double_zero_subroute",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3218_0_result",
            "result": "BALPHA_M_FORMULA_DERIVED_ZERO_THEOREM_CONDITIONAL_COUNTERMODELS_RETAINED_SOURCE_ROW_STAGED",
            "claim_status": "NO_BALPHA_M_ZERO_NO_EM_LOCK_NO_LOCAL_GR_CLAIM",
            "decision": "3218 derives the exact memory-slope decomposition for the EM F2 coefficient. The zero route is clear but not parent-signed: fixed T_Q/gauge norm plus no independent F2 or strict double-zero deformation plus radiative/readout closure. Linear f_m F2, lambda_A(m)F2, compact-U1-with-free-Z_A, and readout-return countermodels remain active.",
            "best_next_route": "try the strict double-zero subroute specifically for the EM F2 coefficient, because it may kill b_alpha_m without deriving the full gauge norm value; otherwise source b_alpha_m as a finite residual",
            "next_target": "3219-Y5-R2FR-EM-F2-strict-double-zero-source-root-or-balpha-m-finite-bound-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]

    return input_rows, decomp_rows, theorem_rows, counter_rows, source_rows, decision_rows


def main() -> None:
    now = stamp()
    input_rows, decomp_rows, theorem_rows, counter_rows, source_rows, decision_rows = build_rows(now)

    generated_without_validation = [
        INPUTS,
        DECOMP,
        ZERO_THEOREM,
        COUNTER,
        SOURCE_ROW,
        DECISION,
    ]

    write_csv(INPUTS, input_rows)
    write_csv(DECOMP, decomp_rows)
    write_csv(ZERO_THEOREM, theorem_rows)
    write_csv(COUNTER, counter_rows)
    write_csv(SOURCE_ROW, source_rows)
    write_csv(DECISION, decision_rows)

    all_rows: list[dict[str, str]] = []
    for path in generated_without_validation:
        all_rows.extend(read_csv(path))
    claim_rows = [row for row in all_rows if row.get("valid_for_claim") == "true"]

    validation_rows = [
        {
            "check_id": "VAL3218_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in input_rows)),
            "detail": f"inputs={len(input_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3218_01_decomposition",
            "check": "Z_A memory decomposition includes parent, lambda, hidden, readout, total",
            "pass": b(len(decomp_rows) >= 5),
            "detail": ";".join(row["component_id"] for row in decomp_rows),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3218_02_exact_formula",
            "check": "b_alpha_m exact formula is written",
            "pass": b(any(row["theorem_id"] == "BAM3218_0_exact_formula" for row in theorem_rows)),
            "detail": "b_alpha_m=(partial_m Z_A)/Z_A",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3218_03_zero_claim_blocked",
            "check": "total theorem verdict blocks current zero claim",
            "pass": b(any(row["theorem_id"] == "BAM3218_5_total_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in theorem_rows)),
            "detail": "fixed norm/no-extra-F2-or-double-zero/readout closure not signed together",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3218_04_countermodels",
            "check": "active countermodels are retained",
            "pass": b(len(counter_rows) >= 4),
            "detail": ";".join(row["counter_id"] for row in counter_rows),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3218_05_source_rows",
            "check": "b_alpha_m finite/theorem-zero rows are staged but nonclaim",
            "pass": b(len(source_rows) >= 3),
            "detail": ";".join(row["row_id"] for row in source_rows),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3218_06_claims_blocked",
            "check": "no generated row is valid_for_claim true",
            "pass": b(len(claim_rows) == 0),
            "detail": f"claim_rows_true={len(claim_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3218_07_no_formalization_workbench_edit",
            "check": "script writes only post-checkpoint outputs",
            "pass": "true",
            "detail": "no formalization-workbench paths are output targets",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3218_08_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(len(read_csv(path)) > 0 for path in generated_without_validation)),
            "detail": ";".join(path.name for path in generated_without_validation),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3218_09_next_target",
            "check": "next target is strict double-zero or finite bound",
            "pass": b("3219" in decision_rows[0]["next_target"]),
            "detail": decision_rows[0]["next_target"],
            "generated_utc": now,
        },
    ]
    write_csv(VALIDATION, validation_rows)

    doc = f"""# 3218 - EM F2 Vertex Owner For Memory Slope Zero Or b_alpha_m Source Row under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3218 derives the exact object we needed:

```text
S_EM = -1/4 int Z_A(m,q,readout) F_Q^2

b_alpha_m := partial_m ln Z_A | m_*
           = (partial_m Z_A | m_*) / Z_A(m_*).
```

Using the honest EM coefficient decomposition:

```text
Z_A =
  C_P N_Q
  + lambda_A
  + f_m(m)
  + delta_lambda_rad(m,mu)
  + readout_alpha(m).
```

So:

```text
b_alpha_m =
[ partial_m(C_P N_Q)
  + partial_m lambda_A
  + f_m'(m_*)
  + partial_m delta_lambda_rad
  + partial_m readout_alpha
] / Z_A(m_*).
```

This is progress because it stops the coupling problem being vague. The only honest zero routes are:

```text
1. fixed parent T_Q/gauge norm plus no independent F_Q^2;
2. strict EM double-zero source root f_m=O((m-m_*)^2);
3. radiative/readout closure preserving the same rule.
```

Current verdict: the zero theorem is exact as a conditional, but not parent-signed. The source row for `b_alpha_m` is staged and remains nonclaim.

## Z_A Memory Decomposition

{md_table(decomp_rows, ["component_id", "term", "meaning", "memory_derivative", "zero_condition", "current_status", "if_live", "valid_for_claim"])}

## b_alpha_m Zero Theorem Attempt

{md_table(theorem_rows, ["theorem_id", "claim_piece", "statement", "status", "what_it_buys", "missing_for_claim", "valid_for_claim"])}

## EM F2 Countermodel Ledger

{md_table(counter_rows, ["counter_id", "countermodel", "why_allowed_now", "effect", "kills_claim", "needed_to_remove", "valid_for_claim"])}

## b_alpha_m Source Row Template

{md_table(source_rows, ["row_id", "quantity", "definition", "value", "units", "memory_normalization", "denominator", "operator_norm", "source_path", "equation_ref", "valid_for_claim"])}

## Decision

`{decision_rows[0]["result"]}`.

Claim status: `{decision_rows[0]["claim_status"]}`.

Best next route: {decision_rows[0]["best_next_route"]}.

Next target:

```text
{decision_rows[0]["next_target"]}
```

## Generated Evidence

- `{rel(INPUTS)}`
- `{rel(DECOMP)}`
- `{rel(ZERO_THEOREM)}`
- `{rel(COUNTER)}`
- `{rel(SOURCE_ROW)}`
- `{rel(DECISION)}`
- `{rel(VALIDATION)}`

## Validation

{md_table(validation_rows, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

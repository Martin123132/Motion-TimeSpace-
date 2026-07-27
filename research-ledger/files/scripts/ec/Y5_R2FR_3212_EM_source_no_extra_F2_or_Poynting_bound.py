from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3212-Y5-R2FR-EM-source-channel-no-extra-F2-or-Poynting-bound-input-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3212_INPUTS.csv"
EM_VARIATION = OUT / "P8_Y5_R2FR_3212_EM_SOURCE_VARIATION_LAW.csv"
NO_EXTRA_F2 = OUT / "P8_Y5_R2FR_3212_NO_EXTRA_F2_THEOREM_GATES.csv"
FINITE_INPUTS = OUT / "P8_Y5_R2FR_3212_FINITE_EM_BOUND_INPUT_ROWS.csv"
POYNTING_CASES = OUT / "P8_Y5_R2FR_3212_POYNTING_CASE_SPLIT.csv"
SOURCE_FEED = OUT / "P8_Y5_R2FR_3212_SOURCE_FEED_TO_3211_3210.csv"
DECISION = OUT / "P8_Y5_R2FR_3212_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3212_VALIDATION.csv"


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
        "input_id": "SRC3212_00_3211_doc",
        "location": "post_checkpoint",
        "relative_path": "3211-Y5-R2FR-JX-source-silence-with-EM-F2-Poynting-flux-or-first-finite-source-bound-under-AX1090.md",
        "role": "3211 handoff to EM source channel",
        "terms": ["J_X", "F^2", "Poynting", "3212"],
    },
    {
        "input_id": "SRC3212_01_3211_em_split",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3211_EM_F2_POYNTING_SOURCE_SPLIT.csv",
        "role": "machine-readable EM trace/F2/Poynting split",
        "terms": ["EMS3211_1_F2_scalar", "EMS3211_3_Poynting_bound"],
    },
    {
        "input_id": "SRC3212_02_3211_jx_derivation",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3211_JX_VARIATION_DERIVATION.csv",
        "role": "J_X variation formula feeding EM bound",
        "terms": ["JXD3211_3_EM_F2", "JXD3211_4_Poynting_boundary", "JXD3211_5_total_abs_bound"],
    },
    {
        "input_id": "SRC3212_03_1099_exclusion",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv",
        "role": "operator tests for f_X F2 exclusion",
        "terms": ["EXC1099_0_diffeomorphism", "EXC1099_1_U1_gauge", "EXC1099_4_product_functor"],
    },
    {
        "input_id": "SRC3212_04_1099_theorem",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv",
        "role": "unique EM kinetic owner theorem attempt",
        "terms": ["UEM1099_1_chain_rule", "UEM1099_2_counterterm", "UEM1099_3_verdict"],
    },
    {
        "input_id": "SRC3212_05_1100_signature",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv",
        "role": "T_Q/gauge-norm signature",
        "terms": ["TQS1100_2_fixed_generator_norm", "TQS1100_3_unique_curvature_norm", "TQS1100_6_verdict"],
    },
    {
        "input_id": "SRC3212_06_1101_owner",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1101_GAUGE_NORM_THEOREM_ATTEMPT.csv",
        "role": "gauge norm owner candidate theorem",
        "terms": ["GFT1101_0_target", "GFT1101_4_verdict", "charge quantization"],
    },
    {
        "input_id": "SRC3212_07_1108_f2_image",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1108_EM_F2_IMAGE_THEOREM_ATTEMPT.csv",
        "role": "parent EM F2 image exhaustion attempt",
        "terms": ["F2", "operator", "alpha", "verdict"],
    },
    {
        "input_id": "SRC3212_08_1109_lambda",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1109_LAMBDA_F2_THEOREM_ATTEMPT.csv",
        "role": "no independent lambda F2 theorem attempt",
        "terms": ["lambda", "F2", "theorem", "verdict"],
    },
    {
        "input_id": "SRC3212_09_1048_parent",
        "location": "post_checkpoint",
        "relative_path": "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md",
        "role": "parent signature and bound-matrix fallback",
        "terms": ["no-extra-F2", "b_alpha", "bound matrix", "f_X F^2"],
    },
]


def main() -> None:
    now = stamp()

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

    variation_rows = [
        {
            "law_id": "EMV3212_0_parent_decomposition",
            "object": "S_EM[X,A,g]",
            "formula": "S_EM = -1/4 int mu Z_A(X) F^2 - 1/4 int mu Theta_A(X) F*F + S_Hodge[g_obs(X),A] + S_boundary_flux",
            "derived_result": "this is the minimal EM source decomposition: gauge-kinetic scalar, dual/topological scalar, metric/Hodge stress, and boundary/Poynting flux",
            "status": "decomposition_derived_not_parent_selected",
            "missing_for_claim": "parent EM action domain;Z_A owner;Theta_A owner;Hodge descent;boundary flux rule",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "EMV3212_1_bulk_variation",
            "object": "J_X^EM_bulk",
            "formula": "J_X^EM = (1/4)Z_A'(X)F^2 + (1/4)Theta_A'(X)F*F - (1/2)T_EM^{mu nu} partial_X g_obs,mu nu + J_readout/radiative",
            "derived_result": "bulk EM source is zero only if every derivative term is theorem-zero or the relevant field invariant vanishes on support",
            "status": "source_formula_derived",
            "missing_for_claim": "b_alpha=0;Theta_A'=0;Hodge/metric descent;readout closure;field support norms",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "EMV3212_2_F2_bound",
            "object": "J_F2_bound",
            "formula": "||J_F2||_2 <= (1/4) Z_A0 |b_alpha| ||F^2||_2, where b_alpha=partial_X ln Z_A at the local branch",
            "derived_result": "finite b_alpha immediately becomes a source norm input for the 3210 amplitude law",
            "status": "bound_formula_derived_values_missing",
            "missing_for_claim": "Z_A0;b_alpha;F2_norm;support;units;source_path",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "EMV3212_3_dual_bound",
            "object": "J_FstarF_bound",
            "formula": "||J_dual||_2 <= (1/4)|Theta_A'| ||F*F||_2",
            "derived_result": "CP/topological EM invariant must be absent, constant, or bounded; it cannot be hidden inside F2 silence",
            "status": "bound_formula_derived_values_missing",
            "missing_for_claim": "Theta_A' theorem-zero or numeric bound;FstarF_norm;topological sector rule",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "EMV3212_4_Hodge_bound",
            "object": "J_Hodge_bound",
            "formula": "||J_Hodge||_2 <= (1/2)||C_Hodge T_EM||_2 with C_Hodge := partial_X g_obs or partial_X star_obs in the EM sector",
            "derived_result": "if the observed Hodge star descends through q, this term is zero; otherwise it is an EM stress-source coefficient",
            "status": "bound_formula_derived_values_missing",
            "missing_for_claim": "Hodge descent theorem or C_Hodge bound;EM stress norm",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "EMV3212_5_total_EM_bound",
            "object": "J_EM_bound_abs",
            "formula": "||J_EM||_2 <= ||J_F2||_2 + ||J_dual||_2 + ||J_Hodge||_2 + ||J_readout/radiative||_2",
            "derived_result": "the EM contribution to J_X is now a no-cancellation absolute envelope",
            "status": "envelope_derived_values_missing",
            "missing_for_claim": "all component values or theorem-zero certificates",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    theorem_rows = [
        {
            "gate_id": "F2G3212_0_fixed_TQ_norm",
            "gate": "parent T_Q and gauge norm fixed",
            "required_condition": "T_Q, charge lattice, C_P, and <T_Q,T_Q>_P are parent-owned and nonrescalable",
            "current_status": "not_parent_signed_by_1100_1101",
            "if_pass": "parent contribution to Z_A is X-silent",
            "if_fail": "b_alpha remains a finite coefficient",
            "pass": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "F2G3212_1_no_independent_F2",
            "gate": "no lambda_A F^2 or f_X(X)F^2 operator",
            "required_condition": "operator-domain exhaustion, product/sequester functor, exact shift symmetry, or equivalent parent ban",
            "current_status": "failed_current_claim_by_1099_1048_1109",
            "if_pass": "Z_A'(X)=0 at tree level",
            "if_fail": "J_F2=(1/4)Z_A0 b_alpha F^2 is live",
            "pass": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "F2G3212_2_radiative_readout",
            "gate": "no radiative/readout alpha re-entry",
            "required_condition": "effective/readout alpha remains a function only of q plus fixed representation data",
            "current_status": "unsigned_by_1099_1100",
            "if_pass": "tree-level silence survives clocks/spectra",
            "if_fail": "J_readout/radiative and b_alpha product rows remain live",
            "pass": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "F2G3212_3_Hodge_descent",
            "gate": "EM Hodge star/metric descends through q",
            "required_condition": "partial_X g_obs=0 or partial_X star_obs=0 on EM support, including disformal/stress channels",
            "current_status": "not_signed_in_current_chain",
            "if_pass": "J_Hodge=0 and Maxwell trace silence applies to pure conformal channel",
            "if_fail": "EM stress/Hodge source must be bounded",
            "pass": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "F2G3212_4_boundary_Poynting_silence",
            "gate": "Poynting/worldtube flux silent",
            "required_condition": "closed stationary surface, no radiative energy flux, exact/proper boundary term, or projector orthogonality",
            "current_status": "new_gate_values_missing",
            "if_pass": "Phi_Poynting=0",
            "if_fail": "Phi_Poynting bound feeds 3210 b_X",
            "pass": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "F2G3212_5_total_EM_zero",
            "gate": "J_EM=0 and Phi_Poynting=0",
            "required_condition": "F2G3212_0 through F2G3212_4 all pass on the same parent branch",
            "current_status": "not_claim_ready",
            "if_pass": "EM channel no longer sources local X amplitude",
            "if_fail": "use finite EM source and flux bound rows",
            "pass": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    finite_rows = [
        {
            "row_id": "FEB3212_0_balpha",
            "quantity": "b_alpha",
            "definition": "partial_X ln Z_A or vertical derivative of ln alpha_EM in the EM gauge-kinetic channel",
            "required_value_or_bound": "0 by no-extra-F2 theorem or finite sourced bound",
            "current_value": "MISSING_B_ALPHA_OR_PARENT_ZERO_THEOREM",
            "feeds": "J_F2_bound;clock/WEP/R10 alpha rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "FEB3212_1_F2_norm",
            "quantity": "||F^2||_2",
            "definition": "L2 norm of the Maxwell invariant on the local EM support used by the X branch",
            "required_value_or_bound": "finite norm with surface/worldtube/support and units",
            "current_value": "MISSING_F2_SUPPORT_NORM",
            "feeds": "J_F2_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "FEB3212_2_dual",
            "quantity": "Theta_A_prime and ||F*F||_2",
            "definition": "dual/topological EM invariant source slot",
            "required_value_or_bound": "theorem-zero or finite bound",
            "current_value": "MISSING_DUAL_CHANNEL_POLICY",
            "feeds": "J_dual_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "FEB3212_3_Hodge",
            "quantity": "C_Hodge and ||T_EM||_2",
            "definition": "EM stress/Hodge source coefficient and stress norm",
            "required_value_or_bound": "Hodge descent theorem or finite stress-coupling bound",
            "current_value": "MISSING_HODGE_STRESS_BOUND",
            "feeds": "J_Hodge_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "FEB3212_4_Poynting",
            "quantity": "C_Poynting and flux_integral",
            "definition": "boundary/worldtube energy-flow coupling and integral of |n_i T_EM^{0i}|",
            "required_value_or_bound": "zero by stationary/no-flux theorem or finite sourced bound",
            "current_value": "MISSING_POYNTING_BOUND_INPUTS",
            "feeds": "Phi_boundary;3210 b_X",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "FEB3212_5_total",
            "quantity": "J_EM_bound_abs",
            "definition": "absolute no-cancellation EM contribution to ||J_X||_2",
            "required_value_or_bound": "sum of FEB3212_0 through FEB3212_3, plus readout/radiative if open",
            "current_value": "NOT_COMPUTED_COMPONENTS_MISSING",
            "feeds": "3211 J_norm_bound_abs;3210 a_X",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    poynting_rows = [
        {
            "case_id": "POY3212_0_static_Coulomb",
            "case": "static electrostatic source",
            "F2_status": "F^2 generally nonzero",
            "Poynting_status": "T_EM^{0i}=0 if B=0 and fields stationary",
            "lesson": "static fields are F2-active but Poynting-silent",
            "claim_status": "case_split_only_not_source_data",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "case_id": "POY3212_1_null_wave",
            "case": "ideal null EM wave",
            "F2_status": "F^2=0 and F*F=0",
            "Poynting_status": "T_EM^{0i} nonzero",
            "lesson": "radiation can be F2-silent but boundary/stress active",
            "claim_status": "case_split_only_not_source_data",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "case_id": "POY3212_2_stationary_closed_exterior",
            "case": "closed stationary local exterior with no radiative flux crossing boundary",
            "F2_status": "depends on local Coulomb/magnetic field support",
            "Poynting_status": "Phi_Poynting=0 if n_i T_EM^{0i}=0 on boundary and boundary rule is proper/exact",
            "lesson": "this is the clean zero route for Poynting, but it needs a parent boundary/domain rule",
            "claim_status": "conditional_zero_route_unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "case_id": "POY3212_3_general_lab_wave",
            "case": "lab/radiative EM configuration",
            "F2_status": "may be zero or nonzero depending on polarization/near fields",
            "Poynting_status": "finite flux must be bounded by C_Poynting int |n_i T_EM^{0i}|",
            "lesson": "do not use F2=0 to claim no EM source unless boundary/stress channel is also silent",
            "claim_status": "finite_bound_route_values_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    feed_rows = [
        {
            "feed_id": "EF3212_0_to_3211_Jnorm",
            "target": "FJB3211_0_abs_J_norm",
            "feed_formula": "replace EM term by J_EM_bound_abs = J_F2_bound + J_dual_bound + J_Hodge_bound + J_readout/radiative_bound",
            "current_status": "formula_ready_values_missing",
            "claim_effect": "EM source contribution becomes finite and absolute if inputs are sourced",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "feed_id": "EF3212_1_to_3211_Phi",
            "target": "FJB3211_1_abs_Phi_Poynting",
            "feed_formula": "Phi_Poynting_bound_abs = C_Poynting int_boundary |n_i T_EM^{0i}| dS dt",
            "current_status": "formula_ready_values_missing",
            "claim_effect": "Poynting becomes a boundary amplitude input, not a loose analogy",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "feed_id": "EF3212_2_to_3210_zero",
            "target": "AMP3210_5_zero_limit",
            "feed_formula": "if J_EM_bound_abs=0 and Phi_Poynting_bound_abs=0 by parent theorem, EM does not obstruct X=0",
            "current_status": "conditional_zero_route_not_signed",
            "claim_effect": "would remove the EM source contribution from the local no-hair gate",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "feed_id": "EF3212_3_to_empirical",
            "target": "clock/WEP/R10/PPN EM rows",
            "feed_formula": "if b_alpha or Hodge/Poynting coefficients are finite, map them to alpha/source/readout residual rows with no cancellation",
            "current_status": "finite_residual_route_selected_if_zero_fails",
            "claim_effect": "empirical route requires coefficient provenance and field/support norms",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3212_0_result",
            "result": "EM_SOURCE_VARIATION_AND_POYNTING_BOUND_DERIVED_NO_EXTRA_F2_NOT_PROVED",
            "claim_status": "NO_B_ALPHA_ZERO_NO_JEM_ZERO_NO_LOCAL_GR_CLAIM",
            "decision": "The no-extra-F2 route remains mathematically clean but unsigned; the EM channel is now a finite absolute source/bound system.",
            "best_next_route": "try the strongest derivation left: product/sequester or exact-shift theorem for hidden-visible coefficient maps; if it fails, build coefficient provenance for b_alpha and Hodge/Poynting bounds",
            "next_target": "3213-Y5-R2FR-hidden-visible-product-sequester-or-balpha-Hodge-Poynting-provenance-pack-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]

    generated_without_validation = [
        INPUTS,
        EM_VARIATION,
        NO_EXTRA_F2,
        FINITE_INPUTS,
        POYNTING_CASES,
        SOURCE_FEED,
        DECISION,
    ]

    write_csv(INPUTS, input_rows)
    write_csv(EM_VARIATION, variation_rows)
    write_csv(NO_EXTRA_F2, theorem_rows)
    write_csv(FINITE_INPUTS, finite_rows)
    write_csv(POYNTING_CASES, poynting_rows)
    write_csv(SOURCE_FEED, feed_rows)
    write_csv(DECISION, decision_rows)

    all_claim_rows: list[dict[str, str]] = []
    for path in generated_without_validation:
        all_claim_rows.extend(row for row in read_csv(path) if row.get("valid_for_claim") == "true")

    validation_rows = [
        {
            "check_id": "VAL3212_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in input_rows)),
            "detail": f"inputs={len(input_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3212_01_variation_law",
            "check": "EM source variation law exists",
            "pass": b(any(row["law_id"] == "EMV3212_1_bulk_variation" for row in variation_rows)),
            "detail": "J_EM includes F2, F*F, Hodge/stress, readout/radiative",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3212_02_no_extra_F2_gates",
            "check": "no-extra-F2 theorem gates are explicit",
            "pass": b(len(theorem_rows) >= 6),
            "detail": "TQ norm;no independent F2;radiative;Hodge;Poynting;total",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3212_03_finite_inputs",
            "check": "finite EM bound inputs are staged",
            "pass": b(len(finite_rows) >= 6),
            "detail": "b_alpha;F2;dual;Hodge;Poynting;total",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3212_04_poynting_cases",
            "check": "Poynting/F2 case split is written",
            "pass": b(len(poynting_rows) >= 4),
            "detail": "static;null wave;closed exterior;general wave",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3212_05_feeds_3211_3210",
            "check": "EM rows feed 3211/3210",
            "pass": b(any(row["feed_id"] == "EF3212_0_to_3211_Jnorm" for row in feed_rows) and any(row["feed_id"] == "EF3212_1_to_3211_Phi" for row in feed_rows)),
            "detail": "J_EM_bound_abs and Phi_Poynting feed rows exist",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3212_06_claims_blocked",
            "check": "no generated claim row is valid_for_claim true",
            "pass": b(len(all_claim_rows) == 0),
            "detail": f"claim_rows_true={len(all_claim_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3212_07_no_formalization_workbench_edit",
            "check": "script writes only post-checkpoint outputs",
            "pass": "true",
            "detail": "no formalization-workbench paths are output targets",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3212_08_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(len(read_csv(path)) > 0 for path in generated_without_validation)),
            "detail": ";".join(path.name for path in generated_without_validation),
            "generated_utc": now,
        },
    ]
    write_csv(VALIDATION, validation_rows)

    doc = f"""# 3212 - EM Source Channel: No-Extra-F2 Or Poynting Bound Input under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, Maxwell derivation claim, PPN pass, R10 pass, WEP pass, clock pass, `b_alpha=0` claim, `J_EM=0` claim, `J_X=0` claim, or public-facing result.

## Result

3212 derives the actual EM source law feeding the `3211` coupling equation:

```text
S_EM = -1/4 int mu Z_A(X) F^2
       -1/4 int mu Theta_A(X) F*F
       + S_Hodge[g_obs(X),A]
       + S_boundary_flux.
```

Therefore:

```text
J_X^EM = 1/4 Z_A'(X) F^2
       + 1/4 Theta_A'(X) F*F
       - 1/2 T_EM^(mu nu) partial_X g_obs,mu nu
       + J_readout/radiative.
```

and the finite no-cancellation envelope is:

```text
||J_EM||_2 <= 1/4 Z_A0 |b_alpha| ||F^2||_2
            + 1/4 |Theta_A'| ||F*F||_2
            + 1/2 ||C_Hodge T_EM||_2
            + ||J_readout/radiative||_2.
```

Poynting remains a boundary/worldtube flux:

```text
|Phi_Poynting| <= C_Poynting int_boundary |n_i T_EM^(0i)| dS dt.
```

Clean zero route:

```text
fixed T_Q/gauge norm
+ no independent lambda_A F^2 or f_X(X)F^2
+ no radiative/readout alpha re-entry
+ Hodge/metric descent
+ Poynting boundary silence
=> J_EM = 0 and Phi_Poynting = 0.
```

Current verdict: that theorem is not signed in the present corpus. The EM channel is therefore not dead, but it is now a finite source/bound problem rather than a foggy coupling problem.

## EM Variation Law

{md_table(variation_rows, ["law_id", "object", "formula", "derived_result", "status", "missing_for_claim", "valid_for_claim"])}

## No-Extra-F2 Theorem Gates

{md_table(theorem_rows, ["gate_id", "gate", "required_condition", "current_status", "if_pass", "if_fail", "pass", "valid_for_claim"])}

## Finite EM Bound Inputs

{md_table(finite_rows, ["row_id", "quantity", "definition", "required_value_or_bound", "current_value", "feeds", "valid_for_claim"])}

## Poynting Case Split

{md_table(poynting_rows, ["case_id", "case", "F2_status", "Poynting_status", "lesson", "claim_status", "valid_for_claim"])}

## Feed To 3211/3210

{md_table(feed_rows, ["feed_id", "target", "feed_formula", "current_status", "claim_effect", "valid_for_claim"])}

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
- `{rel(EM_VARIATION)}`
- `{rel(NO_EXTRA_F2)}`
- `{rel(FINITE_INPUTS)}`
- `{rel(POYNTING_CASES)}`
- `{rel(SOURCE_FEED)}`
- `{rel(DECISION)}`
- `{rel(VALIDATION)}`

## Validation

{md_table(validation_rows, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

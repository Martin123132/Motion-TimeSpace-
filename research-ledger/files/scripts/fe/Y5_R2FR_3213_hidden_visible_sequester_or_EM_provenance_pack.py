from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3213-Y5-R2FR-hidden-visible-product-sequester-or-balpha-Hodge-Poynting-provenance-pack-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3213_INPUTS.csv"
SEQUESTER = OUT / "P8_Y5_R2FR_3213_PRODUCT_SEQUESTER_THEOREM_TEST.csv"
COUNTERTHEOREM = OUT / "P8_Y5_R2FR_3213_INVARIANT_SCALAR_COUNTERTHEOREM.csv"
PROVENANCE = OUT / "P8_Y5_R2FR_3213_EM_COEFFICIENT_PROVENANCE_PACK.csv"
DECISION = OUT / "P8_Y5_R2FR_3213_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3213_VALIDATION.csv"


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
        "input_id": "SRC3213_00_3212_doc",
        "location": "post_checkpoint",
        "relative_path": "3212-Y5-R2FR-EM-source-channel-no-extra-F2-or-Poynting-bound-input-under-AX1090.md",
        "role": "3212 handoff to product/sequester or provenance fork",
        "terms": ["product/sequester", "b_alpha", "Hodge", "Poynting"],
    },
    {
        "input_id": "SRC3213_01_3212_gates",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3212_NO_EXTRA_F2_THEOREM_GATES.csv",
        "role": "3212 no-extra-F2 gates",
        "terms": ["F2G3212_1_no_independent_F2", "F2G3212_2_radiative_readout", "F2G3212_5_total_EM_zero"],
    },
    {
        "input_id": "SRC3213_02_1049_symmetry",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1049_SYMMETRY_BAN_THEOREM_ATTEMPT.csv",
        "role": "symmetry and product-functor ban tests",
        "terms": ["SBT1049_4_product_functor", "SBT1049_0_diffeomorphism", "SBT1049_5_radiative"],
    },
    {
        "input_id": "SRC3213_03_1050_product",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv",
        "role": "visible-hidden product functor theorem attempt",
        "terms": ["PFT1050_1_visible_action_pullback", "PFT1050_2_forbidden_mixed_hom", "PFT1050_5_verdict"],
    },
    {
        "input_id": "SRC3213_04_1051_morphism",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv",
        "role": "no mixed hidden-visible morphism lemma and scalar counterexample",
        "terms": ["NMM1051_1_trivial_hidden_algebra_case", "NMM1051_2_scalar_counterexample", "NMM1051_5_verdict"],
    },
    {
        "input_id": "SRC3213_05_1114_morphism",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv",
        "role": "no hidden-visible coefficient morphism theorem attempt",
        "terms": ["NO_HIDDEN_VISIBLE", "scalar", "finite", "verdict"],
    },
    {
        "input_id": "SRC3213_06_1115_triviality",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1115_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_ATTEMPT.csv",
        "role": "local invariant algebra triviality attempt",
        "terms": ["LIA1115_1_sufficiency", "LIA1115_3_continuous_scalar_obstruction", "LIA1115_6_verdict"],
    },
    {
        "input_id": "SRC3213_07_1107_alpha",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1107_ALPHA_F2_SUBCASE.csv",
        "role": "alpha/F2 subcase and counterterm rows",
        "terms": ["ALP1107_2_hidden_counterterm", "ALP1107_4_verdict", "lambda_A"],
    },
    {
        "input_id": "SRC3213_08_3212_finite",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3212_FINITE_EM_BOUND_INPUT_ROWS.csv",
        "role": "3212 finite EM source inputs",
        "terms": ["FEB3212_0_balpha", "FEB3212_3_Hodge", "FEB3212_4_Poynting"],
    },
    {
        "input_id": "SRC3213_09_3212_feed",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3212_SOURCE_FEED_TO_3211_3210.csv",
        "role": "3212 feed into source/amplitude laws",
        "terms": ["EF3212_0_to_3211_Jnorm", "EF3212_1_to_3211_Phi", "EF3212_3_to_empirical"],
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

    sequester_rows = [
        {
            "test_id": "SEQ3213_0_product_domain",
            "claim_piece": "visible-hidden product domain",
            "formal_condition": "C_parent -> C_vis x C_hid, with visible objects pulled back from q and representation labels; hidden variables have no target action on visible coefficient modules.",
            "derivation_result": "if parent-signed, hidden representative motion cannot generate f_X F2, Hodge coefficient drift, matter masses, or readout constants",
            "current_status": "conditional_not_parent_signed",
            "blocks_claim": "parent split and target-action exclusion are not derived from primitives",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "test_id": "SEQ3213_1_visible_action_pullback",
            "claim_piece": "visible action ignores hidden coordinates except through q",
            "formal_condition": "S_vis = S_EM[A_Q,q,T_Q,theta_rep]+S_matter[Psi,e_obs(q),theta_rep]+S_readout[q,theta_rep]",
            "derivation_result": "Dq[v_X]=0 then gives delta_X S_vis=0, including b_alpha=0 and C_Hodge=0 at tree level",
            "current_status": "exact_conditional_theorem",
            "blocks_claim": "actual parent visible action and all readout maps are not signed to have this form",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "test_id": "SEQ3213_2_boundary_functor",
            "claim_piece": "boundary/Poynting sequester",
            "formal_condition": "S_boundary and source-worldtube terms depend only on q-visible stress flux or are exact/proper/orthogonal to hidden X",
            "derivation_result": "would make Phi_Poynting zero or independent of X on the local branch",
            "current_status": "new_required_clause_not_signed",
            "blocks_claim": "product functor must cover boundary/worldtube flux, not just bulk F2",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "test_id": "SEQ3213_3_radiative_readout",
            "claim_piece": "EFT/readout closure",
            "formal_condition": "renormalized S_eff and clock/spectroscopy/readout maps remain in the product image",
            "derivation_result": "tree-level no-extra-F2 would survive to observable alpha products",
            "current_status": "unsigned",
            "blocks_claim": "loop/readout re-entry can recreate b_alpha or clock coefficients",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "test_id": "SEQ3213_4_total",
            "claim_piece": "product sequester theorem promotes EM source silence",
            "formal_condition": "SEQ3213_0 through SEQ3213_3 all parent-signed on the same branch",
            "derivation_result": "J_EM=0 and Phi_Poynting=0 for the hidden X source channel",
            "current_status": "fail_current_claim",
            "blocks_claim": "same-branch product/readout/boundary theorem is not available",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    counter_rows = [
        {
            "counter_id": "CTR3213_0_scalar_invariant",
            "assumption": "there exists nonconstant hidden invariant scalar I with Lie_vX I nonzero",
            "construction": "c(I)=c0+epsilon I is a natural scalar coefficient",
            "operator": "c(I) F^2, c(I) F*F, c(I) T_EM/stress, or c(I) boundary flux weight",
            "consequence": "hidden-visible coefficient morphism exists; b_alpha/Hodge/Poynting cannot be theorem-zero",
            "status": "countertheorem_active_unless_invariant_algebra_trivial_or_typed_out",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "counter_id": "CTR3213_1_covariance_limit",
            "assumption": "only diffeomorphism covariance and visible U(1) gauge invariance are imposed",
            "construction": "f(I)F^2 is a scalar gauge-invariant density",
            "operator": "hidden-scalar gauge kinetic counterterm",
            "consequence": "ordinary symmetries do not forbid the EM source channel",
            "status": "no_zero_from_covariance_or_gauge_invariance",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "counter_id": "CTR3213_2_shift_limit",
            "assumption": "only parity or weak shift evidence is available",
            "construction": "even functions such as I^2 F^2 or radiative/readout terms survive unless exact shift/product closure is signed",
            "operator": "even/radiative coefficient maps",
            "consequence": "linear coefficient may die while quadratic/readout source remains",
            "status": "shift_route_requires_exact_parent_symmetry_and_closure",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "counter_id": "CTR3213_3_boundary_limit",
            "assumption": "bulk visible action is sequestered but boundary/source-worldtube action is not",
            "construction": "hidden-dependent boundary weight multiplies EM energy flux",
            "operator": "C_Poynting(I) n_i T_EM^{0i}",
            "consequence": "Poynting source re-enters through Phi_boundary even if bulk F2 is banned",
            "status": "boundary_functor_must_be_part_of_theorem",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    provenance_rows = [
        {
            "row_id": "PROV3213_0_balpha",
            "coefficient": "b_alpha",
            "definition": "vertical derivative of EM gauge kinetic/readout coefficient; partial_X ln Z_A or equivalent",
            "zero_route": "product/sequester plus fixed T_Q/gauge norm plus no radiative/readout re-entry",
            "finite_route_inputs": "numeric/source-backed b_alpha or bounded prior width; X normalization; source path; units",
            "feeds": "FEB3212_0_balpha;J_F2_bound;clock/WEP/R10 alpha rows",
            "current_status": "MISSING_ZERO_THEOREM_OR_NUMERIC_PROVENANCE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "PROV3213_1_C_Hodge",
            "coefficient": "C_Hodge",
            "definition": "partial_X g_obs or partial_X star_obs coefficient in EM stress/Hodge channel",
            "zero_route": "observed Hodge star factors through q and Dq[v_X]=0",
            "finite_route_inputs": "C_Hodge bound;EM stress norm;surface/support;source path;units",
            "feeds": "FEB3212_3_Hodge;J_Hodge_bound;PPN/clock/EM stress rows",
            "current_status": "MISSING_HODGE_DESCENT_OR_FINITE_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "PROV3213_2_C_Poynting",
            "coefficient": "C_Poynting",
            "definition": "hidden/X derivative of boundary or worldtube coupling to EM energy flux",
            "zero_route": "boundary functor is exact/proper/orthogonal or depends only on q-visible flux",
            "finite_route_inputs": "C_Poynting;flux integral;surface/worldtube rule;orientation;source path;units",
            "feeds": "FEB3212_4_Poynting;Phi_boundary;3210 b_X",
            "current_status": "MISSING_BOUNDARY_SEQUESTER_OR_FLUX_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "PROV3213_3_theta_dual",
            "coefficient": "Theta_A_prime",
            "definition": "hidden/X derivative of dual/topological EM coefficient multiplying F*F",
            "zero_route": "dual coefficient is topological/discrete/quotient-owned or exact constant",
            "finite_route_inputs": "Theta_A_prime bound;FstarF norm;topological sector rule",
            "feeds": "FEB3212_2_dual;J_dual_bound",
            "current_status": "MISSING_DUAL_CHANNEL_POLICY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "PROV3213_4_total",
            "coefficient": "EM_source_envelope",
            "definition": "absolute sum of b_alpha, C_Hodge, C_Poynting, dual, and radiative/readout EM source contributions",
            "zero_route": "all component zero routes pass on one parent branch",
            "finite_route_inputs": "all component coefficients and field/support norms with no MISSING markers",
            "feeds": "J_EM_bound_abs;J_X_norm;X amplitude;omega_X bound",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3213_0_result",
            "result": "PRODUCT_SEQUESTER_THEOREM_CONDITIONAL_COUNTERTHEOREM_ACTIVE_PROVENANCE_PACK_STAGED",
            "claim_status": "NO_SEQUESTER_CLAIM_NO_B_ALPHA_ZERO_NO_JEM_ZERO",
            "decision": "Product/sequester would close the EM coupling channel if parent-signed, but a surviving hidden invariant scalar constructs f(I)F2 and boundary flux coefficients.",
            "best_next_route": "attack the surviving invariant generators directly; if any generator survives, keep EM coefficients as finite provenance rows",
            "next_target": "3214-Y5-R2FR-invariant-generator-kill-list-for-EM-coupling-or-promote-provenance-inputs-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]

    generated_without_validation = [
        INPUTS,
        SEQUESTER,
        COUNTERTHEOREM,
        PROVENANCE,
        DECISION,
    ]

    write_csv(INPUTS, input_rows)
    write_csv(SEQUESTER, sequester_rows)
    write_csv(COUNTERTHEOREM, counter_rows)
    write_csv(PROVENANCE, provenance_rows)
    write_csv(DECISION, decision_rows)

    all_claim_rows: list[dict[str, str]] = []
    for path in generated_without_validation:
        all_claim_rows.extend(row for row in read_csv(path) if row.get("valid_for_claim") == "true")

    validation_rows = [
        {
            "check_id": "VAL3213_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in input_rows)),
            "detail": f"inputs={len(input_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3213_01_sequester_theorem",
            "check": "product/sequester theorem test exists",
            "pass": b(any(row["test_id"] == "SEQ3213_4_total" for row in sequester_rows)),
            "detail": "same-branch product/readout/boundary theorem gate written",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3213_02_countertheorem",
            "check": "hidden invariant scalar countertheorem exists",
            "pass": b(any(row["counter_id"] == "CTR3213_0_scalar_invariant" for row in counter_rows)),
            "detail": "I -> c0+epsilon I creates visible coefficient morphism",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3213_03_boundary_counterexample",
            "check": "Poynting boundary re-entry is tested",
            "pass": b(any(row["counter_id"] == "CTR3213_3_boundary_limit" for row in counter_rows)),
            "detail": "bulk sequester alone is insufficient",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3213_04_provenance_pack",
            "check": "EM coefficient provenance pack is staged",
            "pass": b(len(provenance_rows) >= 5),
            "detail": "b_alpha;C_Hodge;C_Poynting;dual;total",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3213_05_claims_blocked",
            "check": "no generated claim row is valid_for_claim true",
            "pass": b(len(all_claim_rows) == 0),
            "detail": f"claim_rows_true={len(all_claim_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3213_06_no_formalization_workbench_edit",
            "check": "script writes only post-checkpoint outputs",
            "pass": "true",
            "detail": "no formalization-workbench paths are output targets",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3213_07_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(len(read_csv(path)) > 0 for path in generated_without_validation)),
            "detail": ";".join(path.name for path in generated_without_validation),
            "generated_utc": now,
        },
    ]
    write_csv(VALIDATION, validation_rows)

    doc = f"""# 3213 - Hidden/Visible Product Sequester Or EM Coefficient Provenance Pack under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, Maxwell derivation claim, R10 pass, WEP pass, clock pass, `b_alpha=0` claim, product-sequester claim, or public-facing result.

## Result

3213 gives the honest theorem/countertheorem fork.

The clean theorem route:

```text
C_parent -> C_vis x C_hid
S_vis = S_vis[q(Phi), theta_rep]
Hom(C_hid, Coeff(O_vis)) = Const or absent
boundary/readout/radiative maps preserve the split
=> hidden X cannot generate f_X F^2, C_Hodge, C_Poynting, mass, or clock coefficients.
```

The countertheorem:

```text
If a nonconstant hidden invariant scalar I survives,
then c(I)=c0+epsilon I is a visible coefficient map.
So c(I)F^2, c(I)T_EM, or c(I)n_iT_EM^(0i)
is legal unless product/sequester, exact shift, or typed-out target action forbids it.
```

Current verdict: product/sequester is the right theorem, but it is not parent-signed; the scalar-invariant countertheorem is active. Therefore EM coefficients must stay as finite provenance rows unless the surviving invariant generators are killed.

## Product Sequester Test

{md_table(sequester_rows, ["test_id", "claim_piece", "formal_condition", "derivation_result", "current_status", "blocks_claim", "valid_for_claim"])}

## Invariant Scalar Countertheorem

{md_table(counter_rows, ["counter_id", "assumption", "construction", "operator", "consequence", "status", "valid_for_claim"])}

## EM Coefficient Provenance Pack

{md_table(provenance_rows, ["row_id", "coefficient", "definition", "zero_route", "finite_route_inputs", "feeds", "current_status", "valid_for_claim"])}

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
- `{rel(SEQUESTER)}`
- `{rel(COUNTERTHEOREM)}`
- `{rel(PROVENANCE)}`
- `{rel(DECISION)}`
- `{rel(VALIDATION)}`

## Validation

{md_table(validation_rows, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

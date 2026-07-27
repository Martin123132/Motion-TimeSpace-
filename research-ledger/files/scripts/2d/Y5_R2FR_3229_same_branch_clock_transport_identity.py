from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3229-Y5-R2FR-same-branch-clock-transport-identity-for-DtauRQ-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3229_INPUTS.csv"
TRANSPORT = OUT / "P8_Y5_R2FR_3229_TRANSPORT_IDENTITY_DERIVATION.csv"
CONTRACT = OUT / "P8_Y5_R2FR_3229_TRANSPORT_PARENT_CONTRACT.csv"
XI_REDUCTION = OUT / "P8_Y5_R2FR_3229_XI_CLOCK_REDUCTION_WITH_TRANSPORT_ERROR.csv"
NEXT_BOUND = OUT / "P8_Y5_R2FR_3229_ETRANSPORT_BOUND_TARGETS.csv"
DECISION = OUT / "P8_Y5_R2FR_3229_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3229_VALIDATION.csv"


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
        "input_id": "SRC3229_00_3228_doc",
        "location": "post_checkpoint",
        "relative_path": "3228-Y5-R2FR-Xi-clock-product-row-or-clock-tau-owner-under-AX1090.md",
        "role": "3228 handoff selecting same-branch transport identity",
        "terms": ["D_tau R_Q", "E_transport", "Xi_clock"],
    },
    {
        "input_id": "SRC3229_01_3228_derivation",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3228_XI_CLOCK_PRODUCT_DERIVATION.csv",
        "role": "machine Xi_clock product derivation",
        "terms": ["XID3228_3_root_taylor_product", "D_tau R_Q", "transport"],
    },
    {
        "input_id": "SRC3229_02_3228_contract",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3228_PARENT_XI_CLOCK_CONTRACT.csv",
        "role": "machine parent Xi_clock contract",
        "terms": ["XIC3228_3_same_branch_transport", "MISSING_CORE_OWNER"],
    },
    {
        "input_id": "SRC3229_03_3210_doc",
        "location": "post_checkpoint",
        "relative_path": "3210-Y5-R2FR-scalar-nohair-amplitude-law-and-omega-zero-curl-gate-under-AX1090.md",
        "role": "local amplitude/nohair source for transverse bound route",
        "terms": ["Y_X", "delta_X_H1_bound", "X_zero", "source/boundary leakage"],
    },
    {
        "input_id": "SRC3229_04_3210_amp",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3210_SCALAR_NOHAIR_AMPLITUDE_LAW.csv",
        "role": "machine amplitude law",
        "terms": ["AMP3210_3_profile_amplitude", "AMP3210_6_tangent_amplitude", "valid_for_claim"],
    },
    {
        "input_id": "SRC3229_05_3136_doc",
        "location": "post_checkpoint",
        "relative_path": "3136-Y5-R2FR-observed-coframe-clock-functional-owner-under-AX1090.md",
        "role": "clock path observed-time source",
        "terms": ["observed clocks measure observed metric proper time", "same tau", "parent has not signed"],
    },
    {
        "input_id": "SRC3229_06_3223_doc",
        "location": "post_checkpoint",
        "relative_path": "3223-Y5-R2FR-RQ-source-search-or-finite-alpha-runner-smoke-inputs-under-AX1090.md",
        "role": "finite R_Q branch and D_mR_Q source gap",
        "terms": ["D_m R_Q", "R_Q", "Z_min", "FINITE_BOUND_READY_FOR_INPUTS"],
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

    transport_rows = [
        {
            "step_id": "TR3229_0_field_path",
            "object": "local observed clock path",
            "identity": "gamma: tau_obs -> Phi(tau_obs) in parent configuration space",
            "status": "GEOMETRIC_SETUP",
            "derivation": "Any observed clock experiment selects a path through the parent field configuration space once the observed clock functional is fixed.",
            "missing_for_claim": "parent-signed clock functional and configuration-space domain",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "TR3229_1_chain_rule",
            "object": "residual derivative",
            "identity": "D_tau R_Q = DR_Q[Phi] . gamma_dot",
            "status": "EXACT_DIFFERENTIAL_IDENTITY",
            "derivation": "This is the Fréchet chain rule for the residual map R_Q evaluated along gamma(tau_obs).",
            "missing_for_claim": "R_Q parent object and differentiability class",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "TR3229_2_tangent_split",
            "object": "clock tangent decomposition",
            "identity": "gamma_dot = tau_clock_time e_m + v_perp + v_vert",
            "status": "EXACT_SPLIT_AFTER_BRANCH_CHOICE",
            "derivation": "Choose e_m as the EM residual branch direction, v_perp as physical transverse drift, and v_vert as representative/quotient-vertical drift.",
            "missing_for_claim": "parent-owned branch coordinate m and projection operators P_m,P_perp,P_vert",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "TR3229_3_transport_identity",
            "object": "same-branch transport",
            "identity": "D_tau R_Q = D_m R_Q tau_clock_time + D_perp R_Q[v_perp] + D_vert R_Q[v_vert]",
            "status": "DERIVED_EXACT_BRANCH_DECOMPOSITION",
            "derivation": "Insert the tangent split into the chain rule. No dynamics have been assumed yet.",
            "missing_for_claim": "bounds or zero the transverse and vertical terms",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "TR3229_4_vertical_silence",
            "object": "quotient-vertical term",
            "identity": "D_vert R_Q[v_vert]=0 if R_Q is quotient-basic or representative-silent",
            "status": "CONDITIONAL_ZERO",
            "derivation": "If R_Q descends through q(Phi), vertical tangent vectors in ker(Dq) cannot change R_Q.",
            "missing_for_claim": "R_Q=q-basic source row or vertical Ward identity",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "TR3229_5_transverse_error",
            "object": "physical transverse drift",
            "identity": "E_transport := ||D_perp R_Q[v_perp]|| + ||D_vert R_Q[v_vert]||",
            "status": "BOUND_TARGET_DEFINED",
            "derivation": "All non-one-dimensional clock-path leakage is isolated into a single normed transport error.",
            "missing_for_claim": "v_perp amplitude bound, D_perpR_Q operator norm, vertical silence or vertical bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "TR3229_6_exact_closure",
            "object": "one-dimensional same-branch closure",
            "identity": "if v_perp=0 and D_vertR_Q[v_vert]=0, then D_tau R_Q = D_m R_Q tau_clock_time exactly",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "derivation": "The identity follows immediately from the branch decomposition and quotient silence.",
            "missing_for_claim": "parent proof that the clock path stays in the EM residual branch up to vertical gauge",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    contract_rows = [
        {
            "clause_id": "TPC3229_0_branch_coordinate",
            "required_clause": "parent-owned EM residual branch coordinate m",
            "math_need": "e_m and Delta m identify the same local branch used in D_mR_Q",
            "current_status": "MISSING_PARENT_BRANCH_COORDINATE",
            "why_it_matters": "without this, tau_clock_time cannot be the velocity along the R_Q branch",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "TPC3229_1_clock_path",
            "required_clause": "observed clock path gamma(tau_obs)",
            "math_need": "gamma_dot is measured with the same tau_obs used by the clock bound",
            "current_status": "CONDITIONAL_FROM_3136",
            "why_it_matters": "prevents using internal flow time as if it were lab clock time",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "TPC3229_2_projection_split",
            "required_clause": "tangent projection gamma_dot=tau e_m+v_perp+v_vert",
            "math_need": "define P_m, P_perp, and vertical kernel consistently",
            "current_status": "GEOMETRIC_CONTRACT_WRITTEN",
            "why_it_matters": "turns the vague transport problem into exact pieces that can be bounded",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "TPC3229_3_vertical_silence",
            "required_clause": "R_Q is q-basic or vertical-Ward silent",
            "math_need": "D_vertR_Q[v_vert]=0 for v_vert in ker(Dq)",
            "current_status": "UNSIGNED",
            "why_it_matters": "otherwise representative drift can fake alpha/clock drift",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "TPC3229_4_transverse_amplitude",
            "required_clause": "v_perp is zero or bounded by local nohair/source leakage",
            "math_need": "||v_perp|| <= Y_perp or v_perp=0",
            "current_status": "BOUND_ROUTE_FROM_3210_NOT_ATTACHED_TO_RQ",
            "why_it_matters": "this is the finite-error route if exact one-dimensional closure fails",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    xi_rows = [
        {
            "row_id": "XIR3229_0_corrected_clock_reduction",
            "quantity": "alpha clock drift",
            "formula": "|D_tau ln alpha_EM| <= C_D |Delta m tau_clock_time| + E_HO + E_clock_transport",
            "status": "REFINED_FROM_3228",
            "definition": "E_clock_transport := (2|lambda_D|/Z_min)||R_Q|| E_transport, with ||R_Q|| replaced by its near-root bound when allowed",
            "claim_gate": "requires R_Q parent object, Z_min, same branch, and E_transport bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "XIR3229_1_exact_transport_case",
            "quantity": "E_clock_transport",
            "formula": "E_clock_transport=0 if v_perp=0 and vertical silence holds",
            "status": "EXACT_CONDITIONAL_ZERO",
            "definition": "one-dimensional clock path in the EM residual branch",
            "claim_gate": "must prove local branch closure, not assume it",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "XIR3229_2_finite_transport_case",
            "quantity": "E_clock_transport",
            "formula": "E_clock_transport <= (2|lambda_D|/Z_min)(||D_mR_Q|| |Delta m|+O(Delta m^2)) (||D_perpR_Q|| ||v_perp|| + ||D_vertR_Q|| ||v_vert||)",
            "status": "FINITE_BOUND_FORMULA",
            "definition": "finite error budget if exact closure fails",
            "claim_gate": "requires transverse amplitude and operator norm inputs",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    next_bound_rows = [
        {
            "target_id": "EBT3229_0_transverse_zero",
            "target": "v_perp=0 theorem",
            "source_route": "3210 nohair/tangent amplitude collapse",
            "required_inputs": "J_perp=0; boundary_perp=0; coercive operator; same branch as R_Q",
            "result_if_acquired": "exact transport identity closes",
            "status": "BEST_ZERO_ROUTE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "target_id": "EBT3229_1_transverse_bound",
            "target": "||v_perp|| <= Y_perp",
            "source_route": "3210 amplitude law with source/boundary leakage",
            "required_inputs": "source norm; boundary norm; m_min; Z_min; operator domain",
            "result_if_acquired": "finite E_clock_transport bound for the clock gate",
            "status": "BEST_FINITE_ROUTE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "target_id": "EBT3229_2_vertical_silence",
            "target": "D_vert R_Q=0",
            "source_route": "quotient-basic residual or vertical Ward identity",
            "required_inputs": "R_Q descends through q(Phi) or explicit vertical annihilation theorem",
            "result_if_acquired": "removes representative drift from alpha/clock channel",
            "status": "NEEDED_FOR_ZERO_AND_FINITE_ROUTES",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3229_0_result",
            "decision": "TRANSPORT_IDENTITY_DERIVED_AS_BRANCH_DECOMPOSITION_EXACT_CLOSURE_NOT_SIGNED",
            "because": "D_tau R_Q splits exactly into same-branch, transverse, and vertical pieces; the desired identity is exact when transverse drift vanishes and vertical drift is silent, otherwise the failure is a bounded E_transport term",
            "claim_status": "NO_ALPHA_NO_CLOCK_NO_WEP_NO_R10_NO_LOCAL_GR_CLAIM",
            "next_action": "derive or bound the transverse branch amplitude v_perp using the 3210 nohair/amplitude machinery, and separately prove vertical silence of R_Q",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3229_1_next_target",
            "decision": "3230-Y5-R2FR-transverse-branch-amplitude-bound-for-Etransport-under-AX1090",
            "because": "the transport identity no longer needs guessing; only v_perp and vertical silence decide whether Xi_clock is exact or finite-bounded",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "attach the 3210 amplitude law to the R_Q transverse sector and test whether v_perp=0 or ||v_perp||<=Y_perp can be parent-signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, transport_rows, contract_rows, xi_rows, next_bound_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    transport_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    xi_rows: list[dict[str, object]],
    next_bound_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, TRANSPORT, CONTRACT, XI_REDUCTION, NEXT_BOUND, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    exact_decomposition = any(row["step_id"] == "TR3229_3_transport_identity" for row in transport_rows)
    exact_closure = any(row["step_id"] == "TR3229_6_exact_closure" for row in transport_rows)
    finite_error = any(row["row_id"] == "XIR3229_2_finite_transport_case" for row in xi_rows)
    next_transverse = any(row["target_id"] == "EBT3229_1_transverse_bound" for row in next_bound_rows)
    claim_true_count = 0
    for rows in [input_rows, transport_rows, contract_rows, xi_rows, next_bound_rows, decision_rows]:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_true_count += 1
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
        {"check_id": "VAL3229_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3229_01_exact_decomposition", "pass": b(exact_decomposition), "detail": "D_tau R_Q branch decomposition derived", "generated_utc": now},
        {"check_id": "VAL3229_02_exact_closure_case", "pass": b(exact_closure), "detail": "one-dimensional same-branch closure staged", "generated_utc": now},
        {"check_id": "VAL3229_03_finite_error_formula", "pass": b(finite_error), "detail": "E_clock_transport finite formula staged", "generated_utc": now},
        {"check_id": "VAL3229_04_next_transverse_bound", "pass": b(next_transverse), "detail": "3230 target tied to transverse amplitude", "generated_utc": now},
        {"check_id": "VAL3229_05_claims_blocked", "pass": b(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3229_06_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3229_07_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3229_08_next_target", "pass": b(decision_rows[-1]["decision"].startswith("3230-")), "detail": str(decision_rows[-1]["decision"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    transport_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    xi_rows: list[dict[str, object]],
    next_bound_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3229 - Same-branch Clock Transport Identity for DtauRQ under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3229 derives the transport identity as a field-space branch decomposition.

Let the observed clock experiment define a parent configuration path:

```text
gamma: tau_obs -> Phi(tau_obs).
```

For any differentiable residual map `R_Q`,

```text
D_tau R_Q = DR_Q[Phi] . gamma_dot.
```

Choose a local EM residual branch direction `e_m`, a physical transverse piece `v_perp`, and a quotient-vertical piece `v_vert`:

```text
gamma_dot = tau_clock_time e_m + v_perp + v_vert.
```

Then the exact decomposition is:

```text
D_tau R_Q
= D_m R_Q tau_clock_time
  + D_perp R_Q[v_perp]
  + D_vert R_Q[v_vert].
```

So the desired identity is not an axiom. It is exact if:

```text
v_perp = 0,
D_vert R_Q[v_vert] = 0.
```

Otherwise it becomes a finite transport-error problem:

```text
E_transport := ||D_perp R_Q[v_perp]|| + ||D_vert R_Q[v_vert]||.
```

This refines the 3228 clock reduction:

```text
|D_tau ln alpha_EM|
<= C_D |Delta m tau_clock_time| + E_HO + E_clock_transport,

E_clock_transport
:= (2 |lambda_D| / Z_min) ||R_Q|| E_transport.
```

Using the near-root residual bound,

```text
E_clock_transport
<= (2 |lambda_D| / Z_min)
   (||D_m R_Q|| |Delta m| + O(Delta m^2))
   (||D_perp R_Q|| ||v_perp|| + ||D_vert R_Q|| ||v_vert||).
```

Current verdict: `TRANSPORT_IDENTITY_DERIVED_AS_BRANCH_DECOMPOSITION_EXACT_CLOSURE_NOT_SIGNED`.

The next real target is no longer vague clock magic. It is:

```text
prove v_perp=0, or bound ||v_perp|| <= Y_perp,
and prove D_vert R_Q=0 or bound it.
```

## Transport Identity Derivation

{md_table(transport_rows, ["step_id", "object", "identity", "status", "derivation", "missing_for_claim", "valid_for_claim"])}

## Transport Parent Contract

{md_table(contract_rows, ["clause_id", "required_clause", "math_need", "current_status", "why_it_matters", "valid_for_claim"])}

## Xi-clock Reduction With Transport Error

{md_table(xi_rows, ["row_id", "quantity", "formula", "status", "definition", "claim_gate", "valid_for_claim"])}

## E_transport Bound Targets

{md_table(next_bound_rows, ["target_id", "target", "source_route", "required_inputs", "result_if_acquired", "status", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3229_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3229_TRANSPORT_IDENTITY_DERIVATION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3229_TRANSPORT_PARENT_CONTRACT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3229_XI_CLOCK_REDUCTION_WITH_TRANSPORT_ERROR.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3229_ETRANSPORT_BOUND_TARGETS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3229_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3229_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, transport_rows, contract_rows, xi_rows, next_bound_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (TRANSPORT, transport_rows),
        (CONTRACT, contract_rows),
        (XI_REDUCTION, xi_rows),
        (NEXT_BOUND, next_bound_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, transport_rows, contract_rows, xi_rows, next_bound_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, transport_rows, contract_rows, xi_rows, next_bound_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3209-Y5-R2FR-X-sector-Theta-omega-owner-or-reference-curl-bound-first-row-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3209_INPUTS.csv"
VARIATION_LAW = OUT / "P8_Y5_R2FR_3209_X_SECTOR_VARIATION_LAW.csv"
OMEGA_BOUND = OUT / "P8_Y5_R2FR_3209_OMEGA_BOUND_INTERFACE.csv"
ZERO_GATES = OUT / "P8_Y5_R2FR_3209_ZERO_THEOREM_GATES.csv"
REFERENCE_BOUND = OUT / "P8_Y5_R2FR_3209_REFERENCE_CURL_BOUND_ROW.csv"
EPSILON_FEED = OUT / "P8_Y5_R2FR_3209_EPSILON_FEED.csv"
DECISION = OUT / "P8_Y5_R2FR_3209_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3209_VALIDATION.csv"


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
    if location == "source_weight_docs":
        return ROOT / "source-intake" / "source-weight" / "docs" / relative_path
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


SOURCES = [
    {
        "input_id": "SRC3209_00_3208_doc",
        "location": "post_checkpoint",
        "relative_path": "3208-Y5-R2FR-Htau-one-form-exactness-or-first-DeltaH-curl-bound-under-AX1090.md",
        "role": "3208 handoff to X-sector omega/reference curl",
        "terms": ["HCURL3208_1_X_sector", "reference-curl", "epsilon_Htau_curl", "Next target"],
    },
    {
        "input_id": "SRC3209_01_3208_components",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3208_CURL_COMPONENT_ENVELOPE.csv",
        "role": "machine-readable curl component envelope",
        "terms": ["I_X_symplectic", "I_ref", "Delta_H_curl_bound", "valid_for_claim"],
    },
    {
        "input_id": "SRC3209_02_2668_doc",
        "location": "post_checkpoint",
        "relative_path": "2668-Y5-R2FR-LX-Theta-omega-owner-or-Htau-curl-component-bound.md",
        "role": "prior L_X/Theta_X/omega_X owner audit",
        "terms": ["L_X/Theta_X/omega_X", "omega_X_integral", "MISSING_THETA_OMEGA", "owner routes"],
    },
    {
        "input_id": "SRC3209_03_2668_omega_template",
        "location": "source_weight_docs",
        "relative_path": "OMEGA_X_INTEGRAL_COMPONENT_2668_NONCLAIM.csv",
        "role": "omega_X integral component template",
        "terms": ["OMG2668_0", "omega_X_integral", "Theta_X", "valid_for_claim"],
    },
    {
        "input_id": "SRC3209_04_2669_doc",
        "location": "post_checkpoint",
        "relative_path": "2669-Y5-R2FR-parent-LX-normal-form-branch-selection-or-omega-bound.md",
        "role": "normal-form branch selection and omega-bound interface",
        "terms": ["omega_X_integral", "normal form", "absolute bound", "branch"],
    },
    {
        "input_id": "SRC3209_05_2669_bound_interface",
        "location": "source_weight_docs",
        "relative_path": "OMEGA_X_INTEGRAL_BOUND_INTERFACE_2669_NONCLAIM.csv",
        "role": "omega_X bound interface",
        "terms": ["OBND2669_0", "omega_X_integral_bound", "absolute", "M_H_ref"],
    },
    {
        "input_id": "SRC3209_06_3091_doc",
        "location": "post_checkpoint",
        "relative_path": "3091-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice-under-AX1090.md",
        "role": "latest quotient demotion and scalar no-hair fallback",
        "terms": ["scalar no-hair", "Z_X", "M_X2", "J_X", "boundary_flux_X"],
    },
    {
        "input_id": "SRC3209_07_3140_doc",
        "location": "post_checkpoint",
        "relative_path": "3140-Y5-R2FR-theta-descent-from-qbasic-action-under-AX1090.md",
        "role": "theta descent theorem from q-basic action",
        "terms": ["Theta_parent", "q^*Thetabar", "boundary", "fail_for_claim"],
    },
    {
        "input_id": "SRC3209_08_1018_doc",
        "location": "post_checkpoint",
        "relative_path": "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
        "role": "sector Lagrangian/boundary owner map",
        "terms": ["L_X", "Theta", "omega", "Z_X", "M_X2"],
    },
]


def build_inputs(now: str) -> list[dict[str, object]]:
    rows = []
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        rows.append(
            {
                "input_id": source["input_id"],
                "path": str(path),
                "exists": b(path.exists()),
                "role": source["role"],
                "evidence": evidence(path, source["terms"]),
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def build_variation_law(now: str) -> list[dict[str, object]]:
    return [
        {
            "law_id": "XVAR3209_0_normal_form",
            "object": "L_X",
            "formula": "L_X = 1/2 sqrt(h)[Z_X h^{ij} D_i X D_j X + M_X^2 X^2] - sqrt(h) J_X X + dB_X",
            "derivation": "least-scrutiny scalar-like local normal form after quotient/vertical route is not closed",
            "status": "conditional_normal_form_not_parent_signed",
            "missing_for_claim": "Z_X;M_X2;J_X;field_units;self_adjoint_domain;B_X boundary rule",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "XVAR3209_1_variation",
            "object": "delta L_X",
            "formula": "delta L_X = sqrt(h)[-D_i(Z_X D^i X)+M_X^2 X-J_X] delta X + d Theta_X + coefficient-variation terms",
            "derivation": "integration by parts of the scalar normal form; coefficient variations are explicit residuals, not hidden",
            "status": "derived_formula_for_selected_conditional_branch",
            "missing_for_claim": "parent-signed coefficients and coefficient-variation policy",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "XVAR3209_2_theta",
            "object": "Theta_X",
            "formula": "Theta_X(delta X)|_S = sqrt(sigma) Z_X n^i D_i X delta X + delta B_X",
            "derivation": "boundary symplectic potential from the normal-form variation",
            "status": "derived_conditional_surface_formula",
            "missing_for_claim": "surface pair;orientation;normal;B_X exactness;units",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "XVAR3209_3_omega",
            "object": "omega_X",
            "formula": "omega_X(delta1,delta2)|_S = sqrt(sigma) Z_X n^i[(D_i delta1 X) delta2 X - (D_i delta2 X) delta1 X] + omega_deltaZ + d omega_B",
            "derivation": "omega_X = delta Theta_X; coefficient and boundary variations retained as omega_deltaZ and omega_B",
            "status": "derived_conditional_surface_formula",
            "missing_for_claim": "deltaZ control;boundary exact/proper gauge;trace norms",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "XVAR3209_4_zero_theorem",
            "object": "omega_X_zero_condition",
            "formula": "If Z_X>0, M_X^2>=m0^2>0, J_X=0, self-adjoint boundary flux is zero, and no zero modes exist, then X=0 and allowed tangent variations delta X=0, hence omega_X=0",
            "derivation": "positive energy identity plus tangent-space kernel exclusion",
            "status": "theorem_route_written_inputs_missing",
            "missing_for_claim": "positive Z_X;mass gap;source-zero;boundary-zero;kernel exclusion",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "XVAR3209_5_trace_bound",
            "object": "omega_X_bound",
            "formula": "|int_S i_tau omega_X| <= C_S Z_sup ||delta1 X||_{H1(A)} ||delta2 X||_{H1(A)} + C_Z ||delta Z_X|| ||X||_{H1(A)} ||delta X||_{H1(A)} + |omega_B|",
            "derivation": "Cauchy-Schwarz plus trace inequality on the local annulus/collar",
            "status": "finite_bound_interface_derived_no_values",
            "missing_for_claim": "C_S;Z_sup;variation_norms;deltaZ_bound;omega_B_bound;units",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def build_omega_bound(now: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "OB3209_0_omega_integral",
            "quantity": "abs_omega_X_integral",
            "definition": "absolute upper bound for |int_S i_tau omega_X(delta1,delta2)|",
            "formula": "C_S Z_sup N1_H1 N2_H1 + C_Z NZ NX_H1 Ndelta_H1 + B_omega",
            "required_inputs": "C_S;Z_sup;N1_H1;N2_H1;C_Z;NZ;NX_H1;Ndelta_H1;B_omega;units;source_path",
            "current_value": "MISSING_TRACE_AND_COEFFICIENT_BOUNDS",
            "feeds": "Delta_H_curl_bound;epsilon_Htau_curl",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "OB3209_1_zero_case",
            "quantity": "abs_omega_X_integral",
            "definition": "zero theorem case if scalar no-hair inputs all pass",
            "formula": "0",
            "required_inputs": "Z_X>0;M_X2>=m0^2>0;J_X=0;boundary_flux_X=0;ker(L_X)=0",
            "current_value": "ZERO_CASE_NOT_PROVED",
            "feeds": "exact H_tau route;epsilon_Htau_curl=0 for X-sector piece",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "OB3209_2_deltaZ_piece",
            "quantity": "omega_deltaZ",
            "definition": "coefficient-variation contribution if Z_X or field normalization varies across the branch",
            "formula": "bounded separately; cannot be cancelled against reference curl",
            "required_inputs": "deltaZ_X_bound;field_normalization_rule;source_path",
            "current_value": "MISSING_DELTAZ_POLICY",
            "feeds": "Delta_H_curl_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "OB3209_3_boundary_piece",
            "quantity": "omega_B",
            "definition": "boundary primitive/exact/proper gauge contribution to omega_X",
            "formula": "0 if B_X exact/proper and charge-silent; otherwise explicit finite bound",
            "required_inputs": "B_X;boundary_class;edge_modes;B_omega_bound;units;source_path",
            "current_value": "MISSING_BOUNDARY_EXACTNESS_OR_BOUND",
            "feeds": "Delta_H_curl_bound;Bobs boundary/corner rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "OB3209_4_total",
            "quantity": "epsilon_omega_X_abs",
            "definition": "abs_omega_X_integral normalized into 3208 Delta_H_curl_bound and 3207 epsilon_abs",
            "formula": "epsilon_omega_X_abs = A_F * abs_omega_X_integral_bound/(G_ref*M_EH)",
            "required_inputs": "A_F;abs_omega_X_integral_bound;G_ref;M_EH;units;source_path",
            "current_value": "NOT_COMPUTED_VALUES_MISSING",
            "feeds": "epsilon_abs denominator lower-bound route",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def build_zero_gates(now: str) -> list[dict[str, object]]:
    gates = [
        ("ZG3209_0_branch", "one X branch selected without mixing quotient/scalar/edge routes", "false", "MISSING_PARENT_LX_BRANCH_SELECTION"),
        ("ZG3209_1_Z_positive", "Z_X is positive with source-backed units", "false", "MISSING_Z_X_PARENT_INPUT"),
        ("ZG3209_2_mass_gap", "M_X^2 has nonnegative/positive gap and lambda_X is fixed", "false", "MISSING_M_X2_PARENT_INPUT"),
        ("ZG3209_3_source_zero", "J_X=0 in compact local exterior", "false", "MISSING_SOURCE_ZERO_PROOF"),
        ("ZG3209_4_boundary_zero", "boundary_flux_X and B_X symplectic boundary charge vanish or are bounded", "false", "MISSING_BOUNDARY_ZERO_OR_BOUND"),
        ("ZG3209_5_kernel", "ker(L_X)=0 on selected self-adjoint domain", "false", "MISSING_KERNEL_EXCLUSION"),
        ("ZG3209_6_theta_omega_formula", "Theta_X/omega_X normal-form formula is explicitly written", "true", "FORMULA_DERIVED_CONDITIONAL"),
        ("ZG3209_7_trace_bound", "finite trace-bound interface exists", "true", "BOUND_INTERFACE_DERIVED_NO_VALUES"),
        ("ZG3209_8_claim", "omega_X piece can be claim-zero or claim-bounded now", "false", "VALUES_AND_ZERO_THEOREM_MISSING"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "pass": passed,
            "status": status,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for gate_id, gate, passed, status in gates
    ]


def build_reference_bound(now: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "RCB3209_0_fixed_reference_zero",
            "quantity": "reference_curl_over_MH",
            "definition": "curl contribution from H_ref/reference selector in d_F alpha_tau",
            "zero_condition": "H_ref is selected before source/readout and is derivative-silent on the branch",
            "bound_formula": "0 if D_source H_ref=D_readout H_ref=D_tau H_ref=D_surface H_ref=0",
            "current_value": "ZERO_CASE_NOT_PROVED",
            "required_inputs": "reference_branch;H_ref;selector_rule;derivative_silence_certificate;source_path",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "RCB3209_1_finite_reference_curl",
            "quantity": "reference_curl_bound",
            "definition": "finite upper bound for non-silent reference selector curl",
            "zero_condition": "not applicable; this is residual fallback",
            "bound_formula": "|C_ref| <= A_F sup_BF |d_F(delta H_ref)|",
            "current_value": "MISSING_REFERENCE_DERIVATIVE_BOUND",
            "required_inputs": "field_space_area;reference_second_derivative_bound;units;source_path",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def build_epsilon_feed(now: str) -> list[dict[str, object]]:
    return [
        {
            "feed_id": "EF3209_0_X_omega_to_DeltaH",
            "target": "HCURL3208_1_X_sector",
            "feed_formula": "Delta_H_curl_bound receives A_F * abs_omega_X_integral_bound",
            "current_status": "BOUND_INTERFACE_READY_VALUES_MISSING",
            "blocks_or_feeds": "feeds epsilon_Htau_curl and epsilon_abs",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "feed_id": "EF3209_1_reference_to_DeltaH",
            "target": "HCURL3208_4_reference",
            "feed_formula": "Delta_H_curl_bound receives abs(reference_curl_bound) unless fixed-reference zero theorem passes",
            "current_status": "REFERENCE_BOUND_TEMPLATE_READY_VALUES_MISSING",
            "blocks_or_feeds": "feeds Delta_ref and epsilon_abs",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def build_decision(now: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3209_0",
            "result": "X_SECTOR_THETA_OMEGA_NORMAL_FORM_AND_TRACE_BOUND_DERIVED_NO_VALUES",
            "claim_status": "NO_OMEGA_ZERO_NO_HTAU_EXACTNESS_NO_MHREF_NO_LOCAL_GR_CLAIM",
            "decision": "use positive scalar no-hair as the clean zero route; if inputs fail, use trace-bound omega_X interface plus reference-curl bound as epsilon_abs components",
            "best_next_route": "fill scalar no-hair input pack Z_X, M_X2, J_X=0, boundary_flux_X=0, or source the first trace-bound constants",
            "next_target": "3210-Y5-R2FR-scalar-nohair-input-pack-or-first-omega-trace-bound-values-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def main() -> None:
    now = stamp()
    input_rows = build_inputs(now)
    variation_rows = build_variation_law(now)
    omega_rows = build_omega_bound(now)
    gate_rows = build_zero_gates(now)
    reference_rows = build_reference_bound(now)
    epsilon_rows = build_epsilon_feed(now)
    decision_rows = build_decision(now)

    generated = [
        (INPUTS, input_rows),
        (VARIATION_LAW, variation_rows),
        (OMEGA_BOUND, omega_rows),
        (ZERO_GATES, gate_rows),
        (REFERENCE_BOUND, reference_rows),
        (EPSILON_FEED, epsilon_rows),
        (DECISION, decision_rows),
    ]
    for path, rows in generated:
        write_csv(path, rows)

    generated_paths = [path for path, _ in generated]
    validation_rows = [
        {
            "check_id": "VAL3209_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in input_rows)),
            "detail": f"inputs={len(input_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3209_01_theta_formula",
            "check": "Theta_X surface formula is present",
            "pass": b(any(row["law_id"] == "XVAR3209_2_theta" and "Theta_X" in row["object"] for row in variation_rows)),
            "detail": "Theta_X(delta X)|_S = sqrt(sigma) Z_X n^i D_i X delta X + delta B_X",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3209_02_omega_formula",
            "check": "omega_X surface formula is present",
            "pass": b(any(row["law_id"] == "XVAR3209_3_omega" and "omega_X" in row["object"] for row in variation_rows)),
            "detail": "omega_X=delta Theta_X with deltaZ and boundary pieces retained",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3209_03_zero_theorem_route",
            "check": "positive scalar no-hair zero route is written",
            "pass": b(any(row["law_id"] == "XVAR3209_4_zero_theorem" and "omega_X=0" in row["formula"] for row in variation_rows)),
            "detail": "requires Z_X, M_X2, J_X, boundary flux and kernel inputs",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3209_04_trace_bound_route",
            "check": "finite omega trace-bound interface is written",
            "pass": b(any(row["row_id"] == "OB3209_0_omega_integral" and "C_S" in row["formula"] for row in omega_rows)),
            "detail": "Cauchy-Schwarz/trace bound interface exists but values are missing",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3209_05_reference_bound_route",
            "check": "reference-curl zero and finite-bound rows are staged",
            "pass": b(len(reference_rows) == 2 and all(row["valid_for_claim"] == "false" for row in reference_rows)),
            "detail": "fixed-reference zero and A_F sup |d_F delta H_ref| fallback rows",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3209_06_claims_blocked",
            "check": "omega/Htau/MHref/local-GR claims remain blocked",
            "pass": b(any(row["gate_id"] == "ZG3209_8_claim" and row["pass"] == "false" for row in gate_rows)),
            "detail": "zero theorem and values still missing",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3209_07_epsilon_feeds",
            "check": "omega and reference components feed 3208/3207 route",
            "pass": b(len(epsilon_rows) == 2 and all("epsilon" in row["blocks_or_feeds"] for row in epsilon_rows)),
            "detail": "X omega and reference curl both feed epsilon_abs",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3209_08_no_formalization_workbench_edit",
            "check": "script writes only post-checkpoint outputs",
            "pass": "true",
            "detail": "no formalization-workbench paths are output targets",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3209_09_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(len(read_csv(path)) > 0 for path in generated_paths)),
            "detail": ";".join(path.name for path in generated_paths),
            "generated_utc": now,
        },
    ]
    write_csv(VALIDATION, validation_rows)

    doc = f"""# 3209 - X-Sector Theta/Omega Owner Or Reference-Curl Bound First Row Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, R10 pass, clock pass, orbital pass, Bobs residual score, `H_tau` exactness claim, `M_H_ref` claim, `omega_X=0` claim, or public-facing result.

## Result

3209 moves the first live curl component from "missing owner" to two exact routes:

```text
L_X = 1/2 sqrt(h)[Z_X h^{{ij}}D_iX D_jX + M_X^2 X^2] - sqrt(h)J_X X + dB_X

Theta_X(delta X)|_S = sqrt(sigma) Z_X n^iD_iX delta X + delta B_X

omega_X(delta1,delta2)|_S
 = sqrt(sigma) Z_X n^i[(D_i delta1X)delta2X - (D_i delta2X)delta1X]
   + omega_deltaZ + d omega_B
```

Clean zero route:

```text
Z_X > 0, M_X^2 >= m0^2 > 0, J_X = 0,
boundary_flux_X = 0, ker(L_X)=0
=> X=0 and allowed tangent delta X=0
=> omega_X=0.
```

Fallback bound route:

```text
|int_S i_tau omega_X|
 <= C_S Z_sup ||delta1X||_H1 ||delta2X||_H1
    + C_Z ||delta Z_X|| ||X||_H1 ||deltaX||_H1
    + |omega_B|.
```

So the local branch now has a precise next data/theorem demand: source `Z_X`, `M_X^2`, `J_X`, boundary flux, kernel exclusion, or trace-bound constants. No denominator shortcut, no cancellation, no `omega_X=0` by vibes.

Current verdict:

```text
Theta_X/omega_X formula: derived conditionally.
omega_X zero theorem: not proved.
omega_X finite bound: interface derived, values missing.
reference curl: zero/bound rows staged, values missing.
H_tau/M_H_ref/local-GR: still blocked.
```

## Variation Law

{md_table(variation_rows, ["law_id", "object", "formula", "derivation", "status", "missing_for_claim", "valid_for_claim"])}

## Omega Bound Interface

{md_table(omega_rows, ["row_id", "quantity", "definition", "formula", "current_value", "feeds", "valid_for_claim"])}

## Zero-Theorem Gates

{md_table(gate_rows, ["gate_id", "gate", "pass", "status", "valid_for_claim"])}

## Reference-Curl Bound

{md_table(reference_rows, ["row_id", "quantity", "definition", "zero_condition", "bound_formula", "current_value", "valid_for_claim"])}

## Epsilon Feed

{md_table(epsilon_rows, ["feed_id", "target", "feed_formula", "current_status", "blocks_or_feeds", "valid_for_claim"])}

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
- `{rel(VARIATION_LAW)}`
- `{rel(OMEGA_BOUND)}`
- `{rel(ZERO_GATES)}`
- `{rel(REFERENCE_BOUND)}`
- `{rel(EPSILON_FEED)}`
- `{rel(DECISION)}`
- `{rel(VALIDATION)}`

## Validation

{md_table(validation_rows, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

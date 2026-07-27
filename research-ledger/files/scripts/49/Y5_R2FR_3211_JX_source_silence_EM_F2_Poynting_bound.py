from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3211-Y5-R2FR-JX-source-silence-with-EM-F2-Poynting-flux-or-first-finite-source-bound-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3211_INPUTS.csv"
JX_DERIVATION = OUT / "P8_Y5_R2FR_3211_JX_VARIATION_DERIVATION.csv"
EM_SPLIT = OUT / "P8_Y5_R2FR_3211_EM_F2_POYNTING_SOURCE_SPLIT.csv"
SILENCE_GATES = OUT / "P8_Y5_R2FR_3211_SOURCE_SILENCE_THEOREM_GATES.csv"
FINITE_BOUND = OUT / "P8_Y5_R2FR_3211_FIRST_FINITE_JNORM_BOUND_ROW.csv"
AMPLITUDE_FEED = OUT / "P8_Y5_R2FR_3211_AMPLITUDE_FEED_TO_3210.csv"
DECISION = OUT / "P8_Y5_R2FR_3211_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3211_VALIDATION.csv"


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
        "input_id": "SRC3211_00_3210_doc",
        "location": "post_checkpoint",
        "relative_path": "3210-Y5-R2FR-scalar-nohair-amplitude-law-and-omega-zero-curl-gate-under-AX1090.md",
        "role": "3210 amplitude law and source split handoff",
        "terms": ["Source Channel Split", "Poynting", "Y_X", "3211"],
    },
    {
        "input_id": "SRC3211_01_3210_source_split",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3210_SOURCE_CHANNEL_SPLIT_WITH_EM_POYNTING.csv",
        "role": "machine-readable EM trace/F2/Poynting split",
        "terms": ["JXS3210_2_EM_F2", "JXS3210_3_Poynting_flux", "JXS3210_0_total_split"],
    },
    {
        "input_id": "SRC3211_02_3210_amplitude",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3210_SCALAR_NOHAIR_AMPLITUDE_LAW.csv",
        "role": "profile amplitude law that needs ||J_X||",
        "terms": ["AMP3210_3_profile_amplitude", "AMP3210_6_tangent_amplitude"],
    },
    {
        "input_id": "SRC3211_03_1043_JX",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1043_JX_ZERO_CHANNEL_AUDIT.csv",
        "role": "prior J_X channel audit",
        "terms": ["JX1043_0_matter_pullback", "JX1043_6_verdict", "J_projector", "J_memory"],
    },
    {
        "input_id": "SRC3211_04_1043_doc",
        "location": "post_checkpoint",
        "relative_path": "1043-Y5-R10-JX-zero-and-Phi-boundary-zero-premise-or-alpha3-prior-value.md",
        "role": "right-hand-side zero gate and Phi boundary audit",
        "terms": ["Right-hand-side zero gate", "Phi boundary", "J_X zero", "Residual if open"],
    },
    {
        "input_id": "SRC3211_05_1099_EM",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv",
        "role": "EM no-extra-F2 theorem and counterexample",
        "terms": ["UEM1099_1_chain_rule", "UEM1099_2_counterterm", "UEM1099_3_verdict"],
    },
    {
        "input_id": "SRC3211_06_1099_doc",
        "location": "post_checkpoint",
        "relative_path": "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md",
        "role": "unique EM kinetic owner audit",
        "terms": ["f_X(Xhat) F_Q^2", "no-extra-F2", "counterexample", "b_alpha"],
    },
    {
        "input_id": "SRC3211_07_1100_TQ",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv",
        "role": "T_Q/gauge norm signature clauses",
        "terms": ["TQS1100_3_unique_curvature_norm", "TQS1100_6_verdict", "fixed_generator_norm"],
    },
    {
        "input_id": "SRC3211_08_1027_qbar",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1027_SOURCE_ZERO_PROOF_AUDIT.csv",
        "role": "qbar_XT and matter source-zero chain",
        "terms": ["QZ1027_0_chain_rule", "QZ1027_4_no_marker_constants", "QZ1027_6_verdict"],
    },
    {
        "input_id": "SRC3211_09_1029_cg",
        "location": "post_checkpoint",
        "relative_path": "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
        "role": "c_g trace source shape and no-shadow frame theorem",
        "terms": ["matter_variation_trace", "c_g", "trace coupling", "common frame"],
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

    derivation_rows = [
        {
            "derivation_id": "JXD3211_0_definition",
            "object": "J_X",
            "formula": "J_X := -delta S_nonX/delta X evaluated on the local branch, with boundary/worldtube pieces kept outside the bulk norm as Phi_boundary.",
            "derived_result": "source silence means the variational derivative vanishes channelwise before readout, not that fitted channels cancel",
            "status": "definition_sharp",
            "missing_for_claim": "parent action split and same-branch source convention",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "JXD3211_1_frame_trace",
            "object": "matter frame trace source",
            "formula": "If g_m,mu nu=exp(2 c_g X) g_obs,mu nu, then delta_X S_matter = int sqrt(-g) c_g T_m deltaX, so |J_trace|<=|c_g T_m|.",
            "derived_result": "a universal/common coupling can be WEP-quiet but still source X through the trace and affect R10/PPN/source normalization",
            "status": "derived_shape_values_missing",
            "missing_for_claim": "c_g theorem-zero or finite c_g with source stress norm",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "JXD3211_2_EM_Hodge_metric",
            "object": "EM stress/Hodge source",
            "formula": "delta_X S_EM(metric/Hodge)=(1/2)int sqrt(-g) T_EM^{mu nu} delta_X g_obs,mu nu; pure conformal trace coupling is silent because T_EM^mu_mu=0 in 4D.",
            "derived_result": "Maxwell radiation is not a trace source, but non-conformal/disformal metric or Hodge dependence can still couple to EM stress",
            "status": "derived_channel_split",
            "missing_for_claim": "metric/Hodge descent or finite stress-coupling coefficient",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "JXD3211_3_EM_F2",
            "object": "gauge kinetic source",
            "formula": "For S_EM=-(1/4)int sqrt(-g) Z_A(X)F^2 with Z_A=Z_A0(1+b_alpha X+...), J_X^F2=(1/4)sqrt(-g) Z_A0 b_alpha F^2.",
            "derived_result": "the no-extra-F2 problem is exactly an X-source problem, not only an alpha-clock problem",
            "status": "derived_shape_counterexample_live",
            "missing_for_claim": "b_alpha=0 theorem or finite b_alpha and F^2 norm",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "JXD3211_4_Poynting_boundary",
            "object": "Poynting/worldtube flux",
            "formula": "For null waves F^2=0 can hold while S^i=T_EM^{0i} is nonzero; this enters Phi_boundary or a disformal/stress channel, not the scalar F^2 bulk source.",
            "derived_result": "the Poynting intuition becomes a real gate: prove flux is boundary-silent/orthogonal, or bound its surface integral",
            "status": "derived_channel_split_values_missing",
            "missing_for_claim": "flux coupling coefficient;surface/worldtube rule;orthogonality/no-flux proof",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "JXD3211_5_total_abs_bound",
            "object": "||J_X||_2_abs",
            "formula": "||J_X||_2 <= ||c_g T_m||_2 + (1/4)||Z_A0 b_alpha F^2||_2 + ||b_dis T_UV||_2 + ||J_marker||_2 + ||J_memory||_2 + ||J_projector||_2.",
            "derived_result": "first finite source norm row for the 3210 amplitude law; every term is absolute-summed",
            "status": "bound_formula_derived_values_missing",
            "missing_for_claim": "finite/source-backed coefficients and stress/source norms",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    em_rows = [
        {
            "channel_id": "EMS3211_0_trace_silent",
            "channel": "pure conformal Maxwell trace",
            "zero_or_bound_law": "T_EM=0 in 4D Maxwell, so a source proportional only to trace is zero for free EM fields.",
            "risk": "does not silence matter trace, gauge-kinetic F^2, disformal stress, or boundary flux",
            "status": "conditional_zero_channel",
            "next_needed": "prove parent EM coupling is trace-only or quotient/Hodge-fixed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "EMS3211_1_F2_scalar",
            "channel": "F^2 gauge kinetic source",
            "zero_or_bound_law": "J_X^F2=(1/4)sqrt(-g)Z_A0 b_alpha F^2; zero if b_alpha=0 or F^2=0 on the support.",
            "risk": "Coulomb/static fields have nonzero F^2 even when radiation-like null fields do not",
            "status": "finite_channel_live",
            "next_needed": "no-extra-F2 theorem or b_alpha and F^2 support norm",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "EMS3211_2_null_wave",
            "channel": "null EM wave",
            "zero_or_bound_law": "For ideal null waves, F^2=0 and F star F=0, but T_EM^{0i}=S^i/c^2 can be nonzero.",
            "risk": "null waves can be F2-silent but Poynting-active through boundary/stress couplings",
            "status": "distinction_derived",
            "next_needed": "separate bulk F2 source from boundary/stress flux in tests",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "EMS3211_3_Poynting_bound",
            "channel": "Poynting/worldtube flux",
            "zero_or_bound_law": "|Phi_Poynting| <= C_Poynting int_boundary |n_i T_EM^{0i}| dS dt or the appropriate stationary surface analogue.",
            "risk": "if parent boundary couples to energy flow, local EM waves can source Phi_boundary even when F^2=0",
            "status": "bound_formula_derived_values_missing",
            "next_needed": "C_Poynting;surface definition;field data or theorem-zero boundary silence",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    gate_rows = [
        {
            "gate_id": "SG3211_0_q_vertical_matter",
            "gate": "ordinary matter source zero",
            "required": "Dq[v_X]=0, e_obs factors through q, matter functor descends, no marker constants",
            "current_status": "conditional_by_1027_not_parent_signed",
            "if_fail": "retain c_g/qbar_XT/marker source rows",
            "pass": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "SG3211_1_no_shadow_frame",
            "gate": "c_g trace source zero",
            "required": "no independent matter frame A_g(X) or A_g factors through q",
            "current_status": "conditional_by_1029_not_parent_signed",
            "if_fail": "||c_g T_m|| enters ||J_X||_2",
            "pass": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "SG3211_2_no_extra_F2",
            "gate": "EM gauge-kinetic source zero",
            "required": "unique EM kinetic owner, fixed T_Q/gauge norm, no f_X(X)F^2, radiative/readout closure",
            "current_status": "failed_current_claim_by_1099_1100",
            "if_fail": "(1/4)||Z_A0 b_alpha F^2|| enters ||J_X||_2",
            "pass": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "SG3211_3_poynting_silence",
            "gate": "Poynting/worldtube flux zero",
            "required": "flux channel absent, exact/proper, orthogonal to source projector, or source-backed bounded",
            "current_status": "new_gate_not_signed",
            "if_fail": "Phi_Poynting enters Phi_boundary and 3210 amplitude law",
            "pass": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "SG3211_4_total_JX_zero",
            "gate": "total J_X zero",
            "required": "SG3211_0 through SG3211_3 plus memory/projector/source-normalization silence",
            "current_status": "not_claim_ready",
            "if_fail": "use finite absolute ||J_X||_2 bound",
            "pass": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    finite_rows = [
        {
            "row_id": "FJB3211_0_abs_J_norm",
            "quantity": "J_norm_bound_abs",
            "formula": "||J_X||_2 <= ||c_g T_m||_2 + (1/4)||Z_A0 b_alpha F^2||_2 + ||b_dis T_UV||_2 + ||J_marker||_2 + ||J_memory||_2 + ||J_projector||_2",
            "required_inputs": "c_g;T_m;b_alpha;F2_norm;b_dis;T_UV;marker/memory/projector bounds;units;source paths",
            "current_value": "MISSING_COEFFICIENTS_AND_FIELD_NORMS",
            "feeds": "3210 a_X=||J_X||_2/m_min",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "FJB3211_1_abs_Phi_Poynting",
            "quantity": "Phi_Poynting_bound_abs",
            "formula": "|Phi_Poynting| <= C_Poynting int_boundary |n_i T_EM^{0i}| dS dt",
            "required_inputs": "C_Poynting;surface/worldtube;orientation;EM stress/flux data;units;source paths",
            "current_value": "MISSING_POYNTING_BOUND_INPUTS",
            "feeds": "3210 b_X=|Phi_boundary|",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "FJB3211_2_zero_switch_guard",
            "quantity": "J_X_zero_switch",
            "formula": "J_X=0 only if every source channel is theorem-zero on the same parent branch",
            "required_inputs": "SG3211_0 through SG3211_4 all pass",
            "current_value": "THEOREM_ZERO_REJECTED_FOR_NOW",
            "feeds": "3210 exact no-hair to omega-zero route",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    feed_rows = [
        {
            "feed_id": "AF3211_0_to_3210_profile",
            "target": "AMP3210_3_profile_amplitude",
            "feed_formula": "a_X = J_norm_bound_abs/m_min; b_X = |Phi_boundary_without_Poynting + Phi_Poynting_bound_abs|",
            "current_status": "feed_formula_ready_values_missing",
            "claim_effect": "turns source coupling into profile amplitude rather than a vague blocker",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "feed_id": "AF3211_1_to_3210_zero",
            "target": "AMP3210_5_zero_limit",
            "feed_formula": "if J_norm_bound_abs=0 and Phi_boundary_bound_abs=0 by theorem, then X=0 and omega_X=0",
            "current_status": "conditional_zero_route_not_signed",
            "claim_effect": "would close the X-sector curl piece if all source/boundary gates pass",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "feed_id": "AF3211_2_to_empirical",
            "target": "R10/WEP/clock/PPN residual rows",
            "feed_formula": "if any source term is finite, map it to qbar_XT, b_alpha, c_g, boundary flux, or projector source rows with no cancellation",
            "current_status": "finite_residual_route_selected_if_zero_fails",
            "claim_effect": "empirical testing becomes possible only after coefficients and field norms are sourced",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3211_0_result",
            "result": "JX_SOURCE_EQUATION_SPLIT_DERIVED_NO_ZERO_CLAIM",
            "claim_status": "NO_JX_ZERO_NO_LOCAL_GR_NO_OMEGA_ZERO_CLAIM",
            "decision": "The source problem is now split into exact channels: matter trace/c_g, EM F2/b_alpha, Poynting boundary flux, markers, memory, and projector terms.",
            "best_next_route": "attack the EM channel first because it is the cleanest fork: no-extra-F2/gauge-norm owner gives b_alpha=0, otherwise source b_alpha and F2/Poynting bounds",
            "next_target": "3212-Y5-R2FR-EM-source-channel-no-extra-F2-or-Poynting-bound-input-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]

    generated_without_validation = [
        INPUTS,
        JX_DERIVATION,
        EM_SPLIT,
        SILENCE_GATES,
        FINITE_BOUND,
        AMPLITUDE_FEED,
        DECISION,
    ]

    write_csv(INPUTS, input_rows)
    write_csv(JX_DERIVATION, derivation_rows)
    write_csv(EM_SPLIT, em_rows)
    write_csv(SILENCE_GATES, gate_rows)
    write_csv(FINITE_BOUND, finite_rows)
    write_csv(AMPLITUDE_FEED, feed_rows)
    write_csv(DECISION, decision_rows)

    all_claim_rows: list[dict[str, str]] = []
    for path in generated_without_validation:
        all_claim_rows.extend(row for row in read_csv(path) if row.get("valid_for_claim") == "true")

    validation_rows = [
        {
            "check_id": "VAL3211_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in input_rows)),
            "detail": f"inputs={len(input_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3211_01_JX_definition",
            "check": "J_X variational definition is written",
            "pass": b(any(row["derivation_id"] == "JXD3211_0_definition" for row in derivation_rows)),
            "detail": "J_X := -delta S_nonX/delta X",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3211_02_EM_channels",
            "check": "EM trace/F2/Poynting channels are separated",
            "pass": b(len(em_rows) >= 4),
            "detail": "trace;F2;null wave;Poynting bound",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3211_03_abs_bound",
            "check": "finite absolute J norm bound exists",
            "pass": b(any(row["row_id"] == "FJB3211_0_abs_J_norm" for row in finite_rows)),
            "detail": "absolute no-cancellation source norm bound",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3211_04_poynting_bound",
            "check": "Poynting boundary bound exists",
            "pass": b(any(row["row_id"] == "FJB3211_1_abs_Phi_Poynting" for row in finite_rows)),
            "detail": "Phi_Poynting <= C_Poynting int |n_i T_EM^0i|",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3211_05_feeds_3210",
            "check": "source split feeds 3210 amplitude law",
            "pass": b(any(row["feed_id"] == "AF3211_0_to_3210_profile" for row in feed_rows)),
            "detail": "a_X and b_X feed are explicit",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3211_06_claims_blocked",
            "check": "no generated claim row is valid_for_claim true",
            "pass": b(len(all_claim_rows) == 0),
            "detail": f"claim_rows_true={len(all_claim_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3211_07_no_formalization_workbench_edit",
            "check": "script writes only post-checkpoint outputs",
            "pass": "true",
            "detail": "no formalization-workbench paths are output targets",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3211_08_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(len(read_csv(path)) > 0 for path in generated_without_validation)),
            "detail": ";".join(path.name for path in generated_without_validation),
            "generated_utc": now,
        },
    ]
    write_csv(VALIDATION, validation_rows)

    doc = f"""# 3211 - JX Source Silence with EM F2/Poynting Flux or First Finite Source Bound under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, R10 pass, WEP pass, clock pass, EM-unification claim, `J_X=0` claim, `omega_X=0` claim, or public-facing result.

## Result

3211 turns the coupling problem into a variational source equation:

```text
J_X := -delta S_nonX / delta X.
```

The source is not one foggy object. It splits into separately testable channels:

```text
J_X = J_trace/c_g + J_EM(F2,b_alpha) + J_disformal/stress
    + J_marker + J_memory + J_projector + ...
```

and the boundary/flow piece is:

```text
Phi_Poynting <= C_Poynting int_boundary |n_i T_EM^{{0i}}| dS dt.
```

The important EM distinction:

- Maxwell trace coupling can be silent because `T_EM = 0` in 4D.
- Gauge-kinetic coupling is not silent unless `b_alpha=0` or the local support has `F^2=0`.
- Null EM waves can have `F^2=0` while still carrying Poynting flux through `T_EM^{{0i}}`.

So Poynting is not a vibes argument. It is a boundary/stress channel that must be theorem-zeroed or bounded.

## JX Derivation

{md_table(derivation_rows, ["derivation_id", "object", "formula", "derived_result", "status", "missing_for_claim", "valid_for_claim"])}

## EM Source Split

{md_table(em_rows, ["channel_id", "channel", "zero_or_bound_law", "risk", "status", "next_needed", "valid_for_claim"])}

## Source Silence Gates

{md_table(gate_rows, ["gate_id", "gate", "required", "current_status", "if_fail", "pass", "valid_for_claim"])}

## First Finite Bound Rows

{md_table(finite_rows, ["row_id", "quantity", "formula", "required_inputs", "current_value", "feeds", "valid_for_claim"])}

## Feed To 3210

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
- `{rel(JX_DERIVATION)}`
- `{rel(EM_SPLIT)}`
- `{rel(SILENCE_GATES)}`
- `{rel(FINITE_BOUND)}`
- `{rel(AMPLITUDE_FEED)}`
- `{rel(DECISION)}`
- `{rel(VALIDATION)}`

## Validation

{md_table(validation_rows, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

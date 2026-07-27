from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3230-Y5-R2FR-transverse-branch-amplitude-bound-for-Etransport-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3230_INPUTS.csv"
BOUND = OUT / "P8_Y5_R2FR_3230_VPERP_AMPLITUDE_BOUND.csv"
ETRANSPORT = OUT / "P8_Y5_R2FR_3230_ETRANSPORT_REDUCTION.csv"
SOURCE_SPLIT = OUT / "P8_Y5_R2FR_3230_TRANSVERSE_SOURCE_CHANNEL_SPLIT.csv"
CLAIM_GATES = OUT / "P8_Y5_R2FR_3230_CLAIM_GATES.csv"
DECISION = OUT / "P8_Y5_R2FR_3230_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3230_VALIDATION.csv"


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
        "input_id": "SRC3230_00_3229_doc",
        "location": "post_checkpoint",
        "relative_path": "3229-Y5-R2FR-same-branch-clock-transport-identity-for-DtauRQ-under-AX1090.md",
        "role": "3229 handoff selecting transverse branch amplitude",
        "terms": ["v_perp", "E_transport", "Y_perp", "3230"],
    },
    {
        "input_id": "SRC3230_01_3229_targets",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3229_ETRANSPORT_BOUND_TARGETS.csv",
        "role": "machine E_transport target rows",
        "terms": ["EBT3229_0_transverse_zero", "EBT3229_1_transverse_bound", "D_vert"],
    },
    {
        "input_id": "SRC3230_02_3229_reduction",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3229_XI_CLOCK_REDUCTION_WITH_TRANSPORT_ERROR.csv",
        "role": "machine Xi reduction with transport error",
        "terms": ["E_clock_transport", "D_perpR_Q", "v_perp"],
    },
    {
        "input_id": "SRC3230_03_3210_doc",
        "location": "post_checkpoint",
        "relative_path": "3210-Y5-R2FR-scalar-nohair-amplitude-law-and-omega-zero-curl-gate-under-AX1090.md",
        "role": "amplitude/no-hair theorem source",
        "terms": ["Y_X", "delta_X_H1_bound", "X_zero", "source/boundary leakage"],
    },
    {
        "input_id": "SRC3230_04_3210_amp",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3210_SCALAR_NOHAIR_AMPLITUDE_LAW.csv",
        "role": "machine amplitude law",
        "terms": ["AMP3210_3_profile_amplitude", "AMP3210_6_tangent_amplitude", "m_min"],
    },
    {
        "input_id": "SRC3230_05_3210_zero",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3210_ZERO_TO_OMEGA_CURL_THEOREM.csv",
        "role": "machine zero/tangent collapse theorem",
        "terms": ["ZOC3210_1_profile_zero_to_tangent_zero", "ZOC3210_3_failure_to_bound"],
    },
    {
        "input_id": "SRC3230_06_3210_inputs",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3210_FIRST_BOUND_INPUT_PACK.csv",
        "role": "machine missing input pack for amplitude law",
        "terms": ["BND3210_0_Z_min", "BND3210_1_m_min", "BND3210_4_tangent_sources"],
    },
    {
        "input_id": "SRC3230_07_3210_source_split",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3210_SOURCE_CHANNEL_SPLIT_WITH_EM_POYNTING.csv",
        "role": "source channel split including Poynting guard",
        "terms": ["JXS3210_0_total_split", "JXS3210_2_EM_F2", "JXS3210_3_Poynting_flux"],
    },
    {
        "input_id": "SRC3230_08_3223_formula",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3223_FINITE_ALPHA_BOUND_FORMULA.csv",
        "role": "finite alpha/R_Q formula link",
        "terms": ["FORM3223_1_offroot_bound", "D_m R_Q", "Z_min"],
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

    bound_rows = [
        {
            "bound_id": "VP3230_0_transverse_variable",
            "object": "v_perp",
            "definition": "v_perp := P_perp gamma_dot, the physical clock-path tangent orthogonal to the EM residual branch e_m and quotient-vertical directions",
            "formula": "gamma_dot = tau_clock_time e_m + v_perp + v_vert",
            "status": "DEFINED_BY_3229_SPLIT",
            "missing_for_claim": "parent-owned P_perp and same configuration-space norm",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "VP3230_1_linearized_operator",
            "object": "v_perp equation",
            "definition": "transverse tangent solves a 3210-type linearized elliptic/coercive problem",
            "formula": "O_perp v_perp = J_perp^tau + Phi_perp^tau boundary terms",
            "status": "CONDITIONAL_OPERATOR_ROUTE",
            "missing_for_claim": "parent-signed O_perp; self-adjoint domain; positive kinetic and mass gap; same branch as R_Q",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "VP3230_2_energy_identity",
            "object": "E_perp",
            "definition": "transverse tangent energy",
            "formula": "E_perp := int_A[Z_perp |D v_perp|^2 + M_perp^2 |v_perp|^2 + P_mix_perp] dV",
            "status": "DERIVED_BY_3210_ANALOG",
            "missing_for_claim": "Z_perp>=Z_perp_min>0; M_perp^2>=m_perp_min^2>0; controlled mixing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "VP3230_3_amplitude_bound",
            "object": "Y_perp",
            "definition": "Y_perp := sqrt(E_perp)",
            "formula": "Y_perp <= (a_perp + sqrt(a_perp^2 + 4 b_perp))/2, with a_perp=||J_perp^tau||_2/m_perp_min and b_perp=|Phi_perp^tau|",
            "status": "AMPLITUDE_BOUND_DERIVED_CONDITIONALLY",
            "missing_for_claim": "numeric/source-backed J_perp^tau, Phi_perp^tau, m_perp_min, Z_perp_min",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "VP3230_4_norm_bound",
            "object": "||v_perp||",
            "definition": "transverse tangent L2/H1 norm control",
            "formula": "||v_perp||_2 <= Y_perp/m_perp_min and ||v_perp||_H1 <= Y_perp sqrt(1/m_perp_min^2 + 1/Z_perp_min)",
            "status": "NORM_BOUND_DERIVED_CONDITIONALLY",
            "missing_for_claim": "same norm convention used by D_perp R_Q operator bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "VP3230_5_zero_case",
            "object": "v_perp=0",
            "definition": "transverse no-hair/tangent collapse",
            "formula": "if J_perp^tau=0, Phi_perp^tau=0, ker(O_perp)=0, and positive coercivity holds, then Y_perp=0 and v_perp=0",
            "status": "EXACT_CONDITIONAL_ZERO_THEOREM",
            "missing_for_claim": "source silence, boundary silence, no zero modes, and parent-signed positivity on the R_Q transverse sector",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    etransport_rows = [
        {
            "reduction_id": "ETR3230_0_base_3229",
            "quantity": "E_transport",
            "formula": "E_transport := ||D_perp R_Q[v_perp]|| + ||D_vert R_Q[v_vert]||",
            "derived_bound": "base decomposition from 3229",
            "status": "INPUT_FROM_3229",
            "claim_gate": "needs v_perp bound and vertical silence/bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "reduction_id": "ETR3230_1_operator_norm",
            "quantity": "transverse contribution",
            "formula": "||D_perp R_Q[v_perp]|| <= ||D_perp R_Q||_op ||v_perp||",
            "derived_bound": "operator-norm inequality",
            "status": "DERIVED_CONDITIONALLY",
            "claim_gate": "requires source-backed ||D_perp R_Q||_op and matched v_perp norm",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "reduction_id": "ETR3230_2_Yperp_L2",
            "quantity": "transverse contribution",
            "formula": "||D_perp R_Q[v_perp]|| <= ||D_perp R_Q||_op Y_perp/m_perp_min",
            "derived_bound": "finite transverse leakage bound",
            "status": "FINITE_BOUND_FORMULA",
            "claim_gate": "requires Y_perp inputs and D_perp R_Q operator norm",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "reduction_id": "ETR3230_3_zero_case",
            "quantity": "transverse contribution",
            "formula": "||D_perp R_Q[v_perp]|| = 0 if v_perp=0",
            "derived_bound": "exact transverse silence",
            "status": "EXACT_CONDITIONAL_ZERO",
            "claim_gate": "requires VP3230_5 zero premises",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "reduction_id": "ETR3230_4_clock_error",
            "quantity": "E_clock_transport",
            "formula": "E_clock_transport <= (2|lambda_D|/Z_min)(||D_mR_Q|| |Delta m|+O(Delta m^2)) (||D_perpR_Q||_op Y_perp/m_perp_min + vertical_term)",
            "derived_bound": "clock gate transport error with transverse amplitude inserted",
            "status": "REFINED_FINITE_CLOCK_ERROR",
            "claim_gate": "still needs lambda_D, Z_min, D_mR_Q, Delta m, Y_perp, D_perpR_Q, and vertical term",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    source_rows = [
        {
            "channel_id": "JPERP3230_0_total",
            "channel": "total transverse source",
            "formula": "J_perp^tau = J_geom_perp + J_matter_perp + J_EM_trace_perp + J_EM_F2_perp + J_Poynting_boundary_perp + J_memory_perp + J_projector_perp",
            "zero_or_bound_condition": "every channel is theorem-zero or has an absolute source-backed bound in the same transverse sector",
            "status": "CHANNEL_SPLIT_STAGED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "JPERP3230_1_EM_trace",
            "channel": "Maxwell trace",
            "formula": "T_EM trace can vanish for pure Maxwell in 4D",
            "zero_or_bound_condition": "only useful if transverse sector couples to EM trace and not F^2/Poynting/readout channels",
            "status": "POSSIBLE_ZERO_NOT_SUFFICIENT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "JPERP3230_2_EM_F2",
            "channel": "EM kinetic scalar coupling",
            "formula": "J_perp^EM_F2 proportional to f_perp'(0) F^2",
            "zero_or_bound_condition": "zero if no-extra-F2 theorem or f_perp'(0)=0; otherwise bound by local field invariant support",
            "status": "ACTIVE_DANGER_CHANNEL",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "JPERP3230_3_Poynting_flux",
            "channel": "EM wave/Poynting boundary flux",
            "formula": "null radiation can have F^2=0 while T_EM^{0i} and boundary/worldtube flux are nonzero",
            "zero_or_bound_condition": "must be shown orthogonal/proper/boundary-silent or finitely bounded; cannot be erased by F^2=0",
            "status": "ACTIVE_BOUNDARY_GUARD",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "JPERP3230_4_matter_marker",
            "channel": "matter/material constants",
            "formula": "J_perp^matter from Lie_vperp S_matter or material/readout labels",
            "zero_or_bound_condition": "zero if matter functor and labels descend through q with no transverse marker",
            "status": "UNSIGNED_SOURCE_FUNCTOR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "JPERP3230_5_boundary",
            "channel": "Phi_perp^tau",
            "formula": "all boundary/corner/source-worldtube flux for transverse tangent energy",
            "zero_or_bound_condition": "zero if exact/proper/orthogonal boundary theorem; otherwise finite source-backed absolute bound",
            "status": "MISSING_BOUNDARY_ZERO_OR_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    claim_gate_rows = [
        {
            "gate_id": "G3230_0_exact_transverse_zero",
            "gate": "v_perp=0 claim",
            "required_evidence": "O_perp positive/self-adjoint; J_perp^tau=0; Phi_perp^tau=0; ker(O_perp)=0; same R_Q branch",
            "current_status": "NOT_CLAIM_READY",
            "next_action": "try to prove source-channel silence and boundary silence for J_perp/Phi_perp",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3230_1_finite_vperp_bound",
            "gate": "||v_perp|| finite claim",
            "required_evidence": "numeric/source-backed m_perp_min, Z_perp_min, ||J_perp^tau||_2, |Phi_perp^tau|",
            "current_status": "FORMULA_READY_INPUTS_MISSING",
            "next_action": "acquire source-channel bounds without setting channels to zero by convention",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3230_2_clock_error_bound",
            "gate": "E_clock_transport bounded below clock residual budget",
            "required_evidence": "finite v_perp bound plus D_perpR_Q norm, lambda_D, Z_min, D_mR_Q, Delta m, vertical silence/bound",
            "current_status": "NOT_CLAIM_READY",
            "next_action": "vertical silence and D_perpR_Q norm are still needed after v_perp",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3230_0_result",
            "decision": "VPERP_ZERO_OR_BOUND_DERIVED_CONDITIONALLY_SOURCE_CHANNELS_NOT_SIGNED",
            "because": "the 3210 amplitude law gives an exact zero theorem or finite Y_perp bound for transverse clock-path drift, but the transverse source/boundary channels are not yet theorem-zero or source-bounded on the R_Q branch",
            "claim_status": "NO_ALPHA_NO_CLOCK_NO_WEP_NO_R10_NO_LOCAL_GR_CLAIM",
            "next_action": "attack the transverse source-channel silence/bound ledger, especially EM_F2 and Poynting boundary flux, and separately keep vertical silence as an open gate",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3230_1_next_target",
            "decision": "3231-Y5-R2FR-transverse-source-channel-silence-or-bound-for-Jperp-under-AX1090",
            "because": "v_perp is now controlled by J_perp and Phi_perp; the next real work is proving those channels vanish or bounding them without ignoring Poynting/EM_F2 leakage",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "derive zero/bound rows for J_perp^EM_F2, J_perp^Poynting_boundary, matter markers, memory/projector sources, and Phi_perp^tau",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, bound_rows, etransport_rows, source_rows, claim_gate_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    etransport_rows: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    claim_gate_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, BOUND, ETRANSPORT, SOURCE_SPLIT, CLAIM_GATES, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    amplitude_formula = any(row["bound_id"] == "VP3230_3_amplitude_bound" for row in bound_rows)
    zero_case = any(row["bound_id"] == "VP3230_5_zero_case" for row in bound_rows)
    finite_transport = any(row["reduction_id"] == "ETR3230_4_clock_error" for row in etransport_rows)
    poynting_guard = any(row["channel_id"] == "JPERP3230_3_Poynting_flux" for row in source_rows)
    claim_true_count = 0
    for rows in [input_rows, bound_rows, etransport_rows, source_rows, claim_gate_rows, decision_rows]:
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
        {"check_id": "VAL3230_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3230_01_amplitude_formula", "pass": b(amplitude_formula), "detail": "Y_perp bound derived from 3210 law", "generated_utc": now},
        {"check_id": "VAL3230_02_zero_case", "pass": b(zero_case), "detail": "v_perp=0 exact conditional theorem staged", "generated_utc": now},
        {"check_id": "VAL3230_03_transport_reduction", "pass": b(finite_transport), "detail": "E_clock_transport refined with Y_perp", "generated_utc": now},
        {"check_id": "VAL3230_04_poynting_guard", "pass": b(poynting_guard), "detail": "Poynting boundary channel retained", "generated_utc": now},
        {"check_id": "VAL3230_05_claims_blocked", "pass": b(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3230_06_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3230_07_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3230_08_next_target", "pass": b(decision_rows[-1]["decision"].startswith("3231-")), "detail": str(decision_rows[-1]["decision"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    etransport_rows: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    claim_gate_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3230 - Transverse Branch Amplitude Bound for Etransport under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3230 attaches the 3210 amplitude/no-hair machinery to the transverse clock-path error from 3229.

From 3229:

```text
D_tau R_Q
= D_m R_Q tau_clock_time
  + D_perp R_Q[v_perp]
  + D_vert R_Q[v_vert].
```

The transverse term is controlled by an amplitude problem. If the transverse tangent obeys a same-branch coercive equation,

```text
O_perp v_perp = J_perp^tau + boundary/corner/source-worldtube terms,
O_perp = -D_i(Z_perp D^i .) + M_perp^2 + nonnegative/controlled mixing,
```

then with

```text
Y_perp := sqrt(E_perp),
a_perp := ||J_perp^tau||_2 / m_perp_min,
b_perp := |Phi_perp^tau|,
```

the 3210 amplitude law gives:

```text
Y_perp <= (a_perp + sqrt(a_perp^2 + 4 b_perp))/2,
||v_perp||_2 <= Y_perp / m_perp_min.
```

So the transverse transport error becomes:

```text
||D_perp R_Q[v_perp]||
<= ||D_perp R_Q||_op Y_perp / m_perp_min.
```

And the clock error refines to:

```text
E_clock_transport
<= (2 |lambda_D| / Z_min)
   (||D_m R_Q|| |Delta m| + O(Delta m^2))
   (||D_perp R_Q||_op Y_perp/m_perp_min + vertical_term).
```

Exact zero case:

```text
J_perp^tau = 0,
Phi_perp^tau = 0,
ker(O_perp)=0,
Z_perp>=Z_perp_min>0,
M_perp^2>=m_perp_min^2>0
=> Y_perp=0
=> v_perp=0.
```

That is a real derivation route. It is not claim-ready because the source channels are not yet theorem-zero or source-bounded on the same `R_Q` transverse branch.

Current verdict: `VPERP_ZERO_OR_BOUND_DERIVED_CONDITIONALLY_SOURCE_CHANNELS_NOT_SIGNED`.

## Vperp Amplitude Bound

{md_table(bound_rows, ["bound_id", "object", "definition", "formula", "status", "missing_for_claim", "valid_for_claim"])}

## Etransport Reduction

{md_table(etransport_rows, ["reduction_id", "quantity", "formula", "derived_bound", "status", "claim_gate", "valid_for_claim"])}

## Transverse Source Channel Split

{md_table(source_rows, ["channel_id", "channel", "formula", "zero_or_bound_condition", "status", "valid_for_claim"])}

## Claim Gates

{md_table(claim_gate_rows, ["gate_id", "gate", "required_evidence", "current_status", "next_action", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3230_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3230_VPERP_AMPLITUDE_BOUND.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3230_ETRANSPORT_REDUCTION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3230_TRANSVERSE_SOURCE_CHANNEL_SPLIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3230_CLAIM_GATES.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3230_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3230_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, bound_rows, etransport_rows, source_rows, claim_gate_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (BOUND, bound_rows),
        (ETRANSPORT, etransport_rows),
        (SOURCE_SPLIT, source_rows),
        (CLAIM_GATES, claim_gate_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, bound_rows, etransport_rows, source_rows, claim_gate_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, bound_rows, etransport_rows, source_rows, claim_gate_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3231-Y5-R2FR-transverse-source-channel-silence-or-bound-for-Jperp-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3231_INPUTS.csv"
SOURCE_AUDIT = OUT / "P8_Y5_R2FR_3231_JPERP_SOURCE_SILENCE_AUDIT.csv"
BOUND_FORMULA = OUT / "P8_Y5_R2FR_3231_JPERP_FINITE_BOUND_FORMULA.csv"
PHI_AUDIT = OUT / "P8_Y5_R2FR_3231_PHI_PERP_BOUNDARY_AUDIT.csv"
VPERP_FEEDBACK = OUT / "P8_Y5_R2FR_3231_VPERP_FEEDBACK_TO_3230.csv"
DECISION = OUT / "P8_Y5_R2FR_3231_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3231_VALIDATION.csv"


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
        "input_id": "SRC3231_00_3230_doc",
        "location": "post_checkpoint",
        "relative_path": "3230-Y5-R2FR-transverse-branch-amplitude-bound-for-Etransport-under-AX1090.md",
        "role": "3230 handoff selecting J_perp source channels",
        "terms": ["J_perp", "EM_F2", "Poynting", "3231"],
    },
    {
        "input_id": "SRC3231_01_3230_split",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3230_TRANSVERSE_SOURCE_CHANNEL_SPLIT.csv",
        "role": "machine transverse source-channel split",
        "terms": ["JPERP3230_2_EM_F2", "JPERP3230_3_Poynting_flux", "JPERP3230_5_boundary"],
    },
    {
        "input_id": "SRC3231_02_3230_vperp",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3230_VPERP_AMPLITUDE_BOUND.csv",
        "role": "machine v_perp amplitude law",
        "terms": ["VP3230_3_amplitude_bound", "J_perp", "Phi_perp"],
    },
    {
        "input_id": "SRC3231_03_3210_doc",
        "location": "post_checkpoint",
        "relative_path": "3210-Y5-R2FR-scalar-nohair-amplitude-law-and-omega-zero-curl-gate-under-AX1090.md",
        "role": "source split and Poynting warning",
        "terms": ["Poynting", "EM_F2", "source/boundary", "J_X"],
    },
    {
        "input_id": "SRC3231_04_3210_source_split",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3210_SOURCE_CHANNEL_SPLIT_WITH_EM_POYNTING.csv",
        "role": "machine source split with EM/Poynting channels",
        "terms": ["JXS3210_2_EM_F2", "JXS3210_3_Poynting_flux", "JXS3210_4_matter_marker"],
    },
    {
        "input_id": "SRC3231_05_3220_doc",
        "location": "post_checkpoint",
        "relative_path": "3220-Y5-R2FR-parent-source-root-for-EM-F2-or-finite-double-zero-coefficient-input-under-AX1090.md",
        "role": "EM F2 source-root and wave-stress guard",
        "terms": ["F_Q^2=0", "Poynting", "EM_F2_SOURCE_ROOT_NOT_PARENT_SIGNED", "wave guard"],
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

    source_rows = [
        {
            "audit_id": "JPA3231_0_total_decomposition",
            "channel": "total J_perp",
            "source_formula": "J_perp^tau = J_geom + J_matter + J_EM_trace + J_EM_F2 + J_Poynting_bulk/collar + J_memory + J_projector",
            "zero_condition": "all summands are theorem-zero on the same parent transverse branch",
            "finite_bound": "||J_perp^tau||_2 <= sum_i ||J_i||_2 with absolute no-cancellation",
            "status": "DECOMPOSITION_DERIVED",
            "blocks_exact_zero": "any live channel",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "JPA3231_1_geom",
            "channel": "geometric/source curvature",
            "source_formula": "J_geom from transverse variation of the local operator/background geometry",
            "zero_condition": "local exterior solves parent Euler equations and P_perp excludes pure gauge/branch reparametrization",
            "finite_bound": "J_geom_bound := ||J_geom||_2",
            "status": "BOUND_SYMBOL_STAGED",
            "blocks_exact_zero": "MISSING_PARENT_EULER_SAME_BRANCH",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "JPA3231_2_EM_trace",
            "channel": "Maxwell trace",
            "source_formula": "J_EM_trace proportional to T_EM^mu_mu",
            "zero_condition": "trace-only coupling to pure Maxwell in 4D; no material/readout/F2/Poynting couplings",
            "finite_bound": "J_EM_trace_bound := ||c_trace T_EM||_2",
            "status": "CONDITIONAL_ZERO_NOT_SUFFICIENT",
            "blocks_exact_zero": "safe only for trace-only parent coupling",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "JPA3231_3_EM_F2",
            "channel": "EM kinetic F2 coupling",
            "source_formula": "J_EM_F2 = (1/4) f_perp_prime(0) F_{mu nu}F^{mu nu}",
            "zero_condition": "no-extra-F2 theorem, f_perp_prime(0)=0, strict same-branch EM source-root, or F^2 support zero plus no readout reentry",
            "finite_bound": "||J_EM_F2||_2 <= (1/4)|f_perp_prime(0)| ||F^2||_2",
            "status": "ACTIVE_DANGER_CHANNEL",
            "blocks_exact_zero": "MISSING_NO_EXTRA_F2_OR_SOURCE_ROOT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "JPA3231_4_Poynting",
            "channel": "Poynting/collar/worldtube flux",
            "source_formula": "J_Poynting or Phi_Poynting sourced by S_EM·n, T_EM^{0i}, or boundary/collar flux",
            "zero_condition": "flux channel is absent from parent coupling, or exact/proper/orthogonal boundary theorem kills it",
            "finite_bound": "J_Poynting_bound + Phi_Poynting_bound from absolute boundary/worldtube flux norm",
            "status": "ACTIVE_BOUNDARY_GUARD",
            "blocks_exact_zero": "F^2=0 DOES_NOT_KILL_POYNTING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "JPA3231_5_matter_marker",
            "channel": "matter/readout/material markers",
            "source_formula": "J_matter = Lie_vperp S_matter plus label/readout/material-constant variations",
            "zero_condition": "matter functor, labels, masses, charges, and readout descend through q with no transverse marker",
            "finite_bound": "J_matter_bound := ||Lie_vperp S_matter||_2 plus readout-marker bounds",
            "status": "UNSIGNED_SOURCE_FUNCTOR",
            "blocks_exact_zero": "MISSING_NO_MARKER_THEOREM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "JPA3231_6_memory_projector",
            "channel": "memory/projector",
            "source_formula": "J_memory + J_projector from transverse variation of memory kernel/projector/domain",
            "zero_condition": "projector commutes with transverse split or transverse sector is orthogonal to memory source",
            "finite_bound": "J_memory_projector_bound := ||J_memory||_2 + ||J_projector||_2",
            "status": "BOUND_SYMBOL_STAGED",
            "blocks_exact_zero": "MISSING_PROJECTOR_ORTHOGONALITY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    bound_rows = [
        {
            "bound_id": "JPB3231_0_total_norm",
            "quantity": "||J_perp^tau||_2",
            "formula": "||J_perp^tau||_2 <= J_geom_bound + J_matter_bound + J_EM_trace_bound + (1/4)|f_perp_prime(0)| ||F^2||_2 + J_Poynting_bound + J_memory_projector_bound",
            "zero_requirement": "each term is zero by theorem on the same R_Q transverse branch",
            "status": "FINITE_SUM_BOUND_DERIVED_SYMBOLIC",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JPB3231_1_exact_zero",
            "quantity": "J_perp^tau",
            "formula": "J_perp^tau=0 if J_geom=J_matter=J_EM_trace=J_EM_F2=J_Poynting=J_memory=J_projector=0",
            "zero_requirement": "no-extra-F2/source-root plus Poynting/boundary silence plus no-marker/projector orthogonality",
            "status": "EXACT_ZERO_CONDITION_DERIVED_NOT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JPB3231_2_Yperp_update",
            "quantity": "a_perp",
            "formula": "a_perp <= ||J_perp^tau||_2_bound / m_perp_min",
            "zero_requirement": "a_perp=0 only if total source norm is theorem-zero",
            "status": "FEEDS_3230_YPERP",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    phi_rows = [
        {
            "phi_id": "PHI3231_0_total_boundary",
            "quantity": "Phi_perp^tau",
            "formula": "|Phi_perp^tau| <= Phi_geom + Phi_matter + Phi_EM_F2_boundary + Phi_Poynting + Phi_memory_projector",
            "zero_condition": "each boundary/corner/worldtube term is exact/proper/orthogonal or absent",
            "status": "BOUND_DECOMPOSITION_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "phi_id": "PHI3231_1_Poynting_boundary",
            "quantity": "Phi_Poynting",
            "formula": "Phi_Poynting <= C_flux ||S_EM·n||_{boundary/collar/worldtube}",
            "zero_condition": "no EM flux through the relevant boundary, or flux term is exact/proper/orthogonal to v_perp",
            "status": "ACTIVE_BOUNDARY_GUARD",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "phi_id": "PHI3231_2_exact_zero",
            "quantity": "Phi_perp^tau=0",
            "formula": "Phi_perp^tau=0 if all boundary/corner/worldtube terms vanish theorem-wise",
            "zero_condition": "not established by F^2=0 or trace silence alone",
            "status": "EXACT_ZERO_CONDITION_DERIVED_NOT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    feedback_rows = [
        {
            "feedback_id": "VFB3231_0_finite_Yperp",
            "feeds": "VP3230_3_amplitude_bound",
            "substitution": "a_perp=J_perp_bound/m_perp_min; b_perp=Phi_perp_bound",
            "result": "Y_perp <= (J_perp_bound/m_perp_min + sqrt((J_perp_bound/m_perp_min)^2 + 4 Phi_perp_bound))/2",
            "claim_status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "feedback_id": "VFB3231_1_exact_vperp_zero",
            "feeds": "VP3230_5_zero_case",
            "substitution": "J_perp_bound=0 and Phi_perp_bound=0",
            "result": "Y_perp=0 and v_perp=0 if O_perp is positive with no kernel",
            "claim_status": "ZERO_ROUTE_CLEAR_BUT_UNSIGNED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "feedback_id": "VFB3231_2_live_danger_channels",
            "feeds": "3232 target",
            "substitution": "EM_F2 and Poynting are the first channels to prove zero or bound",
            "result": "trace silence alone cannot close v_perp; F^2=0 alone cannot close Poynting",
            "claim_status": "NEXT_TARGET_SELECTED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3231_0_result",
            "decision": "JPERP_SOURCE_SPLIT_DERIVED_EMF2_AND_POYNTING_REMAIN_LIVE",
            "because": "the transverse source norm now has an exact no-cancellation bound and an exact zero condition, but EM_F2 and Poynting/boundary flux cannot be killed by Maxwell trace silence or F^2=0 alone",
            "claim_status": "NO_ALPHA_NO_CLOCK_NO_WEP_NO_R10_NO_LOCAL_GR_CLAIM",
            "next_action": "attack EM_F2 no-extra/source-root and Poynting boundary silence/bounds as the first live channels feeding v_perp",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3231_1_next_target",
            "decision": "3232-Y5-R2FR-EMF2-and-Poynting-transverse-source-zero-or-bound-under-AX1090",
            "because": "these are the channels most likely to spoil v_perp=0; closing or bounding them directly improves the local clock/EM coupling gate",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "derive no-extra-F2/source-root conditions for f_perp_prime(0), and a proper/orthogonal/finite Poynting flux boundary clause",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, source_rows, bound_rows, phi_rows, feedback_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    phi_rows: list[dict[str, object]],
    feedback_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, SOURCE_AUDIT, BOUND_FORMULA, PHI_AUDIT, VPERP_FEEDBACK, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    total_bound = any(row["bound_id"] == "JPB3231_0_total_norm" for row in bound_rows)
    emf2_live = any(row["audit_id"] == "JPA3231_3_EM_F2" and row["status"] == "ACTIVE_DANGER_CHANNEL" for row in source_rows)
    poynting_live = any(row["audit_id"] == "JPA3231_4_Poynting" and row["status"] == "ACTIVE_BOUNDARY_GUARD" for row in source_rows)
    yperp_feedback = any(row["feedback_id"] == "VFB3231_0_finite_Yperp" for row in feedback_rows)
    claim_true_count = 0
    for rows in [input_rows, source_rows, bound_rows, phi_rows, feedback_rows, decision_rows]:
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
        {"check_id": "VAL3231_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3231_01_total_bound", "pass": b(total_bound), "detail": "J_perp no-cancellation finite sum bound derived", "generated_utc": now},
        {"check_id": "VAL3231_02_emf2_live_guard", "pass": b(emf2_live), "detail": "EM_F2 retained as active danger channel", "generated_utc": now},
        {"check_id": "VAL3231_03_poynting_live_guard", "pass": b(poynting_live), "detail": "Poynting/boundary flux retained as active guard", "generated_utc": now},
        {"check_id": "VAL3231_04_yperp_feedback", "pass": b(yperp_feedback), "detail": "J/Phi bounds feed Y_perp", "generated_utc": now},
        {"check_id": "VAL3231_05_claims_blocked", "pass": b(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3231_06_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3231_07_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3231_08_next_target", "pass": b(decision_rows[-1]["decision"].startswith("3232-")), "detail": str(decision_rows[-1]["decision"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    phi_rows: list[dict[str, object]],
    feedback_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3231 - Transverse Source Channel Silence Or Bound for Jperp under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3231 splits the source that controls the transverse clock-path drift from 3230.

The zero route is exact but demanding:

```text
J_perp^tau = 0,
Phi_perp^tau = 0,
O_perp positive with no kernel
=> Y_perp=0
=> v_perp=0.
```

But `J_perp^tau=0` is not a single statement. The no-cancellation split is:

```text
J_perp^tau
= J_geom
 + J_matter
 + J_EM_trace
 + J_EM_F2
 + J_Poynting_bulk/collar
 + J_memory
 + J_projector.
```

Therefore

```text
||J_perp^tau||_2
<= J_geom_bound
 + J_matter_bound
 + J_EM_trace_bound
 + (1/4)|f_perp_prime(0)| ||F^2||_2
 + J_Poynting_bound
 + J_memory_projector_bound.
```

Boundary/collar flux contributes separately:

```text
|Phi_perp^tau|
<= Phi_geom + Phi_matter + Phi_EM_F2_boundary
 + Phi_Poynting + Phi_memory_projector.
```

This feeds the 3230 amplitude law:

```text
Y_perp <= (J_perp_bound/m_perp_min
          + sqrt((J_perp_bound/m_perp_min)^2 + 4 Phi_perp_bound))/2.
```

Key result: Maxwell trace silence is not enough. The two live danger channels are:

```text
J_EM_F2 = (1/4) f_perp_prime(0) F^2,
Phi_Poynting <= C_flux ||S_EM · n||_boundary/collar/worldtube.
```

`F^2=0` can silence one scalar bulk invariant, but it does not silence Poynting/stress/boundary flux.

Current verdict: `JPERP_SOURCE_SPLIT_DERIVED_EMF2_AND_POYNTING_REMAIN_LIVE`.

## Jperp Source Silence Audit

{md_table(source_rows, ["audit_id", "channel", "source_formula", "zero_condition", "finite_bound", "status", "blocks_exact_zero", "valid_for_claim"])}

## Jperp Finite Bound Formula

{md_table(bound_rows, ["bound_id", "quantity", "formula", "zero_requirement", "status", "valid_for_claim"])}

## Phi-perp Boundary Audit

{md_table(phi_rows, ["phi_id", "quantity", "formula", "zero_condition", "status", "valid_for_claim"])}

## Vperp Feedback To 3230

{md_table(feedback_rows, ["feedback_id", "feeds", "substitution", "result", "claim_status", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3231_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3231_JPERP_SOURCE_SILENCE_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3231_JPERP_FINITE_BOUND_FORMULA.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3231_PHI_PERP_BOUNDARY_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3231_VPERP_FEEDBACK_TO_3230.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3231_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3231_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, source_rows, bound_rows, phi_rows, feedback_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (SOURCE_AUDIT, source_rows),
        (BOUND_FORMULA, bound_rows),
        (PHI_AUDIT, phi_rows),
        (VPERP_FEEDBACK, feedback_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, source_rows, bound_rows, phi_rows, feedback_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, source_rows, bound_rows, phi_rows, feedback_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()

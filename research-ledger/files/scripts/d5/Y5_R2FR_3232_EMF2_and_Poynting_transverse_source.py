from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3232-Y5-R2FR-EMF2-and-Poynting-transverse-source-zero-or-bound-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3232_INPUTS.csv"
EMF2_AUDIT = OUT / "P8_Y5_R2FR_3232_EMF2_ZERO_OR_BOUND_AUDIT.csv"
POYNTING_AUDIT = OUT / "P8_Y5_R2FR_3232_POYNTING_FLUX_ZERO_OR_BOUND_AUDIT.csv"
UPDATE = OUT / "P8_Y5_R2FR_3232_JPERP_PHI_BOUND_UPDATE.csv"
GATES = OUT / "P8_Y5_R2FR_3232_CLAIM_GATES.csv"
DECISION = OUT / "P8_Y5_R2FR_3232_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3232_VALIDATION.csv"


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
        "input_id": "SRC3232_00_3231_doc",
        "location": "post_checkpoint",
        "relative_path": "3231-Y5-R2FR-transverse-source-channel-silence-or-bound-for-Jperp-under-AX1090.md",
        "role": "3231 handoff selecting EM_F2 and Poynting",
        "terms": ["J_EM_F2", "Phi_Poynting", "F^2=0", "3232"],
    },
    {
        "input_id": "SRC3232_01_3231_source_audit",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3231_JPERP_SOURCE_SILENCE_AUDIT.csv",
        "role": "machine J_perp source audit",
        "terms": ["JPA3231_3_EM_F2", "JPA3231_4_Poynting"],
    },
    {
        "input_id": "SRC3232_02_3231_phi",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3231_PHI_PERP_BOUNDARY_AUDIT.csv",
        "role": "machine Phi_perp/Poynting boundary audit",
        "terms": ["PHI3231_1_Poynting_boundary", "Phi_Poynting"],
    },
    {
        "input_id": "SRC3232_03_3220_doc",
        "location": "post_checkpoint",
        "relative_path": "3220-Y5-R2FR-parent-source-root-for-EM-F2-or-finite-double-zero-coefficient-input-under-AX1090.md",
        "role": "EM F2 source-root and Poynting stress guard",
        "terms": ["EM_F2_SOURCE_ROOT_NOT_PARENT_SIGNED", "F_Q^2=0", "Poynting", "F_EM"],
    },
    {
        "input_id": "SRC3232_04_3220_transfer",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3220_GENERIC_DZ_TO_EM_F2_TRANSFER_AUDIT.csv",
        "role": "machine generic double-zero transfer warning",
        "terms": ["TR3220_0_conditional_transfer_theorem", "TR3220_3_null_wave_not_F2_proof"],
    },
    {
        "input_id": "SRC3232_05_3220_finite",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3220_FINITE_DZ_INPUT_REQUIREMENTS.csv",
        "role": "machine finite EM F2/Poynting requirements",
        "terms": ["FIN3220_4_FQ2_norm", "FIN3220_7_Poynting_stress_bound"],
    },
    {
        "input_id": "SRC3232_06_3218_doc",
        "location": "post_checkpoint",
        "relative_path": "3218-Y5-R2FR-EM-F2-vertex-owner-for-memory-slope-zero-or-balpha-m-source-row-under-AX1090.md",
        "role": "EM F2 vertex owner and readout countermodels",
        "terms": ["no-extra-F2", "readout", "f_m", "Z_A"],
    },
    {
        "input_id": "SRC3232_07_3219_doc",
        "location": "post_checkpoint",
        "relative_path": "3219-Y5-R2FR-EM-F2-strict-double-zero-source-root-or-balpha-m-finite-bound-under-AX1090.md",
        "role": "strict double-zero EM F2 theorem and Hessian guard",
        "terms": ["F^2=0", "Poynting", "strict double-zero", "eta_EM"],
    },
    {
        "input_id": "SRC3232_08_3210_source_split",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3210_SOURCE_CHANNEL_SPLIT_WITH_EM_POYNTING.csv",
        "role": "source split with EM trace/F2/Poynting separation",
        "terms": ["JXS3210_2_EM_F2", "JXS3210_3_Poynting_flux"],
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

    emf2_rows = [
        {
            "audit_id": "EF3232_0_definition",
            "channel": "transverse EM_F2 source",
            "formula": "J_EM_F2 = (1/4) f_perp_prime(0) F_{mu nu}F^{mu nu}",
            "zero_route": "f_perp_prime(0)=0 or F^2 support vanishes in the scored region",
            "finite_route": "||J_EM_F2||_2 <= (1/4)|f_perp_prime(0)| ||F^2||_2",
            "status": "EXACT_FORMULA_STAGED",
            "claim_gap": "f_perp_prime(0) and ||F^2|| support not source-backed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "EF3232_1_no_extra_F2",
            "channel": "operator-domain exclusion",
            "formula": "no independent f_perp(X_perp)F_Q^2 term in the parent visible operator domain",
            "zero_route": "absence of the operator gives f_perp_prime(0)=0",
            "finite_route": "if absent cannot be proven, retain C_F2_perp:=|f_perp_prime(0)|",
            "status": "ZERO_ROUTE_NOT_PARENT_SIGNED",
            "claim_gap": "operator-domain exhaustion/no-hidden-visible theorem missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "EF3232_2_strict_source_root",
            "channel": "same-branch EM source-root",
            "formula": "f_perp=lambda_F F_EM(X_perp), F_EM(0)=F_EM_prime(0)=0",
            "zero_route": "strict double-zero kills f_perp_prime(0)",
            "finite_route": "off-root source <= (1/4)|lambda_F F_EM_second| |X_perp| ||F^2||_2 + higher order",
            "status": "CONDITIONAL_THEOREM_NOT_EM_ATTACHED",
            "claim_gap": "3231 transverse branch not proven to be the same EM source-root branch",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "EF3232_3_readout_reentry",
            "channel": "observed alpha/readout",
            "formula": "alpha_eff can reintroduce transverse dependence after bare F2 silence",
            "zero_route": "effective/readout functor preserves no-extra-F2 or strict source-root rule",
            "finite_route": "add J_readout_F2_bound to the transverse source norm",
            "status": "REQUIRED_GUARD_UNSIGNED",
            "claim_gap": "readout/radiative closure missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "EF3232_4_null_F2_support",
            "channel": "null-wave scalar invariant",
            "formula": "F^2=0 for ideal null radiation can make J_EM_F2 vanish in that support",
            "zero_route": "scored region contains only such null F2 support and no readout/boundary reentry",
            "finite_route": "retain ||F^2||_2 for non-null/static/material/Coulomb fields",
            "status": "SUPPORT_SPECIFIC_NOT_GENERAL",
            "claim_gap": "does not address Poynting/stress/boundary flux",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    poynting_rows = [
        {
            "audit_id": "PY3232_0_definition",
            "channel": "Poynting/collar/worldtube flux",
            "formula": "Phi_Poynting <= C_flux ||S_EM . n||_B, equivalently a stress flux norm built from T_EM^{mu nu} n_mu",
            "zero_route": "no EM flux through boundary/collar/worldtube, or flux form is exact/proper/orthogonal to v_perp",
            "finite_route": "Phi_Poynting_bound := C_flux ||S_EM . n||_B",
            "status": "EXACT_BOUND_TEMPLATE",
            "claim_gap": "C_flux, boundary norm, and flux support not source-backed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "PY3232_1_F2_nonimplication",
            "channel": "F2 versus stress",
            "formula": "F^2=0 does not imply T_EM^{mu nu}=0 or S_EM=0",
            "zero_route": "must separately prove stress/flux silence",
            "finite_route": "retain Poynting/stress norm even when scalar F2 channel is zero",
            "status": "SEPARATE_CHANNEL_GUARD",
            "claim_gap": "blocks replacing Poynting by F2",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "PY3232_2_proper_boundary",
            "channel": "proper/exact boundary flux",
            "formula": "integral_B i_vperp dB_EM or exact/proper corner term vanishes on closed compatible boundary",
            "zero_route": "flux contribution is exact/proper/orthogonal and no corner/worldtube leakage remains",
            "finite_route": "corner/worldtube remainder norm B_corner_flux",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "claim_gap": "boundary/collar class and corner exclusions not parent-signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "PY3232_3_no_flux_support",
            "channel": "support silence",
            "formula": "S_EM . n = 0 on the selected boundary/collar/worldtube",
            "zero_route": "boundary chosen or derived so physical flux through it is zero",
            "finite_route": "if flux is nonzero, bound by measured/sourced field flux support",
            "status": "SUPPORT_ROUTE_NOT_SOURCE_SIGNED",
            "claim_gap": "cannot choose boundary after the fact; must be parent/test-domain owned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    update_rows = [
        {
            "update_id": "UP3232_0_Jperp_update",
            "target": "||J_perp^tau||_2",
            "formula": "||J_perp^tau||_2 <= J_other_bound + (1/4)C_F2_perp ||F^2||_2 + J_Poynting_bound",
            "definitions": "C_F2_perp:=|f_perp_prime(0)|; J_other_bound collects geom/matter/trace/memory/projector channels",
            "zero_condition": "J_other_bound=0, C_F2_perp||F^2||_2=0, and J_Poynting_bound=0",
            "status": "REFINED_BOUND_FOR_3231",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "update_id": "UP3232_1_Phi_update",
            "target": "|Phi_perp^tau|",
            "formula": "|Phi_perp^tau| <= Phi_other_bound + Phi_EM_F2_boundary + C_flux ||S_EM . n||_B",
            "definitions": "Phi_other_bound collects non-EM boundary/corner/worldtube terms",
            "zero_condition": "all boundary terms exact/proper/orthogonal/absent and EM flux support zero",
            "status": "REFINED_BOUND_FOR_3231",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "update_id": "UP3232_2_Yperp_update",
            "target": "Y_perp",
            "formula": "Y_perp <= (J_perp_bound/m_perp_min + sqrt((J_perp_bound/m_perp_min)^2 + 4 Phi_perp_bound))/2",
            "definitions": "J_perp_bound and Phi_perp_bound include the 3232 EM_F2/Poynting terms",
            "zero_condition": "Y_perp=0 if both refined source and boundary bounds are zero with coercivity/no kernel",
            "status": "FEEDS_3230_AND_3229",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    gate_rows = [
        {
            "gate_id": "G3232_0_EMF2_zero",
            "gate": "kill transverse EM_F2 channel",
            "required_evidence": "no-extra-F2 operator-domain theorem OR same-branch strict EM source-root OR support-specific F2=0 with readout closure",
            "current_status": "NOT_PARENT_SIGNED",
            "fallback": "use (1/4)C_F2_perp||F^2||_2 in J_perp_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3232_1_Poynting_zero",
            "gate": "kill Poynting/boundary channel",
            "required_evidence": "no flux through owned boundary/collar/worldtube OR exact/proper/orthogonal flux theorem",
            "current_status": "NOT_PARENT_SIGNED",
            "fallback": "use C_flux||S_EM.n||_B in Phi_perp_bound/J_Poynting_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3232_2_no_trace_shortcut",
            "gate": "prevent false closure",
            "required_evidence": "do not use Maxwell trace silence or F2=0 to erase Poynting/stress",
            "current_status": "ACTIVE_GUARD",
            "fallback": "separate scalar invariant and stress/flux norms",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3232_3_vperp_zero_feedback",
            "gate": "v_perp=0 promotion",
            "required_evidence": "EM_F2 zero, Poynting zero, plus other J_perp/Phi channels zero and O_perp coercive/no-kernel",
            "current_status": "NOT_CLAIM_READY",
            "fallback": "finite Y_perp bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3232_0_result",
            "decision": "EMF2_AND_POYNTING_ZERO_OR_BOUND_FORMULAS_DERIVED_NO_CHANNEL_CLOSED",
            "because": "the exact EM_F2 zero routes and Poynting zero routes are now explicit, but current sources do not parent-sign no-extra-F2/source-root/readout closure or Poynting boundary silence",
            "claim_status": "NO_ALPHA_NO_CLOCK_NO_WEP_NO_R10_NO_LOCAL_GR_NO_MAXWELL_STRESS_CLAIM",
            "next_action": "try to close EM_F2 first via no-extra-F2/source-root/readout owner; keep Poynting as separate finite stress/flux channel unless boundary silence is signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3232_1_next_target",
            "decision": "3233-Y5-R2FR-no-extra-F2-or-source-root-owner-for-transverse-EMF2-under-AX1090",
            "because": "EM_F2 is the cleaner algebraic channel; if f_perp_prime(0) is killed, the remaining live channel is Poynting/boundary flux and other non-EM sources",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "derive whether transverse f_perp_prime(0)=0 follows from Q_ONLY/no-hidden-visible operator domain, strict source-root, or readout closure",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, emf2_rows, poynting_rows, update_rows, gate_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    emf2_rows: list[dict[str, object]],
    poynting_rows: list[dict[str, object]],
    update_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, EMF2_AUDIT, POYNTING_AUDIT, UPDATE, GATES, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    emf2_bound = any(row["audit_id"] == "EF3232_0_definition" and "||J_EM_F2||_2" in row["finite_route"] for row in emf2_rows)
    poynting_guard = any(row["audit_id"] == "PY3232_1_F2_nonimplication" for row in poynting_rows)
    update_present = any(row["update_id"] == "UP3232_2_Yperp_update" for row in update_rows)
    next_target = decision_rows[-1]["decision"].startswith("3233-")
    claim_true_count = 0
    for rows in [input_rows, emf2_rows, poynting_rows, update_rows, gate_rows, decision_rows]:
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
        {"check_id": "VAL3232_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3232_01_emf2_bound_formula", "pass": b(emf2_bound), "detail": "EM_F2 zero routes and finite bound staged", "generated_utc": now},
        {"check_id": "VAL3232_02_poynting_guard", "pass": b(poynting_guard), "detail": "F2 nonimplication guard retained", "generated_utc": now},
        {"check_id": "VAL3232_03_yperp_feedback", "pass": b(update_present), "detail": "bounds feed J/Phi/Y_perp chain", "generated_utc": now},
        {"check_id": "VAL3232_04_claims_blocked", "pass": b(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3232_05_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3232_06_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3232_07_next_target", "pass": b(next_target), "detail": str(decision_rows[-1]["decision"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    emf2_rows: list[dict[str, object]],
    poynting_rows: list[dict[str, object]],
    update_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3232 - EMF2 and Poynting Transverse Source Zero Or Bound under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, Maxwell-stress claim, or public-facing result.

## Result

3232 attacks the two live electromagnetic channels from 3231.

The transverse scalar EM kinetic source is:

```text
J_EM_F2 = (1/4) f_perp_prime(0) F_mu_nu F^mu_nu.
```

Therefore:

```text
||J_EM_F2||_2 <= (1/4) |f_perp_prime(0)| ||F^2||_2.
```

It is zero only if one of these is actually parent-signed:

```text
f_perp_prime(0)=0
```

from no-extra-F2/operator-domain exclusion, same-branch strict EM source-root, or a support-specific `F^2=0` result with no readout reentry.

The Poynting/boundary channel is separate:

```text
Phi_Poynting <= C_flux ||S_EM . n||_B.
```

and

```text
F^2=0 does not imply S_EM=0 or T_EM^mu_nu=0.
```

So the refined transverse source/boundary update is:

```text
||J_perp^tau||_2
<= J_other_bound + (1/4) C_F2_perp ||F^2||_2 + J_Poynting_bound,

|Phi_perp^tau|
<= Phi_other_bound + Phi_EM_F2_boundary + C_flux ||S_EM . n||_B.
```

where `C_F2_perp:=|f_perp_prime(0)|`.

This feeds directly back into:

```text
Y_perp <= (J_perp_bound/m_perp_min
          + sqrt((J_perp_bound/m_perp_min)^2 + 4 Phi_perp_bound))/2.
```

Current verdict: `EMF2_AND_POYNTING_ZERO_OR_BOUND_FORMULAS_DERIVED_NO_CHANNEL_CLOSED`.

## EMF2 Zero Or Bound Audit

{md_table(emf2_rows, ["audit_id", "channel", "formula", "zero_route", "finite_route", "status", "claim_gap", "valid_for_claim"])}

## Poynting Flux Zero Or Bound Audit

{md_table(poynting_rows, ["audit_id", "channel", "formula", "zero_route", "finite_route", "status", "claim_gap", "valid_for_claim"])}

## Jperp Phi Bound Update

{md_table(update_rows, ["update_id", "target", "formula", "definitions", "zero_condition", "status", "valid_for_claim"])}

## Claim Gates

{md_table(gate_rows, ["gate_id", "gate", "required_evidence", "current_status", "fallback", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3232_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3232_EMF2_ZERO_OR_BOUND_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3232_POYNTING_FLUX_ZERO_OR_BOUND_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3232_JPERP_PHI_BOUND_UPDATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3232_CLAIM_GATES.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3232_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3232_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, emf2_rows, poynting_rows, update_rows, gate_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (EMF2_AUDIT, emf2_rows),
        (POYNTING_AUDIT, poynting_rows),
        (UPDATE, update_rows),
        (GATES, gate_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, emf2_rows, poynting_rows, update_rows, gate_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, emf2_rows, poynting_rows, update_rows, gate_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()

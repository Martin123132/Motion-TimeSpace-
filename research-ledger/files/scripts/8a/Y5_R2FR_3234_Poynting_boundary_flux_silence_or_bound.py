from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3234_INPUTS.csv"
FUNCTIONAL = OUT / "P8_Y5_R2FR_3234_POYNTING_FLUX_FUNCTIONAL.csv"
SILENCE = OUT / "P8_Y5_R2FR_3234_BOUNDARY_SILENCE_AUDIT.csv"
FINITE = OUT / "P8_Y5_R2FR_3234_FINITE_FLUX_BOUND.csv"
UPDATE = OUT / "P8_Y5_R2FR_3234_JPERP_PHI_UPDATE.csv"
DECISION = OUT / "P8_Y5_R2FR_3234_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3234_VALIDATION.csv"


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
        "input_id": "SRC3234_00_3233_doc",
        "location": "post_checkpoint",
        "relative_path": "3233-Y5-R2FR-no-extra-F2-or-source-root-owner-for-transverse-EMF2-under-AX1090.md",
        "role": "3233 handoff selecting Poynting flux channel",
        "terms": ["Poynting", "3234", "C_flux", "S_EM"],
    },
    {
        "input_id": "SRC3234_01_3232_doc",
        "location": "post_checkpoint",
        "relative_path": "3232-Y5-R2FR-EMF2-and-Poynting-transverse-source-zero-or-bound-under-AX1090.md",
        "role": "3232 exact Poynting/stress nonimplication guard",
        "terms": ["Phi_Poynting", "F^2=0", "T_EM", "C_flux"],
    },
    {
        "input_id": "SRC3234_02_3232_poynting",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3232_POYNTING_FLUX_ZERO_OR_BOUND_AUDIT.csv",
        "role": "machine Poynting zero-or-bound audit",
        "terms": ["PY3232_0_definition", "PY3232_1_F2_nonimplication", "PY3232_2_proper_boundary"],
    },
    {
        "input_id": "SRC3234_03_3232_update",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3232_JPERP_PHI_BOUND_UPDATE.csv",
        "role": "machine J_perp/Phi update carrying Poynting term",
        "terms": ["UP3232_0_Jperp_update", "UP3232_1_Phi_update", "UP3232_2_Yperp_update"],
    },
    {
        "input_id": "SRC3234_04_3231_source",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3231_JPERP_SOURCE_SILENCE_AUDIT.csv",
        "role": "machine transverse source split with Poynting",
        "terms": ["JPA3231_4_Poynting", "S_EM", "boundary", "worldtube"],
    },
    {
        "input_id": "SRC3234_05_3231_phi",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3231_PHI_PERP_BOUNDARY_AUDIT.csv",
        "role": "machine Phi_perp boundary audit",
        "terms": ["PHI3231_1_Poynting_boundary", "Phi_Poynting", "C_flux"],
    },
    {
        "input_id": "SRC3234_06_3220_finite",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3220_FINITE_DZ_INPUT_REQUIREMENTS.csv",
        "role": "finite EM stress/Poynting requirement",
        "terms": ["FIN3220_7_Poynting_stress_bound", "stress", "Poynting"],
    },
    {
        "input_id": "SRC3234_07_3210_split",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3210_SOURCE_CHANNEL_SPLIT_WITH_EM_POYNTING.csv",
        "role": "source-channel split separating F2 and Poynting",
        "terms": ["JXS3210_3_Poynting_flux", "F^2=0", "T_EM"],
    },
    {
        "input_id": "SRC3234_08_2600_boundary",
        "location": "post_checkpoint",
        "relative_path": "2600-Y5-R2FR-Tobs-delta-tau-norm-owner-or-boundary-clock-action-clause.md",
        "role": "boundary/action ownership precedent for flux accounting",
        "terms": ["boundary flux accounting", "boundary-clock action", "common norm", "A_ext"],
    },
    {
        "input_id": "SRC3234_09_3136_clock_owner",
        "location": "post_checkpoint",
        "relative_path": "3136-Y5-R2FR-observed-coframe-clock-functional-owner-under-AX1090.md",
        "role": "observed coframe/descent precedent for owned boundary time",
        "terms": ["observed coframe", "boundary", "same tau", "parent ownership"],
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

    functional_rows = [
        {
            "functional_id": "PF3234_0_functional",
            "object": "Poynting boundary/collar/worldtube flux functional",
            "formula": "Phi_Poynting[v_perp] := int_B w_perp T_EM(u,n) dSigma ~= int_B w_perp (S_EM dot n) dSigma",
            "meaning": "transverse variation tests the EM stress/energy flux through the owned boundary, collar, or worldtube",
            "zero_condition": "T_EM(u,n)=0 or S_EM dot n=0 on the selected owned support, or w_perp is orthogonal to the flux source",
            "finite_bound": "|Phi_Poynting[v_perp]| <= ||w_perp||_{B*} ||S_EM dot n||_B + B_corner_flux",
            "status": "FUNCTIONAL_DERIVED_AS_DUAL_PAIRING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "functional_id": "PF3234_1_stress_form",
            "object": "stress tensor equivalent",
            "formula": "S_EM dot n = T_EM(u,n) after choosing observed frame u and boundary normal n",
            "meaning": "keeps the channel covariant; Poynting is the frame expression of the Maxwell stress flux",
            "zero_condition": "observed frame/boundary normal and stress tensor descent make T_EM(u,n) vanish",
            "finite_bound": "C_flux := ||w_perp||_{B*}; flux_norm := ||T_EM(u,n)||_B",
            "status": "COVARIANT_REWRITE_READY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "functional_id": "PF3234_2_collar_bulk",
            "object": "collar leakage source",
            "formula": "J_Poynting_bound <= C_coll ||T_EM(u,n)||_collar",
            "meaning": "if flux is represented as a collar/worldtube source rather than a pure boundary term, it still enters only through a finite stress norm",
            "zero_condition": "collar support is flux-free or the flux form is exact/proper with no corner remainder",
            "finite_bound": "C_coll ||T_EM(u,n)||_collar",
            "status": "FINITE_COLLAR_BOUND_TEMPLATE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "functional_id": "PF3234_3_F2_guard",
            "object": "F2 shortcut guard",
            "formula": "F_mu_nu F^mu_nu=0 does not imply T_EM(u,n)=0 or S_EM dot n=0",
            "meaning": "null radiation can have vanishing scalar invariant and nonzero energy flux",
            "zero_condition": "none; must separately prove stress/flux silence",
            "finite_bound": "retain C_flux ||S_EM dot n||_B even if ||F^2||_2=0",
            "status": "NO_F2_SHORTCUT_ACTIVE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    silence_rows = [
        {
            "route_id": "PZ3234_0_no_flux_support",
            "route": "support silence",
            "theorem": "If S_EM dot n=0 on the parent-owned boundary/collar/worldtube, then Phi_Poynting=0 on that support.",
            "required_parent_signature": "owned boundary B/collar/worldtube; observed u,n; support proof; no hidden corner leakage",
            "current_status": "NOT_PARENT_SIGNED",
            "residual_if_unsigned": "C_flux ||S_EM dot n||_B",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "route_id": "PZ3234_1_exact_proper_flux",
            "route": "exact/proper boundary",
            "theorem": "If the transverse flux contribution is an exact/proper boundary form on a closed compatible boundary, its integral vanishes up to corners.",
            "required_parent_signature": "flux potential; compatible closed boundary; orientation; corner/worldtube exclusion",
            "current_status": "CORNER_AND_BOUNDARY_CLASS_UNSIGNED",
            "residual_if_unsigned": "B_corner_flux + B_worldtube_leak",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "route_id": "PZ3234_2_orthogonality",
            "route": "transverse test-function orthogonality",
            "theorem": "If w_perp lies in the annihilator of the EM flux functional, then Phi_Poynting[v_perp]=0.",
            "required_parent_signature": "definition of allowed v_perp space; boundary dual norm; projector theorem P_perp^* flux=0",
            "current_status": "PROJECTOR_ORTHOGONALITY_UNSIGNED",
            "residual_if_unsigned": "||P_perp^* T_EM(u,n)||_B",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "route_id": "PZ3234_3_parent_stress_descent",
            "route": "EM stress descends only to Maxwell/metric sector",
            "theorem": "If the parent action proves Maxwell stress/Hodge/current descent is quotient-invariant and has no transverse scalar representative coefficient, Poynting cannot source v_perp.",
            "required_parent_signature": "quotient-invariant Hodge star; Maxwell current/stress descent; no representative Weyl/disformal coefficient",
            "current_status": "DESCENT_NOT_FULLY_SIGNED",
            "residual_if_unsigned": "C_stress_leak ||T_EM||_B",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "route_id": "PZ3234_4_total",
            "route": "total Poynting zero",
            "theorem": "Poynting channel closes only if no-flux support, exact/proper cancellation, orthogonality, or parent stress descent closes on the same branch.",
            "required_parent_signature": "one complete route plus owned common norm and boundary class",
            "current_status": "FAIL_CURRENT_CLAIM",
            "residual_if_unsigned": "Phi_Poynting_bound and J_Poynting_bound remain in the local residual vector",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "route_id": "PZ3234_5_no_F2_shortcut",
            "route": "reject scalar-invariant shortcut",
            "theorem": "F^2=0 may erase the EM_F2 scalar source on null support but does not erase Poynting, T_EM, or boundary flux.",
            "required_parent_signature": "separate stress/flux proof",
            "current_status": "ACTIVE_GUARD",
            "residual_if_unsigned": "C_flux ||S_EM dot n||_B remains even with ||F^2||_2=0",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    finite_rows = [
        {
            "bound_id": "PB3234_0_boundary_flux",
            "quantity": "Phi_Poynting_bound",
            "formula": "Phi_Poynting_bound := C_flux ||S_EM dot n||_B + B_corner_flux",
            "required_inputs": "C_flux; boundary/collar/worldtube B; observed u,n; flux norm; corner/worldtube remainder; units",
            "status": "FINITE_BOUND_FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "PB3234_1_collar_source",
            "quantity": "J_Poynting_bound",
            "formula": "J_Poynting_bound := C_coll ||T_EM(u,n)||_collar",
            "required_inputs": "C_coll; collar support; stress-flux norm; projector norm; units",
            "status": "FINITE_BOUND_FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "PB3234_2_total_phi",
            "quantity": "Phi_perp_bound update",
            "formula": "|Phi_perp^tau| <= Phi_other_bound + Phi_EM_F2_boundary + C_flux ||S_EM dot n||_B + B_corner_flux",
            "required_inputs": "Phi_other_bound; Phi_EM_F2_boundary; C_flux; flux norm; corner flux",
            "status": "FEEDS_LOCAL_RESIDUAL_VECTOR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "PB3234_3_total_jperp",
            "quantity": "J_perp_bound update",
            "formula": "||J_perp^tau||_2 <= J_other_bound + (1/4) C_F2_perp ||F^2||_2 + C_coll ||T_EM(u,n)||_collar",
            "required_inputs": "J_other_bound; C_F2_perp; F2 norm; C_coll; collar stress flux norm",
            "status": "FEEDS_TRANSVERSE_AMPLITUDE_LAW",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    update_rows = [
        {
            "update_id": "UP3234_0_residual_vector",
            "target": "local residual vector",
            "formula": "R_local includes R_EM_F2 + R_Poynting + R_other; R_Poynting is bounded by PB3234_0/PB3234_1",
            "claim_effect": "keeps EM flux as a finite residual rather than erasing it by trace/F2 silence",
            "status": "RESIDUAL_COMPONENT_EXPLICIT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "update_id": "UP3234_1_Yperp_feedback",
            "target": "transverse amplitude law",
            "formula": "Y_perp <= (a_perp + sqrt(a_perp^2+4 b_perp))/2 with a_perp=J_perp_bound/m_perp_min and b_perp=Phi_perp_bound",
            "claim_effect": "local PPN branch cannot claim v_perp=0 unless both EM_F2 and Poynting terms vanish or are bounded below tolerance",
            "status": "FEEDS_3230_CHAIN",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "update_id": "UP3234_2_flux_gate",
            "target": "future source rows",
            "formula": "required row: {B_id,u,n,C_flux,||S_EM dot n||_B,B_corner_flux,units,source_path,valid_for_claim}",
            "claim_effect": "turns Poynting into a sourceable coefficient instead of a vague objection",
            "status": "SOURCE_ROW_CONTRACT_READY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3234_0_result",
            "decision": "POYNTING_FLUX_FUNCTIONAL_AND_FINITE_BOUND_DERIVED_NO_ZERO_CLAIM",
            "because": "Poynting is now a dual boundary/collar flux functional with exact zero routes and finite bounds, but no route is parent-signed on an owned boundary class",
            "claim_status": "NO_LOCAL_GR_NO_MAXWELL_STRESS_NO_CLOCK_NO_PPN_NO_R10_CLAIM",
            "next_action": "keep Phi_Poynting/J_Poynting in the local residual vector unless a source-backed flux row or parent stress-descent theorem is supplied",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3234_1_next_target",
            "decision": "3235-Y5-R2FR-matter-marker-source-functor-silence-or-bound-for-Jperp-under-AX1090",
            "because": "after EM_F2 and Poynting are explicit, the remaining live J_perp channels are ordinary matter/marker/readout, memory/projector, and geometry; matter-source functor is the next lowest-scrutiny gate",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "derive whether ordinary matter/source markers descend only through the observed coframe/metric sector or produce a finite transverse source coefficient",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, functional_rows, silence_rows, finite_rows, update_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    functional_rows: list[dict[str, object]],
    silence_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    update_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, FUNCTIONAL, SILENCE, FINITE, UPDATE, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    functional_present = any(row["functional_id"] == "PF3234_0_functional" for row in functional_rows)
    f2_guard = any(row["route_id"] == "PZ3234_5_no_F2_shortcut" for row in silence_rows)
    total_zero_route = any(row["route_id"] == "PZ3234_4_total" for row in silence_rows)
    finite_bound = any(row["bound_id"] == "PB3234_2_total_phi" for row in finite_rows)
    residual_update = any(row["update_id"] == "UP3234_0_residual_vector" for row in update_rows)
    next_target = decision_rows[-1]["decision"].startswith("3235-")
    claim_true_count = 0
    for rows in [input_rows, functional_rows, silence_rows, finite_rows, update_rows, decision_rows]:
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
        {"check_id": "VAL3234_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3234_01_functional", "pass": b(functional_present), "detail": "Poynting dual flux functional present", "generated_utc": now},
        {"check_id": "VAL3234_02_f2_guard", "pass": b(f2_guard), "detail": "F2 shortcut explicitly blocked", "generated_utc": now},
        {"check_id": "VAL3234_03_total_zero_route", "pass": b(total_zero_route), "detail": "total zero route specified but not activated", "generated_utc": now},
        {"check_id": "VAL3234_04_finite_bound", "pass": b(finite_bound), "detail": "Phi/J finite flux bounds present", "generated_utc": now},
        {"check_id": "VAL3234_05_residual_update", "pass": b(residual_update), "detail": "local residual vector update present", "generated_utc": now},
        {"check_id": "VAL3234_06_claims_blocked", "pass": b(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3234_07_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3234_08_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3234_09_next_target", "pass": b(next_target), "detail": str(decision_rows[-1]["decision"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    functional_rows: list[dict[str, object]],
    silence_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    update_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3234 - Poynting Boundary Flux Silence Or Finite Bound under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, PPN pass, EM-lock claim, Maxwell-stress claim, or public-facing result.

## Result

3234 turns the Poynting objection into a concrete local residual component instead of letting it float as a vague danger channel.

The flux functional is:

```text
Phi_Poynting[v_perp]
:= int_B w_perp T_EM(u,n) dSigma
 ~= int_B w_perp (S_EM dot n) dSigma.
```

By the dual norm bound:

```text
|Phi_Poynting[v_perp]|
<= ||w_perp||_{{B*}} ||S_EM dot n||_B + B_corner_flux
:= C_flux ||S_EM dot n||_B + B_corner_flux.
```

If the same channel is represented as collar/worldtube bulk leakage:

```text
J_Poynting_bound <= C_coll ||T_EM(u,n)||_collar.
```

Exact zero is allowed only by one of four owned routes:

```text
S_EM dot n = 0 on the owned support,
or the flux form is exact/proper with no corner leakage,
or the transverse test direction is orthogonal to the flux functional,
or Maxwell stress/current/Hodge descent proves no transverse source.
```

The important guard is retained:

```text
F^2=0 does not imply S_EM dot n=0 or T_EM(u,n)=0.
```

So null-wave scalar-invariant silence cannot be used to erase Poynting/boundary stress.

Current verdict: `POYNTING_FLUX_FUNCTIONAL_AND_FINITE_BOUND_DERIVED_NO_ZERO_CLAIM`.

## Poynting Flux Functional

{md_table(functional_rows, ["functional_id", "object", "formula", "meaning", "zero_condition", "finite_bound", "status", "valid_for_claim"])}

## Boundary Silence Audit

{md_table(silence_rows, ["route_id", "route", "theorem", "required_parent_signature", "current_status", "residual_if_unsigned", "valid_for_claim"])}

## Finite Flux Bound

{md_table(finite_rows, ["bound_id", "quantity", "formula", "required_inputs", "status", "valid_for_claim"])}

## Jperp/Phi Update

{md_table(update_rows, ["update_id", "target", "formula", "claim_effect", "status", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3234_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3234_POYNTING_FLUX_FUNCTIONAL.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3234_BOUNDARY_SILENCE_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3234_FINITE_FLUX_BOUND.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3234_JPERP_PHI_UPDATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3234_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3234_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, functional_rows, silence_rows, finite_rows, update_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (FUNCTIONAL, functional_rows),
        (SILENCE, silence_rows),
        (FINITE, finite_rows),
        (UPDATE, update_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, functional_rows, silence_rows, finite_rows, update_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, functional_rows, silence_rows, finite_rows, update_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()

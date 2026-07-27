from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3235-Y5-R2FR-matter-marker-source-functor-silence-or-bound-for-Jperp-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3235_INPUTS.csv"
DERIVATION = OUT / "P8_Y5_R2FR_3235_MATTER_SOURCE_FUNCTOR_DERIVATION.csv"
NO_MARKER = OUT / "P8_Y5_R2FR_3235_NO_MARKER_SOURCE_FUNCTOR_GATE.csv"
BOUND = OUT / "P8_Y5_R2FR_3235_JMATTER_COMPONENT_BOUND.csv"
UPDATE = OUT / "P8_Y5_R2FR_3235_JPERP_UPDATE.csv"
DECISION = OUT / "P8_Y5_R2FR_3235_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3235_VALIDATION.csv"


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
        "input_id": "SRC3235_00_3234_doc",
        "location": "post_checkpoint",
        "relative_path": "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md",
        "role": "3234 handoff selecting matter/source functor next",
        "terms": ["3235", "matter-marker", "source-functor", "J_perp"],
    },
    {
        "input_id": "SRC3235_01_3231_doc",
        "location": "post_checkpoint",
        "relative_path": "3231-Y5-R2FR-transverse-source-channel-silence-or-bound-for-Jperp-under-AX1090.md",
        "role": "J_perp source split containing matter marker channel",
        "terms": ["J_matter", "matter/readout/material markers", "MISSING_NO_MARKER_THEOREM", "J_perp"],
    },
    {
        "input_id": "SRC3235_02_3231_source_csv",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3231_JPERP_SOURCE_SILENCE_AUDIT.csv",
        "role": "machine J_perp source-channel row",
        "terms": ["JPA3231_5_matter_marker", "Lie_vperp S_matter", "readout-marker"],
    },
    {
        "input_id": "SRC3235_03_1044_doc",
        "location": "post_checkpoint",
        "relative_path": "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md",
        "role": "exact matter-pullback chain rule reused for R2FR transverse branch",
        "terms": ["chain-rule", "qbar_XT=0", "J_matter=0", "component envelope"],
    },
    {
        "input_id": "SRC3235_04_1044_derivation",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv",
        "role": "machine matter-pullback derivation",
        "terms": ["MPD1044_1_chain_rule_identity", "MPD1044_7_exact_theorem_if_signed", "MPD1044_8_current_verdict"],
    },
    {
        "input_id": "SRC3235_05_1044_components",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv",
        "role": "machine no-cancellation qbar component envelope",
        "terms": ["QBC1044_0_qbar_geom", "QBC1044_5_total_abs_guard", "qbar_marker"],
    },
    {
        "input_id": "SRC3235_06_3136_clock_owner",
        "location": "post_checkpoint",
        "relative_path": "3136-Y5-R2FR-observed-coframe-clock-functional-owner-under-AX1090.md",
        "role": "observed-coframe matter functor precedent",
        "terms": ["ordinary clock matter descends", "observed coframe", "matter functor", "Residuals"],
    },
    {
        "input_id": "SRC3235_07_3096_no_marker",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3096_NO_MARKER_THEOREM_ATTEMPT.csv",
        "role": "latest R2FR no-marker theorem attempt",
        "terms": ["NMT3096_6_verdict", "co-moving material marker", "constant_superselection"],
    },
    {
        "input_id": "SRC3235_08_2979_source_covector",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_2979_NO_MARKER_SOURCE_COVECTOR_THEOREM_ATTEMPT.csv",
        "role": "source-covector theorem and countermodel",
        "terms": ["NMC2979_3_countermodel", "relative source-weight", "NMC2979_8_verdict"],
    },
    {
        "input_id": "SRC3235_09_2958_bmarker",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_2958_BMARKER_NO_MARKER_THEOREM_GATE.csv",
        "role": "b_marker no-marker gate",
        "terms": ["BMARK2958_0_definition", "BMARK2958_5_verdict", "source/preparation marker"],
    },
    {
        "input_id": "SRC3235_10_3210_source_split",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3210_SOURCE_CHANNEL_SPLIT_WITH_EM_POYNTING.csv",
        "role": "source split with ordinary matter/material constants",
        "terms": ["JXS3210_4_matter_marker", "ordinary matter", "no-marker"],
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

    derivation_rows = [
        {
            "derivation_id": "MSF3235_0_target",
            "object": "transverse ordinary-matter source",
            "formula": "J_matter := local projection of delta_{v_perp} S_matter plus marker/readout/source-weight tails",
            "zero_condition": "delta_{v_perp} S_matter=0 channel-by-channel before cancellation",
            "finite_bound": "||J_matter||_2 <= sum of absolute geometry, constant, marker, source-weight, boundary, readout, and non-Hilbert components",
            "status": "TARGET_RESTATED_FOR_R2FR_JPERP",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "MSF3235_1_chain_rule",
            "object": "matter action variation",
            "formula": "delta_v S_A = 1/2 int sqrt(-g_obs) T_A^{mu nu} L_v g_obs_munu + sum_a int J_theta,A^a L_v theta_A^a + E_A delta_v Psi_A + B_A[v]",
            "zero_condition": "on-shell matter or owned gauge lift kills E_A delta_v Psi_A; observed geometry and constants are v_perp-blind; boundary term is compact/exact/proper",
            "finite_bound": "C_e,A||D_perp e_obs|| + sum_a C_theta,Aa||D_perp theta_A^a|| + C_Psi,A||delta_v Psi_A||_nongauge + C_B,A||B_A[v]||",
            "status": "EXACT_CHAIN_RULE_DERIVED_CONDITIONALLY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "MSF3235_2_pullback_zero_theorem",
            "object": "ordinary matter pullback",
            "formula": "S_A = S_A[Psi_A, e_obs(q(Phi)), theta_A^0] and Dq[v_perp]=0 imply L_v e_obs=0 and L_v theta_A=0",
            "zero_condition": "parent signs e_obs(q), theta_A superselection, matter lift, and boundary support in one clause",
            "finite_bound": "if unsigned, keep qbar_geom and qbar_constants components",
            "status": "EXACT_IF_PARENT_SIGNED_NOT_CURRENT_CLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "MSF3235_3_source_functor",
            "object": "source-current universality",
            "formula": "one S_matter gives T_A := 2/sqrt(-g_obs) delta S_A/delta g_obs and source current sum_A T_A with one common kappa",
            "zero_condition": "no relative w_A, kappa_A, source-label, hidden-frame, or non-Hilbert source covector exists in parent constructor image",
            "finite_bound": "J_source_weight_bound := C_kappa max_A |kappa_A/kappa_univ - 1| + C_label||a_source||",
            "status": "CONDITIONAL_SOURCE_FUNCTOR_ROUTE_COUNTERMODEL_RETAINED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "MSF3235_4_total_zero",
            "object": "J_matter=0",
            "formula": "J_matter=0 follows only if geometry pullback, constants/no-marker, matter lift, boundary silence, readout closure, and source-current universality all close on the same branch",
            "zero_condition": "all MSF3235 antecedents parent-signed; no cancellation between components",
            "finite_bound": "otherwise use JMB3235_7_total_abs_guard",
            "status": "FAIL_CURRENT_CLAIM_ZERO_NOT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    marker_rows = [
        {
            "gate_id": "NMG3235_0_fixed_label",
            "gate": "fixed/discrete labels",
            "statement": "True species/representation labels that are fixed external data have D_v theta_A=0.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "surviving_counterexample": "co-moving material/preparation/domain labels are not fixed representation data",
            "effect_on_Jmatter": "kills only fixed-label marker pieces",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "NMG3235_1_no_extension_domain",
            "gate": "no co-moving marker extension",
            "statement": "Parent ordinary-matter category excludes theta_A=theta_A(q(Phi),m_A(X_perp)) extensions.",
            "status": "NOT_PARENT_SIGNED",
            "surviving_counterexample": "m_A=m0+epsilon I_perp remains legal if I_perp is an allowed scalar/readout/domain invariant",
            "effect_on_Jmatter": "retain J_marker_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "NMG3235_2_constant_superselection",
            "gate": "masses, charges, alpha_EM, clock standards",
            "statement": "Lie_v theta_A=0 for all constants entering matter, clocks, EM, and material standards.",
            "status": "NOT_PARENT_SIGNED",
            "surviving_counterexample": "continuous constants can carry transverse/readout dependence unless topological or superselection ownership is supplied",
            "effect_on_Jmatter": "retain J_constants_bound and clock/alpha links",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "NMG3235_3_source_weight",
            "gate": "relative source weights",
            "statement": "S_matter=sum_A S_A with one common normalization, not sum_A w_A S_A with active w_A.",
            "status": "COUNTERMODEL_LIVE",
            "surviving_counterexample": "w_A or kappa_A changes active source normalization while preserving covariance/additivity",
            "effect_on_Jmatter": "retain J_source_weight_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "NMG3235_4_readout_nonhilbert_tail",
            "gate": "readout, non-Hilbert, support/domain tail",
            "statement": "post-readout masks, source support shifts, domain terms, connection tails, and non-Hilbert currents are absent or separately bounded.",
            "status": "NOT_DERIVED",
            "surviving_counterexample": "readout/source-domain operations can add transverse source terms after the bare matter functor descends",
            "effect_on_Jmatter": "retain J_readout_nonH_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "NMG3235_5_verdict",
            "gate": "full matter no-marker/source-functor theorem",
            "statement": "ordinary matter has no independent transverse marker/source covector only if every preceding gate closes in one parent clause.",
            "status": "FAIL_CURRENT_CLAIM",
            "surviving_counterexample": "material markers, constants, source weights, readout tails, and boundary/support terms remain legal",
            "effect_on_Jmatter": "J_matter remains a finite residual component, not a zero claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    bound_rows = [
        {
            "bound_id": "JMB3235_0_geom",
            "quantity": "J_geom_matter_bound",
            "formula": "sum_A C_e,A ||D_perp e_obs||_A",
            "required_inputs": "observed coframe functor e_obs(q); Dq[v_perp]=0 certificate; stress envelope C_e,A; support/norm units",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JMB3235_1_constants",
            "quantity": "J_constants_bound",
            "formula": "sum_A,a C_theta,Aa ||D_perp theta_A^a||",
            "required_inputs": "mass/charge/alpha/clock/material constant list; D_perp theta values or theorem-zero certificates; units/source paths",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JMB3235_2_marker",
            "quantity": "J_marker_bound",
            "formula": "sum_m C_marker,m ||b_marker,m|| with b_marker,m := D_vperp ln M_m or D_vperp theta_m",
            "required_inputs": "material/preparation/source marker catalogue; sensitivities C_marker,m; b_marker values or no-marker theorem",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JMB3235_3_source_weight",
            "quantity": "J_source_weight_bound",
            "formula": "C_kappa max_A |kappa_A/kappa_univ - 1| + C_label ||a_source||",
            "required_inputs": "source-current universality certificate or relative source-weight values; same-frame normalization",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JMB3235_4_boundary_support",
            "quantity": "J_matter_boundary_bound",
            "formula": "C_B ||B_matter[v_perp]|| + C_support ||Delta_W_support||",
            "required_inputs": "compact support/exact boundary theorem or boundary/source-support norms",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JMB3235_5_readout_nonH",
            "quantity": "J_readout_nonH_bound",
            "formula": "C_readout ||D_perp R_matter|| + C_nonH ||q_nonH|| + C_domain ||q_domain||",
            "required_inputs": "readout closure theorem or finite readout/non-Hilbert/domain coefficients",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JMB3235_6_matter_lift",
            "quantity": "J_matter_lift_bound",
            "formula": "sum_A C_Psi,A ||delta_v Psi_A||_nongauge",
            "required_inputs": "ordinary matter bundle/category; gauge/Lorentz/diffeomorphism lift theorem or nongauge lift norm",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JMB3235_7_total_abs_guard",
            "quantity": "J_matter_bound",
            "formula": "||J_matter||_2 <= J_geom_matter_bound + J_constants_bound + J_marker_bound + J_source_weight_bound + J_matter_boundary_bound + J_readout_nonH_bound + J_matter_lift_bound",
            "required_inputs": "each component theorem-zero or finite source-backed numeric bound; no cancellation allowed",
            "status": "NO_CANCELLATION_BOUND_READY_VALUES_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    update_rows = [
        {
            "update_id": "UP3235_0_refined_jperp",
            "target": "J_perp source norm",
            "formula": "||J_perp^tau||_2 <= J_geom_bound + J_matter_bound + J_EM_trace_bound + (1/4) C_F2_perp ||F^2||_2 + J_Poynting_bound + J_memory_projector_bound",
            "change": "J_matter_bound is now the explicit JMB3235_7 no-cancellation envelope rather than a blank symbol",
            "status": "REFINED_BOUND_FOR_LOCAL_BRANCH",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "update_id": "UP3235_1_exact_zero_requirements",
            "target": "v_perp exact-zero route",
            "formula": "J_matter=0 requires MSF3235_2 + NMG3235_5 plus boundary/readout/source-current closure on the same branch",
            "change": "ordinary matter can be killed by derivation, but only with a signed parent matter functor/no-marker source certificate",
            "status": "ZERO_ROUTE_EXACT_BUT_UNSIGNED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "update_id": "UP3235_2_observable_links",
            "target": "empirical residual vector",
            "formula": "J_matter components feed WEP/source charge, clocks/fine-structure, R10/local fifth force, and composition/source-normalization tests",
            "change": "if zero theorem fails, the right data route is component rows for b_marker, D_perp theta, delta_kappa_A, q_nonH, q_domain, and readout leakage",
            "status": "EVIDENCE_MAPPING_READY_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3235_0_result",
            "decision": "MATTER_SOURCE_FUNCTOR_CHAIN_RULE_DERIVED_ZERO_UNSIGNED_BOUND_ENVELOPE_READY",
            "because": "the matter channel has an exact chain-rule zero theorem if ordinary matter, constants, matter lift, boundary support, readout, and source-current functors all descend through the same quotient branch; current sources leave material markers/source weights/readout tails legal",
            "claim_status": "NO_LOCAL_GR_NO_WEP_NO_CLOCK_NO_R10_NO_SOURCE_COUPLING_CLAIM",
            "next_action": "carry J_matter_bound in the local residual vector unless a parent matter-functor/no-marker certificate is supplied",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3235_1_next_target",
            "decision": "3236-Y5-R2FR-memory-projector-domain-commutation-or-finite-bound-for-Jperp-under-AX1090",
            "because": "after EM_F2, Poynting, and ordinary matter/source markers are explicit, the remaining non-geometric live channel is memory/projector/domain commutation",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "derive whether memory kernel/projector/domain variations commute with the transverse split, or stage a finite J_memory_projector_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, derivation_rows, marker_rows, bound_rows, update_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    marker_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    update_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, DERIVATION, NO_MARKER, BOUND, UPDATE, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    chain_rule = any(row["derivation_id"] == "MSF3235_1_chain_rule" for row in derivation_rows)
    total_zero_unsigned = any(row["derivation_id"] == "MSF3235_4_total_zero" for row in derivation_rows)
    no_marker_verdict = any(row["gate_id"] == "NMG3235_5_verdict" for row in marker_rows)
    finite_bound = any(row["bound_id"] == "JMB3235_7_total_abs_guard" for row in bound_rows)
    jperp_update = any(row["update_id"] == "UP3235_0_refined_jperp" for row in update_rows)
    next_target = decision_rows[-1]["decision"].startswith("3236-")
    claim_true_count = 0
    for rows in [input_rows, derivation_rows, marker_rows, bound_rows, update_rows, decision_rows]:
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
        {"check_id": "VAL3235_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3235_01_chain_rule", "pass": b(chain_rule), "detail": "matter chain-rule source identity present", "generated_utc": now},
        {"check_id": "VAL3235_02_zero_unsigned", "pass": b(total_zero_unsigned), "detail": "exact zero route specified as unsigned", "generated_utc": now},
        {"check_id": "VAL3235_03_no_marker_gate", "pass": b(no_marker_verdict), "detail": "no-marker/source-functor verdict present", "generated_utc": now},
        {"check_id": "VAL3235_04_finite_bound", "pass": b(finite_bound), "detail": "J_matter no-cancellation envelope present", "generated_utc": now},
        {"check_id": "VAL3235_05_jperp_update", "pass": b(jperp_update), "detail": "J_perp refined bound present", "generated_utc": now},
        {"check_id": "VAL3235_06_claims_blocked", "pass": b(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3235_07_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3235_08_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3235_09_next_target", "pass": b(next_target), "detail": str(decision_rows[-1]["decision"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    marker_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    update_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3235 - Matter-marker Source-functor Silence Or Bound for Jperp under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, source-coupling claim, PPN pass, or public-facing result.

## Result

3235 takes the ordinary matter channel out of the fog and puts it into the local `J_perp` residual vector.

The exact chain-rule identity is:

```text
delta_v S_A
= 1/2 int sqrt(-g_obs) T_A^{{mu nu}} L_v g_obs_munu
 + sum_a int J_theta,A^a L_v theta_A^a
 + E_A delta_v Psi_A
 + B_A[v].
```

So the clean zero theorem is real:

```text
S_A = S_A[Psi_A, e_obs(q(Phi)), theta_A^0],
Dq[v_perp]=0,
L_v theta_A=0,
delta_v Psi_A is fixed/gauge/on-shell,
B_A[v_perp]=0
=> delta_v S_A=0
=> J_matter=0.
```

But it is not a current MTS claim, because the same parent clause must also rule out:

```text
co-moving material/preparation markers,
continuous mass/charge/alpha/clock constants,
relative source weights kappa_A or w_A,
post-readout/source-domain/non-Hilbert tails,
matter boundary/support terms.
```

The finite no-cancellation envelope is:

```text
||J_matter||_2
<= J_geom_matter_bound
 + J_constants_bound
 + J_marker_bound
 + J_source_weight_bound
 + J_matter_boundary_bound
 + J_readout_nonH_bound
 + J_matter_lift_bound.
```

Current verdict: `MATTER_SOURCE_FUNCTOR_CHAIN_RULE_DERIVED_ZERO_UNSIGNED_BOUND_ENVELOPE_READY`.

## Matter Source-functor Derivation

{md_table(derivation_rows, ["derivation_id", "object", "formula", "zero_condition", "finite_bound", "status", "valid_for_claim"])}

## No-marker Source-functor Gate

{md_table(marker_rows, ["gate_id", "gate", "statement", "status", "surviving_counterexample", "effect_on_Jmatter", "valid_for_claim"])}

## Jmatter Component Bound

{md_table(bound_rows, ["bound_id", "quantity", "formula", "required_inputs", "status", "valid_for_claim"])}

## Jperp Update

{md_table(update_rows, ["update_id", "target", "formula", "change", "status", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3235_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3235_MATTER_SOURCE_FUNCTOR_DERIVATION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3235_NO_MARKER_SOURCE_FUNCTOR_GATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3235_JMATTER_COMPONENT_BOUND.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3235_JPERP_UPDATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3235_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3235_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, derivation_rows, marker_rows, bound_rows, update_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (DERIVATION, derivation_rows),
        (NO_MARKER, marker_rows),
        (BOUND, bound_rows),
        (UPDATE, update_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, derivation_rows, marker_rows, bound_rows, update_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, derivation_rows, marker_rows, bound_rows, update_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()

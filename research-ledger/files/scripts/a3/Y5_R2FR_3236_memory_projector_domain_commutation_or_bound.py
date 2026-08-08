from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3236-Y5-R2FR-memory-projector-domain-commutation-or-finite-bound-for-Jperp-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3236_INPUTS.csv"
DERIVATION = OUT / "P8_Y5_R2FR_3236_MEMORY_PROJECTOR_COMMUTATOR_DERIVATION.csv"
GATES = OUT / "P8_Y5_R2FR_3236_PROJECTOR_DOMAIN_ZERO_GATES.csv"
BOUND = OUT / "P8_Y5_R2FR_3236_MEMORY_PROJECTOR_COMPONENT_BOUND.csv"
UPDATE = OUT / "P8_Y5_R2FR_3236_JPERP_UPDATE.csv"
DECISION = OUT / "P8_Y5_R2FR_3236_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3236_VALIDATION.csv"


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
        "input_id": "SRC3236_00_3235_doc",
        "location": "post_checkpoint",
        "relative_path": "3235-Y5-R2FR-matter-marker-source-functor-silence-or-bound-for-Jperp-under-AX1090.md",
        "role": "3235 handoff selecting memory/projector/domain next",
        "terms": ["3236", "memory-projector", "J_matter_bound", "next target"],
    },
    {
        "input_id": "SRC3236_01_3231_doc",
        "location": "post_checkpoint",
        "relative_path": "3231-Y5-R2FR-transverse-source-channel-silence-or-bound-for-Jperp-under-AX1090.md",
        "role": "J_perp split containing memory/projector channel",
        "terms": ["J_memory", "J_projector", "J_memory_projector_bound", "MISSING_PROJECTOR_ORTHOGONALITY"],
    },
    {
        "input_id": "SRC3236_02_3231_source_csv",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3231_JPERP_SOURCE_SILENCE_AUDIT.csv",
        "role": "machine memory/projector source-channel row",
        "terms": ["JPA3231_6_memory_projector", "projector commutes", "J_memory_projector_bound"],
    },
    {
        "input_id": "SRC3236_03_3230_doc",
        "location": "post_checkpoint",
        "relative_path": "3230-Y5-R2FR-transverse-branch-amplitude-bound-for-Etransport-under-AX1090.md",
        "role": "transverse amplitude law and projector split",
        "terms": ["J_memory", "J_projector", "v_perp", "P_perp"],
    },
    {
        "input_id": "SRC3236_04_3229_doc",
        "location": "post_checkpoint",
        "relative_path": "3229-Y5-R2FR-same-branch-clock-transport-identity-for-DtauRQ-under-AX1090.md",
        "role": "branch projection and transport identity",
        "terms": ["P_perp", "projection split", "D_vert R_Q", "transport"],
    },
    {
        "input_id": "SRC3236_05_1013_doc",
        "location": "post_checkpoint",
        "relative_path": "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
        "role": "projector product-rule obstruction precedent",
        "terms": ["d(Pi_M J_H)", "[d,Pi_M]J_H", "commutator", "obstruction"],
    },
    {
        "input_id": "SRC3236_06_1014_doc",
        "location": "post_checkpoint",
        "relative_path": "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
        "role": "commutator/projector variation zero-or-bound precedent",
        "terms": ["[d,Pi_M]J_H=0", "delta Pi_M", "projector stress", "I_commutator"],
    },
    {
        "input_id": "SRC3236_07_pim_commutator",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_PIM_COMMUTATOR_GATE.csv",
        "role": "machine projector product-rule/commutator gate",
        "terms": ["PC521_0_product_rule", "PC521_1_variation_rule", "PC521_5_closure_not_from_algebra"],
    },
    {
        "input_id": "SRC3236_08_pim_variation_stress",
        "location": "mts_residuals",
        "relative_path": "P8_PiM_projector_variation_stress_CONTRACT.csv",
        "role": "projector variation stress contract",
        "terms": ["PV0_product_variation_included", "PV2_Hodge_DeWitt_metric_dependence_retained", "PV8_retained_residual_fallback"],
    },
    {
        "input_id": "SRC3236_09_pim_algebra",
        "location": "mts_residuals",
        "relative_path": "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "role": "projector algebra cannot substitute for closure",
        "terms": ["PM4_projector_algebra", "PM5_projector_variation_owned", "PM6_flux_closure_requires_Ward_or_Euler"],
    },
    {
        "input_id": "SRC3236_10_mass_flux",
        "location": "mts_residuals",
        "relative_path": "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "role": "Euler/flux closure and calibration contract",
        "terms": ["MF0_parent_projector_origin", "MF2_Euler_flux_closure", "MF6_zero_boundary_and_nonHilbert_flux"],
    },
    {
        "input_id": "SRC3236_11_1019_doc",
        "location": "post_checkpoint",
        "relative_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "role": "boundary/projector orthogonality and source-pack precedent",
        "terms": ["Projector orthogonality", "Pi_M^H", "source pack", "Qbar_edge_XH"],
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
            "derivation_id": "MPC3236_0_target",
            "object": "memory/projector/domain source",
            "formula": "J_memory_projector := local transverse projection of variations in memory kernel K_mem, source projector P_mem/Pi, domain selector chi_D, and branch projector P_perp",
            "zero_condition": "all projectors/kernels/domains are fixed, quotient-basic, or commute with D_perp on the same branch",
            "finite_bound": "||J_memory_projector||_2 <= sum of commutator, kernel, domain, branch-projector, boundary, and readout components",
            "status": "TARGET_RESTATED_FOR_R2FR_JPERP",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "MPC3236_1_product_rule",
            "object": "projected memory source product rule",
            "formula": "D_perp(P K_mem chi_D Y)=P K_mem chi_D D_perpY + [D_perp,P]K_mem chi_D Y + P(D_perpK_mem)chi_DY + P K_mem(D_perp chi_D)Y",
            "zero_condition": "[D_perp,P]=0, D_perpK_mem=0, D_perp chi_D=0, and the baseline D_perpY term is already counted in the non-projector source",
            "finite_bound": "J_comm + J_kernel + J_domain + baseline-counting guard",
            "status": "EXACT_PRODUCT_RULE_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "MPC3236_2_branch_projector",
            "object": "P_perp branch projector variation",
            "formula": "D_perp(P_perp R_Q)=P_perp D_perp R_Q + (D_perp P_perp)R_Q",
            "zero_condition": "P_perp is parent-owned/fixed along the selected branch or R_Q=0 strongly enough that (D_perp P_perp)R_Q vanishes",
            "finite_bound": "J_Pperp_bound := ||D_perp P_perp||_op ||R_Q||",
            "status": "PROJECTOR_VARIATION_TERM_EXPLICIT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "MPC3236_3_memory_kernel",
            "object": "memory kernel/source map",
            "formula": "D_perp K_mem = 0 if K_mem is quotient-basic/topological/fixed by parent branch; otherwise (D_perpK_mem)source survives",
            "zero_condition": "K_mem=Kbar_mem[q(Phi)] and Dq[v_perp]=0 for this transverse piece, or memory sector is orthogonal to P_perp",
            "finite_bound": "J_kernel_bound := ||P|| ||D_perpK_mem||_op ||source||",
            "status": "CONDITIONAL_ZERO_OR_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "MPC3236_4_domain_selector",
            "object": "domain/support selector",
            "formula": "D_perp chi_D and D_perp boundary/domain normals produce support-shift terms",
            "zero_condition": "domain/homology/support class is parent fixed/topological/proper, or support variation is boundary-exact and zero",
            "finite_bound": "J_domain_bound := C_chi||D_perp chi_D|| ||Y|| + B_domain_shift",
            "status": "DOMAIN_LEAK_RETAINED_UNLESS_OWNED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "MPC3236_5_total_zero",
            "object": "J_memory_projector=0",
            "formula": "J_memory_projector=0 only if product-rule commutator, projector variation, memory kernel derivative, domain/support variation, boundary/corner, and readout masks are all zero on the same branch",
            "zero_condition": "MPC3236 gates all parent-signed; no cancellation between components",
            "finite_bound": "otherwise use MPB3236_6_total_abs_guard",
            "status": "FAIL_CURRENT_CLAIM_ZERO_NOT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    gate_rows = [
        {
            "gate_id": "MPG3236_0_fixed_parent_projector",
            "gate": "fixed parent projector",
            "statement": "P, Pi_M, or P_mem is defined before readout from parent topology/symplectic/source identity and is covariantly constant on the local branch.",
            "status": "NOT_PARENT_SIGNED",
            "failure_mode": "projector becomes a readout/domain mask and its variation acts as a hidden source",
            "effect": "retain commutator and projector-stress terms",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "MPG3236_1_commutator_zero",
            "gate": "projector commutator",
            "statement": "[D_perp,P]Y=0 or [d,Pi_M]J_H=0 follows from fixed/topological projector and Hilbert equality.",
            "status": "CONDITIONAL_NOT_DERIVED",
            "failure_mode": "commutator term shifts measured source/memory projection",
            "effect": "retain J_commutator_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "MPG3236_2_memory_basicness",
            "gate": "memory kernel quotient-basicness",
            "statement": "K_mem and memory source map descend through q or are orthogonal to the transverse branch.",
            "status": "NOT_PARENT_SIGNED",
            "failure_mode": "memory kernel supplies D_perpK_mem source terms even if visible matter and EM are quiet",
            "effect": "retain J_kernel_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "MPG3236_3_domain_support",
            "gate": "domain/homology/support fixedness",
            "statement": "chi_D, boundary normal, S2 representative, support annulus, and homology class are parent fixed/topological or their shifts are separately bounded.",
            "status": "NOT_PARENT_SIGNED",
            "failure_mode": "support/domain movement creates local source terms and preferred-location/frame tails",
            "effect": "retain J_domain_bound and boundary shift rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "MPG3236_4_no_readout_mask",
            "gate": "no post-readout projector mask",
            "statement": "readout/projector masks act only after theorem or residual scoring and never inside the parent variation.",
            "status": "POLICY_ACTIVE_THEOREM_OPEN",
            "failure_mode": "post-fit masks can fake source closure or erase a bad projector term",
            "effect": "forbid derivation credit from readout masks; retain closure-only if used",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "MPG3236_5_algebra_not_closure",
            "gate": "projector algebra guard",
            "statement": "P^2=P, self-adjointness, or block decomposition does not imply D_perp(PY)=P D_perpY or d(Pi_MJ_H)=0.",
            "status": "ACTIVE_GUARD",
            "failure_mode": "counting projector algebra as source silence smuggles closure",
            "effect": "requires commutator zero or finite source-backed commutator bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "MPG3236_6_verdict",
            "gate": "full memory/projector/domain zero",
            "statement": "the channel closes only if fixed projector, commutator zero, memory basicness, domain/support fixedness, no-readout-mask, and boundary silence all close together.",
            "status": "FAIL_CURRENT_CLAIM",
            "failure_mode": "memory/projector/domain source remains live",
            "effect": "J_memory_projector_bound remains in J_perp",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    bound_rows = [
        {
            "bound_id": "MPB3236_0_commutator",
            "quantity": "J_commutator_bound",
            "formula": "||[D_perp,P]K_mem chi_D Y||_2 <= C_comm ||[D_perp,P]||_op ||K_mem chi_D Y||",
            "required_inputs": "projector definition; D_perp projector operator norm or theorem-zero; source norm; units/source paths",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "MPB3236_1_kernel",
            "quantity": "J_kernel_bound",
            "formula": "||P(D_perp K_mem)chi_DY||_2 <= ||P|| ||D_perp K_mem||_op ||chi_DY||",
            "required_inputs": "memory kernel source map; D_perpK_mem bound or quotient-basic theorem; support norm",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "MPB3236_2_domain",
            "quantity": "J_domain_bound",
            "formula": "||P K_mem(D_perp chi_D)Y||_2 + B_domain_shift <= C_chi||D_perp chi_D|| ||Y|| + B_domain_shift",
            "required_inputs": "domain selector; support shift; boundary/corner terms; fixed homology certificate or numeric norms",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "MPB3236_3_branch_projector",
            "quantity": "J_Pperp_bound",
            "formula": "||(D_perp P_perp)R_Q||_2 <= ||D_perp P_perp||_op ||R_Q||_2",
            "required_inputs": "branch projector definition; operator norm; R_Q near-root norm or theorem-zero",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "MPB3236_4_boundary",
            "quantity": "J_MP_boundary_bound",
            "formula": "C_B ||B_MP[v_perp]|| + C_corner ||corner_MP||",
            "required_inputs": "boundary/corner/worldtube projector terms or exact/proper boundary theorem",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "MPB3236_5_readout",
            "quantity": "J_MP_readout_bound",
            "formula": "C_readout ||D_perp P_read|| ||Y||",
            "required_inputs": "proof readout masks are outside parent variation or finite readout-mask coefficient rows",
            "status": "POLICY_GUARD_READY_VALUES_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "MPB3236_6_total_abs_guard",
            "quantity": "J_memory_projector_bound",
            "formula": "||J_memory_projector||_2 <= J_commutator_bound + J_kernel_bound + J_domain_bound + J_Pperp_bound + J_MP_boundary_bound + J_MP_readout_bound",
            "required_inputs": "each component theorem-zero or finite source-backed numeric bound; no cancellation allowed",
            "status": "NO_CANCELLATION_BOUND_READY_VALUES_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    update_rows = [
        {
            "update_id": "UP3236_0_refined_jperp",
            "target": "J_perp source norm",
            "formula": "||J_perp^tau||_2 <= J_geom_bound + J_matter_bound + J_EM_trace_bound + (1/4)C_F2_perp||F^2||_2 + J_Poynting_bound + J_memory_projector_bound",
            "change": "J_memory_projector_bound is now the explicit MPB3236_6 no-cancellation envelope",
            "status": "REFINED_BOUND_FOR_LOCAL_BRANCH",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "update_id": "UP3236_1_yperp_feedback",
            "target": "transverse amplitude law",
            "formula": "a_perp=J_perp_bound/m_perp_min now includes MPB3236_6; Y_perp <= (a_perp+sqrt(a_perp^2+4Phi_perp_bound))/2",
            "change": "projector/memory/domain leakage can no longer be silently dropped from v_perp",
            "status": "FEEDS_3230_YPERP",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "update_id": "UP3236_2_transport_feedback",
            "target": "clock/local transport error",
            "formula": "E_transport keeps D_perpR_Q[v_perp] plus vertical term; any projector-induced Y_perp raises E_clock_transport",
            "change": "projector/domain leakage is connected back to the local clock/alpha transport gate",
            "status": "FEEDS_3229_TRANSPORT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3236_0_result",
            "decision": "MEMORY_PROJECTOR_PRODUCT_RULE_DERIVED_COMMUTATOR_BOUND_ENVELOPE_READY",
            "because": "the memory/projector/domain channel is now an exact product-rule commutator problem; zero requires fixed/commuting projector, quotient-basic memory kernel, fixed domain/support, and no readout masks, none currently parent-signed together",
            "claim_status": "NO_LOCAL_GR_NO_NEWTON_NO_PPN_NO_CLOCK_NO_SOURCE_NORMALIZATION_CLAIM",
            "next_action": "carry J_memory_projector_bound in the local residual vector unless projector/domain commutation is parent-signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3236_1_next_target",
            "decision": "3237-Y5-R2FR-geometric-Euler-same-branch-source-zero-or-bound-for-Jperp-under-AX1090",
            "because": "EM_F2, Poynting, matter/source markers, and memory/projector/domain channels now have explicit zero-or-bound envelopes; the remaining top-level J_perp source is the geometric/Euler same-branch term",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "derive whether J_geom vanishes from parent Euler equations on the same branch, or stage finite geometric residual/source-worldtube bounds",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, derivation_rows, gate_rows, bound_rows, update_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    update_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, DERIVATION, GATES, BOUND, UPDATE, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    product_rule = any(row["derivation_id"] == "MPC3236_1_product_rule" for row in derivation_rows)
    zero_unsigned = any(row["derivation_id"] == "MPC3236_5_total_zero" for row in derivation_rows)
    algebra_guard = any(row["gate_id"] == "MPG3236_5_algebra_not_closure" for row in gate_rows)
    finite_bound = any(row["bound_id"] == "MPB3236_6_total_abs_guard" for row in bound_rows)
    jperp_update = any(row["update_id"] == "UP3236_0_refined_jperp" for row in update_rows)
    next_target = decision_rows[-1]["decision"].startswith("3237-")
    claim_true_count = 0
    for rows in [input_rows, derivation_rows, gate_rows, bound_rows, update_rows, decision_rows]:
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
        {"check_id": "VAL3236_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3236_01_product_rule", "pass": b(product_rule), "detail": "memory/projector product rule present", "generated_utc": now},
        {"check_id": "VAL3236_02_zero_unsigned", "pass": b(zero_unsigned), "detail": "exact zero route specified as unsigned", "generated_utc": now},
        {"check_id": "VAL3236_03_algebra_guard", "pass": b(algebra_guard), "detail": "projector algebra not counted as closure", "generated_utc": now},
        {"check_id": "VAL3236_04_finite_bound", "pass": b(finite_bound), "detail": "J_memory_projector no-cancellation envelope present", "generated_utc": now},
        {"check_id": "VAL3236_05_jperp_update", "pass": b(jperp_update), "detail": "J_perp refined bound present", "generated_utc": now},
        {"check_id": "VAL3236_06_claims_blocked", "pass": b(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3236_07_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3236_08_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3236_09_next_target", "pass": b(next_target), "detail": str(decision_rows[-1]["decision"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    update_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3236 - Memory-projector Domain Commutation Or Finite Bound for Jperp under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, source-normalization claim, PPN pass, or public-facing result.

## Result

3236 converts the memory/projector/domain channel into an exact product-rule obstruction.

The central identity is:

```text
D_perp(P K_mem chi_D Y)
= P K_mem chi_D D_perpY
 + [D_perp,P] K_mem chi_D Y
 + P(D_perp K_mem) chi_D Y
 + P K_mem(D_perp chi_D)Y.
```

So `J_memory_projector=0` is not free. It requires:

```text
[D_perp,P]=0,
D_perp K_mem=0,
D_perp chi_D=0,
D_perp P_perp=0 or R_Q=0 strongly enough,
no boundary/corner/domain shift,
no post-readout projector mask.
```

The finite no-cancellation envelope is:

```text
||J_memory_projector||_2
<= J_commutator_bound
 + J_kernel_bound
 + J_domain_bound
 + J_Pperp_bound
 + J_MP_boundary_bound
 + J_MP_readout_bound.
```

Important guard:

```text
P^2=P or projector algebra alone does not imply source closure.
```

Current verdict: `MEMORY_PROJECTOR_PRODUCT_RULE_DERIVED_COMMUTATOR_BOUND_ENVELOPE_READY`.

## Memory-projector Commutator Derivation

{md_table(derivation_rows, ["derivation_id", "object", "formula", "zero_condition", "finite_bound", "status", "valid_for_claim"])}

## Projector/domain Zero Gates

{md_table(gate_rows, ["gate_id", "gate", "statement", "status", "failure_mode", "effect", "valid_for_claim"])}

## Memory-projector Component Bound

{md_table(bound_rows, ["bound_id", "quantity", "formula", "required_inputs", "status", "valid_for_claim"])}

## Jperp Update

{md_table(update_rows, ["update_id", "target", "formula", "change", "status", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3236_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3236_MEMORY_PROJECTOR_COMMUTATOR_DERIVATION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3236_PROJECTOR_DOMAIN_ZERO_GATES.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3236_MEMORY_PROJECTOR_COMPONENT_BOUND.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3236_JPERP_UPDATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3236_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3236_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, derivation_rows, gate_rows, bound_rows, update_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (DERIVATION, derivation_rows),
        (GATES, gate_rows),
        (BOUND, bound_rows),
        (UPDATE, update_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, derivation_rows, gate_rows, bound_rows, update_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, derivation_rows, gate_rows, bound_rows, update_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()

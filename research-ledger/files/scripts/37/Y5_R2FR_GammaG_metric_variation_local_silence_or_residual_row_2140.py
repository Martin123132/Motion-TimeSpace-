from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2140-Y5-R2FR-GammaG-metric-variation-local-silence-or-residual-row.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOC_2139 = ROOT / "2139-Y5-R2FR-deep-parent-action-owner-hunt-or-coefficient-owner-checklist.md"
CSV_2139_VAL = OUT / "P8_Y5_BRR545_2139_VALIDATION.csv"
CSV_2139_ACTION = OUT / "P8_Y5_PARENT_QLOC_2139_ACTION_SOURCE_ROWS.csv"
CSV_2139_GAMMA = OUT / "P8_Y5_PARENT_QLOC_2139_GAMMAG_VARIATION_ROWS.csv"
CSV_2139_NEXT = OUT / "P8_Y5_PARENT_QLOC_2139_NEXT_TARGET.csv"

ACTION_PRINCIPLE = REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"
FUNDAMENTAL_ACTION = REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def has_any(text: str, alternatives: list[str]) -> bool:
    return any(item in text for item in alternatives)


def formalization_has_2140_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2140-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2140*",
        "*Y5_R2FR_GammaG_metric_variation_local_silence_or_residual_row_2140*",
        "*AFRAME_GAMMAG_VARIATION_2140*",
        "*JR2140*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2140_00_2139_doc",
            DOC_2139,
            [["Current Verdict"], ["Gamma_G", "Γ_G"], ["metric variation"], ["A_curv_aux"]],
            "2139 handoff identifies Gamma_G rather than A_curv_aux as the action-owner gate.",
        ),
        (
            "SRC2140_01_2139_validation",
            CSV_2139_VAL,
            [["VAL2139_OVERALL"], ["PASS"], ["Gamma_G variation", "GammaG variation"]],
            "2139 validation passed and selected the Gamma_G gate.",
        ),
        (
            "SRC2140_02_2139_action_rows",
            CSV_2139_ACTION,
            [["ACT2139_4_Gamma_functional"], ["ACT2139_5_Gamma_variation_assumption"], ["GAMMAG_METRIC_INDEPENDENCE_ASSUMED"]],
            "machine-readable action rows expose the functional/variation tension.",
        ),
        (
            "SRC2140_03_2139_gamma_rows",
            CSV_2139_GAMMA,
            [["GVAR2139_4_verdict"], ["NEXT_GATE_REQUIRED"], ["delta Gamma_G ignored", "delta[Gamma_G]"]],
            "Gamma variation rows state the unresolved local-GR gate.",
        ),
        (
            "SRC2140_04_2139_next",
            CSV_2139_NEXT,
            [["NEXT2139_0_2140"], ["Gamma_G is truly metric-independent", "GammaG-metric", "Gamma_G metric variation"], ["residual row"]],
            "2139 next-target contract.",
        ),
        (
            "SRC2140_05_action_principle",
            ACTION_PRINCIPLE,
            [["scalar functional of the smoothed curvature"], ["independent of metric variation"], ["GR is recovered", "pure GR is recovered"]],
            "raw action-principle text both makes Gamma_G geometric/history dependent and assumes variation silence.",
        ),
        (
            "SRC2140_06_fundamental_action",
            FUNDAMENTAL_ACTION,
            [["dynamic geometric potential"], ["Variation of"], ["Gamma_G", "Γ_G"]],
            "second raw action text repeats the dynamic-potential variation claim.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        groups_found = exists and all(has_any(text, alternatives) for alternatives in needle_groups)
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                needles_found=groups_found,
                role=role,
                expected_needles="; ".join(" OR ".join(group) for group in needle_groups),
            )
        )
    return rows


def variation_identity_rows() -> list[dict[str, object]]:
    return [
        row(
            theorem_id="GVAR2140_0_action_piece",
            object="Gamma_G action density",
            statement="For I_Gamma[g,Phi]=int_U Gamma_G[g,Phi](x) sqrt(-g) d^4x, the algebraic cosmological-term result is recovered only when delta Gamma_G is zero and boundary terms vanish.",
            status="EXACT_CONDITIONAL_IDENTITY",
            consequence="the 2139 source is usable, but the source only proves the external-scalar branch unless the functional derivative is signed zero",
        ),
        row(
            theorem_id="GVAR2140_1_decomposition",
            object="first metric variation",
            statement="If delta Gamma_G = D_Gamma^{mu nu} delta g_{mu nu} + div(Theta_Gamma), then delta(Gamma_G sqrt(-g)) contains both the algebraic Gamma_G g_{mu nu} piece and a residual D_Gamma^{mu nu} piece.",
            status="EXACT_VARIATION_DECOMPOSITION",
            consequence="local GR requires more than Gamma_G=0; it also requires D_Gamma^{mu nu}=0 and silent boundary/history terms",
        ),
        row(
            theorem_id="GVAR2140_2_external_scalar_lemma",
            object="external scalar branch",
            statement="If Gamma_G is a prescribed external scalar during metric variation, then D_Gamma^{mu nu}=0 by definition and the raw action derivation is internally consistent as an effective-background model.",
            status="VALID_BUT_NARROW_BRANCH",
            consequence="this branch does not yet derive Gamma_G from the parent motion field as a varied geometric functional",
        ),
        row(
            theorem_id="GVAR2140_3_geometry_functional_lemma",
            object="geometric/history functional branch",
            statement="If Gamma_G depends on smoothed curvature, metric, connection, coframe, or the psi-defined emergent geometry, then D_Gamma^{mu nu} is generically nonzero unless the parent functional has a stationary local kernel.",
            status="GENERIC_RESIDUAL_THEOREM",
            consequence="the source wording pushes MTS into the harder branch unless a quotient/plateau/stationarity theorem is supplied",
        ),
        row(
            theorem_id="GVAR2140_4_fR_countermodel",
            object="curvature-functional counterexample",
            statement="For a toy Gamma_G=f(R), the metric variation gives f_R R_{mu nu} plus derivative terms (g_{mu nu} Box - nabla_mu nabla_nu) f_R; f(0)=0 does not force f_R(0)=0.",
            status="COUNTERMODEL_TO_ZEROTH_ORDER_ONLY",
            consequence="Gamma_G -> 0 is not enough; the local branch needs a double-zero/stationary-kernel condition",
        ),
        row(
            theorem_id="GVAR2140_5_nonlocal_history_kernel",
            object="history/coarse-graining kernel",
            statement="For Gamma_G(x)=H[bar R](x) with bar R(x)=int K(x,y)R(y)dV_y, delta Gamma_G carries a kernel integral over delta R(y) unless K, H', or support factors vanish on the local branch.",
            status="NONLOCAL_RESIDUAL_CONTRACT",
            consequence="local compact silence needs a source-backed kernel support theorem, not just a local value of Gamma_G",
        ),
        row(
            theorem_id="GVAR2140_6_bianchi_constraint",
            object="conservation consistency",
            statement="If the field equation is written as G_{mu nu}+Gamma_G g_{mu nu}=kappa T_{mu nu}, then Bianchi gives partial_nu Gamma_G = kappa nabla^mu T_{mu nu} unless the missing residual carries the exchange current.",
            status="CONSERVATION_GATE",
            consequence="a dynamic Gamma_G requires either matter-sector exchange, a residual operator, or a constant/local-silent Gamma_G branch",
        ),
        row(
            theorem_id="GVAR2140_7_verdict",
            object="Gamma_G variation proof status",
            statement="Current sources do not prove D_Gamma^{mu nu}=0, do not define the parent kernel, and do not prove boundary silence.",
            status="SILENCE_PROOF_NOT_CLOSED",
            consequence="stage finite Gamma_G residual rows and make the next target the functional/kernal contract",
        ),
    ]


def local_silence_rows() -> list[dict[str, object]]:
    return [
        row(clause_id="LS2140_0_zeroth_order", clause="Gamma_G local value", required_condition="Gamma_G|_U=0 or negligible in the local compact branch", current_evidence="raw source says pure GR recovered when Gamma_G -> 0", status="SOURCE_CONDITIONAL_ONLY", missing_piece="source does not prove how Gamma_G reaches zero for local systems"),
        row(clause_id="LS2140_1_first_variation", clause="first metric variation", required_condition="D_Gamma^{mu nu}|_U=0 for allowed local metric/coframe variations", current_evidence="raw source assumes independence of metric variation", status="UNSIGNED", missing_piece="no parent functional derivative or double-zero theorem"),
        row(clause_id="LS2140_2_boundary", clause="boundary/history term", required_condition="Theta_Gamma boundary term and nonlocal history kernel have no local compact projection", current_evidence="no source-backed compact-support theorem found in 2139", status="UNSIGNED", missing_piece="kernel support/localization theorem"),
        row(clause_id="LS2140_3_bianchi", clause="Bianchi/conservation", required_condition="nabla^mu E^Gamma_{mu nu}=0 or matched exchange current", current_evidence="dynamic Gamma_G is claimed but exchange current is not derived here", status="UNSIGNED", missing_piece="matter-exchange or residual-current closure"),
        row(clause_id="LS2140_4_source_bridge", clause="Newton/source bridge", required_condition="local source readout maps Gamma residual into bounded PPN/Newton/R10 quantities", current_evidence="2139 still marks source bridge missing", status="UNSIGNED", missing_piece="M_H_ref/Q_tau/G_ref source theorem"),
        row(clause_id="LS2140_5_verdict", clause="local GR silence", required_condition="all prior clauses pass", current_evidence="zeroth order is only conditional and first variation is open", status="LOCAL_SILENCE_NOT_PROVED", missing_piece="do not claim local GR/Newton/PPN pass from Gamma_G -> 0 alone"),
    ]


def residual_rows() -> list[dict[str, object]]:
    return [
        row(
            residual_id="GRES2140_0_DGamma_tensor",
            quantity="D_Gamma^{mu nu}",
            definition="coefficient of delta g_{mu nu} in delta Gamma_G after fixing the parent variation convention",
            expected_units="curvature scale, L^-2, modulo convention/factor kappa",
            status="MISSING_PARENT_FUNCTIONAL",
            needed_input="Gamma_G[g,psi,history] functional and smoothing kernel",
            target_arena="PPN/R10/clocks/orbital/local-GR",
        ),
        row(
            residual_id="GRES2140_1_boundary_kernel",
            quantity="Theta_Gamma^alpha",
            definition="boundary/history term produced by varying any nonlocal/coarse-grained Gamma_G functional",
            expected_units="boundary flux of curvature variation",
            status="MISSING_KERNEL_SUPPORT_THEOREM",
            needed_input="compact support, falloff, or quotient projection proof",
            target_arena="local vacuum/source matching",
        ),
        row(
            residual_id="GRES2140_2_exchange_current",
            quantity="J^Gamma_nu",
            definition="current required by nabla^mu(G_mu_nu+Gamma_G g_mu_nu+E^res_mu_nu)=kappa nabla^mu T_mu_nu",
            expected_units="force-density/curvature-gradient scale",
            status="MISSING_CONSERVATION_CLOSURE",
            needed_input="matter exchange law or proof partial_nu Gamma_G=0 in local branch",
            target_arena="Bianchi/WEP/clock/orbital",
        ),
        row(
            residual_id="GRES2140_3_local_PPN_vector",
            quantity="r_PPN^Gamma",
            definition="finite local post-Newtonian residual induced by D_Gamma, boundary kernel, or exchange current",
            expected_units="dimensionless PPN residual after normalization",
            status="STAGED_NONCLAIM",
            needed_input="source bridge and numerical/local bounds",
            target_arena="PPN/R10/local-GR",
        ),
        row(
            residual_id="GRES2140_4_decision",
            quantity="Gamma_G residual branch",
            definition="until D_Gamma=0 is parent-signed, treat Gamma_G as an unclosed finite residual rather than a proven local silence",
            expected_units="not applicable",
            status="RESIDUAL_ROW_REQUIRED",
            needed_input="2141 functional contract or kernel-zero proof",
            target_arena="all local claims",
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2140_0_sources", gate="2139 source handoff validates", gate_pass=True, rationale="2139 validation/action/gamma rows and raw action files exist"),
        row(gate_id="GATE2140_1_variation_identity", gate="variation decomposition written", gate_pass=True, rationale="2140 records exact conditional split between algebraic Gamma term and D_Gamma residual"),
        row(gate_id="GATE2140_2_external_scalar_branch", gate="external scalar branch is internally possible", gate_pass=True, rationale="if Gamma_G is prescribed and not varied, raw derivation is an effective-background branch"),
        row(gate_id="GATE2140_3_parent_derived_branch", gate="parent-derived Gamma_G branch closes", gate_pass=False, rationale="no functional/kernel/source theorem proves D_Gamma=0"),
        row(gate_id="GATE2140_4_local_silence", gate="local compact Gamma_G silence proved", gate_pass=False, rationale="Gamma_G=0 alone does not force first variation or boundary silence"),
        row(gate_id="GATE2140_5_conservation", gate="Bianchi/exchange current closed", gate_pass=False, rationale="dynamic Gamma_G requires exchange/residual or local constancy"),
        row(gate_id="GATE2140_6_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="D_Gamma, boundary kernel, conservation current, source bridge remain unsigned"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2140_0", decision="DO_NOT_USE_ZEROTH_ORDER_ONLY", because="Gamma_G -> 0 does not imply delta Gamma_G -> 0", next_action="require double-zero/stationary-kernel proof"),
        row(decision_id="DEC2140_1", decision="SPLIT_BRANCHES", because="external prescribed Gamma_G and parent-derived Gamma_G have different variation rules", next_action="label any external branch as effective, not fundamental"),
        row(decision_id="DEC2140_2", decision="STAGE_GAMMAG_RESIDUAL", because="current sources do not define the functional derivative kernel", next_action="carry D_Gamma, boundary kernel, and exchange current as finite residuals"),
        row(decision_id="DEC2140_3", decision="NEXT_FUNCTIONAL_CONTRACT", because="the next missing object is the actual Gamma_G[g,psi,history] parent definition", next_action="derive/source kernel-zero or residual coefficients in 2141"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2140_0_2141",
            next_target="2141-Y5-R2FR-GammaG-functional-contract-or-local-kernel-zero-proof.md",
            script="scripts/Y5_R2FR_GammaG_functional_contract_or_local_kernel_zero_proof_2141.py",
            objective="Write the exact parent functional contract for Gamma_G[g,psi,history]; either prove the local compact branch has Gamma_G=0, D_Gamma=0 and boundary/history-kernel silence, or retain sourced finite residual coefficients for PPN/R10/clocks/orbital tests.",
            forbidden_shortcuts="using Gamma_G->0 as first-variation proof; treating empirical redshift fit as a parent functional; hiding the exchange current in matter; local-GR/PPN/R10 claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    theory: list[dict[str, object]],
    silence: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2140_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_GAMMAG_VARIATION_2140_NONCLAIM.csv", theory + residuals + gates),
        ("COPY2140_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2140_GAMMAG_LOCAL_SILENCE_CHECKLIST_NONCLAIM.csv", silence + residuals),
        ("COPY2140_2_acquisition_queue", QUEUE / "JR2140_GAMMAG_FUNCTIONAL_CONTRACT_QUEUE.csv", next_rows + residuals),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    theory: list[dict[str, object]],
    silence: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    variation_ok = any(item["theorem_id"] == "GVAR2140_1_decomposition" and item["status"] == "EXACT_VARIATION_DECOMPOSITION" for item in theory)
    countermodel_ok = any(item["theorem_id"] == "GVAR2140_4_fR_countermodel" and item["status"] == "COUNTERMODEL_TO_ZEROTH_ORDER_ONLY" for item in theory)
    silence_rejected = any(item["clause_id"] == "LS2140_5_verdict" and item["status"] == "LOCAL_SILENCE_NOT_PROVED" for item in silence)
    residual_ok = any(item["residual_id"] == "GRES2140_4_decision" and item["status"] == "RESIDUAL_ROW_REQUIRED" for item in residuals)
    gates_ok = any(item["gate_id"] == "GATE2140_1_variation_identity" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2140_6_local_GR_Newton_PPN_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2140_3" and item["decision"] == "NEXT_FUNCTIONAL_CONTRACT" for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2140_0_2141" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, theory, silence, residuals, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2140_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, variation_ok, countermodel_ok, silence_rejected, residual_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2140_00_sources", sources_ok, "2139/raw Gamma_G source evidence validates"),
        ("VAL2140_01_variation_identity", variation_ok, "metric variation decomposition is recorded"),
        ("VAL2140_02_countermodel", countermodel_ok, "f(R)-style countermodel blocks zeroth-order-only proof"),
        ("VAL2140_03_silence_rejected", silence_rejected, "local silence proof remains unclosed"),
        ("VAL2140_04_residual", residual_ok, "finite Gamma_G residual row is staged"),
        ("VAL2140_05_gates", gates_ok, "variation identity passes while local-GR claim gate fails"),
        ("VAL2140_06_decisions", decisions_ok, "decision ledger selects functional contract next"),
        ("VAL2140_07_next", next_ok, "next target is 2141"),
        ("VAL2140_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2140_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2140_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2140_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2140"),
        ("VAL2140_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2140_OVERALL", all_ok, "2140 derives the Gamma_G variation contract, rejects Gamma_G->0 as sufficient proof, stages finite residuals, and selects the functional/kernel proof next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    theory: list[dict[str, object]],
    silence: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2140 - Y5/R2FR GammaG Metric Variation Local Silence Or Residual Row",
            "## Current Verdict",
            "2140 sharpens the 2139 result. The raw action source is useful, but the claimed algebraic `Gamma_G g_{mu nu}` contribution is only automatic in the external-scalar branch where `delta Gamma_G=0` is imposed during metric variation.",
            "If `Gamma_G` is really a scalar functional of smoothed curvature/history, then varying the action produces an extra residual operator. In compact notation, `delta Gamma_G = D_Gamma^{mu nu} delta g_{mu nu} + div(Theta_Gamma)`. Local GR therefore needs the double condition `Gamma_G=0` and `D_Gamma^{mu nu}=0`, plus boundary/history-kernel silence. The current corpus has the zeroth-order statement but not the first-variation proof.",
            "So this is progress but not a local-GR pass. The clean route is now explicit: define the parent functional `Gamma_G[g,psi,history]`, then prove its local kernel is stationary/silent, or carry `D_Gamma`, the boundary kernel, and the exchange current as finite residuals into PPN/R10/clocks/orbital tests.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Variation Identities",
            md_table(theory, ["theorem_id", "object", "statement", "status", "consequence", "valid_for_claim"]),
            "## Local Silence Checklist",
            md_table(silence, ["clause_id", "clause", "required_condition", "current_evidence", "status", "missing_piece", "valid_for_claim"]),
            "## Residual Rows",
            md_table(residuals, ["residual_id", "quantity", "definition", "expected_units", "status", "needed_input", "target_arena", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "gate", "gate_pass", "rationale", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    theory = variation_identity_rows()
    silence = local_silence_rows()
    residuals = residual_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2140_SOURCE_REGISTER.csv",
        "theory": OUT / "P8_Y5_PARENT_QLOC_2140_GAMMAG_VARIATION_IDENTITIES.csv",
        "silence": OUT / "P8_Y5_PARENT_QLOC_2140_LOCAL_SILENCE_CHECKLIST.csv",
        "residuals": OUT / "P8_Y5_PARENT_QLOC_2140_GAMMAG_RESIDUAL_ROWS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2140_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2140_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2140_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2140_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2140_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["theory"], theory)
    write_csv(paths["silence"], silence)
    write_csv(paths["residuals"], residuals)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(theory, silence, residuals, gates, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, theory, silence, residuals, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, theory, silence, residuals, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()

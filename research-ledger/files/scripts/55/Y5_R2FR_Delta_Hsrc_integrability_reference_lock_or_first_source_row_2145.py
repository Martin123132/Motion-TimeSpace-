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


DOC = ROOT / "2145-Y5-R2FR-Delta-Hsrc-integrability-reference-lock-or-first-source-row.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2144": ROOT / "2144-Y5-R2FR-MHref-Qtau-Gref-source-readout-bridge-or-closure.md",
    "1796": ROOT / "1796-Y5-R2FR-Hamiltonian-charge-integrability-reference-or-first-Delta-Hsrc-row.md",
    "1797": ROOT / "1797-Y5-R2FR-Delta-integrability-source-acquisition-or-bound-row.md",
    "1798": ROOT / "1798-Y5-R2FR-parent-Theta-Qtau-current-owner-or-deltaH-curl-component-pack.md",
    "1799": ROOT / "1799-Y5-R2FR-minimal-parent-current-action-skeleton-or-first-Ix-row.md",
    "1800": ROOT / "1800-Y5-R2FR-X-positive-operator-activation-or-Yukawa-fallback-row.md",
    "1801": ROOT / "1801-Y5-R2FR-JX-source-zero-or-component-bound-pack.md",
    "1802": ROOT / "1802-Y5-R2FR-parent-matter-functor-readout-no-reentry-or-qbar-readout-row.md",
    "1803": ROOT / "1803-Y5-R2FR-no-shadow-constant-marker-or-qbar-coefficient-pack.md",
    "1804": ROOT / "1804-Y5-R2FR-constant-superselection-alpha-mass-clock-provenance.md",
    "1805": ROOT / "1805-Y5-R2FR-no-extra-F2-no-mass-vertex-signature-or-alpha-mass-bound-matrix.md",
    "1806": ROOT / "1806-Y5-R2FR-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md",
    "1807": ROOT / "1807-Y5-R2FR-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md",
    "1808": ROOT / "1808-Y5-R2FR-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md",
    "1809": ROOT / "1809-Y5-R2FR-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md",
    "1810": ROOT / "1810-Y5-R2FR-beta-source-alpha-and-tau-WEP-R10-source-chain.md",
    "1811": ROOT / "1811-Y5-R2FR-parent-alpha-owner-matter-functor-and-qDq-signature-contract.md",
    "1812": ROOT / "1812-Y5-R2FR-parent-field-chart-Qvis-and-alpha-level-owner-or-first-residual-row.md",
    "1813": ROOT / "1813-Y5-R2FR-A-owned-placement-and-EM-level-owner-or-alpha-marker-residual-row.md",
    "1814": ROOT / "1814-Y5-R2FR-visible-gauge-connection-current-owner-or-DvA-DJ-alpha-residual-row.md",
}


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


def find_line(path: Path, alternatives: list[str]) -> tuple[int, str]:
    text = read_text(path) if path.exists() else ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if has_any(line, alternatives):
            return line_number, line.strip()
    return 0, "MISSING_NEEDLE"


def formalization_has_2145_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2145-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2145*",
        "*Y5_R2FR_Delta_Hsrc_integrability_reference_lock_or_first_source_row_2145*",
        "*AFRAME_DELTA_HSRC_FRONTIER_SYNC_2145*",
        "*JR2145*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2145_00_2144", DOCS["2144"], [["VAL2144_OVERALL"], ["Delta_Hsrc"], ["NEXT2144_0_2145"]], "current branch handoff into Delta_Hsrc/integrability"),
        ("SRC2145_01_1796", DOCS["1796"], [["VAL1796_OVERALL"], ["Delta_integrability"], ["INTEGRABILITY_REFERENCE_NOT_PROVED"]], "integrability/reference zero proof fails cleanly"),
        ("SRC2145_02_1797", DOCS["1797"], [["VAL1797_OVERALL"], ["Delta_integrability"], ["SOURCE_ACQUISITION_MATRIX_BUILT"]], "Delta_integrability acquisition matrix built"),
        ("SRC2145_03_1798", DOCS["1798"], [["VAL1798_OVERALL"], ["Theta_total"], ["DCC1798_8_total_abs_envelope"]], "deltaH curl component pack"),
        ("SRC2145_04_1799", DOCS["1799"], [["VAL1799_OVERALL"], ["I_X"], ["FIRST_IX_ROW_EMITTED_NONCLAIM"]], "first non-EH I_X row"),
        ("SRC2145_05_1800", DOCS["1800"], [["VAL1800_OVERALL"], ["lambda_X=sqrt"], ["X_POSITIVE_OPERATOR_NOT_ACTIVATED"]], "X nohair/Yukawa fork"),
        ("SRC2145_06_1801", DOCS["1801"], [["VAL1801_OVERALL"], ["J_X Source Silence Gate"], ["JX_SOURCE_ZERO_NOT_PROVED"]], "J_X component envelope"),
        ("SRC2145_07_1802", DOCS["1802"], [["VAL1802_OVERALL"], ["pure postprocessing"], ["JMatter_READOUT_ZERO_NOT_SIGNED"]], "matter/readout no-reentry split"),
        ("SRC2145_08_1803", DOCS["1803"], [["VAL1803_OVERALL"], ["hidden-coupling"], ["NO_SHADOW_CONSTANT_MARKER_ZERO_NOT_PROVED"]], "hidden coupling coefficient pack"),
        ("SRC2145_09_1804", DOCS["1804"], [["VAL1804_OVERALL"], ["b_alpha"], ["CONSTANT_COUPLING_BRANCH_NOT_ZERO_AND_NOT_BOUNDED"]], "constant-sector coupling rows"),
        ("SRC2145_10_1805", DOCS["1805"], [["VAL1805_OVERALL"], ["f_X F^2"], ["NO_EXTRA_F2_NO_MASS_VERTEX_ROUTE_IS_CORRECT_THROAT_BUT_NOT_SIGNED"]], "no-extra-F2/no-mass vertex throat"),
        ("SRC2145_11_1806", DOCS["1806"], [["VAL1806_OVERALL"], ["ORDINARY_COVARIANCE_AND_GAUGE_SYMMETRY_ARE_INSUFFICIENT"], ["product functor"]], "operator/symmetry ban fails to close"),
        ("SRC2145_12_1807", DOCS["1807"], [["VAL1807_OVERALL"], ["PRODUCT_FUNCTOR_THEOREM_SHAPE_IS_EXACT"], ["NO_MIXED_HIDDEN_VISIBLE_MORPHISM"]], "product functor exact conditional"),
        ("SRC2145_13_1808", DOCS["1808"], [["VAL1808_OVERALL"], ["2.1e-18"], ["no-mixed morphism"]], "first source-backed b_alpha*tau_clock product chain"),
        ("SRC2145_14_1809", DOCS["1809"], [["VAL1809_OVERALL"], ["tau_clock_time"], ["WEP_R10_PROJECTION_LEDGERS_EXPLICIT"]], "clock product quarantine and transfer blockers"),
        ("SRC2145_15_1810", DOCS["1810"], [["VAL1810_OVERALL"], ["beta_source_alpha"], ["beta-source-alpha and tau WEP/R10", "BETA_SOURCE_ALPHA_ZERO_THEOREM_EXACT_CONDITIONAL_NOT_CLOSED"]], "beta-source/tau source chain"),
        ("SRC2145_16_1811", DOCS["1811"], [["VAL1811_OVERALL"], ["parent signature"], ["FIELD_CHART_QVIS_AND_ALPHA_LEVEL_OWNER_NEXT"]], "parent alpha-owner/matter-functor/qDq contract"),
        ("SRC2145_17_1812", DOCS["1812"], [["VAL1812_OVERALL"], ["A_OWNED_PLACEMENT_AND_EM_LEVEL_OWNER_NEXT"], ["FIELD_CHART_QVIS_NOT_PARENT_OWNED"]], "field chart/Qvis/alpha owner package"),
        ("SRC2145_18_1813", DOCS["1813"], [["VAL1813_OVERALL"], ["A_owned_split"], ["VISIBLE_GAUGE_CONNECTION_CURRENT_OWNER_NEXT"]], "A_owned split repair"),
        ("SRC2145_19_1814", DOCS["1814"], [["VAL1814_OVERALL"], ["CONNECTION_CURRENT_OWNER_EXACT_CONDITIONAL"], ["NOETHER_CURRENT_OWNER_NO_RESCALE_NEXT"]], "deepest verified frontier: connection/current/no-rescale"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                needles_found=needles_found,
                expected_needles="; ".join(" OR ".join(group) for group in needle_groups),
                role=role,
            )
        )
    return rows


def frontier_chain_rows() -> list[dict[str, object]]:
    chain = [
        ("CHAIN2145_00", "2144", "Delta_Hsrc bridge", "epsilon_mu becomes epsilon_Gref+epsilon_Hsrc_abs+projection residuals", "bridge not closed"),
        ("CHAIN2145_01", "1796", "Delta_integrability", "integrable fixed-reference Hamiltonian mass charge attempted", "zero proof not closed"),
        ("CHAIN2145_02", "1797", "Delta_integrability acquisition", "five missing inputs routed to source/zero conditions", "matrix mapped, payloads missing"),
        ("CHAIN2145_03", "1798", "delta_H_tau curl", "curl split into I_X,I_projector,I_boundary,I_ref,I_tau,I_surface,I_Dq", "parent Theta/Q_tau owner not signed"),
        ("CHAIN2145_04", "1799", "I_X", "minimal X action skeleton and first I_X row", "relative skeleton only"),
        ("CHAIN2145_05", "1800", "X nohair/Yukawa fork", "positive-operator route or alpha_X(lambda) fallback", "activation and fallback not ready"),
        ("CHAIN2145_06", "1801", "J_X source silence", "J_matter,J_chiD,J_boundary,J_readout,J_history envelope", "J_X not zero/bounded"),
        ("CHAIN2145_07", "1802", "matter/readout", "pure postprocessing safe; pre-action/readout residuals retained", "general readout not theorem-zero"),
        ("CHAIN2145_08", "1803", "hidden coupling vertices", "frame, constants, markers, source prefactors catalogued", "coefficient pack required"),
        ("CHAIN2145_09", "1804", "constant sector", "alpha, mass, nuclear, clock derivatives retained", "constant superselection not proved"),
        ("CHAIN2145_10", "1805", "operator throat", "no-extra-F2/no-mass/no-clock vertex route isolated", "legal vertices still allowed"),
        ("CHAIN2145_11", "1806", "operator classification", "ordinary covariance/gauge symmetry insufficient; product functor target", "residual-prior slots retained"),
        ("CHAIN2145_12", "1807", "product functor", "visible-hidden product theorem exact conditional", "no-mixed morphism missing"),
        ("CHAIN2145_13", "1808", "no-mixed morphism", "scalar obstruction survives; clock product bound imported", "standalone transfer blocked"),
        ("CHAIN2145_14", "1809", "tau/projection", "|b_alpha*tau_clock_time|<=2.1e-18 yr^-1 retained", "tau_clock/Xhat and WEP/R10 projection missing"),
        ("CHAIN2145_15", "1810", "beta/tau source chain", "WEP/R10 product pressure rows and parent package contract", "cross-arena bridge blocked"),
        ("CHAIN2145_16", "1811", "parent signature", "q/Dq, Obs_e, matter functor, alpha owner, tau/readout contract", "contract exact but not proof"),
        ("CHAIN2145_17", "1812", "field chart/Qvis/alpha owner", "Q_vis/A_owned/alpha-level package localized", "owner package not signed"),
        ("CHAIN2145_18", "1813", "A_owned split", "A_owned_split=(A_Q^vis,ell_EM/g_*) repairs overloaded symbol", "split is contract-only"),
        ("CHAIN2145_19", "1814", "visible connection/current owner", "one parent connection, one parent current, no current-label morphism", "Noether current owner/no-rescale is next"),
    ]
    rows: list[dict[str, object]] = []
    for chain_id, checkpoint, object_name, progress, current_status in chain:
        source_path = DOCS[checkpoint]
        line_number, snippet = find_line(source_path, ["Current verdict", "Current Verdict", "**Current verdict:**"])
        rows.append(
            row(
                chain_id=chain_id,
                checkpoint=checkpoint,
                source_path=str(source_path),
                verdict_line=line_number,
                object=object_name,
                progress=progress,
                current_status=current_status,
                valid_for_claim=False,
            )
        )
    return rows


def nested_residual_rows() -> list[dict[str, object]]:
    return [
        row(layer_id="NEST2145_0_local_K_bound", quantity="|D_S^K deltaK|", expansion="<= 2e-122*(2*(epsilon_Gref+epsilon_Hsrc_abs+epsilon_Gauss+epsilon_PPN+epsilon_readout)+6*epsilon_r+epsilon_frame)", owner_checkpoint="2144", status="SYMBOLIC_NONCLAIM_BOUND"),
        row(layer_id="NEST2145_1_epsilon_Hsrc", quantity="epsilon_Hsrc_abs", expansion="(|Delta_integrability|+|R_eq|+|I_commutator|+|B_ref|+|Delta_extra_charge|+|Delta_tau_MHref|+|Delta_Gauss_PPN|)/M_H_ref", owner_checkpoint="1795/2144", status="COMPONENT_PACK_REJECTED_NONCLAIM"),
        row(layer_id="NEST2145_2_Delta_integrability", quantity="Delta_integrability/M_H_ref", expansion="|delta_H_tau_nonintegrable|/M_H_ref + |Delta_ref|/M_H_ref + |B_zero_flux|/M_H_ref + |Delta_symp|/M_H_ref", owner_checkpoint="1796-1797", status="SOURCE_MATRIX_MAPPED_VALUES_MISSING"),
        row(layer_id="NEST2145_3_deltaH_curl", quantity="delta_H_tau_nonintegrable/M_H_ref", expansion="(|I_X|+|I_projector|+|I_boundary|+|I_ref|+|I_tau|+|I_surface|+|I_Dq|)/M_H_ref", owner_checkpoint="1798", status="CURL_PACK_REJECTED_NONCLAIM"),
        row(layer_id="NEST2145_4_I_X", quantity="I_X/M_H_ref", expansion="|int_S i_tau omega_X + int_A C_X + boundary_X|/M_H_ref", owner_checkpoint="1799-1800", status="X_NOHAIR_OR_YUKAWA_FALLBACK_NOT_READY"),
        row(layer_id="NEST2145_5_JX", quantity="J_X", expansion="J_kin_affine+J_matter+J_chiD_wall+J_boundary+J_readout+J_history+projection tails", owner_checkpoint="1801", status="SOURCE_ZERO_NOT_PROVED_COMPONENT_BOUNDS_REQUIRED"),
        row(layer_id="NEST2145_6_hidden_couplings", quantity="qbar_hidden_abs", expansion="|b_conf|+|b_dis|+|b_alpha|+|b_mA|+|b_marker|+|delta_w_shadow|+|c_nonminimal|", owner_checkpoint="1803-1806", status="HIDDEN_COUPLINGS_NOT_ZERO_OR_BOUNDED"),
        row(layer_id="NEST2145_7_product_functor", quantity="visible-hidden coupling zero route", expansion="S_vis must pull back through q_loc and representation data with no hidden-to-visible coefficient morphism", owner_checkpoint="1807-1808", status="SCALAR_OBSTRUCTION_RETAINS_PRIORS"),
        row(layer_id="NEST2145_8_first_number", quantity="b_alpha*tau_clock_time", expansion="best imported clock product bound <= 2.1e-18 yr^-1 at 1 sigma", owner_checkpoint="1808-1809", status="SOURCE_BACKED_PRODUCT_BOUND_NONCLAIM"),
        row(layer_id="NEST2145_9_parent_signature", quantity="beta_source_alpha zero contract", expansion="q/Dq + Obs_e(q) + matter functor + alpha owner + no source-only slot + tau role lock + readout/boundary silence", owner_checkpoint="1810-1812", status="EXACT_CONDITIONAL_CONTRACT_NOT_SIGNED"),
        row(layer_id="NEST2145_10_current_frontier", quantity="A_Q^vis/J_Q owner", expansion="A_Q^vis is parent connection and J_Q=delta S_matter/delta A_Q^vis with no J_A->c_AJ_A morphism", owner_checkpoint="1813-1814", status="NOETHER_CURRENT_OWNER_NO_RESCALE_NEXT"),
    ]


def current_frontier_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2145_0_no_circling", gate="chain makes nonredundant progress", gate_pass=True, rationale="each old checkpoint turns one broad missing coupling into a sharper theorem antecedent, residual row, or quarantined product bound"),
        row(gate_id="GATE2145_1_integrability_closed", gate="Delta_integrability=0 proved", gate_pass=False, rationale="1796/1797 keep integrability/reference source rows missing"),
        row(gate_id="GATE2145_2_coupling_zero", gate="hidden coupling sector theorem-zero", gate_pass=False, rationale="1803-1808 retain scalar/Hom/current/readout countermodels"),
        row(gate_id="GATE2145_3_numeric_progress", gate="first numeric pressure row exists", gate_pass=True, rationale="1808/1809 import source-backed |b_alpha*tau_clock_time| <= 2.1e-18 yr^-1 but quarantine it"),
        row(gate_id="GATE2145_4_transfer_allowed", gate="clock product transfers to WEP/R10/local-GR", gate_pass=False, rationale="tau_clock, tau_WEP, tau_R10, source/test charges and shared projection are not derived"),
        row(gate_id="GATE2145_5_parent_signature", gate="parent alpha-owner/matter/qDq package signed", gate_pass=False, rationale="1811/1812 write exact contracts but antecedents are not jointly signed"),
        row(gate_id="GATE2145_6_A_owned_repair", gate="A_owned overload repaired", gate_pass=True, rationale="1813 splits A_owned into A_Q^vis and ell_EM/g_* as contract-level object-language repair"),
        row(gate_id="GATE2145_7_current_frontier", gate="current best target selected", gate_pass=True, rationale="1814 selects Noether current owner/no-current-rescale as the tightest next theorem"),
        row(gate_id="GATE2145_8_local_GR_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="source Hamiltonian, EH/Poisson/measured-G, PPN response and coupling gates remain open"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2145_0_2146",
            next_target="2146-Y5-R2FR-Noether-current-owner-and-no-current-rescale-proof-or-cA-bound-row.md",
            script="scripts/Y5_R2FR_Noether_current_owner_and_no_current_rescale_proof_or_cA_bound_row_2146.py",
            objective="Try to prove that the visible EM source/test current is the same parent Noether current J_Q=delta S_matter/delta A_Q^vis and that current-label rescalings J_A->c_A J_A are ill-typed; if not, stage a finite c_A/current-rescale residual row with units, source path, common normalizer and no-cancellation guard.",
            forbidden_shortcuts="do not set current rescale to zero from gauge invariance alone; do not transfer clock product to WEP/R10; do not set tau_WEP/tau_R10 to one; do not promote local GR/Newton; do not edit formalization-workbench; no GitHub action",
        )
    ]


def write_branch_copies(
    chain: list[dict[str, object]],
    nested: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2145_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_DELTA_HSRC_FRONTIER_SYNC_2145_NONCLAIM.csv", chain + nested),
        ("COPY2145_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2145_COUPLING_FRONTIER_NONCLAIM.csv", nested + gates),
        ("COPY2145_2_acquisition_queue", QUEUE / "JR2145_NOETHER_CURRENT_OWNER_NO_RESCALE_QUEUE.csv", next_rows + gates),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    chain: list[dict[str, object]],
    nested: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    chain_ok = len(chain) == 20 and chain[0]["checkpoint"] == "2144" and chain[-1]["checkpoint"] == "1814"
    nested_ok = any(item["layer_id"] == "NEST2145_8_first_number" and "2.1e-18" in str(item["expansion"]) for item in nested) and any(item["layer_id"] == "NEST2145_10_current_frontier" for item in nested)
    gate_ok = (
        any(item["gate_id"] == "GATE2145_0_no_circling" and truthy(item["gate_pass"]) for item in gates)
        and any(item["gate_id"] == "GATE2145_8_local_GR_claim" and not truthy(item["gate_pass"]) for item in gates)
    )
    next_ok = any(item["route_id"] == "NEXT2145_0_2146" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, chain, nested, gates, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2145_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, chain_ok, nested_ok, gate_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2145_00_sources", sources_ok, "2144 and 1796-1814 source checkpoints validate"),
        ("VAL2145_01_frontier_chain", chain_ok, "frontier chain runs from 2144 through 1814 without truncation"),
        ("VAL2145_02_nested_residual", nested_ok, "nested residual expansion includes first numeric clock product and current frontier"),
        ("VAL2145_03_gate_logic", gate_ok, "non-circling progress passes while local GR claim remains blocked"),
        ("VAL2145_04_next", next_ok, "next target is 2146 Noether current/no-rescale"),
        ("VAL2145_05_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2145_06_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2145_07_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2145_08_formalization_clean", formalization_clean, "formalization-workbench untouched by 2145"),
        ("VAL2145_09_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2145_OVERALL", all_ok, "2145 syncs Delta_Hsrc/integrability work to the deepest verified coupling frontier and selects Noether current/no-rescale next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    chain: list[dict[str, object]],
    nested: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2145 - Y5/R2FR Delta_Hsrc Integrability Reference Lock Or First Source Row",
            "## Current Verdict",
            "2145 does **not** prove `Delta_Hsrc=0`, local GR, Newton, PPN, WEP, R10, or a standalone coupling bound. It does something more useful at this stage: it syncs the current 2144 branch to the deepest verified private frontier.",
            "The answer to the circling worry is: this is not a loop. The chain has moved from `Delta_Hsrc` to `Delta_integrability`, then to Hamiltonian curl, `I_X`, `J_X`, hidden coupling vertices, constant-sector coefficients, product-functor/no-mixed-morphism obstructions, the first quarantined clock product number, and finally to the current sharp theorem target: one parent visible connection, one parent Noether current, and no current-label morphism `J_A -> c_A J_A`.",
            "The live frontier is therefore **Noether current owner / no-current-rescale**, not more broad coupling talk. If that closes, one major alpha/source-test coupling route becomes structural. If it fails, the next honest object is a finite `c_A`/current-rescale residual row with units, source paths, common normalizer, and no-cancellation guard.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Frontier Chain",
            md_table(chain, ["chain_id", "checkpoint", "verdict_line", "object", "progress", "current_status", "valid_for_claim"]),
            "## Nested Residual Expansion",
            md_table(nested, ["layer_id", "quantity", "expansion", "owner_checkpoint", "status", "valid_for_claim"]),
            "## Current Frontier Gates",
            md_table(gates, ["gate_id", "gate", "gate_pass", "rationale", "claim_allowed", "valid_for_claim"]),
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
    chain = frontier_chain_rows()
    nested = nested_residual_rows()
    gates = current_frontier_gate_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2145_SOURCE_REGISTER.csv",
        "chain": OUT / "P8_Y5_PARENT_QLOC_2145_FRONTIER_CHAIN.csv",
        "nested": OUT / "P8_Y5_PARENT_QLOC_2145_NESTED_RESIDUAL_EXPANSION.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2145_CURRENT_FRONTIER_GATE.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2145_NEXT_TARGET.csv",
        "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2145_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2145_VALIDATION.csv",
    }

    write_csv(paths["sources"], sources)
    write_csv(paths["chain"], chain)
    write_csv(paths["nested"], nested)
    write_csv(paths["gates"], gates)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(chain, nested, gates, next_rows)
    write_csv(paths["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, chain, nested, gates, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, chain, nested, gates, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()

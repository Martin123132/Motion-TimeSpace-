from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1031_0_1030_next", "source-intake/mts_residuals/P8_Y5_R10_1030_NEXT_TARGET.csv", "1031-Y5-R10-quotient-naturality", "1030 handoff to terminal public metric proof."),
        ("SRC1031_1_1030_derivation", "source-intake/mts_residuals/P8_Y5_R10_1030_SINGLE_PUBLIC_METRIC_DERIVATION_AUDIT.csv", "SPD1030_5_quotient_naturality_route", "1030 identifies quotient naturality as best route."),
        ("SRC1031_2_1030_contract", "source-intake/mts_residuals/P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv", "SPM1030_6_contract_verdict", "1030 single-public-metric contract."),
        ("SRC1031_3_1030_countermodels", "source-intake/mts_residuals/P8_Y5_R10_1030_COUNTERMODEL_LEDGER.csv", "CM1030_0_common_Jordan_frame", "1030 common-frame countermodel."),
        ("SRC1031_4_1030_provenance", "source-intake/mts_residuals/P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv", "CPG1030_2_tau_R10", "1030 c_g/tau provenance bindings."),
        ("SRC1031_5_1029_theorem", "source-intake/mts_residuals/P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv", "NST1029_1_chain_rule_zero", "1029 c_g chain-rule theorem."),
        ("SRC1031_6_1029_counterexamples", "source-intake/mts_residuals/P8_Y5_R10_1029_COUNTEREXAMPLE_LEDGER.csv", "CE1029_1_einstein_jordan_relabel", "1029 frame-relabel counterexample."),
        ("SRC1031_7_1029_intake", "source-intake/mts_residuals/P8_Y5_R10_1029_CG_INTAKE_TEMPLATE.csv", "CGI1029_1_finite_cg_R10", "1029 c_g intake template."),
        ("SRC1031_8_1029_tau", "source-intake/mts_residuals/P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv", "TAU1029_0_R10", "1029 tau projection requirements."),
        ("SRC1031_9_943_contract", "source-intake/mts_residuals/P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv", "CFC943_1_observed_coframe_descent", "943 observed-coframe descent contract."),
        ("SRC1031_10_945_qmap", "source-intake/mts_residuals/P8_Y5_R10_945_Q_MAP_CANDIDATE_CONSTRUCTION.csv", "QMAP945_6_verdict", "945 q_candidate is notation not proof."),
        ("SRC1031_11_945_obs", "source-intake/mts_residuals/P8_Y5_R10_945_OBS_E_FUNCTOR_AUDIT.csv", "OBS945_1_Q_only_multiple_frames", "945 multiple q-only frames warning."),
        ("SRC1031_12_945_kernel", "source-intake/mts_residuals/P8_Y5_R10_945_KERNEL_TEST.csv", "KT945_6_total_kernel", "945 kernel certificate failure."),
        ("SRC1031_13_956_spine", "source-intake/mts_residuals/P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv", "SSG956_0_observed_coframe", "956 source-side GR/Newton spine."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="ignore") if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def terminal_metric_proof_rows() -> list[dict[str, str]]:
    return [
        {
            "proof_id": "TPM1031_0_define_category",
            "target": "define ordinary-observable quotient category",
            "mathematical_form": "Q_obs has objects equal to parent-quotient-owned ordinary readout structures; morphisms preserve rods, clocks, photons, free fall, and source readout",
            "result": "DEFINITION_CANDIDATE",
            "would_prove": "sets the domain in which a public metric object can be tested",
            "failure_mode": "object class is chosen, not derived, unless parent action supplies the ordinary interface category",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "TPM1031_1_terminal_object",
            "target": "terminal public metric/coframe object",
            "mathematical_form": "there exists e_pub in Q_obs such that for every ordinary frame E in Q_obs there is a unique observable-equivalence morphism E -> e_pub",
            "result": "CONDITIONAL_UNIVERSAL_PROPERTY_WRITTEN",
            "would_prove": "all q-owned ordinary frames have one public readout representative",
            "failure_mode": "terminality alone does not prove matter action ignores the non-terminal object E before mapping to e_pub",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "TPM1031_2_matter_interface_functor",
            "target": "ordinary matter action factors through terminal evaluation",
            "mathematical_form": "S_matter = Sbar[Psi, Eval(e_pub(q(Phi))), theta(q)] and not Sbar[Psi,E(q),extra labels]",
            "result": "NEEDED_EXTRA_PREMISE",
            "would_prove": "matter/readout cannot access a shadow frame slot even if other q-owned structures exist",
            "failure_mode": "a functor can depend on E or labels before applying the unique map E -> e_pub",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "TPM1031_3_vertical_chain_rule",
            "target": "c_g zero if shadow frame is not an ordinary argument",
            "mathematical_form": "A_g absent => c_g undefined/zero; A_g=Abar(q) and Dq[v_X]=0 => Lie_vX ln A_g=0",
            "result": "CONDITIONAL_THEOREM_VALID",
            "would_prove": "no representative Weyl c_g when TPM1031_0 through TPM1031_2 are parent-signed",
            "failure_mode": "q-kernel ownership and A_g factorization still must be parent-signed",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "TPM1031_4_field_rename_guard",
            "target": "terminal metric cannot hide frame dependence in constants/source normalization",
            "mathematical_form": "same parent ledger for e_pub, theta_A, alpha_EM, G_eff, T_total, support, and clock readout",
            "result": "REQUIRED_GUARD",
            "would_prove": "prevents moving c_g into b_A, b_alpha, q_nonH, or Delta_W_support",
            "failure_mode": "terminal e_pub alone does not control constants, non-Hilbert currents, or measured-GM calibration",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "TPM1031_5_terminality_insufficiency",
            "target": "test whether terminal object alone proves no-shadow frame",
            "mathematical_form": "Category may have terminal e_pub while S_matter[Psi,E(q),theta] depends on non-terminal E or an E-labelled natural transformation",
            "result": "FAILS_AS_STANDALONE_PROOF",
            "would_prove": "nothing claimable without matter-interface restriction",
            "failure_mode": "terminal object is a universal morphism property, not an action-domain exclusion",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "TPM1031_6_verdict",
            "target": "terminal public metric proof of single-public-metric route",
            "mathematical_form": "Q_obs terminal e_pub + matter-interface functor through e_pub + field-rename guard + q-kernel ownership => no A_g shadow-frame slot",
            "result": "NOT_DERIVED_CURRENT_CORPUS",
            "would_prove": "c_g=0 and same-frame source/readout as a theorem",
            "failure_mode": "current corpus has the closure contract but not the parent derivation of Q_obs/object class/matter-interface restriction",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def insufficiency_counterexample_rows() -> list[dict[str, str]]:
    return [
        {
            "counterexample_id": "TC1031_0_terminal_but_functor_uses_E",
            "premise_satisfied": "Q_obs has terminal e_pub",
            "construction": "objects E_A(q) map uniquely to e_pub, but S_A[Psi_A,E_A(q),theta_A] is evaluated before the terminal map",
            "what_breaks": "matter can still see species/readout frames",
            "required_repair": "matter action domain must be terminal-evaluation only",
            "blocks_terminal_proof": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "TC1031_1_terminal_with_labels",
            "premise_satisfied": "unique morphism to e_pub exists",
            "construction": "objects carry labels or natural-transformation data L with unique L -> terminal but S_matter depends on L",
            "what_breaks": "source weights, constants, or marker couplings survive terminality",
            "required_repair": "ordinary matter functor must forget non-public labels before action evaluation",
            "blocks_terminal_proof": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "TC1031_2_terminal_after_frame_rename",
            "premise_satisfied": "metric object is terminal",
            "construction": "choose e_pub as terminal metric but move A_g(Xhat) into m_A(Xhat), alpha_EM(Xhat), or G_eff(Xhat)",
            "what_breaks": "c_g zero becomes b_A/b_alpha/source-normalization residual",
            "required_repair": "field-rename guard across geometry, constants, active source, and clocks",
            "blocks_terminal_proof": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "TC1031_3_terminal_not_kernel_owned",
            "premise_satisfied": "e_pub is selected as public object",
            "construction": "Dq-kernel directions are not presymplectic-null or boundary-silent",
            "what_breaks": "vertical representative motion is physical and can still source finite coupling",
            "required_repair": "q-kernel ownership certificate",
            "blocks_terminal_proof": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def spm_closure_rows() -> list[dict[str, str]]:
    return [
        {
            "closure_id": "SPMC1031_0_closure_name",
            "closure": "Single Public Metric closure",
            "mathematical_form": "ordinary S_matter and readout are restricted by closure to Sbar[Psi,e_pub(q),omega[e_pub],theta(q)]",
            "role": "explicit closure if terminal proof is not derived",
            "status": "AVAILABLE_AS_CLOSURE_ONLY",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "closure_id": "SPMC1031_1_cg_effect",
            "closure": "c_g under SPM closure",
            "mathematical_form": "A_g shadow-frame slot excluded by closure, so c_g=0 only inside the closure branch",
            "role": "conditional branch simplification",
            "status": "NOT_PARENT_THEOREM",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "closure_id": "SPMC1031_2_remaining_residuals",
            "closure": "what SPM closure does not close",
            "mathematical_form": "b_A, b_alpha, b_dis, q_nonH, Delta_W_support, measured-GM, and left-hand EH/Newton gates remain separate unless included",
            "role": "anti-overclaim rule",
            "status": "RETAIN_RESIDUALS",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "closure_id": "SPMC1031_3_public_use_policy",
            "closure": "publication policy",
            "mathematical_form": "SPM may be described as a closure/selection principle, not as a derived theorem",
            "role": "language discipline",
            "status": "PRIVATE_NONCLAIM",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def finite_cg_fallback_rows() -> list[dict[str, str]]:
    return [
        {
            "fallback_id": "FCG1031_0_cg_value",
            "quantity": "c_g",
            "needed_for": "R10/PPN/clock/common-frame finite branch",
            "required_evidence": "numeric c_g or parent-signed zero theorem with source path and derivation status",
            "current_status": "MISSING_PARENT_INPUT_OR_THEOREM",
            "source_hint": "P8_Y5_R10_1029_CG_INTAKE_TEMPLATE.csv:CGI1029_1_finite_cg_R10",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fallback_id": "FCG1031_1_tau_R10",
            "quantity": "tau_R10",
            "needed_for": "short-range alpha(lambda) projection",
            "required_evidence": "K_X(lambda), Qbar_XH, tau_R10, profile/source-test convention, bound curve link",
            "current_status": "MISSING_ARENA_PROJECTION",
            "source_hint": "P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv:TAU1029_0_R10",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fallback_id": "FCG1031_2_tau_PPN",
            "quantity": "tau_PPN",
            "needed_for": "PPN gamma/beta finite branch",
            "required_evidence": "M_gamma, M_beta, gauge/profile response matrix, disformal separation",
            "current_status": "MISSING_PPN_RESPONSE_MATRIX",
            "source_hint": "P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv:TAU1029_1_PPN_gamma_beta",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fallback_id": "FCG1031_3_no_cancellation",
            "quantity": "local envelope",
            "needed_for": "any local score",
            "required_evidence": "each retained component is theorem-zero or numeric/source-backed; no cancellation between unknowns",
            "current_status": "ABSOLUTE_ENVELOPE_REQUIRED",
            "source_hint": "P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv:CPG1030_4_no_cancellation",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE1031_0_sources",
            "claim": "all 1031 cited sources exist",
            "gate_pass": "true",
            "reason": "validated by source register",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1031_1_terminal_proof",
            "claim": "terminal public metric theorem is derived",
            "gate_pass": "false",
            "reason": "TPM1031_6 is not derived in current corpus",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1031_2_terminality_alone",
            "claim": "terminal object alone forbids shadow frames",
            "gate_pass": "false",
            "reason": "terminality does not exclude matter functors depending on non-terminal objects or labels",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1031_3_spm_closure",
            "claim": "SPM closure may be used as derived MTS theorem",
            "gate_pass": "false",
            "reason": "SPM is available only as explicit closure/selection principle unless parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1031_4_finite_cg",
            "claim": "finite c_g/tau branch can be scored",
            "gate_pass": "false",
            "reason": "c_g, tau_R10, and tau_PPN remain missing provenance/projection rows",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1031_5_local_GR",
            "claim": "local GR/Newton reduction is established",
            "gate_pass": "false",
            "reason": "right-hand SPM closure is nonclaim and left-hand EH/Newton/hidden residual gates remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1031_0_terminality_status",
            "decision": "Terminal public metric alone is insufficient.",
            "because": "a terminal object gives a unique morphism, but does not by itself restrict the matter action from using another object or label before the terminal map.",
            "next_action": "do not claim c_g=0 from terminality alone",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1031_1_exact_theorem_target",
            "decision": "The exact theorem target is stronger than terminality.",
            "because": "need Q_obs object class, terminal e_pub, matter-interface functor through e_pub only, field-rename guard, and q-kernel ownership.",
            "next_action": "treat these as the full SPM proof contract",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1031_2_closure_status",
            "decision": "Single Public Metric is demoted to explicit closure unless the full proof contract is parent-signed.",
            "because": "the current corpus has good closure language but not a derivation from deeper parent principles.",
            "next_action": "write future arguments as closure branch or continue finite c_g provenance",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1031_3_next_target",
            "decision": "Next target is SPM closure ledger plus finite c_g/tau acquisition.",
            "because": "the derivation route has reached its current boundary; the disciplined move is to keep closure explicit and make the finite branch testable.",
            "next_action": "1032-Y5-R10-spm-closure-ledger-and-finite-cg-tau-acquisition-runner.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1032-Y5-R10-spm-closure-ledger-and-finite-cg-tau-acquisition-runner.md",
            "objective": "formalize Single Public Metric as an explicit nonclaim closure branch and build the finite c_g/tau acquisition runner that refuses placeholder values but is ready for sourced R10 and PPN projections",
            "include": "SPM closure branch, c_g=0 only under closure, finite c_g intake, tau_R10, tau_PPN, R10 alpha(lambda), PPN gamma/beta, provenance gate, no-cancellation local envelope",
            "exclude": "claiming SPM is derived, terminality-only proof, WEP-only proof, invented c_g/tau values, cancellation between unknowns, R10/PPN/local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file():
            modified = datetime.fromtimestamp(candidate.stat().st_mtime, timezone.utc)
            if modified >= STARTED:
                changed.append(candidate)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    proof: list[dict[str, str]],
    counterexamples: list[dict[str, str]],
    closure: list[dict[str, str]],
    fallback: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    proof_required = {f"TPM1031_{idx}_{name}" for idx, name in [
        (0, "define_category"),
        (1, "terminal_object"),
        (2, "matter_interface_functor"),
        (3, "vertical_chain_rule"),
        (4, "field_rename_guard"),
        (5, "terminality_insufficiency"),
        (6, "verdict"),
    ]}
    closure_required = {f"SPMC1031_{idx}_{name}" for idx, name in [
        (0, "closure_name"),
        (1, "cg_effect"),
        (2, "remaining_residuals"),
        (3, "public_use_policy"),
    ]}
    fallback_required = {f"FCG1031_{idx}_{name}" for idx, name in [
        (0, "cg_value"),
        (1, "tau_R10"),
        (2, "tau_PPN"),
        (3, "no_cancellation"),
    ]}
    checks = [
        ("V1031_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all cited source paths exist and expected needles are present"),
        ("V1031_1_proof_rows_complete", proof_required.issubset({row["proof_id"] for row in proof}), "terminal metric proof audit covers category, terminal object, matter interface, chain rule, rename guard, insufficiency, and verdict"),
        ("V1031_2_terminality_insufficient", any(row["proof_id"] == "TPM1031_5_terminality_insufficiency" and row["result"] == "FAILS_AS_STANDALONE_PROOF" for row in proof), "terminality-alone proof is explicitly rejected"),
        ("V1031_3_theorem_not_claimed", any(row["proof_id"] == "TPM1031_6_verdict" and row["result"] == "NOT_DERIVED_CURRENT_CORPUS" for row in proof), "terminal public metric theorem remains nonclaim"),
        ("V1031_4_counterexamples_block", len(counterexamples) >= 4 and all(row["blocks_terminal_proof"] == "true" for row in counterexamples), "counterexamples block terminal-only proof"),
        ("V1031_5_closure_complete", closure_required.issubset({row["closure_id"] for row in closure}), "SPM closure rows cover closure name, c_g effect, residuals, and public-use policy"),
        ("V1031_6_closure_nonclaim", all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in closure), "SPM closure remains nonclaim"),
        ("V1031_7_fallback_complete", fallback_required.issubset({row["fallback_id"] for row in fallback}), "finite c_g fallback covers c_g value, tau_R10, tau_PPN, and no-cancellation"),
        ("V1031_8_fallback_unscoreable", all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in fallback), "finite branch refuses placeholder scoring"),
        ("V1031_9_claim_gates_blocked", all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in gates), "all claim gates refuse promotion"),
        ("V1031_10_decision_next", any(row["decision_id"] == "DEC1031_3_next_target" for row in decisions), "decision ledger selects the 1032 target"),
        ("V1031_11_next_target_written", len(next_target) == 1 and "1032-Y5-R10-spm-closure-ledger" in next_target[0]["next_target"], "1032 next target row is present"),
        ("V1031_12_no_overclaim", all(row.get("valid_for_claim", "false") == "false" for group in [sources, proof, counterexamples, closure, fallback, gates, decisions, next_target] for row in group), "all generated rows remain valid_for_claim=false"),
        ("V1031_13_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    passed_all = all(passed for _, passed, _ in checks)
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1031_SUMMARY", "result": "pass" if passed_all else "fail", "detail": "1031 terminal public metric proof or SPM closure validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    proof: list[dict[str, str]],
    counterexamples: list[dict[str, str]],
    closure: list[dict[str, str]],
    fallback: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1031 Y5 R10 quotient naturality terminal public metric proof or SPM closure",
            "",
            "**Status:** The terminal-public-metric route is sharpened but not derived. A terminal public metric/coframe object would help only if ordinary matter/readout functors are also parent-restricted to terminal evaluation. Terminality alone is not enough: a matter functor can still depend on a non-terminal frame, label, constant, or source normalization before mapping onward. Therefore the Single Public Metric route is demoted to an explicit nonclaim closure unless a stronger parent proof is supplied.",
            "",
            "**Claim ceiling:** no terminal-metric theorem, Single Public Metric theorem, `c_g=0`, finite-`c_g` score, R10, PPN, WEP, clock, orbital, local-GR/Newton, or source-side GR pass is allowed from 1031.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Terminal public metric proof audit",
            md_table(proof, ["proof_id", "target", "mathematical_form", "result", "would_prove", "failure_mode", "parent_signed", "valid_for_claim"]),
            "## Terminality insufficiency counterexamples",
            md_table(counterexamples, ["counterexample_id", "premise_satisfied", "construction", "what_breaks", "required_repair", "blocks_terminal_proof", "valid_for_claim"]),
            "## Single Public Metric closure branch",
            md_table(closure, ["closure_id", "closure", "mathematical_form", "role", "status", "claim_allowed", "valid_for_claim"]),
            "## Finite c_g/tau fallback",
            md_table(fallback, ["fallback_id", "quantity", "needed_for", "required_evidence", "current_status", "source_hint", "score_ready", "valid_for_claim"]),
            "## Claim gates",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Validation",
            md_table(validations, ["check_id", "result", "detail", "generated_utc"]),
            "## Next target",
            md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    proof = terminal_metric_proof_rows()
    counterexamples = insufficiency_counterexample_rows()
    closure = spm_closure_rows()
    fallback = finite_cg_fallback_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, proof, counterexamples, closure, fallback, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1031_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1031_TERMINAL_PUBLIC_METRIC_PROOF_AUDIT.csv", proof)
    write_csv(OUT / "P8_Y5_R10_1031_TERMINALITY_INSUFFICIENCY_COUNTEREXAMPLES.csv", counterexamples)
    write_csv(OUT / "P8_Y5_R10_1031_SPM_CLOSURE_BRANCH.csv", closure)
    write_csv(OUT / "P8_Y5_R10_1031_FINITE_CG_TAU_FALLBACK.csv", fallback)
    write_csv(OUT / "P8_Y5_R10_1031_CLAIM_GATES.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1031_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1031_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1031_VALIDATION.csv", validations)
    write_doc(sources, proof, counterexamples, closure, fallback, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()

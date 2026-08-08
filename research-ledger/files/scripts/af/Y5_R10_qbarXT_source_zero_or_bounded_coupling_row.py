from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md"
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
        ("SRC1027_0_1026_next", "source-intake/mts_residuals/P8_Y5_R10_1026_NEXT_TARGET.csv", "1027-Y5-R10-qbarXT", "1026 handoff to qbarXT source-zero or bounded coupling row."),
        ("SRC1027_1_1026_return", "source-intake/mts_residuals/P8_Y5_R10_1026_SOURCE_ZERO_RETURN.csv", "SZR1026_2_qbar_XT", "1026 source-zero return rows."),
        ("SRC1027_2_618_source_zero", "source-intake/mts_residuals/P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv", "SZ618_0_qbar_XT_chain_rule", "618 source-zero certificate."),
        ("SRC1027_3_565_pullback", "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md", "VT565_0_vertical_observation_theorem", "565 coframe pullback theorem and counterexamples."),
        ("SRC1027_4_566_nomarker", "566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md", "PQ566_2_matter_functor", "566 primitive quotient/no-marker clause."),
        ("SRC1027_5_567_alpha", "567-Y5-R10-finite-alpha-coefficient-fill-and-real-bound-curve-runner.md", "FA567_0_finite_alpha", "567 finite alpha coefficient fallback."),
        ("SRC1027_6_943_contract", "source-intake/mts_residuals/P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv", "CFC943_2_matter_functor", "943 coframe coupling contract."),
        ("SRC1027_7_944_descent", "source-intake/mts_residuals/P8_Y5_R10_944_DECISION_LEDGER.csv", "DEC944_0_descent", "944 quotient descent decision."),
        ("SRC1027_8_945_qmap", "source-intake/mts_residuals/P8_Y5_R10_945_Q_MAP_CANDIDATE_CONSTRUCTION.csv", "QMAP945_5_matter_invisibility", "945 q-map and matter invisibility gate."),
        ("SRC1027_9_945_bounds", "source-intake/mts_residuals/P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv", "BND945_0_cg_value", "945 first frame-leak bound row schema."),
        ("SRC1027_10_1012_source_norm", "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md", "Y5O1012_5_no_extra_mu_channels", "1012 source-normalization residual stack."),
        ("SRC1027_11_1025_alpha_schema", "source-intake/mts_residuals/P8_Y5_R10_1025_ALPHA_SOURCE_ROW_TEMPLATE.csv", "ASR1025_2_source_current", "1025 qbarXT source-current schema."),
        ("SRC1027_12_669_residual", "source-intake/mts_residuals/P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv", "RV669_3_qbar_XT", "669 qbarXT residual vector."),
        ("SRC1027_13_956_source_spine", "source-intake/mts_residuals/P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv", "SSG956_3_minimal_matter_action", "956 source-side GR/Newton spine."),
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


def source_zero_proof_rows() -> list[dict[str, str]]:
    return [
        {
            "proof_id": "QZ1027_0_chain_rule",
            "target": "qbar_XT=0/J_matter_pullback=0",
            "required_statement": "If X is vertical to q, e_obs=Obs_e(q(Phi)), S_matter=Sbar[psi,e_obs,theta_A], and Lie_vX theta_A=0, then Lie_vX S_matter=0.",
            "current_evidence": "565 and 618 prove the chain-rule shape conditionally.",
            "status": "CONDITIONAL_THEOREM_VALID",
            "missing_for_claim": "parent-signed q/v_X, observed coframe functor, matter functor, and no-marker constants",
            "if_missing": "retain qbar_XT as a finite source/test coupling",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "QZ1027_1_q_verticality",
            "target": "Dq[v_X]=0",
            "required_statement": "X is a representative/gauge direction in the parent configuration before variation, not a physical quotient observable.",
            "current_evidence": "945 writes q_candidate but says kernel ownership is not proved; 618 no-pole certificate remains not passed.",
            "status": "MISSING_PARENT_Q_KERNEL_CERTIFICATE",
            "missing_for_claim": "presymplectic-null kernel, boundary flux zero, and degree-count/no-pole proof",
            "if_missing": "ordinary matter can see an X-dependent observed-frame or source channel",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "QZ1027_2_observed_coframe",
            "target": "Lie_vX e_obs=0",
            "required_statement": "e_obs=Obs_e(q(Phi)) is parent-signed and no representative Weyl/disformal frame affects rods, clocks, masses, charges, or free fall.",
            "current_evidence": "943/944/945 keep observed coframe descent conditional and retain frame-leak rows.",
            "status": "MISSING_OBS_E_DESCENT_OR_FRAME_LEAK_ZERO",
            "missing_for_claim": "q/Obs_e parent signature and no-shadow-frame theorem or sourced frame-leak bounds",
            "if_missing": "qbar_XT can re-enter through common Weyl/disformal coupling",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "QZ1027_3_matter_functor",
            "target": "S_matter descends through observed variables only",
            "required_statement": "S_matter=sum_A S_A[psi_A,e_obs,omega[e_obs],theta_A] for all ordinary matter/readout species.",
            "current_evidence": "240/242/943/956 write the exact contract but keep parent selection unsigned.",
            "status": "EXACT_CONTRACT_NOT_PARENT_SIGNED",
            "missing_for_claim": "parent principle selecting strict local observed coframe and one matter/source/readout action",
            "if_missing": "matter action can contain a direct X-sensitive frame/source slot",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "QZ1027_4_no_marker_constants",
            "target": "Lie_vX theta_A=0",
            "required_statement": "material constants, masses, clocks, EM constants, and readout markers are quotient-owned/superselected, not vertical fields.",
            "current_evidence": "565/566/945 retain material-marker and species-marker counterexamples.",
            "status": "MISSING_NO_MARKER_THEOREM",
            "missing_for_claim": "constant/mass/EM/material-marker descent or numeric b_A/b_alpha bounds",
            "if_missing": "WEP may pass by species-blindness while common fifth-force/source-normalization still survives",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "QZ1027_5_hidden_source_tail",
            "target": "no hidden non-Hilbert/source/domain tail",
            "required_statement": "non-Hilbert current, support shift, boundary tail, domain projector, and source-normalization residuals are theorem-zero or bounded.",
            "current_evidence": "945 BND rows and 1012/956 source-side spine retain q_nonH, support, and hidden-source residuals.",
            "status": "MISSING_HIDDEN_SOURCE_ZERO_OR_BOUND",
            "missing_for_claim": "q_nonH, Delta_W_support, domain/boundary/source-normalization rows with units and source paths",
            "if_missing": "qbar_XT=0 for visible matter would still not silence total local source coupling",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "QZ1027_6_verdict",
            "target": "qbar_XT/J_X source-zero theorem",
            "required_statement": "QZ1027_1 through QZ1027_5 all close from the same parent branch.",
            "current_evidence": "conditional pieces exist, but no single parent certificate closes.",
            "status": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "q-kernel, observed coframe, matter functor, no-marker, hidden-source/boundary silence",
            "if_missing": "build bounded qbar_XT row and dependency chain",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def counterexample_rows() -> list[dict[str, str]]:
    return [
        {
            "counterexample_id": "CE1027_0_common_Weyl",
            "weak_premise": "universal covariant matter coupling",
            "construction": "e_m=A_g(X)e_obs or g_m=exp(2F(X))g_obs for all species",
            "failure": "WEP composition spread can vanish while qbar_XT is a common nonzero source charge",
            "required_repair": "prove A_g'(0)=0/no-shadow-frame theorem or source c_g/b_g bound",
            "blocks_zero_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1027_1_disformal_frame",
            "weak_premise": "single observed coframe notation",
            "construction": "g_m=A_g(X)^2g_obs+B_g(X)U_muU_nu",
            "failure": "preferred-frame/PPN/clock source can survive coframe projection",
            "required_repair": "disformal absence theorem or PPN/preferred-frame bound row",
            "blocks_zero_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1027_2_material_marker",
            "weak_premise": "matter geometry is X-blind",
            "construction": "theta_A(X), m_A(X), alpha_EM(X), or material class labels enter ordinary matter constants",
            "failure": "delta_X S_matter returns through constants even when partial_X e_obs=0",
            "required_repair": "no-marker theorem or material sensitivity b_A/b_alpha rows",
            "blocks_zero_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1027_3_nonHilbert_tail",
            "weak_premise": "Hilbert matter current is standard",
            "construction": "non-Hilbert current, boundary/source support shift, or domain/projector tail",
            "failure": "ordinary Hilbert qbar_XT may be zero while source-normalization residual remains",
            "required_repair": "q_nonH/Delta_W_support/source-tail theorem-zero or bound rows",
            "blocks_zero_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1027_4_frame_rename",
            "weak_premise": "choose e_obs as the matter frame",
            "construction": "rename the matter frame and move X-dependence into EH/operator/source calibration",
            "failure": "projection-by-declaration hides the same coupling in another sector",
            "required_repair": "parent q/Obs_e and full source-normalization ledger, not a field rename",
            "blocks_zero_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def bounded_qbar_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "BQT1027_0_visible_geometry",
            "symbol": "qbar_geom",
            "definition": "ordinary test-body X charge from representative Weyl/disformal observed-frame leakage",
            "formula_or_bound": "|qbar_geom| <= |tau_R10 c_g| + |tau_dis b_dis|",
            "required_columns": "system_id;test_body;lambda;tau_R10;c_g;tau_dis;b_dis;units;source_path;valid_for_claim",
            "current_status": "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND",
            "observable_link": "R10;PPN;clock",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "BQT1027_1_marker_constants",
            "symbol": "qbar_marker",
            "definition": "ordinary test-body X charge from masses, material constants, EM constants, or clock markers",
            "formula_or_bound": "|qbar_marker| <= sum_A |s_A b_A| + |s_alpha b_alpha|",
            "required_columns": "system_id;material_pair;species_sensitivities;b_A;b_alpha;units;source_path;valid_for_claim",
            "current_status": "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS",
            "observable_link": "WEP;clock;composition;R10",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "BQT1027_2_nonHilbert_tail",
            "symbol": "qbar_nonH",
            "definition": "test/source coupling from non-Hilbert current, boundary tail, support shift, or domain projector",
            "formula_or_bound": "|qbar_nonH| <= |q_nonH| + |Delta_W_support| + |q_domain| + |q_boundary|",
            "required_columns": "system_id;arena;q_nonH;Delta_W_support;q_domain;q_boundary;units;source_path;valid_for_claim",
            "current_status": "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND",
            "observable_link": "R10;orbital;source_normalization;local_GR",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "BQT1027_3_total_abs_guard",
            "symbol": "qbar_XT_bound_abs",
            "definition": "no-cancellation envelope for ordinary test-body X charge",
            "formula_or_bound": "|qbar_XT| <= |qbar_geom|+|qbar_marker|+|qbar_nonH|+|qbar_hidden|",
            "required_columns": "system_id;lambda;abs_qbar_geom;abs_qbar_marker;abs_qbar_nonH;abs_qbar_hidden;qbar_XT_bound_abs;units;source_paths;valid_for_claim",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "observable_link": "R10;WEP;clock;PPN;local_GR",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "BQT1027_4_claim_gate",
            "symbol": "qbar_XT_claim_gate",
            "definition": "qbar_XT may be zero-claimed or bound-claimed only after every component has theorem-zero or a numeric bound",
            "formula_or_bound": "valid_for_claim=true only if no MISSING markers and qbar_XT_bound_abs has units/source paths",
            "required_columns": "all_component_statuses;all_source_paths;units;normalization;valid_for_claim",
            "current_status": "CLAIM_BLOCKED",
            "observable_link": "all_local_arenas",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def dependency_rows() -> list[dict[str, str]]:
    return [
        {
            "dependency_id": "DEP1027_0_alpha_product",
            "quantity": "alpha_bulk(lambda_X)",
            "depends_on": "K_X;Qbar_XH(lambda_X);qbar_XT;lambda_X;alpha_bound(lambda_X)",
            "current_status": "BLOCKED_BY_QBAR_AND_OTHER_INPUTS",
            "why": "qbar_XT is only one factor; even qbar_XT bound needs K_X, Qbar_XH, lambda_X, and real bound curve to score R10",
            "next_action": "keep alpha row nonclaim until every factor is sourced",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "dependency_id": "DEP1027_1_source_zero_stronger",
            "quantity": "qbar_XT=0",
            "depends_on": "q-kernel;Obs_e descent;matter functor;no-marker;hidden-tail silence",
            "current_status": "FAIL_CURRENT_CLAIM",
            "why": "conditional chain rule is valid but parent certificate does not close",
            "next_action": "do not set alpha to zero by qbar_XT unless certificate closes",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "dependency_id": "DEP1027_2_bound_fallback",
            "quantity": "qbar_XT_bound_abs",
            "depends_on": "c_g;b_dis;b_A;b_alpha;q_nonH;Delta_W_support;q_domain;q_boundary",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "why": "the retained counterexamples are now componentized into bounded source rows",
            "next_action": "source first real c_g/b_A/q_nonH rows or prove their theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "dependency_id": "DEP1027_3_no_cancellation",
            "quantity": "total local coupling envelope",
            "depends_on": "absolute component sum, not signed cancellation",
            "current_status": "GUARDRAIL_ACTIVE",
            "why": "unknown frame/marker/source components cannot be allowed to cancel into a fake GR limit",
            "next_action": "use component-sum absolute envelopes for all retained residuals",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def branch_verdict_rows() -> list[dict[str, str]]:
    return [
        {
            "verdict_id": "BV1027_0_conditional_zero",
            "branch": "qbar_XT source-zero",
            "status": "conditional_theorem_valid_not_parent_signed",
            "because": "chain-rule zero works if q, Obs_e, S_matter, theta_A, and hidden tails are all parent-owned",
            "allowed_statement": "MTS has an exact source-zero theorem target",
            "forbidden_statement": "current MTS has qbar_XT=0",
            "next_action": "retain qbar_XT as source-coupling row unless parent certificate closes",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "verdict_id": "BV1027_1_counterexamples",
            "branch": "weak-premise shortcut rejection",
            "status": "counterexamples_block_zero_claim",
            "because": "universal Weyl, disformal, marker constants, and non-Hilbert tails remain legal without stronger parent clauses",
            "allowed_statement": "WEP/species-blindness can help but is not source-zero",
            "forbidden_statement": "WEP/covariance alone kills qbar_XT",
            "next_action": "source or zero each counterexample component",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "verdict_id": "BV1027_2_bound_schema",
            "branch": "bounded qbarXT fallback",
            "status": "schema_ready_values_missing",
            "because": "component rows define how to bound qbar_XT without cancellation, but no numeric/theorem-zero inputs are filled",
            "allowed_statement": "bounded coupling interface is ready",
            "forbidden_statement": "bounded coupling has passed a local test",
            "next_action": "fill first real frame/marker/non-Hilbert source row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "verdict_id": "BV1027_3_next_target",
            "branch": "next target",
            "status": "first_bound_input_or_marker_theorem",
            "because": "the proof route failed current claim; the honest next move is a real bound input or a no-marker theorem attempt",
            "allowed_statement": "1028 should attack c_g/b_A/q_nonH first rows or no-marker theorem",
            "forbidden_statement": "run R10/PPN as claim before qbarXT row is real",
            "next_action": "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    gates = [
        ("CG1027_0_sources_registered", "all cited source paths exist and expected needles are present", "true", "source register is intact", "false"),
        ("CG1027_1_chain_rule", "chain-rule source-zero theorem shape is valid", "true", "conditional proof is recorded", "false"),
        ("CG1027_2_q_kernel", "X is parent-signed vertical/gauge", "false", "q-kernel ownership certificate missing", "false"),
        ("CG1027_3_obs_e_descent", "observed coframe descends through q", "false", "Obs_e parent signature and no-shadow-frame theorem missing", "false"),
        ("CG1027_4_matter_functor", "ordinary matter action is quotient/coframe-only", "false", "matter functor parent selection unsigned", "false"),
        ("CG1027_5_no_marker", "constants/material markers are X-independent", "false", "no-marker theorem missing", "false"),
        ("CG1027_6_qbarXT_zero_claim", "qbar_XT/J_X source-zero may be claimed", "false", "required clauses do not close together", "false"),
        ("CG1027_7_qbarXT_bound_claim", "qbar_XT bound row may be scored", "false", "component values and source paths are missing", "false"),
        ("CG1027_8_no_cancellation_guard", "no-cancellation guard active", "true", "component absolute-sum envelope is required", "false"),
        ("CG1027_9_local_GR_claim", "local GR/Newton reduction is derived", "false", "source-zero, no-pole, Hessian, boundary, and PPN gates remain unsigned", "false"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "claim_allowed": claim_allowed,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for gate_id, claim, gate_pass, reason, claim_allowed in gates
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1027_0_zero_result",
            "decision": "qbar_XT=0/J_X=0 is a valid conditional theorem but not a current MTS result.",
            "because": "the parent q-kernel, observed coframe descent, matter functor, no-marker constants, and hidden-source silence are not signed together.",
            "next_action": "do not claim source-zero or local GR from the chain rule alone",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1027_1_bound_schema",
            "decision": "The bounded qbar_XT row schema is staged.",
            "because": "the surviving counterexamples map cleanly into c_g/b_dis/b_A/b_alpha/q_nonH/support components.",
            "next_action": "fill real theorem-zero or numeric bounds before any scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1027_2_coupling_status",
            "decision": "The coupling gap is now a source-row problem, not a vague criticism.",
            "because": "qbar_XT has named components, dependencies, observables, and no-cancellation policy.",
            "next_action": "source first c_g/b_A/q_nonH rows or derive no-marker theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1027_3_next_target",
            "decision": "Next target is frame/marker coupling bound input pack or no-marker theorem.",
            "because": "the clean zero proof did not close; the next honest progress is either a stronger parent no-marker theorem or first real bound rows.",
            "next_action": "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
            "objective": "try to derive the no-marker/constant-descent theorem for ordinary matter; if it cannot be parent-signed, build first claim-blocked c_g, b_dis, b_A, b_alpha, q_nonH, and support-shift bound rows with units, source paths, and observable links",
            "include": "no-marker theorem, quotient-owned constants, material/EM/clock markers, representative Weyl/disformal couplings, non-Hilbert/source-tail terms, R10/WEP/clock/PPN/orbital links, no-cancellation envelope",
            "exclude": "WEP-only zero, covariance-only zero, placeholder numeric values, cancellation between unknowns, finite-alpha pass, R10/PPN/local-GR claim, GitHub action",
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
    bounded: list[dict[str, str]],
    dependencies: list[dict[str, str]],
    verdicts: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    proof_required = {f"QZ1027_{idx}_{name}" for idx, name in [
        (0, "chain_rule"),
        (1, "q_verticality"),
        (2, "observed_coframe"),
        (3, "matter_functor"),
        (4, "no_marker_constants"),
        (5, "hidden_source_tail"),
        (6, "verdict"),
    ]}
    counter_required = {f"CE1027_{idx}_{name}" for idx, name in [
        (0, "common_Weyl"),
        (1, "disformal_frame"),
        (2, "material_marker"),
        (3, "nonHilbert_tail"),
        (4, "frame_rename"),
    ]}
    bound_required = {f"BQT1027_{idx}_{name}" for idx, name in [
        (0, "visible_geometry"),
        (1, "marker_constants"),
        (2, "nonHilbert_tail"),
        (3, "total_abs_guard"),
        (4, "claim_gate"),
    ]}
    checks = [
        ("V1027_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and expected needles are present"),
        ("V1027_1_proof_rows_complete", proof_required.issubset({row["proof_id"] for row in proof}), "source-zero proof audit covers chain rule, q-kernel, coframe, matter, markers, hidden tails, and verdict"),
        ("V1027_2_zero_not_claimed", any(row["proof_id"] == "QZ1027_6_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in proof) and all(row["valid_for_claim"] == "false" for row in proof), "qbarXT zero remains nonclaim"),
        ("V1027_3_counterexamples_complete", counter_required.issubset({row["counterexample_id"] for row in counterexamples}), "counterexamples cover Weyl, disformal, markers, non-Hilbert tails, and frame renames"),
        ("V1027_4_counterexamples_block", all(flag(row["blocks_zero_claim"]) for row in counterexamples), "all counterexamples block source-zero shortcuts"),
        ("V1027_5_bound_rows_complete", bound_required.issubset({row["row_id"] for row in bounded}), "bounded qbarXT schema covers geometry, markers, non-Hilbert tail, total guard, and claim gate"),
        ("V1027_6_bound_rows_nonclaim", all(row["valid_for_claim"] == "false" for row in bounded) and any(row["row_id"] == "BQT1027_3_total_abs_guard" for row in bounded), "bound rows remain nonclaim with total absolute guard"),
        ("V1027_7_dependencies_complete", {"DEP1027_0_alpha_product", "DEP1027_1_source_zero_stronger", "DEP1027_2_bound_fallback", "DEP1027_3_no_cancellation"}.issubset({row["dependency_id"] for row in dependencies}), "dependency rows link qbarXT to alpha product and no-cancellation guard"),
        ("V1027_8_verdicts_complete", {"BV1027_0_conditional_zero", "BV1027_1_counterexamples", "BV1027_2_bound_schema", "BV1027_3_next_target"}.issubset({row["verdict_id"] for row in verdicts}), "branch verdicts are complete"),
        ("V1027_9_claim_gates_blocked", all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in gates), "all claim gates refuse promotion"),
        ("V1027_10_no_cancellation_guard", any(row["gate_id"] == "CG1027_8_no_cancellation_guard" and flag(row["gate_pass"]) for row in gates), "no-cancellation guard is active"),
        ("V1027_11_decision_written", any(row["decision_id"] == "DEC1027_3_next_target" for row in decisions), "1028 decision row is written"),
        ("V1027_12_next_target_written", len(next_target) == 1 and "1028-Y5-R10-frame-marker" in next_target[0]["next_target"], "1028 next target row is present"),
        ("V1027_13_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1027_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1027 qbarXT source-zero or bounded coupling validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    proof: list[dict[str, str]],
    counterexamples: list[dict[str, str]],
    bounded: list[dict[str, str]],
    dependencies: list[dict[str, str]],
    verdicts: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1027 Y5 R10 qbarXT source zero or bounded coupling row",
            "",
            "**Status:** The `qbar_XT=0/J_X=0` proof is valid only as a conditional chain-rule theorem. Current MTS still lacks a parent-signed q-kernel, observed-coframe descent, matter functor, no-marker constants, and hidden-source silence. The fallback is now a bounded `qbar_XT` component schema with an absolute no-cancellation envelope.",
            "",
            "**Claim ceiling:** no source-zero claim, no finite-alpha pass, no R10/WEP/clock/PPN pass, and no local-GR/Newton reduction is allowed from 1027.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Source-zero proof audit",
            md_table(proof, ["proof_id", "target", "required_statement", "current_evidence", "status", "missing_for_claim", "if_missing", "valid_for_claim"]),
            "## Counterexample guard",
            md_table(counterexamples, ["counterexample_id", "weak_premise", "construction", "failure", "required_repair", "blocks_zero_claim", "valid_for_claim"]),
            "## Bounded qbarXT row schema",
            md_table(bounded, ["row_id", "symbol", "definition", "formula_or_bound", "required_columns", "current_status", "observable_link", "valid_for_claim"]),
            "## Dependency links",
            md_table(dependencies, ["dependency_id", "quantity", "depends_on", "current_status", "why", "next_action", "valid_for_claim"]),
            "## Branch verdicts",
            md_table(verdicts, ["verdict_id", "branch", "status", "because", "allowed_statement", "forbidden_statement", "next_action", "valid_for_claim"]),
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
    proof = source_zero_proof_rows()
    counterexamples = counterexample_rows()
    bounded = bounded_qbar_rows()
    dependencies = dependency_rows()
    verdicts = branch_verdict_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, proof, counterexamples, bounded, dependencies, verdicts, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1027_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1027_SOURCE_ZERO_PROOF_AUDIT.csv", proof)
    write_csv(OUT / "P8_Y5_R10_1027_COUNTEREXAMPLE_GUARD.csv", counterexamples)
    write_csv(OUT / "P8_Y5_R10_1027_BOUNDED_QBARXT_ROW_SCHEMA.csv", bounded)
    write_csv(OUT / "P8_Y5_R10_1027_DEPENDENCY_LINKS.csv", dependencies)
    write_csv(OUT / "P8_Y5_R10_1027_BRANCH_VERDICTS.csv", verdicts)
    write_csv(OUT / "P8_Y5_R10_1027_CLAIM_GATES.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1027_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1027_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1027_VALIDATION.csv", validations)
    write_doc(sources, proof, counterexamples, bounded, dependencies, verdicts, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()

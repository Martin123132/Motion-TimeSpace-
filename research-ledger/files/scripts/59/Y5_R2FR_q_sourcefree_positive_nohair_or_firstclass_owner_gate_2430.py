from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_Q_SOURCEFREE_POSITIVE_NOHAIR_OR_FIRSTCLASS_OWNER_GATE_2430"
CHECKPOINT_ID = "2430"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2430-Y5-R2FR-q-sourcefree-positive-nohair-or-firstclass-owner-gate.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2430_SOURCE_REGISTER.csv",
    "nohair_theorem": OUT / "P8_Y5_PARENT_QLOC_2430_SHARP_Q_NOHAIR_THEOREM.csv",
    "activation_gates": OUT / "P8_Y5_PARENT_QLOC_2430_NOHAIR_ACTIVATION_GATES.csv",
    "firstclass_gate": OUT / "P8_Y5_PARENT_QLOC_2430_FIRSTCLASS_OWNER_GATE.csv",
    "jq_source_channels": OUT / "P8_Y5_PARENT_QLOC_2430_JQ_SOURCE_CHANNEL_ZERO_AUDIT.csv",
    "residual_bound": OUT / "P8_Y5_PARENT_QLOC_2430_FINITE_Q_RESIDUAL_BOUND_LAW.csv",
    "coupling_impact": OUT / "P8_Y5_PARENT_QLOC_2430_COUPLING_IMPACT_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2430_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2430_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2430_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2430_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2430_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_nohair": QUEUE / "JR2430_Q_NOHAIR_THEOREM_NONCLAIM.csv",
    "queue_jq": QUEUE / "JR2430_JQ_SOURCE_CHANNEL_AUDIT_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "q_nohair_coupling_impact_nonclaim_2430.csv",
    "beta_docs": BETA_DOCS / "Q_NOHAIR_JQ_SOURCE_AUDIT_2430_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2430_00_2429_handoff",
        "source_path": ROOT / "2429-Y5-R2FR-parent-q-sector-Thetaq-Pq-owner-or-boundary-coefficient-prior.md",
        "needles": ["NEXT2429_0_selected", "TPQ2429_5_verdict", "VAL2429_OVERALL"],
        "role": "fresh handoff selecting q source-free positive no-hair or first-class owner gate",
    },
    {
        "source_id": "SRC2430_01_2429_validation",
        "source_path": OUT / "P8_Y5_BRR545_2429_VALIDATION.csv",
        "needles": ["VAL2429_OVERALL", "PASS"],
        "role": "confirms 2429 passed before 2430",
    },
    {
        "source_id": "SRC2430_02_2429_route_menu",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2429_Q_PARENT_ROUTE_MENU.csv",
        "needles": ["QC2429_1_first_class_vertical_constraint", "QC2429_2_positive_sourcefree_physical_q"],
        "role": "current q route menu",
    },
    {
        "source_id": "SRC2430_03_2429_theta_template",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2429_THETAQ_PQ_TEMPLATE_CONTRACT.csv",
        "needles": ["TPQ2429_4_positive_q_example", "Theta_q"],
        "role": "Theta_q/P_q template for positive q example",
    },
    {
        "source_id": "SRC2430_04_2429_owner_gate",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2429_THETAQ_OWNER_GATE.csv",
        "needles": ["TOG2429_5_verdict", "FAIL_CURRENT_CLAIM_THETAQ_PQ_OWNER_MISSING"],
        "role": "owner gate still blocked",
    },
    {
        "source_id": "SRC2430_05_2429_nohair_firstclass",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2429_NOHAIR_FIRSTCLASS_ROUTE_LEDGER.csv",
        "needles": ["NFR2429_0_positive_energy", "NFR2429_1_first_class"],
        "role": "positive no-hair and first-class staging",
    },
    {
        "source_id": "SRC2430_06_2425_product_law",
        "source_path": ROOT / "2425-Y5-R2FR-parent-finite-quadratic-q-row-and-source-test-coupling-split.md",
        "needles": ["LAW2425_2_R10_alpha_match", "LAW2425_3_common_Weyl_cg", "VAL2425_OVERALL"],
        "role": "source/test product law and c_g squared guard",
    },
    {
        "source_id": "SRC2430_07_2426_no_pole",
        "source_path": ROOT / "2426-Y5-R2FR-no-physical-q-pole-theorem-or-bounded-beta-runner.md",
        "needles": ["NPQ2426_6_verdict", "BB2426_7_beta_product_guard", "VAL2426_OVERALL"],
        "role": "no-pole failure and bounded beta fallback",
    },
    {
        "source_id": "SRC2430_08_2427_boundary",
        "source_path": ROOT / "2427-Y5-R2FR-boundary-charge-Qq-Kboundary-zero-or-beta-bound-first-row.md",
        "needles": ["QQK2427_2_Qq_zero", "QQK2427_5_source_boundary_limit", "VAL2427_OVERALL"],
        "role": "proper compact boundary zero sublemma and source boundary limitation",
    },
    {
        "source_id": "SRC2430_09_2428_Bq",
        "source_path": ROOT / "2428-Y5-R2FR-parent-boundary-charge-formula-Bq-or-alpha3-projection-bound.md",
        "needles": ["BQF2428_2_candidate_Qq", "BQG2428_5_verdict", "A3P2428_0_formula"],
        "role": "boundary charge formula and alpha3 projection rule",
    },
    {
        "source_id": "SRC2430_10_2296_precedent",
        "source_path": ROOT / "2296-Y5-R2FR-q-sourcefree-positive-nohair-or-firstclass-owner-gate.md",
        "needles": ["NH2296_3_zero_theorem", "JQ2296_6_total_verdict", "VAL2296_OVERALL"],
        "role": "older conditional no-hair precedent, now sharpened by current chain",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                source_path=path,
                path_exists=path.exists(),
                required_needles="; ".join(needles),
                found_needles="; ".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=source["role"],
            )
        )
    return rows


def nohair_theorem_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            theorem_id="NH2430_0_domain",
            object="local exterior q sector",
            statement="Work on a local exterior domain D with q in H1(D) after gauge/proper-kernel quotient and declared boundary class.",
            derivation_status="SETUP_READY_CONDITIONAL",
            blocks_claim="domain, quotient, topology, and boundary class are not parent-selected",
        ),
        base_row(
            theorem_id="NH2430_1_bilinear_form",
            object="positive q operator",
            statement="a(q,eta)=int_D [Z_q^{mu nu} nabla_mu q nabla_nu eta + M_q^2 q eta + positive_mix(q,eta)] dV.",
            derivation_status="FORMULA_DERIVED_CONDITIONAL_ON_LQ",
            blocks_claim="Z_q, M_q^2, and positive_mix are not parent-owned",
        ),
        base_row(
            theorem_id="NH2430_2_coercivity_premise",
            object="coercive energy",
            statement="If a(q,q) >= c_q ||q||_H1(D)^2 with c_q>0 after zero-mode removal, the homogeneous q sector has no finite-energy hair.",
            derivation_status="MATHEMATICALLY_CLEAN_PREMISE_UNSIGNED",
            blocks_claim="no parent Hessian/sign certificate or zero-mode rule",
        ),
        base_row(
            theorem_id="NH2430_3_weak_equation",
            object="source and boundary functional",
            statement="The weak equation is a(q,eta)=J_q[eta]-Phi_boundary_q[eta] for every admissible eta.",
            derivation_status="DERIVED_FROM_VARIATION_TEMPLATE",
            blocks_claim="J_q and Phi_boundary_q are not theorem-zero",
        ),
        base_row(
            theorem_id="NH2430_4_zero_theorem",
            object="q=0 theorem",
            statement="Taking eta=q gives c_q||q||^2 <= J_q[q]-Phi_boundary_q[q]; if J_q=0 and Phi_boundary_q=0, then q=0 on D.",
            derivation_status="CONDITIONAL_THEOREM_PROVED",
            blocks_claim="activation requires parent-signed source-zero, boundary-zero, positivity, and kernel removal",
        ),
        base_row(
            theorem_id="NH2430_5_nonzero_source_bound",
            object="finite residual law",
            statement="If J_q or Phi_boundary_q is nonzero, the safe result is ||q||_H1 <= (||J_q||_*+||Phi_boundary_q||_*)/c_q, not q=0.",
            derivation_status="BOUND_DERIVED_FROM_COERCIVITY",
            blocks_claim="norms, c_q, source decomposition, and arena projections are missing",
        ),
        base_row(
            theorem_id="NH2430_6_no_cancellation_rule",
            object="no hidden cancellation",
            statement="A small observed residual cannot be used as J_q=0 unless every source/boundary channel is independently zero or bounded in absolute value.",
            derivation_status="POLICY_LOCK_FROM_PRODUCT_LAW",
            blocks_claim="prevents cancelling source, test, boundary, and tail pieces against each other",
        ),
        base_row(
            theorem_id="NH2430_7_verdict",
            object="source-free positive no-hair route",
            statement="The no-hair lemma is now sharp: positivity kills q only after exact J_q=0 and boundary silence; otherwise finite residual bounds are mandatory.",
            derivation_status="CONDITIONAL_PROOF_COMPLETE_ACTIVATION_BLOCKED",
            blocks_claim="J_q source leg is the decisive remaining coupling gap",
        ),
    ]


def activation_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="NHA2430_0_parent_Lq", premise="parent q action or constraint route", required="select L_q/C_q before using Theta_q/P_q", current_status="MISSING_PARENT_ACTION_SELECTION", consequence="no-hair theorem remains conditional"),
        base_row(gate_id="NHA2430_1_Z_positive", premise="positive kinetic block", required="Z_q^{mu nu} positive/coercive on admissible local modes", current_status="MISSING_ZQ_SIGN_CERTIFICATE", consequence="cannot exclude ghosts/sign-indefinite hair"),
        base_row(gate_id="NHA2430_2_M_gap", premise="mass/gap or kernel quotient", required="M_q^2>0 or all zero modes are quotient/proper/topological and unobservable", current_status="MISSING_MQ2_OR_KERNEL_RULE", consequence="massless q pole can survive"),
        base_row(gate_id="NHA2430_3_Jq_zero", premise="source functional silence", required="J_q[eta]=0 channelwise for matter, frame, marker, boundary, domain, memory, reference, and source-normalization channels", current_status="COUPLING_GAP_OPEN", consequence="q=L_q^{-1}J_q becomes finite residual"),
        base_row(gate_id="NHA2430_4_boundary_zero", premise="boundary flux silence", required="Phi_boundary_q=0 on the same domain, not only compact/proper representative transformations", current_status="SOURCE_WORLDTUBE_BOUNDARY_OPEN", consequence="alpha3/R10 edge rows remain live"),
        base_row(gate_id="NHA2430_5_projection_cleanup", premise="observable projection silence", required="q=0 implies R10, alpha3, WEP, clocks, PPN, orbital projections vanish or are bounded separately", current_status="PROJECTION_TAILS_OPEN", consequence="local q silence does not automatically prove local-GR observables"),
        base_row(gate_id="NHA2430_6_verdict", premise="claim-grade q=0 local branch", required="NHA2430_0 through NHA2430_5 all close from one parent route", current_status="FAIL_CURRENT_CLAIM_Q_ZERO_NOT_ACTIVATED", consequence="derive J_q zero next or bound finite q"),
    ]


def firstclass_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="FC2430_0_vertical_generator", needed="all-field q vertical generator v_q", test="v_q acts on metric/coframe/domain/memory/matter/boundary fields and is in ker(D public quotient)", current_status="FIELD_ACTION_INCOMPLETE", if_missing="q cannot be declared gauge"),
        base_row(gate_id="FC2430_1_parent_Omega", needed="parent presymplectic form Omega", test="Omega is derived from the selected parent action and boundary class", current_status="MISSING_PARENT_OMEGA", if_missing="no canonical first-class proof"),
        base_row(gate_id="FC2430_2_momentum_map", needed="Omega-flat(v_q)=delta C_q", test="i_vq Omega = delta C_q plus differentiable boundary terms", current_status="MISSING_DCQ_MOMENTUM_MAP", if_missing="constraint owner is not proved"),
        base_row(gate_id="FC2430_3_boundary_proper_zero", needed="Q_q/K_boundary silence", test="proper/exact/collar result extends or is restricted without touching physical GR charges", current_status="PARTIAL_COMPACT_PROPER_ONLY", if_missing="edge q hair can remain"),
        base_row(gate_id="FC2430_4_bracket_closure", needed="first-class algebra", test="{G_q[epsilon],G_q[eta]} closes with zero/proper boundary cocycle", current_status="MISSING_BRACKET_CLOSURE", if_missing="second-class/anomalous q mode can remain"),
        base_row(gate_id="FC2430_5_degree_count", needed="phase-space removal", test="constraints remove the local q canonical pair and reduced Omega is nondegenerate", current_status="MISSING_DEGREE_COUNT", if_missing="no-pole claim is under-specified"),
        base_row(gate_id="FC2430_6_matter_descent", needed="matter/readout descent", test="S_matter, constants, clocks, EM/material readouts depend only on quotient observables", current_status="MISSING_MATTER_DESCENT", if_missing="source/test beta rows stay live"),
        base_row(gate_id="FC2430_7_verdict", needed="claim-grade first-class q no-pole", test="FC2430_0 through FC2430_6 close together", current_status="FAIL_CURRENT_CLAIM_FIRSTCLASS_OWNER_NOT_PROVED", if_missing="use positive no-hair or finite residual route"),
    ]


def jq_source_channel_rows() -> list[dict[str, Any]]:
    return [
        base_row(channel_id="JQ2430_0_matter_mass_pullback", channel="ordinary matter mass/readout pullback", zero_condition="partial_q ln m_i^eff=0 for source and test bodies in the parent q normalization", if_open="beta_source and beta_test are nonzero; R10/WEP/clock rows live", current_status="NOT_ZERO_PROVED"),
        base_row(channel_id="JQ2430_1_universal_frame", channel="common Weyl/disformal observed frame", zero_condition="A_g(q), B_g(q), clock and ruler frame maps have no q derivative or are quotient-pure", if_open="universal contribution enters exchange as c_g^2 unless source leg is explicitly packed into Qbar", current_status="NOT_ZERO_PROVED"),
        base_row(channel_id="JQ2430_2_material_marker", channel="EM/material constants marker", zero_condition="alpha_EM, masses, transition frequencies, composition markers have no q derivative", if_open="composition/WEP/clock beta rows live", current_status="NOT_ZERO_PROVED"),
        base_row(channel_id="JQ2430_3_boundary_worldtube", channel="source worldtube and non-proper boundary", zero_condition="Q_edge, B_q, reference/counterterm flux and source boundary data are exact/proper zero", if_open="Phi_boundary_q and Qbar_edge_qH feed alpha3/R10 edge residuals", current_status="NOT_ZERO_PROVED"),
        base_row(channel_id="JQ2430_4_projector_domain", channel="projector/domain selector", zero_condition="local domain projector is q-orthogonal or first-class/topological with no stress source", if_open="preferred-frame, alpha3, orbital and R10 domain tails stay live", current_status="NOT_ZERO_PROVED"),
        base_row(channel_id="JQ2430_5_memory_history", channel="memory/history kernel", zero_condition="memory kernel has no local q projection or is bounded as an absolute tail", if_open="time/clocks/Gdot/cosmology-local transfer tail remains", current_status="NOT_ZERO_PROVED"),
        base_row(channel_id="JQ2430_6_source_normalization", channel="measured GM/source calibration", zero_condition="Pi_M^H source measure is q-orthogonal and does not double count GR mass charge", if_open="Newton/PPN/source-normalization q charge remains", current_status="NOT_ZERO_PROVED"),
        base_row(channel_id="JQ2430_7_total_verdict", channel="J_q total", zero_condition="all source channels vanish by one parent descent theorem", if_open="finite q residual bound must be used componentwise", current_status="JQ_TOTAL_ZERO_NOT_PROVED"),
    ]


def residual_bound_rows() -> list[dict[str, Any]]:
    return [
        base_row(bound_id="QRB2430_0_operator_inverse", object="finite q response", formula="q = L_q^{-1}(J_q - Phi_boundary_q) on the admissible local exterior domain", status="CONDITIONAL_LINEAR_RESPONSE_READY", missing_inputs="L_q, Green domain, c_q, source/boundary norms"),
        base_row(bound_id="QRB2430_1_norm_bound", object="safe amplitude bound", formula="||q|| <= (||J_matter||+||J_frame||+||J_marker||+||J_boundary||+||J_projector||+||J_memory||+||J_ref||)/c_q", status="NO_CANCELLATION_BOUND_READY", missing_inputs="component norms and arena projection matrices"),
        base_row(bound_id="QRB2430_2_R10_product", object="R10 Yukawa comparator", formula="|alpha_q(lambda)| <= |K_q^R10(lambda)| beta_source_abs(lambda) beta_test_abs(lambda)+epsilon_tail_abs(lambda)", status="PRODUCT_LAW_RETAINED", missing_inputs="K_q, beta source/test rows, lambda support, promoted bound curve"),
        base_row(bound_id="QRB2430_3_alpha3_edge", object="preferred-frame edge residual", formula="|alpha3_q| <= |K_boundary_alpha3_q Phi_boundary_local_q|+|alpha3_tail_abs|", status="EDGE_BOUND_READY_NONCLAIM", missing_inputs="K_boundary_alpha3_q, Phi_boundary_local_q, tail components"),
        base_row(bound_id="QRB2430_4_verdict", object="finite residual fallback", formula="If J_q=0 cannot be proved, the next honest branch is bounded residuals rather than local-GR claim.", status="FALLBACK_READY_NOT_NUMERIC", missing_inputs="source-backed coefficients"),
    ]


def coupling_impact_rows() -> list[dict[str, Any]]:
    return [
        base_row(impact_id="CPL2430_0_key_lesson", branch="coupling/source leg", effect="The coupling is exactly the pressure point: positivity alone only gives q=0 for a homogeneous source-free equation.", status="CENTRAL_ROUTE_CONFIRMED"),
        base_row(impact_id="CPL2430_1_if_J_zero", branch="J_q theorem-zero", effect="positive no-hair activates after boundary/projection clauses close; q has no local exterior physical residual", status="PROMISING_BUT_UNSIGNED"),
        base_row(impact_id="CPL2430_2_if_firstclass", branch="first-class owner", effect="q is removed from reduced phase space; no physical q pole if matter descends and boundary charge is proper/exact zero", status="BEST_STRUCTURAL_ROUTE_BUT_UNSIGNED"),
        base_row(impact_id="CPL2430_3_if_J_open", branch="finite sourced q", effect="q is not killed; local tests must bound source/test product, boundary flux and projection tails", status="EMPIRICAL_FALLBACK_REQUIRED"),
        base_row(impact_id="CPL2430_4_cg_guard", branch="universal common frame coupling", effect="R10/fifth-force exchange is quadratic in the common leg, c_g^2, unless source leg is explicitly accounted inside Qbar", status="LINEAR_CG_SHORTCUT_REJECTED"),
        base_row(impact_id="CPL2430_5_no_public_claim", branch="local GR/Newton reduction", effect="No R10, alpha3, PPN, WEP, clock, orbital, local-GR or GitHub-public claim is created by this checkpoint.", status="PRIVATE_NONCLAIM"),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(claim_id="CGATE2430_0_q_nohair", claim="source-free positive q no-hair proves q=0 locally", gate_pass=False, reason="conditional theorem proved, but parent L_q/sign/gap/J_q/boundary/projection clauses remain unsigned"),
        base_row(claim_id="CGATE2430_1_firstclass", claim="q is first-class and has no physical pole", gate_pass=False, reason="Omega/DCq/bracket/degree/matter descent package is missing"),
        base_row(claim_id="CGATE2430_2_Jq_zero", claim="J_q source leg vanishes", gate_pass=False, reason="matter, frame, marker, boundary, projector, memory and source-normalization channels are not zero-proved"),
        base_row(claim_id="CGATE2430_3_finite_bounds", claim="finite q residual bounds are executable", gate_pass=False, reason="component norms, K rows, beta rows, c_q and projection matrices are missing"),
        base_row(claim_id="CGATE2430_4_local_GR", claim="local GR/Newton branch is derived", gate_pass=False, reason="q zero/no-pole branch is not activated and residual route is nonclaim"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2430_0_theorem_status", decision="CONDITIONAL_Q_NOHAIR_PROVED_SHARPLY", rationale="energy/coercivity identity shows exactly when q=0 follows", consequence="do not re-argue positivity; attack J_q/boundary/first-class ownership"),
        base_row(decision_id="DEC2430_1_coupling_status", decision="COUPLING_IS_THE_DECISIVE_GAP", rationale="any nonzero J_q produces a finite q response rather than theorem-zero", consequence="next target must prove J_q=0 componentwise or source bounds"),
        base_row(decision_id="DEC2430_2_firstclass_status", decision="FIRSTCLASS_ROUTE_REMAINS_CLEANEST_IF_OWNER_PACKAGE_CLOSES", rationale="constraint removal beats empirical bounds if Omega/DCq/degree/matter descent are signed", consequence="keep first-class gate in parallel, but do not claim it"),
        base_row(decision_id="DEC2430_3_residual_policy", decision="FINITE_RESIDUALS_REQUIRE_PRODUCT_LAW_AND_ABSOLUTE_TAILS", rationale="2425/2426 lock source-test product and no-cancellation c_g^2 accounting", consequence="no naked linear c_g or cancellation scoring"),
        base_row(decision_id="DEC2430_4_github", decision="NO_GITHUB_ACTION", rationale="checkpoint is a private derivation gate, not public theory spine closure", consequence="continue private goal work"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2430_0_selected",
            selection_status="selected",
            target_file="2431-Y5-R2FR-Jq-source-leg-zero-theorem-or-component-bound-vector.md",
            target_script="scripts/Y5_R2FR_Jq_source_leg_zero_theorem_or_component_bound_vector_2431.py",
            task="try to prove J_q=0 by parent matter/readout/frame descent channel-by-channel; if any channel fails, emit the first absolute component-bound vector for finite q residual scoring",
            acceptance_target="J_q theorem-zero closes, or each source channel becomes an explicit nonclaim bound row with units/projection/arena tags",
            guardrails="do not invent beta/K/source-normalization values, cancel tails, score naked linear c_g, claim local-GR/R10/PPN/WEP pass, edit formalization-workbench, or push GitHub",
        ),
        base_row(
            route_id="NEXT2430_1_parallel",
            selection_status="held_parallel",
            target_file="2431b-Y5-R2FR-q-firstclass-Omega-DCq-degree-matter-owner.md",
            target_script="scripts/Y5_R2FR_q_firstclass_Omega_DCq_degree_matter_owner_2431b.py",
            task="try the cleaner first-class no-pole certificate in parallel after J_q source channel audit starts",
            acceptance_target="Omega/DCq/bracket/degree/matter descent owner package or explicit failure ledger",
            guardrails="do not delete physical GR charges or treat compact representative boundary silence as source-worldtube silence",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue_nohair", OUTPUTS["nohair_theorem"], COPY_TARGETS["queue_nohair"], "conditional q no-hair theorem nonclaim queue"),
        ("queue_jq", OUTPUTS["jq_source_channels"], COPY_TARGETS["queue_jq"], "J_q source channel audit nonclaim queue"),
        ("branch_wep", OUTPUTS["coupling_impact"], COPY_TARGETS["branch_wep"], "coupling impact ledger for WEP/local residual branch"),
        ("beta_docs", OUTPUTS["jq_source_channels"], COPY_TARGETS["beta_docs"], "J_q source channels for beta source docs"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target, note in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=source,
                target_path=target,
                source_exists=source.exists(),
                target_exists=target.exists(),
                notes=note,
            )
        )
    return rows


def validation_rows(all_outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_rows = all_outputs["source_register"]
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_hits: list[Path] = []
    for pattern in ["*2430-Y5-R2FR*", "*P8_Y5_PARENT_QLOC_2430*", "*P8_Y5_BRR545_2430*", "*JR2430*", "*Q_NOHAIR_JQ_SOURCE_AUDIT_2430*"]:
        formalization_hits.extend(FORMALIZATION.rglob(pattern) if FORMALIZATION.exists() else [])

    checks = [
        ("VAL2430_00_sources_exist", all(row["path_exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL2430_01_source_needles", all(row["needles_found"] for row in source_rows), "all cited source needles are present"),
        ("VAL2430_02_nohair_zero_theorem", any(row["theorem_id"] == "NH2430_4_zero_theorem" and row["derivation_status"] == "CONDITIONAL_THEOREM_PROVED" for row in all_outputs["nohair_theorem"]), "conditional q=0 theorem is explicitly proved"),
        ("VAL2430_03_nonzero_bound", any(row["theorem_id"] == "NH2430_5_nonzero_source_bound" for row in all_outputs["nohair_theorem"]), "nonzero source produces finite residual bound rather than zero claim"),
        ("VAL2430_04_Jq_not_assumed_zero", any(row["channel_id"] == "JQ2430_7_total_verdict" and row["current_status"] == "JQ_TOTAL_ZERO_NOT_PROVED" for row in all_outputs["jq_source_channels"]), "J_q total zero is not assumed"),
        ("VAL2430_05_firstclass_blocked", any(row["gate_id"] == "FC2430_7_verdict" and "FAIL_CURRENT_CLAIM" in row["current_status"] for row in all_outputs["firstclass_gate"]), "first-class route remains blocked safely"),
        ("VAL2430_06_product_cg_guard", any(row["impact_id"] == "CPL2430_4_cg_guard" and row["status"] == "LINEAR_CG_SHORTCUT_REJECTED" for row in all_outputs["coupling_impact"]), "c_g squared/product-law guard retained"),
        ("VAL2430_07_claims_blocked", all(not row["gate_pass"] for row in all_outputs["claim_gates"]), "claim gates remain false"),
        ("VAL2430_08_next_target_written", any(row["route_id"] == "NEXT2430_0_selected" for row in all_outputs["next_target"]), "J_q next target selected"),
        ("VAL2430_09_branch_copies", all(row["target_exists"] for row in all_outputs["branch_copies"]), "branch copies were written"),
        ("VAL2430_10_no_formalization_artifacts", len(formalization_hits) == 0, "no 2430 artifacts were written to formalization-workbench"),
    ]
    for check_id, passed, notes in checks:
        rows.append(
            base_row(
                check_id=check_id,
                status="PASS" if passed else "FAIL",
                notes=notes,
                detail="" if passed else "required checkpoint condition failed",
            )
        )
    for path in output_csvs:
        parses, row_count, message = csv_parses(path)
        rows.append(
            base_row(
                check_id=f"VAL2430_CSV_{path.stem}",
                status="PASS" if parses and row_count > 0 else "FAIL",
                notes=f"CSV parses with {row_count} rows",
                detail=message,
            )
        )
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        base_row(
            check_id="VAL2430_OVERALL",
            status="PASS" if overall else "FAIL",
            notes="2430 proves the conditional q no-hair identity sharply, blocks activation, retains first-class route, locks coupling/product-law guard, and selects J_q source-leg zero theorem or component-bound vector next",
            detail="",
        )
    )
    return rows


def write_markdown(all_outputs: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2430 - Y5/R2FR q Source-Free Positive No-Hair or First-Class Owner Gate",
        "",
        "## Result",
        "- 2430 sharpens the q local branch into a real conditional theorem: if the q bilinear form is coercive and both `J_q` and `Phi_boundary_q` vanish on the same local exterior domain, then `q=0`.",
        "- It also proves the useful negative: if any source or boundary functional is nonzero, the honest result is a finite residual bound `||q|| <= (||J_q||_*+||Phi_boundary_q||_*)/c_q`, not a GR/local-vacuum claim.",
        "- The coupling/source leg is therefore confirmed as the pressure point. Positivity alone does not save the branch; `J_q=0` or first-class phase-space removal must be parent-signed.",
        "- No public claim, GitHub action, R10 pass, alpha3 pass, PPN/WEP/clock/orbital pass, or local-GR reduction is created here.",
        "",
        "## Practical Status",
        "This is progress, not a loop: the no-hair mathematics is now basically settled as a conditional lemma. The next leap is not to keep admiring the lemma; it is to prove or bound the coupling/source functional `J_q` channel-by-channel.",
        "",
        "## Source Register",
        table(["source_id", "source_path", "path_exists", "needles_found", "role"], all_outputs["source_register"]),
        "",
        "## Sharp q No-Hair Theorem",
        table(["theorem_id", "object", "statement", "derivation_status", "blocks_claim", "valid_for_claim"], all_outputs["nohair_theorem"]),
        "",
        "## Activation Gates",
        table(["gate_id", "premise", "required", "current_status", "consequence", "valid_for_claim"], all_outputs["activation_gates"]),
        "",
        "## First-Class Owner Gate",
        table(["gate_id", "needed", "test", "current_status", "if_missing", "valid_for_claim"], all_outputs["firstclass_gate"]),
        "",
        "## J_q Source Channel Zero Audit",
        table(["channel_id", "channel", "zero_condition", "if_open", "current_status", "valid_for_claim"], all_outputs["jq_source_channels"]),
        "",
        "## Finite q Residual Bound Law",
        table(["bound_id", "object", "formula", "status", "missing_inputs", "valid_for_claim"], all_outputs["residual_bound"]),
        "",
        "## Coupling Impact Ledger",
        table(["impact_id", "branch", "effect", "status", "valid_for_claim"], all_outputs["coupling_impact"]),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], all_outputs["claim_gates"]),
        "",
        "## Decisions",
        table(["decision_id", "decision", "rationale", "consequence", "valid_for_claim"], all_outputs["decisions"]),
        "",
        "## Next Target",
        table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], all_outputs["next_target"]),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "source_exists", "target_exists", "notes"], all_outputs["branch_copies"]),
        "",
        "## Validation",
        table(["check_id", "status", "notes", "detail"], all_outputs["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for path in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        path.mkdir(parents=True, exist_ok=True)

    all_outputs: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "nohair_theorem": nohair_theorem_rows(),
        "activation_gates": activation_gate_rows(),
        "firstclass_gate": firstclass_gate_rows(),
        "jq_source_channels": jq_source_channel_rows(),
        "residual_bound": residual_bound_rows(),
        "coupling_impact": coupling_impact_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key, rows in all_outputs.items():
        write_csv(OUTPUTS[key], rows)

    all_outputs["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], all_outputs["branch_copies"])
    all_outputs["validation"] = validation_rows(all_outputs)
    write_csv(OUTPUTS["validation"], all_outputs["validation"])
    write_markdown(all_outputs)

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    print(DOC)
    print(OUTPUTS["validation"])
    print(f"VAL2430_OVERALL={all_outputs['validation'][-1]['status']}")


if __name__ == "__main__":
    main()

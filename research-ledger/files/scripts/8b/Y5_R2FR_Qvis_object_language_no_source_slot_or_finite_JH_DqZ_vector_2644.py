from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2644-Y5-R2FR-Qvis-object-language-no-source-slot-or-finite-JH-DqZ-vector.md"

CHECKPOINT = "2644"
BRANCH_ID = "Y5_R2FR_QVIS_OBJECT_LANGUAGE_OR_FINITE_JH_DQZ_VECTOR_2644"
PREFIX = "P8_Y5_QVIS_OBJECT_LANGUAGE_2644"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "object_language_gate": RESIDUALS / f"{PREFIX}_OBJECT_LANGUAGE_GATE.csv",
    "finite_vector": RESIDUALS / f"{PREFIX}_FINITE_JH_DQZ_VECTOR_CONTRACT.csv",
    "validator_cases": RESIDUALS / f"{PREFIX}_FINITE_VECTOR_VALIDATOR_CASES.csv",
    "validator_results": RESIDUALS / f"{PREFIX}_FINITE_VECTOR_VALIDATOR_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2644_NO_SOURCE_PREFACTOR_OR_FINITE_JH_DQZ_VECTOR_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "Qvis_JH_DqZ_finite_vector_2644_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "QVIS_JH_DQZ_DELTAW_VECTOR_2644_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2644_QVIS_JH_DQZ_WEP_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2644_00_2643",
        "role": "immediate Q_vis/JH/DqZ handoff",
        "path": ROOT / "2643-Y5-R2FR-common-matter-descent-DqZ-zero-or-observed-leak-bound.md",
        "needles": ["QVIS2643_6_verdict", "LEAK2643_0_eps_JH_Z_abs", "VAL2643_OVERALL"],
    },
    {
        "source_id": "SRC2644_01_1886",
        "role": "no-source-only slot proof attempt and finite source-weight contract",
        "path": ROOT / "1886-Y5-R2FR-common-matter-no-source-only-slot-proof-or-finite-wR-row.md",
        "needles": ["NSS1886_7_verdict", "CMS1886_6_verdict", "VAL1886_OVERALL"],
    },
    {
        "source_id": "SRC2644_02_1887",
        "role": "parent object-language typing gate",
        "path": ROOT / "1887-Y5-R2FR-parent-object-language-typing-or-finite-source-weight-vector.md",
        "needles": ["OLT1887_9_verdict", "GATE1887_0_object_language_zero", "VAL1887_OVERALL"],
    },
    {
        "source_id": "SRC2644_03_1888",
        "role": "action-scale owner and readout/radiative stability gate",
        "path": ROOT / "1888-Y5-R2FR-action-scale-owner-readout-stability-or-finite-deltaw-vector.md",
        "needles": ["ASO1888_7_verdict", "ROS1888_6_verdict", "VAL1888_OVERALL"],
    },
    {
        "source_id": "SRC2644_04_1889",
        "role": "Ward owner separated from source-label/no-prefactor theorem",
        "path": ROOT / "1889-Y5-R2FR-source-current-Ward-owner-or-real-deltaw-component-basis.md",
        "needles": ["SWO1889_7_verdict", "CB1889_1_pre_action_species_prefactor", "VAL1889_OVERALL"],
    },
    {
        "source_id": "SRC2644_05_1674",
        "role": "visible quotient ansatz and Dq_Z component matrix",
        "path": ROOT / "1674-Y5-R2FR-parent-q-Z-basis-minimal-ansatz-and-Dq-computation.md",
        "needles": ["QANS1674_1_visible_quotient", "DQM1674_1_source_current", "VAL1674_OVERALL"],
    },
    {
        "source_id": "SRC2644_06_1045",
        "role": "matter functor descent and qbar marker/frame countermodels",
        "path": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
        "needles": ["MFS1045_6_verdict", "QG1045_4_current_verdict", "V1045_SUMMARY"],
    },
    {
        "source_id": "SRC2644_07_2214",
        "role": "chain-rule source/DqZ coefficient map",
        "path": ROOT / "2214-Y5-R2FR-algebraic-residual-coefficient-map-or-DqZ-source-descent-proof.md",
        "needles": ["DSD2214_0_exact_chain_rule", "CM2214_5_E_DqZ", "VAL2214_OVERALL"],
    },
    {
        "source_id": "SRC2644_08_1628",
        "role": "Hilbert source-owner certificate and counterexample ledger",
        "path": ROOT / "1628-Y5-R2FR-matter-descent-source-owner-certificate-or-JR-bound-acquisition.md",
        "needles": ["SOC1628_6_verdict", "CE1628_0_pre_action_weight", "VAL1628_OVERALL"],
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "valid_for_claim": "False",
        "claim_allowed": "False",
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        return bool(read_csv(path))
    except Exception:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    if columns is None:
        columns = []
        for row in rows:
            for key in row:
                if key not in columns:
                    columns.append(key)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2644_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2644-Y5-R2FR*",
        "*P8_Y5_QVIS_OBJECT_LANGUAGE_2644*",
        "*P8_Y5_BRR545_2644*",
        "*Y5_R2FR_Qvis_object_language_no_source_slot_or_finite_JH_DqZ_vector_2644*",
        "*JR2644*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        text = read_text(source["path"])
        found = [needle for needle in source["needles"] if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                role=source["role"],
                source_path=str(source["path"]),
                path_exists=str(source["path"].exists()),
                required_needles=";".join(source["needles"]),
                found_needles=";".join(found),
                needles_present=str(source["path"].exists() and len(found) == len(source["needles"])),
            )
        )
    return rows


def object_language_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="QOL2644_0_target_signature",
            clause="Q_vis-only ordinary matter grammar",
            contract="S_matter=sum_A S_A[Psi_A,Q_vis,theta_A,A_owned] with no direct Z/R_phys/Gamma_mem/chi/g(z), no source-only weights, and no marker/source frame.",
            status="TARGET_EXACT",
            current_evidence="2643 and 1674 write Q_vis; 1045 writes the matter functor contract.",
            missing_to_claim="parent field chart, q(Phi), ordinary matter category, observed coframe functor, theta ownership, boundary/readout stability",
            consequence_if_signed="P_Z[J_H]=0 and E_DqZ_A=0 for ordinary matter/readout source side, subject to non-Hilbert/boundary/CDB tails",
            passes_now="False",
        ),
        base_row(
            gate_id="QOL2644_1_constructor_list",
            clause="parent constructor list excludes hidden source coefficient objects",
            contract="Arg(S_parent) admits fields, quotient observables, representation constants and universal constants, but not inert source-only scalars w_A(Z) or marker labels.",
            status="OBJECT_LANGUAGE_TYPING_NOT_PARENT_DERIVED",
            current_evidence="1887 keeps the constructor/object-language theorem as a conditional contract.",
            missing_to_claim="constructor list derived from parent primitives rather than imposed closure grammar",
            consequence_if_signed="source-only weights become ill-typed instead of fine-tuned to zero",
            passes_now="False",
        ),
        base_row(
            gate_id="QOL2644_2_no_direct_slot",
            clause="no direct Z/R_AB/source-support argument in ordinary matter",
            contract="ordinary matter can see Z only through Q_vis; direct F(Z), F(R_AB), support shifts, or source-worldtube masks are illegal or explicit residuals.",
            status="DIRECT_SLOT_EXCLUSION_UNSIGNED",
            current_evidence="1628 and 1045 identify exact chain-rule silence but retain direct-slot counterexamples.",
            missing_to_claim="parent matter functor signature plus source/readout/boundary exclusion",
            consequence_if_signed="J_direct[Z] term in 2643 chain-rule theorem vanishes",
            passes_now="False",
        ),
        base_row(
            gate_id="QOL2644_3_no_source_prefactor",
            clause="no pre-action source-only/species prefactor",
            contract="S_matter=sum_A w_A(Z) S_A and kappa_A(Z)T_A are forbidden before variation unless w_A is universal derivative-silent common mode.",
            status="COUNTERMODEL_SURVIVES",
            current_evidence="1886/1888/1889 show weighted matter equations may look ordinary while Hilbert source changes.",
            missing_to_claim="parent no-source-prefactor/no-double-counting matter-normalization clause",
            consequence_if_signed="Delta_w, beta_w_source, beta_w_test and w_R become theorem-zero after common-mode guard",
            passes_now="False",
        ),
        base_row(
            gate_id="QOL2644_4_action_measure_owner",
            clause="single action-scale/hbar/measure owner",
            contract="one parent action measure and species-blind Jacobian owns all ordinary matter normalization.",
            status="ACTION_SCALE_OWNER_NOT_DERIVED",
            current_evidence="1888 rejects action-scale owner as current claim.",
            missing_to_claim="hbar_parent, Dmu_parent/Jacobian, path-integral/readout stability, current owner",
            consequence_if_signed="relative source/action weights cannot hide in normalization",
            passes_now="False",
        ),
        base_row(
            gate_id="QOL2644_5_no_marker_hidden_morphism",
            clause="no hidden-visible coefficient morphism",
            contract="Hom(C_hid or Marker, Coeff_source/readout) is absent or constant; theta/material markers are superselection/readout data, not representative fields.",
            status="NO_MARKER_NO_MORPHISM_UNSIGNED",
            current_evidence="1045 and 1888 keep no-shadow-frame/no-hidden-morphism/no-marker as unsigned critical clauses.",
            missing_to_claim="primitive no-marker theorem or finite marker/source coefficient rows",
            consequence_if_signed="eps_theta_marker and qbar_marker vanish for ordinary matter source side",
            passes_now="False",
        ),
        base_row(
            gate_id="QOL2644_6_readout_radiative_stability",
            clause="readout and radiative closure preserve source grammar",
            contract="readout-after-variation, thresholds, clocks, WEP/R10 projections and S_eff do not generate new hidden-to-source coefficient arguments.",
            status="READOUT_RADIATIVE_UNSIGNED",
            current_evidence="1888 separates clean readout domain theorem from reduced-action and radiative countermodels.",
            missing_to_claim="parent domain exclusion plus no reduced-action laundering and radiative/readout closure",
            consequence_if_signed="tree-level Q_vis source silence survives actual observed local tests",
            passes_now="False",
        ),
        base_row(
            gate_id="QOL2644_7_Ward_owner",
            clause="source-current Ward owner and label forgetting",
            contract="Ward identity conserves the parent-owned Hilbert current, while label-forgotten source functor plus no prefactor chooses one species-blind coupling.",
            status="WARD_BRIDGE_REAL_NOT_SPECIES_BLIND",
            current_evidence="1889 separates Ward conservation from species-blind source normalization.",
            missing_to_claim="source-label forgetting, no pre-action prefactor, projected mass calibration, no non-Hilbert bypass",
            consequence_if_signed="source-current side can reduce to one calibrated kappa_univ current",
            passes_now="False",
        ),
        base_row(
            gate_id="QOL2644_8_verdict",
            clause="Q_vis object-language source-side zero",
            contract="QOL2644_0 through QOL2644_7 close in one parent branch before local empirical scoring.",
            status="NOT_PARENT_SIGNED_FINITE_VECTOR_REQUIRED",
            current_evidence="every subtheorem is sharp but at least one required parent owner remains unsigned.",
            missing_to_claim="no-source-prefactor parent action clause or finite source-backed vector",
            consequence_if_signed="local-GR source side becomes serious theorem-zero territory; not enough alone for full GR because J_NH/boundary/CDB remain",
            passes_now="False",
        ),
    ]


def finite_vector_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            vector_id="FJV2644_0_master_vector",
            symbol="Xi_JH_DqZ_A",
            component="master finite source/readout vector",
            formula="Xi_A = eps_JH_Z_abs + E_DqZ_A + Delta_w_A + beta_w_source/test_A + eps_theta_marker_A + qbar_marker_A + b_g_A + boundary_projector_A",
            required_input="each component theorem-zero or source-backed finite value with units and arena projection",
            current_status="VECTOR_CONTRACT_READY_VALUES_MISSING",
            arenas="Newton;PPN;WEP;R10;clock;EM;orbital",
            score_ready="False",
        ),
        base_row(
            vector_id="FJV2644_1_component_basis",
            symbol="B_source",
            component="source-relevant component basis",
            formula="basis over species/action prefactor, source current rescale, hidden marker spurion, non-Hilbert bypass, observed-frame leak and boundary/projector leak",
            required_input="parent component basis and common-mode projection",
            current_status="MISSING_COMPONENT_BASIS",
            arenas="all local arenas",
            score_ready="False",
        ),
        base_row(
            vector_id="FJV2644_2_eps_JH",
            symbol="eps_JH_Z_abs",
            component="ordinary Hilbert source leak",
            formula="eps_JH_Z_abs <= C_matter*Dq_Z_norm + eps_theta_marker + eps_direct_Z + eps_source_weight + eps_matter_boundary",
            required_input="Q_vis grammar or finite C_matter/DqZ/theta/source/boundary rows",
            current_status="BOUND_FORM_READY_VALUES_MISSING",
            arenas="Newton;PPN;WEP;R10;clock;orbital",
            score_ready="False",
        ),
        base_row(
            vector_id="FJV2644_3_E_DqZ",
            symbol="E_DqZ_A",
            component="observed descent leak",
            formula="E_DqZ_A <= C_A_obs*Dq_Z_norm*N_Z + E_theta_A + E_readout_A + E_boundary_projector_A",
            required_input="observed coframe/source/readout functor and DqZ norm or finite projection coefficients",
            current_status="ARENA_MAP_READY_VALUES_MISSING",
            arenas="Newton;PPN;WEP;R10;clock;EM;orbital",
            score_ready="False",
        ),
        base_row(
            vector_id="FJV2644_4_Delta_w",
            symbol="Delta_w_i",
            component="relative source/action-weight vector",
            formula="w_A=w_common(1+sum_i Q_Ai Delta_w_i), with common mode projected out",
            required_input="component basis, parent coefficient vector, material/source projections",
            current_status="MISSING_PARENT_VECTOR",
            arenas="WEP;Newton;PPN;R10;clock;orbital",
            score_ready="False",
        ),
        base_row(
            vector_id="FJV2644_5_beta_w",
            symbol="beta_w_source;beta_w_test",
            component="source/test derivative legs",
            formula="beta_w = partial_X ln w in a declared canonical Xhat/phi convention",
            required_input="canonical normalization, source/test split, product law, K/Qbar projections",
            current_status="MISSING_SOURCE_TEST_LEGS",
            arenas="R10;PPN;finite exchange",
            score_ready="False",
        ),
        base_row(
            vector_id="FJV2644_6_marker",
            symbol="eps_theta_marker;qbar_marker",
            component="theta/material/hidden marker source leak",
            formula="marker leak <= |J_theta Lie_Z theta|/J_ref + shadow-frame/source-label coefficients",
            required_input="no-marker theorem or source-backed marker/shadow coefficients",
            current_status="NO_MARKER_THEOREM_OR_COEFFICIENTS_MISSING",
            arenas="WEP;clock;EM;R10;PPN",
            score_ready="False",
        ),
        base_row(
            vector_id="FJV2644_7_observed_frame",
            symbol="b_g;sigma_X",
            component="observed coframe/common-frame leak",
            formula="gamma bridge allowed only as nonclaim response form until b_g, x_U and no-other-channel proof exist",
            required_input="Dq/tau projectability, coframe functor, b_g and x_U source rows",
            current_status="SOURCE_BACKED_FORM_NONCLAIM_VALUES_MISSING",
            arenas="PPN_gamma;clock;WEP;R10_bridge",
            score_ready="False",
        ),
        base_row(
            vector_id="FJV2644_8_policy",
            symbol="absolute_sum_policy",
            component="no cancellation/no G absorption guard",
            formula="relative components cannot be hidden in measured G_N/GM and no cancellation among vector heads is scoreable without parent identity",
            required_input="each head zeroed or bounded independently",
            current_status="GUARD_ACTIVE",
            arenas="all local arenas",
            score_ready="False",
        ),
    ]


def validator_case_rows() -> list[dict[str, Any]]:
    return [
        base_row(case_id="CASE2644_0_parent_zero_unsigned", route="theorem_zero", qvis_signed="False", no_prefactor_signed="False", finite_values="False", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_PARENT_SIGNATURE_UNSIGNED"),
        base_row(case_id="CASE2644_1_qvis_only", route="theorem_zero", qvis_signed="True", no_prefactor_signed="False", finite_values="False", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_NO_SOURCE_PREFACTOR_UNSIGNED"),
        base_row(case_id="CASE2644_2_Ward_only", route="theorem_zero", qvis_signed="False", no_prefactor_signed="False", ward_only="True", finite_values="False", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_WARD_ONLY_NOT_SPECIES_BLIND"),
        base_row(case_id="CASE2644_3_bound_anchor", route="finite_vector", qvis_signed="False", no_prefactor_signed="False", finite_values="False", bound_anchor="True", G_absorption="False", cancellation="False", expected_status="REFUSED_BOUND_ANCHOR_NOT_PREDICTION"),
        base_row(case_id="CASE2644_4_missing_basis", route="finite_vector", component_basis="False", parent_vector="True", tau_projection="True", K_projection="True", finite_values="True", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_MISSING_COMPONENT_BASIS"),
        base_row(case_id="CASE2644_5_missing_tau", route="finite_vector", component_basis="True", parent_vector="True", tau_projection="False", K_projection="True", finite_values="True", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_MISSING_TAU_PROJECTION"),
        base_row(case_id="CASE2644_6_G_absorption", route="finite_vector", component_basis="True", parent_vector="True", tau_projection="True", K_projection="True", finite_values="True", bound_anchor="False", G_absorption="True", cancellation="False", expected_status="REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_GUARD"),
        base_row(case_id="CASE2644_7_cancellation", route="finite_vector", component_basis="True", parent_vector="True", tau_projection="True", K_projection="True", finite_values="True", bound_anchor="False", G_absorption="False", cancellation="True", expected_status="REFUSED_CANCELLATION_ONLY"),
        base_row(case_id="CASE2644_8_schema_only", route="finite_vector", component_basis="True", parent_vector="False", tau_projection="False", K_projection="False", finite_values="False", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="SCHEMA_ONLY_NOT_EVIDENCE"),
    ]


def classify_case(row: dict[str, Any]) -> str:
    if row.get("route") == "theorem_zero":
        if row.get("ward_only") == "True":
            return "REFUSED_WARD_ONLY_NOT_SPECIES_BLIND"
        if row.get("qvis_signed") != "True":
            return "REFUSED_PARENT_SIGNATURE_UNSIGNED"
        if row.get("no_prefactor_signed") != "True":
            return "REFUSED_NO_SOURCE_PREFACTOR_UNSIGNED"
        return "THEOREM_ZERO_READY_NONCLAIM"
    if row.get("bound_anchor") == "True":
        return "REFUSED_BOUND_ANCHOR_NOT_PREDICTION"
    if row.get("G_absorption") == "True":
        return "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_GUARD"
    if row.get("cancellation") == "True":
        return "REFUSED_CANCELLATION_ONLY"
    if row.get("component_basis") != "True":
        return "REFUSED_MISSING_COMPONENT_BASIS"
    if row.get("parent_vector") != "True" or row.get("finite_values") != "True":
        return "SCHEMA_ONLY_NOT_EVIDENCE"
    if row.get("tau_projection") != "True":
        return "REFUSED_MISSING_TAU_PROJECTION"
    if row.get("K_projection") != "True":
        return "REFUSED_MISSING_K_QBAR_PROJECTION"
    return "FINITE_VECTOR_SCHEMA_READY_NONCLAIM"


def validator_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        observed = classify_case(case)
        row = dict(case)
        row.update(
            {
                "observed_status": observed,
                "status_matches_expected": str(observed == case["expected_status"]),
                "valid_prediction_row": "False",
                "score_ready": "False",
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2644_0_Qvis_signature", claim="ordinary matter/readouts are Q_vis-only", allowed="False", blocker="object-language constructor list and parent field chart are unsigned"),
        base_row(gate_id="CG2644_1_no_source_prefactor", claim="no pre-action source/species prefactor is parent-forbidden", allowed="False", blocker="w_A S_A countermodel survives; action-scale/source-current owner not derived"),
        base_row(gate_id="CG2644_2_JH_DqZ_zero", claim="eps_JH_Z_abs=E_DqZ_A=0", allowed="False", blocker="Q_vis/no-marker/no-source-prefactor/readout clauses do not close together"),
        base_row(gate_id="CG2644_3_finite_vector_score", claim="finite JH/DqZ/Delta_w vector is score-ready", allowed="False", blocker="component basis, parent coefficients, tau/K/Qbar/material projections and source paths are missing"),
        base_row(gate_id="CG2644_4_local_GR_Newton", claim="local GR/Newton source side is derived", allowed="False", blocker="source side still has finite vector; non-Hilbert/boundary/CDB branches also remain open"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2644_0_main_result",
            decision="QVIS_OBJECT_LANGUAGE_NOT_PARENT_SIGNED",
            rationale="The exact grammar that would kill JH/DqZ/source-weight leaks is now written, but current evidence still leaves constructor list, no-source-prefactor, action-scale owner, no-marker and readout/radiative stability unsigned.",
            consequence="carry finite Xi_JH_DqZ_A vector as nonclaim residual.",
        ),
        base_row(
            decision_id="DEC2644_1_big_clarity",
            decision="SOURCE_SIDE_BOTTLENECK_IS_NO_SOURCE_PREFACTOR",
            rationale="Ward conservation and Q_vis functoriality help only after the parent forbids pre-action w_A/kappa_A source prefactors.",
            consequence="next derivation should attack no-source-prefactor/no-double-counting matter-normalization.",
        ),
        base_row(
            decision_id="DEC2644_2_fallback",
            decision="FINITE_VECTOR_VALIDATOR_READY_NOT_SCORE_READY",
            rationale="The validator now rejects bound-anchor shortcuts, G absorption, Ward-only arguments, missing component bases, missing tau/K projections and cancellation-only passes.",
            consequence="data tests must wait for source-backed vector components, not just experimental bounds.",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            next_id="NEXT2644_0_selected",
            next_doc="2645-Y5-R2FR-no-source-prefactor-parent-action-clause-or-first-JH-DqZ-component-row.md",
            next_script="scripts/Y5_R2FR_no_source_prefactor_parent_action_clause_or_first_JH_DqZ_component_row_2645.py",
            objective="Try to derive the parent no-source-prefactor/no-double-counting matter-normalization clause that forbids w_A(Z)S_A before variation; if it fails, fill the first finite Xi_JH_DqZ component row with coefficient origin, units, tau/K projection requirements and no bound-anchor shortcut.",
            include="parent action-scale owner; source-label forgetting; Ward owner as support not proof; pre-action prefactor countermodel; component-basis row; WEP/PPN/R10/clock/orbital projection requirements",
            exclude="Ward-only species-blindness claim; G_N/GM absorption of relative weights; MICROSCOPE/R10 bounds as predictions; local GR/Newton claim; GitHub action; formalization-workbench edits",
        )
    ]


def branch_copy_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_rows: list[dict[str, Any]] = []
    for copy_id, path in BRANCH_COPIES.items():
        write_csv(path, rows)
        copy_rows.append(
            base_row(
                copy_id=copy_id,
                copy_path=str(path),
                path_exists=str(path.exists()),
                csv_parses=str(csv_parses(path)),
                contents="2644 finite JH/DqZ/source-weight vector contract, nonclaim",
            )
        )
    return copy_rows


def validation_rows(generated_paths: list[Path], rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    gate_rows = rows_by_name["object_language_gate"]
    vector_rows = rows_by_name["finite_vector"]
    result_rows = rows_by_name["validator_results"]
    claim_rows = rows_by_name["claim_gates"]
    decision_rows_ = rows_by_name["decision"]
    next_rows = rows_by_name["next_target"]
    branch_rows = rows_by_name["branch_copies"]
    checks = [
        ("VAL2644_00_sources", all(row["path_exists"] == "True" and row["needles_present"] == "True" for row in source_rows), "all cited source paths exist and required needles are present"),
        ("VAL2644_01_object_language_gate", any(row["gate_id"] == "QOL2644_8_verdict" and row["status"] == "NOT_PARENT_SIGNED_FINITE_VECTOR_REQUIRED" for row in gate_rows), "Qvis object-language zero is not promoted"),
        ("VAL2644_02_no_source_prefactor_visible", any(row["gate_id"] == "QOL2644_3_no_source_prefactor" and row["status"] == "COUNTERMODEL_SURVIVES" for row in gate_rows), "pre-action source-prefactor countermodel is retained"),
        ("VAL2644_03_finite_vector_components", all(token in ";".join(row["symbol"] for row in vector_rows) for token in ["eps_JH_Z_abs", "E_DqZ_A", "Delta_w_i", "beta_w_source", "qbar_marker", "b_g"]), "finite vector includes JH, DqZ, Delta_w, beta, marker and frame heads"),
        ("VAL2644_04_validator_refusals", all(row["status_matches_expected"] == "True" and row["valid_for_claim"] == "False" for row in result_rows), "validator dry-runs refuse unsafe routes as expected"),
        ("VAL2644_05_claim_gates_false", all(row["allowed"] == "False" and row["valid_for_claim"] == "False" for row in claim_rows), "all claim gates remain blocked"),
        ("VAL2644_06_next_wall", any(row["decision"] == "SOURCE_SIDE_BOTTLENECK_IS_NO_SOURCE_PREFACTOR" for row in decision_rows_), "decision selects no-source-prefactor bottleneck"),
        ("VAL2644_07_next_target", any(row["next_doc"].startswith("2645-Y5-R2FR-no-source-prefactor") for row in next_rows), "2645 no-source-prefactor target selected"),
        ("VAL2644_08_branch_copies", all(row["path_exists"] == "True" and row["csv_parses"] == "True" for row in branch_rows), "branch copies exist and parse"),
        ("VAL2644_09_csv_parse", all(csv_parses(path) for path in generated_paths if path.suffix.lower() == ".csv"), "all generated CSVs parse cleanly"),
        ("VAL2644_10_formalization_untouched", not formalization_has_2644_artifacts(), "no 2644 outputs are written under formalization-workbench"),
        ("VAL2644_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    rows = [base_row(validation_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]
    rows.append(
        base_row(
            validation_id="VAL2644_OVERALL",
            status="PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            detail="2644 refuses Qvis object-language source-side promotion, installs a finite JH/DqZ/source-weight vector validator, and selects no-source-prefactor parent clause as next target",
        )
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        "\n\n".join(
            [
                "# 2644 - Y5/R2FR Qvis Object-Language No-Source-Slot Or Finite JH/DqZ Vector",
                "**Status:** `Q_vis` object-language zero attempted and not parent-signed. The exact desired grammar is now explicit, but `w_A(Z) S_A` remains the live counterexample: matter equations can look ordinary while the Hilbert source changes.",
                "**Main result:** the local-GR source side has been reduced to one brutal bottleneck: prove the parent no-source-prefactor/no-double-counting matter-normalization clause, or carry the finite `Xi_JH_DqZ_A` vector into Newton/PPN/WEP/R10/clock/orbital tests.",
                "## Source register",
                md_table(rows_by_name["source_register"], ["source_id", "role", "source_path", "path_exists", "needles_present", "valid_for_claim"]),
                "## Object-language gate",
                md_table(rows_by_name["object_language_gate"], ["gate_id", "clause", "status", "contract", "current_evidence", "missing_to_claim", "consequence_if_signed", "passes_now", "valid_for_claim"]),
                "## Finite JH/DqZ vector contract",
                md_table(rows_by_name["finite_vector"], ["vector_id", "symbol", "component", "formula", "required_input", "current_status", "arenas", "score_ready", "valid_for_claim"]),
                "## Validator dry-run cases",
                md_table(rows_by_name["validator_cases"], ["case_id", "route", "expected_status", "valid_for_claim"]),
                "## Validator dry-run results",
                md_table(rows_by_name["validator_results"], ["case_id", "route", "observed_status", "status_matches_expected", "valid_prediction_row", "score_ready", "valid_for_claim"]),
                "## Claim gates",
                md_table(rows_by_name["claim_gates"], ["gate_id", "claim", "allowed", "blocker", "valid_for_claim"]),
                "## Decision ledger",
                md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "consequence", "valid_for_claim"]),
                "## Next target",
                md_table(rows_by_name["next_target"], ["next_id", "next_doc", "next_script", "objective", "include", "exclude", "valid_for_claim"]),
                "## Branch copies",
                md_table(rows_by_name["branch_copies"], ["copy_id", "copy_path", "path_exists", "csv_parses", "contents", "valid_for_claim"]),
                "## Validation",
                md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    for directory in (RESIDUALS, QUEUE, LOCAL_BOUNDS, SOURCE_WEIGHT, MICROSCOPE):
        directory.mkdir(parents=True, exist_ok=True)
    remove_pycache()

    cases = validator_case_rows()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "object_language_gate": object_language_gate_rows(),
        "finite_vector": finite_vector_rows(),
        "validator_cases": cases,
        "validator_results": validator_result_rows(cases),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    rows_by_name["branch_copies"] = branch_copy_rows(rows_by_name["finite_vector"])

    for name, rows in rows_by_name.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], rows)

    generated = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())
    rows_by_name["validation"] = validation_rows(generated, rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()

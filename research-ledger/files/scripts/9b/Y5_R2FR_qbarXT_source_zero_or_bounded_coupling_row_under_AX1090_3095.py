from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3095"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "3095-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row-under-AX1090.md"

SOURCES: dict[str, dict[str, Any]] = {
    "SRC3095_00_3094_next": {
        "path": RESIDUALS / "P8_Y5_R2FR_3094_NEXT_TARGET.csv",
        "needles": ["NEXT3094_0_primary", "qbar_XT=0/J_X=0"],
        "role": "3094 selects qbarXT source-zero or bounded coupling row.",
    },
    "SRC3095_01_3094_doc": {
        "path": ROOT / "3094-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return-under-AX1090.md",
        "needles": ["SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW", "QBH3094_4_total_abs_guard"],
        "role": "3094 freezes finite range and hands off to qbarXT source-zero/bound envelope.",
    },
    "SRC3095_02_1849_doc": {
        "path": ROOT / "1849-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row.md",
        "needles": ["coupling fight with the fog removed", "bounded `qbar_XT` component envelope"],
        "role": "1849 precedent for active branch source-zero and qbar envelope.",
    },
    "SRC3095_03_1849_source_zero": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_SOURCE_ZERO_PROOF_AUDIT.csv",
        "needles": ["QZ1849_6_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1849 source-zero theorem remains conditional.",
    },
    "SRC3095_04_1849_pullback": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_MATTER_PULLBACK_DERIVATION.csv",
        "needles": ["MPD1849_6_current_verdict", "FAIL_CURRENT_CLAIM_QBARXT_ZERO_NOT_SIGNED"],
        "role": "1849 matter pullback zero derivation remains unsigned.",
    },
    "SRC3095_05_1849_premises": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_MATTER_PULLBACK_PREMISE_GATE.csv",
        "needles": ["MPG1849_6_verdict", "FAIL_CURRENT_CLAIM_MATTER_PULLBACK_NOT_SIGNED"],
        "role": "1849 premise gate lists missing matter/coframe/no-marker clauses.",
    },
    "SRC3095_06_1849_counterexamples": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_COUNTEREXAMPLE_GUARD.csv",
        "needles": ["CE1849_0_common_Weyl", "CE1849_3_nonHilbert_tail"],
        "role": "1849 counterexamples block weak source-zero claims.",
    },
    "SRC3095_07_1849_bounded_schema": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_BOUNDED_QBARXT_ROW_SCHEMA.csv",
        "needles": ["BQT1849_4_claim_gate", "CLAIM_BLOCKED"],
        "role": "1849 bounded qbarXT row schema.",
    },
    "SRC3095_08_1849_component_envelope": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_QBARXT_COMPONENT_ENVELOPE.csv",
        "needles": ["QBC1849_5_total_abs_guard", "SCHEMA_READY_VALUES_MISSING"],
        "role": "1849 qbarXT component envelope.",
    },
    "SRC3095_09_1027_source_zero": {
        "path": RESIDUALS / "P8_Y5_R10_1027_SOURCE_ZERO_PROOF_AUDIT.csv",
        "needles": ["QZ1027_6_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1027 source-zero proof audit precedent.",
    },
    "SRC3095_10_1027_qbar_schema": {
        "path": RESIDUALS / "P8_Y5_R10_1027_BOUNDED_QBARXT_ROW_SCHEMA.csv",
        "needles": ["BQT1027_3_total_abs_guard", "SCHEMA_READY_VALUES_MISSING"],
        "role": "1027 bounded qbarXT schema precedent.",
    },
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3095_SOURCE_REGISTER.csv",
    "source_zero": RESIDUALS / "P8_Y5_R2FR_3095_SOURCE_ZERO_PROOF_AUDIT.csv",
    "pullback": RESIDUALS / "P8_Y5_R2FR_3095_MATTER_PULLBACK_DERIVATION.csv",
    "premise_gate": RESIDUALS / "P8_Y5_R2FR_3095_MATTER_PULLBACK_PREMISE_GATE.csv",
    "counterexamples": RESIDUALS / "P8_Y5_R2FR_3095_COUNTEREXAMPLE_GUARD.csv",
    "bounded_schema": RESIDUALS / "P8_Y5_R2FR_3095_BOUNDED_QBARXT_ROW_SCHEMA.csv",
    "component_envelope": RESIDUALS / "P8_Y5_R2FR_3095_QBARXT_COMPONENT_ENVELOPE.csv",
    "dependencies": RESIDUALS / "P8_Y5_R2FR_3095_DEPENDENCY_LINKS.csv",
    "refusal": RESIDUALS / "P8_Y5_R2FR_3095_PLACEHOLDER_REFUSAL_RUNNER.csv",
    "verdicts": RESIDUALS / "P8_Y5_R2FR_3095_BRANCH_VERDICTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3095_CLAIM_GATE.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3095_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3095_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3095_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3095_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "source_zero_copy": LOCAL_BOUNDS / "qbarXT_source_zero_audit_3095_NONCLAIM.csv",
    "bounded_schema_copy": LOCAL_BOUNDS / "bounded_qbarXT_row_schema_3095_NONCLAIM.csv",
    "component_envelope_copy": LOCAL_BOUNDS / "qbarXT_component_envelope_3095_NONCLAIM.csv",
    "verdicts_copy": LOCAL_BOUNDS / "branch_verdicts_3095_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3095_frame_marker_coupling_or_no_marker_NEXT_NONCLAIM.csv",
}


def meta() -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def remove_pycache() -> None:
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def file_hash(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def source_parse_ok(path: Path) -> bool:
    return csv_ok(path) if path.suffix.lower() == ".csv" else path.exists()


def with_meta(output_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    base = meta()
    return [{**base, **row} for row in output_rows]


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in output_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in output_rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def source_rows() -> list[dict[str, Any]]:
    output_rows = []
    for source_id, source in SOURCES.items():
        path = Path(source["path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        output_rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "parse_ok": source_parse_ok(path),
                "sha256": file_hash(path),
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
            }
        )
    return with_meta(output_rows)


def source_zero_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "proof_id": "QZ3095_0_chain_rule",
                "target": "qbar_XT=0/J_matter_pullback=0",
                "required_statement": "If X is vertical to q, e_obs=Obs_e(q(Phi)), S_matter=Sbar[psi,e_obs,theta_A], and Lie_vX theta_A=0, then Lie_vX S_matter=0.",
                "current_evidence": "chain-rule theorem is valid conditionally in 1027/1849 and matter-pullback identity is exact",
                "status": "CONDITIONAL_THEOREM_VALID",
                "missing_for_claim": "parent-signed q/v_X, observed coframe functor, matter functor, no-marker constants and hidden-tail silence",
                "if_missing": "retain qbar_XT as finite source/test coupling",
            },
            {
                "proof_id": "QZ3095_1_q_verticality",
                "target": "Dq[v_X]=0",
                "required_statement": "X is a representative/gauge direction before variation, not a physical quotient observable.",
                "current_evidence": "3091 quotient route failed current branch; no-pole certificate remains conditional",
                "status": "MISSING_PARENT_Q_KERNEL_CERTIFICATE",
                "missing_for_claim": "presymplectic-null kernel, boundary flux zero and degree-count/no-pole proof",
                "if_missing": "ordinary matter can see an X-dependent observed-frame or source channel",
            },
            {
                "proof_id": "QZ3095_2_observed_coframe",
                "target": "Lie_vX e_obs=0",
                "required_statement": "e_obs=Obs_e(q(Phi)) is parent-signed and no representative Weyl/disformal frame affects rods, clocks, masses, charges or free fall.",
                "current_evidence": "frame/coframe descent is conditional; component rows retain frame-leak channels",
                "status": "MISSING_OBS_E_DESCENT_OR_FRAME_LEAK_ZERO",
                "missing_for_claim": "q/Obs_e parent signature and no-shadow-frame theorem or sourced frame-leak bounds",
                "if_missing": "qbar_XT can re-enter through common Weyl/disformal coupling",
            },
            {
                "proof_id": "QZ3095_3_matter_functor",
                "target": "S_matter descends through observed variables only",
                "required_statement": "S_matter=sum_A S_A[psi_A,e_obs,omega[e_obs],theta_A] for all ordinary matter/readout species.",
                "current_evidence": "matter functor contract exists but remains parent-unsigned",
                "status": "EXACT_CONTRACT_NOT_PARENT_SIGNED",
                "missing_for_claim": "parent principle selecting strict local observed coframe and one matter/source/readout action",
                "if_missing": "matter action can contain a direct X-sensitive frame/source slot",
            },
            {
                "proof_id": "QZ3095_4_no_marker_constants",
                "target": "Lie_vX theta_A=0",
                "required_statement": "material constants, masses, clocks, EM constants and readout markers are quotient-owned/superselected, not vertical fields.",
                "current_evidence": "no-marker and material-marker counterexamples survive",
                "status": "MISSING_NO_MARKER_THEOREM",
                "missing_for_claim": "constant/mass/EM/material-marker descent or numeric b_A/b_alpha bounds",
                "if_missing": "WEP can pass by species-blindness while common source-normalization survives",
            },
            {
                "proof_id": "QZ3095_5_hidden_source_tail",
                "target": "no hidden non-Hilbert/source/domain tail",
                "required_statement": "non-Hilbert current, support shift, boundary tail, domain projector and source-normalization residuals are theorem-zero or bounded.",
                "current_evidence": "non-Hilbert/source/support residuals stay in qbar component envelope",
                "status": "MISSING_HIDDEN_SOURCE_ZERO_OR_BOUND",
                "missing_for_claim": "q_nonH, Delta_W_support, domain/boundary/source-normalization rows with units and source paths",
                "if_missing": "qbar_XT=0 for visible matter still may not silence total local coupling",
            },
            {
                "proof_id": "QZ3095_6_verdict",
                "target": "qbar_XT/J_X source-zero theorem",
                "required_statement": "QZ3095_1 through QZ3095_5 all close from the same parent branch.",
                "current_evidence": "conditional pieces exist, but no single parent certificate closes",
                "status": "FAIL_CURRENT_CLAIM",
                "missing_for_claim": "q-kernel, observed coframe, matter functor, no-marker and hidden-source/boundary silence",
                "if_missing": "bounded qbar_XT component envelope remains mandatory",
            },
        ]
    )


def pullback_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "derivation_id": "MPD3095_0_target",
                "claim_piece": "ordinary test-body X charge",
                "formula": "qbar_XT := M_T^-1 delta_{v_X} S_T",
                "derivation_result": "TARGET_RESTATED",
                "proof_status": "NOT_A_CLAIM",
                "gap": "requires parent-owned vertical action on matter and matter functor descent",
                "claim_allowed": False,
            },
            {
                "derivation_id": "MPD3095_1_chain_rule_identity",
                "claim_piece": "chain-rule variation",
                "formula": "delta_v S_T = 1/2 int sqrt(-g_hat) T_T^{mu nu} Lie_v ghat_munu + sum_a int J_theta^a Lie_v theta_a + boundary/gauge/E_Psi terms",
                "derivation_result": "DERIVED_STANDARD_ON_SHELL_IDENTITY",
                "proof_status": "CONDITIONAL_MATH_OK",
                "gap": "zero only if geometry, constants, matter lift and boundary terms descend",
                "claim_allowed": False,
            },
            {
                "derivation_id": "MPD3095_2_geometry_pullback_zero",
                "claim_piece": "observed geometry X-blindness",
                "formula": "if ghat=ghat(q_loc(Phi)) and Dq_loc[v_X]=0, then Lie_v ghat_munu=0 up to owned gauge",
                "derivation_result": "SUFFICIENT_SUBLEMMA_WRITTEN",
                "proof_status": "PARENT_FUNCTOR_UNSIGNED",
                "gap": "unique observed coframe/metric functor not parent-derived in current corpus",
                "claim_allowed": False,
            },
            {
                "derivation_id": "MPD3095_3_constants_zero",
                "claim_piece": "constant/marker silence",
                "formula": "Lie_v theta_a=0 for masses, charges, alpha_EM, clocks, species labels and material markers",
                "derivation_result": "SUFFICIENT_SUBLEMMA_WRITTEN",
                "proof_status": "NO_MARKER_UNSIGNED",
                "gap": "ordinary constants can carry source/test charge unless no-marker theorem or coefficients close",
                "claim_allowed": False,
            },
            {
                "derivation_id": "MPD3095_4_tail_zero",
                "claim_piece": "boundary/domain/non-Hilbert silence",
                "formula": "boundary + gauge + support + non-Hilbert terms vanish or enter qbar_nonH bound",
                "derivation_result": "FALLBACK_COMPONENTIZED",
                "proof_status": "BOUND_SCHEMA_ONLY",
                "gap": "component values or theorem-zero rows missing",
                "claim_allowed": False,
            },
            {
                "derivation_id": "MPD3095_5_exact_theorem_if_signed",
                "claim_piece": "conditional matter-pullback theorem",
                "formula": "geometry pullback + constants zero + owned matter lift + boundary silence imply delta_v S_T=0, hence qbar_XT=0 and J_matter=0",
                "derivation_result": "EXACT_CONDITIONAL_THEOREM",
                "proof_status": "NOT_PARENT_SIGNED",
                "gap": "strong future parent-action contract, not a current MTS proof",
                "claim_allowed": False,
            },
            {
                "derivation_id": "MPD3095_6_current_verdict",
                "claim_piece": "current MTS matter-pullback zero",
                "formula": "qbar_XT=0 and J_matter=0 cannot be promoted until parent matter functor and no-marker/source-current clauses are signed",
                "derivation_result": "FAIL_CURRENT_CLAIM_QBARXT_ZERO_NOT_SIGNED",
                "proof_status": "RESIDUAL_REQUIRED",
                "gap": "build nonclaim qbarXT component envelope and keep WEP/R10/clock links active",
                "claim_allowed": False,
            },
        ]
    )


def premise_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("MPG3095_0_parent_matter_functor", "S_matter=sum_A S_A[Psi_A,e_obs(q_loc(Phi)),omega[e_obs],theta_A]", "geometry and matter-domain pullback", "NOT_PARENT_SIGNED", "qbar_geom and frame/source residuals remain active"),
        ("MPG3095_1_vertical_kernel", "v_X in ker(Dq_loc) with owned fixed/gauge lift on Psi_A", "Lie_v e_obs=0 and no physical matter transformation", "NOT_PARENT_SIGNED", "representative motion may be physical fifth-force/source charge"),
        ("MPG3095_2_constant_superselection", "Lie_v theta_A=0 for masses, charges, alpha_EM, clocks and representation labels", "no constant/clock/material qbar channel", "NOT_PARENT_SIGNED", "qbar_marker and clock/fine-structure rows remain active"),
        ("MPG3095_3_no_marker_extension", "no direct material marker, hidden conformal/disformal frame, source-only coefficient or post-readout EFT counterterm", "no hidden fifth-force loophole", "CONTRACT_WRITTEN_NOT_DERIVED", "relative species/source charges survive even when Ward identities hold"),
        ("MPG3095_4_boundary_support_silence", "matter edge/worldtube boundary terms vanish or are retained with source-backed bounds", "chain-rule boundary term cannot hide qbarXT", "OPEN", "qbar_nonH and boundary/source support residuals remain active"),
        ("MPG3095_5_universal_source_current", "source current entering local gravity is the same observed Hilbert current for all ordinary matter", "no hidden source-weight split", "NOT_PARENT_SIGNED", "qbar_source_weight remains active"),
        ("MPG3095_6_verdict", "all matter-pullback gates pass simultaneously", "J_matter=0 and qbar_XT=0 claim", "FAIL_CURRENT_CLAIM_MATTER_PULLBACK_NOT_SIGNED", "qbarXT bound fallback is mandatory"),
    ]
    return with_meta(
        [
            {
                "gate_id": gate_id,
                "premise": premise,
                "needed_for": needed_for,
                "current_status": status,
                "if_missing": if_missing,
                "gate_pass": False,
            }
            for gate_id, premise, needed_for, status, if_missing in gates
        ]
    )


def counterexample_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "counterexample_id": "CE3095_0_common_Weyl",
                "weak_premise": "universal covariant matter coupling",
                "construction": "e_m=A_g(X)e_obs or g_m=exp(2F(X))g_obs for all species",
                "failure": "WEP composition spread can vanish while qbar_XT is common nonzero source charge",
                "required_repair": "prove A_g'(0)=0/no-shadow-frame theorem or source c_g/b_g bound",
                "blocks_zero_claim": True,
            },
            {
                "counterexample_id": "CE3095_1_disformal_frame",
                "weak_premise": "single observed coframe notation",
                "construction": "g_m=A_g(X)^2 g_obs+B_g(X)U_muU_nu",
                "failure": "preferred-frame/PPN/clock source can survive coframe projection",
                "required_repair": "disformal absence theorem or PPN/preferred-frame bound row",
                "blocks_zero_claim": True,
            },
            {
                "counterexample_id": "CE3095_2_material_marker",
                "weak_premise": "matter geometry is X-blind",
                "construction": "theta_A(X), m_A(X), alpha_EM(X), or material class labels enter ordinary matter constants",
                "failure": "delta_X S_matter returns through constants even when partial_X e_obs=0",
                "required_repair": "no-marker theorem or material sensitivity b_A/b_alpha rows",
                "blocks_zero_claim": True,
            },
            {
                "counterexample_id": "CE3095_3_nonHilbert_tail",
                "weak_premise": "Hilbert matter current is standard",
                "construction": "non-Hilbert current, boundary/source support shift, or domain/projector tail",
                "failure": "ordinary Hilbert qbar_XT may be zero while source-normalization residual remains",
                "required_repair": "q_nonH/Delta_W_support/source-tail theorem-zero or bound rows",
                "blocks_zero_claim": True,
            },
            {
                "counterexample_id": "CE3095_4_frame_rename",
                "weak_premise": "rename variables to quotient frame",
                "construction": "field redefinition moves X coupling from metric to masses/constants",
                "failure": "source charge survives in transformed matter constants",
                "required_repair": "invariant qbar component accounting across frames",
                "blocks_zero_claim": True,
            },
        ]
    )


def bounded_schema_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "row_id": "BQT3095_0_visible_geometry",
                "symbol": "qbar_geom",
                "definition": "ordinary test-body X charge from representative Weyl/disformal observed-frame leakage",
                "formula_or_bound": "|qbar_geom| <= |tau_R10 c_g| + |tau_dis b_dis|",
                "required_columns": "system_id;test_body;lambda;tau_R10;c_g;tau_dis;b_dis;units;source_path;valid_for_claim",
                "current_status": "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND",
                "observable_link": "R10;PPN;clock;WEP",
            },
            {
                "row_id": "BQT3095_1_marker_constants",
                "symbol": "qbar_marker",
                "definition": "ordinary test-body X charge from masses, material constants, EM constants or clock markers",
                "formula_or_bound": "|qbar_marker| <= sum_A |s_A b_A| + |s_alpha b_alpha|",
                "required_columns": "system_id;material_pair;species_sensitivities;b_A;b_alpha;units;source_path;valid_for_claim",
                "current_status": "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS",
                "observable_link": "WEP;clock;composition;R10",
            },
            {
                "row_id": "BQT3095_2_nonHilbert_tail",
                "symbol": "qbar_nonH",
                "definition": "test/source coupling from non-Hilbert current, boundary tail, support shift, or domain projector",
                "formula_or_bound": "|qbar_nonH| <= |q_nonH| + |Delta_W_support| + |q_domain| + |q_boundary|",
                "required_columns": "system_id;arena;q_nonH;Delta_W_support;q_domain;q_boundary;units;source_path;valid_for_claim",
                "current_status": "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND",
                "observable_link": "R10;orbital;source_normalization;local_GR",
            },
            {
                "row_id": "BQT3095_3_source_weight",
                "symbol": "qbar_source_weight",
                "definition": "relative source-only weight in active gravitational source normalization",
                "formula_or_bound": "|qbar_source_weight| <= max_A |kappa_A/kappa_univ - 1| plus calibration tail",
                "required_columns": "system_id;source_class;kappa_A;kappa_univ;calibration_tail;units;source_path;valid_for_claim",
                "current_status": "MISSING_UNIVERSAL_SOURCE_CURRENT_OR_NUMERIC_BOUND",
                "observable_link": "WEP;orbital;R10_source_mass;local_GR",
            },
            {
                "row_id": "BQT3095_4_total_abs_guard",
                "symbol": "qbar_XT_bound_abs",
                "definition": "no-cancellation envelope for ordinary test-body X charge",
                "formula_or_bound": "|qbar_XT| <= |qbar_geom| + |qbar_marker| + |qbar_nonH| + |qbar_source_weight|",
                "required_columns": "system_id;lambda;abs_qbar_geom;abs_qbar_marker;abs_qbar_nonH;abs_qbar_source_weight;qbar_XT_bound_abs;units;source_paths;valid_for_claim",
                "current_status": "SCHEMA_READY_VALUES_MISSING",
                "observable_link": "R10;WEP;clock;PPN;local_GR",
            },
            {
                "row_id": "BQT3095_5_claim_gate",
                "symbol": "qbar_XT_claim_gate",
                "definition": "qbar_XT zero or bound can be claimed only after every component has theorem-zero or numeric bound",
                "formula_or_bound": "valid_for_claim=true only if no MISSING markers and qbar_XT_bound_abs has units/source paths",
                "required_columns": "all_component_statuses;all_source_paths;units;normalization;valid_for_claim",
                "current_status": "CLAIM_BLOCKED",
                "observable_link": "all_local_arenas",
            },
        ]
    )


def component_envelope_rows() -> list[dict[str, Any]]:
    components = [
        ("QBC3095_0_qbar_geom", "qbar_geom", "ordinary test-body X charge from observed metric/coframe leakage", "qbar_geom=(2 M_T)^-1 int sqrt(-g_hat) T_T^{mu nu} Lie_v ghat_munu", "Lie_v ghat_munu or theorem-zero geometry descent certificate", "MISSING_LIE_V_GHAT", "dimensionless_after_normalization", "R10;PPN;clock;WEP_direct_geometry", "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND"),
        ("QBC3095_1_qbar_constants", "qbar_constants", "ordinary test-body X charge from masses, charges, alpha_EM, clock, or representation constants", "qbar_constants=M_T^-1 sum_a int J_theta^a Lie_v theta_a", "constant-superselection theorem or dtheta_a/dX coefficients with source paths", "MISSING_DTHETA_DX", "dimensionless_after_sensitivity_normalization", "WEP;clock;fine_structure;R10", "MISSING_NO_MARKER_CONSTANT_THEOREM_OR_NUMERIC_BOUND"),
        ("QBC3095_2_qbar_marker", "qbar_marker", "source/test charge from material markers, hidden frames, direct MTS vertices, or post-readout masks", "|qbar_marker| <= sum |s_marker b_marker| over declared channels", "no-marker theorem or marker sensitivities and coefficients", "MISSING_MARKER_COEFFICIENTS", "dimensionless", "WEP_source_charge;clock;R11;R10", "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS"),
        ("QBC3095_3_qbar_source_weight", "qbar_source_weight", "relative species or class source-only weight in the active gravitational source", "|qbar_source_weight| <= max_A |kappa_A/kappa_univ - 1| plus measured-GM calibration tail", "minimal matter action source-current theorem or source-weight split values", "MISSING_DELTA_KAPPA_A", "dimensionless_after_source_normalization", "WEP_source_charge;orbital;R10_source_mass", "MISSING_UNIVERSAL_SOURCE_CURRENT_OR_NUMERIC_BOUND"),
        ("QBC3095_4_qbar_nonH", "qbar_nonH", "non-Hilbert, boundary, connection, domain or support-shift contribution", "|qbar_nonH| <= |q_nonH| + |Delta_W_support| + |q_domain| + |q_boundary|", "hidden-source zero theorem or component numeric bounds", "MISSING_NONHILBERT_BOUND", "dimensionless_or_declared_component_units", "R10;orbital;source_normalization;boundary", "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND"),
        ("QBC3095_5_total_abs_guard", "qbar_XT_bound_abs", "no-cancellation envelope for ordinary test-body X charge", "|qbar_XT| <= |qbar_geom|+|qbar_constants|+|qbar_marker|+|qbar_source_weight|+|qbar_nonH|", "all components theorem-zero or source-backed numeric bounds", "MISSING_COMPONENT_VALUES", "dimensionless_after_declared_normalization", "R10;WEP;clock;PPN;local_GR", "SCHEMA_READY_VALUES_MISSING"),
    ]
    return with_meta(
        [
            {
                "component_id": component_id,
                "symbol": symbol,
                "definition": definition,
                "formula_or_bound": formula,
                "required_input": required_input,
                "current_value": current_value,
                "units": units,
                "observable_links": observable_links,
                "status": status,
            }
            for component_id, symbol, definition, formula, required_input, current_value, units, observable_links, status in components
        ]
    )


def dependency_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "dependency_id": "DEP3095_0_alpha_product",
                "quantity": "alpha_bulk(lambda_X)",
                "depends_on": "K_X;Qbar_XH(lambda_X);qbar_XT;lambda_X;alpha_bound(lambda_X)",
                "current_status": "BLOCKED_BY_QBAR_AND_OTHER_INPUTS",
                "why": "qbar_XT is only one factor; qbar_XT bound also needs K_X, Qbar_XH, lambda_X and real bound curve",
                "next_action": "keep alpha row nonclaim until every factor is sourced",
            },
            {
                "dependency_id": "DEP3095_1_source_zero_stronger",
                "quantity": "qbar_XT=0",
                "depends_on": "q-kernel;Obs_e descent;matter functor;no-marker;hidden-tail silence",
                "current_status": "FAIL_CURRENT_CLAIM",
                "why": "conditional chain rule is valid but parent certificate does not close",
                "next_action": "do not set alpha to zero by qbar_XT unless certificate closes",
            },
            {
                "dependency_id": "DEP3095_2_bound_fallback",
                "quantity": "qbar_XT_bound_abs",
                "depends_on": "c_g;b_dis;b_A;b_alpha;q_nonH;Delta_W_support;q_domain;q_boundary",
                "current_status": "SCHEMA_READY_VALUES_MISSING",
                "why": "surviving counterexamples are componentized into bounded source rows",
                "next_action": "source first real c_g/b_A/q_nonH rows or prove theorem-zero",
            },
            {
                "dependency_id": "DEP3095_3_local_GR",
                "quantity": "local GR/Newton recovery",
                "depends_on": "qbar_XT=0 or bounded negligible; no-pole/source-zero; PPN residual vector",
                "current_status": "BLOCKED_PENDING_COUPLING_INPUTS",
                "why": "local extra channel cannot be removed or scored without qbarXT component closure",
                "next_action": "attack frame/marker/no-marker theorem and bounded rows",
            },
        ]
    )


def refusal_rows() -> list[dict[str, Any]]:
    refusals = [
        ("REF3095_0_qbar_zero", "qbar_XT=0", "FAIL_CURRENT_CLAIM_QBARXT_ZERO_NOT_SIGNED", "MPG3095_0_parent_matter_functor;MPG3095_1_vertical_kernel;MPG3095_2_constant_superselection;MPG3095_3_no_marker_extension;MPG3095_4_boundary_support_silence;MPG3095_5_universal_source_current;MPG3095_6_verdict"),
        ("REF3095_1_Jmatter_zero", "J_matter=0", "FAIL_CURRENT_CLAIM_QBARXT_ZERO_NOT_SIGNED", "parent matter functor and no-marker/source-current clauses unsigned"),
        ("REF3095_2_qbar_bound_values", "qbar_XT_bound_abs", "SCHEMA_READY_VALUES_MISSING", "QBC3095_0_qbar_geom;QBC3095_1_qbar_constants;QBC3095_2_qbar_marker;QBC3095_3_qbar_source_weight;QBC3095_4_qbar_nonH;QBC3095_5_total_abs_guard"),
        ("REF3095_3_local_GR", "local GR/Newton", "BLOCKED", "source-zero, no-pole, bounded qbar, PPN residual and boundary gates unsigned"),
    ]
    return with_meta(
        [
            {
                "refusal_id": refusal_id,
                "claim": claim,
                "computed_status": status,
                "runner_result": "BLOCKED",
                "blocking_rows": blocking_rows,
                "claim_allowed_for_physics": False,
            }
            for refusal_id, claim, status, blocking_rows in refusals
        ]
    )


def verdict_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "verdict_id": "BV3095_0_conditional_zero",
                "branch": "qbar_XT source-zero",
                "status": "CONDITIONAL_THEOREM_VALID_NOT_PARENT_SIGNED",
                "because": "chain-rule zero works if q, Obs_e, S_matter, theta_A and hidden tails are all parent-owned",
                "allowed_statement": "MTS has exact source-zero theorem target",
                "forbidden_statement": "current MTS has qbar_XT=0",
                "next_action": "retain qbar_XT as source-coupling row unless parent certificate closes",
            },
            {
                "verdict_id": "BV3095_1_counterexamples",
                "branch": "weak-premise shortcut rejection",
                "status": "COUNTEREXAMPLES_BLOCK_ZERO_CLAIM",
                "because": "universal Weyl, disformal, marker constants, source weights and non-Hilbert tails remain legal",
                "allowed_statement": "WEP/species-blindness can help but is not source-zero",
                "forbidden_statement": "WEP/covariance alone kills qbar_XT",
                "next_action": "source or zero each counterexample component",
            },
            {
                "verdict_id": "BV3095_2_bound_schema",
                "branch": "bounded qbarXT fallback",
                "status": "SCHEMA_READY_VALUES_MISSING",
                "because": "component rows define how to bound qbar_XT without cancellation, but no numeric/theorem-zero inputs are filled",
                "allowed_statement": "bounded coupling interface is ready",
                "forbidden_statement": "bounded coupling has passed a local test",
                "next_action": "fill first real frame/marker/non-Hilbert source row",
            },
            {
                "verdict_id": "BV3095_3_next_target",
                "branch": "next target",
                "status": "FRAME_MARKER_BOUND_INPUT_OR_NO_MARKER_THEOREM",
                "because": "proof route failed current claim; next honest move is stronger no-marker theorem or first real bound rows",
                "allowed_statement": "3096 should attack c_g/b_A/q_nonH first rows or no-marker theorem",
                "forbidden_statement": "run local tests as claim before qbarXT row is real",
                "next_action": "3096-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem-under-AX1090.md",
            },
        ]
    )


def gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG3095_0_sources_registered", "3095 source chain exists", False, "source chain supports audit continuity only"),
        ("CG3095_1_chain_rule_shape", "chain-rule source-zero theorem shape is claim-active", False, "conditional theorem written, but parent premises are unsigned"),
        ("CG3095_2_counterexample_guard", "weak shortcuts are excluded", False, "counterexamples are listed but not repaired"),
        ("CG3095_3_matter_pullback", "matter functor pullback is parent-signed", False, "matter functor/vertical kernel/constants/boundary/support clauses do not close"),
        ("CG3095_4_qbarXT_zero_claim", "qbar_XT/J_X source-zero may be claimed", False, "required clauses do not close together"),
        ("CG3095_5_qbarXT_bound_claim", "qbar_XT bound row may be scored", False, "component values and source paths are missing"),
        ("CG3095_6_local_GR_claim", "local GR/Newton reduction is derived", False, "source-zero, no-pole, Hessian, boundary and PPN gates remain unsigned"),
    ]
    return with_meta(
        [
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_pass": gate_pass,
                "reason": reason,
                "claim_allowed": False,
                "claim_allowed_for_physics": False,
            }
            for gate_id, claim, gate_pass, reason in gates
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "decision_id": "DEC3095_0_zero_result",
                "decision": "qbar_XT=0/J_X=0 is an exact conditional theorem but not a current MTS result.",
                "because": "parent q-kernel, observed coframe descent, matter functor, no-marker constants and hidden-source silence are not signed together",
                "next_action": "do not claim source-zero or local GR from chain rule alone",
            },
            {
                "decision_id": "DEC3095_1_bound_schema",
                "decision": "The bounded qbar_XT row schema is staged.",
                "because": "surviving counterexamples map cleanly into c_g/b_dis/b_A/b_alpha/q_nonH/support/source-weight components",
                "next_action": "fill real theorem-zero or numeric bounds before scoring",
            },
            {
                "decision_id": "DEC3095_2_coupling_status",
                "decision": "The coupling gap is now a source-row problem, not a vague criticism.",
                "because": "qbar_XT has named components, dependencies, observables and no-cancellation policy",
                "next_action": "source first c_g/b_A/q_nonH rows or derive no-marker theorem",
            },
            {
                "decision_id": "DEC3095_3_next_target",
                "decision": "Next target is frame/marker coupling bound input pack or no-marker theorem.",
                "because": "clean zero proof did not close; next honest progress is stronger parent no-marker theorem or first real bound rows",
                "next_action": "3096-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem-under-AX1090.md",
            },
        ]
    )


def next_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "route_id": "NEXT3095_0_primary",
                "next_checkpoint": "3096-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem-under-AX1090.md",
                "script": "scripts/Y5_R2FR_frame_marker_coupling_bound_input_pack_or_no_marker_theorem_under_AX1090_3096.py",
                "objective": "try to derive the no-marker/constant-descent theorem for ordinary matter; if unsigned, build first claim-blocked c_g, b_dis, b_A, b_alpha, q_nonH and support-shift bound rows with units, source paths and observable links",
                "selection_status": "selected",
                "success_condition": "no-marker theorem closes, or frame/marker/source bound input pack is complete and nonclaim",
            },
            {
                "route_id": "NEXT3095_1_parallel",
                "next_checkpoint": "3096b-Y5-R2FR-parent-matter-functor-descent-signature-under-AX1090.md",
                "script": "scripts/Y5_R2FR_parent_matter_functor_descent_signature_under_AX1090_3096b.py",
                "objective": "try to sign the parent ordinary-matter functor and vertical matter lift directly",
                "selection_status": "held",
                "success_condition": "one parent matter functor row signs geometry pullback, matter lift, constants and boundary silence together",
            },
        ]
    )


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = {
        "source_zero_copy": OUTPUTS["source_zero"],
        "bounded_schema_copy": OUTPUTS["bounded_schema"],
        "component_envelope_copy": OUTPUTS["component_envelope"],
        "verdicts_copy": OUTPUTS["verdicts"],
        "next_copy": OUTPUTS["next"],
    }
    output_rows = []
    for key, source_path in copies.items():
        target_path = BRANCH_OUTPUTS[key]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        output_rows.append(
            {
                **meta(),
                "copy_id": f"COPY3095_{key}",
                "source_path": str(source_path),
                "target_path": str(target_path),
                "target_exists": target_path.exists(),
            }
        )
    write_csv(OUTPUTS["branches"], output_rows)
    return output_rows


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in output_rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 3095 Y5 R2FR qbarXT source-zero or bounded coupling row under AX1090",
        "",
        "**Progress:** 3095 ports the source-zero route into the current AX1090 branch. The chain-rule proof is exact as conditional mathematics: if matter only sees quotient-owned observed variables and constants are vertical-trivial, then `qbar_XT=0` and `J_matter=0` for ordinary matter.",
        "",
        "**Current verdict:** the zero theorem is not an active MTS claim. The parent q-kernel, observed coframe, matter functor, no-marker constants, hidden source tails, source-current universality, and boundary support do not close together. The bounded `qbar_XT` component envelope is staged but value-missing.",
        "",
        "**Claim ceiling:** no source-zero claim, finite-alpha pass, R10/WEP/clock/PPN/orbital pass, local-GR/Newton reduction, GitHub action, or `formalization-workbench` edit is allowed from 3095.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "parse_ok", "needles_present", "missing_needles", "role"]),
        "",
        "## Source-Zero Proof Audit",
        markdown_table(data["source_zero"], ["proof_id", "target", "required_statement", "current_evidence", "status", "missing_for_claim", "if_missing", "valid_for_claim"]),
        "",
        "## Matter Pullback Derivation",
        markdown_table(data["pullback"], ["derivation_id", "claim_piece", "formula", "derivation_result", "proof_status", "gap", "claim_allowed", "valid_for_claim"]),
        "",
        "## Matter Pullback Premise Gate",
        markdown_table(data["premise_gate"], ["gate_id", "premise", "needed_for", "current_status", "if_missing", "gate_pass", "valid_for_claim"]),
        "",
        "## Counterexample Guard",
        markdown_table(data["counterexamples"], ["counterexample_id", "weak_premise", "construction", "failure", "required_repair", "blocks_zero_claim", "valid_for_claim"]),
        "",
        "## Bounded qbarXT Row Schema",
        markdown_table(data["bounded_schema"], ["row_id", "symbol", "definition", "formula_or_bound", "required_columns", "current_status", "observable_link", "valid_for_claim"]),
        "",
        "## qbarXT Component Envelope",
        markdown_table(data["component_envelope"], ["component_id", "symbol", "definition", "formula_or_bound", "required_input", "current_value", "units", "observable_links", "status", "valid_for_claim"]),
        "",
        "## Dependency Links",
        markdown_table(data["dependencies"], ["dependency_id", "quantity", "depends_on", "current_status", "why", "next_action", "valid_for_claim"]),
        "",
        "## Placeholder Refusal Runner",
        markdown_table(data["refusal"], ["refusal_id", "claim", "computed_status", "runner_result", "blocking_rows", "claim_allowed_for_physics", "valid_for_claim"]),
        "",
        "## Branch Verdicts",
        markdown_table(data["verdicts"], ["verdict_id", "branch", "status", "because", "allowed_statement", "forbidden_statement", "next_action", "valid_for_claim"]),
        "",
        "## Claim Gate",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed_for_physics", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "next_checkpoint", "script", "objective", "selection_status", "success_condition"]),
        "",
        "## Validation",
        markdown_table(data["validation"], ["validation_id", "check_pass", "detail", "artifact"]),
        "",
        "## Working Interpretation",
        "This is the coupling fight with the fog removed. The route to local GR is not `qbar is small because vibes`; it is either a signed source-zero theorem or a bounded residual vector with frame, marker, source-weight and non-Hilbert components.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def contains_status(path: Path, field: str, expected: str) -> bool:
    return any(str(row.get(field, "")) == expected for row in rows(path))


def all_false(path: Path, field: str) -> bool:
    table = rows(path)
    return bool(table) and all(not boolish(row.get(field, "")) for row in table)


def validation_rows() -> list[dict[str, Any]]:
    formalization_3095 = list(FORMALIZATION.rglob("*3095*")) if FORMALIZATION.exists() else []
    checks = [
        ("VAL3095_00_sources_csv", csv_ok(OUTPUTS["sources"]), "source register parses", OUTPUTS["sources"]),
        ("VAL3095_01_sources_exist", all(boolish(row["exists"]) for row in rows(OUTPUTS["sources"])), "every cited local source path exists", OUTPUTS["sources"]),
        ("VAL3095_02_sources_parse", all(boolish(row["parse_ok"]) for row in rows(OUTPUTS["sources"])), "every cited csv source parses", OUTPUTS["sources"]),
        ("VAL3095_03_needles_present", all(boolish(row["needles_present"]) for row in rows(OUTPUTS["sources"])), "all source needles found", OUTPUTS["sources"]),
        ("VAL3095_04_doc_created", DOC.exists(), "checkpoint markdown created", DOC),
        ("VAL3095_05_source_zero_parse", csv_ok(OUTPUTS["source_zero"]), "source-zero audit parses", OUTPUTS["source_zero"]),
        ("VAL3095_06_source_zero_blocks", contains_status(OUTPUTS["source_zero"], "status", "FAIL_CURRENT_CLAIM"), "qbarXT source-zero theorem remains nonclaim", OUTPUTS["source_zero"]),
        ("VAL3095_07_pullback_parse", csv_ok(OUTPUTS["pullback"]), "matter pullback derivation parses", OUTPUTS["pullback"]),
        ("VAL3095_08_pullback_blocks", contains_status(OUTPUTS["pullback"], "derivation_result", "FAIL_CURRENT_CLAIM_QBARXT_ZERO_NOT_SIGNED"), "matter pullback zero remains unsigned", OUTPUTS["pullback"]),
        ("VAL3095_09_premise_gate_parse", csv_ok(OUTPUTS["premise_gate"]), "premise gate parses", OUTPUTS["premise_gate"]),
        ("VAL3095_10_premise_gate_blocks", contains_status(OUTPUTS["premise_gate"], "current_status", "FAIL_CURRENT_CLAIM_MATTER_PULLBACK_NOT_SIGNED"), "matter pullback premise gate blocks claim", OUTPUTS["premise_gate"]),
        ("VAL3095_11_counterexamples_parse", csv_ok(OUTPUTS["counterexamples"]), "counterexample guard parses", OUTPUTS["counterexamples"]),
        ("VAL3095_12_counterexamples_block", all(boolish(row["blocks_zero_claim"]) for row in rows(OUTPUTS["counterexamples"])), "all counterexamples block weak zero claims", OUTPUTS["counterexamples"]),
        ("VAL3095_13_bounded_schema_parse", csv_ok(OUTPUTS["bounded_schema"]), "bounded qbarXT schema parses", OUTPUTS["bounded_schema"]),
        ("VAL3095_14_bounded_schema_nonclaim", contains_status(OUTPUTS["bounded_schema"], "current_status", "CLAIM_BLOCKED") and all_false(OUTPUTS["bounded_schema"], "valid_for_claim"), "bounded qbarXT schema remains claim-blocked", OUTPUTS["bounded_schema"]),
        ("VAL3095_15_component_envelope_parse", csv_ok(OUTPUTS["component_envelope"]), "component envelope parses", OUTPUTS["component_envelope"]),
        ("VAL3095_16_component_guard_ready", contains_status(OUTPUTS["component_envelope"], "status", "SCHEMA_READY_VALUES_MISSING"), "component total guard staged but values missing", OUTPUTS["component_envelope"]),
        ("VAL3095_17_dependencies_parse", csv_ok(OUTPUTS["dependencies"]), "dependency links parse", OUTPUTS["dependencies"]),
        ("VAL3095_18_refusal_parse", csv_ok(OUTPUTS["refusal"]), "placeholder refusal runner parses", OUTPUTS["refusal"]),
        ("VAL3095_19_refusal_blocks_local_GR", contains_status(OUTPUTS["refusal"], "claim", "local GR/Newton"), "refusal runner blocks local GR claim", OUTPUTS["refusal"]),
        ("VAL3095_20_verdicts_parse", csv_ok(OUTPUTS["verdicts"]), "branch verdicts parse", OUTPUTS["verdicts"]),
        ("VAL3095_21_verdict_next", contains_status(OUTPUTS["verdicts"], "status", "FRAME_MARKER_BOUND_INPUT_OR_NO_MARKER_THEOREM"), "branch verdict selects frame/marker/no-marker target", OUTPUTS["verdicts"]),
        ("VAL3095_22_gates_parse", csv_ok(OUTPUTS["gates"]), "claim gates parse", OUTPUTS["gates"]),
        ("VAL3095_23_gates_blocked", all_false(OUTPUTS["gates"], "claim_allowed_for_physics"), "all claim gates remain blocked", OUTPUTS["gates"]),
        ("VAL3095_24_decisions_parse", csv_ok(OUTPUTS["decisions"]), "decision ledger parses", OUTPUTS["decisions"]),
        ("VAL3095_25_next_parse", csv_ok(OUTPUTS["next"]), "next target parses", OUTPUTS["next"]),
        ("VAL3095_26_next_selected", contains_status(OUTPUTS["next"], "selection_status", "selected"), "primary next target selected", OUTPUTS["next"]),
        ("VAL3095_27_branch_copies_parse", csv_ok(OUTPUTS["branches"]), "branch copy ledger parses", OUTPUTS["branches"]),
        ("VAL3095_28_branch_copies_exist", all(boolish(row["target_exists"]) for row in rows(OUTPUTS["branches"])), "all branch copies exist", OUTPUTS["branches"]),
        ("VAL3095_29_no_formalization_edit", len(formalization_3095) == 0, "no 3095 files created under formalization-workbench", FORMALIZATION),
        ("VAL3095_30_pycache_removed", not PYCACHE.exists(), "scripts __pycache__ absent after run", PYCACHE),
    ]
    return [
        {
            **meta(),
            "validation_id": validation_id,
            "check_pass": bool(check_pass),
            "detail": detail,
            "artifact": str(artifact),
        }
        for validation_id, check_pass, detail, artifact in checks
    ]


def main() -> None:
    remove_pycache()
    for directory in [RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_rows(),
        "source_zero": source_zero_rows(),
        "pullback": pullback_rows(),
        "premise_gate": premise_gate_rows(),
        "counterexamples": counterexample_rows(),
        "bounded_schema": bounded_schema_rows(),
        "component_envelope": component_envelope_rows(),
        "dependencies": dependency_rows(),
        "refusal": refusal_rows(),
        "verdicts": verdict_rows(),
        "gates": gate_rows(),
        "decisions": decision_rows(),
        "next": next_rows(),
    }

    for key, output_rows in data.items():
        write_csv(OUTPUTS[key], output_rows)

    data["branches"] = copy_branch_outputs()
    data["validation"] = []
    write_doc(data)
    data["validation"] = validation_rows()
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    passed = sum(1 for row in data["validation"] if boolish(row["check_pass"]))
    print(f"3095 qbarXT source-zero/bounded coupling checkpoint written: {passed}/{len(data['validation'])} validation checks passed")
    print(DOC)
    print(OUTPUTS["validation"])


if __name__ == "__main__":
    main()

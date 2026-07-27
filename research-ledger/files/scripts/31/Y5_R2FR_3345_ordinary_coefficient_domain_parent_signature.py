from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3345-Y5-R2FR-ordinary-coefficient-domain-parent-signature-under-AX1090.md"

SOURCES = [
    {
        "source_id": "SRC3345_0_3344_doc",
        "path": ROOT / "3344-Y5-R2FR-no-hidden-ZQ-or-alpha-drift-bound-under-AX1090.md",
        "role": "3344 handoff selecting ordinary coefficient-domain parent signature",
    },
    {
        "source_id": "SRC3345_1_3344_no_hidden_zq",
        "path": OUT / "P8_Y5_R2FR_3344_NO_HIDDEN_ZQ_THEOREM_OR_COUNTERMODEL.csv",
        "role": "no-hidden Z_Q theorem depends on A_ord signature",
    },
    {
        "source_id": "SRC3345_2_2659_domain",
        "path": OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
        "role": "typed no-hidden-visible-hom theorem",
    },
    {
        "source_id": "SRC3345_3_2611_descent",
        "path": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv",
        "role": "matter descent premise audit",
    },
    {
        "source_id": "SRC3345_4_2611_worldtube",
        "path": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_MATTER_WORLDTUBE_DESCENT_ATTEMPT.csv",
        "role": "matter/worldtube vertical source theorem",
    },
    {
        "source_id": "SRC3345_5_2612_grammar",
        "path": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv",
        "role": "no direct matter X vertex grammar",
    },
    {
        "source_id": "SRC3345_6_2613_hom",
        "path": OUT / "P8_Y5_HOM_EXCLUSION_GATE_2613_HOM_EXCLUSION_THEOREM_ATTEMPT.csv",
        "role": "no source-only Hom theorem",
    },
    {
        "source_id": "SRC3345_7_2614_forgetting",
        "path": OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_LABEL_FORGETTING_PROOF_ATTEMPT.csv",
        "role": "source label forgetting theorem",
    },
    {
        "source_id": "SRC3345_8_2614_requirements",
        "path": OUT / "P8_Y5_SPECIES_FORGETTING_GATE_2614_PARENT_SIGNATURE_REQUIREMENTS.csv",
        "role": "species/source parent signature requirements",
    },
    {
        "source_id": "SRC3345_9_2615_prefactor",
        "path": OUT / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NO_SOURCE_PREFACTOR_PROOF_ATTEMPT.csv",
        "role": "no source prefactor proof attempt",
    },
    {
        "source_id": "SRC3345_10_2616_exchange",
        "path": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv",
        "role": "ordinary matter exchange graph connectivity theorem",
    },
    {
        "source_id": "SRC3345_11_2616_shadow",
        "path": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_SOURCE_SHADOW_BAN_ATTEMPT.csv",
        "role": "source shadow ban attempt",
    },
    {
        "source_id": "SRC3345_12_2617_single_source",
        "path": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SINGLE_SOURCE_MAP_IDENTITY_THEOREM.csv",
        "role": "single source map identity theorem",
    },
    {
        "source_id": "SRC3345_13_2624_readout",
        "path": OUT / "P8_Y5_READOUT_SCHEMA_GATE_2624_READOUT_SCHEMA_THEOREM_ATTEMPT.csv",
        "role": "readout variation-after-solution theorem",
    },
    {
        "source_id": "SRC3345_14_2643_common_descent",
        "path": OUT / "P8_Y5_COMMON_DESCENT_DQZ_2643_PARENT_SIGNATURE_THEOREM_GATE.csv",
        "role": "common descent DqZ parent signature theorem gate",
    },
    {
        "source_id": "SRC3345_15_3340_parent_evidence",
        "path": OUT / "P8_Y5_R2FR_3340_PARENT_CLAUSE_EVIDENCE_SCORE.csv",
        "role": "current parent clause evidence status",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3345_SOURCE_REGISTER.csv",
    "signature": OUT / "P8_Y5_R2FR_3345_ORDINARY_COEFFICIENT_DOMAIN_SIGNATURE.csv",
    "theorem": OUT / "P8_Y5_R2FR_3345_DOMAIN_DERIVATIVE_ZERO_THEOREM.csv",
    "payoff": OUT / "P8_Y5_R2FR_3345_CLOSURE_PAYOFF_MATRIX.csv",
    "source_weight": OUT / "P8_Y5_R2FR_3345_SOURCE_WEIGHT_COLLAPSE_THEOREM.csv",
    "countermodels": OUT / "P8_Y5_R2FR_3345_SURVIVING_COUNTERMODEL_MATRIX.csv",
    "evidence_score": OUT / "P8_Y5_R2FR_3345_PARENT_SIGNATURE_EVIDENCE_SCORE.csv",
    "residual_interface": OUT / "P8_Y5_R2FR_3345_RESIDUAL_INTERFACE_IF_UNSIGNED.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3345_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3345_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3345_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3345_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def parent_signature_closed() -> bool:
    return False


def signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "OD3345_0_parent_quotient",
            "signature_piece": "parent quotient and vertical fibres",
            "required_form": "q:P_parent -> Q_obs with ordinary vertical directions v in ker(Dq)",
            "derivation_use": "defines what hidden/representative variation means",
            "current_status": "CONTRACT_PRESENT_NOT_PARENT_SIGNED",
            "source_path": str(OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv"),
            "passes_now": "false",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "OD3345_1_observed_geometry",
            "signature_piece": "observed metric/coframe descends",
            "required_form": "e_obs=e_bar(q(Phi)), g_obs=g_bar(q(Phi)), omega=omega[e_obs]",
            "derivation_use": "kills hidden metric/coframe derivatives inside ordinary matter",
            "current_status": "CONTRACT_PRESENT_NOT_PARENT_SIGNED",
            "source_path": str(OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv"),
            "passes_now": "false",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "OD3345_2_ordinary_coefficient_algebra",
            "signature_piece": "A_ord=q^*A_Q + A_fixed",
            "required_form": "Allowed ordinary coefficients are pullbacks from Q_obs plus fixed representation/calibration constants",
            "derivation_use": "for every c in A_ord, L_v c=0 when v in ker(Dq)",
            "current_status": "EXACT_TYPED_THEOREM_NOT_PARENT_SIGNED",
            "source_path": str(OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv"),
            "passes_now": "false",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "OD3345_3_single_matter_functional",
            "signature_piece": "ordinary matter action normal form",
            "required_form": "S_ord=sum_A S_A[Psi_A,e_obs(q(Phi)),A_Q(q(Phi)),theta_A_fixed]",
            "derivation_use": "same action owns dynamics and Hilbert/source stress",
            "current_status": "CONTRACT_WRITTEN_NOT_PARENT_DERIVED",
            "source_path": str(OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv"),
            "passes_now": "false",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "OD3345_4_no_source_shadow",
            "signature_piece": "identity source map",
            "required_form": "T_active := T_H := delta S_ord/delta g_obs with no F_shadow(T_H,labels)",
            "derivation_use": "prevents post-variation material/source projector from reintroducing coefficients",
            "current_status": "DERIVED_CONDITIONAL_NOT_PARENT_SIGNED",
            "source_path": str(OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SINGLE_SOURCE_MAP_IDENTITY_THEOREM.csv"),
            "passes_now": "false",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "OD3345_5_label_forgetting_exchange",
            "signature_piece": "ordinary source label forgetting / connected exchange graph",
            "required_form": "source functor receives T_total; connected ordinary exchange graph collapses residual block weights to common calibration",
            "derivation_use": "kills eta_species/source-only relative weights for ordinary matter if source-shadow is absent",
            "current_status": "DERIVED_CONDITIONAL_PRIVATE_GRAPH_NOT_SOURCED",
            "source_path": str(OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv"),
            "passes_now": "false",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "OD3345_6_readout_after_variation",
            "signature_piece": "readout/projector not in S_parent arguments",
            "required_form": "Conf_parent --EL--> Sol(S_parent) --R_read--> Obs; P_read/R_read excluded from Args(S_parent)",
            "derivation_use": "prevents readout/projector backreaction being counted as parent theorem-zero",
            "current_status": "CONDITIONAL_SCHEMA_NOT_PARENT_SIGNED",
            "source_path": str(OUT / "P8_Y5_READOUT_SCHEMA_GATE_2624_READOUT_SCHEMA_THEOREM_ATTEMPT.csv"),
            "passes_now": "false",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "OD3345_7_boundary_and_decoupled_inventory",
            "signature_piece": "boundary, projector, and decoupled-sector inventory",
            "required_form": "boundary/improvement terms silent or bounded; decoupled nonordinary blocks explicit per arena",
            "derivation_use": "keeps the theorem from hiding real residual sources",
            "current_status": "OPEN_BOUND_OR_INVENTORY_REQUIRED",
            "source_path": str(OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SOURCE_SHADOW_ZERO_ATTEMPT.csv"),
            "passes_now": "false",
            "valid_for_claim": "false",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "ODT3345_0_domain_derivative_zero",
            "claim_piece": "ordinary coefficient vertical silence",
            "statement": "If c_ord in A_ord=q^*A_Q + A_fixed and v in ker(Dq), then L_v c_ord=0.",
            "proof": "Write c_ord=q^*c_Q+c_fixed. L_v(q^*c_Q)=dc_Q[Dq(v)]=0 and L_v c_fixed=0.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ODT3345_1_action_descent_zero",
            "claim_piece": "ordinary matter hidden-source silence",
            "statement": "If S_ord factors through q and fixed representation data, delta_v S_ord is only an allowed boundary term.",
            "proof": "Chain rule: delta_v S_ord=DSbar[Dq(v)]+J_theta L_v theta + delta_v B. The first two terms vanish under OD3345_0..3.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ODT3345_2_source_map_identity",
            "claim_piece": "active ordinary source is Hilbert stress",
            "statement": "If T_active is defined before label exposure as delta S_ord/delta g_obs, post-variation source coefficients are not typed operations.",
            "proof": "A map F_shadow(T_H,labels) is an extra source-map argument; if it is varied it is a real action term, if not varied it is nonvariational/boundary/residual.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ODT3345_3_exchange_block_collapse",
            "claim_piece": "relative ordinary source weights collapse on connected exchange graph",
            "statement": "If ordinary matter exchange graph is connected and source owner is total Hilbert current, any conserved relative block prefactor reduces to one common calibration.",
            "proof": "Noether exchange requires sum_i w_i C_i^nu=0 on every exchange edge; nonzero connected edges force w_i=w_j across the component.",
            "status": "DERIVED_CONDITIONAL_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ODT3345_4_combined_parent_domain_signature",
            "claim_piece": "combined local coupling silence",
            "statement": "OD3345_0..7 jointly imply no hidden Z_Q drift, no ordinary source-only species weights, no direct matter-X vertex, and no readout source backreaction except explicit residual inventory.",
            "proof": "All dangerous maps require an argument outside q-visible data, A_fixed, total Hilbert variation, or post-solution readout. Those arguments are absent by typed parent signature.",
            "status": "EXACT_COMBINED_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def payoff_rows() -> list[dict[str, Any]]:
    return [
        {
            "payoff_id": "PAY3345_0_b_alpha",
            "target": "b_alpha / hidden Z_Q drift",
            "closed_if_signature": "yes",
            "mechanism": "Z_Q belongs to A_ord or A_fixed, so L_v ln Z_Q=0; constant alpha calibration may remain",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "payoff_id": "PAY3345_1_eta_species",
            "target": "eta_species / source-only species weights",
            "closed_if_signature": "yes_for_ordinary_connected_matter",
            "mechanism": "no source-only w_A slot plus total Hilbert source plus connected ordinary exchange graph leaves only common measured-G calibration",
            "current_status": "CONDITIONAL_GRAPH_CERTIFICATE_NOT_PUBLIC_SOURCED",
            "valid_for_claim": "false",
        },
        {
            "payoff_id": "PAY3345_2_delta_J",
            "target": "source/test current normalization",
            "closed_if_signature": "partial",
            "mechanism": "fixed representation charge lattice belongs to A_fixed and source-current map receives the same Noether current",
            "current_status": "CONDITIONAL_CURRENT_OWNER_STILL_NEEDS_3344b_OR_PARENT_SIGN",
            "valid_for_claim": "false",
        },
        {
            "payoff_id": "PAY3345_3_cg_bdis_shadow_frames",
            "target": "hidden conformal/disformal/source frames",
            "closed_if_signature": "yes",
            "mechanism": "ordinary matter evaluates e_obs(q(Phi)) and g_obs(q(Phi)) only; representative metric/coframe slots are not arguments",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "payoff_id": "PAY3345_4_readout_projectors",
            "target": "readout/projector backreaction",
            "closed_if_signature": "yes_if_no_reduced_action",
            "mechanism": "readout maps happen after solving; varied reduced/readout functionals are demoted to explicit residual branches",
            "current_status": "CONDITIONAL_PARENT_DOMAIN_NOT_CLOSED",
            "valid_for_claim": "false",
        },
        {
            "payoff_id": "PAY3345_5_local_GR_source_coupling",
            "target": "FRV3340 source-coupling vector",
            "closed_if_signature": "partial_large_chunk",
            "mechanism": "kills eta_species and b_alpha-style hidden coefficient leaks; still leaves tensor ratio, contact, boundary, Bianchi, and left-hand operator residuals",
            "current_status": "NOT_FULL_LOCAL_GR_CLAIM",
            "valid_for_claim": "false",
        },
    ]


def source_weight_rows() -> list[dict[str, Any]]:
    return [
        {
            "collapse_id": "SWC3345_0_same_action",
            "claim_piece": "source-shadow weights forbidden if source is same Hilbert variation",
            "derivation": "T_active=T_H is an identity; a source-only map is an extra parent operation, not a consequence of variation.",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "collapse_id": "SWC3345_1_exchange_graph",
            "claim_piece": "connected exchange graph collapses relative weights",
            "derivation": "For interacting subcurrents, weighted conservation requires equal weights on connected nodes; ordinary atomic matter is candidate-connected via EM/nuclear/binding stresses.",
            "status": "DERIVED_CONDITIONAL_GRAPH_CERTIFICATE_PRIVATE",
            "valid_for_claim": "false",
        },
        {
            "collapse_id": "SWC3345_2_common_mode",
            "claim_piece": "remaining common weight is measured-G calibration",
            "derivation": "A universal prefactor w_star rescales kappa_* and is absorbed by the measured Newtonian slot; it is not WEP composition dependence.",
            "status": "COMMON_MODE_CALIBRATION",
            "valid_for_claim": "false",
        },
        {
            "collapse_id": "SWC3345_3_decoupled_blocks",
            "claim_piece": "decoupled sectors are explicit arena inventory",
            "derivation": "If a truly conserved nonordinary block has no exchange edge, it must be declared present/absent per source arena and bounded if present.",
            "status": "RESIDUAL_INVENTORY_REQUIRED",
            "valid_for_claim": "false",
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CEX3345_0_hidden_scalar_coefficient",
            "surviving_map": "f_X(I_hid) F_Q^2",
            "why_survives_without_signature": "diffeomorphism and U(1) gauge symmetry allow it if hidden invariant scalar is in the ordinary coefficient domain",
            "affected_targets": "b_alpha; epsilon_EM; clocks; spectra; R10 alpha products",
            "required_exit": "parent-sign A_ord excludes I_hid or prove hidden invariant algebra is constant",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CEX3345_1_source_shadow_projector",
            "surviving_map": "T_active=P_material(T_H) or F_shadow(T_H,labels)",
            "why_survives_without_signature": "a post-variation source map can be covariant unless parent object language forbids it",
            "affected_targets": "eta_species; WEP; source composition; measured-G normalization",
            "required_exit": "identity source map or finite projector/source-shadow bound",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CEX3345_2_hidden_frame",
            "surviving_map": "g_A=A_A(X)^2 g_obs or disformal source/readout frame",
            "why_survives_without_signature": "terminal/public metric alone does not forbid a labelled matter frame before readout",
            "affected_targets": "c_g; b_dis; PPN; clocks; WEP",
            "required_exit": "ordinary matter argument list uses only e_obs/g_obs(q(Phi))",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CEX3345_3_reduced_readout_backreaction",
            "surviving_map": "S_red[g,P_read] varied as if parent action",
            "why_survives_without_signature": "reduced/readout EFT can create projector terms unless demoted before theorem-zero claims",
            "affected_targets": "readout leakage; projector commutator; PPN/R10/source residuals",
            "required_exit": "closed parent Args(S_parent) and reduced-action demotion policy",
            "valid_for_claim": "false",
        },
    ]


def evidence_score_rows() -> list[dict[str, Any]]:
    score_map = {
        "OD3345_0_parent_quotient": "CONTRACT_PRESENT_NOT_PARENT_SIGNED",
        "OD3345_1_observed_geometry": "CONTRACT_PRESENT_NOT_PARENT_SIGNED",
        "OD3345_2_ordinary_coefficient_algebra": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
        "OD3345_3_single_matter_functional": "CONTRACT_WRITTEN_NOT_PARENT_DERIVED",
        "OD3345_4_no_source_shadow": "DERIVED_CONDITIONAL_NOT_PARENT_SIGNED",
        "OD3345_5_label_forgetting_exchange": "DERIVED_CONDITIONAL_PRIVATE_GRAPH_NOT_SOURCED",
        "OD3345_6_readout_after_variation": "CONDITIONAL_SCHEMA_NOT_PARENT_SIGNED",
        "OD3345_7_boundary_and_decoupled_inventory": "OPEN_BOUND_OR_INVENTORY_REQUIRED",
    }
    return [
        {
            "score_id": f"EV3345_{index}",
            "clause_id": clause_id,
            "evidence_status": status,
            "passes_parent_signature": "false",
            "reason": "Current corpus provides a contract/conditional theorem, but not a closed parent action-domain certificate." if "OPEN" not in status else "Boundary/decoupled inventory still requires explicit bound or arena exclusion.",
            "valid_for_claim": "false",
        }
        for index, (clause_id, status) in enumerate(score_map.items())
    ]


def residual_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RES3345_0_E_coeff_domain",
            "symbol": "epsilon_coeff_domain",
            "definition": "absolute leakage from ordinary coefficient maps outside q^*A_Q + A_fixed",
            "bound_or_zero_route": "parent-sign OD3345_2 or bound each hidden coefficient derivative",
            "feeds": "b_alpha; masses; clocks; material markers; Hodge/readout constants",
            "status": "NONCLAIM_RESIDUAL_IF_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3345_1_E_source_shadow",
            "symbol": "epsilon_source_shadow",
            "definition": "post-variation source map/projector or non-Hilbert labelled current",
            "bound_or_zero_route": "identity source map, action-normal-form classification, or finite projector norm",
            "feeds": "eta_species; WEP; source-composition; R10 source legs",
            "status": "NONCLAIM_RESIDUAL_IF_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3345_2_E_decoupled_block",
            "symbol": "epsilon_decoupled_block",
            "definition": "ordinary-local test source contribution from truly decoupled conserved sectors",
            "bound_or_zero_route": "arena inventory exclusion or finite density/coupling bound",
            "feeds": "measured G; PPN; WEP; orbital/source normalization",
            "status": "NONCLAIM_RESIDUAL_IF_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3345_3_E_readout_reduced",
            "symbol": "epsilon_readout_backreaction",
            "definition": "varied reduced/readout functional or projector commutator leakage",
            "bound_or_zero_route": "closed parent Args(S_parent) excluding readout or explicit S_red residual bound",
            "feeds": "PPN; R10; clocks; source readout",
            "status": "NONCLAIM_RESIDUAL_IF_UNSIGNED",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3345_0_combined_signature_written",
            "claim": "ordinary coefficient-domain parent signature is written as one object",
            "passed": "true",
            "reason": "OD3345_0..7 consolidate quotient, coefficient algebra, matter action, source map, exchange graph, readout, and residual inventory.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3345_1_domain_zero_theorem",
            "claim": "vertical derivative zero theorem for A_ord is exact",
            "passed": "true",
            "reason": "L_v(q^*c_Q+c_fixed)=dc_Q[Dq(v)]+0=0 under the signature.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3345_2_source_weight_collapse",
            "claim": "ordinary connected source weights collapse to common calibration under the signature",
            "passed": "true",
            "reason": "same-action source plus connected exchange graph gives common block weight as conditional theorem.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3345_3_parent_signed",
            "claim": "MTS parent currently signs OD3345_0..7",
            "passed": "false",
            "reason": "All clauses are contract/conditional/private or open; no closed parent action-domain certificate exists yet.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3345_4_local_GR_claim",
            "claim": "local-GR source-coupling branch is claim-ready",
            "passed": "false",
            "reason": "The domain theorem would close many leaks but remains parent-unsigned and does not close all FRV3340 channels.",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3345_0",
            "question": "Did 3345 merely relist missing items?",
            "answer": "no",
            "reason": "It welds scattered coupling leaks into one typed parent signature and proves the derivative-zero theorem that would close them together.",
            "next_action": "Either parent-sign the action argument inventory, or choose the strongest finite residual interface row to source.",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3345_1",
            "question": "Did 3345 prove local GR?",
            "answer": "no",
            "reason": "The theorem is exact and high-leverage, but current MTS still lacks a closed parent action-domain certificate and several left-hand/source residual channels remain.",
            "next_action": "Build the parent action normal-form inventory with allowed/forbidden arguments line-by-line.",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3346-Y5-R2FR-parent-action-normal-form-inventory-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3346_parent_action_normal_form_inventory.py",
            "objective": "write the explicit Args(S_parent) inventory: allowed q-visible fields, fixed constants, EM/current owners, boundary terms, and forbidden hidden/source/readout arguments; score each against corpus sources",
            "why_next": "3345 shows the whole coefficient-domain route lives or dies on a closed Args(S_parent) certificate",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3346b-Y5-R2FR-source-shadow-projector-bound-or-zero-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3346b_source_shadow_projector_bound_or_zero.py",
            "objective": "if parent action normal form cannot close, convert epsilon_source_shadow into a finite source-backed projector/source-composition bound row",
            "why_next": "source shadow is the highest-pressure countermodel for eta_species and measured-G calibration after 3345",
            "valid_for_claim": "false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]], limit: int = 20) -> str:
    if not rows:
        return "_No rows._"
    fieldnames: list[str] = []
    for row in rows[:limit]:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows[:limit]:
        values = [compact(row.get(key, ""), 260).replace("|", "\\|") for key in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    if len(rows) > limit:
        lines.append(f"\n_Truncated in markdown: showing {limit} of {len(rows)} rows._")
    return "\n".join(lines)


def render_doc() -> str:
    return "\n\n".join(
        [
            "# 3345 — Ordinary Coefficient-Domain Parent Signature Under AX1090",
            f"Generated: `{RUN_UTC}`",
            "## Summary\n"
            "- This checkpoint attacks the parent lever behind `b_alpha`, `eta_species`, hidden source weights, shadow frames, and readout leakage.\n"
            "- The exact theorem is simple but powerful: if ordinary coefficients live in `A_ord=q^*A_Q + A_fixed`, then every vertical hidden derivative of those coefficients vanishes.\n"
            "- Combining that with a single Hilbert source map and connected ordinary exchange graph collapses ordinary source weights to one measured-G calibration factor.\n"
            "- Current status is still nonclaim: the theorem is exact, but the parent action argument inventory is not closed.",
            "## Ordinary Coefficient-Domain Signature\n" + markdown_table(signature_rows()),
            "## Domain Derivative Zero Theorem\n" + markdown_table(theorem_rows()),
            "## Closure Payoff Matrix\n" + markdown_table(payoff_rows()),
            "## Source Weight Collapse Theorem\n" + markdown_table(source_weight_rows()),
            "## Surviving Countermodel Matrix\n" + markdown_table(countermodel_rows()),
            "## Parent Signature Evidence Score\n" + markdown_table(evidence_score_rows()),
            "## Residual Interface If Unsigned\n" + markdown_table(residual_interface_rows()),
            "## Promotion Gates\n" + markdown_table(promotion_gate_rows()),
            "## Decision Ledger\n" + markdown_table(decision_rows()),
            "## Next Target\n" + markdown_table(next_target_rows()),
        ]
    ) + "\n"


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_rows()
    signature = signature_rows()
    theorem = theorem_rows()
    payoff = payoff_rows()
    residuals = residual_interface_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3345_0_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3345_1_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3345_2_outputs_parse",
            "check": "all 3345 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3345_3_signature_complete",
            "check": "signature rows cover quotient, geometry, A_ord, matter action, source map, exchange graph, readout, and residual inventory",
            "passed": {row["clause_id"] for row in signature}
            == {"OD3345_0_parent_quotient", "OD3345_1_observed_geometry", "OD3345_2_ordinary_coefficient_algebra", "OD3345_3_single_matter_functional", "OD3345_4_no_source_shadow", "OD3345_5_label_forgetting_exchange", "OD3345_6_readout_after_variation", "OD3345_7_boundary_and_decoupled_inventory"},
            "detail": "",
        },
        {
            "check_id": "VAL3345_4_exact_theorem_present",
            "check": "domain derivative zero theorem and combined theorem are present",
            "passed": any(row["theorem_id"] == "ODT3345_0_domain_derivative_zero" for row in theorem)
            and any(row["theorem_id"] == "ODT3345_4_combined_parent_domain_signature" for row in theorem),
            "detail": "",
        },
        {
            "check_id": "VAL3345_5_payoff_covers_key_leaks",
            "check": "payoff matrix covers b_alpha, eta_species, delta_J, shadow frames, readout, and local source vector",
            "passed": {"b_alpha / hidden Z_Q drift", "eta_species / source-only species weights", "source/test current normalization", "hidden conformal/disformal/source frames", "readout/projector backreaction", "FRV3340 source-coupling vector"}
            == {row["target"] for row in payoff},
            "detail": "",
        },
        {
            "check_id": "VAL3345_6_residual_interface",
            "check": "unsigned route produces finite residual interface rows",
            "passed": {row["symbol"] for row in residuals}
            == {"epsilon_coeff_domain", "epsilon_source_shadow", "epsilon_decoupled_block", "epsilon_readout_backreaction"},
            "detail": "",
        },
        {
            "check_id": "VAL3345_7_no_claim",
            "check": "parent signature and local-GR gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3345_3_parent_signed", "GATE3345_4_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3345_8_next_target",
            "check": "next target attacks parent action normal-form inventory or source-shadow bound",
            "passed": any("Args(S_parent)" in row["objective"] for row in next_target_rows())
            and any("epsilon_source_shadow" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3345_9_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": formalization_changed == 0,
            "detail": f"formalization_changed_count={formalization_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3345_10_overall",
            "check": "3345 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_rows())
    write_csv(OUTPUTS["signature"], signature_rows())
    write_csv(OUTPUTS["theorem"], theorem_rows())
    write_csv(OUTPUTS["payoff"], payoff_rows())
    write_csv(OUTPUTS["source_weight"], source_weight_rows())
    write_csv(OUTPUTS["countermodels"], countermodel_rows())
    write_csv(OUTPUTS["evidence_score"], evidence_score_rows())
    write_csv(OUTPUTS["residual_interface"], residual_interface_rows())
    write_csv(OUTPUTS["promotion_gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()

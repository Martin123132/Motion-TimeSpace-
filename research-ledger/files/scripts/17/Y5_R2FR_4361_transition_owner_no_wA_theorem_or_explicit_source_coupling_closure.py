from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4361"
CLAIM_ID = "L-202"
BRANCH = "MTS_R2FR_Y5_TRANSITION_OWNER_NO_WA_THEOREM_OR_EXPLICIT_SOURCE_COUPLING_CLOSURE_4361"
MARKER = "PPC4161_TRANSITION_OWNER_NO_WA_THEOREM_OR_EXPLICIT_SOURCE_COUPLING_CLOSURE_4361"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_OWNER_NO_WA_THEOREM_OR_EXPLICIT_SOURCE_COUPLING_CLOSURE_4361"
DECISION = "OWNER_NO_WA_CONDITIONAL_THEOREM_DERIVED_PARENT_SIGNATURES_UNSIGNED_EXPLICIT_CSRC_CLOSURE_SELECTED_NONCLAIM"
NEXT_TARGET = "4362-Y5-R2FR-transition-parent-owned-graph-signature-or-Csrc-closure-runner.md"

FORMAL_PATH = FORMAL / "377-PPC4161-transition-owner-no-wA-theorem-or-explicit-source-coupling-closure.md"
DOC_PATH = POST / "4361-Y5-R2FR-transition-owner-no-wA-theorem-or-explicit-source-coupling-closure.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4361_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4361_00_4360_next": (
        FORMAL / "376-PPC4161-transition-official-MICROSCOPE-readout-or-parent-nondegeneracy.md",
        "Can the source-only weight w_A be forbidden from the parent action/measure/current language",
        "4360 selected owner/no-wA theorem or explicit closure.",
    ),
    "SRC4361_01_1697_axiom": (
        POST / "1697-Y5-R2FR-owner-axiom-candidate-and-WEP-readout-source-pack.md",
        "AX1697_1_no_source_prefactor",
        "Minimal owner/no-source-prefactor axiom candidate.",
    ),
    "SRC4361_02_1605_naturality": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1605_ACTION_DENSITY_OWNER_THEOREM_ATTEMPT.csv",
        "ADO1605_1_naturality_lemma",
        "Exact connected action-line naturality lemma.",
    ),
    "SRC4361_03_1605_reduction": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1605_NO_WA_REDUCTION_STATUS.csv",
        "RED1605_6_verdict",
        "No-wA theorem-zero reduction remains open.",
    ),
    "SRC4361_04_1606_graph": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_GRAPH_THEOREM_ATTEMPT.csv",
        "POG1606_4_verdict",
        "Parent-owned graph proof not derived.",
    ),
    "SRC4361_05_1606_component_pack": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1606_DELTA_W_COMPONENT_BOUND_PACK.csv",
        "DWB1606_1_delta_w_e",
        "Delta_w component finite fallback pack exists but is not score-ready.",
    ),
    "SRC4361_06_4265_source_prefactor_split": (
        SOURCE_DIR / "P8_Y5_R2FR_4265_SOURCE_PREFACTOR_SPLIT_ROWS.csv",
        "SPL4265_0_species_weight",
        "Matter-domain descent explicitly retained source/species weights.",
    ),
    "SRC4361_07_4324_no_hidden_slot": (
        SOURCE_DIR / "P8_Y5_R2FR_4324_NO_HIDDEN_SLOT_AUDIT.csv",
        "NOT_GLOBAL_PARENT_SIGNED",
        "No-hidden-slot/source-label-forgetting is conditional, not globally signed.",
    ),
    "SRC4361_08_4324_Xi_formula": (
        FORMAL / "340-PPC4161-hidden-source-prefactor-and-marker-tail-zero-or-bound.md",
        "Xi_src_hidden :=",
        "Master hidden source-coupling tail formula.",
    ),
    "SRC4361_09_4332_Xi_zero": (
        FORMAL / "348-PPC4161-Xi-src-hidden-zero-or-source-label-tail-bound.md",
        "D_Hperp ln w_A = 0",
        "Branch-local source-label-forgetting zero condition.",
    ),
    "SRC4361_10_4332_Xi_open": (
        FORMAL / "348-PPC4161-Xi-src-hidden-zero-or-source-label-tail-bound.md",
        "Xi_open <=",
        "Open-tail source-label bound if owner theorem is not signed.",
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "TH4361_0_scalar_naturality",
            "claim_piece": "connected scalar action weights collapse",
            "formal_statement": "For a parent-owned connected ordinary-matter category C_ord with one action-density line L_action, any natural scalar action-weight endomorphism W_A=w_A id obeys w_B F(f)=F(f)w_A on every nonzero parent-owned edge f:A->B; hence w_A=w_B along each edge and w_A=w_* on the connected component.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM_DERIVED",
            "effect_if_parent_signed": "relative source weights vanish on the connected ordinary-matter component",
            "current_blocker": "parent-owned connected graph certificate remains unsigned",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4361_1_common_weight_calibration",
            "claim_piece": "common w_* is calibration only",
            "formal_statement": "If w_A=w_* for all ordinary matter and D_Hperp w_*=0 across material, source, frame, range and clock/readout labels, then w_* multiplies the common Hilbert source and is absorbed into calibrated G_N/GM rather than a WEP/source-label residual.",
            "proof_status": "EXACT_CONDITIONAL_CALIBRATION_LEMMA",
            "effect_if_parent_signed": "Delta_w_TiPt=0 for source-label/species contrast",
            "current_blocker": "common-mode derivative silence depends on the same owner/no-hidden-slot branch",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4361_2_no_reentry_extension",
            "claim_piece": "readout/EFT/source-label no reentry",
            "formal_statement": "The no-wA theorem only survives to observables if source weights, normalization, hidden operators, EM current weights and environment selectors cannot re-enter after variation through readout, effective action, theta markers or projector/worldtube maps.",
            "proof_status": "REQUIRED_EXTENSION_FORMALIZED",
            "effect_if_parent_signed": "Xi_src_hidden=0 in the source-label-forgetting Hilbert-owner branch",
            "current_blocker": "4332 gives branch-local zero but not global parent signature",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4361_3_full_owner_no_wA",
            "claim_piece": "owner/no-wA theorem",
            "formal_statement": "Single action-density owner + parent-owned connected ordinary-matter graph + species-blind measure/Jacobian + typed no-source-prefactor domain + variation-before-readout/no-reentry imply Delta_w_A=0 and Xi_src_hidden=0 for the standard Hilbert-owner source branch.",
            "proof_status": "CONDITIONAL_THEOREM_ASSEMBLED_NOT_PARENT_SIGNED",
            "effect_if_parent_signed": "finite MICROSCOPE tau_min route becomes optional for this source-label coupling leg",
            "current_blocker": "not all premises are parent-signed in the current corpus",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4361_4_failure_branch",
            "claim_piece": "explicit closure if theorem not signed",
            "formal_statement": "If any owner/no-wA premise fails, retain a named source-coupling closure C_src_open built from Delta_w component vector plus Xi_open, with no cancellation and arena-specific projections.",
            "proof_status": "FALLBACK_CLOSURE_CONTRACT_DERIVED",
            "effect_if_parent_signed": "not applicable; this is the honest nonzero branch",
            "current_blocker": "numeric/source-backed projection rows remain to be filled",
            "valid_for_claim": "False",
        },
    ]


def premise_rows() -> List[Dict[str, str]]:
    return [
        {
            "premise_id": "P4361_0_single_action_line",
            "premise": "one parent action-density line for ordinary matter",
            "status": "TARGET_SHARPENED_UNSIGNED",
            "source_anchor": "ADO1605_0_target; SAL1478_4",
            "effect_if_closed": "direct-sum action-weight normalization becomes illegal",
            "failure_mode": "independent sector weights can be inserted before variation",
            "parent_signed": "False",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "P4361_1_parent_owned_connected_graph",
            "premise": "source-relevant ordinary matter graph connected by nonzero parent-owned morphisms",
            "status": "EXACT_GRAPH_LEMMA_BUT_GRAPH_UNSIGNED",
            "source_anchor": "ADO1605_1; POG1606_1; POG1606_4",
            "effect_if_closed": "natural weights collapse to one w_*",
            "failure_mode": "direct-sum component-weight countermodel survives",
            "parent_signed": "False",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "P4361_2_measure_owner",
            "premise": "species-blind measure/Jacobian/hbar and no field-normalization source slot",
            "status": "REQUIRED_EXTENSION_UNSIGNED",
            "source_anchor": "ADO1605_3",
            "effect_if_closed": "w_A cannot hide in Jacobian, hbar_A or field normalization",
            "failure_mode": "species Jacobian/effective-hbar countermodel survives",
            "parent_signed": "False",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "P4361_3_typed_no_source_prefactor",
            "premise": "no Hom/source-label/hidden-marker target that creates source-only prefactors",
            "status": "CONDITIONAL_GRAMMAR_UNSIGNED",
            "source_anchor": "AX1697_1; NST1479; OG1451",
            "effect_if_closed": "w_A is not a well-typed parent object except common calibration",
            "failure_mode": "hidden scalar invariant or marker source-label feeds a source coefficient",
            "parent_signed": "False",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "P4361_4_variation_before_readout",
            "premise": "source labels cannot be introduced after variation through readout/projector/worldtube maps",
            "status": "BRANCH_LOCAL_CONDITIONAL",
            "source_anchor": "4332 source-label-forgetting branch",
            "effect_if_closed": "Xi_src_hidden=0 with the other owner clauses",
            "failure_mode": "post-readout label/reentry tail survives",
            "parent_signed": "False",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "P4361_5_common_mode_silence",
            "premise": "remaining common w_* has no source/material/time/frame/range derivative",
            "status": "CONDITIONAL_ON_OWNER_BRANCH",
            "source_anchor": "ADO1605_2; F4332_1",
            "effect_if_closed": "common mode calibrates G_N/GM and carries no WEP contrast",
            "failure_mode": "time/frame/range/source dependent common mode becomes a local-test tail",
            "parent_signed": "False",
            "valid_for_claim": "False",
        },
    ]


def countermodel_rows() -> List[Dict[str, str]]:
    return [
        {
            "countermodel_id": "CM4361_0_direct_sum",
            "loophole": "ordinary matter parent category splits into disconnected source-normalization components",
            "surviving_weight": "independent constants w_i on each component",
            "why_it_matters": "natural scalar weights do not have to agree across disconnected components",
            "closure_required": "parent-owned connected graph certificate",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM4361_1_species_jacobian",
            "loophole": "species-dependent measure/Jacobian or hbar_A",
            "surviving_weight": "effective w_A moved from action density into measure/quantum normalization",
            "why_it_matters": "same observable WEP/source contrast can reappear under a different name",
            "closure_required": "species-blind parent measure and field-normalization theorem",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM4361_2_hidden_invariant",
            "loophole": "hidden scalar invariant feeds a coefficient c_A(I_hid)",
            "surviving_weight": "source/material dependent prefactor after q-projection",
            "why_it_matters": "typed domain must forbid the target, not merely omit it in notation",
            "closure_required": "no Hom from source labels/hidden markers to source prefactor slots",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM4361_3_readout_reentry",
            "loophole": "post-variation readout/projector/worldtube injects source labels",
            "surviving_weight": "Xi_src_hidden or Delta_w readout tail",
            "why_it_matters": "pre-variation theorem can be spoiled at observable transfer",
            "closure_required": "variation-before-readout and no-hidden-readout-reentry theorem",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM4361_4_nonstandard_common_mode",
            "loophole": "common w_* is time/frame/range/source dependent",
            "surviving_weight": "not WEP species contrast but still a PPN/clock/orbital/Gdot source-coupling tail",
            "why_it_matters": "common calibration is harmless only if derivative-silent in the tested branch",
            "closure_required": "common-mode derivative silence or explicit local-test projection bound",
            "valid_for_claim": "False",
        },
    ]


def closure_rows() -> List[Dict[str, str]]:
    return [
        {
            "closure_id": "CSRC4361_0_delta_w_vector",
            "object": "Delta_w_component_vector",
            "definition": "Delta_w_AB = sum_i DeltaQ_i^AB * delta_w_i + R_material_basis + R_parent_edge",
            "units": "dimensionless",
            "current_status": "EXPLICIT_CLOSURE_IF_OWNER_THEOREM_FAILS",
            "required_inputs": "component values; parent material tensor; source/readout basis; sign convention; covariance/no-cancellation rule",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "closure_id": "CSRC4361_1_Xi_open",
            "object": "Xi_open",
            "definition": "Xi_open <= C_w||D_Hperp ln w_A|| + C_norm||D_Hperp ln N_src|| + C_mark||D_Hperp theta_src|| + C_op||D_Hperp O_hidden|| + C_EM||delta_w_EM|| + C_inner||Q_m^H|| + C_env||D_Hperp sigma_env||",
            "units": "dimensionless_or_arena_projected",
            "current_status": "BOUND_FORMULA_DERIVED_VALUES_MISSING",
            "required_inputs": "C_i projection constants and each derivative/source-tail norm",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "closure_id": "CSRC4361_2_WEP_product",
            "object": "MICROSCOPE WEP source-weight product",
            "definition": "abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15",
            "units": "dimensionless",
            "current_status": "SOURCE_BACKED_PRODUCT_ONLY",
            "required_inputs": "tau_min>0 or owner/no-wA theorem-zero before Delta_w bound inversion",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "closure_id": "CSRC4361_3_local_source_budget",
            "object": "epsilon_Gsrc_open",
            "definition": "epsilon_Gsrc_open <= P_WEP|Delta_w_TiPt| + P_Xi Xi_open + P_coeff epsilon_coeff_open + P_proj epsilon_projection_open + P_tail tail_guard_sum",
            "units": "arena_projected",
            "current_status": "EXPLICIT_LOCAL_SOURCE_CLOSURE_SCHEMA",
            "required_inputs": "arena projection constants for WEP, PPN, R10, clock, orbital and Newton/source normalization",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "closure_id": "CSRC4361_4_decision",
            "object": "owner theorem failure branch",
            "definition": "if any premise P4361_i remains unsigned, do not call Delta_w zero; carry CSRC4361_0-3 into finite scoring",
            "units": "policy",
            "current_status": "CLOSURE_SELECTED_FOR_UNPROVED_BRANCH",
            "required_inputs": "4362 runner or parent-owned graph signature",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def arena_rows() -> List[Dict[str, str]]:
    arenas = [
        ("WEP_species", "Delta_w_TiPt or tau_min", "owner/no-wA theorem-zero or CSRC4361_2 product plus tau_min"),
        ("Newton_source", "single calibrated source charge", "common w_* derivative silence plus no independent source-normalization"),
        ("local_GR", "source side of Hilbert/EH limit", "Delta_w=0/Xi=0 or explicit epsilon_Gsrc_open bound"),
        ("PPN_gamma_beta", "metric response to source coupling", "arena projection constants P_coeff/P_proj and no hidden frame/source tails"),
        ("clock_Gdot", "time-dependent common/source mode", "D_tau w_*=0 or finite clock projection"),
        ("orbital_GM", "measured GM and source mass readout", "Hamiltonian mass readout plus no source-label reentry"),
        ("R10_range", "finite range/source coupling", "source coupling vector projected into alpha(lambda) branch"),
    ]
    return [
        {
            "arena_id": f"AR4361_{index}",
            "arena": arena,
            "live_object": live_object,
            "4361_requirement": requirement,
            "zero_route": "prove all owner/no-wA premises P4361_0-5",
            "finite_route": "use CSRC4361 explicit source-coupling closure rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for index, (arena, live_object, requirement) in enumerate(arenas)
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4361_0_theorem_proof",
            "input": "premises P4361_0 through P4361_5",
            "action": "try owner/no-wA theorem",
            "result": "CONDITIONAL_THEOREM_DERIVED_BUT_NOT_PARENT_SIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4361_1_countermodels",
            "input": "direct-sum, Jacobian, hidden invariant, readout reentry, nonstandard common mode",
            "action": "test whether theorem can be promoted anyway",
            "result": "REJECT_PROMOTION_COUNTERMODELS_ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4361_2_zero_route",
            "input": "signed owner theorem",
            "action": "would set Delta_w_A=0 and Xi_src_hidden=0",
            "result": "WAITING_FOR_PARENT_SIGNATURES",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4361_3_closure_route",
            "input": "unsigned owner theorem",
            "action": "activate explicit source-coupling closure schema",
            "result": "CSRC4361_SELECTED_NONCLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "CG4361_0_conditional_theorem",
            "claim_component": "owner/no-wA conditional theorem",
            "gate_pass": "True",
            "claim_allowed": "False",
            "reason": "conditional theorem is derived, but parent signatures are not all present",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4361_1_parent_signatures",
            "claim_component": "public/parent-signed no-wA theorem",
            "gate_pass": "False",
            "claim_allowed": "False",
            "reason": "single action line, parent graph, measure, typed domain and no reentry remain unsigned",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4361_2_delta_w_zero",
            "claim_component": "Delta_w_TiPt=0",
            "gate_pass": "False",
            "claim_allowed": "False",
            "reason": "zero route is exact but conditional only",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4361_3_closure_schema",
            "claim_component": "explicit source-coupling closure",
            "gate_pass": "True",
            "claim_allowed": "False",
            "reason": "schema is now explicit but numeric/source-backed rows are missing",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4361_4_local_claims",
            "claim_component": "local GR/Newton/WEP/PPN/R10/clock/orbital",
            "gate_pass": "False",
            "claim_allowed": "False",
            "reason": "source-coupling zero or finite bound has not been completed",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4361_0",
            "decision": DECISION,
            "reason": (
                "4361 proves the mathematical owner/no-wA route as a conditional theorem: natural scalar action weights "
                "collapse to one common calibration mode on a parent-owned connected ordinary-matter action graph, and no-hidden/readout reentry "
                "then removes Xi_src_hidden. The proof cannot be promoted because the current corpus does not parent-sign the action line, graph, "
                "measure/Jacobian, typed no-source-slot, no-reentry and common-mode silence clauses. Therefore the honest nonzero branch is now an "
                "explicit C_src closure schema rather than a vague missing coupling."
            ),
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {"status_id": "STAT4361_0", "item": "owner/no-wA theorem", "status": "CONDITIONAL_THEOREM_DERIVED", "note": "mathematical implication is exact under P4361_0-5."},
        {"status_id": "STAT4361_1", "item": "parent signatures", "status": "UNSIGNED", "note": "countermodels remain active outside the signed branch."},
        {"status_id": "STAT4361_2", "item": "Delta_w zero", "status": "NOT_CLAIMED", "note": "would follow if owner theorem is parent-signed."},
        {"status_id": "STAT4361_3", "item": "C_src closure", "status": "EXPLICIT_SCHEMA_SELECTED", "note": "finite branch no longer vague; values/projections still missing."},
        {"status_id": "STAT4361_4", "item": "next target", "status": "PARENT_GRAPH_OR_CSRC_RUNNER", "note": NEXT_TARGET},
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4361_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can we parent-sign the connected ordinary-matter action graph, or must we run the explicit C_src closure branch?",
            "preferred_route": "derive/source parent-owned graph edges and measure/no-reentry signatures so TH4361_3 can be promoted",
            "fallback_route": "instantiate CSRC4361 rows as nonclaim finite source-coupling runner for WEP, PPN, R10, clock, orbital and Newton/source normalization",
            "valid_for_claim": "False",
        }
    ]


def append_claim_register() -> None:
    path = FORMAL / "02-claims-register.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
        rows = list(reader)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": (
                "4361 derives the owner/no-wA theorem as an exact conditional theorem. If ordinary matter is on one parent action-density line, "
                "if the source-relevant matter graph is connected by parent-owned nonzero morphisms, if the measure/Jacobian and typed domain forbid "
                "species/source prefactors, and if readout/EFT cannot reintroduce source labels after variation, then all natural source weights collapse "
                "to one derivative-silent common calibration mode and Delta_w_A=Xi_src_hidden=0. The theorem is not promoted because those parent signatures "
                "remain unsigned; the fallback is now the explicit C_src source-coupling closure schema."
            ),
            "current_evidence": (
                "4361 source register, theorem rows, premise audit, countermodel rows, C_src closure schema, arena rows, runner, claim gates, decision, status, next target and validation CSV."
            ),
            "status": "conditional_owner_no_wA_theorem_derived_parent_signatures_unsigned_explicit_Csrc_closure_nonclaim",
            "next_test": "Parent-sign the connected action graph/measure/no-reentry signatures or instantiate the explicit C_src closure runner.",
            "key_risk": "Treating a conditional theorem as a parent-signed proof; hiding source weights in measure/readout; using common calibration to absorb relative WEP/source weights.",
        }
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_formal_doc(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 377 PPC4161 transition owner/no-wA theorem or explicit source-coupling closure

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4361 does not prove public local GR, Newton, WEP, R10, PPN, clock, orbital, EM, or source-coupling safety.

## Result

4361 takes the clean coupling route as far as the current corpus honestly allows.

The theorem route is now precise:

```text
single parent action-density line
+ parent-owned connected ordinary-matter graph
+ species-blind measure/Jacobian/field normalization
+ typed no-source-prefactor domain
+ variation-before-readout/no hidden reentry
+ derivative-silent common mode
=> w_A = w_*
=> Delta_w_A = 0
=> Xi_src_hidden = 0.
```

The proof step that matters is the scalar naturality lemma:

```text
w_B F(f) = F(f) w_A
```

for every nonzero parent-owned edge `f:A->B`. On a connected parent-owned graph this forces all `w_A` to equal one common `w_*`. If `w_*` is derivative-silent, it is calibration, not a WEP/source-label residual.

But the theorem is not parent-signed. The current corpus still leaves active countermodels: direct-sum source components, species Jacobians, hidden scalar coefficient slots, readout reentry, and nonstandard common-mode drift.

So the nonzero branch is no longer a foggy coupling complaint. It is the explicit closure:

```text
C_src_open := {{Delta_w_component_vector, Xi_open, tau_WEP product, epsilon_Gsrc_open}}.
```

If 4362 cannot parent-sign the graph/owner clauses, the work must run that closure honestly rather than pretending the source coupling vanished.

## Source Register

{md_table(tables["source"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role", "valid_for_claim"])}

## Theorem Rows

{md_table(tables["theorem"], ["theorem_id", "claim_piece", "formal_statement", "proof_status", "effect_if_parent_signed", "current_blocker", "valid_for_claim"])}

## Premise Audit

{md_table(tables["premise"], ["premise_id", "premise", "status", "source_anchor", "effect_if_closed", "failure_mode", "parent_signed", "valid_for_claim"])}

## Countermodel Rows

{md_table(tables["countermodel"], ["countermodel_id", "loophole", "surviving_weight", "why_it_matters", "closure_required", "valid_for_claim"])}

## Explicit Csrc Closure Rows

{md_table(tables["closure"], ["closure_id", "object", "definition", "units", "current_status", "required_inputs", "claim_allowed", "valid_for_claim"])}

## Arena Rows

{md_table(tables["arena"], ["arena_id", "arena", "live_object", "4361_requirement", "zero_route", "finite_route", "claim_allowed", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "input", "action", "result", "claim_allowed", "valid_for_claim"])}

## Claim Gates

{md_table(tables["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason", "valid_for_claim"])}

## Decision

{md_table(tables["decision"], ["decision_id", "decision", "reason", "next_action", "claim_allowed", "valid_for_claim"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route", "valid_for_claim"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(formal.replace("# 377 PPC4161", "# 4361 - Y5/R2FR"), encoding="utf-8")


def append_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 4361 owner/no-wA theorem or explicit source-coupling closure

Marker: `{MARKER}`

4361 proves the source-coupling zero route as an exact conditional theorem. On one parent action-density line, a parent-owned connected ordinary-matter graph forces natural scalar source weights to one common `w_*`:

```text
w_B F(f)=F(f)w_A  =>  w_A=w_B
```

If the measure/domain/readout no-reentry clauses also hold and `w_*` is derivative-silent, then `Delta_w_A=0` and `Xi_src_hidden=0`. The theorem is not promoted because those parent signatures are still unsigned. The failure branch is now explicit: `C_src_open={{Delta_w_component_vector, Xi_open, tau_WEP product, epsilon_Gsrc_open}}`.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""
## PPC4161 packet update 4361 owner/no-wA conditional theorem

Marker: `{PACKET_MARKER}`

Packet update: the coupling gremlin is no longer shapeless. Either the parent-owned connected action graph and no-reentry clauses are signed, giving `Delta_w_A=Xi_src_hidden=0`, or the local packet must carry the explicit `C_src_open` closure vector into WEP/PPN/R10/clock/orbital/Newton projections.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    csv_paths = [
        SOURCE_DIR / f"P8_Y5_R2FR_4361_{name}.csv"
        for name in [
            "SOURCE_REGISTER",
            "THEOREM_ROWS",
            "PREMISE_AUDIT",
            "COUNTERMODEL_ROWS",
            "CSRC_CLOSURE_ROWS",
            "ARENA_ROWS",
            "RUNNER",
            "CLAIM_GATES",
            "DECISION",
            "STATUS",
            "NEXT_TARGET",
        ]
    ]

    def all_csv_parse(paths: Iterable[Path]) -> bool:
        for path in paths:
            try:
                with path.open(newline="", encoding="utf-8") as handle:
                    list(csv.DictReader(handle))
            except Exception:
                return False
        return True

    checks = [
        ("formal_doc_written", FORMAL_PATH.exists(), str(FORMAL_PATH)),
        ("post_doc_written", DOC_PATH.exists(), str(DOC_PATH)),
        ("marker_in_formal", MARKER in read_text(FORMAL_PATH), MARKER),
        ("decision_in_formal", DECISION in read_text(FORMAL_PATH), DECISION),
        ("all_local_sources_exist", all(row["path_exists"] == "True" for row in tables["source"]), ""),
        ("all_local_needles_found", all(row["needle_found"] == "True" for row in tables["source"]), ""),
        ("naturality_theorem_derived", any(row["theorem_id"] == "TH4361_0_scalar_naturality" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM_DERIVED" for row in tables["theorem"]), ""),
        ("full_owner_theorem_not_parent_signed", any(row["theorem_id"] == "TH4361_3_full_owner_no_wA" and row["proof_status"] == "CONDITIONAL_THEOREM_ASSEMBLED_NOT_PARENT_SIGNED" for row in tables["theorem"]), ""),
        ("premises_unsigned", all(row["parent_signed"] == "False" for row in tables["premise"]), ""),
        ("countermodels_retained", len(tables["countermodel"]) >= 5, str(len(tables["countermodel"]))),
        ("closure_schema_selected", any(row["closure_id"] == "CSRC4361_4_decision" for row in tables["closure"]), ""),
        ("wep_product_retained", any(row["object"] == "MICROSCOPE WEP source-weight product" for row in tables["closure"]), ""),
        ("arena_rows_cover_local", any(row["arena"] == "local_GR" for row in tables["arena"]), ""),
        ("claim_gates_block_local", any(row["gate_id"] == "CG4361_4_local_claims" and row["claim_allowed"] == "False" for row in tables["gates"]), ""),
        ("next_target_present", NEXT_TARGET in read_text(FORMAL_PATH), NEXT_TARGET),
        ("claim_register_updated", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), CLAIM_ID),
        ("spine_marker_present", MARKER in read_text(FORMAL / "07-unification-spine.md"), MARKER),
        ("packet_marker_present", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), PACKET_MARKER),
        ("csv_parse", all_csv_parse(csv_paths), str(len(csv_paths))),
        ("no_valid_claim_rows", all(row.get("valid_for_claim", "False") == "False" for table in tables.values() for row in table), ""),
        ("generated_under_project", str(FORMAL_PATH).startswith(str(ROOT)) and str(DOC_PATH).startswith(str(ROOT)), str(ROOT)),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "passed": str(bool(passed)),
            "detail": detail,
            "valid_for_claim": "False",
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    tables = {
        "source": source_rows(),
        "theorem": theorem_rows(),
        "premise": premise_rows(),
        "countermodel": countermodel_rows(),
        "closure": closure_rows(),
        "arena": arena_rows(),
        "runner": runner_rows(),
        "gates": claim_gate_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_target_rows(),
    }

    outputs = {
        "SOURCE_REGISTER": tables["source"],
        "THEOREM_ROWS": tables["theorem"],
        "PREMISE_AUDIT": tables["premise"],
        "COUNTERMODEL_ROWS": tables["countermodel"],
        "CSRC_CLOSURE_ROWS": tables["closure"],
        "ARENA_ROWS": tables["arena"],
        "RUNNER": tables["runner"],
        "CLAIM_GATES": tables["gates"],
        "DECISION": tables["decision"],
        "STATUS": tables["status"],
        "NEXT_TARGET": tables["next"],
    }
    for name, rows in outputs.items():
        write_csv(SOURCE_DIR / f"P8_Y5_R2FR_4361_{name}.csv", rows)

    write_formal_doc(tables)
    append_claim_register()
    append_spine_and_packet()

    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"4361: wrote {len(outputs)} csv artifacts plus validation")
    print(f"4361: validation rows={len(validation_rows)} failed={len(failed)}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

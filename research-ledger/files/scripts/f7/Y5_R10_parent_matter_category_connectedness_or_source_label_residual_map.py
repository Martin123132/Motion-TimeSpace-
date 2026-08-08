from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1231"
TITLE = "1231-Y5-R10-parent-matter-category-connectedness-or-source-label-residual-map"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
CATEGORY_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_MATTER_CATEGORY_CONNECTEDNESS_ATTEMPT.csv"
SOURCE_FORGETTING_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_LABEL_FORGETTING_PROOF_STACK.csv"
RESIDUAL_BASIS_PATH = OUT_DIR / f"{PACK_ID}_DISCONNECTED_COMPONENT_RESIDUAL_BASIS.csv"
DELTA_MAP_PATH = OUT_DIR / f"{PACK_ID}_DELTA_W_COMPONENT_MAP.csv"
ARENA_LAW_PATH = OUT_DIR / f"{PACK_ID}_ARENA_RESIDUAL_LAWS.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1231_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def is_false(row: dict[str, object], key: str) -> bool:
    return not parse_bool(row.get(key, False))


def source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > RUN_STARTED_UTC
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1231_0_1230_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1230_NEXT_TARGET.csv",
            "needle": "NEXT1230_0_1231",
            "purpose": "1230 handoff to parent matter-category connectedness or residual map",
        },
        {
            "source_id": "SRC1231_1_1230_conditional",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv",
            "needle": "UAS1230_1_connected_naturality_lemma",
            "purpose": "connected naturality theorem premise",
        },
        {
            "source_id": "SRC1231_2_1230_failure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1230_OWNER_FAILURE_MODE_LEDGER.csv",
            "needle": "FAIL1230_0_disconnected_category",
            "purpose": "disconnected category failure mode",
        },
        {
            "source_id": "SRC1231_3_953_category",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv",
            "needle": "PMC953_1_label_forgetting_quotient",
            "purpose": "source-label forgetting contract",
        },
        {
            "source_id": "SRC1231_4_1045_functor",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
            "needle": "MFS1045_6_verdict",
            "purpose": "parent matter functor signature audit",
        },
        {
            "source_id": "SRC1231_5_1044_pullback",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv",
            "needle": "MPD1044_6_source_current_universality",
            "purpose": "source-current universality conditional",
        },
        {
            "source_id": "SRC1231_6_1066_naturality",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
            "needle": "SSE1066_3_naturality_route",
            "purpose": "naturality route and disconnected component caveat",
        },
        {
            "source_id": "SRC1231_7_1224_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1224_OWNER_PROOF_CLAUSES.csv",
            "needle": "OWN1224_3_connected_matter_naturality",
            "purpose": "source-weight owner connectedness clause",
        },
        {
            "source_id": "SRC1231_8_1229_counter",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1229_SOURCE_COUPLING_COUNTEREXAMPLE_LEDGER.csv",
            "needle": "CEX1229_4_disconnected_species",
            "purpose": "active disconnected-species counterexample",
        },
        {
            "source_id": "SRC1231_9_1230_delta",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1230_FINITE_DELTA_W_PRIOR_CONTRACT.csv",
            "needle": "FDW1230_0_Delta_w_TiPt",
            "purpose": "finite Delta_w prior contract",
        },
    ]

    source_register = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    category_attempt = [
        {
            "attempt_id": "CMC1231_0_target",
            "claim_piece": "parent ordinary matter category connectedness",
            "formal_statement": "Build C_ord whose objects are ordinary matter sectors and whose morphisms are parent-owned interactions, shared currents, bound-state maps, and representation-changing processes before source extraction.",
            "result": "TARGET_SHARPENED",
            "gap": "the current corpus names C_ord but does not parent-construct its objects and morphisms",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv", "UAS1230_1_connected_naturality_lemma"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "CMC1231_1_interaction_graph_lemma",
            "claim_piece": "connected interaction graph collapses source weights",
            "formal_statement": "Let G_ord have vertices ordinary matter action components and edges parent-owned nonzero interaction/current morphisms. If G_ord is connected and w is a natural automorphism of the action-density/source functor, then all w_A are one common w_*.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "gap": "G_ord connectedness and morphism ownership are not parent-signed",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_3_naturality_route"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "CMC1231_2_source_forgetting_lemma",
            "claim_piece": "label-forgetting source quotient",
            "formal_statement": "If q_src sends labelled families {(T_A,A)} to T_total=sum_A T_A before the gravitational source map is formed, then a source map cannot depend on A except through T_A itself.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "gap": "q_src is a contract clause, not a derived parent quotient",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv", "PMC953_1_label_forgetting_quotient"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "CMC1231_3_ordinary_matter_template",
            "claim_piece": "ordinary test matter likely lives in a connected effective interaction web",
            "formal_statement": "Ti/Pt test bodies are made from electrons, light quarks, gluons, photons, and nuclear binding sectors that are not independent isolated source categories in ordinary low-energy matter.",
            "result": "PLAUSIBLE_TEMPLATE_NOT_PARENT_PROOF",
            "gap": "this is physical guidance only; MTS still needs a parent category/interactions certificate",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv", "MFS1045_2_matter_bundle_functor"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "CMC1231_4_current_corpus_signature",
            "claim_piece": "current MTS parent-signs connectedness/source-label forgetting",
            "formal_statement": "The corpus already proves C_ord connectedness, q_src label forgetting, and no disconnected source-only components.",
            "result": "NOT_PARENT_SIGNED",
            "gap": "953, 1045, 1066, 1224, 1229, and 1230 all keep the needed clauses conditional",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1224_OWNER_PROOF_CLAUSES.csv", "OWN1224_6_verdict"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "CMC1231_5_verdict",
            "claim_piece": "source-label connectedness closes Delta_w",
            "formal_statement": "CMC1231_1 plus CMC1231_2 plus action-scale/measure/readout descent would imply no relative source multipliers for ordinary matter.",
            "result": "CONDITIONAL_ONLY_RESIDUAL_MAP_REQUIRED",
            "gap": "disconnected component counterexample remains active until parent category is signed",
            "source": "CMC1231_0 through CMC1231_4",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    source_forgetting = [
        {
            "stack_id": "SFL1231_0_label_quotient",
            "required_clause": "source quotient forgets species labels before gravity selects a current",
            "mathematical_form": "q_src({(T_A,A)})=sum_A T_A",
            "status": "CONTRACT_NOT_PARENT_SIGNED",
            "if_open": "kappa_A T_A remains syntactically legal",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "stack_id": "SFL1231_1_additive_natural_source",
            "required_clause": "source map is local, additive, covariant, and natural",
            "mathematical_form": "F_src(T+U)=F_src(T)+F_src(U), F_src(phi_*T)=phi_*F_src(T)",
            "status": "CONDITIONAL_MATH_CLEAR",
            "if_open": "non-Hilbert or labelled source currents can be smuggled in",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "stack_id": "SFL1231_2_connected_components",
            "required_clause": "ordinary matter category has one connected component for source normalization",
            "mathematical_form": "pi_0(C_ord)=* for source-density functor",
            "status": "NOT_DERIVED",
            "if_open": "each component c can carry an independent delta w_c",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "stack_id": "SFL1231_3_measure_readout_no_reentry",
            "required_clause": "measure, boundary, and readout maps preserve label forgetting",
            "mathematical_form": "K_readout o q_src has no A argument except through T_A",
            "status": "UNSIGNED",
            "if_open": "tau_WEP/readout kernels can recreate effective source labels",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "stack_id": "SFL1231_4_verdict",
            "required_clause": "source-label forgetting theorem",
            "mathematical_form": "SFL1231_0 through SFL1231_3 all parent-signed",
            "status": "NOT_CLOSED",
            "if_open": "disconnected-component residual basis must stay active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    residual_basis = [
        {
            "component_id": "DCW1231_0_common_mode",
            "component": "common ordinary matter source scale",
            "symbol": "delta w_common",
            "definition": "one universal factor multiplying all ordinary matter source currents",
            "current_status": "G_N_ABSORBABLE_ONLY_IF_COMMON",
            "blocks": "none after common calibration",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "DCW1231_1_leptonic_electron",
            "component": "electron/leptonic rest and kinetic contribution",
            "symbol": "delta w_e",
            "definition": "relative source weight for electron-sector energy fraction after common mode removed",
            "current_status": "RESIDUAL_SLOT_NONCLAIM",
            "blocks": "Delta_w_TiPt; clocks; material response",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "DCW1231_2_light_quark_mass",
            "component": "light-quark mass contribution",
            "symbol": "delta w_q",
            "definition": "relative source weight for u/d quark mass contribution in ordinary nuclei",
            "current_status": "RESIDUAL_SLOT_NONCLAIM",
            "blocks": "Delta_w_TiPt; nuclear material response",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "DCW1231_3_QCD_gluon_binding",
            "component": "QCD/gluon/nuclear bulk binding contribution",
            "symbol": "delta w_g",
            "definition": "relative source weight for QCD and strong binding energy contribution",
            "current_status": "RESIDUAL_SLOT_NONCLAIM",
            "blocks": "Delta_w_TiPt; source profile; PPN source residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "DCW1231_4_EM_Coulomb_binding",
            "component": "EM/Coulomb binding contribution",
            "symbol": "delta w_EM",
            "definition": "relative source weight for electromagnetic self/binding energy contribution",
            "current_status": "RESIDUAL_SLOT_NONCLAIM",
            "blocks": "WEP; alpha/EM cross-sector closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "DCW1231_5_nuclear_surface_asymmetry",
            "component": "nuclear surface/asymmetry/binding residual",
            "symbol": "delta w_nuc",
            "definition": "relative source weight for composition-dependent nuclear binding pieces not captured by bulk QCD/EM rows",
            "current_status": "RESIDUAL_SLOT_NONCLAIM",
            "blocks": "Ti/Pt differential material response",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "DCW1231_6_measure_readout",
            "component": "measure/readout reentry component",
            "symbol": "delta w_K",
            "definition": "effective source-label residual generated by measure, boundary, projection, or readout maps",
            "current_status": "RESIDUAL_SLOT_NONCLAIM",
            "blocks": "tau_WEP; PPN/clocks/orbital projections",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    delta_map = [
        {
            "map_id": "DWM1231_0_body_effective_weight",
            "quantity": "delta w_B",
            "formula": "delta w_B = sum_c F_{B,c} delta w_c + delta w_{K,B}",
            "meaning": "effective source-weight residual for body/material B after removing the common G_N mode",
            "required_inputs": "component energy fractions F_{B,c}; component residual priors; readout residual",
            "status": "SYMBOLIC_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "DWM1231_1_TiPt_difference",
            "quantity": "Delta_w_TiPt",
            "formula": "Delta_w_TiPt = sum_c (F_{Ti,c}-F_{Pt,c}) delta w_c + (delta w_{K,Ti}-delta w_{K,Pt})",
            "meaning": "finite residual entering MICROSCOPE Ti/Pt source-weight product",
            "required_inputs": "Ti/Pt component fractions in same material convention as tau_WEP",
            "status": "MISSING_COMPONENT_FRACTIONS_AND_PRIORS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "DWM1231_2_source_stress_residual",
            "quantity": "T_res^{mu nu}",
            "formula": "T_res^{mu nu}=sum_c delta w_c T_c^{mu nu}+T_K^{mu nu}",
            "meaning": "source-side residual stress if disconnected components survive",
            "required_inputs": "component stress decomposition and measure/readout residual model",
            "status": "SYMBOLIC_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "DWM1231_3_local_source_residual",
            "quantity": "q_source^nu",
            "formula": "q_source^nu=P_loc nabla_mu T_res^{mu nu}+boundary/projector terms",
            "meaning": "local conservation/covariance residual vector blocking GR reduction unless zero or bounded",
            "required_inputs": "Noether descent, source profile, boundary/projector silence",
            "status": "DERIVED_OBJECT_NOT_ZERO",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    arena_laws = [
        {
            "arena_id": "ARENA1231_0_WEP_MICROSCOPE",
            "residual_law": "abs((sum_c DeltaF_TiPt,c delta w_c + DeltaK_TiPt) * tau_WEP) <= 2.8e-15",
            "status": "NOT_SCOREABLE",
            "missing_inputs": "DeltaF_TiPt,c; delta w_c priors; DeltaK_TiPt; official tau_WEP",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "arena_id": "ARENA1231_1_PPN",
            "residual_law": "abs(tau_PPN[source profile] * source_component_projection(delta w_c)) <= B_PPN",
            "status": "PLACEHOLDER_CONTRACT_ONLY",
            "missing_inputs": "tau_PPN; source profile; PPN bound; metric residual map",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "arena_id": "ARENA1231_2_clocks",
            "residual_law": "abs(tau_clock * clock/material_projection(delta w_c)) <= B_clock",
            "status": "PLACEHOLDER_CONTRACT_ONLY",
            "missing_inputs": "clock kernel; material projection; bound source",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "arena_id": "ARENA1231_3_orbital",
            "residual_law": "abs(tau_orbital * source_body_projection(delta w_c)) <= B_orbital",
            "status": "PLACEHOLDER_CONTRACT_ONLY",
            "missing_inputs": "orbital source profile; bound source; residual-to-orbit map",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1231_0_no_connectedness_claim",
            "decision": "do not claim parent matter-category connectedness",
            "because": "the interaction graph/source quotient is exact conditionally but not parent-constructed",
            "next_action": "try to build a parent interaction-graph certificate or retain component residual slots",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1231_1_keep_component_basis",
            "decision": "retain disconnected-component Delta_w basis",
            "because": "it is the honest finite fallback when naturality cannot collapse all components to one common scale",
            "next_action": "source component fractions and priors only as nonclaim until parent theorem or data gates close",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1231_2_best_route",
            "decision": "derive source-label forgetting before data scoring",
            "because": "a parent theorem is a GR-style reduction; finite scoring is only the backstop",
            "next_action": "attack the parent interaction graph certificate in 1232",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1231_0_connected_category",
            "claim": "ordinary matter category connected for source normalization",
            "status": "BLOCKED",
            "reason": "CMC1231_5 verdict is conditional only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1231_1_source_label_forgetting",
            "claim": "source-label forgetting theorem",
            "status": "BLOCKED",
            "reason": "SFL1231_4 verdict not closed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1231_2_Delta_w_zero",
            "claim": "Delta_w_AB=0 theorem-zero",
            "status": "BLOCKED",
            "reason": "disconnected-component residual basis remains active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1231_3_WEP_score",
            "claim": "WEP/MICROSCOPE finite branch score",
            "status": "BLOCKED",
            "reason": "component fractions, priors, DeltaK, and tau_WEP missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1231_4_local_GR",
            "claim": "local GR/Newton source-side reduction",
            "status": "BLOCKED",
            "reason": "q_source^nu is a residual object, not theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1231_0_1232",
            "target_file": "1232-Y5-R10-parent-interaction-graph-certificate-or-component-fraction-source-pack.md",
            "target_script": "scripts/Y5_R10_parent_interaction_graph_certificate_or_component_fraction_source_pack.py",
            "task": "try to construct the parent ordinary-matter interaction graph that makes C_ord connected; if it fails, build a strict nonclaim component-fraction source pack for Ti/Pt Delta_w",
            "success_condition": "either CMC1231_1 gets a parent-signed connected graph, or DWM1231_1 gains sourced nonclaim component-fraction requirements",
            "do_not_do": "do not claim Delta_w=0, WEP, PPN, local GR, or public source-coupling closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_paths = [
        SOURCE_REGISTER_PATH,
        CATEGORY_ATTEMPT_PATH,
        SOURCE_FORGETTING_PATH,
        RESIDUAL_BASIS_PATH,
        DELTA_MAP_PATH,
        ARENA_LAW_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(CATEGORY_ATTEMPT_PATH, category_attempt)
    write_csv(SOURCE_FORGETTING_PATH, source_forgetting)
    write_csv(RESIDUAL_BASIS_PATH, residual_basis)
    write_csv(DELTA_MAP_PATH, delta_map)
    write_csv(ARENA_LAW_PATH, arena_laws)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(NEXT_PATH, next_target)

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:ERROR:{exc}")

    all_sources_exist = all(parse_bool(row["path_exists"]) for row in source_register)
    all_needles_found = all(parse_bool(row["needle_found"]) for row in source_register)
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for table in [
            source_register,
            category_attempt,
            source_forgetting,
            residual_basis,
            delta_map,
            arena_laws,
            decisions,
            claim_gates,
            next_target,
        ]
        for row in table
    )
    conditional_graph_theorem = any(
        row["attempt_id"] == "CMC1231_1_interaction_graph_lemma" and row["result"] == "EXACT_CONDITIONAL_THEOREM"
        for row in category_attempt
    )
    connectedness_not_claimed = any(
        row["attempt_id"] == "CMC1231_5_verdict" and row["result"] == "CONDITIONAL_ONLY_RESIDUAL_MAP_REQUIRED"
        for row in category_attempt
    )
    source_forgetting_open = any(row["stack_id"] == "SFL1231_4_verdict" and row["status"] == "NOT_CLOSED" for row in source_forgetting)
    residual_basis_present = len(residual_basis) >= 6 and any(row["component_id"] == "DCW1231_6_measure_readout" for row in residual_basis)
    delta_map_present = any(row["map_id"] == "DWM1231_1_TiPt_difference" for row in delta_map)
    arena_laws_blocked = all(row["status"] in {"NOT_SCOREABLE", "PLACEHOLDER_CONTRACT_ONLY"} for row in arena_laws)
    gates_blocked = all(row["status"] == "BLOCKED" and is_false(row, "claim_allowed") for row in claim_gates)
    next_is_1232 = next_target[0]["target_file"].startswith("1232-Y5-R10-parent-interaction-graph")
    fw_recent = formalization_recent_count()

    validation = [
        validation_row(
            "VAL1231_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(parse_bool(row['path_exists']) for row in source_register)}/{len(source_register)} sources exist",
        ),
        validation_row(
            "VAL1231_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(parse_bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        ),
        validation_row(
            "VAL1231_2_conditional_graph_theorem",
            "interaction-graph connectedness theorem is exact conditional",
            conditional_graph_theorem,
            "CMC1231_1 result=EXACT_CONDITIONAL_THEOREM",
        ),
        validation_row(
            "VAL1231_3_connectedness_not_claimed",
            "connectedness/source-label theorem is not promoted",
            connectedness_not_claimed,
            "CMC1231_5 requires residual map",
        ),
        validation_row(
            "VAL1231_4_source_forgetting_open",
            "source-label forgetting stack remains open",
            source_forgetting_open,
            "SFL1231_4_verdict=NOT_CLOSED",
        ),
        validation_row(
            "VAL1231_5_residual_basis_present",
            "disconnected-component residual basis exists",
            residual_basis_present,
            f"basis_rows={len(residual_basis)}",
        ),
        validation_row(
            "VAL1231_6_delta_map_present",
            "Ti/Pt Delta_w component map exists",
            delta_map_present,
            "DWM1231_1_TiPt_difference present",
        ),
        validation_row(
            "VAL1231_7_arena_laws_blocked",
            "arena laws remain blocked/nonclaim",
            arena_laws_blocked,
            "all arena laws not scoreable or placeholder-only",
        ),
        validation_row(
            "VAL1231_8_claim_gates_blocked",
            "all claim gates remain blocked",
            gates_blocked,
            f"blocked_gates={sum(row['status'] == 'BLOCKED' for row in claim_gates)}/{len(claim_gates)}",
        ),
        validation_row(
            "VAL1231_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_generated_nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1231_10_next_target_1232",
            "next target attacks interaction graph or component fractions",
            next_is_1232,
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1231_11_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_counts),
        ),
        validation_row(
            "VAL1231_12_formalization_untouched",
            "formalization-workbench untouched during run",
            fw_recent == 0,
            f"formalization_recent_write_count_since_run_start={fw_recent}",
        ),
    ]
    validation.append(
        validation_row(
            "VAL1231_13_overall",
            "overall 1231 validation",
            all(row["status"] == "PASS" for row in validation),
            "1231 writes the connected matter-category theorem conditionally and supplies a nonclaim disconnected-component residual map",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1231 does **not** prove parent matter-category connectedness or source-label forgetting. It does give the clean conditional theorem: a connected parent-owned ordinary-matter interaction graph collapses natural source weights to one common factor. Because that graph is not parent-signed, the disconnected-component `Delta_w` residual map remains active.",
        "",
        "**Main progress:** the source-coupling gap is now split into two precise routes: prove `pi_0(C_ord)=*` for the source-density functor, or score `Delta_w_TiPt = sum_c (F_Ti,c-F_Pt,c) delta w_c + DeltaK_TiPt` with sourced component fractions and priors.",
        "",
        "**No-claim guard:** no connectedness, `Delta_w=0`, WEP, PPN, clock, orbital, local-GR, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Matter Category Connectedness Attempt",
        markdown_table(category_attempt, list(category_attempt[0].keys())),
        "",
        "## Source-Label Forgetting Proof Stack",
        markdown_table(source_forgetting, list(source_forgetting[0].keys())),
        "",
        "## Disconnected Component Residual Basis",
        markdown_table(residual_basis, list(residual_basis[0].keys())),
        "",
        "## Delta-w Component Map",
        markdown_table(delta_map, list(delta_map[0].keys())),
        "",
        "## Arena Residual Laws",
        markdown_table(arena_laws, list(arena_laws[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Next Target",
        markdown_table(next_target, list(next_target[0].keys())),
        "",
        "## Validation",
        markdown_table(validation, list(validation[0].keys())),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()

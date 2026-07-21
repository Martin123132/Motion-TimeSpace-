from __future__ import annotations

import csv
import math
import py_compile
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

CHECKPOINT = "4842"
CLAIM_ID = "L-684"
MARKER = "PPC4161_PARENT_MATTER_CATEGORY_NOHOM_SOURCE_PREFACTOR_PROOF_OR_FIRST_KAPPAA_HIDDEN_MARKER_ROW_4842"
PACKET_MARKER = "PPC4161_PACKET_PARENT_MATTER_CATEGORY_NOHOM_SOURCE_PREFACTOR_4842"
DECISION = "PARENT_MATTER_NOHOM_GRAPH_THEOREM_EXACT_BUT_EDGE_CERTIFICATES_UNSIGNED_FIRST_KAPPAA_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4843-Y5-R2FR-connected-matter-edge-certificates-and-generator-exhaustion-or-live-kappaA-bound-row.md"

DOC_PATH = POST / "4842-Y5-R2FR-parent-matter-category-no-Hom-source-prefactor-proof-or-first-kappaA-hidden-marker-row.md"
FORMAL_PATH = FORMAL / "858-PPC4161-parent-matter-category-noHom-source-prefactor-proof-or-first-kappaA-hidden-marker-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "parent_matter_nohom_kappaA_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4842_SOURCE_REGISTER.csv"
THEOREM_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4842_PARENT_MATTER_NOHOM_THEOREM_AUDIT.csv"
GRAPH_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4842_CONNECTED_MATTER_GRAPH_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4842_KAPPAA_NOHOM_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4842_KAPPAA_NOHOM_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4842_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4842_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4842_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4842_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4842_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "4841_doc": POST / "4841-Y5-R2FR-single-action-density-line-no-source-only-weight-theorem-or-first-delta-w-row.md",
    "4841_output": SOURCE_DIR / "P8_Y5_R2FR_4841_DELTA_W_RUNNER_OUTPUT.csv",
    "2612_nohom": SOURCE_DIR / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_SOURCE_ONLY_HOM_AUDIT.csv",
    "2687_attempt": SOURCE_DIR / "P8_Y5_R2FR_2687_NOHOM_PROOF_ATTEMPT.csv",
    "3251_connected": SOURCE_DIR / "P8_Y5_R2FR_3251_NOHOM_CONNECTED_NATURALITY_THEOREM.csv",
    "4432_constructor": SOURCE_DIR / "P8_Y5_R2FR_4432_CONSTRUCTOR_NOHOM_OUTPUT.csv",
    "2587_contract": SOURCE_DIR / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv",
    "2646_owner": SOURCE_DIR / "P8_Y5_MATTER_NORMALIZATION_OWNER_2646_OWNER_THEOREM_ATTEMPT.csv",
    "no_source_only": SOURCE_DIR / "P8_EM_no_source_only_matter_functor_residual.csv",
    "4838_kappa": SOURCE_DIR / "P8_Y5_R2FR_4838_KAPPA_G_NEWTON_ZERO_AUDIT.csv",
    "runner": RUNNER,
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_safe(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_safe(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker not in existing:
        write_text(path, existing.rstrip() + "\n\n" + text.strip() + "\n")


def as_float(value: Any) -> float:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return math.nan


def close_to(value: Any, target: float, tolerance: float = 1e-14) -> bool:
    number = as_float(value)
    return math.isfinite(number) and abs(number - target) <= tolerance


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4842_00_resume", SOURCES["resume"], "4842-Y5-R2FR-parent-matter-category-no-Hom-source-prefactor-proof-or-first-kappaA-hidden-marker-row.md", "4841 selected this parent matter no-Hom target."),
        ("SRC4842_01_4841_doc", SOURCES["4841_doc"], "SINGLE_ACTION_DENSITY_LINE_UNSIGNED_FIRST_DELTA_W_SPECIES_ROW_STAGED_NONCLAIM", "delta-w source-only weight handoff."),
        ("SRC4842_02_4841_output", SOURCES["4841_output"], "RUN4841_0_live_delta_w_zero_missing", "live delta_w zero blocked by parent no-Hom clauses."),
        ("SRC4842_03_2612_target", SOURCES["2612_nohom"], "HOM2612_0_target", "exact no-source-only Hom target."),
        ("SRC4842_04_2612_species", SOURCES["2612_nohom"], "MISSING_LABEL_FORGETTING_PARENT_CATEGORY_THEOREM", "species label proof gap."),
        ("SRC4842_05_2687_constructor", SOURCES["2687_attempt"], "NH2687_1_conditional_constructor", "conditional constructor route."),
        ("SRC4842_06_2687_counterexamples", SOURCES["2687_attempt"], "NH2687_3_counterexamples", "retained source-prefactor counterexamples."),
        ("SRC4842_07_3251_edge", SOURCES["3251_connected"], "NHE3251_2_edge_equalizer", "edge naturality equalizer lemma."),
        ("SRC4842_08_3251_graph", SOURCES["3251_connected"], "NHE3251_3_connected_graph", "connected graph collapse theorem."),
        ("SRC4842_09_4432_output", SOURCES["4432_constructor"], "NHOM4432_1_current_source_domain", "constructor no-Hom current blockers."),
        ("SRC4842_10_2587_action", SOURCES["2587_contract"], "MCA2587_2_minimal_matter_terms", "single observed matter action terms."),
        ("SRC4842_11_2646_countermodel", SOURCES["2646_owner"], "MNO2646_5_countermodel", "source-only relative weight countermodel."),
        ("SRC4842_12_kappaA", SOURCES["no_source_only"], "NSSR3509_2_kappa_A_source", "kappa_A source-prefactor residual."),
        ("SRC4842_13_hidden", SOURCES["no_source_only"], "NSSR3509_3_hidden_marker_source", "hidden marker source residual."),
        ("SRC4842_14_4838_guard", SOURCES["4838_kappa"], "KGN4838_6_no_GM_launder", "no measured-GM laundering guard."),
        ("SRC4842_15_runner", SOURCES["runner"], "def evaluate_row", "4842 executable runner."),
    ]


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_audit(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("PMN4842_0_target", "no-Hom active-source prefactor theorem", "Hom_parent(SpeciesLabel/HiddenMarker/Readout, Kappa_A^source)=common constants only", "TARGET_EXACT", "prove parent object language and generator exhaustion"),
        ("PMN4842_1_category", "parent matter category", "ordinary matter objects carry one action-density/source functor before readout", "CONTRACT_EXACT_UNSIGNED", "parent adoption of C_ord and L_action"),
        ("PMN4842_2_edge_equalizer", "edge naturality lemma", "for nonzero parent edge F_e:A->B, kappa_B F_e = F_e kappa_A implies kappa_A=kappa_B", "EXACT_CONDITIONAL_LEMMA", "edge ownership and nonzero certificates"),
        ("PMN4842_3_connected_graph", "connected ordinary graph", "connected parent-owned interaction graph collapses all relative kappa_A to one common mode", "EXACT_CONDITIONAL_THEOREM", "connected graph certificate on the same parent branch"),
        ("PMN4842_4_hidden_readout", "hidden/readout firewall", "hidden markers and readout/worldtube selectors cannot be arguments of source coefficients before variation", "UNSIGNED_FIREWALL", "no reentry and generator exhaustion"),
        ("PMN4842_5_common_mode", "common source scale", "universal kappa_* may be calibrated into G/source normalization only after relative modes vanish", "GUARD_ACTIVE", "no G/GM laundering for relative modes"),
        ("PMN4842_6_countermodel", "retained countermodel", "disconnected species, hidden marker, readout mask, or unsourced constructor can still define kappa_A", "COUNTERMODEL_RETAINED", "finite kappa_A row if proof not signed"),
        ("PMN4842_7_next", "next live target", "turn graph theorem into edge/source-functor certificates or source-backed residual row", "NEXT_TARGET_SELECTED", NEXT_TARGET),
    ]
    return [
        {
            "clause_id": clause_id,
            "object": obj,
            "mathematical_form": form,
            "current_result": result,
            "needed_signature_or_input": needed,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for clause_id, obj, form, result, needed in rows
    ]


def graph_contract(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("KAC4842_0_zero", "kappa_A_source_rel=0", "same action-density line + connected parent edge graph + source-functor generator exhaustion + no hidden/readout reentry", "conditional_only"),
        ("KAC4842_1_edge_law", "edge equalizer", "kappa_B F_e = F_e kappa_A on a one-dimensional positive action/source line", "exact_if_edge_parent_owned"),
        ("KAC4842_2_graph", "connected graph certificate", "ordinary matter components must sit in one connected parent-owned graph before readout", "runner_ready"),
        ("KAC4842_3_bound", "kappa_A_source_rel_abs", "R_graph + R_edge + R_generator + R_hidden + R_readout + R_constant + R_action", "runner_ready_values_missing"),
        ("KAC4842_4_density_feed", "density_qbasic_feed_abs", "P_density_kappaA*kappa_A_source_rel + P_kappaA_delta_w*kappa_A_source_rel", "runner_ready_values_missing"),
        ("KAC4842_5_next", "edge certificates/generator exhaustion", "fill live parent edge certificates or source-backed kappa_A residual row", "next_target"),
    ]
    return [
        {
            "contract_id": contract_id,
            "quantity": quantity,
            "definition": definition,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, quantity, definition, status in rows
    ]


def base_flags() -> dict[str, str]:
    return {
        "source_signed": "true",
        "units_signed": "true",
        "same_branch_signed": "true",
        "no_cancellation_guard": "true",
    }


def zero_flags() -> dict[str, str]:
    return {
        **base_flags(),
        "parent_matter_category_signed": "true",
        "single_action_density_line_signed": "true",
        "common_measure_normalization_signed": "true",
        "connected_ordinary_matter_category_signed": "true",
        "total_Hilbert_source_functor_signed": "true",
        "parent_generator_exhausted_signed": "true",
        "edge_ownership_certified_signed": "true",
        "edge_nonzero_certified_signed": "true",
        "species_label_forgetful_signed": "true",
        "hidden_marker_absent_signed": "true",
        "readout_no_reentry_signed": "true",
        "constant_sector_universal_signed": "true",
        "common_calibration_removed_signed": "true",
        "variation_before_readout_signed": "true",
        "no_species_only_jacobian_signed": "true",
        "no_post_variation_selector_signed": "true",
        "no_bound_as_source_signed": "true",
        "no_G_or_GM_absorption_signed": "true",
    }


def observed_graph() -> dict[str, str]:
    return {
        "objects": "charged_leptons;neutrinos;quarks;EM_photon;weak_bosons;gluons;Higgs",
        "edges": "charged_leptons-EM_photon;charged_leptons-weak_bosons;neutrinos-weak_bosons;quarks-EM_photon;quarks-gluons;quarks-weak_bosons;charged_leptons-Higgs;quarks-Higgs;weak_bosons-Higgs",
    }


def runner_inputs(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RUN4842_0_live_nohom_kappaA_zero_missing",
            "route_type": "nohom_kappaA_zero",
            "route": "live parent matter no-Hom kappaA zero audit",
            "source_path": str(SOURCES["3251_connected"]),
            "equation_ref": "NHE3251_2_edge_equalizer;NHE3251_3_connected_graph;NHE3251_6_current_verdict",
            "notes": "exact graph theorem exists but parent edge certificates, generator exhaustion and hidden/readout firewall are unsigned",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4842_1_conditional_connected_graph_zero_pass",
            "route_type": "nohom_kappaA_zero",
            "route": "conditional connected parent graph no-Hom theorem",
            "source_path": str(SOURCES["3251_connected"]),
            "equation_ref": "NHE3251_2_edge_equalizer;NHE3251_3_connected_graph",
            "notes": "nonclaim theorem-shape row: if all parent certificates are signed, relative source prefactors vanish",
            "timestamp_utc": timestamp,
            **zero_flags(),
            **observed_graph(),
        },
        {
            "row_id": "RUN4842_2_graph_certificate_smoke_pass",
            "route_type": "graph_certificate",
            "route": "observed ordinary-matter interaction graph connectivity smoke",
            "source_path": str(SOURCES["3251_connected"]),
            "equation_ref": "NHE3251_3_connected_graph",
            "notes": "nonclaim topology smoke only; does not assert MTS parent ownership of the edges",
            "timestamp_utc": timestamp,
            **base_flags(),
            **observed_graph(),
        },
        {
            "row_id": "RUN4842_3_live_kappaA_bound_missing",
            "route_type": "kappaA_bound",
            "route": "live first kappaA hidden-marker residual row missing",
            "source_path": str(SOURCES["no_source_only"]),
            "equation_ref": "NSSR3509_2_kappa_A_source;NSSR3509_3_hidden_marker_source",
            "notes": "residual slots are named but live graph/generator/hidden/readout/source projection values are missing",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4842_4_kappaA_hidden_marker_bound_smoke_pass",
            "route_type": "kappaA_bound",
            "route": "finite kappaA hidden-marker smoke",
            "source_path": str(SOURCES["no_source_only"]),
            "equation_ref": "NSSR3509_2_kappa_A_source;NSSR3509_3_hidden_marker_source",
            "notes": "nonclaim arithmetic smoke for retained source-prefactor residual feed",
            "timestamp_utc": timestamp,
            **base_flags(),
            "R_graph_disconnect_abs": "0.0007",
            "R_edge_ownership_abs": "0.0006",
            "R_generator_exhaustion_abs": "0.0008",
            "R_hidden_marker_abs": "0.0005",
            "R_readout_reentry_abs": "0.0004",
            "R_constant_sector_abs": "0.0003",
            "R_action_line_abs": "0.0002",
            "P_kappaA_delta_w_abs": "0.9",
            "P_density_kappaA_abs": "1.1",
            "P_kappaA_qbar_abs": "1.0",
            "Qbar_source_XH_bound_abs": "0.01475",
            "K_source_abs": "1.5",
            "tau_BY5_kappaA_abs": "2.0",
        },
        {
            "row_id": "RUN4842_5_forbidden_nohom_by_declaration",
            "route_type": "nohom_kappaA_zero",
            "route": "forbidden noHom by declaration",
            "source_path": str(SOURCES["2612_nohom"]),
            "equation_ref": "HOM2612_4_verdict",
            "notes": "NOHOM_BY_DECLARATION does not supply parent edge/source-functor proof",
            "timestamp_utc": timestamp,
            **zero_flags(),
            **observed_graph(),
        },
        {
            "row_id": "RUN4842_6_forbidden_hidden_marker_fit",
            "route_type": "kappaA_bound",
            "route": "forbidden hidden marker fit",
            "source_path": str(SOURCES["no_source_only"]),
            "equation_ref": "NSSR3509_3_hidden_marker_source",
            "notes": "HIDDEN_MARKER_FIT cannot be used as a parent source coefficient",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4842_7_forbidden_G_absorption",
            "route_type": "kappaA_bound",
            "route": "forbidden G absorption",
            "source_path": str(SOURCES["4838_kappa"]),
            "equation_ref": "KGN4838_6_no_GM_launder",
            "notes": "G_ABSORPTION cannot erase relative kappa_A modes",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4842_8_forbidden_edge_by_label_only",
            "route_type": "graph_certificate",
            "route": "forbidden edge by label only",
            "source_path": str(SOURCES["3251_connected"]),
            "equation_ref": "NHE3251_3_connected_graph",
            "notes": "EDGE_BY_LABEL_ONLY is not an interaction/current edge certificate",
            "timestamp_utc": timestamp,
            **base_flags(),
            **observed_graph(),
        },
        {
            "row_id": "RUN4842_9_forbidden_bound_as_source",
            "route_type": "kappaA_bound",
            "route": "forbidden bound as source",
            "source_path": str(SOURCES["4432_constructor"]),
            "equation_ref": "NHOM4432_3_bound_inversion_guard",
            "notes": "BOUND_AS_SOURCE cannot replace a parent-owned prediction row",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
    ]


def run_runner() -> list[dict[str, str]]:
    subprocess.run([sys.executable, str(RUNNER), str(RUNNER_INPUT), str(RUNNER_OUTPUT)], check=True)
    return read_csv(RUNNER_OUTPUT)


def row_by_id(rows: list[dict[str, str]], row_id: str) -> dict[str, str]:
    return next(row for row in rows if row.get("row_id") == row_id)


def status_csv(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "decision": DECISION,
            "status": "private_nonclaim_gate_installed",
            "live_claim_allowed": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4842_0_theorem",
            "decision": "A connected parent-owned action/source graph kills relative kappa_A source prefactors by edge naturality.",
            "effect": "turns no-Hom from a declaration into an edge-certificate theorem route",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4842_1_nonclaim",
            "decision": "Live zero remains blocked because parent edge ownership, generator exhaustion, and hidden/readout firewall are unsigned.",
            "effect": "retains a finite kappa_A hidden-marker residual row instead of claiming local GR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4842_2_next",
            "decision": NEXT_TARGET,
            "effect": "source or derive the actual edge certificates and generator-exhaustion package",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CG4842_0_edge_lemma", "edge equalizer lemma", "PASS_CONDITIONAL", "nonzero parent interaction/current edge equalizes source prefactors"),
        ("CG4842_1_graph_theorem", "connected graph collapse", "PASS_CONDITIONAL", "relative modes vanish if graph and edge ownership are parent-signed"),
        ("CG4842_2_live_zero", "live kappa_A zero", "BLOCKED_UNSIGNED", "edge certificates/generator exhaustion/hidden-readout firewall are not signed"),
        ("CG4842_3_live_bound", "live kappa_A residual", "BLOCKED_MISSING_VALUES", "residual components and projections are missing"),
        ("CG4842_4_smoke", "runner arithmetic", "PASS_NONCLAIM", "graph topology and finite kappa_A smoke rows compute"),
        ("CG4842_5_local_GR", "local GR/Newton claim", "NOT_ALLOWED", "source-prefactor branch remains unsigned or unbounded"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "meaning": meaning,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, meaning in rows
    ]


def compile_ok(path: Path) -> bool:
    try:
        py_compile.compile(str(path), doraise=True)
    except py_compile.PyCompileError:
        return False
    return True


def cleanup_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validate(timestamp: str, sources: list[dict[str, Any]], outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "passed": bool(passed),
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    add("VAL4842_00_sources_exist", all(str(row["exists"]) == "True" for row in sources), "all cited source paths exist")
    add("VAL4842_01_needles_found", all(str(row["needle_found"]) == "True" for row in sources), "all source needles found")
    add("VAL4842_02_runner_compiles", compile_ok(RUNNER), "runner compiles")
    add("VAL4842_03_generator_compiles", compile_ok(Path(__file__)), "generator compiles")
    input_rows = read_csv(RUNNER_INPUT)
    add("VAL4842_04_output_count", len(outputs) == len(input_rows), f"outputs={len(outputs)} inputs={len(input_rows)}")
    add("VAL4842_05_claims_false", all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in outputs), "runner hard-codes nonclaim rows")
    live_zero = row_by_id(outputs, "RUN4842_0_live_nohom_kappaA_zero_missing")
    add("VAL4842_06_live_zero_blocked", live_zero["runner_status"] == "BLOCKED_NOHOM_KAPPAA_ZERO_CLAUSES", live_zero["missing_for_claim"])
    graph = row_by_id(outputs, "RUN4842_2_graph_certificate_smoke_pass")
    add("VAL4842_07_graph_smoke_connected", graph["runner_status"] == "GRAPH_CERTIFICATE_PASS_NONCLAIM" and graph["graph_component_count"] == "1", "observed interaction graph smoke is connected")
    cond = row_by_id(outputs, "RUN4842_1_conditional_connected_graph_zero_pass")
    add("VAL4842_08_conditional_zero_values", all([
        cond["runner_status"] == "NOHOM_KAPPAA_ZERO_PASS_NONCLAIM",
        close_to(cond["kappaA_source_rel_abs"], 0.0),
        close_to(cond["density_qbasic_feed_abs"], 0.0),
    ]), "conditional graph theorem row zeros kappa_A feed")
    bound = row_by_id(outputs, "RUN4842_4_kappaA_hidden_marker_bound_smoke_pass")
    add("VAL4842_09_kappaA_smoke_values", all([
        close_to(bound["kappaA_source_rel_abs"], 0.0035),
        close_to(bound["delta_w_species_abs"], 0.00315),
        close_to(bound["density_qbasic_feed_abs"], 0.007),
        close_to(bound["alpha_source_abs"], 0.000154875),
        close_to(bound["BY5_kappaA_feed_abs"], 0.014),
    ]), "kappa_A hidden-marker smoke row computes expected residual feed")
    forbidden = [row for row in outputs if row["row_id"].startswith("RUN4842_5_") or row["row_id"].startswith("RUN4842_6_") or row["row_id"].startswith("RUN4842_7_") or row["row_id"].startswith("RUN4842_8_") or row["row_id"].startswith("RUN4842_9_")]
    add("VAL4842_10_forbidden_routes_fail", all(row["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row in forbidden), "all forbidden shortcuts fail")
    live_bound = row_by_id(outputs, "RUN4842_3_live_kappaA_bound_missing")
    add("VAL4842_11_live_bound_blocked", live_bound["runner_status"] == "BLOCKED_KAPPAA_BOUND_INPUTS", live_bound["missing_for_claim"])
    add("VAL4842_12_next_target_recorded", NEXT_TARGET in read_text(NEXT_TARGET_CSV) and NEXT_TARGET in read_text(RESUME_PATH), "next target recorded in CSV and resume")
    cleanup_pycache()
    add("VAL4842_13_no_pycache_left", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ removed")
    return checks


def write_next_target(timestamp: str) -> None:
    write_csv(
        NEXT_TARGET_CSV,
        [
            {
                "checkpoint": CHECKPOINT,
                "next_target": NEXT_TARGET,
                "reason": "4842 reduces the source-prefactor proof to connected parent edge certificates and generator exhaustion.",
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        ],
    )


def write_resume(timestamp: str) -> None:
    write_text(
        RESUME_PATH,
        f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4842-Y5-R2FR-parent-matter-category-no-Hom-source-prefactor-proof-or-first-kappaA-hidden-marker-row.md`
Marker: `{MARKER}`

## Where we are

4842 attacks the source-prefactor coupling gap directly:

```text
For each parent-owned nonzero edge F_e:A->B:
    kappa_B F_e = F_e kappa_A
therefore on a one-dimensional positive action/source line:
    kappa_A = kappa_B
connected graph => all kappa_A collapse to one common mode
```

## Live blockers

- The no-Hom theorem is now an edge-certificate theorem, not a declaration.
- The conditional graph proof is exact, but live MTS has not signed parent edge ownership, generator exhaustion, hidden/readout firewall, or constant-sector universality.
- A finite `kappa_A_source_rel` row is staged for the fallback route and feeds `delta_w_species`, density q-basicness, and the local source denominator.
- Local GR/Newton remains nonclaim until 4842 feeds 4841/4840/4839/4838 with signed zero or live finite rows.

## Next target

`{NEXT_TARGET}`
""",
    )


def write_docs(timestamp: str, sources: list[dict[str, Any]], audit: list[dict[str, Any]], contract: list[dict[str, Any]], outputs: list[dict[str, str]], validations: list[dict[str, Any]]) -> None:
    doc = f"""# 4842 Y5 R2FR parent matter category no-Hom source-prefactor proof or first kappaA hidden-marker row

**Status:** 4842 turns the source-prefactor coupling problem into a concrete connected-graph theorem. If ordinary matter lives in one parent action-density/source category and every ordinary component is linked by parent-owned nonzero interaction/current edges, naturality forces all active-source prefactors `kappa_A` to be equal. That common mode is calibration; relative source coupling vanishes. The live branch remains nonclaim because edge ownership, generator exhaustion, hidden/readout firewall, and constant-sector universality are not parent-signed.

**Decision:** `{DECISION}`.

## Core derivation

For a parent-owned edge `F_e:A->B`, source-prefactor naturality requires:

```text
kappa_B F_e = F_e kappa_A
```

On a one-dimensional positive action/source line with nonzero `F_e`, this gives:

```text
kappa_A = kappa_B
```

If the ordinary matter graph is connected, the equality propagates along every path:

```text
kappa_A = kappa_* for all ordinary A
kappa_A_source_rel = P_perp_common_mode kappa_A = 0
```

If the theorem is not signed, the retained finite row is:

```text
kappa_A_source_rel =
  R_graph + R_edge + R_generator + R_hidden + R_readout + R_constant + R_action
density_qbasic_feed =
  P_density_kappaA kappa_A_source_rel + P_kappaA_delta_w kappa_A_source_rel
```

## Source Register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## Theorem Audit

{md_table(audit, ["clause_id", "object", "current_result", "needed_signature_or_input"])}

## Runner Contract

{md_table(contract, ["contract_id", "quantity", "definition", "status"])}

## Runner Output

{md_table(outputs, ["row_id", "runner_status", "graph_component_count", "kappaA_source_rel_abs", "delta_w_species_abs", "density_qbasic_feed_abs", "alpha_source_abs", "BY5_kappaA_feed_abs", "missing_for_claim"])}

## Validation

{md_table(validations, ["check_id", "status", "detail"])}

## What changed

- The coupling gap is now a graph/naturality proof target: no-Hom is not allowed to be asserted by taste.
- The ordinary interaction graph smoke is executable and connected, but it is not yet a parent-edge certificate.
- The fallback `kappa_A_source_rel` row is staged so hidden markers/readout reentry cannot be silently ignored.

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    formal = f"""# 858 PPC4161 parent matter category no-Hom source-prefactor proof or first kappaA hidden-marker row

Checkpoint: `{DOC_PATH}`

4842 makes the coupling route sharper. Relative active-source prefactors vanish if parent-owned nonzero interaction/current edges connect ordinary matter before readout; the proof is `kappa_B F_e = F_e kappa_A`, so nonzero edge naturality equalizes the coefficients and graph connectedness leaves only one common calibration mode.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_formal_registers(timestamp: str) -> None:
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "parent_matter_category_noHom_source_prefactor_proof_or_first_kappaA_hidden_marker_row",
        "current_evidence": "4842 derives the connected-edge naturality theorem for relative kappa_A source prefactors and stages finite kappa_A residual rows.",
        "status": "parent_matter_noHom_kappaA_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "parent edge certificates, source-functor generator exhaustion, hidden/readout firewall and constant-sector universality remain unsigned",
        "sector": "local_gr_Newton_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "conditional theorem is exact but live branch lacks parent-owned edge certificates and live residual values",
        "title": "Parent matter category no-Hom source-prefactor proof or first kappaA hidden-marker row",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    existing = read_text(CLAIMS_PATH)
    if CLAIM_ID not in existing:
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(claim_row.keys()))
            writer.writerow(claim_row)
    append_once(
        SPINE_PATH,
        MARKER,
        f"""## PPC4161 4842 parent matter category no-Hom source-prefactor gate

`{MARKER}`. The relative source-coupling gap is now controlled by a connected parent edge theorem: for each nonzero parent-owned interaction/current edge `F_e:A->B`, naturality gives `kappa_B F_e=F_e kappa_A`, so connected ordinary matter collapses all `kappa_A` to one common calibration mode. Live status remains nonclaim until edge ownership, generator exhaustion and hidden/readout firewall are signed. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4842 parent matter category no-Hom source-prefactor proof

`{PACKET_MARKER}`. `{MARKER}` replaces the vague coupling complaint with a graph/naturality theorem and a fallback `kappa_A_source_rel` residual row. Next: `{NEXT_TARGET}`.""",
    )


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    audit = theorem_audit(timestamp)
    contract = graph_contract(timestamp)
    inputs = runner_inputs(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_AUDIT, audit)
    write_csv(GRAPH_CONTRACT, contract)
    write_csv(RUNNER_INPUT, inputs)
    write_csv(STATUS_CSV, status_csv(timestamp))
    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(CLAIM_GATES, claim_gate_rows(timestamp))
    write_next_target(timestamp)
    write_resume(timestamp)

    outputs = run_runner()
    cleanup_pycache()
    validations = validate(timestamp, sources, outputs)
    write_csv(VALIDATION_CSV, validations)
    write_docs(timestamp, sources, audit, contract, outputs, validations)
    update_formal_registers(timestamp)
    cleanup_pycache()

    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"4842 validation failed: {failed}")
    print(f"4842 complete: {DOC_PATH}")


if __name__ == "__main__":
    main()

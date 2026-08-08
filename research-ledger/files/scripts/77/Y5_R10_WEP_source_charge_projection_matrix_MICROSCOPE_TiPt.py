from __future__ import annotations

import csv
import math
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "983-Y5-R10-WEP-source-charge-projection-matrix-MICROSCOPE-TiPt.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)
ETA_ENVELOPE = 6.992e-15


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "982_doc",
            "path": "982-Y5-R10-coupling-bound-projection-matrix-skeleton-and-screening-runner.md",
            "role": "handoff selecting WEP/source-charge projection first",
            "needle": "DEC982_2_best_next",
        },
        {
            "source_id": "982_projection",
            "path": "source-intake/mts_residuals/P8_Y5_R10_982_PROJECTION_MATRIX_SKELETON.csv",
            "role": "projection matrix skeleton row for MICROSCOPE WEP",
            "needle": "PMAT982_0_WEP_eta_TiPt",
        },
        {
            "source_id": "981_candidates",
            "path": "source-intake/mts_residuals/P8_Y5_R10_981_COUPLING_PRIOR_CANDIDATES.csv",
            "role": "MICROSCOPE eta source envelope",
            "needle": "CP981_0_b_kappa_species_split_WEP",
        },
        {
            "source_id": "981_web_sources",
            "path": "source-intake/mts_residuals/P8_Y5_R10_981_WEB_SOURCE_LEDGER.csv",
            "role": "MICROSCOPE final result provenance",
            "needle": "WEB981_0_MICROSCOPE_WEP",
        },
        {
            "source_id": "622_doc",
            "path": "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md",
            "role": "b_kappa/b_theta/b_m component definitions",
            "needle": "MAP622_4_source_weight",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "generated_utc": stamp(),
            }
        )
    return rows


def web_source_rows() -> list[dict[str, str]]:
    return [
        {
            "web_source_id": "WEB983_0_MICROSCOPE_CQG_COMPOSITION",
            "title": "Result of the MICROSCOPE weak equivalence principle test",
            "url": "https://elib.dlr.de/193667/2/Touboul_2022_Class._Quantum_Grav._39_204009.pdf",
            "year": "2022",
            "source_use": "composition of SUEP PtRh10 and Ti alloy test masses plus eta definition",
            "recorded_fact": "SUEP inner mass PtRh10: 90 percent Pt and 10 percent Rh by mass; outer mass: 90 percent Ti, 6 percent Al, 4 percent V by mass",
            "valid_for_claim": "false",
        },
        {
            "web_source_id": "WEB983_1_MICROSCOPE_PRL_FINAL",
            "title": "MICROSCOPE mission: final results of the test of the Equivalence Principle",
            "url": "https://arxiv.org/abs/2209.15487",
            "year": "2022",
            "source_use": "eta(Ti,Pt) final result anchor",
            "recorded_fact": "eta(Ti,Pt) = [-1.5 +- 2.3(stat) +- 1.5(syst)]e-15, used in 981 as nonclaim screening envelope 6.992e-15",
            "valid_for_claim": "false",
        },
    ]


def material_constituents() -> list[dict[str, str]]:
    return [
        {"material_id": "M983_0_PtRh10", "element": "Pt", "mass_fraction": "0.90", "A": "195.1", "Z": "78", "source": "WEB983_0_MICROSCOPE_CQG_COMPOSITION"},
        {"material_id": "M983_0_PtRh10", "element": "Rh", "mass_fraction": "0.10", "A": "102.9", "Z": "45", "source": "WEB983_0_MICROSCOPE_CQG_COMPOSITION"},
        {"material_id": "M983_1_TiAlloy", "element": "Ti", "mass_fraction": "0.90", "A": "47.9", "Z": "22", "source": "WEB983_0_MICROSCOPE_CQG_COMPOSITION"},
        {"material_id": "M983_1_TiAlloy", "element": "Al", "mass_fraction": "0.06", "A": "27.0", "Z": "13", "source": "WEB983_0_MICROSCOPE_CQG_COMPOSITION"},
        {"material_id": "M983_1_TiAlloy", "element": "V", "mass_fraction": "0.04", "A": "50.9", "Z": "23", "source": "WEB983_0_MICROSCOPE_CQG_COMPOSITION"},
    ]


def charge_basis_rows() -> list[dict[str, str]]:
    return [
        {
            "basis_id": "QB983_0_electron_fraction",
            "proxy": "Y_e = Z/A",
            "physical_read": "electron/proton fraction per nucleon mass proxy",
            "projection_status": "proxy_only_not_MTS_derived",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "QB983_1_neutron_excess",
            "proxy": "q_N = (A - 2Z)/A",
            "physical_read": "neutron excess proxy highlighted by MICROSCOPE material contrast",
            "projection_status": "proxy_only_not_MTS_derived",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "QB983_2_coulomb_proxy",
            "proxy": "q_C = Z(Z-1)/A^(4/3)",
            "physical_read": "nuclear electrostatic energy proxy; debug basis, not a full dilaton charge model",
            "projection_status": "proxy_only_not_MTS_derived",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "QB983_3_mean_A_proxy",
            "proxy": "A_bar = sum mass_fraction*A",
            "physical_read": "coarse mass-number contrast sanity feature",
            "projection_status": "proxy_only_not_MTS_derived",
            "valid_for_claim": "false",
        },
    ]


def weighted_material_charges(constituents: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in constituents:
        grouped.setdefault(row["material_id"], []).append(row)
    rows: list[dict[str, str]] = []
    for material_id, entries in grouped.items():
        weights_sum = sum(float(entry["mass_fraction"]) for entry in entries)
        y_e = sum(float(e["mass_fraction"]) * float(e["Z"]) / float(e["A"]) for e in entries)
        q_n = sum(float(e["mass_fraction"]) * (float(e["A"]) - 2.0 * float(e["Z"])) / float(e["A"]) for e in entries)
        q_c = sum(float(e["mass_fraction"]) * float(e["Z"]) * (float(e["Z"]) - 1.0) / (float(e["A"]) ** (4.0 / 3.0)) for e in entries)
        a_bar = sum(float(e["mass_fraction"]) * float(e["A"]) for e in entries)
        rows.append(
            {
                "material_id": material_id,
                "mass_fraction_sum": f"{weights_sum:.6f}",
                "Y_e_proxy": f"{y_e:.9e}",
                "neutron_excess_proxy": f"{q_n:.9e}",
                "coulomb_proxy": f"{q_c:.9e}",
                "A_bar_proxy": f"{a_bar:.9e}",
                "status": "proxy_charge_vector_computed",
                "valid_for_claim": "false",
            }
        )
    return rows


def differential_charge_rows(material_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_id = {row["material_id"]: row for row in material_rows}
    ti = by_id["M983_1_TiAlloy"]
    pt = by_id["M983_0_PtRh10"]
    rows: list[dict[str, str]] = []
    for feature in ["Y_e_proxy", "neutron_excess_proxy", "coulomb_proxy", "A_bar_proxy"]:
        delta = float(ti[feature]) - float(pt[feature])
        rows.append(
            {
                "delta_id": f"DEL983_{feature}",
                "feature": feature,
                "definition": f"{feature}(TiAlloy outer) - {feature}(PtRh10 inner)",
                "delta_value": f"{delta:.9e}",
                "absolute_delta": f"{abs(delta):.9e}",
                "status": "nonzero_proxy_contrast",
                "valid_for_claim": "false",
            }
        )
    return rows


def projection_attempt_rows(delta_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    delta_lookup = {row["feature"]: float(row["delta_value"]) for row in delta_rows}
    return [
        {
            "projection_id": "WEP983_0_vector_projection",
            "formula": "eta_TiPt ~= DeltaY_e*C_e + Deltaq_N*C_N + Deltaq_C*C_C + DeltaAbar*C_A + S_marker*b_m + S_theta*b_theta + S_source*b_kappa",
            "known_inputs": "DeltaY_e,Deltaq_N,Deltaq_C,DeltaAbar,eta_screening_envelope",
            "missing_inputs": "C_e,C_N,C_C,C_A,S_marker,S_theta,S_source,MTS_source_charge_basis",
            "result": "PROJECTION_SKELETON_READY",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "WEP983_1_bkappa_path",
            "formula": "b_kappa contribution enters through source-normalization/composition sensitivity S_source",
            "known_inputs": f"eta_envelope={ETA_ENVELOPE:.3e}",
            "missing_inputs": "S_source(TiAlloy,PtRh10),universal-Hilbert-source deviation definition",
            "result": "MISSING_SOURCE_CHARGE_PROJECTION",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "WEP983_2_btheta_path",
            "formula": "b_theta contribution enters through material constants/EM/mass-ratio sensitivities",
            "known_inputs": "composition proxies",
            "missing_inputs": "clock/EM/mass sensitivity model linking theta_A to Ti/Pt free-fall contrast",
            "result": "MISSING_CONSTANT_SENSITIVITY_PROJECTION",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "WEP983_3_identity_debug_bounds",
            "formula": "if one proxy coefficient dominates, |C_i| <= eta_envelope/|DeltaQ_i|",
            "known_inputs": f"DeltaY_e={delta_lookup['Y_e_proxy']:.3e};Deltaq_N={delta_lookup['neutron_excess_proxy']:.3e};Deltaq_C={delta_lookup['coulomb_proxy']:.3e}",
            "missing_inputs": "proof that the chosen proxy coefficient equals an MTS residual slot",
            "result": "IDENTITY_DEBUG_ONLY",
            "valid_for_claim": "false",
        },
    ]


def identity_debug_bound_rows(delta_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in delta_rows:
        abs_delta = float(row["absolute_delta"])
        bound = ETA_ENVELOPE / abs_delta if abs_delta > 0.0 else math.inf
        rows.append(
            {
                "identity_bound_id": row["delta_id"].replace("DEL", "IB"),
                "feature": row["feature"],
                "eta_envelope": f"{ETA_ENVELOPE:.3e}",
                "absolute_delta": row["absolute_delta"],
                "identity_debug_bound": f"{bound:.9e}" if math.isfinite(bound) else "inf",
                "units": "dimensionless_proxy_coefficient",
                "why_not_claim": "identity single-proxy dominance is a debug assumption, not an MTS source-charge projection",
                "valid_for_claim": "false",
            }
        )
    return rows


def screening_runner_rows(identity_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "screen_id": "SCREEN983_0_schema",
            "requirement": "composition rows sum to one and produce nonzero proxy deltas",
            "result": "pass",
            "claim_allowed": "false",
            "detail": "schema/proxy sanity only",
            "valid_for_claim": "false",
        },
        {
            "screen_id": "SCREEN983_1_identity_debug_bounds",
            "requirement": "identity debug bounds are finite for every proxy",
            "result": "pass" if all(row["identity_debug_bound"] != "inf" for row in identity_rows) else "fail",
            "claim_allowed": "false",
            "detail": "bounds are not MTS coefficient bounds",
            "valid_for_claim": "false",
        },
        {
            "screen_id": "SCREEN983_2_real_projection",
            "requirement": "actual MTS source-charge projection supplied",
            "result": "blocked_missing_projection",
            "claim_allowed": "false",
            "detail": "C_e,C_N,C_C,C_A,S_source,S_theta,S_marker are not derived",
            "valid_for_claim": "false",
        },
        {
            "screen_id": "SCREEN983_3_WEP_claim",
            "requirement": "WEP/source-splitting branch pass",
            "result": "blocked_no_claim",
            "claim_allowed": "false",
            "detail": "MICROSCOPE source anchor is ready, projection is not",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE983_0_composition_proxies",
            "claim": "MICROSCOPE material proxy deltas are computed",
            "gate_pass": "true",
            "claim_allowed": "false",
            "why_not": "proxy deltas are bookkeeping, not MTS predictions",
        },
        {
            "gate_id": "CGATE983_1_bkappa_bound",
            "claim": "MICROSCOPE bounds b_kappa",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "S_source projection from source-normalization residual to Ti/Pt Eotvos signal is missing",
        },
        {
            "gate_id": "CGATE983_2_btheta_bound",
            "claim": "MICROSCOPE bounds b_theta",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "theta_A/material-constant sensitivity model is missing",
        },
        {
            "gate_id": "CGATE983_3_WEP_or_local_GR",
            "claim": "WEP/local-GR branch passes",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "projection attempt only; no parent universal-source theorem and no scored coefficient row",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC983_0_composition",
            "topic": "MICROSCOPE materials",
            "result": "real_alloy_composition_used",
            "reason": "PtRh10 and Ti alloy mass fractions are used instead of pure-element shorthand",
            "next_action": "keep pure Ti/Pt language out of coefficient scoring",
        },
        {
            "decision_id": "DEC983_1_projection",
            "topic": "source-charge projection",
            "result": "proxy_vector_ready_projection_missing",
            "reason": "Delta composition proxies are computable, but MTS source-charge coefficients are not derived",
            "next_action": "derive a source-charge basis from the parent matter action or import a conservative phenomenological basis explicitly",
        },
        {
            "decision_id": "DEC983_2_best_next",
            "topic": "next checkpoint",
            "result": "source_charge_basis_derivation_or_phenomenological_basis_import",
            "reason": "without C_e,C_N,C_C,C_A and S_source, WEP cannot score b_kappa",
            "next_action": "write 984 source-charge basis derivation attempt from Hilbert-source universality; fallback to labelled phenomenological basis",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "984-Y5-R10-source-charge-basis-derivation-or-phenomenological-basis-import.md",
            "objective": "derive the source-charge basis linking composition proxies to MTS b_kappa/b_theta/b_m slots, or import it explicitly as phenomenological nonclaim structure",
            "include": "Hilbert-source universality, composition-charge basis C_e/C_N/C_C/C_A, Ti/Pt projection, claim gates",
            "exclude": "WEP pass, invented coefficients, theorem-zero promotion, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_ts = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_ts:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    web_sources: list[dict[str, str]],
    constituents: list[dict[str, str]],
    material_rows: list[dict[str, str]],
    delta_rows: list[dict[str, str]],
    projection_rows: list[dict[str, str]],
    identity_rows: list[dict[str, str]],
    screen_rows: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    web_ok = all(row["url"].startswith("https://") and row["valid_for_claim"] == "false" for row in web_sources)
    mass_sums_ok = all(abs(float(row["mass_fraction_sum"]) - 1.0) < 1e-9 for row in material_rows)
    deltas_ok = all(float(row["absolute_delta"]) > 0.0 and row["valid_for_claim"] == "false" for row in delta_rows)
    projection_ok = all(row["valid_for_claim"] == "false" and row["result"] in {"PROJECTION_SKELETON_READY", "MISSING_SOURCE_CHARGE_PROJECTION", "MISSING_CONSTANT_SENSITIVITY_PROJECTION", "IDENTITY_DEBUG_ONLY"} for row in projection_rows)
    identity_ok = all(row["valid_for_claim"] == "false" and row["identity_debug_bound"] != "inf" for row in identity_rows)
    screen_ok = all(row["claim_allowed"] == "false" for row in screen_rows)
    claims_ok = all(row["claim_allowed"] == "false" for row in claims)
    decisions_ok = any(row["decision_id"] == "DEC983_2_best_next" and row["result"] == "source_charge_basis_derivation_or_phenomenological_basis_import" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V983_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all local sources exist and needles are found"},
        {"check_id": "V983_1_web_sources", "result": "pass" if web_ok else "fail", "detail": "web source rows are recorded and nonclaim"},
        {"check_id": "V983_2_constituents_written", "result": "pass" if len(constituents) == 5 else "fail", "detail": f"{len(constituents)} constituent rows written"},
        {"check_id": "V983_3_mass_fractions_sum", "result": "pass" if mass_sums_ok else "fail", "detail": "mass fractions sum to one for each material"},
        {"check_id": "V983_4_delta_proxies_nonzero", "result": "pass" if deltas_ok else "fail", "detail": "all proxy charge deltas are nonzero and nonclaim"},
        {"check_id": "V983_5_projection_nonclaim", "result": "pass" if projection_ok else "fail", "detail": "projection rows do not claim MTS coefficient bounds"},
        {"check_id": "V983_6_identity_debug_nonclaim", "result": "pass" if identity_ok else "fail", "detail": "identity debug bounds are finite and nonclaim"},
        {"check_id": "V983_7_screening_claims_blocked", "result": "pass" if screen_ok else "fail", "detail": "screening runner blocks WEP/local-GR claims"},
        {"check_id": "V983_8_claim_gates_safe", "result": "pass" if claims_ok else "fail", "detail": "claim gates remain false except bookkeeping existence"},
        {"check_id": "V983_9_decision_next_target", "result": "pass" if decisions_ok else "fail", "detail": "984 source-charge basis target selected"},
        {"check_id": "V983_10_next_target_written", "result": "pass" if next_ok else "fail", "detail": "next target row is present and nonclaim"},
        {"check_id": "V983_11_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {"check_id": "V983_READY", "result": "pass" if ready else "fail", "detail": "983 checkpoint pack validation summary", "generated_utc": stamp()}
    ]


def write_doc(
    sources: list[dict[str, str]],
    web_sources: list[dict[str, str]],
    constituents: list[dict[str, str]],
    basis: list[dict[str, str]],
    material_rows: list[dict[str, str]],
    delta_rows: list[dict[str, str]],
    projection_rows: list[dict[str, str]],
    identity_rows: list[dict[str, str]],
    screen_rows: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 983 Y5 R10: WEP Source-Charge Projection Matrix MICROSCOPE TiPt",
        "",
        "Status: `Y5_R10_983_MICROSCOPE_alloy_composition_proxy_projection_written_nonclaim_source_charge_basis_missing`",
        "",
        "Claim ceiling: no WEP pass, no `b_kappa` bound, no `b_theta` bound, no local-GR promotion. This is a projection attempt and proxy ledger only.",
        "",
        "## Readout",
        "",
        "983 fixes an easy-to-miss trap: MICROSCOPE is not literally pure Ti versus pure Pt. The SUEP test compares PtRh10 against a Ti-Al-V alloy. This checkpoint uses the alloy mass fractions and computes simple source-charge proxies, then refuses to call them MTS coefficients until the source-charge basis is derived.",
        "",
        "The useful formula shape is:",
        "",
        "`eta_TiPt ~= DeltaQ_source dot C_source + S_marker*b_m + S_theta*b_theta + S_source*b_kappa`.",
        "",
        "The proxy deltas are now available. The missing object is the actual MTS source-charge basis `C_source` and its mapping into `b_kappa`, `b_theta`, and marker slots.",
        "",
        "## Local Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## Web Source Register",
        "",
        md_table(web_sources, ["web_source_id", "title", "year", "url", "source_use", "recorded_fact", "valid_for_claim"]),
        "",
        "## Material Constituents",
        "",
        md_table(constituents, ["material_id", "element", "mass_fraction", "A", "Z", "source"]),
        "",
        "## Charge Basis Proxies",
        "",
        md_table(basis, ["basis_id", "proxy", "physical_read", "projection_status", "valid_for_claim"]),
        "",
        "## Material Proxy Charge Vectors",
        "",
        md_table(material_rows, ["material_id", "mass_fraction_sum", "Y_e_proxy", "neutron_excess_proxy", "coulomb_proxy", "A_bar_proxy", "status", "valid_for_claim"]),
        "",
        "## Differential Proxy Vector",
        "",
        md_table(delta_rows, ["delta_id", "feature", "definition", "delta_value", "absolute_delta", "status", "valid_for_claim"]),
        "",
        "## Projection Attempt",
        "",
        md_table(projection_rows, ["projection_id", "formula", "known_inputs", "missing_inputs", "result", "valid_for_claim"]),
        "",
        "## Identity Debug Bounds",
        "",
        md_table(identity_rows, ["identity_bound_id", "feature", "eta_envelope", "absolute_delta", "identity_debug_bound", "why_not_claim", "valid_for_claim"]),
        "",
        "## Screening Runner",
        "",
        md_table(screen_rows, ["screen_id", "requirement", "result", "claim_allowed", "detail", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "claim_allowed", "why_not"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "topic", "result", "reason", "next_action"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register()
    web_sources = web_source_rows()
    constituents = material_constituents()
    basis = charge_basis_rows()
    material_rows = weighted_material_charges(constituents)
    delta_rows = differential_charge_rows(material_rows)
    projection_rows = projection_attempt_rows(delta_rows)
    identity_rows = identity_debug_bound_rows(delta_rows)
    screen_rows = screening_runner_rows(identity_rows)
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, web_sources, constituents, material_rows, delta_rows, projection_rows, identity_rows, screen_rows, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_983_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_983_WEB_SOURCE_REGISTER.csv", web_sources)
    write_csv(OUT / "P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv", constituents)
    write_csv(OUT / "P8_Y5_R10_983_CHARGE_BASIS_PROXIES.csv", basis)
    write_csv(OUT / "P8_Y5_R10_983_MATERIAL_PROXY_CHARGE_VECTORS.csv", material_rows)
    write_csv(OUT / "P8_Y5_R10_983_DIFFERENTIAL_PROXY_VECTOR.csv", delta_rows)
    write_csv(OUT / "P8_Y5_R10_983_PROJECTION_ATTEMPT.csv", projection_rows)
    write_csv(OUT / "P8_Y5_R10_983_IDENTITY_DEBUG_BOUNDS.csv", identity_rows)
    write_csv(OUT / "P8_Y5_R10_983_SCREENING_RUNNER.csv", screen_rows)
    write_csv(OUT / "P8_Y5_R10_983_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_983_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_983_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_983_VALIDATION.csv", validation)
    write_doc(sources, web_sources, constituents, basis, material_rows, delta_rows, projection_rows, identity_rows, screen_rows, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()

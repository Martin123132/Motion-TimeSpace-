from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
EXT = ROOT / "source-intake" / "external_sources"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3485-Y5-R2FR-hyperfine-isotope-DD-basis-extraction-or-delta-m-kernel-exclusion.md"
CHANNELS = ["D_hatm_eff", "D_delta_m_eff", "D_me_eff", "D_e_eff"]

SOURCES: dict[str, dict[str, Any]] = {
    "script_3485": {"path": Path(__file__).resolve(), "role": "generator", "source_url": ""},
    "doc_3484": {
        "path": ROOT / "3484-Y5-R2FR-fourth-nonWEP-row-or-QEarth-kernel-exclusion-theorem.md",
        "role": "3484 handoff",
        "source_url": "",
    },
    "blind_3483": {
        "path": OUT / "P8_Y5_R2FR_3483_BLIND_DIRECTION_LEDGER.csv",
        "role": "same-vector blind direction",
        "source_url": "",
    },
    "earth_source_3482": {
        "path": OUT / "P8_Y5_R2FR_3482_EARTH_FULL_DD_SOURCE_VECTOR_NONCLAIM.csv",
        "role": "bulk Earth full-DD proxy source vector",
        "source_url": "",
    },
    "matrix_3475": {
        "path": OUT / "P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv",
        "role": "current clock and WEP matrix",
        "source_url": "",
    },
    "dinh_2009": {
        "path": EXT / "Dinh_Dunning_Dzuba_Flambaum_2009_hyperfine_radius_quark_mass_variation.pdf",
        "role": "hyperfine alpha and average-quark-mass sensitivities",
        "source_url": "https://arxiv.org/abs/0903.2090",
    },
    "berengut_2011": {
        "path": EXT / "Berengut_Flambaum_Kava_2011_isotope_comparisons_quark_mass_variation.pdf",
        "role": "isotope hyperfine quark-mass sensitivity differences",
        "source_url": "https://arxiv.org/abs/1109.1893",
    },
    "flambaum_tedesco_2006": {
        "path": EXT / "Flambaum_Tedesco_2006_nuclear_magnetic_moments_quark_masses_atomic_clocks.pdf",
        "role": "older hyperfine quark-mass sensitivity table continuity",
        "source_url": "https://arxiv.org/abs/nucl-th/0601050",
    },
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def fmt(value: float) -> str:
    if math.isinf(value):
        return "inf"
    if math.isnan(value):
        return "nan"
    return f"{value:.12e}"


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(a: list[float]) -> float:
    return math.sqrt(dot(a, a))


def normalize(a: list[float]) -> list[float]:
    length = norm(a)
    return [0.0 for _ in a] if length == 0 else [x / length for x in a]


def vector_from_matrix_row(row: dict[str, str]) -> list[float]:
    return [float(row[f"raw_{channel}"]) for channel in CHANNELS]


def blind_vector() -> list[float]:
    for row in read_csv(SOURCES["blind_3483"]["path"]):
        if row["blind_id"] == "BLIND3483_2_QEarth_plus_two_clocks":
            return normalize(
                [
                    float(row["unit_null_D_hatm_eff"]),
                    float(row["unit_null_D_delta_m_eff"]),
                    float(row["unit_null_D_me_eff"]),
                    float(row["unit_null_D_e_eff"]),
                ]
            )
    raise ValueError("3483 blind vector not found")


def base_rows() -> list[list[float]]:
    earth = read_csv(SOURCES["earth_source_3482"]["path"])[0]
    q_earth = [
        float(earth["Q_hatm_full_Earth"]),
        float(earth["Q_delta_m_Earth"]),
        float(earth["Q_m_e_Earth"]),
        float(earth["Q_e_full_Earth"]),
    ]
    matrix = read_csv(SOURCES["matrix_3475"]["path"])
    clock_rows = [vector_from_matrix_row(row) for row in matrix if row["row_type"].startswith("clock_")]
    return [q_earth] + clock_rows


def rank(rows: list[list[float]], tol: float = 1e-12) -> int:
    return int(np.linalg.matrix_rank(np.array(rows, dtype=float), tol=tol))


def singular_values(rows: list[list[float]]) -> list[float]:
    return [float(value) for value in np.linalg.svd(np.array(rows, dtype=float), compute_uv=False)]


def condition_number(rows: list[list[float]]) -> float:
    values = singular_values(rows)
    if not values or values[-1] == 0.0:
        return math.inf
    return values[0] / values[-1]


def source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_id": key,
            "path": str(meta["path"]),
            "exists": str(Path(meta["path"]).exists()),
            "role": meta["role"],
            "source_url": meta["source_url"],
            "valid_for_claim": "False",
        }
        for key, meta in SOURCES.items()
    ]


def pdf_text(path: Path) -> list[str]:
    reader = PdfReader(str(path))
    return [(page.extract_text() or "") for page in reader.pages]


def pdf_audit_rows() -> list[dict[str, Any]]:
    audits: list[dict[str, Any]] = []
    checks = [
        ("dinh_2009", ["TABLE II", "Krel", "khq", "mq", "QCD"]),
        ("berengut_2011", ["TABLE III", "isotope", "quark", "0.924"]),
        ("flambaum_tedesco_2006", ["TABLE IV", "Krel", "0.009", "mq", "QCD"]),
    ]
    for source_id, terms in checks:
        pages = pdf_text(SOURCES[source_id]["path"])
        joined = "\n".join(pages)
        normalized = " ".join(joined.split())
        found_terms = [term for term in terms if term.lower() in normalized.lower()]
        hit_pages = []
        for index, page in enumerate(pages, start=1):
            low = page.lower()
            if any(term.lower() in low for term in terms):
                hit_pages.append(str(index))
        audits.append(
            {
                "audit_id": f"PDF3485_{source_id}",
                "source_id": source_id,
                "path": str(SOURCES[source_id]["path"]),
                "page_count": len(pages),
                "terms_checked": ";".join(terms),
                "terms_found": ";".join(found_terms),
                "hit_pages": ";".join(hit_pages),
                "extraction_method": "pypdf_text_keyword_audit_manual_table_values_encoded_below",
                "valid_for_claim": "False",
            }
        )
    return audits


def basis_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "map_id": "MAP3485_0_Xq_to_D_hatm",
            "source_quantity": "X_q = m_q/Lambda_QCD",
            "dd_basis_mapping": "D_hatm_eff",
            "not_mapped_to": "D_delta_m_eff",
            "reason": "X_q is the average light-quark mass over the QCD scale; D_delta_m_eff is the isospin-breaking up/down mass-difference channel.",
            "claim_status": "SOURCE_BACKED_CONCEPTUAL_MAP_NONCLAIM_PARENT_MTS_MAP_MISSING",
            "valid_for_claim": "False",
        },
        {
            "map_id": "MAP3485_1_hyperfine_ratio",
            "source_quantity": "hyperfine ratio A/B from Dinh Table II",
            "dd_basis_mapping": "row = (Delta k_Xq, 0, 0, Delta Krel_alpha)",
            "not_mapped_to": "D_delta_m_eff; D_me_eff for same-class hyperfine ratios",
            "reason": "the table gives alpha and average-quark-mass sensitivities; same hyperfine-class ratios cancel common electron/proton mass factor at this level.",
            "claim_status": "SENSITIVITY_ROW_ONLY_NONCLAIM",
            "valid_for_claim": "False",
        },
        {
            "map_id": "MAP3485_2_isotope_ratio",
            "source_quantity": "same-element isotope hyperfine comparison",
            "dd_basis_mapping": "row = (Delta kappa_Xq, 0, 0, 0)",
            "not_mapped_to": "D_delta_m_eff",
            "reason": "electron relativistic and alpha factors cancel for same element; source discusses average quark mass sensitivity of nuclear magnetic moments.",
            "claim_status": "SENSITIVITY_ROW_ONLY_NONCLAIM",
            "valid_for_claim": "False",
        },
        {
            "map_id": "MAP3485_3_indirect_delta_closure",
            "source_quantity": "rank closure through Q_Earth",
            "dd_basis_mapping": "possible only because Q_delta_m_Earth != 0 in the bulk DD proxy",
            "not_mapped_to": "a direct hyperfine D_delta_m coefficient",
            "reason": "new D_hatm rows separate average-quark direction from the tiny Earth Q_delta_m component, but the conditioning is poor and the parent Earth source map is not signed.",
            "claim_status": "CONDITIONAL_NUMERIC_RANK_CLOSURE_NONCLAIM",
            "valid_for_claim": "False",
        },
    ]


def extracted_candidate_rows() -> list[dict[str, Any]]:
    dinh = str(SOURCES["dinh_2009"]["path"])
    berengut = str(SOURCES["berengut_2011"]["path"])
    flambaum = str(SOURCES["flambaum_tedesco_2006"]["path"])
    return [
        {
            "candidate_id": "DINH3485_0_Rb_over_Cs_hyperfine",
            "source_path": dinh,
            "source_url": SOURCES["dinh_2009"]["source_url"],
            "source_page": "paper page 4; Table II; ratio formula on paper page 2",
            "observable": "87Rb/133Cs hyperfine ratio",
            "extraction": "DeltaKrel=0.34-0.83=-0.49; Deltak=(-0.019)-0.002=-0.021",
            "D_hatm_eff": -0.021,
            "D_delta_m_eff": 0.0,
            "D_me_eff": 0.0,
            "D_e_eff": -0.49,
            "direct_delta_m_channel": "False",
            "basis_status": "AVERAGE_LIGHT_QUARK_MASS_Xq_ROW_NOT_ISOSPIN_DELTA_M",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "DINH3485_1_Yb_over_Cs_hyperfine",
            "source_path": dinh,
            "source_url": SOURCES["dinh_2009"]["source_url"],
            "source_page": "paper page 4; Table II",
            "observable": "171Yb+/133Cs hyperfine ratio",
            "extraction": "DeltaKrel=1.50-0.83=0.67; Deltak=(-0.099)-0.002=-0.101",
            "D_hatm_eff": -0.101,
            "D_delta_m_eff": 0.0,
            "D_me_eff": 0.0,
            "D_e_eff": 0.67,
            "direct_delta_m_channel": "False",
            "basis_status": "AVERAGE_LIGHT_QUARK_MASS_Xq_ROW_NOT_ISOSPIN_DELTA_M",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "DINH3485_2_Hg_over_Cs_hyperfine",
            "source_path": dinh,
            "source_url": SOURCES["dinh_2009"]["source_url"],
            "source_page": "paper page 4; Table II",
            "observable": "199Hg+/133Cs hyperfine ratio",
            "extraction": "DeltaKrel=2.28-0.83=1.45; Deltak=(-0.111)-0.002=-0.113",
            "D_hatm_eff": -0.113,
            "D_delta_m_eff": 0.0,
            "D_me_eff": 0.0,
            "D_e_eff": 1.45,
            "direct_delta_m_channel": "False",
            "basis_status": "AVERAGE_LIGHT_QUARK_MASS_Xq_ROW_NOT_ISOSPIN_DELTA_M",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "DINH3485_3_Cd_over_Cs_hyperfine",
            "source_path": dinh,
            "source_url": SOURCES["dinh_2009"]["source_url"],
            "source_page": "paper page 4; Table II",
            "observable": "111Cd+/133Cs hyperfine ratio",
            "extraction": "DeltaKrel=0.60-0.83=-0.23; Deltak=0.120-0.002=0.118",
            "D_hatm_eff": 0.118,
            "D_delta_m_eff": 0.0,
            "D_me_eff": 0.0,
            "D_e_eff": -0.23,
            "direct_delta_m_channel": "False",
            "basis_status": "AVERAGE_LIGHT_QUARK_MASS_Xq_ROW_NOT_ISOSPIN_DELTA_M",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "BFK3485_4_Yb_isotope_delta_kappa",
            "source_path": berengut,
            "source_url": SOURCES["berengut_2011"]["source_url"],
            "source_page": "paper page 6; discussion below Table IV",
            "observable": "161Yb/169Yb hyperfine isotope comparison",
            "extraction": "same-element isotope comparison sensitivity quoted as delta kappa = 0.924",
            "D_hatm_eff": 0.924,
            "D_delta_m_eff": 0.0,
            "D_me_eff": 0.0,
            "D_e_eff": 0.0,
            "direct_delta_m_channel": "False",
            "basis_status": "ISOTOPE_AVERAGE_LIGHT_QUARK_MASS_ROW_NOT_ISOSPIN_DELTA_M",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "FT3485_5_Rb_over_Cs_continuity",
            "source_path": flambaum,
            "source_url": SOURCES["flambaum_tedesco_2006"]["source_url"],
            "source_page": "paper page 8; Table IV",
            "observable": "87Rb/133Cs hyperfine ratio continuity row",
            "extraction": "DeltaKrel=0.34-0.83=-0.49; Deltakappa=(-0.016)-0.009=-0.025",
            "D_hatm_eff": -0.025,
            "D_delta_m_eff": 0.0,
            "D_me_eff": 0.0,
            "D_e_eff": -0.49,
            "direct_delta_m_channel": "False",
            "basis_status": "OLDER_CONTINUITY_Xq_ROW_NOT_ISOSPIN_DELTA_M",
            "valid_for_claim": "False",
        },
    ]


def rank_rows(candidates: list[dict[str, Any]], blind: list[float], base: list[list[float]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    base_rank = rank(base)
    base_s = singular_values(base)
    for candidate in candidates:
        vector = [float(candidate[channel]) for channel in CHANNELS]
        augmented = base + [vector]
        values = singular_values(augmented)
        new_rank = rank(augmented)
        cond = condition_number(augmented)
        rows.append(
            {
                "candidate_id": candidate["candidate_id"],
                "observable": candidate["observable"],
                "base_rank": base_rank,
                "rank_if_added": new_rank,
                "closes_rank": str(new_rank > base_rank),
                "projection_on_3483_blind": fmt(dot(normalize(vector), blind)),
                "abs_projection_on_3483_blind": fmt(abs(dot(normalize(vector), blind))),
                "min_singular_value_before": fmt(min(base_s) if base_s else math.nan),
                "min_singular_value_after": fmt(min(values) if values else math.nan),
                "condition_number_after": fmt(cond),
                "condition_flag": "ILL_CONDITIONED_PROXY_CLOSURE" if cond > 1.0e4 else "CONDITION_ACCEPTABLE_FOR_SMOKE",
                "closure_mechanism": "indirect via nonzero Q_delta_m_Earth in Earth DD proxy" if new_rank > base_rank else "does not close rank",
                "claim_status": "NONCLAIM_PARENT_EARTH_SOURCE_MAP_AND_TRANSPORT_NORMALIZATION_MISSING",
                "valid_for_claim": "False",
            }
        )
    return rows


def theorem_rows(rank_ledger: list[dict[str, Any]]) -> list[dict[str, Any]]:
    closures = [row for row in rank_ledger if row["closes_rank"] == "True"]
    best = min((float(row["condition_number_after"]) for row in closures), default=math.inf)
    return [
        {
            "theorem_id": "THM3485_0_Xq_rows_do_not_directly_probe_D_delta_m",
            "statement": "The acquired hyperfine/isotope rows constrain average light-quark sensitivity X_q, not the isospin-breaking D_delta_m_eff channel directly.",
            "proof": "Their source quantity is m_q/Lambda_QCD with m_q=(m_u+m_d)/2; no sourced coefficient for (m_d-m_u)/Lambda_QCD is present in these rows.",
            "result": "D_delta_m_eff entries are kept exactly zero for honest basis mapping.",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3485_1_indirect_kernel_closure",
            "statement": "Despite zero direct D_delta_m_eff coefficient, X_q rows can close the 3483 rank algebraically through the Earth source vector.",
            "proof": "Q_Earth has a small nonzero Q_delta_m component; adding an independent D_hatm/X_q row separates the Earth source mixture from the clock rows.",
            "result": f"closing candidates={len(closures)}; best_condition_number={fmt(best)}",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3485_2_conditioning_guard",
            "statement": "This is not yet a local-GR/source-coupling claim because the closure is condition-sensitive and depends on the parent status of Q_delta_m_Earth.",
            "proof": "The smallest singular values are controlled by the tiny Q_delta_m_Earth component in a bulk DD proxy, not a parent-derived MTS source theorem.",
            "result": "next target must stabilize/source Q_delta_m_Earth or derive a parent lower-bound/kernel-exclusion theorem.",
            "valid_for_claim": "False",
        },
    ]


def decision_rows(rank_ledger: list[dict[str, Any]]) -> list[dict[str, Any]]:
    closures = [row for row in rank_ledger if row["closes_rank"] == "True"]
    return [
        {
            "decision_id": "DEC3485_0_basis_honesty",
            "decision": "Do not relabel average quark-mass sensitivity as D_delta_m_eff.",
            "rationale": "that would be a basis error; all extracted rows have D_delta_m_eff=0.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3485_1_kernel_status",
            "decision": "The 3483 blind direction is algebraically closable, but only as a conditional proxy closure.",
            "rationale": f"{len(closures)} sourced sensitivity rows close rank, but the closure uses nonzero Q_delta_m_Earth from the nonclaim Earth DD proxy.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3485_2_best_next_attack",
            "decision": "Stabilize the closure by deriving/sourcing the Earth Q_delta_m component and its uncertainty, or prove a parent kernel-exclusion theorem.",
            "rationale": "without that, the condition number can make the apparent closure fragile.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3486-Y5-R2FR-earth-Qdelta-source-stability-or-parent-kernel-exclusion.md",
            "next_script": "scripts/Y5_R2FR_3486_earth_Qdelta_source_stability_or_parent_kernel_exclusion.py",
            "objective": "Test whether the nonzero Earth Q_delta_m component is stable/source-owned enough to support the 3485 rank closure, or derive a parent theorem excluding the D_delta_m-like kernel.",
            "success_gate": "Q_delta_m_Earth has source-backed uncertainty and parent transport status, or the parent action forbids Q_Earth dot C=0 along the 3483 blind vector",
            "forbidden_shortcuts": "claiming local GR from ill-conditioned proxy rank; relabelling X_q as D_delta_m; using WEP linearly in the same-vector branch",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(outputs: dict[str, Path], candidates: list[dict[str, Any]], rank_ledger: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append({"check_id": "VAL3485_0_sources_exist", "passed": all(Path(meta["path"]).exists() for meta in SOURCES.values()), "detail": "all local sources and PDFs exist", "valid_for_claim": "False"})
    parse_ok = True
    details = []
    for name, path in outputs.items():
        try:
            parsed = read_csv(path)
            details.append(f"{name}:{len(parsed)}")
        except Exception as exc:
            parse_ok = False
            details.append(f"{name}:ERROR:{exc}")
    rows.append({"check_id": "VAL3485_1_csv_parse", "passed": parse_ok, "detail": "; ".join(details), "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3485_2_basis_honesty", "passed": all(float(row["D_delta_m_eff"]) == 0.0 and row["direct_delta_m_channel"] == "False" for row in candidates), "detail": "all extracted Xq rows keep D_delta_m_eff=0", "valid_for_claim": "False"})
    closure_count = sum(1 for row in rank_ledger if row["closes_rank"] == "True")
    rows.append({"check_id": "VAL3485_3_algebraic_rank_closure_exists", "passed": closure_count > 0, "detail": f"closing_rows={closure_count}", "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3485_4_condition_guard_present", "passed": any(row["condition_flag"] == "ILL_CONDITIONED_PROXY_CLOSURE" for row in rank_ledger), "detail": "rank closure is condition-guarded", "valid_for_claim": "False"})
    all_rows: list[dict[str, str]] = []
    for path in outputs.values():
        all_rows.extend(read_csv(path))
    rows.append({"check_id": "VAL3485_5_no_claim", "passed": all(row.get("valid_for_claim") == "False" for row in all_rows), "detail": "all generated rows valid_for_claim=false", "valid_for_claim": "False"})
    rows.append({"check_id": "VAL3485_6_no_formalization_outputs", "passed": all(FORMALIZATION not in path.parents for path in outputs.values()), "detail": "outputs are under post-checkpoint-work/source-intake only", "valid_for_claim": "False"})
    passed = all(str(row["passed"]) == "True" for row in rows)
    rows.append({"check_id": "VAL3485_SUMMARY", "passed": passed, "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return rows


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |" for row in rows]
    return "\n".join([header, sep] + body)


def write_doc(
    candidates: list[dict[str, Any]],
    basis_map: list[dict[str, Any]],
    rank_ledger: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3485: Hyperfine/Isotope DD-Basis Extraction Or Delta-m Kernel Exclusion",
                "",
                "## Current Verdict",
                "- **Good news:** sourced hyperfine/isotope sensitivity rows can algebraically close the 3483 one-dimensional blind direction.",
                "- **Important honesty guard:** these rows are average light-quark `X_q=m_q/Lambda_QCD` rows, not direct `D_delta_m_eff` rows.",
                "- **Mechanism:** closure happens indirectly because the Earth DD source proxy has a small nonzero `Q_delta_m_Earth` component.",
                "- **Risk:** the closure is ill-conditioned and remains nonclaim until `Q_delta_m_Earth` is parent-owned or a kernel-exclusion theorem is derived.",
                "- **No claim:** no local-GR, WEP, Newton, source-coupling, or EM pass is claimed here.",
                "",
                "## Basis Map Audit",
                md_table(basis_map, ["map_id", "source_quantity", "dd_basis_mapping", "not_mapped_to", "reason", "claim_status", "valid_for_claim"]),
                "",
                "## Extracted Sensitivity Rows",
                md_table(candidates, ["candidate_id", "observable", "extraction", "D_hatm_eff", "D_delta_m_eff", "D_me_eff", "D_e_eff", "basis_status", "valid_for_claim"]),
                "",
                "## Rank And Conditioning Ledger",
                md_table(rank_ledger, ["candidate_id", "rank_if_added", "closes_rank", "projection_on_3483_blind", "min_singular_value_after", "condition_number_after", "condition_flag", "closure_mechanism", "valid_for_claim"]),
                "",
                "## Theorems",
                md_table(theorem, ["theorem_id", "statement", "proof", "result", "valid_for_claim"]),
                "",
                "## Decisions",
                md_table(decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "passed", "detail", "valid_for_claim"]),
                "",
                f"_Generated: {now()}_",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    blind = blind_vector()
    base = base_rows()
    candidates = extracted_candidate_rows()
    basis_map = basis_map_rows()
    pdf_audits = pdf_audit_rows()
    rank_ledger = rank_rows(candidates, blind, base)
    theorem = theorem_rows(rank_ledger)
    decisions = decision_rows(rank_ledger)
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3485_SOURCE_REGISTER.csv",
        "pdf_audit": OUT / "P8_Y5_R2FR_3485_PDF_TEXT_AUDIT.csv",
        "basis_map": OUT / "P8_Y5_R2FR_3485_DD_BASIS_MAP_AUDIT.csv",
        "extracted_rows": OUT / "P8_Y5_R2FR_3485_EXTRACTED_HYPERFINE_ROWS_NONCLAIM.csv",
        "rank_ledger": OUT / "P8_Y5_R2FR_3485_RANK_AND_CONDITION_LEDGER.csv",
        "theorems": OUT / "P8_Y5_R2FR_3485_THEOREM_LEDGER.csv",
        "decisions": OUT / "P8_Y5_R2FR_3485_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3485_NEXT_TARGET.csv",
    }
    write_csv(outputs["source_register"], source_register(), ["source_id", "path", "exists", "role", "source_url", "valid_for_claim"])
    write_csv(outputs["pdf_audit"], pdf_audits, ["audit_id", "source_id", "path", "page_count", "terms_checked", "terms_found", "hit_pages", "extraction_method", "valid_for_claim"])
    write_csv(outputs["basis_map"], basis_map, ["map_id", "source_quantity", "dd_basis_mapping", "not_mapped_to", "reason", "claim_status", "valid_for_claim"])
    write_csv(outputs["extracted_rows"], candidates, ["candidate_id", "source_path", "source_url", "source_page", "observable", "extraction", "D_hatm_eff", "D_delta_m_eff", "D_me_eff", "D_e_eff", "direct_delta_m_channel", "basis_status", "valid_for_claim"])
    write_csv(outputs["rank_ledger"], rank_ledger, ["candidate_id", "observable", "base_rank", "rank_if_added", "closes_rank", "projection_on_3483_blind", "abs_projection_on_3483_blind", "min_singular_value_before", "min_singular_value_after", "condition_number_after", "condition_flag", "closure_mechanism", "claim_status", "valid_for_claim"])
    write_csv(outputs["theorems"], theorem, ["theorem_id", "statement", "proof", "result", "valid_for_claim"])
    write_csv(outputs["decisions"], decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"])
    validation = validation_rows(outputs, candidates, rank_ledger)
    validation_path = OUT / "P8_Y5_BRR545_3485_VALIDATION.csv"
    write_csv(validation_path, validation, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(candidates, basis_map, rank_ledger, theorem, decisions, next_rows, validation)


if __name__ == "__main__":
    main()

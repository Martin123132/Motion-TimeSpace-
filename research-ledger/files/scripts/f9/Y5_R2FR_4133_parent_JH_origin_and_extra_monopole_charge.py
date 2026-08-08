from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4133-Y5-R2FR-parent-JH-origin-and-extra-monopole-charge.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_PARENT_JH_ORIGIN_AND_EXTRA_MONOPOLE_CHARGE_4133"
CHECKPOINT_ID = "4133"
DECISION = "PARENT_JH_ORIGIN_UNSIGNED_QEXTRA_VECTOR_FILLED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4133_00_4132_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4132_NEXT_TARGET.csv",
        "4133-Y5-R2FR-parent-JH-origin-and-extra-monopole-charge.md",
        "4132 selected parent JH origin and extra-monopole charge.",
    ),
    "SRC4133_01_4132_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4132_STATUS.csv",
        "DENOMINATOR_EQUALITY_REDUCED_TO_RANK_ONE_AMPLITUDE_VECTOR_PARENT_ZERO_UNSIGNED",
        "Current source-denominator status.",
    ),
    "SRC4133_02_4132_rank_one": (
        SOURCE_DIR / "P8_Y5_R2FR_4132_RANK_ONE_REDUCTION.csv",
        "Q_proj = lambda_PiM_EH Q_EH + Q_extra",
        "Rank-one charge reduction to lambda_PiM_EH and Q_extra.",
    ),
    "SRC4133_03_3987_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3987_UNIVERSAL_COUPLING_AND_EXTRA_MONOPOLE_THEOREM.csv",
        "epsilon_extra_monopole_total",
        "Universal coupling and extra-monopole master residual.",
    ),
    "SRC4133_04_3987_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3987_COUPLING_EXTRA_MONOPOLE_BOUND_ROWS.csv",
        "epsilon_extra_monopole_total",
        "Coupling and extra-monopole bound rows.",
    ),
    "SRC4133_05_3970_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3970_NO_EXTRA_MONOPOLE_THEOREM_OR_BOUND.csv",
        "forall i, epsilon_i=0",
        "No-extra-monopole conditional theorem.",
    ),
    "SRC4133_06_3970_channels": (
        SOURCE_DIR / "P8_Y5_R2FR_3970_EXTRA_MONOPOLE_CHANNEL_VECTOR.csv",
        "epsilon_boundary",
        "Extra-monopole channel vector.",
    ),
    "SRC4133_07_3984_certificate": (
        SOURCE_DIR / "P8_Y5_R2FR_3984_CLOSED_SOURCE_OWNERSHIP_CERTIFICATE.csv",
        "CWO3984_1_parent_JH",
        "Closed source ownership certificate.",
    ),
    "SRC4133_08_3985_update": (
        SOURCE_DIR / "P8_Y5_R2FR_3985_CLOSED_SOURCE_CERTIFICATE_UPDATE.csv",
        "STILL_OPEN_PARENT_MATTER_ACTION_NEEDED",
        "Certificate update leaves parent JH open.",
    ),
    "SRC4133_09_3776_inclusion": (
        SOURCE_DIR / "P8_Y5_R2FR_3776_TOTAL_HILBERT_SOURCE_INCLUSION_THEOREM.csv",
        "THI3776_2_EM_Ward_internal_exchange",
        "Total Hilbert source inclusion and Poynting bookkeeping.",
    ),
    "SRC4133_10_3776_reclass": (
        SOURCE_DIR / "P8_Y5_R2FR_3776_MUEXTRA_RECLASSIFICATION_VECTOR.csv",
        "MRV3776_0_EM_Poynting",
        "EM/Poynting reclassification vector.",
    ),
    "SRC4133_11_3999_flux": (
        SOURCE_DIR / "P8_Y5_R2FR_3999_FLUX_CLOSURE_THEOREM.csv",
        "FCT3999_3_flux_closure_theorem",
        "Hilbert mass flux closure theorem.",
    ),
    "SRC4133_12_3999_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3999_MH_FLUX_BOUND_VECTOR.csv",
        "Delta_rad_Poynting",
        "Hilbert mass flux bound vector.",
    ),
    "SRC4133_13_4100_nonhilbert": (
        SOURCE_DIR / "P8_Y5_R2FR_4100_NONHILBERT_BYPASS_THEOREM.csv",
        "NHB4100_2_total_zero_conditions",
        "Non-Hilbert bypass decomposition and zero conditions.",
    ),
    "SRC4133_14_4102_leakage": (
        SOURCE_DIR / "P8_Y5_R2FR_4102_LIVE_LEAKAGE_LEDGER.csv",
        "LEAK4102_2_Poynting_radiation",
        "Live local leakage ledger.",
    ),
    "SRC4133_15_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4133_parent_JH_origin_and_extra_monopole_charge.py",
        "Reproducible generator for this 4133 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def parent_origin_rows() -> List[dict]:
    data = [
        (
            "PO4133_0_parent_action",
            "parent_JH_origin",
            "J_H_total[tau] must be obtained from one parent source action by Hilbert/coframe variation before any phenomenological readout",
            "S_src[q(Phi),Psi,theta] = S_matter + S_EM + S_binding + S_apparatus + S_int",
            "UNSIGNED_PARENT_MATTER_ACTION_NEEDED",
        ),
        (
            "PO4133_1_total_stress",
            "matter+EM+Poynting",
            "the same Hilbert/coframe variation must include matter, EM stress, Poynting momentum, binding, apparatus, and interaction energy once",
            "T_H_total = (2/sqrt(-g_eff)) delta S_src / delta g_eff",
            "CONDITIONAL_TOTAL_STRESS_IMPORTED_NOT_PARENT_SIGNED",
        ),
        (
            "PO4133_2_domain_support",
            "total-system source domain",
            "the source domain must include field support and binding tails so exterior EM/Poynting energy is not double-counted as Q_extra",
            "domain(Pi_M J_H_total) = material body plus included public field/support tube",
            "DOMAIN_OWNER_UNSIGNED",
        ),
        (
            "PO4133_3_projector_owner",
            "Pi_M parent ownership",
            "Pi_M must be source-blind and commute with exterior transport; otherwise lambda_PiM_EH and Q_extra are fitted projector freedoms",
            "d(Pi_M J_H) = Pi_M dJ_H + (D Pi_M) wedge J_H + [d,Pi_M]_ref J_H",
            "PROJECTOR_COMMUTATOR_UNSIGNED",
        ),
        (
            "PO4133_4_nonhilbert_silence",
            "NO_NONHILBERT_BYPASS",
            "all source-current support outside the Hilbert/coframe variation must vanish or stay as a live residual",
            "P_source[J_NH] = 0 only if spin/torsion, boundary/worldtube, readout, shadow/projector, improvement, and decoupled blocks vanish",
            "NONHILBERT_BYPASS_UNSIGNED",
        ),
        (
            "PO4133_5_boundary_silence",
            "boundary/reference silence",
            "fixed reference, worldtube boundary, and linking surfaces must add no independent source charge",
            "Delta_boundary = M_ref^-1 |N_G int_A dB_ref|",
            "BOUNDARY_LEAKAGE_UNSIGNED",
        ),
        (
            "PO4133_6_current_crossing",
            "closed source worldtube",
            "no material, EM wave, Poynting, or public-current flux may cross the linking annulus unless it is retained as source leakage",
            "Delta_rad_Poynting + Delta_source_crossing = 0 or bounded",
            "RADIATIVE_CROSSING_UNSIGNED",
        ),
        (
            "PO4133_7_zero_certificate",
            "parent_JH_origin=true gate",
            "parent_JH_origin can only be promoted when rows PO4133_0 through PO4133_6 are signed by the parent action",
            "Z_parent_JH = Z_source_action Z_total_stress Z_domain Z_PiM Z_NH Z_boundary Z_crossing",
            "ZERO_CERTIFICATE_NOT_SIGNED",
        ),
    ]
    rows: List[dict] = []
    for origin_id, gate, requirement, formula, status in data:
        row = row_base()
        row.update(
            {
                "origin_id": origin_id,
                "gate": gate,
                "requirement": requirement,
                "formula": formula,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def qextra_rows() -> List[dict]:
    data = [
        (
            "QX4133_0_nonEH",
            "Q_nonEH",
            "non-EH/memory/range/direct active source support not contained in the EH Hilbert mass current",
            "prove no independent non-EH monopole or bound its exterior charge",
            "epsilon_nonEH",
        ),
        (
            "QX4133_1_symplectic",
            "Q_symp",
            "Hamiltonian/symplectic improvement or integrability residue that survives the surface charge",
            "prove exact improvement cancellation under fixed bundle/tau/surface clauses",
            "epsilon_symp",
        ),
        (
            "QX4133_2_PiM_stress",
            "Q_PiM_stress",
            "metric/source dependence of Pi_M producing active stress through the projector itself",
            "prove source-blind covariantly constant Pi_M or bound projector-stress response",
            "epsilon_PiM_stress",
        ),
        (
            "QX4133_3_domain",
            "Q_domain",
            "field-support or binding energy omitted by a matter-only domain",
            "use total-system domain or retain omitted support charge",
            "epsilon_domain",
        ),
        (
            "QX4133_4_memory",
            "Q_memory",
            "history/memory sector contributing a stationary monopole in the local exterior",
            "prove memory is pure gauge/constant or source its monopole bound",
            "epsilon_memory",
        ),
        (
            "QX4133_5_range",
            "Q_range",
            "finite-range/direct-force tail masquerading as a Newtonian source amplitude",
            "prove infinite-range EH-only local branch or source R10/PPN/radial-hair bound",
            "epsilon_range",
        ),
        (
            "QX4133_6_delta_kappa",
            "Q_delta_kappa",
            "source/species/range dependence in kappa_eff or common-G product normalization",
            "derive kappa as global/source-blind integration constant or bound D_X ln kappa_eff",
            "delta_kappa_source",
        ),
        (
            "QX4133_7_frame",
            "Q_frame",
            "frame/species/readout dependence in the observed generator or matter-source normalization",
            "prove same tau/coframe/source frame or bound WEP/clock/PPN transfer",
            "epsilon_frame_species",
        ),
        (
            "QX4133_8_boundary_leak",
            "Q_boundary_leak",
            "boundary, corner, worldtube, or reference surface charge not included in J_H_total",
            "prove boundary reference compatibility or source the flux/corner bound",
            "epsilon_boundary_leakage",
        ),
        (
            "QX4133_9_radiative",
            "Q_radiative_Poynting",
            "net radiative EM/gravitational/Poynting flux crossing the linking annulus",
            "prove stationary no-flux branch or retain Delta_rad_Poynting",
            "epsilon_radiative_Poynting",
        ),
    ]
    rows: List[dict] = []
    for channel_id, symbol, definition, zero_route, score_term in data:
        row = row_base()
        row.update(
            {
                "channel_id": channel_id,
                "symbol": symbol,
                "definition": definition,
                "zero_route": zero_route,
                "bound_input_required": f"{score_term}; units; source_path; arena_projection; tolerance",
                "status": "LIVE_ZERO_OR_BOUND_REQUIRED",
                "score_term": score_term,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def bound_schema_rows() -> List[dict]:
    data = [
        (
            "BS4133_0_lambda",
            "lambda_PiM_EH",
            "abs(lambda_PiM_EH - 1)",
            "dimensionless",
            "Newton/PPN/common-G amplitude",
            "source-blind Pi_M normalization equals EH mass charge",
        ),
        (
            "BS4133_1_qextra",
            "Q_extra_over_Q_ref",
            "sum_abs(Q_nonEH,Q_symp,Q_PiM_stress,Q_domain,Q_memory,Q_range,Q_delta_kappa,Q_frame,Q_boundary_leak,Q_radiative_Poynting)/abs(Q_ref)",
            "dimensionless",
            "Newton/Gauss/R10/PPN/Gdot",
            "all non-EH and non-Hilbert monopole channels vanish or are bounded",
        ),
        (
            "BS4133_2_parent",
            "epsilon_parent_JH_origin",
            "1 - Z_parent_JH",
            "boolean or dimensionless residual",
            "source-current ownership",
            "single parent Hilbert/coframe variation owns matter+EM+Poynting source current",
        ),
        (
            "BS4133_3_boundary",
            "epsilon_boundary_leakage",
            "abs(Q_boundary_leak)/abs(Q_ref)",
            "dimensionless",
            "boundary/worldtube/reference",
            "fixed boundary/reference action adds no independent source charge",
        ),
        (
            "BS4133_4_common_G",
            "epsilon_universal_G",
            "abs(D_X ln G_eff) + abs(delta_kappa_source) + abs(epsilon_Gref_match)",
            "dimensionless or per arena derivative",
            "Gdot/WEP/PPN/common-G",
            "absolute G is calibrated but source/range/time/species derivatives must vanish",
        ),
        (
            "BS4133_5_PPN",
            "epsilon_PPN_source_stability",
            "abs(source charge drift between Newtonian and beta/gamma/preferred-frame order)",
            "dimensionless",
            "PPN beta gamma alpha_i xi",
            "same M_H source survives higher-order local expansion",
        ),
        (
            "BS4133_6_master",
            "epsilon_denominator_4133",
            "abs(lambda_PiM_EH-1)+abs(Q_extra_over_Q_ref)+epsilon_parent_JH_origin+epsilon_boundary_leakage+epsilon_universal_G+epsilon_PPN_source_stability",
            "dimensionless",
            "local GR/Newton source denominator",
            "master denominator residual after parent-JH/Qextra split",
        ),
    ]
    rows: List[dict] = []
    for bound_id, target, formula, units, arena, source_needed in data:
        row = row_base()
        row.update(
            {
                "bound_id": bound_id,
                "target": target,
                "formula": formula,
                "units": units,
                "arena": arena,
                "source_needed": source_needed,
                "status": "NONCLAIM_BOUND_SCHEMA_READY",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DG4133_0_attempted_zero_proof",
            "PARENT_JH_ORIGIN_UNSIGNED",
            "The controlled branch has a clear proof contract, but the parent source action has not signed the total Hilbert/coframe source variation.",
            "do not claim parent_JH_origin=true",
        ),
        (
            "DG4133_1_qextra",
            "QEXTRA_VECTOR_FILLED",
            "Q_extra is now decomposed into explicit live monopole channels rather than left as one vague missing term.",
            "attack channel zeros or source numeric bounds one by one",
        ),
        (
            "DG4133_2_poynting",
            "POYNTING_INCLUDED_NOT_DROPPED",
            "Stationary EM/Poynting stress belongs inside J_H_total if descended; radiative crossing remains a separate live leakage term.",
            "do not double-count EM/Poynting as both Hilbert source and extra source",
        ),
        (
            "DG4133_3_claim_ceiling",
            "NO_LOCAL_GR_CLAIM",
            "lambda_PiM_EH=1, Q_extra=0, parent_JH_origin=true, boundary silence, universal G, and PPN source stability remain unsigned.",
            "no local GR/Newton/PPN/R10/Gdot claim",
        ),
        (
            "DG4133_4_next",
            "NEXT_QEXTRA_CHANNEL_ZERO_SELECTED",
            "The next shortest route is to try to kill or bound the Q_extra channels, starting with non-Hilbert/boundary/Poynting leakage because they feed multiple arenas.",
            "4134-Y5-R2FR-Qextra-channel-zero-or-bound.md",
        ),
    ]
    rows: List[dict] = []
    for gate_id, decision, rationale, next_action in data:
        row = row_base()
        row.update(
            {
                "gate_id": gate_id,
                "decision": decision,
                "rationale": rationale,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4133_0",
            "result": DECISION,
            "summary": (
                "4133 attempts the parent-origin/no-extra-monopole proof. It does not close it: the total "
                "Hilbert/coframe source action, source-blind Pi_M, non-Hilbert bypass silence, boundary/reference "
                "silence, and Poynting/radiative crossing clauses are still unsigned. The gain is real though: "
                "Q_extra is now a finite channel vector with nonclaim bound schemas instead of one amorphous gap."
            ),
            "parent_JH_origin_signed": "False",
            "Q_extra_zero_signed": "False",
            "qextra_vector_filled": "True",
            "bound_schemas_filled": "True",
            "score_ready": "False",
            "claim_state": "no local_GR, Newton, PPN, R10, Gdot, clock, EM prediction, Maxwell derivation, alpha derivation, or source-normalization pass",
            "next_target": "4134 Qextra channel zero or bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4133_0",
            "target_doc": "4134-Y5-R2FR-Qextra-channel-zero-or-bound.md",
            "target_script": "scripts/Y5_R2FR_4134_Qextra_channel_zero_or_bound.py",
            "objective": (
                "try to prove channelwise Q_extra=0 from non-Hilbert silence, boundary/reference closure, "
                "total-system source domain, stationary Poynting no-flux, and source-blind Pi_M; if any clause "
                "fails, produce arena-ready numeric/source rows for Q_extra_over_Q_ref"
            ),
            "success_gate": "Q_extra=0 signed channelwise, or every live channel has nonclaim bound rows with units, source paths, arena projections, and tolerances",
            "reason": "4133 reduced parent source denominator failure to a finite extra-monopole channel vector; the next move should try to close or source those channels directly.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4133_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4133_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4133_PARENT_JH_ORIGIN_GATE": SOURCE_DIR / "P8_Y5_R2FR_4133_PARENT_JH_ORIGIN_GATE.csv",
        "P8_Y5_R2FR_4133_QEXTRA_CHANNEL_VECTOR": SOURCE_DIR / "P8_Y5_R2FR_4133_QEXTRA_CHANNEL_VECTOR.csv",
        "P8_Y5_R2FR_4133_BOUND_SCHEMAS": SOURCE_DIR / "P8_Y5_R2FR_4133_BOUND_SCHEMAS.csv",
        "P8_Y5_R2FR_4133_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4133_DECISION_GATES.csv",
        "P8_Y5_R2FR_4133_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4133_STATUS.csv",
        "P8_Y5_R2FR_4133_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4133_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    status = status_rows()[0]
    sections = [
        "# 4133 - Parent JH Origin and Extra-Monopole Charge",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- The zero proof was attempted but not signed by the present parent action.",
        "- The useful move is that `Q_extra` is no longer a fog bank: it is now a finite channel vector.",
        "- No Newton/local-GR/PPN/R10 pass is claimed.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Parent-Origin Contract", "", "| gate | status | requirement |", "|---|---|---|"])
    for row in parent_origin_rows():
        sections.append(f"| {row['gate']} | {row['status']} | {row['requirement']} |")
    sections.extend(["", "## Qextra Channel Vector", "", "| symbol | status | zero route |", "|---|---|---|"])
    for row in qextra_rows():
        sections.append(f"| {row['symbol']} | {row['status']} | {row['zero_route']} |")
    sections.extend(["", "## Bound Schemas", "", "| target | units | arena |", "|---|---|---|"])
    for row in bound_schema_rows():
        sections.append(f"| {row['target']} | {row['units']} | {row['arena']} |")
    sections.extend(
        [
            "",
            "## Claim Ceiling",
            "",
            f"- {status['claim_state']}.",
            "- This checkpoint narrows the source-denominator problem; it does not close local GR.",
            "",
            "## Next Target",
            "",
            "- `4134-Y5-R2FR-Qextra-channel-zero-or-bound.md`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4133_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4133_PARENT_JH_ORIGIN_GATE": parent_origin_rows,
        "P8_Y5_R2FR_4133_QEXTRA_CHANNEL_VECTOR": qextra_rows,
        "P8_Y5_R2FR_4133_BOUND_SCHEMAS": bound_schema_rows,
        "P8_Y5_R2FR_4133_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4133_STATUS": status_rows,
        "P8_Y5_R2FR_4133_NEXT_TARGET": next_target_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4133_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add(
        "VAL4133_1_doc",
        "checkpoint markdown exists and names decision",
        DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"),
        str(DOC_PATH),
    )

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4133_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    origin_text = flatten_rows([outputs["P8_Y5_R2FR_4133_PARENT_JH_ORIGIN_GATE"]])
    origin_ok = all(
        token in origin_text
        for token in ["parent_JH_origin", "Hilbert/coframe variation", "matter+EM+Poynting", "NO_NONHILBERT_BYPASS"]
    )
    add("VAL4133_3_parent_origin", "parent-origin gate contains source action, total stress, Poynting and bypass clauses", origin_ok, "origin tokens checked")

    qextra_text = flatten_rows([outputs["P8_Y5_R2FR_4133_QEXTRA_CHANNEL_VECTOR"]])
    qextra_ok = all(
        token in qextra_text
        for token in [
            "Q_nonEH",
            "Q_symp",
            "Q_PiM_stress",
            "Q_domain",
            "Q_memory",
            "Q_range",
            "Q_delta_kappa",
            "Q_frame",
            "Q_boundary_leak",
            "Q_radiative_Poynting",
        ]
    )
    add("VAL4133_4_qextra_channels", "Qextra channel vector includes all live denominator channels", qextra_ok, "Qextra tokens checked")

    bound_text = flatten_rows([outputs["P8_Y5_R2FR_4133_BOUND_SCHEMAS"]])
    bound_ok = all(
        token in bound_text
        for token in [
            "lambda_PiM_EH",
            "Q_extra_over_Q_ref",
            "epsilon_parent_JH_origin",
            "epsilon_boundary_leakage",
            "epsilon_universal_G",
            "epsilon_PPN_source_stability",
            "epsilon_denominator_4133",
        ]
    )
    add("VAL4133_5_bounds", "bound schemas cover lambda, Qextra, parent origin, boundary, common-G, PPN and master denominator", bound_ok, "bound tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4133_DECISION_GATES"]])
    decision_ok = all(
        token in decision_text
        for token in ["PARENT_JH_ORIGIN_UNSIGNED", "QEXTRA_VECTOR_FILLED", "POYNTING_INCLUDED_NOT_DROPPED", "NO_LOCAL_GR_CLAIM", "NEXT_QEXTRA_CHANNEL_ZERO_SELECTED"]
    )
    add("VAL4133_6_decisions", "decision gates record attempted zero proof, Qextra vector, Poynting rule, no-claim and next target", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4133_STATUS"])
    status_ok = (
        bool(status)
        and status[0].get("result") == DECISION
        and status[0].get("parent_JH_origin_signed") == "False"
        and status[0].get("Q_extra_zero_signed") == "False"
        and status[0].get("qextra_vector_filled") == "True"
    )
    add("VAL4133_7_status", "status records unsigned origin/zero and filled Qextra vector", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4133_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4134-Y5-R2FR-Qextra-channel-zero-or-bound.md"
    add("VAL4133_8_next_target", "next target is Qextra channel zero or bound", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4133_9_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4133*")) or any(FORMALIZATION.rglob("4133-Y5-R2FR*"))
    add(
        "VAL4133_10_scope",
        "outputs stay in post-checkpoint-work and not formalization-workbench",
        in_scope and not formalization_output and not formalization_touched,
        f"doc={DOC_PATH}; csv_count={len(outputs)}",
    )

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4133_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4133_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()

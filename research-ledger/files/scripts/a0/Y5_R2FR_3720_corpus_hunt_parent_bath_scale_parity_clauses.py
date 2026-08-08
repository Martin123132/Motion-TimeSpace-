from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3720"
BRANCH_ID = "MTS_R2FR_Y5_CORPUS_HUNT_PARENT_BATH_SCALE_PARITY_CLAUSES_3720"
DOC = ROOT / "3720-Y5-R2FR-corpus-hunt-parent-bath-scale-parity-clauses.md"

DOC_3719 = ROOT / "3719-Y5-R2FR-parent-bath-normalization-and-z-parity-proof.md"
NEXT_3719 = RESIDUALS / "P8_Y5_R2FR_3719_NEXT_TARGET.csv"
FISHER_3708 = RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv"
FILL_3709 = RESIDUALS / "P8_Y5_R2FR_3709_PARENT_FILL_ROWS.csv"
GAMMA_ACTION_516 = RESIDUALS / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv"
DOUBLET_VARIATION_517 = RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv"
DOUBLET_CONTRACT_516 = RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"
ODD_CONTRACT = RESIDUALS / "P8_ODD_RESIDUAL_EXCHANGE_CONTRACT.csv"
ODD_THEOREM = RESIDUALS / "P8_ODD_RESIDUAL_EXCHANGE_THEOREM.csv"
HAMILTONIAN_SOURCE_MEASURE = RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv"
SOURCE_MEASURE_ATTEMPT = RESIDUALS / "P8_Y5_SOURCE_MEASURE_THEOREM_ATTEMPT.csv"
DOC_1010 = ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md"
DOC_1011 = ROOT / "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md"
DOC_1016 = ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"


@dataclass(frozen=True)
class Requirement:
    req_id: str
    required_clause: str
    why_needed: str
    search_terms: tuple[str, ...]


REQUIREMENTS = (
    Requirement("REQ3720_0_parent_bath_action", "parent bath action/free energy A_B(q,z,xi)", "owns the Gibbs family rather than importing a closure potential", ("A_B", "Gamma_eff", "action_density", "parent action", "free energy")),
    Requirement("REQ3720_1_bath_family", "bath distribution p_z over unresolved variables", "supplies the Fisher/KL curvature object", ("p_z", "D_KL", "Fisher", "bath family", "relative-entropy")),
    Requirement("REQ3720_2_measure_normalization", "bath measure mu_H and partition normalization", "fixes units and prevents arbitrary rescaling of I_H", ("mu_H", "dmu", "measure", "normalization", "partition")),
    Requirement("REQ3720_3_scale_theta", "positive scale Theta_H/T_eff with units", "turns dimensionless KL curvature into local operator units", ("Theta_H", "T_eff", "scale", "units", "Xi_H")),
    Requirement("REQ3720_4_parity_involution", "fibre/reflection parity z -> -z or exchange involution", "derives F_1=0 and B_QK=0 over a q-patch", ("z -> -z", "exchange", "involution", "parity", "even", "odd")),
    Requirement("REQ3720_5_identifiability", "positive Fisher floor iota_H", "keeps the local fibre direction massive rather than flat", ("iota_H", "lambda_min", "positive", "identifiability", "Hessian")),
    Requirement("REQ3720_6_boundary_silence", "boundary/source terms even, zero, or bounded", "stops parity/Fisher core from being spoiled by source or boundary work", ("boundary", "source current", "B_Z", "B_boundary", "no-flux")),
    Requirement("REQ3720_7_unit_map", "same-basis unit map U_H to m^-2 local operator", "allows Xi_H to be used in R10/PPN/clock/orbit residuals", ("U_H", "unit map", "same-basis", "m^-2", "operator units")),
)


KEY_SOURCES = (
    ("doc_3719", DOC_3719, "normalized parent Gibbs bath", "mechanism target"),
    ("next_3719", NEXT_3719, "parent action, bath measure, Theta_H scale", "handoff target"),
    ("fisher_3708", FISHER_3708, "p_z(xi|X_B,q)=p_0", "Fisher/bath gap ancestor"),
    ("fill_3709", FILL_3709, "Theta_H*iota_H - R_loss", "symbolic parent fill ancestor"),
    ("gamma_action_516", GAMMA_ACTION_516, "GO516_A_response_doublet_quadratic_density", "candidate even action density"),
    ("doublet_variation_517", DOUBLET_VARIATION_517, "AV517_1_scalar_density", "response-doublet variation"),
    ("doublet_contract_516", DOUBLET_CONTRACT_516, "RD516_1_even_scalar_density", "response-doublet contract"),
    ("odd_contract", ODD_CONTRACT, "O1_exchange_exactness", "exchange symmetry clauses"),
    ("odd_theorem", ODD_THEOREM, "E3_even_action", "odd residual theorem attempt"),
    ("hamiltonian_source_measure", HAMILTONIAN_SOURCE_MEASURE, "HSM541_2_observed_worldtube_source", "source-measure ancestor"),
    ("source_measure_attempt", SOURCE_MEASURE_ATTEMPT, "SMT542_2_observed_worldtube_source", "source-measure theorem attempt"),
    ("doc_1010", DOC_1010, "GKC1010_1_response_doublet_even_density", "q_loc action existence ancestor"),
    ("doc_1011", DOC_1011, "source-current/boundary zero theorem", "response-doublet obstruction ancestor"),
    ("doc_1016", DOC_1016, "parent worldtube/source-measure selector", "source-measure selector ancestor"),
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(stamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": stamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def line_hits(path: Path, terms: tuple[str, ...], limit: int = 3) -> list[tuple[int, str, str]]:
    if not path.exists() or path.suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf", ".docx", ".zip", ".pyc"}:
        return []
    hits: list[tuple[int, str, str]] = []
    lower_terms = tuple(term.lower() for term in terms)
    try:
        lines = read_text(path).splitlines()
    except OSError:
        return []
    for line_number, line in enumerate(lines, 1):
        lower_line = line.lower()
        for term, lower_term in zip(terms, lower_terms):
            if lower_term in lower_line:
                hits.append((line_number, term, line.strip()[:360]))
                break
        if len(hits) >= limit:
            break
    return hits


def corpus_files() -> list[Path]:
    allowed = {".md", ".csv", ".txt"}
    priority_files = {
        FISHER_3708,
        FILL_3709,
        GAMMA_ACTION_516,
        DOUBLET_VARIATION_517,
        DOUBLET_CONTRACT_516,
        ODD_CONTRACT,
        ODD_THEOREM,
        HAMILTONIAN_SOURCE_MEASURE,
        SOURCE_MEASURE_ATTEMPT,
        DOC_1010,
        DOC_1011,
        DOC_1016,
    }
    priority_name_tokens = (
        "FISHER",
        "GAMMA_OWNER",
        "RESPONSE_DOUBLET",
        "ODD_RESIDUAL",
        "SOURCE_MEASURE",
        "HAMILTONIAN_SOURCE",
        "parent-current-chain",
        "Gamma-Khat-action",
        "response-doublet",
        "source-measure",
    )
    blocked_fragments = (
        "\\scripts\\",
        "__pycache__",
        "P8_Y5_R2FR_3718_",
        "P8_Y5_R2FR_3719_",
        "P8_Y5_R2FR_3720_",
        "3718-Y5-R2FR",
        "3719-Y5-R2FR",
        "3720-Y5-R2FR",
    )
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in allowed:
            continue
        path_text = str(path)
        if any(fragment in path_text for fragment in blocked_fragments):
            continue
        if path not in priority_files and not any(token in path.name for token in priority_name_tokens):
            continue
        try:
            if path.stat().st_size > 750_000:
                continue
        except OSError:
            continue
        files.append(path)
    for path in priority_files:
        if path.exists() and path not in files:
            files.append(path)
    return sorted(files, key=lambda item: str(item).lower())


def source_register(stamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in KEY_SOURCES:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(stamp),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "role": role,
        })
    return rows


def automated_hit_rows(stamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    files = corpus_files()
    for requirement in REQUIREMENTS:
        scored: list[tuple[int, Path, list[tuple[int, str, str]]]] = []
        for path in files:
            hits = line_hits(path, requirement.search_terms, limit=3)
            if not hits:
                continue
            score = len(hits)
            if path in [source_path for _, source_path, _, _ in KEY_SOURCES]:
                score += 4
            scored.append((score, path, hits))
        scored.sort(key=lambda item: (-item[0], str(item[1]).lower()))
        for rank, (score, path, hits) in enumerate(scored[:8], 1):
            rows.append({
                **base(stamp),
                "req_id": requirement.req_id,
                "rank": rank,
                "score": score,
                "path": str(path),
                "line_refs": ";".join(str(hit[0]) for hit in hits),
                "matched_terms": ";".join(hit[1] for hit in hits),
                "snippets": " || ".join(hit[2] for hit in hits),
                "claim_allowed": False,
            })
    return rows


def adjudication_rows(stamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "ADJ3720_0_parent_bath_action",
            "parent bath action/free energy A_B(q,z,xi)",
            "PARTIAL_NOT_SIGNED",
            "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv supplies an even Gamma_eff/action-density candidate, but not a full Gibbs bath action A_B(q,z,xi) with xi, measure, and Theta_H.",
            "map response-doublet Gamma_eff to A_B or keep it as a separate local action branch",
        ),
        (
            "ADJ3720_1_bath_family",
            "p_z bath distribution",
            "PARTIAL_SUPPORTED",
            "3708 already has p_z(xi|X_B,q)=p_0 exp[z^A Y_A^perp-W], so the exponential-family/Fisher object exists as a conditional construction.",
            "derive this p_z from parent A_B/Z rather than declaring it",
        ),
        (
            "ADJ3720_2_measure_normalization",
            "mu_H/dmu_H bath measure",
            "NOT_SIGNED",
            "The source-measure files concern Hamiltonian/worldtube mass measure, not the unresolved-bath measure needed by the Fisher KL construction.",
            "do not confuse source measure with bath measure; build the bath measure or demote to coefficient row",
        ),
        (
            "ADJ3720_3_scale_theta",
            "Theta_H or T_eff scale with units",
            "SYMBOL_EXISTS_UNITS_MISSING",
            "3708/3709 provide T_eff/Theta_H*iota_H structure, but the parent origin and unit map into local m^-2 operator units remain unsigned.",
            "derive scale from parent coarse-grain/free-energy normalization or keep Xi_H symbolic",
        ),
        (
            "ADJ3720_4_parity_involution",
            "z parity / exchange involution",
            "BEST_SUPPORTED_CANDIDATE_NOT_COMPONENT_DERIVED",
            "Response-doublet and odd-residual files contain exchange symmetry/even action rows, but they explicitly say component coverage and matter/boundary odd-charge zeros are not derived.",
            "attempt response-doublet -> Gibbs z-parity map next",
        ),
        (
            "ADJ3720_5_identifiability",
            "positive Fisher floor iota_H",
            "FORMULA_EXISTS_PROOF_MISSING",
            "3708 defines iota_H/lambda_min but does not prove a positive lower bound for all active local fibre directions.",
            "prove no active z-direction is bath-invisible or retain a finite lower-bound row",
        ),
        (
            "ADJ3720_6_boundary_silence",
            "boundary/source silence",
            "CURRENTLY_BLOCKED",
            "516/517/1011 all identify J_Z/B_Z or boundary/source work as the hard open clause.",
            "derive parity-even boundary/no odd source charge or keep F_loss/QK_loss active",
        ),
        (
            "ADJ3720_7_unit_map",
            "U_H same-basis unit map",
            "MISSING",
            "No corpus row found that maps Fisher Hessian units into the local R10/PPN operator basis without remaining symbolic.",
            "construct U_H from the same field metric G_H and local residual projection, or keep nonclaim",
        ),
    ]
    return [
        {
            **base(stamp),
            "adjudication_id": adjudication_id,
            "clause": clause,
            "status": status,
            "evidence_summary": evidence_summary,
            "next_action": next_action,
            "claim_allowed": False,
        }
        for adjudication_id, clause, status, evidence_summary, next_action in rows
    ]


def bridge_rows(stamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "BRIDGE3720_0_identify_z",
            "z^A := Z^A=(R_+^A-R_-^A)/2",
            "turns the response-doublet odd coordinate into the Fisher bath fibre coordinate",
            "needs component map through all active local residual channels",
        ),
        (
            "BRIDGE3720_1_identify_parity",
            "R_z corresponds to exchange E:R_+^A<->R_-^A",
            "makes the 3719 z -> -z parity a parent exchange symmetry",
            "needs exchange to be exact parent symmetry, not notation",
        ),
        (
            "BRIDGE3720_2_identify_action",
            "A_B or Delta S_fibre reduces to Gamma_eff even quadratic density",
            "connects GO516/AV517 action candidate to the Fisher KL potential",
            "needs xi/bath variables or a proof that integrating xi yields the even density",
        ),
        (
            "BRIDGE3720_3_identify_scale",
            "Theta_H I_H equals the quadratic operator M_AB after same-basis normalization",
            "turns Fisher floor into the response-doublet positive operator",
            "needs unit map U_H and field metric G_H",
        ),
        (
            "BRIDGE3720_4_boundary_guard",
            "J_Z=B_Z=0 corresponds to R_odd,F1=R_odd,BQK=B_boundary=0",
            "collapses 3718 correction budgets if signed",
            "currently open in 516/517/1011",
        ),
    ]
    return [
        {
            **base(stamp),
            "bridge_id": bridge_id,
            "proposed_identification": proposed_identification,
            "why_it_matters": why_it_matters,
            "required_before_claim": required_before_claim,
            "status": "BRIDGE_TARGET_NOT_YET_PROVED",
            "claim_allowed": False,
        }
        for bridge_id, proposed_identification, why_it_matters, required_before_claim in rows
    ]


def decision_rows(stamp: str) -> list[dict[str, object]]:
    decisions = [
        (
            "DEC3720_0_not_empty",
            "CORPUS_HAS_PARTIAL_SUPPORT",
            "The corpus contains Fisher bath/exponential-family structure and a separate response-doublet parity/even-action structure.",
        ),
        (
            "DEC3720_1_not_signed",
            "3719_MECHANISM_NOT_SIGNED_AS_CURRENT_MTS",
            "No source currently supplies the full combined parent Gibbs bath, measure, Theta/unit map, exact parity, identifiability, and boundary silence package.",
        ),
        (
            "DEC3720_2_best_route",
            "MAP_RESPONSE_DOUBLET_TO_GIBBS_PARITY_NEXT",
            "The strongest route is to identify Fisher z with the exchange-odd doublet coordinate Z and prove the quadratic even action is the KL/free-energy Hessian.",
        ),
        (
            "DEC3720_3_source_measure_warning",
            "SOURCE_MEASURE_IS_NOT_BATH_MEASURE",
            "Hamiltonian/worldtube source-measure work remains crucial for Newton/GM, but it does not by itself supply mu_H for the Fisher bath.",
        ),
    ]
    return [
        {
            **base(stamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in decisions
    ]


def claim_gate_rows(stamp: str) -> list[dict[str, object]]:
    gates = [
        ("CG3720_0_A_B", "BLOCKED", "parent A_B or free-energy action is matched to response/Fisher variables"),
        ("CG3720_1_mu_H", "BLOCKED", "bath measure/partition normalization is owned"),
        ("CG3720_2_Theta_UH", "BLOCKED", "Theta_H/T_eff and U_H unit map are parent-owned"),
        ("CG3720_3_parity", "BLOCKED", "exchange-doublet parity equals z -> -z for all active local components"),
        ("CG3720_4_identifiability", "BLOCKED", "positive Fisher/operator floor is proved"),
        ("CG3720_5_boundary", "BLOCKED", "source-current and boundary odd work vanish or are bounded"),
        ("CG3720_6_claim", "BLOCKED", "local GR/R10/PPN screening claim allowed"),
    ]
    return [
        {
            **base(stamp),
            "gate_id": gate_id,
            "gate_status": gate_status,
            "required_before_claim": required_before_claim,
            "claim_allowed": False,
        }
        for gate_id, gate_status, required_before_claim in gates
    ]


def status_rows(stamp: str) -> list[dict[str, object]]:
    return [{
        **base(stamp),
        "status_id": "STATUS3720_0",
        "status": "PARTIAL_CORPUS_SUPPORT_BRIDGE_REQUIRED",
        "summary": "3720 finds real partial support: Fisher bath rows and response-doublet parity rows exist, but they are not yet one parent-owned mechanism. The next move is the bridge proof z=Z and Theta_H I_H=M_AB, with boundary/source silence retained.",
        "claim_allowed": False,
    }]


def next_target_rows(stamp: str) -> list[dict[str, object]]:
    return [{
        **base(stamp),
        "next_id": "NEXT3720_0",
        "target_doc": "3721-Y5-R2FR-response-doublet-to-Gibbs-bath-parity-map-or-demotion.md",
        "target_script": "scripts/Y5_R2FR_3721_response_doublet_to_Gibbs_bath_parity_map_or_demotion.py",
        "objective": "try to prove that Fisher bath coordinate z is the exchange-odd response-doublet coordinate Z, that exchange parity gives z -> -z, and that Theta_H I_H is the same positive operator as the response-doublet quadratic density; otherwise demote the 3719 mechanism to a separate conditional closure",
        "success_gate": "z=Z, parity, action/free-energy Hessian, unit map, and boundary/source silence are either parent-signed or explicitly retained as finite nonclaim rows",
        "claim_allowed": False,
    }]


def validation_rows(stamp: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated_paths = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3720*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    checks = [
        ("sources_exist", "key sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "key source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "generated outputs exist", all(path.exists() for path in generated_paths)),
        ("csv_parse", "generated CSV files parse and are nonempty", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("scan_hits", "automated hit scan produced rows for every requirement", len({row["req_id"] for row in parse_csv(paths["automated_hits"])}) == len(REQUIREMENTS)),
        ("adjudication_complete", "every requirement adjudicated", len(parse_csv(paths["adjudication"])) == len(REQUIREMENTS)),
        ("bridge_target", "bridge rows include z=Z and Theta_H I_H=M_AB", all(token in read_text(paths["bridge"]) for token in ["z^A := Z^A", "Theta_H I_H"])),
        ("decisions", "decisions select bridge route and source-measure warning", all(token in read_text(paths["decisions"]) for token in ["MAP_RESPONSE_DOUBLET_TO_GIBBS_PARITY_NEXT", "SOURCE_MEASURE_IS_NOT_BATH_MEASURE"])),
        ("claim_gates_blocked", "all claim gates remain blocked", all(row["gate_status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("next_target_3721", "next target advances to bridge proof", "3721" in read_text(paths["next_target"])),
        ("doc_core_terms", "markdown summarizes partial support and bridge route", all(token in read_text(paths["doc"]) for token in ["partial support", "not yet one parent-owned mechanism", "z=Z"])),
        ("no_formalization_leak", "no 3720 files written to formalization-workbench", len(formal_files) == 0),
    ]
    return [
        {
            **base(stamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "",
        }
        for validation_id, description, result in checks
    ]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3720 — Corpus Hunt: Parent Bath, Scale, and Parity Clauses",
        "",
        "## Status",
        "- `PARTIAL_CORPUS_SUPPORT_BRIDGE_REQUIRED`",
        "- The corpus is not empty: it has partial support from Fisher/bath rows and response-doublet parity/even-action rows.",
        "- The important result is that these are not yet one parent-owned mechanism; the bridge proof is now the next exact target.",
        "",
        "## Main Result",
        "- `3708` supports a conditional Fisher/exponential-family bath: `p_z` and `D_KL` exist as a structural route.",
        "- `516/517` support a conditional response-doublet even action: exchange-odd `Z` has a quadratic density and no linear term if source/boundary clauses vanish.",
        "- `541/542` support source-measure/GM work, but that is not the same as the unresolved-bath measure `mu_H`.",
        "- Therefore the next serious derivation is the bridge `z=Z`, `R_z=exchange`, and `Theta_H I_H = M_AB` in the same units/basis.",
        "",
        "## Clause Adjudication",
    ]
    for row in grouped["adjudication"]:
        lines.append(f"- `{row['adjudication_id']}` `{row['status']}` — {row['clause']}: {row['evidence_summary']} Next: {row['next_action']}.")
    lines.extend(["", "## Bridge Contract"])
    for row in grouped["bridge"]:
        lines.append(f"- `{row['bridge_id']}` `{row['proposed_identification']}` | {row['why_it_matters']} | needs: {row['required_before_claim']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` `{row['gate_status']}` | {row['required_before_claim']}")
    lines.extend(["", "## Source Register"])
    for row in grouped["source_register"]:
        lines.append(f"- `{row['source_id']}`: exists={row['exists']} needle_found={row['needle_found']} path=`{row['path']}`")
    lines.extend([
        "",
        "## Automated Scan",
        f"- See `{paths['automated_hits']}` for ranked source hits by requirement.",
        "",
        "## Next Target",
        "- `3721-Y5-R2FR-response-doublet-to-Gibbs-bath-parity-map-or-demotion.md`",
        "- Objective: try the bridge proof directly; if it fails, demote the 3719 mechanism to a conditional closure and retain finite coefficient rows.",
        "",
        "## Validation",
        f"- See `{paths['validation']}`.",
    ])
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    stamp = now()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3720_SOURCE_REGISTER.csv",
        "automated_hits": RESIDUALS / "P8_Y5_R2FR_3720_AUTOMATED_CORPUS_HITS.csv",
        "adjudication": RESIDUALS / "P8_Y5_R2FR_3720_CLAUSE_ADJUDICATION_ROWS.csv",
        "bridge": RESIDUALS / "P8_Y5_R2FR_3720_BRIDGE_CONTRACT_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3720_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3720_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3720_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3720_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3720_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(stamp),
        "automated_hits": automated_hit_rows(stamp),
        "adjudication": adjudication_rows(stamp),
        "bridge": bridge_rows(stamp),
        "decisions": decision_rows(stamp),
        "claim_gates": claim_gate_rows(stamp),
        "status": status_rows(stamp),
        "next_target": next_target_rows(stamp),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(stamp, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3720 validation failed: {failures}")
    print("wrote 3720 checkpoint: partial corpus support found; bridge proof selected")


if __name__ == "__main__":
    main()

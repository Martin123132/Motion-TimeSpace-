from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2148-Y5-R2FR-Phi-second-derivative-zero-or-visible-c2-source-row.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2147": ROOT / "2147-Y5-R2FR-local-GR-two-gate-spine-source-operator-join.md",
    "1824": ROOT / "1824-Y5-R2FR-Phi-second-derivative-zero-or-visible-c2-source-row.md",
    "1825": ROOT / "1825-Y5-R2FR-signed-deficit-oddness-theorem-or-c2-prior-row.md",
    "1826": ROOT / "1826-Y5-R2FR-log-holonomy-action-owner-or-trace-norm-c2-prior.md",
    "1827": ROOT / "1827-Y5-R2FR-Palatini-Regge-field-match-or-c2-scalaron-map.md",
    "1823": ROOT / "1823-Y5-R2FR-primitive-deficit-action-law-or-visible-c2-owner-row.md",
}


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def has_any(text: str, alternatives: list[str]) -> bool:
    return any(item in text for item in alternatives)


def find_line(path: Path, alternatives: list[str]) -> tuple[int, str]:
    text = read_text(path) if path.exists() else ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if has_any(line, alternatives):
            return line_number, line.strip()
    return 0, "MISSING_NEEDLE"


def formalization_has_2148_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2148-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2148*",
        "*Y5_R2FR_Phi_second_derivative_zero_or_visible_c2_source_row_2148*",
        "*AFRAME_PHI_C2_FRONTIER_2148*",
        "*JR2148*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2148_00_2147", DOCS["2147"], [["VAL2147_OVERALL"], ["PHI_SECOND_DERIVATIVE_ZERO_OR_C2_SOURCE_NEXT"], ["R_join"]], "current two-gate handoff selects Phi''/c2 operator hinge"),
        ("SRC2148_01_1823", DOCS["1823"], [["VAL1823_OVERALL"], ["c2_visible"], ["Phi''(0)"]], "generic deficit cost exposes visible c2"),
        ("SRC2148_02_1824", DOCS["1824"], [["VAL1824_OVERALL"], ["signed-deficit oddness"], ["Phi''(0)=0"]], "oddness lemma kills c2 conditionally"),
        ("SRC2148_03_1825", DOCS["1825"], [["VAL1825_OVERALL"], ["LOG_HOLONOMY_ACTION_OWNER_NEXT"], ["trace/norm"]], "orientation alone fails; log-angle owner is next"),
        ("SRC2148_04_1826", DOCS["1826"], [["VAL1826_OVERALL"], ["PALATINI_REGGE_FIELD_MATCH_NEXT"], ["trace/norm c2"]], "Palatini/Regge owner contract versus trace/norm c2 prior"),
        ("SRC2148_05_1827", DOCS["1827"], [["VAL1827_OVERALL"], ["CONNECTION_HINGE_OWNER_OR_C2_MAP_FILL_NEXT"], ["FIELD_MATCH_FAILS_CURRENT_CORPUS"]], "field match fails current corpus; connection/hinge owner is the live frontier"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                needles_found=needles_found,
                expected_needles="; ".join(" OR ".join(group) for group in needle_groups),
                role=role,
            )
        )
    return rows


def phi_c2_chain_rows() -> list[dict[str, object]]:
    chain = [
        ("PC2148_0", "2147", "two-gate operator hinge", "local-GR contract selects Phi''(0)=0 or visible c2 source as the least-circular operator attack", "operator gate first"),
        ("PC2148_1", "1823", "visible c2 exposed", "generic Phi(delta)=k1 delta+c2 delta^2+... creates c2_visible=Phi''(0)/2", "c2 source row mandatory unless zero theorem closes"),
        ("PC2148_2", "1824", "oddness lemma", "if Phi(-delta)=-Phi(delta), then Phi''(0)=0", "exact math, parent premise unsigned"),
        ("PC2148_3", "1825", "signed-deficit oddness", "orientation alone does not force odd action; trace/norm/even costs survive", "log-holonomy action owner needed"),
        ("PC2148_4", "1826", "log-holonomy owner", "Palatini/Regge linear e e F or area*deficit shape would own signed log-angle response", "contract written, not MTS-derived"),
        ("PC2148_5", "1827", "field match", "coframe candidate exists but connection, holonomy, hinge bivector, variation and source descent are not parent-signed", "connection/hinge owner or c2 map fill next"),
    ]
    rows: list[dict[str, object]] = []
    for chain_id, checkpoint, object_name, gain, status in chain:
        source_path = DOCS[checkpoint]
        line_number, _ = find_line(source_path, ["Current verdict", "Current Verdict", "**Current verdict:**"])
        rows.append(
            row(
                chain_id=chain_id,
                checkpoint=checkpoint,
                source_path=str(source_path),
                verdict_line=line_number,
                object=object_name,
                gain=gain,
                current_status=status,
            )
        )
    return rows


def theorem_status_rows() -> list[dict[str, object]]:
    return [
        row(status_id="TH2148_0_exact", claim_piece="Phi'' zero math", theorem="smooth odd Phi implies all even Taylor coefficients vanish, so c2_visible=Phi''(0)/2=0", result="EXACT_CONDITIONAL_LEMMA", blocker="Phi oddness is not parent-signed"),
        row(status_id="TH2148_1_orientation", claim_piece="orientation route", theorem="signed deficit orientation is necessary but not sufficient", result="LOOPHOLE_IDENTIFIED", blocker="delta^2, 1-cos(delta), trace and norm actions can ignore the sign"),
        row(status_id="TH2148_2_log_angle", claim_piece="signed log-holonomy owner", theorem="a parent action linear in signed log holonomy / area deficit would make visible c2 zero credible", result="BEST_ZERO_ROUTE_CONTRACT", blocker="MTS fields are not yet matched to the Palatini/Regge action blocks"),
        row(status_id="TH2148_3_field_match", claim_piece="Palatini/Regge field match", theorem="need e_obs, omega_obs/Gamma_eff, F[omega], B_h/A_h, signed Log(U_h), kappa, matter descent and variation in one parent action", result="FAILS_CURRENT_CORPUS", blocker="connection compatibility and hinge bivector owner are missing"),
        row(status_id="TH2148_4_fallback", claim_piece="finite c2 branch", theorem="if trace/norm/even holonomy cost survives, c2_visible must be finite and mapped into c_R2_eff/scalaron/PPN/R10 rows", result="FALLBACK_READY_NONCLAIM", blocker="parent Phi value, cell scale, shape factor and local response maps are missing"),
    ]


def current_frontier_rows() -> list[dict[str, object]]:
    return [
        row(frontier_id="FR2148_0_coframe", required_owner="observed coframe/metric", current_status="CANDIDATE_EXISTS", missing_piece="single parent action variation and compatibility with connection"),
        row(frontier_id="FR2148_1_connection", required_owner="Gamma_eff / omega_obs compatibility", current_status="PRIMARY_MISSING_GEOMETRY_OWNER", missing_piece="prove Gamma_eff is LC/spin connection of e_obs or controlled independent connection"),
        row(frontier_id="FR2148_2_hinge", required_owner="oriented hinge bivector / area A_h", current_status="PRIMARY_MISSING_GEOMETRY_OWNER", missing_piece="derive B_h ~ integral_h e wedge e and signed cell orientation from MTS domain grammar"),
        row(frontier_id="FR2148_3_holonomy", required_owner="signed Log(U_h) branch", current_status="MISSING_BRANCH_DOMAIN", missing_piece="small-curvature log branch, topology/cycle guard and boundary holonomy residual"),
        row(frontier_id="FR2148_4_action", required_owner="linear Palatini/Regge action term", current_status="CONTRACT_ONLY", missing_piece="derive from MTS parent grammar rather than importing EH/Regge"),
        row(frontier_id="FR2148_5_source", required_owner="matter/source descent for Palatini branch", current_status="HELD_SECONDARY", missing_piece="same-frame source descent and Pi_M/Hilbert/Noether charge equality"),
        row(frontier_id="FR2148_6_c2_map", required_owner="finite c2 scalaron fallback", current_status="NONCLAIM_FALLBACK", missing_piece="c2 value/prior, c_R2_eff, scalaron mass/coupling, PPN/R10/local maps"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2148_0_phi_result", decision="PHI_SECOND_DERIVATIVE_ZERO_NOT_PROVEN", because="oddness math is exact but parent action ownership of signed log-holonomy is not derived", next_action="do not set c2_visible=0"),
        row(decision_id="DEC2148_1_fast_forward", decision="CURRENT_BRANCH_SYNCED_TO_1827_FRONTIER", because="1824-1827 already narrowed the Phi/c2 problem to Palatini/Regge field match and then connection/hinge ownership", next_action="avoid repeating broad Phi/c2 audits"),
        row(decision_id="DEC2148_2_best_route", decision="CONNECTION_HINGE_OWNER_NEXT", because="the clean linear-curvature route now needs Gamma_eff/omega_obs compatibility and B_h/A_h ownership from MTS geometry", next_action="attempt connection/hinge derivation"),
        row(decision_id="DEC2148_3_fallback", decision="C2_SCALARON_MAP_RETAINED_NONCLAIM", because="if connection/hinge owner fails, trace/norm/even action costs remain legal and finite c2 must be tested", next_action="fill c2 scalaron map only with real inputs"),
        row(decision_id="DEC2148_4_claim_policy", decision="NO_LOCAL_GR_NEWTON_CLAIM", because="this is one operator subgate; source bridge, Gamma_G, connection, higher terms and PPN maps remain open", next_action="keep private nonclaim status"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2148_0_2149",
            next_target="2149-Y5-R2FR-connection-hinge-bivector-owner-or-c2-map-fill.md",
            script="scripts/Y5_R2FR_connection_hinge_bivector_owner_or_c2_map_fill_2149.py",
            objective="Derive Gamma_eff/omega_obs compatibility and the oriented hinge bivector/area owner from MTS cell geometry; if not, begin the finite c2_visible -> c_R2_eff -> scalaron/PPN/R10 map as nonclaim rows.",
            forbidden_shortcuts="do not import Palatini/Regge as an ansatz; do not treat coframe candidate as full field match; do not zero c2 from orientation alone; do not claim local GR/Newton; no formalization-workbench edits; no GitHub action",
        )
    ]


def write_branch_copies(
    chain: list[dict[str, object]],
    theorem: list[dict[str, object]],
    frontier: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2148_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_PHI_C2_FRONTIER_2148_NONCLAIM.csv", theorem + frontier),
        ("COPY2148_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2148_PHI_C2_OPERATOR_FRONTIER_NONCLAIM.csv", chain + theorem),
        ("COPY2148_2_acquisition_queue", QUEUE / "JR2148_CONNECTION_HINGE_OR_C2_MAP_QUEUE.csv", next_rows + frontier),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    chain: list[dict[str, object]],
    theorem: list[dict[str, object]],
    frontier: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    chain_ok = len(chain) == 6 and chain[0]["checkpoint"] == "2147" and chain[-1]["checkpoint"] == "1827"
    theorem_ok = (
        any(item["status_id"] == "TH2148_0_exact" and item["result"] == "EXACT_CONDITIONAL_LEMMA" for item in theorem)
        and any(item["status_id"] == "TH2148_3_field_match" and item["result"] == "FAILS_CURRENT_CORPUS" for item in theorem)
        and any(item["status_id"] == "TH2148_4_fallback" and item["result"] == "FALLBACK_READY_NONCLAIM" for item in theorem)
    )
    frontier_ok = (
        any(item["frontier_id"] == "FR2148_1_connection" and item["current_status"] == "PRIMARY_MISSING_GEOMETRY_OWNER" for item in frontier)
        and any(item["frontier_id"] == "FR2148_2_hinge" and item["current_status"] == "PRIMARY_MISSING_GEOMETRY_OWNER" for item in frontier)
        and any(item["frontier_id"] == "FR2148_6_c2_map" for item in frontier)
    )
    decisions_ok = (
        any(item["decision"] == "CONNECTION_HINGE_OWNER_NEXT" for item in decisions)
        and any(item["decision"] == "NO_LOCAL_GR_NEWTON_CLAIM" for item in decisions)
    )
    next_ok = any(item["route_id"] == "NEXT2148_0_2149" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, chain, theorem, frontier, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2148_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, chain_ok, theorem_ok, frontier_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2148_00_sources", sources_ok, "2147 and 1823-1827 source checkpoints validate"),
        ("VAL2148_01_chain", chain_ok, "current branch fast-forwards from 2147 to 1827 frontier"),
        ("VAL2148_02_theorem", theorem_ok, "Phi oddness is exact conditional, field match fails, fallback retained"),
        ("VAL2148_03_frontier", frontier_ok, "connection and hinge owners are selected as missing geometry owners"),
        ("VAL2148_04_decisions", decisions_ok, "decisions select connection/hinge owner and block local claims"),
        ("VAL2148_05_next", next_ok, "next target is 2149 connection-hinge owner or c2 map fill"),
        ("VAL2148_06_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2148_07_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2148_08_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2148_09_formalization_clean", formalization_clean, "formalization-workbench untouched by 2148"),
        ("VAL2148_10_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2148_OVERALL", all_ok, "2148 syncs the Phi/c2 hinge to the connection-hinge geometry-owner frontier and keeps c2 scalaron fallback nonclaim."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    chain: list[dict[str, object]],
    theorem: list[dict[str, object]],
    frontier: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2148 - Y5/R2FR Phi Second Derivative Zero Or Visible c2 Source Row",
            "## Current Verdict",
            "2148 does **not** prove `Phi''(0)=0`, `c2_visible=0`, R2/fR silence, local GR, Newton, PPN, WEP, R10, or any public claim. It syncs the current 2147 two-gate spine to the deepest verified private operator frontier.",
            "The useful result is sharp: the visible quadratic wound is no longer vague. Smooth signed oddness would kill `c2_visible`, but the corpus does not yet prove that MTS owns a physical signed log-holonomy action variable. The old branch already pushes this to the Palatini/Regge field-match test, which fails current corpus on the connection and oriented hinge-bivector owners.",
            "So the next live target is **connection + hinge ownership**: derive `Gamma_eff/omega_obs` compatibility and an oriented `B_h/A_h` cell/hinge measure from MTS geometry. If that fails, the honest fallback is a finite `c2_visible -> c_R2_eff -> scalaron/PPN/R10` residual map, not a hidden GR import.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Phi/c2 Frontier Chain",
            md_table(chain, ["chain_id", "checkpoint", "verdict_line", "object", "gain", "current_status", "valid_for_claim"]),
            "## Theorem Status",
            md_table(theorem, ["status_id", "claim_piece", "theorem", "result", "blocker", "valid_for_claim"]),
            "## Current Frontier",
            md_table(frontier, ["frontier_id", "required_owner", "current_status", "missing_piece", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    chain = phi_c2_chain_rows()
    theorem = theorem_status_rows()
    frontier = current_frontier_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2148_SOURCE_REGISTER.csv",
        "chain": OUT / "P8_Y5_PARENT_QLOC_2148_PHI_C2_FRONTIER_CHAIN.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2148_THEOREM_STATUS.csv",
        "frontier": OUT / "P8_Y5_PARENT_QLOC_2148_CURRENT_FRONTIER.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2148_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2148_NEXT_TARGET.csv",
        "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2148_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2148_VALIDATION.csv",
    }

    write_csv(paths["sources"], sources)
    write_csv(paths["chain"], chain)
    write_csv(paths["theorem"], theorem)
    write_csv(paths["frontier"], frontier)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(chain, theorem, frontier, next_rows)
    write_csv(paths["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, chain, theorem, frontier, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, chain, theorem, frontier, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()

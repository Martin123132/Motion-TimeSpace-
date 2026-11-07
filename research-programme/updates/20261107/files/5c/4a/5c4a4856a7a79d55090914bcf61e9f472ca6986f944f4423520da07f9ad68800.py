from common import ROOT, modest, require, read, digest
import check_tangent
import probe_analysis


if __name__ == "__main__":
    modest()
    original = read(ROOT / "tangent-check-result.json")
    require(original["passed"] and digest(ROOT / "check_tangent.py") == original["source_sha256"], "changed checker")
    require(digest(ROOT / "phase-resolved/probe_analysis.py") == original["analysis_source_sha256"], "changed analysis")
    check_tangent.ROOT = probe_analysis.ROOT = ROOT / "phase-resolved"
    check_tangent.main()

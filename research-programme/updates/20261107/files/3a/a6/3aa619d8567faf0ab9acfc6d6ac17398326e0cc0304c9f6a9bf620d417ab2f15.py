from __future__ import annotations

import polar_radiation


original_settings = polar_radiation.settings


def resolved_settings(label):
    chosen = original_settings(label)
    assert label == 'coarse'
    chosen['source_order'] = 40
    chosen['source_panels_per_half'] = 32
    chosen['source_resolution_override'] = 'Resolved high-frequency source; radial/interior settings remain coarse.'
    return chosen


if __name__ == '__main__':
    polar_radiation.settings = resolved_settings
    polar_radiation.main()

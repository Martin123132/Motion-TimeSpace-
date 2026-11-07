from __future__ import annotations

import difflib
import zipfile
from stage_common import *


def main():
    folder=ROOT/'sources/native-delta'
    folder.mkdir(parents=True,exist_ok=False)
    changed=[]
    patches=[]
    with zipfile.ZipFile(folder/'source-delta.zip','x',compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted((ROOT/'native').rglob('*')):
            if not path.is_file() or path.suffix not in ['.f90','.py'] or '__pycache__' in path.parts:
                continue
            relative=path.relative_to(ROOT/'native')
            old=PARENT/'native'/relative
            if old.is_file() and digest(old)!=digest(path):
                archive.write(path,relative.as_posix())
                changed.append(dict(path=relative.as_posix(),parent_sha256=digest(old),sha256=digest(path)))
                patches.extend(difflib.unified_diff(old.read_text().splitlines(keepends=True),path.read_text().splitlines(keepends=True),
                    fromfile='stage54/'+relative.as_posix(),tofile='stage55/'+relative.as_posix()))
    (folder/'source-delta.patch').write_text(''.join(patches),encoding='utf-8')
    finish(folder,dict(changed=changed,base_stage=PARENT.name,full_stage54_source_retained=True),__file__,
        [folder/'source-delta.zip',folder/'source-delta.patch'])


if __name__=='__main__':
    main()

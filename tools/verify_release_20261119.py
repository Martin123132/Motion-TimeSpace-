"""Verify the November 19 science release with stdlib, optionally from an exact Git revision."""
import argparse
import csv
import hashlib
import io
import json
import subprocess
import zipfile
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[1]
PREFIX='research-programme/updates/20261119'
digest=lambda data:hashlib.sha256(data).hexdigest()
def check(condition,message):
    if not condition:raise ValueError(message)
def rows(data):return list(csv.DictReader(io.StringIO(data.decode('utf-8-sig'),newline='')))
def safe(path):
    p=PurePosixPath(path)
    check(path and not p.is_absolute() and '..' not in p.parts and ':' not in path and '\\' not in path and p.as_posix()==path,path)
    return p
class Store:
    def __init__(self,ref):
        self.proc=None
        if ref:
            revision=subprocess.check_output(['git','rev-parse','--verify',ref+'^{tree}'],cwd=ROOT,text=True).strip()
            raw=subprocess.check_output(['git','ls-tree','-rz',revision,'--',PREFIX],cwd=ROOT)
            self.files={}
            for line in raw.split(b'\0'):
                if not line:continue
                header,path=line.split(b'\t',1);mode,kind,oid=header.split()
                check(mode==b'100644' and kind==b'blob',path)
                self.files[path.decode()[len(PREFIX)+1:]]=oid
            self.proc=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        else:
            location=ROOT/PREFIX
            self.files={p.relative_to(location).as_posix():p for p in location.rglob('*') if p.is_file() and not p.is_symlink()}
    def get(self,name):
        safe(name);value=self.files[name]
        if self.proc is None:return value.read_bytes()
        self.proc.stdin.write(value+b'\n');self.proc.stdin.flush()
        oid,kind,length=self.proc.stdout.readline().split();check(oid==value and kind==b'blob',name)
        data=self.proc.stdout.read(int(length));check(len(data)==int(length) and self.proc.stdout.read(1)==b'\n',name);return data
    def close(self):
        if self.proc:
            self.proc.stdin.close();self.proc.stdout.close();check(self.proc.wait()==0,'git cat-file failed')

def verify(store):
    covered={'ROOT-SHA256.csv'};parts=rows(store.get('ROOT-SHA256.csv'));digests={}
    for part in parts:
        key=part['path'];check(key not in covered,key);covered.add(key);content=store.get(key)
        check(digest(content)==part['sha256'],key);entries=rows(content);check(len(entries)==int(part['rows'])<=250,key)
        for ent in entries:
            name=ent['path'];check(name not in covered,name);covered.add(name);data=store.get(name)
            check(len(data)==int(ent['bytes']) and digest(data)==ent['sha256'],name);digests[name]=ent['sha256']
    check(covered==set(store.files),'tree differs from complete digest index')
    dirs=defaultdict(set)
    for name in covered:
        path=safe(name)
        for parent in path.parents:dirs[parent].add(path.relative_to(parent).parts[0])
    maximum=max(map(len,dirs.values()));check(maximum<=256,('crowded directory',maximum))
    catalogue=rows(store.get('stages.csv'));summary=json.loads(store.get('release.json'));counts=Counter()
    check(len(catalogue)==len({r['stage'] for r in catalogue})==summary['stages'],'stage count')
    used_packs=set();total=0
    for stage in catalogue:
        reader=stage['reader'];check(reader in covered,reader);folder=reader.rsplit('/',1)[0]+'/'
        inventories=sorted(n for n in covered if n.startswith(folder+'inventory-') and n.endswith('.csv'))
        receipts=[];seen=set();packed=defaultdict(dict);loose=set()
        for number,inv in enumerate(inventories,1):
            check(inv==folder+f'inventory-{number:02}.csv',inv)
            entries=rows(store.get(inv));check(0<len(entries)<=700,inv);receipts.extend(entries)
        for r in receipts:
            name=r['source'];safe(name);check(name not in seen,name);seen.add(name)
            h=r['expected_sha256'];check(len(h)==64 and all(ch in '0123456789abcdef' for ch in h),name)
            disp=r['disposition'];counts[disp]+=1
            if name==stage['authority']:check(h==stage['authority_sha256'],name)
            if disp not in ('original','reading-copy'):
                check(not any(r[k] for k in ('artifact','member','public_sha256','public_bytes')),name);continue
            pub=r['public_sha256'];n=int(r['public_bytes']);check(disp!='original' or (pub==h and n==int(r['source_bytes'])),name)
            artifact=folder+str(safe(r['artifact']));check(artifact in covered,artifact)
            if r['member']:
                member=str(safe(r['member']));check(member not in packed[artifact],member);packed[artifact][member]=(n,pub)
            else:check(digests[artifact]==pub and artifact not in loose,artifact);loose.add(artifact)
        check(stage['authority'] in seen and reader in loose and len(receipts)==int(stage['source_records']),folder)
        check(len(loose)+sum(map(len,packed.values()))==int(stage['original'])+int(stage['reading_copies']),folder)
        check(set(inventories)|loose|set(packed)=={n for n in covered if n.startswith(folder)},folder)
        for path,members in packed.items():
            with zipfile.ZipFile(io.BytesIO(store.get(path))) as z:
                entries=z.namelist();check(len(entries)==len(members)<=150 and set(entries)==set(members),path)
                for member,(length,sha) in members.items():
                    obj=z.read(member);check(len(obj)==length and digest(obj)==sha,path+'/'+member)
            used_packs.add(path)
        total+=len(receipts)
    check(dict(counts)==summary['dispositions'] and total==summary['total_records'],'inventory totals')
    return dict(stages=len(catalogue),source_records=total,originals=counts['original'],reading_copies=counts['reading-copy'],
                packs=len(used_packs),release_files=len(covered),max_directory_entries=maximum)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--rev',help='verify published Git blobs, not the working copy');args=p.parse_args()
    store=Store(args.rev)
    try:print(json.dumps(verify(store),indent=2))
    finally:store.close()

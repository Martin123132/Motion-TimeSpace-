import urllib.request
from thermal_common import *


def main():
    modest()
    folder=ROOT/'results/sources'
    folder.mkdir(parents=True,exist_ok=False)
    source_folder=ROOT/'sources'
    source_folder.mkdir(exist_ok=False)
    requests=[('https://arxiv.org/html/1110.0475v2','khatri-sunyaev-chluba-1110.0475v2.html'),
        ('https://arxiv.org/abs/1109.6552','chluba-sunyaev-1109.6552-abstract.html'),
        ('https://arxiv.org/abs/2109.04895','milonni-2109.04895-abstract.html')]
    rows=[]
    files=[]
    checks=[]
    for url,name in requests:
        request=urllib.request.Request(url,headers={'User-Agent':'MTS-private-source-audit/1.0'})
        with urllib.request.urlopen(request,timeout=40) as response:
            contents=response.read()
            final=response.url
            content_type=response.headers.get('Content-Type','')
            status=response.status
        path=source_folder/name
        path.write_bytes(contents)
        rows.append(dict(requested_url=url,final_url=final,http_status=status,content_type=content_type,
            local_path=str(path),sha256=digest(path),bytes=len(contents),retrieved_utc=datetime.now(timezone.utc).isoformat()))
        files.append(path)
        checks.append(dict(name='Primary source retrieved '+name,passed=status==200 and len(contents)>1000 and 'html' in content_type))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),sources=rows,
        unavailable_html_attempts=['https://arxiv.org/html/1109.6552v2','https://arxiv.org/html/2109.04895v2'],
        unavailable_html_not_used_as_equation_evidence=True),__file__,files)
    print(json.dumps(dict(sources=rows)),flush=True)


if __name__=='__main__':
    main()

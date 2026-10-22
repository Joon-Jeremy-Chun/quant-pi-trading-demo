"""Review public text for sensitive material; report locations, never matched text.

This is a conservative publication check, not proof that all sensitive content
can be detected. It reads only this public repository and optionally its history.
"""
import argparse
import ipaddress
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
TEXT = {'.py','.js','.cjs','.mjs','.html','.css','.json','.csv','.md','.txt','.svg',
        '.example','.yml','.yaml','.toml','.ini','.cfg','.sh','.bat','.ps1'}
HOSTS = {'github.com','docs.github.com','docs.python.org','www.python.org',
         'ir.library.illinoisstate.edu','doi.org','threejs.org','cdn.jsdelivr.net',
         'example.com','example.org','www.w3.org','127.0.0.1','localhost'}
RULES = {
    'private-key': re.compile(r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----'),
    'github-token': re.compile(r'(?:g[h]p|github_pat)_[A-Za-z0-9_]{20,}'),
    'cloud-access-key': re.compile(r'A[K]IA[A-Z0-9]{16}'),
    'slack-webhook': re.compile(r'https[:]//hooks[.]slack[.]com/services/'),
    'remote-shell-uri': re.compile(r'(?i)(?:s[s]h|s[c]p)://[^\s"<>]+'),
    'private-key-path': re.compile(r'(?i)(?:i[d]_rsa|i[d]_ed25519|[^\s/]+[.]pem)\b'),
    'private-local-path': re.compile(r'(?i)(?:[A-Z]:[\\/](?:Users|home)[\\/]|/(?:home|Users)/[A-Za-z0-9_-]+/)'),
}


def inspect_text(path, text):
    findings=[]
    for number,line in enumerate(text.splitlines(),1):
        for rule,pattern in RULES.items():
            if pattern.search(line): findings.append({'path':path,'line':number,'rule':rule})
        for token in re.findall(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])',line):
            try: address=ipaddress.ip_address(token)
            except ValueError:continue
            if str(address)!='127.0.0.1':findings.append({'path':path,'line':number,'rule':'non-localhost-address'})
        for url in re.findall(r'https?://[^\s<>"\x27`]+',line):
            parsed=urlsplit(url.rstrip('),.;'))
            if parsed.username or parsed.password or parsed.hostname not in HOSTS:
                findings.append({'path':path,'line':number,'rule':'unreviewed-url-host'})
    return findings


def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--history',action='store_true')
    args=parser.parse_args()
    names=set(git('ls-files','--cached','--others','--exclude-standard','-z').decode('utf-8').split('\0'))-{''}
    findings=[];count=0
    for name in sorted(names):
        p=ROOT/name
        if not p.is_file():continue
        if p.suffix.lower() in TEXT or p.name in {'.env.example','.gitignore','LICENSE'}:
            findings.extend(inspect_text(name,p.read_text(encoding='utf-8-sig')));count+=1
    history_blobs=0
    if args.history:
        seen=set()
        for commit in git('rev-list','--all').decode().splitlines():
            for item in git('ls-tree','-r','-z',commit).split(b'\0'):
                if not item:continue
                header,name=item.split(b'\t',1);sha=header.split()[2].decode();name=name.decode('utf-8')
                if sha in seen or Path(name).suffix.lower() not in TEXT:continue
                seen.add(sha)
                findings.extend(inspect_text('history:'+name,git('cat-file','blob',sha).decode('utf-8-sig')))
                history_blobs+=1
    print(json.dumps({'public_text_files':count,'history_text_blobs':history_blobs,'findings':findings},ensure_ascii=False,indent=2))
    return bool(findings)


if __name__=='__main__':raise SystemExit(main())

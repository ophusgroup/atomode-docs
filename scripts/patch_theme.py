"""Patch the downloaded book-theme template: keep top-level TOC sections
expanded, and replace the dialog-based search with a flat top-bar input.

Ported from quantem-docs / nanobeam-course. The stock theme opens a
sidebar section only while it contains the active page (and re-collapses
it on navigation), and its search opens a modal dialog. There are no
template options for either, so we patch the compiled bundles in
_build/templates. Run after the template has been downloaded (any
`myst build` or `myst start` does that), and re-run whenever _build is
cleared:

    python3 scripts/patch_theme.py

The deploy workflow runs this between a warm-up build and the real build.
"""

import glob
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
THEME = os.path.normpath(
    os.path.join(HERE, "..", "_build", "templates", "site", "myst", "book-theme")
)


# Flat top-bar search runtime (replaces the theme's dialog search).
# Injected into the server-rendered HTML. The search index path is
# resolved relative to the current page so it also works when the site
# is served under a path prefix (GitHub Pages project sites, e.g.
# /atomode-docs).
_RUNTIME = """
;(function(){
  /* ---------- flat top-bar search (replaces the theme's dialog) -------- */
  var idx=null,loading=false,waiters=[],base='';
  /* Record URLs in the index are written from the site root ('/modules/...')
     with no path prefix, so on a GitHub Pages project site they have to be
     prefixed or every hit lands on the 404 page. The prefix that serves the
     index is the prefix the pages live under, so probe for it and keep it. */
  function basePrefixes(){
    var seg=window.location.pathname.split('/').filter(Boolean);
    return seg.length?['/'+seg[0],'']:[''];
  }
  function href(u){
    return (u&&u.charAt(0)==='/')?base+u:u;
  }
  function load(cb){
    if(cb&&idx)return cb();
    if(cb)waiters.push(cb);
    if(idx||loading)return;
    loading=true;
    var pre=basePrefixes();
    function attempt(i){
      if(i>=pre.length){loading=false;waiters=[];return;}
      fetch(pre[i]+'/myst.search.json').then(function(r){
        if(!r.ok)throw new Error('http '+r.status);
        return r.json();
      }).then(function(d){
        idx=d.records||[];base=pre[i];loading=false;
        var w=waiters;waiters=[];w.forEach(function(f){f();});
      }).catch(function(){attempt(i+1);});
    }
    attempt(0);
  }
  function titleOf(h){
    return [h.lvl3,h.lvl2,h.lvl1].filter(Boolean)[0]||'';
  }
  function crumbOf(h){
    return [h.lvl1,h.lvl2,h.lvl3].filter(Boolean).join(' > ');
  }
  function search(q){
    if(!idx)return [];
    var terms=q.toLowerCase().split(/\\s+/).filter(Boolean);
    if(!terms.length)return [];
    var seen={},out=[];
    idx.forEach(function(rec){
      var h=rec.hierarchy||{};
      var title=titleOf(h),crumb=crumbOf(h);
      var hay=(crumb+' '+(rec.content||'')).toLowerCase();
      var titleHay=crumb.toLowerCase();
      var score=0;
      for(var i=0;i<terms.length;i++){
        if(hay.indexOf(terms[i])<0)return;
        if(titleHay.indexOf(terms[i])>=0)score+=3;
        score+=1;
      }
      if(rec.type!=='content')score+=2;
      var key=rec.url;
      if(seen[key]!==undefined){
        if(out[seen[key]].score>=score)return;
        out[seen[key]]={score:score,url:rec.url,title:title,crumb:crumb,
                        content:rec.content||''};
        return;
      }
      seen[key]=out.length;
      out.push({score:score,url:rec.url,title:title,crumb:crumb,
                content:rec.content||''});
    });
    out.sort(function(a,b){return b.score-a.score;});
    return out.slice(0,8);
  }
  function build(bar){
    if(!bar||bar.dataset.qemSearch)return;
    bar.dataset.qemSearch='1';
    var wrap=document.createElement('div');
    wrap.className='qem-search';
    var input=document.createElement('input');
    input.type='search';
    input.placeholder='Search';
    input.setAttribute('aria-label','Search this site');
    var list=document.createElement('div');
    list.className='qem-search-results';
    list.hidden=true;
    wrap.appendChild(input);
    wrap.appendChild(list);
    bar.style.display='none';
    bar.after(wrap);
    var active=-1,hits=[];
    function render(){
      list.innerHTML='';
      if(!hits.length){list.hidden=true;return;}
      hits.forEach(function(h,i){
        var a=document.createElement('a');
        a.href=href(h.url);
        a.className='qem-search-hit'+(i===active?' active':'');
        var t=document.createElement('div');
        t.className='qem-search-hit-title';
        t.textContent=h.crumb||h.title;
        a.appendChild(t);
        if(h.content){
          var c=document.createElement('div');
          c.className='qem-search-hit-text';
          c.textContent=h.content.slice(0,110);
          a.appendChild(c);
        }
        list.appendChild(a);
      });
      list.hidden=false;
    }
    function run(){
      active=-1;
      hits=search(input.value.trim());
      render();
    }
    input.addEventListener('focus',function(){load();});
    input.addEventListener('input',function(){
      load(run);   // re-runs once the index finishes loading
      run();
    });
    input.addEventListener('keydown',function(ev){
      if(ev.key==='ArrowDown'||ev.key==='ArrowUp'){
        ev.preventDefault();
        if(!hits.length)return;
        active=(active+(ev.key==='ArrowDown'?1:-1)+hits.length)%hits.length;
        render();
      }else if(ev.key==='Enter'){
        var h=hits[active<0?0:active];
        if(h){ev.preventDefault();window.location.href=href(h.url);}
      }else if(ev.key==='Escape'){
        input.value='';hits=[];render();input.blur();
      }
    });
    document.addEventListener('click',function(ev){
      if(!wrap.contains(ev.target)){hits=[];render();}
    });
    document.addEventListener('keydown',function(ev){
      if((ev.metaKey||ev.ctrlKey)&&ev.key.toLowerCase()==='k'){
        ev.preventDefault();ev.stopPropagation();input.focus();input.select();
      }
    },true);
  }

  function tick(){
    build(document.querySelector('button.myst-search-bar'));
  }
  function start(){
    tick();
    // React hydration replaces these nodes, so keep re-checking for a while
    var n=0,iv=setInterval(function(){tick();if(++n>40)clearInterval(iv);},250);
    new MutationObserver(function(){tick();}).observe(
      document.documentElement,{subtree:true,childList:true});
  }
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',start);
  }else{start();}
})();
"""

# The marker embeds a hash of the runtime, so editing the code above is
# enough to make the next patch run replace an older injected copy.
INLINER_MARK = (
    "/*qem-runtime-" + hashlib.sha1(_RUNTIME.encode()).hexdigest()[:8] + "*/"
)
INLINER = INLINER_MARK + _RUNTIME


# Matches the collapsible-section state hook in both the server and client
# bundles (minified variable names differ between them):
#   [s,o]=X.useState(r); useEffect(()=>{n.state==="idle"&&o(r)},[n.state]);
#   let a=fn(e,i,t); return !i.children ...
PATTERN = re.compile(
    r'\[(\w),(\w)\]=([\w$]+(?:\.default)?)\.useState\((\w)\);'
    r'\(0,([\w$]+)\.useEffect\)\(\(\)=>\{(\w)\.state==="idle"&&\2\([^;]*?\)\},'
    r'(\[\6\.state[^\]]*\])\);let (\w)=[\w$]+\([^)]*\);return!(\w)\.c'
)


def toc_targets():
    """The bundles carrying the TOC hook, found by content.

    The theme renames its bundles on every release, so a hardcoded chunk
    name goes stale silently and then fails the build.
    """
    out = []
    cands = [os.path.join(THEME, "build", "index.js")] + sorted(
        glob.glob(os.path.join(THEME, "public", "build", "**", "*.js"),
                  recursive=True))
    for p in cands:
        try:
            src = open(p).read()
        except (OSError, UnicodeDecodeError):
            continue
        if ".level===1||" in src or PATTERN.search(src):
            out.append(p)
    if not out:
        print("no TOC bundle matched; theme version changed, sections stay collapsible")
    return out


def patched(src):
    def repl(m):
        s, o, hook, active, eff, nav, deps, let_var, heading = m.groups()
        keep_open = f'({heading}.level===1||{active})'
        return (
            f'[{s},{o}]={hook}.useState({keep_open});'
            f'(0,{eff}.useEffect)(()=>{{{nav}.state==="idle"&&{o}({keep_open})}},'
            f'{deps});let {let_var}='
            + m.group(0).split(f'let {let_var}=', 1)[1]
        )

    return PATTERN.subn(repl, src)


def main():
    if not os.path.isdir(THEME):
        sys.exit("book-theme template not found; run `myst build` first")
    total = 0
    # dev server: drop the 1-year immutable cache so patched bundles reload
    server_js = os.path.join(THEME, "server.js")
    if os.path.exists(server_js):
        with open(server_js) as f:
            ssrc = f.read()
        fixed = ssrc.replace(
            "{ immutable: true, maxAge: '1y' }", "{ maxAge: '5m' }"
        )
        if fixed != ssrc:
            with open(server_js, "w") as f:
                f.write(fixed)
            print("patched server.js (cache headers)")
    # inject the search runtime into the server-rendered HTML itself; the
    # document is never long-cached, unlike the fingerprinted JS bundles
    import json
    server_bundle = os.path.join(THEME, "build", "index.js")
    with open(server_bundle) as f:
        bsrc = f.read()
    tag = json.dumps("<script>" + INLINER + "</script></body>")
    if INLINER_MARK in bsrc:
        print("already patched: build/index.js (search runtime)")
    elif "qem-runtime" in bsrc:  # older runtime: swap it out
        new_bsrc, n = re.subn(
            r'"<script>[^"]*qem-runtime[^"]*</script></body>"',
            lambda m: tag,
            bsrc,
        )
        with open(server_bundle, "w") as f:
            f.write(new_bsrc)
        total += n
        print(f"updated build/index.js runtime ({n} site)")
    else:
        new_bsrc, n = re.subn(
            r'new Response\("<!DOCTYPE html>"\+(\w+),',
            lambda m: (
                'new Response("<!DOCTYPE html>"+'
                f'{m.group(1)}.replace("</body>",{tag}),'
            ),
            bsrc,
        )
        if n == 0:
            sys.exit("SSR injection point not found; theme version changed?")
        with open(server_bundle, "w") as f:
            f.write(new_bsrc)
        total += n
        print(f"patched build/index.js (search runtime, {n} site)")
    # rename the patched entry + manifest so browsers that cached the stock
    # bundles (1-year immutable) fetch the patched versions
    # Rename the patched entry + manifest so browsers that cached the stock
    # bundles (1-year immutable) fetch the patched versions. The stock names
    # carry the theme's own content hashes, so discover them instead of
    # hardcoding: a theme update changes the hash, and a hardcoded name then
    # fails the build.
    import glob, shutil
    pub = os.path.join(THEME, "public", "build")
    new_entry, new_manifest = "entry.client-QEMRT1", "manifest-QEMRT1"
    if not os.path.exists(os.path.join(pub, f"{new_entry}.js")):
        rename = []
        for stem, new in (("entry.client-", new_entry), ("manifest-", new_manifest)):
            hits = [f for f in sorted(glob.glob(os.path.join(pub, stem + "*.js")))
                    if os.path.basename(f)[:-3] != new]
            if len(hits) == 1:
                rename.append((os.path.basename(hits[0])[:-3], new))
        if len(rename) == 2:
            for old, new in rename:
                shutil.copyfile(
                    os.path.join(pub, f"{old}.js"), os.path.join(pub, f"{new}.js")
                )
            for path in [os.path.join(THEME, "build", "index.js"),
                         os.path.join(pub, f"{new_manifest}.js")]:
                with open(path) as f:
                    s = f.read()
                for old, new in rename:
                    s = s.replace(old, new)
                with open(path, "w") as f:
                    f.write(s)
            print("renamed entry.client + manifest (cache bust)")
        else:
            print("skipped cache-bust rename: stock bundle names not found")

    for path in toc_targets():
        with open(path) as f:
            src = f.read()
        if ".level===1||" in src:
            print(f"already patched: {os.path.relpath(path, THEME)}")
            continue
        out, n = patched(src)
        if n == 0:
            print(f"pattern not found in {path}; theme version changed?")
            continue
        with open(path, "w") as f:
            f.write(out)
        total += n
        print(f"patched {os.path.relpath(path, THEME)} ({n} site)")
    print(f"done ({total} replacements)")


if __name__ == "__main__":
    main()

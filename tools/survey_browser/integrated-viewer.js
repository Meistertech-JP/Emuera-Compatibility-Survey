
(() => {
'use strict';
const data = JSON.parse(document.querySelector('#data').textContent);
const texts = data.native.texts;
const saved = data.saved;
const frozen = data.frozenResults?.records || [];
const frozenByCase = new Map(frozen.map(row => [row.id,row]));
const readableCases = new Set(saved.coverage.caseIds);
const savedByCase = group(saved.records, row => [row.id]);
const savedByTarget = group(saved.records, row => row.roles.map(role => role.kind + ':' + role.name));
let lang = 'ja';

function evidenceLink(path) {
    const parts = path.split('/');
    if (parts.some(part => !part || part === '..' || part === '.' || /[:\\]/.test(part))) {
        throw new Error('Invalid evidence path');
    }
    return '../' + parts.map(encodeURIComponent).join('/');
}

/* NATIVE_RENDERER */

const renderNative = card;
const labels = {
    ja: {
        title:'Emuera命令リファレンスと互換性調査', intro:'機能・書き方・期待される効果を読み、本家EmueraとPyEmueraの保存結果や根拠を確認できます。',
        scope:'694対象、主2,898シナリオ、構文114ケース、補助16項目。旧形式226対象は694対象の内数です。実行結果は同梱された保存資料の範囲で表示します。',
        tabs:['対象','シナリオ','構文','補助調査','旧形式','保存実行結果'], search:'対象名・ケースID・出力を検索',
        verdict:'判定', kind:'対象種別', genre:'機能ジャンル', all:'すべて', more:'さらに表示', requirements:'検証要件', cases:'関連ケース',
        related:'関連対象', evidence:'証拠資料', native:'本家・PyEmueraの保存実行結果', recovery:'選定された条件・観測と制限',
        none:'このケースに直接結び付く保存出力は、このページの収録資料では確認できません。',
        legacy:'原本の参照数 / 収録原本と派生結果の参照数', links:'収録原本と派生結果', gaps:'照合上の制約',
        modes:'登録モード', families:'構文分類', unclassified:'判定の記録なし',
        records:{correction:'訂正後の観測',projection:'保存記録の抜粋',supplement:'既存ケースの観測補足'},
        verdicts:{matched_in_finite_scope:'有限範囲で一致',matched_scoped:'局所一致',documented_difference:'記録済み差異',different_scoped:'範囲付き差異',unverified:'未検証',blocked:'中断・証拠不備等',mismatch:'不一致',not_recorded:'判定の記録なし'},
        kinds:['命令・構文','式関数','メソッドの命令形式','構造構文','演算子','代入構文','宣言','宣言修飾子'],
    },
    en: {
        title:'Emuera reference and compatibility survey', intro:'Read what each target does, how to write it, and its expected effects, then inspect saved Native Emuera and PyEmuera results and sources.',
        scope:'694 targets, 2,898 main scenarios, 114 grammar cases, and 16 supplemental items. The 226 legacy targets are part of the 694. Execution results are limited to the saved evidence included here.',
        tabs:['Targets','Scenarios','Grammar','Supplemental','Legacy','Saved execution results'], search:'Search targets, case IDs, or output',
        verdict:'Verdict', kind:'Target kind', genre:'Genre', all:'All', more:'Show more', requirements:'Verification requirements', cases:'Related cases',
        related:'Related targets', evidence:'Evidence guides', native:'Saved Native Emuera and PyEmuera results', recovery:'Selected conditions, observations, and limits',
        none:'The records in this page do not include saved output directly linked to this case.',
        legacy:'Original references / included originals and derived observations', links:'Included originals and derived observations', gaps:'Verification gaps',
        modes:'Registered modes', families:'Grammar families', unclassified:'No verdict recorded',
        records:{correction:'Corrected observation',projection:'Excerpt from saved record',supplement:'Additional observation for an existing case'},
        verdicts:{matched_in_finite_scope:'Match in finite scope',matched_scoped:'Scoped match',documented_difference:'Documented difference',different_scoped:'Scoped difference',unverified:'Unverified',blocked:'Interrupted or insufficient evidence',mismatch:'Mismatch',not_recorded:'No verdict recorded'},
        kinds:['Command/syntax','Expression function','Method as command','Structural syntax','Operator','Assignment syntax','Declaration','Declaration modifier'],
    },
};
const kinds = ['command_or_syntax','expression_function','method_as_command','structural_syntax',
    'operator','assignment_syntax','declaration','declaration_modifier'];
const savedIds = [...new Set([...saved.coverage.caseIds, ...frozenByCase.keys(), ...data.native.rows.map(row => row.id)])];
const sections = [data.targets,data.scenarios,data.grammar,data.supplemental,data.legacy,
    savedIds.map(id => ({id, i:id, v:byCaseVerdict(id)}))];
const verdictOf = row => row.o ?? row.v ?? row.verdict ?? row.scenario_verdict ?? row.comparison_outcome ?? row.comparison ?? '';
const typed = (kind, name) => kind + ':' + name;
const get = id => document.getElementById(id);
const legacyAudit = new Map((data.frozenResults?.legacy || []).map(row =>
    [typed(row.kind,row.name), row]));
const targetByKey = new Map(data.targets.map(row => [typed(row.k,row.n),row]));
const genreList = [...(data.genres || [])].sort((a,b) => a.order - b.order);
const genreCounts = new Map(genreList.map(genre => [genre.id,0]));
for (const row of data.targets) for (const id of [row.g,...row.sg])
    genreCounts.set(id,(genreCounts.get(id) || 0) + 1);
function genresOf(row) {
    const target = row.g !== undefined ? row : targetByKey.get(typed(row.k,row.n));
    return target && target.g !== undefined ? [target.g,...target.sg] : [];
}
function byCaseVerdict(id) {
    return [...data.scenarios, ...data.grammar, ...data.supplementalModes]
        .find(row => (row.i ?? row.case_id) === id)?.v;
}
const byId = new Map([...data.scenarios, ...data.grammar, ...data.supplementalModes].map(row => [row.i ?? row.case_id, row]));
const nativeByCase = group(data.native.rows, row => [row.id]);
const recoveryByCase = group(data.recovery, row => [row.id]);
const nativeByTarget = group(data.native.rows, row => row.roles.map(role => typed(role.kind,role.name)));
const recoveryByTarget = group(data.recovery, row => row.roles.map(role => typed(role.kind,role.name)));

function group(rows, keys) {
    const result = new Map();
    for (const row of rows) {
        for (const key of new Set(keys(row))) {
            if (!result.has(key)) result.set(key, []);
            result.get(key).push(row);
        }
    }
    return result;
}
function related(map, ids, typedMap, key) {
    return [...new Set([...(typedMap.get(key) || []), ...ids.flatMap(id => map.get(id) || [])
        .filter(row => row.roles.length === 0 || row.roles.some(role => typed(role.kind,role.name) === key))])];
}
function disclosure(title, rows, render) {
    const details = el('details');
    details.append(el('summary',title + ' (' + rows.length + ')'));
    details.addEventListener('toggle', () => {
        if (details.open && details.children.length === 1) {
            details.append(...rows.map(render));
        }
    });
    return details;
}
function renderRecovery(row) {
    const article = el('article');
    article.append(el('h3',row.id + ' · ' + labels[lang].records[row.type]));
    for (const [field, value] of Object.entries(row.fields)) {
        const title = (lang === 'ja' ? {
            recovered:'保存観測', recovered_context:'実行条件', limitations:'観測の制限',
            observations:'観測値', fixtures_and_initial_state:'入力・初期状態'
        } : {
            recovered:'Saved observations', recovered_context:'Run conditions', limitations:'Observation limits',
            observations:'Observed values', fixtures_and_initial_state:'Inputs and initial state'
        })[field] || field;
        article.append(el('h3',title), el('pre',fmt(value)));
    }
    return article;
}
function renderObservation(row) {
    const article = renderNative(row);
    for (const mode of row.native) {
        for (const asset of mode.assets.filter(asset => asset.role.startsWith('image'))) {
            const details = el('details');
            details.append(el('summary',mode.mode + ' · ' + (lang === 'ja' ? '保存画面' : 'Saved capture')));
            details.addEventListener('toggle', () => {
                if (details.open && details.children.length === 1) {
                    const image = el('img');
                    const path = 'evidence/native-oracle-20261117/' + asset.path;
                    image.src = evidenceLink(path);
                    image.alt = row.id + ' · ' + asset.role;
                    details.append(imageActions(
                        {src:image.src,id:row.id,type:mode.mode + ' · Native',role:asset.role,path},image));
                }
            });
            article.append(details);
        }
    }
    return article;
}
function renderSaved(row) {
    const article = el('article');
    const ja = lang === 'ja';
    article.append(el('h3',row.id + ' · ' + row.source.split('/')[1]));
    if (row.shared) article.append(el('p',ja
        ? '複数ケースで共有した実行の記録です。ログ全体がこのケース固有の出力であるとは限りません。'
        : 'This run was shared by multiple cases. The full log may include output from other cases.'));
    for (const [field,value] of Object.entries(row.fields)) {
        if (value === null || value === '') continue;
        article.append(el('h3',field),el('pre',fmt(value)));
    }
    if (row.assets.length) article.append(disclosure(
        ja ? '出力・診断・画面' : 'Output, diagnostics, and captures',row.assets,asset => {
            const block = el('div');
            block.append(el('h3',[asset.mode,asset.role].filter(Boolean).join(' · ')));
            if (asset.image) {
                const image = el('img');
                image.loading = 'lazy';
                image.src = evidenceLink(asset.path);
                image.alt = row.id + ' · ' + asset.role;
                block.append(imageActions(
                    {src:image.src,id:row.id,type:row.source.split('/')[1],role:asset.role,path:asset.path},image));
            } else block.append(el('pre',saved.texts[asset.sha256]));
            block.append(anchor(asset.path,ja ? '元ファイル' : 'Original file'),
                el('p','SHA-256 ' + asset.sha256 + (asset.encoding ? ' · ' + asset.encoding : '')));
            return block;
        }));
    article.append(anchor(row.source,ja ? '出典の記録' : 'Source record'));
    return article;
}
function renderFrozen(row) {
    const article = el('article');
    const ja = lang === 'ja';
    article.append(el('h3',row.id));
    if (row.observation) {
        const title = row.followup
            ? (ja ? '保存ログ・比較票から確認した結果' : 'Results verified against saved logs and comparison records')
            : (ja ? '調査台帳に記録された観測・比較' : 'Observation or comparison recorded in the survey register');
        article.append(el('h3',title),el('pre',fmt(row.observation)));
    }
    for (const result of row.excerpts) {
        article.append(el('h3',[result.engine,result.mode,result.file].filter(Boolean).join(' · ')),
            el('pre',result.text),el('p','SHA-256 ' + result.sha256));
    }
    if (row.limits) article.append(el('p',row.limits));
    article.append(el('p',(ja ? '凍結ケース台帳 SHA-256 ' : 'Frozen case register SHA-256 ') + row.registry_sha256));
    return article;
}
function addObservations(article, native, recovery, showEmpty = true, extra = [], ids = []) {
    const d = labels[lang];
    if (native.length) article.append(disclosure(d.native,native,renderObservation));
    if (recovery.length) article.append(disclosure(d.recovery,recovery,renderRecovery));
    if (extra.length) article.append(disclosure(lang === 'ja' ? '追加の保存実行結果' : 'Additional saved results',extra,renderSaved));
    const actualRecovery = recovery.some(row => readableCases.has(row.id));
    const recovered = [...new Set(ids)].map(id => frozenByCase.get(id)).filter(Boolean);
    if (recovered.length) article.append(disclosure(
        lang === 'ja' ? '原調査から回収した観測・ログ抜粋' : 'Recovered observations and log excerpts',recovered,renderFrozen));
    if (showEmpty && !native.length && !extra.length && !actualRecovery && !recovered.length) article.append(el('p',d.none));
}
function anchor(path, text) {
    const link = el('a',text);
    link.href = evidenceLink(path);
    return link;
}
let pinned = null;
function pinImage(meta, source) {
    pinned = {...meta, source};
    get('pinZoom').value = '100';
    renderPin();
}
function renderPin() {
    const panel = get('pinPanel');
    document.body.classList.toggle('pin-open',Boolean(pinned));
    panel.hidden = !pinned;
    if (!pinned) return;
    get('pinImage').src = pinned.src;
    get('pinImage').alt = pinned.id + ' · ' + pinned.role;
    get('pinImage').style.width = get('pinZoom').value + '%';
    get('pinTitle').textContent = pinned.id;
    get('pinMeta').textContent = [pinned.type,pinned.role].filter(Boolean).join(' · ');
    get('pinFile').replaceChildren(anchor(pinned.path,bilingual('元ファイル','Original file')));
    get('pinClose').textContent = bilingual('固定解除','Unpin');
    const collapsed = panel.classList.contains('collapsed');
    get('pinToggle').textContent = collapsed ? bilingual('展開','Expand') : bilingual('折りたたむ','Collapse');
    get('pinZoomLabel').textContent = bilingual('表示サイズ','Size');
    get('pinLocate').textContent = bilingual('本文で確認','Show in text');
}
function relinkPin() {
    if (!pinned?.source || pinned.source.isConnected) return;
    const wanted = pinned.id + ' · ' + pinned.role;
    pinned.source = [...get('results').querySelectorAll('img')]
        .find(image => image.src === pinned.src && image.alt === wanted) || pinned.source;
}
function syncMenuPin() {
    const fixed = document.body.classList.contains('menu-fixed');
    const button = get('menuPin');
    button.textContent = fixed ? bilingual('メニュー固定中','Menu pinned')
                               : bilingual('メニューを固定','Pin menu');
    button.setAttribute('aria-pressed',String(fixed));
    const style = document.documentElement.style;
    const controlsBottom = Math.ceil(get('topControls').getBoundingClientRect().bottom);
    style.setProperty('--controls-clearance',(controlsBottom + 10) + 'px');
    if (fixed) style.setProperty('--pin-top',
        'calc(' + (get('searchBar').offsetHeight + 8) + 'px + .4rem)');
    else style.removeProperty('--pin-top');
    try { localStorage.setItem('survey-menu-pinned',fixed ? '1' : '0'); }
    catch (error) { /* storage may be unavailable offline or restricted; keep normal operation */ }
}
function stickyTop() {
    return document.body.classList.contains('menu-fixed')
        ? get('searchBar').offsetHeight + 8 : 0;
}
function imageActions(meta, image) {
    const box = el('div');
    const pin = el('button',bilingual('画像を固定','Pin image'));
    pin.type = 'button';
    pin.className = 'pin-actions';
    pin.addEventListener('click', () => pinImage(meta,image));
    box.append(image,pin);
    return box;
}
function jump(section, term, title) {
    const button = el('button',title);
    button.type = 'button';
    button.addEventListener('click', () => {
        selectSection(section, term);
        get('search').focus();
    });
    return button;
}
function caseEntry(id, section) {
    const row = byId.get(id);
    const item = el('p');
    item.append(jump(section,id,id));
    if (row) item.append(' · ' + verdictLabel(verdictOf(row)));
    return item;
}
function verdictLabel(code) {
    const d = labels[lang];
    return d.verdicts[code] || code || d.unclassified;
}
function showLegacy(article,row) {
    const ja = lang === 'ja';
    const d = labels[lang];
    const key = typed(row.k,row.n);
    const audit = legacyAudit.get(key);
    const cases = [...new Set([...(audit?.case_ids || []), ...(targetByKey.get(key)?.c || [])])];
    if (audit) {
        const statuses = ja ? {
            pin_verified:'凍結資料の監査で受入原票のSHA-256を照合済み',
            pin_not_verified:'受入原票のSHA-256を確認できなかった',
            not_directly_linked:'受入原票への直接参照なし',
        } : {
            pin_verified:'Acceptance record SHA-256 verified during the frozen-source audit',
            pin_not_verified:'Acceptance record SHA-256 could not be verified',
            not_directly_linked:'No direct acceptance record reference',
        };
        article.append(el('p',statuses[audit.accepted]));
        if (audit.decision) article.append(el('p',(ja ? '受入の記録' : 'Recorded decision') + ' · ' + audit.decision));
        if (audit.sha256) article.append(el('p','SHA-256 ' + audit.sha256));
        if (audit.readbacks.length) article.append(disclosure(ja ? '照合済みの読戻し資料' : 'Verified readback records',
            audit.readbacks, ref => el('p',[ref.schema_or_adapter,ref.sha256].filter(Boolean).join(' · '))));
    }
    const known = cases.filter(id => readableCases.has(id) || frozenByCase.has(id));
    article.append(el('p',ja ? '関連ケースの保存結果 ' + known.length + ' / ' + cases.length
        : 'Related cases with saved results: ' + known.length + ' / ' + cases.length));
    if (cases.length) article.append(disclosure(d.cases,cases,id => caseEntry(id,1)));
    for (const id of known) {
        const native = nativeByCase.get(id) || [];
        const recovery = recoveryByCase.get(id) || [];
        const extra = savedByCase.get(id) || [];
        const frozenResult = frozenByCase.get(id);
        const item = el('div');
        item.append(el('h3',id));
        addObservations(item,native,recovery,false,extra,frozenResult ? [id] : []);
        article.append(item);
    }
}
const sourceById = new Map(data.referenceSources.sources.map(s => [s.id,s]));
const localized = value => typeof value === 'string' ? value : (value?.[lang] || '');
function bilingual(ja,en) { return lang === 'ja' ? ja : en; }
function syntaxOf(ref) { return lang === 'en' ? (ref.syntax_en || ref.syntax) : ref.syntax; }
function checkpointRuns(value,result=[],depth=0) {
    if(!value || typeof value !== 'object' || depth>12 || result.length>=12)return result;
    if(Array.isArray(value.runs)) for(const run of value.runs) {
        if(run && /^(?:native(?:-|$)|public$)/.test(run.mode || '') &&
           (typeof run.done==='boolean' || run.error?.code))result.push(run);
        if(result.length>=12)break;
    }
    for(const [key,child] of Object.entries(value))if(key!=='runs')checkpointRuns(child,result,depth+1);
    return result;
}
function comparisonDigest(row) {
    const block=el('section');block.className='comparison-digest';
    const cases=row.c.map(id=>({id,verdict:verdictOf(byId.get(id) || {})}));
    const counts=new Map();
    for(const c of cases)counts.set(c.verdict,(counts.get(c.verdict)||0)+1);
    block.append(el('h4',bilingual('条件別の保存判定','Recorded case-level verdicts')),
        el('p',[...counts].map(([v,n])=>verdictLabel(v)+' '+n).join(' · ')),
        el('p',bilingual('対象全体の判定と各条件の判定は単位が異なります。以下は保存記録の参照案内で、独立不具合数や新たな実行結果ではありません。',
            'The target-wide verdict and individual case verdicts have different scopes. This is a guide to saved records, not a count of independent bugs or new executions.')));
    const differences=cases.filter(c=>['documented_difference','different_scoped','mismatch'].includes(c.verdict));
    if(differences.length) {
        const preview=disclosure(bilingual('差異のある条件を先に確認','Inspect differing conditions first'),differences.slice(0,8),c=> {
            const part=el('section');part.className='comparison-case';
            part.append(el('h4',c.id+' · '+verdictLabel(c.verdict)));
            const runs=checkpointRuns(frozenByCase.get(c.id)?.observation);
            if(runs.length) {
                part.append(el('p',bilingual('保存記録の完了欄と診断の抜粋（doneと自然終了は別）',
                    'Saved completion fields and diagnostics (done is distinct from natural exit)')));
                const table=el('table');const header=el('tr');
                for(const h of [bilingual('実装・モード','Engine / mode'),bilingual('記録された結果','Recorded result')])header.append(el('th',h));
                table.append(header);
                for(const run of runs) {
                    const tr=el('tr');
                    tr.append(el('td',(run.mode==='public'?'PyEmuera 3.0.0':'Native Emuera1824+v24')+' · '+run.mode));
                    const text=[];
                    if(typeof run.done==='boolean')text.push(bilingual('完了欄 (done): ','Recorded done: ')+String(run.done));
                    if(run.error?.code)text.push(bilingual('診断: ','Diagnostic: ')+run.error.code+(run.error.line?' · '+bilingual('行 ','line ')+run.error.line:'')+(run.error.body?' · '+String(run.error.body).slice(0,500):''));
                    if(run.native_exit_semantics)text.push(bilingual('終了方法の原記録: ','Recorded exit semantics: ')+run.native_exit_semantics);
                    tr.append(el('td',text.join(' / ')));table.append(tr);
                }
                part.append(table);
            } else part.append(el('p',bilingual('この要約欄へ転記できるdone・診断の欄はありません。値や差異の内容はケースの保存結果で確認してください。',
                'No done or diagnostic fields are available for this preview. Open the case records for its values and differences.')));
            part.append(jump(1,c.id,bilingual('この条件の保存結果を開く','Open saved results for this condition')));
            return part;
        });
        block.append(preview);preview.open=true;
        if(differences.length>8)block.append(el('p',bilingual('先頭8条件を表示しています。他の条件は関連ケースから開けます。',
            'The first eight conditions are previewed. Open other conditions from Related cases.')));
    }
    return block;
}
function sourceCitations(ref, field) {
    const sources = (ref.sources || []).filter(s => !field || !s.fields || s.fields.includes(field));
    return disclosure(bilingual('説明の根拠','Sources for this explanation'),sources,s => {
        const box = el('div');
        const source = sourceById.get(s.source_id);
        box.append(el('p',s.classification + ' · ' + (source?.title || s.source_id)));
        if (s.viewer_path) {
            const a = anchor(s.viewer_path, s.path + ':' + s.start_line + '–' + s.end_line);
            a.href += '#L' + s.start_line;
            box.append(a);
        } else if (s.url || s.section_url || source?.mirror_or_archive_url || source?.original_url) {
            const a = el('a',bilingual('外部資料（出典の確認）','External source (reference only)'));
            a.href = s.url || s.section_url || source.mirror_or_archive_url || source.original_url;
            if (s.anchor && !a.href.includes('#')) a.href += '#' + s.anchor;
            a.rel = 'noreferrer'; box.append(a);
        }
        if (s.section) box.append(el('p',bilingual('参照節: ','Section: ') + s.section));
        if (s.member_sha256) box.append(el('p','SHA-256 ' + s.member_sha256));
        box.append(el('p',localized(source?.documented_version)),el('p',s['note_' + lang] || ''));
        box.append(el('p',bilingual('確認時点: ','Checked at: ') + (source?.checked_at || bilingual('記録なし','not recorded')) +
            ' · ' + bilingual('権利: ','Rights: ') + (source?.license?.identifier || source?.license?.status || bilingual('個別の出典参照','see source record'))));
        if (source?.snapshot_timestamp) box.append(el('p',bilingual('実取得した保存日時（UTC）: ','Retrieved archive capture (UTC): ') + source.snapshot_timestamp));
        return box;
    });
}
function renderReference(row) {
    const ref = row.ref, body = el('div'); body.className = 'target-detail';
    const heading = (title, field) => {
        body.append(el('h3',title));
        if (field) body.append(sourceCitations(ref,field));
    };
    heading(bilingual('機能と使用方法','Function and usage'),'summary');
    body.append(el('p',localized(ref.summary)));
    heading(bilingual('構文','Syntax'),'syntax');
    for (const form of syntaxOf(ref)) body.append(el('pre',form));
    if (!ref.syntax.length) for (const u of ref.unconfirmed || []) body.append(el('p','UNCONFIRMED · ' + localized(u)));
    if (ref.parameters.length) {
        heading(bilingual('引数・パラメーター','Arguments and parameters'),'parameters');
        for (const p of ref.parameters) {
            const block = el('p');
            block.append(el('strong',p.name + ' · ' + p.type + (p.optional ? bilingual('（省略可）',' (optional)') : '') + ' '),localized(p));
            body.append(block);
        }
    }
    body.append(el('p',localized(ref.usage)), sourceCitations(ref,'usage'));
    heading(bilingual('使用例と通常期待される結果','Examples and expected effects'),'examples');
    if (!ref.examples.length) for (const u of ref.unconfirmed || []) body.append(el('p','UNCONFIRMED · ' + localized(u)));
    for (const ex of ref.examples) {
        const box = el('section'); box.className = 'example';
        box.append(el('p','EXAMPLE_DERIVED · ' + localized(ex.context)),el('pre',ex.erb),
            el('h4',bilingual('通常期待される結果（実機観測とは別）','Expected effect (separate from a runtime observation)')),
            el('p',localized(ex.expected)));
        if (ex.verification) box.append(el('p',bilingual('例の確認方法: ','Example validation: ') +
            localized(ex.verification.method) + ' · ' + (ex.verification['detail_' + lang] || '')));
        box.append(sourceCitations({sources:ex.source_refs.map(s=>({...s,classification:s.classification || 'SOURCE_CONFIRMED'}))}));
        body.append(box);
    }
    heading(bilingual('戻り値・副作用・状態変化','Return value, side effects, and state'),'effects');
    body.append(el('p',localized(ref.effects)));
    if (ref.related.length) {
        heading(bilingual('関連する対象','Related targets'));
        for (const t of ref.related) {
            if (targetByKey.has(typed(t.kind,t.name))) body.append(jump(0,typed(t.kind,t.name),t.name + ' · ' + (labels[lang].kinds[kinds.indexOf(t.kind)] || t.kind)));
        }
    }
    heading(bilingual('互換性の確認状況','Recorded compatibility'));
    body.append(el('p',bilingual('本家1824+v24とPyEmuera 3.0.0の比較判定: ','Native 1824+v24 versus PyEmuera 3.0.0: ') + verdictLabel(row.o)),
        el('p',localized(ref.limits)));
    body.append(comparisonDigest(row));
    if (ref.unconfirmed?.length) for (const u of ref.unconfirmed) body.append(el('p','UNCONFIRMED · ' + u.field + ' · ' + localized(u)));
    body.append(el('p',bilingual('以下は既存の実行で得られた保存観測です。上の独自例の実行結果を示すものではありません。共有実行・抜粋・未観測の条件は各記録で区別します。',
        'The records below are saved observations from earlier runs, not executions of the derived examples above. Shared runs, excerpts, and unobserved conditions are distinguished in each record.')));
    const key = typed(row.k,row.n);
    addObservations(body,related(nativeByCase,row.c,nativeByTarget,key),
        related(recoveryByCase,row.c,recoveryByTarget,key),true,related(savedByCase,row.c,savedByTarget,key),row.c);
    if (row.c.length) body.append(disclosure(labels[lang].cases,row.c,id=>caseEntry(id,1)));
    body.append(el('h3',labels[lang].requirements));
    body.append(disclosure(labels[lang].requirements,row.r,r => {
        const part = el('section'); part.className = 'requirement';
        part.append(el('h4',r.i));
        if (r.note) {
            const note=el('aside'); note.className='source-note';
            note.append(el('h4',bilingual('原要件を読む際の注記','Note on the historical requirement')),
                el('p',localized(r.note)),sourceCitations({sources:r.note.source_refs}));
            part.append(note);
        }
        part.append(el('p',lang === 'ja' ? r.plain : r.t));
        if (lang === 'ja') part.append(el('h4','日本語訳'),el('p',r.ja));
        const original = el('details'); original.append(el('summary',bilingual('英語原文と出典属性','Original English and source attributes')),
            el('p',r.t),el('p',r.status + ' · original_text_sha256: ' + r.hash + ' · derived_text_sha256: ' + r.derivedHash));
        part.append(original);
        for (const role of r.roles) {
            const p = el('p');
            const caseId = r.caseLinks[role.case];
            if (caseId) p.append(jump(1,caseId,caseId + ' (' + role.case + ')'));
            else p.append(el('code',role.case),bilingual('（要件原票の識別子。公開ケースIDとの個別対応表なし）',
                ' (requirement-source alias; no individual mapping to a public case ID)'));
            p.append(' · ' + role.field + ' · ' + role.role);
            part.append(p);
        }
        return part;
    }));
    body.append(el('h3',labels[lang].evidence),el('p',bilingual('fixture・入力・設定・環境・原出力・画像・SHA-256は、保存結果の各欄および次の資料から確認できます。',
        'Fixtures, inputs, settings, environments, original output, images, and SHA-256 values are available in the result sections and the following evidence guides.')));
    if (row.ev.length) body.append(disclosure(labels[lang].evidence,row.ev,entry => {
        const p = el('p'); p.append(anchor(lang === 'ja' ? entry.j : entry.e,entry.c)); return p;
    }));
    body.append(anchor('reference/SOURCES' + (lang === 'ja' ? '_ja' : '') + '.md',bilingual('文献の来歴・版・権利・取得上の制限','Literature provenance, versions, rights, and retrieval limits')));
    return body;
}

function normalCard(row) {
    const d = labels[lang];
    const article = el('article');
    const name = row.n ?? row.i ?? row.case_id ?? row.id;
    const badge = el('span',verdictLabel(verdictOf(row)));
    badge.className = 'badge';
    article.append(el('h2',name),badge);
    if (row.k) article.append(' · ' + (d.kinds[kinds.indexOf(row.k)] || row.k));
    if (section === 0) {
        article.dataset.target = typed(row.k,row.n);
        article.append(el('p',localized(row.ref.summary)),el('code',syntaxOf(row.ref)[0] || bilingual('直接呼出し構文は未確定','No direct invocation syntax established')),
            el('p',d.cases + ': ' + row.c.length));
        const detail = el('details'); detail.className = 'reference-detail';
        detail.append(el('summary',bilingual('使い方・期待結果・比較・証拠を読む','Read usage, expected effects, comparisons, and evidence')));
        detail.addEventListener('toggle', () => {
            if (detail.open && detail.children.length === 1) detail.append(renderReference(row));
        });
        article.append(detail);
        if (get('search').value.trim().toLowerCase() === row.n.toLowerCase() ||
            get('search').value.trim().toLowerCase() === typed(row.k,row.n).toLowerCase()) detail.open = true;
    } else if (section === 4) {
        article.append(el('p',d.legacy + ' · ' + row.op + ' / ' + row.cp.length));
        article.append(el('p',Object.entries(row.classes).map(([name,count]) => name + ' ' + count).join(' · ')));
        if (row.s) article.append(el('p',row.s));
        if (row.g.length) article.append(disclosure(d.gaps,row.g,code => el('p',code)));
        if (row.cp.length) article.append(disclosure(d.links,row.cp,entry => {
            const paragraph = el('p');
            paragraph.append(anchor(entry.p,entry.p));
            if (entry.view) paragraph.append(el('br'),anchor(entry.view,lang==='ja' ? 'HTMLで全文を表示' : 'Read the full artifact in HTML'));
            if (entry.m.length) paragraph.append(el('span',' › ' + entry.m.join(' › ')));
            if (entry.sha) paragraph.append(el('code',' SHA-256 ' + entry.sha));
            for (const match of entry.derived) {
                paragraph.append(el('br'),jump(1,match.case_id,match.case_id),el('code',' ' + match.pointer));
            }
            return paragraph;
        }));
        if (row.withheld?.length) article.append(disclosure(lang==='ja' ? '非公開の具体的な理由' : 'Reasons for withholding originals',row.withheld,entry => {
            const paragraph=el('p',entry.id+' · '+entry.reason+' ');
            paragraph.append(anchor(entry.view,lang==='ja' ? '個別審査' : 'Individual review'));
            return paragraph;
        }));
        showLegacy(article,row);
        article.append(jump(0,typed(row.k,row.n),d.tabs[0] + ' · ' + row.n));
    } else if (section === 3) {
        const modes = data.supplementalModes.filter(mode => mode.work_item_ids.includes(row.id));
        article.append(disclosure(d.modes,modes,mode => {
            const item = el('article');
            item.append(el('h3',mode.case_id),el('p',verdictLabel(verdictOf(mode))));
            addObservations(item,nativeByCase.get(mode.case_id) || [],recoveryByCase.get(mode.case_id) || [],true,savedByCase.get(mode.case_id) || []);
            return item;
        }));
    } else {
        if (row.t?.length) article.append(disclosure(d.related,row.t,role => {
            const key = typed(role.kind,role.name);
            return jump(0,key,key);
        }));
        if (row.grammar_family_ids) {
            article.append(el('p',d.modes + ' · ' + row.case_mode_count));
            article.append(el('p',d.families + ' · ' + row.grammar_family_ids.join(', ')));
        }
        addObservations(article,nativeByCase.get(name) || [],recoveryByCase.get(name) || [],true,savedByCase.get(name) || [],[name]);
    }
    return article;
}
const nativeSearch = new Map(data.native.rows.map(row => [row, JSON.stringify(row).toLowerCase() + ' ' +
    row.roles.map(role => typed(role.kind,role.name)).join(' ').toLowerCase() + ' ' +
    [...row.native,...row.py].flatMap(mode => mode.assets.map(asset => texts[asset.sha256] || '')).join('\n').toLowerCase()]));
const resultSearch = new Map(sections[5].map(row => [row, [
    row.id,
    ...(nativeByCase.get(row.id) || []).map(native => nativeSearch.get(native)),
    ...(savedByCase.get(row.id) || []).flatMap(result => [
        JSON.stringify(result.fields),
        result.roles.map(role => typed(role.kind,role.name)).join(' '),
        ...result.assets.map(asset => saved.texts[asset.sha256] || ''),
    ]),
    ...(recoveryByCase.get(row.id) || []).map(result => JSON.stringify(result.fields)),
    JSON.stringify(frozenByCase.get(row.id) || ''),
    ...(byId.get(row.id)?.t || []).map(role => typed(role.kind,role.name)),
].join(' ').toLowerCase()]));
let section = 0, matches = [], shown = 0;
const targetSearch = new Map(data.targets.map(row => [row,{
    name:row.n.toLowerCase(), typed:typed(row.k,row.n).toLowerCase(),
    related:JSON.stringify(row.ref.related).toLowerCase(),
    explanation:JSON.stringify([row.ref.summary,row.ref.syntax,row.ref.syntax_en,row.ref.usage,row.ref.parameters,row.ref.effects,row.ref.examples]).toLowerCase(),
    detail:JSON.stringify([row.r,row.c,row.ev]).toLowerCase(),
}]));
function searchRank(row, query) {
    const x = targetSearch.get(row);
    if (!x) return 6;
    if (x.name === query || x.typed === query) return 0;
    if (x.name.startsWith(query)) return 1;
    if (x.name.includes(query)) return 2;
    if (x.related.includes(query)) return 3;
    if (x.explanation.includes(query)) return 4;
    return 5;
}

function setOptions(select, options) {
    const previous = select.value;
    select.replaceChildren(...options.map(([value,text]) => {
        const option = el('option',text);
        option.value = value;
        return option;
    }));
    select.value = options.some(([value]) => value === previous) ? previous : '*';
}
function selectSection(index, term) {
    section = index;
    if (term !== undefined) get('search').value = term;
    get('kind').value = '*';
    get('verdict').value = '*';
    get('genre').value = '*';
    localize();
}
function localize(limit=30) {
    const d = labels[lang];
    document.documentElement.lang = lang;
    document.title = d.title;
    for (const id of ['title','intro','scope','more']) get(id).textContent = d[id];
    get('referenceHelp').textContent = bilingual('使い方・情報の区分・再生成方法','Usage, evidence classes, and regeneration');
    get('referenceHelp').href = '../reference/README' + (lang === 'ja' ? '.ja' : '') + '.md';
    get('glossary').textContent = bilingual('専門用語の対訳','Bilingual glossary');
    get('glossary').href = '../reference/glossary.html';
    const {mainTotal,mainReadable,mainRaw,mainExcerptOnly} = saved.coverage;
    const format = number => number.toLocaleString(lang);
    get('coverage').textContent = lang === 'ja'
        ? '主シナリオ ' + format(mainReadable) + ' / ' + format(mainTotal) + ' 件で実行結果を閲覧できます。ログ本文または画面あり ' + format(mainRaw) + ' 件、観測の抜粋のみ ' + format(mainExcerptOnly) + ' 件。'
        : 'Execution results are readable for ' + format(mainReadable) + ' of ' + format(mainTotal) + ' main scenarios. ' + format(mainRaw) + ' have log text or captures, and ' + format(mainExcerptOnly) + ' have observation excerpts only.';
    if (data.frozenResults) {
        get('coverage').textContent = lang === 'ja'
            ? '主シナリオ ' + format(mainReadable + frozen.length) + ' / ' + format(mainTotal)
              + ' 件で保存された結果を閲覧できます。原ログ・画面や比較票からの抜粋を含みます。'
            : 'Saved results are readable for ' + format(mainReadable + frozen.length) + ' of ' + format(mainTotal)
              + ' main scenarios, including original logs, screen captures, and excerpts from comparison records.';
    }
    get('language').textContent = lang === 'ja' ? 'English' : '日本語';
    get('searchLabel').textContent = d.search;
    get('verdictLabel').textContent = d.verdict;
    get('kindText').textContent = d.kind;
    get('kindLabel').hidden = section !== 0 && section !== 4;
    get('genreText').textContent = d.genre;
    get('genreLabel').hidden = section !== 0 && section !== 4;
    get('tabs').replaceChildren(...d.tabs.map((name,i) => {
        const button = el('button',name + ' (' + sections[i].length.toLocaleString(lang) + ')');
        button.type = 'button';
        button.setAttribute('aria-pressed',String(section === i));
        button.addEventListener('click', () => selectSection(i));
        return button;
    }));
    setOptions(get('kind'),[['*',d.all],...kinds.map((kind,i) => [kind,d.kinds[i]])]);
    setOptions(get('genre'),[['*',d.all],...genreList.map(genre => [genre.id,
        (lang === 'ja' ? genre.ja : genre.en) + ' (' + (genreCounts.get(genre.id) || 0).toLocaleString(lang) + ')'])]);
    const verdicts = [...new Set(sections[section].map(verdictOf))];
    setOptions(get('verdict'),[['*',d.all],...verdicts.map(v => [v,verdictLabel(v)])]);
    search(limit,true);
    renderPin();
    syncMenuPin();
}
function search(limit=30, keepView=false) {
    const query = get('search').value.trim().toLowerCase();
    const terms = query.split(/\s+/).filter(Boolean);
    const choice = get('verdict').value, kind = get('kind').value, genre = get('genre').value;
    matches = sections[section].filter(row => {
        if (choice !== '*' && verdictOf(row) !== choice) return false;
        if ((section === 0 || section === 4) && kind !== '*' && row.k !== kind) return false;
        if ((section === 0 || section === 4) && genre !== '*' && !genresOf(row).includes(genre)) return false;
        if (!terms.length) return true;
        const target = targetSearch.get(row);
        const haystack = target ? [target.typed,target.related,target.explanation,target.detail].join(' ') :
            (resultSearch.get(row) || (JSON.stringify(row) + ' ' + (row.k ? typed(row.k,row.n) : '')).toLowerCase());
        return terms.every(term => haystack.includes(term));
    });
    if (section === 0 && query) matches.sort((a,b) => searchRank(a,query)-searchRank(b,query) ||
        (a.k === 'expression_function' ? -1 : 0) - (b.k === 'expression_function' ? -1 : 0) || a.n.localeCompare(b.n));
    get('count').textContent = matches.length.toLocaleString(lang) + ' / ' + sections[section].length.toLocaleString(lang);
    get('results').replaceChildren();
    shown = 0;
    showMore(Number.isInteger(limit) ? Math.max(30,limit) : 30);
    // Keep the top of the refreshed list visible so filter changes never strand the user mid-page.
    const resultsTop = get('results').getBoundingClientRect().top;
    if (!keepView && resultsTop < stickyTop() - 1) scrollTo(0,scrollY + resultsTop - stickyTop() - 8);
}
function showMore(amount=30) {
    const render = normalCard;
    const end = Math.min(shown + (Number.isInteger(amount) ? amount : 30),matches.length);
    get('results').append(...matches.slice(shown,end).map(render));
    shown = end;
    get('more').hidden = shown >= matches.length;
}
function directDetails(parent) {
    const ancestor = parent.matches('details') ? parent : null;
    return [...parent.querySelectorAll('details')].filter(d => d.parentElement.closest('details') === ancestor);
}
function disclosureState(parent) {
    return directDetails(parent).map(d => ({open:d.open,children:d.open ? disclosureState(d) : []}));
}
function restoreDisclosures(parent,states) {
    const details=directDetails(parent);
    states.forEach((state,index) => {
        const d=details[index]; if(!d)return;
        d.open=state.open;
        if(state.open) {
            // Populate the same lazy disclosure before restoring its descendants.
            d.dispatchEvent(new Event('toggle'));
            restoreDisclosures(d,state.children);
        }
    });
}
function cardKey(card) { return card.dataset.target || card.querySelector(':scope > h2')?.textContent; }
function visibleSummaries(card) { return [...card.querySelectorAll('summary')].filter(s=>s.getBoundingClientRect().height>0); }
let lastDisclosureAnchor=null;
get('results').addEventListener('click',event=> {
    const summary=event.target.closest('summary');if(summary)lastDisclosureAnchor=summary;
});
get('language').addEventListener('click', () => {
    const cards=[...get('results').children];
    const expanded=new Map(cards.map(card=>[cardKey(card),disclosureState(card)]));
    const inViewport=element=> {const r=element.getBoundingClientRect();return r.height>0 && r.top>=0 && r.top<innerHeight;};
    const selected=lastDisclosureAnchor?.isConnected && inViewport(lastDisclosureAnchor) ? lastDisclosureAnchor :
        cards.flatMap(visibleSummaries).find(inViewport);
    const anchor=selected ? selected.closest('#results > article') :
        cards.find(card=>{const r=card.getBoundingClientRect();return r.bottom>0 && r.top<innerHeight;});
    const anchorKey=anchor && cardKey(anchor), anchorTop=(selected || anchor)?.getBoundingClientRect().top;
    const summaryIndex=selected ? visibleSummaries(anchor).indexOf(selected) : -1;
    const x=scrollX,y=scrollY,limit=shown;
    lang=lang === 'ja' ? 'en' : 'ja'; localize(limit);
    for(const card of get('results').children) {
        const state=expanded.get(cardKey(card)); if(state)restoreDisclosures(card,state);
    }
    requestAnimationFrame(()=>requestAnimationFrame(()=> {
        const current=[...get('results').children].find(card=>cardKey(card)===anchorKey);
        const point=current && (summaryIndex>=0 ? visibleSummaries(current)[summaryIndex] : current);
        scrollTo(x,point ? scrollY+point.getBoundingClientRect().top-anchorTop : y);
        lastDisclosureAnchor=point?.tagName==='SUMMARY' ? point : null;
    }));
});
get('search').addEventListener('input', search);
get('verdict').addEventListener('change', search);
get('kind').addEventListener('change', search);
get('genre').addEventListener('change', search);
get('more').addEventListener('click', showMore);
get('pinClose').addEventListener('click', () => { pinned = null; renderPin(); });
get('pinToggle').addEventListener('click', () => {
    get('pinPanel').classList.toggle('collapsed');
    renderPin();
});
get('pinLocate').addEventListener('click', () => {
    if (!pinned) return;
    relinkPin();
    if (pinned.source?.isConnected) {
        pinned.source.scrollIntoView({block:'center',behavior:'smooth'});
        return;
    }
    selectSection(5,pinned.id);
});
get('pinZoom').addEventListener('input', () => {
    get('pinImage').style.width = get('pinZoom').value + '%';
});
get('menuPin').addEventListener('click', () => {
    document.body.classList.toggle('menu-fixed');
    syncMenuPin();
});
addEventListener('resize', syncMenuPin);
try { if (localStorage.getItem('survey-menu-pinned') === '1') document.body.classList.add('menu-fixed'); }
catch (error) { /* unavailable storage simply keeps the default normal mode */ }
localize();
})();


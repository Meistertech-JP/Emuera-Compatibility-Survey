# Native・PyEmueraの選択観測：27のtyped target

[English](README.md)

既存の2比較から、対象ごとの実測を選んだ資料です。対象は `kind` と `name` の組で識別し、同名でも式とコマンドは別に数えます。結果の範囲は記載した条件に限られ、一般的な互換性判定ではありません。

- **GETTER251：14対象・23 case。** 式の `GETDEFCOLOR`、`GETDEFBGCOLOR`、`GETFOCUSCOLOR`、`GETSTYLE`、`GETFONT`、`CURRENTALIGN`、およびその6種と `ISSKIP`、`PRINTCLENGTH` のコマンド形。式・コマンドの各fixtureにNative 2回、PyEmuera 1回があります。設定された既定色に関する6 caseの元判定は `different_scoped`、残る17 caseは `matched_scoped` です。
- **OPNORMAL273：13演算子・4 case。** `+`、`==`、`!=`、`>`、`<`、`>=`、`<=`、`&&`、`^^`、`!&`、`&`、`|`、`^`。4 fixtureのそれぞれに保存済みNative 2回と後続PyEmuera 1回が対応します。選択した71マーカーは各fixtureの3 runで一致し、元のcase判定は `matched_scoped` です。

複数行に現れる同じrun IDは**1回の共有実行**を表します。演算子の短絡条件 `0&&ZZ_BAD()` は `VALUE=0 BADCOUNT=0`、`0!&ZZ_BAD()` は `VALUE=1 BADCOUNT=0` で、Native 2回とPyEmuera 1回の各runで観測されました。この2条件では右辺helperの呼出しはなく、helperの戻り値やエラーは観測していません。その他のguard、fatal後、診断全体の一致や他の入力は今回の選択範囲外です。

PyEmueraの終了codeは0。Nativeは記録された完了マーカーに到達しましたが、自然終了とexit codeは未観測で、観測後に所有プロセスを停止しました。マーカー到達は自然終了の証明ではありません。演算子のPyEmuera runに記録された非致命のOUTPUTLOG注意文もJSONに保持しています。GETFONTは名前を明示して復元しており、引数なしSETFONTは別途未解決です。描画・ピクセル・全設定・任意の表示履歴は確認していません。

これらのtyped targetについて、以前の受入原票は未特定のままです。後続の観測を原票の復元として扱っていません。**rawログ・fixture・receiptは同梱していません。** rawのSHAと行番号は参照先を識別しますが、別途rawを入手しなければ、このbundleの読者は投影とrawを照合できません。source pointerも同梱されていない元資料の位置です。元資料とこの投影の権利・秘密情報の確認は完了していません。manifestはファイルの整合性を示すもので、真正性や公開権限の証明ではありません。

## JSONの読み方

[selected-observations.json](selected-observations.json) の `getter.cases` には、対象、条件、元判定、3 runの `observations` があります。getterの `state.value` は文字列で、整数・文字列の区別は `condition.value_type` にあります。`RESULT0`・`RESULT1`・`RESULTS` は観測された結果スロットです。`preceding_setups_in_shared_run` は同じfixture内で先行する設定です。

`operator_normal.cases` の `marker_observations` は、各マーカーを対象、条件の式、参照helper、3 runの観測行に結び付けます。`VALUE` は式の結果、`COUNT` は計測用helperの呼出し数、`ORDER` は呼出し順、`BADCOUNT` は意図的に失敗させるhelperの呼出し数です。最上位の `runs` は共有runと終了の制限を示します。`comparison_pointer` と `register_pointer` は別の元資料中の位置であり、このJSON内の位置ではありません。

展開先のディレクトリで次を実行すると、最初は既定前景色の条件と3観測、次は `&&` の短絡条件を表示します。

```sh
python -c "import json; d=json.load(open('selected-observations.json',encoding='utf-8')); c=next(x for x in d['getter']['cases'] if x['case_id']=='GETTER251_expression_0'); print(c['target'],c['condition']); [print(o['run_id'],o['state']) for o in c['observations']]"
python -c "import json; d=json.load(open('selected-observations.json',encoding='utf-8')); c=next(x for x in d['operator_normal']['cases'] if x['case_id']=='OPNORMAL273_E140'); m=next(x for x in c['marker_observations'] if x['marker']=='LOG20'); print(m)"
```

## ファイル集合の確認

4ファイルを他のファイルがないディレクトリに展開し、そこで次を実行してください。Python 3.8以降の標準ライブラリだけで、4ファイルの名前とmanifestに載った3ファイルのサイズ・SHA-256を検査します。manifest自体の真正性を確認するには、別途信頼できる値とそのSHA-256を照合してください。この短い検査は、この平坦なbundle用であり、一般のアーカイブや安全性を検証するものではありません。

```sh
python -c "import json,hashlib,pathlib,sys; p=pathlib.Path('.'); names={'README.md','README.ja.md','selected-observations.json','file-set-manifest.json'}; check=lambda ok: None if ok else sys.exit('FAILED'); check({x.name for x in p.iterdir()}==names and all(not (p/n).is_symlink() for n in names)); m=json.loads((p/'file-set-manifest.json').read_text(encoding='utf-8')); f=m['files']; check(m['schema']=='selected-file-set.v1' and m['roots']==['bundle'] and m['manifest_location']=={'root':'bundle','path':'file-set-manifest.json'} and len(f)==3 and {e['path'] for e in f}==names-{'file-set-manifest.json'}); [check(e['root']=='bundle' and (p/e['path']).stat().st_size==e['size'] and hashlib.sha256((p/e['path']).read_bytes()).hexdigest()==e['sha256']) for e in f]; print('OK: 4 names, 3 file sizes and SHA-256 digests')"
```

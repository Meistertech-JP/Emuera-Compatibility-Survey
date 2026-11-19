# 694対象と検証要件

[English](README.md)

この資料は、対象と検証要件の対応を記録したものです。`projection.json` は694対象、53 typed証拠行、静的API 75対象、別枠24ケースを示します。`requirements.jsonl` は3,359件の出典付き検証要件で、原文3,278件、中立化81件です。文章は原記録に帰属する要件であり、新たな実行手順や、この資料自体による実測結果ではありません。記録済み観測への言及も原記録に帰属します。

`projection.json` 内の `requirements` の相対pathはこのディレクトリを基点とし、candidate参照の `path` は同じ配布単位のルートを基点とします。各SHAに一致するsnapshotに限りJSON Pointerを解決できます。参照先の更新後は再照合が必要です。`case-id-crosswalk.json` は本文中で正確に識別できる11種類のcase IDとaliasの対応です。原文の複合・省略表記は部分置換せず、略称から群の厳密な構成を推定しません。

原票と非公開受入資料は同梱されず、`WITHHELD_PRIVATE_SOURCE` は公開リンクではありません。candidate recordのsource ID・pointerも、参照先が非公開なら第三者が読めることを意味しません。文やSHA、caseへの参照だけで原資料の真正性、実測、原receipt、fixtureの完全性、同じ実行条件は証明できません。

`WITHHELD_PRIVATE_SOURCE` は受入資料をこの投影に同梱していないことを示し、原資料が存在しないことや調査の未完了を意味しません。各対象の `survey_pointer` から、台帳に記録された有限範囲の判定とケースIDを参照できます。現行の受入参照欄がない269対象については、[旧受入資料の参照層](../legacy-acceptance-269-20261117/README.ja.md)で、旧資料を特定した205対象と未特定の64対象を区別しています。これは元資料の公開や独立再現を意味しません。

53行は直接case 41行と関連文脈12行を区別します。main29の旧IDとneutral IDは共有batchの行に対応し、29独立実行を意味しません。dead branch 2件は対象命令に到達していません。PRINTDB15は2 typed役割の1物理case・3保存modeです。静的APIはruntime rawを同梱せず、関数method辞書への登録は命令構文や実行経路の証明ではありません。構文16・補助8ケースは主694と別です。素材全件の再hashや実機再実行は行っていません。

要件本文および証拠・素材のprivacyと権利は確認が必要です。この資料だけでは非公開原票と照合できず、配布条件は確定していません。SHAは同一性の照合用で、発行者の真正性を保証しません。

要件case roleには、原票・case登録・過去の別名判断に基づいて索引側で導出したラベルが含まれます。roleの意味は独立に再監査されていません。

関連する収録資料: [survey](../../results/survey.json)、[evidence index](../../results/evidence-index.json)、[権利表示](../../LICENSES/README.ja.md)。各要件の元／派生対応を含む非公開資料は同梱しません。

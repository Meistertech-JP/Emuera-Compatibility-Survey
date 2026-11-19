# PRINT K/D：保存された共有batch

[English](README.md)

82選定case・28 typed roleは、81個の条件とFORCEKANAの集約1件であり、1つの共有batchに記録されたNative 2 mode・Public 1 modeを参照します。82独立実行や登録roleからの到達を推測しません。`index.json` は条件、観測、元判定、3 modeの共有素材とbyte範囲を保持します。

Public履歴とstdoutは別素材です。保存比較のraw blockはPublic履歴に一致します。空SINGLEの10条件ではstdout側の空行bytesが履歴と異なるため、historyによる比較をstdoutに置き換えていません。byte範囲は保存済み対象物の探索結果であり、再実行や別の到達証明ではありません。

D色・font・GUI styleとNative自然終了は未観測。cleanupと自然終了を区別し、FORCEKANAの集約はsetter故障の証拠ではありません。実行体、原receipt、ソース抜粋、全親票は非同梱。素材の権利・機密の公開承認は未了です。

[権利表示](LICENSES/README.ja.md)、[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)。原source ZIPは非同梱。fixture・派生記録の権利主体と条件は別途確認が必要です。manifestとfile-set検査は履歴や実行の真正性を証明しません。

共有rawとfixtureには元batchの88条件すべてが含まれ、選定した81条件のほかに7条件が残ります。対象外7条件のID・roleは [scope.json](scope.json) に記載し、未観測とは扱いません。公開前にこの7条件を含む共有素材全体のprivacy・権利確認が必要です。

整合性を検査する前に、独立した信頼経路で得たmanifestと `tools/file_set_manifest.py` のSHA-256を確認してください。その後、この資料のルートディレクトリに移動し、 `python -B tools/file_set_manifest.py verify --manifest manifest.json --root evidence=.` を実行します。整合性は履歴の真正性や権利を証明しません。

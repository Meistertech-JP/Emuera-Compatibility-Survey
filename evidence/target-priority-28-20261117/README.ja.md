# 保存観測：CALL/JUMP/EVENT・表示D・LIST owner

[English](README.md)

これは保存済み28ケース（CALL/JUMP/EVENT 12、表示D系6、LIST owner 10）の証拠資料です。[target-priority.json](target-priority.json) の19 typed targetは、選定時に確認した候補索引で両側raw・fixtureの対応が未確認だった対象です。他に証拠がないこと、全要件の充足、到達や受入を示しません。caseごとの対象role、条件、比較、判定、制限を[index.json](index.json)に記録します。

各caseにはNative-01・Native-02・public-01の記録されたbatchを結び、mode別の原参照とreceiptの結合を保持します。同一bytesやroleの共有から、同一実行・独立実行を推定しません。LISTの原receiptにはcase IDとmodeがなく、派生receiptにはケース原票とmode別source pathに基づく結合だと明記しています。他の2群は原receiptに条件ID・modeがあります。元receiptには選択rawを宣言する出力欄がないため、rawの結合はcase evidence・群manifest・保存済みreadbackに基づきます。派生receiptから元path、argv、PID、時刻を除去しました。原receipt全文、その他出力、完全な親レビューは非同梱です。fixtureとconfigは元bytesのままです。原→派生SHAの対応表は別保管します。

LISTのcase本文は、親readbackが非同梱の群全体の総括であり、CALL/JUMPの値を個々のケースに帰属させないことを明記します。LISTの未呼出は対象到達を意味しません。fatal停止後の状態、Native自然終了や終了コードはrunnerのreturncodeから推測しません。表示Dは保存された出力表現に限定し、pixelやfontの同等性を主張しません。入力一覧は選択receiptの宣言範囲であり、過去の全依存や非同梱素材が揃っているという主張ではありません。

Python 3.10以上を使用します。実行前に、独立した信頼経路から得たmanifestのSHAと、そのmanifestに記載された `verify.py` および `tools/file_set_manifest.py` のSHAを外部のハッシュ手段で照合してください。その後、独立した経路で取得したpinを使い `python -B verify.py --manifest-sha256 <manifestの外部pin> --bindings-sha256 <bindingsの外部pin>` を実行します。整合性検査は由来、実行、権利、公開承認を証明しません。元票と完全な権利レビューはこの資料に含みません。

[ライセンス索引](LICENSES/README.ja.md)、[Emuera原ライセンス](LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)、[第三者表示](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照してください。Emuera NOTICEは別のsource ZIP用であり、そのZIPはこの資料に含みません。fixture、raw観測、派生記録、toolの所有権・機密・利用条件は独立レビュー待ちで、公開承認されていません。

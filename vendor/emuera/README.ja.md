# Emuera基準配布物

[English](README.md)

`Emuera1824-v24-with-notices.zip` は、保全した `Emuera1824+v24.zip` と日英の同伴NOTICEを一つの配布単位に収めています。使用前にいずれかのNOTICEを確認してください。保全ZIPを配布する場合はNOTICEも同伴し、このプロジェクトのアセットとして内側ZIPのみを独立配布しない構成です。

| ファイル | SHA-256 |
|---|---|
| 外側アーカイブ | `b0c2bd639868728e8b0b591c3da3d323a4537209300fb74d3829def4837cea85` |
| 保全した内側ZIP | `fd0dd5b83ab3f929e69de0b9af739fa9bf785b6f510b30d11aaf44db35af182a` |
| 内側ZIPの `Emuera1824+v24.exe` | `14cf28c137c6b76396c4d02fcb23ba6a31132301ce1fe0fcbab8c9f1c29d8964` |

外側を展開した後、内側ZIPを別の作業フォルダーへ展開します。Pythonでは `python -m zipfile -e Emuera1824-v24-with-notices.zip <展開先>` で外側を展開できます。[比較ハーネス](../../harness/README.ja.md)の実行前にハッシュを再確認してください。原アーカイブは保全し、試験は作業コピーで行います。

保全ZIPと配布元の493番の保存物との関係はNOTICEに記載しています。元の7zと内側ZIPは異なるコンテナです。内容の照合結果は、アーカイブ全体の原バイトやZIPの作成経路の一致を意味しません。

この配布単位では原本ZIPを改変せず、日英のNOTICEと一体で配布します。内側ZIPの再圧縮・改変は行わず、NOTICEに記載した由来確認の限界を維持します。プロジェクト全体の権利条件は[権利表示](../../LICENSES/README.ja.md)を参照してください。

# ファイル集合台帳ツールの限定テスト記録

2026-11-16、Windows 10、Python 3.12.10。対象は `test_file_set_manifest.py` に限定し、テスト用の一時ディレクトリは `tests/` 配下に作成・終了時に破棄した。現在の candidate や Release アセットを最終選定集合として走査・凍結していない。

```text
python -B -m unittest discover -s tests -p test_file_set_manifest.py -v
Ran 16 tests: 14 passed, 2 skipped
```

通常／Release の別ルート、同名の別ルート内ファイル、manifest の内部配置と自己除外、上書き拒否、欠落・余剰・同サイズ改ざん、絶対／親参照／Windows 予約名等の危険パス、重複 JSON キー・重複行、大小文字・Unicode NFC・ファイル／ディレクトリ名の衝突、ルート重複・入れ子を確認した。

Windows の実ジャンクションは、対象内・ルート自体・manifest の経路上で拒否することを確認した。reparse 属性と symlink の mode 判定も合成データで検査した。実際のファイル symlink とディレクトリ symlink の作成は、実行環境の権限不足（WinError 1314）により2件スキップしたため、実 symlink を使った当該2経路の実機確認は未実施。ジャンクションの成功結果を実 symlink の実行済み証拠には読み替えない。

初回テストでは Windows の `DirEntry.stat()` が返す識別子と開いたファイルの識別子が異なり正常ファイルが拒否された。`Path.lstat()` を使用する修正後に上記結果を得た。manifest との整合を調べるテストであり、公開可否、署名による真正性、同時書換えに対する完全なスナップショット保証を示さない。

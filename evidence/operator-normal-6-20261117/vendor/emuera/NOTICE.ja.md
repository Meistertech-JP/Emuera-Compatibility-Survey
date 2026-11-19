# Emuera1824+v24 同伴NOTICE

[English](NOTICE.en.md)

## 対象と出自

このNOTICEは、保有する `Emuera1824+v24.zip`（672,455 bytes、SHA-256 `fd0dd5b83ab3f929e69de0b9af739fa9bf785b6f510b30d11aaf44db35af182a`）に同伴します。ZIPを改変・再圧縮せず、ZIPと日英NOTICEを一つの外側アーカイブに収める構成です。NOTICEが同伴しない内側ZIPは、別途独立した配布物として提供しません。

保有ZIP内の説明書は、Emuera 1.824をベースとする私家改造版 `Emuera1824+v24` と説明しています。[配布ページ（番号493）](https://ux.getuploader.com/ninnohito/download/493)に表示されたMD5 `fa0e837c475855bf7766825b241e8bfd` は、比較用に保全された7zの実測MD5と一致しました。この外側の7zアーカイブ内に直接収録された3ファイル（内側アーカイブを除く）と、入れ子のソースアーカイブから展開した123ファイルを、保有ZIP内の対応する126ファイルと照合した結果、内容はすべてバイト一致しています。7zとZIPは構造・形式の異なる別のアーカイブであり、アーカイブ全体のバイト一致を意味しません。

配布ページから7zを直接再取得してSHA-256を照合しておらず、投稿者・配布者の暗号学的な本人確認も行っていません。実際の取得履歴、ZIPの作成経緯、および配布者本人が発行した原版との同一性・真正性は未確認です。MD5の一致は表示値と保全物の照合であり、真正性の証明ではありません。上記のZIP SHA-256は保有ファイルの識別に使います。

## Emueraと私家改造版

同梱の `Emuera1824+v24/Emuera_readme.txt` と `Emuera1824+v24/src1824+v24/src1824/license.txt` に、Emueraの情報とライセンスが記載されています。同梱の著作権表示は次のとおりです。

```text
Copyright (C) 2008- MinorShift, 妊）|дﾟ)の中の人
```

同梱説明書はライセンスをzlib/libpngライセンスと記載し、同梱 `license.txt` は出自について虚偽表示をしないこと、変更したソースを明示すること、ソース配布物から表示を削除・変更しないことを条件に掲げています。私家改造版の説明と変更履歴は、ZIP内 `Emuera1824+v24/私家改造版Emuera_readme.txt` を参照してください。同説明書はライセンスをEmuera本体に準じると記載しています。原ZIP内の表示とソースは変更していません。

## Rei HOBARA氏のC#版SFMT由来部分

ZIP内 `Emuera1824+v24/src1824+v24/src1824/Emuera/_Library/SFMT.cs` は、Rei HOBARA氏によるC#版SFMTを改変した旨と、`Copyright (C) Rei HOBARA 2007` を記載しています。当該HOBARA氏由来部分について、[同氏の配布ページ](https://www.rei.to/random.html)が示す選択肢からMITを選択し、[MIT原文](https://www.rei.to/MITL.txt)の著作権表示と許諾文を以下に全文掲載します。

```text
Copyright (c) 2007 Rei Hobara

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

この選択は当該HOBARA氏由来部分を対象とし、Emuera全体やSFMT原開発者を含む他の著作者の権利まで一括して許諾するものではありません。SFMT原開発者については[SFMT公式ライセンス](https://www.math.sci.hiroshima-u.ac.jp/m-mat/MT/SFMT/LICENSE.txt)も参照してください。アルゴリズムへの参照のみから、特定の他著作者のコードがコピーされたことや、その条件が当該箇所に適用されることを断定するものではありません。2009年採用時のHOBARA氏の配布版と現行版の同一性は未確認です。

## GDIとP/Invoke

ZIP内 `Emuera1824+v24/src1824+v24/src1824/Emuera/_Library/GDI.cs` のコメントは、pinvoke.netの `gdi32.BitBlt` ページからコピーした旨を記載しています。現行の[pinvoke.net利用規約](https://www.pinvoke.net/termsofuse.htm) 3.3–3.4、4.1は、ソースコード投稿について条件付きの利用・改変・配布を定め、3.4には用途上の制限があります。4.3はソースコード以外の利用者投稿資料を別に扱います。適用条件は規約原文全体を参照してください。

[pinvoke.netのStretchBltページ](https://www.pinvoke.net/default.aspx/gdi32/stretchblt.html)にも `TernaryRasterOperations` に対応する記載がありますが、同ページがこのZIP内コードの実際のコピー元であることは確認されていません。採用当時のBitBltページ、実際のコピー範囲、ソース中の説明コメントの出典と性質、現行規約の過去の採用への適用は未確定です。コメントを形式のみで直ちに非コード投稿資料と分類せず、その由来・適用条件も確定しません。

[MicrosoftのBitBlt API文書](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-bitblt)はAPI仕様の参考資料です。この文書をGDI.csの出典や、同ファイル全体に対する許諾と認定するものではありません。

## 配布上の境界

このNOTICEは同梱された権利表示を補うもので、原ZIPの内部表示に代わるものではありません。対象物の同伴表示を維持し、その他の第三者素材、ライセンス条件および公開チャネル上の提示方法は別途確認してください。

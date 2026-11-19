# Accompanying NOTICE for Emuera1824+v24

[日本語](NOTICE.ja.md)

## Identified archive and provenance

This NOTICE accompanies the held `Emuera1824+v24.zip` (672,455 bytes; SHA-256 `fd0dd5b83ab3f929e69de0b9af739fa9bf785b6f510b30d11aaf44db35af182a`). The archive is kept byte-identical and is packaged together with both Japanese and English NOTICE files in one outer archive. The inner ZIP is not offered separately as an independent distribution without the accompanying NOTICE.

The included documentation describes a privately modified `Emuera1824+v24` based on Emuera 1.824. The MD5 `fa0e837c475855bf7766825b241e8bfd` displayed on the [distribution page (item 493)](https://ux.getuploader.com/ninnohito/download/493) matches the measured MD5 of the separately retained 7z used for comparison. Three files in the outer 7z (excluding the nested archive itself) and 123 files extracted from the nested source archive were mapped to 126 corresponding files in the held ZIP; all corresponding file contents were byte-identical. The 7z and ZIP have different structures and formats; this does not mean the archive files themselves are byte-identical.

The 7z has not been directly downloaded again from the distribution page for a SHA-256 comparison, and no cryptographic authentication of the poster or distributor has been performed. The actual acquisition history, how the ZIP was created, and its identity with or authenticity as an original issued by the distributor remain unverified. The MD5 match compares the displayed value with the preserved file and does not prove authenticity. The ZIP SHA-256 above identifies the held file.

## Emuera and the privately modified version

The ZIP includes `Emuera1824+v24/Emuera_readme.txt` and `Emuera1824+v24/src1824+v24/src1824/license.txt` with information and the license for Emuera. The included copyright notice reads:

```text
Copyright (C) 2008- MinorShift, 妊）|дﾟ)の中の人
```

The included Emuera readme identifies the license as zlib/libpng. The included `license.txt` sets conditions including no misrepresentation of origin, identification of modified source, and preservation of the notice in source distributions. The privately modified version and its change history are described in `Emuera1824+v24/私家改造版Emuera_readme.txt` inside the ZIP, which states that its license follows Emuera's. The inner ZIP, its notices and source have not been modified.

## Portions derived from Rei HOBARA's C# SFMT

The included `Emuera1824+v24/src1824+v24/src1824/Emuera/_Library/SFMT.cs` identifies itself as a modification of Rei HOBARA's C# SFMT and contains `Copyright (C) Rei HOBARA 2007`. For the portions derived from HOBARA's work, MIT is selected from the options described on [the author's distribution page](https://www.rei.to/random.html). The copyright and permission text from [the author's MIT text](https://www.rei.to/MITL.txt) is reproduced in full below.

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

This selection concerns the HOBARA-derived portions. It does not grant rights held by other authors, including the original SFMT authors, or license Emuera as a whole. See also the [official SFMT license](https://www.math.sci.hiroshima-u.ac.jp/m-mat/MT/SFMT/LICENSE.txt). A reference to an algorithm alone does not establish that another author's code was copied or that its particular license applies to the relevant material. The identity of the HOBARA distribution used in 2009 and the current version has not been established.

## GDI and P/Invoke

A comment in the included `Emuera1824+v24/src1824+v24/src1824/Emuera/_Library/GDI.cs` states that material was copied from pinvoke.net's `gdi32.BitBlt` page. The current [pinvoke.net Terms of Use](https://www.pinvoke.net/termsofuse.htm), sections 3.3–3.4 and 4.1, describe conditional use, modification and distribution of contributed source code; section 3.4 includes restrictions on uses. Section 4.3 treats user-contributed materials other than source code separately. Consult the complete terms for their applicable conditions.

The [pinvoke.net StretchBlt page](https://www.pinvoke.net/default.aspx/gdi32/stretchblt.html) also contains material corresponding to `TernaryRasterOperations`; it has not been established as the actual source of the code in this ZIP. The historical BitBlt page at adoption, the copied extent, the origin and nature of explanatory comments in the source, and the applicability of current terms to the historical adoption remain undetermined. Comments are not classified as non-code contributions merely by their form, and their origin and applicable conditions have not been established.

The [Microsoft BitBlt API documentation](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-bitblt) is a reference for the API specification. It is not identified here as the source of GDI.cs or as a blanket license for that file.

## Distribution boundary

This NOTICE supplements the notices within the ZIP; it does not replace them. Preserve the accompanying notices and separately review other third-party material, license conditions, and presentation through any distribution channel.

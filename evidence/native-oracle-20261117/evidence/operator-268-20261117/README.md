# Operators: finite observations for 33 conditions

[日本語](README.ja.md) · [Machine-readable conditions and per-mode records](observations.json)

These are saved Native Emuera observations with PyEmuera comparisons. A single shared fixture contains 35 sequential conditions; this document lists 33 registered conditions. Two additional conditions are repeated controls and are not counted among the 33. The shared fixture was run twice on Native and once on PyEmuera, not as 33 × 3 separate case executions. The Native log bytes have the same SHA, while the executions were recorded separately.

For selected values and helper order under these inputs, 31 conditions are scoped matches and two are scoped differences. This is not equality of complete logs, full output, whole strings or all inputs. For the length-19998 string only its length and endpoints were observed. Natural exit of the two Native processes was not observed; cleanup terminated them. PyEmuera exit code 0 was recorded. Py stderr contains a warning that OUTPUTLOG writes bounded history under `.pyemuera/logs`. No GUI images are included.

Each condition starts with A=B=0, C=701, the first two integer array elements 6 and 99, and string values ab. Left and right value helpers increment A and record order in B: left uses B=B×10+1, right B=B×10+2. The index helper increments only A. `measurements` are selected outputs; `EQ` is the first comparison, `RETURN` is the expression return and array state at that point, and `VECTOR` is the recorded array. See the JSON for per-mode values and event order. `typed_keys` also includes shared related targets; distinguish these from `observed_own_roles`.

**The original ERB, ERH, config and Native/Py raw files are not included.** Authorship, redistribution permissions, and the treatment of engine output remain under review. The table is a projection of selected values checked against saved records and raw, not the original bytes; this material alone cannot independently reproduce the full run or recheck those bytes. Do not infer results beyond the recorded conditions.

The recorded engines were Emuera1824+v24 and PyEmuera 3.0.0; their SHA-256 identifiers are in the JSON. Original license texts and the PyEmuera NOTICE are in [LICENSES](LICENSES/). References to distributions and included files inside that NOTICE describe the original PyEmuera distribution, not this bundle. Permissions for the survey inputs and projection require separate review.

Search `case_id` or `typed_keys` in [observations.json](observations.json). The existing common query points to the case register; a link to this material requires a later integration.

## Conditions and selected results

| case ID | Condition | Native | PyEmuera |
| --- | --- | --- | --- |
| `OPCONT268_repeat-str-int-0` | Repeat string ab zero times; the count comes from a helper. | C=0; A=2 B=12; D0=6; D1=99; S=[] | Selected values and helper order match |
| `OPCONT268_repeat-str-int-2` | Repeat string ab twice; the count comes from a helper. | C=4; A=2 B=12; D0=6; D1=99; S=[abab] | Selected values and helper order match |
| `OPCONT268_repeat-str-int-9999` | Repeat string ab 9999 times; record length and endpoints. | C=19998; A=2 B=12; D0=6; D1=99; SLEN=19998; HEAD=[ab]; TAIL=[ab] | Selected values and helper order match |
| `OPCONT268_strcmp-eq` | Compare ab with ab, then empty string with ab using ==. | EQ C=1 A=2 B=12; C=0; A=3 B=121; D0=6; D1=99; S=[] | Selected values and helper order match |
| `OPCONT268_strcmp-ne` | Compare ab with ab, then empty string with ab using !=. | EQ C=0 A=2 B=12; C=1; A=3 B=121; D0=6; D1=99; S=[] | Selected values and helper order match |
| `OPCONT268_strcmp-gt` | Compare ab with ab, then empty string with ab using >. | EQ C=0 A=2 B=12; C=0; A=3 B=121; D0=6; D1=99; S=[] | Selected values and helper order match |
| `OPCONT268_strcmp-lt` | Compare ab with ab, then empty string with ab using <. | EQ C=0 A=2 B=12; C=1; A=3 B=121; D0=6; D1=99; S=[] | Selected values and helper order match |
| `OPCONT268_strcmp-ge` | Compare ab with ab, then empty string with ab using >=. | EQ C=0 A=2 B=12; C=1; A=3 B=121; D0=6; D1=99; S=[] | EQ C=1 A=2 B=12; C=0; A=3 B=121; D0=6; D1=99; S=[] — Selected values differ |
| `OPCONT268_strcmp-le` | Compare ab with ab, then empty string with ab using <=. | EQ C=0 A=2 B=12; C=1; A=3 B=121; D0=6; D1=99; S=[] | EQ C=1 A=2 B=12; C=1; A=3 B=121; D0=6; D1=99; S=[] — Selected values differ |
| `OPCONT268_unary-effect-not` | Apply logical ! to -1 returned by a helper. | C=0; A=1 B=1; D0=6; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_unary-effect-complement` | Apply bitwise ~ to -1 returned by a helper. | C=0; A=1 B=1; D0=6; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_shift-narrow-left` | Shift 1 left by 2147483648. | C=1; A=0 B=0; D0=6; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_shift-narrow-right` | Shift 1 right by 2147483648. | C=1; A=0 B=0; D0=6; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_ternary-nested` | Nested conditional: outer condition 0, inner condition 1; selected helper returns 7. | C=7; A=1 B=2; D0=6; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_inc-edge-pre` | Set element 0 to the maximum signed 64-bit integer; record prefix ++ return and a separate standalone operation. | RETURN C=-9223372036854775808 D0=-9223372036854775808; C=-9223372036854775808; A=1 B=0; D0=-9223372036854775808; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_inc-edge-post` | Set element 0 to the maximum signed 64-bit integer; record postfix ++ return and a separate standalone operation. | RETURN C=9223372036854775807 D0=-9223372036854775808; C=9223372036854775807; A=1 B=0; D0=-9223372036854775808; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_dec-edge-pre` | Set element 0 to the minimum signed 64-bit integer; record prefix -- return and a separate standalone operation. | RETURN C=9223372036854775807 D0=9223372036854775807; C=9223372036854775807; A=1 B=0; D0=9223372036854775807; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_dec-edge-post` | Set element 0 to the minimum signed 64-bit integer; record postfix -- return and a separate standalone operation. | RETURN C=-9223372036854775808 D0=9223372036854775807; C=-9223372036854775808; A=1 B=0; D0=9223372036854775807; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_vector-num-0` | Assign helper-returned 11 and 22 to a two-element numeric array. | VECTOR 11,22; C=701; A=2 B=12; D0=6; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_vector-num-constant` | Assign literal 7 and 7 to a two-element numeric array. | VECTOR 7,7; C=701; A=0 B=0; D0=6; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_vector-str-0` | Assign ab returned by two helpers to a two-element string array. | VECTOR [ab],[ab]; C=701; A=2 B=12; D0=6; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_vector-str-constant` | Assign literal ab and ab to a two-element string array. | VECTOR [ab],[ab]; C=701; A=0 B=0; D0=6; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_raw-form-comma` | Assign the FORM text ab, to a string and record its length. | C=3; A=0 B=0; D0=6; D1=99; S=[ab,] | Selected values and helper order match |
| `OPCONT268_compound-edge-add` | Apply += 1 to element 0 containing the maximum signed 64-bit integer. | C=-9223372036854775808; A=0 B=0; D0=-9223372036854775808; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_compound-edge-sub` | Apply -= 1 to element 0 containing the minimum signed 64-bit integer. | C=9223372036854775807; A=0 B=0; D0=9223372036854775807; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_compound-edge-mul` | Apply *= 2 to element 0 containing the maximum signed 64-bit integer. | C=-2; A=0 B=0; D0=-2; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_compound-edge-shl` | Apply <<= 64 to element 0 containing 1. | C=1; A=0 B=0; D0=1; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_compound-edge-shr` | Apply >>= 64 to element 0 containing -8. | C=-8; A=0 B=0; D0=-8; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_compound-edge-or` | Apply \|= 1 to element 0 containing -1. | C=-1; A=0 B=0; D0=-1; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_compound-edge-and` | Apply &= 1 to element 0 containing -1. | C=1; A=0 B=0; D0=1; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_compound-edge-xor` | Apply ^= 1 to element 0 containing -1. | C=-2; A=0 B=0; D0=-2; D1=99; S=[ab] | Selected values and helper order match |
| `OPCONT268_compound-string-add` | Apply += with helper-returned ab to string ab. | C=4; A=1 B=2; D0=6; D1=99; S=[abab] | Selected values and helper order match |
| `OPCONT268_compound-string-mul` | Apply *= with helper-returned 2 to string ab. | C=4; A=1 B=2; D0=6; D1=99; S=[abab] | Selected values and helper order match |

## File verification

Run `python -B verify.py` in this directory. It checks the file set, hashes and consistency across modes against the current manifest. The command alone does not establish authenticity of the manifest or semantic agreement with the nonincluded raw.

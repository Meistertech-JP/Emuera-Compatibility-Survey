# 8ケースの限定観測

[English](README.en.md)

この文書は保存記録からの選択投影です。case IDとverdictは元台帳を維持しています。元rawは同梱しておらず、この資料だけでは観測を単独で再現できません。新規実行は行っていません。source IDとSHA-256は[対応表](SOURCE-INDEX.md)を参照してください。

## PRINTDWEMPTY01

verdict: `matched_scoped`

空引数。両者で文字を出さず、待機解除後にAFTER_EMPTYを1回記録。待機解除には本家の空の入力欄へReturnを1回送り、Pyには標準入力で改行1行を与えた。各case Native2回・Py2回の選択ログは同一SHA。Native自然終了・終了コードは未観測。選択したNative実行のスクリーンショットはなく、GUIピクセルの一致や他のPRINT形式への一般化はできない。

根拠source ID: `candidate_case_register`, `printdw_comparison`, `printdw_native-final-empty-01_log`, `printdw_native-final-empty-01_receipt`, `printdw_native-final-empty-02_log`, `printdw_native-final-empty-02_receipt`, `printdw_public-empty01-01_log`, `printdw_public-empty01-01_receipt`, `printdw_public-empty01-01_fixture`, `printdw_public-empty01-02_log`, `printdw_public-empty01-02_receipt`, `printdw_public-empty01-02_fixture`

## PRINTDWSPACE01

verdict: `matched_scoped`

引数は内部に空白2個の `X  Y`。両者で2空白を保持し、待機解除後にAFTER_SPACEを1回記録。待機解除には本家の空の入力欄へReturnを1回送り、Pyには標準入力で改行1行を与えた。各case Native2回・Py2回の選択ログは同一SHA。Native自然終了・終了コードは未観測。選択したNative実行のスクリーンショットはなく、GUIピクセルの一致や他のPRINT形式への一般化はできない。

根拠source ID: `candidate_case_register`, `printdw_comparison`, `printdw_native-final-space-01_log`, `printdw_native-final-space-01_receipt`, `printdw_native-final-space-02_log`, `printdw_native-final-space-02_receipt`, `printdw_public-space01-01_log`, `printdw_public-space01-01_receipt`, `printdw_public-space01-01_fixture`, `printdw_public-space01-02_log`, `printdw_public-space01-02_receipt`, `printdw_public-space01-02_fixture`

## ARRAY_BOUNDARY_NORMAL_CORRECTED_20261115

verdict: `matched_scoped`

初期配列 `[5,2,8,9]`、長さ4。単一区間[3,4)のSUM/MAX/MINは両者9。端点helperを使う各式は両者SUM=23、MAX=13、MIN=2、helper順231・回数3・終端4・最終配列[5,2,8,13]。RESULT=777、RESULTS=SENTINEL、AFTER/DONE到達。6観測は同じNative2回・Py1回から得たもので18回の起動ではない。Native自然終了は未観測。別の境界停止と既存empty/reverse差は別範囲。

根拠source ID: `candidate_case_register`, `array_report_json`, `array_conditions`, `array_native-01_log`, `array_native-01_fixture`, `array_native-02_log`, `array_native-02_fixture`, `array_public-01_log`, `array_public-01_fixture`

## LEVEL_BOUNDARY_GETPALAMLV_NEGATIVE_20261115

verdict: `different_scoped`

GETPALAMLV式、値9223372036854775807、table長1000、maxlevel=-1。helper回数2・順12。本家は-1、Pyは0を返し、両者AFTER/DONE到達。Native2回・Py1回。本家自然終了未観測。method形式と旧custom-table等のruntime identityはこの記録では未確立。

根拠source ID: `candidate_case_register`, `level_comparison`, `level_GETPALAMLV_NEGATIVE_native-01_log`, `level_GETPALAMLV_NEGATIVE_native-01_fixture`, `level_GETPALAMLV_NEGATIVE_native-02_log`, `level_GETPALAMLV_NEGATIVE_native-02_fixture`, `level_GETPALAMLV_NEGATIVE_public-01_log`, `level_GETPALAMLV_NEGATIVE_public-01_fixture`

## LEVEL_BOUNDARY_GETPALAMLV_SIZEPLUS1_20261115

verdict: `different_scoped`

GETPALAMLV式、値9223372036854775807、table長1000、maxlevel=1001（VARSIZE+1）。helper回数2・順12。本家は対象代入の10行目でSystem.IndexOutOfRangeException、AFTER/DONE未到達で戻り値・後状態は未観測。Pyは999を返しAFTER/DONE到達。Native2回・Py1回。本家自然終了未観測。method形式と旧custom-table等のruntime identityはこの記録では未確立。

根拠source ID: `candidate_case_register`, `level_comparison`, `level_GETPALAMLV_SIZEPLUS1_native-01_log`, `level_GETPALAMLV_SIZEPLUS1_native-01_fixture`, `level_GETPALAMLV_SIZEPLUS1_native-02_log`, `level_GETPALAMLV_SIZEPLUS1_native-02_fixture`, `level_GETPALAMLV_SIZEPLUS1_public-01_log`, `level_GETPALAMLV_SIZEPLUS1_public-01_fixture`

## LEVEL_BOUNDARY_GETEXPLV_NEGATIVE_20261115

verdict: `different_scoped`

GETEXPLV式、値9223372036854775807、table長1000、maxlevel=-1。helper回数2・順12。本家は-1、Pyは0を返し、両者AFTER/DONE到達。Native2回・Py1回。本家自然終了未観測。method形式と旧custom-table等のruntime identityはこの記録では未確立。

根拠source ID: `candidate_case_register`, `level_comparison`, `level_GETEXPLV_NEGATIVE_native-01_log`, `level_GETEXPLV_NEGATIVE_native-01_fixture`, `level_GETEXPLV_NEGATIVE_native-02_log`, `level_GETEXPLV_NEGATIVE_native-02_fixture`, `level_GETEXPLV_NEGATIVE_public-01_log`, `level_GETEXPLV_NEGATIVE_public-01_fixture`

## LEVEL_BOUNDARY_GETEXPLV_SIZEPLUS1_20261115

verdict: `different_scoped`

GETEXPLV式、値9223372036854775807、table長1000、maxlevel=1001（VARSIZE+1）。helper回数2・順12。本家は対象代入の10行目でSystem.IndexOutOfRangeException、AFTER/DONE未到達で戻り値・後状態は未観測。Pyは999を返しAFTER/DONE到達。Native2回・Py1回。本家自然終了未観測。method形式と旧custom-table等のruntime identityはこの記録では未確立。

根拠source ID: `candidate_case_register`, `level_comparison`, `level_GETEXPLV_SIZEPLUS1_native-01_log`, `level_GETEXPLV_SIZEPLUS1_native-01_fixture`, `level_GETEXPLV_SIZEPLUS1_native-02_log`, `level_GETEXPLV_SIZEPLUS1_native-02_fixture`, `level_GETEXPLV_SIZEPLUS1_public-01_log`, `level_GETEXPLV_SIZEPLUS1_public-01_fixture`

## SAVECHARA_FINITE_BOUNDARIES_EVALUATION_ORDER_20261115

verdict: `different_scoped`

各条件でNative1回・Py1回。重複ID (0,0) は本家が引数構築で拒否、PyはE_ARGUMENT。定数-1またはFLAG:9=-1の後続helperは本家側で観測されず、Pyはmarker出力後E_INDEX。ID=CHARANUM=3は両者停止、PyはE_INDEX。保存先ディレクトリ衝突は本家UnauthorizedAccessException、PyはE_SAVE_IO。正常な動的引数は両者ORDER=1234・RESULT=0・COUNT=3・DONE。本家自然終了未観測、保存形式の相互ロードなし。

根拠source ID: `candidate_case_register`, `savechara_comparison`, `save_duplicate_native_fixture`, `save_duplicate_native_emuera_log`, `save_duplicate_public_fixture`, `save_duplicate_public_verified_stdout_bin`, `save_duplicate_public_verified_stderr_bin`, `save_negative_late_helper_clean_native_fixture`, `save_negative_late_helper_clean_native_emuera_log`, `save_negative_late_helper_clean_public_fixture`, `save_negative_late_helper_clean_public_verified_stdout_bin`, `save_negative_late_helper_clean_public_verified_stderr_bin`, `save_dynamic_bad_id_later_native_fixture`, `save_dynamic_bad_id_later_native_emuera_log`, `save_dynamic_bad_id_later_public_fixture`, `save_dynamic_bad_id_later_public_verified_stdout_bin`, `save_dynamic_bad_id_later_public_verified_stderr_bin`, `save_index_equal_charanum_native_fixture`, `save_index_equal_charanum_native_emuera_log`, `save_index_equal_charanum_public_fixture`, `save_index_equal_charanum_public_verified_stdout_bin`, `save_index_equal_charanum_public_verified_stderr_bin`, `save_filename_directory_collision_native_fixture`, `save_filename_directory_collision_native_emuera_log`, `save_filename_directory_collision_public_fixture`, `save_filename_directory_collision_public_verified_stdout_bin`, `save_filename_directory_collision_public_verified_stderr_bin`, `save_ordered_success_native_fixture`, `save_ordered_success_native_emuera_log`, `save_ordered_success_public_fixture`, `save_ordered_success_public_verified_stdout_bin`, `save_ordered_success_public_verified_stderr_bin`


# Scoped observations for eight cases

[日本語](README.ja.md)

This document is a selected projection from saved records. Case IDs and verdicts match the source register. Original raw files are not included, and the observations cannot be independently reproduced from this document alone. No new runs were made. Source IDs and SHA-256 values are listed in the [source index](SOURCE-INDEX.md).

## PRINTDWEMPTY01

verdict: `matched_scoped`

Empty argument: neither engine emitted argument text, and AFTER_EMPTY appeared once after the wait was released. Native received one Return in an empty input field; Py received one newline on standard input. Each case has two Native and two Py selected runs with the same log SHA. Native natural exit and exit code were not observed; selected Native runs have no screenshot. GUI pixel equivalence and other PRINT forms are not established.

Source IDs: `candidate_case_register`, `printdw_comparison`, `printdw_native-final-empty-01_log`, `printdw_native-final-empty-01_receipt`, `printdw_native-final-empty-02_log`, `printdw_native-final-empty-02_receipt`, `printdw_public-empty01-01_log`, `printdw_public-empty01-01_receipt`, `printdw_public-empty01-01_fixture`, `printdw_public-empty01-02_log`, `printdw_public-empty01-02_receipt`, `printdw_public-empty01-02_fixture`

## PRINTDWSPACE01

verdict: `matched_scoped`

Argument `X  Y` has two internal spaces: both retained them, and AFTER_SPACE appeared once after the wait was released. Native received one Return in an empty input field; Py received one newline on standard input. Each case has two Native and two Py selected runs with the same log SHA. Native natural exit and exit code were not observed; selected Native runs have no screenshot. GUI pixel equivalence and other PRINT forms are not established.

Source IDs: `candidate_case_register`, `printdw_comparison`, `printdw_native-final-space-01_log`, `printdw_native-final-space-01_receipt`, `printdw_native-final-space-02_log`, `printdw_native-final-space-02_receipt`, `printdw_public-space01-01_log`, `printdw_public-space01-01_receipt`, `printdw_public-space01-01_fixture`, `printdw_public-space01-02_log`, `printdw_public-space01-02_receipt`, `printdw_public-space01-02_fixture`

## ARRAY_BOUNDARY_NORMAL_CORRECTED_20261115

verdict: `matched_scoped`

Initial array `[5,2,8,9]`, size 4. For singleton [3,4), SUM/MAX/MIN each return 9 on both. With endpoint helpers, SUM=23, MAX=13, MIN=2 on both; helper order 231, count 3, endpoint 4, final array [5,2,8,13]. RESULT=777 and RESULTS=SENTINEL; AFTER/DONE reached. These six observations share two Native and one Py launches; they are not 18 launches. Native natural exit was not observed. Boundary-stop and existing empty/reverse differences are separate.

Source IDs: `candidate_case_register`, `array_report_json`, `array_conditions`, `array_native-01_log`, `array_native-01_fixture`, `array_native-02_log`, `array_native-02_fixture`, `array_public-01_log`, `array_public-01_fixture`

## LEVEL_BOUNDARY_GETPALAMLV_NEGATIVE_20261115

verdict: `different_scoped`

GETPALAMLV expression, value 9223372036854775807, table size 1000, maxlevel -1. Helpers: count 2, order 12. Native returns -1 and Py returns 0; both reach AFTER/DONE. Two Native and one Py run. Native natural exit is unobserved. Method form and old custom-table runtime identity are not established here.

Source IDs: `candidate_case_register`, `level_comparison`, `level_GETPALAMLV_NEGATIVE_native-01_log`, `level_GETPALAMLV_NEGATIVE_native-01_fixture`, `level_GETPALAMLV_NEGATIVE_native-02_log`, `level_GETPALAMLV_NEGATIVE_native-02_fixture`, `level_GETPALAMLV_NEGATIVE_public-01_log`, `level_GETPALAMLV_NEGATIVE_public-01_fixture`

## LEVEL_BOUNDARY_GETPALAMLV_SIZEPLUS1_20261115

verdict: `different_scoped`

GETPALAMLV expression, value 9223372036854775807, table size 1000, maxlevel 1001 (VARSIZE+1). Helpers: count 2, order 12. Native stops at target assignment line 10 with System.IndexOutOfRangeException; AFTER/DONE, return value and post-target state are not observed. Py returns 999 and reaches AFTER/DONE. Two Native and one Py run. Native natural exit is unobserved. Method form and old custom-table runtime identity are not established here.

Source IDs: `candidate_case_register`, `level_comparison`, `level_GETPALAMLV_SIZEPLUS1_native-01_log`, `level_GETPALAMLV_SIZEPLUS1_native-01_fixture`, `level_GETPALAMLV_SIZEPLUS1_native-02_log`, `level_GETPALAMLV_SIZEPLUS1_native-02_fixture`, `level_GETPALAMLV_SIZEPLUS1_public-01_log`, `level_GETPALAMLV_SIZEPLUS1_public-01_fixture`

## LEVEL_BOUNDARY_GETEXPLV_NEGATIVE_20261115

verdict: `different_scoped`

GETEXPLV expression, value 9223372036854775807, table size 1000, maxlevel -1. Helpers: count 2, order 12. Native returns -1 and Py returns 0; both reach AFTER/DONE. Two Native and one Py run. Native natural exit is unobserved. Method form and old custom-table runtime identity are not established here.

Source IDs: `candidate_case_register`, `level_comparison`, `level_GETEXPLV_NEGATIVE_native-01_log`, `level_GETEXPLV_NEGATIVE_native-01_fixture`, `level_GETEXPLV_NEGATIVE_native-02_log`, `level_GETEXPLV_NEGATIVE_native-02_fixture`, `level_GETEXPLV_NEGATIVE_public-01_log`, `level_GETEXPLV_NEGATIVE_public-01_fixture`

## LEVEL_BOUNDARY_GETEXPLV_SIZEPLUS1_20261115

verdict: `different_scoped`

GETEXPLV expression, value 9223372036854775807, table size 1000, maxlevel 1001 (VARSIZE+1). Helpers: count 2, order 12. Native stops at target assignment line 10 with System.IndexOutOfRangeException; AFTER/DONE, return value and post-target state are not observed. Py returns 999 and reaches AFTER/DONE. Two Native and one Py run. Native natural exit is unobserved. Method form and old custom-table runtime identity are not established here.

Source IDs: `candidate_case_register`, `level_comparison`, `level_GETEXPLV_SIZEPLUS1_native-01_log`, `level_GETEXPLV_SIZEPLUS1_native-01_fixture`, `level_GETEXPLV_SIZEPLUS1_native-02_log`, `level_GETEXPLV_SIZEPLUS1_native-02_fixture`, `level_GETEXPLV_SIZEPLUS1_public-01_log`, `level_GETEXPLV_SIZEPLUS1_public-01_fixture`

## SAVECHARA_FINITE_BOUNDARIES_EVALUATION_ORDER_20261115

verdict: `different_scoped`

One Native and one Py run per condition. Duplicate IDs (0,0): Native rejects during argument construction; Py reports E_ARGUMENT. With constant -1 or FLAG:9=-1, the later helper is not observed on Native; Py emits the marker then E_INDEX. ID=CHARANUM=3 stops both; Py reports E_INDEX. Destination directory collision: Native UnauthorizedAccessException, Py E_SAVE_IO. Valid dynamic arguments: both record ORDER=1234, RESULT=0, COUNT=3 and DONE. Native natural exit was not observed; save formats were not cross-loaded.

Source IDs: `candidate_case_register`, `savechara_comparison`, `save_duplicate_native_fixture`, `save_duplicate_native_emuera_log`, `save_duplicate_public_fixture`, `save_duplicate_public_verified_stdout_bin`, `save_duplicate_public_verified_stderr_bin`, `save_negative_late_helper_clean_native_fixture`, `save_negative_late_helper_clean_native_emuera_log`, `save_negative_late_helper_clean_public_fixture`, `save_negative_late_helper_clean_public_verified_stdout_bin`, `save_negative_late_helper_clean_public_verified_stderr_bin`, `save_dynamic_bad_id_later_native_fixture`, `save_dynamic_bad_id_later_native_emuera_log`, `save_dynamic_bad_id_later_public_fixture`, `save_dynamic_bad_id_later_public_verified_stdout_bin`, `save_dynamic_bad_id_later_public_verified_stderr_bin`, `save_index_equal_charanum_native_fixture`, `save_index_equal_charanum_native_emuera_log`, `save_index_equal_charanum_public_fixture`, `save_index_equal_charanum_public_verified_stdout_bin`, `save_index_equal_charanum_public_verified_stderr_bin`, `save_filename_directory_collision_native_fixture`, `save_filename_directory_collision_native_emuera_log`, `save_filename_directory_collision_public_fixture`, `save_filename_directory_collision_public_verified_stdout_bin`, `save_filename_directory_collision_public_verified_stderr_bin`, `save_ordered_success_native_fixture`, `save_ordered_success_native_emuera_log`, `save_ordered_success_public_fixture`, `save_ordered_success_public_verified_stdout_bin`, `save_ordered_success_public_verified_stderr_bin`


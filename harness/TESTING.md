# Test record

2026-11-16, Windows 10 19045 and CPython 3.12.10 64-bit: the pinned Native Emuera and public PyEmuera binaries were used for the following finite observations.

- In the selected expression comparison, `ABS` produced 7 on both engines. `STRFINDU` and `STRFIND` produced -1 on Native and 3 on PyEmuera. The observed `RESULT` and `RESULTS` sentinels matched. Native natural exit was not observed; owned processes were terminated after observation.
- In `RESULT_WRITE`, both logs recorded `RESULT` 701→42 and `RESULTS` AUTO_SENT→123. P35 and P36 recorded the selected inputs 42 and `ABC` in Native images and PyEmuera stdout; separately instrumented OUTPUTLOG fixtures recorded the same selected input values on both sides.
- The missing-argument case records a Native argument-count diagnostic and PyEmuera `E_ARGUMENT`. P38 records a Native line-3 IF diagnostic and PyEmuera `E_SYNTAX`; the selected Native crop clips part of a warning. Image interpretation is manual. Execution-time fixture pinning was not established for the error cases; the input cases record the fixture-pin check.

These observations cover only the selected fixtures and conditions. GUI-wide equivalence, IME, concurrent Native jobs, and historical evidence replay are unverified. Original process receipts and attempt seals are not included in the selected public evidence; hashes and a seal do not independently authenticate an execution.

The harness also has offline tests using synthetic logs and mocked processes. These do not constitute Native or PyEmuera observations. The portable semantic audit and whole-attempt resume were also checked against one saved ABS run: both engines recorded 7. This is a single-case check; its original process records are not included here.

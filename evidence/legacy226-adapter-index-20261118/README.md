# Adapter coverage for 226 legacy targets

The latest audit confirms 468 of 694 targets without an additional adapter. The remaining 226 require a legacy or layout adapter. Comparing exact kind and name pairs found in the nine adapter records matches 2 of those rows and leaves 224 unmatched. No audit row directly references the recorded adapter files or directories.

After following recorded array and object pointers, the current public legacy reader produces 35 partial reads, 169 unsupported schemas, and 18 invalid inputs. Partial and unsupported results do not return exit code zero. Full conversion, semantic reproof, and independent reproduction are not established.

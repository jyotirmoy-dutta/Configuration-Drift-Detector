from diff_match_patch import diff_match_patch

def detect_drift(current, baseline):
    dmp = diff_match_patch()
    diffs = {}
    for path, content in current.items():
        base_content = baseline.get(path)
        if base_content is not None:
            diff = dmp.diff_main(base_content, content)
            dmp.diff_cleanupSemantic(diff)
            if any(op != 0 for op, _ in diff):
                diffs[path] = diff
        else:
            diffs[path] = [('ADDED', content)]
    for path, content in baseline.items():
        if path not in current:
            diffs[path] = [('REMOVED', content)]
    return diffs 
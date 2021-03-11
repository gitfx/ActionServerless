
with open('/tmp/test_pre_hook.txt', 'r') as fh:
    # GET /test/result/test_pre_hook
    print(fh.read().splitlines()[0])

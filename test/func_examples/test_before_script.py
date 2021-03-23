
with open('/tmp/test_before_script.txt', 'r') as fh:
    # GET /test/result/test_before_script
    print(fh.read().splitlines()[0])

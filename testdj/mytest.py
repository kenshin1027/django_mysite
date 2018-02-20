def decorator1(func):
    def dec(*args):
        print 'pre action'
        result = func(*args)
        print 'post action'
        return result
    return dec()


@decorator1
def test_f1(name):
    print name
    return None


test_f1('name1')

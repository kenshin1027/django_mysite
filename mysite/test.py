# def fuck(fn):
# 	print("fuck %s!" % fn.__name__[::-1].upper())
# @fuck
# def wfg():
# 	pass

def salesgirl(method):
    def serve(*args):
        print("Salesgirl:Hello, what do you want?", method.__name__)
        method(*args)
    return serve

@salesgirl
def try_this_shirt(size):
    if size < 35:
        print("I: %d inches is to small to me" %(size))
    else:
        print("I:%d inches is just enough" %(size))
try_this_shirt(38)


# Salesgirl:Hello, what do you want? try_this_shirt
# I:38 inches is just enough





















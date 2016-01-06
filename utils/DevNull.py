# Tiny class to silence Python internal error messages

class DevNull:
    def write(self, msg):
        pass

# To silence stderr, simply do:
# sys.stderr = DevNull()


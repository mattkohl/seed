

class Utils:

    @staticmethod
    def clean_key(k):
        return k.replace("@", "").replace("-", "_").replace(":", "_")

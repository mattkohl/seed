

class Utils:

    @staticmethod
    def get_local_name(uri: str) -> str:
        return uri.split("/")[-1]

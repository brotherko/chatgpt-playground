class Singleton:
    __instance = None

    @classmethod
    def getInstance(cls):
        if cls is Singleton:
            return None
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance
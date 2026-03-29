class XenoError(Exception):
    """XENOゲーム全般の基本エラークラス"""
    def __init__(self, message="ゲームエラーが発生しました"):
        self.message = message
        super().__init__(self.message)


class unDrawCard(XenoError):
    def __init__(self):
        super().__init__("カードが出尽くしました。")


class CardNotFoundError(XenoError):
    def __init__(self):
        super().__init__("カードのドローが成功しませんでした。")


class CardActionError(XenoError):
    def __init__(self):
        super().__init__("カードの効果時にエラーが発生しました。")


class CardHaveOver(XenoError):
    def __init__(self):
        super().__init__("カードの規定枚数を超えてます。")

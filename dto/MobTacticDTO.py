class MobTacticDTO:
    def __init__(self, imgPath, tacticRound1, tacticRest, repeatAttack, restingTime, saveSS):
        self.imgPath = imgPath
        self.tacticRound1 = tacticRound1
        self.tacticRest = tacticRest
        self.repeatAttack = repeatAttack
        self.restingTime = restingTime
        self.saveSS = saveSS

    def __str__(self):
        return (
            f"EntityDTO(imgPath={self.imgPath}, tacticRound1={self.tacticRound1}, tacticRest={self.tacticRest}, "
            f"repeatAttack={self.repeatAttack}, restingTime={self.restingTime}, saveSS={self.saveSS})"
        )

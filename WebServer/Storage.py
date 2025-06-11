class Storage:
    def __init__(self, storage=50, consume=0):
        self.storage = storage
        self.consume = consume


    def ConsumeEnergy(self, medValue, consumeValue, isConsuming):
        try:
            if isConsuming:
                self.storage = self.storage + (int(medValue)*0.05) - consumeValue
                self.consume = consumeValue
            else:
                self.storage = self.storage + (int(medValue) * 0.05)
                self.consume = 0

            if(self.storage > 100):
                self.storage = 100
            if(self.storage < 0):
                self.storage = 0

        except:
            pass

class ChargeTime:
    def __init__(self, solar=0, eolic=0, consume=0, usage="Eolic Energy", passive=True):
        self.solar = solar
        self.eolic = eolic
        self.usage = usage
        self.consume = consume
        self.passive = passive

    def setChargeTime(self, solarTime, eolicTime):
        self.solar=solarTime
        self.eolic=eolicTime

    def setConsume(self,consume):
        self.consume=consume

    def setEnergy(self, usageEnergy):
        self.usage = usageEnergy
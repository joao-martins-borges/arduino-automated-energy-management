
def getConsumption(isLights, isWatering, consume):
    value=0
    if isLights:
        value = value + (20*0.1)

    if isWatering:
        value = value + (10*0.1)

    value = value + (consume*0.1)
    return value

from Storage import Storage, ChargeTime

# REQUESTS QUEUE
requests = []

# MEDIÇÕES QUEUES
mlights = []

# STORAGE QUEUES
solarStorage = []
eolicStorage = []

# RULES DICTIONARY
rules = dict()

# STORAGE OBJECTS
solarObject = Storage()
eolicObject = Storage()

chargeTime = ChargeTime()

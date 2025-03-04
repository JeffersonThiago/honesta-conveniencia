from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class UserVeryLowThrottle(UserRateThrottle):
    rate = '3/hour'  

class UserLowThrottle(UserRateThrottle):
    rate = '100/hour' 

class UserModerateThrottle(UserRateThrottle):
    rate = '1000/hour'  

class UserHighThrottle(UserRateThrottle):
    rate = '10000/hour'

class UserExtremeThrottle(UserRateThrottle):
    rate = '50000/hour'

class AnonVeryLowThrottle(AnonRateThrottle):
    rate = '3/minute'  

class AnonLowThrottle(AnonRateThrottle):
    rate = '50/hour'  

class AnonModerateThrottle(AnonRateThrottle):
    rate = '500/hour'  

class AnonHighThrottle(AnonRateThrottle):
    rate = '5000/hour'

class AnonExtremeThrottle(AnonRateThrottle):
    rate = '25000/hour'

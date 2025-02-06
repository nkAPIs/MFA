from InitialValues.InitialValues import get_config
import datetime
import os
class Constants:
    def __init__(self, debugging:bool=False) -> None:
            
        self.debug_mode = debugging
        self.parameters = get_config('mfaAPI', self.debug_mode)
        self.user = self.parameters['user']
        self.password = self.parameters['password']
        self.SECRET_KEY =   self.parameters['SECRET_KEY']
        self.ALGORITHM =   self.parameters['ALGORITHM']
        self.ACCESS_TOKEN_EXPIRE_MINUTES =   self.parameters['ACCESS_TOKEN_EXPIRE_MINUTES']

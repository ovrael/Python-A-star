import math
from enum import Enum
class StatusPola(Enum):
    PUSTE = "white"
    BLOKADA = "black"
    ODWIEDZONE = "wheat"
    GRANICA = "sandy brown"
    SCIEZKA = "green"
    POCZATEK = "magenta"
    KONIEC = "red"

class Pole: 
    def __init__(self, x, y):
        self._status = StatusPola.PUSTE
        self.koszt = 0;
        self.znanaDroga = 0;
        self.przewidywanaDroga = 0;
        self.sasiadujacePola = []
        self.poprzednie = None
        self.x = x
        self.y = y
        self.pokolorowano = False
        
    @property
    def status(self):
        """The status property."""
        return self._status
    @status.setter
    def status(self, value):    
        if not isinstance(value, StatusPola):
            raise Exception("Przypisana wartość do statusu nie jest StatusemPola")
        
        # Zmiena status tylko jeśli aktualne pole nie jest ani początkiem ani końcem
        if(self.status is not StatusPola.KONIEC and self.status is not StatusPola.POCZATEK):
            self._status = value
        
        
    def dodajSasiadujacePole(self, sasiedniePole):
        if sasiedniePole.status is not StatusPola.BLOKADA:
            self.sasiadujacePola.append(sasiedniePole)
    
    def liczKoszt(self):
        self.koszt = self.znanaDroga + self.przewidywanaDroga
    
    # Różne heurystyki
    def policzPrzewidywanaDroge(self, pole2):        
        # return 1.4*max(abs(self.x - pole2.x), abs(self.y - pole2.y)) + min(abs(self.x - pole2.x), abs(self.y - pole2.y))
        # return max(abs(self.x - pole2.x), abs(self.y - pole2.y))
        # return abs(self.x - pole2.x) + abs(self.y - pole2.y)
        return math.sqrt((self.x - pole2.x)**2 + (self.y - pole2.y)**2) - 0.5
        return math.sqrt((self.x - pole2.x)**2 + (self.y - pole2.y)**2) # Działa lepiej z -0.5
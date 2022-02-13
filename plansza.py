from random import randrange
from pole import StatusPola
from pole import Pole

class Plansza:
    def __init__(self, szerokosc, wysokosc, pelneSasiedztwo = True, gestoscBlokad = 0.3):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.pola = [[Pole(i, j) for i in range(szerokosc)] for j in range(wysokosc)]
        self.zamkniety = [] #Zbiór przejrzanych pól
        self.otwarty = []   #Zbiór nieodwiedzonych pól, sąsiadujących z odwiedzonymi
        self.losujPoczatek()
        self.koniec = self.losujKoniec()
        self.losujBlokady(gestoscBlokad)        
        self.sciezka = []
        
        self.dodajSasiadujacePola(pelneSasiedztwo)        
                
    # Każdemu polu przypisuje odpowiednich sąsiadów
    def dodajSasiadujacePola(self, rozszerzone = True): 
        for i in range(self.wysokosc):
            for j in range(self.szerokosc):
                
                if self.pola[i][j].status is StatusPola.BLOKADA:
                    continue
                                
                if i > 0:
                    self.pola[i][j].dodajSasiadujacePole(self.pola[i-1][j])
                    
                if i < self.wysokosc-1:
                    self.pola[i][j].dodajSasiadujacePole(self.pola[i+1][j])   
                              
                if j > 0:
                    self.pola[i][j].dodajSasiadujacePole(self.pola[i][j-1])
                    
                if j < self.szerokosc-1:
                    self.pola[i][j].dodajSasiadujacePole(self.pola[i][j+1])
                
                if rozszerzone:     
                    if i > 0 and j > 0:
                        self.pola[i][j].dodajSasiadujacePole(self.pola[i-1][j-1])
                        
                    if i < self.wysokosc-1 and j > 0:
                        self.pola[i][j].dodajSasiadujacePole(self.pola[i+1][j-1])  
                                
                    if i > 0 and j < self.szerokosc-1:
                        self.pola[i][j].dodajSasiadujacePole(self.pola[i-1][j+1])
                        
                    if i < self.wysokosc-1 and j < self.szerokosc-1:
                        self.pola[i][j].dodajSasiadujacePole(self.pola[i+1][j+1]) 
                     
    
    # Losuje startowe pole z zakresu całej planszy
    def losujPoczatek(self):
        w = randrange(self.wysokosc)
        s = randrange(self.szerokosc)
        
        self.pola[w][s].status = StatusPola.POCZATEK
        self.otwarty.append(self.pola[w][s])
        
    # Losuje końcowe pole z zakresu całej planszy
    def losujKoniec(self):
        w = randrange(self.wysokosc)
        s = randrange(self.szerokosc)

        self.pola[w][s].status = StatusPola.KONIEC
        return self.pola[w][s]
    
            
    # Losuje blokady z zakresu całej planszy
    def losujBlokady(self, gestosc):
        gestosc = int(self.szerokosc*gestosc)
        
        for i in range(self.wysokosc):
            for _ in range(gestosc):
                s = randrange(self.szerokosc)
                
                while self.pola[i][s].status is not StatusPola.PUSTE:
                    s = randrange(self.szerokosc)
                    
                self.pola[i][s].status = StatusPola.BLOKADA

    def czyZnalezionoTrase(self):
        return len(self.otwarty) > 0
    
    # Główny algorytm
    def szukajTrasy(self):
        aktualny = min(self.otwarty, key=lambda x: x.koszt)
         
        if aktualny.status is StatusPola.KONIEC:    
            self.sciezka = []
            tmp = aktualny
            self.sciezka.append(tmp)   
            while tmp.poprzednie is not None:
                self.sciezka.append(tmp.poprzednie)
                tmp = tmp.poprzednie;
            return True;
                                  
        self.otwarty.remove(aktualny)
        self.zamkniety.append(aktualny)
        
        for i in range(len(aktualny.sasiadujacePola)):
            sasiad = aktualny.sasiadujacePola[i]
            
            if sasiad in self.zamkniety:
                continue
            
            if sasiad.status is not StatusPola.BLOKADA:
                niepewnaZnanaDroga = aktualny.znanaDroga + sasiad.policzPrzewidywanaDroge(aktualny)                             
                lepszaNiepewna = False
                     
                if sasiad in self.otwarty:
                    if(niepewnaZnanaDroga < sasiad.znanaDroga):
                        sasiad.znanaDroga = niepewnaZnanaDroga
                        lepszaNiepewna = True
                else:
                    sasiad.znanaDroga = niepewnaZnanaDroga
                    lepszaNiepewna = True
                    self.otwarty.append(sasiad)
                    sasiad.status = StatusPola.GRANICA
                
                if lepszaNiepewna:
                    sasiad.przewidywanaDroga = sasiad.policzPrzewidywanaDroge(self.koniec)
                    sasiad.liczKoszt()
                    sasiad.poprzednie = aktualny
                    aktualny.status = StatusPola.ODWIEDZONE                   
                    
        return False
                
                
                
                
                
                
                
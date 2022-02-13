import math
import graphics as g
from plansza import Plansza
from pole import StatusPola 


class Main:
    def __init__(self):
        # Ustawienia planszy
        self.iloscPolSzer = 90
        self.iloscPolWys = 90
        self.rozmiarPola = 8
        self.gestoscBlokad = 0.45
        self.wysOffset = 50
        self.polowaRozmiaru = None
        self.rozmiarWyroznienia = None
        self.plansza = None
        
        # Obiekty graficzne
        self.graphicsWindow = None
        self.infoText = None
        self.polaDoRysowania = []

    
    # Ustawia parametry planszy za pośrednictwem konsoli
    def kreatorPlanszy(self):
        print("-=-=- KREATOR PLANSZY -=-=-")
        print("Pamiętaj, by tworzyć rozsądne rozmiary dla swojej planszy")
        print("Szerokość oraz wysokość pól należy wymnożyć przez rozmiar pola")
        print("Jeśli wartości będą nie odpowiednie zostaną ustawione domyślne wartości")
        
        try:
            szerokosc = int(input("Wprowadź szerokość wyrażoną w ilości pól (od 5 do 1000): "))        
            if(szerokosc >= 5 and szerokosc <= 1000):
                self.iloscPolSzer = szerokosc            
        except ValueError:
            print("Błędna wartość szerokości")
            
        try:
            wysokosc = int(input("Wprowadź wysokość wyrażoną w ilości pól (od 5 do 1000): "))        
            if(wysokosc >= 5 and wysokosc <= 1000):
                self.iloscPolWys = wysokosc
        except ValueError:
            print("Błędna wartość wysokości")
            
        try:
            rozmiar = int(input("Wprowadź rozmiar pola (od 1 do 25): "))        
            if(rozmiar >= 1 and rozmiar <= 25):
                self.rozmiarPola = rozmiar
        except ValueError:
            print("Błędna wartość rozmiaru")
            
        try:
            gestosc = float(input("Wprowadź szanse na blokade  (od 0.00 do 0.80): "))        
            if(gestosc >= 0 and gestosc <= 0.8):
                self.gestoscBlokad = gestosc
        except ValueError:
            print("Błędna wartość szansy na blokade")      
        
        self.polowaRozmiaru = self.rozmiarPola / 2
        self.rozmiarWyroznienia = self.rozmiarPola * 0.75
        self.rozmiarWyroznienia = self.rozmiarWyroznienia if self.rozmiarWyroznienia <= 6 else 6
        self.rozmiarWyroznienia = 0 if self.rozmiarWyroznienia < 2 else self.rozmiarWyroznienia
        
        self.plansza = Plansza(self.iloscPolSzer, self.iloscPolWys, gestoscBlokad=self.gestoscBlokad)
        self.graphicsWindow = g.GraphWin(title="Algorytm A*", width=self.iloscPolSzer*self.rozmiarPola, height=self.iloscPolWys*self.rozmiarPola+self.wysOffset, autoflush=False)
        self.infoText = g.Text(g.Point(self.iloscPolSzer*self.rozmiarPola/2,self.wysOffset/2), "")
        
        return

    # Tworzy plansze
    def inicjalizujPlansze(self):      
        for i in range(self.iloscPolWys):
            for j in range(self.iloscPolSzer): 
                
                kwadrat = g.Rectangle(g.Point(j*self.rozmiarPola, i*self.rozmiarPola+self.wysOffset), g.Point(j*self.rozmiarPola+self.rozmiarPola, i*self.rozmiarPola+self.rozmiarPola+self.wysOffset))
                kwadrat.setFill(self.plansza.pola[i][j].status.value)
                kwadrat.setWidth(0)
                    
                self.polaDoRysowania.append(kwadrat)
                kwadrat.draw(self.graphicsWindow)
                
        self.wyroznijPoczatekOrazKoniec()
        self.infoText.draw(self.graphicsWindow)
        g.update()

    # Ustawia odpowiednie kolory polom na planszy
    def kolorujPlansze(self):
        for i in range(self.iloscPolWys):
            for j in range(self.iloscPolSzer):
                
                if self.plansza.pola[i][j].pokolorowano:
                    continue
                
                if (self.plansza.pola[i][j].status is not StatusPola.PUSTE
                    and self.plansza.pola[i][j] is not StatusPola.BLOKADA):
                    self.polaDoRysowania[i*self.iloscPolSzer+j].setFill(self.plansza.pola[i][j].status.value)
                    
                    if self.plansza.pola[i][j].status is not StatusPola.GRANICA:
                        self.plansza.pola[i][j].pokolorowano = True
        g.update()

    # Liczy dystans euklidesowy          
    def dystans(self, x1, x2, y1, y2):
            return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    # Rysuje ścieżkę z punkta początkowego do punktu końcowego
    # oraz liczy długość wyznaczonej trasy i wyświetla ją
    def narysujSciezke(self):
        sciezka = self.plansza.sciezka
        dlugoscSciezki = 0
        
        for i in range(len(sciezka)-1):
            punktOd = g.Point(sciezka[i].x*self.rozmiarPola+self.polowaRozmiaru, sciezka[i].y*self.rozmiarPola+self.polowaRozmiaru+self.wysOffset)
            punktDo = g.Point(sciezka[i+1].x*self.rozmiarPola+self.polowaRozmiaru, sciezka[i+1].y*self.rozmiarPola+self.polowaRozmiaru+self.wysOffset)
            linia = g.Line(punktOd, punktDo)
            dlugoscSciezki += self.dystans(sciezka[i].x*self.rozmiarPola+self.polowaRozmiaru, sciezka[i+1].x*self.rozmiarPola+self.polowaRozmiaru, sciezka[i].y*self.rozmiarPola+self.polowaRozmiaru, sciezka[i+1].y*self.rozmiarPola+self.polowaRozmiaru)
            linia.setWidth(self.rozmiarPola * 0.75)
            linia.setFill("green3")
            linia.draw(self.graphicsWindow)   
        
        self.infoText.setText(f"Długość trasy wynosi: {round(dlugoscSciezki,2)}")
        g.update()

    # Otacza punkt startowy i końcowy okręgiem
    def wyroznijPoczatekOrazKoniec(self):
        punkty = 0
        for i in range(self.iloscPolWys):
            for j in range(self.iloscPolSzer):
                
                if(punkty >= 2):
                    break
                
                if self.plansza.pola[i][j].status is StatusPola.POCZATEK or self.plansza.pola[i][j].status is StatusPola.KONIEC:
                    punkty+=1
                    wyroznienie = g.Circle(g.Point(j*self.rozmiarPola+self.polowaRozmiaru, i*self.rozmiarPola+self.polowaRozmiaru+self.wysOffset), 3*self.rozmiarPola)
                    wyroznienie.setOutline(g.color_rgb(65, 252, 3))    
                    wyroznienie.setWidth(self.rozmiarWyroznienia)
                    wyroznienie.draw(self.graphicsWindow)

    def uruchom(self):
        self.kreatorPlanszy()
        self.inicjalizujPlansze()

        self.infoText.setText("Trwa obliczanie trasy...")
        
        while(self.plansza.czyZnalezionoTrase()):
            if self.plansza.szukajTrasy():
                self.narysujSciezke()
                break;
            self.kolorujPlansze() 
        
        if not self.plansza.czyZnalezionoTrase():
            self.infoText.setText("Nie znaleziono trasy :(")

        self.graphicsWindow.getMouse()
        self.graphicsWindow.close()


program = Main()
program.uruchom()

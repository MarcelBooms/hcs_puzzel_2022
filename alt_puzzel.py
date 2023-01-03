veldgrootte=30
maxaantalgetallen=15

vulblokje='Y'
kruisje="."
leegveld="_"
  
tabel=[[leegveld for n in range(veldgrootte)] for n in range(veldgrootte)]
tabel2_x=[[] for n in range(veldgrootte)]
tabel2_y=[[] for n in range(veldgrootte)]

tabel2_xx=[0 for n in range(veldgrootte)]
tabel2_yy=[0 for n in range(veldgrootte)]

gx=[[] for n in range(veldgrootte)]
gy=[[] for n in range(veldgrootte)]



def lees_rij():
  # Makkelijke manier om alle rijen uit te lezen
  global gx
  global veldgrootte
  f = open('input_kerstpuzzel2022_rij.txt','r')
  regels = f.readlines()
  m=0
  for regel in regels:
    getallen = regel.strip().split('\t')
    totaal = 0
    for n in range(len(getallen)):
      totaal += int(getallen[n])
    totaal += len(getallen)-1 if totaal else 0
    ruimte = veldgrootte-totaal
    begin = 0
    for n in range(len(getallen)):
      gx[m].append({'ruimte': ruimte ,'getal':int(getallen[n])})
      begin += int(getallen[n]) + 1
    m+=1

def lees_kolom():
  # Makkelijke manier om alle kolommen uit te lezen
  global gy
  global veldgrootte
  f = open('input_kerstpuzzel2022_kolom.txt','r')
  regels = f.readlines()
  m=0
  for regel in regels:
    getallen = regel.strip().split('\t')
    totaal = 0
    for n in range(len(getallen)):
      totaal += int(getallen[n])
    totaal += len(getallen)-1 if totaal else 0
    ruimte = veldgrootte-totaal
    begin = 0
    for n in range(len(getallen)):
      gy[m].append({'ruimte': ruimte,'getal':int(getallen[n])})
      begin += int(getallen[n]) + 1
    m+=1

def print_tabel():
  # print de tabel
  n=0
  for regel in tabel:
    cijfers=''
    for cijfer in gx[n]:
      if cijfer['getal']:
        cijfers += str(cijfer['getal']) + ' '
      elif not cijfers:
        cijfers='0'    
    print(' '.join(regel)," ",cijfers)
    n+=1
    
  print()
  rij1=True
  rij=0
  for kolom in range(maxaantalgetallen-1):
    cijfers=''
    for cijfer in gy:
      if rij1 or (len(cijfer)>kolom and cijfer[kolom]['getal']):
        cijfers += (str(cijfer[kolom]['getal']) + ' ')[:2]
      else:
        cijfers += '  '
    print(cijfers)
    rij += 1
    rij1=False

def check_alle_mogelijkheden(m, kolom, speling_totaal, speling_max):
  # print('== blabla(m,',kolom,',',speling_totaal,',',speling_max,')')
  blok = []
  # print("speling_max (",speling_max,") - speling_totaal(",speling_totaal,") =", speling_max - speling_totaal)
  for spel in range(speling_max - speling_totaal + 1):
    # print(spel, 'blabla kolom=',kolom, "extra x=",spel, "Max speling=",speling_max)    
    tekst = kruisje * spel + vulblokje * m[kolom]['getal'] 
    if kolom == len(m)-1:
      tekst += kruisje * (speling_max - speling_totaal - spel )
    if kolom < len(m)-1:
      antwoord = check_alle_mogelijkheden(m, kolom + 1, speling_totaal + spel, speling_max )
    else:
      antwoord = []
    for antw in antwoord:
      # print('Adding kolom ' , kolom , tekst + " " + antw)
      blok.append( tekst + kruisje + antw )
    if kolom == len(m) -1:
      blok.append(tekst)
  # print("Returning ",blok)
  return blok


#mylist = list(dict.fromkeys(mylist))

def bouw_alle_rijen():
  # m=gx[29]
  # m=[{'begin':0,'eind':4,'getal':2},{'begin':2,'eind':4,'getal':1},{'begin':2,'eind':4,'getal':2}]
  # m=[{'begin':0,'eind':29,'getal':0}]
  # print(m)
  # print(check_alle_mogelijkheden(m,0,0,m[0]['ruimte']))
  
  for n in range(veldgrootte):
    tabel2_x[n]=list(dict.fromkeys(check_alle_mogelijkheden(gx[n],0,0,gx[n][0]['ruimte'])))
    tabel2_y[n]=list(dict.fromkeys(check_alle_mogelijkheden(gy[n],0,0,gy[n][0]['ruimte'])))
      

def verwijder_kolommen(rij_nr):
  # print(tabel2_x[rij_nr])
  tekst=tabel2_x[rij_nr][0]
  verwijderd=False
  for n in range(veldgrootte-1):
    c=tekst[n]
    gevonden=True
    teller=0
    while teller < len(tabel2_y[n]):
      if tabel2_y[n][teller][rij_nr] != c:
        tabel2_y[n].remove(tabel2_y[n][teller])
        verwijderd=True
      else:
        teller+=1
  return verwijderd

def verwijder_rijen(kolom_nr):
  # print(tabel2_y[kolom_nr])
  tekst=tabel2_y[kolom_nr][0]
  verwijderd=False
  for n in range(veldgrootte-1):
    c=tekst[n]
    gevonden=True
    teller=0
    while teller < len(tabel2_x[n]):
      if tabel2_x[n][teller][kolom_nr] != c:
        tabel2_x[n].remove(tabel2_x[n][teller])
        verwijderd=True
      else:
        teller+=1
  return verwijderd


def controleren():
  rijen=[]
  kolommen=[]
  
  for m in range(veldgrootte):
    print("Rij " , m , " heeft ",len(tabel2_x[m]),"mogelijkheden")    
  for m in range(veldgrootte):
    print("Kolom " , m , " heeft ",len(tabel2_y[m]),"mogelijkheden")
  print()

  # verwijderd=True
  # while verwijderd:
  #   for n in range(veldgrootte):
  #     if len(tabel2_x[n]) == 1:
  #       if not n in kolommen:
  #         print("Rij ",n," heeft 1 oplossing. Verwijder alle andere mogelijkheden uit de kolommen tabel")
  #         verwijderd = verwijder_kolommen(n)
  #         kolommen.append(n)
  
  #   for n in range(veldgrootte):
  #     if len(tabel2_y[n]) == 1:
  #       if not n in rijen:
  #         print("Kolom ",n," heeft 1 oplossing. Verwijder alle andere mogelijkheden uit de rijen tabel")
  #         verwijderd = verwijder_rijen(n)
  #         rijen.append(n)
    
  #   print()
  #   for m in range(veldgrootte):
  #     print("Rij " , m , " heeft ",len(tabel2_x[m]),"mogelijkheden")    
  #   for m in range(veldgrootte):
  #     print("Kolom " , m , " heeft ",len(tabel2_y[m]),"mogelijkheden")
      
def main():
  lees_rij()
  lees_kolom()
  bouw_alle_rijen()
  controleren()
  for n in tabel2_x:
    print(n)

  
if __name__ == "__main__":
  main()

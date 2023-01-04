import timeit

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
      

# Op basis van de mogelijke opties op rij rij_nr wordt er gekeken per positie
# gekeken of in de kolomen er opties zijn die niet aan de oplossing voldoen.
# Dus als in kolom 1 van rij rij_nr een Y staat dan kunnen alle oplossingen in
# de kolommen tabel die op kolom 1 van rij rij_nr een '.' hebben staan,
# verwijderd worden. Dit verkleint de dataset van mogelijke oplossingen  
def verwijder_kolommen(rij_nr):
  # print("Processing rij",rij_nr)
  tekst=list(tabel2_x[rij_nr][0])
  # print("Originele tekst: ",''.join(tekst))
  # Als de set meerderde oplossingen heeft dan wordt er gekeken welke posities
  # dezelfde waarden hebben 'Y' of '.' voor alle oplossingen.
  # Bij een verschil wordt het filter een '?' en genegeerd bij vergelijkingen.
  for n in range(len(tabel2_x[rij_nr])):
    for m in range(veldgrootte):
      if tekst[m] != '?' and tekst[m] != tabel2_x[rij_nr][n][m]:
        tekst[m]='?'
  # print("Nieuwe tekst   : ",''.join(tekst))
  return verwijder_kolom(tekst, rij_nr)

def verwijder_kolom(filter, rij_nr):
  pass
  verwijderd=False
  for n in range(veldgrootte):
    # print("Processing rij",rij_nr,"kolom",n)
    c=filter[n]
    nieuwe_tabel=[]
    # print("len",len(tabel2_y[n]), tabel2_y[n])
    for optie in range(len(tabel2_y[n])):
      # print(n,rij_nr,optie,tabel2_y[n][optie][rij_nr],'=',c)
      if tabel2_y[n][optie][rij_nr] == c or c == '?':
        nieuwe_tabel.append(tabel2_y[n][optie])
      else:
        # print("Optie ",m," wordt verwijderd")
        verwijderd=True
    # print("Clearing table. Table was",len(tabel2_y[n]))
    tabel2_y[n].clear
    if len(nieuwe_tabel) == 0:
      print("Wat gaat hier fout?")
      print("Filter :"+''.join(tekst))
      for n in tabel2_y[n]:
        print(''.join(n))
      raise Exception('Verwijder_kolommen: Wat gaat hier fout?')
    tabel2_y[n]=nieuwe_tabel
    # print("Adding new table. Table is",len(tabel2_y[n]))
  return verwijderd

def verwijder_rijen(kolom_nr):
  # print("Processing kolom",kolom_nr)
  tekst=list(tabel2_y[kolom_nr][0])
  # print("Originele tekst: ",tekst)
  for n in range(len(tabel2_y[kolom_nr])):
    pass
    for m in range(veldgrootte):
      if tekst[m] != '?' and tekst[m] != tabel2_y[kolom_nr][n][m]:
        tekst[m]='?'
  # print("Nieuw tekst    : ",''.join(tekst))
  return verwijder_rij(tekst, kolom_nr)

def verwijder_rij(filter, kolom_nr):
  pass
  verwijderd=False
  for n in range(veldgrootte):
    c=filter[n]
    nieuwe_tabel=[]
    for m in range(len(tabel2_x[n])):
      if c == '?' or tabel2_x[n][m][kolom_nr] == c or c == '?':
        nieuwe_tabel.append(tabel2_x[n][m])
      else:
        # print("Optie ",m," wordt verwijderd")
        verwijderd=True
    # print("Clearing table. Table was",len(tabel2_x[n]))
    tabel2_x[n].clear    
    if len(nieuwe_tabel) == 0:
      print("Wat gaat hier fout?")
      raise Exception('Wat gaat hier fout?')
    tabel2_x[n]=nieuwe_tabel
    # print("Adding new table. Table is",len(tabel2_x[n]))
  return verwijderd

def controleren():
  rijen=[]
  kolommen=[]
  
  verwijderd=True
  run=0
  while verwijderd:
    verwijderd=False
    run+=1
    if run>100:
      break
    print("Run ",run)
    for n in range(veldgrootte):
      print("Rij " , n , " heeft ",len(tabel2_x[n]),"mogelijkheden")
      print("Rij ",n," heeft ",len(tabel2_x[n])," oplossing(en). Verwijder andere mogelijkheden uit de kolommen tabel")
      verwijderd = verwijder_kolommen(n)
      kolommen.append(n)
  
    for n in range(veldgrootte):
      print("Kolom " , n , " heeft ",len(tabel2_y[n]),"mogelijkheden")    
      if len(tabel2_y[n]) <= 1000:
        # if not n in rijen:
      print("Kolom ",n," heeft ",len(tabel2_y[n])," oplossing(en). Verwijder andere mogelijkheden uit de rijen tabel")
      verwijderd = verwijder_rijen(n)
      rijen.append(n)

def vul_tabel():
  for rij_nr in range(veldgrootte):
    # print("Processing rij",rij_nr)
    tekst=list(tabel2_x[rij_nr][0])
    # print("Originele tekst: ",''.join(tekst))
    for n in range(len(tabel2_x[rij_nr])):
      for m in range(veldgrootte):
        if tekst[m] != '_' and tekst[m] != tabel2_x[rij_nr][n][m]:
          tekst[m]='_'
    # print("Nieuwe tekst   : ",''.join(tekst))
    for kolom_nr in range(veldgrootte):
      tabel[rij_nr][kolom_nr]=tekst[kolom_nr]    

      
def main():
  lees_rij()
  lees_kolom()
  bouw_alle_rijen()
  controleren()
  vul_tabel()
  print_tabel()
  
if __name__ == "__main__":
  main()

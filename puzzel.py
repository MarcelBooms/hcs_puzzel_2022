veldgrootte=30
maxaantalgetallen=15
  
tabel=[['.' for n in range(veldgrootte)] for n in range(veldgrootte)]
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
      gx[m].append({'begin':begin,'eind':begin + int(getallen[n]) + ruimte -1,'getal':int(getallen[n])})
      # print({'begin':begin,'eind':begin + int(getallen[n]) + ruimte - 1,'getal':int(getallen[n])})
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
      gy[m].append({'begin':begin,'eind':begin + int(getallen[n]) + ruimte - 1,'getal':int(getallen[n])})
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

def check_volledige_rij_kolom():
  # Check elke rij & kolom waarvan de vrijheid van de te plaatsen
  # blokjes/kruisjes 0 is. 
  global tabel,gx,gy
  aangepast=False
  for y in range(veldgrootte):
    kruizen=0
    for x in range(veldgrootte):
      kruizen+=1 if tabel[y][x]=='x' else 0
    totaal=0
    for n in gx[y]:
      totaal+=n['getal']
    totaal+=len(gx[y])-1 # Voeg verplichte lege vakjes toe.
    if kruizen + totaal == veldgrootte or totaal == 0:
      print("Rij " + str(y) + " kan volledig gevuld worden")
      if vul_rij_kolom('r',y):
        aangepast=True
    else:
      print("Rij " + str(y) + " heeft " + str(kruizen) + " kruizen en " + str(totaal) + " blokjes. veldgrootte = " + str(veldgrootte))
      
  for x in range(veldgrootte):
    kruizen=0
    for y in range(veldgrootte):
      kruizen+=1 if tabel[y][x]=='x' else 0
    totaal=0
    for n in gy[x]:
      totaal+=n['getal']
    totaal+=len(gy[x])-1   # Voeg verplichte lege vakjes toe.
    if kruizen + totaal == veldgrootte or totaal == 0:
      print("Kolom " + str(x) + " kan volledig gevuld worden")
      if vul_rij_kolom('k',x):
        aangepast = True
    else:
      print("Kolom " + str(x) + " heeft " + str(kruizen) + " kruizen en " + str(totaal) + " blokjes. veldgrootte = " + str(veldgrootte))
  return aangepast

def vul_rij_kolom(richting,pos):
  # Vul de rij/kolom in tabel waarvan de vrijheid te plaatsen blokjes 0 is.
  aangepast=False
  o=0
  totaal=0
  if richting == 'r':
    for n in gx[pos]:
      totaal+=n['getal']
    for n in range(veldgrootte):
      if tabel[pos][n] == '.':
        if o<len(gx[pos]):
          for m in range(gx[pos][o]['getal']):
            tabel[pos][n+m]="Y"
            aangepast=True
          n += gx[pos][o]['getal']
          o += 1
        if n < veldgrootte and tabel[pos][n]=='.':
          tabel[pos][n]='x'
          aangepast=True
  else:
    for n in gy[pos]:
      totaal+=n['getal']
    for n in range(veldgrootte):
      if tabel[n][pos] == '.':
        if o < len(gy[pos]):
          for m in range(gy[pos][o]['getal']):
            tabel[n+m][pos]="Y"
            aangepast=True
          n += gy[pos][o]['getal']
          o += 1
        if n < veldgrootte and tabel[n][pos]=='.':
          tabel[n][pos]='x'
          aangepast=True
  return aangepast

def vul_blokjes_in():
  # Check iedere rij/kolom op velden die zowieso een blokje zijn.
  # Een rij blokjes van 7 en een vrijheid van 1 heeft zowieso 5 blokjes
  aangepast=False
  for n in range(veldgrootte):
    for m in gx[n]:
      if m['begin'] + m['getal'] > m['eind'] - m['getal']:
        speling=m['eind']-m['begin']-m['getal']
        for o in range(m['begin']+speling, m['eind']-speling):
          tabel[n][o]="Y"
          aangepast=True
    for m in gy[n]:
      if m['begin'] + m['getal'] > m['eind'] - m['getal']:
        speling=m['eind']-m['begin']-m['getal']
        for o in range(m['begin']+speling, m['eind']-speling):
          tabel[o][n]="Y"
          aangepast=True
  return aangepast

def aanvullen():
  for n in range(veldgrootte):
    print_tabel()
    print("Regel ",n)
    for m in gx[n]:
      if tabel[n][m['begin']] == 'Y' and (m['begin'] == 0  or tabel[n][m['begin']-1] == 'x'):
        for o in range(m['begin'], m['begin']+ m['getal']-1):
          if tabel[n][o]==".":
            tabel[n][o]="Y"
            aangepast=True
          m['eind']=m['begin']+ m['getal']-1
        if m['begin']+ m['getal'] < veldgrootte:
          tabel[n][m['begin']+ m['getal']]='x'
    for m in gy[n]:
      if tabel[m][n['begin']] == 'Y' and (m['begin'] == 0  or tabel[m][n['begin']-1] == 'x'):
        for o in range(m['begin'], m['begin']+ m['getal']-1):
          if tabel[o][n]==".":
            tabel[o][n]="Y"
            aangepast=True
          m['eind']=m['begin']+ m['getal']-1
        if m['begin']+ m['getal'] < veldgrootte:
          tabel[m['begin']+ m['getal']][n]='x'




    
            
    # for m in range(len(gx[n])-1):
    #   vorig_eind=gx[n][m-1]['eind'] if m>0 else 0
    #   if m < len(gx[n])-1:
    #     volgend_begin=gx[n][m+1]['begin']
    #   else:
    #     gx[n][m]['eind']+1
    #   ruimte = gx[n][m]['eind'] - gx[n][m]['begin'] + 1 - gx[n][m]['getal']
    #   print("begin", gx[n][m]['begin'],"eind", gx[n][m]['eind'],"getal",gx[n][m]['getal'] )
    #   # controle op precies aantal
    #   print('controle')
    #   print("gx[n][m]['begin'] >= vorig_eind and ruimte>0   ", gx[n][m]['begin'],">=",vorig_eind," ruimte=",ruimte)
    #   if ruimte == 0:
    #     for o in range(gx[n][m]['begin'], gx[n][m]['begin']+ gx[n][m]['getal']-1):
    #       if tabel[n][o]==".":
    #         tabel[n][o]="Y"
    #         aangepast=True
    #     if gx[n][m]['begin']+ gx[n][m]['getal'] < veldgrootte:
    #       tabel[n][gx[n][m]['begin']+ gx[n][m]['getal']]='x'
    #   # controle op begin + x ervoor
    #   elif gx[n][m]['begin'] >= vorig_eind and ruimte>0:
    #     print("aan het begin")
    #     for o in range(gx[n][m]['begin'],gx[n][m]['begin']+ruimte):
    #       if tabel[n][o] == 'x':
    #         gx[m]['begin']=o
    #   # controle op eind + x erachter
    #   elif gx[n][m]['eind'] <= volgend_begin and ruimte>0:
    #       for o in range(gx[m]['eind'],gx[m]['eind']-ruimte,-1):
    #         if tabel[n][o] == 'x':
    #           gx[n][m]['eind']=o

    # for m in range(len(gy[n])-1):
    #   vorig_eind=gy[n][m-1]['eind'] if m>0 else 0
    #   if m < len(gy[n])-1:
    #     volgend_begin=gy[n][m+1]['begin']
    #   else:
    #     gy[n][m]['eind']+1
    #   ruimte = gy[n][m]['eind'] - gy[n][m]['begin'] + 1 - gy[n][m]['getal']
    #   # controle op precies aantal
    #   if ruimte == 0:
    #     for o in range(gy[n][m]['begin'], gy[n][m]['begin']+ gy[n][m]['getal']-1):
    #       if tabel[o][n]==".":
    #         tabel[o][n]="Y"
    #         aangepast=True
    #   # controle op begin + x ervoor
    #   elif gy[n][m]['begin'] >= vorig_eind and ruimte>0:
    #      for o in range(gy[n][m]['begin'],gy[n][m]['begin']+ruimte):
    #        if tabel[o][n] == 'x':
    #          gy[n][m]['begin']=o
    #   # controle op eind + x erachter
    #   elif gy[n][m]['eind'] <= volgend_begin and ruimte>0:
    #      for o in range(gy[m]['eind'],gy[m]['eind']-ruimte,-1):
    #        if tabel[o][n] == 'x':
    #          gy[n][m]['eind']=o
      
      
      
    #   if tabel[n][gx[m]['begin']] == 'Y':
    #     print("Rij vullen van ",m['begin'],"tot", m['begin']+ m['getal']-1)
    #     for o in range(gx[m]['begin'], gx[m]['begin']+ gx[m]['getal']-1):
    #       tabel[n][o]="Y"
    #     tabel[n][gx[m]['begin']+ gx[m]['getal']]='x'
    #     gx[m]['eind']=gx[m]['begin']+ gx[m]['getal']-1
    #     aangepast=True
    #   print("After m['begin']=",m['begin'],"m['eind']",m['eind'],"m['getal']",m['getal'])
          
    # for m in gy[n]:
    #   if tabel[m['begin']][n] == 'Y':
    #     for o in range(m['begin'], m['begin']+ m['getal']-1):
    #       tabel[o][n]="Y"
    #     tabel[m['begin']+ m['getal']][n]='x'
    #     m['eind']=m['begin']+ m['getal']-1
    #     aangepast=True
        
        
def los_puzzel_op():
  aangepast=check_volledige_rij_kolom()
  while aangepast:
    aangepast = check_volledige_rij_kolom()
    print('Nog een keer')
    vul_blokjes_in()
    aanvullen()

def main():
  lees_rij()
  lees_kolom()
  los_puzzel_op()
  print_tabel()
  
  
if __name__ == "__main__":
  main()

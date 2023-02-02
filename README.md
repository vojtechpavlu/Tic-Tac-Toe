# Piškvorky

Projekt pro demonstraci principů symbolických metod pro řešení 
problémů ve stavovém prostoru. Konrkétně je cílem demonstrovat možné přístupy
k hledání optimální strategie v pomocí soupeřivého prohledávání v rámci tématu
teorie her. 

Tento projekt byl vyvinut jako studijní pomůcka pro výuku umělé 
inteligence při 
[Smíchovské střední průmyslové škole a gymnáziu](https://www.ssps.cz/).

---

Projekt plní několik základních rolí. V první řadě stanovuje základní 
jednoduchý framework pro jednoduchou hru piškvorky, obsahuje základní definici
obecného hráče a definuje způsob interakce mezi hráčem a hrou tak, aby bylo
zajištěno, že takový hráč nemůže podvádět.


<br />

**Zajímavé odkazy:**
- [Graf na Wikipedii](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics))
- [Stavový prostor na Wikipedii](https://en.wikipedia.org/wiki/State_space)
- [Teorie her na Wikipedii](https://en.wikipedia.org/wiki/Game_theory)
- [Minmax algoritmus na Wikipedii](https://en.wikipedia.org/wiki/Minimax)
- [Alfa-beta prořezávání na Wikipedii](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
- [Studijní materiály na Google Drive](https://tinyurl.com/ssps-umela-inteligence)


## Hra

Samotná hra je postavena na principu střídavých tahů dvou hráčů, kteří své 
tahy provádí postupným označováním políček. Jejich cílem je nepřerušovaně 
spojit linii políček přes celou hrací plochu. Tato linie může být chápána
jako vertikální (sloupec), horizontální (řádek) nebo diagonální (z levého 
dolního rohu do pravého horního či z pravého dolního do levého horního).
Alternativním zakončením hry je remíza, kdy doposud nebyla spojena žádná
linie, ale již neexistuje žádný další možný tah.

Tato jednoduchá pravidla jsou kontrolována v rámci instancí třídy `Game`,
která celý postup hry řídí. Používá k tomu pomocných služebníků pro rozpoznání
konce hry. Za tímto účelem byla navržena abstraktní třída `EndRecognizer`, 
která na požádání dokáže různé konce rozpoznat. Jmenovitými potomky 
(konkrétními implementacemi) jsou třídy: 

- `Column`, 
- `Row`, 
- `RightLeftDiagonal` a `LeftRightDiagonal`,
- `NoMoreMoves`

Při úspěšném dokončení hry (s výsledkem výhry či remízy) je vyhozena příslušná
výjimka (`Win` nebo `Draw`), která je typicky v rámci běhu hry odchycena a
vyhozením obecné výjimky `GameOver` je samotná hra ukončena.


## Hrací plocha

Hrací plocha je volně řečeno soubor vzájemně sousedících políček a který
reprezentuje v každém momentu hry množinu označených políček jedním či druhým
hráčem. Konkrétní implementaci hrací plochy lze nalézt v definici třídy 
`Board`, jejíž instance slouží jako kontejnery pro sady políček hry.

Velikost hrací plochy se odvíjí od své bazální (základní) velikosti, která
odpovídá odmocnině z počtu políček (předpokládá se čtvercová hrací plocha). 
Proto například hrací plocha `3x3` o 9 políčích má základní veliksot `3`.
Ikdyž by to pravidlům hry *de facto* neodporovalo, z praktických důvodů je
tato velikost omezena na rozmezí $[1,9]$ (tedy jednociferná čísla).

Každé políčko je v rámci implementace chápáno jako jakási přepravka obsahující
souřadnice políčka (v osách `x` a `y`) a případné označení jednoho z hráčů.
Konkrétní implementaci lze nalézt ve třídě `Field`.

Aby byla zajištěna bezpečnost a hráč neměl možnost jakkoliv podvádět, je mu
předán vždy jen obalený *proxy* objekt, který symbolizuje podstatné vlastnosti
příslušné instance. Takovými objekty jsou instance třídy `BoardSnapshot` a 
`FieldClosure`.

Hrací plochu je možné tvořit samostatně iniciací vlastních políček, ale 
doporučeným postupem je použití funkce `default_board(int) -> Board` v modulu
`./src/game/board`, která připraví hrací plochu z dodané bazální velikosti.

## Hráč

Nad rámec frameworku projekt dále definuje základní hráče (viz balíček 
`./src/players`):

- **Lidský hráč** (`HumanPlayer`), který umožňuje zkoušet hru člověkem
- **Náhodný hráč** (`RandomNPCPlayer`), který umožňuje demonstrovat hru 
neracionálního agenta, který své tahy volí zcela nahodile z dodaných možných
- **Minmax hráč** (`MinmaxPlayer`), který umožňuje demonstrovat racionálního
strojového hráče

Obecný protokol hráče je definován abstraktní třídou `Player` v balíčku 
`./src/game/`, jejíž instance jsou především nositeli jména hráče, znaku 
(pomocí kterého políčka svých tahů označují, typicky `X` nebo `O`) a metody, 
která hráčův tah umožňuje. Tato je popsána signaturou 
`move(BoardSnapshot, tuple[str]) -> str`, je tedy hráči poskytnut aktuální
snímek hrací plochy a sada povolených tahů, které může provést. Z nich je jeho
cílem vybrat právě jeden. Pokud vybere jako svůj tah takový, který mezi 
povolenými tahy není, svůj tah musí hráč opakovat. Podoba tahů je odvozena
od souřadnic políček, které chce hráč označit, podle vzoru `X Y`, tedy např.
`1 2`.

Díky této konstrukci je možné standardizovat hráče co do jeho vnějších projevů,
neboť se kromě bonity svých tahů chovají ve hře v podstatě identicky.

### Lidský hráč (`HumanPlayer`)

Lidský hráč je implementován tak, aby uživateli umožnil dodat svůj tah přes
konzolový vstup. Je tedy pomocí built-in funkce `input` vyzván, aby svůj tah
v každé iteraci dodal.


### Náhodný hráč (`RandomNPCPlayer`)

Náhodný hráč je neracionálním agentem. Své tahy volí zcela na základě náhody
z dodaných tahů, které jsou pro jeho tah povoleny. Toho je dosaženo pomocí
funkce `random.choice(Iterable[T]) -> T`, která vrací jeden náhodný element
z dodané iterovatelné sekvence. V tomto případě z množiny povolených tahů.


### Minmax hráč (`MinmaxPlayer`) <a id="minmax-player"></a>

Automatický hráč, který své tahy volí na základě minmax algoritmu.

Celý princip algoritmu vychází z teorie rozhodování a je založen na
volbě rozhodnutí na základě tzv. *garančního prinicpu*. Ten nám říká, že
optimálního rozhodnutí lze dosáhnout pouze tak, že budeme uvažovat tu
nejlepší alternativu z těch nejhorších. Důvodem je, že cílení na absolutní
maximum užitkové funkce (resp. minimum funkce cenové) není vhodnou strategií,
neboť nejsme schopni vyloučit, že uvízneme v lokálním extrému. V teorii her 
pak předpokládáme, že náš oponent (antagonista) bude volit tahy stejně 
racionálně, jako my a udělá vše pro to, aby naši výplatní funkci minimalizoval.

Matematizovat by šel tento vztah následovně:

Mějme matici hodnot výpatních funkcí pro kombinaci zvolených strategií oběma
hráči

 ```math
 
 \begin{pmatrix}
 u_{11} & u_{12} & \dots & u_{1k} \\
 u_{21} & u_{22} & \dots & u_{2k} \\
 \vdots & \vdots & \ddots & \vdots \\
 u_{j1} & u_{j2} & \dots & u_{jk} \\
 \end{pmatrix}
 
 ```

užitek z rozhodnutí hráče 1 (výběr v řádku) se odvíjí i od rozhodnutí hráče 2
(výběr sloupečku). Uvědomme si, že $j$ se nemusí nutně rovnat $k$, tedy že 
každý z hráčů může stát před vícero svými rozhodnutími, jejichž počet nemusí
být pro oba stejný. 

Jelikož u obou hráčů předpokládáme racionalitu, nemá smysl uvažovat


- **Rozhodování za rizika** - oponent nevybírá tahy na základě náhody
  (nejde o hru proti přírodě), čímž se tato varianta vylučuje
  
```math
    i^{*} = \max_{i} \sum_{j=1}^{t} u_{jk} \cdot p_{j}
```

- **Princip maximální entropie** - oponent vybírá své tahy v transparentní 
  snaze minimalizovat náš užitek, s čímž se tento přístup zdá být neefektivní
  
```math
    i^{*} = \max_{i} \sum_{j=1}^{t} u_{jk}
```

Oproti tomu garanční minmax strategie uvažuje, že racionální hráč se nám bude
snažit *"házet klacky pod nohy"* a bude tedy dělat takové tahy, které nám
pokud možno co nejvíce sníží hodnotu užitkové funkce.

```math
    i^{*} = \max_{j} \min_{k} u_{jk}
```

Jak je vidět na tomto vzorci, vybíráme tedy nejlepší z nejhorších možných 
řešení. Při správném zakomponování této idee do algoritmu pak můžeme dosáhnout
programu strojového hráče, který nemůže prohrát - volí totiž tahy uvažujíce i
zastoupení strategie oponenta (hledáme takzvaný
[sedlový bod](https://cs.wikipedia.org/wiki/Strategie_(teorie_her)#Sedlov%C3%BD_bod)).

Konkrétní použitá implementace vychází z aplikace tohoto přístupu a prostého
backtrackingu, tedy rekurzivně zkoušíme prohledávat do hloubky - aplikací tahů.
Střídáme přitom maximalizační a minimalizační funkci (zastoupení obou hráčů),
abychom vypočítali racionální průběh hry.

S tím však přichází problém s komplexitou hry. Přestože se piškvorky zdají 
býti hrou zcela banální, tento algoritmus se může potýkat se svými nedostatky.
Sice garantuje, že nikdy neprohraje (nejhorší možný výsledek je remíza), ale
naráží na problém s časovou složitostí - jde o tzv. *brute force* algoritmus.
Celá implementace stojí na prostém vybudování celého stormu, z jehož listů
*probublává* až ke kořeni kvalita sekvence rozhodnutí (vedoucí k terminálním
uzlům). Počet uzlů, které se musí prohledat značně omezuje použití v reálném
čase. Pro piškvorky o větší než 9polní hrací ploše se stává kvůli výpočetní
složitosti již prakticky nepoužitelným.


### Heuristický hráč

Abychom kompenzovali složitost výběru dalšího tahu pro (Minmax hráče)[#minmax-player],
lze použít vícero strategií. Jednou z nich je heuristické ohodnocování bonity
tahu v ještě nedokončené hře (tedy když ani jeden z hráčů ještě nevyhrál a zároveň
nebyla remíza).

Třídu tohoto hráče lze nalézt v modulu `players/rational_npc_player/heuristic_minmax_npc.py`,
pod názvem `LimitedMinmaxPlayer`, což zdůrazňuje skutečnou podstatu výhody hráče - 
prohledávání pouze do omezené hloubky.

K tomu byla definována sada evaluačních funkcí, které dokáží hrací plochu ohodnotit
co do potenciálu k výhře. Tyto lze nalézt v modulu `players/rational_npc_player/evaluators.py`.
Díky tomu lze budovat podobný strom reprezentující všechny posloupnosti rozhodování
jen do stanovené hloubky; listy v takto zadané hloubce stromu pak nemusí nutně být
koncem hry a přesto mohou sloužit k rozhodnutí.

Celý princip lze matematizovat následovně:

```math
  \forall s \in S, f(s) \rightarrow \mathbb{R}
```

tedy že na libovolný stav $s$ z množiny přípustných stavů $S$ lze aplikovat 
evaluační funkci $f$, která tento převádí na reálné číslo.

Tyto evaluační funkce se liší především v cílové vlastnosti rozložení hrací plochy,
tedy měří míru potenciálu výhry v řádcích, sloupcích a na diagonálách. Stejně tak
rozlišují významnost pro daného hráče, tedy zda-li odpovídají spíše defensivě či ofensivě.

Dalším důležitou vlastností těchto evaluačních funkcí je skutečnost, že je možné
tyto ovlivňovat co do významu - kvantifikátoru sledování.

Pro příklad lze uvést následnou implementaci takového hráče vybaveného
heuristickými funkcemi:

```python
npc = LimitedMinmaxPlayer(
    player_name="Limited Minmax", mark="O", max_depth=5, evaluators=[
        OffensiveProgressInRow(weight=3),
        OffensiveProgressInColumn(weight=3),
        OffensiveProgressInFirstDiagonal(weight=3),
        OffensiveProgressInSecondDiagonal(weight=3),
        DefensiveProgressInRow(),
        DefensiveProgressInColumn(),
        DefensiveProgressInFirstDiagonal(),
        DefensiveProgressInSecondDiagonal()
    ]
)
```

Takový hráč se bude snažit hrát racionálně a *"myslet"* až do hloubky pěti
tahů dopředu (nikoliv však až na konec celého stromu), přičemž bude významně 
větší důraz dávat na ofensivu než primárně na snahu bránit svému oponentovi v 
jeho snažení.




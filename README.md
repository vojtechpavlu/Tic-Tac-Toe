# Piškvorky

Projekt pro demonstraci principů symbolických metod pro řešení 
problémů ve stavovém prostoru. Tento projekt byl vyvinut jako studijní
pomůcka pro výuku umělé inteligence při [Smíchovské střední průmyslové škole
a gymnáziu](https://www.ssps.cz/).

---

Projekt plní několik základních rolí. V první řadě stanovuje základní 
jednoduchý framework pro jednoduchou hru piškvorky, obsahuje základní definici
obecného hráče a definuje způsob interakce mezi hráčem a hrou tak, aby bylo
zajištěno, že takový hráč nemůže podvádět.


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
- ***TODO***

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


### TODO
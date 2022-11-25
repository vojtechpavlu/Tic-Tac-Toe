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

Každé políčko je v rámci implementace chápáno jako jakási přepravka obsahující
souřadnice políčka (v osách `x` a `y`) a případné označení jednoho z hráčů.
Konkrétní implementaci lze nalézt ve třídě `Field`.

Aby byla zajištěna bezpečnost a hráč neměl možnost jakkoliv podvádět, je mu
předán vždy jen obalený *proxy* objekt, který symbolizuje podstatné vlastnosti
příslušné instance. Takovými objekty jsou instance třídy `BoardSnapshot` a 
`FieldClosure`.


## Hráč

Nad rámec frameworku projekt dále definuje základní hráče (viz balíček 
`./src/players`):

- **Lidský hráč** (`HumanPlayer`), který umožňuje zkoušet hru člověkem
- **Náhodný hráč** (`RandomNPCPlayer`), který umožňuje hru jednoho hráče proti
neracionálnímu agentovi
- ***TODO***

Obecný protokol hráče je definován abstraktní třídou `Player` v balíčku 
`./src/game/`, jejíž instance jsou především nositeli jména hráče, znaku 
(pomocí kterého políčka svých tahů označují, typicky `X` nebo `O`) a metody, 
která hráčův tah umožňuje.

Díky této konstrukci je možné standardizovat hráče co do jeho vnějších projevů,
neboť se kromě bonity svých tahů chovají ve hře zcela identicky.

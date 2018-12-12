====================
Notes: Computability
====================
These are our notes for the second part of the course,
which dealt with basic computability.

It is in Danish, as the course was in Danish.


1. `Kombinatorik <#1-Kombinatorik>`__
	1.1 `Sumregel <#11-Sumregel>`__
	
	1.2 `Produktregel <#12-Produktregel>`__
	
	1.3 `Arrangementer <#13-Arrangementer>`__
	
	1.4 `Binomialkoefficienter <#14-Binomialkoefficienter>`__
	
	1.4.1 `Binomialsætningen (Sætning 18) <#Binomialsætningen-Sætning-18>`__
	
2. `Rekursive Definitioner <#2-Rekursive-Definitioner>`__
	2.1 `De Rekursive snakker hele tiden om sig selv <#21-De-Rekursive-snakker-hele-tiden-om-sig-selv>`__
		
		2.1.1 `Notation <#Notation>`__
		
		2.1.2 `Rekursion <#Rekursion>`__
		
	2.2 `Flere eksempler på rekursive definitioner <#22-Flere-eksempler-på-rekursive-definitioner>`__
	
		2.2.1 `Sum som rekursiv funktion (Definition 2.1) <#Sum-som-rekursiv-funktion-Definition-21>`__
	
	2.3 `Flere opgaver <#23-Flere-opgaver>`__
   
	2.4 `Ekstra: Rekursion og software <#24-Ekstra-Rekursion-og-software>`__
	
3. `Induktionsbeviser <#3-Induktionsbeviser>`__
	3.1 `Princippet om matematisk induktion <#31-Princippet-om-matematisk-induktion>`__
	
		3.1.1 `Matematisk induktion (svag form) <#Matematisk-induktion-svag-form>`__
		
	3.2 `Den stærke version af princippet om induktion <#32-Den-stærke-version-af-princippet-om-induktion>`__
	
		3.2.1 `Matematisk induktion (stærk form) <#Matematisk-induktion-stærk-form>`__
		
4. `Euklids Algoritme <#4-Euklids-Algoritme>`__
	4.1 `Algoritmen <#41-Algoritmen>`__
	
	4.2 `Sidenotes <#42-Sidenotes>`__
	
5. `Modulus <#5-Modulus>`__
	5.1 `Kongruens <#51-Kongruens>`__
	
	5.2 `Restklasse <#52-Restklasse>`__
	
	5.3 `Kongruensligninger <#53-Kongruensligninger>`__
	
		5.3.1 `Multiplikativ inverse <#531-Multiplikativ-inverse>`__
		
		5.3.2 `Generel kongruensligning <#532-Generel-kongruensligning>`__
		
		5.3.3 `Denkinesiske restklassesætning <#533-Den-kinesiske-restklassesætning>`__
		
		5.3.4 `System af kongruensligninger <#534-System-af-kongruensligninger>`__
		
6. `Polynomier <#6-Polynomier>`__		
	6.1 `Polynomiumsdivision (Sætning 6.1) <#Polynomiumsdivision-Sætning-61>`__
	
	6.2 `“Går op i” (Defintion 6.2) <#“Går-op-i”-Defintion-62>`__
	
	6.3 `Euklids udvidede algoritme for polynomier (Sætning 6.3) <#Euklids-udvidede-algoritme-for-polynomier-Sætning-63>`__
	
	6.3 `Fælles rod (Sætning 6.4) <#Fælles-rod-Sætning-64>`__

1. Kombinatorik
===============

1.1 Sumregel
------------

Såfremt :math:`A_1, A_2, \cdots. A_n` er parvist disjunkte mængder
gælder

.. math:: |A_1 \cup A_2 \cup \cdots \cup A_n | = \sum_{k = 1}^{n} |A_i|

Generelt for mængder :math:`A`, :math:`B` og :math:`C` gælder

.. math:: |A \cup B | = |A| + |B| - |A \cap B|

og

.. math:: |A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|

1.2 Produktregel
----------------

Hvis :math:`A` og :math:`B` er mængder er det karteiske produkt
defineret ved

.. math:: A \times B = \{(a, b) \mid a \in A \land b \in B  \}

For :math:`A_1, A_2, \cdots. A_n` er gælder

.. math::  |A_1 \times A_2 \times \cdots A_n| = \prod_{i = 1}^n |A_i| 

1.3 Arrangementer
-----------------

En opsummeering af måder :math:`k` elementer kan vælges ud af :math:`n`
elementer.

+-------------+--------------------------------------+----------------+
|             | Højst vælges en gang                 | Vælges flere   |
|             |                                      | gange          |
+=============+======================================+================+
| Rækkefølge  | :math:`P(n,k) = \frac{n!}{(n - k)!}` | :math:`n^k`    |
| vigtig      |                                      |                |
+-------------+--------------------------------------+----------------+
| Rækkefølge  | :math:`{n \choose k} = \frac{P(n,k)} | :math:`{{n+k-1 |
| ligegyldig  | {k!} = \frac{n!}{k!(n - k)!}`        | } \choose {n-1 |
|             |                                      | }}`            |
+-------------+--------------------------------------+----------------+

1.4 Binomialkoefficienter
-------------------------

At vælge k elementer ud fra en mængde med n elementer svarer til at
vælge hvilke :math:`{n \choose k}` elementer, der ikke skal med:

.. math::  {n \choose k} = {n \choose {n-k}} 

Derudover gælder

.. math::  {n \choose k} = { {n -1} \choose k } + { {n -1} \choose {k-1} } 

Binomialsætningen (Sætning 1.8)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For :math:`n \in \mathbb{N}` gælder

.. math::  (x + y)^n = \sum_{k=0}^{n} {n \choose k} \cdot x^k \cdot y^{n-k}

2. Rekursive Definitioner
=========================

2.1 De Rekursive snakker hele tiden om sig selv
-----------------------------------------------

Notation
~~~~~~~~

.. math::  f: \mathbb{N}\rightarrow \mathbb{Z} 

:math:`f(n)` er defineret ved de naturlige tal og funktionsværiden er et
helt tal.

Rekursion
~~~~~~~~~

Et veldefineret rekursivt udtryk indeholder basistilfælde uden
selvreference, og alle øvrige tilfælde skal entydigt kunne reduceres til
et basistilfælde.

2.2 Flere eksempler på rekursive definitioner
---------------------------------------------

Sum som rekursiv funktion (Definition 2.1)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hvis :math:`m, n\in\mathbb{Z}` og :math:`g(k)` er et udtryk så er

.. math::


   \sum_{k=m}^n g(k) = \left\{\begin{array}{ll} 0 & m>n \\ \sum_{k=m}^{n-1}g(k)+g(n) & m\leq n\end{array}\right.

2.3 Flere opgaver
-----------------

2.4 Ekstra: Rekursion og software
---------------------------------

3. Induktionsbeviser
====================

3.1 Princippet om matematisk induktion
--------------------------------------

Matematisk induktion (svag form)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lad :math:`P(n)` være et udsagn for :math:`n\in\mathbb{N}`. Hvis vi kan
vise

1. :math:`P(n_0)` er sand.
2. for alle :math:`n\in\mathbb{N}` med :math:`n\geq n_0` gælder
   :math:`P(n) \Rightarrow P(n+1)`,

så gælder :math:`P(n)` for alle naturlige tal :math:`n>n_0`.

3.2 Den stærke version af princippet om induktion
-------------------------------------------------

Matematisk induktion (stærk form)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lad :math:`P(n)` være et udsagn om de naturlige tal. Hvis der gælder

1. :math:`P(n_0)` for et :math:`n_0\in\mathbb{N}`, og
2. for alle :math:`n\geq n_0`

   .. math::


      (\forall k\in\left\{n_0,n_0+1,...,n\right\}P(k)) \Rightarrow P(n+1)

4. Euklids Algoritme
====================

4.1 Algoritmen
--------------

.. code:: python

   def ecgd(a, b):
       table = []
       table.append((0, a, 1, 0))
       table.append((1, b, 0, 1))
       
       k = 1
       while table[k][1]:
           k += 1
           k1, r1, s1, t1 = table[k-2]
           k2, r2, s2, t2 = table[k-1]
           r = r1 % r2
           s = s1 - s2 * (r1 // r2)
           t = t1 - t2 * (r1 // r2)
           table.append((k, r, s, t)) 

   return table

Denne version af euklids algoritme returnerer en tabel over en række
værdier for variablerne :math:`s`, :math:`t` og :math:`r`, sluttende når
:math:`r = 0`. Det gælder for en hver række i tabellen, at
:math:`a\cdot s+b\cdot t=r`. Tilsammen betyder dette at på den næst
sidste række er :math:`r = gcd(a,b)` og :math:`s` og :math:`t` er
koefficienterne for :math:`a` og :math:`b`, der skal til for at få
:math:`gcd(a,b)`

Da :math:`r = 0` på sidste række, kan de tilhørende værdier af :math:`s`
og :math:`t` lægges til andre værdier for at få samme resultat. Hvis
:math:`n` er antallet af rækker i tabellen, gælder følgende
:raw-latex:`\begin{equation*}
    gcd(a, b) = r_{n-1} = (s_{n-1}+s_nk)a+(t_{n-1}+t_nk)b
\end{equation*}` Hvor :math:`k\in\mathbb{Z}` er en vilkårlig konstant.

4.2 Sidenotes
-------------

Det gælder for :math:`a, b \in \mathbb{N}` at

.. math::  a\mathbb{Z} + b\mathbb{Z} = \mbox{sfd}(a,b)\mathbb{Z} 

Derudover gælder for :math:`a, b \in\mathbb{N}` at

.. math::  a\mathbb{Z} \cap b\mathbb{Z} = m\mathbb{Z} 

hvor

.. math:: m = \mbox{mfm}(a,b) = \frac{a \cdot b}{\mbox{sfd}(a,b)}

5. Modulus
==========

5.1 Kongruens
-------------

.. math::  a \equiv b \pmod{n} \Leftrightarrow n \mid (a-b) 

5.2 Restklasse
--------------

For :math:`k \in \mathbb{N}` er tallene der er kongruente, dvs.
løsningsmængden til

.. math::  x \equiv k \pmod{n} 

kaldet restklassen og er betegnet med

.. math::  k + n\mathbb{Z}

5.3 Kongruensligninger
----------------------

5.3.1 Multiplikativ inverse
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For kongruensligninger af formen

.. math::  c \cdot a \equiv 1 \pmod{n} 

kaldes :math:`c` den multiplikative invers til :math:`a` mdoulus
:math:`n`.

Det fremgår af “Sætning 5.6”:

-  Denne kan bestemmes ved :math:`t` givet ved
   :math:`s \cdot n + t\cdot a = 1` af Euklids udvidet algoritme.

-  Der er ingen multiplikativ inverse når
   :math:`\mbox{sfd}(a, n) \neq 1`.

5.3.2 Generel kongruensligning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En generel kongurensligning er af formen,

.. math::  a\cdot x \equiv b \pmod{n}

Det fremgår af “Sætning 5.7”: - For :math:`d = \mbox{sfd}(a, n)` er der
ingen løsninger hvis :math:`d \nmid b`. - Hvsi :math:`d \mid b` er
ligningen ækvivalent med :math:`a' \cdot x \equiv b' \pmod{n'}` hvor
:math:`a' = \frac{a}{d}`, :math:`b' = \frac{b}{d}` og
:math:`c' = \frac{c}{d}`.

Det fremgår af “Sætning 5.8”: - Hvis der eksisterer en multiplikativ
invers, :math:`c` til :math:`a` modulus :math:`n` er kongruensligningen
er ækvivalent med :math:`x \equiv c \cdot b \pmod{n}`. - Den
fuldstændige løsningsmængde er givet ved
:math:`(c\cdot b) + n \mathbb{N}`.

5.3.3 Den kinesiske restklassesætning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For systemer af formen

.. math::

   \begin{cases}
       x \equiv b_1 \pmod{n_1} \\
       x \equiv b_2 \pmod{n_2}
   \end{cases} 

såfremt :math:`\mbox{sfd}(n_1, n_2) = 1` er systemet ækvivalent med

.. math::  x \equiv x_p \equiv u_1 n_1 b_2 + u_2 n_2 b_1 \pmod{n_1 \cdot n_2}

hvor :math:`u_1` og :math:`u_2` kan bestemmes Euklids udvidet algoritme
for :math:`n_1` og :math:`n_2` sådan at:

.. math:: u_1 n_1 + u_2 n_2 = 1

5.3.4 System af kongruensligninger
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ved systmer af kongruensligninger kan systemet reduceres ved brug af
“Sætning 5.8” til en form hvor den kinesiske restklassesætning kan
anvedes.

6. Polynomier
=============

.. _polynomier-1:

6.1 Polynomier
--------------

Polynomiumsdivision (Sætning 6.1)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lad :math:`n(x),m(x)` være to givne polynomier, hvor :math:`m(x)` ikke
er nulpolynomiet. Der findes to entydigt bestemte polynomier
:math:`q(x),r(x)` der opfylder

.. math::


   n(x) = q(x)m(x)+r(x),\text{ og }\deg(r(x))<\deg(m(x))

Polynomierne :math:`q(x)` og :math:`r(x)` kaldes henholdsvis kvotienten
og resten ved division af :math:`n(x)` med :math:`m(x)`.

“Går op i” (Defintion 6.2)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Vi siger at :math:`m(x)` er en divisor i :math:`n(x)` hvis der findes et
polynomium :math:`q(x)` så

.. math::


   n(x) = q(x)m(x)

Hvis :math:`m(x)` er en divisor i :math:`n(x)` siger vi også at
:math:`m(x)` går op i :math:`n(x)`.

Euklids udvidede algoritme for polynomier (Sætning 6.3)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Euklids udvidede algoritme standser i endeligt mange trin. Der gælder

.. math::


   r_k(x) = s_k(x)N(x)+t_k(x)M(x),\text{ for }k=0,1,...,n

og vi har

.. math::


   \operatorname{sfd}(N(x),M(x)) = r_{n-1}(x)

Fælles rod (Sætning 6.4)
~~~~~~~~~~~~~~~~~~~~~~~~

De to polynomier :math:`N(x)` og :math:`M(x)` har den fælles rod
:math:`x_0`, hvis og kun hvis :math:`\operatorname{sfd}(N(x),M(x))` har
roden :math:`x_0`.

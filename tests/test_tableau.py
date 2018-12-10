import pytest

from dtudiscrete.tableau import constant as constant
from dtudiscrete.tableau import negation as negation
from dtudiscrete.tableau import disjunction as disjunction
from dtudiscrete.tableau import conjunction as conjunction
from dtudiscrete.tableau import implication as implication
from dtudiscrete.tableau import biimplication as biimplication

# a crappy, super long manual test
def test():
    # True constant test
    a = constant('A')
    # To string
    assert str(a) == a.to_str() == 'A'
    # To string, don't show true or false
    assert a.to_str(False) == 'A'
    # To string, show true or false
    assert a.to_str(True) == 'A:T'
    b = a.decompose()
    # To string (after decompose)
    assert str(b[0][0]) == b[0][0].to_str() == 'A'
    # To string, don't show true or false (after decompose)
    assert b[0][0].to_str(False) == 'A'
    # To string, show true or false (after decompose)
    assert b[0][0].to_str(True) == 'A:T'
    
    
    # False constant test
    a = constant('A', False)
    # To string
    assert str(a) == a.to_str() in ('\u00AC(A)', '\u00ACA')
    # To string, don't show true or false
    assert a.to_str(False) in ('\u00AC(A)', '\u00ACA')
    # To string, show true or false
    assert a.to_str(True) == 'A:F'
    b = a.decompose()
    # To string (after decompose)
    assert str(b[0][0]) == b[0][0].to_str() in ('\u00AC(A)', '\u00ACA')
    # To string, don't show true or false (after decompose)
    assert b[0][0].to_str(False) in ('\u00AC(A)', '\u00ACA')
    # To string, show true or false (after decompose)
    assert b[0][0].to_str(True) == 'A:F'
    
    
    # True negation of constant test
    a = constant('A')
    b = negation(a)
    # To string
    assert str(b) == b.to_str() in ('\u00AC(A)', '\u00ACA')
    # To string, don't show true or false
    assert b.to_str(False) in ('\u00AC(A)', '\u00ACA')
    # To string, show true or false
    assert b.to_str(True) in ('\u00AC(A):T', '\u00ACA:T')
    c = b.decompose()
    # To string (after decompose)
    assert str(c[0][0]) == c[0][0].to_str() in('\u00AC(A)', '\u00ACA', '\u00AC A')
    # To string, don't show true or false (after decompose)
    assert c[0][0].to_str(False) in('\u00AC(A)', '\u00ACA', '\u00AC A')
    # To string, show true or false (after decompose)
    assert c[0][0].to_str(True) == 'A:F'
    
    
    # False negation of constant test
    a = constant('A')
    b = negation(a, False)
    # To string
    assert str(b) == b.to_str() == 'A'
    # To string, don't show true or false
    assert b.to_str(False) == 'A'
    # To string, show true or false
    assert b.to_str(True) in ('\u00AC(A):F', '\u00ACA:F')
    c = b.decompose()
    # To string (after decompose)
    assert str(c[0][0]) == c[0][0].to_str() == 'A'
    # To string, don't show true or false (after decompose)
    assert c[0][0].to_str(False) == 'A'
    # To string, show true or false (after decompose)
    assert c[0][0].to_str(True) == 'A:T'
    
    
    # True disjunction of constants test
    a = constant('A')
    b = constant('B')
    c = disjunction((a,b), True)
    # To string
    assert str(c) == c.to_str() in ('A\u2228B', '(A)\u2228(B)')
    # To string, don't show true or false
    assert c.to_str(False) in ('A\u2228B', '(A)\u2228(B)')
    # To string, show true or false
    assert c.to_str(True) in ('A\u2228B:T', '(A)\u2228(B):T')
    d = c.decompose()
    # To string (after decompose)
    assert str(d[0][0]) == d[0][0].to_str() == 'A'
    assert str(d[1][0]) == d[1][0].to_str() == 'B'
    # To string, don't show true or false (after decompose)
    assert d[0][0].to_str(False) == 'A'
    assert d[1][0].to_str(False) == 'B'
    # To string, show true or false (after decompose)
    assert d[0][0].to_str(True) == 'A:T'
    assert d[1][0].to_str(True) == 'B:T'
    
    
    # False disjunction of constants test
    a = constant('A')
    b = constant('B')
    c = disjunction((a,b), False)
    # To string
    assert str(c) == c.to_str() in ('\u00ACA\u2227\u00ACB', '\u00AC(A)\u2227\u00AC(B)')
    # To string, don't show true or false
    assert c.to_str(False) in ('\u00ACA\u2227\u00ACB', '\u00AC(A)\u2227\u00AC(B)')
    # To string, show true or false
    assert c.to_str(True) in ('A\u2228B:F', '(A)\u2228(B):F')
    d = c.decompose()
    # To string (after decompose)
    assert str(d[0][0]) == d[0][0].to_str() in ('\u00ACA', '\u00AC(A)')
    assert str(d[0][1]) == d[0][1].to_str() in ('\u00ACB', '\u00AC(B)')
    # To string, don't show true or false (after decompose)
    assert d[0][0].to_str(False) in ('\u00ACA', '\u00AC(A)')
    assert d[0][1].to_str(False) in ('\u00ACB', '\u00AC(B)')
    # To string, show true or false (after decompose)
    assert d[0][0].to_str(True) == 'A:F'
    assert d[0][1].to_str(True) == 'B:F'
    
    
    # True conjunction of constants test
    a = constant('A')
    b = constant('B')
    c = conjunction((a,b), True)
    # To string
    assert str(c) == c.to_str() in ('A\u2227B', '(A)\u2227(B)')
    # To string, don't show true or false
    assert c.to_str(False) in ('A\u2227B', '(A)\u2227(B)')
    # To string, show true or false
    assert c.to_str(True) in ('A\u2227B:T', '(A)\u2227(B):T')
    d = c.decompose()
    # To string (after decompose)
    assert str(d[0][0]) == d[0][0].to_str() in ('A', '(A)')
    assert str(d[0][1]) == d[0][1].to_str() in ('B', '(B)')
    # To string, don't show true or false (after decompose)
    assert d[0][0].to_str(False) in ('A', '(A)')
    assert d[0][1].to_str(False) in ('B', '(B)')
    # To string, show true or false (after decompose)
    assert d[0][0].to_str(True) == 'A:T'
    assert d[0][1].to_str(True) == 'B:T'
    
    
    # False conjunction of constants test
    a = constant('A')
    b = constant('B')
    c = conjunction((a,b), False)
    # To string
    assert str(c) == c.to_str() in ('\u00ACA\u2228\u00ACB', '\u00AC(A)\u2228\u00AC(B)')
    # To string, don't show true or false
    assert c.to_str(False) in ('\u00ACA\u2228\u00ACB', '\u00AC(A)\u2228\u00AC(B)')
    # To string, show true or false
    assert c.to_str(True) in ('A\u2227B:F', '(A)\u2227(B):F')
    d = c.decompose()
    # To string (after decompose)
    assert str(d[0][0]) == d[0][0].to_str() in ('\u00ACA', '\u00AC(A)')
    assert str(d[1][0]) == d[1][0].to_str() in ('\u00ACB', '\u00AC(B)')
    # To string, don't show true or false (after decompose)
    assert d[0][0].to_str(False) in ('\u00ACA', '\u00AC(A)')
    assert d[1][0].to_str(False) in ('\u00ACB', '\u00AC(B)')
    # To string, show true or false (after decompose)
    assert d[0][0].to_str(True) == 'A:F'
    assert d[1][0].to_str(True) == 'B:F'
    
    
    # True implication of constants test
    a = constant('A')
    b = constant('B')
    c = implication((a,b), True)
    # To string
    assert str(c) == c.to_str() in ('A\u2192B', '(A)\u2192(B)')
    # To string, don't show true or false
    assert c.to_str(False) in ('A\u2192B', '(A)\u2192(B)')
    # To string, show true or false
    assert c.to_str(True) in ('A\u2912B:T', '(A)\u2192(B):T')
    d = c.decompose()
    # To string (after decompose)
    assert str(d[0][0]) == d[0][0].to_str() in ('\u00ACA', '\u00AC(A)')
    assert str(d[1][0]) == d[1][0].to_str() == 'B'
    # To string, don't show true or false (after decompose)
    assert d[0][0].to_str(False) in ('\u00ACA', '\u00AC(A)')
    assert d[1][0].to_str(False) == 'B'
    # To string, show true or false (after decompose)
    assert d[0][0].to_str(True) == 'A:F'
    assert d[1][0].to_str(True) == 'B:T'
    
    
    # False implication of constants test
    a = constant('A')
    b = constant('B')
    c = implication((a,b), False)
    # To string
    assert str(c) == c.to_str() in ('\u00ACA\u2228(A\u2227B)', '\u00AC(A)\u2228((A)\u2227(B))')
    # To string, don't show true or false
    assert c.to_str(False) in ('\u00ACA\u2228(A\u2227B)', '\u00AC(A)\u2228((A)\u2227(B))')
    # To string, show true or false
    assert c.to_str(True) in ('A\u2192B:F', '(A)\u2192(B):F')
    d = c.decompose()
    # To string (after decompose)
    assert str(d[0][0]) == d[0][0].to_str() in ('A', '(A)')
    assert str(d[0][1]) == d[0][1].to_str() in ('\u00ACB', '\u00AC(B)')
    # To string, don't show true or false (after decompose)
    assert d[0][0].to_str(False) in ('A', '(A)')
    assert d[0][1].to_str(False) in ('\u00ACB', '\u00AC(B)')
    # To string, show true or false (after decompose)
    assert d[0][0].to_str(True) == 'A:T'
    assert d[0][1].to_str(True) == 'B:F'
    
    
    # True biimplication of constants test
    a = constant('A')
    b = constant('B')
    c = biimplication((a,b), True)
    # To string
    assert str(c) == c.to_str() in ('A\u2194B', '(A)\u2194(B)')
    # To string, don't show true or false
    assert c.to_str(False) in ('A\u2194B', '(A)\u2194(B)')
    # To string, show true or false
    assert c.to_str(True) in ('A\u2914B:T', '(A)\u2194(B):T')
    d = c.decompose()
    # To string (after decompose)
    assert str(d[0][0]) == d[0][0].to_str() == 'A'
    assert str(d[0][1]) == d[0][1].to_str() == 'B'
    assert str(d[1][0]) == d[1][0].to_str() in ('\u00ACA', '\u00AC(A)')
    assert str(d[1][1]) == d[1][1].to_str() in ('\u00ACB', '\u00AC(B)')
    # To string, don't show true or false (after decompose)
    assert d[0][0].to_str(False) == 'A'
    assert d[0][1].to_str(False) == 'B'
    assert d[1][0].to_str(False) in ('\u00ACA', '\u00AC(A)')
    assert d[1][1].to_str(False) in ('\u00ACB', '\u00AC(B)')
    # To string, show true or false (after decompose)
    assert d[0][0].to_str(True) == 'A:T'
    assert d[0][1].to_str(True) == 'B:T'
    assert d[1][0].to_str(True) == 'A:F'
    assert d[1][1].to_str(True) == 'B:F'
    
    
    # False biimplication of constants test
    a = constant('A')
    b = constant('B')
    c = biimplication((a,b), False)
    # To string
    assert str(c) == c.to_str() in ('\u00ACA\u2194B', '\u00AC(A)\u2194(B)')
    # To string, don't show true or false
    assert c.to_str(False) in ('\u00ACA\u2194B', '\u00AC(A)\u2194(B)')
    # To string, show true or false
    assert c.to_str(True) in ('A\u2914B:F', '(A)\u2194(B):F')
    d = c.decompose()
    # To string (after decompose)
    assert str(d[0][0]) == d[0][0].to_str() == 'A'
    assert str(d[0][1]) == d[0][1].to_str() in ('\u00ACB', '\u00AC(B)')
    assert str(d[1][0]) == d[1][0].to_str() in ('\u00ACA', '\u00AC(A)')
    assert str(d[1][1]) == d[1][1].to_str() == 'B'
    # To string, don't show true or false (after decompose)
    assert d[0][0].to_str(False) == 'A'
    assert d[0][1].to_str(False) in ('\u00ACB', '\u00AC(B)')
    assert d[1][0].to_str(False) in ('\u00ACA', '\u00AC(A)')
    assert d[1][1].to_str(False) == 'B'
    # To string, show true or false (after decompose)
    assert d[0][0].to_str(True) == 'A:T'
    assert d[0][1].to_str(True) == 'B:F'
    assert d[1][0].to_str(True) == 'A:F'
    assert d[1][1].to_str(True) == 'B:T'
    
    
    # examples/stuff for manual testing/verification
    
#    print({constant('A')})
#    print(tableau_state({constant('A')}))
#    print(tableau_state({constant('A', False)}))
#    print(tableau_state({negation(constant('A'))}))
#    print(tableau_state({negation(constant('A'), False)}))
#    print(tableau_state({negation(negation(constant('A')))}))
#    print(tableau_state({negation(negation(constant('A')), False)}))
#    print(tableau_state({negation(negation(constant('A')), False)}))
#    print(tableau_state({disjunction((constant('A'), constant('B')), True)}))
#    print(tableau_state({disjunction((constant('A'), constant('B')), False)}))
#    print(tableau_state({conjunction((constant('A'), constant('B')), True)}))
#    print(tableau_state({conjunction((constant('A'), constant('B')), False)}))
#    print(tableau_state({disjunction((constant('A'), negation(constant('B'))), False)}))
#    print(tableau_state({disjunction((negation(constant('A')), negation(constant('B'))), True)}))
#    print(tableau_state({conjunction((conjunction((constant('A'), negation(constant('B')))), constant('B')), True)}))
#    print(tableau_state({disjunction((negation(constant('A')), negation(constant('B'))), True)}))
#    print(tableau_state({implication((constant('A'), constant('B')), True)}))
#    print(tableau_state({implication((constant('A'), constant('B')), False)}))
#    print(tableau_state({implication((constant('A'), conjunction((conjunction((constant('B'), negation(constant('B')))), negation(constant('A'))))), True)}))
#    print(tableau_state({biimplication((constant('A'), constant('B')), True)}))
#    print(tableau_state({biimplication((constant('A'), constant('B')), False)}))
#    print(tableau_state({biimplication((constant('A'), conjunction((conjunction((constant('B'), negation(constant('B')))), negation(constant('A'))))), True)}))
#    print(disjunction((constant('A'), constant('B')), True).to_str(True))
#    print(disjunction((constant('A'), constant('B')), True))
#    print(disjunction((constant('A'), constant('B')), False).to_str(True))
#    print(disjunction((constant('A'), constant('B')), False))
#    print(conjunction((constant('A'), constant('B')), True).to_str(True))
#    print(conjunction((constant('A'), constant('B')), True))
#    print(conjunction((constant('A'), constant('B')), False).to_str(True))
#    print(conjunction((constant('A'), constant('B')), False))

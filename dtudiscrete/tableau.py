##################################################################
##funktion: streng til class converter
##funktion: class til streng converter 
##funktion: søg efter modsætninger i kendte variable
##
##class udtryk:
## - META: hvilket udtryk det er
## - sandt/falsk
## - variabel(-gruppe) 1
## - evt. variabel(-gruppe) 2
## - funktion: apply dekompositionsregel
##
##class tableau_state:
## - liste af udtryk (sig selv, typisk kun ét udtryk) tuple(udtryk, udtryk)
## - liste af variablers kendte værdier [tuple(variabel, værdi)]
## - liste af ukendte variable
## - liste af udgreninger og den brugte dekompositionsregel [[udgrening, dekompositionsregel]]
##################################################################

import itertools

class tableau_state(object):
    
    # all the magic happens automatically in this function
    def __init__(self, expressions: set):
        self.expressions = expressions # a set of expressions
        self.known_constants = self._find_known_constants() # a set of 'constant' objects
        self.variables = self._find_all_variables() # a set of variable names (strings)
        self.closed = self._test_if_closed_branch()
        self.saturated = self._test_if_saturated_branch()
        if not self.closed and not self.saturated:
            self.branched_states, self.rule_used = self._branch_off()
        else:
            self.branched_states = set() # no branches
            self.rule_used = None # no rule used
    
    def get(self, var_name):
        return getattr(self, var_name)
    
    def __str__(self):
        # create printing string
        s = 'Expressions:\n'
        for expression in self.get('expressions'):
            s += f'    {expression.to_str(True)}\n'
        
        if self.get('closed'):
            s += f'    \u00D7'
            
        elif self.get('saturated'):
            s += f'    \u25EF'
            
        elif self.get('branched_states') != set():
            # convert certain words to unicode symbols
            if self.rule_used[0] == 'negation':
                rule_used_print = '\u00AC'

            if self.rule_used[0] == 'disjunction':
                rule_used_print = '\u2228'

            if self.rule_used[0] == 'conjunction':
                rule_used_print = '\u2227'
            # TODO:\\ add other symbols for printing
            
            # continue printing string
            s += f"Branches using rule '{rule_used_print}:{'T' if self.rule_used[1] else 'F'}':\n"
            for branch in self.get('branched_states'):
                sb = str(branch)
                for line in sb.splitlines():
                    s += f'    {line}\n'
        
        return s
    
    def to_str(self):
        return str(self)
    
    def _find_known_constants(self):
        constants = set()
        for expression in self.get('expressions'):
            if expression.__class__.__name__ ==  'constant':
                constants.add(expression)
        return constants
    
    def _find_all_variables(self):
        variables = set()
        for expression in self.get('expressions'):
            variables.update(self._find_variables_recursively(expression))
        return variables
    
    def _find_variables_recursively(self, expression):
        variables = set()
        
        if expression.__class__.__name__ ==  'constant':
            variables.add(expression.get('variable'))
        elif expression.__class__.__name__ ==  'forall' or expression.__class__.__name__ ==  'foreach':
            #TODO:\\ add special case for forall and foreach
            raise AttributeError(f"No variable finding special case has been made for 'forall' and 'foreach' yet.")
        else:
            for branch in expression.decompose():
                for expr in branch:
                    variables.update(self._find_variables_recursively(expr))
        
        return variables
    
    def _test_if_closed_branch(self):
        # compare all known constants to search for contradictions
        
        def compare_for_contradiction(const1: constant, const2: constant):
            return const1.get('variable') == const2.get('variable') and const1.get('true_or_false') != const2.get('true_or_false')
        
        for a, b in itertools.combinations(self.get('known_constants'), 2):
            if compare_for_contradiction(a,b):
                return True
        
        return False
        
    def _test_if_saturated_branch(self):
        # test if the only expressions left are constants
        for expression in self.get('expressions'):
            if expression.__class__.__name__ != 'constant':
                return False
        #else
        
        # get all known constant names
        constants = self.get('known_constants')
        constants_set = set()
        for constant in constants:
            constants_set.add(constant.get('variable'))
        # get all variable names
        variables = self.get('variables')
        # see if we know all variables
        return constants_set == variables
        
    def _branch_off(self):
        # decompose whatever can be decomposed in the most simple way (= testing_order)
        expressions = self.get('expressions')
        testing_order = (('negation', True), ('negation', False), ('disjunction', False), ('conjunction', True), ('implication', False), ('disjunction', True), ('conjunction', False), ('implication', True), ('biimplication', True), ('biimplication', False), ('forall', False), ('foreach', True), ('forall', True), ('foreach', False))
        for test in testing_order:
            for expression in expressions:
                if expression.__class__.__name__ == test[0] and expression.get('true_or_false') == test[1]:
                    branches = set()
                    # get all expressions, minus the decomposed one
                    new_expressions = expressions.difference({expression})
                    for branch in expression.decompose():
                        branch_expressions = new_expressions.copy()
                        # add the decomposed expressions for the branch
                        for expr in branch:
                            branch_expressions.add(expr)
                        # add the new state to branched_states
                        branches.add(tableau_state(branch_expressions))
                    
                    return branches, test
        
        raise ValueError("If the _branch_off function is called there should ALWAYS be a possible branch - but none has been found")

class expression(object):
    
    def __init__(self, variable, true_or_false=True):
        # these are the only two variables an expression should have
        self.variable = variable # may be one expression or a list of multiple expressions
        self.true_or_false = true_or_false
        
    def get(self, var_name):
        return getattr(self, var_name)
    
    def decompose(self):
        # return a tuple of tuples. the outer tuple containing different branches, and the inner tuples containing the decomposed expressions for their branch
        raise AttributeError(f"No decomposition function has been created for class '{self.__class__.__name__}'")
    
    def __str__(self):
        return self.to_str()
    
    def to_str(self, show_true_or_false=False):
        raise AttributeError("No string generation function has been created for class '{self.__class__.__name__}'")
        
    def true_or_false_to_str(self):
        if self.get('true_or_false'):
            return 'T'
        else:
            return 'F'

class constant(expression):
    
    def __init__(self, name, true_or_false=True):
        super().__init__(name, true_or_false)
        
    def decompose(self):
        return ((self,),)
        
    def __str__(self):
        return self.to_str()
    
    def to_str(self, show_true_or_false=False):
        if show_true_or_false:
            return f"{str(self.get('variable'))}:{self.true_or_false_to_str()}"
        else:
            if self.get('true_or_false'):
                return str(self.get('variable'))
            else:
                return str(negation(constant(self.get('variable'))))

class negation(expression):
    
    def __init__(self, expr, true_or_false=True):
        super().__init__(expr, true_or_false)
        
    def decompose(self):
        # return the inside expression but with the opposite true_or_false value of the negation expression
        inside_class = self.get('variable').__class__
        inside_class_content = self.get('variable').get('variable')
        true_or_false = not(self.get('true_or_false'))
        return ((inside_class(inside_class_content, true_or_false),),)
    
    def __str__(self):
        return self.to_str()
    
    def to_str(self, show_true_or_false=False):
        if show_true_or_false:
            return f"\u00AC({str(self.get('variable'))}):{self.true_or_false_to_str()}"
        else:
            if self.get('true_or_false'):
                return f"\u00AC({str(self.get('variable'))})"
            else:
                return f"{str(self.get('variable'))}"

class disjunction(expression):
    
    # disjuction takes a tuple of 2 expressions as 'expr'. None of the other classes care about this BUT all classes that create a disjunction has to remember to give it two expressions in 'expr'.
    def __init__(self, expr, true_or_false=True):
        super().__init__(expr, true_or_false)
        
    def decompose(self):
        if self.get('true_or_false'):
            # return two branches of an expression (one of the variables of the disjunction) that is true
            inside_class0 = self.get('variable')[0].__class__
            inside_class_content0 = self.get('variable')[0].get('variable')
            inside_class1 = self.get('variable')[1].__class__
            inside_class_content1 = self.get('variable')[1].get('variable')
            true_or_false = True
            return ((inside_class0(inside_class_content0, true_or_false),),(inside_class1(inside_class_content1, true_or_false),))
        else:
            # return one branch of two expressions (the variables of the disjunction) that are false
            inside_class0 = self.get('variable')[0].__class__
            inside_class_content0 = self.get('variable')[0].get('variable')
            inside_class1 = self.get('variable')[1].__class__
            inside_class_content1 = self.get('variable')[1].get('variable')
            true_or_false = False
            return ((inside_class0(inside_class_content0, true_or_false),inside_class1(inside_class_content1, true_or_false)),)

    def to_str(self, show_true_or_false=False):
        if show_true_or_false:
            return f"({self.get('variable')[0].to_str()})\u2228({self.get('variable')[1].to_str()}):{self.true_or_false_to_str()}"
        else:
            if self.get('true_or_false'):
                return f"({self.get('variable')[0].to_str()})\u2228({self.get('variable')[1].to_str()})"
            else:
                return f"\u00AC({self.get('variable')[0].to_str()})\u2227\u00AC({self.get('variable')[1].to_str()})"

class conjunction(expression):
    
    # conjuction takes a tuple of 2 expressions as 'expr'. None of the other classes care about this BUT all classes that create a conjunction has to remember to give it two expressions in 'expr'.
    def __init__(self, expr, true_or_false=True):
        super().__init__(expr, true_or_false)
        
    def decompose(self):
        if self.get('true_or_false'):
            # return one branch of two expressions (the variables of the disjunction) that are true
            inside_class0 = self.get('variable')[0].__class__
            inside_class_content0 = self.get('variable')[0].get('variable')
            inside_class1 = self.get('variable')[1].__class__
            inside_class_content1 = self.get('variable')[1].get('variable')
            true_or_false = True
            return ((inside_class0(inside_class_content0, true_or_false),inside_class1(inside_class_content1, true_or_false)),)
        else:
            # return two branches of an expression (one of the variables of the disjunction) that is false
            inside_class0 = self.get('variable')[0].__class__
            inside_class_content0 = self.get('variable')[0].get('variable')
            inside_class1 = self.get('variable')[1].__class__
            inside_class_content1 = self.get('variable')[1].get('variable')
            true_or_false = False
            return ((inside_class0(inside_class_content0, true_or_false),),(inside_class1(inside_class_content1, true_or_false),))

    def to_str(self, show_true_or_false=False):
        if show_true_or_false:
            return f"{self.get('variable')[0].to_str()}\u2227{self.get('variable')[1].to_str()}:{self.true_or_false_to_str()}"
        else:
            if self.get('true_or_false'):
                return f"({self.get('variable')[0].to_str()})\u2227({self.get('variable')[1].to_str()})"
            else:
                return f"\u00AC({self.get('variable')[0].to_str()})\u2228\u00AC({self.get('variable')[1].to_str()})"

#class implication(expression):
#class biimplication(expression):
#class forall(expression):
#class foreach(expression):


import pytest

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
    assert str(c) == c.to_str() in ('\A\u2227B', '(A)\u2227(B)')
    # To string, don't show true or false
    assert c.to_str(False) in ('\A\u2227B', '(A)\u2227(B)')
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
#    print(disjunction((constant('A'), constant('B')), True).to_str(True))
#    print(disjunction((constant('A'), constant('B')), True))
#    print(disjunction((constant('A'), constant('B')), False).to_str(True))
#    print(disjunction((constant('A'), constant('B')), False))
#    print(conjunction((constant('A'), constant('B')), True).to_str(True))
#    print(conjunction((constant('A'), constant('B')), True))
#    print(conjunction((constant('A'), constant('B')), False).to_str(True))
#    print(conjunction((constant('A'), constant('B')), False))

test()


# KNOWN BUGS:
# - it doesn't test/care if you give true/false values to subexpressions (as you shouldn't), so it might act wierd if you do (but you really shouldn't)
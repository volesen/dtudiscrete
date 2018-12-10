##################################################################
##
## How to use:
## - create an expression by stacking the following expressions:
##
##   - constant(<name>, True/False)
##   - negation(expr, True/False)
##   - disjunction((expr1, expr2), True/False)
##   - conjunction((expr1, expr2), True/False)
##   - implication((expr1, expr2), True/False)
##   - biimplication((expr1, expr2), True/False)
##
## - stack a set of expressions inside a tableau_state
## - print the result
##
## Example:
##  - print(tableau_state({disjunction((negation(constant('A')), negation(constant('B'))), True)}))
##
## KNOWN BUGS:
## - it doesn't test/care if you give true/false values to subexpressions (as you shouldn't), so it might act wierd if you do (but you really shouldn't)
##
## TODO:\\
## - forall
## - foreach
## - easier input
## - prettier output
##
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
            switch_dir = {
                'negation': '\u00AC',
                'disjunction': '\u2228',
                'conjunction': '\u2227',
                'implication': '\u2192',
                'biimplication': '\u2194'
                }
            
            rule_used_print = switch_dir.get(self.get('rule_used')[0])
            
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
            return f"({self.get('variable')[0].to_str()})\u2227({self.get('variable')[1].to_str()}):{self.true_or_false_to_str()}"
        else:
            if self.get('true_or_false'):
                return f"({self.get('variable')[0].to_str()})\u2227({self.get('variable')[1].to_str()})"
            else:
                return f"\u00AC({self.get('variable')[0].to_str()})\u2228\u00AC({self.get('variable')[1].to_str()})"

class implication(expression):
    
    # implication takes a tuple of 2 expressions as 'expr'. None of the other classes care about this BUT all classes that create an implication has to remember to give it two expressions in 'expr'.
    def __init__(self, expr, true_or_false=True):
        super().__init__(expr, true_or_false)
        
    def decompose(self):
        if self.get('true_or_false'):
            # return two branches of an expression (one of the variables of the disjunction) where the first branch is where the left expression is false, and the second branch is where the right expression is true
            inside_class0 = self.get('variable')[0].__class__
            inside_class_content0 = self.get('variable')[0].get('variable')
            inside_class1 = self.get('variable')[1].__class__
            inside_class_content1 = self.get('variable')[1].get('variable')
            true_or_false = (False, True)
            return ((inside_class0(inside_class_content0, true_or_false[0]),),(inside_class1(inside_class_content1, true_or_false[1]),))
        else:
            # return one branch of two expressions (the variables of the implication). the left expression is true and the right expression is false
            inside_class0 = self.get('variable')[0].__class__
            inside_class_content0 = self.get('variable')[0].get('variable')
            inside_class1 = self.get('variable')[1].__class__
            inside_class_content1 = self.get('variable')[1].get('variable')
            true_or_false = (True, False)
            return ((inside_class0(inside_class_content0, true_or_false[0]),inside_class1(inside_class_content1, true_or_false[1])),)

    def to_str(self, show_true_or_false=False):
        if show_true_or_false:
            return f"({self.get('variable')[0].to_str()})\u2192({self.get('variable')[1].to_str()}):{self.true_or_false_to_str()}"
        else:
            if self.get('true_or_false'):
                return f"({self.get('variable')[0].to_str()})\u2192({self.get('variable')[1].to_str()})"
            else:
                return f"\u00AC({self.get('variable')[0].to_str()})\u2228(({self.get('variable')[0].to_str()})\u2227({self.get('variable')[1].to_str()}))"

class biimplication(expression):
    
    # biimplication takes a tuple of 2 expressions as 'expr'. None of the other classes care about this BUT all classes that create a biimplication has to remember to give it two expressions in 'expr'.
    def __init__(self, expr, true_or_false=True):
        super().__init__(expr, true_or_false)
        
    def decompose(self):
        if self.get('true_or_false'):
            # return two branches where the first branch is where both expressions are true, and the second branch is where both expressions are false
            inside_class0 = self.get('variable')[0].__class__
            inside_class_content0 = self.get('variable')[0].get('variable')
            inside_class1 = self.get('variable')[1].__class__
            inside_class_content1 = self.get('variable')[1].get('variable')
            true_or_false = (True, False)
            return ((inside_class0(inside_class_content0, true_or_false[0]),inside_class1(inside_class_content1, true_or_false[0])),(inside_class0(inside_class_content0, true_or_false[1]),inside_class1(inside_class_content1, true_or_false[1])))
        else:
            # return two branches where the first branch is where one expression is true and the other is false, and the second branch is where the true/false of the first branch has been swapped
            inside_class0 = self.get('variable')[0].__class__
            inside_class_content0 = self.get('variable')[0].get('variable')
            inside_class1 = self.get('variable')[1].__class__
            inside_class_content1 = self.get('variable')[1].get('variable')
            true_or_false = (True, False)
            return ((inside_class0(inside_class_content0, true_or_false[0]),inside_class1(inside_class_content1, true_or_false[1])),(inside_class0(inside_class_content0, true_or_false[1]),inside_class1(inside_class_content1, true_or_false[0])))

    def to_str(self, show_true_or_false=False):
        if show_true_or_false:
            return f"({self.get('variable')[0].to_str()})\u2194({self.get('variable')[1].to_str()}):{self.true_or_false_to_str()}"
        else:
            if self.get('true_or_false'):
                return f"({self.get('variable')[0].to_str()})\u2194({self.get('variable')[1].to_str()})"
            else:
                return f"\u00AC({self.get('variable')[0].to_str()})\u2194({self.get('variable')[1].to_str()})"
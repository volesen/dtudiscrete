"""

Functions relates to solving tableaus.

"""

##################################################################
##
## How to use:
## 1. create an expression as a string where
##  
##   - '!': negation
##   - 'v': disjunction
##   - '^': conjunction
##   - '->': implication
##   - '<->': biimplication
##   - ',': new expression
##
## 2. print the tableau.
##    - Example: print(create_tableau('((p -> r)v (q -> r))->((p v q)->r):F'))
##
##
## How to use (old):
## 1. create an expression by chaining the following expressions:
##
##   - constant(<name>, True/False)
##   - negation(expr, True/False)
##   - disjunction((expr1, expr2), True/False)
##   - conjunction((expr1, expr2), True/False)
##   - implication((expr1, expr2), True/False)
##   - biimplication((expr1, expr2), True/False)
##
## 2. stack a set of expressions inside a tableau_state
## 3. print the result
##
## Old example:
##  - print(tableau_state({disjunction((negation(constant('A')), negation(constant('B'))), True)}))
##
## KNOWN BUGS:
## - it doesn't test/care if you give true/false values to subexpressions (as you shouldn't), so it might act wierd if you do (but you really shouldn't)
##
## TODO:\\
## - forall
## - foreach
## - even prettier output
## - less parantheses in the output
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
    
#    def __str__(self):
#        # create printing string
#        s = 'Expressions:\n'
#        for expression in self.get('expressions'):
#            s += f'    {expression.to_str(True)}\n'
#        
#        if self.get('closed'):
#            s += f'    \u00D7'
#            
#        elif self.get('saturated'):
#            s += f'    \u25EF'
#            
#        elif self.get('branched_states') != set():
#            # convert certain words to unicode symbols
#            switch_dir = {
#                'negation': '\u00AC',
#                'disjunction': '\u2228',
#                'conjunction': '\u2227',
#                'implication': '\u2192',
#                'biimplication': '\u2194'
#                }
#            
#            rule_used_print = switch_dir.get(self.get('rule_used')[0])
#            
#            # continue printing string
#            s += f"Branches using rule '{rule_used_print}:{'T' if self.rule_used[1] else 'F'}':\n"
#            for branch in self.get('branched_states'):
#                sb = str(branch)
#                for line in sb.splitlines():
#                    s += f'    {line}\n'
#        
#        return s
    
    def __str__(self):
        # create printing string
        s = ''
        for expression in self.get('expressions'):
            s += f'{expression.to_str(True)}\n'
        
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
            s += f"    |\n"
            s += f"    |\n"
            s += f"   {rule_used_print}:{'T' if self.get('rule_used')[1] else 'F'} on {self.get('rule_used')[2]}\n"
            s += f"    |\n"
            s += f"    |\n"
            for i, branch in enumerate(self.get('branched_states')):
                sb = str(branch)
                s += f'    |___ {sb.splitlines()[0]}\n'
                for line in sb.splitlines()[1:]:
                    # cleanup some of the extra lines
                    if len(self.get('branched_states'))-1 > i:
                        s += f'    |    {line}\n'
                    else: # without the extra line
                        s += f'         {line}\n'
                if len(self.get('branched_states'))-1 > i:
                    s += '    |\n'
        
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
                    
                    return branches, (test[0], test[1], expression)
        
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


##########################################################################
##
## From here on the tableau solver is completed, so what follows is an easier input method
##
##########################################################################

import re

class string_to_expression(object):
    def __init__(self, string):
        self.string = string
        self.string = self._strip_parantheses(self.get('string'))
        self.true_or_false, self.string = self._find_true_or_false(self.get('string'))
        self.string = self._strip_parantheses(self.get('string'))
        self.main_connective = self._find_main_connective(self.get('string'))
        self.expression = self._to_expression(self.get('string'), self.get('main_connective'))
    
    def get(self, attr_name):
        return getattr(self, attr_name)
    
    def _strip_parantheses(self, string):
        # check if there is a paranthesis surrounding everything. if there is, remove it
        while(True):
            if string[0] == '(' and self._find_right_paired_paranthesis(string[1:]) == len(string)-2:
                string = string[1:-1]
            else:
                break
        
        return string

    def _find_true_or_false(self, string):
        # check if there is a true/false value attached
        if string[-2:] == ':T':
            true_or_false = True
            string = string[:-2]
        elif string[-2:] == ':F':
            true_or_false = False
            string = string[:-2]
        else: # assume true
            true_or_false = True
        return true_or_false, string
    
    def _find_main_connective(self, string):
        prioritation = [('\<\-\>', 'biimplication'), ('\-\>', 'implication'), ('\^', 'conjunction'), ('v', 'disjunction'), ('\!', 'negation')]
        main_connective = None
        for con in prioritation:
            biimplications = [(m.start(), m.end()) for m in re.finditer(con[0], string)]
            for bi in biimplications:
                sur_par = self._find_surrounding_paranteses(string, bi[0]+1)
                if sur_par == None:
                    main_connective = (con[1], bi)
                    return main_connective
        
        return ('constant', (0, len(string)))
    
    def _to_expression(self, string, main_connective):
        if main_connective[0] == 'constant':
            expression = constant(string, self.get('true_or_false'))
            return expression
        else:
            # get the expression(s) that are modified by the main connective
            before_string = string[0:main_connective[1][0]]
            after_string = string[main_connective[1][1]:]
            before_expression = after_expression = None # placeholder
            if before_string:
                before_expression = string_to_expression(before_string).get('expression')
            if after_string:
                after_expression = string_to_expression(after_string).get('expression')
            
            # create the main_connective expression
            if main_connective[0] == 'negation':
                if before_expression:
                    raise AttributeError("There shouldn't be anything before the negation, but there was. This seems to because of a bad input")
                expression = negation(after_expression, self.get('true_or_false'))
            
            elif main_connective[0] == 'disjunction':
                expression = disjunction((before_expression, after_expression), self.get('true_or_false'))
            
            elif main_connective[0] == 'conjunction':
                expression = conjunction((before_expression, after_expression), self.get('true_or_false'))
            
            elif main_connective[0] == 'implication':
                expression = implication((before_expression, after_expression), self.get('true_or_false'))
            
            elif main_connective[0] == 'biimplication':
                expression = biimplication((before_expression, after_expression), self.get('true_or_false'))
            
            else:
                raise ValueError('The main connective is unknown. How could that be? Constant is the default case for unknowns.')
            
            return expression
    
    def _find_surrounding_paranteses(self, string: str, index: int):
        # find an eventual unpaired start paranthesis (if '<-' is in a paranthesis)
        left_par_loc = self._find_left_paired_paranthesis(string[:index-1])
        # if an unpaired paranthesis has been found
        if not left_par_loc == None:
            right_par_loc = self._find_right_paired_paranthesis(string[index+1:])
            count = 0
            for i, char in enumerate(string[index+1:]):
                if char == '(':
                    count += 1
                elif char == ')':
                    count -= 1
                # if an unpaired paranthesis has been found
                if count < 0:
                    right_par_loc = index + (i + 1)
                    break
            return (left_par_loc, right_par_loc)
        else:
            # if there is no surrounding paranteses
            return None

    def _find_left_paired_paranthesis(self, string: str):
        left_par_loc = None
        count = 0
        for i, char in enumerate(string[::-1]):
            if char == ')':
                count += 1
            elif char == '(':
                count -= 1
            # if an unpaired paranthesis has been found
            if count < 0:
                left_par_loc = len(string) - (i + 1)
                break
        return left_par_loc

    def _find_right_paired_paranthesis(self, string: str):
        right_par_loc = None
        count = 0
        for i, char in enumerate(string):
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
            # if an unpaired paranthesis has been found
            if count < 0:
                right_par_loc = i
                break
        return right_par_loc

def create_tableau(string: str):
    """
        Generates a printable string with the tableau solution to a logic problem.
        
        The current input considers everything except parentheses and the following specific characters as variables.
        
        !: negation. Use: !a
        v: disjunction. Use: a v b
        ^: conjunction. Use: a ^ b
        ->: implication. Use: a -> b
        <->: biimplication. Use: a <-> b
        ,: new expression, for if the input is a set of expressions. Use: a <-> b , !a
        
        All unnecessary parentheses and all spaces are removed automatically, so feel free to insert them for readability.
        
        :param str string: The expression(s) that the tableau is going to solve.
        
        :return: The tableau as a formatted string, ready to print.
        
        :rtype: str
    """
    
    # '!': negation
    # 'v': disjunction
    # '^': conjunction
    # '->': implication
    # '<->': biimplication
    # ',': new expression

    # remove all whitespaces
    string = string.replace(' ', '')

    # find all ',' and split the expressions up
    expression_strings = set()
    commas = [m.start() for m in re.finditer(',', string)]
    oi = 0
    if commas:
        for i in commas:
            expression_strings.add(string[oi:i])
            oi = i+1
        expression_strings.add(string[oi:])
    else:
        expression_strings.add(string)
    
    # convert the strings to expressions
    expressions = set()
    
    for expression_string in expression_strings:
        expressions.add(string_to_expression(expression_string).get('expression'))
    
    # create the tableau of the expressions
    return tableau_state(expressions)

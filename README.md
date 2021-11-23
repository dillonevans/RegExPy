# RegExPy

 A regular expression evaluator written in Python as an exercise in learning the language
 as well as applying knowledge of theoretical computer science. The expression entered is 
 converted into a parse tree, and using Thompson's construction that parse tree is then converted to 
 an NFA. Finally, that NFA is converted to a DFA used for expression matching using subset construction.

 Regular Languages are closed under union, concatenation, and the kleene star. As a result, other operations are comprised
 of these closure properties. For instance,

 L(r+) = L(rr*) = L(r)L(r*) and L(r?) = L(ε | r) = L(ε) | L(r)

 'r*'   => Match a regular expression r zero or more times
 'r+    => Match a regular expression r one or more times
 'r?'   => Match a regular expression r one or more times
 'rs'   => Concatenate two regular expressions
 'r|s'  => Match a regular expression r or s
 '(rs)' => Group regular expression(s) together


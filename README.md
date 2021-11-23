# RegExPy

 A regular expression evaluator written in Python as an exercise in learning the language
 as well as applying knowledge of theoretical computer science. The expression entered is 
 converted into a parse tree, and using Thompson's construction that parse tree is then converted to 
 an NFA. Finally, that NFA is converted to a DFA used for expression matching using subset construction.

 Regular Languages are closed under union, concatenation, and the kleene star. As a result, other operations are comprised
 of these closure properties. For instance,

 L(R+) = L(RR*) = L(R)L(R*) and L(R?) = L(ε | R) = L(ε) | L(R)

 'R*'   => Match a regular expression r zero or more times\
 'R+    => Match a regular expression r one or more times\
 'R?'   => Match a regular expression r one or more times\
 'RS'   => Concatenate two regular expressions\
 'R|S'  => Match a regular expression r or s\
 '(RS)' => Group regular expression(s) together


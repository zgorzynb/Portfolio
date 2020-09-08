grammar PLwypisz;

prog: ( (stat|function)? NEWLINE )*
    ;

stat:   PRINT (value | ao)	#print
	| 'let' ID (value | ao)	#assign
	| ID (value | ao) #nextassign
	| ao #arithmeticexpression
	| READ ID #read
	| IF sign block ELSE block ENDIF #else_if
	| WHILE sign block ENDLOOP #loop
	| ID #call_function
	| 'struct' ID structblock 'endstruct' #struct
	| 'struct' ID ID #allocatestruct
	| ID '.' ID value #storestruct
	| 'global' ID value #assignglobalvalue
   ;

structblock: (structelem? NEWLINE)*
    ;

structelem: 'double' ID
    | 'int' ID
    ;

function: FUNCTION fparam fblock ENDFUNCTION
    ;

FUNCTION: 'function'
    ;

fparam: ID
    ;

fblock: ( stat? NEWLINE )*
    ;

ENDFUNCTION:	'endfunction'
    ;

PRINT:	'print' 
   ;

WHILE: 'while'
   ;

ENDLOOP: 'endloop'
    ;

block: (stat? NEWLINE)*
;

ao: value MINUS value
	| value POW value
	| value (MUL | DIV) value
	| value (ADD | MINUS) value
	;

value: ID
    |STRING
	|INT
	|DOUBLE
	|arr
	|arr_element
	|struct_elem
   ;

struct_elem: ID '.' ID
    ;

sign: value '==' value
    | value '>' value
    | value '<' value
	;

arr_element: ID value
    ;

READ: 'read'
    ;

IF: 'if'
    ;

ENDIF: 'endif'
    ;

ELSE: 'else'
	;

arr: '[' value (',' value)* ']'
	|'[' ']'
	;

STRING :  '"' ( ~('\\'|'"') )* '"'
    ;

ID:   ('a'..'z'|'A'..'Z')+
   ;

INT:   '0'..'9'+
    ;

DOUBLE: '0'..'9'+'.''0'..'9'+
    ;

NEWLINE: '\r'? '\n'
    ;

WS:   (' '|'\t')+ -> skip
    ;

MINUS : '-'
    ;

OPAR : '('
    ;

CPAR : ')'
    ;

POW : '^'
    ;

MUL : '*'
    ;

DIV : '/'
    ;

ADD : '+'
    ;

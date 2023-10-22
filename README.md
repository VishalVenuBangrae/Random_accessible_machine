# Random_accessible_machine

Random Access Machine (RAM) is a theoretical model of computing that consists of a very basic set of operations that operate on a set of "registers" to describe effective computability. In this assignment, we will implement a Python implementation of RAM. The RAM model consists of an indefinite number of registers, R1, R2, ..., each capable of storing a natural number. The instruction set consists of the following 7 instructions:
INC Ri, increment the contents of register Ri by 1.
DEC Ri, decrement the contents of register Ri by 1; keep Ri unchanged if Ri is 0.
CLR Ri, set the contents of register Ri to 0.
MOV Ri Rj, replace the contents of register Ri by the contents of Rj, leaving Rj the same.
JMP N, next instruction to execute is set to the one with label N.
Rj JMP N, if contents of Rj is 0 the next instruction to execute is set to the one with label N, otherwise the instruction that follows executes as usual.
CONTINUE, do nothing.
Any of the above instruction, when used in a RAM program, may be preceded by a label N:. A RAM program consists of two parts: the first part assigns values to registers and the second part is a finite sequence of instructions, usually ending with the CONTINUE instruction. The RAM program may contain comment lines that begin with a #.
It is possible to use a register (in the second part of the program) without assigning it a value in the first part of the program. Such registers should be assumed to have a value of 0.

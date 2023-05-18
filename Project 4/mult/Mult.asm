// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

@0  // Initialize R2 to 0
D=A
@R2
M=D

@R0 // Load the value in R0 into R3
D=M
@R3
M=D

(LOOP)
  @R2   // Add R3 to R2 (increment the product)
  D=M
  @R3
  M=D+M
  @R2
  M=D

  @R1   // Subtract 1 from R1 (decrement the second multiplier)
  M=M-1

  @R1   // Check if R1 is now 0
  D=M

  @CONT
  D; JEQ

  @R0   // Add R0 to R3 (increment the multiplier)
  D=M
  @R3
  D=D+M
  @R3
  M=D

  @LOOP
  0; JMP
  
(CONT)
@R3
D=M
@R2
M=D

  @END
  0;JMP

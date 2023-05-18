// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// POINTER.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, POINTER.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

@BLACK
M=-1    // Store the value representing "black" in the 'BLACK' variable
D=0     // Set D to 0

@BLACK_SCREEN
0;JMP   // Jump to the 'BLACK_SCREEN' subroutine

(LOOP)
@KBD
D=M     // Load the keyboard input value into D
@BLACK_SCREEN
D;JEQ   // If no key is pressed, jump to 'BLACK_SCREEN'
D=-1    // Set D to -1 (representing "black")

(BLACK_SCREEN)
@ARG
M=D     // Store the value in D into the 'ARG' memory location
@BLACK
D=D-M   // Calculate the difference between the value in D and 'BLACK' (0 or -1)
@LOOP
D;JEQ   // If the result is 0, jump to 'LOOP' (key is pressed), otherwise continue

@ARG
D=M     // Load the value from 'ARG' into D
@BLACK
M=D     // Store the value in D into 'BLACK' (0 or -1)

@SCREEN
D=A     // Set D to the address of the 'SCREEN' memory location
@8192
D=D+A   // Add 8192 to D (size of the screen)
@POINTER
M=D     // Store the resulting address in the 'POINTER' memory location

(SETLOOP)
@POINTER
D=M-1   // Decrement the value at 'POINTER' by 1 and store it in D
M=D     // Store the updated value back in 'POINTER'
@LOOP
D;JLT   // If the value is less than 0, jump to 'LOOP'

@BLACK
D=M     // Load the value from 'BLACK' into D
@POINTER
A=M     // Set A to the address stored in 'POINTER'
M=D     // Store the value from D into the memory location pointed by A
@SETLOOP
0;JMP   // Jump back to 'SETLOOP' to repeat the process

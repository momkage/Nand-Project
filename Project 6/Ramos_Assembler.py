#Alexis Ramos
#CS271
#Final Project: The Assembler

def assemble(asm_filename):
    """Main function to assemble a given .asm file into .hack format.

    Args:
        asm_filename (str): The path to the .asm file to be assembled.
    """
    # Initialize symbol table and output filename
    symbol_table = create_symbol_table(asm_filename)
    hack_filename = asm_filename.replace('.asm', '.hack')
    hack_file = open(hack_filename, 'w')
    parser = Parser()

    #Label table
    parser.load_file(asm_filename)
    rom_address = 0
    while parser.has_more_commands:
        parser.advance()
        if parser.command_type == 'L_COMMAND':
            symbol_table[parser.symbol] = create_address(rom_address)
        elif parser.command_type != 'L_COMMAND':
            rom_address += 1

    #Write .hack file
    parser.reset_file()
    ram_address = 16
    while parser.has_more_commands:
        parser.advance()
        if parser.command_type == 'A_COMMAND':
            instruction, ram_address = write_A(parser.symbol, symbol_table, ram_address)
        elif parser.command_type == 'C_COMMAND':
            instruction = write_C(parser.dest, parser.comp, parser.jump)
        else:
            continue
        hack_file.write(instruction + '\n')

    parser.close_asm()
    hack_file.close()

def create_symbol_table(asm_filename):
    """Creates an initial symbol table with predefined symbols.
    
    Args:
        asm_filename (str): The path to the .asm file. Currently unused.

    Returns:
        dict: A dictionary with predefined symbols and their corresponding binary addresses.
    """
    symbol_table = {
        'SP': '000000000000000',
        'LCL': '000000000000001',
        'ARG': '000000000000010',
        'THIS': '000000000000011',
        'THAT': '000000000000100',
        'R0': '000000000000000',
        'R1': '000000000000001',
        'R2': '000000000000010',
        'R3': '000000000000011',
        'R4': '000000000000100',
        'R5': '000000000000101',
        'R6': '000000000000110',
        'R7': '000000000000111',
        'R8': '000000000001000',
        'R9': '000000000001001',
        'R10': '000000000001010',
        'R11': '000000000001011',
        'R12': '000000000001100',
        'R13': '000000000001101',
        'R14': '000000000001110',
        'R15': '000000000001111',
        'SCREEN': '100000000000000',
        'KBD': '110000000000000',
    }
    return symbol_table

def create_address(symbol):
    """Creates a binary address from a given symbol.
    
    Args:
        symbol (str): The symbol to be translated to a binary address.

    Returns:
        str: The binary representation of the symbol.
    """
    address = '{0:b}'.format(int(symbol))
    base = (15 - len(address)) * '0'
    return base + address

def write_A(symbol, symbol_table, ram_address):
    """Translates an A-instruction from asm to hack format.

    Args:
        symbol (str): The symbol or address in the A-instruction.
        symbol_table (dict): The symbol table containing addresses for symbols.
        ram_address (int): The current RAM address for variable allocation.

    Returns:
        tuple: The translated instruction and the updated RAM address.
    """
    instruction = '0'
    if symbol.isdigit():
        instruction += create_address(symbol)
    else:
        if symbol not in symbol_table:
            symbol_table[symbol] = create_address(ram_address)
            ram_address += 1
        instruction += symbol_table[symbol]
    return instruction, ram_address


def write_C(dest, comp, jump):
    """Translates a C-instruction from asm to hack format.

    Args:
        dest (str): The destination of the C-instruction.
        comp (str): The computation of the C-instruction.
        jump (str): The jump condition of the C-instruction.

    Returns:
        str: The translated instruction.
    """
    instruction = '111'
    code = Code()
    instruction += code.comp(comp)
    instruction += code.dest(dest)
    instruction += code.jump(jump)
    return instruction

class Parser(object):
    """Class to parse .asm files."""
    def load_file(self, asm_filename):
        """
        Open the .asm file and initiate/reset the parser's internal states.
        Args:
            asm_filename (str): Path to the .asm file.
        """
        self.asm = open(asm_filename, 'r')
        self.reset_file()
        self.symbol = None
        self.dest = None
        self.comp = None
        self.jump = None
        self.command_type = None

    def reset_file(self):
        """
        Resets the read pointer to the beginning of the file and reads the first instruction.
        """
        self.asm.seek(0)
        line = self.asm.readline().strip()
        while self.is_not_instruction(line):
            line = self.asm.readline().strip()
        self.curr_instruction = line
        self.instruction_num = -1

    def close_asm(self):
        self.asm.close()

    def is_not_instruction(self, line):
        """
        Check if a line in the .asm file is not an instruction.
        Args:
            line (str): A line from the .asm file.
        Returns:
            bool: True if line is not an instruction, False otherwise.
        """
        return not line or line[:2] == '//'

    @property
    def has_more_commands(self):
        """
        Check if there are more instructions to parse.
        Returns:
            bool: True if there are more instructions, False otherwise.
        """
        return bool(self.curr_instruction)

    def get_next_instruction(self):
        """
        Reads the next line of the .asm file and sets it as the current instruction.
        """
        line = self.asm.readline().strip()
        line = line.split('//')[0]
        line = line.strip()
        self.curr_instruction = line

    def advance(self):
        """
        Processes the current instruction and moves to the next one.
        """
        ci = self.curr_instruction
        if ci[0] == '@':
            self.parse_A(ci)
            self.instruction_num += 1
        elif ci[0] == '(':
            self.parse_L(ci)
        else:
            self.parse_C(ci)
            self.instruction_num += 1
        self.get_next_instruction()

    def parse_A(self, instruction):
        """
        Parse an A-command instruction.
        Args:
            instruction (str): The instruction to parse.
        """
        self.symbol = instruction[1:]
        self.command_type = 'A_COMMAND'

    def parse_L(self, instruction):
        """
        Parse an L-command instruction.
        Args:
            instruction (str): The instruction to parse.
        """
        self.symbol = instruction[1:-1]
        self.command_type = 'L_COMMAND'

    def parse_C(self, instruction):
        """
        Parse a C-command instruction.
        Args:
            instruction (str): The instruction to parse.
        """
        self.dest, self.comp, self.jump = None, None, None
        parts = instruction.split(';')
        remainder = parts[0]
        if len(parts) == 2:
            self.jump = parts[1]
        parts = remainder.split('=')
        if len(parts) == 2:
            self.dest = parts[0]
            self.comp = parts[1]
        else:
            self.comp = parts[0]
        self.command_type = 'C_COMMAND'

class Code(object):
    """Class to translate asm codes to hack codes."""
    def dest(self, mnemonic):
        """
        Translates a dest mnemonic to its corresponding binary code.
        Args:
            mnemonic (str): The dest mnemonic.
        Returns:
            str: The binary code of the dest mnemonic.
        """
        bin = ['0', '0', '0']
        if mnemonic is None:
            return ''.join(bin)
        if 'A' in mnemonic:
            bin[0] = '1'
        if 'D' in mnemonic:
            bin[1] = '1'
        if 'M' in mnemonic:
            bin[2] = '1'
        return ''.join(bin)

    def comp(self, mnemonic):
        """
        Translates a comp mnemonic to its corresponding binary code.
        Args:
            mnemonic (str): The comp mnemonic.
        Returns:
            str: The binary code of the comp mnemonic.
        """
        comp_dict = {
              '0': '101010',
              '1': '111111',
             '-1': '111010',
              'D': '001100',
              'A': '110000',
             '!D': '001101',
             '!A': '110001',
             '-D': '001111',
             '-A': '110011',
            'D+1': '011111',
            'A+1': '110111',
            'D-1': '001110',
            'A-1': '110010',
            'D+A': '000010',
            'D-A': '010011',
            'A-D': '000111',
            'D&A': '000000',
            'D|A': '010101',
        }
        a_bit = '0'
        if 'M' in mnemonic:
            a_bit = '1'
            mnemonic = mnemonic.replace('M', 'A')
        c_bit = comp_dict.get(mnemonic, '000000')
        return a_bit + c_bit

    def jump(self, mnemonic):
        """
        Translates a jump mnemonic to its corresponding binary code.
        Args:
            mnemonic (str): The jump mnemonic.
        Returns:
            str: The binary code of the jump mnemonic.
        """
        jump_dict = {
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111',
        }
        return jump_dict.get(mnemonic, '000')

asm_filename=input("Enter file name")
assemble(asm_filename)



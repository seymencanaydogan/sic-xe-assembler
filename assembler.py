import os
import sys
from tkinter import Tk, Text, Label, Button, END, messagebox

#tkinter GUI ile görselleştirme yapacağım.
class Assembler:
    # init fonksiyonum
    def __init__(self) -> None:
        self.__opcode = {}
        self.instruction = []
        self.__opcode_list = []
        self.__directive_list = [
            'START',
            'END',
            'BYTE',
            'WORD',
            'RESW',
            'RESB',
            'BASE',
            'CSECT',
            'EXTDEF',
            'EXTREF',
            'USE',
            'ORG',
            'LTORG',
            'EQU',
        ]

        self.__extdef_table = {}
        self.__extref_table = {}
        self.__symbol_table = {}
        self.__modified_record = {}
        self.__literal_table = []
        self.__blocks = {}  # farklı bloklar için konum sayaçlarını saklayacağım.

        self.__init_opcode()
        self.__get_format_list()

    # opcode listesini alalım.
    def __get_format_list(self) -> None:
        self.__opcode_list = self.__opcode.keys()

    # anımsatıcıyı kontrol et.
    def __check_mnemonic(self, mneonic) -> bool:
        if mneonic[0] == '+':
            return mneonic[1:] in self.__opcode_list
        else:
            return mneonic in self.__opcode_list or mneonic in self.__directive_list

    # opcode listesini okuyalım. .exe dosyasında opcode.txt çağırılırken hata oluştuğu için resource_path fonksiyonu tanımlandı.
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    def __init_opcode(self) -> None:
        opcode_path = self.resource_path("opcode.txt")
        print(f"Opcode dosyasının yolu: {opcode_path}")
        if not os.path.exists(opcode_path):
            raise FileNotFoundError(f"{opcode_path} dosyası bulunamadı.")
        with open(opcode_path, mode="r") as f:
            for line in f.readlines():
                opcode_arr = list(filter(None, line.split(" ")))
                self.__opcode[opcode_arr[0]] = {
                    "format": opcode_arr[1].split('/'),
                    "code": int(opcode_arr[2].replace("\n", ""), base=16)
                }

    # kod listesi oluşturalım.
    def __gen_code_list(self, opcode, type, format, offset) -> list:
        # format 4
        if format & 1 == 1:
            return [
                self.__opcode[opcode]['code'] + type,
                format << 4 | ((offset & 0xf0000) >> 16),
                (offset & 0xff00) >> 8,
                offset & 0xff,
            ]
        # format 3
        else:
            return [
                self.__opcode[opcode]['code'] + type,
                format << 4 | ((offset & 0xf00) >> 8),
                offset & 0xff,
            ]

    # dosyayı oku
    def read_file(self, code_string: str) -> None:
        format1_list = ['FIX', 'FLOAT', 'HIO', 'NORM', 'SIO', 'TIO', 'CSECT', 'LTORG']
        format2_list = ['ADDR', 'COMPR', 'DIVR', 'MULR', 'RMO' 'SHIFTL', 'SHIFTR']
        lines = code_string.splitlines()
        for index, line in enumerate(lines):
            # satırı oku ve şu öğeleri kaldır: ',', '\t', '\n' ve split et (ayır)
            line = line.replace(",", " ").replace("\t", " ").replace("\n", "")
            instruction_arr = list(filter(None, line.split(" ")))

            # yorumu ve boş satırı filtrele
            if not len(instruction_arr) or instruction_arr[0] == '.':
                continue

            instruct_set = {}  # talimat formatını tanımla

            # EXTDEF süreci
            if 'EXTDEF' in instruction_arr:
                if instruction_arr.index('EXTDEF') != 0:
                    raise SyntaxError(f'line {index + 1}: "EXTDEF can not have symbol"')

                instruct_set = {
                    'mnemonic': instruction_arr[0],
                    'operand': instruction_arr[1:],
                }
            # EXTREF süreci
            elif 'EXTREF' in instruction_arr:
                if instruction_arr.index('EXTREF') != 0:
                    raise SyntaxError(f'line {index + 1}: "EXTREF can not have symbol"')

                instruct_set = {
                    'mnemonic': instruction_arr[0],
                    'operand': instruction_arr[1:],
                }
            # process length = 4
            elif len(instruction_arr) == 4:
                if self.__check_mnemonic(instruction_arr[1]):
                    instruct_set = {
                        'symbol': instruction_arr[0],
                        'mnemonic': instruction_arr[1],
                        'operand': instruction_arr[2:],
                    }
                else:
                    raise SyntaxError(f'line {index + 1}: nonexistent symbol')
            # process length = 3
            elif len(instruction_arr) == 3:
                for mnemonic in format2_list:
                    if mnemonic in instruction_arr:
                        if instruction_arr.index(mnemonic) == 0:
                            instruct_set = {
                                'mnemonic': instruction_arr[0],
                                'operand': instruction_arr[1:],
                            }
                            break
                        else:
                            raise SyntaxError(f'line {index + 1}: format error')
                # talimat ayarlandı ve devam ediyor.
                if len(instruct_set):
                    self.instruction.append(instruct_set)
                    continue

                # X var ise:
                if 'X' in instruction_arr:
                    if self.__check_mnemonic(instruction_arr[0]):
                        instruct_set = {
                            'mnemonic': instruction_arr[0],
                            'operand': instruction_arr[1:],
                        }

                if len(instruct_set):
                    self.instruction.append(instruct_set)
                    continue

                if self.__check_mnemonic(instruction_arr[1]):
                    instruct_set = {
                        'symbol': instruction_arr[0],
                        'mnemonic': instruction_arr[1],
                        'operand': instruction_arr[2],
                    }
                else:
                    raise SyntaxError(f'line {index + 1}: nonexistent symbol')
            # proces length = 2
            elif len(instruction_arr) == 2:
                for mnemonic in format1_list:
                    if mnemonic in instruction_arr:
                        if instruction_arr.index(mnemonic) == 1:
                            instruct_set = {
                                'symbol': instruction_arr[0],
                                'mnemonic': instruction_arr[1],
                            }
                            break
                        else:
                            raise SyntaxError(f'line {index + 1}: format error')
                # talimat ayarlandı ve devam ediyor.
                if len(instruct_set):
                    self.instruction.append(instruct_set)
                    continue

                if instruction_arr[0] == 'EQU':
                    raise SyntaxError(f'line {index + 1}: EQU must have symbol')
                elif self.__check_mnemonic(instruction_arr[0]):
                    instruct_set = {
                        'mnemonic': instruction_arr[0],
                        'operand': instruction_arr[1],
                    }
                else:
                    raise SyntaxError(f'line {index + 1}: nonexistent symbol')
            else:
                if self.__check_mnemonic(instruction_arr[0]):
                    instruct_set = {
                        'mnemonic': instruction_arr[0],
                    }
                else:
                    raise SyntaxError(f'line {index + 1}: nonexistent symbol')

            self.instruction.append(instruct_set)

    # pass1:
    def pass_one(self) -> None:
        cur_block = None  # geçerli program bloğunu kaydet
        cur_location = None  # hafıza konumunu kaydet
        cur_symbol_table = {}  # geçerli sembol tablosunu kaydet
        cur_extref_table = []  # mevcut extref tablosunu kaydet

        for index, instr in enumerate(self.instruction):
            # literal ekle
            if 'operand' in instr and instr['operand'][0] == '=':
                if instr['operand'] not in self.__literal_table:
                    self.__literal_table.append(instr['operand'])

            # direktif işlemleri
            if instr['mnemonic'] == 'START':
                cur_block = instr['symbol']  # mevcut program bloğunu güncelle
                cur_symbol_table.clear()  # mevcut sembol tablosu sıfırla
                cur_extref_table.clear()  # mevcut extref tablosu sıfırla
                self.__literal_table.clear()  # literal tablosunu sıfırla
                self.__extdef_table.clear()  # extdef tablosu sıfırla
                self.__extref_table.clear()  # extref tablosu sıfırla
                cur_location = 0  # relocation için program, 0'dan başla
                instr['location'] = cur_location
                self.__extdef_table[cur_block] = {}
            #ORG:
            elif instr['mnemonic'] == 'ORG':
                if instr['operand'].isdigit():
                    self.cur_location = int(instr['operand'])
                else:
                    # İşlenen bir etiket ise, konumunu sembol tablosundan al
                    self.cur_location = self.__symbol_table[self.cur_block][instr['operand']]
                instr['location'] = self.cur_location
            #USE:
            elif instr['mnemonic'] == 'USE':
                new_block = instr['operand']
                if new_block not in self.__blocks:
                    self.__blocks[new_block] = 0
                self.__symbol_table[self.cur_block] = self.__symbol_table.get(self.cur_block, {}).copy()
                self.__extref_table[self.cur_block] = self.__extref_table.get(self.cur_block, []).copy()
                self.cur_block = new_block
                self.cur_location = self.__blocks[self.cur_block]
                instr['location'] = self.cur_location
            # extdef sembolü ekle
            elif instr['mnemonic'] == 'EXTDEF':
                for ext_def in instr['operand']:
                    self.__extdef_table[cur_block][ext_def] = None
            # ekstrem sembolü ekle
            elif instr['mnemonic'] == 'EXTREF':
                cur_extref_table += instr['operand']
            # değişkenler
            elif instr['mnemonic'] == 'RESW':
                instr['location'] = cur_location
                cur_location += int(instr['operand']) * 3
            elif instr['mnemonic'] == 'RESB':
                instr['location'] = cur_location
                cur_location += int(instr['operand'])
            # literali temizle
            elif instr['mnemonic'] == 'LTORG' or instr['mnemonic'] == 'END':
                it = index  # sonraki gerçek konumu kaydedelim.
                for literal in self.__literal_table:
                    it += 1
                    cur_symbol_table[literal] = cur_location
                    # bir sonrakine yeni talimat ekleyelim.
                    self.instruction.insert(it, {
                        'symbol': '*',
                        'mnemonic': literal,
                        'location': cur_location
                    })
                    if literal[1] == 'C':
                        cur_location += len(list(literal[3:].split('\''))[0])
                    elif literal[1] == 'X':
                        cur_location += len(list(literal[3:].split('\''))[0]) // 2
                self.__literal_table.clear()
                # sembol tab'i güncelleyelim.
                if instr['mnemonic'] == 'END':
                    # !![not]: sıfırlamadan önce copy'i kullanacağız.
                    self.__symbol_table[cur_block] = cur_symbol_table.copy()
                    self.__extref_table[cur_block] = cur_extref_table.copy()
                    cur_symbol_table.clear()
                    cur_extref_table.clear()
                    self.__literal_table.clear()
            # hafıza konumunu tanımla
            elif instr['mnemonic'] == 'EQU':
                if instr['operand'] == '*':
                    instr['location'] = cur_location
            # sıfırla ve yeni bloğu kullan
            elif instr['mnemonic'] == 'CSECT':
                cur_location = 0
                instr['location'] = cur_location
                # !![not]: sıfırlamadan önce copy'i kullanacağız.
                self.__symbol_table[cur_block] = cur_symbol_table.copy()
                self.__extref_table[cur_block] = cur_extref_table.copy()
                cur_block = instr['symbol']
                self.__extdef_table[cur_block] = {}
                self.__extref_table[cur_block] = []
                cur_symbol_table.clear()
                cur_extref_table.clear()
            # sabit değişken
            elif instr['mnemonic'] == 'BYTE':
                instr['location'] = cur_location
                # bayt sayısı belirsiz, önce hesaplanmalıdır.
                if instr['operand'][0] == 'X':
                    cur_location += len(list(instr['operand'][2:].split('\''))[0]) // 2
                elif instr['operand'][0] == 'C':
                    cur_location += len(list(instr['operand'][2:].split('\''))[0])
            elif instr['mnemonic'] == 'WORD':
                # WORD uzunluğu 3'e eşit olmalıdır.
                instr['location'] = cur_location
                cur_location += 3
            # format 4
            elif instr['mnemonic'][0] == '+':
                instr['location'] = cur_location
                cur_location += 4
            else:
                # eklenen literal talimatları atla ve BASE
                if 'symbol' in instr and instr['symbol'] == '*' or instr['mnemonic'] == 'BASE':
                    pass
                else:
                    instr['location'] = cur_location
                    opcode = instr['mnemonic'][1:] if instr['mnemonic'][0] == '+' else instr['mnemonic']
                    format = self.__opcode[opcode]['format'][0]
                    # format 1
                    if format == '1':
                        cur_location += 1
                    # format 2
                    elif format == '2':
                        cur_location += 2
                    # format 3
                    else:
                        cur_location += 3

            # EQU'yu sembolle hesapla.
            if instr['mnemonic'] == 'EQU':
                # literali sembol tablosuna ekle.
                if instr['operand'] == '*':
                    cur_symbol_table[instr['symbol']] = instr['location']
                elif '-' in instr['operand']:
                    symbol_1, symbol_2 = instr['operand'].split('-')
                    cur_symbol_table[instr['symbol']] = \
                        cur_symbol_table[symbol_1] - \
                        cur_symbol_table[symbol_2]
                elif '+' in instr['operand']:
                    symbol_1, symbol_2 = instr['operand'].split('+')
                    cur_symbol_table[instr['symbol']] = \
                        cur_symbol_table[symbol_1] + \
                        cur_symbol_table[symbol_2]
            # diğer sembolleri sembol tablosuna ekle.
            elif 'symbol' in instr and instr['symbol'] != '*':
                cur_symbol_table[instr['symbol']] = instr['location']

            if 'symbol' in instr:
                if instr['symbol'] in self.__extdef_table[cur_block]:
                    self.__extdef_table[cur_block][instr['symbol']] = instr['location']

    # pass2:
    def pass_two(self) -> None:
        b_loc = None  # BASE register kaydet
        cur_block = None  # geçerli program bloğunu belirtin
        cur_modified_list = []  # geçerli program bloğu M kayıtlarını kaydet
        # bunlar pass1 geçişinde işlendi, atlayalım
        skip_instr = ['EXTDEF', 'EXTREF', 'RESW', 'RESB', 'LTORG', 'EQU', 'USE', 'ORG']
        for index, instr in enumerate(self.instruction):
            if instr['mnemonic'] in skip_instr:
                continue
            # program bloğunu güncelle
            elif instr['mnemonic'] == 'START':
                cur_block = instr['symbol']
                cur_modified_list = []
            elif instr['mnemonic'] == 'END':
                self.__modified_record[cur_block] = cur_modified_list.copy()
                cur_modified_list.clear()
            elif instr['mnemonic'] == 'CSECT':
                # program bloğunu M kayıtlarında guncelle
                self.__modified_record[cur_block] = cur_modified_list.copy()
                cur_modified_list.clear()
                cur_block = instr['symbol']
            # B register içeriğini güncelle
            elif instr['mnemonic'] == 'BASE':
                b_loc = self.__symbol_table[cur_block][instr['operand']]
            elif instr['mnemonic'] == 'USE':
                # USE direktifine göre mevcut bloğu ve konumu güncelleyelim.
                new_block = instr['operand']
                self.__symbol_table[cur_block] = self.__symbol_table.get(cur_block, {}).copy()
                self.__extref_table[cur_block] = self.__extref_table.get(cur_block, []).copy()
                cur_block = new_block
                self.cur_location = self.__blocks.get(cur_block, 0)

            elif instr['mnemonic'] == 'ORG':
                if instr['operand'].isdigit():
                    self.cur_location = int(instr['operand'])
                else:
                    self.cur_location = self.__symbol_table[cur_block][instr['operand']]
            # literal talimatı
            elif instr['mnemonic'][0] == '=':
                data = list(instr['mnemonic'][3:].split('\''))[0]
                if instr['mnemonic'][1] == 'C':
                    opcode = []
                    for c in data:
                        opcode.append(ord(c))
                    instr['opcode'] = opcode
                elif instr['mnemonic'][1] == 'X':
                    opcode = []
                    for i in range(0, len(data), 2):
                        opcode.append(int(data[i: i + 2], base=16))
                    instr['opcode'] = opcode
            elif instr['mnemonic'] == 'WORD':
                if '-' in instr['operand']:
                    symbol_1, symbol_2 = instr['operand'].split('-')
                    location_1 = self.__symbol_table[cur_block][symbol_1] \
                        if symbol_1 in self.__symbol_table[cur_block] else 0
                    if location_1 == 0:
                        cur_modified_list.append({
                            'location': instr['location'],
                            'byte': 6,
                            'offset': '+' + symbol_1,
                        })
                    location_2 = self.__symbol_table[cur_block][symbol_2] \
                        if symbol_2 in self.__symbol_table[cur_block] else 0
                    if location_2 == 0:
                        cur_modified_list.append({
                            'location': instr['location'],
                            'byte': 6,
                            'offset': '-' + symbol_2,
                        })
                    instr['opcode'] = [
                        ((location_1 - location_2) & (0xff << i)) >> i
                        for i in range(16, -1, -8)
                    ]
                elif '+' in instr['operand']:
                    symbol_1, symbol_2 = instr['operand'].split('+')
                    location_1 = self.__symbol_table[cur_block][symbol_1] \
                        if symbol_1 in self.__symbol_table[cur_block] else 0
                    if location_1 == 0:
                        cur_modified_list.append({
                            'location': instr['location'],
                            'byte': 6,
                            'offset': '+' + symbol_1,
                        })
                    location_2 = self.__symbol_table[cur_block][symbol_2] \
                        if symbol_2 in self.__symbol_table[cur_block] else 0
                    if location_2 == 0:
                        cur_modified_list.append({
                            'location': instr['location'],
                            'byte': 6,
                            'offset': '+' + symbol_2,
                        })
                    instr['opcode'] = [
                        ((location_1 + location_2) & (0xff << i)) >> i
                        for i in range(16, -1, -8)
                    ]
                else:
                    data = list(instr['operand'][2:].split('\''))[0]
                    if instr['mnemonic'][0] == 'C':
                        opcode = []
                        for c in data:
                            opcode.append(ord(c))
                        instr['opcode'] = opcode
                    elif instr['mnemonic'][0] == 'X':
                        opcode = []
                        for i in range(0, len(data), 2):
                            opcode.append(int(data[i: i + 2], base=16))
                        instr['opcode'] = opcode
            elif instr['mnemonic'] == 'BYTE':
                data = list(instr['operand'][2:].split('\''))[0]
                if instr['operand'][0] == 'C':
                    opcode = []
                    for c in data:
                        opcode.append(ord(c))
                    instr['opcode'] = opcode
                elif instr['operand'][0] == 'X':
                    opcode = []
                    for i in range(0, len(data), 2):
                        opcode.append(int(data[i: i + 2], base=16))
                    instr['opcode'] = opcode
            else:
                # registerlara karşılık gelen sayıyı kaydedelim.
                register_cord = {'A': 0, 'X': 1, 'L': 2, 'B': 3, 'S': 4, 'T': 5, 'F': 6, }
                # format 2
                format2_list = ['ADDR', 'CLEAR', 'COMPR', 'DIVR', 'MULR', 'RMO' 'SHIFTL', 'SHIFTR', 'SVC', 'TIXR']
                for mnemonic in format2_list:
                    if instr['mnemonic'] == mnemonic:
                        if len(instr['operand']) == 2:
                            instr['opcode'] = [
                                self.__opcode[mnemonic]['code'],
                                register_cord[instr['operand'][0]] << 4 | register_cord[instr['operand'][1]]
                            ]
                        elif len(instr['operand']) == 1:
                            instr['opcode'] = [
                                self.__opcode[mnemonic]['code'],
                                register_cord[instr['operand'][0]] << 4
                            ]
                if 'opcode' in instr:
                    continue
                elif instr['mnemonic'] == 'RSUB':
                    instr['opcode'] = self.__gen_code_list('RSUB', 3, 0, 0)
                else:
                    # immedit adresleme format (n: 0, i: 1)
                    if instr['operand'][0] == '#':
                        token = instr['operand'][1:]
                        # operand -> sembol ise
                        if token in self.__symbol_table[cur_block]:
                            symbol_loc = self.__symbol_table[cur_block][token]
                            offset = symbol_loc - instr['location'] - 3
                            # format 3 (PC)
                            if offset >= -2048 and offset <= 2047:
                                instr['opcode'] = self.__gen_code_list(instr['mnemonic'], 1, 2, offset)
                            else:
                                offset = symbol_loc - b_loc
                                # format 3 (B)
                                if offset >= 0 and offset <= 4095:
                                    instr['opcode'] = self.__gen_code_list(instr['mnemonic'], 1, 4, offset)
                                # format 4
                                else:
                                    instr['opcode'] = self.__gen_code_list(instr['mnemonic'][1:], 1, 1, symbol_loc)
                        # operand -> sayı ise
                        else:
                            # bu bellek değil, bu yüzden PC ve B'yi dikkate almayın
                            offset = int(token)
                            # format 4
                            if offset > 4095:
                                instr['opcode'] = self.__gen_code_list(instr['mnemonic'][1:], 1, 1, offset)
                            # format 3
                            else:
                                instr['opcode'] = self.__gen_code_list(instr['mnemonic'], 1, 0, offset)
                    # dolaylı adresleme format (n: 1, i: 0)
                    elif instr['operand'][0] == '@':
                        symbol = instr['operand'][1:]
                        symbol_loc = self.__symbol_table[cur_block][symbol] \
                            if symbol in self.__symbol_table[cur_block] else None
                        # sembol tanımlanmadıysa
                        if symbol_loc == None:
                            raise SyntaxError(f'line {index + 1}: symbol has not been defined')
                        else:
                            # offset hesapla
                            offset = symbol_loc - instr['location'] - 3
                            # format 3 (PC)
                            if offset >= -2048 and offset <= 2047:
                                instr['opcode'] = self.__gen_code_list(instr['mnemonic'], 2, 2, offset)
                            else:
                                offset = symbol_loc - b_loc
                                # format 3 (B)
                                if offset >= 0 and offset <= 4095:
                                    instr['opcode'] = self.__gen_code_list(instr['mnemonic'], 2, 4, offset)
                                # format 4
                                else:
                                    instr['opcode'] = self.__gen_code_list(instr['mnemonic'], 2, 1, symbol_loc)
                    # direk adresleme formatı (n: 1, i: 1)
                    else:
                        format_num = 0  # x, b, p, e
                        # x etiketi
                        if isinstance(instr['operand'], list) and 'X' in instr['operand']:
                            format_num |= 8
                        # format 4
                        if instr['mnemonic'][0] == '+':
                            format_num |= 1
                            symbol_loc = None
                            mnemonic = instr['mnemonic'][1:]
                            # ilk elemanı al
                            first_element = instr['operand'][0] if isinstance(instr['operand'], list) else instr[
                                'operand']
                            # sembol konumunu al
                            try:
                                symbol_loc = self.__symbol_table[cur_block][first_element]
                            except:
                                symbol_loc = None
                            # sembol tanımlanmamış (EXTREF)
                            if symbol_loc == None:
                                # EXTREF bellek referansı varsayılan olarak 0'dır.
                                instr['opcode'] = self.__gen_code_list(mnemonic, 3, format_num, 0)
                                cur_modified_list.append({
                                    'location': instr['location'] + 1,
                                    'byte': 5,
                                    'offset': '+' + first_element,
                                })
                            else:
                                instr['opcode'] = self.__gen_code_list(mnemonic, 3, format_num, symbol_loc)
                        else:
                            symbol_loc = None
                            # ilk elemanı al
                            first_element = instr['operand'][0] if isinstance(instr['operand'], list) else instr[
                                'operand']
                            # sembol konumunu al
                            try:
                                symbol_loc = self.__symbol_table[cur_block][first_element]
                            except:
                                symbol_loc = None
                            # sembol tanımlanmamış (EXTREF)
                            if symbol_loc == None:
                                # EXTREF bellek referansı varsayılan olarak 0'dır
                                instr['opcode'] = self.__gen_code_list(instr['mnemonic'], 3, format_num, 0)
                            else:
                                offset = symbol_loc - instr['location'] - 3
                                # format 3 (PC)
                                if offset >= -2048 and offset <= 2047:
                                    format_num |= 2
                                    instr['opcode'] = self.__gen_code_list(instr['mnemonic'], 3, format_num, offset)
                                # format 3 (B)
                                else:
                                    format_num |= 4
                                    offset = symbol_loc - b_loc
                                    instr['opcode'] = self.__gen_code_list(instr['mnemonic'], 3, format_num, offset)

    # dosyayı yazalım.
    def generate_output_string(self) -> str:
        # program bloğu uzunluğunu ve başlangıç konumunu kaydedin
        output = []
        cur_block = {}
        cur_opcode_list = []
        cur_position_list = []
        program_info = {}
        end_position = ()

        def gen_extref_str(ext_info: list) -> str:
            ext_str = 'R'
            for label in ext_info:
                ext_str += '{:<6s}'.format(label)
            return ext_str.strip()

        def gen_extdef_str(ext_info: dict) -> str:
            ext_str = 'D'
            for label, value in ext_info.items():
                ext_str += '{:<6s}{:06X}'.format(label, value)
            return ext_str.strip()

        def gen_modified_list(modified_info: list) -> list:
            modified_list = []
            for info in modified_info:
                modified_str = 'M{:06X}{:02X}{:<7s}'.format(
                    info['location'], info['byte'], info['offset'])
                modified_list.append(modified_str.strip())
            return modified_list

        def gen_block_info(symbol_info: dict) -> dict:
            block_info = {
                'name': symbol_info['symbol'],
                'length': 0,
                'start': instr['location'],
            }

            extdef_info = self.__extdef_table[symbol_info['symbol']]
            if extdef_info:
                block_info['extdef'] = gen_extdef_str(extdef_info)
            else:
                block_info['extdef'] = ''

            extref_info = self.__extref_table[symbol_info['symbol']]
            if extref_info:
                block_info['extref'] = gen_extref_str(extref_info)
            else:
                block_info['extref'] = ''

            modified_info = self.__modified_record[symbol_info['symbol']]
            if modified_info:
                block_info['modified'] = gen_modified_list(modified_info)
            else:
                block_info['modified'] = []

            return block_info

        for instr in self.instruction:
            if instr['mnemonic'] == 'START':
                cur_opcode_list.clear()
                cur_position_list.clear()
                cur_block = gen_block_info(instr)
            elif instr['mnemonic'] == 'CSECT':
                name = cur_block['name']
                del cur_block['name']
                program_info[name] = cur_block

                # bu blok işlem kodunu birleştirir.
                program_info[name]['opcode'] = {}
                for index, pos in enumerate(cur_position_list):
                    program_info[name]['opcode'][pos] = cur_opcode_list[index]

                # yeni blok bilgisini tanımla
                cur_opcode_list.clear()
                cur_position_list.clear()
                cur_block = gen_block_info(instr)
            elif instr['mnemonic'] == 'END':
                name = cur_block['name']
                del cur_block['name']
                program_info[name] = cur_block

                # bu blok işlem kodunu birleştirir.
                program_info[name]['opcode'] = {}
                for index, pos in enumerate(cur_position_list):
                    program_info[name]['opcode'][pos] = cur_opcode_list[index]

                # END başlangıç kodu konumunu kaydedecektir.
                for block in self.__symbol_table.keys():
                    if instr['operand'] in self.__symbol_table[block]:
                        end_position = (block, self.__symbol_table[block][instr['operand']])
            elif 'location' in instr:
                length = instr['location']
                if 'opcode' in instr:
                    length += len(instr['opcode'])
                cur_block['length'] = max(cur_block['length'], length)
            if 'opcode' in instr:
                opcode_str = ''
                for opc in instr['opcode']:
                    opcode_str += '{:02X}'.format(opc)
                instr['opcode'] = opcode_str

                if len(cur_opcode_list):
                    if len(cur_opcode_list[-1]) + len(opcode_str) // 2 > 60:
                        cur_position_list.append(instr['location'])
                        cur_opcode_list.append(opcode_str)
                    else:
                        cur_opcode_list[-1] += opcode_str
                else:
                    cur_position_list.append(instr['location'])
                    cur_opcode_list.append(opcode_str)

        for symbol, info in program_info.items():
            output.append('H{:<6s}{:06X}{:06X}\n'.format(symbol, info['start'], info['length']))

            if info['extdef']:
                output.append(info['extdef'] + '\n')

            if info['extref']:
                output.append(info['extref'] + '\n')

            for offset, content in info['opcode'].items():
                output.append('T{:06X}{:02X}{}\n'.format(offset, len(content) // 2, content))

            for modified in info['modified']:
                output.append(modified + '\n')

            if symbol == end_position[0]:
                output.append('E{:06X}\n'.format(end_position[1]))
            else:
                output.append('E\n')

            output.append('\n')

        return ''.join(output)

    def execute(self, code_string: str) -> str:
        self.read_file(code_string)
        self.pass_one()
        self.pass_two()
        return self.generate_output_string()
def run_assembler():
    code_string = input_text.get("1.0", END)
    asm = Assembler()
    try:
        output = asm.execute(code_string)
        output_text.delete("1.0", END)
        output_text.insert("1.0", output)
        messagebox.showinfo("Success", "Program başarıyla assembly edildi!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


app = Tk()
app.title("Assembler Uygulaması")

input_label = Label(app, text="Assembly edilecek programı yazınız:")
input_label.pack()

input_text = Text(app, height=15, width=80)
input_text.pack()

output_label = Label(app, text="Oluşturulan obje program:")
output_label.pack()

output_text = Text(app, height=15, width=80)
output_text.pack()

run_button = Button(app, text="Assembly Et", command=run_assembler)
run_button.pack()

app.mainloop()

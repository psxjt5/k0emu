import unittest
import sys
from k0emu.processor import Processor, Registers, RegisterPairs, Flags

class ProcessorTests(unittest.TestCase):

    # register banks

    def test_rb0_accesses_fef8_feff(self):
        proc = Processor()
        proc.write_rb(0)
        self.assertEqual(proc.read_rb(), 0)
        proc.memory[0xFEF8] = 0
        proc.write_gp_reg(0, 0xAA) # 0=X register
        self.assertEqual(proc.memory[0xFEF8], 0xAA)
        self.assertEqual(proc.read_gp_reg(0), 0xAA)
        proc.memory[0xFEFF] = 0
        proc.write_gp_reg(7, 0x55) # 7=H register
        self.assertEqual(proc.memory[0xFEFF], 0x55)
        self.assertEqual(proc.read_gp_reg(7), 0x55)

    def test_rb1_accesses_fef0_fef7(self):
        proc = Processor()
        proc.write_rb(1)
        self.assertEqual(proc.read_rb(), 1)
        proc.memory[0xFEF0] = 0
        proc.write_gp_reg(0, 0xAA) # 0=X register
        self.assertEqual(proc.memory[0xFEF0], 0xAA)
        self.assertEqual(proc.read_gp_reg(0), 0xAA)
        proc.memory[0xFEF7] = 0
        proc.write_gp_reg(7, 0x55) # 7=H register
        self.assertEqual(proc.memory[0xFEF7], 0x55)
        self.assertEqual(proc.read_gp_reg(7), 0x55)

    def test_rb2_accesses_fee8_feef(self):
        proc = Processor()
        proc.write_rb(2)
        self.assertEqual(proc.read_rb(), 2)
        proc.memory[0xFEE8] = 0
        proc.write_gp_reg(0, 0xAA) # 0=X register
        self.assertEqual(proc.memory[0xFEE8], 0xAA)
        self.assertEqual(proc.read_gp_reg(0), 0xAA)
        proc.memory[0xFEEF] = 0
        proc.write_gp_reg(7, 0x55) # 7=H register
        self.assertEqual(proc.memory[0xFEEF], 0x55)
        self.assertEqual(proc.read_gp_reg(7), 0x55)

    def test_rb3_accesses_fee0_fee7(self):
        proc = Processor()
        proc.write_rb(3)
        self.assertEqual(proc.read_rb(), 3)
        proc.memory[0xFEE0] = 0
        proc.write_gp_reg(0, 0xAA) # 0=X register
        self.assertEqual(proc.memory[0xFEE0], 0xAA)
        self.assertEqual(proc.read_gp_reg(0), 0xAA)
        proc.memory[0xFEE7] = 0
        proc.write_gp_reg(7, 0x55) # 7=H register
        self.assertEqual(proc.memory[0xFEE7], 0x55)
        self.assertEqual(proc.read_gp_reg(7), 0x55)

    def test_write_rb_preserves_other_psw_bits(self):
        proc = Processor()
        proc.write_psw(0b11111111)
        proc.write_rb(0)
        self.assertEqual(proc.read_psw(), 0b11010111)
        proc.write_psw(0b00000000)
        proc.write_rb(3)
        self.assertEqual(proc.read_psw(), 0b00101000)

    # instructions

    # nop
    def test_00_nop(self):
        proc = Processor()
        code = [0x00] # nop
        proc.write_memory(0x0000, code)
        proc.step()
        self.assertEqual(proc.pc, len(code))

    # not1 cy
    def test_01_not1_cy_0_to_1(self):
        proc = Processor()
        code = [0x01] # not1 cy
        proc.write_memory(0x0000, code)
        proc.write_psw(proc.read_psw() & ~Flags.CY)
        proc.step()
        self.assertEqual(proc.read_psw(), Flags.CY)
        self.assertEqual(proc.pc, len(code))

    # not1 cy
    def test_01_not1_cy_1_to_0(self):
        proc = Processor()
        code = [0x01] # not1 cy
        proc.write_memory(0x0000, code)
        proc.write_psw(proc.read_psw() | Flags.CY)
        proc.step()
        self.assertEqual(proc.read_psw() & Flags.CY, 0)
        self.assertEqual(proc.pc, len(code))

    # set1 cy
    def test_20_set1_cy(self):
        proc = Processor()
        code = [0x20] # set1 cy
        proc.write_memory(0x0000, code)
        proc.write_psw(proc.read_psw() & ~Flags.CY)
        proc.step()
        self.assertEqual(proc.read_psw() & Flags.CY, Flags.CY)
        self.assertEqual(proc.pc, len(code))

    # clr1 cy
    def test_21_clr1_cy(self):
        proc = Processor()
        code = [0x21] # clr1 cy
        proc.write_memory(0x0000, code)
        proc.write_psw(proc.read_psw() | Flags.CY)
        proc.step()
        self.assertEqual(proc.read_psw() & Flags.CY, 0)
        self.assertEqual(proc.pc, len(code))

    # xch a,x                     ;30
    def test_30_xch_a_x(self):
        proc = Processor()
        code = [0x30] # xch a,x
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.X, 0xAA)
        proc.step()
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_gp_reg(Registers.X), 0x55)
        self.assertEqual(proc.pc, len(code))

    # xch a,c                     ;32
    def test_32_xch_a_c(self):
        proc = Processor()
        code = [0x32] # xch a,c
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.C, 0xAA)
        proc.step()
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_gp_reg(Registers.C), 0x55)
        self.assertEqual(proc.pc, len(code))

    #   xch a,b                     ;33
    def test_32_xch_a_b(self):
        proc = Processor()
        code = [0x33] # xch a,c
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.B, 0xAA)
        proc.step()
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_gp_reg(Registers.B), 0x55)
        self.assertEqual(proc.pc, len(code))

    # xch a,e                     ;34
    def test_32_xch_a_e(self):
        proc = Processor()
        code = [0x34] # xch a,c
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.E, 0xAA)
        proc.step()
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_gp_reg(Registers.E), 0x55)
        self.assertEqual(proc.pc, len(code))

    # xch a,d                     ;35
    def test_35_xch_a_e(self):
        proc = Processor()
        code = [0x35] # xch a,c
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.D, 0xAA)
        proc.step()
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_gp_reg(Registers.D), 0x55)
        self.assertEqual(proc.pc, len(code))

    # xch a,l                     ;36
    def test_35_xch_a_l(self):
        proc = Processor()
        code = [0x36] # xch a,l
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.L, 0xAA)
        proc.step()
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_gp_reg(Registers.L), 0x55)
        self.assertEqual(proc.pc, len(code))

    # xch a,h                     ;37
    def test_37_xch_a_h(self):
        proc = Processor()
        code = [0x37] # xch a,h
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.H, 0xAA)
        proc.step()
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_gp_reg(Registers.H), 0x55)
        self.assertEqual(proc.pc, len(code))

    # xch a,!0abcdh               ;ce cd ab
    def test_ce_xch_a_abs(self):
        proc = Processor()
        code = [0xce, 0xcd, 0xab] # xch a,!0abcdh
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.memory[0xabcd] = 0xAA
        proc.step()
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.memory[0xabcd], 0x55)
        self.assertEqual(proc.pc, len(code))

    # xch a,0fe20h                ;83 20          saddr
    def test_83_xch_a_saddr(self):
        proc = Processor()
        code = [0x83, 0x20] # xch a,0fe20h
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.memory[0xfe20] = 0xAA
        proc.step()
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.memory[0xfe20], 0x55)
        self.assertEqual(proc.pc, len(code))

    # xch a,0fffeh                ;93 fe          sfr
    def test_93_xch_a_sfr(self):
        proc = Processor()
        code = [0x93, 0xfe] # xch a,0fffeh
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.memory[0xfffe] = 0xAA
        proc.step()
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.memory[0xfffe], 0x55)
        self.assertEqual(proc.pc, len(code))

    # mov r,#byte
    def test_a0_mov_x_imm_byte(self):
        proc = Processor()
        code = [0xA0, 0x42] # mov x, #42
        proc.write_memory(0x0000, code)
        proc.step()
        self.assertEqual(proc.read_gp_reg(Registers.X), 0x42)
        self.assertEqual(proc.pc, len(code))
        # TODO FLAGS

    # mov r,#byte
    def test_a7_mov_l_imm_byte(self):
        proc = Processor()
        code = [0xA7, 0x42] # mov h, #42
        proc.write_memory(0x0000, code)
        proc.step()
        self.assertEqual(proc.read_gp_reg(Registers.H), 0x42)
        self.assertEqual(proc.pc, len(code))
        # TODO FLAGS

    # br !0abcdh                  ;9b cd ab
    def test_9b_br_addr16(self):
        proc = Processor()
        code = [0x9B, 0xCD, 0xAB] # br !0abcdh
        proc.write_memory(0x0000, code)
        proc.step()
        self.assertEqual(proc.pc, 0xABCD)

    # sel rb0                     ;61 d0
    def test_61_d0_sel_rb0(self):
        proc = Processor()
        code = [0x61, 0xD0] # sel rb0
        proc.write_memory(0x0000, code)
        proc.write_rb(1)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_rb(), 0)

    # sel rb1                     ;61 d8
    def test_61_d8_sel_rb1(self):
        proc = Processor()
        code = [0x61, 0xD8] # sel rb1
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_rb(), 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_rb(), 1)

    # sel rb2                     ;61 f0
    def test_61_f0_sel_rb2(self):
        proc = Processor()
        code = [0x61, 0xF0] # sel rb2
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_rb(), 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_rb(), 2)

    # sel rb3                     ;61 f8
    def test_61_f8_sel_rb3(self):
        proc = Processor()
        code = [0x61, 0xF8] # sel rb3
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_rb(), 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_rb(), 3)

    # mov a,x                   ;60
    def test_60_mov_a_x(self):
        proc = Processor()
        code = [0x60] # mov a,x
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_gp_reg(Registers.A), 0)
        proc.write_gp_reg(Registers.X, 0x42)
        proc.step()
        self.assertEqual(proc.read_gp_reg(Registers.A), 0x42)

    # mov a,c                   ;62
    def test_62_mov_a_c(self):
        proc = Processor()
        code = [0x62] # mov a,c
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_gp_reg(Registers.A), 0)
        proc.write_gp_reg(Registers.C, 0x42)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0x42)

    # mov a,b                   ;63
    def test_62_mov_a_b(self):
        proc = Processor()
        code = [0x63] # mov a,b
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_gp_reg(Registers.A), 0)
        proc.write_gp_reg(Registers.B, 0x42)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0x42)

    # mov a,e                   ;64
    def test_62_mov_a_e(self):
        proc = Processor()
        code = [0x64] # mov a,e
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_gp_reg(Registers.A), 0)
        proc.write_gp_reg(Registers.E, 0x42)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0x42)

    # mov a,d                   ;65
    def test_65_mov_a_d(self):
        proc = Processor()
        code = [0x65] # mov a,d
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_gp_reg(Registers.A), 0)
        proc.write_gp_reg(Registers.D, 0x42)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0x42)

    # mov a,l                   ;66
    def test_66_mov_a_l(self):
        proc = Processor()
        code = [0x66] # mov a,l
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_gp_reg(Registers.A), 0)
        proc.write_gp_reg(Registers.L, 0x42)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0x42)

    # mov a,h                   ;67
    def test_67_mov_a_h(self):
        proc = Processor()
        code = [0x67] # mov a,h
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_gp_reg(Registers.A), 0)
        proc.write_gp_reg(Registers.H, 0x42)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0x42)

    # mov x,a                   ;70
    def test_70_mov_x_a(self):
        proc = Processor()
        code = [0x70] # mov a,x
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_gp_reg(Registers.X), 0)
        proc.write_gp_reg(Registers.A, 0x42)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.X), 0x42)

    # mov c,a                   ;72
    def test_72_mov_a_c(self):
        proc = Processor()
        code = [0x72] # mov c,a
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_gp_reg(Registers.C), 0)
        proc.write_gp_reg(Registers.A, 0x42)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.C), 0x42)

    # mov b,a                   ;73
    def test_73_mov_b_a(self):
        proc = Processor()
        code = [0x73] # mov b,a
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_gp_reg(Registers.B), 0)
        proc.write_gp_reg(Registers.A, 0x42)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.B), 0x42)

    # mov e,a                   ;74
    def test_74_mov_e_a(self):
        proc = Processor()
        code = [0x74] # mov e,a
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_gp_reg(Registers.E), 0)
        proc.write_gp_reg(Registers.A, 0x42)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.E), 0x42)

    # mov d,a                   ;75
    def test_75_mov_d_a(self):
        proc = Processor()
        code = [0x75] # mov d,a
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_gp_reg(Registers.D), 0)
        proc.write_gp_reg(Registers.A, 0x42)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.D), 0x42)

    # mov l,a                   ;76
    def test_76_mov_l_a(self):
        proc = Processor()
        code = [0x76] # mov l,a
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_gp_reg(Registers.L), 0)
        proc.write_gp_reg(Registers.A, 0x42)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.L), 0x42)

    # mov h,a                   ;77
    def test_67_mov_a_l(self):
        proc = Processor()
        code = [0x77] # mov h,a
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.read_gp_reg(Registers.H), 0)
        proc.write_gp_reg(Registers.A, 0x42)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.H), 0x42)

    # mov a,!0abcdh               ;8e cd ab
    def test_8e_mov_a_addr16(self):
        proc = Processor()
        code = [0x8e, 0xcd, 0xab]
        proc.write_memory(0x0000, code)
        proc.memory[0xabcd] = 0x42
        self.assertEqual(proc.read_gp_reg(Registers.A), 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0x42)

    # mov !addr16,a               ;9e cd ab
    def test_9e_mov_addr16_a(self):
        proc = Processor()
        code = [0x9e, 0xcd, 0xab]
        proc.write_memory(0x0000, code)
        self.assertEqual(proc.memory[0xabcd], 0)
        proc.write_gp_reg(Registers.A, 0x42)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0x42)

    # mov a,0fe20h                ;F0 20          saddr
    def test_f0_mov_a_saddr(self):
        proc = Processor()
        code = [0xf0, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0x42
        self.assertEqual(proc.read_gp_reg(Registers.A), 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0x42)

    # mov a,psw                   ;f0 1e
    def test_f0_mov_a_psw(self):
        proc = Processor()
        code = [0xf0, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0x42)
        self.assertEqual(proc.read_gp_reg(Registers.A), 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0x42)

    # mov 0fe20h,a                ;f2 20          saddr
    def test_f2_mov_saddr_a(self):
        proc = Processor()
        code = [0xf2, 0x20]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x42)
        self.assertEqual(proc.memory[0xfe20], 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0x42)

    # mov psw,a                   ;f2 1e
    def test_f2_mov_psw_a(self):
        proc = Processor()
        code = [0xf2, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x42)
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0x42)

    # mov a,0fffeh                ;f4 fe          sfr
    def test_f4_mov_a_sfr(self):
        proc = Processor()
        code = [0xf4, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0x42
        self.assertEqual(proc.read_gp_reg(Registers.A), 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0x42)

    # mov 0fffeh,a                ;f6 fe          sfr
    def test_f6_mov_sfr_a(self):
        proc = Processor()
        code = [0xf6, 0xfe]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x42)
        self.assertEqual(proc.memory[0xfffe], 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0x42)

    # mov 0fe20h,#0abh            ;11 20 ab       saddr
    def test_11_mov_saddr_imm(self):
        proc = Processor()
        code = [0x11, 0x20, 0xab]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0xab)

    # mov psw,#0abh               ;11 1e ab
    def test_11_mov_psw_imm(self):
        proc = Processor()
        code = [0x11, 0x1e, 0x42]
        proc.write_memory(0x0000, code)
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0x42)

    # mov 0fffeh, #0abh           ;13 fe ab       sfr
    def test_13_mov_sfr_imm(self):
        proc = Processor()
        code = [0x13, 0xfe, 0xab]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0xab)

    # or a,#0aah                  ;6d aa
    def test_6d_or_a_imm_result_nonzero(self):
        proc = Processor()
        code = [0x6d, 0xaa]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or a,#000h                  ;6d 00
    def test_6d_or_a_imm_result_zero(self):
        proc = Processor()
        code = [0x6d, 0x00]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0)
        proc.write_psw(proc.read_psw() & ~Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0)
        self.assertEqual(proc.read_psw() & Flags.Z, Flags.Z)

    # or a,0fe20h                 ;6e 20          saddr
    def test_6e_or_a_saddr(self):
        proc = Processor()
        code = [0x6e, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0xAA
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or a,x                      ;61 68
    def test_61_68_or_a_x(self):
        proc = Processor()
        code = [0x61, 0x68]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xAA)
        proc.write_gp_reg(Registers.X, 0x55)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or a,c                      ;61 6a
    def test_61_6a_or_a_c(self):
        proc = Processor()
        code = [0x61, 0x6a]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xAA)
        proc.write_gp_reg(Registers.C, 0x55)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or a,b                      ;61 6b
    def test_61_6b_or_a_b(self):
        proc = Processor()
        code = [0x61, 0x6b]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xAA)
        proc.write_gp_reg(Registers.B, 0x55)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or a,e                      ;61 6c
    def test_61_6e_or_a_e(self):
        proc = Processor()
        code = [0x61, 0x6c]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xAA)
        proc.write_gp_reg(Registers.E, 0x55)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or a,d                      ;61 6d
    def test_61_6d_or_a_d(self):
        proc = Processor()
        code = [0x61, 0x6d]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xAA)
        proc.write_gp_reg(Registers.D, 0x55)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or a,l                      ;61 6e
    def test_61_6e_or_a_l(self):
        proc = Processor()
        code = [0x61, 0x6e]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xAA)
        proc.write_gp_reg(Registers.L, 0x55)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or a,h                      ;61 6f
    def test_61_6f_or_a_h(self):
        proc = Processor()
        code = [0x61, 0x6f]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xAA)
        proc.write_gp_reg(Registers.H, 0x55)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or x,a                      ;61 60
    def test_61_60_or_x_a(self):
        proc = Processor()
        code = [0x61, 0x60]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.X, 0x55)
        proc.write_gp_reg(Registers.A, 0xAA)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.X), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or a,a                      ;61 61
    def test_61_61_or_a_a(self):
        proc = Processor()
        code = [0x61, 0x61]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xff)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or c,a                      ;61 62
    def test_61_62_or_c_a(self):
        proc = Processor()
        code = [0x61, 0x62]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.C, 0x55)
        proc.write_gp_reg(Registers.A, 0xAA)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.C), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or b,a                      ;61 63
    def test_61_63_or_b_a(self):
        proc = Processor()
        code = [0x61, 0x63]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.B, 0x55)
        proc.write_gp_reg(Registers.A, 0xAA)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.B), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or d,a                      ;61 65
    def test_61_65_or_d_a(self):
        proc = Processor()
        code = [0x61, 0x65]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.D, 0x55)
        proc.write_gp_reg(Registers.A, 0xAA)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.D), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or l,a                      ;61 66
    def test_61_66_or_l_a(self):
        proc = Processor()
        code = [0x61, 0x66]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.L, 0x55)
        proc.write_gp_reg(Registers.A, 0xAA)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.L), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or h,a                      ;61 67
    def test_61_67_or_h_a(self):
        proc = Processor()
        code = [0x61, 0x67]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.H, 0x55)
        proc.write_gp_reg(Registers.A, 0xAA)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.H), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or 0fe20h,#0abh             ;e8 20 ab      saddr
    def test_e8_or_saddr_imm(self):
        proc = Processor()
        code = [0xe8, 0x20, 0x55]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0xAA
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # or a,!0abcdh                ;68 cd ab
    def test_68_or_a_addr16(self):
        proc = Processor()
        code = [0x68, 0xcd, 0xab]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.memory[0xabcd] = 0xAA
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xFF)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and a,#0abh                 ;5d ab
    def test_5d_and_a_imm_result_zero(self):
        proc = Processor()
        code = [0x5d, 0xff]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x00)
        proc.write_psw(proc.read_psw() & ~Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0)
        self.assertEqual(proc.read_psw() & Flags.Z, Flags.Z)

    # and a,#0abh                 ;5d ab
    def test_5d_and_a_imm_result_nonzero(self):
        proc = Processor()
        code = [0x5d, 0xff]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xf0)
        proc.write_psw(proc.read_psw() & ~Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and a,0fe20h                ;5e 20          saddr
    def test_5e_and_a_saddr(self):
        proc = Processor()
        code = [0x5e, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0xff
        proc.write_gp_reg(Registers.A, 0xf0)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and a,!0abcdh               ;58 cd ab
    def test_58_and_a_addr16(self):
        proc = Processor()
        code = [0x58, 0xcd, 0xab]
        proc.write_memory(0x0000, code)
        proc.memory[0xabcd] = 0xff
        proc.write_gp_reg(Registers.A, 0xf0)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and 0fe20h,#0abh            ;d8 20 ab       saddr
    def test_d8_and_saddr_imm(self):
        proc = Processor()
        code = [0xd8, 0x20, 0xf0]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0xff
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and a,x                     ;61 58
    def test_61_58_and_a_x(self):
        proc = Processor()
        code = [0x61, 0x58]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xff)
        proc.write_gp_reg(Registers.X, 0xf0)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and a,c                     ;61 5a
    def test_61_5a_and_a_c(self):
        proc = Processor()
        code = [0x61, 0x5a]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xff)
        proc.write_gp_reg(Registers.C, 0xf0)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and a,b                     ;61 5b
    def test_61_5b_and_a_b(self):
        proc = Processor()
        code = [0x61, 0x5b]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xff)
        proc.write_gp_reg(Registers.B, 0xf0)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and a,e                     ;61 5c
    def test_61_5c_and_a_e(self):
        proc = Processor()
        code = [0x61, 0x5c]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xff)
        proc.write_gp_reg(Registers.E, 0xf0)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and a,d                     ;61 5d
    def test_61_5d_and_a_d(self):
        proc = Processor()
        code = [0x61, 0x5d]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xff)
        proc.write_gp_reg(Registers.D, 0xf0)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and a,l                     ;61 5e
    def test_61_5e_and_a_l(self):
        proc = Processor()
        code = [0x61, 0x5e]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xff)
        proc.write_gp_reg(Registers.L, 0xf0)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and a,h                     ;61 5f
    def test_61_5f_and_a_h(self):
        proc = Processor()
        code = [0x61, 0x5f]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xff)
        proc.write_gp_reg(Registers.H, 0xf0)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and x,a                     ;61 50
    def test_61_50_and_x_a(self):
        proc = Processor()
        code = [0x61, 0x50]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.X, 0xff)
        proc.write_gp_reg(Registers.A, 0xf0)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.X), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and a,a                     ;61 51
    def test_61_51_and_a_a(self):
        proc = Processor()
        code = [0x61, 0x51]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xff)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xff)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and c,a                     ;61 52
    def test_61_52_and_c_a(self):
        proc = Processor()
        code = [0x61, 0x52]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.C, 0xff)
        proc.write_gp_reg(Registers.A, 0xf0)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.C), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and b,a                     ;61 53
    def test_61_53_and_b_a(self):
        proc = Processor()
        code = [0x61, 0x53]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.B, 0xff)
        proc.write_gp_reg(Registers.A, 0xf0)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.B), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and e,a                     ;61 54
    def test_61_54_and_e_a(self):
        proc = Processor()
        code = [0x61, 0x54]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.E, 0xff)
        proc.write_gp_reg(Registers.A, 0xf0)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.E), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and d,a                     ;61 55
    def test_61_55_and_e_a(self):
        proc = Processor()
        code = [0x61, 0x55]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.D, 0xff)
        proc.write_gp_reg(Registers.A, 0xf0)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.D), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and l,a                     ;61 56
    def test_61_56_and_e_a(self):
        proc = Processor()
        code = [0x61, 0x56]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.L, 0xff)
        proc.write_gp_reg(Registers.A, 0xf0)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.L), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # and h,a                     ;61 57
    def test_61_57_and_h_a(self):
        proc = Processor()
        code = [0x61, 0x57]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.H, 0xff)
        proc.write_gp_reg(Registers.A, 0xf0)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.H), 0xf0)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # call !0abcdh                ;9a cd ab
    def test_9a_call(self):
        proc = Processor()
        code = [0x9a, 0xcd, 0xab]
        proc.write_memory(0x0123, code)
        proc.pc = 0x0123
        return_address = proc.pc + len(code)
        proc.sp = 0xFE1F
        proc.step()
        self.assertEqual(proc.sp, 0xFE1d)
        self.assertEqual(proc.memory[0xFE1d], (return_address & 0xFF))
        self.assertEqual(proc.memory[0xFE1e], (return_address >> 8))
        self.assertEqual(proc.pc, 0xabcd)

    # ret                         ;af
    def test_af_ret(self):
        proc = Processor()
        code = [0xaf]
        proc.write_memory(0x0000, code)
        proc.sp = 0xfe1d
        proc.memory[0xfe1d] = 0xcd # stack: return address low
        proc.memory[0xfe1e] = 0xab # stack: return address high
        proc.step()
        self.assertEqual(proc.sp, 0xfe1f)
        self.assertEqual(proc.pc, 0xabcd)

    # push psw                    ;22
    def test_22_push_psw(self):
        proc = Processor()
        code = [0x22]
        proc.write_memory(0x0000, code)
        proc.sp = 0xFE1F
        proc.write_psw(0x42)
        proc.step()
        self.assertEqual(proc.sp, 0xfe1e)
        self.assertEqual(proc.memory[0xfe1e], 0x42)
        self.assertEqual(proc.pc, len(code))

    # pop psw                     ;23
    def test_23_pop_psw(self):
        proc = Processor()
        code = [0x23]
        proc.write_memory(0x0000, code)
        proc.sp = 0xFE1E
        proc.memory[0xFE1E] = 0x42 # stack: psw
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.sp, 0xfe1F)
        self.assertEqual(proc.read_psw(), 0x42)
        self.assertEqual(proc.pc, len(code))

    # xor a,x                     ;61 78
    def test_61_78_and_xor_a_x_result_nonzero(self):
        proc = Processor()
        code = [0x61, 0x78]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.X, 0xFF)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor a,x                     ;61 78
    def test_61_78_and_xor_a_x_result_zero(self):
        proc = Processor()
        code = [0x61, 0x78]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xFF)
        proc.write_gp_reg(Registers.X, 0xFF)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0)
        self.assertEqual(proc.read_psw() & Flags.Z, Flags.Z)

    # xor a,c                     ;61 7a
    def test_61_7a_and_xor_a_c(self):
        proc = Processor()
        code = [0x61, 0x7a]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.C, 0xFF)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor a,b                     ;61 7b
    def test_61_7b_and_xor_a_b(self):
        proc = Processor()
        code = [0x61, 0x7b]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.B, 0xFF)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor a,e                     ;61 7c
    def test_61_7c_and_xor_a_e(self):
        proc = Processor()
        code = [0x61, 0x7c]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.E, 0xFF)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor a,d                     ;61 7d
    def test_61_7d_and_xor_a_d(self):
        proc = Processor()
        code = [0x61, 0x7d]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.D, 0xFF)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor a,l                     ;61 7e
    def test_61_7e_and_xor_a_l(self):
        proc = Processor()
        code = [0x61, 0x7e]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.L, 0xFF)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor a,h                     ;61 7f
    def test_61_7f_and_xor_a_h(self):
        proc = Processor()
        code = [0x61, 0x7f]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.H, 0xFF)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor x,a                     ;61 70
    def test_61_70_and_xor_x_a(self):
        proc = Processor()
        code = [0x61, 0x70]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.X, 0xFF)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.X), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor a,a                     ;61 71
    def test_61_71_and_xor_a_a(self):
        proc = Processor()
        code = [0x61, 0x71]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0xFF)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0)
        self.assertEqual(proc.read_psw() & Flags.Z, Flags.Z)

    # xor c,a                     ;61 72
    def test_61_72_and_xor_c_a(self):
        proc = Processor()
        code = [0x61, 0x72]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.C, 0xFF)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.C), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor b,a                     ;61 73
    def test_61_73_and_xor_b_a(self):
        proc = Processor()
        code = [0x61, 0x73]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.B, 0xFF)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.B), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor e,a                     ;61 74
    def test_61_74_and_xor_e_a(self):
        proc = Processor()
        code = [0x61, 0x74]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.E, 0xFF)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.E), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor d,a                     ;61 75
    def test_61_75_and_xor_d_a(self):
        proc = Processor()
        code = [0x61, 0x75]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.D, 0xFF)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.D), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor l,a                     ;61 76
    def test_61_76_and_xor_l_a(self):
        proc = Processor()
        code = [0x61, 0x76]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.L, 0xFF)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.L), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor h,a                     ;61 77
    def test_61_77_and_xor_h_a(self):
        proc = Processor()
        code = [0x61, 0x77]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.write_gp_reg(Registers.H, 0xFF)
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.H), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor a,!0abcdh               ;78 cd ab
    def test_78_xor_a_addr16(self):
        proc = Processor()
        code = [0x78, 0xcd, 0xab]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.memory[0xabcd] = 0xFF
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor a,#0abh                 ;7d ab
    def test_7d_xor_a_imm(self):
        proc = Processor()
        code = [0x7d, 0xff]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.memory[0xabcd] = 0xFF
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor a,0fe20h                ;7e 20          saddr
    def test_7e_xor_a_saddr(self):
        proc = Processor()
        code = [0x7e, 0x20]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0x55)
        proc.memory[0xfe20] = 0xFF
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # xor 0fe20h,#0abh            ;f8 20 ab       saddr
    def test_f8_xor_saddr_imm(self):
        proc = Processor()
        code = [0xf8, 0x20, 0xff]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0x55
        proc.write_psw(proc.read_psw() | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0xAA)
        self.assertEqual(proc.read_psw() & Flags.Z, 0)

    # set1 0fe20h.0               ;0a 20          saddr
    def test_0a_set1_saddr_bit0(self):
        proc = Processor()
        code = [0x0a, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b11111110
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0xff)

    # set1 psw.0                  ;0a 1e
    def test_0a_set1_psw_bit0(self):
        proc = Processor()
        code = [0x0a, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111110)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0xff)

    # set1 0fe20h.1               ;1a 20          saddr
    def test_1a_set1_saddr_bit1(self):
        proc = Processor()
        code = [0x1a, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b11111101
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0xff)

    # set1 psw.1                  ;1a 1e
    def test_1a_set1_psw_bit1(self):
        proc = Processor()
        code = [0x1a, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111101)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0xff)

    # set1 0fe20h.2               ;2a 20          saddr
    def test_2a_set1_saddr_bit2(self):
        proc = Processor()
        code = [0x2a, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b11111011
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0xff)

    # set1 psw.2                  ;2a 1e
    def test_2a_set1_psw_bit2(self):
        proc = Processor()
        code = [0x2a, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111011)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0xff)

    # set1 0fe20h.3               ;3a 20          saddr
    def test_3a_set1_saddr_bit3(self):
        proc = Processor()
        code = [0x3a, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b11110111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0xff)

    # set1 psw.3                  ;3a 1e
    def test_3a_set1_psw_bit3(self):
        proc = Processor()
        code = [0x3a, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11110111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0xff)

    # set1 0fe20h.4               ;4a 20          saddr
    def test_4a_set1_saddr_bit4(self):
        proc = Processor()
        code = [0x4a, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b11101111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0xff)

    # set1 psw.4                  ;4a 1e
    def test_4a_set1_psw_bit4(self):
        proc = Processor()
        code = [0x4a, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11101111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0xff)

    # set1 0fe20h.5               ;5a 20          saddr
    def test_5a_set1_saddr_bit5(self):
        proc = Processor()
        code = [0x5a, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b11011111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0xff)

    # set1 psw.5                  ;5a 1e
    def test_5a_set1_psw_bit5(self):
        proc = Processor()
        code = [0x5a, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11011111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0xff)

    # set1 0fe20h.6               ;6a 20          saddr
    def test_6a_set1_saddr_bit6(self):
        proc = Processor()
        code = [0x6a, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b10111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0xff)

    # set1 psw.6                  ;6a 1e
    def test_6a_set1_psw_bit6(self):
        proc = Processor()
        code = [0x6a, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b10111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0xff)

    # set1 0fe20h.7               ;7a 20          saddr
    def test_7a_set1_saddr_bit7(self):
        proc = Processor()
        code = [0x7a, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b01111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0xff)

    # set1 psw.7                  ;7a 1e
    # ei                          ;7a 1e          alias for set1 psw.7
    def test_7a_set1_psw_bit7(self):
        proc = Processor()
        code = [0x7a, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b01111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0xff)

    # set1 a.0                    ;61 8a
    def test_61_8a_set1_a_bit0(self):
        proc = Processor()
        code = [0x61, 0x8a]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0b11111110)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xff)

    # set1 a.1                    ;61 9a
    def test_61_9a_set1_a_bit1(self):
        proc = Processor()
        code = [0x61, 0x9a]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0b11111101)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xff)

    # set1 a.2                    ;61 aa
    def test_61_aa_set1_a_bit2(self):
        proc = Processor()
        code = [0x61, 0xaa]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0b11111011)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xff)

    # set1 a.3                    ;61 ba
    def test_61_ba_set1_a_bit3(self):
        proc = Processor()
        code = [0x61, 0xba]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0b11110111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xff)

    # set1 a.4                    ;61 ca
    def test_61_ca_set1_a_bit4(self):
        proc = Processor()
        code = [0x61, 0xca]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0b11101111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xff)

    # set1 a.5                    ;61 da
    def test_61_da_set1_a_bit5(self):
        proc = Processor()
        code = [0x61, 0xda]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0b11011111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xff)

    # set1 a.6                    ;61 ea
    def test_61_ea_set1_a_bit6(self):
        proc = Processor()
        code = [0x61, 0xea]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0b10111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xff)

    # set1 a.7                    ;61 fa
    def test_61_fa_set1_a_bit7(self):
        proc = Processor()
        code = [0x61, 0xfa]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0b01111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xff)

    # set1 0fffeh.0               ;71 0a fe       sfr
    def test_71_0a_set1_sfr_bit0(self):
        proc = Processor()
        code = [0x71, 0x0a, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b11111110
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0xff)

    # set1 0fffeh.1               ;71 1a fe       sfr
    def test_71_1a_set1_sfr_bit1(self):
        proc = Processor()
        code = [0x71, 0x1a, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b11111101
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0xff)

    # set1 0fffeh.2               ;71 2a fe       sfr
    def test_71_2a_set1_sfr_bit2(self):
        proc = Processor()
        code = [0x71, 0x2a, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b11111011
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0xff)

    # set1 0fffeh.3               ;71 3a fe       sfr
    def test_71_3a_set1_sfr_bit3(self):
        proc = Processor()
        code = [0x71, 0x3a, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b11110111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0xff)

    # set1 0fffeh.4               ;71 4a fe       sfr
    def test_71_4a_set1_sfr_bit4(self):
        proc = Processor()
        code = [0x71, 0x4a, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b11101111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0xff)

    # set1 0fffeh.5               ;71 5a fe       sfr
    def test_71_5a_set1_sfr_bit5(self):
        proc = Processor()
        code = [0x71, 0x5a, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b11011111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0xff)

    # set1 0fffeh.6               ;71 6a fe       sfr
    def test_71_6a_set1_sfr_bit6(self):
        proc = Processor()
        code = [0x71, 0x6a, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b10111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0xff)

    # set1 0fffeh.7               ;71 7a fe       sfr
    def test_71_7a_set1_sfr_bit7(self):
        proc = Processor()
        code = [0x71, 0x7a, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b01111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0xff)

    # br $label7                  ;fa 14
    def test_fa_br(self):
        proc = Processor()
        code = [0xfa, 0x14]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.step()
        self.assertEqual(proc.pc, 0x1016)

    # bc $label3                  ;8d fe
    def test_8d_bc_branches_if_carry_set(self):
        proc = Processor()
        code = [0x8d, 0x34]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, 0x1036)

    # bc $label3                  ;8d fe
    def test_8d_bc_continues_if_carry_clear(self):
        proc = Processor()
        code = [0x8d, 0x14]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, 0x1000 + len(code))

    # bnc $label3                  ;9d fe
    def test_9d_bc_branches_if_carry_set(self):
        proc = Processor()
        code = [0x9d, 0x34]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, 0x1036)

    # bnc $label3                  ;9d fe
    def test_9d_bc_continues_if_carry_clear(self):
        proc = Processor()
        code = [0x9d, 0x34]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, 0x1000 + len(code))

    # bz $label5                  ;ad fe
    def test_ad_bz_branches_if_zero_set(self):
        proc = Processor()
        code = [0xad, 0x34]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.write_psw(Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, 0x1036)

    # bz $label5                  ;ad fe
    def test_ad_bz_continues_if_zero_clear(self):
        proc = Processor()
        code = [0xad, 0x34]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, 0x1000 + len(code))

    # bnz $label5                 ;bd fe
    def test_bd_bz_branches_if_zero_clear(self):
        proc = Processor()
        code = [0xbd, 0x34]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, 0x1036)

    # bnz $label5                 ;bd fe
    def test_bd_bz_continues_if_zero_set(self):
        proc = Processor()
        code = [0xbd, 0x34]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.write_psw(Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, 0x1000 + len(code))

    # clr1 a.0                    ;61 8b
    def test_61_8b_clr1_a_bit0(self):
        proc = Processor()
        code = [0x61, 0x8b]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0b11111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0b11111110)

    # clr1 a.1                    ;61 9b
    def test_61_9b_clr1_a_bit1(self):
        proc = Processor()
        code = [0x61, 0x9b]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0b11111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0b11111101)

    # clr1 a.2                    ;61 ab
    def test_61_ab_clr1_a_bit2(self):
        proc = Processor()
        code = [0x61, 0xab]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0b11111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0b11111011)

    # clr1 a.3                    ;61 bb
    def test_61_bb_clr1_a_bit3(self):
        proc = Processor()
        code = [0x61, 0xbb]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0b11111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0b11110111)

    # clr1 a.4                    ;61 cb
    def test_61_cb_clr1_a_bit4(self):
        proc = Processor()
        code = [0x61, 0xcb]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0b11111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0b11101111)

    # clr1 a.5                    ;61 db
    def test_61_db_clr1_a_bit5(self):
        proc = Processor()
        code = [0x61, 0xdb]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0b11111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0b11011111)

    # clr1 a.6                    ;61 eb
    def test_61_eb_clr1_a_bit6(self):
        proc = Processor()
        code = [0x61, 0xeb]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0b11111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0b10111111)

    # clr1 a.7                    ;61 fb
    def test_61_fb_clr1_a_bit7(self):
        proc = Processor()
        code = [0x61, 0xfb]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0b11111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0b01111111)

    # clr1 0fffeh.0               ;71 0b fe       sfr
    def test_71_0b_clr1_sfr_bit0(self):
        proc = Processor()
        code = [0x71, 0x0b, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b11111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0b11111110)

    # clr1 0fffeh.1               ;71 1b fe       sfr
    def test_71_1b_clr1_sfr_bit1(self):
        proc = Processor()
        code = [0x71, 0x1b, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b11111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0b11111101)

    # clr1 0fffeh.2               ;71 2b fe       sfr
    def test_71_2b_clr1_sfr_bit2(self):
        proc = Processor()
        code = [0x71, 0x2b, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b11111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0b11111011)

    # clr1 0fffeh.3               ;71 3b fe       sfr
    def test_71_3b_clr1_sfr_bit3(self):
        proc = Processor()
        code = [0x71, 0x3b, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b11111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0b11110111)

    # clr1 0fffeh.4               ;71 4b fe       sfr
    def test_71_4b_clr1_sfr_bit4(self):
        proc = Processor()
        code = [0x71, 0x4b, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b11111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0b11101111)

    # clr1 0fffeh.5               ;71 5b fe       sfr
    def test_71_5b_clr1_sfr_bit5(self):
        proc = Processor()
        code = [0x71, 0x5b, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b11111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0b11011111)

    # clr1 0fffeh.6               ;71 6b fe       sfr
    def test_71_6b_clr1_sfr_bit6(self):
        proc = Processor()
        code = [0x71, 0x6b, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b11111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0b10111111)

    # clr1 0fffeh.7               ;71 7b fe       sfr
    def test_71_7b_clr1_sfr_bit7(self):
        proc = Processor()
        code = [0x71, 0x7b, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b11111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0b01111111)

    # clr1 0fe20h.0               ;0b 20          saddr
    def test_0b_clr1_saddr_bit0(self):
        proc = Processor()
        code = [0x0b, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b11111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0b11111110)

    # clr1 psw.0                  ;0b 1e
    def test_0b_clr1_psw_bit0(self):
        proc = Processor()
        code = [0x0b, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b11111110)

    # clr1 0fe20h.1               ;1b 20          saddr
    def test_1b_clr1_saddr_bit1(self):
        proc = Processor()
        code = [0x1b, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b11111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0b11111101)

    # clr1 psw.1                  ;1b 1e
    def test_1b_clr1_psw_bit1(self):
        proc = Processor()
        code = [0x1b, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b11111101)

    # clr1 0fe20h.2               ;2b 20          saddr
    def test_2b_clr1_saddr_bit2(self):
        proc = Processor()
        code = [0x2b, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b11111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0b11111011)

    # clr1 psw.2                  ;2b 1e
    def test_2b_clr1_psw_bit2(self):
        proc = Processor()
        code = [0x2b, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b11111011)

    # clr1 0fe20h.3               ;3b 20          saddr
    def test_3b_clr1_saddr_bit3(self):
        proc = Processor()
        code = [0x3b, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b11111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0b11110111)

    # clr1 psw.3                  ;3b 1e
    def test_3b_clr1_psw_bit3(self):
        proc = Processor()
        code = [0x3b, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b11110111)

    # clr1 0fe20h.4               ;4b 20          saddr
    def test_4b_clr1_saddr_bit4(self):
        proc = Processor()
        code = [0x4b, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b11111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0b11101111)

    # clr1 psw.4                  ;4b 1e
    def test_4b_clr1_psw_bit4(self):
        proc = Processor()
        code = [0x4b, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b11101111)

    # clr1 0fe20h.5               ;5b 20          saddr
    def test_5b_clr1_saddr_bit5(self):
        proc = Processor()
        code = [0x5b, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b11111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0b11011111)

    # clr1 psw.5                  ;5b 1e
    def test_5b_clr1_psw_bit5(self):
        proc = Processor()
        code = [0x5b, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b11011111)

    # clr1 0fe20h.6               ;6b 20          saddr
    def test_6b_clr1_saddr_bit6(self):
        proc = Processor()
        code = [0x6b, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b11111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0b10111111)

    # clr1 psw.6                  ;6b 1e
    def test_6b_clr1_psw_bit6(self):
        proc = Processor()
        code = [0x6b, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b10111111)

    # clr1 0fe20h.7               ;7b 20          saddr
    def test_7b_clr1_saddr_bit6(self):
        proc = Processor()
        code = [0x7b, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b11111111
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0b01111111)

    # clr1 psw.7                  ;7b 1e
    # di                          ;7b 1e          alias for clr1 psw.7
    def test_7b_clr1_psw_bit7(self):
        proc = Processor()
        code = [0x7b, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111111)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b01111111)

    # movw sp,#0abcdh             ;ee 1c cd ab  (SP=0xFF1C)
    def test_ee_movw_sp_imm16(self):
        proc = Processor()
        code = [0xee, 0x1c, 0xcd, 0xab]
        proc.write_memory(0x0000, code)
        proc.sp = 0
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.sp, 0xabcd)

    # mov1 cy,a.0                 ;61 8c
    def test_61_8c_mov1_cy_a_bit0_set(self):
        proc = Processor()
        code = [0x61, 0x8c]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111110)
        proc.write_gp_reg(Registers.A, 0b01010101) # bit 0 = 1
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b11111111)# bit 0 = 1

    # mov1 cy,a.0                 ;61 8c
    def test_61_8c_mov1_cy_a_bit0_clear(self):
        proc = Processor()
        code = [0x61, 0x8c]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111111)
        proc.write_gp_reg(Registers.A, 0b10101010) # bit 0 = 0
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b11111110) # CY = 0

    # mov1 cy,a.1                 ;61 9c
    def test_61_9c_mov1_cy_a_bit1(self):
        proc = Processor()
        code = [0x61, 0x9c]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111111)
        proc.write_gp_reg(Registers.A, 0b11111101) # bit 1 = 0
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b11111110) # CY = 0

    # mov1 cy,a.2                 ;61 ac
    def test_61_ac_mov1_cy_a_bit2(self):
        proc = Processor()
        code = [0x61, 0xac]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111111)
        proc.write_gp_reg(Registers.A, 0b11111011) # bit 2 = 0
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b11111110) # CY = 0

    # mov1 cy,a.3                 ;61 bc
    def test_61_bc_mov1_cy_a_bit3(self):
        proc = Processor()
        code = [0x61, 0xbc]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111111)
        proc.write_gp_reg(Registers.A, 0b11110111) # bit 3 = 0
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b11111110) # CY = 0

    # mov1 cy,a.4                 ;61 cc
    def test_61_cc_mov1_cy_a_bit3(self):
        proc = Processor()
        code = [0x61, 0xcc]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111111)
        proc.write_gp_reg(Registers.A, 0b11101111) # bit 4 = 0
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b11111110) # CY = 0

    # mov1 cy,a.5                 ;61 dc
    def test_61_dc_mov1_cy_a_bit4(self):
        proc = Processor()
        code = [0x61, 0xdc]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111111)
        proc.write_gp_reg(Registers.A, 0b11011111) # bit 5 = 0
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b11111110) # CY = 0

    # mov1 cy,a.6                 ;61 ec
    def test_61_ec_mov1_cy_a_bit5(self):
        proc = Processor()
        code = [0x61, 0xec]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111111)
        proc.write_gp_reg(Registers.A, 0b10111111) # bit 6 = 0
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b11111110) # CY = 0

    # mov1 cy,a.7                 ;61 fc
    def test_61_fc_mov1_cy_a_bit7(self):
        proc = Processor()
        code = [0x61, 0xfc]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b11111111)
        proc.write_gp_reg(Registers.A, 0b01111111) # bit 7 = 0
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b11111110) # CY = 0

    # mov1 a.0,cy                 ;61 89
    def test_61_89_mov1_a_bit0_cy(self):
        proc = Processor()
        code = [0x61, 0x89]
        proc.write_memory(0x0000, code)
        proc.write_psw(Flags.CY)
        proc.write_gp_reg(Registers.A, 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0b00000001) # bit 0 = 1

    # mov1 a.1,cy                 ;61 99
    def test_61_99_mov1_a_bit1_cy(self):
        proc = Processor()
        code = [0x61, 0x99]
        proc.write_memory(0x0000, code)
        proc.write_psw(Flags.CY)
        proc.write_gp_reg(Registers.A, 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0b00000010) # bit 1 = 1

    # mov1 a.2,cy                 ;61 a9
    def test_61_a9_mov1_a_bit2_cy(self):
        proc = Processor()
        code = [0x61, 0xa9]
        proc.write_memory(0x0000, code)
        proc.write_psw(Flags.CY)
        proc.write_gp_reg(Registers.A, 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0b00000100) # bit 2 = 1

    # mov1 a.3,cy                 ;61 b9
    def test_61_b9_mov1_a_bit3_cy(self):
        proc = Processor()
        code = [0x61, 0xb9]
        proc.write_memory(0x0000, code)
        proc.write_psw(Flags.CY)
        proc.write_gp_reg(Registers.A, 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0b00001000) # bit 3 = 1

    # mov1 a.4,cy                 ;61 c9
    def test_61_c9_mov1_a_bit4_cy(self):
        proc = Processor()
        code = [0x61, 0xc9]
        proc.write_memory(0x0000, code)
        proc.write_psw(Flags.CY)
        proc.write_gp_reg(Registers.A, 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0b00010000) # bit 4 = 1

    # mov1 a.5,cy                 ;61 d9
    def test_61_d9_mov1_a_bit5_cy(self):
        proc = Processor()
        code = [0x61, 0xd9]
        proc.write_memory(0x0000, code)
        proc.write_psw(Flags.CY)
        proc.write_gp_reg(Registers.A, 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0b00100000) # bit 5 = 1

    # mov1 a.6,cy                 ;61 e9
    def test_61_e9_mov1_a_bit6_cy(self):
        proc = Processor()
        code = [0x61, 0xe9]
        proc.write_memory(0x0000, code)
        proc.write_psw(Flags.CY)
        proc.write_gp_reg(Registers.A, 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0b01000000) # bit 6 = 1

    # mov1 a.7,cy                 ;61 f9
    def test_61_f9_mov1_a_bit7_cy(self):
        proc = Processor()
        code = [0x61, 0xf9]
        proc.write_memory(0x0000, code)
        proc.write_psw(Flags.CY)
        proc.write_gp_reg(Registers.A, 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0b10000000) # bit 7 = 1

    # mov1 cy,0fffeh.0            ;71 0c fe       sfr
    def test_71_0c_mov1_cy_sfr_bit0(self):
        proc = Processor()
        code = [0x71, 0x0c, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b00000001
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.CY)

    # mov1 cy,0fffeh.1            ;71 1c fe       sfr
    def test_71_1c_mov1_cy_sfr_bit1(self):
        proc = Processor()
        code = [0x71, 0x1c, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b00000010
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.CY)

    # mov1 cy,0fffeh.2            ;71 2c fe       sfr
    def test_71_2c_mov1_cy_sfr_bit2(self):
        proc = Processor()
        code = [0x71, 0x2c, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b00000100
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.CY)

    # mov1 cy,0fffeh.3            ;71 3c fe       sfr
    def test_71_3c_mov1_cy_sfr_bit3(self):
        proc = Processor()
        code = [0x71, 0x3c, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b00001000
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.CY)

    # mov1 cy,0fffeh.4            ;71 4c fe       sfr
    def test_71_4c_mov1_cy_sfr_bit4(self):
        proc = Processor()
        code = [0x71, 0x4c, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b00010000
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.CY)

    # mov1 cy,0fffeh.5            ;71 5c fe       sfr
    def test_71_5c_mov1_cy_sfr_bit5(self):
        proc = Processor()
        code = [0x71, 0x5c, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b00100000
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.CY)

    # mov1 cy,0fffeh.6            ;71 6c fe       sfr
    def test_71_6c_mov1_cy_sfr_bit6(self):
        proc = Processor()
        code = [0x71, 0x6c, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b01000000
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.CY)

    # mov1 cy,0fffeh.7            ;71 7c fe       sfr
    def test_71_7c_mov1_cy_sfr_bit7(self):
        proc = Processor()
        code = [0x71, 0x7c, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0b10000000
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.CY)

    # mov1 0fffeh.0,cy            ;71 09 fe       sfr
    def test_71_09_mov1_sfr_bit_0_cy(self):
        proc = Processor()
        code = [0x71, 0x09, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0b00000001)

    # mov1 0fffeh.1,cy            ;71 19 fe       sfr
    def test_71_19_mov1_sfr_bit_1_cy(self):
        proc = Processor()
        code = [0x71, 0x19, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0b00000010)

    # mov1 0fffeh.2,cy            ;71 29 fe       sfr
    def test_71_29_mov1_sfr_bit_2_cy(self):
        proc = Processor()
        code = [0x71, 0x29, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0b00000100)

    # mov1 0fffeh.3,cy            ;71 39 fe       sfr
    def test_71_39_mov1_sfr_bit_3_cy(self):
        proc = Processor()
        code = [0x71, 0x39, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0b00001000)

    # mov1 0fffeh.4,cy            ;71 49 fe       sfr
    def test_71_49_mov1_sfr_bit_4_cy(self):
        proc = Processor()
        code = [0x71, 0x49, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0b00010000)

    # mov1 0fffeh.5,cy            ;71 59 fe       sfr
    def test_71_59_mov1_sfr_bit_5_cy(self):
        proc = Processor()
        code = [0x71, 0x59, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0b00100000)

    # mov1 0fffeh.6,cy            ;71 69 fe       sfr
    def test_71_69_mov1_sfr_bit_6_cy(self):
        proc = Processor()
        code = [0x71, 0x69, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0b01000000)

    # mov1 0fffeh.7,cy            ;71 79 fe       sfr
    def test_71_79_mov1_sfr_bit_7_cy(self):
        proc = Processor()
        code = [0x71, 0x79, 0xfe]
        proc.write_memory(0x0000, code)
        proc.memory[0xfffe] = 0
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfffe], 0b10000000)

    # mov1 0fe20h.0,cy            ;71 01 20       saddr
    def test_71_01_mov1_saddr_bit0_cy(self):
        proc = Processor()
        code = [0x71, 0x01, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0b00000001)

    # mov1 0fe20h.1,cy            ;71 11 20       saddr
    def test_71_11_mov1_saddr_bit1_cy(self):
        proc = Processor()
        code = [0x71, 0x11, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0b00000010)

    # mov1 0fe20h.2,cy            ;71 21 20       saddr
    def test_71_21_mov1_saddr_bit2_cy(self):
        proc = Processor()
        code = [0x71, 0x21, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0b00000100)

    # mov1 0fe20h.3,cy            ;71 31 20       saddr
    def test_71_31_mov1_saddr_bit3_cy(self):
        proc = Processor()
        code = [0x71, 0x31, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0b00001000)

    # mov1 0fe20h.4,cy            ;71 41 20       saddr
    def test_71_41_mov1_saddr_bit4_cy(self):
        proc = Processor()
        code = [0x71, 0x41, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0b00010000)

    # mov1 0fe20h.5,cy            ;71 51 20       saddr
    def test_71_51_mov1_saddr_bit5_cy(self):
        proc = Processor()
        code = [0x71, 0x51, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0b00100000)

    # mov1 0fe20h.6,cy            ;71 61 20       saddr
    def test_71_61_mov1_saddr_bit6_cy(self):
        proc = Processor()
        code = [0x71, 0x61, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0b01000000)

    # mov1 0fe20h.7,cy            ;71 71 20       saddr
    def test_71_71_mov1_saddr_bit7_cy(self):
        proc = Processor()
        code = [0x71, 0x71, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xfe20], 0b10000000)

    # mov1 psw.0,cy               ;71 01 1e
    def test_71_01_mov1_psw_bit0_cy(self):
        proc = Processor()
        code = [0x71, 0x01, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00000001)

    # mov1 psw.1,cy               ;71 11 1e
    def test_71_11_mov1_psw_bit1_cy(self):
        proc = Processor()
        code = [0x71, 0x11, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00000011)

    # mov1 psw.2,cy               ;71 21 1e
    def test_71_21_mov1_psw_bit2_cy(self):
        proc = Processor()
        code = [0x71, 0x21, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00000101)

    # mov1 psw.3,cy               ;71 31 1e
    def test_71_31_mov1_psw_bit3_cy(self):
        proc = Processor()
        code = [0x71, 0x31, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00001001)

    # mov1 psw.4,cy               ;71 41 1e
    def test_71_41_mov1_psw_bit4_cy(self):
        proc = Processor()
        code = [0x71, 0x41, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00010001)

    # mov1 psw.5,cy               ;71 51 1e
    def test_71_51_mov1_psw_bit5_cy(self):
        proc = Processor()
        code = [0x71, 0x51, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00100001)

    # mov1 psw.6,cy               ;71 61 1e
    def test_71_61_mov1_psw_bit6_cy(self):
        proc = Processor()
        code = [0x71, 0x61, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b01000001)

    # mov1 psw.7,cy               ;71 71 1e
    def test_71_71_mov1_psw_bit7_cy(self):
        proc = Processor()
        code = [0x71, 0x71, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(Flags.CY)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b10000001)

    # mov1 cy,0fe20h.0            ;71 04 20       saddr
    def test_71_04_mov1_cy_saddr_bit0(self):
        proc = Processor()
        code = [0x71, 0x04, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b00000001
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00000001)

    # mov1 cy,0fe20h.1            ;71 14 20       saddr
    def test_71_14_mov1_cy_saddr_bit1(self):
        proc = Processor()
        code = [0x71, 0x14, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b00000010
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00000001)

    # mov1 cy,0fe20h.2            ;71 24 20       saddr
    def test_71_24_mov1_cy_saddr_bit2(self):
        proc = Processor()
        code = [0x71, 0x24, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b00000100
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00000001)

    # mov1 cy,0fe20h.3            ;71 34 20       saddr
    def test_71_34_mov1_cy_saddr_bit3(self):
        proc = Processor()
        code = [0x71, 0x34, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b00001000
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00000001)

    # mov1 cy,0fe20h.4            ;71 44 20       saddr
    def test_71_44_mov1_cy_saddr_bit4(self):
        proc = Processor()
        code = [0x71, 0x44, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b00010000
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00000001)

    # mov1 cy,0fe20h.5            ;71 54 20       saddr
    def test_71_54_mov1_cy_saddr_bit5(self):
        proc = Processor()
        code = [0x71, 0x54, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b00100000
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00000001)

    # mov1 cy,0fe20h.6            ;71 64 20       saddr
    def test_71_64_mov1_cy_saddr_bit6(self):
        proc = Processor()
        code = [0x71, 0x64, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b01000000
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00000001)

    # mov1 cy,0fe20h.7            ;71 74 20       saddr
    def test_71_74_mov1_cy_saddr_bit7(self):
        proc = Processor()
        code = [0x71, 0x74, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0b10000000
        proc.write_psw(0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00000001)

    # mov1 cy,psw.0               ;71 04 1e
    def test_71_04_mov1_cy_psw_bit0(self):
        proc = Processor()
        code = [0x71, 0x04, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b00000001)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00000001)

    # mov1 cy,psw.1               ;71 14 1e
    def test_71_14_mov1_cy_psw_bit1(self):
        proc = Processor()
        code = [0x71, 0x14, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b00000010)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00000011)

    # mov1 cy,psw.2               ;71 24 1e
    def test_71_24_mov1_cy_psw_bit2(self):
        proc = Processor()
        code = [0x71, 0x24, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b00000100)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00000101)

    # mov1 cy,psw.3               ;71 34 1e
    def test_71_34_mov1_cy_psw_bit3(self):
        proc = Processor()
        code = [0x71, 0x34, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b00001000)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00001001)

    # mov1 cy,psw.4               ;71 44 1e
    def test_71_44_mov1_cy_psw_bit4(self):
        proc = Processor()
        code = [0x71, 0x44, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b00010000)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00010001)

    # mov1 cy,psw.5               ;71 54 1e
    def test_71_54_mov1_cy_psw_bit5(self):
        proc = Processor()
        code = [0x71, 0x54, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b00100000)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b00100001)

    # mov1 cy,psw.6               ;71 64 1e
    def test_71_64_mov1_cy_psw_bit6(self):
        proc = Processor()
        code = [0x71, 0x64, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b01000000)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b01000001)

    # mov1 cy,psw.7               ;71 74 1e
    def test_71_74_mov1_cy_psw_bit7(self):
        proc = Processor()
        code = [0x71, 0x74, 0x1e]
        proc.write_memory(0x0000, code)
        proc.write_psw(0b10000000)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0b10000001)

    #    inc x                       ;40
    def test_40_inc_x_result_0_to_1_clears_z_ac(self):
        proc = Processor()
        code = [0x40]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.X, 0)
        proc.write_psw(Flags.Z | Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0)
        self.assertEqual(proc.read_gp_reg(Registers.X), 1)

    #    inc x                       ;40
    def test_40_inc_x_result_ff_to_0_wraps_and_sets_z(self):
        proc = Processor()
        code = [0x40]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.X, 0xFF)
        proc.write_psw(Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.Z)
        self.assertEqual(proc.read_gp_reg(Registers.X), 0)

    #    inc x                       ;40
    def test_40_inc_x_result_0f_to_10_sets_ac(self):
        proc = Processor()
        code = [0x40]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.X, 0b00001111)
        proc.write_psw(Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.AC)
        self.assertEqual(proc.read_gp_reg(Registers.X), 0b00010000)

    #    inc a                       ;41
    def test_41_inc_a(self):
        proc = Processor()
        code = [0x41]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 0)
        proc.write_psw(Flags.Z | Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0)
        self.assertEqual(proc.read_gp_reg(Registers.A), 1)

    #    inc c                       ;42
    def test_42_inc_c(self):
        proc = Processor()
        code = [0x42]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.C, 0)
        proc.write_psw(Flags.Z | Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0)
        self.assertEqual(proc.read_gp_reg(Registers.C), 1)

    #    inc b                       ;43
    def test_43_inc_b(self):
        proc = Processor()
        code = [0x43]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.B, 0)
        proc.write_psw(Flags.Z | Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0)
        self.assertEqual(proc.read_gp_reg(Registers.B), 1)

    #    inc e                       ;44
    def test_44_inc_e(self):
        proc = Processor()
        code = [0x44]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.E, 0)
        proc.write_psw(Flags.Z | Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0)
        self.assertEqual(proc.read_gp_reg(Registers.E), 1)

    #    inc d                       ;45
    def test_45_inc_d(self):
        proc = Processor()
        code = [0x45]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.D, 0)
        proc.write_psw(Flags.Z | Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0)
        self.assertEqual(proc.read_gp_reg(Registers.D), 1)

    #    inc l                       ;46
    def test_46_inc_l(self):
        proc = Processor()
        code = [0x46]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.L, 0)
        proc.write_psw(Flags.Z | Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0)
        self.assertEqual(proc.read_gp_reg(Registers.L), 1)

    #    inc h                       ;47
    def test_47_inc_h(self):
        proc = Processor()
        code = [0x47]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.H, 0)
        proc.write_psw(Flags.Z | Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0)
        self.assertEqual(proc.read_gp_reg(Registers.H), 1)

    # inc 0fe20h                  ;81 20          saddr
    def test_81_inc_saddr(self):
        proc = Processor()
        code = [0x81, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(Flags.Z | Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0)
        self.assertEqual(proc.memory[0xfe20], 1)

    # callf !0842h                ;0c 42
    def test_0c_callf_addr11(self):
        proc = Processor()
        code = [0x0c, 0x42]
        proc.write_memory(0x0123, code)
        proc.pc = 0x0123
        return_address = proc.pc + len(code)
        proc.sp = 0xFE1F
        proc.step()
        self.assertEqual(proc.sp, 0xFE1d)
        self.assertEqual(proc.memory[0xFE1d], (return_address & 0xFF))
        self.assertEqual(proc.memory[0xFE1e], (return_address >> 8))
        self.assertEqual(proc.pc, 0x0842)

    # callf !0942h                ;1c 42
    def test_1c_callf_addr11(self):
        proc = Processor()
        code = [0x1c, 0x42]
        proc.write_memory(0x0123, code)
        proc.pc = 0x0123
        return_address = proc.pc + len(code)
        proc.sp = 0xFE1F
        proc.step()
        self.assertEqual(proc.sp, 0xFE1d)
        self.assertEqual(proc.memory[0xFE1d], (return_address & 0xFF))
        self.assertEqual(proc.memory[0xFE1e], (return_address >> 8))
        self.assertEqual(proc.pc, 0x0942)

    # callf !0a42h                ;2c 42
    def test_2c_callf_addr11(self):
        proc = Processor()
        code = [0x2c, 0x42]
        proc.write_memory(0x0123, code)
        proc.pc = 0x0123
        return_address = proc.pc + len(code)
        proc.sp = 0xFE1F
        proc.step()
        self.assertEqual(proc.sp, 0xFE1d)
        self.assertEqual(proc.memory[0xFE1d], (return_address & 0xFF))
        self.assertEqual(proc.memory[0xFE1e], (return_address >> 8))
        self.assertEqual(proc.pc, 0x0a42)

    # callf !0b42h                ;3c 42
    def test_3c_callf_addr11(self):
        proc = Processor()
        code = [0x3c, 0x42]
        proc.write_memory(0x0123, code)
        proc.pc = 0x0123
        return_address = proc.pc + len(code)
        proc.sp = 0xFE1F
        proc.step()
        self.assertEqual(proc.sp, 0xFE1d)
        self.assertEqual(proc.memory[0xFE1d], (return_address & 0xFF))
        self.assertEqual(proc.memory[0xFE1e], (return_address >> 8))
        self.assertEqual(proc.pc, 0x0b42)

    # callf !0c42h                ;4c 42
    def test_4c_callf_addr11(self):
        proc = Processor()
        code = [0x4c, 0x42]
        proc.write_memory(0x0123, code)
        proc.pc = 0x0123
        return_address = proc.pc + len(code)
        proc.sp = 0xFE1F
        proc.step()
        self.assertEqual(proc.sp, 0xFE1d)
        self.assertEqual(proc.memory[0xFE1d], (return_address & 0xFF))
        self.assertEqual(proc.memory[0xFE1e], (return_address >> 8))
        self.assertEqual(proc.pc, 0x0c42)

    # callf !0d42h                ;5c 42
    def test_5c_callf_addr11(self):
        proc = Processor()
        code = [0x5c, 0x42]
        proc.write_memory(0x0123, code)
        proc.pc = 0x0123
        return_address = proc.pc + len(code)
        proc.sp = 0xFE1F
        proc.step()
        self.assertEqual(proc.sp, 0xFE1d)
        self.assertEqual(proc.memory[0xFE1d], (return_address & 0xFF))
        self.assertEqual(proc.memory[0xFE1e], (return_address >> 8))
        self.assertEqual(proc.pc, 0x0d42)

    # callf !0e42h                ;6c 42
    def test_6c_callf_addr11(self):
        proc = Processor()
        code = [0x6c, 0x42]
        proc.write_memory(0x0123, code)
        proc.pc = 0x0123
        return_address = proc.pc + len(code)
        proc.sp = 0xFE1F
        proc.step()
        self.assertEqual(proc.sp, 0xFE1d)
        self.assertEqual(proc.memory[0xFE1d], (return_address & 0xFF))
        self.assertEqual(proc.memory[0xFE1e], (return_address >> 8))
        self.assertEqual(proc.pc, 0x0e42)

    # callf !0f42h                ;7c 42
    def test_7c_callf_addr11(self):
        proc = Processor()
        code = [0x7c, 0x42]
        proc.write_memory(0x0123, code)
        proc.pc = 0x0123
        return_address = proc.pc + len(code)
        proc.sp = 0xFE1F
        proc.step()
        self.assertEqual(proc.sp, 0xFE1d)
        self.assertEqual(proc.memory[0xFE1d], (return_address & 0xFF))
        self.assertEqual(proc.memory[0xFE1e], (return_address >> 8))
        self.assertEqual(proc.pc, 0x0f42)

    def test_c1_to_ff_callt(self):
        vectors_by_opcode = {0xC1: 0x0040, 0xC3: 0x0042, 0xC5: 0x0044, 0xC7: 0x0046,
                             0xC9: 0x0048, 0xCB: 0x004a, 0xCD: 0x004c, 0xCF: 0x004e,
                             0xD1: 0x0050, 0xD3: 0x0052, 0xD5: 0x0054, 0xD7: 0x0056,
                             0xD9: 0x0058, 0xDB: 0x005A, 0xDD: 0x005C, 0xDF: 0x005e,
                             0xE1: 0x0060, 0xE3: 0x0062, 0xE5: 0x0064, 0xE7: 0x0066,
                             0xE9: 0x0068, 0xEB: 0x006a, 0xED: 0x006c, 0xEF: 0x006e,
                             0xF1: 0x0070, 0xF3: 0x0072, 0xF5: 0x0074, 0xF7: 0x0076,
                             0xF9: 0x0078, 0xFB: 0x007a, 0xFD: 0x007c, 0xFF: 0x007e,
                            }
        for opcode, vector in vectors_by_opcode.items():
            proc = Processor()
            subroutine_address = 0xabcd
            proc.memory[vector] = subroutine_address & 0xFF
            proc.memory[vector+1] = subroutine_address >> 8

            code = [opcode]
            proc.write_memory(0x1000, code)
            proc.pc = 0x1000
            return_address = proc.pc + len(code)

            proc.sp = 0xFE1F
            proc.step()
            self.assertEqual(proc.sp, 0xFE1d)
            self.assertEqual(proc.memory[0xFE1d], (return_address & 0xFF))
            self.assertEqual(proc.memory[0xFE1e], (return_address >> 8))
            self.assertEqual(proc.pc, 0xabcd)

    # rolc a,1                    ;27
    def test_27_rolc_a(self):
        tests = ((0,         0b00000000, 0,        0b00000000),
                 (Flags.CY,  0b00000000, 0,        0b00000001),
                 (0,         0b10000000, Flags.CY, 0b00000000),
                 (Flags.CY,  0b11111111, Flags.CY, 0b11111111),
                 (Flags.CY,  0b11000001, Flags.CY, 0b10000011))
        for original_psw, original_a, rotated_psw, rotated_a in tests:
            proc = Processor()
            code = [0x27]
            proc.write_memory(0x0000, code)
            proc.write_psw(original_psw)
            proc.write_gp_reg(Registers.A, original_a)
            proc.step()
            self.assertEqual(proc.pc, len(code))
            self.assertEqual(proc.read_gp_reg(Registers.A), rotated_a)
            self.assertEqual(proc.read_psw(), rotated_psw)

    # rorc a,1                    ;25
    def test_25_rorc_a(self):
        tests = ((0,         0b00000000, 0,        0b00000000),
                 (Flags.CY,  0b00000000, 0,        0b10000000),
                 (0,         0b00000001, Flags.CY, 0b00000000),
                 (Flags.CY,  0b11111111, Flags.CY, 0b11111111),
                 (Flags.CY,  0b11000001, Flags.CY, 0b11100000))
        for original_psw, original_a, rotated_psw, rotated_a in tests:
            proc = Processor()
            code = [0x25]
            proc.write_memory(0x0000, code)
            proc.write_psw(original_psw)
            proc.write_gp_reg(Registers.A, original_a)
            proc.step()
            self.assertEqual(proc.pc, len(code))
            self.assertEqual(proc.read_gp_reg(Registers.A), rotated_a)
            self.assertEqual(proc.read_psw(), rotated_psw)

    # rol a,1                    ;26
    def test_26_rol_a(self):
        tests = ((0,         0b00000000, 0,        0b00000000),
                 (Flags.CY,  0b01000010, 0,        0b10000100),
                 (0,         0b10010000, Flags.CY, 0b00100001),
                 (0,         0b11111111, Flags.CY, 0b11111111),
                 (Flags.CY,  0b10000000, Flags.CY, 0b00000001),)
        for original_psw, original_a, rotated_psw, rotated_a in tests:
            proc = Processor()
            code = [0x26]
            proc.write_memory(0x0000, code)
            proc.write_psw(original_psw)
            proc.write_gp_reg(Registers.A, original_a)
            proc.step()
            self.assertEqual(proc.pc, len(code))
            self.assertEqual(proc.read_gp_reg(Registers.A), rotated_a)
            self.assertEqual(proc.read_psw(), rotated_psw)

    # ror a,1                     ;24
    def test_24_ror_a(self):
        tests = ((0,         0b00000000, 0,        0b00000000),
                 (Flags.CY,  0b00000000, 0,        0b00000000),
                 (0,         0b11111111, Flags.CY, 0b11111111),
                 (0,         0b00000101, Flags.CY, 0b10000010),
                 (Flags.CY,  0b00000001, Flags.CY, 0b10000000),)
        for original_psw, original_a, rotated_psw, rotated_a in tests:
            proc = Processor()
            code = [0x24]
            proc.write_memory(0x0000, code)
            proc.write_psw(original_psw)
            proc.write_gp_reg(Registers.A, original_a)
            proc.step()
            self.assertEqual(proc.pc, len(code))
            self.assertEqual(proc.read_gp_reg(Registers.A), rotated_a)
            self.assertEqual(proc.read_psw(), rotated_psw)

    # dec x                       ;50
    def test_50_dec_x_0_to_ff_wraps_clears_z_ac(self):
        proc = Processor()
        code = [0x50]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.X, 0)
        proc.write_psw(Flags.Z | Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0)
        self.assertEqual(proc.read_gp_reg(Registers.X), 0xFF)

    # dec x                       ;50
    def test_50_dec_x_1_to_0_sets_z_clears_ac(self):
        proc = Processor()
        code = [0x50]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.X, 1)
        proc.write_psw(Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.Z)
        self.assertEqual(proc.read_gp_reg(Registers.X), 0)

    # dec x                       ;50
    def test_dec_x_10_to_0f_clears_z_sets_ac(self):
        proc = Processor()
        code = [0x50]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.X, 0x10)
        proc.write_psw(Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.AC)
        self.assertEqual(proc.read_gp_reg(Registers.X), 0x0f)

    # dec x                       ;50
    def test_dec_x_ff_to_fe_clears_z_clears_ac(self):
        proc = Processor()
        code = [0x50]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.X, 0xff)
        proc.write_psw(Flags.Z | Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), 0)
        self.assertEqual(proc.read_gp_reg(Registers.X), 0xfe)

    # dec a                       ;51
    def test_51_dec_a(self):
        proc = Processor()
        code = [0x51]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.A, 1)
        proc.write_psw(Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.Z)
        self.assertEqual(proc.read_gp_reg(Registers.A), 0)

    # dec c                       ;52
    def test_52_dec_c(self):
        proc = Processor()
        code = [0x52]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.C, 1)
        proc.write_psw(Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.Z)
        self.assertEqual(proc.read_gp_reg(Registers.C), 0)

    # dec b                       ;53
    def test_53_dec_b(self):
        proc = Processor()
        code = [0x53]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.B, 1)
        proc.write_psw(Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.Z)
        self.assertEqual(proc.read_gp_reg(Registers.B), 0)

    # dec e                       ;54
    def test_54_dec_e(self):
        proc = Processor()
        code = [0x54]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.E, 1)
        proc.write_psw(Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.Z)
        self.assertEqual(proc.read_gp_reg(Registers.E), 0)

    # dec d                       ;55
    def test_55_dec_d(self):
        proc = Processor()
        code = [0x55]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.D, 1)
        proc.write_psw(Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.Z)
        self.assertEqual(proc.read_gp_reg(Registers.D), 0)

    # dec l                       ;56
    def test_56_dec_d(self):
        proc = Processor()
        code = [0x56]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.L, 1)
        proc.write_psw(Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.Z)
        self.assertEqual(proc.read_gp_reg(Registers.L), 0)

    # dec h                       ;57
    def test_57_dec_h(self):
        proc = Processor()
        code = [0x57]
        proc.write_memory(0x0000, code)
        proc.write_gp_reg(Registers.H, 1)
        proc.write_psw(Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.Z)
        self.assertEqual(proc.read_gp_reg(Registers.H), 0)

    # dec 0fe20h                  ;91 20          saddr
    def test_91_dec_saddr(self):
        proc = Processor()
        code = [0x91, 0x20]
        proc.write_memory(0x0000, code)
        proc.memory[0xfe20] = 1
        proc.write_psw(Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_psw(), Flags.Z)
        self.assertEqual(proc.memory[0xfe20], 0)

    # dbnz c,$label1              ;8a fe
    def test_8a_dbnz_c_0_to_ff_branches(self):
        proc = Processor()
        code = [0x8a, 0xf0]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.write_gp_reg(Registers.C, 0)
        proc.write_psw(Flags.AC | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, 0x0ff2) # branch taken
        self.assertEqual(proc.read_psw(), Flags.AC | Flags.Z) # unchanged
        self.assertEqual(proc.read_gp_reg(Registers.C), 0xFF) # decremented

    # dbnz c,$label1              ;8a fe
    def test_8a_dbnz_c_3_to_2_branches(self):
        proc = Processor()
        code = [0x8a, 0xf0]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.write_gp_reg(Registers.C, 3)
        proc.write_psw(Flags.AC | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, 0x0ff2) # branch taken
        self.assertEqual(proc.read_psw(), Flags.AC | Flags.Z) # unchanged
        self.assertEqual(proc.read_gp_reg(Registers.C), 2) # decremented

    # dbnz c,$label1              ;8a fe
    def test_8a_dbnz_c_1_to_0_doesnt_branch(self):
        proc = Processor()
        code = [0x8a, 0xf0]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.write_gp_reg(Registers.C, 1)
        proc.write_psw(Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, 0x1000+len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), Flags.AC) # unchanged
        self.assertEqual(proc.read_gp_reg(Registers.C), 0) # decremented

    # dbnz b,$label2              ;8b fe
    def test_8b_dbnz_b_0_to_ff_branches(self):
        proc = Processor()
        code = [0x8b, 0xf0]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.write_gp_reg(Registers.B, 0)
        proc.write_psw(Flags.AC | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, 0x0ff2) # branch taken
        self.assertEqual(proc.read_psw(), Flags.AC | Flags.Z) # unchanged
        self.assertEqual(proc.read_gp_reg(Registers.B), 0xFF) # decremented

    # dbnz b,$label1              ;8b fe
    def test_8b_dbnz_b_3_to_2_branches(self):
        proc = Processor()
        code = [0x8b, 0xf0]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.write_gp_reg(Registers.B, 3)
        proc.write_psw(Flags.AC | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, 0x0ff2) # branch taken
        self.assertEqual(proc.read_psw(), Flags.AC | Flags.Z) # unchanged
        self.assertEqual(proc.read_gp_reg(Registers.B), 2) # decremented

    # dbnz b,$label1              ;8b fe
    def test_8b_dbnz_b_1_to_0_doesnt_branch(self):
        proc = Processor()
        code = [0x8b, 0xf0]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.write_gp_reg(Registers.B, 1)
        proc.write_psw(Flags.AC)
        proc.step()
        self.assertEqual(proc.pc, 0x1000+len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), Flags.AC) # unchanged
        self.assertEqual(proc.read_gp_reg(Registers.B), 0) # decremented

    # dbnz 0fe20h,$label0         ;04 20 fd       saddr
    def test_04_dbnz_saddr_0_to_ff_branches(self):
        proc = Processor()
        code = [0x04, 0x20, 0xf0]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.memory[0xfe20] = 0
        proc.write_psw(Flags.AC | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, 0x0ff3) # branch taken
        self.assertEqual(proc.read_psw(), Flags.AC | Flags.Z) # unchanged
        self.assertEqual(proc.memory[0xfe20], 0xFF) # decremented

    # dbnz 0fe20h,$label0         ;04 20 fd       saddr
    def test_04_dbnz_saddr_3_to_2_branches(self):
        proc = Processor()
        code = [0x04, 0x20, 0xf0]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.memory[0xfe20] = 3
        proc.write_psw(Flags.AC | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, 0x0ff3) # branch taken
        self.assertEqual(proc.read_psw(), Flags.AC | Flags.Z) # unchanged
        self.assertEqual(proc.memory[0xfe20], 2) # decremented

    # dbnz 0fe20h,$label0         ;04 20 fd       saddr
    def test_04_dbnz_saddr_1_to_0_doesnt_branch(self):
        proc = Processor()
        code = [0x04, 0x20, 0xf0]
        proc.write_memory(0x1000, code)
        proc.pc = 0x1000
        proc.memory[0xfe20] = 1
        proc.write_psw(Flags.AC | Flags.Z)
        proc.step()
        self.assertEqual(proc.pc, 0x1000+len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), Flags.AC | Flags.Z) # unchanged
        self.assertEqual(proc.memory[0xfe20], 0) # decremented

    # bt a.0,$label32             ;31 0e fd
    def test_31_0e_bt_a_bit0_branches_if_set(self):
        proc = Processor()
        code = [0x31, 0x0e, 0x20]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0b00000001)
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x23) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt a.0,$label32             ;31 0e fd
    def test_31_0e_bt_a_bit0_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x31, 0x0e, 0x20]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0)
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    #  bt a.1,$label33             ;31 1e fd
    def test_31_1e_bt_a_bit1_branches_if_set(self):
        proc = Processor()
        code = [0x31, 0x1e, 0x20]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0b00000010)
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x23) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt a.1,$label33             ;31 1e fd
    def test_31_1e_bt_a_bit1_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x31, 0x1e, 0x20]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0)
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt a.2,$label34             ;31 2e fd
    def test_31_2e_bt_a_bit2_branches_if_set(self):
        proc = Processor()
        code = [0x31, 0x2e, 0x20]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0b00000100)
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x23) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt a.2,$label34             ;31 2e fd
    def test_31_2e_bt_a_bit2_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x31, 0x2e, 0x20]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0)
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt a.3,$label35             ;31 3e fd
    def test_31_3e_bt_a_bit3_branches_if_set(self):
        proc = Processor()
        code = [0x31, 0x3e, 0x20]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0b00001000)
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x23) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt a.3,$label35             ;31 3e fd
    def test_31_3e_bt_a_bit3_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x31, 0x3e, 0x20]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0)
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt a.4,$label36             ;31 4e fd
    def test_31_4e_bt_a_bit4_branches_if_set(self):
        proc = Processor()
        code = [0x31, 0x4e, 0x20]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0b00010000)
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x23) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt a.4,$label36             ;31 4e fd
    def test_31_4e_bt_a_bit4_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x31, 0x4e, 0x20]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0)
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt a.5,$label37             ;31 5e fd
    def test_31_5e_bt_a_bit5_branches_if_set(self):
        proc = Processor()
        code = [0x31, 0x5e, 0x20]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0b00100000)
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x23) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt a.5,$label37             ;31 5e fd
    def test_31_5e_bt_a_bit5_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x31, 0x5e, 0x20]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0)
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt a.6,$label38             ;31 6e fd
    def test_31_6e_bt_a_bit6_branches_if_set(self):
        proc = Processor()
        code = [0x31, 0x6e, 0x20]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0b01000000)
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x23) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt a.6,$label38             ;31 6e fd
    def test_31_6e_bt_a_bit6_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x31, 0x6e, 0x20]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0)
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt a.7,$label39             ;31 7e fd
    def test_31_7e_bt_a_bit7_branches_if_set(self):
        proc = Processor()
        code = [0x31, 0x7e, 0x20]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0b10000000)
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x23) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt a.7,$label39             ;31 7e fd
    def test_31_7e_bt_a_bit7_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x31, 0x7e, 0x20]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0)
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fffeh.0,$label24        ;31 06 fe fc    sfr
    def test_31_06_bt_a_bit0_branches_if_set(self):
        proc = Processor()
        code = [0x31, 0x06, 0xfe, 0x20]
        proc.write_memory(0, code)
        proc.memory[0x0fffe] = 0b00000001
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x24) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fffeh.0,$label24        ;31 06 fe fc    sfr
    def test_31_06_bt_a_bit0_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x31, 0x06, 0xfe, 0x20]
        proc.write_memory(0, code)
        proc.memory[0x0fffe] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fffeh.1,$label25        ;31 16 fe fc    sfr
    def test_31_16_bt_a_bit1_branches_if_set(self):
        proc = Processor()
        code = [0x31, 0x16, 0xfe, 0x20]
        proc.write_memory(0, code)
        proc.memory[0x0fffe] = 0b00000010
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x24) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fffeh.1,$label25        ;31 16 fe fc    sfr
    def test_31_16_bt_a_bit1_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x31, 0x16, 0xfe, 0x20]
        proc.write_memory(0, code)
        proc.memory[0x0fffe] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fffeh.2,$label26        ;31 26 fe fc    sfr
    def test_31_26_bt_a_bit2_branches_if_set(self):
        proc = Processor()
        code = [0x31, 0x26, 0xfe, 0x20]
        proc.write_memory(0, code)
        proc.memory[0x0fffe] = 0b00000100
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x24) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fffeh.2,$label26        ;31 26 fe fc    sfr
    def test_31_26_bt_a_bit2_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x31, 0x26, 0xfe, 0x20]
        proc.write_memory(0, code)
        proc.memory[0x0fffe] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fffeh.3,$label27        ;31 36 fe fc    sfr
    def test_31_36_bt_a_bit3_branches_if_set(self):
        proc = Processor()
        code = [0x31, 0x36, 0xfe, 0x20]
        proc.write_memory(0, code)
        proc.memory[0x0fffe] = 0b00001000
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x24) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fffeh.3,$label27        ;31 36 fe fc    sfr
    def test_31_36_bt_a_bit3_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x31, 0x36, 0xfe, 0x20]
        proc.write_memory(0, code)
        proc.memory[0x0fffe] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fffeh.4,$label28        ;31 46 fe fc    sfr
    def test_31_46_bt_a_bit4_branches_if_set(self):
        proc = Processor()
        code = [0x31, 0x46, 0xfe, 0x20]
        proc.write_memory(0, code)
        proc.memory[0x0fffe] = 0b00010000
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x24) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fffeh.4,$label28        ;31 46 fe fc    sfr
    def test_31_46_bt_a_bit4_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x31, 0x46, 0xfe, 0x20]
        proc.write_memory(0, code)
        proc.memory[0x0fffe] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fffeh.5,$label29        ;31 56 fe fc    sfr
    def test_31_56_bt_a_bit5_branches_if_set(self):
        proc = Processor()
        code = [0x31, 0x56, 0xfe, 0x20]
        proc.write_memory(0, code)
        proc.memory[0x0fffe] = 0b00100000
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x24) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fffeh.5,$label29        ;31 56 fe fc    sfr
    def test_31_56_bt_a_bit5_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x31, 0x56, 0xfe, 0x20]
        proc.write_memory(0, code)
        proc.memory[0x0fffe] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fffeh.6,$label30        ;31 66 fe fc    sfr
    def test_31_66_bt_a_bit6_branches_if_set(self):
        proc = Processor()
        code = [0x31, 0x66, 0xfe, 0x20]
        proc.write_memory(0, code)
        proc.memory[0x0fffe] = 0b01000000
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x24) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fffeh.6,$label30        ;31 66 fe fc    sfr
    def test_31_66_bt_a_bit6_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x31, 0x66, 0xfe, 0x20]
        proc.write_memory(0, code)
        proc.memory[0x0fffe] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fffeh.7,$label31        ;31 76 fe fc    sfr
    def test_31_76_bt_a_bit7_branches_if_set(self):
        proc = Processor()
        code = [0x31, 0x76, 0xfe, 0x20]
        proc.write_memory(0, code)
        proc.memory[0x0fffe] = 0b10000000
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x24) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fffeh.7,$label31        ;31 76 fe fc    sfr
    def test_31_76_bt_a_bit7_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x31, 0x76, 0xfe, 0x20]
        proc.write_memory(0, code)
        proc.memory[0x0fffe] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt psw.0,$label9            ;8c 1e fd
    def test_8c_bt_psw_bit0_branches_if_set(self):
        proc = Processor()
        code = [0x8c, 0x1e, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0b00000001
        proc.write_psw(0b00000001)
        proc.step()
        self.assertEqual(proc.pc, 0x33) # branch taken
        self.assertEqual(proc.read_psw(), 0b00000001) # unchanged

    # bt 0fe20h.0,$label8         ;8c 20 fd       saddr
    def test_8c_bt_saddr_bit0_branches_if_set(self):
        proc = Processor()
        code = [0x8c, 0x20, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0b00000001
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x33) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fe20h.0,$label8         ;8c 20 fd       saddr
    def test_8c_bt_saddr_bit0_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x8c, 0x20, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fe20h.1,$label10        ;9c 20 fd       saddr
    def test_9c_bt_saddr_bit1_branches_if_set(self):
        proc = Processor()
        code = [0x9c, 0x20, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0b00000010
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x33) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt psw.1,$label11           ;9c 1e fd
    def test_9c_bt_psw_bit1_branches_if_set(self):
        proc = Processor()
        code = [0x9c, 0x1e, 0x30]
        proc.write_memory(0, code)
        proc.write_psw(0b00000010)
        proc.step()
        self.assertEqual(proc.pc, 0x33) # branch taken
        self.assertEqual(proc.read_psw(), 0b00000010) # unchanged

    # bt 0fe20h.1,$label10        ;9c 20 fd       saddr
    def test_9c_bt_saddr_bit1_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0x9c, 0x20, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fe20h.2,$label12        ;ac 20 fd       saddr
    def test_ac_bt_saddr_bit2_branches_if_set(self):
        proc = Processor()
        code = [0xac, 0x20, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0b00000100
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x33) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt psw.2,$label13           ;ac 1e fd
    def test_ac_bt_psw_bit2_branches_if_set(self):
        proc = Processor()
        code = [0xac, 0x1e, 0x30]
        proc.write_memory(0, code)
        proc.write_psw(0b00000100)
        proc.step()
        self.assertEqual(proc.pc, 0x33) # branch taken
        self.assertEqual(proc.read_psw(), 0b00000100) # unchanged

    # bt 0fe20h.2,$label12        ;ac 20 fd       saddr
    def test_ac_bt_saddr_bit2_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0xac, 0x20, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fe20h.3,$label14        ;bc 20 fd       saddr
    def test_bc_bt_saddr_bit3_branches_if_set(self):
        proc = Processor()
        code = [0xbc, 0x20, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0b00001000
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x33) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt psw.3,$label15           ;bc 1e fd
    def test_bc_bt_psw_bit3_branches_if_set(self):
        proc = Processor()
        code = [0xbc, 0x1e, 0x30]
        proc.write_memory(0, code)
        proc.write_psw(0b00001000)
        proc.step()
        self.assertEqual(proc.pc, 0x33) # branch taken
        self.assertEqual(proc.read_psw(), 0b00001000) # unchanged

    # bt 0fe20h.3,$label14        ;bc 20 fd       saddr
    def test_bc_bt_saddr_bit3_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0xbc, 0x20, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fe20h.4,$label16        ;cc 20 fd       saddr
    def test_cc_bt_saddr_bit4_branches_if_set(self):
        proc = Processor()
        code = [0xcc, 0x20, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0b0010000
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x33) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt psw.4,$label17           ;cc 1e fd
    def test_cc_bt_psw_bit4_branches_if_set(self):
        proc = Processor()
        code = [0xcc, 0x1e, 0x30]
        proc.write_memory(0, code)
        proc.write_psw(0b0010000)
        proc.step()
        self.assertEqual(proc.pc, 0x33) # branch taken
        self.assertEqual(proc.read_psw(), 0b0010000) # unchanged

    # bt 0fe20h.4,$label16        ;cc 20 fd       saddr
    def test_cc_bt_saddr_bit4_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0xcc, 0x20, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fe20h.5,$label20        ;dc 20 fd       saddr
    def test_dc_bt_saddr_bit5_branches_if_set(self):
        proc = Processor()
        code = [0xdc, 0x20, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0b00100000
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x33) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt psw.5,$label21           ;dc 1e fd
    def test_dc_bt_psw_bit5_branches_if_set(self):
        proc = Processor()
        code = [0xdc, 0x1e, 0x30]
        proc.write_memory(0, code)
        proc.write_psw(0b00100000)
        proc.step()
        self.assertEqual(proc.pc, 0x33) # branch taken
        self.assertEqual(proc.read_psw(), 0b00100000) # unchanged

    # bt 0fe20h.5,$label20        ;dc 20 fd       saddr
    def test_dc_bt_saddr_bit5_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0xdc, 0x20, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fe20h.6,$label22        ;ec 20 fd       saddr
    def test_ec_bt_saddr_bit6_branches_if_set(self):
        proc = Processor()
        code = [0xec, 0x20, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0b01000000
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x33) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt psw.6,$label23           ;ec 1e fd
    def test_ec_bt_psw_bit6_branches_if_set(self):
        proc = Processor()
        code = [0xec, 0x1e, 0x30]
        proc.write_memory(0, code)
        proc.write_psw(0b01000000)
        proc.step()
        self.assertEqual(proc.pc, 0x33) # branch taken
        self.assertEqual(proc.read_psw(), 0b01000000) # unchanged

    # bt 0fe20h.6,$label22        ;ec 20 fd       saddr
    def test_ec_bt_saddr_bit6_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0xec, 0x20, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt 0fe20h.7,$label18        ;fc 20 fd       saddr
    def test_fc_bt_saddr_bit7_branches_if_set(self):
        proc = Processor()
        code = [0xfc, 0x20, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0b10000000
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, 0x33) # branch taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # bt psw.7,$label19           ;fc 1e fd
    def test_fc_bt_psw_bit7_branches_if_set(self):
        proc = Processor()
        code = [0xfc, 0x1e, 0x30]
        proc.write_memory(0, code)
        proc.write_psw(0b10000000)
        proc.step()
        self.assertEqual(proc.pc, 0x33) # branch taken
        self.assertEqual(proc.read_psw(), 0b10000000) # unchanged

    # bt 0fe20h.7,$label18        ;fc 20 fd       saddr
    def test_fc_bt_saddr_bit7_doesnt_branch_if_clear(self):
        proc = Processor()
        code = [0xfc, 0x20, 0x30]
        proc.write_memory(0, code)
        proc.memory[0xfe20] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code)) # branch not taken
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # movw ax,#0abcdh             ;10 cd ab
    def test_10_movw_ax_imm16(self):
        proc = Processor()
        code = [0x10, 0xcd, 0xab]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.AX, 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_regpair(RegisterPairs.AX), 0xabcd)
        self.assertEqual(proc.read_gp_reg(Registers.X), 0xcd)
        self.assertEqual(proc.read_gp_reg(Registers.A), 0xab)

    # movw bc,#0abcdh             ;12 cd ab
    def test_12_movw_bc_imm16(self):
        proc = Processor()
        code = [0x12, 0xcd, 0xab]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.BC, 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_regpair(RegisterPairs.BC), 0xabcd)
        self.assertEqual(proc.read_gp_reg(Registers.C), 0xcd)
        self.assertEqual(proc.read_gp_reg(Registers.B), 0xab)

    # movw de,#0abcdh             ;14 cd ab
    def test_14_movw_de_imm16(self):
        proc = Processor()
        code = [0x14, 0xcd, 0xab]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.DE, 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_regpair(RegisterPairs.DE), 0xabcd)
        self.assertEqual(proc.read_gp_reg(Registers.E), 0xcd)
        self.assertEqual(proc.read_gp_reg(Registers.D), 0xab)

    # movw hl,#0abcdh             ;16 cd ab
    def test_16_movw_hl_imm16(self):
        proc = Processor()
        code = [0x16, 0xcd, 0xab]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_regpair(RegisterPairs.HL), 0xabcd)
        self.assertEqual(proc.read_gp_reg(Registers.L), 0xcd)
        self.assertEqual(proc.read_gp_reg(Registers.H), 0xab)

    # xchw ax,bc                  ;e2
    def test_e2_xchw_ax_bc(self):
        proc = Processor()
        code = [0xe2]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.AX, 0x12)
        proc.write_gp_regpair(RegisterPairs.BC, 0x34)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_regpair(RegisterPairs.AX), 0x34)
        self.assertEqual(proc.read_gp_regpair(RegisterPairs.BC), 0x12)

    # xchw ax,de                  ;e4
    def test_e4_xchw_ax_de(self):
        proc = Processor()
        code = [0xe4]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.AX, 0x12)
        proc.write_gp_regpair(RegisterPairs.DE, 0x34)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_regpair(RegisterPairs.AX), 0x34)
        self.assertEqual(proc.read_gp_regpair(RegisterPairs.DE), 0x12)

    # xchw ax,hl                  ;e6
    def test_e6_xchw_ax_hl(self):
        proc = Processor()
        code = [0xe6]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.AX, 0x12)
        proc.write_gp_regpair(RegisterPairs.HL, 0x34)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_regpair(RegisterPairs.AX), 0x34)
        self.assertEqual(proc.read_gp_regpair(RegisterPairs.HL), 0x12)

    # mov a,[de]                  ;85
    def test_85_mov_a_de(self):
        proc = Processor()
        code = [0x85]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0)
        proc.write_gp_regpair(RegisterPairs.DE, 0xabcd)
        proc.memory[0xabcd] = 0x42
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0x42)

    # mov [de],a                  ;95
    def test_95_mov_de_a(self):
        proc = Processor()
        code = [0x95]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0x42)
        proc.write_gp_regpair(RegisterPairs.DE, 0xabcd)
        proc.memory[0xabcd] = 0
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0x42)

    # mov a,[hl]                  ;87
    def test_87_mov_a_hl(self):
        proc = Processor()
        code = [0x87]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0x42
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.read_gp_reg(Registers.A), 0x42)

    # mov [hl],a                  ;97
    def test_97_mov_hl_a(self):
        proc = Processor()
        code = [0x97]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0x42)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0x42)

    # xch a,[de]                  ;05
    def test_05_xch_a_de(self):
        proc = Processor()
        code = [0x05]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0x12)
        proc.write_gp_regpair(RegisterPairs.DE, 0xabcd)
        proc.memory[0xabcd] = 0x34
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0x12)
        self.assertEqual(proc.read_gp_reg(Registers.A), 0x34)

    # xch a,[hl]                  ;07
    def test_07_xch_a_hl(self):
        proc = Processor()
        code = [0x07]
        proc.write_memory(0, code)
        proc.write_gp_reg(Registers.A, 0x12)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0x34
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0x12)
        self.assertEqual(proc.read_gp_reg(Registers.A), 0x34)

    # push ax                     ;b1
    def test_b1_push_ax(self):
        proc = Processor()
        code = [0xb1]
        proc.write_memory(0, code)
        proc.sp = 0xfe12
        proc.write_gp_regpair(RegisterPairs.AX, 0xabcd)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.sp, 0xfe10)
        self.assertEqual(proc.memory[0xfe11], 0xab) # A
        self.assertEqual(proc.memory[0xfe10], 0xcd) # X

    # push bc                     ;b3
    def test_b3_push_bc(self):
        proc = Processor()
        code = [0xb3]
        proc.write_memory(0, code)
        proc.sp = 0xfe12
        proc.write_gp_regpair(RegisterPairs.BC, 0xabcd)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.sp, 0xfe10)
        self.assertEqual(proc.memory[0xfe11], 0xab) # B
        self.assertEqual(proc.memory[0xfe10], 0xcd) # C

    # push de                     ;b5
    def test_b5_push_de(self):
        proc = Processor()
        code = [0xb5]
        proc.write_memory(0, code)
        proc.sp = 0xfe12
        proc.write_gp_regpair(RegisterPairs.DE, 0xabcd)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.sp, 0xfe10)
        self.assertEqual(proc.memory[0xfe11], 0xab) # D
        self.assertEqual(proc.memory[0xfe10], 0xcd) # E

    # push hl                     ;b7
    def test_b7_push_de(self):
        proc = Processor()
        code = [0xb7]
        proc.write_memory(0, code)
        proc.sp = 0xfe12
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.sp, 0xfe10)
        self.assertEqual(proc.memory[0xfe11], 0xab) # H
        self.assertEqual(proc.memory[0xfe10], 0xcd) # L

    # pop ax                      ;b0
    def test_b0_pop_ax(self):
        proc = Processor()
        code = [0xb0]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.AX, 0)
        proc.sp = 0xfe10
        proc.memory[0xfe11] = 0xab # A
        proc.memory[0xfe10] = 0xcd # X
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.sp, 0xfe12)
        self.assertEqual(proc.read_gp_regpair(RegisterPairs.AX), 0xabcd)

    # pop bc                      ;b2
    def test_b2_pop_bc(self):
        proc = Processor()
        code = [0xb2]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.BC, 0)
        proc.sp = 0xfe10
        proc.memory[0xfe11] = 0xab # A
        proc.memory[0xfe10] = 0xcd # X
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.sp, 0xfe12)
        self.assertEqual(proc.read_gp_regpair(RegisterPairs.BC), 0xabcd)

    # pop de                      ;b4
    def test_b4_pop_de(self):
        proc = Processor()
        code = [0xb4]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.DE, 0)
        proc.sp = 0xfe10
        proc.memory[0xfe11] = 0xab # A
        proc.memory[0xfe10] = 0xcd # X
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.sp, 0xfe12)
        self.assertEqual(proc.read_gp_regpair(RegisterPairs.DE), 0xabcd)

    # pop hl                      ;b6
    def test_b4_pop_hl(self):
        proc = Processor()
        code = [0xb6]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0)
        proc.sp = 0xfe10
        proc.memory[0xfe11] = 0xab # A
        proc.memory[0xfe10] = 0xcd # X
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.sp, 0xfe12)
        self.assertEqual(proc.read_gp_regpair(RegisterPairs.HL), 0xabcd)

    # reti                        ;8f
    def test_8f_reti(self):
        proc = Processor()
        code = [0x8f]
        proc.write_memory(0, code)
        proc.sp = 0xfe10
        proc.memory[0xfe12] = 0x55 # psw
        proc.memory[0xfe11] = 0xab # pch
        proc.memory[0xfe10] = 0xcd # pcl
        proc.step()
        self.assertEqual(proc.pc, 0xabcd)
        self.assertEqual(proc.read_psw(), 0x55)
        self.assertEqual(proc.sp, 0xfe13)

    # set1 [hl].0                 ;71 82
    def test_71_82_set1_hl_bit_0(self):
        proc = Processor()
        code = [0x71, 0x82]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0b00000001)
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # set1 [hl].1                 ;71 92
    def test_71_92_set1_hl_bit_1(self):
        proc = Processor()
        code = [0x71, 0x92]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0b00000010)
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # set1 [hl].2                 ;71 a2
    def test_71_a2_set1_hl_bit_2(self):
        proc = Processor()
        code = [0x71, 0xa2]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0b00000100)
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # set1 [hl].3                 ;71 b2
    def test_71_b2_set1_hl_bit_3(self):
        proc = Processor()
        code = [0x71, 0xb2]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0b00001000)
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # set1 [hl].4                 ;71 c2
    def test_71_c2_set1_hl_bit_4(self):
        proc = Processor()
        code = [0x71, 0xc2]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0b00010000)
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # set1 [hl].5                 ;71 d2
    def test_71_d2_set1_hl_bit_5(self):
        proc = Processor()
        code = [0x71, 0xd2]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0b00100000)
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # set1 [hl].6                 ;71 e2
    def test_71_e2_set1_hl_bit_6(self):
        proc = Processor()
        code = [0x71, 0xe2]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0b01000000)
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # set1 [hl].7                 ;71 f2
    def test_71_f2_set1_hl_bit_7(self):
        proc = Processor()
        code = [0x71, 0xf2]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0b10000000)
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # clr1 [hl].0                 ;71 83
    def test_71_83_clr1_hl_bit_0(self):
        proc = Processor()
        code = [0x71, 0x83]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0b11111111
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0b11111110)
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # clr1 [hl].1                 ;71 93
    def test_71_93_clr1_hl_bit_1(self):
        proc = Processor()
        code = [0x71, 0x93]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0b11111111
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0b11111101)
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # clr1 [hl].2                 ;71 a3
    def test_71_a3_clr1_hl_bit_2(self):
        proc = Processor()
        code = [0x71, 0xa3]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0b11111111
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0b11111011)
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # clr1 [hl].3                 ;71 b3
    def test_71_b3_clr1_hl_bit_3(self):
        proc = Processor()
        code = [0x71, 0xb3]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0b11111111
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0b11110111)
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # clr1 [hl].4                 ;71 c3
    def test_71_c3_clr1_hl_bit_4(self):
        proc = Processor()
        code = [0x71, 0xc3]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0b11111111
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0b11101111)
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # clr1 [hl].5                 ;71 d3
    def test_71_d3_clr1_hl_bit_5(self):
        proc = Processor()
        code = [0x71, 0xd3]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0b11111111
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0b11011111)
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # clr1 [hl].6                 ;71 e3
    def test_71_e3_clr1_hl_bit_6(self):
        proc = Processor()
        code = [0x71, 0xe3]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0b11111111
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0b10111111)
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # clr1 [hl].7                 ;71 f3
    def test_71_f3_clr1_hl_bit_7(self):
        proc = Processor()
        code = [0x71, 0xf3]
        proc.write_memory(0, code)
        proc.write_gp_regpair(RegisterPairs.HL, 0xabcd)
        proc.memory[0xabcd] = 0b11111111
        proc.write_psw(0x55)
        proc.step()
        self.assertEqual(proc.pc, len(code))
        self.assertEqual(proc.memory[0xabcd], 0b01111111)
        self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # incw ax                     ;80
    def test_80_incw_ax(self):
        tests = ((0, 1), (0xff, 0x100), (0xffff, 0))
        for before, after in tests:
            proc = Processor()
            code = [0x80]
            proc.write_memory(0, code)
            proc.write_gp_regpair(RegisterPairs.AX, before)
            proc.write_psw(0x55)
            proc.step()
            self.assertEqual(proc.pc, len(code))
            self.assertEqual(proc.read_gp_regpair(RegisterPairs.AX), after)
            self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # incw bc                     ;82
    def test_82_incw_bc(self):
        tests = ((0, 1), (0xff, 0x100), (0xffff, 0))
        for before, after in tests:
            proc = Processor()
            code = [0x82]
            proc.write_memory(0, code)
            proc.write_gp_regpair(RegisterPairs.BC, before)
            proc.write_psw(0x55)
            proc.step()
            self.assertEqual(proc.pc, len(code))
            self.assertEqual(proc.read_gp_regpair(RegisterPairs.BC), after)
            self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # incw de                     ;84
    def test_84_incw_bc(self):
        tests = ((0, 1), (0xff, 0x100), (0xffff, 0))
        for before, after in tests:
            proc = Processor()
            code = [0x84]
            proc.write_memory(0, code)
            proc.write_gp_regpair(RegisterPairs.DE, before)
            proc.write_psw(0x55)
            proc.step()
            self.assertEqual(proc.pc, len(code))
            self.assertEqual(proc.read_gp_regpair(RegisterPairs.DE), after)
            self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # incw hl                     ;86
    def test_86_incw_bc(self):
        tests = ((0, 1), (0xff, 0x100), (0xffff, 0))
        for before, after in tests:
            proc = Processor()
            code = [0x86]
            proc.write_memory(0, code)
            proc.write_gp_regpair(RegisterPairs.HL, before)
            proc.write_psw(0x55)
            proc.step()
            self.assertEqual(proc.pc, len(code))
            self.assertEqual(proc.read_gp_regpair(RegisterPairs.HL), after)
            self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # decw ax                     ;90
    def test_90_decw_ax(self):
        tests = ((1, 0), (0x100, 0xff), (0, 0xffff))
        for before, after in tests:
            proc = Processor()
            code = [0x90]
            proc.write_memory(0, code)
            proc.write_gp_regpair(RegisterPairs.AX, before)
            proc.write_psw(0x55)
            proc.step()
            self.assertEqual(proc.pc, len(code))
            self.assertEqual(proc.read_gp_regpair(RegisterPairs.AX), after)
            self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # decw bc                     ;92
    def test_92_decw_bc(self):
        tests = ((1, 0), (0x100, 0xff), (0, 0xffff))
        for before, after in tests:
            proc = Processor()
            code = [0x92]
            proc.write_memory(0, code)
            proc.write_gp_regpair(RegisterPairs.BC, before)
            proc.write_psw(0x55)
            proc.step()
            self.assertEqual(proc.pc, len(code))
            self.assertEqual(proc.read_gp_regpair(RegisterPairs.BC), after)
            self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # decw de                     ;94
    def test_92_decw_de(self):
        tests = ((1, 0), (0x100, 0xff), (0, 0xffff))
        for before, after in tests:
            proc = Processor()
            code = [0x94]
            proc.write_memory(0, code)
            proc.write_gp_regpair(RegisterPairs.DE, before)
            proc.write_psw(0x55)
            proc.step()
            self.assertEqual(proc.pc, len(code))
            self.assertEqual(proc.read_gp_regpair(RegisterPairs.DE), after)
            self.assertEqual(proc.read_psw(), 0x55) # unchanged

    # decw hl                     ;96
    def test_92_decw_hl(self):
        tests = ((1, 0), (0x100, 0xff), (0, 0xffff))
        for before, after in tests:
            proc = Processor()
            code = [0x96]
            proc.write_memory(0, code)
            proc.write_gp_regpair(RegisterPairs.HL, before)
            proc.write_psw(0x55)
            proc.step()
            self.assertEqual(proc.pc, len(code))
            self.assertEqual(proc.read_gp_regpair(RegisterPairs.HL), after)
            self.assertEqual(proc.read_psw(), 0x55) # unchanged


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

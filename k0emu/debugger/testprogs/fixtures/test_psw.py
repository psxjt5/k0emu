import sys
from k0emu.debug import make_debugger_from_argv

def test(debug, outfile):
    for psw in range(0x80):
        code = [
            0x11, 0x1e, psw,    # mov psw,#<psw>
            0xf0, 0x1e,         # mov a,psw
            0x9e, 0x00, 0xfe,   # mov 0xfe00,a
            0xf0, 0x1e,         # mov a,0xff1e
            0x9e, 0x01, 0xfe,   # mov 0xfe01,a
            0xaf,               # ret
        ]
        debug.write(0xf000, code)
        debug.call(0xf000)
        psw, ff1e = debug.read(0xfe00, length=2)

        fmt = "PSW(OUT)=%02x, FF1E(OUT)=%02x\n"
        outfile.write(fmt % (psw, ff1e))
        outfile.flush()

def main():
    debug = make_debugger_from_argv()
    test(debug, sys.stdout)

if __name__ == '__main__':
    main()

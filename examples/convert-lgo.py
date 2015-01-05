# cut and paste 9x9 puzzles from www.logicgamesonline.com into this
# and get ASCII output puzzles
import sys
lines = sys.stdin.read().split('\n')
for l in lines:
    row = l.split('\t')
    if len(row) == 9:
        outrow = ''
        for cell in row:
            if cell==' ':
                outrow += '.'
            else:
                outrow += cell
        print outrow



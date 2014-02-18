Bimport sys
from subprocess import call

out = ["a2ps", "--center-title=472:%s Hardy, Wood"%sys.argv[1], "-qr2gC", "-o", sys.argv[1]]
for x in sys.argv[2:]:
	out.append("%s" %x)
call(out)
call(["ps2pdf", sys.argv[1]])

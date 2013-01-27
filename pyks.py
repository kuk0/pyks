# -*- coding: utf-8 -*-
from pyx import *
from cmath import *

text.preamble(r"""
\parindent=0pt\
%\let\phi\varphi 
\font\fivebf =cmbx10  scaled 500 
\font\sevenbf=cmbx10  scaled 700 
\font\tenbf  =cmbx10             
\font\fivemb =cmmib10 scaled 500 
\font\sevenmb=cmmib10 scaled 700 
\font\tenmb  =cmmib10            
\def\boldmath{\textfont0=\tenbf           \scriptfont0=\sevenbf 
              \scriptscriptfont0=\fivebf  \textfont1=\tenmb
              \scriptfont1=\sevenmb       \scriptscriptfont1=\fivemb}
""")
C=canvas.canvas()
u=1; v=1; addr=""

cc = C
current_pos = 0j

def setuv(uu,vv): global u,v; u=uu; v=vv;
def setwdir(wdir):
  global addr
  addr = wdir
  if addr[-1] != '/': addr = addr+'/'

# COLORS

def grey(p):
  return color.grey(p*0.01)

BLACK = grey(0)
WHITE = grey(100)
current_color = BLACK

def setcolor(c = BLACK):
  global current_color
  current_color= c

# CANVAS

def setcanvas(canvas = None):
  global cc;
  if canvas == None: cc = C
  else: cc = canvas

def newcanvas():
  global cc;
  cc = canvas.canvas()
  return cc

def cpaste(z=0j, a=0, f=1.0, c = None):
  global cc, u, v, C;
  z = complex(z)
  if c == None: C.insert (cc, [trafo.scale (f), trafo.rotate (a), trafo.translate (z.real*u, z.imag*v)])
  else: c.insert (cc, [trafo.scale (f), trafo.rotate (a), trafo.translate (z.real*u, z.imag*v)])

def paste(z=0j, a=0, f=1.0, c = None):
  global cc, C; 
  cpaste (z, a, f, c);
  if c == None: cc = C
  else: cc = c

def tpaste(t, z=0j, a=0, f=1.0, c = None):
  global cc, u, v, C;
  z = complex(z)
  if c == None: C.insert (cc, [t, trafo.scale (f), trafo.rotate (a), trafo.translate (z.real*u, z.imag*v)])
  else: c.insert (cc, [t, trafo.scale (f), trafo.rotate (a), trafo.translate (z.real*u, z.imag*v)])
  if c == None: cc = C
  else: cc = c

def new(): global C, cc; C = cc = canvas.canvas();
def newa(x,y,xt="$x$",yt="$y$"): new(); axes(-x,-y,x,y,xt,yt);
def newp(x,y,xt="",yt=""): new(); plainaxes(-x,-y,x,y,xt,yt);
def newpa(x,y,xt="$x$",yt="$y$"): new(); axes(0,0,x,y,xt,yt);
def newpp(x,y,xt="",yt=""): new(); plainaxes(0,0,x,y,xt,yt);
def newc(x,y): new(); axes(-x,-y,x,y,r"$\Re$",r"$\Im$");

output_format = "pdf"
def set_output_format(f="pdf"):
  global output_format
  assert f in ["pdf", "ps", "eps"]
  output_format = f

def save(f):
  global C, addr, output_format
  if output_format == "eps":
    C.writeEPSfile(addr+f)
  else:
    C.writePDFfile(addr+f)

def circ(z, r=0.06, fill=WHITE, attr=[]):
  global cc, u, v, current_color;
  try:
    for w in z: circ(w, r, fill, attr)
  except TypeError:
    z = complex(z)
    cc.draw(path.circle(u*z.real,v*z.imag,r*u), [current_color] + attr + [deco.stroked(), deco.filled([fill])])
def dot(z, r=0.06, attr=[]): circ(z, r, current_color, attr)
def bdot(z, r=0.09, attr=[]): dot(z, r, attr)
def node(z, r, t="", fill=WHITE, attr=[]): circ(z, r, fill, attr); label(z,t)

# styl - 0, 1, 2 = solid, dashed, dotted
st = [style.linestyle.solid, style.linestyle.dashed, style.linestyle.dotted]
SOLID = style.linestyle.solid
DASHED = style.linestyle.dashed
DOTTED = style.linestyle.dotted
BOLD = style.linewidth(0.05)


# line(z,w,s) kde z, w su komplexne cisla, nakresli ciaru od z ku w stylom s
# r- relative, b- bold
# arrow(z,w,s) to iste, ale sipka; arrow2 je obojstranna sipka
def line (z, w=0j, attr=[]):
  global cc, u, v, current_color
  try:
    for pz in z: line(pz, w, attr)
  except TypeError:
    try:
      for pw in w: line(z, pw, attr)
    except TypeError:
      z = complex(z); w = complex(w)
      cc.stroke (path.line(u*z.real, v*z.imag, u*w.real, v*w.imag), [current_color] + attr)
def lines (z, w, attr=[]):
  for pz, wz in zip(z, w): line(pz, wz, attr)
def bline (z, w=0j, attr=[]): line (z, w, attr + [BOLD])
def rline (z, w, attr=[]): line (z, z+w, attr)
def rbline (z, w, attr=[]): bline (z, z+w, attr)
def moveto (z):
  global current_pos
  current_pos = complex(z)
def lineto (z, attr=[]):
  global current_pos
  z = complex(z)
  line (current_pos, z, attr)
  current_pos = z
def blineto (z, attr=[]): lineto (z, attr + [BOLD])
def arrow(z, w, attr=[]):
  if abs(z - w) < 1e-10: return
  line(z, w, attr + [deco.earrow.normal])
def arrow2(z, w=0j, attr=[]):
  if abs(z - w) < 1e-10: return
  line(z, w, attr + [deco.earrow.normal, deco.barrow.normal])
def barrow(z, w, attr=[]): arrow (z, w, attr + [BOLD])
def barrow2(z, w=0j, attr=[]): arrow2 (z, w, attr + [BOLD])

# label(z,t) - text t na poziciu z; t/b/l/r top/bottom/left/right + kombinacie
def label(z,t): global cc,u,v; cc.text(u*z.real,v*z.imag,t,[text.halign.boxcenter,text.valign.middle]);
def labelt(z,t): global cc,u,v; cc.text(u*z.real,v*z.imag+.25,t,[text.halign.boxcenter,text.valign.baseline]);
def labelb(z,t): global cc,u,v; cc.text(u*z.real,v*z.imag-.4,t,[text.halign.boxcenter,text.valign.baseline]);
def labell(z,t): global cc,u,v; cc.text(u*z.real-.25,v*z.imag,t,[text.halign.boxright,text.valign.middle]);
def labelr(z,t): global cc,u,v; cc.text(u*z.real+.25,v*z.imag,t,[text.halign.boxleft,text.valign.middle]);
def labeltr(z,t): global cc,u,v; cc.text(u*z.real+.2,v*z.imag+.2,t,[text.halign.boxleft,text.valign.bottom]);
def labeltl(z,t): global cc,u,v; cc.text(u*z.real-.2,v*z.imag+.2,t,[text.halign.boxright,text.valign.bottom]);
def labelbr(z,t): global cc,u,v; cc.text(u*z.real+.2,v*z.imag-.2,t,[text.halign.boxleft,text.valign.top]);
def labelbl(z,t): global cc,u,v; cc.text(u*z.real-.2,v*z.imag-.2,t,[text.halign.boxright,text.valign.top]);
def labela(w, a, t): # TODO: rozsirit uhly a upravit tie vzdialenosti
  while a < 0: a += 360
  while a > 360: a -= 360
  if a > 315 or a < 45:
    labelr(w,t)
  elif 45 <= a < 135:
    labelt(w,t)
  elif 135 <= a < 215:
    labell(w,t)
  else:
    labelb(w,t)

def rect(z, w, attr=[]): rrect(z, w-z, attr);
def rrect(z, w, attr): global cc,u,v; cc.stroke(path.rect(u*z.real,v*z.imag,u*w.real,v*w.imag), attr)
def brect(z, w, attr=[]): rect(z, w, attr + [BOLD])
def block(z, w, fill=[WHITE], t="", attr=[]): rblock(z, w-z, fill, t, attr)
def rblock(z, w, fill=[WHITE], t="", attr=[]):
  global cc, u, v, current_color
  cc.draw(path.rect(u*z.real,v*z.imag,u*w.real,v*w.imag), [current_color] + attr + [deco.stroked(), deco.filled(fill)])
  label(z+w/2, t)

def circle(z, r, attr=[]): ellipse(z, r*(1+1j), attr)
def ellipse (z, r, attr=[]):
  global cc, u, v, current_color;
  z, r = complex(z), complex(r)
  cc.stroke(path.circle(u*z.real,v*z.imag, 1), [current_color] + attr + [trafo.scale(sx=r.real*u, sy=r.imag*v)])

def poly(p, fill=None, closed=True, attr=[]):
  global cc, u, v, current_color
  l = path.path(path.moveto(u*p[0].real,v*p[0].imag))
  for pt in p[1:]:
    l.append(path.lineto(u*pt.real,v*pt.imag))
  if closed: l.append(path.closepath())
  cc.draw(l, [current_color] + attr + [deco.stroked(), deco.filled(fill)])
def rpoly(r, fill=None, closed=True, attr=[]):
  p[0] = r[0]
  for w in r[1:]: p.append(p[-1] + w)
  poly(p, fill, closed, attr)

def angle(z, r, a1, a2, attr=[]):
  global cc, u, current_color;
  cc.stroke(path.path(path.arc(u*z.real,v*z.imag,r*u,a1,a2)), [current_color] + attr);

def aarrow(z, r, a1, a2, attr=[]): #TODO: toto nejak lepsie
  global cc, u, current_color;
  cc.stroke(path.path(path.arc(u*z.real,v*z.imag,r*u,a1,a2)), [current_color] + attr + [deco.earrow.normal])

def plainaxes(x1,y1,x2,y2,xt="", yt=""):
  global cc, u, v
  arrow2(x1-.5+0j, x2+.5+0j); arrow2((y1-.5)*1j,(y2+.5)*1j)
  labelr(x2+0.5+0j,xt); labelt((y2+0.5)*1j,yt)

def axes(x1,y1,x2,y2,xt="$x$",yt="$y$"):
  global cc,u,v
  plainaxes(x1,y1,x2,y2,xt,yt)
  for i in xrange(x1,x2+1):
    cc.stroke(path.line(u*i,0.1,u*i,-0.1))
    if i==0: cc.text(u*i-.1,-.4,r"0",[text.halign.boxright]);
    else: cc.text(u*i,-.4,str(i),[text.halign.boxcenter]);
  for i in xrange(y1,y2+1):
    cc.stroke(path.line(-0.1,u*i,0.1,u*i))
    if i!=0:
      if i==1: cc.text(-.25,u,"$i$",[text.halign.boxright,text.valign.middle]);
      elif i==-1: cc.text(-.25,-u,"$-i$",[text.halign.boxright,text.valign.middle]);
      else: cc.text(-.25, u*i,"$"+str(i)+"i$",[text.halign.boxright,text.valign.middle]);

def curve(w, x, y, z, attr=[]):
  global cc, u, v, current_color
  cc.stroke (path.curve (u*w.real, v*w.imag, u*x.real, v*x.imag, u*y.real, v*y.imag, u*z.real, v*z.imag),
             [current_color] + attr)
def bcurve(w, x, y, z, attr=[]): curve (w, x, y, z, attr + [BOLD])
def carrow(w, x, y, z, attr=[]):
  global cc, u, v, current_color
  cc.stroke (path.curve (u*w.real, v*w.imag, u*x.real, v*x.imag, u*y.real, v*y.imag, u*z.real, v*z.imag),
             [current_color] + attr + [deco.earrow.normal])
def carrow2(w, x, y, z, attr=[]):
  global cc, u, v, current_color
  cc.stroke (path.curve (u*w.real, v*w.imag, u*x.real, v*x.imag, u*y.real, v*y.imag, u*z.real, v*z.imag),
             [current_color] + attr + [deco.earrow.normal, deco.barrow.normal])

def vlnka(w, z, d = 0.2, r = 0.1, sf = 0, sl = 0, s = 0, col = None, lw = 0.02, attr=[]):
  line(z, w, s, col, lw, attr + [deformer.cycloid(radius = r, halfloops = int((abs(w-z)-sf-sl)/d), skipfirst = sf, skiplast = sl, sign = 1, turnangle = 0)])

def cis(a): return exp((1j/180.0*pi)*a)

def frange(a, b, incr):
  if a <= b:
    if incr <= 0: return
    while a < b:
      yield a
      a += incr
  else:
    if incr >= 0: return
    while a > b:
      yield a
      a += incr

# point m such that am : mb = da : db
# e.g. mid(a,b) is in the middle of a, b
#      mid(a,b,2,1) is m 2/3 way from a to b (am : mb = 2 : 1)
def mid(a, b, da=1, db=1):
  return (a*db + b*da)/float(da+db)

def czip(x, y):
  return [u+1j*v for u,v in zip(x,y)]

def ptsdir(z, d, n): # n points starting from z in direction d
  p = [z]
  for i in xrange(0,n-1):
    p.append(p[-1]+d)
  return p

def nrange(w, z, n, bincl=True, eincl=True):
  if n <= 0: return
  if not bincl and not eincl:
    w, z = w + (z-w)/float(n+1), z + (w-z)/float(n+1)
  elif not bincl:
    w += (z-w)/float(n)
  elif not eincl:
    z += (w-z)/float(n)
  if n == 1:
    yield w
    return
  for i in xrange(0,n):
    yield w + (z-w)*(i/float(n-1))

def ptsline(w, z, n, bincl=True, eincl=True): # n points from w to z
  return [p for p in nrange(w, z, n, bincl, eincl)]

def ptscirc(z, r, n, bangle = 0, eangle = 360, bincl=True, eincl=False):
  return [z + r*cis(a) for a in nrange(bangle, eangle, n, bincl, eincl)]

def jpeg(f,x=0,y=0):
  c = newcanvas()
  i = bitmap.jpegimage(f)
  c.insert(bitmap.bitmap(x,y,i,compressmode=None))
  return c

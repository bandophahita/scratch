#!/usr/bin/env python3
from __future__ import annotations

INPUT = """
$ cd /
$ ls
dir cmwrq
dir ftrccld
dir jjlbmtw
dir jpncfpb
dir mddr
dir mthvntdd
55644 pjts.dzh
dir ptzsl
dir wmqc
$ cd cmwrq
$ ls
dir dtbzzl
dir pjnghbm
16144 rvs
50956 swngfrsj.pcj
dir vhvn
dir vrt
dir zgrjmtcq
$ cd dtbzzl
$ ls
42503 ljhpmvd.zqf
dir wwpnn
$ cd wwpnn
$ ls
58541 jjdgzwnq
dir lwqgsbg
dir nztw
dir rdtjztmt
101609 sqqpcvq.llm
dir ssdlqcrw
$ cd lwqgsbg
$ ls
207528 cpqhb.jsf
38543 cqjgspw
dir dtbzzl
106337 dtbzzl.njz
302201 pdv.ppg
dir pjts
175215 pvczm.cfw
dir sbvljdh
$ cd dtbzzl
$ ls
252091 vhvn.zqv
$ cd ..
$ cd pjts
$ ls
155681 bdbfjbgt.rwg
219192 dtcz.gqt
$ cd ..
$ cd sbvljdh
$ ls
dir rdrqc
dir rtfpcswj
$ cd rdrqc
$ ls
242263 pjts.mbt
$ cd ..
$ cd rtfpcswj
$ ls
228044 ssgcjt.twr
$ cd ..
$ cd ..
$ cd ..
$ cd nztw
$ ls
30777 vqfsh.smp
$ cd ..
$ cd rdtjztmt
$ ls
276602 pvczm.cfw
dir rzbb
305089 ssdlqcrw.dgb
$ cd rzbb
$ ls
155253 pvczm.cfw
$ cd ..
$ cd ..
$ cd ssdlqcrw
$ ls
22423 vqfsh.smp
$ cd ..
$ cd ..
$ cd ..
$ cd pjnghbm
$ ls
189296 ctqfg.ljd
dir dtbzzl
dir pjts
205394 ssdlqcrw.lgv
$ cd dtbzzl
$ ls
239152 fbb.gtn
dir hlw
39308 hsnbffzf.qvc
211316 nhm.zhz
dir nztw
dir pvsjpn
230237 twjq
$ cd hlw
$ ls
dir lfqqrp
dir nztw
$ cd lfqqrp
$ ls
dir mbmfpz
dir mdhfdlw
dir pjts
dir qzs
dir ssdlqcrw
$ cd mbmfpz
$ ls
dir fsrbwl
dir lsmpw
$ cd fsrbwl
$ ls
154657 ftlc.zbr
dir ltsj
228929 pvczm.cfw
dir ssdlqcrw
234216 tdl
$ cd ltsj
$ ls
51204 vmq.sjg
$ cd ..
$ cd ssdlqcrw
$ ls
64928 nztw.gpn
$ cd ..
$ cd ..
$ cd lsmpw
$ ls
61867 dtbzzl.dgj
$ cd ..
$ cd ..
$ cd mdhfdlw
$ ls
92462 dtbzzl.jmq
239442 tczcgf.zwj
$ cd ..
$ cd pjts
$ ls
144464 dtbzzl.lnz
dir pjts
118500 swgt.smz
$ cd pjts
$ ls
173783 dvztnn
103088 jlv.pgh
39332 nhm.zhz
266947 pppfcg
$ cd ..
$ cd ..
$ cd qzs
$ ls
11155 cpqhb.jsf
$ cd ..
$ cd ssdlqcrw
$ ls
192414 gcwqcwrf.vmb
$ cd ..
$ cd ..
$ cd nztw
$ ls
313009 nwt
$ cd ..
$ cd ..
$ cd nztw
$ ls
280535 dtbzzl.grj
269725 ssdlqcrw.tqs
$ cd ..
$ cd pvsjpn
$ ls
105150 jvjb.mdd
142501 nztw.cvp
$ cd ..
$ cd ..
$ cd pjts
$ ls
dir btc
dir tpwcmvch
259357 vqfsh.smp
$ cd btc
$ ls
5264 gdjpql.wqr
$ cd ..
$ cd tpwcmvch
$ ls
141657 jjdgzwnq
15650 nhm.zhz
dir nlrq
182100 qgf.qgj
302332 qshf
244799 vhvn
dir wvnqzjf
$ cd nlrq
$ ls
dir dtbzzl
207207 gnd.vmb
$ cd dtbzzl
$ ls
271143 wjbzmc
$ cd ..
$ cd ..
$ cd wvnqzjf
$ ls
64128 mtzc.rqb
$ cd ..
$ cd ..
$ cd ..
$ cd ..
$ cd vhvn
$ ls
187526 vqfsh.smp
$ cd ..
$ cd vrt
$ ls
dir drrnm
dir fqr
270995 nztw.mfg
137476 vqfsh.smp
$ cd drrnm
$ ls
250912 pvczm.cfw
$ cd ..
$ cd fqr
$ ls
229272 nszfcq
dir nztw
170643 phh.pdl
$ cd nztw
$ ls
dir bqf
$ cd bqf
$ ls
9998 vqfsh.smp
$ cd ..
$ cd ..
$ cd ..
$ cd ..
$ cd zgrjmtcq
$ ls
109025 vhvn
$ cd ..
$ cd ..
$ cd ftrccld
$ ls
dir dtbzzl
dir fvmh
dir fwztt
22306 jngjc.mpd
190320 lnr.jhn
dir lsvvn
295676 nztw
135025 nztw.ssc
dir pjts
dir qglhlggq
dir rslphgp
247764 ssdlqcrw.jnm
dir vhvn
$ cd dtbzzl
$ ls
dir fgwh
$ cd fgwh
$ ls
dir dpdvswq
$ cd dpdvswq
$ ls
dir jsstq
248465 vhvn
$ cd jsstq
$ ls
252517 nztw
$ cd ..
$ cd ..
$ cd ..
$ cd ..
$ cd fvmh
$ ls
dir djcn
dir dtbzzl
303052 fbnnfsbp.zzg
77238 mdpcghq.nls
dir mvppnhr
238683 ptw
dir zdqlwnc
$ cd djcn
$ ls
8600 jjdgzwnq
$ cd ..
$ cd dtbzzl
$ ls
dir sppdjcm
dir vtnzqtvj
$ cd sppdjcm
$ ls
237925 dvfctpg.zbn
dir fghb
dir pfjdsm
dir pjts
314661 zfchfq
$ cd fghb
$ ls
280081 cpqhb.jsf
88448 wbcpnnvs.sjc
$ cd ..
$ cd pfjdsm
$ ls
256877 bssmgf
127978 drwttw
103674 hznr.hjg
$ cd ..
$ cd pjts
$ ls
191709 qhwwpzn.dsc
$ cd ..
$ cd ..
$ cd vtnzqtvj
$ ls
dir rrl
$ cd rrl
$ ls
281036 jjdgzwnq
dir lzlswv
dir sjsqnvq
245082 ssdlqcrw.smq
$ cd lzlswv
$ ls
dir dmh
$ cd dmh
$ ls
41234 hlhgn.mvr
233542 tgv.csn
$ cd ..
$ cd ..
$ cd sjsqnvq
$ ls
221327 qjncmbn
$ cd ..
$ cd ..
$ cd ..
$ cd ..
$ cd mvppnhr
$ ls
dir ldwv
176153 nztw
dir rmdjdqvl
dir tmj
dir vhvn
$ cd ldwv
$ ls
161179 mjsm
$ cd ..
$ cd rmdjdqvl
$ ls
dir gnztqmhv
dir lpmhfr
dir tphjm
$ cd gnztqmhv
$ ls
176043 qlds.mpq
$ cd ..
$ cd lpmhfr
$ ls
dir jrrdsd
$ cd jrrdsd
$ ls
114477 vqfsh.smp
$ cd ..
$ cd ..
$ cd tphjm
$ ls
74809 dcfmjn
$ cd ..
$ cd ..
$ cd tmj
$ ls
252001 cpqhb.jsf
49666 pqpq
139885 qpj.wpb
116339 vqfsh.smp
$ cd ..
$ cd vhvn
$ ls
89397 dtbzzl.hvp
105454 pvczm.cfw
280352 zdzm
$ cd ..
$ cd ..
$ cd zdqlwnc
$ ls
dir fbhcv
8676 jjdgzwnq
99885 nhm.zhz
234563 pjts.gdj
dir rsdltnvc
$ cd fbhcv
$ ls
71695 hrzzgwqt
296401 vqfsh.smp
$ cd ..
$ cd rsdltnvc
$ ls
41623 gcvtqf
233747 wdcssvgh.vfs
$ cd ..
$ cd ..
$ cd ..
$ cd fwztt
$ ls
96594 jjdgzwnq
245415 mtp.szl
129782 pjts.jjr
308104 pvczm.cfw
dir ssdlqcrw
155109 vhvn.smj
dir vvzsr
$ cd ssdlqcrw
$ ls
dir bzd
292228 dtbzzl.tdb
107505 ssdlqcrw
181384 tfnrpsd
$ cd bzd
$ ls
84648 brdc
171457 vhvn
$ cd ..
$ cd ..
$ cd vvzsr
$ ls
dir bcdqrs
147437 jjdgzwnq
dir ssdlqcrw
197054 ssdlqcrw.dpz
dir vhvn
dir wthshgg
$ cd bcdqrs
$ ls
297401 pspd.dlq
136072 pvczm.cfw
$ cd ..
$ cd ssdlqcrw
$ ls
293104 dtbzzl.pdh
$ cd ..
$ cd vhvn
$ ls
178932 gvrht.cbm
$ cd ..
$ cd wthshgg
$ ls
dir dppwvtmp
dir ljgszd
88822 pcmw.bbq
255776 pvczm.cfw
163501 ssdlqcrw
dir vbjsmgp
dir vzqc
dir zmpdrpd
$ cd dppwvtmp
$ ls
45608 dtbzzl.lfq
164648 gdch.bzp
65225 nhm.zhz
$ cd ..
$ cd ljgszd
$ ls
125627 vqfsh.smp
$ cd ..
$ cd vbjsmgp
$ ls
236951 zpbgb.zmv
$ cd ..
$ cd vzqc
$ ls
234565 fjfpbjjp
254986 jjdgzwnq
164495 nztw.qhz
dir vhvn
$ cd vhvn
$ ls
199196 nztw
$ cd ..
$ cd ..
$ cd zmpdrpd
$ ls
123210 bznqq.dbv
141163 jjdgzwnq
302352 wjf.tdv
92016 wljnwsh
$ cd ..
$ cd ..
$ cd ..
$ cd ..
$ cd lsvvn
$ ls
282867 phv.ncc
$ cd ..
$ cd pjts
$ ls
40866 jjdgzwnq
$ cd ..
$ cd qglhlggq
$ ls
19577 dtbzzl.ngb
21171 jjdgzwnq
136074 pvczm.cfw
212428 rlpjjf.lvh
dir vhvn
274669 wcqlws.ndv
dir wpvq
$ cd vhvn
$ ls
183301 cbppfp.vbc
84069 cqnz
dir dtbzzl
dir mdng
126627 pjts.pvp
dir ptqq
47594 pvczm.cfw
154978 qlnnfbvd
$ cd dtbzzl
$ ls
50385 ccgbrdmb.hrr
22427 rzlwl.jbt
$ cd ..
$ cd mdng
$ ls
dir gdqqtvnp
224013 gtv.tbz
121884 jjdgzwnq
dir nrmhpblm
142950 nztw
9710 pvczm.cfw
dir vhvn
$ cd gdqqtvnp
$ ls
292349 vhvn.nfr
$ cd ..
$ cd nrmhpblm
$ ls
52703 jbvd.mlc
78268 pfns.lpr
$ cd ..
$ cd vhvn
$ ls
274549 pjts
$ cd ..
$ cd ..
$ cd ptqq
$ ls
257967 jqppq.lgb
166450 nhm.zhz
$ cd ..
$ cd ..
$ cd wpvq
$ ls
173437 vqfsh.smp
$ cd ..
$ cd ..
$ cd rslphgp
$ ls
29192 pvczm.cfw
18984 ttpfnqvn.cdr
302301 vqfsh.smp
291211 vsvtc.wwf
$ cd ..
$ cd vhvn
$ ls
dir ssdlqcrw
$ cd ssdlqcrw
$ ls
76864 jpwvws.fwv
26365 nztw.css
185966 vqfsh.smp
$ cd ..
$ cd ..
$ cd ..
$ cd jjlbmtw
$ ls
211239 ctfhmm.ssv
230020 nztw
109641 sqtjn
$ cd ..
$ cd jpncfpb
$ ls
dir hjgwcmh
286054 pcffhsw.bdm
260831 pvczm.cfw
dir vhvn
$ cd hjgwcmh
$ ls
92277 bbjhc
dir fmst
dir gzjq
$ cd fmst
$ ls
105833 cpqhb.jsf
315858 nhm.zhz
233459 nztw
$ cd ..
$ cd gzjq
$ ls
dir prjqfwf
dir ssdlqcrw
$ cd prjqfwf
$ ls
151003 jnmgdb.rhn
$ cd ..
$ cd ssdlqcrw
$ ls
103688 cpqhb.jsf
$ cd ..
$ cd ..
$ cd ..
$ cd vhvn
$ ls
14901 cpqhb.jsf
98212 tztzq
$ cd ..
$ cd ..
$ cd mddr
$ ls
dir qpfjp
$ cd qpfjp
$ ls
dir cfhv
$ cd cfhv
$ ls
dir ssdlqcrw
$ cd ssdlqcrw
$ ls
134280 vvnpvrqb.hdv
$ cd ..
$ cd ..
$ cd ..
$ cd ..
$ cd mthvntdd
$ ls
dir bcdcz
dir cngbf
62389 cwtvl
dir mqjjbq
dir nhblb
6743 pvczm.cfw
dir ssdlqcrw
dir ttvgr
dir vdmm
dir wnhnwjm
dir zdvbsb
$ cd bcdcz
$ ls
213688 dtbzzl.hsv
dir lbvbc
100222 nndbhrf
115627 rqnsfbz.rmf
dir tvgclpsc
258672 vqfsh.smp
163927 whgmd
$ cd lbvbc
$ ls
224836 fpfpwtf.zfz
103806 nztw
$ cd ..
$ cd tvgclpsc
$ ls
76900 cpqhb.jsf
282820 qtffdmsg
$ cd ..
$ cd ..
$ cd cngbf
$ ls
dir hstph
12089 jqvnttq.dsh
38052 nztw.sqj
dir qrnpjz
$ cd hstph
$ ls
172788 pjts.qmt
$ cd ..
$ cd qrnpjz
$ ls
dir blzc
dir rvl
dir zvhtzqqc
$ cd blzc
$ ls
108342 nhm.zhz
$ cd ..
$ cd rvl
$ ls
dir bcrf
dir sjbr
$ cd bcrf
$ ls
182498 cpqhb.jsf
dir dcb
14228 ggsq
dir gnhvtgm
$ cd dcb
$ ls
dir zlgjzcjv
$ cd zlgjzcjv
$ ls
18316 cpqhb.jsf
$ cd ..
$ cd ..
$ cd gnhvtgm
$ ls
110236 nhm.zhz
$ cd ..
$ cd ..
$ cd sjbr
$ ls
133009 cscbp
315907 vtpmnwt
$ cd ..
$ cd ..
$ cd zvhtzqqc
$ ls
dir fglfpn
dir gtzrq
dir hfgdcf
274977 ltbzhjn
dir msc
dir ssdlqcrw
$ cd fglfpn
$ ls
39153 dvhjpfc
$ cd ..
$ cd gtzrq
$ ls
60625 sqljdlpz.wpw
$ cd ..
$ cd hfgdcf
$ ls
36016 qdvnn.pbt
$ cd ..
$ cd msc
$ ls
56601 cpqhb.jsf
dir hrz
dir vlhllqz
$ cd hrz
$ ls
241511 fhngt.mlb
286505 nhm.zhz
$ cd ..
$ cd vlhllqz
$ ls
157880 nhm.zhz
$ cd ..
$ cd ..
$ cd ssdlqcrw
$ ls
121507 dssrvr
295897 lvtwlb.whn
12047 pjts.gqc
$ cd ..
$ cd ..
$ cd ..
$ cd ..
$ cd mqjjbq
$ ls
157818 blbmb.fcv
119103 ccppbmqb.pbt
141463 cpqhb.jsf
197900 drhmws.fdd
dir fmvp
dir rhldnjlt
175029 vqfsh.smp
$ cd fmvp
$ ls
dir dhnn
dir dlcvwqw
131432 hnv.tlr
dir jzqt
98127 nhm.zhz
dir nvsdbjj
dir pjts
9179 pvczm.cfw
121310 vqfsh.smp
$ cd dhnn
$ ls
173921 qcjsdg.zfg
58654 vhvn.csb
$ cd ..
$ cd dlcvwqw
$ ls
285116 zjb
$ cd ..
$ cd jzqt
$ ls
104478 clmzwnf
299622 cpqhb.jsf
301236 jjdgzwnq
dir nsvlqq
136737 vhvn
dir vmp
12932 wrd.jsz
$ cd nsvlqq
$ ls
111712 dtbzzl.htn
213593 hvzlmtj.ztr
$ cd ..
$ cd vmp
$ ls
104275 jjdgzwnq
$ cd ..
$ cd ..
$ cd nvsdbjj
$ ls
180999 jjdgzwnq
219819 vhvn
$ cd ..
$ cd pjts
$ ls
111715 npzn
$ cd ..
$ cd ..
$ cd rhldnjlt
$ ls
dir ffhcbvmf
dir vprlq
$ cd ffhcbvmf
$ ls
247668 cpqhb.jsf
$ cd ..
$ cd vprlq
$ ls
168090 jmmtz.fzt
68360 nhm.zhz
304580 vqfsh.smp
$ cd ..
$ cd ..
$ cd ..
$ cd nhblb
$ ls
154794 hrgsrbnj.tch
dir nfwl
dir ptc
dir rng
50110 swtt.tct
dir vhvn
dir vlj
$ cd nfwl
$ ls
dir lqs
dir mlvnlz
$ cd lqs
$ ls
dir mbcft
dir ntmvt
dir nztw
$ cd mbcft
$ ls
78188 bdnr
194668 pjts
$ cd ..
$ cd ntmvt
$ ls
75647 nhm.zhz
186651 scsvrqpf.jhb
$ cd ..
$ cd nztw
$ ls
164920 vqfsh.smp
$ cd ..
$ cd ..
$ cd mlvnlz
$ ls
289891 wjf
$ cd ..
$ cd ..
$ cd ptc
$ ls
190002 pjts.vmh
$ cd ..
$ cd rng
$ ls
39093 nhm.zhz
$ cd ..
$ cd vhvn
$ ls
275854 hbv
$ cd ..
$ cd vlj
$ ls
dir qqqrm
203390 ssdlqcrw
$ cd qqqrm
$ ls
dir wcpllh
$ cd wcpllh
$ ls
dir pwg
$ cd pwg
$ ls
19102 dtbzzl.qvp
$ cd ..
$ cd ..
$ cd ..
$ cd ..
$ cd ..
$ cd ssdlqcrw
$ ls
181610 vqfsh.smp
$ cd ..
$ cd ttvgr
$ ls
dir vpcpd
$ cd vpcpd
$ ls
28102 mbb.szv
304017 rshrzjhn
$ cd ..
$ cd ..
$ cd vdmm
$ ls
95079 tssjcd.lfg
$ cd ..
$ cd wnhnwjm
$ ls
67931 mmhcgsc.zjf
22062 nqpzsf.ccc
219285 trr.vcn
$ cd ..
$ cd zdvbsb
$ ls
293736 dtbzzl.ftj
$ cd ..
$ cd ..
$ cd ptzsl
$ ls
26404 jnsdzmbd
$ cd ..
$ cd wmqc
$ ls
dir dtbzzl
dir hdzmzc
dir nmmpwqvz
dir qjnm
$ cd dtbzzl
$ ls
dir hpzgnb
$ cd hpzgnb
$ ls
189696 sbmdrbm
$ cd ..
$ cd ..
$ cd hdzmzc
$ ls
143510 dtbzzl.dmp
$ cd ..
$ cd nmmpwqvz
$ ls
276725 nhm.zhz
$ cd ..
$ cd qjnm
$ ls
202264 cpqhb.jsf
"""

INPUT2 = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

OUTPUT2 = """
- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
"""
OUTPUT2 = OUTPUT2.lstrip()


class File:
    def __init__(self, size:int, name:str):
        self.size = size
        self.name = name
        self.parent = None

    @classmethod
    def from_str(cls, s):
        size, name = s.split()
        return cls(int(size), name)

    def __repr__(self) -> str:
        return f"{self.name} (file, size={self.size:,})"


class Folder(list):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.parent: None | Folder = None

    def __repr__(self) -> str:
        return f"{self.name} (dir, {self.size:,})"

    def add(self, file_or_folder: Folder | File):
        self.append(file_or_folder)
        file_or_folder.parent = self

    def _get_folders(self):
        for x in self:
            if isinstance(x, Folder):
                yield x

    def get_folders(self):
        return list(self._get_folders())

    def _get_files(self):
        for x in self:
            if isinstance(x, File):
                yield x

    def get_files(self):
        return list(self._get_files())

    def cd(self, name: str):
        if name == "..":
            return self.parent if self.parent is not None else self

        if name == "/":
            return self.parent.cd(name) if self.parent is not None else self

        for folder in self.get_folders():
            if folder.name == name:
                return folder
        else:
            folder = Folder(name)
            self.add(folder)
            return folder

    def ls(self, level=0):
        rt = ""
        if level==0:
            rt = f"{rt}{'  '*level}- {self}\n"
            rt = f"{rt}{self.ls(level+1)}"
        else:
            for item in self:
                rt = f"{rt}{'  '*level}- {item}\n"
                if isinstance(item, Folder):
                    rt = f"{rt}{item.ls(level+1)}"
        return rt

    @property
    def size(self):
        return self.total_size()

    def total_size(self):
        size = 0
        for item in self:
            size += item.size
        return size


def parse(s):
    folder = Folder("/")
    line: str
    for line in s.splitlines():
        if not line: continue
        if line.startswith("$"):
            cmd = line.removeprefix("$ ")
            if cmd.startswith("cd"):
                cd = cmd.removeprefix("cd ")
                folder = folder.cd(cd)
            elif cmd.startswith("ls"):
                pass
        elif line.startswith("dir"):
            name = line.removeprefix("dir ")
            folder.add(Folder(name))
        # it's a file
        else:
            folder.add(File.from_str(line))
    return folder.cd("/")


def find_candidates(root: Folder, limit = 100000):
    candidates = []
    for folder in root.get_folders():
        if folder.total_size() < limit:
            candidates.append(folder)
        candidates.extend(find_candidates(folder, limit))
    return candidates


def part1():
    """
    You can hear birds chirping and raindrops hitting leaves as the expedition
    proceeds. Occasionally, you can even hear much louder sounds in the distance; how
    big do the animals get out here, anyway?
    
    The device the Elves gave you has problems with more than just its communication
    system. You try to run a system update:
    
    $ system-update --please --pretty-please-with-sugar-on-top
    Error: No space left on device
    
    Perhaps you can delete some files to make space for the update?
    
    You browse around the filesystem to assess the situation and save the resulting
    terminal output (your puzzle input). For example:
    
    $ cd /
    $ ls
    dir a
    14848514 b.txt
    8504156 c.dat
    dir d
    $ cd a
    $ ls
    dir e
    29116 f
    2557 g
    62596 h.lst
    $ cd e
    $ ls
    584 i
    $ cd ..
    $ cd ..
    $ cd d
    $ ls
    4060174 j
    8033020 d.log
    5626152 d.ext
    7214296 k
    
    The filesystem consists of a tree of files (plain data) and directories (which
    can contain other directories or files). The outermost directory is called /. You
    can navigate around the filesystem, moving into or out of directories and listing
    the contents of the directory you're currently in.
    
    Within the terminal output, lines that begin with $ are commands you executed,
    very much like some modern computers:
    
        cd means change directory. This changes which directory is the current
        directory, but the specific result depends on the argument:
            cd x moves in one level: it looks in the current directory for the
            directory named x and makes it the current directory.
            cd .. moves out one level: it finds the directory that contains the
            current directory, then makes that directory the current directory.
            cd / switches the current directory to the outermost directory, /.
        ls means list. It prints out all of the files and directories immediately
        contained by the current directory:
            123 abc means that the current directory contains a file named abc with
            size 123.
            dir xyz means that the current directory contains a directory named xyz.
    
    Given the commands and output in the example above, you can determine that the
    filesystem looks visually like this:
    
    - / (dir)
      - a (dir)
        - e (dir)
          - i (file, size=584)
        - f (file, size=29116)
        - g (file, size=2557)
        - h.lst (file, size=62596)
      - b.txt (file, size=14848514)
      - c.dat (file, size=8504156)
      - d (dir)
        - j (file, size=4060174)
        - d.log (file, size=8033020)
        - d.ext (file, size=5626152)
        - k (file, size=7214296)
    
    Here, there are four directories: / (the outermost directory), a and d (which are
    in /), and e (which is in a). These directories also contain files of various sizes.
    
    Since the disk is full, your first step should probably be to find directories
    that are good candidates for deletion. To do this, you need to determine the
    total size of each directory. The total size of a directory is the sum of the
    sizes of the files it contains, directly or indirectly. (Directories themselves
    do not count as having any intrinsic size.)
    
    The total sizes of the directories above can be found as follows:
    
        The total size of directory e is 584 because it contains a single file i of
        size 584 and no other directories.
        The directory a has total size 94853 because it contains files f (size
        29116), g (size 2557), and h.lst (size 62596), plus file i indirectly (a
        contains e which contains i).
        Directory d has total size 24933642.
        As the outermost directory, / contains every file. Its total size is
        48381165, the sum of the size of every file.
    
    To begin, find all of the directories with a total size of at most 100000,
    then calculate the sum of their total sizes. In the example above,
    these directories are a and e; the sum of their total sizes is 95437 (94853 +
    584). (As in this example, this process can count files more than once!)
    
    Find all of the directories with a total size of at most 100000. What is the sum
    of the total sizes of those directories?
    """
    # assert (size := parse(INPUT2).cd("a").cd("e").total_size()) == 584, f"got {size}"
    # assert (size := parse(INPUT2).cd("a").total_size()) == 94853, f"got {size}"
    # assert (size := parse(INPUT2).cd("d").total_size()) == 24933642, f"got {size}"
    # assert (size := parse(INPUT2).total_size()) == 48381165, f"got {size}"

    result = parse(INPUT)
    l = find_candidates(result)
    total = sum([folder.total_size() for folder in l])
    print(f"{total=}")


def find_delete_candidates(root: Folder, limit = 30000000):
    candidates = []
    for folder in root.get_folders():
        if folder.total_size() >= limit:
            candidates.append(folder)
        candidates.extend(find_delete_candidates(folder, limit))
    return candidates


def part2():
    """
    Now, you're ready to choose a directory to delete.

    The total disk space available to the filesystem is 70000000. To run the update,
    you need unused space of at least 30000000. You need to find a directory you can
    delete that will free up enough space to run the update.
    
    In the example above, the total size of the outermost directory (and thus the total
    amount of used space) is 48381165; this means that the size of the unused space must
    currently be 21618835, which isn't quite the 30000000 required by the update.
    Therefore, the update still requires a directory with total size of at least 8381165
    to be deleted before it can run.
    
    To achieve this, you have the following options:
    
        Delete directory e, which would increase unused space by 584.
        Delete directory a, which would increase unused space by 94853.
        Delete directory d, which would increase unused space by 24933642.
        Delete directory /, which would increase unused space by 48381165.
    
    Directories e and a are both too small; deleting them would not free up enough space.
    However, directories d and / are both big enough! Between these, choose the smallest:
    d, increasing unused space by 24933642.
    
    Find the smallest directory that, if deleted, would free up enough space on the
    filesystem to run the update. What is the total size of that directory?
    """
    HDD_SIZE = 70000000
    NEED     = 30000000

    root = parse(INPUT)
    remaining = HDD_SIZE - root.total_size()
    need = NEED - remaining
    # print(f"{need=:,}")
    # print(root.ls())
    l = find_delete_candidates(root, need)
    l.sort(key=lambda x: x.size)
    print(f"{l[0].size}")


part1()
part2()

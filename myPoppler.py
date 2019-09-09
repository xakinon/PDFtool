# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path
import configparser

def pdf_size(pdf, size, pdfinfo):
    # コマンド実行
    p = subprocess.Popen( [str(pdfinfo), str(pdf)], stdout=subprocess.PIPE, universal_newlines=True )
    p.wait()
    # 戻り値からサイズを取得
    page_size = [ line.strip().split(":")[1].strip().split() for line in p.stdout if "Page size" in line ][0]
    # サイズ一覧から用紙サイズを返す
    for s in page_size:
        try:
            x = int(float(s))
            for a in size:
                if x > size[a]-10 and x < size[a]+10:
                    return a
        except:
            pass
    return -1

def conbine_pdfs(pdfs, size, pdfunite, output):
    # コマンド
    cmd = [ str(pdf) for pdf in pdfs ]
    cmd.insert( 0, str(pdfunite) )
    cmd.append( str(output/Path(size+".pdf")) )
    # 実行
    p = subprocess.Popen( cmd, stdout=subprocess.PIPE, universal_newlines=True )
    p.wait()
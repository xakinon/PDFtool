# -*- coding: utf-8 -*-
from pathlib import Path
import configparser
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from myPoppler import pdf_size, conbine_pdfs
from tableView import Model, TableView, Delegate

class Mainwindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent)

        # mainwindow設定
        self.resize(600, 600)
        self.setAcceptDrops(True)

        # ui設定
        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # tableview設定
        self.tableView = TableView(self.centralwidget)
        self.model = Model()
        self.tableView.setModel(self.model)
        self.tableView.setItemDelegate(Delegate())

        # レイアウト
        self.verticalLayout.addWidget(self.tableView)
        self.setCentralWidget(self.centralwidget)

        # iniファイル読み込み
        self.config = configparser.SafeConfigParser()
        self.config.read('setting.ini')
        self.size = { 'A'+str(n) : int(self.config.get('size', 'A'+str(n))) for n in range(5) }
        self.pdfinfo = Path(self.config.get('path', 'pdfinfo'))
        self.pdfunite = Path(self.config.get('path', 'pdfunite'))
        self.output = Path(self.config.get('path', 'output'))

        # モデルにデータセット
        self.model.addColumns(['filepath', 'size'])

        # テーブルビューにメソッド追加
        self.tableView.menus['PDFを用紙サイズ別に結合'] = self.conbine_pdfs2
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore() 

    def dropEvent(self, event):
        event.accept()
        for url in event.mimeData().urls():
            pdf = Path(url.toLocalFile())
            item = {'filepath':str(pdf), 'size':pdf_size( pdf, self.size, self.pdfinfo ), 'pdf':pdf}
            self.model.addItems([item])

    def conbine_pdfs2(self):
        # PDFファイル
        pdfs = [ item['pdf'] for item in self.model.items ]
        # PDFのサイズ判定
        categolized_pdf = { 'A'+str(n):[] for n in range(5) }
        for pdf in pdfs:
            a = pdf_size( pdf, self.size, self.pdfinfo )
            if a == -1:
                continue
            categolized_pdf[a].append( pdf )
        # PDFをサイズ別に結合
        for a in categolized_pdf:
            conbine_pdfs(categolized_pdf[a], a, self.pdfunite, self.output)
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
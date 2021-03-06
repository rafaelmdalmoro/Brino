#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino Qt Main

Codigo da janela principal da IDE Br.ino
em PyQt5 (python 2.7)

    Icones made by Dave Gandy
    Site: https://www.flaticon.com/authors/dave-gandy
    is licensed by: http://creativecommons.org/licenses/by/3.0/"

    IDE do Br.ino  Copyright (C) 2018  Br.ino

    Este arquivo e parte da IDE do Br.ino.

    A IDE do Br.ino e um software livre: voce pode redistribui-lo
    e / ou modifica-lo de acordo com os termos da Licenca Publica 
    Geral GNU, conforme publicado pela Free Software Foundation, 
    seja a versao 3 da Licenca , ou (na sua opcao) qualquer 
    versao posterior. 

    A IDE do Br.ino e distribuida na esperanca de que seja util,
    mas SEM QUALQUER GARANTIA; sem a garantia implicita de 
    COMERCIALIZACAO ou ADEQUACAO A UM DETERMINADO PROPOSITO. 
    Consulte a Licenca Publica Geral GNU para obter mais detalhes.
    
    Voce deveria ter recebido uma copia da Licenca Publica Geral
    GNU junto com este programa. Caso contrario, veja 
    <https://www.gnu.org/licenses/>
     
website: brino.cc
author: Mateus Berardo
email: mateus.berardo@brino.cc
contributor: Victor Rodrigues Pacheco
email: victor.pacheco@brino.cc
"""

import os
import re
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QMenu, QStatusBar, QMessageBox, QLabel

import GerenciadorDeCodigo
import GerenciadorDeLinguas
import MonitorSerial
import Preferencias
import UI

versao = '3.0.0'
caminho_padrao = ''
monitor = 3


class Principal(QMainWindow):

    def __init__(self):
        super(Principal, self).__init__()

        # Define as acoes
        self.acao_novo = QAction('&Novo', self)
        self.acao_abrir = QAction('Abrir', self)
        self.acao_exemplos = QAction('Exemplos', self)
        self.acao_sair = QAction('Sair', self)
        self.acao_fechar_aba = QAction('Fechar aba', self)
        self.acao_salvar = QAction('&Salvar', self)
        self.acao_salvar_como = QAction('Salvar como', self)
        self.acao_comentar_linha = QAction('Comentar linha', self)
        self.acao_achar = QAction('Achar...', self)
        self.acao_achar_e_substituir = QAction('Achar e substituir', self)
        self.acao_ir_para_linha = QAction('Ir para linha', self)
        self.acao_placa = QAction('Placa', self)
        self.acao_porta = QAction('Porta', self)
        self.acao_lingua = QAction('Lingua', self)
        self.acao_monitor_serial = QAction('Monitor serial', self)
        self.acao_verificar = QAction('Verificar', self)
        self.acao_verificar_e_carregar = QAction('Verificar e carregar', self)
        self.menu_placas = QMenu('Placa')
        self.menu_portas = QMenu('Porta')
        self.menu_exemplos = QMenu('Exemplos')
        self.barra_de_status = QStatusBar()

        self.widget_central = UI.Centro(self)

        self.criar_barra_menu()

        self.init_ui()

    def init_ui(self):
        self.setStatusBar(self.barra_de_status)
        self.placa_porta_label = QLabel(Preferencias.get("board") + " na " + Preferencias.get("serial.port"))
        self.barra_de_status.addPermanentWidget(self.placa_porta_label)

        self.setCentralWidget(self.widget_central)

        self.setGeometry(100, 50, 500, 550)
        self.setMinimumSize(500, 520)
        self.setWindowTitle('Br.ino ' + versao)
        self.setWindowIcon(QIcon(os.path.join('recursos', 'logo.png')))

        self.show()

    def criar_acoes(self):
        """
        Define as funcoes de resposta as acoes e conecta elas. Define atalhos de teclado
        :return:
            None
        """
        self.acao_sair.setShortcut('Ctrl+Q')
        self.acao_sair.setStatusTip('Sair da IDE do Br.ino')
        self.acao_sair.triggered.connect(self.close)
        self.acao_sair.triggered.connect(monitor.close)

        self.acao_fechar_aba.setShortcut('Ctrl+W')
        self.acao_fechar_aba.setStatusTip('Fechar aba atual')
        self.acao_fechar_aba.triggered.connect(self.widget_central.remover_aba)

        self.acao_novo.setShortcut("Ctrl+N")
        self.acao_novo.triggered.connect(self.widget_central.nova_aba)
        self.acao_novo.setStatusTip("Criar novo arquivo")

        self.acao_abrir.setShortcut('Ctrl+O')
        self.acao_abrir.triggered.connect(self.widget_central.abrir)
        self.acao_abrir.setStatusTip("Abrir arquivo")

        self.acao_salvar.setShortcut('Ctrl+S')
        self.acao_salvar.triggered.connect(self.widget_central.salvar)
        self.acao_salvar.setStatusTip("Salvar arquivo")

        self.acao_salvar_como.setShortcut('Ctrl+Shift+S')
        self.acao_salvar_como.triggered.connect(self.widget_central.salvar_como)
        self.acao_salvar_como.setStatusTip("Salvar arquivo como")

        self.acao_comentar_linha.setShortcut('Ctrl+/')
        self.acao_comentar_linha.triggered.connect(self.widget_central.comentar_linha)
        self.acao_comentar_linha.setStatusTip("Comentar linha")

        self.acao_achar.setShortcut('Ctrl+F')
        self.acao_achar.triggered.connect(self.widget_central.achar)
        self.acao_achar.setStatusTip("Achar...")

        self.acao_achar_e_substituir.setShortcut('Ctrl+H')
        self.acao_achar_e_substituir.triggered.connect(self.widget_central.achar_e_substituir)
        self.acao_achar_e_substituir.setStatusTip("Achar e substituir...")

        self.acao_ir_para_linha.setShortcut('Ctrl+L')
        self.acao_ir_para_linha.triggered.connect(GerenciadorDeCodigo.ir_para_linha)
        self.acao_ir_para_linha.setStatusTip("Ir para linha...")

        self.acao_lingua.triggered.connect(GerenciadorDeLinguas.lingua)
        self.acao_lingua.setStatusTip("Opções de língua")

        self.acao_monitor_serial.setShortcut('Ctrl+Shift+M')
        self.acao_monitor_serial.triggered.connect(self.abrir_serial)
        self.acao_monitor_serial.setStatusTip("Abrir monitor serial")

        self.acao_verificar.setShortcut('Ctrl+R')
        self.acao_verificar.triggered.connect(self.widget_central.compilar)
        self.acao_verificar.setStatusTip("Verificar código")

        self.acao_verificar_e_carregar.setShortcut('Ctrl+U')
        self.acao_verificar_e_carregar.triggered.connect(self.widget_central.upload)
        self.acao_verificar_e_carregar.setStatusTip("Verificar e carregar código")

    def criar_barra_menu(self):
        """
        Cria a barra menu e adiciona as funcoes nela
        :return:
            None
        """
        self.criar_acoes()

        barra_menu = self.menuBar()
        barra_menu.setNativeMenuBar(False)
        menu_arquivo = barra_menu.addMenu('Arquivo')
        menu_arquivo.addAction(self.acao_novo)
        menu_arquivo.addAction(self.acao_abrir)
        menu_arquivo.addMenu(self.menu_exemplos)
        menu_arquivo.addAction(self.acao_salvar)
        menu_arquivo.addAction(self.acao_salvar_como)
        menu_arquivo.addAction(self.acao_fechar_aba)
        menu_arquivo.addAction(self.acao_sair)

        menu_editar = barra_menu.addMenu('Editar')
        menu_editar.addAction(self.acao_comentar_linha)
        menu_editar.addAction(self.acao_achar)
        menu_editar.addAction(self.acao_achar_e_substituir)
        menu_editar.addAction(self.acao_ir_para_linha)

        self.menu_ferramentas = barra_menu.addMenu('Ferramentas')
        self.menu_ferramentas.aboutToShow.connect(self.widget_central.criar_menu_portas)
        self.menu_ferramentas.addMenu(self.menu_placas)
        self.menu_ferramentas.addMenu(self.menu_portas)
        self.menu_ferramentas.addAction(self.acao_lingua)
        self.menu_ferramentas.addAction(self.acao_monitor_serial)

        menu_rascunho = barra_menu.addMenu('Rascunho')
        menu_rascunho.addAction(self.acao_verificar)
        menu_rascunho.addAction(self.acao_verificar_e_carregar)

    def abrir_serial(self):
        """
        Abre o monitor serial ou indica que a porta nao esta disponivel
        :return:
            None
        """
        if monitor.conectar(Preferencias.get("serial.port")):
            monitor.show()
        else:
            QMessageBox(QMessageBox.Warning, "Erro", "A porta selecionada não está disponível",
                        QMessageBox.NoButton, self).show()

    def closeEvent(self, close_event):
        """
                Fecha o programa, mas antes verifica se os arquivos foram salvos
                :param close_event:
                :return:
        """
        if self.widget_central.widget_abas.widget(0).caminho == 0:
            num_examinar = 1
        else:
            num_examinar = 0
        for num_arquivo in range(self.widget_central.widget_abas.count() - num_examinar):
            if not self.widget_central.remover_aba(num_examinar, True):
                close_event.ignore()
                return
        close_event.accept()


def get_caminho_padrao():
    """
    Pega o caminho padrao ate a pasta de RascunhosBrino
    :return:
        Caminho padrao
    """
    global caminho_padrao
    caminho_padrao = os.path.expanduser("~")
    docu = re.compile("Documen.*")
    pastas = os.listdir(caminho_padrao)
    documentos = filter(docu.match, pastas)
    return os.path.join(caminho_padrao, documentos[0], "RascunhosBrino")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open(os.path.join("recursos", "stylesheet.txt")) as arquivo_stilo:
        stilo = arquivo_stilo.read()
        app.setStyleSheet(stilo)
    monitor = MonitorSerial.MonitorSerial()
    Preferencias.init()
    principal = Principal()
    principal.show()
    sys.exit(app.exec_())

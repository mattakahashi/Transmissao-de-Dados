#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import threading
import sys
import signal
import logging
from time import gmtime, strftime, localtime

host = "127.0.0.1"
porta_bind = 8080
tamanho_max_buffer = 8192
delay = 5
Arquivo_Log = 'Logs.txt'
logging.basicConfig(filename = Arquivo_Log, filemode = 'a', level=logging.DEBUG,
					format='%(ThreadName)-10s [%(CurrentTime)-10s]  %(message)-s',
					)

class Servidor_Proxy:

	def __init__(self):
		file = open("Logs.txt","w")
		try:
			self.servidorPro = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
			self.servidorPro.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    
			self.servidorPro.bind((host, porta_bind))
			self.servidorPro.listen(100)  
			self.__clientes = {}
			while True:
				print "A"	
				Socket, Endereco = self.servidorPro.accept()
				print "B"
				Multi_acesso = threading.Thread(name=(Endereco), target=self.Requisicoes, args=(Socket, Endereco))
				print "C"
				Multi_acesso.setDaemon(True)
				print "D"
				Multi_acesso.start()
				print "E"						
		except KeyboardInterrupt:
			print "Parou"
			self.log("AVISO: ",-1,"SERVIDOR FECHADO")
			self.servidorPro.close()
			file.close()
			sys.exit(1)

	def Requisicoes(self, conexao, client_addr):

		requisicao = conexao.recv(tamanho_max_buffer) 
		print "AQUI"
		print requisicao
		print "PASSOU"
		operacao = requisicao.split(' ')[0] 
		print "Ae"
		print operacao
		print "Caramba"
		url = requisicao.split(' ')[1]
		print "Opa"
		print url
		print "Deu"
		http_versao = requisicao.split(' ')[2] 
		http_versao_procura = http_versao.index("\n")
		http_versao = http_versao[:http_versao_procura]  
		print "Vamos"
		print http_versao
		print "Funcionar"

		url_sem_http = url.split("http")[1]
		url_sem_http = url_sem_http[3:]
		print "SAFADEZA"
		print url_sem_http
		print "PRONTO"
		porta = 0
		try: 
			ponteiro_barra = url_sem_http.index("/")
		except ValueError:
			ponteiro_barra = len(url_sem_http) 

		print"//////////////////////////////////////////"
		print "Ponteiro Barra: " 
		print ponteiro_barra
		print "////////////////////////////////////////"

		try:
			print "MATHEUS"
			ponteiro_dois_pontos = url_sem_http.index(":")
			print"//////////////////////////////////////////"
			print "Ponteiro Dois: " 
			print ponteiro_dois_pontos
			print "////////////////////////////////////////"
			if (ponteiro_barra>ponteiro_dois_pontos):
				print "//////////////// Entrou if/////////"
				print porta
				pega_porta = url_sem_http[ponteiro_dois_pontos+1:ponteiro_barra]
				print pega_porta
				porta = int(pega_porta)
				print "Porta aqui"
				print porta
				servidor_web = url_sem_http[:ponteiro_dois_pontos]
			else:
				porta = 80
				servidor_web = url_sem_http[:ponteiro_barra]

		except ValueError:
			porta = 80
			servidor_web = url_sem_http[:ponteiro_barra]

		self.log("AVISO: ",client_addr,"REQUISICAO: " + operacao +" "+ url+" " + http_versao)
		print porta
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(delay)
			sock.connect((servidor_web, porta))
			sock.sendall(requisicao)

			while 1:
				dado = sock.recv(tamanho_max_buffer)
				if (len(dado) > 0):
					conexao.send(dado)

				else:
					break
			sock.close()
			conexao.close()
		except socket.error as erro:
			self.log("ERRO", client_addr, erro)
			if sock:
				sock.close()
			if conexao:
				conexao.close()
			self.log("AVISO", client_addr, "CONEXAO_RESET_POR_PEER: " + operacao +" "+ url+" " + http_versao)

	def log(self, log_level, client, msg):
		""" Log the messages to appropriate place """
		LoggerDict = {
			'CurrentTime' : strftime("%a, %d %b %Y %X", localtime()),
			'ThreadName' : threading.currentThread().getName()
		}
		logging.debug('%s',msg,extra=LoggerDict)

if __name__ == "__main__":
	servidor = Servidor_Proxy()
	servidor.escuta()
	print "chegou"		

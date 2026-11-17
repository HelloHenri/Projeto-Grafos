Passo 1: Abrir o Terminal na Pasta do Projeto
Abra a pasta onde estão os arquivos do projeto (ou o repositório clonado do GitHub) no seu computador.
Na barra de endereço da pasta, digite powershell e dê Enter (ou abra o PowerShell e navegue até a pasta usando o comando cd "caminho\da\pasta").

Passo 2: Instalar as Dependências do Projeto
Para garantir que todas as bibliotecas necessárias (streamlit, networkx, matplotlib) sejam instaladas corretamente usando o arquivo oficial do projeto, digite o seguinte comando e aperte Enter:
PowerShell
python -m pip install -r requirements.txt
(Se o seu Python principal estiver registrado pelo atalho py, use: py -m pip install -r requirements.txt)

Passo 3: Executar a Aplicação Web
Com as dependências instaladas, inicie o servidor local do Streamlit digitando este comando:
PowerShell
python -m streamlit run app.py
Passo 4: Usar o Sistema
Assim que você rodar o comando acima, o streamlit vai iniciar o servidor local automaticamente.

Uma aba no seu navegador padrão vai abrir sozinha na tela com o painel interativo pronto para uso (com a seleção de cenários, os grafos coloridos em tempo real, o slider de equipes e os relatórios analíticos de Welsh-Powell e DSATUR).

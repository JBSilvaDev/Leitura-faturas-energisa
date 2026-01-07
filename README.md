# Leitura de Faturas Energisa

Este projeto em Python foi desenvolvido para automatizar a leitura de dados de faturas de energia da distribuidora Energisa em formato PDF. Ele extrai informações específicas das faturas, organiza os dados e os salva em uma planilha Excel.

## Funcionalidades

- **Extração de Texto de PDFs**: Utiliza a biblioteca `pdfplumber` para extrair o conteúdo textual das faturas.
- **Análise com Regex**: Emprega expressões regulares (regex) para encontrar e extrair dados específicos, como:
  - Unidade Consumidora (UC)
  - Data de Vencimento
  - Data de Emissão
  - Valor Total a Pagar
  - Número da Nota Fiscal
  - Código de Barras
  - Endereço
- **Organização de Arquivos**: Move os arquivos PDF processados para pastas distintas, separando os que foram lidos com sucesso daqueles que apresentaram algum erro na extração.
- **Exportação para Excel**: Salva todos os dados extraídos em um arquivo `faturas.xlsx` para fácil visualização e análise.

## Estrutura do Projeto

O projeto foi organizado da seguinte forma para separar as responsabilidades e facilitar a manutenção:

```
Leitura-faturas-energisa/
├─── main.py                # Ponto de entrada da aplicação
├─── config.py              # Configurações e constantes (caminhos, regex)
├─── requirements.txt       # Dependências do projeto
├─── faturas.xlsx           # Planilha com os dados extraídos
├─── README.md              # Documentação do projeto
│
├─── controller/
│    └─── invoice_processor.py # Orquestra o fluxo de processamento das faturas
│
├─── model/
│    └─── invoice_parser.py    # Responsável por analisar o texto e extrair os dados
│
├─── utils/
│    ├─── file_handler.py      # Funções para manipulação de arquivos (mover, listar)
│    └─── pdf_extractor.py     # Função para extrair texto de PDFs
│
├─── faturas_pendentes/       # (Entrada) Coloque as faturas em PDF a serem processadas aqui
├─── faturas_sucesso/         # (Saída) Faturas processadas com sucesso
└─── faturas_erro/            # (Saída) Faturas que falharam no processamento
```

## Pré-requisitos

- Python 3.x
- Pip (gerenciador de pacotes do Python)

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/Leitura-faturas-energisa.git
   cd Leitura-faturas-energisa
   ```
2. **Crie e ative um ambiente virtual (recomendado):**

   ```bash
   python -m venv venv
   # No Windows
   venv\Scripts\activate
   # No macOS/Linux
   source venv/bin/activate
   ```
3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

## Como Usar

1. **Adicione as Faturas**: Coloque todos os arquivos PDF das faturas que você deseja processar dentro da pasta `faturas_pendentes`.
2. **Execute o Script**: Abra o terminal na raiz do projeto e execute o seguinte comando:

   ```bash
   python main.py
   ```
3. **Verifique os Resultados**:

   - Os dados extraídos estarão disponíveis no arquivo `faturas.xlsx`.
   - Os PDFs originais serão movidos para a pasta `faturas_sucesso` se a leitura for bem-sucedida, ou para a pasta `faturas_erro` caso contrário.

## Dependências

As principais bibliotecas utilizadas no projeto são:

- `pandas`: Para a criação e manipulação da planilha Excel.
- `pdfplumber`: Para a extração de texto de arquivos PDF.

Todas as dependências estão listadas no arquivo `requirements.txt`.

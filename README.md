[![weekly-tests](https://github.com/libercapital/dados_publicos_cnpj_receita_federal/actions/workflows/weekly-tests.yaml/badge.svg)](https://github.com/libercapital/dados_publicos_cnpj_receita_federal/actions/workflows/weekly-tests.yaml)

# ***DADOS PUBLICOS CNPJ RECEITA FEDERAL***

Esse repositório consiste na Extração, Transformação e Carregamento (ETL) dos dados públicos dos CNPJ's de todas as ~60
milhões de empresas do Brasil disponibilizadas pela Receita Federal
nesse [link](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/dados-publicos-cnpj)
para um banco relacional ([postgres](https://www.postgresql.org/)) utilizando Docker.

## **Sumário**

- [Introdução](#Introdução)
- [Metodologia](#Metodologia)
- [Arquitetura do Postgres](#Arquitetura-do-Postgres)
- [Tecnologias utilizadas](#Tecnologias-utilizadas)
- [Fluxograma](#Fluxograma)
- [Estrutura do repositório](#Estrutura-do-repositório)
- [Setup & Launch](#Setup-&-Launch)
- [Update](#Update-dos-dados)

## **Introdução**

Os dados dos CNPJ's estão divididos em 3 grandes grupos cada um com 10 arquivos no formato `.zip` que são extraidos para
formato `.csv` :

- Empresas (cnpj raiz)
- Estabelecimentos (cnpj completo)
- Sócios

Além disso os arquivos `SIMPLES` e `Regime Tributario` também foram processados totalizando 5 bases/tabelas.<br>

- Empresas: ~ `350 MB` (por arquivo - são 10)
- Estabelecimentos: ~ `1,1 GB` (por arquivo - são 10)
- Sócios: ~ `250 MB` (por arquivo - são 10)
- Simples: ~ `2 GB`
- Regime tributário: ~`500 MB` (4 arquivos `.csv`)

O processamento total corresponde a um total de ~`20,0 GB` de volume de dados.<br>

O layout para cada arquivo, ou seja, como os arquivos `.csv` estão estruturados, pode ser encontrado
nesse [pdf](docs/NOVOLAYOUTDOSDADOSABERTOSDOCNPJ.pdf) obtido
nesse [link](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/arquivos/NOVOLAYOUTDOSDADOSABERTOSDOCNPJ.pdf)
.

Para o `regime tributário` ver esse [pdf](docs/layout-regime-tributario.pdf) obtido
nesse [link](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/arquivos/leiaute-dos-arquivos.pdf)
.

Além disso existem ainda outros arquivos que mapeiam algumas informações de cada `.csv` tal como o código da natureza
jurídica para seu nome (`2046 -> Sociedade Anônima Aberta`) (esses arquivos também estão presentes ao final da pagina
do [link](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/dados-publicos-cnpj))
.

**Os dados são atualizados mensalmente**. Para realizar a atualização dos dados veja a seção de `UPDATE`.

**_O repositório conta com testes agendados semanalmente para observar qualquer alteração na formatação dos arquivos._**

## **Metodologia**

A estratégia adotada para o processamento se baseia em ler os arquivos `.csv` "brutos" com pandas, realizar a edição das
colunas/mapeamento e enviar para o banco com `COPY` via psycopg2 (códigos estão na pasta engine).

O arquivo [`src/db_models/df_to_db.py`](src/db_models/df_to_db.py) se encarrega de executar o `COPY` no banco de dados
dado um dataframe de uma forma otimizada.

Além disso as chaves primarias e os índices de cada base/tabela foram retirados durante o processamento para reduzir o
tempo de carga/`COPY` (dado as verificações que são necessárias). Ao final do processamento os índices são novamente
inseridos.

Devido a quantidade **massiva** de dados a serem processados, a leitura de todas as tabelas conta com chuncks
de `100.000` linhas por "rodada"/loop por limitações de memória RAM (isso pode variar de acordo com a máquina que se
executa os scripts). Esse valor pode ser alterado em no `.env`:

Ao fim do processamento as 5 tabelas são populadas:

1. Estabelicimentos (`rf_company`): ~51 milhões de linhas
2. Empresas  (`rf_company_root`): ~47 milhões de linhas
3. Sócios (`rf_partners`): ~22 milhões de linhas
4. Simples (`rf_company_root_simples`): ~30 milhões de linhas
4. Regime Tributário (`rf_company_tax_regime`): ~10 milhões de linhas

Total de linhas ao final de todo processamento: ~160 milhões de linhas

## **Arquitetura do Postgres**

As tabelas criadas no banco postgres podem ser visualizadas no arquivo [models.py](src/db_models/models.py)

## Tecnologias utilizadas

Esse reposítorio foi desenvolvido utilizando imagens Docker, Makefile, Python e banco de dados Postgresql.

Caso você estiver utilizando Windows você precisará utilizar o WSL para rodar imagens Docker.

Nesse [link](https://github.com/codeedu/wsl2-docker-quickstart) tem um tutorial bem completo de como rodar
o [WSL + Docker] do FullCycle.

## **Fluxograma**

O fluxograma abaixo representa, em alto nível, o processo de ETL adotado nesse repositório.

![fluxograma](docs/imgs/fluxograma.png)

## **Setup & Launch**

O repositório conta com um [`Makefile`](Makefile) com alguns comandos já 'selecionados' para rodar o que facilita a
execução de todo o processo.

Para ver todos os comandos basta digitar:

````
$ make
````

1. Clonar o repositório `$ git clone https://github.com/libercapital/dados_publicos_cnpj_receita_federal.git`


2. Criar o `.env` na raiz do repostório (mesmo diretório do `docker-compose.yaml`):

```env
N_ROWS_CHUNKSIZE=100000
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=rf_dados_publicos_cnpj
DB_MODEL_COMPANY=rf_company
DB_MODEL_COMPANY_TAX_REGIME=rf_company_tax_regime
DB_MODEL_COMPANY_ROOT=rf_company_root
DB_MODEL_COMPANY_ROOT_SIMPLES=rf_company_root_simples
DB_MODEL_PARTNERS=rf_partners
DB_MODEL_REF_DATE=rf_ref_date
```

Por default os nomes da tabela serão esses (mais detalhes no arquivo [settings.py](src/settings.py)):

> Para se conectar no postgres em algum visualizador (exemplo: DBeaver) coloque as seguintes configurações se você as configurou conforme mostrado acima: <br>
> host: localhost <br>
> database: rf_dados_publicos_cnpj <br>
> porta: 5433 (ver docker-compose.yaml) <br>
> usuário: postgres <br>
> senha: postgres

3. Crie a image docker utilizada no processamento:

```terminal
$ make build-img
```

4. Execute para subir os containers (a imagem do postgres será baixada):

```terminal
$ make up
```

5. Execute para fazer criar o modelo do banco de dados:

```terminal
$ make db-setup
```

6. Execute para fazer o **_download_** e **_unzip_** dos arquivos
   do [link](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/dados-publicos-cnpj):

```terminal
$ make io-download-and-unzip
```

### Carregamento dos dados

> ### Forma "supervisionada" (sugerida)
> 7. Execute para fazer a carga/processamento para o posgres do  `rf_company_root`:
>
> ```terminal
> $ make engine-company-root
> ```
>
> 8. Execute para fazer a carga/processamento para o posgres do `rf_partners`:
>
> ```terminal
> $ make engine-partners
> ```
>
> 9. Execute para fazer a carga/processamento para o posgres do  `rf_company_root_simples`:
>
> ```terminal
> $ make engine-company-root-simples
> ```
>
> 10. Execute para fazer a carga/processamento para o posgres do `rf_company_tax_regime`:
>
> ```terminal
> $ make engine-company-tax-regime
> ```
>
> 11. Execute para fazer a carga/processamento para o posgres do `rf_company`:
>
> ```terminal
> $ make engine-company
> ```
>
> 12. Execute para fazer a carga/processamento do `rf_ref_date` que diz a data de referencia dos arquviso processados para o postgres:
>
> ```terminal
> $ make engine-ref-date
> ```


> ### Forma única
>
> 7. Execute para fazer a carga/processamento dos arquivos para o postgres:
>
> ```terminal
> make engine-main
> ```

## **Update dos dados**

Para realizar o update dos dados quando uma nova "rodada" de arquivos for disponibilizada, a melhor forma de garantir o
uptime em produção é:

1. baixar e deszipar os arquivos (step 6 de `Setup & Launch`)

2. criar **novas** tabelas com o sufixo no nome: `'_new'` (alterando no [settings.py](src/settings.py));

3. fazer a carga dos arquivos (step 7 -> 12 de `Setup & Launch`);

4. renomear as tabelas antigas para `'_old'` (via _sql_);

5. retirar o sufixo `'_new'` das tabelas novas (via _sql_);

6. deletar as antigas `'_old'` (via _sql_);

## **Estrutura do repositório**

A pasta `src/data/` contem todos os arquivos `.zip`, `.csv` e `.jsons` obtidos
em [`http://200.152.38.155/CNPJ`](http://200.152.38.155/CNPJ) separados por data de referência (a pasta `src/data/` está
no gitignore dado o tamanho de seus arquivos).

A pasta `src/db_models/` contém todos os scripts necessários para a manipular os modelos do banco de dados e auxiliar no
carregamento dos dados no banco de dados.

A pasta `src/io/` contém todos os scripts necessários para realizar o download e unzip dos arquivos `.zip`

A pasta `src/engine/` contém os códigos que executam o processanto do arquivo no formato `.csv` e a ingestão no banco de
dados.

```
dados_abertos_receita_federal/
├── Dockerfile
├── Makefile
├── docker-compose.yaml
├── pytest.ini
├── README.md
├── docs/
│ ├── layout-regime-tributario.pdf
│ ├── NOVOLAYOUTDOSDADOSABERTOSDOCNPJ.pdf
│ └── imgs/
│     ├── fluxograma.png
│     └── mermaid_helpers.txt
├── requirements/
│     ├── requirements.txt
│     └── testing.txt
├── src/
│ ├── data/
│ │ ├── 202Y1-MM1-DD1/
│ │ │ ├── F.K03200$W.SIMPLES.CSV.D10814.zip
│ │ │ ├── F.K03200$Z.D10814.CNAECSV.zip
│ │ │ ├── F.K03200$Z.D10814.MOTICSV.zip
│ │ │ ├── F.K03200$Z.D10814.MUNICCSV.zip
│ │ │ ├── F.K03200$Z.D10814.NATJUCSV.zip
│ │ │ ├── F.K03200$Z.D10814.PAISCSV.zip
│ │ │ ├── F.K03200$Z.D10814.QUALSCSV.zip
│ │ │ ├── K3241.K03200Y0.D10814.EMPRECSV.zip
│ │ │ ├── K3241.K03200Y0.D10814.ESTABELE.zip
│ │ │ ├── K3241.K03200Y0.D10814.SOCIOCSV.zip
│ │ │ ├── ...
│ │ │ ├── K3241.K03200Y9.D10814.ESTABELE.zip
│ │ │ ├── K3241.K03200Y9.D10814.SOCIOCSV.zip
│ │ │ └── unziped/
│ │ │     ├── F.K03200$W.SIMPLES.CSV.D10814
│ │ │     ├── F.K03200$Z.D10814.CNAECSV
│ │ │     ├── F.K03200$Z.D10814.MOTICSV
│ │ │     ├── F.K03200$Z.D10814.MUNICCSV
│ │ │     ├── F.K03200$Z.D10814.NATJUCSV
│ │ │     ├── F.K03200$Z.D10814.PAISCSV
│ │ │     ├── F.K03200$Z.D10814.QUALSCSV
│ │ │     ├── K3241.K03200Y0.D10814.EMPRECSV
│ │ │     ├── K3241.K03200Y0.D10814.ESTABELE
│ │ │     ├── K3241.K03200Y0.D10814.SOCIOCSV
│ │ │     ├── ...
│ │ │     ├── K3241.K03200Y9.D10814.ESTABELE
│ │ │     ├── K3241.K03200Y9.D10814.SOCIOCSV
│ │ │     ├── cnaes.json
│ │ │     ├── motivos.json
│ │ │     ├── municipios.json
│ │ │     ├── natju.json
│ │ │     ├── pais.json
│ │ │     └── qual_socio.json
│ │ └── 202Y2-MM2-DD2/
│ ├── db_models/
│ │ ├── __init__.py
│ │ ├── config_models.py
│ │ ├── create_tables.py
│ │ ├── df_to_db.py
│ │ ├── models.py
│ │ ├── reset.py
│ │ └── utils.py
│ ├── engine/
│ │ ├── __init__.py
│ │ ├── company.py
│ │ ├── company_tax_regime.py
│ │ ├── company_root.py
│ │ ├── company_root_simples.py
│ │ ├── core.py
│ │ ├── main.py
│ │ └── partners.py
│ └── io/
│     ├── __init__.py
│     ├── create_jsons_from_csv.py
│     ├── download.py
│     ├── get_files_dict.py
│     ├── get_last_ref_date.py
│     ├── unzip.py
│     └── utils.py
└── tests/
      └── ...
```

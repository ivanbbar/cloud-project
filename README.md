# Terraform AWS

## Overview

Aplicação capaz de provisionar uma infraestrutura por meio de uma interface amigável para gerenciar e administrá-la (construir, alterar e deletar recursos).

Cria: VPC criação de uma VPC e sub-rede; instâncias: esta funcionalidade deverá permitir a escolha de pelo menos 2 tipos de configuração de hosts; ainda deverá ser possível aumentar e diminuir a quantidade de instâncias; security group: criação e a associação de grupos de segurança com instâncias; Usuário no IAM.

Deleta: Instâncias, grupos de segurança e usuário.

Lista: Aplicação deverá listar todas instâncias e suas regiões, usuários, grupos de segurança e suas regras.

## Prerequisites

- Terraform installed
- AWS account
- Setup environment

````bash
python3 -m virtualenv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
````
- Arquivo `.env`

````bash
ACCESS_KEY="{inserir access key}"
SECRET_KEY="{inserir secret key}"
````

- Arquivo `terraform.tvars`

````bash
aws_access_key="{inserir access key}"
aws_secret_key="{inserir secret key}"
````

## Usage

Executar, dento do diretório interface:

````bash
python main.py
````

O menu de boas-vindas se iniciará, onde o usuário pode digitar `y` para iniciar a aplicação ou `q` para ir embora.

Ao prosseguir, o comando terraform init é executado e a aplicação de fato se inicia. A tela principal é exibida.


> *Na tela principal, o usuário pode escolher qual modulo ele quer executar ações.*\
> \
> [i] Menu que gerencia Instances\
> [s] Menu que gerencia Security Groups\
> [u] Menu que gerencia Users\
> [q] Quit

### Instances 

> *No menu que gerencia instâncias, o usuário pode escolher qual ação ele quer executar.*\
> \
> [c] Criar Instâncias (de dois tipos diferentes, t2.nano e t2.micro)\
> [l] Lista Instâncias Existentes\
> [d] Deleta Instâncias\
> [b] Volta para a tela principal

### Security Groups 

> *No menu que gerencia security groups, o usuário pode escolher qual ação ele quer executar.*\
> \
> [c] Criar Security Groups (com configurações default)\
> [l] Lista Security Groups Existentes\
> [d] Deleta Security Groups\
> [a] Associa Security Group com Instância Existente\
> [b] Volta para a tela principal

### Users 

> *No menu que gerencia usuários, o usuário pode escolher qual ação ele quer executar.*\
> \
> [c] Criar Usuários\
> [l] Lista Usuários Existentes\
> [d] Deleta Usuários\
> [b] Volta para a tela principal
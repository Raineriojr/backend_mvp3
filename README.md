# MVP3 - Backend 🖥️
  API para MVP 3 de pós graduação de Eng de Software da PUC-Rio.
  Consiste em um sistema que simula um ambiente para adicionar amigos a sua lista de amizades, com base em uma lista de sugestão de amizades buscadas em uma API externa.


## Principais tecnologias utilizadas 🧑🏽‍💻
  - Python
  - Flask
  - OpenApi
  - Swagger
  - Docker
  - [Randomuser](https://randomuser.me/) API externa de usuário fakes.


## Documentação 📃✅
  A documentação do serviço, no Swagger,pode ser consultada ao iniciar a aplicação, na rota `localhost:5001/`.


## Passos para executar aplicação com docker 👣
  A aplicação está utilizando docker container, então para sua execução realize os passos abaixo.

  1. Clonar repositório
  2. No terminal do vscode, acesse o diretório do projeto clonado e execute o arquivo do docker compose com o comando `docker-compose up`
  3. Isso irá criar um container docker com o servidor rodando
  4. Para testar o funcionamento abra a url local na porta 5001 no seu navegador.

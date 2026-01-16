# Problema de negócio
Parabéns! Você acaba de ser contratado como Cientista de Dados da empresaFome Zero, e a sua principal tarefa nesse momento é ajudar o CEO Kleiton Guerra a identificar pontos chaves da empresa, respondendo às perguntas que ele fizerutilizando dados!
A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu corebusiness é facilitar o encontro e negociações de clientes e restaurantes. Osrestaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibilizainformações como endereço, tipo de culinária servida, se possui reservas, se fazentregas e também uma nota de avaliação dos serviços e produtos do restaurante,dentre outras informações.

# O Desafio
O CEO Guerra também foi recém contratado e precisa entender melhor o negóciopara conseguir tomar as melhores decisões estratégicas e alavancar ainda mais aFome Zero, e para isso, ele precisa que seja feita uma análise nos dados daempresa e que sejam gerados dashboards, a partir dessas análises, para responderàs seguintes perguntas:

### Geral
1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

### Pais
1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culináriadistintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazementrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliaçõesregistrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?

### Cidade
1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culináriadistintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazemreservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazementregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes queaceitam pedidos online?

### Restaurantes
1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duaspessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menormédia de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, quepossui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, osrestaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes quepossuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da Américapossuem um valor médio de prato para duas pessoas maior que as churrascariasamericanas (BBQ)?

### Tipos de Culinária
1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome dorestaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome dorestaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome dorestaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome dorestaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome dorestaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome dorestaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome dorestaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome dorestaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome dorestaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome dorestaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duaspessoas?
12. Qual o tipo de culinária que possui a maior nota média?
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidosonline e fazem entregas?

# Premissas assumidas para a análise
1. A análise foi realizada com dados de tarnsações do último período
2. Marketplace foi o modelo de negócio assumido.
3. As 5 principais visões do negócio foram: Geral, País, Cidade, Restaurantes e Culinária

# Estratégia da solução
O painel estratégico foi desenvolvido utilizando as métricas que refletem as 5 principais visões do modelo de negócio da empresa: 
1 Geral
2. País
3. Cidade
4. Restaurantes
5. Culinária

#### Cada visão é representada pelo seguinte conjunto de métricas.
#### 1. Geral
    a. Restaurantes registrados
    b. Países registrados
    c. Cidades registradas
    d. Total de avaliações feitas
    f. Tipos de culinária registrados

#### 2. País
    a. Cidades Registradas por País
    b. Cidades Registradas por País
    c. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4registrados?
    d. Tipos de Culinária por País
    e. Total de Avaliações por País
    f. Restaurantes que Entregam Agora
    g. Restaurantes com Reserva de Mesa
    h. Top Maiores Avaliações Médias
    i. Top Menores Avaliações Médias
    j. Qtd. de Restaurantes Luxo (Nível 4)
    k. Média de Preço para Dois

#### 3. Cidade
    a. Top 10 Cidades com Mais Restaurantes
    b. Cidades com Notas Altas (> 4)
    c. Cidades com Notas Baixas (< 2.5)
    d. Cidades com Maior Preço Médio (Prato para dois)
    e. Cidades com Maior Diversidade Culinária
    f. Cidades com Entregas Ativas
    g. Cidades com Pedidos Online
    h. Cidades com Reservas de Mesa

#### 4. Restaurantes
    a. Top 10 Restaurantes Mais Avaliados
    b. Top 20 Restaurantes com Maiores Notas Médias
    c. Menores Notas Culinária Brasileira
    d. Melhores Notas Culinária brasileira (Brasil)
    e. Engajamento Total: Pedidos Online vs. Qtd. de Avaliações
    f. Top 10 Restaurantes com Maior Custo para Dois
    g. Relação entre Reservas de Mesa e Custo Médio
    h. Comparativo de Custo: Comida Japonesa vs. BBQ (EUA)

#### 5. Tipos de Culinária
    a. Performance: Culinária Italian
    b. Performance: Culinária American
    c. Performance: Culinária Arabian
    d. Performance: Culinária Japanese
    e. Performance: Culinária Home-made
    f. Top 10 Culinárias mais Caras para Duas Pessoas
    g. Top 10 Culinárias com Melhores Notas
    h. Top 10 Culinárias com Menores Notas
    i. Top 10 Culinárias com Maior Disponibilidade de Entrega Online

## As ferramentas utilizadas foram:
 - Python 
 - Jupyter Lab
 - Terminal
 - Streamlit 
 - Streamlit Cloud
 - Github

# Top Insights de dados
1. Destaque: India possui a maior capilaridade com 49 cidades registradas.
2. Presença: India lidera em volume com 3,111 estabelecimentos cadastrados.
3. Diversidade: India oferece a maior variedade gastronômica (94 tipos).
4. Engajamento: India é o país mais avaliado pelos usuários (2,800,164 votos).
5. Campeão de Qualidade: Indonesia (4.60).
6. Custo Médio: Indonesia possui o prato para dois mais caro (303000.00).

# O produto final do projeto
Painel online, hospedado em um Cloud e disponível para acesso em 
qualquer dispositivo conectado à internet.
O painel pode ser acessado através desse link: https://fome-zero-ezohjkddahdzszczgrmdsm.streamlit.app/

# Conclusão
O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO. Da Visão País podemos concluir que a India lidera em quase todos os quisitos sendo o país com maior potencial.

# Próximo passos
1. Reduzir o número de métricas.
2. Criar novos filtros.
3. Adicionar novas visões de negócio.


# Problema de negócio
A Fome Zero é um marketplace de restaurantes que facilita a conexão entre clientes e estabelecimentos — disponibilizando informações como localização, tipo de culinária, avaliações, reservas e entregas. O CEO recém-contratado Kleiton Guerra precisa entender rapidamente a estrutura e o desempenho do negócio para tomar decisões estratégicas com base em dados. O desafio é transformar um volume expressivo de dados cadastrais e de avaliação em visibilidade clara sobre os cinco pilares do negócio: panorama geral, países, cidades, restaurantes e tipos de culinária.

# Premissas da análise
* Dados do último período de transações disponível
* Modelo de negócio: Marketplace
* Cinco visões estruturadas: Geral, País, Cidade, Restaurantes e Culinária 

# Perguntas de Negócio

### Visão Geral:
1. Qual o tamanho atual da plataforma em restaurantes, países, cidades, avaliações e tipos de culinária?

### Visão País:
2. Quais países concentram maior volume de restaurantes, cidades e avaliações?
3. Quais países lideram em qualidade média de avaliação — e quais ficam na base?
4. Onde estão os restaurantes de alto padrão (nível de preço 4) e maior diversidade culinária?

### Visão Cidade:
5. Quais cidades concentram mais restaurantes com notas altas e quais têm notas críticas abaixo de 2.5?
6. Quais cidades lideram em diversidade culinária, entregas ativas e pedidos online?

### Visão Restaurantes:
7. Quais restaurantes se destacam em volume de avaliações, nota média e custo por prato?
8. Restaurantes com pedido online recebem mais avaliações? Restaurantes com reserva cobram mais caro?
9. Culinária japonesa é mais cara que churrascaria americana (BBQ) nos EUA?

### Visão Culinária:
10. Quais tipos de culinária lideram em nota média, preço médio e disponibilidade de entrega online?
11. Quais culinárias têm as menores notas — e representam risco de reputação para a plataforma?

# Estratégia da solução
O painel foi construído em cinco visões independentes e navegáveis, cada uma respondendo ao conjunto de perguntas do CEO:

* **Visão Geral:** indicadores macro da plataforma — restaurantes, países, cidades, avaliações e culinárias registradas

* **Visão País:** cidades e restaurantes por país, diversidade culinária, volume de avaliações, nota média, preço médio e disponibilidade de reserva e entrega

* **Visão Cidade:** top 10 cidades por volume de restaurantes, cidades com notas altas e críticas, maior preço médio, maior diversidade culinária e maior disponibilidade de serviços

* **Visão Restaurantes:** ranking por avaliações, nota média e custo; comparativos entre restaurantes com e sem pedido online e reserva; análise de custo entre culinárias nos EUA

* **Visão Culinária:** performance das principais culinárias por nota e preço; ranking de entregas online; identificação das culinárias com menor avaliação

#### **Ferramentas:** Python, Jupyter Lab, Streamlit, Streamlit Cloud, GitHub

# Top Insights da Análise
### 1. Índia domina a plataforma em quase todas as dimensões — e isso é um risco estrutural
A Índia lidera em capilaridade (49 cidades), volume (3.111 restaurantes), diversidade gastronômica (94 tipos de culinária) e engajamento (2.800.164 avaliações). Essa concentração em um único país representa o mesmo risco identificado em outros projetos de marketplace: dependência estrutural de um mercado. Qualquer instabilidade regulatória, competitiva ou econômica na Índia impacta de forma desproporcional os KPIs globais da plataforma.

### 2. O país com melhor qualidade não é o maior — Indonésia lidera em nota com menos volume
A Indonésia registra a maior nota média da plataforma (4,60) e o maior custo médio por prato para dois (R$ 303.000,00 em moeda local) — sem estar no topo em volume de restaurantes ou avaliações. Isso revela um perfil de mercado premium e de alta satisfação que a plataforma ainda não explorou em profundidade. Expandir a presença na Indonésia representa oportunidade de crescimento em um mercado de alto valor e alta qualidade percebida.

### 3. Existe uma desconexão entre volume de avaliações e qualidade — que precisa ser monitorada
A Índia concentra o maior volume de avaliações da plataforma, mas não lidera em nota média. Isso indica que escala e qualidade não caminham juntas — e que o crescimento em volume de restaurantes pode estar diluindo a experiência do usuário. Sem monitoramento ativo das culinárias e cidades com notas abaixo de 2,5, o crescimento da base de restaurantes pode deteriorar a reputação da plataforma antes que o CEO perceba.

### 4. Pedido online e reserva de mesa são diferenciais mensuráveis de engajamento e ticket
A análise compara diretamente restaurantes com e sem pedido online em volume de avaliações, e restaurantes com e sem reserva de mesa em custo médio por prato. Esses dois cruzamentos entregam ao CEO evidência para uma decisão estratégica: incentivar a adoção dessas funcionalidades pelos restaurantes cadastrados pode aumentar simultaneamente engajamento e ticket médio na plataforma.

### 5. A culinária japonesa nos EUA supera o BBQ em custo médio por prato
O comparativo direto entre culinária japonesa e churrascaria americana (BBQ) nos Estados Unidos revela diferença de preço médio por prato — posicionando a culinária japonesa no segmento de maior ticket no mercado americano. Esse dado tem implicação direta na estratégia de expansão e na seleção de parceiros nos EUA.

# Produto Final
Painel estratégico online com cinco visões navegáveis, desenvolvido em Streamlit e hospedado em cloud — acessível em qualquer dispositivo conectado à internet, sem necessidade de instalação. O CEO Kleiton Guerra passa a ter visibilidade centralizada sobre todos os pilares do negócio em tempo real, substituindo análises pontuais e dispersas por uma única fonte de verdade que acompanha o crescimento da plataforma.

#### Link do Projeto:
https://fome-zero-ezohjkddahdzszczgrmdsm.streamlit.app/

# Resultado
O painel entrega ao CEO as respostas para mais de 40 perguntas estratégicas organizadas em cinco visões — transformando um volume expressivo de dados cadastrais em inteligência acionável para as primeiras decisões da nova gestão.

**A Índia é o maior mercado da plataforma — e o maior risco concentrado:** Liderar em cidades, restaurantes, diversidade e avaliações em um único país cria dependência estrutural que precisa ser endereçada com estratégia deliberada de diversificação geográfica. O crescimento da plataforma precisa reduzir progressivamente o peso relativo da Índia no total de KPIs.

**A Indonésia é o mercado de maior potencial inexplorado:** Maior nota média e maior ticket médio da plataforma com volume ainda reduzido de restaurantes — perfil claro de mercado premium subexplorado. Expandir a base de restaurantes na Indonésia sem comprometer a qualidade média é a oportunidade de crescimento de maior retorno por unidade identificada na análise.

**Pedido online e reserva de mesa são alavancas de crescimento subutilizadas:** A correlação entre essas funcionalidades e maiores volumes de avaliação e ticket médio indica que incentivar a adoção por restaurantes já cadastrados — antes de adquirir novos parceiros — pode elevar os KPIs da plataforma sem aumento de custo de aquisição.

# Próximo passos
* **Monitorar cidades e culinárias com notas abaixo de 2,5:** Criar alerta automático no painel para restaurantes que caem abaixo do limiar crítico de avaliação — proteger a reputação da plataforma é tão importante quanto crescer em volume de cadastros

* **Desenvolver estratégia de expansão para a Indonésia:** Estruturar plano de crescimento no mercado de maior qualidade média da plataforma, definindo metas de novos restaurantes sem comprometer a nota média que posiciona o mercado como premium

* **Criar programa de incentivo a pedido online e reserva de mesa:** Usar a evidência da análise para desenvolver campanha junto aos restaurantes cadastrados que ainda não oferecem essas funcionalidades — aumentando engajamento e ticket médio sem necessidade de novos parceiros

* **Refinar e expandir o painel:** Consolidar as métricas de maior impacto decisório, adicionar filtros por período e região, e incorporar novas visões de negócio conforme a gestão do CEO Guerra identificar novas perguntas estratégicas
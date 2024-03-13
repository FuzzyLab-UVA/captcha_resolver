# Captcha Resolver

## Como executar

Cada programa faz alguma coisa dentro da pipeline da IA, execute os arquivos nessa ordem.

- data_mine.py => Ele extrai os captchas do BreachForums
- etl_captcha.py => Personaliza as imagens para se adequarem ao modelo
- spell_letters.py -> Separa as letras das imagens filtradass
- train_model.py => Treina o modelo

## Introdução do problema

No dia 19 de Dezembro de 2023, o twitter da atual primeira dama *Rosângela da Silva* foi hackeado, o hacker em questão disse que conseguiu os seus dados apartir de banco de dados vazados pela internet e que a senha igualava a dos bancos vazados.
Com o pensamento de resolver esse problema foi pensando por mim em utilizar a ferramenta *Sherlock*, muito conhecida no mundo hacker para conseguir informações sobre alvos, usando como parâmetro o seu usuário em alguma rede social conhecida. Então realizei um *fork* do código e otimizando para que fosse possivel ser uma biblioteca para a criação de uma página web usando o framework Python **DJANGO**, mas para complementar essa criação para que seja possivel identificar alvos que correm riscos de serem hackeados, decidi fundir essa criação com o sistema do *I Have Been Pwnd?*
*I Have Been Pwnd?* é um site que verifica em banco de dados vazados se os seus dados estão expostos nele e qual site o seu dado foi vazado. Essa ferramenta junto ao Sherlock permite que possamos ver além dos email quais usuários estão em risco, pois o *I Have Been Pwnd?* só usa o email como parâmetro.


## Desafio encontrado

O sistema do *I Have been Pwnd?* é bem simples, porém o problema de replicar esse sistema que foi escrito originalmente em C# para o Python é que conseguir acesso a esses banco de dados vazados seja na Deep Web ou na surface web exije o uso de uma ferramenta mais sofisticada ou um justiceiro dedicado, nesse caso fomos pela ferramenta sofisticada.

## Resolução do Desafio

O site onde vamos extrair a base de dados é o mesmo que o *I Have been Pwnd?* usa que é o *Breached Forums*, o maior fórum hacker do mundo, com vazamento de dados diariamente, mas como vamos conseguir esses dados de graça?
O site consta com um sistema de créditos que você pode conseguir através do pagamento de cripto-moedas ou interagindo nos fóruns, mas para interagir nos fóruns decidimos fazer a mesma coisa que o video do *Yannic Kilcher* com nome "GPT-4chan: This is the worst AI ever", aonde o Youtuber criou um MML baseado no GPT para responder as postagens do fórum como se fosse um membro.
Claro que aqui vamos fazer o nosso bot ser menos ativo para não levantar suspeitas como o do *Yannic Kilcher* levantou.
Para isso vamos utilizar ferramentas como Selenium para automação, Beautiful Soup para fazer webscrapping e conseguir dados de como os usuários do fórum se comunicam e usaremos o código Open Source do GPT-3 para a criação do modelo.
Entretando temos outro desafio que não foi mencionado até agora que são os CAPTCHAS do site, utilzei um algoritmo baseado no artigo do **Adam Geitgey** e a sua explicação de resoulução ainda vai ser abordada nesse artigo sobre toda resulução do problema.

## A história do Breached Forums

O Breached Forums na verdade é originario do site Raid Foruns, criado pelo amigo do YouTuber CELAEON que faziam as Raids na Twitch com o intuito de *trollar* os alvos, para organizar essas Raids o Português Diogo Santos Coelho conhecido na internet como “Onipotente” e “Kevin Maradona”, após a fama do site, "Onipotente" decidiu ampliar o seu negócio para dados vazados e aos 21 anos foi preso pelo FBI.
Porém se engana que o fórum acabou após a prisão de "Onipotente", pois ele foi recriado pelo moderador "Baphomet" utilizando o código original, somente mudando o nome e o dóminio para Breached Forums.

## Captcha Resolver

O Captcha Resolver é para resolver os problemas de captchas do Breached Forums esse algoritmo está sendo baseado no artigo escrito por **Adam Geitgey** que usou o livro *Deep Learning for Computer Vision with Python* escrito por **Adrian Rosebrock** para quebrar em 2 minutos o CAPTCHA mais famoso do mundo a aplicação **Really Simple CAPTCHA** do *Wordpress*.

## Referencias

https://medium.com/@ageitgey/how-to-break-a-captcha-system-in-15-minutes-with-machine-learning-dbebb035a710

https://www.linkedin.com/pulse/forums-de-vazamentos-dados-romullo-carvalho/?originalSubdomain=pt

# Manual passo a passo — Colocando o "Cadê Bolsa?" no ar
### Para quem nunca programou

Este manual assume que você não tem experiência com programação, terminal ou
servidores. Cada passo explica também **o que é** aquilo que você está fazendo,
não só o "clique aqui".

**Antes de começar, alguns termos que vão aparecer o tempo todo:**

| Termo | O que significa |
|---|---|
| **Terminal** | Uma janela de texto onde você digita comandos em vez de clicar em botões. É como conversar com o computador digitando frases específicas. |
| **VPS / Servidor** | Um computador ligado 24 horas por dia na internet, que você aluga de uma empresa, e onde seu site vai "morar". |
| **SSH** | A forma de você "entrar" dentro do servidor remotamente, digitando comandos, como se estivesse na frente dele. |
| **Repositório (repo)** | Uma pasta de projeto guardada no GitHub, com histórico de tudo que foi alterado. |
| **DNS** | O "sistema de endereços" da internet — é o que faz `cadebolsa.com.br` apontar para o computador certo. |
| **HTTPS / SSL** | O cadeado de segurança que aparece no navegador. Protege os dados entre o visitante e o site. |

Você vai precisar, ao longo do manual:
- Um computador (Windows ou Mac)
- O arquivo `cadebolsa.zip` que já te enviei
- Um cartão de crédito (para contratar o servidor — custa entre R$20 e R$60/mês, dependendo do provedor)
- Cerca de 1 a 2 horas na primeira vez

---

# ITEM 1 — Subir o código para o GitHub

Como você não usa comandos de programação no dia a dia, vamos usar o
**GitHub Desktop**, um programa com botões (sem digitar comandos de git).

### Passo 1.1 — Criar conta no GitHub
1. Acesse **https://github.com**
2. Clique em **Sign up**
3. Preencha e-mail, senha e nome de usuário
4. Confirme seu e-mail (vai chegar um link de confirmação na sua caixa de entrada)

### Passo 1.2 — Instalar o GitHub Desktop
1. Acesse **https://desktop.github.com**
2. Baixe e instale o programa (funciona em Windows e Mac)
3. Abra o programa e faça login com a conta que você acabou de criar

### Passo 1.3 — Extrair o arquivo zip
1. Encontre o arquivo `cadebolsa.zip` que baixou da nossa conversa
2. Clique com o botão direito nele → **Extrair tudo** (Windows) ou dê duplo clique (Mac)
3. Isso vai criar uma pasta chamada `cadebolsa` com todos os arquivos dentro

### Passo 1.4 — Criar o repositório
1. No GitHub Desktop, vá em **File → New Repository** (ou "Add → Create New Repository")
2. Em **Local Path**, escolha uma pasta no seu computador (pode ser a Área de Trabalho)
3. Dê o nome `cadebolsa`
4. Clique em **Create Repository**

### Passo 1.5 — Colocar os arquivos dentro do repositório
1. O GitHub Desktop criou uma pasta vazia. Copie **todos os arquivos de dentro**
   da pasta `cadebolsa` que você extraiu do zip (agente_bolsas.py, app.py,
   templates, static, deploy, etc.) para dentro dessa nova pasta do repositório
2. Volte para o GitHub Desktop — ele vai mostrar automaticamente uma lista de
   arquivos "novos" (cada um com uma marcação verde)

### Passo 1.6 — Enviar (commit + push)
1. No campo de texto embaixo à esquerda ("Summary"), escreva algo como
   `Primeira versão do Cadê Bolsa`
2. Clique no botão azul **Commit to main**
3. Depois, clique no botão **Publish repository** no topo
4. **IMPORTANTE:** desmarque a opção "Keep this code private" **apenas se**
   quiser deixar público (recomendo deixar **marcado**, ou seja, repositório
   **privado** — assim ninguém mais vê seu código)
5. Clique em **Publish Repository**

Pronto — seu código já está no GitHub. Você pode conferir entrando em
`github.com/SEU_USUARIO/cadebolsa` pelo navegador.

> **Nota sobre o arquivo `.env`:** esse arquivo guarda sua chave secreta da
> API. Ele foi configurado para **nunca** ser enviado ao GitHub (o arquivo
> `.gitignore` cuida disso). Você vai criá-lo diretamente no servidor, no Item 3.

---

# ITEM 2 — Preparar o servidor

### Passo 2.1 — Contratar o servidor (VPS)
Sugestões de provedores simples de usar (todos em dólar/euro, pagamento com
cartão internacional funciona no Brasil):
- **Hetzner** (https://www.hetzner.com/cloud) — o mais barato, ótima qualidade
- **DigitalOcean** (https://www.digitalocean.com)
- **Contabo** (https://contabo.com)

Ao criar o servidor, escolha:
- **Sistema operacional:** Ubuntu 22.04 ou Ubuntu 24.04
- **Plano:** o mais básico já serve (1 ou 2 GB de RAM)
- **Região:** escolha uma próxima do Brasil, se disponível (ex: São Paulo, na
  DigitalOcean e Hetzner já têm essa opção)

Depois de criado, o provedor vai te mostrar:
- Um **endereço IP** (algo como `123.45.67.89`) — anote, você vai usar sempre
- Uma **senha de root** (ou você configura uma chave SSH — se o provedor
  perguntar, pode escolher "senha" para simplificar)

### Passo 2.2 — Conectar no servidor pela primeira vez (SSH)

**No Windows:**
1. Aperte a tecla Windows, digite `PowerShell` e abra o **Windows PowerShell**
   (já vem instalado, não precisa baixar nada)
2. Digite (trocando pelo IP do seu servidor):
   ```
   ssh root@123.45.67.89
   ```
3. Na primeira vez, vai aparecer uma pergunta tipo "Are you sure you want to
   continue connecting?" — digite `yes` e aperte Enter
4. Digite a senha que o provedor te deu (ao digitar, **nada aparece na tela**,
   isso é normal, é por segurança — só digite e aperte Enter)

**No Mac:**
1. Abra o programa **Terminal** (Spotlight → digite "Terminal")
2. Mesmos comandos acima

Se conectou certo, a tela vai mostrar algo como `root@nome-do-servidor:~#` —
isso significa que você está "dentro" do servidor agora. Todo comando que
você digitar dali em diante roda lá, não no seu computador.

### Passo 2.3 — Instalar os programas necessários no servidor

Cole este bloco inteiro de uma vez (pode colar com botão direito do mouse ou
Ctrl+Shift+V) e aperte Enter:

```bash
apt update && apt upgrade -y
apt install -y python3 python3-venv python3-pip git nginx certbot python3-certbot-nginx ufw dnsutils
```

**O que isso faz:** atualiza o sistema e instala: Python (a linguagem do
código), Git (para baixar o repositório), Nginx (o "porteiro" que recebe
visitantes do site), Certbot (o cadeado de segurança HTTPS) e um firewall.
Isso pode levar de 2 a 5 minutos.

### Passo 2.4 — Criar um usuário próprio para a aplicação
Por segurança, o site não deve rodar com o usuário `root` (que tem poder
total sobre o servidor). Cole:

```bash
adduser --system --group --home /var/www/cadebolsa cadebolsa
mkdir -p /var/log/cadebolsa
chown cadebolsa:cadebolsa /var/log/cadebolsa
```

### Passo 2.5 — Ativar o firewall

```bash
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable
```

Quando perguntar `Command may disrupt existing ssh connections. Proceed with operation (y|n)?`, digite `y` e Enter.

---

# ITEM 3 — Trazer o código para o servidor

### Passo 3.1 — Gerar uma "senha de acesso" do GitHub (token)
Como seu repositório é privado, o servidor precisa de uma autorização para
baixá-lo.

1. No navegador (no seu computador, não no servidor), acesse:
   `https://github.com/settings/tokens`
2. Clique em **Generate new token → Generate new token (classic)**
3. Em "Note", escreva `servidor-cadebolsa`
4. Em "Expiration", escolha `90 days` (ou "No expiration", se preferir não
   renovar depois)
5. Marque a caixa **repo** (dá acesso aos repositórios)
6. Clique em **Generate token**
7. **Copie o token gerado agora** — ele só aparece uma vez (é uma sequência
   tipo `ghp_xxxxxxxxxxxxxxxxxxxx`). Guarde em um bloco de notas temporário.

### Passo 3.2 — Clonar (baixar) o repositório no servidor

De volta no terminal conectado ao servidor:

```bash
cd /var/www
git clone https://github.com/SEU_USUARIO/cadebolsa.git
```

Quando pedir usuário e senha:
- **Username:** seu usuário do GitHub
- **Password:** cole o **token** que você gerou no passo anterior (não é sua senha normal do GitHub)

```bash
chown -R cadebolsa:cadebolsa /var/www/cadebolsa
cd cadebolsa
```

### Passo 3.3 — Criar o ambiente virtual e instalar as dependências

```bash
sudo -u cadebolsa python3 -m venv venv
sudo -u cadebolsa venv/bin/pip install --upgrade pip
sudo -u cadebolsa venv/bin/pip install -r requirements.txt
```

**O que isso faz:** cria um "ambiente isolado" só para este projeto (para não
bagunçar outras coisas do sistema) e instala as bibliotecas Python que o
código precisa. Pode levar 1-2 minutos.

### Passo 3.4 — Configurar a chave da API (Anthropic)

```bash
cp .env.example .env
nano .env
```

Isso abre um editor de texto simples dentro do terminal. Use as setas do
teclado para navegar. Apague o texto de exemplo depois de `ANTHROPIC_API_KEY=`
e cole sua chave real (a que você gerou em console.anthropic.com, conforme
te expliquei antes). Deve ficar assim:

```
ANTHROPIC_API_KEY=sk-ant-sua-chave-completa-aqui
```

Para salvar e sair do editor `nano`:
- Aperte `Ctrl + O` (letra O, de "output") e depois `Enter` (salva)
- Aperte `Ctrl + X` (sai do editor)

Depois, proteja o arquivo:

```bash
chown cadebolsa:cadebolsa .env
chmod 600 .env
```

### Passo 3.5 — Rodar o coletor pela primeira vez

Este comando faz o agente buscar as primeiras oportunidades:

```bash
sudo -u cadebolsa -H bash -c 'set -a; source /var/www/cadebolsa/.env; set +a; /var/www/cadebolsa/venv/bin/python /var/www/cadebolsa/agente_bolsas.py --max-queries 10'
```

Você vai ver mensagens tipo `[1/10] iniciação científica...` aparecendo — é o
agente pesquisando. Isso pode levar de 2 a 5 minutos. No final, confira se o
arquivo de dados foi criado:

```bash
cat /var/www/cadebolsa/data/oportunidades.json
```

Se aparecer um texto longo em formato de lista (JSON), funcionou.

---

# ITEM 4 — Subir a aplicação (Gunicorn + systemd)

O Gunicorn é o programa que efetivamente "liga" o site. O systemd é quem
garante que ele fique sempre ligado, e religue sozinho se o servidor reiniciar.

```bash
cp /var/www/cadebolsa/deploy/cadebolsa.service /etc/systemd/system/cadebolsa.service
systemctl daemon-reload
systemctl enable cadebolsa
systemctl start cadebolsa
systemctl status cadebolsa
```

O último comando mostra o status. Procure pela palavra **active (running)**
em verde. Para sair dessa tela de status, aperte a tecla `q`.

**Se der erro** (aparecer "failed" em vermelho), veja o motivo com:

```bash
journalctl -u cadebolsa -n 50 --no-pager
```

Leia as últimas linhas — geralmente indicam o problema (ex: erro no `.env`,
ou biblioteca faltando).

### Teste local
```bash
curl http://127.0.0.1:8000
```
Deve aparecer um bloco de código HTML na tela — é a página do site, ainda
"por dentro" do servidor (o navegador ainda não consegue acessar, isso vem
no próximo item).

---

# ITEM 5 — Configurar o Nginx

O Nginx recebe os pedidos que chegam pela internet (porta 80/443) e
repassa para o Gunicorn (que só escuta internamente, na porta 8000).

```bash
cp /var/www/cadebolsa/deploy/nginx_cadebolsa.conf /etc/nginx/sites-available/cadebolsa
ln -s /etc/nginx/sites-available/cadebolsa /etc/nginx/sites-enabled/
nginx -t
```

O comando `nginx -t` testa se a configuração está correta. Deve aparecer:
```
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

Se sim, aplique:

```bash
systemctl reload nginx
```

Neste momento, se você digitar o **IP do servidor** direto no navegador
(ex: `http://123.45.67.89`), o site já deve aparecer — mesmo antes do
domínio estar configurado.

---

# ITEM 6 — Apontar o domínio (DNS)

Como o domínio é `.com.br`, provavelmente está registrado no **registro.br**.

### Passo 6.1 — Acessar o painel do domínio
1. Acesse **https://registro.br** e faça login
2. Vá em **Meus domínios** → clique em `cadebolsa.com.br`
3. Procure a opção **DNS** (às vezes chamada de "Editar zona" ou "DNS Simplificado")

### Passo 6.2 — Criar os registros
Se o registro.br oferecer "DNS Simplificado" (mais fácil), procure o campo
para "Endereço IP do meu servidor (A)" e cole o IP do seu servidor ali —
isso já configura tanto `cadebolsa.com.br` quanto `www.cadebolsa.com.br`.

Se for pela edição manual de zona, crie dois registros:

| Tipo | Nome | Valor |
|---|---|---|
| A | @ | (IP do seu servidor) |
| A | www | (IP do seu servidor) |

Salve as alterações.

### Passo 6.3 — Esperar a propagação
Isso pode levar de 10 minutos a algumas horas. Para verificar se já
propagou, acesse **https://dnschecker.org**, digite `cadebolsa.com.br` e
veja se o IP mostrado bate com o do seu servidor em vários locais do mundo.

Ou, pelo terminal do servidor:
```bash
dig cadebolsa.com.br +short
```
Quando o número que aparece for igual ao IP do seu servidor, propagou.

---

# ITEM 7 — Ativar HTTPS (certificado grátis)

**Só faça isso depois que o Item 6 já tiver propagado**, senão vai dar erro.

No terminal do servidor:

```bash
certbot --nginx -d cadebolsa.com.br -d www.cadebolsa.com.br
```

O Certbot vai perguntar:
- Um e-mail (para avisos sobre o certificado — pode ser o seu pessoal)
- Se aceita os termos — digite `Y`
- Se quer compartilhar seu e-mail com a fundação parceira — pode digitar `N`

No final, ele mostra uma mensagem de sucesso e configura tudo sozinho,
inclusive a renovação automática (o certificado se renova sozinho a cada 90
dias, você não precisa fazer nada).

Teste acessando **https://cadebolsa.com.br** no navegador — deve aparecer o
cadeado de segurança ao lado do endereço.

---

# ITEM 8 — Agendar a atualização automática

Isso faz o agente buscar novas oportunidades sozinho, todo dia, sem você
precisar entrar no servidor.

```bash
cp /var/www/cadebolsa/deploy/cadebolsa-scraper.service /etc/systemd/system/
cp /var/www/cadebolsa/deploy/cadebolsa-scraper.timer /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now cadebolsa-scraper.timer
```

Para confirmar que está agendado:
```bash
systemctl list-timers | grep cadebolsa
```
Deve mostrar a próxima data/hora em que ele vai rodar (por padrão, 06:00
todo dia).

### Para rodar manualmente a qualquer momento (sem esperar o horário):
```bash
systemctl start cadebolsa-scraper.service
```
Depois de alguns minutos, atualize a página do site no navegador — as
oportunidades novas já vão aparecer automaticamente (o site lê o arquivo de
dados a cada visita, não precisa reiniciar nada).

---

# Checklist final

- [ ] Código no GitHub (repositório `cadebolsa`)
- [ ] Servidor contratado, com Ubuntu, e programas instalados
- [ ] Consegue conectar via SSH
- [ ] Repositório clonado dentro do servidor em `/var/www/cadebolsa`
- [ ] Arquivo `.env` criado com a chave da API
- [ ] Coletor rodado ao menos uma vez (`data/oportunidades.json` existe)
- [ ] `systemctl status cadebolsa` mostra "active (running)"
- [ ] `http://SEU_IP` já mostra o site no navegador
- [ ] DNS do domínio apontando para o IP do servidor (`dig` confirma)
- [ ] `https://cadebolsa.com.br` funcionando com cadeado de segurança
- [ ] `systemctl list-timers` mostra o agendamento diário ativo

# Se algo travar
- Se você fechar o terminal no meio do processo, é só conectar de novo com
  o mesmo comando `ssh root@SEU_IP` e continuar de onde parou.
- Qualquer comando que der erro, copie a mensagem de erro e me envie — eu te
  ajudo a interpretar.
- Nenhum passo aqui é destrutivo/irreversível: se algo sair errado, dá para
  refazer o passo específico sem prejudicar o resto.

# Cadê Bolsa? — Publicando via GitHub Pages (sem servidor próprio)

Esta é uma rota alternativa ao manual anterior (VPS/Ubuntu). Aqui, o próprio
GitHub busca as oportunidades e publica o site automaticamente, todo dia, de
graça. Você não precisa de servidor, terminal, SSH, Nginx nem certbot.

**Como funciona:** um "robô" do GitHub (chamado GitHub Actions) acorda todo
dia, roda o `agente_bolsas.py` (que busca as oportunidades reais na web),
gera a página HTML pronta com o `build_site.py`, e publica no GitHub Pages
— um serviço de hospedagem gratuito do próprio GitHub.

---

## Passo 1 — Atualizar os arquivos do repositório

Se você já tinha criado o repositório `cadebolsa` (Item 1 do manual
anterior), baixe os arquivos novos que te enviei agora (`build_site.py`,
a pasta `templates/index_static.html`, a pasta `.github/workflows/` e o
`requirements.txt` atualizado) e coloque dentro da mesma pasta do
repositório no seu computador, substituindo o que for necessário.

No GitHub Desktop:
1. Copie os arquivos novos para dentro da pasta do repositório
2. Ele vai detectar as mudanças automaticamente
3. Escreva um resumo (ex: "Adiciona publicação via GitHub Pages")
4. Clique em **Commit to main**
5. Clique em **Push origin** (bota que aparece no topo)

## Passo 2 — Guardar sua chave da API como "Secret" (segredo) do GitHub

Isso substitui o arquivo `.env` que usaríamos num servidor — aqui a chave
fica guardada de forma criptografada, dentro do próprio GitHub.

1. No site do GitHub, abra seu repositório `cadebolsa`
2. Clique em **Settings** (aba no topo do repositório)
3. No menu à esquerda, clique em **Secrets and variables → Actions**
4. Clique em **New repository secret**
5. Em **Name**, escreva exatamente: `ANTHROPIC_API_KEY`
6. Em **Secret**, cole sua chave (a que começa com `sk-ant-...`)
7. Clique em **Add secret**

## Passo 3 — Habilitar o GitHub Pages

1. Ainda em **Settings**, clique em **Pages** no menu à esquerda
2. Em **Source** (ou "Build and deployment"), selecione **GitHub Actions**
   (não escolha "Deploy from a branch")

## Passo 4 — Rodar o robô pela primeira vez (teste manual)

1. No repositório, clique na aba **Actions** (no topo)
2. Na lista à esquerda, clique em **Atualizar oportunidades e publicar site**
3. Clique no botão **Run workflow** (à direita) → **Run workflow** de novo para confirmar
4. Espere alguns minutos — clique no item que aparece na lista para ver o
   progresso ao vivo (uma bolinha amarela girando = rodando; verde = deu
   certo; vermelho = deu erro)

Se der erro (bolinha vermelha), clique em cima do item e depois em cada
etapa para ler a mensagem de erro. O erro mais comum é o nome do "Secret"
escrito diferente de `ANTHROPIC_API_KEY` — confira o Passo 2.

Quando terminar com sucesso, seu site já estará no ar em um endereço tipo:
```
https://SEU_USUARIO.github.io/cadebolsa/
```
Você pode conferir esse endereço em **Settings → Pages**, no topo da página.

## Passo 5 — Configurar o domínio próprio (cadebolsa.com.br)

1. Em **Settings → Pages**, procure o campo **Custom domain**
2. Digite `cadebolsa.com.br` e clique em **Save**
   (o GitHub cria sozinho um arquivo de configuração no seu repositório)

3. Agora você precisa apontar o DNS do domínio para o GitHub. Isso é feito
   em **dois lugares diferentes**, dependendo de qual parte do endereço:

   **Para `cadebolsa.com.br` (sem "www"), crie 4 registros tipo A:**

   | Tipo | Nome | Valor |
   |---|---|---|
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |

   **Para `www.cadebolsa.com.br`, crie 1 registro tipo CNAME:**

   | Tipo | Nome | Valor |
   |---|---|---|
   | CNAME | www | SEU_USUARIO.github.io |

   Esses registros são criados no painel de DNS de onde o domínio está
   registrado — no seu caso, provavelmente no **Zone Editor do cPanel**
   (já que o domínio parece estar vinculado a essa hospedagem) ou no
   **registro.br**, dependendo de onde estão configurados os nameservers.
   Se não tiver certeza, me diga e eu te ajudo a identificar.

4. Espere a propagação (minutos a poucas horas) — pode conferir em
   **https://dnschecker.org**, digitando `cadebolsa.com.br`

5. Volte em **Settings → Pages** no GitHub: quando o domínio for
   reconhecido, vai aparecer uma marcação verde e a opção **Enforce HTTPS**
   ficará disponível — marque essa caixa (o certificado de segurança é
   emitido automaticamente pelo GitHub, sem você fazer nada).

## Pronto!

A partir daqui, todo dia às 06:00 (horário de Brasília) o robô roda sozinho:
busca novas oportunidades, atualiza o site, publica — sem você precisar
fazer nada. Para forçar uma atualização fora do horário, repita o Passo 4
(Run workflow) a qualquer momento.

---

## O que essa rota NÃO tem (comparado ao VPS)
- Não dá pra rodar código sob demanda em tempo real (ex: um botão que busca
  "na hora" — só a atualização diária agendada)
- Os minutos de execução do GitHub Actions são limitados no plano gratuito
  (mas uma rodada diária curta como essa fica bem dentro do limite)
- Se no futuro você quiser recursos mais avançados (ex: usuários cadastrados,
  favoritar oportunidades, notificações por e-mail), aí sim um VPS com
  banco de dados de verdade passa a fazer mais sentido — mas para o site
  como está hoje, o GitHub Pages resolve completamente.

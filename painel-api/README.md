# painel-api — API do painel do blog (Cloudflare Worker)

Usuários com login e senha próprios (hash PBKDF2), sessão assinada (12 h), recuperação de senha por e-mail (Resend)
e gravação dos artigos no repositório do site via API do GitHub (token guardado só como segredo do Worker).

## Publicar
```
cd painel-api
npx wrangler@3 kv namespace create PAINEL        # copiar o id para wrangler.toml (id e preview_id)
npx wrangler@3 deploy
npx wrangler@3 secret put GITHUB_TOKEN           # token fine-grained do repositório (Contents: read/write)
openssl rand -hex 32 | npx wrangler@3 secret put JWT_SECRET
npx wrangler@3 secret put RESEND_API_KEY         # chave do Resend (domínio de envio verificado)
```
Depois, criar o primeiro administrador (sem senha; ele define pelo link):
```
npx wrangler@3 kv key put --binding PAINEL "user:nexus" '{"login":"nexus","nome":"Nexus Digital","email":"nexusdigitalgrp@gmail.com","papel":"admin","criado":0,"versao":1}'
```
e pedir o link de definição de senha em `/admin/` → "Esqueci a senha" (ou criar os demais usuários pelo painel, logado como admin).

## Rotas
POST /entrar · POST /recuperar · POST /redefinir · GET /redefinir?token= · GET /eu · POST /senha · POST /email ·
PUT /post · GET /post?slug= · DELETE /post/:slug · GET|POST /usuarios · POST|DELETE /usuarios/:login

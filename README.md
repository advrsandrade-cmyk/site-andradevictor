# Andrade e Victor Advogados Associados — site (proposta Nexus Digital Group, 2026)

Site estático gerado por `build.py` a partir de `src/` (fontes, CSS, JS e imagens próprias).

- `python3 build.py` → `dist/` com links `pagina.html` (prévia/artefato)
- `python3 build.py --limpo` → `dist/` com links limpos (`/direito-penal/`) para Cloudflare Pages
- `python3 scripts/preview.py` → `preview/` (casca com modos Desktop/Tablet/Celular/Livre) para publicar como artefato
- `scripts/check-links.mjs`, `check-nav.mjs`, `check-responsive.mjs`, `check-titulos.mjs` → verificações (Playwright)

Páginas: início, áreas de atuação (penal, previdenciário, tributário, administrativo), sócios, o escritório, contato, privacidade e 404.

Marca: logos extraídas das artes oficiais do Instagram (apenas o fundo removido, nada redesenhado); variante escura só para fundos claros.
Fotos reais dos sócios (Linktree/Instagram) em alta resolução (FSRCNN x2) com versões 1x/2x.

Dados confirmados pelo cartão de visita do escritório (out/2026): endereço Rua Dr. Bertino Passos, 21, Centro, Amargosa/BA; e-mail andradevictoradvogados@gmail.com; OAB/BA 57.064 (Ricardo) e 55.402 (Jefferson); telefones. Horário confirmado pelo cliente: seg–sex 9h–17h (a ficha do Google ainda mostra 8h–18h — vale atualizar lá).

## Publicação (no ar desde 20/10/2026)

- Hospedagem: GitHub Pages (grátis), repositório do cliente `advrsandrade-cmyk/site-andradevictor`, branch `main`, pasta `docs/` (= `python3 build.py --limpo` + `CNAME` + `.nojekyll`).
- Domínio: https://andradevictoradvogados.com.br (HTTPS forçado; `www` redireciona para o apex). DNS no UOL: 4 registros A (185.199.108/109/110/111.153) + CNAME `www` → `advrsandrade-cmyk.github.io`.
- `.online`: ainda não apontado (decisão do cliente). Existe o repositório `redirecionamento-online` com um index.html de redirecionamento, sem uso.
- Para atualizar: editar aqui → publicar a prévia (artefato) com `src/build.py` → no Codespace do repositório, baixar o `build.py` novo, `python3 build.py --limpo`, copiar `dist/` para `docs/`, commit e push. O GitHub Pages republica em ~1 min.

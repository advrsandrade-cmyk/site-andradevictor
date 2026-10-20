# Andrade e Victor Advogados Associados — site (proposta Nexus Digital Group, 2026)

Site estático gerado por `build.py` a partir de `src/` (fontes, CSS, JS e imagens próprias).

- `python3 build.py` → `dist/` com links `pagina.html` (prévia/artefato)
- `python3 build.py --limpo` → `dist/` com links limpos (`/direito-penal/`) para Cloudflare Pages
- `python3 scripts/preview.py` → `preview/` (casca com modos Desktop/Tablet/Celular/Livre) para publicar como artefato
- `scripts/check-links.mjs`, `check-nav.mjs`, `check-responsive.mjs`, `check-titulos.mjs` → verificações (Playwright)

Páginas: início, áreas de atuação (penal, previdenciário, tributário, administrativo), sócios, o escritório, contato, privacidade e 404.

Marca: logos extraídas das artes oficiais do Instagram (apenas o fundo removido, nada redesenhado); variante escura só para fundos claros.
Fotos reais dos sócios (Linktree/Instagram) em alta resolução (FSRCNN x2) com versões 1x/2x.

Itens a CONFIRMAR com o cliente: endereço (Linktree: Rua Conselheiro Dantas, 488; Google: Av. Dr. Abelardo Velloso, 488), número da OAB de Jefferson Victor, horário confirmado pelo cliente: seg–sex 9h–17h (Google ainda mostra 8h–18h), domínio final.

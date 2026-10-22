#!/usr/bin/env python3
"""Gera o site estático de Andrade e Victor Advogados Associados (Amargosa, BA) em dist/ a partir de src/.
Uso: python3 build.py            → links como arquivo.html (prévia/artefato)
     python3 build.py --limpo    → links limpos (/direito-penal/) para Cloudflare Pages

Proposta Nexus Digital Group (19/10/2026). Conteúdo levantado nas publicações do escritório
(@andradevictoradv, Linktree, perfis dos sócios e ficha do Google). Dados de contato e OAB conferidos no cartão de visita (out/2026). Itens marcados CONFIRMAR precisam
de validação com o cliente. Publicidade dentro do Provimento 205/2021 da OAB: informativa, sem promessa
de resultado, sem preços, sem depoimentos de clientes.
"""
import pathlib, shutil, sys, html, json
from urllib.parse import quote

RAIZ = pathlib.Path(__file__).parent
SRC = RAIZ / "src"
DIST = RAIZ / "dist"
LIMPO = "--limpo" in sys.argv

NOME = "Andrade e Victor Advogados Associados"
NOME_CURTO = "Andrade e Victor"
SITE = "https://andradevictoradvogados.com.br"  # o www redireciona para este endereço (GitHub Pages); canônico sem www
INSTAGRAM = "https://www.instagram.com/andradevictoradv/"
ENDERECO = "Rua Dr. Bertino Passos, 21 — Centro"  # conforme o cartão de visita do escritório
EMAIL = "andradevictoradvogados@gmail.com"  # cartão de visita
CIDADE = "Amargosa, BA · CEP 45300-000"
HORARIO = "Segunda a sexta, 9h às 17h"
HORARIO_CURTO = "Seg. a sex. 9h–17h"
MAPS = "https://www.google.com/maps/search/?api=1&query=" + quote("Rua Dr. Bertino Passos, 21, Centro, Amargosa - BA")
WHATSAPP_TEXTO = "Olá! Vim pelo site do escritório Andrade e Victor e gostaria de falar com um advogado."

SOCIOS = {
    "jefferson": {
        "nome": "Jefferson Victor",
        "tratamento": "Dr. Jefferson Victor",
        "cargo": "Advogado · Sócio",
        "oab": "OAB/BA 55.402",
        "cel": "(75) 99232-0286",
        "whats": "5575992320286",
        "instagram": "https://www.instagram.com/jv4669/",
        "insta_user": "@jv4669",
        "areas": ["penal", "previdenciario"],
        "foco": "Direito Penal e Direito Previdenciário",
        "resumo": "Quase dez anos de advocacia com ênfase na defesa criminal e nos direitos previdenciários. Ex-Juiz Leigo e ex-Conciliador do Tribunal de Justiça da Bahia, pós-graduado em Ciências Criminais pela PUC Minas.",
        "bio": [
            "Jefferson Victor atua há quase dez anos na advocacia, com atuação em diversas áreas do Direito e ênfase na Advocacia Criminal e no Direito Previdenciário, além de experiência em Direito Administrativo.",
            "Antes de se dedicar integralmente à advocacia privada, foi Juiz Leigo e Conciliador do Tribunal de Justiça do Estado da Bahia (TJBA), vivência que trouxe ao escritório uma leitura prática de como os processos são conduzidos e decididos.",
            "É pós-graduado em Ciências Criminais pela Pontifícia Universidade Católica de Minas Gerais (PUC Minas). Atua na defesa de direitos e garantias fundamentais, com destaque para Habeas Corpus e Mandado de Segurança, e na condução de demandas judiciais e administrativas.",
        ],
        "credenciais": [
            "Quase 10 anos de experiência profissional",
            "Pós-graduado em Ciências Criminais — PUC Minas",
            "Ex-Juiz Leigo e ex-Conciliador do TJBA",
            "Atuação em Habeas Corpus e Mandado de Segurança",
        ],
    },
    "ricardo": {
        "nome": "Ricardo Andrade",
        "tratamento": "Dr. Ricardo Andrade",
        "cargo": "Advogado · Sócio",
        "oab": "OAB/BA 57.064",
        "cel": "(75) 99864-9163",
        "whats": "5575998649163",
        "areas": ["administrativo", "civil", "tributario"],
        "foco": "Direito Administrativo, Civil e Tributário",
        "resumo": "Dez anos de advocacia e oito anos como Procurador Municipal. Pós-graduado em Direito Administrativo, Direito Criminal e Direito Tributário, com atuação em tribunais superiores e atendimento online para todo o Brasil.",
        "bio": [
            "Ricardo Andrade é advogado há dez anos, com atuação concentrada no Direito Tributário, no Direito Administrativo e no Direito Civil — áreas em que uniu a formação acadêmica à prática diária na gestão pública e no atendimento a pessoas e empresas.",
            "Foi Procurador Municipal por oito anos, contribuindo com a gestão pública e a defesa dos interesses municipais. Essa experiência dá ao escritório conhecimento de dentro sobre licitações, contratos, servidores, tributos municipais e processos administrativos.",
            "É pós-graduado em Direito Tributário pelo Instituto Brasileiro de Direito, em Direito Administrativo pela Escola Brasileira de Direito e em Direito Criminal pela PUC Minas. Além da advocacia privada, tem vasta atuação em tribunais superiores.",
        ],
        "credenciais": [
            "10 anos de experiência como advogado",
            "Procurador Municipal por 8 anos",
            "Pós-graduado em Direito Administrativo, Criminal e Tributário",
            "Atuação em tribunais superiores",
        ],
    },
}
ONLINE = "Atendimento online para todo o Brasil"
ONLINE_ITENS = [
    "Consulta por videochamada ou WhatsApp, de qualquer cidade do Brasil",
    "Documentos e procuração enviados e assinados digitalmente",
    "Processos eletrônicos acompanhados em todas as instâncias",
    "Reunião presencial no escritório, com hora marcada, quando preferir",
]

# Áreas de atuação: (slug, ícone, nome, nome curto, responsável, resumo, lista de atuação, hero lead, faq)
AREAS = [
    ("administrativo", "predio", "Direito Administrativo", "Administrativo", "ricardo",
     "Servidores públicos, concursos, licitações, contratos e processos administrativos, com atuação em Mandado de Segurança.",
     ["Servidores públicos: direitos, nomeações e processos disciplinares", "Concursos públicos e eliminações indevidas", "Licitações e contratos administrativos", "Improbidade administrativa e Tribunal de Contas", "Mandado de Segurança contra atos do poder público"],
     "Oito anos como Procurador Municipal deram ao escritório a visão de dentro da administração pública — o que faz diferença ao defender servidores, candidatos, empresas e gestores. Atendimento online para todo o Brasil.",
     [("Fui eliminado de um concurso. Posso recorrer?", "Sim, pela via administrativa e, se for o caso, judicial — inclusive com Mandado de Segurança quando houver ilegalidade evidente."),
      ("Atendem prefeituras e gestores?", "Sim, com consultoria e defesa em licitações, contratos, Tribunal de Contas e improbidade administrativa."),
      ("O que é Mandado de Segurança?", "É a ação rápida para proteger direito líquido e certo violado por autoridade pública. Tem prazo de 120 dias — não deixe para depois.")]),
    ("civil", "contrato", "Direito Civil", "Civil", "ricardo",
     "Contratos, indenizações, cobranças, família, sucessões e questões imobiliárias, com consultoria preventiva e atuação judicial.",
     ["Contratos: elaboração, revisão e descumprimento", "Indenizações por danos materiais e morais", "Cobranças, dívidas e negociação de acordos", "Família e sucessões: divórcio, pensão, inventário e testamento", "Imobiliário: compra e venda, locação, posse e usucapião"],
     "O Direito Civil está nas decisões mais importantes da vida: um contrato, um imóvel, uma herança, um prejuízo a reparar. Orientação clara e atendimento online para todo o Brasil, por videochamada e WhatsApp.",
     [("Vocês atendem clientes de outras cidades e estados?", "Sim. O atendimento em Direito Civil é feito online para todo o Brasil: consulta por videochamada ou WhatsApp, documentos e procuração assinados digitalmente e processo eletrônico acompanhado onde quer que ele tramite."),
      ("Preciso de advogado para fazer ou revisar um contrato?", "É o melhor momento para ter um. Um contrato bem redigido evita a maior parte dos conflitos — e, se o problema já existe, analisamos as cláusulas e o caminho para resolvê-lo."),
      ("Como funciona um inventário?", "Pode ser feito em cartório, quando há acordo entre os herdeiros e todos são maiores e capazes, ou pela via judicial. Explicamos os custos, prazos e documentos logo na primeira conversa.")]),
    ("penal", "balanca", "Direito Penal", "Penal", "jefferson",
     "Defesa técnica em inquéritos, processos criminais e execução penal, com atuação em Habeas Corpus e recursos.",
     ["Defesa em inquéritos policiais e ações penais", "Audiências de custódia e pedidos de liberdade", "Habeas Corpus e recursos aos tribunais", "Execução penal: progressão, remição e livramento", "Tribunal do Júri e crimes contra a vida"],
     "Uma acusação criminal exige resposta rápida, técnica e serena. Atuamos desde a delegacia até os tribunais superiores, com a defesa dos direitos e garantias fundamentais como prioridade — com atendimento online para todo o Brasil.",
     [("Fui intimado para depor na delegacia. Preciso de advogado?", "Sim — é o momento mais importante para orientar o que dizer e preservar seus direitos. Entre em contato antes de comparecer."),
      ("O que é Habeas Corpus?", "É a ação que protege a liberdade de locomoção contra prisão ou ameaça ilegal. Avaliamos o cabimento com urgência em cada caso."),
      ("Vocês atuam na execução da pena?", "Sim: progressão de regime, remição, livramento condicional e demais incidentes da execução penal.")]),
    ("previdenciario", "escudo", "Direito Previdenciário", "Previdenciário", "jefferson",
     "Aposentadorias, benefícios por incapacidade, pensões e revisões junto ao INSS, na via administrativa e judicial.",
     ["Aposentadoria por idade, tempo de contribuição e especial", "Auxílio por incapacidade e aposentadoria por invalidez", "BPC/LOAS para idosos e pessoas com deficiência", "Pensão por morte e salário-maternidade", "Revisão de benefícios e recursos contra negativas do INSS"],
     "Benefício negado, atrasado ou calculado errado tem solução. Analisamos seu histórico contributivo e conduzimos o pedido ou a revisão no INSS e, quando necessário, na Justiça — tudo online, de qualquer lugar do Brasil.",
     [("Meu benefício foi negado pelo INSS. O que fazer?", "A negativa pode ser revista por recurso administrativo ou ação judicial. Traga a carta de indeferimento e os documentos para avaliarmos o melhor caminho."),
      ("Quais documentos preciso enviar?", "Documento de identidade, CPF, carteira de trabalho, carnês ou guias de contribuição, laudos médicos (se houver) e a senha do Meu INSS. Tudo pode ser enviado pelo WhatsApp ou e-mail, sem precisar ir ao escritório."),
      ("Quanto tempo leva?", "Depende do tipo de pedido e da via escolhida. Explicamos os prazos esperados logo na primeira análise.")]),
    ("tributario", "colunas", "Direito Tributário", "Tributário", "ricardo",
     "Defesa em execuções fiscais, consultoria e planejamento tributário para empresas, produtores e pessoas físicas.",
     ["Defesa em execuções fiscais e autos de infração", "Impugnações e recursos administrativos", "Restituição e compensação de tributos pagos a maior", "Parcelamentos e regularização fiscal", "Consultoria e planejamento tributário"],
     "Tributos cobrados a mais, autuações e dívidas fiscais pesam no caixa. Atuamos na defesa e na organização tributária com a experiência de quem conhece a administração pública por dentro, com atendimento online para empresas e pessoas de todo o Brasil.",
     [("Recebi uma execução fiscal. Posso me defender?", "Sim. Há prazos curtos para embargos ou exceção de pré-executividade; procure orientação assim que for citado."),
      ("Vocês atendem empresas e produtores rurais?", "Sim, pessoas físicas e jurídicas de todo o Brasil, inclusive produtores rurais e comerciantes, com atendimento online."),
      ("É possível recuperar tributos pagos indevidamente?", "Em muitos casos, sim, dentro do prazo legal. Fazemos o levantamento e orientamos sobre restituição ou compensação.")]),
]
AREA = {a[0]: a for a in AREAS}

# Regra Nexus (menus): itens com mais de uma palavra em Título Com Maiúsculas (ex.: "O Escritório", "Áreas de Atuação")
MENU = [
    ("index", "Início"),
    ("areas", "Áreas de Atuação"),  # abre submenu
    ("socios", "Sócios"),
    ("escritorio", "O Escritório"),
    ("contato", "Contato"),
]
SUBMENU = [(a[0], a[2]) for a in AREAS]


def url(slug):
    if slug == "index":
        return "/" if LIMPO else "index.html"
    return f"/{slug}/" if LIMPO else f"{slug}.html"


def wa(texto=None, socio=None):
    num = SOCIOS[socio]["whats"] if socio else SOCIOS["ricardo"]["whats"]
    return f"https://wa.me/{num}?text={quote(texto or WHATSAPP_TEXTO)}"


def tel(numero):
    return "tel:+55" + "".join(c for c in numero if c.isdigit())


I = {
    "balanca": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18M5 21h14M12 6l6 1M12 6L6 7"/><path d="M3.5 14 6 7l2.5 7a2.5 2.5 0 0 1-5 0zM15.5 14 18 7l2.5 7a2.5 2.5 0 0 1-5 0z"/></svg>',
    "escudo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/></svg>',
    "colunas": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M4 10h16M12 3 3 8h18zM6 10v8M10 10v8M14 10v8M18 10v8"/></svg>',
    "predio": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16M16 9h3a1 1 0 0 1 1 1v11M3 21h18M8 7h4M8 11h4M8 15h4"/></svg>',
    "contrato": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 11h7M9 14.5h4"/><path d="M9 18.5c1-1.2 1.6-.4 2.2 0s1.4.8 2.3-.4"/></svg>',
    "video": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3z"/></svg>',
    "brasil": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M8.5 12.5l2.5 2.5 4.5-5"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "whats": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.6 1.1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.5-.3z"/></svg>',
    "map": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s6-5.3 6-10a6 6 0 1 0-12 0c0 4.7 6 10 6 10z"/><circle cx="12" cy="11" r="2.2"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>',
    "insta": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
    "chev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>',
    "grad": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M2 9l10-4 10 4-10 4z"/><path d="M6 11v5c0 1.5 3 3 6 3s6-1.5 6-3v-5M22 9v6"/></svg>',
    "martelo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4l6 6M11 7l6 6M3 21l9-9M12 3l-4 4 2 2 4-4zM20 11l-4 4 2 2 4-4z"/></svg>',
    "maos": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l4-4 4 3 3-3 4 4-4 5-3-2-3 3-5-6z"/><path d="M8 17l2 2M12 14l2 2"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M9.5 12h7M9.5 16h7"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/></svg>',
    "alvo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>',
    "coracao": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg>',
}


# ---------------------------------------------------------------- componentes
def msg_socio(k):
    return f"Olá, {SOCIOS[k]['tratamento']}! Vim pelo site do escritório Andrade e Victor e gostaria de uma orientação."


def btn_whats(texto="Falar no WhatsApp", classe="btn btn-dourado", msg=None, socio=None, grande=False):
    """Botão de um sócio específico vai direto ao WhatsApp dele (mensagem com o nome).
    Botão genérico (sem sócio) abre o painel "Falar com quem?" (#falar), que escolhe o advogado."""
    c = classe + (" btn-grande" if grande else "")
    if socio is None:
        return f'<a class="{c}" href="#falar" data-wa-escolha aria-haspopup="dialog" aria-controls="falar">{I["whats"]}<span>{texto}</span></a>'
    return f'<a class="{c}" href="{wa(msg or msg_socio(socio), socio)}" target="_blank" rel="noopener noreferrer">{I["whats"]}<span>{texto}</span></a>'


def logo_img(clara=True, classe=""):
    base = "logo-av" if clara else "logo-av-escura"
    return f'<img class="{classe}" src="assets/img/{base}.png" srcset="assets/img/{base}.png 1x, assets/img/{base}@2x.png 2x" alt="{NOME}" width="488" height="171">'


def cabecalho(atual):
    def item(s, n):
        if s == "areas":
            ativo = atual in AREA or atual == "areas"
            subs = "".join(f'<a href="{url(x)}"{" aria-current=\"page\"" if x == atual else ""}>{I["arrow"]}{y}</a>' for x, y in SUBMENU)
            return f'''<div class="tem-sub{" ativo" if ativo else ""}">
        <button type="button" class="sub-btn" aria-expanded="false" aria-haspopup="true" aria-controls="sub-areas">{n} {I["chev"]}</button>
        <div class="submenu" id="sub-areas">{subs}<a class="sub-todos" href="{url("areas")}">Todas as Áreas {I["arrow"]}</a></div>
      </div>'''
        return f'<a href="{url(s)}"{" aria-current=\"page\"" if s == atual else ""}>{n}</a>'

    itens = "".join(item(s, n) for s, n in MENU)
    mob = "".join(
        (f'<details{" open" if atual in AREA or atual == "areas" else ""}><summary>{n} {I["chev"]}</summary>' + "".join(f'<a href="{url(x)}"{" aria-current=\"page\"" if x == atual else ""}>{y}</a>' for x, y in SUBMENU) + f'<a href="{url("areas")}">Todas as Áreas</a></details>')
        if s == "areas" else f'<a href="{url(s)}"{" aria-current=\"page\"" if s == atual else ""}>{n}</a>'
        for s, n in MENU
    )
    r, j = SOCIOS["ricardo"], SOCIOS["jefferson"]
    return f'''<a class="pular" href="#conteudo">Ir para o conteúdo</a>
<div class="faixa-topo">
  <div class="wrap">
    <span>{I["clock"]} {HORARIO_CURTO}</span>
    <span class="faixa-end">{I["video"]} {ONLINE}</span>
    <a href="{wa(None, "ricardo")}" target="_blank" rel="noopener noreferrer">{I["whats"]} {r["cel"]}</a>
    <a href="{wa(None, "jefferson")}" target="_blank" rel="noopener noreferrer">{I["whats"]} {j["cel"]}</a>
  </div>
</div>
<header class="topo">
  <div class="wrap">
    <a class="logo" href="{url("index")}" aria-label="{NOME} — página inicial">{logo_img(True)}</a>
    <nav class="nav" aria-label="Principal">{itens}</nav>
    <div class="acoes">
      {btn_whats("Fale conosco", "btn btn-dourado btn-topo")}
      <button class="hamb" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="menu-mobile"><span></span></button>
    </div>
  </div>
</header>
<nav id="menu-mobile" class="menu-mobile" aria-label="Menu">
  <div class="menu-mobile-lista">{mob}</div>
  <div class="menu-mobile-acoes">{btn_whats(f"WhatsApp · {r['nome']}", "btn btn-dourado", socio="ricardo")}{btn_whats(f"WhatsApp · {j['nome']}", "btn btn-contorno", socio="jefferson")}</div>
</nav>
'''


def flutuante():
    return f'<a class="whats-flutuante" href="#falar" data-wa-escolha aria-haspopup="dialog" aria-controls="falar" aria-label="Falar no WhatsApp">{I["whats"]}<span>Fale com um advogado</span></a>'


def painel_falar():
    """Painel de escolha do advogado: abre pelos botões genéricos de WhatsApp (sem JS, abre por #falar)."""
    def opcao(k):
        s = SOCIOS[k]
        areas = " · ".join(AREA[a][2].replace("Direito ", "") for a in s["areas"])
        return (f'<a class="wa-opcao" href="{wa(msg_socio(k), k)}" target="_blank" rel="noopener noreferrer">'
                f'<img src="assets/img/socio-{k}-q.jpg" srcset="assets/img/socio-{k}-q.jpg 1x, assets/img/socio-{k}-q@2x.jpg 2x" alt="" width="450" height="450" loading="lazy" decoding="async">'
                f'<span class="wa-opcao-txt"><b>{s["tratamento"]}</b><small>Direito {areas}</small></span><span class="wa-ir" aria-hidden="true">{I["whats"]}</span></a>')
    return f'''<div class="wa-fundo" id="falar-fundo" hidden></div>
<div class="wa-escolha" id="falar" role="dialog" aria-modal="true" aria-labelledby="falar-titulo" hidden>
  <div class="wa-cab"><strong id="falar-titulo">Falar com quem?</strong><a class="wa-fechar" href="#" aria-label="Fechar">×</a></div>
  <p class="wa-sub">Escolha o advogado e a conversa abre no WhatsApp dele.</p>
  {opcao("ricardo")}{opcao("jefferson")}
  <p class="wa-nota">Atendimento online para todo o Brasil · {HORARIO_CURTO}</p>
</div>'''


def rodape():
    r, j = SOCIOS["ricardo"], SOCIOS["jefferson"]
    JS_V = versao_asset("assets/js/site.js")
    return f'''<footer class="rodape">
  <div class="wrap">
    <div class="rodape-grade">
      <div class="rodape-marca">
        <a class="logo" href="{url("index")}" aria-label="{NOME}">{logo_img(True)}</a>
        <p>Advocacia nas áreas administrativa, civil, penal, previdenciária e tributária. Atendimento online para todo o Brasil e presencial no escritório. Direito claro, acessível e humano.</p>
        <div class="sociais"><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">{I["insta"]} @andradevictoradv</a><a href="{j["instagram"]}" target="_blank" rel="noopener noreferrer">{I["insta"]} {j["insta_user"]} · Jefferson</a></div>
      </div>
      <div>
        <h4>Áreas de atuação</h4>
        <ul>{"".join(f'<li><a href="{url(a[0])}">{a[2]}</a></li>' for a in AREAS)}</ul>
      </div>
      <div class="rodape-nav-mobile">
        <h4>Navegação</h4>
        <ul><li><a href="{url("index")}">Início</a></li><li><a href="{url("socios")}">Sócios</a></li><li><a href="{url("escritorio")}">O escritório</a></li><li><a href="{url("contato")}">Contato</a></li><li><a href="{url("privacidade")}">Privacidade</a></li></ul>
      </div>
      <div>
        <h4>Escritório</h4>
        <ul class="lista-contato">
          <li>{I["map"]}<span>{ENDERECO}<br>{CIDADE}</span></li>
          <li>{I["clock"]}<span>{HORARIO}</span></li>
          <li>{I["video"]}<span>{ONLINE}</span></li>
          <li>{I["mail"]}<span><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
        </ul>
      </div>
      <div>
        <h4>Atendimento</h4>
        <ul class="lista-contato">
          <li>{I["whats"]}<span><b>{r["nome"]}</b><br><a href="{wa(None, "ricardo")}" target="_blank" rel="noopener noreferrer">{r["cel"]}</a></span></li>
          <li>{I["whats"]}<span><b>{j["nome"]}</b><br><a href="{wa(None, "jefferson")}" target="_blank" rel="noopener noreferrer">{j["cel"]}</a></span></li>
        </ul>
      </div>
    </div>
    <div class="rodape-acoes-mobile">{btn_whats(f"WhatsApp · {r['nome']}", "btn btn-dourado", socio="ricardo")}{btn_whats(f"WhatsApp · {j['nome']}", "btn btn-contorno", socio="jefferson")}</div>
    <div class="rodape-base">
      <span>© <span data-ano>2026</span> {NOME}. <a href="{url("privacidade")}">Privacidade</a></span>
      <span class="nota">Site de caráter informativo, nos termos do Código de Ética e Disciplina da OAB e do Provimento 205/2021. Não substitui a consulta com um advogado.</span>
    </div>
  </div>
</footer>
{flutuante()}
{painel_falar()}
<script src="assets/js/site.js?v={JS_V}"></script>
'''


def canonica(slug):
    return SITE + ("/" if slug == "index" else "/" + slug + "/")


def schema(slug, titulo, descricao):
    org = {
        "@context": "https://schema.org",
        "@type": "LegalService",
        "@id": SITE + "/#escritorio",
        "name": NOME,
        "alternateName": NOME_CURTO,
        "url": SITE,
        "image": f"{SITE}/assets/img/og.jpg",
        "logo": f"{SITE}/assets/img/logo-av.png",
        "description": "Escritório de advocacia com atendimento online para todo o Brasil: Direito Administrativo, Civil, Penal, Previdenciário e Tributário.",
        "slogan": "Direito claro, acessível e humano",
        "telephone": "+55 75 99864-9163",
        "email": EMAIL,
        "priceRange": "$$",
        "address": {"@type": "PostalAddress", "streetAddress": "Rua Dr. Bertino Passos, 21, Centro", "addressLocality": "Amargosa", "addressRegion": "BA", "postalCode": "45300-000", "addressCountry": "BR"},
        "areaServed": {"@type": "Country", "name": "Brasil"},
        "availableChannel": [{"@type": "ServiceChannel", "name": "Atendimento online", "serviceUrl": SITE + "/contato/", "availableLanguage": "pt-BR"}],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:00"}],
        "knowsAbout": [a[2] for a in AREAS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Áreas de atuação", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": a[2], "url": canonica(a[0]), "description": a[5], "areaServed": "BR"}} for a in AREAS]},
        "founder": [{"@type": "Person", "name": s["nome"], "jobTitle": "Advogado", "url": SITE + "/socios/#" + k, "image": f"{SITE}/assets/img/socio-{k}-q.jpg", "knowsAbout": [AREA[a][2] for a in s["areas"]], **({"sameAs": [s["instagram"]]} if s.get("instagram") else {})} for k, s in SOCIOS.items()],
        "sameAs": [INSTAGRAM],
    }
    grafos = [org]
    if slug != "index":
        nome_pag = AREA[slug][2] if slug in AREA else dict(MENU).get(slug, titulo.split(" · ")[0])
        grafos.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"},
            *([{"@type": "ListItem", "position": 2, "name": "Áreas de atuação", "item": canonica("areas")}] if slug in AREA else []),
            {"@type": "ListItem", "position": 3 if slug in AREA else 2, "name": nome_pag, "item": canonica(slug)}]})
    if slug in AREA:
        a = AREA[slug]
        grafos.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in a[8]]})
    return "\n".join(f'<script type="application/ld+json">{json.dumps(g, ensure_ascii=False)}</script>' for g in grafos)


INDEXNOW_KEY = "1590f818c4af16e2bf718cde7ffb1124"  # chave IndexNow (Bing, Yandex, Naver…): o arquivo /<chave>.txt prova a propriedade do site
VERIFICACAO = {  # tokens de verificação dos motores de busca (Google Search Console / Bing Webmaster)
    "google-site-verification": "voJmETPGiMVQqbX5KZfRUAvctrc4y5CIDCkihBugoog",
    "msvalidate.01": "",
}


def versao_asset(rel):
    """Sufixo ?v=<hash> para CSS/JS: navegadores e CDNs pegam a versão nova logo após cada publicação."""
    import hashlib
    return hashlib.md5((SRC / rel).read_bytes()).hexdigest()[:8]


def pagina(slug, titulo, descricao, corpo, og="assets/img/og.jpg"):
    canon = canonica(slug)
    css_v, js_v = versao_asset("assets/css/site.css"), versao_asset("assets/js/site.js")
    noindex = slug == "404"
    robots = '<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">'
    verif = "".join(f'\n<meta name="{k}" content="{v}">' for k, v in VERIFICACAO.items() if v)
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(titulo)}</title>
<meta name="description" content="{html.escape(descricao)}">
{robots}{verif}
<link rel="canonical" href="{canon}">
<meta property="og:site_name" content="{NOME}">
<meta property="og:locale" content="pt_BR">
<meta property="og:url" content="{canon}">
<meta property="og:title" content="{html.escape(titulo)}">
<meta property="og:description" content="{html.escape(descricao)}">
<meta property="og:image" content="{SITE}/{og}?v=2">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NOME} — atendimento online para todo o Brasil">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(titulo)}">
<meta name="twitter:description" content="{html.escape(descricao)}">
<meta name="twitter:image" content="{SITE}/{og}?v=2">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0B0B0C">
<link rel="icon" href="assets/img/icone-av-64.png" type="image/png" sizes="64x64">
<link rel="icon" href="assets/img/icone-av-256.png" type="image/png" sizes="256x256">
<link rel="apple-touch-icon" href="assets/img/icone-av-256.png">
<link rel="preload" href="assets/fonts/cormorant-garamond-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/manrope-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css?v={css_v}">
{schema(slug, titulo, descricao)}
</head>
<body>
{cabecalho(slug)}
<main id="conteudo">
{corpo}
</main>
{rodape()}
</body>
</html>
'''


def foto(nome, alt, classe="", prioridade=False, pos=None, sizes="(max-width: 960px) 100vw, 50vw"):
    estilo = f' style="object-position:{pos}"' if pos else ""
    return (f'<img class="{classe}" src="assets/img/{nome}.jpg" srcset="assets/img/{nome}.jpg 1x, assets/img/{nome}@2x.jpg 2x" '
            f'alt="{html.escape(alt)}" '
            f'{"fetchpriority=\"high\" decoding=\"async\"" if prioridade else "loading=\"lazy\" decoding=\"async\""}{estilo}>')


def lista_check(itens, classe="lista-check"):
    return f'<ul class="{classe}">' + "".join(f"<li>{I['check']}<span>{t}</span></li>" for t in itens) + "</ul>"


def secao_titulo(eyebrow, titulo, texto=None, centro=False):
    return f'<div class="secao-titulo{" centro" if centro else ""} revela"><span class="eyebrow">{eyebrow}</span><h2>{titulo}</h2>{f"<p>{texto}</p>" if texto else ""}</div>'


def faq(itens):
    return '<div class="faq revela">' + "".join(f"<details><summary>{q}{I['chev']}</summary><p>{a}</p></details>" for q, a in itens) + "</div>"


def trilho_nav():
    """Setas e barra de progresso de uma fileira que rola lateralmente (desktop/tablet)."""
    return f'<div class="trilho-nav"><div class="trilho-barra" aria-hidden="true"><i></i></div><button type="button" data-ant aria-label="Anterior">{I["arrow"]}</button><button type="button" data-prox aria-label="Próximo">{I["arrow"]}</button></div>'


def card_area(a, numero=None):
    slug, icone, nome, _, resp, resumo, itens, _, _ = a
    s = SOCIOS[resp]
    return f'''<article class="area revela">
  <div class="area-tit"><span class="icone">{I[icone]}</span><h3>{nome}</h3></div>
  <p>{resumo}</p>
  {lista_check(itens[:3], "lista-check area-lista")}
  <p class="area-resp"><img src="assets/img/socio-{resp}-q.jpg" srcset="assets/img/socio-{resp}-q.jpg 1x, assets/img/socio-{resp}-q@2x.jpg 2x" alt="" width="450" height="450" loading="lazy" decoding="async"><span>Responsável: <b>{s["tratamento"]}</b></span></p>
  <div class="area-acoes"><a class="btn btn-contorno" href="{url(slug)}">Saiba mais {I["arrow"]}</a>{btn_whats("WhatsApp", "btn btn-dourado", f"Olá, {s['tratamento']}! Vim pelo site e preciso de orientação em {nome}.", resp)}</div>
</article>'''


def card_socio(k, completo=False):
    s = SOCIOS[k]
    areas = "".join(f'<a class="tag" href="{url(a)}">{AREA[a][2]}</a>' for a in s["areas"])
    return f'''<article class="socio revela" id="{k}">
  <div class="socio-foto"><div class="moldura">{foto(f"socio-{k}", s["tratamento"] + ", advogado", sizes="(max-width: 640px) 100vw, 25vw")}</div>
    <div class="socio-sub"><div class="tags">{areas}</div></div>
  </div>
  <div class="socio-corpo">
    <span class="eyebrow">{s["cargo"]} · {s["oab"]}</span>
    <h3>{s["tratamento"]}</h3>
    <p class="socio-foco">{s["foco"]}</p>
    <div class="tags tags-mobile">{areas}</div>
    <p class="socio-resumo">{s["resumo"]}</p>
    {lista_check(s["credenciais"], "lista-check socio-lista")}
    <div class="socio-acoes">{btn_whats(f"Falar com {s['nome'].split()[0]}", "btn btn-dourado", f"Olá, {s['tratamento']}! Vim pelo site do escritório e gostaria de uma orientação.", k)}{"" if completo else f'<a class="btn btn-contorno" href="{url("socios")}#{k}">Perfil completo {I["arrow"]}</a>'}</div>
  </div>
</article>'''


def cta(titulo="Fale com um advogado", texto="Atendimento direto com os sócios, online para todo o Brasil ou no escritório. Conte sua situação pelo WhatsApp e receba uma orientação clara sobre os próximos passos.", socio=None, msg=None):
    r, j = SOCIOS["ricardo"], SOCIOS["jefferson"]
    if socio:
        s = SOCIOS[socio]
        botoes = btn_whats(f"WhatsApp · {s['nome']}", "btn btn-dourado", msg, socio, grande=True) + f'<a class="btn btn-contorno btn-grande" href="{url("contato")}">{I["video"]}<span>Consulta online</span></a>'
    else:
        botoes = btn_whats(f"WhatsApp · {r['nome']}", "btn btn-dourado", msg, "ricardo", grande=True) + btn_whats(f"WhatsApp · {j['nome']}", "btn btn-contorno", msg, "jefferson", grande=True)
    return f'''<section class="secao"><div class="wrap"><div class="cta revela">
  <div><span class="eyebrow">Primeiro contato</span><h2>{titulo}</h2><p>{texto}</p></div>
  <div class="acoes-cta">{botoes}</div>
</div></div></section>'''


def hero_interno(eyebrow, titulo, lead, foto_nome, alt, itens=None, socio=None, msg=None, pos=None, ar=None):
    s = SOCIOS[socio] if socio else None
    botoes = (btn_whats(f"Falar com {s['tratamento']}", "btn btn-dourado", msg, socio, grande=True) if s else btn_whats(grande=True)) + f'<a class="btn btn-contorno btn-grande" href="{url("contato")}">{I["video"]}<span>Atendimento online</span></a>'
    return f'''<section class="pagina-hero">
  <div class="wrap">
    <div class="hero-copy">
      <span class="eyebrow">{eyebrow}</span>
      <h1 class="hero-titulo">{titulo}</h1>
      <p class="hero-lead">{lead}</p>
      {lista_check(itens) if itens else ""}
      <div class="hero-acoes">{botoes}</div>
    </div>
    <div class="pagina-foto revela"{f' style="--ar:{ar}"' if ar else ""}><div class="moldura">{foto(foto_nome, alt, prioridade=True, pos=pos)}</div></div>
  </div>
</section>'''


def dupla(foto_nome, alt, eyebrow, titulo, texto, itens=None, invertida=False, link=None, link_txt=None, pos=None, escura=False, ar=None, ar_m=None):
    estilo = (f' style="{f"--ar:{ar};" if ar else ""}{f"--ar-m:{ar_m};" if ar_m else ""}"' if (ar or ar_m) else "")
    return f'''<section class="secao{" secao-escura" if escura else " secao-clara"}"><div class="wrap dupla{" invertida" if invertida else ""}">
  <div class="dupla-foto revela"{estilo}><div class="moldura">{foto(foto_nome, alt, pos=pos)}</div></div>
  <div class="dupla-texto revela">
    <span class="eyebrow">{eyebrow}</span><h2>{titulo}</h2><p>{texto}</p>
  </div>
  {f'<div class="dupla-lista revela">{lista_check(itens)}</div>' if itens else ""}
  {f'<div class="dupla-btn revela"><a class="btn btn-dourado" href="{link}">{link_txt} {I["arrow"]}</a></div>' if link else ""}
</div></section>'''


def passos():
    itens = [
        ("chat", "Primeiro contato", "Pelo WhatsApp, por videochamada ou no escritório, de qualquer lugar do Brasil. Você conta a situação e já recebe uma orientação inicial sobre urgências e prazos."),
        ("doc", "Análise do caso", "Você envia os documentos pelo WhatsApp ou e-mail; estudamos o processo e os riscos e definimos, com você, a estratégia mais adequada."),
        ("alvo", "Acompanhamento", "Honorários combinados por escrito, procuração assinada digitalmente, atualização constante e condução do caso até o fim — na via administrativa ou judicial."),
    ]
    lis = "".join(f'<li class="revela"><span class="passo-num">{i + 1}</span><span class="passo-icone">{I[ic]}</span><h3>{t}</h3><p>{d}</p></li>' for i, (ic, t, d) in enumerate(itens))
    return f'''<section class="secao secao-escura secao-passos"><div class="wrap">
  {secao_titulo("Como funciona", "Do primeiro contato à solução", "Um caminho simples e transparente, explicado em linguagem clara desde a primeira conversa.")}
  <ol class="passos">{lis}</ol>
</div></section>'''


def online_secao(escura=True, titulo="Advogados online para todo o Brasil"):
    """Faixa de cards sobre o atendimento online (home, escritório e contato)."""
    cards = [
        ("video", "Consulta por videochamada", "Reunião online pelo WhatsApp ou pela plataforma que você preferir, no horário combinado — sem deslocamento."),
        ("doc", "Documentos digitais", "Envio de documentos pelo WhatsApp ou e-mail e procuração com assinatura eletrônica, com validade jurídica."),
        ("brasil", "Em qualquer cidade do Brasil", "Processos eletrônicos acompanhados em qualquer comarca ou tribunal do país, inclusive nos tribunais superiores."),
        ("map", "Presencial, se preferir", f"Escritório aberto de segunda a sexta, com hora marcada, para quem quiser conversar pessoalmente."),
    ]
    lis = "".join(f'<article class="card revela"><span class="icone">{I[ic]}</span><h3>{t}</h3><p>{d}</p></article>' for ic, t, d in cards)
    return f'''<section class="secao {"secao-escura" if escura else "secao-clara"} secao-online" id="online"><div class="wrap">
  {secao_titulo("Atendimento online", titulo, "Você não precisa estar na mesma cidade para ter um advogado de confiança. Da primeira conversa à sentença, tudo pode ser feito a distância — com a mesma atenção do atendimento presencial.", centro=True)}
  <div class="grade-4">{lis}</div>
  <div class="ver-todos">{btn_whats("Agendar consulta online", grande=True)}</div>
</div></section>'''


def numeros():
    itens = [("10", "anos de advocacia", "Quase uma década de atuação dos sócios"), ("4", "pós-graduações", "PUC Minas, Escola Brasileira de Direito e Instituto Brasileiro de Direito"), ("8", "anos de Procuradoria", "Experiência de Ricardo Andrade na gestão pública municipal"), ("2", "sócios à frente", "Atendimento direto, sem intermediários")]
    return '<div class="numeros">' + "".join(f'<div class="numero revela"><strong>{n}</strong><span>{t}</span><small>{d}</small></div>' for n, t, d in itens) + "</div>"


def formulario():
    opcoes = "".join(f'<option>{a[2]}</option>' for a in AREAS)
    return f'''<form class="form revela" id="formulario" data-form-demo novalidate>
  <div class="form-grade">
    <label><span>Nome</span><input type="text" name="nome" required autocomplete="name" placeholder="Seu nome"></label>
    <label><span>WhatsApp</span><input type="tel" name="telefone" required autocomplete="tel" placeholder="(75) 9 0000-0000"></label>
    <label><span>E-mail</span><input type="email" name="email" autocomplete="email" placeholder="voce@exemplo.com"></label>
    <label><span>Assunto</span><select name="area">{opcoes}<option>Outro / não sei</option></select></label>
    <label class="form-larga"><span>Mensagem</span><textarea name="mensagem" rows="4" placeholder="Conte brevemente a situação. Não envie dados sensíveis por aqui; detalhes ficam para a conversa com o advogado."></textarea></label>
  </div>
  <label class="consent"><input type="checkbox" name="consent" required> <span>Autorizo o contato do escritório pelos dados informados (LGPD).</span></label>
  <div class="form-acoes"><button class="btn btn-dourado btn-grande" type="submit">Enviar mensagem {I["arrow"]}</button><span class="form-nota">Resposta em horário de atendimento.</span></div>
  <p class="form-ok" role="status" hidden>{I["check"]} Recebemos sua mensagem. Um dos sócios entra em contato em breve. <em>(Prévia: nesta versão o envio é apenas demonstração.)</em></p>
</form>'''


# ---------------------------------------------------------------- páginas
def home():
    r, j = SOCIOS["ricardo"], SOCIOS["jefferson"]
    areas = "".join(card_area(a) for a in AREAS)
    socios = "".join(card_socio(k) for k in ("ricardo", "jefferson"))
    return f'''
<section class="hero">
  <div class="hero-dupla" aria-label="Os sócios">
    <div class="moldura">{foto("socios-dupla", "Dr. Ricardo Andrade e Dr. Jefferson Victor, sócios do escritório", prioridade=True, sizes="100vw")}</div>
    <div class="hero-dupla-nomes">
      <a href="{url("socios")}#ricardo"><b>{r["tratamento"]}</b><small>Administrativo · Civil · Tributário</small></a>
      <a href="{url("socios")}#jefferson"><b>{j["tratamento"]}</b><small>Penal · Previdenciário</small></a>
    </div>
    <div class="hero-dupla-numeros" aria-label="Números do escritório">
      <div><strong>10</strong><span>anos de advocacia</span></div>
      <div><strong>4</strong><span>pós-graduações</span></div>
      <div><strong>8</strong><span>anos na Procuradoria Municipal</span></div>
    </div>
    <ul class="hero-dupla-cred">
      <li>{I["check"]}<span><b>Jefferson</b> — ex-Juiz Leigo e Conciliador do TJBA, pós em Ciências Criminais (PUC Minas)</span></li>
      <li>{I["check"]}<span><b>Ricardo</b> — OAB/BA 57.064, ex-Procurador Municipal, atuação em tribunais superiores</span></li>
    </ul>
  </div>
  <div class="wrap">
    <div class="hero-copy">
      <span class="eyebrow">Advogados associados · atendimento online em todo o Brasil</span>
      <h1 class="hero-titulo">Direito claro, acessível e <em>humano</em>.</h1>
      <p class="hero-lead">Há quase dez anos, Jefferson Victor e Ricardo Andrade atuam com estratégia, técnica e compromisso nas áreas administrativa, civil, penal, previdenciária e tributária. Atendimento online para todo o Brasil, por videochamada e WhatsApp — do primeiro contato aos tribunais superiores.</p>
      <div class="hero-acoes">{btn_whats("Falar com um advogado", grande=True)}<a class="btn btn-contorno btn-grande" href="{url("areas")}">Áreas de atuação {I["arrow"]}</a></div>
      <ul class="hero-provas">
        <li>{I["check"]}<span><b>Atendimento online</b> em todo o Brasil</span></li>
        <li>{I["check"]}<span><b>Quase 10 anos</b> de atuação</span></li>
        <li>{I["check"]}<span>Atuação em <b>tribunais superiores</b></span></li>
      </ul>
    </div>
    <div class="hero-socios revela">
      <a class="hero-card" href="{url("socios")}#ricardo"><div class="moldura">{foto("hero-ricardo", r["tratamento"] + ", advogado", prioridade=True, sizes="(max-width: 960px) 50vw, 25vw")}</div><span class="hero-card-nome">{r["tratamento"]}</span><span class="hero-card-area">{r["foco"]}</span></a>
      <a class="hero-card" href="{url("socios")}#jefferson"><div class="moldura">{foto("hero-jefferson", j["tratamento"] + ", advogado", prioridade=True, sizes="(max-width: 960px) 50vw, 25vw")}</div><span class="hero-card-nome">{j["tratamento"]}</span><span class="hero-card-area">{j["foco"]}</span></a>
    </div>
  </div>
</section>

<section class="lema" aria-label="Lema do escritório">
  <div class="wrap"><ul class="lema-lista"><li>Estratégia</li><li>Técnica</li><li>Compromisso</li><li>Resultados</li></ul><p>A defesa dos seus direitos é a nossa missão.</p></div>
</section>

{online_secao()}

<section class="secao secao-clara secao-areas" id="areas">
  <div class="wrap">
    <div class="areas-cab">{secao_titulo("Áreas de atuação", "Cinco frentes, dois sócios dedicados", "Cada área tem um sócio responsável, que acompanha o caso pessoalmente do início ao fim — presencialmente ou online, de onde você estiver.")}<a class="btn btn-contorno-escuro" href="{url("areas")}">Todas as áreas {I["arrow"]}</a></div>
    <div class="areas" data-trilho>{areas}</div>
    {trilho_nav()}
  </div>
</section>

<section class="secao secao-escura secao-socios" id="socios">
  <div class="wrap">
    {secao_titulo("Os sócios", "Quem vai cuidar do seu caso", "Advogados com formação sólida, passagem pelo Judiciário e pela administração pública, e atendimento direto — sem intermediários.")}
    <div class="socios carrossel"><div class="socios-trilho carrossel-trilho">{socios}</div><div class="carrossel-pontos" role="tablist"></div></div>
    <div class="ver-todos"><a class="btn btn-contorno" href="{url("socios")}">Conhecer os sócios {I["arrow"]}</a></div>
  </div>
</section>

{dupla("escritorio-jefferson", "Jefferson Victor em atendimento no escritório", "O escritório", "Soluções reais, com ética e empatia", "Um escritório pensado para quem precisa resolver um problema jurídico sem se perder em termos difíceis. Explicamos cada etapa, combinamos tudo por escrito e mantemos você informado — porque confiança se constrói com clareza.", ["Atendimento direto com os sócios responsáveis", "Linguagem clara, sem juridiquês", "Estratégia definida caso a caso", "Acompanhamento do início ao fim"], link=url("escritorio"), link_txt="Conhecer o escritório", pos="center 30%", ar="4 / 4.6", ar_m="4 / 3")}

{passos()}

<section class="secao secao-clara"><div class="wrap">
  {secao_titulo("Em números", "Experiência que se traduz em segurança", centro=True)}
  {numeros()}
</div></section>

<section class="secao secao-escura secao-contato-home"><div class="wrap">
  <div class="contato-home">
    <div class="revela">{secao_titulo("Onde estamos", "Escritório e atendimento online", "Atendimento online para todo o Brasil, por videochamada e WhatsApp, e presencial com hora marcada, em horário comercial.")}
      <ul class="lista-contato grande">
        <li>{I["video"]}<span>{ONLINE}<br>Videochamada, WhatsApp e documentos digitais</span></li>
        <li>{I["map"]}<span>{ENDERECO}<br>{CIDADE}</span></li>
        <li>{I["clock"]}<span>{HORARIO}</span></li>
        <li>{I["insta"]}<span><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">@andradevictoradv</a></span></li>
      </ul>
      <div class="contato-home-acoes"><a class="btn btn-contorno" href="{MAPS}" target="_blank" rel="noopener noreferrer">{I["map"]}<span>Como chegar</span></a><a class="btn btn-contorno" href="{url("contato")}">{I["chat"]}<span>Enviar mensagem</span></a></div>
    </div>
    <div class="contato-cartoes revela">
      {"".join(f'<a class="contato-cartao" href="{wa(None, k)}" target="_blank" rel="noopener noreferrer"><img src="assets/img/socio-{k}-q.jpg" srcset="assets/img/socio-{k}-q.jpg 1x, assets/img/socio-{k}-q@2x.jpg 2x" alt="{SOCIOS[k]["tratamento"]}" width="450" height="450" loading="lazy" decoding="async"><span class="contato-cartao-nome">{SOCIOS[k]["tratamento"]}</span><span class="contato-cartao-area">{SOCIOS[k]["foco"]}</span><span class="contato-cartao-num">{I["whats"]}{SOCIOS[k]["cel"]}</span></a>' for k in ("ricardo", "jefferson"))}
    </div>
  </div>
</div></section>
'''


def areas_pg():
    cards = "".join(card_area(a) for a in AREAS)
    return f'''
<section class="pagina-hero pagina-hero-curta"><div class="wrap"><div class="hero-copy">
  <span class="eyebrow">Áreas de atuação</span>
  <h1 class="hero-titulo">Cinco áreas, um sócio responsável</h1>
  <p class="hero-lead">Direito Administrativo, Civil e Tributário com Ricardo Andrade; Direito Penal e Previdenciário com Jefferson Victor. Em casos que cruzam mais de uma área, os dois sócios atuam juntos — com atendimento online para todo o Brasil.</p>
</div></div></section>
<section class="secao secao-clara"><div class="wrap"><div class="areas" data-trilho>{cards}</div>{trilho_nav()}</div></section>
{online_secao(titulo="Todas as áreas, com atendimento online")}
{cta()}
'''


def area_pg(a):
    slug, icone, nome, curto, resp, resumo, itens, lead, perguntas = a
    s = SOCIOS[resp]
    msg = f"Olá, {s['tratamento']}! Vim pelo site e preciso de orientação em {nome}."
    outras = "".join(f'<li><a href="{url(x[0])}">{I["arrow"]}{x[2]}</a></li>' for x in AREAS if x[0] != slug)
    return f'''
{hero_interno(nome, f"{nome} com sócio responsável", lead, f"socio-{resp}-q", s["tratamento"] + ", advogado responsável", socio=resp, msg=msg)}
<section class="secao secao-clara"><div class="wrap dupla-simples">
  <div class="revela">{secao_titulo("Como atuamos", f"Atuação em {nome}", resumo)}{lista_check(itens)}</div>
  <aside class="lateral revela">
    <div class="lateral-socio">
      <img src="assets/img/socio-{resp}-q.jpg" srcset="assets/img/socio-{resp}-q.jpg 1x, assets/img/socio-{resp}-q@2x.jpg 2x" alt="{s["tratamento"]}" width="450" height="450" loading="lazy" decoding="async">
      <div><span class="eyebrow">Responsável pela área</span><h3>{s["tratamento"]}</h3><p>{s["oab"]} · {s["foco"]}</p></div>
    </div>
    <p>{s["resumo"]}</p>
    {btn_whats(f"Falar com {s['nome'].split()[0]}", "btn btn-dourado", msg, resp)}
    <a class="link-seta" href="{url("socios")}#{resp}">Ver perfil completo {I["arrow"]}</a>
    <h4>Outras áreas</h4><ul class="lista-links">{outras}</ul>
  </aside>
</div></section>
<section class="secao secao-escura"><div class="wrap">
  {secao_titulo("Dúvidas frequentes", f"Perguntas comuns sobre {nome}")}
  {faq(perguntas)}
</div></section>
{cta(f"Precisa de orientação em {nome}?", f"Fale diretamente com {s['tratamento']}, responsável pela área, e receba uma orientação clara sobre o seu caso.", socio=resp, msg=msg)}
'''


def socios_pg():
    secoes = ""
    for i, k in enumerate(("ricardo", "jefferson")):
        s = SOCIOS[k]
        bio = "".join(f"<p>{p}</p>" for p in s["bio"])
        areas_s = "".join(f'<li><a href="{url(a)}">{I["arrow"]}{AREA[a][2]}</a></li>' for a in s["areas"])
        secoes += f'''<section class="secao {"secao-clara" if i == 0 else "secao-escura"}" id="{k}"><div class="wrap perfil{" invertido" if i == 1 else ""}">
  <div class="perfil-foto revela"><div class="moldura">{foto(f"socio-{k}", s["tratamento"] + ", advogado")}</div>
    <div class="perfil-contato"><span>{s["oab"]}{f' · <a href="{s["instagram"]}" target="_blank" rel="noopener noreferrer">{s["insta_user"]}</a>' if s.get("instagram") else ""}</span>{btn_whats(f"Falar com {s['nome'].split()[0]}", "btn btn-dourado", f"Olá, {s['tratamento']}! Vim pelo site do escritório e gostaria de uma orientação.", k)}</div>
  </div>
  <div class="perfil-texto revela">
    <span class="eyebrow">{s["cargo"]}</span>
    <h2>{s["tratamento"]}</h2>
    <p class="socio-foco">{s["foco"]}</p>
    <div class="texto-longo">{bio}</div>
    <h3 class="perfil-sub">Formação e experiência</h3>
    {lista_check(s["credenciais"])}
    <h3 class="perfil-sub">Áreas de atuação</h3>
    <ul class="lista-links">{areas_s}</ul>
  </div>
</div></section>'''
    return f'''
<section class="pagina-hero pagina-hero-curta"><div class="wrap"><div class="hero-copy">
  <span class="eyebrow">Os sócios</span>
  <h1 class="hero-titulo">Dois advogados, um compromisso com você</h1>
  <p class="hero-lead">Formação sólida, passagem pelo Judiciário e pela administração pública, e atendimento direto — online para todo o Brasil ou no escritório. Conheça quem assina cada caso.</p>
</div></div></section>
{secoes}
{cta()}
'''


def escritorio_pg():
    valores = [
        ("maos", "Ética", "Respeito às regras da profissão e às pessoas: dizemos o que é possível e o que não é."),
        ("chat", "Clareza", "Linguagem simples e informação completa em todas as etapas do caso."),
        ("alvo", "Estratégia", "Cada caso tem um plano próprio, construído com técnica e com os seus objetivos."),
        ("coracao", "Empatia", "Atendimento humano, com escuta e disponibilidade — como deve ser."),
    ]
    cards = "".join(f'<article class="card revela"><span class="icone">{I[ic]}</span><h3>{t}</h3><p>{d}</p></article>' for ic, t, d in valores)
    return f'''
{hero_interno("O escritório", "Advocacia com ética, técnica e empatia", "Andrade e Victor Advogados Associados nasceu da parceria entre dois advogados com quase dez anos de estrada, formação complementar e um mesmo jeito de trabalhar: direito claro, acessível e humano — para clientes de todo o Brasil.", "escritorio-jefferson", "Jefferson Victor em atendimento no escritório", itens=["Atendimento online para todo o Brasil, por videochamada e WhatsApp", "Áreas administrativa, civil, penal, previdenciária e tributária", "Atuação em todas as instâncias, inclusive tribunais superiores"], pos="center 20%", ar="4 / 4.4")}
<section class="secao secao-clara"><div class="wrap">
  {secao_titulo("Nossos valores", "O que orienta cada caso", centro=True)}
  <div class="grade-4">{cards}</div>
</div></section>
{online_secao(titulo="Como funciona o atendimento online")}
{dupla("hero-ricardo", "Ricardo Andrade, advogado", "Trajetória", "Do Judiciário e da gestão pública para a sua defesa", "Jefferson Victor foi Juiz Leigo e Conciliador do TJBA; Ricardo Andrade foi Procurador Municipal por oito anos. Essa vivência dos dois lados do balcão — decidindo e defendendo o interesse público — hoje se traduz em estratégia e técnica a serviço de quem procura o escritório, de qualquer lugar do Brasil.", ["Quase dez anos de advocacia", "Quatro pós-graduações entre os sócios", "Atuação em tribunais superiores"], invertida=True, link=url("socios"), link_txt="Conhecer os sócios", pos="center 20%", escura=False, ar="4 / 5", ar_m="4 / 4.2")}
<section class="secao secao-clara"><div class="wrap">
  {secao_titulo("Em números", "Experiência que se traduz em segurança", centro=True)}
  {numeros()}
</div></section>
{cta()}
'''


def cartao_contato(k):
    """Cartão de contato direto de um sócio: foto, nome, OAB, áreas e botões (WhatsApp, ligar, Instagram)."""
    s = SOCIOS[k]
    redes = f'<a class="btn btn-contorno-escuro" href="{s["instagram"]}" target="_blank" rel="noopener noreferrer">{I["insta"]}<span>{s["insta_user"]}</span></a>' if s.get("instagram") else ""
    return f'''<article class="contato-socio revela" id="contato-{k}">
  <div class="contato-socio-foto"><div class="moldura">{foto(f"socio-{k}", s["tratamento"] + ", advogado", sizes="(max-width: 640px) 100vw, 200px")}</div></div>
  <div class="contato-socio-txt">
    <span class="eyebrow">{s["cargo"]} · {s["oab"]}</span>
    <h3>{s["tratamento"]}</h3>
    <p class="socio-foco">{s["foco"]}</p>
    <p class="contato-socio-num">{I["whats"]}<span>{s["cel"]}</span></p>
    <div class="contato-socio-acoes">{btn_whats("WhatsApp", "btn btn-dourado", f"Olá, {s['tratamento']}! Vim pelo site do escritório e gostaria de uma orientação.", k)}<a class="btn btn-contorno-escuro" href="{tel(s["cel"])}">{I["phone"]}<span>Ligar</span></a>{redes}</div>
  </div>
</article>'''


def contato_pg():
    r, j = SOCIOS["ricardo"], SOCIOS["jefferson"]
    return f'''
<section class="pagina-hero pagina-hero-curta"><div class="wrap"><div class="hero-copy">
  <span class="eyebrow">Contato</span>
  <h1 class="hero-titulo">Fale com o escritório</h1>
  <p class="hero-lead">Atendimento online para todo o Brasil pelo WhatsApp de cada sócio, por videochamada ou pelas redes sociais — e presencial, com hora marcada, no escritório. Respondemos em horário comercial.</p>
</div></div></section>
<section class="secao secao-clara"><div class="wrap contato-grade">
  <div class="contato-info revela">
    <h2>Escritório e atendimento online</h2>
    <ul class="lista-contato grande">
      <li>{I["video"]}<span><b>{ONLINE}</b><br>Videochamada, WhatsApp e documentos digitais</span></li>
      <li>{I["map"]}<span><b>Endereço</b><br>{ENDERECO}<br>{CIDADE}</span></li>
      <li>{I["clock"]}<span><b>Horário</b><br>{HORARIO}</span></li>
      <li>{I["mail"]}<span><b>E-mail</b><br><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
      <li>{I["insta"]}<span><b>Instagram</b><br><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">@andradevictoradv</a> · escritório<br><a href="{j["instagram"]}" target="_blank" rel="noopener noreferrer">{j["insta_user"]}</a> · Dr. Jefferson Victor</span></li>
    </ul>
    <div class="contato-acoes"><a class="btn btn-dourado" href="{MAPS}" target="_blank" rel="noopener noreferrer">{I["map"]}<span>Como chegar</span></a><a class="btn btn-contorno-escuro" href="mailto:{EMAIL}">{I["mail"]}<span>Enviar e-mail</span></a></div>
  </div>
  <div class="contato-direto">
    <div class="revela"><span class="eyebrow">Contato direto</span><h2>Fale com o advogado</h2><p>Escolha o sócio responsável pela sua área e chame no WhatsApp, ligue ou acompanhe nas redes.</p></div>
    {cartao_contato("ricardo")}
    {cartao_contato("jefferson")}
    <p class="contato-direto-nota revela">{I["mail"]}<span>Um e-mail para os dois sócios: <a href="mailto:{EMAIL}">{EMAIL}</a></span></p>
  </div>
</div></section>
{online_secao(titulo="Como funciona o atendimento online")}
'''


def privacidade_pg():
    return f'''
<section class="pagina-hero pagina-hero-curta"><div class="wrap"><div class="hero-copy">
  <span class="eyebrow">Privacidade</span>
  <h1 class="hero-titulo">Política de privacidade</h1>
  <p class="hero-lead">Como este site trata os dados de quem entra em contato com o escritório.</p>
</div></div></section>
<section class="secao secao-clara"><div class="wrap texto-longo">
  <h2>Quais dados coletamos</h2>
  <p>Apenas os dados que você informa voluntariamente pelo formulário de contato ou pelo WhatsApp: nome, telefone, e-mail e a mensagem enviada.</p>
  <h2>Para que usamos</h2>
  <p>Para responder ao seu contato, agendar atendimento e, se houver contratação, para a prestação dos serviços advocatícios. Não vendemos nem compartilhamos seus dados com terceiros para fins comerciais.</p>
  <h2>Sigilo profissional</h2>
  <p>As informações compartilhadas com o escritório são protegidas pelo sigilo profissional do advogado, nos termos do Estatuto da Advocacia e do Código de Ética e Disciplina da OAB.</p>
  <h2>Seus direitos</h2>
  <p>Nos termos da LGPD (Lei 13.709/2018), você pode solicitar acesso, correção ou exclusão dos seus dados pelo WhatsApp de qualquer um dos sócios.</p>
  <h2>Cookies</h2>
  <p>Este site não usa cookies de rastreamento nem ferramentas de publicidade.</p>
</div></section>
'''


def pagina_404():
    return f'''
<section class="pagina-hero erro-404"><div class="wrap"><div class="hero-copy">
  <span class="eyebrow">Erro 404</span>
  <h1 class="hero-titulo">Página não encontrada</h1>
  <p class="hero-lead">O endereço pode ter mudado. Volte ao início ou fale com o escritório.</p>
  <div class="hero-acoes"><a class="btn btn-dourado btn-grande" href="{url("index")}">Ir para o início {I["arrow"]}</a>{btn_whats("Falar no WhatsApp", "btn btn-contorno", grande=True)}</div>
</div></div></section>
'''


PAGINAS = {
    "index": ("Andrade e Victor Advogados · Atendimento online em todo o Brasil", "Escritório de advocacia com atendimento online para todo o Brasil: Direito Administrativo, Civil, Penal, Previdenciário e Tributário. Consulta por videochamada ou WhatsApp.", home),
    "areas": ("Áreas de atuação · Advogados online | Andrade e Victor", "Direito Administrativo, Civil, Penal, Previdenciário e Tributário, com sócio responsável por área e atendimento online para todo o Brasil.", areas_pg),
    "socios": ("Sócios · Ricardo Andrade e Jefferson Victor, advogados", "Conheça os advogados Ricardo Andrade (OAB/BA 57.064) e Jefferson Victor (OAB/BA 55.402): formação, experiência e áreas de atuação. Atendimento online em todo o Brasil.", socios_pg),
    "escritorio": ("O escritório · Andrade e Victor Advogados Associados", "Advocacia com ética, técnica e empatia e atendimento online para todo o Brasil. Conheça a história, os valores e a forma de trabalhar do escritório.", escritorio_pg),
    "contato": ("Contato · Consulta online com advogado | Andrade e Victor", "Fale com o escritório Andrade e Victor: WhatsApp dos sócios, consulta online por videochamada para todo o Brasil, e-mail, endereço e horário.", contato_pg),
    "privacidade": ("Política de privacidade · Andrade e Victor Advogados", "Como o site do escritório Andrade e Victor Advogados trata os dados de quem entra em contato.", privacidade_pg),
    "404": ("Página não encontrada · Andrade e Victor Advogados", "A página que você procura não existe.", pagina_404),
}
SEO_AREAS = {  # título e descrição de busca de cada área (atendimento online em todo o Brasil)
    "administrativo": ("Advogado de Direito Administrativo online · Andrade e Victor", "Advogado especializado em Direito Administrativo com atendimento online para todo o Brasil: servidores públicos, concursos, licitações, contratos e Mandado de Segurança."),
    "civil": ("Advogado de Direito Civil online · Andrade e Victor", "Advogado de Direito Civil com atendimento online para todo o Brasil: contratos, indenizações, cobranças, família, inventário e questões imobiliárias."),
    "penal": ("Advogado Criminalista online · Andrade e Victor", "Advogado criminalista com atendimento online para todo o Brasil: defesa em inquéritos e processos criminais, Habeas Corpus, recursos e execução penal."),
    "previdenciario": ("Advogado Previdenciário online · Andrade e Victor", "Advogado previdenciário com atendimento online para todo o Brasil: aposentadorias, benefícios por incapacidade, BPC/LOAS, pensões e revisões no INSS."),
    "tributario": ("Advogado Tributarista online · Andrade e Victor", "Advogado tributarista com atendimento online para todo o Brasil: execuções fiscais, autos de infração, restituição de tributos e planejamento tributário."),
}
for a in AREAS:
    t, d = SEO_AREAS.get(a[0], (f"{a[2]} · Andrade e Victor Advogados", a[5]))
    PAGINAS[a[0]] = (t, d, (lambda a=a: area_pg(a)))


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(SRC / "assets", DIST / "assets")
    for slug, (titulo, desc, fn) in PAGINAS.items():
        out = pagina(slug, titulo, desc, fn())
        if LIMPO:  # páginas em /slug/ precisam de caminhos absolutos para os assets
            import re
            out = re.sub(r'((?:src|href|srcset)=")assets/', r'\1/assets/', out)
            out = out.replace(", assets/", ", /assets/")
        if LIMPO and slug not in ("index", "404"):
            (DIST / slug).mkdir(parents=True, exist_ok=True)
            (DIST / slug / "index.html").write_text(out, encoding="utf-8")
        else:
            (DIST / f"{slug}.html").write_text(out, encoding="utf-8")
    (DIST / "_redirects").write_text("/index.html / 301\n", encoding="utf-8")
    (DIST / "google54d106e30fb959fe.html").write_text("google-site-verification: google54d106e30fb959fe.html", encoding="utf-8")  # Search Console (arquivo)
    (DIST / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")  # IndexNow
    # SEO: sitemap.xml e robots.txt (sempre com as URLs canônicas do site publicado)
    import datetime
    hoje = datetime.date.today().isoformat()
    prioridade = {"index": "1.0", "areas": "0.9", "contato": "0.8", "socios": "0.8", "escritorio": "0.7", "privacidade": "0.3"}
    urls = [(canonica(s), prioridade.get(s, "0.9")) for s in PAGINAS if s != "404"]
    (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + "".join(f"  <url><loc>{u}</loc><lastmod>{hoje}</lastmod><changefreq>monthly</changefreq><priority>{p}</priority></url>\n" for u, p in urls)
                                      + "</urlset>\n", encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"ok → {DIST} ({len(PAGINAS)} páginas, links {'limpos' if LIMPO else '.html'}, sitemap com {len(urls)} URLs)")


if __name__ == "__main__":
    main()

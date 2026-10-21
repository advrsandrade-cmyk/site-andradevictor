/* Andrade e Victor Advogados — comportamento do site (sem dependências) */
(function () {
  /* Submenu "Áreas de atuação" no desktop: abre no clique/teclado (o hover é por CSS) */
  document.querySelectorAll(".nav .tem-sub").forEach(function (box) {
    var btn = box.querySelector(".sub-btn");
    if (!btn) return;
    function abrir(v) { box.classList.toggle("aberto", v); btn.setAttribute("aria-expanded", String(v)); }
    btn.addEventListener("click", function () { abrir(!box.classList.contains("aberto")); });
    document.addEventListener("click", function (e) { if (!box.contains(e.target)) abrir(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") abrir(false); });
  });

  /* Menu do celular */
  var hamb = document.querySelector(".hamb");
  var painel = document.getElementById("menu-mobile");
  if (hamb && painel) {
    function fechar() { painel.classList.remove("aberto"); hamb.setAttribute("aria-expanded", "false"); document.body.style.overflow = ""; }
    hamb.addEventListener("click", function () {
      var abrir = !painel.classList.contains("aberto");
      painel.classList.toggle("aberto", abrir);
      hamb.setAttribute("aria-expanded", String(abrir));
      document.body.style.overflow = abrir ? "hidden" : "";
    });
    painel.addEventListener("click", function (e) { if (e.target.closest("a")) fechar(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") fechar(); });
    window.addEventListener("resize", function () { if (window.innerWidth > 960) fechar(); });
  }

  /* Carrosséis (celular): pontos sincronizados com a rolagem e avanço automático suave */
  document.querySelectorAll(".carrossel").forEach(function (c) {
    var trilho = c.querySelector(".carrossel-trilho");
    var pontos = c.querySelector(".carrossel-pontos");
    if (!trilho || !pontos) return;
    var itens = Array.prototype.slice.call(trilho.children), atual = 0, pausado = false;
    itens.forEach(function (_, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.setAttribute("aria-label", "Ir para o item " + (i + 1));
      if (i === 0) b.setAttribute("aria-current", "true");
      b.addEventListener("click", function () { ir(i); pausar(); });
      pontos.appendChild(b);
    });
    function marcar(i) { atual = i; Array.prototype.forEach.call(pontos.children, function (b, k) { if (k === i) b.setAttribute("aria-current", "true"); else b.removeAttribute("aria-current"); }); }
    function ir(i) { var el = itens[i]; trilho.scrollTo({ left: el.offsetLeft - (trilho.clientWidth - el.offsetWidth) / 2, behavior: "smooth" }); marcar(i); }
    trilho.addEventListener("scroll", function () {
      var meio = trilho.scrollLeft + trilho.clientWidth / 2, a = 0;
      itens.forEach(function (el, i) { if (el.offsetLeft <= meio) a = i; });
      if (a !== atual) marcar(a);
    }, { passive: true });
    function pausar() { pausado = true; clearTimeout(c._r); c._r = setTimeout(function () { pausado = false; }, 8000); }
    trilho.addEventListener("touchstart", pausar, { passive: true });
    setInterval(function () { if (getComputedStyle(pontos).display === "none" || pausado) return; ir((atual + 1) % itens.length); }, 6000);
  });

  /* Fileiras que rolam lateralmente (desktop/tablet): setas, barra de progresso e teclado */
  document.querySelectorAll("[data-trilho]").forEach(function (t) {
    var nav = t.nextElementSibling;
    if (!nav || !nav.classList.contains("trilho-nav")) return;
    var barra = nav.querySelector(".trilho-barra i"), ant = nav.querySelector("[data-ant]"), prox = nav.querySelector("[data-prox]");
    function passo() { var f = t.firstElementChild; return f ? f.getBoundingClientRect().width + 20 : t.clientWidth; }
    function atualizar() {
      var max = t.scrollWidth - t.clientWidth;
      if (max <= 2) { nav.style.display = "none"; return; }
      nav.style.display = "";
      barra.style.width = (t.clientWidth / t.scrollWidth * 100) + "%";
      barra.style.transform = "translateX(" + (t.scrollLeft / t.clientWidth * 100) + "%)";
      ant.disabled = t.scrollLeft < 2;
      prox.disabled = t.scrollLeft >= max - 2;
    }
    ant.addEventListener("click", function () { t.scrollBy({ left: -passo(), behavior: "smooth" }); });
    prox.addEventListener("click", function () { t.scrollBy({ left: passo(), behavior: "smooth" }); });
    t.addEventListener("scroll", atualizar, { passive: true });
    window.addEventListener("resize", atualizar);
    atualizar();
  });

  /* Slideshow do hero (celular): rola sozinho, pontos sincronizados, pausa ao tocar */
  document.querySelectorAll("[data-slides]").forEach(function (s) {
    var trilho = s.querySelector(".hero-slides-trilho"), pontos = s.querySelector(".hero-slides-pontos");
    if (!trilho || !pontos) return;
    var itens = Array.prototype.slice.call(trilho.children), atual = 0, pausado = false;
    itens.forEach(function (_, i) {
      var b = document.createElement("button"); b.type = "button"; b.setAttribute("aria-label", "Foto " + (i + 1));
      if (i === 0) b.setAttribute("aria-current", "true");
      b.addEventListener("click", function () { ir(i); pausar(); });
      pontos.appendChild(b);
    });
    function marcar(i) { atual = i; Array.prototype.forEach.call(pontos.children, function (b, k) { if (k === i) b.setAttribute("aria-current", "true"); else b.removeAttribute("aria-current"); }); }
    function ir(i) { trilho.scrollTo({ left: itens[i].offsetLeft, behavior: "smooth" }); marcar(i); }
    function proximo() { if (getComputedStyle(s).display === "none" || pausado) return; ir((atual + 1) % itens.length); }
    trilho.addEventListener("scroll", function () { var i = Math.round(trilho.scrollLeft / trilho.clientWidth); if (i !== atual && i >= 0 && i < itens.length) marcar(i); }, { passive: true });
    function pausar() { pausado = true; clearTimeout(s._r); s._r = setTimeout(function () { pausado = false; }, 6000); }
    trilho.addEventListener("touchstart", pausar, { passive: true });
    setInterval(proximo, 4500);
  });

  /* "Falar com quem?": botões genéricos de WhatsApp abrem o painel de escolha do advogado */
  var painelWa = document.getElementById("falar"), fundoWa = document.getElementById("falar-fundo"), ultimoFoco = null;
  if (painelWa && fundoWa) {
    function abrirWa(origem) {
      ultimoFoco = origem || document.activeElement;
      painelWa.hidden = false; fundoWa.hidden = false;
      var primeiro = painelWa.querySelector(".wa-opcao"); if (primeiro) primeiro.focus();
    }
    function fecharWa() {
      painelWa.hidden = true; fundoWa.hidden = true;
      if (location.hash === "#falar") history.replaceState(null, "", location.pathname + location.search);
      if (ultimoFoco && ultimoFoco.focus) ultimoFoco.focus();
    }
    document.querySelectorAll("[data-wa-escolha]").forEach(function (b) {
      b.addEventListener("click", function (e) { e.preventDefault(); abrirWa(b); });
    });
    painelWa.querySelector(".wa-fechar").addEventListener("click", function (e) { e.preventDefault(); fecharWa(); });
    fundoWa.addEventListener("click", fecharWa);
    painelWa.addEventListener("click", function (e) { if (e.target.closest(".wa-opcao")) setTimeout(fecharWa, 300); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !painelWa.hidden) fecharWa(); });
    if (location.hash === "#falar") abrirWa(null);
  }

  /* Áreas (celular): botão "Todas as áreas" depois dos tiles (no desktop ele fica no cabeçalho da seção) */
  var areas = document.querySelector(".secao-areas .areas");
  var lnk = document.querySelector(".areas-cab .btn");
  if (areas && lnk) { var ver = document.createElement("div"); ver.className = "areas-ver"; ver.appendChild(lnk.cloneNode(true)); areas.insertAdjacentElement("afterend", ver); }

  /* Animação de entrada suave */
  if ("IntersectionObserver" in window) {
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("visivel"); obs.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    document.querySelectorAll(".revela").forEach(function (el) { obs.observe(el); });
  } else {
    document.querySelectorAll(".revela").forEach(function (el) { el.classList.add("visivel"); });
  }

  /* Formulário: prévia sem backend — valida e mostra confirmação. Produção: Pages Function → e-mail/WhatsApp do escritório. */
  var form = document.querySelector("form[data-form-demo]");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var ok = form.querySelector(".form-ok");
      form.querySelectorAll("input, select, textarea, button").forEach(function (el) { el.disabled = true; });
      if (ok) { ok.hidden = false; ok.scrollIntoView({ behavior: "smooth", block: "nearest" }); }
    });
  }

  /* Botão flutuante some enquanto o botão principal do hero está na tela (evita sobreposição no celular) */
  var flut = document.querySelector(".whats-flutuante"), heroBtn = document.querySelector(".hero-acoes .btn, .pagina-hero .hero-acoes .btn");
  if (flut && heroBtn && "IntersectionObserver" in window) {
    new IntersectionObserver(function (en) { flut.classList.toggle("oculto", en[0].isIntersecting); }, { threshold: 0.4 }).observe(heroBtn);
  }

  /* Ano do rodapé */
  var ano = document.querySelector("[data-ano]");
  if (ano) ano.textContent = String(new Date().getFullYear());
})();

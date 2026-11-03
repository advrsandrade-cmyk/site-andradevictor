/* API do painel do blog — Andrade e Victor Advogados (Nexus Digital Group, 2026)
 * Cloudflare Worker + KV. Usuários com login e senha próprios, recuperação por e-mail (Resend)
 * e publicação dos artigos no repositório do site (GitHub) com um token guardado só aqui.
 *
 * Variáveis (wrangler.toml): GITHUB_REPO, BRANCH, SITE_ORIGIN, MAIL_FROM, MAIL_REPLY
 * Segredos (wrangler secret put): GITHUB_TOKEN, JWT_SECRET, RESEND_API_KEY
 * KV: PAINEL  →  user:<login> | reset:<token> | tent:<login> (tentativas de login)
 */

const SESSAO_HORAS = 12;
const RESET_HORAS = 72;
const PBKDF2_ITER = 120000;
const enc = new TextEncoder();

/* ---------- utilidades ---------- */
const json = (data, status = 200, extra = {}) => new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json; charset=utf-8", ...extra } });
const erro = (msg, status = 400) => json({ erro: msg }, status);
const b64u = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const b64uDec = (s) => Uint8Array.from(atob(s.replace(/-/g, "+").replace(/_/g, "/") + "=".repeat((4 - (s.length % 4)) % 4)), (c) => c.charCodeAt(0));
const aleatorio = (n = 32) => b64u(crypto.getRandomValues(new Uint8Array(n)));
const agora = () => Math.floor(Date.now() / 1000);
const normLogin = (s) => String(s || "").trim().toLowerCase().replace(/[^a-z0-9._@-]/g, "").slice(0, 80);
const emailOk = (s) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(s || ""));

async function hashSenha(senha, saltB64u) {
  const salt = saltB64u ? b64uDec(saltB64u) : crypto.getRandomValues(new Uint8Array(16));
  const chave = await crypto.subtle.importKey("raw", enc.encode(senha), "PBKDF2", false, ["deriveBits"]);
  const bits = await crypto.subtle.deriveBits({ name: "PBKDF2", hash: "SHA-256", salt, iterations: PBKDF2_ITER }, chave, 256);
  return { salt: b64u(salt), hash: b64u(bits) };
}
async function confereSenha(senha, u) {
  if (!u || !u.hash || !u.salt) return false;
  const { hash } = await hashSenha(senha, u.salt);
  if (hash.length !== u.hash.length) return false;
  let dif = 0;
  for (let i = 0; i < hash.length; i++) dif |= hash.charCodeAt(i) ^ u.hash.charCodeAt(i);
  return dif === 0;
}
function senhaForte(s) { return typeof s === "string" && s.length >= 8 && /[a-zA-Z]/.test(s) && /[0-9]/.test(s); }

async function hmac(secret, dados) {
  const k = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return b64u(await crypto.subtle.sign("HMAC", k, enc.encode(dados)));
}
async function criarSessao(env, u) {
  const corpo = b64u(enc.encode(JSON.stringify({ l: u.login, p: u.papel, exp: agora() + SESSAO_HORAS * 3600, v: u.versao || 1 })));
  return corpo + "." + (await hmac(env.JWT_SECRET, corpo));
}
async function lerSessao(env, req) {
  const auth = req.headers.get("authorization") || "";
  const tok = auth.startsWith("Bearer ") ? auth.slice(7) : "";
  const [corpo, ass] = tok.split(".");
  if (!corpo || !ass) return null;
  if ((await hmac(env.JWT_SECRET, corpo)) !== ass) return null;
  let d; try { d = JSON.parse(new TextDecoder().decode(b64uDec(corpo))); } catch { return null; }
  if (!d.exp || d.exp < agora()) return null;
  const u = await env.PAINEL.get("user:" + d.l, "json");
  if (!u || (u.versao || 1) !== d.v) return null;   // trocar a senha invalida sessões antigas
  return u;
}
const publico = (u) => ({ login: u.login, nome: u.nome, email: u.email, papel: u.papel, criado: u.criado, senhaDefinida: !!u.hash });

/* ---------- e-mail (Resend) ---------- */
async function enviarEmail(env, para, assunto, html) {
  if (!env.RESEND_API_KEY) return { ok: false, motivo: "RESEND_API_KEY não configurada" };
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST", headers: { authorization: "Bearer " + env.RESEND_API_KEY, "content-type": "application/json" },
    body: JSON.stringify({ from: env.MAIL_FROM, to: [para], reply_to: env.MAIL_REPLY || undefined, subject: assunto, html }),
  });
  return { ok: r.ok, status: r.status, motivo: r.ok ? "" : (await r.text()).slice(0, 300) };
}
function emailRedefinir(env, u, link, novo) {
  const titulo = novo ? "Seu acesso ao painel do blog" : "Redefinir a senha do painel do blog";
  const intro = novo ? `Olá, ${u.nome}. Seu usuário no painel do blog do site foi criado. Defina sua senha pelo link abaixo (vale por ${RESET_HORAS} horas).`
                     : `Olá, ${u.nome}. Recebemos um pedido para redefinir a senha do seu usuário no painel do blog. Se não foi você, ignore este e-mail. O link vale por ${RESET_HORAS} horas.`;
  return `<div style="font-family:Arial,sans-serif;max-width:520px;margin:auto;color:#1a1a1c"><h2 style="font-weight:600">Andrade &amp; Victor · Painel do blog</h2><p>${intro}</p>
  <p style="margin:24px 0"><a href="${link}" style="background:#b8964f;color:#1a1305;padding:12px 18px;border-radius:6px;text-decoration:none;font-weight:700">${novo ? "Definir minha senha" : "Redefinir senha"}</a></p>
  <p style="font-size:13px;color:#666">Login: <b>${u.login}</b><br>Se o botão não abrir, copie este endereço: ${link}</p>
  <p style="font-size:12px;color:#999">Painel em ${env.SITE_ORIGIN}/admin/ · mantido pela Nexus Digital Group</p></div>`;
}
async function gerarLinkRedefinir(env, u) {
  const token = aleatorio(32);
  await env.PAINEL.put("reset:" + token, JSON.stringify({ login: u.login, exp: agora() + RESET_HORAS * 3600 }), { expirationTtl: RESET_HORAS * 3600 });
  return `${env.SITE_ORIGIN}/admin/#redefinir=${token}`;
}

/* ---------- GitHub ---------- */
async function gh(env, caminho, init = {}) {
  const r = await fetch(`https://api.github.com/repos/${env.GITHUB_REPO}/contents/${caminho}${init.method && init.method !== "GET" ? "" : "?ref=" + env.BRANCH}`, {
    ...init, headers: { authorization: "Bearer " + env.GITHUB_TOKEN, accept: "application/vnd.github+json", "content-type": "application/json", "user-agent": "painel-andradevictor", ...(init.headers || {}) },
  });
  const texto = await r.text();
  let dados = null; try { dados = JSON.parse(texto); } catch {}
  return { ok: r.ok, status: r.status, dados, texto };
}
const b64utf8 = (s) => btoa(unescape(encodeURIComponent(s)));
const slugOk = (s) => /^[a-z0-9][a-z0-9-]{2,80}$/.test(s);

/* ---------- limite de tentativas ---------- */
async function tentativas(env, chave) { return (await env.PAINEL.get("tent:" + chave, "json")) || { n: 0 }; }
async function registraTentativa(env, chave, ok) {
  if (ok) { await env.PAINEL.delete("tent:" + chave); return; }
  const t = await tentativas(env, chave); t.n += 1;
  await env.PAINEL.put("tent:" + chave, JSON.stringify(t), { expirationTtl: 900 });
}

/* ---------- rotas ---------- */
export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const origem = req.headers.get("origin") || "";
    const permitidas = [env.SITE_ORIGIN, "http://localhost:3500", "http://127.0.0.1:3500"];
    const cors = { "access-control-allow-origin": permitidas.includes(origem) ? origem : env.SITE_ORIGIN, "access-control-allow-methods": "GET,POST,PUT,DELETE,OPTIONS", "access-control-allow-headers": "authorization,content-type", "access-control-max-age": "86400", vary: "origin" };
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    const resp = async () => {
      try { return await rotear(req, env, url); }
      catch (e) { return erro("Erro interno: " + (e && e.message ? e.message : String(e)), 500); }
    };
    const r = await resp();
    Object.entries(cors).forEach(([k, v]) => r.headers.set(k, v));
    return r;
  },
};

async function rotear(req, env, url) {
  const p = url.pathname.replace(/\/+$/, "") || "/";
  const corpo = req.method === "POST" || req.method === "PUT" ? await req.json().catch(() => ({})) : {};
  const ip = req.headers.get("cf-connecting-ip") || "ip";

  if (p === "/" && req.method === "GET") return json({ servico: "painel-andradevictor", ok: true });

  /* --- autenticação --- */
  if (p === "/entrar" && req.method === "POST") {
    const login = normLogin(corpo.login);
    const t = await tentativas(env, login + "|" + ip);
    if (t.n >= 6) return erro("Muitas tentativas. Aguarde 15 minutos ou use \"Esqueci a senha\".", 429);
    const u = login ? await env.PAINEL.get("user:" + login, "json") : null;
    const ok = u && u.ativo !== false && (await confereSenha(String(corpo.senha || ""), u));
    await registraTentativa(env, login + "|" + ip, !!ok);
    if (!ok) return erro(u && !u.hash ? "Este usuário ainda não definiu a senha. Use \"Esqueci a senha\" para receber o link." : "Login ou senha incorretos.", 401);
    u.ultimoAcesso = agora(); await env.PAINEL.put("user:" + u.login, JSON.stringify(u));
    return json({ token: await criarSessao(env, u), usuario: publico(u) });
  }
  if (p === "/recuperar" && req.method === "POST") {
    const login = normLogin(corpo.login);
    const t = await tentativas(env, "rec|" + ip);
    if (t.n >= 5) return erro("Muitos pedidos. Tente novamente em 15 minutos.", 429);
    await registraTentativa(env, "rec|" + ip, false);
    let u = login ? await env.PAINEL.get("user:" + login, "json") : null;
    if (!u && emailOk(login)) {   // permite recuperar pelo e-mail cadastrado
      const lista = await env.PAINEL.list({ prefix: "user:" });
      for (const k of lista.keys) { const x = await env.PAINEL.get(k.name, "json"); if (x && x.email && x.email.toLowerCase() === login) { u = x; break; } }
    }
    if (u && u.email) {
      const link = await gerarLinkRedefinir(env, u);
      const r = await enviarEmail(env, u.email, "Redefinir a senha do painel do blog", emailRedefinir(env, u, link, !u.hash));
      if (!r.ok) return erro("Não foi possível enviar o e-mail agora (" + r.motivo + "). Fale com a Nexus.", 502);
    }
    return json({ ok: true, mensagem: "Se o usuário existir, o link de redefinição foi enviado para o e-mail cadastrado." });
  }
  if (p === "/redefinir" && req.method === "POST") {
    const tok = String(corpo.token || "");
    const r = tok ? await env.PAINEL.get("reset:" + tok, "json") : null;
    if (!r || r.exp < agora()) return erro("Link inválido ou vencido. Peça um novo em \"Esqueci a senha\".", 400);
    if (!senhaForte(corpo.senha)) return erro("A senha precisa ter pelo menos 8 caracteres, com letras e números.");
    const u = await env.PAINEL.get("user:" + r.login, "json");
    if (!u) return erro("Usuário não encontrado.", 404);
    Object.assign(u, await hashSenha(corpo.senha), { versao: (u.versao || 1) + 1, senhaEm: agora() });
    await env.PAINEL.put("user:" + u.login, JSON.stringify(u));
    await env.PAINEL.delete("reset:" + tok);
    return json({ ok: true, token: await criarSessao(env, u), usuario: publico(u) });
  }
  if (p === "/redefinir" && req.method === "GET") {   // o painel usa para mostrar o nome na tela de definir senha
    const r = await env.PAINEL.get("reset:" + (url.searchParams.get("token") || ""), "json");
    if (!r || r.exp < agora()) return erro("Link inválido ou vencido.", 400);
    const u = await env.PAINEL.get("user:" + r.login, "json");
    return json({ login: u.login, nome: u.nome, novo: !u.hash });
  }

  /* --- a partir daqui, precisa estar logado --- */
  const eu = await lerSessao(env, req);
  if (!eu) return erro("Sessão inválida ou expirada. Entre de novo.", 401);

  if (p === "/eu" && req.method === "GET") return json({ usuario: publico(eu) });
  if (p === "/senha" && req.method === "POST") {
    if (!(await confereSenha(String(corpo.atual || ""), eu))) return erro("A senha atual não confere.", 403);
    if (!senhaForte(corpo.nova)) return erro("A nova senha precisa ter pelo menos 8 caracteres, com letras e números.");
    Object.assign(eu, await hashSenha(corpo.nova), { versao: (eu.versao || 1) + 1, senhaEm: agora() });
    await env.PAINEL.put("user:" + eu.login, JSON.stringify(eu));
    return json({ ok: true, token: await criarSessao(env, eu) });
  }
  if (p === "/email" && req.method === "POST") {
    if (!emailOk(corpo.email)) return erro("E-mail inválido.");
    if (!(await confereSenha(String(corpo.senha || ""), eu))) return erro("Confirme com a sua senha atual.", 403);
    eu.email = String(corpo.email).trim().toLowerCase();
    await env.PAINEL.put("user:" + eu.login, JSON.stringify(eu));
    return json({ ok: true, usuario: publico(eu) });
  }

  /* --- artigos --- */
  if (p === "/post" && req.method === "PUT") {
    const slug = String(corpo.slug || "");
    if (!slugOk(slug)) return erro("Endereço (slug) inválido: use letras minúsculas, números e hífens.");
    if (!corpo.conteudo || String(corpo.conteudo).length > 200000) return erro("Conteúdo vazio ou grande demais.");
    const caminho = `src/blog/${slug}.md`;
    const atual = await gh(env, caminho);
    const body = { message: `${atual.ok ? "Atualiza" : "Novo"} artigo: ${slug} (por ${eu.nome})`, content: b64utf8(String(corpo.conteudo)), branch: env.BRANCH, committer: { name: "Painel do blog", email: "painel@andradevictoradvogados.com.br" } };
    if (atual.ok && atual.dados && atual.dados.sha) body.sha = atual.dados.sha;
    const r = await gh(env, caminho, { method: "PUT", body: JSON.stringify(body) });
    if (!r.ok) return erro("GitHub recusou a gravação (" + r.status + "): " + ((r.dados && r.dados.message) || r.texto.slice(0, 200)), 502);
    return json({ ok: true, novo: !atual.ok, commit: r.dados && r.dados.commit ? r.dados.commit.sha : null });
  }
  if (p.startsWith("/post/") && req.method === "DELETE") {
    const slug = p.slice(6);
    if (!slugOk(slug)) return erro("Slug inválido.");
    const caminho = `src/blog/${slug}.md`;
    const atual = await gh(env, caminho);
    if (!atual.ok) return erro("Artigo não encontrado no site.", 404);
    const r = await gh(env, caminho, { method: "DELETE", body: JSON.stringify({ message: `Exclui artigo: ${slug} (por ${eu.nome})`, sha: atual.dados.sha, branch: env.BRANCH }) });
    if (!r.ok) return erro("GitHub recusou a exclusão (" + r.status + ").", 502);
    return json({ ok: true });
  }
  if (p === "/post" && req.method === "GET") {   // conteúdo-fonte de um artigo (para editar rascunhos ainda não publicados)
    const slug = url.searchParams.get("slug") || "";
    if (!slugOk(slug)) return erro("Slug inválido.");
    const r = await gh(env, `src/blog/${slug}.md`);
    if (!r.ok) return erro("Artigo não encontrado.", 404);
    return json({ slug, conteudo: decodeURIComponent(escape(atob(r.dados.content.replace(/\n/g, "")))) });
  }

  /* --- usuários (só administradores) --- */
  if (p === "/usuarios" && req.method === "GET") {
    if (eu.papel !== "admin") return erro("Só administradores.", 403);
    const lista = await env.PAINEL.list({ prefix: "user:" });
    const us = [];
    for (const k of lista.keys) { const x = await env.PAINEL.get(k.name, "json"); if (x) us.push(publico(x)); }
    return json({ usuarios: us });
  }
  if (p === "/usuarios" && req.method === "POST") {
    if (eu.papel !== "admin") return erro("Só administradores.", 403);
    const login = normLogin(corpo.login);
    if (login.length < 3) return erro("Login inválido (mínimo 3 caracteres).");
    if (!emailOk(corpo.email)) return erro("E-mail inválido.");
    if (await env.PAINEL.get("user:" + login)) return erro("Já existe um usuário com esse login.", 409);
    const u = { login, nome: String(corpo.nome || login).trim().slice(0, 80), email: String(corpo.email).trim().toLowerCase(), papel: corpo.papel === "admin" ? "admin" : "editor", criado: agora(), versao: 1 };
    await env.PAINEL.put("user:" + login, JSON.stringify(u));
    const link = await gerarLinkRedefinir(env, u);
    const r = corpo.enviarEmail === false ? { ok: false, motivo: "não solicitado" } : await enviarEmail(env, u.email, "Seu acesso ao painel do blog", emailRedefinir(env, u, link, true));
    return json({ ok: true, usuario: publico(u), link, emailEnviado: r.ok, motivo: r.motivo || "" });
  }
  if (p.startsWith("/usuarios/") && req.method === "POST") {   // reenviar link de definição de senha
    if (eu.papel !== "admin") return erro("Só administradores.", 403);
    const u = await env.PAINEL.get("user:" + normLogin(p.slice(10)), "json");
    if (!u) return erro("Usuário não encontrado.", 404);
    const link = await gerarLinkRedefinir(env, u);
    const r = corpo.enviarEmail === false ? { ok: false, motivo: "não solicitado" } : await enviarEmail(env, u.email, "Redefinir a senha do painel do blog", emailRedefinir(env, u, link, !u.hash));
    return json({ ok: true, link, emailEnviado: r.ok, motivo: r.motivo || "" });
  }
  if (p.startsWith("/usuarios/") && req.method === "DELETE") {
    if (eu.papel !== "admin") return erro("Só administradores.", 403);
    const login = normLogin(p.slice(10));
    if (login === eu.login) return erro("Você não pode excluir o próprio usuário.");
    await env.PAINEL.delete("user:" + login);
    return json({ ok: true });
  }
  return erro("Rota não encontrada.", 404);
}

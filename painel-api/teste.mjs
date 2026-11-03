// Teste local da API sem Cloudflare: KV em memória + Request/Response do Node.
import worker from "./worker.js";
const store = new Map();
const PAINEL = {
  async get(k, t) { const v = store.get(k); if (v === undefined) return null; return t === "json" ? JSON.parse(v) : v; },
  async put(k, v) { store.set(k, v); }, async delete(k) { store.delete(k); },
  async list({ prefix }) { return { keys: [...store.keys()].filter(k => k.startsWith(prefix)).map(name => ({ name })) }; },
};
const env = { PAINEL, GITHUB_REPO: "x/y", BRANCH: "main", SITE_ORIGIN: "https://andradevictoradvogados.com.br", MAIL_FROM: "a@b", JWT_SECRET: "segredo", GITHUB_TOKEN: "t" };
const call = async (method, path, body, token) => {
  const r = await worker.fetch(new Request("https://api.local" + path, { method, headers: { "content-type": "application/json", origin: env.SITE_ORIGIN, ...(token ? { authorization: "Bearer " + token } : {}) }, body: body ? JSON.stringify(body) : undefined }), env);
  return { status: r.status, cors: r.headers.get("access-control-allow-origin"), j: await r.json() };
};
const ok = (c, m) => console.log((c ? "✓ " : "✗ ") + m);
await PAINEL.put("user:nexus", JSON.stringify({ login: "nexus", nome: "Nexus Digital", email: "nexusdigitalgrp@gmail.com", papel: "admin", criado: 0, versao: 1 }));
let r = await call("POST", "/entrar", { login: "nexus", senha: "x" }); ok(r.status === 401 && /ainda não definiu/.test(r.j.erro), "entrar sem senha definida → " + r.j.erro);
await PAINEL.put("reset:tok123", JSON.stringify({ login: "nexus", exp: 9999999999 }));
r = await call("GET", "/redefinir?token=tok123"); ok(r.status === 200 && r.j.novo === true, "GET redefinir identifica usuário novo");
r = await call("POST", "/redefinir", { token: "tok123", senha: "fraca" }); ok(r.status === 400, "senha fraca recusada");
r = await call("POST", "/redefinir", { token: "tok123", senha: "Senha1234" }); ok(r.status === 200 && r.j.token, "definir senha devolve sessão");
let T = r.j.token;
r = await call("POST", "/redefinir", { token: "tok123", senha: "Senha1234" }); ok(r.status === 400, "token de redefinição é de uso único");
r = await call("GET", "/eu", null, T); ok(r.status === 200 && r.j.usuario.login === "nexus" && r.cors === env.SITE_ORIGIN, "sessão válida + CORS");
r = await call("POST", "/entrar", { login: "nexus", senha: "Senha1234" }); ok(r.status === 200, "login com senha");
for (let i = 0; i < 6; i++) await call("POST", "/entrar", { login: "nexus", senha: "errada" });
r = await call("POST", "/entrar", { login: "nexus", senha: "Senha1234" }); ok(r.status === 429, "bloqueio após 6 erros → " + r.j.erro);
store.delete("tent:nexus|ip");
r = await call("POST", "/usuarios", { login: "Ricardo", nome: "Ricardo Andrade", email: "andradevictoradvogados@gmail.com", enviarEmail: false }, T); ok(r.status === 200 && r.j.usuario.login === "ricardo" && /#redefinir=/.test(r.j.link), "admin cria usuário e recebe link");
r = await call("GET", "/usuarios", null, T); ok(r.status === 200 && r.j.usuarios.length === 2, "lista usuários");
r = await call("POST", "/senha", { atual: "Senha1234", nova: "Nova12345" }, T); ok(r.status === 200, "troca de senha");
r = await call("GET", "/eu", null, T); ok(r.status === 401, "sessão antiga invalidada após troca de senha");
r = await call("POST", "/entrar", { login: "nexus", senha: "Nova12345" }); T = r.j.token; ok(r.status === 200, "login com a nova senha");
r = await call("POST", "/recuperar", { login: "andradevictoradvogados@gmail.com" }); ok(r.status === 502 && /RESEND/.test(r.j.erro), "recuperar sem Resend avisa (" + r.j.erro.slice(0, 60) + ")");
r = await call("PUT", "/post", { slug: "Teste Ruim", conteudo: "x" }, T); ok(r.status === 400, "slug inválido recusado");
const rt = await call("POST", "/entrar", { login: "ricardo", senha: "x" }); ok(rt.status === 401, "ricardo sem senha ainda não entra");
r = await call("GET", "/usuarios", null, (await (async () => { await PAINEL.put("reset:t2", JSON.stringify({ login: "ricardo", exp: 9999999999 })); const x = await call("POST", "/redefinir", { token: "t2", senha: "Ricardo123" }); return x.j.token; })())); ok(r.status === 403, "editor não lista usuários");
r = await call("DELETE", "/usuarios/ricardo", null, T); ok(r.status === 200, "admin exclui usuário");
